"""Réception, DOE, garanties : la fin de chantier, et ce qu'elle coûte par jour (REC).

Dernier module du palier 1. Il ferme le déroulé du § 10.2, et il a un cœur calculable que
les modules précédents ont préparé sans le savoir : D1 publie les frais de durée et les
pénalités, D2 publie la date et le réseau, C7 publie le coût d'une non-conformité. REC
n'en recalcule aucun — il les lit, et il en tire ce qu'aucun d'eux ne pouvait voir.

Cinq résultats, tous non normatifs :

1. **Un jour de non-réception n'a pas un prix, il en a DEUX**, et c'est la correction la
   plus lourde apportée à ce module. Les pénalités ne courent qu'au-delà du terme
   contractuel, et elles cessent de croître au plafond. Le coût d'un jour est donc le
   même AVANT le terme et APRÈS le plafond — les frais de durée seuls — et huit fois
   plus élevé entre les deux. Ce n'est pas une courbe croissante : c'est une fenêtre de
   cherté, et savoir où l'on est dedans change toutes les décisions de fin de chantier.
2. **Le jour de bascule ne dépend pas du montant du marché** : c'est le plafond en
   pour-cent divisé par la pénalité en pour-mille, et rien d'autre.
3. **L'arbitrage entre retenue de garantie et caution bancaire ne dépend pas de la durée
   de la garantie** — qui est ⏸. La durée se simplifie (D-054).
4. **Une liste de réserves ne se hiérarchise pas par son volume mais par son délai le
   plus long.** Ce qui coûte n'est pas le nombre de lignes : c'est la pièce qu'on
   attend.
5. **Le DOE se constitue pendant le chantier.** Reconstitué après coup, il coûte quatre
   fois plus d'heures de cadre, et il bloque le décompte définitif pendant ce temps.

Ce que le module ne dit pas, et ne dira pas tant que les documents manquent : les durées
des garanties, le délai de levée des réserves, les conditions d'une réception tacite, le
contenu obligatoire du DOE, et les EFFETS JURIDIQUES de la réception. Il donne le
mécanisme et sa conséquence financière.
"""
from __future__ import annotations
import json, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "calc"))


def _f(x: float, dec: int = 0) -> str:
    """Format français : espace fine insécable, virgule décimale (voir calc/qualite.py)."""
    s = f"{x:,.{dec}f}".replace(",", " ")
    return s.replace(".", ",") if dec else s


def _b(o: dict) -> tuple[float, float]:
    f = o.get("fourchette")
    return (float(f[0]), float(f[1])) if f else (float(o["valeur"]), float(o["valeur"]))


