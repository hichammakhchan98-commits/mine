"""Qualité, HSE, environnement : ce qui rend la sécurité pilotable (C7).

Ce module ne cite aucune valeur réglementaire — ni fréquence de prélèvement, ni critère
de résistance, ni distance de sécurité. Il calcule ce qui n'en dépend pas, et c'est
exactement ce qu'un chef de projet suivi manipule tous les jours :

1. L'EXPOSITION se compte en HEURES, jamais en effectif. C'est le dénominateur de tous
   les indicateurs de sécurité, et c'est ce qui permet de comparer deux chantiers. Le
   cours connaît désormais ses heures tâche par tâche, et D1 les retrouve identiques
   depuis l'autre bout de la chaîne — ce qui rend le calcul vérifiable par une seconde
   voie au lieu d'être cru sur parole.
2. Le COÛT D'UNE NON-CONFORMITÉ n'est pas le coût de sa reprise. C'est la reprise, plus
   l'attente de la décision, plus le décalage mesuré sur le réseau, plus le
   durcissement du contrôle sur tout ce qui suit.
3. La CRITICITÉ d'un risque est un produit d'échelles ORDINALES : elle sert à classer,
   jamais à chiffrer. Multiplier des rangs ne produit pas une grandeur — c'est la même
   faute de domaine que D-037 dénonce ailleurs, et elle est universelle dans les
   analyses de risques.

Toute grandeur publiée ici porte ses BORNES (D-036) : les entrées sont des hypothèses
V3 à fourchette large, et un résultat publié sans ses bornes laisse croire à une
précision qu'il n'a pas. Les bornes du retard et du coût ne sont pas déduites : elles
sont MESURÉES en rejouant le réseau aux deux bornes de l'immobilisation (D-040).
"""
from __future__ import annotations
import json, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import planification as pln                                              # noqa: E402
import plage                                                             # noqa: E402


# ------------------------------------------------------------------ mise en forme
def _f(x: float, dec: int = 0) -> str:
    """Format français : espace fine insécable pour les milliers, virgule décimale.

    Une version précédente formatait avec `f"{x:,.0f}"` puis remplaçait TOUTES les
    virgules de la chaîne par des espaces : elle effaçait aussi la ponctuation, et trois
    phrases publiées se lisaient « ... heures travaillées dont 4 651 ». Le séparateur se
    pose à la source, pas par un remplacement global.
    """
    s = f"{x:,.{dec}f}".replace(",", " ")
    return s.replace(".", ",") if dec else s


def _trois(x: float) -> float:
    """Trois chiffres significatifs (§ 3.6) — pour les valeurs envoyées aux figures.

    Le corps du texte formate ses nombres ; les figures, elles, impriment la valeur
    brute. Elles affichaient « 134213,56 » pour une hypothèse connue à un facteur deux
    près.
    """
    from math import floor, log10
    if not x:
        return 0.0
    p = 2 - floor(log10(abs(x)))
    return round(x, p) if p > 0 else float(round(x, p))


def _bornes(o: dict) -> tuple[float, float]:
    f = o.get("fourchette")
    return (float(f[0]), float(f[1])) if f else (float(o["valeur"]), float(o["valeur"]))


