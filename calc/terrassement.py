"""Terrassements, fouilles et évacuation des terres (module C2).

Cinq résultats, aucun réglementaire :

1. **La place décide du mode de soutènement, et la place se mesure.** Un talus de fruit
   m sur une fouille de hauteur h demande m·h de recul, plus une banquette en crête.
   Côté par côté, on compare ce recul à ce qui est disponible : là où il tient, on
   talute ; là où il ne tient pas, on blinde. Ce n'est pas un calcul de stabilité — la
   pente admissible est un résultat de B2 (⏸) — c'est un calcul de GÉOMÉTRIE, et il
   tranche avant toute étude.
2. **Le volume d'un talus a une forme fermée exacte**, et la « méthode des profils »
   que tout le monde emploie le SURESTIME d'exactement a·b·h³/6, où a et b sont les
   reculs de talus par mètre de profondeur dans chaque direction. On publie les trois
   voies : l'intégrale exacte, la formule prismatique (exacte aussi, et c'est le point),
   et la moyenne des aires (fausse, et de combien).
3. **Le bilan des terres** : décapage, fouille, talus, foisonnement, réemploi en
   remblai, et ce qui part au dépôt. Le volume de talus n'est dans AUCUNE ligne du
   bordereau de D1, qui a cubé la fouille comme un prisme vertical.
4. **La durée d'un terrassement s'achète au camion.** Le débit de la pelle n'est
   presque jamais la contrainte : c'est la rotation. Le nombre de camions nécessaire est
   proportionnel à la distance au dépôt, et la fourchette déclarée de cette distance
   fait varier la flotte d'un facteur cinq.
5. **La cadence déclarée par D2 suppose deux ateliers**, donc deux pelles, et une flotte
   de camions que personne n'a écrite. Le module C6, qui a chiffré le matériel, compte
   UNE pelle : l'écart est publié.

Ce que le module ne dit pas : la stabilité d'un talus, le dimensionnement d'un blindage,
le rabattement de nappe, les distances réglementaires en crête. Tout cela est
réglementaire ou relève d'un calcul géotechnique, et reste ⏸ (module B2).
"""
from __future__ import annotations
import json, math, pathlib

RACINE = pathlib.Path(__file__).resolve().parent.parent


def _f(x: float, dec: int = 0) -> str:
    s = f"{x:,.{dec}f}".replace(",", " ")
    return s.replace(".", ",") if dec else s


def _b(o: dict) -> tuple[float, float]:
    f = o.get("fourchette")
    return (float(f[0]), float(f[1])) if f else (float(o["valeur"]), float(o["valeur"]))


def _v(o) -> float:
    return float(o["valeur"]) if isinstance(o, dict) else float(o)


# --------------------------------------------------------- 1. les trois voies du talus
def volume_talus_exact(L: float, W: float, m: float, h: float,
                       cotes_L: int, cotes_W: int) -> float:
    """Volume EXACT d'une fouille talutée, par intégration.

    À la hauteur y au-dessus du fond, la section horizontale mesure
    (L + cotes_L·m·y) par (W + cotes_W·m·y), où cotes_L et cotes_W comptent combien des
    côtés de chaque direction sont talutés (0, 1 ou 2). L'intégrale de 0 à h est donc
    exacte, et c'est elle qui sert de référence aux deux autres voies.
    """
    a, b = cotes_L * m, cotes_W * m
    return (L * W * h + (L * b + W * a) * h ** 2 / 2 + a * b * h ** 3 / 3)


def volume_talus_par_profils(L, W, m, h, cotes_L, cotes_W) -> float:
    """Méthode des profils : hauteur x moyenne des aires extrêmes. FAUSSE, et de
    combien — l'aire varie comme un polynôme de degré 2 en y, et la moyenne de deux
    valeurs ne reproduit pas l'intégrale d'une parabole."""
    A0 = L * W
    A1 = (L + cotes_L * m * h) * (W + cotes_W * m * h)
    return h * (A0 + A1) / 2


