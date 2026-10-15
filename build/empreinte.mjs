/* Empreinte de data/ (§ 4.3) : tout module affiche ce hash ; check.mjs signale les modules perimes. */
import { readdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { join } from "node:path";

export function empreinteData(dir = "data") {
  const h = createHash("sha256");
  const parcours = (d) => {
    for (const e of readdirSync(d, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const p = join(d, e.name);
      if (e.isDirectory()) parcours(p);
      else if (/\.(json|csv)$/.test(e.name)) { h.update(e.name); h.update(readFileSync(p)); }
    }
  };
  parcours(dir);
  return h.digest("hex").slice(0, 12);
}

if (import.meta.url === `file://${process.argv[1]}`) console.log(empreinteData());
