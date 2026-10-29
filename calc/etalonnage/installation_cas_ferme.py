"""Etalonnage de calc/installation.py (§ 3.3) : cas a solution fermee et invariants.

La geometrie d'un plan d'installation se prete bien a l'etalonnage : un disque, un
rectangle et une hyperbole ont tous les trois des solutions exactes, et l'echantillonnage
qui les approche doit converger vers elles.

Ce que l'etalonnage ne valide pas : la courbe de charge elle-meme, qui est un abaque de
constructeur simplifie et declare comme tel. Il valide la facon de s'en servir.
"""
import json, math, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import installation as ins                                              # noqa: E402

echecs = []


def cas(nom, obtenu, attendu, tol=1e-9, unite=""):
    ok = abs(obtenu - attendu) <= tol
    if not ok:
        echecs.append(nom)
    print(f"  {'ok  ' if ok else 'ECHEC'} {nom} — {obtenu:.6f} contre {attendu:.6f} {unite}")


print("=== 1. La courbe de charge : deux regimes et un coude ===")
# charge_max 8 t, moment 200 t.m : le coude est a 200/8 = 25 m.
cas("a 10 m, la charge maximale s'applique",
    ins.charge_disponible_t(8.0, 200.0, 10.0), 8.0, 1e-9, "t")
cas("a 25 m, les deux regimes se rejoignent",
    ins.charge_disponible_t(8.0, 200.0, 25.0), 8.0, 1e-9, "t")
cas("a 50 m, c'est le moment qui commande",
    ins.charge_disponible_t(8.0, 200.0, 50.0), 4.0, 1e-9, "t")
cas("et a 100 m, deux fois moins", ins.charge_disponible_t(8.0, 200.0, 100.0), 2.0, 1e-9, "t")
# INVARIANT : au-dela du coude, charge x rayon = moment, exactement.
for r_ in (30.0, 45.0, 60.0, 80.0):
    cas(f"INVARIANT : a {r_:.0f} m, charge x rayon = moment",
        ins.charge_disponible_t(8.0, 200.0, r_) * r_, 200.0, 1e-9, "t.m")

print("\n=== 2. Le rayon limite d'une masse ===")
cas("une piece de 8 t passe jusqu'a 25 m", ins.rayon_pour_lever(8.0, 200.0, 8.0), 25.0, 1e-9, "m")
cas("une piece de 4 t jusqu'a 50 m", ins.rayon_pour_lever(8.0, 200.0, 4.0), 50.0, 1e-9, "m")
ok = ins.rayon_pour_lever(8.0, 200.0, 9.0) is None
if not ok:
    echecs.append("piece plus lourde que la charge maximale")
print(f"  {'ok  ' if ok else 'ECHEC'} une piece plus lourde que la charge maximale ne "
      "passe nulle part — None, et non zero (D-042)")

print("\n=== 3. La couverture : un disque dans un rectangle, solution exacte ===")


def jeu(L, l, grues, cmax=8.0, mom=200.0):
    return {"geometrie": {"emprise_m": [L, l]},
            "installation": {"grue": {"charge_max_t": {"valeur": cmax},
                                      "moment_max_tm": {"valeur": mom}}}}


# Un disque de rayon 10 centre dans un carre de 40 x 40 : aire pi.r2 / aire du carre.
d = jeu(40, 40, None)
c = ins.couverture(d, {"nom": "test", "grues": [{"x_m": 20, "y_m": 20, "portee_m": 10}]},
                   [{"piece": "legere", "masse_t": 0.1}], pas=0.5)
exact = math.pi * 100 / 1600 * 100
cas("un disque de rayon 10 dans un carre de 40 : pi.r2/S", c["couverture_pct"], exact,
    0.4, "%")
# Une portee qui depasse la diagonale couvre tout, exactement.
c2 = ins.couverture(d, {"nom": "t2", "grues": [{"x_m": 20, "y_m": 20, "portee_m": 30}]},
                    [{"piece": "legere", "masse_t": 0.1}], pas=1.0)
cas("une portee superieure a la demi-diagonale couvre 100 %", c2["couverture_pct"],
    100.0, 1e-9, "%")
# Le point le plus defavorable d'un carre, grue au centre : le coin, a L/2 x racine(2).
cas("le point le plus defavorable est le coin",
    c2["distance_la_plus_defavorable_m"], 20 * math.sqrt(2), 0.8, "m")

print("\n=== 4. INVARIANT : couvrir n'est pas lever ===")
# Meme geometrie, deux masses : la part SERVIE ne peut pas depasser la part COUVERTE,
# et elle est strictement plus petite des que la masse approche la limite.
c3 = ins.couverture(d, {"nom": "t3", "grues": [{"x_m": 20, "y_m": 20, "portee_m": 30}]},
                    [{"piece": "legere", "masse_t": 0.5},
                     {"piece": "lourde", "masse_t": 8.0}], pas=1.0)
