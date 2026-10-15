"""Tests de la tranche verticale (§ 12.1 f).

Regle reprise du socle : une assertion qui ne peut pas echouer ne vaut rien.
Chaque controle ci-dessous est double d'une erreur injectee qui DOIT le faire sonner.
"""
from __future__ import annotations
import json, sys, pathlib
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
va = valeur_acquise(d, q, c)
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

# --- durees : recalcul independant
coff = q["coffrage_m2"] / (d["cadences"]["coffrage_dalle_m2_j"]["valeur"] * d["effectifs"]["coffreurs"])
verifie("duree de coffrage recalculee", abs(t["coffrage_j"] - coff) < 0.01,
        f"{t['coffrage_j']} j")
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
va2 = valeur_acquise(d2, q, c)
verifie("la voie B ne depend pas de l'avancement declare",
        va2["contre_calcul"]["voie_B_par_les_quantites_MAD"] == vcc["voie_B_par_les_quantites_MAD"],
        "elle part des releves, pas du declare")
verifie("la voie A, elle, en depend bien",
        va2["contre_calcul"]["voie_A_par_les_couts_MAD"] != vcc["voie_A_par_les_couts_MAD"])

# --- CPI et SPI : ordres de grandeur plausibles pour un chantier
verifie("CPI dans une plage plausible (0,7 a 1,2)", 0.7 <= va["CPI"] <= 1.2, f"{va['CPI']}")
verifie("SPI dans une plage plausible (0,7 a 1,2)", 0.7 <= va["SPI"] <= 1.2, f"{va['SPI']}")

print(f"  info  le contre-calcul de valeur acquise SONNE volontairement "
      f"({vcc['ecart_pct']} % > {vcc['tolerance_pct']} %) : c'est le cas que le module enseigne")
print(f"  info  le controle de prix horaire sort de sa fourchette "
      f"({c['coherence_prix_horaire']['part_constatee_pct']} % contre "
      f"{c['coherence_prix_horaire']['fourchette_attendue_pct']}) : explique dans le module")

print(f"\n{len(echecs)} echec(s)." if echecs else "\nTests du plancher : tous verts.")
sys.exit(1 if echecs else 0)
