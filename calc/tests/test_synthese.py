"""Tests du module B7b + C4 — lots techniques et second œuvre.

Des tests de REGLE. Aucun n'epingle « 200 mm ne passe nulle part » ni « 31 fois plus
cher » : ils verifient qu'un passage libre est une soustraction faite sur les armatures
que B3e publie, qu'une date de gel est une date de coulage moins un delai, que la file
de corps d'etat suit sa forme fermee et bute sur son goulot. Trois canaris cherchent
l'erreur au lieu de la confirmer.
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
r = json.loads((S / "synthese.json").read_text(encoding="utf-8"))
fer = json.loads((S / "ferraillage.json").read_text(encoding="utf-8"))
pl = json.loads((S / "planification.json").read_text(encoding="utf-8"))
su = json.loads((S / "suivi.json").read_text(encoding="utf-8"))
go = json.loads((S / "gros-oeuvre.json").read_text(encoding="utf-8"))
LT = d["lots_techniques"]
import synthese as syn                                                   # noqa: E402

# ------------------------------------------------- 1. le passage libre
print("\n--- ce qui passe entre deux armatures ---")
pa = r["passage_libre"]
verifie("les espacements viennent de B3e, aucun n'est redeclare dans ce module",
        all("espacement" not in k for k in LT["reservations"])
        and len(pa["endroits"]) == len(fer["cadres"]["zones"]) + 2,
        f"{len(pa['endroits'])} endroits")
for e in pa["endroits"]:
    verifie(f"{e['endroit'][:38]} : libre = espacement - diametre d'armature",
            abs(e["passage_libre_mm"]
                - (e["espacement_mm"] - e["dia_armature_mm"])) < 1e-9,
            f"{e['passage_libre_mm']} mm")
    verifie(f"{e['endroit'][:38]} : les deux listes partitionnent le catalogue",
            sorted(e["diametres_qui_passent"] + e["diametres_qui_ne_passent_pas"])
            == sorted(LT["reservations"]["diametres_courants_mm"]))
# LA regle : le plus etroit des passages est celui des cadres resserres sur appui.
_cadres = [e for e in pa["endroits"] if e["endroit"].startswith("Poutre")]
verifie("le passage le plus etroit est sur appui, la ou les cadres sont resserres",
        min(_cadres, key=lambda e: e["passage_libre_mm"])["espacement_mm"]
        == min(z["espacement_cm"] for z in fer["cadres"]["zones"]) * 10,
        pa["endroit_le_plus_etroit"])
# canari : si les cadres etaient espaces de 30 cm, le 250 passerait. Le test doit voir
# le calcul suivre les armatures, et non un nombre fige.
_d2 = json.loads(json.dumps(d))
_f2 = json.loads(json.dumps(fer))
_f2["cadres"]["zones"][1]["espacement_cm"] = 30
_large = syn.passage_libre(_d2, _f2)
verifie("canari : des cadres a 30 cm laisseraient passer un fourreau de 250 mm",
        250 in [x for e in _large["endroits"] for x in e["diametres_qui_passent"]]
        and 250 not in [x for e in pa["endroits"] for x in e["diametres_qui_passent"]],
        "le calcul suit les armatures, il n'est pas fige")
verifie("le module dit que la geometrie ne donne PAS le droit de percer",
        dit(pa["_ce_que_ce_nombre_ne_dit_pas"], "reglementaire", "⏸"))

# ------------------------------------------------- 2. le gel du carnet
print("\n--- le carnet de reservations et sa date de gel ---")
g = r["gel_des_reservations"]
_seg = pl["segments_de_travail"]["MEZZ"]
verifie("il y a autant de carnets que de zones de coulage chez C3",
        len(g["lignes"]) == go["cycle"]["nb_zones"] == g["nb_zones"],
        f"{g['nb_zones']} zones")
for x in g["lignes"]:
    verifie(f"zone {x['zone']} : gel = coulage - delai",
            abs(x["date_de_gel_j"]
                - (x["date_de_coulage_j"] - g["delai_de_gel_j"])) < 0.05)
verifie("les coulages suivent la cadence que C3 publie",
        all(abs((b["date_de_coulage_j"] - a["date_de_coulage_j"]) - g["cadence_j"]) < 0.05
            for a, b in zip(g["lignes"], g["lignes"][1:])),
        f"{g['cadence_j']} j")
verifie("le premier coulage tombe apres le debut de MEZZ chez D2",
        g["lignes"][0]["date_de_coulage_j"] > _seg[0][0],
        f"j {g['lignes'][0]['date_de_coulage_j']} apres j {_seg[0][0]}")
verifie("la fenetre du carnet encadre toutes les dates de gel",
        g["fenetre_du_carnet_j"][0] == min(x["date_de_gel_j"] for x in g["lignes"])
        and g["fenetre_du_carnet_j"][1] == max(x["date_de_gel_j"] for x in g["lignes"]))
# LE resultat du module : le carnet se joue pendant le gros oeuvre, loin du second oeuvre.
verifie("le carnet gele AVANT le debut du second oeuvre, et de tres loin",
        g["fenetre_du_carnet_j"][1] < pl["segments_de_travail"]["SECO"][0][0],
        f"j {g['fenetre_du_carnet_j'][1]} contre j "
        f"{pl['segments_de_travail']['SECO'][0][0]}")
verifie("les taches en cours au premier gel sont LUES dans le reseau",
        all(any(v[0][0] <= g["fenetre_du_carnet_j"][0] <= v[-1][1]
                for t2, v in pl["segments_de_travail"].items()
                if pl["durees"].get(t2, {}).get("nom") == t)
            for t in g["taches_en_cours_au_premier_gel"]),
        " · ".join(g["taches_en_cours_au_premier_gel"]))
verifie("le nombre de reservations suit la densite declaree",
        abs(g["reservations_sur_le_plancher"]
            - g["surface_d_une_zone_m2"] * g["nb_zones"] * g["densite_par_m2"]) < 1,
        f"{g['reservations_sur_le_plancher']:.0f} reservations")
verifie("et ses bornes encadrent le nombre publie",
        g["reservations_bornes"][0] <= g["reservations_sur_le_plancher"]
        <= g["reservations_bornes"][1])

# ------------------------------------------------- 3. le trou oublie
print("\n--- ce que coute un trou oublie ---")
c = r["cout_du_trou_oublie"]
verifie("le cout du percement est la somme de ses postes",
        abs(c["cout_du_percement_MAD"] - sum(p["MAD"] for p in c["postes"])) < 0.01,
        f"{c['cout_du_percement_MAD']:.0f} MAD")
verifie("les parts des postes font 100 %",
        abs(sum(p["part_pct"] for p in c["postes"]) - 100) < 0.5)
verifie("le rapport est le quotient des deux couts",
        abs(c["rapport"]
            - c["cout_du_percement_MAD"] / c["cout_d_une_reservation_prevue_MAD"]) <= 0.0501,
        f"x{c['rapport']} pour "
        f"{c['cout_du_percement_MAD'] / c['cout_d_une_reservation_prevue_MAD']:.2f}")
# LA regle des bornes : la borne basse du rapport combine le percement le moins cher avec
# la reservation la plus chere. L'inverse donnerait une fourchette trop etroite.
verifie("les bornes du rapport croisent les extremes dans le bon sens",
        abs(c["rapport_bornes"][0]
            - c["cout_du_percement_bornes_MAD"][0]
            / c["cout_d_une_reservation_bornes_MAD"][1]) < 0.05
        and c["rapport_bornes"][0] < c["rapport"] < c["rapport_bornes"][1],
        f"{c['rapport_bornes']}")
verifie("la part « sans outil » ne compte que l'etude et la remise en etat",
        abs(c["part_sans_outil_pct"]
            - sum(p["MAD"] for p in c["postes"]
                  if "etude" in p["poste"] or "abords" in p["poste"])
            / c["cout_du_percement_MAD"] * 100) < 0.2,
        f"{c['part_sans_outil_pct']} %")
verifie("le module refuse de chiffrer le cas d'un element porteur",
        dit(c["_sur_un_element_porteur"], "⏸", "bureau d'etudes"))

# ------------------------------------------------- 4. la file de corps d'etat
print("\n--- le second oeuvre est une file ---")
so = r["second_oeuvre"]
W = [x["duree_totale_j"] for x in so["corps"]]
verifie("la serie pure est la somme des durees",
        abs(so["duree_en_serie_pure_j"] - sum(W)) < 0.05, f"{sum(W)} j")
verifie("le plancher incompressible est la duree du corps le plus lent",
        so["plancher_incompressible_j"] == max(W)
        and so["duree_du_goulot_j"] == max(W),
        f"{so['goulot']} — {max(W)} j")
verifie("un seul corps est marque comme goulot",
        sum(1 for x in so["corps"] if x["est_le_goulot"]) == 1)
verifie("la duree a Z zones suit la forme fermee",
        abs(so["duree_a_Z_zones_j"]
            - syn.file_de_corps_d_etat(W, so["nb_zones_du_gros_oeuvre"],
                                       so["cout_de_frontiere_j"])) < 0.05,
        f"{so['duree_a_Z_zones_j']} j")
verifie("le decoupage en zones raccourcit la file",
        so["duree_a_Z_zones_j"] < so["duree_en_serie_pure_j"],
        f"{so['duree_en_serie_pure_j']} -> {so['duree_a_Z_zones_j']} j")
verifie("et il ne descend jamais sous le plancher",
        min(p["v"] for p in so["courbe"]) >= so["plancher_incompressible_j"] - 1e-9)
# LA regle du cout de frontiere : sans lui la courbe decroit, avec lui elle a un minimum.
verifie("sans cout de frontiere la file decroit strictement",
        all(b["v"] < a["v"] for a, b in zip(so["courbe_sans_frontiere"],
                                            so["courbe_sans_frontiere"][1:])))
verifie("avec cout de frontiere, l'optimum est interieur",
        1 < so["zone_optimale"] < max(p["x"] for p in so["courbe"]),
        f"{so['zone_optimale']} zones")
verifie("et le nombre de zones du gros oeuvre n'est pas loin de cet optimum",
        abs(so["zone_optimale"] - so["nb_zones_du_gros_oeuvre"]) <= 2,
        f"{so['zone_optimale']} contre {so['nb_zones_du_gros_oeuvre']}")
# SECONDE VOIE : la forme fermee et la duree declaree par D2 doivent se ressembler.
verifie("la forme fermee et la duree declaree par D2 s'accordent a moins de 10 %",
        abs(so["ecart_avec_D2_j"]) / so["duree_declaree_par_D2_j"] < 0.10,
        f"{so['duree_a_Z_zones_j']} j contre {so['duree_declaree_par_D2_j']} declares "
        f"— {so['ecart_avec_D2_j']:+.1f} j")
verifie("la duree declaree est celle que D2 publie pour SECO",
        so["duree_declaree_par_D2_j"] == pl["durees"]["SECO"]["duree_j"])
# canari : accelerer un corps qui n'est PAS le goulot ne change presque rien.
_W2 = [w / 2 if w != max(W) else w for w in W]
verifie("canari : diviser par deux tous les corps SAUF le goulot ne suffit pas",
        syn.file_de_corps_d_etat(_W2, so["nb_zones_du_gros_oeuvre"])
        > so["plancher_incompressible_j"],
        f"{syn.file_de_corps_d_etat(_W2, so['nb_zones_du_gros_oeuvre']):.1f} j, toujours "
        f"au-dessus de {so['plancher_incompressible_j']} j")
# canari : diviser le goulot par deux deplace VRAIMENT le plancher.
_W3 = [w / 2 if w == max(W) else w for w in W]
verifie("canari : diviser le goulot par deux abaisse le plancher",
        max(_W3) < max(W)
        and syn.file_de_corps_d_etat(_W3, 1_000_000) < so["plancher_incompressible_j"],
        f"plancher {max(_W3)} j au lieu de {max(W)}")

# ------------------------------------------------- 5. la chaine des supports
print("\n--- la chaine des supports ---")
ch = r["chaine_des_supports"]
verifie("chaque corps declare de qui il recoit son support",
        all(x["recoit_de"] and x["support"] for x in ch["lignes"]))
verifie("la chaine est continue : chaque corps recoit du precedent",
        all(b["recoit_de"].lower().startswith(a["corps"].split(" (")[0].lower()[:8])
            for a, b in zip(ch["lignes"], ch["lignes"][1:])),
        " -> ".join(x["corps"][:14] for x in ch["lignes"]))
verifie("et le premier recoit du gros oeuvre",
        "gros" in ch["lignes"][0]["recoit_de"])

# ------------------------------------------------- figures
print("\n--- figures ---")
f = r["figures"]
verifie("la figure des passages porte tous les endroits",
        len(f["passages"]) == len(pa["endroits"]))
verifie("la figure du gel porte toutes les zones, du gel au coulage",
        len(f["gel"]) == g["nb_zones"]
        and all(abs(x["duree"] - g["delai_de_gel_j"]) < 0.05 for x in f["gel"]))
verifie("la cascade du cout recolle a ses postes",
        f["cout"][-1].get("type") == "total"
        and abs(f["cout"][-1]["montant"]
                - sum(x["montant"] for x in f["cout"][:-1])) <= 1)
verifie("la figure des corps marque le goulot, et lui seul",
        sum(1 for x in f["corps"] if x["alerte"]) == 1)
verifie("la courbe de la file part de la serie pure",
        abs(f["file"][0]["v"] - so["duree_en_serie_pure_j"]) < 0.05)
verifie("et le marqueur est le nombre de zones du gros oeuvre",
        f["marqueur_zones"]["x"] == so["nb_zones_du_gros_oeuvre"])

print()
if echecs:
    print(f"ECHEC : {len(echecs)} controle(s) — {', '.join(echecs[:4])}")
    sys.exit(1)
print("Tests synthese : tous verts.")
