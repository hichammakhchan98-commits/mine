"""Metres, prix, sous-details et situations de travaux (module D1).

D2 a donne au chantier ses durees. D1 lui donne ses prix, et les deux sortent des
MEMES hypotheses : c'est la seule facon qu'un planning et un bordereau ne se
contredisent pas. Trois choses que ce module fait, et qu'un bordereau de ratios ne
peut pas faire :

1. Le prix unitaire n'est pas saisi, il est CONSTRUIT. Sa part de main d'oeuvre est
   deduite de la cadence et de l'effectif du planning : h/unite = 8 x compagnons /
   cadence. Changer une cadence change une duree ET un prix, du meme coup.
2. Le type d'un poste suit la FAMILLE de sa duree (§ D2) : une tache calculee donne
   un prix unitaire, une tache declaree un forfait, une tache imposee une fourniture
   sans heure de chantier. Et certains couts ne dependent d'aucune quantite : ils
   sont indexes sur la DUREE, et c'est par eux qu'un retard coute de l'argent.
3. Retourner les cadences en productivites par compagnon localise une erreur que la
   part de main d'oeuvre globale ne faisait que signaler (dette n° 10 de STATE.md).
"""
from __future__ import annotations
import json, math, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import planification as pln                                    # noqa: E402
from etat import avancement_planifie, trois_etats             # noqa: E402

TOL_DEUX_VOIES_PCT = 20.0   # justifiee dans ecart_des_deux_voies()


# ------------------------------------------------------------------ ressources
def taux_horaire_atelier(d: dict, metier: str) -> dict:
    """Taux horaire MOYEN d'un atelier, deduit de sa composition.

    Sans cette etape, un sous-detail paie des ferrailleurs au prix du manoeuvre.
    """
    r = d["prix_unitaires_MAD"]["ressources"]
    mo, comp = r["main_oeuvre_MAD_h"], r["composition_atelier"]
    n = d["planning"]["effectifs_chantier_V3"]["compagnons_par_atelier"][metier]
    chefs = comp["chefs_equipe"]
    if n <= chefs:
        raise ValueError(f"atelier {metier} : {n} compagnons pour {chefs} chef(s) d'equipe")
    part = comp["part_compagnons_qualifies_pct"]["valeur"] / 100
    qualifies = (n - chefs) * part
    manoeuvres = (n - chefs) - qualifies
    total = (chefs * mo["chef_equipe"]["valeur"]
             + qualifies * mo["compagnon_qualifie"]["valeur"]
             + manoeuvres * mo["manoeuvre"]["valeur"])
    return {"metier": metier, "effectif": n, "chefs_equipe": chefs,
            "compagnons_qualifies": round(qualifies, 2), "manoeuvres": round(manoeuvres, 2),
            "taux_MAD_h": round(total / n, 2)}


# ------------------------------------------------------------------ quantites
def quantites_bordereau(d: dict, q: dict) -> dict:
    """Quantite de chaque poste, DANS SON UNITE DE BORDEREAU.

    La quantite ne se redecide pas ici : elle est celle du metre de D2 (q), reexprimee
    dans l'unite du poste. Une seule quantite est propre a D1 : le m3 foisonne des
    deblais, qui n'est pas le m3 en place.
    """
    pl = d["planning"]
    part = pl["contraintes_exploitation"]["part_levage_sous_consignation_pct"]["valeur"] / 100
    kg = q["charpente_t"] * 1000.0
    out = {
        "TERR": q["decapage_m3"], "FOUI": q["fouille_niveau_technique_m3"],
        "FOND": q["beton_semelles_m3"], "RADT": q["surface_niveau_technique_m2"],
        "VOIL": q["voiles_niveau_technique_m2"], "PHNT": q["surface_niveau_technique_m2"],
        "POTR": float(q["n_poteaux"]), "MEZZ": q["surface_mezzanine_m2"],
        "CHFA": kg, "CHAP": kg * (1 - part), "CHLV": kg * part,
        "COUV": q["surface_couverture_m2"], "FACA": q["facade_m2"],
    }
    for id_, sd in d["prix_unitaires_MAD"]["sous_details"].items():
        if not id_.startswith("_") and sd["unite"] == "ens":
            out[id_] = 1.0
    manquants = set(pln.NOMS) - set(out)
    if manquants:
        raise ValueError(f"postes sans quantite : {sorted(manquants)}")
    return {k: round(v, 2) for k, v in out.items()}


# ------------------------------------------------------------------ sous-details
def _mat(d, cle, coef):
    """(libelle, quantite, prix unitaire, montant) pour une ligne de matiere."""
    pu = d["prix_unitaires_MAD"]["ressources"]["materiaux_MAD"][cle]["valeur"]
    return {"ressource": cle, "quantite": round(coef, 4), "pu_MAD": pu,
            "montant_MAD": round(coef * pu, 2)}


def _eng(d, cle, coef):
    pu = d["prix_unitaires_MAD"]["ressources"]["materiel_MAD"][cle]["valeur"]
    return {"ressource": cle, "quantite": round(coef, 5), "pu_MAD": pu,
            "montant_MAD": round(coef * pu, 2)}


def consommations(d: dict, poste: str) -> tuple[list, list]:
    """Matiere et materiel consommes par UNE unite de bordereau du poste.

    Les coefficients viennent de data/ ; les formules sont ici (§ 4.3). Les postes
    forfaitaires et de fourniture n'en ont pas : leur prix est un montant, pas une
    composition.
    """
    c = d["prix_unitaires_MAD"]["coefficients_sous_detail"]
    rq = d["planning"]["ratios_quantites_V3"]
    pl = d["planning"]
    pertes = 1 + c["pertes_beton_pct"]["valeur"] / 100
    acier = c["acier_kg_par_m3"]
    coff = c["coffrage_m2_par_unite"]
    cad = pl["cadences_chantier_V3"]
    mats, engs = [], []

    if poste in ("TERR", "FOUI"):
        foison = 1 + rq["foisonnement_pct"]["valeur"] / 100
        mats = [_mat(d, "evacuation_deblais_m3", foison)]
        # une pelle produit cadence/8 m3 par heure : son cout au m3 en decoule
        m3_par_h = cad["terrassement_m3_j_atelier"]["valeur"] / d["prix_unitaires_MAD"]["ressources"]["heures_par_jour"]
        engs = [_eng(d, "pelle_30t_h", 1.0 / m3_par_h)]

    elif poste == "FOND":
        mats = [_mat(d, "beton_bpe_m3", pertes),
                _mat(d, "acier_ha_kg", acier["semelles"]["valeur"]),
                _mat(d, "coffrage_rotation_m2", coff["semelle_par_m3"]["valeur"])]
        engs = [_eng(d, "vibreur_j", c["vibreur_j_par_m3"]["valeur"])]

    elif poste in ("RADT", "PHNT"):
        ep = rq["radier_niveau_technique_m" if poste == "RADT" else "dalle_niveau_technique_m"]["valeur"]
        ratio = acier["radier" if poste == "RADT" else "dalle_pleine"]["valeur"]
        mats = [_mat(d, "beton_bpe_m3", pertes * ep),
                _mat(d, "acier_ha_kg", ratio * ep),
                _mat(d, "coffrage_rotation_m2",
                     coff["radier_par_m2" if poste == "RADT" else "dalle_par_m2"]["valeur"])]
        if poste == "PHNT":
            mats.append(_mat(d, "etaiement_rotation_m2", c["etaiement_m2_par_m2_dalle"]["valeur"]))
        engs = [_eng(d, "pompe_a_beton_j", c["pompe_j_par_m3"]["valeur"] * ep),
                _eng(d, "vibreur_j", c["vibreur_j_par_m3"]["valeur"] * ep)]

    elif poste == "VOIL":
        ep = rq["voile_epaisseur_m"]["valeur"]
        mats = [_mat(d, "beton_bpe_m3", pertes * ep),
                _mat(d, "acier_ha_kg", acier["voile"]["valeur"] * ep),
                _mat(d, "coffrage_rotation_m2", coff["voile_par_m2"]["valeur"])]
        engs = [_eng(d, "vibreur_j", c["vibreur_j_par_m3"]["valeur"] * ep)]

    elif poste == "POTR":
        s, h = rq["poteau_section_m2"]["valeur"], _h_poteau(d)
        vol = s * h
        mats = [_mat(d, "beton_bpe_m3", pertes * vol),
                _mat(d, "acier_ha_kg", acier["poteau"]["valeur"] * vol),
                # section carree : 4 cotes de racine(S) sur la hauteur
                _mat(d, "coffrage_rotation_m2", 4 * math.sqrt(s) * h)]
        engs = [_eng(d, "vibreur_j", c["vibreur_j_par_m3"]["valeur"] * vol)]

    elif poste in ("CHAP", "CHLV"):
        # fourniture nulle : l'acier est paye en CHFA. On ne paie ici que le levage.
        t_par_j = cad["charpente_t_j_atelier"]["valeur"]
        engs = [_eng(d, "grue_mobile_200t_j", 1.0 / (t_par_j * 1000))]

    elif poste == "COUV":
        mats = [_mat(d, "couverture_m2", 1.0)]
        engs = [_eng(d, "nacelle_j", 1.0 / cad["couverture_m2_j_atelier"]["valeur"])]

    elif poste == "FACA":
        mats = [_mat(d, "facade_m2", 1.0)]
        engs = [_eng(d, "nacelle_j", 1.0 / cad["facade_m2_j_atelier"]["valeur"])]

    elif poste == "CHFA":
        mats = [_mat(d, "charpente_acier_kg", 1.0)]

    return mats, engs


