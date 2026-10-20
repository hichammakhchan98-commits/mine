"""Planification d'un chantier de gare (module D2).

Change d'echelle, pas de methode : le plancher de mezzanine du module TV y est UNE
tache parmi vingt-cinq. Trois choses que le referentiel generique de gestion de projet
ne donne pas, et qui font ce module (§ 1.1 : le lecteur maitrise CPM, on ne le lui
reapprend pas) :

1. Les durees ne sont pas estimees : elles appartiennent a trois FAMILLES distinctes
   (calculee, imposee, declaree) qui ne se pilotent pas de la meme facon. Mettre des
   hommes sur une duree imposee ne raccourcit rien.
2. Le chemin critique d'un chantier ferroviaire n'est pas celui du reseau : c'est
   celui du reseau PLUS les fenetres de consignation accordees par l'exploitant.
3. Les ressources se lissent dans les marges ; ce que le lissage consomme, le planning
   ne l'a plus. Une marge depensee en confort est une marge perdue pour l'alea.
"""
from __future__ import annotations
import json, math, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "calc"))
from cpm import Tache, contre_calcul, voie_A_parcours     # noqa: E402


# ---------------------------------------------------------------- quantites
def quantites_chantier(d: dict, pl: dict) -> dict:
    """Quantites d'ordre de grandeur du chantier, depuis la GEOMETRIE et des ratios V3."""
    g = d["geometrie"]
    r = pl["ratios_quantites_V3"]
    L, l = g["emprise_m"]
    emprise = L * l
    nt = next(n for n in g["niveaux"] if n["nom"] == "niveau technique")
    ntL, ntl = nt["emprise_partielle_m"]
    surf_nt = ntL * ntl
    prof = abs(nt["altitude_m"]) + r["surprofondeur_forme_m"]["valeur"]

    # poteaux : 4 files longitudinales (rives + bords du hall), une file par trame
    n_files = 4
    n_trames = g["nb_travees_longitudinales"] + 1
    n_poteaux = n_files * n_trames
    h_rdc = next(n for n in g["niveaux"] if n["nom"].startswith("RDC"))["h_libre_m"]

    decapage = emprise * r["decapage_m"]["valeur"]
    fouille = surf_nt * prof
    deblais = (decapage + fouille) * (1 + r["foisonnement_pct"]["valeur"] / 100)

    # voiles perimetriques du niveau technique
    peri_nt = 2 * (ntL + ntl)
    voiles_m2 = peri_nt * nt["h_libre_m"]

    mz = g["mezzanine"]["zones_de_coulage"]
    surf_mezz = mz["nb_zones"] * mz["longueur_zone_m"] * mz["largeur_zone_m"]
    surf_couverture = emprise
    charpente_t = surf_couverture * r["charpente_kg_m2"]["valeur"] / 1000.0
    facade_m2 = 2 * (L + l) * r["facade_hauteur_m"]["valeur"]

    return {
        "emprise_m2": round(emprise, 1),
        "decapage_m3": round(decapage, 1),
        "fouille_niveau_technique_m3": round(fouille, 1),
        "deblais_transportes_m3": round(deblais, 1),
        "n_poteaux": n_poteaux,
        "hauteur_poteau_rdc_m": h_rdc,
        "beton_semelles_m3": round(n_poteaux * r["semelle_m3_par_poteau"]["valeur"], 1),
        "beton_poteaux_rdc_m3": round(n_poteaux * h_rdc * r["poteau_section_m2"]["valeur"], 1),
        "surface_niveau_technique_m2": round(surf_nt, 1),
        "beton_radier_m3": round(surf_nt * r["radier_niveau_technique_m"]["valeur"], 1),
        "beton_plancher_haut_nt_m3": round(surf_nt * r["dalle_niveau_technique_m"]["valeur"], 1),
        "voiles_niveau_technique_m2": round(voiles_m2, 1),
        "surface_mezzanine_m2": round(surf_mezz, 1),
        "surface_couverture_m2": round(surf_couverture, 1),
        "charpente_t": round(charpente_t, 1),
        "facade_m2": round(facade_m2, 1),
    }


# ---------------------------------------------------------------- durees
def _cal(q, cad, ateliers):
    return q / (cad * ateliers)


