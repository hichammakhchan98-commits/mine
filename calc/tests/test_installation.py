"""Tests du module C1 — installation de chantier.

Des tests de REGLE : aucun n'epingle « deux grues » ni « couvrir n'est pas lever ». Ils
verifient que la couverture est bien bornee par la geometrie, que la part servie ne
depasse jamais la part couverte, que les grandeurs heritees sont celles des modules qui
les publient, et qu'une voie dont les bornes enjambent le seuil est declaree comme ne
tranchant pas.
"""
from __future__ import annotations
import json, math, sys, pathlib, unicodedata

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))

echecs = []


def sansaccent(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s).lower())
                   if unicodedata.category(c) != "Mn")


def dit(texte, *mots):
    t_ = sansaccent(texte)
    return all(sansaccent(m) in t_ for m in mots)


def verifie(nom, condition, detail=""):
    if not condition:
        echecs.append(nom)
    print(f"  {'ok   ' if condition else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
r = json.loads((RACINE / "calc" / "sorties" / "installation.json").read_text(encoding="utf-8"))
pl = json.loads((RACINE / "calc" / "sorties" / "planification.json").read_text(encoding="utf-8"))
pr = json.loads((RACINE / "calc" / "sorties" / "prix.json").read_text(encoding="utf-8"))
go = json.loads((RACINE / "calc" / "sorties" / "gros-oeuvre.json").read_text(encoding="utf-8"))
I = d["installation"]
G = I["grue"]

# ------------------------------------------------- 1. les pieces et la courbe de charge
print("\n--- la courbe de charge, et ce qu'elle interdit ---")
for p in r["pieces"]:
    if p["rayon_limite_m"]:
        verifie(f"{p['piece'][:30]} : rayon limite = moment / masse",
                abs(p["rayon_limite_m"]
                    - G["moment_max_tm"]["valeur"] / p["masse_t"]) < 0.05,
                f"{p['masse_t']} t -> {p['rayon_limite_m']} m")
# LA grandeur heritee : la piece de charpente n'est pas redeclaree ici (D-039).
_charpente = d["ferroviaire"]["sous_interception"]["masse_d_une_piece_t"]["valeur"]
_p = next(p for p in r["pieces"] if p["masse_t"] == _charpente)
verifie("la piece la plus lourde est LUE dans le module B7c, pas redeclaree",
        "ferroviaire" in _p["source"]
        and all(x.get("masse_t") is None for x in I["pieces_a_lever"]
                if "charpente" in x["piece"].lower()),
        f"{_charpente} t — {_p['source']}")
verifie("et c'est bien la plus lourde du chantier",
        _charpente == max(p["masse_t"] for p in r["pieces"]))
verifie("une piece plus lourde que la charge maximale ne passerait nulle part",
        all(p["rayon_limite_m"] is not None for p in r["pieces"]
            if p["masse_t"] <= G["charge_max_t"]["valeur"]))

# ------------------------------------------------- 2. la couverture
print("\n--- la couverture : ce que la geometrie permet ---")
L, l = d["geometrie"]["emprise_m"]
for c in r["couverture"]:
    verifie(f"{c['variante'][:22]} : la couverture est un pourcentage",
            0 <= c["couverture_pct"] <= 100, f"{c['couverture_pct']} %")
    # REGLE centrale : on ne peut pas SERVIR plus qu'on ne COUVRE.
    for piece, part in c["part_servie_pct"].items():
        verifie(f"{c['variante'][:14]} / {piece[:22]} : servir <= couvrir",
                part <= c["couverture_pct"] + 1e-9,
                f"{part} % servis pour {c['couverture_pct']} % couverts")
    # Et une piece plus lourde est servie sur une part plus petite, jamais l'inverse.
    parts = [c["part_servie_pct"][p["piece"]]
             for p in sorted(r["pieces"], key=lambda x: x["masse_t"])]
    verifie(f"{c['variante'][:22]} : plus la piece est lourde, moins elle est servie",
            all(a >= b - 1e-9 for a, b in zip(parts, parts[1:])),
            " >= ".join(f"{x:.0f}" for x in parts))
    if c["moment_pour_tout_servir_tm"]:
        verifie(f"{c['variante'][:22]} : le moment requis = masse la plus lourde x distance",
                abs(c["moment_pour_tout_servir_tm"]
                    - max(p["masse_t"] for p in r["pieces"])
                    * c["distance_la_plus_defavorable_m"]) < 0.2,
                f"{c['moment_pour_tout_servir_tm']} t·m")
        verifie(f"{c['variante'][:22]} : et il depasse le moment disponible",
                c["rapport_au_moment_disponible"] > 1,
                f"x{c['rapport_au_moment_disponible']}")
    verifie(f"{c['variante'][:22]} : le point le plus defavorable est dans l'emprise",
            c["point_le_plus_defavorable"] is None
            or (0 <= c["point_le_plus_defavorable"][0] <= L
                and 0 <= c["point_le_plus_defavorable"][1] <= l))
    if c["charge_au_point_le_plus_defavorable_t"]:
        import installation as ins
        verifie(f"{c['variante'][:22]} : la charge au point le plus loin suit la courbe",
                abs(c["charge_au_point_le_plus_defavorable_t"]
                    - ins.charge_disponible_t(G["charge_max_t"]["valeur"],
                                              G["moment_max_tm"]["valeur"],
                                              c["distance_la_plus_defavorable_m"])) < 0.02)
# canari qui CHERCHE : une grue dont la portee couvrirait tout ne rendrait pas la piece
# lourde levable partout pour autant. C'est la these du module, et elle doit etre
# verifiable sur un cas construit, pas seulement constatee sur le cas phare.
import installation as ins                                              # noqa: E402
_c = ins.couverture({"geometrie": {"emprise_m": [L, l]},
                     "installation": {"grue": G}},
                    {"nom": "canari", "grues": [{"x_m": L / 2, "y_m": l / 2,
                                                 "portee_m": 500}]},
                    [{"piece": "lourde", "masse_t": _charpente}], pas=2.0)
verifie("canari : une portee infinie couvre tout et ne leve pas tout",
        _c["couverture_pct"] == 100.0 and _c["part_servie_pct"]["lourde"] < 100.0,
        f"{_c['couverture_pct']} % couverts, "
        f"{_c['part_servie_pct']['lourde']} % servis")

# ------------------------------------------------- 2bis. le voisinage : la voie
print("\n--- le voisinage : le cercle de la fleche et le gabarit ---")
vo = r["voisinage"]
_dist = I["voisinage"]["distance_facade_cote_voies_au_gabarit_m"]["valeur"]
verifie("le gabarit est a la largeur de l'emprise plus la distance de site",
        abs(vo["y_du_gabarit_m"] - (l + _dist)) < 1e-9,
        f"{l} + {_dist} = {vo['y_du_gabarit_m']} m")
for x, c in zip(vo["lignes"], r["couverture"]):
    verifie(f"{x['variante'][:22]} : le survol est le depassement du cercle le plus loin",
            abs(x["survol_du_gabarit_m"]
                - max(gr["y_m"] + gr["portee_m"] - vo["y_du_gabarit_m"]
                      for gr in c["grues"])) < 0.05,
            f"{x['survol_du_gabarit_m']} m")
    verifie(f"{x['variante'][:22]} : atteindre le gabarit, c'est un survol positif",
            x["atteint_le_gabarit"] == (x["survol_du_gabarit_m"] > 0))
    verifie(f"{x['variante'][:22]} : la famille B7c suit le survol, pas l'inverse",
            (x["famille_B7c"] == "à proximité") == x["atteint_le_gabarit"],
            x["famille_B7c"])
    verifie(f"{x['variante'][:22]} : les bornes encadrent le survol",
            x["survol_bornes_m"][0] <= x["survol_du_gabarit_m"]
            <= x["survol_bornes_m"][1], f"{x['survol_bornes_m']}")
# LA regle : une variante ne compte comme « concernee quelles que soient les bornes » que
# si elle atteint le gabarit a la distance la PLUS FAVORABLE. Le test nomme la propriete.
verifie("la liste robuste est exactement celle qui tient a la borne favorable",
        vo["variantes_concernees_quelles_que_soient_les_bornes"]
        == [x["variante"] for x in vo["lignes"]
            if x["survol_bornes_m"][0] > 0],
        f"{len(vo['variantes_concernees_quelles_que_soient_les_bornes'])} sur "
        f"{len(vo['lignes'])}")
verifie("et elle est plus courte que la liste des variantes qui l'atteignent",
        len(vo["variantes_concernees_quelles_que_soient_les_bornes"])
        <= len([x for x in vo["lignes"] if x["atteint_le_gabarit"]]))
# L'axe doit aller en SENS INVERSE de la couverture, sinon le module n'enseigne rien :
# le test verifie que la variante la mieux couverte n'est pas la moins intrusive.
_mieux = max(r["couverture"], key=lambda c: c["couverture_pct"])["variante"]
_moins = min(vo["lignes"], key=lambda x: x["survol_du_gabarit_m"])["variante"]
verifie("la meilleure couverture n'est pas le moindre survol",
        _mieux != _moins, f"couverture : {_mieux[:1]} · survol : {_moins[:1]}")

# ------------------------------------------------- 2ter. les aires
print("\n--- les aires : ce qui doit etre sous la grue ---")
ai, bv = r["aires"], r["base_vie"]
verifie("la base-vie est la seule aire CALCULEE, les autres sont decidees",
        [x["aire"] for x in ai["lignes"] if x["calculee"]] == ["Base-vie"])
verifie("et sa surface est la surface INSTALLEE, modules entiers compris",
        next(x["surface_m2"] for x in ai["lignes"] if x["calculee"])
        == bv["surface_installee_m2"], f"{bv['surface_installee_m2']} m²")
verifie("le total est la somme des lignes",
        abs(ai["surface_totale_m2"]
            - sum(x["surface_m2"] for x in ai["lignes"])) < 0.05)
verifie("le besoin sous grue est la somme des aires qui le declarent",
        abs(ai["surface_a_mettre_sous_la_grue_m2"]
            - sum(x["surface_m2"] for x in ai["lignes"] if x["sous_la_grue"])) < 0.05,
        f"{ai['surface_a_mettre_sous_la_grue_m2']} m²")
verifie("le besoin ne depasse pas le total",
        ai["surface_a_mettre_sous_la_grue_m2"] <= ai["surface_totale_m2"])
verifie("le majorant exclut le batiment : il est plus petit que l'aire des cercles",
        ai["majorant_sous_grue_hors_batiment_m2"]
        < sum(math.pi * gr["portee_m"] ** 2
              for gr in next(c for c in r["couverture"]
                             if c["variante"] == ai["variante"])["grues"]),
        f"{ai['majorant_sous_grue_hors_batiment_m2']} m²")
verifie("et le module declare que c'est un MAJORANT, parcelle non connue",
        dit(ai["_pourquoi_un_majorant"], "majorant", "parcelle"))
verifie("la variante des aires est celle du plan masse, pas une autre",
        ai["variante"] == r["figures"]["plan_masse"]["variante"])

# ------------------------------------------------- 3. le debit
print("\n--- le debit : une seconde voie, et ses bornes ---")
de = r["debit"]
verifie("la capacite est cycles x heures x taux d'utilisation",
        abs(de["capacite_levages_par_jour"]
            - de["cycles_par_heure"] * de["heures_par_jour"]
            * de["taux_d_utilisation_fraction"]) < 0.05,
        f"{de['capacite_levages_par_jour']} levages/j")
# LA regle : ce qui se leve est le coffrage d'UNE ZONE, a la cadence que le planning
# tient. Ni le parc (qui est un stock), ni la cadence d'une ligne de tableau que C3
# publie comme un optimum de cout sans en faire une decision.
_tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json")
                 .read_text(encoding="utf-8"))
