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
import json, pathlib, sys
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
    return {
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

    # --- date d'arret du suivi : DEDUITE du planning, pas ecrite dans les donnees
    s_ = d["suivi"]
    jour_arret = plan["debuts"]["Z%d" % s_["zones_prevues_a_date"]] + duree_zone
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
    courbe = []
    pas = plan["duree_totale_j"] / 32
    for k in range(33):
        j = k * pas
        pt = {"j": round(j, 1), "prevu": round(avancement_prevu(j), 1)}
        if j <= jour_arret:
            # l'avancement reel suit la meme forme, ramene au constat de la date d'arret
            ref = avancement_prevu(jour_arret)
            pt["realise"] = round(avancement_prevu(j) * (reel_zones / s_["zones_prevues_a_date"])
                                  if ref else 0.0, 1)
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

    res = {
        "quantites": q, "durees": t,
        "suivi": {"jour_arret": round(jour_arret, 1), "semaine_arret": round(semaine_arret, 1),
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
