"""Lots techniques et second œuvre, vus par l'interface (B7b + C4).

Le lecteur n'est pas responsable des lots techniques. Il en subit deux choses, et toutes
deux se calculent sans aucune norme :

1. **La géométrie d'une réservation.** Entre deux cadres d'une poutre il y a un espace
   libre, et il ne dépend que de l'espacement et du diamètre du cadre. Ce nombre décide
   quel fourreau passe sans toucher une armature — et au-delà, ce n'est plus une
   réservation, c'est une modification de structure, dont la règle est ⏸.
2. **La date de gel.** Une réservation se décide avant que le coffrage ne se ferme. Le
   carnet a donc une date limite par zone, et elle se lit dans le calendrier de coulage
   du module C3 moins un délai de commande. C'est la même soustraction que les interfaces
   du module D7, appliquée à un autre objet.

S'y ajoutent deux résultats sur l'enchaînement des corps d'état :

3. **Le second œuvre est une FILE, pas une tâche.** Sa durée en zones pipelinées s'écrit
   exactement : (ΣW + (Z−1)·max W) / Z. Elle décroît avec le nombre de zones et bute sur
   un plancher — la durée du corps d'état le plus lent — qu'aucun découpage ne franchit.
4. **Une frontière de zone coûte.** Chaque corps d'état s'y réinstalle. Le découpage
   optimal n'est donc pas le plus fin, et il se calcule.

Ce que le module ne dit pas : les règles de percement d'un élément porteur, les sections
admissibles, les distances aux armatures, le rétablissement du degré coupe-feu d'une
traversée, les classements au feu. Toutes sont réglementaires et restent ⏸.
"""
from __future__ import annotations
import json, math, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "calc"))


def _f(x: float, dec: int = 0) -> str:
    s = f"{x:,.{dec}f}".replace(",", " ")
    return s.replace(".", ",") if dec else s


def _court(texte: str, n: int) -> str:
    """Tronque au dernier espace avant n : un libelle coupe en plein mot est illisible."""
    if len(texte) <= n:
        return texte
    return texte[:n].rsplit(" ", 1)[0] + "…"


def _b(o: dict) -> tuple[float, float]:
    f = o.get("fourchette")
    return (float(f[0]), float(f[1])) if f else (float(o["valeur"]), float(o["valeur"]))


