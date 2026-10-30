"""Etalonnage de calc/terrassement.py sur des cas a solution fermee (§ 3.3).

Trois objets, et tous ont une forme exacte :

1. **Le volume d'une fouille talutee.** L'aire de la section horizontale est un
   polynome de degre 2 en hauteur ; son integrale est donc exacte et calculable a la
   main. On verifie que la formule PRISMATIQUE (Simpson) la reproduit au chiffre pres —
   c'est une propriete de Simpson, exact jusqu'au degre 3 — et que la METHODE DES
   PROFILS (moyenne des aires) surestime d'exactement a.b.h3/6. La formule fausse est
   rejouee, et l'ecart mesure est compare a sa forme fermee.
2. **Le debit d'une pelle** : godet x remplissage x 3600/cycle, et la division par le
   foisonnement pour passer du terrain transporte au terrain en place.
3. **La rotation** : un cycle de camion est une somme de temps, et la flotte qui sature
   la pelle vaut cycle / temps de chargement. Deux cas degenerants figent le sens :
   trajet nul, et un seul camion.
"""
from __future__ import annotations
import json, pathlib, random, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import terrassement as te                                               # noqa: E402

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


print("=== 1. Le volume d'une fouille talutee ===")
# (a) fruit nul : le prisme droit. Les trois voies doivent coincider.
for f in (te.volume_talus_exact, te.volume_talus_prismatique, te.volume_talus_par_profils):
    cas(f"fruit nul, prisme 10 x 10 x 5 — {f.__name__}", f(10, 10, 0, 5, 2, 2), 500.0,
        1e-9, "m3")
# (b) tronc de pyramide symetrique, calcule a la main :
#     exact = LWh + (Lb + Wa)h2/2 + a.b.h3/3, avec a = b = 2 x 1 = 2
#     = 100 x 2 + (10x2 + 10x2) x 4/2 + 2 x 2 x 8/3 = 200 + 80 + 32/3 = 290,6667
cas("tronc symetrique 10 x 10, m = 1, h = 2 : integrale exacte",
    te.volume_talus_exact(10, 10, 1, 2, 2, 2), 200 + 80 + 32 / 3, 1e-9, "m3")
cas("la formule PRISMATIQUE la reproduit exactement",
    te.volume_talus_prismatique(10, 10, 1, 2, 2, 2), 200 + 80 + 32 / 3, 1e-9, "m3")
cas("la methode des PROFILS surestime : 2 x (100 + 196)/2",
    te.volume_talus_par_profils(10, 10, 1, 2, 2, 2), 296.0, 1e-9, "m3")
cas("et son erreur vaut exactement a.b.h3/6", 296.0 - (200 + 80 + 32 / 3),
    2 * 2 * 8 / 6, 1e-9, "m3")

# (c) LA PROPRIETE, sur cent geometries tirees au hasard : Simpson est exact, et
#     l'erreur des profils a toujours sa forme fermee. C'est ce que la premiere version
#     de ce module avait rate — elle publiait a.b.h3/3, le double.
rng = random.Random(20261030)
pires = {"simpson": 0.0, "profils": 0.0}
for _ in range(100):
    L, W = rng.uniform(5, 80), rng.uniform(5, 60)
    m, h = rng.uniform(0.2, 2.0), rng.uniform(1, 12)
    cL, cW = rng.choice([0, 1, 2]), rng.choice([0, 1, 2])
    ex = te.volume_talus_exact(L, W, m, h, cL, cW)
    pr = te.volume_talus_prismatique(L, W, m, h, cL, cW)
    pf = te.volume_talus_par_profils(L, W, m, h, cL, cW)
    pires["simpson"] = max(pires["simpson"], abs(pr - ex))
    pires["profils"] = max(pires["profils"],
                           abs((pf - ex) - (cL * m) * (cW * m) * h ** 3 / 6))
cas("sur 100 geometries : la formule prismatique est exacte", pires["simpson"], 0.0,
    1e-6, "m3 d'ecart maximal")
