"""Batiments ferroviaires : construire a cote d'une voie exploitee (B7c).

Ce module ne refait pas D2. D2 modelise les consignations a l'echelle du JOUR : quand la
fenetre tombe, et ce qu'elle decale. B7c descend d'un cran et traite ce qui se passe A
L'INTERIEUR d'une plage — la meme discipline que C3 appliquait au cycle du module TV.

Cinq resultats, tous non normatifs :

1. Le RENDEMENT d'une plage (lu dans `plage.py`, qui le tient pour D2 aussi).
2. Le POINT DE NON-RETOUR : l'heure apres laquelle on ne lance plus, parce qu'on ne
   pourrait plus replier. Meme deduction que la fenetre de coulage de C3, mais ici le
   depassement n'abime pas un ouvrage, il arrete un train.
3. Le nombre de PLAGES, et ce qu'il devient sous chaque levier — chacun MESURE en
   rejouant le reseau de D2 (D-040), jamais deduit.
4. Le COUT D'UNE HEURE UTILE, avec le domaine sur lequel ce ratio se compare (D-037).
5. La MATRICE D'INTERFACES : combien, lesquelles sont des decisions, et le delai de
   chacune — parce qu'une interface ratee ne se rattrape pas, elle s'attend.
"""
from __future__ import annotations
import json, math, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import plage as pg                                                       # noqa: E402
import planification as pln                                              # noqa: E402


# ---------------------------------------------------- 1 et 2. la plage, de l'interieur
def decomposition_de_la_plage(d: dict) -> dict:
    r = pg.rendement(d)
    v = {k: d["ferroviaire"]["plage_travaux"][k]["valeur"]
         for k in d["ferroviaire"]["plage_travaux"]
         if isinstance(d["ferroviaire"]["plage_travaux"][k], dict)
         and "valeur" in d["ferroviaire"]["plage_travaux"][k]}
    libelles = {
        "prise_de_possession_h": ("Prise de possession, balisage", "l'entreprise"),
        "consignation_catenaire_h": ("Consignation caténaire, mise à la terre, VAT",
                                     "L'EXPLOITANT"),
        "amenee_des_moyens_h": ("Amenée des moyens sur zone", "l'entreprise"),
        "repli_des_moyens_h": ("Repli des moyens, dépose des mises à la terre",
                               "l'entreprise"),
        "deconsignation_h": ("Déconsignation, contrôle du gabarit", "L'EXPLOITANT"),
        "marge_de_restitution_h": ("Marge de restitution", "personne — elle ne se "
                                   "négocie pas"),
    }
    detail = ([{"poste": libelles[k][0], "h": v[k], "tenu_par": libelles[k][1],
                "quand": "avant"} for k in pg.POSTES_AVANT]
              + [{"poste": "TRAVAIL EFFECTIF", "h": r["travail_effectif_h"],
                  "tenu_par": "l'entreprise", "quand": "travail"}]
              + [{"poste": libelles[k][0], "h": v[k], "tenu_par": libelles[k][1],
                  "quand": "apres"} for k in pg.POSTES_APRES])
    exploitant = sum(v[k] for k in ("consignation_catenaire_h", "deconsignation_h"))
    return {
        **r,
        "detail": detail,
        "part_tenue_par_l_exploitant_h": round(exploitant, 2),
        "abattement_de_cadence_nuit_pct": v["abattement_de_cadence_nuit_pct"],
        "facteur_d_interception": round(pg.facteur_d_interception(d), 3),
        "lecture": (
            f"Sur une plage de {r['duree_nominale_h']:.0f} h, il reste "
            f"{r['travail_effectif_h']:.2f} h de travail, soit {r['rendement_pct']:.0f} %. "
            f"Les {r['part_fixe_h']:.2f} h restantes ne sont pas du temps perdu : ce sont "
            f"des operations obligatoires, dont {exploitant:.2f} h appartiennent a "
            "l'exploitant. Doubler l'effectif ne les raccourcit d'aucune minute."),
        "_les_deux_effets_se_multiplient": (
            f"Le temps utile tombe a {r['rendement_pct']:.0f} % ET la cadence de nuit "
            f"perd {v['abattement_de_cadence_nuit_pct']:.0f} %. Les deux se composent : "
            f"une journee de travail normale demande {pg.facteur_d_interception(d):.2f} "
            "plages, pas deux. C'est la ou l'intuition se trompe le plus souvent."),
        "seuil_de_plage_inutile_h": round(r["part_fixe_h"], 2),
        "_seuil": (
            f"En dessous de {r['part_fixe_h']:.2f} h, une plage ne produit RIEN : la part "
            "fixe la consomme entierement. Ce seuil est le premier argument d'une "
            "demande de plage, et il se calcule — il ne se plaide pas."),
    }


