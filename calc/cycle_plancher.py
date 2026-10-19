"""Cycle de realisation d'une zone de plancher : durees, planning, cout.

Chaine imposee par la fiche du module :
  quantites V3 -> cadences et effectifs -> duree -> cout -> planning -> valeur acquise.

DEUX CONTRE-CALCULS, qui ne mesurent pas la meme chose et ne doivent pas etre
confondus :
  1. duree d'une tache : cadence UNITAIRE x effectif, contre RENDEMENT D'EQUIPE
     declare separement. Les deux sont des hypotheses V3 ; les comparer verifie
     qu'elles sont mutuellement coherentes, pas qu'elles sont vraies.
  2. duree du CYCLE : parcours avant/arriere contre enumeration des chemins
     (calc/cpm.py). Les deux calculent la MEME grandeur par deux algorithmes :
     elles doivent coincider exactement.

Note de methode. La fiche de l'Etape 0 annoncait « duree par cadences contre duree
par chemin critique ». Ces deux grandeurs ne sont pas comparables : la somme des
durees et le chemin critique different par construction, c'est tout l'objet du CPM.
L'ecart entre les deux est un RESULTAT a commenter (le gain du recouvrement), pas
un contre-calcul. Consigne dans DECISIONS.md.
"""
from __future__ import annotations
import json, math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from cpm import Tache, contre_calcul, voie_A_parcours
from plancher import quantites_zone, fourchette_acier

RACINE = pathlib.Path(__file__).resolve().parent.parent


def durees_taches(d: dict, q: dict) -> dict:
    c, e = d["cadences"], d["effectifs"]
    h = e["heures_par_jour"]

    coffrage = q["coffrage_m2"] / (c["coffrage_dalle_m2_j"]["valeur"] * e["coffreurs"])
    ferr_poutres = q["acier_poutres_kg"] / (c["ferraillage_poutre_kg_j"]["valeur"] * e["ferrailleurs_poutres"])
    ferr_dalle = q["acier_dalle_kg"] / (c["ferraillage_dalle_kg_j"]["valeur"] * e["ferrailleurs_dalle"])
    betonnage = q["beton_m3"] / c["betonnage_m3_h"]["valeur"] / h

    # --- contre-calcul 1 : le coffrage par le rendement d'EQUIPE declare a part
    coffrage_equipe = q["coffrage_m2"] / c["rendement_equipe_coffrage_m2_j"]["valeur"]
    ecart = abs(coffrage - coffrage_equipe) / coffrage * 100

    # Quelle PART de la fourchette declaree du rendement d'equipe passe la tolerance ?
    # C'est la seule facon honnete de presenter ce controle : il est satisfait par le
    # point retenu, pas par les donnees. Les bornes se posent sans iteration :
    # |Q/R - D| <= tol.D  <=>  Q/(D(1+tol)) <= R <= Q/(D(1-tol))
    tol = 5.0 / 100.0
    r_lo = q["coffrage_m2"] / (coffrage * (1 + tol))
    r_hi = q["coffrage_m2"] / (coffrage * (1 - tol))
    f_lo, f_hi = c["rendement_equipe_coffrage_m2_j"]["fourchette"]
    couvert = max(0.0, min(r_hi, f_hi) - max(r_lo, f_lo))

    return {
        "coffrage_j": round(coffrage, 2),
        "ferraillage_poutres_j": round(ferr_poutres, 2),
        "ferraillage_dalle_j": round(ferr_dalle, 2),
        "betonnage_j": round(betonnage, 2),
        "betonnage_h": round(q["beton_m3"] / c["betonnage_m3_h"]["valeur"], 2),
        "contre_calcul_duree_coffrage": {
            "voie_A_cadence_unitaire_x_effectif_j": round(coffrage, 3),
            "voie_B_rendement_d_equipe_j": round(coffrage_equipe, 3),
            "ecart_pct": round(ecart, 2),
            "tolerance_pct": 5.0,
            "ce_que_ce_controle_prouve": (
                "que les deux hypotheses V3 (cadence unitaire et rendement d'equipe) "
                "sont mutuellement coherentes. Il ne prouve PAS qu'elles sont justes : "
                "seul un attachement reel le dirait."
            ),
            "verdict": "OK" if ecart <= 5.0 else "LES DEUX HYPOTHESES V3 SE CONTREDISENT",
            # Ce que le controle ne dit pas de lui-meme : sur quelle largeur il tient.
            "plage_de_rendement_qui_passe_m2_j": [round(r_lo, 1), round(r_hi, 1)],
            "fourchette_declaree_m2_j": [f_lo, f_hi],
            "part_de_la_fourchette_qui_passe_pct": round(couvert / (f_hi - f_lo) * 100, 1),
        },
    }


