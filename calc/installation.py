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
def debit(d: dict, go: dict, pl: dict) -> dict:
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
    # La demande vient du PARC de coffrage et de sa cadence, tous deux publiés par C3 :
    # le parc est posé puis reposé à chaque rotation, soit deux levages par unité.
    ligne = next(x for x in go["parc"]["lignes"] if x.get("optimum_de_cout"))
    parc = ligne["parc_m2"]
    cadence = ligne["cadence_tenue_j"]
    surface_par_jour = parc / cadence
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
        "parc_de_coffrage_m2": parc,
        "cadence_j": cadence,
        "_source_du_parc": "calc/sorties/gros-oeuvre.json — parc (module C3), ligne "
                           "retenue comme optimum de coût",
        "surface_manutentionnee_par_jour_m2": round(surface_par_jour, 1),
        "levages_de_coffrage_par_jour": round(lev_coffrage, 1),
        "levages_divers_par_jour": div,
        "demande_levages_par_jour": round(demande, 1),
        "demande_bornes": [round(dem_b[0], 1), round(dem_b[1], 1)],
        "taux_de_charge_pct": round(demande / capacite * 100, 1),
        "taux_de_charge_bornes_pct": [round(dem_b[0] / cap_b[1] * 100, 1),
                                      round(dem_b[1] / cap_b[0] * 100, 1)],
        "grues_necessaires_par_le_debit": math.ceil(demande / capacite - 1e-9),
        "lecture": (
            f"Une grue fait {_f(cyc, 1)} levages par heure et travaille "
            f"{_f(heures)} heures, dont {_f(tau * 100)} % à lever : "
            f"{_f(capacite, 0)} levages par jour. Le gros œuvre en demande "
            f"{_f(demande, 0)} — {_f(surface_par_jour, 0)} m² de coffrage posés puis "
            f"déposés chaque jour, plus {_f(div)} levages divers. Le taux de charge est "
            f"de {_f(demande / capacite * 100)} %."),
        "_ce_que_le_taux_de_charge_cache": (
            "Un taux de charge moyen ne dit rien des pointes. Le jour où l'on décoffre "
            "une zone et où l'on coffre la suivante, la demande double ; le jour du "
            "bétonnage, elle s'effondre. Une grue chargée à 80 % en moyenne est saturée "
            "un jour sur trois, et c'est ce jour-là qui fixe la cadence — c'est "
            "exactement ce que le module D2 montre sur le profil journalier, et c'est "
            "pourquoi une moyenne ne remplace pas un profil."),
        "_pourquoi_deux_levages_par_unite": (
            "Un coffrage se pose ET se dépose : chaque mètre carré de parc compte deux "
            "levages par rotation. L'oublier divise la demande par deux, et c'est "
            "l'erreur qui fait conclure qu'une grue suffit."),
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
            "grue sur une demande moyenne (§ S4b) ou lire un avancement sans son "
            "dénominateur (module D4) : une moyenne ne remplace jamais un profil."),
        "_l_arrondi_n_est_pas_une_perte": (
            f"La surface installée dépasse la surface calculée de "
            f"{_f(modules * mod - s_pointe, 0)} m², parce qu'on commande des modules "
            "entiers. Ce n'est pas du gaspillage : c'est la marge qui absorbe les "
            "visites, les sous-traitants de passage et la pointe qu'on n'avait pas "
            "prévue. Une base-vie calée au mètre carré près est une base-vie trop "
            "petite."),
    }


