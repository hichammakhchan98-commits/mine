"""Installation de chantier : où la grue se pose, ce qu'elle atteint, ce qu'elle lève (C1).

Un plan d'installation n'est pas un problème de place disponible : c'est un problème de
**géométrie** et de **temps**. Ce module calcule quatre choses, toutes non normatives :

1. **Couvrir n'est pas lever.** Une grue à tour couvre un disque, mais sa charge
   disponible décroît comme l'inverse de la portée : le point le plus lointain est
   précisément celui où elle peut le moins. Une grue choisie sur son rayon est choisie
   sur le mauvais nombre.
2. **Le débit.** Une grue fait un nombre fini de levages par jour, et le gros œuvre en
   demande un nombre que le parc de coffrage détermine. C'est une SECONDE VOIE, par le
   débit, vers une question que le module D2 a déjà tranchée par le temps : combien de
   grues ? Les deux voies sont indépendantes, et c'est ce qui donne du poids à leur
   accord.
3. **La base-vie se dimensionne sur l'effectif de POINTE**, jamais sur l'effectif moyen
   — et le module D3 publie les deux, qui diffèrent d'un facteur deux.
4. **Le coût de l'installation est en deux morceaux** : un coût fixe, qui ne dépend que
   de la décision, et un loyer, qui ne dépend que de la durée du chantier. Le second
   n'appartient donc pas à l'installation : il appartient au planning.

Ce que le module ne dit pas : les distances de sécurité, les règles de survol, les
obligations de clôture, les surfaces réglementaires des locaux sociaux. Toutes sont
réglementaires et restent ⏸.
"""
from __future__ import annotations
import json, math, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "calc"))


def _f(x: float, dec: int = 0) -> str:
    s = f"{x:,.{dec}f}".replace(",", " ")
    return s.replace(".", ",") if dec else s


def _b(o: dict) -> tuple[float, float]:
    f = o.get("fourchette")
    return (float(f[0]), float(f[1])) if f else (float(o["valeur"]), float(o["valeur"]))


# ------------------------------------------------- 1. la courbe de charge
def charge_disponible_t(charge_max: float, moment: float, rayon: float) -> float:
    """Ce qu'une grue à tour peut lever à une portée donnée.

        charge(r) = min(charge maximale, moment maximal / r)

    Deux régimes et un coude. Près du mât, la grue est limitée par ses organes — c'est
    la charge maximale, constante. Au-delà, elle est limitée par son MOMENT, et la
    charge décroît comme 1/r. Le rayon du coude vaut moment / charge maximale.

    Cette formule est un abaque de constructeur simplifié, pas une norme : elle décrit
    la forme de la courbe, pas la courbe d'une machine précise. Elle suffit à ce que ce
    module démontre, et le module le dit.
    """
    if rayon <= 0:
        return charge_max
    return min(charge_max, moment / rayon)


def rayon_pour_lever(charge_max: float, moment: float, masse: float) -> float | None:
    """La portée maximale à laquelle une masse donnée reste levable, ou None si jamais."""
    if masse > charge_max:
        return None
    return moment / masse


# ------------------------------------------------- 2. la couverture, par échantillonnage
def couverture(d: dict, variante: dict, masses: list, pas: float = 1.0) -> dict:
    """Quelle part de l'emprise chaque grue atteint — et quelle part elle peut SERVIR.

    L'emprise est échantillonnée au mètre. Pour chaque point, on retient la grue qui
    offre la plus grande charge disponible, et non la plus proche : à deux grues de
    portées différentes, la plus proche n'est pas toujours la plus forte. C'est une
    nuance de calcul, et elle change le résultat sur les variantes à deux grues.
    """
    g = d["installation"]["grue"]
    cmax, mom = g["charge_max_t"]["valeur"], g["moment_max_tm"]["valeur"]
    L, l = d["geometrie"]["emprise_m"]
    nx, ny = int(L / pas), int(l / pas)

    total = 0
    couverts = 0
    servis = {m["piece"]: 0 for m in masses}
    pire_distance = 0.0
    pire_point = None
    for i in range(nx):
        for j in range(ny):
            x, y = (i + 0.5) * pas, (j + 0.5) * pas
            total += 1
            meilleure, d_min = 0.0, None
            for gr in variante["grues"]:
                r = math.hypot(x - gr["x_m"], y - gr["y_m"])
                if r <= gr["portee_m"]:
                    meilleure = max(meilleure, charge_disponible_t(cmax, mom, r))
                    d_min = r if d_min is None else min(d_min, r)
            if d_min is not None:
                couverts += 1
                if d_min > pire_distance:
                    pire_distance, pire_point = d_min, (round(x, 1), round(y, 1))
            for m in masses:
                if meilleure >= m["masse_t"]:
                    servis[m["piece"]] += 1
    return {
        "variante": variante["nom"],
        "grues": [{**gr} for gr in variante["grues"]],
        "nb_grues": len(variante["grues"]),
        "points_echantillonnes": total,
        "couverture_pct": round(couverts / total * 100, 1),
        "distance_la_plus_defavorable_m": round(pire_distance, 1),
        "point_le_plus_defavorable": pire_point,
        "charge_au_point_le_plus_defavorable_t": round(
            charge_disponible_t(cmax, mom, pire_distance), 2) if pire_distance else None,
        "part_servie_pct": {m["piece"]: round(servis[m["piece"]] / total * 100, 1)
                            for m in masses},
        # Ce qu'il faudrait pour servir la piece la plus lourde PARTOUT : un moment egal
        # a sa masse par la distance la plus defavorable. Le dire en « il faudrait une
        # grue plus grosse » sans le chiffrer laisse croire a un facteur deux.
        # Calcule sur la distance PUBLIEE, et non sur la distance interne : un lecteur
        # qui multiplie les deux nombres imprimes doit retrouver le troisieme.
        "moment_pour_tout_servir_tm": round(max(m["masse_t"] for m in masses)
                                            * round(pire_distance, 1), 1)
        if pire_distance else None,
        "rapport_au_moment_disponible": round(
            max(m["masse_t"] for m in masses) * round(pire_distance, 1) / mom, 2)
        if pire_distance else None,
    }


# ------------------------------------------------- 2bis-a. deux flèches qui se croisent
def interference(d: dict, variante: dict) -> dict:
    """Deux grues dont les cercles se recoupent ne sont pas deux grues indépendantes.

    Rien ici n'est réglementaire — les règles d'anti-collision, de décalage de hauteur
    et de priorité relèvent du marché et de la réglementation, et restent ⏸. Ce qui se
    calcule, c'est la GÉOMÉTRIE : l'aire commune aux deux cercles, et le fait que les
    deux crochets travaillent à la même hauteur parce que data/ n'en déclare qu'une.
    """
    g = d["installation"]["grue"]
    L, l = d["geometrie"]["emprise_m"]
    gr = variante["grues"]
    paires = []
    for i in range(len(gr)):
        for j in range(i + 1, len(gr)):
            a, b = gr[i], gr[j]
            dd = math.hypot(a["x_m"] - b["x_m"], a["y_m"] - b["y_m"])
            r1, r2 = a["portee_m"], b["portee_m"]
            if dd >= r1 + r2:                      # cercles disjoints
                aire = 0.0
            elif dd <= abs(r1 - r2):               # l'un dans l'autre
                aire = math.pi * min(r1, r2) ** 2
            else:
                # aire de la lentille de deux disques secants, forme fermee
                a1 = r1 ** 2 * math.acos((dd ** 2 + r1 ** 2 - r2 ** 2) / (2 * dd * r1))
                a2 = r2 ** 2 * math.acos((dd ** 2 + r2 ** 2 - r1 ** 2) / (2 * dd * r2))
                tri = 0.5 * math.sqrt(max(0.0, (-dd + r1 + r2) * (dd + r1 - r2)
                                          * (dd - r1 + r2) * (dd + r1 + r2)))
                aire = a1 + a2 - tri
            paires.append({
                "grues": [a["nom"], b["nom"]],
                "entraxe_m": round(dd, 1),
                "aire_commune_m2": round(aire, 1),
                "part_de_l_emprise_pct": round(aire / (L * l) * 100, 1),
                "secantes": aire > 0,
            })
    secantes = [x for x in paires if x["secantes"]]
    h = g["hauteur_sous_crochet_m"]
    return {
        "variante": variante["nom"],
        "nb_grues": len(gr),
        "paires": paires,
        "nb_paires_secantes": len(secantes),
        "aire_commune_totale_m2": round(sum(x["aire_commune_m2"] for x in secantes), 1),
        "hauteur_sous_crochet_m": h,
        "hauteurs_distinctes_declarees": False,
        "lecture": (
            f"Dans cette variante, {len(secantes)} paire(s) de flèches se recoupent sur "
            f"{_f(sum(x['aire_commune_m2'] for x in secantes), 0)} m², soit "
            f"{_f(sum(x['aire_commune_m2'] for x in secantes) / (L * l) * 100, 0)} % de "
            f"l'emprise. Les deux crochets travaillent à {_f(h)} m : data/ ne déclare "
            "qu'une hauteur sous crochet, donc le cours décrit deux grues au même "
            "niveau."
            if secantes else
            "Aucune paire de flèches ne se recoupe dans cette variante."),
        "_ce_que_la_geometrie_impose": (
            "Deux flèches qui se recoupent à la même hauteur ne peuvent pas travailler "
            "en même temps dans la zone commune : l'une attend, ou les deux travaillent "
            "sous un dispositif qui garantit qu'elles ne s'y rencontrent pas. La "
            "conséquence de planning est immédiate et elle ne figure dans aucun "
            "calcul de ce module : la capacité de deux grues sécantes n'est pas le "
            "double de celle d'une seule. Le taux de charge du § S3b compare la demande "
            "à UNE grue ; le comparer à deux supposerait une indépendance que cette "
            "géométrie n'a pas."),
        "_ce_qui_reste_en_attente": (
            "⏸ : les règles d'implantation de deux grues à tour, les dispositifs "
            "d'anti-collision, les décalages de hauteur sous crochet et de hauteur de "
            "flèche, les règles de priorité et les consignes aux grutiers. Elles sont "
            "réglementaires et contractuelles, et le cours ne les possède pas. Ce "
            "module dit seulement, et c'est déjà une obligation du plan d'installation, "
            "QUE la question se pose dans la variante retenue, et sur quelle surface."),
    }


