"""Etalonnage de calc/plage.py (§ 3.3) : cas a solution fermee.

Le rendement d'une plage est une SOUSTRACTION et le facteur d'interception un produit de
deux quotients : les deux ont une solution analytique exacte, verifiable a la main. C'est
la forme la plus sure d'etalonnage — il n'y a pas de modele a se tromper, seulement une
arithmetique a ne pas rater.

Ce que l'etalonnage NE valide pas : les six durees de la part fixe, qui sont des
hypotheses V3 declarees. Il valide la facon de les combiner.
"""
import pathlib, sys, copy, json

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import plage as pg                                                       # noqa: E402

echecs = []


def cas(nom, obtenu, attendu, tol=1e-9, unite=""):
    ok = abs(obtenu - attendu) <= tol
    if not ok:
        echecs.append(nom)
    print(f"  {'ok  ' if ok else 'ECHEC'} {nom} — {obtenu:.4f} contre {attendu:.4f} {unite}")


def jeu(nominale, avant, apres, abattement_pct):
    """Jeu de donnees minimal, construit a la main : la solution est evidente."""
    return {"ferroviaire": {"plage_travaux": {
        "duree_nominale_h": {"valeur": nominale},
        "prise_de_possession_h": {"valeur": avant}, "consignation_catenaire_h": {"valeur": 0.0},
        "amenee_des_moyens_h": {"valeur": 0.0}, "repli_des_moyens_h": {"valeur": apres},
        "deconsignation_h": {"valeur": 0.0}, "marge_de_restitution_h": {"valeur": 0.0},
        "abattement_de_cadence_nuit_pct": {"valeur": abattement_pct}}}}


print("=== 1. Le rendement est une soustraction ===")
d1 = jeu(10.0, 2.0, 3.0, 0.0)
cas("10 h moins 2 h avant et 3 h apres", pg.rendement(d1)["travail_effectif_h"], 5.0, 1e-12, "h")
cas("rendement = 50 %", pg.rendement(d1)["rendement_pct"], 50.0, 1e-9, "%")
cas("la part fixe est la somme des deux", pg.rendement(d1)["part_fixe_h"], 5.0, 1e-12, "h")

print("\n=== 2. Sans part fixe, le rendement vaut 100 % ===")
cas("plage nue", pg.rendement(jeu(8.0, 0.0, 0.0, 0.0))["rendement_pct"], 100.0, 1e-9, "%")

print("\n=== 3. Le facteur compose les deux effets ===")
# Travail effectif 5 h sur une journee de 10 h : facteur 2 sur le temps.
# Abattement de 50 % : facteur 2 sur le travail. Les deux se MULTIPLIENT -> 4.
cas("rendement 1/2 et abattement 1/2 donnent x4",
    pg.facteur_d_interception(jeu(10.0, 2.0, 3.0, 50.0), heures_par_jour=10.0), 4.0, 1e-9)
cas("sans abattement, le facteur est le seul rapport des temps",
    pg.facteur_d_interception(jeu(10.0, 2.0, 3.0, 0.0), heures_par_jour=10.0), 2.0, 1e-9)
cas("une plage egale a la journee et sans part fixe donne x1",
    pg.facteur_d_interception(jeu(8.0, 0.0, 0.0, 0.0), heures_par_jour=8.0), 1.0, 1e-9)

print("\n=== 4. Les cas limites levent au lieu de rendre un nombre faux ===")
for nom, args in (("plage egale a la part fixe", (5.0, 2.0, 3.0, 0.0)),
                  ("plage plus courte que la part fixe", (4.0, 2.0, 3.0, 0.0))):
    try:
        pg.rendement(jeu(*args))
        echecs.append(nom)
        print(f"  ECHEC {nom} — n'a PAS leve")
    except ValueError:
        print(f"  ok   {nom} — leve bien")

print("\n=== 5. Monotonie : une plage plus longue produit toujours plus ===")
prec = 0.0
for h in (5.5, 6.0, 8.0, 10.0, 12.0):
    u = pg.rendement(jeu(h, 2.0, 3.0, 0.0))["travail_effectif_h"]
    ok = u > prec
    if not ok:
        echecs.append(f"monotonie a {h} h")
    print(f"  {'ok  ' if ok else 'ECHEC'} {h:>5.1f} h -> {u:.2f} h utiles")
    prec = u

print("\n=== 6. Le jeu REEL du projet, recalcule a la main ===")
d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
V = {k: v["valeur"] for k, v in d["ferroviaire"]["plage_travaux"].items()
     if isinstance(v, dict) and "valeur" in v}
attendu = V["duree_nominale_h"] - sum(V[k] for k in pg.POSTES_AVANT + pg.POSTES_APRES)
cas("travail effectif du projet", pg.rendement(d)["travail_effectif_h"], attendu, 1e-12, "h")

print()
if echecs:
    print(f"ETALONNAGE ECHOUE : {len(echecs)} cas — {', '.join(echecs)}")
    sys.exit(1)
print("Etalonnage plage : tous les cas fermes sont verifies.")
