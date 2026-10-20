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
                           prochaine_fenetre, etalement_sous_fenetres, marges,
                           liens_resolus, planning_avec_fenetres, segments_de_travail,
                           conflits_de_grue, effectifs_par_tache)  # noqa: E402

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
    # Ce controle-ci etait vrai par construction : il comparait det["debut"] au point
    # fixe de prochaine_fenetre, c'est-a-dire a lui-meme. Il n'a pas vu que le reseau
    # faisait demarrer la tache ailleurs. On compare desormais les DEUX dates publiees,
    # celle du reseau et celle de la fenetre, qui differaient de 17,5 jours.
    verifie(f"{cle} : la date de debut DU RESEAU est celle de la fenetre",
            abs(r["durees"][cle]["debut_j"] - det["debut"]) < 1e-6,
            f"reseau {r['durees'][cle]['debut_j']} contre fenetre {det['debut']}")
    _prem = ce["premiere_fenetre_jour"]["valeur"]
    verifie(f"{cle} : cette date est bien un multiple de periode apres la premiere fenetre",
            abs((det["debut"] - _prem) % per) < 1e-6 or det["debut"] == _prem,
            f"debut {det['debut']}, premiere {_prem}, periode {per}")
    verifie(f"{cle} : l'attente se mesure contre le reseau NU, pas contre le reseau contraint",
            abs(det["attente_avant_premiere_fenetre_j"]
                - (det["debut"] - det["debut_du_reseau_nu"])) < 0.02,
            f"{det['attente_avant_premiere_fenetre_j']} j")

# canari de ce controle : en decalant la phase des fenetres d'un jour, la date de debut
# publiee ne peut plus etre une fenetre. Si rien ne sonne, le controle ne controle rien.
import copy as _copy
_d2 = _copy.deepcopy(d)
_d2["planning"]["contraintes_exploitation"]["premiere_fenetre_jour"]["valeur"] += 1
_f2 = planning_avec_fenetres(_d2, t)
_ok = all(abs(_f2["detail_fenetres"][c]["debut"] - r["consignations"][c]["debut"]) > 1e-9
          for c in ce["taches_soumises"])
verifie("canari : decaler la phase des fenetres deplace bien les dates de debut", _ok,
        "sinon la contrainte n'est pas appliquee")

# canari n 2 : si la contrainte n'etait pas honoree, le projet serait plus court. On le
# mesure en rejouant le reseau SANS au_plus_tot, comme le faisait la version fausse.
_lr = liens_resolus(d, t)
_etale = {i: r["durees"][i]["duree_etalee_j"] for i in NOMS}
_faux = voie_A_parcours([Tache(i, NOMS[i], _etale[i], _lr[i]) for i in NOMS])
verifie("canari : ignorer la contrainte de fenetre RACCOURCIT le projet — c'etait le bloquant B1",
        _faux["duree"] < r["reseau"]["duree_avec_fenetres_j"] - 1,
        f"{_faux['duree']:.2f} j sans la contrainte contre "
        f"{r['reseau']['duree_avec_fenetres_j']} j avec")

verifie("les fenetres allongent le projet, et le module le chiffre",
        r["reseau"]["duree_avec_fenetres_j"] > r["reseau"]["duree_sans_contrainte_j"],
        f"{r['reseau']['duree_sans_contrainte_j']} -> {r['reseau']['duree_avec_fenetres_j']} j")

# canari : sans contrainte d'exploitation, le projet doit retomber sur le reseau nu
_sans = etalement_sous_fenetres(5.0, 10.0, 1e9, 1e9, 0.0)
verifie("une fenetre infinie ne produit aucun etalement",
        abs(_sans["etalement_j"] - 5.0) < 1e-6, f"{_sans['etalement_j']} j")

# --- le chemin critique passe-t-il par les durees IMPOSEES ? c'est la these du module
chemin = r["reseau"]["chemin_critique"]
crit = set(r["reseau"]["contre_calcul_cpm"]["taches_critiques_voie_A"])
imposees = {i for i, v in t.items() if v["famille"] == "imposee"}
verifie("le chemin critique traverse bien des durees imposees",
        bool(set(chemin) & imposees), f"imposees sur le chemin : {sorted(set(chemin) & imposees)}")
