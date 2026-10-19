# Passe adversariale /devil n° 4 — module TV (tranche verticale de suivi)

**Relecteur hostile, indépendant de l'auteur. 19/10/2026.**
Méthode : contre-expertise à l'aveugle d'abord — neuf grandeurs recalculées depuis `data/projet-gare.json`
**seul**, par mes propres scripts, **avant** d'ouvrir `calc/`. Puis treize canaris (cinq rejoués, huit neufs),
mesure des cinq figures dans le SVG rendu, `npm run check` et `python3 calc/run_all.py`.
`QA/TV-tranche-verticale-passe3.md`, la section « passe adversariale » de `STATE.md` et `DECISIONS.md`
D-023 à D-025 n'ont été lus **qu'à la fin**, pour confronter le déclaré au constaté.

Scripts de preuve : `/tmp/claude-0/-home-user-mine/70713aa8-3622-5c6d-a7c2-bce4a8b25d73/scratchpad/blind/`
(`aveugle.py`, `preuve_recouvrement.py`, `preuve_va.py`, `preuve_grue.py`, `run_canaris.py`).
Rien du dépôt n'a été modifié ; les essais ont tourné sur une copie `cp -a`.

---

## 0. Ce que l'outillage dit de lui-même

```
npm run check            VERT — 15 contrôles passés
python3 calc/run_all.py  calc/ : VERT
```

Les trois bloquants ci-dessous franchissent ces deux commandes sans bruit.

---

## 1. Contre-expertise à l'aveugle — neuf grandeurs recalculées depuis `data/` seul

| # | Grandeur | Mon recalcul indépendant | Publié | |
|---|---|---:|---:|---|
| 1 | Béton d'une zone : 360 × 0,25 + 2 × 24,0 × 0,35 × 0,50 | **98,40 m³** | 98,4 | ✓ |
| 2 | Coffrage : (360 − 16,8) + 48,0 + 16,8, + 4 % de rives | **424,32 m²** | 424,3 | ✓ |
| 3 | Acier : 80 × 90,0 + 180 × 8,40 | **8 712 kg** (88,5 kg/m³) | 8 712 / 88,5 | ✓ |
| 4 | Durées : 424,32/(30×8) · 1512/(150×4) · 7200/(300×8) · 98,4/30/8 | **1,768 · 2,520 · 3,000 · 0,410 j** | 1,77 · 2,52 · 3,00 · 0,41 | ✓ |
| 5 | **Cycle**, lecture littérale de `data/` et de la balise V3 (« part du ferraillage des poutres **faite avant** que celui de la dalle démarre » = 40 %) | **8,053 j** | 8,557 | ✗ → **B2** |
| | **Cycle**, lecture « 40 % de recouvrement » (celle du code) | **8,557 j** | 8,557 | ✓ |
| 6 | **Cadence** = max(équipe la plus chargée 3,000 ; grue (1,768 + 0,500)/1 = 2,268) × 1,14 | **3,420 j** | 3,42 | ✓ |
| 7 | Coût d'une zone : 98,4×1250 + 8712×17 + 424,32×180 | **347 478 MAD** ; BAC **2 779 824** | 347 478 / 2 779 824 | ✓ |
| 8 | **État physique** de la zone en cours à 60 % du cycle (t = 5,13 j), dérivé du réseau | COF **100 %**, FEP **100 %**, FED **91,2 %**, BET **0 %** → 424,3 m² · 8 081 kg · **0,0 m³** | idem | ✓ |
| 9 | Écarts relevés / état physique : −0,61 % · −0,80 % · −2,01 % | idem | idem | ✓ |
| 10 | **Valeur acquise**, à partir de l'état physique du 8 | **1 256 185 MAD**, CPI **0,945** | 1 250 921 / **0,941** | ✗ → **B1** |
| 11 | Conflits de grue dans le planning publié (8 zones, cadence 3,4 j) | **6 conflits de 0,50 j** | aucun signalé | ✗ → **B3** |

L'arithmétique est juste partout. **Trois modèles ne disent pas ce qu'ils prétendent.** C'est la
cinquième occurrence de la même famille, et c'est elle que je rapporte.

---

## 2. Les trois bloquants

### B1 · La valeur acquise applique le prorata uniforme que le module condamne douze lignes plus haut

`calc/valeur_acquise.py` :

```python
avancement_zones = s["zones_realisees_a_date"] + s["avancement_zone_en_cours_pct"] / 100.0   # 3 + 0,60
VA_A = BAC * (avancement_zones / n_zones)                                                    # = 3,6 × budget de zone
```

`avancement_zone_en_cours_pct` est une **fraction de temps de cycle**. `VA_A` lui applique donc, en
dirhams, exactement ce que l'encart du § S6 déclare impossible : « 60 % d'une zone, ce n'est pas 60 % de
chaque poste ». Le même fichier, trente lignes plus bas, calcule pourtant l'état physique poste par
poste — et ne s'en sert que pour le recoupement, jamais pour la valeur acquise.

Le module se réfute lui-même dans son corrigé de l'exercice 4 :

> « **La racine commune aux trois.** Le sous-traitant a pris son avancement déclaré et l'a appliqué à
> chaque ligne. Toutes ses quantités valent donc 60 % du total — et c'est le signe, visible d'un coup
> d'œil, que personne n'est allé mesurer. »

Puis il publie CPI, SPI, SV, CV, EAC, la dérive prévue, la figure 5 et le « 3,60 zones réalisées » du § S6
sur ce modèle-là.

**Portée mesurée** (`preuve_va.py`, valeur de la zone en cours selon les deux modèles) :

| fraction du cycle | VA linéaire (modèle publié) | VA par l'état physique | écart |
|---:|---:|---:|---:|
| 0,20 | 69 496 | 82 286 | **−15,5 %** |
| 0,50 | 173 739 | 178 850 | −2,9 % |
| **0,60 (point publié)** | 208 487 | 213 751 | **−2,5 %** |
| 0,65 | 225 861 | 224 478 | +0,6 % |
| **0,70** | 243 235 | 327 353 | **−25,7 %** |
| 0,80 | 277 982 | 347 478 | −20,0 % |