def durees_chantier(d: dict, pl: dict, q: dict, duree_mezzanine_j: float) -> dict:
    """Chaque duree porte sa FAMILLE. C'est la colonne la plus utile du tableau."""
    c, e = pl["cadences_chantier_V3"], pl["effectifs_chantier_V3"]
    f, i_ = pl["forfaits_V3"], pl["delais_imposes_V3"]
    out = {}

    def calculee(id_, j, formule):
        out[id_] = {"duree_j": round(j, 2), "famille": "calculee", "formule": formule}

    def imposee(id_, cle):
        out[id_] = {"duree_j": float(i_[cle]["valeur"]), "famille": "imposee",
                    "fourchette": i_[cle]["fourchette"], "source": cle}

    def declaree(id_, cle):
        out[id_] = {"duree_j": float(f[cle]["valeur"]), "famille": "declaree",
                    "fourchette": f[cle]["fourchette"], "source": cle}

    declaree("INST", "installation_chantier_j")
    declaree("GRUE", "montage_grue_j")
    declaree("TOPO", "implantation_j")
    calculee("TERR", _cal(q["decapage_m3"], c["terrassement_m3_j_atelier"]["valeur"],
                          e["ateliers_terrassement"]),
             "decapage_m3 / (terrassement_m3_j_atelier x ateliers_terrassement)")
    calculee("FOUI", _cal(q["fouille_niveau_technique_m3"], c["terrassement_m3_j_atelier"]["valeur"],
                          e["ateliers_terrassement"]),
             "fouille_m3 / (terrassement_m3_j_atelier x ateliers_terrassement)")
    declaree("SOUT", "soutenement_j")
    # le moteur d'une semelle isolee n'est pas son volume mais son NOMBRE : implantation,
    # coffrage, cage et coulage se refont a chaque unite, quelle que soit sa taille
    calculee("FOND", _cal(q["n_poteaux"], c["semelle_unites_j_atelier"]["valeur"],
                          e["ateliers_fondations"]),
             "n_poteaux / (semelle_unites_j_atelier x ateliers_fondations)")
    calculee("RADT", _cal(q["surface_niveau_technique_m2"], c["dalle_pleine_m2_j_atelier"]["valeur"],
                          e["ateliers_fondations"]),
             "surface_niveau_technique_m2 / (dalle_pleine_m2_j_atelier x ateliers_fondations)")
    calculee("VOIL", _cal(q["voiles_niveau_technique_m2"], c["voile_m2_j_atelier"]["valeur"],
                          e["ateliers_voiles"]),
             "voiles_m2 / (voile_m2_j_atelier x ateliers_voiles)")
    calculee("PHNT", _cal(q["surface_niveau_technique_m2"], c["dalle_pleine_m2_j_atelier"]["valeur"],
                          e["ateliers_fondations"]),
             "surface_niveau_technique_m2 / (dalle_pleine_m2_j_atelier x ateliers_fondations)")
    declaree("ETAN", "etancheite_remblais_j")
    calculee("POTR", _cal(q["n_poteaux"], c["poteau_unites_j_atelier"]["valeur"],
                          e["ateliers_poteaux"]),
             "n_poteaux / (poteau_unites_j_atelier x ateliers_poteaux)")
    # la mezzanine ne se redivise pas : sa duree VIENT du module TV, par la meme chaine
    out["MEZZ"] = {"duree_j": round(duree_mezzanine_j, 2), "famille": "calculee",
                   "formule": "(nb_zones - 1) x cadence + cycle — sortie du module TV"}
    declaree("NOYX", "noyaux_escaliers_j")
    imposee("CHET", "etudes_et_visa_charpente_j")
    imposee("CHFA", "fabrication_charpente_j")
    part = pl["contraintes_exploitation"]["part_levage_sous_consignation_pct"]["valeur"] / 100
    t_total = q["charpente_t"]
    j_total = _cal(t_total, c["charpente_t_j_atelier"]["valeur"], e["ateliers_charpente"])
    calculee("CHAP", j_total * (1 - part),
             "charpente_t x (1 - part sous consignation) / (charpente_t_j_atelier x ateliers)")
    calculee("CHLV", j_total * part,
             "charpente_t x part sous consignation / (charpente_t_j_atelier x ateliers)")
    calculee("COUV", _cal(q["surface_couverture_m2"], c["couverture_m2_j_atelier"]["valeur"],
                          e["ateliers_couverture"]),
             "surface_couverture_m2 / (couverture_m2_j_atelier x ateliers_couverture)")
    calculee("FACA", _cal(q["facade_m2"], c["facade_m2_j_atelier"]["valeur"],
                          e["ateliers_facade"]),
             "facade_m2 / (facade_m2_j_atelier x ateliers_facade)")
    declaree("MARQ", "marquise_j")
    declaree("PSOU", "passage_souterrain_j")
    declaree("QUAI", "quais_equipements_j")
    imposee("SECH", "sechage_avant_second_oeuvre_j")
    declaree("SECO", "second_oeuvre_lots_techniques_j")
    declaree("ESSA", "essais_mise_en_service_j")
    declaree("RECE", "reception_j")
    return out