def _h_poteau(d: dict) -> float:
    return next(n for n in d["geometrie"]["niveaux"] if n["nom"].startswith("RDC"))["h_libre_m"]


def heures_par_unite(d: dict, poste: str) -> dict:
    """h de main d'oeuvre de CHANTIER par unite de bordereau — DEDUITES du planning.

    h/unite_cadence = heures_par_jour x compagnons_par_atelier / cadence_atelier,
    puis x conversion (nombre d'unites de cadence par unite de bordereau).
    Le nombre d'ateliers n'y figure pas, et c'est normal : doubler les ateliers
    divise la duree par deux et laisse les heures — donc le prix — inchangees.
    """
    sd = d["prix_unitaires_MAD"]["sous_details"][poste]
    r = d["prix_unitaires_MAD"]["ressources"]
    cad = d["planning"]["cadences_chantier_V3"][sd["cadence"]]["valeur"]
    n = d["planning"]["effectifs_chantier_V3"]["compagnons_par_atelier"][sd["metier"]]
    h_cad = r["heures_par_jour"] * n / cad
    h = h_cad * sd["conversion"]
    return {"h_par_unite": round(h, 5), "h_par_unite_de_cadence": round(h_cad, 4),
            "cadence": sd["cadence"], "cadence_valeur": cad, "compagnons_par_atelier": n,
            "conversion": sd["conversion"],
            "taux": taux_horaire_atelier(d, sd["metier"])}


def heures_forfait(d: dict, poste: str, durees: dict) -> dict:
    """Un poste forfaitaire est TOUT COMPRIS : sa main d'oeuvre est deja dedans.

    La premiere version ajoutait duree x effectif x taux horaire au montant du forfait.
    C'etait un double compte : un forfait de 2,9 MMAD pour des noyaux en beton contient
    deja ses ferrailleurs et ses coffreurs. L'erreur ne pesait que quelques pour cent du
    total, mais elle rendait la part de main d'oeuvre du bordereau ininterpretable, parce
    qu'elle melait des heures CONNUES (celles des sous-details) et des heures INVENTEES
    (celles des forfaits).

    Ce que cela laisse : la main d'oeuvre d'un forfait n'est pas visible. C'est une
    propriete du forfait, pas une lacune du calcul, et c'est la raison pour laquelle un
    ratio de part de main d'oeuvre ne se calcule QUE sur les postes decomposes.
    """
    f = d["prix_unitaires_MAD"]["forfaits_MAD"]
    e = d["planning"]["effectifs_chantier_V3"]["effectif_par_tache"]
    return {"h_total": 0.0, "tout_compris": True,
            "sous_traite": poste in f["_sous_traites"],
            "effectif_au_planning": e.get(poste, 0),
            "duree_j": durees[poste]["duree_j"],
            "note": "montant tout compris : la main d'oeuvre y est, mais elle n'est pas "
                    "visible. Aucune heure n'est comptee pour ce poste."}


def sous_detail(d: dict, poste: str, qte: float, durees: dict) -> dict:
    """Un poste du bordereau, du debourse sec au prix de vente."""
    sd = d["prix_unitaires_MAD"]["sous_details"][poste]
    comp = d["prix_unitaires_MAD"]["composition_prix_pct"]
    f = d["prix_unitaires_MAD"]["forfaits_MAD"]
    typ = sd["type"]
    o = {"poste": poste, "libelle": pln.NOMS[poste], "lot": pln.LOT[poste], "type": typ,
         "unite": sd["unite"], "quantite": qte, "famille_duree": durees[poste]["famille"]}

    if typ == "unitaire":
        mats, engs = consommations(d, poste)
        h = heures_par_unite(d, poste)
        mo = h["h_par_unite"] * h["taux"]["taux_MAD_h"]
        o["main_oeuvre"] = {**h, "montant_MAD_par_unite": round(mo, 2)}
        o["materiaux"] = mats
        o["materiel"] = engs
        o["debourse_sec_par_unite_MAD"] = round(
            mo + sum(m["montant_MAD"] for m in mats) + sum(e["montant_MAD"] for e in engs), 2)
        o["heures_totales"] = round(h["h_par_unite"] * qte, 1)

    elif typ == "unitaire_herite_TV":
        o.update(_mezzanine(d, qte))

    elif typ in ("forfait", "fourniture_forfait"):
        o["main_oeuvre"] = heures_forfait(d, poste, durees)
        o["forfait_MAD"] = f[poste]["valeur"]
        o["fourchette_forfait_MAD"] = f[poste]["fourchette"]
        o["debourse_sec_par_unite_MAD"] = float(f[poste]["valeur"])
        o["heures_totales"] = 0.0

    elif typ == "fourniture_unitaire":
        mats, engs = consommations(d, poste)
        o["materiaux"], o["materiel"] = mats, engs
        o["main_oeuvre"] = {"h_par_unite": 0.0, "montant_MAD_par_unite": 0.0,
                            "note": "aucune heure de chantier : la main d'oeuvre d'atelier est "
                                    "dans le prix du fournisseur"}
        o["debourse_sec_par_unite_MAD"] = round(
            sum(m["montant_MAD"] for m in mats) + sum(e["montant_MAD"] for e in engs), 2)
        o["heures_totales"] = 0.0
    else:
        raise ValueError(f"type de poste inconnu : {typ}")

    k = 1 + sum(comp[x]["valeur"] for x in ("frais_generaux_siege", "aleas", "marge")) / 100
    o["coefficient_de_vente"] = round(k, 4)
    o["pu_de_vente_MAD"] = round(o["debourse_sec_par_unite_MAD"] * k, 2)
    o["debourse_sec_total_MAD"] = round(o["debourse_sec_par_unite_MAD"] * qte, 2)
    o["prix_total_MAD"] = round(o["pu_de_vente_MAD"] * qte, 2)
    o["main_oeuvre_totale_MAD"] = round(
        o["heures_totales"] * (o["main_oeuvre"].get("taux", {}).get("taux_MAD_h")
                               or o["main_oeuvre"].get("taux_MAD_h") or 0.0), 2)
    return o


