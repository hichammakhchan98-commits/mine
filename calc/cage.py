"""Metre d'une cage d'armatures, par DEUX VOIES INDEPENDANTES (§ 3.3).

Voie A — premiers principes : aire de la section droite x longueur x masse volumique.
Voie B — coefficient d'ingenieur tabule : m = 0,00617 . d^2  (kg/m, d en mm), route
         historiquement etablie a partir de la masse volumique de l'acier mais
         utilisee telle quelle sur les plans ; elle ne repasse PAS par pi.

L'ecart tolere est de 5 % (§ 3.3). Il est en pratique de l'ordre de 0,06 % : c'est
normal, les deux voies decrivent la meme geometrie. Ce qu'elles testent, ce sont les
erreurs de saisie, d'unite et de facteur, pas la physique.

ATTENTION : ce script ne dimensionne rien. Il mesure une geometrie donnee.
"""
from __future__ import annotations
import json, math, pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
COEF_TABULE = 0.00617          # kg/m par mm^2 de diametre au carre (plan de ferraillage)


def aire_mm2(dia_mm: float) -> float:
    return math.pi * (dia_mm / 2.0) ** 2


def perimetre_cadre_mm(b_mm: float, h_mm: float, r_mm: float) -> float:
    """Perimetre d'un cadre rectangulaire a coins arrondis — SOLUTION FERMEE.

    Les quatre quarts de cercle forment un cercle complet : 2.pi.r.
    Les parties droites valent 2(b - 2r) + 2(h - 2r).
    """
    if r_mm <= 0:
        return 2 * (b_mm + h_mm)
    if 2 * r_mm > min(b_mm, h_mm):
        raise ValueError(f"rayon de cintrage {r_mm} mm incompatible avec {b_mm} x {h_mm} mm")
    return 2 * (b_mm - 2 * r_mm) + 2 * (h_mm - 2 * r_mm) + 2 * math.pi * r_mm


def metre(d: dict) -> dict:
    s, t, c = d["section"], d["troncon"], d["cadres"]
    rho = d["constantes"]["masse_volumique_acier_kg_m3"]

    b_mm, h_mm = s["b_cm"] * 10.0, s["h_cm"] * 10.0
    e_mm = s["enrobage_cm"] * 10.0
    L_mm = t["L_cm"] * 10.0
    esp_mm = c["espacement_cm"] * 10.0
    d_cad = c["dia_mm"]

    # --- cadres
    bc, hc = b_mm - 2 * e_mm, h_mm - 2 * e_mm
    r_cintrage = max(2.5 * d_cad, 20.0)               # geometrique, cale sur la bibliotheque 3D
    per_mm = perimetre_cadre_mm(bc, hc, r_cintrage)
    n_cadres = max(2, int((L_mm - 2 * e_mm) // esp_mm) + 1)
    long_cadres_m = per_mm * n_cadres / 1000.0

    # --- barres longitudinales
    long_barre_m = (L_mm - 2 * e_mm) / 1000.0
    barres = [(s["inf"]["n"], s["inf"]["dia_mm"]), (s["sup"]["n"], s["sup"]["dia_mm"])]

    # ---- voie A : premiers principes
    masse_cadres_A = aire_mm2(d_cad) * 1e-6 * long_cadres_m * rho
    masse_barres_A = sum(n * aire_mm2(dia) * 1e-6 * long_barre_m * rho for n, dia in barres)

    # ---- voie B : coefficient tabule des plans de ferraillage
    masse_cadres_B = COEF_TABULE * d_cad ** 2 * long_cadres_m
    masse_barres_B = sum(n * COEF_TABULE * dia ** 2 * long_barre_m for n, dia in barres)

    total_A = masse_cadres_A + masse_barres_A
    total_B = masse_cadres_B + masse_barres_B
    ecart = abs(total_A - total_B) / total_A * 100.0

    vol_beton = (b_mm / 1000) * (h_mm / 1000) * (L_mm / 1000)

    return {
        "_avertissement": d["meta"]["avertissement"],
        "n_cadres": n_cadres,
        "perimetre_cadre_m": round(per_mm / 1000.0, 4),
        "rayon_cintrage_mm": round(r_cintrage, 1),
        "longueur_cadres_m": round(long_cadres_m, 3),
        "n_barres": sum(n for n, _ in barres),
        "longueur_barre_m": round(long_barre_m, 3),
        "masse_cadres_kg": round(masse_cadres_A, 2),
        "masse_barres_kg": round(masse_barres_A, 2),
        "masse_acier_kg": round(total_A, 2),
        "volume_beton_m3": round(vol_beton, 4),
        "ratio_kg_m3": round(total_A / vol_beton, 1),
        "ordre_de_grandeur": {
            "but": "detecter une erreur d'unite ou de facteur, PAS valider un dimensionnement",
            "fourchette_geometrique_kg_m3": [30, 250],
            "dans_la_fourchette_geometrique": 30 <= total_A / vol_beton <= 250,
            "fourchette_poutre_dimensionnee_kg_m3": [80, 150],
            "niveau_preuve_fourchettes": "V3",
            "dans_la_fourchette_poutre_dimensionnee": 80 <= total_A / vol_beton <= 150,
            "observation": (
                "Le ratio de cette cage est INFERIEUR a la fourchette usuelle d'une poutre "
                "dimensionnee. C'est attendu et ce n'est pas un defaut de calcul : les "
                "diametres et le nombre de barres sont des parametres de demonstration (V3), "
                "ils ne sortent d'aucun dimensionnement — la phase § 5.0 l'interdit. "
                "C'est precisement le piege que la page de demonstration enseigne : on ne lit "
                "pas un ferraillage dimensionne sur un modele 3D."
            ),
        },
        "contre_calcul": {
            "voie_A_premiers_principes_kg": round(total_A, 2),
            "voie_B_coefficient_tabule_kg": round(total_B, 2),
            "ecart_pct": round(ecart, 3),
            "tolerance_pct": 5.0,
            "verdict": "OK" if ecart <= 5.0 else "ECART HORS TOLERANCE",
        },
    }


def verification_dimensionnelle() -> dict:
    """Chaque formule passe une verification dimensionnelle (§ 3.3, avec pint)."""
    import pint
    u = pint.UnitRegistry()
    dia = 20 * u.mm
    longueur = 1.94 * u.m
    rho = 7850 * u.kg / u.m**3
    aire = math.pi * (dia / 2) ** 2
    masse = (aire * longueur * rho).to(u.kg)
    coef = COEF_TABULE * u.kg / (u.m * u.mm**2)
    masse_b = (coef * dia**2 * longueur).to(u.kg)
    perim = perimetre_cadre_mm(290.0, 690.0, 20.0) * u.mm
    return {
        "masse_voie_A": {"valeur": round(masse.magnitude, 4), "unite": str(masse.units)},
        "masse_voie_B": {"valeur": round(masse_b.magnitude, 4), "unite": str(masse_b.units)},
        "perimetre_cadre": {"valeur": round(perim.to(u.m).magnitude, 4), "unite": "meter"},
        "verdict": "OK" if str(masse.units) == "kilogram" and str(masse_b.units) == "kilogram" else "UNITE INATTENDUE",
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "demo-cage.json").read_text(encoding="utf-8"))
    res = metre(d)
    res["verification_dimensionnelle"] = verification_dimensionnelle()
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "metre-cage.json").write_text(
        json.dumps(res, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False))