# ------------------------------------------------- 1. ce qui passe entre deux armatures
def passage_libre(d: dict, fer: dict) -> dict:
    """Le plus gros fourreau qui passe sans toucher une armature, endroit par endroit.

    Attention au piège, et il a coûté une passe à ce module : **un fourreau ne passe pas
    entre DEUX armatures, il passe dans une MAILLE**. Une dalle est armée dans deux sens
    et une poutre porte des cadres ET des barres longitudinales : l'ouverture libre est
    un rectangle, et un fourreau rond y tient par sa plus petite dimension.

    Tout se lit dans le plan de ferraillage que le module B3e publie — espacements,
    diamètres, largeur de l'âme entre les branches du cadre. Rien de normatif : la règle
    qui dit si l'on a le DROIT de percer là est, elle, réglementaire (⏸).
    """
    lt = d["lots_techniques"]["reservations"]
    dias = lt["diametres_courants_mm"]
    coupe = fer["figures"]["coupe"]["section"]
    dia_cadre = fer["cadres"]["dia_mm"]
    # Largeur libre entre les deux branches du cadre : la largeur de la poutre moins deux
    # enrobages et deux diamètres de cadre. L'enrobage se mesure à la peau EXTÉRIEURE du
    # cadre, comme la convention du plan le dit.
    largeur_ame = (coupe["b_cm"] * 10 - 2 * coupe["enrobage_cm"] * 10
                   - 2 * dia_cadre)
    endroits = []
    for z in fer["cadres"]["zones"]:
        esp = z["espacement_cm"] * 10
        endroits.append({
            "endroit": f"Âme de poutre — {z['nom']}",
            "armatures": f"cadres HA{dia_cadre} à {_f(z['espacement_cm'])} cm, "
                         f"âme de {_f(largeur_ame)} mm entre branches",
            "maille_mm": [round(esp - dia_cadre, 1), round(largeur_ame, 1)],
            "longueur_concernee_m": z["longueur_m"],
        })
    # Au niveau des armatures longitudinales inférieures, c'est leur espacement libre qui
    # commande, et il est bien plus serré que celui des cadres.
    inf = coupe["inf"]
    libre_inf = (largeur_ame - inf["n"] * inf["dia_mm"]) / (inf["n"] - 1)
    endroits.append({
        "endroit": "Poutre — au niveau des aciers inférieurs",
        "armatures": f"{inf['n']} HA{inf['dia_mm']} dans {_f(largeur_ame)} mm d'âme",
        "maille_mm": [round(libre_inf, 1),
                      round(min(z["espacement_cm"] * 10 - dia_cadre
                                for z in fer["cadres"]["zones"]), 1)],
        "longueur_concernee_m": None,
    })
    # La dalle est armée dans DEUX sens : une seule maille, pas deux endroits.
    nappe = fer["nappes"]["lignes"][:2]
    endroits.append({
        "endroit": "Dalle — maille des deux nappes",
        "armatures": " × ".join(f"HA{l['dia_mm']} à {_f(l['espacement_cm'], 1)} cm"
                                for l in nappe),
        "maille_mm": [round(nappe[0]["espacement_cm"] * 10 - nappe[0]["dia_mm"], 1),
                      round(nappe[1]["espacement_cm"] * 10 - nappe[1]["dia_mm"], 1)],
        "longueur_concernee_m": None,
    })
    for e in endroits:
        # Un fourreau ROND tient par la plus petite dimension de la maille.
        e["passage_libre_mm"] = min(e["maille_mm"])
        passe = [x for x in dias if x <= e["passage_libre_mm"]]
        e["plus_gros_diametre_qui_passe_mm"] = max(passe) if passe else None
        e["diametres_qui_passent"] = passe
        e["diametres_qui_ne_passent_pas"] = [x for x in dias if x > e["passage_libre_mm"]]
    pire = min(endroits, key=lambda e: e["passage_libre_mm"])
    meilleur = max(e["passage_libre_mm"] for e in endroits)
    nulle_part = [x for x in dias if x > meilleur]
    return {
        "endroits": endroits,
        "largeur_d_ame_mm": round(largeur_ame, 1),
        "passage_le_plus_etroit_mm": pire["passage_libre_mm"],
        "endroit_le_plus_etroit": pire["endroit"],
        "passage_le_plus_large_mm": meilleur,
        "diametres_qui_ne_passent_nulle_part_mm": nulle_part,
        "_source_des_armatures": "calc/sorties/ferraillage.json — cadres, nappes et coupe "
                                 "du module B3e. Aucun espacement, aucun diamètre et "
                                 "aucune largeur ne sont redéclarés ici (D-039)",
        "_une_maille_pas_un_espacement": (
            "Un fourreau rond ne passe pas « entre deux armatures » : il passe dans une "
            "MAILLE, et il y tient par la plus petite de ses deux dimensions. Une dalle "
            "armée {} donne une maille de {} × {} mm : c'est {} mm qui commandent, pas "
            "{}. Prendre le plus grand des deux espacements — l'erreur que ce module a "
            "commise avant sa relecture — fait croire qu'un fourreau de {} mm passe en "
            "dalle, alors qu'il n'y passe pas.".format(
                endroits[-1]["armatures"], _f(endroits[-1]["maille_mm"][0]),
                _f(endroits[-1]["maille_mm"][1]), _f(min(endroits[-1]["maille_mm"])),
                _f(max(endroits[-1]["maille_mm"])), 160)),
        "lecture": (
            f"La maille la plus étroite est celle {pire['endroit'].split(' — ')[-1]} : "
            f"{_f(pire['passage_libre_mm'])} mm. La plus large est de {_f(meilleur)} mm. "
            f"Un fourreau de {_f(nulle_part[0])} mm — un diamètre courant de désenfumage "
            "ou d'eaux usées — ne passe donc **nulle part** sans toucher une armature."
            if nulle_part else
            f"Les mailles vont de {_f(pire['passage_libre_mm'])} à {_f(meilleur)} mm : "
            "tous les diamètres du catalogue passent quelque part."),
        "_ce_que_ce_nombre_ne_dit_pas": (
            "Qu'un fourreau tienne dans une maille ne veut pas dire qu'on a le droit de "
            "le mettre là. La position admissible d'une réservation dans un élément "
            "porteur, sa section maximale, sa distance aux appuis et aux armatures "
            "principales sont **réglementaires** : ⏸. Ce calcul répond à une question "
            "plus modeste et toujours utile — **est-ce seulement géométriquement "
            "possible ?** Quand la réponse est non, la discussion avec le bureau d'études "
            "n'a pas lieu d'être : il faut changer de tracé."),
        "_la_vraie_frontiere": (
            "Une réservation qui coupe une armature n'est pas une réservation. C'est une "
            "modification de la structure, elle quitte le carnet de réservations pour "
            "devenir une note de calcul, et elle change de délai, de décideur et de prix. "
            "C'est la seule frontière que ce module ait besoin de connaître — et elle est "
            "géométrique, donc vérifiable par un chef de projet suivi sur un plan, sans "
            "attendre personne."),
    }