verifie("ce qui se leve est le coffrage d'une zone, pas le parc",
        de["coffrage_d_une_zone_m2"] == _tv["quantites"]["coffrage_m2"]
        and de["coffrage_d_une_zone_m2"] < de["parc_declare_m2"],
        f"{de['coffrage_d_une_zone_m2']} m² sur un parc de {de['parc_declare_m2']} m²")
verifie("la cadence est celle du cycle que C3 publie",
        abs(de["cadence_j"] - go["cycle"]["cadence_j"]) < 0.01,
        f"{de['cadence_j']} j")
# canari : prendre le parc au lieu de la zone doit CHANGER le nombre publie, sinon le
# test ne verifie rien.
verifie("canari : prendre le parc au lieu de la zone change la demande",
        abs(de["parc_declare_m2"] / de["cadence_j"] * 2
            / I["levages"]["surface_par_levage_m2"]["valeur"]
            - de["levages_de_coffrage_par_jour"]) > 1.0,
        f"{de['parc_declare_m2'] / de['cadence_j'] * 2 / 10:.1f} contre "
        f"{de['levages_de_coffrage_par_jour']} levages/j")
verifie("un coffrage compte DEUX levages par rotation : pose et depose",
        abs(de["levages_de_coffrage_par_jour"]
            - de["surface_manutentionnee_par_jour_m2"] * 2
            / I["levages"]["surface_par_levage_m2"]["valeur"]) < 0.1)
