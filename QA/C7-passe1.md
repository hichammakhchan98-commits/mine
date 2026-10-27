# C7 — Qualité, HSE, environnement · passe adversariale n° 1

> Relecteur hostile, indépendant de l'auteur. Les commentaires de `calc/qualite.py` et les encarts
> du module ont été lus **comme des affirmations à vérifier**, jamais comme des preuves. Les trois
> captures ont été ouvertes et regardées. Tests automatiques au moment de la passe : **16/16 verts**,
> `test_qualite.py` 56 contrôles verts, `verif_unites.py` vert. Aucun des défauts ci-dessous n'est
> vu par ces contrôles.

---

## 0. Contre-expertise à l'aveugle

Recalculs faits en `python3` **depuis `data/projet-gare.json` et `calc/sorties/planification.json`
seuls**, avant toute lecture de `calc/qualite.py`.

### 0.1 Les heures et la part de nuit

```
h = planification.json → heures_de_main_oeuvre_par_tache        (27 tâches)
nuit = projet-gare.json → planning.contraintes_exploitation.taches_soumises = [CHLV, PSOU]

total   = Σ h                      = 58 260,6 h
h_nuit  = h[CHLV] + h[PSOU]        = 2 918,4 + 1 732,3 = 4 650,7 h
h_jour  = 53 609,9 h
part de nuit en heures             = 4 650,7 / 58 260,6 = 7,98 %
```
→ **concorde** avec `qualite.json` (58 260,6 h · 4 650,7 h · 7,98 %). Publié : 58 261 h, 8,0 %.

**Mais** : trois tâches pèsent **0 h** — `CHET` (études charpente, 40 j), `CHFA` (**fabrication de
312 t de charpente en atelier, 60 j**), `SECH` (séchage, 20 j). Et `SECO` vaut **27 000 h, soit
46,3 % de toute l'assiette** : un lot second œuvre / lots techniques à 45 personnes, c'est-à-dire
très probablement sous-traité. Voir B13, M4, M5.

### 0.2 Les heures pondérées et le nombre d'accidents

```
k = 1,8
h_pond = h_jour + k·h_nuit = 53 609,9 + 8 371,3 = 61 981,2 h
part de nuit dans le risque = 8 371,3 / 61 981,2 = 13,51 %
accidents = TF · h_pond / 1e6 = 28 × 61 981,2 / 1e6 = 1,7355   → publié 1,74
```
→ les nombres **se reproduisent**. Mais je recalcule aussi la version **non pondérée** :
```
accidents = 28 × 58 260,6 / 1e6 = 1,6313   → 1,6
```
**C'est le nombre qu'écrit le module lui-même dans son encart** (« Annoncer « nous aurons 1,6
accident » »), à côté d'un tableau qui en publie 1,74. Voir B1 et B6.

### 0.3 Le coût de la non-conformité, ligne par ligne

```
reprise      = 48 m² × 420 MAD/m²                                   =  20 160,00 MAD
h de contrôle supplémentaires = 22 × 1,5 h × 25 %                   =       8,25 h
durcissement = 8,25 h × 45 MAD/h (prix_unitaires.main_oeuvre_h)     =     371,25 MAD
frais de durée (prix.json → bordereau.frais_de_duree)               = 16 240,33 MAD/j ouvré
attente de décision = 4 j × 16 240,33                               =  64 961,32 MAD
durée de reprise    = 3 j × 16 240,33                               =  48 720,99 MAD
TOTAL                                                               = 134 213,56 MAD
part visible = 20 160 / 134 213,56                                  =  15,02 %
```
→ **arithmétiquement reproductible**. Mais deux des quatre lignes sont **illégitimes** et une
troisième est calculée au mauvais taux : voir B3 et M3. Recalculé proprement, le coût de cette NC
sur **cet** ouvrage vaut **20 531 MAD, dont 98,2 % visibles sur un devis** — soit l'exact inverse de
la thèse publiée.

Et le même calcul aux bornes des fourchettes déclarées dans `data/` :
```
borne basse  = 20×250 + (1+1,5)×16 240 + 10×0,5×0 %×35   =  45 601 MAD
borne haute  = 120×700 + (10+6)×16 240 + 40×3×60 %×60    = 348 165 MAD
```
**×7,6 d'étendue**, pour un nombre publié à la **dizaine de centimes** (134 213,56 MAD sur la
figure 2). Voir M1, M2.

### 0.4 Le tonnage de déchets

```
emprise = 120 × 40 = 4 800 m²
38,0 ×4 800/1000 = 182,4 t (80 % → 145,9)      4,5 → 21,6 t (95 % → 20,5)
 6,0 →  28,8 t (60 % →  17,3)                  3,5 → 16,8 t (40 % →  6,7)
 0,4 →   1,92 t (0 %)
TOTAL 251,5 t · valorisé 190,4 t · taux 75,72 % · part dangereuse 0,76 %
```
→ **concorde** (251,5 t · 75,7 % · 0,76 %). Bornes des fourchettes : **127,7 t … 481,0 t**, jamais
publiées (M1).

### 0.5 Vérifications supplémentaires

| Objet | Mon recalcul | Publié | Verdict |
|---|---|---|---|
| Criticités f×g×d | 24 ×5, 16 ×2, 12 ×1 | idem, « cinq ex æquo » | **juste** |
| Classement secondaire par g | 4,4,4 puis 2,2 parmi les 24 | idem | **juste** |
| TF exercice 1 | 2e6/21 600 = 92,6 → 93 ; 5e6/108 000 = 46,3 → 46 | 93 et 46 | **juste** |
| Amplification CHLV | 48,64 → 17 fenêtres (fin 460,64) ; 55,64 → 19 fenêtres (fin 501,64) ; Δ = **41,0 j** | 41,0 j | arithmétiquement reproductible, **mais l'entrée est fausse** (B4) |
| Marge de NOYX, l'ouvrage du cas d'étude | **436,39 j** | 436,4 j | **juste — et il tue le § S4a** (B3) |

---

## 1. Les dix points du § 12.2

**1 · Unités et homogénéité dimensionnelle.** **DÉFAUT.** Deux problèmes distincts.
(a) `impact_sur_le_planning` fait `t[tache]["duree_j"] += 7`. Pour CHLV, `duree_j` **n'est pas en
jours** : `planification.json → durees.CHLV.unite` dit littéralement *« plages de consignation, et
non journees de 8 h »* (48,64 plages = 12,13 j de travail de jour × facteur d'interception 4,01).
On additionne 7 jours ouvrés à 48,64 plages. (B4)
(b) `heures_ponderees_par_le_risque` est manipulé comme des heures — `verif_unites.py:280` lui
attache `u.hour` à la main — alors que c'est une grandeur sans dimension physique (une somme
pondérée). La vérification dimensionnelle valide l'étiquette que l'auteur a posée, pas la grandeur.
(B1)

**2 · Référentiels mélangés.** **DÉFAUT.** Le § S4g invoque le **PPSPS** et le **plan de prévention**
(instruments du Code du travail **français** : décrets 94-1159 et 92-158), et le glossaire pose le
**bordereau de suivi** comme obligation. Le cadre du cours est marocain (CPS, CCAG-T, § 1 de
CLAUDE.md). Aucun V0, aucun ⚠, aucun ⏸ — alors que le mémo du même module range « obligations de
tri » en ⏸. (B11)

**3 · Article cité sans V0 ni V1.** **DÉFAUT**, même point que ci-dessus : trois obligations
réglementaires énoncées comme des faits. Aucune ligne C7 dans `registre-sources.csv` (0).

**4 · Ordres de grandeur et ratios.** **DÉFAUT.** Aucun nombre publié ne porte sa fourchette, alors
que `data/` les porte toutes et que **D-036** l'exige. Étendues recalculées : coût de NC ×7,6,
accidents 0,71–3,38, part de nuit dans le risque 9,4–20,7 %, déchets 128–481 t, journées perdues
35,5–202,7. (M1)

