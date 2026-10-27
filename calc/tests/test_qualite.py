"""Tests du module C7 — qualite, HSE, environnement."""
from __future__ import annotations
import json, math, re, sys, pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))

echecs = []


def sansaccent(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", str(s).lower())
                   if unicodedata.category(c) != "Mn")


def dit(texte, *mots):
    """Le texte publie contient ces mots, accents et casse mis de cote."""
    t_ = sansaccent(texte)
    return all(sansaccent(m) in t_ for m in mots)


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
# INVARIANT central : la ponderation REPARTIT le risque, elle ne l'ajoute pas. Un taux
# de branche est mesure sur des heures reelles qui contiennent deja du travail de nuit ;
# l'appliquer a des heures ponderees le compterait deux fois.
import copy as _copy, importlib as _il, sys as _sys
_sys.path.insert(0, str(RACINE / "calc"))
_qa = _il.import_module("qualite")
_tot = {}
for _k in (1.0, k, 3.0):
    _dd = _copy.deepcopy(d)
    _dd["qualite_hse"]["exposition"]["surexposition_du_travail_de_nuit"]["valeur"] = _k
    _e = _qa.exposition(_dd, pl)
    _tot[_k] = (_e["accidents_avec_arret_attendus"], _e["part_de_nuit_dans_le_risque_pct"])
verifie("INVARIANT : le coefficient de nuit ne change PAS le total d'accidents",
        len({v[0] for v in _tot.values()}) == 1,
        " / ".join(f"k={a} : {b[0]}" for a, b in _tot.items()))
verifie("mais il change la REPARTITION, et dans le bon sens",
        _tot[1.0][1] < _tot[k][1] < _tot[3.0][1],
        " / ".join(f"k={a} : {b[1]} %" for a, b in _tot.items()))
verifie("canari : a k = 1, la part de nuit dans le risque EGALE sa part des heures",
        abs(_tot[1.0][1] - e["part_de_nuit_pct"]) < 0.02,
        f"{_tot[1.0][1]} % contre {e['part_de_nuit_pct']} %")
verifie("la nuit pese plus dans le RISQUE que dans les heures",
        e["part_de_nuit_dans_le_risque_pct"] > e["part_de_nuit_pct"],
        f"{e['part_de_nuit_dans_le_risque_pct']} % du risque pour "
        f"{e['part_de_nuit_pct']} % des heures")
tf = Q["exposition"]["taux_de_frequence_reference"]["valeur"]
verifie("le nombre d'accidents attendus est le taux applique aux heures REELLES",
        abs(e["accidents_avec_arret_attendus"] - tf * e["heures_totales"] / 1e6) < 0.02,
        f"{e['accidents_avec_arret_attendus']} pour TF = {tf}")
verifie("et le module explique pourquoi ce n'est pas sur les heures ponderees",
        "deux fois" in e["_la_ponderation_repartit_elle_n_ajoute_pas"])
verifie("la part attribuable a la nuit est le total fois sa part de risque",
        abs(e["dont_attribuables_a_la_nuit"]
            - e["accidents_avec_arret_attendus"]
            * e["part_de_nuit_dans_le_risque_pct"] / 100) < 0.02)
verifie("l'assiette declare les taches SANS heures au lieu de les taire",
        len(e["assiette"]["taches_sans_heures"]) > 0
        and dit(e["assiette"]["note"], "atelier"),
        f"{e['assiette']['taches_sans_heures']}")
verifie("et elle nomme ses DEUX frontieres : le site, et les entreprises",
        dit(e["assiette"]["consequence"], "fabricant")
        and dit(e["assiette"]["perimetre_des_entreprises"], "sous-trait", "denominateur"),
        "l'atelier est hors assiette ; les sous-traitants y sont")
verifie("le module dit que ce n'est ni une prevision ni un objectif",
        dit(e["_ce_que_le_nombre_d_accidents_n_est_pas"], "prevision", "objectif"))
verifie("et il explique pourquoi la part du risque n'est pas la part des heures fois k",
        dit(e["_pourquoi_le_rapport_n_est_pas_le_coefficient"], "denominateur")
        and abs(e["rapport_des_parts"]
                - e["part_de_nuit_dans_le_risque_pct"] / e["part_de_nuit_pct"]) < 0.02,
        f"x{e['rapport_des_parts']} et non x{e['coefficient_de_surexposition_de_nuit']}")
