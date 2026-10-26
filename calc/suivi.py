"""Suivi et controle d'un chantier (module D4).

D2 a donne les durees, D1 les prix. Celui-ci les confronte a ce que le chantier fait
reellement. Quatre choses que le referentiel generique de la valeur acquise ne donne
pas, et qui font ce module :

1. Il n'y a pas UN avancement mais TROIS — physique, financier, temporel — et ils ne
   coincident jamais. Publier l'un pour l'autre est l'erreur fondatrice du reporting.
2. Entre le planifie, le constate et le declare, il y a deux ecarts distincts : le
   premier est une derive de chantier, le second est un objet de visa. Les confondre
   fait viser une situation sur une declaration.
3. Un SPI global ne voit pas le chemin critique. Sur un chantier sous fenetre de
   consignation, il peut valoir 1,00 pendant que la seule tache qui porte la date
   derive — et l'inverse est vrai aussi.
4. Un CPI calcule trop tot ne veut rien dire. On peut dire a partir de quel
   avancement il devient un indicateur, et ce module le calcule au lieu de citer une
   regle d'usage.
"""
from __future__ import annotations
import json, math, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import planification as pln                                              # noqa: E402
import prix as px                                                        # noqa: E402


from etat import avancement_planifie, trois_etats                       # noqa: E402,F401


# ------------------------------------------------- les trois avancements
def trois_avancements(d: dict, bord: dict, etats: dict, j: float,
                      duree_totale: float, sit: dict) -> dict:
    """Physique, financier, temporel — au meme instant, et jamais egaux.

    - PHYSIQUE : la part du budget que les ouvrages executes representent. C'est le seul
      qui mesure de l'ouvrage.
    - FINANCIER : la part du marche deja facturee. Il porte la revision, les retenues et
      l'avance : il peut depasser le physique sans qu'un m3 de plus soit coule.
    - TEMPOREL : la part du delai ecoulee. Il ne mesure rien d'autre que le calendrier,
      et c'est celui qu'on cite le plus souvent par erreur.
    """
    par_id = {p["poste"]: p for p in bord["postes"]}
    bac = bord["prix_de_vente_MAD"]
    physique = sum(par_id[i]["prix_total_MAD"] * etats["constate"][i] / 100
                   for i in etats["constate"])
    # les frais indexes sur la duree avancent avec le TEMPS, par construction
    fd = bord["frais_de_duree"]
    physique += fd["total_MAD"] * bord["coefficient_de_vente"] * min(1.0, j / duree_totale)
    return {
        "date_arret_j": j,
        "physique_pct": round(physique / bac * 100, 2),
        "financier_pct": round(sit["net_cumule_a_payer_MAD"] / bac * 100, 2),
        "temporel_pct": round(j / duree_totale * 100, 2),
        "montant_physique_MAD": round(physique, 2),
        "ecart_physique_temporel_pts": round(physique / bac * 100 - j / duree_totale * 100, 2),
        "ecart_physique_financier_pts": round(
            physique / bac * 100 - sit["net_cumule_a_payer_MAD"] / bac * 100, 2),
        "lecture": (
            "Le financier est en dessous du physique parce que la retenue de garantie et "
            "le remboursement d'avance s'y soustraient : l'entreprise a construit plus "
            "qu'elle n'a encaisse, et c'est normal. Le temporel, lui, ne mesure que le "
            "calendrier. Trois nombres, trois questions differentes — et c'est le "
            "physique qui repond a « ou en est le chantier ? »."),
    }


