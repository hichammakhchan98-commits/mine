import { test, expect } from "@playwright/test";
import { readdirSync, readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { resolve, join } from "node:path";

/* Controle du rendu reel (§ 12.1 a a e, § 9.4).
   Les pages sont chargees en file:// : c'est la preuve que le cours fonctionne hors ligne. */

const RACINE = resolve(".");
const CAPTURES = join(RACINE, "tests", "captures");
mkdirSync(CAPTURES, { recursive: true });

const modules = readdirSync(join(RACINE, "modules")).filter((f) => f.endsWith(".html"));
const EMPREINTE_ATTENDUE = readFileSync(join(RACINE, "index.html"), "utf8")
  .match(/Empreinte des donn[eé]es\s*:\s*<code>([0-9a-f]+)<\/code>/)[1];

const rapport = [];

for (const fichier of modules) {
  test.describe(fichier, () => {
    let page, erreurs, requetesExternes;

    test.beforeEach(async ({ browser }) => {
      page = await browser.newPage();
      erreurs = [];
      requetesExternes = [];
      page.on("console", (m) => {
        if (m.type() === "error" || m.type() === "warning") erreurs.push(`${m.type()}: ${m.text()}`);
      });
      page.on("pageerror", (e) => erreurs.push(`pageerror: ${e.message}`));
      // § 12.1 e : aucune requete reseau externe
      page.on("request", (r) => {
        const u = r.url();
        if (!u.startsWith("file://") && !u.startsWith("data:") && !u.startsWith("blob:"))
          requetesExternes.push(u);
      });
      await page.addInitScript(() => { window.__CIVIL3D_TEST__ = true; });
      await page.goto(pathToFileURL(join(RACINE, "modules", fichier)).href);
      await page.waitForLoadState("load");
    });

    /* La scene 3D n'est initialisee qu'a l'affichage (IntersectionObserver) : il faut
       l'amener dans le cadre, exactement comme un lecteur qui fait defiler la page. */
    const preparerVue = async () => {
      if (!(await page.locator(".vue3d").count())) return false;
      await page.locator(".vue3d").scrollIntoViewIfNeeded();
      await page.waitForFunction(() => document.querySelector(".vue3d")?.dataset.pret === "1",
        null, { timeout: 30_000 });
      return true;
    };

    test.afterEach(async () => { await page?.close(); });

    test("a · zero erreur de console, zero requete externe, contexte WebGL", async () => {
      if (await preparerVue()) {
        const webgl = await page.evaluate(() => {
          const c = document.querySelector(".vue3d-toile");
          return !!(c && (c.getContext("webgl2") || c.getContext("webgl")));
        });
        expect(webgl, "un contexte WebGL doit etre cree quand le module porte un modele 3D").toBe(true);
      }
      expect(requetesExternes, "le cours doit fonctionner hors ligne").toEqual([]);
      expect(erreurs, "aucune erreur ni avertissement de console").toEqual([]);
    });

    test("j · empreinte de data/ identique a celle de l'index", async () => {
      const emp = await page.locator(".pied code").first().textContent();
      expect(emp.trim()).toBe(EMPREINTE_ATTENDUE);
    });

    test("g · liens internes valides", async () => {
      const liens = await page.$$eval("a[href]", (as) => as.map((a) => a.getAttribute("href")));
      const ancres = await page.$$eval("[id]", (es) => es.map((e) => e.id));
      for (const h of liens.filter((x) => x.startsWith("#")))
        expect(ancres, `ancre ${h} introuvable`).toContain(h.slice(1));
    });

    test("c · textes SVG sans chevauchement, legendes completes", async () => {
      const res = await page.evaluate(() => {
        const out = [];
        document.querySelectorAll("figure svg").forEach((svg, i) => {
          const textes = [...svg.querySelectorAll("text")].map((t) => {
            const b = t.getBBox();
            return { t: t.textContent, x: b.x, y: b.y, l: b.width, h: b.height,
              puce: t.classList.contains("puce"), leg: t.classList.contains("leg-num") };
          });
          const chevauche = [];
          for (let a = 0; a < textes.length; a++)
            for (let b = a + 1; b < textes.length; b++) {
              const A = textes[a], B = textes[b];
              // une puce et son numero de legende portent le meme texte a des endroits differents :
              // on compare bien les boites, pas les contenus
              const inter = A.x < B.x + B.l && B.x < A.x + A.l && A.y < B.y + B.h && B.y < A.y + A.h;
              if (inter) chevauche.push(`« ${A.t} » / « ${B.t} »`);
            }
          out.push({ i: i + 1, textes: textes.length, chevauche,
            puces: textes.filter((t) => t.puce).map((t) => t.t),
            legNums: textes.filter((t) => t.leg).map((t) => t.t) });
        });
        return out;
      });
      for (const f of res) {
        expect(f.chevauche, `figure ${f.i} : textes qui se chevauchent`).toEqual([]);
        if (f.legNums.length)
          for (const p of f.puces)
            expect(f.legNums, `figure ${f.i} : puce ${p} absente de la legende`).toContain(p);
      }
      rapport.push({ fichier, figures: res.map((f) => ({ n: f.i, textes: f.textes })) });
    });

    test("b, c · recette du modele 3D : etats, captures non vides, etiquettes", async () => {
      if (!(await preparerVue())) { test.skip(); return; }

      const etats = [];
      const regler = async (reglages) => {
        await page.evaluate((r) => {
          const v = Civil3D.vues()[0];
          for (const [cle, val] of Object.entries(r)) v.reglerCurseur(cle, val);
        }, reglages);
        await page.waitForTimeout(350);
      };
      const mesurer = async (nom) => {
        const d = await page.evaluate(() => {
          const v = Civil3D.vues()[0];
          return { diag: v.diagnostic(), variance: v.varianceRendu() };
        });
        await page.locator(".vue3d").screenshot({ path: join(CAPTURES, `${fichier}-${nom}.png`) });
        etats.push({ nom, ...d });
        return d;
      };

      // bornes des curseurs, pour les tester AUX bornes (§ 9.4)
      const bornes = await page.evaluate(() => {
        const v = Civil3D.vues()[0], o = {};
        for (const cle of Object.keys(v.curseurs ?? {})) o[cle] = v.bornes(cle);
        return o;
      });

      await mesurer("defaut");
      await regler({ __coupe: 0.5 });      await mesurer("coupe");
      await regler({ __coupe: 0 , __eclate: 1 }); await mesurer("eclate");
      await regler({ __eclate: 0, __phase: 1 }); await mesurer("phase1");
      await regler({ __phase: 2 });        await mesurer("phase2");
      await regler({ __phase: 4 });        await mesurer("phase4");

      const auxBornes = {};
      for (const [cle, b] of Object.entries(bornes)) if (!cle.startsWith("__")) auxBornes[cle] = b.min;
      await regler(auxBornes);             await mesurer("curseurs-min");
      for (const [cle, b] of Object.entries(bornes)) if (!cle.startsWith("__")) auxBornes[cle] = b.max;
      await regler(auxBornes);             await mesurer("curseurs-max");

      for (const e of etats) {
        expect(e.variance, `${e.nom} : la scene est vide (variance de pixels nulle)`).toBeGreaterThan(2);
        expect(e.diag.triangles, `${e.nom} : budget de triangles depasse (§ 4.4)`).toBeLessThanOrEqual(150_000);
        expect(e.diag.etiquettes.chevauchements, `${e.nom} : etiquettes 3D qui se chevauchent`).toBe(0);
        expect(e.diag.etiquettes.visibles, `${e.nom} : aucune etiquette visible`).toBeGreaterThan(0);
        expect(e.diag.repli, `${e.nom} : la vue est tombee en repli`).toBe(false);
        expect(e.diag.contextesVivants, "plafond de contextes WebGL").toBeLessThanOrEqual(4);
      }
      // le phasage doit reellement changer la scene
      const v1 = etats.find((e) => e.nom === "phase1").variance;
      const v4 = etats.find((e) => e.nom === "phase4").variance;
      expect(Math.abs(v1 - v4), "la phase 1 et la phase 4 rendent la meme image : le phasage ne fait rien")
        .toBeGreaterThan(0.5);

      expect(erreurs, "aucune erreur de console pendant le pilotage du modele").toEqual([]);
      writeFileSync(join(CAPTURES, `${fichier}-etats.json`),
        JSON.stringify(etats.map((e) => ({ nom: e.nom, variance: Number(e.variance.toFixed(2)),
          triangles: e.diag.triangles, etiquettes: e.diag.etiquettes, params: e.diag.params })), null, 2));
    });

    test("d · coherence des donnees : le metre affiche = la sortie de calc/", async () => {
      const metre = JSON.parse(readFileSync(join(RACINE, "calc", "sorties", "metre-cage.json"), "utf8"));
      const txt = (await page.locator(".corps").innerText()).replace(/ /g, " ");
      const attendu = metre.masse_acier_kg.toFixed(1).replace(".", ",");
      expect(txt, `la masse d'acier ${attendu} kg doit figurer dans la page`).toContain(attendu);
      if (await preparerVue()) {
        const m3d = await page.evaluate(() => Civil3D.vues()[0].diagnostic().metre);
        // meme geometrie, deux implementations (python et javascript) : ecart <= 1 %
        const e = Math.abs(m3d.masseAcier_kg - metre.masse_acier_kg) / metre.masse_acier_kg * 100;
        expect(e, `metre 3D ${m3d.masseAcier_kg.toFixed(2)} kg contre calc/ ${metre.masse_acier_kg} kg`)
          .toBeLessThan(1);
        expect(m3d.nCadres, "nombre de cadres : 3D contre calc/").toBe(metre.n_cadres);
      }
    });
  });
}