# ------------------------------------------------- 5. le coût de l'installation
def cout(d: dict, pr: dict, bv: dict, nb_grues: int) -> dict:
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
    loyer = (loyer_grue_mois * nb_grues + loyer_bv_mois) * duree_mois
    total = fixe + loyer
    marche = pr["bordereau"]["prix_de_vente_MAD"]
    return {
        "nb_grues": nb_grues,
        "duree_mois_calendaires": duree_mois,
        "_source_de_la_duree": "calc/sorties/prix.json — frais de duree (module D1), "
                               "elle-meme issue du reseau de D2",
        "cout_fixe_MAD": round(fixe, 2),
        "cout_fixe_bornes_MAD": [round(fixe_b[0], 2), round(fixe_b[1], 2)],
        "loyer_MAD_par_mois": loyer_grue_mois * nb_grues + loyer_bv_mois,
        "loyer_total_MAD": round(loyer, 2),
        "total_MAD": round(total, 2),
        "part_fixe_pct": round(fixe / total * 100, 1),
        # Un mois gagne, rapporte au cout fixe : c'est la seule facon honnete de comparer
        # un loyer a une remise. « Plus que 18 % de remise » etait faux — 18 % de
        # 1 460 000 MAD font plus qu'un mois de loyer.
        "un_mois_en_part_du_fixe_pct": round(
            (loyer_grue_mois * nb_grues + loyer_bv_mois) / fixe * 100, 1) if fixe else None,
        "part_du_marche_pct": round(total / marche * 100, 2),
        "cout_d_une_grue_de_plus_MAD": round(
            g["montage_demontage_MAD"]["valeur"] + g["massif_de_fondation_MAD"]["valeur"]
            + loyer_grue_mois * duree_mois, 2),
        "lecture": (
            f"L'installation coûte {_f(total)} MAD sur ce chantier, soit "
            f"{_f(total / marche * 100, 2)} % du marché : {_f(fixe)} MAD de coût fixe — "
            f"montage, massif, raccordements — et {_f(loyer)} MAD de loyer sur "
            f"{_f(duree_mois, 1)} mois. La part fixe ne pèse que "
            f"{_f(fixe / total * 100)} % du total."),
        "_les_deux_morceaux_n_obeissent_pas_a_la_meme_chose": (
            "Le coût fixe dépend d'une DÉCISION : combien de grues, quelle base-vie. Le "
            "loyer dépend de la DURÉE DU CHANTIER, c'est-à-dire d'un planning que "
            "l'installation ne décide pas. Les additionner dans un même poste « coût "
            "d'installation » fait croire qu'on peut l'optimiser en choisissant mieux "
            "son matériel — alors que les quatre cinquièmes se jouent sur la date de "
            "fin. Réduire l'installation de 10 % rapporte moins qu'un mois de chantier "
            "gagné."),
        "_ce_que_D1_a_budgete": (
            f"Le module D1 porte dans ses frais de durée le loyer d'**une** grue à "
            f"{_f(loyer_grue_mois)} MAD par mois. Le parc retenu ici en demande "
            f"{nb_grues} : à ce compte, les frais de durée du chantier augmentent de "
            f"{_f(loyer_grue_mois * (nb_grues - 1))} MAD par mois, soit "
            f"{_f(loyer_grue_mois * (nb_grues - 1) * duree_mois)} MAD sur la durée. Ce "
            "n'est pas reporté dans D1 : les deux chiffres sont posés à deux moments "
            "différents du cours, l'écart est publié comme tel et versé en dette "
            "(D-055), et ce qui se généralise est le mécanisme — **un plan "
            "d'installation qui conclut à une grue de plus modifie le bordereau, et "
            "personne ne le voit si les deux documents ne se parlent pas**."
            if nb_grues > 1 else
            "Le parc retenu est d'une grue, et c'est ce que le module D1 a budgété."),
        "ecart_avec_D1_MAD": round(loyer_grue_mois * (nb_grues - 1) * duree_mois, 2),
        "_le_prix_d_une_grue_de_plus": (
            f"Une grue de plus coûte {_f(g['montage_demontage_MAD']['valeur'] + g['massif_de_fondation_MAD']['valeur'])} MAD "
            f"de fixe avant même d'avoir levé quoi que ce soit, puis "
            f"{_f(loyer_grue_mois)} MAD par mois. Sur ce chantier, "
            f"{_f(g['montage_demontage_MAD']['valeur'] + g['massif_de_fondation_MAD']['valeur'] + loyer_grue_mois * duree_mois)} MAD. "
            "C'est pourquoi la question « faut-il une deuxième grue ? » ne se tranche "
            "pas sur un ressenti de saturation : elle se tranche en comparant ce "
            "montant au coût des jours que la grue unique fait perdre."),
    }


