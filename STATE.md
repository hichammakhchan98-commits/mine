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

## Grille d'auto-évaluation § 7.2 — page de démonstration E1

Notée après la passe /devil, qui avait relevé deux critères sous le minimum de 2.

| Critère | Note | Appui |
|---|:--:|---|
| Le « pourquoi » est expliqué | 3 | chaque mécanisme est justifié avant d'être montré |
| Les hypothèses sont explicites | 3 | *était 1* — rayon de cintrage, convention d'enrobage et absence de crochets sont maintenant publiés et balisés V3 |
| Les formules sont justifiées | 2 | périmètre démontré ; masse volumique posée en constante |
| L'exemple est vérifié | 3 | deux voies divergentes, étalonnage indépendant, canari rejoué |
| Le piège est identifié | 3 | trois pièges, dont deux trouvés sur ce livrable même |
| Lien avec l'exécution | 2 | *était 1* — cadences de façonnage, nombre de cadres comme grandeur de planning |
| Lien avec le coût et le délai | 2 | *était 0* — prix de l'acier et cadence, en V3 déclarées |

**Minimum 2 partout : tenu.** La page reste une démonstration de socle, pas un module de cours : les
notes de 2 sur l'exécution et l'économie sont volontaires, ces sujets appartiennent à D1, D3 et C3.

## Passe adversariale /devil (§ 12.2)

Portée par un **sous-agent distinct**, qui n'a pas lu le raisonnement de l'auteur et a recalculé les
valeurs clés à partir de `data/` seul. Rapport : `QA/E1-socle.md`.

**Trois passes ont été nécessaires.**

| Passe | Verdict | Corrigé |
|---|---|---|
| 1 | 26 défauts — **5 bloquants**, 9 majeurs, 12 mineurs | tous bloquants et majeurs, m1–m6, m9–m11 |
| 2 | 14 défauts — **1 bloquant**, 7 majeurs, 6 mineurs. **3 canaris franchissaient les 11 contrôles** | le bloquant, les 7 majeurs, les 6 mineurs |
| 3 | 10 défauts — **0 bloquant**, 4 majeurs, 6 mineurs. 2 nouveaux canaris rouges (erreur de modèle *partagée*) | les 4 majeurs, les 6 mineurs |

**Le § 12.2 est satisfait : zéro bloquant.** Rapports : `QA/E1-socle.md`, `QA/E1-socle-passe2.md`,
`QA/E1-socle-passe3.md`.

**Ce que ces trois passes ont appris, et qui vaut pour tout le cours.** Deux fois, une correction
s'est retournée : le contrôle « dépôt propre » ajouté en passe 1 cassait la reprise du mode B sur un
clone neuf, et le paragraphe de coût ajouté pour combler une note faible réintroduisait un nombre
tapé à la main **et faux**. Une correction est un changement comme un autre : elle se relit.

**Canaris (§ 12.2, contrôle du relecteur).** 12 joués au total sur les trois passes. Tous rouges à ce
jour : barres SVG empilées, enrobage 3D ignoré, régression du diamètre de tube, décalage vertical,
resserrement de 20 %, divergence de règle Python/JS, comptage faux des deux côtés, règle de placement
faussée des deux côtés, règle d'axe faussée des deux côtés, coût faux d'un facteur 10, V3 publiée
sans balise, longueur de barre fausse des deux côtés.

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

### Corrigés après la passe /devil

