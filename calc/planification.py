"""Planification d'un chantier de gare (module D2).

Change d'echelle, pas de methode : le plancher de mezzanine du module TV y est UNE
tache parmi vingt-sept. Trois choses que le referentiel generique de gestion de projet
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
import plage as pg                                                      # noqa: E402
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
    # Une journee de consignation n'est PAS une journee de travail. Entre la prise de
    # possession et la restitution, une part fixe est consommee — prise de possession,
    # consignation catenaire, amenee, repli, deconsignation, marge de restitution — et
    # deux de ces postes appartiennent a l'exploitant. Sur une plage de nuit, le travail
    # effectif tombe sous la moitie, et la cadence de nuit perd encore. Les deux effets
    # se MULTIPLIENT : le facteur se lit dans calc/plage.py, qui le tient aussi pour B7c
    # (D-039 — une grandeur, un seul endroit).
    #
    # Avant cette correction, D2 donnait a CHLV la duree d'un travail de jour et la
    # logeait dans des fenetres de consignation comme si elles produisaient huit heures.
    facteur = pg.facteur_d_interception(d, heures_par_jour=pl["calendrier"]["heures_par_jour"])
    calculee("CHLV", j_total * part * facteur,
             "charpente_t x part sous consignation / (charpente_t_j_atelier x ateliers) "
             "x facteur d'interception (rendement de plage x abattement de nuit)")
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

# (tache, [(predecesseur, cle_de_recouvrement | None)]).
#
# Le recouvrement n'est PLUS un nombre de jours : c'est une cle de
# `planning.recouvrements_pct`, resolue par `liens_resolus()` en pourcentage de la duree
# du PREDECESSEUR. Deux raisons, toutes deux trouvees par la passe adversariale :
#   — un decalage en jours ignore la duree qu'il recouvre, et faisait demarrer deux
#     successeurs AVANT leur predecesseur (bloquant B7) ;
#   — la sequence terrassement etait l'inverse de ce que la rubrique securite ecrit :
#     le soutenement suivait la fouille. Il la precede maintenant (bloquant B6).
LIENS = {
    "INST": [], "CHET": [],
    "GRUE": [("INST", "grue_sur_installation")],
    "TOPO": [("INST", "topographie_sur_installation")],
    "TERR": [("TOPO", None)],
    # securite (§ 3.4) : la paroi se realise depuis la plateforme decapee, PUIS on
    # approfondit a son abri. La fouille ne precede jamais le soutenement.
    "SOUT": [("TERR", "soutenement_sur_decapage")],
    "FOUI": [("SOUT", "fouille_sur_soutenement")],
    "FOND": [("FOUI", None), ("GRUE", None)],
    "RADT": [("FOND", "radier_sur_fondations")], "VOIL": [("RADT", None)],
    "PHNT": [("VOIL", None)], "ETAN": [("PHNT", None)],
    "POTR": [("PHNT", None)], "MEZZ": [("POTR", "mezzanine_sur_poteaux")],
    "NOYX": [("PHNT", None)],
    "CHFA": [("CHET", None)],
    "CHAP": [("CHFA", None), ("MEZZ", None)], "CHLV": [("CHAP", None)],
    "COUV": [("CHLV", None)], "FACA": [("CHLV", "facade_sur_levage")],
    "MARQ": [("MEZZ", None), ("CHAP", None)],
    "PSOU": [("ETAN", None)], "QUAI": [("PSOU", None)],
    "SECH": [("COUV", None), ("FACA", None)],
    "SECO": [("SECH", None), ("NOYX", None), ("MARQ", None)],
    "ESSA": [("SECO", None), ("QUAI", None)], "RECE": [("ESSA", None)],
}


def liens_resolus(d: dict, durees: dict) -> dict:
    """Transforme les cles de recouvrement en decalages, en jours.

    Et verifie l'invariant que le bloquant B7 violait : un recouvrement ne peut pas
    depasser la duree du predecesseur, sans quoi le successeur demarre avant lui. Avec
    des pourcentages borne a 100 %, l'invariant est vrai par construction — le controle
    reste la pour le cas ou quelqu'un reecrirait un decalage en dur.
    """
    pct = d["planning"]["recouvrements_pct"]
    out = {}
    for i, liens in LIENS.items():
        resolus = []
        for pred, cle in liens:
            if cle is None:
                dec = 0.0
            else:
                part = pct[cle]["valeur"] / 100.0
                if not 0.0 <= part <= 1.0:
                    raise ValueError(f"recouvrement {cle} = {part:.0%} hors de [0 ; 100 %]")
                dec = -part * durees[pred]["duree_j"]
            if abs(dec) > durees[pred]["duree_j"] + 1e-9:
                raise ValueError(
                    f"lien {pred} -> {i} : recouvrement de {abs(dec):.2f} j pour un "
                    f"predecesseur de {durees[pred]['duree_j']:.2f} j — le successeur "
                    "demarrerait avant son predecesseur")
            resolus.append((pred, round(dec, 4)))
        out[i] = resolus
    return out


def reseau(d: dict, durees: dict) -> list:
    lr = liens_resolus(d, durees)
    return [Tache(i, NOMS[i], durees[i]["duree_j"], lr[i]) for i in NOMS]


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


def planning_avec_fenetres(d: dict, durees: dict, iterations: int = 30) -> dict:
    """Point fixe : la fenetre depend de la date, la date depend de la fenetre.

    Une fenetre de consignation agit sur la tache de DEUX facons, et il a fallu une
    passe adversariale pour voir que la seconde manquait :

    1. elle l'ETALE — le travail se fait par tranches, une par fenetre ;
    2. elle la DECALE — elle ne peut pas commencer avant la premiere fenetre
       disponible, meme si le reseau, lui, serait pret plus tot.

    La premiere version n'appliquait que l'etalement : elle calculait la date de la
    fenetre, la publiait dans `detail_fenetres`, et laissait la tache demarrer a la
    date du reseau. Le chantier perdait ainsi 17,5 jours ouvres et la date
    contractuelle 27 jours calendaires (bloquant B1). La contrainte passe maintenant
    par `Tache.au_plus_tot`, que les deux voies du CPM honorent.

    Le point fixe converge parce que les deux effets ne font que RETARDER : la suite
    des dates au plus tot est croissante et majoree par la plus tardive des fenetres
    atteignables.
    """
    ce = d["planning"]["contraintes_exploitation"]
    fen, per = ce["fenetre_jours"]["valeur"], ce["periode_entre_fenetres_jours"]["valeur"]
    prem = ce["premiere_fenetre_jour"]["valeur"]
    soumises = ce["taches_soumises"]
    lr = liens_resolus(d, durees)
    etale = {i: durees[i]["duree_j"] for i in durees}
    debut_impose = {i: 0.0 for i in durees}
    # date a laquelle le reseau NU serait pret : c'est contre elle que se mesure
    # l'attente. Mesuree contre le reseau deja contraint, elle vaut zero par
    # construction et l'information se perd.
    nu = voie_A_parcours([Tache(i, NOMS[i], durees[i]["duree_j"], lr[i]) for i in NOMS])
    detail = {}
    for n_iter in range(iterations):
        r = voie_A_parcours([Tache(i, NOMS[i], etale[i], lr[i], debut_impose[i]) for i in NOMS])
        change = False
        for i in soumises:
            d0 = r["tot"][i][0]
            e = etalement_sous_fenetres(durees[i]["duree_j"], d0, fen, per, prem)
            e["debut_du_reseau_nu"] = round(nu["tot"][i][0], 2)
            e["attente_avant_premiere_fenetre_j"] = round(e["debut"] - nu["tot"][i][0], 2)
            if abs(e["etalement_j"] - etale[i]) > 1e-6:
                etale[i], change = e["etalement_j"], True
            if abs(e["debut"] - debut_impose[i]) > 1e-6:
                debut_impose[i], change = e["debut"], True
            detail[i] = e
        if not change:
            break
    else:
        raise ValueError(f"point fixe des fenetres non converge en {iterations} iterations")
    taches = [Tache(i, NOMS[i], etale[i], lr[i], debut_impose[i]) for i in NOMS]
    cc = contre_calcul(taches)
    res = cc["detail"]
    # Sous contrainte externe, le plus long CHEMIN et l'ensemble des taches a marge
    # nulle ne coincident plus : en amont d'une tache epinglee par une fenetre, tout
    # le monde gagne de la marge. Le controle d'inclusion ne vaut donc que sur la
    # partie du chemin situee APRES la derniere tache contrainte active.
    chemin = cc["chemin_critique"]
    actives = [i for i in soumises if abs(res["tot"][i][0] - debut_impose[i]) < 1e-6
               and debut_impose[i] > 0]
    idx = max([chemin.index(i) for i in actives if i in chemin], default=-1)
    aval = chemin[idx:] if idx >= 0 else chemin
    cc["taches_contraintes_actives"] = actives
    cc["chemin_en_aval_de_la_contrainte"] = aval
    cc["aval_entierement_critique"] = set(aval) <= set(cc["taches_critiques_voie_A"])
    cc["pourquoi_l_inclusion_complete_ne_tient_plus"] = (
        "Une tache epinglee sur une fenetre de consignation coupe le chemin critique en "
        "deux : en amont, la duree ne commande plus la date de la tache epinglee, donc "
        "toutes les taches amont recoivent de la marge ; en aval, la chaine redevient "
        "critique. Un planning sous fenetres n'a pas un chemin critique continu, et "
        "c'est exactement ce qui le distingue d'un planning ordinaire.")
    # Garde-fou du bloquant B1 : la date au plus tot publiee DOIT etre celle de la
    # fenetre. Le test de recette d'avant comparait la fenetre a elle-meme, ce qui
    # etait vrai par construction et n'a rien vu.
    for i in soumises:
        if abs(res["tot"][i][0] - detail[i]["debut"]) > 1e-6:
            raise ValueError(
                f"{i} : le reseau la fait demarrer a {res['tot'][i][0]:.2f} alors que sa "
                f"fenetre est a {detail[i]['debut']:.2f} — la contrainte n'est pas appliquee")
    return {"durees_etalees": {i: round(etale[i], 2) for i in soumises},
            "debuts_imposes": {i: round(debut_impose[i], 2) for i in soumises},
            "detail_fenetres": detail, "contre_calcul": cc, "taches": taches,
            "iterations": n_iter + 1}


def segments_de_travail(durees: dict, res: dict, detail: dict, ce: dict) -> dict:
    """Quand on travaille VRAIMENT sur chaque tache, et pas seulement quand elle court.

    Une tache ordinaire travaille sur tout son intervalle. Une tache consignee ne
    travaille que pendant ses fenetres : entre deux consignations, personne n'est la.
    Cette distinction decide de deux grandeurs que le module publie :

      — l'histogramme d'effectifs, qui dimensionne la base-vie : compter dix
        compagnons pendant 80 jours d'attente dimensionne une base-vie fantome ;
      — la courbe en S, qui mesure le travail consomme : la version precedente
        comptait l'etalement x l'effectif, soit 801 jours-hommes pour 121 de travail,
        et gonflait le total de 13,8 % (bloquant B5). Elle contredisait la phrase que
        le module repete : le cout suit la duree de travail, le delai suit l'etalement.

    Elle produit aussi les vrais PALIERS de la courbe en S : entre deux fenetres, elle
    est plate, et c'est cela que la legende doit decrire (bloquant B4).
    """
    fen, per = ce["fenetre_jours"]["valeur"], ce["periode_entre_fenetres_jours"]["valeur"]
    out = {}
    for i in NOMS:
        deb, fin = res["tot"][i]
        if i in detail:
            e = detail[i]
            segs, reste = [], e["duree_de_travail_j"]
            for k in range(e["nb_fenetres"]):
                t = min(fen, reste)
                s0 = e["debut"] + k * per
                segs.append((round(s0, 4), round(s0 + t, 4)))
                reste -= t
            out[i] = segs
        else:
            out[i] = [(round(deb, 4), round(fin, 4))]
        total = sum(b - a for a, b in out[i])
        if abs(total - durees[i]["duree_j"]) > 1e-6:
            raise ValueError(f"{i} : {total:.4f} j de travail segmente pour une duree de "
                             f"{durees[i]['duree_j']:.4f} j")
    return out


# ------------------------------------------------------------- marges
def marges(res: dict, durees: dict, liens: dict) -> dict:
    """Marge totale (donnee par le parcours) et marge LIBRE (recalculee ici).

    La distinction n'est pas academique : consommer une marge totale decale les
    successeurs, consommer une marge libre ne decale personne. C'est elle qu'un
    conducteur de travaux peut depenser sans rien demander a quiconque.
    """
    tot = res["tot"]
    succ = {i: [] for i in NOMS}
    for i, preds in liens.items():
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


def histogramme_effectifs(res: dict, eff: dict, segments: dict,
                          decalages: dict | None = None) -> list:
    """Effectif present chaque jour, sur les SEGMENTS DE TRAVAIL.

    Une tache consignee n'occupe personne entre deux fenetres : la compter sur tout son
    etalement dimensionnerait une base-vie pour des gens qui ne sont pas la.
    """
    dec = decalages or {}
    fin = int(math.ceil(res["duree"])) + 1
    jours = []
    for k in range(fin):
        n = 0
        for i in NOMS:
            dk = dec.get(i, 0.0)
            if any(a + dk <= k < b + dk for a, b in segments[i]):
                n += eff[i]
        jours.append(n)
    return jours


def conflits_de_grue(d: dict, segments: dict, eff: dict,
                     decalages: dict | None = None) -> dict:
    """La grue a tour est-elle demandee en deux endroits le meme jour ?

    Une occupation MOYENNE ne repond pas a la question : c'est l'erreur que la tranche
    verticale avait faite et que la passe adversariale de D2 a retrouvee intacte (la
    check-list du module exigeait ce controle, et le module ne le faisait pas). On
    compte donc, jour par jour, combien de taches servies par la grue sont actives, et
    on compare au parc.
    """
    taches = d["planning"]["taches_servies_par_la_grue"]["valeur"]
    parc = d["materiel"]["nb_grues"]
    dec = decalages or {}
    fin = max(int(math.ceil(b + dec.get(i, 0.0))) for i in NOMS for _, b in segments[i]) + 1
    profil, pire, j_pire = [], 0, 0
    for k in range(fin):
        actives = [i for i in taches
                   if any(a + dec.get(i, 0.0) <= k < b + dec.get(i, 0.0)
                          for a, b in segments[i])]
        profil.append({"j": k, "demande": len(actives), "taches": actives})
        if len(actives) > pire:
            pire, j_pire = len(actives), k
    jours_en_conflit = [x["j"] for x in profil if x["demande"] > parc]
    return {
        "parc_de_grues": parc, "taches_servies": taches,
        "demande_maximale": pire, "jour_de_la_demande_maximale": j_pire,
        "taches_au_pire_jour": profil[j_pire]["taches"],
        "nb_jours_en_conflit": len(jours_en_conflit),
        "premier_jour_en_conflit": jours_en_conflit[0] if jours_en_conflit else None,
        "dernier_jour_en_conflit": jours_en_conflit[-1] if jours_en_conflit else None,
        "conflit": bool(jours_en_conflit),
        "profil": [{"j": x["j"], "demande": x["demande"]} for x in profil],
        "occupation_moyenne_pct": round(
            sum(x["demande"] for x in profil) / max(1, len(profil)) / max(1, parc) * 100, 1),
        "pourquoi_la_moyenne_ne_suffit_pas": (
            "L'occupation moyenne lisse les pointes : une grue demandee trois fois le "
            "meme jour et nulle part le lendemain affiche une moyenne rassurante. Seul "
            "le profil journalier dit si le planning est faisable."),
    }


def lisser(res: dict, eff: dict, mg: dict, segments: dict, passes: int = 4) -> dict:
    """Lissage : on DECALE les taches non critiques dans leur marge pour abaisser la
    pointe. Aucune duree ne change, aucune date de fin ne bouge.

    Le decalage est borne par la marge LIBRE, pas par la marge totale. Dans la marge
    totale, une tache peut se decaler sans repousser la fin du projet, mais en
    repoussant le DEBUT de son successeur : l'histogramme lisse etait alors
    irrealisable, et la simplification n'etait pas declaree. Dans la marge libre, aucun
    successeur ne bouge, donc le planning lisse reste celui qu'on a calcule.

    C'est une heuristique gloutonne, pas un optimum : le lissage de ressources est un
    probleme combinatoire. Elle est declaree comme telle (§ R6), et le module dit ce
    qu'elle ne garantit pas.
    """
    base = histogramme_effectifs(res, eff, segments)
    dec = {i: 0.0 for i in NOMS}
    meilleure = max(base)
    for _ in range(passes):
        bouge = False
        for i in sorted(NOMS, key=lambda x: -eff[x]):
            m = mg[i]["marge_libre_j"]
            if m < 1e-9 or eff[i] == 0:
                continue
            for pas in range(1, int(m) + 1):
                essai = dict(dec); essai[i] = float(pas)
                p = max(histogramme_effectifs(res, eff, segments, essai))
                if p < meilleure - 1e-9:
                    meilleure, dec, bouge = p, essai, True
        if not bouge:
            break
    lisse = histogramme_effectifs(res, eff, segments, dec)
    utiles = [x for x in base if x > 0]
    utiles_l = [x for x in lisse if x > 0]
    jh_avant, jh_apres = sum(base), sum(lisse)
    if abs(jh_avant - jh_apres) > 1e-9:
        raise ValueError(f"le lissage a cree ou detruit du travail : {jh_avant} -> {jh_apres} "
                         "jours-hommes. Un decalage deplace, il n'ajoute rien.")
    return {
        "pointe_avant": max(base), "pointe_apres": max(lisse),
        "moyenne_avant": round(sum(base) / max(1, len(utiles)), 1),
        "moyenne_apres": round(sum(lisse) / max(1, len(utiles_l)), 1),
        "gain_de_pointe_pct": round((max(base) - max(lisse)) / max(base) * 100, 1),
        "decalages_utilises_j": {i: v for i, v in dec.items() if v},
        "marge_totale_consommee_j": round(sum(dec.values()), 1),
        "histogramme_brut": base, "histogramme_lisse": lisse,
        "borne": "marge libre",
        "jours_hommes_avant": jh_avant, "jours_hommes_apres": jh_apres,
        "jours_travailles_avant": len(utiles), "jours_travailles_apres": len(utiles_l),
        "limite": ("Heuristique gloutonne : elle abaisse la pointe, elle ne prouve pas "
                   "qu'aucune autre combinaison ne ferait mieux. Et ce qu'elle depense "
                   "en marge libre n'est plus disponible pour l'alea."),
        "ce_que_le_lissage_conserve": (
            f"Les jours-hommes sont identiques avant et apres ({jh_avant} de part et "
            "d'autre, et le calcul leve si ce n'est pas le cas) : lisser DEPLACE du "
            "travail, il n'en supprime aucun. La MOYENNE, elle, bouge — de "
            f"{round(sum(base) / max(1, len(utiles)), 1)} a "
            f"{round(sum(lisse) / max(1, len(utiles_l)), 1)} compagnons — non pas "
            "parce que le travail a change, mais parce qu'il s'etale desormais sur "
            f"{len(utiles_l)} jours travailles au lieu de {len(utiles)}. C'est une "
            "moyenne a denominateur variable : la grandeur conservee est l'aire, pas "
            "la moyenne."),
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
def courbe_en_s(res: dict, eff: dict, segments: dict, pas: int = 1) -> list:
    """Avancement en % des jours-hommes de TRAVAIL, date par date.

    L'assiette n'est ni le nombre de taches finies, ni le temps ecoule, ni l'etalement :
    c'est le travail consomme. Une courbe batie sur le temps serait une droite ; une
    courbe batie sur l'etalement compte des jours-hommes que personne ne fait, et c'est
    ce qu'elle faisait avant la passe adversariale (bloquant B5). Accumuler sur les
    segments de travail produit en prime les vrais paliers : entre deux fenetres de
    consignation, et pendant le sechage, la courbe est PLATE.
    """
    fin = int(math.ceil(res["duree"]))
    total = sum(eff[i] * sum(b - a for a, b in segments[i]) for i in NOMS)
    pts = []
    for k in range(0, fin + 1, pas):
        acc = 0.0
        for i in NOMS:
            for a, b in segments[i]:
                if k >= b:
                    acc += eff[i] * (b - a)
                elif k > a:
                    acc += eff[i] * (k - a)
        pts.append({"j": k, "prevu": round(acc / total * 100, 1) if total else 0.0})
    return pts


def paliers_de_la_courbe(pts: list, seuil_pts: float = 0.05) -> list:
    """Les plages ou la courbe en S ne monte pas, et ce qui les explique.

    Publier les paliers evite d'en commenter un qui n'existe pas : la legende de la
    figure designait l'attente de consignation la ou le plat etait celui du sechage.
    """
    out, debut = [], None
    for k in range(1, len(pts)):
        plat = pts[k]["prevu"] - pts[k - 1]["prevu"] <= seuil_pts
        if plat and debut is None:
            debut = pts[k - 1]["j"]
        elif not plat and debut is not None:
            out.append({"de_j": debut, "a_j": pts[k - 1]["j"]})
            debut = None
    if debut is not None and debut < pts[-1]["j"]:
        out.append({"de_j": debut, "a_j": pts[-1]["j"]})
    return [x for x in out if x["a_j"] - x["de_j"] >= 5]


def _resume_des_paliers(paliers: list) -> dict:
    """Les paliers groupes par cause, pour que la legende n'ait pas a les compter.

    Une version precedente ecrivait « puis quatre paliers entre deux fenetres » en toutes
    lettres. Le chantier en a maintenant seize : le texte etait faux, et il ne pouvait pas
    se corriger seul puisqu'il etait tape a la main (§ 4.3). Grouper dit d'ailleurs mieux
    ce qu'il y a a voir — ce n'est pas un palier, c'est une serie.
    """
    groupes = []
    for p in paliers:
        if groupes and groupes[-1]["cause"] == p["cause"]:
            groupes[-1]["nombre"] += 1
            groupes[-1]["a_j"] = p["a_j"]
        else:
            groupes.append({"cause": p["cause"], "nombre": 1,
                            "de_j": p["de_j"], "a_j": p["a_j"]})
    for g in groupes:
        g["jours"] = round(g["a_j"] - g["de_j"], 1)
    return {
        "nb_paliers": len(paliers),
        "groupes": groupes,
        "phrase": " ; puis ".join(
            (f"{g['nombre']} paliers — {g['cause']}" if g["nombre"] > 1 else g["cause"])
            for g in groupes),
    }


def _cause_du_palier(pal: dict, res: dict, durees: dict, detail: dict) -> str:
    """Quelle tache explique un palier : on la CHERCHE, on ne la devine pas.

    La legende de la figure designait l'attente de consignation la ou le plat etait
    celui du sechage (bloquant B4). Un palier dont la cause est calculee ne peut plus
    etre commente de travers.
    """
    milieu = (pal["de_j"] + pal["a_j"]) / 2
    # une tache imposee a effectif nul qui court pendant le palier l'explique
    for i in NOMS:
        deb, fin = res["tot"][i]
        if deb <= milieu <= fin and durees[i]["famille"] == "imposee":
            return f"{i} · {NOMS[i]} — durée imposée, aucun effectif sur le chantier"
    for i, e in detail.items():
        if e["debut"] <= milieu <= e["fin"]:
            return f"{i} · {NOMS[i]} — entre deux fenêtres de consignation"
    return "aucune cause identifiee automatiquement"


# ------------------------------------------- contre-calcul n° 2, hors CPM
def contre_calcul_chemin(res: dict, chemin: list, durees_etalees: dict,
                         liens: dict, debuts_imposes: dict | None = None) -> dict:
    """Seconde voie, qui n'est PAS un second algorithme de CPM.

    On additionne a la main les durees et les decalages du chemin annonce critique.
    Si la somme ne rend pas la duree du projet, c'est que le chemin publie n'est pas
    celui qui porte la duree — une erreur qu'aucune des deux voies de `cpm.py` ne voit,
    puisqu'elles partagent le meme reseau.
    """
    imp = debuts_imposes or {}
    total, detail = 0.0, []
    for k, i in enumerate(chemin):
        dec = dict(liens[i]).get(chemin[k - 1], 0.0) if k else 0.0
        d = durees_etalees.get(i, 0.0)
        # une contrainte externe (fenetre de consignation) peut repousser le debut
        # au-dela de ce que le chemin accumule : l'addition doit en tenir compte,
        # sinon la somme du chemin ne retrouve plus la duree du reseau
        debut = max(total + dec, imp.get(i, 0.0))
        attente = round(debut - (total + dec), 4)
        total = debut + d
        detail.append({"tache": i, "duree_j": round(d, 2), "decalage_j": round(dec, 2),
                       "attente_de_fenetre_j": attente, "cumul_j": round(total, 2)})
    ecart = abs(total - res["duree"])
    return {"somme_du_chemin_j": round(total, 2), "duree_du_reseau_j": round(res["duree"], 2),
            "ecart_j": round(ecart, 6), "detail": detail,
            "verdict": "OK" if ecart <= 1e-6 else
                       "LE CHEMIN PUBLIE NE PORTE PAS LA DUREE DU PROJET"}


def decomposition_du_chemin(cc2: dict, durees: dict, detail: dict) -> dict:
    """De quoi la duree du projet est-elle FAITE, le long de son chemin critique ?

    Repartir les durees par famille sur « l'ensemble des taches a marge nulle » ne
    repond plus a la question des qu'une fenetre de consignation epingle une tache :
    cet ensemble se reduit a l'aval, et sa somme ne fait plus la duree du projet. La
    passe adversariale avait raison de refuser ce tableau — mais la bonne reponse
    n'etait pas de le corriger, elle etait de decomposer le CHEMIN, qui lui, par
    construction, somme exactement a la duree.

    Cinq postes, dont deux que les trois familles de durees ne savaient pas nommer :
    l'ATTENTE d'une fenetre, et l'IMMOBILISATION entre deux fenetres.
    """
    postes = {"calculee": 0.0, "imposee": 0.0, "declaree": 0.0,
              "attente_de_fenetre": 0.0, "immobilisation_entre_fenetres": 0.0,
              "recouvrements": 0.0}
    lignes = []
    for pas in cc2["detail"]:
        i = pas["tache"]
        fam = durees[i]["famille"]
        travail = durees[i]["duree_j"]
        immo = detail[i]["immobilisation_improductive_j"] if i in detail else 0.0
        postes[fam] += travail
        postes["immobilisation_entre_fenetres"] += immo
        postes["attente_de_fenetre"] += pas["attente_de_fenetre_j"]
        postes["recouvrements"] += pas["decalage_j"]
        lignes.append({"tache": i, "famille": fam, "travail_j": round(travail, 2),
                       "immobilisation_j": round(immo, 2),
                       "attente_j": pas["attente_de_fenetre_j"],
                       "recouvrement_j": pas["decalage_j"]})
    total = sum(postes.values())
    ecart = abs(total - cc2["duree_du_reseau_j"])
    if ecart > 0.02:
        raise ValueError(f"la decomposition du chemin fait {total:.2f} j pour une duree de "
                         f"{cc2['duree_du_reseau_j']:.2f} j — ecart {ecart:.2f} j")
    duree = cc2["duree_du_reseau_j"]
    return {
        "lignes": lignes,
        "postes_j": {k: round(v, 2) for k, v in postes.items()},
        "postes_pct": {k: round(v / duree * 100, 1) for k, v in postes.items()},
        "total_j": round(total, 2), "duree_du_reseau_j": duree, "ecart_j": round(ecart, 4),
        "part_que_les_effectifs_ne_touchent_pas_pct": round(
            (postes["imposee"] + postes["attente_de_fenetre"]
             + postes["immobilisation_entre_fenetres"]) / duree * 100, 1),
        "lecture": (
            "Seul le poste « calculee » repond aux effectifs. Les durees imposees, "
            "l'attente de la premiere fenetre et l'immobilisation entre deux fenetres "
            "sont hors d'atteinte des moyens : doubler les equipes ne les touche pas "
            "d'un jour. C'est le chiffre a avoir en tete avant de promettre une date."),
    }


def resoudre_le_conflit_de_grue(d: dict, segments: dict, eff: dict, mg: dict,
                                depart: dict | None = None) -> dict:
    """Peut-on tenir le planning avec le parc de grues declare ?

    On cherche un decalage des taches servies par la grue, DANS LEUR MARGE LIBRE, qui
    ramene la demande journaliere au parc. Si aucun n'y suffit, on le dit : le planning
    publie demande une grue de plus, et c'est une decision de moyens, pas un detail.
    """
    taches = d["planning"]["taches_servies_par_la_grue"]["valeur"]
    parc = d["materiel"]["nb_grues"]
    dec = dict(depart or {})
    best = conflits_de_grue(d, segments, eff, dec)
    essais = 0
    for _ in range(6):
        if not best["conflit"]:
            break
        bouge = False
        for i in sorted(taches, key=lambda x: -mg[x]["marge_libre_j"]):
            m = mg[i]["marge_libre_j"]
            if m < 1e-9:
                continue
            for pas in range(1, int(m) + 1):
                essai = dict(dec); essai[i] = float(pas)
                c = conflits_de_grue(d, segments, eff, essai)
                essais += 1
                if (c["nb_jours_en_conflit"], c["demande_maximale"]) < \
                   (best["nb_jours_en_conflit"], best["demande_maximale"]):
                    best, dec, bouge = c, essai, True
        if not bouge:
            break
    return {
        "decalages_essayes": essais,
        "decalages_retenus_j": {i: v for i, v in dec.items() if v},
        "marge_libre_consommee_j": round(sum(dec.values()), 1),
        "resultat": {k: v for k, v in best.items() if k != "profil"},
        "resolu_dans_les_marges": not best["conflit"],
        "parc_necessaire_si_non_resolu": best["demande_maximale"] if best["conflit"] else parc,
        "verdict": (
            "Le conflit se resorbe dans les marges libres : le planning tient avec "
            f"{parc} grue(s)."
            if not best["conflit"] else
            f"Le conflit NE se resorbe pas dans les marges libres : il reste "
            f"{best['nb_jours_en_conflit']} jour(s) ou {best['demande_maximale']} taches "
            f"demandent {parc} grue(s). Trois issues, et une seule est honnete : louer "
            "une seconde grue sur cette periode, completer par une grue mobile, ou "
            "deplacer une tache HORS de sa marge libre en acceptant de repousser son "
            "successeur. Publier le planning tel quel sans le dire n'en est pas une."),
    }


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
    d2 = {**d, "planning": pl2}
    f = planning_avec_fenetres(d2, t)
    res = voie_A_parcours(f["taches"])
    return {"duree_projet_j": round(res["duree"], 2),
            "attente_de_fenetre_j": round(
                f["detail_fenetres"]["CHLV"]["attente_avant_premiere_fenetre_j"], 2),
            "chemin_critique": f["contre_calcul"]["chemin_critique"],
            "etalement_levage_j": round(f["detail_fenetres"]["CHLV"]["etalement_j"], 2),
            "travail_levage_j": round(f["detail_fenetres"]["CHLV"]["duree_de_travail_j"], 2),
            "nb_fenetres_levage": f["detail_fenetres"]["CHLV"]["nb_fenetres"],
            "duree_poteaux_j": round(t["POTR"]["duree_j"], 2),
            "duree_mezzanine_j": round(t["MEZZ"]["duree_j"], 2)}


def variante_aux_bornes(d: dict, pl: dict, duree_mezz: float, sens: str) -> dict:
    """Rejoue le planning avec TOUTES les hypotheses au meme bout de leur fourchette.

    Un planning publie une date. Celle-ci sort d'une trentaine d'hypotheses V3 qui
    portent toutes une fourchette declaree, et qu'aucune variante n'exploitait : le
    module exhibait ses incertitudes puis publiait un nombre unique, ce qu'il reproche
    lui-meme aux plannings qu'il critique.

    « pessimiste » : cadences au bas de leur fourchette (on va moins vite), forfaits et
    delais imposes au haut (tout dure plus longtemps), recouvrements au bas (on se
    superpose moins). « optimiste » : l'inverse. Ces deux bornes ne sont PAS des
    probabilites : elles ne disent pas qu'une date est plus vraisemblable qu'une autre,
    elles disent de combien la date bouge quand les hypotheses bougent ensemble — ce qui
    est deja la seule chose defendable en reunion.
    """
    import copy
    assert sens in ("optimiste", "pessimiste")
    bas = sens == "pessimiste"
    d2 = copy.deepcopy(d)
    pl2 = d2["planning"]

    def borne(o, prendre_le_bas):
        if isinstance(o, dict) and "valeur" in o and "fourchette" in o:
            o["valeur"] = o["fourchette"][0 if prendre_le_bas else 1]

    for v in pl2["cadences_chantier_V3"].values():
        borne(v, bas)                      # cadence basse = chantier lent
    for bloc in ("forfaits_V3", "delais_imposes_V3"):
        for v in pl2[bloc].values():
            borne(v, not bas)              # forfaits hauts = chantier lent
    for v in pl2["recouvrements_pct"].values():
        borne(v, bas)                      # peu de recouvrement = chantier lent
    ce = pl2["contraintes_exploitation"]
    borne(ce["fenetre_jours"], bas)                    # fenetre courte = chantier lent
    borne(ce["periode_entre_fenetres_jours"], not bas)
    borne(ce["premiere_fenetre_jour"], not bas)
    borne(ce["part_levage_sous_consignation_pct"], not bas)
    borne(pl2["calendrier"]["jours_non_ouvres_par_mois_intemperies"], not bas)

    q = quantites_chantier(d2, pl2)
    t = durees_chantier(d2, pl2, q, duree_mezz)
    f = planning_avec_fenetres(d2, t)
    res = voie_A_parcours(f["taches"])
    cal = calendrier(res["duree"], pl2["calendrier"])
    return {"sens": sens, "duree_j": round(res["duree"], 1),
            "duree_avec_intemperies_j": cal["duree_ouvree_avec_intemperies_j"],
            "fin": cal["fin_avec_alea"],
            "chemin_critique": f["contre_calcul"]["chemin_critique"]}


def fourchette_de_date(d: dict, pl: dict, duree_mezz: float, reference: dict,
                       cal_ref: dict) -> dict:
    opt = variante_aux_bornes(d, pl, duree_mezz, "optimiste")
    pes = variante_aux_bornes(d, pl, duree_mezz, "pessimiste")
    ref = reference["duree"]
    return {
        "optimiste": opt, "retenue": {"duree_j": round(ref, 1),
                                      "duree_avec_intemperies_j": cal_ref["duree_ouvree_avec_intemperies_j"],
                                      "fin": cal_ref["fin_avec_alea"]},
        "pessimiste": pes,
        "facteur_pessimiste": round(pes["duree_j"] / ref, 2),
        "facteur_optimiste": round(opt["duree_j"] / ref, 2),
        "etendue_j": round(pes["duree_j"] - opt["duree_j"], 1),
        "etendue_pct_de_la_retenue": round((pes["duree_j"] - opt["duree_j"]) / ref * 100, 0),
        "lecture": (
            "Les deux bornes ne sont pas des probabilites : rien ne dit que toutes les "
            "hypotheses se trompent dans le meme sens. Elles mesurent la SENSIBILITE de "
            "la date aux hypotheses, et cette sensibilite est le seul argument qui tienne "
            "quand on demande de s'engager : une date unique tiree de trente hypotheses "
            "non bornees n'est pas defendable, meme si son arithmetique est juste."),
        "lien_avec_la_dette_n10": (
            "La dette n° 10 du projet soupconne les cadences V3 d'etre optimistes d'un "
            "facteur 2 a 3, sur la foi d'une part de main d'oeuvre trop faible. La borne "
            "pessimiste ci-dessus ne va pas jusque-la : elle ne descend les cadences qu'au "
            "bas de leur fourchette declaree, soit environ un tiers. Si le soupcon se "
            "confirmait, la date pessimiste serait encore au-dela. Le module D1, qui "
            "ouvre les prix poste par poste, est l'endroit ou ce soupcon se verifie."),
    }


# ------------------------------------------------------------- sortie
def tout_calculer(d: dict, pl: dict, duree_mezzanine_j: float, cadence_mezz: float,
                  cycle_mezz: float) -> dict:
    q = quantites_chantier(d, pl)
    t = durees_chantier(d, pl, q, duree_mezzanine_j)

    lr = liens_resolus(d, t)
    sans = contre_calcul(reseau(d, t))
    f = planning_avec_fenetres(d, t)
    res = voie_A_parcours(f["taches"])
    etalees = {x.id: x.duree for x in f["taches"]}
    seg = segments_de_travail(t, res, f["detail_fenetres"], pl["contraintes_exploitation"])
    mg = marges(res, t, lr)
    eff = effectifs_par_tache(d, pl, t)
    lis = lisser(res, eff, mg, seg)
    grue = conflits_de_grue(d, seg, eff)
    grue_lissee = conflits_de_grue(d, seg, eff, lis["decalages_utilises_j"])
    grue_res = resoudre_le_conflit_de_grue(d, seg, eff, mg, lis["decalages_utilises_j"])
    cs = courbe_en_s(res, eff, seg, 5)
    cal = calendrier(res["duree"], pl["calendrier"])
    cc2 = contre_calcul_chemin(res, f["contre_calcul"]["chemin_critique"], etalees, lr,
                               f["debuts_imposes"])
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
             for i in sous_reseau for p, _ in lr[i] if p in sous_reseau]

    _pal_s = [{**pal, "cause": _cause_du_palier(pal, res, t, f["detail_fenetres"])}
              for pal in paliers_de_la_courbe(cs)]
    return {
        "quantites": q,
        "durees": {i: {**t[i], "duree_etalee_j": round(etalees[i], 2), **mg[i],
                       "debut_j": round(res["tot"][i][0], 2),
                       "fin_j": round(res["tot"][i][1], 2),
                       "nom": NOMS[i], "lot": LOT[i]} for i in NOMS},
        "familles": {"nb_taches": {k: len(v) for k, v in par_famille.items()},
                     "somme_des_durees_j": somme,
                     "sur_le_chemin_critique_j": crit_par_famille,
                     "_note_chemin": (
                         "Attention : « sur_le_chemin_critique_j » somme les taches a "
                         "marge nulle, dont le total ne fait PAS la duree du projet des "
                         "qu'une fenetre epingle une tache. Pour decomposer la duree, "
                         "utiliser « decomposition_du_chemin », qui somme exactement.")},
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
        "consignations": {**f["detail_fenetres"],
                          "_debuts_imposes": f["debuts_imposes"],
                          "_iterations_du_point_fixe": f["iterations"]},
        "segments_de_travail": {i: seg[i] for i in NOMS},
        "ressources": lis,
        "grue": grue,
        "grue_apres_lissage": grue_lissee,
        "grue_resolution": grue_res,
        "decomposition_du_chemin": decomposition_du_chemin(cc2, t, f["detail_fenetres"]),
        "calendrier": cal,
        "fourchette_de_date": fourchette_de_date(d, pl, duree_mezzanine_j, res, cal),
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
            "courbe_s": cs,
            "grue": [{"j": x["j"], "n": x["demande"]} for x in grue["profil"]],
            "paliers": [{"de_j": pal["de_j"], "a_j": pal["a_j"],
                         "etiquette": _cause_du_palier(pal, res, t, f["detail_fenetres"]).split(" · ")[0]}
                        for pal in paliers_de_la_courbe(cs)],
        },
        "paliers_de_la_courbe_s": _pal_s,
        "resume_des_paliers": _resume_des_paliers(_pal_s),
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
