"""Etalonnage de calc/qualite.py (§ 3.3) : cas a solution fermee.

Les grandeurs de ce module sont des taux et des repartitions : elles ont toutes une
solution analytique exacte, et deux d'entre elles ont un INVARIANT qui se verifie sans
connaitre le resultat — c'est la forme d'etalonnage la plus sure dont dispose un module
qui ne calcule aucune structure.

Ce que l'etalonnage ne valide pas : les taux de reference eux-memes, qui sont des
hypotheses V3 declarees. Il valide la facon de les appliquer.
"""
import json, pathlib, sys, copy

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import qualite as qa                                                     # noqa: E402

echecs = []


def cas(nom, obtenu, attendu, tol=1e-9, unite=""):
    ok = abs(obtenu - attendu) <= tol
    if not ok:
        echecs.append(nom)
    print(f"  {'ok  ' if ok else 'ECHEC'} {nom} — {obtenu:.6f} contre {attendu:.6f} {unite}")


# Plage de consignation minimale : `exposition` publie le rapport entre la PRESENCE et
# la PRODUCTION d'une nuit d'interception, et il le lit dans cette plage. Les valeurs
# ci-dessous sont celles d'un jeu d'etalonnage — 4 h utiles sur 6 — et non celles du
# projet : ce que l'etalonnage valide ici, c'est la facon d'appliquer les taux, pas le
# rendement d'une plage, qui a son propre etalonnage dans le module B7c.
PLAGE = {"plage_travaux": {
    "duree_nominale_h": {"valeur": 6.0},
    "prise_de_possession_h": {"valeur": 0.5},
    "consignation_catenaire_h": {"valeur": 0.5},
    "amenee_des_moyens_h": {"valeur": 0.5},
    "repli_des_moyens_h": {"valeur": 0.25},
    "deconsignation_h": {"valeur": 0.25},
    "marge_de_restitution_h": {"valeur": 0.0},
    "abattement_de_cadence_nuit_pct": {"valeur": 0.0}}}


def jeu(h_jour, h_nuit, tf, tg, k):
    """Jeu minimal, construit a la main : la solution est evidente."""
    return ({"qualite_hse": {"exposition": {
                "taux_de_frequence_reference": {"valeur": tf},
                "taux_de_gravite_reference": {"valeur": tg},
                "surexposition_du_travail_de_nuit": {"valeur": k}}},
             "ferroviaire": PLAGE,
             "planning": {"contraintes_exploitation": {"taches_soumises": ["N"]}}},
            {"heures_de_main_oeuvre_par_tache": {"J": h_jour, "N": h_nuit}})


print("=== 1. Le taux applique a des heures : solution evidente ===")
d, pl = jeu(1e6, 0.0, 28.0, 1.4, 1.8)
e = qa.exposition(d, pl)
cas("un million d'heures a TF 28 donne 28 accidents",
    e["accidents_avec_arret_attendus"], 28.0, 1e-9)
cas("et TG 1,4 donne 1 400 journees perdues", e["journees_perdues_attendues"], 1400.0, 0.5)

print("\n=== 2. INVARIANT : la ponderation repartit, elle n'ajoute pas ===")
# Le meme chantier, avec cinq coefficients differents : le TOTAL ne doit pas bouger.
ref = None
for k in (1.0, 1.5, 1.8, 2.5, 5.0):
    d, pl = jeu(90_000.0, 10_000.0, 28.0, 1.4, k)
    e = qa.exposition(d, pl)
    if ref is None:
        ref = e["accidents_avec_arret_attendus"]
    cas(f"k = {k} : total inchange", e["accidents_avec_arret_attendus"], ref, 1e-9)

print("\n=== 3. … mais la REPARTITION, elle, suit le coefficient ===")
parts = []
for k in (1.0, 2.0, 4.0):
    d, pl = jeu(90_000.0, 10_000.0, 28.0, 1.4, k)
    parts.append(qa.exposition(d, pl)["part_de_nuit_dans_le_risque_pct"])
