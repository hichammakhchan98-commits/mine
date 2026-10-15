import * as THREE from "three";
import { materiau } from "./materiaux.js";
import { cm, mm, CourbePolyligne } from "./geometrie.js";
import { positionsArmatures, placementCadres, contourCadre, perimetreCadreFerme } from "./section.js";

/* Helpers d'armatures. Les armatures repetitives (cadres) passent par InstancedMesh (§ 4.4).
   ATTENTION : cette bibliotheque DESSINE une geometrie a partir de parametres.
   Elle ne dimensionne rien et ne verifie aucune regle. */

/**
 * Tube ferme suivant un contour deja calcule par section.js.
 * `diametreBarre` est bien un DIAMETRE : le rayon du tube vaut sa moitie, une seule fois.
 * (La version precedente recevait deja une moitie et redivisait : les cadres etaient
 * dessines a la moitie de leur diametre, soit 4 mm pour un HA8.)
 */
function geometrieCadre(contour_m, diametreBarre_m, segments = 160) {
  const pts = contour_m.map(([x, y]) => new THREE.Vector3(x, y, 0));
  const courbe = new CourbePolyligne(pts, true);
  const geo = new THREE.TubeGeometry(courbe, segments, diametreBarre_m / 2, 6, true);
  geo.userData = { longueur_m: courbe.getLength() };
  return geo;
}

/**
 * Cage d'armatures d'un troncon de poutre rectangulaire.
 * Entrees en cm / mm (comme sur un plan) ; la scene est en metres.
 * Retourne { groupe, metre } ou `metre` donne les longueurs et masses RECALCULABLES (V1).
 */
