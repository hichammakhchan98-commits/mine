"""Gros oeuvre : le cycle, le parc de coffrage et le betonnage par temps chaud (C3).

Le lecteur maitrise l'execution du beton arme : ce module ne lui reapprend ni ce qu'est
une banche ni comment on vibre. Il traite trois choses qu'un manuel d'execution ne donne
pas, et qui decident d'un cycle :

1. Le cycle n'est pas une duree, c'est une contrainte de RESSOURCE. Le module TV a
   trouve l'equipe qui borne ; celui-ci ajoute la contrainte qu'on oublie le plus
   souvent — le PARC DE COFFRAGE — et montre qu'elle peut devenir la premiere.
2. Le parc optimal n'est pas le plus grand ni le plus petit : c'est celui qui minimise
   la somme du loyer et des frais de duree. Et sur CE chantier, l'optimum n'est pas
   celui qu'on croit, parce que le plancher n'est pas ce qui porte la date.
3. Par temps chaud, ce n'est pas la cadence des equipes qui commande le betonnage,
   c'est le TEMPS DE MANIABILITE : le debit minimal pour eviter une reprise froide se
   calcule, et il decide du nombre de toupies.
"""
from __future__ import annotations
import json, math, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import planification as pln                                              # noqa: E402
import prix as px                                                        # noqa: E402
import plancher as plc                                                   # noqa: E402
import cycle_plancher as cy                                              # noqa: E402


# ------------------------------------------------------------ le parc de coffrage
def duree_coffree(d: dict, reseau: list, debuts: dict) -> dict:
    """Combien de temps une zone IMMOBILISE du coffrage.

    Ce n'est pas la duree du cycle : le coffrage est pose au debut et depose a la fin,
    mais il n'est pas rendu entre les deux. La grandeur qui compte va du debut du
    coffrage a la fin du decoffrage — cure comprise, et c'est la cure qui pese.
    """
    par_id = {t.id: t for t in reseau}
    deb = debuts["COF"]
    fin = debuts["DEC"] + par_id["DEC"].duree
    return {"de_j": round(deb, 2), "a_j": round(fin, 2),
            "duree_j": round(fin - deb, 2),
            "dont_cure_j": par_id["CUR"].duree,
            "part_de_cure_pct": round(par_id["CUR"].duree / (fin - deb) * 100, 1),
            "lecture": (
                "La cure occupe le coffrage sans occuper personne. C'est la raison pour "
                "laquelle un parc se dimensionne sur la duree d'immobilisation et non "
                "sur la duree de travail : raccourcir une equipe ne libere pas une table.")}


def cadence_bornee_par_le_parc(parc_m2: float, surface_zone_m2: float,
                               immobilisation_j: float) -> dict:
    """La cadence minimale qu'un parc donne permet.

    Si une zone immobilise le coffrage pendant I jours et qu'on en demarre une tous les
    T jours, il y a I/T zones coffrees en meme temps. Le parc doit les porter :

        parc >= ceil(I / T) x surface_zone    =>    T >= I / (parc / surface_zone)

    Le ceil compte : un parc de 2,6 zones n'en porte que deux.
    """
    zones = math.floor(parc_m2 / surface_zone_m2 + 1e-9)
    if zones < 1:
        return {"parc_m2": parc_m2, "zones_simultanees": 0, "cadence_min_j": None,
                "faisable": False,
                "note": "le parc ne couvre meme pas une zone : le cycle est impossible"}
    return {"parc_m2": parc_m2, "zones_simultanees": zones,
            "cadence_min_j": round(immobilisation_j / zones, 2), "faisable": True}


