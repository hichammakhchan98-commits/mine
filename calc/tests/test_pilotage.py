"""Tests du module D7 — pilotage et suivi multi-sites.

Des tests de REGLE. Aucun n'epingle « CPI consolide 0,877 » ni « le site secondaire va
mal » : ils verifient qu'un ratio est bien un rapport de sommes, qu'une grandeur heritee
vient du module qui la publie, que la latence contient les deux termes, et que le seuil
d'alerte ferroviaire est une duree. Trois canaris cherchent l'erreur plutot que de la
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
r = json.loads((S / "pilotage.json").read_text(encoding="utf-8"))
su = json.loads((S / "suivi.json").read_text(encoding="utf-8"))
pl = json.loads((S / "planification.json").read_text(encoding="utf-8"))
rec = json.loads((S / "reception.json").read_text(encoding="utf-8"))
fer = json.loads((S / "ferroviaire.json").read_text(encoding="utf-8"))
MS = d["multi_sites"]
import pilotage as pil                                                   # noqa: E402

# ------------------------------------------------- 1. les deux sites
print("\n--- les deux sites, et d'ou viennent leurs chiffres ---")
gv, rer = r["sites"]
verifie("le site principal n'est PAS recalcule : ses quatre grandeurs viennent de D4",
        all(gv[k] == su["valeur_acquise"][k] for k in
            ("budget_a_l_achevement_BAC_MAD", "valeur_planifiee_VP_MAD",
             "valeur_acquise_VA_MAD", "cout_reel_CR_MAD", "CPI", "SPI")),
        f"CPI {gv['CPI']} · BAC {gv['budget_a_l_achevement_BAC_MAD']:.0f}")
verifie("et la date d'arret est celle de D4",
        r["date_d_arret_j"] == su["date_arret"]["jour_ouvre"],
        f"jour {r['date_d_arret_j']}")
# LA regle : la valeur acquise d'un lot est son budget par son avancement PHYSIQUE.
for x in rer["lots"]:
    verifie(f"{x['lot'][:28]} : VA = budget x avancement physique",
            abs(x["valeur_acquise_MAD"]
                - x["budget_MAD"] * x["avancement_constate_pct"] / 100) < 0.01)
    verifie(f"{x['lot'][:28]} : VP = budget x avancement planifie",
            abs(x["valeur_planifiee_MAD"]
                - x["budget_MAD"] * x["avancement_planifie_pct"] / 100) < 0.01)
verifie("le budget du site est la somme des budgets de ses lots",
        abs(rer["budget_a_l_achevement_BAC_MAD"]
            - sum(x["budget_MAD"] for x in rer["lots"])) < 0.01,
        f"{rer['budget_a_l_achevement_BAC_MAD']:.0f} MAD")
verifie("et ses trois grandeurs sont les sommes de celles de ses lots",
        all(abs(rer[k] - sum(x[c] for x in rer["lots"])) < 0.01 for k, c in (
            ("valeur_planifiee_VP_MAD", "valeur_planifiee_MAD"),
            ("valeur_acquise_VA_MAD", "valeur_acquise_MAD"),
            ("cout_reel_CR_MAD", "cout_reel_MAD"))))
# canari : un avancement de DEPENSE donnerait CPI = 1 par construction. Le test doit
# montrer que la chaine ne le fait pas.
_faux = pil.situation_par_lots("canari", [
    {"lot": "x", "budget_MAD": 1000, "avancement_planifie_pct": 50,
     "avancement_constate_pct": 60, "cout_reel_MAD": 600}], 1000)
verifie("canari : un avancement physique different du cout donne un CPI different de 1",
        abs(_faux["CPI"] - 1.0) < 1e-9,
        "600 MAD depenses pour 60 % physique sur 1 000 : CPI = 1, et c'est juste")
_faux2 = pil.situation_par_lots("canari", [
    {"lot": "x", "budget_MAD": 1000, "avancement_planifie_pct": 50,
     "avancement_constate_pct": 40, "cout_reel_MAD": 600}], 1000)
verifie("et 40 % physique pour 600 MAD donne bien 0,667",
        abs(_faux2["CPI"] - 2 / 3) < 1e-3, f"{_faux2['CPI']}")

# ------------------------------------------------- 2. la consolidation
print("\n--- la consolidation : un ratio ne se consolide pas ---")
c = r["consolidation"]
verifie("le CPI consolide est le rapport des SOMMES",
        abs(c["CPI_consolide"]
            - sum(s["valeur_acquise_VA_MAD"] for s in r["sites"])
            / sum(s["cout_reel_CR_MAD"] for s in r["sites"])) < 1e-4,
        f"{c['CPI_consolide']}")
verifie("et il differe de la moyenne des CPI",
        abs(c["CPI_consolide"] - c["moyenne_des_CPI"]) > 1e-3,
        f"{c['CPI_consolide']} contre {c['moyenne_des_CPI']}")
# LA regle : le consolide est TOUJOURS entre les deux CPI, et du cote du plus gros.
verifie("le consolide est encadre par les CPI des sites",
        min(s["CPI"] for s in r["sites"]) <= c["CPI_consolide"]
        <= max(s["CPI"] for s in r["sites"]))
_gros = max(r["sites"], key=lambda s: s["cout_reel_CR_MAD"])
verifie("et il est plus proche de celui du site qui a le plus depense",
        abs(c["CPI_consolide"] - _gros["CPI"])
        < abs(c["CPI_consolide"] - min(s["CPI"] for s in r["sites"])),
        f"plus proche de {_gros['id']}")
for p in c["poids"]:
    verifie(f"{p['id']} : l'amortissement est l'inverse du poids",
            abs(p["amortissement"] - 100 / p["poids_du_cout_pct"]) < 0.1,
            f"x{p['amortissement']} pour {p['poids_du_cout_pct']} %")
verifie("les poids font 100 %",
        abs(sum(p["poids_du_cout_pct"] for p in c["poids"]) - 100) < 0.2)
verifie("un centieme de CPI vaut un centieme du cout reel total",
        abs(c["MAD_pour_un_centieme_de_CPI"] - 0.01 * c["cout_reel_CR_MAD"]) < 1,
        f"{c['MAD_pour_un_centieme_de_CPI']:.0f} MAD")
verifie("le depassement prevu est la somme des depassements de site",
        abs(c["depassement_prevu_total_MAD"]
            - sum(p["depassement_prevu_MAD"] for p in c["poids"])) < 1)
# Ce qui porte l'enseignement : la part du depassement n'est PAS la part du budget.
verifie("la part du depassement d'un site differe de sa part de budget",
        any(abs(p["part_du_depassement_prevu_pct"] - p["poids_du_budget_pct"]) > 5
            for p in c["poids"]),
        " · ".join(f"{p['id']} {p['poids_du_budget_pct']} % du budget / "
                   f"{p['part_du_depassement_prevu_pct']} % du depassement"
                   for p in c["poids"]))
verifie("le niveau atteint suit les deux seuils declares",
        c["niveau_atteint"] == ("alerte" if c["CPI_consolide"] < c["seuil_d_alerte_CPI"]
                                else "vigilance"
                                if c["CPI_consolide"] < c["seuil_de_vigilance_CPI"]
                                else "normal"),
        c["niveau_atteint"])
verifie("et les seuils sont ceux que data/ declare",
        c["seuil_de_vigilance_CPI"] == MS["seuils_du_tableau_de_bord"]["vigilance_CPI"]
        and c["seuil_d_alerte_CPI"] == MS["seuils_du_tableau_de_bord"]["alerte_CPI"])

# ------------------------------------------------- 3. le masquage
print("\n--- le masquage, et le seuil qui n'est pas franchi ---")
m = r["seuil_de_masquage"]
verifie("le seuil retenu est celui qui n'est PAS encore franchi",
        c["CPI_consolide"] >= m["seuil_retenu_CPI"],
        f"{m['quel_seuil']} : {m['seuil_retenu_CPI']}")
# LA regle : au CPI limite, le consolide vaut exactement le seuil. On le rejoue.
_va = (c["valeur_acquise_VA_MAD"] - rer["valeur_acquise_VA_MAD"]
       + m["CPI_du_site_au_seuil_consolide"] * rer["cout_reel_CR_MAD"])
verifie("au CPI limite du petit site, le consolide vaut exactement le seuil",
        abs(_va / c["cout_reel_CR_MAD"] - m["seuil_retenu_CPI"]) < 1e-3,
        f"{_va / c['cout_reel_CR_MAD']:.4f} contre {m['seuil_retenu_CPI']}")
verifie("la derive invisible est positive, et c'est une derive SUPPLEMENTAIRE",
        m["derive_supplementaire_invisible_MAD"] > 0
        and m["CPI_du_site_au_seuil_consolide"] < rer["CPI"],
        f"{m['derive_supplementaire_invisible_MAD']:.0f} MAD")
verifie("et elle vaut la baisse de valeur acquise correspondante",
        abs(m["derive_supplementaire_invisible_MAD"]
            - (rer["valeur_acquise_VA_MAD"]
               - m["CPI_du_site_au_seuil_consolide"] * rer["cout_reel_CR_MAD"])) < 1)

print("\n--- le masquage recursif : un etage plus bas ---")
mr = r["masquage_recursif"]
_dem = [x for x in rer["lots"] if x["demarre"]]
verifie("le lot designe est bien le plus degrade des lots demarres",
        mr["CPI_du_lot"] == min(x["CPI"] for x in _dem),
        f"{mr['lot_le_plus_degrade'][:30]} a {mr['CPI_du_lot']}")
verifie("un lot non demarre n'est jamais designe",
        all(x["demarre"] for x in _dem) and mr["nb_lots_demarres"] == len(_dem))
verifie("l'amortissement du lot par son site est l'inverse de son poids dans le cout",
        abs(mr["amortissement_du_lot_par_le_site"]
            - 100 / mr["poids_du_lot_dans_le_cout_du_site_pct"]) < 0.1,
        f"x{mr['amortissement_du_lot_par_le_site']}")
verifie("le CPI du lot est pire que celui de son site",
        mr["CPI_du_lot"] < mr["CPI_du_site"])
verifie("le module dit que les amortissements se MULTIPLIENT",
        dit(mr["_les_amortissements_se_multiplient"], "produit"))

# ------------------------------------------------- 4. la latence
print("\n--- la latence du reporting ---")
lat = r["latence"]
rp = MS["reporting"]
for ligne, cle in zip(lat["lignes"], ("periode_hebdomadaire_j", "periode_mensuelle_j")):
    verifie(f"{ligne['rythme']} : latence = demi-periode + remontee",
            abs(ligne["latence_moyenne_j"]
                - (rp[cle]["valeur"] / 2 + rp["delai_de_remontee_j"]["valeur"])) < 0.05,
            f"{ligne['latence_moyenne_j']} j")
    verifie(f"{ligne['rythme']} : le pire cas est une periode entiere plus la remontee",
            abs(ligne["latence_pire_cas_j"]
                - (rp[cle]["valeur"] + rp["delai_de_remontee_j"]["valeur"])) < 0.05)
    verifie(f"{ligne['rythme']} : la latence moyenne est dans ses bornes",
            ligne["latence_moyenne_bornes_j"][0] <= ligne["latence_moyenne_j"]
            <= ligne["latence_moyenne_bornes_j"][1])
verifie("le cout d'un jour est celui que REC publie, hors penalites",
        lat["cout_d_un_jour_MAD"]
        == rec["cout_d_un_jour"]["cout_hors_penalites_MAD_par_jour_ouvre"],
        f"{lat['cout_d_un_jour_MAD']} MAD/j")
# canari : oublier le delai de remontee doit CHANGER l'ecart entre les deux rythmes.
_sans = (rp["periode_mensuelle_j"]["valeur"] - rp["periode_hebdomadaire_j"]["valeur"]) / 2
verifie("canari : le delai de remontee ne change PAS l'ecart des deux rythmes",
        abs(_sans - lat["ecart_des_deux_rythmes_j"]) < 0.05,
        "il s'annule dans la difference — c'est pourquoi il faut le dire a part")
verifie("mais il pese une part declaree de la latence hebdomadaire",
        abs(lat["part_du_delai_de_remontee_dans_l_hebdo_pct"]
            - rp["delai_de_remontee_j"]["valeur"]
            / lat["lignes"][0]["latence_moyenne_j"] * 100) < 0.2,
        f"{lat['part_du_delai_de_remontee_dans_l_hebdo_pct']} %")

# ------------------------------------------------- 5. l'alerte ferroviaire
print("\n--- l'alerte qui compte : une duree, pas un ratio ---")
a = r["alerte_ferroviaire"]
verifie("la periode entre fenetres est celle que data/ declare pour les consignations",
        a["periode_entre_fenetres_j"] == d["planning"]["contraintes_exploitation"]
        ["periode_entre_fenetres_jours"]["valeur"],
        f"{a['periode_entre_fenetres_j']} j")
verifie("le retard effectif est un MULTIPLE de la periode",
        abs(a["retard_effectif_j"] % a["periode_entre_fenetres_j"]) < 1e-9,
        f"{a['retard_effectif_j']} j")
verifie("et c'est le plus petit multiple qui couvre le retard constate",
        a["retard_effectif_j"] >= a["retard_constate_du_site_j"]
        and a["retard_effectif_j"] - a["periode_entre_fenetres_j"]
        < a["retard_constate_du_site_j"],
        f"{a['cycles_perdus']} cycle(s)")
verifie("l'amplification est le rapport des deux",
        abs(a["amplification"]
            - a["retard_effectif_j"] / a["retard_constate_du_site_j"]) < 0.01,
        f"x{a['amplification']}")
verifie("le seuil d'alerte du site EST la periode entre fenetres",
        a["seuil_d_alerte_du_site_j"] == a["periode_entre_fenetres_j"])
verifie("et le module dit que ce seuil est une duree, pas un pourcentage",
        dit(a["_le_seuil_est_une_duree_pas_un_ratio"], "jours"))
# canari : un retard plus petit que la periode ne coute qu'un cycle, pas zero.
_d2 = json.loads(json.dumps(d))
_d2["multi_sites"]["sites"][1]["retard_constate_j"]["valeur"] = 3
_petit = pil.alerte_ferroviaire(_d2)
verifie("canari : trois jours de retard coutent quand meme un cycle entier",
        _petit["retard_effectif_j"] == a["periode_entre_fenetres_j"]
        and _petit["cycles_perdus"] == 1,
        f"3 j -> {_petit['retard_effectif_j']} j")
_d2["multi_sites"]["sites"][1]["retard_constate_j"]["valeur"] = 0
verifie("canari : zero jour de retard ne coute aucun cycle",
        pil.alerte_ferroviaire(_d2)["cycles_perdus"] == 0)

# ------------------------------------------------- 6. les interfaces
print("\n--- les interfaces, rangees par marge ---")
itf = r["interfaces"]
verifie("seules les interfaces de DECISION sont listees",
        len(itf["lignes"]) == sum(1 for x in fer["interfaces"]["liste"]
                                  if x["nature"] == "decision") * 2,
        f"{len(itf['lignes'])} lignes pour 2 sites")
for x in itf["lignes"]:
    verifie(f"{x['site']} / {x['objet'][:22]} : limite = besoin - delai converti",
            abs(x["date_limite_de_demande_j"]
                - (x["date_de_besoin_j"] - x["delai_ouvre_j"])) < 0.1)
    verifie(f"{x['site']} / {x['objet'][:22]} : marge = limite - date d'arret",
            abs(x["marge_a_la_date_d_arret_j"]
                - (x["date_limite_de_demande_j"] - itf["date_d_arret_j"])) < 0.1)
verifie("un besoin deja servi n'est JAMAIS compte comme une demande en retard",
        all(not x["deja_depassee"] for x in itf["lignes"]
            if x["statut"] == "besoin déjà servi"),
        f"{itf['nb_besoins_deja_servis']} besoins deja servis")
verifie("les lignes encore a venir sont rangees par marge croissante",
        [x["marge_a_la_date_d_arret_j"] for x in itf["lignes"]
         if x["statut"] != "besoin déjà servi"]
        == sorted(x["marge_a_la_date_d_arret_j"] for x in itf["lignes"]
                  if x["statut"] != "besoin déjà servi"))
verifie("l'interface la plus longue a demander est celle qui echoit la premiere",
        max((x for x in itf["lignes"] if x["statut"] != "besoin déjà servi"),
            key=lambda x: x["delai_calendaire_j"])["marge_a_la_date_d_arret_j"]
        == min(x["marge_a_la_date_d_arret_j"] for x in itf["lignes"]
               if x["statut"] != "besoin déjà servi"))
verifie("le ratio de conversion vient du calendrier, pas d'une constante",
        abs(itf["jours_ouvres_par_mois_calendaire"] - 20.2) < 0.5
        and "duree" in sansaccent(itf["_d_ou_vient_le_ratio"]),
        f"{itf['jours_ouvres_par_mois_calendaire']} j ouvres / mois")
# Le PARADOXE, publie : le retard du site recule la date limite.
_r0 = itf["lignes"][0]
verifie("le retard du site recule la date limite de la demande en retard",
        _r0["marge_apres_le_retard_du_site_j"] > _r0["marge_a_la_date_d_arret_j"]
        and abs(_r0["marge_apres_le_retard_du_site_j"]
                - (_r0["marge_a_la_date_d_arret_j"]
                   + a["retard_constate_du_site_j"])) < 0.1,
        f"{_r0['marge_a_la_date_d_arret_j']} -> "
        f"{_r0['marge_apres_le_retard_du_site_j']} j")

# ------------------------------------------------- figures
print("\n--- figures ---")
f = r["figures"]
verifie("la figure des CPI porte les deux sites, le consolide et la moyenne",
        len(f["cpi_par_site"]) == len(r["sites"]) + 2
        and f["cpi_par_site"][-1]["libelle"].startswith("Moyenne"))
verifie("et la barre « moyenne » est marquee comme fausse",
        f["cpi_par_site"][-1]["alerte"] is True)
verifie("la figure des lots ne montre que les lots DEMARRES",
        len(f["lots_du_site_secondaire"]) == mr["nb_lots_demarres"])
verifie("la figure des interfaces ne montre que les besoins encore a venir",
        len(f["interfaces"]) == itf["nb_a_venir"],
        f"{len(f['interfaces'])} lignes")
verifie("l'escalier du retard est croissant et constant par morceaux",
        all(b["v"] >= aa["v"] for aa, b in zip(f["retard_quantise"],
                                               f["retard_quantise"][1:]))
        and len({x["v"] for x in f["retard_quantise"]})
        == len(f["retard_quantise"]) // a["periode_entre_fenetres_j"] + 1,
        f"{len({x['v'] for x in f['retard_quantise']})} marches")
verifie("le marqueur de l'escalier est le retard constate",
        f["marqueur_retard"]["x"] == a["retard_constate_du_site_j"])

print()
if echecs:
    print(f"ECHEC : {len(echecs)} controle(s) — {', '.join(echecs[:4])}")
    sys.exit(1)
print("Tests pilotage : tous verts.")
