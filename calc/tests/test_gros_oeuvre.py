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
pr = json.loads((RACINE / "calc" / "sorties" / "prix.json").read_text(encoding="utf-8"))
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
verifie("les deux marges du plancher sont celles que D2 publie",
        abs(op["marge_libre_j"] - pl["durees"]["MEZZ"]["marge_libre_j"]) < 0.01
        and abs(op["marge_totale_j"] - pl["durees"]["MEZZ"]["marge_totale_j"]) < 0.01,
        f"libre {op['marge_libre_j']} j, totale {op['marge_totale_j']} j")

# Le retard du chantier est MESURE en rejouant le reseau, pas deduit d'une marge. On le
# verifie en rejouant nous-memes pour la ligne la plus allongee.
_pire = max((x for x in op["lignes"] if x.get("total_MAD") is not None),
            key=lambda x: x["rallonge_j"])
import planification as _pln                                             # noqa: E402
_q = _pln.quantites_chantier(d, d["planning"])
_t = _pln.durees_chantier(d, d["planning"], _q, _pire["duree_du_plancher_j"])
_f = _pln.planning_avec_fenetres(d, _t)
_duree = _pln.voie_A_parcours(_f["taches"])["duree"]
_retard = max(0.0, _duree - pl["reseau"]["duree_avec_fenetres_j"])
verifie("le retard du chantier est recalcule ici en rejouant le reseau",
        abs(_pire["retard_du_chantier_j"] - _retard) < 0.05,
        f"{_pire['retard_du_chantier_j']} j pour une rallonge de {_pire['rallonge_j']} j")

# canari : la marge LIBRE est le mauvais seuil pour cette question, et c'etait le
# bloquant B1 de la passe. On verifie que le modele ne l'utilise plus.
_avec_marge_libre = [x for x in op["lignes"] if x.get("total_MAD") is not None
                     and x["rallonge_j"] > op["marge_libre_j"]
                     and x["retard_du_chantier_j"] < 1e-9]
verifie("canari : une rallonge au-dela de la marge LIBRE ne declenche aucun frais de duree",
        bool(_avec_marge_libre),
        f"{len(_avec_marge_libre)} ligne(s) au-dela de la marge libre et sans retard — "
        "la premiere version leur imputait des frais de duree")
for x in op["lignes"]:
    if x.get("total_MAD") is None:
        continue
    verifie(f"parc {x['parc_m2']} m2 : des frais de duree si et seulement si la fin bouge",
            (x["frais_de_duree_MAD"] > 0) == (x["retard_du_chantier_j"] > 0),
            f"retard {x['retard_du_chantier_j']} j")
    verifie(f"parc {x['parc_m2']} m2 : le regime annonce correspond aux marges",
            (("libre" in x["regime"] and "totale" not in x["regime"])
             == (x["rallonge_j"] <= op["marge_libre_j"] + 1e-6)),
            x["regime"][:45])

verifie("l'optimum de cout est bien le minimum du total, recalcule ici",
        op["optimum_de_cout"]["total_MAD"] == min(x["total_MAD"] for x in op["lignes"]
                                                  if x.get("total_MAD") is not None),
        f"{op['optimum_de_cout']['parc_m2']} m2 a {op['optimum_de_cout']['total_MAD']:,.0f} MAD")
# Ce test ne verrouille PAS une conclusion narrative. La version precedente verifiait
# que l'optimum « n'est ni le plus petit ni le plus grand » : c'etait une propriete des
# six valeurs choisies, pas du modele, et elle a survecu a un bloquant qu'elle aurait du
# faire tomber. On verifie la REGLE : tant qu'aucun parc ne retarde la fin, le moins
# cher est le plus petit faisable.
_sans_retard = [x for x in op["lignes"] if x.get("total_MAD") is not None
                and x["retard_du_chantier_j"] < 1e-9]
if len(_sans_retard) == len([x for x in op["lignes"] if x.get("total_MAD") is not None]):
    verifie("aucun parc ne retarde la fin : l'optimum de cout est donc le plus petit faisable",
            op["optimum_de_cout"]["parc_m2"] == min(x["parc_m2"] for x in _sans_retard),
            "et le module le dit au lieu de presenter un U")
verifie("le module publie AUSSI le plus petit parc sans rallonge, qui n'est pas l'optimum de cout",
        op["plus_petit_parc_sans_rallonge"]["parc_m2"] > op["optimum_de_cout"]["parc_m2"],
        f"{op['plus_petit_parc_sans_rallonge']['parc_m2']} m2 contre "
        f"{op['optimum_de_cout']['parc_m2']} — ecart {op['ecart_entre_les_deux_choix_MAD']:,.0f} MAD")
verifie("l'ecart entre les deux choix est recalcule ici",
        abs(op["ecart_entre_les_deux_choix_MAD"]
            - (op["plus_petit_parc_sans_rallonge"]["total_MAD"]
               - op["optimum_de_cout"]["total_MAD"])) < 1)
verifie("et le module dit explicitement que l'optimum de cout n'est pas une decision",
        "n'est pas" in op["ce_que_le_cout_ne_decide_pas"]
        or "hypothese" in op["ce_que_le_cout_ne_decide_pas"])
verifie("les frais de duree sont LUS chez D1, pas re-derives",
        abs(op["frais_de_duree_MAD_par_jour_ouvre"]
            - pr["bordereau"]["frais_de_duree"]["cout_MAD_par_jour_ouvre"]) < 0.01,
        f"{op['frais_de_duree_MAD_par_jour_ouvre']} MAD/j ouvre")