def cadence_rotation(t: dict) -> dict:
    """Cadence de rotation d'une zone : tous les combien une zone redemarre.

    Elle est bornee par la plus longue des taches qui mobilisent une equipe DEDIEE —
    une equipe ne peut etre que sur une zone a la fois — plus le betonnage, qui
    immobilise la zone, la pompe et la grue pour tout le monde.

    La premiere version de cette regle oubliait le ferraillage des POUTRES. Sans effet
    sur le cas de reference, ou le ferraillage de dalle est plus long et masque
    l'oubli ; decisif des qu'on renforce l'equipe de dalle, puisque c'est alors le
    ferraillage des poutres qui prend le relais. Le module enonce justement cette
    regle — « renforcer une tache critique ne garantit un gain que jusqu'a ce qu'un
    autre chemin prenne le relais » — et sa propre formule la violait.
    """
    dediees = {
        "coffrage_j": "coffreurs",
        "ferraillage_poutres_j": "ferrailleurs_poutres",
        "ferraillage_dalle_j": "ferrailleurs_dalle",
    }
    durees = {cle: t[cle] for cle in dediees}
    cle_max = max(durees, key=durees.get)
    cad = durees[cle_max] + t["betonnage_j"]
    return {
        "cadence_j": round(cad, 2),
        "tache_qui_borne": cle_max,
        "equipe_qui_borne": dediees[cle_max],
        "durees_des_equipes_dediees_j": {k: round(v, 2) for k, v in durees.items()},
        "regle": ("max(taches a equipe dediee) + betonnage. Le betonnage s'ajoute parce "
                  "qu'il immobilise la zone entiere ; la cure et le decoffrage ne "
                  "comptent pas, ils n'occupent aucune equipe."),
    }


def reseau_zone(t: dict, cz: dict) -> list[Tache]:
    """Le reseau d'une zone. Les recouvrements sont le coeur du metier : le
    ferraillage des poutres demarre avant la fin du coffrage, et le ferraillage de
    dalle avant la fin de celui des poutres.

    Les cinq parametres qui ne viennent ni d'une quantite ni d'une cadence — cure,
    decoffrage, point d'arret et les deux taux de recouvrement — sont LUS dans
    `data/cycle_zone`. Ils etaient ecrits en dur ici : ils pesent pres d'un tiers du
    cycle et la totalite du gain de recouvrement, sans fourchette ni registre.
    """
    r1 = cz["recouvrement_coffrage_ferraillage_poutres_pct"]["valeur"] / 100.0
    r2 = cz["recouvrement_ferraillage_poutres_dalle_pct"]["valeur"] / 100.0
    return [
        Tache("COF", "Coffrage dalle et poutres", t["coffrage_j"]),
        Tache("FEP", "Ferraillage des poutres", t["ferraillage_poutres_j"],
              [("COF", -t["coffrage_j"] * r1)]),
        Tache("FED", "Ferraillage de la dalle", t["ferraillage_dalle_j"],
              [("FEP", -t["ferraillage_poutres_j"] * r2), "COF"]),
        Tache("PTA", "Point d'arrêt : visa du ferraillage avant coulage",
              cz["point_arret_visa_ferraillage_j"]["valeur"], ["FED"]),
        Tache("BET", "Bétonnage et surfaçage", t["betonnage_j"], ["PTA"]),
        Tache("CUR", "Cure et attente de résistance",
              cz["cure_avant_decoffrage_j"]["valeur"], ["BET"]),
        Tache("DEC", "Décoffrage, étais de reprise maintenus",
              cz["decoffrage_j"]["valeur"], ["CUR"]),
    ]