# ------------------------------------------------- 2. le carnet et sa date de gel
def gel_des_reservations(d: dict, pl: dict, su: dict, go: dict) -> dict:
    """À quelle date le carnet de réservations de chaque zone est irrévocable.

    Une réservation se pose dans le coffrage avant fermeture. La date limite est donc la
    date de coulage de la zone moins le délai de diffusion, commande, livraison et pose.
    C'est la soustraction du module D7 appliquée à un autre objet, et elle a la même
    vertu : elle transforme une liste en ordre du jour.
    """
    r = d["lots_techniques"]["reservations"]
    delai, delai_b = r["delai_de_gel_j"]["valeur"], _b(r["delai_de_gel_j"])
    dens, dens_b = r["densite_par_m2"]["valeur"], _b(r["densite_par_m2"])
    j_arret = su["date_arret"]["jour_ouvre"]
    seg = pl["segments_de_travail"]["MEZZ"]
    debut, fin = seg[0][0], seg[-1][1]
    nb_zones = go["cycle"]["nb_zones"]
    cadence = go["cycle"]["cadence_j"]
    surface_zone = d["geometrie"]["mezzanine"]["zones_de_coulage"]["longueur_zone_m"] \
        * d["geometrie"]["mezzanine"]["zones_de_coulage"]["largeur_zone_m"]
    lignes = []
    # Les dates de coulage se DEDUISENT du segment que D2 publie pour MEZZ et de la duree
    # de plancher que C3 calcule : la derniere zone se coule a la fin du segment, et les
    # autres remontent a la cadence. Une premiere version posait « debut + (i+1) x cadence »
    # et decalait les huit gels de 2,2 jours (D-039 : on lit, on ne suppose pas).
    duree_plancher = go["cycle"]["duree_du_plancher_j"]
    for i in range(nb_zones):
        coulage = fin - (nb_zones - 1 - i) * cadence
        limite = coulage - delai
        lignes.append({
            "zone": i + 1,
            "date_de_coulage_j": round(coulage, 1),
            "date_de_gel_j": round(limite, 1),
            "marge_a_la_date_d_arret_j": round(limite - j_arret, 1),
            "gelee": limite <= j_arret,
            "reservations": round(surface_zone * dens, 1),
        })
    gelees = [x for x in lignes if x["gelee"]]
    # LA FENETRE DU CARNET : de la premiere a la derniere date de gel. C'est la periode
    # pendant laquelle le carnet se joue reellement — et elle tombe bien avant le second
    # oeuvre, ce qui est tout l'enseignement de cette section.
    f_debut = min(x["date_de_gel_j"] for x in lignes)
    f_fin = max(x["date_de_gel_j"] for x in lignes)
    # Ce que faisait le chantier a ce moment-la : on LIT le reseau, on ne le suppose pas.
    seg_tous = pl["segments_de_travail"]
    en_cours = sorted(t for t, v in seg_tous.items()
                      if v[0][0] <= f_debut <= v[-1][1])
    noms = {t: pl["durees"][t]["nom"] for t in en_cours if t in pl["durees"]}
    return {
        "fenetre_du_carnet_j": [round(f_debut, 1), round(f_fin, 1)],
        "fenetre_duree_j": round(f_fin - f_debut, 1),
        "taches_en_cours_au_premier_gel": [noms.get(t, t) for t in en_cours],
        "_quand_le_carnet_se_joue": (
            f"Le premier carnet gèle au jour {_f(f_debut, 0)} et le dernier au jour "
            f"{_f(f_fin, 0)} : toute la question des réservations se règle en "
            f"{_f(f_fin - f_debut, 0)} jours, pendant que le chantier en est à "
            + (", ".join(noms.get(t, t).lower() for t in en_cours) if noms else "ses "
               "premiers ouvrages")
            + ". Le second œuvre, lui, commence au jour "
            f"{_f(pl['segments_de_travail']['SECO'][0][0], 0)} — plus de "
            f"{_f(pl['segments_de_travail']['SECO'][0][0] - f_fin, 0)} jours plus tard. "
            "**Le carnet de réservations se joue pendant le gros œuvre, par des gens qui "
            "ne seront plus là quand on s'en servira.**"),
        "date_d_arret_j": j_arret,
        "nb_zones": nb_zones,
        "cadence_j": cadence,
        "duree_du_plancher_j": duree_plancher,
        "_source_des_dates": "la dernière zone se coule à la fin du segment MEZZ que D2 "
                             "publie ; les autres remontent à la cadence que C3 calcule. "
                             "Aucune date n'est posée (D-039)",
        "surface_d_une_zone_m2": surface_zone,
        "delai_de_gel_j": delai,
        "delai_bornes_j": list(delai_b),
        "densite_par_m2": dens,
        "reservations_par_zone": round(surface_zone * dens, 1),
        "reservations_sur_le_plancher": round(surface_zone * nb_zones * dens, 0),
        "reservations_bornes": [round(surface_zone * nb_zones * dens_b[0], 0),
                                round(surface_zone * nb_zones * dens_b[1], 0)],
        "lignes": lignes,
        "nb_zones_gelees": len(gelees),
        "part_gelee_pct": round(len(gelees) / nb_zones * 100, 1),
        "_source_du_calendrier": "calc/sorties/planification.json — segments MEZZ (D2) et "
                                 "calc/sorties/gros-oeuvre.json — cycle (C3)",
        "lecture": (
            f"Le plancher compte {_f(surface_zone * nb_zones * dens, 0)} réservations "
            f"({_f(surface_zone * nb_zones * dens_b[0], 0)} à "
            f"{_f(surface_zone * nb_zones * dens_b[1], 0)}), réparties sur "
            f"{nb_zones} zones coulées tous les {_f(cadence, 1)} jours. Chaque carnet "
            f"gèle {_f(delai)} jours avant le coulage de sa zone : à la date d'arrêt, "
            f"{len(gelees)} zones sur {nb_zones} sont irrévocables, soit "
            f"{_f(len(gelees) / nb_zones * 100, 0)} % du plancher."),
        "_ce_que_le_gel_veut_dire": (
            "Après cette date, une réservation oubliée ne s'ajoute plus : elle se perce. "
            "Le carnet n'est donc pas un document de synthèse qu'on met à jour quand on a "
            "le temps — c'est une **échéance par zone**, et elle avance à la cadence du "
            "coulage. Un chef de projet suivi qui attend « la synthèse » pour figer les "
            "réservations a déjà perdu les zones coulées entre-temps."),
    }


