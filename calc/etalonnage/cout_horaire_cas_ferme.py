"""Etalonnage de calc/cout_horaire.py sur des cas a solution fermee (§ 3.3).

Quatre objets, et tous ont une forme exacte :

1. **L'amortissement lineaire** : (prix − residuelle) / annees. Trivial, et c'est
   justement pourquoi il se fige : la seule facon de se tromper est d'oublier la
   residuelle ou de diviser par la mauvaise duree.
2. **Le point d'equilibre** : h* = fixe / (location par heure − variable par heure).
   La reference n'est PAS cette formule : c'est un BALAYAGE des deux couts annuels, qui
   cherche le changement de signe sans rien savoir de l'algebre. C'est la regle D-067 —
   une formule homogene peut etre fausse, et seule une voie qui ne la connait pas le
   voit.
3. **La disponibilite d'une chaine** : le produit des disponibilites. La reference est
   une SIMULATION de matinees tirees au hasard ; on verifie aussi que la formule fausse
   que tout le monde emploie — « la chaine vaut son maillon le plus faible » —
   SURESTIME, et de combien.
4. **Le secours d'un maillon** : 1 − (1 − p)^2, exacte, et bornee par 1.
"""
from __future__ import annotations
import json, pathlib, random, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import cout_horaire as ch                                               # noqa: E402

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


# Un jeu de parametres ROND, choisi pour que chaque resultat soit calculable de tete.
PAR = {"achat": 1000000.0, "amort": 10.0, "entretien": 0.0, "financier": 0.0,
       "residuelle": 0.0, "carburant": 0.0, "gasoil": 0.0, "conducteur": 50.0,
       "prix_loc": 150.0, "_operateur_compris": True,
       "_regime_loc": "par_heure_de_service"}

print("=== 1. Amortissement et parts fixe / variable ===")
c = ch.couts_annuels(PAR, heures_par_an=1000.0, unites_facturees_par_an=1000.0)
cas("amortissement lineaire sans residuelle : 1 000 000 / 10", c["amortissement_MAD_an"],
    100000.0, 1e-6, "MAD/an")
cas("part fixe = amortissement seul quand entretien et financier sont nuls",
    c["fixe_MAD_an"], 100000.0, 1e-6, "MAD/an")
cas("part variable = le seul conducteur quand le carburant est nul",
    c["variable_MAD_h"], 50.0, 1e-9, "MAD/h")
# residuelle 20 % sur 10 ans : (1 000 000 x 0,8) / 10
cas("amortissement avec 20 % de residuelle",
    ch.couts_annuels({**PAR, "residuelle": 20.0}, 1000.0, 1000.0)["amortissement_MAD_an"],
    80000.0, 1e-6, "MAD/an")
# cout financier : capital moyen (1 000 000 + 200 000)/2 = 600 000, a 10 %
cas("cout financier sur le capital MOYEN",
    ch.couts_annuels({**PAR, "residuelle": 20.0, "financier": 10.0}, 1000.0,
                     1000.0)["cout_financier_MAD_an"], 60000.0, 1e-6, "MAD/an")

print("\n=== 2. Le seuil d'emploi : forme fermee contre balayage, et son SENS ===")
# Le meme engin, les memes couts, sous les TROIS regimes de location. Fixe 100 000
# MAD/an, variable 50 MAD/h, et une location calibree pour couter 150 MAD par heure de
# travail au point de fonctionnement de 1 000 h/an dans les trois cas. Les trois
# regimes donnent alors le MEME cout annuel... et trois seuils differents, dont deux de
# sens oppose. C'est tout le module en un cas ferme.
EMP_H = {"_unites_par_an_exact": 1000.0}
EMP_I = {"_unites_par_an_exact": 500.0, "duree_d_une_intervention_h": 2.0}
EMP_P = {"_unites_par_an_exact": 1000.0}

PAR_H = dict(PAR)                                        # 150 MAD / heure de service
PAR_I = {**PAR, "_regime_loc": "par_intervention", "prix_loc": 300.0}   # 300 MAD / venue de 2 h
PAR_P = {**PAR, "_regime_loc": "par_duree_de_presence", "prix_loc": 150.0}  # 150 MAD / jour de presence

for nom, par, emp in (("heure de service", PAR_H, EMP_H), ("intervention", PAR_I, EMP_I),
                      ("duree de presence", PAR_P, EMP_P)):
    c = ch.couts_annuels(par, 1000.0, ch._unites(par, emp, 1000.0))
    cas(f"regime « {nom} » : meme location annuelle au point de fonctionnement",
        c["location_MAD_an"], 150000.0, 1e-6, "MAD/an")