# ------------------------------------------------- 2bis. le voisinage : la voie
def voisinage(d: dict, couv: list) -> dict:
    """Le cercle de la flèche atteint-il le gabarit de la voie ?

    Une grue hors service est mise en girouette : la flèche balaie tout son cercle. La
    question n'est donc pas « survole-t-on la voie en travaillant » — on peut s'en
    abstenir — mais « le cercle atteint-il le gabarit ». Si oui, la grue relève de la
    famille « à proximité » du module B7c : pas de fermeture de voie, mais un dispositif
    et une interface avec l'exploitant. C'est le troisième axe de comparaison des
    variantes, et il va en sens inverse des deux autres.
    """
    v = d["installation"]["voisinage"]
    _, l = d["geometrie"]["emprise_m"]
    dist, bornes = v["distance_facade_cote_voies_au_gabarit_m"]["valeur"], _b(
        v["distance_facade_cote_voies_au_gabarit_m"])
    y_gabarit = l + dist
    lignes = []
    for c in couv:
        survols = [round(gr["y_m"] + gr["portee_m"] - y_gabarit, 1)
                   for gr in c["grues"]]
        pire = max(survols)
        # Avec la distance la plus FAVORABLE de la fourchette, le survol disparaît-il ?
        pire_borne_favorable = max(gr["y_m"] + gr["portee_m"] - (l + bornes[1])
                                   for gr in c["grues"])
        lignes.append({
            "variante": c["variante"],
            "survol_du_gabarit_m": pire,
            "survol_bornes_m": [round(pire_borne_favorable, 1),
                                round(max(gr["y_m"] + gr["portee_m"] - (l + bornes[0])
                                          for gr in c["grues"]), 1)],
            "atteint_le_gabarit": pire > 0,
            "atteint_le_gabarit_meme_au_plus_favorable": pire_borne_favorable > 0,
            "famille_B7c": ("à proximité" if pire > 0 else "hors interception"),
            "nb_grues_concernees": sum(1 for x in survols if x > 0),
        })
    aucune = [x for x in lignes if not x["atteint_le_gabarit"]]
    return {
        "distance_au_gabarit_m": dist,
        "distance_bornes_m": list(bornes),
        "y_du_gabarit_m": y_gabarit,
        "lignes": lignes,
        "aucune_variante_n_evite_le_gabarit": not aucune,
        "variantes_concernees_quelles_que_soient_les_bornes": [
            x["variante"] for x in lignes
            if x["atteint_le_gabarit_meme_au_plus_favorable"]],
        "lecture": (
            f"Le gabarit de la voie est à {_f(y_gabarit, 0)} m de la façade côté ville. "
            + (f"Aucune des {len(lignes)} variantes n'évite de l'atteindre : le dépassement "
               f"va de {_f(min(x['survol_du_gabarit_m'] for x in lignes), 0)} à "
               f"{_f(max(x['survol_du_gabarit_m'] for x in lignes), 0)} m."
               if not aucune else
               f"{len(aucune)} variante(s) l'évitent.")),
        "_ce_que_cela_change": (
            "Rien au calcul de couverture, et tout au plan d'installation. Une grue dont "
            "le cercle atteint le gabarit se traite comme un ouvrage « à proximité » au "
            "sens du module B7c : dispositif de limitation ou de mise en girouette "
            "orientée, convention avec l'exploitant, et un délai d'instruction qui n'est "
            "pas celui du chantier. ⏸ les règles applicables, qui sont réglementaires et "
            "contractuelles — ce calcul dit seulement que la question se pose, et pour "
            "quelles variantes."),
        "_ce_qui_resiste_aux_bornes": (
            "La distance au gabarit est une hypothèse à fourchette large (de "
            f"{_f(bornes[0], 0)} à {_f(bornes[1], 0)} m), et c'est elle qui décide. "
            + (f"{len([x for x in lignes if x['atteint_le_gabarit_meme_au_plus_favorable']])} "
               "variante(s) atteignent le gabarit même avec la distance la plus "
               "favorable : "
               + ", ".join(x["variante"].split(" — ")[0] for x in lignes
                           if x["atteint_le_gabarit_meme_au_plus_favorable"])
               + ". Pour les autres, la réponse dépend d'un relevé de site, et le cours "
               "ne peut pas la donner : il peut seulement dire quelle mesure il faut "
               "aller chercher, et c'est déjà la moitié du travail."
               if any(x["atteint_le_gabarit_meme_au_plus_favorable"] for x in lignes)
               else "Aucune variante n'y résiste à la borne favorable.")),
        "_le_sens_inverse": (
            "C'est l'axe qui contredit les deux autres. La variante qui couvre le mieux "
            "est celle qui empiète le plus ; la variante décalée côté ville, la plus "
            "mauvaise en couverture, est la moins intrusive. Un plan d'installation ne "
            "maximise donc pas la couverture : il arbitre entre trois grandeurs qui ne "
            "vont pas dans le même sens, et deux d'entre elles se mesurent alors que la "
            "troisième se négocie."),
    }


# ------------------------------------------------- 2ter. les aires, et le rayon
def aire_couverte_hors_batiment(L: float, l: float, grues: list,
                                pas: float = 1.0) -> float:
    """Surface couverte par au moins une grue et située HORS de l'emprise du bâtiment.

    Par échantillonnage sur la boîte englobante des cercles. Isolée dans sa propre
    fonction pour être étalonnée sur un cas à solution fermée : un disque centré dans un
    carré de côté 2a, avec a < R < a√2, dont l'aire intérieure s'écrit exactement.
    """
    x0 = min([0.0] + [g["x_m"] - g["portee_m"] for g in grues])
    x1 = max([L] + [g["x_m"] + g["portee_m"] for g in grues])
    y0 = min([0.0] + [g["y_m"] - g["portee_m"] for g in grues])
    y1 = max([l] + [g["y_m"] + g["portee_m"] for g in grues])
    hors = 0
    nx, ny = int((x1 - x0) / pas), int((y1 - y0) / pas)
    for i in range(nx):
        for j in range(ny):
            x, y = x0 + (i + 0.5) * pas, y0 + (j + 0.5) * pas
            if 0 <= x <= L and 0 <= y <= l:
                continue                     # sous le bâtiment : pas une aire de stockage
            if any(math.hypot(x - g["x_m"], y - g["y_m"]) <= g["portee_m"]
                   for g in grues):
                hors += 1
    return round(hors * pas * pas, 1)