# ---------------------------------------------------- 1. l'exposition, en heures
def exposition(d: dict, pl: dict) -> dict:
    """Les heures travaillées, et comment le risque s'y répartit entre jour et nuit.

    Un indicateur de sécurité se rapporte TOUJOURS à des heures : c'est la seule assiette
    qui absorbe à la fois l'effectif et la durée. Dix compagnons pendant deux ans et cent
    pendant deux mois n'ont ni le même risque ni le même nombre d'heures.

    La pondération de la nuit RÉPARTIT le risque, elle ne l'augmente pas. C'est le point
    délicat, et une première version s'y est trompée : elle appliquait le taux de
    fréquence de référence à des heures pondérées, ce qui CRÉAIT des accidents — +6,4 %,
    et davantage encore si l'on montait le coefficient. Or un taux de branche est mesuré
    sur des heures RÉELLES, et ces heures contiennent déjà leur part de travail de nuit :
    le multiplier par une pondération le compte deux fois. Les poids sont donc normalisés
    pour que leur somme redonne les heures réelles. Le total d'accidents ne dépend alors
    que du taux et des heures ; seule leur RÉPARTITION dépend du coefficient, ce qui est
    exactement ce qu'on lui demande.
    """
    e = d["qualite_hse"]["exposition"]
    h = pl["heures_de_main_oeuvre_par_tache"]
    nuit = set(d["planning"]["contraintes_exploitation"]["taches_soumises"])
    h_nuit = sum(v for i, v in h.items() if i in nuit)
    h_jour = sum(v for i, v in h.items() if i not in nuit)
    total = h_nuit + h_jour
    tf, tg, k = (e["taux_de_frequence_reference"]["valeur"],
                 e["taux_de_gravite_reference"]["valeur"],
                 e["surexposition_du_travail_de_nuit"]["valeur"])
    tf_b, tg_b, k_b = (_bornes(e["taux_de_frequence_reference"]),
                       _bornes(e["taux_de_gravite_reference"]),
                       _bornes(e["surexposition_du_travail_de_nuit"]))
    brut = h_jour + k * h_nuit
    norm = total / brut                      # ramène la somme des poids aux heures réelles
    part_h = h_nuit / total
    part_r = k * h_nuit / brut
    part_r_b = [round(x * h_nuit / (h_jour + x * h_nuit) * 100, 2) for x in k_b]
    accidents = tf * total / 1e6             # sur les heures RÉELLES : pas de double compte
    r = plage.rendement(d)
    plus_grosse = max(h, key=lambda i: h[i])
    # Cas degeneres : un chantier sans heures de nuit n'a pas de rapport de parts. Le
    # module le dit au lieu de diviser par zero — l'etalonnage passe par la.
    rapport = part_r / part_h if part_h else 0.0
    pourquoi_le_rapport = (
        f"Le coefficient vaut {_f(k, 1)} et la part du risque n'est pourtant que "
        f"{_f(rapport, 2)} fois la part des heures : {_f(part_h * 100, 1)} % "
        f"deviennent {_f(part_r * 100, 1)} %, et non {_f(part_h * k * 100, 1)} %. Le "
        "dénominateur a grossi lui aussi — les heures de nuit pèsent plus lourd au "
        "numérateur ET au dénominateur. Un lecteur qui multiplie de tête trouve un "
        "chiffre trop grand, et il a raison de s'en étonner : c'est la mécanique d'une "
        "clé de répartition, pas celle d'une majoration."
        if part_h else
        "Ce chantier n'a aucune heure de nuit : la part du risque de nuit est nulle, et "
        "le rapport entre les deux parts n'est pas défini. Le publier comme valant zéro "
        "serait faux — zéro sur zéro n'est pas zéro (D-042).")
    return {
        "heures_totales": round(total, 1),
        "heures_de_jour": round(h_jour, 1),
        "heures_de_nuit": round(h_nuit, 1),
        "part_de_nuit_pct": round(part_h * 100, 2),
        "taches_de_nuit": sorted(nuit),
        "coefficient_de_surexposition_de_nuit": k,
        "facteur_de_normalisation": round(norm, 4),
        "part_de_nuit_dans_le_risque_pct": round(part_r * 100, 2),
        "part_de_nuit_dans_le_risque_bornes_pct": part_r_b,
        "surcroit_de_part_pct": round((part_r - part_h) * 100, 2),
        "rapport_des_parts": round(rapport, 2) if part_h else None,
        "_pourquoi_le_rapport_n_est_pas_le_coefficient": pourquoi_le_rapport,
        "taux_de_frequence_de_reference": tf,
        "taux_de_gravite_de_reference": tg,
        "accidents_avec_arret_attendus": round(accidents, 2),
        "accidents_bornes": [round(x * total / 1e6, 2) for x in tf_b],
        "dont_attribuables_a_la_nuit": round(accidents * part_r, 2),
        "journees_perdues_attendues": round(tg * total / 1000, 1),
        "journees_perdues_bornes": [round(x * total / 1000, 1) for x in tg_b],
        "_bornes": (
            f"Les heures sont connues — elles viennent du planning, et le module D1 les "
            f"retrouve tâche par tâche depuis les prix. Les taux, non : ce sont des "
            f"hypothèses déclarées. Les accidents attendus valent donc de "
            f"{_f(tf_b[0] * total / 1e6, 2)} à {_f(tf_b[1] * total / 1e6, 2)} et les "
            f"journées perdues de {_f(tg_b[0] * total / 1000)} à "
            f"{_f(tg_b[1] * total / 1000)}. La part de nuit dans le risque, elle, va de "
            f"{_f(part_r_b[0], 1)} à {_f(part_r_b[1], 1)} % : c'est le nombre le plus "
            "fragile du module, et c'est aussi celui qu'on a le plus envie de citer. Ce "
            "qui résiste aux bornes n'est aucun de ces nombres — c'est leur ORDRE : la "
            "nuit pèse plus que ses heures, quelle que soit la borne retenue."),
        "lecture": (
            f"Le chantier représente {_f(total)} heures travaillées, dont "
            f"{_f(h_nuit)} de nuit sous interception — {_f(part_h * 100, 1)} % des "
            f"heures. Mais une heure de nuit expose {_f(k, 1)} fois plus : elle pèse "
            f"{_f(part_r * 100, 1)} % du risque. C'est le premier résultat de ce "
            "module, et il ne se voit sur aucun effectif."),
        "_la_ponderation_repartit_elle_n_ajoute_pas": (
            f"Les {_f(accidents, 2)} accidents attendus se calculent sur les heures "
            "RÉELLES, jamais sur les heures pondérées : un taux de branche est mesuré "
            "sur des heures réelles qui contiennent déjà du travail de nuit, et "
            "l'appliquer à des heures gonflées le compterait deux fois. Le coefficient "
            "ne change donc pas le total — il change la RÉPARTITION, et c'est tout ce "
            f"qu'on lui demande. Contrôle : porter le coefficient de {_f(k, 1)} à 3,0 ne "
            "doit pas faire varier le total d'un centième."),
        "_ce_que_le_nombre_d_accidents_n_est_pas": (
            "Ce n'est PAS une prévision, et encore moins un objectif : c'est ce qu'un "
            "taux de référence APPLIQUÉ à ces heures donnerait. Il sert à dimensionner — "
            "combien de secouristes, quelle organisation des secours, quel budget de "
            "prévention — et à comparer. Annoncer un nombre d'accidents à venir serait "
            "aussi faux que d'annoncer qu'il n'y en aura aucun, et plus dangereux : un "
            "nombre annoncé devient une permission."),
        "_pourquoi_pas_l_effectif": (
            "Un effectif ne dit rien de l'exposition : dix compagnons pendant deux ans "
            "et cent pendant deux mois n'ont ni le même risque ni le même nombre "
            "d'heures. Piloter la sécurité sur un effectif, c'est la même faute que "
            "piloter un avancement sur un pourcentage sans dénominateur (module D4)."),
        "assiette": {
            "taches_sans_heures": sorted(i for i, v in h.items() if v == 0),
            "note": (
                "Les tâches à zéro heure ne sont pas une lacune du calcul, mais elles "
                "dessinent une FRONTIÈRE qu'il faut énoncer avant de se servir du "
                "résultat : l'assiette couvre les heures passées SUR LE SITE. Les "
                "études, la fabrication en ATELIER et le séchage en sont exclus. Or la "
                "fabrication de la charpente, ce sont des centaines de tonnes soudées, "
                "meulées et manutentionnées ailleurs — précisément les postes que le "
                "module B5 associe aux contrôles non destructifs. Leur risque existe, il "
                "est lourd, et il appartient à l'établissement du fabricant."),
            "consequence": (
                "Un taux de fréquence de chantier ne couvre donc pas l'atelier. Le chef "
                "de projet suivi qui veut savoir ce que sa charpente coûte en accidents "
                "doit le DEMANDER au fabricant, et il ne l'obtiendra pas en lisant son "
                "propre tableau de bord. Croire l'assiette complète est la première "
                "façon de se rassurer à bon compte."),
            "perimetre_des_entreprises": (
                "Deuxième frontière, et elle est plus piégeuse que la première : "
                "l'assiette compte TOUTES les entreprises présentes sur le site, "
                f"sous-traitants compris. La tâche {plus_grosse} pèse à elle seule "
                f"{_f(h[plus_grosse] / total * 100)} % des heures et elle est très "
                "probablement sous-traitée. Un taux de fréquence se calcule normalement "
                "sur le périmètre de l'entité qui le déclare : celui de l'entreprise "
                "générale seule porterait sur une autre assiette, et il serait plus "
                "flatteur sans qu'aucun accident ait été évité. Comparer deux taux sans "
                "comparer leurs périmètres est la même faute que comparer deux "
                "pourcentages sans dénominateur."),
        },
        "presence_et_production_de_nuit": {
            "duree_de_la_plage_h": r["duree_nominale_h"],
            "travail_effectif_h": r["travail_effectif_h"],
            "part_fixe_h": r["part_fixe_h"],
            "rapport_presence_production": round(
                r["duree_nominale_h"] / r["travail_effectif_h"], 2),
            "note": (
                "Les deux tâches sous interception se font INTÉGRALEMENT de nuit : la "
                "fenêtre va de la dernière circulation à la première du matin (module "
                f"B7c). Et sur les {_f(r['duree_nominale_h'], 1)} heures d'une plage, "
                f"{_f(r['part_fixe_h'], 2)} ne sont pas du travail — prise de "
                "possession, consignation, amenée, repli, déconsignation, marge de "
                "restitution — mais elles sont toutes de l'EXPOSITION : on est sur la "
                "voie, de nuit, à côté d'une caténaire. L'exposition compte donc la "
                "présence là où le module D1 compte la production, et la nuit "
                f"d'interception expose "
                f"{_f(r['duree_nominale_h'] / r['travail_effectif_h'], 2)} fois son "
                "temps productif. Les deux comptes sont justes ; ce qui serait faux est "
                "de les additionner ou de les confondre."),
        },
        "par_tache": sorted(
            ({"tache": i, "heures": round(v, 1),
              "de_nuit": i in nuit,
              "part_des_heures_pct": round(v / total * 100, 1),
              "part_du_risque_pct": round((k if i in nuit else 1) * v / brut * 100, 1)}
             for i, v in h.items() if v > 0),
            key=lambda x: -x["heures"]),
    }