# ------------------------------------------------- 1. le prix d'un jour
def cout_d_un_jour(d: dict, pr: dict) -> dict:
    """Ce que coûte une journée de plus avant la réception — et il y a DEUX prix.

    La correction la plus lourde de ce module, et elle est venue d'une passe adversariale.
    La première version publiait un seul « coût d'un jour de non-réception » :
    127 850 MAD, frais de durée plus pénalité, appliqué à toutes les journées de la fin
    de chantier — les opérations préalables, l'hésitation sur les réserves, le vendredi
    d'un exercice. Or ce que le module D1 publie est le coût d'un jour de RETARD, et les
    pénalités ne courent qu'au-delà du terme contractuel. Avant ce terme, une journée
    perdue ne coûte que les frais de durée. Tout l'argent du module était multiplié par
    huit, et aucun test ne pouvait le voir : l'arithmétique était juste, c'est la
    CONDITION qui n'était pas écrite.

    Il y a donc trois périodes et deux prix seulement, parce que le premier et le
    troisième sont le même :

        avant le terme contractuel ........ frais de durée seuls
        du terme au plafond ............... frais de durée + pénalité
        après le plafond .................. frais de durée seuls

    Ce n'est pas une courbe croissante, c'est une FENÊTRE de cherté. Savoir si l'on est
    dedans est la première question à poser avant de chiffrer un jour de fin de chantier,
    et personne ne la pose.

    Les deux termes sont LUS dans la sortie de D1 (D-039), jamais recalculés. Le piège de
    calendrier vient de lui et il est conservé : les pénalités se comptent en jours
    calendaires et les frais de durée en jours ouvrés.
    """
    c = d["prix_unitaires_MAD"]["contrat"]
    r1 = pr["cout_du_retard"]["1"]
    conv = pr["bordereau"]["frais_de_duree"]["conversion"]["calendaires_par_jour_ouvre"]
    frais = r1["frais_de_duree_MAD"]
    penal = r1["penalites_MAD"]
    plafond = r1["penalites_plafond_MAD"]
    marche = pr["bordereau"]["prix_de_vente_MAD"]

    sans_penalite = penal <= 0
    bascule_ouvres = None if sans_penalite else plafond / penal
    bascule_calendaires = None if sans_penalite else bascule_ouvres * conv
    hors, sous = frais, frais + penal

    plafond_pct = c["penalite_plafond_pct"]["valeur"]
    pour_mille = c["penalite_retard_pour_mille_par_j"]["valeur"]
    pm_b = _b(c["penalite_retard_pour_mille_par_j"])
    pf_b = _b(c["penalite_plafond_pct"])
    forme_fermee = None if sans_penalite else plafond_pct * 10.0 / pour_mille
    bornes_j = [] if sans_penalite else [round(pf_b[0] * 10.0 / pm_b[1], 1),
                                         round(pf_b[1] * 10.0 / pm_b[0], 1)]
    # Bornes du coût d'un jour SOUS pénalités : seule la clause de pénalité est une
    # hypothèse ici. Les frais de durée viennent de D1, qui les publie sans bornes — le
    # dire est plus honnête que de les inventer, et c'est la borne qui manque.
    sous_b = [round(frais + marche * pm_b[0] / 1000 * conv, 2),
              round(frais + marche * pm_b[1] / 1000 * conv, 2)]
    return {
        "marche_MAD": marche,
        "frais_de_duree_MAD_par_jour_ouvre": frais,
        "penalites_MAD_par_jour_ouvre": penal,
        "_source": "calc/sorties/prix.json — cout_du_retard (module D1), jamais recalculé ici",
        "plafond_des_penalites_MAD": plafond,
        "cout_hors_penalites_MAD_par_jour_ouvre": round(hors, 2),
        "cout_sous_penalites_MAD_par_jour_ouvre": round(sous, 2),
        "cout_sous_penalites_bornes_MAD": sous_b,
        "rapport_des_deux_regimes": round(sous / hors, 1) if hors else None,
        "rapport_bornes": ([round(sous_b[0] / hors, 1), round(sous_b[1] / hors, 1)]
                           if hors else None),
        "sans_penalite": sans_penalite,
        "jour_de_bascule_ouvre": None if sans_penalite else round(bascule_ouvres, 1),
        "jour_de_bascule_calendaire": (None if sans_penalite
                                       else round(bascule_calendaires, 1)),
        "jour_de_bascule_bornes_calendaires": bornes_j or None,
        "largeur_de_la_fenetre_ouvres": None if sans_penalite else round(bascule_ouvres, 1),
        "ecart_des_deux_calendriers_j": (None if sans_penalite
                                         else round(bascule_calendaires - bascule_ouvres, 1)),
        "forme_fermee_calendaire": None if sans_penalite else round(forme_fermee, 1),
        "les_trois_periodes": [
            {"periode": "avant le terme contractuel", "regime": "hors pénalités",
             "cout_MAD_par_jour_ouvre": round(hors, 2)},
            {"periode": "du terme contractuel au plafond", "regime": "sous pénalités",
             "cout_MAD_par_jour_ouvre": round(sous, 2)},
            {"periode": "après le plafond", "regime": "hors pénalités",
             "cout_MAD_par_jour_ouvre": round(hors, 2)},
        ],
        "_la_condition_qui_manquait": (
            "Un jour de fin de chantier ne coûte la pénalité QUE si le chantier est déjà "
            "au-delà de son terme contractuel. Avant, il coûte les frais de durée seuls "
            f"— {_f(hors)} MAD. Entre le terme et le plafond, il en coûte {_f(sous)}. "
            f"Après le plafond, il retombe à {_f(hors)}."
            + (f" Les deux prix sont dans un rapport de {_f(sous / hors, 1)}." if hors
               else " Sans frais de durée, le prix hors pénalités serait nul et leur "
                    "rapport ne serait pas défini (D-042).")
            + " Et la première question avant de chiffrer une journée de fin de "
            "chantier est donc : **sommes-nous en retard ?** La première version de ce "
            "module ne la posait pas et facturait partout le prix fort."),
        "_la_forme_fermee": (
            "Ce marché ne porte aucune pénalité de retard : il n'y a pas de plafond à "
            "atteindre, donc pas de jour de bascule. Le coût d'un jour est constant, et "
            "égal aux frais de durée. L'index n'est pas publié comme valant zéro — il "
            "n'est pas défini (D-042)." if sans_penalite else
            f"Le jour de bascule en jours calendaires vaut le plafond en pour-cent divisé "
            f"par la pénalité en pour-mille, soit {_f(plafond_pct)} ÷ "
            f"{_f(pour_mille, 1)} ‰ = {_f(forme_fermee)} jours. **Le montant du marché "
            "n'y figure pas** : il est au numérateur du plafond et au dénominateur de la "
            "pénalité, et il se simplifie. Deux marchés de dix millions et de dix "
            "milliards, avec les mêmes clauses, voient leur pénalité plafonner le même "
            "jour. C'est pour cela que ces deux lignes se lisent ensemble dans un CPS, "
            "et qu'aucune des deux ne veut rien dire seule."),
        "lecture": (
            f"Ce marché ne porte aucune pénalité de retard : un jour coûte "
            f"{_f(frais)} MAD de frais de durée, le premier comme le centième."
            if sans_penalite else
            f"Hors pénalités — avant le terme contractuel, ou une fois le plafond "
            f"atteint — un jour de non-réception coûte {_f(hors)} MAD. Sous pénalités, "
            f"c'est-à-dire du terme au plafond, il en coûte {_f(sous)} : "
            f"{_f(frais)} de frais de durée et {_f(penal)} de pénalités, soit "
            + (f"{_f(sous / hors, 1)} fois plus" if hors else "tout le coût")
            + ". La fenêtre de cherté dure "
            f"{_f(bascule_calendaires)} jours calendaires, soit "
            f"{_f(bascule_ouvres, 1)} jours ouvrés."),
        "_ce_que_le_changement_de_regime_veut_dire": (
            "Trois conséquences, et aucune n'est confortable. **Pour le maître "
            "d'ouvrage** : son levier a une durée de vie. Passé le plafond, la pénalité "
            "ne monte plus et il ne lui reste que la résiliation, qui le coûte aussi — "
            "un maître d'ouvrage averti n'attend pas le plafond pour agir. **Pour "
            "l'entreprise** : le calcul change de sens deux fois. Avant le terme, une "
            "journée coûte peu et rien ne pousse à se presser ; dans la fenêtre, "
            "accélérer à presque n'importe quel prix est rationnel ; après, plus rien ne "
            "pousse de nouveau. **Pour les deux** : ces deux clauses se lisent avant de "
            "signer, et elles se lisent ensemble."),
        "_ce_qui_n_est_pas_chiffre": (
            "Ni la résiliation, ni la mise en régie, ni la mobilisation d'une autre "
            "entreprise aux frais de la première, ni le préjudice d'exploitation d'une "
            "gare qui n'ouvre pas à la date annoncée — lequel peut dépasser de loin "
            "toutes les lignes ci-dessus, et ne relève pas du marché de travaux. Un coût "
            "de retard publié est une borne basse."),
    }


