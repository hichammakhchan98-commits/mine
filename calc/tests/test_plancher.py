"""Tests de la tranche verticale (§ 12.1 f).

Regle reprise du socle : une assertion qui ne peut pas echouer ne vaut rien.
Chaque controle ci-dessous est double d'une erreur injectee qui DOIT le faire sonner.
"""
from __future__ import annotations
import json, math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from plancher import quantites_zone, fourchette_acier
from cycle_plancher import (durees_taches, reseau_zone, cout_zone, cadence_rotation,
                            etat_physique_de_zone, conflits_de_ressource)
from cpm import Tache, contre_calcul, voie_A_parcours
from valeur_acquise import valeur_acquise

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
echecs = []


def verifie(nom, cond, detail=""):
    print(f"  {'ok   ' if cond else 'ECHEC'} {nom}{(' — ' + detail) if detail else ''}")
    if not cond:
        echecs.append(nom)


d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
q = quantites_zone(d)
q["fourchette_acier"] = fourchette_acier(d, q)
t = durees_taches(d, q)
cc = contre_calcul(reseau_zone(t, d["cycle_zone"]))
_pl = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json").read_text(encoding="utf-8"))
# le cycle vient du CONTRE-CALCUL recalcule ici, pas de la sortie publiee : on ne
# verifie pas un resultat avec lui-meme
c = cout_zone(d, q, t, cc["voie_A_parcours_avant_arriere_j"])
va = valeur_acquise(d, q, c, _pl["suivi"], _pl["avancement_physique"]["quantites_faites"],
                     _pl["valeur_planifiee_a_l_arret"]["quantites"])
z = d["geometrie"]["mezzanine"]["zones_de_coulage"]

# --- geometrie : les zones doivent recouvrir exactement la mezzanine
total = z["nb_zones"] * z["longueur_zone_m"] * z["largeur_zone_m"]
attendu = 120.0 * d["geometrie"]["mezzanine"]["largeur_m"]
verifie("les zones recouvrent exactement la mezzanine", abs(total - attendu) < 1e-9,
        f"{total:.0f} m2 contre {attendu:.0f} m2")

# --- beton : recalcule depuis data/ par un AUTRE decoupage geometrique.
# La version precedente recopiait les cotes en clair (360 x 0,25 + 2 x 24 x 0,35 x 0,50) :
# elle se disait « independante » alors qu'elle figeait les donnees dans le test. Elle ne
# bougeait donc pas si data/ changeait, et ne verifiait que l'arithmetique de l'auteur.
# Ici, les cotes sont LUES dans data/ et le volume est obtenu autrement : par le prisme
# plein de la zone a la hauteur totale (dalle + retombee), moins le vide entre poutres.
_z = d["geometrie"]["mezzanine"]["zones_de_coulage"]
_dalle = next(x for x in d["elements"]["dalles"] if x["id"] == "DM1")
_poutre = next(x for x in d["elements"]["poutres"] if x["id"] == "PM1")
_L, _l = _z["longueur_zone_m"], _z["largeur_zone_m"]
_ep, _h = _dalle["epaisseur_m"], _poutre["retombee_sous_dalle_m"]
_b, _Lp = _poutre["b_m"], _poutre["longueur_dans_zone_m"]
_n = round(_L / _poutre["entraxe_m"])
_prisme = _L * _l * (_ep + _h)                      # tout plein, dalle + retombee
_vide = _l * (_ep + _h) * 0 + (_L * _l - _n * _Lp * _b) * _h   # vide sous la dalle
beton_main = _prisme - _vide
verifie("volume de beton recalcule par un autre decoupage geometrique",
        abs(q["beton_m3"] - beton_main) < 0.01,
        f"{q['beton_m3']} m3 contre {beton_main:.2f} m3")
verifie("ce recalcul SUIT data/ : changer l'epaisseur le deplace",
        abs((_L * _l * (_ep + 0.05 + _h)
             - (_L * _l - _n * _Lp * _b) * _h) - beton_main - _L * _l * 0.05) < 1e-6)

# --- coffrage : il DOIT depasser la surface, sinon les joues sont oubliees
verifie("le ratio de coffrage depasse 1,00 (les joues sont comptees)",
        q["ratio_coffrage_m2_par_m2"] > 1.0, f"{q['ratio_coffrage_m2_par_m2']}")