NOMS = {
    "INST": "Installation de chantier", "GRUE": "Montage de la grue à tour",
    "TOPO": "Implantation topographique", "TERR": "Terrassement général",
    "FOUI": "Fouille du niveau technique", "SOUT": "Soutènement périphérique",
    "FOND": "Semelles et longrines", "RADT": "Radier du niveau technique",
    "VOIL": "Voiles du niveau technique", "PHNT": "Plancher haut niveau technique",
    "ETAN": "Étanchéité et remblais", "POTR": "Poteaux du RDC (9 m)",
    "MEZZ": "Plancher de mezzanine (8 zones)", "NOYX": "Noyaux et escaliers",
    "CHET": "Études, visa et approbation de la charpente", "CHFA": "Fabrication de la charpente en atelier",
    "CHAP": "Pré-assemblage et levage hors voie", "CHLV": "Levage au-dessus de la voie (consignation)",
    "COUV": "Pannes, bac et étanchéité de couverture", "FACA": "Façades vitrées",
    "MARQ": "Marquise en porte-à-faux", "PSOU": "Raccordement du passage souterrain (consignation)",
    "QUAI": "Quais et équipements", "SECH": "Séchage avant second œuvre",
    "SECO": "Second œuvre et lots techniques", "ESSA": "Essais et mise en service",
    "RECE": "Réception",
}

LOT = {
    "INST": "0 · Préparation", "GRUE": "0 · Préparation", "TOPO": "0 · Préparation",
    "TERR": "1 · Terrassements", "FOUI": "1 · Terrassements", "SOUT": "1 · Terrassements",
    "FOND": "2 · Infrastructure", "RADT": "2 · Infrastructure", "VOIL": "2 · Infrastructure",
    "PHNT": "2 · Infrastructure", "ETAN": "2 · Infrastructure",
    "POTR": "3 · Superstructure", "MEZZ": "3 · Superstructure", "NOYX": "3 · Superstructure",
    "CHET": "4 · Charpente", "CHFA": "4 · Charpente", "CHAP": "4 · Charpente", "CHLV": "4 · Charpente",
    "COUV": "5 · Clos et couvert", "FACA": "5 · Clos et couvert", "MARQ": "5 · Clos et couvert",
    "PSOU": "6 · Interfaces ferroviaires", "QUAI": "6 · Interfaces ferroviaires",
    "SECH": "7 · Finitions", "SECO": "7 · Finitions", "ESSA": "8 · Réception", "RECE": "8 · Réception",
}

# (tache, [(predecesseur, decalage)]) — decalage negatif = recouvrement
LIENS = {
    "INST": [], "CHET": [],
    "GRUE": [("INST", -5.0)], "TOPO": [("INST", -8.0)],
    "TERR": [("TOPO", 0.0)], "FOUI": [("TERR", -2.0)], "SOUT": [("FOUI", -4.0)],
    "FOND": [("FOUI", 0.0), ("SOUT", 0.0), ("GRUE", 0.0)],
    "RADT": [("FOND", -3.0)], "VOIL": [("RADT", 0.0)], "PHNT": [("VOIL", 0.0)],
    "ETAN": [("PHNT", 0.0)],
    "POTR": [("PHNT", 0.0)], "MEZZ": [("POTR", -4.0)], "NOYX": [("PHNT", 0.0)],
    "CHFA": [("CHET", 0.0)],
    "CHAP": [("CHFA", 0.0), ("MEZZ", 0.0)], "CHLV": [("CHAP", 0.0)],
    "COUV": [("CHLV", 0.0)], "FACA": [("CHLV", -6.0)], "MARQ": [("MEZZ", 0.0), ("CHAP", 0.0)],
    "PSOU": [("ETAN", 0.0)], "QUAI": [("PSOU", 0.0)],
    "SECH": [("COUV", 0.0), ("FACA", 0.0)], "SECO": [("SECH", 0.0), ("NOYX", 0.0), ("MARQ", 0.0)],
    "ESSA": [("SECO", 0.0), ("QUAI", 0.0)], "RECE": [("ESSA", 0.0)],
}


def reseau(durees: dict) -> list:
    return [Tache(i, NOMS[i], durees[i]["duree_j"], LIENS[i]) for i in NOMS]


