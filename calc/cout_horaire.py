"""Materiel : l'heure d'un engin, et ce qu'elle decide (module C6).

Cinq resultats, aucun reglementaire :

1. **Le cout horaire de possession est une FONCTION du taux d'emploi.** Une part fixe
   (amortissement, entretien, cout du capital) divisee par des heures, plus une part
   variable (carburant, conducteur). La question « louer ou acheter » ne se tranche
   donc pas sur une duree de detention mais sur un NOMBRE D'HEURES PAR AN, et il a une
   forme fermee.
2. **Ce qui decide n'est pas l'engin, c'est l'UNITE dans laquelle on le paie.** Trois
   regimes de location coexistent sur un meme chantier — par intervention, par heure de
   service, par duree de presence — et a heures de travail egales ils ne coutent pas du
   tout la meme chose. Le troisieme fait basculer la decision.
3. **Le taux d'emploi se LIT dans le planning**, il ne se declare pas. Les taches
   servies donnent les jours de travail ; la premiere et la derniere donnent la fenetre
   de presence. L'ecart entre les deux est ce que personne ne compte.
4. **Le rendement catalogue d'un engin n'existe pas sur un chantier.** Une chaine de
   facteurs mene du prospectus au debit reel, et son produit vaut la moitie. Le module
   C3 declare un debit pratique de pompe « et non son debit catalogue » : on le
   retrouve ici par une voie independante, et on mesure l'ecart (§ 3.3).
5. **La disponibilite d'une chaine est le PRODUIT des disponibilites.** Quatre maillons
   a 88 a 97 % ne font pas une chaine a 88 %. Et le secours ne se choisit pas sur le
   maillon le plus fragile : il se choisit sur le prix du point de chaine gagne.

Ce que le module ne dit pas : aucune duree reglementaire, aucune regle de controle
technique d'engin, aucune obligation de verification periodique n'est chiffree (⏸). Les
exigences de securite des appareils de levage relevent de la reglementation et du plan
HSE, et le cours ne les invente pas.
"""
from __future__ import annotations
import json, math, pathlib, random

RACINE = pathlib.Path(__file__).resolve().parent.parent

# Seuil de verdict, en part des tirages favorables a la possession. Entre les deux
# bornes, la decision n'est pas acquise a la precision de ces hypotheses.
SEUIL_VERDICT_PCT = 10.0


def _f(x: float, dec: int = 0) -> str:
    s = f"{x:,.{dec}f}".replace(",", " ")
    return s.replace(".", ",") if dec else s


def _b(o: dict) -> tuple[float, float]:
    f = o.get("fourchette")
    return (float(f[0]), float(f[1])) if f else (float(o["valeur"]), float(o["valeur"]))


def _v(o) -> float:
    return float(o["valeur"]) if isinstance(o, dict) else float(o)


def _prix_de_location(d: dict, fam: dict) -> dict:
    """L'objet de prix, LU dans le bordereau de D1 quand il le porte."""
    loc = fam["location"]
    return (d["prix_unitaires_MAD"]["ressources"]["materiel_MAD"][loc["cle_prix"]]
            if "cle_prix" in loc else loc["MAD_j"])


# --------------------------------------------------------- 1. le cout, a parametres donnes
def couts_annuels(par: dict, heures_par_an: float, unites_facturees_par_an: float) -> dict:
    """Couts ANNUELS de possession et de location pour UN jeu de parametres.

    Une seule implementation, utilisee par les trois voies : la forme fermee du point
    d'equilibre, les combinaisons extremes, et le tirage aleatoire. Deux
    implementations auraient partage leurs erreurs sans qu'aucun test ne le voie.

    Les deux quantites d'emploi sont PASSEES, et separement, parce qu'elles ne sont pas
    la meme chose : `heures_par_an` est du travail (il brule du carburant et occupe un
    conducteur), `unites_facturees_par_an` est ce que le loueur compte — des
    interventions, des heures de compteur, ou des jours de presence. Les confondre est
    l'erreur que ce module a commise dans sa premiere version : elle facturait a la
    pompe un jour de location par jour de tache, soit vingt-cinq fois son emploi reel.
    """
    amort = par["achat"] * (1 - par["residuelle"] / 100) / par["amort"]
    entretien = par["achat"] * par["entretien"] / 100
    # capital MOYEN engage : la demi-somme du prix d'achat et de la valeur residuelle
    financier = par["achat"] * (1 + par["residuelle"] / 100) / 2 * par["financier"] / 100
    fixe = amort + entretien + financier
    variable_h = par["carburant"] * par["gasoil"] + par["conducteur"]
    possession = fixe + heures_par_an * variable_h
    location = unites_facturees_par_an * par["prix_loc"]
    if not par["_operateur_compris"]:
        location += heures_par_an * par["conducteur"]
    return {"heures_par_an": heures_par_an,
            "unites_facturees_par_an": unites_facturees_par_an,
            "amortissement_MAD_an": amort, "entretien_MAD_an": entretien,
            "cout_financier_MAD_an": financier, "fixe_MAD_an": fixe,
            "variable_MAD_h": variable_h, "possession_MAD_an": possession,
            "location_MAD_an": location, "ecart_MAD_an": possession - location}


def parametres(d: dict, fam: dict, bornes: str = "nominal") -> dict:
    """Parametres d'un engin. `bornes` : 'nominal', 'pro_possession', 'pro_location'.

    Les deux jeux extremes ne sont PAS obtenus en prenant tous les minimums : il faut
    savoir, parametre par parametre, dans quel sens il pousse. Un amortissement PLUS
    LONG baisse la charge annuelle et favorise la possession ; un prix de location plus
    HAUT la favorise aussi. Prendre les bornes au hasard donnait un intervalle qui ne
    bornait rien.
    """
    m = d["materiel_engins"]
    sens = {  # (objet, +1 si une valeur haute favorise la POSSESSION, 0 si ambigu)
        "achat": (fam["prix_achat_MAD"], -1),
        "amort": (fam["amortissement_ans"], +1),
        "entretien": (fam["entretien_pct_achat_an"], -1),
        "financier": (m["cout_financier_pct_an"], -1),
        "residuelle": (m["valeur_residuelle_pct"], +1),
        "carburant": (fam["carburant_l_h"], -1),
        "gasoil": (m["gasoil_MAD_l"], -1),
        "conducteur": (m["conducteur_MAD_h"], 0),
        "prix_loc": (_prix_de_location(d, fam), +1),
    }
    out = {}
    for cle, (o, s) in sens.items():
        lo, hi = _b(o)
        out[cle] = (_v(o) if bornes == "nominal" or s == 0
                    else (hi if s > 0 else lo) if bornes == "pro_possession"
                    else (lo if s > 0 else hi))
    out["_operateur_compris"] = bool(fam["location"]["operateur_compris"])
    out["_regime_loc"] = fam["regime_de_location"]
    return out