def comparaison_de_deux_chantiers(d: dict, acc_a: int, eff_a: int,
                                  acc_b: int, eff_b: int) -> dict:
    """Le calcul de l'exercice 1 : deux chantiers que leur nombre d'accidents classe mal.

    Cinq nombres étaient tapés à la main dans le corrigé, dont une hypothèse — les heures
    annuelles d'un compagnon — qui n'était ni balisée, ni bornée, ni registrée. Le § 4.3
    l'interdit, et avec raison : c'est l'hypothèse qui porte toute la démonstration.
    """
    o = d["qualite_hse"]["exposition"]["heures_par_compagnon_et_par_an"]
    hpa = o["valeur"]
    b = _bornes(o)
    h_a, h_b = eff_a * hpa, eff_b * hpa
    tf_a, tf_bb = acc_a * 1e6 / h_a, acc_b * 1e6 / h_b
    return {
        "heures_par_compagnon_et_par_an": hpa,
        "chantiers": [
            {"nom": "A", "accidents": acc_a, "effectif": eff_a,
             "heures": round(h_a), "tf": round(tf_a, 1),
             "tf_bornes": [round(acc_a * 1e6 / (eff_a * b[1]), 1),
                           round(acc_a * 1e6 / (eff_a * b[0]), 1)]},
            {"nom": "B", "accidents": acc_b, "effectif": eff_b,
             "heures": round(h_b), "tf": round(tf_bb, 1),
             "tf_bornes": [round(acc_b * 1e6 / (eff_b * b[1]), 1),
                           round(acc_b * 1e6 / (eff_b * b[0]), 1)]},
        ],
        "rapport_des_taux": round(tf_a / tf_bb, 2),
        "_le_rapport_ne_depend_pas_de_l_hypothese": (
            "Les deux taux dépendent entièrement des heures annuelles retenues, mais "
            f"leur RAPPORT — {_f(tf_a / tf_bb, 2)} — n'en dépend pas du tout : "
            "l'hypothèse se simplifie. C'est ce qui rend la conclusion de l'exercice "
            "solide alors que ses deux nombres ne le sont pas, et c'est un réflexe à "
            "prendre : avant de borner un résultat, regarder si la question posée ne "
            "porte pas sur un rapport."),
    }


