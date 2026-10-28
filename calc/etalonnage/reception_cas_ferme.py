"""Etalonnage de calc/reception.py (§ 3.3) : cas a solution fermee et invariants.

Les grandeurs de ce module sont des produits et des quotients de taux : elles ont toutes
une solution exacte, et deux d'entre elles ont un INVARIANT qui se verifie sans connaitre
le resultat — c'est la forme d'etalonnage la plus sure.

1. Le jour de bascule des penalites ne depend PAS du montant du marche. On le verifie sur
   trois marches dont les montants varient d'un facteur mille.
2. L'arbitrage retenue / caution ne depend NI de la duree NI du montant. On le verifie sur
   trois durees et trois montants.

Ce que l'etalonnage ne valide pas : les taux eux-memes, qui sont des hypotheses V3
declarees, ni les clauses, qui se lisent dans le CPS. Il valide la facon de les composer.
"""
import json, pathlib, sys, copy

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import reception as rc                                                   # noqa: E402

echecs = []


def cas(nom, obtenu, attendu, tol=1e-9, unite=""):
    ok = abs(obtenu - attendu) <= tol
    if not ok:
        echecs.append(nom)
    print(f"  {'ok  ' if ok else 'ECHEC'} {nom} — {obtenu:.6f} contre {attendu:.6f} {unite}")


def jeu(marche, plafond_pct, pour_mille, frais_jour, conv=1.0,
        taux_portage=7.0, commission=1.2, retenue_pct=7.0):
    """Jeu minimal construit a la main : la solution s'ecrit en une ligne."""
    penal_jour_ouvre = marche * pour_mille / 1000 * conv
    d = {"prix_unitaires_MAD": {"contrat": {
            "penalite_plafond_pct": {"valeur": plafond_pct},
            "penalite_retard_pour_mille_par_j": {"valeur": pour_mille},
            "cout_de_portage_annuel_pct": {"valeur": taux_portage},
            "commission_de_caution_annuelle_pct": {"valeur": commission}}}}
    pr = {"cout_du_retard": {"1": {
              "frais_de_duree_MAD": frais_jour,
              "penalites_MAD": penal_jour_ouvre,
              "penalites_plafond_MAD": marche * plafond_pct / 100}},
          "bordereau": {"prix_de_vente_MAD": marche,
                        "frais_de_duree": {"conversion": {"calendaires_par_jour_ouvre": conv}}},
          "tresorerie": {"retenue_de_garantie_finale_MAD": marche * retenue_pct / 100}}
    return d, pr


print("=== 1. Le jour de bascule : forme fermee, verifiee sur le reseau de D1 ===")
d, pr = jeu(100e6, 10, 1.0, 20000.0)
c = rc.cout_d_un_jour(d, pr)
# plafond 10 MMAD, penalite 100 000 MAD/j : 100 jours. Et 10 % / 1 pour mille = 100.
cas("bascule a 100 jours", c["jour_de_bascule_calendaire"], 100.0, 1e-6, "j")
cas("et la forme fermee donne le meme nombre",
    c["forme_fermee_calendaire"], c["jour_de_bascule_calendaire"], 1e-6, "j")

print("\n=== 2. INVARIANT : la bascule ne depend pas du montant du marche ===")
ref = None
for marche in (1e6, 100e6, 1000e6):
    d, pr = jeu(marche, 10, 1.0, 20000.0)
    j = rc.cout_d_un_jour(d, pr)["jour_de_bascule_calendaire"]
    if ref is None:
        ref = j
    cas(f"marche de {marche/1e6:.0f} MMAD : bascule inchangee", j, ref, 1e-6, "j")

print("\n=== 3. … mais elle suit les deux clauses, et dans le bon sens ===")
j_plafond_bas = rc.cout_d_un_jour(*jeu(100e6, 5, 1.0, 20000.0))["jour_de_bascule_calendaire"]
j_penalite_forte = rc.cout_d_un_jour(*jeu(100e6, 10, 2.0, 20000.0))["jour_de_bascule_calendaire"]
cas("un plafond deux fois plus bas : bascule deux fois plus tot", j_plafond_bas, 50.0, 1e-6, "j")
cas("une penalite deux fois plus forte : bascule deux fois plus tot",
    j_penalite_forte, 50.0, 1e-6, "j")

