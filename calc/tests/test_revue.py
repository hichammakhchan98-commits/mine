"""Tests du module RC1 — le dossier à corriger de la revue de palier.

Un dossier à corriger a une exigence que les autres modules n'ont pas : **le corrigé ne
doit pas pouvoir dériver du dossier**. Un corrigé qui désigne une erreur absente, ou qui
en oublie une présente, apprend une erreur de plus. Ces tests vérifient la BIJECTION
entre les lignes fausses et le corrigé, et que chaque ligne juste l'est vraiment — c'est-
à-dire qu'elle vaut exactement ce que publie le module dont elle est extraite.
"""
from __future__ import annotations
import json, sys, pathlib, unicodedata

RACINE = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RACINE / "calc"))

echecs = []


def sansaccent(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s).lower())
                   if unicodedata.category(c) != "Mn")


def verifie(nom, condition, detail=""):
    if not condition:
        echecs.append(nom)
    print(f"  {'ok   ' if condition else 'ECHEC'} {nom}" + (f" — {detail}" if detail else ""))


d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
r = json.loads((RACINE / "calc" / "sorties" / "revue.json").read_text(encoding="utf-8"))
do = r["dossier"]
S = {n: json.loads((RACINE / "calc" / "sorties" / f"{n}.json").read_text(encoding="utf-8"))
     for n in ("prix", "planification", "reception", "qualite", "suivi",
               "valeur-acquise", "ferraillage")}

# ------------------------------------------------- 1. le cadre du § 5.5
print("\n--- le cadre impose par le § 5.5 ---")
verifie("le dossier porte de 5 a 8 erreurs plantees",
        5 <= do["nb_erreurs"] <= 8, f"{do['nb_erreurs']} erreurs")
verifie("chaque erreur appartient a une famille DIFFERENTE",
        len(do["familles"]) == do["nb_erreurs"],
        " · ".join(do["familles"]))
verifie("et le dossier contient aussi des lignes JUSTES",
        do["nb_justes"] >= 3,
        f"{do['nb_justes']} lignes justes sur {do['nb_lignes']}")

# ------------------------------------------------- 2. la bijection ligne <-> corrige
print("\n--- le corrige ne peut pas deriver du dossier ---")
_fausses = {x["erreur"]: x for x in do["lignes"] if x["erreur"]}
_corrige = {x["id"]: x for x in do["erreurs"]}
verifie("chaque ligne fausse a son entree au corrige",
        set(_fausses) == set(_corrige),
        f"{sorted(_fausses)} contre {sorted(_corrige)}")
for eid, e in _corrige.items():
    verifie(f"{eid} : le corrige designe une ligne qui existe",
            e["ligne"] in {x["id"] for x in do["lignes"]})
    verifie(f"{eid} : et cette ligne est bien marquee fausse",
            next(x for x in do["lignes"] if x["id"] == e["ligne"])["erreur"] == eid)
# LA regle : une erreur plantee doit CHANGER le nombre. Une « erreur » qui ne deplace
# rien n'est pas une erreur, c'est une opinion — et le lecteur qui la cherche ne la
# trouvera jamais.
# UNE exception, nommee : E4 ne deplace aucun nombre parce que c'est une erreur de
# LECTURE — le chiffre est juste et c'est la comparaison qui ne l'est pas. Elle doit
# alors porter sa propre explication, et le test l'exige.
_SANS_ECART = {"E4": "erreur de lecture : le chiffre est juste, la comparaison ne l'est "
                     "pas. Elle porte « _le_piege_dans_le_piege » a la place."}
for eid, l in _fausses.items():
    ecart = abs(l["valeur"] - l["juste"]) / max(abs(l["juste"]), 1e-9)
    if eid in _SANS_ECART:
        verifie(f"{eid} : exception nommee, et elle s'explique",
                "_le_piege_dans_le_piege" in _corrige[eid],
                _SANS_ECART[eid][:60])
        continue
    verifie(f"{eid} : l'erreur deplace reellement le nombre",
            ecart > 0.05,
            f"{l['affiche'][:28]} contre {l['juste']:.2f} — "
            f"{ecart * 100:.0f} % d'ecart")
for eid, e in _corrige.items():
    verifie(f"{eid} : le corrige nomme sa famille",
            len(str(e.get("famille", ""))) > 5, e.get("famille"))
    for champ in ("symptome", "comment_la_trouver", "ce_qu_elle_coute",
                  "ou_le_cours_l_a_commise"):
        verifie(f"{eid} : le corrige dit « {champ} »",
                len(str(e.get(champ, ""))) > 30)