# ------------------------------------------------- valeur acquise, a l'echelle du chantier
def valeur_acquise(d: dict, bord: dict, etats: dict, j: float, duree_totale: float,
                   depense: dict) -> dict:
    """VA, VP, CR et les indices, sur le bordereau entier.

    La valeur acquise est **valorisee sur l'etat CONSTATE**, jamais sur le declare : la
    declaration est un acte commercial, le constat est une mesure. Et la valeur planifiee
    vient de la courbe de DEPENSE (en dirhams), pas de la courbe de travail (en
    jours-hommes) : les deux different ici de plus de vingt points en milieu de chantier.
    """
    par_id = {p["poste"]: p for p in bord["postes"]}
    sv = d["suivi_chantier"]
    fd = bord["frais_de_duree"]["total_MAD"]
    part_temps = min(1.0, j / duree_totale)
    # Les OUVRAGES et les FRAIS DE DUREE ne se mesurent pas de la meme facon, et les
    # melanger dans une seule valeur acquise rend l'indice inutilisable. Un ouvrage a un
    # avancement physique, constate ; des frais de chantier n'en ont pas — ils courent
    # avec le temps. Une premiere version les additionnait en repartissant les frais au
    # prorata du temps ecoule, dans le module dont l'encart central dit qu'une grandeur
    # d'etat ne se repartit pas. On les publie donc separement, et le CPI porte sur les
    # OUVRAGES, qui sont la seule chose dont l'avancement a ete constate.
    bac_ouvrages = bord["debourse_sec_MAD"] - fd
    va = sum(par_id[i]["debourse_sec_total_MAD"] * etats["constate"][i] / 100
             for i in etats["constate"])
    vp_tout = depense["cumul"](min(j, duree_totale))
    vp = vp_tout - fd * part_temps
    bac = bac_ouvrages
    cr_tout = sv["cout_reel_MAD"]["valeur"]
    cr = cr_tout - fd * part_temps
    cpi, spi = va / cr, va / vp
    return {
        "perimetre": "les OUVRAGES seuls — les frais indexes sur la duree sont publies a part",
        "frais_de_duree": {
            "total_a_l_achevement_MAD": round(fd, 2),
            "part_du_temps_ecoulee": round(part_temps, 4),
            "engages_a_la_date_MAD": round(fd * part_temps, 2),
            "pourquoi_a_part": (
                "Un ouvrage a un avancement physique, qui se constate ; des frais de "
                "chantier n'en ont pas, ils courent avec le temps. Les additionner dans "
                "une seule valeur acquise melange une mesure et une horloge, et le CPI "
                "qui en sort ne mesure plus rien de precis. Ici les frais representent "
                f"{fd / bord['debourse_sec_MAD'] * 100:.1f} % du budget : les inclure "
                "au prorata du temps remontait le CPI de 0,90 a 0,96."),
        },
        "budget_a_l_achevement_BAC_MAD": round(bac, 2),
        "budget_total_avec_frais_de_duree_MAD": round(bord["debourse_sec_MAD"], 2),
        "cout_reel_total_MAD": round(cr_tout, 2),
        "valeur_planifiee_VP_MAD": round(vp, 2),
        "valeur_acquise_VA_MAD": round(va, 2),
        "cout_reel_CR_MAD": round(cr, 2),
        "ecart_de_cout_CV_MAD": round(va - cr, 2),
        "ecart_de_delai_SV_MAD": round(va - vp, 2),
        "CPI": round(cpi, 4), "SPI": round(spi, 4),
        "EAC_si_la_derive_persiste_MAD": round(bac / cpi, 2),
        "EAC_si_la_derive_cesse_MAD": round(cr + (bac - va), 2),
        "EAC_cout_et_delai_MAD": round(cr + (bac - va) / (cpi * spi), 2),
        "quelle_EAC": (
            "La premiere suppose que la derive est SYSTEMATIQUE et continuera : c'est le "
            "cas d'un prix de ressource mal estime ou d'une cadence trop optimiste. La "
            "deuxieme suppose qu'elle etait ACCIDENTELLE et ne se reproduira pas : un "
            "aleas ponctuel, une reprise. La troisieme suppose qu'il faut en plus "
            "rattraper le retard, donc payer des moyens. Choisir entre les trois n'est "
            "pas un calcul : c'est un diagnostic, et il s'ecrit."),
        "valorise_sur": "l'etat CONSTATE, jamais le declare",
        "fourchette": _bornes_des_indices(d, va, vp, bac, fd, part_temps),
    }


