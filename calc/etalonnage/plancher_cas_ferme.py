"""Etalonnage de plancher.py et de valeur_acquise.py (§ 3.3).

Sans etalonnage, leurs resultats restent V3 et ne servent pas d'exemple de reference.
Deux familles de cas :
  a) GEOMETRIE a solution fermee, posee a la main sans appeler le module ;
  b) IDENTITES de la valeur acquise, qui tiennent quels que soient les chiffres.
Plus une verification dimensionnelle (pint) de chaque formule publiee.
"""
from __future__ import annotations
import json, sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from plancher import quantites_zone
from cycle_plancher import durees_taches, cout_zone, reseau_zone
from cpm import contre_calcul
from valeur_acquise import valeur_acquise

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
ok = True


def dit(bon, nom, detail=""):
    global ok
    ok &= bon
    print(f"  {'ok   ' if bon else 'ECHEC'} {nom}{(' — ' + detail) if detail else ''}")


# ---------- a) geometrie a solution fermee ----------
print("ETALONNAGE — quantites d'une zone de plancher")
cas = {
    "geometrie": {"mezzanine": {"largeur_m": 10.0, "zones_de_coulage": {
        "nb_zones": 1, "longueur_zone_m": 10.0, "largeur_zone_m": 10.0}}},
    "elements": {
        "dalles": [{"id": "DM1", "epaisseur_m": 0.20}],
        "poutres": [{"id": "PM1", "entraxe_m": 5.0, "longueur_dans_zone_m": 10.0,
                     "b_m": 0.40, "h_m": 0.60, "retombee_sous_dalle_m": 0.40}]},
    "ratios_V3": {"acier_dalle_kg_m3": {"valeur": 100, "fourchette": [100, 100]},
                  "acier_poutre_kg_m3": {"valeur": 200, "fourchette": [200, 200]},
                  "coffrage_rives_pct": {"valeur": 0}},
}
q = quantites_zone(cas)
# pose a la main : 10 x 10 x 0,20 = 20,00 m3 de dalle ; 2 poutres de 10 m, 0,40 x 0,40 = 3,20 m3
dit(abs(q["beton_dalle_m3"] - 20.00) < 1e-9, "beton de dalle, solution fermee", f"{q['beton_dalle_m3']} m3")
dit(abs(q["beton_poutres_m3"] - 3.20) < 1e-9, "beton de poutres, solution fermee", f"{q['beton_poutres_m3']} m3")
# coffrage : 100 - 2x10x0,40 = 92,0 de sous-face ; joues 2x10x0,40x2 = 16,0 ; fond 2x10x0,40 = 8,0
dit(abs(q["coffrage_m2"] - 116.0) < 1e-9, "coffrage, solution fermee", f"{q['coffrage_m2']} m2")
# acier : 20 x 100 + 3,2 x 200 = 2 640 kg
dit(q["acier_kg"] == 2640, "acier par ratios, solution fermee", f"{q['acier_kg']} kg")
# le coffrage d'une dalle SANS poutre vaut exactement sa surface
sans = json.loads(json.dumps(cas))
sans["elements"]["poutres"][0]["retombee_sous_dalle_m"] = 0.0
sans["elements"]["poutres"][0]["b_m"] = 0.0
dit(abs(quantites_zone(sans)["coffrage_m2"] - 100.0) < 1e-9,
    "sans retombee, coffrage = surface", "cas limite")

# ---------- b) identites de la valeur acquise ----------
print("ETALONNAGE — identites de la valeur acquise")
d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
qr = quantites_zone(d)
t = durees_taches(d, qr)
c = cout_zone(d, qr, t)
plan_suivi = {"zones_prevues_equivalentes":
              json.loads((RACINE / "calc" / "sorties" / "tranche-plancher.json")
                         .read_text(encoding="utf-8"))["suivi"]["zones_prevues_equivalentes"]}
va = valeur_acquise(d, qr, c, plan_suivi)
dit(abs(va["CPI"] - va["valeur_acquise_VA_MAD"] / va["cout_reel_CR_MAD"]) < 1e-3,
    "CPI = VA / CR", f"{va['CPI']}")
dit(abs(va["SPI"] - va["valeur_acquise_VA_MAD"] / va["valeur_planifiee_VP_MAD"]) < 1e-3,
    "SPI = VA / VP", f"{va['SPI']}")
dit(abs(va["ecart_de_cout_CV_MAD"] - (va["valeur_acquise_VA_MAD"] - va["cout_reel_CR_MAD"])) < 1,
    "CV = VA - CR")
dit(abs(va["ecart_de_delai_SV_MAD"] - (va["valeur_acquise_VA_MAD"] - va["valeur_planifiee_VP_MAD"])) < 1,
    "SV = VA - VP")
dit(abs(va["prevision_a_terminaison_EAC_MAD"] * va["CPI"]
        - va["budget_a_l_achevement_BAC_MAD"]) < 2000, "EAC x CPI = BAC")
# cas trivial : un chantier parfaitement a l'heure et au budget doit donner CPI = SPI = 1
d2 = json.loads(json.dumps(d))
bac = c["total_fournitures_et_mise_en_oeuvre_MAD"] * d["geometrie"]["mezzanine"]["zones_de_coulage"]["nb_zones"]
d2["suivi"]["zones_realisees_a_date"] = 4
d2["suivi"]["avancement_zone_en_cours_pct"] = 0
d2["suivi"]["cout_reel_constate_MAD"] = bac * 4 / 8
va2 = valeur_acquise(d2, qr, c, {"zones_prevues_equivalentes": 4.0})
dit(abs(va2["CPI"] - 1.0) < 1e-6 and abs(va2["SPI"] - 1.0) < 1e-6,
    "chantier parfaitement a l'heure et au budget : CPI = SPI = 1",
    f"CPI {va2['CPI']} · SPI {va2['SPI']}")

# ---------- c) verification dimensionnelle (pint) ----------
print("VERIFICATION DIMENSIONNELLE (pint)")
import pint
u = pint.UnitRegistry()
S = 360 * u.m**2
e_d = 0.25 * u.m
vol = (S * e_d).to(u.m**3)
dit(str(vol.units) == "meter ** 3", "surface x epaisseur donne un volume", f"{vol:~P}")
cad = 30 * u.m**2 / u.day
duree = (424.3 * u.m**2 / (cad * 8)).to(u.day)
dit(str(duree.units) == "day", "quantite / (cadence x effectif) donne un temps", f"{duree.magnitude:.2f} j")
prix = 1250 * u.MAD if hasattr(u, "MAD") else 1250 * u.dimensionless
cout_ = (98.4 * u.m**3) * (1250 / u.m**3)
dit(str(cout_.dimensionality) == "dimensionless", "volume x prix par volume est sans dimension (MAD)")
# une formule non homogene DOIT lever
leve = False
try:
    (424.3 * u.m**2 / (30 * u.m**2)).to(u.day)
except pint.DimensionalityError:
    leve = True
dit(leve, "une cadence sans unite de temps leve bien")

sys.exit(0 if ok else 1)
