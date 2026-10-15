import * as THREE from "three";
import { materiau } from "./materiaux.js";

/* Helpers de geometrie : extrusions de profils et cables.
   Tout est en METRES dans la scene ; les donnees arrivent en cm ou mm et sont converties ici. */

export const cm = (v) => v / 100;
export const mm = (v) => v / 1000;

/**
 * Courbe suivant EXACTEMENT une polyligne, parametree par longueur d'arc.
 *
 * Pourquoi elle existe : un contour fait de droites et d'arcs (un cadre d'armature, par
 * exemple) n'est PAS une spline. Une CatmullRomCurve3 passant par les points du contour
 * gonfle entre eux — mesure faite : +23,9 % sur le perimetre d'un cadre quand on ne lui
 * donne que les coins, et encore +1,2 % avec un contour densifie. L'erreur se voit a peine
 * a l'ecran et fausse completement le metre. Ici la longueur est celle de la polyligne.
 */
export class CourbePolyligne extends THREE.Curve {
  constructor(points, fermee = false) {
    super();
    this.points = fermee ? [...points, points[0]] : [...points];
    this.cumul = [0];
    for (let i = 1; i < this.points.length; i++)
      this.cumul.push(this.cumul[i - 1] + this.points[i].distanceTo(this.points[i - 1]));
    this.longueur = this.cumul[this.cumul.length - 1];
  }
  getLength() { return this.longueur; }
  getPoint(t, cible = new THREE.Vector3()) {
    const s = Math.min(Math.max(t, 0), 1) * this.longueur;
    let i = 1;
    while (i < this.cumul.length - 1 && this.cumul[i] < s) i++;
    const l0 = this.cumul[i - 1], l1 = this.cumul[i];
    const u = l1 - l0 < 1e-12 ? 0 : (s - l0) / (l1 - l0);
    return cible.copy(this.points[i - 1]).lerp(this.points[i], u);
  }
}

/** Profil ferme -> solide extrude. `profil` : [[x,y], ...] en metres, dans le plan XY. */
export function extruder(profil, longueur, { cle = "beton", opacite, biseau = 0 } = {}) {
  const forme = new THREE.Shape();
  profil.forEach(([x, y], i) => (i ? forme.lineTo(x, y) : forme.moveTo(x, y)));
  forme.closePath();
  const geo = new THREE.ExtrudeGeometry(forme, {
    depth: longueur, bevelEnabled: biseau > 0, bevelSize: biseau, bevelThickness: biseau, curveSegments: 8,
  });
  geo.translate(0, 0, -longueur / 2);
  const m = new THREE.Mesh(geo, materiau(cle, { opacite }));
  m.userData.triangles = geo.index ? geo.index.count / 3 : geo.attributes.position.count / 3;
  return m;
}

/** Profil en I (charpente) : h, b, tw, tf en metres. */
export function profilI({ h, b, tw, tf }) {
  const x = b / 2, w = tw / 2;
  return [[-x, -h / 2], [x, -h / 2], [x, -h / 2 + tf], [w, -h / 2 + tf], [w, h / 2 - tf],
          [x, h / 2 - tf], [x, h / 2], [-x, h / 2], [-x, h / 2 - tf], [-w, h / 2 - tf],
          [-w, -h / 2 + tf], [-x, -h / 2 + tf]];
}

/** Cable sur courbe : TubeGeometry sur CatmullRomCurve3 (§ 9.1). */
export function cable(points, { diametre_mm = 100, cle = "cable", segments = 64, ferme = false } = {}) {
  const courbe = new THREE.CatmullRomCurve3(points.map((p) => new THREE.Vector3(...p)), ferme,
    "catmullrom", 0.5);
  const geo = new THREE.TubeGeometry(courbe, segments, mm(diametre_mm) / 2, 10, ferme);
  const m = new THREE.Mesh(geo, materiau(cle));
  m.userData.triangles = geo.index.count / 3;
  m.userData.longueur_m = courbe.getLength();
  return m;
}

/** Gaine translucide autour d'un trace de cable. */
export function gaine(points, { diametre_mm = 140, segments = 64 } = {}) {
  const courbe = new THREE.CatmullRomCurve3(points.map((p) => new THREE.Vector3(...p)), false,
    "catmullrom", 0.5);
  const geo = new THREE.TubeGeometry(courbe, segments, mm(diametre_mm) / 2, 12, false);
  const m = new THREE.Mesh(geo, materiau("beton", { opacite: 0.22 }));
  m.renderOrder = 2;
  m.userData.triangles = geo.index.count / 3;
  return m;
}

/** Libere recursivement geometries et materiaux non partages. */
export function liberer(objet) {
  objet.traverse((o) => {
    if (o.geometry) o.geometry.dispose();
    if (o.material && o.material.userData?.jetable) o.material.dispose();
  });
}
