"""Qualite, HSE, environnement : ce qui rend la securite pilotable (C7).

Ce module ne cite aucune valeur reglementaire — ni frequence de prelevement, ni critere
de resistance, ni distance de securite. Il calcule ce qui n'en depend pas, et c'est
exactement ce qu'un chef de projet suivi manipule tous les jours :

1. L'EXPOSITION se compte en HEURES, jamais en effectif. C'est le denominateur de tous
   les indicateurs de securite, et c'est ce qui permet de comparer deux chantiers. Le
   cours connait desormais ses heures exactement — D1 et D2 les trouvent identiques,
   tache par tache — ce qui rend le calcul possible et verifiable.
2. Le COUT D'UNE NON-CONFORMITE n'est pas le cout de sa reprise. C'est la reprise, plus
   l'attente de la decision, plus le decalage mesure sur le reseau, plus le
   durcissement du controle sur tout ce qui suit.
3. La CRITICITE d'un risque est un produit d'echelles ORDINALES : elle sert a classer,
   jamais a chiffrer. Multiplier des rangs ne produit pas une grandeur — c'est la meme
   faute de domaine que D-037 denonce ailleurs, et elle est universelle dans les
   analyses de risques.
"""
from __future__ import annotations
import json, math, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import planification as pln                                              # noqa: E402


# ---------------------------------------------------- 1. l'exposition, en heures
def exposition(d: dict, pl: dict) -> dict:
    """Les heures travaillees, et comment elles se repartissent entre jour et nuit.

    Un indicateur de securite se rapporte TOUJOURS a des heures. Le piege est de le
    rapporter a un effectif ou a une duree : deux chantiers de meme effectif n'exposent
    pas leurs compagnons autant si l'un travaille six mois et l'autre deux ans, et deux
    chantiers de meme duree n'exposent pas autant si l'un a dix compagnons et l'autre
    cent. Les heures sont la seule assiette qui absorbe les deux.
    """
    e = d["qualite_hse"]["exposition"]
    h = pl["heures_de_main_oeuvre_par_tache"]
    nuit = set(d["planning"]["contraintes_exploitation"]["taches_soumises"])
    h_nuit = sum(v for i, v in h.items() if i in nuit)
    h_jour = sum(v for i, v in h.items() if i not in nuit)
    total = h_nuit + h_jour
    tf = e["taux_de_frequence_reference"]["valeur"]
    tg = e["taux_de_gravite_reference"]["valeur"]
    k = e["surexposition_du_travail_de_nuit"]["valeur"]
    # Heures ponderees par le risque : une heure de nuit "pese" k heures de jour.
    h_pond = h_jour + k * h_nuit
    accidents = tf * h_pond / 1e6
    return {
        "heures_totales": round(total, 1),
        "heures_de_jour": round(h_jour, 1),
        "heures_de_nuit": round(h_nuit, 1),
        "part_de_nuit_pct": round(h_nuit / total * 100, 2),
        "taches_de_nuit": sorted(nuit),
        "coefficient_de_surexposition_de_nuit": k,
        "heures_ponderees_par_le_risque": round(h_pond, 1),
        "part_de_nuit_dans_le_risque_pct": round(k * h_nuit / h_pond * 100, 2),
        "taux_de_frequence_de_reference": tf,
        "taux_de_gravite_de_reference": tg,
        "accidents_avec_arret_attendus": round(accidents, 2),
        "journees_perdues_attendues": round(tg * h_pond / 1000, 1),
        "lecture": (
            f"Le chantier represente {total:,.0f} heures travaillees, dont "
            f"{h_nuit:,.0f} de nuit sous interception — {h_nuit / total * 100:.1f} % des "
            f"heures. Mais une heure de nuit expose {k} fois plus : elle pese "
            f"{k * h_nuit / h_pond * 100:.1f} % du risque. C'est le premier resultat de "
            "ce module, et il ne se voit sur aucun effectif."
        ).replace(",", " "),
        "_ce_que_le_nombre_d_accidents_n_est_pas": (
            "Ce n'est PAS une prevision, et encore moins un objectif : c'est ce qu'un "
            "taux de reference APPLIQUE a ces heures donnerait. Il sert a dimensionner "
            "— combien de secouristes, quelle organisation des secours, quel budget de "
            "prevention — et a comparer. Annoncer « nous aurons 1,6 accident » serait "
            "aussi faux que d'annoncer qu'on n'en aura aucun."),
        "_pourquoi_pas_l_effectif": (
            "Un effectif ne dit rien de l'exposition : dix compagnons pendant deux ans "
            "et cent pendant deux mois n'ont ni le meme risque ni le meme nombre "
            "d'heures. Piloter la securite sur un effectif, c'est la meme faute que "
            "piloter un avancement sur un pourcentage sans denominateur (module D4)."),
        "par_tache": sorted(
            ({"tache": i, "heures": round(v, 1),
              "de_nuit": i in nuit,
              "part_des_heures_pct": round(v / total * 100, 1),
              "part_du_risque_pct": round((k if i in nuit else 1) * v / h_pond * 100, 1)}
             for i, v in h.items() if v > 0),
            key=lambda x: -x["part_du_risque_pct"]),
    }