# ---------------------------------------------------- 2. le coût d'une non-conformité
def cout_de_la_non_conformite(d: dict, pl: dict, pr: dict, imp: dict,
                              imp_bornes=None) -> dict:
    """Ce qu'une NC coûte vraiment — et cela dépend ENTIÈREMENT de l'ouvrage touché.

    Le réflexe est de chiffrer la reprise. Mais les frais de durée du CHANTIER ne courent
    que si la fin du chantier bouge : les imputer à une non-conformité sur un ouvrage qui
    a de la marge est une faute, et c'est exactement celle que D-040 interdit. Une
    première version de ce module la commettait — elle facturait 113 682 MAD
    d'immobilisation à un ouvrage dont elle montrait deux sections plus loin qu'il ne
    décalait rien.

    Le coût se calcule donc pour CHAQUE régime, et le résultat est bien plus instructif
    que le nombre unique qu'il remplace : la même non-conformité, le même défaut, la
    même surface, coûte d'un facteur dix-sept selon l'ouvrage — et la part VISIBLE sur
    un devis passe de 6 % à 100 %.

    L'heure de contrôle n'est pas payée au taux du compagnon. Le durcissement du contrôle
    est du temps de CADRE — maîtrise d'œuvre, bureau d'études ou service qualité — et le
    chiffrer au taux de production le divisait par trois, dans la ligne même sur laquelle
    le module concluait.
    """
    nc = d["qualite_hse"]["non_conformite"]
    v = {k: nc[k]["valeur"] for k in nc if isinstance(nc[k], dict) and "valeur" in nc[k]}
    bo = {k: _bornes(nc[k]) for k in nc if isinstance(nc[k], dict) and "valeur" in nc[k]}
    fd = pr["bordereau"]["frais_de_duree"]["cout_MAD_par_jour_ouvre"]
    poste = d["prix_unitaires_MAD"]["ressources"]["main_oeuvre_MAD_h"]["controleur"]
    taux, taux_b = poste["valeur"], _bornes(poste)

    reprise = v["surface_m2"] * v["cout_de_reprise_MAD_m2"]
    h_sup = (v["heures_de_controle_par_levee"] * v["durcissement_du_controle_pct"] / 100
             * v["levees_restantes"])
    controle = h_sup * taux
    visible = reprise + controle
    visible_b = [bo["surface_m2"][i] * bo["cout_de_reprise_MAD_m2"][i]
                 + bo["heures_de_controle_par_levee"][i]
                 * bo["durcissement_du_controle_pct"][i] / 100
                 * bo["levees_restantes"][i] * taux_b[i] for i in (0, 1)]

    cas = []
    for n, x in enumerate(imp["lignes"]):
        delai = x["retard_du_chantier_j"] * fd
        total = visible + delai
        # Les bornes du retard sont MESURÉES : le réseau est rejoué à l'immobilisation
        # basse et haute (D-040). Les déduire en multipliant le retard nominal par le
        # rapport des immobilisations donnerait un nombre qui ne sort d'aucun réseau.
        rb = ([imp_bornes[i]["lignes"][n]["retard_du_chantier_j"] for i in (0, 1)]
              if imp_bornes else [x["retard_du_chantier_j"]] * 2)
        cas.append({
            "tache": x["tache"], "nom": x["nom"], "regime": x["regime"],
            "marge_totale_j": x["marge_totale_j"],
            "retard_du_chantier_j": x["retard_du_chantier_j"],
            "retard_bornes_j": rb,
            "reprise_MAD": round(reprise, 2),
            "durcissement_du_controle_MAD": round(controle, 2),
            "frais_de_duree_MAD": round(delai, 2),
            "total_MAD": round(total, 2),
            "total_bornes_MAD": [round(visible_b[0] + rb[0] * fd, 2),
                                 round(visible_b[1] + rb[1] * fd, 2)],
            "part_visible_pct": round(visible / total * 100, 1),
        })
    pire = max(cas, key=lambda c: c["total_MAD"])
    moindre = min(cas, key=lambda c: c["total_MAD"])
    return {
        "ouvrage": nc["ouvrage"],
        "taux_de_l_heure_de_controle_MAD": taux,
        "heures_de_controle_ajoutees": round(h_sup, 2),
        "part_visible_sur_un_devis_MAD": round(visible, 2),
        "part_visible_bornes_MAD": [round(visible_b[0], 2), round(visible_b[1], 2)],
        "detail_de_la_part_visible": [
            {"poste": "Reprise du parement", "montant_MAD": round(reprise, 2),
             "note": f"{_f(v['surface_m2'])} m² de parement vu"},
            {"poste": "Durcissement du contrôle", "montant_MAD": round(controle, 2),
             "note": f"+{_f(v['durcissement_du_controle_pct'])} % de temps de contrôle "
                     f"sur les {_f(v['levees_restantes'])} levées restantes, soit "
                     f"{_f(h_sup, 2)} h de cadre"},
        ],
        "_pourquoi_l_heure_de_controle_coute_plus": (
            f"Le durcissement du contrôle est du temps de CADRE — maîtrise d'œuvre, "
            f"bureau d'études ou service qualité — et non du temps de production : "
            f"{_f(taux)} MAD l'heure, pas le taux du compagnon. Le recoupement vient des "
            "frais de durée du module D1, qui portent l'encadrement du chantier au mois. "
            "Une version précédente payait ces heures au taux du compagnon et concluait, "
            "sur cette ligne-là, que le durcissement du contrôle ne pèse rien : la "
            f"conclusion survit — {_f(controle)} MAD contre {_f(reprise)} MAD de "
            "reprise — mais elle n'était pas démontrée, et elle reposait sur un taux "
            "sous-estimé d'un facteur trois."),
        "jours_immobilises": v["delai_de_decision_j"] + v["duree_de_reprise_j"],
        "jours_immobilises_bornes": [
            bo["delai_de_decision_j"][0] + bo["duree_de_reprise_j"][0],
            bo["delai_de_decision_j"][1] + bo["duree_de_reprise_j"][1]],
        "decomposition_de_l_immobilisation": {
            "delai_de_decision_j": v["delai_de_decision_j"],
            "duree_de_reprise_j": v["duree_de_reprise_j"],
            "note": ("l'attente de la décision — expertise, avis du bureau d'études, "
                     "accord sur la méthode — est le poste qu'on oublie, et souvent le "
                     "plus long des deux. Il ne coûte rien si l'ouvrage a de la marge, "
                     "et tout s'il n'en a pas."),
        },
        "frais_de_duree_MAD_par_jour_ouvre": fd,
        "_source_des_frais": "calc/sorties/prix.json — bordereau.frais_de_duree",
        "par_ouvrage": cas,
        "ecart_entre_les_regimes": round(pire["total_MAD"] / moindre["total_MAD"], 1),
        "lecture": (
            f"La partie visible — la reprise et le durcissement du contrôle — vaut "
            f"{_f(visible)} MAD et ne dépend pas de l'ouvrage. Le reste en dépend "
            f"entièrement : {_f(moindre['total_MAD'])} MAD sur {moindre['tache']}, "
            f"{_f(pire['total_MAD'])} sur {pire['tache']}, soit un facteur "
            f"{_f(pire['total_MAD'] / moindre['total_MAD'])}. Et la part qu'un devis "
            f"montre passe de {_f(pire['part_visible_pct'])} % à "
            f"{_f(moindre['part_visible_pct'])} %."),
        "_bornes": (
            f"Rien de tout cela n'est connu à mieux qu'un facteur deux. La part visible "
            f"va de {_f(visible_b[0])} à {_f(visible_b[1])} MAD selon les bornes de la "
            f"surface, du prix de reprise et du durcissement ; le coût sur l'ouvrage le "
            f"plus contraint va de {_f(pire['total_bornes_MAD'][0])} à "
            f"{_f(pire['total_bornes_MAD'][1])} MAD, et ses bornes de retard sont "
            "mesurées en rejouant le réseau aux deux bornes de l'immobilisation, non "
            "déduites par une règle de trois. Ce qui ne bouge pas quand on balaie les "
            "fourchettes, c'est l'ÉCART entre les régimes : l'ouvrage contraint reste "
            "plus cher d'un ordre de grandeur, et la part visible reste trompeuse. On "
            "publie donc le rapport, pas le montant."),
        "ce_qui_n_est_PAS_chiffre_ici": (
            "Ni la perte de confiance de la maîtrise d'œuvre, qui durcit tous les visas "
            "suivants et qu'on ne sait pas chiffrer, ni le risque que la reprise soit "
            "elle-même refusée, ni les pénalités de retard — elles relèvent du contrat "
            "et du module de réception. Un coût de non-conformité publié est toujours "
            "une borne basse."),
        "_le_piege": (
            "Chiffrer une non-conformité une fois pour toutes. Le même défaut, la même "
            "surface et la même méthode de reprise donnent ici un coût dans un rapport "
            f"de {_f(pire['total_MAD'] / moindre['total_MAD'])} selon l'ouvrage touché. "
            "Négocier le prix de la reprise au dirham près pendant que l'attente court à "
            "l'autre bout du tableau est la version courante de cette erreur."),
    }


# le réseau de référence ne dépend pas de la non-conformité : le recalculer à chaque
# appel triplait le coût des bornes sans changer un chiffre.
_BASE: dict = {}


def _reseau_de_base(d: dict) -> dict:
    cle = id(d)
    if cle not in _BASE:
        tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json")
                        .read_text(encoding="utf-8"))
        q = pln.quantites_chantier(d, d["planning"])
        t0 = pln.durees_chantier(d, d["planning"], q,
                                 tv["planning_plancher"]["duree_totale_j"])
        res0 = pln.voie_A_parcours(pln.planning_avec_fenetres(d, t0)["taches"])
        _BASE[cle] = {"d": d, "t0": t0, "res0": res0, "ref": res0["duree"],
                      "marges": pln.marges(res0, t0, pln.liens_resolus(d, t0))}
    return _BASE[cle]


