/* Point d'entree bundle en IIFE -> window.Civil3D (§ 4.4 : pas de module ES en file://). */
import * as THREE from "three";
import { vue, vues, libererTout } from "./civil3d/scene.js";
import { cage } from "./civil3d/armatures.js";
import { extruder, profilI, cable, gaine, cm, mm, liberer } from "./civil3d/geometrie.js";
import { materiau, legende, COULEURS, LIBELLES } from "./civil3d/materiaux.js";
import { Coupe, Eclate, Phasage } from "./civil3d/outils.js";
import { Etiquettes } from "./civil3d/etiquettes.js";

export { THREE, vue, vues, libererTout, cage, extruder, profilI, cable, gaine, cm, mm, liberer,
  materiau, legende, COULEURS, LIBELLES, Coupe, Eclate, Phasage, Etiquettes };
export const version = "1.0.0";
