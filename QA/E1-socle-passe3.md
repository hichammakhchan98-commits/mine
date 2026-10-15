# Passe adversariale « /devil » n° 3 — Étape 1, socle

Contre-relecture de `5d3857f`, après correction annoncée du bloquant **N2** et des 7 majeurs de
`QA/E1-socle-passe2.md`. Mêmes règles : le raisonnement de l'auteur n'a pas été lu, `STATE.md` et les
sections de suites de `QA/` n'ont servi à juger aucune valeur, tout a été recalculé depuis
`data/demo-cage.json` seul avant d'ouvrir `calc/`.

Exécuté : `npm run check` (11 contrôles verts), recalcul indépendant des onze valeurs publiées, le
**test du clone neuf** demandé au point 3, les **quatre canaris de la passe 2 rejoués**, **cinq
nouveaux canaris** visant les zones touchées, et l'examen des captures.

---

## 1. Contre-expertise à l'aveugle, refaite

Recalcul depuis les seuls paramètres et la section `conventions` (axe du cadre à `enrobage + ⌀/2`
**en section comme le long de l'axe**, r = 20 mm, sans crochets).

| Grandeur | Mon recalcul | Publié | |
|---|---:|---:|---|
| Zone ferraillée — 2000 − 2(30 + 4) | **1932 mm** | — | |
| Nombre de cadres — 1 + ⌈1932/150⌉ = 1 + ⌈12,88⌉ | **14** | 14 | ✓ |
| Espacement réel — 1932/13 | **148,615 mm** | 14,86 cm | ✓ |
| **About réellement réalisé** — (30 + 4) − 4 | **30,00 mm** | — | ✓ **N1 corrigé** |
| Rectangle d'axe du cadre | **282 × 682 mm** | 28,2 × 68,2 | ✓ |
| Périmètre discrétisé / fermé | **1,89353 / 1,89366 m** | 1,89353 / 1,89366 | ✓ |
| Longueur développée | **26,5095 m** | 26,509 | ✓ |
| Masse cadres / barres | **10,4602 / 20,4769 kg** | 10,46 / 20,48 | ✓ |
| **Masse totale** | **30,93716 kg** | 30,94 | ✓ |
| Ratio | **58,9279 kg/m³** | 58,9 | ✓ |
| **Coût** — 30,937 × 14 et × 20 | **433,1 à 618,7 MAD** | 433 à 619 | ✓ **N4 corrigé** |
| **Heures de ferrailleur** — 8 × 30,937/130 et /90 | **1,904 à 2,750 h** | 1,9 à 2,8 | ✓ |
| Variante 7 cm — 1 + ⌈1932/70⌉ | **29 cadres ; 42,14 kg ; Δ 11,2** | 29 / 42,14 / 11,2 | ✓ |

**Treize valeurs recalculées, treize concordances.** Aucun écart.

**Point 2 du mandat — about réel.** Mesuré : la peau du premier cadre est à **30,00 mm** de la face
d'about, contre **26,0 mm** sous la règle de la passe 2 (que j'ai rejouée pour comparer). N1 est
corrigé, et l'enrobage est désormais tenu dans les trois directions.

**Point 3 du mandat — clone neuf.** `git archive HEAD` extrait dans un répertoire vierge, `git init`,
`npm ci`, `npm run check` → **VERT, 11 contrôles**, et `git status --porcelain` **vide** après coup.
`git ls-files | grep pycache` → aucun fichier ; `.gitignore` contient `__pycache__/` et `*.pyc`.
**N6 corrigé, vérifié dans les conditions exactes où il échouait.**

**Point 5 du mandat — registre.** `data/registre-hypotheses.csv` porte 5 lignes dont les **huit
colonnes** sont remplies, `fourchette` et `annee_ref` comprises ; `build/build.mjs:230` **fait
échouer le build** si l'une des deux manque, et le registre est **généré** depuis les balises, donc
il ne peut plus diverger du texte. **N3 corrigé** — une réserve en **P6**.

---

