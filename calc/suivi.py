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
    bac = bord["debourse_sec_MAD"]
    va = sum(par_id[i]["debourse_sec_total_MAD"] * etats["constate"][i] / 100
             for i in etats["constate"])
    va += bord["frais_de_duree"]["total_MAD"] * min(1.0, j / duree_totale)
    vp = depense["cumul"](min(j, duree_totale))
    cr = sv["cout_reel_MAD"]["valeur"]
    cpi, spi = va / cr, va / vp
    return {
        "budget_a_l_achevement_BAC_MAD": round(bac, 2),
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
    }


def spi_du_chemin_critique(etats: dict, planifie: dict, chemin: list,
                           durees: dict) -> dict:
    """Le SPI global ne voit pas le chemin critique — et c'est ce qui le rend dangereux.

    Un indice global pondere par les budgets : une derive sur un gros poste non critique
    l'ecrase, une derive sur une petite tache critique y disparait. On recalcule donc la
    meme comparaison en se limitant aux taches qui portent la date, en DUREE et non en
    dirhams, puisque c'est de delai qu'il s'agit.
    """
    def avance(tab, ids):
        num = sum(durees[i]["duree_j"] * tab[i] / 100 for i in ids)
        den = sum(durees[i]["duree_j"] for i in ids)
        return num / den * 100 if den else 0.0

    tous = list(etats["constate"])
    g_c, g_p = avance(etats["constate"], tous), avance(planifie, tous)
    c_c, c_p = avance(etats["constate"], chemin), avance(planifie, chemin)
    return {
        "taches_du_chemin": chemin,
        "avancement_global_constate_pct": round(g_c, 2),
        "avancement_global_planifie_pct": round(g_p, 2),
        "SPI_en_duree_global": round(g_c / g_p, 4) if g_p else None,
        "avancement_du_chemin_constate_pct": round(c_c, 2),
        "avancement_du_chemin_planifie_pct": round(c_p, 2),
        "SPI_en_duree_du_chemin": round(c_c / c_p, 4) if c_p else None,
        "ecart_pts": round(c_c / c_p * 100 - g_c / g_p * 100, 2) if g_p and c_p else None,
        "lecture": (
            "Deux indices, deux reponses. Le global dit si le chantier, dans son ensemble, "
            "produit ce qui etait prevu ; celui du chemin dit si la DATE tient. Sur un "
            "chantier sous fenetre de consignation, le second est le seul qui engage, "
            "parce qu'une tache en avance hors du chemin ne rattrape rien : elle attend "
            "la fenetre avec les autres."),
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
def visa_de_situation(d: dict, bord: dict, etats: dict, sit: dict) -> dict:
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
    net_vise = sit["net_cumule_a_payer_MAD"] - retire
    return {
        "controles": controles,
        "lignes_reduites": lignes,
        "montant_retire_MAD": round(retire, 2),
        "net_declare_MAD": sit["net_cumule_a_payer_MAD"],
        "net_vise_MAD": round(net_vise, 2),
        "reduction_pct": round(retire / sit["net_cumule_a_payer_MAD"] * 100, 2),
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
def figures(etats: dict, av: dict, ve: dict, spi: dict, fia: dict, visa: dict,
            depense: dict, j: float) -> dict:
    # courbe en S de depense, avec le constat de valeur acquise pose comme un POINT
    pts = [{"j": p["j"], "prevu": p["pct"]} for p in depense["points"]]
    constat = [{"j": j, "realise": round(
        ve["valeur_acquise_VA_MAD"] / ve["budget_a_l_achevement_BAC_MAD"] * 100, 2)}]
    ordre = sorted(etats["constate"], key=lambda i: -abs(
        etats["declare"][i] - etats["constate"][i]))
    BANDE = (0.95, 1.05)
    ind = [
        {"libelle": "CPI (coût)", "valeur": ve["CPI"]},
        {"libelle": "SPI global (valeur)", "valeur": ve["SPI"]},
        {"libelle": "SPI global (durée)", "valeur": spi["SPI_en_duree_global"]},
        {"libelle": "SPI du chemin critique", "valeur": spi["SPI_en_duree_du_chemin"]},
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
    dep = px.courbe_de_depense(bord, res, t)
    j = float(d["suivi_chantier"]["date_arret_j"])

    planifie = avancement_planifie(seg, durees, j)
    etats = trois_etats(d, planifie)
    sit = px.situation(d, bord, etats["declare"])
    av = trois_avancements(d, bord, etats, j, duree, sit)
    ve = valeur_acquise(d, bord, etats, j, duree, dep)
    chemin = f["contre_calcul"]["chemin_critique"]
    spi = spi_du_chemin_critique(etats, planifie, chemin, t)
    fia = fiabilite_du_cpi(bord, dep, duree)
    visa = visa_de_situation(d, bord, etats, sit)
    mod = impact_modification(d, bord, ve, duree, cal)
    return {
        "date_arret": {"jour_ouvre": j, "mois": round(j / 21, 2),
                       "duree_totale_j": round(duree, 2)},
        "etats": etats, "avancements": av, "valeur_acquise": ve,
        "spi_du_chemin": spi, "fiabilite_du_cpi": fia, "visa": visa,
        "modification": mod,
        "figures": figures(etats, av, ve, spi, fia, visa, dep, j),
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
          f"CPI {v['CPI']} SPI {v['SPI']} | SPI chemin {r['spi_du_chemin']['SPI_en_duree_du_chemin']} | "
          f"visa -{r['visa']['montant_retire_MAD']:,.0f} MAD")
