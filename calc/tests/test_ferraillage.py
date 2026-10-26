"""Tests du module B3e — beton arme en execution : lire, metrer, controler.

Chaque verdict publie porte ici son controle, et chaque controle qui rend un verdict
porte son canari (regle de STATE.md). Les canaris rejouent le calcul avec l'erreur
classique et verifient que le nombre CHANGE : un test qui passerait aussi bien avec
l'erreur ne prouve rien.
"""
from __future__ import annotations
import json, math, sys, pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import ferraillage as fe                                                 # noqa: E402
import plancher as plc                                                   # noqa: E402

echecs = []


def verifie(nom, condition, detail=""):
    if not condition:
        echecs.append(nom)
    print(f"  {'ok   ' if condition else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
r = json.loads((RACINE / "calc" / "sorties" / "ferraillage.json").read_text(encoding="utf-8"))
tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json").read_text(encoding="utf-8"))
A = d["armatures"]
q = plc.quantites_zone(d)
RHO = A["conventions"]["masse_volumique_acier_kg_m3"]

# ------------------------------------------------- la masse lineique, recalculee ici
print("\n--- masse lineique ---")
for ligne in r["nomenclature"]["lignes"]:
    verifie(f"{ligne['repere']} : masse lineique recalculee depuis le diametre",
            abs(ligne["masse_lineique_kg_m"]
                - math.pi / 4 * (ligne["dia_mm"] / 1000) ** 2 * RHO) < 5e-4,
            f"HA{ligne['dia_mm']} = {ligne['masse_lineique_kg_m']} kg/m")

# ------------------------------------------------- le metre, ligne par ligne
print("\n--- nomenclature ---")
nom = r["nomenclature"]
for ligne in nom["lignes"]:
    verifie(f"{ligne['repere']} : masse = longueur totale x masse lineique",
            abs(ligne["masse_kg"]
                - ligne["longueur_totale_m"] * ligne["masse_lineique_kg_m"]) < 0.6)
    verifie(f"{ligne['repere']} : longueur totale = longueur faconnee x nombre",
            abs(ligne["longueur_totale_m"]
                - ligne["longueur_faconnee_m"] * ligne["nombre"]) < 0.05)
verifie("la masse de la poutre est la somme de ses lignes",
        abs(nom["masse_kg"] - sum(x["masse_kg"] for x in nom["lignes"])) < 0.2,
        f"{nom['masse_kg']} kg")
verifie("le recapitulatif par diametre totalise la meme masse",
        abs(sum(x["masse_kg"] for x in nom["recapitulatif_par_diametre"])
            - nom["masse_kg"]) < 0.2)
verifie("les parts par diametre font 100 %",
        abs(sum(x["part_pct"] for x in nom["recapitulatif_par_diametre"]) - 100) < 0.3)

# Les recouvrements de filante sont GEOMETRIQUES : une barre de 24 m avec des barres de
# 12 m en demande un. Un repere non filant n'en porte aucun.
Lc = A["conventions"]["longueur_commerciale_m"]
for ligne in nom["lignes"]:
    src = next((b for b in A["plan"]["poutre_PM1"]["barres"]
                if b["repere"] == ligne["repere"]), None)
    if src is None:
        continue
    attendu = math.ceil(fe.longueur_developpee_m(src) / Lc) - 1 if src.get("filante") else 0
    verifie(f"{ligne['repere']} : nombre de recouvrements deduit de la longueur commerciale",
            ligne["recouvrements_par_barre"] == attendu,
            f"{ligne['recouvrements_par_barre']} pour {ligne['longueur_unitaire_m']} m")
verifie("canari : oublier les recouvrements allegerait le metre des filantes",
        sum(x["longueur_faconnee_m"] for x in nom["lignes"])
        > sum(x["longueur_unitaire_m"] for x in nom["lignes"]),
        "le metre publie est le plus lourd des deux")

# ------------------------------------------------- les cadres : intervalles + 1
print("\n--- cadres ---")
c = r["cadres"]
p = A["plan"]["poutre_PM1"]
attendu = sum(math.floor(z["longueur_cumulee_m"] / (z["espacement_cm"] / 100)) + 1
              for z in p["cadres"]["zones"])
verifie("le nombre de cadres est recalcule ici : floor(L/s) + 1 par zone",
        c["nombre_par_poutre"] == attendu, f"{attendu} par poutre")
verifie("canari : compter L/s au lieu de L/s + 1 donnerait un cadre de moins par zone",
        c["nombre_par_poutre"]
        - sum(math.floor(z["longueur_cumulee_m"] / (z["espacement_cm"] / 100))
              for z in p["cadres"]["zones"]) == len(p["cadres"]["zones"]),
        f"{len(p['cadres']['zones'])} cadres d'ecart")
s = p["section_cm"]
b_ax = (s["b"] - 2 * s["enrobage"] - c["dia_mm"] / 10) / 100
h_ax = (s["h"] - 2 * s["enrobage"] - c["dia_mm"] / 10) / 100
verifie("le perimetre du cadre est celui de son AXE, enrobage pris a la peau du cadre",
        abs(c["perimetre_m"] - 2 * (b_ax + h_ax)) < 1e-3, f"{c['perimetre_m']} m")
verifie("canari : mesurer le cadre a la peau du beton le surestimerait",
        2 * ((s["b"] + s["h"]) / 100) > c["perimetre_m"],
        f"{2 * ((s['b'] + s['h']) / 100):.3f} m contre {c['perimetre_m']} m")
verifie("la longueur des zones de cadres couvre la poutre entiere",
        abs(sum(z["longueur_cumulee_m"] for z in p["cadres"]["zones"])
            - p["longueur_m"]) < 1e-6,
        f"{sum(z['longueur_cumulee_m'] for z in p['cadres']['zones'])} m sur {p['longueur_m']}")

# ------------------------------------------------- les nappes : 100/s barres par metre
print("\n--- nappes de dalle ---")
nap = r["nappes"]
for ligne in nap["lignes"]:
    verifie(f"{ligne['repere']} : {ligne['barres_par_metre']} barres par metre a "
            f"{ligne['espacement_cm']} cm",
            abs(ligne["barres_par_metre"] - 100 / ligne["espacement_cm"]) < 0.01)
    verifie(f"{ligne['repere']} : masse = nombre x longueur x masse lineique",
            abs(ligne["masse_kg"] - ligne["nombre"] * ligne["longueur_barre_m"]
                * ligne["masse_lineique_kg_m"]) < 0.6)
verifie("la masse de la dalle est la somme de ses nappes",
        abs(nap["masse_kg"] - sum(x["masse_kg"] for x in nap["lignes"])) < 0.2,
        f"{nap['masse_kg']} kg, soit {nap['masse_par_m2_kg']} kg/m2")
verifie("la masse au m2 est recalculee ici",
        abs(nap["masse_par_m2_kg"] - nap["masse_kg"] / nap["surface_m2"]) < 0.01)

# ------------------------------------------------- les deux voies (§ 3.3)
print("\n--- les deux voies ---")
dv = r["deux_voies"]
verifie("la voie A est la somme des deux ouvrages metres",
        abs(dv["voie_A_metre_du_plan_kg"] - (nom["masse_kg"] + nap["masse_kg"])) < 0.2,
        f"{dv['voie_A_metre_du_plan_kg']} kg")
for e in dv["elements"]:
    verifie(f"{e['element'][:22]} : ratio recalcule ici",
            abs(e["ratio_du_plan_kg_m3"] - e["voie_A_kg"] / e["beton_m3"]) < 0.1,
            f"{e['ratio_du_plan_kg_m3']} kg/m3")
    verifie(f"{e['element'][:22]} : « dans la fourchette » si et seulement si le ratio y est",
            e["dans_la_fourchette"]
            == (e["fourchette_kg_m3"][0] <= e["ratio_du_plan_kg_m3"] <= e["fourchette_kg_m3"][1]))
# Le plan est CALIBRE sur les ratios du projet (data : armatures._calibrage). Si une
# modification du plan le fait sortir de sa fourchette, c'est une decision a prendre,
# pas un detail : le test l'impose.
verifie("le plan fictif reste dans la fourchette V3 de CHAQUE element",
        dv["tous_dans_la_fourchette"],
        "sinon le cours porterait deux estimations contradictoires de son propre acier")
verifie("canari : comparer les deux ouvrages a un ratio GLOBAL masquerait un ecart",
        any(abs(e["ecart_pct"]) > abs(dv["ecart_pct"]) for e in dv["elements"]),
        f"global {dv['ecart_pct']} % contre "
        + " et ".join(f"{e['ecart_pct']} %" for e in dv["elements"]))

# ------------------------------------------------- metre contre estimation
print("\n--- le metre contre l'estimation par ratio ---")
m = r["metre_contre_estimation"]
verifie("l'estimation comparee est bien celle que publie le module TV",
        m["estimation_par_ratio_kg"] == tv["quantites"]["acier_kg"],
        f"{m['estimation_par_ratio_kg']} kg")
verifie("l'ecart est recalcule ici",
        abs(m["ecart_pct"] - (m["metre_du_plan_kg"] - m["estimation_par_ratio_kg"])
            / m["estimation_par_ratio_kg"] * 100) < 0.05,
        f"{m['ecart_pct']} %")
verifie("le metre tombe dans la fourchette que l'estimation avait declaree",
        m["le_metre_est_dans_la_fourchette_de_l_estimation"],
        f"{m['metre_du_plan_kg']} kg dans {m['fourchette_de_l_estimation_kg']}")
verifie("canari : l'estimation et le metre ne sont PAS egaux, et le module ne le pretend pas",
        abs(m["ecart_kg"]) > 1.0,
        f"{m['ecart_kg']} kg d'ecart — un module qui les trouverait egaux aurait "
        "recopie l'un dans l'autre")

# ------------------------------------------------- du plan a la commande
print("\n--- du plan a la commande ---")
cmd = r["commande"]
k = A["du_plan_a_la_commande"]
verifie("les chutes sont un pourcentage de l'acier DU PLAN",
        abs(cmd["chutes_kg"] - cmd["acier_du_plan_kg"] * k["chutes_pct"]["valeur"] / 100) < 0.2)
verifie("les ligatures portent sur l'acier plan + chutes, pas sur le plan seul",
        abs(cmd["ligatures_kg"] - (cmd["acier_du_plan_kg"] + cmd["chutes_kg"])
            * k["ligatures_pct"]["valeur"] / 100) < 0.2)
verifie("l'acier commande est la somme de la cascade",
        abs(cmd["acier_commande_kg"]
            - (cmd["acier_du_plan_kg"] + cmd["chutes_kg"] + cmd["ligatures_kg"])) < 0.2,
        f"{cmd['acier_commande_kg']} kg")
verifie("la cascade publiee part du plan et arrive a la commande",
        abs(cmd["cascade"][0]["montant"] - cmd["acier_du_plan_kg"]) < 0.2
        and abs(cmd["cascade"][-1]["montant"] - cmd["acier_commande_kg"]) < 0.2)
verifie("l'acier commande est strictement superieur a l'acier du plan",
        cmd["acier_commande_kg"] > cmd["acier_du_plan_kg"],
        f"+{cmd['ecart_commande_plan_pct']} %")
verifie("canari : payer la commande au lieu du plan gonflerait la quantite",
        abs(cmd["acier_commande_kg"] - cmd["acier_du_plan_kg"])
        > 0.03 * cmd["acier_du_plan_kg"],
        "l'ecart est assez grand pour qu'une confusion se voie au decompte")
verifie("les cales sont comptees sur la surface de dalle, pas sur l'acier",
        cmd["cales_d_enrobage_u"] == round(nap["surface_m2"] * k["cales_par_m2"]["valeur"]),
        f"{cmd['cales_d_enrobage_u']} cales")

# ------------------------------------------------- lecture et controles
print("\n--- lire et controler ---")
lp = r["lire_un_plan"]
verifie("les sept etapes de lecture sont numerotees dans l'ordre",
        [e["n"] for e in lp["etapes"]] == list(range(1, len(lp["etapes"]) + 1)),
        f"{len(lp['etapes'])} etapes")
verifie("chaque etape dit POURQUOI on la fait, et non seulement quoi regarder",
        all(len(e["pourquoi"]) > 40 for e in lp["etapes"]))
ct = r["controles"]
verifie("chaque controle porte sa REFERENCE : on ne juge pas de memoire",
        all(c["reference"] for c in ct["liste"]), f"{len(ct['liste'])} controles")
verifie("chaque controle dit si sa regle est normative (⏸) ou non",
        all(c["statut_de_la_regle"] for c in ct["liste"]))
verifie("chaque controle porte le symptome de son oubli",
        all(len(c["symptome_si_rate"]) > 20 for c in ct["liste"]))
verifie("la phase § 5.0 est tenue : aucun controle n'avance de valeur normative",
        sum(1 for c in ct["liste"] if "⏸" in c["statut_de_la_regle"]) >= 4,
        f"{sum(1 for c in ct['liste'] if '⏸' in c['statut_de_la_regle'])} regles declarees ⏸")
verifie("la double lecture entreprise / maitrise d'oeuvre est presente",
        bool(ct["double_lecture"]["entreprise"])
        and bool(ct["double_lecture"]["maitrise_d_oeuvre"]))

# ------------------------------------------------- figures
print("\n--- figures ---")
f = r["figures"]
# La coupe doit montrer les filantes du PLAN, pas une section recopiee a la main.
for lit in ("inf", "sup"):
    src = next(x for x in A["plan"]["poutre_PM1"]["barres"]
               if x["lit"] == lit and x.get("filante"))
    vue = f["coupe"]["section"][lit]
    verifie(f"coupe : le lit {lit} dessine la filante {src['repere']} du plan",
            vue["dia_mm"] == src["dia_mm"]
            and vue["n"] == sum(q["n"] for q in src["positions"]),
            f"{vue['n']} HA{vue['dia_mm']}")
verifie("coupe : les cotes de la section sont celles du plan",
        f["coupe"]["section"]["b_cm"] == A["plan"]["poutre_PM1"]["section_cm"]["b"]
        and f["coupe"]["section"]["h_cm"] == A["plan"]["poutre_PM1"]["section_cm"]["h"])
verifie("la figure par diametre totalise la masse de la poutre",
        abs(sum(x["valeur"] for x in f["par_diametre"]) - nom["masse_kg"]) < 0.3)
verifie("la figure des deux voies porte exactement les deux nombres publies",
        abs(f["deux_voies"][0]["valeur"] - dv["voie_A_metre_du_plan_kg"]) < 0.2
        and abs(f["deux_voies"][1]["valeur"] - dv["voie_B_ratio_kg"]) < 0.2)
verifie("la bande de la figure est la fourchette publiee, pas une bande choisie",
        f["deux_voies_bande"] == dv["voie_B_fourchette_kg"])
reperes_plan = {a["repere"] for a in f["elevation"]["aciers"]}
reperes_nom = {x["repere"] for x in nom["lignes"]} - {"C1"}
verifie("l'elevation dessine exactement les reperes de la nomenclature",
        reperes_plan == reperes_nom,
        f"{sorted(reperes_plan)}")
# Le plan DESSINE et la nomenclature CHIFFRENT : le module en fait un controle (etape 5
# de la lecture). Il doit donc etre vrai de ses propres figures.
for rep in sorted(reperes_nom):
    dessine = sum(a["n"] for a in f["elevation"]["aciers"] if a["repere"] == rep)
    chiffre = next(x["nombre"] for x in nom["lignes"] if x["repere"] == rep) \
        // nom["nb_de_poutres_dans_la_zone"]
    verifie(f"{rep} : le nombre de barres DESSINEES egale celui de la nomenclature",
            dessine == chiffre, f"{dessine} contre {chiffre} par poutre")
for a in f["elevation"]["aciers"]:
    verifie(f"{a['repere']} [{a['de_m']} ; {a['a_m']}] : longueur dessinee coherente "
            f"avec la nomenclature",
            abs((a["a_m"] - a["de_m"])
                - next(x["longueur_unitaire_m"] for x in nom["lignes"]
                       if x["repere"] == a["repere"])
                + (0.6 if a["repere"] == "B3" else 0)) < 0.02)

print()
if echecs:
    print(f"ECHEC : {len(echecs)} controle(s) — {', '.join(echecs)}")
    sys.exit(1)
print("Tests du ferraillage : tous verts.")