def impact_sur_le_planning(d: dict, jours: float) -> dict:
    """Le décalage se MESURE en rejouant le réseau (D-040), il ne se suppose pas.

    Et il se modélise comme un RETARD DE DÉBUT, pas comme un allongement de durée : une
    reprise ne rend pas la tâche plus longue, elle la fait commencer plus tard. La
    distinction n'est pas cosmétique — ajouter des jours ouvrés à la durée d'une tâche
    sous consignation, dont la durée est un nombre de PLAGES, est une erreur d'unité, et
    c'est exactement celle que la passe adversariale de B7c avait déjà trouvée.

    Les trois tâches comparées ne sont pas choisies à la main, et surtout elles ne sont
    plus choisies par l'ordre d'insertion d'un dictionnaire : six tâches ont ici une
    marge nulle, et une version précédente en prenait deux « au hasard » du tri stable
    de Python. Le départage est déclaré — à marge égale, la tâche qui porte le plus
    d'heures de main-d'œuvre — et il est publié avec le résultat.
    """
    b = _reseau_de_base(d)
    t0, res0, ref, mg = b["t0"], b["res0"], b["ref"], b["marges"]
    soumises = set(d["planning"]["contraintes_exploitation"]["taches_soumises"])
    pl = json.loads((RACINE / "calc" / "sorties" / "planification.json")
                    .read_text(encoding="utf-8"))
    heures = pl["heures_de_main_oeuvre_par_tache"]

    reels = [i for i in mg if t0[i]["duree_j"] > 0.5]

    def cle(i):
        # départage déclaré : marge croissante, puis heures de main-d'œuvre
        # décroissantes, puis ordre alphabétique. Aucune des trois clés n'est l'ordre
        # du code, et c'est tout l'objet de la correction.
        return (round(mg[i]["marge_totale_j"], 3), -heures.get(i, 0.0), i)

    sans_marge = sorted((i for i in reels if mg[i]["marge_totale_j"] < 0.01), key=cle)
    choix = []
    for i in (next((x for x in sans_marge if x in soumises), None),
              next((x for x in sans_marge if x not in soumises), None),
              max(reels, key=lambda x: (mg[x]["marge_totale_j"], heures.get(x, 0.0)))):
        if i and i not in choix:
            choix.append(i)

    out = []
    for tache in choix:
        f = pln.planning_avec_fenetres(
            d, t0, retards={tache: res0["tot"][tache][0] + jours})
        res = pln.voie_A_parcours(f["taches"])
        retard = round(max(0.0, res["duree"] - ref), 2)
        out.append({
            "tache": tache, "nom": pln.NOMS[tache],
            # `round` d'un flottant négatif infinitésimal rend « -0.0 », qui s'affiche
            # tel quel dans un tableau de planning et suggère un réseau infaisable.
            "marge_totale_j": round(mg[tache]["marge_totale_j"], 2) + 0.0,
            "heures_de_main_oeuvre": round(heures.get(tache, 0.0), 1),
            "sous_consignation": tache in soumises,
            "retard_du_chantier_j": retard,
            "amplification": round(retard / jours, 2) if jours else 0.0,
            "regime": ("amplifié par les fenêtres de consignation" if retard > jours + 0.5
                       else "transmis intégralement" if retard > 0.01
                       else "absorbé par la marge"),
        })
    periode = d["planning"]["contraintes_exploitation"][
        "periode_entre_fenetres_jours"]["valeur"]
    ampl = next((x for x in out if x["sous_consignation"]), None)
    return {
        "immobilisation_j": jours,
        "duree_de_reference_j": round(ref, 2),
        "periode_entre_fenetres_j": periode,
        "lignes": out,
        "_comment_les_trois_sont_choisies": (
            f"{len(sans_marge)} tâches de ce réseau ont une marge nulle : les prendre "
            "dans l'ordre du code aurait fait dépendre la démonstration de l'ordre d'un "
            "dictionnaire. Le départage est déclaré — à marge égale, la tâche qui porte "
            "le plus d'heures de main-d'œuvre — et on retient celle qui est sous "
            "consignation, celle qui ne l'est pas, et celle qui a le plus de marge. Les "
            "trois régimes sortent du réseau, pas du texte."),
        "lecture": (
            f"La MÊME non-conformité, {_f(jours)} jours d'immobilisation, décale le "
            "chantier de "
            + ", ".join(f"{_f(x['retard_du_chantier_j'], 1)} j sur {x['tache']}"
                        for x in out)
            + ". Ni la gravité du défaut ni la surface concernée n'y sont pour quoi que "
            "ce soit."),
        "la_regle_en_deux_temps": (
            "Deux mécanismes, et il faut les deux pour lire le tableau. La MARGE décide "
            "si le retard passe : au-delà d'elle, il est transmis ; en deçà, il est "
            "absorbé. La CONSIGNATION décide ensuite de combien il est amplifié : une "
            "tâche qui attend une fenêtre ne rate pas sa reprise, elle rate son créneau. "
            "Deux tâches de marge identique — "
            + " et ".join(x["tache"] for x in out if x["marge_totale_j"] < 0.01)
            + " — donnent ici "
            + " et ".join(f"{_f(x['retard_du_chantier_j'])} j" for x in out
                          if x["marge_totale_j"] < 0.01)
            + " : la marge seule ne suffit donc pas à hiérarchiser."),
        "_le_mecanisme_de_l_amplification": (
            (f"Le mécanisme exact, parce qu'une explication approximative est ici pire "
             f"que pas d'explication. Le levage occupe un nombre entier de PLAGES, et "
             f"les plages sont espacées de {periode} jours. Les {_f(jours)} jours "
             f"d'immobilisation ne rallongent pas le levage : ils lui font rater son "
             f"créneau, et le suivant est {periode} jours plus loin — d'où "
             f"{_f(ampl['retard_du_chantier_j'])} jours de chantier, soit "
             f"{_f(ampl['retard_du_chantier_j'] / jours, 2)} fois l'immobilisation. "
             f"Le nombre de fenêtres ratées vaut "
             f"{round(ampl['retard_du_chantier_j'] / periode)}, pas davantage : "
             "l'écrire au pluriel quand il n'y en a qu'une, ou l'inverse, suffit à "
             "rendre l'explication fausse d'un facteur deux — et c'est elle qui est "
             "censée convaincre le lecteur que le nombre n'est pas une erreur de "
             "calcul.")
            if ampl and ampl["retard_du_chantier_j"] > jours + 0.5 else
            "Aucune des tâches retenues n'est amplifiée par les fenêtres sur ce jeu de "
            "données."),
        "_consequence_de_pilotage": (
            "Deux non-conformités de même gravité technique n'ont pas la même urgence. "
            "Celle qui touche une tâche à marge nulle ET sous consignation se traite "
            "toutes affaires cessantes ; celle qui touche un ouvrage à marge large se "
            "traite bien. Un plan de contrôle qui ignore le planning met le même effort "
            "partout, donc trop peu là où il faudrait — et il le met sur les ouvrages "
            "visibles plutôt que sur les ouvrages contraints."),
    }


def quantification_du_retard(d: dict, tache: str, sondes) -> dict:
    """Sous consignation, le retard ne varie pas continument : il est QUANTIFIÉ.

    C'est le résultat le plus utile de ce module et il n'était pas prévu : on le trouve
    en sondant le réseau, pas en lisant une formule. Une tâche qui attend une fenêtre
    paie le pas entier dès la première demi-journée perdue, puis plus rien jusqu'au pas
    suivant. Le coût marginal d'un jour d'immobilisation est donc nul presque partout et
    brutal une fois par pas — ce qui est l'inverse de l'intuition que donne un Gantt.
    """
    b = _reseau_de_base(d)
    out = []
    for j in sondes:
        f = pln.planning_avec_fenetres(
            d, b["t0"], retards={tache: b["res0"]["tot"][tache][0] + j})
        out.append({
            "immobilisation_j": j,
            "retard_j": round(max(0.0, pln.voie_A_parcours(f["taches"])["duree"]
                                  - b["ref"]), 2)})
    pas = d["planning"]["contraintes_exploitation"][
        "periode_entre_fenetres_jours"]["valeur"]
    paliers = sorted({x["retard_j"] for x in out})
    return {
        "tache": tache,
        "pas_j": pas,
        "sondes": out,
        "nb_sondes": len(out),
        "paliers_observes_j": paliers,
        "nb_paliers_observes": len(paliers),
        "note": (
            f"Le réseau rejoué pour {len(out)} immobilisations différentes ne rend que "
            f"{len(paliers)} retards distincts : {', '.join(_f(x) for x in paliers)} "
            f"jours. Le pas est la période entre deux fenêtres, {pas} jours. Une "
            f"demi-journée perdue coûte déjà le pas entier ; les "
            f"{_f(pas - 0.5, 1)} jours suivants ne coûtent rien de plus. C'est pour "
            "cela qu'une non-conformité sous consignation se traite toutes affaires "
            "cessantes AVANT la fenêtre, et que se presser une fois la fenêtre ratée ne "
            "rachète rien : la vitesse ne sert qu'à ne pas franchir le pas suivant."),
        "consequence_sur_les_bornes": (
            f"Et cela règle la question des bornes du retard : entre les deux bornes "
            f"déclarées de l'immobilisation, le retard ne bouge pas d'un jour — il reste "
            f"au palier. Ce n'est donc pas l'incertitude sur la reprise qui porte "
            "l'incertitude du résultat, c'est la PÉRIODE des fenêtres, qui est une "
            "donnée de l'exploitant et non du chantier. Borner le mauvais paramètre est "
            "une façon courante de se rassurer : on balaie ce qu'on connaît."),
    }