def _bornes_des_indices(d: dict, va: float, vp: float, bac: float, fd: float,
                        part_temps: float) -> dict:
    """Les indices, le cout reel pousse aux deux bouts de sa fourchette (D-036).

    Le CPI est un rapport dont le denominateur est une grandeur V3 declaree avec sa
    fourchette. Publier un CPI sans ses bornes, c'est publier une decimale qu'on n'a
    pas. Et ici le resultat n'est pas decoratif : le diagnostic change de signe a
    l'interieur de la fourchette declaree.
    """
    lo, hi = d["suivi_chantier"]["cout_reel_MAD"]["fourchette"]
    out = {}
    for nom, cr_tout in (("cout_reel_bas", lo), ("cout_reel_haut", hi)):
        cr = cr_tout - fd * part_temps
        cpi = va / cr
        out[nom] = {"cout_reel_total_MAD": cr_tout, "CPI": round(cpi, 4),
                    "EAC_si_la_derive_persiste_MAD": round(bac / cpi, 2),
                    "diagnostic": "depassement" if cpi < 1 else "economie"}
    change = out["cout_reel_bas"]["diagnostic"] != out["cout_reel_haut"]["diagnostic"]
    return {
        **out,
        "le_diagnostic_change_de_signe": bool(change),
        "lecture": (
            "Le cout reel est une hypothese V3 declaree entre "
            f"{lo:,.0f} et {hi:,.0f} MAD. Sur cette seule fourchette, le CPI va de "
            f"{out['cout_reel_haut']['CPI']:.2f} a {out['cout_reel_bas']['CPI']:.2f} et "
            "le diagnostic " + ("CHANGE DE SIGNE" if change else "garde son signe") + ". "
            "Annoncer « le chantier derive » sur un CPI dont la fourchette contient 1 "
            "n'est pas une alerte, c'est une opinion. Ce qu'il faut faire en premier "
            "n'est donc pas de corriger le chantier, c'est de **resserrer le cout reel** "
            "— c'est-a-dire de fiabiliser l'imputation analytique."
        ).replace(",", "\u202f"),
    }


def ce_qui_porte_la_date(etats: dict, planifie: dict, chemin: list, critiques: list,
                        durees: dict, marges: dict) -> dict:
    """La date tient-elle ? — et pourquoi un indice ne sait pas y repondre a cette date.

    La premiere version publiait un « SPI du chemin critique » cense etre la
    contribution du module. Il ne mesurait pas ce qu'il annoncait : a la date d'arret,
    AUCUNE des taches a marge nulle n'a commence. Un indice sur elles vaut 0/0 ; celui
    qui etait publie portait en fait sur la plus longue chaine du reseau, dont les deux
    tiers des taches ont quarante jours de marge, et toute sa derive venait d'une seule
    tache non critique.

    Ce qui repond vraiment a la question, c'est la MARGE : une derive ne menace la date
    que lorsqu'elle depasse la marge de la tache qui la subit. On mesure donc, tache par
    tache, le retard en jours et ce qu'il reste de marge apres lui.
    """
    def avance(tab, ids):
        num = sum(durees[i]["duree_j"] * tab[i] / 100 for i in ids)
        den = sum(durees[i]["duree_j"] for i in ids)
        return (num / den * 100) if den else None

    demarrees = [i for i in chemin if planifie[i] > 1e-9]
    crit_demarrees = [i for i in critiques if planifie[i] > 1e-9]
    g_c, g_p = avance(etats["constate"], list(etats["constate"])), avance(planifie, list(planifie))

    derives = []
    for i in etats["constate"]:
        perdu = (planifie[i] - etats["constate"][i]) / 100 * durees[i]["duree_j"]
        if perdu <= 1e-6:
            continue
        mt = marges[i]["marge_totale_j"]
        ml = marges[i]["marge_libre_j"]
        derives.append({
            "tache": i, "nom": durees[i].get("nom", i),
            "retard_j": round(perdu, 2),
            "marge_totale_j": mt, "marge_libre_j": ml,
            "marge_totale_restante_j": round(mt - perdu, 2),
            "marge_libre_restante_j": round(ml - perdu, 2),
            "menace_la_date": bool(perdu > mt + 1e-9),
            "decale_un_successeur": bool(perdu > ml + 1e-9),
        })
    derives.sort(key=lambda x: x["marge_totale_restante_j"])
    return {
        "taches_a_marge_nulle": critiques,
        "taches_a_marge_nulle_demarrees": crit_demarrees,
        "un_indice_sur_elles_est_il_defini": bool(crit_demarrees),
        "SPI_en_duree_global": round(g_c / g_p, 4) if g_p else None,
        "SPI_sur_la_plus_longue_chaine_demarree": (
            round(avance(etats["constate"], demarrees) / avance(planifie, demarrees), 4)
            if demarrees and avance(planifie, demarrees) else None),
        "taches_de_la_chaine_demarrees": demarrees,
        "derives": derives,
        "derive_la_plus_menacante": derives[0] if derives else None,
        "une_derive_menace_t_elle_la_date": any(x["menace_la_date"] for x in derives),
        "derives_qui_decalent_un_successeur": [x["tache"] for x in derives
                                               if x["decale_un_successeur"]],
        "lecture": (
            "A cette date, aucune tache a marge nulle n'a commence : un indice de "
            "performance sur le chemin critique n'est pas defini, et celui qu'on "
            "publierait porterait sur une chaine dont l'essentiel a de la marge. Ce qui "
            "repond a « la date tient-elle ? » n'est donc pas un indice mais une "
            "MARGE : tant qu'aucune derive ne depasse la marge totale de sa tache, la "
            "date tient — et c'est verifiable tache par tache, pas en moyenne."),
        "ce_qu_il_faut_suivre": (
            "La colonne « marge totale restante ». Elle se lit comme un carburant : elle "
            "ne se reconstitue pas, et le jour ou l'une d'elles passe en dessous de zero, "
            "la tache devient critique et la date bouge. C'est un indicateur qui previent "
            "AVANT, la ou un SPI constate APRES."),
    }