def courbe_du_cout(d: dict, pr: dict, cj: dict, pas: int = 10, n: int = 16) -> dict:
    """Le coût CUMULÉ d'un retard, jour après jour, À PARTIR DU TERME CONTRACTUEL.

    L'origine de l'axe n'est pas la fin des travaux : c'est le terme du marché. Avant
    lui, la courbe serait une droite de pente « frais de durée », et aucune pénalité n'y
    figurerait.
    """
    frais = cj["frais_de_duree_MAD_par_jour_ouvre"]
    penal = cj["penalites_MAD_par_jour_ouvre"]
    plafond = cj["plafond_des_penalites_MAD"]
    pts = []
    for i in range(n + 1):
        j = i * pas
        cum = frais * j + min(penal * j, plafond)
        # Trois décimales de MMAD, soit le millier de MAD : la figure n'en montre que
        # deux, mais un test qui verifie une PENTE sur dix jours a besoin que l'arrondi
        # soit petit devant la pente.
        pts.append({"x": j, "v": round(cum / 1e6, 3)})
    return {
        "points": pts,
        "unite": "MMAD, cumulé depuis le terme contractuel",
        "pente_avant_MAD_par_jour": round(frais + penal, 2),
        "pente_apres_MAD_par_jour": round(frais, 2),
        "note": (
            "Sans pénalité au marché, la courbe est une droite : le coût du retard "
            "monte des seuls frais de durée, sans cassure." if cj["sans_penalite"] else
            f"La courbe est une droite qui se casse au "
            f"{_f(cj['jour_de_bascule_ouvre'], 1)}ᵉ jour ouvré APRÈS LE TERME "
            f"CONTRACTUEL. Avant, elle monte de {_f(frais + penal)} MAD par jour ; "
            f"après, de {_f(frais)}. Ce n'est pas un adoucissement : c'est la fin d'un "
            "mécanisme, et il n'y en a pas d'autre derrière — sauf la résiliation, qui "
            "n'est pas sur ce graphique. Et à gauche de l'origine, la même courbe "
            f"monterait de {_f(frais)} MAD par jour : le chantier coûte avant d'être en "
            "retard."),
    }


# ------------------------------------------------- 2. le portage de la retenue
def portage_de_la_retenue(d: dict, pr: dict) -> dict:
    """Retenue de garantie ou caution bancaire : la durée se simplifie, et c'est tout.

    Le réflexe est de chercher la durée de la garantie pour chiffrer le portage. Elle est
    ⏸ — elle se lit dans le code et dans le CPS. Or les deux options coûtent chacune un
    taux annuel appliqué au MÊME montant pendant la MÊME durée : leur rapport ne dépend
    donc ni de la durée, ni du montant. La décision se prend sans la donnée manquante.

    D-041 s'applique ensuite : le calcul dit laquelle coûte moins cher. Il ne dit pas si
    la banque accordera la caution, ni ce que cette caution consomme de la ligne de
    crédit — qui servira peut-être, le mois suivant, à démarrer un autre chantier.
    """
    c = d["prix_unitaires_MAD"]["contrat"]
    retenue = pr["tresorerie"]["retenue_de_garantie_finale_MAD"]
    taux = c["cout_de_portage_annuel_pct"]["valeur"]
    comm = c["commission_de_caution_annuelle_pct"]["valeur"]
    tb, cb = _b(c["cout_de_portage_annuel_pct"]), _b(c["commission_de_caution_annuelle_pct"])
    par_mois = retenue * taux / 100 / 12
    caution_par_mois = retenue * comm / 100 / 12
    return {
        "retenue_immobilisee_MAD": retenue,
        "_source_de_la_retenue": "calc/sorties/prix.json — tresorerie (module D1)",
        "taux_de_portage_annuel_pct": taux,
        "commission_de_caution_annuelle_pct": comm,
        "cout_de_la_retenue_MAD_par_mois": round(par_mois, 2),
        "cout_de_la_caution_MAD_par_mois": round(caution_par_mois, 2),
        "economie_MAD_par_mois": round(par_mois - caution_par_mois, 2),
        "economie_bornes_MAD_par_mois": [
            round(retenue * (tb[0] - cb[1]) / 100 / 12, 2),
            round(retenue * (tb[1] - cb[0]) / 100 / 12, 2)],
        "rapport_des_deux_couts": round(taux / comm, 2),
        "rapport_bornes": [round(tb[0] / cb[1], 2), round(tb[1] / cb[0], 2)],
        "_la_duree_se_simplifie": (
            "Les deux coûts s'écrivent « taux × montant × durée ». Le montant est le "
            "même — la retenue — et la durée aussi : celle de la garantie. Leur RAPPORT "
            f"vaut donc {_f(taux, 1)} ÷ {_f(comm, 1)} = {_f(taux / comm, 2)}, et il ne "
            "contient ni l'un ni l'autre. On peut donc trancher sans connaître la durée "
            "de la garantie, qui est pourtant la première chose qu'on va chercher — et "
            "qui est ⏸ dans ce cours. C'est le seul endroit de ce palier où une donnée "
            "manquante se révèle inutile au lieu de bloquer."),
        "lecture": (
            f"La retenue immobilise {_f(retenue)} MAD. À "
            f"{_f(taux, 1)} % l'an, les porter coûte {_f(par_mois)} MAD par mois ; la "
            f"caution qui les remplace en coûte {_f(caution_par_mois)}. L'économie est "
            f"de {_f(par_mois - caution_par_mois)} MAD par mois de garantie, et elle "
            "reste positive sur toute l'étendue des deux fourchettes : le rapport va de "
            f"{_f(tb[0] / cb[1], 1)} à {_f(tb[1] / cb[0], 1)}."),
        "_ce_que_la_comparaison_ne_compte_pas": (
            "Trois choses, et elles vont toutes dans le même sens — celui de la "
            "caution. La retenue est prélevée sur CHAQUE situation, donc dès le premier "
            "mois du chantier : la remplacer par une caution libère aussi cette "
            "trésorerie-là, pendant toute la durée des travaux, et ce calcul ne compte "
            "que la période d'après la réception. Elle alourdit le besoin maximal que le "
            "module D1 publie. Et elle est payée par une entreprise qui a déjà engagé "
            "ses fonds. Le chiffre ci-dessus est donc une borne basse de ce que la "
            "caution rapporte."),
        "_et_ce_qui_n_est_pas_dans_le_calcul": (
            "La caution consomme la ligne de crédit de l'entreprise, et cette ligne a "
            "une limite. Celle qui garantit ce chantier-ci ne garantira pas le suivant, "
            "ni la soumission qui tombe le mois prochain. Un calcul qui montre une "
            "économie ne dit pas que la banque dira oui, ni que c'est le meilleur usage "
            "d'une signature (D-041 : un optimum calculé n'est pas une décision)."),
    }


