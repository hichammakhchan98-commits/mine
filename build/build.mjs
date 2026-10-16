/* Chaine de generation : data/ -> calc/ -> { SVG, 3D, metre } -> HTML  (§ 4.3)
   Regles appliquees ici, sans exception :
   - aucun nombre technique n'est tape a la main dans un module : il vient de data/ ou de calc/ ;
   - le build ECHOUE si une variable {{...}} est absente ;
   - le build ECHOUE si un nombre d'un bloc :::normatif n'est pas balise (§ 3.2) ;
   - les registres de sources et d'hypotheses sont GENERES depuis les balises. */

import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";
import katex from "katex";
import { compiler, extraireBalises, controlerBlocsNormatifs,
         controlerAccidentsDeGabarit } from "./md.mjs";
import { empreinteData } from "./empreinte.mjs";

await import("../assets/section.js");   // doit preceder svgkit : il la consomme
await import("../assets/svgkit.js");
const SVGKit = globalThis.SVGKit;

const DATE = new Date().toISOString().slice(0, 10);
const erreurs = [];
const avertissements = [];

/* ---------- 1. donnees + sorties de calcul ---------- */
const data = {};
for (const f of readdirSync("data")) if (f.endsWith(".json"))
  data[f.replace(/\.json$/, "")] = JSON.parse(readFileSync(join("data", f), "utf8"));

const calc = {};
if (existsSync("calc/sorties"))
  for (const f of readdirSync("calc/sorties")) if (f.endsWith(".json"))
    calc[f.replace(/\.json$/, "")] = JSON.parse(readFileSync(join("calc/sorties", f), "utf8"));

const EMPREINTE = empreinteData();

/** Resolution d'un chemin pointe dans data/ ou calc/ : "gare.geometrie.emprise_m.0" */
function resoudre(chemin) {
  const alias = { gare: data["projet-gare"], r5: data["projet-r5"], ref: data["referentiels"] };
  const parts = chemin.split(".");
  let cur = alias[parts[0]] ?? data[parts[0]] ?? calc[parts[0]];
  if (cur === undefined) throw new Error(`racine inconnue « ${parts[0]} »`);
  for (const p of parts.slice(1)) {
    if (cur == null) throw new Error(`chemin interrompu a « ${p} »`);
    cur = cur[p];
  }
  if (cur === undefined) throw new Error(`valeur absente`);
  return cur;
}

/* Injection des variables {{chemin::format}} (§ 4.3). Utilisee deux fois : sur le HTML
   compile, et sur les champs des balises de preuve AVANT extraction, pour qu'une balise
   V3 puisse lire sa valeur dans data/ au lieu de la recopier a la main (§ 3.2, R1). */
const FINE = "\u202f";                       // espace fine insecable
function grouper(txt) {
  return txt.replace(/^(-?)(\d{4,})(,\d+)?$/, (_, signe, ent, dec = "") =>
    signe + ent.replace(/\B(?=(\d{3})+$)/g, FINE) + dec);
}

function substituerDans(texte, f) {
  return texte.replace(/\{\{([^}]+)\}\}/g, (_, expr) => {
    // separateur « :: » et non « | » : « | » delimite les cellules de tableau en Markdown
    const [chemin, fmt] = expr.split("::").map((s) => s.trim());
    try {
      let v = resoudre(chemin);
      if (fmt === "n1") v = Number(v).toFixed(1);
      else if (fmt === "n2") v = Number(v).toFixed(2);
      else if (fmt === "n0") v = Math.round(Number(v));
      else if (fmt === "n3s") v = Number(v).toPrecision(3);
      // Typographie francaise : virgule decimale, et milliers separes par une espace
      // fine insecable des 4 chiffres. Sans elle, un cout s'affiche « 2955556 MAD »
      // a cote d'un « 1 250 » de tableau : le lecteur ne peut plus comparer.
      return grouper(String(v).replace(/\./g, ","));
    } catch (e) {
      erreurs.push(`${f} : variable {{${expr}}} — ${e.message}`);
      return `<mark>VARIABLE ABSENTE : ${expr}</mark>`;
    }
  });
}

/* ---------- 2. formules : KaTeX PRE-RENDU au build (§ 4.4) ---------- */
const math = (tex, bloc) => katex.renderToString(tex, {
  displayMode: bloc, throwOnError: true, output: "html", strict: "ignore",
});

/* ---------- 3. directives ---------- */
let nFigure = 0;
const scripts = [];

