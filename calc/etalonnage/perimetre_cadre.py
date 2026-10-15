"""Etalonnage de la routine geometrique sur une SOLUTION ANALYTIQUE FERMEE (§ 3.3).

Sans etalonnage, les resultats d'une bibliotheque de calc/ restent V3 et ne servent pas
d'exemple de reference. Ici : le perimetre du cadre a coins arrondis, calcule par la
formule fermee, est compare a une discretisation numerique du MEME contour.
Deux chemins differents : si la formule fermee est fausse, la discretisation le dira.
"""
from __future__ import annotations
import math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from cage import perimetre_cadre_mm


def perimetre_numerique(b, h, r, n=200_000):
    """Longueur du contour par somme de segments : parties droites + 4 arcs discretises."""
    droites = 2 * (b - 2 * r) + 2 * (h - 2 * r)
    arcs = 0.0
    for _ in range(4):
        prev = (r, 0.0)
        for i in range(1, n // 4 + 1):
            a = (i / (n // 4)) * (math.pi / 2)
            cur = (r * math.cos(a), r * math.sin(a))
            arcs += math.dist(prev, cur)
            prev = cur
    return droites + arcs


CAS = [
    ("cadre du troncon de demonstration", 290.0, 690.0, 20.0),
    ("cadre carre",                       300.0, 300.0, 24.0),
    ("rayon nul (cadre vif)",             200.0, 400.0, 0.0),
]

if __name__ == "__main__":
    ok = True
    print("ETALONNAGE — perimetre d'un cadre a coins arrondis")
    for nom, b, h, r in CAS:
        ferme = perimetre_cadre_mm(b, h, r)
        num = perimetre_numerique(b, h, r) if r > 0 else 2 * (b + h)
        ecart = abs(ferme - num) / num * 100
        etat = "ok" if ecart < 0.01 else "ECHEC"
        if ecart >= 0.01:
            ok = False
        print(f"  {etat:5s} {nom:36s} ferme {ferme:9.3f} mm · numerique {num:9.3f} mm · ecart {ecart:.5f} %")
    # borne de validite : le rayon ne peut exceder la demi-dimension
    try:
        perimetre_cadre_mm(100.0, 300.0, 60.0)
        print("  ECHEC garde-fou : un rayon impossible a ete accepte")
        ok = False
    except ValueError:
        print("  ok    garde-fou : rayon de cintrage impossible refuse")
    sys.exit(0 if ok else 1)