print("\n=== 4. Les deux regimes du cout d'un jour ===")
d, pr = jeu(100e6, 10, 1.0, 20000.0)
c = rc.cout_d_un_jour(d, pr)
cas("avant le plafond : frais + penalite", c["cout_sous_penalites_MAD_par_jour_ouvre"],
    20000.0 + 100000.0, 1e-6, "MAD")
cas("apres le plafond : les frais seuls", c["cout_hors_penalites_MAD_par_jour_ouvre"],
    20000.0, 1e-6, "MAD")
cas("rapport des deux regimes", c["rapport_des_deux_regimes"], 6.0, 0.05)
# La courbe cumulee doit recoller aux deux pentes, de part et d'autre de la bascule.
co = rc.courbe_du_cout(d, pr, c, pas=10, n=20)
p = {x["x"]: x["v"] * 1e6 for x in co["points"]}
cas("a 10 jours : 10 x (frais + penalite)", p[10], 10 * 120000.0, 1.0, "MAD")
cas("a 200 jours : plafond atteint, puis frais seuls",
    p[200], 200 * 20000.0 + 10e6, 1.0, "MAD")
pente_apres = (p[200] - p[190]) / 10
cas("la pente apres la bascule vaut les frais de duree", pente_apres, 20000.0, 1.0, "MAD/j")

print("\n=== 5. INVARIANT : l'arbitrage retenue / caution ignore duree ET montant ===")
ref = None
for marche in (10e6, 100e6, 1000e6):
    d, pr = jeu(marche, 10, 1.0, 20000.0)
    po = rc.portage_de_la_retenue(d, pr)
    if ref is None:
        ref = po["rapport_des_deux_couts"]
    cas(f"marche de {marche/1e6:.0f} MMAD : rapport inchange",
        po["rapport_des_deux_couts"], ref, 1e-9)
cas("et ce rapport vaut le taux de portage sur la commission", ref, 7.0 / 1.2, 0.01)
# Le rapport des COUTS MENSUELS est le meme que celui des couts annuels : la duree ne
# figure dans aucun des deux. C'est l'invariant qui permet de trancher sans la donnee ⏸.
d, pr = jeu(100e6, 10, 1.0, 20000.0)
po = rc.portage_de_la_retenue(d, pr)
cas("cout mensuel de la retenue = montant x taux / 12",
    po["cout_de_la_retenue_MAD_par_mois"], 7e6 * 7.0 / 100 / 12, 0.01, "MAD")
cas("cout mensuel de la caution = montant x commission / 12",
    po["cout_de_la_caution_MAD_par_mois"], 7e6 * 1.2 / 100 / 12, 0.01, "MAD")
cas("le rapport des deux couts mensuels est celui des deux taux",
    po["cout_de_la_retenue_MAD_par_mois"] / po["cout_de_la_caution_MAD_par_mois"],
    7.0 / 1.2, 0.001)

print("\n=== 6. Cas degeneres ===")
# Une penalite nulle : il n'y a plus de plafond a atteindre, donc pas de jour de
# bascule. Le module publie l'index comme NON DEFINI (D-042) au lieu de le poser a zero
# ou de diviser par zero.
c0 = rc.cout_d_un_jour(*jeu(100e6, 10, 0.0, 20000.0))
ok = (c0["sans_penalite"] and c0["jour_de_bascule_calendaire"] is None
      and c0["cout_sous_penalites_MAD_par_jour_ouvre"]
      == c0["cout_hors_penalites_MAD_par_jour_ouvre"] == 20000.0)
if not ok:
    echecs.append("penalite nulle mal traitee")
print(f"  {'ok  ' if ok else 'ECHEC'} sans penalite : pas de bascule, et le cout d'un "
      f"jour est constant — {c0['jour_de_bascule_calendaire']}")
# Et le cout d'un jour ne doit pas devenir negatif ni nul quand les frais sont nuls :
# un chantier sans frais de duree ne coute que sa penalite, pas rien.
c1 = rc.cout_d_un_jour(*jeu(100e6, 10, 1.0, 0.0))
cas("sans frais de duree, un jour coute la penalite seule",
    c1["cout_sous_penalites_MAD_par_jour_ouvre"], 100000.0, 1e-6, "MAD")

