/* Compilateur du contenu pedagogique : Markdown + directives + balises de preuve (§ 4.3, § 3.2).
   Volontairement reduit a ce que le cours utilise : moins de surface, moins de surprises. */

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

/* ---------- balises de preuve ⟦V2|reference|enonce⟧ (§ 3.2) ---------- */
const RE_BALISE = /⟦(V[0-3])\|([^|⟧]*)\|([^⟧]*)⟧/g;

export function extraireBalises(texte, module) {
  const out = [];
  for (const m of texte.matchAll(RE_BALISE)) {
    // V0 a V2 : ⟦Vn|reference|enonce⟧
    // V3      : ⟦V3|hypothese|valeur affichee|unite|fourchette|annee⟧ — les champs
    //           supplementaires alimentent registre-hypotheses.csv, que le § 3.2 veut
    //           complet (fourchette ET annee de reference), et non a moitie vide.
    const champs = m[3].split("|").map((x) => x.trim());
    out.push({ niveau: m[1], reference: m[2].trim(), enonce: champs[0], champs, module });
  }
  return out;
}

function rendreBalises(s) {
  return s.replace(RE_BALISE, (_, niv, ref, reste) => {
    const champs = reste.split("|").map((x) => x.trim());
    const titre = niv === "V3"
      ? `${niv} — ${ref}` + (champs[3] ? ` · fourchette ${champs[3]}` : "")
        + (champs[4] ? ` · annee ${champs[4]}` : "")
      : `${niv} — ${ref}`;
    return `${esc(champs[0])}<sup class="preuve preuve-${niv}" title="${esc(titre)}">${niv}</sup>`;
  });
}