def point_de_non_retour(d: dict, dec: dict, duree_operation_h: float,
                        cadence_nuit_t_h: float) -> dict:
    """L'heure apres laquelle on ne lance plus — et les deux seuils qui en decoulent.

    Formellement c'est la deduction de la fenetre de coulage de C3 : on part de l'heure a
    laquelle il faut avoir FINI et on recule. La difference est ailleurs — ici le
    depassement n'abime pas un ouvrage, il arrete un train.

    Et un levage ne se fractionne pas. On n'interrompt pas la pose d'une ferme a mi-course
    pour rendre la voie : la piece est accrochee ou elle est posee. Le point de non-retour
    n'est donc pas une recommandation de prudence, c'est une contrainte de faisabilite —
    et elle se retourne en deux seuils de CONCEPTION, tous deux calculables :

      - la masse maximale d'une piece qui tient dans une plage donnee ;
      - la duree minimale de plage a demander pour une piece donnee.

    Ces deux nombres se decident en etudes, six mois avant le premier levage. Les
    decouvrir sur le chantier revient a decouvrir qu'on ne peut pas monter la charpente.
    """
    t_debut = dec["avant_travail_h"]
    t_limite = dec["duree_nominale_h"] - dec["apres_travail_h"] - duree_operation_h
    marge = t_limite - t_debut
    piece = d["ferroviaire"]["sous_interception"]["masse_d_une_piece_t"]["valeur"]
    piece_max = dec["travail_effectif_h"] * cadence_nuit_t_h
    plage_min = dec["part_fixe_h"] + duree_operation_h

    def hhmm(x):
        signe = "-" if x < 0 else "+"
        x = abs(x)
        return f"H{signe}{int(x):02d}:{int(round((x - int(x)) * 60)):02d}"

    return {
        "masse_d_une_piece_t": piece,
        "cadence_de_nuit_t_h": round(cadence_nuit_t_h, 3),
        "duree_de_l_operation_h": round(duree_operation_h, 2),
        "debut_possible_du_travail": hhmm(t_debut),
        "point_de_non_retour": hhmm(t_limite),
        "marge_de_decision_h": round(marge, 2),
        "l_operation_tient_dans_la_plage": bool(marge >= 0),
        "masse_maximale_d_une_piece_t": round(piece_max, 2),
        "plage_minimale_pour_cette_piece_h": round(plage_min, 2),
        "regle": (
            "On part de l'heure a laquelle la voie doit etre restituee et on recule du "
            "repli, de la deconsignation et de la marge. Ce qui reste est l'heure limite "
            "de LANCEMENT — pas l'heure de fin. Une operation lancee apres elle ne peut "
            "plus etre repliee a temps, et une voie restituee en retard arrete un train."),
        "lecture": (
            f"Une piece de {piece:.0f} t demande {duree_operation_h:.2f} h de levage a la "
            f"cadence de nuit. La plage de {dec['duree_nominale_h']:.0f} h n'en laisse que "
            f"{dec['travail_effectif_h']:.2f} h : l'operation NE TIENT PAS, et le point de "
            f"non-retour ({hhmm(t_limite)}) tombe avant meme que le travail puisse "
            f"commencer ({hhmm(t_debut)})."
            if marge < 0 else
            f"Une piece de {piece:.0f} t demande {duree_operation_h:.2f} h. Le travail "
            f"peut commencer a {hhmm(t_debut)}, le point de non-retour tombe a "
            f"{hhmm(t_limite)} : il reste {marge:.2f} h pour decider de lancer."),
        "_divisibilite": (
            "Le nombre de plages d'un levier suppose que le levage se divise librement — "
            "qu'on peut s'arreter a la fin de chaque plage. C'est une BORNE INFERIEURE. "
            "Des pieces indivisibles la rendent optimiste, et peuvent la rendre "
            "inatteignable : si une seule piece ne tient pas dans une plage, aucun nombre "
            "de plages ne suffit. Les deux resultats de ce module se lisent ensemble, et "
            "c'est le second qui commande."),
        "les_deux_seuils": (
            f"Dans une plage de {dec['duree_nominale_h']:.0f} h, la piece la plus lourde "
            f"qu'on puisse lever pese {piece_max:.2f} t. Et pour lever la piece de "
            f"{piece:.0f} t prevue, il faut une plage d'au moins {plage_min:.2f} h. Ces "
            "deux nombres ne se negocient pas entre eux : ils disent que la MASSE DES "
            "PIECES et la DUREE DES PLAGES sont une seule decision, prise en etudes. Un "
            "projet qui dimensionne sa charpente sans savoir quelles plages il obtiendra "
            "decouvre le probleme au montage, quand il ne reste plus qu'a redecouper des "
            "pieces deja fabriquees."),
        "_un_levage_ne_se_fractionne_pas": (
            "On peut interrompre un coulage — mal, avec une reprise — mais on "
            "n'interrompt pas la pose d'une ferme a mi-course pour rendre la voie. Le "
            "point de non-retour d'un levage est donc une contrainte dure, pas une marge "
            "de prudence qu'un chef de chantier motive pourrait rogner."),
        "_qui_decide": (
            "Pas le chef d'equipe, qui a passe la nuit a preparer l'operation et n'a "
            "aucune envie d'y renoncer a vingt minutes du but. La decision de lancement "
            "se delegue par ECRIT, avant la plage, a quelqu'un dont le travail n'est pas "
            "en jeu — le plus souvent le responsable de la securite ferroviaire."),
    }