# Ce que le module publie maintenant : la fenetre COUPE le chemin critique. En amont de
# la tache epinglee, tout porte de la marge ; en aval, tout est critique.
_cc = r["reseau"]["contre_calcul_cpm"]
verifie("une tache est bien epinglee par sa fenetre",
        bool(_cc["taches_contraintes_actives"]), f"{_cc['taches_contraintes_actives']}")
verifie("l'aval de l'epingle est entierement critique", _cc["aval_entierement_critique"],
        f"{_cc['chemin_en_aval_de_la_contrainte']}")
_amont = chemin[:chemin.index(_cc["chemin_en_aval_de_la_contrainte"][0])]
verifie("et l'amont, lui, porte de la marge — ce n'est pas une anomalie",
        all(r["durees"][i]["marge_totale_j"] > 1e-9 for i in _amont),
        f"{len(_amont)} taches amont, marge minimale "
        f"{min([r['durees'][i]['marge_totale_j'] for i in _amont], default=0)} j")

# --- la decomposition du chemin DOIT sommer a la duree du projet. Recalculee ici.
dec = r["decomposition_du_chemin"]
_somme = sum(dec["postes_j"].values())
verifie("la decomposition du chemin somme a la duree du reseau",
        abs(_somme - r["reseau"]["duree_avec_fenetres_j"]) < 0.05,
        f"{_somme:.2f} contre {r['reseau']['duree_avec_fenetres_j']} j")
_hors = (dec["postes_j"]["imposee"] + dec["postes_j"]["attente_de_fenetre"]
         + dec["postes_j"]["immobilisation_entre_fenetres"]) / r["reseau"]["duree_avec_fenetres_j"] * 100
verifie("la part hors d'atteinte des moyens est recalculee ici",
        abs(dec["part_que_les_effectifs_ne_touchent_pas_pct"] - _hors) < 0.15,
        f"{dec['part_que_les_effectifs_ne_touchent_pas_pct']} % contre {_hors:.1f} %")

# --- recouvrements : aucun ne peut depasser la duree de son predecesseur (bloquant B7)
_lr0 = liens_resolus(d, t)
_viol = [(i, p, dec_) for i, ls in _lr0.items() for p, dec_ in ls
         if abs(dec_) > t[p]["duree_j"] + 1e-9]
verifie("aucun recouvrement ne depasse la duree de son predecesseur", not _viol, f"{_viol}")
_debuts = {i: r["durees"][i]["debut_j"] for i in NOMS}
_avant = [(p, i) for i, ls in _lr0.items() for p, _ in ls if _debuts[i] < _debuts[p] - 1e-6]
verifie("aucun successeur ne demarre avant son predecesseur", not _avant, f"{_avant}")

# --- securite (S4c) : le soutenement precede l'approfondissement, et le reseau le fait
verifie("le soutenement demarre avant la fouille", _debuts["SOUT"] <= _debuts["FOUI"] + 1e-9,
        f"SOUT j{_debuts['SOUT']} contre FOUI j{_debuts['FOUI']}")
verifie("et il ne se termine pas apres elle en laissant la fouille ouverte non soutenue",
        r["durees"]["SOUT"]["debut_j"] < r["durees"]["FOUI"]["debut_j"]
        or r["durees"]["SOUT"]["fin_j"] <= r["durees"]["FOUI"]["fin_j"] + 1e-9,
        "la paroi avance devant l'excavation")

# --- grue : le conflit se compte en CONFLIT, pas en moyenne (bloquant B8)
gr = r["grue"]
_seg = segments_de_travail(t, voie_A_parcours(
    [Tache(i, NOMS[i], r["durees"][i]["duree_etalee_j"], _lr0[i],
           r["consignations"]["_debuts_imposes"].get(i, 0.0)) for i in NOMS]),
    {c: r["consignations"][c] for c in ce["taches_soumises"]}, ce)
_eff = effectifs_par_tache(d, pl, t)
_gr2 = conflits_de_grue(d, _seg, _eff)
verifie("le profil de grue est recalcule ici", _gr2["demande_maximale"] == gr["demande_maximale"],
        f"{_gr2['demande_maximale']} contre {gr['demande_maximale']}")
verifie("le conflit de grue est publie, pas masque",
        gr["conflit"] == (gr["demande_maximale"] > gr["parc_de_grues"]),
        f"demande {gr['demande_maximale']} pour un parc de {gr['parc_de_grues']}")
verifie("canari : l'occupation moyenne ne suffirait pas a detecter ce conflit",
        gr["occupation_moyenne_pct"] <= 100 and gr["conflit"],
        f"moyenne {gr['occupation_moyenne_pct']} % et pourtant "
        f"{gr['nb_jours_en_conflit']} jours en conflit")