# ------------------------------------------------- betonnage par temps chaud
b = r["betonnage"]
cz = d["geometrie"]["mezzanine"]["zones_de_coulage"]
_larg = G["betonnage_temps_chaud"]["largeur_de_bande_m"]["valeur"]
_sens = G["betonnage_temps_chaud"]["sens_d_avancement"]["valeur"]
_avance = cz["longueur_zone_m"] if _sens == "dans la longueur" else cz["largeur_zone_m"]
import math as _m
_n = _m.ceil(_avance / _larg)
_vol = tv["quantites"]["beton_m3"] / _n
verifie("le volume d'une bande est recalcule ici, poutres comprises",
        abs(b["volume_d_une_bande_m3"] - _vol) < 0.05,
        f"{b['volume_d_une_bande_m3']} m3 = {tv['quantites']['beton_m3']} / {_n} bandes")
verifie("le debit minimal est le volume d'une bande divise par le temps de maniabilite",
        all(abs(v["debit_minimal_m3_h"] - _vol / v["temps_de_maniabilite_h"]) < 0.1
            for v in b["par_temperature"].values()))
verifie("le debit minimal CROIT quand la temperature monte",
        b["par_temperature"]["a_35_degres"]["debit_minimal_m3_h"]
        > b["par_temperature"]["a_30_degres"]["debit_minimal_m3_h"]
        > b["par_temperature"]["a_20_degres"]["debit_minimal_m3_h"],
        f"rapport 35/20 : x{b['rapport_35_sur_20']}")
ctrl = b["controle_les_bandes_font_la_zone"]
verifie("les bandes reconstituent EXACTEMENT le volume de la zone, poutres comprises",
        abs(ctrl["ecart_m3"]) < 0.01,
        f"{ctrl['somme_des_bandes_m3']} contre {ctrl['volume_de_la_zone_m3']} m3")
verifie("canari : une bande vaut plus que la seule dalle sur sa surface",
        b["volume_d_une_bande_m3"]
        > b["largeur_de_bande_m"] * b["longueur_de_bande_m"] * b["epaisseur_de_dalle_m"] + 0.1,
        "sinon les poutres seraient hors du debit minimal, la ou la reprise froide est "
        "le plus grave")
verifie("le sens d'avancement est declare dans data/, pas pris par un min() silencieux",
        b["sens_d_avancement"] == d["gros_oeuvre"]["betonnage_temps_chaud"]["sens_d_avancement"]["valeur"],
        b["sens_d_avancement"])
verifie("la duree de coulage retenue est coherente avec le cycle du module TV",
        b["duree_du_coulage_h"] <= b["duree_du_betonnage_au_cycle_TV_h"] + 0.01,
        f"{b['duree_du_coulage_h']} h contre {b['duree_du_betonnage_au_cycle_TV_h']} h au cycle TV")
verifie("et l'attelage retenu est celui qu'implique ce cycle, pas la cible horaire seule",
        b["toupies_retenues"] >= b["option_qui_tient_la_cible_horaire"]["toupies"],
        f"{b['toupies_retenues']} toupies contre "
        f"{b['option_qui_tient_la_cible_horaire']['toupies']} pour la seule cible horaire")
verifie("canari obsolete : le modele ne raisonne PAS en couches sur toute la surface",
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
verifie("l'option qui tient la cible horaire est la premiere a y arriver",
        b["option_qui_tient_la_cible_horaire"]["duree_du_coulage_h"]
        <= b["duree_cible_du_coulage_h"]
        and all(o["duree_du_coulage_h"] > b["duree_cible_du_coulage_h"]
                for o in b["options_de_rotation"]
                if o["toupies"] < b["option_qui_tient_la_cible_horaire"]["toupies"]),
        f"{b['option_qui_tient_la_cible_horaire']['toupies']} toupies")
verifie("et l'option RETENUE est la plus exigeante des trois contraintes",
        b["toupies_retenues"] >= max(b["toupies_pour_tenir_le_minimum"],
                                     b["option_qui_tient_la_cible_horaire"]["toupies"]),
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
verifie("sa part est rapportee a la DUREE du cycle, pas a la somme de ses taches",
        abs(pa["part_du_cycle_pct"]
            - pa["duree_dans_le_cycle_j"] / r["cycle"]["duree_j"] * 100) < 0.02,
        f"{pa['part_du_cycle_pct']} % ; rapportee a la somme des durees elle vaudrait "
        f"{pa['duree_dans_le_cycle_j'] / tv['cycle_zone']['somme_des_durees_j'] * 100:.2f} %")

# la fenetre de coulage se DEDUIT, et sa consequence securite est publiee
fe = r["fenetre_de_coulage"]
verifie("l'heure de demarrage est deduite de l'heure de fin voulue",
        "FINI" in fe["regle"] and bool(fe["demarrage_deduit"]),
        f"fin voulue {fe['heure_de_fin_voulue']} -> demarrage {fe['demarrage_deduit']}")
verifie("le module dit si le coulage demarre avant le lever du soleil, et ce que ca implique",
        isinstance(fe["demarrage_avant_le_jour"], bool) and fe["consequence_securite"],
        f"lever {fe['lever_du_soleil']}, demarrage {fe['demarrage_deduit']}")
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