def optimum_du_parc(d: dict, q: dict, regle: dict, immobilisation: dict,
                    nb_zones: int, cycle_j: float, frais_par_mois: float,
                    jours_ouvres_par_mois: float, critique: bool,
                    marge_j: float) -> dict:
    """Le parc qui minimise la somme du loyer et des frais de duree.

    Trois termes, et le troisieme est celui qu'on oublie :
      - le LOYER du parc, proportionnel a sa taille ET a la duree ;
      - le MONTAGE, proportionnel a sa taille seulement ;
      - les FRAIS DE DUREE du chantier, proportionnels a la duree seulement — et ils ne
        bougent QUE si le plancher porte la date du chantier.

    C'est ce dernier point qui renverse la conclusion sur ce chantier-ci.
    """
    g = d["gros_oeuvre"]["coffrage"]
    loyer = g["location_MAD_m2_mois"]["valeur"]
    montage = g["montage_demontage_MAD_m2"]["valeur"]
    surf = regle["surface_zone_m2"]
    # duree de reference : celle que les equipes tiennent quand le parc ne borne pas
    duree_reference = (nb_zones - 1) * regle["cadence_j"] + cycle_j
    lignes = []
    for parc in g["parcs_a_comparer_m2"]:
        b = cadence_bornee_par_le_parc(parc, surf, immobilisation["duree_j"])
        if not b["faisable"]:
            lignes.append({**b, "retenue": False})
            continue
        # la cadence reellement tenue est la plus CONTRAIGNANTE des deux bornes
        cad = max(regle["cadence_j"], b["cadence_min_j"])
        duree = (nb_zones - 1) * cad + cycle_j
        mois = duree / jours_ouvres_par_mois
        cout_parc = parc * loyer * mois + parc * montage
        # Ce que l'allongement coute DEPEND DE LA MARGE. Tant qu'il tient dedans, il ne
        # coute rien au chantier ; au-dela, il repousse la fin et les frais de duree
        # courent sur le depassement. Ignorer la marge faisait choisir le plus petit
        # parc possible, qui doublait la duree du plancher sans cout apparent.
        rallonge = max(0.0, duree - duree_reference)
        depassement = max(0.0, rallonge - marge_j)
        cout_duree = (frais_par_mois * depassement / jours_ouvres_par_mois
                      if (critique or depassement > 0) else 0.0)
        lignes.append({
            "parc_m2": parc, "zones_simultanees": b["zones_simultanees"],
            "cadence_du_parc_j": b["cadence_min_j"],
            "cadence_des_equipes_j": regle["cadence_j"],
            "cadence_tenue_j": round(cad, 2),
            "ce_qui_borne": ("le parc de coffrage" if b["cadence_min_j"] > regle["cadence_j"]
                             else "les equipes"),
            "duree_du_plancher_j": round(duree, 2),
            "rallonge_j": round(rallonge, 2),
            "marge_consommee_j": round(min(rallonge, marge_j), 2),
            "marge_restante_j": round(max(0.0, marge_j - rallonge), 2),
            "depassement_j": round(depassement, 2),
            "loyer_et_montage_MAD": round(cout_parc, 2),
            "frais_de_duree_MAD": round(cout_duree, 2),
            "total_MAD": round(cout_parc + cout_duree, 2),
        })
    retenues = [x for x in lignes if x.get("total_MAD") is not None]
    best = min(retenues, key=lambda x: x["total_MAD"])
    for x in lignes:
        x["optimum"] = x is best
    # le parc actuellement declare dans data/, pour comparaison
    actuel = d["materiel"]["tables_coffrantes_m2"]
    b_act = cadence_bornee_par_le_parc(actuel, surf, immobilisation["duree_j"])
    cad_act = max(regle["cadence_j"], b_act["cadence_min_j"])
    return {
        "lignes": lignes, "optimum": best,
        "duree_de_reference_j": round(duree_reference, 2),
        "marge_disponible_j": marge_j,
        "parc_declare_m2": actuel,
        "cadence_du_parc_declare_j": b_act["cadence_min_j"],
        "le_parc_declare_borne_t_il": b_act["cadence_min_j"] > regle["cadence_j"],
        "le_plancher_porte_t_il_la_date": critique,
        "lecture": (
            "Le parc optimal minimise la SOMME du loyer et de ce que l'allongement "
            "coute. Et l'allongement ne coute RIEN tant qu'il tient dans la marge du "
            "plancher : c'est la marge, et non le delai, qu'un parc plus petit achete. "
            "Au-dela, chaque jour de depassement repousse la fin du chantier et fait "
            "courir les frais de duree. L'optimum est donc le plus petit parc dont "
            "l'allongement reste dans la marge — et il est tres en dessous du reflexe "
            "de chantier, qui est de commander large."),
        "ce_que_le_calcul_ne_price_pas": (
            "Une marge depensee en loyer de coffrage n'est plus disponible pour l'alea. "
            "Ce calcul la traite comme gratuite jusqu'a epuisement, ce qui est vrai au "
            "sens comptable et faux au sens du risque. Le choix du parc le plus serre "
            "revient a parier qu'il n'y aura pas d'alea sur le plancher — un pari qui "
            "ne figure sur aucune ligne du bordereau."),
    }


