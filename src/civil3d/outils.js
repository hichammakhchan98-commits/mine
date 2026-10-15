import * as THREE from "three";

/* Coupe (plans de clipping), vue eclatee et phasage 4D : trois outils qui agissent
   sur un groupe deja construit, sans le reconstruire. */

/** Plan de coupe pilote par un curseur 0..1 le long d'un axe. */
export class Coupe {
  constructor(renderer, boite, axe = "z") {
    this.plan = new THREE.Plane(new THREE.Vector3(0, 0, -1), 0);
    this.renderer = renderer;
    this.axe = axe;
    this.boite = boite;
    this.active = false;
    renderer.localClippingEnabled = true;
  }
  definirBoite(boite) { this.boite = boite; }
  /** t = 0 : pas de coupe ; t = 1 : coupe a l'autre extremite. */
  regler(t) {
    const n = { x: [-1, 0, 0], y: [0, -1, 0], z: [0, 0, -1] }[this.axe];
    const min = this.boite.min[this.axe], max = this.boite.max[this.axe];
    const pos = min + (max - min) * t;
    this.plan.normal.set(...n);
    this.plan.constant = pos * -n[{ x: 0, y: 1, z: 2 }[this.axe]];
    this.active = t > 0.001;
  }
  appliquer(materiaux) {
    for (const m of materiaux) {
      m.clippingPlanes = this.active ? [this.plan] : null;
      m.needsUpdate = true;
    }
  }
}

/** Vue eclatee : chaque enfant s'ecarte du centre proportionnellement a `t`. */
export class Eclate {
  constructor(groupe) {
    this.groupe = groupe;
    this.origines = new Map();
    this.directions = new Map();
    const centre = new THREE.Box3().setFromObject(groupe).getCenter(new THREE.Vector3());
    for (const enfant of groupe.children) {
      this.origines.set(enfant, enfant.position.clone());
      // Direction declaree par le constructeur si elle existe : un eclate utile separe des
      // COUCHES (coffrage, armatures, beton), pas chaque barre dans une direction differente.
      let d;
      if (enfant.userData?.eclate) d = new THREE.Vector3(...enfant.userData.eclate);
      else {
        const c = new THREE.Box3().setFromObject(enfant).getCenter(new THREE.Vector3());
        d = c.sub(centre);
        if (d.lengthSq() < 1e-6) d.set(0, 1, 0);
      }
      this.directions.set(enfant, d.normalize());
    }
  }
  regler(t) {
    this.deplacements = new Map();
    for (const [enfant, p0] of this.origines) {
      const d = this.directions.get(enfant);
      enfant.position.copy(p0).addScaledVector(d, t);
      this.deplacements.set(enfant.name, d.clone().multiplyScalar(t));
    }
  }
  /** Deplacement applique a une piece, pour que son etiquette la suive. */
  deplacement(nom) { return this.deplacements?.get(nom) ?? null; }
}

/**
 * Phasage 4D. Un element est visible de sa phase d'apparition (userData.phase) a sa phase
 * de disparition incluse (userData.phaseFin, facultative). Sans intervalle, on ne peut pas
 * representer un decoffrage : le coffrage doit POUVOIR disparaitre.
 */
export class Phasage {
  constructor(groupe, noms = []) {
    this.groupe = groupe;
    this.noms = noms;
    this.n = noms.length;
  }
  regler(n) {
    this.n = n;
    this.groupe.traverse((o) => {
      const u = o.userData;
      if (u && u.phase != null)
        o.visible = u.phase <= n && (u.phaseFin == null || n <= u.phaseFin);
    });
  }
  nom(n) { return this.noms[Math.max(0, Math.min(this.noms.length - 1, n - 1))] ?? `phase ${n}`; }
}