def _objets_tirables(d: dict, fam: dict) -> dict:
    m = d["materiel_engins"]
    o = {"achat": fam["prix_achat_MAD"], "amort": fam["amortissement_ans"],
         "entretien": fam["entretien_pct_achat_an"],
         "financier": m["cout_financier_pct_an"],
         "residuelle": m["valeur_residuelle_pct"], "carburant": fam["carburant_l_h"],
         "gasoil": m["gasoil_MAD_l"], "conducteur": m["conducteur_MAD_h"],
         "prix_loc": _prix_de_location(d, fam)}
    if fam["regime_de_service"] == "continu":
        o["hpjs"] = fam["heures_par_jour_servi"]
    return o


def part_des_tirages(d: dict, fam: dict, emp: dict, tirages: int, graine: int,
                     facteur_emploi: float = 1.0) -> float:
    """Part des tirages uniformes dans les fourchettes ou la possession est moins chere.

    Les parametres sont tires INDEPENDAMMENT, et c'est une hypothese declaree : si le
    prix d'achat et le prix de location montaient ensemble (meme marche, meme annee),
    la dispersion serait plus faible et le verdict plus net. La part publiee est donc
    une borne prudente.

    `hpjs` est tire avec les autres pour les engins a service continu, parce qu'il
    deplace l'emploi ET le cout variable : l'ignorer donnait une dispersion trop
    etroite. `facteur_emploi` sert a la mutualisation, qui multiplie l'emploi sans
    toucher aux couts fixes.
    """
    objets = _objets_tirables(d, fam)
    rng = random.Random(graine)
    gagne = 0
    for _ in range(tirages):
        par = {k: rng.uniform(*_b(o)) for k, o in objets.items()}
        par["_operateur_compris"] = bool(fam["location"]["operateur_compris"])
        par["_regime_loc"] = fam["regime_de_location"]
        h, uf = emploi_pour(fam, emp, par.get("hpjs"), facteur_emploi)
        if couts_annuels(par, h, uf)["ecart_MAD_an"] < 0:
            gagne += 1
    return gagne / tirages * 100


# ------------------------------------------------------- 2. le taux d'emploi, lu au planning
def emploi(fam: dict, pl: dict, jours_ouvres_par_an: float, prix: dict, d: dict,
           tp: dict, go: dict) -> dict:
    """Jours de travail, fenetre de presence, heures et unites facturees.

    Tout est LU : les taches servies donnent leurs segments de travail et leur
    enveloppe. Pour un engin a service continu, les heures viennent d'une intensite
    declaree ; pour un engin a service par intervention, elles sont entierement
    deduites — nombre d'interventions = volume pompe du bordereau de D1 / volume d'un
    coulage de zone (module TV), duree d'une intervention = duree d'un coulage
    (module C3). Rien n'est redeclare.

    Attention a ce qui N'EST PAS un contre-calcul : la somme des segments de travail
    vaut la duree declaree PAR CONSTRUCTION dans le modele de D2 (une consignation
    decoupe le travail, elle ne l'etire pas). Ce que les segments apportent, c'est
    l'ETALEMENT, et il se lit dans la fenetre.
    """
    seg, dur = pl["segments_de_travail"], pl["durees"]
    taches = [t for t in fam["taches"] if t in seg]
    manquantes = [t for t in fam["taches"] if t not in seg]
    jours_seg = sum(b - a for t in taches for a, b in seg[t])
    jours_dur = sum(dur[t]["duree_j"] for t in taches)
    debut = min(a for t in taches for a, b in seg[t])
    fin = max(b for t in taches for a, b in seg[t])
    fenetre = fin - debut
    fenetre_ans = fenetre / jours_ouvres_par_an
    out = {
        "regime_de_service": fam["regime_de_service"],
        "regime_de_location": fam["regime_de_location"],
        "taches": taches, "taches_absentes_du_planning": manquantes,
        "jours_de_travail_voie_segments_j": round(jours_seg, 2),
        "jours_de_travail_voie_durees_j": round(jours_dur, 2),
        "ecart_des_deux_voies_j": round(jours_seg - jours_dur, 2),
        "_les_deux_voies_ne_sont_pas_independantes": (
            "Nul par construction : une consignation découpe le travail sans l'étirer. "
            "Ce n'est donc pas un contre-calcul, c'est un contrôle de non-régression du "
            "modèle de D2 — il n'attrapera qu'une faute de lecture des segments."),
        "jours_de_travail_j": round(jours_seg, 2),
        "fenetre_j": [round(debut, 2), round(fin, 2)],
        "fenetre_duree_j": round(fenetre, 2),
        "fenetre_ans": round(fenetre_ans, 3),
        "_fenetre_ans_exact": fenetre_ans,
        "taux_de_presence_utile_pct": round(jours_seg / fenetre * 100, 1),
        "jours_de_presence_sans_travail_j": round(fenetre - jours_seg, 1),
    }
    if fam["regime_de_service"] == "intervention":
        # volume pompe du bordereau de D1, lu et non redeclare : la somme des jours de
        # pompe des sous-details, divisee par le coefficient jours/m3 de D1.
        jours_pompe_D1 = sum(m["quantite"] * p["quantite"]
                             for p in prix["bordereau"]["postes"]
                             for m in (p.get("materiel") or [])
                             if m["ressource"] == fam["location"]["cle_prix"])
        coef = _v(d["prix_unitaires_MAD"]["coefficients_sous_detail"]["pompe_j_par_m3"])
        volume = jours_pompe_D1 / coef
        vol_zone = tp["quantites"]["beton_m3"]
        duree_une = go["fenetre_de_coulage"]["duree_du_coulage_h"]
        n = math.ceil(volume / vol_zone)
        out.update({
            "volume_pompe_du_bordereau_m3": round(volume, 1),
            "volume_d_un_coulage_m3": vol_zone,
            "interventions": n,
            "duree_d_une_intervention_h": duree_une,
            "heures_de_travail_h": round(n * duree_une, 1),
            "unites_facturees": n,
            "unite_de_facturation": "interventions",
            "jours_pompe_au_bordereau_de_D1_j": round(jours_pompe_D1, 2),
        })
    else:
        hpjs = _v(fam["heures_par_jour_servi"])
        out.update({
            "heures_par_jour_servi_h": hpjs,
            "heures_de_travail_h": round(jours_seg * hpjs, 1),
        })
        if fam["regime_de_location"] == "par_heure_de_service":
            out.update({"unites_facturees": round(jours_seg * hpjs, 1),
                        "unite_de_facturation": "heures de service"})
        else:
            # paye du premier au dernier jour de besoin, jours d'attente compris
            out.update({"unites_facturees": round(fenetre, 2),
                        "unite_de_facturation": "jours de présence"})
    h, uf = emploi_pour(fam, out, out.get("heures_par_jour_servi_h"))
    out["heures_par_an_h"] = round(h, 1)
    out["unites_facturees_par_an"] = round(uf, 1)
    out["_heures_par_an_exact"] = h
    out["_unites_par_an_exact"] = uf
    return out


