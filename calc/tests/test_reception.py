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
        abs(c["cout_sous_penalites_MAD_par_jour_ouvre"]
            - (d1["frais_de_duree_MAD"] + d1["penalites_MAD"])) < 0.01,
        f"{c['cout_sous_penalites_MAD_par_jour_ouvre']:.0f} MAD")
verifie("cout apres le plafond = les frais de duree SEULS",
        abs(c["cout_hors_penalites_MAD_par_jour_ouvre"]
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
            abs(pente - c["cout_sous_penalites_MAD_par_jour_ouvre"])
            < 0.01 * c["cout_sous_penalites_MAD_par_jour_ouvre"],
            f"{pente:.0f} MAD/j contre "
            f"{c['cout_sous_penalites_MAD_par_jour_ouvre']:.0f}")
if len(_apres) >= 2:
    pente = (pts[_apres[-1]] - pts[_apres[-2]]) / (_apres[-1] - _apres[-2])
    verifie("et la pente apres ne vaut plus que les frais de duree",
            abs(pente - c["cout_hors_penalites_MAD_par_jour_ouvre"])
            < 0.01 * c["cout_hors_penalites_MAD_par_jour_ouvre"],
            f"{pente:.0f} MAD/j contre "
            f"{c['cout_hors_penalites_MAD_par_jour_ouvre']:.0f}")

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
        f"{s['heures_totales']:.0f} h-homme")
verifie("les bornes des heures encadrent la valeur",
        s["heures_bornes"][0] <= s["heures_totales"] <= s["heures_bornes"][1],
        f"{s['heures_bornes']}")
verifie("la capacite est l'effectif fois la journee de travail du cours",
        abs(s["capacite_h_homme_par_jour"] - s["effectif_de_levee"]
            * d["prix_unitaires_MAD"]["ressources"]["heures_par_jour"]) < 0.01,
        f"{s['capacite_h_homme_par_jour']} h-homme par jour")
# REGLE, et non conclusion : la duree d'un ensemble est le MAXIMUM des deux delais, pas
# leur somme et pas le seul temps d'atelier. Le test la verifie sur les deux ensembles
# publies, quels que soient les nombres.
for cle in ("levee_des_bloquantes", "levee_de_toutes"):
    x = s[cle]
    verifie(f"{cle} : la duree est le maximum de l'atelier et du delai de tiers",
            abs(x["duree_j"] - max(x["jours_d_atelier"],
                                   x["delai_de_tiers_le_plus_long_j"])) < 0.02,
            f"max({x['jours_d_atelier']} ; {x['delai_de_tiers_le_plus_long_j']}) = "
            f"{x['duree_j']} j")
    verifie(f"{cle} : le module nomme ce qui commande la duree",
            (x["commande_par"] == "l'atelier") ==
            (x["jours_d_atelier"] >= x["delai_de_tiers_le_plus_long_j"]),
            x["commande_par"])
verifie("lever TOUTES les reserves ne peut pas etre plus rapide que lever les bloquantes",
        s["levee_de_toutes"]["duree_j"] >= s["levee_des_bloquantes"]["duree_j"] - 0.01,
        f"{s['levee_de_toutes']['duree_j']} j contre "
        f"{s['levee_des_bloquantes']['duree_j']} j")
verifie("les jours en plus sont la difference des deux durees",
        abs(s["jours_de_non_reception_en_plus"]
            - (s["levee_de_toutes"]["duree_j"] - s["levee_des_bloquantes"]["duree_j"])) < 0.02,
        f"{s['jours_de_non_reception_en_plus']} j")
# canari qui CHERCHE : ignorer le delai de tiers — ce que faisait la premiere version —
# donnerait un cout plusieurs fois superieur.
_naif = (s["levee_de_toutes"]["jours_d_atelier"]
         - s["levee_des_bloquantes"]["jours_d_atelier"]) \
    * c["cout_sous_penalites_MAD_par_jour_ouvre"]
