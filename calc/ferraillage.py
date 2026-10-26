"""Beton arme EN EXECUTION : lire un plan, le metrer, le controler (B3e).

Ce module ne dimensionne rien. La phase § 5.0 l'interdit, et ce n'est pas le metier du
lecteur : sur un chantier, le chef de projet suivi ne calcule pas le ferraillage, il
verifie que ce qui est pose est ce que le plan VISE montre. Ce que ce module calcule est
donc entierement non normatif :

1. Le METRE d'un plan de ferraillage, barre par barre : longueur developpee x masse
   lineique x nombre. La masse lineique est une constante physique (pi/4 d^2 rho), pas
   une valeur reglementaire : elle se recalcule et s'etalonne sur solution fermee.
2. Le meme metre par une SECONDE voie — le ratio kg/m3 — et l'ecart entre les deux. Un
   ratio ne verifie pas un metre, il le CADRE : il dit si l'ordre de grandeur tient.
3. Le passage du plan a la COMMANDE puis a ce qui est PAYE : recouvrements, chutes,
   ligatures. Trois nombres differents pour le meme ouvrage, et la premiere source de
   litige au decompte.
4. Le COMPTAGE des cadres, ou la difference entre un espacement nominal et un espacement
   pose se voit a l'unite pres.

Ce qui reste ⏸ : d'ou viennent les sections, les longueurs d'arret, les longueurs de
recouvrement et le resserrement des cadres. Ce sont des dispositions constructives
reglementaires. Le module le dit a chaque fois plutot que d'avancer un chiffre.
"""
from __future__ import annotations
import json, math, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "calc"))


# --------------------------------------------------------------- la brique de base
def masse_lineique_kg_m(dia_mm: float, rho_kg_m3: float = 7850.0) -> float:
    """Masse d'un metre de barre de diametre nominal donne.

        m = (pi / 4) x d^2 x rho

    C'est une grandeur GEOMETRIQUE et PHYSIQUE, pas une valeur normative : elle se
    recalcule, et le tableau du commerce (HA12 = 0,888 kg/m, HA20 = 2,466) en est la
    sortie arrondie. C'est la seule constante de ce module qui ne soit pas une hypothese,
    et c'est pour cela que le metre d'un plan est un calcul SUR, meme quand le plan,
    lui, n'est pas verifie.
    """
    return math.pi / 4 * (dia_mm / 1000.0) ** 2 * rho_kg_m3


def longueur_developpee_m(barre: dict) -> float:
    """Longueur de barre a facconner : partie droite + retours d'equerre.

    La partie droite n'est pas saisie : elle se LIT sur l'elevation, entre le point ou
    la barre commence et celui ou elle s'arrete. C'est la facon dont un metreur travaille
    sur un plan, et cela evite qu'une longueur de nomenclature et un trait d'elevation se
    contredisent — le controle n° 5 de la lecture d'un plan.

    Les CROCHETS d'extremite n'y sont pas : leur longueur est une valeur constructive
    reglementaire (⏸ § 5.0). Le metre est donc minorant, et `ecart_des_crochets` dit de
    combien. Ne jamais corriger un metre d'une valeur qu'on ne peut pas citer : on
    publie le minorant et on nomme ce qui manque.
    """
    if "positions" in barre:
        pos = barre["positions"][0]
        droit = pos["a_m"] - pos["de_m"]
        if any(abs((q["a_m"] - q["de_m"]) - droit) > 1e-9 for q in barre["positions"]):
            raise ValueError(
                f"{barre['repere']} : les positions n'ont pas toutes la meme longueur. "
                "Un repere, c'est une barre faconnee a une longueur ; deux longueurs "
                "differentes, ce sont deux reperes.")
    else:
        droit = float(barre.get("droit_m", 0.0))
    return droit + sum(barre.get("retours_m", []) or [])


def nombre_par_poutre(barre: dict) -> int:
    """Le nombre d'un repere est la somme de ses positions sur l'elevation."""
    if "positions" in barre:
        return sum(q["n"] for q in barre["positions"])
    return int(barre["n_par_poutre"])


