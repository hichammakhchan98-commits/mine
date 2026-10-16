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
from cpm import Tache, contre_calcul
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


def reseau_zone(t: dict, cure_j: float = 2.0) -> list[Tache]:
    """Le reseau d'une zone. Les recouvrements sont le coeur du metier : le
    ferraillage des poutres demarre avant la fin du coffrage, et le ferraillage de
    dalle avant la fin de celui des poutres."""
    return [
        Tache("COF", "Coffrage dalle et poutres", t["coffrage_j"]),
        Tache("FEP", "Ferraillage des poutres", t["ferraillage_poutres_j"],
              [("COF", -t["coffrage_j"] * 0.5)]),
        Tache("FED", "Ferraillage de la dalle", t["ferraillage_dalle_j"],
              [("FEP", -t["ferraillage_poutres_j"] * 0.4), "COF"]),
        Tache("PTA", "Point d'arrêt : visa du ferraillage avant coulage", 0.25, ["FED"]),
        Tache("BET", "Bétonnage et surfaçage", t["betonnage_j"], ["PTA"]),
        Tache("CUR", "Cure et attente de résistance", cure_j, ["BET"]),
        Tache("DEC", "Décoffrage, étais de reprise maintenus", 0.5, ["CUR"]),
    ]


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
    reseau = reseau_zone(t)
    cc = contre_calcul(reseau)
    somme = sum(x.duree for x in reseau)
    cout = cout_zone(d, q, t)
    duree_zone = cc["voie_A_parcours_avant_arriere_j"]
    # la cadence de rotation : une zone tous les N jours, bornee par la tache la plus longue
    cadence = round(max(t["coffrage_j"], t["ferraillage_dalle_j"]) + t["betonnage_j"], 1)
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
        if j <= jour_arret:
            # l'avancement reel suit la meme forme, cale sur le constat de la date d'arret
            pt["realise"] = round(avancement_prevu(j) * (reel_zones / zones_prevues_arret)
                                  if zones_prevues_arret else 0.0, 1)
        courbe.append(pt)

    e = d["effectifs"]
    effectifs_jour = []
    for k in range(int(plan["duree_totale_j"]) + 1):
        n = 0
        for i in range(plan["nb_zones"]):
            deb = plan["debuts"]["Z%d" % (i + 1)]
            if deb <= k < deb + t["coffrage_j"]:
                n += e["coffreurs"]
            elif deb <= k < deb + t["coffrage_j"] + t["ferraillage_poutres_j"]:
                n += e["ferrailleurs_poutres"]
            elif deb <= k < deb + duree_zone - 2.5:
                n += e["ferrailleurs_dalle"]
            elif deb <= k < deb + duree_zone:
                n += e["equipe_betonnage"]
        effectifs_jour.append({"j": k, "n": n + e["chef_equipe"] + e["grutier"]})

    # --- variantes des exercices : leurs valeurs attendues sont CALCULEES, plus affirmees
    def variante_effectif(n_ferr_dalle):
        e2 = dict(d["effectifs"]); e2["ferrailleurs_dalle"] = n_ferr_dalle
        d2 = dict(d); d2["effectifs"] = e2
        t2 = durees_taches(d2, q)
        cc2 = contre_calcul(reseau_zone(t2))
        dz = cc2["voie_A_parcours_avant_arriere_j"]
        cad = round(max(t2["coffrage_j"], t2["ferraillage_dalle_j"]) + t2["betonnage_j"], 2)
        pl = planning_chantier(d, dz, cad)
        pointe = 0
        for k in range(int(pl["duree_totale_j"]) + 1):
            n = 0
            for i in range(pl["nb_zones"]):
                deb = pl["debuts"]["Z%d" % (i + 1)]
                if deb <= k < deb + t2["coffrage_j"]:
                    n += e2["coffreurs"]
                elif deb <= k < deb + t2["coffrage_j"] + t2["ferraillage_poutres_j"]:
                    n += e2["ferrailleurs_poutres"]
                elif deb <= k < deb + dz - 2.5:
                    n += n_ferr_dalle
                elif deb <= k < deb + dz:
                    n += e2["equipe_betonnage"]
            pointe = max(pointe, n + e2["chef_equipe"] + e2["grutier"])
        # Le coffrage d'une zone est immobilise du debut du coffrage a la fin du
        # decoffrage, soit un cycle entier. A une cadence plus courte que le cycle,
        # plusieurs zones en detiennent en meme temps : c'est une CONTRAINTE, pas une
        # consequence. Un planning qui demande plus de tables que le parc n'existe pas.
        simultanees = max(1, math.ceil(dz / cad))      # zones coffrees en meme temps
        mobilise = round(simultanees * q["coffrage_m2"])
        stock = d["materiel"]["tables_coffrantes_m2"]
        return {"ferrailleurs_dalle": n_ferr_dalle,
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
        "effectif_renforce": variante_effectif(12),
        "sous_estimation_si_coffrage_egale_surface_pct": round(
            (q["coffrage_m2"] - q["surface_m2"]) / q["coffrage_m2"] * 100, 1),
    }

    # --- coherence du planning avec le materiel declare (§ 4.3)
    _ref = res_variantes["reference"]
    etais_zone = q["surface_m2"] * d["materiel"]["etais_par_m2"]
    coherence_materiel = {
        "zones_coffrees_simultanement": _ref["zones_coffrees_simultanement"],
        "coffrage_mobilise_m2": _ref["coffrage_mobilise_m2"],
        "stock_declare_m2": _ref["stock_coffrage_declare_m2"],
        "marge_m2": _ref["stock_coffrage_declare_m2"] - _ref["coffrage_mobilise_m2"],
        "etais_necessaires": round(_ref["zones_coffrees_simultanement"] * etais_zone),
        "verdict": ("OK" if _ref["coffrage_suffisant"]
                    else "LE PLANNING DEMANDE PLUS DE COFFRAGE QUE LE PARC DECLARE"),
        "regle": (
            "Le coffrage d'une zone est immobilise pendant un cycle entier. Le nombre de "
            "zones qui en detiennent en meme temps vaut ceil(cycle / cadence). Reduire la "
            "cadence sans ajouter de tables est impossible : c'est la contrainte que les "
            "plannings de rotation oublient le plus souvent."
        ),
    }

    res = {
        "quantites": q, "durees": t, "variantes": res_variantes,
        "coherence_materiel": coherence_materiel,
        "suivi": {"jour_arret": round(jour_arret, 1), "semaine_arret": round(semaine_arret, 1),
                  "avancement_prevu_pct": round(prevu_arret, 1),
                  "zones_prevues_equivalentes": round(zones_prevues_arret, 2),
                  "libelle_arret": f"jour {jour_arret:.0f}, soit la fin de la semaine {semaine_arret:.0f}"},
        "figures": {
            "zones": {"longueur_m": z["longueur_zone_m"], "largeur_m": z["largeur_zone_m"],
                      "nb_zones": z["nb_zones"], "entraxe_poutres_m": poutre["entraxe_m"],
                      "avancement": av},
            "sequence": [x.nom for x in reseau],
            "gantt": [{"nom": x.nom, "debut": round(cc["detail"]["tot"][x.id][0], 2),
                       "duree": round(x.duree, 2),
                       "critique": x.id in cc["detail"]["critiques"]} for x in reseau],
            "courbe_s": courbe,
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
