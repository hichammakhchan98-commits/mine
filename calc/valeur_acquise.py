"""Valeur acquise d'un plancher en cours, par DEUX voies (§ 3.3).

    Voie A — par les COUTS : VA = budget a l'achevement x avancement physique.
    Voie B — par les QUANTITES RELEVEES sur le chantier (attachements) x prix
             unitaires. Cette voie ne passe NI par le budget, NI par l'avancement
             declare : c'est ce qui la rend independante.

Une premiere version de ce contre-calcul multipliait les quantites THEORIQUES par
l'avancement declare. Elle etait algebriquement identique a la voie A — l'ecart
valait zero par construction, et le controle ne pouvait rien detecter. C'est le
meme piege que le contre-calcul du socle : deux voies ne sont independantes que si
elles ne partagent pas leur entree decisive.

Les deux doivent coincider : si elles divergent, c'est que l'avancement physique
declare ne correspond pas aux quantites reellement mises en oeuvre — exactement la
derive qu'un chef de projet suivi cherche a detecter.

Rappel de ce que la valeur acquise NE dit pas : elle compare ce qui est produit a ce
qui est depense et a ce qui etait prevu. Elle ne dit rien de la qualite, rien des
reserves a venir, et elle se laisse tromper par un avancement declare a vue de nez.
"""
from __future__ import annotations
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from plancher import quantites_zone, fourchette_acier
from cycle_plancher import durees_taches, cout_zone

RACINE = pathlib.Path(__file__).resolve().parent.parent


def _recoupement(d: dict, q: dict, avancement: float) -> dict:
    """Recoupement en unites physiques : releve contre theorique x avancement declare.

    Separer les postes GEOMETRIQUES (beton, coffrage) du poste issu d'un RATIO (acier)
    est le coeur du controle : un ecart sur les premiers est un signal, un ecart sur le
    second est attendu.
    """
    # 1 % est defendable sur un poste GEOMETRIQUE, et sur lui seul : le beton et le
    # coffrage se mesurent sur plan, leur incertitude est celle du releve, pas d'une
    # hypothese. Le meme seuil applique a l'acier ou aux dirhams n'aurait aucun sens
    # (fourchette du ratio V3 : plus ou moins 20 %).
    SEUIL_GEOMETRIQUE_PCT = 1.0
    rel = d["suivi"]["quantites_relevees"]
    postes = [("beton_m3", "m3", "geometrique"), ("coffrage_m2", "m2", "geometrique"),
              ("acier_kg", "kg", "ratio V3")]
    out, signal = [], False
    for cle, unite, nature in postes:
        theo = q[cle] * avancement
        ecart = (rel[cle] - theo) / theo * 100
        alerte = nature == "geometrique" and abs(ecart) > SEUIL_GEOMETRIQUE_PCT
        signal = signal or alerte
        out.append({"poste": cle, "unite": unite, "nature": nature,
                    "theorique_x_avancement": round(theo, 1), "releve": rel[cle],
                    "ecart_pct": round(ecart, 2), "signal": alerte})
    # Les rapports que le texte publie ne se tapent pas a la main : ils se calculent.
    # Deux d'entre eux ont ete publies faux (« quarante fois », « vingt fois »).
    acier = next(x for x in out if x["poste"] == "acier_kg")
    etendue = q.get("fourchette_acier", {}).get("etendue_pct")
    rapports = {}
    if etendue:
        if abs(acier["ecart_pct"]) > 1e-9:
            rapports["fourchette_du_ratio_sur_ecart_constate"] = round(
                etendue / abs(acier["ecart_pct"]), 1)
        rapports["fourchette_du_ratio_sur_seuil_geometrique"] = round(
            etendue / SEUIL_GEOMETRIQUE_PCT, 1)
        rapports["etendue_du_ratio_pct"] = etendue

    return {
        "postes": out,
        "rapports": rapports,
        "seuil_poste_geometrique_pct": SEUIL_GEOMETRIQUE_PCT,
        "un_poste_geometrique_derive": signal,
        "lecture": (
            "Un ecart sur le beton ou le coffrage met en cause l'avancement declare : ces "
            "quantites sont geometriques, elles ne dependent d'aucune hypothese. Un ecart "
            "sur l'acier ne prouve rien : il vient d'un ratio V3 dont la fourchette est "
            "bien plus large que l'ecart."
        ),
    }


