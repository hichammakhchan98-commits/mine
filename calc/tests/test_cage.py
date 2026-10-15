"""Tests de calc/ (§ 12.1 f).

Regle que ces tests se donnent : une assertion qui ne peut pas echouer ne vaut rien.
La version precedente en contenait trois — un perimetre compare a la meme formule
retapee avec les cotes en dur, un « les deux voies different » satisfait par un simple
arrondi, et un verdict pint vrai par construction apres un .to(kg) explicite.
"""
from __future__ import annotations
import json, math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from cage import (metre, aire_mm2, perimetre_cadre_ferme, perimetre_cadre_discretise,
                  placement_cadres, verification_dimensionnelle)

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
echecs = []


def verifie(nom, cond, detail=""):
    print(f"  {'ok   ' if cond else 'ECHEC'} {nom}{(' — ' + detail) if detail else ''}")
    if not cond:
        echecs.append(nom)


d = json.loads((RACINE / "data" / "demo-cage.json").read_text(encoding="utf-8"))
r = metre(d)
s, c, cv = d["section"], d["cadres"], d["conventions"]

# --- geometrie elementaire
verifie("aire d'une barre HA20", abs(aire_mm2(20) - 314.159) < 0.01, f"{aire_mm2(20):.3f} mm2")
verifie("nombre de barres = n_inf + n_sup", r["n_barres"] == s["inf"]["n"] + s["sup"]["n"],
        str(r["n_barres"]))

# --- la convention d'enrobage est-elle tenue ? (defaut B4 de la passe /devil)
peau_cadre = (s["b_cm"] * 10 - r["axe_cadre_cm"]["b"] * 10) / 2 - c["dia_mm"] / 2
verifie("l'enrobage se mesure bien a la PEAU du cadre",
        abs(peau_cadre - s["enrobage_cm"] * 10) < 1e-6,
        f"peau a {peau_cadre:.2f} mm, enrobage annonce {s['enrobage_cm'] * 10:.0f} mm")

# --- perimetre : cas a solution connue, etablie SANS la formule du module
verifie("cercle b = h = 2r donne 2.pi.r",
        abs(perimetre_cadre_ferme(120, 120, 60) - 2 * math.pi * 60) < 1e-9)
verifie("coins vifs r = 0 donne 2(b+h)",
        abs(perimetre_cadre_ferme(200, 400, 0) - 2 * 600) < 1e-9)

# --- les deux voies doivent differer sur le CHEMIN, pas seulement sur un arrondi
cc = r["contre_calcul"]
# « A != B » serait satisfait par un ecart de 50 % : on exige deux chemins DISTINCTS
# et CONVERGENTS, ce qui est la seule situation interessante.
verifie("deux chemins de longueur distincts",
        cc["perimetre_voie_A_m"] != cc["perimetre_voie_B_m"],
        f"A {cc['perimetre_voie_A_m']} m (discretise) / B {cc['perimetre_voie_B_m']} m (ferme)")
verifie("et convergents a moins de 0,05 %", cc["ecart_perimetre_pct"] < 0.05,
        f"ecart {cc['ecart_perimetre_pct']} %")
verifie("contre-calcul dans la tolerance de 5 %", cc["ecart_pct"] <= cc["tolerance_pct"],
        f"ecart {cc['ecart_pct']} %")

# --- le contre-calcul attrape-t-il vraiment une erreur ? on en injecte une.
faux = json.loads(json.dumps(d))
faux["conventions"]["rayon_cintrage_mm"] = 40          # rayon double
rf = metre(faux)
verifie("une erreur de rayon de cintrage DEPLACE le resultat",
        abs(rf["masse_acier_kg"] - r["masse_acier_kg"]) > 0.05,
        f"{rf['masse_acier_kg']} kg contre {r['masse_acier_kg']} kg")

