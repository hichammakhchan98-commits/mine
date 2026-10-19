/* svgkit.js — fonctions SVG parametriques (§ 8).
   Regle R2 : un schema est PRODUIT a partir des donnees, jamais dessine a l'oeil.
   Aucune cote n'est ecrite en dur ici : tout vient des arguments.
   Sortie : chaine SVG. Utilisable au build (Node) comme dans le navigateur. */

(function (racine) {
  "use strict";

  // ---------- outils ----------
  const ech = (v) => Math.round(v * 100) / 100;          // 2 decimales : SVG plus leger
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  /** Convertisseur metre -> pixel, avec marges. */
  function repere({ largeur, hauteur, marge = 40, margeDroite, xmin, xmax, ymin, ymax,
                    yInverse = true, libre = false }) {
    const dx = xmax - xmin || 1, dy = ymax - ymin || 1;
    const md = margeDroite ?? marge;
    const lu = largeur - marge - md, hu = hauteur - 2 * marge;
    // `libre` : echelles X et Y independantes. Un PLAN garde son rapport d'aspect — une
    // coupe ecrasee serait fausse. Un GRAPHIQUE n'en a pas : l'axe des jours et l'axe des
    // pourcents n'ont aucun rapport commun, et en imposer un tasse la courbe dans un coin.
    const kx = libre ? lu / dx : Math.min(lu / dx, hu / dy);
    const ky = libre ? hu / dy : kx;
    const ox = marge + (libre ? 0 : (lu - kx * dx) / 2);
    const oy = marge + (libre ? 0 : (hu - ky * dy) / 2);
    return {
      k: kx, kx, ky,
      x: (xm) => ech(ox + (xm - xmin) * kx),
      y: (ym) => ech(yInverse ? oy + (ymax - ym) * ky : oy + (ym - ymin) * ky),
      l: (m) => ech(m * kx),
    };
  }

  // ---------- motifs de materiaux : definis UNE SEULE FOIS (§ 8) ----------
  const MOTIFS = {
    beton: `<pattern id="m-beton" width="7" height="7" patternUnits="userSpaceOnUse">
      <rect width="7" height="7" fill="#e7e8e3"/>
      <circle cx="2" cy="2.5" r=".7" fill="#b9bbb4"/><circle cx="5.4" cy="5" r=".5" fill="#b9bbb4"/></pattern>`,
    sol: `<pattern id="m-sol" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <rect width="8" height="8" fill="#efe7d8"/><path d="M0 0v8" stroke="#a08358" stroke-width=".8"/></pattern>`,
    acier: `<pattern id="m-acier" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <rect width="6" height="6" fill="#dfe5ea"/><path d="M0 0v6" stroke="#41607d" stroke-width="1"/></pattern>`,
    remblai: `<pattern id="m-remblai" width="10" height="10" patternUnits="userSpaceOnUse">
      <rect width="10" height="10" fill="#f3efe6"/><path d="M0 7h10M5 7l-2 3M5 7l2 3" stroke="#a08358"
      stroke-width=".7" fill="none"/></pattern>`,
  };

  /** Enveloppe SVG. `motifs` : liste de cles de MOTIFS a inclure. */
  function svg({ largeur, hauteur, titre, desc, motifs = [], contenu, classe = "" }) {
    const defs = motifs.map((m) => MOTIFS[m] || "").join("\n");
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${largeur} ${hauteur}" `
      + `role="img" aria-labelledby="t-${titre ? hash(titre) : "x"}" class="${classe}">`
      + (titre ? `<title id="t-${hash(titre)}">${esc(titre)}</title>` : "")
      + (desc ? `<desc>${esc(desc)}</desc>` : "")
      + (defs ? `<defs>${defs}${fleches()}</defs>` : `<defs>${fleches()}</defs>`)
      + contenu + "</svg>";
  }
  const hash = (s) => { let h = 0; for (const c of String(s)) h = (h * 31 + c.charCodeAt(0)) | 0;
    return Math.abs(h).toString(36); };

  const fleches = () => `
    <marker id="fl" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0.8 L7.5 4 L0 7.2 z" fill="currentColor"/></marker>
    <marker id="fl-deb" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M8 0.8 L0.5 4 L8 7.2 z" fill="currentColor"/></marker>`;

  // ---------- primitives ----------
  const texte = (x, y, t, o = {}) =>
    `<text x="${ech(x)}" y="${ech(y)}" font-family="${o.mono ? "ui-monospace,monospace" : "sans-serif"}" `
    + `font-size="${o.taille || 11}" font-weight="${o.gras ? 600 : 400}" `
    + `fill="${o.couleur || "#14181d"}" text-anchor="${o.ancre || "start"}" `
    + `dominant-baseline="${o.base || "auto"}"${o.classe ? ` class="${o.classe}"` : ""}>${esc(t)}</text>`;

  const ligne = (x1, y1, x2, y2, o = {}) =>
    `<line x1="${ech(x1)}" y1="${ech(y1)}" x2="${ech(x2)}" y2="${ech(y2)}" `
    + `stroke="${o.couleur || "#14181d"}" stroke-width="${o.ep || 1}"`
    + (o.tirets ? ` stroke-dasharray="${o.tirets}"` : "") + (o.marqueur ? ` marker-end="url(#fl)"` : "")
    + (o.marqueurDeb ? ` marker-start="url(#fl-deb)"` : "") + ` />`;

  const rect = (x, y, l, h, o = {}) =>
    `<rect x="${ech(x)}" y="${ech(y)}" width="${ech(l)}" height="${ech(h)}" `
    + `fill="${o.remplissage || "none"}" stroke="${o.couleur || "#14181d"}" `
    + `stroke-width="${o.ep || 1}"${o.rayon ? ` rx="${o.rayon}"` : ""} />`;

  const cercle = (x, y, r, o = {}) =>
    `<circle cx="${ech(x)}" cy="${ech(y)}" r="${ech(r)}" fill="${o.remplissage || "#14181d"}"`
    + (o.couleur ? ` stroke="${o.couleur}" stroke-width="${o.ep || 1}"` : "") + ` />`;

  const chemin = (d, o = {}) =>
    `<path d="${d}" fill="${o.remplissage || "none"}" stroke="${o.couleur || "#14181d"}" `
    + `stroke-width="${o.ep || 1}"` + (o.tirets ? ` stroke-dasharray="${o.tirets}"` : "")
    + (o.jointure ? ` stroke-linejoin="${o.jointure}"` : "") + ` />`;

  /** Cote avec traits de rappel. `val` est TOUJOURS fournie par les donnees. */
  function cote(x1, y1, x2, y2, val, o = {}) {
    const d = o.decalage || 0;
    const horiz = Math.abs(y2 - y1) < Math.abs(x2 - x1);
    const [ax, ay, bx, by] = horiz ? [x1, y1 + d, x2, y2 + d] : [x1 + d, y1, x2 + d, y2];
    const mx = (ax + bx) / 2, my = (ay + by) / 2;
    return `<g color="${o.couleur || "#3f4852"}">`
      + ligne(x1, y1, ax, ay, { couleur: "#a8aca4", ep: .6 })
      + ligne(x2, y2, bx, by, { couleur: "#a8aca4", ep: .6 })
      + ligne(ax, ay, bx, by, { couleur: o.couleur || "#3f4852", ep: .7, marqueur: 1, marqueurDeb: 1 })
      + texte(mx + (horiz ? 0 : 6), my - (horiz ? 4 : 0), val,
        { taille: 10.5, mono: 1, ancre: horiz ? "middle" : "start", couleur: o.couleur || "#3f4852" })
      + `</g>`;
  }

  /** Legende numerotee : chaque numero du dessin DOIT y figurer (§ 8, grille de qualite). */
  function legende(x, y, entrees, o = {}) {
    const pas = o.pas || 15;
    return `<g>` + entrees.map((e, i) =>
      cercle(x + 6, y + i * pas, 6.5, { remplissage: "#fff", couleur: "#14181d", ep: .9 })
      + texte(x + 6, y + i * pas + .5, String(e.n),
        { taille: 9, gras: 1, ancre: "middle", base: "middle", classe: "leg-num" })
      + texte(x + 18, y + i * pas + .5, e.t, { taille: 11, base: "middle", classe: "leg-txt" })
      ).join("") + `</g>`;
  }

  /** Puce numerotee a poser sur le dessin. */
  const puce = (x, y, n) =>
    cercle(x, y, 7, { remplissage: "#fbfbf9", couleur: "#14181d", ep: .9 })
    + texte(x, y + .5, String(n), { taille: 9, gras: 1, ancre: "middle", base: "middle", classe: "puce" });

  // ---------- schemas composes ----------

  /**
   * Coupe de section rectangulaire ferraillee.
   * Les positions ne sont PAS recalculees ici : elles viennent de SectionGeom
   * (assets/section.js), la meme routine que la 3D. Avant, cette fonction posait les
   * barres a l'enrobage en ignorant l'epaisseur du cadre, pendant que la 3D la comptait :
   * deux geometries differentes a partir du meme fichier de donnees.
   */
  function coupeSection(d, o = {}) {
    const SG = (typeof globalThis !== "undefined" && globalThis.SectionGeom) || null;
    if (!SG) throw new Error("coupeSection : assets/section.js doit etre charge avant svgkit.js");
    // `d` est le jeu de donnees complet : section, cadres et conventions en viennent tous.
    const s = d.section, cad = d.cadres, cv = d.conventions;
    if (!s || !cad || !cv)
      throw new Error("coupeSection : attend un jeu de donnees { section, cadres, conventions }");
    const conv = { dia_cadre_mm: cad.dia_mm, rayon_cintrage_mm: cv.rayon_cintrage_mm };
    const g = SG.positionsArmatures(s, conv);
    const L = o.largeur || 300, H = o.hauteur || 340;
    const b = s.b_cm, h = s.h_cm, e = s.enrobage_cm;
    const r = repere({ largeur: L, hauteur: H, marge: 56, xmin: -b / 2, xmax: b / 2, ymin: -h / 2, ymax: h / 2 });

    let out = rect(r.x(-b / 2), r.y(h / 2), r.l(b), r.l(h),
      { remplissage: "url(#m-beton)", ep: 1.4 });

    // cadre : trace sur son AXE, avec le rayon de cintrage des donnees (et non une
    // valeur en pixels choisie a l'oeil), epaisseur = diametre reel du cadre
    const pts = SG.contourCadre(g.axe_cadre_cm.b, g.axe_cadre_cm.h, g.rayon_cintrage_cm, 8, 2);
    const trace = pts.map((p, i) => `${i ? "L" : "M"}${r.x(p[0])} ${r.y(p[1])}`).join(" ") + " Z";
    out += chemin(trace, { couleur: "#8c3b2e", ep: Math.max(1.2, r.l(g.dia_cadre_cm)), jointure: "round" });

    // barres : une par position fournie par la regle
    const barres = g.barres.map((bar) => ({
      x: r.x(bar.x_cm), y: r.y(bar.y_cm), r: Math.max(2.4, r.l(bar.dia_mm / 20)), dia: bar.dia_mm,
    }));
    out += barres.map((p) => cercle(p.x, p.y, p.r, { remplissage: "#8c3b2e" })).join("");

    // cotes, toutes issues des donnees
    out += cote(r.x(-b / 2), r.y(-h / 2), r.x(b / 2), r.y(-h / 2), `b = ${b} cm`, { decalage: 26 });
    out += cote(r.x(b / 2), r.y(-h / 2), r.x(b / 2), r.y(h / 2), `h = ${h} cm`, { decalage: 30 });
    out += cote(r.x(-b / 2), r.y(h / 2), r.x(-b / 2 + e), r.y(h / 2), `${e}`, { decalage: -16 });

    out += puce(r.x(0), r.y(h / 2) - 18, 1);
    out += puce(barres[0].x - 14, barres[0].y, 2);
    out += puce(r.x(-g.axe_cadre_cm.b / 2) - 13, r.y(0), 3);
    return { svg: out, largeur: L, hauteur: H, barres, axe_cadre_cm: g.axe_cadre_cm };
  }

  /** Elevation d'une poutre continue : travees issues des donnees + console eventuelle. */
  function elevationPoutre(p, o = {}) {
    const L = o.largeur || 640, H = o.hauteur || 180;
    const total = p.travees_m.reduce((a, b) => a + b, 0) + (p.console_m || 0);
    const r = repere({ largeur: L, hauteur: H, marge: 42, xmin: 0, xmax: total, ymin: 0, ymax: Math.max(2, total / 6) });
    const yh = r.y(1.1), hp = r.l(p.h_m || 0.75);
    let g = "", x = 0;
    g += rect(r.x(0), yh - hp / 2, r.l(total), hp, { remplissage: "url(#m-beton)", ep: 1.3 });
    const appuis = [0];
    for (const t of p.travees_m) { x += t; appuis.push(x); }
    appuis.forEach((a, i) => {
      const ax = r.x(a), ay = yh + hp / 2;
      g += chemin(`M${ax - 9} ${ay + 15} L${ax} ${ay} L${ax + 9} ${ay + 15} z`,
        { remplissage: "#41607d", couleur: "#41607d", ep: 1 });
      g += ligne(ax - 13, ay + 15, ax + 13, ay + 15, { couleur: "#41607d", ep: 1.6 });
      g += texte(ax, ay + 29, `A${i + 1}`, { taille: 10, ancre: "middle", couleur: "#3f4852" });
    });
    let xc = 0;
    p.travees_m.forEach((t) => {
      g += cote(r.x(xc), yh - hp / 2, r.x(xc + t), yh - hp / 2, `${t.toFixed(2)} m`, { decalage: -24 });
      xc += t;
    });
    if (p.console_m) {
      g += cote(r.x(xc), yh - hp / 2, r.x(total), yh - hp / 2, `${p.console_m.toFixed(2)} m`,
        { decalage: -24, couleur: "#8c3b2e" });
      g += texte(r.x(xc + p.console_m / 2), yh + hp / 2 + 40, "console", { taille: 10.5, ancre: "middle", couleur: "#8c3b2e" });
    }
    return { svg: g, largeur: L, hauteur: H };
  }

  /** Diagramme issu d'un calcul : liste de {x, v}. Jamais dessine a la main. */
  function diagramme(pts, o = {}) {
    const L = o.largeur || 640, H = o.hauteur || 200;
    const xs = pts.map((p) => p.x), vs = pts.map((p) => p.v);
    const vmax = Math.max(...vs.map(Math.abs)) || 1;
    const r = repere({ largeur: L, hauteur: H, marge: 44, libre: true,
      xmin: Math.min(...xs), xmax: Math.max(...xs), ymin: -vmax, ymax: vmax });
    const y0 = r.y(0);
    let g = ligne(r.x(Math.min(...xs)), y0, r.x(Math.max(...xs)), y0, { couleur: "#a8aca4", ep: 1 });
    const d = pts.map((p, i) => `${i ? "L" : "M"}${r.x(p.x)} ${r.y(p.v)}`).join(" ");
    g += chemin(`${d} L${r.x(xs[xs.length - 1])} ${y0} L${r.x(xs[0])} ${y0} z`,
      { remplissage: o.remplissage || "rgba(27,79,114,.13)", couleur: "none", ep: 0 });
    g += chemin(d, { couleur: o.couleur || "#1b4f72", ep: 1.8, jointure: "round" });
    const iMax = vs.indexOf(Math.max(...vs)), iMin = vs.indexOf(Math.min(...vs));
    for (const i of new Set([iMax, iMin])) {
      g += cercle(r.x(pts[i].x), r.y(pts[i].v), 3, { remplissage: o.couleur || "#1b4f72" });
      g += texte(r.x(pts[i].x), r.y(pts[i].v) + (pts[i].v >= 0 ? -8 : 15),
        `${pts[i].v.toFixed(1)} ${o.unite || ""}`.trim(),
        { taille: 10.5, mono: 1, ancre: "middle", gras: 1, couleur: o.couleur || "#1b4f72" });
    }
    g += texte(r.x(xs[0]) - 6, y0, "0", { taille: 10, mono: 1, ancre: "end", base: "middle", couleur: "#6b7682" });
    if (o.titre) g += texte(L / 2, 20, o.titre, { taille: 12, gras: 1, ancre: "middle" });
    return { svg: g, largeur: L, hauteur: H };
  }

  /** Gantt : taches {nom, debut, duree, critique}. Unite = jour. */
  function gantt(taches, o = {}) {
    const lig = 24, L = o.largeur || 700;
    // la colonne d'etiquettes se dimensionne sur le nom le plus long, au lieu d'une
    // largeur fixe qui tronquait les libelles
    const lab = o.labels || Math.min(300, Math.max(140,
      Math.round(Math.max(...taches.map((t) => t.nom.length)) * 6.3) + 16));
    const H = 52 + taches.length * lig;
    const fin = Math.max(...taches.map((t) => t.debut + t.duree)) || 1;
    const k = (L - lab - 60) / fin;        // 60 : place pour l'etiquette de duree a droite
    const X = (j) => ech(lab + j * k);
    let g = "";
    const pasG = fin > 60 ? 10 : fin > 20 ? 5 : 2;
    for (let j = 0; j <= fin; j += pasG) {
      g += ligne(X(j), 34, X(j), H - 14, { couleur: "#e7e8e3", ep: 1 });
      g += texte(X(j), 28, String(j), { taille: 9.5, mono: 1, ancre: "middle", couleur: "#6b7682" });
    }
    g += texte(lab - 8, 28, "jour", { taille: 9.5, ancre: "end", couleur: "#6b7682" });
    taches.forEach((t, i) => {
      const y = 42 + i * lig;
      g += texte(lab - 10, y + 7, t.nom, { taille: 11, ancre: "end" });
      g += rect(X(t.debut), y, Math.max(2, ech(t.duree * k)), 13,
        { remplissage: t.critique ? "#8c3b2e" : "#41607d", couleur: "none", ep: 0, rayon: 2 });
      // format UNIFORME : deux decimales partout. Melanger « 1,77 j » et « 3 j » dans
      // la meme colonne laisse croire a deux precisions differentes.
      const dj = Number(t.duree).toFixed(2).replace(".", ",");
      g += texte(X(t.debut + t.duree) + 5, y + 7, `${dj} j`,
        { taille: 9.5, mono: 1, base: "middle", couleur: "#6b7682" });
    });
    return { svg: g, largeur: L, hauteur: H };
  }

  /** Courbe en S : pts {j, prevu, realise?}, en % cumule. */
  function courbeS(z, o = {}) {
    // Deux formes acceptees : un tableau de points, ou { points, constat }. Le constat
    // est dessine comme un POINT et non comme une courbe : tant qu'un seul releve
    // existe, tracer une ligne reviendrait a publier une prevision deguisee en constat.
    const pts = Array.isArray(z) ? z : z.points;
    const constat = Array.isArray(z) ? null : (z.constat || null);
    const L = o.largeur || 620, H = o.hauteur || 260;
    const r = repere({ largeur: L, hauteur: H, marge: 48, margeDroite: 24, libre: true,
      xmin: 0, xmax: Math.max(...pts.map((p) => p.j)), ymin: 0, ymax: 100 });
    let g = "";
    for (let v = 0; v <= 100; v += 25) {
      g += ligne(r.x(0), r.y(v), r.x(Math.max(...pts.map((p) => p.j))), r.y(v), { couleur: "#e7e8e3", ep: 1 });
      g += texte(r.x(0) - 7, r.y(v), `${v} %`, { taille: 9.5, mono: 1, ancre: "end", base: "middle", couleur: "#6b7682" });
    }
    const trace = (cle, coul, tirets) => {
      const q = pts.filter((p) => p[cle] != null);
      if (q.length < 2) return "";
      return chemin(q.map((p, i) => `${i ? "L" : "M"}${r.x(p.j)} ${r.y(p[cle])}`).join(" "),
        { couleur: coul, ep: 2, tirets, jointure: "round" });
    };
    g += trace("prevu", "#41607d", "6 4");
    g += trace("realise", "#8c3b2e", null);
    // le constat : un point, un trait d'aplomb jusqu'a la courbe prevue, et l'ecart cote
    if (constat) for (const c of constat) {
      const prev = (() => {
        const av = pts.filter((p) => p.j <= c.j).pop(), ap = pts.find((p) => p.j >= c.j);
        if (!av || !ap) return null;
        if (ap.j === av.j) return av.prevu;
        return av.prevu + (ap.prevu - av.prevu) * (c.j - av.j) / (ap.j - av.j);
      })();
      if (prev != null) {
        g += ligne(r.x(c.j), r.y(prev), r.x(c.j), r.y(c.realise), { couleur: "#8c3b2e", ep: 1.4 });
        g += texte(r.x(c.j) + 7, r.y((prev + c.realise) / 2), `${(prev - c.realise).toFixed(1).replace(".", ",")} pts`,
          { taille: 9.5, mono: 1, base: "middle", couleur: "#8c3b2e" });
      }
      g += cercle(r.x(c.j), r.y(c.realise), 4.5, { remplissage: "#8c3b2e", couleur: "#ffffff", ep: 1.5 });
    }
    // graduations en abscisse : sans elles, la courbe ne se lit pas dans le temps
    const jmax = Math.max(...pts.map((p) => p.j));
    const pasJ = jmax > 60 ? 10 : jmax > 20 ? 5 : 2;
    for (let j = 0; j <= jmax + 1e-9; j += pasJ) {
      g += ligne(r.x(j), r.y(0), r.x(j), r.y(0) + 4, { couleur: "#a8aca4", ep: 1 });
      g += texte(r.x(j), r.y(0) + 16, String(Math.round(j)),
        { taille: 9.5, mono: 1, ancre: "middle", couleur: "#6b7682" });
    }
    g += texte(L / 2, H - 8, "jours ouvrés", { taille: 10, ancre: "middle", couleur: "#6b7682" });
    // legende : sans elle, deux traits de couleurs differentes ne disent rien
    const yl = 20;
    g += ligne(L - 150, yl, L - 126, yl, { couleur: "#41607d", ep: 2, tirets: "6 4" });
    g += texte(L - 120, yl + 3.5, "prévu", { taille: 10.5, couleur: "#3f4852" });
    if (constat) {
      g += cercle(L - 68, yl, 4.5, { remplissage: "#8c3b2e", couleur: "#ffffff", ep: 1.5 });
      g += texte(L - 58, yl + 3.5, "constat", { taille: 10.5, couleur: "#3f4852" });
    } else {
      g += ligne(L - 74, yl, L - 50, yl, { couleur: "#8c3b2e", ep: 2 });
      g += texte(L - 44, yl + 3.5, "réalisé", { taille: 10.5, couleur: "#3f4852" });
    }
    return { svg: g, largeur: L, hauteur: H };
  }

  /** Histogramme d'effectifs : {j, n}. */
  function histogramme(pts, o = {}) {
    const L = o.largeur || 620, H = o.hauteur || 220;
    const nmax = Math.max(...pts.map((p) => p.n)) || 1;
    const r = repere({ largeur: L, hauteur: H, marge: 44, libre: true,
      xmin: 0, xmax: pts.length, ymin: 0, ymax: nmax * 1.1 });
    const l = (r.x(1) - r.x(0)) * .82;
    let g = "";
    pts.forEach((p, i) => {
      const h = r.y(0) - r.y(p.n);
      g += rect(r.x(i) + l * .11, r.y(p.n), l, h, { remplissage: "#41607d", couleur: "none", ep: 0 });
      if (i % Math.ceil(pts.length / 12) === 0)
        g += texte(r.x(i) + l / 2, r.y(0) + 13, String(p.j), { taille: 9, mono: 1, ancre: "middle", couleur: "#6b7682" });
    });
    g += ligne(r.x(0), r.y(0), r.x(pts.length), r.y(0), { couleur: "#14181d", ep: 1 });
    // Axe des ordonnees gradue, avec son unite. Sans lui, une legende qui dit « c'est la
    // pointe qu'il faut lire » demande au lecteur de lire un nombre qui n'est pas ecrit.
    const pasN = nmax > 40 ? 10 : nmax > 15 ? 5 : 2;
    for (let v = 0; v <= nmax; v += pasN) {
      g += ligne(r.x(0) - 4, r.y(v), r.x(pts.length), r.y(v),
        { couleur: v ? "#eceee9" : "#14181d", ep: 1 });
      g += texte(r.x(0) - 8, r.y(v), String(v),
        { taille: 9, mono: 1, ancre: "end", base: "middle", couleur: "#6b7682" });
    }
    // l'unite se pose DANS le cadre : ancree a gauche de l'axe, elle sortait de la vue
    g += texte(r.x(0) + 2, r.y(nmax) + 10, o.unite || "personnes",
      { taille: 9, ancre: "start", couleur: "#6b7682" });
    // la pointe est cotee : c'est le nombre que la legende demande de lire
    const iMax = pts.findIndex((p) => p.n === nmax);
    g += ligne(r.x(iMax) + l / 2, r.y(nmax) - 6, r.x(iMax) + l / 2, r.y(nmax) - 16,
      { couleur: "#8c3b2e", ep: 1 });
    g += texte(r.x(iMax) + l / 2, r.y(nmax) - 21, `pointe ${nmax}`,
      { taille: 9.5, mono: 1, ancre: "middle", couleur: "#8c3b2e" });
    const moy = pts.reduce((a, p) => a + p.n, 0) / pts.length;
    g += ligne(r.x(0), r.y(moy), r.x(pts.length), r.y(moy), { couleur: "#8c3b2e", ep: 1.2, tirets: "5 4" });
    g += texte(r.x(pts.length) - 4, r.y(moy) - 5, `moyenne ${moy.toFixed(1).replace(".", ",")}`,
      { taille: 9.5, mono: 1, ancre: "end", couleur: "#8c3b2e" });
    return { svg: g, largeur: L, hauteur: H };
  }

  /**
   * Plan de zones de coulage d'un plancher. Toutes les cotes viennent des donnees ;
   * l'etat d'avancement de chaque zone aussi.
   * `z` : { longueur_m, largeur_m, nb_zones, entraxe_poutres_m, avancement: [etat...] }
   * etat : "faite" | "en_cours" | "a_venir"
   */
  function planZones(z, o = {}) {
    const L = o.largeur || 760, H = o.hauteur || 220;
    const Lt = z.nb_zones * z.longueur_m;
    const r = repere({ largeur: L, hauteur: H, marge: 46, margeDroite: 86,
      xmin: 0, xmax: Lt, ymin: 0, ymax: z.largeur_m });
    const TEINTE = { faite: "#cfe0d4", en_cours: "#fdf1cf", a_venir: "#f1f1ed" };
    const BORD = { faite: "#1f5c3a", en_cours: "#7a5c00", a_venir: "#a8aca4" };
    let g = "";

    for (let i = 0; i < z.nb_zones; i++) {
      const x0 = i * z.longueur_m;
      const etat = (z.avancement && z.avancement[i]) || "a_venir";
      g += rect(r.x(x0), r.y(z.largeur_m), r.l(z.longueur_m), r.l(z.largeur_m),
        { remplissage: TEINTE[etat], couleur: BORD[etat], ep: etat === "a_venir" ? 1 : 1.6 });
    }

    // Lignes de poutres AVANT les libelles, et interrompues dans la bande centrale :
    // elles traversaient les textes « Z1 / coulee », qu'aucun controle ne voyait
    // puisque le test de chevauchement ne compare que du texte a du texte.
    if (z.entraxe_poutres_m) {
      const yh = r.y(z.largeur_m), yb = r.y(0);
      const c1 = yh + (yb - yh) * 0.30, c2 = yh + (yb - yh) * 0.72;
      for (let x = z.entraxe_poutres_m; x < Lt - 1e-9; x += z.entraxe_poutres_m) {
        g += ligne(r.x(x), yh, r.x(x), c1, { couleur: "#8c3b2e", ep: .8, tirets: "4 3" });
        g += ligne(r.x(x), c2, r.x(x), yb, { couleur: "#8c3b2e", ep: .8, tirets: "4 3" });
      }
    }

    // Ce que le PLANNING prevoyait a la meme date, en contour : sans lui, le tableau de
    // bord le plus lisible du module tait l'ecart que tout le § S6 etablit.
    if (z.avancement_prevu) {
      for (let i = 0; i < z.nb_zones; i++) {
        const f = z.avancement_prevu[i];
        // seules les zones PARTIELLEMENT prevues portent un repere : sur une zone prevue
        // a 100 %, le trait tomberait sur le bord et se lirait comme une bordure de plus
        if (!f || f >= 1) continue;
        const x0 = i * z.longueur_m;
        // un trait de niveau, pose SOUS le bord haut de la zone : un rectangle plein
        // cadre masquait les couleurs d'etat qu'il etait cense completer
        const yh = r.y(z.largeur_m) + 6, yb = r.y(0) - 6;
        const yT = yb - (yb - yh) * 0.22;        // sous les libelles de zone
        g += ligne(r.x(x0 + z.longueur_m * f), yh, r.x(x0 + z.longueur_m * f), yb,
          { couleur: "#41607d", ep: 2 });
        g += ligne(r.x(x0), yT, r.x(x0 + z.longueur_m * f), yT,
          { couleur: "#41607d", ep: 1.2, tirets: "4 3" });
      }
      g += puce(r.x(z.longueur_m * 4.25), r.y(z.largeur_m) - 16, 3);
    }

    for (let i = 0; i < z.nb_zones; i++) {
      const x0 = i * z.longueur_m;
      const etat = (z.avancement && z.avancement[i]) || "a_venir";
      g += texte(r.x(x0 + z.longueur_m / 2), r.y(z.largeur_m / 2) - 2, `Z${i + 1}`,
        { taille: 13, gras: 1, ancre: "middle", base: "middle", couleur: BORD[etat] });
      if (etat !== "a_venir")
        g += texte(r.x(x0 + z.longueur_m / 2), r.y(z.largeur_m / 2) + 14,
          etat === "faite" ? "coulée" : "en cours",
          { taille: 9.5, ancre: "middle", base: "middle", couleur: BORD[etat] });
    }

    g += cote(r.x(0), r.y(0), r.x(z.longueur_m), r.y(0), `${z.longueur_m} m`, { decalage: 22 });
    g += cote(r.x(0), r.y(0), r.x(Lt), r.y(0), `${ech(Lt)} m`, { decalage: 40 });
    g += cote(r.x(Lt), r.y(0), r.x(Lt), r.y(z.largeur_m), `${z.largeur_m} m`, { decalage: 26 });
    // La puce 1 designe une ZONE, la puce 2 une ligne de poutres. Le centre d'une zone
    // tombe TOUJOURS sur une ligne de poutres (la zone fait un nombre entier de trames) :
    // la puce 1 se pose donc au quart de la zone, sinon les deux puces se superposent.
    g += puce(r.x(z.longueur_m * 0.25), r.y(z.largeur_m) - 16, 1);
    if (z.entraxe_poutres_m)
      g += puce(r.x(z.entraxe_poutres_m), r.y(z.largeur_m) - 16, 2);
    return { svg: g, largeur: L, hauteur: H };
  }

  /** Diagramme de rotation : les zones dans le temps, phase par phase, et le coffrage
      immobilise jour par jour sous le meme axe. C'est la figure qui rend visible d'un
      coup ce que le Gantt d'UNE zone ne montre pas : la cadence, le recouvrement entre
      zones, et la contrainte de parc qui en decoule. */
  function rotation(r, o = {}) {
    const L = o.largeur || 760, hZ = 15, hBas = 62;
    const n = r.zones.length;
    const fin = Math.max(...r.zones.map((z) => z.debut_j + r.cycle_j));
    const H = 34 + n * hZ + hBas;
    const gx = 40, lx = L - gx - 96;
    const X = (j) => ech(gx + j * lx / fin);
    const PH = { COF: "#7a93ad", FEP: "#c9a227", FED: "#1f5c3a", PTA: "#8c3b2e",
                 BET: "#41607d", CUR: "#e0ded5", DEC: "#a8aca4" };
    let g = "";
    const pasJ = fin > 30 ? 5 : 2;
    for (let j = 0; j <= fin; j += pasJ) {
      g += ligne(X(j), 20, X(j), 26 + n * hZ, { couleur: "#eceee9", ep: 1 });
      g += texte(X(j), 15, String(j), { taille: 9, mono: 1, ancre: "middle", couleur: "#6b7682" });
    }
    r.zones.forEach((z, i) => {
      const y = 24 + i * hZ;
      g += texte(gx - 6, y + 6, `Z${z.zone}`, { taille: 9.5, mono: 1, ancre: "end", base: "middle", couleur: "#6b7682" });
      z.phases.forEach((ph) => {
        const x0 = X(z.debut_j + ph.debut_j), x1 = X(z.debut_j + ph.fin_j);
        g += rect(x0, y, Math.max(1.2, x1 - x0), hZ - 4,
          { remplissage: PH[ph.id] || "#d5d7d1", couleur: "none", ep: 0 });
      });
    });
    // la cadence : une droite qui joint les debuts de zone, et sa pente EST la cadence
    g += chemin(r.zones.map((z, i) => `${i ? "L" : "M"}${X(z.debut_j)} ${24 + i * hZ}`).join(" "),
      { couleur: "#8c3b2e", ep: 1.6, remplissage: "none", tirets: "5 4" });
    // l'etiquette se pose dans la marge de droite, a mi-pente : posee au dernier debut
    // de zone, elle passait par-dessus la barre de la zone 8
    g += texte(L - 8, 24 + (n / 2) * hZ,
      `cadence ${String(r.cadence_j).replace(".", ",")} j/zone`,
      { taille: 9.5, mono: 1, ancre: "end", base: "middle", couleur: "#8c3b2e" });

    // bande basse : coffrage immobilise, et le parc declare
    const yB = 34 + n * hZ, hB = hBas - 26;
    const mmax = Math.max(r.stock_coffrage_m2, ...r.coffrage_immobilise.map((x) => x.m2)) * 1.08;
    const Y = (m) => ech(yB + hB - m / mmax * hB);
    g += chemin(r.coffrage_immobilise.map((x, i) => `${i ? "L" : "M"}${X(x.j)} ${Y(x.m2)}`).join(" "),
      { couleur: "#41607d", ep: 1.6, remplissage: "none" });
    g += ligne(X(0), Y(r.stock_coffrage_m2), X(fin), Y(r.stock_coffrage_m2),
      { couleur: "#8c3b2e", ep: 1.4, tirets: "6 4" });
    g += texte(X(fin) + 6, Y(r.stock_coffrage_m2), `parc ${r.stock_coffrage_m2} m²`,
      { taille: 9, mono: 1, base: "middle", couleur: "#8c3b2e" });
    g += ligne(X(0), Y(0), X(fin), Y(0), { couleur: "#14181d", ep: 1 });
    g += texte(gx - 6, Y(0), "0", { taille: 9, mono: 1, ancre: "end", base: "middle", couleur: "#6b7682" });
    g += texte(gx - 6, yB + 4, "m²", { taille: 9, ancre: "end", couleur: "#6b7682" });
    g += texte(L / 2, H - 4, "jours ouvrés", { taille: 10, ancre: "middle", couleur: "#6b7682" });
    return { svg: g, largeur: L, hauteur: H };
  }

  /** Sequence d'execution en etapes numerotees. */
  function sequence(etapes, o = {}) {
    const L = o.largeur || 700, cel = L / etapes.length, H = o.hauteur || 150;
    let g = "";
    etapes.forEach((e, i) => {
      const x = i * cel;
      g += rect(x + 6, 30, cel - 12, H - 62, { remplissage: "#f1f1ed", couleur: "#d5d7d1", ep: 1, rayon: 4 });
      g += puce(x + cel / 2, 30, i + 1);
      const mots = String(e).split(" ");
      let l = "", lignes = [];
      for (const m of mots) { if ((l + " " + m).trim().length > 16) { lignes.push(l.trim()); l = m; } else l += " " + m; }
      lignes.push(l.trim());
      lignes.forEach((t, k) => { g += texte(x + cel / 2, 56 + k * 14, t, { taille: 10.5, ancre: "middle" }); });
      if (i < etapes.length - 1)
        g += ligne(x + cel - 4, H - 46, x + cel + 4, H - 46, { couleur: "#6b7682", ep: 1.2, marqueur: 1 });
    });
    // Les numeros sont decrits EN PLACE, sous chaque puce : le generateur le declare, pour que
    // le controle de legende du build (§ 8) n'ait pas a le deviner ni a etre contourne.
    return { svg: g, largeur: L, hauteur: H,
      legendeImplicite: etapes.map((e, i) => ({ n: i + 1, t: String(e) })) };
  }

  const API = { repere, svg, texte, ligne, rect, cercle, chemin, cote, legende, puce,
    coupeSection, elevationPoutre, diagramme, gantt, courbeS, histogramme, sequence,
    planZones, rotation, MOTIFS, ech };

  if (typeof module !== "undefined" && module.exports) module.exports = API;
  racine.SVGKit = API;
})(typeof globalThis !== "undefined" ? globalThis : this);
