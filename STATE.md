# STATE — avancement du cours

Dernière mise à jour : **26/10/2026** · Étape : **3 — paliers, programme recentré au 31/10**
Mode d'exécution : **B** (chat avec bac à sable éphémère, § 12.5)
Phase : **§ 5.0 — SANS CALCULS NORMATIFS** (`normes_disponibles = false`)

## Reprise (mode B — à lire en premier à chaque séance)

- **Dernier livrable** : `C3` et `D4`, passes /devil faites et **bloquants corrigés**. Zip :
  `cours-genie-civil-P1-C3-D4.zip`
- **Commande de contrôle** : `npm ci --ignore-scripts && npm run check`
- **EN ATTENTE DE VALIDATION** : la TV (forme, profondeur, utilité de la 3D). Les cinq relecteurs
  ont tous jugé l'absence de 3D justifiée.
- **Prochain module** : `B3e` — Béton armé en exécution (lire un plan, métrer, contrôler).
- **Programme recentré au 31/10/2026** : `cadrage/07-programme-31-10.md` (décisions D-033, D-034).
- **Règle absolue** : aucun chiffre repris de mémoire. Seul le zip (ou la branche git) fait foi.

## Données figées

| Jeu de données | Version | État |
|---|---|---|
| `data/projet-gare.json` | **1.0** | **FIGÉ** le 15/10/2026 · commit `ad792eb` · tag local `donnees-gare-v1.0` · site S1 (région de Marrakech) |
| `data/projet-r5.json` | **1.0** | **FIGÉ** — cas secondaire léger |
| `data/referentiels.json` | **1.0** | **FIGÉ** — option M (béton, séisme) + E 1re génération (acier) |
| `data/demo-cage.json` | 1.0 | paramètres de la page de démonstration du socle |

## Statut des modules

**Périmètre recentré (D-033)** : paliers 2 et 3 supprimés sauf ce qui touche une gare.
**24 livraisons**, dont **6 faites** et 16 au programme du 31/10 (`cadrage/07-programme-31-10.md`).

- **Livré** : `E1` (socle), `TV` (tranche verticale), `D2` (planification, 32 défauts, 8 bloquants
  — D-035), `D1` (métrés et prix, 28 défauts, 7 bloquants corrigés), `D4` (suivi),
  `C3` (gros œuvre, 33 défauts, 6 bloquants — D-040, D-041), `D4` (suivi et contrôle, 32 défauts,
  8 bloquants — D-042). **Toutes les passes sont faites**, tous les bloquants corrigés.
- ▶ **actifs, non écrits** : A1, A2a, A5a, B5a-exec, B7b, B7c, C1, C2, C3, C4, C6, C7,
  D1, D2, D3, D4, D6, D7, M3D, REC, RC1
- ⏸ **suspendus** (§ 5.0.4) : A2b, A3, A4, A5b, B1, B2, B3, B5a-calc, B6, B6b, B7a, R5