# --------------------------------------------------------------- la poutre, barre par barre
def nomenclature_poutre(d: dict) -> dict:
    """Le metre d'une poutre se fait sur sa NOMENCLATURE : une ligne par repere.

    Une nomenclature de plan d'execution porte, pour chaque repere : le nombre, le
    diametre, la longueur unitaire developpee, la longueur totale et la masse. C'est le
    document que le ferrailleur faconne et que le suivi verifie — et c'est la seule piece
    du plan qui se controle sans savoir calculer une section.
    """
    a = d["armatures"]
    cv, p = a["conventions"], a["plan"]["poutre_PM1"]
    rho = cv["masse_volumique_acier_kg_m3"]
    Lc = cv["longueur_commerciale_m"]
    Lr = a["du_plan_a_la_commande"]["longueur_de_recouvrement_du_plan_m"]["valeur"]
    n_poutres = p["nb_dans_la_zone"]

    lignes = []
    for b in p["barres"]:
        Lu = longueur_developpee_m(b)
        # Une FILANTE plus longue que la barre commerciale se reconstitue par
        # recouvrement : ce n'est pas une disposition, c'est une contrainte de livraison.
        # Le nombre de recouvrements est geometrique ; seule leur LONGUEUR est ⏸.
        n_rec = math.ceil(Lu / Lc) - 1 if b.get("filante") else 0
        Lu_avec_rec = Lu + n_rec * Lr
        ml = masse_lineique_kg_m(b["dia_mm"], rho)
        n_tot = nombre_par_poutre(b) * n_poutres
        lignes.append({
            "repere": b["repere"], "role": b["role"], "lecture": b["_lecture"],
            "nombre": n_tot, "dia_mm": b["dia_mm"],
            "longueur_unitaire_m": round(Lu, 3),
            "recouvrements_par_barre": n_rec,
            "longueur_faconnee_m": round(Lu_avec_rec, 3),
            "longueur_totale_m": round(Lu_avec_rec * n_tot, 2),
            "masse_lineique_kg_m": round(ml, 4),
            "masse_kg": round(Lu_avec_rec * n_tot * ml, 1),
        })

    cad = cadres_poutre(d)
    lignes.append({
        "repere": "C1", "role": "cadres", "lecture": cad["lecture"],
        "nombre": cad["nombre_total"], "dia_mm": cad["dia_mm"],
        "longueur_unitaire_m": cad["perimetre_m"],
        "recouvrements_par_barre": 0,
        "longueur_faconnee_m": cad["perimetre_m"],
        "longueur_totale_m": round(cad["perimetre_m"] * cad["nombre_total"], 2),
        "masse_lineique_kg_m": round(masse_lineique_kg_m(cad["dia_mm"], rho), 4),
        "masse_kg": cad["masse_kg"],
    })

    masse = round(sum(x["masse_kg"] for x in lignes), 1)
    par_dia = {}
    for x in lignes:
        par_dia.setdefault(x["dia_mm"], {"dia_mm": x["dia_mm"], "masse_kg": 0.0,
                                         "longueur_m": 0.0, "reperes": []})
        par_dia[x["dia_mm"]]["masse_kg"] += x["masse_kg"]
        par_dia[x["dia_mm"]]["longueur_m"] += x["longueur_totale_m"]
        par_dia[x["dia_mm"]]["reperes"].append(x["repere"])
    recap = sorted(({**v, "masse_kg": round(v["masse_kg"], 1),
                     "longueur_m": round(v["longueur_m"], 1),
                     "part_pct": round(v["masse_kg"] / masse * 100, 1)}
                    for v in par_dia.values()), key=lambda v: -v["masse_kg"])
    return {
        "nb_de_poutres_dans_la_zone": n_poutres,
        "longueur_de_poutre_m": p["longueur_m"],
        "lignes": lignes,
        "masse_kg": masse,
        "recapitulatif_par_diametre": recap,
        "_pourquoi_le_recapitulatif": (
            "Le ferrailleur ne commande pas des reperes, il commande des DIAMETRES. Le "
            "recapitulatif est la piece qui passe commande, et c'est sur elle que se "
            "voient les erreurs de saisie : un diametre qui pese "
            f"{recap[0]['part_pct']} % de la masse merite d'etre revu deux fois."),
        "longueur_de_recouvrement_utilisee_m": Lr,
        "_recouvrement_note": (
            "Les recouvrements comptes ici sont ceux que la LIVRAISON impose : une "
            f"filante de {p['longueur_m']:.0f} m se fait avec des barres de {Lc:.0f} m. "
            "Leur nombre est geometrique. Leur LONGUEUR, elle, est reglementaire et "
            "reste ⏸ : celle du plan fictif est une hypothese de metre declaree."),
    }