def emploi_pour(fam: dict, emp: dict, hpjs: float | None,
                facteur: float = 1.0) -> tuple[float, float]:
    """Heures par an et unites facturees par an, pour un `hpjs` eventuellement tire.

    Le facteur multiplie l'emploi — c'est la mutualisation — sans toucher aux couts
    fixes, qui ne dependent pas de l'emploi. Un engin paye a la PRESENCE est le seul
    dont les unites facturees ne suivent pas le facteur : ajouter un second site ne
    rallonge pas la fenetre, il la remplit.
    """
    ans = emp["_fenetre_ans_exact"]
    if fam["regime_de_service"] == "intervention":
        h = emp["interventions"] * emp["duree_d_une_intervention_h"] * facteur / ans
        return h, emp["interventions"] * facteur / ans
    heures = emp["jours_de_travail_j"] * hpjs * facteur
    if fam["regime_de_location"] == "par_heure_de_service":
        return heures / ans, heures / ans
    return heures / ans, emp["fenetre_duree_j"] / ans


# ----------------------------------------------------------- 3. point d'equilibre et verdict
def location_affine(par: dict, emp: dict) -> tuple[float, float]:
    """La location annuelle est AFFINE en heures de travail : loc(h) = L0 + L1.h.

    Et c'est tout l'enjeu du module, parce que L0 n'est nul que dans deux des trois
    regimes :

    * **par heure de service** : L0 = 0, L1 = le prix horaire ;
    * **par intervention** : L0 = 0, L1 = prix / duree d'une intervention — les heures
      et les venues sont proportionnelles ;
    * **par duree de presence** : L1 = 0 (hors conducteur) et **L0 = toute la facture**.
      Travailler une heure de plus ne coute rien au locataire.

    Le conducteur non compris s'ajoute a L1 dans les trois cas : il se paie a l'heure
    travaillee, quel que soit le regime de l'engin.
    """
    reg = par["_regime_loc"]
    if reg == "par_heure_de_service":
        L0, L1 = 0.0, par["prix_loc"]
    elif reg == "par_intervention":
        L0, L1 = 0.0, par["prix_loc"] / emp["duree_d_une_intervention_h"]
    elif reg == "par_duree_de_presence":
        L0, L1 = emp["_unites_par_an_exact"] * par["prix_loc"], 0.0
    else:
        raise ValueError(f"regime de location inconnu : {reg}")
    if not par["_operateur_compris"]:
        L1 += par["conducteur"]
    return L0, L1


def point_d_equilibre(par: dict, emp: dict, heures_par_an: float) -> dict:
    """Le seuil d'emploi qui separe les deux decisions — ET DE QUEL COTE.

    L'ecart annuel est une DROITE en heures de travail :

        ecart(h) = (F - L0) + (v - L1).h

    d'ou un seuil h0 = (L0 - F) / (v - L1), et un SENS qui depend du signe de v - L1,
    c'est-a-dire de qui des deux a le cout marginal le plus eleve.

    * v < L1 : la possession coute moins cher a l'heure marginale. Elle gagne
      AU-DESSUS du seuil. C'est le cas classique, celui des manuels, et celui des
      regimes ou la location est proportionnelle aux heures.
    * v > L1 : la location est devenue un cout FIXE — regime « par duree de presence »,
      ou l'on paie le calendrier. La possession gagne alors AU-DESSOUS du seuil, et
      l'enonce des manuels s'inverse. Un engin peu employe mais loue a la presence se
      possede, et c'est contre-intuitif.

    La version precedente de cette fonction calculait h* = F / (loc_par_heure - v) avec
    loc_par_heure prise AU POINT DE FONCTIONNEMENT. C'est exact quand L0 = 0 et faux
    sinon — et le faux ne se voyait pas, parce que les deux formules coincident sur deux
    des trois regimes. Ce qui l'a vu : la figure 1, qui evalue les deux couts
    directement et ne croisait pas zero la ou le seuil l'annoncait. Une figure est une
    execution directe du modele : elle le controle (D-067).
    """
    c = couts_annuels(par, heures_par_an, _unites(par, emp, heures_par_an))
    L0, L1 = location_affine(par, emp)
    v = c["variable_MAD_h"]
    A, pente = c["fixe_MAD_an"] - L0, v - L1
    h0 = -A / pente if abs(pente) > 1e-12 else None
    return {
        "location_fixe_L0_MAD_an": round(L0),
        "location_marginale_L1_MAD_h": round(L1, 1),
        "variable_MAD_h": round(v, 1),
        "pente_de_l_ecart_MAD_h": round(pente, 1),
        "ecart_a_emploi_nul_MAD_an": round(A),
        "seuil_h_par_an": round(h0, 1) if h0 and h0 > 0 else None,
        "sens": ("possession gagne AU-DESSUS du seuil" if pente < 0
                 else "possession gagne AU-DESSOUS du seuil"),
        "cas_classique": bool(pente < 0),
        "location_MAD_h_de_travail": round(c["location_MAD_an"] / heures_par_an, 1),
    }


def _unites(par: dict, emp: dict, heures_par_an: float) -> float:
    """Unites facturees pour un nombre d'heures donne, par la forme affine.

    Elle doit redonner exactement l'emploi publie au point de fonctionnement, et un
    test le verifie : c'est le seul lien entre la forme affine et la lecture du
    planning.
    """
    reg = par["_regime_loc"]
    if reg == "par_heure_de_service":
        return heures_par_an
    if reg == "par_intervention":
        return heures_par_an / emp["duree_d_une_intervention_h"]
    return emp["_unites_par_an_exact"]