Fiches-module : `cadrage/05-sommaire.md` (périmètre d'origine, conservé pour mémoire).
Ordre de livraison **en vigueur** : `cadrage/07-programme-31-10.md`.

## Ce que le socle livre (Étape 1, § 5.2)

Charte et impression (contrastes AA) · SVG paramétrique (`assets/svgkit.js`, 12 générateurs, chacun
déclarant ses options — le build **échoue** sur une option inconnue) · 3D (`src/civil3d/`, bundle
IIFE 765 ko) · build qui échoue sur variable absente, légende incomplète, nombre normatif non balisé
ou accident de gabarit · `calc/` : contre-calcul à deux voies, étalonnages sur solution fermée,
`pint` · **16 contrôles** `npm run check`, captures de toutes les figures.

## Grilles d'auto-évaluation § 7.2

E1, TV, D2, D1 : **minimum 2 partout** après correction des bloquants. Détail : `QA/grilles-72.md`.

## Défauts et passe adversariale /devil (§ 12.2)

Portée par un **sous-agent distinct** qui n'a pas lu le raisonnement de l'auteur et recalcule les
valeurs clés depuis `data/` seul. E1 : 50 (3 passes) · TV : 117 (5 passes) · D2 : 32 · D1 : 28 ·
C3 : 33 · D4 : 32 (une passe chacun, D-034). **Bloquants : 15 · 8 · 7 · 6 · 8, tous corrigés.**
Détail de chaque défaut, de sa preuve et de la suite donnée : `QA/`.

**Les six familles qui reviennent**, et ce sont elles qu'il faut chercher dans les modules suivants :
(1) une grandeur d'état **saisie** au lieu d'être dérivée ; (2) un paramètre déclaré, publié, et que
**rien ne lit** (D2-B1, D1-B6, C3-M8) ; (3) un ratio ou un indice lu **hors de son domaine**, voire
sur un domaine vide (D1, D4-B5, D-037, D-042) ; (4) une figure ou une légende qui ne montre pas la
série annoncée ; (5) deux modules qui recalculent la même grandeur et en publient deux valeurs
(D1-M1, C3-B3, C3-B5, D-039) ; (6) une conclusion **déduite** d'une définition piégeuse — marge libre
contre marge totale — au lieu d'être mesurée (C3-B1, D-040).

**Ce qui les trouve** : une contre-expertise à l'aveugle, deux nombres du même fichier de sortie, et
des captures regardées. **Jamais un test** — les contrôles étaient verts avant chaque passe.

**Deux fautes de méthode à ne pas reproduire.** D4 a modifié les fichiers de D1 pendant sa passe
adversariale : un livrable en relecture est figé. Et un test de C3 épinglait la **conclusion
narrative** du module (« l'optimum n'est ni le plus petit ni le plus grand ») au lieu de sa règle :
corrigé le bloquant, le test rougissait et poussait à déplacer les données. Un test vérifie une
règle, jamais un résultat raconté.

**La règle qui en sort** : toute grandeur d'état est **dérivée** et un test refait la dérivation ;
tout paramètre déclaré est **relu dans le résultat qu'il engendre** ; tout **verdict publié est une
sortie de `calc/`** ; toute V3 est registrée et vérifiée dans sa fourchette ; un module à risque
porte ses dispositions de sécurité (§ 3.4) ; chaque contrôle rendant un verdict porte son canari.
**Canaris** : 14 sur E1 et TV, 11 inventés par les relecteurs, 5 par D2, 7 par D1, 6 par C3, 7 par
D4 ; tous rouges.

**Dette déclarée de la TV** : scalaires V3 sans fourchette hors registre · deux bibliothèques hors
vérification dimensionnelle · glossaire S7 absent · contrôle de sécurité qui ne cherche qu'un mot.

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
| 9 | Le 16ᵉ contrôle de sécurité ne cherche qu'un mot : une section S7c vidée de sa substance mais contenant « sécurité » resterait verte | `build/check.mjs` |

## Dette

| # | Dette | Échéance |
|---|---|---|
| 1 | 12 modules du palier 1 inaccessibles faute de documents normatifs | levée du § 5.0 |
| 2 | Aucun bordereau : tout le volet économique reste V3 | question 7, sans réponse |
| 3 | Dates du palier 1 : **hypothèse V3** (fin du P1 actif au 15/03/2027), non confirmée | § 5.5 |
| 4 | Logiciel aux éléments finis du lecteur inconnu — nécessaire avant B6b (⏸) | avant B6b |
| 5 | Référentiel ferroviaire non identifié (quais, gabarits, caténaire) | CPS du marché |
| 7 | Bundle 3D de 765 ko, hors budget par module | à surveiller |
| 8 | **Les tags git ne sont pas poussables** dans ce bac à sable (le proxy n'expose que `refs/heads/*`) : les tags de palier vivent dans le zip, pas sur GitHub | limite de l'environnement |
| 9 | `TV` sans modèle 3D (le phasage appartient à C3) — à réviser si vous jugez qu'il en manque un | après validation |
| 10 | **Part de main-d'œuvre hors fourchette.** D1 l'a instruite : la base du ratio était fausse (bordereau entier au lieu du béton armé décomposé), **et** les cadences sont optimistes — facteur **×1,92** pondéré par le travail, chemin indépendant. Le soupçon « 2 à 3 » est confirmé dans son sens, **revu à la baisse dans son ampleur**. **Chiffrée, non soldée** | attachements réels |
| 11 | Chevauchements **texte contre trait** non détectés : le test ne compare que texte contre texte | à outiller |
| 12 | Le contre-calcul n° 1 ne passe que sur **27 %** de la fourchette déclarée : publié comme tel | attachements réels |
| 13 | Aucun contrôle ne vérifie qu'une figure **montre ce qu'elle prétend montrer** : 3 bloquants de la TV et 6 de D2 ont franchi tous les contrôles verts | à outiller, et c'est la dette la plus lourde |
| 17 | **C3, non corrigés** : le `floor` du parc ne mord sur aucune ligne du tableau (m5) · cure de 2 j insensible sur sa fourchette, non publiée (m6) · loyer et montage sans leurs bornes dans le tableau (m7) · loyer sans battement de livraison ni repli : **borne basse** (m8) · deux durées du plancher coexistent dans `data/` (m10) | avant la revue de palier |
| 18 | **D4, non corrigés** : les 15 majeurs et 9 mineurs que la réécriture de S3c, S4c, de l'exercice 2 et de la fiche mémo n'a pas emportés (détail : `QA/D4-passe1.md`) | avant la revue de palier |
| 16 | **D1, non corrigés** (D-034) : figure 4 écrite en dur dans `figures()` au lieu d'être générée depuis `data/` (M6) · un seul canari pour cinq verdicts (M9) · nombres encore écrits à la main (M10) · dix mineurs. Et une **simplification déclarée** : tous les totaux de D1 sont calculés **sans** la ligne de divers calibrée (28,7 %), donc ce sont des bornes basses | avant la revue de palier |
| 15 | **D1, corrigé en écrivant D4** : l'avancement déclaré de la situation était saisi à la main dans `data/` et décrivait un état de chantier du 2ᵉ mois pour une situation annoncée au 7ᵉ. Il est désormais dérivé du réseau (`calc/etat.py`), partagé par D1 et D4 | fait, D-039 |
| 14 | **D2, non corrigés** (D-034) : réseau, lots et `21,7` en dur dans `calc/` au lieu de `data/` (M1) · 9 effectifs posés sans forme `{valeur, fourchette}` (M3) · levier « protection de voie » modélisé par un contournement (M5) · nombres encore écrits à la main (M10) · quantités calculées jamais publiées (m1) · axe de la ligne d'équilibre (m2, m3) · deux libellés plus larges que leur métré (m5) · pas de double lecture MOE (m6) · effet de seuil des fenêtres non commenté (m9, m10) | avant la revue de palier |

## Données modifiées depuis la dernière livraison

Jeux figés en 1.0, valeurs de conception inchangées. Corrigé par les passes /devil : le parc de
tables (420 → 1 300, l'ancienne valeur contredisait le planning), les étais (densité au m² + durée
de maintien), `suivi.quantites_relevees` (refaits sur l'état **physique** et non sur un prorata),
`materiel.nb_grues`, et le bloc `cycle_zone` — cure, décoffrage, point d'arrêt, deux taux de
recouvrement, marge de rotation, tâches servies par la grue, effectif par tâche — qui vivait en dur
dans `calc/`. **27 hypothèses V3 registrées**, 20 sur 20 couvertes.

## Effort consommé (§ 13.2)

**12 séances** : Étape 0 = 1 · Étape 1 = 2 · Étape 2 = 4 · D2, D1, D4, C3 = 1 chacun, plus 1 pour
les passes et corrections de C3 et D4.
**Avancement sur le programme du 31/10** : **6 livraisons sur 18**, toutes passées au /devil. À la
cadence constatée, il en reste 4 à 6 atteignables sur les 12 annoncées, et non 12. **Ordre de priorité retenu** : B3e, B7c, C7, REC ; C1 et C4+B7b sont les
premiers coupés. C'est dit au lecteur, pas découvert le 31.
