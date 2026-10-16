"""Chemin critique (CPM), par DEUX algorithmes independants (§ 3.3).

    Voie A — parcours avant/arriere : dates au plus tot, dates au plus tard, marges.
             C'est la methode qu'un logiciel de planification applique.
    Voie B — enumeration exhaustive des chemins du reseau, et le plus long l'emporte.
             Impraticable sur un vrai planning (le nombre de chemins explose), mais
             exacte sur un reseau de quelques dizaines de taches, donc parfaite comme
             contre-calcul.

Les deux doivent donner EXACTEMENT la meme duree. Si elles different, l'une des deux
est fausse — et le controle ne dit PAS laquelle. L'enumeration n'est pas une reference
par nature : sa premiere version rendait 1 jour la ou la reponse etait 10, sur un
reseau a fort decalage negatif. C'est l'etalonnage, pas l'intuition, qui tranche.

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
        # borne a zero, comme la voie B : un decalage negatif important ne peut pas
        # faire demarrer une tache avant l'origine du planning
        debut = max(0.0, max([tot[p][1] + dec for p, dec in _norm(t.predecesseurs)], default=0.0))
        tot[i] = (debut, debut + t.duree)
    duree = max(f for _, f in tot.values())

    succ = {i: [] for i in ordre}
    for t in taches:
        for p, dec in _norm(t.predecesseurs):
            succ[p].append((t.id, dec))
    for i in reversed(ordre):                         # arriere : au plus tard
        t = T[i]
        # BORNE A LA FIN DE PROJET. Sans elle, une tache dont le successeur demarre tres
        # tot a cause d'un decalage negatif important se voit crediter une marge qui
        # n'existe pas : sur A(10 j) -> B(1 j) avec un decalage de -10, A recevait 9 jours
        # de marge et le chemin critique ressortait VIDE, alors que A porte a elle seule
        # la duree du projet. Aucune tache ne peut finir apres la fin du projet.
        fin = min([tard[s][0] - dec for s, dec in succ[i]] + [duree])
        tard[i] = (fin - t.duree, fin)

    marges = {i: round(tard[i][0] - tot[i][0], 6) for i in ordre}
    critiques = [i for i in ordre if abs(marges[i]) < 1e-9]
    # Deux invariants qu'un parcours juste respecte toujours : aucune marge negative, et
    # au moins une tache critique. Les violer signale une erreur de parcours, pas un
    # reseau exotique : on leve, plutot que de publier des marges fausses.
    if any(m < -1e-9 for m in marges.values()):
        raise ValueError(f"marge negative : parcours arriere incoherent — {marges}")
    if not critiques:
        raise ValueError("aucune tache critique : tout reseau en a au moins une")
    return {"duree": duree, "tot": tot, "tard": tard, "marges": marges, "critiques": critiques}


def voie_B_enumeration(taches: list[Tache]) -> dict:
    """Enumeration de tous les chemins du reseau.

    Deux corrections par rapport a une enumeration naive, toutes deux necessaires a
    la JUSTESSE et non a la performance :

    1. La fin de projet se lit a CHAQUE noeud, pas seulement aux noeuds sans
       successeur. Sur A(10 j) -> B(1 j) avec un decalage de -10, le seul chemin
       complet mesure 1 jour, alors que A finit a 10 : une enumeration qui ne
       regarde que les fins de chemin rendait 1 au lieu de 10.
    2. Une tache ne peut pas commencer avant l'origine : le debut est borne a zero.
       Sans cette borne, un decalage negatif plus grand que la duree du predecesseur
       produisait une duree negative.
    """
    T = {t.id: t for t in taches}
    succ = {t.id: [] for t in taches}
    for t in taches:
        for p, dec in _norm(t.predecesseurs):
            if p not in T:
                raise ValueError(f"predecesseur inconnu « {p} » pour la tache « {t.id} »")
            succ[p].append((t.id, dec))
    ordonner(taches)                                  # refuse un circuit avant de descendre
    departs = [t.id for t in taches if not t.predecesseurs]
    if not departs:
        raise ValueError("aucune tache de depart : le reseau est mal forme")

    meilleur, chemin_max = 0.0, []

    def descendre(i, debut, chemin):
        nonlocal meilleur, chemin_max
        debut = max(0.0, debut)                       # (2) pas de demarrage avant l'origine
        fin = debut + T[i].duree
        chemin = chemin + [i]
        if fin > meilleur:                            # (1) on lit la fin a chaque noeud
            meilleur, chemin_max = fin, chemin
        for s, dec in succ[i]:
            descendre(s, fin + dec, chemin)

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
        "verdict": "OK" if ecart <= tolerance else
                   "ECART entre les deux algorithmes — l'un des deux est faux, le controle ne dit pas lequel",
        "detail": a,
    }