# ------------------------------------------------------ betonnage par temps chaud
def debit_minimal(d: dict, q: dict) -> dict:
    """Le debit qu'il faut tenir pour ne pas creer de reprise froide.

    Une couche de beton accepte d'etre vibree avec la suivante pendant un certain temps.
    Passe ce delai, la vibration ne melange plus les deux : il se forme un plan de
    faiblesse qui n'etait pas prevu, et qui ne se repare pas. A 35 °C ce delai tombe de
    moitie par rapport a 20 °C — c'est le regime dimensionnant d'un ete marocain.

        debit minimal = surface x epaisseur de couche / temps de maniabilite

    Le debit ne depend donc NI de l'effectif NI de la cadence du chantier. C'est une
    contrainte physique, et c'est elle qui decide du nombre de toupies.
    """
    b = d["gros_oeuvre"]["betonnage_temps_chaud"]
    cz = d["geometrie"]["mezzanine"]["zones_de_coulage"]
    larg = b["largeur_de_bande_m"]["valeur"]
    # une bande traverse la zone dans sa plus petite dimension
    traverse = min(cz["longueur_zone_m"], cz["largeur_zone_m"])
    ep_dalle = d["geometrie"]["mezzanine"]["dalle"]["epaisseur_m"] \
        if "dalle" in d["geometrie"]["mezzanine"] else q["beton_dalle_m3"] / q["surface_m2"]
    vol_bande = larg * traverse * ep_dalle
    out = {}
    for cle in ("a_20_degres", "a_30_degres", "a_35_degres"):
        t = b["temps_de_maniabilite_h"][cle]["valeur"]
        # la bande suivante doit rejoindre la precedente avant la fin du delai
        out[cle] = {"temps_de_maniabilite_h": t,
                    "debit_minimal_m3_h": round(vol_bande / t, 1)}
    ref = out["a_35_degres"]["debit_minimal_m3_h"]
    pompe = b["debit_pompe_m3_h"]["valeur"]
    vol_toupie = b["volume_toupie_m3"]["valeur"]
    rot = b["rotation_toupie_min"]["valeur"]
    # une toupie livre son volume par rotation complete
    debit_par_toupie = vol_toupie / (rot / 60)
    n_toupies = math.ceil(ref / debit_par_toupie)
    n_pompes = math.ceil(ref / pompe)
    # Le debit minimal est un PLANCHER, pas le debit qu'on tient : il interdit la
    # reprise froide, il ne dit rien de l'heure a laquelle on finit. Le debit tenu est
    # celui de la rotation des toupies, plafonne par la pompe — et c'est lui qui decide
    # si le coulage se termine avant la chaleur.
    options = []
    for n in range(n_toupies, n_toupies + 8):
        tenu = min(pompe, n * debit_par_toupie)
        options.append({"toupies": n, "debit_tenu_m3_h": round(tenu, 1),
                        "duree_du_coulage_h": round(q["beton_m3"] / tenu, 2),
                        "au_dessus_du_minimum": bool(tenu >= ref),
                        "borne_par": "la pompe" if n * debit_par_toupie > pompe
                                     else "la rotation des toupies"})
        if tenu >= pompe - 1e-9:
            break
    cible = b["duree_cible_du_coulage_h"]["valeur"]
    choisie = next((o for o in options if o["duree_du_coulage_h"] <= cible), options[-1])
    return {
        "surface_zone_m2": q["surface_m2"],
        "largeur_de_bande_m": larg, "longueur_de_bande_m": traverse,
        "epaisseur_de_dalle_m": round(ep_dalle, 3),
        "volume_d_une_bande_m3": round(vol_bande, 2),
        "nb_de_bandes": math.ceil(max(cz["longueur_zone_m"], cz["largeur_zone_m"]) / larg),
        "par_temperature": out,
        "temperature_de_calcul_C": b["temperature_de_calcul_C"]["valeur"],
        "debit_dimensionnant_m3_h": ref,
        "_modele": b["_modele"],
        "debit_pratique_d_une_pompe_m3_h": pompe,
        "pompes_necessaires": n_pompes,
        "debit_d_une_toupie_m3_h": round(debit_par_toupie, 2),
        "toupies_pour_tenir_le_minimum": n_toupies,
        "options_de_rotation": options,
        "duree_cible_du_coulage_h": cible,
        "option_retenue": choisie,
        "toupies_retenues": choisie["toupies"],
        "duree_du_coulage_h": choisie["duree_du_coulage_h"],
        "volume_de_la_zone_m3": q["beton_m3"],
        "deux_contraintes": (
            f"Le debit MINIMAL de {ref:.1f} m3/h interdit la reprise froide entre deux "
            f"bandes : en dessous, la bande precedente a pris. Il se tient avec "
            f"{n_toupies} toupies, et le coulage dure alors "
            f"{options[0]['duree_du_coulage_h']:.1f} h — ce qui le fait finir en pleine "
            f"chaleur. Le debit TENU, lui, decide de l'heure de fin : avec "
            f"{choisie['toupies']} toupies on coule en {choisie['duree_du_coulage_h']:.1f} h. "
            "Les deux contraintes ne disent pas la meme chose, et c'est la seconde qui "
            "commande la commande de camions."),
        "rapport_35_sur_20": round(
            out["a_35_degres"]["debit_minimal_m3_h"]
            / out["a_20_degres"]["debit_minimal_m3_h"], 2),
        "ce_qui_borne": choisie["borne_par"],
        "lecture": (
            f"A {b['temperature_de_calcul_C']['valeur']} °C, il faut tenir "
            f"{ref:.0f} m3/h — "
            f"{round(out['a_35_degres']['debit_minimal_m3_h'] / out['a_20_degres']['debit_minimal_m3_h'], 1)} "
            "fois plus qu'a 20 °C — sous peine de reprise froide. Ce n'est pas une "
            "question de cadence : c'est une course contre la prise. Une pompe qui tombe "
            "en panne a mi-coulage ne fait pas perdre une demi-journee, elle cree un "
            "defaut dans l'ouvrage."),
        "parade_si_le_debit_n_est_pas_tenable": (
            "Trois parades, dans l'ordre de ce qu'elles coutent : couler aux heures "
            "fraiches (nuit ou petit matin) ; refroidir le beton (granulats arroses, eau "
            "refrigeree, glace) ; ou DECOUPER la zone en sous-zones avec une reprise "
            "PREVUE, traitee comme telle — une reprise prevue est un detail d'execution, "
            "une reprise subie est un desordre."),
    }


