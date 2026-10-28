# STATE — avancement du cours

Dernière mise à jour : **28/10/2026** · Étape : **3 — paliers, programme recentré au 31/10**
Mode d'exécution : **B** (chat avec bac à sable éphémère, § 12.5)
Phase : **§ 5.0 — SANS CALCULS NORMATIFS** (`normes_disponibles = false`)

## Reprise (mode B — à lire en premier à chaque séance)

- **Dernier livrable** : `C1` — installation de chantier. Zip : `cours-genie-civil-P1-C1.zip`
- **Toutes les passes /devil sont faites**, tous les bloquants corrigés. C7 : **45 défauts,
  13 bloquants, 22 majeurs — livraison refusée en première passe**, tous traités (D-049 à D-052).
- **Commande de contrôle** : `npm ci --ignore-scripts && npm run check`
- **EN ATTENTE DE VALIDATION** : la TV (forme, profondeur, utilité de la 3D). Les cinq relecteurs
  ont tous jugé l'absence de 3D justifiée.
- **PALIER 1 CLOS** par sa revue critique (RC1). Le lecteur a donné le go sur **C1**, premier
  module d'après-palier ; la suite du programme reste à arbitrer (§ 5.5).
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
**24 livraisons**, dont **12 faites** et 13 au programme du 31/10 (`cadrage/07-programme-31-10.md`).

- **Livré (12)** : `E1` (socle) · `TV` (tranche verticale) · `D2` (planification, 32 défauts,
  8 bloquants — D-035) · `D1` (métrés et prix, 28 défauts, 7 bloquants) · `D4` (suivi et contrôle,
  32 défauts, 8 bloquants — D-042) · `C3` (gros œuvre, 33 défauts, 6 bloquants — D-040, D-041) ·
  `B3e` (béton armé en exécution, 36 défauts, 11 bloquants dont **trois erreurs de modèle
  physique**) · `B7c` (bâtiments ferroviaires, 39 défauts, 11 bloquants dont le **changement
  d'unité silencieux** — D-045 à D-048) · `C7` (qualité et HSE, 45 défauts, 13 bloquants —
  D-049 à D-052) · `REC` (réception, DOE, garanties, 28 défauts dont 8 bloquants — D-054 à
  D-057) · `RC1` (revue critique du palier, § 5.5, 23 défauts dont 6 bloquants — D-058) ·
  `C1` (installation de chantier, D-059 à D-061 — **passe adversariale à faire**).
  Toutes les passes sont faites sauf celle de C1 ; tous leurs bloquants et majeurs corrigés.
- ▶ **actifs, non écrits (12)** : A1, A2a, A5a, B5a-exec, B7b, C2, C4, C6, D3, D6, D7, M3D
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
valeurs clés depuis `data/` seul. **16 rapports, 411 défauts, 93 bloquants** au dernier comptage de
`calc/revue.py` (borne basse, dette 27) — E1 : 50 en 3 passes, TV : 117 en 5, une passe pour chacun
des autres (D-034). **Tous les bloquants corrigés**, sauf C1 dont la passe reste à faire. Détail de
chaque défaut, de sa preuve et de la suite donnée : `QA/`.

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

**Deux fautes de méthode à ne pas reproduire.** D4 a modifié les fichiers de D1 pendant sa passe : un
livrable en relecture est figé. Et deux fois — C3 puis B3e — un test épinglait la **conclusion
narrative** au lieu de la règle : un test vérifie une règle, jamais un résultat raconté (D-041, D-043).

**La règle qui en sort** : toute grandeur d'état est **dérivée**, un test refait la dérivation ; tout
paramètre déclaré est **relu dans le résultat qu'il engendre** ; tout **verdict est une sortie de
`calc/`** ; toute V3 est registrée et vérifiée dans sa fourchette ; deux modules qui chiffrent la
même tâche **trouvent les mêmes heures** ; chaque verdict porte son canari. **74 canaris, tous
rouges**, et deux ont trouvé seuls une erreur que la passe n'avait pas vue : un canari cherche.