def volume_talus_prismatique(L, W, m, h, cotes_L, cotes_W) -> float:
    """Formule prismatique (Simpson) : h/6 (A0 + 4Am + A1). EXACTE pour une aire
    quadratique, donc exacte ici — et c'est tout l'intérêt de la connaître."""
    A0 = L * W
    Am = (L + cotes_L * m * h / 2) * (W + cotes_W * m * h / 2)
    A1 = (L + cotes_L * m * h) * (W + cotes_W * m * h)
    return h * (A0 + 4 * Am + A1) / 6


# --------------------------------------------------- 2. la géométrie, côté par côté
def geometrie(d: dict) -> dict:
    """Quel côté se talute et quel côté se blinde — par la GÉOMÉTRIE seule.

    Les dimensions de la fouille et sa profondeur sont LUES : emprise partielle du
    niveau technique et son altitude (geometrie.niveaux), plus la surprofondeur de forme
    que D1 emploie déjà pour cuber. Rien n'est redéclaré.
    """
    g, t = d["geometrie"], d["terrassement"]
    nt = next(n for n in g["niveaux"] if n["nom"] == "niveau technique")
    L, W = float(nt["emprise_partielle_m"][0]), float(nt["emprise_partielle_m"][1])
    surp = _v(d["planning"]["ratios_quantites_V3"]["surprofondeur_forme_m"])
    h = abs(float(nt["altitude_m"])) + surp
    emp_L, emp_W = float(g["emprise_m"][0]), float(g["emprise_m"][1])
    m = _v(t["fouille"]["fruit_de_talus"])
    banq = _v(t["fouille"]["banquette_en_crete_m"])
    retrait = float(t["fouille"]["retrait_facade_cote_voies_m"])
    besoin = m * h + banq
    # Repère de C1 : y = 0 au nu de la façade côté ville, y = emp_W côté voies.
    y_voies, y_ville = emp_W - retrait, emp_W - retrait - W
    x_debut = (emp_L - L) / 2
    cotes = [
        {"cote": "Côté voies (long, 40 m)", "longueur_m": L,
         "place_disponible_m": retrait,
         "_place": "retrait de la fouille au nu de la façade côté voies : au-delà, "
                   "l'emprise des travaux s'arrête, le quai est exploité"},
        {"cote": "Côté ville (long, 40 m)", "longueur_m": L,
         "place_disponible_m": y_ville,
         "_place": "de l'arête de fouille au nu de la façade côté ville"},
        {"cote": "Pignon ouest (20 m)", "longueur_m": W, "place_disponible_m": x_debut,
         "_place": "de l'arête de fouille au bord de l'emprise, dans la longueur"},
        {"cote": "Pignon est (20 m)", "longueur_m": W, "place_disponible_m": x_debut,
         "_place": "de l'arête de fouille au bord de l'emprise à l'autre extrémité : "
                   "la fouille est centrée dans la longueur du bâtiment, les deux "
                   "pignons ont donc la même réserve"},
    ]
    for c in cotes:
        c["recul_necessaire_m"] = round(besoin, 2)
        c["talutable"] = bool(c["place_disponible_m"] >= besoin)
        c["mode"] = "talus" if c["talutable"] else "blindage"
        c["marge_m"] = round(c["place_disponible_m"] - besoin, 2)
    blindes = [c for c in cotes if not c["talutable"]]
    surface_blindage = sum(c["longueur_m"] for c in blindes) * h
    return {
        "longueur_m": L, "largeur_m": W, "profondeur_m": round(h, 2),
        "altitude_du_niveau_m": float(nt["altitude_m"]),
        "surprofondeur_de_forme_m": surp,
        "fruit": m, "banquette_m": banq,
        "recul_necessaire_par_cote_m": round(besoin, 2),
        "position": {"x_de_m": round(x_debut, 2), "x_a_m": round(x_debut + L, 2),
                     "y_de_m": round(y_ville, 2), "y_a_m": round(y_voies, 2)},
        "cotes": cotes,
        "nb_cotes_talutes": sum(1 for c in cotes if c["talutable"]),
        "nb_cotes_blindes": len(blindes),
        "cotes_blindes": [c["cote"] for c in blindes],
        "surface_de_blindage_m2": round(surface_blindage, 1),
        # combien de côtés talutés dans chaque direction, pour l'intégrale
        "cotes_talutes_en_longueur": sum(1 for c in cotes[2:] if c["talutable"]),
        "cotes_talutes_en_largeur": sum(1 for c in cotes[:2] if c["talutable"]),
        "emprise_au_sol_fouille_m2": round(L * W, 1),
        "lecture": (
            f"La fouille fait {_f(L, 0)} x {_f(W, 0)} m sur {_f(h, 2)} m de profondeur. "
            f"Un talus au fruit {_f(m, 1)} demande {_f(besoin, 2)} m de recul "
            f"({_f(m * h, 2)} m de talus et {_f(banq, 1)} m de banquette en crête). "
            f"Trois côtés l'ont, un ne l'a pas : "
            + ", ".join(c["cote"].split(" (")[0] for c in blindes)
            + f", où il ne reste que {_f(blindes[0]['place_disponible_m'], 1)} m."
            if blindes else "et les quatre côtés l'ont."),
    }