verifie("la nuit d'interception est declaree nocturne ET plus exposee que productive",
        e["presence_et_production_de_nuit"]["rapport_presence_production"] > 1.0
        and dit(e["presence_et_production_de_nuit"]["note"], "B7c", "exposition"),
        f"{e['presence_et_production_de_nuit']['duree_de_la_plage_h']} h de presence "
        f"pour {e['presence_et_production_de_nuit']['travail_effectif_h']} h de travail")
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
print("\n--- le cout d'une non-conformite, par ouvrage ---")
n = r["non_conformite"]
v = {k_: Q["non_conformite"][k_]["valeur"] for k_ in Q["non_conformite"]
     if isinstance(Q["non_conformite"][k_], dict) and "valeur" in Q["non_conformite"][k_]}
taux_h = d["prix_unitaires_MAD"]["ressources"]["main_oeuvre_MAD_h"]["controleur"]["valeur"]
_taux_compagnon = d["prix_unitaires_MAD"]["ressources"]["main_oeuvre_MAD_h"]["compagnon"]["valeur"]
_reprise = v["surface_m2"] * v["cout_de_reprise_MAD_m2"]
_ctrl = (v["heures_de_controle_par_levee"] * v["durcissement_du_controle_pct"] / 100
         * v["levees_restantes"] * taux_h)
verifie("la part visible est la reprise plus le durcissement du controle",
        abs(n["part_visible_sur_un_devis_MAD"] - (_reprise + _ctrl)) < 1,
        f"{n['part_visible_sur_un_devis_MAD']:.0f} MAD")
verifie("elle ne depend PAS de l'ouvrage touche",
        len({x["reprise_MAD"] + x["durcissement_du_controle_MAD"]
             for x in n["par_ouvrage"]}) == 1)
fd = pr["bordereau"]["frais_de_duree"]["cout_MAD_par_jour_ouvre"]
verifie("les frais de duree sont LUS chez D1, pas re-derives",
        abs(n["frais_de_duree_MAD_par_jour_ouvre"] - fd) < 0.01, f"{fd:.2f} MAD/j")
for x in n["par_ouvrage"]:
    verifie(f"{x['tache']} : les frais de duree suivent le retard MESURE, pas "
            "l'immobilisation",
            abs(x["frais_de_duree_MAD"] - x["retard_du_chantier_j"] * fd) < 1,
            f"{x['retard_du_chantier_j']} j x {fd:.0f} = {x['frais_de_duree_MAD']:.0f} MAD")
    verifie(f"{x['tache']} : total = part visible + frais de duree",
            abs(x["total_MAD"] - (n["part_visible_sur_un_devis_MAD"]
                                  + x["frais_de_duree_MAD"])) < 1)
# LE controle que la premiere version n'avait pas : un ouvrage a marge ne paie AUCUN
# frais de duree. C'est D-040, et le module le violait en facturant 113 682 MAD a un
# ouvrage dont il publiait lui-meme la marge de 436 jours.
for x in n["par_ouvrage"]:
    if x["marge_totale_j"] > 1.0:
        verifie(f"{x['tache']} a de la marge : AUCUN frais de duree ne lui est impute",
                abs(x["frais_de_duree_MAD"]) < 1,
                f"marge {x['marge_totale_j']} j, {x['part_visible_pct']} % visible")
verifie("canari : imputer l'immobilisation a un ouvrage a marge gonflerait son cout",
        min(x["total_MAD"] for x in n["par_ouvrage"])
        < n["part_visible_sur_un_devis_MAD"] + n["jours_immobilises"] * fd - 1,
        "le cout minimal publie est la part visible seule, pas la part visible + "
        f"{n['jours_immobilises']:.0f} j de frais")
verifie("la part visible varie fortement d'un ouvrage a l'autre",
        max(x["part_visible_pct"] for x in n["par_ouvrage"])
        - min(x["part_visible_pct"] for x in n["par_ouvrage"]) > 50,
        " / ".join(f"{x['tache']} {x['part_visible_pct']} %" for x in n["par_ouvrage"]))
verifie("l'ecart entre les regimes est recalcule ici",
        abs(n["ecart_entre_les_regimes"]
            - max(x["total_MAD"] for x in n["par_ouvrage"])
            / min(x["total_MAD"] for x in n["par_ouvrage"])) < 0.1,
        f"x{n['ecart_entre_les_regimes']}")
verifie("le module declare ce qu'il ne chiffre PAS",
        "borne basse" in n["ce_qui_n_est_PAS_chiffre_ici"])