# ------------------------------------------------- contraintes d'exploitation
def prochaine_fenetre(j: float, premiere: float, periode: float) -> float:
    """Debut de la premiere fenetre de consignation disponible a partir du jour j."""
    if j <= premiere:
        return premiere
    k = math.ceil((j - premiere) / periode)
    return premiere + k * periode


def etalement_sous_fenetres(duree: float, debut_au_plus_tot: float,
                            fenetre: float, periode: float, premiere: float) -> dict:
    """Une tache qui ne peut travailler que pendant les consignations.

    Elle ne dure pas plus longtemps : elle s'ETALE. La distinction compte, parce que
    l'effectif ne change ni l'un ni l'autre, et parce que le cout, lui, suit la duree
    de travail alors que le delai suit l'etalement.
    """
    n = max(1, math.ceil(round(duree / fenetre, 6)))
    debut = prochaine_fenetre(debut_au_plus_tot, premiere, periode)
    reste = duree - (n - 1) * fenetre
    fin = debut + (n - 1) * periode + reste
    return {"debut": round(debut, 2), "fin": round(fin, 2),
            "duree_de_travail_j": round(duree, 2),
            "etalement_j": round(fin - debut, 2),
            "attente_avant_premiere_fenetre_j": round(debut - debut_au_plus_tot, 2),
            "nb_fenetres": n,
            "immobilisation_improductive_j": round((fin - debut) - duree, 2)}


def planning_avec_fenetres(durees: dict, ce: dict, iterations: int = 30) -> dict:
    """Point fixe : la fenetre depend de la date, la date depend de la fenetre.

    On recalcule le reseau avec les durees ETALEES jusqu'a ce que les dates ne bougent
    plus. Sans cette boucle, on appliquerait la fenetre a une date au plus tot qui
    n'existe deja plus.
    """
    fen, per = ce["fenetre_jours"]["valeur"], ce["periode_entre_fenetres_jours"]["valeur"]
    prem = ce["premiere_fenetre_jour"]
    soumises = ce["taches_soumises"]
    etale = {i: durees[i]["duree_j"] for i in durees}
    detail = {}
    for _ in range(iterations):
        r = voie_A_parcours([Tache(i, NOMS[i], etale[i], LIENS[i]) for i in NOMS])
        change = False
        for i in soumises:
            d0 = r["tot"][i][0]
            e = etalement_sous_fenetres(durees[i]["duree_j"], d0, fen, per, prem)
            if abs(e["etalement_j"] - etale[i]) > 1e-6:
                etale[i], change = e["etalement_j"], True
            detail[i] = e
        if not change:
            break
    taches = [Tache(i, NOMS[i], etale[i], LIENS[i]) for i in NOMS]
    cc = contre_calcul(taches)
    return {"durees_etalees": {i: round(etale[i], 2) for i in soumises},
            "detail_fenetres": detail, "contre_calcul": cc, "taches": taches}


# ------------------------------------------------------------- marges
def marges(res: dict, durees: dict) -> dict:
    """Marge totale (donnee par le parcours) et marge LIBRE (recalculee ici).

    La distinction n'est pas academique : consommer une marge totale decale les
    successeurs, consommer une marge libre ne decale personne. C'est elle qu'un
    conducteur de travaux peut depenser sans rien demander a quiconque.
    """
    tot = res["tot"]
    succ = {i: [] for i in NOMS}
    for i, preds in LIENS.items():
        for p, dec in preds:
            succ[p].append((i, dec))
    out = {}
    for i in NOMS:
        mt = res["marges"][i]
        if succ[i]:
            ml = min(tot[s][0] - dec - tot[i][1] for s, dec in succ[i])
        else:
            ml = res["duree"] - tot[i][1]
        out[i] = {"marge_totale_j": round(mt, 2), "marge_libre_j": round(max(0.0, ml), 2),
                  "critique": abs(mt) < 1e-9}
    return out