def aires(d: dict, variante: dict, bv: dict, pas: float = 1.0) -> dict:
    """Les aires qui doivent être sous la grue tiennent-elles dans ce qu'elle couvre ?

    L'emprise de la parcelle n'est pas déclarée dans ce cours : la surface calculée ici
    est donc un MAJORANT — tout ce que la grue couvre hors bâtiment, sans tenir compte
    des limites de propriété ni de la voirie. Un majorant insuffisant est décisif ; un
    majorant suffisant ne prouve rien, et le module le dit.
    """
    g = d["installation"]["grue"]
    L, l = d["geometrie"]["emprise_m"]
    lignes = []
    for a in d["installation"]["aires"]:
        s = a["surface_m2"]
        if s is None:                       # la base-vie se calcule, elle n'est pas posée
            s = bv["surface_installee_m2"]
        lignes.append({"aire": a["aire"], "surface_m2": s,
                       "sous_la_grue": a["sous_la_grue"],
                       "calculee": a["surface_m2"] is None})
    besoin = sum(x["surface_m2"] for x in lignes if x["sous_la_grue"])
    total = sum(x["surface_m2"] for x in lignes)

    majorant = aire_couverte_hors_batiment(L, l, variante["grues"], pas)
    return {
        "variante": variante["nom"],
        "lignes": lignes,
        "surface_totale_m2": round(total, 1),
        "surface_a_mettre_sous_la_grue_m2": round(besoin, 1),
        "part_sous_la_grue_pct": round(besoin / total * 100, 1) if total else None,
        "majorant_sous_grue_hors_batiment_m2": round(majorant, 1),
        "rapport_besoin_sur_majorant_pct": round(besoin / majorant * 100, 1)
        if majorant else None,
        "la_plus_grande_aire": max(lignes, key=lambda x: x["surface_m2"])["aire"],
        "la_plus_grande_est_sous_la_grue": max(
            lignes, key=lambda x: x["surface_m2"])["sous_la_grue"],
        "lecture": (
            f"Les aires d'installation totalisent {_f(total, 0)} m², dont "
            f"{_f(besoin, 0)} m² — {_f(besoin / total * 100, 0)} % — doivent être dans le "
            f"rayon de la grue. La variante retenue couvre au plus {_f(majorant, 0)} m² "
            f"hors bâtiment : le besoin en occupe {_f(besoin / majorant * 100, 0)} %."),
        "_pourquoi_un_majorant": (
            "Ce cours ne déclare pas l'emprise de la parcelle, seulement celle du "
            "bâtiment. La surface sous grue hors bâtiment est donc calculée sans limite "
            "de propriété : c'est un majorant. S'il ne suffisait pas, la conclusion "
            "serait ferme ; comme il suffit, il ne prouve rien — sur un chantier réel, "
            "c'est le plan de la parcelle qui tranche, et c'est là que les aires de "
            "stockage se perdent."),
        "_l_aire_qui_n_est_pas_sous_la_grue": (
            "La plus grande aire du chantier — le pré-assemblage de charpente — est "
            "déclarée HORS rayon, et ce n'est pas un oubli : ces pièces sont levées par "
            "une grue mobile, sous interception, et non par la grue à tour. Une aire hors "
            "rayon n'est une erreur que si la grue à tour doit la servir ; alors la "
            "manutention se fait deux fois, et c'est le défaut de plan d'installation le "
            "plus répandu."),
    }


# ------------------------------------------------- 3. le débit
def debit(d: dict, go: dict, pl: dict, tv: dict) -> dict:
    """Combien de levages par jour la grue peut faire, et combien le chantier en demande.

    C'est une SECONDE VOIE vers la question « combien de grues ? », que le module D2 a
    tranchée autrement — en regardant quelles tâches se chevauchent dans le temps. Ici
    on ne regarde pas le calendrier : on regarde le parc de coffrage, la cadence, et le
    nombre de levages que cela fait par jour. Les deux chemins n'ont aucun terme commun,
    et c'est ce qui donne du poids à leur accord (§ 3.3).
    """
    g = d["installation"]["grue"]
    lv = d["installation"]["levages"]
    heures = d["prix_unitaires_MAD"]["ressources"]["heures_par_jour"]
    cyc, cyc_b = g["cycles_par_heure"]["valeur"], _b(g["cycles_par_heure"])
    # Le taux est en POURCENTAGE dans data/ (son nom le dit) : il se divise ici, une
    # seule fois, et la sortie publie la fraction sous un nom qui le dit aussi.
    tau = g["taux_d_utilisation_pct"]["valeur"] / 100
    tau_b = [x / 100 for x in _b(g["taux_d_utilisation_pct"])]
    spl, spl_b = lv["surface_par_levage_m2"]["valeur"], _b(lv["surface_par_levage_m2"])
    div, div_b = lv["levages_divers_par_jour"]["valeur"], _b(lv["levages_divers_par_jour"])

    capacite = cyc * heures * tau
    cap_b = [cyc_b[0] * heures * tau_b[0], cyc_b[1] * heures * tau_b[1]]
    # Ce qui se LÈVE chaque jour, c'est le coffrage d'UNE ZONE, posé puis déposé, à la
    # cadence des zones. Ce n'est ni le parc ni la cadence du parc : le reste du parc est
    # immobilisé sur les zones en cure, et une table en cure ne passe pas au crochet.
    # Une première version lisait la ligne « optimum de coût » du tableau de parc de C3 —
    # un parc que le cours ne construit pas, et dont C3 écrit lui-même que ce n'est PAS
    # une décision. Elle sous-estimait la demande de 63 % et inversait le verdict.
    zone = tv["quantites"]["coffrage_m2"]
    cadence = go["cycle"]["cadence_j"]
    surface_par_jour = zone / cadence
    lev_coffrage = surface_par_jour * 2 / spl
    demande = lev_coffrage + div
    dem_b = [surface_par_jour * 2 / spl_b[1] + div_b[0],
             surface_par_jour * 2 / spl_b[0] + div_b[1]]
    return {
        "capacite_levages_par_jour": round(capacite, 1),
        "capacite_bornes": [round(cap_b[0], 1), round(cap_b[1], 1)],
        "cycles_par_heure": cyc,
        "taux_d_utilisation_fraction": tau,
        "heures_par_jour": heures,
        "coffrage_d_une_zone_m2": zone,
        "cadence_j": cadence,
        "parc_declare_m2": go["parc"]["parc_declare_m2"],
        "_source_du_coffrage": "calc/sorties/tranche-plancher.json — quantites.coffrage_m2 "
                               "(coffrage d'une zone, tranche verticale) et "
                               "calc/sorties/gros-oeuvre.json — cycle.cadence_j (C3) : "
                               "la cadence que le planning tient, pas celle d'un parc "
                               "hypothetique",
        "_ce_qui_se_leve_n_est_pas_le_parc": (
            "Le parc déclaré est de "
            f"{_f(go['parc']['parc_declare_m2'])} m², soit "
            f"{_f(go['parc']['parc_declare_m2'] / zone, 1)} fois le coffrage d'une zone : "
            "c'est ce qu'il faut POSSÉDER pour tenir la cadence, parce que plusieurs "
            "zones sont immobilisées en même temps, dont une en cure. Ce qui se LÈVE "
            "chaque cycle est le coffrage d'une seule zone. Confondre les deux "
            "multiplie la demande de levage par le nombre de zones simultanées — ou la "
            "divise, si l'on prend un parc plus petit que le vrai."),
        "surface_manutentionnee_par_jour_m2": round(surface_par_jour, 1),
        "levages_de_coffrage_par_jour": round(lev_coffrage, 1),
        "levages_divers_par_jour": div,
        "demande_levages_par_jour": round(demande, 1),
        "demande_bornes": [round(dem_b[0], 1), round(dem_b[1], 1)],
        "taux_de_charge_pct": round(demande / capacite * 100, 1),
        "taux_de_charge_bornes_pct": [round(dem_b[0] / cap_b[1] * 100, 1),
                                      round(dem_b[1] / cap_b[0] * 100, 1)],
        # Les bornes ci-dessus combinent QUATRE extremes dans le meme sens : c'est une
        # enveloppe, pas un intervalle de confiance. Le controle qui compte est donc
        # celui-ci : en ne faisant varier qu'UNE hypothese a la fois, le seuil de 100 %
        # est-il encore enjambe ? S'il ne l'etait pas, la voie trancherait.
        "sensibilite_une_a_une": [
            {"hypothese": "surface par levage",
             "taux_min_pct": round((surface_par_jour * 2 / spl_b[1] + div) / capacite * 100, 1),
             "taux_max_pct": round((surface_par_jour * 2 / spl_b[0] + div) / capacite * 100, 1)},
            {"hypothese": "levages divers",
             "taux_min_pct": round((lev_coffrage + div_b[0]) / capacite * 100, 1),
             "taux_max_pct": round((lev_coffrage + div_b[1]) / capacite * 100, 1)},
            {"hypothese": "cycles par heure",
             "taux_min_pct": round(demande / (cyc_b[1] * heures * tau) * 100, 1),
             "taux_max_pct": round(demande / (cyc_b[0] * heures * tau) * 100, 1)},
            {"hypothese": "taux d'utilisation",
             "taux_min_pct": round(demande / (cyc * heures * tau_b[1]) * 100, 1),
             "taux_max_pct": round(demande / (cyc * heures * tau_b[0]) * 100, 1)},
        ],
        "_ce_que_valent_les_bornes": (
            "Les bornes larges combinent les quatre hypothèses à leur extrême dans le "
            "même sens : c'est une enveloppe, pas un intervalle de confiance, et une "
            "enveloppe enjambe presque toujours le seuil. Le contrôle qui décide est "
            "donc la sensibilité UNE À UNE, ci-dessus : si une seule hypothèse, prise "
            "seule dans sa fourchette, fait passer le taux de charge de part et d'autre "
            "de 100 %, alors la voie ne tranche pas pour une raison de fond et non par "
            "accumulation de prudences."),
        # La POINTE : le jour ou l'on depose une zone et ou l'on coffre la suivante, le
        # coffrage compte deux fois. Ce n'est pas une statistique, c'est le cycle.
        # Calculee sur les levages de coffrage PUBLIES : un lecteur qui double le nombre
        # imprime doit retrouver celui-ci.
        "demande_de_pointe_levages_par_jour": round(round(lev_coffrage, 1) * 2 + div, 1),
        "taux_de_charge_de_pointe_pct": round(
            (round(lev_coffrage, 1) * 2 + div) / capacite * 100, 1),
        "_la_pointe_se_calcule": (
            "Le jour où l'on dépose le coffrage d'une zone ET où l'on pose celui de la "
            f"suivante, la part coffrage double : {_f(lev_coffrage * 2 + div, 0)} levages "
            f"au lieu de {_f(demande, 0)}, soit "
            f"{_f((round(lev_coffrage, 1) * 2 + div) / capacite * 100, 0)} % d'une grue. Ce n'est "
            "pas une statistique, c'est le cycle : il y a dans un cycle un jour de "
            "dépose et un jour de pose, et rien n'interdit qu'ils tombent le même. "
            "Dimensionner sur la moyenne revient à accepter que ce jour-là, la grue "
            "soit le goulot."),
        "grues_necessaires_par_le_debit": math.ceil(demande / capacite - 1e-9),
        "lecture": (
            f"Une grue fait {_f(cyc, 1)} levages par heure et travaille "
            f"{_f(heures)} heures, dont {_f(tau * 100)} % à lever : "
            f"{_f(capacite, 0)} levages par jour. Le gros œuvre en demande "
            f"{_f(demande, 0)} — {_f(surface_par_jour, 0)} m² de coffrage posés puis "
            f"déposés chaque jour, plus {_f(div)} levages divers. Le taux de charge est "
            f"de {_f(demande / capacite * 100)} %, et il dépasse 100 % : une grue n'y "
            "suffit pas."),
        "_ce_que_le_taux_de_charge_cache": (
            "Un taux de charge moyen ne dit rien des pointes. Le jour où l'on décoffre "
            "une zone et où l'on coffre la suivante, la demande double ; le jour du "
            "bétonnage, elle s'effondre. Ce module publie la pointe du cycle plutôt "
            "qu'un ordre de grandeur sur la fréquence des jours chargés : la seconde se "
            "dirait bien, et ne se calcule pas avec ce que le cours possède. C'est "
            "exactement ce que le module D2 montre sur le profil journalier de la grue, "
            "et c'est pourquoi une moyenne ne remplace pas un profil."),
        "_pourquoi_deux_levages_par_unite": (
            "Un coffrage se pose ET se dépose : chaque mètre carré de parc compte deux "
            "levages par rotation. L'oublier divise la demande par deux, et c'est "
            "l'erreur qui fait conclure qu'une grue suffit."),
        "_la_zone_et_le_parc": (
            "Deux grandeurs portent le mot « coffrage » et ne se remplacent pas : le "
            "PARC, qu'on possède, et la zone, qu'on manutentionne. Le parc dimensionne "
            "un loyer ; la zone dimensionne un nombre de levages. Les échanger est la "
            "même faute que confondre un stock et un flux, et elle se voit d'autant "
            "moins ici que les deux s'expriment en mètres carrés."),
    }


