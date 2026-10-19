# STATE — avancement du cours

Dernière mise à jour : **16/10/2026** · Étape en cours : **2 — tranche verticale, corrigée après la passe /devil n° 1**
Mode d'exécution : **B** (chat avec bac à sable éphémère, § 12.5)
Phase : **§ 5.0 — SANS CALCULS NORMATIFS** (`normes_disponibles = false`)

## Reprise (mode B — à lire en premier à chaque séance)

- **Dernier livrable** : Étape 2 — tranche verticale (`TV`). Zip : `cours-genie-civil-P1-TV.zip`
- **Commande de contrôle** : `npm ci --ignore-scripts && npm run check`
- **EN ATTENTE DE VALIDATION** : la TV doit être validée **avant toute duplication** (forme,
  profondeur, ergonomie, chaîne de données, utilité de la 3D) — et une **passe 3** reste à lancer.
- **Prochain module une fois validée** : `D2` — Planification. Son moteur est déjà écrit et testé
  hors dépôt (quantités, durées par familles, CPM, fenêtres de consignation, lissage, courbe en S).
- **Règle absolue** : aucun chiffre repris de mémoire. Seul le zip (ou la branche git) fait foi.

## Données figées

| Jeu de données | Version | État |
|---|---|---|
| `data/projet-gare.json` | **1.0** | **FIGÉ** le 15/10/2026 · commit `ad792eb` · tag local `donnees-gare-v1.0` · site S1 (région de Marrakech) |
| `data/projet-r5.json` | **1.0** | **FIGÉ** — cas secondaire léger |
| `data/referentiels.json` | **1.0** | **FIGÉ** — option M (béton, séisme) + E 1re génération (acier) |
| `data/demo-cage.json` | 1.0 | paramètres de la page de démonstration du socle |

## Statut des modules

**Palier 1 — 35 modules, 50 livraisons.** ▶ 23 / 30 actifs · ⏸ 12 / 20 suspendus (§ 5.0.4).

- **Livré** : `E1` (socle + page de démonstration), `TV` (tranche verticale de suivi).
- ▶ **actifs, non écrits** : A1, A2a, A5a, B5a-exec, B7b, B7c, C1, C2, C3, C4, C6, C7,
  D1, D2, D3, D4, D6, D7, M3D, REC, RC1
- ⏸ **suspendus** (§ 5.0.4) : A2b, A3, A4, A5b, B1, B2, B3, B5a-calc, B6, B6b, B7a, R5

**Palier 2** — 12 modules, 26 livraisons · **Palier 3** — 8 modules, 14 livraisons · non ouverts.
Sommaire, fiches et ordre de livraison : `cadrage/05-sommaire.md`.

## Ce que le socle livre (Étape 1, § 5.2)

Charte et impression (contrastes AA) · SVG paramétrique (`assets/svgkit.js`, 9 générateurs de
figures) · 3D (`src/civil3d/`, bundle IIFE 765 ko : scène, orbite, matériaux, étiquettes, coupe,
éclaté, phasage 4D) · build qui **échoue** sur variable absente, légende incomplète, nombre normatif
non balisé ou accident de gabarit · `calc/` : contre-calcul à deux voies, 3 étalonnages sur solution
fermée, `pint` sur les 5 bibliothèques · **15 contrôles** `npm run check`, 14 tests de rendu,
captures de toutes les figures · page de démonstration testée.

## Grilles d'auto-évaluation § 7.2