# ------------------------------------------------- 3. les lignes justes le sont
print("\n--- les lignes justes valent ce que publie leur module ---")
_attendu = {
    "L1": S["suivi"]["avancements"]["physique_pct"],
    "L9": S["ferraillage"]["ordre_de_grandeur"]["elements"][0]["ratio_du_plan_kg_m3"],
    "L10": S["qualite"]["dechets"]["part_dangereuse_pct"],
    "L11": S["valeur-acquise"]["CPI"],
}
for lid, v in _attendu.items():
    l = next(x for x in do["lignes"] if x["id"] == lid)
    verifie(f"{lid} : la valeur affichee est celle du module, au centieme",
            abs(l["valeur"] - v) < 0.01 and l["erreur"] is None,
            f"{l['affiche']} — {l['source']}")
verifie("chaque ligne nomme le module d'ou elle sort",
        all("module" in x["source"] for x in do["lignes"]))

# ------------------------------------------------- 4. les valeurs justes des fausses
print("\n--- et les valeurs JUSTES des lignes fausses viennent des modules ---")
_justes = {
    "E6": S["suivi"]["avancements"]["physique_pct"],
    "E3": S["planification"]["durees"]["CHLV"]["duree_j"],
    "E5": next(x["total_MAD"] for x in S["qualite"]["non_conformite"]["par_ouvrage"]
               if x["tache"] == "NOYX"),
    "E7": next(x["retard_du_chantier_j"] for x in S["qualite"]["impact_planning"]["lignes"]
               if x["tache"] == "CHLV"),
}
for eid, v in _justes.items():
    verifie(f"{eid} : la valeur juste est celle que publie le module",
            abs(_fausses[eid]["juste"] - v) < 0.01,
            f"{v:.2f}")
# E2 : le prix juste est le regime HORS penalites, pas le regime sous penalites.
_e2 = _fausses["E2"]
_hors = S["reception"]["cout_d_un_jour"]["cout_hors_penalites_MAD_par_jour_ouvre"]
_sous = S["reception"]["cout_d_un_jour"]["cout_sous_penalites_MAD_par_jour_ouvre"]
verifie("E2 : le rapport des deux valeurs est celui des deux regimes de REC",
        abs(_e2["valeur"] / _e2["juste"] - _sous / _hors) < 0.01,
        f"x{_e2['valeur'] / _e2['juste']:.1f}")
# E1 : le rapport est le facteur de conversion des deux calendriers.
_e1 = _fausses["E1"]
_conv = S["prix"]["bordereau"]["frais_de_duree"]["conversion"]["calendaires_par_jour_ouvre"]
verifie("E1 : le rapport des deux valeurs est le facteur des deux calendriers",
        abs(_e1["juste"] / _e1["valeur"] - _conv) < 0.01,
        f"x{_e1['juste'] / _e1['valeur']:.4f} contre {_conv}")
# E3 : le rapport est le facteur d'interception publie par D2.
_e3 = _fausses["E3"]
_fi = S["planification"]["durees"]["CHLV"]["facteur_d_interception"]
verifie("E3 : le rapport des deux valeurs est le facteur d'interception de D2",
        abs(_e3["juste"] / _e3["valeur"] - _fi) < 0.01,
        f"x{_e3['juste'] / _e3['valeur']:.2f} contre {_fi}")
# E4 : la valeur n'a PAS bouge — c'est la comparaison qui est fausse, pas le chiffre.
_e4 = _fausses["E4"]
verifie("E4 : le chiffre est juste, et c'est la COMPARAISON qui est fausse",
        abs(_e4["valeur"] - _e4["juste"]) < 1e-9
        and "ALERTE" in _e4["affiche"]
        and "_le_piege_dans_le_piege" in _corrige["E4"],
        "une erreur de lecture, pas de calcul")

# ------------------------------------------------- 5. les appats
print("\n--- les appats : savoir dire RAS est la moitie du metier ---")
verifie("il y a au moins trois appats",
        len(do["appats"]) >= 3, f"{len(do['appats'])} appats")
for a in do["appats"]:
    verifie(f"l'appat {a['ligne']} designe une ligne JUSTE du dossier",
            next((x for x in do["lignes"] if x["id"] == a["ligne"]), {}).get("erreur") is None,
            a["verdict"][:48])
    verifie(f"l'appat {a['ligne']} dit pourquoi on doute, et tranche",
            len(a["pourquoi_on_doute"]) > 60 and len(a["verdict"]) > 10)

print()
if echecs:
    print(f"ECHEC : {len(echecs)} controle(s) — {', '.join(echecs)}")
    sys.exit(1)
print("Tests revue : tous verts.")