verifie("la surface manutentionnee par jour est la zone divisee par la cadence",
        abs(de["surface_manutentionnee_par_jour_m2"]
            - de["coffrage_d_une_zone_m2"] / de["cadence_j"]) < 0.1,
        f"{de['surface_manutentionnee_par_jour_m2']} m²/j")
verifie("la demande est le coffrage plus les divers",
        abs(de["demande_levages_par_jour"]
            - (de["levages_de_coffrage_par_jour"] + de["levages_divers_par_jour"])) < 0.1)
verifie("les bornes encadrent le taux de charge",
        de["taux_de_charge_bornes_pct"][0] <= de["taux_de_charge_pct"]
        <= de["taux_de_charge_bornes_pct"][1],
        f"{de['taux_de_charge_bornes_pct']}")
# LA regle de D-059 : la voie ne tranche pas, et il faut que ce soit vrai hypothese par
# hypothese — sinon le verdict ne tiendrait qu'a l'accumulation des extremes.
for x in de["sensibilite_une_a_une"]:
    verifie(f"sensibilite « {x['hypothese'][:24]} » : les bornes encadrent le nominal",
            x["taux_min_pct"] <= de["taux_de_charge_pct"] <= x["taux_max_pct"],
            f"{x['taux_min_pct']} - {x['taux_max_pct']} %")
