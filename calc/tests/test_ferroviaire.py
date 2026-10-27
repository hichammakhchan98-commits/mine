"""Tests du module B7c — batiments ferroviaires : construire a cote d'une voie exploitee."""
from __future__ import annotations
import json, math, sys, pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import plage as pg                                                       # noqa: E402

echecs = []


def verifie(nom, condition, detail=""):
    if not condition:
        echecs.append(nom)
    print(f"  {'ok   ' if condition else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
r = json.loads((RACINE / "calc" / "sorties" / "ferroviaire.json").read_text(encoding="utf-8"))
pl = json.loads((RACINE / "calc" / "sorties" / "planification.json").read_text(encoding="utf-8"))
F = d["ferroviaire"]
PT = F["plage_travaux"]
V = {k: PT[k]["valeur"] for k in PT if isinstance(PT[k], dict) and "valeur" in PT[k]}

# ------------------------------------------------- 1. le rendement est une soustraction
print("\n--- le rendement d'une plage ---")
p = r["plage"]
avant = V["prise_de_possession_h"] + V["consignation_catenaire_h"] + V["amenee_des_moyens_h"]
apres = V["repli_des_moyens_h"] + V["deconsignation_h"] + V["marge_de_restitution_h"]
verifie("le travail effectif est la plage moins les deux parts fixes",
        abs(p["travail_effectif_h"] - (V["duree_nominale_h"] - avant - apres)) < 1e-9,
        f"{V['duree_nominale_h']} - {avant:.2f} - {apres:.2f} = {p['travail_effectif_h']} h")
verifie("le rendement est recalcule ici",
        abs(p["rendement_pct"] - p["travail_effectif_h"] / p["duree_nominale_h"] * 100) < 0.05,
        f"{p['rendement_pct']} %")
verifie("le detail publie totalise exactement la plage",
        abs(sum(x["h"] for x in p["detail"]) - V["duree_nominale_h"]) < 1e-9)
verifie("la part tenue par l'exploitant est consignation + deconsignation",
        abs(p["part_tenue_par_l_exploitant_h"]
            - (V["consignation_catenaire_h"] + V["deconsignation_h"])) < 1e-9,
        f"{p['part_tenue_par_l_exploitant_h']} h que rien n'accelere")
verifie("le seuil de plage inutile est la part fixe",
        abs(p["seuil_de_plage_inutile_h"] - (avant + apres)) < 1e-9,
        f"{p['seuil_de_plage_inutile_h']} h")
try:
    pg.rendement(d, avant + apres)
    verifie("canari : une plage egale a la part fixe doit LEVER", False)
except ValueError:
    verifie("canari : une plage egale a la part fixe leve bien",
            True, f"{avant + apres:.2f} h de part fixe")

# ------------------------------------------------- 2. les deux effets se multiplient
print("\n--- le facteur d'interception ---")
h_j = d["planning"]["calendrier"]["heures_par_jour"]
abat = V["abattement_de_cadence_nuit_pct"] / 100
attendu = h_j / p["travail_effectif_h"] / (1 - abat)
verifie("le facteur compose le rendement du TEMPS et celui du TRAVAIL",
        abs(p["facteur_d_interception"] - attendu) < 0.005,
        f"{h_j}/{p['travail_effectif_h']} / (1-{abat}) = {attendu:.3f}")
verifie("canari : additionner les deux effets au lieu de les multiplier donnerait moins",
        (h_j / p["travail_effectif_h"]) + abat < p["facteur_d_interception"],
        "l'intuition « il reste la moitie du temps, donc deux fois plus de nuits » "
        "sous-estime")
verifie("D2 lit le MEME facteur : une grandeur, un seul endroit (D-039)",
        "facteur d'interception" in pl["durees"]["CHLV"]["formule"],
        pl["durees"]["CHLV"]["formule"][-60:])

# ------------------------------------------------- 3. le point de non-retour
print("\n--- le point de non-retour ---")
nr = r["point_de_non_retour"]
verifie("la duree de l'operation est la masse de la piece sur la cadence de nuit",
        abs(nr["duree_de_l_operation_h"]
            - nr["masse_d_une_piece_t"] / nr["cadence_de_nuit_t_h"]) < 0.02,
        f"{nr['duree_de_l_operation_h']} h pour {nr['masse_d_une_piece_t']} t")
verifie("« tient dans la plage » si et seulement si la marge de decision est positive",
        nr["l_operation_tient_dans_la_plage"] == (nr["marge_de_decision_h"] >= 0))
verifie("la masse maximale levable est le travail effectif x la cadence de nuit",
        abs(nr["masse_maximale_d_une_piece_t"]
            - p["travail_effectif_h"] * nr["cadence_de_nuit_t_h"]) < 0.02,
        f"{nr['masse_maximale_d_une_piece_t']} t dans une plage de "
        f"{p['duree_nominale_h']} h")
verifie("la plage minimale est la part fixe plus l'operation",
        abs(nr["plage_minimale_pour_cette_piece_h"]
            - (p["seuil_de_plage_inutile_h"] + nr["duree_de_l_operation_h"])) < 0.02,
        f"{nr['plage_minimale_pour_cette_piece_h']} h")
verifie("les deux seuils sont coherents entre eux",
        (nr["masse_d_une_piece_t"] > nr["masse_maximale_d_une_piece_t"])
        == (nr["plage_minimale_pour_cette_piece_h"] > p["duree_nominale_h"]),
        "la piece ne tient pas dans la plage ET la plage ne suffit pas a la piece : "
        "les deux faces du meme fait")

# ------------------------------------------------- 4. les leviers, MESURES
print("\n--- les leviers ---")
lev = r["leviers"]
ref = lev["reference"]
verifie("la reference est la methode et les plages declarees dans data/",
        ref["part_sous_interception_pct"]
        == d["planning"]["contraintes_exploitation"]["part_levage_sous_consignation_pct"]["valeur"]
        and ref["plage_h"] == V["duree_nominale_h"])
verifie("la reference reproduit la duree de chantier que D2 publie",
        abs(ref["duree_du_chantier_j"] - pl["calendrier"]["duree_ouvree_j"]) < 0.5,
        f"{ref['duree_du_chantier_j']} contre {pl['calendrier']['duree_ouvree_j']} j")
for x in lev["lignes"]:
    verifie(f"{x['levier'][:40]} : ecart de date recalcule ici",
            abs(x["ecart_de_date_j"]
                - (x["duree_du_chantier_j"] - ref["duree_du_chantier_j"])) < 0.02,
            f"{x['ecart_de_date_j']:+.1f} j")
verifie("tous les leviers raccourcissent ou laissent la date inchangee",
        all(x["ecart_de_date_j"] <= 0.01 for x in lev["lignes"]))
# Le pre-assemblage n'est pas gratuit : il ALLONGE la tache au sol.
pre = next(x for x in lev["lignes"] if x["part_sous_interception_pct"] == 15
           and x["plage_h"] == V["duree_nominale_h"])
verifie("pre-assembler allonge bien la tache AU SOL : le levier n'est pas gratuit",
        pre["CHAP_j"] > ref["CHAP_j"],
        f"CHAP {ref['CHAP_j']} -> {pre['CHAP_j']} j")
verifie("et le reseau mesure le solde, qui reste favorable",
        pre["ecart_de_date_j"] < 0,
        f"{pre['ecart_de_date_j']:+.1f} j malgre l'allongement au sol")
verifie("le module signale les leviers qui SORTENT de la fourchette declaree",
        any(x["part_hors_fourchette_declaree"] for x in lev["lignes"]),
        "changer de methode n'est pas choisir une valeur basse de l'hypothese")
verifie("chaque levier nomme ce que le calcul ne price pas (D-041)",
        all(len(x["ce_que_le_calcul_ne_price_pas"]) > 5 for x in lev["lignes"]))
verifie("canari : deduire l'effet par une regle de trois donnerait un autre nombre",
        abs((ref["duree_du_chantier_j"] - pre["duree_du_chantier_j"])
            - (ref["etalement_CHLV_j"] - pre["etalement_CHLV_j"])) > 1.0,
        f"date {ref['duree_du_chantier_j'] - pre['duree_du_chantier_j']:.1f} j contre "
        f"etalement {ref['etalement_CHLV_j'] - pre['etalement_CHLV_j']:.1f} j — "
        "le reseau absorbe une partie")

# ------------------------------------------------- 5. le cout d'une heure utile
print("\n--- le cout d'une heure utile ---")
c = r["cout"]
taux = d["prix_unitaires_MAD"]["postes"]["main_oeuvre_h"]["valeur"]
maj = V["majoration_horaire_nuit_pct"] / 100
verifie("le cout d'une plage est la plage ENTIERE au taux majore",
        abs(c["cout_d_une_plage_MAD_par_compagnon"]
            - p["duree_nominale_h"] * taux * (1 + maj)) < 0.5)
verifie("le cout de l'heure utile divise par les heures UTILES, pas par la plage",
        abs(c["cout_de_l_heure_UTILE_MAD"]
            - c["cout_d_une_plage_MAD_par_compagnon"] / p["travail_effectif_h"]) < 0.5,
        f"{c['cout_de_l_heure_UTILE_MAD']} MAD")
verifie("le ratio porte sa base (D-037)",
        "ouvrage" in c["ratio_defini_sur_cette_base"])
verifie("et le rapport a l'heure d'OUVRAGE depasse celui au taux horaire brut",
        c["rapport_a_l_heure_d_OUVRAGE_de_jour"] > c["rapport_au_taux_de_jour"],
        f"x{c['rapport_a_l_heure_d_OUVRAGE_de_jour']} contre x{c['rapport_au_taux_de_jour']} "
        "— comparer au taux brut sous-estime l'ecart")
verifie("la majoration de nuit n'explique qu'une petite part de l'ecart",
        (1 + maj) < c["rapport_a_l_heure_d_OUVRAGE_de_jour"] / 2,
        f"majoration x{1 + maj} contre ecart total "
        f"x{c['rapport_a_l_heure_d_OUVRAGE_de_jour']}")

# ------------------------------------------------- 6. les interfaces
print("\n--- les interfaces ---")
i = r["interfaces"]
n = len(F["interfaces"]["intervenants"])
verifie("le nombre d'interfaces possibles est n(n-1)/2",
        i["interfaces_possibles"] == n * (n - 1) // 2, f"{n} intervenants")
verifie("les interfaces actives sont un sous-ensemble strict des possibles",
        0 < i["interfaces_actives"] < i["interfaces_possibles"])
verifie("la liste est triee par delai decroissant : la plus longue se demande en premier",
        all(i["liste"][k]["delai_de_demande_j"] >= i["liste"][k + 1]["delai_de_demande_j"]
            for k in range(len(i["liste"]) - 1)))
verifie("chaque interface porte sa nature : decision ou information",
        all(x["nature"] in ("decision", "information") for x in i["liste"]))
verifie("le chantier porte plusieurs maitres d'ouvrage, et le module le dit",
        i["nb_maitres_d_ouvrage"] >= 2 and "maitres d'ouvrage" in i["lecture"],
        f"{i['nb_maitres_d_ouvrage']} donneurs d'ordre distincts")
verifie("le delai le plus long est celui d'une DECISION, pas d'une information",
        i["liste"][0]["nature"] == "decision",
        f"{i['delai_le_plus_long_j']} j")

# ------------------------------------------------- 7. figures
print("\n--- figures ---")
f = r["figures"]
verifie("la figure de la plage totalise la plage nominale",
        abs(sum(x["valeur"] for x in f["plage"]) - p["duree_nominale_h"]) < 1e-9)
verifie("la figure des leviers porte exactement les etalements mesures",
        all(abs(a["valeur"] - b["etalement_CHLV_j"]) < 0.01
            for a, b in zip(f["leviers"], lev["lignes"])))
verifie("et celle des dates porte exactement les durees de chantier mesurees",
        all(abs(a["valeur"] - b["duree_du_chantier_j"]) < 0.01
            for a, b in zip(f["leviers_dates"], lev["lignes"])))

print()
if echecs:
    print(f"ECHEC : {len(echecs)} controle(s) — {', '.join(echecs)}")
    sys.exit(1)
print("Tests ferroviaires : tous verts.")