def sensibilite_a_la_periode(d: dict, tache: str, jours: float) -> dict:
    """Le paramètre qui porte vraiment l'incertitude du retard : la période des fenêtres.

    Elle n'appartient pas au chantier — c'est l'exploitant qui l'accorde — et c'est elle
    qu'il faut négocier, six mois à l'avance, plutôt que la durée de la reprise.
    """
    import copy
    o = d["planning"]["contraintes_exploitation"]["periode_entre_fenetres_jours"]
    out = []
    for per in (o["fourchette"][0], o["valeur"], o["fourchette"][1]):
        dd = copy.deepcopy(d)
        dd["planning"]["contraintes_exploitation"][
            "periode_entre_fenetres_jours"]["valeur"] = per
        b = _reseau_de_base(dd)
        f = pln.planning_avec_fenetres(
            dd, b["t0"], retards={tache: b["res0"]["tot"][tache][0] + jours})
        out.append({
            "periode_j": per,
            "duree_de_reference_j": round(b["ref"], 2),
            "retard_j": round(max(0.0, pln.voie_A_parcours(f["taches"])["duree"]
                                  - b["ref"]), 2)})
    return {
        "tache": tache,
        "immobilisation_j": jours,
        "lignes": out,
        "note": (
            f"La même non-conformité, le même ouvrage, la même reprise : le retard va de "
            f"{_f(min(x['retard_j'] for x in out))} à "
            f"{_f(max(x['retard_j'] for x in out))} jours selon la seule période des "
            "fenêtres de consignation. Chaque ligne est MESURÉE sur un réseau rejoué "
            "avec cette période, durée de référence recalculée comprise — c'est "
            "nécessaire, car changer la période change aussi la date de fin sans "
            "non-conformité, et de bien plus que le retard : la durée de référence "
            f"passe de {_f(min(x['duree_de_reference_j'] for x in out))} à "
            f"{_f(max(x['duree_de_reference_j'] for x in out))} jours, soit "
            f"{_f(max(x['duree_de_reference_j'] for x in out) - min(x['duree_de_reference_j'] for x in out))} "
            "jours de chantier qui ne se jouent ni sur une cadence, ni sur un effectif, "
            "ni sur une méthode. Le paramètre le plus lourd de ce planning appartient à "
            "l'exploitant ferroviaire."),
    }


# ---------------------------------------------------- 3. la criticité, et son domaine
def criticite(d: dict) -> dict:
    """f × g × d sur des échelles ORDINALES : un classement, jamais une grandeur.

    C'est l'outil le plus utilisé et le plus mal lu des analyses de risques. Les trois
    notes sont des RANGS : « 4 » n'est pas « deux fois 2 », c'est « plus que 3 ». Leur
    produit se compare donc à un autre produit — il classe — mais il ne s'interprète pas
    comme une magnitude, ne s'additionne pas, ne se moyenne pas, et sa variation n'a pas
    de sens quantitatif. Dire « la criticité a baissé de 30 % » n'a aucun contenu.

    Ce qu'il faut en garder : le classement est utile, et il suffit. Ce qui ne suffit
    pas, c'est le seuil — « on traite au-dessus de 24 » dépend entièrement du choix des
    échelles, et deux équipes avec deux échelles différentes ne traiteront pas les mêmes
    risques.
    """
    r = d["qualite_hse"]["risques"]
    lignes = [{**x, "criticite": x["f"] * x["g"] * x["d"]} for x in r["liste"]]
    # Départage des ex æquo : gravité, puis NON-DÉTECTABILITÉ. Sans la troisième clé,
    # « chute de charge » (d = 2) passait devant « effondrement d'étaiement » (d = 4),
    # qui est le seul risque indétectable du tableau — l'ordre le moins défendable.
    lignes.sort(key=lambda x: (-x["criticite"], -x["g"], -x["d"]))
    for n, x in enumerate(lignes, 1):
        x["rang"] = n
    par_gravite = sorted(lignes, key=lambda x: (-x["g"], -x["f"], -x["d"]))
    desaccord = [x["risque"] for x in lignes[:3]
                 if x["risque"] not in {y["risque"] for y in par_gravite[:3]}]
    ex_aequo = [x["risque"] for x in lignes if x["criticite"] == lignes[0]["criticite"]]
    return {
        "echelle": r["echelle"],
        "lignes": lignes,
        "les_trois_premiers": [x["risque"] for x in lignes[:3]],
        "les_trois_plus_graves": [x["risque"] for x in par_gravite[:3]],
        "classements_en_desaccord": desaccord,
        "valeurs_distinctes": sorted({x["criticite"] for x in lignes}, reverse=True),
        "_ce_que_la_criticite_n_est_pas": (
            "Un produit de RANGS. « 4 » n'est pas deux fois « 2 » : c'est « plus que "
            "3 ». Le produit classe, il ne mesure pas. On ne l'additionne pas, on ne le "
            "moyenne pas, et « la criticité a baissé de 30 % » n'a aucun contenu. C'est "
            "la même faute de domaine que D-037 dénonce pour les ratios — avec une "
            "circonstance aggravante : ici le nombre a l'air d'une mesure."),
        "_le_seuil_est_arbitraire": (
            "« On traite au-dessus de 24 » dépend entièrement du choix des échelles. "
            "Deux équipes avec deux échelles différentes ne traiteront pas les mêmes "
            "risques, et aucune des deux n'aura tort. Le seuil se DÉCIDE et se "
            "consigne, il ne se déduit pas."),
        "ex_aequo_en_tete": ex_aequo,
        "nb_ex_aequo_en_tete": len(ex_aequo),
        "_ce_que_les_ex_aequo_disent": (
            f"{len(ex_aequo)} risques sur {len(lignes)} sont à égalité en tête. Ce n'est "
            "pas un défaut du tableau, c'est une propriété des échelles courtes : avec "
            "des notes de 1 à 4, le produit ne prend ici que "
            f"{len({x['criticite'] for x in lignes})} valeurs distinctes, et le "
            "classement ne discrimine pas. Un outil qui met plusieurs risques au même "
            "rang ne dit pas qu'ils sont équivalents — il dit qu'il ne sait pas les "
            "départager, et c'est alors à l'équipe de le faire, pas au tableau. Le "
            "départage retenu ici est déclaré : à criticité égale, la gravité, puis la "
            "NON-DÉTECTABILITÉ — un risque qu'on ne voit pas venir passe devant."),
        "risques_a_faible_gravite_mais_frequents": [
            x["risque"] for x in lignes if x["g"] <= 2 and x["f"] >= 3],
        "pourquoi_lire_aussi_la_gravite_seule": (
            "Un risque rare et détectable mais mortel se classe mal en criticité et se "
            "traite quand même : on n'arbitre pas une vie contre un rang. Les deux "
            "classements se lisent ensemble, et c'est leur DÉSACCORD qui est "
            "intéressant"
            + (f" — ici {', '.join(desaccord)} sort du trio de tête en criticité sans "
               "sortir de celui de la gravité." if desaccord
               else " — ici ils s'accordent sur le trio de tête, ce qui est confortable "
                    "et ne doit pas faire oublier de les comparer.")),
    }


