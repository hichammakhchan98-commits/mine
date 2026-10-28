"""Réception, DOE, garanties : la fin de chantier, et ce qu'elle coûte par jour (REC).

Dernier module du palier 1. Il ferme le déroulé du § 10.2, et il a un cœur calculable que
les modules précédents ont préparé sans le savoir : D1 publie les frais de durée et les
pénalités, D2 publie la date, C7 publie le coût d'une non-conformité. REC n'en recalcule
aucun — il les lit, et il en tire ce qu'aucun d'eux ne pouvait voir.

Quatre résultats, tous non normatifs :

1. **Un jour de non-réception a un prix, et ce prix CHANGE DE RÉGIME.** Tant que les
   pénalités courent, il vaut les frais de durée plus la pénalité ; une fois le plafond
   atteint, il ne vaut plus que les frais de durée. Le rapport est de huit. Le jour de
   bascule ne dépend pas du montant du marché : c'est le plafond en pour-cent divisé par
   la pénalité en pour-mille, et rien d'autre.
2. **L'arbitrage entre retenue de garantie et caution bancaire ne dépend pas de la durée
   de la garantie** — qui est pourtant la première chose qu'on cherche, et qui est ⏸.
   Les deux coûts sont proportionnels à la même durée : elle se simplifie, et la décision
   se réduit à comparer deux taux annuels.
3. **Les réserves se classent en deux familles, et une seule bloque.** Confondre les deux
   coûte un jour de non-réception par jour d'attente — et ce jour-là, on le connaît.
4. **Le DOE se constitue pendant le chantier.** Reconstitué après coup, il coûte quatre
   fois plus d'heures de cadre, et il immobilise le décompte définitif pendant qu'on le
   reconstitue.

Ce que le module ne dit pas, et ne dira pas tant que les documents manquent : les durées
des garanties, le délai de levée des réserves, les conditions d'une réception tacite, le
contenu obligatoire du DOE. Il donne le mécanisme et sa conséquence financière.
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


# ------------------------------------------------- 1. le prix d'un jour de non-réception
def cout_d_un_jour(d: dict, pr: dict) -> dict:
    """Ce que coûte une journée de plus avant la réception — et le jour où ça change.

    Aucun des deux termes n'est recalculé ici : les frais de durée et la pénalité
    journalière sont LUS dans la sortie du module D1 (D-039, une grandeur, un seul
    endroit). D1 les publie pour trois retards donnés ; ce qu'il ne cherche pas, et que
    ce module trouve, c'est le jour où le plafond est atteint.

    Le piège de calendrier vient de D1 et il est conservé tel quel : les pénalités se
    comptent en jours CALENDAIRES et les frais de durée en jours OUVRÉS. Un jour ouvré de
    retard porte donc 1,4 jour de pénalité.
    """
    c = d["prix_unitaires_MAD"]["contrat"]
    r1 = pr["cout_du_retard"]["1"]
    conv = pr["bordereau"]["frais_de_duree"]["conversion"]["calendaires_par_jour_ouvre"]
    frais = r1["frais_de_duree_MAD"]
    penal = r1["penalites_MAD"]
    plafond = r1["penalites_plafond_MAD"]
    marche = pr["bordereau"]["prix_de_vente_MAD"]

    # Un marche SANS penalite de retard existe — rare, et il faut le lire dans le CPS
    # plutot que le supposer. Il n'y a alors pas de bascule : le cout d'un jour est
    # constant. Publier « 0 » serait faux, et diviser par zero serait pire : l'index
    # n'est pas defini, et c'est ce qui se publie (D-042).
    sans_penalite = penal <= 0
    bascule_ouvres = None if sans_penalite else plafond / penal
    bascule_calendaires = None if sans_penalite else bascule_ouvres * conv
    avant, apres = frais + penal, frais
    # Forme fermée : le jour de bascule en jours CALENDAIRES ne dépend que de deux
    # clauses du marché, et pas du tout de son montant. C'est ce qui en fait une règle
    # de lecture d'un CPS plutôt qu'un résultat de ce chantier-ci.
    plafond_pct = c["penalite_plafond_pct"]["valeur"]
    pour_mille = c["penalite_retard_pour_mille_par_j"]["valeur"]
    forme_fermee = None if sans_penalite else plafond_pct * 10.0 / pour_mille
    bornes = []
    if not sans_penalite:
        for pf, pm in ((_b(c["penalite_plafond_pct"])[0],
                        _b(c["penalite_retard_pour_mille_par_j"])[1]),
                       (_b(c["penalite_plafond_pct"])[1],
                        _b(c["penalite_retard_pour_mille_par_j"])[0])):
            bornes.append(round(pf * 10.0 / pm, 1))
    return {
        "marche_MAD": marche,
        "frais_de_duree_MAD_par_jour_ouvre": frais,
        "penalites_MAD_par_jour_ouvre": penal,
        "_source": "calc/sorties/prix.json — cout_du_retard (module D1), jamais recalculé ici",
        "plafond_des_penalites_MAD": plafond,
        "cout_avant_le_plafond_MAD_par_jour_ouvre": round(avant, 2),
        "cout_apres_le_plafond_MAD_par_jour_ouvre": round(apres, 2),
        # Sans frais de duree, le cout d'un jour tombe a zero une fois le plafond
        # atteint : le RAPPORT des deux regimes n'est alors pas defini, et c'est ce qui
        # se publie. Ce cas a ete trouve par un cas degenere de l'etalonnage, pas par
        # une relecture.
        "rapport_des_deux_regimes": round(avant / apres, 1) if apres else None,
        "sans_penalite": sans_penalite,
        "jour_de_bascule_ouvre": None if sans_penalite else round(bascule_ouvres, 1),
        "jour_de_bascule_calendaire": (None if sans_penalite
                                       else round(bascule_calendaires, 1)),
        "jour_de_bascule_bornes_calendaires": bornes or None,
        "forme_fermee_calendaire": None if sans_penalite else round(forme_fermee, 1),
        "_la_forme_fermee": (
            "Ce marche ne porte aucune penalite de retard : il n'y a pas de plafond a "
            "atteindre, donc pas de jour de bascule. Le cout d'un jour est constant, et "
            "egal aux frais de duree. L'index n'est pas publie comme valant zero — il "
            "n'est pas defini (D-042)." if sans_penalite else
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
            f"Avant le plafond, un jour ouvré de retard coûte {_f(avant)} MAD : "
            f"{_f(frais)} de frais de durée et {_f(penal)} de pénalités. Après, il ne "
            f"coûte plus que les {_f(frais)} MAD de frais de durée"
            + (f" — {_f(avant / apres, 1)} fois moins" if apres else
               ", et sans frais de durée il ne coûterait plus rien du tout")
            + f". La bascule tombe au "
            f"{_f(bascule_calendaires)}ᵉ jour calendaire de retard, soit le "
            f"{_f(bascule_ouvres, 1)}ᵉ jour ouvré."),
        "_ce_que_le_changement_de_regime_veut_dire": (
            "Trois conséquences, et aucune n'est confortable. **Pour le maître "
            "d'ouvrage** : son levier s'épuise. Passé le plafond, la pénalité ne monte "
            "plus et il ne lui reste que la résiliation, qui le coûte aussi — un maître "
            "d'ouvrage averti n'attend pas le plafond pour agir. **Pour l'entreprise** : "
            "le calcul change de sens. Avant le plafond, accélérer à presque n'importe "
            "quel prix est rationnel ; après, non. Ce n'est pas un conseil, c'est ce que "
            "le contrat dit, et il faut le savoir pour ne pas être surpris par la "
            "logique d'en face. **Pour les deux** : cette clause se lit avant de signer, "
            "pas au quatre-vingt-dixième jour."),
        "_ce_qui_n_est_pas_chiffre": (
            "Ni la résiliation, ni la mise en régie, ni la mobilisation d'une autre "
            "entreprise aux frais de la première, ni le préjudice d'exploitation d'une "
            "gare qui n'ouvre pas à la date annoncée — lequel peut dépasser de loin "
            "toutes les lignes ci-dessus, et ne relève pas du marché de travaux. Un coût "
            "de retard publié est une borne basse."),
    }


def courbe_du_cout(d: dict, pr: dict, cj: dict, pas: int = 10, n: int = 16) -> dict:
    """Le coût CUMULÉ du retard, jour après jour : une droite qui se casse."""
    frais = cj["frais_de_duree_MAD_par_jour_ouvre"]
    penal = cj["penalites_MAD_par_jour_ouvre"]
    plafond = cj["plafond_des_penalites_MAD"]
    pts = []
    for i in range(n + 1):
        j = i * pas
        cum = frais * j + min(penal * j, plafond)
        # Trois decimales de MMAD, soit le millier de MAD : la figure n'en montre que
        # deux, mais un test qui verifie une PENTE sur dix jours a besoin que l'arrondi
        # soit petit devant la pente. Publier au centieme de MMAD rendait la pente
        # incertaine de mille dirhams par jour.
        pts.append({"x": j, "v": round(cum / 1e6, 3)})
    return {
        "points": pts,
        "unite": "MMAD, cumulé",
        "pente_avant_MAD_par_jour": round(frais + penal, 2),
        "pente_apres_MAD_par_jour": round(frais, 2),
        "note": (
            "Sans pénalité au marché, la courbe est une droite : le coût du retard "
            "monte des seuls frais de durée, sans cassure." if cj["sans_penalite"] else
            f"La courbe est une droite qui se casse au "
            f"{_f(cj['jour_de_bascule_ouvre'], 1)}ᵉ jour ouvré. Avant, elle monte de "
            f"{_f(frais + penal)} MAD par jour ; après, de {_f(frais)}. Ce n'est pas un "
            "adoucissement : c'est la fin d'un mécanisme, et il n'y en a pas d'autre "
            "derrière — sauf la résiliation, qui n'est pas sur ce graphique."),
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
def reserves(d: dict, pr: dict, cj: dict) -> dict:
    """Deux familles, une seule bloque — et le prix de les confondre.

    Le nombre de réserves n'entre jamais dans la décision de réceptionner. C'est la
    faute la plus répandue de la fin de chantier : on compte les lignes, on trouve que
    « ça fait beaucoup », et on reporte. Trois réserves de sécurité bloquent ; quatre-
    vingt-dix réserves d'aspect ne bloquent pas.
    """
    r = d["reception"]["reserves"]
    h = r["heures_par_levee_h"]["valeur"]
    hb = _b(r["heures_par_levee_h"])
    eff = r["effectif_de_levee"]
    taux = d["prix_unitaires_MAD"]["ressources"]["main_oeuvre_MAD_h"]["compagnon_qualifie"]["valeur"]
    heures_jour = d["prix_unitaires_MAD"]["ressources"]["heures_par_jour"]

    lignes = []
    for f in r["familles"]:
        lignes.append({**f,
                       "heures": round(f["nombre"] * h, 1),
                       "cout_MAD": round(f["nombre"] * h * taux, 2)})
    bloq = [x for x in lignes if x["empeche_l_usage"]]
    non_bloq = [x for x in lignes if not x["empeche_l_usage"]]
    n_tot = sum(x["nombre"] for x in lignes)
    n_bloq = sum(x["nombre"] for x in bloq)
    h_tot = sum(x["heures"] for x in lignes)
    h_non_bloq = sum(x["heures"] for x in non_bloq)
    # Durée de levée : mesurée sur les heures, l'effectif et la journée de travail du
    # cours — pas posée. C'est elle qui donne le prix de la confusion.
    jours_non_bloq = h_non_bloq / (eff * heures_jour)
    jours_bloq = sum(x["heures"] for x in bloq) / (eff * heures_jour)
    cout_confusion = jours_non_bloq * cj["cout_avant_le_plafond_MAD_par_jour_ouvre"]
    return {
        "lignes": lignes,
        "nb_total": n_tot,
        "nb_bloquantes": n_bloq,
        "part_bloquante_pct": round(n_bloq / n_tot * 100, 1),
        "heures_totales": round(h_tot, 1),
        "heures_bornes": [round(n_tot * hb[0], 1), round(n_tot * hb[1], 1)],
        "cout_de_levee_MAD": round(h_tot * taux, 2),
        "taux_horaire_MAD": taux,
        "effectif_de_levee": eff,
        "jours_de_levee_des_bloquantes": round(jours_bloq, 2),
        "jours_de_levee_des_autres": round(jours_non_bloq, 2),
        "cout_de_la_confusion_MAD": round(cout_confusion, 2),
        # Bornes sur la seule grandeur incertaine, le temps de levee : le cout du jour
        # vient de D1 et il est le meme dans les deux colonnes. Melanger les deux
        # sources de variation — les heures ET le regime de penalite — donnerait une
        # etendue plus large et moins lisible, et surtout elle ne dirait plus ce qu'elle
        # mesure.
        "cout_de_la_confusion_bornes_MAD": [
            round((n_tot - n_bloq) * hb[0] / (eff * heures_jour)
                  * cj["cout_avant_le_plafond_MAD_par_jour_ouvre"], 2),
            round((n_tot - n_bloq) * hb[1] / (eff * heures_jour)
                  * cj["cout_avant_le_plafond_MAD_par_jour_ouvre"], 2)],
        "cout_de_la_confusion_apres_le_plafond_MAD": round(
            jours_non_bloq * cj["cout_apres_le_plafond_MAD_par_jour_ouvre"], 2),
        "la_regle": r["_la_regle"],
        "lecture": (
            f"{n_tot} réserves, dont {n_bloq} seulement empêchent l'usage ou mettent en "
            f"cause la sécurité — {_f(n_bloq / n_tot * 100, 1)} %. Les lever toutes "
            f"demande {_f(h_tot)} heures, soit {_f(h_tot / (eff * heures_jour), 1)} "
            f"jours à {eff} compagnons, pour {_f(h_tot * taux)} MAD. Mais seules les "
            f"{n_bloq} bloquantes sont à lever AVANT la réception : "
            f"{_f(jours_bloq, 1)} jours. Les autres se lèvent après, sous délai, et le "
            "chantier est réceptionné pendant ce temps."),
        "_le_prix_de_la_confusion": (
            f"Traiter les {n_tot - n_bloq} réserves non bloquantes comme bloquantes "
            f"repousse la réception de {_f(jours_non_bloq, 1)} jours ouvrés. À "
            f"{_f(cj['cout_avant_le_plafond_MAD_par_jour_ouvre'])} MAD le jour de "
            f"non-réception, cela coûte {_f(cout_confusion)} MAD — plus de "
            f"{_f(cout_confusion / (h_tot * taux), 0)} fois le prix de lever TOUTES les "
            "réserves, bloquantes comprises. La question n'est donc jamais « y a-t-il "
            "des réserves ? » mais « laquelle empêche l'usage ? »."),
        "_et_dans_l_autre_sens": (
            "Le symétrique est pire, et il est moins visible : réceptionner avec une "
            "réserve de sécurité classée « aspect » parce qu'elle était seule de sa "
            "famille dans une liste de quatre-vingt-dix lignes. Un garde-corps non "
            "conforme ne devient pas une finition parce qu'il est noyé dans une liste. "
            "C'est pourquoi le classement se fait ligne à ligne, par la seule question "
            "qui décide, et non par un comptage."),
    }


# ------------------------------------------------- 4. le DOE
def doe(d: dict, pr: dict, po: dict) -> dict:
    """Le DOE se constitue pendant le chantier. Reconstitué, il coûte quatre fois plus.

    Et il ne coûte pas que des heures : il bloque le décompte définitif, c'est-à-dire de
    l'argent dû, non payé, que l'entreprise porte au taux de son découvert.
    """
    o = d["reception"]["doe"]
    taux_cadre = d["prix_unitaires_MAD"]["ressources"]["main_oeuvre_MAD_h"]["controleur"]["valeur"]
    fil, rec = o["heures_au_fil_de_l_eau"]["valeur"], o["heures_reconstitue"]["valeur"]
    fb, rb = _b(o["heures_au_fil_de_l_eau"]), _b(o["heures_reconstitue"])
    jours, jb = o["retard_du_solde_j"]["valeur"], _b(o["retard_du_solde_j"])
    bloque = po["retenue_immobilisee_MAD"]
    taux_portage = po["taux_de_portage_annuel_pct"]
    # La base de l'annee est une CLAUSE de la convention de credit, pas une constante :
    # 365 et 360 sont tous deux courants et different de 1,4 % sur le meme calcul. La
    # verification dimensionnelle a trouve ce point en comparant le resultat a une annee
    # de 365,25 jours — un chiffre qui n'a de sens qu'en astronomie.
    base = d["prix_unitaires_MAD"]["contrat"]["base_de_calcul_des_interets_j"]
    portage = bloque * taux_portage / 100 * jours / base
    return {
        "heures_au_fil_de_l_eau": fil,
        "heures_reconstitue": rec,
        "rapport_des_heures": round(rec / fil, 1),
        "taux_horaire_de_cadre_MAD": taux_cadre,
        "cout_au_fil_de_l_eau_MAD": round(fil * taux_cadre, 2),
        "cout_reconstitue_MAD": round(rec * taux_cadre, 2),
        "surcout_en_heures_MAD": round((rec - fil) * taux_cadre, 2),
        "surcout_bornes_MAD": [round((rb[0] - fb[1]) * taux_cadre, 2),
                               round((rb[1] - fb[0]) * taux_cadre, 2)],
        "montant_bloque_MAD": bloque,
        "retard_du_solde_j": jours,
        "cout_de_portage_MAD": round(portage, 2),
        "base_de_calcul_des_interets_j": base,
        "cout_de_portage_bornes_MAD": [round(bloque * taux_portage / 100 * jb[0] / base, 2),
                                       round(bloque * taux_portage / 100 * jb[1] / base, 2)],
        "_la_base_est_une_clause": (
            f"Les intérêts sont calculés sur une année de {base} jours. Ce n'est pas une "
            "constante : la base 360, dite bancaire, est tout aussi courante, et elle "
            f"donne {_f(bloque * taux_portage / 100 * jours / 360)} MAD au lieu de "
            f"{_f(bloque * taux_portage / 100 * jours / base)} — 1,4 % d'écart sur le "
            "même calcul. Cela se lit dans la convention de crédit, cela ne se suppose "
            "pas, et cela ne se découvre pas en relisant une formule : ici, c'est la "
            "vérification dimensionnelle qui l'a signalé, en comparant le résultat à "
            "une année de 365,25 jours."),
        "cout_total_du_retard_de_DOE_MAD": round((rec - fil) * taux_cadre + portage, 2),
        "lecture": (
            f"Tenu au fil de l'eau, le dossier demande {_f(fil)} heures de cadre, soit "
            f"{_f(fil * taux_cadre)} MAD. Reconstitué après coup, il en demande "
            f"{_f(rec)} — {_f(rec / fil, 1)} fois plus — et pendant qu'on le "
            f"reconstitue, il bloque le décompte définitif. Porter {_f(bloque)} MAD "
            f"pendant {_f(jours)} jours au taux de {_f(taux_portage, 1)} % l'an coûte "
            f"{_f(portage)} MAD de plus. Le retard de DOE coûte donc "
            f"{_f((rec - fil) * taux_cadre + portage)} MAD, dont "
            f"{_f(portage / ((rec - fil) * taux_cadre + portage) * 100)} % qui ne sont "
            "ni du travail ni une pénalité : seulement de l'argent qui attend."),
        "_pourquoi_c_est_sous_estime": (
            "Parce que le DOE ne coûte rien tant qu'on ne le fait pas. C'est une tâche "
            "sans cadence, sans point d'arrêt, dont personne ne constate l'absence avant "
            "la fin — et qui, à ce moment-là, est sur le chemin critique de l'argent. "
            "Les quatre cinquièmes de son surcoût se décident pendant le chantier, dans "
            "des moments où il ne coûtait rien de demander le document : quand le "
            "sous-traitant est encore là, quand la paroi est encore ouverte, quand "
            "celui qui a posé se souvient de ce qu'il a posé."),
        "_le_montant_bloque_est_une_borne_basse": (
            "Ce calcul ne bloque que la retenue de garantie, parce que c'est le seul "
            "montant que ce cours publie. Un décompte définitif porte aussi le solde des "
            "travaux, les révisions de prix non encore réglées et les travaux "
            "supplémentaires acceptés. Le portage réel est donc supérieur, et dans des "
            "proportions qui dépendent du marché."),
        "_le_critere_pratique": o["_ce_qu_il_doit_contenir"],
    }


# ------------------------------------------------- 5. les opérations préalables
def operations_prealables(d: dict) -> dict:
    """La séquence, et sa durée — qui est du délai, pas une formalité."""
    o = d["reception"]["operations_prealables"]
    etapes = o["etapes"]
    cumul, lignes = 0, []
    for e in etapes:
        cumul += e["duree_j"]
        lignes.append({**e, "fin_j": cumul})
    return {
        "etapes": lignes,
        "nb_etapes": len(etapes),
        "duree_totale_j": cumul,
        "note": (
            f"{len(etapes)} étapes, {cumul} jours entre l'avis de fin de travaux et la "
            "décision du maître d'ouvrage — si tout va bien, et si personne n'est "
            "absent. Ce n'est pas une formalité administrative : c'est une tâche du "
            "planning, avec une durée, qui doit y figurer. Un planning qui finit au "
            "dernier coup de peinture ment d'un mois et demi."),
        "_l_essai_qui_commande": (
            "La mise en service des systèmes est la plus longue des étapes, et c'est "
            "aussi la seule que l'entreprise ne maîtrise pas : c'est l'exploitant "
            "ferroviaire qui la conduit. Elle se prépare donc comme une consignation — "
            "demandée longtemps à l'avance, avec ses prérequis vérifiés un par un. Un "
            "essai de système reporté ne se rattrape pas en y mettant plus de monde."),
    }


# ------------------------------------------------- 6. ce que le planning en prevoit
def confrontation_au_planning(d: dict, pr: dict, cj: dict, op: dict) -> dict:
    """Le planning prevoit-il la reception qu'il annonce ? Mesure, pas supposition.

    Le module D2 porte deux taches de fin : « Essais et mise en service » et
    « Reception ». La seconde dure dix jours. La sequence du § S3a en demande davantage,
    une fois la mise en service mise de cote puisqu'elle est deja la premiere.

    Attention a ce que ce calcul EST et n'est pas. Les durees des deux cotes sont des
    decisions de ce cours, posees a deux moments differents : D2 a pose « reception =
    dix jours » avant que ce module n'existe et sans la decomposer, et ce module a pose
    une sequence en six etapes. Ce n'est donc pas la decouverte d'une erreur dans un
    planning reel — c'est la confrontation de deux chiffres de ce cours, et elle vaut
    par son MECANISME : une tache « Reception » qui n'a pas ete decomposee est presque
    toujours trop courte, parce qu'on y pense comme a une signature et qu'elle est une
    sequence.

    L'ecart sur la date de fin est MESURE en rejouant le reseau (D-040), pas deduit de
    la marge : la tache est la derniere du chemin critique, mais le verifier coute un
    appel et evite d'affirmer.
    """
    import copy
    sys.path.insert(0, str(RACINE / "calc"))
    import planification as pln                                          # noqa: E402
    pl = json.loads((RACINE / "calc" / "sorties" / "planification.json")
                    .read_text(encoding="utf-8"))
    prevu = pl["durees"]["RECE"]["duree_j"]
    essais = pl["durees"]["ESSA"]["duree_j"]
    # L'etape « mise en service » de la sequence est deja portee par la tache ESSA du
    # planning : la compter deux fois serait exactement la faute que ce cours reproche
    # ailleurs. On retire donc du besoin ce que le planning porte deja.
    deja = next((x for x in op["etapes"] if "ise en service" in x["etape"]), None)
    besoin = op["duree_totale_j"] - (deja["duree_j"] if deja else 0)
    ecart = besoin - prevu

    tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json")
                    .read_text(encoding="utf-8"))
    q = pln.quantites_chantier(d, d["planning"])
    t0 = pln.durees_chantier(d, d["planning"], q,
                             tv["planning_plancher"]["duree_totale_j"])
    ref = pln.voie_A_parcours(pln.planning_avec_fenetres(d, t0)["taches"])["duree"]
    t1 = copy.deepcopy(t0)
    t1["RECE"]["duree_j"] = prevu + max(0.0, ecart)
    fin = pln.voie_A_parcours(pln.planning_avec_fenetres(d, t1)["taches"])["duree"]
    decalage = round(fin - ref, 2)
    return {
        "duree_prevue_par_le_planning_j": prevu,
        "duree_des_essais_au_planning_j": essais,
        "etape_deja_portee_par_le_planning": deja["etape"] if deja else None,
        "duree_demandee_par_la_sequence_j": round(besoin, 2),
        "ecart_j": round(ecart, 2),
        "decalage_mesure_de_la_fin_j": decalage,
        "duree_de_reference_j": round(ref, 2),
        "cout_de_l_ecart_MAD": round(decalage
                                     * cj["cout_avant_le_plafond_MAD_par_jour_ouvre"], 2),
        "lecture": (
            f"Le planning prévoit {_f(prevu)} jours pour la réception, et "
            f"{_f(essais)} pour les essais et la mise en service. La séquence du § S3a "
            f"en demande {_f(besoin)} une fois la mise en service mise de côté, "
            f"puisqu'elle est déjà la tâche précédente. L'écart est de "
            f"{_f(ecart)} jours ouvrés, et le réseau rejoué décale la fin de "
            f"{_f(decalage)} jours — la tâche est la dernière du chemin critique, rien "
            f"ne l'absorbe. Au prix du jour de non-réception, cela vaut "
            f"{_f(decalage * cj['cout_avant_le_plafond_MAD_par_jour_ouvre'])} MAD."),
        "_ce_que_cette_comparaison_est": (
            "Deux chiffres de ce cours, posés à deux moments différents, et non la "
            "découverte d'une erreur dans un planning réel : le module D2 a posé "
            "« réception = dix jours » avant que ce module n'existe, sans la "
            "décomposer. Ce qui se généralise n'est donc pas l'écart — il dépend "
            "entièrement des durées posées ici — mais le MÉCANISME : une tâche "
            "« Réception » non décomposée est presque toujours trop courte, parce qu'on "
            "y pense comme à une signature alors que c'est une séquence, et parce que "
            "les deux étapes qui la font déborder — les essais de fonctionnement et le "
            "procès-verbal du maître d'ouvrage — ne dépendent pas de l'entreprise."),
        "_quoi_en_faire": (
            "Décomposer la ligne « Réception » du planning en ses étapes, chacune avec "
            "son responsable, comme on décompose un cycle de gros œuvre. C'est la seule "
            "façon de voir que la moitié de sa durée n'appartient pas à l'entreprise — "
            "et donc de la préparer au lieu de la subir. Un planning qui finit sur une "
            "tâche « Réception » de dix jours sans détail annonce une date qu'il n'a pas "
            "vérifiée."),
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
        "reserves": [{"libelle": f"{x['famille']}"
                                 f"{' · BLOQUANTE' if x['empeche_l_usage'] else ''}",
                      "valeur": x["nombre"]} for x in rs["lignes"]],
        "doe": [
            {"libelle": "DOE tenu au fil de l'eau", "montant": round(dd["cout_au_fil_de_l_eau_MAD"] / 1000)},
            {"libelle": "Heures de reconstitution en plus", "montant": round(dd["surcout_en_heures_MAD"] / 1000)},
            {"libelle": "Portage du décompte bloqué", "montant": round(dd["cout_de_portage_MAD"] / 1000)},
            {"libelle": "Total d'un DOE reconstitué", "montant": round(
                (dd["cout_reconstitue_MAD"] + dd["cout_de_portage_MAD"]) / 1000), "type": "total"},
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
        "confrontation_au_planning": cf,
        "cout_d_un_jour": cj,
        "courbe_du_cout": co,
        "portage": po,
        "reserves": rs,
        "doe": dd,
        "operations_prealables": op,
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
    print(f"jour de non-reception : {c['cout_avant_le_plafond_MAD_par_jour_ouvre']:.0f} MAD "
          f"puis {c['cout_apres_le_plafond_MAD_par_jour_ouvre']:.0f} "
          f"(x{c['rapport_des_deux_regimes']}), bascule au "
          f"{c['jour_de_bascule_calendaire']}e jour calendaire "
          f"{c['jour_de_bascule_bornes_calendaires']}")
    print(f"portage : retenue {p['retenue_immobilisee_MAD']:.0f} MAD, "
          f"{p['cout_de_la_retenue_MAD_par_mois']:.0f} MAD/mois contre "
          f"{p['cout_de_la_caution_MAD_par_mois']:.0f} — rapport {p['rapport_des_deux_couts']}")
    print(f"reserves : {s['nb_total']} dont {s['nb_bloquantes']} bloquantes ; "
          f"la confusion coute {s['cout_de_la_confusion_MAD']:.0f} MAD")
    print(f"DOE : {o['cout_total_du_retard_de_DOE_MAD']:.0f} MAD dont "
          f"{o['cout_de_portage_MAD']:.0f} de portage")
    cf = r["confrontation_au_planning"]
    print(f"OPR : {r['operations_prealables']['duree_totale_j']} j ; le planning en "
          f"prevoit {cf['duree_prevue_par_le_planning_j']:.0f} pour "
          f"{cf['duree_demandee_par_la_sequence_j']:.0f} demandes — "
          f"fin decalee de {cf['decalage_mesure_de_la_fin_j']:.1f} j, "
          f"{cf['cout_de_l_ecart_MAD']:.0f} MAD")
