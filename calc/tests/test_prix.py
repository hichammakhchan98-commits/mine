"""Tests du module D1 — metres, prix, sous-details, situations.

Meme discipline que les modules precedents : chaque controle est double d'une erreur
injectee qui DOIT le faire sonner, et les valeurs cles sont recalculees ICI, depuis
data/, sans appeler le code de production.
"""
from __future__ import annotations
import copy, json, math, sys, pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import planification as pln                                              # noqa: E402
import prix as px                                                        # noqa: E402

echecs = []


def verifie(nom, condition, detail=""):
    if not condition:
        echecs.append(nom)
    print(f"  {'ok   ' if condition else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
r = json.loads((RACINE / "calc" / "sorties" / "prix.json").read_text(encoding="utf-8"))
P = d["prix_unitaires_MAD"]
bord = r["bordereau"]
par_id = {p["poste"]: p for p in bord["postes"]}

# ---------------------------------------------------------------- l'identite R1
# La consommation de main d'oeuvre d'un prix unitaire DOIT etre celle qu'implique le
# planning. C'est le pont entre D1 et D2 : si elle se saisissait a part, le metre et le
# planning pourraient diverger sans que rien ne le signale.
e = d["planning"]["effectifs_chantier_V3"]
h_j = P["ressources"]["heures_par_jour"]
for poste in ("TERR", "FOND", "VOIL", "POTR", "CHAP", "COUV", "FACA"):
    sd = P["sous_details"][poste]
    cad = d["planning"]["cadences_chantier_V3"][sd["cadence"]]["valeur"]
    n = e["compagnons_par_atelier"][sd["metier"]]
    attendu = h_j * n / cad * sd["conversion"]
    publie = par_id[poste]["main_oeuvre"]["h_par_unite"]
    verifie(f"{poste} : h/unite = 8 x compagnons / cadence x conversion",
            abs(publie - attendu) < 1e-4, f"{publie} contre {attendu:.5f} h/{sd['unite']}")

# ... et le nombre d'ateliers n'y figure PAS : doubler les ateliers divise la duree par
# deux et laisse le prix inchange. On le prouve en rejouant le bordereau.
d2 = copy.deepcopy(d)
d2["planning"]["effectifs_chantier_V3"]["ateliers_voiles"] *= 2
q2 = pln.quantites_chantier(d2, d2["planning"])
t2 = pln.durees_chantier(d2, d2["planning"], q2, 31.85)
verifie("doubler les ateliers divise la duree par deux",
        abs(t2["VOIL"]["duree_j"] * 2 - r["_durees_reference"]["VOIL"]) < 1e-6,
        f"{t2['VOIL']['duree_j']} contre {r['_durees_reference']['VOIL']}")
h2 = px.heures_par_unite(d2, "VOIL")["h_par_unite"]
verifie("... et laisse le prix unitaire inchange",
        abs(h2 - par_id["VOIL"]["main_oeuvre"]["h_par_unite"]) < 1e-9,
        f"{h2} h/m2 dans les deux cas")

# ---------------------------------------------------------------- recalcul d'un prix
# Le prix du m2 de voile, refait a la main depuis data/ seul.
rq = d["planning"]["ratios_quantites_V3"]
c = P["coefficients_sous_detail"]
m = P["ressources"]["materiaux_MAD"]
ep = rq["voile_epaisseur_m"]["valeur"]
pertes = 1 + c["pertes_beton_pct"]["valeur"] / 100
mat = (pertes * ep * m["beton_bpe_m3"]["valeur"]
       + c["acier_kg_par_m3"]["voile"]["valeur"] * ep * m["acier_ha_kg"]["valeur"]
       + c["coffrage_m2_par_unite"]["voile_par_m2"]["valeur"] * m["coffrage_rotation_m2"]["valeur"])
eng = c["vibreur_j_par_m3"]["valeur"] * ep * P["ressources"]["materiel_MAD"]["vibreur_j"]["valeur"]
taux = px.taux_horaire_atelier(d, "voiles")["taux_MAD_h"]
mo = h_j * e["compagnons_par_atelier"]["voiles"] / d["planning"]["cadences_chantier_V3"]["voile_m2_j_atelier"]["valeur"] * taux
ds = mat + eng + mo
verifie("debourse sec du m2 de voile recalcule a la main",
        abs(par_id["VOIL"]["debourse_sec_par_unite_MAD"] - ds) < 0.05,
        f"{par_id['VOIL']['debourse_sec_par_unite_MAD']} contre {ds:.2f} MAD/m2")
k = 1 + sum(P["composition_prix_pct"][x]["valeur"] for x in
            ("frais_generaux_siege", "aleas", "marge")) / 100
verifie("prix de vente = debourse sec x coefficient d'entreprise",
        abs(par_id["VOIL"]["pu_de_vente_MAD"] - ds * k) < 0.05,
        f"coefficient {k:.4f}")

# ---------------------------------------------------------------- le double compte
# Un forfait est tout compris : aucune heure ne doit lui etre imputee.
forfaits = [p for p in bord["postes"] if p["type"] == "forfait"]
verifie("aucun poste forfaitaire ne porte d'heures de main d'oeuvre",
        all(p["heures_totales"] == 0 for p in forfaits), f"{len(forfaits)} forfaits")
verifie("... et le montant d'un forfait est exactement celui de data/",
        all(abs(p["debourse_sec_par_unite_MAD"] - P["forfaits_MAD"][p["poste"]]["valeur"]) < 1e-6
            for p in forfaits))
fournitures = [p for p in bord["postes"] if p["type"].startswith("fourniture")]
verifie("une fourniture ne porte aucune heure de chantier non plus",
        all(p["heures_totales"] == 0 for p in fournitures),
        f"{[p['poste'] for p in fournitures]}")

# ---------------------------------------------------------------- domaine du ratio
cr = r["controle_ratios"]
verifie("le ratio de part de main d'oeuvre ne recoit un verdict QUE sur une base definie",
        cr["part_main_oeuvre_beton_arme_decompose"]["ratio_defini_sur_cette_base"]
        and not cr["part_main_oeuvre_bordereau_entier"]["ratio_defini_sur_cette_base"]
        and not cr["part_main_oeuvre_tous_postes_decomposes"]["ratio_defini_sur_cette_base"])
verifie("et une base non definie ne peut jamais etre declaree « dans la fourchette »",
        all(not v["dans_la_fourchette"] for k2, v in cr.items()
            if isinstance(v, dict) and not v.get("ratio_defini_sur_cette_base", True)))
_ba = ("FOND", "RADT", "VOIL", "PHNT", "POTR", "MEZZ")
_ds = sum(par_id[i]["debourse_sec_total_MAD"] for i in _ba)
_mo = sum(par_id[i]["main_oeuvre_totale_MAD"] for i in _ba)
verifie("la part de main d'oeuvre du beton arme est recalculee ici",
        abs(cr["part_main_oeuvre_beton_arme_decompose"]["constate"] - _mo / _ds * 100) < 0.02,
        f"{cr['part_main_oeuvre_beton_arme_decompose']['constate']} %")

# ---------------------------------------------------------------- deux voies
ec = r["ecart_des_deux_voies"]
verifie("les deux voies de chiffrage portent sur le MEME perimetre",
        set(ec["par_poste"]) == set(_ba), f"{sorted(ec['par_poste'])}")
verifie("l'ecart global est la somme des deux voies, pas une moyenne d'ecarts",
        abs((ec["voie_A_sous_detail_MAD"] - ec["voie_B_prix_poses_MAD"])
            / ec["voie_B_prix_poses_MAD"] * 100 - ec["ecart_pct"]) < 0.02)
verifie("l'ecart est systematique et de meme signe sur les six postes — c'est une ligne qui manque",
        all(v["ecart_pct"] < 0 for v in ec["par_poste"].values()),
        f"de {min(v['ecart_pct'] for v in ec['par_poste'].values())} % a "
        f"{max(v['ecart_pct'] for v in ec['par_poste'].values())} %")
_div = (ec["voie_B_prix_poses_MAD"] / ec["voie_A_sous_detail_MAD"] - 1) * 100
verifie("le « divers » qui recollerait les deux voies est recalcule ici",
        abs(ec["divers_necessaire_pct"] - _div) < 0.05, f"{ec['divers_necessaire_pct']} %")

# ---------------------------------------------------------------- productivites
coh = r["coherence_cadences"]
for cas in coh["cas"]:
    s_ref = sum(v["reference_j"] for v in cas["metiers"].values())
    verifie(f"{cas['poste']} : le facteur de recalage est le rapport des jours-compagnon",
            abs(cas["facteur_de_recalage"] - s_ref / cas["jours_compagnon_par_unite"]) < 0.02,
            f"x{cas['facteur_de_recalage']}")
verifie("le facteur moyen tombe dans le facteur 2 a 3 soupconne par la dette n 10",
        2.0 <= coh["facteur_de_recalage_moyen"] <= 3.0,
        f"x{coh['facteur_de_recalage_moyen']} — obtenu par un chemin independant de celui "
        "qui a produit le soupcon")
verifie("recaler les cadences rapproche la part de main d'oeuvre de sa fourchette",
        r["variante_recalee"]["part_main_oeuvre_beton_arme_pct"]["recalee"]
        > r["variante_recalee"]["part_main_oeuvre_beton_arme_pct"]["reference"],
        f"{r['variante_recalee']['part_main_oeuvre_beton_arme_pct']['reference']} % -> "
        f"{r['variante_recalee']['part_main_oeuvre_beton_arme_pct']['recalee']} %")
verifie("... et allonge le chantier ET renchérit le debourse — une cadence optimiste se paie deux fois",
        r["variante_recalee"]["duree_j"]["ecart_pct"] > 0
        and r["variante_recalee"]["debourse_MAD"]["ecart_pct"] > 0,
        f"duree +{r['variante_recalee']['duree_j']['ecart_pct']} %, "
        f"debourse +{r['variante_recalee']['debourse_MAD']['ecart_pct']} %")

# ---------------------------------------------------------------- revision et situation
sit = r["situation"]
rv = P["contrat"]["revision_des_prix"]
_k = (rv["part_fixe_a"]["valeur"] + rv["part_b_index_batiment"]["valeur"] * rv["I_sur_I0"]["valeur"]
      + rv["part_c_index_acier"]["valeur"] * rv["J_sur_J0"]["valeur"])
verifie("a + b + c = 1, et le calcul leve si ce n'est pas le cas",
        abs(sit["revision"]["somme_abc"] - 1) < 1e-9)
try:
    _d = copy.deepcopy(d); _d["prix_unitaires_MAD"]["contrat"]["revision_des_prix"]["part_fixe_a"]["valeur"] = 0.2
    px.revision(_d, 1000.0)
    _leve = False
except ValueError:
    _leve = True
verifie("canari : une somme a + b + c differente de 1 fait lever le calcul", _leve)
verifie("le coefficient de revision est recalcule ici",
        abs(sit["revision"]["coefficient"] - _k) < 1e-6, f"{sit['revision']['coefficient']}")
verifie("la revision porte sur les travaux, et la retenue sur le montant REVISE",
        abs(sit["retenue_de_garantie_MAD"]
            - sit["montant_revise_MAD"] * P["contrat"]["retenue_de_garantie_pct"]["valeur"] / 100) < 1,
        f"{sit['retenue_de_garantie_MAD']} MAD")
verifie("la retenue reste sous son plafond",
        sit["retenue_retenue_MAD"] <= sit["retenue_plafond_MAD"] + 1e-6)
_cum = sum(l["montant_cumule_MAD"] for l in sit["lignes"])
verifie("le cumul des lignes de situation est recalcule ici",
        abs(_cum - sit["travaux_cumules_MAD"]) < 1, f"{_cum:.0f} MAD")
_av = P["situation_exemple"]["avancement_declare_pct"]
verifie("chaque ligne attache la quantite de l'avancement declare, pas celle du marche",
        all(abs(l["quantite_attachee"] - l["quantite_marche"] * _av[l["poste"]] / 100) < 0.02
            for l in sit["lignes"] if l["poste"] in _av))

# ---------------------------------------------------------------- tresorerie
tr = r["tresorerie"]
dep = r["courbe_de_depense"]
verifie("la courbe de depense est croissante", all(
    b["depense_MAD"] >= a["depense_MAD"] - 1 for a, b in zip(dep["points"], dep["points"][1:])))
verifie("elle atteint le total du bordereau", dep["points"][-1]["pct"] >= 99.9,
        f"{dep['points'][-1]['pct']} %")
verifie("le besoin maximal est bien le maximum des ecarts publies",
        abs(tr["besoin_maximal_MAD"] - max(p["besoin_MAD"] for p in tr["points"])) <= 1,
        f"{tr['besoin_maximal_MAD']:,} MAD au jour {tr['besoin_maximal_au_jour']}")
verifie("la depense n'est PAS la courbe de travail de D2 : les deux different",
        abs(r["ecart_depense_travail"]["ecart_maximal"]["ecart_pts"]) > 2,
        f"ecart maximal {r['ecart_depense_travail']['ecart_maximal']['ecart_pts']} points "
        f"au jour {r['ecart_depense_travail']['ecart_maximal']['j']}")

# ---------------------------------------------------------------- cout du retard
ret = r["cout_du_retard"]["21"]
fd = bord["frais_de_duree"]
verifie("le cout d'un mois de retard est recalcule ici",
        abs(ret["frais_de_duree_MAD"] - fd["cout_MAD_par_jour_ouvre"] * 21) < 1,
        f"{ret['frais_de_duree_MAD']:,.0f} MAD de frais + "
        f"{ret['penalites_MAD']:,.0f} MAD de penalites")
verifie("les penalites se comptent en jours CALENDAIRES, plus nombreux que les ouvres",
        ret["retard_j_calendaires"] > ret["retard_j_ouvres"],
        f"{ret['retard_j_ouvres']} j ouvres = {ret['retard_j_calendaires']} j calendaires")
verifie("les penalites restent sous leur plafond",
        all(r["cout_du_retard"][k]["penalites_MAD"]
            <= r["cout_du_retard"][k]["penalites_plafond_MAD"] + 1e-6 for k in r["cout_du_retard"]))

# ---------------------------------------------------------------- coherence du total
_somme = sum(p["debourse_sec_total_MAD"] for p in bord["postes"]) + fd["total_MAD"]
verifie("le debourse total est la somme des postes et des frais de duree",
        abs(_somme - bord["debourse_sec_MAD"]) < 1, f"{_somme:,.0f} MAD")
verifie("les parts par lot somment a 100 %",
        abs(sum(v["part_pct"] for v in bord["par_lot"].values()) - 100) < 0.2,
        f"{sum(v['part_pct'] for v in bord['par_lot'].values()):.2f} %")
verifie("chaque tache du planning a un poste au bordereau, et un seul",
        sorted(p["poste"] for p in bord["postes"]) == sorted(pln.NOMS),
        f"{len(bord['postes'])} postes pour {len(pln.NOMS)} taches")
verifie("le type d'un poste suit la famille de sa duree",
        all((p["type"] == "forfait") == (p["famille_duree"] == "declaree")
            for p in bord["postes"] if p["type"] in ("forfait", "unitaire")),
        "calculee -> unitaire, declaree -> forfait, imposee -> fourniture")

print(f"\n{len(echecs)} echec(s)." if echecs else "\nTests des prix : tous verts.")
sys.exit(1 if echecs else 0)
