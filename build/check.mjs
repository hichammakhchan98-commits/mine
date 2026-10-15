/* Controle outille (§ 12.1). Une case cochee par l'auteur ne prouve rien : chaque point
   ci-dessous produit une preuve (sortie de commande, fichier, capture).
   Points couverts ici : a a k. Les points a, b, c, e sont delegues a Playwright
   (tests/rendu.spec.mjs), qui ouvre reellement les pages dans un Chromium. */

import { execFileSync } from "node:child_process";
import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { join } from "node:path";
import { empreinteData } from "./empreinte.mjs";

const SANS_ZIP = process.env.CHECK_SANS_ZIP === "1" || process.argv.includes("--sans-zip");
const ok = [], ec = [], info = [];
const V = (n, d) => ok.push(d ? `${n} — ${d}` : n);
const E = (n, d) => ec.push(d ? `${n} : ${d}` : n);

function etape(nom, cmd, args) {
  try {
    const out = execFileSync(cmd, args, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
    V(nom, out.trim().split("\n").pop());
    return out;
  } catch (e) {
    E(nom, (e.stdout || "") + (e.stderr || ""));
    return null;
  }
}

console.log("CONTROLE — cours de genie civil (§ 12.1)\n");

/* --- f, i : calc/ — etalonnage, calculs, tests, verification dimensionnelle --- */
etape("f,i · calc/ : etalonnage, calculs, tests, unites (pint)", "python3", ["calc/run_all.py"]);

/* --- la chaine de generation : data/ + calc/ -> modules --- */
etape("4.3 · build (variables, balises, legendes)", "node", ["build/build.mjs"]);

/* --- h : balises de preuve et registres (§ 3.2, Annexe 3) --- */
try {
  const entetes = {
    "data/registre-sources.csv": "id;niveau;enonce_reformule;reference;modules;statut;date",
    "data/registre-hypotheses.csv": "id;hypothese;valeur;unite;fourchette;annee_ref;modules;justification",
    "cadrage/registre-sources-cadrage.csv": "id;niveau;enonce_reformule;reference;modules;statut;date",
    "cadrage/registre-hypotheses-cadrage.csv": "id;hypothese;valeur;unite;fourchette;annee_ref;modules;justification",
  };
  let n = 0;
  for (const [f, att] of Object.entries(entetes)) {
    const l = readFileSync(f, "utf8").split("\n");
    if (l[0].trim() !== att) E(`h · en-tete de ${f}`, `attendu « ${att} »`);
    n += l.filter((x) => x.trim()).length - 1;
  }
  V("h · registres : en-tetes conformes", `${n} ligne(s) au total`);
} catch (e) { E("h · registres", e.message); }

/* --- M2 : une V3 publiee sans ligne de registre est une V3 non declaree (§ 3.2) --- */
try {
  const hyp = readFileSync("data/registre-hypotheses.csv", "utf8").trim().split("\n").slice(1);
  const publie = readdirSync("content").filter((f) => f.endsWith(".md"))
    .map((f) => readFileSync(join("content", f), "utf8")).join("\n");
  const balises = [...publie.matchAll(/⟦V3\|([^|⟧]*)\|([^⟧]*)⟧/g)];
  const mentions = [...publie.matchAll(/\(V3[,)]/g)];
  if (mentions.length && !balises.length)
    E("3.2 · registre des hypotheses",
      `${mentions.length} mention(s) « (V3 » dans content/ mais aucune balise ⟦V3|…⟧ : rien n'alimente le registre`);
  else if (balises.length !== hyp.length)
    E("3.2 · registre des hypotheses",
      `${balises.length} balise(s) V3 dans content/ contre ${hyp.length} ligne(s) de registre`);
  else V("3.2 · chaque V3 publiee a sa ligne de registre", `${balises.length} hypothese(s)`);
} catch (e) { E("3.2 · registre des hypotheses", e.message); }

/* --- M8 : le livrable doit etre dans le depot (§ 5.2, et le zip du mode B embarque .git) --- */
try {
  const sale = execFileSync("git", ["status", "--porcelain"], { encoding: "utf8" }).trim();
  if (sale) E("5.2 · depot git", `arbre de travail non propre :\n      ${sale.split("\n").join("\n      ")}`);
  else V("5.2 · depot git propre", "tout le livrable est suivi et committe");
} catch (e) { E("5.2 · depot git", e.message); }

/* --- garde-fou de la phase § 5.0 : aucune valeur normative ne doit fuir --- */
try {
  const g = JSON.parse(readFileSync("data/projet-gare.json", "utf8"));
  const r = JSON.parse(readFileSync("data/referentiels.json", "utf8"));
  if (g.meta.normes_disponibles !== r.meta.normes_disponibles)
    E("5.0 · coherence", "normes_disponibles differe entre projet-gare.json et referentiels.json");
  else if (g.meta.normes_disponibles === false) {
    // toutes les cles de charges, pas une liste figee qui en oublie une (neige)
    for (const [k, v] of Object.entries(g.charges ?? {})) {
      if (k === "note") continue;
      const rempli = v && (typeof v === "object" ? Object.keys(v).length > 0 : v !== null);
      if (rempli) E("5.0 · charges", `charges.${k} est rempli alors que normes_disponibles = false`);
    }
    // les V2 se cherchent dans le CONTENU PUBLIE, pas dans un registre qui peut etre vide
    const publie = readdirSync("content").filter((f) => f.endsWith(".md"))
      .map((f) => readFileSync(join("content", f), "utf8")).join("\n");
    const v2 = [...publie.matchAll(/⟦V2\|[^⟧]*⟧/g)];
    if (v2.length) E("5.0 · balises", `${v2.length} valeur(s) V2 normative(s) ecrite(s) en phase § 5.0`);
    else V("5.0 · phase sans calculs normatifs respectee",
      `${Object.keys(g.charges ?? {}).length - 1} jeux de charges vides, aucune balise V2 dans content/`);
  } else V("5.0 · suspension levee", "normes_disponibles = true");
} catch (e) { E("5.0 · garde-fou", e.message); }

/* --- j : empreinte de data/ identique partout (§ 4.3) --- */
try {
  const emp = empreinteData();
  const perimes = [];
  for (const f of [...readdirSync("modules").map((x) => join("modules", x)), "index.html"]) {
    if (!f.endsWith(".html")) continue;
    const m = readFileSync(f, "utf8").match(/Empreinte des donn[eé]es\s*:\s*<code>([0-9a-f]+)<\/code>/);
    if (!m) perimes.push(`${f} : aucune empreinte affichee`);
    else if (m[1] !== emp) perimes.push(`${f} : ${m[1]} au lieu de ${emp}`);
  }
  if (perimes.length) E("j · empreinte de data/", perimes.join(" ; "));
  else V("j · empreinte de data/ identique dans tous les modules", emp);
} catch (e) { E("j · empreinte", e.message); }

/* --- une seule source de verite visuelle : CSS et civil3d doivent s'accorder --- */
try {
  const css = readFileSync("assets/style.css", "utf8");
  const mat = readFileSync("src/civil3d/materiaux.js", "utf8");
  const paires = { beton: "--mat-beton", acierHA: "--mat-acier-ha", charpente: "--mat-charpente",
    sol: "--mat-sol", cable: "--mat-cable", coffrage: "--mat-coffrage" };
  const ecarts = [];
  for (const [cle, varCss] of Object.entries(paires)) {
    const a = css.match(new RegExp(`${varCss}:\\s*#([0-9a-fA-F]{6})`))?.[1]?.toLowerCase();
    const b = mat.match(new RegExp(`${cle}:\\s*0x([0-9a-fA-F]{6})`))?.[1]?.toLowerCase();
    if (!a || !b) ecarts.push(`${cle} : introuvable`);
    else if (a !== b) ecarts.push(`${cle} : css #${a} contre 3D #${b}`);
  }
  if (ecarts.length) E("R1 · couleurs des materiaux", ecarts.join(" ; "));
  else V("R1 · couleurs des materiaux identiques entre CSS et civil3d", `${Object.keys(paires).length} materiaux`);
} catch (e) { E("R1 · couleurs", e.message); }

/* --- g : poids des fichiers (§ 4.4) --- */
try {
  const lourds = [];
  for (const f of readdirSync("modules")) {
    const ko = statSync(join("modules", f)).size / 1024;
    if (ko > 1536) lourds.push(`${f} : ${ko.toFixed(0)} ko`);
  }
  const bundle = statSync("assets/civil3d.bundle.js").size / 1024;
  if (lourds.length) E("g · poids des modules (objectif <= 1500 ko)", lourds.join(" ; "));
  else V("g · poids des modules", `objectif <= 1500 ko tenu`);
  info.push(`bundle 3D partage : ${bundle.toFixed(0)} ko (hors budget par module)`);
} catch (e) { E("g · poids", e.message); }

/* --- a, b, c, d, e, g : le rendu reel, dans un navigateur --- */
etape("a,b,c,d,e · rendu : console, WebGL, captures, etiquettes, hors ligne",
  "npx", ["playwright", "test", "--config=tests/playwright.config.mjs", "--reporter=line"]);

/* --- k : mode B — le zip de reprise s'ouvre et le projet repasse au vert --- */
if (SANS_ZIP) info.push("k · controle du zip de reprise : non execute (--sans-zip)");
else etape("k · mode B : le zip de reprise rouvre et repasse au vert", "node", ["build/check-zip.mjs"]);

/* --- rapport --- */
console.log("");
for (const l of ok) console.log(`  ok     ${l}`);
for (const l of info) console.log(`  info   ${l}`);
if (ec.length) {
  console.log("");
  for (const l of ec) console.log(`  ECHEC  ${l}`);
  console.log(`\n${ec.length} echec(s) sur ${ok.length + ec.length} controles.`);
  process.exit(1);
}
console.log(`\nVERT — ${ok.length} controles passes. Captures : tests/captures/`);
