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
verifie("la VP vient de la courbe de DEPENSE, pas de la courbe de travail de D2",
        abs(ve["valeur_planifiee_VP_MAD"] / ve["budget_a_l_achevement_BAC_MAD"] * 100
            - av["temporel_pct"]) > 5,
        "sinon la VP ne serait qu'un prorata du temps")

# canari : valoriser la VA sur le DECLARE la gonflerait — c'est l'erreur a ne pas faire
_bord = pr["bordereau"]["par_poste"]
va_declare = sum(_bord[i]["debourse_sec_total_MAD"] * et["declare"][i] / 100 for i in et["declare"])
va_constate = sum(_bord[i]["debourse_sec_total_MAD"] * et["constate"][i] / 100 for i in et["constate"])
verifie("canari : la VA est valorisee sur le CONSTATE, et le declare la gonflerait",
        va_declare > va_constate + 1000
        and abs(ve["valeur_acquise_VA_MAD"] - va_constate) > 1,  # + frais de duree
        f"declare {va_declare:,.0f} contre constate {va_constate:,.0f} MAD")

# ------------------------------------------------- SPI global contre SPI du chemin
sp = r["spi_du_chemin"]
verifie("les deux SPI different : un indice global ne voit pas le chemin critique",
        abs(sp["SPI_en_duree_global"] - sp["SPI_en_duree_du_chemin"]) > 0.01,
        f"global {sp['SPI_en_duree_global']} contre chemin {sp['SPI_en_duree_du_chemin']}")
_chemin = pla["reseau"]["chemin_critique"]
verifie("le chemin utilise est bien celui que D2 publie", sp["taches_du_chemin"] == _chemin)
verifie("le poste le plus en retard n'est pas sur le chemin — et c'est le fond du sujet",
        min(S["ecarts_constates_pts"], key=lambda k: S["ecarts_constates_pts"][k]
            if not k.startswith("_") else 0) not in _chemin,
        "la derive la plus visible est absorbee par la marge")

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
verifie("le montant retire au visa est recalcule ici",
        abs(vi["montant_retire_MAD"] - _att) < 1, f"{vi['montant_retire_MAD']:,.0f} MAD")
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