# ---------------------------------------------------- 2. le cout d'une non-conformite
def cout_de_la_non_conformite(d: dict, pl: dict, pr: dict) -> dict:
    """Ce qu'une NC coute vraiment, et ou est l'argent.

    Le reflexe est de chiffrer la reprise. La reprise est en general la plus petite des
    quatre lignes. Les trois autres — l'attente de la decision, le decalage du cycle, le
    durcissement du controle sur tout ce qui suit — ne figurent sur aucun devis de
    reprise, et c'est pourquoi le cout d'une NC est systematiquement sous-estime.
    """
    nc = d["qualite_hse"]["non_conformite"]
    v = {k: nc[k]["valeur"] for k in nc if isinstance(nc[k], dict) and "valeur" in nc[k]}
    fd = pr["bordereau"]["frais_de_duree"]["cout_MAD_par_jour_ouvre"]
    taux = d["prix_unitaires_MAD"]["postes"]["main_oeuvre_h"]["valeur"]

    reprise = v["surface_m2"] * v["cout_de_reprise_MAD_m2"]
    jours_immobilises = v["delai_de_decision_j"] + v["duree_de_reprise_j"]
    # Le durcissement du controle porte sur les levees RESTANTES, pas sur celle qui a
    # fait defaut : une NC coute aussi sur les ouvrages qui n'en ont pas.
    h_sup = (v["heures_de_controle_par_levee"] * v["durcissement_du_controle_pct"] / 100
             * v["levees_restantes"])
    controle = h_sup * taux

    lignes = [
        {"poste": "Reprise du parement", "montant_MAD": round(reprise, 2),
         "visible_sur_un_devis": True,
         "note": f"{v['surface_m2']:.0f} m² à {v['cout_de_reprise_MAD_m2']:.0f} MAD/m²"},
        {"poste": "Attente de la décision", "montant_MAD": round(
            v["delai_de_decision_j"] * fd, 2), "visible_sur_un_devis": False,
         "note": f"{v['delai_de_decision_j']:.0f} j entre le constat et l'ordre de "
                 "reprise : expertise, avis du BET, accord sur la méthode"},
        {"poste": "Durée de la reprise", "montant_MAD": round(
            v["duree_de_reprise_j"] * fd, 2), "visible_sur_un_devis": False,
         "note": f"{v['duree_de_reprise_j']:.0f} j d'intervention et de séchage avant "
                 "reconstat"},
        {"poste": "Durcissement du contrôle", "montant_MAD": round(controle, 2),
         "visible_sur_un_devis": False,
         "note": f"+{v['durcissement_du_controle_pct']:.0f} % de temps de contrôle sur "
                 f"les {v['levees_restantes']:.0f} levées restantes, soit {h_sup:.1f} h"},
    ]
    total = sum(x["montant_MAD"] for x in lignes)
    visible = sum(x["montant_MAD"] for x in lignes if x["visible_sur_un_devis"])
    return {
        "ouvrage": nc["ouvrage"],
        "lignes": lignes,
        "total_MAD": round(total, 2),
        "part_visible_sur_un_devis_MAD": round(visible, 2),
        "part_visible_pct": round(visible / total * 100, 1),
        "jours_immobilises": jours_immobilises,
        "frais_de_duree_MAD_par_jour_ouvre": fd,
        "_source_des_frais": "calc/sorties/prix.json — bordereau.frais_de_duree",
        "lecture": (
            f"La reprise coute {reprise:,.0f} MAD. La non-conformite en coute "
            f"{total:,.0f}. L'ecart — {total - reprise:,.0f} MAD, soit "
            f"{(total - reprise) / total * 100:.0f} % du total — ne figure sur aucun "
            "devis de reprise : c'est du temps de chantier et du temps de controle."
        ).replace(",", " "),
        "ce_qui_n_est_PAS_chiffre_ici": (
            "Le decalage du cycle n'est chiffre ici qu'en frais de duree, et seulement "
            "si l'ouvrage est sur le chemin critique — ce qui se MESURE en rejouant le "
            "reseau, pas en le supposant. N'y figurent pas non plus : la perte de "
            "confiance de la maitrise d'oeuvre, qui durcit tous les visas suivants et "
            "qu'on ne sait pas chiffrer, ni le risque que la reprise elle-meme soit "
            "refusee. Un cout de NC publie est toujours une borne basse."),
        "_le_piege": (
            "Negocier le prix de la reprise au dirham pres pendant que l'attente de la "
            "decision coute chaque jour davantage. Le poste le plus cher d'une NC est "
            "souvent celui que personne ne pilote, parce qu'il n'a pas de facture."),
    }