print("\n=== 6b. La duree de levee d'un ensemble de reserves ===")
# Forme fermee : max(heures-homme / capacite, plus long delai de tiers). Les deux termes
# se RECOUVRENT, ils ne s'additionnent pas — une famille qui attend une piece n'occupe
# personne pendant ce temps.
F = [{"nombre": 10, "_delai": 0.0}, {"nombre": 2, "_delai": 7.0}]
r1 = rc._duree_de_levee(F, 6.0, 48.0)          # 72 h-h / 48 = 1,5 j ; delai 7 j
cas("72 heures-homme a 48 par jour font 1,5 jour d'atelier", r1["jours_d_atelier"], 1.5, 1e-9, "j")
cas("mais la duree est celle du delai le plus long", r1["duree_j"], 7.0, 1e-9, "j")
ok = r1["commande_par"] == "le délai d'un tiers"
if not ok:
    echecs.append("commande_par")
print(f"  {'ok  ' if ok else 'ECHEC'} et le module dit ce qui commande — {r1['commande_par']}")
r2 = rc._duree_de_levee([{"nombre": 100, "_delai": 0.0}], 6.0, 48.0)
cas("sans delai de tiers, la duree est celle de l'atelier", r2["duree_j"], 12.5, 1e-9, "j")
# INVARIANT : doubler l'effectif ne change RIEN tant que le delai commande.
a_ = rc._duree_de_levee(F, 6.0, 48.0)["duree_j"]
b_ = rc._duree_de_levee(F, 6.0, 96.0)["duree_j"]
cas("INVARIANT : doubler la capacite ne change rien quand un tiers commande", b_, a_, 1e-9, "j")
# … mais elle change tout quand l'atelier commande.
c_ = rc._duree_de_levee([{"nombre": 100, "_delai": 0.0}], 6.0, 96.0)["duree_j"]
cas("… et la divise par deux quand l'atelier commande", c_, 6.25, 1e-9, "j")

print("\n=== 6c. Les deux regimes du cout d'un jour, et leur rapport ===")
d_, pr_ = jeu(100e6, 10, 1.0, 20000.0)
c_ = rc.cout_d_un_jour(d_, pr_)
cas("hors penalites : les frais de duree seuls",
    c_["cout_hors_penalites_MAD_par_jour_ouvre"], 20000.0, 1e-9, "MAD")
cas("sous penalites : frais + penalite",
    c_["cout_sous_penalites_MAD_par_jour_ouvre"], 120000.0, 1e-9, "MAD")
# INVARIANT : le cout APRES le plafond est le meme que celui d'AVANT le terme. Ce n'est
# pas une coincidence, c'est la definition des deux regimes — et c'est tout l'interet du
# resultat : le cout d'un jour n'est pas monotone dans le temps.
p3 = c_["les_trois_periodes"]
cas("INVARIANT : avant le terme et apres le plafond coutent la meme chose",
    p3[0]["cout_MAD_par_jour_ouvre"], p3[2]["cout_MAD_par_jour_ouvre"], 1e-9, "MAD")
ok = p3[1]["cout_MAD_par_jour_ouvre"] > p3[0]["cout_MAD_par_jour_ouvre"]
if not ok:
    echecs.append("fenetre de cherte")
print(f"  {'ok  ' if ok else 'ECHEC'} et la periode du milieu coute strictement plus — "
      f"{p3[1]['cout_MAD_par_jour_ouvre']:.0f} contre {p3[0]['cout_MAD_par_jour_ouvre']:.0f}")

print("\n=== 6d. Le DOE : deux invariants ===")
d_ = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
pr_ = json.loads((RACINE / "calc" / "sorties" / "prix.json").read_text(encoding="utf-8"))
po_ = rc.portage_de_la_retenue(d_, pr_)
dd_ = copy.deepcopy(d_)
# INVARIANT 1 : deux scenarios egaux donnent un surcout en HEURES nul — mais le portage
# du solde, lui, ne s'annule pas : il court des que le dossier est en retard.
dd_["reception"]["doe"]["heures_reconstitue"]["valeur"] = \
    dd_["reception"]["doe"]["heures_au_fil_de_l_eau"]["valeur"]