verifie("chaque hypothese prise SEULE enjambe deja le seuil de 100 %",
        all(x["taux_min_pct"] < 100 < x["taux_max_pct"]
            for x in de["sensibilite_une_a_une"]),
        f"{len(de['sensibilite_une_a_une'])} hypotheses sur "
        f"{len(de['sensibilite_une_a_une'])}")
verifie("et l'enveloppe combinee est plus large que chacune",
        de["taux_de_charge_bornes_pct"][0] <= min(x["taux_min_pct"]
                                                  for x in de["sensibilite_une_a_une"])
        and de["taux_de_charge_bornes_pct"][1] >= max(x["taux_max_pct"]
                                                      for x in de["sensibilite_une_a_une"]))
verifie("la pointe double la part coffrage, et seulement elle",
        abs(de["demande_de_pointe_levages_par_jour"]
            - (de["levages_de_coffrage_par_jour"] * 2
               + de["levages_divers_par_jour"])) < 0.1
        and de["demande_de_pointe_levages_par_jour"] > de["demande_levages_par_jour"],
        f"{de['demande_de_pointe_levages_par_jour']} levages/j")
verifie("et meme deux grues ne sont pas de trop ce jour-la",
        de["taux_de_charge_de_pointe_pct"] > 100,
        f"{de['taux_de_charge_de_pointe_pct']} % d'UNE grue")
verifie("le module dit pourquoi une moyenne ne remplace pas un profil",
        dit(de["_ce_que_le_taux_de_charge_cache"], "pointe", "profil"))

# ------------------------------------------------- 4. le parc, et la voie qui ne vote pas
print("\n--- trois voies vers le parc de grues, et celles qui tranchent ---")
pa = r["parc_de_grues"]
verifie("le temps est LU chez D2, pas recalcule",
        next(v["parc"] for v in pa["voies"] if v["voie"] == "le temps")
        == pl["grue_resolution"]["parc_necessaire_si_non_resolu"],
        f"{pl['grue_resolution']['parc_necessaire_si_non_resolu']} grues chez D2")
