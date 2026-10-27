"""Tests du module C7 — qualite, HSE, environnement."""
from __future__ import annotations
import json, math, re, sys, pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))

echecs = []


def verifie(nom, condition, detail=""):
    if not condition:
        echecs.append(nom)
    print(f"  {'ok   ' if condition else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
r = json.loads((RACINE / "calc" / "sorties" / "qualite.json").read_text(encoding="utf-8"))
pl = json.loads((RACINE / "calc" / "sorties" / "planification.json").read_text(encoding="utf-8"))
pr = json.loads((RACINE / "calc" / "sorties" / "prix.json").read_text(encoding="utf-8"))
Q = d["qualite_hse"]

# ------------------------------------------------- 1. l'exposition, en heures
print("\n--- l'exposition se compte en heures ---")
e = r["exposition"]
h = pl["heures_de_main_oeuvre_par_tache"]
verifie("les heures totales sont celles que publie D2",
        abs(e["heures_totales"] - sum(h.values())) < 0.5,
        f"{e['heures_totales']:.0f} h")
nuit = set(d["planning"]["contraintes_exploitation"]["taches_soumises"])
verifie("les heures de nuit sont exactement celles des taches soumises",
        abs(e["heures_de_nuit"] - sum(v for i, v in h.items() if i in nuit)) < 0.5,
        f"{e['heures_de_nuit']:.0f} h sur {sorted(nuit)}")
verifie("jour + nuit = total",
        abs(e["heures_de_jour"] + e["heures_de_nuit"] - e["heures_totales"]) < 0.5)
k = Q["exposition"]["surexposition_du_travail_de_nuit"]["valeur"]
verifie("les heures ponderees appliquent le coefficient a la SEULE part de nuit",
        abs(e["heures_ponderees_par_le_risque"]
            - (e["heures_de_jour"] + k * e["heures_de_nuit"])) < 0.5)
verifie("la nuit pese plus dans le RISQUE que dans les heures",
        e["part_de_nuit_dans_le_risque_pct"] > e["part_de_nuit_pct"],
        f"{e['part_de_nuit_dans_le_risque_pct']} % du risque pour "
        f"{e['part_de_nuit_pct']} % des heures")
verifie("et le rapport entre les deux parts est le coefficient, a la ponderation pres",
        abs(e["part_de_nuit_dans_le_risque_pct"] / e["part_de_nuit_pct"]
            - k * e["heures_totales"] / e["heures_ponderees_par_le_risque"]) < 0.02)
tf = Q["exposition"]["taux_de_frequence_reference"]["valeur"]
verifie("le nombre d'accidents attendus est le taux applique aux heures ponderees",
        abs(e["accidents_avec_arret_attendus"]
            - tf * e["heures_ponderees_par_le_risque"] / 1e6) < 0.02,
        f"{e['accidents_avec_arret_attendus']} pour TF = {tf}")
verifie("le module dit que ce n'est ni une prevision ni un objectif",
        "prevision" in e["_ce_que_le_nombre_d_accidents_n_est_pas"]
        and "objectif" in e["_ce_que_le_nombre_d_accidents_n_est_pas"])
# Les heures ne se deduisent pas des durees : un classement par duree n'est pas un
# classement par exposition. On compare les deux classements entiers.
_par_h = [x["tache"] for x in e["par_tache"]]
_par_d = sorted(_par_h, key=lambda i: -pl["durees"][i]["duree_j"])
verifie("canari : classer par DUREE donnerait un autre ordre que classer par heures",
        _par_h != _par_d,
        f"1er par heures {_par_h[0]}, 1er par duree {_par_d[0]} ; "
        f"{sum(1 for a, b in zip(_par_h, _par_d) if a != b)} rangs differents")
verifie("les parts de risque somment a 100 %",
        abs(sum(x["part_du_risque_pct"] for x in e["par_tache"]) - 100) < 1.0)

# ------------------------------------------------- 2. le cout d'une non-conformite
print("\n--- le cout d'une non-conformite ---")
n = r["non_conformite"]
v = {k_: Q["non_conformite"][k_]["valeur"] for k_ in Q["non_conformite"]
     if isinstance(Q["non_conformite"][k_], dict) and "valeur" in Q["non_conformite"][k_]}
verifie("la reprise est surface x prix au m2",
        abs(n["lignes"][0]["montant_MAD"]
            - v["surface_m2"] * v["cout_de_reprise_MAD_m2"]) < 1)
fd = pr["bordereau"]["frais_de_duree"]["cout_MAD_par_jour_ouvre"]
verifie("les frais de duree sont LUS chez D1, pas re-derives",
        abs(n["frais_de_duree_MAD_par_jour_ouvre"] - fd) < 0.01,
        f"{fd:.2f} MAD/j")
verifie("l'attente de decision et la reprise sont chiffrees au meme taux journalier",
        abs(n["lignes"][1]["montant_MAD"] - v["delai_de_decision_j"] * fd) < 1
        and abs(n["lignes"][2]["montant_MAD"] - v["duree_de_reprise_j"] * fd) < 1)
verifie("le durcissement porte sur les levees RESTANTES, pas sur celle qui a defailli",
        abs(n["lignes"][3]["montant_MAD"]
            - v["heures_de_controle_par_levee"] * v["durcissement_du_controle_pct"] / 100
            * v["levees_restantes"]
            * d["prix_unitaires_MAD"]["postes"]["main_oeuvre_h"]["valeur"]) < 1)
verifie("le total est la somme des quatre lignes",
        abs(n["total_MAD"] - sum(x["montant_MAD"] for x in n["lignes"])) < 1,
        f"{n['total_MAD']:.0f} MAD")
verifie("la part visible sur un devis est MINORITAIRE",
        n["part_visible_pct"] < 50,
        f"{n['part_visible_pct']} % — le reste est du temps, et il n'a pas de facture")
verifie("canari : ne chiffrer que la reprise sous-estimerait d'un facteur notable",
        n["total_MAD"] / n["part_visible_sur_un_devis_MAD"] > 2,
        f"x{n['total_MAD'] / n['part_visible_sur_un_devis_MAD']:.1f}")
verifie("le module declare ce qu'il ne chiffre PAS",
        "borne basse" in n["ce_qui_n_est_PAS_chiffre_ici"])

# ------------------------------------------------- 3. l'impact planning, MESURE
print("\n--- l'impact sur le planning, mesure en rejouant le reseau ---")
ip = r["impact_planning"]
verifie("la duree de reference est celle que D2 publie",
        abs(ip["duree_de_reference_j"] - pl["calendrier"]["duree_ouvree_j"]) < 0.5,
        f"{ip['duree_de_reference_j']} j")
verifie("les taches comparees couvrent au moins deux regimes de marge",
        len({round(x["marge_totale_j"], 1) for x in ip["lignes"]}) >= 2,
        " / ".join(f"{x['tache']} {x['marge_totale_j']:.1f} j" for x in ip["lignes"]))
verifie("et elles donnent des retards de chantier differents",
        len({x["retard_du_chantier_j"] for x in ip["lignes"]}) == len(ip["lignes"]),
        " / ".join(f"{x['tache']} {x['retard_du_chantier_j']:.1f} j"
                   for x in ip["lignes"]))
verifie("« absorbee par la marge » si et seulement si le retard est nul",
        all(x["absorbee_par_la_marge"] == (x["retard_du_chantier_j"] < 0.01)
            for x in ip["lignes"]))
verifie("une tache a marge nulle transmet son immobilisation, une tache a marge non",
        ip["lignes"][0]["retard_du_chantier_j"] > ip["lignes"][-1]["retard_du_chantier_j"],
        f"{ip['lignes'][0]['tache']} {ip['lignes'][0]['retard_du_chantier_j']} j contre "
        f"{ip['lignes'][-1]['tache']} {ip['lignes'][-1]['retard_du_chantier_j']} j")
# Le resultat non evident : sous consignation, le retard est AMPLIFIE par les fenetres.
_sous_cons = [x for x in ip["lignes"] if x["tache"] in nuit]
if _sous_cons:
    x = _sous_cons[0]
    verifie("sous consignation, le retard est AMPLIFIE : on rate la fenetre suivante",
            x["retard_du_chantier_j"] > ip["immobilisation_j"] * 1.5,
            f"{ip['immobilisation_j']:.0f} j d'immobilisation -> "
            f"{x['retard_du_chantier_j']:.0f} j de chantier, soit "
            f"x{x['retard_du_chantier_j'] / ip['immobilisation_j']:.1f}")
verifie("canari : supposer le retard egal a l'immobilisation serait faux dans les deux sens",
        any(x["retard_du_chantier_j"] > ip["immobilisation_j"] + 0.5 for x in ip["lignes"])
        and any(x["retard_du_chantier_j"] < ip["immobilisation_j"] - 0.5
                for x in ip["lignes"]),
        "une tache amplifie, une autre absorbe : la regle de trois se trompe des deux cotes")

# ------------------------------------------------- 4. la criticite et son domaine
print("\n--- la criticite : un classement, pas une grandeur ---")
c = r["criticite"]
for x in c["lignes"]:
    verifie(f"{x['risque'][:34]} : criticite = f x g x d",
            x["criticite"] == x["f"] * x["g"] * x["d"],
            f"{x['f']}x{x['g']}x{x['d']} = {x['criticite']}")
verifie("les rangs sont consecutifs et suivent la criticite decroissante",
        [x["rang"] for x in c["lignes"]] == list(range(1, len(c["lignes"]) + 1))
        and all(c["lignes"][i]["criticite"] >= c["lignes"][i + 1]["criticite"]
                for i in range(len(c["lignes"]) - 1)))
verifie("chaque risque porte une parade, et elle est concrete",
        all(len(x["parade"]) > 30 for x in c["lignes"]))
verifie("le module dit que la criticite ne se moyenne ni ne se compare en pourcentage",
        "moyenne" in c["_ce_que_la_criticite_n_est_pas"]
        and "%" in c["_ce_que_la_criticite_n_est_pas"])
verifie("le module dit que le seuil est arbitraire et se decide",
        "arbitraire" in c["_le_seuil_est_arbitraire"].lower()
        or "depend entierement" in c["_le_seuil_est_arbitraire"])
verifie("les deux classements — criticite et gravite — sont publies tous les deux",
        len(c["les_trois_premiers"]) == 3 and len(c["les_trois_plus_graves"]) == 3)
# Les deux classements peuvent coincider ou non : ce que le test exige, c'est que le
# module DISE dans quel cas on se trouve, et que sa liste de desaccords soit juste.
_desac = [x for x in c["les_trois_premiers"] if x not in c["les_trois_plus_graves"]]
verifie("la liste des desaccords entre les deux classements est exacte",
        sorted(c["classements_en_desaccord"]) == sorted(_desac),
        f"{len(_desac)} desaccord(s) sur le trio de tete")
verifie("et le module dit dans quel cas on se trouve",
        ("sort du trio" in c["pourquoi_lire_aussi_la_gravite_seule"]) == bool(_desac),
        "s'accordent" if not _desac else "en desaccord")
verifie("canari : classer par gravite seule donne un ordre different du produit",
        [x["risque"] for x in c["lignes"]]
        != sorted((x["risque"] for x in c["lignes"]),
                  key=lambda n_: -next(y["g"] for y in c["lignes"] if y["risque"] == n_)),
        "les deux lectures ne sont pas interchangeables")

# ------------------------------------------------- 5. le plan de controle
print("\n--- le plan de controle ---")
p = r["plan_de_controle"]
verifie("cinq colonnes sont exigees de chaque ligne", len(p["les_cinq_colonnes"]) == 5)
for x in p["lignes"]:
    for col in ("qui", "quand", "critere", "si_non_conforme"):
        verifie(f"{x['controle'][:28]} : la colonne « {col} » est remplie",
                bool(str(x[col]).strip()))
verifie("au moins un controle rend son resultat APRES coup",
        p["nb_differes"] >= 1,
        f"{p['controle_le_plus_differe']} a {p['delai_le_plus_long_j']} j")
verifie("et le module dit que celui-la ne protege pas l'ouvrage qu'il mesure",
        "SUIVANTS" in p["controles_qui_ne_protegent_pas_leur_ouvrage"])
verifie("immediats + differes = total",
        p["nb_immediats"] + p["nb_differes"] == p["nb_controles"])
# Un critere ne doit pas poser de SEUIL CHIFFRE : il renvoie au marche, au plan vise
# ou a un aspect de reference. Un identifiant de module (« B3e ») n'est pas un seuil.
_seuil = re.compile(r"\d+(?:[.,]\d+)?\s*(?:MPa|mm|cm|m|%|kg|j|jours?)\b")
_fautifs = [x["controle"] for x in p["lignes"] if _seuil.search(x["critere"])]
verifie("la phase § 5.0 est tenue : aucun critere ne pose de seuil chiffre",
        not _fautifs, "; ".join(_fautifs) or
        "les criteres renvoient au marche ou au plan vise, ils ne les remplacent pas")
verifie("et chaque critere renvoie a un document ou porte la marque ⏸",
        all("⏸" in x["critere"] or any(mot in x["critere"].lower() for mot in
            ("marche", "plan", "commande", "reference", "tolerance"))
            for x in p["lignes"]))

# ------------------------------------------------- 6. les dechets
print("\n--- les dechets ---")
de = r["dechets"]
verifie("l'emprise est celle de la geometrie du projet",
        abs(de["emprise_m2"] - d["geometrie"]["emprise_m"][0]
            * d["geometrie"]["emprise_m"][1]) < 1)
for x in de["lignes"]:
    verifie(f"{x['flux'][:30]} : tonnage = ratio x emprise",
            abs(x["tonnes"] - x["kg_m2"] * de["emprise_m2"] / 1000) < 0.2)
    verifie(f"{x['flux'][:30]} : valorise = tonnage x taux",
            abs(x["tonnes_valorisees"] - x["tonnes"] * x["valorisation_pct"] / 100) < 0.2)
verifie("le total est la somme des flux",
        abs(de["total_tonnes"] - sum(x["tonnes"] for x in de["lignes"])) < 0.2,
        f"{de['total_tonnes']} t")
verifie("les dechets dangereux pesent peu",
        de["part_dangereuse_pct"] < 1.0, f"{de['part_dangereuse_pct']} %")
verifie("et le module dit qu'ils commandent tout le reste",
        "benne" in de["_dangereux"] or "filiere" in de["_dangereux"])

# ------------------------------------------------- figures
print("\n--- figures ---")
f = r["figures"]
verifie("la figure d'exposition porte des heures, pas des durees",
        all(any(abs(x["valeur"] - v_) < 0.5 for v_ in h.values()) for x in f["exposition"]))
verifie("la cascade du cout part de la reprise et arrive au cout reel",
        abs(f["cout_nc"][0]["montant"] - n["lignes"][0]["montant_MAD"]) < 1
        and abs(f["cout_nc"][-1]["montant"] - n["total_MAD"]) < 1)
verifie("la figure de criticite porte exactement les criticites publiees",
        [x["valeur"] for x in f["criticite"]] == [x["criticite"] for x in c["lignes"]])
verifie("la figure des dechets totalise le tonnage publie",
        abs(sum(x["valeur"] for x in f["dechets"]) - de["total_tonnes"]) < 0.3)

print()
if echecs:
    print(f"ECHEC : {len(echecs)} controle(s) — {', '.join(echecs)}")
    sys.exit(1)
print("Tests qualite : tous verts.")