# ---------------------------------------------------- 3. combien de plages, et les leviers
def _rejoue(d: dict, part_pct: float, plage_h: float, fenetre_j: int, cache: dict) -> dict:
    """Mesure l'effet d'un levier en REJOUANT le reseau de D2 (D-040).

    On ne deduit pas l'effet sur la date d'une regle de trois : la tache sous
    interception raccourcit quand on pre-assemble, mais le pre-assemblage au sol
    s'allonge d'autant, et c'est le reseau qui dit ce qui l'emporte.
    """
    import copy
    cle = (round(part_pct, 3), round(plage_h, 3), fenetre_j)
    if cle in cache:
        return cache[cle]
    dd = copy.deepcopy(d)
    ce = dd["planning"]["contraintes_exploitation"]
    ce["part_levage_sous_consignation_pct"]["valeur"] = part_pct
    ce["fenetre_jours"]["valeur"] = fenetre_j
    dd["ferroviaire"]["plage_travaux"]["duree_nominale_h"]["valeur"] = plage_h
    pl = dd["planning"]
    tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json")
                    .read_text(encoding="utf-8"))
    q = pln.quantites_chantier(dd, pl)
    t = pln.durees_chantier(dd, pl, q, tv["planning_plancher"]["duree_totale_j"])
    f = pln.planning_avec_fenetres(dd, t)
    res = pln.voie_A_parcours(f["taches"])
    det = f["detail_fenetres"]["CHLV"]
    out = {"duree_du_chantier_j": round(res["duree"], 2),
           "CHLV_travail_j": round(t["CHLV"]["duree_j"], 2),
           "CHAP_j": round(t["CHAP"]["duree_j"], 2),
           "etalement_CHLV_j": round(det["etalement_j"], 1),
           "fenetres_CHLV": det["nb_fenetres"],
           "immobilisation_improductive_j": round(det["immobilisation_improductive_j"], 1)}
    cache[cle] = out
    return out