def verdict(d: dict, fam: dict, emp: dict, tirages: int = 20000,
            graine: int = 20261030) -> dict:
    """Possession ou location, avec le DEGRE de certitude que les fourchettes autorisent.

    Trois voies : (a) forme fermee au nominal ; (b) les deux combinaisons extremes de
    parametres ; (c) tirage uniforme dans les fourchettes.

    C'est (c) qui tranche, et non (b). Neuf ou dix parametres declares pris
    SIMULTANEMENT a leur borne favorable ne decrivent aucun chantier : le coin extreme
    encadre toujours le seuil, et s'en servir comme critere refuserait de trancher meme
    quand 999 tirages sur 1 000 vont dans le meme sens. D-059 disait qu'une voie dont
    les bornes encadrent le seuil ne tranche pas ; il manquait qu'un coin de dimension
    dix n'est pas une borne, c'est une combinaison de probabilite nulle.
    """
    h, uf = emp["_heures_par_an_exact"], emp["_unites_par_an_exact"]
    n = parametres(d, fam, "nominal")
    cn = couts_annuels(n, h, uf)
    cpp = couts_annuels(parametres(d, fam, "pro_possession"), h, uf)
    cpl = couts_annuels(parametres(d, fam, "pro_location"), h, uf)
    eq = point_d_equilibre(n, emp, h)
    joa = _v(d["materiel_engins"]["jours_ouvres_par_an"])
    # Plafond d'emploi A CETTE INTENSITE : les jours ouvres de l'annee multiplies par
    # les heures par unite de service. Ce n'est PAS un plafond physique — une pompe peut
    # pomper huit heures d'affilee — c'est le plafond a l'intensite de ce chantier. Le
    # dire autrement serait une phrase fausse a cote d'un nombre juste.
    par_jour = (emp["duree_d_une_intervention_h"]
                if fam["regime_de_service"] == "intervention"
                else emp["heures_par_jour_servi_h"])
    hmax = joa * par_jour
    part = part_des_tirages(d, fam, emp, tirages, graine)
    return {
        "nom": fam["nom"], "cle": fam["cle"],
        "regime_de_service": fam["regime_de_service"],
        "regime_de_location": fam["regime_de_location"],
        "unite_de_facturation": emp["unite_de_facturation"],
        "heures_par_an_h": round(h, 1),
        "unites_facturees_par_an": round(uf, 1),
        "fixe_MAD_an": round(cn["fixe_MAD_an"]),
        "amortissement_MAD_an": round(cn["amortissement_MAD_an"]),
        "entretien_MAD_an": round(cn["entretien_MAD_an"]),
        "cout_financier_MAD_an": round(cn["cout_financier_MAD_an"]),
        "variable_MAD_h": round(cn["variable_MAD_h"], 1),
        "possession_MAD_an": round(cn["possession_MAD_an"]),
        "location_MAD_an": round(cn["location_MAD_an"]),
        "ecart_MAD_an": round(cn["ecart_MAD_an"]),
        "possession_MAD_h": round(cn["possession_MAD_an"] / h, 1),
        "location_MAD_h": round(cn["location_MAD_an"] / h, 1),
        "equilibre": eq,
        "cote_du_seuil": ("au-dessus" if eq["seuil_h_par_an"] and h > eq["seuil_h_par_an"]
                          else "au-dessous" if eq["seuil_h_par_an"] else None),
        "ecart_pro_possession_MAD_an": round(cpp["ecart_MAD_an"]),
        "ecart_pro_location_MAD_an": round(cpl["ecart_MAD_an"]),
        "bornes_tranchent": bool((cpp["ecart_MAD_an"] < 0) == (cpl["ecart_MAD_an"] < 0)),
        "part_des_tirages_pro_possession_pct": round(part, 1),
        "nb_tirages": tirages,
        "nb_parametres_tires": len(_objets_tirables(d, fam)),
        "seuil_de_verdict_pct": SEUIL_VERDICT_PCT,
        "verdict": ("POSSÉDER" if part >= 100 - SEUIL_VERDICT_PCT
                    else "LOUER" if part <= SEUIL_VERDICT_PCT else "NON TRANCHÉ"),
        "verdict_nominal": "posseder" if cn["ecart_MAD_an"] < 0 else "louer",
        "jours_ouvres_par_an_j": joa,
        "heures_max_a_cette_intensite_h": round(hmax, 1),
        # Si le seuil est au-dela du plafond d'emploi, la question est CLOSE sans
        # aucune estimation : un seul des deux cotes du seuil est atteignable. Le camp
        # qui gagne depend alors du sens, et non du seuil.
        "seuil_hors_d_atteinte": bool(eq["seuil_h_par_an"] is None
                                      or eq["seuil_h_par_an"] > hmax),
        "conclusion_sans_estimation": (
            None if eq["seuil_h_par_an"] is not None and eq["seuil_h_par_an"] <= hmax
            else "LOUER quel que soit l'emploi" if eq["cas_classique"]
            else "POSSÉDER quel que soit l'emploi"),
        "_coin_extreme": (
            "Les deux écarts « pro_ » sont les COINS du domaine : tous les paramètres "
            "pris ensemble à leur borne la plus favorable. Un coin de cette dimension "
            "n'est pas un scénario, et quand les deux coins encadrent le seuil ils ne "
            "disent rien — c'est alors la part des tirages qui tranche. Mais quand les "
            "DEUX coins donnent le même verdict, comme ici pour la pompe, il n'y a plus "
            "de question : aucune combinaison de ces fourchettes ne peut l'inverser, et "
            "c'est la preuve la plus forte que ce module sache produire. "
            + ("Les deux coins concordent pour cet engin."
               if (cpp["ecart_MAD_an"] < 0) == (cpl["ecart_MAD_an"] < 0)
               else "Ils encadrent le seuil pour cet engin.")),
    }