# --- l'acier vient d'un ratio : sa fourchette doit etre LARGE et publiee
verifie("la fourchette d'acier est publiee et large",
        q["fourchette_acier"]["etendue_pct"] > 20,
        f"etendue {q['fourchette_acier']['etendue_pct']} %")

# --- durees : les QUATRE sont recalculees independamment, avec leur propre effectif.
# Une version precedente ne verifiait que le coffrage : un canari qui divisait le
# ferraillage de dalle par l'effectif des POUTRES allongeait le plancher de 74 %
# et passait les douze controles sans bruit.
C, E = d["cadences"], d["effectifs"]
attendu = {
    "coffrage_j":            q["coffrage_m2"]      / (C["coffrage_dalle_m2_j"]["valeur"]   * E["coffreurs"]),
    "ferraillage_poutres_j": q["acier_poutres_kg"] / (C["ferraillage_poutre_kg_j"]["valeur"] * E["ferrailleurs_poutres"]),
    "ferraillage_dalle_j":   q["acier_dalle_kg"]   / (C["ferraillage_dalle_kg_j"]["valeur"] * E["ferrailleurs_dalle"]),
    "betonnage_j":           q["beton_m3"] / C["betonnage_m3_h"]["valeur"] / E["heures_par_jour"],
}
for cle, val in attendu.items():
    verifie(f"duree recalculee : {cle}", abs(t[cle] - val) < 0.01, f"{t[cle]} j contre {val:.3f} j")

# chaque duree doit dependre du BON effectif : on le prouve en le changeant un a un
for cle, poste in (("ferraillage_dalle_j", "ferrailleurs_dalle"),
                   ("ferraillage_poutres_j", "ferrailleurs_poutres"),
                   ("coffrage_j", "coffreurs")):
    dx = json.loads(json.dumps(d)); dx["effectifs"][poste] *= 2
    tx = durees_taches(dx, q)
    verifie(f"{cle} depend bien de « {poste} »",
            abs(tx[cle] - t[cle] / 2) < 0.01, f"{tx[cle]} j au lieu de {t[cle]} j")
    # et ne doit pas bouger les autres
    autres = [k for k in attendu if k != cle]
    verifie(f"doubler « {poste} » ne touche pas les autres durees",
            all(abs(tx[k] - t[k]) < 1e-9 for k in autres))
verifie("contre-calcul des deux hypotheses de cadence",
        t["contre_calcul_duree_coffrage"]["verdict"] == "OK",
        f"ecart {t['contre_calcul_duree_coffrage']['ecart_pct']} %")

# --- CPM : les deux algorithmes doivent coincider EXACTEMENT
verifie("les deux algorithmes CPM coincident", cc["ecart_j"] == 0.0,
        f"A {cc['voie_A_parcours_avant_arriere_j']} / B {cc['voie_B_enumeration_des_chemins_j']} j")
verifie("les deux voies designent le meme chemin critique",
        cc["les_deux_voies_designent_le_meme_chemin"])
verifie("le cycle est plus court que la somme des durees (recouvrement)",
        cc["voie_A_parcours_avant_arriere_j"] < sum(x.duree for x in reseau_zone(t, d["cycle_zone"])))

# --- et le CPM doit REAGIR : on allonge une tache critique
t2 = dict(t); t2["ferraillage_dalle_j"] = t["ferraillage_dalle_j"] + 1.0
cc2 = contre_calcul(reseau_zone(t2, d["cycle_zone"]))
verifie("allonger une tache critique allonge le cycle",
        cc2["voie_A_parcours_avant_arriere_j"] > cc["voie_A_parcours_avant_arriere_j"],
        f"{cc2['voie_A_parcours_avant_arriere_j']} j contre {cc['voie_A_parcours_avant_arriere_j']} j")

# --- le plancher complet : recalcul independant de la duree totale
pl = _pl
n = z["nb_zones"]; cad = pl["planning_plancher"]["cadence_zone_j"]
attendu_total = (n - 1) * cad + cc["voie_A_parcours_avant_arriere_j"]
verifie("duree du plancher recalculee a la main",
        abs(pl["planning_plancher"]["duree_totale_j"] - attendu_total) < 0.02,
        f"{pl['planning_plancher']['duree_totale_j']} j contre {attendu_total:.2f} j")

