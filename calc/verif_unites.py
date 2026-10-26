"""Verification dimensionnelle (pint) de CHAQUE formule publiee par les bibliotheques
de la tranche verticale : plancher.py, cycle_plancher.py, cpm.py, valeur_acquise.py.

Pourquoi un fichier a part. Le § 3.3 exige que « chaque formule de calc/ passe une
verification dimensionnelle automatique ». Ecrire les unites dans les bibliotheques
elles-memes doublerait chaque ligne de calcul ; les ecrire ici, une fois, alimentees
par data/, verifie la MEME formule sans alourdir le code de production. La contrepartie
est explicite : si une formule change dans la bibliotheque sans changer ici, la
verification ne le voit pas. C'est pourquoi chaque formule est reprise sous la forme
ou elle est ecrite dans la bibliotheque, avec le numero de ligne, et que les tests de
calc/ recalculent par ailleurs les resultats a la main.

Chaque controle est double d'un CONTRE-CONTROLE : une ecriture fausse qui DOIT lever.
Une verification qui ne peut pas echouer ne verifie rien.
"""
from __future__ import annotations
import json, pathlib, sys

import pint

RACINE = pathlib.Path(__file__).resolve().parent.parent
u = pint.UnitRegistry()
u.define("MAD = [monnaie]")          # dirham : une dimension monetaire a part entiere
u.define("compagnon = [personne]")   # un effectif est une grandeur, pas un nombre nu

ok = True


