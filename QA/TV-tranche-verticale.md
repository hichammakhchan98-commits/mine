# Passe adversariale « /devil » — Étape 2, tranche verticale de suivi (module témoin n° 1)

Relecture hostile de `modules/01-tranche-verticale-suivi.html` (HEAD `465d071`). Le raisonnement de
l'auteur n'a pas été lu : les cinq valeurs clés ont été recalculées depuis `data/projet-gare.json`
seul, avec ma propre arithmétique, **avant** d'ouvrir le moindre fichier de `calc/`.

Exécuté : `npm run check` (12 contrôles verts), recalcul indépendant, **huit réseaux CPM construits
pour mettre le moteur en défaut**, **six canaris** sur la chaîne du module, et le rendu des cinq
figures (aucune n'est capturée par les tests : je les ai produites moi-même avec Playwright).

C'est le module que le lecteur doit valider avant duplication. Le compte rendu est sévère en
conséquence.

---

## 1. Contre-expertise à l'aveugle

| # | Grandeur | Mon recalcul indépendant | Publié | |
|---|---|---:|---:|---|
| **1** | Zone 15 × 24 m | **360 m²** | 360 | ✓ |
| | Béton : 360 × 0,25 + 2 × 24,00 × 0,35 × 0,50 | **90,0 + 8,40 = 98,40 m³** | 98,4 | ✓ |
| | Coffrage : (360 − 2×24×0,35) + 2×2×24×0,50 + 2×24×0,35, +4 % | **343,2 + 48,0 + 16,8 = 408,0 → 424,3 m²** | 424,3 | ✓ |
| | **Ratio coffrage/surface** | **1,1787** | 1,179 | ✓ |
| **2** | Acier : 80 × 90,0 + 180 × 8,40 | **8 712 kg** | 8 712 | ✓ |
| | Fourchette : 65–100 et 140–220 kg/m³ | **7 026 à 10 848 kg (étendue 43,9 %)** | 7 026 / 10 848 / 43,9 | ✓ |
| **3** | Durées : 424,3/(30×8) ; 1512/(150×4) ; 7200/(300×8) ; 98,4/30/8 | **1,768 · 2,520 · 3,000 · 0,410 j** | 1,77 · 2,52 · 3,00 · 0,41 | ✓ |
| | Cycle (chemin 2,40+3,00+0,25+0,41+2,00+0,50) | **8,56 j** ; somme 10,45 ; **gain 1,89 j = 18,1 %** | 8,557 / 10,45 / 1,89 / 18,1 | ✓ |
| **4** | Coût : 98,4×1250 + 8712×17 + 424,3×180 | **123 000 + 148 104 + 76 374 = 347 478 MAD** | 347 478 | ✓ |
| | Au m² | **965,2 MAD/m²** | 965 | ✓ |
| **5** | CPI = 3,6×347 478 / 1 330 000 | **0,9406** | 0,941 | ✓ |
| | SPI = 3,6/4 | **0,9000** | 0,900 | ✓ |
| | EAC = BAC/CPI = 2 779 824/0,9406 | **2 955 556 MAD** (dérive +175 732) | 2 955 556 / 175 732 | ✓ |
| | Voie B : 352×1250 + 30 900×17 + 1 515×180 | **1 238 000 MAD → 3,563 zones** | 1 238 000 / 3,56 | ✓ |

**Dix-neuf valeurs recalculées, dix-neuf concordances.** Le nombre de poutres par zone (2) se recoupe
par deux chemins : 15,0/7,50 = 2, et `nb_travees_longitudinales` 16 ÷ 8 zones = 2. Le moteur de calcul
fait ce qu'il annonce.

**Les erreurs de ce module ne sont donc pas dans `calc/` : elles sont dans le texte publié, dans les
figures, dans le moteur CPM hors du domaine utilisé, et dans ce que les contrôles ne regardent pas.**

---

## 2. Les huit réseaux CPM, et les six canaris

### 2.1 Mise en défaut du moteur CPM (`calc/cpm.py`)

Huit réseaux construits à la main, avec la durée connue d'avance :

| Réseau | Durée juste | Voie A | Voie B | Verdict rendu |
|---|---:|---:|---:|---|
| A(10 j) → B(1 j), décalage **−10** | **10** | 10 ✓ | **1** ✗ | « ECART — le parcours avant/arrière est faux » |
| A(10 j) → B(1 j), décalage **−20** | **10** | 10 ✓ | **−1,0** ✗ | idem |
| A(2 j) → B(5 j), décalage **−10** | — (début de B à −8) | 2 | **−1,0** ✗ | idem |
| Jalons de durée nulle en chaîne | 5 | 5 ✓ | 5 ✓ | OK |
| Deux départs, deux fins | 8 | 8 ✓ | 8 ✓ | OK |
| Tâche isolée de 100 j | 100 | 100 ✓ | 100 ✓ | OK |
| C après A(5) et B(5) décalage −50 | 6 | 6 ✓ | 6 ✓ | OK |
| Réseau entièrement à durée nulle | 0 | 0 ✓ | 0 ✓ | OK |

Les quatre cas de `cpm_cas_ferme.py` (chaîne, branches parallèles, recouvrement de 2 j sur une tâche
de 4 j, tâche isolée) **n'entrent jamais dans le régime où le moteur casse** : leur seul décalage
négatif vaut −2 pour une tâche de 4 j.

### 2.2 Canaris sur la chaîne du module

| # | Canari | Résultat |
|---|---|---|
| **T1** | quantités : béton de dalle majoré de 20 % | **détecté** — « volume de béton recalculé à la main » |
| **T2** | durées : ferraillage de dalle divisé par l'effectif des **poutres** (4 au lieu de 8) | **PASSE, non détecté** |
| **T3** | CPM : le parcours avant prend le `min` des prédécesseurs | **détecté** — étalonnage, « deux branches parallèles » |
| **T4** | coût : l'acier facturé au prix du béton | **détecté** — « CPI dans une plage plausible » |
| **T5** | valeur acquise : voie B ramenée à sa forme tautologique | **détecté** — « la voie B ne dépend pas de l'avancement déclaré » |
| **T6** | rendement d'équipe = 190 m²/j, **bas de sa propre fourchette V3 [190, 280]** | **détecté** — contre-calcul hors tolérance |

T5 confirme que **la correction du contre-calcul de valeur acquise tient** et qu'elle est gardée par
un test. T6 n'est pas une bonne nouvelle : voir **M3**.

---

## 3. Défauts

| défaut | gravité | preuve | correction proposée |
|---|---|---|---|
| **B1 · Le paragraphe « Le piège du coffrage » publie un chiffre faux, deux fois, et c'est un accident de gabarit.** | **bloquant** | Rendu : « Prendre 1,00 au lieu de 1,18, c'est sous-estimer le poste de **40 % environ** ». Source : `content/01-…md` écrit `{{…coffrage_detail_m2.rives_pct::n0}}0 %` — la variable vaut **4**, le « 0 » littéral se colle derrière, et la page affiche **40 %**. La valeur juste : prendre 1,00 au lieu de 1,1787 sous-estime de (1,1787 − 1)/1,1787 = **15,2 %** (17,9 % rapporté à la valeur sous-estimée). L'erreur est **publiée deux fois** : ici, et dans le tableau S5 (« ~{{…rives_pct::n0}}0 % du poste le plus cher »). Un paragraphe qui enseigne à ne pas sous-estimer un poste publie une sous-estimation fausse d'un facteur 2,6. | Remplacer par une variable calculée dans `calc/` (`sous_estimation_coffrage_pct`), et interdire au build la concaténation d'un chiffre littéral derrière une variable. |
| **B2 · Le corrigé de l'exercice 2 affiche une division fausse, et l'erreur se propage jusqu'à inverser la recommandation d'ingénierie de l'exercice 3.** | **bloquant** | Rendu de l'exercice 2 : « La durée passe de 3,00 j à **7200 / (300 × 12) = 2,42 j**, soit 0,58 j de moins ». Or **7200/3600 = 2,00 j**, et le gain réel est de **1,00 j**. L'opération est écrite à côté du résultat : le lecteur voit les deux. L'erreur se propage : l'exercice 3 écrit « Passer de 8 à 12 ferrailleurs ramène la cadence de 3,4 à environ **2,8 j** » — or la règle du module (`cycle_plancher.py:163`, `max(coffrage, ferraillage_dalle) + bétonnage`) donne `max(1,77 ; 2,00) + 0,41 = 2,41 → **2,4 j**` ; 2,8 n'est obtenu qu'en repartant du 2,42 faux. Conséquence : le module conclut **« Insuffisant »** et recommande de **dédoubler le front avec un second jeu de coffrage**, alors qu'avec la valeur juste la durée vaut 7 × 2,4 + 8,557 = **25,4 j**, soit la cible de 25 jours. **Une erreur d'arithmétique renverse la réponse technique**, dans le module que le lecteur doit valider avant duplication. | Faire calculer la variante par `calc/` (comme l'a été `variante_exercice` du socle) et l'injecter par variables ; aucun corrigé chiffré ne doit être saisi. |
| **B3 · La courbe en S (figure 5) contredit le tableau de valeur acquise du même module, et sa légende affirme une égalité fausse.** | **bloquant** | À la date d'arrêt (18,8 j), **le tableau S6** donne VP/BAC = **50,0 %**, VA/BAC = **45,0 %**, SV = −138 991 MAD = **5,0 points**. **La figure 5** donne, par interpolation de `figures.courbe_s`, prévu = **59,9 %**, réalisé = **51,9 %** (dernier point à j = 18,2, donc la courbe s'arrête *avant* la date d'arrêt), écart vertical = **8,0 points**. Soit ~10 points d'écart sur le prévu, ~7 sur l'acquis, et un écart vertical qui vaut 1,6 fois SV — alors que la légende publiée affirme : « L'écart vertical à la date d'arrêt est le retard en valeur, pas en jours : **c'est SV**. » Deux sorties du même module donnent deux avancements différents à la même date. | Construire la courbe en S depuis la **même** base que la valeur acquise (zones × coût de zone), ou, si la courbe doit rester continue en consommation, dire explicitement qu'elle ne coïncide pas avec VP/VA et retirer l'identification à SV. Ajouter un test : `courbe_s(prévu @ date d'arrêt) == VP/BAC` à 0,5 point près. |
| **B4 · Le moteur CPM est faux dès qu'un décalage négatif dépasse la durée du prédécesseur, et le contre-calcul accuse le bon algorithme.** | **bloquant** | Trois défaillances distinctes, reproduites au § 2.1. (a) Réseau A(10 j) → B(1 j), décalage −10 : la durée du projet est **10** (A seule dure 10 j) ; `voie_A_parcours` rend 10, `voie_B_enumeration` rend **1**, parce qu'elle ne retient que les chemins aboutissant à une tâche **sans successeur** et ignore qu'une tâche intermédiaire finit plus tard. (b) Décalage −20 : voie B rend **−1,0** — la sentinelle `meilleur = -1.0` qui fuit en sortie ; aucune garde n'interdit une durée de projet négative. (c) Aucun des deux parcours ne borne les dates à `t ≥ 0` : une tâche peut être planifiée avant le début du projet et disparaître de la durée. Et dans les trois cas le verdict rendu est « **ECART — le parcours avant/arrière est faux** », qui désigne l'algorithme **correct** ; la docstring de `cpm.py` et la page publiée (« Si elles divergeaient, c'est le parcours avant/arrière qui serait faux ») affirment la même chose, qui est fausse. Le réseau publié du module reste dans le domaine sain (|décalage| < durée du prédécesseur), donc **les chiffres d'aujourd'hui sont justes** — par choix de paramètres, pas par construction. `cpm.py` est la bibliothèque de planification de tout le cours. | Dans voie B, énumérer vers **toutes** les tâches et non vers les seules tâches terminales, initialiser `meilleur` à `-inf` et refuser une durée négative ; borner les deux parcours à `t ≥ 0` ; corriger le message de verdict (« les deux voies divergent », sans désigner de coupable) et la phrase publiée ; ajouter à `cpm_cas_ferme.py` les trois réseaux du § 2.1. |
| **M1 · La chaîne des durées n'est gardée par aucun contrôle : une erreur d'effectif double le planning sans allumer un seul des douze contrôles.** | **majeur** | Canari **T2** : `ferr_dalle` divisé par `ferrailleurs_poutres` (4) au lieu de `ferrailleurs_dalle` (8). Publié : ferraillage de dalle **6,00 j** au lieu de 3,00 ; cycle **11,557 j** au lieu de 8,557 ; cadence **6,4 j** au lieu de 3,4 ; durée du plancher **56,36 j au lieu de 32,36 (+74 %)** ; date d'arrêt 30,8 j au lieu de 18,8. Résultat de `npm run check` : **VERT, 12 contrôles**, avec `contre-calcul CPM : OK` et `contre-calcul coffrage : OK`. `test_plancher.py` recalcule à la main le volume de béton (ligne 41) et la durée de **coffrage** (ligne 55) — mais **ni le ferraillage ni le bétonnage**. CPI et SPI restent à 0,941 et 0,900 : ils sont aveugles au planning. | Recalculer à la main, dans le test, **les quatre durées** depuis `data/` (quantité, cadence, effectif nommés explicitement), et ajouter une assertion sur la cadence et la durée totale. |
| **M2 · L'explication du contrôle de main-d'œuvre ne porte pas le facteur qu'elle prétend expliquer, et contredit la définition du ratio donnée dans `data/`.** | **majeur** | La page écrit : « Ce n'est pas une erreur de calcul. C'est que **les deux hypothèses ne décrivent pas la même chose** : le prix horaire est celui d'un compagnon nu ; les heures comptées sont celles des quatre équipes de production seules, sans encadrement, grutier… ». J'ai chiffré ces deux causes : 402,2 h → **5,21 %** ; en ajoutant grutier et chef d'équipe sur tout le cycle (539,1 h) → **6,98 %** ; en prenant en plus le **haut** de la fourchette horaire (60 MAD/h) → **9,31 %**. La fourchette visée commence à 15 % : il faudrait **1 158 h, soit 2,9 fois les heures comptées** (3,2 h/m² au lieu de 1,12 h/m²). Les deux causes invoquées ne couvrent donc pas l'écart. Et `data/ratios_V3.part_main_oeuvre_directe_pct` définit le ratio comme « part de la main d'œuvre DIRECTE de production dans un prix posé de gros œuvre. **Sert de contrôle de cohérence entre le prix horaire et les prix unitaires** » : c'est exactement la comparaison que la page déclare dépourvue de sens. **Réponse à la question posée : l'explication habille une question ouverte.** Le suspect le plus probable est le jeu de cadences (1,12 h/m² de main-d'œuvre directe pour un plancher coulé en place est bas d'un facteur 2 à 3), et ces cadences sont l'entrée de **toutes** les durées que le module publie. | Écrire la conclusion honnête : l'une des trois hypothèses V3 est hors de son domaine, probablement les cadences ; donner la fourchette d'heures/m² qui rendrait le contrôle cohérent ; et, tant que le doute dure, afficher la durée du plancher avec sa fourchette (cadences basses/hautes) plutôt qu'une valeur unique. |
| **M3 · Le contre-calcul n° 1 partage son entrée décisive et ne passe que parce que la seconde hypothèse a été choisie près de la première.** | **majeur** | Les deux voies valent `coffrage_m2/(30×8)` et `coffrage_m2/232` : elles **partagent intégralement `coffrage_m2`**, la seule grandeur qui puisse être fausse. Le contrôle ne compare en réalité que 240 et 232. Canari **T6** : avec le rendement d'équipe à **190 m²/j — borne basse de sa propre fourchette V3 [190, 280]** — l'écart passe à **26,3 %** et le contrôle échoue ; à 280, il vaut 14,3 % et échoue aussi. Seul l'intervalle [228,6 ; 252,6] passe la tolérance de 5 %, soit **27 % de la fourchette déclarée**. Le contrôle est donc satisfait par le choix de l'auteur, pas par une propriété des données. La page dit honnêtement qu'il ne prouve que la cohérence mutuelle — elle ne dit pas qu'il échouerait pour les trois quarts des valeurs que la donnée déclare plausibles. | Soit faire porter la seconde voie sur une grandeur réellement différente (heures relevées sur un attachement), soit rebaptiser le contrôle « compatibilité des deux hypothèses de cadence » et afficher la plage de rendements qui la respecte, ce qui est l'information utile. |
| **M4 · Six nombres techniques sont tapés à la main dans les tableaux publiés, alors qu'ils sont dans `data/`.** | **majeur** | `content/01-…md` lignes 102 à 105 : « 30 m²/j », « 150 kg/j », « 300 kg/j », « 30 m³/h » dans la colonne « Cadence V3 », au milieu de cellules qui sont toutes des `{{variables}}`. Lignes du tableau de coût : « 1 250 MAD/m³ », « 17 MAD/kg », « 180 MAD/m² ». Tous existent dans `data/cadences` et `data/prix_unitaires_MAD`. Violation R1/§ 4.3 (« aucun nombre technique n'est tapé à la main dans un module »). Effet concret : changez une cadence dans `data/`, la **durée** affichée change et la **cadence** affichée ne change pas — le tableau se contredit lui-même, sans qu'aucun contrôle le voie. | Injecter par variables (`{{gare.cadences.coffrage_dalle_m2_j.valeur}}`, etc.) et étendre au `content/` du module le contrôle de nombres non balisés déjà demandé sur le socle. |
| **M5 · Un repère de rédaction non remplacé est publié dans un corrigé.** | **majeur** | Rendu, exercice 3 : « 25 jours est atteignable en dédoublant le front, au prix d'un second jeu de coffrage et d'un **pic d'effectif de X personnes**. Voici les deux plannings. » Le « X » est publié tel quel, dans la phrase que le module présente comme le modèle de ce qu'il faut dire en réunion. La donnée existe pourtant : `figures.effectifs` donne une pointe de 23. | Injecter `{{…}}`, et ajouter au build un échec sur tout « X » isolé ou motif de repère (`XXX`, `TODO`, `…`) dans `content/`. |
| **M6 · Le planning publié demande environ 2,5 fois le coffrage que le projet déclare posséder, et l'exercice 3 affirme le contraire.** | **majeur** | Le coffrage d'une zone est immobilisé du début du coffrage (t = 0) à la fin du décoffrage (t = 8,557 j). À la cadence publiée de 3,4 j/zone, **8,557/3,4 = 2,52 → 3 zones** détiennent du coffrage simultanément (à t = 7,0 j : Z1 pas encore décoffrée, Z2 en cours, Z3 en coffrage). Il faut donc ≈ 3 × 343,2 = **1 030 m²** de tables rien que pour les sous-faces, 1 273 m² avec les poutres. `data/materiel.tables_coffrantes_m2` vaut **420**. L'exercice 3 écrit pourtant : « Il faut deux jeux de tables coffrantes — **420 m² de plus** », ce qui suppose que 420 suffisent au planning nominal. Par ailleurs `materiel.etais` (900) et `materiel.pompe_a_beton` ne sont lus par **aucun** fichier (`grep`), alors que le décoffrage « étais de reprise maintenus » les immobilise plus longtemps encore. | Faire calculer par `calc/` le coffrage simultanément immobilisé et le comparer au stock déclaré ; faire de cette comparaison un contrôle de cohérence (c'est le genre de contrainte que la cadence doit respecter) ; corriger l'exercice 3 en conséquence. |
| **M7 · Aucune vérification dimensionnelle dans les quatre bibliothèques nouvelles, alors que le contrôle continue d'afficher « unités (pint) ».** | **majeur** | `grep -c pint` → **0** dans `calc/plancher.py`, `calc/cycle_plancher.py`, `calc/valeur_acquise.py` et `calc/cpm.py` (seul `cage.py`, du socle, en a une). Le § 3.3 exige que « chaque formule de `calc/` passe une vérification dimensionnelle automatique », et le § 12.1 i en fait un point de contrôle. `build/check.mjs` affiche pourtant « f,i · calc/ : étalonnage, calculs, tests, **unités (pint)** » : le libellé est vrai pour une bibliothèque sur cinq. Le module manipule des MAD/m³, des kg/j, des m²/j, des m³/h, des j et des h — exactement le terrain des erreurs d'unité. | Étendre la vérification `pint` aux quatre bibliothèques (au minimum : `d = Q/(c·n)` en jours, le coût en MAD, CPI et SPI sans dimension), ou retirer la mention « pint » du libellé du contrôle. |
| **M8 · Deux des quatre bibliothèques de `calc/` ne sont pas étalonnées.** | **majeur** | `ls calc/etalonnage/` → `perimetre_cadre.py` (socle) et `cpm_cas_ferme.py`. **`plancher.py` et `valeur_acquise.py` n'ont aucun étalonnage**, et `run_all.py` n'en lance que deux. Le § 3.3 est explicite : « sans étalonnage, ses résultats restent V3 et **ne servent pas d'exemple de référence** ». Or les quantités de `plancher.py` et les indicateurs de `valeur_acquise.py` sont les résultats de tête du module témoin. (Nuance : `plancher.py` est de la géométrie pure, et son volume est recalculé à la main dans le test — mais ni le coffrage ni les ratios d'acier ne le sont, et `valeur_acquise.py` n'a rien du tout.) | Étalonner `valeur_acquise.py` sur un exemple d'EVM à solution connue (un cas publié V0 ou un cas construit à la main : CPI, SPI, EAC posés d'avance) et `plancher.py` sur une géométrie dont les quantités se posent sans la fonction. |
| **M9 · La tolérance du contre-calcul de valeur acquise est deux ordres de grandeur plus serrée que l'incertitude de ses propres entrées.** | **majeur** | Tolérance **1,0 %**, écart constaté **1,033 %** → le contrôle « sonne ». Mais la voie A repose sur le coût de zone, dont **42,6 %** (148 104 MAD sur 347 478) viennent de l'acier, lui-même issu d'un ratio V3 de fourchette 7 026–10 848 kg. En bornes : le coût de zone va de **318 816 à 383 790 MAD**, soit **−8,3 %/+10,4 %** — et la voie B, bâtie sur des quantités relevées, ne bouge pas avec lui. Un écart de 1 % entre les deux voies est donc **noyé dans une incertitude structurelle de ±10 %**. Le § 1 du module dit d'ailleurs lui-même « l'acier est un ordre de grandeur à ± 20 % ». La donnée reconnaît que les relevés ont été « posés légèrement en retrait […] pour que la démonstration montre ce que le contrôle sert à détecter » : l'alarme est donc fabriquée, et la fiche mémo en tire une règle de chantier — « Écart > 1 % → attachements ». | Fixer la tolérance au-dessus de l'incertitude propagée des entrées (ou faire porter le contrôle sur les seules quantités, où l'incertitude du ratio disparaît des deux côtés), et retirer le seuil de 1 % de la fiche mémo tant qu'il n'est pas justifié. |
| **m1 · Figure 1 : les lignes de poutres traversent les libellés de zone.** | mineur | Capture produite et examinée : le trait rouge tireté passe à travers les textes « Z1 / coulée », « Z6 », « Z7 », « Z8 », qui sont centrés sur la zone comme la ligne de poutre. Le contrôle automatique ne le voit pas : il compare des boîtes **texte contre texte** (`rendu.spec.mjs`), jamais texte contre trait. La grille du § 8 demande un « texte lisible à 100 % de zoom ». | Décaler le libellé de zone d'un quart de largeur, ou interrompre le trait derrière le texte (halo). |
| **m2 · Figure 3 : la légende annonce un code couleur qui ne distingue rien.** | mineur | « Ce qu'il faut voir : **les barres en brique sont sur le chemin critique** ». Les sept tâches ont une marge nulle (`marges` : 0.0 partout) : **toutes** les barres sont en brique. La phrase laisse croire à une lecture qui n'existe pas sur cette figure. | Soit ajouter une tâche à marge non nulle au réseau d'exemple (il y en a dans la réalité : l'approvisionnement), soit écrire « toutes les tâches sont ici critiques — c'est précisément le signe d'un cycle tendu ». |
| **m3 · Exercice 3 : la formule de durée totale est fausse dans sa forme.** | mineur | « soit **8 × 2,8** + cycle ≈ 28 j ». La règle du module est (n − 1) × cadence + cycle : le planning publié vaut 7 × 3,4 + 8,557 = 32,357 j. Avec 8 × 2,8 + 8,557 on obtient 30,96, pas 28 ; le « ≈ 28 » ne s'obtient qu'avec 7 × 2,8. La formule affichée et le résultat affiché ne se correspondent pas. | Écrire (n − 1) × cadence + cycle, et laisser `calc/` produire le nombre. |
| **m4 · Aucune grille § 7.2 n'est produite pour ce module.** | mineur | `grep "Grille d'auto" STATE.md` → une seule occurrence, « page de démonstration E1 ». Le § 7.2 impose la note avant livraison et le § 12.2 point 6 la contrôle. Je l'ai donc établie moi-même (§ 5 ci-dessous), et elle n'est pas au minimum requis partout. | Produire la grille, et traiter le critère qui tombe sous 2. |
| **m5 · La règle de cadence de rotation n'est publiée nulle part.** | mineur | La page annonce « une cadence de **3,4 jours par zone** » sans donner la règle. Elle est dans `cycle_plancher.py:163` : `round(max(coffrage_j, ferraillage_dalle_j) + betonnage_j, 1)`. Le lecteur ne peut donc pas retrouver 3,4, ni comprendre pourquoi l'exercice 3 fait varier cette cadence avec l'effectif de ferrailleurs. C'est le seul nombre structurant du planning qui ne soit pas démontré dans un module dont la thèse est « les durées viennent des quantités, pas d'un dire d'expert ». | Publier la règle et la justifier (la rotation est bornée par la tâche la plus longue plus le coulage), et dire qu'elle ignore la contrainte de coffrage (**M6**). |
| **m6 · Les cinq figures de ce module ne sont capturées par aucun test.** | mineur | `ls tests/captures/` : dix-huit fichiers, **tous** du module `00-demo-cage`, plus `figure1.png` et `index.png`. Le module TV n'a pas de 3D, donc le spec ne produit rien pour lui ; la recette du § 9.4 ne s'applique pas, mais le § 12.1 b parle de captures « examinées ». J'ai dû les produire moi-même pour les regarder — et c'est ainsi que **B3** et **m1** sont apparus, qu'aucun contrôle automatique ne voyait. | Capturer chaque `figure` des modules sans 3D et conserver l'image, pour que « examinée » repose sur un artefact. |
| **m7 · Un calcul inutilement obscurci dans `valeur_acquise.py`.** | mineur | `avancement_releve = VA_B / (cout_zone_MAD * n_zones) * n_zones` : le `* n_zones` et le `/ n_zones` s'annulent ; l'expression vaut `VA_B / cout_zone_MAD`. Sans conséquence numérique (3,563 ✓), mais c'est le genre d'écriture qui masque une erreur de facteur lors d'une relecture. | Écrire `VA_B / cout_zone_MAD`. |