def fenetre_de_coulage(d: dict, deb: dict) -> dict:
    """A quelle heure demarrer un coulage pour qu'il finisse avant la chaleur.

    Non normatif et tres concret : c'est la decision que prend un chef de chantier la
    veille, et elle depend d'une duree de coulage qu'on vient de calculer.
    """
    duree = deb["duree_du_coulage_h"]
    return {
        "duree_du_coulage_h": duree,
        "demarrage_conseille": "05:30",
        "fin_attendue": f"{5 + int(duree + .5)}h{'30' if (duree % 1) < .5 else '00'} environ",
        "regle": (
            "On fait tenir le coulage dans la premiere moitie de la matinee, avant que "
            "la temperature du beton frais ne monte. Ce qui decide de l'heure de "
            "demarrage, ce n'est pas l'horaire de l'equipe : c'est l'heure a laquelle on "
            "veut avoir FINI."),
    }


# ------------------------------------------------------------ points d'arret
def points_d_arret(d: dict, reseau: list) -> dict:
    """Les points d'arret du cycle, avec leur duree et leur double lecture.

    Un point d'arret est une TACHE : il a une duree, il est sur le chemin critique du
    cycle, et il se planifie. Le traiter comme une formalite est la facon la plus simple
    de le faire sauter — et un point d'arret saute toujours dans le meme sens, celui qui
    arrange la rotation.
    """
    pa = d["gros_oeuvre"]["points_d_arret"]["valeur"]
    par_id = {t.id: t for t in reseau}
    total = sum(x["duree_j"] for x in pa)
    return {
        "liste": pa, "nombre": len(pa),
        "duree_totale_j": round(total, 3),
        "duree_dans_le_cycle_j": par_id["PTA"].duree,
        "part_du_cycle_pct": round(par_id["PTA"].duree / sum(
            t.duree for t in reseau if t.id in ("COF", "FEP", "FED", "PTA", "BET", "CUR", "DEC")
        ) * 100, 1),
        "double_lecture": {
            "entreprise": (
                "Prevoir le point d'arret au planning avec sa duree, et prevenir la "
                "maitrise d'oeuvre la veille. Un visa demande le matin pour couler "
                "l'apres-midi n'est pas un visa, c'est une pression — et il sera refuse "
                "ou donne a la legere, les deux etant mauvais."),
            "maitrise_d_oeuvre": (
                "Venir avec ses criteres ecrits : sections, recouvrements, enrobages, "
                "cales, proprete du fond de coffrage, reservations. Un refus se motive "
                "par un ecart constate, pas par une impression. Et un visa donne sans "
                "etre alle voir engage celui qui l'a signe."),
        },
        "le_piege": (
            "Le point d'arret du ferraillage tombe juste avant le betonnage, c'est-a-dire "
            "au moment ou la toupie est commandee et ou l'equipe est la. C'est "
            "structurellement le moment ou il coute le plus cher de dire non — donc "
            "celui ou il faut l'avoir prepare. Un ferraillage se pre-visite la veille."),
    }