# ------------------------------------------------------------ 4. le parc, jour apres jour
def profil_du_parc(d: dict, pl: dict) -> dict:
    """Presence et travail de chaque famille, jour par jour.

    La presence est la FENETRE (du premier au dernier jour de besoin) ; le travail est
    l'union des segments des taches servies. L'ecart entre les deux courbes est le taux
    d'emploi du parc, vu a l'oeil — et c'est la regle que la passe de C1 a proposee
    sans que personne l'outille : toute ressource louee a la duree nomme sa fenetre
    d'emploi.
    """
    seg = pl["segments_de_travail"]
    fams = d["materiel_engins"]["familles"]
    jmax = math.ceil(max(b for s in seg.values() for a, b in s))
    presents, travail, detail = [], [], []
    for fam in fams:
        taches = [t for t in fam["taches"] if t in seg]
        debut = min(a for t in taches for a, b in seg[t])
        fin = max(b for t in taches for a, b in seg[t])
        actifs = set()
        for t in taches:
            for a, b in seg[t]:
                actifs.update(range(int(math.floor(a)), int(math.ceil(b))))
        detail.append({"cle": fam["cle"], "nom": fam["nom"],
                       "debut_j": round(debut, 1), "fin_j": round(fin, 1),
                       # La presence se discretise COMME le travail : par les jours
                       # entiers que la fenetre touche. Discretiser les deux autrement
                       # faisait travailler un engin le jour 19 alors que sa fenetre
                       # commencait au jour 19,86, et la courbe du travail sortait
                       # au-dessus de celle de la presence.
                       "premier_jour": int(math.floor(debut)),
                       "dernier_jour": int(math.ceil(fin)) - 1,
                       "jours_actifs": actifs})
    for j in range(jmax + 1):
        presents.append(sum(1 for f in detail
                            if f["premier_jour"] <= j <= f["dernier_jour"]))
        travail.append(sum(1 for f in detail if j in f["jours_actifs"]))
    aire_p, aire_t = sum(presents), sum(travail)

    def plages(jours: list) -> list:
        """Regroupe une liste de jours en intervalles consecutifs."""
        out = []
        for j in sorted(jours):
            if out and j == out[-1][1] + 1:
                out[-1][1] = j
            else:
                out.append([j, j])
        return out

    # Les trous de chaque famille : les jours de sa fenetre ou elle ne travaille pas.
    # Les ecrire a la main dans une legende serait un nombre technique tape au clavier.
    for f in detail:
        creux = [j for j in range(f["premier_jour"], f["dernier_jour"] + 1)
                 if j not in f["jours_actifs"]]
        pl_ = sorted(plages(creux), key=lambda x: x[1] - x[0], reverse=True)
        f["jours_sans_emploi"] = len(creux)
        f["plus_longs_trous_j"] = pl_[:3]
    tout = [j for j, n in enumerate(travail) if n == len(detail)]
    return {
        "jours": jmax + 1,
        "familles": [{k: v for k, v in f.items() if k != "jours_actifs"}
                     for f in detail],
        "engins_jours_de_presence": aire_p,
        "engins_jours_de_travail": aire_t,
        "taux_d_emploi_du_parc_pct": round(aire_t / aire_p * 100, 1),
        "pointe_presents": max(presents), "pointe_au_travail": max(travail),
        "jours_ou_tout_le_parc_travaille": len(tout),
        "plages_ou_tout_le_parc_travaille": plages(tout),
        "profil_presents": presents, "profil_travail": travail,
    }


# ------------------------------------------------- 5. ce que le parc coute, et ce qui manque
def cout_du_parc(d: dict, emplois: dict, verdicts: list, prix: dict) -> dict:
    """Le cout de location du parc sur la duree du chantier, ligne par ligne.

    Et la question que personne ne pose : le bordereau de D1 porte-t-il une ligne pour
    cet engin ? Quand la reponse est non, le montant n'est pas absent du prix de
    revient — il est absorbe par un poste de frais de duree qui n'a pas ete bati pour
    lui. On le compare donc a ce poste.
    """
    utilises = {m["ressource"] for p in prix["bordereau"]["postes"]
                for m in (p.get("materiel") or [])}
    lignes = []
    for v in verdicts:
        fam = next(f for f in d["materiel_engins"]["familles"] if f["cle"] == v["cle"])
        e = emplois[v["cle"]]
        cle = fam["location"].get("cle_prix")
        prix_u = _v(_prix_de_location(d, fam))
        cout = e["unites_facturees"] * prix_u
        if not fam["location"]["operateur_compris"]:
            cout += e["heures_de_travail_h"] * _v(d["materiel_engins"]["conducteur_MAD_h"])
        lignes.append({
            "cle": v["cle"], "nom": v["nom"],
            "unite_de_facturation": e["unite_de_facturation"],
            "unites_facturees": e["unites_facturees"],
            "prix_unitaire_MAD": prix_u,
            "heures_de_travail_h": e["heures_de_travail_h"],
            "cout_sur_le_chantier_MAD": round(cout),
            "cout_par_heure_de_travail_MAD": round(cout / e["heures_de_travail_h"], 1),
            "ligne_au_bordereau_de_D1": bool(cle and cle in utilises),
            "cle_de_prix": cle,
        })
    absentes = [l for l in lignes if not l["ligne_au_bordereau_de_D1"]]
    # LIMITE, publiee avec le nombre : un poste au FORFAIT peut porter la depense sans
    # la montrer. Le bordereau de D1 en compte plusieurs, et leur montant est
    # considerable. On ne peut donc pas affirmer que la depense manque au prix de
    # revient — seulement qu'elle n'est nulle part VISIBLE, ce qui suffit a ce qu'elle
    # ne soit suivie par personne.
    forfaits = [p for p in prix["bordereau"]["postes"] if p["type"] == "forfait"]
    divers = prix["bordereau"]["frais_de_duree"]["lignes"]["energie_et_divers"]
    manque = sum(l["cout_sur_le_chantier_MAD"] for l in absentes)
    # La pompe : deux voies INDEPENDANTES pour le meme engin. D1 compte des jours de
    # pompe au VOLUME de beton ; C6 compte des INTERVENTIONS au nombre de coulages. Les
    # deux repondent a la meme question et ne donnent pas le meme nombre.
    ep = emplois["pompe"]
    jours_D1 = ep["jours_pompe_au_bordereau_de_D1_j"]
    prix_pompe = _v(_prix_de_location(
        d, next(f for f in d["materiel_engins"]["familles"] if f["cle"] == "pompe")))
    cher = max(lignes, key=lambda l: l["cout_par_heure_de_travail_MAD"])
    bon = min(lignes, key=lambda l: l["cout_par_heure_de_travail_MAD"])
    return {
        "lignes": lignes,
        "total_sur_le_chantier_MAD": round(sum(l["cout_sur_le_chantier_MAD"]
                                               for l in lignes)),
        "le_plus_cher_par_heure": cher["nom"],
        "le_moins_cher_par_heure": bon["nom"],
        "rapport_du_plus_cher_au_moins_cher": round(
            cher["cout_par_heure_de_travail_MAD"]
            / bon["cout_par_heure_de_travail_MAD"], 2),
        "lignes_absentes_du_bordereau": [l["nom"] for l in absentes],
        "montant_absent_du_bordereau_MAD": round(manque),
        "poste_qui_devrait_l_absorber": "« énergie et divers » des frais de durée (D1)",
        "montant_de_ce_poste_MAD": divers["montant_MAD"],
        "part_du_poste_consommee_pct": round(manque / divers["montant_MAD"] * 100, 1),
        "nb_postes_au_forfait": len(forfaits),
        "montant_des_postes_au_forfait_MAD": round(
            sum(p["debourse_sec_total_MAD"] for p in forfaits)),
        "_limite": (
            f"Le bordereau de D1 compte {len(forfaits)} postes au FORFAIT, pour "
            f"{_f(sum(p['debourse_sec_total_MAD'] for p in forfaits) / 1e6, 1)} millions de "
            "MAD de déboursé sec. Un forfait peut porter cette dépense sans la montrer : "
            "on ne peut donc pas affirmer qu'elle manque au prix de revient, seulement "
            "qu'elle n'est nulle part VISIBLE. C'est déjà un résultat — une dépense "
            "invisible dans un forfait n'est suivie par personne, et c'est de ce "
            "suivi-là que ce cours parle."),
        "pompe_deux_voies": {
            "voie_D1_au_volume_j": jours_D1,
            "voie_C6_aux_interventions_j": ep["interventions"],
            "rapport": round(ep["interventions"] / jours_D1, 2),
            "ecart_MAD": round((ep["interventions"] - jours_D1) * prix_pompe),
            "pourquoi": (
                "D1 compte un jour de pompe par volume pompé — un jour pour "
                f"{_f(1 / _v(d['prix_unitaires_MAD']['coefficients_sous_detail']['pompe_j_par_m3']), 0)} m³. "
                "C'est juste si la pompe est chargée à plein à chaque venue. Elle ne "
                f"l'est pas : un coulage de zone fait "
                f"{_f(ep['volume_d_un_coulage_m3'], 1)} m³ et dure "
                f"{_f(ep['duree_d_une_intervention_h'], 2)} h, et il se paie une "
                "journée d'intervention entière. Le pompage se facture à la VENUE, pas "
                "au mètre cube."),
        },
    }


