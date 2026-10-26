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


def impact_sur_le_chantier(d: dict, duree_mezz: float, duree_mezz_reference: float,
                           cache: dict) -> dict:
    """De combien la fin du CHANTIER bouge si le plancher dure plus longtemps.

    On ne raisonne pas sur un type de marge : on REJOUE le reseau de D2 avec la nouvelle
    duree du plancher et on lit la date de fin. C'est la seule facon d'etre sur, et la
    passe adversariale a montre pourquoi : la premiere version declenchait les frais de
    duree des que la rallonge depassait la marge LIBRE, alors que la question posee —
    « la fin du chantier bouge-t-elle ? » — appelle la marge TOTALE. Elle imputait
    154 611 MAD de frais de duree a un parc qui ne retardait rien, et faisait basculer
    l'optimum. Le module publiait pourtant, deux lignes plus bas, la marge totale et le
    fait que le plancher ne porte pas la date.

    Rejouer le reseau rend la question de la marge sans objet : on mesure l'effet au
    lieu de le deduire d'une definition.
    """
    cle = round(duree_mezz, 3)
    if cle in cache:
        return cache[cle]
    pl = d["planning"]
    q = pln.quantites_chantier(d, pl)
    t = pln.durees_chantier(d, pl, q, duree_mezz)
    f = pln.planning_avec_fenetres(d, t)
    res = pln.voie_A_parcours(f["taches"])
    if "_reference" not in cache:
        t0 = pln.durees_chantier(d, pl, q, duree_mezz_reference)
        f0 = pln.planning_avec_fenetres(d, t0)
        cache["_reference"] = pln.voie_A_parcours(f0["taches"])["duree"]
    ref = cache["_reference"]
    out = {"duree_du_chantier_j": round(res["duree"], 2),
           "retard_du_chantier_j": round(max(0.0, res["duree"] - ref), 2),
           "le_plancher_devient_critique": bool(
               abs(pln.marges(res, t, pln.liens_resolus(d, t))["MEZZ"]["marge_totale_j"]) < 1e-6)}
    cache[cle] = out
    return out