def dit(bon: bool, nom: str, detail: str = "") -> None:
    global ok
    ok = ok and bool(bon)
    print(f"  {'ok   ' if bon else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


def leve(nom: str, f) -> None:
    """Contre-controle : l'ecriture fausse doit lever une erreur de dimension."""
    try:
        f()
    except pint.DimensionalityError:
        dit(True, f"contre-controle : {nom} leve bien")
        return
    dit(False, f"contre-controle : {nom} N'A PAS leve")


d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
SORTIES = RACINE / "calc" / "sorties"
_tp = json.loads((SORTIES / "tranche-plancher.json").read_text(encoding="utf-8"))
_va = json.loads((SORTIES / "valeur-acquise.json").read_text(encoding="utf-8"))
z = d["geometrie"]["mezzanine"]["zones_de_coulage"]
dalle = next(x for x in d["elements"]["dalles"] if x["id"] == "DM1")
poutre = next(x for x in d["elements"]["poutres"] if x["id"] == "PM1")
r, c, e = d["ratios_V3"], d["cadences"], d["effectifs"]
p = d["prix_unitaires_MAD"]["postes"]

# ---------------------------------------------------------------- plancher.py
print("plancher.py — geometrie et ratios")
L = z["longueur_zone_m"] * u.m
lg = z["largeur_zone_m"] * u.m
ep = dalle["epaisseur_m"] * u.m
b = poutre["b_m"] * u.m
h = poutre["retombee_sous_dalle_m"] * u.m
Lp = poutre["longueur_dans_zone_m"] * u.m
n_p = 2                                       # sans dimension : un comptage

surface = (L * lg).to(u.m**2)
dit(str(surface.units) == "meter ** 2", "surface = L x l", f"{surface.magnitude:.1f} m2")

beton_dalle = (surface * ep).to(u.m**3)
dit(str(beton_dalle.units) == "meter ** 3", "beton de dalle = S x epaisseur",
    f"{beton_dalle.magnitude:.2f} m3")

beton_poutres = (n_p * Lp * b * h).to(u.m**3)
dit(str(beton_poutres.units) == "meter ** 3", "beton de poutres = n x L x b x retombee",
    f"{beton_poutres.magnitude:.2f} m3")

coffrage_joues = (n_p * Lp * h * 2).to(u.m**2)
dit(str(coffrage_joues.units) == "meter ** 2", "joues = 2 x n x L x retombee",
    f"{coffrage_joues.magnitude:.1f} m2")

ratio_dalle = r["acier_dalle_kg_m3"]["valeur"] * u.kg / u.m**3
acier_dalle = (beton_dalle * ratio_dalle).to(u.kg)
dit(str(acier_dalle.units) == "kilogram", "acier = volume x ratio kg/m3",
    f"{acier_dalle.magnitude:.0f} kg")

ratio_coffrage = (coffrage_joues / surface).to(u.dimensionless)
dit(ratio_coffrage.dimensionless, "ratio coffrage/surface est sans dimension")

leve("volume x ratio kg/m3 lu comme un m3", lambda: (beton_dalle * ratio_dalle).to(u.m**3))
leve("surface x epaisseur lue comme une surface", lambda: (surface * ep).to(u.m**2))

# ----------------------------------------------------------- cycle_plancher.py
print("\ncycle_plancher.py — durees, cout, main d'oeuvre")
cad_cof = c["coffrage_dalle_m2_j"]["valeur"] * u.m**2 / (u.day * u.compagnon)
n_cof = e["coffreurs"] * u.compagnon
coffrage_m2 = _tp["quantites"]["coffrage_m2"] * u.m**2
duree_cof = (coffrage_m2 / (cad_cof * n_cof)).to(u.day)
dit(str(duree_cof.units) == "day", "duree = quantite / (cadence x effectif)",
    f"{duree_cof.magnitude:.3f} j")

cad_ferr = c["ferraillage_dalle_kg_j"]["valeur"] * u.kg / (u.day * u.compagnon)
n_ferr = e["ferrailleurs_dalle"] * u.compagnon
duree_ferr = (acier_dalle / (cad_ferr * n_ferr)).to(u.day)
dit(str(duree_ferr.units) == "day", "duree de ferraillage = kg / (kg/j/compagnon x compagnon)",
    f"{duree_ferr.magnitude:.3f} j")

cad_bet = c["betonnage_m3_h"]["valeur"] * u.m**3 / u.hour
heures_j = e["heures_par_jour"] * u.hour / u.day
duree_bet = ((beton_dalle + beton_poutres) / cad_bet / heures_j).to(u.day)
dit(str(duree_bet.units) == "day", "duree de betonnage = m3 / (m3/h) / (h/j)",
    f"{duree_bet.magnitude:.3f} j")

cadence = (max(duree_cof, duree_ferr) + duree_bet).to(u.day)
dit(str(cadence.units) == "day", "cadence de rotation = max(tache la plus longue) + betonnage",
    f"{cadence.magnitude:.2f} j")

acier_zone = _tp["quantites"]["acier_kg"] * u.kg
cout = ((beton_dalle + beton_poutres) * (p["beton_m3"]["valeur"] * u.MAD / u.m**3)
        + acier_zone * (p["acier_kg"]["valeur"] * u.MAD / u.kg)
        + coffrage_m2 * (p["coffrage_m2"]["valeur"] * u.MAD / u.m**2)).to(u.MAD)
dit(str(cout.units) == "MAD", "cout = somme des quantites x prix unitaires",
    f"{cout.magnitude:.0f} MAD")

heures = (duree_cof * n_cof * heures_j).to(u.hour * u.compagnon)
dit(str(heures.dimensionality) == str((u.hour * u.compagnon).dimensionality),
    "heures = duree x effectif x heures par jour", f"{heures.magnitude:.0f} h.compagnon")

prix_h = p["main_oeuvre_h"]["valeur"] * u.MAD / (u.hour * u.compagnon)
part = (heures * prix_h / cout).to(u.dimensionless)
dit(part.dimensionless, "part de main d'oeuvre = (heures x prix horaire) / cout",
    f"{part.magnitude * 100:.2f} %")

n_zones = z["nb_zones"]
cycle = _tp["cycle_zone"]["duree_j"] * u.day
duree_plancher = ((n_zones - 1) * cadence + cycle).to(u.day)
dit(str(duree_plancher.units) == "day", "duree du plancher = (n-1) x cadence + cycle",
    f"{duree_plancher.magnitude:.2f} j")

coffrage_mobilise = (_tp["variantes"]["reference"]["zones_coffrees_simultanement"] * coffrage_m2).to(u.m**2)
stock = d["materiel"]["tables_coffrantes_m2"] * u.m**2
deficit = (coffrage_mobilise - stock).to(u.m**2)
dit(str(deficit.units) == "meter ** 2", "deficit de coffrage = immobilise - stock declare",
    f"{deficit.magnitude:+.0f} m2")
dit(str(coffrage_mobilise.units) == "meter ** 2",
    "coffrage immobilise = zones simultanees x coffrage de zone",
    f"{coffrage_mobilise.magnitude:.0f} m2")

leve("quantite / cadence sans effectif lue en jours",
     lambda: (coffrage_m2 / cad_cof).to(u.day))
leve("heures x prix horaire additionnees a une duree",
     lambda: (heures * prix_h + duree_cof).to(u.MAD))
leve("part de main d'oeuvre calculee avec un prix au m3",
     lambda: (heures * (45 * u.MAD / u.m**3) / cout).to(u.dimensionless))

# ------------------------------------------------------------------- cpm.py
print("\ncpm.py — dates et decalages")
debut = 0.0 * u.day
decalage = -0.884 * u.day                      # decalage negatif : un recouvrement
fin = (debut + duree_cof).to(u.day)
dit(str(fin.units) == "day", "fin = debut + duree", f"{fin.magnitude:.3f} j")
debut_suiv = max(0 * u.day, (fin + decalage)).to(u.day)
dit(str(debut_suiv.units) == "day", "debut du successeur = fin + decalage, borne a zero",
    f"{debut_suiv.magnitude:.3f} j")
marge = (fin - fin).to(u.day)
dit(str(marge.units) == "day", "marge = date au plus tard - date au plus tot")
leve("un decalage exprime en m2", lambda: (fin + 1 * u.m**2).to(u.day))

# --------------------------------------------------------- valeur_acquise.py
print("\nvaleur_acquise.py — indicateurs de valeur acquise")
BAC = _va["budget_a_l_achevement_BAC_MAD"] * u.MAD
VP = _va["valeur_planifiee_VP_MAD"] * u.MAD
VA = _va["valeur_acquise_VA_MAD"] * u.MAD
CR = _va["cout_reel_CR_MAD"] * u.MAD
CPI = (VA / CR).to(u.dimensionless)
SPI = (VA / VP).to(u.dimensionless)
dit(CPI.dimensionless and SPI.dimensionless, "CPI = VA/CR et SPI = VA/VP sont sans dimension",
    f"CPI {CPI.magnitude:.3f} · SPI {SPI.magnitude:.3f}")
CV = (VA - CR).to(u.MAD)
SV = (VA - VP).to(u.MAD)
dit(str(CV.units) == "MAD" and str(SV.units) == "MAD", "CV = VA-CR et SV = VA-VP sont en MAD",
    f"CV {CV.magnitude:.0f} · SV {SV.magnitude:.0f}")
EAC = (BAC / CPI).to(u.MAD)
dit(str(EAC.units) == "MAD", "EAC = BAC/CPI est en MAD", f"{EAC.magnitude:.0f} MAD")
cout_zone = _tp["cout_zone"]["total_fournitures_et_mise_en_oeuvre_MAD"] * u.MAD
avancement = (VA / cout_zone).to(u.dimensionless)
dit(avancement.dimensionless, "avancement en zones = VA / cout de zone",
    f"{avancement.magnitude:.3f} zones")
_poste = next(x for x in _va["recoupement_physique"]["postes"] if x["poste"] == "beton_m3")
releve = _poste["releve"] * u.m**3
theorique = _poste["attendu_par_le_reseau"] * u.m**3
ecart = ((releve - theorique) / theorique).to(u.dimensionless)
dit(ecart.dimensionless, "ecart de recoupement = (releve - theorique) / theorique",
    f"{ecart.magnitude * 100:+.2f} %")

leve("CPI calcule avec un cout realise en jours", lambda: (VA / (30 * u.day)).to(u.dimensionless))
leve("SV additionne a une duree", lambda: (SV + 1 * u.day).to(u.MAD))
leve("recoupement entre un m3 et un m2", lambda: ((releve - 1 * u.m**2) / theorique).to(u.dimensionless))

# ---------------------------------------------------------------- ferraillage.py (B3e)
print("\nferraillage.py — metre d'un plan de ferraillage")
_fe = json.loads((SORTIES / "ferraillage.json").read_text(encoding="utf-8"))
import math
rho = d["armatures"]["conventions"]["masse_volumique_acier_kg_m3"] * u.kg / u.m**3
dia = _fe["nomenclature"]["lignes"][0]["dia_mm"] * u.mm
# l. 38 de ferraillage.py : m = pi/4 x d^2 x rho
ml = (math.pi / 4 * dia**2 * rho).to(u.kg / u.m)
dit(str(ml.units) == "kilogram / meter", "masse lineique = pi/4 d^2 rho est en kg/m",
    f"HA{dia.magnitude:.0f} = {ml.magnitude:.3f} kg/m")
# l. 60 : longueur developpee = droite + somme des retours
Ld = (_fe["nomenclature"]["lignes"][0]["longueur_unitaire_m"] * u.m)
Lrec = (_fe["nomenclature"]["longueur_de_recouvrement_utilisee_m"] * u.m)
Lf = (Ld + _fe["nomenclature"]["lignes"][0]["recouvrements_par_barre"] * Lrec).to(u.m)
dit(str(Lf.units) == "meter", "longueur faconnee = droite + n x recouvrement est en m",
    f"{Lf.magnitude:.2f} m")
# masse d'un repere = longueur totale x masse lineique
masse = (Lf * _fe["nomenclature"]["lignes"][0]["nombre"] * ml).to(u.kg)
dit(str(masse.units) == "kilogram", "masse d'un repere = longueur totale x masse lineique",
    f"{masse.magnitude:.1f} kg")
# l. 180 : barres par metre = 100 / espacement -> en 1/m
esp = _fe["nappes"]["lignes"][0]["espacement_cm"] * u.cm
bpm = (1 / esp).to(1 / u.m)
dit(str(bpm.units) == "1 / meter", "barres par metre = 1 / espacement est en m^-1",
    f"{bpm.magnitude:.2f} /m")
# ratio kg/m3 : masse d'acier sur volume de beton
beton = _fe["deux_voies"]["elements"][0]["beton_m3"] * u.m**3
ratio = (_fe["deux_voies"]["elements"][0]["voie_A_kg"] * u.kg / beton).to(u.kg / u.m**3)
dit(str(ratio.units) == "kilogram / meter ** 3", "ratio d'acier = masse / volume de beton",
    f"{ratio.magnitude:.0f} kg/m3")
# perimetre du cadre : 2 (b + h), en m
c = _fe["cadres"]["section_axe_cadre_m"]
per = (2 * (c["b"] * u.m + c["h"] * u.m)).to(u.m)
dit(str(per.units) == "meter", "perimetre du cadre = 2 (b + h) est en m",
    f"{per.magnitude:.3f} m")

leve("masse lineique calculee avec un diametre au carre oublie",
     lambda: (math.pi / 4 * dia * rho).to(u.kg / u.m))
leve("ratio d'acier rapporte a une surface",
     lambda: (masse / (360 * u.m**2)).to(u.kg / u.m**3))
leve("longueur faconnee additionnee a une masse", lambda: (Lf + masse).to(u.m))

print("\nVerification dimensionnelle : " + ("tout est homogene." if ok else "AU MOINS UNE FORMULE EST FAUSSE."))
sys.exit(0 if ok else 1)
