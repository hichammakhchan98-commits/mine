"""Lance l'etalonnage, les calculs et les tests de calc/ dans l'ordre impose par le § 3.3 :
sans etalonnage valide, les resultats ne servent pas d'exemple de reference."""
import subprocess, sys, pathlib

RACINE = pathlib.Path(__file__).resolve().parent
ETAPES = [
    ("Etalonnage", [sys.executable, str(RACINE / "etalonnage" / "perimetre_cadre.py")]),
    ("Calculs",    [sys.executable, str(RACINE / "cage.py")]),
    ("Tests",      [sys.executable, str(RACINE / "tests" / "test_cage.py")]),
]
code = 0
for nom, cmd in ETAPES:
    print(f"\n=== {nom} ===")
    r = subprocess.run(cmd, capture_output=True, text=True)
    sortie = r.stdout.strip()
    if nom == "Calculs":
        sortie = "  sortie ecrite dans calc/sorties/metre-cage.json"
    print(sortie)
    if r.stderr.strip():
        print(r.stderr.strip())
    if r.returncode:
        code = r.returncode
print(f"\ncalc/ : {'VERT' if code == 0 else 'ECHEC'}")
sys.exit(code)