# ------------------------------------------------------- 6. du catalogue au debit reel
def rendement_de_la_pompe(d: dict, go: dict) -> dict:
    """Le debit catalogue, facteur par facteur, jusqu'au debit pratique.

    Le resultat se compare a la valeur que le module C3 declare : c'est un
    contre-calcul au sens du § 3.3, par une voie qui ne partage avec elle aucune
    hypothese. L'ecart tolere est de 5 %.
    """
    r = d["materiel_engins"]["rendement_de_la_pompe"]
    cat = _v(r["debit_catalogue_m3_h"])
    etapes, courant = [{"etape": "Debit catalogue", "facteur": None,
                        "debit_m3_h": round(cat, 1)}], cat
    for cle, libelle in (("facteur_pompabilite", "Beton reel, tuyauterie"),
                         ("part_de_l_heure_pompee", "Heure reellement pompee"),
                         ("facteur_arrets", "Nettoyages et arrets")):
        f = _v(r[cle])
        courant *= f
        etapes.append({"etape": libelle, "facteur": f, "debit_m3_h": round(courant, 1)})
    produit = courant / cat
    o = d["gros_oeuvre"]["betonnage_temps_chaud"]["debit_pompe_m3_h"]
    declare, (lo, hi) = _v(o), _b(o)
    ecart_pct = (courant - declare) / declare * 100
    return {
        "etapes": etapes, "debit_catalogue_m3_h": round(cat, 1),
        "produit_des_facteurs": round(produit, 3),
        "debit_recalcule_m3_h": round(courant, 1),
        "debit_declare_par_C3_m3_h": declare,
        "fourchette_declaree_par_C3": [lo, hi],
        "dans_la_fourchette": bool(lo <= courant <= hi),
        "ecart_pct": round(ecart_pct, 1),
        "ecart_sous_tolerance_5pct": bool(abs(ecart_pct) <= 5),
        "plancher_anti_reprise_m3_h": go["betonnage"]["debit_dimensionnant_m3_h"],
        "debit_tenu_au_chantier_m3_h": go["betonnage"]["option_retenue"]["debit_tenu_m3_h"],
        "ce_qui_borne_le_coulage": go["betonnage"]["ce_qui_borne"],
        "perte_catalogue_pct": round((1 - produit) * 100, 1),
        "lecture": (
            f"Le prospectus annonce {_f(cat, 0)} m³/h ; la chaîne des facteurs en laisse "
            f"{_f(courant, 1)}, soit {_f((1 - produit) * 100, 0)} % de moins. Le module C3 "
            f"déclare {_f(declare, 0)} m³/h par une autre voie : l'écart est de "
            f"{_f(abs(ecart_pct), 1)} %. Et sur le chantier le coulage tient "
            f"{_f(go['betonnage']['option_retenue']['debit_tenu_m3_h'], 1)} m³/h, borné "
            f"par {go['betonnage']['ce_qui_borne']} : l'engin n'est jamais la contrainte."),
    }


# ----------------------------------------------------------- 7. la chaine et son secours
def chaine_du_coulage(d: dict, prix: dict, go_cycle: dict, tirages: int = 50000,
                      graine: int = 20261031) -> dict:
    """Disponibilite d'une chaine : forme fermee (produit) et SIMULATION directe.

    La forme fermee est un produit de probabilites independantes. La simulation tire
    chaque maillon et compte les matinees ou les quatre repondent : c'est la voie que
    D-067 impose, parce qu'une formule homogene peut etre fausse et qu'aucun test
    comparant la sortie a la formule ne le verrait.
    """
    maillons = d["materiel_engins"]["chaine_du_coulage"]["maillons"]
    ps = [_v(m["disponibilite_pct"]) / 100 for m in maillons]
    produit = math.prod(ps)
    rng = random.Random(graine)
    ok = sum(1 for _ in range(tirages) if all(rng.random() < p for p in ps))
    simulee = ok / tirages
    jour_perdu = prix["cout_du_retard"]["1"]["frais_de_duree_MAD"]
    secours = []
    for i, m in enumerate(maillons):
        if not m["secours_possible"]:
            secours.append({"element": m["element"], "possible": False,
                            "pourquoi": m["_secours"]})
            continue
        c = m["cout_du_secours_MAD_j"]
        prix_j = (_v(d["prix_unitaires_MAD"]["ressources"]["materiel_MAD"][c["cle_prix"]])
                  if "cle_prix" in c else _v(c))
        p2 = list(ps)
        p2[i] = 1 - (1 - ps[i]) ** 2
        nouveau = math.prod(p2)
        gain = nouveau - produit
        secours.append({
            "element": m["element"], "possible": True,
            "disponibilite_pct": round(ps[i] * 100, 1),
            "avec_secours_pct": round(p2[i] * 100, 2),
            "chaine_avec_secours_pct": round(nouveau * 100, 1),
            "gain_en_points_de_chaine": round(gain * 100, 2),
            "cout_du_secours_MAD_j": prix_j,
            "esperance_de_gain_MAD_j": round(gain * jour_perdu, 1),
            "rentable": bool(gain * jour_perdu > prix_j),
            "rapport_gain_sur_cout": round(gain * jour_perdu / prix_j, 2),
            "MAD_par_point_de_chaine": round(prix_j / (gain * 100), 1),
        })
    zones = go_cycle["nb_zones"]
    doublables = [s for s in secours if s["possible"]]
    meilleur = max(doublables, key=lambda s: s["rapport_gain_sur_cout"])
    plus_gros_gain = max(doublables, key=lambda s: s["gain_en_points_de_chaine"])
    return {
        "maillons": [{"element": m["element"],
                      "disponibilite_pct": _v(m["disponibilite_pct"])} for m in maillons],
        "nb_maillons": len(ps),
        "maillon_le_plus_faible_pct": round(min(ps) * 100, 1),
        "disponibilite_forme_fermee_pct": round(produit * 100, 1),
        "disponibilite_simulee_pct": round(simulee * 100, 1),
        "ecart_des_deux_voies_points": round(abs(produit - simulee) * 100, 2),
        "nb_tirages": tirages,
        "ecart_avec_le_maillon_le_plus_faible_points": round((min(ps) - produit) * 100, 1),
        "coulages_derangeables_sur": zones,
        "coulages_derangeables": round((1 - produit) * zones, 1),
        "cout_d_un_jour_perdu_MAD": jour_perdu,
        "perimetre_du_jour_perdu": (
            "Frais de durée seuls, lus dans D1 (cout_du_retard). Les pénalités ne "
            "s'ajoutent que si la fin de chantier dépasse la date contractuelle : c'est "
            "un autre périmètre, et le confondre avec celui-ci multiplierait le coût "
            "par huit."),
        "secours": secours,
        "secours_le_plus_rentable": meilleur["element"],
        "secours_au_plus_gros_gain": plus_gros_gain["element"],
        "le_plus_rentable_n_est_pas_le_plus_gros_gain": bool(
            meilleur["element"] != plus_gros_gain["element"]),
        "lecture": (
            f"Quatre maillons dont le plus faible est à {_f(min(ps) * 100, 0)} % : la "
            f"chaîne répond {_f(produit * 100, 1)} % des matinées, pas "
            f"{_f(min(ps) * 100, 0)} %. Sur {zones} coulages de zone, "
            f"{_f((1 - produit) * zones, 1)} sont dérangés."),
    }