# --- placement : une seule regle gouverne comptage ET placement (defaut M10)
n, esp = placement_cadres(d["troncon"]["L_cm"] * 10, s["enrobage_cm"] * 10, c["espacement_cm"] * 10)
# « (n-1) x espacement reel = longueur utile » est vrai par construction pour tout n :
# ce n'est pas un test. Ce qui se teste, c'est que n est MINIMAL — un cadre de moins
# ferait depasser l'espacement nominal.
verifie("n est le plus petit entier qui tient l'espacement nominal",
        (n - 2) > 0 and (utile_mm := d["troncon"]["L_cm"] * 10 - 2 * (s["enrobage_cm"] * 10 + c["dia_mm"] / 2))
        and utile_mm / (n - 2) > c["espacement_cm"] * 10,
        f"avec {n-1} cadres l'espacement vaudrait {utile_mm / (n - 2) / 10:.2f} cm > {c['espacement_cm']} cm")
verifie("l'espacement reel ne depasse pas l'espacement nominal",
        esp <= c["espacement_cm"] * 10 + 1e-9, f"{esp / 10:.2f} <= {c['espacement_cm']} cm")

# --- ordre de grandeur : ce controle ne detecte qu'une erreur d'unite, et le dit
gf = r["garde_fou_unite"]
verifie("garde-fou d'unite (30-250 kg/m3)", gf["dans_la_fourchette"], f"{r['ratio_kg_m3']} kg/m3")
faux2 = json.loads(json.dumps(d))
faux2["constantes"]["masse_volumique_acier_kg_m3"] = 7850 * 10     # erreur de facteur 10
verifie("une erreur de facteur 10 FAIT SORTIR du garde-fou",
        not metre(faux2)["garde_fou_unite"]["dans_la_fourchette"],
        f"{metre(faux2)['ratio_kg_m3']} kg/m3")

# --- coherence interne : un rapport que le garde-fou d'unite ne voit pas
ci = r["coherence_interne"]
verifie("masse lineique des cadres conforme a la geometrie",
        abs(ci["masse_lineique_cadres_kg_m"] - ci["masse_lineique_attendue_kg_m"]) < 1e-3,
        f"{ci['masse_lineique_cadres_kg_m']} kg/m")
verifie("perimetre plausible devant le rectangle a coins vifs", ci["perimetre_plausible"],
        f"rapport {ci['perimetre_sur_coins_vifs']}")
# et ce rapport doit REAGIR a une erreur de perimetre, sinon il ne sert a rien
faux3 = json.loads(json.dumps(d))
faux3["conventions"]["rayon_cintrage_mm"] = 120          # rayon absurde
try:
    r3 = metre(faux3)
    verifie("un perimetre absurde sort du rapport plausible", not r3["coherence_interne"]["perimetre_plausible"],
            f"rapport {r3['coherence_interne']['perimetre_sur_coins_vifs']}")
except ValueError:
    verifie("un perimetre absurde est refuse en amont", True)

# --- constat rapporte, non bloquant
cp = r["comparaison_poutre_dimensionnee"]
print(f"  info  ratio {r['ratio_kg_m3']} kg/m3 — "
      f"{'dans' if cp['dedans'] else 'SOUS'} la fourchette d'une poutre dimensionnee "
      f"{cp['fourchette_kg_m3']} (V3) : attendu, la cage n'est pas dimensionnee (§ 5.0)")
print(f"  info  cadres modelises SANS crochets : le metre est minorant d'environ 3 %")

# --- les conventions publiees dans data/ sont-elles reellement lues ?
faux4 = json.loads(json.dumps(d))
faux4["conventions"]["enrobage_mesure_a"] = "axe du cadre"
try:
    metre(faux4)
    verifie("une convention qui ment est refusee", False)
except ValueError:
    verifie("une convention qui ment est refusee", True)

# --- unites
vd = verification_dimensionnelle(d)
verifie("verification dimensionnelle (pint) alimentee par data/", vd["verdict"] == "OK", vd["verdict"])
verifie("une formule non homogene LEVE bien", vd["une_formule_non_homogene_leve"])

# --- gardes-fous geometriques
for nom, f in [("formule fermee", perimetre_cadre_ferme), ("contour discretise", perimetre_cadre_discretise)]:
    try:
        f(100, 100, 80)
        verifie(f"refus d'un rayon impossible ({nom})", False)
    except ValueError:
        verifie(f"refus d'un rayon impossible ({nom})", True)

print(f"\n{len(echecs)} echec(s)." if echecs else "\nTests de calc/ : tous verts.")
sys.exit(1 if echecs else 0)