cas("sur 100 geometries : l'erreur des profils est a.b.h3/6", pires["profils"], 0.0,
    1e-6, "m3 d'ecart maximal")
# (d) invariants de sens
vrai("le volume croit avec le fruit",
     te.volume_talus_exact(40, 20, 1.5, 4.4, 2, 1)
     > te.volume_talus_exact(40, 20, 1.0, 4.4, 2, 1)
     > te.volume_talus_exact(40, 20, 0.5, 4.4, 2, 1))
vrai("le volume croit avec le nombre de cotes talutes",
     te.volume_talus_exact(40, 20, 1, 4.4, 2, 2)
     > te.volume_talus_exact(40, 20, 1, 4.4, 2, 1)
     > te.volume_talus_exact(40, 20, 1, 4.4, 0, 0))
vrai("et la methode des profils surestime TOUJOURS, jamais l'inverse",
     all(te.volume_talus_par_profils(40, 20, mm, 4.4, 2, 1)
         >= te.volume_talus_exact(40, 20, mm, 4.4, 2, 1)
         for mm in (0.0, 0.3, 0.8, 1.0, 1.5)))

print("\n=== 2. Le debit d'une pelle ===")
D = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
# cas ROND : godet 2 m3, cycle 36 s (100 cycles/h), remplissage 1, foisonnement 25 %
faux_d = json.loads(json.dumps(D))
faux_d["terrassement"]["pelle"]["godet_m3"]["valeur"] = 2.0
faux_d["terrassement"]["pelle"]["temps_de_cycle_s"]["valeur"] = 36
faux_d["terrassement"]["pelle"]["coefficient_de_remplissage"]["valeur"] = 1.0
p = te.debit_de_la_pelle(faux_d)
cas("100 cycles par heure", p["cycles_par_heure"], 100.0, 1e-9)
cas("2 m3 x 100 = 200 m3/h foisonnes", p["debit_foisonne_m3_h"], 200.0, 1e-9, "m3/h")
cas("et 160 m3/h EN PLACE, foisonnement de 25 % deduit",
    p["debit_en_place_m3_h"], 160.0, 1e-9, "m3/h")
vrai("le debit en place est toujours INFERIEUR au debit foisonne",
     p["debit_en_place_m3_h"] < p["debit_foisonne_m3_h"])
# LA FORMULE FAUSSE, rejouee : oublier le foisonnement surestime le volume en place
# de 25 %, c'est-a-dire qu'elle fait croire a une cadence qu'aucune pelle ne tient.
cas("canari : oublier le foisonnement surestime le debit en place de 25 %",
    200.0 / 160.0, 1.25, 1e-9)

print("\n=== 3. La rotation ===")
# trajet NUL : le cycle se reduit a chargement + dechargement + manoeuvre
nul = json.loads(json.dumps(faux_d))
nul["terrassement"]["depot"]["distance_km"]["valeur"] = 0.0
nul["terrassement"]["camion"]["capacite_m3"]["valeur"] = 20.0
nul["terrassement"]["camion"]["temps_de_dechargement_min"]["valeur"] = 3.0
nul["terrassement"]["camion"]["temps_de_manoeuvre_min"]["valeur"] = 4.0
pn = te.debit_de_la_pelle(nul)
r0 = te.rotation(nul, pn, 0.0)
cas("chargement de 20 m3 a 200 m3/h : 6 min", r0["temps_de_chargement_min"], 6.0, 1e-9, "min")
cas("trajet nul : cycle = 6 + 0 + 3 + 4", r0["temps_de_cycle_min"], 13.0, 1e-9, "min")
# Les sorties sont ARRONDIES (la flotte exacte au centieme, les temps au dixieme de
# minute) : les comparaisons qui les relisent portent la tolerance de cet arrondi, et
# pas une tolerance de complaisance.
cas("flotte saturante = cycle / chargement = 13/6",
    r0["flotte_qui_sature_la_pelle_exacte"], 13 / 6, 0.005, "camions")