# ----------------------------------------------------------------- 3. les cubatures
def cubatures(d: dict, prix: dict, geo: dict) -> dict:
    """Le bilan des terres, et la ligne que le bordereau n'a pas.

    Le décapage et la fouille VERTICALE sont lus dans le bordereau de D1 : ce sont ses
    quantités, calculées depuis la géométrie, et les redéclarer en ferait deux nombres
    pour une seule réalité. Le volume de TALUS, lui, n'est nulle part : D1 a cubé la
    fouille comme un prisme vertical.
    """
    q = {p["poste"]: p["quantite"] for p in prix["bordereau"]["postes"]}
    decapage, vertical = float(q["TERR"]), float(q["FOUI"])
    L, W, h, m = geo["longueur_m"], geo["largeur_m"], geo["profondeur_m"], geo["fruit"]
    cL, cW = geo["cotes_talutes_en_longueur"], geo["cotes_talutes_en_largeur"]
    exact = volume_talus_exact(L, W, m, h, cL, cW)
    profils = volume_talus_par_profils(L, W, m, h, cL, cW)
    prisme = volume_talus_prismatique(L, W, m, h, cL, cW)
    talus = exact - L * W * h
    foisonnement = _v(d["planning"]["ratios_quantites_V3"]["foisonnement_pct"]) / 100
    reemploi = _v(d["terrassement"]["reemploi_en_remblai_pct"]) / 100
    en_place = decapage + exact
    reutilise = en_place * reemploi
    au_depot = en_place - reutilise
    transporte = au_depot * (1 + foisonnement)
    pu = _v(d["prix_unitaires_MAD"]["ressources"]["materiaux_MAD"]["evacuation_deblais_m3"])
    # coefficient du sous-detail de D1 : combien de m3 foisonnes il facture par m3 cube
    coef_evac = next(m_["quantite"] for p_ in prix["bordereau"]["postes"]
                     if p_["poste"] == "FOUI"
                     for m_ in (p_.get("materiaux") or [])
                     if m_["ressource"] == "evacuation_deblais_m3")
    # ce que le bordereau de D1 ignore
    pu_poste = next(p["debourse_sec_par_unite_MAD"] for p in prix["bordereau"]["postes"]
                    if p["poste"] == "FOUI")
    return {
        "decapage_m3": decapage,
        "fouille_verticale_m3": vertical,
        "controle_la_fouille_verticale_est_le_prisme": {
            "prisme_L_x_W_x_h_m3": round(L * W * h, 1),
            "quantite_du_bordereau_m3": vertical,
            "ecart_m3": round(L * W * h - vertical, 2)},
        "talus_m3": round(talus, 1),
        "talus_pct_du_prisme": round(talus / (L * W * h) * 100, 1),
        "trois_voies_du_volume_talute": {
            "integrale_exacte_m3": round(exact, 2),
            "formule_prismatique_m3": round(prisme, 2),
            "methode_des_profils_m3": round(profils, 2),
            "ecart_prismatique_exact_m3": round(prisme - exact, 6),
            "ecart_profils_exact_m3": round(profils - exact, 2),
            "ecart_profils_pct": round((profils - exact) / exact * 100, 2),
            # L'erreur de la methode des profils se demontre en une ligne : la moyenne
            # des aires integre le terme quadratique avec un coefficient 1/2 la ou
            # l'integrale le prend avec 1/3. L'ecart vaut donc a.b.h3(1/2 - 1/3) =
            # a.b.h3/6, avec a = cL.m et b = cW.m. Une premiere version de ce module
            # publiait a.b.h3/3 — le double — et le nombre publie a cote, lui, etait
            # juste : c'est la phrase a cote du nombre, encore une fois.
            "forme_fermee_de_l_erreur": round(cL * m * cW * m * h ** 3 / 6, 2),
            "_regle": ("La formule prismatique est EXACTE pour une fouille talutée, "
                       "parce que l'aire de la section varie comme un polynôme de "
                       "degré deux et que Simpson intègre exactement un polynôme de "
                       "degré trois. La méthode des profils surestime, et son erreur a "
                       "elle aussi une forme fermée : a·b·h³/6 avec a = cL·m et "
                       "b = cW·m."),
        },
        "volume_en_place_m3": round(en_place, 1),
        "foisonnement_pct": round(foisonnement * 100, 1),
        "reemploi_pct": round(reemploi * 100, 1),
        "reutilise_en_remblai_m3": round(reutilise, 1),
        "au_depot_en_place_m3": round(au_depot, 1),
        "transporte_foisonne_m3": round(transporte, 1),
        "prix_evacuation_MAD_m3_foisonne": pu,
        "cout_evacuation_MAD": round(transporte * pu),
        "manque_au_bordereau": {
            "volume_m3": round(talus, 1),
            "pu_du_poste_FOUI_MAD_m3": pu_poste,
            "montant_MAD": round(talus * pu_poste),
            "_pourquoi": ("Le bordereau de D1 cube la fouille comme un prisme vertical "
                          "de L x W x h. C'est exact pour un ouvrage blindé sur ses "
                          "quatre côtés ; dès qu'un côté est taluté, il manque le "
                          "volume du talus — à déblayer, à charger, à transporter et à "
                          "mettre en dépôt comme le reste."),
        },
        "evacuation_du_bordereau_de_D1": {
            "volume_cube_par_D1_m3": round(volume_D1 := decapage + vertical, 1),
            "coefficient_du_sous_detail": coef_evac,
            "volume_facture_foisonne_m3": round(volume_D1 * coef_evac, 1),
            "montant_MAD": round(volume_D1 * coef_evac * pu),
            "montant_de_C2_MAD": round(transporte * pu),
            "ecart_MAD": round((volume_D1 * coef_evac - transporte) * pu),
            "_deux_erreurs_de_sens_contraire": (
                "Le bordereau de D1 évacue CENT POUR CENT de ce qu'il cube, sans "
                "réemploi en remblai, et il ne cube pas le talus. Les deux écarts vont "
                "en sens inverse : le réemploi retire du volume, le talus en ajoute. Le "
                "net est publié ci-dessus, et il ne dispense pas de corriger les deux "
                "lignes — un total juste par compensation reste faux deux fois."),
        },
        "surface_de_blindage_m2": geo["surface_de_blindage_m2"],
        "cout_du_blindage_MAD": round(
            geo["surface_de_blindage_m2"] * _v(d["terrassement"]["fouille"]["blindage_MAD_m2"])),
    }