# (a) heure de service : L0 = 0, L1 = 150. Seuil = 100 000 / (150 - 50) = 1 000 h/an,
#     possession au-DESSUS. C'est le cas des manuels.
eq_h = ch.point_d_equilibre(PAR_H, EMP_H, 1000.0)
cas("heure de service : L0 nul", eq_h["location_fixe_L0_MAD_an"], 0.0, 1e-9, "MAD/an")
cas("heure de service : seuil = F / (L1 - v)", eq_h["seuil_h_par_an"], 1000.0, 1e-6, "h/an")
vrai("heure de service : cas classique, possession au-dessus", eq_h["cas_classique"])

# (b) intervention : L1 = 300 / 2 h = 150 MAD/h. Exactement le meme seuil que (a), et
#     c'est la propriete a figer : une location par intervention EST proportionnelle aux
#     heures, des lors que la duree d'une intervention est fixe.
eq_i = ch.point_d_equilibre(PAR_I, EMP_I, 1000.0)
cas("intervention : L1 = prix / duree d'une venue",
    eq_i["location_marginale_L1_MAD_h"], 150.0, 1e-6, "MAD/h")
cas("intervention : le MEME seuil qu'a l'heure de service",
    eq_i["seuil_h_par_an"], 1000.0, 1e-6, "h/an")
vrai("intervention : cas classique aussi", eq_i["cas_classique"])

# (c) duree de presence : L1 = 0 (operateur compris) et L0 = 150 000 MAD/an TOUT ENTIER.
#     L'ecart vaut alors (100 000 - 150 000) + 50.h : il est NEGATIF a emploi nul et
#     croit. La possession gagne AU-DESSOUS de 50 000 / 50 = 1 000 h/an. Meme nombre,
#     sens INVERSE — et c'est une coincidence de calibrage, choisie pour que le sens
#     soit la seule difference visible.
eq_p = ch.point_d_equilibre(PAR_P, EMP_P, 1000.0)
cas("duree de presence : L0 porte toute la facture",
    eq_p["location_fixe_L0_MAD_an"], 150000.0, 1e-6, "MAD/an")
cas("duree de presence : L1 nul quand l'operateur est compris",
    eq_p["location_marginale_L1_MAD_h"], 0.0, 1e-9, "MAD/h")
cas("duree de presence : seuil = (L0 - F) / v", eq_p["seuil_h_par_an"], 1000.0, 1e-6, "h/an")
vrai("duree de presence : sens INVERSE, possession au-dessous",
     not eq_p["cas_classique"] and "AU-DESSOUS" in eq_p["sens"])
vrai("et c'est bien la meme position de seuil pour les trois : seul le sens change",
     abs(eq_h["seuil_h_par_an"] - eq_p["seuil_h_par_an"]) < 1e-6)

# L'ecart est une DROITE : deux points suffisent a la determiner, et le troisieme doit
# tomber dessus. C'est le controle qui aurait du exister des la premiere version.
for nom, par, emp in (("heure de service", PAR_H, EMP_H), ("duree de presence", PAR_P, EMP_P)):
    e1 = ch.couts_annuels(par, 400.0, ch._unites(par, emp, 400.0))["ecart_MAD_an"]
    e2 = ch.couts_annuels(par, 800.0, ch._unites(par, emp, 800.0))["ecart_MAD_an"]
    e3 = ch.couts_annuels(par, 1200.0, ch._unites(par, emp, 1200.0))["ecart_MAD_an"]
    cas(f"regime « {nom} » : l'ecart est AFFINE en heures", e3 - e2, e2 - e1, 1e-6, "MAD/an")

# et a emploi nul, l'ecart vaut F - L0, sans aucune heure
cas("a emploi nul, l'ecart vaut F - L0 (heure de service)",
    ch.couts_annuels(PAR_H, 0.0, 0.0)["ecart_MAD_an"], 100000.0, 1e-6, "MAD/an")
cas("a emploi nul, l'ecart vaut F - L0 (duree de presence)",
    ch.couts_annuels(PAR_P, 0.0, ch._unites(PAR_P, EMP_P, 0.0))["ecart_MAD_an"],
    -50000.0, 1e-6, "MAD/an")


def seuil_par_balayage(par, emp, pas=0.05):
    """Reference INDEPENDANTE : on augmente l'emploi jusqu'au changement de signe.

    Cette voie ne connait pas la formule : elle appelle les deux couts annuels et
    regarde lequel est le plus grand. Si la forme fermee se trompait d'un terme — et la
    premiere version de ce module s'en trompait d'un, L0 — les deux voies divergeraient.
    C'est la regle D-067.
    """
    precedent = None
    h = pas
    while h <= 100000:
        c = ch.couts_annuels(par, h, ch._unites(par, emp, h))
        signe = c["possession_MAD_an"] - c["location_MAD_an"] < 0
        if precedent is not None and signe != precedent:
            return h - pas / 2
        precedent = signe
        h += pas
    return None


for nom, par, emp in (("heure de service", PAR_H, EMP_H), ("intervention", PAR_I, EMP_I),
                      ("duree de presence", PAR_P, EMP_P)):
    cas(f"balayage « {nom} » : meme seuil que la forme fermee",
        seuil_par_balayage(par, emp), 1000.0, 0.05, "h/an")

