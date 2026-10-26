# QA — C3 · Gros œuvre : le cycle, le parc de coffrage, le bétonnage par temps chaud

**Passe adversariale n° 1** (§ 12.2, Annexe 4) · relecteur indépendant, n'a pas écrit le module
· dépôt figé sur `90013a4` · 26/10/2026
Livrable relu : `content/05-c3-gros-oeuvre.md`, `modules/05-c3-gros-oeuvre.html`,
`calc/gros_oeuvre.py`, `calc/sorties/gros-oeuvre.json`, `calc/tests/test_gros_oeuvre.py`,
`data/projet-gare.json → gros_oeuvre, cycle_zone`, les 4 captures.
Fichiers de D4 non touchés (`calc/suivi.py`, `calc/etat.py`, `content/04-d4-suivi-controle.md`,
`QA/D4-passe1.md`).

**État des contrôles au moment de la passe** : `npm run check` → **VERT, 16 contrôles passés** ;
`calc/tests/test_gros_oeuvre.py` → tous verts. Aucun des six bloquants ci-dessous n'est vu par un
contrôle. C'est la quatrième fois (E1, TV, D2, D1).

---

## 0. Contre-expertise à l'aveugle

Recalculée depuis `data/projet-gare.json` et les sorties des modules amont **seulement**, par
`/tmp/claude-0/-home-user-mine/70713aa8-3622-5c6d-a7c2-bce4a8b25d73/scratchpad/blind.py`, **avant**
toute lecture de `calc/gros_oeuvre.py`.

Réseau du cycle reconstruit à la main depuis `cycle_zone` et les durées de la TV
(COF 1,77 → FEP à 50 % → FED à 40 % → PTA 0,25 → BET 0,41 → CUR 2,00 → DEC 0,50) :
**8,053 j**, identique au cycle publié par la TV.

### 0.1 Immobilisation du coffrage et part de cure

| | Mon calcul | Publié | Écart |
|---|---:|---:|---:|
| Immobilisation (début COF → fin DEC) | 8,053 j | 8,05 | 0 % |
| dont cure | 2,00 j | 2,00 | 0 % |
| Part de cure | 24,84 % | 24,8 % | 0 % |
| Zones simultanément coffrées `I/T` | 8,053 / 3,4 = **2,37** → 3 | 3 | 0 % |

**RAS sur l'arithmétique.** Mais l'immobilisation vaut **exactement** le cycle, et c'est structurel
(COF ouvre le cycle, DEC le ferme) — voir **M11**.

### 0.2 Ce qu'un parc de 1 300 m² porte, et la cadence qu'il permet

Une zone demande **424,3 m² de tables** (`tranche-plancher.quantites.coffrage_m2`), pas ses 360 m²
de plancher. `floor(1300 / 424,3) = 3` zones → cadence du parc `8,053/3 = 2,68 j` < cadence des
équipes 3,4 j : **le parc déclaré ne borne pas**. Publié : identique. **Écart 0 %.**
(Le défaut n° 17 de `STATE.md`, le parc divisé par la mauvaise surface, est bien corrigé.)

### 0.3 Coût total de six tailles de parc, et l'optimum

Loyer 48 MAD/m²/mois, montage 55 MAD/m², conversion 21,66 j ouvrés / mois calendaire (D1).

| Parc | Mon loyer + montage | Publié | Écart | **Mon total** | **Publié** | Écart |
|---:|---:|---:|---:|---:|---:|---:|
| 430 | 85 040 | 85 020 | 0,0 % | *voir ci-dessous* | 239 631 | **−64 %** |
| 850 | 115 011 | 115 057 | 0,0 % | 115 011 | 115 057 | 0,0 % |
| 1 300 | 163 668 | 163 265 | 0,2 % | 163 668 | 163 265 | 0,2 % |
| 1 700 | 214 028 | 213 500 | 0,2 % | 214 028 | 213 500 | 0,2 % |
| 2 150 | 270 682 | 270 015 | 0,2 % | 270 682 | 270 015 | 0,2 % |
| 2 550 | 321 041 | 320 250 | 0,2 % | 321 041 | 320 250 | 0,2 % |

Le loyer et le montage se recalculent à 0,2 % près. **Toute la divergence est sur une seule
ligne et un seul poste : les frais de durée de la ligne 430 m².**

Deux lectures possibles de la marge, et elles ne donnent pas le même optimum :

| Règle de déclenchement des frais de durée | Ligne 430 m² | **Optimum** |
|---|---:|---|
| dépassement de la **marge libre** (22,34 j) — *ce que fait C3* | 239 631 MAD | 850 m² à 115 057 |
| dépassement de la **marge totale** (39,81 j) — *ce que dit le réseau de D2* | **85 020 MAD** | **430 m² à 85 020** |

La rallonge de la ligne 430 vaut 32,55 j ; la marge **totale** de MEZZ vaut 39,81 j. Le plancher ne
porte pas la date — `planification.json → durees.MEZZ.critique = false`, et C3 le publie lui-même
sous `parc.le_plancher_porte_t_il_la_date = false`. **Le chantier ne finit pas plus tard, donc les
frais de durée ne bougent pas, donc l'optimum bascule sur le plus petit parc.** → **B1**.

Taux de frais de durée : C3 = `328 000 / 21,66` = **15 143 MAD/j ouvré** ; D1 publie
`cout_MAD_par_jour_ouvre` = **16 268,18**. **Écart 7,4 %** → **B5**.

### 0.4 Débit minimal de bétonnage à 35 °C

Épaisseur déduite `90 / 360 = 0,250 m`. Zone 15 × 24 m. Bande de 4,0 m.

| Orientation de la bande | Volume | Débit min à 35 °C | Toupies au minimum |
|---|---:|---:|---:|
| **traversant les 15 m** *(choix de C3)* | 15,0 m³ | **11,5 m³/h** | 2 |
| traversant les 24 m | 24,0 m³ | 18,5 m³/h | 3 |

Publié : 15,0 m³ et 11,5 m³/h. **Écart 0 %** sur le chemin retenu — mais le chemin lui-même est un
choix en dur jamais déclaré (**M4**), et les **6 bandes × 15,0 = 90 m³ ne reconstituent pas les
98,4 m³ de la zone** (**B4**).

### 0.5 Nombre de toupies et durée de coulage

Toupie 8 m³ / 75 min = 6,40 m³/h. Zone 98,4 m³. Pompe 45 m³/h. Cible 4 h.

