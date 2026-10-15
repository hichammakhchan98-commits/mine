"""Metre d'une cage d'armatures, par deux voies qui ne partagent NI le chemin de longueur,
NI le chemin de masse (§ 3.3).

    Voie A — longueur par DISCRETISATION du contour (droites + arcs), c'est-a-dire
             exactement le contour que suit le tube de la scene 3D ; masse par les
             premiers principes : aire de la section droite x longueur x masse volumique.

    Voie B — longueur par la FORMULE FERMEE P = 2(b-2r) + 2(h-2r) + 2.pi.r ; masse par le
             coefficient tabule des plans de ferraillage m = 0,00617 . d^2 (kg/m, d en mm).

Les deux voies different donc sur les deux facteurs. Une erreur dans la discretisation du
contour, ou dans la formule fermee, ecarte les resultats. L'ancienne version comparait la
meme formule a elle-meme avec une constante arrondie : l'ecart publie (0,075 %) n'etait que
l'arrondi de 0,00617 par rapport a pi/4 x 7850 x 1e-6 = 0,0061654. Ce n'etait pas un
contre-calcul.

CONVENTION D'ENROBAGE (publiee dans data/demo-cage.json) : l'enrobage se mesure a la peau
de l'armature la plus exterieure, donc du cadre. L'axe du cadre est a enrobage + dia/2.

ATTENTION : ce script ne dimensionne rien. Il mesure une geometrie donnee.
"""
from __future__ import annotations
import json, math, pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent
COEF_TABULE = 0.00617          # kg/m par mm^2 de diametre au carre (plan de ferraillage)


def aire_mm2(dia_mm: float) -> float:
    return math.pi * (dia_mm / 2.0) ** 2


def perimetre_cadre_ferme(b_mm: float, h_mm: float, r_mm: float) -> float:
    """VOIE B — solution fermee. Les quatre quarts de cercle forment un cercle complet."""
    if r_mm <= 0:
        return 2 * (b_mm + h_mm)
    if 2 * r_mm > min(b_mm, h_mm):
        raise ValueError(f"rayon de cintrage {r_mm} mm incompatible avec {b_mm} x {h_mm} mm")
    return 2 * (b_mm - 2 * r_mm) + 2 * (h_mm - 2 * r_mm) + 2 * math.pi * r_mm


def contour_cadre(b_mm: float, h_mm: float, r_mm: float, n_arc: int = 10, n_droite: int = 8):
    """Contour exact echantillonne — le MEME que src/civil3d/section.js."""
    if 2 * r_mm > min(b_mm, h_mm):
        raise ValueError(f"rayon de cintrage {r_mm} mm incompatible avec {b_mm} x {h_mm} mm")
    pts = []
    coins = [(b_mm / 2 - r_mm, h_mm / 2 - r_mm, 0.0),
             (-(b_mm / 2 - r_mm), h_mm / 2 - r_mm, math.pi / 2),
             (-(b_mm / 2 - r_mm), -(h_mm / 2 - r_mm), math.pi),
             (b_mm / 2 - r_mm, -(h_mm / 2 - r_mm), -math.pi / 2)]
    for c in range(4):
        cx, cy, a0 = coins[c]
        for i in range(n_arc + 1):
            a = a0 + (i / n_arc) * (math.pi / 2)
            pts.append((cx + r_mm * math.cos(a), cy + r_mm * math.sin(a)))
        sx, sy, sa = coins[(c + 1) % 4]
        fin = (cx + r_mm * math.cos(a0 + math.pi / 2), cy + r_mm * math.sin(a0 + math.pi / 2))
        deb = (sx + r_mm * math.cos(sa), sy + r_mm * math.sin(sa))
        for i in range(1, n_droite):
            t = i / n_droite
            pts.append((fin[0] + (deb[0] - fin[0]) * t, fin[1] + (deb[1] - fin[1]) * t))
    return pts


def perimetre_cadre_discretise(b_mm, h_mm, r_mm, n_arc=10, n_droite=8) -> float:
    """VOIE A — longueur de la polyligne du contour, fermee."""
    pts = contour_cadre(b_mm, h_mm, r_mm, n_arc, n_droite)
    return sum(math.dist(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))


