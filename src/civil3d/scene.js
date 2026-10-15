import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { Etiquettes } from "./etiquettes.js";
import { Coupe, Eclate, Phasage } from "./outils.js";
import { legende as legendeDe, libererMateriaux } from "./materiaux.js";

/* Gestionnaire de vues 3D.
   CHOIX TECHNIQUE (§ 4.4) : une scene est initialisee a l'affichage (IntersectionObserver) et
   LIBEREE en sortie, avec un plafond de contextes WebGL simultanes (file LRU). C'est la seconde
   option admise par le § 4.4 ; elle est plus simple et plus testable que le renderer unique a
   viewport/scissor, pour des pages qui portent une a trois vues.
   Rendu A LA DEMANDE : aucune boucle d'animation si rien ne bouge. */

const PLAFOND_CONTEXTES = 4;
const vivantes = [];                 // ordre d'utilisation, la plus ancienne est liberee d'abord

function webgl2Disponible() {
  try {
    const c = document.createElement("canvas");
    return !!(window.WebGL2RenderingContext && c.getContext("webgl2"));
  } catch { return false; }
}

class Vue {
  constructor(el, options) {
    this.el = el;
    this.o = options;
    this.params = {};
    for (const [k, p] of Object.entries(options.params ?? {})) this.params[k] = p.valeur;
    this.pret = false;
    this.sale = true;
    this.etatCoupe = 0;
    this.etatEclate = 0;
    this.etatPhase = (options.phases ?? []).length || 4;
    this.construireInterface();
    if (!webgl2Disponible()) { this.repli("WebGL2 n'est pas disponible dans ce navigateur."); return; }
    this.observer = new IntersectionObserver((e) => {
      if (e[0].isIntersecting) this.activer(); else this.dormir();
    }, { rootMargin: "120px" });
    this.observer.observe(el);
  }

  /* ---------- interface ---------- */
  construireInterface() {
    this.el.classList.add("vue3d");
    this.el.setAttribute("data-impression",
      this.o.titre ? `Modèle 3D interactif — ${this.o.titre} (non imprimable)` : "Modèle 3D interactif");
    this.toile = document.createElement("canvas");
    this.toile.className = "vue3d-toile";
    this.toile.setAttribute("aria-label", this.o.alt ?? this.o.titre ?? "modèle 3D");
    this.el.appendChild(this.toile);
    this.calqueEtiq = document.createElement("div");
    this.calqueEtiq.className = "vue3d-etiquettes";
    this.el.appendChild(this.calqueEtiq);
    this.etiq = new Etiquettes(this.calqueEtiq);

    this.pilotage = document.createElement("div");
    this.pilotage.className = "vue3d-pilotage";
    this.el.appendChild(this.pilotage);

    for (const [cle, p] of Object.entries(this.o.params ?? {}))
      this.ajouterCurseur(cle, p, (v) => { this.params[cle] = v; this.reconstruire(); });

    const outils = this.o.outils ?? {};
    if (outils.coupe)
      this.ajouterCurseur("__coupe", { min: 0, max: 1, pas: 0.02, valeur: 0, libelle: "coupe" },
        (v) => { this.etatCoupe = v; this.appliquerOutils(); });
    if (outils.eclate)
      this.ajouterCurseur("__eclate", { min: 0, max: 1, pas: 0.02, valeur: 0, libelle: "éclaté" },
        (v) => { this.etatEclate = v; this.appliquerOutils(); });
    if (outils.phasage && (this.o.phases ?? []).length) {
      const n = this.o.phases.length;
      this.ajouterCurseur("__phase",
        { min: 1, max: n, pas: 1, valeur: n, libelle: "phase", format: (v) => this.o.phases[v - 1] },
        (v) => { this.etatPhase = v; this.appliquerOutils(); });
    }
    const b = document.createElement("button");
    b.type = "button"; b.textContent = "Réinitialiser la vue";
    b.addEventListener("click", () => this.reinitialiser());
    this.pilotage.appendChild(b);
  }

  ajouterCurseur(cle, p, surChangement) {
    const lab = document.createElement("label");
    const span = document.createElement("span");
    span.textContent = p.libelle ?? cle;
    const input = document.createElement("input");
    input.type = "range"; input.min = p.min; input.max = p.max; input.step = p.pas;
    input.value = p.valeur;
    input.setAttribute("aria-label", p.libelle ?? cle);
    const val = document.createElement("span");
    val.className = "val";
    const afficher = (v) => { val.textContent = p.format ? p.format(v) : `${v}${p.unite ? " " + p.unite : ""}`; };
    afficher(p.valeur);
    input.addEventListener("input", () => {
      const v = Number(input.value);
      afficher(v);
      surChangement(v);
    });
    lab.append(span, input, val);
    this.pilotage.appendChild(lab);
    (this.curseurs ??= {})[cle] = { input, p, afficher };
  }