# ------------------------------------------------------------- 4. la rotation
def debit_de_la_pelle(d: dict) -> dict:
    """Débit d'une pelle, en m³ foisonnés et en m³ en place.

    Attention au piège d'unité, et c'est le plus classique du terrassement : un godet
    transporte du terrain FOISONNÉ, un métré compte du terrain EN PLACE. Les deux
    diffèrent du foisonnement, et confondre les deux surestime le débit d'un quart.
    """
    p = d["terrassement"]["pelle"]
    godet, cycle = _v(p["godet_m3"]), _v(p["temps_de_cycle_s"])
    k = _v(p["coefficient_de_remplissage"])
    foi = 1 + _v(d["planning"]["ratios_quantites_V3"]["foisonnement_pct"]) / 100
    foisonne = godet * k * 3600 / cycle
    return {
        "godet_m3": godet, "temps_de_cycle_s": cycle, "coefficient_de_remplissage": k,
        "cycles_par_heure": round(3600 / cycle, 1),
        "debit_foisonne_m3_h": round(foisonne, 1),
        "debit_en_place_m3_h": round(foisonne / foi, 1),
        "foisonnement": round(foi, 3),
        "_piege": ("Le godet charge du terrain FOISONNÉ ; le métré et le bordereau "
                   "comptent du terrain EN PLACE. Le débit utile est donc le débit du "
                   "godet divisé par le foisonnement, et non le débit du godet."),
    }