# ------------------------------------------------- 3. les réserves
def _duree_de_levee(familles: list, h: float, capacite: float) -> dict:
    """La durée de levée d'un ensemble de réserves : le PLUS GRAND des deux délais.

    Le temps d'atelier et le délai des tiers ne s'additionnent pas et ne se remplacent
    pas : ils se recouvrent. Une famille qui attend une pièce pendant dix jours n'occupe
    personne pendant ce temps, et l'atelier travaille sur les autres. La durée d'un
    ensemble est donc le maximum de son temps d'atelier cumulé et du plus long délai de
    tiers qu'il contient — le même raisonnement qu'un chemin critique, appliqué à une
    liste de réserves.

    La première version ne connaissait que le temps d'atelier et trouvait 0,88 jour pour
    lever sept réserves bloquantes, dont un escalator en attente de pièce que l'exercice
    du même module annonçait à dix jours. Un plan fictif ne doit pas contredire ce que le
    module en dit (D-044).
    """
    heures = sum(x["nombre"] for x in familles) * h
    atelier = heures / capacite if capacite else 0.0
    delai = max([x["_delai"] for x in familles], default=0.0)
    return {"heures": round(heures, 1), "jours_d_atelier": round(atelier, 2),
            "delai_de_tiers_le_plus_long_j": delai,
            "duree_j": round(max(atelier, delai), 2),
            "commande_par": "le délai d'un tiers" if delai > atelier else "l'atelier"}


def reserves(d: dict, pr: dict, cj: dict) -> dict:
    """Deux familles, une seule bloque — et le prix de les confondre.

    Le nombre de réserves n'entre jamais dans la décision de réceptionner. C'est la
    faute la plus répandue de la fin de chantier : on compte les lignes, on trouve que
    « ça fait beaucoup », et on reporte. Trois réserves de sécurité bloquent ; quatre-
    vingt-dix réserves d'aspect ne bloquent pas.

    Et ce que le calcul ajoute à la règle : ce n'est pas le VOLUME qui fait la durée,
    c'est le DÉLAI LE PLUS LONG. Les sept réserves bloquantes de ce chantier
    représentent moins d'une journée d'atelier et dix jours de calendrier, parce que l'une
    d'elles attend une pièce.
    """
    r = d["reception"]["reserves"]
    h = r["heures_par_levee_h"]["valeur"]
    hb = _b(r["heures_par_levee_h"])
    eff = r["effectif_de_levee"]
    taux = d["prix_unitaires_MAD"]["ressources"]["main_oeuvre_MAD_h"]["compagnon_qualifie"]["valeur"]
    heures_jour = d["prix_unitaires_MAD"]["ressources"]["heures_par_jour"]
    capacite = eff * heures_jour                    # heures-homme par jour ouvré

    lignes = []
    for f in r["familles"]:
        dt = f["delai_de_tiers_j"]
        v = dt["valeur"] if isinstance(dt, dict) else dt
        bdt = _b(dt) if isinstance(dt, dict) else (v, v)
        lignes.append({**f, "_delai": v,
                       "delai_de_tiers_j": v,
                       "delai_de_tiers_bornes_j": list(bdt),
                       "heures": round(f["nombre"] * h, 1),
                       "jours_d_atelier": round(f["nombre"] * h / capacite, 2),
                       "cout_MAD": round(f["nombre"] * h * taux, 2)})
    bloq = [x for x in lignes if x["empeche_l_usage"]]
    n_tot = sum(x["nombre"] for x in lignes)
    n_bloq = sum(x["nombre"] for x in bloq)
    h_tot = sum(x["heures"] for x in lignes)

    d_bloq = _duree_de_levee(bloq, h, capacite)
    d_tout = _duree_de_levee(lignes, h, capacite)
    jours_en_plus = max(0.0, d_tout["duree_j"] - d_bloq["duree_j"])
    sous = jours_en_plus * cj["cout_sous_penalites_MAD_par_jour_ouvre"]
    hors = jours_en_plus * cj["cout_hors_penalites_MAD_par_jour_ouvre"]
    # Bornes : les heures par levée et les délais de tiers bougent ensemble, et le
    # maximum des deux n'est pas monotone terme à terme — on recalcule donc la durée
    # ENTIÈRE à chaque borne au lieu de borner le résultat.
    bornes = []
    for i in (0, 1):
        li = [{**x, "_delai": x["delai_de_tiers_bornes_j"][i]} for x in lignes]
        bi = [x for x in li if x["empeche_l_usage"]]
        bornes.append(max(0.0, _duree_de_levee(li, hb[i], capacite)["duree_j"]
                          - _duree_de_levee(bi, hb[i], capacite)["duree_j"]))
    for x in lignes:
        x.pop("_delai", None)
    return {
        "lignes": lignes,
        "nb_total": n_tot,
        "nb_bloquantes": n_bloq,
        "part_bloquante_pct": round(n_bloq / n_tot * 100, 1),
        "heures_totales": round(h_tot, 1),
        "heures_bornes": [round(n_tot * hb[0], 1), round(n_tot * hb[1], 1)],
        "capacite_h_homme_par_jour": capacite,
        "cout_de_levee_MAD": round(h_tot * taux, 2),
        "taux_horaire_MAD": taux,
        "effectif_de_levee": eff,
        "levee_des_bloquantes": d_bloq,
        "levee_de_toutes": d_tout,
        "jours_de_non_reception_en_plus": round(jours_en_plus, 2),
        "jours_en_plus_bornes": [round(min(bornes), 2), round(max(bornes), 2)],
        "cout_de_la_confusion_sous_penalites_MAD": round(sous, 2),
        "cout_de_la_confusion_hors_penalites_MAD": round(hors, 2),
        "cout_de_la_confusion_bornes_MAD": [
            round(min(bornes) * cj["cout_hors_penalites_MAD_par_jour_ouvre"], 2),
            round(max(bornes) * cj["cout_sous_penalites_MAD_par_jour_ouvre"], 2)],
        "la_regle": r["_la_regle"],
        "le_delai_de_tiers": r["_delai_de_tiers"],
        "lecture": (
            f"{n_tot} réserves, dont {n_bloq} seulement empêchent l'usage ou mettent en "
            f"cause la sécurité — {_f(n_bloq / n_tot * 100, 1)} %. Lever les "
            f"{n_bloq} bloquantes demande {_f(d_bloq['heures'])} heures-homme, soit "
            f"{_f(d_bloq['jours_d_atelier'], 2)} jour d'atelier — mais "
            f"{_f(d_bloq['duree_j'], 1)} jours de calendrier, parce que l'une d'elles "
            f"attend une pièce. Les lever TOUTES demande {_f(d_tout['duree_j'], 1)} "
            f"jours : {_f(jours_en_plus, 1)} de plus, et c'est l'atelier qui commande "
            "cette fois."),
        "_ce_qui_commande_la_duree": (
            f"La levée des bloquantes est commandée par {d_bloq['commande_par']} "
            f"({_f(d_bloq['delai_de_tiers_le_plus_long_j'])} jours d'attente contre "
            f"{_f(d_bloq['jours_d_atelier'], 2)} jour de travail) ; celle de toutes les "
            f"réserves par {d_tout['commande_par']} "
            f"({_f(d_tout['jours_d_atelier'], 1)} jours de travail contre "
            f"{_f(d_tout['delai_de_tiers_le_plus_long_j'])} jours d'attente). Le "
            "basculement entre les deux régimes est le seul enseignement robuste de ce "
            "tableau : mettre plus de monde ne sert à rien tant qu'on attend une pièce, "
            "et ne sert qu'à cela une fois la pièce arrivée."),
        "_le_prix_de_la_confusion": (
            f"Exiger la levée des {n_tot - n_bloq} réserves non bloquantes avant de "
            f"réceptionner repousse la réception de {_f(jours_en_plus, 1)} jours "
            f"ouvrés — et non de {_f(d_tout['duree_j'], 1)}, parce que les bloquantes "
            f"prennent déjà {_f(d_bloq['duree_j'], 1)} jours qu'on aurait attendus de "
            f"toute façon. Ces {_f(jours_en_plus, 1)} jours coûtent {_f(hors)} MAD si "
            f"le chantier est dans son délai, et {_f(sous)} MAD s'il est en retard et "
            "sous pénalités. La question n'est donc jamais « y a-t-il des réserves ? » "
            "mais « laquelle empêche l'usage ? » — et, juste après, « laquelle attend "
            "quelque chose ? »."),
        "_et_dans_l_autre_sens": (
            "Le symétrique est pire, et il est moins visible : réceptionner avec une "
            "réserve de sécurité classée « aspect » parce qu'elle était seule de sa "
            "famille dans une longue liste. Un garde-corps non conforme ne devient pas "
            "une finition parce qu'il est noyé dans une liste. C'est pourquoi le "
            "classement se fait ligne à ligne, par la seule question qui décide, et non "
            "par un comptage."),
    }