Le point retenu, 60 %, tombe dans l'unique fenêtre étroite où les deux modèles se croisent : le coffrage
à 100 % compense le béton à 0 %. **Le défaut est caché par le choix de la donnée, pas corrigé.**

**Le contre-calcul ne peut pas le voir, et je le prouve.** Si l'on pose les relevés **exactement** sur
l'état physique — un chantier parfaitement conforme, aucune dérive —, la voie A donne 1 250 921 MAD et la
voie B 1 256 185 : **écart résiduel 0,421 %, tolérance 1 %**. Ce 0,42 % n'est pas du chantier, c'est le
biais du modèle, et le seuil l'absorbe. À 70 ou 75 % d'avancement déclaré, le même contre-calcul rendrait
**6,5 %** et sonnerait.

VP est touchée de la même façon (`avancement_prevu(j) = (j − début)/cycle`, § `cycle_plancher.py`) :
VP linéaire 1 690 407 MAD contre 1 702 137 par l'état physique, **−0,69 %** ; SPI publié 0,740 contre 0,738.
La courbe en S de la figure 5 trace cette même fraction de temps sous un axe intitulé « % », et sa légende
— « l'écart vertical entre la courbe et le point, c'est SV » — n'est vraie **que** parce que les deux
termes partagent l'erreur.

**D-023 est à moitié appliquée.** Elle a atteint le tableau des quantités physiques, le recoupement et
l'exercice 4 ; elle n'a atteint ni la valeur acquise, ni la valeur planifiée, ni la courbe en S, ni le
« 3,60 zones réalisées ». `STATE.md` affirme pourtant : « *toute grandeur décrivant l'état du chantier à
une date est dérivée du réseau et un test refait la dérivation* ». Les deux moitiés de la phrase sont
fausses (voir aussi M1).

**Correction proposée.** Faire de la valeur acquise une fonction de l'état physique :
`VA = Σ postes (état_physique_du_poste × quantité × prix)`, pour la zone en cours **et** pour chaque zone
partiellement avancée de la VP. Publier l'avancement en **valeur** (ici 61,5 % de la zone, pas 60 %) à
côté de l'avancement en temps, et dire que les deux diffèrent — c'est précisément la leçon du module.
Descendre ensuite la tolérance du contre-calcul en dirhams à 0,2 %, ce que le modèle corrigé permet.

### B2 · Le taux de recouvrement est appliqué à son complément : `data/`, la balise V3 et le registre disent 40 %, le réseau en fait 60 %

`calc/cycle_plancher.py:reseau_zone` :

```python
Tache("FED", "Ferraillage de la dalle", t["ferraillage_dalle_j"],
      [("FEP", -t["ferraillage_poutres_j"] * r2), "COF"])
```

Le décalage se lit, dans `cpm.py`, comme `début ≥ fin_du_prédécesseur + décalage`. Avec `r2 = 0,40`,
FED démarre donc à `fin_FEP − 0,40 × durée_FEP`, c'est-à-dire quand **60 %** de FEP est fait.

`data/cycle_zone.recouvrement_ferraillage_poutres_dalle_pct`, la balise du § S4d et la ligne **H024** du
registre disent toutes trois : « *part du ferraillage des poutres **faite avant** que celui de la dalle
démarre* » = **40 %**.

**Mesuré dans le SVG rendu de la figure 3** (`modules/01-tranche-verticale-suivi.html`, échelle
19,28 px/j) : FEP 0,89 → 3,41 j, FED démarre à **2,40 j**, soit (2,40 − 0,89)/2,52 = **59,9 %**. La figure
du module prouve la contradiction à l'œil.

**Le paramètre est inversé**, et je l'ai balayé (`preuve_recouvrement.py`) :

| valeur déclarée | part de FEP réellement faite au démarrage de FED | cycle |
|---:|---:|---:|
| 20 % | **80 %** | 9,061 j |
| 40 % | **60 %** | 8,557 j |
| 60 % | **40 %** | 8,053 j |

Augmenter un « recouvrement » **raccourcit** le cycle ; augmenter une « part faite avant le démarrage »
devrait l'**allonger**. Le lecteur qui joue avec la fourchette [20 ; 60] obtient l'inverse de ce que
l'énoncé lui promet.

**Pourquoi quatre passes ne l'ont pas vu.** Le premier recouvrement vaut **50 %** : il est
auto-complémentaire, les deux lectures y coïncident au chiffre près, et il masque le second. La passe 3
avait pourtant **mesuré l'écart** (sa ligne 5 : « cycle, lecture littérale de `data` = 8,048 j contre
8,557 publié ✗ »), puis l'a routé vers son **M3**, qui portait sur l'absence de ligne de registre. La
correction a donc ajouté une balise et une ligne de registre **recopiant l'énoncé faux** : le défaut a
été entériné au lieu d'être corrigé, et il est désormais inscrit dans `data/registre-hypotheses.csv`.

**Conséquences chiffrées** : cycle 8,557 j au lieu de 8,053 (**+6,3 %**) ; durée du plancher 32,4 j au lieu
de 31,0 ; `zones_etayees` 7 au lieu de 7 (inchangé) ; état physique de la zone en cours FED 91,2 % au lieu
de 98,0 % ; acier attendu 34 217 kg au lieu de 34 702, donc l'écart publié sur l'acier (−2,01 %) au lieu
de −3,38 %.

**Correction proposée.** Choisir **une** sémantique et la rendre vérifiable. Si le paramètre est un
recouvrement, écrire dans `data/`, dans la balise et dans H024 : « *part du ferraillage des poutres
qui reste à faire quand celui de la dalle démarre* ». Si c'est une part faite avant, écrire
`-(1 - r2) * t["ferraillage_poutres_j"]`. Dans les deux cas ajouter le test qui manque : pour chaque
recouvrement, recalculer `(début_successeur − début_prédécesseur)/durée_prédécesseur` depuis le réseau et
le confronter au paramètre déclaré. Et **ne jamais retenir 50 % comme valeur de référence pour le
premier** : une valeur auto-complémentaire ne peut pas servir de témoin.

