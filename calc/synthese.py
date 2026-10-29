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


def _b(o: dict) -> tuple[float, float]:
    f = o.get("fourchette")
    return (float(f[0]), float(f[1])) if f else (float(o["valeur"]), float(o["valeur"]))


# ------------------------------------------------- 1. ce qui passe entre deux armatures
def passage_libre(d: dict, fer: dict) -> dict:
    """Le plus gros fourreau qui passe sans toucher une armature, endroit par endroit.

    C'est de la géométrie pure : l'espace libre entre deux armatures parallèles vaut leur
    espacement moins le diamètre de l'une d'elles. Rien de normatif là-dedans — la règle
    qui dit si l'on a le DROIT de percer là est, elle, réglementaire (⏸).
    """
    lt = d["lots_techniques"]["reservations"]
    dias = lt["diametres_courants_mm"]
    endroits = []
    for z in fer["cadres"]["zones"]:
        esp = z["espacement_cm"] * 10
        dia_cadre = fer["cadres"]["dia_mm"]
        endroits.append({
            "endroit": f"Poutre — {z['nom']}",
            "armatures": f"cadres HA{dia_cadre} à {_f(z['espacement_cm'])} cm",
            "espacement_mm": esp,
            "dia_armature_mm": dia_cadre,
            "passage_libre_mm": round(esp - dia_cadre, 1),
            "longueur_concernee_m": z["longueur_m"],
        })
    for ligne in fer["nappes"]["lignes"][:2]:
        esp = ligne["espacement_cm"] * 10
        endroits.append({
            "endroit": f"Dalle — {ligne['role']}",
            "armatures": f"HA{ligne['dia_mm']} à {_f(ligne['espacement_cm'], 1)} cm",
            "espacement_mm": esp,
            "dia_armature_mm": ligne["dia_mm"],
            "passage_libre_mm": round(esp - ligne["dia_mm"], 1),
            "longueur_concernee_m": None,
        })
    for e in endroits:
        # Le plus gros diamètre du catalogue qui tient dans l'espace libre.
        passe = [x for x in dias if x <= e["passage_libre_mm"]]
        e["plus_gros_diametre_qui_passe_mm"] = max(passe) if passe else None
        e["diametres_qui_passent"] = passe
        e["diametres_qui_ne_passent_pas"] = [x for x in dias if x > e["passage_libre_mm"]]
    pire = min(endroits, key=lambda e: e["passage_libre_mm"])
    # Le diamètre qui ne passe NULLE PART : le premier du catalogue au-dessus du plus
    # grand des passages libres.
    meilleur = max(e["passage_libre_mm"] for e in endroits)
    nulle_part = [x for x in dias if x > meilleur]
    return {
        "endroits": endroits,
        "passage_le_plus_etroit_mm": pire["passage_libre_mm"],
        "endroit_le_plus_etroit": pire["endroit"],
        "passage_le_plus_large_mm": meilleur,
        "diametres_qui_ne_passent_nulle_part_mm": nulle_part,
        "_source_des_armatures": "calc/sorties/ferraillage.json — cadres et nappes du "
                                 "module B3e. Aucun espacement n'est redéclaré ici (D-039)",
        "lecture": (
            f"L'espace libre entre deux armatures va de {_f(pire['passage_libre_mm'])} mm "
            f"({pire['endroit'].lower()}) à {_f(meilleur)} mm. Un fourreau de "
            f"{_f(nulle_part[0])} mm — un diamètre courant de désenfumage ou d'eaux "
            "usées — ne passe donc **nulle part** sans toucher une armature."
            if nulle_part else
            f"L'espace libre va de {_f(pire['passage_libre_mm'])} à {_f(meilleur)} mm : "
            "tous les diamètres du catalogue passent quelque part."),
        "_ce_que_ce_nombre_ne_dit_pas": (
            "Qu'un fourreau tienne entre deux armatures ne veut pas dire qu'on a le droit "
            "de le mettre là. La position admissible d'une réservation dans un élément "
            "porteur, sa section maximale, sa distance aux appuis et aux armatures "
            "principales sont **réglementaires** : ⏸. Ce calcul répond à une question plus "
            "modeste et toujours utile — **est-ce seulement géométriquement possible ?** "
            "Quand la réponse est non, la discussion avec le bureau d'études n'a pas lieu "
            "d'être : il faut changer de tracé."),
        "_la_vraie_frontiere": (
            "Une réservation qui coupe un cadre n'est pas une réservation. C'est une "
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
    for i in range(nb_zones):
        coulage = debut + (i + 1) * cadence
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
        "part_sans_outil_pct": round(
            sum(v for k, v, _, _ in postes
                if k in ("etude_et_visa", "remise_en_etat_des_abords")) / total * 100, 1),
        "lecture": (
            f"Une réservation prévue coûte {_f(prevue)} MAD. Le même trou percé après "
            f"coup en coûte {_f(total)} — un rapport de {_f(total / prevue, 1)}, et de "
            f"{_f(total_b[0] / prevue_b[1], 1)} à {_f(total_b[1] / prevue_b[0], 1)} sur "
            "les fourchettes."),
        "_ce_que_le_rapport_cache": (
            f"{_f(sum(v for k, v, _, _ in postes if k in ('etude_et_visa', 'remise_en_etat_des_abords')) / total * 100, 0)} % "
            "de ce coût ne tiennent ni à la machine ni à l'ouvrier : ce sont l'étude, le "
            "visa et la remise en état des ouvrages déjà posés autour. Autrement dit, le "
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
def file_de_corps_d_etat(W: list, Z: int, frontiere: float = 0.0) -> float:
    """Durée d'une file de corps d'état sur Z zones, forme fermée.

    Chaque corps i demande W_i jours sur la totalité du plancher, soit W_i / Z par zone.
    En régime pipeliné, la file met la somme des durées d'une zone, plus (Z−1) fois la
    plus longue : l'avant-dernière zone attend toujours le corps le plus lent.

        T(Z) = ( ΣW + (Z−1)·max W ) / Z   +   N·(Z−1)·coût de frontière

    Le premier terme décroît avec Z et tend vers max W : **aucun découpage ne descend
    sous la durée du corps le plus lent.** Le second croît avec Z. L'optimum existe.
    """
    if Z < 1:
        raise ValueError("au moins une zone")
    return (sum(W) + (Z - 1) * max(W)) / Z + len(W) * (Z - 1) * frontiere


def second_oeuvre(d: dict, pl: dict, go: dict) -> dict:
    so = d["lots_techniques"]["second_oeuvre"]
    corps = so["corps_d_etat"]
    W = [c["duree_totale_j"]["valeur"] for c in corps]
    W_b = [_b(c["duree_totale_j"]) for c in corps]
    fr, fr_b = so["cout_de_frontiere_j"]["valeur"], _b(so["cout_de_frontiere_j"])
    Z0 = go["cycle"]["nb_zones"]
    declaree = pl["durees"]["SECO"]["duree_j"]
    goulot = max(corps, key=lambda c: c["duree_totale_j"]["valeur"])

    courbe = [{"x": z, "v": round(file_de_corps_d_etat(W, z, fr), 1)}
              for z in range(1, 25)]
    sans_frontiere = [{"x": z, "v": round(file_de_corps_d_etat(W, z), 1)}
                      for z in range(1, 25)]
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
        "duree_en_serie_pure_j": round(file_de_corps_d_etat(W, 1), 1),
        "duree_a_Z_zones_j": round(file_de_corps_d_etat(W, Z0, fr), 1),
        "duree_a_Z_zones_sans_frontiere_j": round(file_de_corps_d_etat(W, Z0), 1),
        "plancher_incompressible_j": round(max(W), 1),
        "zone_optimale": meilleur["x"],
        "duree_optimale_j": meilleur["v"],
        "duree_declaree_par_D2_j": declaree,
        "ecart_avec_D2_j": round(file_de_corps_d_etat(W, Z0, fr) - declaree, 1),
        "cout_de_frontiere_j": fr,
        "cout_de_frontiere_bornes_j": list(fr_b),
        "courbe": courbe,
        "courbe_sans_frontiere": sans_frontiere,
        "lecture": (
            f"Les {len(W)} corps d'état demandent {_f(sum(W))} jours s'ils se suivent sur "
            f"la totalité du plancher. Découpé en {Z0} zones, le même travail en demande "
            f"{_f(file_de_corps_d_etat(W, Z0, fr), 0)}. Sans coût de frontière, découper "
            f"à l'infini ferait tendre la file vers {_f(max(W))} jours — la durée du corps "
            f"le plus lent, {goulot['corps'].lower()} — et jamais en dessous. Avec le coût "
            f"de frontière, le meilleur découpage possible est à {meilleur['x']} zones et "
            f"{_f(meilleur['v'], 0)} jours. Le module D2 déclare {_f(declaree)} jours."),
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
        "corps": [{"libelle": c["corps"][:34], "valeur": c["duree_totale_j"],
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
