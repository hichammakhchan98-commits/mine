"""Quantites d'ordre de grandeur d'une zone de plancher de mezzanine (§ 5.0.2).

En phase « sans calculs normatifs », les quantites ne peuvent PAS sortir d'un
dimensionnement. Elles sortent de la GEOMETRIE (exacte) et de RATIOS declares V3.
La geometrie est juste ; les ratios sont des hypotheses. Le resultat en herite :
c'est un ordre de grandeur, pas un metre d'execution. Le module le dit.
"""
from __future__ import annotations
import json, pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent


def quantites_zone(d: dict) -> dict:
    z = d["geometrie"]["mezzanine"]["zones_de_coulage"]
    dalle = next(x for x in d["elements"]["dalles"] if x["id"] == "DM1")
    poutre = next(x for x in d["elements"]["poutres"] if x["id"] == "PM1")
    r = d["ratios_V3"]

    L, l = z["longueur_zone_m"], z["largeur_zone_m"]
    surface = L * l

    # --- poutres dans la zone : une ligne de poutres par trame
    entraxe = poutre["entraxe_m"]
    n_poutres = round(L / entraxe)                      # 15,0 / 7,50 = 2
    long_poutre = poutre["longueur_dans_zone_m"]
    retombee = poutre["retombee_sous_dalle_m"]
    b = poutre["b_m"]

    # --- beton : geometrie exacte
    beton_dalle = surface * dalle["epaisseur_m"]
    beton_poutres = n_poutres * long_poutre * b * retombee
    beton = beton_dalle + beton_poutres

    # --- coffrage : sous-face de dalle + joues de poutres + rives (ratio V3)
    coffrage_dalle = surface - n_poutres * long_poutre * b   # la largeur de poutre n'est pas coffree en sous-face de dalle
    coffrage_joues = n_poutres * long_poutre * retombee * 2
    coffrage_fond_poutres = n_poutres * long_poutre * b
    base = coffrage_dalle + coffrage_joues + coffrage_fond_poutres
    coffrage = base * (1 + r["coffrage_rives_pct"]["valeur"] / 100.0)

    # --- acier : RATIOS V3, c'est ici que la precision s'arrete
    acier_dalle = beton_dalle * r["acier_dalle_kg_m3"]["valeur"]
    acier_poutres = beton_poutres * r["acier_poutre_kg_m3"]["valeur"]
    acier = acier_dalle + acier_poutres

    return {
        "surface_m2": round(surface, 1),
        "n_poutres": n_poutres,
        "beton_dalle_m3": round(beton_dalle, 2),
        "beton_poutres_m3": round(beton_poutres, 2),
        "beton_m3": round(beton, 2),
        "coffrage_m2": round(coffrage, 1),
        "coffrage_detail_m2": {
            "sous_face_dalle": round(coffrage_dalle, 1),
            "joues_de_poutres": round(coffrage_joues, 1),
            "fond_de_poutres": round(coffrage_fond_poutres, 1),
            "rives_pct": r["coffrage_rives_pct"]["valeur"],
        },
        "acier_dalle_kg": round(acier_dalle),
        "acier_poutres_kg": round(acier_poutres),
        "acier_kg": round(acier),
        "ratio_acier_kg_m3": round(acier / beton, 1),
        "ratio_acier_kg_m2": round(acier / surface, 1),
        "ratio_coffrage_m2_par_m2": round(coffrage / surface, 3),
        "_precision": (
            "Le beton et le coffrage viennent de la GEOMETRIE : ils sont justes a la "
            "geometrie pres. L'acier vient de RATIOS V3 : sa fourchette est celle des "
            "ratios, soit environ -20 % a +25 %. Ne jamais presenter ce chiffre comme "
            "un metre d'execution."
        ),
    }


def fourchette_acier(d: dict, q: dict) -> dict:
    """L'incertitude des ratios, propagee. Un chiffre V3 sans sa fourchette ment."""
    r = d["ratios_V3"]
    bd, bp = q["beton_dalle_m3"], q["beton_poutres_m3"]
    lo = bd * r["acier_dalle_kg_m3"]["fourchette"][0] + bp * r["acier_poutre_kg_m3"]["fourchette"][0]
    hi = bd * r["acier_dalle_kg_m3"]["fourchette"][1] + bp * r["acier_poutre_kg_m3"]["fourchette"][1]
    return {"min_kg": round(lo), "max_kg": round(hi),
            "etendue_pct": round((hi - lo) / q["acier_kg"] * 100, 1)}


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    q = quantites_zone(d)
    q["fourchette_acier"] = fourchette_acier(d, q)
    print(json.dumps(q, indent=2, ensure_ascii=False))
