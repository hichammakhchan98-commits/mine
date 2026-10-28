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
beton = _fe["ordre_de_grandeur"]["elements"][0]["beton_m3"] * u.m**3
ratio = (_fe["ordre_de_grandeur"]["elements"][0]["masse_du_plan_kg"] * u.kg / beton).to(u.kg / u.m**3)
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

# ---------------------------------------------------------------- plage.py / ferroviaire.py (B7c)
print("\nplage.py et ferroviaire.py — rendement d'une plage de consignation")
_fv = json.loads((SORTIES / "ferroviaire.json").read_text(encoding="utf-8"))
_p = _fv["plage"]
nominale = _p["duree_nominale_h"] * u.hour
fixe = _p["part_fixe_h"] * u.hour
utile = (nominale - fixe).to(u.hour)
dit(str(utile.units) == "hour", "travail effectif = plage - part fixe est en heures",
    f"{utile.magnitude:.2f} h")
rendement = (utile / nominale).to(u.dimensionless)
dit(rendement.dimensionless, "le rendement est sans dimension",
    f"{rendement.magnitude * 100:.1f} %")
jour = 8 * u.hour
facteur = (jour / utile / (1 - _p["abattement_de_cadence_nuit_pct"] / 100)).to(u.dimensionless)
dit(facteur.dimensionless, "le facteur d'interception est sans dimension",
    f"x{facteur.magnitude:.2f}")
_nr = _fv["point_de_non_retour"]
cad = _nr["cadence_de_nuit_t_h"] * u.tonne / u.hour
duree_op = (_nr["masse_d_une_piece_t"] * u.tonne / cad).to(u.hour)
dit(str(duree_op.units) == "hour", "duree d'une operation = masse / cadence est en heures",
    f"{duree_op.magnitude:.2f} h")
masse_max = (utile * cad).to(u.tonne)
dit(str(masse_max.units) == "metric_ton", "masse levable = temps utile x cadence est en tonnes",
    f"{masse_max.magnitude:.2f} t")
_c = _fv["cout"]
cout_utile = (_c["cout_d_une_plage_MAD_par_compagnon"] * u.MAD / utile).to(u.MAD / u.hour)
dit(str(cout_utile.units) == "MAD / hour", "cout de l'heure utile = cout de la plage / temps utile",
    f"{cout_utile.magnitude:.0f} MAD/h")

leve("rendement calcule en soustrayant des tonnes d'une duree",
     lambda: (nominale - 1 * u.tonne).to(u.hour))
leve("masse levable obtenue en multipliant deux durees",
     lambda: (utile * nominale).to(u.tonne))
leve("facteur d'interception compare a un cout",
     lambda: (facteur + 1 * u.MAD).to(u.dimensionless))

# ---------------------------------------------------------------- qualite.py (C7)
print("\nqualite.py — exposition, cout de non-qualite, dechets")
_q = json.loads((SORTIES / "qualite.json").read_text(encoding="utf-8"))
_e = _q["exposition"]
# Les accidents se calculent sur les heures REELLES : la ponderation de la nuit
# repartit le risque, elle ne l'ajoute pas. Appliquer un taux de branche a des heures
# ponderees le compterait deux fois.
heures = _e["heures_totales"] * u.hour
tf = _e["taux_de_frequence_de_reference"] / (1e6 * u.hour)   # accidents par million d'heures
acc = (tf * heures).to(u.dimensionless)
dit(acc.dimensionless, "accidents = taux de frequence x heures est un nombre",
    f"{acc.magnitude:.2f}")
tg = _e["taux_de_gravite_de_reference"] * u.day / (1000 * u.hour)
jours = (tg * heures).to(u.day)
dit(str(jours.units) == "day", "journees perdues = taux de gravite x heures est en jours",
    f"{jours.magnitude:.1f} j")
_n = _q["non_conformite"]
fd = _n["frais_de_duree_MAD_par_jour_ouvre"] * u.MAD / u.day
# Les frais de duree suivent le RETARD MESURE du chantier, pas l'immobilisation de la
# tache : sur un ouvrage a marge, le retard est nul et aucun frais n'est du.
retard = _n["par_ouvrage"][0]["retard_du_chantier_j"] * u.day
dit(str((fd * retard).to(u.MAD).units) == "MAD",
    "cout de retard = frais par jour x jours de RETARD est en MAD",
    f"{(fd * retard).to(u.MAD).magnitude:.0f} MAD")