# ---------------------------------------------------- 4. le plan de contrôle
def plan_de_controle(d: dict, pl: dict) -> dict:
    """Les cinq colonnes sans lesquelles une ligne de plan de contrôle ne se pilote pas.

    Et une sixième information, qu'on n'y met presque jamais : le DÉLAI du résultat. Un
    contrôle dont le résultat arrive à 28 jours ne protège pas l'ouvrage qu'il mesure —
    il protège les suivants. C'est une différence de nature, pas de degré, et elle
    change ce qu'on fait du résultat.
    """
    p = d["qualite_hse"]["plan_de_controle"]
    # La criticité d'un contrôle se DÉRIVE des marges du réseau : la déclarer en dur,
    # comme le faisait une version précédente, la rend fausse dès que le planning change
    # — et elle l'était (D-040).
    lignes = []
    for x in p["lignes"]:
        t = x.get("tache_arretee")
        marge = pl["durees"][t]["marge_totale_j"] if t else None
        lignes.append({**x,
                       "marge_de_la_tache_j": (round(marge, 2) + 0.0
                                               if marge is not None else None),
                       # Publier « null » dans une cellule de tableau est un defaut de
                       # rendu : un controle qui n'arrete aucune tache le dit en toutes
                       # lettres, il ne laisse pas le gabarit afficher le mot nul.
                       "tache_et_marge": (f"{t} · {round(marge, 2) + 0.0:.2f} j".replace(".", ",")
                                          if t else "aucune"),
                       "detail": x.get("detaille_par") or "—",
                       "sur_le_chemin_critique": bool(marge is not None and marge < 0.01)})
    differes = [x for x in lignes if x["delai_du_resultat_j"] > 0]
    critiques = [x for x in lignes if x["sur_le_chemin_critique"]]
    arrets = [x for x in lignes if x["point_d_arret"]]
    plus_differe = max(lignes, key=lambda x: x["delai_du_resultat_j"])
    return {
        "lignes": lignes,
        "nb_controles": len(lignes),
        "nb_immediats": len(lignes) - len(differes),
        "nb_differes": len(differes),
        "nb_sur_le_chemin_critique": len(critiques),
        "nb_points_d_arret": len(arrets),
        "heures_de_points_d_arret": round(sum(x["duree_h"] for x in arrets), 2),
        "heures_de_controle_total": round(sum(x["duree_h"] for x in lignes), 2),
        "delai_le_plus_long_j": plus_differe["delai_du_resultat_j"],
        "controle_le_plus_differe": plus_differe["controle"],
        "perimetre": p["_perimetre"],
        "qui_et_visa": p["_qui_et_visa"],
        "les_cinq_colonnes": [
            "QUI contrôle — et s'il est indépendant de celui qui exécute",
            "QUAND — avant, pendant, ou après l'opération",
            "SUR QUEL CRITÈRE — mesurable, et écrit avant le contrôle",
            "EN COMBIEN DE TEMPS le résultat arrive",
            "CE QUI SE PASSE si c'est non conforme — décidé à l'avance",
        ],
        "la_regle": (
            "Une ligne de plan de contrôle sans ces cinq colonnes ne se pilote pas : "
            "elle se coche. Et la cinquième est celle qu'on oublie — décider à froid ce "
            "qu'on fera d'une non-conformité évite de le décider à chaud, devant une "
            "toupie qui attend."),
        "controles_qui_ne_protegent_pas_leur_ouvrage": (
            f"{len(differes)} contrôles sur {len(lignes)} rendent leur résultat après "
            f"coup, dont « {plus_differe['controle']} » à "
            f"{plus_differe['delai_du_resultat_j']} jours. Ils ne protègent pas "
            "l'ouvrage qu'ils mesurent — celui-ci est déjà construit — ils protègent "
            "les SUIVANTS. D'où deux conséquences : on ne les attend pas pour avancer, "
            "et on ne les traite pas comme des points d'arrêt."),
        "_le_cout_du_point_d_arret": (
            f"{len(arrets)} des {len(lignes)} contrôles sont des points d'arrêt, pour "
            f"{_f(sum(x['duree_h'] for x in arrets), 1)} heures à prévoir au planning. "
            f"Et {len(critiques)} contrôles arrêtent une tâche à marge nulle : la durée "
            "de ceux-là est du délai, pas une formalité. Pour les autres, elle se prend "
            "sur une marge — ce qui n'est pas gratuit non plus, mais ne se paie pas le "
            "même jour. La criticité est LUE dans le réseau, elle n'est pas déclarée : "
            "elle change dès que le planning change."),
        "controles_critiques": [x["controle"] for x in critiques],
    }