def cadres_poutre(d: dict) -> dict:
    """Compter des cadres, c'est compter des INTERVALLES plus un.

    Sur une longueur L a l'espacement s, il y a floor(L / s) intervalles et donc
    floor(L / s) + 1 cadres. L'erreur de l'unite — compter L / s — coute un cadre par
    zone et se voit au metre ; elle se voit surtout a la pose, ou le dernier cadre
    manque toujours la ou on en a le plus besoin : contre l'appui.
    """
    a = d["armatures"]
    p = a["plan"]["poutre_PM1"]
    s = p["section_cm"]
    cad = p["cadres"]
    rho = a["conventions"]["masse_volumique_acier_kg_m3"]
    # Perimetre du cadre, mesure sur son AXE : l'enrobage se prend a la peau de
    # l'armature la plus exterieure, donc du cadre (meme convention que la cage 3D).
    b_ax = (s["b"] - 2 * s["enrobage"] - cad["dia_mm"] / 10.0) / 100.0
    h_ax = (s["h"] - 2 * s["enrobage"] - cad["dia_mm"] / 10.0) / 100.0
    perim = 2 * (b_ax + h_ax)
    zones = []
    total = 0
    for z in cad["zones"]:
        n = math.floor(z["longueur_cumulee_m"] / (z["espacement_cm"] / 100.0)) + 1
        zones.append({"nom": z["nom"], "longueur_m": z["longueur_cumulee_m"],
                      "espacement_cm": z["espacement_cm"], "nombre": n})
        total += n
    n_poutres = p["nb_dans_la_zone"]
    n_tot = total * n_poutres
    ml = masse_lineique_kg_m(cad["dia_mm"], rho)
    return {
        "dia_mm": cad["dia_mm"],
        "section_axe_cadre_m": {"b": round(b_ax, 4), "h": round(h_ax, 4)},
        "perimetre_m": round(perim, 3),
        "zones": zones,
        "nombre_par_poutre": total,
        "nombre_total": n_tot,
        "masse_kg": round(perim * n_tot * ml, 1),
        "lecture": cad["_lecture"],
        "espacement_moyen_cm": round(
            sum(z["longueur_cumulee_m"] for z in cad["zones"]) / (total - len(cad["zones"]))
            * 100, 1),
        "_piege_du_comptage": (
            f"{total} cadres par poutre pour "
            f"{sum(z['longueur_cumulee_m'] for z in cad['zones']):.0f} m. Compter L/s au "
            f"lieu de L/s + 1 en donnerait {total - len(cad['zones'])}, soit "
            f"{len(cad['zones'])} de moins : un par zone d'espacement. L'ecart de masse "
            "est negligeable ; l'ecart a la pose ne l'est pas, parce que le cadre qui "
            "manque est celui de l'extremite."),
        "_crochets": (
            "Ce perimetre est celui d'un cadre FERME SANS crochets d'extremite. Un cadre "
            "reel en porte deux, et leur longueur est reglementaire (⏸). Le metre des "
            "cadres est donc minorant."),
    }


# --------------------------------------------------------------- la dalle, par nappes
def nappes_dalle(d: dict) -> dict:
    """Une dalle ne se metre pas barre par barre : elle se metre par NAPPE.

    Sur un metre de largeur, a l'espacement s (cm), il y a 100/s barres. On multiplie par
    la largeur developpee et par la longueur de barre. C'est une difference de METHODE,
    pas de precision : chercher une nomenclature de dalle sur un plan, c'est chercher une
    piece qui n'existe pas, et c'est la premiere maladresse d'un metreur qui debute.
    """
    a = d["armatures"]
    dal = a["plan"]["dalle_DM1"]
    rho = a["conventions"]["masse_volumique_acier_kg_m3"]
    lignes = []
    for n in dal["nappes"]:
        bpm = 100.0 / n["espacement_cm"]
        # largeur couverte = surface developpee / longueur d'une barre
        largeur = n["developpe_sur_m2"] / n["longueur_barre_m"]
        nb = math.ceil(largeur * bpm) * n["nb_lits"]
        ml = masse_lineique_kg_m(n["dia_mm"], rho)
        lignes.append({
            "repere": n["repere"], "role": n["role"], "dia_mm": n["dia_mm"],
            "espacement_cm": n["espacement_cm"],
            "barres_par_metre": round(bpm, 2),
            "surface_developpee_m2": n["developpe_sur_m2"],
            "longueur_barre_m": n["longueur_barre_m"],
            "nombre": nb,
            "longueur_totale_m": round(nb * n["longueur_barre_m"], 1),
            "masse_lineique_kg_m": round(ml, 4),
            "masse_kg": round(nb * n["longueur_barre_m"] * ml, 1),
            "masse_par_m2_kg": round(
                nb * n["longueur_barre_m"] * ml / n["developpe_sur_m2"], 2),
        })
    masse = round(sum(x["masse_kg"] for x in lignes), 1)
    return {
        "surface_m2": dal["surface_m2"], "epaisseur_cm": dal["epaisseur_cm"],
        "lignes": lignes, "masse_kg": masse,
        "masse_par_m2_kg": round(masse / dal["surface_m2"], 2),
        "lecture": dal["_lecture"],
        "_controle_de_la_methode": (
            "Chaque nappe publie sa masse AU M2 : c'est le nombre qu'un metreur "
            "experimente verifie en premier, parce qu'il le connait par coeur pour une "
            "dalle courante. Une nappe qui sort de l'ordre de grandeur signale une "
            "erreur d'espacement ou de diametre avant tout autre controle."),
    }