def impact_sur_le_planning(d: dict, jours: float) -> dict:
    """Le decalage se MESURE en rejouant le reseau (D-040), il ne se suppose pas.

    Une NC sur un ouvrage a marge ne decale rien ; la meme NC sur un ouvrage a marge
    nulle decale tout le chantier. La difference ne se devine pas : les deux ouvrages se
    ressemblent sur le chantier, et c'est le reseau — pas la gravite du defaut — qui dit
    laquelle des deux non-conformites il faut traiter toutes affaires cessantes.

    Les trois taches comparees ne sont pas choisies a la main : on prend celle qui n'a
    AUCUNE marge, celle qui en a le moins parmi les autres, et celle qui en a le plus.
    Les ecrire en dur les aurait figees, et le classement change des que le planning
    change — ce qui vient precisement d'arriver.
    """
    import copy
    tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json")
                    .read_text(encoding="utf-8"))
    q = pln.quantites_chantier(d, d["planning"])
    t0 = pln.durees_chantier(d, d["planning"], q, tv["planning_plancher"]["duree_totale_j"])
    f0 = pln.planning_avec_fenetres(d, t0)
    res0 = pln.voie_A_parcours(f0["taches"])
    ref = res0["duree"]
    mg = pln.marges(res0, t0, pln.liens_resolus(d, t0))
    # taches reellement exposees a une NC d'execution : celles qui ont un effectif
    candidates = [i for i in mg if t0[i]["duree_j"] > 0.5]
    candidates.sort(key=lambda i: mg[i]["marge_totale_j"])
    choix, vus = [], set()
    for i in (candidates[0], candidates[1], candidates[-1]):
        if i not in vus:
            vus.add(i)
            choix.append(i)

    out = []
    for tache in choix:
        t = {k: dict(v) for k, v in t0.items()}
        t[tache]["duree_j"] = round(t[tache]["duree_j"] + jours, 2)
        f = pln.planning_avec_fenetres(d, t)
        res = pln.voie_A_parcours(f["taches"])
        out.append({
            "tache": tache, "nom": pln.NOMS[tache],
            "marge_totale_j": round(mg[tache]["marge_totale_j"], 2),
            "retard_du_chantier_j": round(max(0.0, res["duree"] - ref), 2),
            "absorbee_par_la_marge": bool(res["duree"] - ref < 0.01),
        })
    pires = [x for x in out if not x["absorbee_par_la_marge"]]
    return {
        "immobilisation_j": jours,
        "duree_de_reference_j": round(ref, 2),
        "lignes": out,
        "lecture": (
            f"La MEME non-conformite, {jours:.0f} jours d'immobilisation, decale le "
            "chantier de "
            + ", ".join(f"{x['retard_du_chantier_j']:.1f} j sur {x['tache']} "
                        f"(marge {x['marge_totale_j']:.1f} j)" for x in out)
            + ". Ce n'est pas la gravite du defaut qui fait la difference, c'est la "
            "MARGE de l'ouvrage — et elle ne se lit pas sur le chantier."),
        "_ce_que_ce_chantier_montre_en_particulier": (
            "Depuis que le levage sous consignation domine le chemin critique, presque "
            "tous les ouvrages de gros oeuvre ont de la marge : une non-conformite y "
            "coute de l'argent et pas de delai. C'est une information de PILOTAGE, pas "
            "une permission — l'argent se depense quand meme, et la marge consommee "
            "n'est plus la pour l'alea suivant (module C3)."
            if not pires else
            "Les taches a marge nulle transmettent leur immobilisation integralement : "
            "une journee perdue y est une journee de chantier."),
        "_consequence_de_pilotage": (
            "Deux non-conformites de meme gravite technique n'ont pas la meme urgence. "
            "Celle qui touche un ouvrage a marge nulle se traite toutes affaires "
            "cessantes ; l'autre se traite bien. Un plan de controle qui ignore le "
            "planning fait l'inverse : il met le meme effort partout, donc trop peu la "
            "ou il faudrait — et il le met sur les ouvrages visibles plutot que sur les "
            "ouvrages contraints."),
    }


