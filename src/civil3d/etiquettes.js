import * as THREE from "three";

/* Etiquettes projetees en espace ecran, avec resolution de collision (§ 9.4).
   Les boites englobantes sont comparees en pixels : c'est ce que le test verifie. */

export class Etiquettes {
  constructor(conteneur) {
    this.conteneur = conteneur;
    this.items = [];
    this.collisions = 0;
  }

  definir(liste) {
    this.vider();
    for (const e of liste) {
      const el = document.createElement("div");
      el.className = "vue3d-etiq";
      el.innerHTML = `<span class="nom"></span>${e.detail ? '<span class="detail"></span>' : ""}`;
      el.querySelector(".nom").textContent = e.t;
      if (e.detail) el.querySelector(".detail").textContent = e.detail;
      el.addEventListener("click", () => el.classList.toggle("ouverte"));
      this.conteneur.appendChild(el);
      this.items.push({ el, base: new THREE.Vector3(...e.pos), pos: new THREE.Vector3(...e.pos),
        t: e.t, phase: e.phase ?? null, phaseFin: e.phaseFin ?? null, suit: e.suit ?? null });
    }
  }

  vider() {
    for (const i of this.items) i.el.remove();
    this.items = [];
    this.collisions = 0;
  }

  /** Une etiquette suit la piece qu'elle designe quand la vue est eclatee : sinon elle
      reste en l'air, a designer du vide. */
  decaler(donneDeplacement) {
    for (const it of this.items) {
      const d = it.suit ? donneDeplacement(it.suit) : null;
      it.pos.copy(it.base);
      if (d) it.pos.add(d);
    }
  }

  /** Une etiquette disparait avec l'element qu'elle designe (ex. le coffrage au decoffrage). */
  filtrerParPhase(n) {
    for (const it of this.items) {
      const hors = (it.phase != null && n < it.phase) || (it.phaseFin != null && n > it.phaseFin);
      it.el.classList.toggle("masquee-phase", hors);
    }
  }

  /** Projette, masque ce qui sort du cadre, puis decale verticalement pour eviter les recouvrements. */
  majPositions(camera, largeur, hauteur, planCoupe = null) {
    const v = new THREE.Vector3();
    const places = [];
    const candidats = this.items.filter((it) => !it.el.classList.contains("masquee-phase")).map((it) => {
      v.copy(it.pos).project(camera);
      return { it, x: (v.x * 0.5 + 0.5) * largeur, y: (-v.y * 0.5 + 0.5) * hauteur, z: v.z };
    }).sort((a, b) => a.z - b.z);               // le plus proche d'abord

    this.collisions = 0;
    for (const c of candidats) {
      const { it } = c;
      // une etiquette qui designe de la matiere retiree par le plan de coupe n'a plus d'objet :
      // sans ce controle elle flotte dans le vide, ce qui donne un rendu faux
      const coupee = planCoupe && planCoupe.distanceToPoint(it.pos) < 0;
      if (coupee || c.z > 1 || c.x < 0 || c.x > largeur || c.y < 0 || c.y > hauteur) {
        it.el.classList.add("masquee");
        continue;
      }
      it.el.classList.remove("masquee");
      const l = it.el.offsetWidth || 80, h = it.el.offsetHeight || 18;
      let y = c.y, essais = 0;
      const chevauche = (yy) => places.some((p) =>
        Math.abs(p.x - c.x) < (p.l + l) / 2 + 2 && Math.abs(p.y - yy) < (p.h + h) / 2 + 2);
      while (chevauche(y) && essais < 14) { y += (h + 4) * (essais % 2 ? -1 : 1) * Math.ceil((essais + 1) / 2); essais++; }
      if (chevauche(y)) { it.el.classList.add("masquee"); this.collisions++; continue; }
      places.push({ x: c.x, y, l, h });
      it.el.style.left = `${c.x.toFixed(1)}px`;
      it.el.style.top = `${y.toFixed(1)}px`;
    }
    return this.collisions;
  }

  /** Rapport pour les tests : nombre d'etiquettes visibles et de chevauchements irresolus. */
  rapport() {
    const visibles = this.items.filter((i) =>
      !i.el.classList.contains("masquee") && !i.el.classList.contains("masquee-phase"));
    const boites = visibles.map((i) => {
      const r = i.el.getBoundingClientRect();
      const p = this.conteneur.getBoundingClientRect();
      return { t: i.t, x: r.left - p.left, y: r.top - p.top, l: r.width, h: r.height };
    });
    let chevauchements = 0;
    for (let i = 0; i < boites.length; i++)
      for (let j = i + 1; j < boites.length; j++) {
        const a = boites[i], b = boites[j];
        if (a.x < b.x + b.l && b.x < a.x + a.l && a.y < b.y + b.h && b.y < a.y + a.h) chevauchements++;
      }
    return { total: this.items.length, visibles: visibles.length, chevauchements,
      masqueesPourCollision: this.collisions };
  }
}
