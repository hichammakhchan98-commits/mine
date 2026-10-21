"""Etat d'avancement d'un chantier a une date : planifie, constate, declare.

Ce module est a part, et pour une raison precise : le module des PRIX (D1) et celui du
SUIVI (D4) en ont tous deux besoin. Si chacun calculait le sien, la situation deposee et
le visa qui la controle porteraient sur deux tableaux differents — exactement le genre
d'incoherence entre modules que la chaine de donnees du cours existe pour empecher.
"""
from __future__ import annotations


def avancement_planifie(segments: dict, durees: dict, j: float) -> dict:
    """Avancement de chaque tache a la date j, DERIVE DU RESEAU.

    Pas un prorata du temps ecoule sur la duree totale du chantier : la fraction de
    chaque tache est lue sur ses propres segments de travail. Une tache consignee qui
    attend sa fenetre n'avance pas pendant l'attente, et une tache qui n'a pas commence
    est a zero — pas a « un septieme », comme un prorata global le dirait.

    C'est la lecon des quinze bloquants de la tranche verticale, appliquee a l'echelle
    du chantier : une grandeur d'etat se derive, elle ne se repartit pas.
    """
    out = {}
    for i, segs in segments.items():
        fait = sum(max(0.0, min(j, b) - a) for a, b in segs)
        total = sum(b - a for a, b in segs)
        out[i] = round(fait / total * 100, 2) if total > 1e-9 else (
            100.0 if durees[i]["debut_j"] <= j else 0.0)
    return out


def _clamp(x, lo=0.0, hi=100.0):
    return max(lo, min(hi, x))


def trois_etats(d: dict, planifie: dict) -> dict:
    """Planifie, constate, declare : trois tableaux, et deux ecarts qui ne se traitent
    pas de la meme facon.

    - planifie -> constate : la DERIVE du chantier. Elle se pilote (moyens, sequence,
      relance d'un fournisseur).
    - constate -> declare : l'ECART DE DECLARATION. Il ne se pilote pas, il se vise.
      C'est le travail de la maitrise d'oeuvre, et il n'a rien a voir avec le premier.

    Les confondre conduit a l'erreur la plus frequente du suivi : viser une situation
    sur ce que l'entreprise declare, puis s'etonner que l'avancement « reparte en
    arriere » au mois suivant.
    """
    sv = d["suivi_chantier"]
    constate, declare = {}, {}
    for i, p in planifie.items():
        c = _clamp(p + sv["ecarts_constates_pts"].get(i, 0))
        constate[i] = round(c, 2)
        declare[i] = round(_clamp(c + sv["optimisme_declare_pts"].get(i, 0)), 2)
    return {"planifie": planifie, "constate": constate, "declare": declare}