/* ---------- inline ---------- */
function inline(s, ctx) {
  // les maths d'abord : leur contenu ne doit pas etre touche par le reste
  const maths = [];
  s = s.replace(/\$\$([^$]+)\$\$|\$([^$\n]+)\$/g, (_, bloc, enl) => {
    maths.push({ tex: (bloc ?? enl).trim(), bloc: !!bloc });
    return `\u0000M${maths.length - 1}\u0000`;
  });
  const codes = [];
  s = s.replace(/`([^`]+)`/g, (_, c) => { codes.push(c); return `\u0000C${codes.length - 1}\u0000`; });

  s = rendreBalises(esc(s));
  s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
       .replace(/(^|[^*])\*([^*\n]+)\*/g, "$1<em>$2</em>")
       .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  s = s.replace(/\u0000C(\d+)\u0000/g, (_, i) => `<code>${esc(codes[+i])}</code>`);
  s = s.replace(/\u0000M(\d+)\u0000/g, (_, i) => ctx.math(maths[+i].tex, maths[+i].bloc));
  return s;
}

/* ---------- blocs ---------- */
export function compiler(src, ctx) {
  const lignes = src.split("\n");
  const sortie = [];
  const titres = [];
  let i = 0;

  const estTableau = (k) => /^\s*\|.*\|\s*$/.test(lignes[k] ?? "") && /^\s*\|[\s:|-]+\|\s*$/.test(lignes[k + 1] ?? "");

  while (i < lignes.length) {
    const l = lignes[i];

    if (!l.trim()) { i++; continue; }

    // code clos
    if (l.startsWith("```")) {
      const fin = lignes.indexOf("```", i + 1);
      const corps = lignes.slice(i + 1, fin < 0 ? lignes.length : fin).join("\n");
      sortie.push(`<pre><code>${esc(corps)}</code></pre>`);
      i = (fin < 0 ? lignes.length : fin) + 1; continue;
    }

    // directive  ::: nom {json}  ...  :::
    if (l.startsWith(":::")) {
      const m = l.match(/^:::\s*(\w+)\s*(\{[\s\S]*\})?\s*$/);
      if (!m) throw new Error(`directive mal formee ligne ${i + 1} : ${l}`);
      let prof = 1, j = i + 1;
      const corps = [];
      while (j < lignes.length) {
        if (lignes[j].startsWith(":::") && lignes[j].trim() !== ":::") prof++;
        else if (lignes[j].trim() === ":::") { prof--; if (!prof) break; }
        corps.push(lignes[j]); j++;
      }
      if (prof) throw new Error(`directive ${m[1]} non fermee (ligne ${i + 1})`);
      let opts = {};
      if (m[2]) { try { opts = JSON.parse(m[2]); } catch (e) { throw new Error(`JSON invalide dans :::${m[1]} ligne ${i + 1} — ${e.message}`); } }
      sortie.push(ctx.directive(m[1], opts, corps.join("\n")));
      i = j + 1; continue;
    }

    // titres
    const h = l.match(/^(#{1,4})\s+(.*)$/);
    if (h) {
      const niv = h[1].length, txt = inline(h[2], ctx);
      const id = h[2].toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
        .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
      if (niv <= 3) titres.push({ niv, id, txt: h[2].replace(RE_BALISE, "$3") });
      sortie.push(`<h${niv} id="${id}">${txt}</h${niv}>`);
      i++; continue;
    }

    // tableau
    if (estTableau(i)) {
      const cellules = (r) => r.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
      const entete = cellules(lignes[i]);
      const aligns = cellules(lignes[i + 1]).map((a) => a.startsWith(":") && a.endsWith(":") ? "center"
        : a.endsWith(":") ? "right" : "left");
      let j = i + 2;
      const corps = [];
      while (j < lignes.length && /^\s*\|.*\|\s*$/.test(lignes[j])) { corps.push(cellules(lignes[j])); j++; }
      const th = entete.map((c, k) => `<th style="text-align:${aligns[k] ?? "left"}">${inline(c, ctx)}</th>`).join("");
      const tr = corps.map((r) => "<tr>" + r.map((c, k) =>
        `<td style="text-align:${aligns[k] ?? "left"}">${inline(c, ctx)}</td>`).join("") + "</tr>").join("");
      sortie.push(`<table><thead><tr>${th}</tr></thead><tbody>${tr}</tbody></table>`);
      i = j; continue;
    }

    // listes
    if (/^\s*[-*]\s+/.test(l) || /^\s*\d+[.)]\s+/.test(l)) {
      const ordonnee = /^\s*\d+[.)]\s+/.test(l);
      const items = [];
      while (i < lignes.length && (/^\s*[-*]\s+/.test(lignes[i]) || /^\s*\d+[.)]\s+/.test(lignes[i]))) {
        let t = lignes[i].replace(/^\s*(?:[-*]|\d+[.)])\s+/, "");
        i++;
        while (i < lignes.length && /^\s{2,}\S/.test(lignes[i]) && !/^\s*(?:[-*]|\d+[.)])\s/.test(lignes[i])) {
          t += " " + lignes[i].trim(); i++;
        }
        items.push(`<li>${inline(t, ctx)}</li>`);
      }
      sortie.push(`<${ordonnee ? "ol" : "ul"}>${items.join("")}</${ordonnee ? "ol" : "ul"}>`);
      continue;
    }

    // citation
    if (l.startsWith(">")) {
      const buf = [];
      while (i < lignes.length && lignes[i].startsWith(">")) { buf.push(lignes[i].replace(/^>\s?/, "")); i++; }
      sortie.push(`<blockquote>${inline(buf.join(" "), ctx)}</blockquote>`);
      continue;
    }

    // paragraphe
    const buf = [];
    while (i < lignes.length && lignes[i].trim() && !lignes[i].startsWith(":::")
      && !lignes[i].startsWith("```") && !/^(#{1,4})\s/.test(lignes[i])
      && !/^\s*[-*]\s+/.test(lignes[i]) && !/^\s*\d+[.)]\s+/.test(lignes[i])
      && !lignes[i].startsWith(">") && !estTableau(i)) { buf.push(lignes[i]); i++; }
    const txt = buf.join(" ").trim();
    if (txt) sortie.push(`<p>${inline(txt, ctx)}</p>`);
  }

  return { html: sortie.join("\n"), titres };
}

/* ---------- controle des blocs normatifs (§ 3.2 : le build ECHOUE si un nombre n'est pas balise) ---------- */
export function controlerBlocsNormatifs(src, fichier) {
  const fautes = [];
  const re = /^:::\s*normatif[\s\S]*?^:::$/gm;
  for (const bloc of src.match(re) ?? []) {
    const sansBalises = bloc.replace(RE_BALISE, "").replace(/^:::.*$/gm, "");
    for (const m of sansBalises.matchAll(/(?<![\w.])\d+(?:[.,]\d+)?(?![\w.])/g)) {
      const n = m[0];
      if (/^[1-9]$/.test(n)) continue;                  // numerotation courante : toleree
      fautes.push({ fichier, nombre: n, extrait: sansBalises.slice(Math.max(0, m.index - 40), m.index + 40).replace(/\s+/g, " ").trim() });
    }
  }
  return fautes;
}