  repli(message) {
    this.toile?.remove();
    const d = document.createElement("div");
    d.className = "vue3d-repli";
    d.textContent = `${message} Le contenu technique est donné par les schémas et le texte ci-dessous.`;
    this.el.insertBefore(d, this.pilotage);
    this.el.dataset.repli = "1";
  }

  /* ---------- cycle de vie ---------- */
  activer() {
    if (this.pret) { this.demanderRendu(); return; }
    while (vivantes.length >= PLAFOND_CONTEXTES) vivantes.shift()?.dormir();
    try {
      this.renderer = new THREE.WebGLRenderer({
        canvas: this.toile, antialias: true, alpha: false,
        preserveDrawingBuffer: !!window.__CIVIL3D_TEST__,
      });
    } catch (e) { this.repli("Le rendu 3D n'a pas pu démarrer."); return; }
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));   // § 4.4
    this.renderer.setClearColor(0xeceeea, 1);
    this.renderer.localClippingEnabled = true;

    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(42, 16 / 10, 0.05, 200);
    this.controls = new OrbitControls(this.camera, this.el);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.12;
    this.controls.addEventListener("change", () => this.demanderRendu());

    this.scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8f86, 2.0));
    const dir = new THREE.DirectionalLight(0xffffff, 1.5);
    dir.position.set(3, 5, 4);
    this.scene.add(dir);

    this.racine = new THREE.Group();
    this.scene.add(this.racine);

    this.ro = new ResizeObserver(() => this.redimensionner());
    this.ro.observe(this.el);

    this.pret = true;
    vivantes.push(this);
    this.reconstruire(true);
    this.el.dataset.pret = "1";
  }

  dormir() {
    if (!this.pret) return;
    const i = vivantes.indexOf(this);
    if (i >= 0) vivantes.splice(i, 1);
    this.viderRacine();
    this.ro?.disconnect();
    this.controls?.dispose();
    this.renderer?.dispose();
    this.renderer?.forceContextLoss?.();
    this.renderer = null;
    this.etiq.vider();
    this.pret = false;
    delete this.el.dataset.pret;
  }

  viderRacine() {
    this.racine?.traverse((o) => {
      if (o.geometry) o.geometry.dispose();
      if (o.isInstancedMesh) o.dispose?.();
    });
    while (this.racine?.children.length) this.racine.remove(this.racine.children[0]);
  }

  /* ---------- construction ---------- */
  reconstruire(premier = false) {
    if (!this.pret) return;
    this.viderRacine();
    const res = this.o.construire(this.params, { THREE });
    this.contenu = res;
    this.racine.add(res.groupe);
    this.triangles = res.metre?.triangles ?? 0;

    this.boite = new THREE.Box3().setFromObject(res.groupe);
    this.coupe = new Coupe(this.renderer, this.boite, this.o.axeCoupe ?? "z");
    this.eclate = new Eclate(res.groupe);
    this.phasage = new Phasage(res.groupe, this.o.phases ?? res.phases ?? []);
    this.materiaux = [];
    res.groupe.traverse((o) => { if (o.material && !this.materiaux.includes(o.material)) this.materiaux.push(o.material); });

    this.etiq.definir(res.etiquettes ?? []);
    if (res.legende?.length || this.o.legende?.length) this.afficherLegende(res.legende ?? legendeDe(this.o.legende));

    // Les outils sont appliques des la PREMIERE construction : sans cela l'etat initial
    // affiche tout (coffrage compris), ce qui contredit la phase affichee par le curseur.
    this.appliquerOutils();
    const diag = this.boite.getSize(new THREE.Vector3()).length();
    if (premier) this.reinitialiser();
    else if (Math.abs(diag - (this.diagPrec ?? diag)) / (this.diagPrec || 1) > 0.15) this.recadrer();
    this.diagPrec = diag;
    this.demanderRendu();
    this.el.dataset.triangles = String(Math.round(this.triangles));
  }

  afficherLegende(entrees) {
    this.legendeEl?.remove();
    const d = document.createElement("div");
    d.className = "vue3d-legende";
    for (const e of entrees) {
      const s = document.createElement("span");
      const i = document.createElement("i");
      i.style.background = e.couleur;
      s.append(i, document.createTextNode(e.t));
      d.appendChild(s);
    }
    this.el.appendChild(d);
    this.legendeEl = d;
  }

  appliquerOutils() {
    if (!this.pret) return;
    this.coupe.definirBoite(new THREE.Box3().setFromObject(this.contenu.groupe));
    this.coupe.regler(this.etatCoupe);
    this.coupe.appliquer(this.materiaux);
    // 0,16 et non 0,35 : au-dela, les pieces sortent du cadre et la vue eclatee ne montre plus rien
    this.eclate.regler(this.etatEclate * Math.max(0.12, this.boite.getSize(new THREE.Vector3()).length() * 0.16));
    this.etiq.decaler((nom) => this.eclate.deplacement(nom));
    this.phasage.regler(this.etatPhase);
    this.etiq.filtrerParPhase(this.etatPhase);
    this.demanderRendu();
  }

  /** Recadre sans perdre l'orientation choisie par le lecteur : seuls la cible et
      l'eloignement sont repris, quand un curseur change l'encombrement du modele. */
  recadrer() {
    if (!this.pret) return;
    const taille = this.boite.getSize(new THREE.Vector3());
    const centre = this.boite.getCenter(new THREE.Vector3());
    const dir = this.camera.position.clone().sub(this.controls.target).normalize();
    const d = Math.max(taille.length() * 1.15, 0.6);
    this.camera.position.copy(centre).addScaledVector(dir, d);
    this.controls.target.copy(centre);
    this.controls.update();
    this.demanderRendu();
  }

  reinitialiser() {
    if (!this.pret) return;
    const taille = this.boite.getSize(new THREE.Vector3());
    const centre = this.boite.getCenter(new THREE.Vector3());
    const d = Math.max(taille.length() * 1.15, 0.6);
    this.camera.position.set(centre.x + d * 0.62, centre.y + d * 0.44, centre.z + d * 0.72);
    this.controls.target.copy(centre);
    this.controls.update();
    this.redimensionner();
  }

  redimensionner() {
    if (!this.pret) return;
    const l = this.el.clientWidth, h = this.toile.clientHeight || Math.round(l * 10 / 16);
    if (!l || !h) return;
    this.renderer.setSize(l, h, false);
    this.camera.aspect = l / h;
    this.camera.updateProjectionMatrix();
    this.demanderRendu();
  }

  /* ---------- rendu a la demande ---------- */
  demanderRendu() {
    if (!this.pret || this.enAttente) return;
    this.enAttente = true;
    requestAnimationFrame(() => {
      this.enAttente = false;
      if (!this.pret) return;
      const bougeEncore = this.controls.enableDamping && this.controls.update();
      this.renderer.render(this.scene, this.camera);
      this.etiq.majPositions(this.camera, this.el.clientWidth, this.toile.clientHeight,
        this.coupe?.active ? this.coupe.plan : null);
      if (bougeEncore) this.demanderRendu();
    });
  }

  /* ---------- pour les tests (§ 12.1 b, c) ---------- */
  diagnostic() {
    return {
      pret: this.pret, repli: !!this.el.dataset.repli, triangles: Math.round(this.triangles ?? 0),
      etiquettes: this.etiq.rapport(),
      params: { ...this.params }, coupe: this.etatCoupe, eclate: this.etatEclate, phase: this.etatPhase,
      metre: this.contenu?.metre ?? null,
      // positions reelles, pour que les tests confrontent la GEOMETRIE a data/ (§ 12.1 d)
      barres: this.contenu?.metre?.positions_barres_cm ?? null,
      axeCadre: this.contenu?.metre?.axeCadre_cm ?? null,
      contextesVivants: vivantes.length,
    };
  }

  /** Variance des pixels : prouve que la scene n'est pas vide (§ 12.1 b). */
  varianceRendu() {
    if (!this.pret) return null;
    this.renderer.render(this.scene, this.camera);
    const l = 120, h = 75;
    const c2 = document.createElement("canvas");
    c2.width = l; c2.height = h;
    const ctx = c2.getContext("2d");
    ctx.drawImage(this.toile, 0, 0, l, h);
    const d = ctx.getImageData(0, 0, l, h).data;
    let s = 0, s2 = 0, n = 0;
    for (let i = 0; i < d.length; i += 4) {
      const g = 0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2];
      s += g; s2 += g * g; n++;
    }
    const moy = s / n;
    return Math.sqrt(Math.max(0, s2 / n - moy * moy));
  }

  /** Pilotage par les tests : regle un curseur a une valeur et reconstruit. */
  reglerCurseur(cle, valeur) {
    const c = this.curseurs?.[cle];
    if (!c) return false;
    c.input.value = valeur;
    c.input.dispatchEvent(new Event("input"));
    return true;
  }
  bornes(cle) {
    const c = this.curseurs?.[cle];
    return c ? { min: Number(c.input.min), max: Number(c.input.max) } : null;
  }
}

const registre = [];

export function vue(el, options) {
  const v = new Vue(typeof el === "string" ? document.querySelector(el) : el, options);
  registre.push(v);
  return v;
}

export function vues() { return registre; }
export function libererTout() { for (const v of registre) v.dormir(); libererMateriaux(); }