def optimum_du_parc(d: dict, q: dict, regle: dict, immobilisation: dict,
                    nb_zones: int, cycle_j: float, frais_par_jour_ouvre: float,
                    marge_libre_j: float, marge_totale_j: float) -> dict:
    """Le parc qui minimise la somme du loyer et de ce que l'allongement coute.

    Trois termes, et le troisieme se MESURE au lieu de se deduire :
      - le LOYER du parc, proportionnel a sa taille ET a la duree ;
      - le MONTAGE, proportionnel a sa taille seulement ;
      - les FRAIS DE DUREE du chantier, et uniquement si le reseau rejoue montre que la
        fin bouge vraiment.

    Trois regimes apparaissent, et ils ne se traitent pas de la meme facon. Tant que la
    rallonge tient dans la marge LIBRE, rien ne bouge. Entre la marge libre et la marge
    TOTALE, les successeurs se decalent mais la fin tient : c'est gratuit au sens des
    frais de duree, et ce n'est pas gratuit au sens du risque. Au-dela, la fin bouge.
    """
    g = d["gros_oeuvre"]["coffrage"]
    loyer = g["location_MAD_m2_mois"]["valeur"]
    montage = g["montage_demontage_MAD_m2"]["valeur"]
    surf = regle["surface_zone_m2"]
    duree_reference = (nb_zones - 1) * regle["cadence_j"] + cycle_j
    jm = regle["jours_ouvres_par_mois_calendaire"]
    cache = {}
    lignes = []
    for parc in g["parcs_a_comparer_m2"]:
        b = cadence_bornee_par_le_parc(parc, surf, immobilisation["duree_j"])
        if not b["faisable"]:
            lignes.append({**b, "retenue": False})
            continue
        cad = max(regle["cadence_j"], b["cadence_min_j"])
        duree = (nb_zones - 1) * cad + cycle_j
        rallonge = max(0.0, duree - duree_reference)
        imp = impact_sur_le_chantier(d, duree, duree_reference, cache)
        mois = duree / jm
        cout_parc = parc * loyer * mois + parc * montage
        cout_duree = frais_par_jour_ouvre * imp["retard_du_chantier_j"]
        if rallonge <= marge_libre_j + 1e-6:
            regime = "dans la marge libre — rien ne bouge"
        elif rallonge <= marge_totale_j + 1e-6:
            regime = "entre marge libre et marge totale — les successeurs se decalent, la fin tient"
        else:
            regime = "au-dela de la marge totale — la fin du chantier bouge"
        lignes.append({
            "parc_m2": parc, "zones_simultanees": b["zones_simultanees"],
            "cadence_du_parc_j": b["cadence_min_j"],
            "cadence_des_equipes_j": regle["cadence_j"],
            "cadence_tenue_j": round(cad, 2),
            "ce_qui_borne": ("le parc de coffrage" if b["cadence_min_j"] > regle["cadence_j"]
                             else "les equipes"),
            "duree_du_plancher_j": round(duree, 2),
            "rallonge_j": round(rallonge, 2),
            "regime": regime,
            "marge_libre_restante_j": round(max(0.0, marge_libre_j - rallonge), 2),
            "marge_totale_restante_j": round(max(0.0, marge_totale_j - rallonge), 2),
            "retard_du_chantier_j": imp["retard_du_chantier_j"],
            "le_plancher_devient_critique": imp["le_plancher_devient_critique"],
            "loyer_et_montage_MAD": round(cout_parc, 2),
            "frais_de_duree_MAD": round(cout_duree, 2),
            "total_MAD": round(cout_parc + cout_duree, 2),
        })
    retenues = [x for x in lignes if x.get("total_MAD") is not None]
    best = min(retenues, key=lambda x: x["total_MAD"])
    for x in lignes:
        x["optimum_de_cout"] = x is best
    actuel = d["materiel"]["tables_coffrantes_m2"]
    b_act = cadence_bornee_par_le_parc(actuel, surf, immobilisation["duree_j"])
    # Le parc qui ne consomme AUCUNE marge : celui a partir duquel les equipes bornent.
    sans_marge = min((x for x in retenues if x["rallonge_j"] < 1e-6),
                     key=lambda x: x["parc_m2"], default=None)
    return {
        "lignes": lignes, "optimum_de_cout": best,
        "plus_petit_parc_sans_rallonge": sans_marge,
        "duree_de_reference_j": round(duree_reference, 2),
        "marge_libre_j": marge_libre_j, "marge_totale_j": marge_totale_j,
        "parc_declare_m2": actuel,
        "cadence_du_parc_declare_j": b_act["cadence_min_j"],
        "le_parc_declare_borne_t_il": b_act["cadence_min_j"] > regle["cadence_j"],
        "ecart_entre_les_deux_choix_MAD": round(
            (sans_marge["total_MAD"] - best["total_MAD"]) if sans_marge else 0.0, 2),
        "lecture": (
            "L'optimum de COUT est le plus petit parc dont l'allongement ne retarde pas "
            "la fin du chantier — et sur ce chantier, c'est le plus petit parc tout "
            "court, parce que le plancher dispose d'une marge totale large. Le calcul "
            "est juste et la conclusion n'est pas une decision : voir ci-dessous."),
        "ce_que_le_cout_ne_decide_pas": (
            "Le modele ne price que le loyer et le retard de la fin. Il ne price pas : "
            "(1) la marge consommee, qui ne sera plus la pour l'alea — et l'optimum de "
            "cout en mange l'essentiel ; (2) le decalage des SUCCESSEURS, qui n'est "
            "gratuit qu'au sens des frais de duree et qui peut creer des conflits de "
            "ressource ailleurs ; (3) la capacite a rattraper, qui disparait avec la "
            "marge. Un optimum de cout qui recommande un seul jeu de tables dit en "
            "realite : « tout se passera bien ». C'est une hypothese, pas un calcul, et "
            "elle ne figure sur aucune ligne du tableau."),
        "comment_on_tranche": (
            "En nommant ce qu'on achete. Le plus petit parc coute le moins et laisse "
            "le plancher sans marge utile. Le premier parc qui ne consomme aucune marge "
            "coute davantage et rend le plancher insensible a l'alea. L'ecart entre les "
            "deux est le prix de cette assurance : il se discute, il ne se calcule pas."),
    }