def _mezzanine(d: dict, qte: float) -> dict:
    """Le plancher de mezzanine n'est pas re-metre : il est re-PRIX.

    Les quantites viennent du metre geometrique du module TV, les heures de sa chaine
    de cadences unitaires. D1 remplace seulement les prix POSES par des prix de
    ressource, pour que ce poste soit comparable aux vingt-six autres.
    """
    import plancher as pl_tv, cycle_plancher as cy             # noqa: E402
    q = pl_tv.quantites_zone(d)
    t = cy.durees_taches(d, q)
    e = d["effectifs"]
    h_j = e["heures_par_jour"]
    heures = (t["coffrage_j"] * e["coffreurs"]
              + t["ferraillage_poutres_j"] * e["ferrailleurs_poutres"]
              + t["ferraillage_dalle_j"] * e["ferrailleurs_dalle"]
              + t["betonnage_j"] * e["equipe_betonnage"]) * h_j
    r = d["prix_unitaires_MAD"]["ressources"]
    c = d["prix_unitaires_MAD"]["coefficients_sous_detail"]
    m = r["materiaux_MAD"]
    s = q["surface_m2"]
    pertes = 1 + c["pertes_beton_pct"]["valeur"] / 100
    mats = [
        {"ressource": "beton_bpe_m3", "quantite": round(q["beton_m3"] * pertes / s, 4),
         "pu_MAD": m["beton_bpe_m3"]["valeur"],
         "montant_MAD": round(q["beton_m3"] * pertes * m["beton_bpe_m3"]["valeur"] / s, 2)},
        {"ressource": "acier_ha_kg", "quantite": round(q["acier_kg"] / s, 4),
         "pu_MAD": m["acier_ha_kg"]["valeur"],
         "montant_MAD": round(q["acier_kg"] * m["acier_ha_kg"]["valeur"] / s, 2)},
        {"ressource": "coffrage_rotation_m2", "quantite": round(q["coffrage_m2"] / s, 4),
         "pu_MAD": m["coffrage_rotation_m2"]["valeur"],
         "montant_MAD": round(q["coffrage_m2"] * m["coffrage_rotation_m2"]["valeur"] / s, 2)},
        {"ressource": "etaiement_rotation_m2", "quantite": 1.0,
         "pu_MAD": m["etaiement_rotation_m2"]["valeur"],
         "montant_MAD": float(m["etaiement_rotation_m2"]["valeur"])},
    ]
    nb = d["geometrie"]["mezzanine"]["zones_de_coulage"]["nb_zones"]
    engs = [{"ressource": "pompe_a_beton_j", "quantite": round(t["betonnage_j"] / s, 5),
             "pu_MAD": r["materiel_MAD"]["pompe_a_beton_j"]["valeur"],
             "montant_MAD": round(t["betonnage_j"] * r["materiel_MAD"]["pompe_a_beton_j"]["valeur"] / s, 2)}]
    taux = taux_horaire_atelier(d, "fondations")   # meme metier : coffreurs-ferrailleurs-betonnage
    mo_u = heures / s * taux["taux_MAD_h"]
    return {
        "main_oeuvre": {"h_par_unite": round(heures / s, 5), "heures_par_zone": round(heures, 1),
                        "taux": taux, "montant_MAD_par_unite": round(mo_u, 2),
                        "note": "heures de la chaine de cadences UNITAIRES du module TV, "
                                "ramenees au m2 de zone"},
        "materiaux": mats, "materiel": engs,
        "nb_zones": nb, "surface_zone_m2": s,
        "debourse_sec_par_unite_MAD": round(
            mo_u + sum(x["montant_MAD"] for x in mats) + sum(x["montant_MAD"] for x in engs), 2),
        "heures_totales": round(heures / s * qte, 1),
    }


# ------------------------------------------------------------------ bordereau
def frais_de_duree(d: dict, duree_j: float) -> dict:
    """Les postes indexes sur la duree, et le cout d'un mois de retard."""
    fr = d["prix_unitaires_MAD"]["frais_indexes_sur_la_duree_MAD_mois"]
    r = d["prix_unitaires_MAD"]["ressources"]
    mois = duree_j / r["jours_ouvres_par_mois"]
    lignes = {k: {"MAD_mois": v["valeur"], "montant_MAD": round(v["valeur"] * mois, 2)}
              for k, v in fr.items() if not k.startswith("_")}
    par_mois = sum(v["MAD_mois"] for v in lignes.values())
    return {"duree_j": round(duree_j, 2), "duree_mois": round(mois, 2), "lignes": lignes,
            "total_MAD": round(par_mois * mois, 2), "cout_MAD_par_mois": par_mois,
            "cout_MAD_par_jour_ouvre": round(par_mois / r["jours_ouvres_par_mois"], 2)}


def bordereau(d: dict, q: dict, durees: dict, duree_j: float) -> dict:
    qb = quantites_bordereau(d, q)
    postes = [sous_detail(d, p, qb[p], durees) for p in pln.NOMS]
    fd = frais_de_duree(d, duree_j)
    k = postes[0]["coefficient_de_vente"]
    ds = sum(p["debourse_sec_total_MAD"] for p in postes) + fd["total_MAD"]
    heures = sum(p["heures_totales"] for p in postes)
    mo = sum(p["main_oeuvre_totale_MAD"] for p in postes)
    emprise = q["emprise_m2"]
    par_lot = {}
    for p in postes:
        par_lot.setdefault(p["lot"], {"debourse_MAD": 0.0, "prix_MAD": 0.0, "postes": []})
        par_lot[p["lot"]]["debourse_MAD"] += p["debourse_sec_total_MAD"]
        par_lot[p["lot"]]["prix_MAD"] += p["prix_total_MAD"]
        par_lot[p["lot"]]["postes"].append(p["poste"])
    par_lot["9 · Frais de duree"] = {"debourse_MAD": fd["total_MAD"],
                                     "prix_MAD": round(fd["total_MAD"] * k, 2),
                                     "postes": ["ENCADREMENT", "BASE-VIE", "GRUE-LOC", "ENERGIE"]}
    for v in par_lot.values():
        v["debourse_MAD"] = round(v["debourse_MAD"], 2)
        v["prix_MAD"] = round(v["prix_MAD"], 2)
        v["part_pct"] = round(v["debourse_MAD"] / ds * 100, 2)
    return {
        "postes": postes, "frais_de_duree": fd, "par_lot": par_lot,
        "debourse_sec_MAD": round(ds, 2),
        "prix_de_vente_MAD": round(ds * k, 2),
        "coefficient_de_vente": k,
        "heures_de_main_oeuvre_de_chantier": round(heures, 1),
        "main_oeuvre_MAD": round(mo, 2),
        "part_main_oeuvre_du_debourse_pct": round(mo / ds * 100, 2),
        "cout_MAD_par_m2_emprise": round(ds * k / emprise, 1),
        "emprise_m2": emprise,
    }


# ------------------------------------- seconde voie : les prix POSES du jeu de donnees
def voie_prix_poses(d: dict, q: dict) -> dict:
    """Chiffrage par les prix poses (prix_unitaires_MAD.postes), voie independante.

    Elle ne couvre que le gros oeuvre en beton : c'est tout ce que des ratios de
    beton, d'acier et de coffrage peuvent chiffrer. La comparaison porte donc sur ce
    perimetre, et pas sur le bordereau entier — comparer deux perimetres differents
    est la facon la plus simple de se rassurer a tort.
    """
    p = d["prix_unitaires_MAD"]["postes"]
    c = d["prix_unitaires_MAD"]["coefficients_sous_detail"]
    rq = d["planning"]["ratios_quantites_V3"]
    pertes = 1 + c["pertes_beton_pct"]["valeur"] / 100
    ac, co = c["acier_kg_par_m3"], c["coffrage_m2_par_unite"]
    lignes = {}

    def ligne(nom, beton_m3, ratio_acier, coffrage_m2):
        acier = beton_m3 / pertes * ratio_acier
        lignes[nom] = {
            "beton_m3": round(beton_m3, 1), "acier_kg": round(acier, 1),
            "coffrage_m2": round(coffrage_m2, 1),
            "montant_MAD": round(beton_m3 * p["beton_m3"]["valeur"]
                                 + acier * p["acier_kg"]["valeur"]
                                 + coffrage_m2 * p["coffrage_m2"]["valeur"], 2)}

    s_nt = q["surface_niveau_technique_m2"]
    ligne("semelles", q["beton_semelles_m3"] * pertes, ac["semelles"]["valeur"],
          q["beton_semelles_m3"] * co["semelle_par_m3"]["valeur"])
    ligne("radier", q["beton_radier_m3"] * pertes, ac["radier"]["valeur"],
          s_nt * co["radier_par_m2"]["valeur"])
    ep_v = rq["voile_epaisseur_m"]["valeur"]
    ligne("voiles", q["voiles_niveau_technique_m2"] * ep_v * pertes, ac["voile"]["valeur"],
          q["voiles_niveau_technique_m2"] * co["voile_par_m2"]["valeur"])
    ligne("plancher_haut_nt", q["beton_plancher_haut_nt_m3"] * pertes, ac["dalle_pleine"]["valeur"],
          s_nt * co["dalle_par_m2"]["valeur"])
    ligne("poteaux_rdc", q["beton_poteaux_rdc_m3"] * pertes, ac["poteau"]["valeur"],
          q["n_poteaux"] * 4 * math.sqrt(rq["poteau_section_m2"]["valeur"]) * _h_poteau(d))
    mz = _mezz_quantites(d)
    ligne("mezzanine", mz["beton_m3"] * pertes, mz["ratio_acier_kg_m3"], mz["coffrage_m2"])
    return {"lignes": lignes, "perimetre": sorted(lignes),
            "total_MAD": round(sum(v["montant_MAD"] for v in lignes.values()), 2)}


