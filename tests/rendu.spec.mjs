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
      // l'eclate se capture a la phase 3, sinon le coffrage est deja retire et la vue
      // ne montre que deux couches sur trois
      await regler({ __coupe: 0, __eclate: 1, __phase: 3 }); await mesurer("eclate");
      await regler({ __phase: 4 });
      await regler({ __eclate: 0, __phase: 1 }); await mesurer("phase1");
      await regler({ __phase: 2 });        await mesurer("phase2");
      await regler({ __phase: 4 });        await mesurer("phase4");

      // chaque curseur a ses bornes, LES AUTRES AU DEFAUT : un reglage en bloc masque
      // les combinaisons qui degenerent
      const defauts = await page.evaluate(() => {
        const v = Civil3D.vues()[0], o = {};
        for (const [cle, c] of Object.entries(v.curseurs ?? {})) if (!cle.startsWith("__")) o[cle] = c.p.valeur;
        return o;
      });
      for (const [cle, b] of Object.entries(bornes)) {
        if (cle.startsWith("__")) continue;
        await regler({ ...defauts, [cle]: b.min }); await mesurer(`${cle}-min`);
        await regler({ ...defauts, [cle]: b.max }); await mesurer(`${cle}-max`);
      }
      // pire cas explicite : le plus long troncon avec les cadres les plus serres
      const pire = { ...defauts };
      for (const [cle, b] of Object.entries(bornes)) {
        if (cle.startsWith("__")) continue;
        pire[cle] = cle.includes("esp") ? b.min : b.max;     // long + serre + gros diametres
      }
      await regler(pire);                  await mesurer("pire-cas");

      for (const e of etats) {
        // seuil cale sur les valeurs reellement observees (16 a 45) et non sur une marge
        // symbolique : a 2, un rendu quasi blanc passait
        expect(e.variance, `${e.nom} : la scene est quasi vide`).toBeGreaterThan(8);
        expect(e.diag.triangles, `${e.nom} : budget de triangles depasse (§ 4.4)`).toBeLessThanOrEqual(150_000);
        expect(e.diag.etiquettes.chevauchements, `${e.nom} : etiquettes 3D qui se chevauchent`).toBe(0);
        // « zero chevauchement » ne prouve rien avec une seule etiquette : on exige
        // qu'au moins un etat dense en porte plusieurs (verifie apres la boucle)
        expect(e.diag.etiquettes.visibles, `${e.nom} : aucune etiquette visible`).toBeGreaterThan(0);
        expect(e.diag.repli, `${e.nom} : la vue est tombee en repli`).toBe(false);
        expect(e.diag.contextesVivants, "plafond de contextes WebGL").toBeLessThanOrEqual(4);
      }
      // le phasage doit reellement changer la scene
      const v1 = etats.find((e) => e.nom === "phase1").variance;
      const v4 = etats.find((e) => e.nom === "phase4").variance;
      expect(Math.abs(v1 - v4), "la phase 1 et la phase 4 rendent la meme image : le phasage ne fait rien")
        .toBeGreaterThan(0.5);

      const dense = etats.filter((e) => e.diag.etiquettes.visibles >= 3);
      expect(dense.length,
        "aucun etat ne porte 3 etiquettes ou plus : le controle de chevauchement ne teste rien")
        .toBeGreaterThan(0);
      expect(erreurs, "aucune erreur de console pendant le pilotage du modele").toEqual([]);
      writeFileSync(join(CAPTURES, `${fichier}-etats.json`),
        JSON.stringify(etats.map((e) => ({ nom: e.nom, variance: Number(e.variance.toFixed(2)),
          triangles: e.diag.triangles, etiquettes: e.diag.etiquettes, params: e.diag.params })), null, 2));
    });

    test("d · geometrie : positions SVG et 3D recalculees depuis data/ (§ 12.1 d)", async () => {
      // Sans ce test, deux erreurs geometriques injectees (barres empilees en SVG,
      // enrobage ignore en 3D) franchissaient les neuf controles sans en allumer un seul.
      const data = JSON.parse(readFileSync(join(RACINE, "data", "demo-cage.json"), "utf8"));

      // Les attendus sont recalcules ICI, a la main, depuis data/ et la convention publiee.
      // Ils n'appellent PAS section.js : sinon le test compare le produit a lui-meme et un
      // canari place dans section.js deplacerait l'attendu avec le resultat. C'est la
      // « limite et parade » du § 3.3 appliquee a un test de rendu.
      const attendu = (() => {
        const { b_cm: b, h_cm: h, enrobage_cm: e, inf, sup } = data.section;
        const dc = data.cadres.dia_mm / 10;                  // diametre du cadre, en cm
        const axe = { b: b - 2 * (e + dc / 2), h: h - 2 * (e + dc / 2) };
        const libre = b - 2 * (e + dc);                      // largeur libre dans le cadre
        const barres = [];
        for (const [nappe, bas] of [[inf, true], [sup, false]]) {
          const d = nappe.dia_mm / 10;
          const y = bas ? -h / 2 + e + dc + d / 2 : h / 2 - e - dc - d / 2;
          const dispo = libre - d;
          for (let i = 0; i < nappe.n; i++)
            barres.push({ x_cm: nappe.n === 1 ? 0 : -dispo / 2 + (dispo * i) / (nappe.n - 1),
              y_cm: y, dia_mm: nappe.dia_mm });
        }
        return { axe_cadre_cm: axe, barres };
      })();

      // --- SVG : l'echelle se deduit du RECTANGLE DE SECTION, dont les cotes sont connues
      // par data/. La deduire des barres elles-memes, comme le faisait la version
      // precedente, absorbait toute homothetie ou translation du groupe de barres :
      // un decalage de 10 cm en hauteur et un resserrement de 20 % passaient.
      const svg = await page.evaluate(() => {
        const s = document.querySelector("figure svg");
        const rects = [...s.querySelectorAll("rect")].map((r) => ({
          x: +r.getAttribute("x"), y: +r.getAttribute("y"),
          l: +r.getAttribute("width"), h: +r.getAttribute("height") }));
        const cercles = [...s.querySelectorAll("circle")]
          .filter((c) => c.getAttribute("fill") === "#8c3b2e")
          .map((c) => ({ cx: +c.getAttribute("cx"), cy: +c.getAttribute("cy"), r: +c.getAttribute("r") }));
        return { rects, cercles };
      });
      expect(svg.cercles.length, "nombre de barres dessinees en SVG").toBe(attendu.barres.length);

      const section = svg.rects.reduce((a, r) => (r.l * r.h > a.l * a.h ? r : a), svg.rects[0]);
      const kx = section.l / data.section.b_cm, ky = section.h / data.section.h_cm;
      expect(Math.abs(kx - ky) / kx, "la section SVG n'est pas a l'echelle").toBeLessThan(0.01);
      const cx0 = section.x + section.l / 2, cy0 = section.y + section.h / 2;
      const ecarts = attendu.barres.map((b, i) => ({
        dx: Math.abs((cx0 + b.x_cm * kx) - svg.cercles[i].cx) / kx,
        dy: Math.abs((cy0 - b.y_cm * ky) - svg.cercles[i].cy) / ky,   // y inverse en SVG
      }));
      expect(Math.max(...ecarts.map((e) => e.dx)), "abscisse des barres en SVG (cm)").toBeLessThan(0.02);
      expect(Math.max(...ecarts.map((e) => e.dy)), "ordonnee des barres en SVG (cm)").toBeLessThan(0.02);
      // le rayon dessine doit etre celui du diametre reel
      const ecartsR = attendu.barres.map((b, i) =>
        Math.abs(svg.cercles[i].r / kx - b.dia_mm / 20));
      expect(Math.max(...ecartsR), "rayon des barres en SVG (cm)").toBeLessThan(0.05);

      // --- 3D : positions reelles contre la regle
      if (await preparerVue()) {
        const diag = await page.evaluate(() => Civil3D.vues()[0].diagnostic());
        expect(diag.barres.length, "nombre de barres en 3D").toBe(attendu.barres.length);
        const pires = attendu.barres.map((b, i) =>
          Math.hypot(b.x_cm - diag.barres[i].x, b.y_cm - diag.barres[i].y));
        expect(Math.max(...pires),
          `position des barres en 3D (cm) — attendu ${JSON.stringify(attendu.barres.map((b) => [b.x_cm, b.y_cm]))}`)
          .toBeLessThan(0.001);
        expect(Math.abs(diag.axeCadre.b - attendu.axe_cadre_cm.b), "axe du cadre en 3D").toBeLessThan(0.001);
        // le tube du cadre doit avoir le DIAMETRE annonce : sans cette mesure, le defaut
        // B1 (un /2 applique deux fois) revient en silence
        const tube = await page.evaluate(() => {
          let r = null;
          Civil3D.vues()[0].contenu.groupe.traverse((o) => { if (o.name === "cadres") r = o.geometry.parameters.radius; });
          return r;
        });
        expect(tube * 2000, `diametre du tube du cadre (mm), attendu ${data.cadres.dia_mm}`)
          .toBeCloseTo(data.cadres.dia_mm, 3);
        // l'enrobage annonce doit etre celui que la geometrie realise
        const peau = (data.section.b_cm - diag.axeCadre.b) / 2 - data.cadres.dia_mm / 20;
        expect(Math.abs(peau - data.section.enrobage_cm), "enrobage realise en 3D").toBeLessThan(0.001);
      }
    });

    test("d · coherence des donnees : le metre affiche = la sortie de calc/", async () => {
      const metre = JSON.parse(readFileSync(join(RACINE, "calc", "sorties", "metre-cage.json"), "utf8"));
      const data = JSON.parse(readFileSync(join(RACINE, "data", "demo-cage.json"), "utf8"));

      // Le nombre de cadres est recalcule ICI, a la main. Les deux voies du contre-calcul
      // le PARTAGENT : un comptage faux des deux cotes y passe inapercu. C'est ce controle,
      // independant, qui l'attrape.
      const retrait = data.section.enrobage_cm + data.cadres.dia_mm / 20;
      const utile = data.troncon.L_cm - 2 * retrait;
      const nAttendu = Math.max(2, Math.ceil(utile / data.cadres.espacement_cm) + 1);
      expect(metre.n_cadres, `nombre de cadres recalcule depuis data/ : ${nAttendu}`).toBe(nAttendu);
      const espReel = utile / (nAttendu - 1);
      expect(espReel, "l'espacement reel doit rester sous le nominal")
        .toBeLessThanOrEqual(data.cadres.espacement_cm + 1e-9);
      expect(Math.abs(metre.espacement_reel_cm - espReel), "espacement reel").toBeLessThan(0.01);
      const txt = (await page.locator(".corps").innerText()).replace(/ /g, " ");
      const attendu = metre.masse_acier_kg.toFixed(1).replace(".", ",");
      expect(txt, `la masse d'acier ${attendu} kg doit figurer dans la page`).toContain(attendu);
      if (await preparerVue()) {
        const m3d = await page.evaluate(() => Civil3D.vues()[0].diagnostic().metre);
        // Meme geometrie, deux implementations (Python et JavaScript). La tolerance etait
        // de 1 % : une divergence de la regle de cintrage entre les deux (16 mm contre
        // 20 mm, soit 0,35 %) serait passee sans bruit. A 0,1 %, elle ne passe plus.
        const e = Math.abs(m3d.masseAcier_kg - metre.masse_acier_kg) / metre.masse_acier_kg * 100;
        expect(e, `metre 3D ${m3d.masseAcier_kg.toFixed(3)} kg contre calc/ ${metre.masse_acier_kg} kg`)
          .toBeLessThan(0.1);
        // et le perimetre lui-meme, qui est la grandeur ou les deux codes peuvent diverger
        const ep = Math.abs(m3d.longueurCadre_m - metre.perimetre_cadre_m) / metre.perimetre_cadre_m * 100;
        expect(ep, `perimetre 3D ${m3d.longueurCadre_m.toFixed(5)} m contre calc/ ${metre.perimetre_cadre_m} m`)
          .toBeLessThan(0.05);
        expect(m3d.nCadres, "nombre de cadres : 3D contre calc/").toBe(metre.n_cadres);
      }
    });
  });
}