# --------------------------------------------------------------- les deux voies (§ 3.3)
def deux_voies(d: dict, q: dict, nom: dict, nap: dict) -> dict:
    """Voie A : le metre du plan. Voie B : le ratio kg/m3. Et ce que l'ecart veut dire.

    ATTENTION a ce que cette comparaison est, et surtout a ce qu'elle n'est pas. Les deux
    voies ne verifient pas la meme chose :

      - la voie A mesure CE PLAN. Elle est sure a la geometrie pres, parce qu'elle ne
        repose que sur des longueurs et une masse volumique.
      - la voie B mesure A QUOI RESSEMBLE un plancher de ce type. Elle repose sur un
        ratio V3 dont la fourchette est large.

    Un ecart ne dit donc pas « le metre est faux ». Il dit « ce plan est plus leger (ou
    plus lourd) que l'habitude », ce qui est une question a poser au BET, pas une erreur
    a corriger. Le confondre avec un controle de justesse est l'erreur classique, et elle
    conduit a corriger un metre JUSTE pour le faire rentrer dans un ratio APPROXIMATIF.

    La comparaison se fait ELEMENT PAR ELEMENT. Un ratio global sur l'ensemble du
    plancher laisse une poutre trop lourde compenser une dalle trop legere : les deux
    ouvrages n'ont ni la meme densite d'acier, ni la meme fourchette, et leurs ratios ne
    s'additionnent pas plus que deux pourcentages de bases differentes (D-037).
    """
    r = d["ratios_V3"]
    elements = []
    for cle, nom_el, masse, beton in (
            ("acier_poutre_kg_m3", "Poutres PM1 (2 × 24,00 m)", nom["masse_kg"],
             q["beton_poutres_m3"]),
            ("acier_dalle_kg_m3", "Dalle DM1 (360 m², e = 25 cm)", nap["masse_kg"],
             q["beton_dalle_m3"])):
        ref, (bas, haut) = r[cle]["valeur"], r[cle]["fourchette"]
        ratio = masse / beton
        elements.append({
            "element": nom_el,
            "voie_A_kg": round(masse, 1),
            "beton_m3": beton,
            "ratio_du_plan_kg_m3": round(ratio, 1),
            "ratio_de_reference_kg_m3": ref,
            "fourchette_kg_m3": [bas, haut],
            "voie_B_kg": round(ref * beton, 1),
            "voie_B_fourchette_kg": [round(bas * beton, 1), round(haut * beton, 1)],
            "ecart_pct": round((masse - ref * beton) / (ref * beton) * 100, 1),
            "dans_la_fourchette": bool(bas <= ratio <= haut),
        })
    masse_plan = round(sum(e["voie_A_kg"] for e in elements), 1)
    voie_b = round(sum(e["voie_B_kg"] for e in elements), 1)
    beton = q["beton_m3"]
    hors = [e for e in elements if not e["dans_la_fourchette"]]
    return {
        "elements": elements,
        "voie_A_metre_du_plan_kg": masse_plan,
        "voie_A_detail": {"poutres_kg": nom["masse_kg"], "dalle_kg": nap["masse_kg"]},
        "voie_B_ratio_kg": voie_b,
        "voie_B_fourchette_kg": [round(sum(e["voie_B_fourchette_kg"][0] for e in elements), 1),
                                 round(sum(e["voie_B_fourchette_kg"][1] for e in elements), 1)],
        "beton_de_la_zone_m3": beton,
        "ratio_global_du_plan_kg_m3": round(masse_plan / beton, 1),
        "ecart_pct": round((masse_plan - voie_b) / voie_b * 100, 1),
        "elements_hors_fourchette": [e["element"] for e in hors],
        "tous_dans_la_fourchette": not hors,
        "ce_que_l_ecart_veut_dire": (
            "Les deux voies ne mesurent pas la meme chose. La voie A mesure CE plan, "
            "exactement : elle ne repose que sur des longueurs et une masse volumique. "
            "La voie B mesure a quoi ressemble un plancher de ce type, approximativement, "
            "sur un ratio V3 a large fourchette. Un ecart interroge le PLAN ; il ne "
            "condamne jamais le metre."
            + ("" if not hors else
               " Ici " + ", ".join(e["element"] for e in hors) + " sort de sa fourchette : "
               "c'est une question a poser au BET, pas une erreur etablie.")),
        "_pourquoi_element_par_element": (
            f"Globalement le plan pese {masse_plan / beton:.0f} kg/m3, ce qui ne se "
            "compare a rien : il n'existe pas de fourchette pour « un plancher » en "
            "general, parce que la part relative de poutre et de dalle change tout. "
            "Comparer element par element evite qu'une poutre lourde compense une dalle "
            "legere — la meme faute de domaine que D-037 denonce ailleurs."),
        "_erreur_a_ne_pas_commettre": (
            "Corriger le metre pour le faire rentrer dans le ratio. C'est l'inversion "
            "complete : on remplace une mesure sure par une hypothese V3."),
    }