def _mezz_quantites(d: dict) -> dict:
    import plancher as pl_tv                                   # noqa: E402
    q = pl_tv.quantites_zone(d)
    nb = d["geometrie"]["mezzanine"]["zones_de_coulage"]["nb_zones"]
    return {"beton_m3": q["beton_m3"] * nb, "coffrage_m2": q["coffrage_m2"] * nb,
            "acier_kg": q["acier_kg"] * nb, "ratio_acier_kg_m3": q["ratio_acier_kg_m3"],
            "surface_m2": q["surface_m2"] * nb, "nb_zones": nb}


def ecart_des_deux_voies(bord: dict, voie_b: dict) -> dict:
    """Compare les deux voies SUR LE MEME PERIMETRE, et dit ce que l'ecart prouve."""
    noms = {"semelles": "FOND", "radier": "RADT", "voiles": "VOIL",
            "plancher_haut_nt": "PHNT", "poteaux_rdc": "POTR", "mezzanine": "MEZZ"}
    par_poste = {}
    a_tot = b_tot = 0.0
    for cle, poste in noms.items():
        p = next(x for x in bord["postes"] if x["poste"] == poste)
        a = p["prix_total_MAD"]
        b = voie_b["lignes"][cle]["montant_MAD"]
        a_tot += a
        b_tot += b
        par_poste[poste] = {"voie_A_sous_detail_MAD": round(a, 2), "voie_B_prix_poses_MAD": round(b, 2),
                            "ecart_pct": round((a - b) / b * 100, 2)}
    ecart = (a_tot - b_tot) / b_tot * 100
    return {
        "perimetre": "gros oeuvre en beton arme — les six postes que des ratios peuvent chiffrer",
        "par_poste": par_poste,
        "voie_A_sous_detail_MAD": round(a_tot, 2), "voie_B_prix_poses_MAD": round(b_tot, 2),
        "ecart_pct": round(ecart, 2), "tolerance_pct": TOL_DEUX_VOIES_PCT,
        "verdict": "OK" if abs(ecart) <= TOL_DEUX_VOIES_PCT else "ECART",
        "tolerance_justifiee": (
            "La tolerance de 5 % du § 3.3 vaut pour deux calculs du MEME objet. Ici les deux "
            "voies ne chiffrent pas le meme objet : la voie A construit un prix de vente a "
            "partir de ressources et d'un coefficient d'entreprise, la voie B lit des prix de "
            "marche deja poses, qui portent des sujetions que le sous-detail ne detaille pas "
            "(consommables, nettoyage, reprises, encadrement d'equipe, aleas du fournisseur). "
            "Un ecart de 20 % entre un prix construit et un prix de marche est normal ; au-dela, "
            "l'un des deux est faux."),
        "divers_necessaire_pct": round((b_tot / a_tot - 1) * 100, 1),
        "ce_que_l_ecart_dit": (
            f"Le sous-detail est sous le prix de marche sur les SIX postes, de "
            f"{min(v['ecart_pct'] for v in par_poste.values()):.0f} % a "
            f"{max(v['ecart_pct'] for v in par_poste.values()):.0f} %. Un ecart "
            "systematique et de meme signe n'est pas une dispersion : c'est une ligne "
            "qui manque. Un sous-detail porte les ressources qu'on sait nommer — beton, "
            "acier, coffrage, heures, engins — et pas celles qu'on oublie : consommables, "
            "nettoyage, reprises de parement, calage, attente d'approvisionnement, "
            f"encadrement d'equipe. Il faudrait ajouter {round((b_tot / a_tot - 1) * 100, 1)} % "
            "de « divers de chantier » sur le debourse sec pour recoller au prix pose. "
            "C'est ainsi qu'un metreur CALIBRE sa ligne de divers : contre des prix de "
            "marche, poste par poste, et non en recopiant un pourcentage d'usage."),
        "ce_que_ce_controle_prouve": (
            "Que le sous-detail ne s'est pas trompe d'un ORDRE DE GRANDEUR. Il ne prouve ni que "
            "les prix de ressource sont justes, ni que les prix poses le sont : seuls un "
            "bordereau reel et des attachements le diraient."),
    }


