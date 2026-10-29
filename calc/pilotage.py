"""Pilotage et suivi de plusieurs sites (D7).

Un chef de projet suivi ne lit pas un chantier : il lit un TABLEAU DE BORD, c'est-à-dire
des nombres que quelqu'un d'autre a agrégés. Ce module calcule quatre choses, toutes
non normatives, et toutes sur la même question : qu'est-ce qu'une agrégation perd ?

1. **Un ratio ne se consolide pas.** Le CPI d'une opération n'est pas la moyenne des CPI
   de ses sites : c'est le rapport des sommes. L'écart entre les deux se chiffre, et il
   va dans le sens qui rassure.
2. **L'agrégation AMORTIT.** Une dérive de site se retrouve dans l'indicateur consolidé
   divisée par le poids de ce site. Un site à 13 % du coût doit dériver huit fois plus
   que le seuil d'alerte pour le franchir. Le calcul donne le seuil exact, en MAD.
3. **Le masquage est RÉCURSIF.** Ce que le consolidé fait au site, le site le fait à ses
   lots. Le nombre d'étages d'agrégation est le vrai sujet d'un reporting multi-sites.
4. **La latence du reporting se paie.** Entre le moment où une dérive commence et celui
   où un indicateur la montre, il y a la période de reporting et le délai de remontée.
   Ces jours-là se paient au tarif des frais de durée.

Et le cinquième résultat, qui est le plus utile sur un chantier ferroviaire : **le bon
seuil d'alerte d'un site n'est pas un pourcentage, c'est la période entre deux fenêtres
de consignation.** Un retard plus court se rattrape ; un retard plus long coûte un cycle
entier, et aucun indicateur de coût ne le voit venir.

Ce que le module ne dit pas : ce qu'un contrat impose de déclarer, à qui et dans quel
délai ; les obligations de reporting d'un marché public ; les seuils contractuels de
réclamation. Tous sont contractuels et restent ⏸.
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
    coupe = texte[:n].rsplit(" ", 1)[0]
    return coupe + "…"


def _b(o: dict) -> tuple[float, float]:
    f = o.get("fourchette")
    return (float(f[0]), float(f[1])) if f else (float(o["valeur"]), float(o["valeur"]))


# ------------------------------------------------- 1. la situation d'un site
def situation_par_lots(nom: str, lots: list, budget_total: float) -> dict:
    """VP, VA, CR et les deux indices, DÉRIVÉS des lots — jamais déclarés.

    La valeur acquise d'un lot est son budget multiplié par son avancement PHYSIQUE.
    C'est la seule définition qui tienne : un avancement de dépense donnerait un CPI
    égal à 1 par construction, ce qui est la façon la plus répandue de ne rien mesurer.
    """
    lignes = []
    for x in lots:
        vp = x["budget_MAD"] * x["avancement_planifie_pct"] / 100
        va = x["budget_MAD"] * x["avancement_constate_pct"] / 100
        cr = x["cout_reel_MAD"]
        lignes.append({
            "lot": x["lot"],
            "budget_MAD": x["budget_MAD"],
            "part_du_budget_pct": round(x["budget_MAD"] / budget_total * 100, 1),
            "avancement_planifie_pct": x["avancement_planifie_pct"],
            "avancement_constate_pct": x["avancement_constate_pct"],
            "valeur_planifiee_MAD": round(vp, 2),
            "valeur_acquise_MAD": round(va, 2),
            "cout_reel_MAD": cr,
            "CPI": round(va / cr, 4) if cr else None,
            "SPI": round(va / vp, 4) if vp else None,
            "derive_MAD": round(cr - va, 2),
            "demarre": cr > 0 or va > 0,
        })
    vp = sum(x["valeur_planifiee_MAD"] for x in lignes)
    va = sum(x["valeur_acquise_MAD"] for x in lignes)
    cr = sum(x["cout_reel_MAD"] for x in lignes)
    return {
        "site": nom,
        "lots": lignes,
        "budget_a_l_achevement_BAC_MAD": round(budget_total, 2),
        "valeur_planifiee_VP_MAD": round(vp, 2),
        "valeur_acquise_VA_MAD": round(va, 2),
        "cout_reel_CR_MAD": round(cr, 2),
        "CPI": round(va / cr, 4) if cr else None,
        "SPI": round(va / vp, 4) if vp else None,
        "derive_MAD": round(cr - va, 2),
        "avancement_physique_pct": round(va / budget_total * 100, 1),
        "EAC_si_la_derive_persiste_MAD": round(budget_total / (va / cr), 2) if va else None,
    }


def sites(d: dict, su: dict) -> list:
    """Les deux sites, chacun dans son périmètre — les OUVRAGES seuls.

    Le site principal n'est pas recalculé : ses quatre grandeurs viennent du module D4,
    qui les publie déjà (D-039). Le site secondaire se dérive de ses lots.
    """
    ms = d["multi_sites"]
    va_d4 = su["valeur_acquise"]
    principal = {
        "site": ms["sites"][0]["nom"],
        "id": ms["sites"][0]["id"],
        "role": ms["sites"][0]["role"],
        "lots": None,
        "budget_a_l_achevement_BAC_MAD": va_d4["budget_a_l_achevement_BAC_MAD"],
        "valeur_planifiee_VP_MAD": va_d4["valeur_planifiee_VP_MAD"],
        "valeur_acquise_VA_MAD": va_d4["valeur_acquise_VA_MAD"],
        "cout_reel_CR_MAD": va_d4["cout_reel_CR_MAD"],
        "CPI": va_d4["CPI"],
        "SPI": va_d4["SPI"],
        "derive_MAD": round(va_d4["cout_reel_CR_MAD"] - va_d4["valeur_acquise_VA_MAD"], 2),
        "avancement_physique_pct": round(
            va_d4["valeur_acquise_VA_MAD"] / va_d4["budget_a_l_achevement_BAC_MAD"] * 100, 1),
        "EAC_si_la_derive_persiste_MAD": va_d4["EAC_si_la_derive_persiste_MAD"],
        "_source": "calc/sorties/suivi.json — valeur_acquise (module D4). Rien n'est "
                   "recopié : le périmètre est celui de D4, les OUVRAGES seuls.",
    }
    s2 = ms["sites"][1]
    secondaire = situation_par_lots(s2["nom"], s2["lots"],
                                    s2["budget_ouvrages_MAD"]["valeur"])
    secondaire["id"] = s2["id"]
    secondaire["role"] = s2["role"]
    secondaire["_source"] = ("data/projet-gare.json — multi_sites.sites[1].lots : une "
                             "situation de site déclarée lot par lot, V3")
    return [principal, secondaire]


# ------------------------------------------------- 2. la consolidation, et ce qu'elle perd
def consolidation(sites_: list, seuils: dict) -> dict:
    """Le CPI d'une opération est le rapport des SOMMES, jamais la moyenne des rapports.

    Et l'écart entre les deux n'est pas une subtilité d'arrondi : il vaut d'autant plus
    que les sites sont de tailles différentes, et il va TOUJOURS dans le sens du plus
    gros site — c'est-à-dire, en général, dans le sens qui rassure.
    """
    va = sum(s["valeur_acquise_VA_MAD"] for s in sites_)
    cr = sum(s["cout_reel_CR_MAD"] for s in sites_)
    vp = sum(s["valeur_planifiee_VP_MAD"] for s in sites_)
    bac = sum(s["budget_a_l_achevement_BAC_MAD"] for s in sites_)
    cpi = va / cr
    spi = va / vp
    moyenne_cpi = sum(s["CPI"] for s in sites_) / len(sites_)
    vig, alerte_ = seuils["vigilance_CPI"], seuils["alerte_CPI"]
    poids = [{"site": s["site"], "id": s["id"],
              "poids_du_cout_pct": round(s["cout_reel_CR_MAD"] / cr * 100, 1),
              "poids_du_budget_pct": round(s["budget_a_l_achevement_BAC_MAD"] / bac * 100, 1),
              "CPI": s["CPI"],
              "derive_MAD": s["derive_MAD"],
              # L'AMORTISSEMENT : de combien l'indicateur consolidé divise la dérive de
              # ce site. C'est l'inverse de son poids, et rien d'autre.
              # Exact pour une derive a COUT REEL CONSTANT. Si la derive est une
              # depense de plus, le denominateur bouge aussi et le facteur n'est
              # qu'un ordre de grandeur — declare plutot que tu.
              "amortissement": round(cr / s["cout_reel_CR_MAD"], 1),
              # Ce qui se consolide SANS precaution : des montants. Le depassement prevu
              # a terminaison, site par site, s'additionne — et sa repartition n'a rien a
              # voir avec celle du budget.
              "depassement_prevu_MAD": round(s["EAC_si_la_derive_persiste_MAD"]
                                             - s["budget_a_l_achevement_BAC_MAD"], 2)}
             for s in sites_]
    dep_total = sum(x["depassement_prevu_MAD"] for x in poids)
    for x in poids:
        x["part_du_depassement_prevu_pct"] = round(
            x["depassement_prevu_MAD"] / dep_total * 100, 1)
    return {
        "nb_sites": len(sites_),
        "rapport_des_tailles_en_budget": round(
            max(s["budget_a_l_achevement_BAC_MAD"] for s in sites_)
            / min(s["budget_a_l_achevement_BAC_MAD"] for s in sites_), 1),
        "rapport_des_tailles_en_cout_reel": round(
            max(s["cout_reel_CR_MAD"] for s in sites_)
            / min(s["cout_reel_CR_MAD"] for s in sites_), 1),
        "budget_a_l_achevement_BAC_MAD": round(bac, 2),
        "valeur_planifiee_VP_MAD": round(vp, 2),
        "valeur_acquise_VA_MAD": round(va, 2),
        "cout_reel_CR_MAD": round(cr, 2),
        "CPI_consolide": round(cpi, 4),
        "SPI_consolide": round(spi, 4),
        "moyenne_des_CPI": round(moyenne_cpi, 4),
        "ecart_entre_les_deux_pts": round((cpi - moyenne_cpi) * 100, 1),
        "derive_totale_MAD": round(cr - va, 2),
        "depassement_prevu_total_MAD": round(dep_total, 2),
        "depassement_prevu_pct": round(dep_total / bac * 100, 1),
        "_ce_qui_se_consolide_vraiment": (
            "Les montants, et eux seuls. À terminaison, si les dérives persistent, "
            f"l'opération dépasse de {_f(dep_total, 0)} MAD, soit "
            f"{_f(dep_total / bac * 100, 1)} % du budget des ouvrages des deux sites. Et la répartition de ce "
            "dépassement ne ressemble pas à celle du budget : le site secondaire pèse "
            f"{_f(poids[1]['poids_du_budget_pct'], 1)} % du budget et "
            f"{_f(poids[1]['part_du_depassement_prevu_pct'], 1)} % du dépassement prévu. "
            "C'est ce rapport-là qui dit où aller, et il ne se lit sur aucun CPI."),
        "poids": poids,
        "seuil_de_vigilance_CPI": vig,
        "seuil_d_alerte_CPI": alerte_,
        "niveau_atteint": ("alerte" if cpi < alerte_
                           else "vigilance" if cpi < vig else "normal"),
        # La SENSIBILITE : combien de MAD de derive supplementaire sur chaque site pour
        # deplacer le CPI consolide d'un centieme. C'est la loi d'amortissement, en
        # monnaie, et elle est toujours bien posee — contrairement a une distance au
        # seuil, qui n'a de sens que si le seuil n'est pas deja franchi.
        # À COÛT RÉEL CONSTANT : une perte de valeur acquise. Si la dérive est au
        # contraire une DÉPENSE de plus, le dénominateur grandit aussi et il en faut
        # davantage — le module publie les deux plutôt que de laisser croire à un seul.
        "MAD_pour_un_centieme_de_CPI": round(0.01 * cr, 2),
        "MAD_pour_un_centieme_de_CPI_si_surcout": round(va / (cpi - 0.01) - cr, 2),
        "_le_centieme_depend_du_mecanisme": (
            f"{_f(0.01 * cr, 0)} MAD si la dérive est une valeur acquise en moins — un "
            "ouvrage repris, une quantité surestimée. "
            f"{_f(va / (cpi - 0.01) - cr, 0)} MAD si c'est une dépense en plus, "
            "parce qu'alors le dénominateur grandit avec le numérateur. Les deux "
            "mécanismes existent sur un chantier et ils ne se valent pas."),
        "lecture": (
            f"Les {len(sites_)} sites totalisent {_f(cr, 0)} MAD dépensés pour "
            f"{_f(va, 0)} MAD de valeur acquise : CPI consolidé "
            f"{_f(cpi, 3)}. La moyenne des CPI des sites vaut {_f(moyenne_cpi, 3)} — "
            f"{_f(abs(cpi - moyenne_cpi) * 100, 1)} points d'écart."),
        "_dans_quel_sens_va_l_ecart": (
            "Le consolidé est tiré vers le site qui a le plus DÉPENSÉ — c'est la seule "
            "chose qui soit vraie en général. Le sens de l'écart avec la moyenne, lui, "
            "dépend de quel site va mal : si c'est le petit, le consolidé est plus haut "
            "que la moyenne et il rassure ; si c'est le gros, il est plus bas et il "
            "alarme. Deux sites à 0,75 (9 MMAD dépensés) et 0,90 (1 MMAD) donnent un "
            "consolidé de 0,765 pour une moyenne de 0,825 : l'inverse du cas de ce "
            f"chantier. Ici le petit site est le plus dégradé, donc le consolidé "
            f"({_f(cpi, 3)}) est au-dessus de la moyenne ({_f(moyenne_cpi, 3)}) — et "
            "c'est le cas le plus fréquent, parce qu'un petit site reçoit moins "
            "d'encadrement et dérive plus souvent. Fréquent n'est pas toujours."),
        "_un_ratio_ne_se_consolide_pas": (
            "Le CPI est un rapport. La moyenne de deux rapports n'est pas le rapport des "
            "sommes, sauf si les dénominateurs sont égaux — c'est-à-dire si les deux "
            "sites ont dépensé exactement autant. Prendre la moyenne revient à donner le "
            "même poids à un site de "
            f"{_f(sites_[0]['cout_reel_CR_MAD'] / 1e6, 1)} MMAD et à un site de "
            f"{_f(sites_[1]['cout_reel_CR_MAD'] / 1e6, 1)} MMAD. Ce qui se consolide "
            "sans précaution, ce sont les MONTANTS : la dérive de l'opération est la "
            f"somme des dérives, {_f(round((cr - va) / 1e4) * 1e4, 0)} MAD, et elle se "
            "lit site par site."),
    }


def seuil_de_masquage(sites_: list, cons: dict, i_petit: int = 1) -> dict:
    """Jusqu'où un petit site peut dériver sans faire bouger l'indicateur consolidé.

    À coût réel constant, on cherche la valeur acquise du petit site qui amènerait le
    CPI consolidé exactement au seuil d'alerte. La différence avec sa valeur acquise
    actuelle est la dérive supplémentaire que le tableau de bord ne verra pas.
    """
    petit, cr_tot = sites_[i_petit], cons["cout_reel_CR_MAD"]
    # On mesure la distance au seuil qui n'est PAS encore franchi : une distance a un
    # seuil deja depasse n'a pas de sens, et la publier negative ferait un nombre juste
    # et illisible. Le niveau atteint est publie a cote, pour que le choix se voie.
    seuil = (cons["seuil_d_alerte_CPI"]
             if cons["CPI_consolide"] >= cons["seuil_d_alerte_CPI"]
             else cons["seuil_de_vigilance_CPI"])
    va_autres = cons["valeur_acquise_VA_MAD"] - petit["valeur_acquise_VA_MAD"]
    va_limite = seuil * cr_tot - va_autres
    # Le CPI limite est publie a quatre decimales : la derive invisible se calcule sur
    # CE nombre-la, pour qu'un lecteur qui multiplie les deux valeurs imprimees retrouve
    # la troisieme. L'ecart est de 150 MAD sur 689 000 — il ne change rien au resultat,
    # et il change tout a la verifiabilite.
    cpi_limite = round(va_limite / petit["cout_reel_CR_MAD"], 4)
    invisible = petit["valeur_acquise_VA_MAD"] - cpi_limite * petit["cout_reel_CR_MAD"]
    return {
        "site": petit["site"],
        "seuil_retenu_CPI": seuil,
        "quel_seuil": ("alerte" if seuil == cons["seuil_d_alerte_CPI"] else "vigilance"),
        "niveau_consolide_atteint": cons["niveau_atteint"],
        "CPI_du_site_aujourd_hui": petit["CPI"],
        "CPI_du_site_au_seuil_consolide": cpi_limite,
        "derive_supplementaire_invisible_MAD": round(invisible, 2),
        # À COÛT RÉEL CONSTANT. Si la derive supplementaire est une DEPENSE de plus, le
        # denominateur du consolide grandit aussi, et il en faut davantage pour franchir
        # le seuil. Les deux mecanismes sont publies : le module ne choisit pas en
        # silence celui qui donne le plus joli nombre.
        "derive_invisible_si_surcout_MAD": round(
            cons["valeur_acquise_VA_MAD"] / seuil - cr_tot, 2),
        "_les_deux_mecanismes": (
            "Une dérive peut être une valeur acquise en moins (un ouvrage repris, une "
            "quantité surestimée) ou une dépense en plus (des heures, un matériel). "
            "À coût réel constant — le premier cas — le site peut perdre "
            f"{_f(invisible, 0)} MAD sans faire franchir le seuil. Si c'est une dépense "
            "en plus, il en faut "
            f"{_f(cons['valeur_acquise_VA_MAD'] / seuil - cr_tot, 0)}"
            " MAD, parce que le dénominateur grandit avec elle. Le second cas est le "
            "plus fréquent sur un chantier, et c'est le plus favorable au masquage."),
        "part_du_budget_du_site_pct": round(
            invisible / petit["budget_a_l_achevement_BAC_MAD"] * 100, 1),
        "le_consolide_est_il_deja_sous_le_seuil": cons["CPI_consolide"] < seuil,
        "MAD_pour_un_centieme_de_CPI": cons["MAD_pour_un_centieme_de_CPI"],
        "centiemes_de_CPI_par_centieme_du_site": round(
            petit["cout_reel_CR_MAD"] / cons["cout_reel_CR_MAD"], 3),
        "lecture": (
            f"Le consolidé est en {cons['niveau_atteint']} "
            f"({_f(cons['CPI_consolide'], 3)}). Le seuil d'alerte est fixé à CPI "
            f"{_f(seuil, 2)}. "
            f"À coût réel constant, le site secondaire peut tomber de "
            f"{_f(petit['CPI'], 3)} à {_f(cpi_limite, 3)} avant que le CPI consolidé ne "
            f"l'atteigne : {_f(invisible, 0)} MAD de dérive supplémentaire, soit "
            f"{_f(invisible / petit['budget_a_l_achevement_BAC_MAD'] * 100, 0)} % du "
            "budget de ce site, que le tableau de bord consolidé ne montrera pas."),
        "_la_loi": (
            "Ce n'est pas une particularité de ce chantier : un indicateur consolidé "
            "divise la dérive d'un site par le poids de ce site. Le site secondaire pèse "
            f"{_f(cons['poids'][i_petit]['poids_du_cout_pct'], 1)} % du coût réel, donc "
            f"sa dérive apparaît {_f(cons['poids'][i_petit]['amortissement'], 1)} fois "
            "plus petite. Un seuil unique appliqué à tous les étages d'agrégation est "
            "donc un seuil différent à chaque étage — et personne ne l'a décidé."),
    }


def masquage_recursif(sites_: list, i: int = 1) -> dict:
    """Ce que le consolidé fait au site, le site le fait à ses lots.

    Même mécanique, un étage plus bas : le CPI d'un site est le rapport des sommes de ses
    lots, et il amortit la dérive de chacun par son poids. Le nombre d'étages est le vrai
    sujet — à trois étages, une dérive de lot arrive divisée par le produit des poids.
    """
    site = sites_[i]
    demarres = [x for x in site["lots"] if x["demarre"]]
    pire = min(demarres, key=lambda x: x["CPI"])
    amort = site["cout_reel_CR_MAD"] / pire["cout_reel_MAD"]
    # Les deux amortissements se MULTIPLIENT : c'est le point du paragraphe.
    return {
        "site": site["site"],
        "lot_le_plus_degrade": pire["lot"],
        "CPI_du_lot": pire["CPI"],
        "CPI_du_site": site["CPI"],
        "poids_du_lot_dans_le_cout_du_site_pct": round(
            pire["cout_reel_MAD"] / site["cout_reel_CR_MAD"] * 100, 1),
        "amortissement_du_lot_par_le_site": round(amort, 1),
        "nb_lots_demarres": len(demarres),
        "nb_lots": len(site["lots"]),
        "derive_du_lot_MAD": pire["derive_MAD"],
        "part_de_la_derive_du_site_pct": round(
            pire["derive_MAD"] / site["derive_MAD"] * 100, 1) if site["derive_MAD"] else None,
        "lecture": (
            f"Sur le site secondaire, {len(demarres)} lots sur {len(site['lots'])} sont "
            f"démarrés, et un seul porte "
            f"{_f(pire['derive_MAD'] / site['derive_MAD'] * 100, 0)} % de la dérive : "
            f"« {pire['lot']} », CPI {_f(pire['CPI'], 3)} contre "
            f"{_f(site['CPI'], 3)} pour le site. Le site amortit déjà son lot d'un "
            f"facteur {_f(amort, 1)}."),
        "_les_amortissements_se_multiplient": (
            "C'est le point : chaque étage d'agrégation divise par le poids. Le lot est "
            f"amorti {_f(amort, 1)} fois par son site, et le site l'est encore par "
            "l'opération. Un tableau de bord d'opération à deux étages montre donc la "
            "dérive d'un lot divisée par le PRODUIT des deux poids. C'est pourquoi un "
            "chef de projet suivi ne lit jamais le seul indicateur consolidé : il lit la "
            "ligne qui a bougé, et il faut que le tableau de bord la lui donne."),
    }


# ------------------------------------------------- 3. la latence du reporting
def latence(d: dict, rec: dict) -> dict:
    """Combien de temps une dérive vit avant d'être lisible, et ce que ces jours coûtent.

    Une dérive qui commence au hasard dans une période de reporting est lisible, en
    moyenne, une demi-période plus tard, plus le délai de remontée des données. C'est une
    espérance, pas un majorant : le pire cas vaut une période entière plus le délai.
    """
    r = d["multi_sites"]["reporting"]
    cout_jour = rec["cout_d_un_jour"]["cout_hors_penalites_MAD_par_jour_ouvre"]
    remontee, rem_b = r["delai_de_remontee_j"]["valeur"], _b(r["delai_de_remontee_j"])
    lignes = []
    for cle, nom in (("periode_hebdomadaire_j", "reporting hebdomadaire"),
                     ("periode_mensuelle_j", "reporting mensuel")):
        per, per_b = r[cle]["valeur"], _b(r[cle])
        moyenne = per / 2 + remontee
        pire = per + remontee
        lignes.append({
            "rythme": nom,
            "periode_j": per,
            "delai_de_remontee_j": remontee,
            "latence_moyenne_j": round(moyenne, 1),
            "latence_pire_cas_j": round(pire, 1),
            "latence_moyenne_bornes_j": [round(per_b[0] / 2 + rem_b[0], 1),
                                         round(per_b[1] / 2 + rem_b[1], 1)],
            "cout_de_la_latence_moyenne_MAD": round(moyenne * cout_jour, 2),
        })
    ecart = lignes[1]["latence_moyenne_j"] - lignes[0]["latence_moyenne_j"]
    return {
        "lignes": lignes,
        "cout_d_un_jour_MAD": cout_jour,
        "_source_du_cout": "calc/sorties/reception.json — coût d'un jour hors pénalités "
                           "(module REC), c'est-à-dire les frais de durée seuls",
        "_le_domaine_de_ce_cout": (
            "Ce coût journalier est celui de l'OPÉRATION — les frais de durée du site "
            "principal, qui portent l'essentiel de l'encadrement. Il est juste pour "
            "chiffrer la latence d'un dispositif de reporting qui couvre l'opération "
            "entière. Il serait faux appliqué au seul site secondaire, dont les frais "
            "de durée sont bien plus petits : ce cours ne les possède pas, et ne "
            "chiffre donc pas la latence site par site."),
        "ecart_des_deux_rythmes_j": round(ecart, 1),
        "les_bornes_des_deux_rythmes_se_chevauchent": (
            lignes[0]["latence_moyenne_bornes_j"][1]
            > lignes[1]["latence_moyenne_bornes_j"][0]),
        "_ce_que_le_chevauchement_veut_dire": (
            "Les fourchettes des deux latences se chevauchent : un reporting "
            "hebdomadaire mal alimenté (remontée à "
            f"{_f(rem_b[1])} jours) est plus lent qu'un reporting mensuel bien alimenté. "
            "L'écart des deux rythmes, lui, ne dépend PAS du délai de remontée — il "
            "s'annule dans la différence. Les deux leviers sont donc indépendants, et "
            "c'est pourquoi il faut les tirer tous les deux."),
        "cout_de_l_ecart_MAD": round(ecart * cout_jour, 2),
        "part_du_delai_de_remontee_dans_l_hebdo_pct": round(
            remontee / lignes[0]["latence_moyenne_j"] * 100, 1),
        "lecture": (
            f"Une dérive qui commence un jour quelconque devient lisible en moyenne "
            f"{_f(lignes[0]['latence_moyenne_j'], 1)} jours plus tard en reporting "
            f"hebdomadaire, et {_f(lignes[1]['latence_moyenne_j'], 1)} jours en reporting "
            f"mensuel : {_f(ecart, 1)} jours d'écart, soit {_f(ecart * cout_jour, 0)} MAD "
            "de frais de durée à chaque dérive détectée."),
        "_le_delai_de_remontee_est_la_moitie_du_sujet": (
            f"En reporting hebdomadaire, le délai de remontée des données "
            f"({_f(remontee)} jours) pèse "
            f"{_f(remontee / lignes[0]['latence_moyenne_j'] * 100, 0)} % de la latence "
            f"totale — contre {_f(remontee / lignes[1]['latence_moyenne_j'] * 100, 0)} % "
            "en reporting mensuel, où la période écrase tout. Ce n'est donc pas « la "
            "moitié de la latence » en général : c'est la moitié DÈS QU'ON RACCOURCIT "
            "LE RYTHME, et c'est ce qui plafonne le gain. Passer d'un rapport mensuel à un rapport hebdomadaire sans "
            "raccourcir la remontée ne divise donc pas la latence par quatre : c'est la "
            "part oubliée de toutes les décisions de rythme, et elle ne s'achète pas "
            "avec une réunion de plus — elle s'achète avec des attachements saisis le "
            "jour même."),
        "_ce_que_la_latence_n_est_pas": (
            "Ces jours ne sont pas « perdus » au sens d'un retard : le chantier continue. "
            "Ils sont le temps pendant lequel une dérive produit ses effets sans que "
            "personne puisse décider. Les chiffrer aux frais de durée est un ordre de "
            "grandeur, pas une facture : ce que coûte vraiment une décision retardée "
            "dépend de ce qu'on aurait fait — et c'est précisément l'argument pour "
            "raccourcir la boucle plutôt que pour l'estimer finement."),
    }


# ------------------------------------------------- 4. l'alerte qui compte vraiment
def alerte_ferroviaire(d: dict, cout_jour: float) -> dict:
    """Sur un chantier ferroviaire, le bon seuil d'alerte n'est pas un pourcentage.

    Un retard se rattrape tant qu'il reste plus court que la période entre deux fenêtres
    de consignation. Au-delà, la fenêtre est perdue et le travail attend la suivante :
    le retard ne grandit pas, il SAUTE (D-050). Le seuil d'alerte d'un site est donc
    cette période, en jours, et elle ne ressemble à aucun indicateur de coût.
    """
    # La période entre fenêtres est déclarée dans le bloc de planning des consignations.
    bloc = None
    for chemin in (d.get("planning", {}), d.get("ferroviaire", {})):
        for k, v in chemin.items():
            if isinstance(v, dict) and "periode_entre_fenetres_jours" in v:
                bloc = v
                break
    if bloc is None:
        raise KeyError("periode_entre_fenetres_jours introuvable dans data/")
    periode = bloc["periode_entre_fenetres_jours"]["valeur"]
    per_b = _b(bloc["periode_entre_fenetres_jours"])
    s2 = d["multi_sites"]["sites"][1]
    retard, ret_b = s2["retard_constate_j"]["valeur"], _b(s2["retard_constate_j"])
    besoin = s2["date_de_besoin_premiere_interception_j"]["valeur"]
    cycles = math.ceil(retard / periode)
    retard_effectif = cycles * periode
    return {
        "periode_entre_fenetres_j": periode,
        "periode_bornes_j": list(per_b),
        "_source_de_la_periode": "data/ — bloc de consignation du planning (module D2, "
                                 "corrigé par B7c)",
        "retard_constate_du_site_j": retard,
        "retard_bornes_j": list(ret_b),
        "cycles_perdus": cycles,
        "retard_effectif_j": retard_effectif,
        "amplification": round(retard_effectif / retard, 2) if retard else None,
        "date_de_besoin_j": besoin,
        "date_de_besoin_apres_retard_j": besoin + retard_effectif,
        "seuil_d_alerte_du_site_j": periode,
        "le_retard_a_t_il_deja_franchi_le_seuil": retard > periode,
        "retard_tolerable_restant_j": round(cycles * periode - retard, 1),
        # CE QU'IL FAUT RATTRAPER pour descendre d'une marche : redescendre sous le
        # multiple inferieur de la periode. Une premiere version de l'exercice 4 affirmait
        # qu'il fallait « plus de dix jours » et que dix jours ne produiraient rien : les
        # deux etaient faux, et l'escalier publie par le module disait deja l'inverse.
        "jours_a_rattraper_pour_gagner_un_cycle": round(
            max(0.0, retard - (cycles - 1) * periode), 1) if cycles > 1 else None,
        "gain_si_on_gagne_un_cycle_j": periode if cycles > 1 else None,
        "effet_de_rattraper_10_j": (math.ceil(max(0.0, retard - 10) / periode) * periode
                                    if retard > 10 else 0),
        "_ce_que_rattraper_veut_dire": (
            f"Pour descendre d'une marche, il suffit de repasser sous "
            f"{_f((cycles - 1) * periode)} jours de retard, c'est-à-dire d'en rattraper "
            f"{_f(max(0.0, retard - (cycles - 1) * periode))}. Ces "
            f"{_f(max(0.0, retard - (cycles - 1) * periode))} jours-là en valent "
            f"{_f(periode)} : c'est le meilleur rapport du chantier. Les suivants n'en "
            "valent aucun, jusqu'à la marche d'après. **La question n'est jamais "
            "« combien peut-on rattraper » mais « de quel côté de la marche "
            "tombe-t-on »**."
            if cycles > 1 else
            "Le retard tient dans une seule fenêtre : il n'y a pas de marche à "
            "descendre."),
        "lecture": (
            f"Le site secondaire accuse {_f(retard)} jours ouvrés de retard. La période "
            f"entre deux fenêtres de consignation est de {_f(periode)} jours : le retard "
            f"a donc franchi la première marche, et la fenêtre visée est perdue : le "
            f"travail attend la {_f(cycles)}ᵉ fenêtre. Le retard effectif "
            f"sur la première interception n'est pas de {_f(retard)} jours mais de "
            f"{_f(retard_effectif)} — une amplification de "
            f"{_f(retard_effectif / retard, 2) if retard else '—'}."),
        "_le_seuil_est_une_duree_pas_un_ratio": (
            f"C'est le résultat le plus utile de ce module pour un chantier ferroviaire : "
            f"le seuil d'alerte d'un site n'est ni 5 % de dérive ni CPI 0,95, c'est "
            f"{_f(periode)} JOURS — la période entre deux fenêtres. En deçà, un retard se "
            "rattrape dans la fenêtre suivante ; au-delà, il coûte un cycle entier et "
            "aucun indicateur de coût ne le voit venir, parce qu'un cycle perdu ne "
            "dépense rien : il attend."),
        "cout_d_un_cycle_perdu_en_frais_de_duree_MAD": round(periode * cout_jour, 2),
        "_pourquoi_le_CPI_ne_sert_a_rien_ici": (
            "Un cycle perdu ne produit **ni valeur acquise ni dépense d'ouvrage** : dans "
            "le périmètre où ce cours calcule le CPI — les ouvrages seuls, frais de "
            "durée exclus, comme le module D4 le publie — l'indicateur ne bouge pas d'un "
            "millième. L'opération, elle, paie : "
            f"{_f(periode)} jours de frais de durée, soit "
            f"{_f(periode * cout_jour, 0)} MAD. C'est le pire des deux mondes — une "
            "dépense réelle qu'AUCUN indicateur de performance ne montre, parce qu'elle "
            "est hors de son périmètre par construction. Le SPI finit par bouger, avec "
            "la latence du reporting et l'amortissement de l'agrégation. L'alerte qui "
            "aurait servi est d'une autre nature : une date de besoin, une période de "
            "fenêtre, et une soustraction."),
    }


def interfaces_a_date(d: dict, fer: dict, su: dict, pl: dict,
                      periode_fenetres: float) -> dict:
    """Les interfaces, rangées par leur DATE LIMITE DE DEMANDE plutôt que par leur objet.

    Le module B7c publie le registre des interfaces et leur délai de demande. Ce qui
    manque à un chef de projet suivi, c'est la date : à quelle date faut-il avoir déposé
    chaque demande pour que le besoin soit servi. C'est une soustraction, et c'est elle
    qui devrait ouvrir une revue de projet.
    """
    j_arret = su["date_arret"]["jour_ouvre"]
    # Les délais du registre sont en jours CALENDAIRES ; les dates du planning en jours
    # OUVRÉS. La conversion passe par le ratio du calendrier de D2, déclaré une fois.
    ratio = round(pl["calendrier"]["duree_ouvree_j"]
                  / json.loads((RACINE / "calc" / "sorties" / "prix.json")
                               .read_text(encoding="utf-8"))["bordereau"]
                  ["frais_de_duree"]["duree_mois_calendaires"], 2)
    lignes = []
    for s in d["multi_sites"]["sites"]:
        retard_site = (s.get("retard_constate_j") or {}).get("valeur", 0)
        retard_effectif_site = (math.ceil(retard_site / periode_fenetres) * periode_fenetres
                                if retard_site else 0)
        b = s.get("date_de_besoin_premiere_interception_j")
        if not b:
            continue
        if "valeur" in b:
            besoin = b["valeur"]
        else:
            # La date du site principal n'est pas déclarée : elle est LUE dans le réseau,
            # au chemin que data/ indique. Une date de planning se lit, elle ne se pose pas.
            cur = pl
            for cle in b["_lu_dans"].split("."):
                cur = cur[cle]
            besoin = cur
        for it in fer["interfaces"]["liste"]:
            if it["nature"] != "decision":
                continue
            delai_ouvre = it["delai_de_demande_j"] / 30.44 * ratio
            limite = besoin - delai_ouvre
            # Une date limite ne veut rien dire pour un besoin DÉJÀ SERVI : si le
            # travail est en cours, la demande a forcément été faite. Seules les lignes
            # dont le besoin est encore devant nous portent un risque, et ce sont les
            # seules que la revue doit lire.
            passe = besoin <= j_arret
            lignes.append({
                "site": s["id"],
                "interface": f"{it['de']} → {it['a']}",
                "objet": it["objet"],
                "delai_calendaire_j": it["delai_de_demande_j"],
                "delai_ouvre_j": round(delai_ouvre, 1),
                "date_de_besoin_j": besoin,
                "date_limite_de_demande_j": round(limite, 1),
                "marge_a_la_date_d_arret_j": round(limite - j_arret, 1),
                "statut": ("besoin déjà servi" if passe
                           else "demande en retard" if limite < j_arret
                           else "à déposer"),
                "deja_depassee": (not passe) and limite < j_arret,
                # Ce que le retard du site fait à cette échéance. Un retard DÉCALE le
                # besoin, donc il recule la date limite : il peut rattraper une demande
                # en retard. C'est contre-intuitif et c'est vrai.
                # Le besoin se decale du retard EFFECTIF — celui que l'escalier des
                # fenetres impose — et non du retard brut : le travail ne peut avoir
                # lieu qu'a une fenetre. Publier les deux dates donnerait 212 ici et
                # 230 la, pour le meme evenement.
                "marge_apres_le_retard_du_site_j": round(
                    limite + retard_effectif_site - j_arret, 1)
                if (not passe) and retard_effectif_site else None,
            })
    # Rangées par marge, mais les besoins déjà servis en dernier : ils ne portent plus
    # de décision, et les laisser en tête ferait lire une liste d'alarmes éteintes.
    lignes.sort(key=lambda x: (x["statut"] == "besoin déjà servi",
                               x["marge_a_la_date_d_arret_j"]))
    depassees = [x for x in lignes if x["deja_depassee"]]
    a_venir = [x for x in lignes if x["statut"] != "besoin déjà servi"]
    return {
        "date_d_arret_j": j_arret,
        "jours_ouvres_par_mois_calendaire": ratio,
        "_d_ou_vient_le_ratio": "durée ouvrée du chantier (D2) divisée par sa durée en "
                                "mois calendaires (D1) : le même ratio que le module C1, "
                                "et il n'est écrit nulle part à la main",
        "lignes": lignes,
        "nb_depassees": len(depassees),
        "nb_a_venir": len(a_venir),
        "nb_besoins_deja_servis": len(lignes) - len(a_venir),
        "la_plus_depassee": depassees[0] if depassees else None,
        "la_plus_urgente_encore_tenable": next(
            (x for x in lignes if not x["deja_depassee"]), None),
        "lecture": (
            f"À la date d'arrêt (jour {_f(j_arret, 0)}), {len(depassees)} des "
            f"{len(a_venir)} demandes d'interface encore à venir est déjà en "
            f"retard — la plus ancienne de {_f(abs(depassees[0]['marge_a_la_date_d_arret_j']), 0)} "
            f"jours — et la plus urgente de celles qui tiennent encore a "
            f"{_f(next(x['marge_a_la_date_d_arret_j'] for x in lignes if not x['deja_depassee']), 0)} "
            "jours de marge."
            if depassees else
            f"À la date d'arrêt (jour {_f(j_arret, 0)}), aucune demande n'est en retard ; "
            f"la plus urgente a {_f(lignes[0]['marge_a_la_date_d_arret_j'], 0)} jours de "
            "marge."),
        "_ce_que_cette_table_remplace": (
            "Une liste d'interfaces rangée par objet se lit une fois et se classe. La "
            "même liste rangée par MARGE se lit à chaque revue, et elle dit quoi faire "
            "cette semaine. C'est la même donnée : seule la soustraction a été faite."),
        "_la_limite_declaree": (
            "Les délais du registre sont en jours calendaires et les dates du planning en "
            f"jours ouvrés : la conversion utilise {_f(ratio, 2)} jours ouvrés par mois "
            "calendaire, le même ratio que les modules D1 et C1. C'est une conversion "
            "déclarée, pas un calendrier réel — un calendrier réel tiendrait compte des "
            "jours fériés et des périodes de gel d'exploitation, que ce cours ne possède "
            "pas (⏸)."),
    }


# ------------------------------------------------- 5. figures
def figures(sites_: list, cons: dict, mas: dict, lat: dict, alerte: dict,
            interf: dict) -> dict:
    return {
        # La legende de couleur est CALCULEE : elle porte le seuil declare dans data/,
        # et une figure ne peut pas resoudre une variable dans ses options.
        "legende_seuil_alerte": f"sous le seuil d'alerte de "
                                f"{_f(cons['seuil_d_alerte_CPI'], 2)}",
        # Ce que chaque site pèse, et ce que chacun dérive : deux séries, même axe.
        "derive_par_site": [{"libelle": s["site"].split(" (")[0],
                             "valeur": round(s["derive_MAD"] / 1000),
                             "alerte": s["CPI"] < cons["seuil_d_alerte_CPI"]}
                            for s in sites_],
        "cpi_par_site": [{"libelle": s["site"].split(" (")[0],
                          "valeur": round(s["CPI"], 3),
                          "alerte": s["CPI"] < cons["seuil_d_alerte_CPI"]}
                         for s in sites_]
        + [{"libelle": "Consolidé", "valeur": round(cons["CPI_consolide"], 3),
            "alerte": cons["CPI_consolide"] < cons["seuil_d_alerte_CPI"]},
           {"libelle": "Moyenne des CPI — à ne pas utiliser",
            "valeur": round(cons["moyenne_des_CPI"], 3),
            "alerte": cons["moyenne_des_CPI"] < cons["seuil_d_alerte_CPI"]}],
        # Les lots du site secondaire, par leur dérive : la ligne qui a bougé.
        "lots_du_site_secondaire": [
            {"libelle": x["lot"].split(" · ")[-1],
             "valeur": round(x["derive_MAD"] / 1000),
             # Le seuil de l'OPERATION, applique tel quel a un lot : c'est
             # exactement ce que le § S3b deconseille, et la figure le montre pour
             # qu'on le voie. Un troisieme seuil invente ici n'aurait ete decide
             # par personne.
             "alerte": (x["CPI"] is not None
                        and x["CPI"] < cons["seuil_d_alerte_CPI"])}
            for x in sites_[1]["lots"] if x["demarre"]],
        "latence": [{"libelle": x["rythme"], "valeur": x["latence_moyenne_j"]}
                    for x in lat["lignes"]],
        # L'amplification d'un retard par la période des fenêtres : un escalier.
        "retard_quantise": [
            {"x": j, "v": math.ceil(j / alerte["periode_entre_fenetres_j"])
             * alerte["periode_entre_fenetres_j"] if j > 0 else 0}
            for j in range(0, int(2.5 * alerte["periode_entre_fenetres_j"]) + 1, 1)],
        "marqueur_retard": {
            "x": alerte["retard_constate_du_site_j"],
            "libelle": f"{alerte['retard_constate_du_site_j']} j constatés → "
                       f"{alerte['retard_effectif_j']} j subis"},
        # Seules les lignes qui portent ENCORE une decision : la legende de la figure
        # annonce l'absence des besoins deja servis, il faut qu'elle dise vrai.
        "interfaces": [{"libelle": f"{x['site']} · " + _court(x["objet"], 30),
                        "valeur": x["marge_a_la_date_d_arret_j"],
                        "alerte": x["deja_depassee"]}
                       for x in interf["lignes"]
                       if x["statut"] != "besoin déjà servi"],
    }


# ------------------------------------------------- assemblage
def tout_calculer(d: dict) -> dict:
    S = RACINE / "calc" / "sorties"
    su = json.loads((S / "suivi.json").read_text(encoding="utf-8"))
    pl = json.loads((S / "planification.json").read_text(encoding="utf-8"))
    rec = json.loads((S / "reception.json").read_text(encoding="utf-8"))
    fer = json.loads((S / "ferroviaire.json").read_text(encoding="utf-8"))
    st = sites(d, su)
    cons = consolidation(st, d["multi_sites"]["seuils_du_tableau_de_bord"])
    mas = seuil_de_masquage(st, cons)
    rec_mas = masquage_recursif(st)
    lat = latence(d, rec)
    al = alerte_ferroviaire(
        d, rec["cout_d_un_jour"]["cout_hors_penalites_MAD_par_jour_ouvre"])
    itf = interfaces_a_date(d, fer, su, pl, al["periode_entre_fenetres_j"])
    return {
        "date_d_arret_j": su["date_arret"]["jour_ouvre"],
        "sites": st,
        "consolidation": cons,
        "seuil_de_masquage": mas,
        "masquage_recursif": rec_mas,
        "latence": lat,
        "alerte_ferroviaire": al,
        "interfaces": itf,
        "figures": figures(st, cons, mas, lat, al, itf),
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    r = tout_calculer(d)
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "pilotage.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for s in r["sites"]:
        print(f"  {s['site'][:38]:<40} BAC {s['budget_a_l_achevement_BAC_MAD']/1e6:>5.1f} M · "
              f"CPI {s['CPI']:.3f} · SPI {s['SPI']:.3f} · derive "
              f"{s['derive_MAD']/1e6:>5.2f} M")
    c = r["consolidation"]
    print(f"consolide : CPI {c['CPI_consolide']:.3f} contre moyenne "
          f"{c['moyenne_des_CPI']:.3f} — {c['ecart_entre_les_deux_pts']} pts")
    m = r["seuil_de_masquage"]
    print(f"masquage : le petit site peut tomber a CPI {m['CPI_du_site_au_seuil_consolide']:.3f} "
          f"— {m['derive_supplementaire_invisible_MAD']/1e6:.2f} M invisibles")
    rm = r["masquage_recursif"]
    print(f"recursif : lot {rm['CPI_du_lot']:.3f} dans un site a {rm['CPI_du_site']:.3f} "
          f"(amorti x{rm['amortissement_du_lot_par_le_site']})")
    l = r["latence"]
    print(f"latence : {l['lignes'][0]['latence_moyenne_j']} j (hebdo) contre "
          f"{l['lignes'][1]['latence_moyenne_j']} j (mensuel) — "
          f"{l['cout_de_l_ecart_MAD']/1e3:.0f} kMAD")
    a = r["alerte_ferroviaire"]
    print(f"alerte : retard {a['retard_constate_du_site_j']} j -> {a['retard_effectif_j']} j "
          f"(x{a['amplification']}), seuil = {a['seuil_d_alerte_du_site_j']} j")
    print(f"interfaces : {r['interfaces']['nb_depassees']} depassees sur "
          f"{len(r['interfaces']['lignes'])}")
