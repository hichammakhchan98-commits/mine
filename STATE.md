# STATE — avancement du cours

Dernière mise à jour : **16/10/2026** · Étape en cours : **2 — tranche verticale, corrigée après la passe /devil n° 1**
Mode d'exécution : **B** (chat avec bac à sable éphémère, § 12.5)
Phase : **§ 5.0 — SANS CALCULS NORMATIFS** (`normes_disponibles = false`)

## Reprise (mode B — à lire en premier à chaque séance)

- **Dernier livrable** : Étape 2 — tranche verticale de suivi (`TV`). Zip : `cours-genie-civil-P1-TV.zip`
- **Commande de contrôle** : `npm ci --ignore-scripts && npm run check`
- **EN ATTENTE DE VALIDATION** : la tranche verticale doit être validée par le lecteur
  **avant toute duplication** (forme, profondeur, ergonomie, chaîne de données, utilité de la 3D).
- **Prochain module une fois validée** : `D2` — Planification (WBS, cadences, CPM, Gantt, courbe en S,
  lissage), premier de l'ordre de livraison du palier 1 actif.
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

- **Livré** : `E1` (socle + page de démonstration), `TV` (tranche verticale de suivi).
- ▶ **actifs, non écrits** : A1, A2a, A5a, B5a-exec, B7b, B7c, C1, C2, C3, C4, C6, C7,
  D1, D2, D3, D4, D6, D7, M3D, REC, RC1
- ⏸ **suspendus** (§ 5.0.4) : A2b, A3, A4, A5b, B1, B2, B3, B5a-calc, B6, B6b, B7a, R5

**Palier 2** — 12 modules, 26 livraisons · non ouvert.
**Palier 3** — 8 modules, 14 livraisons · non ouvert.

Sommaire et fiches : `cadrage/05-sommaire.md`. Ordre de livraison : § 6 du même fichier.

## Ce que le socle livre (Étape 1, § 5.2)

Charte et impression (`assets/style.css`, `print.css`, contrastes AA) · SVG paramétrique
(`assets/svgkit.js`, 8 générateurs de figures sur 10 primitives) · 3D (`src/civil3d/`, bundle IIFE 763 ko : scène, orbite,
matériaux, étiquettes, coupe, éclaté, phasage 4D) · chaîne de build qui **échoue** sur variable
absente, légende incomplète, nombre normatif non balisé ou accident de gabarit · `calc/` avec
contre-calcul à deux voies, 3 étalonnages sur solution fermée et vérification `pint` des
5 bibliothèques · 13 contrôles `npm run check`, 14 tests de rendu, captures de toutes les figures ·
page de démonstration testée (`modules/00-demo-cage.html`).

## Grilles d'auto-évaluation § 7.2