# ------------------------------------------------- 4. la base-vie
def base_vie(d: dict, pl: dict) -> dict:
    """Dimensionnée sur l'effectif de POINTE, jamais sur l'effectif moyen."""
    b = d["installation"]["base_vie"]
    # La pointe et la moyenne APRÈS lissage : ce sont celles du planning retenu. Prendre
    # la pointe d'avant surdimensionnerait la base-vie d'un quart, et prendre la moyenne
    # la sous-dimensionnerait de moitié — c'est tout le sujet de cette section.
    r = pl["ressources"]
    pointe, moyen = r["pointe_apres"], r["moyenne_apres"]
    pointe_avant = r["pointe_avant"]
    part, part_b = b["part_encadrement_pct"]["valeur"], _b(b["part_encadrement_pct"])
    m2, m2_b = b["m2_par_personne"]["valeur"], _b(b["m2_par_personne"])
    m2e, m2e_b = (b["m2_par_personne_encadrement"]["valeur"],
                  _b(b["m2_par_personne_encadrement"]))
    mod = b["module_m2"]

    def surface(n, p, s, se):
        enc = n * p / 100
        return (n - enc) * s + enc * se

    s_pointe = surface(pointe, part, m2, m2e)
    s_moyen = surface(moyen, part, m2, m2e)
    bornes = [surface(pointe, part_b[0], m2_b[0], m2e_b[0]),
              surface(pointe, part_b[1], m2_b[1], m2e_b[1])]
    modules = math.ceil(s_pointe / mod)
    return {
        "effectif_de_pointe": round(pointe, 1),
        "effectif_de_pointe_avant_lissage": pointe_avant,
        "effectif_moyen": round(moyen, 1),
        "rapport_pointe_sur_moyen": round(pointe / moyen, 2) if moyen else None,
        "_source_des_effectifs": "calc/sorties/planification.json — ressources (module D2/D3)",
        "surface_necessaire_m2": round(s_pointe, 1),
        "surface_bornes_m2": [round(bornes[0], 1), round(bornes[1], 1)],
        "surface_si_dimensionnee_sur_la_moyenne_m2": round(s_moyen, 1),
        "modules": modules,
        "surface_installee_m2": modules * mod,
        "perte_a_l_arrondi_m2": round(modules * mod - s_pointe, 1),
        "lecture": (
            f"L'effectif de pointe est de {_f(pointe, 0)} personnes et l'effectif moyen "
            f"de {_f(moyen, 0)} — un rapport de {_f(pointe / moyen, 2)}. La base-vie se "
            f"dimensionne sur la pointe : {_f(s_pointe, 0)} m², soit {modules} modules "
            f"de {mod} m². Dimensionnée sur la moyenne, elle ferait "
            f"{_f(s_moyen, 0)} m² — et le jour de la pointe, "
            f"{_f(pointe - moyen, 0)} personnes n'auraient ni vestiaire ni place au "
            "réfectoire."),
        "_pourquoi_la_pointe": (
            "Une base-vie n'est pas un service moyen : c'est une capacité. Un "
            "réfectoire dimensionné sur la moyenne est plein un jour sur deux, et ce "
            "qui se passe alors ne se voit sur aucun indicateur — les compagnons "
            "mangent dehors, se changent dans les véhicules, et l'encadrement apprend "
            "le problème par le turn-over. C'est la même faute que dimensionner une "
            "grue sur une demande moyenne (§ S3b) ou lire un avancement sans son "
            "dénominateur (module D4) : une moyenne ne remplace jamais un profil."),
        "_l_arrondi_n_est_pas_une_perte": (
            f"La surface installée dépasse la surface calculée de "
            f"{_f(modules * mod - s_pointe, 0)} m², parce qu'on commande des modules "
            "entiers. Ce n'est pas du gaspillage : c'est la marge qui absorbe les "
            "visites, les sous-traitants de passage et la pointe qu'on n'avait pas "
            "prévue. Une base-vie calée au mètre carré près est une base-vie trop "
            "petite."),
    }