# ---------------------------------------------------- 3. la criticite, et son domaine
def criticite(d: dict) -> dict:
    """f x g x d sur des echelles ORDINALES : un classement, jamais une grandeur.

    C'est l'outil le plus utilise et le plus mal lu des analyses de risques. Les trois
    notes sont des RANGS : « 4 » n'est pas « deux fois 2 », c'est « plus que 3 ». Leur
    produit se compare donc a un autre produit — il classe — mais il ne s'interprete pas
    comme une magnitude, ne s'additionne pas, ne se moyenne pas, et sa variation n'a pas
    de sens quantitatif. Dire « la criticite a baisse de 30 % » n'a aucun contenu.

    Ce qu'il faut en garder : le classement est utile, et il suffit. Ce qui ne suffit
    pas, c'est le seuil — « on traite au-dessus de 24 » depend entierement du choix des
    echelles, et deux equipes avec deux echelles differentes ne traiteront pas les memes
    risques.
    """
    r = d["qualite_hse"]["risques"]
    lignes = []
    for x in r["liste"]:
        c = x["f"] * x["g"] * x["d"]
        lignes.append({**x, "criticite": c})
    lignes.sort(key=lambda x: (-x["criticite"], -x["g"]))
    for n, x in enumerate(lignes, 1):
        x["rang"] = n
    # La gravite seule donne un AUTRE classement : les deux se lisent ensemble.
    par_gravite = sorted(lignes, key=lambda x: (-x["g"], -x["f"]))
    desaccord = [x["risque"] for x in lignes[:3]
                 if x["risque"] not in {y["risque"] for y in par_gravite[:3]}]
    return {
        "echelle": r["echelle"],
        "lignes": lignes,
        "les_trois_premiers": [x["risque"] for x in lignes[:3]],
        "les_trois_plus_graves": [x["risque"] for x in par_gravite[:3]],
        "classements_en_desaccord": desaccord,
        "_ce_que_la_criticite_n_est_pas": (
            "Un produit de RANGS. « 4 » n'est pas deux fois « 2 » : c'est « plus que "
            "3 ». Le produit classe, il ne mesure pas. On ne l'additionne pas, on ne le "
            "moyenne pas, et « la criticite a baisse de 30 % » n'a aucun contenu. C'est "
            "la meme faute de domaine que D-037 denonce pour les ratios — avec une "
            "circonstance aggravante : ici le nombre a l'air d'une mesure."),
        "_le_seuil_est_arbitraire": (
            "« On traite au-dessus de 24 » depend entierement du choix des echelles. "
            "Deux equipes avec deux echelles differentes ne traiteront pas les memes "
            "risques, et aucune des deux n'aura tort. Le seuil se DECIDE et se consigne, "
            "il ne se deduit pas."),
        "ex_aequo_en_tete": [x["risque"] for x in lignes
                             if x["criticite"] == lignes[0]["criticite"]],
        "_ce_que_les_ex_aequo_disent": (
            f"{sum(1 for x in lignes if x['criticite'] == lignes[0]['criticite'])} "
            f"risques sur {len(lignes)} sont a egalite en tete. Ce n'est pas un defaut "
            "du tableau, c'est une propriete des echelles courtes : avec des notes de 1 "
            "a 4, le produit ne prend que peu de valeurs distinctes et le classement ne "
            "discrimine pas. Un outil qui met cinq risques au meme rang ne dit pas "
            "qu'ils sont equivalents — il dit qu'il ne sait pas les departager, et c'est "
            "alors a l'equipe de le faire, pas au tableau."),
        "risques_a_faible_gravite_mais_frequents": [
            x["risque"] for x in lignes if x["g"] <= 2 and x["f"] >= 3],
        "pourquoi_lire_aussi_la_gravite_seule": (
            "Un risque rare et detectable mais mortel se classe mal en criticite et se "
            "traite quand meme : on n'arbitre pas une vie contre un rang. Les deux "
            "classements se lisent ensemble, et c'est leur DESACCORD qui est "
            "interessant"
            + (f" — ici {', '.join(desaccord)} sort du trio de tete en criticite sans "
               "sortir de celui de la gravite." if desaccord
               else " — ici ils s'accordent sur le trio de tete, ce qui est confortable "
                    "et ne doit pas faire oublier de les comparer.")),
    }


