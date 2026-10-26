"""Etalonnage de calc/ferraillage.py (§ 3.3) : cas a solution fermee.

Sans etalonnage externe, deux voies ecrites par le meme auteur peuvent partager la meme
erreur de modele. Les grandeurs de ce module s'y pretent bien : la masse lineique d'une
barre et le perimetre d'un cadre ont une solution analytique exacte, et le tableau du
commerce en donne une verification independante — il n'est pas tire du meme calcul, il
est publie par les producteurs d'acier depuis un siecle.

Important : ce que l'etalonnage valide est le METRE, jamais le PLAN. Un metre juste d'un
plan faux reste un metre juste.
"""
import math, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import ferraillage as fe                                                 # noqa: E402

echecs = []


def cas(nom, obtenu, attendu, tol, unite=""):
    ok = abs(obtenu - attendu) <= tol
    if not ok:
        echecs.append(nom)
    print(f"  {'ok  ' if ok else 'ECHEC'} {nom} — {obtenu:.4f} contre {attendu:.4f} "
          f"{unite} (tolerance {tol})")


print("=== 1. Masse lineique contre le tableau du commerce ===")
# Valeurs publiees par les producteurs d'acier, arrondies au mg/m. Source independante
# de la formule : c'est la verification exterieure que le § 3.3 demande.
TABLEAU = {6: 0.222, 8: 0.395, 10: 0.617, 12: 0.888, 14: 1.208,
           16: 1.578, 20: 2.466, 25: 3.853, 32: 6.313, 40: 9.865}
for dia, m in TABLEAU.items():
    cas(f"HA{dia}", fe.masse_lineique_kg_m(dia), m, 0.001, "kg/m")

print("\n=== 2. Analyse dimensionnelle de la formule ===")
# m = pi/4 d^2 rho : [m] = m^2 x kg/m^3 = kg/m. Verifie numeriquement par homogeneite :
# doubler le diametre quadruple la masse lineique.
cas("doubler le diametre quadruple la masse",
    fe.masse_lineique_kg_m(20) / fe.masse_lineique_kg_m(10), 4.0, 1e-9)
cas("la masse est proportionnelle a la masse volumique",
    fe.masse_lineique_kg_m(12, 15700) / fe.masse_lineique_kg_m(12, 7850), 2.0, 1e-9)

print("\n=== 3. Longueur developpee : solution evidente ===")
cas("barre droite sans retour", fe.longueur_developpee_m(
    {"droit_m": 7.5, "retours_m": []}), 7.5, 1e-12, "m")
cas("barre avec deux retours", fe.longueur_developpee_m(
    {"droit_m": 2.4, "retours_m": [0.6, 0.6]}), 3.6, 1e-12, "m")

print("\n=== 4. Perimetre du cadre : rectangle exact ===")
# Un cadre rectangulaire trace sur son axe a pour perimetre exact 2(b + h). L'axe est a
# enrobage + dia/2 de la peau du beton, donc b_axe = b - 2e - dia.
b, h, e, dia = 35.0, 75.0, 3.0, 8.0
b_ax, h_ax = (b - 2 * e - dia / 10) / 100, (h - 2 * e - dia / 10) / 100
cas("perimetre analytique", 2 * (b_ax + h_ax), 2 * (0.2820 + 0.6820), 1e-9, "m")

print("\n=== 5. Comptage sur une longueur : intervalles + 1 ===")
# Sur 10,00 m a 20 cm : 50 intervalles, 51 cadres. Verifiable a la main.
cas("10,00 m a 20 cm", math.floor(10.0 / 0.20) + 1, 51, 0, "cadres")
cas("une longueur non multiple : 9,70 m a 20 cm",
    math.floor(9.70 / 0.20) + 1, 49, 0, "cadres")

print("\n=== 6. Nappe : barres par metre ===")
# A l'espacement s cm, il y a 100/s barres par metre. Sur 10 m de largeur a 12,5 cm :
# 80 barres (79 intervalles + 1, arrondi superieur du produit : 80).
cas("10 m de largeur a 12,5 cm", math.ceil(10.0 * (100 / 12.5)), 80, 0, "barres")

print()
if echecs:
    print(f"ETALONNAGE ECHOUE : {len(echecs)} cas — {', '.join(echecs)}")
    sys.exit(1)
print("Etalonnage ferraillage : tous les cas fermes sont verifies.")