# ------------------------------------------------- 3. ce que coûte un trou oublié
def cout_du_trou_oublie(d: dict) -> dict:
    """Une réservation prévue contre un percement après coup : le rapport, et ses postes."""
    r = d["lots_techniques"]["reservations"]
    prevue, prevue_b = (r["cout_d_une_reservation_prevue_MAD"]["valeur"],
                        _b(r["cout_d_une_reservation_prevue_MAD"]))
    postes = [(k, v["valeur"], _b(v), v["note"])
              for k, v in r["percement_apres_coup_MAD"].items() if k != "_role"]
    total = sum(x[1] for x in postes)
    total_b = [sum(x[2][0] for x in postes), sum(x[2][1] for x in postes)]
    return {
        "cout_d_une_reservation_prevue_MAD": prevue,
        "cout_d_une_reservation_bornes_MAD": list(prevue_b),
        "postes": [{"poste": k.replace("_", " "), "MAD": v, "bornes_MAD": list(b),
                    "part_pct": round(v / total * 100, 1), "note": n}
                   for k, v, b, n in postes],
        "cout_du_percement_MAD": round(total, 2),
        "cout_du_percement_bornes_MAD": [round(total_b[0], 2), round(total_b[1], 2)],
        "rapport": round(total / prevue, 1),
        "rapport_bornes": [round(total_b[0] / prevue_b[1], 1),
                           round(total_b[1] / prevue_b[0], 1)],
        "poste_le_plus_lourd": max(postes, key=lambda x: x[1])[0].replace("_", " "),
        "part_d_oublis_qui_egale_le_carnet_pct": round(prevue / total * 100, 1),
        "_le_seuil_d_equivalence": (
            f"Quelle part d'oublis coûterait, à elle seule, autant que l'ensemble du "
            f"carnet ? La réponse ne dépend pas du nombre de réservations : c'est "
            f"l'inverse du rapport, soit {_f(prevue / total * 100, 1)} %. En deçà, les "
            "oublis coûtent moins que le carnet ; au-delà, ils coûtent plus. C'est un "
            "repère commode, et il tient en une division."),
        "part_de_l_etude_pct": round(
            sum(v for k, v, _, _ in postes if k == "etude_et_visa") / total * 100, 1),
        "part_de_ce_qui_n_est_pas_le_trou_pct": round(
            sum(v for k, v, _, _ in postes if k not in ("carottage",
                                                        "detection_d_armatures"))
            / total * 100, 1),
        "lecture": (
            f"Une réservation prévue coûte {_f(prevue)} MAD. Le même trou percé après "
            f"coup en coûte {_f(total)} — un rapport de {_f(total / prevue, 1)}, et de "
            f"{_f(total_b[0] / prevue_b[1], 1)} à {_f(total_b[1] / prevue_b[0], 1)} sur "
            "les fourchettes."),
        "_ce_que_le_rapport_cache": (
            f"Le percement lui-même — carottage et détection d'armatures — ne fait que "
            f"{_f(sum(v for k, v, _, _ in postes if k in ('carottage', 'detection_d_armatures')) / total * 100, 0)} % "
            f"de la facture. L'étude et son visa en font "
            f"{_f(sum(v for k, v, _, _ in postes if k == 'etude_et_visa') / total * 100, 0)} % "
            "à eux seuls — plus que le carottage — et ce sont du temps d'ingénieur et une "
            "attente, pas une machine. Autrement dit, le "
            "percement coûte d'autant plus cher qu'on le fait tard — et le chiffre "
            "ci-dessus suppose un élément NON porteur et un second œuvre non terminé. "
            "Les deux hypothèses sautent souvent ensemble."),
        "_sur_un_element_porteur": (
            "Sur une poutre ou un voile porteur, ce n'est plus un coût : c'est une "
            "décision du bureau d'études, dont l'issue n'est pas acquise et dont le délai "
            "n'a rien à voir avec celui d'un carottage. Le module ne la chiffre pas, "
            "parce qu'elle est réglementaire (⏸) et parce qu'une moyenne n'aurait aucun "
            "sens : soit c'est accordé, soit il faut changer le tracé."),
    }


