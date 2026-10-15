# Passe adversariale « /devil » n° 2 — Étape 1, socle

Contre-relecture de l'état `3c0dfe4`, après correction annoncée des 5 bloquants et 9 majeurs de
`QA/E1-socle.md`. Mêmes règles : le raisonnement de l'auteur n'a pas été lu, la section 5 de
`QA/E1-socle.md` et `STATE.md` n'ont servi à juger aucune valeur, et tout a été **recalculé** à
partir de `data/demo-cage.json` seul avant d'ouvrir le moindre fichier de `calc/`.

Objet de cette passe : (a) vérifier chaque correction par la mesure, (b) **chercher ce que les
corrections ont cassé**.

Commandes exécutées : `npm run check` (11 contrôles verts sur `3c0dfe4`), `python3 calc/run_all.py`,
un recalcul indépendant, **neuf canaris** injectés dans une copie du dépôt (deux repris de la passe 1,
sept nouveaux), et l'examen des 15 captures de `tests/captures/`.

---

## 1. Contre-expertise à l'aveugle, refaite entièrement

Recalcul à partir des seuls paramètres et de la nouvelle section `conventions` de
`data/demo-cage.json` (axe du cadre à `enrobage + ⌀/2`, r = 20 mm, sans crochets, premier et dernier
cadre à l'enrobage).

| Grandeur | Mon recalcul indépendant | `metre-cage.json` | Page publiée |
|---|---:|---:|---:|
| Nombre de cadres — 1 + ⌈1940/150⌉ = 1 + ⌈12,933⌉ | **14** | 14 | 14 |
| Espacement réel — 1940/13 | **149,23 mm** | 14,92 cm | 14,9 cm |
| Rectangle d'axe du cadre — 350 − 2(30+4) | **282 × 682 mm** | 28,2 × 68,2 | — |
| Périmètre (formule fermée) | **1,89366 m** | 1,89366 (voie B) | 1,89 m |
| Périmètre (contour discrétisé) | **1,89353 m** | 1,89353 (voie A) | — |
| Longueur développée de cadres | **26,509 m** | 26,509 | 26,51 m |
| Masse des cadres | **10,461 kg** | 10,46 | 10,5 kg |
| Masse des barres | **20,477 kg** | 20,48 | 20,5 kg |
| **Masse totale** | **30,938 kg** | 30,94 | 30,9 kg |
| Ratio | **58,93 kg/m³** | 58,9 | 58,9 kg/m³ |
| Variante de l'exercice (7 cm) — 1 + ⌈1940/70⌉ | **29 cadres ; 42,14 kg ; Δ 11,2 kg** | 29 / 42,14 / 11,2 | idem |

**Concordance exacte sur les onze valeurs.** Les corrections de calcul sont confirmées par la mesure.

**Point 2 du mandat — enrobage réellement réalisé.** Je l'ai recalculé depuis la géométrie produite,
et non depuis la déclaration : peau extérieure du cadre à (350 − 282)/2 − 8/2 = **30,00 mm**, soit
exactement l'enrobage annoncé. **Le défaut B4 est corrigé dans le plan de la section** — mais pas le
long de l'axe de la poutre : voir **N1**.

**Point 6 du mandat — la règle « 14 cadres » est-elle juste ?** Oui, et c'est une vraie correction.
L'espacement nominal est un **maximum** : avec 13 cadres, l'espacement réel valait 1940/12 =
**161,7 mm pour un nominal de 150 mm**, ce que j'ai vérifié en rejouant l'ancienne règle. La nouvelle
(`1 + ⌈utile/nominal⌉`) donne 149,23 mm ≤ 150. Je l'ai éprouvée aux bornes des curseurs : L = 100 cm
et espacement 30 cm → 5 cadres à 235 mm ≤ 300 ; L = 400 cm et espacement 7 cm → 58 cadres à 68,6 mm
≤ 70. Aucun cas dégénéré. **Règle correcte, et le test d'invariant qui l'accompagne est un vrai
test** (canari C8 ci-dessous).

**Point 3 du mandat — diamètre du tube du cadre.** Mesuré dans le code produit :
`geometrieCadre(contour, dCad)` avec `dCad = mm(8) = 0,008 m`, puis
`TubeGeometry(courbe, segments, diametreBarre_m / 2, …)` → rayon 0,004 m, **diamètre 8 mm**. B1 est
corrigé. Mais rien ne l'empêche de revenir : voir **N7**.

---

## 2. Les neuf canaris (point 7 du mandat)

Protocole : copie du dépôt à `3c0dfe4`, un canari à la fois, `bundle` + `calc` + `build`, commit,
puis `npm run check`. Le `.pyc` versionné (défaut **N6**) a été neutralisé dans la copie, sinon il
faisait échouer le contrôle « dépôt git propre » à chaque canari et masquait le signal.

| # | Canari injecté | Résultat | Attrapé par |
|---|---|---|---|
| **C1** | *(passe 1)* barres du SVG empilées au même point | **détecté** | `rendu.spec.mjs` — « position horizontale des barres en SVG » |
| **C2** | *(passe 1)* enrobage ignoré en 3D | **détecté** | test de géométrie SVG + 3D |
| **C3** | **régression de B1** : tube du cadre redivisé (`/4`) | **PASSE, non détecté** | — |
| **C4** | barres du SVG décalées de 10 cm en hauteur | **PASSE, non détecté** | — |
| **C5** | règle de placement divergente Python/JS (13 côté `calc/`) | **détecté** | « métré 3D 30.937 kg contre calc/ 30.19 kg » + test d'invariant |
| **C6** | barres du SVG resserrées de 20 % vers l'axe | **PASSE, non détecté** | — |
| **C7** | périmètre majoré de 50 % côté Python | **détecté** par le contre-calcul (14,4 % > 5 %) — mais **pas** par le contrôle de « cohérence interne », resté vert | contre-calcul seul |
| **C9** | terme droit de la formule fermée faussé (`h − 2r` → `h − r`), pour éprouver le **nouvel** étalonnage (point 5 du mandat) | **détecté** | étalonnage : écart **2,11 %** sur le cadre de la démonstration, 4,14 % sur le cadre carré, et le cas « cercle » tombe à 496,99 mm contre 376,99 attendus. L'ancien étalonnage, qui recopiait ce terme, ne pouvait pas le voir. |
| **C8** | **erreur de modèle partagée** : règle de comptage fausse **des deux côtés** | **détecté** par le seul test d'invariant « l'espacement réel ne dépasse pas le nominal » — le **contre-calcul est resté « OK » à 0,077 %** | invariant |

Trois canaris sur neuf franchissent les onze contrôles. C'est trois fois moins qu'à la passe 1, mais
les trous restants sont précis et nommés ci-dessous (**N7**, **N8**).

---

## 3. Défauts

| défaut | gravité | preuve | correction proposée |
|---|---|---|---|
| **N2 · La page affirme une indépendance des deux voies qu'elle n'a pas, et se contredit elle-même.** Le corps du § « Le métré » écrit : « **Les deux voies ne partagent ni le chemin de longueur, ni le chemin de masse.** » C'est vrai pour la longueur (vraie correction), **faux pour la masse**. | **bloquant** | Voie A : masse/m = (π/4)·d²·ρ = **0,0061654**·d². Voie B : **0,00617**·d². Rapport B/A = 1,000750, soit **0,0750 % constant, quelles que soient la longueur et la géométrie** — c'est exactement l'écart publié (0,077 %, le complément venant des 0,0068 % du périmètre). Le chemin de masse est **identique à celui de la version d'avant**, que l'encart situé douze lignes plus bas qualifie lui-même de « pas un contre-calcul ». De plus les deux voies partagent toujours `n_cadres`, la règle d'axe `bc/hc`, `long_barre_m` et le nombre de barres : canari **C8**, règle de comptage fausse des deux côtés → masse fausse de 2,4 %, **verdict du contre-calcul « OK », écart 0,077 %**. Enfin l'affirmation n° 3 en tête de page dit toujours « deux voies **indépendantes** ». | Soit une vraie seconde voie de masse (masse linéique tabulée par diamètre, HA8 = 0,395 kg/m etc., saisie comme table et non recalculée), soit écrire ce qui est vrai : « les deux voies divergent sur la longueur ; la masse suit la même relation, à l'arrondi de la constante près ». Et faire porter le contre-calcul sur `n_cadres` (p. ex. longueur totale de cadres recomptée depuis les positions `z`). |
| **N1 · La convention d'enrobage n'est appliquée que dans le plan de la section, pas le long de la poutre.** `src/civil3d/section.js:59` : `z.push(-L_cm / 2 + enrobage_cm + i * espacement_reel)` — c'est l'**axe** du cadre qui est posé à l'enrobage de l'about. | **majeur** | La convention publiée dans `data/demo-cage.json` dit : « L'axe du cadre est donc à **enrobage + dia_cadre/2** de la peau du béton ». Appliquée en b et en h, pas en z. Enrobage d'about réellement réalisé : 30 − 8/2 = **26 mm** au lieu de 30, pendant que la scène 3D porte l'étiquette « enrobage 3 cm ». C'est le défaut B4 de la passe 1, survivant dans la troisième dimension. **Je ne le classe pas bloquant** : le métré n'est pas touché (ni le nombre de cadres ni leur longueur n'en dépendent) et aucune valeur publiée n'est fausse — seule l'étiquette globale l'est. | `z = -L/2 + enrobage + dCad/2 + i·espacement_reel`, avec `utile = L - 2(enrobage + dCad/2)`. Ajouter au test de rendu l'assertion symétrique de celle qui existe déjà pour b : enrobage d'about réalisé = enrobage annoncé. |
| **N3 · Le registre des hypothèses est rempli dans les mauvaises colonnes, et les deux colonnes exigées par le § 3.2 sont vides.** | **majeur** | En-tête : `id;hypothese;valeur;unite;fourchette;annee_ref;modules;justification`. Ligne produite : `H001;fourchette plausible 15 à 30 mm, année 2026;;;;;E1-demo;rayon de cintrage`. Donc `hypothese` contient la **valeur**, `justification` contient le **nom** de l'hypothèse, et `valeur`, `unite`, **`fourchette`** et **`annee_ref`** sont **vides** — alors que le § 3.2 exige une V3 « inscrite dans `registre-hypotheses.csv` **avec fourchette et année de référence** ». Les 5 lignes sont toutes dans ce cas. Le contrôle de `check.mjs` ne compare que des **comptes** (`balises.length !== hyp.length`), jamais le contenu : 5 = 5, donc vert. | Donner à la balise une forme structurée (`⟦V3|id|valeur|unité|fourchette|année⟧`) et faire écrire au build chaque champ dans sa colonne ; faire échouer `check.mjs` si `fourchette` ou `annee_ref` est vide. |
| **N4 · Le paragraphe de coût ajouté pour combler m8 contient un nombre tapé à la main, et il est faux.** `content/00-demo-cage.md:167` : « de l'ordre de **450 à 620 MAD** d'acier ». | **majeur** | La masse voisine est bien une variable (`{{metre-cage.masse_acier_kg::n1}}` = 30,9 kg), mais le produit est saisi. Recalcul depuis les valeurs de la page : 30,94 × 14 = **433,2 MAD**, 30,94 × 20 = **618,8 MAD**. La borne publiée 450 implique une masse de **32,14 kg**, la borne 620 une masse de **31,00 kg** : les deux bornes ne sortent **pas de la même masse**, et aucune des deux ne sort de la masse publiée. Violation R1/§ 4.3 sur la page même qui écrit « chaque nombre est une variable produite par `calc/cage.py` ». | Calculer l'intervalle dans `calc/` (`cout_min_MAD`, `cout_max_MAD`) et l'injecter par variables, comme l'exercice l'a déjà été. |
| **N5 · L'encart « Ce que l'étalonnage a réellement attrapé » publie des chiffres périmés qui contredisent le tableau situé juste au-dessus.** | **majeur** | Texte publié : « Le périmètre sortait à 2,386 m au lieu de **1,926 m** […] et la masse de cadres à 12,24 kg au lieu de **9,88 kg** ». Or 1,926 m et 9,88 kg sont les valeurs de **l'ancienne convention d'enrobage**, abandonnée par la correction de B4. Le tableau de la même page affiche désormais **1,89 m** et **10,5 kg**. Quatre nombres techniques tapés à la main (`grep -onE` sur `content/`), dont deux faux depuis la correction. | Soit variabiliser l'anecdote, soit la dater explicitement (« avant la correction de la convention d'enrobage, le périmètre de référence valait 1,926 m »), soit la retirer : un récit d'historique n'a pas à porter des chiffres qui dérivent. |
| **N6 · Un `.pyc` est versionné et `__pycache__` n'est pas ignoré : le nouveau contrôle « dépôt git propre » échoue sur tout clone neuf.** | **majeur** | `git ls-files \| grep pycache` → `calc/__pycache__/cage.cpython-313.pyc` est **suivi**. `cat .gitignore` → `node_modules/`, `tests/captures/`, `*.zip`, `.DS_Store`, `test-results/` — **pas de `__pycache__/`**. Reproduit : j'ai extrait `3c0dfe4` par `git archive` dans un répertoire neuf, puis lancé `npm run check` → `ECHEC 5.2 · dépôt git : arbre de travail non propre : M calc/__pycache__/cage.cpython-313.pyc`, **2 échecs sur 11**. Python recompile dès que la mtime de la source change, c'est-à-dire à tout clone, et un lecteur sur Python 3.12 ou 3.14 produira en plus un fichier `cpython-312/314` non suivi. C'est exactement le scénario de reprise du mode B (§ 12.5 B2). Le contrôle M8 corrigé se retourne donc contre le lecteur. | `git rm --cached -r calc/__pycache__` et ajouter `__pycache__/` à `.gitignore`. (Le contrôle `k` ne l'a pas vu parce que `unzip` restitue les mtimes du zip.) |
| **N7 · Le défaut B1 peut revenir en silence : aucun test ne mesure le diamètre du tube du cadre.** | **majeur** | Canari **C3** : `diametreBarre_m / 2` → `/ 4` dans `src/civil3d/armatures.js`, soit le bug d'origine à l'identique (HA8 dessiné en HA4). Résultat : **`VERT — 11 contrôles passés`**. Le diagnostic n'expose ni le rayon du tube ni le diamètre du cadre (`grep` sur `scene.js` : seuls `barres`, `axeCadre`, `triangles` le sont), et le métré repart du diamètre nominal, donc la comparaison 3D/`calc` est aveugle. | Exposer `diaCadreDessine_mm` dans `diagnostic()` (depuis `geoCad.parameters.radius`) et l'asserter contre `data/demo-cage.json` dans le test de géométrie, à côté des positions de barres. |
| **N8 · Le test de géométrie du SVG ne regarde que les abscisses, et il recale lui-même son échelle sur les barres qu'il contrôle.** | **majeur** | `tests/rendu.spec.mjs` : `k = (max(cxs)−min(cxs))/(max(xs)−min(xs))` puis `ox = min(cxs) − min(xs)·k`. Échelle **et** origine sont déduites des cercles mesurés : toute homothétie ou translation du groupe de barres est absorbée. Et `cy` n'est **jamais** comparé. Deux canaris le prouvent : **C4** (toutes les barres décalées de 10 cm vers le haut — elles sortent du cadre et se retrouvent à mi-hauteur) → **VERT, 11 contrôles** ; **C6** (barres resserrées de 20 % vers l'axe, soit un enrobage dessiné de 8 cm au lieu de 4,8) → **VERT, 11 contrôles**. Le test 3D, lui, est absolu (0,001 cm) et vérifie l'enrobage réalisé : c'est le SVG qui est sous-contrôlé. | Caler l'échelle sur le **rectangle de béton** (dont les coordonnées sont connues depuis `data/` et le `viewBox`), pas sur les barres, puis comparer `cx` **et** `cy` en absolu, plus le rayon des cercles contre `dia_mm/2`. |
| **N9 · Deux nouvelles assertions tautologiques, dans le fichier dont l'en-tête dit « une assertion qui ne peut pas échouer ne vaut rien ».** | mineur | (a) `coherence_interne` : `masse_par_metre = masse_cadres_A / (per_A·n/1000)` et `masse_cadres_A = aire·1e-6·(per_A·n/1000)·rho`, donc le quotient vaut **identiquement** `aire·1e-6·rho`, qui est l'`attendu`. Prouvé par le canari **C7** : périmètre majoré de 50 %, masse publiée fausse de 19 % (36,17 kg) → `ok masse lineique des cadres conforme a la geometrie — 0.3946 kg/m`. (b) `test_cage.py`, « le comptage décrit le placement : (n−1) × espacement réel = longueur utile » : `espacement_reel = utile/(n-1)` par définition, donc l'égalité est vraie pour **tout** n. Prouvé par **C8** : avec 13 cadres au lieu de 14, cette assertion reste `ok` (c'est la suivante, sur le dépassement du nominal, qui attrape). | Supprimer (a) ou la remplacer par un rapport qui ne se simplifie pas (masse des cadres / masse des barres contre une valeur recalculée depuis `data/`). Supprimer (b), redondante avec le test de non-dépassement qui, lui, mord. |
| **N10 · L'assertion « les deux voies suivent deux chemins différents » est satisfaite par n'importe quel écart.** | mineur | Elle teste `perimetre_voie_A_m != perimetre_voie_B_m`. Sortie du canari **C7** : `ok les deux voies suivent deux chemins de longueur differents — A 2.8403 m / B 1.89366 m`, c'est-à-dire **50 % d'écart déclaré conforme**. Un test de différence n'est pas un test d'accord. | La remplacer par un encadrement à deux bornes : l'écart doit être **non nul et inférieur à 0,05 %**. |
| **N11 · La tolérance du contre-calcul reste sans effet.** | mineur | `tolerance_pct: 5.0` pour un écart observé de **0,077 %**, soit 65 fois la marge. Le canari **C7** a dû fausser le périmètre de 50 % pour la franchir. Entre les deux, toute la gamme des erreurs géométriques plausibles passe. | Resserrer à 0,2 % — l'écart est désormais structurel (arrondi de la constante) et donc prévisible. |
| **N12 · Deux captures périmées traînent dans `tests/captures/`.** | mineur | `ls -la --time-style=+%H:%M:%S` : `curseurs-min.png` et `curseurs-max.png` datent de **09:06:53**, les treize autres de **09:32:4x**. Le nouveau spec ne produit plus ces deux états (il produit `L_cm-min/max`, `esp_cm-min/max`, `n_inf-…`, `dia_inf-…`, `pire-cas`). Un relecteur qui applique le § 9.4 « capture de chaque état examinée » examinera deux images qu'aucun test ne produit plus. | Vider `tests/captures/` au début du spec (`rmSync(CAPTURES, {recursive:true})` avant `mkdirSync`). |
| **N13 · Le titre et l'affirmation n° 4 décrivent l'étalonnage à l'envers.** | mineur | Affirmation n° 4 : « La routine géométrique est **calée sur une solution analytique fermée** » ; titre de section : « L'étalonnage, sur une solution fermée ». Or le corps décrit exactement l'inverse, et c'est la bonne version : c'est **la formule fermée qui est l'objet étalonné**, contre une polygonalisation indépendante et deux cas à solution connue. L'énoncé en tête décrit la version creuse corrigée. | « La formule fermée est étalonnée contre une polygonalisation indépendante et deux cas à solution connue. » |
| **N14 · La « règle unique » est en réalité écrite quatre fois ; et la moitié de la section `conventions` n'est lue par aucun code.** | mineur | Transcriptions parallèles Python ↔ JS, vérifiées par `grep` sur les définitions : `placement_cadres`/`placementCadres` (`cage.py:71` / `section.js:51`), `contour_cadre`/`contourCadre` (`:42` / `:70`), `perimetre_cadre_ferme`/`perimetreCadreFerme` (`:33` / `:64`), plus la règle d'axe `b − 2(e + d/2)` écrite dans `cage.py`, dans `section.js` **et** une troisième fois dans `rendu.spec.mjs` (là, délibérément, et c'est justifié). Par ailleurs `grep` montre que `enrobage_mesure_a` et `crochets_extremite` ne sont **lus par aucun fichier** : ce sont des chaînes de documentation ; seul `rayon_cintrage_mm` est réellement consommé. Remplacer « peau extérieure du cadre » par « axe du cadre » dans `data/` ne changerait **rien** au produit. | Accepter la double écriture Python/JS (elle est inévitable) mais ajouter un test qui compare les **sorties** des deux implémentations point par point (le contour échantillonné, pas seulement le périmètre) ; et soit faire lire `enrobage_mesure_a` par `section.js` comme un sélecteur de convention, soit le marquer `_note_` comme les autres champs documentaires. |

---

## 4. Les 10 points du § 12.2

| # | Point | Constat |
|---|---|---|
| **1** | Unités et homogénéité | **RAS.** Les onze valeurs recalculées en SI concordent au dernier chiffre (§ 1). La vérification `pint` est désormais alimentée par `data/` et **teste qu'une formule non homogène lève** (`COEF_TABULE * u.kg / u.mm**2`, sans le « par mètre », doit produire une `DimensionalityError`) : j'ai vérifié que ce chemin est réellement exécuté et que `une_formule_non_homogene_leve` vaut `true`. La tautologie `str(units)=="kilogram"` subsiste dans le `verdict`, mais elle n'est plus seule. |
| **2** | Référentiels mélangés | **RAS.** `grep -onE "BAEL\|BPEL\|RPS ?2000\|Eurocode\|EN 199[0-9]\|NF ?P"` sur `modules/00-demo-cage.html` et `index.html` → **aucune occurrence**. Aucun calcul réglementaire n'est conduit. |
| **3** | Article cité sans V0 ni V1 | **RAS sur les articles** (`grep "art\.? ?[0-9]+"` → rien). La fuite de la passe 1 est traitée : le rayon de cintrage est sorti du code, mis dans `data/`, balisé `⟦V3⟧`, et sa note dit explicitement que **ce n'est pas une règle de cintrage minimal** — la seule occurrence de « cintrage minimal » dans le HTML est cette négation, à l'intérieur du JSON embarqué. **Mais** le registre qui doit recevoir ces V3 est malformé : **N3**. |
| **4** | Ordres de grandeur et ratios | **N11, et le garde-fou reste large.** Ratio recalculé par moi : **58,93 kg/m³**, conforme. Le garde-fou 30–250 est inchangé : le canari **C7** (périmètre +50 %, ratio 68,9) l'a franchi sans bruit. Le contrôle de « cohérence interne » ajouté pour le compléter est tautologique (**N9a**). Le constat honnête sur la fourchette 80–150 est conservé et correctement présenté comme non bloquant. |
| **5** | Cohérence data / SVG / 3D / métré | **Très améliorée, deux trous.** Vérifié : SVG et 3D consomment la même routine `section.js` (canari **C1** désormais attrapé) ; le métré 3D et celui de `calc/` sont comparés à **0,1 % sur la masse et 0,05 % sur le périmètre**, et le canari **C5** (divergence Python/JS) est attrapé avec le message « métré 3D 30.937 kg contre calc/ 30.19 kg ». Restent : le diamètre du tube (**N7**) et la géométrie verticale du SVG (**N8**). |
| **6** | Grille de profondeur § 7.2 | **RAS.** La grille existe maintenant (`STATE.md:53`) et le lien coût/délai, absent à la passe 1, est écrit — j'ai vérifié sa cohérence interne : passer de 15 à 7 cm multiplie le nombre de cadres par 2,07 et la masse par 1,36, ce qui **soutient effectivement** la phrase « resserrer les cadres coûte proportionnellement plus en main-d'œuvre qu'en acier ». La cadence est juste aussi : 30,94 kg à 90–130 kg/j = 0,24 à 0,34 jour, soit bien « quelques heures ». Mais le chiffre de coût lui-même est faux : **N4**. |
| **7** | Sécurité | **RAS.** La lacune m9 est comblée et bien comblée : `content/00-demo-cage.md:53-55` dit que le coffrage modélisé n'a **ni étaiement ni étais de reprise**, que la phase 4 retire les panneaux sans énoncer de condition, que le décoffrage est subordonné à une résistance contrôlée sur éprouvettes, et renvoie au piège du § 7.3. Aucun conseil d'exécution dangereux ; mention § 3.4 présente en pied de page. |
| **8** | Vérité du rendu | **RAS, et nettement mieux.** `npm run check` → 11 contrôles verts, 7 tests Playwright. J'ai ouvert les 15 captures. L'éclaté est maintenant pris à la **phase 3** et montre bien les **trois** couches (coffrage en bas, béton en haut, cage en place) — m4 corrigé, vérifié à l'image. `etats.json` : variance minimale **18,3** pour un seuil relevé à 8 ; **13 états sur 15 portent ≥ 3 étiquettes** et le spec exige qu'au moins un le fasse ; `pire-cas` atteint **111 728 triangles, soit 74,5 % du budget** de 150 000 (contre 18 % à la passe 1) — m1 corrigé et le budget réellement éprouvé. Aucun chevauchement, aucune géométrie dégénérée aux bornes, aucune erreur console. |
| **9** | Simplifications non signalées | **RAS.** Les trois simplifications que je reprochais sont déclarées : `crochets_extremite: false` avec la note « le métré est **minorant d'environ 3 %** » (reprise dans `metre-cage.json` **et** dans la sortie des tests) ; `rayon_cintrage_mm: 20` publié avec sa fourchette V3 ; la convention d'enrobage publiée et vérifiée par un test. J'ai revérifié mon chiffrage des crochets : 2 × 10 ⌀ = 160 mm/cadre → +2,8 %, cohérent avec « environ 3 % ». **Sauf** que la convention publiée n'est pas tenue dans la troisième dimension : **N1**. |
| **10** | Texte télégraphique ou remplissage | **RAS sur la forme**, phrases complètes, chaque paragraphe porte un chiffre ou une méthode. **Deux contradictions internes** : l'affirmation n° 3 et la phrase « ni le chemin de longueur, ni le chemin de masse » contre l'encart qui les dément (**N2**) ; l'affirmation n° 4 contre le corps du § étalonnage (**N13**). Les encarts rétrospectifs se sont multipliés (« La première version de ce contre-calcul n'en était pas un », « Ce que l'étalonnage a réellement attrapé ») : c'est pédagogiquement défendable, mais c'est aussi par là que les chiffres périmés entrent (**N5**). |

---

## 5. Synthèse et verdict

**14 défauts : 1 bloquant, 7 majeurs, 6 mineurs.**

Ce qui a été **réellement corrigé**, vérifié par la mesure et non sur parole : B1 (tube mesuré à
Ø 8 mm), B2 et B3 (routine unique, canari C1 désormais attrapé), B4 **dans le plan de la section**
(enrobage réalisé recalculé à 30,00 mm), M1, M3 (pour « treize » et l'exercice), M4 (vrais tests par
mutation), M5 (canari C9 ci-dessus : une erreur sur le terme droit de la formule fermée est maintenant détectée,
écart 2,11 % — l'ancien étalonnage ne la voyait pas), M9, M10, et les onze mineurs m1 à m11. Le
passage de 13 à 14 cadres est une **vraie trouvaille de l'auteur** et la règle est correcte : je l'ai
revérifiée aux bornes des curseurs.

Les trois points les plus importants :

1. **Le contre-calcul n'est indépendant que sur la longueur.** Le chemin de masse est resté celui que
   la page elle-même qualifie de « pas un contre-calcul » : 0,00617 contre π/4·7850·10⁻⁶ = 0,0061654,
   soit 0,0750 % d'écart structurel. Et les deux voies partagent toujours le nombre de cadres : mon
   canari C8 fausse ce nombre des deux côtés et le verdict reste « OK, 0,077 % ».
2. **Deux corrections se sont retournées.** Le contrôle « dépôt git propre » ajouté pour M8 échoue sur
   tout clone neuf à cause d'un `.pyc` versionné (reproduit : 2 échecs sur 11) ; et le paragraphe de
   coût ajouté pour combler m8 réintroduit un nombre tapé à la main qui est faux (450 MAD là où les
   données de la page donnent 433).
3. **Trois canaris sur neuf passent encore** : le diamètre du tube du cadre n'est mesuré par aucun test,
   donc B1 peut revenir en silence ; et le test de géométrie du SVG ignore les ordonnées et recale son
   échelle sur les barres qu'il contrôle, donc un décalage vertical de 10 cm ou un resserrement de 20 %
   passent au vert.

### Zéro bloquant ? — **NON.**

Il reste **un bloquant** : **N2**. Le § 3.3 exige deux voies indépendantes ; elles ne le sont que sur
un facteur sur deux, le produit publié affirme le contraire en toutes lettres, et le canari C8 montre
qu'une erreur de modèle partagée traverse le contrôle sans l'allumer. Les sept majeurs — dont deux
régressions introduites par les corrections (**N4**, **N6**) et deux trous de test démontrés par
canari (**N7**, **N8**) — sont à traiter avant de considérer l'Étape 1 close. Une troisième passe est
nécessaire ; elle devra rejouer au minimum les canaris C3, C4, C6 et C8.
