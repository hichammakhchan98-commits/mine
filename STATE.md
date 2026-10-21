# STATE — avancement du cours

Dernière mise à jour : **21/10/2026** · Étape : **3 — paliers, programme recentré au 31/10**
Mode d'exécution : **B** (chat avec bac à sable éphémère, § 12.5)
Phase : **§ 5.0 — SANS CALCULS NORMATIFS** (`normes_disponibles = false`)

## Reprise (mode B — à lire en premier à chaque séance)

- **Dernier livrable** : `D4` — Suivi et contrôle. Zip : `cours-genie-civil-P1-D4.zip`
- **Commande de contrôle** : `npm ci --ignore-scripts && npm run check`
- **EN ATTENTE DE VALIDATION** : la TV (forme, profondeur, utilité de la 3D). Les cinq relecteurs
  ont tous jugé l'absence de 3D justifiée.
- **Prochain module** : `C3` — Gros œuvre (coffrage, ferraillage, bétonnage, cycle par niveau).
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
**24 livraisons**, dont **5 faites** et 16 au programme du 31/10 (`cadrage/07-programme-31-10.md`).

- **Livré** : `E1` (socle), `TV` (tranche verticale), `D2` (planification, 32 défauts, 8 bloquants
  **tous corrigés** — D-035), `D1` (métrés et prix), `D4` (suivi et contrôle).
  Passes /devil **à lancer** sur D1 et D4.
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
valeurs clés depuis `data/` seul. E1 : **50 sur trois passes**. TV : **117 sur cinq passes**.
D2 : **32 sur une passe**, D1 : **28 sur une passe** (D-034). Rapports : `QA/`.

**D1**, dont **deux récidives dans le module qui enseigne à ne pas les commettre** : un ratio au m²
comparé hors de son domaine, un facteur de recalage moyenné au lieu d'être pondéré (×2,52 annoncé
pour ×1,92 réel). Les autres : un délai de paiement calendaire comparé à des jours ouvrés (besoin de
trésorerie 15,4 → 10,4 MMAD), des frais de chantier en mois de 21 jours, un écart d'attachement
déclaré et registré que **rien ne lisait**, un verdict jamais publié, une légende contradictoire.
**Tous corrigés.** Les 34 tests de D1 étaient verts et n'en avaient vu aucun.

**Ce qui les trouve** : une contre-expertise à l'aveugle, deux nombres du même fichier de sortie, et
des captures regardées. **Jamais un test.**

**Faute de séquencement à ne pas reproduire** : D4 a modifié les fichiers de D1 pendant sa passe
adversariale, et a corrigé un de ses bloquants par effet de bord. Un livrable en relecture est figé.

### D2 — 8 bloquants · D1 — 7 bloquants · aucun vu par les contrôles

**D2** : une fenêtre de consignation calculée, publiée, puis jetée (17,5 j ouvrés, un mois de date
contractuelle) ; une figure qui ne traçait pas la série annoncée ; une moyenne recalculée dans le
dessin ; une légende commentant un palier qui n'était pas celui-là ; une courbe en S bâtie sur
l'étalement (+13,8 %) ; une séquence contredisant la rubrique sécurité du module ; deux
recouvrements plus grands que la durée recouverte ; la grue vérifiée en moyenne. **Tous corrigés**
(D-035), avec leur contrôle et leur canari.

### E1 (3 passes, 50 défauts) et TV (5 passes, 117 défauts)

Détail : `QA/`. Les quinze bloquants de la TV sont la même famille que ceux de D2 et D1.

**La règle qui en sort** : toute grandeur d'état est **dérivée** et un test refait la dérivation ;
tout paramètre déclaré est **relu dans le résultat qu'il engendre** ; tout **verdict publié est une
sortie de `calc/`** ; toute V3 est registrée et vérifiée dans sa fourchette ; un module à risque
porte ses dispositions de sécurité (§ 3.4) ; chaque contrôle rendant un verdict porte son canari.
**Canaris** : 14 sur E1 et TV, 11 inventés par les relecteurs, 5 par D2, 7 par D1 ; tous rouges.

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
| 6 | Contrôle d'impression visuel, non automatisé | à outiller |
| 7 | Bundle 3D de 765 ko, hors budget par module | à surveiller |
| 8 | **Les tags git ne sont pas poussables** dans ce bac à sable (le proxy n'expose que `refs/heads/*`) : les tags de palier vivent dans le zip, pas sur GitHub | limite de l'environnement |
| 9 | `TV` sans modèle 3D (le phasage appartient à C3) — à réviser si vous jugez qu'il en manque un | après validation |
| 10 | **Part de main-d'œuvre hors fourchette.** D1 l'a instruite : la base du ratio était fausse (bordereau entier au lieu du béton armé décomposé), **et** les cadences sont optimistes — facteur **×1,92** pondéré par le travail, chemin indépendant. Le soupçon « 2 à 3 » est confirmé dans son sens, **revu à la baisse dans son ampleur**. **Chiffrée, non soldée** | attachements réels |
| 11 | Chevauchements **texte contre trait** non détectés : le test ne compare que texte contre texte | à outiller |
| 12 | Le contre-calcul n° 1 ne passe que sur **27 %** de la fourchette déclarée : publié comme tel | attachements réels |
| 13 | Aucun contrôle ne vérifie qu'une figure **montre ce qu'elle prétend montrer** : 3 bloquants de la TV et 6 de D2 ont franchi tous les contrôles verts | à outiller, et c'est la dette la plus lourde |
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

**10 séances** : Étape 0 = 1 · Étape 1 = 2 · Étape 2 = 4 · D2 = 1 (dont la passe et ses
corrections) · D1 = 1 · D4 = 1.
**Avancement sur le programme du 31/10** (18 livraisons) : **5 faites**, dont les deux plus chères,
le socle ne se refaisant pas et le témoin ayant absorbé les défauts de méthode. Reste 13 livraisons
en 10 jours : **1 à 2 par séance**, une passe adversariale par module (D-034), majeurs et mineurs
portés en dette plutôt que corrigés.