def rotation(d: dict, pelle: dict, distance_km: float | None = None,
             nb_camions: int | None = None) -> dict:
    """Cycle d'un camion, flotte nécessaire, et cadence réellement tenue.

    Deux voies pour la cadence, et c'est le contre-calcul du module :
      (a) par la CAPACITÉ DE CHARGEMENT : la pelle ne peut pas sortir plus que son
          débit, quel que soit le nombre de camions ;
      (b) par la ROTATION : N camions de capacité C sur un cycle T sortent N·C/T.
    La cadence tenue est le minimum des deux, et elle plafonne sur (a).
    """
    c, dep = d["terrassement"]["camion"], d["terrassement"]["depot"]
    dist = _v(dep["distance_km"]) if distance_km is None else distance_km
    vit = _v(dep["vitesse_moyenne_km_h"])
    cap = _v(c["capacite_m3"])
    t_charge = cap / pelle["debit_foisonne_m3_h"] * 60
    t_trajet = 2 * dist / vit * 60
    t_cycle = t_charge + t_trajet + _v(c["temps_de_dechargement_min"]) + \
        _v(c["temps_de_manoeuvre_min"])
    # flotte qui sature la pelle : le cycle divisé par le temps de chargement
    flotte_saturante = t_cycle / t_charge
    out = {
        "distance_km": dist, "capacite_camion_m3": cap,
        "temps_de_chargement_min": round(t_charge, 2),
        "temps_de_trajet_aller_retour_min": round(t_trajet, 1),
        "temps_de_dechargement_min": _v(c["temps_de_dechargement_min"]),
        "temps_de_manoeuvre_min": _v(c["temps_de_manoeuvre_min"]),
        "temps_de_cycle_min": round(t_cycle, 1),
        "part_du_cycle_en_route_pct": round(t_trajet / t_cycle * 100, 1),
        "flotte_qui_sature_la_pelle": math.ceil(flotte_saturante),
        "flotte_qui_sature_la_pelle_exacte": round(flotte_saturante, 2),
    }
    if nb_camions is not None:
        par_rotation = nb_camions * cap / (t_cycle / 60)
        tenu = min(pelle["debit_foisonne_m3_h"], par_rotation)
        out.update({
            "nb_camions": nb_camions,
            "cadence_par_rotation_m3_h_foisonne": round(par_rotation, 1),
            "cadence_de_la_pelle_m3_h_foisonne": pelle["debit_foisonne_m3_h"],
            "cadence_tenue_m3_h_foisonne": round(tenu, 1),
            "cadence_tenue_m3_h_en_place": round(tenu / pelle["foisonnement"], 1),
            "ce_qui_borne": ("la pelle" if par_rotation >= pelle["debit_foisonne_m3_h"]
                             else "la rotation des camions"),
            "taux_d_emploi_de_la_pelle_pct": round(
                min(1.0, par_rotation / pelle["debit_foisonne_m3_h"]) * 100, 1),
        })
    return out