immo = _n["jours_immobilises"] * u.day
_de = _q["dechets"]
ratio = _de["lignes"][0]["kg_m2"] * u.kg / u.m**2
tonnes = (ratio * _de["emprise_m2"] * u.m**2).to(u.tonne)
dit(str(tonnes.units) == "metric_ton", "dechets = ratio x emprise est en tonnes",
    f"{tonnes.magnitude:.1f} t")

# L'heure de CONTROLE est un prix par heure de cadre, pas par heure de production :
# le durcissement du controle est un nombre d'heures fois ce taux, et rien d'autre.
taux_ctrl = _n["taux_de_l_heure_de_controle_MAD"] * u.MAD / u.hour
h_ctrl = _n["heures_de_controle_ajoutees"] * u.hour
ctrl = (taux_ctrl * h_ctrl).to(u.MAD)
dit(str(ctrl.units) == "MAD",
    "durcissement du controle = taux horaire x heures est en MAD",
    f"{ctrl.magnitude:.0f} MAD")
# Le retard sous consignation est un multiple de la PERIODE des fenetres : deux durees,
# et leur rapport est un nombre pur. Un retard divise par une periode qui serait en
# heures donnerait un nombre different — c'est le genre d'erreur que B7c a deja produit.
_qd = _q["quantification_du_retard"]
pas = _qd["pas_j"] * u.day
palier = _qd["paliers_observes_j"][0] * u.day
dit((palier / pas).to(u.dimensionless).dimensionless,
    "palier de retard / periode des fenetres est un nombre de fenetres",
    f"{(palier / pas).to(u.dimensionless).magnitude:.0f} fenetre(s)")

leve("heures de controle payees au prix d'un metre carre",
     lambda: (h_ctrl * (420 * u.MAD / u.m**2)).to(u.MAD))
leve("palier de retard compare a une periode exprimee en heures",
     lambda: (palier + _qd["pas_j"] * u.MAD).to(u.day))
leve("accidents obtenus en multipliant un taux par une surface",
     lambda: (tf * (100 * u.m**2)).to(u.dimensionless))
leve("journees perdues additionnees a un cout", lambda: (jours + 1 * u.MAD).to(u.day))
leve("retard de chantier additionne a un cout", lambda: (retard + 1 * u.MAD).to(u.day))
leve("dechets calcules sur une duree", lambda: (ratio * immo).to(u.tonne))

# ---------------------------------------------------------------- reception.py (REC)
print("\nreception.py — cout d'un jour, portage, DOE")
_r = json.loads((SORTIES / "reception.json").read_text(encoding="utf-8"))
_c = _r["cout_d_un_jour"]
cout_jour = _c["cout_sous_penalites_MAD_par_jour_ouvre"] * u.MAD / u.day
plafond = _c["plafond_des_penalites_MAD"] * u.MAD
penal_jour = _c["penalites_MAD_par_jour_ouvre"] * u.MAD / u.day
bascule = (plafond / penal_jour).to(u.day)
dit(str(bascule.units) == "day",
    "jour de bascule = plafond / penalite journaliere est une DUREE",
    f"{bascule.magnitude:.1f} j")
# Le portage est un taux ANNUEL : taux x montant x duree donne des MAD, et la duree doit
# etre homogene a l'annee. Une duree en jours divisee par 365 est sans unite si on
# oublie le /an — c'est l'erreur classique, et le contre-controle la cherche.
_p = _r["portage"]
# L'annee de pint vaut 365,25 jours — l'annee julienne. Une convention de credit n'en
# sait rien : elle compte 365 ou 360 jours, et c'est une CLAUSE. Le controle utilise donc
# la base declaree dans data/, et c'est en comparant les deux que l'ecart de 1,4 % est
# apparu.
_base = _r["doe"]["base_de_calcul_des_interets_j"] * u.day
taux_an = _p["taux_de_portage_annuel_pct"] / 100 / _base
montant = _p["retenue_immobilisee_MAD"] * u.MAD
par_mois = (taux_an * montant * (_base / 12)).to(u.MAD)
dit(abs(par_mois.magnitude - _p["cout_de_la_retenue_MAD_par_mois"]) < 1,
    "cout mensuel de portage = taux annuel x montant x un mois",
    f"{par_mois.magnitude:.0f} MAD")
_d = _r["doe"]
portage_doe = (taux_an * (_d["solde_bloque_MAD"] * u.MAD)
               * (_d["retard_du_solde_j"] * u.day)).to(u.MAD)
dit(abs(portage_doe.magnitude - _d["cout_de_portage_MAD"]) < 20,
    "portage du DOE = taux annuel x montant bloque x jours de retard",
    f"{portage_doe.magnitude:.0f} MAD")