| # | Défaut | Gravité | Correction |
|---|---|---|---|
| B1 | La 3D dessinait les cadres à **⌀ 4 mm** en les étiquetant « HA8 » : un `/2` appliqué deux fois | bloquant | le paramètre est un diamètre, divisé une seule fois ; un test vérifie le rayon réel du tube |
| B2 | SVG et 3D plaçaient les barres **4 à 8 mm** l'une de l'autre à partir du même fichier | bloquant | une **règle unique** (`src/civil3d/section.js`), livrée aussi en `assets/section.js`, consommée par les deux |
| B3 | La figure 1 commettait l'erreur que sa propre légende dénonçait | bloquant | résolu par B2 |
| B4 | L'axe du cadre était posé **sur** la ligne d'enrobage : enrobage réel 26 mm pour 30 annoncés | bloquant | l'enrobage se mesure à la peau du cadre ; convention publiée dans `data/` et testée |
| B5 | Le « contre-calcul par deux voies indépendantes » était la même formule à constante arrondie | bloquant | voie A = contour discrétisé + premiers principes ; voie B = formule fermée + coefficient tabulé : les deux chemins diffèrent |
| M1 | Rayon de cintrage en dur, **dupliqué** Python/JS, jamais publié, et « 2,5 ⌀ » est une règle constructive interdite en § 5.0 | majeur | paramètre de tracé dans `data/`, lu des deux côtés, affiché, balisé V3 |
| M2 | Les registres de `data/` étaient **vides** alors que la page publiait des V3 | majeur | V3 balisées dans le contenu ; `check.mjs` échoue si une V3 publiée n'a pas sa ligne |
| M3 | « treize instances », « 13 à 28 », « 11 kg » tapés à la main — que l'exercice de la page rendait faux | majeur | variables ; les valeurs attendues de l'exercice sont **calculées** par `calc/` |
| M4 | Trois assertions ne pouvaient pas échouer (périmètre retapé, « A ≠ B » satisfait par un arrondi, verdict `pint` vrai par construction) | majeur | cas à solution connue hors formule ; erreurs injectées qui **doivent** déplacer le résultat ; `pint` alimenté par `data/` et vérifiant qu'une formule non homogène lève |
| M5 | L'étalonnage ne discrétisait que les arcs, soit **6,5 %** du périmètre | majeur | polygonalisation indépendante du contour entier + deux cas à solution connue |
| M6 | **Canari : deux erreurs géométriques franchissaient les 9 contrôles** | majeur | test géométrique qui recalcule positions et enrobage **dans le test**, sans appeler le code de production ; les deux canaris sont maintenant rouges |
| M7 | Le garde-fou d'ordre de grandeur n'attrapait qu'un facteur 10 | majeur | renommé `garde_fou_unite`, et doublé d'un contrôle de cohérence interne (masse linéique des cadres) |
| M8 | Le livrable de l'Étape 1 n'était pas committé | majeur | committé ; `check.mjs` exige désormais un arbre de travail propre |
| M9 | Cadres sans crochets : simplification non signalée (−2,7 %) | majeur | déclarée dans la page, dans `data/` et dans la sortie de `calc/` |
| M10 | La règle qui comptait les cadres ne décrivait pas celle qui les plaçait | majeur | règle unique ; et elle était fausse — l'espacement réel **dépassait** le nominal. 14 cadres, et non 13 |

### Corrigés après la passe 2

| # | Défaut | Gravité | Correction |
|---|---|---|---|
| N2 | La page affirmait deux voies « indépendantes » : faux pour la masse (0,00617 dérive de π/4 × 7850 × 10⁻⁶) et les deux partagent comptage, règle d'axe et longueurs | bloquant | la page liste ce qu'elles partagent et ce que le contrôle **n'attrape pas** ; le comptage est recalculé dans le test |
| N1 | L'enrobage n'était pas appliqué le long de l'axe : about réel 26 mm pour 30 annoncés | majeur | premier cadre à `enrobage + ⌀/2` de l'about, des deux côtés |
| N3 | Registre des hypothèses aux colonnes inversées, `fourchette` et `annee_ref` vides | majeur | balises V3 structurées ; le build échoue sans fourchette ni année |
| N4 | Le paragraphe de coût ajouté en passe 1 réintroduisait un nombre **faux** (450 pour 433) | majeur | montants calculés par `calc/` |
| N5 | L'anecdote d'étalonnage publiait les valeurs d'avant correction | majeur | variables |
| N6 | `calc/__pycache__` versionné : le contrôle « dépôt propre » **échouait sur tout clone neuf** | majeur | ignoré et retiré du suivi |
| N7, N8 | Aucun test ne mesurait le diamètre du tube ; le test SVG ne comparait jamais `cy` et recalait son échelle sur les barres contrôlées | majeur | diamètre mesuré ; échelle déduite du rectangle de section, `cx`, `cy` et rayon comparés |

### Corrigés après la passe 3

| # | Défaut | Gravité | Correction |
|---|---|---|---|
| P1 | La page publiait **un nombre faux** (20 mm au lieu de 34), avec une auto-correction laissée dans le texte, sous un encart « Trois simplifications » qui en listait quatre | majeur | texte repris |
| P2 | La phrase désignait un filet inexistant : l'étalonnage n'attrape rien de ces erreurs. Et la longueur de barre n'était recalculée nulle part | majeur | phrase corrigée ; recalcul indépendant ajouté |
| P3 | Le bloc économique n'était testé **nulle part** : un coût faux d'un facteur 10 passait | majeur | montants et heures recalculés, et confrontés au texte publié |
| P4 | Le contrôle de balisage cessait d'exiger quoi que ce soit dès qu'**une** balise existait | majeur | toute mention « (V3 » hors balise échoue |

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
| 5 | **Cadres sans crochets d'extrémité** : le métré est minorant d'environ 3 %. La longueur d'un crochet est une valeur constructive, interdite en § 5.0 | `data/demo-cage.json` → `conventions` |
| 6 | Le coffrage modélisé n'a **ni étaiement ni étais de reprise**, et le décoffrage est animé sans condition de résistance | page de démonstration |

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

Étape 0 : 1 séance. Étape 1 : 2 séances (socle complet ; 8 défauts trouvés en construisant, puis **50 défauts sur trois passes adversariales**, tous bloquants et majeurs corrigés).
Hypothèse de budget en place : 2 séances par semaine, ~1,5 séance par livraison (V3, à confirmer).
