"""Etalonnage de calc/pilotage.py sur des cas a solution fermee (§ 3.3).

Une bibliotheque qui agrege doit etre verifiee sur les cas ou l'agregation a une solution
exacte, et sur les INVARIANTS qui la caracterisent. Les trois lois de ce module en ont :

1. quand deux sites ont depense exactement autant, le CPI consolide EST la moyenne des
   CPI — c'est le seul cas ou l'erreur courante est juste, et il borne le probleme ;
2. deplacer le CPI d'un site de delta deplace le consolide de delta x poids, exactement ;
3. la latence vaut une demi-periode quand le delai de remontee est nul, et le retard
   quantise est la fonction plafond, dont les points de rupture sont connus.
"""
from __future__ import annotations
import json, math, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))
import pilotage as pil                                                   # noqa: E402

echecs = []


def cas(nom, obtenu, attendu, tol, unite=""):
    ok = abs(obtenu - attendu) <= tol
    if not ok:
        echecs.append(nom)
    print(f"  {'ok  ' if ok else 'ECHEC'} {nom} — {obtenu:.6f} contre {attendu:.6f} {unite}")


def _site(nom, va, cr, vp=None, bac=None):
    return {"site": nom, "id": nom, "role": "",
            "budget_a_l_achevement_BAC_MAD": bac or cr * 2,
            "valeur_planifiee_VP_MAD": vp or va,
            "valeur_acquise_VA_MAD": va, "cout_reel_CR_MAD": cr,
            "CPI": round(va / cr, 4), "SPI": 1.0,
            "derive_MAD": cr - va, "avancement_physique_pct": 0.0,
            "EAC_si_la_derive_persiste_MAD": (bac or cr * 2) / (va / cr)}


SEUILS = {"vigilance_CPI": 0.95, "alerte_CPI": 0.85}

print("=== 1. Le seul cas ou la moyenne des CPI est juste ===")
# Deux sites qui ont depense EXACTEMENT autant : les deux formules coincident.
a = pil.consolidation([_site("A", 900, 1000), _site("B", 800, 1000)], SEUILS)
cas("a couts reels egaux, le consolide EST la moyenne des CPI",
    a["CPI_consolide"], a["moyenne_des_CPI"], 1e-9)
cas("et il vaut (0,90 + 0,80) / 2", a["CPI_consolide"], 0.85, 1e-9)

print("\n=== 2. La loi d'amortissement, exactement ===")
# Un site qui pese w du cout reel : bouger son CPI de delta bouge le consolide de w.delta.
cr_a, cr_b = 9000.0, 1000.0
base = pil.consolidation([_site("A", 0.9 * cr_a, cr_a), _site("B", 0.8 * cr_b, cr_b)],
                         SEUILS)
delta = 0.10
bouge = pil.consolidation([_site("A", 0.9 * cr_a, cr_a),
                           _site("B", (0.8 - delta) * cr_b, cr_b)], SEUILS)
w = cr_b / (cr_a + cr_b)
cas("deplacer le CPI du petit site de 0,10 deplace le consolide de 0,10 x son poids",
    base["CPI_consolide"] - bouge["CPI_consolide"], delta * w, 1e-9)
cas("et l'amortissement publie est bien l'inverse du poids",
    base["poids"][1]["amortissement"], 1 / w, 0.05)
# INVARIANT : un site de poids nul ne deplace rien. On s'en approche par la limite.
loin = pil.consolidation([_site("A", 0.9 * 1e6, 1e6), _site("B", 0.1, 1.0)], SEUILS)
cas("un site de poids negligeable ne deplace pas le consolide",
    loin["CPI_consolide"], 0.9, 1e-5)

print("\n=== 3. Le seuil de masquage, forme fermee ===")
# va_B = s.(CR_A + CR_B) - VA_A, donc le CPI limite s'ecrit exactement.
sites_ = [_site("A", 0.9 * cr_a, cr_a), _site("B", 0.8 * cr_b, cr_b)]
cons = pil.consolidation(sites_, SEUILS)
m = pil.seuil_de_masquage(sites_, cons)
attendu = (m["seuil_retenu_CPI"] * (cr_a + cr_b) - 0.9 * cr_a) / cr_b
cas("le CPI limite du petit site suit sa forme fermee",
    m["CPI_du_site_au_seuil_consolide"], attendu, 1e-4)
# INVARIANT : si le seuil EGALE le consolide actuel, la derive invisible est nulle.
cons2 = pil.consolidation(sites_, {"vigilance_CPI": 0.999,
                                   "alerte_CPI": cons["CPI_consolide"]})
m2 = pil.seuil_de_masquage(sites_, cons2)
cas("au seuil exactement atteint, il ne reste aucune derive invisible",
    m2["derive_supplementaire_invisible_MAD"], 0.0, 1.0, "MAD")

print("\n=== 4. La latence, et le retard quantise ===")
d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
rec = json.loads((RACINE / "calc" / "sorties" / "reception.json").read_text(encoding="utf-8"))
d0 = json.loads(json.dumps(d))
d0["multi_sites"]["reporting"]["delai_de_remontee_j"]["valeur"] = 0
l0 = pil.latence(d0, rec)
cas("sans delai de remontee, la latence vaut une demi-periode",
    l0["lignes"][1]["latence_moyenne_j"],
    d["multi_sites"]["reporting"]["periode_mensuelle_j"]["valeur"] / 2, 1e-9, "j")
cas("et l'ecart des deux rythmes ne depend PAS du delai de remontee",
    l0["ecart_des_deux_rythmes_j"], pil.latence(d, rec)["ecart_des_deux_rythmes_j"], 1e-9)

per = d["planning"]["contraintes_exploitation"]["periode_entre_fenetres_jours"]["valeur"]
dq = json.loads(json.dumps(d))
for retard, attendu_cycles in ((1, 1), (per - 1, 1), (per, 1), (per + 1, 2), (2 * per, 2)):
    dq["multi_sites"]["sites"][1]["retard_constate_j"]["valeur"] = retard
    a_ = pil.alerte_ferroviaire(dq)
    cas(f"retard de {retard} j -> {attendu_cycles} cycle(s)",
        a_["cycles_perdus"], attendu_cycles, 1e-9)
# INVARIANT : juste avant une marche, un jour gagne en vaut une periode entiere.
dq["multi_sites"]["sites"][1]["retard_constate_j"]["valeur"] = per + 1
avant = pil.alerte_ferroviaire(dq)["retard_effectif_j"]
dq["multi_sites"]["sites"][1]["retard_constate_j"]["valeur"] = per
apres = pil.alerte_ferroviaire(dq)["retard_effectif_j"]
cas("un jour gagne au bon moment vaut une periode entiere", avant - apres, per, 1e-9, "j")

print("\n=== 5. Le jeu REEL du projet ===")
r = pil.tout_calculer(d)
c = r["consolidation"]
cas("le consolide est entre les deux CPI de site",
    1.0 if min(s["CPI"] for s in r["sites"]) <= c["CPI_consolide"]
    <= max(s["CPI"] for s in r["sites"]) else 0.0, 1.0, 1e-9)
cas("la somme des derives de site egale la derive consolidee",
    sum(s["derive_MAD"] for s in r["sites"]), c["derive_totale_MAD"], 1.0, "MAD")

print()
if echecs:
    print(f"ETALONNAGE ECHOUE : {len(echecs)} cas — {', '.join(echecs)}")
    sys.exit(1)
print("Etalonnage pilotage : tous les cas fermes sont verifies.")