# ------------------------------------------------- 4. le DOE
def doe(d: dict, pr: dict, po: dict) -> dict:
    """Le DOE se constitue pendant le chantier. Reconstitué, il coûte quatre fois plus.

    Et il ne coûte pas que des heures : il bloque le DÉCOMPTE DÉFINITIF, c'est-à-dire le
    solde des travaux — pas la retenue de garantie. La distinction a coûté un bloquant à
    la première version de ce module, qui portait le retard du DOE sur la retenue : la
    retenue est immobilisée par la clause de garantie, que le dossier soit remis ou non,
    et son portage n'est donc pas imputable au DOE. Ce que le DOE retarde, c'est le
    paiement du solde.
    """
    o = d["reception"]["doe"]
    taux_cadre = d["prix_unitaires_MAD"]["ressources"]["main_oeuvre_MAD_h"]["controleur"]["valeur"]
    fil, rec = o["heures_au_fil_de_l_eau"]["valeur"], o["heures_reconstitue"]["valeur"]
    fb, rb = _b(o["heures_au_fil_de_l_eau"]), _b(o["heures_reconstitue"])
    jours, jb = o["retard_du_solde_j"]["valeur"], _b(o["retard_du_solde_j"])
    part, pb = o["part_du_marche_au_decompte_definitif_pct"]["valeur"], _b(
        o["part_du_marche_au_decompte_definitif_pct"])
    marche = pr["bordereau"]["prix_de_vente_MAD"]
    solde = marche * part / 100
    taux_portage = po["taux_de_portage_annuel_pct"]
    tb = _b(d["prix_unitaires_MAD"]["contrat"]["cout_de_portage_annuel_pct"])
    base = d["prix_unitaires_MAD"]["contrat"]["base_de_calcul_des_interets_j"]
    portage = solde * taux_portage / 100 * jours / base
    sur_h = (rec - fil) * taux_cadre
    total = sur_h + portage
    bornes = [round(max(0.0, (rb[0] - fb[1]) * taux_cadre)
                    + marche * pb[0] / 100 * tb[0] / 100 * jb[0] / base, 2),
              round((rb[1] - fb[0]) * taux_cadre
                    + marche * pb[1] / 100 * tb[1] / 100 * jb[1] / base, 2)]
    return {
        "heures_au_fil_de_l_eau": fil,
        "heures_reconstitue": rec,
        "rapport_des_heures": round(rec / fil, 1),
        "rapport_bornes": [round(rb[0] / fb[1], 1), round(rb[1] / fb[0], 1)],
        "taux_horaire_de_cadre_MAD": taux_cadre,
        "cout_au_fil_de_l_eau_MAD": round(fil * taux_cadre, 2),
        "cout_reconstitue_MAD": round(rec * taux_cadre, 2),
        "surcout_en_heures_MAD": round(sur_h, 2),
        "surcout_en_heures_bornes_MAD": [round(max(0.0, (rb[0] - fb[1]) * taux_cadre), 2),
                                         round((rb[1] - fb[0]) * taux_cadre, 2)],
        "part_du_marche_au_decompte_definitif_pct": part,
        "solde_bloque_MAD": round(solde, 2),
        "retard_du_solde_j": jours,
        "base_de_calcul_des_interets_j": base,
        "cout_de_portage_MAD": round(portage, 2),
        "cout_de_portage_bornes_MAD": [
            round(marche * pb[0] / 100 * tb[0] / 100 * jb[0] / base, 2),
            round(marche * pb[1] / 100 * tb[1] / 100 * jb[1] / base, 2)],
        "cout_total_du_retard_de_DOE_MAD": round(total, 2),
        "cout_total_bornes_MAD": bornes,
        "part_du_portage_dans_le_surcout_pct": round(portage / total * 100, 1),
        "lecture": (
            f"Tenu au fil de l'eau, le dossier demande {_f(fil)} heures de cadre, soit "
            f"{_f(fil * taux_cadre)} MAD. Reconstitué après coup, il en demande "
            f"{_f(rec)} — {_f(rec / fil, 1)} fois plus — et pendant qu'on le "
            f"reconstitue, il bloque le décompte définitif. Porter le solde, "
            f"{_f(solde)} MAD, pendant {_f(jours)} jours au taux de "
            f"{_f(taux_portage, 1)} % l'an coûte {_f(portage)} MAD de plus. Le retard "
            f"de DOE coûte donc {_f(total)} MAD, dont "
            f"{_f(portage / total * 100)} % qui ne sont ni du travail ni une pénalité : "
            "seulement de l'argent dû qui attend."),
        "_bornes": (
            f"Entre {_f(bornes[0])} et {_f(bornes[1])} MAD selon les bornes des quatre "
            "hypothèses. La borne basse du surcoût en HEURES est nulle, et il faut le "
            "dire : rien n'interdit qu'un dossier tenu négligemment coûte autant qu'un "
            "dossier reconstitué soigneusement. Ce qui ne s'annule pas, c'est le "
            "portage du solde — il court dès que le dossier est en retard, quel que "
            "soit le soin qu'on y a mis avant."),
        "_pourquoi_c_est_sous_estime": (
            "Parce que le DOE ne coûte rien tant qu'on ne le fait pas. C'est une tâche "
            "sans cadence, sans point d'arrêt, dont personne ne constate l'absence avant "
            "la fin — et qui, à ce moment-là, est sur le chemin critique de l'argent. "
            "Les quatre cinquièmes de son surcoût se décident pendant le chantier, dans "
            "des moments où il ne coûtait rien de demander le document : quand le "
            "sous-traitant est encore là, quand la paroi est encore ouverte, quand "
            "celui qui a posé se souvient de ce qu'il a posé."),
        "_ce_que_le_solde_contient": (
            f"Le solde bloqué est posé à {_f(part, 1)} % du montant du marché : dernière "
            "situation, révisions de prix non encore réglées, travaux supplémentaires "
            "acceptés. Ce n'est PAS la retenue de garantie, que la clause de garantie "
            "immobilise de toute façon — une première version de ce module imputait au "
            "DOE le portage de la retenue, c'est-à-dire le coût d'une clause qui n'a "
            "rien à voir avec lui. Les deux montants cohabitent à la fin d'un chantier, "
            "et ils ne se confondent pas."),
        "_la_base_est_une_clause": (
            f"Les intérêts sont calculés sur une année de {base} jours. Ce n'est pas une "
            "constante : la base 360, dite bancaire, est tout aussi courante, et elle "
            f"donne {_f(solde * taux_portage / 100 * jours / 360)} MAD au lieu de "
            f"{_f(portage)} — 1,4 % d'écart sur le même calcul. Cela se lit dans la "
            "convention de crédit, cela ne se suppose pas, et cela ne se découvre pas en "
            "relisant une formule : ici, c'est la vérification dimensionnelle qui l'a "
            "signalé, en comparant le résultat à une année de 365,25 jours."),
        "_le_critere_pratique": o["_ce_qu_il_doit_contenir"],
    }