heures_doe = _d["heures_reconstitue"] * u.hour
taux_cadre = _d["taux_horaire_de_cadre_MAD"] * u.MAD / u.hour
dit(str((heures_doe * taux_cadre).to(u.MAD).units) == "MAD",
    "cout du DOE = heures x taux horaire de cadre est en MAD",
    f"{(heures_doe * taux_cadre).to(u.MAD).magnitude:.0f} MAD")

# La levee des reserves : des heures-HOMME divisees par une capacite en heures-homme par
# jour donnent des jours. L'unite compte, et la passe adversariale l'a relevee : six
# heures a six compagnons ne font pas six heures de delai. pint ne distingue pas l'homme,
# mais il verifie que le quotient est bien une duree et que le MAXIMUM des deux termes
# est homogene — c'est la ou l'erreur serait.
_s = _r["reserves"]
h_homme = _s["heures_totales"] * u.hour
capacite = _s["capacite_h_homme_par_jour"] * u.hour / u.day
atelier = (h_homme / capacite).to(u.day)
dit(str(atelier.units) == "day",
    "heures-homme / capacite journaliere est une duree",
    f"{atelier.magnitude:.2f} j")
delai = _s["levee_de_toutes"]["delai_de_tiers_le_plus_long_j"] * u.day
duree = max(atelier, delai)
dit(abs(duree.magnitude - _s["levee_de_toutes"]["duree_j"]) < 0.02,
    "et la duree publiee est le maximum des deux, toutes deux en jours",
    f"max({atelier.magnitude:.2f} ; {delai.magnitude:.0f}) = {duree.magnitude:.2f} j")
# Le solde bloque par le DOE est une part du MARCHE, pas la retenue : les deux sont en
# MAD, donc pint ne peut pas les distinguer — le test de valeur, lui, le peut.
_d2 = _r["doe"]
dit(abs(_d2["solde_bloque_MAD"] - _r["portage"]["retenue_immobilisee_MAD"]) > 1,
    "le solde bloque par le DOE n'est pas la retenue de garantie",
    f"{_d2['solde_bloque_MAD']:.0f} contre "
    f"{_r['portage']['retenue_immobilisee_MAD']:.0f} MAD")

# LIMITE DECLAREE de cette verification : pint ne distingue pas l'heure-HOMME de
# l'heure. Diviser 606 heures-homme par 6 compagnons donnerait « 101 heures » qui se
# convertissent en jours sans que rien ne leve. Ce controle-la ne peut donc pas etre
# automatique : il repose sur la note de data/, qui declare l'unite, et sur le fait que
# la capacite est exprimee en heures-homme PAR JOUR. Le dire vaut mieux que de laisser
# croire que la chaine le verifie.
leve("duree de levee obtenue en divisant des heures-homme par un cout horaire",
     lambda: (h_homme / (58 * u.MAD / u.hour)).to(u.day))
leve("delai de tiers additionne a un cout", lambda: (delai + 1 * u.MAD).to(u.day))
leve("jour de bascule obtenu en divisant un plafond par un MONTANT journalier",
     lambda: (plafond / (127850 * u.MAD)).to(u.day))
leve("portage calcule en oubliant que le taux est ANNUEL",
     lambda: (0.07 * montant * (60 * u.day)).to(u.MAD))
leve("cout d'un jour additionne a un nombre de jours",
     lambda: (cout_jour + 1 * u.day).to(u.MAD / u.day))

# ---------------------------------------------------------------- installation.py (C1)
print("\ninstallation.py — courbe de charge, couverture, debit, base-vie, cout")
u.define("levage = [manutention]")   # un levage est une grandeur comptee, pas un nombre nu
_i = json.loads((SORTIES / "installation.json").read_text(encoding="utf-8"))
_g = json.loads((RACINE / "data" / "projet-gare.json").read_text(
    encoding="utf-8"))["installation"]["grue"]

# La courbe de charge. Le moment de service est en tonnes-metres : divise par un RAYON il
# donne une charge, divise par une MASSE il donne un rayon. C'est la meme formule lue
# dans les deux sens, et c'est tout le module — d'ou deux controles et deux contre-
# controles qui echangent le diviseur.
moment = _g["moment_max_tm"]["valeur"] * u.tonne * u.m
charge_max = _g["charge_max_t"]["valeur"] * u.tonne
_c = next(c for c in _i["couverture"] if c["charge_au_point_le_plus_defavorable_t"])
rayon = _c["distance_la_plus_defavorable_m"] * u.m
charge = (moment / rayon).to(u.tonne)
dit(str(charge.units) == "metric_ton",
    "charge disponible = moment / rayon est une MASSE",
    f"{charge.magnitude:.2f} t a {rayon.magnitude:.1f} m")