function directive(nom, o, corps, ctx) {
  switch (nom) {
    case "figure": {
      nFigure++;
      const num = o.num ?? nFigure;
      if (!SVGKit[o.fn]) throw new Error(`figure ${num} : fonction svgkit inconnue « ${o.fn} »`);
      const args = typeof o.args === "string" ? resoudre(o.args) : o.args;
      const r = SVGKit[o.fn](args, o.options ?? {});
      // La legende est placee PAR LE BUILD, sous le dessin, d'apres le nombre d'entrees.
      // Elle etait auparavant posee a une coordonnee ecrite a la main dans le contenu :
      // une cote dessinee a l'oeil, et elle debordait du cadre.
      const pasLeg = 15;
      const hLeg = o.legende ? o.legende.length * pasLeg + 14 : 0;
      const legende = o.legende ? SVGKit.legende(14, r.hauteur + 16, o.legende, { pas: pasLeg }) : "";
      const svg = SVGKit.svg({
        largeur: r.largeur, hauteur: r.hauteur + hLeg, titre: o.titre, desc: o.alt ?? o.titre,
        motifs: o.motifs ?? [], contenu: r.svg
          + (o.legende ? SVGKit.ligne(12, r.hauteur + 4, r.largeur - 12, r.hauteur + 4,
              { couleur: "#d5d7d1", ep: 1 }) : "")
          + legende,
      });
      // § 8 : chaque numero du dessin doit figurer dans la legende, et inversement.
      const puces = [...r.svg.matchAll(/class="puce"[^>]*>(\d+)</g)].map((m) => Number(m[1]));
      if (o.legende) {
        const dansLeg = (o.legende ?? []).map((e) => e.n);
        const manquants = puces.filter((n) => !dansLeg.includes(n));
        const orphelins = dansLeg.filter((n) => !puces.includes(n));
        if (manquants.length) throw new Error(`figure ${num} : numero(s) ${manquants.join(", ")} sur le dessin, absent(s) de la legende`);
        if (orphelins.length) throw new Error(`figure ${num} : numero(s) ${orphelins.join(", ")} en legende, absent(s) du dessin`);
      } else if (r.legendeImplicite) {
        const dansLeg = r.legendeImplicite.map((e) => e.n);
        const manquants = puces.filter((n) => !dansLeg.includes(n));
        if (manquants.length) throw new Error(`figure ${num} : numero(s) ${manquants.join(", ")} non decrit(s), meme en place`);
      } else if (puces.length) {
        throw new Error(`figure ${num} : ${puces.length} numero(s) sur le dessin sans legende`);
      }
      const voir = (o.voir ?? []).map((t) => `<li>${t}</li>`).join("");
      return `<figure class="${o.large ? "large" : ""}">${svg}`
        + `<figcaption><span class="num">Figure ${num}.</span> ${o.titre ?? ""}</figcaption>`
        + (voir ? `<div class="figure-lecture encart encart-voir"><div class="titre">Ce qu'il faut voir</div><ul>${voir}</ul></div>` : "")
        + (o.erreur ? `<div class="figure-lecture encart encart-alerte"><div class="titre">Erreur courante</div><p>${o.erreur}</p></div>` : "")
        + `</figure>`;
    }
    case "model3d": {
      if (!o.id || !o.init) throw new Error("model3d : « id » et « init » sont obligatoires");
      scripts.push(o.init);
      return `<div class="vue3d" id="vue-${o.id}" data-titre="${o.titre ?? ""}"></div>`
        + (o.sous ? `<figcaption>${o.sous}</figcaption>` : "");
    }
    case "exercice":
      return `<details class="exercice"><summary>${o.titre ?? "Exercice"}`
        + (o.niveau ? ` <span class="etiq etiq-${o.niveau === "application" ? "m" : o.niveau === "probleme" ? "c" : "n"}">${o.niveau}</span>` : "")
        + `</summary>${ctx.compilerSous(corps)}</details>`;
    case "encart":
      return `<div class="encart encart-${o.genre ?? "voir"}">`
        + (o.titre ? `<div class="titre">${o.titre}</div>` : "") + ctx.compilerSous(corps) + `</div>`;
    case "memo":
      return `<section class="memo">${ctx.compilerSous(corps)}</section>`;
    case "normatif":
      return `<div class="bloc-normatif">${ctx.compilerSous(corps)}</div>`;
    default:
      throw new Error(`directive inconnue « ${nom} »`);
  }
}

/* ---------- 4. compilation d'un module ---------- */
const balises = [];
const modules = [];