def fiabilite_du_cpi(bord: dict, depense: dict, duree_totale: float,
                     derive_pct: float = 6.0, pas: int = 10) -> dict:
    """A partir de quel avancement un CPI veut-il dire quelque chose ?

    On ne cite pas une regle d'usage : on la fabrique. On simule un chantier qui derive
    d'un taux CONSTANT, on y ajoute le bruit d'un releve de cout imprecis, et on regarde
    a partir de quand le CPI calcule se distingue du bruit.

    Le resultat depend du bruit suppose, et il est declare : c'est une demonstration de
    mecanisme, pas une loi.
    """
    bac = bord["debourse_sec_MAD"]
    bruit = bord["frais_de_duree"]["cout_MAD_par_mois"]   # un mois de frais mal impute
    pts = []
    for j in range(pas, int(duree_totale) + 1, pas):
        va = depense["cumul"](j)
        if va <= 0:
            continue
        cr_vrai = va * (1 + derive_pct / 100)
        cpi_vrai = va / cr_vrai
        # deux releves de cout extremes, a un mois de frais pres
        cpi_haut, cpi_bas = va / max(1.0, cr_vrai - bruit), va / (cr_vrai + bruit)
        pts.append({"j": j, "avancement_pct": round(va / bac * 100, 1),
                    "CPI_vrai": round(cpi_vrai, 4),
                    "CPI_min": round(cpi_bas, 4), "CPI_max": round(cpi_haut, 4),
                    "incertitude_pts": round((cpi_haut - cpi_bas) * 100, 2)})
    # le CPI devient lisible quand son incertitude passe sous la derive qu'on cherche
    seuil = next((p for p in pts if p["incertitude_pts"] < derive_pct), None)
    return {
        "derive_simulee_pct": derive_pct,
        "bruit_suppose_MAD": bruit,
        "points": pts,
        "avancement_ou_le_CPI_devient_lisible_pct": seuil["avancement_pct"] if seuil else None,
        "jour_correspondant": seuil["j"] if seuil else None,
        "lecture": (
            "Avant ce seuil, l'incertitude sur le cout reel — ici un mois de frais de "
            "chantier mal impute — depasse la derive qu'on cherche a detecter. Un CPI "
            "annonce a 5 % d'avancement ne mesure pas le chantier, il mesure la "
            "comptabilite analytique. C'est pour cela qu'on ne declenche pas une alerte "
            "sur les deux premieres situations, et c'est aussi pour cela qu'on les "
            "regarde quand meme : ce qu'elles montrent, ce sont des erreurs d'imputation."),
        "ce_que_ce_calcul_ne_prouve_pas": (
            "Que le seuil vaut pour un autre chantier. Il depend du bruit suppose, qui "
            "est ici une hypothese V3. La demonstration porte sur le MECANISME — "
            "l'incertitude relative decroit quand l'assiette grandit — pas sur la valeur."),
    }


