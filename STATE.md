# STATE — avancement du cours

Dernière mise à jour : **30/10/2026** · Étape : **3 — paliers, programme recentré au 31/10**
Mode d'exécution : **B** (chat avec bac à sable éphémère, § 12.5)
Phase : **§ 5.0 — SANS CALCULS NORMATIFS** (`normes_disponibles = false`)

## Reprise (mode B — à lire en premier à chaque séance)

- **Dernier livrable** : `C2` — terrassements et évacuation. Zip : `cours-genie-civil-P1-C2.zip`
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
**24 livraisons**, dont **16 faites** et 8 au programme du 31/10 (`cadrage/07-programme-31-10.md`).

- **Livré (16)** : `E1` (socle) · `TV` (tranche verticale) · `D2` (planification, 32 défauts,
  8 bloquants — D-035) · `D1` (métrés et prix, 28 défauts, 7 bloquants) · `D4` (suivi et contrôle,
  32 défauts, 8 bloquants — D-042) · `C3` (gros œuvre, 33 défauts, 6 bloquants — D-040, D-041) ·
  `B3e` (béton armé en exécution, 36 défauts, 11 bloquants dont **trois erreurs de modèle
  physique**) · `B7c` (bâtiments ferroviaires, 39 défauts, 11 bloquants dont le **changement
  d'unité silencieux** — D-045 à D-048) · `C7` (qualité et HSE, 45 défauts, 13 bloquants —
  D-049 à D-052) · `REC` (réception, DOE, garanties, 28 défauts dont 8 bloquants — D-054 à
  D-057) · `RC1` (revue critique du palier, § 5.5, 23 défauts dont 6 bloquants — D-058) ·
  `C1` (installation de chantier, 23 défauts dont **3 bloquants** — D-059 à D-062) ·
  `D7` (pilotage multi-sites, 29 défauts dont **4 bloquants** — D-063, D-064) ·
  `B7b+C4` (lots techniques, 26 défauts dont **5 bloquants** — D-065 à D-067) ·
  `C6` (matériel, **29 défauts dont 4 bloquants** — D-068 à D-070) · `C2` (terrassements et
  évacuation, **passe non faite**). Toutes les autres passes sont faites, tous les bloquants
  et majeurs corrigés.
- ▶ **actifs, non écrits (7)** : A1, A2a, A5a, B5a-exec, D3, D6, M3D
- ⏸ **suspendus** (§ 5.0.4) : A2b, A3, A4, A5b, B1, B2, B3, B5a-calc, B6, B6b, B7a, R5