# k = 1 : la part vaut exactement la part des heures, soit 10 %.
cas("k = 1 redonne la part des heures", parts[0], 10.0, 1e-9, "%")
# k = 2 : 2 x 10 / (90 + 2 x 10) = 18,18 %
# La valeur publiee est arrondie au centieme : la tolerance est la moitie du dernier
# chiffre publie, pas une tolerance de calcul.
cas("k = 2 donne 2x10/(90+2x10)", parts[1], 2 * 10 / (90 + 2 * 10) * 100, 0.005, "%")
cas("k = 4 donne 4x10/(90+4x10)", parts[2], 4 * 10 / (90 + 4 * 10) * 100, 0.005, "%")
ok = parts[0] < parts[1] < parts[2]
if not ok:
    echecs.append("monotonie de la part")
print(f"  {'ok  ' if ok else 'ECHEC'} la part croit avec le coefficient — "
      f"{parts[0]:.2f} < {parts[1]:.2f} < {parts[2]:.2f} %")

print("\n=== 4. Cas degeneres ===")
d, pl = jeu(100_000.0, 0.0, 28.0, 1.4, 1.8)
e = qa.exposition(d, pl)
cas("aucune heure de nuit : part de nuit nulle", e["part_de_nuit_dans_le_risque_pct"], 0.0, 1e-9, "%")
d, pl = jeu(0.0, 100_000.0, 28.0, 1.4, 1.8)
e = qa.exposition(d, pl)
cas("que des heures de nuit : part de 100 %", e["part_de_nuit_dans_le_risque_pct"], 100.0, 1e-9, "%")
cas("et le total reste le taux x les heures", e["accidents_avec_arret_attendus"], 2.8, 1e-9)

print("\n=== 4b. Presence et production d'une nuit d'interception ===")
d, pl = jeu(90_000.0, 10_000.0, 28.0, 1.4, 1.8)
pp = qa.exposition(d, pl)["presence_et_production_de_nuit"]
# 6 h de plage, 2 h de prealables et de restitution : 4 h utiles, rapport exactement 1,5
cas("4 h utiles sur une plage de 6 h", pp["travail_effectif_h"], 4.0, 1e-9, "h")
cas("le rapport presence / production vaut 6/4", pp["rapport_presence_production"],
    1.5, 1e-9)

print("\n=== 5. La criticite est bien un produit de rangs ===")
d = {"qualite_hse": {"risques": {
    "echelle": {"1": "a", "2": "b", "3": "c", "4": "d"},
    "liste": [{"risque": "X", "f": 4, "g": 4, "d": 4, "parade": "p" * 40},
              {"risque": "Y", "f": 1, "g": 1, "d": 1, "parade": "p" * 40},
              {"risque": "Z", "f": 2, "g": 3, "d": 4, "parade": "p" * 40}]}}}
c = qa.criticite(d)
cas("4x4x4 = 64", c["lignes"][0]["criticite"], 64, 0)
cas("2x3x4 = 24", c["lignes"][1]["criticite"], 24, 0)
cas("1x1x1 = 1", c["lignes"][2]["criticite"], 1, 0)
ok = [x["rang"] for x in c["lignes"]] == [1, 2, 3]
if not ok:
    echecs.append("rangs")
print(f"  {'ok  ' if ok else 'ECHEC'} les rangs suivent la criticite decroissante")

print("\n=== 6. Le jeu REEL du projet, recalcule a la main ===")
d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
pl = json.loads((RACINE / "calc" / "sorties" / "planification.json").read_text(encoding="utf-8"))
e = qa.exposition(d, pl)
h = pl["heures_de_main_oeuvre_par_tache"]
cas("heures totales", e["heures_totales"], round(sum(h.values()), 1), 0.2, "h")
cas("accidents = TF x heures reelles",
    e["accidents_avec_arret_attendus"],
    round(d["qualite_hse"]["exposition"]["taux_de_frequence_reference"]["valeur"]
          * sum(h.values()) / 1e6, 2), 0.01)

print()
if echecs:
    print(f"ETALONNAGE ECHOUE : {len(echecs)} cas — {', '.join(echecs)}")
    sys.exit(1)
print("Etalonnage qualite : tous les cas fermes sont verifies.")