# ------------------------------------------------- le visa, cote maitrise d'oeuvre
def visa_de_situation(d: dict, bord: dict, etats: dict, sit: dict,
                      sit_constatee: dict) -> dict:
    """Ce que la maitrise d'oeuvre verifie sur une situation, et ce qu'elle en retire.

    Chaque ligne est un CONTROLE execute, pas une case a cocher : il rend un chiffre, et
    c'est ce chiffre qui justifie une reduction. Un visa qui dit « non » sans chiffre se
    negocie ; un visa qui dit « moins 340 000 MAD, voici les trois postes » se signe.
    """
    par_id = {p["poste"]: p for p in bord["postes"]}
    ct = d["prix_unitaires_MAD"]["contrat"]
    lignes, retire = [], 0.0
    for i in sorted(etats["declare"]):
        dec, con = etats["declare"][i], etats["constate"][i]
        if abs(dec - con) < 1e-9:
            continue
        ecart_mad = par_id[i]["prix_total_MAD"] * (dec - con) / 100
        retire += ecart_mad
        lignes.append({"poste": i, "libelle": par_id[i]["libelle"],
                       "declare_pct": dec, "constate_pct": con,
                       "ecart_pts": round(dec - con, 2),
                       "ecart_MAD": round(ecart_mad, 2),
                       "motif": "quantite declaree superieure au constat contradictoire"})
    controles = [
        {"controle": "l'attachement est signe avant la situation",
         "resultat": "procedure", "chiffre": None,
         "note": "ce controle n'est pas calculable : il se verifie sur la piece"},
        {"controle": "les quantites declarees correspondent au constat",
         "resultat": "ECART" if lignes else "OK",
         "chiffre": round(retire, 2),
         "note": f"{len(lignes)} poste(s) a reduire"},
        {"controle": "a + b + c = 1 dans la formule de revision",
         "resultat": "OK" if abs(sit["revision"]["somme_abc"] - 1) < 1e-9 else "ECART",
         "chiffre": sit["revision"]["somme_abc"], "note": "sinon la revision est fausse"},
        {"controle": "la retenue de garantie est appliquee au montant revise",
         "resultat": "OK" if abs(sit["retenue_de_garantie_MAD"]
                                 - sit["montant_revise_MAD"]
                                 * ct["retenue_de_garantie_pct"]["valeur"] / 100) < 1 else "ECART",
         "chiffre": sit["retenue_de_garantie_MAD"], "note": "et non au montant initial"},
        {"controle": "la retenue cumulee reste sous son plafond",
         "resultat": "OK" if sit["retenue_retenue_MAD"] <= sit["retenue_plafond_MAD"] else "ECART",
         "chiffre": sit["retenue_plafond_MAD"], "note": "plafond contractuel"},
        {"controle": "le remboursement d'avance a bien demarre",
         "resultat": "OK" if sit["fraction_de_remboursement"] > 0 else "PAS ENCORE",
         "chiffre": sit["avance_remboursee_cumul_MAD"],
         "note": "il demarre a "
                 f"{ct['avance_remboursement_entre_avancement_pct'][0]} % d'avancement"},
    ]
    # Le net vise N'EST PAS le net declare moins les travaux retires : un montant de
    # travaux BRUTS ne se soustrait pas d'un net dont on a deja retire la retenue de
    # garantie et le remboursement d'avance. On rejoue la situation sur l'etat CONSTATE
    # et on compare les deux nets. La premiere version faisait la faute symetrique de
    # celle que son propre controle n° 4 denonce — « la retenue porte sur le revise ».
    net_vise = sit_constatee["net_cumule_a_payer_MAD"]
    reduction = sit["net_cumule_a_payer_MAD"] - net_vise
    return {
        "controles": controles,
        "lignes_reduites": lignes,
        "travaux_retires_MAD": round(retire, 2),
        "net_declare_MAD": sit["net_cumule_a_payer_MAD"],
        "net_vise_MAD": round(net_vise, 2),
        "reduction_du_net_MAD": round(reduction, 2),
        "reduction_pct": round(reduction / sit["net_cumule_a_payer_MAD"] * 100, 2),
        "pourquoi_la_reduction_est_plus_faible_que_les_travaux_retires": (
            f"Les travaux retires valent {retire:,.0f} MAD, et le net ne baisse que de "
            f"{reduction:,.0f}. La difference n'est pas une erreur : retirer des travaux "
            "fait baisser le montant revise, donc la retenue de garantie qui s'y applique "
            "et le remboursement d'avance qui suit l'avancement. Une partie de la "
            "reduction se recupere ainsi. Soustraire les travaux bruts du net serait la "
            "faute symetrique de celle que le controle n° 4 denonce."
        ).replace(",", "\u202f"),
        "avertissement_CPS": sit["avertissement_CPS"],
        "double_lecture": {
            "entreprise": (
                "Prepare la situation depuis ses attachements signes, pas depuis son metre "
                "d'etude. Un poste declare au-dela du constat sera retire, et il coute deux "
                "fois : la reduction, et la confiance au mois suivant."),
            "maitrise_d_oeuvre": (
                "Verifie dans cet ordre : attachement signe, quantites contre constat, "
                "formule de revision, assiette de la retenue, plafond, remboursement "
                "d'avance. Chaque refus porte un chiffre et un motif. Un visa sans chiffre "
                "n'est pas un visa, c'est un avis."),
        },
    }


