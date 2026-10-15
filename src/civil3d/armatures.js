import * as THREE from "three";
import { materiau } from "./materiaux.js";
import { cm, mm, CourbePolyligne } from "./geometrie.js";

/* Helpers d'armatures. Les armatures repetitives (cadres) passent par InstancedMesh (§ 4.4).
   ATTENTION : cette bibliotheque DESSINE une geometrie a partir de parametres.
   Elle ne dimensionne rien et ne verifie aucune regle. */

/**
 * Un cadre rectangulaire a coins arrondis, comme tube ferme sur le contour EXACT
 * (droites + arcs). Le contour est echantillonne puis suivi par une CourbePolyligne :
 * sa longueur est a 0,02 % de la formule fermee P = 2(b-2r) + 2(h-2r) + 2.pi.r,
 * que calc/etalonnage/perimetre_cadre.py etalonne de son cote.
 */
function geometrieCadre(b, h, r, diaBarre, nArc = 10, nDroite = 8, segments = 160) {
  if (2 * r > Math.min(b, h)) throw new Error(`rayon de cintrage ${r} incompatible avec ${b} x ${h}`);
  const pts = [];
  const coins = [[b / 2 - r, h / 2 - r, 0], [-(b / 2 - r), h / 2 - r, Math.PI / 2],
                 [-(b / 2 - r), -(h / 2 - r), Math.PI], [b / 2 - r, -(h / 2 - r), -Math.PI / 2]];
  for (let c = 0; c < 4; c++) {
    const [cx, cy, a0] = coins[c];
    for (let i = 0; i <= nArc; i++) {                       // l'arc du coin
      const a = a0 + (i / nArc) * (Math.PI / 2);
      pts.push(new THREE.Vector3(cx + r * Math.cos(a), cy + r * Math.sin(a), 0));
    }
    const suiv = coins[(c + 1) % 4];                        // puis la droite jusqu'au coin suivant
    const fin = new THREE.Vector3(cx + r * Math.cos(a0 + Math.PI / 2), cy + r * Math.sin(a0 + Math.PI / 2), 0);
    const deb = new THREE.Vector3(suiv[0] + r * Math.cos(suiv[2]), suiv[1] + r * Math.sin(suiv[2]), 0);
    for (let i = 1; i < nDroite; i++) pts.push(fin.clone().lerp(deb, i / nDroite));
  }
  const courbe = new CourbePolyligne(pts, true);
  const geo = new THREE.TubeGeometry(courbe, segments, diaBarre / 2, 6, true);
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

  // --- cadres : InstancedMesh (armatures repetitives)
  const dCad = mm(cadres.dia_mm);
  const bc = b - 2 * e, hc = h - 2 * e;           // cadre a l'interieur de l'enrobage
  const rayon = Math.max(2.5 * dCad, 0.02);
  const geoCad = geometrieCadre(bc, hc, rayon, dCad / 2);
  const esp = cm(cadres.espacement_cm);
  const nCad = Math.max(2, Math.floor((L - 2 * e) / esp) + 1);
  const inst = new THREE.InstancedMesh(geoCad, materiau("acierHA"), nCad);
  inst.name = "cadres";
  const M = new THREE.Matrix4();
  const z0 = -(nCad - 1) * esp / 2;
  for (let i = 0; i < nCad; i++) inst.setMatrixAt(i, M.makeTranslation(0, 0, z0 + i * esp));
  inst.instanceMatrix.needsUpdate = true;
  inst.userData = { phase: 2, materiau: "acierHA", etiquette: `Cadres HA${cadres.dia_mm}`,
    detail: `${nCad} cadres, espacement ${cadres.espacement_cm} cm` };
  gArmatures.add(inst);
  triangles += (geoCad.index.count / 3) * nCad;

  // --- barres longitudinales
  const barres = [];
  const poseNappe = (nappe, bas) => {
    const d = mm(nappe.dia_mm);
    const y = bas ? -h / 2 + e + dCad + d / 2 : h / 2 - e - dCad - d / 2;
    const dispo = bc - dCad - d;                     // place utile entre brins de cadre
    const geo = new THREE.CylinderGeometry(d / 2, d / 2, L - 2 * e, 10, 1);
    geo.rotateX(Math.PI / 2);
    for (let i = 0; i < nappe.n; i++) {
      const x = nappe.n === 1 ? 0 : -dispo / 2 + (dispo * i) / (nappe.n - 1);
      const m = new THREE.Mesh(geo, materiau("acierHA"));
      m.position.set(x, y, 0);
      m.name = `barre-${bas ? "inf" : "sup"}-${i + 1}`;
      m.userData = { phase: 2, materiau: "acierHA" };
      gArmatures.add(m);
      barres.push({ x, y, dia_mm: nappe.dia_mm, longueur_m: L - 2 * e });
    }
    triangles += (geo.index.count / 3) * nappe.n;
    return { y, d };
  };
  const pInf = poseNappe(inf, true);
  const pSup = poseNappe(sup, false);

  // etiquettes : positions DEDUITES de la geometrie, pas placees a l'oeil
  const etiquettes = [
    { t: `${inf.n} HA${inf.dia_mm}`, detail: "nappe inférieure", phase: 2, suit: "armatures",
      pos: [0, pInf.y, L / 2 + 0.02] },
    { t: `${sup.n} HA${sup.dia_mm}`, detail: "nappe supérieure", phase: 2, suit: "armatures",
      pos: [0, pSup.y, L / 2 + 0.02] },
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