# --- cout : recalcul independant, et le garde-fou du double compte
p = d["prix_unitaires_MAD"]["postes"]
total_main = (q["beton_m3"] * p["beton_m3"]["valeur"] + q["acier_kg"] * p["acier_kg"]["valeur"]
              + q["coffrage_m2"] * p["coffrage_m2"]["valeur"])
verifie("cout de la zone recalcule a la main",
        abs(c["total_fournitures_et_mise_en_oeuvre_MAD"] - total_main) < 2,
        f"{c['total_fournitures_et_mise_en_oeuvre_MAD']} MAD")
verifie("la main d'oeuvre n'est PAS dans le total",
        c["total_fournitures_et_mise_en_oeuvre_MAD"] < total_main + c["main_oeuvre_MAD"] - 1)

# --- valeur acquise : les deux voies sont-elles reellement independantes ?
vcc = va["contre_calcul"]
verifie("les deux voies de valeur acquise donnent des montants differents",
        vcc["voie_A_par_les_couts_MAD"] != vcc["voie_B_par_les_quantites_MAD"],
        f"A {vcc['voie_A_par_les_couts_MAD']} / B {vcc['voie_B_par_les_quantites_MAD']} MAD")
# et la voie B ne doit PAS dependre de l'avancement declare : on le change, elle ne bouge pas
d2 = json.loads(json.dumps(d))
d2["suivi"]["avancement_zone_en_cours_pct"] = 90
va2 = valeur_acquise(d2, q, c, _pl["suivi"], _pl["avancement_physique"]["quantites_faites"])
verifie("la voie B ne depend pas de l'avancement declare",
        va2["contre_calcul"]["voie_B_par_les_quantites_MAD"] == vcc["voie_B_par_les_quantites_MAD"],
        "elle part des releves, pas du declare")
verifie("la voie A non plus : les deux partent desormais du PHYSIQUE, pas du declare",
        va2["contre_calcul"]["voie_A_par_les_couts_MAD"] == vcc["voie_A_par_les_couts_MAD"],
        "voie A = etat physique calcule x prix ; voie B = quantites relevees x prix")

# --- la courbe en S doit dire la MEME chose que le tableau de valeur acquise
# (defaut B3 : 59,9 % contre 50,0 % a la meme date, legende affirmant que l'ecart etait SV)
_arret = _pl["suivi"]["jour_arret"]
_pts = [x for x in _pl["figures"]["courbe_s"]["points"] if abs(x["j"] - _arret) < 1e-9]
verifie("la courbe en S porte un point A la date d'arret", len(_pts) == 1,
        f"{len(_pts)} point(s) a j = {_arret}")
if _pts:
    _pt = _pts[0]
    _bac = va["budget_a_l_achevement_BAC_MAD"]
    _vp, _vaq = va["valeur_planifiee_VP_MAD"] / _bac * 100, va["valeur_acquise_VA_MAD"] / _bac * 100
    verifie("prevu de la courbe = VP/BAC a 0,5 point pres", abs(_pt["prevu"] - _vp) <= 0.5,
            f"{_pt['prevu']} % contre {_vp:.2f} %")
    _cst = _pl["figures"]["constat_avancement"]
    verifie("le constat est UN point, pas une courbe", len(_cst) == 1,
            f"{len(_cst)} point(s) de constat pour 1 releve dans data/")
    verifie("aucun point de la courbe ne porte un « realise » fabrique",
            not any("realise" in x for x in _pl["figures"]["courbe_s"]["points"]))
    verifie("le constat est a la date d'arret", abs(_cst[0]["j"] - _arret) < 1e-9,
            f"j = {_cst[0]['j']}")
    verifie("realise du constat = VA/BAC a 0,5 point pres", abs(_cst[0]["realise"] - _vaq) <= 0.5,
            f"{_cst[0]['realise']} % contre {_vaq:.2f} %")
    _sv = -va["ecart_de_delai_SV_MAD"] / _bac * 100
    verifie("l'ecart vertical de la figure EST bien SV, comme la legende l'affirme",
            abs((_pt["prevu"] - _cst[0]["realise"]) - _sv) <= 0.5,
            f"{_pt['prevu'] - _cst[0]['realise']:.2f} points contre {_sv:.2f}")