o1 = rc.doe(dd_, pr_, po_)
cas("deux scenarios egaux : surcout en heures nul", o1["surcout_en_heures_MAD"], 0.0, 1e-9, "MAD")
ok = o1["cout_de_portage_MAD"] > 0
if not ok:
    echecs.append("portage nul")
print(f"  {'ok  ' if ok else 'ECHEC'} mais le portage du solde demeure — "
      f"{o1['cout_de_portage_MAD']:.0f} MAD")
# INVARIANT 2 : un retard nul annule le portage et lui seul.
dd2 = copy.deepcopy(d_)
dd2["reception"]["doe"]["retard_du_solde_j"]["valeur"] = 0
o2 = rc.doe(dd2, pr_, po_)
cas("un retard nul annule le portage", o2["cout_de_portage_MAD"], 0.0, 1e-9, "MAD")
cas("et laisse le surcout en heures intact", o2["surcout_en_heures_MAD"],
    rc.doe(d_, pr_, po_)["surcout_en_heures_MAD"], 1e-9, "MAD")
# Le solde bloque est bien une part du MARCHE, pas la retenue de garantie.
o3 = rc.doe(d_, pr_, po_)
cas("le solde bloque est la part declaree du marche", o3["solde_bloque_MAD"],
    pr_["bordereau"]["prix_de_vente_MAD"]
    * d_["reception"]["doe"]["part_du_marche_au_decompte_definitif_pct"]["valeur"] / 100,
    0.01, "MAD")
ok = abs(o3["solde_bloque_MAD"] - po_["retenue_immobilisee_MAD"]) > 1
if not ok:
    echecs.append("solde confondu avec la retenue")
print(f"  {'ok  ' if ok else 'ECHEC'} et il differe de la retenue de garantie — "
      f"{o3['solde_bloque_MAD']:.0f} contre {po_['retenue_immobilisee_MAD']:.0f} MAD")

print("\n=== 6e. Les operations prealables ===")
op_ = rc.operations_prealables(d_)
cas("la duree totale est la somme des etapes", op_["duree_totale_j"],
    sum(x["duree_j"] for x in op_["etapes"]), 1e-9, "j")
ok = (op_["duree_bornes_j"][0] <= op_["duree_totale_j"] <= op_["duree_bornes_j"][1])
if not ok:
    echecs.append("bornes OPR")
print(f"  {'ok  ' if ok else 'ECHEC'} et ses bornes l'encadrent — {op_['duree_bornes_j']}")
# Les etapes tenues par l'entreprise n'ont pas de fourchette : leurs bornes valent leur
# valeur. Celles des tiers en ont une, et c'est d'elles que vient toute l'etendue.
etendue_tiers = sum(x["duree_bornes_j"][1] - x["duree_bornes_j"][0]
                    for x in op_["etapes"] if not x["tenue_par_l_entreprise"])
etendue_tot = op_["duree_bornes_j"][1] - op_["duree_bornes_j"][0]
cas("toute l'etendue vient des etapes tenues par des tiers", etendue_tiers, etendue_tot,
    1e-9, "j")

print("\n=== 7. Le jeu REEL du projet, recalcule a la main ===")
d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
pr = json.loads((RACINE / "calc" / "sorties" / "prix.json").read_text(encoding="utf-8"))
c = rc.cout_d_un_jour(d, pr)
_c = d["prix_unitaires_MAD"]["contrat"]
cas("bascule = plafond en % / penalite en pour-mille, x 10",
    c["jour_de_bascule_calendaire"],
    _c["penalite_plafond_pct"]["valeur"] * 10.0
    / _c["penalite_retard_pour_mille_par_j"]["valeur"], 0.05, "j calendaires")
po = rc.portage_de_la_retenue(d, pr)
cas("rapport des couts de portage",
    po["rapport_des_deux_couts"],
    _c["cout_de_portage_annuel_pct"]["valeur"]
    / _c["commission_de_caution_annuelle_pct"]["valeur"], 0.01)

print()
if echecs:
    print(f"ETALONNAGE ECHOUE : {len(echecs)} cas — {', '.join(echecs)}")
    sys.exit(1)
print("Etalonnage reception : tous les cas fermes sont verifies.")