| | Mon calcul | Publié | Écart |
|---|---:|---:|---:|
| Toupies au minimum | 2 | 2 | 0 % |
| Toupies retenues (1ʳᵉ option ≤ 4 h) | 4 | 4 | 0 % |
| Durée du coulage | 3,84 h | 3,84 | 0 % |
| La pompe borne à partir de | 7,03 toupies | « 8 » | — |
| **Bétonnage du cycle TV lu par ce module** | **0,41 j = 3,28 h** | 3,84 h retenue | **+17,1 %** |

Le module décide 3,84 h et **dessine 3,28 h** sur sa figure 1. → **B3**.
Fin de coulage : 05:30 + 3,84 h = **09:20** ; publié « 9h00 environ ». → **M6**.

### 0.6 Deux valeurs recalculées en prime

| | Mon calcul | Publié | Écart |
|---|---:|---:|---:|
| Part du point d'arrêt **dans le cycle** (0,25 / 8,05) | **3,11 %** | 2,4 % | **+29 %** |
| Marges du réseau du cycle (CPM rejoué) | toutes nulles | « les sept tâches sont critiques » | RAS, **vrai** |

Le dénominateur publié est `Σ durées = 10,45 j`, la somme de barres qui se recouvrent — une
grandeur qui n'existe nulle part ailleurs et qui n'est pas le cycle. → **B2**.

---

## 1. Les dix points du § 12.2

