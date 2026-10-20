"""Tests de la bibliotheque de planification (module D2).

Meme discipline que pour la tranche verticale : chaque controle est double d'une erreur
injectee qui DOIT le faire sonner, et les valeurs cles sont recalculees ICI, a partir de
data/, sans appeler le code de production.
"""
from __future__ import annotations
import json, math, sys, pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
from cpm import Tache, voie_A_parcours                                  # noqa: E402
from planification import (quantites_chantier, durees_chantier, reseau, LIENS, NOMS,
                           prochaine_fenetre, etalement_sous_fenetres, marges)  # noqa: E402

echecs = []


def verifie(nom, condition, detail=""):
    if not condition:
        echecs.append(nom)
    print(f"  {'ok   ' if condition else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
pl = d["planning"]
tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json").read_text(encoding="utf-8"))
r = json.loads((RACINE / "calc" / "sorties" / "planification.json").read_text(encoding="utf-8"))
q = quantites_chantier(d, pl)
t = durees_chantier(d, pl, q, tv["planning_plancher"]["duree_totale_j"])

# --- quantites : recalculees depuis la GEOMETRIE, sans appeler quantites_chantier
g = d["geometrie"]
L, l = g["emprise_m"]
_nt = next(n for n in g["niveaux"] if n["nom"] == "niveau technique")
_decap = L * l * pl["ratios_quantites_V3"]["decapage_m"]["valeur"]
verifie("decapage recalcule depuis l'emprise", abs(q["decapage_m3"] - _decap) < 0.5,
        f"{q['decapage_m3']} contre {_decap:.1f} m3")
_npot = 4 * (g["nb_travees_longitudinales"] + 1)
verifie("nombre de poteaux = 4 files x (travees + 1)", q["n_poteaux"] == _npot, f"{q['n_poteaux']}")
verifie("la charpente est deduite de la surface couverte, pas posee",
        abs(q["charpente_t"] - L * l * pl["ratios_quantites_V3"]["charpente_kg_m2"]["valeur"] / 1000) < 0.5,
        f"{q['charpente_t']} t")

# --- les trois familles de durees existent, et aucune tache n'en manque
fam = {v["famille"] for v in t.values()}
verifie("les trois familles de duree sont presentes", fam == {"calculee", "imposee", "declaree"},
        ", ".join(sorted(fam)))
verifie("chaque tache du reseau porte une duree", set(t) == set(NOMS),
        f"{len(t)} durees pour {len(NOMS)} taches")
verifie("aucune duree negative ou nulle sans raison",
        all(v["duree_j"] > 0 for v in t.values()))

# --- durees calculees : recalculees a la main, une par une
c, e = pl["cadences_chantier_V3"], pl["effectifs_chantier_V3"]
for cle, attendu in (
    ("TERR", q["decapage_m3"] / (c["terrassement_m3_j_atelier"]["valeur"] * e["ateliers_terrassement"])),
    ("FOND", q["n_poteaux"] / (c["semelle_unites_j_atelier"]["valeur"] * e["ateliers_fondations"])),
    ("POTR", q["n_poteaux"] / (c["poteau_unites_j_atelier"]["valeur"] * e["ateliers_poteaux"])),
    ("COUV", q["surface_couverture_m2"] / (c["couverture_m2_j_atelier"]["valeur"] * e["ateliers_couverture"])),
):
    verifie(f"duree recalculee : {cle}", abs(t[cle]["duree_j"] - attendu) < 0.02,
            f"{t[cle]['duree_j']} contre {attendu:.2f} j")

# --- la duree du plancher de mezzanine VIENT du module TV, elle n'est pas resaisie
verifie("la mezzanine reprend la duree calculee par le module TV",
        abs(t["MEZZ"]["duree_j"] - tv["planning_plancher"]["duree_totale_j"]) < 0.01,
        f"{t['MEZZ']['duree_j']} j")

# --- le contre-calcul CPM, et le second contre-calcul hors CPM
cc = r["reseau"]["contre_calcul_cpm"]
verifie("les deux algorithmes CPM coincident",
        abs(cc["voie_A_parcours_avant_arriere_j"] - cc["voie_B_enumeration_des_chemins_j"]) < 1e-6,
        f"A {cc['voie_A_parcours_avant_arriere_j']} / B {cc['voie_B_enumeration_des_chemins_j']}")
cc2 = r["reseau"]["contre_calcul_chemin"]
verifie("la somme du chemin critique rend la duree du projet", cc2["verdict"] == "OK",
        f"{cc2['somme_du_chemin_j']} contre {cc2['duree_du_reseau_j']}")

# --- les fenetres de consignation : etalement recalcule a la main
ce = pl["contraintes_exploitation"]
fen, per = ce["fenetre_jours"]["valeur"], ce["periode_entre_fenetres_jours"]["valeur"]
for cle in ce["taches_soumises"]:
    det = r["consignations"][cle]
    n_att = max(1, math.ceil(round(det["duree_de_travail_j"] / fen, 6)))
    verifie(f"{cle} : nombre de fenetres recalcule", det["nb_fenetres"] == n_att,
            f"{det['nb_fenetres']} contre {n_att}")
    reste = det["duree_de_travail_j"] - (n_att - 1) * fen
    verifie(f"{cle} : etalement = (n-1) x periode + reste",
            abs(det["etalement_j"] - ((n_att - 1) * per + reste)) < 0.02,
            f"{det['etalement_j']} j")
    verifie(f"{cle} : le debut tombe sur une fenetre",
            abs(det["debut"] - prochaine_fenetre(det["debut"], ce["premiere_fenetre_jour"], per)) < 1e-6,
            f"debut {det['debut']}")

verifie("les fenetres allongent le projet, et le module le chiffre",
        r["reseau"]["duree_avec_fenetres_j"] > r["reseau"]["duree_sans_contrainte_j"],
        f"{r['reseau']['duree_sans_contrainte_j']} -> {r['reseau']['duree_avec_fenetres_j']} j")

# canari : sans contrainte d'exploitation, le projet doit retomber sur le reseau nu
_sans = etalement_sous_fenetres(5.0, 10.0, 1e9, 1e9, 0.0)
verifie("une fenetre infinie ne produit aucun etalement",
        abs(_sans["etalement_j"] - 5.0) < 1e-6, f"{_sans['etalement_j']} j")

# --- le chemin critique passe-t-il par les durees IMPOSEES ? c'est la these du module
crit = set(r["reseau"]["chemin_critique"])
imposees = {i for i, v in t.items() if v["famille"] == "imposee"}
verifie("le chemin critique traverse bien des durees imposees",
        bool(crit & imposees), f"imposees critiques : {sorted(crit & imposees)}")
verifie("et le gros oeuvre, lui, n'y est pas",
        not ({"TERR", "FOUI", "FOND", "RADT", "MEZZ"} & crit),
        "c'est le resultat contre-intuitif que le module publie")
_part = r["familles"]["part_imposee_du_chemin_pct"]
_calc = sum(t[i]["duree_j"] for i in imposees & crit) / r["reseau"]["duree_avec_fenetres_j"] * 100
verifie("la part imposee du chemin est recalculee ici", abs(_part - _calc) < 0.2,
        f"{_part} % contre {_calc:.1f} %")

# --- marges : totale >= libre, et le chemin critique est a marge nulle
res = voie_A_parcours([Tache(i, NOMS[i], r["durees"][i]["duree_etalee_j"], LIENS[i]) for i in NOMS])
mg = marges(res, t)
verifie("toute marge libre est inferieure ou egale a la marge totale",
        all(v["marge_libre_j"] <= v["marge_totale_j"] + 1e-6 for v in mg.values()))
verifie("les taches critiques ont une marge totale nulle",
        all(abs(mg[i]["marge_totale_j"]) < 1e-6 for i in crit), f"{len(crit)} taches critiques")
verifie("et au moins une tache non critique porte de la marge",
        any(v["marge_totale_j"] > 1 for i, v in mg.items() if i not in crit))

# --- lissage : la pointe baisse, la fin ne bouge pas, et la marge se paie
lis = r["ressources"]
verifie("le lissage abaisse la pointe", lis["pointe_apres"] <= lis["pointe_avant"],
        f"{lis['pointe_avant']} -> {lis['pointe_apres']}")
verifie("il consomme de la marge, et le module le dit",
        lis["marge_totale_consommee_j"] > 0, f"{lis['marge_totale_consommee_j']} j")
verifie("les deux histogrammes ont la meme surface : on deplace, on ne supprime pas",
        abs(sum(lis["histogramme_brut"]) - sum(lis["histogramme_lisse"])) <= 2,
        f"{sum(lis['histogramme_brut'])} contre {sum(lis['histogramme_lisse'])} jours-hommes")

# --- calendrier : les intemperies allongent, et la conversion est recalculee
cal = r["calendrier"]
_inter = pl["calendrier"]["jours_non_ouvres_par_mois_intemperies"]["valeur"]
_facteur = 21.7 / (21.7 - _inter)
verifie("le facteur d'intemperies est recalcule ici", abs(cal["facteur_intemperies"] - _facteur) < 0.001,
        f"{cal['facteur_intemperies']}")
verifie("la fin avec alea est posterieure a la fin sans alea",
        cal["fin_avec_alea"] > cal["fin_sans_alea"],
        f"{cal['fin_sans_alea']} -> {cal['fin_avec_alea']}")

# --- courbe en S : monotone, part de zero, finit a cent
cs = r["figures"]["courbe_s"]
verifie("la courbe en S part de zero", abs(cs[0]["prevu"]) < 0.01)
verifie("elle est croissante", all(b["prevu"] >= a["prevu"] - 0.01 for a, b in zip(cs, cs[1:])))
verifie("et elle atteint 100 % a la fin", cs[-1]["prevu"] > 98, f"{cs[-1]['prevu']} %")

print(f"\n{len(echecs)} echec(s)." if echecs else "\nTests de la planification : tous verts.")
sys.exit(1 if echecs else 0)
