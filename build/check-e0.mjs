// check-e0.mjs — controle de reprise MINIMAL de l'Etape 0 (mode B, § 12.1k).
// Il ne controle que ce qui existe a l'Etape 0 : integrite des JSON, presence des pieces de
// cadrage, en-tetes des registres, empreinte de data/.
// REMPLACE a l'Etape 1 par build/check.mjs, qui couvre les points a a k du § 12.1.
import { readFileSync, readdirSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { join } from "node:path";

const ec = [];
const ok = [];
const seul = process.argv.includes("--empreinte-seule");

function verifie(nom, fn) {
  try { const d = fn(); ok.push(d ? `${nom} — ${d}` : nom); }
  catch (e) { ec.push(`${nom} : ${e.message}`); }
}

// --- 1. JSON lisibles et coherents avec la phase declaree
const jsons = ["data/projet-gare.json", "data/projet-r5.json", "data/referentiels.json"];
for (const f of jsons) {
  verifie(`JSON ${f}`, () => {
    const d = JSON.parse(readFileSync(f, "utf8"));
    if (!d.meta) throw new Error("bloc meta absent");
    return `version ${d.meta.version}`;
  });
}

// --- 2. Garde-fou du § 5.0 : la phase sans calculs normatifs doit rester coherente
verifie("§ 5.0 — coherence de la phase", () => {
  const g = JSON.parse(readFileSync("data/projet-gare.json", "utf8"));
  const r = JSON.parse(readFileSync("data/referentiels.json", "utf8"));
  if (g.meta.normes_disponibles !== r.meta.normes_disponibles)
    throw new Error("normes_disponibles differe entre projet-gare.json et referentiels.json");
  if (g.meta.normes_disponibles === false) {
    const ch = g.charges ?? {};
    for (const k of ["G", "Q", "vent", "sismique"])
      if (ch[k] && Object.keys(ch[k]).length)
        throw new Error(`charges.${k} est rempli alors que normes_disponibles = false (§ 5.0.1)`);
    return "normes_disponibles = false, charges vides — conforme";
  }
  return "normes_disponibles = true — le garde-fou ne s'applique plus";
});

// --- 3. Pieces de cadrage exigees par le § 5.1
const pieces = [
  "CLAUDE.md", "STATE.md", "DECISIONS.md",
  "cadrage/00-questions-etape0.md",   // § 5.1b — les 10 questions
  "cadrage/01-environnement.md",      // § 5.1a — verification des fichiers et outils
  "cadrage/02-jeu-de-donnees.md",     // § 5.1c — jeu de donnees propose et justifie
  "cadrage/03-referentiels.md",       // § 5.1d / § 3.1 — matrice de referentiels
  "cadrage/04-calibrage.md",          // § 5.1d / § 1.1 — tableau de calibrage
  "cadrage/05-sommaire.md",           // § 5.1d / Annexe 1 — sommaire + fiches-module
  "cadrage/06-volume-arret-coupe.md", // § 5.1d — volume, critere d'arret, ordre de coupe
];
for (const f of pieces)
  verifie(`piece ${f}`, () => { const s = statSync(f); if (!s.size) throw new Error("fichier vide"); return `${(s.size / 1024).toFixed(1)} ko`; });

// --- 4. En-tetes des registres (Annexe 3)
const entetes = {
  "data/registre-sources.csv": "id;niveau;enonce_reformule;reference;modules;statut;date",
  "data/registre-hypotheses.csv": "id;hypothese;valeur;unite;fourchette;annee_ref;modules;justification",
  "cadrage/registre-sources-cadrage.csv": "id;niveau;enonce_reformule;reference;modules;statut;date",
  "cadrage/registre-hypotheses-cadrage.csv": "id;hypothese;valeur;unite;fourchette;annee_ref;modules;justification",
};
for (const [f, att] of Object.entries(entetes))
  verifie(`registre ${f}`, () => {
    const l = readFileSync(f, "utf8").split("\n")[0].trim();
    if (l !== att) throw new Error(`en-tete inattendu :\n    attendu : ${att}\n    trouve  : ${l}`);
    const n = readFileSync(f, "utf8").trim().split("\n").length - 1;
    return `${n} ligne(s)`;
  });

// --- 5. Empreinte de data/ (§ 4.3)
function empreinte(dir) {
  const h = createHash("sha256");
  const parcours = (d) => readdirSync(d, { withFileTypes: true })
    .sort((a, b) => a.name.localeCompare(b.name))
    .forEach((e) => {
      const p = join(d, e.name);
      if (e.isDirectory()) parcours(p);
      else { h.update(e.name); h.update(readFileSync(p)); }
    });
  parcours(dir);
  return h.digest("hex").slice(0, 12);
}
const emp = empreinte("data");

if (seul) { console.log(emp); process.exit(0); }

// --- Rapport
console.log("CONTROLE DE REPRISE — ETAPE 0 (minimal, § 12.1k)\n");
ok.forEach((l) => console.log(`  ok   ${l}`));
if (ec.length) {
  console.log("");
  ec.forEach((l) => console.log(`  ECHEC  ${l}`));
  console.log(`\n${ec.length} echec(s) sur ${ok.length + ec.length} controles. Ne pas continuer (§ 12.5 B2).`);
  process.exit(1);
}
console.log(`\n  empreinte data/ : ${emp}`);
console.log(`\nVERT — ${ok.length} controles passes.`);
console.log("Rappel : controle MINIMAL. Il ne teste ni build, ni rendu, ni 3D, ni calc/ :");
console.log("ces controles n'existent qu'a partir de l'Etape 1 (§ 12.1 a-k). Declare dans STATE.md.");
