import * as THREE from "three";

/* Couleurs par materiau — MEME source de verite que les variables CSS de assets/style.css.
   Si tu changes une couleur, change-la aux deux endroits (controle par check.mjs). */
export const COULEURS = {
  beton:     0xb9bbb4,
  acierHA:   0x8c3b2e,
  charpente: 0x41607d,
  sol:       0xa08358,
  cable:     0x6b5a8e,
  coffrage:  0xc9a86a,
  appui:     0x41607d,
};

export const LIBELLES = {
  beton: "béton", acierHA: "acier HA", charpente: "charpente métallique",
  sol: "sol", cable: "câble de précontrainte", coffrage: "coffrage", appui: "appui",
};

const cache = new Map();

/** Materiau partage (un seul par cle : limite les changements d'etat GPU). */
export function materiau(cle, options = {}) {
  const id = cle + "|" + JSON.stringify(options);
  if (cache.has(id)) return cache.get(id);
  const base = {
    color: COULEURS[cle] ?? 0x888888,
    roughness: options.rugosite ?? 0.72,
    metalness: options.metal ?? (cle === "charpente" || cle === "acierHA" ? 0.35 : 0.05),
    transparent: options.opacite != null && options.opacite < 1,
    opacity: options.opacite ?? 1,
    side: options.opacite != null && options.opacite < 1 ? THREE.DoubleSide : THREE.FrontSide,
    depthWrite: !(options.opacite != null && options.opacite < 1),
  };
  const m = new THREE.MeshStandardMaterial(base);
  cache.set(id, m);
  return m;
}

/** Libere tous les materiaux partages (fin de vie de la page). */
export function libererMateriaux() {
  for (const m of cache.values()) m.dispose();
  cache.clear();
}

/** Legende exploitable par l'interface : [{cle, t, couleur}] */
export function legende(cles) {
  return cles.map((c) => ({
    cle: c, t: LIBELLES[c] ?? c,
    couleur: "#" + (COULEURS[c] ?? 0x888888).toString(16).padStart(6, "0"),
  }));
}