def valeur_acquise(d: dict, q: dict, cout: dict, planning: dict) -> dict:
    s = d["suivi"]
    n_zones = d["geometrie"]["mezzanine"]["zones_de_coulage"]["nb_zones"]
    cout_zone_MAD = cout["total_fournitures_et_mise_en_oeuvre_MAD"]

    BAC = cout_zone_MAD * n_zones                      # budget a l'achevement
    avancement_zones = s["zones_realisees_a_date"] + s["avancement_zone_en_cours_pct"] / 100.0
    # L'avancement PREVU est fractionnaire, comme le reel : c'est la meme grandeur que
    # celle que trace la courbe en S. Compter « 4 zones entieres » d'un cote et un
    # avancement fractionnaire de l'autre faisait diverger la figure et le tableau.
    prevu_zones = planning["zones_prevues_equivalentes"]

    VP = cout_zone_MAD * prevu_zones                   # valeur planifiee
    CR = s["cout_reel_constate_MAD"]                   # cout reel

    # ---- voie A : par les couts
    VA_A = BAC * (avancement_zones / n_zones)

    # ---- voie B : par les quantites RELEVEES, qui ne passent pas par l'avancement declare
    p = d["prix_unitaires_MAD"]["postes"]
    rel = s["quantites_relevees"]
    VA_B = (rel["beton_m3"] * p["beton_m3"]["valeur"]
            + rel["acier_kg"] * p["acier_kg"]["valeur"]
            + rel["coffrage_m2"] * p["coffrage_m2"]["valeur"])
    ecart = abs(VA_A - VA_B) / VA_A * 100
    # avancement que les releves impliquent reellement, a comparer au declare
    avancement_releve = VA_B / cout_zone_MAD      # en zones equivalentes

    CPI, SPI = VA_A / CR, VA_A / VP
    EAC = BAC / CPI                                    # prevision a terminaison
    return {
        # la date d'arret est DEDUITE du planning par cycle_plancher.py : elle n'est
        # pas repetee ici, pour qu'elle n'existe qu'a un seul endroit
        "zones_prevues_equivalentes": round(prevu_zones, 2),
        "zones_realisees_equivalentes": round(avancement_zones, 2),
        "budget_a_l_achevement_BAC_MAD": round(BAC),
        "valeur_planifiee_VP_MAD": round(VP),
        "valeur_acquise_VA_MAD": round(VA_A),
        "cout_reel_CR_MAD": round(CR),
        "ecart_de_cout_CV_MAD": round(VA_A - CR),
        "ecart_de_delai_SV_MAD": round(VA_A - VP),
        "CPI": round(CPI, 3),
        "SPI": round(SPI, 3),
        "prevision_a_terminaison_EAC_MAD": round(EAC),
        "derive_prevue_MAD": round(EAC - BAC),
        "retard_en_zones": round(avancement_zones - prevu_zones, 2),
        # Le recoupement se fait en UNITES PHYSIQUES, poste par poste. En dirhams, la
        # comparaison serait polluee par l'incertitude des ratios : l'acier fait 43 % du
        # cout et son ratio V3 le fait varier de plus ou moins 10 %, soit dix fois le seuil.
        # En m3 et en m2, le beton et le coffrage sont GEOMETRIQUES : un ecart y est un
        # vrai signal. En kg, l'ecart est attendu et n'en est pas un — le module le dit.
        "recoupement_physique": _recoupement(d, q, avancement_zones),
        # Contre-exemple : le MEME controle sur un releve de beton court de 5 %. Sans lui,
        # le module montrerait un controle qui ne sonne jamais, et n'apprendrait pas a
        # distinguer un signal d'un bruit.
        "recoupement_contre_exemple": _recoupement(
            {**d, "suivi": {**s, "quantites_relevees": {
                **s["quantites_relevees"],
                "beton_m3": round(q["beton_m3"] * avancement_zones * 0.95, 1)}}},
            q, avancement_zones),
        "contre_calcul": {
            "voie_A_par_les_couts_MAD": round(VA_A),
            "voie_B_par_les_quantites_MAD": round(VA_B),
            "ecart_pct": round(ecart, 3),
            "tolerance_pct": 1.0,
            "limite_de_ce_seuil": (
                "1 % en dirhams est plus serre que l'incertitude des entrees : le ratio "
                "d'acier seul deplace le cout de zone de plus ou moins 10 %. Ce seuil n'a "
                "de sens que parce que les deux voies partagent les memes prix. Le "
                "recoupement qui fait foi est celui en unites physiques, poste par poste."
            ),
            "avancement_declare_zones": round(avancement_zones, 2),
            "avancement_implique_par_les_releves_zones": round(avancement_releve, 2),
            "ecart_d_avancement_zones": round(avancement_zones - avancement_releve, 3),
            "verdict": "OK" if ecart <= 1.0 else "ECART — l'avancement declare ne colle pas aux quantites relevees",
            "ce_que_ce_controle_detecte": (
                "un avancement physique declare qui ne correspond pas aux quantites "
                "reellement mises en oeuvre. C'est la derive la plus courante d'une "
                "situation de travaux, et la plus difficile a voir dans un tableau de bord."
            ),
        },
        "lecture": (
            f"CPI = {CPI:.3f} : chaque dirham depense produit {CPI:.2f} dirham de valeur. "
            f"SPI = {SPI:.3f} : l'avancement vaut {SPI:.0%} de ce qui etait planifie a cette date."
        ),
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    q = quantites_zone(d)
    q["fourchette_acier"] = fourchette_acier(d, q)
    t = durees_taches(d, q)
    c = cout_zone(d, q, t)
    plan = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json").read_text(encoding="utf-8"))
    va = valeur_acquise(d, q, c, plan["suivi"])
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "valeur-acquise.json").write_text(
        json.dumps(va, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for k in ("valeur_planifiee_VP_MAD", "valeur_acquise_VA_MAD", "cout_reel_CR_MAD",
              "CPI", "SPI", "prevision_a_terminaison_EAC_MAD", "derive_prevue_MAD"):
        print(f"  {k:36s} {va[k]}")
    cc = va["contre_calcul"]
    print(f"  contre-calcul : A {cc['voie_A_par_les_couts_MAD']} / B {cc['voie_B_par_les_quantites_MAD']} "
          f"MAD · ecart {cc['ecart_pct']} % · {cc['verdict']}")