# ------------------------------------------------------------------- 8. mutualiser
def mutualisation(d: dict, emplois: dict, verdicts: list) -> dict:
    """Le meme engin sur deux sites : les heures s'additionnent, les fixes non.

    C'est la reponse a la question que les verdicts laissent ouverte : si la location
    gagne, comment le loueur gagne-t-il de l'argent ? Il mutualise. Un chef de projet
    suivi multi-sites (D7) est dans la meme position que lui — et le calcul dit sur
    quels engins cela change quelque chose, et sur lesquels cela n'en change aucun.
    """
    mu = d["materiel_engins"]["mutualisation"]
    k, perte = _v(mu["besoin_relatif_du_second_site"]), _v(
        mu["perte_de_mutualisation_pct"]) / 100
    facteur = (1 + k) * (1 - perte)
    lignes = []
    for v in verdicts:
        fam = next(f for f in d["materiel_engins"]["familles"] if f["cle"] == v["cle"])
        e = emplois[v["cle"]]
        par = parametres(d, fam, "nominal")
        h, uf = emploi_pour(fam, e, e.get("heures_par_jour_servi_h"), facteur)
        c = couts_annuels(par, h, uf)
        h_eq = v["equilibre"]["seuil_h_par_an"]
        part = part_des_tirages(d, fam, e, 20000, 20261101, facteur)
        lignes.append({
            "cle": v["cle"], "nom": v["nom"],
            "heures_par_an_seul_h": v["heures_par_an_h"],
            "heures_par_an_mutualisees_h": round(h, 1),
            "seuil_h_par_an": h_eq,
            "sens": v["equilibre"]["sens"],
            "sites_equivalents_pour_atteindre_le_seuil": round(
                h_eq / v["heures_par_an_h"], 2) if h_eq else None,
            # Ce que ce nombre de sites SIGNIFIE depend du sens du seuil, et l'ecrire
            # une fois pour toutes evite la phrase fausse a cote du nombre juste : pour
            # un engin dont la possession gagne AU-DESSOUS du seuil, atteindre le seuil
            # ne serait pas une bonne nouvelle, ce serait perdre l'avantage.
            "ce_que_le_seuil_signifie": (
                "nombre de sites qu'il faudrait regrouper pour que la POSSESSION "
                "devienne avantageuse" if v["equilibre"]["cas_classique"]
                else "nombre de sites au-dela duquel la possession CESSERAIT d'etre "
                     "avantageuse"),
            "part_du_seuil_atteinte_pct": round(h / h_eq * 100, 1) if h_eq else None,
            "ecart_seul_MAD_an": v["ecart_MAD_an"],
            "ecart_mutualise_MAD_an": round(c["ecart_MAD_an"]),
            "part_des_tirages_pro_possession_pct": round(part, 1),
            "verdict_seul": v["verdict"],
            "verdict_mutualise": ("POSSÉDER" if part >= 100 - SEUIL_VERDICT_PCT
                                  else "LOUER" if part <= SEUIL_VERDICT_PCT
                                  else "NON TRANCHÉ"),
            # Resultat contre-intuitif, et il tient au regime de location : un engin
            # paye a la PRESENCE voit sa facture inchangee quand on le mutualise (la
            # fenetre est deja payee en entier) tandis que la possession paie chaque
            # heure de plus en carburant et en conducteur. Mutualiser un engin de ce
            # regime DEGRADE donc l'argument de la possession, au lieu de le renforcer.
            "la_mutualisation_degrade_la_possession": bool(
                c["ecart_MAD_an"] > v["ecart_MAD_an"]),
        })
    presence = [l for l in lignes if l["la_mutualisation_degrade_la_possession"]]
    return {
        "besoin_relatif_du_second_site": k,
        "_hypothese_de_fenetre": (
            "Mutualiser suppose ici que le travail du second site tient dans la MÊME "
            "fenêtre de présence : on remplit une fenêtre déjà payée, on ne la rallonge "
            "pas. C'est pourquoi un engin payé à la présence y perd — sa facture ne "
            "bouge pas, mais chaque heure de plus coûte du carburant et un conducteur à "
            "celui qui le possède. Pour le locataire, à l'inverse, remplir une fenêtre "
            "déjà payée est le meilleur coup du chantier."),
        "engins_dont_la_mutualisation_degrade_la_possession": [l["nom"]
                                                               for l in presence],
        "perte_de_mutualisation_pct": round(perte * 100, 1),
        "sites_equivalents_mutualises": round(facteur, 2),
        "facteur_d_emploi": round(facteur, 3),
        "lignes": lignes,
        "nb_bascules": sum(1 for l in lignes
                           if l["verdict_mutualise"] != l["verdict_seul"]),
        "lecture": (
            f"Deux sites font {_f(facteur, 2)} site équivalent, pertes de transfert "
            "déduites, et cela ne fait basculer aucun verdict. Les deux engins loués "
            "sont beaucoup trop loin de leur seuil : il faudrait "
            + " et ".join(
                f"{_f(l['sites_equivalents_pour_atteindre_le_seuil'], 1)} sites pour "
                f"{l['cle']}" for l in lignes
                if l["verdict_seul"] == "LOUER") +
            ". Et le troisième n'a rien à y gagner : le chariot est déjà du bon côté de "
            "son seuil, et mutualiser l'en rapproche au lieu de l'en éloigner — "
            f"{_f(next(l['part_du_seuil_atteinte_pct'] for l in lignes if l['cle'] == 'chariot'), 0)} % "
            "du seuil au lieu de "
            f"{_f(next(l['heures_par_an_seul_h'] / l['seuil_h_par_an'] * 100 for l in lignes if l['cle'] == 'chariot'), 0)} %. "
            "La mutualisation n'est pas un levier général : c'est le métier du loueur, "
            "qui regroupe des dizaines de sites, et c'est pour cela qu'il peut vendre "
            "l'heure moins cher que le coût de possession."),
    }