### B3 · Le planning publié est infaisable avec la grue déclarée ; la règle de cadence ne vérifie qu'une moyenne

La règle refondée par D-024 borne la cadence par `occupation cumulée des tâches de grue ÷ nb_grues`
= (1,77 + 0,50)/1 = **2,27 j** contre une cadence de 3,4 j, soit **67 % d'occupation**. C'est une
condition **nécessaire en moyenne**, pas une condition de faisabilité : les tâches sont à des décalages
fixes dans le cycle, et le planning qui en sort viole la ressource à des instants précis.

Balayage du planning publié (`preuve_grue.py`, 8 zones, cadence 3,4 j, cycle 8,557 j) :

```
j  8,06 -> 8,56  : Z1/DEC ET Z3/COF   (0,50 j)
j 11,46 -> 11,96 : Z2/DEC ET Z4/COF   (0,50 j)
j 14,86 -> 15,36 : Z3/DEC ET Z5/COF   (0,50 j)
j 18,26 -> 18,76 : Z4/DEC ET Z6/COF   (0,50 j)
j 21,66 -> 22,16 : Z5/DEC ET Z7/COF   (0,50 j)
j 25,06 -> 25,56 : Z6/DEC ET Z8/COF   (0,50 j)
```

**Six fois**, et à chaque fois sur la **totalité** du décoffrage : la grue unique est demandée en deux
endroits. La figure 2 — la figure phare de la passe 3 — **affiche** ces chevauchements : la barre grise
DEC de Z1 et la barre bleu clair COF de Z3 sont alignées. Personne ne les a confrontées.

Le contrôle n° 5 de la fiche mémo promet pourtant au lecteur que la vérification est faite :

> « La cadence annoncée tient-elle **en matériel** ? […] la grue cumule les tâches qu'elle sert :
> comparez au parc **et** à la grue avant d'annoncer une date. »

Et l'exercice 3 fait défendre en réunion, chiffres à l'appui, l'achat d'une **seconde grue** sur la foi de
cette même règle moyenne. Le conseil est peut-être bon ; la démonstration ne le prouve pas.

**Correction proposée.** Après le calcul de la cadence, **niveler** : balayer les fronts du planning et
vérifier, pour chaque ressource déclarée (grue, et chaque équipe dédiée), que le nombre d'occurrences
simultanées ne dépasse jamais l'effectif de la ressource. Publier le profil d'occupation de la grue
jour par jour sous la figure 2, à côté de la courbe du coffrage immobilisé — c'est la même figure et le
même geste. Lever si la contrainte mord, comme le fait déjà le contrôle de parc de tables.

---

## 3. Canaris

### 3.1 Rejeu des canaris des passes précédentes