vrai("et elle s'arrondit AU-DESSUS : on n'achete pas un tiers de camion",
     r0["flotte_qui_sature_la_pelle"] == 3)
# un seul camion : la cadence est celle de sa rotation, jamais celle de la pelle
r1 = te.rotation(nul, pn, 0.0, 1)
cas("un camion : 20 m3 par cycle de 13 min = 92,3 m3/h",
    r1["cadence_par_rotation_m3_h_foisonne"], 20 / (13 / 60), 0.05, "m3/h")
vrai("un camion ne sature pas la pelle, et c'est la rotation qui borne",
     r1["ce_qui_borne"] == "la rotation des camions"
     and r1["cadence_tenue_m3_h_foisonne"] < pn["debit_foisonne_m3_h"])
# la flotte saturante, elle, plafonne sur la pelle
rs = te.rotation(nul, pn, 0.0, r0["flotte_qui_sature_la_pelle"])
vrai("a la flotte saturante, c'est la pelle qui borne",
     rs["ce_qui_borne"] == "la pelle"
     and abs(rs["cadence_tenue_m3_h_foisonne"] - pn["debit_foisonne_m3_h"]) < 1e-9)
cas("et la pelle est alors employee a 100 %", rs["taux_d_emploi_de_la_pelle_pct"],
    100.0, 1e-9, "%")
# LA PROPRIETE : la cadence est lineaire en nombre de camions jusqu'au plafond
pentes = []
for n in (1, 2):
    pentes.append(te.rotation(nul, pn, 0.0, n)["cadence_par_rotation_m3_h_foisonne"])
cas("la cadence de rotation est proportionnelle au nombre de camions",
    pentes[1] / pentes[0], 2.0, 1e-9)
# le trajet est proportionnel a la distance
c10 = te.rotation(nul, pn, 10.0)["temps_de_trajet_aller_retour_min"]
c20 = te.rotation(nul, pn, 20.0)["temps_de_trajet_aller_retour_min"]
cas("le temps de trajet est proportionnel a la distance", c20 / c10, 2.0, 0.005)

print("\n=== 4. Le jeu REEL du projet ===")
r = te.tout_calculer(D)
g, cu = r["geometrie"], r["cubatures"]
cas("la fouille verticale du bordereau de D1 est bien le prisme L x W x h",
    cu["controle_la_fouille_verticale_est_le_prisme"]["ecart_m3"], 0.0, 0.5, "m3")
cas("le talus est la difference entre le volume talute et le prisme",
    cu["trois_voies_du_volume_talute"]["integrale_exacte_m3"]
    - g["longueur_m"] * g["largeur_m"] * g["profondeur_m"], cu["talus_m3"], 0.1, "m3")
cas("et l'erreur des profils sur CE cas vaut sa forme fermee",
    cu["trois_voies_du_volume_talute"]["ecart_profils_exact_m3"],
    cu["trois_voies_du_volume_talute"]["forme_fermee_de_l_erreur"], 0.02, "m3")
vrai("un cote au moins n'est pas talutable, et c'est ce qui fait le module",
     g["nb_cotes_blindes"] >= 1 and g["surface_de_blindage_m2"] > 0,
     f"{g['nb_cotes_blindes']} cote(s) blinde(s), {g['surface_de_blindage_m2']} m2")
vrai("le recul necessaire est le talus PLUS la banquette",
     abs(g["recul_necessaire_par_cote_m"]
         - (g["fruit"] * g["profondeur_m"] + g["banquette_m"])) < 1e-9)
vrai("la cadence declaree par D2 n'emploie pas la pelle a plein",
     r["cadence_declaree"]["taux_d_emploi_de_la_pelle_a_cette_cadence_pct"] < 60,
     f"{r['cadence_declaree']['taux_d_emploi_de_la_pelle_a_cette_cadence_pct']} %")

print()
if echecs:
    print(f"ETALONNAGE ECHOUE : {len(echecs)} cas — {', '.join(echecs[:3])}")
    sys.exit(1)
print("Etalonnage cubatures et rotations : tous les cas fermes sont verifies.")
