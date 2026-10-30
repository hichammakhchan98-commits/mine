"""Tests du module C2 — terrassements, fouilles et evacuation des terres.

Des tests de REGLE. Aucun n'epingle « 831 m3 » ni « 15 camions » : ils verifient qu'un
recul de talus est un fruit fois une hauteur plus une banquette, qu'un cote se blinde
quand la place manque, qu'un volume talute se mesure par trois voies dont deux sont
exactes, qu'un debit de godet se divise par le foisonnement, et qu'une cadence est le
minimum de la pelle et de la rotation. Six canaris cherchent l'erreur au lieu de la
confirmer.
"""
from __future__ import annotations
import json, math, sys, pathlib, unicodedata

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))

echecs = []


def sansaccent(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s).lower())
                   if unicodedata.category(c) != "Mn").replace("œ", "oe")


def dit(texte, *mots):
    t_ = sansaccent(texte)
    return all(sansaccent(m) in t_ for m in mots)


def verifie(nom, condition, detail=""):
    if not condition:
        echecs.append(nom)
    print(f"  {'ok   ' if condition else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


S = RACINE / "calc" / "sorties"
d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
r = json.loads((S / "terrassement.json").read_text(encoding="utf-8"))
pl = json.loads((S / "planification.json").read_text(encoding="utf-8"))
prix = json.loads((S / "prix.json").read_text(encoding="utf-8"))
mat = json.loads((S / "materiel.json").read_text(encoding="utf-8"))
T = d["terrassement"]
import terrassement as te                                               # noqa: E402

G, C, P = r["geometrie"], r["cubatures"], r["pelle"]
RS, RR, CD = r["rotation_saturante"], r["rotation_retenue"], r["cadence_declaree"]


def val(o):
    return float(o["valeur"]) if isinstance(o, dict) else float(o)


# ------------------------------------------------- 1. la geometrie decide, pas une norme
print("\n--- la geometrie decide du mode de soutenement ---")
nt = next(n for n in d["geometrie"]["niveaux"] if n["nom"] == "niveau technique")
verifie("les dimensions de la fouille sont celles du niveau technique, non redeclarees",
        [G["longueur_m"], G["largeur_m"]] == [float(x) for x in nt["emprise_partielle_m"]]
        and not any("longueur" in k or "largeur" in k for k in T["fouille"]))
verifie("la profondeur est l'altitude du niveau PLUS la surprofondeur de forme de D1",
        abs(G["profondeur_m"] - (abs(float(nt["altitude_m"]))
            + val(d["planning"]["ratios_quantites_V3"]["surprofondeur_forme_m"]))) < 1e-9,
        f"{G['profondeur_m']} m")
verifie("le recul necessaire est fruit x profondeur + banquette",
        abs(G["recul_necessaire_par_cote_m"]
            - (G["fruit"] * G["profondeur_m"] + G["banquette_m"])) < 1e-9,
        f"{G['recul_necessaire_par_cote_m']} m")
for c in G["cotes"]:
    verifie(f"« {c['cote'][:26]} » : talutable si et seulement si la place y est",
            c["talutable"] == (c["place_disponible_m"] >= G["recul_necessaire_par_cote_m"])
            and c["mode"] == ("talus" if c["talutable"] else "blindage")
            and abs(c["marge_m"] - (c["place_disponible_m"]
                                    - G["recul_necessaire_par_cote_m"])) < 0.01,
            f"{c['place_disponible_m']} m pour {c['recul_necessaire_m']} m")
    verifie(f"« {c['cote'][:26]} » : la place disponible est JUSTIFIEE en clair",
            len(c["_place"]) > 40)
verifie("le cote blinde est celui qui touche la voie, et c'est le retrait qui le decide",
        G["cotes_blindes"] == [G["cotes"][0]["cote"]]
        and abs(G["cotes"][0]["place_disponible_m"]
                - float(T["fouille"]["retrait_facade_cote_voies_m"])) < 1e-9)
verifie("la surface de blindage est la longueur des cotes blindes x la profondeur",
        abs(G["surface_de_blindage_m2"]
            - sum(c["longueur_m"] for c in G["cotes"] if not c["talutable"])
            * G["profondeur_m"]) < 0.1, f"{G['surface_de_blindage_m2']} m2")
verifie("le fruit porte sa reserve : la pente admissible est un resultat de B2, pas "
        "une hypothese de C2",
        dit(T["fouille"]["fruit_de_talus"]["note"], "B2", "resultat")
        and dit(T["_role"], "B2"))
verifie("et la banquette aussi : aucune distance reglementaire n'est chiffree",
        dit(T["fouille"]["banquette_en_crete_m"]["note"], "reglementaire"))
verifie("la position de la fouille est une DECISION, sans fourchette",
        not isinstance(T["fouille"]["retrait_facade_cote_voies_m"], dict)
        and dit(T["fouille"]["_retrait"], "decision"))
verifie("la position publiee tient dans l'emprise du batiment",
        0 <= G["position"]["y_de_m"] and G["position"]["y_a_m"]
        <= float(d["geometrie"]["emprise_m"][1])
        and 0 <= G["position"]["x_de_m"] and G["position"]["x_a_m"]
        <= float(d["geometrie"]["emprise_m"][0]))

# ------------------------------------------------- 2. les trois voies du volume
print("\n--- trois voies pour un volume talute, dont deux exactes ---")
V = C["trois_voies_du_volume_talute"]
L, W, h, m = G["longueur_m"], G["largeur_m"], G["profondeur_m"], G["fruit"]
cL, cW = G["cotes_talutes_en_longueur"], G["cotes_talutes_en_largeur"]
verifie("l'integrale exacte est celle du module, recalculee ici",
        abs(V["integrale_exacte_m3"]
            - te.volume_talus_exact(L, W, m, h, cL, cW)) < 0.01)
verifie("la formule prismatique est EXACTE, au dixieme de m3 pres",
        abs(V["ecart_prismatique_exact_m3"]) < 0.01,
        f"{V['ecart_prismatique_exact_m3']} m3")
verifie("la methode des profils SURESTIME",
        V["ecart_profils_exact_m3"] > 0, f"+{V['ecart_profils_exact_m3']} m3")
verifie("et son erreur vaut exactement a.b.h3/6, avec a = cL.m et b = cW.m",
        abs(V["ecart_profils_exact_m3"] - (cL * m) * (cW * m) * h ** 3 / 6) < 0.02
        and abs(V["forme_fermee_de_l_erreur"]
                - (cL * m) * (cW * m) * h ** 3 / 6) < 0.02,
        f"{V['forme_fermee_de_l_erreur']} m3")
verifie("la regle est ecrite, et elle nomme le DEGRE qui la justifie",
        dit(V["_regle"], "degre deux", "simpson"))
verifie("le nombre de cotes talutes par direction est coherent avec les modes",
        cL == sum(1 for c in G["cotes"][2:] if c["talutable"])
        and cW == sum(1 for c in G["cotes"][:2] if c["talutable"])
        and cL + cW == G["nb_cotes_talutes"])

# ------------------------------------------------- 3. les cubatures
print("\n--- le bilan des terres, et ce que le bordereau ignore ---")
q = {p_["poste"]: p_["quantite"] for p_ in prix["bordereau"]["postes"]}
verifie("le decapage et la fouille verticale sont LUS dans le bordereau de D1",
        C["decapage_m3"] == q["TERR"] and C["fouille_verticale_m3"] == q["FOUI"])
verifie("et la fouille verticale du bordereau EST le prisme de la geometrie",
        abs(C["controle_la_fouille_verticale_est_le_prisme"]["ecart_m3"]) < 0.5)
verifie("le talus est le volume talute moins le prisme",
        abs(C["talus_m3"] - (V["integrale_exacte_m3"] - L * W * h)) < 0.1,
        f"{C['talus_m3']} m3")
verifie("le volume en place est le decapage plus le volume talute",
        abs(C["volume_en_place_m3"]
            - (C["decapage_m3"] + V["integrale_exacte_m3"])) < 0.2)
verifie("le reemploi et le depot se partagent exactement le volume en place",
        abs(C["reutilise_en_remblai_m3"] + C["au_depot_en_place_m3"]
            - C["volume_en_place_m3"]) < 0.2)
verifie("le volume transporte est le volume au depot FOISONNE, et il est plus grand",
        abs(C["transporte_foisonne_m3"]
            - C["au_depot_en_place_m3"] * (1 + C["foisonnement_pct"] / 100)) < 0.2
        and C["transporte_foisonne_m3"] > C["au_depot_en_place_m3"])
verifie("le prix d'evacuation est celui du bordereau de D1, non redeclare",
        C["prix_evacuation_MAD_m3_foisonne"]
        == val(d["prix_unitaires_MAD"]["ressources"]["materiaux_MAD"]["evacuation_deblais_m3"])
        and not any("evacuation" in k for k in T))
# Tolerance RELATIVE : les volumes publies sont arrondis au dixieme de m3, et les
# relire pour refaire le produit reinjecte cet arrondi.
verifie("le cout d'evacuation est le volume FOISONNE au prix du m3 foisonne",
        abs(C["cout_evacuation_MAD"] - C["transporte_foisonne_m3"]
            * C["prix_evacuation_MAD_m3_foisonne"]) < 1e-4 * C["cout_evacuation_MAD"])
MQ = C["manque_au_bordereau"]
verifie("ce qui manque au bordereau est exactement le volume de talus",
        MQ["volume_m3"] == C["talus_m3"]
        and abs(MQ["montant_MAD"] - MQ["volume_m3"] * MQ["pu_du_poste_FOUI_MAD_m3"]) < 2,
        f"{MQ['volume_m3']} m3 = {MQ['montant_MAD']:,} MAD".replace(",", " "))
verifie("et la raison est ecrite : D1 cube un prisme vertical",
        dit(MQ["_pourquoi"], "prisme vertical"))
EV = C["evacuation_du_bordereau_de_D1"]
verifie("le coefficient du sous-detail de D1 est lu dans son poste FOUI",
        EV["coefficient_du_sous_detail"]
        == next(x["quantite"] for p_ in prix["bordereau"]["postes"]
                if p_["poste"] == "FOUI" for x in p_["materiaux"]
                if x["ressource"] == "evacuation_deblais_m3"))
verifie("l'ecart avec C2 est la difference des deux volumes factures, au meme prix",
        abs(EV["ecart_MAD"] - (EV["volume_facture_foisonne_m3"]
                               - C["transporte_foisonne_m3"])
            * C["prix_evacuation_MAD_m3_foisonne"]) < 1e-4 * abs(EV["ecart_MAD"]),
        f"{EV['ecart_MAD']:,} MAD".replace(",", " "))
verifie("et le module dit que les DEUX lignes sont fausses, pas seulement leur total",
        dit(EV["_deux_erreurs_de_sens_contraire"], "sens inverse", "deux fois"))
verifie("le cout du blindage est la surface au prix declare",
        abs(C["cout_du_blindage_MAD"] - G["surface_de_blindage_m2"]
            * val(T["fouille"]["blindage_MAD_m2"])) < 2)

# ------------------------------------------------- 4. la pelle et la rotation
print("\n--- la pelle charge, les camions roulent, le plus lent commande ---")
pe = T["pelle"]
verifie("le debit foisonne est godet x remplissage x 3600/cycle",
        abs(P["debit_foisonne_m3_h"] - val(pe["godet_m3"])
            * val(pe["coefficient_de_remplissage"])
            * 3600 / val(pe["temps_de_cycle_s"])) < 0.1,
        f"{P['debit_foisonne_m3_h']} m3/h")
verifie("le debit EN PLACE est le debit foisonne divise par le foisonnement",
        abs(P["debit_en_place_m3_h"]
            - P["debit_foisonne_m3_h"] / P["foisonnement"]) < 0.1
        and P["debit_en_place_m3_h"] < P["debit_foisonne_m3_h"])
verifie("le foisonnement est celui de D2, non redeclare",
        abs(P["foisonnement"] - (1 + val(
            d["planning"]["ratios_quantites_V3"]["foisonnement_pct"]) / 100)) < 1e-9
        and not any("foisonn" in k for k in T))
verifie("et le piege d'unite est ecrit noir sur blanc",
        dit(P["_piege"], "foisonne", "en place"))
ca, dep = T["camion"], T["depot"]
verifie("le temps de chargement est la capacite divisee par le debit FOISONNE",
        abs(RS["temps_de_chargement_min"] - val(ca["capacite_m3"])
            / P["debit_foisonne_m3_h"] * 60) < 0.02)
verifie("le temps de trajet est l'aller-RETOUR a la vitesse moyenne",
        abs(RS["temps_de_trajet_aller_retour_min"] - 2 * val(dep["distance_km"])
            / val(dep["vitesse_moyenne_km_h"]) * 60) < 0.1)
verifie("le cycle est la somme de ses quatre temps",
        abs(RS["temps_de_cycle_min"] - (RS["temps_de_chargement_min"]
            + RS["temps_de_trajet_aller_retour_min"]
            + RS["temps_de_dechargement_min"]
            + RS["temps_de_manoeuvre_min"])) < 0.1,
        f"{RS['temps_de_cycle_min']} min")
verifie("la route pese plus que tout le reste du cycle",
        RS["part_du_cycle_en_route_pct"] > 50,
        f"{RS['part_du_cycle_en_route_pct']} %")
verifie("la flotte saturante est le cycle divise par le chargement, arrondi AU-DESSUS",
        RS["flotte_qui_sature_la_pelle"]
        == math.ceil(RS["temps_de_cycle_min"] / RS["temps_de_chargement_min"])
        and abs(RS["flotte_qui_sature_la_pelle_exacte"]
                - RS["temps_de_cycle_min"] / RS["temps_de_chargement_min"]) < 0.01,
        f"{RS['flotte_qui_sature_la_pelle']} camions")
for rot, nom in ((RS, "a la flotte saturante"), (RR, "a la flotte retenue")):
    verifie(f"{nom} : la cadence de rotation est N x capacite / cycle",
            abs(rot["cadence_par_rotation_m3_h_foisonne"] - rot["nb_camions"]
                * val(ca["capacite_m3"]) / (rot["temps_de_cycle_min"] / 60)) < 0.2)
    verifie(f"{nom} : la cadence tenue est le MINIMUM de la pelle et de la rotation",
            abs(rot["cadence_tenue_m3_h_foisonne"]
                - min(P["debit_foisonne_m3_h"],
                      rot["cadence_par_rotation_m3_h_foisonne"])) < 0.2
            and rot["ce_qui_borne"] == (
                "la pelle" if rot["cadence_par_rotation_m3_h_foisonne"]
                >= P["debit_foisonne_m3_h"] else "la rotation des camions"))
    verifie(f"{nom} : la cadence tenue en place est la cadence foisonnee / foisonnement",
            abs(rot["cadence_tenue_m3_h_en_place"]
                - rot["cadence_tenue_m3_h_foisonne"] / P["foisonnement"]) < 0.2)
    verifie(f"{nom} : le taux d'emploi de la pelle est borne a 100 %",
            0 < rot["taux_d_emploi_de_la_pelle_pct"] <= 100)
verifie("la flotte saturante sature VRAIMENT : c'est la pelle qui borne",
        RS["ce_qui_borne"] == "la pelle"
        and RS["taux_d_emploi_de_la_pelle_pct"] == 100.0)
verifie("et la flotte retenue, plus petite, laisse la pelle attendre",
        RR["nb_camions"] < RS["nb_camions"]
        and RR["ce_qui_borne"] == "la rotation des camions"
        and RR["taux_d_emploi_de_la_pelle_pct"] < 100,
        f"{RR['nb_camions']} camions, pelle a {RR['taux_d_emploi_de_la_pelle_pct']} %")

# ------------------------------------------------- 5. la cadence de D2
print("\n--- la cadence declaree par D2, relue par la rotation ---")
verifie("la cadence d'atelier et le nombre d'ateliers sont ceux de D2, non redeclares",
        CD["cadence_d_atelier_m3_j"]
        == val(d["planning"]["cadences_chantier_V3"]["terrassement_m3_j_atelier"])
        and CD["nb_ateliers"]
        == float(d["planning"]["effectifs_chantier_V3"]["ateliers_terrassement"]))
verifie("la cadence horaire passe par les heures par jour du calendrier de D2",
        abs(CD["cadence_d_atelier_m3_h"] - CD["cadence_d_atelier_m3_j"]
            / float(d["planning"]["calendrier"]["heures_par_jour"])) < 0.05)
verifie("la flotte du chantier est celle d'un atelier multipliee par les ateliers",
        CD["flotte_du_chantier"] == int(CD["flotte_par_atelier"] * CD["nb_ateliers"]))
verifie("la flotte par atelier est arrondie AU-DESSUS de sa valeur exacte",
        CD["flotte_par_atelier"] == math.ceil(CD["flotte_exacte_par_atelier"]))
verifie("a cette cadence la pelle est employee a moins de la moitie de son debit",
        CD["taux_d_emploi_de_la_pelle_a_cette_cadence_pct"] < 50,
        f"{CD['taux_d_emploi_de_la_pelle_a_cette_cadence_pct']} %")
verifie("le module releve que la note de D2 dit « trajet court » sans le chiffrer",
        dit(CD["_note_trajet_court"], "trajet court", "km"))
verifie("la duree declaree est la somme des deux taches de D2, non recalculee",
        abs(CD["duree_declaree_par_D2_j"]
            - sum(pl["durees"][t]["duree_j"] for t in ("TERR", "FOUI"))) < 0.01)
verifie("le volume que D2 a cube est le decapage plus le prisme, sans le talus",
        abs(CD["volume_que_D2_a_cube_m3"]
            - (C["decapage_m3"] + C["fouille_verticale_m3"])) < 0.2
        and CD["volume_reel_avec_talus_m3"] > CD["volume_que_D2_a_cube_m3"])
verifie("la duree avec le talus est le volume reel a la cadence du chantier",
        abs(CD["duree_avec_le_talus_j"] - CD["volume_reel_avec_talus_m3"]
            / CD["cadence_du_chantier_m3_j"]) < 0.02,
        f"{CD['duree_avec_le_talus_j']} j contre {CD['duree_declaree_par_D2_j']}")
verifie("l'allongement tient dans la marge totale de la tache, et le module le DIT",
        CD["l_allongement_tient_dans_la_marge"]
        and CD["allongement_j"] <= CD["marge_totale_de_FOUI_j"]
        and dit(CD["_perimetre"], "marge", "aucun jour"),
        f"+{CD['allongement_j']} j pour {CD['marge_totale_de_FOUI_j']} j de marge")

print("\n--- deux ateliers, donc deux pelles : l'ecart avec C6 ---")
DP = CD["deux_pelles"]
verifie("les heures comptees par C6 sont la duree des taches x son intensite d'emploi",
        abs(DP["heures_comptees_par_C6_h"] - CD["duree_declaree_par_D2_j"]
            * mat["emplois"]["pelle"]["heures_par_jour_servi_h"]) < 0.1)
verifie("les heures reelles sont celles d'une pelle multipliees par les ateliers",
        abs(DP["heures_reelles_h"]
            - DP["heures_comptees_par_C6_h"] * DP["ateliers"]) < 0.2)
verifie("l'ecart en MAD est l'ecart en heures au prix horaire de D1",
        abs(DP["ecart_MAD"] - DP["ecart_h"] * DP["prix_horaire_MAD"])
        < 1e-3 * DP["ecart_MAD"]
        and DP["prix_horaire_MAD"]
        == val(d["prix_unitaires_MAD"]["ressources"]["materiel_MAD"]["pelle_30t_h"]))
verifie("et il se rapporte au cout de la pelle que C6 publie",
        abs(DP["part_du_cout_pelle_de_C6_pct"] - DP["ecart_MAD"]
            / next(l["cout_sur_le_chantier_MAD"] for l in mat["cout_du_parc"]["lignes"]
                   if l["cle"] == "pelle") * 100) < 0.2,
        f"{DP['part_du_cout_pelle_de_C6_pct']} % du cout pelle de C6")
verifie("la raison est ecrite : C6 deduit des heures sans savoir combien de machines",
        dit(DP["_pourquoi"], "deux pelles", "une pelle"))

# ------------------------------------------------- 6. ce que le module ne refait pas
print("\n--- aucun doublon, et aucune valeur normative ---")
verifie("le prix de location de la pelle n'est pas redeclare : il est chez D1",
        not any("MAD_h" in str(k) for k in T["pelle"]))
verifie("aucune quantite de decapage ni de fouille n'est declaree dans C2",
        not any("decapage" in k or "fouille_niveau" in k for k in T)
        and "decapage_m3" not in json.dumps(T))
# Les mots « rabattement », « stabilite » et « dimensionnement » APPARAISSENT dans le
# bloc, et c'est voulu : ils y figurent pour dire que ces sujets sont ⏸. Ce qu'il faut
# verifier n'est donc pas l'absence des mots mais l'absence de VALEURS : aucune clef
# numerique du bloc ne porte un nom de parametre geotechnique.
def _clefs(o, acc=None):
    acc = [] if acc is None else acc
    if isinstance(o, dict):
        for k, v in o.items():
            acc.append(k)
            _clefs(v, acc)
    elif isinstance(o, list):
        for v in o:
            _clefs(v, acc)
    return acc


verifie("aucune CLEF de ce bloc ne porte un parametre geotechnique : les valeurs de "
        "stabilite, de poussee et de rabattement sont ⏸, pas declarees",
        not any(x in sansaccent(k) for k in _clefs(T)
                for x in ("cohesion", "frottement", "poussee", "rabattement",
                          "pression", "phi", "butee")))
verifie("et les trois sujets sont nommes comme ⏸ dans le role du bloc, au lieu d'etre "
        "passes sous silence",
        dit(T["_role"], "stabilite", "dimensionnement", "rabattement", "B2"))
verifie("la nappe du site est hors d'atteinte de cette fouille, et c'est LU dans data/",
        float(d["site"]["options"]["S1"]["nappe_m"]) > G["profondeur_m"],
        f"nappe a {d['site']['options']['S1']['nappe_m']} m pour une fouille de "
        f"{G['profondeur_m']} m")

# ------------------------------------------------- 7. canaris
print("\n--- canaris : six erreurs qu'un calcul juste doit refuser ---")
verifie("canari : cuber la fouille comme un prisme vertical perd le volume du talus",
        L * W * h < V["integrale_exacte_m3"]
        and abs(V["integrale_exacte_m3"] - L * W * h - C["talus_m3"]) < 0.1,
        f"{L * W * h:.0f} contre {V['integrale_exacte_m3']:.0f} m3")
verifie("canari : la methode des profils, employee seule, surfacture le talus",
        V["methode_des_profils_m3"] > V["integrale_exacte_m3"]
        and (V["methode_des_profils_m3"] - V["integrale_exacte_m3"])
        * C["prix_evacuation_MAD_m3_foisonne"] > 1000,
        f"+{(V['methode_des_profils_m3'] - V['integrale_exacte_m3']) * C['prix_evacuation_MAD_m3_foisonne']:.0f} MAD")
verifie("canari : oublier le foisonnement fait croire a une cadence de 25 % de plus",
        abs(P["debit_foisonne_m3_h"] / P["debit_en_place_m3_h"]
            - P["foisonnement"]) < 1e-3,
        f"x{P['foisonnement']}")
verifie("canari : dimensionner la flotte sur le debit de la pelle au lieu de la cadence "
        "demandee achete cinq camions de trop",
        RS["nb_camions"] - CD["flotte_par_atelier"] >= 3,
        f"{RS['nb_camions']} contre {CD['flotte_par_atelier']} camions")
# une banquette oubliee ferait croire que le cote voies est talutable
sans_banq = G["fruit"] * G["profondeur_m"]
verifie("canari : oublier la banquette en crete ferait taluter un cote qui ne peut pas "
        "l'etre",
        sans_banq < G["recul_necessaire_par_cote_m"]
        and float(T["fouille"]["retrait_facade_cote_voies_m"])
        < G["recul_necessaire_par_cote_m"],
        f"{sans_banq} m sans banquette contre {G['recul_necessaire_par_cote_m']} m avec")
# un fruit plus doux ne sauve pas le cote voies
verifie("canari : meme au fruit le plus doux de la fourchette, le cote voies reste "
        "a blinder",
        min(T["fouille"]["fruit_de_talus"]["fourchette"]) * G["profondeur_m"]
        + G["banquette_m"] > float(T["fouille"]["retrait_facade_cote_voies_m"]),
        f"{min(T['fouille']['fruit_de_talus']['fourchette']) * G['profondeur_m'] + G['banquette_m']:.2f} m "
        f"pour {T['fouille']['retrait_facade_cote_voies_m']} m disponibles")

# ------------------------------------------------- figures
print("\n--- figures ---")
f = r["figures"]
verifie("la sequence a cinq etapes, et le blindage y precede la fouille",
        len(f["sequence"]) == 5
        and [i for i, e in enumerate(f["sequence"]) if dit(e, "blindage")][0]
        < [i for i, e in enumerate(f["sequence"]) if dit(e, "pleine masse")][0])
verifie("la figure du bilan marque le talus comme alerte, et lui seul",
        sum(1 for x in f["bilan"] if x.get("alerte")) == 1
        and dit(next(x["libelle"] for x in f["bilan"] if x.get("alerte")), "talus"))
verifie("la courbe flotte / distance couvre la fourchette declaree de la distance",
        f["flotte_vs_distance"]["points"][0]["x"]
        <= min(T["depot"]["distance_km"]["fourchette"])
        and f["flotte_vs_distance"]["points"][-1]["x"]
        >= max(T["depot"]["distance_km"]["fourchette"]))
verifie("et elle croit avec la distance, sans exception",
        all(b["v"] >= a["v"] for a, b in zip(f["flotte_vs_distance"]["points"],
                                             f["flotte_vs_distance"]["points"][1:])))
verifie("son marqueur est la distance retenue",
        abs(f["flotte_vs_distance"]["marqueur"]["x"]
            - val(T["depot"]["distance_km"])) < 1e-9)
verifie("la courbe cadence / camions croit puis PLAFONNE sur le debit de la pelle",
        all(b["v"] >= a["v"] - 0.01 for a, b in zip(f["cadence_vs_camions"]["points"],
                                                    f["cadence_vs_camions"]["points"][1:]))
        and abs(f["cadence_vs_camions"]["points"][-1]["v"]
                - P["debit_en_place_m3_h"]) < 0.2)
verifie("et son marqueur est la flotte qui sature la pelle",
        f["cadence_vs_camions"]["marqueur"]["x"] == float(RS["nb_camions"]))

print()
if echecs:
    print(f"ECHEC : {len(echecs)} controle(s) — {', '.join(echecs[:4])}")
    sys.exit(1)
print("Tests terrassement : tous verts.")