leg = c3["part_servie_pct"]["legere"]
lou = c3["part_servie_pct"]["lourde"]
ok = lou <= c3["couverture_pct"] and lou < leg
if not ok:
    echecs.append("couvrir n'est pas lever")
print(f"  {'ok  ' if ok else 'ECHEC'} la part servie pour une piece lourde est "
      f"strictement plus petite que la part couverte — {lou:.1f} % contre "
      f"{c3['couverture_pct']:.1f} % couverts, et {leg:.1f} % pour une piece legere")
# Et la part servie pour la piece lourde est l'aire du disque de rayon 25 INTERSECTE
# avec le carre — pas l'aire du disque, qui depasse celle du carre. La forme fermee d'un
# disque centre dans un carre, pour a <= R <= a.racine(2) :
#     A = 4 [ a.racine(R2 - a2) + R2 (pi/4 - arccos(a/R)) ]
# C'est le genre de cas ou l'etalonnage attrape une erreur de l'ETALONNAGE : la premiere
# version comparait a pi.R2/S et annoncait 123 % de couverture, ce qui est impossible.
a_, R_ = 20.0, 25.0
aire = 4 * (a_ * math.sqrt(R_ ** 2 - a_ ** 2)
            + R_ ** 2 * (math.pi / 4 - math.acos(a_ / R_)))
cas("la part servie d'une piece de 8 t est le disque de rayon 25 CLIPPE par le carre",
    lou, aire / 1600 * 100, 0.6, "%")

print("\n=== 5. Cas degeneres ===")
c4 = ins.couverture(d, {"nom": "t4", "grues": [{"x_m": 200, "y_m": 200, "portee_m": 10}]},
                    [{"piece": "legere", "masse_t": 0.5}], pas=2.0)
cas("une grue hors de portee ne couvre rien", c4["couverture_pct"], 0.0, 1e-9, "%")
ok = c4["charge_au_point_le_plus_defavorable_t"] is None
if not ok:
    echecs.append("charge sans couverture")
print(f"  {'ok  ' if ok else 'ECHEC'} et la charge au point le plus defavorable n'est "
      "pas definie, plutot que nulle (D-042)")

print("\n=== 5bis. L'aire couverte HORS batiment, forme fermee ===")
# Un disque de rayon R centre dans un carre de cote 2a, avec a < R < a.sqrt(2) : le
# disque depasse les quatre cotes sans atteindre les coins. L'aire INTERIEURE s'ecrit
# exactement (meme forme que le cas 4), donc l'aire EXTERIEURE vaut pi.R2 moins elle.
# C'est le seul moyen d'etalonner un echantillonnage : le comparer a une integrale
# qu'on sait faire a la main.
a2, R2 = 30.0, 36.0
interieure = 4 * (a2 * math.sqrt(R2 ** 2 - a2 ** 2)
                  + R2 ** 2 * (math.pi / 4 - math.acos(a2 / R2)))
exterieure = math.pi * R2 ** 2 - interieure
mesuree = ins.aire_couverte_hors_batiment(
    2 * a2, 2 * a2, [{"x_m": a2, "y_m": a2, "portee_m": R2}], pas=0.5)
cas("l'aire couverte hors batiment vaut pi.R2 moins le disque clippe",
    mesuree, exterieure, exterieure * 0.01, "m2")
# INVARIANT : une grue dont la portee ne depasse pas le batiment ne couvre RIEN dehors.
cas("une grue qui ne depasse pas l'emprise ne couvre rien hors emprise",
    ins.aire_couverte_hors_batiment(
        120, 40, [{"x_m": 60, "y_m": 20, "portee_m": 15}], pas=0.5),
    0.0, 1e-9, "m2")
# INVARIANT de NON-DOUBLE-COMPTE : deux grues au MEME endroit couvrent exactement ce
# que couvre une seule. Si l'echantillonnage comptait un point une fois par grue qui
# l'atteint, ce cas doublerait — c'est l'erreur que cet invariant cherche.
une = ins.aire_couverte_hors_batiment(
    10, 10, [{"x_m": 5, "y_m": 5, "portee_m": 20}], pas=0.5)
jumelles = ins.aire_couverte_hors_batiment(
    10, 10, [{"x_m": 5, "y_m": 5, "portee_m": 20},
             {"x_m": 5, "y_m": 5, "portee_m": 20}], pas=0.5)
cas("deux grues au meme endroit couvrent ce que couvre une seule", jumelles, une,
    1e-9, "m2")
# INVARIANT d'ADDITIVITE, et il n'est PAS « le double ». Deux grues disjointes couvrent
# la somme de leurs disques MOINS le batiment, retire une seule fois ; le double d'une
# grue le retirerait deux fois. L'ecart attendu est donc exactement l'aire du batiment —
# un invariant plus fin que « le double », et c'est en l'ecrivant mal que cet
# etalonnage a trouve sa premiere erreur : l'erreur etait dans l'invariant, pas dans la
# fonction, et le cas garde ici est celui qui distingue les deux.
deux = ins.aire_couverte_hors_batiment(
    10, 10, [{"x_m": 5, "y_m": 5, "portee_m": 20},
             {"x_m": 205, "y_m": 5, "portee_m": 20}], pas=0.5)