def flotte_pour_une_cadence(d: dict, pelle: dict, cadence_en_place: float,
                            distance_km: float | None = None) -> dict:
    """Combien de camions faut-il pour tenir une cadence donnée, à une distance donnée.

    C'est la question que la cadence déclarée par D2 pose sans y répondre : sa note dit
    « pelle 30 t + rotation de camions, trajet court », et ne chiffre ni la flotte ni le
    trajet.
    """
    r = rotation(d, pelle, distance_km)
    cible = cadence_en_place * pelle["foisonnement"]
    n = cible / (_v(d["terrassement"]["camion"]["capacite_m3"]) / (r["temps_de_cycle_min"] / 60))
    return {"distance_km": r["distance_km"], "temps_de_cycle_min": r["temps_de_cycle_min"],
            "cadence_cible_en_place_m3_h": round(cadence_en_place, 1),
            "camions_exacts": round(n, 2), "camions": math.ceil(n),
            "au_dela_de_la_pelle": bool(cible > pelle["debit_foisonne_m3_h"])}


# -------------------------------------------- 5. la cadence de D2, et les deux pelles
def cadence_declaree(d: dict, pl: dict, prix: dict, pelle: dict, cub: dict) -> dict:
    """La cadence de D2 relue par la rotation — et le nombre de pelles qu'elle suppose.

    D2 calcule les durées de TERR et de FOUI par « volume / (cadence d'atelier x
    nombre d'ateliers) ». Deux ateliers de terrassement, c'est deux pelles. Le module
    C6, qui a chiffré le matériel, compte les heures d'UNE pelle sur ces tâches : on
    publie l'écart au lieu de laisser deux modules se contredire en silence.
    """
    cad_at = _v(d["planning"]["cadences_chantier_V3"]["terrassement_m3_j_atelier"])
    nb_at = float(d["planning"]["effectifs_chantier_V3"]["ateliers_terrassement"])
    h_jour = float(d["planning"]["calendrier"]["heures_par_jour"])
    par_atelier_h = cad_at / h_jour
    flotte = flotte_pour_une_cadence(d, pelle, par_atelier_h)
    duree_D2 = sum(pl["durees"][t]["duree_j"] for t in ("TERR", "FOUI"))
    # durée que le même volume demande une fois le talus compté
    volume_D2 = cub["decapage_m3"] + cub["fouille_verticale_m3"]
    volume_reel = cub["volume_en_place_m3"]
    duree_reelle = volume_reel / (cad_at * nb_at)
    # ce que C6 a compté pour la pelle sur ces deux tâches
    mat = json.loads((RACINE / "calc" / "sorties" / "materiel.json").read_text(
        encoding="utf-8"))
    hpjs = mat["emplois"]["pelle"]["heures_par_jour_servi_h"]
    prix_h = _v(d["prix_unitaires_MAD"]["ressources"]["materiel_MAD"]["pelle_30t_h"])
    h_une_pelle = duree_D2 * hpjs
    return {
        "cadence_d_atelier_m3_j": cad_at,
        "nb_ateliers": nb_at,
        "cadence_d_atelier_m3_h": round(par_atelier_h, 1),
        "cadence_du_chantier_m3_j": round(cad_at * nb_at, 1),
        "flotte_par_atelier": flotte["camions"],
        "flotte_du_chantier": int(flotte["camions"] * nb_at),
        "flotte_exacte_par_atelier": flotte["camions_exacts"],
        "taux_d_emploi_de_la_pelle_a_cette_cadence_pct": round(
            par_atelier_h * pelle["foisonnement"] / pelle["debit_foisonne_m3_h"] * 100, 1),
        "_note_trajet_court": (
            "La note de la cadence de D2 dit « trajet court » sans le chiffrer. À "
            f"{_f(_v(d['terrassement']['depot']['distance_km']), 0)} km de dépôt, le "
            f"cycle d'un camion dure {_f(flotte['temps_de_cycle_min'], 0)} min, dont "
            f"{_f(rotation(d, pelle)['part_du_cycle_en_route_pct'], 0)} % de route."),
        "duree_declaree_par_D2_j": round(duree_D2, 2),
        "volume_que_D2_a_cube_m3": round(volume_D2, 1),
        "volume_reel_avec_talus_m3": round(volume_reel, 1),
        "duree_avec_le_talus_j": round(duree_reelle, 2),
        "allongement_j": round(duree_reelle - duree_D2, 2),
        "allongement_pct": round((duree_reelle - duree_D2) / duree_D2 * 100, 1),
        "marge_totale_de_FOUI_j": pl["durees"]["FOUI"]["marge_totale_j"],
        "l_allongement_tient_dans_la_marge": bool(
            duree_reelle - duree_D2 <= pl["durees"]["FOUI"]["marge_totale_j"]),
        "_perimetre": (
            "L'allongement est absorbé par la marge totale de la tâche : il ne coûte "
            "donc AUCUN jour de chantier, et confondre les deux périmètres ferait "
            "annoncer un retard qui n'existe pas. Ce qu'il coûte est un VOLUME, et le "
            "volume se paie à l'évacuation."),
        "deux_pelles": {
            "ateliers": nb_at,
            "heures_comptees_par_C6_h": round(h_une_pelle, 1),
            "heures_reelles_h": round(h_une_pelle * nb_at, 1),
            "ecart_h": round(h_une_pelle * (nb_at - 1), 1),
            "prix_horaire_MAD": prix_h,
            "ecart_MAD": round(h_une_pelle * (nb_at - 1) * prix_h),
            "part_du_cout_pelle_de_C6_pct": round(
                h_une_pelle * (nb_at - 1) * prix_h
                / next(l["cout_sur_le_chantier_MAD"] for l in mat["cout_du_parc"]["lignes"]
                       if l["cle"] == "pelle") * 100, 1),
            "_pourquoi": (
                "Une cadence d'atelier multipliée par deux ateliers, c'est deux pelles "
                "sur le site en même temps. Le module C6 déduit les heures de la pelle "
                "des jours de ses tâches, sans savoir combien de machines les servent : "
                "il compte donc une pelle là où le planning en suppose deux."),
        },
    }