def comparaison_de_plages(d: dict, durees_h: tuple = (4.0, 6.0, 8.0, 10.0)) -> dict:
    """Ce qu'une heure de FERMETURE produit, selon la duree de la plage.

    C'est l'argument de negociation du module, et il se calcule. Deux plages de 4 h ne
    valent pas une plage de 8 h : la part fixe est payee DEUX FOIS. Raisonner en « total
    d'heures de fermeture » est donc faux, et c'est le raisonnement que tient naturellement
    celui qui accorde les plages.
    """
    lignes = []
    for h in durees_h:
        try:
            r = pg.rendement(d, h)
            u, rend = r["travail_effectif_h"], r["rendement_pct"]
        except ValueError:
            u, rend = 0.0, 0.0
        lignes.append({"plage_h": h, "utile_h": round(u, 2), "rendement_pct": rend,
                       "utile_par_heure_de_fermeture": round(u / h, 3)})
    ref = max(lignes, key=lambda x: x["utile_par_heure_de_fermeture"])
    pire = min((x for x in lignes if x["utile_h"] > 0),
               key=lambda x: x["utile_par_heure_de_fermeture"])
    return {
        "lignes": lignes,
        "meilleure_plage_h": ref["plage_h"], "pire_plage_utile_h": pire["plage_h"],
        "rapport_meilleure_sur_pire": round(
            ref["utile_par_heure_de_fermeture"] / pire["utile_par_heure_de_fermeture"], 2),
        "deux_courtes_contre_une_longue": {
            "deux_de_4h_utile_h": round(2 * next(x["utile_h"] for x in lignes if x["plage_h"] == 4.0), 2),
            "une_de_8h_utile_h": next(x["utile_h"] for x in lignes if x["plage_h"] == 8.0),
            "rapport": round(next(x["utile_h"] for x in lignes if x["plage_h"] == 8.0)
                             / (2 * next(x["utile_h"] for x in lignes if x["plage_h"] == 4.0)), 2),
        },
        "lecture": (
            "La part fixe se paie A CHAQUE PLAGE. Deux plages courtes la paient deux "
            "fois : a duree de fermeture egale, elles produisent beaucoup moins qu'une "
            "plage longue. L'argument a porter en reunion n'est donc pas « c'est trop "
            "court », qui est une opinion, mais ce rapport, qui est une soustraction."),
    }


def _cadence_de_nuit(d: dict) -> float:
    """Cadence de levage de nuit — UNE definition, partagee par tout le module.

    Elle se derive de la duree de travail DE JOUR que D2 publie, jamais de la duree
    stretchee : celle-ci est un nombre de PLAGES, et la diviser redonnerait la cadence
    divisee par le facteur d'interception.
    """
    pl = json.loads((RACINE / "calc" / "sorties" / "planification.json")
                    .read_text(encoding="utf-8"))
    ce = d["planning"]["contraintes_exploitation"]
    t = pl["quantites"]["charpente_t"] * ce["part_levage_sous_consignation_pct"]["valeur"] / 100
    jour_t_h = (t / pl["durees"]["CHLV"]["duree_de_travail_de_jour_j"]
                / d["planning"]["calendrier"]["heures_par_jour"])
    abat = d["ferroviaire"]["plage_travaux"]["abattement_de_cadence_nuit_pct"]["valeur"] / 100
    return jour_t_h * (1 - abat)