# ------------------------------------------------- 4. le second œuvre est une file
def file_forme_fermee(W: list, Z: int) -> float:
    """Durée d'une file de corps d'état sur Z zones, SANS coût de transition.

    Chaque corps i demande W_i jours sur la totalité du plancher, soit W_i / Z par zone.
    En régime pipeliné et sans transition, la file met la somme des durées d'une zone,
    plus (Z−1) fois la plus longue : l'avant-dernière zone attend toujours le corps le
    plus lent.

        T(Z) = ( ΣW + (Z−1)·max W ) / Z

    Cette forme est EXACTE — la simulation directe la retrouve au quinzième chiffre — et
    elle ne survit pas à l'ajout d'un coût de frontière : voir `file_simulee`.
    """
    if Z < 1:
        raise ValueError("au moins une zone")
    return (sum(W) + (Z - 1) * max(W)) / Z


def file_simulee(W: list, Z: int, f: float = 0.0) -> float:
    """La même file, AVEC un coût de réinstallation f à chaque changement de zone.

    Il n'y a pas de forme fermée simple, et c'est le point : **le coût de frontière ne
    s'ajoute pas au makespan**. Chaque corps paie f à chaque zone, mais seuls les jours
    du corps qui se trouve sur le chemin critique à ce moment-là se retrouvent dans la
    durée totale ; les autres sont absorbés par l'attente. Une première version de ce
    module ajoutait N·(Z−1)·f à la forme fermée : elle surestimait de 14 jours sur 64 à
    huit zones, et plaçait l'optimum à 7 zones là où il est à 18.

    On place donc les tâches une à une. Le corps i ne commence la zone z que lorsqu'il a
    fini la zone précédente (et s'y est réinstallé) ET que le corps i−1 a libéré la zone.
    """
    if Z < 1:
        raise ValueError("au moins une zone")
    N = len(W)
    d = [w / Z for w in W]
    fin_ = [[0.0] * Z for _ in range(N)]
    for z in range(Z):
        for i in range(N):
            pret_corps = fin_[i][z - 1] + f if z > 0 else 0.0
            pret_zone = fin_[i - 1][z] if i > 0 else 0.0
            fin_[i][z] = max(pret_corps, pret_zone) + d[i]
    return fin_[N - 1][Z - 1]


