"""Tests du module REC — reception, DOE, garanties.

Des tests de REGLE, jamais de conclusion (D-041, D-043) : aucun n'epingle « la caution
est moins chere » ni « le DOE reconstitue coute quatre fois plus ». Ils verifient que les
grandeurs sont composees correctement, que les bornes encadrent la valeur, et que ce que
le module LIT chez D1 est bien ce que D1 publie.
"""
from __future__ import annotations
import json, sys, pathlib, unicodedata

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))

echecs = []


def sansaccent(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s).lower())
                   if unicodedata.category(c) != "Mn")


def dit(texte, *mots):
    t_ = sansaccent(texte)
    return all(sansaccent(m) in t_ for m in mots)


def verifie(nom, condition, detail=""):
    if not condition:
        echecs.append(nom)
    print(f"  {'ok   ' if condition else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
r = json.loads((RACINE / "calc" / "sorties" / "reception.json").read_text(encoding="utf-8"))
pr = json.loads((RACINE / "calc" / "sorties" / "prix.json").read_text(encoding="utf-8"))
C = d["prix_unitaires_MAD"]["contrat"]
R = d["reception"]

# ------------------------------------------------- 1. le cout d'un jour, LU chez D1
print("\n--- le cout d'un jour de non-reception ---")
c = r["cout_d_un_jour"]
d1 = pr["cout_du_retard"]["1"]
verifie("les frais de duree sont ceux que D1 publie, au centime",
        abs(c["frais_de_duree_MAD_par_jour_ouvre"] - d1["frais_de_duree_MAD"]) < 0.01,
        f"{c['frais_de_duree_MAD_par_jour_ouvre']:.2f} MAD/j")
verifie("la penalite journaliere est celle que D1 publie",
        abs(c["penalites_MAD_par_jour_ouvre"] - d1["penalites_MAD"]) < 0.01,
        f"{c['penalites_MAD_par_jour_ouvre']:.2f} MAD/j ouvre")
verifie("le plafond est celui que D1 publie",
        abs(c["plafond_des_penalites_MAD"] - d1["penalites_plafond_MAD"]) < 0.01)
verifie("et D1 le retrouve bien a 10 % du marche",
        abs(c["plafond_des_penalites_MAD"]
            - c["marche_MAD"] * C["penalite_plafond_pct"]["valeur"] / 100) < 1,
        f"{c['plafond_des_penalites_MAD']:.0f} MAD")
verifie("cout avant le plafond = frais + penalite",
        abs(c["cout_avant_le_plafond_MAD_par_jour_ouvre"]
            - (d1["frais_de_duree_MAD"] + d1["penalites_MAD"])) < 0.01,
        f"{c['cout_avant_le_plafond_MAD_par_jour_ouvre']:.0f} MAD")
verifie("cout apres le plafond = les frais de duree SEULS",
        abs(c["cout_apres_le_plafond_MAD_par_jour_ouvre"]
            - d1["frais_de_duree_MAD"]) < 0.01)
verifie("le jour de bascule est le plafond divise par la penalite journaliere",
        abs(c["jour_de_bascule_ouvre"]
            - c["plafond_des_penalites_MAD"] / c["penalites_MAD_par_jour_ouvre"]) < 0.05,
        f"{c['jour_de_bascule_ouvre']} j ouvres")
verifie("et la forme fermee le retrouve sans le montant du marche",
        abs(c["forme_fermee_calendaire"] - c["jour_de_bascule_calendaire"]) < 0.1,
        f"{C['penalite_plafond_pct']['valeur']} % / "
        f"{C['penalite_retard_pour_mille_par_j']['valeur']} pour mille = "
        f"{c['forme_fermee_calendaire']} j calendaires")
verifie("les bornes du jour de bascule encadrent sa valeur",
        c["jour_de_bascule_bornes_calendaires"][0] <= c["jour_de_bascule_calendaire"]
        <= c["jour_de_bascule_bornes_calendaires"][1],
        f"{c['jour_de_bascule_bornes_calendaires']}")
verifie("le piege de calendrier de D1 est conserve : la penalite est en jours "
        "CALENDAIRES",
        abs(c["penalites_MAD_par_jour_ouvre"]
            - c["marche_MAD"] * C["penalite_retard_pour_mille_par_j"]["valeur"] / 1000
            * pr["bordereau"]["frais_de_duree"]["conversion"]["calendaires_par_jour_ouvre"]) < 1,
        "un jour ouvre porte 1,4 jour de penalite")
# canari qui CHERCHE : compter la penalite en jours OUVRES donnerait un autre nombre.
_naif = c["marche_MAD"] * C["penalite_retard_pour_mille_par_j"]["valeur"] / 1000
verifie("canari : compter la penalite en jours ouvres la sous-estimerait",
        abs(_naif - c["penalites_MAD_par_jour_ouvre"]) > 1000,
        f"{_naif:.0f} contre {c['penalites_MAD_par_jour_ouvre']:.0f} MAD")

print("\n--- la courbe du cout cumule ---")
co = r["courbe_du_cout"]
pts = {x["x"]: x["v"] * 1e6 for x in co["points"]}
js = sorted(pts)
verifie("elle part de zero", abs(pts[0]) < 1)
verifie("elle croit sans jamais decroitre",
        all(pts[a] <= pts[b] + 1e-6 for a, b in zip(js, js[1:])))
_avant = [j for j in js if j < c["jour_de_bascule_ouvre"] and j > 0]
_apres = [j for j in js if j > c["jour_de_bascule_ouvre"] + 10]
if len(_avant) >= 2:
    pente = (pts[_avant[-1]] - pts[_avant[-2]]) / (_avant[-1] - _avant[-2])
    verifie("la pente avant la bascule vaut frais + penalite",
            abs(pente - c["cout_avant_le_plafond_MAD_par_jour_ouvre"])
            < 0.01 * c["cout_avant_le_plafond_MAD_par_jour_ouvre"],
            f"{pente:.0f} MAD/j contre "
            f"{c['cout_avant_le_plafond_MAD_par_jour_ouvre']:.0f}")
if len(_apres) >= 2:
    pente = (pts[_apres[-1]] - pts[_apres[-2]]) / (_apres[-1] - _apres[-2])
    verifie("et la pente apres ne vaut plus que les frais de duree",
            abs(pente - c["cout_apres_le_plafond_MAD_par_jour_ouvre"])
            < 0.01 * c["cout_apres_le_plafond_MAD_par_jour_ouvre"],
            f"{pente:.0f} MAD/j contre "
            f"{c['cout_apres_le_plafond_MAD_par_jour_ouvre']:.0f}")

# ------------------------------------------------- 2. le portage
print("\n--- retenue de garantie contre caution ---")
p = r["portage"]
verifie("la retenue immobilisee est celle que D1 publie",
        abs(p["retenue_immobilisee_MAD"]
            - pr["tresorerie"]["retenue_de_garantie_finale_MAD"]) < 0.01,
        f"{p['retenue_immobilisee_MAD']:.0f} MAD")
verifie("et elle vaut bien le taux de retenue du contrat applique au marche",
        abs(p["retenue_immobilisee_MAD"]
            - c["marche_MAD"] * C["retenue_de_garantie_pct"]["valeur"] / 100) < 1)
verifie("le cout mensuel de la retenue = montant x taux annuel / 12",
        abs(p["cout_de_la_retenue_MAD_par_mois"]
            - p["retenue_immobilisee_MAD"] * p["taux_de_portage_annuel_pct"] / 100 / 12) < 0.02,
        f"{p['cout_de_la_retenue_MAD_par_mois']:.0f} MAD/mois")
verifie("le cout mensuel de la caution = montant x commission / 12",
        abs(p["cout_de_la_caution_MAD_par_mois"]
            - p["retenue_immobilisee_MAD"] * p["commission_de_caution_annuelle_pct"] / 100 / 12) < 0.02)
verifie("l'economie est la difference des deux",
        abs(p["economie_MAD_par_mois"] - (p["cout_de_la_retenue_MAD_par_mois"]
                                          - p["cout_de_la_caution_MAD_par_mois"])) < 0.02)
# INVARIANT, et c'est le coeur du raisonnement : le rapport ne contient ni la duree ni
# le montant. Le test le verifie sur le rapport des couts MENSUELS, qui sont des
# grandeurs publiees — pas en relisant la formule.
verifie("INVARIANT : le rapport des couts est celui des deux taux, sans duree ni montant",
        abs(p["cout_de_la_retenue_MAD_par_mois"] / p["cout_de_la_caution_MAD_par_mois"]
            - p["taux_de_portage_annuel_pct"] / p["commission_de_caution_annuelle_pct"]) < 0.001,
        f"x{p['rapport_des_deux_couts']}")
verifie("les bornes du rapport encadrent sa valeur",
        p["rapport_bornes"][0] <= p["rapport_des_deux_couts"] <= p["rapport_bornes"][1],
        f"{p['rapport_bornes']}")
verifie("le module dit que la duree se simplifie, et pourquoi",
        dit(p["_la_duree_se_simplifie"], "rapport", "duree"))
verifie("et il dit ce que le calcul ne decide PAS (D-041)",
        dit(p["_et_ce_qui_n_est_pas_dans_le_calcul"], "ligne de credit", "banque"))
verifie("il declare aussi que son chiffre est une borne basse",
        dit(p["_ce_que_la_comparaison_ne_compte_pas"], "borne basse", "situation"))

# ------------------------------------------------- 3. les reserves
print("\n--- les reserves : deux familles, une seule bloque ---")
s = r["reserves"]
verifie("le nombre total est la somme des familles",
        s["nb_total"] == sum(x["nombre"] for x in s["lignes"]),
        f"{s['nb_total']} reserves")
verifie("les bloquantes sont exactement celles qui empechent l'usage",
        s["nb_bloquantes"] == sum(x["nombre"] for x in s["lignes"] if x["empeche_l_usage"]),
        f"{s['nb_bloquantes']} bloquantes sur {s['nb_total']}")
verifie("chaque famille porte son exemple, et il est concret",
        all(len(x["exemple"]) > 25 for x in s["lignes"]))
verifie("les heures sont le nombre de reserves fois le temps unitaire",
        abs(s["heures_totales"]
            - s["nb_total"] * R["reserves"]["heures_par_levee_h"]["valeur"]) < 0.5,
        f"{s['heures_totales']:.0f} h")
verifie("les bornes des heures encadrent la valeur",
        s["heures_bornes"][0] <= s["heures_totales"] <= s["heures_bornes"][1],
        f"{s['heures_bornes']}")
verifie("la duree de levee est MESUREE sur les heures et l'effectif, pas posee",
        abs(s["jours_de_levee_des_autres"]
            - (s["heures_totales"] - sum(x["heures"] for x in s["lignes"]
                                         if x["empeche_l_usage"]))
            / (s["effectif_de_levee"]
               * d["prix_unitaires_MAD"]["ressources"]["heures_par_jour"])) < 0.02,
        f"{s['jours_de_levee_des_autres']} j a {s['effectif_de_levee']} compagnons")
verifie("le cout de la confusion est cette duree fois le cout d'un jour de D1",
        abs(s["cout_de_la_confusion_MAD"]
            - s["jours_de_levee_des_autres"]
            * c["cout_avant_le_plafond_MAD_par_jour_ouvre"]) < 1,
        f"{s['cout_de_la_confusion_MAD']:.0f} MAD")
verifie("ses bornes ne font varier QUE le temps de levee, pas le regime de penalite",
        abs(s["cout_de_la_confusion_bornes_MAD"][0] / s["cout_de_la_confusion_MAD"]
            - R["reserves"]["heures_par_levee_h"]["fourchette"][0]
            / R["reserves"]["heures_par_levee_h"]["valeur"]) < 0.01,
        f"{s['cout_de_la_confusion_bornes_MAD']}")
verifie("et le module publie aussi ce que la meme confusion coute APRES le plafond",
        s["cout_de_la_confusion_apres_le_plafond_MAD"] < s["cout_de_la_confusion_MAD"],
        f"{s['cout_de_la_confusion_apres_le_plafond_MAD']:.0f} MAD")
verifie("la regle de classement ne compte pas les reserves, elle les qualifie",
        dit(s["la_regle"], "empeche", "securite") and "nombre" in sansaccent(s["la_regle"]))
verifie("le module traite aussi l'erreur SYMETRIQUE, la plus dangereuse",
        dit(s["_et_dans_l_autre_sens"], "garde-corps", "comptage"))

# ------------------------------------------------- 4. le DOE
print("\n--- le DOE conditionne le solde ---")
o = r["doe"]
verifie("les heures des deux scenarios viennent de data/, avec leurs fourchettes",
        o["heures_au_fil_de_l_eau"] == R["doe"]["heures_au_fil_de_l_eau"]["valeur"]
        and "fourchette" in R["doe"]["heures_reconstitue"],
        f"{o['heures_au_fil_de_l_eau']} h contre {o['heures_reconstitue']} h")
verifie("elles sont payees au taux du CADRE, pas du compagnon",
        abs(o["taux_horaire_de_cadre_MAD"]
            - d["prix_unitaires_MAD"]["ressources"]["main_oeuvre_MAD_h"]["controleur"]["valeur"]) < 0.01
        and o["taux_horaire_de_cadre_MAD"]
        > d["prix_unitaires_MAD"]["ressources"]["main_oeuvre_MAD_h"]["compagnon"]["valeur"],
        f"{o['taux_horaire_de_cadre_MAD']} MAD/h")
verifie("le surcout en heures est la difference des deux scenarios",
        abs(o["surcout_en_heures_MAD"]
            - (o["heures_reconstitue"] - o["heures_au_fil_de_l_eau"])
            * o["taux_horaire_de_cadre_MAD"]) < 1)
verifie("le portage est montant x taux annuel x jours / 365",
        abs(o["cout_de_portage_MAD"]
            - o["montant_bloque_MAD"] * p["taux_de_portage_annuel_pct"] / 100
            * o["retard_du_solde_j"] / 365) < 1,
        f"{o['cout_de_portage_MAD']:.0f} MAD")
verifie("le montant bloque est celui du portage, et le module le declare borne basse",
        abs(o["montant_bloque_MAD"] - p["retenue_immobilisee_MAD"]) < 0.01
        and dit(o["_le_montant_bloque_est_une_borne_basse"],
                "solde des travaux", "superieur"))
verifie("le total est la somme des deux postes",
        abs(o["cout_total_du_retard_de_DOE_MAD"]
            - (o["surcout_en_heures_MAD"] + o["cout_de_portage_MAD"])) < 1)
verifie("les bornes du surcout encadrent sa valeur",
        o["surcout_bornes_MAD"][0] <= o["surcout_en_heures_MAD"] <= o["surcout_bornes_MAD"][1],
        f"{o['surcout_bornes_MAD']}")
verifie("le critere pratique du DOE ne cite aucun texte",
        "⏸" in o["_le_critere_pratique"] and dit(o["_le_critere_pratique"], "dix ans"))

# ------------------------------------------------- 5. les operations prealables
print("\n--- les operations prealables ---")
op = r["operations_prealables"]
verifie("la duree totale est la somme des etapes",
        op["duree_totale_j"] == sum(x["duree_j"] for x in op["etapes"]))
verifie("chaque etape nomme QUI la conduit et son piege",
        all(x["qui"] and len(x["piege"]) > 30 for x in op["etapes"]))
verifie("les fins cumulees sont croissantes et finissent sur la duree totale",
        [x["fin_j"] for x in op["etapes"]] == sorted(x["fin_j"] for x in op["etapes"])
        and op["etapes"][-1]["fin_j"] == op["duree_totale_j"],
        f"{op['duree_totale_j']} j")
_plus_long = max(op["etapes"], key=lambda x: x["duree_j"])
verifie("l'etape la plus longue est celle que l'entreprise ne maitrise pas",
        "exploitant" in _plus_long["qui"],
        f"{_plus_long['etape']} — {_plus_long['duree_j']} j")

# ------------------------------------------------- 6. la confrontation au planning
print("\n--- ce que le planning prevoit pour la reception ---")
pl = json.loads((RACINE / "calc" / "sorties" / "planification.json").read_text(encoding="utf-8"))
cf = r["confrontation_au_planning"]
verifie("la duree prevue est celle que D2 publie pour la tache RECE",
        abs(cf["duree_prevue_par_le_planning_j"] - pl["durees"]["RECE"]["duree_j"]) < 0.01,
        f"{cf['duree_prevue_par_le_planning_j']} j")
verifie("et celle des essais est celle de la tache ESSA",
        abs(cf["duree_des_essais_au_planning_j"] - pl["durees"]["ESSA"]["duree_j"]) < 0.01)
verifie("la mise en service n'est PAS comptee deux fois",
        abs(cf["duree_demandee_par_la_sequence_j"]
            - (op["duree_totale_j"]
               - next(x["duree_j"] for x in op["etapes"]
                      if "ise en service" in x["etape"]))) < 0.01,
        f"{op['duree_totale_j']} j de sequence moins la mise en service = "
        f"{cf['duree_demandee_par_la_sequence_j']} j")
verifie("l'ecart est la difference des deux",
        abs(cf["ecart_j"] - (cf["duree_demandee_par_la_sequence_j"]
                             - cf["duree_prevue_par_le_planning_j"])) < 0.01)
# Le decalage est MESURE : le test ne verifie pas qu'il vaut l'ecart — il verifie qu'il
# vient du reseau et qu'il n'est jamais SUPERIEUR a l'ecart, ce qu'aucune marge ne
# permettrait. Si une marge apparaissait un jour sur cette tache, le test resterait
# vrai et le chiffre changerait : c'est le but.
verifie("le decalage mesure ne depasse pas l'allongement applique",
        cf["decalage_mesure_de_la_fin_j"] <= max(0.0, cf["ecart_j"]) + 0.01,
        f"{cf['decalage_mesure_de_la_fin_j']} j pour {cf['ecart_j']} j d'allongement")
verifie("la duree de reference est celle que D2 publie",
        abs(cf["duree_de_reference_j"] - pl["calendrier"]["duree_ouvree_j"]) < 0.5,
        f"{cf['duree_de_reference_j']} j")
verifie("le cout de l'ecart est le decalage MESURE fois le cout d'un jour",
        abs(cf["cout_de_l_ecart_MAD"] - cf["decalage_mesure_de_la_fin_j"]
            * c["cout_avant_le_plafond_MAD_par_jour_ouvre"]) < 1,
        f"{cf['cout_de_l_ecart_MAD']:.0f} MAD")
verifie("le module declare que ce sont DEUX CHIFFRES DE CE COURS, pas une erreur reelle",
        dit(cf["_ce_que_cette_comparaison_est"], "deux chiffres de ce cours", "mecanisme"))

# ------------------------------------------------- figures
print("\n--- figures ---")
f = r["figures"]
verifie("la figure du cout porte exactement les points de la courbe",
        [x["v"] for x in f["cout_cumule"]] == [x["v"] for x in co["points"]])
verifie("la figure des reserves porte toutes les familles, et dit lesquelles bloquent",
        len(f["reserves"]) == len(s["lignes"])
        and sum("BLOQUANTE" in x["libelle"] for x in f["reserves"])
        == sum(1 for x in s["lignes"] if x["empeche_l_usage"]))
verifie("et les nombres de la figure sont ceux du tableau",
        [x["valeur"] for x in f["reserves"]] == [x["nombre"] for x in s["lignes"]])
verifie("la cascade du DOE se termine sur un total, et il recolle a ses etapes",
        f["doe"][-1].get("type") == "total"
        and abs(f["doe"][-1]["montant"]
                - sum(x["montant"] for x in f["doe"][:-1])) <= 1,
        f"{f['doe'][-1]['montant']} kMAD")

print()
if echecs:
    print(f"ECHEC : {len(echecs)} controle(s) — {', '.join(echecs)}")
    sys.exit(1)
print("Tests reception : tous verts.")