def effectifs_du_cycle(d: dict) -> dict:
    """Effectif present sur une zone, tache par tache, lu dans data/."""
    cz, e = d["cycle_zone"]["effectif_par_tache"], d["effectifs"]
    return {k: (e[v] if isinstance(v, str) else v)
            for k, v in cz.items() if not k.startswith("_")}


def histogramme_plancher(d: dict, reseau: list[Tache], debuts: dict, duree_totale: float) -> list:
    """Effectif present sur le plancher, jour par jour.

    Construit sur les DATES du reseau de zone, et non sur une chaine de `elif` qui
    supposait les taches en file indienne. L'ancienne version etait structurellement
    incapable de montrer deux equipes presentes le meme jour sur la meme zone, alors
    que le recouvrement — dont le module fait sa demonstration — consiste exactement
    en cela : elle contredisait le Gantt de la figure voisine.
    """
    from cpm import voie_A_parcours
    r = voie_A_parcours(reseau)
    eff = effectifs_du_cycle(d)
    base = d["effectifs"]
    jours = []
    for k in range(int(math.ceil(duree_totale)) + 1):
        n, zone_active = 0, False
        for cle, debut_zone in debuts.items():
            for tache in reseau:
                deb, fin = r["tot"][tache.id]
                if debut_zone + deb <= k < debut_zone + fin:
                    n += eff.get(tache.id, 0)
                    if eff.get(tache.id, 0):
                        zone_active = True
        # l'encadrement n'est present que si une equipe de production l'est
        if zone_active:
            n += base["chef_equipe"] + base["grutier"]
        jours.append({"j": k, "n": n})
    return jours


def cout_zone(d: dict, q: dict, t: dict) -> dict:
    p = d["prix_unitaires_MAD"]["postes"]
    e = d["effectifs"]
    beton = q["beton_m3"] * p["beton_m3"]["valeur"]
    acier = q["acier_kg"] * p["acier_kg"]["valeur"]
    coffrage = q["coffrage_m2"] * p["coffrage_m2"]["valeur"]
    # main d'oeuvre : heures effectivement mobilisees, poste par poste
    h = e["heures_par_jour"]
    heures = (t["coffrage_j"] * e["coffreurs"]
              + t["ferraillage_poutres_j"] * e["ferrailleurs_poutres"]
              + t["ferraillage_dalle_j"] * e["ferrailleurs_dalle"]
              + t["betonnage_j"] * e["equipe_betonnage"]) * h
    mo = heures * p["main_oeuvre_h"]["valeur"]
    total = beton + acier + coffrage
    return {
        "beton_MAD": round(beton), "acier_MAD": round(acier), "coffrage_MAD": round(coffrage),
        "total_fournitures_et_mise_en_oeuvre_MAD": round(total),
        "heures_de_main_oeuvre": round(heures, 1),
        "main_oeuvre_MAD": round(mo),
        "note_double_compte": (
            "Les prix unitaires de beton, d'acier et de coffrage sont des prix POSES, "
            "main d'oeuvre comprise. La ligne « main d'oeuvre » ci-dessus est donc un "
            "CONTROLE de coherence, pas un poste a additionner : l'ajouter au total "
            "compterait la main d'oeuvre deux fois. C'est l'erreur classique du metre."
        ),
        "part_main_oeuvre_dans_le_total_pct": round(mo / total * 100, 1),
        "cout_au_m2_MAD": round(total / q["surface_m2"]),
        "coherence_prix_horaire": _coherence_prix_horaire(d, total, heures, mo),
    }