def leviers(d: dict, dec: dict) -> dict:
    """Quand une operation ne tient pas dans ses plages, on ne rallonge pas le planning.

    49 nuits n'est pas une reponse : c'est un signal. Les leviers ne sont pas dans le
    planning — ils sont dans la METHODE de montage et dans la NEGOCIATION des plages,
    c'est-a-dire en phase d'etudes, six mois avant le premier levage. Chaque levier est
    mesure en rejouant le reseau, et ce que le calcul ne price pas est nomme a cote.
    """
    ce = d["planning"]["contraintes_exploitation"]
    part0 = ce["part_levage_sous_consignation_pct"]["valeur"]
    bornes = ce["part_levage_sous_consignation_pct"]["fourchette"]
    plage0 = d["ferroviaire"]["plage_travaux"]["duree_nominale_h"]["valeur"]
    fen0 = ce["fenetre_jours"]["valeur"]
    cache = {}
    cas = [
        ("Référence — la méthode et les plages d'aujourd'hui", part0, plage0, fen0,
         "aucune"),
        ("Négocier une plage de 8 h", part0, 8.0, fen0,
         "une demande de plage plus longue : c'est l'exploitant qui arbitre, et il "
         "arbitre contre la circulation"),
        ("Négocier une plage de 10 h", part0, 10.0, fen0,
         "idem, et une plage de 10 h suppose une interruption de service, pas seulement "
         "une fermeture de voie"),
        ("Pré-assembler au sol : part 35 → 20 %", 20.0, plage0, fen0,
         "emprise au sol, pièces plus lourdes, grue plus forte"),
        ("Pré-assembler au sol : part 35 → 15 %", 15.0, plage0, fen0,
         "idem, et la part sort de la fourchette déclarée de la méthode actuelle"),
        ("Pré-assemblage 15 % + plage de 8 h", 15.0, 8.0, fen0, "les deux à la fois"),
        ("idem + 5 nuits par fenêtre", 15.0, 8.0, 5, "les trois à la fois"),
    ]
    lignes = []
    for nom, part, ph, fj, cout in cas:
        r = pg.rendement(d, ph)
        fact = pg.facteur_d_interception(d, ph)
        m = _rejoue(d, part, ph, fj, cache)
        # Un levier qui reduit la part levee le fait en PRE-ASSEMBLANT : moins de
        # levages, mais des pieces plus lourdes. La masse maximale levable, elle, ne
        # depend que de la plage. Les publier cote a cote est le seul moyen de voir
        # qu'un levier peut rendre l'operation MOINS faisable.
        lignes.append({
            "masse_maximale_levable_t": round(r["travail_effectif_h"] * _cadence_de_nuit(d), 2),
            "levier": nom, "part_sous_interception_pct": part,
            "plage_h": ph, "nuits_par_fenetre": fj,
            "travail_effectif_h": r["travail_effectif_h"],
            "rendement_pct": r["rendement_pct"],
            "facteur_d_interception": round(fact, 2),
            "part_hors_fourchette_declaree": bool(not bornes[0] <= part <= bornes[1]),
            "ce_que_le_calcul_ne_price_pas": cout,
            **m,
        })
    ref = lignes[0]
    for x in lignes:
        x["ecart_de_date_j"] = round(x["duree_du_chantier_j"] - ref["duree_du_chantier_j"], 2)
    meilleur = min(lignes, key=lambda x: x["duree_du_chantier_j"])
    return {
        "lignes": lignes, "reference": ref, "meilleur_mesure": meilleur,
        "fourchette_declaree_de_la_part_pct": bornes,
        "lecture": (
            f"La methode d'aujourd'hui demande {ref['fenetres_CHLV']} fenetres et etale "
            f"le levage sur {ref['etalement_CHLV_j']:.0f} jours ouvres. Ce n'est pas un "
            "planning a rallonger : c'est une methode a changer. Les leviers sont tous "
            "en amont du chantier — negocier la plage, pre-assembler au sol — et aucun "
            "ne s'actionne depuis le planning."),
        "le_piege_du_pre_assemblage": (
            "Reduire la part levee sous interception se fait en PRE-ASSEMBLANT au sol : "
            "moins de levages, mais des pieces plus lourdes. Or la masse maximale levable "
            "dans une plage ne depend que de la plage, pas de la methode. Un levier qui "
            "divise le nombre de levages en doublant la masse des pieces peut donc rendre "
            "l'operation MOINS faisable : la colonne « masse maximale levable » est la "
            "pour le verifier, et seuls les leviers qui allongent la PLAGE la deplacent."),
        "_le_levier_le_plus_efficace_n_est_pas_gratuit": (
            "Reduire la part levee sous interception allonge le pre-assemblage au sol : "
            "D2 lie deja les deux taches (CHAP = total x (1 - part)), et le reseau "
            "mesure le solde. Ce que le reseau ne mesure PAS : l'emprise au sol "
            "necessaire, la capacite de la grue pour des pieces plus lourdes, et le "
            "risque propre a un levage de piece lourde. Un levier qui gagne trente jours "
            "au planning et demande une grue qu'on n'a pas n'est pas un levier."),
        "_hors_fourchette": (
            f"Passer la part sous {bornes[0]:.0f} % sort de la fourchette declaree "
            f"({bornes[0]:.0f} a {bornes[1]:.0f} %). Ce n'est donc pas « choisir une "
            "valeur basse de l'hypothese » : c'est adopter une AUTRE methode de montage, "
            "dont la part est un resultat. Le dire evite de presenter un changement de "
            "methode comme un reglage de parametre."),
    }