# --------------------------------------------------------------- plan -> commande -> paye
def du_plan_a_la_commande(d: dict, masse_plan: float, nap: dict) -> dict:
    """Trois masses d'acier pour le meme ouvrage, et elles ne sont jamais egales.

    - l'acier DU PLAN : ce que la nomenclature totalise, recouvrements compris ;
    - l'acier COMMANDE : le plan plus les chutes de faconnage, plus le fil a ligaturer ;
    - l'acier PAYE : ce que le CPS dit de payer, et c'est une question de MARCHE, pas de
      metre. Le plus souvent le poids theorique du plan, sans chutes ni ligatures — ce
      qui veut dire que les chutes sont dans le PRIX unitaire, pas dans la quantite.

    Confondre les deux premiers fait commander trop peu. Confondre les deux derniers fait
    reclamer une quantite qui n'est pas due, et perdre la reclamation.
    """
    k = d["armatures"]["du_plan_a_la_commande"]
    chutes = masse_plan * k["chutes_pct"]["valeur"] / 100.0
    ligat = (masse_plan + chutes) * k["ligatures_pct"]["valeur"] / 100.0
    commande = masse_plan + chutes + ligat
    cales = nap["surface_m2"] * k["cales_par_m2"]["valeur"]
    return {
        "acier_du_plan_kg": round(masse_plan, 1),
        "chutes_kg": round(chutes, 1), "chutes_pct": k["chutes_pct"]["valeur"],
        "ligatures_kg": round(ligat, 1), "ligatures_pct": k["ligatures_pct"]["valeur"],
        "acier_commande_kg": round(commande, 1),
        "ecart_commande_plan_pct": round((commande - masse_plan) / masse_plan * 100, 1),
        "cales_d_enrobage_u": round(cales),
        "cales_note": (
            "Les cales ne sont pas de l'acier et ne pesent rien au metre. Elles sont la "
            "ligne qu'on oublie de commander, et un coulage ne demarre pas sans elles : "
            "sans cale, pas d'enrobage, et sans enrobage le visa tombe."),
        # le generateur `cascade` attend `montant` (et non `valeur`) : une cle mal nommee
        # produit des NaN dans le SVG, ce que le controle de rendu attrape.
        "cascade": [
            {"libelle": "Acier du plan", "montant": round(masse_plan, 1),
             "type": "depart"},
            {"libelle": f"Chutes {k['chutes_pct']['valeur']:.0f} %",
             "montant": round(chutes, 1), "type": "hausse"},
            {"libelle": f"Ligatures {k['ligatures_pct']['valeur']:.0f} %",
             "montant": round(ligat, 1), "type": "hausse"},
            {"libelle": "À commander", "montant": round(commande, 1), "type": "total"},
        ],
        "ce_qui_se_paie": (
            "Ce que le maitre d'ouvrage paie se lit dans le CPS, pas dans cette cascade. "
            "L'usage le plus repandu est le POIDS THEORIQUE du plan — ni chutes, ni "
            "ligatures, ni surlongueurs — l'entreprise les portant dans son prix "
            "unitaire. D'ou la regle de suivi : la quantite d'un attachement d'acier se "
            "prend sur la NOMENCLATURE VISEE, jamais sur un bon de livraison. Les deux "
            f"different ici de {(commande - masse_plan) / masse_plan * 100:.1f} %."),
        "_renvoi_CPS": "⚠ a verifier dans le CPS du marche : mode de metre des aciers.",
    }