# ------------------------------------------------- 3. l'impact planning, MESURE
print("\n--- l'impact sur le planning, mesure en rejouant le reseau ---")
ip = r["impact_planning"]
verifie("la duree de reference est celle que D2 publie",
        abs(ip["duree_de_reference_j"] - pl["calendrier"]["duree_ouvree_j"]) < 0.5,
        f"{ip['duree_de_reference_j']} j")
verifie("l'immobilisation est la somme du delai de decision et de la reprise",
        abs(ip["immobilisation_j"]
            - (Q["non_conformite"]["delai_de_decision_j"]["valeur"]
               + Q["non_conformite"]["duree_de_reprise_j"]["valeur"])) < 0.01,
        f"{ip['immobilisation_j']} j")
verifie("les trois regimes sont representes",
        len({x["regime"] for x in ip["lignes"]}) == 3,
        " / ".join(f"{x['tache']} {x['regime'].split()[0]}" for x in ip["lignes"]))
for x in ip["lignes"]:
    verifie(f"{x['tache']} : l'amplification est le retard sur l'immobilisation",
            abs(x["amplification"] - x["retard_du_chantier_j"] / ip["immobilisation_j"]) < 0.02)
    verifie(f"{x['tache']} : le regime suit les nombres, pas l'inverse",
            (x["regime"].startswith("absorbé") and x["retard_du_chantier_j"] < 0.01)
            or (x["regime"].startswith("transmis")
                and 0.01 <= x["retard_du_chantier_j"] <= ip["immobilisation_j"] + 0.5)
            or (x["regime"].startswith("amplifié")
                and x["retard_du_chantier_j"] > ip["immobilisation_j"] + 0.5),
            f"{x['retard_du_chantier_j']} j — {x['regime']}")
# LA correction de fond : deux taches de MEME marge donnent des retards differents, donc
# la marge seule ne hierarchise pas. C'est la consignation qui amplifie.
_sans_marge = [x for x in ip["lignes"] if x["marge_totale_j"] < 0.01]
verifie("deux taches de marge nulle sont comparees",
        len(_sans_marge) >= 2,
        " / ".join(f"{x['tache']} {x['marge_totale_j']}" for x in _sans_marge))
verifie("et elles ne donnent PAS le meme retard : la marge seule ne suffit pas",
        len({x["retard_du_chantier_j"] for x in _sans_marge}) == len(_sans_marge),
        " / ".join(f"{x['tache']} {x['retard_du_chantier_j']} j" for x in _sans_marge))
verifie("c'est la consignation qui amplifie, et le module le dit",
        all(x["sous_consignation"] for x in _sans_marge
            if x["retard_du_chantier_j"] > ip["immobilisation_j"] + 0.5)
        and "CONSIGNATION" in ip["la_regle_en_deux_temps"])
verifie("canari : supposer le retard egal a l'immobilisation se trompe des DEUX cotes",
        any(x["retard_du_chantier_j"] > ip["immobilisation_j"] + 0.5 for x in ip["lignes"])
        and any(x["retard_du_chantier_j"] < ip["immobilisation_j"] - 0.5
                for x in ip["lignes"]),
        "une tache amplifie, une autre absorbe")
# canari d'unite : l'immobilisation est un RETARD DE DEBUT, pas un allongement de duree.
_sous_cons = next((x for x in ip["lignes"] if x["sous_consignation"]), None)
if _sous_cons:
    verifie("canari d'unite : l'immobilisation ne s'ajoute pas a une duree en PLAGES",
            "plages" in pl["durees"][_sous_cons["tache"]].get("unite", ""),
            f"{_sous_cons['tache']} se compte en "
            f"{pl['durees'][_sous_cons['tache']].get('unite')} — l'ajout de jours ouvres "
            "y serait une erreur d'unite")

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
        dit(c["_ce_que_la_criticite_n_est_pas"], "moyenne")
        and "%" in c["_ce_que_la_criticite_n_est_pas"])
verifie("le module dit que le seuil se DECIDE et ne se deduit pas",
        dit(c["_le_seuil_est_arbitraire"], "decide", "ne se deduit pas"))