# ---------------------------------------------------- 4. le cout d'une heure utile
def cout_de_l_heure_utile(d: dict, dec: dict) -> dict:
    f = d["ferroviaire"]["plage_travaux"]
    maj = f["majoration_horaire_nuit_pct"]["valeur"] / 100.0
    abat = f["abattement_de_cadence_nuit_pct"]["valeur"] / 100.0
    taux = d["prix_unitaires_MAD"]["postes"]["main_oeuvre_h"]["valeur"]
    paye = dec["duree_nominale_h"] * taux * (1 + maj)
    utile = dec["travail_effectif_h"]
    cout_h_utile = paye / utile
    cout_h_jour = taux
    return {
        "taux_horaire_de_jour_MAD": taux,
        "majoration_de_nuit_pct": f["majoration_horaire_nuit_pct"]["valeur"],
        "heures_payees_par_plage": dec["duree_nominale_h"],
        "heures_utiles_par_plage": utile,
        "cout_d_une_plage_MAD_par_compagnon": round(paye, 2),
        "cout_de_l_heure_UTILE_MAD": round(cout_h_utile, 2),
        "rapport_au_taux_de_jour": round(cout_h_utile / cout_h_jour, 2),
        "rapport_a_l_heure_d_OUVRAGE_de_jour": round(
            cout_h_utile / cout_h_jour / (1 - abat), 2),
        "ratio_defini_sur_cette_base": (
            "cout d'une heure d'OUVRAGE realisee sous interception, rapporte au cout "
            "d'une heure d'ouvrage equivalente realisee de jour hors interception. Le "
            "rapport au taux horaire brut (sans l'abattement de cadence) compare deux "
            "heures qui ne produisent pas la meme chose : il sous-estime l'ecart."),
        "lecture": (
            f"Une heure d'ouvrage sous interception coute "
            f"{cout_h_utile / cout_h_jour / (1 - abat):.1f} fois une heure d'ouvrage de "
            f"jour. La majoration de nuit n'en explique qu'une petite part "
            f"({1 + maj:.2f}) : l'essentiel vient de ce qu'on paie la plage entiere pour "
            f"{utile:.2f} h utiles. C'est pourquoi une heure gagnee sur la part fixe vaut "
            "beaucoup plus qu'une heure gagnee sur le travail."),
        "_avertissement_contractuel": (
            "La majoration de nuit est une valeur CONTRACTUELLE, pas une hypothese "
            "technique : ⚠ a verifier dans le CPS et la convention applicable."),
    }