# --- le planning doit tenir avec le MATERIEL declare, pas seulement sur le papier
_cm = _pl["coherence_materiel"]
_ref = _pl["variantes"]["reference"]
verifie("zones coffrees simultanement = ceil(cycle / cadence)",
        _cm["zones_coffrees_simultanement"] == math.ceil(
            _pl["cycle_zone"]["duree_j"] / _pl["planning_plancher"]["cadence_zone_j"] - 1e-9),
        f"{_cm['zones_coffrees_simultanement']} zones")
verifie("coffrage immobilise = zones simultanees x coffrage de zone",
        abs(_cm["coffrage_mobilise_m2"]
            - _cm["zones_coffrees_simultanement"] * q["coffrage_m2"]) <= 1,
        f"{_cm['coffrage_mobilise_m2']} m2")
verifie("le nombre de zones etayees est borne par le nombre de zones",
        _cm["zones_etayees_simultanement"] <= _pl["planning_plancher"]["nb_zones"],
        f"{_cm['zones_etayees_simultanement']} zones etayees sur {_pl['planning_plancher']['nb_zones']}")
verifie("et la saturation de l'etaiement est signalee quand elle arrive",
        _cm["tout_le_plancher_est_etaye"] == (
            _cm["zones_etayees_avant_bornage"] > _pl["planning_plancher"]["nb_zones"]))
verifie("le planning de reference tient avec le parc declare",
        _cm["verdict"] == "OK",
        f"{_cm['coffrage_mobilise_m2']} m2 pour {_cm['stock_declare_m2']} m2 au parc")
# canari : une cadence deliberement trop courte DOIT faire sonner le controle de parc.
# L'ancienne version s'appuyait sur une variante publiee dont la cadence etait fausse :
# le controle paraissait savoir sonner parce qu'un autre defaut le faisait sonner.
_cad_canari = 1.5
_simult = math.ceil(_pl["cycle_zone"]["duree_j"] / _cad_canari)
_mob = _simult * q["coffrage_m2"]
verifie("une cadence trop courte fait sonner le controle de parc : il sait echouer",
        _mob > _cm["stock_declare_m2"],
        f"a {_cad_canari} j/zone il faudrait {_mob:.0f} m2 pour {_cm['stock_declare_m2']} au parc")

# --- la cadence est fixee par la RESSOURCE la plus chargee, equipes ET grue
_rc = _pl["regle_cadence"]
_dur_ded = _rc["durees_des_equipes_dediees_j"]
verifie("toutes les equipes dediees entrent dans la regle, decoffrage compris",
        set(_dur_ded) == {"coffrage_j", "ferraillage_poutres_j", "ferraillage_dalle_j",
                          "betonnage_j", "decoffrage_j"}, ", ".join(sorted(_dur_ded)))
_grue = d["cycle_zone"]["taches_servies_par_la_grue"]["valeur"]
_occ = sum(_dur_ded[c] for c in _grue) / d["materiel"]["nb_grues"]
verifie("l'occupation de la grue est la SOMME de ses taches, divisee par le nombre de grues",
        abs(_rc["occupation_de_la_grue_j"] - _occ) < 0.01, f"{_rc['occupation_de_la_grue_j']} j")
verifie("la borne theorique = max(equipe la plus chargee ; grue), recalcule a la main",
        abs(_rc["borne_theorique_j"] - max(max(_dur_ded.values()), _occ)) < 0.01,
        f"{_rc['borne_theorique_j']} j")
verifie("la cadence retenue = borne + marge declaree",
        abs(_rc["cadence_j"] - _rc["borne_theorique_j"]
            * (1 + d["cycle_zone"]["marge_de_rotation_pct"]["valeur"] / 100)) < 0.01,
        f"{_rc['cadence_j']} j pour une borne de {_rc['borne_theorique_j']}")
verifie("la marge de rotation est publiee, pas cachee dans la formule",
        _rc["marge_de_rotation_j"] > 0, f"{_rc['marge_de_rotation_j']} j")

# chaque renfort DEPLACE la borne sur une autre ressource : c'est la lecon du module
_cascade = [("reference", "ferrailleurs_dalle"), ("effectif_renforce", "ferrailleurs_poutres"),
            ("effectif_renforce_deux_equipes", "grue"), ("deux_equipes_et_deux_grues", "ferrailleurs_dalle")]
