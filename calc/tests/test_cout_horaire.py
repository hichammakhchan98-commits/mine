"""Tests du module C6 — materiel : l'heure d'un engin et ce qu'elle decide.

Des tests de REGLE. Aucun n'epingle « 943 h/an » ni « 75,4 % » : ils verifient qu'un
cout fixe se decompose en ses trois lignes, qu'un point d'equilibre annule l'ecart des
deux couts, que chaque regime de location facture dans SON unite, qu'un taux d'emploi
est un rapport de jours LUS dans le planning, et qu'une disponibilite de chaine est un
produit. Sept canaris cherchent l'erreur au lieu de la confirmer.
"""
from __future__ import annotations
import json, math, sys, pathlib, unicodedata

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))

echecs = []


def sansaccent(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s).lower())
                   if unicodedata.category(c) != "Mn").replace("œ", "oe")


def dit(texte, *mots):
    t_ = sansaccent(texte)
    return all(sansaccent(m) in t_ for m in mots)


def verifie(nom, condition, detail=""):
    if not condition:
        echecs.append(nom)
    print(f"  {'ok   ' if condition else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


S = RACINE / "calc" / "sorties"
d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
r = json.loads((S / "materiel.json").read_text(encoding="utf-8"))
pl = json.loads((S / "planification.json").read_text(encoding="utf-8"))
prix = json.loads((S / "prix.json").read_text(encoding="utf-8"))
go = json.loads((S / "gros-oeuvre.json").read_text(encoding="utf-8"))
tp = json.loads((S / "tranche-plancher.json").read_text(encoding="utf-8"))
M = d["materiel_engins"]
MAT = d["prix_unitaires_MAD"]["ressources"]["materiel_MAD"]
import cout_horaire as ch                                               # noqa: E402

FAM = {f["cle"]: f for f in M["familles"]}
VER = {v["cle"]: v for v in r["verdicts"]}
EMP = r["emplois"]


def val(o):
    return float(o["valeur"]) if isinstance(o, dict) else float(o)


REL = 1e-4   # les sorties sont arrondies : on compare en relatif

# ------------------------------------------------------- 1. la decomposition du cout
print("\n--- le cout annuel se decompose, ligne a ligne ---")
for cle, v in VER.items():
    f = FAM[cle]
    achat, res = val(f["prix_achat_MAD"]), val(M["valeur_residuelle_pct"])
    amort = achat * (1 - res / 100) / val(f["amortissement_ans"])
    entr = achat * val(f["entretien_pct_achat_an"]) / 100
    fin = achat * (1 + res / 100) / 2 * val(M["cout_financier_pct_an"]) / 100
    verifie(f"{cle} : amortissement = (achat − residuelle) / annees",
            abs(v["amortissement_MAD_an"] - amort) < 1, f"{v['amortissement_MAD_an']:.0f}")
    verifie(f"{cle} : entretien = part du prix d'achat",
            abs(v["entretien_MAD_an"] - entr) < 1)
    verifie(f"{cle} : cout financier sur le capital MOYEN, non sur le prix d'achat",
            abs(v["cout_financier_MAD_an"] - fin) < 1
            and v["cout_financier_MAD_an"] < achat * val(M["cout_financier_pct_an"]) / 100)
    verifie(f"{cle} : la part fixe est la somme des trois lignes",
            abs(v["fixe_MAD_an"] - (amort + entr + fin)) < 2)
    varh = val(f["carburant_l_h"]) * val(M["gasoil_MAD_l"]) + val(M["conducteur_MAD_h"])
    verifie(f"{cle} : la part variable est carburant + conducteur",
            abs(v["variable_MAD_h"] - varh) < 0.1, f"{v['variable_MAD_h']} MAD/h")
    verifie(f"{cle} : possession = fixe + heures x variable",
            abs(v["possession_MAD_an"] - (v["fixe_MAD_an"] + v["heures_par_an_h"] * varh))
            < REL * v["possession_MAD_an"])
    verifie(f"{cle} : l'ecart publie est bien possession − location",
            abs(v["ecart_MAD_an"] - (v["possession_MAD_an"] - v["location_MAD_an"])) < 2)
    verifie(f"{cle} : le cout horaire de possession est l'annuel / les heures",
            abs(v["possession_MAD_h"] - v["possession_MAD_an"] / v["heures_par_an_h"])
            < 1e-3 * v["possession_MAD_h"])
    verifie(f"{cle} : la part fixe ne depend PAS de l'emploi",
            abs(ch.couts_annuels(ch.parametres(d, f, "nominal"), 1.0, 1.0)["fixe_MAD_an"]
                - v["fixe_MAD_an"]) < 2)

# ------------------------------------------------------- 2. les trois regimes de location
print("\n--- chaque regime facture dans SON unite ---")
ATTENDU = {"pompe": ("par_intervention", "interventions"),
           "pelle": ("par_heure_de_service", "heures de service"),
           "chariot": ("par_duree_de_presence", "jours de présence")}
for cle, (reg, unite) in ATTENDU.items():
    e = EMP[cle]
    verifie(f"{cle} : regime « {reg} », facture en {unite}",
            FAM[cle]["regime_de_location"] == reg
            and e["unite_de_facturation"] == unite
            and VER[cle]["unite_de_facturation"] == unite)
    prix_u = val(ch._prix_de_location(d, FAM[cle]))
    par = ch.parametres(d, FAM[cle], "nominal")
    attendu = (e["_unites_par_an_exact"] * prix_u
               + e["_heures_par_an_exact"] * par["_en_plus_MAD_h"])
    verifie(f"{cle} : location annuelle = unites x prix + ce que le prix NE comprend pas",
            abs(VER[cle]["location_MAD_an"] - attendu) < REL * VER[cle]["location_MAD_an"],
            f"{VER[cle]['location_MAD_an']:.0f} MAD/an")

print("\n--- ce que le prix de location comprend, et ce qui s'ajoute ---")
for cle in ATTENDU:
    par = ch.parametres(d, FAM[cle], "nominal")
    compris = FAM[cle]["location"].get("comprend", [])
    attendu = ((0.0 if "operateur" in compris else val(M["conducteur_MAD_h"]))
               + (0.0 if "carburant" in compris
                  else val(FAM[cle]["carburant_l_h"]) * val(M["gasoil_MAD_l"])))
    verifie(f"{cle} : ce que le prix ne comprend pas s'ajoute A L'HEURE TRAVAILLEE",
            abs(par["_en_plus_MAD_h"] - attendu) < 0.01,
            f"{par['_en_plus_MAD_h']} MAD/h en plus, prix comprenant {compris}")
    verifie(f"{cle} : et chaque famille DIT ce que son prix comprend",
            bool(compris) and len(FAM[cle]["location"]["_comprend"]) > 40)
verifie("LE POINT DU MODULE : pour une location NUE payee a la presence, ce qui "
        "s'ajoute vaut exactement le cout variable de la possession",
        abs(ch.parametres(d, FAM["chariot"], "nominal")["_en_plus_MAD_h"]
            - VER["chariot"]["variable_MAD_h"]) < 0.01,
        f"{VER['chariot']['variable_MAD_h']} MAD/h des deux cotes")
verifie("donc la pente de son ecart est NULLE, et il n'a aucun seuil",
        VER["chariot"]["equilibre"]["pente_nulle"]
        and VER["chariot"]["equilibre"]["seuil_h_par_an"] is None
        and dit(VER["chariot"]["equilibre"]["sens"], "ne depend pas"))
verifie("et son ecart est le MEME a tout emploi : F moins L0",
        abs(VER["chariot"]["ecart_MAD_an"]
            - (VER["chariot"]["fixe_MAD_an"]
               - VER["chariot"]["equilibre"]["location_fixe_L0_MAD_an"])) < 2)
verifie("canari : compter le carburant du seul cote de la possession redonnerait une "
        "pente egale au gasoil, et c'etait le defaut bloquant de la premiere version",
        abs(val(FAM["chariot"]["carburant_l_h"]) * val(M["gasoil_MAD_l"])
            - (VER["chariot"]["variable_MAD_h"] - val(M["conducteur_MAD_h"]))) < 0.01,
        f"{val(FAM['chariot']['carburant_l_h']) * val(M['gasoil_MAD_l'])} MAD/h")
verifie("la pompe facture autant d'unites que d'interventions, pas de jours de tache",
        EMP["pompe"]["unites_facturees"] == EMP["pompe"]["interventions"]
        and EMP["pompe"]["unites_facturees"] < EMP["pompe"]["jours_de_travail_j"],
        f"{EMP['pompe']['unites_facturees']} interventions pour "
        f"{EMP['pompe']['jours_de_travail_j']:.0f} jours de tache")
verifie("la pelle facture exactement ses heures de travail",
        abs(EMP["pelle"]["unites_facturees"] - EMP["pelle"]["heures_de_travail_h"]) < 0.2)
verifie("le chariot facture sa FENETRE, jours sans emploi compris",
        abs(EMP["chariot"]["unites_facturees"] - EMP["chariot"]["fenetre_duree_j"]) < 0.02
        and EMP["chariot"]["unites_facturees"] > EMP["chariot"]["jours_de_travail_j"],
        f"{EMP['chariot']['unites_facturees']} j de presence pour "
        f"{EMP['chariot']['jours_de_travail_j']} j de travail")
verifie("et c'est ce regime qui coute le plus cher par heure de travail, "
        "sans etre le plus cher a l'unite",
        max(r["cout_du_parc"]["lignes"],
            key=lambda l: l["cout_par_heure_de_travail_MAD"])["cle"] == "pompe"
        and r["cout_du_parc"]["lignes"][2]["cout_par_heure_de_travail_MAD"]
        > r["cout_du_parc"]["lignes"][1]["cout_par_heure_de_travail_MAD"])
verifie("aucun prix de location n'est redeclare quand le bordereau de D1 le porte",
        all("cle_prix" in FAM[c]["location"] for c in ("pompe", "pelle"))
        and FAM["pompe"]["location"]["cle_prix"] in MAT
        and FAM["pelle"]["location"]["cle_prix"] in MAT)
verifie("le seul prix declare ici est celui qui manquait au bordereau",
        "MAD_j" in FAM["chariot"]["location"]
        and not any("chariot" in k for k in MAT))

# ------------------------------------------------------- 3. le point d'equilibre
print("\n--- le seuil d'emploi, et de quel cote il penche ---")
for cle, v in VER.items():
    eq, f, e = v["equilibre"], FAM[cle], EMP[cle]
    par = ch.parametres(d, f, "nominal")
    L0, L1 = ch.location_affine(par, e)
    verifie(f"{cle} : la location est affine, L0 + L1.h, et ses deux termes sont publies",
            abs(eq["location_fixe_L0_MAD_an"] - L0) < 1
            and abs(eq["location_marginale_L1_MAD_h"] - L1) < 0.1,
            f"L0 = {eq['location_fixe_L0_MAD_an']:,} MAD/an, "
            f"L1 = {eq['location_marginale_L1_MAD_h']} MAD/h".replace(",", " "))
    verifie(f"{cle} : la forme affine redonne la location publiee au point de "
            f"fonctionnement",
            abs(L0 + L1 * e["_heures_par_an_exact"] - v["location_MAD_an"])
            < REL * v["location_MAD_an"])
    verifie(f"{cle} : la pente de l'ecart est le cout variable moins L1",
            abs(eq["pente_de_l_ecart_MAD_h"] - (v["variable_MAD_h"] - L1)) < 0.2)
    verifie(f"{cle} : l'ecart a emploi nul est F − L0",
            abs(eq["ecart_a_emploi_nul_MAD_an"] - (v["fixe_MAD_an"] - L0)) < 2)
    verifie(f"{cle} : le seuil annule la droite de l'ecart",
            eq["seuil_h_par_an"] is None
            or abs(eq["ecart_a_emploi_nul_MAD_an"]
                   + eq["seuil_h_par_an"] * eq["pente_de_l_ecart_MAD_h"])
            < 1e-3 * abs(v["possession_MAD_an"]),
            f"seuil {eq['seuil_h_par_an']} h/an")
    if eq["seuil_h_par_an"]:
        # contre-controle : au seuil, les deux couts annuels se rejoignent VRAIMENT —
        # on les recalcule au lieu de rejouer la formule du seuil
        h = eq["seuil_h_par_an"]
        c = ch.couts_annuels(par, h, ch._unites(par, e, h))
        verifie(f"{cle} : au seuil, possession = location, recalcule",
                abs(c["ecart_MAD_an"]) < 1e-3 * c["possession_MAD_an"],
                f"{c['ecart_MAD_an']:.1f} MAD/an")
    verifie(f"{cle} : le SENS du seuil suit le signe de la pente, "
            f"et il est ecrit en clair",
            (eq["pente_de_l_ecart_MAD_h"] < 0) == eq["cas_classique"]
            and ("AU-DESSUS" in eq["sens"]) == eq["cas_classique"])
    verifie(f"{cle} : « cote du seuil » dit de quel cote l'emploi reel tombe",
            v["cote_du_seuil"] == ("au-dessus" if eq["seuil_h_par_an"]
                                   and v["heures_par_an_h"] > eq["seuil_h_par_an"]
                                   else "au-dessous" if eq["seuil_h_par_an"] else None))
    verifie(f"{cle} : le verdict nominal suit le signe de l'ecart",
            (v["verdict_nominal"] == "posseder") == (v["ecart_MAD_an"] < 0))
    verifie(f"{cle} : et il est COHERENT avec le sens et le cote du seuil",
            v["verdict_nominal"] == ("posseder" if (
                (v["cote_du_seuil"] == "au-dessus") == eq["cas_classique"])
                else "louer"))
    verifie(f"{cle} : le verdict publie suit la part des tirages et le seuil declare",
            v["verdict"] == ("POSSÉDER" if v["part_des_tirages_pro_possession_pct"]
                             >= 100 - v["seuil_de_verdict_pct"]
                             else "LOUER" if v["part_des_tirages_pro_possession_pct"]
                             <= v["seuil_de_verdict_pct"] else "NON TRANCHÉ"))
    par_jour = (e["duree_d_une_intervention_h"]
                if f["regime_de_service"] == "intervention"
                else e["heures_par_jour_servi_h"])
    verifie(f"{cle} : le plafond d'emploi est a CETTE intensite, pas un plafond physique",
            abs(v["heures_max_a_cette_intensite_h"]
                - v["jours_ouvres_par_an_j"] * par_jour) < 0.2
            and dit(v["_coin_extreme"], "coin"))
    verifie(f"{cle} : « seuil hors d'atteinte » compare le seuil a ce plafond",
            v["seuil_hors_d_atteinte"]
            == (eq["seuil_h_par_an"] is None
                or eq["seuil_h_par_an"] > v["heures_max_a_cette_intensite_h"]))
    verifie(f"{cle} : une conclusion sans estimation n'existe QUE si le seuil est hors "
            f"d'atteinte, et son camp est celui du sens",
            (v["conclusion_sans_estimation"] is not None) == v["seuil_hors_d_atteinte"]
            and (v["conclusion_sans_estimation"] is None
                 or sansaccent(v["conclusion_sans_estimation"]).startswith(
                     "louer" if eq["cas_classique"] else "posseder")),
            str(v["conclusion_sans_estimation"]))
    verifie(f"{cle} : et elle ne contredit pas le verdict nominal",
            v["conclusion_sans_estimation"] is None
            or sansaccent(v["conclusion_sans_estimation"]).startswith(
                sansaccent(v["verdict_nominal"])))
verifie("les trois engins se tranchent SANS estimer leur emploi : leur seuil est hors "
        "d'atteinte dans les trois cas",
        all(v["seuil_hors_d_atteinte"] and v["conclusion_sans_estimation"]
            for v in VER.values()))
verifie("deux regimes sur trois donnent le cas classique — possession au-dessus du "
        "seuil — et celui de la presence n'a pas de seuil",
        VER["pompe"]["equilibre"]["cas_classique"]
        and VER["pelle"]["equilibre"]["cas_classique"]
        and VER["chariot"]["equilibre"]["pente_nulle"]
        and FAM["chariot"]["regime_de_location"] == "par_duree_de_presence")
verifie("et c'est bien parce que la location devient un cout FIXE : L0 porte toute la "
        "facture et L1 ne porte que ce que le prix ne comprend pas",
        VER["chariot"]["equilibre"]["location_fixe_L0_MAD_an"] > 0
        and abs(VER["chariot"]["equilibre"]["location_marginale_L1_MAD_h"]
                - VER["chariot"]["variable_MAD_h"]) < 0.1
        and all(VER[c]["equilibre"]["location_fixe_L0_MAD_an"] == 0
                for c in ("pompe", "pelle")))
verifie("pour la pompe, les DEUX coins extremes donnent le meme verdict : aucune "
        "combinaison de ces fourchettes ne peut l'inverser",
        VER["pompe"]["bornes_tranchent"]
        and VER["pompe"]["ecart_pro_possession_MAD_an"] > 0
        and VER["pompe"]["verdict"] == "LOUER",
        f"{VER['pompe']['ecart_pro_possession_MAD_an']:,} MAD/an au coin le plus "
        f"favorable a la possession".replace(",", " "))
verifie("pour les deux autres, les coins encadrent le seuil et ne disent rien : "
        "c'est la part des tirages qui tranche",
        all(not VER[c]["bornes_tranchent"]
            and VER[c]["ecart_pro_possession_MAD_an"] < 0
            < VER[c]["ecart_pro_location_MAD_an"] for c in ("pelle", "chariot")))
verifie("et le texte du module dit LEQUEL des deux cas s'applique a chaque engin",
        dit(VER["pompe"]["_coin_extreme"], "concordent")
        and all(dit(VER[c]["_coin_extreme"], "encadrent le seuil pour cet engin")
                for c in ("pelle", "chariot")))
verifie("la part des tirages est une part, et les tirages sont nombreux",
        all(0 <= v["part_des_tirages_pro_possession_pct"] <= 100
            and v["nb_tirages"] >= 10000 for v in VER.values()))
verifie("les engins a service continu tirent une intensite de plus que la pompe, "
        "dont l'emploi est entierement deduit",
        VER["pompe"]["nb_parametres_tires"] + 1
        == VER["pelle"]["nb_parametres_tires"] == VER["chariot"]["nb_parametres_tires"])

# ------------------------------------------------- 4. le taux d'emploi, lu au planning
print("\n--- le taux d'emploi se lit dans le planning ---")
seg = pl["segments_de_travail"]
joa = val(M["jours_ouvres_par_an"])
for cle, e in EMP.items():
    f = FAM[cle]
    union = set()
    for t in e["taches"]:
        for a, b in seg[t]:
            union.update(range(int(math.floor(a)), int(math.ceil(b))))
    somme = sum(b - a for t in e["taches"] for a, b in seg[t])
    deb = min(a for t in e["taches"] for a, b in seg[t])
    fin = max(b for t in e["taches"] for a, b in seg[t])
    verifie(f"{cle} : les jours de travail sont l'UNION des jours, non la somme des "
            f"segments",
            e["jours_de_travail_j"] == float(len(union))
            and abs(e["somme_des_segments_j"] - somme) < 0.02,
            f"{e['jours_de_travail_j']:.0f} j d'union pour {somme:.0f} j de segments")
    verifie(f"{cle} : l'ecart avec la somme des segments est publie, et ses DEUX "
            f"causes sont ecrites",
            abs(e["ecart_avec_la_somme_des_segments_j"] - (somme - len(union))) < 0.02
            and dit(e["_pourquoi_l_union"], "deux fois", "journee entiere", "union"),
            f"{e['ecart_avec_la_somme_des_segments_j']:+.1f} j")
    verifie(f"{cle} : l'intensite d'emploi reste sous les heures d'une journee",
            e["heures_de_travail_h"] / e["jours_de_travail_j"] <= 8.0,
            f"{e['heures_de_travail_h'] / e['jours_de_travail_j']:.1f} h par jour "
            f"reellement travaille")
    verifie(f"{cle} : la fenetre va du premier au dernier jour de besoin",
            abs(e["fenetre_j"][0] - deb) < 0.02 and abs(e["fenetre_j"][1] - fin) < 0.02)
    verifie(f"{cle} : la fenetre en annees passe par les jours ouvres PAR AN",
            abs(e["fenetre_ans"] - e["fenetre_duree_j"] / joa) < 0.002)
    verifie(f"{cle} : les heures par an sont les heures de travail / la fenetre en annees",
            abs(e["heures_par_an_h"]
                - e["heures_de_travail_h"] / e["_fenetre_ans_exact"])
            < 2e-3 * e["heures_par_an_h"])
    verifie(f"{cle} : le taux de presence utile est jours de travail / fenetre",
            abs(e["taux_de_presence_utile_pct"]
                - e["jours_de_travail_j"] / e["fenetre_duree_j"] * 100) < 0.2,
            f"{e['taux_de_presence_utile_pct']} %")
    verifie(f"{cle} : les jours de presence sans travail completent la fenetre",
            abs(e["jours_de_presence_sans_travail_j"]
                + e["jours_de_travail_j"] - e["fenetre_duree_j"]) < 0.2)
    verifie(f"{cle} : toutes les taches servies existent dans le planning",
            not e["taches_absentes_du_planning"])
    verifie(f"{cle} : le verdict lit l'emploi publie, sans le recalculer",
            abs(e["heures_par_an_h"] - VER[cle]["heures_par_an_h"]) < 0.05
            and abs(e["unites_facturees_par_an"]
                    - VER[cle]["unites_facturees_par_an"]) < 0.05)
verifie("la somme des durees declarees de D2 egale la somme des segments, par "
        "construction de son modele",
        all(abs(e["somme_des_segments_j"] - e["jours_de_travail_voie_durees_j"]) < 0.02
            for e in EMP.values()))
# REGLE et non ordre : c'est la fenetre qui fait le taux de presence utile, pas la
# machine. La famille a la fenetre la plus courte a donc le meilleur taux, et celle a la
# fenetre la plus longue le plus mauvais — quelles qu'elles soient.
_par_fenetre = sorted(EMP, key=lambda c: EMP[c]["fenetre_duree_j"])
verifie("la fenetre la plus courte donne le meilleur taux de presence utile, et la plus "
        "longue le plus mauvais : c'est la fenetre qui fait le taux, pas l'engin",
        EMP[_par_fenetre[0]]["taux_de_presence_utile_pct"]
        > EMP[_par_fenetre[-1]]["taux_de_presence_utile_pct"],
        " < ".join(f"{c} {EMP[c]['fenetre_duree_j']:.0f} j "
                   f"({EMP[c]['taux_de_presence_utile_pct']} %)" for c in _par_fenetre))

print("\n--- l'emploi de la pompe est DEDUIT, pas declare ---")
ep = EMP["pompe"]
jours_D1 = sum(m["quantite"] * p["quantite"] for p in prix["bordereau"]["postes"]
               for m in (p.get("materiel") or []) if m["ressource"] == "pompe_a_beton_j")
coef = val(d["prix_unitaires_MAD"]["coefficients_sous_detail"]["pompe_j_par_m3"])
verifie("les taches de la pompe sont DEDUITES du bordereau : ce sont les postes dont "
        "le sous-detail porte sa ressource, et non une liste declaree",
        ep["taches_deduites_du_bordereau"]
        and set(ep["taches"]) == {p_["poste"] for p_ in prix["bordereau"]["postes"]
                                  if any(m_["ressource"] == "pompe_a_beton_j"
                                         for m_ in (p_.get("materiel") or []))},
        " ".join(ep["taches"]))
verifie("et son cout horaire se calcule donc sur un perimetre COHERENT : les heures et "
        "la fenetre viennent des memes taches",
        not EMP["pelle"]["taches_deduites_du_bordereau"]
        and VER["pompe"]["possession_MAD_h"] < 10000,
        f"{VER['pompe']['possession_MAD_h']} MAD/h")
verifie("le volume pompe est celui du bordereau de D1, divise par son coefficient",
        abs(ep["volume_pompe_du_bordereau_m3"] - jours_D1 / coef) < 0.2,
        f"{ep['volume_pompe_du_bordereau_m3']} m3")
verifie("le volume d'un coulage est celui d'une zone du module TV, non redeclare",
        ep["volume_d_un_coulage_m3"] == tp["quantites"]["beton_m3"])
verifie("la duree d'une intervention est celle que C3 calcule, non redeclaree",
        ep["duree_d_une_intervention_h"] == go["fenetre_de_coulage"]["duree_du_coulage_h"])
verifie("le nombre d'interventions est le volume / le volume d'un coulage, arrondi "
        "AU-DESSUS : on n'achete pas une demie venue",
        ep["interventions"]
        == math.ceil(ep["volume_pompe_du_bordereau_m3"] / ep["volume_d_un_coulage_m3"]))
verifie("et les heures de la pompe en decoulent, sans aucune heure declaree",
        abs(ep["heures_de_travail_h"]
            - ep["interventions"] * ep["duree_d_une_intervention_h"]) < 0.1
        and "heures_par_jour_servi" not in FAM["pompe"],
        f"{ep['heures_de_travail_h']} h")

# ------------------------------------------------------- 5. le parc jour par jour
print("\n--- le parc : present n'est pas au travail ---")
p = r["parc"]
verifie("l'aire de presence domine l'aire de travail",
        p["engins_jours_de_presence"] > p["engins_jours_de_travail"])
verifie("le taux d'emploi du parc est le rapport des deux aires",
        abs(p["taux_d_emploi_du_parc_pct"]
            - p["engins_jours_de_travail"] / p["engins_jours_de_presence"] * 100) < 0.2,
        f"{p['taux_d_emploi_du_parc_pct']} %")
verifie("la pointe de presence ne depasse pas le nombre de familles",
        p["pointe_presents"] <= len(M["familles"])
        and p["pointe_au_travail"] <= p["pointe_presents"])
verifie("les deux profils ont la meme longueur, et elle couvre le chantier",
        len(p["profil_presents"]) == len(p["profil_travail"]) == p["jours"]
        and p["jours"] >= math.floor(pl["calendrier"]["duree_ouvree_j"]) - 40)
verifie("le profil de travail est partout sous le profil de presence",
        all(t <= pr for t, pr in zip(p["profil_travail"], p["profil_presents"])))
for fam in p["familles"]:
    e = EMP[fam["cle"]]
    verifie(f"{fam['cle']} : la fenetre du parc est celle de l'emploi",
            abs(fam["debut_j"] - e["fenetre_j"][0]) < 0.1
            and abs(fam["fin_j"] - e["fenetre_j"][1]) < 0.1)
    verifie(f"{fam['cle']} : sa PRESENCE est sa fenetre s'il se paie a la presence, "
            f"et ses seuls jours de travail sinon",
            fam["paye_a_la_presence"]
            == (FAM[fam["cle"]]["regime_de_location"] == "par_duree_de_presence")
            and (fam["jours_de_presence"] > e["jours_de_travail_j"]
                 if fam["paye_a_la_presence"]
                 else fam["jours_de_presence"] == e["jours_de_travail_j"]),
            f"{fam['jours_de_presence']} j de presence pour "
            f"{e['jours_de_travail_j']:.0f} j de travail")
verifie("et le perimetre du parc est ecrit : ni la grue de C1 ni le coffrage de C3",
        dit(p["_perimetre"], "C1", "C3", "pointe"))

print("\n--- ce que le parc coute, et ce qui n'est nulle part visible ---")
cp = r["cout_du_parc"]
for l in cp["lignes"]:
    e = EMP[l["cle"]]
    verifie(f"{l['cle']} : le cout du chantier est unites x prix + ce que le prix ne "
            f"comprend pas",
            abs(l["cout_sur_le_chantier_MAD"]
                - (l["unites_facturees"] * l["prix_unitaire_MAD"]
                   + l["heures_de_travail_h"]
                   * l["en_plus_a_la_charge_du_locataire_MAD_h"])) < 2,
            f"{l['cout_sur_le_chantier_MAD']:,} MAD".replace(",", " "))
    verifie(f"{l['cle']} : la ligne publie ce que son prix comprend",
            l["le_prix_comprend"] == FAM[l["cle"]]["location"].get("comprend", []))
    verifie(f"{l['cle']} : le cout par heure de TRAVAIL est le cout / les heures",
            abs(l["cout_par_heure_de_travail_MAD"]
                - l["cout_sur_le_chantier_MAD"] / l["heures_de_travail_h"]) < 0.5,
            f"{l['cout_par_heure_de_travail_MAD']} MAD/h")
verifie("le total est la somme des lignes",
        abs(cp["total_sur_le_chantier_MAD"]
            - sum(l["cout_sur_le_chantier_MAD"] for l in cp["lignes"])) < 2)
verifie("la seule ligne absente du bordereau de D1 est celle dont aucune ressource "
        "ne porte le prix",
        cp["lignes_absentes_du_bordereau"] == [FAM["chariot"]["nom"]]
        and abs(cp["montant_absent_du_bordereau_MAD"]
                - next(l["cout_sur_le_chantier_MAD"] for l in cp["lignes"]
                       if l["cle"] == "chariot")) < 2)
verifie("le montant absent se compare au poste qui devrait l'absorber, et le depasse",
        cp["montant_de_ce_poste_MAD"]
        == prix["bordereau"]["frais_de_duree"]["lignes"]["energie_et_divers"]["montant_MAD"]
        and cp["part_du_poste_consommee_pct"] > 100,
        f"{cp['part_du_poste_consommee_pct']} % du poste")
verifie("et la LIMITE est publiee avec le nombre : un forfait peut le porter sans "
        "le montrer",
        dit(cp["_limite"], "forfait", "visible")
        and cp["nb_postes_au_forfait"] == sum(
            1 for x in prix["bordereau"]["postes"] if x["type"] == "forfait"))
dv = cp["pompe_deux_voies"]
verifie("les deux voies de la pompe sont comparees, et l'ecart est explique",
        abs(dv["rapport"] - dv["voie_C6_aux_interventions_j"] / dv["voie_D1_au_volume_j"])
        < 0.01 and dit(dv["pourquoi"], "venue", "metre cube"),
        f"x{dv['rapport']}")
verifie("l'ecart en MAD est le nombre de jours d'ecart au prix du bordereau",
        abs(dv["ecart_MAD"] - (dv["voie_C6_aux_interventions_j"] - dv["voie_D1_au_volume_j"])
            * val(MAT["pompe_a_beton_j"])) < 2, f"{dv['ecart_MAD']:,} MAD".replace(",", " "))

# ------------------------------------------------------- 6. catalogue contre reel
print("\n--- du catalogue au debit reel ---")
rp = r["rendement_de_la_pompe"]
R = M["rendement_de_la_pompe"]
courant = val(R["debit_catalogue_m3_h"])
verifie("la premiere etape est le debit catalogue, sans facteur",
        abs(rp["etapes"][0]["debit_m3_h"] - courant) < 0.05
        and rp["etapes"][0]["facteur"] is None)
for e in rp["etapes"][1:]:
    courant *= e["facteur"]
    verifie(f"etape « {e['etape'][:28]} » : le debit est le precedent x son facteur",
            abs(e["debit_m3_h"] - courant) < 0.1, f"{e['debit_m3_h']} m3/h")
verifie("le produit des facteurs est le produit des trois facteurs declares",
        abs(rp["produit_des_facteurs"]
            - val(R["facteur_pompabilite"]) * val(R["part_de_l_heure_pompee"])
            * val(R["facteur_arrets"])) < 1e-6, f"{rp['produit_des_facteurs']}")
verifie("le catalogue perd plus du tiers de son debit en route",
        rp["perte_catalogue_pct"] > 33, f"{rp['perte_catalogue_pct']} %")
verifie("l'ecart avec la valeur que C3 declare tient sous la tolerance de 5 % du § 3.3",
        rp["ecart_sous_tolerance_5pct"] and rp["dans_la_fourchette"],
        f"{rp['ecart_pct']} %")
verifie("le debit declare par C3 est LU, non redeclare ici",
        rp["debit_declare_par_C3_m3_h"]
        == val(d["gros_oeuvre"]["betonnage_temps_chaud"]["debit_pompe_m3_h"])
        and not any("debit" in k for k in M))
verifie("le debit recalcule reste au-dessus du plancher anti-reprise de C3",
        rp["debit_recalcule_m3_h"] > rp["plancher_anti_reprise_m3_h"],
        f"{rp['debit_recalcule_m3_h']} contre {rp['plancher_anti_reprise_m3_h']} m3/h")
verifie("le debit tenu au chantier est celui que C3 publie, et il est borne par "
        "l'approvisionnement, pas par l'engin",
        rp["debit_tenu_au_chantier_m3_h"]
        == go["betonnage"]["option_retenue"]["debit_tenu_m3_h"]
        and dit(rp["ce_qui_borne_le_coulage"], "toupie"))

# ------------------------------------------------------- 7. la chaine
print("\n--- la chaine est un produit ---")
c = r["chaine_du_coulage"]
ps = [m["disponibilite_pct"] / 100 for m in c["maillons"]]
prod = math.prod(ps)
verifie("la disponibilite de la chaine est le produit des maillons",
        abs(c["disponibilite_forme_fermee_pct"] - prod * 100) < 0.05,
        f"{c['disponibilite_forme_fermee_pct']} %")
verifie("la simulation directe retrouve la forme fermee",
        c["ecart_des_deux_voies_points"] < 0.6
        and abs(c["disponibilite_simulee_pct"]
                - c["disponibilite_forme_fermee_pct"]) < 0.6,
        f"{c['disponibilite_simulee_pct']} % simules")
verifie("la chaine est strictement sous son maillon le plus faible",
        c["disponibilite_forme_fermee_pct"] < c["maillon_le_plus_faible_pct"]
        and abs(c["ecart_avec_le_maillon_le_plus_faible_points"]
                - (c["maillon_le_plus_faible_pct"]
                   - c["disponibilite_forme_fermee_pct"])) < 0.15)
verifie("la pompe porte UNE disponibilite, la meme dans la famille et dans la chaine",
        next(m["disponibilite_pct"] for m in c["maillons"] if "ompe" in m["element"])
        == val(FAM["pompe"]["disponibilite_pct"]))
verifie("le nombre de coulages derangeables est lu sur les zones que C3 calcule",
        c["coulages_derangeables_sur"] == go["cycle"]["nb_zones"]
        and abs(c["coulages_derangeables"]
                - (1 - prod) * go["cycle"]["nb_zones"]) < 0.1)
verifie("le cout d'un jour perdu est lu dans D1, et c'est le frais de duree SEUL",
        c["cout_d_un_jour_perdu_MAD"]
        == prix["cout_du_retard"]["1"]["frais_de_duree_MAD"]
        and c["cout_d_un_jour_perdu_MAD"] < prix["cout_du_retard"]["1"]["total_MAD"]
        and dit(c["perimetre_du_jour_perdu"], "penalite", "perimetre"))
for s in c["secours"]:
    if not s["possible"]:
        verifie(f"secours impossible sur « {s['element'][:24]} » : la raison est ecrite",
                len(s["pourquoi"]) > 40)
        continue
    p0 = s["disponibilite_pct"] / 100
    verifie(f"secours sur « {s['element'][:24]} » : 1 − (1 − p)^2",
            abs(s["avec_secours_pct"] / 100 - (1 - (1 - p0) ** 2)) < 1e-6)
    verifie(f"« {s['element'][:24]} » : le gain de chaine est positif et borne",
            0 < s["gain_en_points_de_chaine"] < 100 - c["disponibilite_forme_fermee_pct"])
    verifie(f"« {s['element'][:24]} » : l'esperance est le gain x le jour perdu",
            abs(s["esperance_de_gain_par_coulage_MAD"]
                - s["gain_en_points_de_chaine"] / 100
                * c["cout_d_un_jour_perdu_MAD"]) < 1)
    verifie(f"« {s['element'][:24]} » : « rentable » compare l'esperance au prix",
            s["rentable"] == (s["esperance_de_gain_par_coulage_MAD"]
                              > s["cout_du_secours_par_coulage_MAD"]))
    verifie(f"« {s['element'][:24]} » : le MAD par point de chaine est le prix / le gain",
            abs(s["MAD_par_point_de_chaine"]
                - s["cout_du_secours_par_coulage_MAD"]
                / s["gain_en_points_de_chaine"]) < 0.5,
            f"{s['MAD_par_point_de_chaine']} MAD/point")
    verifie(f"« {s['element'][:24]} » : les deux montants sont PAR COULAGE, et l'unite "
            f"est ecrite",
            dit(s["_unite"], "par coulage"))
verifie("le secours le plus RENTABLE n'est pas celui qui gagne le plus de points, "
        "et le module publie les deux",
        c["le_plus_rentable_n_est_pas_le_plus_gros_gain"]
        and c["secours_le_plus_rentable"] != c["secours_au_plus_gros_gain"],
        f"{c['secours_le_plus_rentable']} contre {c['secours_au_plus_gros_gain']}")
verifie("et le plus rentable est le moins cher au point de chaine",
        min((s for s in c["secours"] if s["possible"]),
            key=lambda s: s["MAD_par_point_de_chaine"])["element"]
        == c["secours_le_plus_rentable"])

# ------------------------------------------------- l'indisponibilite, qui LIT les dispos
print("\n--- la disponibilite de chaque engin, et ce qu'elle coute ---")
IN = r["indisponibilite"]
for l in IN["lignes"]:
    e, f = EMP[l["cle"]], FAM[l["cle"]]
    verifie(f"{l['cle']} : la disponibilite LUE est celle que data/ declare",
            l["disponibilite_pct"] == val(f["disponibilite_pct"]))
    verifie(f"{l['cle']} : les jours perdus esperes sont les jours de travail x (1 - p)",
            abs(l["jours_perdus_esperes_j"]
                - e["jours_de_travail_j"] * (1 - l["disponibilite_pct"] / 100)) < 0.1,
            f"{l['jours_perdus_esperes_j']} j")
    verifie(f"{l['cle']} : la marge retenue est la PLUS FAIBLE de ses taches",
            abs(l["marge_la_plus_faible_des_taches_j"]
                - min(pl["durees"][t]["marge_totale_j"] for t in e["taches"])) < 0.01)
    verifie(f"{l['cle']} : le cout en delai n'existe que si la perte deborde la marge",
            (l["cout_en_delai_MAD"] == 0) == l["la_perte_tient_dans_la_marge"]
            and (l["la_perte_tient_dans_la_marge"]
                 == (l["jours_perdus_esperes_j"]
                     <= l["marge_la_plus_faible_des_taches_j"])))
    verifie(f"{l['cle']} : les taches critiques servies sont celles que D2 marque "
            f"critiques",
            l["taches_critiques_servies"]
            == [t for t in e["taches"] if pl["durees"][t]["critique"]])
verifie("LE RESULTAT : la seule disponibilite qui coute un delai est celle de l'engin "
        "qui sert des taches sans marge",
        IN["nb_familles_dont_la_panne_coute_un_delai"] == 1
        and next(l["cle"] for l in IN["lignes"]
                 if not l["la_perte_tient_dans_la_marge"]) == "chariot"
        and next(l["taches_critiques_servies"] for l in IN["lignes"]
                 if l["cle"] == "chariot"),
        f"{next(l['cout_en_delai_MAD'] for l in IN['lignes'] if l['cle'] == 'chariot'):,} MAD".replace(",", " "))
verifie("et le jour de chantier est lu dans D1, non recalcule",
        IN["cout_d_un_jour_de_chantier_MAD"]
        == prix["cout_du_retard"]["1"]["frais_de_duree_MAD"])
verifie("aucune hypothese declaree du bloc n'est desormais sans lecteur : les trois "
        "disponibilites alimentent un resultat",
        all(any(abs(l["disponibilite_pct"] - val(FAM[c]["disponibilite_pct"])) < 1e-9
                for l in IN["lignes"] if l["cle"] == c) for c in FAM))

# ------------------------------------------------------- 8. mutualiser
print("\n--- mutualiser deplace l'emploi, pas le cout fixe ---")
mu = r["mutualisation"]
k = val(M["mutualisation"]["besoin_relatif_du_second_site"])
perte = val(M["mutualisation"]["perte_de_mutualisation_pct"]) / 100
verifie("le facteur d'emploi ajoute le second site et retranche la perte",
        abs(mu["facteur_d_emploi"] - (1 + k) * (1 - perte)) < 0.005
        and abs(mu["sites_equivalents_mutualises"] - (1 + k) * (1 - perte)) < 0.01,
        f"x{mu['facteur_d_emploi']}")
for l in mu["lignes"]:
    f = FAM[l["cle"]]
    if f["regime_de_location"] == "par_duree_de_presence":
        verifie(f"{l['cle']} : paye a la presence, la mutualisation multiplie ses "
                f"heures mais pas sa facture",
                abs(l["heures_par_an_mutualisees_h"]
                    - l["heures_par_an_seul_h"] * mu["facteur_d_emploi"]) < 1)
    else:
        verifie(f"{l['cle']} : la mutualisation multiplie l'emploi par le facteur",
                abs(l["heures_par_an_mutualisees_h"]
                    - l["heures_par_an_seul_h"] * mu["facteur_d_emploi"]) < 1)
    verifie(f"{l['cle']} : le seuil ne bouge pas, c'est l'emploi qui bouge",
            l["seuil_h_par_an"] == VER[l["cle"]]["equilibre"]["seuil_h_par_an"])
    verifie(f"{l['cle']} : le rapport d'emploi a atteindre est le seuil / l'emploi seul",
            l["sites_equivalents_pour_atteindre_le_seuil"] is None
            or abs(l["sites_equivalents_pour_atteindre_le_seuil"]
                   - l["seuil_h_par_an"] / l["heures_par_an_seul_h"]) < 0.02,
            f"x{l['sites_equivalents_pour_atteindre_le_seuil']} d'emploi")
    verifie(f"{l['cle']} : et le NOMBRE DE SITES est l'inversion du facteur, donc plus "
            f"grand que ce rapport",
            l["nb_sites_equivalents"] is None
            or (l["nb_sites_equivalents"]
                > l["sites_equivalents_pour_atteindre_le_seuil"]
                and abs((1 + (l["nb_sites_equivalents"] - 1) * k) * (1 - perte)
                        - l["sites_equivalents_pour_atteindre_le_seuil"]) < 0.02),
            f"{l['nb_sites_equivalents']} sites")
    verifie(f"{l['cle']} : la distinction des deux nombres est ECRITE",
            dit(l["_ce_que_compte_ce_nombre"], "rapport", "sites"))
verifie("deux sites ne font pas deux : la perte de transfert est comptee",
        mu["sites_equivalents_mutualises"] < 1 + k)
verifie("et deux sites ne changent AUCUN verdict : la mutualisation n'aide que "
        "l'engin deja proche de son equilibre",
        mu["nb_bascules"] == 0
        and all(l["sites_equivalents_pour_atteindre_le_seuil"]
                > mu["sites_equivalents_mutualises"]
                for l in mu["lignes"]
                if l["sites_equivalents_pour_atteindre_le_seuil"]
                and l["verdict_seul"] == "LOUER"))
verifie("mutualiser un engin paye a la PRESENCE et loue NU ne change RIEN : son ecart "
        "ne depend pas des heures",
        not any(l["la_mutualisation_degrade_la_possession"] for l in mu["lignes"])
        and abs(next(l["ecart_mutualise_MAD_an"] for l in mu["lignes"]
                     if l["cle"] == "chariot") - VER["chariot"]["ecart_MAD_an"]) < 2
        and dit(mu["_hypothese_de_fenetre"], "fenetre", "deja payee"))
verifie("la pompe est celle qui en aurait le plus besoin, et de tres loin",
        max((l for l in mu["lignes"]
             if l["sites_equivalents_pour_atteindre_le_seuil"]), key=lambda l:
            l["sites_equivalents_pour_atteindre_le_seuil"])["cle"] == "pompe",
        f"{next(l['sites_equivalents_pour_atteindre_le_seuil'] for l in mu['lignes'] if l['cle'] == 'pompe')} sites")

# ------------------------------------------------------- 9. aucun doublon
print("\n--- aucun doublon avec C1, C3 et D2 ---")
verifie("la grue a tour n'est pas une famille de C6 : elle appartient a C1",
        not any("grue" in f["cle"] or "grue" in sansaccent(f["nom"])
                for f in M["familles"]))
verifie("le parc de coffrage n'est pas une famille de C6 : il appartient a C3",
        not any("coffrage" in sansaccent(f["nom"]) for f in M["familles"])
        and "location_MAD_m2_mois" in d["gros_oeuvre"]["coffrage"])
verifie("et le module l'ecrit, au lieu de laisser le lecteur le deviner",
        dit(M["_familles_note"], "C1", "C3", "deux fois"))
verifie("aucune cadence de betonnage n'est redeclaree ici",
        not any("betonnage" in k for k in M))

# ------------------------------------------------------- 10. canaris
print("\n--- canaris : sept erreurs qu'un calcul juste doit refuser ---")
# 1. prendre le MINIMUM des disponibilites au lieu du produit
faux = min(ps)
verifie("canari : « la chaine vaut son maillon le plus faible » divise par deux "
        "les coulages deranges",
        (1 - faux) * go["cycle"]["nb_zones"] < c["coulages_derangeables"] / 2,
        f"{(1 - faux) * go['cycle']['nb_zones']:.1f} contre "
        f"{c['coulages_derangeables']:.1f} coulages")
# 2. choisir le secours sur le plus gros gain de chaine
gros = next(s for s in c["secours"] if s["element"] == c["secours_au_plus_gros_gain"])
verifie("canari : choisir le secours au plus gros gain prend celui qui n'est PAS "
        "rentable",
        not gros["rentable"] and gros["rapport_gain_sur_cout"] < 1,
        f"{gros['element']} : rapport {gros['rapport_gain_sur_cout']}")
# 3. oublier la valeur residuelle
par = ch.parametres(d, FAM["chariot"], "nominal")
e0 = EMP["chariot"]
sans_res = ch.couts_annuels({**par, "residuelle": 0.0},
                            e0["_heures_par_an_exact"], e0["_unites_par_an_exact"])
verifie("canari : oublier la valeur residuelle alourdit la possession",
        sans_res["ecart_MAD_an"] > VER["chariot"]["ecart_MAD_an"],
        f"{sans_res['ecart_MAD_an']:.0f} contre "
        f"{VER['chariot']['ecart_MAD_an']:.0f} MAD/an")
# 4. facturer le chariot a ses jours de TRAVAIL au lieu de sa PRESENCE
faux_loc = ch.couts_annuels(
    par, e0["_heures_par_an_exact"],
    e0["jours_de_travail_j"] / e0["_fenetre_ans_exact"])
verifie("canari : facturer le chariot a ses jours de travail au lieu de sa presence "
        "inverse le verdict",
        (faux_loc["ecart_MAD_an"] < 0) != (VER["chariot"]["ecart_MAD_an"] < 0),
        f"{faux_loc['ecart_MAD_an']:.0f} contre "
        f"{VER['chariot']['ecart_MAD_an']:.0f} MAD/an")
# 5. facturer la pompe a ses jours de tache au lieu de ses interventions
pp = ch.parametres(d, FAM["pompe"], "nominal")
epp = EMP["pompe"]
faux_pompe = ch.couts_annuels(pp, epp["_heures_par_an_exact"],
                              epp["jours_de_travail_j"] / epp["_fenetre_ans_exact"])
verifie("canari : facturer la pompe a ses jours de tache au lieu de ses interventions "
        "la rend plus de deux fois plus chere qu'elle n'est",
        faux_pompe["location_MAD_an"] > 2 * VER["pompe"]["location_MAD_an"],
        f"{faux_pompe['location_MAD_an']:,.0f} contre "
        f"{VER['pompe']['location_MAD_an']:,.0f} MAD/an".replace(",", " "))
# 6. compter les heures sur la FENETRE au lieu des jours de travail
for cle in ("chariot", "pelle"):
    e = EMP[cle]
    h_fenetre = (e["fenetre_duree_j"] * e["heures_par_jour_servi_h"]
                 / e["_fenetre_ans_exact"])
    verifie(f"canari {cle} : compter la presence au lieu du travail gonfle l'emploi "
            f"d'un facteur {h_fenetre / e['heures_par_an_h']:.1f}",
            h_fenetre >= e["heures_par_an_h"],
            f"{h_fenetre:.0f} contre {e['heures_par_an_h']:.0f} h/an")
# 7. convertir la fenetre avec les jours ouvres du MOIS. L'erreur ne gonfle pas
# l'emploi : elle le DIVISE par 250/21, soit 11,9 — la fenetre compte alors 26
# « annees » au lieu de 2,2. Un engin paraitrait douze fois moins employe, et la
# location gagnerait toujours. Le premier libelle de ce canari disait « multiplie »,
# et c'etait une phrase fausse a cote d'un nombre juste.
mois = val(d["prix_unitaires_MAD"]["ressources"]["jours_ouvres_par_mois"])
faux_h = (e0["jours_de_travail_j"] * e0["heures_par_jour_servi_h"]
          / (e0["fenetre_duree_j"] / mois))
# L'erreur ne gonfle pas l'emploi : elle le DIVISE par 250/21, soit 11,9 — la fenetre
# compte alors 26 « annees » au lieu de 2,2. Sur le chariot, dont l'ecart ne depend plus
# des heures, elle ne change pas le verdict ; sur la POMPE et la PELLE, dont le seuil se
# compare a l'emploi, elle le ferme dans le mauvais sens.
verifie("canari : convertir la fenetre avec les jours ouvres du MOIS divise l'emploi "
        "par 11,9",
        abs(e0["heures_par_an_h"] / faux_h - joa / mois) < 0.05,
        f"{faux_h:.0f} au lieu de {e0['heures_par_an_h']:.0f} h/an, facteur "
        f"{joa / mois:.1f}")
verifie("canari : et sur la pelle, dont le seuil se compare a l'emploi, elle eloigne "
        "encore la possession d'un seuil deja hors d'atteinte",
        EMP["pelle"]["heures_par_an_h"] / (joa / mois)
        < VER["pelle"]["equilibre"]["seuil_h_par_an"],
        f"{EMP['pelle']['heures_par_an_h'] / (joa / mois):.0f} h/an contre "
        f"{VER['pelle']['equilibre']['seuil_h_par_an']} de seuil")

print()
if echecs:
    print(f"ECHEC : {len(echecs)} controle(s) — {', '.join(echecs[:4])}")
    sys.exit(1)
print("Tests cout horaire : tous verts.")