# LA regle : une voie dont les bornes enjambent le seuil NE TRANCHE PAS. Le test nomme
# la propriete, pas la voie : si le debit devenait decisif demain, il resterait vrai.
for v in pa["voies"]:
    if v["voie"] == "le débit":
        b = de["taux_de_charge_bornes_pct"]
        verifie("le debit ne tranche que si ses bornes n'enjambent pas 100 %",
                v["tranche"] == (not (b[0] < 100 < b[1])),
                f"bornes {b} -> {'tranche' if v['tranche'] else 'ne tranche pas'}")
verifie("le parc retenu est le MAXIMUM des voies qui tranchent, jamais leur somme",
        pa["parc_retenu"] == max(v["parc"] for v in pa["voies"]
                                 if v["tranche"] and v["parc"]),
        f"{pa['parc_retenu']} grues")
verifie("et il est strictement plus petit que leur somme",
        pa["parc_retenu"] < sum(v["parc"] for v in pa["voies"] if v["parc"]),
        "les additionner donnerait "
        f"{sum(v['parc'] for v in pa['voies'] if v['parc'])} grues")
verifie("le seuil de la voie geometrie est declare, et il est strict",
        pa["seuil_de_couverture_pct"] >= 99.0
        and all(c["couverture_pct"] >= pa["seuil_de_couverture_pct"]
                for c in r["couverture"]
                if c["nb_grues"] == next(v["parc"] for v in pa["voies"]
                                         if v["voie"] == "la géométrie")),
        f"{pa['seuil_de_couverture_pct']} %")
verifie("et aucune variante sous le seuil n'est retenue par cette voie",
        all(c["couverture_pct"] < pa["seuil_de_couverture_pct"]
            or c["nb_grues"] >= next(v["parc"] for v in pa["voies"]
                                     if v["voie"] == "la géométrie")
            for c in r["couverture"]))
verifie("chaque voie dit sa duree, et elles ne sont pas toutes egales",
        all(v.get("duree") for v in pa["voies"])
        and len({v["duree"] for v in pa["voies"]}) > 1,
        " · ".join(v["duree"][:28] for v in pa["voies"]))
verifie("chaque voie dit d'ou elle vient",
        all(len(v["source"]) > 30 and len(v["pourquoi"]) > 30 for v in pa["voies"]))

# ------------------------------------------------- 5. la base-vie
print("\n--- la base-vie : dimensionnee sur la POINTE ---")
verifie("la pointe et la moyenne sont celles que D2 publie apres lissage",
        bv["effectif_de_pointe"] == pl["ressources"]["pointe_apres"]
        and abs(bv["effectif_moyen"] - pl["ressources"]["moyenne_apres"]) < 0.05,
        f"pointe {bv['effectif_de_pointe']} / moyenne {bv['effectif_moyen']}")
verifie("la surface calculee sur la pointe depasse celle calculee sur la moyenne",
        bv["surface_necessaire_m2"] > bv["surface_si_dimensionnee_sur_la_moyenne_m2"],
        f"{bv['surface_necessaire_m2']} m² contre "
        f"{bv['surface_si_dimensionnee_sur_la_moyenne_m2']} m²")
verifie("le nombre de modules est un ENTIER qui couvre la surface",
        float(bv["modules"]).is_integer()
        and bv["modules"] * I["base_vie"]["module_m2"] >= bv["surface_necessaire_m2"]
        and (bv["modules"] - 1) * I["base_vie"]["module_m2"] < bv["surface_necessaire_m2"],
        f"{bv['modules']} modules de {I['base_vie']['module_m2']} m²")
verifie("l'arrondi est publie, et il est positif",
        0 <= bv["perte_a_l_arrondi_m2"] < I["base_vie"]["module_m2"],
        f"{bv['perte_a_l_arrondi_m2']} m²")
verifie("les bornes encadrent la surface",
        bv["surface_bornes_m2"][0] <= bv["surface_necessaire_m2"]
        <= bv["surface_bornes_m2"][1], f"{bv['surface_bornes_m2']}")

# ------------------------------------------------- 6. le cout
print("\n--- la fenetre de grue : une ressource n'est pas un frais de duree ---")
fe = r["fenetre_de_grue"]
_seg = pl["segments_de_travail"]
verifie("la fenetre encadre toutes les taches servies par la grue",
        all(fe["debut_j"] - 0.05 <= _seg[t][0][0] and _seg[t][-1][1] <= fe["fin_j"] + 0.05
            for t in fe["taches_servies"]),
        f"{fe['debut_j']} -> {fe['fin_j']} j")