def placement_cadres(L_mm: float, enrobage_mm: float, espacement_nominal_mm: float):
    """UNE regle pour le comptage ET le placement : premier et dernier cadre a l'enrobage."""
    utile = L_mm - 2 * enrobage_mm
    if utile <= 0:
        raise ValueError(f"troncon {L_mm} mm trop court pour l'enrobage")
    # l'espacement nominal est un MAXIMUM : on arrondit au superieur, sinon l'espacement
    # reel le depasse (1940 / 12 = 161,7 mm pour un nominal de 150 mm)
    n = max(2, math.ceil(utile / espacement_nominal_mm) + 1)
    espacement_reel = utile / (n - 1) if n > 1 else 0.0
    return n, espacement_reel


def metre(d: dict) -> dict:
    s, t, c, cv = d["section"], d["troncon"], d["cadres"], d["conventions"]
    rho = d["constantes"]["masse_volumique_acier_kg_m3"]

    b_mm, h_mm = s["b_cm"] * 10.0, s["h_cm"] * 10.0
    e_mm = s["enrobage_cm"] * 10.0
    L_mm = t["L_cm"] * 10.0
    d_cad = c["dia_mm"]
    r_cint = cv["rayon_cintrage_mm"]                       # lu dans data/, plus en dur

    # --- cadre : AXE a enrobage + demi-diametre (convention publiee)
    bc = b_mm - 2 * (e_mm + d_cad / 2)
    hc = h_mm - 2 * (e_mm + d_cad / 2)
    per_A = perimetre_cadre_discretise(bc, hc, r_cint)
    per_B = perimetre_cadre_ferme(bc, hc, r_cint)
    n_cadres, esp_reel = placement_cadres(L_mm, e_mm, c["espacement_cm"] * 10.0)

    # --- barres longitudinales : a l'interieur du cadre
    long_barre_m = (L_mm - 2 * e_mm) / 1000.0
    barres = [(s["inf"]["n"], s["inf"]["dia_mm"]), (s["sup"]["n"], s["sup"]["dia_mm"])]

    # ---- voie A : contour discretise + premiers principes
    masse_cadres_A = aire_mm2(d_cad) * 1e-6 * (per_A * n_cadres / 1000.0) * rho
    masse_barres_A = sum(n * aire_mm2(dia) * 1e-6 * long_barre_m * rho for n, dia in barres)
    # ---- voie B : formule fermee + coefficient tabule
    masse_cadres_B = COEF_TABULE * d_cad ** 2 * (per_B * n_cadres / 1000.0)
    masse_barres_B = sum(n * COEF_TABULE * dia ** 2 * long_barre_m for n, dia in barres)

    total_A = masse_cadres_A + masse_barres_A
    total_B = masse_cadres_B + masse_barres_B
    ecart = abs(total_A - total_B) / total_A * 100.0

    vol_beton = (b_mm / 1000) * (h_mm / 1000) * (L_mm / 1000)
    ratio = total_A / vol_beton

    return {
        "_avertissement": d["meta"]["avertissement"],
        "n_cadres": n_cadres,
        "espacement_reel_cm": round(esp_reel / 10.0, 2),
        "axe_cadre_cm": {"b": round(bc / 10.0, 2), "h": round(hc / 10.0, 2)},
        "rayon_cintrage_mm": r_cint,
        "crochets": False,
        "crochets_note": cv["crochets_note"],
        "perimetre_cadre_m": round(per_A / 1000.0, 4),
        "longueur_cadres_m": round(per_A * n_cadres / 1000.0, 3),
        "n_barres": sum(n for n, _ in barres),
        "longueur_barre_m": round(long_barre_m, 3),
        "masse_cadres_kg": round(masse_cadres_A, 2),
        "masse_barres_kg": round(masse_barres_A, 2),
        "masse_acier_kg": round(total_A, 2),
        "volume_beton_m3": round(vol_beton, 4),
        "ratio_kg_m3": round(ratio, 1),
        "garde_fou_unite": {
            "but": "detecter une erreur d'UNITE ou de FACTEUR (un x10, un mm pris pour un cm). "
                   "Ce controle ne valide aucun dimensionnement et n'attrape pas une erreur "
                   "geometrique de quelques pour cent.",
            "fourchette_kg_m3": [30, 250],
            "dans_la_fourchette": 30 <= ratio <= 250,
        },
        "coherence_interne": {
            "but": "rapports internes : ils bougent des qu'une part du metre derape, la ou le "
                   "garde-fou d'unite ne voit rien.",
            "masse_cadres_sur_barres": round(masse_cadres_A / masse_barres_A, 4),
            "masse_par_metre_developpe_cadres_kg_m": round(
                masse_cadres_A / (per_A * n_cadres / 1000.0), 4),
            "attendu_masse_par_metre_cadres_kg_m": round(aire_mm2(d_cad) * 1e-6 * rho, 4),
        },
        "comparaison_poutre_dimensionnee": {
            "fourchette_kg_m3": [80, 150],
            "niveau_preuve": "V3",
            "dedans": 80 <= ratio <= 150,
            "observation": (
                "Le ratio est INFERIEUR a la fourchette usuelle d'une poutre dimensionnee. "
                "C'est attendu : les diametres et le nombre de barres sont des parametres de "
                "demonstration, ils ne sortent d'aucun dimensionnement — la phase § 5.0 "
                "l'interdit. Ce constat est rapporte, il ne fait pas echouer le controle."
            ),
        },
        "contre_calcul": {
            "voie_A": "contour discretise (celui du tube 3D) + aire x longueur x masse volumique",
            "voie_B": "formule fermee du perimetre + coefficient tabule 0,00617 d^2",
            "perimetre_voie_A_m": round(per_A / 1000.0, 5),
            "perimetre_voie_B_m": round(per_B / 1000.0, 5),
            "ecart_perimetre_pct": round(abs(per_A - per_B) / per_B * 100.0, 4),
            "voie_A_kg": round(total_A, 2),
            "voie_B_kg": round(total_B, 2),
            "ecart_pct": round(ecart, 3),
            "tolerance_pct": 5.0,
            "verdict": "OK" if ecart <= 5.0 else "ECART HORS TOLERANCE",
        },
    }


