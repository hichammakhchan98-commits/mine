/* Bundle IIFE de la bibliotheque 3D (§ 4.4).
   Les modules ES et fetch() de fichiers locaux echouent en file:// : on livre un IIFE. */
import { build } from "esbuild";
import { cpSync, mkdirSync, readFileSync, readdirSync, writeFileSync, statSync } from "node:fs";

const r = await build({
  entryPoints: ["src/civil3d.entry.js"],
  bundle: true, format: "iife", globalName: "Civil3D", minify: true,
  target: ["es2020"], outfile: "assets/civil3d.bundle.js",
  legalComments: "none", metafile: true,
});
const o = Object.values(r.metafile.outputs)[0];
console.log(`assets/civil3d.bundle.js — ${(o.bytes / 1024).toFixed(0)} ko`);

/* KaTeX : CSS + polices woff2 en local, zero CDN, zero JS d'execution. */
mkdirSync("assets/katex/fonts", { recursive: true });
cpSync("node_modules/katex/dist/katex.min.css", "assets/katex/katex.min.css");
let n = 0;
for (const f of readdirSync("node_modules/katex/dist/fonts"))
  if (f.endsWith(".woff2")) { cpSync(`node_modules/katex/dist/fonts/${f}`, `assets/katex/fonts/${f}`); n++; }
// Les declarations woff/ttf pointeraient vers des fichiers absents : on ne garde que woff2.
const css = readFileSync("assets/katex/katex.min.css", "utf8")
  .replace(/,url\([^)]*\.woff\)\s*format\("woff"\)/g, "")
  .replace(/,url\([^)]*\.ttf\)\s*format\("truetype"\)/g, "");
writeFileSync("assets/katex/katex.min.css", css);
console.log(`assets/katex — ${n} polices woff2, css ${(statSync("assets/katex/katex.min.css").size / 1024).toFixed(0)} ko`);
