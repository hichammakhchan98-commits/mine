"""Tests du module C3 — gros oeuvre : cycle, parc de coffrage, betonnage par temps chaud."""
from __future__ import annotations
import json, math, sys, pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import gros_oeuvre as go                                                 # noqa: E402

echecs = []


def verifie(nom, condition, detail=""):
    if not condition:
        echecs.append(nom)
    print(f"  {'ok   ' if condition else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
r = json.loads((RACINE / "calc" / "sorties" / "gros-oeuvre.json").read_text(encoding="utf-8"))
pl = json.loads((RACINE / "calc" / "sorties" / "planification.json").read_text(encoding="utf-8"))
tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json").read_text(encoding="utf-8"))
G = d["gros_oeuvre"]

# ------------------------------------------------- le cycle vient du module TV, intact
verifie("le cycle est celui du module TV, repris sans etre recalcule",
        abs(r["cycle"]["duree_j"] - tv["cycle_zone"]["duree_j"]) < 0.01,
        f"{r['cycle']['duree_j']} j")
verifie("la cadence aussi",
        abs(r["cycle"]["cadence_j"] - tv["planning_plancher"]["cadence_zone_j"]) < 0.01)
verifie("et la duree du plancher retombe sur celle que D2 publie",
        abs(r["cycle"]["duree_du_plancher_j"] - pl["durees"]["MEZZ"]["duree_j"]) < 0.05,
        f"{r['cycle']['duree_du_plancher_j']} contre {pl['durees']['MEZZ']['duree_j']} j")

# ------------------------------------------------- immobilisation du coffrage
im = r["immobilisation_du_coffrage"]
verifie("l'immobilisation du coffrage couvre tout le cycle, cure comprise",
        abs(im["duree_j"] - r["cycle"]["duree_j"]) < 0.02, f"{im['duree_j']} j")
verifie("et la cure en represente une part qu'aucun effectif ne reduit",
        abs(im["part_de_cure_pct"] - im["dont_cure_j"] / im["duree_j"] * 100) < 0.2,
        f"{im['part_de_cure_pct']} %")

# ------------------------------------------------- le parc de coffrage
op = r["parc"]
# la bonne grandeur est la surface de COFFRAGE d'une zone, pas sa surface de plancher :
# un parc est un stock de tables. Diviser par la surface de plancher surestimait de
# 18 % le nombre de zones qu'un parc porte.
surf = tv["quantites"]["coffrage_m2"]
for x in op["lignes"]:
    if x.get("total_MAD") is None:
        continue
    verifie(f"parc {x['parc_m2']} m2 : zones simultanees recalculees ici",
            x["zones_simultanees"] == math.floor(x["parc_m2"] / surf + 1e-9),
            f"{x['zones_simultanees']} zones pour {x['parc_m2']} / {surf}")
    verifie(f"parc {x['parc_m2']} m2 : la cadence tenue est la plus contraignante des deux",
            abs(x["cadence_tenue_j"]
                - max(x["cadence_des_equipes_j"], x["cadence_du_parc_j"])) < 0.01)
verifie("la duree de reference est celle des equipes seules",
        abs(op["duree_de_reference_j"] - r["cycle"]["duree_du_plancher_j"]) < 0.05)
verifie("la marge utilisee est la marge LIBRE du plancher publiee par D2",
        abs(op["marge_disponible_j"] - pl["durees"]["MEZZ"]["marge_libre_j"]) < 0.01,
        f"{op['marge_disponible_j']} j")
# le coeur du modele : un allongement ne coute que s'il DEPASSE la marge
for x in op["lignes"]:
    if x.get("total_MAD") is None:
        continue
    verifie(f"parc {x['parc_m2']} m2 : le depassement est la rallonge moins la marge",
            abs(x["depassement_j"] - max(0.0, x["rallonge_j"] - op["marge_disponible_j"])) < 0.02)
    verifie(f"parc {x['parc_m2']} m2 : des frais de duree si et seulement s'il y a depassement",
            (x["frais_de_duree_MAD"] > 0) == (x["depassement_j"] > 0),
            f"rallonge {x['rallonge_j']} j, marge {op['marge_disponible_j']} j")
verifie("l'optimum est bien le minimum du total, recalcule ici",
        op["optimum"]["total_MAD"] == min(x["total_MAD"] for x in op["lignes"]
                                          if x.get("total_MAD") is not None),
        f"{op['optimum']['parc_m2']} m2 a {op['optimum']['total_MAD']:,.0f} MAD")
verifie("le plus petit parc ne porte qu'UNE zone, et la surface de coffrage le decide",
        next(x for x in op["lignes"] if x["parc_m2"] == min(G["coffrage"]["parcs_a_comparer_m2"])
             )["zones_simultanees"] == 1,
        f"une zone demande {surf} m2 de tables pour "
        f"{tv['quantites']['surface_m2']} m2 de plancher")
verifie("l'optimum n'est NI le plus petit NI le plus grand parc",
        op["optimum"]["parc_m2"] != min(G["coffrage"]["parcs_a_comparer_m2"])
        and op["optimum"]["parc_m2"] != max(G["coffrage"]["parcs_a_comparer_m2"]),
        "sinon le modele n'arbitre rien")
# canari : ignorer la marge ferait choisir le plus petit parc, qui double la duree
_sans_marge = min((x for x in op["lignes"] if x.get("total_MAD") is not None),
                  key=lambda x: x["loyer_et_montage_MAD"])
verifie("canari : sans la contrainte de marge, l'optimum basculerait sur le plus petit parc",
        _sans_marge["parc_m2"] < op["optimum"]["parc_m2"]
        and _sans_marge["depassement_j"] > 0,
        f"{_sans_marge['parc_m2']} m2, qui depasse de {_sans_marge['depassement_j']} j")
_declare = next(x for x in op["lignes"] if x["parc_m2"] == op["parc_declare_m2"])
verifie("le parc declare dans data/ coute plus que l'optimum, et on le dit",
        _declare["total_MAD"] > op["optimum"]["total_MAD"],
        f"+{_declare['total_MAD'] - op['optimum']['total_MAD']:,.0f} MAD pour "
        f"{op['optimum']['rallonge_j'] - _declare['rallonge_j']:.1f} j de marge gardee")

# ------------------------------------------------- betonnage par temps chaud
b = r["betonnage"]
cz = d["geometrie"]["mezzanine"]["zones_de_coulage"]
_larg = G["betonnage_temps_chaud"]["largeur_de_bande_m"]["valeur"]
_trav = min(cz["longueur_zone_m"], cz["largeur_zone_m"])
_vol = _larg * _trav * b["epaisseur_de_dalle_m"]
verifie("le volume d'une bande est recalcule ici",
        abs(b["volume_d_une_bande_m3"] - _vol) < 0.05,
        f"{b['volume_d_une_bande_m3']} m3 = {_larg} x {_trav} x {b['epaisseur_de_dalle_m']}")
verifie("le debit minimal est le volume d'une bande divise par le temps de maniabilite",
        all(abs(v["debit_minimal_m3_h"] - _vol / v["temps_de_maniabilite_h"]) < 0.1
            for v in b["par_temperature"].values()))
verifie("le debit minimal CROIT quand la temperature monte",
        b["par_temperature"]["a_35_degres"]["debit_minimal_m3_h"]
        > b["par_temperature"]["a_30_degres"]["debit_minimal_m3_h"]
        > b["par_temperature"]["a_20_degres"]["debit_minimal_m3_h"],
        f"rapport 35/20 : x{b['rapport_35_sur_20']}")
verifie("canari : le modele ne raisonne PAS en couches sur toute la surface",
        b["volume_d_une_bande_m3"] < b["surface_zone_m2"] * b["epaisseur_de_dalle_m"] / 2,
        f"une bande fait {b['volume_d_une_bande_m3']} m3, la zone entiere "
        f"{b['surface_zone_m2'] * b['epaisseur_de_dalle_m']:.0f} m3")
verifie("toutes les options de rotation tiennent le debit minimal",
        all(o["au_dessus_du_minimum"] for o in b["options_de_rotation"]))
verifie("le debit tenu croit avec le nombre de toupies, et plafonne a la pompe",
        all(a["debit_tenu_m3_h"] <= z["debit_tenu_m3_h"] + 1e-9
            for a, z in zip(b["options_de_rotation"], b["options_de_rotation"][1:]))
        and b["options_de_rotation"][-1]["debit_tenu_m3_h"]
        <= b["debit_pratique_d_une_pompe_m3_h"] + 1e-9)
verifie("l'option retenue est la premiere qui tient la duree cible",
        b["option_retenue"]["duree_du_coulage_h"] <= b["duree_cible_du_coulage_h"]
        and all(o["duree_du_coulage_h"] > b["duree_cible_du_coulage_h"]
                for o in b["options_de_rotation"]
                if o["toupies"] < b["option_retenue"]["toupies"]),
        f"{b['toupies_retenues']} toupies en {b['duree_du_coulage_h']} h")
verifie("tenir le seul minimum ferait finir le coulage bien plus tard",
        b["options_de_rotation"][0]["duree_du_coulage_h"] > b["duree_cible_du_coulage_h"],
        f"{b['options_de_rotation'][0]['duree_du_coulage_h']} h avec "
        f"{b['toupies_pour_tenir_le_minimum']} toupies")

# ------------------------------------------------- points d'arret
pa = r["points_d_arret"]
verifie("chaque point d'arret porte son viseur et son critere",
        all(x["vise_par"] and x["critere"] for x in pa["liste"]), f"{pa['nombre']} points")
verifie("le visa du ferraillage est une tache du cycle, avec sa duree",
        pa["duree_dans_le_cycle_j"] == d["cycle_zone"]["point_arret_visa_ferraillage_j"]["valeur"],
        f"{pa['duree_dans_le_cycle_j']} j, soit {pa['part_du_cycle_pct']} % du cycle")
verifie("le decoffrage porte un critere de RESISTANCE, pas un delai",
        "résistance" in next(x for x in pa["liste"]
                             if x["etape"] == "Décoffrage")["critere"].lower())
verifie("la double lecture entreprise / maitrise d'oeuvre est presente",
        set(pa["double_lecture"]) == {"entreprise", "maitrise_d_oeuvre"})
verifie("chaque controle avant coulage porte son symptome",
        all(x["symptome_si_rate"] for x in r["controles_avant_coulage"]["liste"]),
        f"{len(r['controles_avant_coulage']['liste'])} controles")

print(f"\n{len(echecs)} echec(s)." if echecs else "\nTests du gros oeuvre : tous verts.")
sys.exit(1 if echecs else 0)