verifie("canari : ignorer le delai des tiers gonflerait le cout de la confusion",
        _naif > s["cout_de_la_confusion_sous_penalites_MAD"] * 1.5,
        f"{_naif:.0f} MAD contre "
        f"{s['cout_de_la_confusion_sous_penalites_MAD']:.0f} MAD mesures")
for regime, cle in (("sous_penalites", "cout_de_la_confusion_sous_penalites_MAD"),
                    ("hors_penalites", "cout_de_la_confusion_hors_penalites_MAD")):
    verifie(f"le cout de la confusion {regime} est les jours en plus fois le cout du jour",
            abs(s[cle] - s["jours_de_non_reception_en_plus"]
                * c[f"cout_{regime}_MAD_par_jour_ouvre"]) < 1,
            f"{s[cle]:.0f} MAD")
verifie("et le module publie les DEUX regimes, jamais un seul",
        s["cout_de_la_confusion_hors_penalites_MAD"]
        < s["cout_de_la_confusion_sous_penalites_MAD"],
        "un chantier dans son delai ne paie pas le prix fort")
verifie("les bornes du cout de la confusion encadrent les deux regimes",
        s["cout_de_la_confusion_bornes_MAD"][0]
        <= s["cout_de_la_confusion_hors_penalites_MAD"]
        and s["cout_de_la_confusion_sous_penalites_MAD"]
        <= s["cout_de_la_confusion_bornes_MAD"][1],
        f"{s['cout_de_la_confusion_bornes_MAD']}")
verifie("la regle de classement ne compte pas les reserves, elle les qualifie",
        dit(s["la_regle"], "empeche", "securite") and "nombre" in sansaccent(s["la_regle"]))
verifie("et elle dit QUI juge de l'usage",
        dit(s["la_regle"], "exploitant", "jugement"),
        "la securite ne se juge pas ; l'usage, si, et c'est l'exploitant")
verifie("le module traite aussi l'erreur SYMETRIQUE, la plus dangereuse",
        dit(s["_et_dans_l_autre_sens"], "garde-corps", "comptage"))

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
# REGLE, et c'est la correction d'un bloquant : chaque etape declare UNE tache qui la
# porte, et le besoin d'une tache est la somme des etapes qui la declarent. Le test ne
# verifie plus « 41 moins 15 » — il verifie qu'aucune etape n'est oubliee ni comptee
# deux fois, ce qui reste vrai si les durees changent.
_portees = [e for x in cf["lignes"] for e in x["etapes_portees"]]
verifie("aucune etape n'est portee par deux taches du planning",
        len(_portees) == len(set(_portees)),
        f"{len(_portees)} etapes reparties sur {len(cf['lignes'])} taches")
verifie("et toutes les etapes de la sequence sont portees par une tache",
        sorted(_portees) == sorted(x["etape"] for x in op["etapes"]),
        "aucune etape orpheline, aucune en trop")
for x in cf["lignes"]:
    verifie(f"{x['tache']} : la duree prevue est celle que D2 publie",
            abs(x["duree_prevue_j"] - pl["durees"][x["tache"]]["duree_j"]) < 0.01,
            f"{x['duree_prevue_j']} j")
    verifie(f"{x['tache']} : le besoin est la somme des etapes qu'elle porte",
            abs(x["besoin_j"] - sum(e["duree_j"] for e in op["etapes"]
                                    if e["porte_par"] == x["tache"])) < 0.01,
            f"{x['besoin_j']} j pour {len(x['etapes_portees'])} etape(s)")
    verifie(f"{x['tache']} : l'ecart est la difference des deux",
            abs(x["ecart_j"] - (x["besoin_j"] - x["duree_prevue_j"])) < 0.02)
    verifie(f"{x['tache']} : les bornes du besoin encadrent sa valeur",
            x["besoin_bornes_j"][0] <= x["besoin_j"] <= x["besoin_bornes_j"][1],
            f"{x['besoin_bornes_j']}")