for (const f of readdirSync("content").filter((x) => x.endsWith(".md")).sort()) {
  const slug = f.replace(/\.md$/, "");
  const src = readFileSync(join("content", f), "utf8");

  // front-matter
  const fm = {};
  let corpsSrc = src;
  const mfm = src.match(/^---\n([\s\S]*?)\n---\n/);
  if (mfm) {
    for (const l of mfm[1].split("\n")) {
      const i = l.indexOf(":");
      if (i > 0) fm[l.slice(0, i).trim()] = l.slice(i + 1).trim();
    }
    corpsSrc = src.slice(mfm[0].length);
  }

  // § 3.2 : blocs normatifs non balises -> ECHEC
  for (const faute of controlerBlocsNormatifs(corpsSrc, f))
    erreurs.push(`${f} : nombre « ${faute.nombre} » non balise dans un bloc :::normatif — « ${faute.extrait} »`);

  // § 4.3 : accidents de gabarit (variable + chiffre colle, variable dans une formule,
  // repere de redaction) -> ECHEC
  for (const faute of controlerAccidentsDeGabarit(corpsSrc, f))
    erreurs.push(`${f} : ${faute.cause} — « ${faute.extrait} »`);

  // Les champs d'une balise peuvent porter une variable : on les resout avant
  // extraction, sinon le registre publierait « {{...}} » au lieu de la valeur.
  balises.push(...extraireBalises(
    corpsSrc.replace(/⟦[\s\S]*?⟧/g, (b) => substituerDans(b, f)), fm.id ?? slug));

  nFigure = 0;
  scripts.length = 0;
  const ctx = {
    math,
    compilerSous: (c) => compiler(c, ctx).html,
    directive: (n, o, c) => {
      try { return directive(n, o, c, ctx); }
      catch (e) { erreurs.push(`${f} : directive :::${n} — ${e.message}`); return ""; }
    },
  };
  let { html, titres } = compiler(corpsSrc, ctx);

  // injection des variables {{...}} : ECHEC si absente (§ 4.3)
  const substituer = (texte) => substituerDans(texte, f);
  html = substituer(html);

  const som = titres.map((t) =>
    `<li class="${t.niv >= 3 ? "niv2" : ""}"><a href="#${t.id}">${t.txt}</a></li>`).join("");

  let script = "";
  if (fm.donnees) {
    const embarque = {};
    for (const cle of fm.donnees.split(",").map((x) => x.trim()).filter(Boolean)) {
      try { embarque[cle] = resoudre(cle); }
      catch (e) { erreurs.push(`${f} : donnees embarquees « ${cle} » — ${e.message}`); }
    }
    script += `window.DONNEES=${JSON.stringify(embarque)};\n`;
  }
  for (const s of scripts) {
    const p = join("content", `${slug}.${s}.js`);
    if (!existsSync(p)) { erreurs.push(`${f} : script d'initialisation absent (${p})`); continue; }
    script += substituer(readFileSync(p, "utf8")) + "\n";
  }

  const gabarit = readFileSync("src/gabarits/module.html", "utf8");
  const page = gabarit
    .replace(/\{\{titre\}\}/g, fm.titre ?? slug)
    .replace(/\{\{resume\}\}/g, fm.resume ?? "")
    .replace(/\{\{id\}\}/g, fm.id ?? slug)
    .replace(/\{\{fil\}\}/g, fm.fil ?? "")
    .replace(/\{\{meta\}\}/g, fm.meta ?? "")
    .replace(/\{\{pied\}\}/g, fm.pied ?? "")
    .replace(/\{\{sommaire\}\}/g, som)
    .replace(/\{\{corps\}\}/g, html)
    .replace(/\{\{empreinte\}\}/g, EMPREINTE)
    .replace(/\{\{date\}\}/g, DATE)
    .replace(/\{\{script\}\}/g, script);

  if (/\{\{[^}]+\}\}/.test(page))
    erreurs.push(`${f} : variable de gabarit non remplacee — ${page.match(/\{\{[^}]+\}\}/)[0]}`);

  mkdirSync("modules", { recursive: true });
  writeFileSync(join("modules", `${slug}.html`), page);
  const ko = statSync(join("modules", `${slug}.html`)).size / 1024;
  if (ko > 1536) avertissements.push(`${slug}.html pese ${ko.toFixed(0)} ko (objectif <= 1500 ko, § 4.4)`);
  modules.push({ slug, ...fm, ko, figures: nFigure });
}