# ------------------------------------------------- une modification en cours de route
def impact_modification(d: dict, bord: dict, ve: dict, duree_totale: float,
                        cal: dict) -> dict:
    """Un ordre de service en cours de chantier : ce qu'il coute, au-dela de son montant.

    Trois effets, et seul le premier figure dans l'avenant :
      1. le montant des travaux supplementaires ;
      2. les frais indexes sur la duree, si le delai s'allonge ;
      3. la prevision a terminaison, qui bouge aussi parce que le BAC a change.
    Un avenant qui ne porte que (1) est un avenant perdant.
    """
    mo = d["suivi_chantier"]["modification"]
    montant = mo["montant_travaux_MAD"]["valeur"]
    jours = mo["delai_supplementaire_j"]["valeur"]
    fd = bord["frais_de_duree"]
    frais = fd["cout_MAD_par_jour_ouvre"] * jours
    retard_evite = px.cout_du_retard(d, bord, jours)
    bac2 = ve["budget_a_l_achevement_BAC_MAD"] + montant + frais
    return {
        "objet": mo["objet"],
        "montant_des_travaux_MAD": montant,
        "delai_supplementaire_j": jours,
        "frais_indexes_sur_la_duree_MAD": round(frais, 2),
        "cout_complet_MAD": round(montant + frais, 2),
        "part_cachee_pct": round(frais / (montant + frais) * 100, 1),
        "penalites_evitees_MAD": retard_evite["penalites_MAD"],
        "nouveau_BAC_MAD": round(bac2, 2),
        "nouvelle_EAC_MAD": round(bac2 / ve["CPI"], 2),
        "lecture": (
            f"Le montant des travaux est {montant:,.0f} MAD. Le cout complet est "
            f"{montant + frais:,.0f} MAD, parce que {jours} jours de delai font courir "
            f"{frais:,.0f} MAD de frais de chantier que l'avenant ne mentionne pas. "
            f"C'est {round(frais / (montant + frais) * 100, 1)} % du cout reel de la "
            "modification, et c'est la part qu'on oublie de demander."
        ).replace(",", " "),
        "si_le_delai_n_est_pas_accorde_MAD": retard_evite["total_MAD"],
        "regle": (
            "Un ordre de service se chiffre en TROIS lignes : travaux, delai, et effet sur "
            "la prevision a terminaison. Signer la premiere seule, c'est accepter les deux "
            "autres sans les avoir vues."),
    }