# marge nulle : aucun seuil
vrai("cout marginal identique des deux cotes -> aucun seuil",
     ch.point_d_equilibre({**PAR_H, "prix_loc": 50.0}, EMP_H, 1000.0)["seuil_h_par_an"]
     is None)
vrai("l'operateur non compris s'ajoute a L1 et deplace le seuil",
     ch.point_d_equilibre({**PAR_H, "_operateur_compris": False}, EMP_H,
                          1000.0)["location_marginale_L1_MAD_h"] == 200.0)

print("\n=== 3. La disponibilite d'une chaine ===")
rng = random.Random(7)


def chaine_simulee(ps, n=200000, graine=7):
    r = random.Random(graine)
    return sum(1 for _ in range(n) if all(r.random() < p for p in ps)) / n


ps = [0.5, 0.5, 0.5, 0.5]
produit = 0.5 ** 4
cas("quatre maillons a 50 % : 6,25 %", produit, 0.0625, 1e-12)
cas("simulation de 200 000 matinees", chaine_simulee(ps), produit, 0.004)
cas("un maillon parfait ne change rien", 1.0 * 0.8, 0.8, 1e-12)
# LA FORMULE FAUSSE, rejouee : « la chaine vaut son maillon le plus faible ».
faux = min(ps)
vrai("la formule fausse SURESTIME la chaine", faux > produit,
     f"{faux:.3f} contre {produit:.4f} — facteur {faux / produit:.1f}")
# Cas ferme et INDEPENDANT du projet : quatre maillons a 90 % chacun. La formule
# fausse annonce 90 %, la chaine en vaut 65,61 — 24,39 points d'ecart, exactement.
cas("quatre maillons a 90 % : la formule fausse surestime de 24,39 points",
    0.9 - 0.9 ** 4, 0.2439, 1e-9)

print("\n=== 4. Le secours d'un maillon ===")
cas("doubler un maillon a 90 % : 1 − 0,1^2", 1 - (1 - 0.9) ** 2, 0.99, 1e-12)
cas("doubler un maillon a 97 %", 1 - (1 - 0.97) ** 2, 0.9991, 1e-12)
vrai("le secours ne depasse jamais 1", all(1 - (1 - p) ** 2 <= 1 for p in
                                           (0.1, 0.5, 0.9, 0.999)))
vrai("doubler un maillon vaut mieux que ne rien faire",
     all(1 - (1 - p) ** 2 > p for p in (0.1, 0.5, 0.9)))

print("\n=== 5. La cascade de rendement ===")
cas("100 x 0,5 x 0,5 = 25", 100 * 0.5 * 0.5, 25.0, 1e-12)
vrai("une cascade de facteurs < 1 decroit strictement",
     all(a > b for a, b in zip([100, 50, 25], [50, 25, 12.5])))

print("\n=== 6. Le jeu REEL du projet ===")
d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
r = ch.tout_calculer(d)
for v in r["verdicts"]:
    fam = next(f for f in d["materiel_engins"]["familles"] if f["cle"] == v["cle"])
    par = ch.parametres(d, fam, "nominal")
    emp = r["emplois"][v["cle"]]
    h_bal = seuil_par_balayage(par, emp, pas=0.25)
    if v["equilibre"]["seuil_h_par_an"] is not None:
        cas(f"{v['cle']} : seuil par balayage", h_bal,
            v["equilibre"]["seuil_h_par_an"], 0.3, "h/an")
        vrai(f"{v['cle']} : le sens du seuil est celui de la pente de l'ecart",
             (v["equilibre"]["pente_de_l_ecart_MAD_h"] < 0)
             == v["equilibre"]["cas_classique"])
c = r["chaine_du_coulage"]
cas("chaine du coulage : forme fermee contre simulation",
    c["disponibilite_simulee_pct"], c["disponibilite_forme_fermee_pct"], 0.6, "points")
vrai("la chaine est STRICTEMENT inferieure a son maillon le plus faible",
     c["disponibilite_forme_fermee_pct"] < c["maillon_le_plus_faible_pct"])
rp = r["rendement_de_la_pompe"]
cas("cascade de la pompe : le produit des facteurs reproduit le dernier debit",
    rp["debit_catalogue_m3_h"] * rp["produit_des_facteurs"], rp["debit_recalcule_m3_h"],
    0.1, "m3/h")
vrai("le debit recalcule tient dans la fourchette que C3 declare",
     rp["dans_la_fourchette"],
     f"{rp['debit_recalcule_m3_h']} dans {rp['fourchette_declaree_par_C3']}")

print()
if echecs:
    print(f"ETALONNAGE ECHOUE : {len(echecs)} cas — {', '.join(echecs[:3])}")
    sys.exit(1)
print("Etalonnage cout horaire : tous les cas fermes sont verifies.")
