"""Etalonnage de calc/synthese.py sur des cas a solution fermee (§ 3.3).

Deux objets a verifier, et tous deux ont une forme exacte :

1. **Le passage libre entre deux armatures** : une soustraction. Son etalonnage est
   trivial, et c'est precisement pourquoi il faut l'ecrire — la seule facon de se tromper
   est de soustraire le mauvais diametre, et un cas ferme le fige.
2. **La file de corps d'etat** : T(Z) = (SW + (Z-1).maxW)/Z + N.(Z-1).f. Elle a trois
   proprietes exactes — la serie pure en Z=1, le plancher quand Z tend vers l'infini, et
   la forme (N+Z-1).W/Z quand tous les corps durent autant — plus une propriete de forme :
   sans cout de frontiere elle decroit, avec cout de frontiere elle a un minimum interieur.
"""
from __future__ import annotations
import json, math, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import synthese as syn                                                   # noqa: E402

echecs = []


def cas(nom, obtenu, attendu, tol, unite=""):
    ok = abs(obtenu - attendu) <= tol
    if not ok:
        echecs.append(nom)
    print(f"  {'ok  ' if ok else 'ECHEC'} {nom} — {obtenu:.6f} contre {attendu:.6f} {unite}")


def vrai(nom, condition, detail=""):
    if not condition:
        echecs.append(nom)
    print(f"  {'ok  ' if condition else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


print("=== 1. La file de corps d'etat ===")
W = [30.0, 45.0, 30.0, 25.0, 25.0, 20.0]
# LA REFERENCE est la simulation directe : on place les taches une a une. La forme fermee
# n'est exacte que SANS cout de transition, et c'est precisement ce que ce bloc etablit.
cas("en une seule zone, la file est la SOMME des durees",
    syn.file_simulee(W, 1), sum(W), 1e-9, "j")
cas("a tres grand nombre de zones, elle tend vers le corps le plus lent",
    syn.file_simulee(W, 5000), max(W), (sum(W) - max(W)) / 5000 * 1.1, "j")
for Z in (1, 2, 3, 5, 8, 13, 21, 50):
    cas(f"sans cout de frontiere, la forme fermee egale la simulation a Z={Z}",
        syn.file_forme_fermee(W, Z), syn.file_simulee(W, Z, 0.0), 1e-9, "j")
# Tous les corps egaux : la forme classique (N + Z - 1).W / Z.
Wc, N, Z = [7.0] * 5, 5, 4
cas("a durees egales, la file vaut (N + Z - 1).W / Z",
    syn.file_forme_fermee(Wc, Z), (N + Z - 1) * 7.0 / Z, 1e-9, "j")
# INVARIANT : sans cout de frontiere, T(Z) decroit strictement.
suite = [syn.file_simulee(W, z) for z in range(1, 40)]
vrai("sans cout de frontiere, la file decroit strictement",
     all(b < a for a, b in zip(suite, suite[1:])),
     f"{suite[0]:.1f} -> {suite[-1]:.1f} j")
vrai("et elle reste toujours au-dessus du plancher",
     all(x >= max(W) - 1e-9 for x in suite))
# INVARIANT : avec un cout de frontiere, le minimum est INTERIEUR.
f = 0.4
avec = [syn.file_simulee(W, z, f) for z in range(1, 60)]
i_min = avec.index(min(avec))
vrai("avec un cout de frontiere, l'optimum est interieur",
     0 < i_min < len(avec) - 1, f"Z = {i_min + 1} zones")
# LE CAS QUI A TROUVE L'ERREUR : la formule « forme fermee + N(Z-1)f » surestime, parce
# qu'elle met sur le chemin critique des jours que les corps en attente absorbent. Ce cas
# fige l'ecart pour qu'il ne revienne pas.
fausse = syn.file_forme_fermee(W, 8) + len(W) * 7 * f
vrai("la formule « forme fermee + N(Z-1)f » surestime nettement",
     fausse > syn.file_simulee(W, 8, f) + 10,
     f"{fausse:.1f} j contre {syn.file_simulee(W, 8, f):.1f} j simules")
vrai("et elle place l'optimum bien trop tot",
     min(range(1, 60), key=lambda z: syn.file_forme_fermee(W, z) + len(W) * (z - 1) * f)
     < i_min + 1,
     "7 zones contre " + str(i_min + 1))
# Un seul corps d'etat : le decoupage ne change RIEN (hors frontieres).
cas("avec un seul corps d'etat, le decoupage ne change rien",
    syn.file_simulee([30.0], 12), 30.0, 1e-9, "j")

print("\n=== 2. Le passage libre entre deux armatures ===")
d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
fer = json.loads((RACINE / "calc" / "sorties" / "ferraillage.json")
                 .read_text(encoding="utf-8"))
pa = syn.passage_libre(d, fer)
# Forme fermee : espacement moins diametre, pour chaque endroit.
for e in pa["endroits"]:
    cas(f"{e['endroit'][:40]} : le passage est la plus PETITE dimension de la maille",
        e["passage_libre_mm"], min(e["maille_mm"]), 1e-9, "mm")
# LE CAS QUI A TROUVE L'ERREUR : prendre la plus GRANDE dimension de la maille de dalle
# faisait passer un fourreau de 160 mm la ou seul un 100 passe.
_dalle = [e for e in pa["endroits"] if e["endroit"].startswith("Dalle")][0]
vrai("prendre la plus grande dimension de la maille de dalle serait faux",
     max(_dalle["maille_mm"]) > _dalle["passage_libre_mm"] + 50,
     f"{max(_dalle['maille_mm'])} mm contre {_dalle['passage_libre_mm']} mm")
# INVARIANT : le plus gros diametre retenu passe, le suivant du catalogue ne passe pas.
dias = d["lots_techniques"]["reservations"]["diametres_courants_mm"]
for e in pa["endroits"]:
    g = e["plus_gros_diametre_qui_passe_mm"]
    if g is None:
        continue
    suivants = [x for x in dias if x > g]
    vrai(f"{e['endroit'][:40]} : le retenu passe et le suivant ne passe pas",
         g <= e["passage_libre_mm"]
         and (not suivants or suivants[0] > e["passage_libre_mm"]),
         f"{g} mm dans {e['passage_libre_mm']} mm")
# INVARIANT : un diametre qui ne passe nulle part depasse TOUS les passages libres.
for x in pa["diametres_qui_ne_passent_nulle_part_mm"]:
    vrai(f"{x} mm ne passe nulle part",
         all(x > e["passage_libre_mm"] for e in pa["endroits"]))

print("\n=== 3. Le jeu REEL du projet ===")
r = syn.tout_calculer(d)
so = r["second_oeuvre"]
cas("la file a 8 zones recolle a la simulation",
    so["duree_a_Z_zones_j"],
    syn.file_simulee([c["duree_totale_j"] for c in so["corps"]],
                     so["nb_zones_du_gros_oeuvre"], so["cout_de_frontiere_j"]),
    0.05, "j")
vrai("le module ne compare PAS sa duree a celle de D2 : les perimetres different",
     so["perimetre_de_la_decomposition_m2"] < so["perimetre_de_D2_m2"],
     f"{so['perimetre_de_la_decomposition_m2']:.0f} m2 contre "
     f"{so['perimetre_de_D2_m2']:.0f} m2")

print()
if echecs:
    print(f"ETALONNAGE ECHOUE : {len(echecs)} cas — {', '.join(echecs[:3])}")
    sys.exit(1)
print("Etalonnage synthese : tous les cas fermes sont verifies.")