| Canari | Résultat |
|---|---|
| **T2** — effectifs `ferrailleurs_dalle` / `ferrailleurs_poutres` permutés | **SONNE** — 8 échecs (durées recalculées, dépendance à l'effectif, cascade des variantes, SPI). Tient. |
| **T6** — rendement d'équipe à **190 m²/j**, borne basse de sa fourchette déclarée | **SONNE** — écart 26,32 %, 2 échecs. Tient. |
| **permutation de `effectif_par_tache`** (COF ↔ FED) | **SONNE** — « la tâche COF est servie par *coffreurs* — `data/` dit *ferrailleurs_dalle* ». Tient. |
| **recouvrement hors fourchette** (85 % pour [20 ; 60]) | **SONNE** — contrôle de fourchette de D-025. Tient. |
| **maintien d'étais nul** (0 j pour [7 ; 28]) | **SONNE** — même contrôle. Tient. |

Les cinq corrections tiennent. C'est la première passe où c'est le cas.

### 3.2 Huit canaris neufs

| # | Mutation | Verdict | Ce que le module publierait |
|---|---|---|---|
| **N1** | `decoffrage_j` retiré de `taches_servies_par_la_grue` | SONNE | — |
| **N2** | `marge_de_rotation_pct = 0` (borne déclarée de sa fourchette) | SONNE | — |
| **N3** | `nb_grues = 3` | SONNE | — |
| **N4** | **rattachement poste → tâche permuté** dans `etat_physique_de_zone` (coffrage ← BET, béton ← COF) | **TOUS VERTS** | voir ci-dessous → **M1** |
| **N5** | `jour_arret_ouvre = 20` | **TOUS VERTS** | VP passe de 1 688 743 à **1 772 138 MAD** (+4,9 %), SPI de 0,741 à 0,706 ; aucune borne, aucune ligne de registre → **m8** |
| **N6** | `avancement_zone_en_cours_pct = 75` | SONNE (indirectement) | — |
| **N7** | `recouvrement_coffrage_ferraillage_poutres_pct = 30` — **valeur légale, borne de la fourchette déclarée [30 ; 70]** | **SONNE, mais sur un défaut du module** : « la pointe publiée est bien le maximum de l'histogramme — 29 contre 27 » → **M3** |
| **N8** | `longueur_zone_m = 17` | SONNE (4 échecs) | — |

**N4 est le canari décisif de cette passe.** Il permute le cœur même de la correction D-023. Résultat :

```
calc/ : VERT
zone en cours : 0,0 m² de coffrage, 98,4 m³ de béton
   beton_m3     attendu  393,6   relevé  293,4   écart  −25,46 %   signal=True
   coffrage_m2  attendu 1272,9   relevé 1683,6   écart  +32,26 %   signal=True
   acier_kg     attendu  34217   relevé 33530    écart   −2,01 %   signal=False
   CPI 0,941   SPI 0,741   contre-calcul VA : 0,888 %  ->  OK
```

Le module publierait « **0 m² de coffrage et 98,4 m³ de béton** » pour une zone à 60 % de son cycle —
l'énoncé exact que son encart déclare impossible —, les **deux** recoupements géométriques lèveraient
`signal: True`, et `calc/` resterait **vert**. Rien n'assure que `un_poste_geometrique_derive` vaut `false`
sur le cas publié ; rien ne contrôle l'affectation poste → tâche, alors que l'affectation équipe → tâche,
elle, l'est nommément (sept assertions).

Incidemment, N4 **ne bouge ni CPI, ni SPI, ni le contre-calcul de la valeur acquise** : preuve directe et
indépendante que la valeur acquise n'utilise pas l'état physique (**B1**).

---

## 4. Les cinq figures, mesurées dans le SVG rendu

| Figure | Ce qu'elle prétend | Ce que j'ai mesuré | |
|---|---|---|---|
| **1** — zones de coulage | « liséré bleu : zone que le planning voulait finie (trait plein) ou en cours (tireté) » | 4 lisérés pleins (x 49→357, sous Z1–Z4), 2 tiretés (x 363→514, sous Z5–Z6), rien sous Z7–Z8. Conforme à `etat_prevu = [faite ×4, en_cours ×2, à_venir ×2]`. | ✓ |
| **1** | « les lignes tiretées sont les poutres intermédiaires, **au milieu de chaque zone** » | 15 lignes au pas de 39,25 px = 7,50 m : 8 au milieu, 7 **sur les limites de zone**. | ✗ **m1** |
| **2** — rotation | « chaque couleur une phase ; les phases SE RECOUVRENT » | Chaque phase occupe sa propre sous-bande (7 × 3 px dans une ligne de 26). Z1 : COF 40→74,13 px = 1,77 j ; FEP 57,16→105,76 = 2,52 j ; FED 86,28→144,14 = 3,00 j. Les trois durées sont lisibles et exactes. **B2 de la passe 3 corrigé.** | ✓ |
| **2** | « la droite tiretée joint les débuts de zone, sa pente est la cadence » | `M40 24 … L498,98 206` : 65,57 px par zone = 3,40 j à 19,28 px/j. | ✓ |
| **2** | « ses sommets frôlent la ligne du parc » | Sommet de la courbe y = 245,36 ; ligne de parc y = 244,67. Échelle 0,02565 px/m² → 1 273 m² contre 1 300 : **0,69 px**. Exact au pixel. | ✓ |
| **2** | « elle oscille entre **deux et trois** zones ouvertes » | Trois niveaux : 267,13 (1 zone), 256,23 (2), 245,36 (3). Les quatre premiers jours sont à **une** zone, la fin descend à zéro. | ✗ **m2** |
| **2** | — | Toujours ni légende numérotée ni échelle ; les sept couleurs ne vivent que dans la prose. **m5 de la passe 3, non corrigé.** | ✗ **m3** |
| **3** — Gantt | durées du tableau S4a | COF 1,77 · FEP 2,52 (début 0,89) · FED 3,00 (**début 2,40**) · PTA 0,25 · BET 0,41 · CUR 2,00 · DEC 0,50. | ✓ (et **preuve de B2**) |
| **4** — effectifs | axe gradué, pointe cotée | Axe y de 0 à 25 par pas de 5, unité « personnes », pointe 29 cotée, moyenne 19,0. **M8 et m-axe de la passe 3 corrigés.** | ✓ |
| **4** | « les jours à zéro de la **fin** » | j31 = 0, j32 = 0, puis **j33 = 4** et **j34 = 4** (DEC + encadrement). Les zéros ne sont toujours pas à la fin. **m4 de la passe 3, non corrigé.** | ✗ |
| **5** — courbe en S | « le constat est UN point » | un seul point, à j = 19, à 45,0 %. | ✓ |
| **5** | « l'écart vertical, c'est SV, et il vaut ce que le tableau S6 annonce » | 15,8 pts × BAC 2 779 824 = 439 212 MAD contre SV = −437 822 : l'identité ne tient **que** par le prorata (B1). Le tableau S6 publie bien CV et SV désormais : **M10 de la passe 3 corrigé.** | ~ |

---

## 5. Tableau des défauts

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **B1 · La valeur acquise, la valeur planifiée et la courbe en S appliquent le prorata uniforme que le module condamne. D-023 n'a pas atteint le § S6.** | **bloquant** | `valeur_acquise.py` : `VA_A = BAC × (3 + 0,60)/8` ; `cycle_plancher.py:avancement_prevu` : `(j − début)/cycle`. Écart au modèle physique : **−15,5 %** à 20 % du cycle, **−25,7 %** à 70 %, et **−2,5 %** au seul point publié. Relevés posés **exactement** sur l'état physique : voie A 1 250 921 contre voie B 1 256 185, **0,421 %** résiduel pour une tolérance de 1 % — le seuil absorbe le biais. Canari **N4** : CPI, SPI et le contre-calcul restent **identiques** quand l'état physique est inversé. Le corrigé de l'exercice 4 refuse de viser une situation construite ainsi. | `VA = Σ (état_physique_du_poste × quantité × prix)` pour la zone en cours et pour chaque zone partielle de la VP. Publier l'avancement **en valeur** (61,5 %) à côté de l'avancement **en temps** (60 %) et commenter l'écart. Resserrer la tolérance à 0,2 %. |
| **B2 · Le taux de recouvrement est appliqué à son complément ; `data/`, la balise V3 et le registre H024 publient l'énoncé inverse de ce que le réseau fait.** | **bloquant** | `reseau_zone` : `[("FEP", -t["ferraillage_poutres_j"] * r2)]` → FED démarre à `fin_FEP − 0,40 × durée_FEP`, soit **60 %** de FEP fait. Mesuré sur la figure 3 : FEP 0,89→3,41, FED à **2,40** → 59,9 %. Balayage : 20 % → 80 %, 40 % → 60 %, 60 % → 40 %. Le premier recouvrement (50 %) est auto-complémentaire et masque le second. Cycle 8,557 j au lieu de **8,053** (+6,3 %). La passe 3 l'avait **mesuré** (sa ligne 5) et routé vers son M3 : la correction a inscrit l'énoncé faux dans le registre. | Choisir une sémantique, l'écrire dans `data/`, la balise et H024, et ajouter le test manquant : recalculer `(début_successeur − début_prédécesseur)/durée_prédécesseur` depuis le réseau et le confronter au paramètre. Ne plus retenir 50 % comme valeur de référence du premier recouvrement. |
| **B3 · Le planning publié est infaisable avec la grue déclarée ; la règle de cadence ne contrôle qu'une moyenne.** | **bloquant** | Balayage des fronts, 8 zones à 3,4 j, cycle 8,557 : **six conflits de 0,50 j** (Z1/DEC + Z3/COF à j 8,06–8,56, et ainsi de suite jusqu'à Z6/DEC + Z8/COF). La figure 2 les affiche. Occupation moyenne 67 % : la règle passe. La fiche mémo (contrôle n° 5) affirme que la comparaison « au parc **et** à la grue » est faite, et l'exercice 3 fait acheter une seconde grue sur cette base. | Niveler après le calcul : balayer les fronts et vérifier, ressource par ressource, que le nombre d'occurrences simultanées ne dépasse jamais l'effectif déclaré. Publier le profil d'occupation de la grue sous la figure 2. Lever si la contrainte mord, comme le contrôle de parc le fait déjà. |
| **M1 · Le rattachement poste → tâche d'`etat_physique_de_zone` — le cœur de la correction D-023 — n'est contrôlé par rien.** | majeur | Canari **N4** : coffrage ← BET et béton ← COF permutés, `calc/ : VERT`. Le module publierait « 0 m² de coffrage, 98,4 m³ de béton » pour une zone où le béton n'est pas coulé, avec `signal: True` sur les **deux** postes géométriques. Rien n'assert `un_poste_geometrique_derive == false` sur le cas publié ; rien ne confronte le rattachement à autre chose qu'à lui-même. L'affectation équipe → tâche, elle, a ses sept assertions. | Sept assertions symétriques : à `frac = 0`, tous les postes à zéro ; à `frac = 1`, tous à 100 % ; au milieu de COF seul, coffrage partiel et béton nul ; juste après BET, béton à 100 %. Plus une assertion : sur le cas publié, `un_poste_geometrique_derive` vaut `false`. |
| **M2 · Deux durées de plancher publiées pour le même cas de référence : 32,4 j et 32,5 j. m1 et m2 de la passe 3, déclarés corrigés, toujours vivants et désormais visibles.** | majeur | `cadence = round(regle_cadence["cadence_j"], 1)` → le planning tourne à **3,4 j** et rend 32,36 j ; `variante_effectif` prend `rc2["cadence_j"]` **non arrondi** → 3,42 j et 32,50 j. § S4d et énoncé de l'exercice 3 : « *le plancher complet prend 32,4 jours ouvrés* », « *25 jours au lieu de 32,4* ». Corrigé de l'exercice 2 : « *le plancher passe de **32,5** à 27,6 jours* ». L'arrondi `::n1` ne les masque plus. | Une seule cadence, arrondie une seule fois, en amont, et passée partout. Test : `planning_plancher.duree_totale_j == variantes.reference.duree_plancher_j`. |
| **M3 · `pointe_effectif` et la figure 4 ne sont pas calculés avec la même cadence ; une valeur légale les fait diverger.** | majeur | Canari **N7**, `recouvrement_coffrage_ferraillage_poutres_pct = 30`, **borne de sa propre fourchette déclarée [30 ; 70]** : échec « la pointe publiée est bien le maximum de l'histogramme — **29 contre 27** ». Même cause que M2 : la figure lit le planning à 3,4 j, la pointe vient de la variante à 3,42 j. À la valeur de référence, elles coïncident par chance. | Même correction que M2 : une cadence unique. |
| **M4 · 32 scalaires déclarés V3 dans `data/` n'ont ni balise ni ligne de registre — dont les quatre effectifs, qui entrent dans toutes les durées publiées.** | majeur | `build/check.mjs` ne retient que les feuilles portant **à la fois** `valeur` et `fourchette`. Échappent : `effectifs.coffreurs = 8`, `ferrailleurs_dalle = 8`, `ferrailleurs_poutres = 4`, `equipe_betonnage = 5`, `heures_par_jour = 8` (tous publiés tels quels dans le tableau S4a), `materiel.nb_grues = 1`, `materiel.etais_par_m2 = 2,5` (qui porte le « rapport de 2,33 sur un poste de location »), `suivi.jour_arret_ouvre`, `avancement_zone_en_cours_pct`, `cout_reel_constate_MAD`, les trois `quantites_relevees`, et la géométrie de `elements`. D-025 annonce « toute hypothèse V3 de `data/` est registrée » : c'est faux pour 32 valeurs sur 52. | Étendre le parcours à toute feuille numérique d'un bloc portant `niveau_preuve: "V3"`, et exiger pour chacune une fourchette **et** une ligne de registre, ou une mention `non_publiee` explicite. |
| **M5 · `8.56` — la durée du cycle — est toujours écrite en dur dans `_coherence_prix_horaire`, et elle alimente deux lignes publiées. M14 de la passe 3, déclaré corrigé.** | majeur | `cycle_plancher.py:299` : `h_enc = (e["chef_equipe"] + e["grutier"]) * h * 8.56`. Les lignes « + chef d'équipe et grutier » et « + prix horaire au haut de sa fourchette » du tableau S4c en descendent. § 4.3 : « aucun nombre technique n'est tapé à la main ». Et sous B2 corrigé, le cycle passerait à 8,05 : les deux lignes deviendraient fausses en silence. | `duree_zone` est déjà calculée dans le `__main__` : la passer à `cout_zone()` et à `_coherence_prix_horaire()`. |
| **M6 · `etat_physique_de_zone` et `cadence_rotation` — les deux fonctions créées par la passe 3 — ne passent aucune vérification dimensionnelle, alors que `verif_unites.py` affirme les couvrir.** | majeur | En-tête de `calc/verif_unites.py` : « vérification dimensionnelle (pint) de **CHAQUE** formule publiée par les bibliothèques de la tranche verticale ». Les quatre sections du fichier couvrent `plancher.py`, `durees_taches`/`cout_zone`, `cpm.py` et `valeur_acquise.py`. `cadence_rotation` divise des jours par un `nb_grues` sans dimension et multiplie par `(1 + m)` ; `etat_physique_de_zone` multiplie m², kg et m³ par une fraction de temps. Ni l'une ni l'autre n'apparaît. § 3.3. | Ajouter les deux sections, chacune avec son contre-contrôle qui doit lever. |
| **M7 · Aucune disposition de sécurité dans un module qui porte l'étaiement, le décoffrage, le travail en hauteur et le levage à la grue.** | majeur | Recherche sur `content/01-tranche-verticale-suivi.md` : **zéro occurrence** de « sécurité », « HSE », « risque », « chute », « effondrement », « garde-corps », « protection ». Le module traite un plancher à + 5,00 m, 1 273 m² de tables manutentionnées à la grue, 6 300 étais, un décoffrage et des étais de reprise. § 3.4 : « pour toute opération à risque (**étaiement et cintres**, travail en hauteur, levage lourd), le module donne les dispositions de sécurité essentielles et renvoie aux exigences réglementaires et au plan HSE du chantier ». L'option O4 de la fiche-module est cochée ✓, et sa définition (§ 6.2) inclut « sécurité ». La seule mention voisine — « contrôle la stabilité de l'étaiement » — est un point de visa, pas une disposition de sécurité. | Un paragraphe en § S7 (double lecture) et trois lignes dans la fiche mémo : protection des rives et trémies avant toute pose de coffrage, zone d'exclusion sous le décoffrage, vérification de l'étaiement et de ses semelles d'appui avant ferraillage, renvoi au plan HSE et à C7. |
| **M8 · `QA/grilles-72.md` note le module 3/3 sur « les formules sont justifiées » en citant la règle de cadence que le module répudie. m7 de la passe 3, déclaré corrigé.** | majeur | Le fichier porte : « *était 2 — la **règle de cadence** `max(coffrage, ferraillage) + bétonnage` est maintenant publiée et démontrée* ». Le module dit aujourd'hui de cette formule qu'elle « n'était justifiée par aucun modèle de ressources — c'était la marge, déguisée en contrainte ». Même ligne : « 10 V3 balisées et registrées » pour 22 lignes TV au registre. La grille n'a été mise à jour ni après la passe 2 ni après la passe 3. | Renoter la grille après **cette** passe, et faire du fichier une sortie du build plutôt qu'un document tenu à la main. |
| **M9 · `STATE.md` affirme deux garanties que le dépôt ne tient pas.** | majeur | « *toute grandeur décrivant l'état du chantier à une date est **dérivée du réseau** et un test refait la dérivation* » : la valeur acquise, la valeur planifiée et la courbe en S ne le sont pas (**B1**) ; aucun test ne refait la dérivation (**M1**, canari N4). Un bilan qui surestime ce qui est acquis est plus dangereux qu'un bilan absent — c'est l'argument que le module tient lui-même sur les contrôles habillés d'une explication. | Réécrire les deux phrases sur ce qui est réellement couvert, et porter B1 et M1 en dette tant qu'ils ne le sont pas. |
| **M10 · La fiche-module de `cadrage/05-sommaire.md` promet un socle S1–S8 complet et des données écrites : ni le glossaire ni l'écriture n'existent.** | majeur | S7 du § 6.1 = « check-list, **glossaire**, quiz » : aucune occurrence de « glossaire » dans `content/`. « Données écrites : `quantites.beton_m3.mezzanine`, `planning.taches[]`, `effectifs.*` » : `data/projet-gare.json` porte toujours `quantites.beton_m3 = {}` et `planning.taches = []`. La chaîne `data/ → calc/` est à sens unique, alors que le § 10.2 impose que chaque étape « lise **et écrive** `projet-gare.json` ». | Ajouter le glossaire (une douzaine d'entrées : zone de coulage, cadence, cycle, rotation, étai de reprise, attachement, situation, point d'arrêt, valeur acquise, CPI, SPI, EAC). Écrire les quantités et le planning calculés dans `data/`, ou corriger la fiche-module et le consigner. |
| m1 · Figure 1 : « les lignes tiretées sont les poutres intermédiaires, **au milieu de chaque zone** » | mineur | 15 lignes au pas de 7,50 m : 8 au milieu, **7 sur les limites de zone**. | « une ligne de poutres tous les 7,50 m ; une sur deux tombe sur une limite de zone, c'est là que se fait la reprise ». |
| m2 · Figure 2 : « elle oscille entre deux et trois zones ouvertes » | mineur | Trois niveaux mesurés (1, 2, 3 zones) ; les quatre premiers jours sont à **une** zone. | « elle monte à trois zones ouvertes en régime, après une montée en cadence à une puis deux ». |
| m3 · Figure 2 : ni légende numérotée ni échelle. **m5 de la passe 3, non corrigé.** | mineur | Directive `:::figure` sans clé `legende` ; les sept couleurs ne sont nommées que dans « ce qu'il faut voir ». § 8 : « éléments numérotés + légende ». | Bandeau de sept pastilles de couleur légendées, généré par `rotation()`. |
| m4 · Figure 4 : « les jours à zéro de la **fin** ». **m4 de la passe 3, non corrigé.** | mineur | Séquence réelle : j31 = 0, j32 = 0, j33 = 4, j34 = 4. | « les deux jours à zéro, qui sont la cure de la dernière zone ». |
| m5 · Registre : H014 et H019 sont la **même** hypothèse, enregistrée deux fois avec deux valeurs différentes. | mineur | « part de main d'œuvre directe dans un prix posé » = `22 %` en H014 et `15 à 30 %` en H019. Le compte « 27 hypothèses » de D-025 en vaut donc 26. | Fusionner, et ajouter au build un contrôle d'unicité de l'énoncé. |
| m6 · La docstring de `cadence_rotation` contredit `data/`. | mineur | « *Ici la grue sert au coffrage, **au coulage** et au décoffrage* » ; `taches_servies_par_la_grue = ["coffrage_j", "decoffrage_j"]`, et `data/` explique longuement que le béton arrive par pompe. | Supprimer l'énumération de la docstring : la liste est dans `data/`, c'est tout l'objet de D-024. |
| m7 · `equipe_qui_borne` nomme une équipe même quand c'est la grue qui borne. | mineur | `cycle_plancher.py` : `"equipe_qui_borne": equipes[cle_equipe]` est rendu inconditionnellement, alors que `ressource_qui_borne` et `tache_qui_borne`, eux, sont conditionnels. La variante « deux équipes » publie `ressource_qui_borne = grue (partagée)` et `equipe_qui_borne = ferrailleurs_dalle`. | Rendre `null` quand la grue borne, ou renommer en `equipe_la_plus_chargee`. |
| m8 · `suivi.jour_arret_ouvre` n'est ni borné, ni registré, et déplace 5 % de la VP. | mineur | Canari **N5** (jour 20) : tous les contrôles verts, VP de 1 688 743 à 1 772 138 MAD, SPI de 0,741 à 0,706. Cas particulier de M4. | Lui donner une fourchette et une ligne de registre, comme aux autres V3. |
| m9 · Figure 4 : le grutier est compté les jours où seule l'équipe de bétonnage tourne. | mineur | `histogramme_plancher` ajoute `chef_equipe + grutier` dès que `n > 0`. Or `data/materiel` dit que le béton arrive par **pompe automotrice** et que la grue ne sert pas au coulage — c'est le fondement de la règle de cadence. | Rattacher le grutier aux tâches de grue déclarées, comme la cadence le fait déjà. |
| m10 · Conventions de jour mélangées entre les figures et le libellé de la date d'arrêt. | mineur | Les axes des figures 2, 4 et 5 comptent à partir de **0** (temps écoulé) ; `libelle_arret` calcule `((19 − 1) % 5) + 1` et publie « jour 19, 4ᵉ jour de la semaine 4 », en comptant à partir de **1**. À t = 19,0 écoulé, on est dans le 20ᵉ jour. | Une convention unique, dite une fois, et le libellé dérivé d'elle. |
| m11 · `coffrage_immobilise` est toujours échantillonné aux instants entiers. | mineur | `cycle_plancher.py` : `debuts[Zi] <= k < debuts[Zi] + duree_zone` pour `k` entier. La correction par **intersection** avec `[k, k+1)` n'a été appliquée qu'à l'histogramme. Sans effet visible ici (le cycle fait 8,56 j), mais le défaut est le même et reviendra sur un cycle court. | Même règle d'intersection que l'histogramme, ou un maximum sur l'intervalle. |