# ------------------------------------------------- 6. les deux raisons du parc de grues
def pourquoi_ce_parc(d: dict, pl: dict, deb: dict, couv: list) -> dict:
    """Trois voies indépendantes vers le parc de grues — et une qui ne vote pas.

    Le temps (module D2), le débit et la géométrie (ce module) répondent chacun à la
    même question sans partager un seul terme : l'une regarde un calendrier, l'autre un
    parc de coffrage, la troisième un plan. Elles ne s'additionnent pas — on retient le
    MAXIMUM, parce qu'une grue de plus répond souvent aux trois à la fois.

    Et une voie peut ne pas trancher. C'est le cas du débit ici : son taux de charge est
    de 62 %, mais ses bornes vont de 15 à 334 %. Une voie dont les bornes ENJAMBENT le
    seuil ne décide de rien, et le dire vaut mieux que de la compter comme un vote —
    c'est D-049 appliqué à un verdict plutôt qu'à un montant.
    """
    par_temps = pl["grue_resolution"]["parc_necessaire_si_non_resolu"]
    par_debit = deb["grues_necessaires_par_le_debit"]
    bornes = deb["taux_de_charge_bornes_pct"]
    debit_tranche = not (bornes[0] < 100 < bornes[1])
    par_geometrie = min((c["nb_grues"] for c in couv if c["couverture_pct"] >= 99.9),
                        default=None)
    voies = [
        {"voie": "le temps", "parc": par_temps, "tranche": True,
         "source": "module D2 — deux tâches servies par la grue se chevauchent, et le "
                   "conflit ne se résorbe pas dans les marges",
         "pourquoi": "un conflit de calendrier mesuré sur le réseau rejoué"},
        {"voie": "le débit", "parc": par_debit, "tranche": debit_tranche,
         "source": "ce module — levages demandés par jour contre capacité d'une grue",
         "pourquoi": (f"taux de charge de {_f(deb['taux_de_charge_pct'])} %, mais des "
                      f"bornes de {_f(bornes[0])} à {_f(bornes[1])} % : elles enjambent "
                      "le seuil, donc cette voie NE TRANCHE PAS")},
        {"voie": "la géométrie", "parc": par_geometrie, "tranche": par_geometrie is not None,
         "source": "ce module — première variante qui couvre toute l'emprise",
         "pourquoi": "un bâtiment de 120 m ne tient pas dans un disque de 60 m de rayon "
                     "si la grue est en son centre"},
    ]
    decisives = [v["parc"] for v in voies if v["tranche"] and v["parc"]]
    retenu = max(decisives) if decisives else None
    return {
        "voies": voies,
        "parc_retenu": retenu,
        "nb_voies_qui_tranchent": len(decisives),
        "les_voies_qui_tranchent_s_accordent": len(set(decisives)) == 1,
        "la_regle": (
            "Trois raisons indépendantes de vouloir plus d'une grue : le TEMPS (deux "
            "tâches en même temps), le DÉBIT (trop de levages par jour), la GÉOMÉTRIE "
            "(un bâtiment plus long que la portée). Elles ne s'additionnent pas — on "
            "retient le MAXIMUM, parce qu'une seule grue de plus répond souvent aux "
            "trois à la fois. Les additionner conduirait à quatre grues sur un chantier "
            "qui en demande deux, et c'est une erreur qu'on voit."),
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
             "valeur": c["couverture_pct"]},
            {"libelle": c["variante"].split(" — ")[0] + " · pièce de charpente",
             "valeur": list(c["part_servie_pct"].values())[-1], "alerte": True})],
        "survol": [{"libelle": c["variante"].split(" — ")[0],
                    "valeur": round(max(gr["y_m"] + gr["portee_m"] - _y_gab
                                        for gr in c["grues"]), 1),
                    "alerte": True} for c in couv],
        "cout": [
            {"libelle": "Coût fixe", "montant": round(cout_["cout_fixe_MAD"] / 1000)},
            {"libelle": "Loyer", "montant": round(cout_["loyer_total_MAD"] / 1000)},
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
    deb = debit(d, go, pl)
    bv = base_vie(d, pl)
    parc = pourquoi_ce_parc(d, pl, deb, couv)
    co = cout(d, pr, bv, parc["parc_retenu"] or 1)
    vois = voisinage(d, couv)
    # La variante retenue est celle que figures() dessine : une seule definition, lue au
    # meme endroit par les aires et par le plan masse (D-039).
    fig = figures(d, couv, deb, co)
    retenue = next(v for v in d["installation"]["variantes_de_calage"]
                   if v["nom"] == fig["plan_masse"]["variante"])
    air = aires(d, retenue, bv)
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