Socle E1 : **minimum 2 partout tenu**. TV : tenu après la passe 1, **mis en cause par la passe 2**
(« l'exemple est vérifié » noté 1 par le relecteur), à renoter après la passe 3. Détail et
justifications : `QA/grilles-72.md`.

## Défauts et passe adversariale /devil (§ 12.2)

Portée par un **sous-agent distinct**, qui n'a pas lu le raisonnement de l'auteur et a recalculé les
valeurs clés à partir de `data/` seul.

| Étape | En construisant | À la passe /devil | Rapports |
|---|---|---|---|
| E1 — socle | 8 | **50** sur trois passes (6 bloquants, 20 majeurs, 24 mineurs) | `QA/E1-socle*.md` |
| TV — tranche verticale | 6 | **19** (4 bloquants, 9 majeurs, 6 mineurs) | `QA/TV-tranche-verticale.md`, `QA/TV-corrections-passe1.md` |

### Socle E1

**Trois passes** : 26 défauts (5 bloquants), puis 14 (1 bloquant, **3 canaris franchissaient les
11 contrôles**), puis 10 (0 bloquant). **Zéro bloquant à l'arrivée.** Leçon : une correction est un
changement comme un autre, elle se relit — deux fois elle s'est retournée. **Canaris** : 14 sur le
socle et la TV, plus 11 inventés par les relecteurs ; **tous rouges aujourd'hui**.

### Tranche verticale TV — deux passes, 44 défauts, tous corrigés

| Passe | Verdict | Ce qu'elle a appris |
|---|---|---|
| 1 | 19 défauts — **4 bloquants** | un corrigé chiffré ne se tape pas ; un accident de gabarit est une erreur publiée ; un moteur juste dans son domaine d'usage n'est pas un moteur juste |
| 2 | 25 défauts — **3 bloquants**, 12 majeurs, 10 mineurs | **aucun des 25 n'était vu par les 14 contrôles** ; 3 corrections de la passe 1 ne tenaient pas, 2 avaient créé un défaut neuf |
| 3 | 26 défauts — **2 bloquants**, 14 majeurs, 10 mineurs | le modèle d'avancement était faux : **à 60 % du cycle, le béton n'est pas coulé** ; et la règle de cadence déguisait une marge en contrainte |

Journaux : `QA/TV-corrections-passe1.md`, `QA/TV-tranche-verticale-passe2.md`.

**Les sept bloquants des trois passes se ressemblent : des modèles faux sous une arithmétique
juste.** Le dernier est le plus profond. L'avancement d'une zone était réparti **au prorata
uniforme** : 60 % du béton, 60 % de l'acier, 60 % du coffrage. Or à 60 % du cycle, le réseau du
module dit que **le bétonnage n'a pas commencé** et que le coffrage est **entièrement posé**. Le
module publiait 59 m³ pour une zone où rien n'est coulé, et son contrôle « qui fait foi » comparait
deux calculs partageant cette hypothèse. Un avancement se **dérive du réseau**, poste par poste.

La règle de cadence a été refondée dans la foulée sur les **ressources** : borne = max(équipe la
plus chargée ; occupation cumulée de la grue), plus une **marge déclarée**. L'ancien « + bétonnage »
n'était justifié par aucun modèle — c'était cette marge, déguisée en contrainte. D'où l'exercice 3 :
renforcer les équipes ne suffit pas, c'est la **grue** qui finit par borner.

**La leçon vaut pour les cinquante modules à venir** : les contrôles vérifiaient que les nombres se
suivent, pas que le **modèle** dise ce qu'il prétend. Depuis, toute grandeur décrivant l'état du
chantier à une date est **dérivée du réseau** et un test refait la dérivation ; toute V3 de `data/`
est registrée et vérifiée **dans sa propre fourchette** ; l'affectation des équipes aux tâches est
contrôlée nommément. Le contrôle de part de main-d'œuvre **reste ouvert** (dette 10).

## Valeurs V2 en attente de vérification par le lecteur

**Aucune** (§ 5.0.6 ; `npm run check` échoue sur toute balise V2 tant que
`normes_disponibles = false`). Cadrage : `cadrage/registre-sources-cadrage.csv`, E0-S01 et E0-S06 « à vérifier ».

## Simplifications déclarées (§ R6)

| # | Simplification | Où |
|---|---|---|
| 1 | **Une scène 3D par vue** (seconde option du § 4.4), plafond de 4 contextes WebGL, et non un renderer unique à viewport/scissor | `src/civil3d/scene.js` |
| 2 | Le contour du cadre est une **polyligne dense** (0,007 % sous la formule fermée), pas un arc exact | `src/civil3d/armatures.js` |
| 3 | Fiches-module des paliers 2 et 3 sobres, à revoir à l'ouverture du palier | `cadrage/05-sommaire.md` |
| 4 | `print.css` imprime un substitut textuel de la 3D ; vérifié par relecture, **pas** par un test | `assets/print.css` |
| 5 | **Cadres sans crochets** : métré minorant d'environ 3 % (valeur constructive interdite en § 5.0) | `data/demo-cage.json` |
| 6 | Coffrage modélisé **sans étaiement**, décoffrage animé sans condition de résistance | page de démonstration |
| 7 | Vérification dimensionnelle **déportée** dans un fichier : si une formule change sans qu'il suive, le contrôle ne le voit pas | `calc/verif_unites.py` |
| 8 | Un seul relevé d'avancement dans `data/` : le constat est publié comme un point, pas comme une courbe | `calc/cycle_plancher.py` |
| 9 | L'étalonnage de la valeur acquise confronte les formules à un cas posé d'avance, mais n'appelle pas `valeur_acquise()` : il garde l'arithmétique, pas le branchement | `calc/etalonnage/plancher_cas_ferme.py` |

## Dette

| # | Dette | Échéance |
|---|---|---|
| 1 | 12 modules du palier 1 inaccessibles faute de documents normatifs | levée du § 5.0 |
| 2 | Aucun bordereau : tout le volet économique reste V3 | question 7, sans réponse |
| 3 | Dates du palier 1 : **hypothèse V3** (fin du P1 actif au 15/03/2027), non confirmée | § 5.5 |
| 4 | Logiciel aux éléments finis du lecteur inconnu — nécessaire avant B6b (⏸) | avant B6b |
| 5 | Référentiel ferroviaire non identifié (quais, gabarits, caténaire) | CPS du marché |
| 6 | Contrôle d'impression visuel, non automatisé | à outiller |
| 7 | Bundle 3D de 765 ko, hors budget par module | à surveiller |
| 8 | **Les tags git ne sont pas poussables** dans ce bac à sable (le proxy n'expose que `refs/heads/*`) : les tags de palier vivent dans le zip, pas sur GitHub | limite de l'environnement |
| 9 | `TV` sans modèle 3D (le phasage appartient à C3) — à réviser si vous jugez qu'il en manque un | après validation |
| 10 | **Le contrôle de part de main-d'œuvre reste hors fourchette** (5,2 % pour 15 à 30 %) : les cadences V3 sont probablement optimistes d'un facteur 2 à 3, et elles portent **toutes** les durées du cours | premiers attachements réels |
| 11 | Chevauchements **texte contre trait** non détectés : le test ne compare que texte contre texte | à outiller |
| 12 | Le contre-calcul n° 1 ne passe que sur **27 %** de la fourchette déclarée : publié comme tel | attachements réels |
| 13 | Aucun contrôle ne vérifie qu'une figure **montre ce qu'elle prétend montrer** : les 3 bloquants de la passe 2 ont franchi 14 contrôles verts | à outiller, et c'est la dette la plus lourde |

## Données modifiées depuis la dernière livraison

Jeux figés en 1.0, valeurs de conception inchangées. Corrigé par les passes /devil : le parc de
tables (420 → 1 300, l'ancienne valeur contredisait le planning), les étais (densité au m² + durée
de maintien), `suivi.quantites_relevees` (refaits sur l'état **physique** et non sur un prorata),
`materiel.nb_grues`, et le bloc `cycle_zone` — cure, décoffrage, point d'arrêt, deux taux de
recouvrement, marge de rotation, tâches servies par la grue, effectif par tâche — qui vivait en dur
dans `calc/`. **27 hypothèses V3 registrées**, 20 sur 20 couvertes.

## Effort consommé (§ 13.2)

Étape 0 : 1 séance. Étape 1 : 2 séances (8 défauts, puis **50 sur trois passes**). Étape 2 :
3 séances (6 défauts en construisant, **70 sur trois passes**, tous corrigés).
Hypothèse de budget : 2 séances/semaine, ~1,5 séance par livraison (V3, à confirmer).
**Constat** : la relecture adversariale coûte autant que l'écriture — et les 7 bloquants de la TV,
dont aucun n'était vu par les contrôles, montrent qu'il n'y a pas d'économie à faire dessus.