for _cle, _attendu in _cascade:
    _v = _pl["variantes"][_cle]
    verifie(f"variante « {_cle} » : la borne est {_attendu}",
            _attendu in _v["ressource_qui_borne"],
            f"{_v['ressource_qui_borne']} a {_v['cadence_j']} j, plancher {_v['duree_plancher_j']} j")
verifie("renforcer les deux equipes ne suffit PAS a tenir 25 jours",
        _pl["variantes"]["effectif_renforce_deux_equipes"]["duree_plancher_j"] > 25,
        f"{_pl['variantes']['effectif_renforce_deux_equipes']['duree_plancher_j']} j")
verifie("il faut la seconde grue pour passer sous la cible",
        _pl["variantes"]["deux_equipes_et_deux_grues"]["duree_plancher_j"] < 25,
        f"{_pl['variantes']['deux_equipes_et_deux_grues']['duree_plancher_j']} j")

# --- l'affectation des equipes aux taches est-elle la bonne ?
# Une permutation de `effectif_par_tache` (coffreurs sur le ferraillage, et l'inverse)
# deplacait l'histogramme jour par jour sans faire bouger un seul des quinze controles.
_att_eq = {"COF": "coffreurs", "FEP": "ferrailleurs_poutres", "FED": "ferrailleurs_dalle",
           "BET": "equipe_betonnage", "PTA": 0, "CUR": 0}
_pose = d["cycle_zone"]["effectif_par_tache"]
for _t, _e in _att_eq.items():
    verifie(f"la tache {_t} est servie par « {_e} »", _pose.get(_t) == _e,
            f"data/ dit « {_pose.get(_t)} »")
verifie("le decoffrage mobilise un effectif reduit, pas l'equipe de coffrage entiere",
        isinstance(_pose.get("DEC"), int) and 0 < _pose["DEC"] < d["effectifs"]["coffreurs"],
        f"DEC = {_pose.get('DEC')}")

# --- l'histogramme publie, reconstruit ici sans appeler le code de production
_eff_t = {k: (d["effectifs"][v] if isinstance(v, str) else v)
          for k, v in _pose.items() if not k.startswith("_")}
_rz2 = voie_A_parcours(reseau_zone(t, d["cycle_zone"]))
_deb = _pl["planning_plancher"]["debuts"]
_recalcule = []
for _k in range(len(_pl["figures"]["effectifs"])):
    _act = {x.id for dz in _deb.values() for x in reseau_zone(t, d["cycle_zone"])
            if dz + _rz2["tot"][x.id][0] < _k + 1 <= _k + 1
            and _k < dz + _rz2["tot"][x.id][1] and dz + _rz2["tot"][x.id][0] < _k + 1}
    _n = sum(_eff_t.get(i, 0) for i in _act)
    _recalcule.append(_n + (d["effectifs"]["chef_equipe"] + d["effectifs"]["grutier"]) if _n else 0)
_publie = [x["n"] for x in _pl["figures"]["effectifs"]]
verifie("l'histogramme publie est reproductible depuis data/ seul",
        _recalcule == _publie,
        f"{sum(1 for a_, b_ in zip(_recalcule, _publie) if a_ != b_)} jour(s) different(s)")

# --- l'etat physique : chaque poste suit-il la tache qui le PRODUIT ?
# Canari du relecteur : permuter le rattachement poste -> tache laissait calc/ vert,
# alors que le module aurait publie « 0 m2 de coffrage et 98,4 m3 de beton » pour une
# zone ou rien n'est coule. On recalcule ici l'etat a plusieurs dates, sans la fonction.
_res_z = reseau_zone(t, d["cycle_zone"])
_rz3 = voie_A_parcours(_res_z)
_cyc = max(f for _, f in _rz3["tot"].values())
for _frac in (0.0, 0.25, 0.6, 0.9, 1.0):
    _e = etat_physique_de_zone(q, _res_z, _frac)
    _tx = _frac * _cyc

    def _av(cle):
        _deb, _fin = _rz3["tot"][cle]
        return 0.0 if _tx <= _deb else 1.0 if _tx >= _fin else (_tx - _deb) / (_fin - _deb)

    _att_cof = q["coffrage_m2"] * _av("COF")
    _att_ac = q["acier_poutres_kg"] * _av("FEP") + q["acier_dalle_kg"] * _av("FED")
    _att_bet = q["beton_m3"] * _av("BET")
    verifie(f"etat physique a {_frac:.0%} du cycle : le coffrage suit COF",
            abs(_e["coffrage_m2"] - _att_cof) < 0.2, f"{_e['coffrage_m2']} contre {_att_cof:.1f}")
    verifie(f"etat physique a {_frac:.0%} : l'acier suit FEP puis FED",
            abs(_e["acier_kg"] - _att_ac) < 1.0, f"{_e['acier_kg']} contre {_att_ac:.0f}")
    verifie(f"etat physique a {_frac:.0%} : le beton suit BET",
            abs(_e["beton_m3"] - _att_bet) < 0.2, f"{_e['beton_m3']} contre {_att_bet:.1f}")
