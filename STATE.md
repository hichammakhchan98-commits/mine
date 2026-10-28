# STATE — avancement du cours

Dernière mise à jour : **26/10/2026** · Étape : **3 — paliers, programme recentré au 31/10**
Mode d'exécution : **B** (chat avec bac à sable éphémère, § 12.5)
Phase : **§ 5.0 — SANS CALCULS NORMATIFS** (`normes_disponibles = false`)

## Reprise (mode B — à lire en premier à chaque séance)

- **Dernier livrable** : `RC1` — revue critique du palier 1. Zip : `cours-genie-civil-P1-RC1.zip`
- **Toutes les passes /devil sont faites**, tous les bloquants corrigés. C7 : **45 défauts,
  13 bloquants, 22 majeurs — livraison refusée en première passe**, tous traités (D-049 à D-052).
- **Commande de contrôle** : `npm ci --ignore-scripts && npm run check`
- **EN ATTENTE DE VALIDATION** : la TV (forme, profondeur, utilité de la 3D). Les cinq relecteurs
  ont tous jugé l'absence de 3D justifiée.
- **PALIER 1 TERMINÉ.** En attente du **go/no-go du lecteur** (§ 5.5) avant toute suite.
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
**24 livraisons**, dont **9 faites** et 16 au programme du 31/10 (`cadrage/07-programme-31-10.md`).

- **Livré (9)** : `E1` (socle) · `TV` (tranche verticale) · `D2` (planification, 32 défauts,
  8 bloquants — D-035) · `D1` (métrés et prix, 28 défauts, 7 bloquants) · `D4` (suivi et contrôle,
  32 défauts, 8 bloquants — D-042) · `C3` (gros œuvre, 33 défauts, 6 bloquants — D-040, D-041) ·
  `B3e` (béton armé en exécution, 36 défauts, 11 bloquants dont **trois erreurs de modèle
  physique**) · `B7c` (bâtiments ferroviaires, 39 défauts, 11 bloquants dont le **changement
  d'unité silencieux** — D-045 à D-048) · `C7` (qualité et HSE, 45 défauts, 13 bloquants —
  D-049 à D-052) · `REC` (réception, DOE, garanties, 28 défauts dont 8 bloquants — D-054 à
  D-057) · `RC1` (revue critique du palier, § 5.5). Toutes les passes sont faites, tous les
  bloquants et majeurs corrigés.
- ▶ **actifs, non écrits (13)** : A1, A2a, A5a, B5a-exec, B7b, C1, C2, C4, C6, D3, D6, D7, M3D
- ⏸ **suspendus** (§ 5.0.4) : A2b, A3, A4, A5b, B1, B2, B3, B5a-calc, B6, B6b, B7a, R5