---

## 4. Les 10 points du § 12.2

| # | Point | Constat |
|---|---|---|
| **1** | Unités et homogénéité | **Défaut M7.** J'ai vérifié l'homogénéité à la main sur toute la chaîne : `m² / (m²·j⁻¹·compagnon⁻¹ × compagnon) = j` ✓ ; `m³ / (m³·h⁻¹) / (h·j⁻¹) = j` ✓ ; `kg × MAD·kg⁻¹ = MAD` ✓ ; CPI et SPI sans dimension ✓ ; EAC en MAD ✓. Les dix-neuf valeurs recalculées en SI concordent (§ 1). **Mais aucune de ces formules n'est vérifiée automatiquement** : zéro occurrence de `pint` dans les quatre bibliothèques du module, alors que le contrôle affiche « unités (pint) ». |
| **2** | Référentiels mélangés | **RAS.** `grep -onE "BAEL\|BPEL\|RPS ?2000\|Eurocode\|EN 199[0-9]\|NF ?P\|fck\|C25/30"` sur `modules/01-tranche-verticale-suivi.html` → **aucune occurrence**. Le module est entièrement non normatif, ce qui est cohérent avec la phase § 5.0 : aucun cadre de sécurité n'est invoqué, donc aucun mélange possible. |
| **3** | Article cité sans V0 ni V1 | **RAS.** Aucun numéro d'article (`grep "art\.? ?[0-9]+"` → rien). Les valeurs V3 publiées portent des balises à six champs et alimentent `registre-hypotheses.csv` (9 lignes, contrôle « chaque V3 publiée a sa ligne de registre » au vert). **Réserve** : six nombres techniques échappent au balisage comme aux variables — **M4**. |
| **4** | Ordres de grandeur et ratios | **Défauts M2, M9.** Ratios recalculés par moi : acier **88,5 kg/m³** et **24,2 kg/m²** — plausibles pour un plancher à poutres ; coffrage **1,179 m²/m²** — plausible ; coût **965 MAD/m²** de gros œuvre — plausible. En revanche la main-d'œuvre directe ressort à **1,12 h/m²**, soit 2 à 3 fois moins que l'ordre de grandeur d'un plancher coulé en place, ce que le contrôle de part de main-d'œuvre signale (5,2 % contre 15–30 %) et que l'explication publiée écarte à tort (**M2**). Et la tolérance de 1 % du contrôle de valeur acquise est incommensurable avec le ±10 % de ses entrées (**M9**). |
| **5** | Cohérence data / figures / calcul / coût / planning | **Défauts B3, M6, M1.** La courbe en S contredit le tableau de valeur acquise du même module (**B3**). Le planning contredit le matériel déclaré d'un facteur 2,5 (**M6**). Et la chaîne quantité → durée → planning n'est gardée par aucun contrôle (**M1**, canari T2 : +74 % sur la durée totale, douze contrôles verts). Ce qui **est** cohérent et que j'ai vérifié : les quantités, le coût et les indicateurs se recoupent exactement entre `tranche-plancher.json`, `valeur-acquise.json` et la page ; le nombre de poutres par zone se recoupe par deux chemins indépendants ; la date d'arrêt est bien déduite du planning et non saisie. |
| **6** | Grille de profondeur § 7.2 | **Défaut m4** : aucune grille n'existe pour ce module. Je l'ai établie au § 5 ; **un critère tombe sous le minimum de 2**. |
| **7** | Sécurité : conseil dangereux ou omission | **RAS, avec une réserve de forme.** Aucun conseil dangereux : le module ne donne aucune prescription d'exécution. Les trois points durs sont nommés et affectés à la maîtrise d'œuvre dans le tableau S7 — « contrôle la **stabilité de l'étaiement** et la géométrie avant tout ferraillage », « **point d'arrêt** : enrobage, calage, recouvrements », « contrôle le **critère de décoffrage** et la présence des étais de reprise » —, et la fiche mémo S8 les reprend. Le point d'arrêt est modélisé comme une tâche du planning sur le chemin critique, ce qui est le bon traitement. Réserve : le § 3.4 demande, pour l'étaiement, de « renvoyer aux exigences réglementaires et au plan HSE du chantier » ; le module nomme les contrôles mais ne fait pas ce renvoi. La mention pédagogique obligatoire est en pied de page. |
| **8** | Vérité du rendu | **Défauts B3, m1, m2, m6.** Vérifié en exécutant : `npm run check` → **12 contrôles verts**, 12 tests Playwright, **zéro erreur de console**, zéro requête externe (j'ai rejoué le chargement de la page en `file://` et relevé la console : vide). J'ai produit et **regardé les cinq figures**. Aucun chevauchement texte/texte (vérifié par boîtes englobantes : 0 sur les 5 figures, 92 textes au total), aucune figure vide, échelles correctes, la courbe en S n'est plus écrasée et s'arrête bien avant la fin. Ce que l'œil trouve et que les tests ne voient pas : la courbe en S ment sur SV (**B3**), les traits de poutre traversent les libellés (**m1**), le code couleur du Gantt ne distingue rien (**m2**), et rien n'est archivé (**m6**). |
| **9** | Simplifications non signalées | **RAS.** Les simplifications structurantes sont déclarées et au bon endroit : l'encart d'ouverture dit que « le béton et le coffrage sont justes à la géométrie près ; **l'acier est un ordre de grandeur à ± 20 %** », le tableau des trois familles de nombres le reprend, la fourchette d'acier (7 026–10 848 kg, 43,9 %) est publiée, la marquise est explicitement **exclue** des zones dans `data/`, et le contre-calcul n° 1 dit lui-même qu'il ne prouve pas que les hypothèses sont justes. J'ai vérifié chaque exclusion dans les données. |
| **10** | Texte télégraphique ou remplissage | **Défauts B1, B2, M5, m3.** Le texte est dense et en phrases, chaque paragraphe porte une règle ou un chiffre, et la section S2 (« la zone est l'unité de tout ») est la meilleure page écrite jusqu'ici dans ce dépôt. Mais le module publie **un repère de rédaction non remplacé** (« un pic d'effectif de **X** personnes »), **deux chiffres faux** (40 %, 2,42 j) et **une formule qui ne correspond pas à son résultat** (8 × 2,8 ≈ 28). Ce sont des défauts de finition, pas de rédaction — ils n'en sont pas moins publiés. |

---

## 5. Grille d'auto-évaluation § 7.2 (notée par le relecteur, faute d'une grille de l'auteur)

| Critère | Note | Justification |
|---|---:|---|
| Le « pourquoi » est expliqué | **3** | S2 justifie le choix de la zone comme unité par quatre propriétés simultanées (quantité, durée, coût, jalon) : c'est une vraie idée, pas une définition. |
| Les hypothèses sont explicites | **3** | Trois familles de nombres distinguées et nommées, fourchettes publiées, balises V3 à six champs, registre complet. |
| Les formules sont justifiées | **2** | `d = Q/(c·n)` est posée et expliquée ; le volume et le coffrage sont décomposés poste par poste. Mais la **règle de cadence de rotation** — le nombre qui porte tout le planning — n'est publiée nulle part (**m5**). |
| L'exemple est vérifié | **1** | **Sous le minimum.** Le corrigé de l'exercice 2 publie une division fausse (**B2**) qui renverse la conclusion de l'exercice 3 ; la courbe en S contredit le tableau (**B3**) ; et la chaîne des durées passe un canari qui double le planning (**M1**). « Vérifié » ne peut pas être coché. |
| Le piège est identifié | **3** | Le tableau S5 donne six pièges avec leur symptôme **et** leur coût ; l'erreur du double compte de main-d'œuvre est traitée au bon endroit et bien expliquée. |
| Le lien avec l'exécution est fait | **3** | Double lecture entreprise/maîtrise d'œuvre poste par poste, point d'arrêt modélisé comme une tâche du chemin critique, étais de reprise, critère de décoffrage. |
| Le lien avec le coût et le délai est fait | **3** | C'est l'objet même du module, et il va jusqu'au bout : quantités → durées → coût → planning → valeur acquise → reporting. |

**Minimum 2 partout exigé avant livraison (§ 7.2) : non tenu** — « l'exemple est vérifié » est à 1.

---

## 6. Synthèse et verdict

**19 défauts : 4 bloquants, 9 majeurs, 6 mineurs.**

Ce qui est solide, et qu'il faut dire : **le moteur de calcul est juste**. Dix-neuf valeurs recalculées
à l'aveugle depuis `data/` seul concordent au dernier chiffre, y compris les plus composées (gain du
recouvrement, EAC, avancement impliqué par les relevés). La chaîne data → calc → rendu existe
vraiment, la date d'arrêt est déduite et non saisie, le contre-calcul de valeur acquise a bien été
rendu indépendant et un test le garde (canari T5). La forme — S2, S5, S7, la fiche mémo — est au
niveau attendu d'un module témoin.

Les quatre points qui interdisent la validation :

1. **Deux chiffres faux sont publiés, et l'un renverse une conclusion d'ingénierie.** « Sous-estimer
   le poste de 40 % » là où la géométrie donne 15,2 %, par concaténation accidentelle d'une variable
   et d'un zéro littéral ; et « 7200/(300×12) = 2,42 j » là où la division donne 2,00, erreur qui se
   propage en cadence (2,8 au lieu de 2,4), en durée (28 au lieu de 25,4) et finalement en
   recommandation : le module conseille de dédoubler le front avec un second jeu de coffrage alors
   que quatre ferrailleurs de plus atteignent la cible.
2. **La courbe en S contredit le tableau de valeur acquise du même module** — 59,9 % contre 50,0 % de
   prévu, 51,9 % contre 45,0 % d'acquis — pendant que sa légende affirme que l'écart vertical *est*
   SV, lequel vaut 5,0 points et non 8,0.
3. **Le moteur CPM est faux hors du domaine utilisé** : dès qu'un décalage négatif dépasse la durée du
   prédécesseur, l'énumération rend 1 pour une durée de 10, ou une durée négative, et le verdict
   accuse le parcours avant/arrière, qui est le bon. La page publie cette affirmation inversée. Les
   quatre réseaux d'étalonnage n'entrent jamais dans ce régime. C'est la bibliothèque de planification
   de tout le cours.
4. **La chaîne des durées n'est gardée par rien** : un effectif confondu double le planning (+74 %)
   sans allumer un seul des douze contrôles, les deux contre-calculs répondant « OK ». Et le contrôle
   de main-d'œuvre, qui est le seul à pointer vers la cause probable — des cadences optimistes d'un
   facteur 2 à 3 —, est désamorcé par une explication que le chiffrage ne soutient pas.

### Zéro bloquant ? — **NON.**

Quatre bloquants : **B1**, **B2**, **B3**, **B4**. Les neuf majeurs sont à traiter dans la même passe
(§ 12.2 : « les bloquants et majeurs sont corrigés, puis la passe est relancée jusqu'à zéro
bloquant »). Le § 7.2 n'est pas au minimum requis.

**Ce module ne doit pas être dupliqué en l'état.** Une erreur de corrigé qui renverse une
recommandation, une figure qui contredit son propre tableau, et un moteur de planning faux hors
domaine : ce sont exactement les trois choses qu'un module témoin existe pour attraper avant qu'elles
ne partent en cinquante exemplaires. Une seconde passe devra rejouer **T2** et **T6**, et les trois
réseaux CPM du § 2.1.