# canari qui CHERCHE : retirer la seule etape « mise en service » — ce que faisait la
# premiere version — laisserait les essais de fonctionnement comptes comme absents d'une
# tache qui les nomme, et donnerait un ecart different.
_naif = op["duree_totale_j"] - next(x["duree_j"] for x in op["etapes"]
                                    if "ise en service" in x["etape"]) \
    - pl["durees"]["RECE"]["duree_j"]
verifie("canari : l'ancienne lecture attribuait tout l'ecart a la mauvaise tache",
        abs(_naif - next(x["ecart_j"] for x in cf["lignes"] if x["tache"] == "RECE")) > 1,
        f"ancienne lecture {_naif:.0f} j sur RECE seule, contre "
        + " et ".join(f"{x['ecart_j']:.0f} j sur {x['tache']}" for x in cf["lignes"]))
verifie("l'ecart total est la somme des ecarts par tache",
        abs(cf["ecart_total_j"] - sum(x["ecart_j"] for x in cf["lignes"])) < 0.02,
        f"{cf['ecart_total_j']} j")
# Le decalage est MESURE : le test verifie qu'il vient du reseau et qu'il ne depasse
# jamais la somme des allongements, ce qu'aucune marge ne permettrait.
verifie("le decalage mesure ne depasse pas la somme des allongements",
        cf["decalage_mesure_de_la_fin_j"]
        <= sum(max(0.0, x["ecart_j"]) for x in cf["lignes"]) + 0.01,
        f"{cf['decalage_mesure_de_la_fin_j']} j")
verifie("ses bornes sont mesurees elles aussi, et elles l'encadrent",
        cf["decalage_bornes_j"][0] <= cf["decalage_mesure_de_la_fin_j"]
        <= cf["decalage_bornes_j"][1],
        f"{cf['decalage_bornes_j']}")
verifie("la duree de reference est celle que D2 publie",
        abs(cf["duree_de_reference_j"] - pl["calendrier"]["duree_ouvree_j"]) < 0.5,
        f"{cf['duree_de_reference_j']} j")
for regime in ("hors_penalites", "sous_penalites"):
    verifie(f"le cout {regime} est le decalage MESURE fois le cout d'un jour",
            abs(cf[f"cout_{regime}_MAD"] - cf["decalage_mesure_de_la_fin_j"]
                * c[f"cout_{regime}_MAD_par_jour_ouvre"]) < 1,
            f"{cf[f'cout_{regime}_MAD']:.0f} MAD")
verifie("le module declare que ce sont DEUX CHIFFRES DE CE COURS, pas une erreur reelle",
        dit(cf["_ce_que_cette_comparaison_est"], "deux chiffres de ce cours", "mecanisme"))
verifie("et il raconte le double compte qu'il a corrige",
        dit(cf["_le_double_compte_evite"], "essais et mise en service", "attribution"))

# ------------------------------------------------- figures
print("\n--- figures ---")
f = r["figures"]
verifie("la figure du cout porte exactement les points de la courbe",
        [x["v"] for x in f["cout_cumule"]] == [x["v"] for x in co["points"]])
verifie("la figure des reserves porte toutes les familles",
        len(f["reserves"]) == len(s["lignes"]))
# La qualification doit etre dans la FORME de la figure, pas dans son libelle : un mot
# ajoute se lit apres la longueur de la barre, et la figure enseignait alors l'inverse
# de sa legende.
verifie("et les bloquantes y sont marquees par une ALERTE, pas par un mot",
        [bool(x.get("alerte")) for x in f["reserves"]]
        == [x["empeche_l_usage"] for x in s["lignes"]]
        and not any("BLOQUANTE" in x["libelle"] for x in f["reserves"]),
        f"{sum(1 for x in f['reserves'] if x.get('alerte'))} famille(s) en alerte")
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