# --------------------------------------------------------------------------- figures
def figures(verdicts: list, emplois: dict, parc: dict, rend: dict, d: dict) -> dict:
    """Trois figures, et aucune n'est un doublon : C1 a dessine la courbe de charge de
    la grue, C3 l'optimum du parc de coffrage, D2 la demande de grue jour par jour.
    """
    # 1. ecart de cout annuel du chariot selon les heures travaillees par an : le zero
    #    de l'axe EST le prix de la location, et la courbe le croise a l'equilibre.
    fam = next(f for f in d["materiel_engins"]["familles"] if f["cle"] == "chariot")
    e = emplois["chariot"]
    par = parametres(d, fam, "nominal")
    v = next(x for x in verdicts if x["cle"] == "chariot")
    seuil = v["equilibre"]["seuil_h_par_an"]
    # On balaie jusqu'au-dela du seuil ET du plafond d'emploi, pour que la figure montre
    # le croisement et la part du domaine qui est hors d'atteinte.
    hmax_fig = max(seuil * 1.25, v["heures_max_a_cette_intensite_h"] * 1.1)
    pas = 25 * max(1, round(hmax_fig / 1200))
    pts = []
    h_ = pas
    while h_ <= hmax_fig:
        # l'emploi varie, la fenetre de presence ne varie pas : c'est tout le piege du
        # regime « par duree de presence »
        c = couts_annuels(par, h_, _unites(par, e, h_))
        pts.append({"x": h_, "v": round(c["ecart_MAD_an"] / 1000, 1)})
        h_ += pas
    f1 = {"points": pts,
          "marqueur": {"x": round(seuil),
                       "libelle": f"seuil {_f(seuil, 0)} h/an"},
          "plafond": v["heures_max_a_cette_intensite_h"],
          "emploi_reel": v["heures_par_an_h"]}
    f2 = [{"libelle": x["etape"], "valeur": x["debit_m3_h"]} for x in rend["etapes"]]
    return {"equilibre_chariot": f1, "rendement": f2,
            "parc_presents": [{"j": j, "n": n}
                              for j, n in enumerate(parc["profil_presents"])],
            "parc_travail": [{"j": j, "n": n}
                             for j, n in enumerate(parc["profil_travail"])]}


# ------------------------------------------------------------------------- assemblage
def tout_calculer(d: dict) -> dict:
    S = RACINE / "calc" / "sorties"
    def lire(n):
        return json.loads((S / n).read_text(encoding="utf-8"))
    pl, prix, go, tp = (lire("planification.json"), lire("prix.json"),
                        lire("gros-oeuvre.json"), lire("tranche-plancher.json"))
    joa = _v(d["materiel_engins"]["jours_ouvres_par_an"])
    emplois, verdicts = {}, []
    for fam in d["materiel_engins"]["familles"]:
        emplois[fam["cle"]] = emploi(fam, pl, joa, prix, d, tp, go)
    for fam in d["materiel_engins"]["familles"]:
        verdicts.append(verdict(d, fam, emplois[fam["cle"]]))
    parc = profil_du_parc(d, pl)
    rend = rendement_de_la_pompe(d, go)
    return {
        "emplois": emplois, "verdicts": verdicts, "parc": parc,
        "cout_du_parc": cout_du_parc(d, emplois, verdicts, prix),
        "rendement_de_la_pompe": rend,
        "chaine_du_coulage": chaine_du_coulage(d, prix, go["cycle"]),
        "mutualisation": mutualisation(d, emplois, verdicts),
        "figures": figures(verdicts, emplois, parc, rend, d),
    }


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    r = tout_calculer(d)
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "materiel.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for v in r["verdicts"]:
        e = v["equilibre"]
        print(f"  {v['nom'][:32]:<34} {v['unite_de_facturation'][:18]:<20} "
              f"{v['heures_par_an_h']:>7.1f} h/an · seuil "
              f"{e['seuil_h_par_an']} ({'au-dessus' if e['cas_classique'] else 'au-dessous'})"
              f" · {v['conclusion_sans_estimation'] or v['verdict']:<28} "
              f"({v['part_des_tirages_pro_possession_pct']} % des tirages)")
    p = r["parc"]
    print(f"parc : {p['engins_jours_de_travail']} engins-jours de travail sur "
          f"{p['engins_jours_de_presence']} de presence = {p['taux_d_emploi_du_parc_pct']} %")
    cp = r["cout_du_parc"]
    print(f"cout du parc : {cp['total_sur_le_chantier_MAD']:,} MAD · absent du bordereau : "
          f"{cp['montant_absent_du_bordereau_MAD']:,} MAD "
          f"({cp['part_du_poste_consommee_pct']} % du poste qui l'absorbe)")
    dv = cp["pompe_deux_voies"]
    print(f"pompe, deux voies : D1 compte {dv['voie_D1_au_volume_j']} j au volume, "
          f"C6 {dv['voie_C6_aux_interventions_j']} interventions — x{dv['rapport']}")
    rp = r["rendement_de_la_pompe"]
    print(f"rendement : catalogue {rp['debit_catalogue_m3_h']} -> "
          f"{rp['debit_recalcule_m3_h']} m3/h contre {rp['debit_declare_par_C3_m3_h']} "
          f"declare par C3 (ecart {rp['ecart_pct']} %)")
    c = r["chaine_du_coulage"]
    print(f"chaine : {c['disponibilite_forme_fermee_pct']} % (simulee "
          f"{c['disponibilite_simulee_pct']} %) contre {c['maillon_le_plus_faible_pct']} % "
          f"pour le maillon le plus faible · meilleur secours : "
          f"{c['secours_le_plus_rentable']}")
    print("mutualisation : " + " · ".join(
        f"{l['cle']} {l['verdict_seul']}->{l['verdict_mutualise']}"
        for l in r["mutualisation"]["lignes"]))
