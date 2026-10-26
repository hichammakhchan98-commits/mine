"""Tests du module D4 — suivi et controle.

Chaque controle est double d'une erreur injectee qui DOIT le faire sonner, et les
valeurs cles sont recalculees ICI, depuis data/ et les sorties des modules amont,
sans rappeler le code de production.
"""
from __future__ import annotations
import copy, json, sys, pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import planification as pln                                              # noqa: E402
import suivi as sv                                                       # noqa: E402

echecs = []


def verifie(nom, condition, detail=""):
    if not condition:
        echecs.append(nom)
    print(f"  {'ok   ' if condition else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
r = json.loads((RACINE / "calc" / "sorties" / "suivi.json").read_text(encoding="utf-8"))
pla = json.loads((RACINE / "calc" / "sorties" / "planification.json").read_text(encoding="utf-8"))
pr = json.loads((RACINE / "calc" / "sorties" / "prix.json").read_text(encoding="utf-8"))
S = d["suivi_chantier"]
J = float(S["date_arret_j"])
et = r["etats"]

# ------------------------------------------------- l'avancement planifie est DERIVE
# Recalcul independant depuis les segments de travail publies par D2.
seg = pla["segments_de_travail"]
for i in ("MEZZ", "CHFA", "PSOU", "CHLV", "SECO"):
    fait = sum(max(0.0, min(J, b) - a) for a, b in seg[i])
    tot = sum(b - a for a, b in seg[i])
    att = fait / tot * 100 if tot else 0.0
    verifie(f"{i} : avancement planifie recalcule depuis les segments de D2",
            abs(et["planifie"][i] - att) < 0.02, f"{et['planifie'][i]} % contre {att:.2f} %")

# canari : un prorata uniforme du temps ecoule donnerait un tout autre tableau
prorata = J / pla["reseau"]["duree_avec_fenetres_j"] * 100
ecarts = [abs(et["planifie"][i] - prorata) for i in et["planifie"]]
verifie("canari : l'avancement planifie n'est PAS un prorata du temps ecoule",
        max(ecarts) > 40, f"prorata {prorata:.1f} %, ecart maximal {max(ecarts):.1f} points")

# ------------------------------------------------- trois tableaux, deux ecarts
for i, pts in S["ecarts_constates_pts"].items():
    if i.startswith("_"):
        continue
    verifie(f"{i} : constate = planifie + ecart constate",
            abs(et["constate"][i] - max(0, min(100, et["planifie"][i] + pts))) < 0.02,
            f"{et['planifie'][i]} + ({pts}) = {et['constate'][i]}")
for i, pts in S["optimisme_declare_pts"].items():
    if i.startswith("_"):
        continue
    verifie(f"{i} : declare = constate + optimisme declare",
            abs(et["declare"][i] - max(0, min(100, et["constate"][i] + pts))) < 0.02,
            f"{et['constate'][i]} + {pts} = {et['declare'][i]}")
verifie("aucun avancement ne sort de [0 ; 100]",
        all(0 <= v <= 100 for tab in et.values() for v in tab.values()))
verifie("les postes sans ecart declare sont identiques dans les trois tableaux",
        all(et["constate"][i] == et["declare"][i] for i in et["constate"]
            if i not in S["optimisme_declare_pts"]))

# ------------------------------------------------- trois avancements, jamais egaux
av = r["avancements"]
verifie("les trois avancements different au meme instant",
        len({round(av["physique_pct"], 1), round(av["financier_pct"], 1),
             round(av["temporel_pct"], 1)}) == 3,
        f"physique {av['physique_pct']} / financier {av['financier_pct']} / "
        f"temporel {av['temporel_pct']} %")
verifie("le temporel est recalcule ici",
        abs(av["temporel_pct"] - J / r["date_arret"]["duree_totale_j"] * 100) < 0.02)
verifie("le financier est en dessous du physique : retenue et avance s'y soustraient",
        av["financier_pct"] < av["physique_pct"],
        f"{av['ecart_physique_financier_pts']} points d'ecart")
# L'ecart physique/temporel n'est PAS un avance-retard : le verdict se lit au constate
# contre le planifie de la MEME date, et les deux pointent en sens INVERSE ici.
_ve_ = r["valeur_acquise"]
verifie("l'avance-retard est mesure constate contre planifie, sur la meme assiette",
        abs(av["avance_ou_retard_pts"]
            - (_ve_["valeur_acquise_VA_MAD"] - _ve_["valeur_planifiee_VP_MAD"])
            / _ve_["budget_a_l_achevement_BAC_MAD"] * 100) < 0.02,
        f"{av['avance_ou_retard_pts']} pts")
verifie("canari : l'ecart au temporel conclurait l'INVERSE du vrai avance-retard",
        av["ecart_physique_temporel_pts"] * av["avance_ou_retard_pts"] < 0,
        f"temporel : +{av['ecart_physique_temporel_pts']} pts (« en avance ») contre "
        f"{av['avance_ou_retard_pts']} pts reels — le signe s'inverse")
verifie("le signe de l'avance-retard est celui du SPI",
        (av["avance_ou_retard_pts"] < 0) == (_ve_["SPI"] < 1.0))

# ------------------------------------------------- valeur acquise
ve = r["valeur_acquise"]
verifie("CPI = VA / CR", abs(ve["CPI"] - ve["valeur_acquise_VA_MAD"] / ve["cout_reel_CR_MAD"]) < 1e-4)
verifie("SPI = VA / VP", abs(ve["SPI"] - ve["valeur_acquise_VA_MAD"] / ve["valeur_planifiee_VP_MAD"]) < 1e-4)
verifie("CV = VA - CR", abs(ve["ecart_de_cout_CV_MAD"]
                           - (ve["valeur_acquise_VA_MAD"] - ve["cout_reel_CR_MAD"])) < 1)
verifie("SV = VA - VP", abs(ve["ecart_de_delai_SV_MAD"]
                           - (ve["valeur_acquise_VA_MAD"] - ve["valeur_planifiee_VP_MAD"])) < 1)
verifie("les trois EAC sont ordonnees : derive qui cesse < derive qui persiste < cout et delai",
        ve["EAC_si_la_derive_cesse_MAD"] < ve["EAC_si_la_derive_persiste_MAD"]
        < ve["EAC_cout_et_delai_MAD"],
        f"{ve['EAC_si_la_derive_cesse_MAD']:,.0f} < {ve['EAC_si_la_derive_persiste_MAD']:,.0f} "
        f"< {ve['EAC_cout_et_delai_MAD']:,.0f}")
# B1 : la courbe de depense et la valeur acquise doivent partager leur decoupage.
_seg = pla["segments_de_travail"]
_par_id = pr["bordereau"]["par_poste"]
_vp_seg = 0.0
for i, segs in _seg.items():
    tot = sum(b2 - a2 for a2, b2 in segs) or 1e-9
    fait = sum(max(0.0, min(J, b2) - a2) for a2, b2 in segs)
    _vp_seg += _par_id[i]["debourse_sec_total_MAD"] * fait / tot
verifie("la valeur planifiee est batie sur les SEGMENTS, comme la valeur acquise",
        abs(ve["valeur_planifiee_VP_MAD"] - _vp_seg) / _vp_seg < 0.01,
        f"{ve['valeur_planifiee_VP_MAD']:,.0f} contre {_vp_seg:,.0f} MAD recalcules")
verifie("canari : l'etaler sur le span debut->fin donnerait un autre nombre",
        abs(sum(_par_id[i]["debourse_sec_total_MAD"]
                * max(0.0, min(J, pla["durees"][i]["fin_j"]) - pla["durees"][i]["debut_j"])
                / max(1e-9, pla["durees"][i]["fin_j"] - pla["durees"][i]["debut_j"])
                for i in _seg) - _vp_seg) > 100000,
        "une tache qui attend sa fenetre ne depense pas")
verifie("la VP vient de la courbe de DEPENSE, pas de la courbe de travail de D2",
        abs(ve["valeur_planifiee_VP_MAD"] / ve["budget_a_l_achevement_BAC_MAD"] * 100
            - av["temporel_pct"]) > 5,
        "sinon la VP ne serait qu'un prorata du temps")

# canari : valoriser la VA sur le DECLARE la gonflerait — c'est l'erreur a ne pas faire
_bord = pr["bordereau"]["par_poste"]
va_declare = sum(_bord[i]["debourse_sec_total_MAD"] * et["declare"][i] / 100 for i in et["declare"])
va_constate = sum(_bord[i]["debourse_sec_total_MAD"] * et["constate"][i] / 100 for i in et["constate"])
verifie("la VA est valorisee sur le CONSTATE, et vaut EXACTEMENT la somme des ouvrages",
        abs(ve["valeur_acquise_VA_MAD"] - va_constate) < 1,
        f"{ve['valeur_acquise_VA_MAD']:,.0f} MAD")
verifie("canari : la valoriser sur le declare la gonflerait",
        va_declare > va_constate + 1000,
        f"declare {va_declare:,.0f} contre constate {va_constate:,.0f} MAD")
# B8 : les frais de duree sont HORS de la valeur acquise, et le BAC le dit
verifie("les frais de duree sont exclus du perimetre de la valeur acquise",
        abs(ve["budget_total_avec_frais_de_duree_MAD"] - ve["budget_a_l_achevement_BAC_MAD"]
            - ve["frais_de_duree"]["total_a_l_achevement_MAD"]) < 1,
        f"BAC ouvrages {ve['budget_a_l_achevement_BAC_MAD']:,.0f} + frais "
        f"{ve['frais_de_duree']['total_a_l_achevement_MAD']:,.0f}")
verifie("canari : un ouvrage a un avancement constate, des frais de chantier n'en ont pas",
        abs(ve["frais_de_duree"]["engages_a_la_date_MAD"]
            - ve["frais_de_duree"]["total_a_l_achevement_MAD"]
            * ve["frais_de_duree"]["part_du_temps_ecoulee"])
        < ve["frais_de_duree"]["total_a_l_achevement_MAD"] * 1e-4,   # arrondi de la part
        "les frais suivent le TEMPS, et c'est pour cela qu'ils sont a part")
# B6 : D-036, les bornes
fo = ve["fourchette"]
verifie("les indices sont publies avec leurs bornes (D-036)",
        fo["cout_reel_haut"]["CPI"] < ve["CPI"] < fo["cout_reel_bas"]["CPI"],
        f"CPI de {fo['cout_reel_haut']['CPI']} a {fo['cout_reel_bas']['CPI']}")
verifie("et le module dit si le diagnostic change de signe dans la fourchette",
        fo["le_diagnostic_change_de_signe"]
        == (fo["cout_reel_bas"]["diagnostic"] != fo["cout_reel_haut"]["diagnostic"]),
        "ici il change : un CPI dont la fourchette contient 1 n'est pas une alerte")

# ------------------------------------------------- ce qui porte la date
cd_ = r["ce_qui_porte_la_date"]
verifie("aucune tache a marge nulle n'a commence a cette date, et le module le dit",
        not cd_["taches_a_marge_nulle_demarrees"]
        and cd_["un_indice_sur_elles_est_il_defini"] is False,
        f"{len(cd_['taches_a_marge_nulle'])} taches critiques, zero demarree")
verifie("le module ne publie donc PAS d'indice sur le chemin critique",
        "SPI_en_duree_du_chemin" not in cd_,
        "un indice 0/0 n'est pas un indice")
_crit = pla["reseau"]["contre_calcul_cpm"]["taches_critiques_voie_A"]
verifie("les taches a marge nulle sont celles que D2 publie", cd_["taches_a_marge_nulle"] == _crit)
# chaque derive : retard et marge restante recalcules ici
for x in cd_["derives"]:
    i = x["tache"]
    _perdu = (et["planifie"][i] - et["constate"][i]) / 100 * pla["durees"][i]["duree_j"]
    verifie(f"{i} : le retard en jours est recalcule ici",
            abs(x["retard_j"] - _perdu) < 0.02, f"{x['retard_j']} j")
    verifie(f"{i} : la marge restante est la marge de D2 moins ce retard",
            abs(x["marge_totale_restante_j"]
                - (pla["durees"][i]["marge_totale_j"] - _perdu)) < 0.02,
            f"{x['marge_totale_restante_j']} j sur {pla['durees'][i]['marge_totale_j']}")
    verifie(f"{i} : « menace la date » si et seulement si le retard depasse la marge totale",
            x["menace_la_date"] == (_perdu > pla["durees"][i]["marge_totale_j"] + 1e-9))
verifie("la derive la plus menacante est celle dont il reste le moins de marge",
        cd_["derive_la_plus_menacante"]["marge_totale_restante_j"]
        == min(x["marge_totale_restante_j"] for x in cd_["derives"]),
        f"{cd_['derive_la_plus_menacante']['tache']} : "
        f"{cd_['derive_la_plus_menacante']['marge_totale_restante_j']} j")
verifie("une derive peut decaler un successeur sans menacer la date, et les deux sont distingues",
        any(x["decale_un_successeur"] and not x["menace_la_date"] for x in cd_["derives"]),
        f"{cd_['derives_qui_decalent_un_successeur']}")

# ------------------------------------------------- fiabilite du CPI
fi = r["fiabilite_du_cpi"]
verifie("l'incertitude du CPI decroit quand l'avancement augmente",
        all(a["incertitude_pts"] >= b["incertitude_pts"] - 1e-9
            for a, b in zip(fi["points"], fi["points"][1:])))
verifie("le seuil de lisibilite est le premier point sous la derive simulee",
        fi["avancement_ou_le_CPI_devient_lisible_pct"] is not None
        and next(p for p in fi["points"]
                 if p["avancement_pct"] == fi["avancement_ou_le_CPI_devient_lisible_pct"]
                 )["incertitude_pts"] < fi["derive_simulee_pct"],
        f"{fi['avancement_ou_le_CPI_devient_lisible_pct']} % d'avancement")

# ------------------------------------------------- visa
vi = r["visa"]
_att = sum(pr["bordereau"]["par_poste"][l["poste"]]["prix_total_MAD"]
           * (et["declare"][l["poste"]] - et["constate"][l["poste"]]) / 100
           for l in vi["lignes_reduites"])
verifie("les travaux retires au visa sont recalcules ici",
        abs(vi["travaux_retires_MAD"] - _att) < 1, f"{vi['travaux_retires_MAD']:,.0f} MAD")
# B2 : le net vise se REJOUE, il ne se soustrait pas
verifie("la reduction du NET est plus faible que les travaux retires",
        0 < vi["reduction_du_net_MAD"] < vi["travaux_retires_MAD"],
        f"{vi['reduction_du_net_MAD']:,.0f} contre {vi['travaux_retires_MAD']:,.0f} MAD")
verifie("canari : soustraire les travaux bruts du net serait la faute symetrique du controle n 4",
        abs((vi["net_declare_MAD"] - vi["travaux_retires_MAD"]) - vi["net_vise_MAD"]) > 1000,
        "retirer des travaux fait aussi baisser la retenue et le remboursement d'avance")
verifie("les postes reduits sont exactement ceux ou le declare depasse le constate",
        sorted(l["poste"] for l in vi["lignes_reduites"])
        == sorted(i for i in et["declare"] if et["declare"][i] > et["constate"][i] + 1e-9))
verifie("le net vise est inferieur au net declare",
        vi["net_vise_MAD"] < vi["net_declare_MAD"],
        f"-{vi['reduction_pct']} %")
verifie("chaque controle du visa rend un resultat, et aucun n'est vide",
        all(c["resultat"] for c in vi["controles"]), f"{len(vi['controles'])} controles")

# ------------------------------------------------- modification
mo = r["modification"]
verifie("le cout complet d'une modification est travaux + frais de duree",
        abs(mo["cout_complet_MAD"]
            - (mo["montant_des_travaux_MAD"] + mo["frais_indexes_sur_la_duree_MAD"])) < 1)
verifie("la part cachee est recalculee ici",
        abs(mo["part_cachee_pct"] - mo["frais_indexes_sur_la_duree_MAD"]
            / mo["cout_complet_MAD"] * 100) < 0.05, f"{mo['part_cachee_pct']} %")
verifie("refuser le delai coute plus cher que l'accorder",
        mo["si_le_delai_n_est_pas_accorde_MAD"] > mo["frais_indexes_sur_la_duree_MAD"],
        f"{mo['si_le_delai_n_est_pas_accorde_MAD']:,.0f} contre "
        f"{mo['frais_indexes_sur_la_duree_MAD']:,.0f} MAD")
verifie("le nouveau BAC integre les deux effets, pas seulement le montant des travaux",
        mo["nouveau_BAC_MAD"] > ve["budget_a_l_achevement_BAC_MAD"] + mo["montant_des_travaux_MAD"])

print(f"\n{len(echecs)} echec(s)." if echecs else "\nTests du suivi : tous verts.")
sys.exit(1 if echecs else 0)
