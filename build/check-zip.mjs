/* § 12.1 k — en mode B, le zip de reprise doit s'ouvrir et le projet repasser au vert.
   On fabrique le zip, on le deplie dans un repertoire neuf, et on y rejoue la sequence
   de reprise du § 12.5 B2 : npm ci --ignore-scripts && npm run check. */
import { execFileSync } from "node:child_process";
import { mkdtempSync, rmSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const ZIP = "cours-genie-civil-P1-E1-socle.zip";
const sh = (cmd, args, cwd) =>
  execFileSync(cmd, args, { cwd, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });

rmSync(ZIP, { force: true });
sh("zip", ["-rq", ZIP, ".", "-x", "node_modules/*", "tests/captures/*", "test-results/*", "*.zip"], ".");

const tmp = mkdtempSync(join(tmpdir(), "reprise-"));
try {
  sh("unzip", ["-q", join(process.cwd(), ZIP), "-d", tmp], ".");
  for (const f of ["CLAUDE.md", "STATE.md", "DECISIONS.md", "package-lock.json"])
    if (!existsSync(join(tmp, f))) throw new Error(`${f} absent du zip`);
  if (!existsSync(join(tmp, ".git"))) throw new Error(".git absent du zip (§ 12.5 B1)");
  sh("npm", ["ci", "--ignore-scripts", "--no-audit", "--no-fund"], tmp);
  // dans la copie, on ne refait pas le controle du zip : sinon la verification se rappellerait
  sh("npm", ["run", "check", "--", "--sans-zip"], tmp);
  console.log(`zip ${ZIP} : rouvert dans un repertoire neuf, npm ci puis npm run check au vert`);
} finally {
  rmSync(tmp, { recursive: true, force: true });
}