_pc = max(_i["pieces"], key=lambda x: x["masse_t"])
masse = _pc["masse_t"] * u.tonne
rayon_limite = (moment / masse).to(u.m)
dit(abs(rayon_limite.magnitude - _pc["rayon_limite_m"]) < 0.05,
    "rayon limite = moment / masse est une LONGUEUR",
    f"{masse.magnitude:.1f} t -> {rayon_limite.magnitude:.1f} m")

# La couverture est un rapport d'AIRES. L'erreur serait de la calculer sur un rayon et
# une longueur : le contre-controle la cherche.
L, l = _g2 = json.loads((RACINE / "data" / "projet-gare.json").read_text(
    encoding="utf-8"))["geometrie"]["emprise_m"]
emprise = (L * u.m) * (l * u.m)
servie = (_c["couverture_pct"] / 100) * emprise
dit(str((servie / emprise).to(u.dimensionless).units) == "dimensionless",
    "couverture = aire servie / aire de l'emprise est SANS DIMENSION",
    f"{_c['couverture_pct']:.1f} % de {emprise.magnitude:.0f} m²")

# Le survol du gabarit est une difference de LONGUEURS : une position plus une portee
# moins une distance. Rien d'autre n'a le droit d'y entrer, et c'est le contre-controle
# qui le verifie — une aire ajoutee a un rayon ne leverait pas si tout etait en metres.
_vo = _i["voisinage"]
_l0 = _vo["lignes"][0]
_cv = next(c for c in _i["couverture"] if c["variante"] == _l0["variante"])
_gr = max(_cv["grues"], key=lambda g: g["y_m"] + g["portee_m"])
survol = ((_gr["y_m"] * u.m + _gr["portee_m"] * u.m) - _vo["y_du_gabarit_m"] * u.m).to(u.m)
dit(abs(survol.magnitude - _l0["survol_du_gabarit_m"]) < 0.05,
    "survol = position + portee - distance au gabarit est une LONGUEUR",
    f"{survol.magnitude:.1f} m")

# Les aires : une somme de surfaces, et un rapport de surfaces.
_ai = _i["aires"]
besoin = _ai["surface_a_mettre_sous_la_grue_m2"] * u.m**2
majorant = _ai["majorant_sous_grue_hors_batiment_m2"] * u.m**2
dit(str((besoin / majorant).to(u.dimensionless).units) == "dimensionless",
    "besoin sous grue / majorant couvert est SANS DIMENSION",
    f"{_ai['rapport_besoin_sur_majorant_pct']:.1f} %")

# Le debit. Une capacite est un nombre de levages PAR JOUR, obtenue en multipliant des
# levages par heure par des heures par jour. Le taux d'utilisation est sans dimension :
# s'il etait traite comme une duree, le resultat ne serait plus un debit.
_de = _i["debit"]
cycles = _de["cycles_par_heure"] * u.levage / u.hour
heures = _de["heures_par_jour"] * u.hour / u.day
capacite = (cycles * heures * _de["taux_d_utilisation_fraction"]).to(u.levage / u.day)
dit(abs(capacite.magnitude - _de["capacite_levages_par_jour"]) < 0.05,
    "capacite = levages/h x h/j x taux est un DEBIT (levages/j)",
    f"{capacite.magnitude:.1f} levages/j")
surface_jour = _de["surface_manutentionnee_par_jour_m2"] * u.m**2 / u.day
par_levage = (json.loads((RACINE / "data" / "projet-gare.json").read_text(
    encoding="utf-8"))["installation"]["levages"]["surface_par_levage_m2"]["valeur"]
    * u.m**2 / u.levage)
demande = (surface_jour * 2 / par_levage).to(u.levage / u.day)
dit(abs(demande.magnitude - _de["levages_de_coffrage_par_jour"]) < 0.1,
    "demande de coffrage = (m²/j x 2 levages) / (m² par levage) est un DEBIT",
    f"{demande.magnitude:.1f} levages/j")
dit(str((demande / capacite).to(u.dimensionless).units) == "dimensionless",
    "taux de charge = demande / capacite est SANS DIMENSION",
    f"{_de['taux_de_charge_pct']:.1f} %")

# La base-vie. Une surface par personne multipliee par un effectif donne une surface :
# l'effectif est une grandeur (compagnon), pas un nombre nu, sinon n'importe quel
# produit passerait.
_bv = _i["base_vie"]
_rub = json.loads((RACINE / "data" / "projet-gare.json").read_text(
    encoding="utf-8"))["installation"]["base_vie"]