# ------------------------------------------------------------- ressources
def effectifs_par_tache(d: dict, pl: dict, durees: dict) -> dict:
    """Effectif present sur le chantier, tache par tache.

    Calculee -> ateliers x compagnons par atelier. Declaree -> valeur V3 posee.
    Trois taches valent zero et c'est voulu : etudes, fabrication en atelier et
    sechage n'occupent personne sur le chantier.
    """
    e = pl["effectifs_chantier_V3"]
    pose, cpa = e["effectif_par_tache"], e["compagnons_par_atelier"]
    ateliers = {"TERR": ("terrassement", "ateliers_terrassement"),
                "FOUI": ("terrassement", "ateliers_terrassement"),
                "FOND": ("fondations", "ateliers_fondations"),
                "RADT": ("fondations", "ateliers_fondations"),
                "PHNT": ("fondations", "ateliers_fondations"),
                "VOIL": ("voiles", "ateliers_voiles"),
                "POTR": ("poteaux", "ateliers_poteaux"),
                "CHAP": ("charpente", "ateliers_charpente"),
                "CHLV": ("charpente", "ateliers_charpente"),
                "COUV": ("couverture", "ateliers_couverture"),
                "FACA": ("facade", "ateliers_facade")}
    out = {}
    for i in NOMS:
        if i in ateliers:
            metier, cle = ateliers[i]
            out[i] = cpa[metier] * e[cle]
        elif i == "MEZZ":
            f = d["effectifs"]
            out[i] = (f["coffreurs"] + f["ferrailleurs_dalle"] + f["ferrailleurs_poutres"]
                      + f["equipe_betonnage"] + f["chef_equipe"] + f["grutier"])
        else:
            out[i] = pose[i]
    return out


def histogramme_effectifs(res: dict, eff: dict, decalages: dict | None = None) -> list:
    """Effectif present chaque jour. Les taches se recouvrent : on les somme."""
    dec = decalages or {}
    fin = int(math.ceil(res["duree"])) + 1
    jours = []
    for k in range(fin):
        n = 0
        for i in NOMS:
            deb = res["tot"][i][0] + dec.get(i, 0.0)
            if deb <= k < deb + (res["tot"][i][1] - res["tot"][i][0]):
                n += eff[i]
        jours.append(n)
    return jours


def lisser(res: dict, eff: dict, mg: dict, passes: int = 4) -> dict:
    """Lissage : on DECALE les taches non critiques dans leur marge pour abaisser la
    pointe. Aucune duree ne change, aucune date de fin ne bouge.

    C'est une heuristique gloutonne, pas un optimum : le lissage de ressources est un
    probleme combinatoire. Elle est declaree comme telle (§ R6), et le module dit ce
    qu'elle ne garantit pas.
    """
    base = histogramme_effectifs(res, eff)
    dec = {i: 0.0 for i in NOMS}
    meilleure = max(base)
    for _ in range(passes):
        bouge = False
        for i in sorted(NOMS, key=lambda x: -eff[x]):
            m = mg[i]["marge_totale_j"]
            if m < 1e-9 or eff[i] == 0:
                continue
            for pas in range(1, int(m) + 1):
                essai = dict(dec); essai[i] = float(pas)
                p = max(histogramme_effectifs(res, eff, essai))
                if p < meilleure - 1e-9:
                    meilleure, dec, bouge = p, essai, True
        if not bouge:
            break
    lisse = histogramme_effectifs(res, eff, dec)
    utiles = [x for x in base if x > 0]
    utiles_l = [x for x in lisse if x > 0]
    return {
        "pointe_avant": max(base), "pointe_apres": max(lisse),
        "moyenne_avant": round(sum(base) / max(1, len(utiles)), 1),
        "moyenne_apres": round(sum(lisse) / max(1, len(utiles_l)), 1),
        "gain_de_pointe_pct": round((max(base) - max(lisse)) / max(base) * 100, 1),
        "decalages_utilises_j": {i: v for i, v in dec.items() if v},
        "marge_totale_consommee_j": round(sum(dec.values()), 1),
        "histogramme_brut": base, "histogramme_lisse": lisse,
        "limite": ("Heuristique gloutonne : elle abaisse la pointe, elle ne prouve pas "
                   "qu'aucune autre combinaison ne ferait mieux. Et ce qu'elle depense "
                   "en marge totale n'est plus disponible pour l'alea."),
    }


# ------------------------------------------------- ligne d'equilibre (taches repetitives)
def ligne_equilibre(nb_zones: int, cadence: float, cycle: float, debut: float) -> dict:
    """Ligne d'equilibre du plancher de mezzanine.

    Le Gantt montre une barre par zone ; la ligne d'equilibre montre la PENTE, qui est
    la cadence. Sur des taches repetitives c'est la seule representation ou un retard
    de cadence se voit avant d'avoir coute : deux droites qui se rapprochent annoncent
    une collision d'equipes, bien avant que le Gantt ne la montre.
    """
    debuts = [debut + i * cadence for i in range(nb_zones)]
    return {
        "zones": [{"zone": i + 1, "debut_j": round(debuts[i], 2),
                   "fin_j": round(debuts[i] + cycle, 2)} for i in range(nb_zones)],
        "cadence_j_par_zone": round(cadence, 2),
        "pente_zones_par_j": round(1 / cadence, 3),
        "duree_totale_j": round((nb_zones - 1) * cadence + cycle, 2),
        "zones_simultanees": max(1, math.ceil(cycle / cadence)),
    }