# --------------------------------------------------------------------------- figures
def figures(d: dict, geo: dict, cub: dict, pelle: dict, cad: dict) -> dict:
    dep = d["terrassement"]["depot"]
    # 1. la séquence d'exécution
    f1 = ["Décapage de l'emprise et dépôt de la terre végétale",
          "Blindage du côté voies, avant toute fouille",
          "Fouille en pleine masse, talus sur les trois autres côtés",
          "Finition et réglage du fond de fouille",
          "Réception du fond de fouille, point d'arrêt"]
    # 2. le bilan des terres
    f2 = [{"libelle": "Décapage", "valeur": cub["decapage_m3"]},
          {"libelle": "Fouille verticale", "valeur": cub["fouille_verticale_m3"]},
          {"libelle": "Talus (hors bordereau)", "valeur": cub["talus_m3"], "alerte": True},
          {"libelle": "Réemployé en remblai", "valeur": cub["reutilise_en_remblai_m3"]},
          {"libelle": "Au dépôt, en place", "valeur": cub["au_depot_en_place_m3"]},
          {"libelle": "Transporté, foisonné", "valeur": cub["transporte_foisonne_m3"]}]
    # 3. la flotte en fonction de la distance au dépôt
    f3 = {"points": [], "marqueur": None}
    for km in dep["distances_a_comparer_km"]:
        fl = flotte_pour_une_cadence(d, pelle, cad["cadence_d_atelier_m3_h"], float(km))
        f3["points"].append({"x": float(km), "v": float(fl["camions"])})
    f3["marqueur"] = {"x": _v(dep["distance_km"]),
                      "libelle": f"{_f(_v(dep['distance_km']), 0)} km retenus → "
                                 f"{cad['flotte_par_atelier']} camions"}
    # 4. la cadence tenue en fonction du nombre de camions
    f4 = {"points": [], "marqueur": None}
    for n in dep["camions_a_comparer"]:
        r = rotation(d, pelle, None, int(n))
        f4["points"].append({"x": float(n), "v": r["cadence_tenue_m3_h_en_place"]})
    sat = rotation(d, pelle)["flotte_qui_sature_la_pelle"]
    f4["marqueur"] = {"x": float(sat), "libelle": f"{sat} camions saturent la pelle"}
    return {"sequence": f1, "bilan": f2, "flotte_vs_distance": f3,
            "cadence_vs_camions": f4}