**Dette TV** : scalaires V3 hors registre · deux bibliothèques hors vérification dimensionnelle ·
glossaire S7 absent. **V2 en attente** : aucune (le build échoue sur toute balise V2, § 5.0.6).

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
| 23 | **D1 et D2 divergent de ×2,1 sur les heures du plancher de mezzanine** (3 219 contre 6 880 h) : D1 compte les heures productives à la cadence, D2 tout l'effectif de zone présent pendant tout le cycle. Écart antérieur, exposé par le nouveau contrôle croisé, déclaré comme exception nommée dans `test_prix.py` | avant la revue de palier |
| 21 | **Le chantier dure désormais 600 j ouvrés** (fin 2029-04-23) au lieu de 363, parce que B7c a corrigé la tâche sous consignation. D1 et D4 ont suivi par le build ; leurs **textes** n'ont pas été relus ligne à ligne avec les nouvelles dates (D-045, choix du lecteur : laisser le build propager) | avant la revue de palier |
| 22 | **Flake de rendu** : les deux contrôles 3D de `00-demo-cage` échouent par intermittence sur un avertissement du moteur WebGL logiciel, et passent au rejeu. Ce n'est pas un défaut du cours, c'est l'environnement — mais un contrôle qui échoue au hasard finit par ne plus être lu | à outiller |
| 27 | **Le comptage des défauts des passes est une borne basse.** `calc/revue.py` compte les cellules de gravité des tableaux de `QA/` — 16 rapports, 411 défauts, 93 bloquants au dernier build. Un rapport qui présenterait ses défauts hors tableau serait sous-compté ; la limite est publiée avec le chiffre | à outiller si besoin |
| 26 | **D1 et REC divergent sur la date de restitution de la retenue de garantie.** D1 écrit qu'elle « ne revient qu'après la réception » et bâtit sa courbe de trésorerie là-dessus ; REC dit qu'elle est immobilisée jusqu'à une date que le marché fixe (⏸), postérieure. REC ne contredit plus D1 frontalement, mais le besoin de trésorerie publié par D1 est optimiste de la durée de la garantie | revue de palier |
| 25 | **La date de fin publiée par D2 ne comprend pas une réception décomposée.** REC mesure, en rejouant le réseau, que les deux tâches de fin du planning demandent 16 jours ouvrés de plus que ce qu'elles portent : ESSA 15 j prévus pour 25 demandés, RECE 10 pour 16. Soit **16 jours de fin**, de 260 000 à 2 046 000 MAD selon que le chantier est ou non sous pénalités. Les deux durées sont des décisions de ce cours, posées à deux moments (D-055) ; l'écart n'est pas reporté dans `data/` tant que le lecteur n'a pas tranché | revue de palier |
| 28 | **D1 budgète une grue, C1 en retient deux.** Les frais de durée de D1 portent le loyer d'**une** grue à tour (95 000 MAD/mois) ; C1 conclut à 2 grues par deux voies indépendantes. Écart : **2 821 500 MAD** sur la durée du chantier. C1 publie l'écart et ne corrige pas le bordereau (D-055) : la correction demande une révision explicite du prix de revient, donc une décision du lecteur | revue de palier |
| 29, 30 | **Deux dettes d'échafaudage.** Les fiches livrées de REC et de RC1 ne sont pas écrites (D-061) ; B7c, C7 et C1 ont la leur. Et `npm run check` a échoué 4 fois sur 16 pour une raison étrangère au cours — `maxBuffer` de 1 Mo dépassé par la sortie de Playwright (108 tests), corrigé à 64 Mo : l'échafaudage grandit avec le cours, et un faux rouge coûte autant qu'un faux vert | prochaine revue |
| 31 | **Le contrôle « chaque V3 de data/ est registrée » compare des NOMBRES, pas des chemins.** Le massif de grue (180 000 MAD) passait parce que D1 déclare un encadrement à 180 000 MAD/mois — une grandeur sans rapport. Il est désormais déclaré en propre, mais le contrôle reste satisfiable par coïncidence : il faudrait une colonne de chemin dans le registre | à outiller |
| 17, 24 | **C3 et C7, non corrigés.** C3 : le `floor` du parc ne mord sur aucune ligne du tableau (m5) · cure de 2 j insensible sur sa fourchette (m6) · loyer et montage sans bornes dans le tableau (m7) · loyer sans battement ni repli, donc **borne basse** (m8) · deux durées du plancher coexistent dans `data/` (m10). C7 : la pondération de nuit (1,8) et l'abattement de cadence de nuit de B7c (30 %) restent deux coefficients pour une même cause, leurs notes se croisent sans qu'aucun soit dérivé de l'autre · 4 mineurs de forme (`QA/C7-passe1.md`) | avant la prochaine revue |
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
`cycle_zone`, portées des nappes, segments de cadres, base des ratios d'acier. **207 hypothèses V3
registrées**, toutes couvertes. Ajouts de C7 : l'heure de contrôle d'un cadre (140 MAD/h, distincte de l'heure de compagnon), les heures annuelles d'un compagnon, les cinq ratios de déchets désormais tous balisés ; le plan de contrôle porte l'exécutant ET le visa, les points d'arrêt avec leur durée, et le renvoi vers les plans de C3 et de B3e. Ajouts de C1 : le bloc `installation` (grue, trois variantes de calage, pièces à lever — dont celle de charpente **lue** chez B7c et non redéclarée —, levages, base-vie, aires) et `installation.voisinage` (distance de la façade côté voies au gabarit de la voie). Détail dans git et dans `QA/`.

## Effort consommé (§ 13.2)

**20 séances** : Étape 0 = 1 · Étape 1 = 2 · Étape 2 = 4 · D2, D1, D4, C3, B3e, B7c, C7, REC, RC1, C1 = 1 chacun, plus 3 pour les passes et corrections de C3, D4, B7c et C7.
**Avancement sur le programme du 31/10** : **12 livraisons sur 18**. C1, premier module de l'ordre de coupe, a été livré sur go du lecteur. Restent : C4+B7b, C2, C6, D3, D6, D7, A1, A2a, A5a, B5a-exec, M3D — plus que le budget ne permet d'ici le 31/10. L'arbitrage est au lecteur, et il est posé maintenant, pas découvert le 31.