# ------------------------------------------------------------- calendrier
JOURS_OUVRES_PAR_MOIS = 21.7          # moyenne d'une annee de 5 jours ouvres sur 7


def calendrier(duree_ouvree: float, cal: dict) -> dict:
    """Du jour ouvre a la date civile, et l'ecart que les intemperies y creusent.

    Un planning se calcule en jours ouvres et se CONTRACTE en dates. Entre les deux il
    y a deux conversions, et chacune allonge : les week-ends, puis les jours ou la grue
    ne tourne pas. Les oublier est l'erreur qui fait signer un delai intenable.
    """
    import datetime as dt
    jours_sem = cal["jours_ouvres_par_semaine"]
    inter = cal["jours_non_ouvres_par_mois_intemperies"]["valeur"]
    facteur = JOURS_OUVRES_PAR_MOIS / (JOURS_OUVRES_PAR_MOIS - inter)
    ouvres_avec_alea = duree_ouvree * facteur

    def civile(n_ouvres):
        d0 = dt.date.fromisoformat(cal["origine"])
        restant, j = n_ouvres, d0
        while restant > 0:
            j += dt.timedelta(days=1)
            if j.weekday() < jours_sem:
                restant -= 1
        return j

    fin_sec = civile(math.ceil(duree_ouvree))
    fin_alea = civile(math.ceil(ouvres_avec_alea))
    return {
        "origine": cal["origine"],
        "duree_ouvree_j": round(duree_ouvree, 1),
        "duree_ouvree_avec_intemperies_j": round(ouvres_avec_alea, 1),
        "facteur_intemperies": round(facteur, 3),
        "jours_perdus_intemperies_j": round(ouvres_avec_alea - duree_ouvree, 1),
        "fin_sans_alea": fin_sec.isoformat(),
        "fin_avec_alea": fin_alea.isoformat(),
        "semaines_calendaires": round((fin_alea - dt.date.fromisoformat(cal["origine"])).days / 7, 1),
        "mois_calendaires": round((fin_alea - dt.date.fromisoformat(cal["origine"])).days / 30.4, 1),
    }


# ------------------------------------------------------------- courbe en S
def courbe_en_s(res: dict, eff: dict, pas: int = 1) -> list:
    """Avancement en % des jours-hommes, date par date.

    L'assiette n'est pas le nombre de taches finies ni le temps ecoule : c'est le
    travail consomme. Une courbe batie sur le temps serait une droite, et une droite
    n'est pas une courbe en S.
    """
    fin = int(math.ceil(res["duree"]))
    total = sum(eff[i] * (res["tot"][i][1] - res["tot"][i][0]) for i in NOMS)
    pts = []
    for k in range(0, fin + 1, pas):
        acc = 0.0
        for i in NOMS:
            deb, f = res["tot"][i]
            if k >= f:
                acc += eff[i] * (f - deb)
            elif k > deb:
                acc += eff[i] * (k - deb)
        pts.append({"j": k, "prevu": round(acc / total * 100, 1) if total else 0.0})
    return pts


# ------------------------------------------- contre-calcul n° 2, hors CPM
def contre_calcul_chemin(res: dict, chemin: list, durees_etalees: dict) -> dict:
    """Seconde voie, qui n'est PAS un second algorithme de CPM.

    On additionne a la main les durees et les decalages du chemin annonce critique.
    Si la somme ne rend pas la duree du projet, c'est que le chemin publie n'est pas
    celui qui porte la duree — une erreur qu'aucune des deux voies de `cpm.py` ne voit,
    puisqu'elles partagent le meme reseau.
    """
    total, detail = 0.0, []
    for k, i in enumerate(chemin):
        dec = 0.0
        if k:
            dec = dict(LIENS[i]).get(chemin[k - 1], 0.0)
        d = durees_etalees.get(i, 0.0)
        total += d + dec
        detail.append({"tache": i, "duree_j": round(d, 2), "decalage_j": dec,
                       "cumul_j": round(total, 2)})
    ecart = abs(total - res["duree"])
    return {"somme_du_chemin_j": round(total, 2), "duree_du_reseau_j": round(res["duree"], 2),
            "ecart_j": round(ecart, 6), "detail": detail,
            "verdict": "OK" if ecart <= 1e-6 else
                       "LE CHEMIN PUBLIE NE PORTE PAS LA DUREE DU PROJET"}