# ---------------------------------------------------- 4. le plan de controle
def plan_de_controle(d: dict) -> dict:
    """Les cinq colonnes sans lesquelles une ligne de plan de controle ne se pilote pas.

    Et une sixieme information, qu'on n'y met presque jamais : le DELAI du resultat. Un
    controle dont le resultat arrive a 28 jours ne protege pas l'ouvrage qu'il mesure —
    il protege les suivants. C'est une difference de nature, pas de degre, et elle
    change ce qu'on fait du resultat.
    """
    p = d["qualite_hse"]["plan_de_controle"]
    lignes = list(p["lignes"])
    immediats = [x for x in lignes if x["delai_du_resultat_j"] == 0]
    differes = [x for x in lignes if x["delai_du_resultat_j"] > 0]
    critiques = [x for x in lignes if x["sur_le_chemin_critique"]]
    return {
        "lignes": lignes,
        "nb_controles": len(lignes),
        "nb_immediats": len(immediats),
        "nb_differes": len(differes),
        "nb_sur_le_chemin_critique": len(critiques),
        "delai_le_plus_long_j": max(x["delai_du_resultat_j"] for x in lignes),
        "controle_le_plus_differe": max(
            lignes, key=lambda x: x["delai_du_resultat_j"])["controle"],
        "les_cinq_colonnes": [
            "QUI controle — et s'il est independant de celui qui execute",
            "QUAND — avant, pendant, ou apres l'operation",
            "SUR QUEL CRITERE — mesurable, et ecrit avant le controle",
            "EN COMBIEN DE TEMPS le resultat arrive",
            "CE QUI SE PASSE si c'est non conforme — decide a l'avance",
        ],
        "la_regle": (
            "Une ligne de plan de controle sans ces cinq colonnes ne se pilote pas : "
            "elle se coche. Et la cinquieme est celle qu'on oublie — decider a froid ce "
            "qu'on fera d'une non-conformite evite de le decider a chaud, devant une "
            "toupie qui attend."),
        "controles_qui_ne_protegent_pas_leur_ouvrage": (
            f"{len(differes)} controle(s) sur {len(lignes)} rendent leur resultat apres "
            f"coup, dont « {max(lignes, key=lambda x: x['delai_du_resultat_j'])['controle']} » "
            f"a {max(x['delai_du_resultat_j'] for x in lignes)} jours. Ils ne protegent "
            "pas l'ouvrage qu'ils mesurent — celui-ci est deja construit — ils protegent "
            "les SUIVANTS. D'ou deux consequences : on ne les attend pas pour avancer, "
            "et on ne les traite pas comme des points d'arret."),
        "_le_cout_du_point_d_arret": (
            f"{len(critiques)} controles sur {len(lignes)} sont sur le chemin critique "
            "du cycle : leur duree est du delai, pas une formalite. Le module C3 l'a "
            "chiffre pour le visa de ferraillage."),
    }