**3 bloquants · 10 majeurs · 11 mineurs = 24 défauts.**

---

## 6. Ce que les corrections de la passe 3 ont réellement donné

Je dois le dire : **la plupart tiennent**, et certaines sont bonnes.

| Correction annoncée | Constat |
|---|---|
| B2 p3 — figure 2, phases peintes l'une sur l'autre | **Tient.** Mesure sur le SVG : COF 1,77 j, FEP 2,52 j, FED 3,00 j, toutes lisibles sur leur propre sous-bande. |
| M8 p3 — histogramme échantillonné aux instants entiers | **Tient.** Règle d'intersection avec `[k, k+1)` ; les huit bétonnages apparaissent. |
| M8 p3 — axe absent de l'histogramme | **Tient.** Axe gradué, unité, pointe cotée. |
| M4 p3 — aucune V3 confrontée à sa fourchette | **Tient** pour les 20 feuilles `{valeur, fourchette}` ; ne couvre pas les 32 autres (**M4**). |
| M13 p3 — permutation de `effectif_par_tache` indétectable | **Tient.** Sept assertions nommées ; le canari sonne. |
| M5 p3 — `zones_etayees` non bornée | **Tient.** Bornée à `nb_zones`, saturation signalée. |
| M10 p3 — SV absent du tableau S6 | **Tient.** CV et SV publiés. |
| M11 p3 — étalonnage de `valeur_acquise` qui n'appelait pas la bibliothèque | **Tient.** `valeur_acquise()` est appelée, et le cas faux doit lever. *Réserve* : le cas fermé pose son `attendu` sur le modèle linéaire, donc il entérine **B1**. |
| M9 p3 — points de phrase convertis en virgules | **Tient.** `lecture` est accentuée et ponctuée. |
| M6, M7 p3 — rapports tapés à la main, balise recopiée | **Tient.** `rapport_etais` est calculé. |
| M14 p3 — `8.56` écrit en dur | **NE TIENT PAS** (→ **M5**). |
| m1, m2 p3 — deux cadences, deux durées de plancher | **NE TIENT PAS**, et c'est désormais visible (→ **M2**, **M3**). |
| m4, m5, m7 p3 — figure 4, figure 2, grille 7.2 | **NE TIENNENT PAS** (→ **m4**, **m3**, **M8**). |
| M3 p3 — V3 sans registre | **Tient à moitié**, et sa correction a **entériné B2** en inscrivant l'énoncé faux dans H024. |
| B1 p3 — avancement au prorata uniforme | **Tient à moitié.** Corrigé dans les quantités physiques et le recoupement ; **jamais appliqué à la valeur acquise, à la VP ni à la courbe en S** (→ **B1**). |