# ------------------------------- productivites : la ou se localise la dette n 10
def coherence_cadences(d: dict, q: dict) -> dict:
    """Retourne chaque cadence d'atelier en productivite PAR COMPAGNON, metier par metier.

    La part de main d'oeuvre globale signale un probleme ; elle ne dit pas ou. Une
    productivite individuelle, elle, se compare a ce qu'un compagnon pose vraiment en
    une journee. C'est le controle qui localise la dette n° 10 de STATE.md.
    """
    pr = d["prix_unitaires_MAD"]["ratios_de_controle"]["productivites_par_compagnon_et_par_jour"]
    r = d["prix_unitaires_MAD"]["ressources"]
    c = d["prix_unitaires_MAD"]["coefficients_sous_detail"]
    rq = d["planning"]["ratios_quantites_V3"]
    ac, co = c["acier_kg_par_m3"], c["coffrage_m2_par_unite"]
    pertes = 1 + c["pertes_beton_pct"]["valeur"] / 100
    h_j = r["heures_par_jour"]

    def implique(poste, acier_kg_u, coffrage_m2_u, beton_m3_u):
        """Pour une unite d'ouvrage, les trois productivites qu'implique la cadence."""
        h = heures_par_unite(d, poste)
        jh = h["h_par_unite"] / h_j            # jours-compagnon par unite d'ouvrage
        out = {"poste": poste, "jours_compagnon_par_unite": round(jh, 4), "metiers": {}}
        for metier, par_unite, cle in (("ferraillage_kg", acier_kg_u, "ferraillage_kg"),
                                       ("coffrage_m2", coffrage_m2_u, "coffrage_m2"),
                                       ("betonnage_m3", beton_m3_u, "betonnage_m3")):
            if par_unite <= 0:
                continue
            # hypothese explicite : les trois metiers se partagent les jours-compagnon
            # au prorata du temps qu'ils prendraient a la productivite de reference
            out["metiers"][metier] = {"quantite_par_unite": round(par_unite, 4),
                                      "reference_j": round(par_unite / pr[cle]["valeur"], 4)}
        besoin = sum(v["reference_j"] for v in out["metiers"].values())
        out["jours_compagnon_de_reference_par_unite"] = round(besoin, 4)
        out["facteur_de_recalage"] = round(besoin / jh, 2) if jh > 0 else None
        for metier, v in out["metiers"].items():
            part = v["reference_j"] / besoin if besoin else 0
            v["productivite_implicite"] = round(v["quantite_par_unite"] / (jh * part), 1) if jh * part else None
            v["fourchette_de_reference"] = pr[metier]["fourchette"]
            v["dans_la_fourchette"] = bool(
                v["productivite_implicite"] is not None
                and pr[metier]["fourchette"][0] <= v["productivite_implicite"] <= pr[metier]["fourchette"][1])
        return out

    s = math.sqrt(rq["poteau_section_m2"]["valeur"])
    hp = _h_poteau(d)
    vol_pot = rq["poteau_section_m2"]["valeur"] * hp
    ep_r, ep_d, ep_v = (rq["radier_niveau_technique_m"]["valeur"],
                        rq["dalle_niveau_technique_m"]["valeur"],
                        rq["voile_epaisseur_m"]["valeur"])
    cas = [
        implique("FOND", ac["semelles"]["valeur"], co["semelle_par_m3"]["valeur"], pertes),
        implique("RADT", ac["radier"]["valeur"] * ep_r, co["radier_par_m2"]["valeur"], pertes * ep_r),
        implique("VOIL", ac["voile"]["valeur"] * ep_v, co["voile_par_m2"]["valeur"], pertes * ep_v),
        implique("PHNT", ac["dalle_pleine"]["valeur"] * ep_d, co["dalle_par_m2"]["valeur"], pertes * ep_d),
        implique("POTR", ac["poteau"]["valeur"] * vol_pot, 4 * s * hp, pertes * vol_pot),
    ]
    hors = [c_["poste"] for c_ in cas
            if any(not v["dans_la_fourchette"] for v in c_["metiers"].values())]
    facteurs = [c_["facteur_de_recalage"] for c_ in cas]
    # Bande de credibilite du FACTEUR lui-meme : un facteur proche de 1 veut dire que la
    # cadence demande le travail qu'un compagnon fournit. C'est le critere de la figure,
    # et il doit etre publie, sans quoi la legende et le dessin comptent differemment.
    BANDE = (0.8, 1.2)
    hors_bande = [c_["poste"] for c_ in cas
                  if not BANDE[0] <= c_["facteur_de_recalage"] <= BANDE[1]]
    return {
        "cas": cas, "postes_hors_fourchette": hors,
        "bande_de_credibilite": list(BANDE),
        "postes_hors_bande": hors_bande,
        "nb_postes": len(cas),
        "poste_le_plus_optimiste": max(cas, key=lambda c_: c_["facteur_de_recalage"])["poste"],
        "poste_le_plus_prudent": min(cas, key=lambda c_: c_["facteur_de_recalage"])["poste"],
        "facteur_de_recalage_min": round(min(facteurs), 2),
        "facteur_de_recalage_max": round(max(facteurs), 2),
        "facteur_de_recalage_moyen": round(sum(facteurs) / len(facteurs), 2),
        "lecture": (
            "Le facteur de recalage est le rapport entre les jours-compagnon qu'il faudrait aux "
            "productivites de reference et ceux qu'implique la cadence du planning. Superieur a "
            "1, la cadence est optimiste : les durees de D2 et les prix de D1 sont tous deux "
            "trop bas, du meme facteur et pour la meme raison."),
        "ce_que_ce_controle_ne_dit_pas": (
            "Il ne dit pas que les cadences sont fausses : il dit qu'elles sont incompatibles "
            "avec des productivites individuelles d'ordre de grandeur courant. Les deux sont "
            "des hypotheses V3. Un seul attachement reel tranche, et aucun n'est disponible."),
    }


def variante_recalee(d: dict, q: dict, durees: dict, duree_j: float, facteur: float,
                     duree_mezz: float) -> dict:
    """Ce que devient le chantier si les cadences sont divisees par le facteur de recalage.

    On ne touche PAS aux donnees : la variante est une lecture, pas une decision. Les
    durees et les prix de reference restent ceux de D2 et du bordereau ci-dessus.
    """
    import copy
    d2 = copy.deepcopy(d)
    for cle, v in d2["planning"]["cadences_chantier_V3"].items():
        if isinstance(v, dict) and "valeur" in v:
            v["valeur"] = v["valeur"] / facteur
    q2 = pln.quantites_chantier(d2, d2["planning"])
    dur2 = pln.durees_chantier(d2, d2["planning"], q2, duree_mezz)
    f2 = pln.planning_avec_fenetres(d2, dur2)
    res2 = pln.voie_A_parcours(f2["taches"])
    b2 = bordereau(d2, q2, dur2, res2["duree"])
    b1 = bordereau(d, q, durees, duree_j)
    return {
        "facteur": facteur,
        "duree_j": {"reference": round(duree_j, 1),
                    "recalee": round(res2["duree"], 1),
                    "ecart_pct": round((res2["duree"] - duree_j) / duree_j * 100, 1)},
        "debourse_MAD": {"reference": b1["debourse_sec_MAD"], "recalee": b2["debourse_sec_MAD"],
                         "ecart_pct": round((b2["debourse_sec_MAD"] - b1["debourse_sec_MAD"])
                                            / b1["debourse_sec_MAD"] * 100, 1)},
        "part_main_oeuvre_beton_arme_pct": {
            "reference": controle_ratios(d, b1, q)["part_main_oeuvre_beton_arme_decompose"]["constate"],
            "recalee": controle_ratios(d2, b2, q2)["part_main_oeuvre_beton_arme_decompose"]["constate"],
            "fourchette_attendue": d["prix_unitaires_MAD"]["ratios_de_controle"]
                                    ["part_main_oeuvre_gros_oeuvre_pct"]["fourchette"],
            "_base": "beton arme decompose — la seule base ou ce ratio est defini"},
        "frais_de_duree_MAD": {"reference": b1["frais_de_duree"]["total_MAD"],
                               "recalee": b2["frais_de_duree"]["total_MAD"]},
        "lecture": (
            "Une cadence divisee par le facteur de recalage allonge le chantier ET renchérit le "
            "debourse, par deux chemins differents : plus d'heures de main d'oeuvre, et plus de "
            "mois de frais indexes sur la duree. C'est pourquoi une cadence optimiste est la plus "
            "couteuse des hypotheses : elle se paie deux fois."),
        "limite": (
            "Le recalage ne porte que sur les cadences d'ATELIER du chantier. Les cadences "
            "unitaires du module TV, qui donnent la duree du plancher de mezzanine, sont un "
            "autre bloc de donnees : elles ne sont pas recalees ici, et la duree de MEZZ est "
            "donc inchangee dans la variante. C'est une sous-estimation du facteur, pas une "
            "surestimation."),
    }


# ------------------------------------------------------------------ situations
def revision(d: dict, montant: float) -> dict:
    """Revision des prix par formule a index. Le controle a + b + c = 1 est le premier
    a faire dans un CPS : une somme differente de 1 fausse toutes les revisions."""
    rv = d["prix_unitaires_MAD"]["contrat"]["revision_des_prix"]
    a = rv["part_fixe_a"]["valeur"]
    b = rv["part_b_index_batiment"]["valeur"]
    c = rv["part_c_index_acier"]["valeur"]
    somme = a + b + c
    if abs(somme - 1.0) > 1e-9:
        raise ValueError(f"revision : a + b + c = {somme:.4f} et non 1 — formule inutilisable")
    I, J = rv["I_sur_I0"]["valeur"], rv["J_sur_J0"]["valeur"]
    k = a + b * I + c * J
    return {"a": a, "b": b, "c": c, "somme_abc": round(somme, 6), "I_sur_I0": I, "J_sur_J0": J,
            "coefficient": round(k, 5), "montant_initial_MAD": round(montant, 2),
            "montant_revise_MAD": round(montant * k, 2),
            "revision_MAD": round(montant * (k - 1), 2),
            "part_de_la_revision_pct": round((k - 1) * 100, 2)}