# ------------------------------------------------------ betonnage par temps chaud
def debit_minimal(d: dict, q: dict, duree_betonnage_tv_h: float) -> dict:
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
    # Sens d'avancement : une bande traverse la zone dans la dimension choisie, et on
    # avance dans l'autre. Le choix n'est pas neutre — il change le debit minimal de
    # 60 % — il est donc DECLARE dans data/ et non pris par un min() silencieux.
    sens = b["sens_d_avancement"]["valeur"]
    L, l = cz["longueur_zone_m"], cz["largeur_zone_m"]
    traverse, avance = (l, L) if sens == "dans la longueur" else (L, l)
    n_bandes = math.ceil(avance / larg)
    # Le volume d'une bande est celui de la ZONE divise par le nombre de bandes : il
    # porte ainsi les poutres, qu'une bande traverse comme le reste. Une version
    # precedente multipliait largeur x traverse x epaisseur de DALLE, et laissait les
    # 8,4 m3 de poutres — la ou une reprise froide est le plus grave — hors du calcul.
    vol_bande = q["beton_m3"] / n_bandes
    ep_dalle = q["beton_dalle_m3"] / q["surface_m2"]
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
    # Troisieme contrainte, et c'est elle qui commande : le CYCLE du module TV pose deja
    # une duree de betonnage. Si C3 en retenait une autre, deux modules publieraient deux
    # durees pour le meme coulage — exactement ce que l'introduction de ce module
    # reproche. On lit donc la duree du TV et on cherche l'attelage qui la tient.
    duree_tv = duree_betonnage_tv_h
    debit_tv = q["beton_m3"] / duree_tv
    n_tv = math.ceil(debit_tv / debit_par_toupie)
    if all(o["toupies"] != n_tv for o in options) and n_tv <= 12:
        tenu = min(pompe, n_tv * debit_par_toupie)
        options.append({"toupies": n_tv, "debit_tenu_m3_h": round(tenu, 1),
                        "duree_du_coulage_h": round(q["beton_m3"] / tenu, 2),
                        "au_dessus_du_minimum": bool(tenu >= ref),
                        "borne_par": "la pompe" if n_tv * debit_par_toupie > pompe
                                     else "la rotation des toupies"})
        options.sort(key=lambda o: o["toupies"])
    choisie = next(o for o in options if o["toupies"] == n_tv)
    sous_cible = next((o for o in options if o["duree_du_coulage_h"] <= cible), options[-1])
    return {
        "surface_zone_m2": q["surface_m2"],
        "largeur_de_bande_m": larg, "longueur_de_bande_m": traverse,
        "sens_d_avancement": sens, "avance_sur_m": avance,
        "epaisseur_de_dalle_m": round(ep_dalle, 3),
        "volume_d_une_bande_m3": round(vol_bande, 2),
        "nb_de_bandes": n_bandes,
        "controle_les_bandes_font_la_zone": {
            "somme_des_bandes_m3": round(vol_bande * n_bandes, 2),
            "volume_de_la_zone_m3": q["beton_m3"],
            "ecart_m3": round(vol_bande * n_bandes - q["beton_m3"], 4)},
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
        "duree_du_betonnage_au_cycle_TV_h": round(duree_tv, 2),
        "debit_qu_implique_le_cycle_TV_m3_h": round(debit_tv, 1),
        "option_qui_tient_la_cible_horaire": sous_cible,
        "option_retenue": choisie,
        "toupies_retenues": choisie["toupies"],
        "duree_du_coulage_h": choisie["duree_du_coulage_h"],
        "trois_contraintes": (
            f"Le minimum anti-reprise demande {n_toupies} toupies. La cible horaire — "
            f"finir en moins de {cible:.0f} h — en demande "
            f"{sous_cible['toupies']}. Et le CYCLE du module TV, qui a servi a batir tout "
            f"le planning, suppose un betonnage en {duree_tv:.2f} h, soit "
            f"{debit_tv:.0f} m3/h : {n_tv} toupies. C'est la plus exigeante des trois qui "
            "commande, et c'est celle du cycle — parce qu'elle est deja dans le planning "
            "de D2 et dans le prix de D1. Retenir moins reviendrait a casser une chaine "
            "de calcul en aval pour economiser un camion."),
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
    """A quelle heure demarrer pour avoir FINI avant la chaleur.

    L'heure de demarrage se deduit, elle ne se pose pas : on part de l'heure a laquelle
    on veut avoir fini et on recule de la duree du coulage. Une version precedente
    posait « 05:30 » en constante tout en publiant la regle inverse.
    """
    b = d["gros_oeuvre"]["betonnage_temps_chaud"]
    fin_voulue = b["heure_de_fin_voulue_h"]["valeur"]
    duree = deb["duree_du_coulage_h"]
    debut = fin_voulue - duree
    lever = b["lever_du_soleil_ete_h"]["valeur"]

    def hhmm(x):
        h = int(x)
        return f"{h:02d} h {int(round((x - h) * 60)):02d}"

    return {
        "duree_du_coulage_h": duree,
        "heure_de_fin_voulue": hhmm(fin_voulue),
        "demarrage_deduit": hhmm(debut),
        "lever_du_soleil": hhmm(lever),
        "demarrage_avant_le_jour": bool(debut < lever),
        "eclairage_necessaire_h": round(max(0.0, lever - debut), 2),
        "regle": (
            "On part de l'heure a laquelle on veut avoir FINI et on recule de la duree "
            "du coulage. Ce qui decide de l'heure de demarrage, ce n'est pas l'horaire "
            "de l'equipe : c'est la temperature a laquelle on surfacera."),
        "consequence_securite": (
            f"Le demarrage deduit tombe {round(max(0.0, lever - debut) * 60)} minutes "
            "AVANT le lever du soleil : la premiere partie du coulage se fait de nuit. "
            "Cela se prepare — eclairage de l'aire de coulage et des circulations, "
            "balisage de la zone de manoeuvre de la pompe et des toupies, et un homme "
            "dedie au guidage des camions. Un coulage de nuit improvise pour fuir la "
            "chaleur echange un risque contre un autre."
            if debut < lever else
            "Le demarrage deduit tombe apres le lever du soleil : pas d'eclairage "
            "specifique a prevoir pour le coulage lui-meme."),
    }


# ------------------------------------------------------------ points d'arret
def points_d_arret(d: dict, reseau: list, cycle_j: float) -> dict:
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
        "part_du_cycle_pct": round(par_id["PTA"].duree / cycle_j * 100, 2),
        "_denominateur": ("la DUREE du cycle, pas la somme des durees de ses taches : "
                          "les taches se recouvrent, leur somme vaut 10,45 j pour un "
                          "cycle de 8,05 j, et rapporter a la somme minorait la part "
                          "d'un tiers"),
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
        "parc": [{"libelle": f"{x['parc_m2']} m² · {x['zones_simultanees']} zone(s)"
                             + (" · optimum de coût" if x["optimum_de_cout"] else "")
                             + (" · sans rallonge" if x is opt["plus_petit_parc_sans_rallonge"]
                                else ""),
                  "valeur": round(x["total_MAD"] / 1e3, 1)} for x in ok],
        "marges": [{"libelle": f"{x['parc_m2']} m² · {x['zones_simultanees']} zone(s)",
                    "valeur": x["marge_totale_restante_j"]} for x in ok],
        "marges_bande": [opt["marge_libre_j"], opt["marge_totale_j"]],
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
    # Les frais de duree sont LUS chez D1 — au jour ouvre, tels qu'il les publie — et
    # non re-derives ici : les re-deriver donnait 15 143 MAD/j contre 16 268, soit 7,4 %
    # d'ecart, dans le module qui ouvre sur « trois modules qui recalculent la meme
    # grandeur en publient trois valeurs ».
    regle["jours_ouvres_par_mois_calendaire"] = fd["conversion"]["jours_ouvres_par_mois_calendaire"]
    opt = optimum_du_parc(d, q, regle, immo, nb_zones, cycle_j,
                          fd["cout_MAD_par_jour_ouvre"],
                          pl["durees"]["MEZZ"]["marge_libre_j"],
                          pl["durees"]["MEZZ"]["marge_totale_j"])
    opt["frais_de_duree_MAD_par_jour_ouvre"] = fd["cout_MAD_par_jour_ouvre"]
    opt["_source_des_frais"] = "calc/sorties/prix.json — bordereau.frais_de_duree"
    # Les deux nombres de l'exercice 1 : le quotient exact avant arrondi, et le
    # battement entre le parc qu'on calcule et celui que le projet a commande. Les
    # ecrire a la main faisait publier « 3 x 424,3 = 1 300 », une egalite fausse de 2 %
    # (le produit vaut 1 273 ; 1 300 est le stock declare).
    immo["zones_simultanees_exact"] = round(immo["duree_j"] / regle["cadence_j"], 2)
    immo["zones_simultanees"] = math.ceil(immo["duree_j"] / regle["cadence_j"] - 1e-9)
    immo["parc_minimum_m2"] = round(immo["zones_simultanees"] * q["coffrage_m2"], 1)
    immo["battement_du_parc_declare_m2"] = round(
        opt["parc_declare_m2"] - immo["parc_minimum_m2"], 1)
    deb = debit_minimal(d, q, t["betonnage_h"] if "betonnage_h" in t
                        else t["betonnage_j"] * 8)
    return {
        "cycle": {"duree_j": round(cycle_j, 2), "cadence_j": regle["cadence_j"],
                  "ressource_qui_borne": regle["ressource_qui_borne"],
                  "nb_zones": nb_zones,
                  "duree_du_plancher_j": round((nb_zones - 1) * regle["cadence_j"] + cycle_j, 2)},
        "immobilisation_du_coffrage": immo,
        "parc": opt,
        "betonnage": deb,
        "fenetre_de_coulage": fenetre_de_coulage(d, deb),
        "points_d_arret": points_d_arret(d, reseau, cycle_j),
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
          f"parc : optimum de cout {o['optimum_de_cout']['parc_m2']} m2, "
          f"sans rallonge {o['plus_petit_parc_sans_rallonge']['parc_m2']} m2 "
          f"(declare {o['parc_declare_m2']}) | "
          f"debit a 35 °C {b['debit_dimensionnant_m3_h']} m3/h, "
          f"{b['toupies_retenues']} toupies en {b['duree_du_coulage_h']} h")
