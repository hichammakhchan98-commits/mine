"""Lance l'etalonnage, les calculs et les tests de calc/ dans l'ordre impose par le § 3.3 :
sans etalonnage valide, les resultats ne servent pas d'exemple de reference."""
import subprocess, sys, pathlib

RACINE = pathlib.Path(__file__).resolve().parent
ETAPES = [
    ("Etalonnage perimetre", [sys.executable, str(RACINE / "etalonnage" / "perimetre_cadre.py")]),
    ("Etalonnage CPM",       [sys.executable, str(RACINE / "etalonnage" / "cpm_cas_ferme.py")]),
    ("Calculs cage",         [sys.executable, str(RACINE / "cage.py")]),
    ("Etalonnage plancher",  [sys.executable, str(RACINE / "etalonnage" / "plancher_cas_ferme.py")]),
    ("Calculs plancher",     [sys.executable, str(RACINE / "cycle_plancher.py")]),
    ("Calculs valeur acquise", [sys.executable, str(RACINE / "valeur_acquise.py")]),
    ("Calculs planification",  [sys.executable, str(RACINE / "planification.py")]),
    ("Verification dimensionnelle", [sys.executable, str(RACINE / "verif_unites.py")]),
    ("Tests cage",           [sys.executable, str(RACINE / "tests" / "test_cage.py")]),
    ("Tests plancher",       [sys.executable, str(RACINE / "tests" / "test_plancher.py")]),
    ("Tests planification",  [sys.executable, str(RACINE / "tests" / "test_planification.py")]),
    ("Prix (D1)",            [sys.executable, str(RACINE / "prix.py")]),
    ("Tests prix",           [sys.executable, str(RACINE / "tests" / "test_prix.py")]),
    ("Suivi (D4)",           [sys.executable, str(RACINE / "suivi.py")]),
    ("Tests suivi",          [sys.executable, str(RACINE / "tests" / "test_suivi.py")]),
    ("Gros oeuvre (C3)",     [sys.executable, str(RACINE / "gros_oeuvre.py")]),
    ("Tests gros oeuvre",    [sys.executable, str(RACINE / "tests" / "test_gros_oeuvre.py")]),
    ("Etalonnage ferraillage", [sys.executable, str(RACINE / "etalonnage" / "ferraillage_cas_ferme.py")]),
    ("Ferraillage (B3e)",    [sys.executable, str(RACINE / "ferraillage.py")]),
    ("Tests ferraillage",    [sys.executable, str(RACINE / "tests" / "test_ferraillage.py")]),
]
code = 0
for nom, cmd in ETAPES:
    print(f"\n=== {nom} ===")
    r = subprocess.run(cmd, capture_output=True, text=True)
    sortie = r.stdout.strip()
    if nom.startswith("Calculs"):
        sortie = f"  sortie ecrite dans calc/sorties/"
    print(sortie)
    if r.stderr.strip():
        print(r.stderr.strip())
    if r.returncode:
        code = r.returncode
print(f"\ncalc/ : {'VERT' if code == 0 else 'ECHEC'}")
sys.exit(code)
