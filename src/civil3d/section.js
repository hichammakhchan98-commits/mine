/* Regle UNIQUE de positionnement des armatures dans une section rectangulaire.
 *
 * Pourquoi ce fichier existe : la regle etait ecrite trois fois — en Python (calc/),
 * en JavaScript pour la 3D, et encore en JavaScript pour le SVG — avec des conventions
 * DIFFERENTES. Le SVG posait les barres a l'enrobage, la 3D a l'enrobage + le cadre, et
 * les deux pretendaient lire le meme fichier de donnees. Une seule routine, desormais.
 *
 * Convention d'enrobage : l'enrobage se mesure a la peau de l'armature la plus
 * EXTERIEURE, donc a la peau du cadre. L'axe du cadre est donc a (enrobage + dia/2).
 *
 * Toutes les entrees sont en cm/mm (comme sur un plan) ; toutes les sorties en cm.
 */

/**
 * Les chaines de `data/.../conventions` ne doivent pas etre decoratives : si elles
 * decrivent une regle que ce code n'implemente pas, c'est la documentation qui ment.
 * On refuse de tourner plutot que de laisser les deux diverger.
 */
export function verifierConventions(cv) {
  if (!cv) throw new Error("conventions absentes du jeu de donnees");
  if (cv.enrobage_mesure_a !== "peau exterieure du cadre")
    throw new Error(`convention d'enrobage « ${cv.enrobage_mesure_a} » non implementee : `
      + `ce code mesure l'enrobage a la peau exterieure du cadre`);
  if (cv.crochets_extremite !== false)
    throw new Error("les crochets d'extremite ne sont pas modelises : "
      + "conventions.crochets_extremite doit valoir false");
  if (!String(cv.placement_cadres ?? "").includes("premier et dernier cadre a l'enrobage"))
    throw new Error(`regle de placement « ${cv.placement_cadres} » non implementee`);
  return true;
}

export function positionsArmatures(s, conv) {
  const b = s.b_cm, h = s.h_cm, e = s.enrobage_cm;
  const dCad = conv.dia_cadre_mm / 10;              // cm
  const rCint = conv.rayon_cintrage_mm / 10;        // cm

  // --- cadre : son AXE, a enrobage + demi-diametre de la peau du beton
  const axe = { b: b - 2 * (e + dCad / 2), h: h - 2 * (e + dCad / 2) };
  if (axe.b <= 0 || axe.h <= 0)
    throw new Error(`enrobage ${e} cm incompatible avec une section ${b} x ${h} cm`);
  if (2 * rCint > Math.min(axe.b, axe.h))
    throw new Error(`rayon de cintrage ${conv.rayon_cintrage_mm} mm incompatible avec le cadre`);

  // --- interieur libre du cadre : c'est la que logent les barres
  const libre = { b: b - 2 * (e + dCad), h: h - 2 * (e + dCad) };

  const barres = [];
  const poseNappe = (nappe, bas) => {
    const d = nappe.dia_mm / 10;                    // cm
    const y = bas ? -h / 2 + e + dCad + d / 2 : h / 2 - e - dCad - d / 2;
    const dispo = libre.b - d;                      // entre axes extremes
    if (dispo < 0) throw new Error("les barres ne tiennent pas dans le cadre");
    for (let i = 0; i < nappe.n; i++) {
      const x = nappe.n === 1 ? 0 : -dispo / 2 + (dispo * i) / (nappe.n - 1);
      barres.push({ x_cm: x, y_cm: y, dia_mm: nappe.dia_mm, nappe: bas ? "inf" : "sup" });
    }
  };
  poseNappe(s.inf, true);
  poseNappe(s.sup, false);

  return { axe_cadre_cm: axe, libre_cm: libre, rayon_cintrage_cm: rCint,
    dia_cadre_cm: dCad, enrobage_cm: e, barres };
}

/**
 * Placement des cadres sur un troncon : premier et dernier a l'enrobage de chaque about,
 * les autres repartis a espacement constant. UNE regle pour le comptage ET le placement.
 */
export function placementCadres(L_cm, enrobage_cm, espacement_nominal_cm, dia_cadre_mm = 0) {
  // L'enrobage se mesure a la PEAU du cadre, le long de l'axe comme en section :
  // l'axe du premier cadre est donc a enrobage + diametre/2 de l'about.
  const retrait = enrobage_cm + dia_cadre_mm / 20;
  const utile = L_cm - 2 * retrait;
  if (utile <= 0) throw new Error(`troncon ${L_cm} cm trop court pour l'enrobage`);
  // l'espacement nominal est un MAXIMUM : arrondi au superieur, sinon l'espacement reel
  // le depasse (194 / 12 = 16,2 cm pour un nominal de 15 cm)
  const n = Math.max(2, Math.ceil(utile / espacement_nominal_cm) + 1);
  const espacement_reel = n > 1 ? utile / (n - 1) : 0;
  const z = [];
  for (let i = 0; i < n; i++) z.push(-L_cm / 2 + retrait + i * espacement_reel);
  return { n, espacement_reel_cm: espacement_reel, z_cm: z };
}

/** Perimetre d'un cadre a coins arrondis — SOLUTION FERMEE. */
export function perimetreCadreFerme(b_cm, h_cm, r_cm) {
  if (r_cm <= 0) return 2 * (b_cm + h_cm);
  return 2 * (b_cm - 2 * r_cm) + 2 * (h_cm - 2 * r_cm) + 2 * Math.PI * r_cm;
}

/** Contour EXACT du cadre (droites + arcs), echantillonne. Sert au tube 3D et au metre. */
export function contourCadre(b_cm, h_cm, r_cm, nArc = 10, nDroite = 8) {
  if (2 * r_cm > Math.min(b_cm, h_cm)) throw new Error("rayon de cintrage incompatible");
  const pts = [];
  const coins = [[b_cm / 2 - r_cm, h_cm / 2 - r_cm, 0], [-(b_cm / 2 - r_cm), h_cm / 2 - r_cm, Math.PI / 2],
                 [-(b_cm / 2 - r_cm), -(h_cm / 2 - r_cm), Math.PI], [b_cm / 2 - r_cm, -(h_cm / 2 - r_cm), -Math.PI / 2]];
  for (let c = 0; c < 4; c++) {
    const [cx, cy, a0] = coins[c];
    for (let i = 0; i <= nArc; i++) {
      const a = a0 + (i / nArc) * (Math.PI / 2);
      pts.push([cx + r_cm * Math.cos(a), cy + r_cm * Math.sin(a)]);
    }
    const su = coins[(c + 1) % 4];
    const fin = [cx + r_cm * Math.cos(a0 + Math.PI / 2), cy + r_cm * Math.sin(a0 + Math.PI / 2)];
    const deb = [su[0] + r_cm * Math.cos(su[2]), su[1] + r_cm * Math.sin(su[2])];
    for (let i = 1; i < nDroite; i++)
      pts.push([fin[0] + (deb[0] - fin[0]) * i / nDroite, fin[1] + (deb[1] - fin[1]) * i / nDroite]);
  }
  return pts;
}