# ---------------------------------------------------- 5. les interfaces
def matrice_d_interfaces(d: dict) -> dict:
    """Combien d'interfaces un chantier de gare porte, et lesquelles sont des decisions.

    n intervenants -> n(n-1)/2 interfaces POSSIBLES. Toutes ne sont pas actives ; mais
    celles qui le sont ne se traitent pas de la meme facon selon qu'elles portent une
    DECISION ou une INFORMATION. L'erreur de suivi la plus courante n'est pas d'oublier
    une interface : c'est de traiter une interface de decision comme une information,
    donc par courriel, donc sans trace de qui a tranche.
    """
    it = d["ferroviaire"]["interfaces"]
    n = len(it["intervenants"])
    actives = it["interfaces_actives"]
    decisions = [x for x in actives if x["nature"] == "decision"]
    par_delai = sorted(actives, key=lambda x: -x["delai_de_demande_j"])
    maitres_d_ouvrage = [x for x in it["intervenants"]
                         if x["type"] == "decision" and x["id"] in ("MOA-G", "GI", "EXPL")]
    return {
        "nb_intervenants": n,
        "interfaces_possibles": n * (n - 1) // 2,
        "interfaces_actives": len(actives),
        "dont_decisions": len(decisions),
        "liste": par_delai,
        "delai_le_plus_long_j": par_delai[0]["delai_de_demande_j"],
        "interface_la_plus_longue": f"{par_delai[0]['de']} → {par_delai[0]['a']} · "
                                    f"{par_delai[0]['objet']}",
        "nb_maitres_d_ouvrage": len(maitres_d_ouvrage),
        "lecture": (
            f"{n} intervenants, donc {n * (n - 1) // 2} interfaces possibles, dont "
            f"{len(actives)} actives et {len(decisions)} qui portent une DECISION. Et "
            f"{len(maitres_d_ouvrage)} d'entre eux sont des maitres d'ouvrage distincts : "
            "le gestionnaire d'infrastructure ne recoit pas d'ordre du maitre d'ouvrage "
            "de la gare, il se coordonne avec lui. C'est la difference de fond avec un "
            "chantier de batiment ordinaire — il n'y a pas un seul donneur d'ordre."),
        "la_regle_du_delai": (
            f"Une interface se demande au moins {par_delai[0]['delai_de_demande_j']} jours "
            "a l'avance pour la plus longue. Ce delai n'est pas une politesse : une plage "
            "perdue ne se redemande pas pour la semaine suivante, elle se redemande pour "
            "le prochain cycle. C'est ce qui rend une interface ferroviaire differente "
            "d'une interface de batiment — on ne la rattrape pas, on l'attend."),
        "decision_contre_information": (
            "Une interface de DECISION produit un document signe, avec un auteur et une "
            "date : elle se tient en reunion et se conclut par un releve de decisions. "
            "Une interface d'INFORMATION produit une diffusion : elle se tient par ecrit "
            "et n'engage personne. Traiter la premiere comme la seconde est l'erreur qui "
            "fait perdre une plage, parce que personne n'avait formellement tranche."),
    }


# ---------------------------------------------------- assemblage
def tout_calculer(d: dict) -> dict:
    dec = decomposition_de_la_plage(d)
    pl = json.loads((RACINE / "calc" / "sorties" / "planification.json")
                    .read_text(encoding="utf-8"))
    # Duree d'une operation elementaire de levage : une piece de charpente, lue chez D2.
    cad_nuit = _cadence_de_nuit(d)
    piece_t = d["ferroviaire"]["sous_interception"]["masse_d_une_piece_t"]["valeur"]
    duree_op = piece_t / cad_nuit
    lev = leviers(d, dec)
    return {
        "plage": dec,
        "point_de_non_retour": point_de_non_retour(d, dec, duree_op, cad_nuit),
        "leviers": lev,
        "cout": cout_de_l_heure_utile(d, dec),
        "comparaison_de_plages": comparaison_de_plages(d),
        "interfaces": matrice_d_interfaces(d),
        "figures": {
            "plage": [{"libelle": x["poste"], "valeur": x["h"]} for x in dec["detail"]],
            "leviers": [{"libelle": x["levier"], "valeur": x["etalement_CHLV_j"]}
                        for x in lev["lignes"]],
            "leviers_dates": [{"libelle": x["levier"], "valeur": x["duree_du_chantier_j"]}
                              for x in lev["lignes"]],
        },
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    r = tout_calculer(d)
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "ferroviaire.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    p, l = r["plage"], r["leviers"]
    print(f"plage {p['duree_nominale_h']} h -> {p['travail_effectif_h']} h utiles "
          f"({p['rendement_pct']} %), facteur x{p['facteur_d_interception']}")
    print(f"point de non-retour : {r['point_de_non_retour']['point_de_non_retour']} "
          f"(operation {r['point_de_non_retour']['duree_de_l_operation_h']} h)")
    for x in l["lignes"]:
        print(f"  {x['levier'][:44]:<44} {x['fenetres_CHLV']:>3} fen. "
              f"{x['etalement_CHLV_j']:>6.0f} j  chantier {x['duree_du_chantier_j']:>7.1f} j "
              f"({x['ecart_de_date_j']:+.0f})")
    print(f"heure utile : x{r['cout']['rapport_a_l_heure_d_OUVRAGE_de_jour']} une heure de jour")
    i = r["interfaces"]
    print(f"interfaces : {i['nb_intervenants']} intervenants, {i['interfaces_possibles']} possibles, "
          f"{i['interfaces_actives']} actives dont {i['dont_decisions']} decisions")