def situation(d: dict, bord: dict, declare: dict) -> dict:
    """Situation mensuelle : de l'avancement declare au net a payer.

    L'ordre des operations n'est pas decoratif : la revision porte sur les travaux, la
    retenue de garantie sur le montant revise, et le remboursement d'avance sur le
    cumul. Inverser deux lignes change le net a payer.
    """
    ct = d["prix_unitaires_MAD"]["contrat"]
    se = d["prix_unitaires_MAD"]["situation_exemple"]
    # L'avancement declare n'est PAS saisi ici : il vient de l'etat du chantier
    # (calc/etat.py), partage avec le module de suivi. Saisi a part, il pouvait — et il
    # l'a fait — decrire une date qui n'etait pas celle du planning : la situation
    # annoncait sept mois ecoules pour un etat de chantier correspondant au deuxieme.
    av = declare
    marche = bord["prix_de_vente_MAD"]

    lignes, cumul = [], 0.0
    for p in bord["postes"]:
        a = av[p["poste"]] / 100
        m = p["prix_total_MAD"] * a
        cumul += m
        lignes.append({"poste": p["poste"], "libelle": p["libelle"], "unite": p["unite"],
                       "quantite_marche": p["quantite"], "avancement_pct": av[p["poste"]],
                       "quantite_attachee": round(p["quantite"] * a, 2),
                       "pu_MAD": p["pu_de_vente_MAD"], "montant_cumule_MAD": round(m, 2)})
    # les frais indexes sur la duree s'attachent au TEMPS ecoule, pas a un ouvrage
    fd = bord["frais_de_duree"]
    mois = d["suivi_chantier"]["date_arret_j"] / d["prix_unitaires_MAD"]["ressources"]["jours_ouvres_par_mois"]
    part_temps = min(1.0, mois / fd["duree_mois"])
    m_fd = fd["total_MAD"] * bord["coefficient_de_vente"] * part_temps
    cumul += m_fd
    lignes.append({"poste": "FRAIS-DUREE", "libelle": "Frais de chantier indexes sur la duree",
                   "unite": "mois", "quantite_marche": fd["duree_mois"],
                   "avancement_pct": round(part_temps * 100, 1),
                   "quantite_attachee": round(mois, 2),
                   "pu_MAD": round(fd["cout_MAD_par_mois"] * bord["coefficient_de_vente"], 2),
                   "montant_cumule_MAD": round(m_fd, 2)})

    rev = revision(d, cumul)
    revise = rev["montant_revise_MAD"]
    rg = revise * ct["retenue_de_garantie_pct"]["valeur"] / 100
    plafond = marche * ct["retenue_plafond_pct_du_marche"]["valeur"] / 100
    rg_plafonnee = min(rg, plafond)
    avance = marche * ct["avance_pct"]["valeur"] / 100
    bas, haut = ct["avance_remboursement_entre_avancement_pct"]
    pct = cumul / marche * 100
    frac = 0.0 if pct <= bas else (1.0 if pct >= haut else (pct - bas) / (haut - bas))
    rembourse = avance * frac
    net = revise - rg_plafonnee - rembourse + avance * 0.0   # l'avance a deja ete encaissee
    cal = pln.calendrier(fd["duree_j"], d["planning"]["calendrier"])
    return {
        "numero": se["numero"], "mois_ecoules": round(mois, 2), "lignes": lignes,
        "montant_marche_MAD": marche,
        "travaux_cumules_MAD": round(cumul, 2),
        "travaux_cumules_pct_du_marche": round(pct, 2),
        "_note_avancement": (
            "Ce pourcentage est celui des TRAVAUX factures, avant retenues. Le module D4 "
            "publie un « avancement financier » different, qui est le NET encaissable : "
            "les deux ne se confondent pas, et c'est la retenue de garantie plus le "
            "remboursement d'avance qui les separent."),
        "revision": rev,
        "montant_revise_MAD": round(revise, 2),
        "retenue_de_garantie_MAD": round(rg, 2),
        "retenue_plafond_MAD": round(plafond, 2),
        "retenue_retenue_MAD": round(rg_plafonnee, 2),
        "avance_versee_MAD": round(avance, 2),
        "avance_remboursee_cumul_MAD": round(rembourse, 2),
        "fraction_de_remboursement": round(frac, 4),
        "net_cumule_a_payer_MAD": round(net, 2),
        "delai_de_paiement_j": ct["delai_de_paiement_j"]["valeur"],
        "avertissement_CPS": (
            "Tous les taux de cette situation (avance, retenue, plafond, delai, revision) sont "
            "des hypotheses V3 posees pour faire tourner l'exemple. Dans un marche reel ils se "
            "lisent dans le CPS, qui prime (§ 3.1) : ne reportez aucun de ces chiffres sur un "
            "dossier sans l'avoir ouvert."),
        "_calendrier_du_chantier": {"fin": cal["fin_avec_alea"],
                                    "duree_ouvree_avec_intemperies_j":
                                        cal["duree_ouvree_avec_intemperies_j"]},
    }


def courbe_de_depense(bord: dict, res: dict, durees: dict) -> dict:
    """Profil de DEPENSE dans le temps — qui n'est pas la courbe en S de D2.

    La courbe en S du module D2 est en jours-hommes : elle mesure le travail. Celle-ci
    est en dirhams. Les deux ne peuvent pas coincider, parce que des postes depensent
    sans mobiliser personne sur le chantier (fabrication de la charpente, lots
    techniques sous-traites) et que d'autres mobilisent beaucoup pour peu d'argent.
    Prendre l'une pour l'autre est la facon la plus directe de se tromper sur une
    tresorerie : c'est la meme erreur que de repartir un avancement au prorata du
    temps au lieu de le deriver de l'etat physique.

    Chaque poste etale son debourse uniformement sur la duree de SA tache ; les frais
    indexes sur la duree s'etalent sur le chantier entier.
    """
    duree = res["duree"]
    fin = int(math.ceil(duree))
    seg = []
    for p in bord["postes"]:
        deb, f = res["tot"][p["poste"]]
        seg.append((deb, max(f, deb + 1e-9), p["debourse_sec_total_MAD"]))
    seg.append((0.0, duree, bord["frais_de_duree"]["total_MAD"]))
    total = sum(m for _, _, m in seg)

    def cumul(j):
        acc = 0.0
        for deb, f, m in seg:
            if j >= f:
                acc += m
            elif j > deb:
                acc += m * (j - deb) / (f - deb)
        return acc

    pts = [{"j": k, "depense_MAD": round(cumul(k)), "pct": round(cumul(k) / total * 100, 2)}
           for k in range(0, fin + 1, 5)]
    if pts[-1]["j"] < fin:
        pts.append({"j": fin, "depense_MAD": round(total), "pct": 100.0})
    return {"points": pts, "total_MAD": round(total, 2), "cumul": cumul}


def ecart_depense_travail(dep: dict, courbe_s: list) -> dict:
    """De combien la courbe de l'argent devance celle du travail, et pourquoi."""
    par_j = {p["j"]: p["prevu"] for p in courbe_s}
    ecarts = []
    for p in dep["points"]:
        if p["j"] in par_j:
            ecarts.append({"j": p["j"], "depense_pct": p["pct"], "travail_pct": par_j[p["j"]],
                           "ecart_pts": round(p["pct"] - par_j[p["j"]], 1)})
    pire = max(ecarts, key=lambda e: abs(e["ecart_pts"])) if ecarts else None
    return {
        "points": ecarts, "ecart_maximal": pire,
        "lecture": (
            "Un ecart positif veut dire que l'argent part plus vite que les heures : le "
            "chantier paie des fournitures et des sous-traitants avant d'avoir consomme la "
            "main d'oeuvre correspondante. C'est la situation normale d'un batiment a forte "
            "part de fourniture, et c'est ce qui rend la tresorerie plus tendue que le "
            "planning ne le laisse croire."),
    }


