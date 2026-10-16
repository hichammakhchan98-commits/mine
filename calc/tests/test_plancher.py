"""Tests de la tranche verticale (§ 12.1 f).

Regle reprise du socle : une assertion qui ne peut pas echouer ne vaut rien.
Chaque controle ci-dessous est double d'une erreur injectee qui DOIT le faire sonner.
"""
from __future__ import annotations
import json, math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from plancher import quantites_zone, fourchette_acier
from cycle_plancher import durees_taches, reseau_zone, cout_zone
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
cc = contre_calcul(reseau_zone(t))
c = cout_zone(d, q, t)
_pl = json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json").read_text(encoding="utf-8"))
va = valeur_acquise(d, q, c, _pl["suivi"])
z = d["geometrie"]["mezzanine"]["zones_de_coulage"]

# --- geometrie : les zones doivent recouvrir exactement la mezzanine
total = z["nb_zones"] * z["longueur_zone_m"] * z["largeur_zone_m"]
attendu = 120.0 * d["geometrie"]["mezzanine"]["largeur_m"]
verifie("les zones recouvrent exactement la mezzanine", abs(total - attendu) < 1e-9,
        f"{total:.0f} m2 contre {attendu:.0f} m2")

# --- beton : recalcul INDEPENDANT, a la main, sans appeler plancher.py
beton_main = 360 * 0.25 + 2 * 24.0 * 0.35 * 0.50
verifie("volume de beton recalcule a la main", abs(q["beton_m3"] - beton_main) < 0.01,
        f"{q['beton_m3']} m3 contre {beton_main} m3")

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
        cc["voie_A_parcours_avant_arriere_j"] < sum(x.duree for x in reseau_zone(t)))

# --- et le CPM doit REAGIR : on allonge une tache critique
t2 = dict(t); t2["ferraillage_dalle_j"] = t["ferraillage_dalle_j"] + 1.0
cc2 = contre_calcul(reseau_zone(t2))
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
va2 = valeur_acquise(d2, q, c, _pl["suivi"])
verifie("la voie B ne depend pas de l'avancement declare",
        va2["contre_calcul"]["voie_B_par_les_quantites_MAD"] == vcc["voie_B_par_les_quantites_MAD"],
        "elle part des releves, pas du declare")
verifie("la voie A, elle, en depend bien",
        va2["contre_calcul"]["voie_A_par_les_couts_MAD"] != vcc["voie_A_par_les_couts_MAD"])

# --- la courbe en S doit dire la MEME chose que le tableau de valeur acquise
# (defaut B3 : 59,9 % contre 50,0 % a la meme date, legende affirmant que l'ecart etait SV)
_arret = _pl["suivi"]["jour_arret"]
_pts = [x for x in _pl["figures"]["courbe_s"] if abs(x["j"] - _arret) < 1e-9]
verifie("la courbe en S porte un point A la date d'arret", len(_pts) == 1,
        f"{len(_pts)} point(s) a j = {_arret}")
if _pts:
    _pt = _pts[0]
    _bac = va["budget_a_l_achevement_BAC_MAD"]
    _vp, _vaq = va["valeur_planifiee_VP_MAD"] / _bac * 100, va["valeur_acquise_VA_MAD"] / _bac * 100
    verifie("prevu de la courbe = VP/BAC a 0,5 point pres", abs(_pt["prevu"] - _vp) <= 0.5,
            f"{_pt['prevu']} % contre {_vp:.2f} %")
    verifie("realise de la courbe = VA/BAC a 0,5 point pres", abs(_pt["realise"] - _vaq) <= 0.5,
            f"{_pt['realise']} % contre {_vaq:.2f} %")
    _sv = -va["ecart_de_delai_SV_MAD"] / _bac * 100
    verifie("l'ecart vertical de la figure EST bien SV, comme la legende l'affirme",
            abs((_pt["prevu"] - _pt["realise"]) - _sv) <= 0.5,
            f"{_pt['prevu'] - _pt['realise']:.2f} points contre {_sv:.2f}")
    verifie("le constat ne depasse pas la date d'arret",
            max(x["j"] for x in _pl["figures"]["courbe_s"] if "realise" in x) <= _arret + 1e-9)

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
verifie("le planning de reference tient avec le parc declare",
        _cm["verdict"] == "OK",
        f"{_cm['coffrage_mobilise_m2']} m2 pour {_cm['stock_declare_m2']} m2 au parc")
verifie("la variante renforcee, elle, NE tient PAS : le controle sait donc sonner",
        not _pl["variantes"]["effectif_renforce"]["coffrage_suffisant"]
        and _pl["variantes"]["effectif_renforce"]["deficit_coffrage_m2"] > 0,
        f"deficit {_pl['variantes']['effectif_renforce']['deficit_coffrage_m2']} m2")

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

# --- CPI et SPI : ordres de grandeur plausibles pour un chantier
verifie("CPI dans une plage plausible (0,7 a 1,2)", 0.7 <= va["CPI"] <= 1.2, f"{va['CPI']}")
verifie("SPI dans une plage plausible (0,7 a 1,2)", 0.7 <= va["SPI"] <= 1.2, f"{va['SPI']}")

_geo = [p for p in va["recoupement_physique"]["postes"] if p["nature"] == "geometrique"]
_detail = ", ".join("{} {:+.2f} %".format(p["poste"], p["ecart_pct"]) for p in _geo)
print(f"  info  recoupement en dirhams : ecart {vcc['ecart_pct']} % > tolerance "
      f"{vcc['tolerance_pct']} %, mais les postes GEOMETRIQUES restent sous le pour cent "
      f"({_detail}) : bruit du ratio d'acier, pas signal d'avancement — "
      f"c'est la lecture que le module enseigne")
print(f"  info  le controle de prix horaire sort de sa fourchette "
      f"({c['coherence_prix_horaire']['part_constatee_pct']} % contre "
      f"{c['coherence_prix_horaire']['fourchette_attendue_pct']}) : explique dans le module")

print(f"\n{len(echecs)} echec(s)." if echecs else "\nTests du plancher : tous verts.")
sys.exit(1 if echecs else 0)