# ------------------------------------------------- variantes des exercices
def variante(d: dict, pl: dict, duree_mezz: float, **modifs) -> dict:
    """Rejoue TOUT le calcul avec une hypothese changee.

    Les valeurs attendues d'un corrige ne se tapent pas : elles se calculent. C'est la
    lecon que la passe adversariale du module TV a imposee, ou une division fausse
    saisie a la main avait fini par inverser une recommandation d'ingenierie.
    """
    import copy
    pl2 = copy.deepcopy(pl)
    ce = pl2["contraintes_exploitation"]
    if "fenetre_jours" in modifs:
        ce["fenetre_jours"]["valeur"] = modifs["fenetre_jours"]
    if "part_consignation_pct" in modifs:
        ce["part_levage_sous_consignation_pct"]["valeur"] = modifs["part_consignation_pct"]
    if "periode_jours" in modifs:
        ce["periode_entre_fenetres_jours"]["valeur"] = modifs["periode_jours"]
    for cle, val in modifs.get("ateliers", {}).items():
        pl2["effectifs_chantier_V3"][cle] = val

    q = quantites_chantier(d, pl2)
    t = durees_chantier(d, pl2, q, duree_mezz)
    f = planning_avec_fenetres(t, ce)
    res = voie_A_parcours(f["taches"])
    return {"duree_projet_j": round(res["duree"], 2),
            "chemin_critique": f["contre_calcul"]["chemin_critique"],
            "etalement_levage_j": round(f["detail_fenetres"]["CHLV"]["etalement_j"], 2),
            "travail_levage_j": round(f["detail_fenetres"]["CHLV"]["duree_de_travail_j"], 2),
            "nb_fenetres_levage": f["detail_fenetres"]["CHLV"]["nb_fenetres"],
            "duree_poteaux_j": round(t["POTR"]["duree_j"], 2),
            "duree_mezzanine_j": round(t["MEZZ"]["duree_j"], 2)}


