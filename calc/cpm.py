"""Chemin critique (CPM), par DEUX algorithmes independants (§ 3.3).

    Voie A — parcours avant/arriere : dates au plus tot, dates au plus tard, marges.
             C'est la methode qu'un logiciel de planification applique.
    Voie B — enumeration exhaustive des chemins du reseau, et le plus long l'emporte.
             Impraticable sur un vrai planning (le nombre de chemins explose), mais
             exacte sur un reseau de quelques dizaines de taches, donc parfaite comme
             contre-calcul.

Les deux doivent donner EXACTEMENT la meme duree. Si elles different, c'est le
parcours avant/arriere qui est faux : l'enumeration, elle, ne peut pas se tromper.

Conventions : taches a duree fixe, liens fin-debut, decalage (`decalage`) possible
et negatif autorise (recouvrement). Unite : le jour ouvre.
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Tache:
    id: str
    nom: str
    duree: float
    predecesseurs: list = field(default_factory=list)   # [(id, decalage)] ou [id]


def _norm(preds):
    out = []
    for p in preds:
        out.append(p if isinstance(p, tuple) else (p, 0.0))
    return out


def ordonner(taches: list[Tache]) -> list[str]:
    """Tri topologique. Leve si le reseau contient un circuit."""
    restants = {t.id: {p for p, _ in _norm(t.predecesseurs)} for t in taches}
    ordre = []
    while restants:
        libres = sorted(i for i, p in restants.items() if not (p - set(ordre)))
        if not libres:
            raise ValueError(f"circuit dans le reseau : {sorted(restants)}")
        ordre.extend(libres)
        for i in libres:
            del restants[i]
    return ordre


def voie_A_parcours(taches: list[Tache]) -> dict:
    """Parcours avant puis arriere."""
    T = {t.id: t for t in taches}
    for t in taches:
        for p, _ in _norm(t.predecesseurs):
            if p not in T:
                raise ValueError(f"predecesseur inconnu « {p} » pour la tache « {t.id} »")
    ordre = ordonner(taches)

    tot, tard = {}, {}
    for i in ordre:                                   # avant : au plus tot
        t = T[i]
        debut = max([tot[p][1] + dec for p, dec in _norm(t.predecesseurs)], default=0.0)
        tot[i] = (debut, debut + t.duree)
    duree = max(f for _, f in tot.values())

    succ = {i: [] for i in ordre}
    for t in taches:
        for p, dec in _norm(t.predecesseurs):
            succ[p].append((t.id, dec))
    for i in reversed(ordre):                         # arriere : au plus tard
        t = T[i]
        fin = min([tard[s][0] - dec for s, dec in succ[i]], default=duree)
        tard[i] = (fin - t.duree, fin)

    marges = {i: round(tard[i][0] - tot[i][0], 6) for i in ordre}
    critiques = [i for i in ordre if abs(marges[i]) < 1e-9]
    return {"duree": duree, "tot": tot, "tard": tard, "marges": marges, "critiques": critiques}


def voie_B_enumeration(taches: list[Tache]) -> dict:
    """Enumeration de tous les chemins, du debut a la fin du reseau."""
    T = {t.id: t for t in taches}
    succ = {t.id: [] for t in taches}
    for t in taches:
        for p, dec in _norm(t.predecesseurs):
            succ[p].append((t.id, dec))
    departs = [t.id for t in taches if not t.predecesseurs]

    meilleur, chemin_max = -1.0, []

    def descendre(i, longueur, chemin):
        nonlocal meilleur, chemin_max
        longueur += T[i].duree
        chemin = chemin + [i]
        if not succ[i]:
            if longueur > meilleur:
                meilleur, chemin_max = longueur, chemin
            return
        for s, dec in succ[i]:
            descendre(s, longueur + dec, chemin)

    for dep in departs:
        descendre(dep, 0.0, [])
    return {"duree": meilleur, "chemin": chemin_max}


def contre_calcul(taches: list[Tache], tolerance: float = 1e-9) -> dict:
    a = voie_A_parcours(taches)
    b = voie_B_enumeration(taches)
    ecart = abs(a["duree"] - b["duree"])
    return {
        "voie_A_parcours_avant_arriere_j": round(a["duree"], 3),
        "voie_B_enumeration_des_chemins_j": round(b["duree"], 3),
        "ecart_j": round(ecart, 9),
        "chemin_critique": b["chemin"],
        "taches_critiques_voie_A": a["critiques"],
        "les_deux_voies_designent_le_meme_chemin":
            set(b["chemin"]) <= set(a["critiques"]),
        "verdict": "OK" if ecart <= tolerance else "ECART — le parcours avant/arriere est faux",
        "detail": a,
    }