def controles_avant_coulage(d: dict) -> dict:
    """La check-list du dernier quart d'heure, celle qui se fait coffrage ferme."""
    return {
        "liste": [
            {"controle": "Enrobage", "comment": "cales en place, du bon type et en nombre",
             "symptome_si_rate": "aciers apparents ou corrosion a cinq ans, et le defaut "
                                 "ne se voit qu'une fois le coffrage depose"},
            {"controle": "Recouvrements", "comment": "longueur et position des barres de "
                                                     "reprise, nomenclature en main",
             "symptome_si_rate": "une reprise de betonnage sans continuite d'armature"},
            {"controle": "Proprete du fond", "comment": "fils de ligature, chutes, eau "
                                                        "stagnante evacues",
             "symptome_si_rate": "nid de cailloux et point faible en pied"},
            {"controle": "Reservations et inserts", "comment": "plan de reservation du "
                                                               "lot technique en main",
             "symptome_si_rate": "percement apres coup dans un ouvrage ferraille"},
            {"controle": "Etaiement et contreventement", "comment": "serrage, verticalite, "
                                                                    "stabilite au vent",
             "symptome_si_rate": "deformation du coffrage pendant le coulage, au mieux"},
            {"controle": "Bon de livraison", "comment": "classe, consistance, heure de "
                                                        "fabrication, temperature",
             "symptome_si_rate": "un beton qui n'est pas celui qu'on a commande, et "
                                 "personne pour le dire apres coup"},
        ],
        "regle": (
            "Ces six controles se font coffrage FERME et avant que la premiere toupie "
            "arrive. Apres, le cout de dire non est multiplie par le nombre de camions "
            "deja commandes — et c'est exactement pour cela qu'on ne les fait plus."),
    }


# ------------------------------------------------------------------ figures
def figures(opt: dict, deb: dict, immo: dict, reseau: list, debuts: dict,
            cycle_j: float) -> dict:
    ok = [x for x in opt["lignes"] if x.get("total_MAD") is not None]
    return {
        "parc": [{"libelle": f"{x['parc_m2']} m² · {x['zones_simultanees']} zone(s)",
                  "valeur": round(x["total_MAD"] / 1e3, 1)} for x in ok],
        "cadences": [{"libelle": f"{x['parc_m2']} m²",
                      "valeur": x["cadence_tenue_j"]} for x in ok],
        "debits": [{"libelle": f"{cle.replace('a_', '').replace('_degres', ' °C')} — "
                                f"{v['temps_de_maniabilite_h']} h de maniabilité",
                    "valeur": v["debit_minimal_m3_h"]}
                   for cle, v in deb["par_temperature"].items()],
        "toupies": [{"libelle": f"{o['toupies']} toupies · {o['debit_tenu_m3_h']} m³/h",
                     "valeur": o["duree_du_coulage_h"]}
                    for o in deb["options_de_rotation"]],
        "toupies_cible": [0.0, deb["duree_cible_du_coulage_h"]],
        "cycle": [{"nom": t.nom, "debut": round(debuts[t.id], 2),
                   "duree": round(t.duree, 2),
                   "critique": t.id in ("COF", "FEP", "FED", "PTA", "BET", "CUR", "DEC")}
                  for t in reseau],
    }