| # | Point | Constat |
|---|---|---|
| 1 | Unités et homogénéité | **DÉFAUT** : m³/bande contre m³/zone (B4) ; m³/h contre la durée de bétonnage du cycle (B3) ; % du cycle contre % de la somme des durées (B2). Jours ouvrés / calendaires : **RAS**, la conversion 21,66 est la bonne et elle est appliquée au loyer comme aux frais. m² plancher / m² coffrage : **RAS**, corrigé et testé (test l. 47-53). |
| 2 | Référentiels mélangés | **RAS prouvé** : aucun référentiel n'est cité ; `grep -o '⟦V[0-9]' content/05-c3-gros-oeuvre.md` → **11 balises, toutes V3**, zéro V2. |
| 3 | Valeur normative sans V0/V1, durée présentée comme critère | **RAS prouvé sur le fond.** S4c ligne 1 dit explicitement « le critère est une **résistance**, jamais une durée. La durée de 2 jour(s) de ce module est une hypothèse de planification » ; l'exercice 4 corrigé n° 5, le quiz n° 6 et la check-list n° 8 le répètent. La cure est portée au Gantt comme durée imposée, pas comme critère. **Réserve** : le débit minimal de 11,5 m³/h est présenté comme « une contrainte physique » alors qu'il est intégralement porté par une V3 (M5). |
| 4 | Ordres de grandeur | Rotation 75 min, pompe pratique 45 m³/h contre 90 catalogue, toupie 8 m³ : **reconnaissables**. Loyer 48 MAD/m²/mois (≈ 4,4 €) et montage 55 MAD/m² (≈ 5 €) : **bas** pour des tables avec étaiement (m7). Cure 2 j pour une dalle de 25 cm sur tables : **optimiste** (m6). Maniabilité 1,3 h à 35 °C : plausible avec retardateur, haut de gamme sans. |
| 5 | Cohérence data / figures / calc / amont | **DÉFAUT** : frais de durée re-dérivés au lieu d'être lus chez D1 (B5) ; durée de coulage incohérente avec le cycle TV (B3) ; marge libre employée là où la date du chantier dépend de la marge totale (B1). Cycle et cadence : **RAS**, lus dans `planning_plancher` et testés. |
| 6 | Grille § 7.2 | voir § 4 : **1 critère sous le minimum de 2**. |
| 7 | Sécurité (§ 3.4) | S4c **existe et est réelle** (4 opérations, dispositions, lien explicite avec le reste du module). **Omission** : le module recommande un démarrage à 05:30 mi-juillet et propose « couler la nuit » sans un mot sur l'éclairage et l'accès de nuit ; la pompe, centrale au module, est absente de S4c (M9). |
| 8 | Vérité du rendu | **DÉFAUT** : figure 2 « les barres dessinent un U » sur un diagramme à barres horizontales (M2) ; figure 4 « de six à huit on ne gagne plus rien » alors que la figure montre 2,56 → 2,19 (M3). Figure 1 : libellé tronqué (m3). Pas de chevauchement de textes, captures non vides, aucune erreur console. |
| 9 | Simplifications non signalées (R6) | **DÉFAUT** : orientation de bande (M4) ; béton des poutres hors des bandes (B4) ; choix marge libre / marge totale (B1) ; parc traité en location alors que D1 le price à la rotation — ici **RAS**, `data → gros_oeuvre.coffrage._role` le dit (« les deux ne s'additionnent pas »), mais le **module** ne le dit pas au lecteur ; marge « gratuite jusqu'à épuisement » : **RAS**, déclarée dans l'encart `ce_que_le_calcul_ne_price_pas`, et appliquée de la même façon sur les six lignes. |
| 10 | Remplissage, télégraphie, généralités | **RAS prouvé.** S1 annonce ce qu'il ne refait pas ; aucune définition de banche, d'étai ou de vibration ; les six contrôles et les cinq points d'arrêt portent chacun un symptôme ou un critère ; les corrigés sont rédigés. Le niveau [M] est respecté. |
| 11 | *(point de mon cru)* arithmétique juste, modèle faux | **Trois nouvelles instances** : B1 (la bonne marge n'est pas celle-là), B2 (le bon dénominateur n'est pas celui-là), B4 (le bon volume n'est pas celui-là). Les trois arithmétiques sont exactes. |

---

## 2. Défauts

### Bloquants

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **B1 · Les frais de durée sont déclenchés sur la marge LIBRE, alors que la date du chantier dépend de la marge TOTALE. L'optimum du parc en est l'artefact direct, et le module publie lui-même la clé qui le dément.** `optimum_du_parc` reçoit `pl["durees"]["MEZZ"]["marge_libre_j"]` (22,34 j) et facture `frais × (rallonge − marge)`. La rallonge de la ligne 430 m² vaut 32,55 j, **inférieure à la marge totale de 39,81 j** : la fin du chantier ne bouge pas, donc aucun frais de durée du chantier ne court. Le texte affirme pourtant trois fois le contraire (« les frais de durée du chantier entier se réveillent », « la date du chantier bougerait », `parc.lecture` : « chaque jour de dépassement repousse la fin du chantier »). | **bloquant** | `calc/gros_oeuvre.py` l. 405-413 : `marge = …marge_totale_j` est lu **puis seulement rangé** (l. 414) ; c'est `marge_libre_j` qui est passé à la fonction. Même fichier l. 106-107 : `if (critique or depassement > 0)` — `critique` est **mort**, la branche `depassement > 0` facture quoi qu'il arrive. Or `planification.json → durees.MEZZ.critique = false` et `gros-oeuvre.json → parc.le_plancher_porte_t_il_la_date = false` : le module écrit que le plancher ne porte pas la date, puis lui impute 154 611 MAD de frais de durée. Recalcul § 0.3 : ligne 430 m² **239 631 → 85 020 MAD (−64,5 %)**, et l'optimum passe de **850 m² à 430 m² (115 057 → 85 020, −26 %)**. | Déclencher les frais de durée sur le **dépassement de la marge totale**, et supprimer `critique or` qui ne sert à rien. Si l'on préfère garder la prudence de la marge libre, alors le dire : la marge libre borne le **décalage des successeurs**, pas la date de fin, et le surcoût entre 22,34 et 39,81 j n'est pas un frais de durée mais un déplacement de tâches à chiffrer autrement. Dans les deux cas republier le tableau S4a, la figure 2, les trois lectures, l'exercice 3, S5, la fiche mémo — et retirer le test l. 80-83 (voir M1). Ajouter le test qui manque : `depassement == max(0, rallonge − marge_totale)`, avec un canari qui bascule l'optimum. |
| **B2 · « 2,4 % du cycle » n'est pas un pourcentage du cycle.** `part_du_cycle_pct` divise la durée du point d'arrêt par **la somme des durées des sept tâches (10,45 j)**, c'est-à-dire la somme de barres qui se recouvrent — une grandeur qui n'apparaît nulle part ailleurs dans le cours. Le cycle vaut 8,05 j. | **bloquant** | `calc/gros_oeuvre.py` l. 294-296 : `par_id["PTA"].duree / sum(t.duree for t in reseau …)`. Vérification : `1,77+2,52+3,00+0,25+0,41+2,00+0,50 = 10,45` ; `0,25/10,45 = 2,39 %` ; **`0,25/8,05 = 3,11 %`**, soit **+29 %**. Publié deux fois, § S4c et puce 2 de la figure 1 : « 0,25 jour, soit 2,4 % **du cycle** ». Et `part_de_cure_pct`, deux fonctions plus haut, utilise **bien** le cycle (24,8 %) : les deux pourcentages de la même figure n'ont pas le même dénominateur. | Diviser par `immobilisation["duree_j"]` comme la cure, republier 3,1 %, et ajouter au test l. 140-142 une vérification du dénominateur (aujourd'hui il ne fait qu'imprimer la valeur). |
| **B3 · La durée de coulage retenue contredit le bétonnage du cycle que le module lit et dessine.** S1 pose la discipline : « Ce module ne le recalcule pas — il le **lit** ; trois modules qui recalculent la même grandeur finissent par en publier trois valeurs. » Le module lit un cycle dont la tâche BET dure 0,41 j, **soit 3,28 h** (la TV l'a bâtie sur 30 m³/h), puis décide 4 toupies à 25,6 m³/h, **soit 3,84 h**. Les deux nombres sont dans le même livrable, à deux sections d'écart. | **bloquant** | `tranche-plancher.json → durees.betonnage_j = 0,41` et `durees.betonnage_h = 3,28`. `gros-oeuvre.json → betonnage.duree_du_coulage_h = 3,84` et `figures.cycle[4].duree = 0,41`. Écart **+17,1 %**. Capture `05-c3-gros-oeuvre.html-figure1.png` : la barre « Bétonnage et surfaçage » est étiquetée **0,41 j** sur la figure même dont la légende dit « le cycle d'une zone ». Tenir 30 m³/h demanderait **5** toupies (32,0 m³/h), pas 4. Aucun test ne confronte les deux. | Trancher et propager : soit la TV adopte le débit tenu de C3 (le cycle passe à 8,12 j, la cadence et D2 suivent), soit C3 retient 5 toupies. Dans les deux cas, ajouter `assert abs(betonnage.duree_du_coulage_h − tv.durees.betonnage_h) < tolérance` — c'est exactement le test qui manquait à D2 (M11 de sa passe). |
| **B4 · Les bandes ne reconstituent pas la zone : 90 m³ contre 98,4 m³. Le béton des poutres, là où une reprise froide est le plus grave, est hors du débit minimal.** `vol_bande = largeur × traverse × **épaisseur de dalle**` : 6 bandes × 15,0 = **90 m³**, c'est-à-dire la dalle seule. La durée de coulage, elle, est calculée sur **98,4 m³**, poutres comprises. Une bande de 4 m traverse pourtant les deux poutres de la zone (35 × 75 cm, retombée de 0,50 m) : `2 × 4,0 × 0,35 × 0,50 = 1,4 m³` par bande. | **bloquant** | `calc/gros_oeuvre.py` l. 176-178 : `ep_dalle = q["beton_dalle_m3"] / q["surface_m2"]` = 0,250, et `vol_bande = larg × traverse × ep_dalle`. `tranche-plancher.json → quantites` : `beton_dalle_m3 = 90,0`, `beton_poutres_m3 = 8,4`, `beton_m3 = 98,4` ; `gros-oeuvre.json → betonnage.volume_de_la_zone_m3 = 98,4`, `nb_de_bandes = 6`, `volume_d_une_bande_m3 = 15,0`. **8,5 % du béton de la zone n'est dans aucune bande.** Volume réel d'une bande **16,4 m³** → débit minimal à 35 °C **12,6 m³/h** au lieu de 11,5 (+9,6 %). Le test l. 103-105 rejoue la même formule et ne peut pas le voir. Le canari l. 114-117 ne teste que « la bande est plus petite que la moitié de la zone » : il passerait aussi avec les poutres oubliées. | Ajouter la part de poutre traversée au volume de bande, et poser le contrôle qui manque : `nb_de_bandes × volume_d_une_bande ≈ volume_de_la_zone` à quelques pour cent. C'est le contrôle d'homogénéité le plus simple du module et il n'existe pas. |
| **B5 · Le coût d'un jour de retard est re-dérivé au lieu d'être lu chez D1, et il en diffère de 7,4 %.** C3 recalcule `frais_par_mois / jours_ouvres_par_mois = 328 000 / 21,66 = 15 143 MAD/j`. D1 **publie** `cout_MAD_par_jour_ouvre = 16 268,18`. Le module qui ouvre sur « trois modules qui recalculent la même grandeur finissent par en publier trois valeurs » en publie une troisième. | **bloquant** | `calc/gros_oeuvre.py` l. 410-412 (`fd["cout_MAD_par_mois"]`, `fd["conversion"]["jours_ouvres_par_mois_calendaire"]`) et l. 106-107. `prix.json → bordereau.frais_de_duree` contient **les deux** : `cout_MAD_par_jour_ouvre = 16 268,18` (= 5 904 000 / 362,92) et `cout_MAD_par_mois = 328 000` sur 389,9 j ouvrés (= 15 143/j). C3 choisit silencieusement la seconde branche. Effet sur la ligne 430 m² : 154 611 contre **166 098** MAD, soit **+7,4 %**. C'est la récidive de **D1-M1** (« le même chantier converti en calendrier de deux façons »), déclarée corrigée. | Lire `cout_MAD_par_jour_ouvre` et rien d'autre. Et instruire l'incohérence interne de D1 (362,92 contre 389,9 j ouvrés pour la même période) avant qu'un troisième module n'en hérite. Test : `frais_de_duree_MAD == depassement_j × prix.cout_MAD_par_jour_ouvre`. |
| **B6 · S5, ligne 1 : l'erreur décrite ne produit pas la conséquence chiffrée.** « Parc dimensionné sur la surface d'une zone \| il manque des tables dès la troisième zone \| la cadence tombe à **8,1 j**, le plancher **double** ». Dimensionner sur la surface de **plancher** (l'erreur que l'exercice 1 et la figure 2 décrivent, et que la dette n° 17 dit corrigée) donne `3 × 360 = 1 080 m²` → `floor(1080/424,3) = 2` zones → cadence **4,03 j** et plancher 36,3 j, **+14 %, pas +102 %**. 8,05 j et le doublement sont la conséquence du parc de **430 m²**, une autre erreur. Et avec 1 zone de parc, il manque des tables dès la **deuxième** zone, pas la troisième. | **bloquant** | `content/05-c3-gros-oeuvre.md` § S5 ligne 1, qui lit `{{gros-oeuvre.parc.lignes.0.cadence_du_parc_j}}` — la ligne **430 m²**. `gros-oeuvre.json → parc.lignes[1]` (850 m², 2 zones) : `cadence_du_parc_j = 4,03`, `duree_du_plancher_j = 36,26`. La colonne « comment elle se voit » (3ᵉ zone) et la colonne « ce qu'elle coûte » (1 zone) décrivent deux parcs différents. | Chiffrer la ligne sur le parc que l'erreur produit réellement (1 080 m², 2 zones, 4,03 j, +4,4 j absorbés par la marge) — ce qui est d'ailleurs la bonne leçon : cette erreur-là ne se voit pas au planning, elle mange la marge. Et faire produire la ligne par `calc/` au lieu de pointer un index de tableau. |

### Majeurs

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **M1 · « L'optimum n'est ni le plus petit ni le plus grand » est un accident des six valeurs choisies, pas une propriété du modèle — et un TEST verrouille la conclusion au lieu de la vérifier.** Le modèle est : coût = loyer croissant + frais de durée nuls tant que la rallonge tient dans la marge. Son minimum est donc **toujours le plus petit parc dont la rallonge tient dans la marge** — ce que `calc/` écrit mot pour mot. Que ce parc ne soit pas le plus petit **testé** dépend entièrement de la marge retenue : avec la marge totale (B1), l'optimum **est** le plus petit. | majeur | `gros-oeuvre.json → parc.lecture` : « L'optimum est donc le **plus petit** parc dont l'allongement reste dans la marge » — contre S1 et S4a : « un optimum qui n'est ni le plus grand ni le plus petit ». `calc/tests/test_gros_oeuvre.py` l. 80-83 : `verifie("l'optimum n'est NI le plus petit NI le plus grand parc", …, "sinon le modele n'arbitre rien")`. Un test qui épingle le résultat narratif : si B1 est corrigé, ce test rougit et la tentation sera de déplacer les données. | Remplacer l'affirmation par ce que le modèle dit : « l'optimum est le plus petit parc dont l'allongement tient dans la marge », et montrer en une ligne ce qui le ferait bouger (une marge plus grande ⇒ le plus petit parc ; un plancher critique ⇒ le plus grand). Supprimer le test l. 80-83 et le remplacer par la vérification de la **règle** (`optimum == min des parcs à dépassement nul`, ou le minimum global si tous dépassent). |
| **M2 · Figure 2 : « Les barres dessinent un U ».** Un diagramme à barres horizontales ne dessine pas de U : il dessine six longueurs. L'allure en U est dans les **valeurs**, pas dans le dessin. | majeur | Capture `05-c3-gros-oeuvre.html-figure2.png` : barres horizontales 239,6 / 115,1 / 163,3 / 213,5 / 270 / 320,3, aucune forme de U visible. Famille des bloquants D2-B4 et D1-B7. | Soit une courbe (coût en fonction de la taille du parc, le U devient visible et c'est le vrai sujet), soit « le coût ne croît pas avec la taille du parc : il **passe par un minimum** ». |
| **M3 · Figure 4 : « passer de six à huit toupies ne gagne plus rien parce que la pompe borne à 45 m³/h » — la figure même montre le contraire.** De 6 à 8 toupies la durée passe de 2,56 à 2,19 h, **−14,5 %**. Et la pompe ne borne qu'à partir de **7,03** toupies : à 6 toupies on est à 38,4 m³/h, à 7 à 44,8. | majeur | `gros-oeuvre.json → betonnage.options_de_rotation` : 6 → 2,56 h `borne_par = la rotation des toupies` ; 7 → 2,20 h `la rotation des toupies` ; 8 → 2,19 h `la pompe`. Capture figure 4 : les deux barres sont visiblement différentes. | « Le gain s'écrase : de 2 à 4 toupies la durée est divisée par deux, de 6 à 8 elle ne gagne plus qu'un quart d'heure, et au-delà de 7 la pompe borne. » Faire produire la phrase par `calc/` depuis `borne_par`. |
| **M4 · L'orientation de la bande de coulage est un choix de modèle écrit en dur, jamais déclaré, et il change le résultat de 60 %.** `traverse = min(longueur_zone, largeur_zone)` : la bande traverse la zone dans sa **plus petite** dimension. L'autre orientation donne 24,0 m³ par bande, **18,5 m³/h** au lieu de 11,5, et **3 toupies au minimum** au lieu de 2. Rien dans `data/` ni dans le module ne dit que c'est un choix, ni pourquoi c'est celui-là. La largeur de bande, elle, est déclarée V3 avec sa fourchette et sa justification. | majeur | `calc/gros_oeuvre.py` l. 174-175 : `# une bande traverse la zone dans sa plus petite dimension` / `traverse = min(…)`. Recalcul § 0.4. Le contenu écrit « une bande de 4 m × 15 m » comme une donnée (§ S4b exercice 2, légende figure 3), sans jamais dire que 15 est un choix. Violation R6, et R9 : c'est le choix **favorable** qui est retenu sans l'instruire. | Déclarer l'orientation dans `data/` (`sens_de_coulage`), avec sa justification physique réelle (portée de flèche, position de la pompe, sens des poutres), et publier la variante : « dans l'autre sens il faudrait 18,5 m³/h et 3 toupies ». C'est un meilleur enseignement que le nombre seul. |
| **M5 · « C'est une contrainte physique » : 11,5 m³/h est intégralement porté par une V3, et il n'est pas stable sur sa propre fourchette.** Le temps de maniabilité à 35 °C est déclaré `1,3 h, fourchette 0,8 à 2,0`. Le débit minimal va donc de **7,5 à 18,8 m³/h** (facteur 2,5), et la conclusion « 2 toupies tiennent le minimum » ne tient que sur **69 %** de la fourchette déclarée (elle passe à 3 toupies dès `t < 1,17 h`). Le module n'en dit rien et qualifie le résultat de contrainte physique, en gras, deux fois. | majeur | `data → betonnage_temps_chaud.temps_de_maniabilite_h.a_35_degres.fourchette = [0.8, 2.0]`. `content` § S3b : « Le débit minimal ne dépend **ni de l'effectif ni de la cadence** : c'est une contrainte physique » ; docstring `debit_minimal()` l. 168-169 : idem. Dette n° 12 de `STATE.md` : le même reproche avait été traité pour la TV (« le contre-calcul ne passe que sur 27 % de la fourchette : publié comme tel »). | Publier la fourchette du débit minimal et le seuil où le nombre de toupies change, comme la TV l'a fait pour son contre-calcul. La forme est physique, la **valeur** est une hypothèse : le dire. |
| **M6 · La fenêtre de coulage fait l'inverse de la règle qu'elle publie, et son heure de fin est fausse de 20 minutes.** `regle` : « Ce qui décide de l'heure de démarrage, ce n'est pas l'horaire de l'équipe : c'est l'heure à laquelle on veut avoir **FINI**. » Le code pose `demarrage_conseille = "05:30"` en **constante littérale** et en **dérive** la fin. Et la formule de la fin perd les 30 minutes du départ : `05:30 + 3,84 h = 09:20`, publié « 9h00 environ ». | majeur | `calc/gros_oeuvre.py` l. 268-269 : `"demarrage_conseille": "05:30"` ; `f"{5 + int(duree + .5)}h{'30' if (duree % 1) < .5 else '00'} environ"` — la minute est choisie par la partie fractionnaire de la durée, pas par l'addition. Contrôle : avec `duree = 3,2` la formule rend « 8h30 » pour un vrai 08:42. | Déclarer l'heure de fin visée dans `data/` (`heure_de_fin_visee`, V3), en déduire le démarrage, et faire l'addition en minutes. Trois lignes, et la règle du module devient le calcul du module. |
| **M7 · Le tableau des toupies met en gras une ligne désignée par son index, pas par le calcul.** Le contenu lit `options_de_rotation.0/1/2/4/6` en dur et marque la ligne **2** « retenu ». `option_retenue` et `toupies_retenues` existent dans la sortie ; `grep -c option_retenue content/05-c3-gros-oeuvre.md` → **0**. La liste commence à `n_toupies`, qui dépend du débit minimal : si celui-ci montait (M4, M5, B4), l'index 2 désignerait 5 toupies et le tableau mettrait en gras une ligne qui n'est pas la retenue — sans qu'aucun contrôle ne sonne. | majeur | `calc/gros_oeuvre.py` l. 198 : `for n in range(n_toupies, n_toupies + 8)`. `content` § S4b, tableau des toupies. Règle de `STATE.md` : « tout verdict publié est une sortie de `calc/` ». | Faire émettre par `calc/` une liste de lignes déjà annotées (`retenue: true/false`, commentaire) et n'afficher que cela. |
| **M8 · Les deux clés qui démentent la conclusion sont calculées, publiées, et lues par personne.** `parc.marge_totale_du_plancher_j = 39,81` et `parc.le_plancher_porte_t_il_la_date = false` : **0 occurrence** dans le contenu. Ce sont précisément les deux grandeurs qui annulent les frais de durée de B1. | majeur | `grep -c "marge_totale_du_plancher_j\|le_plancher_porte_t_il_la_date" content/05-c3-gros-oeuvre.md` → 0 / 0. `calc/gros_oeuvre.py` l. 405-406 : `marge` et `critique` lus, `critique` neutralisé par `or depassement > 0` (B1), `marge` seulement rangé l. 414. Famille exacte de D1-B6 et D2-B1 (« un paramètre déclaré, publié, et que rien ne lit »), tous deux déclarés corrigés. | Les publier dans le module : la phrase « ce plancher ne porte pas la date du chantier, il a 39,8 j de marge totale » est le vrai enseignement de la section, et elle change la réponse. Ajouter le contrôle générique que D1-B6 réclamait déjà : toute clé publiée par `calc/` et lue par aucun module échoue le build ou se déclare `non_publiee`. |
| **M9 · S4c ne couvre pas le risque que la recommandation phare du module crée.** Le module conclut « démarrage **05:30** » et propose, si le débit ne tient pas, de « couler aux heures fraîches (**nuit** ou petit matin) ». Mi-juillet dans la région de Marrakech, le soleil se lève vers 06:20 : le coulage commence dans le noir. Éclairage de la zone, accès et circulation d'engins de nuit, surveillance du ferraillage avant coulage à la lampe : rien. La **pompe**, qui est le matériel central de la section, est absente des quatre opérations de S4c (fouettement de flexible, débouchage sous pression, flèche et lignes aériennes). | majeur | `content` § S4c, quatre lignes : décoffrage, étaiement de reprise, travail en hauteur, coulage par temps chaud — cette dernière ne parle que de contrainte thermique de l'équipe. `gros-oeuvre.json → betonnage.parade_si_le_debit_n_est_pas_tenable`. `fenetre_de_coulage.demarrage_conseille = "05:30"`. Le § 3.4 vise explicitement « toute opération à risque ». | Ajouter deux lignes à S4c : **coulage avant le jour** (éclairage, balisage, accès, consigne de ne pas commencer sans visa contradictoire fait de jour) et **pompage** (zone d'exclusion de la flèche, débouchage, flexible). Le module recommande l'horaire ; il doit en porter le risque. |
| **M10 · Le nombre de pompes est dimensionné sur le débit MINIMAL — la confusion que le module dénonce, dans son propre calcul.** `n_pompes = ceil(11,5 / 45) = 1`, alors que la pompe doit passer le débit **tenu** de 25,6 m³/h. Sans effet ici (1 dans les deux cas), faux dès qu'on monte dans les fourchettes. | majeur | `calc/gros_oeuvre.py` l. 192 : `n_pompes = math.ceil(ref / pompe)` où `ref` est le débit minimal. La figure 4 et l'exercice 4 consacrent pourtant une page à « les deux nombres ne répondent pas à la même question ». | `ceil(debit_tenu / pompe)`. Et publier le résultat : « une pompe suffit, et c'est elle qui plafonne à 7 toupies ». |
| **M11 · Le deuxième levier du module est une distinction sans différence numérique, et ce n'est pas dit.** S2 : « on ne divise pas la surface par le nombre d'équipes, on la divise par le nombre de zones simultanément coffrées, qui vaut l'**immobilisation** divisée par la cadence ». Or l'immobilisation vaut **exactement** le cycle (8,05 = 8,05), par construction : COF ouvre le cycle, DEC le ferme, rien ne précède ni ne suit. La formule « cycle / cadence », que le module présente implicitement comme naïve, donne le même nombre. | majeur | `calc/tests/test_gros_oeuvre.py` l. 36-37 : `verifie("l'immobilisation du coffrage couvre tout le cycle", abs(im["duree_j"] − r["cycle"]["duree_j"]) < 0.02)` — le test **prouve** l'égalité et le module ne la mentionne pas. Recalcul § 0.1. | Dire que les deux coïncident **ici**, et à quelle condition elles divergent (une tâche hors coffrage en tête ou en queue de cycle : traçage, réservations, finition). La leçon reste juste ; présentée comme une correction d'un calcul qu'elle ne corrige pas, elle s'use. |
| **M12 · Exercice 1 : « 3 × 424,3 = 1 300 m² ».** Le produit vaut **1 272,9**. 1 300 est le **stock déclaré au projet**, pas le résultat de la multiplication — et la TV publie d'ailleurs le bon nombre, `coffrage_mobilise_m2 = 1 273`. Le corrigé présente une égalité fausse de 2,1 % au lecteur. | majeur | `content` § S6 exercice 1 ; rendu HTML : « Parc minimum : 3 × 424,3 = 1 300 m², et c'est précisément le parc déclaré au projet ». `tranche-plancher.json → variantes.reference.coffrage_mobilise_m2 = 1273`, `stock_coffrage_declare_m2 = 1300`. | « 3 × 424,3 = 1 273 m² ; le projet a commandé 1 300 m², soit 27 m² de battement » — et injecter `coffrage_mobilise_m2` par variable au lieu de pointer la ligne du tableau. |
| **M13 · Exercice 3 : « il reste 17,9 jours de marge » ne dit pas de quelle marge il parle, et l'autre réponse est le double.** Après 4,4 j de rallonge il reste 17,9 j de marge **libre** et **35,4 j** de marge **totale**. Le corrigé bâtit tout son enseignement (« c'est payé en marge, et la marge sert à encaisser les aléas ») sur un nombre dont la définition décide de l'ampleur. | majeur | `gros-oeuvre.json → parc.lignes[1].marge_restante_j = 17,93`, `parc.marge_totale_du_plancher_j = 39,81`. Le mot « totale » n'apparaît pas une fois dans le contenu. | Nommer la marge partout où elle est publiée, et donner les deux dans la fiche mémo : marge libre (ce qui ne bouge personne) et marge totale (ce qui ne bouge pas la date). C'est la distinction qui fait B1. |
| **M14 · S5 : un loyer comparé à un total.** « Parc commandé large “pour être tranquille” \| … \| **320 250 MAD** au lieu de **115 057** » : le premier nombre est `lignes.5.loyer_et_montage_MAD`, le second `optimum.total_MAD`. Numériquement sans effet (la ligne 5 n'a pas de frais de durée), mais c'est la comparaison hors domaine qui a produit deux bloquants de D1. | majeur | `content` § S5 ligne 2, variables citées. | `lignes.5.total_MAD` des deux côtés. |

### Mineurs

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **m1 · Un identifiant de code en prose, quatre fois.** « bornée par l'**equipe ferrailleurs_dalle** » : sans accent, avec un souligné, dans le S1, le tableau S2, le quiz n° 3 et la fiche mémo. | mineur | Rendu HTML, 4 occurrences ; `gros-oeuvre.json → cycle.ressource_qui_borne = "equipe ferrailleurs_dalle"`. | Un libellé lisible dans `data/` à côté de l'identifiant (« l'équipe de ferraillage de dalle »). |
| **m2 · Deux arrondis de la même valeur publiée.** `rapport_35_sur_20 = 2,3` est calculé depuis les débits **arrondis** (11,5/5,0) et non depuis les temps (3,0/1,3 = 2,31) ; et `betonnage.lecture` écrit « il faut tenir **12** m³/h » là où tout le reste du module publie **11,5**. | mineur | `calc/gros_oeuvre.py` l. 238-240 et l. 244 (`{ref:.0f}`). | Arrondir une fois, à l'affichage. |
| **m3 · Figure 1 : libellé tronqué, et criticité affirmée plutôt que dérivée.** « Point d'arrêt : visa du ferraillage avant co… ». Et `figures.cycle[].critique` est posé par **énumération d'identifiants** (l. 367) alors que `cc["detail"]["critiques"]` est disponible deux lignes plus haut. *Vérifié : la légende « les sept tâches sont toutes critiques » est **exacte** — j'ai rejoué le CPM, toutes les marges sont nulles.* Le défaut est que rien ne la garantit. | mineur | `calc/gros_oeuvre.py` l. 365-368 ; CPM rejoué : `marges = {COF:0, FEP:0, FED:0, PTA:0, BET:0, CUR:0, DEC:0}`. Capture figure 1. | Lire `critiques` du CPM, et élargir la gouttière gauche du Gantt au plus long libellé (déjà demandé en D2-M14). |
| **m4 · « 8,05 / 3,4 = 2,37 » tapé à la main** (§ 4.3 : aucun nombre technique écrit à la main). Juste avec la cadence arrondie, **2,35** avec la cadence calculée de la TV. | mineur | `content` § S6 exercice 1. | Variable. |
| **m5 · Le `floor` dont le module fait un point ne mord sur aucune ligne du tableau.** Les six parcs comparés (430, 850, 1 300, 1 700, 2 150, 2 550) sont tous juste **au-dessus** de n × 424,3 (de +1 à +14 m²). La démonstration « un parc de 2,6 zones n'en porte que deux » n'a donc aucune illustration dans le tableau qui la suit. | mineur | `data → gros_oeuvre.coffrage.parcs_a_comparer_m2` ; `floor(parc/424,3)` = 1,2,3,4,5,6 exactement. | Remplacer une des valeurs par un parc intermédiaire (1 100 m², qui porte 2 zones et non 2,59) : la leçon se voit, au lieu d'être affirmée. |
| **m6 · Cure de 2,0 j avant décoffrage d'une dalle de 25 cm sur tables : optimiste**, même dans sa fourchette 1–4 j. Elle porte toute l'immobilisation, donc tout le dimensionnement du parc. *Vérifié : à 4 j (haut de fourchette) l'optimum ne bouge pas — 1 300 m² porte encore 3 zones à 3,35 j.* | mineur | `data → cycle_zone.cure_avant_decoffrage_j`. Recalcul de sensibilité. | Publier cette insensibilité : c'est rassurant et ça se dit en une ligne. |
| **m7 · Loyer et montage bas de gamme.** 48 MAD/m²/mois ≈ 4,4 €/m²/mois et 55 MAD/m² ≈ 5 €/m² pour des tables coffrantes **avec étaiement**. Dans la fourchette déclarée, mais le total du parc leur est strictement proportionnel. | mineur | `data → gros_oeuvre.coffrage`. | Les publier avec leurs bornes dans le tableau S4a, comme D-036 l'exige des dates et des coûts. |
| **m8 · Le loyer ne court que sur la durée du plancher** : ni délai de livraison, ni battement avant la première zone, ni repli après la dernière — alors que l'exercice 3 porte précisément sur un retard de livraison de deux semaines. | mineur | `calc/gros_oeuvre.py` l. 98-99 : `mois = duree / jours_ouvres_par_mois`. | Déclarer le battement (V3) ou dire que le loyer est une borne basse. |
| **m9 · « La durée de 2 jour(s) »** rendu tel quel dans S4c. | mineur | Rendu HTML § S4c. | Format entier, ou « deux jours ». |
| **m10 · Le cours porte désormais deux durées du plancher de mezzanine.** C3 lit la bonne clé (`planning_plancher.duree_totale_j = 31,85`, cadence 3,4), mais la TV publie aussi `variantes.reference.duree_plancher_j = 32,0` avec `cadence_j = 3,42`. Le module ne le dit pas ; le commentaire de `calc/` le dit, le lecteur ne le lit pas. | mineur | `tranche-plancher.json` : les deux valeurs coexistent. `calc/gros_oeuvre.py` l. 386-397 (commentaire et `regle["_arrondi"]`, jamais publié). | Publier `_arrondi` dans le module, ou aligner la TV sur une seule valeur. |
| **m11 · Exercice 4, correction n° 1 : « on finit vers 13 h » est calculé avec 4 toupies**, alors que le plan soumis au visa en annonce **2** — qui donneraient 7,69 h et une fin à **16 h 40**. La correction n° 3, trois lignes plus bas, le dit. | mineur | `content` § S6 exercice 4, corrections 1 et 3. | « Même correctement approvisionné (4 toupies, 3,8 h), un départ à 9 h finit à 12 h 50 ; avec les 2 toupies annoncées, à 16 h 40. » Les deux nombres servent la leçon. |
| **m12 · Le « canari » du parc n'injecte aucune erreur.** Le test l. 84-90 relit les lignes publiées et vérifie que la moins chère en loyer a un dépassement : il passe **quelle que soit** la règle de marge, donc il aurait passé avec B1 corrigé comme avec B1 présent. Ce n'est pas un canari au sens de `STATE.md` (« une erreur plantée dans une copie du livrable, qui doit rougir »). | mineur | `calc/tests/test_gros_oeuvre.py` l. 84-90. | Un vrai canari : rejouer `optimum_du_parc` avec `marge_j = 0` et vérifier que l'optimum bascule **et** que le test échoue. |
| **m13 · Les cinq confrontations qui manquent aux tests** : taux de frais de durée contre D1 (B5), durée de coulage contre la TV (B3), somme des bandes contre le volume de zone (B4), dénominateur de `part_du_cycle_pct` (B2), marge totale contre marge libre (B1). Les 34 contrôles verts ne touchent aucune de ces cinq jonctions. | mineur | `calc/tests/test_gros_oeuvre.py`, 153 lignes ; `npm run check` → 16/16 verts. | Les cinq assertions sont écrites dans les corrections ci-dessus. |

**Total : 6 bloquants · 14 majeurs · 13 mineurs.**

---

## 3. Réponses aux trois questions du point 11

1. **« La marge est gratuite jusqu'à épuisement » est-elle respectée sur toutes les lignes ?**
   **Oui** — `depassement = max(0, rallonge − marge)` et seul l'excédent est facturé, sur les six
   lignes, et l'encart `ce_que_le_calcul_ne_price_pas` déclare honnêtement la limite du principe.
   **Le défaut n'est pas la règle, c'est la marge qu'on lui donne** (B1) : une marge libre là où la
   question posée — « la fin du chantier bouge-t-elle ? » — appelle la marge totale.
2. **« Ni le plus petit ni le plus grand » : propriété ou accident ?**
   **Accident.** Le modèle a pour minimum le plus petit parc dont la rallonge tient dans la marge,
   et `calc/parc.lecture` l'écrit. Avec la marge totale, ce parc **est** le plus petit testé. Avec
   une marge nulle (plancher critique), ce serait le plus grand. Le module énonce comme une loi ce
   qui dépend de deux chiffres. → **M1**, et un test qui l'épingle.
3. **La durée de coulage est-elle cohérente avec le cycle de la TV ?**
   **Non.** La TV pose le bétonnage à 0,41 j = **3,28 h** (30 m³/h) ; C3 retient 4 toupies, **3,84 h**
   (25,6 m³/h). **+17,1 %**, et la figure 1 du module dessine la valeur de la TV pendant que la
   section S4b publie la sienne. → **B3**.

---

## 4. Grille d'auto-évaluation § 7.2

| Critère | Note | Justification |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | Les trois leviers sont introduits par leur mécanisme, pas par leur formule ; « ce qu'un petit parc achète, c'est de la marge » est une idée juste et neuve pour un [M]. |
| Les hypothèses sont explicites | **2** | S4b est complet et borné (11 V3 registrées). Mais l'orientation de la bande (M4), le béton des poutres (B4) et le choix marge libre / totale (B1) sont trois hypothèses structurantes non déclarées. |
| Les formules sont justifiées | **2** | `T ≥ I/⌊parc/S⌋` et `V̇ = ℓLe/t` sont posées et motivées. La seconde omet un terme (B4) et la première s'appuie sur une distinction sans différence (M11). |
| L'exemple est vérifié | **1** | **Sous le minimum.** Aucun contre-calcul par une voie indépendante (§ 3.3) : les tests rejouent les formules du module. Et trois résultats publiés sont faux (B1, B2, B4), tous les contrôles au vert. |
| Le piège est identifié | **3** | S5, les « erreurs courantes » des quatre figures et l'exercice 4 sont la meilleure partie du module ; la reconnaissance explicite de l'erreur des 138 m³/h est exemplaire au sens R8. |
| Lien avec l'exécution | **3** | Six contrôles coffrage fermé, cinq points d'arrêt avec critères, double lecture entreprise / MOE, fenêtre de coulage : c'est du métier. |
| Lien avec le coût et le délai | **2** | Présent partout, mais il repose sur B1 et B5 : le chiffre central du module (115 057 contre 163 265 MAD) tombe avec eux. |

**Minimum 2 partout : NON TENU** (critère 4 à 1/3).

---

## 5. Verdict

Un module juste de ton, juste de niveau et faux sur son chiffre central : l'optimum du parc est un
artefact de la marge libre employée à la place de la marge totale, et le module publie lui-même les
deux clés qui le démontrent sans jamais les lire — **6 bloquants, 14 majeurs, 13 mineurs, et 16
contrôles verts qui n'en ont vu aucun.**

---

## Suite donnée (26/10/2026, par l'auteur)

**Les 6 bloquants sont corrigés**, et chacun porte un contrôle qui sonne :

| # | Correction | Contrôle ajouté |
|---|---|---|
| B1 | La question « la fin du chantier bouge-t-elle ? » n'est plus **déduite** d'un type de marge : `impact_sur_le_chantier` **rejoue le réseau de D2** avec la nouvelle durée du plancher et lit la date de fin. Les frais de durée ne courent que sur le retard mesuré. Ligne 430 m² : 239 631 → **85 020 MAD** ; optimum 850 → **430 m²**. | Test : `frais_de_duree_MAD == retard_du_chantier_j × prix.cout_MAD_par_jour_ouvre`, et un canari qui rejoue le réseau sans la rallonge et vérifie qu'il raccourcit |
| B2 | `part_du_cycle_pct` divise par la **durée du cycle** (8,05 j), pas par la somme des durées de ses tâches (10,45 j). 2,4 → **3,1 %**. La clé `_denominateur` nomme le dénominateur dans la sortie. | Test du dénominateur, aligné sur celui de `part_de_cure_pct` |
| B3 | C3 ne choisit plus sa durée de coulage : il **lit** celle du cycle de la TV (3,28 h) et cherche l'attelage qui la tient — **5 toupies**, pas 4. `trois_contraintes` publie les trois exigences (anti-reprise 3, cible horaire 4, cycle TV 5) et dit laquelle commande et pourquoi. | Test : la durée retenue tient la durée de bétonnage de la TV ; aucun module ne publie deux durées pour le même coulage |
| B4 | Le volume d'une bande est le volume **de la zone** divisé par le nombre de bandes : les 8,4 m³ de poutres y sont. 15,0 → **24,6 m³** par bande, 6 → 4 bandes. | `controle_les_bandes_font_la_zone` publie somme, référence et écart ; test à écart nul |
| B5 | Les frais de durée sont **lus** chez D1 au jour ouvré (`cout_MAD_par_jour_ouvre`), plus re-dérivés depuis le mois. `_source_des_frais` nomme le fichier. | Test de provenance : la valeur utilisée est identique à celle que publie `prix.json` |
| B6 | La ligne 1 de S5 est chiffrée sur le parc que l'erreur **produit** (dimensionner sur la surface de plancher : 1,179 fois moins de tables), et non sur un index de tableau. | Les deux colonnes lisent le même parc |

**Majeurs et mineurs corrigés en plus** : M1 (la thèse du module est refaite — *un optimum de coût
n'est pas une décision* : `ce_que_le_cout_ne_decide_pas`, `plus_petit_parc_sans_rallonge` et
`ecart_entre_les_deux_choix_MAD` = 78 245 MAD, le prix de l'assurance ; le test qui épinglait la
conclusion narrative est remplacé par le test de la **règle**), M2, M3, M4 (`sens_d_avancement`
déclaré dans `data/` avec sa justification), M5, M6 (l'heure de démarrage se **déduit** de l'heure de
fin voulue, addition en minutes : **06 h 55** pour une fin à 10 h), M7, M8 (les deux clés qui
démentaient la conclusion sont publiées et lues), M9 (deux lignes de sécurité ajoutées à S4c :
démarrage avant le jour, manœuvre de la pompe et des toupies — six opérations au lieu de quatre),
M10, M11, M12 (`3 × 424,3 = 1 273 m²`, et 1 300 commandés : 27 m² de battement, les deux nombres
publiés par `calc/`), M13 (les marges sont nommées partout), M14, m1, m2, m3, m9, m11, m12, m13.

**Portés en dette déclarée** (`STATE.md`) : m5, m6, m7, m8, m10.

**Ce que cette passe a prouvé.** Les six bloquants sont tous de la même famille : **arithmétique
juste, modèle faux.** Aucun n'a été vu par les 34 contrôles verts. B1 a été trouvé en lisant deux
clés du même fichier de sortie qui se contredisaient (`le_plancher_porte_t_il_la_date = false` face à
154 611 MAD de frais de durée) — et c'est la troisième récidive de ce motif après D2-B1 et D1-B6. La
parade retenue cette fois n'est pas un test de plus : c'est de **mesurer au lieu de déduire**. Rejouer
le réseau rend la question du bon type de marge sans objet.