verifie("et ses bornes SONT celles d'une tache servie, pas une marge",
        any(abs(_seg[t][0][0] - fe["debut_j"]) < 0.05 for t in fe["taches_servies"])
        and any(abs(_seg[t][-1][1] - fe["fin_j"]) < 0.05 for t in fe["taches_servies"]))
verifie("les taches servies sont celles que D2 declare",
        fe["taches_servies"] == [t for t in pl["grue"]["taches_servies"] if t in _seg])
verifie("la fenetre est strictement plus courte que le chantier",
        fe["duree_ouvree_j"] < fe["duree_du_chantier_ouvree_j"],
        f"{fe['part_du_chantier_pct']} % du chantier")
verifie("la conversion en mois calendaires utilise le ratio de D1",
        abs(fe["duree_mois_calendaires"]
            - fe["duree_ouvree_j"] / fe["jours_ouvres_par_mois_calendaire"]) < 0.02)

print("\n--- le cout : un fixe et DEUX loyers, sur deux durees ---")
co = r["cout"]
_fd = pr["bordereau"]["frais_de_duree"]
verifie("la duree du chantier est celle que D1 publie",
        abs(co["duree_du_chantier_mois"] - _fd["duree_mois_calendaires"]) < 0.01,
        f"{co['duree_du_chantier_mois']} mois")
verifie("la duree de location des grues est celle de la fenetre, pas du chantier",
        abs(co["duree_de_location_des_grues_mois"] - fe["duree_mois_calendaires"]) < 0.02
        and co["duree_de_location_des_grues_mois"] < co["duree_du_chantier_mois"],
        f"{co['duree_de_location_des_grues_mois']} mois contre "
        f"{co['duree_du_chantier_mois']}")
verifie("le loyer des grues court sur LEUR duree",
        abs(co["loyer_des_grues_MAD"]
            - _fd["lignes"]["grue_tour_location"]["MAD_mois"] * co["nb_grues"]
            * co["duree_de_location_des_grues_mois"]) < 500,
        f"{co['loyer_des_grues_MAD']:.0f} MAD")
verifie("le loyer de la base-vie court sur celle du chantier",
        abs(co["loyer_de_la_base_vie_MAD"]
            - _fd["lignes"]["base_vie_et_fonctionnement"]["MAD_mois"]
            * co["duree_du_chantier_mois"]) < 1)
verifie("le total est le fixe plus les deux loyers",
        abs(co["total_MAD"] - (co["cout_fixe_MAD"] + co["loyer_des_grues_MAD"]
                               + co["loyer_de_la_base_vie_MAD"])) < 1)
# canari : louer les grues sur toute la duree du chantier doit CHANGER le total.
verifie("canari : louer les grues sur toute la duree change le total",
        abs(_fd["lignes"]["grue_tour_location"]["MAD_mois"] * co["nb_grues"]
            * co["duree_du_chantier_mois"] - co["loyer_des_grues_MAD"]) > 1e6,
        f"{_fd['lignes']['grue_tour_location']['MAD_mois'] * co['nb_grues'] * co['duree_du_chantier_mois']:.0f} "
        f"contre {co['loyer_des_grues_MAD']:.0f} MAD")
verifie("un mois gagne sur le gros oeuvre vaut plus qu'un mois gagne a la fin",
        co["un_mois_gagne_sur_le_gros_oeuvre_MAD"] > co["un_mois_gagne_a_la_fin_MAD"],
        f"{co['un_mois_gagne_sur_le_gros_oeuvre_MAD']} contre "
        f"{co['un_mois_gagne_a_la_fin_MAD']} MAD")
verifie("le trou se tranche en comparant deux montants, et la decision suit",
        (co["trou_decision"] == "garder")
        == (co["trou_garder_les_grues_MAD"] < co["trou_les_demonter_et_remonter_MAD"]),
        f"{co['trou_decision']} : {co['trou_garder_les_grues_MAD']:.0f} contre "
        f"{co['trou_les_demonter_et_remonter_MAD']:.0f} MAD")
