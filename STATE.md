# STATE — avancement du cours

Dernière mise à jour : **15/10/2026** · Étape en cours : **1 — socle, LIVRÉ**
Mode d'exécution : **B** (chat avec bac à sable éphémère, § 12.5)
Phase : **§ 5.0 — SANS CALCULS NORMATIFS** (`normes_disponibles = false`)

## Reprise (mode B — à lire en premier à chaque séance)

- **Dernier livrable** : Étape 1 — socle. Zip : `cours-genie-civil-P1-E1-socle.zip`
- **Commande de contrôle** : `npm ci --ignore-scripts && npm run check`
- **Prochain module** : **Étape 2 — tranche verticale de suivi** (`TV`, § 5.3 adapté) :
  cycle de réalisation d'un plancher de mezzanine, de bout en bout.
  **Le lecteur la valide avant toute duplication** (forme, profondeur, ergonomie, chaîne de données).
- **Règle absolue** : aucun chiffre n'est repris de la mémoire d'une conversation précédente.
  Seul le zip (ou la branche git) fait foi.

## Données figées

| Jeu de données | Version | État |
|---|---|---|
| `data/projet-gare.json` | **1.0** | **FIGÉ** le 15/10/2026 · commit `ad792eb` · tag local `donnees-gare-v1.0` · site S1 (région de Marrakech) |
| `data/projet-r5.json` | **1.0** | **FIGÉ** — cas secondaire léger |
| `data/referentiels.json` | **1.0** | **FIGÉ** — option M (béton, séisme) + E 1re génération (acier) |
| `data/demo-cage.json` | 1.0 | paramètres de la page de démonstration du socle |

## Statut des modules

**Palier 1 — 35 modules, 50 livraisons.** ▶ 23 modules / 30 livraisons actifs ·
⏸ 12 modules / 20 livraisons suspendus.

- **Livré** : `E1` (socle + page de démonstration).
- ▶ **actifs, non écrits** : TV, A1, A2a, A5a, B5a-exec, B7b, B7c, C1, C2, C3, C4, C6, C7,
  D1, D2, D3, D4, D6, D7, M3D, REC, RC1
- ⏸ **suspendus** (§ 5.0.4) : A2b, A3, A4, A5b, B1, B2, B3, B5a-calc, B6, B6b, B7a, R5

**Palier 2** — 12 modules, 26 livraisons · non ouvert.
**Palier 3** — 8 modules, 14 livraisons · non ouvert.

Sommaire et fiches : `cadrage/05-sommaire.md`. Ordre de livraison : § 6 du même fichier.

## Ce que le socle livre (Étape 1, § 5.2)

| Élément | Fichier | Preuve |
|---|---|---|
| Charte graphique + impression | `assets/style.css`, `assets/print.css` | contrastes AA, feuille d'impression des exercices et fiches mémo |
| Bibliothèque SVG paramétrique | `assets/svgkit.js` | 8 générateurs, motifs de matériaux définis une seule fois |
| Bibliothèque 3D | `src/civil3d/`, `assets/civil3d.bundle.js` (763 ko, IIFE) | scène, orbite, matériaux, étiquettes, coupe, éclaté, phasage 4D, armatures, câbles, extrusions |
| Chaîne de build | `build/build.mjs`, `build/md.mjs` | échoue si une variable manque, si une légende est incomplète, si un nombre d'un bloc `:::normatif` n'est pas balisé |
| Calculs + étalonnage | `calc/` | contre-calcul par 2 voies, étalonnage sur solution fermée, unités vérifiées (`pint`) |
| Tests | `tests/rendu.spec.mjs`, `build/check.mjs` | 9 contrôles, 6 tests de rendu, 8 captures examinées |
| Page de démonstration | `modules/00-demo-cage.html` | cage d'armatures paramétrique testée |

## Défauts trouvés et corrigés pendant l'Étape 1 (§ R6, § 12.2)