# ------------------------------------------------------------------ figures
def figures(d: dict, etats: dict, av: dict, ve: dict, spi: dict, fia: dict, visa: dict,
            depense: dict, j: float) -> dict:
    # courbe en S de depense, avec le constat de valeur acquise pose comme un POINT
    pts = [{"j": p["j"], "prevu": p["pct"]} for p in depense["points"]]
    constat = [{"j": j, "realise": round(
        ve["valeur_acquise_VA_MAD"] / ve["budget_a_l_achevement_BAC_MAD"] * 100, 2)}]
    ordre = sorted(etats["constate"], key=lambda i: -abs(
        etats["declare"][i] - etats["constate"][i]))
    # Un verdict ne se rend que sur une base ou l'indice est DEFINI et comparable
    # (D-037). Les trois indices ci-dessous portent sur trois assiettes differentes —
    # dirhams produits sur dirhams depenses, dirhams sur dirhams prevus, jours sur
    # jours — et la bande de conformite est declaree dans data/, pas en dur ici.
    BANDE = tuple(d["suivi_chantier"]["bande_de_conformite_des_indices"]["valeur"])
    ind = [
        {"libelle": "CPI — dirhams produits / dépensés", "valeur": ve["CPI"]},
        {"libelle": "SPI — dirhams produits / prévus", "valeur": ve["SPI"]},
        {"libelle": "SPI en durée — jours produits / prévus", "valeur": spi["SPI_en_duree_global"]},
    ]
    return {
        "courbe": {"points": pts, "constat": constat},
        "avancements": [
            {"libelle": "Physique (ouvrages exécutés)", "valeur": av["physique_pct"]},
            {"libelle": "Financier (net facturé)", "valeur": av["financier_pct"]},
            {"libelle": "Temporel (délai écoulé)", "valeur": av["temporel_pct"]},
        ],
        "ecarts": [{"libelle": f"{i} · planifié {etats['planifie'][i]:.0f} %",
                    "valeur": round(etats["constate"][i] - etats["planifie"][i], 1)}
                   for i in ordre if abs(etats["constate"][i] - etats["planifie"][i]) > 0.5],
        "indices": ind,
        "indices_bande": list(BANDE),
        "indices_hors_bande": [x["libelle"] for x in ind
                               if not BANDE[0] <= x["valeur"] <= BANDE[1]],
        "indices_origine": round(min(x["valeur"] for x in ind) - 0.02, 2),
        "marges": [{"libelle": f"{x['tache']} · {x['nom']}",
                    "valeur": x["marge_totale_restante_j"]} for x in spi["derives"]],
    }


