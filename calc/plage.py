"""Le rendement d'une plage de consignation — une grandeur, un seul endroit (D-039).

Deux modules en ont besoin et aucun ne doit la recalculer : `planification.py` (D2) pour
chiffrer la duree d'une tache sous interception, et `ferroviaire.py` (B7c) pour tout le
reste. La mettre ici evite le cycle d'import et, surtout, evite que le cours publie deux
rendements pour la meme plage.

Ce fichier ne contient que des SOUSTRACTIONS. C'est ce qui rend le resultat sur : aucune
des grandeurs ci-dessous n'est normative, aucune n'est estimee par un modele.
"""
from __future__ import annotations

POSTES_AVANT = ("prise_de_possession_h", "consignation_catenaire_h", "amenee_des_moyens_h")
POSTES_APRES = ("repli_des_moyens_h", "deconsignation_h", "marge_de_restitution_h")


def _v(d: dict) -> dict:
    f = d["ferroviaire"]["plage_travaux"]
    return {k: f[k]["valeur"] for k in f if isinstance(f[k], dict) and "valeur" in f[k]}


def rendement(d: dict, duree_plage_h: float | None = None) -> dict:
    """Ce qu'il reste d'une plage une fois payes les prealables et la restitution.

    La part fixe ne depend NI de l'effectif NI de la quantite a realiser. Deux de ses
    postes — la consignation catenaire et la deconsignation — sont tenus par l'exploitant
    et ne se negocient pas. C'est la raison pour laquelle on ne rattrape pas une plage en
    y mettant plus de monde.
    """
    v = _v(d)
    nominale = duree_plage_h if duree_plage_h is not None else v["duree_nominale_h"]
    avant = sum(v[k] for k in POSTES_AVANT)
    apres = sum(v[k] for k in POSTES_APRES)
    utile = nominale - avant - apres
    if utile <= 0:
        raise ValueError(
            f"Plage de {nominale} h : les {avant + apres:.2f} h de prealables et de "
            "restitution ne laissent aucun temps de travail. Ce n'est pas un cas "
            "d'ecole — c'est ce qui arrive quand on demande une plage trop courte pour "
            "l'operation qu'elle doit couvrir, et le seul remede est de demander "
            "autre chose, six mois a l'avance.")
    return {
        "duree_nominale_h": nominale,
        "part_fixe_h": round(avant + apres, 2),
        "avant_travail_h": round(avant, 2),
        "apres_travail_h": round(apres, 2),
        "travail_effectif_h": round(utile, 3),
        "rendement_pct": round(utile / nominale * 100, 1),
    }


def facteur_d_interception(d: dict, duree_plage_h: float | None = None,
                           heures_par_jour: float = 8.0) -> float:
    """De combien une journee de travail « normale » se dilate sous interception.

        facteur = (heures d'une journee normale / heures utiles d'une plage)
                  / (1 - abattement de cadence de nuit)

    Deux effets qui se MULTIPLIENT, et c'est la ou l'intuition se trompe : on pense
    « il reste la moitie du temps », donc deux fois plus de nuits. Le rendement du temps
    et le rendement du travail se composent.
    """
    v = _v(d)
    r = rendement(d, duree_plage_h)
    abattement = v["abattement_de_cadence_nuit_pct"] / 100.0
    return heures_par_jour / r["travail_effectif_h"] / (1 - abattement)