# ------------------------------------------------- 5. les opérations préalables
def _duree(e: dict) -> tuple:
    """La durée d'une étape : décision (un nombre) ou hypothèse ({valeur, fourchette})."""
    v = e["duree_j"]
    if isinstance(v, dict):
        return float(v["valeur"]), _b(v)
    return float(v), (float(v), float(v))


def operations_prealables(d: dict) -> dict:
    """La séquence, sa durée — et à qui chacune de ses durées appartient.

    Deux natures de durée cohabitent, et les confondre était une faute : ce que
    l'entreprise tient est une DÉCISION d'organisation, sans fourchette ; ce qui
    appartient à un tiers — la maîtrise d'œuvre qui visite, l'exploitant qui essaie, le
    maître d'ouvrage qui décide — est une HYPOTHÈSE, et elle porte sa fourchette. On ne
    décide pas une durée qui appartient à quelqu'un d'autre.
    """
    o = d["reception"]["operations_prealables"]
    cumul, lignes, bas, haut = 0.0, [], 0.0, 0.0
    for e in o["etapes"]:
        v, b = _duree(e)
        cumul += v
        bas += b[0]
        haut += b[1]
        lignes.append({**e, "duree_j": v, "duree_bornes_j": list(b),
                       "fin_j": round(cumul, 1)})
    tiers = [x for x in lignes if not x["tenue_par_l_entreprise"]]
    part_tiers = sum(x["duree_j"] for x in tiers) / cumul * 100
    return {
        "etapes": lignes,
        "nb_etapes": len(lignes),
        "unite": o["unite"],
        "duree_totale_j": round(cumul, 1),
        "duree_bornes_j": [round(bas, 1), round(haut, 1)],
        "duree_tenue_par_des_tiers_j": round(sum(x["duree_j"] for x in tiers), 1),
        "part_tenue_par_des_tiers_pct": round(part_tiers, 1),
        "note": (
            f"{len(lignes)} étapes, {_f(cumul)} {o['unite']} entre l'avis de fin de "
            f"travaux et la décision du maître d'ouvrage — si tout va bien, et si "
            f"personne n'est absent. Les bornes vont de {_f(bas)} à {_f(haut)} "
            f"{o['unite']}, et l'étendue vient presque entièrement des étapes que "
            "l'entreprise ne tient pas. Ce n'est pas une formalité administrative : "
            "c'est une tâche du planning, avec une durée, qui doit y figurer. Un "
            "planning qui finit au dernier coup de peinture ment de deux mois ouvrés."),
        "_a_qui_appartiennent_ces_jours": (
            f"{_f(sum(x['duree_j'] for x in tiers))} des {_f(cumul)} {o['unite']} — "
            f"{_f(part_tiers)} % — sont tenus par des tiers : la maîtrise d'œuvre qui "
            "visite, l'exploitant qui met en service, le maître d'ouvrage qui décide. "
            "L'entreprise ne les raccourcit pas en mettant plus de monde ; elle ne les "
            "raccourcit qu'en les préparant plus tôt. C'est pour cela que leurs durées "
            "portent une fourchette et que les siennes n'en portent pas."),
        "_l_essai_qui_commande": (
            "La mise en service des systèmes est la plus longue des étapes, et c'est "
            "aussi la seule que l'entreprise ne maîtrise pas du tout : c'est "
            "l'exploitant ferroviaire qui la conduit. Elle se prépare donc comme une "
            "consignation — demandée longtemps à l'avance, avec ses prérequis vérifiés "
            "un par un. Un essai de système reporté ne se rattrape pas en y mettant plus "
            "de monde, et sa borne haute est près du triple de sa valeur retenue."),
    }