def fenetre_de_grue(pl: dict, pr: dict) -> dict:
    """De quand a quand la grue a tour est REELLEMENT necessaire.

    Une grue a tour n'est pas un frais de duree : c'est une ressource qui arrive, sert
    les taches de gros oeuvre, et s'en va. Le module D1 la facture au mois sur toute la
    duree du chantier, parce que son modele de frais de duree ne connait que des mois.
    Ici on lit le planning : les taches que D2 declare servies par la grue, et leur
    premiere et derniere journee. L'ecart entre les deux lectures est ce que ce module
    publie — il ne reecrit pas le bordereau de D1 (D-055).
    """
    seg = pl["segments_de_travail"]
    servies = [t for t in pl["grue"]["taches_servies"] if t in seg]
    debut = min(seg[t][0][0] for t in servies)
    fin = max(seg[t][-1][1] for t in servies)
    fd = pr["bordereau"]["frais_de_duree"]
    duree_ouvree = pl["calendrier"]["duree_ouvree_j"]
    duree_mois = fd["duree_mois_calendaires"]
    j_par_mois = duree_ouvree / duree_mois
    # Le TROU : la derniere tache servie (la marquise) arrive longtemps apres les autres.
    fins = sorted(((seg[t][-1][1], t) for t in servies), reverse=True)
    derniere, t_derniere = fins[0]
    avant_derniere = max((seg[t][-1][1] for t in servies if t != t_derniere),
                         default=derniere)
    debut_derniere = min(seg[t_derniere][0][0] for _ in [0])
    trou = max(0.0, debut_derniere - avant_derniere)
    profil = pl["grue"]["profil"]
    jours_actifs = len([x for x in profil if x["demande"] > 0])
    return {
        "taches_servies": servies,
        "debut_j": round(debut, 1),
        "fin_j": round(fin, 1),
        "duree_ouvree_j": round(fin - debut, 1),
        "duree_mois_calendaires": round((fin - debut) / j_par_mois, 2),
        "duree_du_chantier_ouvree_j": round(duree_ouvree, 1),
        "duree_du_chantier_mois": duree_mois,
        "part_du_chantier_pct": round((fin - debut) / duree_ouvree * 100, 1),
        "jours_ouvres_par_mois_calendaire": round(j_par_mois, 2),
        "jours_ou_la_grue_sert": jours_actifs,
        "part_de_la_fenetre_reellement_servie_pct": round(
            jours_actifs / (fin - debut) * 100, 1),
        "derniere_tache": t_derniere,
        "trou_avant_la_derniere_tache_j": round(trou, 1),
        "trou_mois": round(trou / j_par_mois, 2),
        "_source": "calc/sorties/planification.json — segments_de_travail et "
                   "grue.taches_servies (module D2)",
        "lecture": (
            f"Les {len(servies)} tâches servies par la grue à tour vont du jour "
            f"{_f(debut, 0)} au jour {_f(fin, 0)} : {_f(fin - debut, 0)} jours ouvrés, "
            f"soit {_f((fin - debut) / j_par_mois, 1)} mois calendaires sur les "
            f"{_f(duree_mois, 1)} du chantier — "
            f"{_f((fin - debut) / duree_ouvree * 100, 0)} %. Dans cette fenêtre, la grue "
            f"sert {jours_actifs} jours : le reste, elle attend."),
        "_une_grue_n_est_pas_un_frais_de_duree": (
            "Un frais de durée se paie tant que le chantier dure : encadrement, "
            "base-vie, gardiennage. Une grue à tour, non — elle se monte quand le gros "
            "œuvre commence et se démonte quand il finit. La facturer au mois sur toute "
            "la durée est commode et faux dans un rapport qui n'a rien de petit : ici "
            f"{_f(duree_mois / ((fin - debut) / j_par_mois), 1)}."),
    }