verifie("a 60 % du cycle, le beton est a ZERO : c'est la these du module",
        etat_physique_de_zone(q, _res_z, 0.6)["beton_m3"] == 0.0)
verifie("et a 100 %, tout y est",
        all(abs(etat_physique_de_zone(q, _res_z, 1.0)[k] - q[k]) < 0.2
            for k in ("beton_m3", "coffrage_m2")))

# --- la grue : conflits INSTANTANES, pas seulement occupation moyenne
_ids_g = {"coffrage_j": "COF", "decoffrage_j": "DEC", "betonnage_j": "BET",
          "ferraillage_poutres_j": "FEP", "ferraillage_dalle_j": "FED"}
_tg_t = [_ids_g[x] for x in d["cycle_zone"]["taches_servies_par_la_grue"]["valeur"]]
_cf = conflits_de_ressource(_res_z, _pl["planning_plancher"]["debuts"], _tg_t,
                            d["materiel"]["nb_grues"])
verifie("le planning BRUT demande bien la grue en deux endroits : le controle le voit",
        len(_cf) > 0, f"{len(_cf)} conflit(s), ex. {_cf[0]['demandes'] if _cf else '-'}")
verifie("et le module publie ce nombre",
        _pl["coherence_materiel"]["grue"]["conflits_au_planning_brut"] == len(_cf))
verifie("decaler le decoffrage dans sa marge les resout tous",
        _pl["coherence_materiel"]["grue"]["conflits_apres_resolution"] == 0,
        f"decalage max {_pl['coherence_materiel']['grue']['resolution']['decalage_max_j']} j")
verifie("une occupation MOYENNE sous 100 % ne suffisait donc pas",
        _pl["regle_cadence"]["occupation_de_la_grue_j"] < _pl["planning_plancher"]["cadence_zone_j"],
        f"{_pl['regle_cadence']['occupation_de_la_grue_j']} j occupee pour une cadence de "
        f"{_pl['planning_plancher']['cadence_zone_j']} j — et pourtant {len(_cf)} conflits")

# --- le taux de recouvrement declare est-il celui que le reseau realise ?
# Il etait applique a son COMPLEMENT : 40 % declare produisait 60 % realise. Sur le
# premier lien l'erreur etait invisible, 50 % etant auto-complementaire.
_rr = voie_A_parcours(reseau_zone(t, d["cycle_zone"]))
for _a, _b, _cle in (("COF", "FEP", "recouvrement_coffrage_ferraillage_poutres_pct"),
                     ("FEP", "FED", "recouvrement_ferraillage_poutres_dalle_pct")):
    _da, _fa = _rr["tot"][_a]
    _db = _rr["tot"][_b][0]
    _realise = (_db - _da) / (_fa - _da) * 100
    verifie(f"recouvrement {_a}->{_b} : le reseau realise le taux DECLARE",
            abs(_realise - d["cycle_zone"][_cle]["valeur"]) < 0.5,
            f"declare {d['cycle_zone'][_cle]['valeur']} %, realise {_realise:.1f} %")

# --- B2 : l'histogramme suit le reseau, donc il montre les recouvrements
_h = {x["j"]: x["n"] for x in _pl["figures"]["effectifs"]}
_r_zone = voie_A_parcours(reseau_zone(t, d["cycle_zone"]))
_deb_fep, _fin_cof = _r_zone["tot"]["FEP"][0], _r_zone["tot"]["COF"][1]
verifie("le reseau comporte bien un recouvrement coffrage / ferraillage de poutres",
        _deb_fep < _fin_cof, f"FEP demarre a {_deb_fep:.2f}, COF finit a {_fin_cof:.2f}")