## 2. Les neuf canaris (point 7 du mandat)

Protocole : clone neuf, un canari à la fois, `bundle` + `calc` + `build`, commit, `npm run check`.

| # | Canari | Résultat | Assertion qui mord |
|---|---|---|---|
| **C3** | *(rejoué)* tube du cadre redivisé → HA8 dessiné en HA4 | **détecté** | « diamètre du tube du cadre (mm), attendu 8 » |
| **C4** | *(rejoué)* barres du SVG décalées de 10 cm en hauteur | **détecté** | « ordonnée des barres en SVG (cm) » |
| **C6** | *(rejoué)* barres du SVG resserrées de 20 % | **détecté** | « abscisse des barres en SVG (cm) » |
| **C8** | *(rejoué)* comptage faux **des deux côtés** | **détecté** | « nombre de cadres recalculé depuis data/ : 14 » |
| **D1** | *(nouveau)* règle de placement : `retrait = enrobage` seul, **des deux côtés** — la correction N1 annulée | **détecté** | « espacement réel » (recalcul indépendant dans le test) |
| **D2** | *(nouveau)* règle d'**axe** ramenée à `enrobage`, **des deux côtés**, la chaîne de convention laissée intacte | **détecté** | « axe du cadre en 3D » |
| **D3** | *(nouveau)* **calcul économique** : coût max × 10 (6 188 MAD au lieu de 619) | **PASSE, non détecté** | — |
| **D4** | *(nouveau)* valeur V3 chiffrée publiée **sans balise ni ligne de registre** (« le béton revient à 1 350 MAD/m³ (V3) ») | **PASSE, non détecté** | — |
| **D5bis** | *(nouveau)* **longueur de barre fausse, vraiment partagée** (Python + les trois sites de la 3D) | **PASSE, non détecté** | — |

Les quatre canaris de la passe 2 sont bien rouges : **vérifié moi-même**, avec l'assertion exacte.
Sur les cinq nouveaux, **deux sont rouges et trois passent**. D1 et D2 sont la preuve que la parade du
§ 3.3 fonctionne désormais : une erreur de modèle **partagée** sur le placement ou sur la règle d'axe
est rattrapée par le recalcul indépendant logé dans le test. D5bis montre que cette parade a un trou.