# ------------------------------------------------- 5. le coût de l'installation
def cout(d: dict, pr: dict, bv: dict, fen: dict, nb_grues: int,
         nb_grues_somme: int | None = None) -> dict:
    """Deux morceaux qui n'obéissent pas à la même chose : un fixe, un loyer."""
    g = d["installation"]["grue"]
    b = d["installation"]["base_vie"]
    fd = pr["bordereau"]["frais_de_duree"]
    duree_mois = fd["duree_mois_calendaires"]
    loyer_grue_mois = fd["lignes"]["grue_tour_location"]["MAD_mois"]
    loyer_bv_mois = fd["lignes"]["base_vie_et_fonctionnement"]["MAD_mois"]

    fixe = (g["montage_demontage_MAD"]["valeur"] + g["massif_de_fondation_MAD"]["valeur"]
            ) * nb_grues + b["installation_MAD"]["valeur"]
    fixe_b = [(_b(g["montage_demontage_MAD"])[0] + _b(g["massif_de_fondation_MAD"])[0])
              * nb_grues + _b(b["installation_MAD"])[0],
              (_b(g["montage_demontage_MAD"])[1] + _b(g["massif_de_fondation_MAD"])[1])
              * nb_grues + _b(b["installation_MAD"])[1]]
    # CHAQUE ressource sur SA durée. La base-vie dure autant que le chantier ; les grues
    # durent le gros œuvre. Une première version louait deux grues pendant les 29,7 mois
    # du chantier, soit cinq fois leur besoin : 5,6 MMAD de loyer pour 117 jours ouvrés
    # de service. C'est la faute que ce module dénonce ailleurs — confondre une ressource
    # et un frais de durée — et il la commettait dans son propre calcul de coût.
    mois_grue = fen["duree_mois_calendaires"]
    loyer_grues = loyer_grue_mois * nb_grues * mois_grue
    loyer_bv = loyer_bv_mois * duree_mois
    loyer = loyer_grues + loyer_bv
    total = fixe + loyer
    # Garder les grues pendant le trou, ou les démonter et les remonter pour la dernière
    # tâche : les deux se chiffrent, et l'écart n'est pas celui qu'on croit.
    garder = loyer_grue_mois * nb_grues * fen["trou_mois"]
    remonter = g["montage_demontage_MAD"]["valeur"] * nb_grues
    marche = pr["bordereau"]["prix_de_vente_MAD"]
    return {
        "nb_grues": nb_grues,
        "duree_du_chantier_mois": duree_mois,
        "duree_de_location_des_grues_mois": round(mois_grue, 2),
        "rapport_des_deux_durees": round(duree_mois / mois_grue, 1) if mois_grue else None,
        "_source_de_la_duree": "chantier : calc/sorties/prix.json — frais de duree (D1) ; "
                               "grues : fenêtre des tâches servies, calc/sorties/"
                               "planification.json (D2)",
        "cout_fixe_MAD": round(fixe, 2),
        "cout_fixe_bornes_MAD": [round(fixe_b[0], 2), round(fixe_b[1], 2)],
        "loyer_des_grues_MAD": round(loyer_grues, 2),
        "loyer_de_la_base_vie_MAD": round(loyer_bv, 2),
        # SECONDE VOIE sur le loyer de la base-vie : les modules comptes un a un, au
        # prix unitaire declare, contre la ligne forfaitaire de D1. Les deux doivent se
        # ressembler ; l'ecart est publie, et c'est lui qui valide l'ordre de grandeur.
        "loyer_base_vie_par_les_modules_MAD_par_mois": round(
            bv["modules"] * b["cout_module_MAD_par_mois"]["valeur"], 2),
        "ecart_des_deux_voies_base_vie_pct": round(
            (bv["modules"] * b["cout_module_MAD_par_mois"]["valeur"] / loyer_bv_mois - 1)
            * 100, 1),
        "_deux_voies_sur_la_base_vie": (
            f"Le module D1 porte la base-vie et son fonctionnement à "
            f"{_f(loyer_bv_mois)} MAD par mois, en forfait. Compté module par module — "
            f"{bv['modules']} modules à "
            f"{_f(b['cout_module_MAD_par_mois']['valeur'])} MAD — on trouve "
            f"{_f(bv['modules'] * b['cout_module_MAD_par_mois']['valeur'])} MAD par "
            f"mois, soit "
            f"{_f((bv['modules'] * b['cout_module_MAD_par_mois']['valeur'] / loyer_bv_mois - 1) * 100, 0)} % "
            "de plus. Deux voies indépendantes à moins d'un quart l'une de l'autre, sur "
            "une grandeur entièrement V3 : c'est un recoupement utile, pas une "
            "contradiction. Le total de ce module garde la ligne de D1, pour que les "
            "deux documents restent comparables ; la seconde voie dit simplement que "
            "le forfait de D1 est plutôt un peu bas."),
        "loyer_grue_MAD_par_mois": loyer_grue_mois * nb_grues,
        "loyer_base_vie_MAD_par_mois": loyer_bv_mois,
        "loyer_total_MAD": round(loyer, 2),
        "total_MAD": round(total, 2),
        "part_fixe_pct": round(fixe / total * 100, 1),
        "part_du_marche_pct": round(total / marche * 100, 2),
        # D1 publie DEUX prix : le bordereau de reference, qui montre d'ou vient chaque
        # dirham, et celui qu'on SIGNE, qui porte en plus la ligne de divers calibree.
        # Rapporter un poste au premier le fait paraitre plus lourd qu'il ne l'est dans
        # l'offre reellement remise.
        "marche_de_reference_MAD": marche,
        "marche_signe_MAD": pr["bordereau_avec_divers"]["prix_de_vente_MAD"],
        "part_du_marche_signe_pct": round(
            total / pr["bordereau_avec_divers"]["prix_de_vente_MAD"] * 100, 2),
        "_deux_bases_de_prix": (
            "Le module D1 publie deux prix et dit lequel on signe : le bordereau de "
            f"référence ({_f(marche / 1e6, 1)} MMAD), outil d'analyse, et celui qui "
            f"porte la ligne de divers calibrée "
            f"({_f(pr['bordereau_avec_divers']['prix_de_vente_MAD'] / 1e6, 1)} MMAD), "
            "qui est l'offre. L'installation pèse "
            f"{_f(total / marche * 100, 2)} % du premier et "
            f"{_f(total / pr['bordereau_avec_divers']['prix_de_vente_MAD'] * 100, 2)} % "
            "du second. Les deux sont justes ; un seul répond à « quelle part de mon "
            "offre est-ce que j'immobilise en installation ? », et c'est le second."),
        # Ce que couterait le parc obtenu en ADDITIONNANT les voies, au lieu d'en
        # prendre le maximum. Ecrire « quinze pour cent du marche » a la main donnait un
        # ordre de grandeur invente la ou le calcul etait a portee.
        "parc_si_somme_des_voies": nb_grues_somme,
        "part_du_marche_si_somme_des_voies_pct": round(
            ((g["montage_demontage_MAD"]["valeur"]
              + g["massif_de_fondation_MAD"]["valeur"]) * nb_grues_somme
             + b["installation_MAD"]["valeur"]
             + loyer_grue_mois * nb_grues_somme * mois_grue + loyer_bv)
            / marche * 100, 2) if nb_grues_somme else None,
        # Un mois gagne ne vaut pas la meme chose selon OU on le gagne : sur le gros
        # oeuvre, il economise les grues ET la base-vie ; a la fin du chantier, la
        # base-vie seule, parce que les grues sont parties depuis longtemps.
        "un_mois_gagne_sur_le_gros_oeuvre_MAD": loyer_grue_mois * nb_grues + loyer_bv_mois,
        "un_mois_gagne_a_la_fin_MAD": loyer_bv_mois,
        "rapport_des_deux_mois": round(
            (loyer_grue_mois * nb_grues + loyer_bv_mois) / loyer_bv_mois, 1),
        "cout_d_une_grue_de_plus_MAD": round(
            g["montage_demontage_MAD"]["valeur"] + g["massif_de_fondation_MAD"]["valeur"]
            + loyer_grue_mois * mois_grue, 2),
        "trou_garder_les_grues_MAD": round(garder, 2),
        "trou_les_demonter_et_remonter_MAD": round(remonter, 2),
        "trou_decision": ("garder" if garder < remonter else "démonter"),
        "trou_ecart_MAD": round(abs(remonter - garder), 2),
        "lecture": (
            f"L'installation coûte {_f(total, 0)} MAD sur ce chantier, soit "
            f"{_f(total / marche * 100, 2)} % du marché : {_f(fixe, 0)} MAD de coût fixe "
            "— montage, massif, raccordements — et un loyer en deux morceaux, "
            f"{_f(loyer_grues, 0)} MAD pour {nb_grues} grues pendant "
            f"{_f(mois_grue, 1)} mois et {_f(loyer_bv, 0)} MAD de base-vie pendant les "
            f"{_f(duree_mois, 1)} mois du chantier. La part fixe pèse "
            f"{_f(fixe / total * 100, 1)} % du total."),
        "_la_grue_n_est_pas_un_frais_de_duree": (
            f"Les grues à tour servent {_f(mois_grue, 1)} mois sur "
            f"{_f(duree_mois, 1)} — un rapport de {_f(duree_mois / mois_grue, 1)}. Les "
            "louer sur toute la durée du chantier, comme le fait un modèle de frais de "
            f"durée, coûterait {_f(loyer_grue_mois * nb_grues * duree_mois, 0)} MAD au "
            f"lieu de {_f(loyer_grues, 0)} : l'erreur ne porte pas sur un prix unitaire, "
            "elle porte sur une DURÉE, et c'est la famille d'erreur la plus chère d'un "
            "budget d'installation."),
        "_ou_se_gagne_un_mois": (
            f"Un mois gagné sur le gros œuvre vaut "
            f"{_f(loyer_grue_mois * nb_grues + loyer_bv_mois, 0)} MAD : les grues et la "
            f"base-vie. Un mois gagné à la fin du chantier vaut {_f(loyer_bv_mois, 0)} "
            f"MAD — {_f((loyer_grue_mois * nb_grues + loyer_bv_mois) / loyer_bv_mois, 1)} "
            "fois moins, parce que les grues sont démontées depuis longtemps. « Gagner "
            "un mois » n'est donc pas une grandeur : il faut dire LEQUEL."),
        "_le_trou": (
            f"La dernière tâche servie par la grue ({fen['derniere_tache']}) arrive "
            f"{_f(fen['trou_avant_la_derniere_tache_j'], 0)} jours ouvrés après les "
            f"autres, soit {_f(fen['trou_mois'], 1)} mois pendant lesquels les grues ne "
            f"servent à rien. Les garder coûte {_f(garder, 0)} MAD ; les démonter et les "
            f"remonter, {_f(remonter, 0)} MAD. On "
            f"{'garde' if garder < remonter else 'démonte'}, et l'écart est de "
            f"{_f(abs(remonter - garder), 0)} MAD — une décision qui se calcule en deux "
            "lignes et qu'on prend d'habitude au sentiment."),
        "_les_deux_morceaux_n_obeissent_pas_a_la_meme_chose": (
            "Le coût fixe dépend d'une DÉCISION : combien de grues, quelle base-vie. Le "
            "loyer dépend de DURÉES — et il y en a deux, pas une. Celle du gros œuvre "
            "porte les grues, celle du chantier entier porte la base-vie. Les écrire "
            "sur une seule ligne « coût d'installation » fait croire que ce poste "
            "s'optimise en choisissant mieux son matériel, et interdit de voir laquelle "
            "des deux durées on est en train de payer."),
        "_ce_que_D1_a_budgete": (
            f"Le module D1 porte dans ses frais de durée le loyer d'**une** grue à "
            f"{_f(loyer_grue_mois)} MAD par mois, **sur les {_f(duree_mois, 1)} mois du "
            f"chantier** : {_f(loyer_grue_mois * duree_mois)} MAD. Ce module conclut à "
            f"{nb_grues} grues, mais pendant {_f(mois_grue, 1)} mois seulement : "
            f"{_f(loyer_grues)} MAD. Les deux écarts vont en sens inverse, et celui de "
            f"la DURÉE l'emporte — D1 surestime de {_f(abs(loyer_grue_mois * duree_mois - loyer_grues))} MAD. "
            "Ce n'est pas reporté dans D1 : les deux chiffres sont posés à deux moments "
            "du cours, l'écart est publié et versé en dette (D-055). Ce qui se "
            "généralise est le mécanisme — **un modèle de frais de durée facture au "
            "mois tout ce qu'il ne sait pas dater, et une grue à tour se date**."),
        "ecart_avec_D1_MAD": round(loyer_grues - loyer_grue_mois * duree_mois, 2),
        "D1_loyer_de_grue_MAD": round(loyer_grue_mois * duree_mois, 2),
        "_le_prix_d_une_grue_de_plus": (
            f"Une grue de plus coûte {_f(g['montage_demontage_MAD']['valeur'] + g['massif_de_fondation_MAD']['valeur'])} MAD "
            f"de fixe avant même d'avoir levé quoi que ce soit, puis "
            f"{_f(loyer_grue_mois)} MAD par mois pendant {_f(mois_grue, 1)} mois : "
            f"{_f(g['montage_demontage_MAD']['valeur'] + g['massif_de_fondation_MAD']['valeur'] + loyer_grue_mois * mois_grue)} MAD. "
            "Le fixe en fait "
            f"{_f((g['montage_demontage_MAD']['valeur'] + g['massif_de_fondation_MAD']['valeur']) / (g['montage_demontage_MAD']['valeur'] + g['massif_de_fondation_MAD']['valeur'] + loyer_grue_mois * mois_grue) * 100, 0)} %, "
            "et c'est ce qui rend une deuxième grue chère même pour quelques semaines : "
            "on paie surtout de l'avoir montée."),
    }