---

## 7. Grille du § 7.2

| Critère | Note | Appui |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | Chaque mécanisme est justifié avant d'être montré ; le § S2 fonde la zone comme unité par quatre propriétés simultanées. |
| Les hypothèses sont explicites | **1** | 32 scalaires V3 hors registre, dont les quatre effectifs publiés tels quels (**M4**) ; et l'énoncé de **deux** hypothèses registrées (H023, H024) dit l'inverse de ce que le code en fait (**B2**). Le module *dit* distinguer trois familles de nombres ; sur les hypothèses de conduite de chantier, il ne le fait pas. |
| Les formules sont justifiées | **2** | La règle de cadence est désormais posée sur un modèle de ressources, démontrée et publiée avec sa marge — c'est un vrai progrès. Mais elle n'est qu'une condition de moyenne et le planning qui en sort viole la ressource (**B3**), et deux fonctions ne passent aucune vérification dimensionnelle (**M6**). |
| L'exemple est vérifié | **1** | Le cœur de la correction D-023 n'est vérifié par rien (canari **N4** vert), la valeur acquise tourne sur le modèle que le module condamne (**B1**), et deux grandeurs de référence sont publiées en double (**M2**, **M3**). |
| Le piège est identifié | **3** | Six pièges chiffrés, plus trois que le module s'applique à lui-même. C'est le meilleur critère du module. |
| Lien avec l'exécution | **2** | Double lecture entreprise/MOE, point d'arrêt modélisé comme tâche critique, contrainte de parc : solide. Mais **aucune disposition de sécurité** sur un module d'étaiement et de travail en hauteur (**M7**). |
| Lien avec le coût et le délai | **2** | C'est l'objet du module et la chaîne est complète ; les indicateurs d'arrivée reposent sur un modèle faux (**B1**). |