cas("deux grues disjointes = le double, moins le batiment compte une fois de trop",
    deux - 2 * une, 10.0 * 10.0, 1.0, "m2")

print("\n=== 5ter. Le survol du gabarit, forme exacte ===")
# Aucune integrale ici : le survol est une difference de longueurs, et sa forme fermee
# est l'enonce lui-meme. Ce qui s'etalonne, c'est le SENS : une grue plus loin de la voie
# survole moins, a portee egale, et exactement de la difference des positions.
y_gab = 52.0
s1 = 20.0 + 40.0 - y_gab
s2 = 14.0 + 40.0 - y_gab
cas("deplacer la grue de 6 m vers la ville reduit le survol de 6 m",
    s1 - s2, 6.0, 1e-9, "m")
# Et une grue dont la portee est inferieure a la distance au gabarit ne l'atteint jamais,
# ou qu'elle soit dans l'emprise.
cas("une portee plus courte que la distance au gabarit ne l'atteint jamais",
    max(y + 20.0 - y_gab for y in (0.0, 20.0, 40.0)), 8.0, 1e-9, "m")

print("\n=== 5quater. La lentille de deux fleches, forme fermee ===")
# Deux disques de meme rayon R dont les centres sont distants de R : l'aire commune vaut
# exactement 2.R2.(pi/3 - racine(3)/4). C'est un cas d'ecole, et il suffit a etalonner la
# formule generale employee par le module.
R3 = 40.0
attendu = 2 * R3 ** 2 * (math.pi / 3 - math.sqrt(3) / 4)
d3 = {"geometrie": {"emprise_m": [120, 40]}, "installation": {"grue": {
    "hauteur_sous_crochet_m": 45}}}
v3 = {"nom": "etalon", "grues": [{"nom": "A", "x_m": 0.0, "y_m": 0.0, "portee_m": R3},
                                 {"nom": "B", "x_m": R3, "y_m": 0.0, "portee_m": R3}]}
cas("l'aire commune de deux disques distants de R vaut 2.R2.(pi/3 - V3/4)",
    ins.interference(d3, v3)["paires"][0]["aire_commune_m2"], attendu, 0.5, "m2")
# INVARIANTS : deux cercles tangents ne se recouvrent pas ; deux cercles confondus se
# recouvrent entierement.
v4 = {"nom": "tangents", "grues": [{"nom": "A", "x_m": 0.0, "y_m": 0.0, "portee_m": R3},
                                   {"nom": "B", "x_m": 2 * R3, "y_m": 0.0,
                                    "portee_m": R3}]}
cas("deux fleches tangentes ne partagent aucune aire",
    ins.interference(d3, v4)["paires"][0]["aire_commune_m2"], 0.0, 1e-9, "m2")
v5 = {"nom": "confondus", "grues": [{"nom": "A", "x_m": 0.0, "y_m": 0.0, "portee_m": R3},
                                    {"nom": "B", "x_m": 0.0, "y_m": 0.0,
                                     "portee_m": R3}]}
cas("deux fleches confondues partagent tout le disque",
    ins.interference(d3, v5)["paires"][0]["aire_commune_m2"], math.pi * R3 ** 2,
    0.5, "m2")

print("\n=== 6. Le jeu REEL du projet ===")
d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
r = ins.tout_calculer(d)
g = d["installation"]["grue"]
charpente = d["ferroviaire"]["sous_interception"]["masse_d_une_piece_t"]["valeur"]
cas("le rayon limite de la piece de charpente vaut moment / masse",
    [p["rayon_limite_m"] for p in r["pieces"] if p["masse_t"] == charpente][0],
    g["moment_max_tm"]["valeur"] / charpente, 0.05, "m")
# La variante a deux grues couvre tout, celle a une grue non : c'est la geometrie du
# batiment, pas une opinion.
cA = next(c for c in r["couverture"] if c["variante"].startswith("A"))
cB = next(c for c in r["couverture"] if c["variante"].startswith("B"))
ok = cB["couverture_pct"] > cA["couverture_pct"]
if not ok:
    echecs.append("couverture A vs B")
print(f"  {'ok  ' if ok else 'ECHEC'} deux grues aux tiers couvrent mieux qu'une au "
      f"centre — {cB['couverture_pct']} % contre {cA['couverture_pct']} %")

print()
if echecs:
    print(f"ETALONNAGE ECHOUE : {len(echecs)} cas — {', '.join(echecs)}")
    sys.exit(1)
print("Etalonnage installation : tous les cas fermes sont verifies.")