# --- marges : totale >= libre, et le chemin critique est a marge nulle
res = voie_A_parcours([Tache(i, NOMS[i], r["durees"][i]["duree_etalee_j"], _lr0[i],
                             r["consignations"]["_debuts_imposes"].get(i, 0.0)) for i in NOMS])
mg = marges(res, t, _lr0)
verifie("toute marge libre est inferieure ou egale a la marge totale",
        all(v["marge_libre_j"] <= v["marge_totale_j"] + 1e-6 for v in mg.values()))
verifie("les taches a marge nulle sont exactement celles que le module publie comme critiques",
        all(abs(mg[i]["marge_totale_j"]) < 1e-6 for i in crit)
        and {i for i, v in mg.items() if abs(v["marge_totale_j"]) < 1e-6} == crit,
        f"{len(crit)} taches critiques")
verifie("et au moins une tache non critique porte de la marge",
        any(v["marge_totale_j"] > 1 for i, v in mg.items() if i not in crit))

# --- lissage : la pointe baisse, la fin ne bouge pas, et la marge se paie
lis = r["ressources"]
verifie("le lissage abaisse la pointe", lis["pointe_apres"] <= lis["pointe_avant"],
        f"{lis['pointe_avant']} -> {lis['pointe_apres']}")
verifie("il consomme de la marge, et le module le dit",
        lis["marge_totale_consommee_j"] > 0, f"{lis['marge_totale_consommee_j']} j")
verifie("les deux histogrammes ont EXACTEMENT la meme surface : on deplace, on ne supprime pas",
        sum(lis["histogramme_brut"]) == sum(lis["histogramme_lisse"]),
        f"{sum(lis['histogramme_brut'])} contre {sum(lis['histogramme_lisse'])} jours-hommes")
verifie("chaque decalage du lissage tient dans la marge LIBRE de sa tache",
        all(v <= r["durees"][i]["marge_libre_j"] + 1e-9
            for i, v in lis["decalages_utilises_j"].items()),
        f"{lis['decalages_utilises_j']}")
# la moyenne bouge, et le module ne pretend pas le contraire : son denominateur change
verifie("la moyenne change parce que le nombre de jours travailles change",
        (lis["moyenne_avant"] == lis["moyenne_apres"])
        == (lis["jours_travailles_avant"] == lis["jours_travailles_apres"]),
        f"{lis['moyenne_avant']} -> {lis['moyenne_apres']} sur "
        f"{lis['jours_travailles_avant']} -> {lis['jours_travailles_apres']} jours")

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
# L'assiette est le TRAVAIL, pas l'etalement (bloquant B5) : on recalcule les deux et on
# verifie que le total publie est bien le premier, strictement inferieur au second.
_travail = sum(_eff[i] * t[i]["duree_j"] for i in NOMS)
_etalement = sum(_eff[i] * r["durees"][i]["duree_etalee_j"] for i in NOMS)
verifie("l'assiette de la courbe en S est le travail, et il est inferieur a l'etalement",
        _travail < _etalement - 1,
        f"{_travail:.0f} jours-hommes de travail contre {_etalement:.0f} d'etalement")
verifie("l'histogramme porte la meme assiette que la courbe en S",
        abs(sum(lis["histogramme_brut"]) - _travail) / _travail < 0.03,
        f"{sum(lis['histogramme_brut'])} contre {_travail:.0f}")
# les paliers sont CHERCHES par le calcul, et chacun porte une cause nommee
pal = r["paliers_de_la_courbe_s"]
verifie("la courbe en S porte des paliers, et ils sont identifies", len(pal) >= 2, f"{len(pal)}")
verifie("chaque palier porte une cause nommee",
        all("aucune cause" not in x["cause"] for x in pal),
        "; ".join(x["cause"].split(" — ")[0] for x in pal))
verifie("et chaque palier est vraiment plat sur la courbe publiee",
        all(max(p["prevu"] for p in cs if x["de_j"] <= p["j"] <= x["a_j"])
            - min(p["prevu"] for p in cs if x["de_j"] <= p["j"] <= x["a_j"]) < 0.3 for x in pal),
        f"{len(pal)} paliers verifies")

print(f"\n{len(echecs)} echec(s)." if echecs else "\nTests de la planification : tous verts.")
sys.exit(1 if echecs else 0)