# ------------------------------------------------- 6. les deux raisons du parc de grues
def pourquoi_ce_parc(d: dict, pl: dict, deb: dict, couv: list) -> dict:
    """Trois voies indépendantes vers le parc de grues — et une qui ne vote pas.

    Le temps (module D2), le débit et la géométrie (ce module) répondent chacun à la
    même question sans partager un seul terme : l'une regarde un calendrier, l'autre un
    parc de coffrage, la troisième un plan. Elles ne s'additionnent pas — on retient le
    MAXIMUM, parce qu'une grue de plus répond souvent aux trois à la fois.

    Et une voie peut ne pas trancher : celle du débit, dont les bornes enjambent le
    seuil de 100 %. Elle donne pourtant le même nombre que les deux autres — ce qui la
    rend plus instructive encore, parce qu'une voie qui tombe du bon côté n'a pas plus
    le droit de voter qu'une autre (D-059).

    Enfin, chaque voie porte sa propre DURÉE, et c'est elle qu'on oublie : le maximum
    des voies donne un NOMBRE de grues, jamais une durée de location. Les additionner
    double un budget ; les confondre dans le temps le quintuple.
    """
    res = pl["grue_resolution"]
    par_temps = res["parc_necessaire_si_non_resolu"]
    jours_de_conflit = res["resultat"]["nb_jours_en_conflit"]
    par_debit = deb["grues_necessaires_par_le_debit"]
    bornes = deb["taux_de_charge_bornes_pct"]
    debit_tranche = not (bornes[0] < 100 < bornes[1])
    # Le seuil est DECLARE, et il est strict : une variante qui couvre 98 % laisse des
    # angles hors d'atteinte, et un angle hors d'atteinte est une zone qu'il faudra
    # servir autrement. « Presque tout » n'est pas un critere de plan d'installation.
    SEUIL_COUVERTURE = 99.9
    par_geometrie = min((c["nb_grues"] for c in couv
                         if c["couverture_pct"] >= SEUIL_COUVERTURE), default=None)
    manquant = [(c["variante"], round((100 - c["couverture_pct"]) / 100
                                      * couv[0]["points_echantillonnes"]))
                for c in couv if c["couverture_pct"] < SEUIL_COUVERTURE]
    voies = [
        {"voie": "le temps", "parc": par_temps, "tranche": True,
         "duree": f"{jours_de_conflit} jour(s) de conflit, après lissage",
         "duree_j": jours_de_conflit,
         "source": "module D2 — deux tâches servies par la grue se chevauchent, et le "
                   "conflit ne se résorbe pas dans les marges",
         "pourquoi": "un conflit de calendrier mesuré sur le réseau rejoué"},
        {"voie": "le débit", "parc": par_debit, "tranche": debit_tranche,
         "duree": "toute la durée du gros œuvre en cycle",
         "duree_j": None,
         "source": "ce module — levages demandés par jour contre capacité d'une grue",
         "pourquoi": (f"taux de charge de {_f(deb['taux_de_charge_pct'])} %, mais des "
                      f"bornes de {_f(bornes[0])} à {_f(bornes[1])} % : elles enjambent "
                      "le seuil, donc cette voie NE TRANCHE PAS")},
        {"voie": "la géométrie", "parc": par_geometrie,
         "tranche": par_geometrie is not None,
         "duree": "toute la fenêtre de la grue",
         "duree_j": None,
         "source": "ce module — première variante qui couvre toute l'emprise",
         "pourquoi": "un bâtiment de 120 m ne tient pas dans un disque de 60 m de rayon "
                     "si la grue est en son centre"},
    ]
    decisives = [v["parc"] for v in voies if v["tranche"] and v["parc"]]
    retenu = max(decisives) if decisives else None
    return {
        "voies": voies,
        "seuil_de_couverture_pct": SEUIL_COUVERTURE,
        "_pourquoi_ce_seuil": (
            "La voie de la géométrie retient la première variante qui couvre "
            f"{_f(SEUIL_COUVERTURE, 1)} % de l'emprise, et non 95 ou 98 : un mètre carré "
            "non couvert est un mètre carré qu'il faudra servir autrement, et les "
            "variantes à une grue en laissent "
            + " · ".join(f"{v} : environ {n} m²" for v, n in manquant)
            + ". Ce ne sont pas des arrondis : ce sont les angles du bâtiment, et "
              "c'est là que se posent les banches de rive."),
        "parc_retenu": retenu,
        "nb_voies_qui_tranchent": len(decisives),
        "les_voies_qui_tranchent_s_accordent": len(set(decisives)) == 1,
        "la_regle": (
            "Trois raisons indépendantes de vouloir plus d'une grue : le TEMPS (deux "
            "tâches en même temps), le DÉBIT (trop de levages par jour), la GÉOMÉTRIE "
            "(un bâtiment plus long que la portée). Elles ne s'additionnent pas — on "
            "retient le MAXIMUM, parce qu'une seule grue de plus répond souvent aux "
            f"trois à la fois. Les additionner conduirait ici à "
            f"{sum(v['parc'] for v in voies if v['parc'])} grues sur un chantier qui en "
            f"demande {retenu}, et c'est une erreur qu'on voit."),
        "_une_voie_qui_ne_tranche_pas": (
            f"Le débit donne {par_debit} grue et ne vote pas pour autant : son taux de "
            f"charge nominal est de {_f(deb['taux_de_charge_pct'])} %, mais ses bornes "
            f"vont de {_f(bornes[0])} à {_f(bornes[1])} %. Elles enjambent le seuil de "
            "100 % : selon les hypothèses retenues, la même grue est à moitié vide ou "
            "trois fois saturée. **Une voie dont les bornes enjambent le seuil ne "
            "décide de rien**, et la compter comme un vote serait pire que de "
            "l'ignorer — ce serait transformer une incertitude en verdict. Elle garde "
            "pourtant son utilité : elle dit QUELLES hypothèses il faudrait resserrer "
            "pour trancher, et ce sont le taux d'utilisation et la surface par levage."),
        "_ce_que_leur_accord_vaut": (
            f"Les {len(decisives)} voies qui tranchent donnent "
            f"{retenu if retenu else '—'}, et elles n'ont aucun terme commun : l'une "
            "regarde un calendrier, l'autre un plan. C'est ce qui rend le résultat "
            "solide — pas la précision de chacune. Si elles avaient divergé, la plus "
            "contraignante aurait gagné, et le désaccord aurait été la vraie "
            "information."
            if len(set(decisives)) == 1 else
            f"Les voies qui tranchent ne s'accordent pas : "
            + " · ".join(f"{v['voie']} → {v['parc']}" for v in voies if v["tranche"])
            + f". On retient la plus contraignante, {retenu}, et le désaccord est la "
              "vraie information : il dit que le parc est dimensionné par une seule "
              "contrainte, donc fragile si cette contrainte bouge."),
        "_le_maximum_donne_un_nombre_pas_une_duree": (
            "Les trois voies ne disent pas seulement COMBIEN de grues : chacune dit "
            f"aussi PENDANT COMBIEN DE TEMPS, et ce n'est pas la même chose. Le temps "
            f"en demande {par_temps} pendant {jours_de_conflit} jour(s) — la durée du "
            "conflit, pas celle du chantier. La géométrie en demande "
            f"{par_geometrie} pendant toute la fenêtre de la grue. Prendre le maximum "
            "des nombres est juste ; prendre en même temps la plus longue des durées ne "
            "l'est pas, et c'est ainsi qu'un budget d'installation se met à porter deux "
            "grues sur toute la durée d'un chantier qui n'en a besoin que sur un "
            "cinquième. **Le maximum des voies donne un nombre. La durée, elle, se lit "
            "voie par voie.**"),
        "_ce_que_trois_jours_de_conflit_veulent_dire": (
            f"Le conflit de calendrier ne dure que {jours_de_conflit} jour(s) après "
            "lissage. Une deuxième grue à tour ne se loue pas pour trois jours : son "
            "montage seul en prend plusieurs semaines. Le module D2 le dit lui-même — "
            "trois issues, et une seule est honnête : une seconde grue, une grue "
            "mobile, ou déplacer une tâche hors de sa marge. C'est la voie de la "
            "GÉOMÉTRIE, et elle seule, qui justifie de louer la seconde grue sur toute "
            "la fenêtre du gros œuvre."),
    }