**Minimum de 2 partout : NON TENU** — deux critères à 1.

---

## 8. La question de fond : la cinquième erreur

Elle existe, et elle est triple.

Les trois passes précédentes ont trouvé la même famille : **un modèle faux sous une arithmétique juste**.
Cette passe en trouve trois de plus, et les trois ont le même mécanisme de survie :

1. **Un point de fonctionnement qui masque l'écart.** Le premier recouvrement vaut 50 %, valeur
   auto-complémentaire : les deux lectures du paramètre y coïncident exactement, et le second
   recouvrement passe inaperçu derrière (**B2**). L'avancement vaut 60 % du cycle : c'est la seule
   fenêtre, large d'environ cinq points, où le modèle linéaire et le modèle physique se croisent — à
   70 % l'écart vaut 25 points (**B1**). La grue est à 67 % d'occupation moyenne : assez pour que la
   règle passe, pas assez pour que le planning soit faisable (**B3**).
2. **Un contrôle réglé plus large que le biais.** Le contre-calcul de la valeur acquise tolère 1 % ; le
   biais du modèle vaut 0,42 % sur un chantier parfaitement conforme. Le module enseigne lui-même, au
   § S6, qu'« un seuil n'a de sens qu'au regard de l'incertitude de ce qu'il mesure ». Il n'a pas été
   appliqué à ce seuil-là.