def tresorerie(d: dict, bord: dict, dep: dict) -> dict:
    """Decaissements contre encaissements : le besoin de tresorerie du chantier.

    Les deux courbes sortent du profil de DEPENSE (en dirhams), jamais du profil de
    travail. Les recettes le suivent avec un mois de constat, le delai de paiement du
    CPS, et moins la retenue de garantie. L'ecart maximal entre les deux est ce que
    l'entreprise doit financer, et il ne se devine pas.
    """
    ct = d["prix_unitaires_MAD"]["contrat"]
    r = d["prix_unitaires_MAD"]["ressources"]
    jm = r["jours_ouvres_par_mois"]
    duree = bord["frais_de_duree"]["duree_j"]
    ds, marche = bord["debourse_sec_MAD"], bord["prix_de_vente_MAD"]
    rg = ct["retenue_de_garantie_pct"]["valeur"] / 100
    delai = ct["delai_de_paiement_j"]["valeur"]
    avance = marche * ct["avance_pct"]["valeur"] / 100
    bas, haut = ct["avance_remboursement_entre_avancement_pct"]
    total = dep["total_MAD"]

    def frac_avancement(j):
        return min(1.0, max(0.0, dep["cumul"](min(max(j, 0.0), duree)) / total))

    pas = max(1, int(round(duree / 60)))
    points, besoin_max, j_max = [], 0.0, 0
    for j in range(0, int(duree) + pas, pas):
        decaisse = ds * frac_avancement(j)
        encaisse = avance
        mois = 0
        while True:
            mois += 1
            depot = mois * jm
            if depot + delai > j:
                break
            cum = marche * frac_avancement(depot)
            pct = cum / marche * 100
            fr = 0.0 if pct <= bas else (1.0 if pct >= haut else (pct - bas) / (haut - bas))
            encaisse = avance + cum * (1 - rg) - avance * fr
        ecart = decaisse - encaisse
        if ecart > besoin_max:
            besoin_max, j_max = ecart, j
        points.append({"j": j, "decaisse_MAD": round(decaisse), "encaisse_MAD": round(encaisse),
                       "besoin_MAD": round(ecart)})
    return {
        "points": points, "besoin_maximal_MAD": round(besoin_max),
        "besoin_maximal_au_jour": j_max,
        "besoin_maximal_pct_du_marche": round(besoin_max / marche * 100, 2),
        "avance_versee_MAD": round(avance),
        "retenue_de_garantie_finale_MAD": round(marche * rg),
        "lecture": (
            "Le besoin maximal n'est pas une perte : c'est l'argent que l'entreprise avance au "
            f"maitre d'ouvrage pendant le chantier. Une avance de {ct['avance_pct']['valeur']} % "
            f"le reduit, un delai de paiement de {delai} jours l'augmente, et la retenue de "
            "garantie ne revient qu'apres la reception. Un chantier rentable peut mettre une "
            "entreprise en defaut : la marge est au bilan, la tresorerie est a la banque."),
        "hypothese_de_profil": (
            "Les decaissements suivent le profil de depense, lui-meme etale uniformement sur "
            "la duree de chaque tache. C'est faux pour les achats, payes a la commande, et "
            "pour le materiel, paye au mois : la courbe donne un ordre de grandeur du besoin, "
            "pas un plan de tresorerie. Elle est declaree comme telle (V3)."),
    }


def cout_du_retard(d: dict, bord: dict, jours: float) -> dict:
    """Ce que coute un retard : frais de duree + penalites. Deux additions, deux logiques."""
    ct = d["prix_unitaires_MAD"]["contrat"]
    fd = bord["frais_de_duree"]
    marche = bord["prix_de_vente_MAD"]
    cal = d["planning"]["calendrier"]
    # les penalites courent en jours CALENDAIRES, les frais de duree en jours ouvres
    _c = pln.calendrier(fd["duree_j"], cal)
    ratio = _c["semaines_calendaires"] * 7 / fd["duree_j"]
    j_cal = jours * ratio
    pen = marche * ct["penalite_retard_pour_mille_par_j"]["valeur"] / 1000 * j_cal
    plafond = marche * ct["penalite_plafond_pct"]["valeur"] / 100
    return {
        "retard_j_ouvres": jours, "retard_j_calendaires": round(j_cal, 1),
        "frais_de_duree_MAD": round(fd["cout_MAD_par_jour_ouvre"] * jours, 2),
        "penalites_MAD": round(min(pen, plafond), 2),
        "penalites_plafond_MAD": round(plafond, 2),
        "penalites_plafonnees": bool(pen > plafond),
        "total_MAD": round(fd["cout_MAD_par_jour_ouvre"] * jours + min(pen, plafond), 2),
        "cout_MAD_par_jour": round(
            (fd["cout_MAD_par_jour_ouvre"] * jours + min(pen, plafond)) / jours, 2),
        "piege": (
            "Les penalites se comptent en jours CALENDAIRES et les frais de duree en jours "
            "OUVRES : un retard d'un mois ouvre pese "
            f"{round(ratio, 2)} fois plus de jours de penalite que de jours de frais. "
            "Confondre les deux calendriers sous-estime la penalite d'un tiers."),
    }


def controle_ratios(d: dict, bord: dict, q: dict) -> dict:
    """Verification d'ordre de grandeur (§ 3.3), et surtout : sur QUEL perimetre.

    La dette n° 10 du projet vient d'un ratio de part de main d'oeuvre applique a une
    base ou il n'est pas defini. Un ratio a un domaine de definition, et l'ecrire est la
    moitie du travail :

      — sur un poste FORFAITAIRE, la part de main d'oeuvre n'existe pas : le montant est
        tout compris et ne se decompose pas ;
      — sur un poste de FOURNITURE, elle vaut zero par construction, et ce zero n'est pas
        une alerte ;
      — elle n'a de sens que sur les postes DECOMPOSES, et la fourchette de 15 a 30 % ne
        vaut que pour ceux d'entre eux qui sont du BETON ARME.
    """
    rc = d["prix_unitaires_MAD"]["ratios_de_controle"]
    BETON_ARME = ("FOND", "RADT", "VOIL", "PHNT", "POTR", "MEZZ")
    par_id = {p["poste"]: p for p in bord["postes"]}
    decomposes = [p for p in bord["postes"] if p["type"].startswith("unitaire")]
    ba = [par_id[i] for i in BETON_ARME]

    def part_mo(postes):
        ds = sum(p["debourse_sec_total_MAD"] for p in postes)
        mo = sum(p["main_oeuvre_totale_MAD"] for p in postes)
        return (mo / ds * 100 if ds else 0.0), ds, mo

    p_ba, ds_ba, mo_ba = part_mo(ba)
    p_dec, ds_dec, _ = part_mo(decomposes)
    p_tout = bord["part_main_oeuvre_du_debourse_pct"]
    out = {}

    def ctrl(nom, valeur, ref, unite, defini=True):
        lo, hi = ref["fourchette"]
        out[nom] = {"constate": round(valeur, 2), "attendu": ref["valeur"],
                    "fourchette": [lo, hi], "unite": unite,
                    "ratio_defini_sur_cette_base": defini,
                    "dans_la_fourchette": bool(defini and lo <= valeur <= hi)}

    ctrl("cout_par_m2_emprise", bord["cout_MAD_par_m2_emprise"],
         rc["cout_MAD_m2_batiment_voyageurs"], "MAD/m2")
    ctrl("part_main_oeuvre_beton_arme_decompose", p_ba,
         rc["part_main_oeuvre_gros_oeuvre_pct"], "%")
    ctrl("part_main_oeuvre_tous_postes_decomposes", p_dec,
         rc["part_main_oeuvre_gros_oeuvre_pct"], "%", defini=False)
    ctrl("part_main_oeuvre_bordereau_entier", p_tout,
         rc["part_main_oeuvre_gros_oeuvre_pct"], "%", defini=False)
    gros = sum(v["debourse_MAD"] for k, v in bord["par_lot"].items()
               if k.startswith(("1 ·", "2 ·", "3 ·")))
    ctrl("part_gros_oeuvre", gros / bord["debourse_sec_MAD"] * 100,
         rc["part_gros_oeuvre_pct"], "%")

    out["_perimetres"] = {
        "beton_arme_decompose": list(BETON_ARME),
        "debourse_MAD": round(ds_ba, 2), "main_oeuvre_MAD": round(mo_ba, 2),
        "tous_postes_decomposes": [p["poste"] for p in decomposes],
        "forfaits_sans_part_de_main_oeuvre": [p["poste"] for p in bord["postes"]
                                              if p["type"] == "forfait"],
    }
    out["_lecture"] = (
        f"Sur le beton arme decompose, la part de main d'oeuvre vaut {p_ba:.1f} %. Sur "
        f"l'ensemble des postes decomposes {p_dec:.1f} %, et sur le bordereau entier "
        f"{p_tout:.1f} % — mais ces deux dernieres bases ne recoivent PAS de verdict, "
        "parce que le ratio n'y est pas defini : elles melent des heures connues, des "
        "fournitures sans heures, et des forfaits dont les heures existent sans etre "
        "visibles. Le module TV comparait la derniere a la fourchette de la premiere. La "
        "base etait donc fausse — et la conclusion restait partiellement juste : voir "
        "coherence_cadences, qui attaque la question par les productivites individuelles "
        "au lieu d'un ratio global, et trouve un facteur de recalage du meme ordre que "
        "le facteur 2 a 3 soupconne par la dette n° 10.")
    return out


