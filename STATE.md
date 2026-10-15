# STATE — avancement du cours

Dernière mise à jour : **15/10/2026** · Étape en cours : **0 — cadrage (en attente de validation)**
Mode d'exécution : **B** (chat avec bac à sable éphémère, § 12.5)
Phase : **§ 5.0 — SANS CALCULS NORMATIFS** (`normes_disponibles = false`)

## Reprise (mode B — à lire en premier à chaque séance)

- **Dernier livrable** : Étape 0 — cadrage. Zip : `cours-genie-civil-E0-cadrage.zip`
- **Commande de contrôle** : `npm ci --ignore-scripts && npm run check`
  (à l'Étape 0 le contrôle est **minimal** : intégrité des JSON, présence des pièces de cadrage,
  en-têtes des registres, empreinte de `data/`. Il est remplacé par le vrai `check.mjs` à l'Étape 1.)
- **Prochaine action** : **attendre les réponses du lecteur** aux 10 questions
  (`cadrage/00-questions-etape0.md`). Rien ne se livre avant.
- **Au go** : Étape 1 — socle (§ 5.2), puis Étape 2 — tranche verticale de suivi (§ 5.3 adapté).
- **Règle absolue** : aucun chiffre n'est repris de la mémoire d'une conversation précédente.
  Seul le zip (ou la branche git) fait foi.

## Données figées

| Jeu de données | Version | État |
|---|---|---|
| `data/projet-gare.json` | `0.1-propose` | **NON FIGÉ** — passe en 1.0 + date + commit après validation (§ 5.1c/e) |
| `data/projet-r5.json` | `0.1-propose` | **NON FIGÉ** |
| `data/referentiels.json` | `0.1-propose` | **NON FIGÉ** — question 2 |

## Statut des modules

**Palier 1 — 34 modules, 49 livraisons.** ▶ 22 modules / 28 livraisons actifs · ⏸ 12 modules /
21 livraisons suspendus. **Aucun module écrit à ce jour.**

- ▶ **actifs** : E1, TV, A1, A2a, A5a, B7b, B7c*, C1, C2, C3, C4, C6, C7, D1, D2, D3, D4, D6, D7,
  M3D, REC, RC1
- ⏸ **suspendus** (§ 5.0.4) : A2b, A3, A4, A5b, B1, B2, B3, B5a, B6, B6b, B7a, R5
- *B7c est un **module proposé en addition** au périmètre du § 11 (interfaces ferroviaires) : il
  n'existe qu'après accord du lecteur (question 5).

**Palier 2** — 12 modules, 26 livraisons · non ouvert.
**Palier 3** — 8 modules, 14 livraisons · non ouvert.

Sommaire et fiches : `cadrage/05-sommaire.md`.

## Valeurs V2 en attente de vérification par le lecteur

Aucune valeur V2 normative n'est écrite dans le cours (§ 5.0.6 l'interdit dans cette phase). Les six
sources du cadrage sont dans `cadrage/registre-sources-cadrage.csv`, et les **10 hypothèses V3** du
cadrage (sols, prédimensionnements, prix, effort) dans `cadrage/registre-hypotheses-cadrage.csv`, chacune
avec sa fourchette et son année. Deux sources demandent une vérification :

| id | Point | À vérifier |
|---|---|---|
| E0-S01 | Décrets 2.24.766 / 2.24.767 publiés au BO n° 7351 du 11/11/2024 | lire le **texte officiel** et son **catalogue communal** avant tout calcul sismique (source secondaire, fetch direct bloqué par le proxy) |
| E0-S06 | Décret des marchés publics 2-22-431 (2023) | seul l'avant-projet a été retrouvé |

## Simplifications déclarées (§ R6)

| # | Simplification | Où |
|---|---|---|
| 1 | Contrôle de reprise **minimal** à l'Étape 0 (pas de build, pas de navigateur, pas de test de rendu) : il n'y a encore ni module ni bibliothèque à contrôler. Remplacé à l'Étape 1 par `check.mjs` complet (§ 12.1 a–k). | `build/check-e0.mjs` |
| 2 | Fiches-module des paliers 2 et 3 volontairement sobres, à revoir à l'ouverture de leur palier. | `cadrage/05-sommaire.md` § 5 |

## Dette

| # | Dette | Échéance |
|---|---|---|
| 1 | `pint` (vérification dimensionnelle, § 3.3) non installé | Étape 1 |
| 2 | Chaîne de build, `civil3d`, `svgkit`, tests Playwright : rien n'existe | Étape 1 |
| 3 | 12 modules du palier 1 inaccessibles faute de documents normatifs | levée du § 5.0 par le lecteur |
| 4 | Référentiel **ferroviaire** (quais, gabarits, caténaire) et **effets de foule en gare** : aucun référentiel identifié ; aucun numéro ne sera écrit sans V0 | à fournir par le CPS |
| 5 | Aucun bordereau de prix : tout le volet économique restera V3 (fourchettes, 2026) | question 7 |
| 6 | Date de fin du palier 1 non fixée (exigée par le § 5.5) | question 1 |

## Données modifiées depuis la dernière livraison

Création initiale : `data/projet-gare.json`, `data/projet-r5.json`, `data/referentiels.json`,
registres `data/` (en-têtes seuls), pièces de cadrage `cadrage/00` à `cadrage/06`, registres du cadrage
(6 sources, 10 hypothèses V3).

## Effort consommé (§ 13.2)

Étape 0 : 1 séance (lecture du prompt, vérification d'environnement, 1 recherche web de
re-vérification, production des 9 pièces de cadrage). Pas de point de comparaison : le budget est
demandé en question 1.