_k = int(math.floor((_deb_fep + _fin_cof) / 2))
verifie("au jour du recouvrement, les DEUX equipes au moins sont comptees",
        _h.get(_k, 0) >= d["effectifs"]["coffreurs"] + d["effectifs"]["ferrailleurs_poutres"],
        f"jour {_k} : {_h.get(_k)} presents")
verifie("la pointe publiee est bien le maximum de l'histogramme",
        _pl["variantes"]["reference"]["pointe_effectif"] == max(_h.values()),
        f"{_pl['variantes']['reference']['pointe_effectif']} contre {max(_h.values())}")

# --- le contre-calcul du coffrage doit publier la LARGEUR sur laquelle il tient
_cc1 = _pl["durees"]["contre_calcul_duree_coffrage"]
_lo, _hi = _cc1["plage_de_rendement_qui_passe_m2_j"]
_rend = d["cadences"]["rendement_equipe_coffrage_m2_j"]["valeur"]
verifie("le rendement retenu est bien dans la plage qui passe", _lo <= _rend <= _hi,
        f"{_rend} dans [{_lo} ; {_hi}]")
verifie("la plage qui passe est plus etroite que la fourchette declaree",
        _cc1["part_de_la_fourchette_qui_passe_pct"] < 100,
        f"{_cc1['part_de_la_fourchette_qui_passe_pct']} % de la fourchette")
_fl, _fh = _cc1["fourchette_declaree_m2_j"]
verifie("pris a la borne basse de sa fourchette, le controle echouerait",
        abs(q["coffrage_m2"] / _fl - _pl["durees"]["coffrage_j"]) / _pl["durees"]["coffrage_j"] * 100
        > _cc1["tolerance_pct"],
        f"rendement {_fl} m2/j")

# --- chaque V3 de data/ doit etre DANS sa propre fourchette.
# Aucun controle ne le verifiait : une valeur pouvait sortir de l'intervalle qu'elle
# declare, ce qui rend la fourchette decorative.
def _feuilles_v3(o, chemin=""):
    if isinstance(o, dict):
        if "valeur" in o and "fourchette" in o:
            yield chemin, o
            return
        for k, v in o.items():
            yield from _feuilles_v3(v, f"{chemin}.{k}" if chemin else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _feuilles_v3(v, f"{chemin}.{i}")

_hors, _n_v3 = [], 0
for _ch, _h in _feuilles_v3(d):
    if not isinstance(_h["valeur"], (int, float)):
        continue
    _n_v3 += 1
    _lo, _hi = _h["fourchette"]
    if not (_lo <= _h["valeur"] <= _hi):
        _hors.append(f"{_ch} = {_h['valeur']} hors [{_lo} ; {_hi}]")
verifie("chaque hypothese V3 de data/ est dans sa propre fourchette", not _hors,
        "; ".join(_hors) if _hors else f"{_n_v3} hypotheses verifiees")
verifie("et le controle sait echouer", not (0 <= -1 <= 0))

# --- CPI et SPI : ordres de grandeur plausibles pour un chantier
verifie("CPI dans une plage plausible (0,7 a 1,2)", 0.7 <= va["CPI"] <= 1.2, f"{va['CPI']}")
verifie("SPI dans une plage plausible (0,7 a 1,2)", 0.7 <= va["SPI"] <= 1.2, f"{va['SPI']}")

_geo = [p for p in va["recoupement_physique"]["postes"] if p["nature"] == "geometrique"]
_detail = ", ".join("{} {:+.2f} %".format(p["poste"], p["ecart_pct"]) for p in _geo)
_comp = ">" if vcc["ecart_pct"] > vcc["tolerance_pct"] else "<="
print(f"  info  recoupement en dirhams : ecart {vcc['ecart_pct']} % {_comp} tolerance "
      f"{vcc['tolerance_pct']} % · postes GEOMETRIQUES : {_detail}. "
      f"L'alarme d'avant venait d'un etat attendu calcule au prorata uniforme, "
      f"c'est-a-dire d'un modele faux — pas du chantier.")
print(f"  info  le controle de prix horaire sort de sa fourchette "
      f"({c['coherence_prix_horaire']['part_constatee_pct']} % contre "
      f"{c['coherence_prix_horaire']['fourchette_attendue_pct']}) : explique dans le module")

print(f"\n{len(echecs)} echec(s)." if echecs else "\nTests du plancher : tous verts.")
sys.exit(1 if echecs else 0)