def second_oeuvre(d: dict, pl: dict, go: dict) -> dict:
    so = d["lots_techniques"]["second_oeuvre"]
    corps = so["corps_d_etat"]
    W = [c["duree_totale_j"]["valeur"] for c in corps]
    W_b = [_b(c["duree_totale_j"]) for c in corps]
    fr, fr_b = so["cout_de_frontiere_j"]["valeur"], _b(so["cout_de_frontiere_j"])
    Z0 = go["cycle"]["nb_zones"]
    declaree = pl["durees"]["SECO"]["duree_j"]
    goulot = max(corps, key=lambda c: c["duree_totale_j"]["valeur"])
    zc = d["geometrie"]["mezzanine"]["zones_de_coulage"]
    surface_mezzanine = zc["longueur_zone_m"] * zc["largeur_zone_m"] * zc["nb_zones"]
    surface_gare = d["geometrie"]["emprise_m"][0] * d["geometrie"]["emprise_m"][1]

    # La courbe va jusqu'a 30 zones : l'optimum reel se trouve au-dela de 24, et une
    # courbe qui s'arrete avant son minimum raconte le contraire de ce qu'elle montre.
    courbe = [{"x": z, "v": round(file_simulee(W, z, fr), 1)} for z in range(1, 31)]
    sans_frontiere = [{"x": z, "v": round(file_forme_fermee(W, z), 1)}
                      for z in range(1, 31)]
    meilleur = min(courbe, key=lambda p: p["v"])
    return {
        "corps": [{"corps": c["corps"], "duree_totale_j": c["duree_totale_j"]["valeur"],
                   "duree_par_zone_j": round(c["duree_totale_j"]["valeur"] / Z0, 2),
                   "bornes_j": list(b), "recoit_de": c["recoit_de"],
                   "support_a_receptionner": c["support_a_receptionner"],
                   "est_le_goulot": c["corps"] == goulot["corps"]}
                  for c, b in zip(corps, W_b)],
        "nb_corps": len(W),
        "somme_des_durees_j": round(sum(W), 1),
        "goulot": goulot["corps"],
        "duree_du_goulot_j": goulot["duree_totale_j"]["valeur"],
        "nb_zones_du_gros_oeuvre": Z0,
        "duree_en_serie_pure_j": round(file_simulee(W, 1, fr), 1),
        "duree_a_Z_zones_j": round(file_simulee(W, Z0, fr), 1),
        "duree_a_Z_zones_sans_frontiere_j": round(file_forme_fermee(W, Z0), 1),
        "plancher_incompressible_j": round(max(W), 1),
        "zone_optimale": meilleur["x"],
        "duree_optimale_j": meilleur["v"],
        # Le second oeuvre herite du decoupage du gros oeuvre. Ce qu'il en coute se
        # chiffre, et c'est une decision — pas une fatalite ni une evidence.
        "cout_de_reutiliser_le_decoupage_du_gros_oeuvre_j": round(
            file_simulee(W, Z0, fr) - meilleur["v"], 1),
        # L'optimum depend ENTIEREMENT du cout de frontiere, qui est une V3 a fourchette
        # large. On publie sa plage : une voie qui sert a decider porte ses bornes (D-059).
        "zone_optimale_bornes": [
            min(range(1, 61), key=lambda z: file_simulee(W, z, fr_b[1])),
            min(range(1, 61), key=lambda z: file_simulee(W, z, fr_b[0]))],
        "_l_optimum_n_est_pas_un_nombre": (
            "Le découpage optimal dépend entièrement du coût de frontière, et celui-ci "
            f"est une hypothèse déclarée de {_f(fr_b[0], 2)} à {_f(fr_b[1], 1)} jour par "
            "corps et par frontière. L'optimum va donc de "
            f"{min(range(1, 61), key=lambda z: file_simulee(W, z, fr_b[1]))} à "
            f"{min(range(1, 61), key=lambda z: file_simulee(W, z, fr_b[0]))} zones. "
            "**Ce n'est pas un nombre à retenir, c'est une forme à connaître** : une "
            "courbe en U dont le minimum se déplace avec le seul paramètre que personne "
            "ne mesure. Ce que le calcul dit de sûr, c'est que le minimum existe et que "
            f"le découpage hérité ({Z0} zones) n'est pas lui."),
        "_redecouper_ou_pas": (
            f"Le gros œuvre a découpé le plancher en {Z0} zones de coulage, pour des "
            "raisons qui lui appartiennent — une zone se coule en une demi-journée de "
            "pompe. Le second œuvre hérite de ce découpage sans l'avoir choisi, et "
            f"l'optimum de SA file est à {meilleur['x']} zones. La différence vaut "
            f"{_f(file_simulee(W, Z0, fr) - meilleur['v'], 1)} jours, soit "
            f"{_f((file_simulee(W, Z0, fr) / meilleur['v'] - 1) * 100, 0)} %. **C'est un "
            "arbitrage, pas une évidence** : redécouper veut dire gérer deux maillages "
            "sur le même plancher, deux jeux de réceptions de support et deux listes de "
            "réserves. Le calcul donne le prix de la simplicité ; il ne dit pas qu'elle "
            "est trop chère."),
        # LE PERIMETRE, et c'est lui qui interdit la comparaison. La duree declaree par
        # D2 couvre le second oeuvre de TOUTE la gare ; la decomposition ci-dessus ne
        # couvre que le plancher de mezzanine, decoupe en zones de coulage. Une premiere
        # version annoncait « deux voies qui s'accordent a 4 % » : elle comparait 2 880 m2
        # a 4 800, et deux jeux de parametres poses au meme moment. Ce n'etait ni
        # independant ni du meme domaine (D-037, D-043).
        "duree_declaree_par_D2_j": declaree,
        "perimetre_de_la_decomposition_m2": round(surface_mezzanine, 0),
        "perimetre_de_D2_m2": round(surface_gare, 0),
        "_pourquoi_on_ne_compare_pas": (
            f"Le module D2 donne {_f(declaree)} jours au second œuvre de la gare entière "
            f"({_f(surface_gare, 0)} m² d'emprise). La décomposition ci-dessus ne décrit "
            f"que le plancher de mezzanine ({_f(surface_mezzanine, 0)} m²), parce que "
            "c'est le seul ouvrage dont ce cours connaisse le découpage en zones. **Les "
            "deux nombres ne sont pas comparables**, et les rapprocher donnerait un "
            "accord ou un désaccord également dénués de sens. Ce que la décomposition "
            "apporte n'est donc pas une vérification de D2 : c'est un MODÈLE du second "
            "œuvre — une file, un goulot, un optimum de découpage — qu'on peut appliquer "
            "à l'un comme à l'autre une fois le périmètre fixé."),
        "gain_du_decoupage_pct": round(
            (1 - file_simulee(W, Z0, fr) / file_simulee(W, 1, fr)) * 100, 1),
        "cout_de_frontiere_j": fr,
        "cout_de_frontiere_bornes_j": list(fr_b),
        "courbe": courbe,
        "courbe_sans_frontiere": sans_frontiere,
        "lecture": (
            f"Les {len(W)} corps d'état demandent {_f(sum(W))} jours s'ils se suivent sur "
            f"la totalité du plancher. Découpé en {Z0} zones, le même travail en demande "
            f"{_f(file_simulee(W, Z0, fr), 0)}. Sans coût de frontière, découper "
            f"à l'infini ferait tendre la file vers {_f(max(W))} jours — la durée du corps "
            f"le plus lent, {goulot['corps'].lower()} — et jamais en dessous. Avec le coût "
            f"de frontière, le meilleur découpage possible est à {meilleur['x']} zones et "
            f"{_f(meilleur['v'], 0)} jours."),
        "_la_forme_fermee": (
            "T(Z) = (ΣW + (Z−1)·max W) / Z + N·(Z−1)·f. Le premier terme décroît avec le "
            "nombre de zones et tend vers max W : **le découpage ne fait pas de miracle, "
            "il rattrape le temps perdu par les corps d'état qui attendent, et rien de "
            "plus.** Le second terme croît : chaque frontière oblige chaque corps à se "
            "réinstaller. L'optimum n'est donc pas le découpage le plus fin."),
        "_ce_que_le_goulot_impose": (
            f"Le corps le plus lent — {goulot['corps'].lower()}, {_f(max(W))} jours — fixe "
            "le plancher de toute la file. Accélérer n'importe quel autre corps ne change "
            "rien au-delà de la première zone : ce sont des jours gagnés sur une file qui "
            "attend ailleurs. **La seule question utile sur un second œuvre en retard est "
            "donc : qui est le goulot, et qu'est-ce qui le ralentit ?** Et la réponse, "
            "ici, n'est pas un corps d'état unique mais quatre lots qui partagent le même "
            "plénum."),
    }