| # | Défaut | Trouvé par | Correction |
|---|---|---|---|
| 1 | Périmètre du cadre **+23,9 %** : une Catmull-Rom passant par les coins gonfle entre les arcs. Le métré 3D annonçait 12,24 kg de cadres contre 9,88 kg réels | croisement `calc/` ↔ 3D du test `d` | `CourbePolyligne` suivant le contour exact (droites + arcs) ; écart ramené à 0,007 % de la formule fermée |
| 2 | Phase 1 « coffrage » rendait une **image vide** : le modèle annonçait 4 phases mais ne contenait aucun coffrage | variance de pixels, test `b` | coffrage ajouté (fond de moule + 2 joues) ; phasage par **intervalle** pour que le coffrage disparaisse au décoffrage |
| 3 | Le phasage n'était **pas appliqué** à la première construction : l'état initial montrait tout, en contradiction avec le curseur | examen de la capture `defaut.png` | outils appliqués dès la première construction |
| 4 | Étiquettes **flottant dans le vide** du côté retiré par le plan de coupe | examen de `coupe.png` | une étiquette dont l'ancrage est coupé est masquée |
| 5 | Modèle **débordant du cadre** quand un curseur change l'encombrement | examen de `curseurs-max.png` | recadrage automatique au-delà de 15 % de variation, sans perdre l'orientation choisie |
| 6 | Vue éclatée illisible : pièces projetées hors cadre, étiquettes restées sur place | examen de `eclate.png` | éclatement par **couche** (coffrage / armatures / béton) avec direction déclarée ; amplitude 0,35 → 0,16 ; étiquettes solidaires de leur couche |
| 7 | Variables `{{x::fmt}}` cassées dans les tableaux : `\|` sert de séparateur de colonnes | échec du build | séparateur de format `::` |
| 8 | `katex@0.18.0` porte un avis de sécurité (GHSA-238p-pmpm-9mq7) | `npm audit` | épinglé en `0.18.10` ; 0 vulnérabilité |

## Valeurs V2 en attente de vérification par le lecteur

**Aucune dans le cours** : le § 5.0.6 l'interdit dans cette phase, et `npm run check` échoue si une
balise V2 apparaît dans le contenu tant que `normes_disponibles = false`.
Les sources du cadrage sont dans `cadrage/registre-sources-cadrage.csv` (E0-S01 et E0-S06 restent
« à vérifier »).

## Simplifications déclarées (§ R6)

| # | Simplification | Où |
|---|---|---|
| 1 | **Une scène 3D par vue**, initialisée à l'affichage et libérée en sortie, plafond de 4 contextes WebGL — et non un renderer unique à viewport/scissor. C'est la seconde option admise par le § 4.4 ; à revoir si une page devait porter plus de trois vues | `src/civil3d/scene.js` |
| 2 | Le contour du cadre est une **polyligne dense** (0,007 % sous la formule fermée), pas un arc exact | `src/civil3d/armatures.js` |
| 3 | Fiches-module des paliers 2 et 3 volontairement sobres, à revoir à l'ouverture de leur palier | `cadrage/05-sommaire.md` |
| 4 | `print.css` n'imprime pas la 3D : il imprime un substitut textuel. Vérifié par relecture du CSS, **pas** par un test automatique d'impression | `assets/print.css` |

## Dette

| # | Dette | Échéance |
|---|---|---|
| 1 | 12 modules du palier 1 inaccessibles faute de documents normatifs | levée du § 5.0 |
| 2 | Aucun bordereau de prix : tout le volet économique restera V3 | question 7, sans réponse |
| 3 | Dates du palier 1 : **hypothèse V3** (fin du P1 actif au 15/03/2027), non confirmée | § 5.5 |
| 4 | Logiciel aux éléments finis du lecteur inconnu — nécessaire avant B6b (⏸) | avant B6b |
| 5 | Référentiel ferroviaire non identifié (quais, gabarits, caténaire) | CPS du marché |
| 6 | Le contrôle d'impression est visuel, pas automatisé | à outiller si le besoin se confirme |
| 7 | Bundle 3D de 763 ko : hors budget par module, mais c'est le poste le plus lourd du cours | à surveiller |
| 8 | **Les tags git ne sont pas poussables** dans ce bac à sable (le proxy n'expose que `refs/heads/*`) : les tags de palier vivront dans le zip, pas sur GitHub | limite de l'environnement |

## Données modifiées depuis la dernière livraison

`projet-gare.json`, `projet-r5.json`, `referentiels.json` figés en 1.0 ; `demo-cage.json` créé ;
registres régénérés par le build. Empreinte de `data/` : voir le pied de chaque module.

## Effort consommé (§ 13.2)

Étape 0 : 1 séance. Étape 1 : 1 séance (socle complet, 8 défauts trouvés et corrigés, passe /devil).
Hypothèse de budget en place : 2 séances par semaine, ~1,5 séance par livraison (V3, à confirmer).