# ------------------------------------------------------------------------- assemblage
def tout_calculer(d: dict) -> dict:
    S = RACINE / "calc" / "sorties"
    pl = json.loads((S / "planification.json").read_text(encoding="utf-8"))
    prix = json.loads((S / "prix.json").read_text(encoding="utf-8"))
    geo = geometrie(d)
    cub = cubatures(d, prix, geo)
    pelle = debit_de_la_pelle(d)
    rot = rotation(d, pelle, None, rotation(d, pelle)["flotte_qui_sature_la_pelle"])
    cad = cadence_declaree(d, pl, prix, pelle, cub)
    rot_retenue = rotation(d, pelle, None, cad["flotte_par_atelier"])
    return {
        "geometrie": geo, "cubatures": cub, "pelle": pelle,
        "rotation_saturante": rot, "rotation_retenue": rot_retenue,
        "cadence_declaree": cad,
        "figures": figures(d, geo, cub, pelle, cad),
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    r = tout_calculer(d)
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "terrassement.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    g, c, p = r["geometrie"], r["cubatures"], r["pelle"]
    print(f"  fouille {g['longueur_m']:.0f} x {g['largeur_m']:.0f} x {g['profondeur_m']:.2f} m · "
          f"recul necessaire {g['recul_necessaire_par_cote_m']} m · "
          f"{g['nb_cotes_talutes']} cotes talutes, {g['nb_cotes_blindes']} blinde "
          f"({g['surface_de_blindage_m2']:.0f} m2)")
    t = c["trois_voies_du_volume_talute"]
    print(f"  talus {c['talus_m3']:.0f} m3 (+{c['talus_pct_du_prisme']} % du prisme) · "
          f"exacte {t['integrale_exacte_m3']:.1f} = prismatique "
          f"{t['formule_prismatique_m3']:.1f} · profils {t['methode_des_profils_m3']:.1f} "
          f"(+{t['ecart_profils_pct']} %)")
    print(f"  bilan : {c['volume_en_place_m3']:.0f} m3 en place -> "
          f"{c['transporte_foisonne_m3']:.0f} m3 transportes = "
          f"{c['cout_evacuation_MAD']:,} MAD".replace(",", " "))
    print(f"  manque au bordereau : {c['manque_au_bordereau']['volume_m3']:.0f} m3 = "
          f"{c['manque_au_bordereau']['montant_MAD']:,} MAD".replace(",", " "))
    print(f"  pelle {p['debit_foisonne_m3_h']:.0f} m3/h foisonnes = "
          f"{p['debit_en_place_m3_h']:.0f} en place · "
          f"{r['rotation_saturante']['nb_camions']} camions la saturent "
          f"(cycle {r['rotation_saturante']['temps_de_cycle_min']:.0f} min)")
    cd = r["cadence_declaree"]
    print(f"  D2 : {cd['cadence_du_chantier_m3_j']:.0f} m3/j avec {cd['nb_ateliers']:.0f} "
          f"ateliers -> {cd['flotte_du_chantier']} camions, pelle a "
          f"{cd['taux_d_emploi_de_la_pelle_a_cette_cadence_pct']} % · duree "
          f"{cd['duree_declaree_par_D2_j']} j -> {cd['duree_avec_le_talus_j']} j avec le talus")
    dp = cd["deux_pelles"]
    print(f"  deux pelles : C6 compte {dp['heures_comptees_par_C6_h']} h, il en faut "
          f"{dp['heures_reelles_h']} -> {dp['ecart_MAD']:,} MAD "
          f"({dp['part_du_cout_pelle_de_C6_pct']} % du cout pelle de C6)".replace(",", " "))