**5 · Cohérence data / SVG / 3D / métré / coût / planning.** **DÉFAUT GRAVE.** La figure 1 est triée
et coupée sur une grandeur (le risque pondéré) et affiche une autre (les heures) : barres dans le
désordre, et une tâche à 1 120 h absente d'un graphique qui en montre une à 1 088 h. (B7) Le cas
d'étude du § S4a et le tableau du § S4b portent sur le **même** ouvrage et se contredisent. (B3)
Trois plans de contrôle du même chantier (C3, B3e, C7) s'attribuent les mêmes contrôles à des
acteurs différents. (M15)

**6 · Grille de profondeur (§ 7.2).** **DÉFAUT** sur deux critères : « les hypothèses sont
explicites » (l'assiette des heures et son incomplétude ne sont jamais dites) et « l'exemple est
vérifié » (aucune seconde voie ; O7 revendiqué, inexistant). Note détaillée au § 3.

**7 · Sécurité : conseil dangereux ou omission.** **PARTIELLEMENT RAS.** Je ne trouve **aucun
conseil dangereux** : les parades sont justes, le module refuse toute distance et tout seuil, il
pose explicitement qu'un risque de gravité 4 se traite quel que soit son rang (S4g, quiz 7), et la
phrase « une parade qui dépend de la vigilance de celui qui prend le risque n'est pas une parade »
est **défendable** — c'est la hiérarchie classique protection collective > protection individuelle,
et le module la décline correctement en matérielle / organisationnelle / géométrique. **Mais deux
omissions** : (a) le module conclut que « la prévention se met là où sont les heures » alors que son
assiette d'heures ignore l'atelier de fabrication (CHFA, 312 t, soudage et CND) — il envoie la
prévention au mauvais endroit par construction (M4) ; (b) une pièce de charpente est décrite comme
ayant un « défaut d'enrobage » (M17), ce qui désigne un désordre inexistant et brouille le geste de
contrôle.

**8 · Vérité du rendu.** **DÉFAUT GRAVE.** Figure 3 : libellé tronqué à 46 caractères, affiché
« Chute de hauteur depuis un coffrage ou une **pas** » — mot coupé, et contredisant le tableau situé
juste au-dessus qui écrit « passerelle ». (B8) Figure 2 : la 4ᵉ barre a une hauteur nulle, son
étiquette flotte sans barre, et les montants sont affichés **au centime** (134 213,56). (M2, m3)
Dans le corps du texte, `.replace(",", " ")` a supprimé les **virgules de ponctuation** des chaînes
calculées : « heures travaillees dont 4 651 », « 114 054 MAD  soit 85 % », « ce module et il ne se
voit ». (M10) Ces blocs sont de surcroît **sans accents** dans un cours français. (M11) Et les
séparateurs décimaux sont mélangés sur la même page : « 13.5 % » (chaîne calculée) et « 13,5 % »
(variable formatée). (M12)

**9 · Simplifications non signalées.** **DÉFAUT.** Quatre, toutes muettes : l'assiette d'heures
exclut l'atelier et les études (M4) ; « heures de nuit » est posé comme équivalent à « heures sous
consignation » sans que la donnée le dise (m7) ; les frais de durée sont imputés sans vérifier que
l'ouvrage porte la date (B3) ; le taux de contrôle est un taux de compagnon (M3).

**10 · Texte télégraphique ou remplissage.** **RAS.** La prose est dense, argumentée, chaque
paragraphe porte une règle ou un chiffre. C'est la qualité incontestable de ce module. Seule
réserve : le § S4g, le quiz et le mémo répètent trois fois la même règle marge/gravité.

---

## 2. Défauts

### Bloquants

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **B1 · Double compte de la pondération de nuit : un taux mesuré sur des heures réelles est appliqué à des heures pondérées, et crée du risque ex nihilo** | bloquant | `calc/qualite.py:47-48` : `h_pond = h_jour + k*h_nuit` puis `accidents = tf * h_pond / 1e6`. TF = 28 est défini (données, note) comme « accidents avec arrêt **par million d'heures travaillées** » — une statistique de branche mesurée sur des heures **réelles**, qui contient déjà la part moyenne de travail de nuit de la population de référence. Le module l'applique à 61 981 « heures » qui n'existent pas. Conséquence mesurée : 28 × 58 260,6/1e6 = **1,63** devient 1,74, soit **+6,4 % d'accidents créés par un changement de pondération**. Signature du double compte : porter k à sa borne haute (3,0) fait passer le total à **1,89** — le chantier devient plus dangereux **au total** parce qu'on a changé un coefficient de répartition. Même faute sur `journees_perdues_attendues` (TG × h_pond). | Une pondération **répartit**, elle n'ajoute pas. Garder `accidents_attendus = TF × heures_totales` (1,63) et n'utiliser k que pour la **clé de répartition** jour/nuit : 13,5 % × 1,63 = 0,22 accident de nuit, 1,41 de jour. Ou, si l'on veut un taux de nuit propre, poser TF_nuit = k·TF_jour avec TF_jour calibré pour que le mélange redonne TF. Le mémo et la figure 1 suivent. |
| **B2 · Deuxième double compte : l'abattement de cadence de nuit est déjà dans les heures de nuit, et k le recompte** | bloquant | `calc/plage.py:63-66` : `facteur_d_interception = 8 / travail_effectif_h / (1 - abattement)` avec `abattement_de_cadence_nuit_pct = 30` ⇒ 8/2,85/0,70 = **4,01**. Ce facteur gonfle la durée de CHLV de 12,13 j à 48,64 plages, donc gonfle ses **heures** de 970 h à 2 918 h. Or la note de `abattement_de_cadence_nuit_pct` dit : *« éclairage artificiel, fatigue, zone étroite, co-activité avec l'agent de sécurité »*. Et la note de `surexposition_du_travail_de_nuit` (k = 1,8) dit : *« éclairage artificiel, fatigue, zone étroite, co-activité ferroviaire »*. **Mot pour mot la même cause physique, appliquée deux fois** : une fois en gonflant les heures (×1/0,7), une fois en gonflant chaque heure (×1,8). | Séparer les deux mécanismes dans les données et le dire : l'abattement de cadence est une perte de **rendement** (elle augmente le temps de présence, donc l'exposition, et c'est déjà compté) ; k ne doit couvrir que ce qui rend une **heure de présence** plus dangereuse à travail égal (visibilité, co-activité voie). Réécrire la note de k en excluant explicitement la fatigue/le rendement, et recaler sa valeur. |
| **B3 · La NC est chiffrée avec 113 682 MAD de frais de durée sur un ouvrage dont le module montre deux sections plus loin que le retard est nul** | bloquant | Le cas d'étude est `data → qualite_hse.non_conformite.ouvrage = "voile de noyau"` = tâche **NOYX**. `qualite.json → impact_planning.lignes[2]` : NOYX, **marge totale 436,39 j, retard du chantier 0,00 j, absorbée**. Pourtant `qualite.py:116-123` impute 4 j + 3 j × 16 240,33 MAD/j = **113 682 MAD** de frais de durée à cette même NC, soit **85 % du total publié**. Or `prix.json → bordereau.frais_de_duree` est le coût fixe de **prolongation du chantier** (encadrement + base-vie + grue + énergie, au mois calendaire) : il n'existe que si la **date de fin bouge**. Elle ne bouge pas. Pire, le module le sait et l'écrit : « Le decalage du cycle n'est chiffre ici **qu'en frais de duree, et seulement si l'ouvrage est sur le chemin critique**… ce qui se MESURE en rejouant le reseau » — il énonce la condition, et ne la vérifie pas. C'est **exactement** le défaut que **D-040** a corrigé dans C3 (« il imputait 154 611 MAD à un parc de coffrage qui ne retardait rien »), reproduit à l'identique. | Rejouer le réseau pour l'ouvrage **du cas d'étude** et n'imputer les frais de durée que du retard mesuré. Sur NOYX : **0 MAD**. Le coût devient 20 531 MAD, **98 % visibles sur un devis** — et la thèse du module s'inverse. Deux sorties honnêtes : (a) déplacer le cas d'étude sur un ouvrage qui porte la date, et le dire ; (b) garder le voile de noyau et **remplacer** les frais de durée par ce qui se paie vraiment sans retard (immobilisation de l'équipe et du coffrage pendant 7 j, marge consommée), en chiffrant cette immobilisation-là. Dans les deux cas, 85 %, 15 %, 134 214 MAD, le mémo, le quiz 3 et la ligne S5 changent. |
| **B4 · Erreur d'unité au cœur du résultat vedette : 7 jours ouvrés ajoutés à une durée exprimée en plages de consignation** | bloquant | `calc/qualite.py:194` : `t[tache]["duree_j"] = round(t[tache]["duree_j"] + jours, 2)`, avec `jours = 7` (4 j de décision + 3 j de reprise, des **jours ouvrés ordinaires**). Pour CHLV, `planification.json → durees.CHLV` porte `"unite": "plages de consignation, et non journees de 8 h"` et `facteur_d_interception: 4.01`. On ajoute donc 7 jours à 48,64 **plages**. Converti correctement, 7 jours ouvrés d'immobilisation ne font pas « 7 plages de plus de travail » : une immobilisation est un **arrêt**, pas un supplément de contenu de travail. Le +41 j est le produit arithmétique exact de cette confusion (48,64 → 55,64 ⇒ 17 → 19 fenêtres ⇒ 2 × 20 j + 1 j). | Modéliser une immobilisation comme un **décalage de début** (`debut_impose += 7`) ou comme une indisponibilité, pas comme un allongement de durée. Et, pour une tâche sous consignation, exprimer l'immobilisation en **plages ratées**, qui est la grandeur physique. Le chiffre de 41 j et toutes les phrases qui en dépendent (S4b, encart, exercice 2, S5, mémo, **D-048**) sont à recalculer. |
| **B5 · La règle publiée — « une NC se hiérarchise sur sa marge » — est réfutée par le tableau qui est censé la démontrer** | bloquant | `qualite.json → impact_planning.lignes` : CHLV marge **-0,0 j** → 41,0 j ; COUV marge **-0,0 j** → 7,0 j. **Deux tâches de marge identique, deux retards dans un rapport de 6.** La marge n'explique donc rien de la différence entre les deux premiers régimes ; c'est la **consignation** qui l'explique. Le module publie pourtant, en citation encadrée : *« Une non-conformité se hiérarchise sur sa marge, pas sur sa gravité technique »*, et l'exercice 2 fait raisonner le lecteur par la marge seule (« touche une tâche à marge nulle … il coûte 41 jours »), ce qui donnerait 7 j sur COUV. Le tableau affiche de surcroît « 0,0 j » et « 0,0 j » dans la colonne *Marge totale* pour deux lignes étiquetées « amplifié » et « transmis » : un lecteur attentif voit l'incohérence à l'œil nu. | Énoncer la règle juste : **une NC se hiérarchise sur ce que le réseau en fait**, et le réseau dépend de la marge **et du régime d'accès** (libre, contraint par fenêtres). Trois régimes, trois causes : marge, marge nulle, fenêtre. Reformuler la citation, l'encart, l'exercice 2, la ligne S5, le quiz 4, le mémo et **D-048**. |
| **B6 · Le module publie deux nombres d'accidents différents sur la même page** | bloquant | Tableau du § S2 : « Accidents avec arrêt attendus **1,74** ». Encart immédiatement en dessous (`qualite.py:73`, rendu tel quel) : « Annoncer « nous aurons **1,6** accident » serait aussi faux… ». Vérifié dans le rendu : les deux apparaissent à huit lignes d'écart. 1,6 est exactement la valeur **non pondérée** (28 × 58 260,6/1e6 = 1,631) : la prose a été écrite avant l'ajout de la pondération et n'a pas été reprise. Elle est donc aussi la **preuve interne** de B1 — l'auteur raisonnait, lui, sur les heures réelles. | Supprimer le nombre en dur de la chaîne `_ce_que_le_nombre_d_accidents_n_est_pas` et y injecter la variable (§ 4.3 : aucun nombre technique tapé à la main). Et corriger la valeur après B1. |
| **B7 · La figure 1 est triée et coupée sur le risque pondéré, mais son titre, sa légende et son axe annoncent des heures** | bloquant | `calc/qualite.py:384-386` : `figures.exposition` prend `exp["par_tache"][:10]` — liste triée par `part_du_risque_pct` (`qualite.py:86`) — et affiche `x["heures"]`. **Capture `tests/captures/08-c7-qualite-hse.html-figure1.png` ouverte et regardée** : les barres ne décroissent pas. CHLV **2 918,4** est placé au-dessus de QUAI **3 360** ; PSOU **1 732,3** au-dessus de NOYX **2 400** et de FACA **1 920**. Et la coupe à 10 par le risque **exclut MARQ (1 120 h)** d'un graphique qui affiche FOND (1 088 h) : la figure intitulée « Où sont les heures travaillées » omet une tâche qui en a davantage que la dernière montrée. La légende aggrave : « C'est pour cela qu'on **classe par heures** et non par durée ». Le test censé la couvrir (`test_qualite.py` : « la figure d'exposition porte des heures, pas des durees ») ne vérifie que l'appartenance des valeurs, jamais l'ordre. | Choisir : soit trier et couper **par heures** (et la légende devient vraie), soit faire une figure du **risque pondéré** et changer titre, axe et légende. Ne pas mélanger. Ajouter un test d'ordre décroissant sur toute figure en barres classée. |
| **B8 · Figure 3 : libellé tronqué au milieu d'un mot, en contradiction avec le tableau situé juste au-dessus** | bloquant | `calc/qualite.py:391` : `x["risque"][:46]`. **Capture `…-figure3.png` ouverte et regardée** : première barre étiquetée « Chute de hauteur depuis un coffrage ou une **pas** ». Le tableau du § S4d, trois lignes plus haut, écrit « …ou une **passerelle** ». Violation directe de la grille § 8 (« texte lisible », « cohérence avec le calcul ») et du § 12.1.c. Le contrôle de collision d'étiquettes passe parce qu'une étiquette tronquée ne chevauche rien. | Supprimer la troncature et laisser la mise en page gérer (les libellés tiennent : le plus long fait 52 caractères), ou tronquer sur mot entier avec une ellipse. |
| **B9 · Exercice 2 : « Le rapport est de 1 à 41 » alors que le module chiffre lui-même l'autre terme à 0** | bloquant | `content/08-c7-qualite-hse.md:289-295`, rendu vérifié : « sa reprise coûte de l'argent et **0 jour de chantier** » … « il coûte **41 jours** » … « **Le rapport est de 1 à 41** ». Un rapport dont le dénominateur est 0 n'existe pas, et aucun des deux termes ne vaut 1. Le gabarit injecte `lignes.2.retard_du_chantier_j::n0` = 0, et la phrase a été écrite pour une valeur de 1 qui n'est plus produite. | Écrire « 0 jour contre 41 » et retirer la notion de rapport ; ou corriger après B4/B5, qui changent les trois nombres. |
| **B10 · La criticité des contrôles pour le planning est déclarée en dur dans les données, publiée comme un fait, et fausse pour ce chantier** | bloquant | `data → qualite_hse.plan_de_controle.lignes[*].sur_le_chemin_critique` : quatre booléens **posés à la main**, sans fourchette, sans V3, sans balise. `qualite.py:315` les compte et publie : « **4 controles sur 6 sont sur le chemin critique** du cycle : leur duree est du delai, pas une formalite ». Or les contrôles visés portent sur les voiles, le ferraillage, le bétonnage et le parement, c'est-à-dire sur des tâches dont `planification.json` donne la marge totale : MEZZ **39,81 j**, VOIL **39,81 j**, NOYX **436,39 j**. Le chemin critique réel est CHLV → COUV → SECH → SECO → ESSA → RECE. **Leur durée n'est pas du délai sur ce chantier.** C'est la violation littérale de **D-040** (« un effet sur le planning se **mesure** en rejouant le réseau, il ne se **déduit** pas »), dans le module qui invoque D-040 trois paragraphes plus haut. | Supprimer le booléen des données et **mesurer** : rejouer le réseau en allongeant chaque contrôle de sa durée, comme `impact_sur_le_planning` le fait déjà. Si aucun n'est critique, le dire — c'est une information de pilotage, pas une faiblesse. |
| **B11 · Trois obligations réglementaires étrangères au cadre du cours sont énoncées comme des faits, en pleine phase § 5.0** | bloquant | § S4g : « Elles ne remplacent ni le **plan de prévention** du chantier, ni le **PPSPS**, ni les obligations réglementaires du marché ». Glossaire : « **PPSPS** : plan de sécurité propre à l'entreprise sur un chantier donné » ; « **Bordereau de suivi** : document qui accompagne un déchet dangereux de sa production à son traitement ». § S4e : « ils **imposent** un stockage séparé, un **bordereau de suivi** et une filière agréée ». PPSPS et plan de prévention sont des instruments du **Code du travail français** ; le bordereau de suivi des déchets l'est aussi. Le cadre du cours est marocain (CLAUDE.md § 1 : CPS, CCAG-Travaux). `registre-sources.csv` : **0 ligne C7**. Et le mémo du même module classe « obligations de tri » en **⏸** — le corps affirme ce que le mémo déclare suspendu. | Soit nommer le texte applicable **au Maroc** avec son niveau (V0 si fourni, sinon ⚠ à vérifier), soit écrire la **fonction** sans le nom de l'instrument (« un document de traçabilité qui suit le déchet de sa production à son traitement, dont le nom et le régime sont fixés par la réglementation applicable — ⏸ »). Le contrôle § 12.1 ne voit rien parce qu'il ne cherche que les balises V2 et les jeux de charges. |
| **B12 · La double lecture entreprise / maîtrise d'œuvre est cochée dans la fiche-module et absente du module** | bloquant | `cadrage/05-sommaire.md:857` (fiche C7 livrée) : « **Double lecture entreprise / MOE : ✓** ». `grep -c "double" content/08-c7-qualite-hse.md` → **0**. Il n'existe aucune section, aucun encart, aucun bloc qui oppose ce que fait l'entreprise et ce que vise la MOE. C3 le fait (`gros-oeuvre.json → points_d_arret.double_lecture`, deux paragraphes) ; C7 se contente d'une colonne « Qui » dans un tableau. CLAUDE.md § 6.2 O4 et § 12.3 l'exigent pour un module d'exécution, **avec preuve**. | Soit écrire la double lecture (ce que l'entreprise soumet au visa, ce que la MOE contrôle, critère d'acceptation, traitement d'une NC côté MOE — le module en a toute la matière), soit décocher la case et l'inscrire en dette dans `STATE.md`. |
| **B13 · O7 revendiqué ✓ : il n'existe aucun contre-calcul indépendant, et `qualite.py` n'est pas étalonné** | bloquant | Fiche C7 : « Options : … **O7 ✓ — RELEVE** par rapport a la fiche d'origine » et « Contre-calcul : l'effet planning est MESURE en rejouant le reseau ». Rejouer le réseau appelle `pln.voie_A_parcours` et `pln.planning_avec_fenetres` — **les mêmes fonctions** qui ont produit la référence : c'est la même voie, pas une seconde. **D-043** l'interdit explicitement (« quand les deux termes d'une comparaison viennent de la même source, le module écrit que ce n'est pas une vérification au sens du § 3.3 »). `calc/tests/test_qualite.py` ré-applique les formules de `qualite.py` (ex. ligne 49-52 : `abs(e["accidents…"] - tf * e["heures_ponderees…"]/1e6) < 0.02`) : c'est une vérification de transcription, pas de modèle. Et `ls calc/etalonnage/` ne contient **aucun** fichier pour `qualite.py` — § 3.3 : « sans étalonnage, ses résultats restent V3 et ne servent pas d'exemple de référence ». | Ajouter une vraie seconde voie : (a) le coût de NC recalculé en MAD/m² tout compris et comparé au cumul des postes ; (b) l'exposition recalculée depuis effectifs × durées étalées × heures de plage, indépendamment de `heures_de_main_oeuvre_par_tache` ; (c) l'effet planning recalculé à la main sur le chemin critique. Ou décocher O7 et le dire. Et créer `calc/etalonnage/qualite_cas_ferme.py` (un cas à solution fermée : N fenêtres de f jours, immobilisation i ⇒ retard analytique). |

### Majeurs

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **M1 · Aucun chiffre publié ne porte sa fourchette, alors que toutes les entrées en ont une (D-036)** | majeur | `data → qualite_hse` porte une fourchette sur **chacune** de ses 17 valeurs. Le module publie 1,74 accident, 13,5 %, 134 214 MAD, 15,0 %, 251,5 t, 75,7 %, 41 j, 86,8 j perdues — **aucun avec bornes**. Recalculé : accidents **0,71–3,38** ; part de nuit dans le risque **9,4–20,7 %** ; coût de NC **45 601–348 165 MAD** (×7,6) ; déchets **127,7–481,0 t** ; journées perdues **35,5–202,7**. D-036 : « Tout module qui publie une date ou une durée publie aussi les deux bornes », et son impact l'étend à D1 sur les coûts. | Publier les bornes à côté de chaque résultat, comme D2 le fait pour la date. Et dire que la part de nuit **dans le risque** est le nombre le plus fragile du module (×2,2 d'étendue) alors qu'il est répété cinq fois. |
| **M2 · Faux niveau de précision : des hypothèses V3 à ±2× publiées au centime** | majeur | Capture `…-figure2.png` : « 48720,99 », « 134213,56 », « 371,25 », « 64961,32 ». CLAUDE.md § 3.6 : résultats intermédiaires à **3 chiffres significatifs**. Le corps du texte formate en `::n0` ; la figure, elle, imprime la valeur brute de `qualite.json`. | Arrondir dans `figures()` ou dans le rendu de la cascade (3 chiffres significatifs, ou le millier de MAD). |
| **M3 · Le durcissement du contrôle est chiffré au taux horaire d'un compagnon alors que le contrôle est fait par la MOE** | majeur | `calc/qualite.py:102` : `taux = d["prix_unitaires_MAD"]["postes"]["main_oeuvre_h"]["valeur"]` = 45 MAD/h, dont la note dans `data/` dit : « **compagnon, charges comprises** ». Or `data → plan_de_controle` attribue le contrôle de parement à « **MOE** » et le durcissement porte sur des heures de contrôle, pas de production. `prix.json → bordereau.frais_de_duree.lignes.encadrement` vaut 180 000 MAD/mois : l'heure d'encadrement est d'un tout autre ordre. La 4ᵉ ligne est sous-estimée d'un facteur ≈ 3 à 5 — et le module **conclut sur cette ligne** : « en argent, le durcissement du contrôle ne pèse rien ». | Introduire un `controle_h` distinct dans `prix_unitaires_MAD` (V3, fourchette), le baliser, et refaire la ligne. La conclusion reste peut-être vraie en ordre de grandeur ; elle n'est pas démontrée aujourd'hui. |
| **M4 · L'assiette des heures exclut l'atelier et les études, et le module affirme l'exhaustivité** | majeur | `planification.json → heures_de_main_oeuvre_par_tache` : `CHET = 0`, `CHFA = 0`, `SECH = 0` — assumé dans `planification.py:effectifs_par_tache` (« etudes, fabrication en atelier et sechage n'occupent personne **sur le chantier** »). Mais C7 écrit, § S1 : « ce cours connaît maintenant ses heures **exactement, tâche par tâche** », et § S2 : « Le chantier represente 58 261 heures travaillees ». CHFA = 60 j de fabrication de **312 t** de charpente : des milliers d'heures de soudage, meulage, levage d'atelier, c'est-à-dire précisément les postes que B5 associe aux CND et à la fatigue. Elles sont absentes de l'assiette **et** du raisonnement de prévention du § S4g. | Dire la frontière en une phrase (« l'assiette couvre les heures **sur site** ; l'atelier et les études en sont exclus et relèvent de l'établissement du fabricant »), et ajouter la conséquence : un TF de chantier ne couvre pas l'atelier, et le chef de projet suivi doit le demander au fabricant. |
| **M5 · 46 % de l'assiette est un lot très probablement sous-traité, et le module ne dit jamais de qui est le TF** | majeur | `heures_de_main_oeuvre_par_tache.SECO = 27 000 h` sur 58 260,6, soit **46,3 %**, avec `effectif_par_tache.SECO = 45`. Un TF se calcule normalement sur le périmètre de l'entité qui le déclare ; mélanger les heures de ses sous-traitants change la nature de l'indicateur, et c'est l'un des pièges classiques du métier. Le module construit pourtant toute sa démonstration (« le second œuvre domine, et c'est normal », § S4g « le gros œuvre impressionne, le second œuvre expose ») sur cette ligne, sans jamais dire qui la porte. | Ajouter une ligne : périmètre = toutes entreprises présentes sur le site ; dire que le TF de l'entreprise générale seule serait calculé sur une autre assiette, et que comparer deux TF sans comparer leurs périmètres est la même faute que comparer sans dénominateur. |
| **M6 · Deux coefficients de nuit contradictoires cohabitent dans la même base de données** | majeur | `data → ferroviaire.plage_travaux.abattement_de_cadence_nuit_pct = 30` (soit ×1,43) et `data → qualite_hse.exposition.surexposition_du_travail_de_nuit = 1,8`, avec des notes **identiques mot pour mot** sur la cause. Aucun des deux ne renvoie à l'autre. R1 (source de vérité unique) et R6 (aucune simplification silencieuse). | Voir B2. A minima : croiser les deux notes, expliquer ce que chacune couvre, et ne pas les justifier par la même phrase. |
| **M7 · Les trois quarts des valeurs V3 publiées par C7 ne sont dans aucun registre — et le contrôle ne peut pas le voir** | majeur | `grep -c C7 data/registre-hypotheses.csv` → **6** (H177–H182). Valeurs V3 publiées et **absentes** du registre : `surface_m2` 48 m², `delai_de_decision_j` 4 j, `duree_de_reprise_j` 3 j, `durcissement_du_controle_pct` 25 %, `heures_de_controle_par_levee` 1,5 h, `levees_restantes` 22, `kg_m2` du béton 38 / du bois 6,0 / des dangereux 0,4, les **cinq** `valorisation_pct` (80/95/60/40/0), et le « 1 800 h par compagnon » de l'exercice 1 — soit **≈ 16 valeurs**. Toutes ont pourtant une fourchette dans `data/`. Le contrôle § 12.1.h affiche « 187 lue(s) sur 187 » parce qu'il compte les **balises ⟦ ⟧**, et que ces valeurs sont injectées par `{{ }}` : elles sont structurellement invisibles au contrôle. | Baliser (ou faire générer une ligne de registre pour) toute valeur V3 injectée par variable, pas seulement celles écrites à la main. Et corriger le contrôle, qui annonce une exhaustivité qu'il ne vérifie pas. |
| **M8 · Cinq nombres techniques tapés à la main dans l'exercice 1, dont une hypothèse non déclarée** | majeur | `content:272-277` : « **1 800 h** par compagnon et par an », « **21 600** », « **108 000** », « **93** », « **46** ». Arithmétique vérifiée et **juste** (92,6 et 46,3). Mais § 4.3 : « Aucun nombre technique n'est tapé à la main dans un module ». Et 1 800 h/an est une hypothèse V3 sans balise, sans fourchette, sans registre — qui contredit de surcroît le calendrier du cours (`planning.calendrier` : 5 j/semaine × 8 h ⇒ ≈ 1 940 h ouvrées par an avant intempéries). | Mettre 1 800 h (ou la valeur recalée sur le calendrier du cours) dans `data/`, la baliser, et faire calculer les quatre autres par `calc/`. |
| **M9 · Trois tests épinglent des conclusions au lieu de vérifier des règles — le défaut que D-041 et D-043 ont déjà corrigé deux fois** | majeur | `calc/tests/test_qualite.py` : « la part visible sur un devis est **MINORITAIRE** » (`part_visible_pct < 50`), « canari : ne chiffrer que la reprise **sous-estimerait d'un facteur notable** » (`total/visible > 2`), « sous consignation, le retard est **AMPLIFIE** » (`> immobilisation × 1,5`). Ces trois assertions gèlent les thèses du module : corriger B3 (part visible → 98 %) ou B4 (retard → autre chose) fait **échouer les tests**, qui protègent donc l'erreur au lieu de la détecter. D-043 : « un test épinglait la conclusion … c'est-à-dire exactement le défaut que C3 avait dû corriger ». | Remplacer par des tests de **règle** : « les frais de durée ne sont imputés que si le retard mesuré est non nul » ; « le retard est celui que donne le réseau rejoué, quel qu'il soit » ; « la part visible est celle que donne la somme des lignes légitimes ». |
| **M10 · Le rendu supprime les virgules de ponctuation des textes calculés** | majeur | `calc/qualite.py:68, 145` : `.replace(",", " ")` — destiné aux séparateurs de milliers de `f"{x:,.0f}"`, il frappe aussi la ponctuation. Rendu vérifié : « 58 261 heures travaillees **dont** 4 651 », « C'est le premier resultat de ce module **et** il ne se voit », « 114 054 MAD **  soit** 85 % ». Trois phrases cassées, visibles à l'écran. | Formater avec une espace insécable fine dès l'origine (`f"{x:,.0f}".replace(",", " ")`) ou passer par le formateur du gabarit (`::n0`). |
| **M11 · De larges blocs de texte s'affichent sans accents dans un cours en français** | majeur | Toutes les chaînes produites par `calc/qualite.py` sont écrites sans accents et rendues telles quelles : `lecture`, `_pourquoi_pas_l_effectif`, `_ce_que_le_nombre_d_accidents_n_est_pas`, `_ce_que_la_criticite_n_est_pas`, `_le_seuil_est_arbitraire`, `la_regle`, `controles_qui_ne_protegent_pas_leur_ouvrage`, `_le_cout_du_point_d_arret`, `_ce_que_les_ex_aequo_disent`, `pourquoi_lire_aussi_la_gravite_seule`, `_consequence_de_pilotage`, `lecture` des déchets, et les 6 lignes du plan de contrôle et les 8 parades lues dans `data/` (partiellement accentuées : « protections périphériques **posees** »). Environ un tiers du texte affiché. CLAUDE.md § 1 : « langue : français ». | Accentuer les chaînes de `calc/` et de `data/`, et ajouter un contrôle de build qui refuse un mot français courant non accentué dans une chaîne publiée. |
| **M12 · Séparateurs décimaux mélangés sur la même page, parfois dans la même phrase** | majeur | Rendu : « elle pese **13.5** % du risque » (chaîne calculée) puis, deux lignes plus bas, « Part de la nuit dans le risque **13,5** % » (variable `::n1`). Également « 8.0 % » / « 8,0 % », « 1.9 t » / « 1,9 t », « 0.76 % », « 41.0 j » / « 41,0 j », « 8.2 h », « 436.4 j ». | Même correction que M10 : formater côté gabarit, pas en f-string. |
| **M13 · Les balises V3 avalent l'unité de la valeur qu'elles portent** | majeur | Tableau de la NC, rendu : « 48 m² à 420 MAD/m², **à 420 ^V3** » — la balise ⟦V3\|…\|420\|MAD/m²\|…⟧ affiche la valeur sans son unité, et juste après une note qui la répète déjà. Tableau des déchets : « Acier et metaux **4,5 ^V3** » dans une colonne « kg/m² » tandis que les quatre autres lignes affichent un nombre nu — **deux lignes sur cinq** sont balisées, les trois autres (38,0 · 6,0 · 0,4) ne le sont pas, ni aucun des cinq taux de valorisation. | Faire afficher l'unité par la balise, et baliser les cinq lignes ou aucune. Lié à M7. |
| **M14 · C7 condamne le critère chiffré recopié que B3e publie** | majeur | C7, exercice 3 ligne 2 et check-list point 3 : un critère d'enrobage « doit **renvoyer** [au plan visé] au lieu de le recopier », et le recopier est présenté comme un défaut en soi (« Il est peut-être juste sur ce chantier-ci ; il sera faux sur le suivant »). `calc/sorties/ferraillage.json → controles.liste[0]` (module B3e) : « Enrobage … **reference: "la cote du plan (3 cm ici)"** », et de même « Recouvrements … (1.00 m ici) », « Espacement des cadres … 10 cm … 20 cm ». B3e **nomme la source et marque ⏸**, ce qui est la bonne pratique ; C7 énonce une règle plus raide que la sienne, sans la nuancer, et condamne donc un module livré. | Préciser la règle : un critère peut porter la valeur **à condition** de nommer le document dont elle vient et de marquer ce qui est normatif ⏸ ; ce qui est interdit, c'est la valeur **orpheline** dans un plan générique. Citer B3e comme l'exemple de la bonne forme. |
| **M15 · Trois plans de contrôle du même chantier, qui s'attribuent les mêmes contrôles à des acteurs différents** | majeur | C3 (`gros-oeuvre.json → points_d_arret`, 5 étapes) : « Autorisation de bétonnage — visé par **maîtrise d'œuvre** — critère : bon de livraison conforme, température du béton ». C7 (`plan_de_controle`) : « Affaissement au cône — qui : **entreprise** » et « Réception des aciers — entreprise, visa MOE ». C3 publie en outre « Implantation et altimétrie du coffrage », « Fermeture du coffrage de voile » et « Décoffrage » comme points d'arrêt — **absents** du plan C7, qui prétend être « le plan de contrôle du cas phare ». B3e publie une troisième liste (6 contrôles d'armatures) qui n'apparaît dans aucune des deux. Rien ne dit comment les trois s'articulent. | Soit C7 consolide les trois et renvoie explicitement (« les six contrôles d'armatures de B3e sont le détail de la ligne 2 ; les cinq points d'arrêt de C3 sont le détail des lignes 2 et 5 »), soit chaque module nomme son périmètre. Un chantier n'a qu'un plan de contrôle. |
| **M16 · « la fenêtre suivante, un mois plus tard » explique 20 jours, pas 41** | majeur | Encart § S4b : « elle attend la **fenêtre suivante**, un mois plus tard ». Or le calcul rate **deux** fenêtres : 48,64 → 17 fenêtres (fin 460,64) ; 55,64 → **19** fenêtres (fin 501,64) ; 2 × 20 j + 1 j = 41 j. `periode_entre_fenetres_jours = 20`. L'explication donnée au lecteur est fausse d'un facteur 2 — et c'est elle qui est censée justifier que « ce n'est pas une erreur de calcul ». D-048 reprend la même formulation. | Écrire le mécanisme exact (« 7 jours de contenu de travail en plus, à 3 jours par fenêtre, c'est deux fenêtres de plus ; à 20 jours d'écart, 40 jours ») — après avoir corrigé B4, qui change l'entrée. |
| **M17 · « Défaut d'enrobage sur une pièce de charpente » : un désordre qui n'existe pas** | majeur | `content:285` (exercice 2). L'enrobage est la distance béton–armature ; une pièce de charpente métallique n'en a pas. Pour un profilé, on parle de défaut de **revêtement**, de **galvanisation**, de **soudure** (B5 : CND, EN ISO 5817 ⚠), ou d'**épaisseur de protection au feu**. L'erreur est d'autant plus visible que le module traite par ailleurs correctement le vocabulaire du contrôle. | Remplacer par « un défaut de soudure détecté au ressuage sur une pièce à lever sous consignation » — plus juste, et cohérent avec B5 et le délai du résultat (§ S3b). |
| **M18 · Le choix des trois tâches comparées n'est pas celui que la docstring annonce, et il n'est pas reproductible** | majeur | `calc/qualite.py:168-189`. La docstring affirme : « on prend celle qui n'a **AUCUNE** marge, celle qui en a **le moins parmi les autres**, et celle qui en a le plus ». Le code fait `candidates.sort(key=marge_totale)` puis prend `[0], [1], [-1]`. Or `planification.json` donne **six** tâches à marge ≈ 0 (CHLV, COUV, SECH, SECO, ESSA, RECE) : `candidates[1]` n'a pas « le moins parmi les autres », il a **zéro aussi**. Le tri de Python étant stable, l'ordre entre ces six dépend de l'**ordre d'insertion du dictionnaire** `NOMS` — une variable de code, pas une donnée. Le module publie pourtant « les trois tâches ne sont pas choisies à la main ». | Trier avec une clé de départage explicite et déclarée (par exemple marge, puis heures de main-d'œuvre décroissantes), ou choisir la tâche sous consignation **explicitement** puisque c'est elle qui porte la démonstration. Et corriger la docstring. |
| **M19 · Une marge de « -0,0 j » est publiée dans un tableau destiné au lecteur** | majeur | Rendu § S4b : « CHLV · … **0,0 j** » / « COUV · … **0,0 j** » depuis `marge_totale_j: -0.0`. Le `-0.0` provient de `round(mt, 2)` sur un flottant négatif infinitésimal. Dans la chaîne `lecture`, il s'affiche en toutes lettres : « marge **-0.0** j ». Une marge négative affichée dans un cours de planning suggère un planning infaisable. | `round(mt, 2) + 0.0` ou `max(0.0, …)` avec la convention déclarée. |
| **M20 · `STATE.md` classe C7 à la fois comme dernier livrable et comme « actif, non écrit »** | majeur | `STATE.md:9` : « **Dernier livrable** : `C7` ». `STATE.md:38` : « ▶ **actifs, non écrits** : … C3, C4, C6, **C7**, … ». Le cycle § 13.1 étape 6 impose la mise à jour de `STATE.md` avant le commit. Le contrôle § 12.1 ne vérifie que la longueur (149/150 lignes). | Retirer C7 de la liste des non-écrits. Et vérifier au passage C3, qui est livré et figure dans la même liste. |
| **M21 · O4 coché sans séquence, sans matériel, sans cadence et sans effectif** | majeur | Fiche C7 : « **O4 ✓** ». CLAUDE.md § 6.2 O4 : « séquence, matériel, cadences, effectifs, contrôles, sécurité — **avec la double lecture** ». Le module livre les contrôles et la sécurité ; il ne livre ni séquence, ni matériel, ni cadence, ni effectif — et pas la double lecture (B12). | Décocher O4, ou le restreindre explicitement (« O4 partiel : contrôles et sécurité ; séquence et moyens vivent en C1–C3 ») et l'inscrire tel quel dans la fiche. |
| **M22 · Les captures ont été produites mais, visiblement, pas regardées** | majeur | § 12.1.b : captures « non vides … **et examinées visuellement** ». Les trois captures existent et sont vertes au test de variance de pixels. B7 (barres dans le désordre, tâche manquante) et B8 (mot coupé) se voient en **deux secondes** à l'écran, et aucun des deux n'est dans la dette. C'est la deuxième fois dans ce dépôt (cf. QA antérieurs) que les défauts de figure échappent à une chaîne de contrôle verte. | Faire figurer, dans le bilan de fin de module, la phrase « j'ai ouvert les N captures » avec ce qui a été vu sur chacune — et ajouter un test d'ordre et un test de troncature de libellé. |