def le_metre_contre_l_estimation(d: dict, q: dict, dv: dict, tv: dict) -> dict:
    """Ce que le metre d'un plan vise change pour le budget qui a ete bati AVANT lui.

    Toute la chaine economique du cours — bordereau de D1, situation, valeur acquise de
    D4 — repose sur une quantite d'acier ESTIMEE par ratio, avant que le moindre plan
    n'existe. C'est la facon normale de proceder, et ce n'est pas un defaut : on ne
    chiffre pas un marche en attendant les plans d'execution.

    Ce qui serait un defaut, c'est de ne jamais remplacer l'estimation par le metre une
    fois le plan vise. Le metre d'un plan vise est une MESURE ; le ratio est une
    hypothese. Le jour du visa, le second cede la place au premier, et la difference se
    propage : quantite au bordereau, montant des situations, BAC de la valeur acquise.

    Le controle qui compte ici n'est pas « les deux nombres sont-ils egaux ? » — ils ne
    le seront jamais — mais « le metre tombe-t-il dans la FOURCHETTE que l'estimation
    avait declaree ? ». S'il y tombe, l'estimation a fait son travail. S'il en sort,
    c'est le budget qu'il faut rouvrir, pas le plan qu'il faut discuter.
    """
    est = tv["quantites"]["acier_kg"]
    f = tv["quantites"]["fourchette_acier"]
    metre = dv["voie_A_metre_du_plan_kg"]
    dans = f["min_kg"] <= metre <= f["max_kg"]
    return {
        "estimation_par_ratio_kg": est,
        "fourchette_de_l_estimation_kg": [f["min_kg"], f["max_kg"]],
        "metre_du_plan_kg": metre,
        "ecart_kg": round(metre - est, 1),
        "ecart_pct": round((metre - est) / est * 100, 1),
        "le_metre_est_dans_la_fourchette_de_l_estimation": bool(dans),
        "lecture": (
            f"L'estimation par ratio annoncait {est:.0f} kg, fourchette {f['min_kg']:.0f} "
            f"a {f['max_kg']:.0f}. Le metre du plan en donne {metre:.0f}, soit "
            f"{(metre - est) / est * 100:+.1f} %. "
            + ("Il tombe DANS la fourchette : l'estimation a fait son travail, et c'est "
               "desormais le metre qui vaut."
               if dans else
               "Il en SORT : ce n'est plus le plan qu'on discute, c'est le budget qu'on "
               "rouvre.")),
        "ce_qui_change_en_aval": (
            "Des le visa, la ligne « aciers » du bordereau, les quantites des "
            "attachements et le BAC de la valeur acquise se prennent sur la NOMENCLATURE "
            "et non sur le ratio. Tant que ce basculement n'est pas fait, le suivi "
            "compare un avancement mesure sur des plans a un budget bati sur une "
            "hypothese : les indices de performance ne mesurent alors plus rien de "
            "precis — c'est la meme faute d'assiette que D4 corrige sur sa valeur "
            "acquise."),
        "_pourquoi_ce_module_ne_le_fait_pas": (
            "Le cours ne rebascule PAS le bordereau sur ce metre, et c'est deliberé : le "
            "plan de B3e ne couvre qu'UNE zone sur huit, et il est fictif. Rebasculer "
            "donnerait l'illusion d'un metre d'execution complet. Ce qui est enseigne "
            "est la regle et le moment ou elle s'applique, pas un nouveau nombre."),
    }


# --------------------------------------------------------------- lire et controler
def lire_un_plan() -> dict:
    """Les sept informations qu'un plan de ferraillage porte, et dans quel ordre les lire.

    L'ordre compte : il va du general au detail, et chaque etape conditionne la suivante.
    Un plan qu'on lit en commencant par les diametres se lit deux fois.
    """
    return {"etapes": [
        {"n": 1, "quoi": "Le cartouche",
         "ce_qu_on_y_cherche": "indice, date, mention « BON POUR EXECUTION » ou « VISE »",
         "pourquoi": "un plan non vise ne se pose pas, et un indice perime se pose encore "
                     "moins : c'est la premiere cause de ferraillage a refaire"},
        {"n": 2, "quoi": "Le reperage dans l'ouvrage",
         "ce_qu_on_y_cherche": "quel element, quel niveau, quelle zone, quel sens",
         "pourquoi": "une poutre posee a l'envers a ses chapeaux en bas ; cela se voit a "
                     "la fissuration, des le decoffrage"},
        {"n": 3, "quoi": "La coupe transversale",
         "ce_qu_on_y_cherche": "b, h, enrobage, lits inferieurs et superieurs, cadres",
         "pourquoi": "c'est la seule vue ou l'enrobage et l'espacement entre lits se "
                     "lisent ; tout le reste du plan la suppose connue"},
        {"n": 4, "quoi": "L'elevation",
         "ce_qu_on_y_cherche": "ou chaque barre COMMENCE et ou elle S'ARRETE",
         "pourquoi": "les arrets de barres sont l'information la plus dense du plan et la "
                     "plus souvent mal posee ; une barre arretee trop tot ne se rattrape pas"},
        {"n": 5, "quoi": "La nomenclature",
         "ce_qu_on_y_cherche": "une ligne par repere : nombre, diametre, longueur, faconnage",
         "pourquoi": "c'est ce que le ferrailleur faconne, et ce que le metre totalise. "
                     "Le plan dessine, la nomenclature chiffre : les deux doivent dire la "
                     "meme chose, et c'est un controle a faire"},
        {"n": 6, "quoi": "Les detail de faconnage",
         "ce_qu_on_y_cherche": "retours, crochets, cotes de pliage",
         "pourquoi": "une barre se commande a la longueur DEVELOPPEE ; la cote du dessin "
                     "n'est pas la longueur a couper"},
        {"n": 7, "quoi": "Les reservations et les attentes",
         "ce_qu_on_y_cherche": "trous, fourreaux, aciers en attente pour la suite",
         "pourquoi": "ce sont les seules informations du plan qui viennent d'un AUTRE "
                     "lot ; elles arrivent en retard, et on coule sans elles"},
    ],
        "la_regle": (
            "Lire un plan de ferraillage, ce n'est pas verifier un calcul : c'est "
            "verifier qu'il est EXECUTABLE et CONFORME A CE QUI A ETE VISE. Le calcul "
            "appartient au BET et au controle technique. Confondre les deux roles fait "
            "perdre du temps sur ce qu'on ne peut pas trancher, et en fait perdre "
            "davantage sur ce qu'on etait seul a pouvoir voir."),
    }