# ------------------------------------------------------------- sortie
def tout_calculer(d: dict, pl: dict, duree_mezzanine_j: float, cadence_mezz: float,
                  cycle_mezz: float) -> dict:
    q = quantites_chantier(d, pl)
    t = durees_chantier(d, pl, q, duree_mezzanine_j)

    sans = contre_calcul(reseau(t))
    f = planning_avec_fenetres(t, pl["contraintes_exploitation"])
    res = voie_A_parcours(f["taches"])
    etalees = {x.id: x.duree for x in f["taches"]}
    mg = marges(res, t)
    eff = effectifs_par_tache(d, pl, t)
    lis = lisser(res, eff, mg)
    cal = calendrier(res["duree"], pl["calendrier"])
    cc2 = contre_calcul_chemin(res, f["contre_calcul"]["chemin_critique"], etalees)
    leq = ligne_equilibre(d["geometrie"]["mezzanine"]["zones_de_coulage"]["nb_zones"],
                          cadence_mezz, cycle_mezz, res["tot"]["MEZZ"][0])

    par_famille = {}
    for i, v in t.items():
        par_famille.setdefault(v["famille"], []).append(i)
    somme = {k: round(sum(t[i]["duree_j"] for i in v), 1) for k, v in par_famille.items()}
    crit = f["contre_calcul"]["taches_critiques_voie_A"]
    crit_par_famille = {k: round(sum(etalees[i] for i in v if i in crit), 1)
                        for k, v in par_famille.items()}

    lots = []
    for lot in sorted(set(LOT.values())):
        lots.append({"lot": lot, "taches": [
            {"id": i, "nom": NOMS[i], "duree": t[i]["duree_j"], "famille": t[i]["famille"]}
            for i in NOMS if LOT[i] == lot]})

    sous_reseau = ["CHET", "CHFA", "MEZZ", "CHAP", "CHLV", "COUV", "FACA", "MARQ",
                   "SECH", "SECO", "ESSA", "RECE"]
    noeuds = [{"id": i, "duree": etalees[i], "marge": mg[i]["marge_totale_j"],
               "critique": mg[i]["critique"]} for i in sous_reseau]
    liens = [{"de": p, "vers": i, "critique": mg[i]["critique"] and mg[p]["critique"]}
             for i in sous_reseau for p, _ in LIENS[i] if p in sous_reseau]

    return {
        "quantites": q,
        "durees": {i: {**t[i], "duree_etalee_j": round(etalees[i], 2), **mg[i],
                       "debut_j": round(res["tot"][i][0], 2),
                       "fin_j": round(res["tot"][i][1], 2),
                       "nom": NOMS[i], "lot": LOT[i]} for i in NOMS},
        "familles": {"nb_taches": {k: len(v) for k, v in par_famille.items()},
                     "somme_des_durees_j": somme,
                     "sur_le_chemin_critique_j": crit_par_famille,
                     "part_imposee_du_chemin_pct": round(
                         crit_par_famille.get("imposee", 0) / res["duree"] * 100, 1)},
        "reseau": {
            "duree_sans_contrainte_j": sans["voie_A_parcours_avant_arriere_j"],
            "duree_avec_fenetres_j": round(res["duree"], 2),
            "surcout_de_delai_j": round(res["duree"] - sans["voie_A_parcours_avant_arriere_j"], 2),
            "surcout_de_delai_pct": round(
                (res["duree"] - sans["voie_A_parcours_avant_arriere_j"])
                / sans["voie_A_parcours_avant_arriere_j"] * 100, 1),
            "chemin_critique": f["contre_calcul"]["chemin_critique"],
            "nb_taches_critiques": len(crit),
            "contre_calcul_cpm": f["contre_calcul"],
            "contre_calcul_chemin": cc2,
        },
        "consignations": f["detail_fenetres"],
        "ressources": lis,
        "calendrier": cal,
        "ligne_equilibre": leq,
        "variantes": {},
        "exercices": {},
        "figures": {
            "wbs": lots,
            "reseau": {"noeuds": noeuds, "liens": liens},
            "gantt": [{"nom": f"{i} · {NOMS[i]}", "debut": round(res["tot"][i][0], 2),
                       "duree": round(etalees[i], 2), "critique": mg[i]["critique"]}
                      for i in NOMS],
            "ligne_equilibre": leq,
            "effectifs": [{"j": k, "n": n} for k, n in enumerate(lis["histogramme_brut"])],
            "effectifs_lisses": [{"j": k, "n": n} for k, n in enumerate(lis["histogramme_lisse"])],
            "courbe_s": courbe_en_s(res, eff, 5),
        },
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    pl = d["planning"]
    tv = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json").read_text(encoding="utf-8"))
    r = tout_calculer(d, pl, tv["planning_plancher"]["duree_totale_j"],
                      tv["planning_plancher"]["cadence_zone_j"], tv["cycle_zone"]["duree_j"])
    dm = tv["planning_plancher"]["duree_totale_j"]
    # valeurs attendues des corriges : CALCULEES, jamais saisies
    q0 = r["quantites"]
    c0 = pl["cadences_chantier_V3"]
    e0 = pl["effectifs_chantier_V3"]
    r["exercices"] = {
        "terrassement_un_atelier_j": round(
            q0["decapage_m3"] / c0["terrassement_m3_j_atelier"]["valeur"], 2),
        "terrassement_deux_ateliers_j": round(
            q0["decapage_m3"] / (c0["terrassement_m3_j_atelier"]["valeur"] * 2), 2),
        "poteaux_deux_ateliers_j": round(
            q0["n_poteaux"] / (c0["poteau_unites_j_atelier"]["valeur"] * 2), 2),
        "poteaux_trois_ateliers_j": round(
            q0["n_poteaux"] / (c0["poteau_unites_j_atelier"]["valeur"] * 3), 2),
        "gain_poteaux_j": round(
            q0["n_poteaux"] / (c0["poteau_unites_j_atelier"]["valeur"] * 2)
            - q0["n_poteaux"] / (c0["poteau_unites_j_atelier"]["valeur"] * 3), 2),
        "charpente_etudes_plus_fabrication_j": round(
            pl["delais_imposes_V3"]["etudes_et_visa_charpente_j"]["valeur"]
            + pl["delais_imposes_V3"]["fabrication_charpente_j"]["valeur"], 1),
    }
    r["variantes"] = {
        "reference": variante(d, pl, dm),
        "fenetre_longue": variante(d, pl, dm, fenetre_jours=10),
        "moins_de_levage_sur_voie": variante(d, pl, dm, part_consignation_pct=15),
        "protection_de_voie": variante(d, pl, dm, part_consignation_pct=0.001),
        "deux_ateliers_charpente": variante(d, pl, dm, ateliers={"ateliers_charpente": 2}),
        "poteaux_trois_ateliers": variante(d, pl, dm, ateliers={"ateliers_poteaux": 3}),
    }
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "planification.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"duree_j": r["reseau"]["duree_avec_fenetres_j"],
                      "fin": r["calendrier"]["fin_avec_alea"]}, ensure_ascii=False))