verifie("le module dit que les morceaux n'obeissent pas a la meme chose",
        dit(co["_les_deux_morceaux_n_obeissent_pas_a_la_meme_chose"],
            "decision", "gros \u0153uvre", "chantier entier"))
# L'ecart avec D1 est PUBLIE, pas tu : D1 budgete une grue, C1 en retient deux.
verifie("le parc « somme des voies » est bien la somme, pas le maximum",
        co["parc_si_somme_des_voies"]
        == sum(v["parc"] for v in pa["voies"] if v["parc"])
        and co["parc_si_somme_des_voies"] > co["nb_grues"],
        f"{co['parc_si_somme_des_voies']} contre {co['nb_grues']} retenues")
verifie("et il coute strictement plus cher, en part du marche",
        co["part_du_marche_si_somme_des_voies_pct"] > co["part_du_marche_pct"],
        f"{co['part_du_marche_si_somme_des_voies_pct']} % contre "
        f"{co['part_du_marche_pct']} %")
# DEUX bases de prix : D1 en publie deux et dit laquelle on signe. Le module doit citer
# la bonne, et publier l'autre — pas choisir en silence.
verifie("la part du marche est publiee sur les DEUX bases de D1",
        abs(co["part_du_marche_pct"] - co["total_MAD"] / co["marche_de_reference_MAD"] * 100) < 0.01
        and abs(co["part_du_marche_signe_pct"]
                - co["total_MAD"] / co["marche_signe_MAD"] * 100) < 0.01
        and co["part_du_marche_signe_pct"] < co["part_du_marche_pct"],
        f"{co['part_du_marche_signe_pct']} % du prix signe contre "
        f"{co['part_du_marche_pct']} % de la reference")
verifie("le prix signe est celui que D1 declare signer",
        co["marche_signe_MAD"]
        == pr["bordereau_avec_divers"]["prix_de_vente_MAD"])
# SECONDE VOIE sur la base-vie : deux chemins independants, un ecart publie.
verifie("la base-vie a une seconde voie, et son ecart est publie",
        abs(co["loyer_base_vie_par_les_modules_MAD_par_mois"]
            - bv["modules"] * I["base_vie"]["cout_module_MAD_par_mois"]["valeur"]) < 1
        and abs(co["ecart_des_deux_voies_base_vie_pct"]) < 50,
        f"{co['loyer_base_vie_par_les_modules_MAD_par_mois']} MAD/mois contre "
        f"{co['loyer_base_vie_MAD_par_mois']} — {co['ecart_des_deux_voies_base_vie_pct']} %")
verifie("et c'est la ligne de D1 qui entre dans le total, pas la seconde voie",
        abs(co["loyer_de_la_base_vie_MAD"]
            - co["loyer_base_vie_MAD_par_mois"] * co["duree_du_chantier_mois"]) < 1)
verifie("l'ecart avec le bordereau de D1 est publie, et il est NEGATIF",
        abs(co["ecart_avec_D1_MAD"]
            - (co["loyer_des_grues_MAD"] - co["D1_loyer_de_grue_MAD"])) < 1
        and co["ecart_avec_D1_MAD"] < 0,
        f"{co['ecart_avec_D1_MAD']:.0f} MAD — D1 surestime")

# ------------------------------------------------- figures
print("\n--- l'interference des deux fleches ---")
inf = r["interference"]
verifie("l'interference porte sur la variante retenue",
        inf["variante"] == r["figures"]["plan_masse"]["variante"])