| Livrable | Minimum 2 partout | Détail |
|---|---|---|
| Page de démonstration E1 | **tenu** (2 critères remontés de 1 et 0 après la passe) | `QA/grilles-72.md` |
| Tranche verticale TV | **tenu** (« l'exemple est vérifié » remonté de **1** à 3) | `QA/grilles-72.md` |

## Défauts et passe adversariale /devil (§ 12.2)

Portée par un **sous-agent distinct**, qui n'a pas lu le raisonnement de l'auteur et a recalculé les
valeurs clés à partir de `data/` seul.

| Étape | En construisant | À la passe /devil | Rapports |
|---|---|---|---|
| E1 — socle | 8 | **50** sur trois passes (6 bloquants, 20 majeurs, 24 mineurs) | `QA/E1-socle*.md` |
| TV — tranche verticale | 6 | **19** (4 bloquants, 9 majeurs, 6 mineurs) | `QA/TV-tranche-verticale.md`, `QA/TV-corrections-passe1.md` |

### Socle E1

**Trois passes** : 26 défauts (5 bloquants), puis 14 (1 bloquant, **3 canaris franchissaient les
11 contrôles**), puis 10 (0 bloquant). **Le § 12.2 est satisfait : zéro bloquant.**

**Ce que ces trois passes ont appris, et qui vaut pour tout le cours.** Deux fois, une correction
s'est retournée : le contrôle « dépôt propre » ajouté en passe 1 cassait la reprise du mode B sur un
clone neuf, et le paragraphe de coût ajouté pour combler une note faible réintroduisait un nombre
tapé à la main **et faux**. Une correction est un changement comme un autre : elle se relit. Et un
`replace` scripté dont l'ancre contient une faute **échoue en silence** : depuis, chacun porte un
`assert`.

**Canaris (§ 12.2, contrôle du relecteur).** 14 joués au total (12 sur le socle, 2 sur la TV), **tous
rouges aujourd'hui** — dont T2, qui doublait le planning en franchissant les douze contrôles avant
correction. Liste détaillée dans les rapports `QA/`.

### Tranche verticale TV — passe 1 corrigée, seconde passe à lancer

**Tous corrigés** ; journal et preuves : `QA/TV-corrections-passe1.md`. Quatre leçons pour la suite :
(1) **un corrigé chiffré ne se tape pas** — une division fausse (2,42 pour 2,00) s'est propagée
jusqu'à inverser la recommandation du module ; (2) **un accident de gabarit est une erreur publiée** —
`{{…::n0}}0 %` affichait 40 % pour 4, le build échoue désormais sur ce motif, sur une variable placée
dans une formule et sur un repère de rédaction (`build/tests/test-gabarit.mjs`) ; (3) **un moteur
juste dans son domaine d'usage n'est pas un moteur juste** — `cpm.py` rendait 1 pour une durée de 10
hors domaine, et son verdict accusait le bon algorithme (étalonnage porté à **9 cas**) ; (4) **une
alarme n'est pas un signal** — le recoupement sonnait en dirhams, mais les postes géométriques sont à
−0,63 % et −0,82 % : le seuil de 1 % n'appartient qu'à eux.

Le contrôle de part de main-d'œuvre **reste ouvert** (dette 10). **Reste à faire : relancer la passe**
(§ 12.2, « jusqu'à zéro bloquant »), en rejouant T2, T6 et les trois réseaux CPM.

## Valeurs V2 en attente de vérification par le lecteur

**Aucune dans le cours** (§ 5.0.6 ; `npm run check` échoue sur toute balise V2 tant que
`normes_disponibles = false`). Cadrage : `cadrage/registre-sources-cadrage.csv`, E0-S01 et E0-S06
restent « à vérifier ».

## Simplifications déclarées (§ R6)

| # | Simplification | Où |
|---|---|---|
| 1 | **Une scène 3D par vue**, initialisée à l'affichage et libérée en sortie, plafond de 4 contextes WebGL — et non un renderer unique à viewport/scissor. C'est la seconde option admise par le § 4.4 ; à revoir si une page devait porter plus de trois vues | `src/civil3d/scene.js` |
| 2 | Le contour du cadre est une **polyligne dense** (0,007 % sous la formule fermée), pas un arc exact | `src/civil3d/armatures.js` |
| 3 | Fiches-module des paliers 2 et 3 volontairement sobres, à revoir à l'ouverture de leur palier | `cadrage/05-sommaire.md` |
| 4 | `print.css` n'imprime pas la 3D : il imprime un substitut textuel. Vérifié par relecture du CSS, **pas** par un test automatique d'impression | `assets/print.css` |
| 5 | **Cadres sans crochets d'extrémité** : le métré est minorant d'environ 3 %. La longueur d'un crochet est une valeur constructive, interdite en § 5.0 | `data/demo-cage.json` → `conventions` |
| 6 | Le coffrage modélisé n'a **ni étaiement ni étais de reprise**, et le décoffrage est animé sans condition de résistance | page de démonstration |
| 7 | La vérification dimensionnelle des 5 bibliothèques est **déportée** dans `calc/verif_unites.py` plutôt qu'écrite dans chaque formule : si une formule change sans que le fichier suive, le contrôle ne le voit pas. Les tests recalculent par ailleurs les résultats à la main | `calc/verif_unites.py` |
| 8 | L'avancement réel de la courbe en S suit la **forme** de l'avancement prévu, calée sur le constat à la date d'arrêt : il n'y a pas de relevé jour par jour dans `data/` | `calc/cycle_plancher.py` |

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
| 8 | **Les tags git ne sont pas poussables** dans ce bac à sable (le proxy n'expose que `refs/heads/*`) : les tags de palier vivent dans le zip, pas sur GitHub | limite de l'environnement |
| 9 | Le module `TV` ne porte **aucun modèle 3D** : le phasage 3D appartient à C3. À réviser si le lecteur juge qu'il en manque un | après validation de la TV |
| 10 | **Le contrôle de part de main-d'œuvre reste hors fourchette** (5,2 % pour 15 à 30 %) : les cadences V3 sont probablement optimistes d'un facteur 2 à 3, et elles portent **toutes** les durées du cours | premiers attachements réels |
| 11 | Les chevauchements **texte contre trait** dans les figures ne sont pas détectés automatiquement : le test ne compare que texte contre texte. Trouvé à l'œil sur la figure 1, corrigé à la main | à outiller si le cas se reproduit |
| 12 | Le contre-calcul n° 1 du coffrage ne passe que sur **27 %** de la fourchette déclarée du rendement d'équipe : il mesure un choix d'auteur, pas une propriété des données. Publié comme tel | attachements réels |

## Données modifiées depuis la dernière livraison

Jeux figés en 1.0 inchangés dans leurs valeurs de conception. Corrigés depuis la passe /devil TV :
`materiel.tables_coffrantes_m2` (420 → 1 300, l'ancienne valeur contredisait le planning d'un facteur
2,5) et `materiel.etais` remplacé par une densité `etais_par_m2`, le total se déduisant du nombre de
zones étayées. Registres régénérés par le build (10 hypothèses V3).
Empreinte de `data/` : voir le pied de chaque module.

## Effort consommé (§ 13.2)

Étape 0 : 1 séance. Étape 1 : 2 séances (8 défauts en construisant, puis **50 sur trois passes**).
Étape 2 : 2 séances (6 défauts en construisant, 19 à la passe /devil, tous corrigés).
Hypothèse de budget : 2 séances par semaine, ~1,5 séance par livraison (V3, à confirmer).
**Constat de tendance** : la relecture adversariale coûte autant que l'écriture. C'est le prix du
§ 12.2, et les quatre bloquants de la TV montrent qu'il est justifié.
