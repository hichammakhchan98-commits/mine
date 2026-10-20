"""Etalonnage du moteur CPM sur des reseaux a solution connue A LA MAIN (§ 3.3).

Sans etalonnage, les sorties de calc/ restent V3 et ne servent pas d'exemple de
reference. Les quatre cas ci-dessous ont une duree que l'on pose sans calculer :
c'est la condition pour que l'etalonnage ne soit pas le module se comparant a
lui-meme.
"""
from __future__ import annotations
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from cpm import Tache, contre_calcul, voie_A_parcours, voie_B_enumeration, ordonner

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

    # --- Regimes que les quatre cas ci-dessus n'atteignaient JAMAIS, et ou le moteur
    #     etait faux : la passe adversariale les a trouves. Ils restent ici pour que
    #     la correction ne puisse plus regresser.
    ("decalage negatif egal a la duree du predecesseur : A finit a 10, B ne l'avance pas",
     [Tache("m", "m", 10), Tache("n", "n", 1, [("m", -10)])], 10.0),
    ("decalage negatif PLUS GRAND que la duree : le debut reste borne a zero",
     [Tache("o", "o", 10), Tache("p", "p", 1, [("o", -20)])], 10.0),
    ("tache de duree nulle (un point d'arret instantane)",
     [Tache("q", "q", 0), Tache("r", "r", 5, ["q"])], 5.0),
    ("deux fins distinctes : la plus tardive l'emporte",
     [Tache("s", "s", 3), Tache("t", "t", 7, ["s"]), Tache("u", "u", 1, ["s"])], 10.0),
    ("deux departs independants qui convergent",
     [Tache("v", "v", 4), Tache("w", "w", 9), Tache("x2", "x2", 1, ["v", "w"])], 10.0),

    # --- Contrainte de debut au plus tot imposee de l'exterieur (fenetre de
    #     consignation, ordre de service, livraison). Regime ajoute apres le bloquant
    #     B1 de la passe adversariale de D2 : le planning calculait la date de la
    #     fenetre, la publiait, et faisait quand meme demarrer la tache au reseau.
    ("contrainte externe active : A finit a 2, B ne peut pas demarrer avant 40 — 40 + 3 = 43",
     [Tache("y1", "y1", 2), Tache("y2", "y2", 3, ["y1"], au_plus_tot=40)], 43.0),
    ("contrainte externe inactive : le reseau est deja plus tard qu'elle — 20 + 3 = 23",
     [Tache("z1", "z1", 20), Tache("z2", "z2", 3, ["z1"], au_plus_tot=5)], 23.0),
    ("contrainte externe sur une tache sans predecesseur : 7 + 4 = 11",
     [Tache("w1", "w1", 4, [], au_plus_tot=7)], 11.0),
    ("contrainte externe sur une branche NON critique : la plus longue l'emporte encore",
     [Tache("v1", "v1", 1), Tache("v2", "v2", 30, ["v1"]),
      Tache("v3", "v3", 2, ["v1"], au_plus_tot=10), Tache("v4", "v4", 1, ["v2", "v3"])], 32.0),
    ("contrainte externe qui DEPLACE le chemin critique : 50 + 2 + 1 = 53 contre 31",
     [Tache("u1", "u1", 1), Tache("u2", "u2", 30, ["u1"]),
      Tache("u3", "u3", 2, ["u1"], au_plus_tot=50), Tache("u4", "u4", 1, ["u2", "u3"])], 53.0),
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

    # --- marges et chemin critique, et pas seulement la duree
    # La duree etait juste sur ces trois reseaux alors que les MARGES etaient fausses et
    # que le chemin critique ressortait vide : un etalonnage qui ne verifie que la duree
    # laisse passer la moitie de ce qu'un planificateur lit reellement.
    print("  marges et chemin critique (decalages negatifs importants)")
    for nom, taches, crit_attendu, marges_attendues in (
        ("A(10) -> B(1), dec -10", [Tache("A", "A", 10.0), Tache("B", "B", 1.0, [("A", -10.0)])],
         ["A"], {"A": 0.0, "B": 9.0}),
        ("A(10) -> B(1), dec -20", [Tache("A", "A", 10.0), Tache("B", "B", 1.0, [("A", -20.0)])],
         ["A"], {"A": 0.0, "B": 9.0}),
        ("A(2) -> B(5), dec -10", [Tache("A", "A", 2.0), Tache("B", "B", 5.0, [("A", -10.0)])],
         ["B"], {"A": 3.0, "B": 0.0}),
    ):
        r = voie_A_parcours(taches)
        bon = r["critiques"] == crit_attendu and all(
            abs(r["marges"][k] - v) < 1e-9 for k, v in marges_attendues.items())
        print(f"     {'ok   ' if bon else 'ECHEC'} {nom} — critiques {r['critiques']} "
              f"(attendu {crit_attendu}) · marges {r['marges']}")
        ok = ok and bon

    print("  gardes-fous")
    try:
        ordonner([Tache("x", "x", 1, ["y"]), Tache("y", "y", 1, ["x"])])
        print("     ECHEC un circuit a ete accepte"); ok = False
    except ValueError:
        print("     ok    un circuit est refuse")
    for nom, f in (("voie A", voie_A_parcours), ("voie B", voie_B_enumeration)):
        try:
            f([Tache("x", "x", 1, ["fantome"])])
            print(f"     ECHEC {nom} : un predecesseur inconnu a ete accepte"); ok = False
        except ValueError:
            print(f"     ok    {nom} : un predecesseur inconnu est refuse")
        try:
            f([Tache("y", "y", 1, ["z"]), Tache("z", "z", 1, ["y"])])
            print(f"     ECHEC {nom} : un circuit a ete accepte"); ok = False
        except ValueError:
            print(f"     ok    {nom} : un circuit est refuse")
    sys.exit(0 if ok else 1)