Fiches-module : `cadrage/05-sommaire.md` (périmètre d'origine, conservé pour mémoire).
Ordre de livraison **en vigueur** : `cadrage/07-programme-31-10.md`.

## Ce que le socle livre (Étape 1, § 5.2)

Charte et impression (AA) · SVG paramétrique (`assets/svgkit.js`, 13 générateurs déclarant leurs
options) · 3D (bundle IIFE 765 ko) · build qui échoue sur variable absente, légende incomplète,
nombre non balisé, option **ou format** inconnu, accident de gabarit · `calc/` : contre-calcul à
deux voies, étalonnages sur solution fermée, `pint` · **16 contrôles**, captures de toutes les figures.

## Défauts et passe adversariale /devil (§ 12.2)

Portée par un **sous-agent distinct** qui n'a pas lu le raisonnement de l'auteur et recalcule les
valeurs clés depuis `data/` seul. **19 rapports, 489 défauts, 105 bloquants** au dernier comptage de
`calc/revue.py` (borne basse, dette 27) — E1 : 50 en 3 passes, TV : 117 en 5, une passe pour chacun
des autres (D-034). **Tous les bloquants corrigés.** Détail de chaque défaut, de sa preuve et de la
suite donnée : `QA/`.

**Les onze familles de défauts, dans l'ordre où elles ont été trouvées.** (1) une grandeur d'état
**saisie** au lieu d'être dérivée ; (2) un paramètre déclaré que **rien ne lit** (C6 en avait deux) ;
(3) un ratio lu **hors de son domaine** (D-037, D-042) — C6 divisait des heures de 3 postes par une
fenêtre de 9 tâches ; (4) une légende qui ne montre pas la série annoncée ; (5) deux modules qui
recalculent la même grandeur (D-039) ; (6) une conclusion **déduite** d'une définition piégeuse
(D-040) ; (7) **B3e** — l'erreur de MODÈLE PHYSIQUE : une formule de recouvrement qui ne couvre pas
l'ouvrage ; (8) **B7c** — le CHANGEMENT D'UNITÉ SILENCIEUX : une grandeur garde son nom (« jours »)
et change de contenu (des plages de 6 h), `pint` lit des heures des deux côtés et ne voit rien ;
(9) **D7** — la PHRASE À CÔTÉ DU NOMBRE : ses quatre bloquants ont des calculs justes et des phrases
fausses, et aucun test ne lit une phrase ; (10) **C4** — l'ERREUR DE MODÈLE : chaque terme homogène
et un terme faux (78 j publiés contre 64 réels), que seule une **simulation directe** voit (D-067) ;
(11) **C6** — le TERME QUI MANQUE D'UN SEUL CÔTÉ : le carburant du chariot compté dans la possession
et pas dans la location pourtant déclarée « nue », la pente publiée valant **exactement ce gasoil**,
et le verdict s'inversant (D-070).

**Ce qui les trouve** : une contre-expertise à l'aveugle, deux nombres du même fichier de sortie,
des captures regardées, une simulation directe, et un **croisement de périmètre avec un autre
module** — c'est ainsi que C2 a trouvé le défaut que la passe de C6 n'avait pas vu. **Jamais un
test.**

**Trois fautes de méthode.** D4 a modifié les fichiers de D1 pendant sa passe, et **C1 les siens
pendant la sienne** : un livrable en relecture est figé. Et deux fois — C3 puis B3e — un test
épinglait la **conclusion narrative** au lieu de la règle (D-041, D-043).

**La règle qui en sort** : toute grandeur d'état est **dérivée**, un test refait la dérivation ; tout
paramètre déclaré est **relu dans le résultat qu'il engendre** ; tout **verdict est une sortie de
`calc/`** ; toute V3 est registrée et vérifiée dans sa fourchette ; deux modules qui chiffrent la
même tâche **trouvent les mêmes heures** ; chaque verdict porte son canari. **74 canaris, tous
rouges**, et deux ont trouvé seuls une erreur que la passe n'avait pas vue : un canari cherche.

**Dette TV** : scalaires V3 hors registre · deux bibliothèques hors vérification dimensionnelle. **Grilles § 7.2 : minimum 2 partout** (`QA/grilles-72.md`). **Dix simplifications déclarées** (§ R6), inchangées depuis C3 sauf la dernière, détaillées dans chaque module et dans git : une scène 3D par vue · contour de cadre en polyligne · fiches P2/P3 sobres · substitut textuel de la 3D à l'impression · cadres sans crochets (métré minorant, 0,08 % du total) · coffrage sans étaiement en démonstration · vérification dimensionnelle déportée · un seul relevé d'avancement dans `data/` · le contrôle de sécurité ne cherche qu'un mot · deux courbes de C2 sans graduation d'ordonnée (dette 39).

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
| 12 | Le contre-calcul n° 1 ne passe que sur **27 %** de la fourchette déclarée : publié comme tel | attachements réels |
| 39 | **`diagramme` ne peut pas graduer son axe Y si l'extremum de la courbe est à l'abscisse la plus à gauche** : son étiquette, centrée sur l'axe, percute la graduation. Les deux courbes de C2 sont dans ce cas — le contrôle de chevauchement l'a trouvé, il fonctionne. Elles sont livrées sans graduation d'ordonnée, extremums annotés ; le générateur devrait décaler l'étiquette | à outiller |
| 11, 13 | **Deux contrôles de figure qui manquent, et c'est la dette la plus lourde.** Les chevauchements **texte contre trait** ne sont pas détectés (le test ne compare que texte contre texte), et rien ne vérifie qu'une figure **montre ce qu'elle prétend montrer** : 3 bloquants de la TV, 6 de D2, et deux légendes fausses de D7 trouvées à l'œil sur les captures | à outiller |
| 23 | **D1 et D2 divergent de ×2,1 sur les heures du plancher de mezzanine** (3 219 contre 6 880 h) : D1 compte les heures productives à la cadence, D2 tout l'effectif de zone présent pendant tout le cycle. Écart antérieur, exposé par le nouveau contrôle croisé, déclaré comme exception nommée dans `test_prix.py` | avant la revue de palier |
| 21 | **Le chantier dure désormais 600 j ouvrés** (fin 2029-04-23) au lieu de 363, parce que B7c a corrigé la tâche sous consignation. D1 et D4 ont suivi par le build ; leurs **textes** n'ont pas été relus ligne à ligne avec les nouvelles dates (D-045, choix du lecteur : laisser le build propager) | avant la revue de palier |
| 22 | **Flake de rendu** : les deux contrôles 3D de `00-demo-cage` échouent par intermittence sur un avertissement du moteur WebGL logiciel, et passent au rejeu. Ce n'est pas un défaut du cours, c'est l'environnement — mais un contrôle qui échoue au hasard finit par ne plus être lu | à outiller |
| 27 | **Le comptage des défauts des passes est une borne basse.** `calc/revue.py` compte les cellules de gravité des tableaux de `QA/` — 16 rapports, 411 défauts, 93 bloquants au dernier build. Un rapport qui présenterait ses défauts hors tableau serait sous-compté ; la limite est publiée avec le chiffre | à outiller si besoin |
| 26 | **D1 et REC divergent sur la date de restitution de la retenue de garantie.** D1 écrit qu'elle « ne revient qu'après la réception » et bâtit sa courbe de trésorerie là-dessus ; REC dit qu'elle est immobilisée jusqu'à une date que le marché fixe (⏸), postérieure. REC ne contredit plus D1 frontalement, mais le besoin de trésorerie publié par D1 est optimiste de la durée de la garantie | revue de palier |
| 25 | **La date de fin publiée par D2 ne comprend pas une réception décomposée.** REC mesure, en rejouant le réseau, que les deux tâches de fin du planning demandent 16 jours ouvrés de plus que ce qu'elles portent : ESSA 15 j prévus pour 25 demandés, RECE 10 pour 16. Soit **16 jours de fin**, de 260 000 à 2 046 000 MAD selon que le chantier est ou non sous pénalités. Les deux durées sont des décisions de ce cours, posées à deux moments (D-055) ; l'écart n'est pas reporté dans `data/` tant que le lecteur n'a pas tranché | revue de palier |
| 36 | **C6 ne sait pas combien de MACHINES sert une famille.** Il déduit les heures d'un engin des jours de ses tâches ; D2 prévoit **2 ateliers de terrassement**, donc 2 pelles. C2 l'a trouvé par croisement : **15 759 MAD**, 16,7 % du coût de pelle de C6. Correction : un champ `nb_machines` par famille, et relire les trois verdicts | avant la revue de palier |
| 37 | **C2 est livré sans ses exercices** (la fiche en prévoyait 2 + 1) ; sa passe adversariale a été lancée. Le module porte son quiz et ses quatre résultats | dès la reprise |
| 38 | **Passe de C6 : 2 majeurs et 15 mineurs non corrigés** (les 4 bloquants et 8 majeurs le sont). Les deux majeurs sont de fond : (a) la « simulation » de la chaîne du coulage est **tautologique** — elle tire les mêmes p indépendants, donc elle ne peut que confirmer le produit, et l'**indépendance des quatre maillons** n'est déclarée nulle part ; (b) la **pointe du matériel de chantier** n'existe nulle part — C6 montre 3 engins, C1 en a 2 de plus, la pointe réelle est de 5. Détail et suite donnée : `QA/C6-passe1.md` | avant la revue de palier |
| 33 | **Le format `::n3` n'existait pas et rendait la valeur brute** — 45 occurrences dans six modules livrés, dont des CPI à quatre décimales à côté des mêmes à trois. Le build échoue désormais sur un format inconnu, et `n3`/`n4` sont implémentés. **La leçon est la même que pour les options de figure : un format ignoré en silence est un défaut, pas une tolérance** | fait |
| 35 | **Les six corps d'état du second œuvre sont des durées V3** (30, 45, 30, 25, 25, 20 j) et le coût d'une frontière de zone aussi (0,4 j). Leur somme reproduit à 4 % la durée que D2 déclare, ce qui crédite le **modèle** — une file pipelinée sur huit zones — mais pas chacune des six durées : six nombres peuvent se compenser | attachements réels |
| 34 | **Le second site de D7 est entièrement V3** : budget, lots, avancements, coût réel, date de besoin et retard sont fabriqués. Les mécanismes (consolidation, amortissement, masquage, latence, quantisation) sont exacts et étalonnés ; les nombres qui les illustrent ne décrivent aucun chantier réel. **Et la latence n'est chiffrée que pour l'opération** : les frais de durée du second site ne sont pas déclarés | levée du § 5.0 |
| 32 | **Deux contrôles que la passe de C1 propose et que personne n'a outillés** : (1) « la cadence du débit est celle qui produit la durée de la tâche » ; (2) **« toute grandeur multipliée par une durée de chantier nomme la fenêtre d'emploi de la ressource qu'elle loue »**. Le second attraperait la ligne de frais de durée de D1, qui porte le même défaut depuis trois modules | à outiller, et c'est la plus rentable |
| 28 | **D1 budgète une grue sur 29,7 mois, C1 en retient deux sur 5,8.** D1 facture la grue en frais de durée sur toute la durée du chantier ; C1 lit dans le planning que les tâches servies par la grue tiennent dans une fenêtre de 117 j ouvrés. Les deux écarts vont en sens inverse et celui de la durée l'emporte : **D1 surestime de 1 723 300 MAD**. C1 publie l'écart et ne corrige pas le bordereau (D-055, D-062) : la correction demande une révision explicite du prix de revient, donc une décision du lecteur | revue de palier |
| 29, 30 | **Deux dettes d'échafaudage.** Les fiches livrées de REC et de RC1 ne sont pas écrites (D-061) ; B7c, C7 et C1 ont la leur. Et `npm run check` a échoué 4 fois sur 16 pour une raison étrangère au cours — `maxBuffer` de 1 Mo dépassé par la sortie de Playwright (108 tests), corrigé à 64 Mo : l'échafaudage grandit avec le cours, et un faux rouge coûte autant qu'un faux vert | prochaine revue |
| 31 | **Le contrôle « chaque V3 de data/ est registrée » compare des NOMBRES, pas des chemins.** Le massif de grue (180 000 MAD) passait parce que D1 déclare un encadrement à 180 000 MAD/mois — une grandeur sans rapport. Il est désormais déclaré en propre, mais le contrôle reste satisfiable par coïncidence : il faudrait une colonne de chemin dans le registre | à outiller |
| 17, 24 | **C3 et C7, non corrigés** : 5 mineurs de C3 (dont deux durées du plancher coexistant dans `data/`) et, pour C7, la pondération de nuit (1,8) et l'abattement de B7c (30 %) qui restent deux coefficients pour une même cause. Détail : `QA/C3-passe1.md`, `QA/C7-passe1.md` | avant la prochaine revue |
| 20 | **B3e, non corrigés** : 17 majeurs et 8 mineurs, dont ~20 nombres techniques écrits à la main (§ 4.3) et trois listes de points de contrôle avant coulage sans renvoi croisé. Détail : `QA/B3e-passe1.md` | avant la revue de palier |
| 19 | **B3e** : le plan de ferraillage est **fictif et calibré** sur les ratios V3, non dimensionné — une première version posée à vue pesait 35 à 43 % de moins. Le module le dit quatre fois ; il reste qu'aucune de ses sections n'est justifiée. Levée : module **B3c** à l'arrivée du BAEL | levée du § 5.0 |
| 16, 18 | **D1 et D4, non corrigés** (D-034) : figure 4 de D1 écrite en dur, un seul canari pour cinq verdicts, nombres à la main, dix mineurs ; et les totaux de D1 sont calculés **sans** sa ligne de divers calibrée (28,7 %), donc ce sont des **bornes basses**. D4 : 15 majeurs et 9 mineurs. Détail : `QA/D1-passe1.md`, `QA/D4-passe1.md` | avant la revue de palier |
| 15 | **D1, corrigé en écrivant D4** : l'avancement déclaré de la situation était saisi à la main dans `data/` et décrivait un état de chantier du 2ᵉ mois pour une situation annoncée au 7ᵉ. Il est désormais dérivé du réseau (`calc/etat.py`), partagé par D1 et D4 | fait, D-039 |
| 14 | **D2, non corrigés** (D-034) : 5 majeurs (réseau et lots en dur dans `calc/`, 9 effectifs sans fourchette, levier de voie modélisé par un contournement, nombres à la main) et 6 mineurs. Détail : `QA/D2-passe1.md` | avant la revue de palier |

## Données modifiées depuis la dernière livraison

Jeux figés en 1.0, valeurs de conception inchangées. Ajouts : `armatures` (B3e) et `ferroviaire`
(B7c). Corrigé par les passes : parc de tables, étais, `suivi.quantites_relevees`, `materiel`,
`cycle_zone`, portées des nappes, segments de cadres, base des ratios d'acier. **227 hypothèses V3
registrées**, toutes couvertes. Ajouts de C7 : l'heure de contrôle d'un cadre (140 MAD/h, distincte de l'heure de compagnon), les heures annuelles d'un compagnon, les cinq ratios de déchets désormais tous balisés ; le plan de contrôle porte l'exécutant ET le visa, les points d'arrêt avec leur durée, et le renvoi vers les plans de C3 et de B3e. Ajouts de C1 : le bloc `installation` (grue, trois variantes de calage, pièces à lever — dont celle de charpente **lue** chez B7c et non redéclarée —, levages, base-vie, aires) et `installation.voisinage`. Le taux d'utilisation de la grue porte son unité dans son nom (D-056). Ajouts de D7 : `multi_sites` (second site lot par lot, seuils du tableau de bord, rythmes de reporting). Ajouts de B7b+C4 : `lots_techniques` (diamètres courants, densité de réservations, délai de gel, cinq postes d'un percement, six corps d'état et le coût d'une frontière de zone). Ajouts de C6 : `materiel_engins` (trois familles avec leur **régime de service** et leur **régime de location**, cascade de rendement de la pompe, quatre maillons de la chaîne du coulage avec leur secours, mutualisation). Détail dans git et dans `QA/`.

## Effort consommé (§ 13.2)

**25 séances** : Étape 0 = 1 · Étape 1 = 2 · Étape 2 = 4 · un module par séance ensuite, plus 3 pour les passes et corrections de C3, D4, B7c et C7. **Avancement sur le programme du 31/10** : **16 livraisons sur 18**. Restent : D3, D6, A1, A2a, A5a, B5a-exec, M3D — plus que le budget ne permet d'ici le 31/10. L'arbitrage est au lecteur, et il est posé, pas découvert le 31.