# ------------------------------------------------- 6. ce que le planning en prévoit
def confrontation_au_planning(d: dict, pr: dict, cj: dict, op: dict) -> dict:
    """Le planning prévoit-il la réception qu'il annonce ? Tâche par tâche, et mesuré.

    La première version retirait du besoin la seule étape « mise en service », alors que
    la tâche du planning qui la porte s'appelle « ESSAIS ET mise en service » : les dix
    jours d'essais de fonctionnement étaient comptés comme absents d'une tâche qui les
    nomme. Le module affirmait pourtant, test à l'appui, qu'il n'y avait pas de double
    compte. La correction ne consiste pas à changer un nombre : elle consiste à ÉCRIRE
    dans `data/`, étape par étape, quelle tâche du planning la porte — et à comparer
    ensuite tâche par tâche.

    Ce que cette comparaison est, et n'est pas : les durées des deux côtés sont des
    décisions de ce cours, posées à deux moments différents. D2 a posé « réception =
    dix jours » avant que ce module n'existe et sans la décomposer. Ce n'est donc pas la
    découverte d'une erreur dans un planning réel — c'est la confrontation de deux
    chiffres du cours (D-055), et elle vaut par son mécanisme.
    """
    import copy
    sys.path.insert(0, str(RACINE / "calc"))
    import planification as pln                                          # noqa: E402
    pl = json.loads((RACINE / "calc" / "sorties" / "planification.json")
                    .read_text(encoding="utf-8"))

    par_tache: dict = {}
    for e in op["etapes"]:
        par_tache.setdefault(e["porte_par"], []).append(e)
    lignes, allongements = [], {}
    for tache, etapes in sorted(par_tache.items()):
        if tache is None:
            continue
        prevu = pl["durees"][tache]["duree_j"]
        besoin = sum(x["duree_j"] for x in etapes)
        b_bas = sum(x["duree_bornes_j"][0] for x in etapes)
        b_haut = sum(x["duree_bornes_j"][1] for x in etapes)
        ecart = besoin - prevu
        allongements[tache] = max(0.0, ecart)
        lignes.append({
            "tache": tache, "nom": pl["durees"][tache]["nom"],
            "duree_prevue_j": prevu,
            "etapes_portees": [x["etape"] for x in etapes],
            "besoin_j": round(besoin, 1),
            "besoin_bornes_j": [round(b_bas, 1), round(b_haut, 1)],
            "ecart_j": round(ecart, 1),
            "ecart_bornes_j": [round(b_bas - prevu, 1), round(b_haut - prevu, 1)],
        })

    tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json")
                    .read_text(encoding="utf-8"))
    q = pln.quantites_chantier(d, d["planning"])
    t0 = pln.durees_chantier(d, d["planning"], q,
                             tv["planning_plancher"]["duree_totale_j"])
    ref = pln.voie_A_parcours(pln.planning_avec_fenetres(d, t0)["taches"])["duree"]

    def mesure(allonge: dict) -> float:
        t1 = copy.deepcopy(t0)
        for k, v in allonge.items():
            t1[k]["duree_j"] = t1[k]["duree_j"] + v
        fin_ = pln.voie_A_parcours(pln.planning_avec_fenetres(d, t1)["taches"])["duree"]
        return round(fin_ - ref, 2)

    decalage = mesure(allongements)
    # Bornes MESURÉES, pas déduites : le réseau est rejoué aux deux bornes du besoin.
    bas = mesure({x["tache"]: max(0.0, x["ecart_bornes_j"][0]) for x in lignes})
    haut = mesure({x["tache"]: max(0.0, x["ecart_bornes_j"][1]) for x in lignes})
    ecart_total = sum(x["ecart_j"] for x in lignes)
    return {
        "lignes": lignes,
        "ecart_total_j": round(ecart_total, 1),
        "decalage_mesure_de_la_fin_j": decalage,
        "decalage_bornes_j": [min(bas, haut), max(bas, haut)],
        "duree_de_reference_j": round(ref, 2),
        "cout_hors_penalites_MAD": round(
            decalage * cj["cout_hors_penalites_MAD_par_jour_ouvre"], 2),
        "cout_sous_penalites_MAD": round(
            decalage * cj["cout_sous_penalites_MAD_par_jour_ouvre"], 2),
        "lecture": (
            "Le planning porte deux tâches de fin, et la séquence du § S3a dit ce que "
            "chacune doit contenir. "
            + " ".join(
                f"« {x['nom']} » prévoit {_f(x['duree_prevue_j'])} jours pour "
                f"{len(x['etapes_portees'])} étape(s) qui en demandent "
                f"{_f(x['besoin_j'])}, soit {_f(x['ecart_j'])} de trop."
                for x in lignes)
            + f" Le réseau rejoué avec les deux allongements décale la fin de "
              f"{_f(decalage, 1)} jours ouvrés — les deux tâches sont sur le chemin "
              f"critique, rien ne les absorbe. Au prix d'un jour de non-réception, cela "
              f"vaut {_f(decalage * cj['cout_hors_penalites_MAD_par_jour_ouvre'])} MAD "
              f"si le chantier est dans son délai, et "
              f"{_f(decalage * cj['cout_sous_penalites_MAD_par_jour_ouvre'])} s'il est "
              "déjà sous pénalités."),
        "_le_double_compte_evite": (
            "Chaque étape déclare dans `data/` la tâche du planning qui la porte, et "
            "aucune n'en déclare deux. C'est la correction d'un bloquant : la première "
            "version ne retirait du besoin que l'étape « mise en service », alors que la "
            "tâche qui la porte s'appelle « essais ET mise en service » — les dix jours "
            "d'essais de fonctionnement étaient comptés comme absents d'une tâche qui "
            "les nomme. L'erreur ne se voyait pas dans le total, qui était le même ; "
            "elle se voyait dans l'ATTRIBUTION, et c'est l'attribution qui dit quoi "
            "corriger."),
        "_ce_que_cette_comparaison_est": (
            "Deux chiffres de ce cours, posés à deux moments différents, et non la "
            "découverte d'une erreur dans un planning réel : le module D2 a posé "
            "« réception = dix jours » avant que ce module n'existe, sans la "
            "décomposer. Ce qui se généralise n'est donc pas l'écart — il dépend "
            "entièrement des durées posées ici — mais le MÉCANISME : une tâche "
            "« Réception » non décomposée est presque toujours trop courte, parce qu'on "
            "y pense comme à une signature alors que c'est une séquence."),
        "_quoi_en_faire": (
            f"Décomposer les lignes de fin du planning en leurs étapes, chacune avec son "
            f"responsable, comme on décompose un cycle de gros œuvre. C'est la seule "
            f"façon de voir que {_f(op['part_tenue_par_des_tiers_pct'])} % de leur durée "
            "n'appartient pas à l'entreprise — et donc de la préparer au lieu de la "
            "subir. Un planning qui finit sur une tâche « Réception » de dix jours sans "
            "détail annonce une date qu'il n'a pas vérifiée."),
    }