# Les ex aequo sont departages par une regle DECLAREE : a criticite egale, la gravite
# puis la non-detectabilite. Sans la troisieme cle, un risque indetectable passait
# derriere un risque detectable de meme gravite — l'ordre le moins defendable.
_tete = [x for x in c["lignes"] if x["criticite"] == c["lignes"][0]["criticite"]]
verifie("les ex aequo sont ordonnes par gravite puis par NON-detectabilite",
        [(-x["g"], -x["d"]) for x in _tete] == sorted((-x["g"], -x["d"]) for x in _tete),
        " / ".join(f"{x['risque'][:18]} g{x['g']}d{x['d']}" for x in _tete))
verifie("et le nombre d'ex aequo est publie en clair, pas deduit du gabarit",
        c["nb_ex_aequo_en_tete"] == len(_tete), f"{c['nb_ex_aequo_en_tete']} ex aequo")
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
        all("⏸" in x["critere"] or any(dit(x["critere"], mot) for mot in
            ("marche", "plan", "commande", "reference", "tolerance"))
            for x in p["lignes"]),
        "; ".join(x["controle"] for x in p["lignes"]
                  if "⏸" not in x["critere"]
                  and not any(dit(x["critere"], m) for m in
                              ("marche", "plan", "commande", "reference", "tolerance")))
        or "tous renvoient a un document")

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
# Les figures publient trois chiffres significatifs (§ 3.6) : le test verifie donc un
# ECART RELATIF, et il verifie aussi que l'arrondi a bien eu lieu — une figure qui
# imprimerait « 134213,56 » pour une hypothese connue a un facteur deux pres est un
# faux niveau de precision, et c'est ce que la passe adversariale avait vu a l'ecran.
def _trois_cs(x):
    from math import floor, log10
    if not x:
        return 0.0
    # trois chiffres significatifs, y compris au-dessus de 1 000 : l'exposant negatif
    # arrondit a la centaine ou au millier, ce qui est le but.
    return round(x, 2 - floor(log10(abs(x))))


verifie("la figure d'exposition porte des heures, pas des durees",
        all(any(abs(x["valeur"] - _trois_cs(v_)) < 0.01 * max(1.0, abs(v_))
                for v_ in h.values()) for x in f["exposition"]))
verifie("la figure du cout porte les totaux par ouvrage, a trois chiffres significatifs",
        [x["valeur"] for x in f["cout_nc"]]
        == [_trois_cs(x["total_MAD"]) for x in n["par_ouvrage"]],
        " / ".join(f"{x['libelle']} {x['valeur']:.0f}" for x in f["cout_nc"]))
verifie("canari : aucune valeur de figure n'est publiee au centime",
        all(abs(x["valeur"] - round(x["valeur"], 2)) < 1e-9
            and len(f"{x['valeur']:.10f}".rstrip("0").split(".")[1]) <= 2
            for x in f["cout_nc"] + f["dechets"]),
        "les montants et les tonnages sont arrondis avant d'entrer dans la figure")
verifie("la figure d'exposition montre TOUTES les taches qui ont des heures",
        len(f["exposition"]) == sum(1 for v in h.values() if v > 0),
        f"{len(f['exposition'])} barres")
verifie("et elle est triee par heures decroissantes, comme son axe l'annonce",
        [x["valeur"] for x in f["exposition"]]
        == sorted((x["valeur"] for x in f["exposition"]), reverse=True))
verifie("les libelles de criticite ne sont pas tronques",
        [x["libelle"] for x in f["criticite"]] == [x["risque"] for x in c["lignes"]])
verifie("la figure de criticite porte exactement les criticites publiees",
        [x["valeur"] for x in f["criticite"]] == [x["criticite"] for x in c["lignes"]])
verifie("la figure des dechets totalise le tonnage publie, a l'arrondi pres",
        abs(sum(x["valeur"] for x in f["dechets"]) - de["total_tonnes"])
        < 0.01 * de["total_tonnes"],
        f"{sum(x['valeur'] for x in f['dechets']):.1f} t contre {de['total_tonnes']} t")

# ------------------------------------------------- 7. les bornes (D-036)
print("\n--- les bornes : tout ce qui est publie porte ses deux bornes ---")
# REGLE, pas conclusion : toute grandeur qui publie des bornes doit les publier dans
# l'ordre, et sa valeur nominale doit tomber dedans. Le test ne fixe aucune largeur :
# si la fourchette change dans data/, il reste vrai.
_couples = [
    ("accidents attendus", e["accidents_avec_arret_attendus"], e["accidents_bornes"]),
    ("journees perdues", e["journees_perdues_attendues"], e["journees_perdues_bornes"]),
    ("part de nuit dans le risque", e["part_de_nuit_dans_le_risque_pct"],
     e["part_de_nuit_dans_le_risque_bornes_pct"]),
    ("part visible de la NC", n["part_visible_sur_un_devis_MAD"],
     n["part_visible_bornes_MAD"]),
    ("dechets, total", de["total_tonnes"], de["total_bornes_tonnes"]),
]
for nom_, val_, b_ in _couples:
    verifie(f"{nom_} : borne basse <= valeur <= borne haute",
            b_[0] <= val_ <= b_[1],
            f"{b_[0]} <= {val_} <= {b_[1]}")