Fiches-module : `cadrage/05-sommaire.md` (périmètre d'origine, conservé pour mémoire).
Ordre de livraison **en vigueur** : `cadrage/07-programme-31-10.md`.

## Ce que le socle livre (Étape 1, § 5.2)

Charte et impression (AA) · SVG paramétrique (`assets/svgkit.js`, 12 générateurs déclarant leurs
options) · 3D (bundle IIFE 765 ko) · build qui échoue sur variable absente, légende incomplète,
nombre normatif non balisé, option inconnue ou accident de gabarit · `calc/` : contre-calcul à deux
voies, étalonnages sur solution fermée, `pint` · **16 contrôles** `npm run check`, captures de
toutes les figures.

## Grilles d'auto-évaluation § 7.2

E1, TV, D2, D1 : **minimum 2 partout** après correction des bloquants. Détail : `QA/grilles-72.md`.

## Défauts et passe adversariale /devil (§ 12.2)

Portée par un **sous-agent distinct** qui n'a pas lu le raisonnement de l'auteur et recalcule les
valeurs clés depuis `data/` seul. E1 : 50 (3 passes) · TV : 117 (5 passes) · D2 : 32 · D1 : 28 ·
C3 : 33 · D4 : 32 · B3e : 36 · B7c : 33 (une passe chacun, D-034).
**Bloquants : 15 · 8 · 7 · 6 · 8 · 11 · 11, tous corrigés.**
Détail de chaque défaut, de sa preuve et de la suite donnée : `QA/`.

**La huitième famille, trouvée par B7c, est la plus insidieuse : le CHANGEMENT D'UNITÉ SILENCIEUX.**
Une grandeur garde son nom (« jours ») et change de contenu (des plages de 6 h). Aucune vérification
dimensionnelle ne le voit — `pint` lit des heures des deux côtés. Le seul contrôle qui l'attrape est
celui que personne n'avait écrit : **deux modules qui chiffrent la même tâche doivent trouver les
mêmes heures**. Il est en place, et il a exposé un second écart du même genre dès sa première
exécution.

**La septième, découverte par B3e : l'erreur de MODÈLE PHYSIQUE.** Une formule de recouvrement qui ne couvre pas l'ouvrage, une nappe qui laisse 18 m² de
dalle nue, un plan qui met l'acier du mauvais côté de la poutre. Aucun contrôle de cohérence ne les
voit : il faut refaire la géométrie. Les chercher d'abord dans tout module qui pose une géométrie.

**Les six autres familles** : (1) une grandeur d'état **saisie** au lieu d'être dérivée ; (2) un
paramètre déclaré, publié, que **rien ne lit** ; (3) un ratio ou un indice lu **hors de son
domaine**, voire sur un domaine vide (D-037, D-042) ; (4) une figure ou une légende qui ne montre
pas la série annoncée ; (5) deux modules qui recalculent la même grandeur (D-039) ; (6) une
conclusion **déduite** d'une définition piégeuse au lieu d'être mesurée (D-040).

**Ce qui les trouve** : une contre-expertise à l'aveugle, deux nombres du même fichier de sortie, et
des captures regardées. **Jamais un test** — les contrôles étaient verts avant chaque passe.

**Deux fautes de méthode à ne pas reproduire.** D4 a modifié les fichiers de D1 pendant sa passe :
un livrable en relecture est figé. Et deux fois — C3 puis B3e — un test épinglait la **conclusion
narrative** au lieu de la règle. Un test vérifie une règle, jamais un résultat raconté (D-041,
D-043).

**La règle qui en sort** : toute grandeur d'état est **dérivée** et un test refait la dérivation ;
tout paramètre déclaré est **relu dans le résultat qu'il engendre** ; tout **verdict publié est une
sortie de `calc/`** ; toute V3 est registrée et vérifiée dans sa fourchette ; deux modules qui
chiffrent la même tâche **trouvent les mêmes heures** ; chaque contrôle rendant un verdict porte son
canari. **73 canaris, tous rouges** — et deux d'entre eux ont trouvé seuls une erreur que la passe
n'avait pas vue : un canari utile ne confirme pas, il cherche.

**Dette TV** : scalaires V3 hors registre · deux bibliothèques hors vérification dimensionnelle ·
glossaire S7 absent · contrôle de sécurité qui ne cherche qu'un mot.
**Valeurs V2 en attente** : aucune (§ 5.0.6, le build échoue sur toute balise V2).

## Simplifications déclarées (§ R6)

Neuf, inchangées depuis C3, détaillées dans chaque module et dans git : une scène 3D par vue · contour de cadre en polyligne · fiches P2/P3 sobres · substitut textuel de la 3D à l'impression · cadres sans crochets (métré minorant, 0,08 % du total) · coffrage sans étaiement en démonstration · vérification dimensionnelle déportée · un seul relevé d'avancement dans `data/` · le contrôle de sécurité ne cherche qu'un mot.

## Dette

| # | Dette | Échéance |
|---|---|---|
| 1-2 | 12 modules inaccessibles faute de normes · aucun bordereau fourni, tout l'économique reste V3 | levée du § 5.0 |
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
| 23 | **D1 et D2 divergent de ×2,1 sur les heures du plancher de mezzanine** (3 219 contre 6 880 h) : D1 compte les heures productives à la cadence, D2 tout l'effectif de zone présent pendant tout le cycle. Écart antérieur, exposé par le nouveau contrôle croisé, déclaré comme exception nommée dans `test_prix.py` | avant la revue de palier |
| 21 | **Le chantier dure désormais 600 j ouvrés** (fin 2029-04-23) au lieu de 363, parce que B7c a corrigé la tâche sous consignation. D1 et D4 ont suivi par le build ; leurs **textes** n'ont pas été relus ligne à ligne avec les nouvelles dates (D-045, choix du lecteur : laisser le build propager) | avant la revue de palier |
| 22 | **Flake de rendu** : les deux contrôles 3D de `00-demo-cage` échouent par intermittence sur un avertissement du moteur WebGL logiciel, et passent au rejeu. Ce n'est pas un défaut du cours, c'est l'environnement — mais un contrôle qui échoue au hasard finit par ne plus être lu | à outiller |
| 26 | **D1 et REC divergent sur la date de restitution de la retenue de garantie.** D1 écrit qu'elle « ne revient qu'après la réception » et bâtit sa courbe de trésorerie là-dessus ; REC dit qu'elle est immobilisée jusqu'à une date que le marché fixe (⏸), postérieure. REC ne contredit plus D1 frontalement, mais le besoin de trésorerie publié par D1 est optimiste de la durée de la garantie | revue de palier |
| 25 | **La date de fin publiée par D2 ne comprend pas une réception décomposée.** REC mesure, en rejouant le réseau, que les deux tâches de fin du planning demandent 16 jours ouvrés de plus que ce qu'elles portent : ESSA 15 j prévus pour 25 demandés, RECE 10 pour 16. Soit **16 jours de fin**, de 260 000 à 2 046 000 MAD selon que le chantier est ou non sous pénalités. Les deux durées sont des décisions de ce cours, posées à deux moments (D-055) ; l'écart n'est pas reporté dans `data/` tant que le lecteur n'a pas tranché | revue de palier |
| 24 | **C7, non corrigés** : la pondération de nuit (coefficient 1,8) et l'abattement de cadence de nuit de B7c (30 %) restent deux coefficients distincts pour une même cause — leurs notes se croisent désormais, mais aucune n'est dérivée de l'autre · 4 mineurs de forme (détail : `QA/C7-passe1.md`) | avant la revue de palier |
| 20 | **B3e, non corrigés** : les 17 majeurs et 8 mineurs que la correction des bloquants n'a pas emportés — dont ~20 nombres techniques encore écrits à la main (§ 4.3) et trois listes fermées de points de contrôle avant coulage (C3 en a deux, B3e une) sans renvoi croisé (D-039 non appliqué entre les deux modules). Détail : `QA/B3e-passe1.md` | avant la revue de palier |
| 19 | **B3e** : le plan de ferraillage est **fictif et calibré** sur les ratios V3, non dimensionné — une première version posée à vue pesait 35 à 43 % de moins. Le module le dit quatre fois ; il reste qu'aucune de ses sections n'est justifiée. Levée : module **B3c** à l'arrivée du BAEL | levée du § 5.0 |
| 18 | **D4, non corrigés** : les 15 majeurs et 9 mineurs que la réécriture de S3c, S4c, de l'exercice 2 et de la fiche mémo n'a pas emportés (détail : `QA/D4-passe1.md`) | avant la revue de palier |
| 16 | **D1, non corrigés** (D-034) : figure 4 écrite en dur dans `figures()` au lieu d'être générée depuis `data/` (M6) · un seul canari pour cinq verdicts (M9) · nombres encore écrits à la main (M10) · dix mineurs. Et une **simplification déclarée** : tous les totaux de D1 sont calculés **sans** la ligne de divers calibrée (28,7 %), donc ce sont des bornes basses | avant la revue de palier |
| 15 | **D1, corrigé en écrivant D4** : l'avancement déclaré de la situation était saisi à la main dans `data/` et décrivait un état de chantier du 2ᵉ mois pour une situation annoncée au 7ᵉ. Il est désormais dérivé du réseau (`calc/etat.py`), partagé par D1 et D4 | fait, D-039 |
| 14 | **D2, non corrigés** (D-034) : réseau, lots et `21,7` en dur dans `calc/` au lieu de `data/` (M1) · 9 effectifs posés sans forme `{valeur, fourchette}` (M3) · levier « protection de voie » modélisé par un contournement (M5) · nombres encore écrits à la main (M10) · quantités calculées jamais publiées (m1) · axe de la ligne d'équilibre (m2, m3) · deux libellés plus larges que leur métré (m5) · pas de double lecture MOE (m6) · effet de seuil des fenêtres non commenté (m9, m10) | avant la revue de palier |

## Données modifiées depuis la dernière livraison

Jeux figés en 1.0, valeurs de conception inchangées. Ajouts : le bloc `armatures` (plan de
ferraillage fictif calibré, B3e) et le bloc `ferroviaire` (plages de consignation, interfaces,
B7c). Corrigé par les passes : parc de tables, étais, `suivi.quantites_relevees`, `materiel`,
`cycle_zone`, portées des nappes, segments de cadres, base des ratios d'acier. **176 hypothèses V3
registrées**, 189 sur 189 couvertes. Ajouts de C7 : l'heure de contrôle d'un cadre (140 MAD/h, distincte de l'heure de compagnon), les heures annuelles d'un compagnon, les cinq ratios de déchets désormais tous balisés ; le plan de contrôle porte l'exécutant ET le visa, les points d'arrêt avec leur durée, et le renvoi vers les plans de C3 et de B3e. Détail dans git et dans `QA/`.

## Effort consommé (§ 13.2)

**19 séances** : Étape 0 = 1 · Étape 1 = 2 · Étape 2 = 4 · D2, D1, D4, C3, B3e, B7c, C7, REC, RC1 = 1 chacun, plus 3 pour les passes et corrections de C3, D4, B7c et C7.
**Avancement sur le programme du 31/10** : **11 livraisons sur 18**, palier 1 clos par sa revue critique. L'ordre annoncé est épuisé ; au-delà, le budget sera dépassé. **Ordre de priorité retenu** : B3e, B7c, C7, REC ; C1 et C4+B7b sont les premiers coupés. C'est dit au lecteur, pas découvert le 31.