export function cage({
  b_cm, h_cm, L_cm, enrobage_cm,
  inf = { n: 3, dia_mm: 20 }, sup = { n: 2, dia_mm: 16 },
  cadres = { dia_mm: 8, espacement_cm: 15 },
  betonVisible = true, opaciteBeton = 0.17,
} = {}) {
  const conv = { dia_cadre_mm: cadres.dia_mm, rayon_cintrage_mm: cadres.rayon_cintrage_mm ?? 20 };
  const geo2d = positionsArmatures({ b_cm, h_cm, enrobage_cm, inf, sup }, conv);
  const pose = placementCadres(L_cm, enrobage_cm, cadres.espacement_cm);
  const b = cm(b_cm), h = cm(h_cm), L = cm(L_cm), e = cm(enrobage_cm);
  const groupe = new THREE.Group();
  groupe.name = "cage";
  let triangles = 0;

  // Trois couches, chacune avec sa direction d'eclatement : c'est ce qui rend la vue
  // eclatee lisible (le coffrage descend, le beton monte, la cage reste en place).
  const gCoffrage = new THREE.Group();
  gCoffrage.name = "coffrage"; gCoffrage.userData.eclate = [0, -1, 0];
  const gArmatures = new THREE.Group();
  gArmatures.name = "armatures"; gArmatures.userData.eclate = [0, 0, 0];
  const gBeton = new THREE.Group();
  gBeton.name = "beton-couche"; gBeton.userData.eclate = [0, 1, 0];
  groupe.add(gCoffrage, gArmatures, gBeton);

  // --- coffrage : fond de moule + deux joues. Present du coffrage au betonnage,
  //     RETIRE au decoffrage : c'est ce que la phase 4 doit montrer.
  const epC = 0.027;                                  // panneau de 27 mm, epaisseur courante
  const debord = 0.06;
  const panneaux = [
    { t: "Fond de moule", g: [b + 2 * epC, epC, L + 2 * debord], p: [0, -h / 2 - epC / 2, 0] },
    { t: "Joue gauche",   g: [epC, h + epC, L + 2 * debord],     p: [-b / 2 - epC / 2, -epC / 2, 0] },
    { t: "Joue droite",   g: [epC, h + epC, L + 2 * debord],     p: [b / 2 + epC / 2, -epC / 2, 0] },
  ];
  for (const pan of panneaux) {
    const geo = new THREE.BoxGeometry(...pan.g);
    const m = new THREE.Mesh(geo, materiau("coffrage"));
    m.position.set(...pan.p);
    m.name = pan.t.toLowerCase().replace(/ /g, "-");
    m.userData = { phase: 1, phaseFin: 3, materiau: "coffrage", etiquette: pan.t };
    gCoffrage.add(m);
    triangles += 12;
  }

  // --- beton (enveloppe translucide, pour voir la cage dedans)
  if (betonVisible) {
    const geo = new THREE.BoxGeometry(b, h, L);
    const m = new THREE.Mesh(geo, materiau("beton", { opacite: opaciteBeton }));
    m.name = "beton";
    m.userData = { phase: 3, materiau: "beton", etiquette: "Béton",
      detail: `${b_cm} x ${h_cm} cm, longueur ${L_cm} cm` };
    m.renderOrder = 3;
    gBeton.add(m);
    triangles += 12;
  }

  // --- cadres : InstancedMesh (armatures repetitives), poses par la regle unique
  const dCad = mm(cadres.dia_mm);
  const contour = contourCadre(geo2d.axe_cadre_cm.b, geo2d.axe_cadre_cm.h, geo2d.rayon_cintrage_cm)
    .map(([x, y]) => [cm(x), cm(y)]);
  const geoCad = geometrieCadre(contour, dCad);
  const nCad = pose.n;
  const inst = new THREE.InstancedMesh(geoCad, materiau("acierHA"), nCad);
  inst.name = "cadres";
  const M = new THREE.Matrix4();
  for (let i = 0; i < nCad; i++) inst.setMatrixAt(i, M.makeTranslation(0, 0, cm(pose.z_cm[i])));
  inst.instanceMatrix.needsUpdate = true;
  inst.userData = { phase: 2, materiau: "acierHA", etiquette: `Cadres HA${cadres.dia_mm}`,
    detail: `${nCad} cadres, espacement reel ${pose.espacement_reel_cm.toFixed(1)} cm` };
  gArmatures.add(inst);
  triangles += (geoCad.index.count / 3) * nCad;

  // --- barres longitudinales : positions issues de section.js, jamais recalculees ici
  const barres = [];
  const compteur = { inf: 0, sup: 0 };
  for (const bar of geo2d.barres) {
    const d = mm(bar.dia_mm);
    const geo = new THREE.CylinderGeometry(d / 2, d / 2, L - 2 * e, 10, 1);
    geo.rotateX(Math.PI / 2);
    const m = new THREE.Mesh(geo, materiau("acierHA"));
    m.position.set(cm(bar.x_cm), cm(bar.y_cm), 0);
    m.name = `barre-${bar.nappe}-${++compteur[bar.nappe]}`;
    m.userData = { phase: 2, materiau: "acierHA" };
    gArmatures.add(m);
    barres.push({ x_cm: bar.x_cm, y_cm: bar.y_cm, dia_mm: bar.dia_mm, longueur_m: L - 2 * e });
    triangles += geo.index.count / 3;
  }
  const yInf = geo2d.barres.find((x) => x.nappe === "inf").y_cm;
  const ySup = geo2d.barres.find((x) => x.nappe === "sup").y_cm;

  // etiquettes : positions DEDUITES de la geometrie, pas placees a l'oeil
  const etiquettes = [
    { t: `${inf.n} HA${inf.dia_mm}`, detail: "nappe inférieure", phase: 2, suit: "armatures",
      pos: [0, cm(yInf), L / 2 + 0.02] },
    { t: `${sup.n} HA${sup.dia_mm}`, detail: "nappe supérieure", phase: 2, suit: "armatures",
      pos: [0, cm(ySup), L / 2 + 0.02] },
    { t: `Cadres HA${cadres.dia_mm} / ${cadres.espacement_cm} cm`, detail: `${nCad} cadres`, phase: 2, suit: "armatures",
      pos: [b / 2 + 0.03, 0, 0] },
    { t: `enrobage ${enrobage_cm} cm`, detail: "paramètre de la démonstration (V3)", phase: 2, suit: "armatures",
      pos: [-b / 2 - 0.03, -h / 2 + e / 2, L / 2 * 0.6] },
    { t: "Coffrage", detail: "retiré à la phase 4 (décoffrage)", phase: 1, phaseFin: 3, suit: "coffrage",
      pos: [0, -h / 2 - epC, -L / 2 * 0.7] },
    { t: "Béton", detail: `${b_cm} x ${h_cm} cm`, phase: 3, suit: "beton-couche", pos: [-b / 2 - 0.03, h / 2 - 0.08, 0] },
  ];

  // --- metre RECALCULABLE (V1) : geometrie x masse volumique de l'acier
  const RHO = 7850;                                   // kg/m3 — constante physique
  const aire = (dia_mm) => Math.PI * Math.pow(mm(dia_mm) / 2, 2);
  const masseBarres = barres.reduce((s, x) => s + aire(x.dia_mm) * x.longueur_m * RHO, 0);
  const longCadre = geoCad.userData.longueur_m;
  const masseCadres = aire(cadres.dia_mm) * longCadre * nCad * RHO;
  const volBeton = b * h * L;

  return {
    groupe,
    metre: {
      nCadres: nCad,
      espacementReel_cm: pose.espacement_reel_cm,
      crochets: false,
      positions_barres_cm: barres.map((x) => ({ x: x.x_cm, y: x.y_cm, dia_mm: x.dia_mm })),
      axeCadre_cm: geo2d.axe_cadre_cm,
      longueurCadre_m: longCadre,
      nBarres: barres.length,
      longueurBarre_m: L - 2 * e,
      masseCadres_kg: masseCadres,
      masseBarres_kg: masseBarres,
      masseAcier_kg: masseCadres + masseBarres,
      volumeBeton_m3: volBeton,
      ratio_kg_m3: (masseCadres + masseBarres) / volBeton,
      triangles,
    },
    etiquettes,
    phases: ["Coffrage", "Ferraillage", "Bétonnage", "Décoffrage"],
  };
}