for x in n["par_ouvrage"]:
    verifie(f"{x['tache']} : le cout nominal tombe dans ses bornes",
            x["total_bornes_MAD"][0] <= x["total_MAD"] <= x["total_bornes_MAD"][1],
            f"{x['total_bornes_MAD'][0]:.0f} <= {x['total_MAD']:.0f} <= "
            f"{x['total_bornes_MAD'][1]:.0f}")
    verifie(f"{x['tache']} : les bornes du retard sont MESUREES, pas deduites",
            x["retard_bornes_j"][0] <= x["retard_du_chantier_j"] <= x["retard_bornes_j"][1],
            f"{x['retard_bornes_j']} pour un retard de {x['retard_du_chantier_j']} j")
# canari qui CHERCHE : une regle de trois sur l'immobilisation donnerait, pour la tache
# sous consignation, des bornes differentes de celles que le reseau rend.
_ib = r["impact_planning_bornes"]
_cons = next(x for x in n["par_ouvrage"] if x["tache"] == ip["lignes"][0]["tache"])
_regle_de_trois = [round(_cons["retard_du_chantier_j"] * _ib["immobilisation_basse_j"]
                         / ip["immobilisation_j"], 2),
                   round(_cons["retard_du_chantier_j"] * _ib["immobilisation_haute_j"]
                         / ip["immobilisation_j"], 2)]
verifie("canari : la regle de trois ne retrouve PAS les bornes mesurees",
        _regle_de_trois != _cons["retard_bornes_j"],
        f"regle de trois {_regle_de_trois} contre mesure {_cons['retard_bornes_j']}")

# ------------------------------------------------- 8. la quantification du retard
print("\n--- sous consignation, le retard est quantifie ---")
qd = r["quantification_du_retard"]
_pas = qd["pas_j"]
verifie("chaque palier observe est un multiple entier du pas des fenetres",
        all(abs(x / _pas - round(x / _pas)) < 0.01 for x in qd["paliers_observes_j"]),
        f"paliers {qd['paliers_observes_j']} pour un pas de {_pas} j")
verifie("le retard croit avec l'immobilisation, sans jamais decroitre",
        all(a_["retard_j"] <= b_["retard_j"] + 1e-9
            for a_, b_ in zip(qd["sondes"], qd["sondes"][1:])),
        " / ".join(f"{x['immobilisation_j']}->{x['retard_j']}" for x in qd["sondes"]))
verifie("et il prend STRICTEMENT moins de valeurs que de sondes : c'est le palier",
        len(qd["paliers_observes_j"]) < len(qd["sondes"]),
        f"{len(qd['paliers_observes_j'])} paliers pour {len(qd['sondes'])} sondes")
verifie("une demi-journee d'immobilisation coute deja un pas entier",
        abs(qd["sondes"][0]["retard_j"] - _pas) < 0.01,
        f"{qd['sondes'][0]['immobilisation_j']} j d'immobilisation -> "
        f"{qd['sondes'][0]['retard_j']} j de retard")
sp = r["sensibilite_a_la_periode"]
verifie("la periode des fenetres est bien le parametre qui porte le retard",
        len({x["retard_j"] for x in sp["lignes"]}) == len(sp["lignes"]),
        " / ".join(f"periode {x['periode_j']} j -> {x['retard_j']} j"
                   for x in sp["lignes"]))
verifie("et chaque ligne a sa propre duree de reference, recalculee",
        len({x["duree_de_reference_j"] for x in sp["lignes"]}) == len(sp["lignes"]),
        " / ".join(f"{x['duree_de_reference_j']} j" for x in sp["lignes"]))

# ------------------------------------------------- 9. l'heure de controle
print("\n--- l'heure de controle n'est pas l'heure de production ---")
verifie("le durcissement du controle est paye au taux du CADRE, pas du compagnon",
        abs(n["taux_de_l_heure_de_controle_MAD"] - taux_h) < 0.01
        and taux_h > _taux_compagnon,
        f"{taux_h} MAD/h contre {_taux_compagnon} MAD/h pour un compagnon")