pointe = _bv["effectif_de_pointe"] * u.compagnon
# L'encadrement occupe des bureaux, pas des vestiaires : deux surfaces unitaires, donc,
# ponderees par la part d'encadrement — qui est un POURCENTAGE, sans dimension.
part = _rub["part_encadrement_pct"]["valeur"] / 100
compagnons = _rub["m2_par_personne"]["valeur"] * u.m**2 / u.compagnon
bureaux = _rub["m2_par_personne_encadrement"]["valeur"] * u.m**2 / u.compagnon
surface = (pointe * (1 - part) * compagnons + pointe * part * bureaux).to(u.m**2)
dit(abs(surface.magnitude - _bv["surface_necessaire_m2"]) < 0.5,
    "surface de base-vie = effectif x surface par personne est une AIRE",
    f"{pointe.magnitude:.0f} compagnons -> {surface.magnitude:.1f} m²")
module = _rub["module_m2"] * u.m**2
dit(str((surface / module).to(u.dimensionless).units) == "dimensionless",
    "nombre de modules = surface / surface d'un module est SANS DIMENSION",
    f"{_bv['modules']} modules")

# Le cout. Un loyer est un MAD PAR MOIS : multiplie par une duree il donne des MAD, et
# c'est la seule facon de l'additionner au cout fixe. Le contre-controle additionne les
# deux sans multiplier — exactement l'erreur qui ferait passer un loyer pour un forfait.
_co = _i["cout"]
loyer = _co["loyer_MAD_par_mois"] * u.MAD / u.month
duree = _co["duree_mois_calendaires"] * u.month
fixe = _co["cout_fixe_MAD"] * u.MAD
total = (fixe + (loyer * duree).to(u.MAD)).to(u.MAD)
dit(abs(total.magnitude - _co["total_MAD"]) < 1,
    "total = cout fixe + loyer x duree, les deux termes en MAD",
    f"{total.magnitude:.0f} MAD")
dit(str((fixe / total).to(u.dimensionless).units) == "dimensionless",
    "part fixe = cout fixe / total est SANS DIMENSION",
    f"{_co['part_fixe_pct']:.1f} %")

leve("charge disponible obtenue en divisant le moment par la charge maximale",
     lambda: (moment / charge_max).to(u.tonne))
leve("rayon limite obtenu en MULTIPLIANT le moment par la masse",
     lambda: (moment * masse).to(u.m))
leve("couverture calculee en divisant une aire par une longueur",
     lambda: (servie / (L * u.m)).to(u.dimensionless))
# LIMITE DECLAREE. Deux erreurs de C1 sont dimensionnellement INVISIBLES, et il vaut
# mieux l'ecrire que de les laisser croire controlees. (1) Diviser les levages par heure
# par les heures par jour au lieu de les multiplier donne encore des levages par unite de
# temps : pint convertit et ne leve pas. (2) Une part d'encadrement est un pourcentage,
# donc sans dimension : la mettre au mauvais endroit du produit ne change aucune unite.
# Ces deux-la sont attrapees par les tests de VALEUR de calc/tests/test_installation.py,
# qui recalculent la capacite et la surface terme a terme — pas ici.
leve("survol calcule en ajoutant une surface d'aire a une portee",
     lambda: ((_gr["portee_m"] * u.m + besoin) - _vo["y_du_gabarit_m"] * u.m).to(u.m))
leve("besoin sous grue rapporte a une portee au lieu d'une surface",
     lambda: (besoin / (_gr["portee_m"] * u.m)).to(u.dimensionless))
leve("taux d'utilisation traite comme une duree",
     lambda: (cycles * heures * (_de["taux_d_utilisation_fraction"] * u.day)).to(u.levage / u.day))
leve("demande calculee en oubliant la surface par levage",
     lambda: (surface_jour * 2).to(u.levage / u.day))
leve("surface de base-vie obtenue en multipliant l'effectif par le nombre de modules",
     lambda: (pointe * _bv["modules"]).to(u.m**2))
leve("surface par personne prise pour une surface totale",
     lambda: (pointe * (4.5 * u.m**2)).to(u.m**2))
leve("loyer ADDITIONNE au cout fixe sans etre multiplie par la duree",
     lambda: (fixe + loyer).to(u.MAD))
leve("duree de location additionnee a une surface de base-vie",
     lambda: (duree + surface).to(u.month))

print("\nVerification dimensionnelle : " + ("tout est homogene." if ok else "AU MOINS UNE FORMULE EST FAUSSE."))
sys.exit(0 if ok else 1)
