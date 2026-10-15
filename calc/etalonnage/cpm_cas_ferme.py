"""Etalonnage du moteur CPM sur des reseaux a solution connue A LA MAIN (§ 3.3).

Sans etalonnage, les sorties de calc/ restent V3 et ne servent pas d'exemple de
reference. Les quatre cas ci-dessous ont une duree que l'on pose sans calculer :
c'est la condition pour que l'etalonnage ne soit pas le module se comparant a
lui-meme.
"""
from __future__ import annotations
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from cpm import Tache, contre_calcul, voie_A_parcours, ordonner

CAS = [
    ("chaine de 3 taches : 2 + 3 + 4 = 9",
     [Tache("a", "a", 2), Tache("b", "b", 3, ["a"]), Tache("c", "c", 4, ["b"])], 9.0),
    ("deux branches paralleles, la plus longue l'emporte : 1 + max(5, 2) + 1 = 7",
     [Tache("d", "d", 1), Tache("e", "e", 5, ["d"]), Tache("f", "f", 2, ["d"]),
      Tache("g", "g", 1, ["e", "f"])], 7.0),
    ("recouvrement de 2 jours : 4 + 4 - 2 = 6",
     [Tache("h", "h", 4), Tache("i", "i", 4, [("h", -2)])], 6.0),
    ("tache isolee la plus longue : max(10, 3 + 3) = 10",
     [Tache("j", "j", 10), Tache("k", "k", 3), Tache("l", "l", 3, ["k"])], 10.0),
]

if __name__ == "__main__":
    ok = True
    print("ETALONNAGE — moteur CPM")
    for nom, reseau, attendu in CAS:
        r = contre_calcul(reseau)
        bon = abs(r["voie_A_parcours_avant_arriere_j"] - attendu) < 1e-9 and r["verdict"] == "OK"
        ok &= bon
        print(f"  {'ok   ' if bon else 'ECHEC'} {nom:58s} A {r['voie_A_parcours_avant_arriere_j']:5.1f} · "
              f"B {r['voie_B_enumeration_des_chemins_j']:5.1f} · attendu {attendu:5.1f}")

    print("  gardes-fous")
    try:
        ordonner([Tache("x", "x", 1, ["y"]), Tache("y", "y", 1, ["x"])])
        print("     ECHEC un circuit a ete accepte"); ok = False
    except ValueError:
        print("     ok    un circuit est refuse")
    try:
        voie_A_parcours([Tache("x", "x", 1, ["fantome"])])
        print("     ECHEC un predecesseur inconnu a ete accepte"); ok = False
    except ValueError:
        print("     ok    un predecesseur inconnu est refuse")
    sys.exit(0 if ok else 1)