# ------------------------------------------------- figures
def figures(d: dict, couv: list, deb: dict, cout_: dict) -> dict:
    g = d["installation"]["grue"]
    cmax, mom = g["charge_max_t"]["valeur"], g["moment_max_tm"]["valeur"]
    pts = [{"x": r, "v": round(charge_disponible_t(cmax, mom, r), 2)}
           for r in range(2, int(g["portee_m"]) + 1, 2)]
    piece = d["_c1_masse_charpente"]
    r_lim = rayon_pour_lever(cmax, mom, piece)
    _y_gab = (d["geometrie"]["emprise_m"][1]
              + d["installation"]["voisinage"]
              ["distance_facade_cote_voies_au_gabarit_m"]["valeur"])
    # Le plan masse est une DONNEE, pas un dessin : la variante retenue sort du calcul.
    meilleure = max(couv, key=lambda c: (c["couverture_pct"],
                                         list(c["part_servie_pct"].values())[-1]))
    return {
        "plan_masse": {
            "emprise_m": d["geometrie"]["emprise_m"],
            "grues": [{"nom": g_["nom"], "x_m": g_["x_m"], "y_m": g_["y_m"],
                       "portee_m": g_["portee_m"]} for g_ in meilleure["grues"]],
            "variante": meilleure["variante"],
            "gabarit": {"y_m": _y_gab,
                        "libelle": f"gabarit de la voie — à {_f(_y_gab, 0)} m"},
        },
        "point_defavorable": {
            "x": meilleure["point_le_plus_defavorable"][0],
            "y": meilleure["point_le_plus_defavorable"][1],
            "libelle": f"{_f(meilleure['distance_la_plus_defavorable_m'], 1)} m → "
                       f"{_f(meilleure['charge_au_point_le_plus_defavorable_t'], 1)} t",
        },
        "courbe_de_charge": pts,
        "marqueur_charpente": {
            "x": round(r_lim, 1) if r_lim else 0,
            "libelle": f"au-delà, la pièce de {_f(piece, 1)} t ne passe plus"},
        # Les deux barres d'une meme variante sont ADJACENTES : groupees par serie, la
        # figure se lisait comme deux classements independants, alors que sa legende
        # annonce une comparaison deux a deux.
        "couverture": [x for c in couv for x in (
            {"libelle": c["variante"].split(" — ")[0] + " · couverture",
             "valeur": round(c["couverture_pct"], 1)},
            {"libelle": c["variante"].split(" — ")[0] + " · pièce de charpente",
             "valeur": list(c["part_servie_pct"].values())[-1], "alerte": True})],
        "survol": [{"libelle": c["variante"].split(" — ")[0],
                    "valeur": round(max(gr["y_m"] + gr["portee_m"] - _y_gab
                                        for gr in c["grues"]), 1),
                    "alerte": True} for c in couv],
        # Trois marches, pas deux : le loyer se coupe en ce qui dure le gros oeuvre et
        # ce qui dure le chantier. Les reunir cachait la grandeur qui decide.
        "cout": [
            {"libelle": "Coût fixe", "montant": round(cout_["cout_fixe_MAD"] / 1000)},
            {"libelle": "Grues (gros œuvre)",
             "montant": round(cout_["loyer_des_grues_MAD"] / 1000)},
            {"libelle": "Base-vie (chantier)",
             "montant": round(cout_["loyer_de_la_base_vie_MAD"] / 1000)},
            {"libelle": "Installation", "montant": round(cout_["total_MAD"] / 1000),
             "type": "total"},
        ],
    }


# ------------------------------------------------- assemblage
def tout_calculer(d: dict) -> dict:
    pl = json.loads((RACINE / "calc" / "sorties" / "planification.json")
                    .read_text(encoding="utf-8"))
    pr = json.loads((RACINE / "calc" / "sorties" / "prix.json").read_text(encoding="utf-8"))
    go = json.loads((RACINE / "calc" / "sorties" / "gros-oeuvre.json")
                    .read_text(encoding="utf-8"))
    # La pièce la plus lourde n'est PAS redéclarée ici : elle vient du module B7c (D-039).
    charpente = d["ferroviaire"]["sous_interception"]["masse_d_une_piece_t"]["valeur"]
    d = {**d, "_c1_masse_charpente": charpente}
    masses = []
    for p in d["installation"]["pieces_a_lever"]:
        m = (charpente if p["masse_t"] is None else p["masse_t"]["valeur"])
        masses.append({"piece": p["piece"], "masse_t": m,
                       "bornes_t": (list(_b(p["masse_t"])) if p["masse_t"]
                                    else list(_b(d["ferroviaire"]["sous_interception"]
                                                 ["masse_d_une_piece_t"]))),
                       "source": p.get("_lu_dans", "data/ — installation.pieces_a_lever")})
    couv = [couverture(d, v, masses) for v in d["installation"]["variantes_de_calage"]]
    tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json")
                    .read_text(encoding="utf-8"))
    deb = debit(d, go, pl, tv)
    bv = base_vie(d, pl)
    parc = pourquoi_ce_parc(d, pl, deb, couv)
    fen = fenetre_de_grue(pl, pr)
    co = cout(d, pr, bv, fen, parc["parc_retenu"] or 1,
              sum(v["parc"] for v in parc["voies"] if v["parc"]))
    vois = voisinage(d, couv)
    # La variante retenue est celle que figures() dessine : une seule definition, lue au
    # meme endroit par les aires et par le plan masse (D-039).
    fig = figures(d, couv, deb, co)
    retenue = next(v for v in d["installation"]["variantes_de_calage"]
                   if v["nom"] == fig["plan_masse"]["variante"])
    air = aires(d, retenue, bv)
    inter = interference(d, retenue)
    g = d["installation"]["grue"]
    rayons = {m["piece"]: rayon_pour_lever(g["charge_max_t"]["valeur"],
                                           g["moment_max_tm"]["valeur"], m["masse_t"])
              for m in masses}
    return {
        "pieces": [{**m, "rayon_limite_m": (round(rayons[m["piece"]], 1)
                                            if rayons[m["piece"]] else None)}
                   for m in masses],
        "couverture": couv,
        "debit": deb,
        "base_vie": bv,
        "parc_de_grues": parc,
        "fenetre_de_grue": fen,
        "interference": inter,
        "voisinage": vois,
        "aires": air,
        "cout": co,
        "figures": fig,
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    r = tout_calculer(d)
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "installation.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for p in r["pieces"]:
        print(f"  {p['piece'][:44]:<46} {p['masse_t']:>5.2f} t  levable jusqu'a "
              f"{p['rayon_limite_m'] if p['rayon_limite_m'] else '—'} m")
    for c in r["couverture"]:
        print(f"  {c['variante'][:34]:<36} couverture {c['couverture_pct']:>5.1f} % · "
              f"point le plus loin {c['distance_la_plus_defavorable_m']:>5.1f} m "
              f"({c['charge_au_point_le_plus_defavorable_t']} t) · "
              + " / ".join(f"{v:.0f} %" for v in c["part_servie_pct"].values()))
    de, bv, pa, co = r["debit"], r["base_vie"], r["parc_de_grues"], r["cout"]
    print(f"debit : {de['demande_levages_par_jour']} demandes contre "
          f"{de['capacite_levages_par_jour']} — {de['taux_de_charge_pct']} % "
          f"{de['taux_de_charge_bornes_pct']}")
    print(f"base-vie : pointe {bv['effectif_de_pointe']} / moyen {bv['effectif_moyen']} "
          f"-> {bv['surface_necessaire_m2']} m2, {bv['modules']} modules")
    print("parc : " + " · ".join(
        f"{v['voie']} {v['parc']}{'' if v['tranche'] else ' (ne tranche pas)'}"
        for v in pa["voies"]) + f" -> {pa['parc_retenu']}")
    print(f"cout : {co['total_MAD']:.0f} MAD dont {co['part_fixe_pct']} % fixe, "
          f"{co['part_du_marche_pct']} % du marche")