def _coherence_prix_horaire(d: dict, total: float, heures: float, mo: float) -> dict:
    """Le prix horaire et les prix unitaires sont DEUX hypotheses V3 independantes.
    Rien ne garantit qu'elles se tiennent : ce controle le verifie, et rapporte
    l'ecart au lieu de le taire."""
    r = d["ratios_V3"]["part_main_oeuvre_directe_pct"]
    part = mo / total * 100
    lo, hi = r["fourchette"]
    implique = total * r["valeur"] / 100 / heures
    # On CHIFFRE chaque cause invoquee, au lieu de les enumerer. Si leur somme
    # n'explique pas l'ecart, il faut le dire : c'est le cas ici.
    e = d["effectifs"]
    h = e["heures_par_jour"]
    px = d["prix_unitaires_MAD"]["postes"]["main_oeuvre_h"]
    causes = []
    base = mo / total * 100
    causes.append({"cause": "equipes de production seules, prix horaire au point declare",
                   "part_pct": round(base, 2)})
    # + encadrement et grutier, presents toute la duree du cycle
    h_enc = (e["chef_equipe"] + e["grutier"]) * h * 8.56
    avec_enc = (heures + h_enc) * px["valeur"] / total * 100
    causes.append({"cause": "+ chef d'equipe et grutier", "part_pct": round(avec_enc, 2)})
    # + prix horaire au haut de sa fourchette
    haut = (heures + h_enc) * px["fourchette"][1] / total * 100
    causes.append({"cause": "+ prix horaire au haut de sa fourchette", "part_pct": round(haut, 2)})
    reste = r["fourchette"][0] / haut
    return {
        "causes_chiffrees": causes,
        "part_apres_toutes_les_causes_pct": round(haut, 2),
        "facteur_encore_inexplique": round(reste, 1),
        "ce_qui_reste": (
            "Les causes invoquees ne suffisent pas : meme en comptant l'encadrement et en "
            "prenant le haut de la fourchette horaire, la part reste tres en dessous de la "
            "fourchette attendue. Le suspect le plus probable est ailleurs : des CADENCES "
            "optimistes d'un facteur deux a trois, qui sont l'entree de TOUTES les durees "
            "publiees. C'est une hypothese, pas une conclusion — seuls des attachements "
            "reels la confirmeraient ou l'infirmeraient."
        ),
        "part_constatee_pct": round(part, 1),
        "fourchette_attendue_pct": [lo, hi],
        "dans_la_fourchette": lo <= part <= hi,
        "prix_horaire_declare_MAD": d["prix_unitaires_MAD"]["postes"]["main_oeuvre_h"]["valeur"],
        "prix_horaire_implique_par_les_prix_unitaires_MAD": round(implique),
        "facteur": round(implique / d["prix_unitaires_MAD"]["postes"]["main_oeuvre_h"]["valeur"], 1),
        "lecture": (
            "L'ecart n'est pas une erreur de calcul : il vient de ce que les deux hypotheses "
            "ne decrivent pas la meme chose. Le prix horaire declare est celui d'un compagnon "
            "nu ; les heures comptees sont celles des quatre equipes de production seules, sans "
            "encadrement, grutier, approvisionnement ni moyens ; et les prix unitaires sont des "
            "prix POSES, qui portent en plus les materiaux, le materiel, les frais de chantier "
            "et la marge. Les additionner n'a pas de sens, et les comparer sans le dire non plus. "
            "C'est exactement ce qu'un sous-detail de prix met a plat, poste par poste (module D1)."
        ),
    }