# ---------------------------------------------------- 5. les dechets
def dechets(d: dict, pl: dict) -> dict:
    """Les flux, et celui qui pese le moins mais commande le plus."""
    dd = d["qualite_hse"]["dechets"]
    emprise = d["geometrie"]["emprise_m"][0] * d["geometrie"]["emprise_m"][1]
    lignes = []
    for f in dd["flux"]:
        kg = f["kg_m2"]["valeur"] * emprise
        lignes.append({"flux": f["flux"], "kg_m2": f["kg_m2"]["valeur"],
                       "tonnes": round(kg / 1000, 1),
                       "valorisation_pct": f["valorisation_pct"],
                       "tonnes_valorisees": round(kg * f["valorisation_pct"] / 100000, 1)})
    total = sum(x["tonnes"] for x in lignes)
    valo = sum(x["tonnes_valorisees"] for x in lignes)
    dang = next(x for x in lignes if "dangereux" in x["flux"])
    return {
        "emprise_m2": emprise, "lignes": lignes,
        "total_tonnes": round(total, 1),
        "valorisees_tonnes": round(valo, 1),
        "taux_de_valorisation_pct": round(valo / total * 100, 1),
        "part_dangereuse_pct": round(dang["tonnes"] / total * 100, 2),
        "lecture": (
            f"{total:.0f} t de dechets, valorisees a {valo / total * 100:.0f} %. Les "
            f"dechets dangereux pesent {dang['tonnes']:.1f} t, soit "
            f"{dang['tonnes'] / total * 100:.2f} % du total — et ils commandent toute "
            "l'organisation du tri."),
        "_dangereux": dd["_dangereux"],
    }


# ---------------------------------------------------- figures
def figures(exp: dict, nc: dict, cr: dict, de: dict) -> dict:
    return {
        "exposition": [{"libelle": f"{x['tache']}{' · nuit' if x['de_nuit'] else ''}",
                        "valeur": x["heures"]}
                       for x in exp["par_tache"][:10]],
        "cout_nc": [{"libelle": x["poste"], "montant": x["montant_MAD"],
                     "type": "depart" if i == 0 else "hausse"}
                    for i, x in enumerate(nc["lignes"])]
                   + [{"libelle": "Coût réel", "montant": nc["total_MAD"], "type": "total"}],
        "criticite": [{"libelle": x["risque"][:46], "valeur": x["criticite"]}
                      for x in cr["lignes"]],
        "dechets": [{"libelle": x["flux"][:40], "valeur": x["tonnes"]}
                    for x in de["lignes"]],
    }


# ---------------------------------------------------- assemblage
def tout_calculer(d: dict) -> dict:
    pl = json.loads((RACINE / "calc" / "sorties" / "planification.json")
                    .read_text(encoding="utf-8"))
    pr = json.loads((RACINE / "calc" / "sorties" / "prix.json").read_text(encoding="utf-8"))
    exp = exposition(d, pl)
    nc = cout_de_la_non_conformite(d, pl, pr)
    cr = criticite(d)
    de = dechets(d, pl)
    return {
        "exposition": exp,
        "non_conformite": nc,
        "impact_planning": impact_sur_le_planning(d, nc["jours_immobilises"]),
        "criticite": cr,
        "plan_de_controle": plan_de_controle(d),
        "dechets": de,
        "figures": figures(exp, nc, cr, de),
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    r = tout_calculer(d)
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "qualite.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    e, n, c = r["exposition"], r["non_conformite"], r["criticite"]
    print(f"{e['heures_totales']:.0f} h dont {e['part_de_nuit_pct']} % de nuit, "
          f"qui pesent {e['part_de_nuit_dans_le_risque_pct']} % du risque")
    print(f"NC : reprise {n['lignes'][0]['montant_MAD']:.0f} MAD, cout reel "
          f"{n['total_MAD']:.0f} ({n['part_visible_pct']} % visible sur un devis)")
    for x in r["impact_planning"]["lignes"]:
        print(f"  {x['tache']} : {x['retard_du_chantier_j']} j de retard de chantier")
    print(f"criticite : 1er {c['lignes'][0]['risque'][:40]} ({c['lignes'][0]['criticite']})")
    print(f"dechets : {r['dechets']['total_tonnes']} t, "
          f"{r['dechets']['taux_de_valorisation_pct']} % valorisees")