3. **Une prose qui tient lieu de contrat.** La sémantique du recouvrement vit dans une note de `data/`,
   une balise et une ligne de registre — trois textes que **rien n'exécute**. Le rattachement poste →
   tâche vit dans un commentaire (« le coffrage est POSÉ pendant COF »). Un commentaire n'est pas un
   test : le canari N4 l'inverse et tout reste vert.

Et il faut dire le pire : la passe 3 **avait mesuré B2**. Sa ligne 5 publie « cycle, lecture littérale de
`data` = 8,048 j contre 8,557 ✗ ». Elle l'a routé vers un défaut de registre ; la correction a ajouté la
ligne de registre **en y recopiant l'énoncé faux**. Un défaut vu, mal classé, puis gravé.

**Ce qui marche désormais, et qu'il faut garder.** Le dépôt a maintenant quatre représentations
réellement indépendantes, et chacune a prouvé son utilité pendant cette passe :
le **réseau** (CPM par deux algorithmes, étalonné sur neuf cas fermés), les **quantités relevées**
(voie B de la valeur acquise, qui ne passe ni par le budget ni par l'avancement déclaré), le **SVG rendu**
(où j'ai mesuré B2 au pixel), et les **fourchettes déclarées** (d'où sortent les canaris N2 et N7). Ce qui
manque n'est pas une cinquième représentation : c'est de les **confronter**. Aucun test ne confronte le
réseau à la valeur acquise, ni le paramètre déclaré au réseau qu'il engendre, ni le planning à ses propres
ressources. Les quatre vivent côte à côte sans jamais se contredire, et c'est précisément pour cela que
trois modèles faux y survivent.

> **La règle à inscrire dans `DECISIONS.md` avant toute duplication** : toute grandeur déclarée dans
> `data/` en mots doit avoir un test qui **relit cette grandeur dans le résultat** et la compare à sa
> déclaration. Pas « la formule est appliquée » — « le réseau produit bien ce que l'énoncé promet ».

---

## 9. Verdict

**3 bloquants · 10 majeurs · 11 mineurs.**

**Zéro bloquant ? NON.**

**Ce module peut-il servir de modèle à la duplication (§ 5.3) ? Pas encore — mais il n'en est plus loin,
et la raison du refus a changé.**

La forme est bonne et stable : la chaîne `data → calc → rendu` tient, les cinq figures sont générées,
mesurables et deux d'entre elles sont maintenant exactes au pixel, la double lecture entreprise/MOE est au
bon niveau, les pièges sont les meilleurs du dépôt, et sur les seize corrections de la passe 3, onze
tiennent. Ce n'est plus un module fragile ; c'est un module dont **trois modèles mentent sur ce qu'ils
font**.

Dupliquer maintenant reviendrait à dupliquer cela : un indicateur de reporting qui applique le prorata
que son propre encart interdit (**B1**), un paramètre de planning dont l'énoncé publié est l'inverse de
son effet (**B2**), et une règle de ressources qui valide une moyenne en publiant un planning infaisable
(**B3**) — dans un cours destiné à un **Chef de Projet Suivi**, dont ce sont précisément les trois gestes
du métier.

**Ce que je recommande.** Corriger B1, B2, B3 et M1 — quatre corrections, toutes dans `calc/`, toutes
testables —, puis une passe n° 5 **courte**, bornée à ces quatre points et à leurs tests, avant le go de
l'Étape 2. Les majeurs M2 à M10 et les onze mineurs peuvent partir en dette déclarée dans `STATE.md` sans
bloquer la duplication, à l'exception de **M7** (sécurité), qui doit être traité avant que le gabarit ne
soit recopié sur C1 à C8 : un module d'exécution sans disposition de sécurité est un gabarit qu'on ne veut
pas dupliquer cinquante fois.