/* ---------- 5. registres GENERES depuis les balises (§ 3.2, Annexe 3) ---------- */
const lignesS = ["id;niveau;enonce_reformule;reference;modules;statut;date"];
const lignesH = ["id;hypothese;valeur;unite;fourchette;annee_ref;modules;justification"];
let nS = 0, nH = 0;
const nettoie = (s) => String(s).replace(/;/g, ",").replace(/\n/g, " ");
for (const b of balises) {
  if (b.niveau === "V3") {
    nH++;
    const [valeur, unite = "", fourchette = "", annee = "", justif = ""] = b.champs.slice(0);
    if (!fourchette || !annee)
      erreurs.push(`balise V3 « ${b.reference} » : fourchette et annee de reference sont exigees (§ 3.2)`);
    lignesH.push([`H${String(nH).padStart(3, "0")}`, nettoie(b.reference), nettoie(valeur),
      nettoie(unite), nettoie(fourchette), nettoie(annee), nettoie(b.module),
      nettoie(justif || b.reference)].join(";"));
  } else {
    nS++;
    const statut = b.niveau === "V0" ? "verifie sur source" : b.niveau === "V1" ? "recalcule par script" : "a verifier";
    lignesS.push(`S${String(nS).padStart(3, "0")};${b.niveau};${nettoie(b.enonce)};${nettoie(b.reference)};${nettoie(b.module)};${statut};${DATE}`);
  }
}
writeFileSync("data/registre-sources.csv", lignesS.join("\n") + "\n");
writeFileSync("data/registre-hypotheses.csv", lignesH.join("\n") + "\n");

/* ---------- 6. index ---------- */
const g = JSON.parse(readFileSync("data/projet-gare.json", "utf8"));
const phase = g.meta.normes_disponibles
  ? `<div class="encart encart-voir"><div class="titre">Phase</div><p>Normes disponibles : les modules de calcul sont actifs.</p></div>`
  : `<div class="encart encart-attente"><div class="titre">Phase sans calculs normatifs (§ 5.0)</div>
     <p>Les documents normatifs n'ont pas encore ete fournis : <code>normes_disponibles = false</code>.
     Tout calcul de dimensionnement ou de verification reglementaire est suspendu. Les modules de calcul
     restent au sommaire avec leur fiche, marques <span class="etiq etiq-pause">en attente des normes</span>,
     et aucun n'est ecrit. Le cours avance sur le suivi, l'execution, la planification, les couts,
     le BIM de suivi et la conception qualitative.</p></div>`;
const liste = modules.length
  ? `<table><thead><tr><th>Module</th><th>Titre</th><th>Type</th><th class="num">Figures</th><th class="num">Poids</th></tr></thead><tbody>`
    + modules.map((m) => `<tr><td><code>${m.id ?? m.slug}</code></td>`
      + `<td><a href="modules/${m.slug}.html">${m.titre ?? m.slug}</a></td>`
      + `<td>${m.type ?? ""}</td><td class="num">${m.figures}</td>`
      + `<td class="num">${m.ko.toFixed(0)} ko</td></tr>`).join("") + `</tbody></table>`
  : `<p>Aucun module livre.</p>`;
const etat = `<table><thead><tr><th>Element</th><th>Etat</th></tr></thead><tbody>`
  + `<tr><td>Jeu de donnees du cas phare</td><td><code>${g.meta.version}</code> — ${g.meta.statut.split(".")[0]}</td></tr>`
  + `<tr><td>Empreinte de <code>data/</code></td><td><code>${EMPREINTE}</code></td></tr>`
  + `<tr><td>Sources enregistrees (V0 a V2)</td><td class="num">${nS}</td></tr>`
  + `<tr><td>Hypotheses declarees (V3)</td><td class="num">${nH}</td></tr>`
  + `</tbody></table>`;
writeFileSync("index.html", readFileSync("src/gabarits/index.html", "utf8")
  .replace(/\{\{meta\}\}/g, `Mode B · phase § 5.0 · build du ${DATE}`)
  .replace(/\{\{phase\}\}/g, phase).replace(/\{\{liste\}\}/g, liste).replace(/\{\{etat\}\}/g, etat)
  .replace(/\{\{empreinte\}\}/g, EMPREINTE).replace(/\{\{date\}\}/g, DATE));

/* ---------- rapport ---------- */
console.log(`BUILD — ${modules.length} module(s), empreinte data/ ${EMPREINTE}`);
for (const m of modules) console.log(`  ${m.slug} — ${m.figures} figure(s), ${m.ko.toFixed(0)} ko`);
console.log(`  registres : ${nS} source(s), ${nH} hypothese(s)`);
for (const a of avertissements) console.log(`  ATTENTION  ${a}`);
if (erreurs.length) {
  console.log("");
  for (const e of erreurs) console.log(`  ECHEC  ${e}`);
  console.log(`\n${erreurs.length} erreur(s) — le build echoue (§ 4.3).`);
  process.exit(1);
}
console.log("Build OK.");