for pr_ in inf["paires"]:
    _g = {x["nom"]: x for x in next(c for c in r["couverture"]
                                    if c["variante"] == inf["variante"])["grues"]}
    a_, b_ = _g[pr_["grues"][0]], _g[pr_["grues"][1]]
    dd = math.hypot(a_["x_m"] - b_["x_m"], a_["y_m"] - b_["y_m"])
    verifie(f"{'-'.join(pr_['grues'])} : l'entraxe est la distance des deux mats",
            abs(pr_["entraxe_m"] - dd) < 0.05, f"{pr_['entraxe_m']} m")
    verifie(f"{'-'.join(pr_['grues'])} : secantes si et seulement si l'entraxe est "
            "plus petit que la somme des portees",
            pr_["secantes"] == (dd < a_["portee_m"] + b_["portee_m"]))
    if pr_["secantes"]:
        # forme fermee de la lentille, recalculee ici par une autre ecriture
        r1, r2 = a_["portee_m"], b_["portee_m"]
        x = (dd ** 2 + r1 ** 2 - r2 ** 2) / (2 * dd)
        aire = (r1 ** 2 * math.acos(x / r1) - x * math.sqrt(r1 ** 2 - x ** 2)
                + r2 ** 2 * math.acos((dd - x) / r2)
                - (dd - x) * math.sqrt(r2 ** 2 - (dd - x) ** 2))
        verifie(f"{'-'.join(pr_['grues'])} : l'aire commune recolle a la forme fermee",
                abs(pr_["aire_commune_m2"] - aire) < 0.5,
                f"{pr_['aire_commune_m2']} contre {aire:.1f} m²")
        verifie(f"{'-'.join(pr_['grues'])} : elle est plus petite que le plus petit disque",
                pr_["aire_commune_m2"] < math.pi * min(r1, r2) ** 2)
verifie("le module dit que deux grues secantes ne font pas deux fois une grue",
        dit(inf["_ce_que_la_geometrie_impose"], "pas le double", "attend")
        or dit(inf["_ce_que_la_geometrie_impose"], "n'est pas le double"))
verifie("et il met les regles en attente plutot que de les inventer",
        "⏸" in inf["_ce_qui_reste_en_attente"])

print("\n--- figures ---")
f = r["figures"]
verifie("la courbe de charge commence a la charge maximale et decroit",
        f["courbe_de_charge"][0]["v"] == G["charge_max_t"]["valeur"]
        and all(a["v"] >= b["v"] for a, b in zip(f["courbe_de_charge"],
                                                 f["courbe_de_charge"][1:])))
verifie("le marqueur de la figure est le rayon limite de la piece de charpente",
        abs(f["marqueur_charpente"]["x"]
            - G["moment_max_tm"]["valeur"] / _charpente) < 0.1,
        f"{f['marqueur_charpente']['x']} m")
verifie("le plan masse porte la variante retenue par le calcul, pas une dessinee",
        f["plan_masse"]["variante"] in [c["variante"] for c in r["couverture"]]
        and len(f["plan_masse"]["grues"]) >= 1,
        f["plan_masse"]["variante"])
verifie("le point defavorable de la figure est celui de la variante retenue",
        [f["point_defavorable"]["x"], f["point_defavorable"]["y"]]
        == list(next(c for c in r["couverture"]
                     if c["variante"] == f["plan_masse"]["variante"]
                     )["point_le_plus_defavorable"]))
verifie("la figure de couverture porte toutes les variantes, deux fois",
        len(f["couverture"]) == 2 * len(r["couverture"]))
# La legende annonce une comparaison DEUX A DEUX : les deux barres d'une variante doivent
# donc se suivre, sinon la figure montre autre chose que ce que sa legende promet.
verifie("et les deux barres d'une meme variante se suivent",
        all(f["couverture"][2 * i]["libelle"].split(" · ")[0]
            == f["couverture"][2 * i + 1]["libelle"].split(" · ")[0]
            for i in range(len(r["couverture"]))),
        " / ".join(x["libelle"] for x in f["couverture"][:4]))
verifie("la figure du survol porte les memes nombres que la section voisinage",
        [x["valeur"] for x in f["survol"]]
        == [x["survol_du_gabarit_m"] for x in r["voisinage"]["lignes"]],
        " / ".join(f"{x['valeur']:.0f} m" for x in f["survol"]))
verifie("la cascade du cout recolle a ses etapes",
        f["cout"][-1].get("type") == "total"
        and abs(f["cout"][-1]["montant"]
                - sum(x["montant"] for x in f["cout"][:-1])) <= 1)
verifie("et elle porte TROIS marches : un fixe et deux loyers",
        len(f["cout"]) == 4,
        " + ".join(x["libelle"] for x in f["cout"][:-1]))

print()
if echecs:
    print(f"ECHEC : {len(echecs)} controle(s) — {', '.join(echecs)}")
    sys.exit(1)
print("Tests installation : tous verts.")