_ligne_ctrl = n["detail_de_la_part_visible"][1]["montant_MAD"]
_h_sup = (v["heures_de_controle_par_levee"] * v["durcissement_du_controle_pct"] / 100
          * v["levees_restantes"])
verifie("et la ligne du durcissement est bien ce taux fois les heures ajoutees",
        abs(_ligne_ctrl - _h_sup * taux_h) < 1
        and abs(n["heures_de_controle_ajoutees"] - _h_sup) < 0.05,
        f"{_h_sup:.2f} h x {taux_h} = {_ligne_ctrl:.0f} MAD")
# La conclusion du module tient-elle encore avec le bon taux ? Le test ne l'EPINGLE pas :
# il verifie que le module publie les deux lignes, et il affiche leur rapport.
verifie("les deux lignes de la part visible sont publiees separement",
        len(n["detail_de_la_part_visible"]) == 2,
        f"reprise {n['detail_de_la_part_visible'][0]['montant_MAD']:.0f} MAD contre "
        f"controle {n['detail_de_la_part_visible'][1]['montant_MAD']:.0f} MAD")

# ------------------------------------------------- 10. le plan de controle, suite
print("\n--- qui execute, qui vise, et ce qui est point d'arret ---")
for x in p["lignes"]:
    verifie(f"{x['controle'][:28]} : l'executant et le visa sont distingues",
            bool(str(x["qui"]).strip()) and bool(str(x["visa"]).strip()),
            f"{x['qui']} / visa {x['visa']}")
verifie("les points d'arret portent une duree, et elle est au planning",
        all(x["duree_h"] > 0 for x in p["lignes"] if x["point_d_arret"]),
        f"{p['nb_points_d_arret']} point(s) d'arret, "
        f"{p['heures_de_points_d_arret']} h")
verifie("le total des heures de controle est la somme des lignes",
        abs(p["heures_de_controle_total"] - sum(x["duree_h"] for x in p["lignes"])) < 0.01)
verifie("le perimetre du plan est declare, et il nomme les deux autres plans du cours",
        "C3" in p["perimetre"] and "B3e" in p["perimetre"],
        "les trois plans sont emboites, pas concurrents")
verifie("et le module explique pourquoi C3 et C7 n'attribuent pas le meme acte au meme",
        "visa" in p["qui_et_visa"].lower() and "autocontrole" in p["qui_et_visa"].lower())

# ------------------------------------------------- 11. l'exercice 1, calcule
print("\n--- l'exercice 1 : plus un seul nombre tape a la main ---")
cx = r["comparaison_de_deux_chantiers"]
_hpa = Q["exposition"]["heures_par_compagnon_et_par_an"]["valeur"]
verifie("les heures annuelles viennent de data/, avec leur fourchette",
        abs(cx["heures_par_compagnon_et_par_an"] - _hpa) < 0.01
        and "fourchette" in Q["exposition"]["heures_par_compagnon_et_par_an"],
        f"{_hpa} h/an")
for x in cx["chantiers"]:
    verifie(f"chantier {x['nom']} : heures = effectif x heures annuelles",
            abs(x["heures"] - x["effectif"] * _hpa) < 1)
    verifie(f"chantier {x['nom']} : TF = accidents x 1e6 / heures",
            abs(x["tf"] - x["accidents"] * 1e6 / x["heures"]) < 0.1,
            f"TF {x['tf']} [{x['tf_bornes'][0]} a {x['tf_bornes'][1]}]")
_a, _b = cx["chantiers"]
verifie("le chantier qui declare MOINS d'accidents a le PIRE taux",
        (_a["accidents"] < _b["accidents"]) == (_a["tf"] > _b["tf"]),
        f"{_a['accidents']} accidents -> TF {_a['tf']} ; "
        f"{_b['accidents']} -> TF {_b['tf']}")
verifie("et le rapport des taux ne depend pas de l'hypothese d'heures annuelles",
        abs(cx["rapport_des_taux"]
            - (_a["accidents"] / _a["effectif"]) / (_b["accidents"] / _b["effectif"])) < 0.01,
        f"x{cx['rapport_des_taux']} — l'hypothese se simplifie")

print()
if echecs:
    print(f"ECHEC : {len(echecs)} controle(s) — {', '.join(echecs)}")
    sys.exit(1)
print("Tests qualite : tous verts.")
