"""Etalonnage de la routine geometrique (§ 3.3).

Sans etalonnage, les sorties de calc/ restent V3 et ne servent pas d'exemple de reference.

La version precedente etait creuse : elle recopiait la partie droite de la formule fermee
et ne discretisait que les quatre arcs, soit 6,5 % du perimetre. Une erreur sur le terme
droit aurait ete identique des deux cotes. Ici :

  1. le contour ENTIER est polygonalise independamment, par une parametrisation du contour
     offset qui ne reutilise aucun morceau de la formule fermee ;
  2. deux cas a solution connue HORS formule : le cercle (b = h = 2r, perimetre 2.pi.r) et
     le rectangle a coins vifs (r = 0, perimetre 2(b+h)) ;
  3. les gardes-fous geometriques doivent LEVER sur une geometrie impossible.
"""
from __future__ import annotations
import math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from cage import perimetre_cadre_ferme, perimetre_cadre_discretise


def perimetre_independant(b, h, r, n=400_000):
    """Polygonalisation du contour ENTIER, sans reutiliser la formule fermee.

    Le contour d'un rectangle a coins arrondis est l'ensemble des points a distance r
    du rectangle reduit (b-2r) x (h-2r). On le parcourt par abscisse curviligne sur le
    rectangle reduit, on decale chaque point de r selon la normale sortante, et on somme
    les cordes. Aucun terme n'est repris de la formule fermee.
    """
    B, H = b - 2 * r, h - 2 * r
    coins = [(B / 2, H / 2), (-B / 2, H / 2), (-B / 2, -H / 2), (B / 2, -H / 2)]
    normales = [(0, 1), (-1, 0), (0, -1), (1, 0)]       # normale de chaque cote sortant
    pts = []
    for c in range(4):
        x0, y0 = coins[c]
        x1, y1 = coins[(c + 1) % 4]
        nx, ny = normales[c]
        m = max(2, n // 8)
        for i in range(m):                               # le cote droit, decale de r
            t = i / m
            pts.append((x0 + (x1 - x0) * t + nx * r, y0 + (y1 - y0) * t + ny * r))
        # puis l'arc autour du coin d'arrivee, de la normale du cote courant a la suivante
        a0 = math.atan2(ny, nx)
        nx2, ny2 = normales[(c + 1) % 4]
        a1 = math.atan2(ny2, nx2)
        if a1 < a0:                                  # le parcours est dans le sens direct :
            a1 += 2 * math.pi                        # la normale tourne dans le meme sens
        k = max(2, n // 8)
        for i in range(k + 1):
            a = a0 + (a1 - a0) * i / k
            pts.append((x1 + r * math.cos(a), y1 + r * math.sin(a)))
    return sum(math.dist(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))


CAS = [
    ("cadre de la demonstration", 282.0, 682.0, 20.0),
    ("cadre carre",               300.0, 300.0, 24.0),
    ("rayon nul (coins vifs)",    200.0, 400.0, 0.0),
]

# Cas a solution connue, etablie SANS la formule du module
CAS_CONNUS = [
    ("cercle : b = h = 2r -> 2.pi.r", 120.0, 120.0, 60.0, 2 * math.pi * 60.0),
    ("coins vifs : r = 0 -> 2(b+h)",  200.0, 400.0, 0.0, 2 * (200.0 + 400.0)),
]

if __name__ == "__main__":
    ok = True
    print("ETALONNAGE — perimetre d'un cadre a coins arrondis")

    print("  a) formule fermee contre polygonalisation INDEPENDANTE du contour entier")
    for nom, b, h, r in CAS:
        ferme = perimetre_cadre_ferme(b, h, r)
        indep = perimetre_independant(b, h, r) if r > 0 else 2 * (b + h)
        e = abs(ferme - indep) / indep * 100
        etat = "ok" if e < 0.01 else "ECHEC"
        ok &= e < 0.01
        print(f"     {etat:5s} {nom:30s} {ferme:9.3f} / {indep:9.3f} mm · ecart {e:.5f} %")

    print("  b) contour discretise (voie A) contre formule fermee (voie B)")
    for nom, b, h, r in CAS:
        if r <= 0:
            continue
        a = perimetre_cadre_discretise(b, h, r)
        bb = perimetre_cadre_ferme(b, h, r)
        e = abs(a - bb) / bb * 100
        etat = "ok" if e < 0.05 else "ECHEC"
        ok &= e < 0.05
        print(f"     {etat:5s} {nom:30s} {a:9.3f} / {bb:9.3f} mm · ecart {e:.5f} %")

    print("  c) cas a solution connue, hors formule du module")
    for nom, b, h, r, attendu in CAS_CONNUS:
        v = perimetre_cadre_ferme(b, h, r)
        e = abs(v - attendu) / attendu * 100
        etat = "ok" if e < 1e-9 else "ECHEC"
        ok &= e < 1e-9
        print(f"     {etat:5s} {nom:30s} {v:9.3f} mm contre {attendu:9.3f} attendus")

    print("  d) gardes-fous")
    for nom, f in [("formule fermee", perimetre_cadre_ferme),
                   ("contour discretise", perimetre_cadre_discretise)]:
        try:
            f(100.0, 300.0, 60.0)
            print(f"     ECHEC {nom} : un rayon impossible a ete accepte")
            ok = False
        except ValueError:
            print(f"     ok    {nom} : rayon de cintrage impossible refuse")

    sys.exit(0 if ok else 1)