*(Note de méthode : une première version de D5 n'avait faussé que la géométrie dessinée des barres, pas
la longueur que la 3D rapporte ; elle était détectée par simple divergence Python/JS. D5bis corrige les
quatre sites pour que l'erreur soit réellement commune — et passe alors.)*

---

## 3. Défauts

| défaut | gravité | preuve | correction proposée |
|---|---|---|---|
| **P1 · Une phrase publiée énonce une valeur fausse et porte une correction inachevée ; et l'encart annonce trois simplifications pour quatre.** | **majeur** | Rendu dans `modules/00-demo-cage.html`, extrait verbatim : « L'enrobage vaut aussi le long de l'axe : **l'axe du premier cadre est à 20 mm près de l'about… non — à l'enrobage plus le demi-diamètre du cadre**, comme en section. » Trois problèmes dans une phrase : (a) 20 mm est le **rayon de cintrage** (`{{metre-cage.rayon_cintrage_mm}}` injecté là où l'enrobage est attendu) ; la valeur juste est **34 mm**, que j'ai recalculée au § 1 ; (b) « … non — » est une **auto-correction laissée dans le texte publié** ; (c) le titre dit « **Trois** simplifications » alors que `grep -cE "^[0-9]+\. "` compte **4** items. Le paragraphe qui annonce la correction de N1 est donc le seul de la page à publier un nombre faux. **Je ne le classe pas bloquant** : la règle correcte est énoncée dans la même phrase, et aucune valeur calculée n'en dépend — mais c'est une décision de proportion, pas une absolution. | Écrire « l'axe du premier cadre est à {{…}} mm de l'about » depuis une variable (ou en toutes lettres : enrobage + demi-diamètre), supprimer « … non — », et corriger le titre en « Quatre simplifications ». |
| **P2 · Le filet de sécurité annoncé par la page n'existe pas pour la longueur des barres — et l'étalonnage n'attrape aucun des trois cas cités.** Texte publié : « Ce que ce contre-calcul n'attrape donc pas : … un comptage de cadres faux, une règle d'axe fausse, **une longueur de barre fausse**. Ces erreurs-là **sont attrapées ailleurs : par l'étalonnage**, et par des tests qui recalculent le comptage et les positions dans le test lui-même. » | **majeur** | Canari **D5bis** : `long_barre_m = (L − 4e)` côté Python **et** les trois sites de la 3D (`CylinderGeometry`, `barres.push`, `longueurBarre_m`). Résultat publié : longueur de barre **1,88 m au lieu de 1,94**, masse totale **30,30 kg au lieu de 30,94** (−2,1 %), ratio **57,7**, coût **424–606 MAD au lieu de 433–619**. `npm run check` → **VERT, 11 contrôles**. Le contre-calcul reste à 0,077 %, `perimetre_plausible` reste vrai, le garde-fou 30–250 reste franchi. Quant à « par l'étalonnage » : `calc/etalonnage/perimetre_cadre.py` ne manipule que des triplets `(b, h, r)` (`CAS` et `CAS_CONNUS`) — il n'a **aucune connaissance** du comptage, de la règle d'axe ni des longueurs de barres, donc il n'attrape **aucun** des trois cas que la phrase lui attribue. **Réponse à la question posée : l'affirmation publiée est plus honnête qu'en passe 2 — la liste de ce qui est partagé est exacte — mais elle reste trop généreuse sur ce qui rattrape.** | Ajouter au test de rendu le recalcul indépendant de la **longueur de barre** (`L − 2e` depuis `data/`) comparé à `metre.longueur_barre_m` **et** à `diag.barres[i].longueur_m`, comme c'est déjà fait pour le comptage et les positions. Puis corriger la phrase : retirer « par l'étalonnage », et ne citer que les contrôles qui existent réellement. |
| **P3 · Le bloc économique, ajouté pour corriger N4, n'est contrôlé nulle part.** | **majeur** | Canari **D3** : `cout_acier_MAD_max = round(masse × prix[1] × 10)` → la page publie **6 188 MAD** au lieu de 619, et `npm run check` → **VERT, 11 contrôles**. `grep -rn "economie\|cout_acier\|heures_ferrailleur" calc/tests/ tests/ build/check.mjs` → **aucune occurrence**. Les valeurs actuellement publiées sont justes — je les ai recalculées (433,1–618,7 MAD ; 1,904–2,750 h) — c'est donc un trou de contrôle, pas une erreur vive ; mais le § 4.3 exige que « masse d'acier du métré = base du coût » soit une cohérence **testée**. | Ajouter à `test_cage.py` : coût = masse × prix recalculés depuis `data/ordres_de_grandeur`, heures = 8 × masse/cadence, bornes dans le bon ordre (min < max), et une mutation (prix × 10) qui doit faire échouer. |
| **P4 · Le balisage V3 du § 3.2 n'est plus exigé dès qu'une balise existe.** | **majeur** | `build/check.mjs:57-64` : le garde-fou sur les mentions ne se déclenche que si `mentions.length && !balises.length` — c'est-à-dire **uniquement quand il n'y a aucune balise**. Canari **D4** : j'ai ajouté en clair dans `content/00-demo-cage.md` « Le béton, lui, revient à **1 350 MAD/m³ (V3)** », sans balise ni ligne de registre. `npm run check` → **VERT, 11 contrôles**, la phrase est publiée telle quelle. Le § 3.2 veut que le build **échoue** si un nombre d'un bloc normatif n'est pas balisé ; la comparaison `balises.length !== hyp.length` ne le voit pas non plus, puisque le registre est généré **depuis** les balises et suit donc toujours. | Faire échouer sur toute mention « (V3 » hors balise, quel que soit le nombre de balises ; et, plus largement, signaler tout nombre suivi d'une unité monétaire ou d'une cadence hors balise et hors `{{variable}}` dans `content/`. |
| **P5 · Une des trois « cohérences internes » ajoutées est une tautologie pure.** | mineur | `calc/cage.py` : `"longueur_sur_n_fois_perimetre": round((per_A * n_cadres / 1000.0) / (n_cadres * per_A / 1000.0), 6)` — c'est **x / x**, identiquement **1.0** pour toute valeur de `per_A` et de `n_cadres`. Publié dans le bloc dont le `but` déclaré est « rapports qui **BOUGENT** quand une part du métré dérape ». Vérifié sous canari D5bis : `longueur_sur_n_fois_perimetre = 1.0` inchangé. *(Les deux autres sont bonnes : `perimetre_sur_coins_vifs` = 0,9821 réagit bien — un rayon absurde le sort de [0,90 ; 1,00] et le test le vérifie ; la masse linéique est explicitement présentée comme indicative.)* | Supprimer la ligne, ou la remplacer par un rapport qui ne se simplifie pas — par exemple la longueur développée recomptée depuis les positions `z` renvoyées par `placement_cadres`, qui, elle, bouge si le placement dérape. |
| **P6 · La colonne `valeur` de H001 ne contient pas la valeur.** | mineur | `data/registre-hypotheses.csv` : `H001;rayon de cintrage du cadre;**un paramètre de tracé**;mm;15 à 30;2026;…`. Le rayon qui porte 1,8 % du périmètre publié vaut **20 mm** et ce nombre n'apparaît nulle part dans sa propre ligne de registre. Conséquence visible à l'écran : la balise rend « pas un rayon minimal réglementaire — *un paramètre de tracé*^V3 », où un lecteur attend une valeur. (H002 à H005 recopient la fourchette dans `valeur`, ce qui est acceptable pour une hypothèse qui n'est qu'une fourchette.) | Mettre `20` dans `valeur` et déplacer « un paramètre de tracé » en `justification`, qui est sa place. |
| **P7 · Le contrôle des conventions est dissymétrique et facultatif.** | mineur | Python (`calc/cage.py:93-99`) vérifie **trois** règles : `enrobage_mesure_a`, `crochets_extremite`, `placement_cadres`. JavaScript (`src/civil3d/section.js:19-26`) n'en vérifie que **deux** : `placement_cadres` n'y est pas contrôlé, alors que c'est précisément la règle que D1 fausse. De plus l'appel est conditionnel : `armatures.js:36` fait `if (cadres.conventions) verifierConventions(cadres.conventions)` — un appelant qui omet le champ **saute silencieusement tout le contrôle**. Le site d'appel actuel le passe bien (`demoCage.js:30`), mais rien ne l'impose. | Ajouter la vérification de `placement_cadres` côté JS, et rendre le champ obligatoire : lever si `cadres.conventions` est absent plutôt que de passer outre. |
| **P8 · Quatre captures sur dix-neuf datent d'avant la refonte du spec (défaut N12 non corrigé).** | mineur | `ls -la --time-style=+%H:%M:%S tests/captures/` : la campagne courante date de **12:37:11–12:37:19** (15 états). Subsistent `00-demo-cage.html-curseurs-min.png` et `-curseurs-max.png` à **09:06:53** — produites par un spec qui ne les produit plus —, `index.png` à **09:00:21** et `figure1.png` à **09:22:42**. Un relecteur qui applique le § 9.4 (« capture de chaque état **examinée** ») examine quatre images périmées de plus de trois heures. | `rmSync(CAPTURES, { recursive: true, force: true })` avant le `mkdirSync` du spec. |
| **P10 · Le contrôle « dépôt git propre » passe au rouge dès que le relecteur fait son travail.** | mineur | Le § 12.2 **impose** au relecteur d'écrire `QA/NN-slug.md`. Dès que ce fichier existe et avant que l'auteur ne l'ait committé, `npm run check` tombe : reproduit à l'instant sur `5d3857f` avec le présent rapport — `ECHEC 5.2 · dépôt git : arbre de travail non propre : ?? QA/E1-socle-passe3.md`, qui entraîne en cascade `ECHEC k · mode B`, soit **2 échecs sur 11** dont la seule cause est le rapport de relecture lui-même. Le contrôle se déclenchera donc à chaque passe adversariale. (C'est la contrepartie de la correction de N6 ; le dépôt est par ailleurs propre, j'ai vérifié que rien d'autre n'est en cause.) | Exclure `QA/` du contrôle, comme le § 12.2 l'y invite (le rapport est produit *après* le livrable), ou n'y prendre en compte que les fichiers suivis (`git status --porcelain --untracked-files=no`). |
| **P9 · Les conventions sont comparées à la chaîne exacte, ce qui casse dans le mauvais sens.** | mineur | `cv.get("enrobage_mesure_a") != "peau exterieure du cadre"` : reformuler la convention en « peau extérieure du cadre » (avec accents) ou « à la peau du cadre » **fait tomber tout le build**, alors que la règle est la même. À l'inverse, le canari **D2** montre qu'un changement de code qui contredit la convention **passe** ce contrôle (il a été rattrapé ailleurs, par le recalcul indépendant). La chaîne est donc un verrou de version, pas une vérification sémantique. | Comparer à un identifiant stable (`enrobage_mesure_a: "peau_cadre"`) et garder la phrase française dans un champ `_note` voisin. |

---

## 4. Les 10 points du § 12.2

| # | Point | Constat |
|---|---|---|
| **1** | Unités et homogénéité | **RAS.** Treize valeurs recalculées en SI depuis `data/` seul, treize concordances (§ 1), y compris les deux nouvelles grandeurs économiques (MAD et heures). La vérification `pint` est alimentée par `data/` et **teste qu'une formule non homogène lève** (`COEF_TABULE * u.kg / u.mm**2`) : `une_formule_non_homogene_leve = true` dans la sortie. |
| **2** | Référentiels mélangés | **RAS.** `grep -onE "BAEL\|BPEL\|RPS ?2000\|Eurocode\|EN 199[0-9]\|NF ?P\|fck\|fe ?500"` sur `modules/00-demo-cage.html` et `index.html` → **aucune occurrence**. Aucun calcul réglementaire n'est conduit, donc aucun mélange possible. |
| **3** | Article cité sans V0 ni V1 | **RAS sur les articles** (`grep "art\.? ?[0-9]+"` → rien). Les 5 valeurs V3 publiées portent une balise structurée à six champs et une ligne de registre complète, et le build échoue si fourchette ou année manquent (`build.mjs:230`) — c'est une vraie correction. **Mais** le balisage n'est plus **exigé** : **P4**, prouvé par le canari D4. |
| **4** | Ordres de grandeur et ratios | **RAS, avec réserve.** Ratio recalculé par moi : **58,9279 kg/m³**, conforme. La tolérance du contre-calcul est passée de 5 % à **1 %** pour un écart de 0,077 % (marge 13× au lieu de 65×), et le vrai garde-fou est désormais `ecart_perimetre_pct < 0,05 %` dans le test, pour 0,0068 % observé. Le nouveau rapport `perimetre_sur_coins_vifs` (0,9821, borné [0,90 ; 1,00]) **réagit** réellement, et le test le vérifie par mutation (rayon 120 mm). Réserve : le garde-fou 30–250 reste assez large pour laisser passer D5bis (ratio 57,7). |
| **5** | Cohérence data / SVG / 3D / métré | **Nettement renforcée, un trou.** Vérifié par canaris : le diamètre du tube est mesuré (C3 rouge), les ordonnées et le rayon des cercles SVG sont comparés en absolu à une échelle déduite du **rectangle de section** (C4 et C6 rouges), le comptage est recalculé dans le test (C8 et D1 rouges), la règle d'axe aussi (D2 rouge). La tolérance 3D/`calc` est à 0,1 % sur la masse et 0,05 % sur le périmètre. **Reste non couvert : la longueur des barres** (**P2**, canari D5bis), et le lien métré → coût (**P3**, canari D3). |
| **6** | Grille de profondeur § 7.2 | **RAS.** La grille est dans `STATE.md:53`. Le lien coût/délai, que je notais 0/3 en passe 1, est maintenant **calculé** et non écrit : j'ai refait les deux bouts (433,1–618,7 MAD ; 1,904–2,750 h) et ils concordent avec la page. Le lien avec l'exécution reste porté par le phasage et par le point 4 de l'encart des simplifications. |
| **7** | Sécurité | **RAS.** Vérifié dans le HTML rendu : « Le coffrage modélisé n'a ni étaiement ni étais de reprise, et la phase 4 retire les panneaux sans dire à quelle condition. Dans la réalité, le décoffrage est subordonné à une résistance atteinte, contrôlée sur éprouvettes ; le décoffrage prématuré est l'un des pièges listés au § 7.3. Le sujet est traité au module d'exécution, en attente des normes. » Aucun conseil d'exécution dangereux ; la mention du § 3.4 est en pied de page. |
| **8** | Vérité du rendu | **RAS, hors P8.** `npm run check` → 11 contrôles verts, 7 tests Playwright, zéro erreur console, zéro requête externe. `etats.json` : 15 états, variance minimale **18,15** (seuil 8), **13 états sur 15** portent ≥ 3 étiquettes, **zéro chevauchement partout**, `pire-cas` à **111 728 triangles** (74,5 % du budget). J'ai ouvert les captures : les cadres ont désormais l'épaisseur d'un HA8 (B1 confirmé à l'œil et par la mesure du rayon du tube), la cage est contenue dans le béton, et à l'espacement minimal (7 cm, 29 cadres) la géométrie n'est pas dégénérée. Seule réserve : quatre captures périmées traînent (**P8**). |
| **9** | Simplifications non signalées | **RAS sur le fond, défaut de forme.** Les quatre simplifications sont déclarées, dans `data/` **et** dans la page : crochets absents (métré minorant d'environ 3 %), rayon de cintrage V3 avec fourchette, enrobage le long de l'axe, coffrage sans étaiement. J'ai revérifié le chiffrage des crochets (2 × 10 ⌀ = 160 mm/cadre → +2,8 %, cohérent avec « environ 3 % »). La forme, elle, est fautive : **P1**. |
| **10** | Texte télégraphique ou remplissage | **RAS sur la densité** — phrases complètes, chaque paragraphe porte un chiffre, une règle ou une méthode. L'anecdote d'étalonnage ne cite plus de valeurs figées (`grep "2,386\|1,926\|12,24\|9,88"` → **aucune occurrence**) : elle lit `{{metre-cage.perimetre_cadre_m}}` et `{{…ecart_perimetre_pct}}`, seul le « près de 24 % » historique subsiste, et il porte sur une version disparue qui ne peut plus dériver. **N5 corrigé.** Reste la correction inachevée « … non — » de **P1**. |

---

## 5. Synthèse et verdict

**10 défauts : 0 bloquant, 4 majeurs, 6 mineurs.**

Corrections **vérifiées par la mesure**, pas sur parole : **N1** (about réel recalculé à 30,00 mm
contre 26,0 sous l'ancienne règle), **N3** (registre à huit colonnes remplies, généré depuis les
balises, build qui échoue sans fourchette ni année), **N4** (coût et heures recalculés par moi,
433,1–618,7 MAD et 1,904–2,750 h, concordants), **N5** (plus aucune valeur figée dans l'anecdote),
**N6** (clone neuf : 11 contrôles verts, arbre propre après coup), **N7** et **N8** (C3, C4, C6
rouges, avec l'assertion exacte), ainsi que les mineurs sur les tautologies et la tolérance. Et
surtout : **D1 et D2 montrent que la parade du § 3.3 fonctionne** — une erreur de modèle *partagée*
entre Python et JavaScript, sur le placement comme sur la règle d'axe, est maintenant rattrapée par
le recalcul indépendant logé dans le test. C'est le progrès le plus réel des trois passes.

Les trois points les plus importants :

1. **Le filet annoncé a un trou, et la page annonce le trou au mauvais endroit (P2).** La phrase
   publiée cite trois erreurs communes aux deux voies et affirme qu'elles sont rattrapées « par
   l'étalonnage et par des tests qui recalculent… ». Deux le sont (D1, D2). La troisième, la longueur
   de barre, ne l'est pas : mon canari D5bis fait passer la masse de 30,94 à 30,30 kg et le coût de
   433–619 à 424–606 MAD sans allumer un seul des onze contrôles. Et l'étalonnage, qui ne manipule que
   des triplets (b, h, r), n'en rattrape aucune des trois. **Réponse à la question posée : l'affirmation
   est désormais honnête sur ce qu'elle partage, encore trop généreuse sur ce qui la rattrape.**
2. **Deux zones neuves sont livrées sans contrôle (P3, P4).** Le bloc économique accepte un coût
   multiplié par dix ; et le balisage V3 cesse d'être exigé dès qu'une seule balise existe, si bien
   qu'un prix inventé publié en clair passe. Les valeurs actuelles sont justes — je les ai
   recalculées — mais rien ne les y oblige.
3. **Le paragraphe qui annonce la correction de N1 est le seul de la page à publier un nombre faux
   (P1)** : « l'axe du premier cadre est à 20 mm près de l'about… non — », où 20 mm est le rayon de
   cintrage et la valeur juste est 34 mm, avec une auto-correction laissée dans le texte et un encart
   intitulé « Trois simplifications » qui en liste quatre.

### Zéro bloquant ? — **OUI.**

Aucun défaut bloquant au sens retenu depuis la passe 1 : **aucune erreur de calcul** (les treize
valeurs publiées sont exactes, recalculées indépendamment), **aucune erreur de sécurité** (la lacune
du décoffrage est comblée et vérifiée dans le rendu), **aucune incohérence entre modules** (SVG, 3D et
`calc/` concordent, et les six canaris de cohérence mordent), **aucune erreur de rendu** (11 contrôles
verts, 15 états capturés et examinés, diamètre du tube mesuré).

Je signale cependant que **P1 a été classé majeur par décision de proportion** : la phrase publie bien
un nombre faux, mais elle énonce la règle correcte dans le même souffle et aucune valeur calculée n'en
dépend. Si l'auteur juge qu'un nombre faux publié est bloquant par nature, ce classement se discute —
c'est à lui de trancher, pas au relecteur de l'absoudre.

Les quatre majeurs sont à corriger avant de clore l'Étape 1 (§ 12.2 : « les bloquants et majeurs sont
corrigés »). Une quatrième passe devra rejouer **D3, D4 et D5bis**, qui sont aujourd'hui les trois
canaris verts.

---

## Suites données par l'auteur — 15/10/2026

Les **4 majeurs** et les **6 mineurs** sont corrigés. Trois remarques :

1. **P1 est traité comme s'il était bloquant**, sans attendre l'arbitrage proposé. Une page qui publie
   un nombre faux est fausse, quelle que soit la gravité qu'on lui assigne — le § 2.1 met l'exactitude
   technique avant tout le reste. Le texte est repris, et l'encart compte maintenant ses quatre entrées.
2. **Le rejeu du canari D4 a d'abord donné un faux négatif de mon fait** : mon `sed` d'injection ne
   matchait pas (apostrophes typographiques), et j'ai lu « passe encore » là où rien n'avait été injecté.
   Injecté correctement, le contrôle P4 se déclenche. Le défaut était réel, la correction tient, mais
   mon harnais de rejeu était faux — ce qui est exactement le genre d'erreur que ces passes existent
   pour attraper, y compris chez le correcteur.
3. **P10 est corrigé en excluant `QA/`** du contrôle « dépôt propre ». Le contrôle virait au rouge par
   le seul fait d'être relu, puisque le relecteur écrit son rapport pendant la passe.