# ------------------------------------------------------------------ figures
def figures(d: dict, bord: dict, tres: dict, coh: dict, dep: dict, cs: list) -> dict:
    p = next(x for x in bord["postes"] if x["poste"] == "VOIL")
    mo = p["main_oeuvre"]["montant_MAD_par_unite"]
    mat = sum(x["montant_MAD"] for x in p["materiaux"])
    eng = sum(x["montant_MAD"] for x in p["materiel"])
    ds = p["debourse_sec_par_unite_MAD"]
    comp = d["prix_unitaires_MAD"]["composition_prix_pct"]
    etapes = [
        {"libelle": "Main d'oeuvre", "montant": round(mo, 1), "type": "ajout"},
        {"libelle": "Matériaux", "montant": round(mat, 1), "type": "ajout"},
        {"libelle": "Matériel", "montant": round(eng, 1), "type": "ajout"},
        {"libelle": "Déboursé sec", "montant": round(ds, 1), "type": "total"},
    ]
    cum = ds
    for cle, lib in (("frais_generaux_siege", "Frais généraux"), ("aleas", "Aléas"),
                     ("marge", "Marge")):
        m = ds * comp[cle]["valeur"] / 100
        etapes.append({"libelle": f"{lib} ({comp[cle]['valeur']} %)", "montant": round(m, 1),
                       "type": "ajout"})
        cum += m
    etapes.append({"libelle": "Prix de vente", "montant": round(cum, 1), "type": "total"})

    lots = sorted(bord["par_lot"].items(), key=lambda kv: -kv[1]["debourse_MAD"])
    return {
        "cascade": etapes,
        "lots": [{"libelle": k, "valeur": round(v["debourse_MAD"] / 1e6, 2),
                  "part": v["part_pct"]} for k, v in lots],
        "tresorerie": tres["points"],
        "recalage": [{"libelle": f"{c['poste']} · {pln.NOMS[c['poste']]}",
                      "valeur": c["facteur_de_recalage"]} for c in coh["cas"]],
        "depense_contre_travail": {
            "series": [
                {"nom": "Dépense (MAD)", "points": [{"j": p["j"], "pct": p["pct"]}
                                                    for p in dep["points"]]},
                {"nom": "Travail (jours-hommes)", "points": [{"j": p["j"], "pct": p["prevu"]}
                                                             for p in cs]},
            ]},
        "situation": ["Constat contradictoire sur site", "Attachement signé",
                      "Projet de situation", "Vérification maîtrise d'œuvre",
                      "Visa et décompte", "Ordonnancement", "Paiement"],
    }


# ------------------------------------------------------------------ tout
def tout_calculer(d: dict, duree_mezz: float, cadence_mezz: float, cycle_mezz: float) -> dict:
    pl = d["planning"]
    q = pln.quantites_chantier(d, pl)
    t = pln.durees_chantier(d, pl, q, duree_mezz)
    f = pln.planning_avec_fenetres(d, t)
    res = pln.voie_A_parcours(f["taches"])
    seg = pln.segments_de_travail(t, res, f["detail_fenetres"],
                                  pl["contraintes_exploitation"])
    eff = pln.effectifs_par_tache(d, pl, t)
    cs = pln.courbe_en_s(res, eff, seg, 5)

    bord = bordereau(d, q, t, res["duree"])
    dep = courbe_de_depense(bord, res, t)
    durees_dates = {i: {**t[i], "debut_j": res["tot"][i][0], "fin_j": res["tot"][i][1]}
                    for i in pln.NOMS}
    etats = trois_etats(d, avancement_planifie(
        seg, durees_dates, float(d["suivi_chantier"]["date_arret_j"])))
    ecart_ct = ecart_depense_travail(dep, cs)
    voie_b = voie_prix_poses(d, q)
    ecart = ecart_des_deux_voies(bord, voie_b)
    coh = coherence_cadences(d, q)
    tres = tresorerie(d, bord, dep)
    sit = situation(d, bord, etats["declare"])
    retard = {str(j): cout_du_retard(d, bord, j) for j in (1, 21, 63)}
    ctrl = controle_ratios(d, bord, q)
    var = variante_recalee(d, q, t, res["duree"], coh["facteur_de_recalage_moyen"], duree_mezz)
    return {
        "_durees_reference": {i: t[i]["duree_j"] for i in pln.NOMS},
        "quantites_bordereau": quantites_bordereau(d, q),
        "taux_horaires": {m: taux_horaire_atelier(d, m)
                          for m in pl["effectifs_chantier_V3"]["compagnons_par_atelier"]},
        "bordereau": {**bord, "par_poste": {x["poste"]: x for x in bord["postes"]}},
        "voie_prix_poses": voie_b, "ecart_des_deux_voies": ecart,
        "coherence_cadences": coh, "variante_recalee": var,
        "situation": sit, "etats_a_la_date_d_arret": etats,
        "tresorerie": tres, "cout_du_retard": retard,
        "courbe_de_depense": {k: v for k, v in dep.items() if k != "cumul"},
        "ecart_depense_travail": ecart_ct,
        "controle_ratios": ctrl,
        "figures": figures(d, bord, tres, coh, dep, cs),
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json").read_text(encoding="utf-8"))
    r = tout_calculer(d, tv["planning_plancher"]["duree_totale_j"],
                      tv["planning_plancher"]["cadence_zone_j"], tv["cycle_zone"]["duree_j"])
    b = r["bordereau"]
    # valeurs attendues des corriges : CALCULEES, jamais saisies
    voil = next(p for p in b["postes"] if p["poste"] == "VOIL")
    r["exercices"] = {
        "voile_debourse_par_m2_MAD": voil["debourse_sec_par_unite_MAD"],
        "voile_pu_vente_MAD": voil["pu_de_vente_MAD"],
        "voile_h_par_m2": voil["main_oeuvre"]["h_par_unite"],
        "voil_un_atelier_j": round(
            r["_durees_reference"]["VOIL"] * d["planning"]["effectifs_chantier_V3"]["ateliers_voiles"], 2),
        "voil_deux_ateliers_j": round(
            r["_durees_reference"]["VOIL"] * d["planning"]["effectifs_chantier_V3"]["ateliers_voiles"] / 2, 2),
        "retard_un_mois_MAD": r["cout_du_retard"]["21"]["total_MAD"],
        "besoin_tresorerie_MAD": r["tresorerie"]["besoin_maximal_MAD"],
        "revision_pct": r["situation"]["revision"]["part_de_la_revision_pct"],
    }
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "prix.json").write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n",
                                      encoding="utf-8")
    print(f"bordereau : {b['prix_de_vente_MAD']:,.0f} MAD  "
          f"({b['cout_MAD_par_m2_emprise']:,.0f} MAD/m2)  "
          f"part MO {b['part_main_oeuvre_du_debourse_pct']} %  "
          f"ecart deux voies {r['ecart_des_deux_voies']['ecart_pct']} %  "
          f"recalage moyen x{r['coherence_cadences']['facteur_de_recalage_moyen']}")