# ------------------------------------------------- 5. la réception des supports
def chaine_des_supports(so: dict) -> dict:
    """Qui reçoit quoi de qui — et ce qu'un support non conforme coûte à la file.

    Chaque corps d'état reçoit un support du précédent. S'il le refuse, il attend ; s'il
    l'accepte alors qu'il est mauvais, le défaut est scellé sous son ouvrage. C'est la
    seule décision de la journée qui soit irréversible, et elle se prend sur un seuil
    qu'aucun des deux n'a écrit.
    """
    lignes = [{"corps": c["corps"], "recoit_de": c["recoit_de"],
               "support": c["support_a_receptionner"],
               "est_le_goulot": c["est_le_goulot"]} for c in so["corps"]]
    return {
        "lignes": lignes,
        "nb_receptions": len(lignes),
        "_la_regle": (
            "Une réception de support n'est pas une formalité entre entreprises : c'est le "
            "moment où la responsabilité change de main. Celui qui pose sur un support "
            "qu'il n'a pas refusé le reprend à son compte — et il le découvre à la "
            "réception de l'ouvrage, quand son travail recouvre le défaut de l'autre."),
        "_ce_qui_la_rend_difficile": (
            "Refuser coûte des jours à soi-même et accepter coûte des reprises à "
            "l'arrivée : les deux coûts ne tombent pas sur la même personne ni au même "
            "moment. C'est la définition d'un arbitrage mal posé, et c'est le rôle du "
            "chef de projet suivi de le reposer — en écrivant le critère AVANT, pas en "
            "arbitrant le jour même entre deux entreprises qui ont chacune raison."),
        "_le_seul_critere_qui_tienne": (
            "Un critère de réception de support se formule en une phrase vérifiable par "
            "les deux parties, avec un instrument : une règle de 2 m et un réglet pour "
            "une planéité, un humidimètre pour un sol, un mètre pour une implantation. "
            "Les valeurs, elles, sont contractuelles ou normatives : ⏸. Ce que le suivi "
            "peut exiger sans attendre personne, c'est que le critère soit ÉCRIT et "
            "l'instrument PRÉSENT le jour de la réception."),
    }