def verification_dimensionnelle(d: dict) -> dict:
    """Verification dimensionnelle alimentee par data/ (§ 3.3), et qui teste aussi qu'une
    unite incoherente LEVE — sinon le controle serait vrai par construction."""
    import pint
    u = pint.UnitRegistry()
    s, c, cv = d["section"], d["cadres"], d["conventions"]
    rho = d["constantes"]["masse_volumique_acier_kg_m3"] * u.kg / u.m**3
    dia = s["inf"]["dia_mm"] * u.mm
    L = (d["troncon"]["L_cm"] * 10 - 2 * s["enrobage_cm"] * 10) * u.mm

    aire = math.pi * (dia / 2) ** 2
    masse_A = (aire * L * rho).to(u.kg)
    coef = COEF_TABULE * u.kg / (u.m * u.mm**2)
    masse_B = (coef * dia**2 * L).to(u.kg)

    # une formule fausse en dimension DOIT lever : on le verifie
    leve = False
    try:
        mauvais = COEF_TABULE * u.kg / u.mm**2          # oubli du « par metre »
        (mauvais * dia**2 * L).to(u.kg)
    except pint.DimensionalityError:
        leve = True

    coherent = abs(masse_A.magnitude - masse_B.magnitude) / masse_A.magnitude < 0.01
    return {
        "source": "data/demo-cage.json (aucune valeur en dur)",
        "masse_1_barre_voie_A_kg": round(masse_A.magnitude, 4),
        "masse_1_barre_voie_B_kg": round(masse_B.magnitude, 4),
        "les_deux_voies_concordent": coherent,
        "une_formule_non_homogene_leve": leve,
        "verdict": "OK" if (coherent and leve and str(masse_A.units) == "kilogram") else "ECHEC",
    }


def variante(d: dict, **modifs) -> dict:
    """Metre d'une variante des parametres. Sert a l'exercice de la page : ses valeurs
    attendues sont CALCULEES, pas tapees dans le texte."""
    v = json.loads(json.dumps(d))
    for cle, val in modifs.items():
        v["cadres"][cle] = val
    return metre(v)


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "demo-cage.json").read_text(encoding="utf-8"))
    res = metre(d)
    res["verification_dimensionnelle"] = verification_dimensionnelle(d)

    # variante de l'exercice : espacement des cadres a 7 cm
    ex = variante(d, espacement_cm=7)
    res["variante_exercice"] = {
        "_role": "valeurs attendues de l'exercice de la page, calculees et non ecrites a la main",
        "espacement_cm": 7,
        "n_cadres": ex["n_cadres"],
        "masse_acier_kg": ex["masse_acier_kg"],
        "delta_masse_kg": round(ex["masse_acier_kg"] - res["masse_acier_kg"], 2),
        "ratio_kg_m3": ex["ratio_kg_m3"],
    }
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "metre-cage.json").write_text(
        json.dumps(res, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(res, indent=2, ensure_ascii=False))