# ------------------------------------------------- figures
def figures(cj: dict, co: dict, rs: dict, dd: dict) -> dict:
    return {
        "cout_cumule": co["points"],
        # Le marqueur de la figure 1 est une DONNEE, pas une annotation ecrite a la main :
        # il bouge avec les clauses du marche, comme la courbe qu'il marque.
        "marqueur_bascule": (
            {"x": cj["jour_de_bascule_ouvre"], "libelle": "plafond atteint"}
            if cj["jour_de_bascule_ouvre"] is not None
            else {"x": 0, "libelle": ""}),
        # `bloque` : la figure doit porter la qualification dans sa FORME, pas seulement
        # dans son libelle. Une figure dont le propos est « la longueur n'entre pas dans
        # la decision » et qui ne distingue les bloquantes que par un mot ajoute met la
        # longueur au premier plan et la qualification en note.
        "reserves": [{"libelle": x["famille"], "valeur": x["nombre"],
                      "alerte": bool(x["empeche_l_usage"])} for x in rs["lignes"]],
        # La cascade part du SURCOUT, pas du cout de reference : son titre dit « d'ou
        # vient le surcout », et son total doit donc etre le surcout publie par le
        # tableau de la meme section. La version precedente y ajoutait la barre de
        # reference et affichait un total que le tableau contredisait.
        "doe": [
            {"libelle": "Heures en plus", "montant": round(dd["surcout_en_heures_MAD"] / 1000)},
            {"libelle": "Solde bloqué", "montant": round(dd["cout_de_portage_MAD"] / 1000)},
            {"libelle": "Surcoût total", "montant": round(
                dd["cout_total_du_retard_de_DOE_MAD"] / 1000), "type": "total"},
        ],
    }


# ------------------------------------------------- assemblage
def tout_calculer(d: dict) -> dict:
    pr = json.loads((RACINE / "calc" / "sorties" / "prix.json").read_text(encoding="utf-8"))
    cj = cout_d_un_jour(d, pr)
    co = courbe_du_cout(d, pr, cj)
    po = portage_de_la_retenue(d, pr)
    rs = reserves(d, pr, cj)
    dd = doe(d, pr, po)
    op = operations_prealables(d)
    cf = confrontation_au_planning(d, pr, cj, op)
    return {
        "cout_d_un_jour": cj,
        "courbe_du_cout": co,
        "portage": po,
        "reserves": rs,
        "doe": dd,
        "operations_prealables": op,
        "confrontation_au_planning": cf,
        "figures": figures(cj, co, rs, dd),
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    r = tout_calculer(d)
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "reception.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    c, p, s, o = r["cout_d_un_jour"], r["portage"], r["reserves"], r["doe"]
    print(f"un jour : {c['cout_hors_penalites_MAD_par_jour_ouvre']:.0f} MAD hors "
          f"penalites, {c['cout_sous_penalites_MAD_par_jour_ouvre']:.0f} sous "
          f"{c['cout_sous_penalites_bornes_MAD']} (x{c['rapport_des_deux_regimes']}), "
          f"fenetre de {c['jour_de_bascule_calendaire']} j calendaires "
          f"{c['jour_de_bascule_bornes_calendaires']}")
    print(f"portage : retenue {p['retenue_immobilisee_MAD']:.0f} MAD, "
          f"{p['cout_de_la_retenue_MAD_par_mois']:.0f} MAD/mois contre "
          f"{p['cout_de_la_caution_MAD_par_mois']:.0f} — rapport {p['rapport_des_deux_couts']}")
    print(f"reserves : {s['nb_total']} dont {s['nb_bloquantes']} bloquantes ; "
          f"bloquantes {s['levee_des_bloquantes']['duree_j']} j "
          f"({s['levee_des_bloquantes']['commande_par']}), toutes "
          f"{s['levee_de_toutes']['duree_j']} j ; la confusion coute "
          f"{s['cout_de_la_confusion_hors_penalites_MAD']:.0f} a "
          f"{s['cout_de_la_confusion_sous_penalites_MAD']:.0f} MAD")
    print(f"DOE : solde bloque {o['solde_bloque_MAD']:.0f}, surcout "
          f"{o['cout_total_du_retard_de_DOE_MAD']:.0f} MAD {o['cout_total_bornes_MAD']} "
          f"dont {o['part_du_portage_dans_le_surcout_pct']} % de portage")
    cf = r["confrontation_au_planning"]
    op = r["operations_prealables"]
    print(f"OPR : {op['duree_totale_j']} j {op['duree_bornes_j']} dont "
          f"{op['part_tenue_par_des_tiers_pct']} % tenus par des tiers")
    for x in cf["lignes"]:
        print(f"  {x['tache']} : {x['duree_prevue_j']:.0f} j prevus pour "
              f"{x['besoin_j']:.0f} demandes — ecart {x['ecart_j']:.0f} j "
              f"{x['ecart_bornes_j']}")
    print(f"  fin decalee de {cf['decalage_mesure_de_la_fin_j']} j "
          f"{cf['decalage_bornes_j']}, {cf['cout_hors_penalites_MAD']:.0f} a "
          f"{cf['cout_sous_penalites_MAD']:.0f} MAD")