def tout_calculer(d: dict) -> dict:
    q = plc.quantites_zone(d)
    t = cy.durees_taches(d, q)
    reseau = cy.reseau_zone(t, d["cycle_zone"])
    cc = pln.contre_calcul(reseau)
    debuts = {i: v[0] for i, v in cc["detail"]["tot"].items()}
    cycle_j = cc["detail"]["duree"]
    regle = cy.cadence_rotation(t, d["cycle_zone"], d["materiel"]["nb_grues"])
    # La grandeur qui compte est la surface de COFFRAGE d'une zone, pas sa surface de
    # plancher : un parc est un stock de tables, et une zone en demande 1,18 m2 par m2
    # coule (sous-face, joues et fonds de poutres, rives). Diviser le parc par la
    # surface de plancher surestimait le nombre de zones qu'il porte.
    regle["surface_zone_m2"] = q["coffrage_m2"]
    regle["surface_plancher_zone_m2"] = q["surface_m2"]
    # La cadence et la duree du plancher sont LUES dans la sortie du module TV, pas
    # recalculees : le TV arrondit la cadence retenue avant d'en faire un planning
    # (3,42 j deviennent 3,4), et recalculer sans cet arrondi faisait diverger C3 de
    # D2 d'un dixieme de jour. Un module aval lit, il ne refait pas.
    tvj = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json").read_text(encoding="utf-8"))
    regle["cadence_calculee_j"] = regle["cadence_j"]
    regle["cadence_j"] = tvj["planning_plancher"]["cadence_zone_j"]
    regle["_arrondi"] = (
        f"cadence calculee {regle['cadence_calculee_j']} j, arrondie a "
        f"{regle['cadence_j']} j par le module TV pour construire son planning ; C3 "
        "reprend la valeur arrondie, qui est celle que D2 a utilisee. Recalculer sans "
        "l'arrondi faisait diverger les trois modules d'un dixieme de jour.")

    immo = duree_coffree(d, reseau, debuts)

    # le plancher porte-t-il la date du chantier ? on le LIT dans la sortie de D2,
    # on ne le suppose pas : c'est la question qui renverse la conclusion du parc.
    pl = json.loads((RACINE / "calc" / "sorties" / "planification.json").read_text(encoding="utf-8"))
    pr = json.loads((RACINE / "calc" / "sorties" / "prix.json").read_text(encoding="utf-8"))
    marge = pl["durees"]["MEZZ"]["marge_totale_j"]
    critique = pl["durees"]["MEZZ"]["critique"]
    fd = pr["bordereau"]["frais_de_duree"]

    nb_zones = d["geometrie"]["mezzanine"]["zones_de_coulage"]["nb_zones"]
    opt = optimum_du_parc(d, q, regle, immo, nb_zones, cycle_j,
                          fd["cout_MAD_par_mois"],
                          fd["conversion"]["jours_ouvres_par_mois_calendaire"], critique,
                          pl["durees"]["MEZZ"]["marge_libre_j"])
    opt["marge_totale_du_plancher_j"] = marge
    deb = debit_minimal(d, q)
    return {
        "cycle": {"duree_j": round(cycle_j, 2), "cadence_j": regle["cadence_j"],
                  "ressource_qui_borne": regle["ressource_qui_borne"],
                  "nb_zones": nb_zones,
                  "duree_du_plancher_j": round((nb_zones - 1) * regle["cadence_j"] + cycle_j, 2)},
        "immobilisation_du_coffrage": immo,
        "parc": opt,
        "betonnage": deb,
        "fenetre_de_coulage": fenetre_de_coulage(d, deb),
        "points_d_arret": points_d_arret(d, reseau),
        "controles_avant_coulage": controles_avant_coulage(d),
        "figures": figures(opt, deb, immo, reseau, debuts, cycle_j),
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    r = tout_calculer(d)
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "gros-oeuvre.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    o, b = r["parc"], r["betonnage"]
    print(f"cycle {r['cycle']['duree_j']} j · cadence {r['cycle']['cadence_j']} j "
          f"({r['cycle']['ressource_qui_borne']}) | immobilisation "
          f"{r['immobilisation_du_coffrage']['duree_j']} j dont "
          f"{r['immobilisation_du_coffrage']['part_de_cure_pct']} % de cure | "
          f"parc optimal {o['optimum']['parc_m2']} m2 (declare {o['parc_declare_m2']}) | "
          f"debit a 35 °C {b['debit_dimensionnant_m3_h']} m3/h, "
          f"{b['toupies_retenues']} toupies en {b['duree_du_coulage_h']} h")