### Mineurs

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **m1 · Le quiz 6 utilise une criticité de 36 qui n'existe pas dans l'échelle du module** | mineur | « La criticité d'un risque passe de **36** à 24 ». Le tableau du module ne produit que 24, 16 et 12. 36 est atteignable (3×3×4) mais sort de nulle part. | Prendre deux valeurs du tableau (24 → 16). |
| **m2 · Les ex æquo à 16 sont départagés par l'ordre de la liste, et l'ordre obtenu est le moins défendable** | mineur | `qualite.py:254` trie par `(-criticite, -g)`. « Chute de charge en levage » (f2 g4 d2) passe devant « Effondrement d'étaiement » (f1 g4 **d4**) : même gravité, mais l'étaiement est le seul risque **non détectable** du tableau. | Ajouter `-d` comme troisième clé, ou dire que les ex æquo ne sont pas ordonnés. |
| **m3 · Figure 2 : la quatrième barre a une hauteur nulle et son étiquette flotte dans le vide** | mineur | Capture `…-figure2.png` : « 371,25 » s'affiche en haut de la figure sans barre sous lui. La légende l'assume (« à peine visible ») — mais un libellé sans trait est un défaut de lecture, pas un effet pédagogique. | Hauteur minimale d'une barre de cascade (1 px) ou annotation explicite « < 0,3 % ». |
| **m4 · Le passage de « 1,8 fois plus » à « 13,5 % » n'est pas montré, et 8,0 × 1,8 ≠ 13,5** | mineur | Le lecteur qui vérifie trouve 14,4 %. Le vrai rapport est 13,51/7,98 = **1,69**, parce que le dénominateur a grossi lui aussi. Le test interne l'encode (« à la pondération près ») ; le module, non. | Montrer la ligne de calcul, ou cesser de pondérer (B1). |
| **m5 · « Sur le chemin critique » dans la donnée, « du cycle » dans le texte** | mineur | Clé `sur_le_chemin_critique` (sans qualificatif) ; texte publié « sur le chemin critique **du cycle** ». Deux notions différentes, un seul booléen. | Renommer la clé `sur_le_chemin_critique_du_cycle`, après avoir traité B10. |
| **m6 · La « sixième colonne » du mémo n'existe pas dans la donnée** | mineur | Mémo : « Et : ce contrôle est-il un point d'arrêt, avec sa durée au planning ? », présentée comme la colonne qu'on oublie. `plan_de_controle.lignes` n'a pas de champ `point_d_arret` ni `duree_j` : elle n'est renseignée pour aucune des six lignes. | Ajouter les deux champs, ou retirer la promesse. |
| **m7 · Heures de nuit = 100 % des tâches sous consignation, sans que ce soit dit** | mineur | `qualite.py:40` compte l'intégralité de CHLV et PSOU en nuit. C'est **étayé** (`ferroviaire.plage_travaux` : « de la dernière circulation à la première du matin », 6 h, et `heures_sur_site_par_jour` = 6 pour ces deux tâches) — mais le module ne fait jamais le lien, et le lecteur voit apparaître une « nuit » que la donnée appelle « consignation ». | Une phrase : « les deux tâches sous consignation se font intégralement de nuit, parce que la fenêtre d'interception est nocturne (B7c) ». |
| **m8 · Le mémo publie une formule de TF sur des « heures » alors que le calcul utilise des heures pondérées** | mineur | Mémo : $TF = \text{accidents} \times 10^6 / \text{heures}$. Calcul : `tf * h_pond`. Deux définitions du même symbole dans le même module. Corollaire de B1. | Disparaît avec la correction de B1. |
| **m9 · Syntaxe JavaScript dans un gabarit de contenu** | mineur | `content:184` : `{{qualite.criticite.ex_aequo_en_tete.length}}`. Elle rend « 5 » par chance ; `qualite.json` publie par ailleurs le même nombre en toutes lettres dans `_ce_que_les_ex_aequo_disent`. | Publier `nb_ex_aequo_en_tete` dans `calc/` et l'injecter. |
| **m10 · L'exposition de nuit compte 6 h de présence dont 3,15 h ne sont pas du travail, sans le dire** | mineur | `ferroviaire.plage_travaux` : prise de possession 0,5 + consignation 0,75 + amenée 0,4 + repli 0,5 + déconsignation 0,5 + marge 0,5 = **3,15 h** sur 6. Compter la présence est **le bon choix** pour l'exposition (c'est même un argument fort du module) — mais il est tu, et il fait diverger la notion d'« heure » de C7 de celle de D1. | Le dire, et en faire un point : le temps d'exposition d'une nuit d'interception est le double du temps productif. |

---

## 3. Grille d'auto-évaluation § 7.2

| Critère | Note /3 | Justification |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | Remarquable. Chaque notion est amenée par son mécanisme (pourquoi des heures et pas un effectif, pourquoi le délai du résultat change la nature d'un contrôle, pourquoi un produit de rangs ne se soustrait pas). C'est le meilleur module du dépôt sur ce critère. |
| Les hypothèses sont explicites | **1** | TF, TG et k sont correctement balisés V3 avec fourchette et note — c'est fait, et bien fait. Mais l'assiette des heures (atelier exclu, sous-traitance incluse, nuit = consignation), la légitimité des frais de durée, le taux de l'heure de contrôle et la criticité déclarée des contrôles sont tous des choix tus. ≈ 16 valeurs V3 publiées sans registre. |
| Les formules sont justifiées | **1** | TF et TG sont justes et justifiés. `h_pond = h_jour + k·h_nuit` n'est jamais justifié, et son usage avec TF est un double compte (B1) ; l'ajout de 7 jours à une durée en plages est une erreur d'unité (B4) ; la règle « hiérarchiser sur la marge » est réfutée par le tableau qui l'illustre (B5). |
| L'exemple est vérifié | **0** | Aucune seconde voie (D-043), aucun étalonnage de `qualite.py`, et les tests ré-appliquent les formules testées — dont trois épinglent la conclusion. O7 est coché. Le seul contrôle externe réel serait l'ordre de grandeur, et il n'est pas fait. |
| Le piège est identifié | **3** | Le § S5 est excellent (onze pièges, chacun avec son symptôme et son coût), les exercices sont bien construits, le quiz est expliqué. Réserve : deux des pièges reposent sur des nombres faux (15 %, 41 j). |
| Le lien avec l'exécution est fait | **1** | Le plan de contrôle et le § S4g sont ancrés dans le geste. Mais pas de double lecture entreprise/MOE (B12), pas de séquence ni de moyens alors que O4 est coché (M21), et le plan contredit ceux de C3 et B3e (M15). |
| Le lien avec le coût et le délai est fait | **1** | L'intention est juste et c'est l'apport central du module. L'exécution ne l'est pas : 85 % du coût publié est illégitime sur l'ouvrage choisi (B3), et le délai vedette vient d'une addition d'unités différentes (B4). |

**Total : 10/21.** Le minimum de 2 partout exigé par le § 7.2 **n'est pas atteint** sur cinq critères
sur sept. Le module ne peut pas être livré en l'état.

---

## 4. Verdict

**13 bloquants, 22 majeurs, 10 mineurs — 45 défauts. Module à reprendre, livraison refusée.**

Les tests sont 16/16 verts et n'en voient aucun. Ce n'est pas un accident : la chaîne de contrôle de
ce dépôt vérifie la **transcription** (le code fait ce que le code dit) et pas le **modèle**. Trois
mécanismes expliquent l'angle mort, et ils sont réutilisables :

1. **`verif_unites.py` valide l'étiquette, pas la grandeur.** Il attache `u.hour` à
   `heures_ponderees_par_le_risque` et conclut que tout est homogène. Un pint ne peut pas savoir
   qu'une somme pondérée n'est pas une durée.
2. **`test_qualite.py` ré-applique les formules de `qualite.py`.** Chacun de ses 56 contrôles est
   vrai par construction ; les quatre « canaris » testent des propriétés que le code garantit déjà.
   Et trois tests **épinglent les conclusions** du module, c'est-à-dire protègent les erreurs B3 et
   B4 contre leur propre correction. C'est le défaut que D-041 et D-043 ont déjà corrigé deux fois
   dans ce dépôt ; il est revenu.
3. **Les captures sont produites et pas regardées.** B7 et B8 se voient à l'œil nu en deux secondes.

Les quatre défauts à traiter en premier, parce que tout le reste en dépend :

- **B3** — le cas d'étude impute 113 682 MAD d'immobilisation à un ouvrage que le module montre
  lui-même, deux sections plus loin, avoir **436 jours de marge**. Recalculé proprement, la NC coûte
  **20 531 MAD dont 98 % visibles sur un devis**, et la thèse publiée (« 15 % visibles ») s'inverse.
  C'est D-040 reproduit à l'identique, dans le module qui cite D-040.
- **B1 et B2** — deux double comptes successifs sur le travail de nuit : un taux mesuré sur des
  heures réelles appliqué à des heures pondérées, et un abattement de cadence déjà contenu dans les
  heures puis recompté par un coefficient. Le module en porte la preuve interne : son propre encart
  écrit « 1,6 accident » là où son tableau publie 1,74.
- **B4 et B5** — le « ×6 sous consignation » naît de l'addition de 7 jours ouvrés à une durée que D2
  déclare être en **plages de consignation**, et la règle qu'il est censé démontrer est réfutée par
  la ligne voisine du même tableau (deux marges nulles, deux retards dans un rapport de 6).

Ce qu'il faut dire en faveur du module, parce qu'une passe hostile qui ne le dit pas est malhonnête :
la **thèse** est juste et neuve (l'exposition se compte en heures ; le coût d'une NC n'est pas celui
de sa reprise ; la criticité classe et ne mesure pas), le § S5 et les exercices sont les meilleurs du
dépôt, aucun conseil dangereux n'a été trouvé, et le refus obstiné de citer un seuil ou une distance
tient le § 5.0 proprement sur le fond. Ce sont les **nombres** qui ne tiennent pas — et dans un
module dont toute l'ambition est de rendre la sécurité *pilotable*, c'est-à-dire chiffrable, c'est
précisément ce qui ne peut pas être approximatif.

**Passe à relancer après correction, jusqu'à zéro bloquant.** Un canari explicite est recommandé
pour la prochaine passe (§ 12.2) : les cinq dernières passes du dépôt ont toutes trouvé ≥ 6
bloquants qu'aucun test n'avait vus.

---

## 5. Suite donnée (27/10/2026)

**13 bloquants : tous corrigés.** **22 majeurs : 18 corrigés, 4 versés en dette.** **10 mineurs :
6 corrigés, 4 versés en dette.** Le module a été repris sur ses trois quarts ; ce qui suit ne liste
que ce qui a changé de fond, le détail est dans git.

### Ce que les bloquants ont emporté

| # | Correction |
|---|---|
| B1 | La pondération de nuit **répartit** le risque, elle ne l'ajoute plus : les poids sont normalisés pour que leur somme redonne les heures réelles. Le total d'accidents ne dépend plus du coefficient — un invariant d'étalonnage le vérifie à cinq coefficients, de 1,0 à 5,0. |
| B2 | Les deux coefficients de nuit (surexposition 1,8 et abattement de cadence 30 %) portent désormais des notes qui se croisent et disent ce que chacun mesure. **Non dérivés l'un de l'autre : versé en dette.** |
| B3 | Les frais de durée ne sont plus imputés à un ouvrage à marge : ils suivent le **retard mesuré**, qui est nul là où il est nul (D-040). Le module publie trois régimes au lieu d'un coût unique, et le résultat est plus instructif que le nombre qu'il remplace. |
| B4 | L'immobilisation est un **retard de début**, pas un allongement de durée : l'ajouter à une durée exprimée en plages était une erreur d'unité. |
| B5 | La marge seule ne hiérarchise pas — la consignation amplifie — et le module le démontre au lieu de l'affirmer. |
| B6 à B13 | Assiette des heures déclarée ; criticité départagée par une règle publiée ; `-0,0 j` supprimé ; figures arrondies ; libellés entiers ; toutes les tâches de la figure 1 ; textes recalculés depuis `calc/`. |

### Ce que les majeurs ont changé, et qui vaut plus que la correction

- **M1 (bornes)** → **D-049**. Tout est publié avec ses deux bornes. Et en les publiant, on
  découvre que le nombre qui résiste au balayage n'est aucun montant : c'est l'**écart entre les
  régimes**. Le module enseigne désormais le rapport, pas la somme.
- **M16 (« un mois plus tard » explique 20 jours, pas 41)** → **D-050**. En allant mesurer au lieu
  d'expliquer, on trouve mieux qu'une correction : le retard sous consignation est **quantifié**.
  Six rejeux du réseau ne rendent que deux retards distincts, et le coût marginal d'un jour perdu
  est nul presque partout et brutal une fois par palier. Trois règles de pilotage en sortent, dont
  aucune n'était dans le module. Le reproche de la passe était juste ; le chiffre qu'elle citait
  (41 j) venait du réseau d'avant la correction de B7c, qui en donne 20.
- **M3 (l'heure de contrôle au taux du compagnon)** → **D-051**. Erreur de taux d'un facteur trois
  dans la ligne même sur laquelle le module concluait. La conclusion survit, ce qui est exactement
  ce qui rend l'erreur dangereuse.
- **M15 (trois plans de contrôle) et M14 (C7 condamnait B3e)** → **D-052**. Les trois mailles sont
  emboîtées et se renvoient l'une à l'autre ; chaque ligne porte l'exécutant **et** le visa ; et la
  règle sur les critères chiffrés est précisée — un critère peut porter une valeur s'il nomme son
  document, et B3e est cité comme la bonne forme.
- **M4 et M5 (l'assiette)** → **D-053**. Les deux frontières sont publiées, avec les trois
  questions à poser devant tout taux.
- **M7, M8, M13** : les seize valeurs V3 injectées par variable sont balisées, les cinq ratios de
  déchets aussi (tous ou aucun), et les cinq nombres de l'exercice 1 sont calculés — l'hypothèse
  des 1 800 h/an est dans `data/` avec sa fourchette, et le module montre que le **rapport** des
  deux taux ne dépend pas d'elle.
- **M9** : les tests de conclusion étaient déjà remplacés par des tests de règle ; quinze tests de
  règle ont été ajoutés (bornes ordonnées, paliers multiples du pas, taux de contrôle strictement
  supérieur au taux de production, exécutant et visa distingués).
- **M10, M11, M12** : un formateur français unique (`_f`) remplace le `.replace(",", " ")` qui
  mangeait la ponctuation ; toutes les chaînes publiées par `calc/` et par `data/` sont accentuées ;
  un comparateur insensible aux accents évite qu'accentuer une chaîne casse un test d'orthographe.
- **M17** : « défaut d'enrobage sur une pièce de charpente » → défaut de **soudure détecté au
  ressuage**, avec la note de vocabulaire qui explique pourquoi l'enrobage n'existe pas sur un
  profilé.
- **M18, M19, M2, M20, M21, M22** : départage déclaré et publié ; `-0,0` supprimé ; figures à trois
  chiffres significatifs ; `STATE.md` corrigé ; **O4 déclaré partiel** dans la fiche, avec la raison ;
  les quatre captures ouvertes et regardées (deux corrections : libellé du flux dangereux trop long
  pour l'axe, légende qui annonçait une barre « invisible » alors qu'elle est tracée).

### Versé en dette (`STATE.md`, ligne 24)

Les deux coefficients de nuit restent distincts sans être dérivés l'un de l'autre (B2/M6) ; quatre
mineurs de forme (m3 hauteur minimale de barre, m5 nom de clé, m7 et m10 désormais traités dans le
texte mais pas dans les noms de clés).

### Ce que cette passe apprend sur le contrôle

C'est la neuvième passe du dépôt et la neuvième fois qu'aucun défaut n'est trouvé par la chaîne
automatique, verte à chaque fois. Ce qui a trouvé les treize bloquants : **recalculer trois valeurs
à partir de `data/` seulement**, **rapprocher deux nombres publiés par le même module à deux
sections d'écart**, et **ouvrir les captures**. Les trois sont des gestes humains, et deux d'entre
eux sont maintenant outillés — mais seulement là où on savait déjà quoi chercher.