# ---------------------------------------------------- 5. les déchets
def dechets(d: dict, pl: dict) -> dict:
    """Les flux, et celui qui pèse le moins mais commande le plus."""
    dd = d["qualite_hse"]["dechets"]
    emprise = d["geometrie"]["emprise_m"][0] * d["geometrie"]["emprise_m"][1]
    lignes, bornes = [], [0.0, 0.0]
    for f in dd["flux"]:
        kg = f["kg_m2"]["valeur"] * emprise
        b = _bornes(f["kg_m2"])
        bornes = [bornes[0] + b[0] * emprise / 1000, bornes[1] + b[1] * emprise / 1000]
        lignes.append({"flux": f["flux"], "kg_m2": f["kg_m2"]["valeur"],
                       "kg_m2_bornes": list(b),
                       "tonnes": round(kg / 1000, 1),
                       "valorisation_pct": f["valorisation_pct"],
                       "tonnes_valorisees": round(kg * f["valorisation_pct"] / 100000, 1)})
    total = sum(x["tonnes"] for x in lignes)
    valo = sum(x["tonnes_valorisees"] for x in lignes)
    dang = next(x for x in lignes if "dangereux" in x["flux"])
    return {
        "emprise_m2": emprise, "lignes": lignes,
        "total_tonnes": round(total, 1),
        "total_bornes_tonnes": [round(bornes[0], 1), round(bornes[1], 1)],
        "valorisees_tonnes": round(valo, 1),
        "taux_de_valorisation_pct": round(valo / total * 100, 1),
        "part_dangereuse_pct": round(dang["tonnes"] / total * 100, 2),
        "lecture": (
            f"{_f(total)} t de déchets, valorisées à {_f(valo / total * 100)} %. Les "
            f"déchets dangereux pèsent {_f(dang['tonnes'], 1)} t, soit "
            f"{_f(dang['tonnes'] / total * 100, 2)} % du total — et ils commandent "
            "toute l'organisation du tri."),
        "_bornes": (
            f"Les ratios au mètre carré sont des ordres de grandeur déclarés : le total "
            f"va de {_f(bornes[0])} à {_f(bornes[1])} t, presque un facteur quatre. Ce "
            "qui ne dépend pas des bornes, c'est le rapport entre les flux — les "
            "gravats pèsent, les dangereux commandent — et c'est la seule chose dont on "
            "se sert pour organiser une aire de tri."),
        "_dangereux": dd["_dangereux"],
    }


# ---------------------------------------------------- figures
def figures(exp: dict, nc: dict, cr: dict, de: dict) -> dict:
    return {
        # TOUTES les tâches qui ont des heures, triées par heures : la figure porte un
        # axe en heures et doit donc montrer les heures, toutes, dans leur ordre. Une
        # version précédente triait par risque pondéré, coupait à dix, et annonçait des
        # heures : deux tâches manquaient dont une plus grosse que la dernière affichée.
        "exposition": [{"libelle": f"{x['tache']}{' · nuit' if x['de_nuit'] else ''}",
                        "valeur": _trois(x["heures"])}
                       for x in exp["par_tache"]],
        # Valeurs arrondies à trois chiffres significatifs (§ 3.6) : la figure imprimait
        # « 134213,56 » pour une grandeur connue à un facteur deux près.
        "cout_nc": [{"libelle": f"{x['tache']} · {x['regime'].split()[0]}",
                     "valeur": _trois(x["total_MAD"])} for x in nc["par_ouvrage"]],
        # Libellés ENTIERS : la troncature à 46 caractères produisait « … ou une pas »,
        # en contradiction avec le tableau situé trois lignes plus haut.
        "criticite": [{"libelle": x["risque"], "valeur": x["criticite"]}
                      for x in cr["lignes"]],
        "dechets": [{"libelle": x["flux"], "valeur": _trois(x["tonnes"])}
                    for x in de["lignes"]],
    }


# ---------------------------------------------------- assemblage
def tout_calculer(d: dict) -> dict:
    pl = json.loads((RACINE / "calc" / "sorties" / "planification.json")
                    .read_text(encoding="utf-8"))
    pr = json.loads((RACINE / "calc" / "sorties" / "prix.json").read_text(encoding="utf-8"))
    exp = exposition(d, pl)
    _nc0 = d["qualite_hse"]["non_conformite"]
    jours = _nc0["delai_de_decision_j"]["valeur"] + _nc0["duree_de_reprise_j"]["valeur"]
    j_bas = _bornes(_nc0["delai_de_decision_j"])[0] + _bornes(_nc0["duree_de_reprise_j"])[0]
    j_haut = _bornes(_nc0["delai_de_decision_j"])[1] + _bornes(_nc0["duree_de_reprise_j"])[1]
    imp = impact_sur_le_planning(d, jours)
    # Les bornes du retard sont mesurées sur le réseau, aux deux bornes de
    # l'immobilisation : six rejeux de plus, et aucun nombre déduit.
    bornes = (impact_sur_le_planning(d, j_bas), impact_sur_le_planning(d, j_haut))
    nc = cout_de_la_non_conformite(d, pl, pr, imp, bornes)
    cr = criticite(d)
    de = dechets(d, pl)
    return {
        "exposition": exp,
        "comparaison_de_deux_chantiers": comparaison_de_deux_chantiers(d, 2, 12, 5, 60),
        "non_conformite": nc,
        "impact_planning": imp,
        "impact_planning_bornes": {
            "immobilisation_basse_j": j_bas,
            "immobilisation_haute_j": j_haut,
            "lignes_basses": bornes[0]["lignes"],
            "lignes_hautes": bornes[1]["lignes"],
            "note": (
                f"Le même tableau, à {_f(j_bas, 1)} puis {_f(j_haut, 1)} jours "
                "d'immobilisation, mesuré sur le réseau et non déduit. C'est la seule "
                "façon honnête de borner un retard quand des fenêtres de consignation "
                "le discrétisent : un retard qui passe d'une fenêtre à deux ne suit "
                "aucune règle de trois."),
        },
        "quantification_du_retard": quantification_du_retard(
            d, imp["lignes"][0]["tache"], (0.5, 2.5, jours, 16.0, 21.0, 25.0)),
        "sensibilite_a_la_periode": sensibilite_a_la_periode(
            d, imp["lignes"][0]["tache"], jours),
        "criticite": cr,
        "plan_de_controle": plan_de_controle(d, pl),
        "dechets": de,
        "figures": figures(exp, nc, cr, de),
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    r = tout_calculer(d)
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "qualite.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    e, n, c = r["exposition"], r["non_conformite"], r["criticite"]
    print(f"{e['heures_totales']:.0f} h dont {e['part_de_nuit_pct']} % de nuit, "
          f"qui pesent {e['part_de_nuit_dans_le_risque_pct']} % du risque "
          f"(bornes {e['part_de_nuit_dans_le_risque_bornes_pct']})")
    print(f"NC : part visible {n['part_visible_sur_un_devis_MAD']:.0f} MAD "
          f"[{n['part_visible_bornes_MAD'][0]:.0f} a "
          f"{n['part_visible_bornes_MAD'][1]:.0f}], "
          f"ecart entre regimes x{n['ecart_entre_les_regimes']}")
    for x in n["par_ouvrage"]:
        print(f"  {x['tache']:<5} marge {x['marge_totale_j']:>7.1f} j  retard "
              f"{x['retard_du_chantier_j']:>5.1f} j {str(x['retard_bornes_j']):>14}  "
              f"cout {x['total_MAD']:>9.0f} MAD "
              f"[{x['total_bornes_MAD'][0]:.0f} a {x['total_bornes_MAD'][1]:.0f}]  "
              f"{x['part_visible_pct']:>5.1f} % visible — {x['regime']}")
    print(f"criticite : 1er {c['lignes'][0]['risque'][:40]} ({c['lignes'][0]['criticite']})")
    print(f"dechets : {r['dechets']['total_tonnes']} t "
          f"{r['dechets']['total_bornes_tonnes']}, "
          f"{r['dechets']['taux_de_valorisation_pct']} % valorisees")