def tout_calculer(d: dict, duree_mezz: float) -> dict:
    pl = d["planning"]
    q = pln.quantites_chantier(d, pl)
    t = pln.durees_chantier(d, pl, q, duree_mezz)
    f = pln.planning_avec_fenetres(d, t)
    res = pln.voie_A_parcours(f["taches"])
    seg = pln.segments_de_travail(t, res, f["detail_fenetres"], pl["contraintes_exploitation"])
    duree = res["duree"]
    durees = {i: {**t[i], "debut_j": res["tot"][i][0], "fin_j": res["tot"][i][1]} for i in pln.NOMS}

    cal = pln.calendrier(duree, pl["calendrier"])
    bord = px.bordereau(d, q, t, duree, cal)
    dep = px.courbe_de_depense(bord, res, t, seg)
    j = float(d["suivi_chantier"]["date_arret_j"])

    planifie = avancement_planifie(seg, durees, j)
    etats = trois_etats(d, planifie)
    sit = px.situation(d, bord, etats["declare"])
    av = trois_avancements(d, bord, etats, j, duree, sit)
    ve = valeur_acquise(d, bord, etats, j, duree, dep)
    # L'ecart entre l'avancement PHYSIQUE et l'avancement TEMPOREL n'est pas un verdict.
    # Une version precedente concluait « le chantier est en avance de 11,98 points sur sa
    # production » — en comparant une part de BUDGET a une part de DELAI, c'est-a-dire
    # deux pourcentages de denominateurs differents : exactement l'erreur que ce module
    # denonce. Le seul avance/retard qui se lise est physique CONSTATE contre physique
    # PLANIFIE a la MEME date, et il dit l'inverse.
    av["physique_planifie_pct"] = round(
        ve["valeur_planifiee_VP_MAD"] / ve["budget_a_l_achevement_BAC_MAD"] * 100, 2)
    av["physique_constate_sur_ouvrages_pct"] = round(
        ve["valeur_acquise_VA_MAD"] / ve["budget_a_l_achevement_BAC_MAD"] * 100, 2)
    av["avance_ou_retard_pts"] = round(
        av["physique_constate_sur_ouvrages_pct"] - av["physique_planifie_pct"], 2)
    av["ce_que_l_ecart_avec_le_temporel_ne_dit_pas"] = (
        f"Le physique depasse le temporel de {av['ecart_physique_temporel_pts']} points, "
        "et cela ne veut PAS dire que le chantier est en avance : on compare une part de "
        "budget a une part de delai, deux pourcentages de denominateurs differents. La "
        "courbe planifiee n'est pas lineaire dans le temps — c'est tout l'objet d'une "
        "courbe en S. Le seul avance/retard qui se lise compare le physique CONSTATE au "
        "physique PLANIFIE a la MEME date : "
        f"{av['physique_constate_sur_ouvrages_pct']} % contre "
        f"{av['physique_planifie_pct']} %, soit "
        f"{abs(av['avance_ou_retard_pts'])} points de "
        + ("RETARD" if av["avance_ou_retard_pts"] < 0 else "AVANCE")
        + ". L'ecart avec le temporel dit seulement que les taches denses en budget sont "
        "en tete de planning, ce qui est la forme normale d'une courbe en S.")
    chemin = f["contre_calcul"]["chemin_critique"]
    mg = pln.marges(res, t, pln.liens_resolus(d, t))
    durees_nom = {i: {**t[i], "nom": pln.NOMS[i]} for i in pln.NOMS}
    spi = ce_qui_porte_la_date(etats, planifie, chemin,
                               f["contre_calcul"]["taches_critiques_voie_A"],
                               durees_nom, mg)
    fia = fiabilite_du_cpi(bord, dep, duree)
    sit_constatee = px.situation(d, bord, etats["constate"])
    visa = visa_de_situation(d, bord, etats, sit, sit_constatee)
    mod = impact_modification(d, bord, ve, duree, cal)
    return {
        "date_arret": {"jour_ouvre": j, "mois": round(j / 21, 2),
                       "duree_totale_j": round(duree, 2)},
        "etats": etats, "avancements": av, "valeur_acquise": ve,
        "ce_qui_porte_la_date": spi, "fiabilite_du_cpi": fia, "visa": visa,
        "modification": mod,
        "figures": figures(d, etats, av, ve, spi, fia, visa, dep, j),
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json").read_text(encoding="utf-8"))
    r = tout_calculer(d, tv["planning_plancher"]["duree_totale_j"])
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "suivi.json").write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n",
                                       encoding="utf-8")
    v = r["valeur_acquise"]
    print(f"j{r['date_arret']['jour_ouvre']:.0f} · physique {r['avancements']['physique_pct']} % · "
          f"financier {r['avancements']['financier_pct']} % · temporel {r['avancements']['temporel_pct']} % | "
          f"CPI {v['CPI']} SPI {v['SPI']} | "
          f"derive la plus menacante : {r['ce_qui_porte_la_date']['derive_la_plus_menacante']['tache']} "
          f"({r['ce_qui_porte_la_date']['derive_la_plus_menacante']['marge_totale_restante_j']} j de marge restante) | "
          f"visa -{r['visa']['reduction_du_net_MAD']:,.0f} MAD")
