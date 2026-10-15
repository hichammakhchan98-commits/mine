"""Tests de calc/ : valeurs attendues et ecart <= tolerance (§ 12.1 f)."""
from __future__ import annotations
import json, math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from cage import metre, aire_mm2, perimetre_cadre_mm, verification_dimensionnelle

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
echecs = []


def verifie(nom, cond, detail=""):
    print(f"  {'ok   ' if cond else 'ECHEC'} {nom}{(' — ' + detail) if detail else ''}")
    if not cond:
        echecs.append(nom)


d = json.loads((RACINE / "data" / "demo-cage.json").read_text(encoding="utf-8"))
r = metre(d)

# --- geometrie : valeurs attendues recalculees a la main
verifie("aire d'une barre HA20", abs(aire_mm2(20) - 314.159) < 0.01, f"{aire_mm2(20):.3f} mm2")
verifie("nombre de barres = 3 + 2", r["n_barres"] == 5, str(r["n_barres"]))
# troncon 2000 mm, enrobage 30 mm de chaque bout, espacement 150 mm : (2000-60)//150 + 1 = 12 + 1 = 13
verifie("nombre de cadres = 13", r["n_cadres"] == 13, str(r["n_cadres"]))
verifie("longueur d'une barre = 1,940 m", abs(r["longueur_barre_m"] - 1.940) < 1e-6, f"{r['longueur_barre_m']} m")

# --- perimetre du cadre : 2(290-40) + 2(690-40) + 2.pi.20
attendu = 2 * (290 - 40) + 2 * (690 - 40) + 2 * math.pi * 20
verifie("perimetre du cadre", abs(r["perimetre_cadre_m"] * 1000 - attendu) < 0.5,
        f"{r['perimetre_cadre_m'] * 1000:.2f} mm contre {attendu:.2f} mm attendus")

# --- contre-calcul : les deux voies doivent converger (§ 3.3)
cc = r["contre_calcul"]
verifie("contre-calcul dans la tolerance de 5 %", cc["ecart_pct"] <= cc["tolerance_pct"],
        f"ecart {cc['ecart_pct']} %")
verifie("les deux voies ne sont pas identiques (sinon ce n'est pas un contre-calcul)",
        cc["voie_A_premiers_principes_kg"] != cc["voie_B_coefficient_tabule_kg"],
        f"A = {cc['voie_A_premiers_principes_kg']} kg, B = {cc['voie_B_coefficient_tabule_kg']} kg")

# --- ordre de grandeur. Ce que ce controle sert a attraper : une erreur d'unite ou de
# facteur (un x10, un mm pris pour un cm). Il NE valide PAS un dimensionnement : les
# parametres de la cage sont des parametres de demonstration, pas un resultat de calcul.
og = r["ordre_de_grandeur"]
verifie("ratio kg/m3 dans la fourchette geometrique 30-250 (detecte les erreurs d'unite)",
        og["dans_la_fourchette_geometrique"], f"{r['ratio_kg_m3']} kg/m3")
# Et on CONSTATE, sans echouer, l'ecart avec une poutre reellement dimensionnee.
print(f"  info  ratio {r['ratio_kg_m3']} kg/m3 — "
      f"{'dans' if og['dans_la_fourchette_poutre_dimensionnee'] else 'SOUS'} la fourchette "
      f"d'une poutre dimensionnee {og['fourchette_poutre_dimensionnee_kg_m3']} (V3) : attendu, "
      f"la cage de demonstration n'est pas dimensionnee (§ 5.0)")

# --- unites
vd = verification_dimensionnelle()
verifie("verification dimensionnelle (pint)", vd["verdict"] == "OK", vd["verdict"])

# --- garde-fou : une geometrie impossible doit lever
try:
    perimetre_cadre_mm(100, 100, 80)
    verifie("refus d'un rayon de cintrage impossible", False)
except ValueError:
    verifie("refus d'un rayon de cintrage impossible", True)

print(f"\n{len(echecs)} echec(s)." if echecs else "\nTests de calc/ : tous verts.")
sys.exit(1 if echecs else 0)