def controles_du_ferraillage(d: dict, nap: dict) -> dict:
    """Ce qu'on controle sur un ferraillage pose, et contre QUOI on le controle.

    Chaque ligne porte sa REFERENCE de controle, et c'est tout l'enjeu : aucune de ces
    valeurs ne se juge de memoire. Elles se comparent au plan vise. La ou le critere est
    reglementaire, la colonne le dit ⏸ au lieu d'avancer un chiffre.
    """
    p = d["armatures"]["plan"]["poutre_PM1"]
    k = d["armatures"]["du_plan_a_la_commande"]
    return {"liste": [
        {"controle": "Enrobage", "comment": "cale en place, nombre et repartition",
         "reference": f"la cote du plan ({p['section_cm']['enrobage']} cm ici)",
         "statut_de_la_regle": "⏸ la valeur MINIMALE est normative (durabilite, feu)",
         "symptome_si_rate": "armature apparente ou trace de rouille au decoffrage, puis "
                             "corrosion : le desordre le plus courant et le plus cher"},
        {"controle": "Diametres et nombre", "comment": "lit par lit, contre la nomenclature",
         "reference": "la nomenclature visee",
         "statut_de_la_regle": "non normatif : c'est une conformite au plan",
         "symptome_si_rate": "rien de visible. C'est pour cela qu'on compte AVANT de "
                             "couler, et qu'on le compte a deux"},
        {"controle": "Arrets de barres", "comment": "ou chaque barre commence et s'arrete",
         "reference": "l'elevation du plan",
         "statut_de_la_regle": "⏸ la regle d'arret est normative",
         "symptome_si_rate": "fissure a l'endroit meme de l'arret, souvent des la mise en "
                             "charge"},
        {"controle": "Recouvrements", "comment": "longueur, et barres non recouvertes au "
                                                 "meme endroit",
         "reference": f"la cote du plan ({k['longueur_de_recouvrement_du_plan_m']['valeur']:.2f} m ici)",
         "statut_de_la_regle": "⏸ la longueur minimale est normative",
         "symptome_si_rate": "une section entierement recouverte au meme droit est une "
                             "section affaiblie, et cela ne se voit qu'apres"},
        {"controle": "Espacement des cadres", "comment": "au metre, dans chaque zone",
         "reference": "le plan : "
                      + " et ".join(f"{z['espacement_cm']} cm en {z['nom']}"
                                    for z in p["cadres"]["zones"]),
         "statut_de_la_regle": "⏸ l'espacement MAXIMAL est normatif",
         "symptome_si_rate": "fissures inclinees pres des appuis"},
        {"controle": "Proprete et calage", "comment": "terre, rouille non adherente, "
                                                      "stabilite de la cage",
         "reference": "aucune cote : c'est un controle visuel",
         "statut_de_la_regle": "non normatif",
         "symptome_si_rate": "cage deplacee pendant le coulage, et tous les controles "
                             "precedents deviennent faux"},
        {"controle": "Reservations et attentes", "comment": "presence, position, fixation",
         "reference": "le plan de synthese des lots techniques",
         "statut_de_la_regle": "non normatif",
         "symptome_si_rate": "carottage apres coup, dans une zone d'acier : le pire des "
                             "cas, parce qu'il faut alors decider de couper une armature"},
    ],
        "cales_a_prevoir_u": round(nap["surface_m2"] * k["cales_par_m2"]["valeur"]),
        "la_regle": (
            "On ne controle pas un ferraillage « contre la norme » : on le controle "
            "contre le PLAN VISE, et le plan a ete controle contre la norme par le BET "
            "et le controle technique, en amont. Le suivi qui pretend refaire ce "
            "controle-la sur le chantier fait mal les deux. En revanche, le suivi est le "
            "SEUL a pouvoir constater ce qui est reellement pose — et c'est irreversible "
            "des que le beton est coule."),
        "double_lecture": {
            "entreprise": (
                "Le chef de chantier controle AVANT d'appeler : nomenclature pointee, "
                "cales en place, propre. Appeler la maitrise d'oeuvre sur un ferraillage "
                "non termine coute une demi-journee de cycle et la confiance pour les "
                "zones suivantes."),
            "maitrise_d_oeuvre": (
                "Le visa de ferraillage est un POINT D'ARRET : il se leve sur un constat "
                "ecrit, date, et sur place — jamais sur une photo, jamais par telephone. "
                "Une non-conformite se formule par ecrit avec le delai de reprise et "
                "l'heure du reconstat, parce que le planning de coulage tourne derriere."),
        },
    }