def planning_chantier(d: dict, duree_zone: float, cadence_zone_j: float) -> dict:
    """Les 8 zones s'enchainent a une zone par cycle : le planning du plancher."""
    n = d["geometrie"]["mezzanine"]["zones_de_coulage"]["nb_zones"]
    taches = []
    for i in range(n):
        preds = [("Z%d" % i, -(duree_zone - cadence_zone_j))] if i else []
        taches.append(Tache("Z%d" % (i + 1), "Zone %d" % (i + 1), duree_zone, preds))
    r = contre_calcul(taches)
    return {"nb_zones": n, "duree_totale_j": round(r["voie_A_parcours_avant_arriere_j"], 2),
            "cadence_zone_j": cadence_zone_j, "contre_calcul": r,
            "debuts": {t.id: round(r["detail"]["tot"][t.id][0], 2) for t in taches}}


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    q = quantites_zone(d)
    q["fourchette_acier"] = fourchette_acier(d, q)
    t = durees_taches(d, q)
    reseau = reseau_zone(t, d["cycle_zone"])
    cc = contre_calcul(reseau)
    somme = sum(x.duree for x in reseau)
    cout = cout_zone(d, q, t)
    duree_zone = cc["voie_A_parcours_avant_arriere_j"]
    # la cadence de rotation : une zone tous les N jours, bornee par la tache la plus longue
    regle_cadence = cadence_rotation(t)
    cadence = round(regle_cadence["cadence_j"], 1)
    plan = planning_chantier(d, duree_zone, cadence)

    # --- date d'arret : DONNEE. L'avancement prevu a cette date s'en deduit.
    s_ = d["suivi"]
    jour_arret = float(s_["jour_arret_ouvre"])
    semaine_arret = jour_arret / s_["jours_ouvres_par_semaine"]

    # --- donnees des figures, calculees et non dessinees
    av = []
    for i in range(plan["nb_zones"]):
        if i < s_["zones_realisees_a_date"]:
            av.append("faite")
        elif i == s_["zones_realisees_a_date"]:
            av.append("en_cours")
        else:
            av.append("a_venir")
    z = d["geometrie"]["mezzanine"]["zones_de_coulage"]
    poutre = next(x for x in d["elements"]["poutres"] if x["id"] == "PM1")

    # Vraie courbe en S : a chaque date, on somme l'avancement de CHAQUE zone.
    # Le demarrage est lent (une seule zone en cours), le milieu lineaire (plusieurs
    # zones se recouvrent), la fin lente a nouveau. Une formule lineaire donnait une
    # droite, ce qui n'est pas une courbe en S et n'apprend rien.
    def avancement_prevu(j):
        tot = 0.0
        for i in range(plan["nb_zones"]):
            deb = plan["debuts"]["Z%d" % (i + 1)]
            tot += min(1.0, max(0.0, (j - deb) / duree_zone))
        return tot / plan["nb_zones"] * 100

    reel_zones = s_["zones_realisees_a_date"] + s_["avancement_zone_en_cours_pct"] / 100.0
    prevu_arret = avancement_prevu(jour_arret)
    zones_prevues_arret = prevu_arret / 100 * plan["nb_zones"]

    courbe = []
    pas = plan["duree_totale_j"] / 32
    # La date d'arret est AJOUTEE aux abscisses. Sans elle, le dernier point du constat
    # tombait avant la date d'arret : l'ecart vertical lisible sur la figure n'etait pas
    # celui du tableau de valeur acquise, alors que la legende affirmait que c'etait SV.
    abscisses = sorted(set([round(k * pas, 1) for k in range(33)] + [round(jour_arret, 1)]))
    for j in abscisses:
        pt = {"j": round(j, 1), "prevu": round(avancement_prevu(j), 1)}
        courbe.append(pt)

    # LE CONSTAT N'EST PAS UNE COURBE. Les donnees ne portent qu'UN releve : les zones
    # faites a la date d'arret. La version precedente tracait vingt points de constat
    # obtenus en multipliant la courbe prevue par une constante — une prevision deguisee
    # en releve, dans la figure meme dont la legende interdit de les confondre. Tant
    # qu'il n'y a qu'un point, on publie un point.
    constat = [{"j": round(jour_arret, 1),
                "realise": round(reel_zones / plan["nb_zones"] * 100, 1)}]

    effectifs_jour = histogramme_plancher(d, reseau, plan["debuts"], plan["duree_totale_j"])
    _rz = voie_A_parcours(reseau)
    # --- variantes des exercices : leurs valeurs attendues sont CALCULEES, plus affirmees
    def variante_effectif(n_ferr_dalle, n_ferr_poutres=None):
        e2 = dict(d["effectifs"]); e2["ferrailleurs_dalle"] = n_ferr_dalle
        if n_ferr_poutres is not None:
            e2["ferrailleurs_poutres"] = n_ferr_poutres
        d2 = dict(d); d2["effectifs"] = e2
        t2 = durees_taches(d2, q)
        cc2 = contre_calcul(reseau_zone(t2, d["cycle_zone"]))
        dz = cc2["voie_A_parcours_avant_arriere_j"]
        rc2 = cadence_rotation(t2)
        cad = rc2["cadence_j"]
        pl = planning_chantier(d, dz, cad)
        # meme construction que l'histogramme publie : sur les DATES du reseau, et non
        # sur une chaine de `elif` qui supposait les taches en file indienne
        pointe = max(x["n"] for x in histogramme_plancher(
            d2, reseau_zone(t2, d["cycle_zone"]), pl["debuts"], pl["duree_totale_j"]))
        # Le coffrage d'une zone est immobilise du debut du coffrage a la fin du
        # decoffrage, soit un cycle entier. A une cadence plus courte que le cycle,
        # plusieurs zones en detiennent en meme temps : c'est une CONTRAINTE, pas une
        # consequence. Un planning qui demande plus de tables que le parc n'existe pas.
        simultanees = max(1, math.ceil(dz / cad))      # zones coffrees en meme temps
        mobilise = round(simultanees * q["coffrage_m2"])
        stock = d["materiel"]["tables_coffrantes_m2"]
        return {"ferrailleurs_dalle": n_ferr_dalle,
                "ferrailleurs_poutres": e2["ferrailleurs_poutres"],
                "ferraillage_poutres_j": round(t2["ferraillage_poutres_j"], 2),
                "tache_qui_borne_la_cadence": rc2["tache_qui_borne"],
                "equipe_qui_borne_la_cadence": rc2["equipe_qui_borne"],
                "ferraillage_dalle_j": round(t2["ferraillage_dalle_j"], 2),
                "cycle_j": round(dz, 2), "cadence_j": cad,
                "duree_plancher_j": round(pl["duree_totale_j"], 1),
                "pointe_effectif": pointe,
                "zones_coffrees_simultanement": simultanees,
                "coffrage_mobilise_m2": mobilise,
                "stock_coffrage_declare_m2": stock,
                "deficit_coffrage_m2": max(0, mobilise - stock),
                "coffrage_suffisant": mobilise <= stock}

    res_variantes = {
        "reference": variante_effectif(d["effectifs"]["ferrailleurs_dalle"]),
        # Renforcer la SEULE equipe de dalle : le ferraillage des poutres prend le
        # relais et la cible n'est pas atteinte. C'est le cas que l'exercice 3 doit
        # montrer, et que la premiere version du module avait manque.
        "effectif_renforce": variante_effectif(12),
        # Renforcer les DEUX equipes de ferraillage : la seule variante qui tienne.
        "effectif_renforce_deux_equipes": variante_effectif(12, 6),
        "sous_estimation_si_coffrage_egale_surface_pct": round(
            (q["coffrage_m2"] - q["surface_m2"]) / q["coffrage_m2"] * 100, 1),
    }

    # --- coherence du planning avec le materiel declare (§ 4.3)
    _ref = res_variantes["reference"]
    # Les etais de REPRISE restent en place apres le decoffrage : le nombre de zones
    # etayees n'est pas le nombre de zones coffrees. Les confondre sous-compte le parc
    # d'etais, et c'est l'erreur que le module enseigne par ailleurs a ne pas commettre.
    etais_zone = q["surface_m2"] * d["materiel"]["etais_par_m2"]
    maintien = d["materiel"]["etais_de_reprise_maintenus_j"]["valeur"]
    zones_etayees = max(1, math.ceil(
        (duree_zone + maintien) / plan["cadence_zone_j"]))
    coherence_materiel = {
        "zones_coffrees_simultanement": _ref["zones_coffrees_simultanement"],
        "coffrage_mobilise_m2": _ref["coffrage_mobilise_m2"],
        "stock_declare_m2": _ref["stock_coffrage_declare_m2"],
        "marge_m2": _ref["stock_coffrage_declare_m2"] - _ref["coffrage_mobilise_m2"],
        "zones_etayees_simultanement": zones_etayees,
        "etais_necessaires": round(zones_etayees * etais_zone),
        "etais_si_on_ne_comptait_que_les_zones_coffrees": round(
            _ref["zones_coffrees_simultanement"] * etais_zone),
        "duree_de_maintien_des_etais_de_reprise_j": maintien,
        "verdict": ("OK" if _ref["coffrage_suffisant"]
                    else "LE PLANNING DEMANDE PLUS DE COFFRAGE QUE LE PARC DECLARE"),
        "regle": (
            "Le coffrage d'une zone est immobilise pendant un cycle entier. Le nombre de "
            "zones qui en detiennent en meme temps vaut ceil(cycle / cadence). Reduire la "
            "cadence sans ajouter de tables est impossible : c'est la contrainte que les "
            "plannings de rotation oublient le plus souvent."
        ),
    }

    # --- situation de travaux de l'exercice de revue critique.
    # Elle etait tapee a la main dans le contenu : douze nombres justes aujourd'hui, et
    # faux au premier changement de data/. Elle est desormais calculee comme le reste.
    # NB : surtout pas « av », qui porte deja la liste des etats de zone de la figure 1.
    # La premiere version de ce bloc l'a ecrasee, et la figure a perdu ses couleurs
    # d'avancement sans qu'aucun test ne le voie — c'est l'oeil sur la capture qui l'a vu.
    frac = d["suivi"]["avancement_zone_en_cours_pct"] / 100.0
    p_ = d["prix_unitaires_MAD"]["postes"]
    _postes = [
        ("beton", "m³", q["beton_m3"] * frac, p_["beton_m3"]["valeur"]),
        ("acier", "kg", q["acier_kg"] * frac, p_["acier_kg"]["valeur"]),
        ("coffrage", "m²", q["coffrage_m2"] * frac, p_["coffrage_m2"]["valeur"]),
    ]
    _mo_h = cout["heures_de_main_oeuvre"] * frac
    _mo = _mo_h * p_["main_oeuvre_h"]["valeur"]
    _juste = sum(x[2] * x[3] for x in _postes)
    situation = {
        "avancement_declare_pct": round(frac * 100, 1),
        "postes": [{"poste": n, "unite": u, "quantite": round(x, 1),
                    "prix_unitaire": pu, "montant_MAD": round(x * pu)} for n, u, x, pu in _postes],
        "main_oeuvre_h": round(_mo_h),
        "main_oeuvre_MAD": round(_mo),
        "total_presente_MAD": round(_juste + _mo),
        "total_juste_MAD": round(_juste),
        "double_compte_MAD": round(_mo),
        "ratio_coffrage_de_la_situation": round(
            (q["coffrage_m2"] * frac) / (q["surface_m2"] * frac), 3),
    }

    res = {
        "quantites": q, "durees": t, "variantes": res_variantes,
        "situation_exercice": situation,
        "regle_cadence": regle_cadence,
        "coherence_materiel": coherence_materiel,
        "suivi": {"jour_arret": round(jour_arret, 1), "semaine_arret": round(semaine_arret, 1),
                  "avancement_prevu_pct": round(prevu_arret, 1),
                  "zones_prevues_equivalentes": round(zones_prevues_arret, 2),
                  "libelle_arret": (
                      f"jour {jour_arret:.0f}, soit le {((jour_arret - 1) % 5) + 1:.0f}ᵉ jour "
                      f"de la semaine {math.floor((jour_arret - 1) / 5) + 1:.0f}")},
        "figures": {
            "zones": {"avancement_prevu": [
                          round(min(1.0, max(0.0, (jour_arret - plan["debuts"]["Z%d" % (i + 1)])
                                             / duree_zone)), 2)
                          for i in range(plan["nb_zones"])],
                      "longueur_m": z["longueur_zone_m"], "largeur_m": z["largeur_zone_m"],
                      "nb_zones": z["nb_zones"], "entraxe_poutres_m": poutre["entraxe_m"],
                      "avancement": av},
            "sequence": [x.nom for x in reseau],
            "gantt": [{"nom": x.nom, "debut": round(cc["detail"]["tot"][x.id][0], 2),
                       "duree": round(x.duree, 2),
                       "critique": x.id in cc["detail"]["critiques"]} for x in reseau],
            # Diagramme de rotation : les zones DANS LE TEMPS, phase par phase, plus
            # le coffrage immobilise jour par jour. La figure precedente (sequence)
            # etait un enchainement de blocs et de fleches sans cote ni duree, qui
            # dupliquait le Gantt de la zone sans rien ajouter — le § 8 l'interdit.
            "rotation": {
                "zones": [
                    {"zone": i + 1, "debut_j": round(plan["debuts"]["Z%d" % (i + 1)], 2),
                     "phases": [
                         {"id": x.id, "nom": x.nom,
                          "debut_j": round(_rz["tot"][x.id][0], 2),
                          "fin_j": round(_rz["tot"][x.id][1], 2)}
                         for x in reseau]}
                    for i in range(plan["nb_zones"])],
                "cadence_j": plan["cadence_zone_j"],
                "cycle_j": duree_zone,
                "coffrage_par_zone_m2": q["coffrage_m2"],
                "stock_coffrage_m2": d["materiel"]["tables_coffrantes_m2"],
                "coffrage_immobilise": [
                    {"j": k, "m2": round(sum(
                        1 for i in range(plan["nb_zones"])
                        if plan["debuts"]["Z%d" % (i + 1)] <= k
                        < plan["debuts"]["Z%d" % (i + 1)] + duree_zone) * q["coffrage_m2"])}
                    for k in range(int(math.ceil(plan["duree_totale_j"])) + 1)],
            },
            "courbe_s": {"points": courbe, "constat": constat},
            "constat_avancement": constat,
            "effectifs": effectifs_jour,
        },
        "cycle_zone": {
            "duree_j": duree_zone,
            "somme_des_durees_j": round(somme, 2),
            "gain_du_recouvrement_j": round(somme - duree_zone, 2),
            "gain_pct": round((somme - duree_zone) / somme * 100, 1),
            "chemin_critique": cc["chemin_critique"],
            "contre_calcul": {k: v for k, v in cc.items() if k != "detail"},
            "taches": [{"id": x.id, "nom": x.nom, "duree_j": round(x.duree, 2),
                        "debut_j": round(cc["detail"]["tot"][x.id][0], 2),
                        "marge_j": cc["detail"]["marges"][x.id],
                        "critique": x.id in cc["detail"]["critiques"]} for x in reseau],
        },
        "cout_zone": cout,
        "planning_plancher": plan,
    }
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "tranche-plancher.json").write_text(
        json.dumps(res, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("durees", "cycle_zone", "cout_zone")},
                     indent=2, ensure_ascii=False)[:2200])