# ------------------------------------------------- 6. figures
def figures(pa: dict, gel: dict, cout: dict, so: dict) -> dict:
    return {
        # Ce qui passe entre deux armatures, endroit par endroit, avec le diamètre
        # qui ne passe nulle part en repère.
        "passages": [{"libelle": e["endroit"].replace(" — ", " · "),
                      "valeur": e["passage_libre_mm"],
                      "alerte": e["plus_gros_diametre_qui_passe_mm"] is None
                      or e["plus_gros_diametre_qui_passe_mm"] < 160}
                     for e in pa["endroits"]],
        # De la date de GEL a la date de COULAGE : la fenetre pendant laquelle une
        # reservation existe encore sur le papier mais plus dans le coffrage.
        "gel": [{"nom": f"Zone {x['zone']} — {_f(x['reservations'], 0)} réservations",
                 "debut": x["date_de_gel_j"],
                 "duree": round(x["date_de_coulage_j"] - x["date_de_gel_j"], 2),
                 "critique": False} for x in gel["lignes"]],
        "cout": [{"libelle": p["poste"].capitalize(),
                  "montant": round(p["MAD"])} for p in cout["postes"]]
        + [{"libelle": "Percement après coup", "montant": round(cout["cout_du_percement_MAD"]),
            "type": "total"}],
        "corps": [{"libelle": _court(c["corps"], 34), "valeur": c["duree_totale_j"],
                   "alerte": c["est_le_goulot"]} for c in so["corps"]],
        # La durée de la file en fonction du nombre de zones : une décroissance qui bute
        # sur un plancher, et une remontée quand les frontières l'emportent.
        "file": so["courbe"],
        "marqueur_zones": {"x": so["nb_zones_du_gros_oeuvre"],
                           "libelle": f"{so['nb_zones_du_gros_oeuvre']} zones de coulage "
                                      f"→ {_f(so['duree_a_Z_zones_j'], 0)} j"},
    }


# ------------------------------------------------- assemblage
def tout_calculer(d: dict) -> dict:
    S = RACINE / "calc" / "sorties"
    fer = json.loads((S / "ferraillage.json").read_text(encoding="utf-8"))
    pl = json.loads((S / "planification.json").read_text(encoding="utf-8"))
    su = json.loads((S / "suivi.json").read_text(encoding="utf-8"))
    go = json.loads((S / "gros-oeuvre.json").read_text(encoding="utf-8"))
    pa = passage_libre(d, fer)
    gel = gel_des_reservations(d, pl, su, go)
    cout = cout_du_trou_oublie(d)
    so = second_oeuvre(d, pl, go)
    return {
        "passage_libre": pa,
        "gel_des_reservations": gel,
        "cout_du_trou_oublie": cout,
        "second_oeuvre": so,
        "chaine_des_supports": chaine_des_supports(so),
        "figures": figures(pa, gel, cout, so),
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    r = tout_calculer(d)
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "synthese.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for e in r["passage_libre"]["endroits"]:
        print(f"  {e['endroit'][:46]:<48} libre {e['passage_libre_mm']:>6.1f} mm · "
              f"passe jusqu'a {e['plus_gros_diametre_qui_passe_mm']} mm")
    print(f"ne passe nulle part : {r['passage_libre']['diametres_qui_ne_passent_nulle_part_mm']} mm")
    g = r["gel_des_reservations"]
    print(f"gel : {g['nb_zones_gelees']}/{g['nb_zones']} zones gelees a la date d'arret · "
          f"{g['reservations_sur_le_plancher']:.0f} reservations")
    c = r["cout_du_trou_oublie"]
    print(f"trou oublie : {c['cout_du_percement_MAD']:.0f} contre "
          f"{c['cout_d_une_reservation_prevue_MAD']} MAD — x{c['rapport']} "
          f"{c['rapport_bornes']}")
    s = r["second_oeuvre"]
    print(f"second oeuvre : serie {s['duree_en_serie_pure_j']} j · {s['nb_zones_du_gros_oeuvre']} "
          f"zones {s['duree_a_Z_zones_j']} j · plancher {s['plancher_incompressible_j']} j · "
          f"optimum {s['zone_optimale']} zones a {s['duree_optimale_j']} j · D2 dit "
          f"{s['duree_declaree_par_D2_j']}")