# --------------------------------------------------------------- figures
def _filante(p: dict, lit: str) -> dict:
    """La barre filante d'un lit : celle qui court sur toute la poutre.

    C'est elle que montre une coupe en travee — les renforts et les chapeaux, eux,
    n'existent qu'a certaines abscisses, et c'est l'elevation qui les porte.
    """
    b = next(x for x in p["barres"] if x["lit"] == lit and x.get("filante"))
    return {"n": sum(q["n"] for q in b["positions"]), "dia_mm": b["dia_mm"],
            "repere": b["repere"]}
def figures(d: dict, nom: dict, nap: dict, dv: dict, cmd: dict) -> dict:
    a = d["armatures"]
    p = a["plan"]["poutre_PM1"]
    el = d["elements"]["poutres"][0]
    return {
        # La coupe montre les FILANTES, les seules barres presentes sur toute la
        # longueur : elle se derive donc du plan, lit par lit. Ecrite a la main, elle
        # portait HA20 et HA14 quand le plan, recalibre, portait HA25 et HA16 — une
        # figure qui contredit ses propres donnees, la famille de defaut la plus
        # frequente de ce cours.
        "coupe": {
            "section": {"b_cm": p["section_cm"]["b"], "h_cm": p["section_cm"]["h"],
                        "enrobage_cm": p["section_cm"]["enrobage"],
                        "inf": _filante(p, "inf"), "sup": _filante(p, "sup")},
            "cadres": {"dia_mm": p["cadres"]["dia_mm"],
                       "espacement_cm": p["cadres"]["zones"][1]["espacement_cm"]},
            "conventions": {"rayon_cintrage_mm": 20,
                            "enrobage_mesure_a": "peau exterieure du cadre"},
        },
        "elevation": {
            "travees_m": el["travees_m"], "b_m": el["b_m"], "h_m": el["h_m"],
            "aciers": [{"repere": br["repere"], "lit": br["lit"], "dia_mm": br["dia_mm"],
                        "de_m": q["de_m"], "a_m": q["a_m"], "n": q["n"]}
                       for br in p["barres"] for q in br["positions"]],
        },
        "par_diametre": [{"libelle": f"HA{x['dia_mm']} · {'+'.join(x['reperes'])}",
                          "valeur": x["masse_kg"]}
                         for x in nom["recapitulatif_par_diametre"]],
        "deux_voies": [
            {"libelle": "Voie A — métré du plan (nomenclature + nappes)",
             "valeur": dv["voie_A_metre_du_plan_kg"]},
            {"libelle": "Voie B — ratio kg/m³ × béton de la zone",
             "valeur": dv["voie_B_ratio_kg"]},
        ],
        "deux_voies_bande": dv["voie_B_fourchette_kg"],
        "cascade": cmd["cascade"],
    }


# --------------------------------------------------------------- assemblage
def tout_calculer(d: dict) -> dict:
    import plancher as plc
    q = plc.quantites_zone(d)
    nom = nomenclature_poutre(d)
    nap = nappes_dalle(d)
    dv = deux_voies(d, q, nom, nap)
    cmd = du_plan_a_la_commande(d, dv["voie_A_metre_du_plan_kg"], nap)
    tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json")
                    .read_text(encoding="utf-8"))
    return {
        "metre_contre_estimation": le_metre_contre_l_estimation(d, q, dv, tv),
        "lire_un_plan": lire_un_plan(),
        "nomenclature": nom,
        "cadres": cadres_poutre(d),
        "nappes": nap,
        "deux_voies": dv,
        "commande": cmd,
        "controles": controles_du_ferraillage(d, nap),
        "figures": figures(d, nom, nap, dv, cmd),
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    r = tout_calculer(d)
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "ferraillage.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    dv, n = r["deux_voies"], r["nomenclature"]
    print(f"poutres {n['masse_kg']} kg ({len(n['lignes'])} reperes) + dalle "
          f"{r['nappes']['masse_kg']} kg = {dv['voie_A_metre_du_plan_kg']} kg")
    for e in dv["elements"]:
        print(f"  {e['element']} : {e['ratio_du_plan_kg_m3']} kg/m3 "
              f"(reference {e['ratio_de_reference_kg_m3']}, fourchette "
              f"{e['fourchette_kg_m3']}) -> "
              f"{'dans' if e['dans_la_fourchette'] else 'HORS'}, {e['ecart_pct']:+} %")
    print(f"commande {r['commande']['acier_commande_kg']} kg "
          f"(+{r['commande']['ecart_commande_plan_pct']} %) | "
          f"{r['cadres']['nombre_total']} cadres, perimetre {r['cadres']['perimetre_m']} m")
