# QA — D2 · Planification · passe adversariale n° 1

Relecteur hostile, indépendant de l'auteur. Annexe 4 du prompt maître.
Date : 20/10/2026 · Livrable relu : `content/02-d2-planification.md`,
`modules/02-d2-planification.html`, `calc/planification.py`,
`calc/sorties/planification.json`, `calc/tests/test_planification.py`,
`tests/captures/02-d2-planification.html-figure{1..6}.png`.

État des contrôles automatiques au moment de la relecture : **`npm run check` = VERT, 16 contrôles**.
Aucun des huit bloquants ci-dessous n'est vu par un contrôle.

---

## 0. Contre-expertise à l'aveugle

Les quatre recalculs ont été faits **avant** toute lecture du contenu, depuis `data/projet-gare.json`
seul, par un script jetable écrit pour l'occasion
(`/tmp/claude-0/-home-user-mine/70713aa8-3622-5c6d-a7c2-bce4a8b25d73/scratchpad/recalc.py`) :
tri topologique, parcours avant/arrière et point fixe des fenêtres **réécrits à la main**, sans
importer `calc/cpm.py` ni `calc/planification.py`.

**Réserve de méthode, qui est déjà un défaut (voir M1)** : le réseau — 27 tâches, 32 liens, 6
décalages négatifs — **n'est pas dans `data/`**. `data/planning` ne contient ni `taches` ni
`dependances` (Annexe 2 les prévoit). Il a donc fallu recopier `LIENS` depuis
`calc/planification.py`. Sur ce point, la contre-expertise n'a pas pu être aveugle : il n'existe
aucune source indépendante du code de production.

### 1 — Une quantité : la charpente et les quantités de gros œuvre

| Grandeur | Mon calcul, depuis la géométrie | Publié | Écart |
|---|---:|---:|---:|
| Emprise | 120 × 40 = 4 800 m² | 4 800 | 0 % |
| Décapage | 4 800 × 0,30 = 1 440 m³ | 1 440 | 0 % |
| Fouille niveau technique | 800 × (4,0 + 0,4) = 3 520 m³ | 3 520 | 0 % |
| Poteaux | 4 files × (16 + 1) = 68 | 68 | 0 % |
| **Charpente** | 4 800 × 65 / 1 000 = **312,0 t** | 312,0 | **0 %** |
| Façades | 2 × (120 + 40) × 9 = 2 880 m² | 2 880 | 0 % |

**RAS** sur les quantités. Chaîne géométrie → ratios V3 → quantité correcte et reproductible.

### 2 — Une durée par quantité ÷ cadence ÷ ateliers

$d_{\text{POTR}} = 68 / (3 \times 2) = 11,333$ j · publié **11,33 j** · écart 0 %.
$d_{\text{CHAP}} = 312 / (9 \times 1) \times (1 - 0{,}35) = 22,533$ j · publié **22,53 j** · écart 0 %.
$d_{\text{FOUI}} = 3\,520 / (450 \times 2) = 3,911$ j · publié **3,91 j** · écart 0 %.
Homogénéité : m³ / (m³·j⁻¹·atelier⁻¹ × atelier) = j. **RAS.**

### 3 — Durée du projet et chemin critique (CPM refait à la main)

| | Mon CPM | Publié | Écart |
|---|---:|---:|---:|
| Réseau nu | 273,867 j | 273,86 | 0,00 % |
| Avec étalement des consignations | **341,867 j** | **341,86** | 0,00 % |
| Chemin critique | CHET→CHFA→CHAP→CHLV→COUV→SECH→SECO→ESSA→RECE | identique | — |

L'**arithmétique est juste**. Le **modèle ne l'est pas** : mon point fixe reproduit exactement celui
de l'auteur, y compris son erreur. En reprenant le même modèle mais en faisant **démarrer la tâche
consignée sur sa fenêtre** — ce que le module calcule et publie lui-même dans
`consignations.CHLV.debut = 140` — j'obtiens :

> **359,33 j ouvrés** au lieu de 341,86 → **+ 17,47 j, soit + 5,1 %**, au-delà du seuil de 5 % du § 3.3.

Détail : CHLV `debut_j = 122,53` dans `durees`, `debut = 140` dans `consignations`, pour la **même
tâche, dans le même fichier**. Voir **B1**.

### 4 — Calendrier

Facteur intempéries 21,7 / (21,7 − 1,5) = 1,07426 · 341,867 × 1,07426 = 367,3 j ouvrés ·
origine 2026-11-02, semaine de 5 j → **2028-03-30**. **Identique au publié, écart 0 %.**
Mais avec la durée corrigée du point 3 : 359,33 × 1,07426 = 386,0 j → **2028-04-26**, soit
**27 jours calendaires** après la date que le module donne comme « durée à contracter ».

### Bilan de la contre-expertise

Trois recalculs sur quatre tombent à 0,00 %. Le quatrième montre que **le module calcule
correctement un planning dont le modèle perd 17,5 jours** — exactement la famille d'erreur des
quinze bloquants de la TV : une arithmétique juste sous un modèle faux.

---

## 1. Tableau des défauts

| # | Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|---|
| **B1** | **L'attente de la fenêtre de consignation n'entre pas dans le réseau.** `etalement_sous_fenetres` calcule `debut` (la fenêtre) et `attente_avant_premiere_fenetre_j`, mais `planning_avec_fenetres` ne réinjecte que `etalement_j` comme *durée* : la **date de début reste celle du réseau**. CHLV est critique, donc le projet perd 17,47 j et la date contractuelle 27 j calendaires. | **bloquant** | `calc/planification.py` l. 246-258 : `etale[i] = e["etalement_j"]`, `e["debut"]` jamais utilisé. `calc/sorties/planification.json` : `consignations.CHLV.debut = 140` / `fin = 220.13` contre `durees.CHLV.debut_j = 122.53` / `fin_j = 202.66`, et `attente_avant_premiere_fenetre_j = 17.47` publié sans effet. Recalcul § 0.3 : 359,33 j, fin 2028-04-26. | Contraindre la date au plus tôt dans le parcours avant : pour `i ∈ taches_soumises`, `ES_i = prochaine_fenetre(ES_i, premiere, periode)`. Republier durée, chemin, marges, calendrier, histogramme et courbe en S. Ajouter un test qui compare `durees[i].debut_j` à `consignations[i].debut` — c'est ce test qui manque. |
| **B2** | **La figure 5 ne dessine jamais la série lissée.** Le directive passe `"serie2":"planification.figures.effectifs_lisses"` ; `assets/svgkit.js` ne contient **aucune occurrence de `serie2`** et `histogramme(pts, o)` ne trace qu'une série. La légende affirme pourtant « Le contour foncé est l'effectif après lissage ». Toute la section S4d (59 → 45, −23,7 %) repose sur une figure qui ne la montre pas. | **bloquant** | `grep -n serie2 assets/svgkit.js` → 0 résultat. `assets/svgkit.js` l. 333-369 : une seule boucle `pts.forEach`. Capture `02-d2-planification.html-figure5.png` : une seule série bleue, aucun contour superposé. | Ajouter une seconde série (contour, pas de remplissage) à `histogramme`, ou retirer la promesse de la légende. Ajouter au build un contrôle : toute clé de directive inconnue du générateur **échoue** au lieu d'être ignorée en silence. |
| **B3** | **La figure 5 publie une moyenne qui contredit le texte.** Le générateur recalcule `moy = Σn / pts.length = 22,9` (moyenne sur **tous** les jours) ; le texte publie `moyenne_avant = 24,4` (moyenne sur les jours **travaillés**). Deux nombres différents pour la même grandeur, l'un dans la figure, l'autre trois lignes plus haut. Et c'est un nombre **calculé dans le dessin**, pas une sortie de `calc/` (§ 4.3). | **bloquant** | `assets/svgkit.js` l. 365 : `const moy = pts.reduce(...)/pts.length;`. Vérifié : 7 863/343 = 22,92 ; 7 863/322 = 24,42. Capture figure 5 : « moyenne 22,9 ». `content/…md` l. 199 : `moyenne_avant` → 24,4. | Passer la moyenne en paramètre depuis `calc/` (`ressources.moyenne_avant`) et supprimer le calcul local. Choisir une définition unique et l'écrire dans la légende (« moyenne sur les jours travaillés »). |
| **B4** | **La légende de la figure 6 décrit un palier qui n'est pas celui-là.** « Le palier au milieu de la courbe […] c'est l'attente des fenêtres de consignation, pendant laquelle le chantier avance peu. » Faux : pendant l'attente (j 122 → 203) la courbe monte **à plein régime** (CHLV compte 10 compagnons tous les jours, cf. B5). Le seul vrai palier est j 222 → 242 : c'est **SECH, le séchage**, dont l'effectif déclaré vaut 0. | **bloquant** | `calc/planification.py` l. 450-461 : `acc += eff[i]*(k-deb)`, accumulation linéaire sur `tot[i][1]-tot[i][0]`. `effectif_par_tache.SECH = 0`, `durees.SECH = [221.86 ; 241.86]`. Capture figure 6 : le plat est bien à 222-242, pas à 122-203. | Corriger la légende, **et** faire produire à la courbe les vrais paliers : accumuler le travail par fenêtre (5 marches de 3 j) au lieu d'une rampe continue. |
| **B5** | **L'assiette de la courbe en S et de l'histogramme est l'étalement, pas le travail.** `eff[i] × (fin − début)` compte 10 compagnons pendant les 80,13 j de CHLV, soit **801 j·h** là où le travail vaut **121 j·h**. Total : 7 847 j·h publiés contre 6 895 j·h réels, **+ 952 j·h soit + 13,8 %**. Le module écrit pourtant deux fois, en S4a et dans l'exercice 4, que « le coût suit la durée de travail, le délai suit l'étalement » : la courbe fait exactement l'inverse de ce qu'il énonce. | **bloquant** | `calc/planification.py` l. 450 (`total = Σ eff[i]*(tot[i][1]-tot[i][0])`) et l. 362-371 (`histogramme_effectifs`). Recalcul : Σ eff·étalement = 7 847 ; Σ eff·travail = 6 895. Docstring de `etalement_sous_fenetres` l. 220-222 qui dit le contraire. | Séparer les deux assiettes : présence (délai) et travail (coût, trésorerie). La courbe en S annoncée « en jours-hommes » et donnant « le pic de trésorerie » doit être bâtie sur le **travail**. |
| **B6** | **Contradiction de sécurité entre le texte et le réseau.** S4c : « le soutènement précède l'approfondissement, **jamais** l'inverse ». Le réseau pose `SOUT: [("FOUI", -4.0)]` : la fouille de 4,4 m est **terminée au jour 13,51** et le soutènement court **jusqu'au jour 27,51**, soit 14 jours de fouille ouverte non soutenue. Le planning publié fait précisément ce que la rubrique sécurité interdit. | **bloquant** | `calc/planification.py` l. 193 ; `durees.FOUI = [9.60 ; 13.51]`, `durees.SOUT = [9.51 ; 27.51]`. Capture figure 3 : la barre SOUT s'étend bien au-delà de FOUI. | Soit inverser le lien (FOUI succède à SOUT, avec recouvrement par passes), soit découper la fouille en passes alternées avec le soutènement. Dans tous les cas, mettre le texte et le réseau d'accord — c'est une règle de sécurité, pas une préférence de séquence (§ 3.4). |
| **B7** | **Deux décalages négatifs plus grands que la durée du prédécesseur** : un successeur démarre **avant** son prédécesseur. TERR dure 1,60 j et FOUI la suit avec −2,0 → FOUI démarre j **9,60**, TERR j **10,00**. FOUI dure 3,91 j et SOUT la suit avec −4,0 → SOUT démarre j **9,51**, FOUI j 9,60. Publié tel quel au Gantt. | **bloquant** | `LIENS` : `"FOUI": [("TERR", -2.0)]`, `"SOUT": [("FOUI", -4.0)]`. `durees` : TERR 10,00 ; FOUI 9,60 ; SOUT 9,51. Les durées étant **calculées**, le décalage en dur ne connaît pas la durée qu'il recouvre : un décapage plus rapide rendrait l'écart arbitrairement grand. | Exprimer les recouvrements en **pourcentage du prédécesseur** (comme `cycle_zone.recouvrement_*_pct`, déjà fait dans la TV), les déclarer dans `data/`, et ajouter un contrôle : `|décalage| ≤ durée du prédécesseur`. |
| **B8** | **Les ressources ne sont jamais vérifiées en conflit** — alors que la check-list S7 n° 5 et le quiz n° 3 l'exigent noir sur blanc. Le module ne produit qu'un histogramme de **compagnons**. L'unique grue à tour (`materiel.nb_grues = 1`) dessert simultanément **POTR, MEZZ et NOYX au jour 54**. Le module prêche le contrôle que la TV avait raté, et ne le fait pas davantage. | **bloquant** | `data/projet-gare.json` : `materiel.nb_grues = 1`, `cycle_zone.taches_servies_par_la_grue`. Dates : POTR [46,07 ; 57,40], MEZZ [53,40 ; 85,25], NOYX [46,07 ; 71,07]. `content/…md` l. 440 (check-list) et l. 469 (quiz). Aucune fonction de `calc/planification.py` ne touche à la grue. | Déclarer dans `data/` les tâches servies par la grue à l'échelle du chantier, produire un profil d'occupation **journalier** et publier le jour de conflit maximal. Sans quoi la check-list est une prescription que le module ne tient pas. |
| **M1** | **Le réseau et une constante de calendrier vivent en dur dans `calc/`.** 27 `NOMS`, 27 `LOT`, 32 liens et **6 décalages négatifs** (−5, −8, −2, −4, −3, −6) sont des littéraux de `calc/planification.py` ; `JOURS_OUVRES_PAR_MOIS = 21.7` aussi. `data/planning` n'a ni `taches` ni `dependances` (Annexe 2 les prévoit). Le texte affirme pourtant : « Ces […] hypothèses sont dans `data/`, pas dans le texte ». C'est le défaut que la TV avait corrigé sur `cycle_zone` — il revient à l'échelle du chantier. | majeur | `calc/planification.py` l. 170-206 et l. 398. `data/projet-gare.json` → `planning` : aucune clé `taches`/`dependances`. `content/…md` l. 279. | Descendre `NOMS`, `LOT`, `LIENS`, les décalages et `21,7` dans `data/planning`, et faire relire chacun par un test. |
| **M2** | **« Ces trente-six hypothèses » : il y en a 28.** Le contenu porte 28 balises `⟦V3`, le registre 28 lignes (H028 → H055). Le chiffre est tapé à la main et le build le contredit. | majeur | `grep -c "⟦V3" content/02-d2-planification.md` → **28**. `grep D2 data/registre-hypotheses.csv \| wc -l` → **28**. `content/…md` l. 279. | Injecter le compte par variable depuis le registre généré, ou le supprimer. |
| **M3** | **Des paramètres qui portent les résultats publiés échappent à toute déclaration.** `premiere_fenetre_jour = 40` (phase de **toutes** les fenêtres, donc de B1) : ni balise, ni fourchette, ni ligne de registre. Les 9 effectifs posés (`INST 6, SOUT 10, NOYX 12, MARQ 10, PSOU 8, QUAI 14, SECO 45, ESSA 8, RECE 4`) portent la pointe de 59 et toute la courbe en S : idem. Plus 5 forfaits (INST, TOPO, MARQ, QUAI, ESSA) et 3 cadences (voile, façade, dalle) utilisés mais non balisés. Le contrôle « 57 lues sur 57 » ne les voit pas : il ne retient que les objets ayant **à la fois** `valeur` et `fourchette`. | majeur | `build/check.mjs` l. 87-88 : `if ("valeur" in o && "fourchette" in o)`. `data/…json` : `"premiere_fenetre_jour": 40` est un nombre nu ; `effectif_par_tache` aussi. | Donner à ces valeurs la forme `{valeur, fourchette, note}`, les baliser, et faire échouer le contrôle sur tout nombre de `planning` qui n'a pas cette forme ou un `_nature: "decision"` explicite. |
| **M4** | **68 jours d'attente comptés dans la famille « calculée ».** `crit_par_famille` somme les durées **étalées** : les 80,13 j de CHLV entrent entiers dans « calculée », d'où 121,9 j. Le piège de l'exercice 3 en tire : « Elles ne pèsent que 121,9 jours du chemin critique » — comme si ces 121,9 j se réduisaient par les moyens. 68 d'entre eux sont de l'attente de consignation, que **rien** ne réduit. La leçon s'inverse. | majeur | `calc/planification.py` l. 541-543 : `sum(etalees[i] …)`, alors que `somme_des_durees_j` utilise `t[i]["duree_j"]` — deux assiettes différentes dans le même tableau. `content/…md` l. 389-391. | Ajouter une **quatrième famille « étalée »** (ou ventiler CHLV en 12,13 j calculés + 68 j d'attente) et refaire le piège de l'exercice 3 sur ce découpage. |
| **M5** | **Le levier (c) « protection de voie » n'est pas modélisé.** Le texte dit « supprimer la consignation par une protection de voie » ; le calcul met `part_levage_sous_consignation_pct = 0,001`, c'est-à-dire **le levier (b) poussé à l'extrême** (plus rien n'est levé au-dessus de la voie). Retirer la consignation se modélise en retirant CHLV de `taches_soumises`. La coïncidence numérique masque deux décisions d'ingénierie différentes. | majeur | `calc/planification.py` l. 626 : `variante(d, pl, dm, part_consignation_pct=0.001)`. `content/…md` l. 379-382. | Ajouter un paramètre `taches_soumises` aux variantes et modéliser (c) par son retrait. |
| **M6** | **Aucune sensibilité publiée, alors que le module publie une date contractuelle.** Les 28 fourchettes sont déclarées puis jamais exploitées : les variantes ne font varier que la fenêtre, la part sous consignation et deux effectifs d'ateliers. En prenant les cadences au **bas** de leur fourchette et les forfaits et délais imposés au **haut**, j'obtiens **543,4 j ouvrés (× 1,59), fin 2029-01-26** — 10 mois après la date publiée. La **dette n° 10 de `STATE.md`** (« les cadences V3 sont probablement optimistes d'un facteur 2 à 3, et elles portent **toutes** les durées du cours ») n'est ni citée, ni répercutée, ni même mentionnée dans le module. | majeur | Recalcul complet (script de contre-expertise, section D). `STATE.md` l. 128. `calc/planification.py` l. 620-627 : aucune variante sur les fourchettes. | Publier au moins une fourchette de date de fin (optimiste / retenue / pessimiste) et citer explicitement la dette n° 10 à côté de la « durée à contracter ». Une date unique issue de V3 non bornées est indéfendable en réunion — ce que le module reproche lui-même aux autres. |
| **M7** | **Figure 2 : un réseau qui ne montre pas ses dépendances.** Les boîtes se chevauchent (CHET/CHFA, CHLV/COUV, MARQ/FACA, MEZZ sur la rangée du dessous) et les liens passent **derrière** elles : aucune flèche n'est lisible. La légende dit « Un réseau sert à montrer une structure de dépendances ». | majeur | Capture `…figure2.png`. Le test de chevauchement ne compare que texte contre texte (dette n° 11), donc rien ne sonne. | Disposer les nœuds par rang topologique sur plusieurs lignes, avec un espacement garanti, et router les liens hors des boîtes. |
| **M8** | **Figure 6 : entrée de légende orpheline.** `courbeS` dessine toujours la légende « réalisé » quand il n'y a pas de `constat`, même sans série `realise`. Le § 8 impose l'inverse : chaque élément de la légende doit exister dans le dessin. | majeur | `assets/svgkit.js` l. 326-328 (branche `else`). Capture figure 6 : trait brique « réalisé » en légende, aucune courbe brique. | Ne tracer l'entrée que si `pts.some(p => p.realise != null)`. Étendre le contrôle de légende du build (aujourd'hui limité aux puces numérotées) aux entrées de légende de série. |
| **M9** | **Figure 1, légende fausse** : « Les durées déclarées sont **majoritaires en nombre** ». Elles sont **12 contre 12** calculées (et 3 imposées) — le module publie ce compte deux paragraphes plus haut. | majeur | `familles.nb_taches = {declaree: 12, calculee: 12, imposee: 3}`. Légende de la figure 1, 3ᵉ puce. | « à égalité avec les calculées », ou injecter les deux comptes par variable. Un verdict écrit à la main contredit par le chiffre d'à côté : c'est la famille exacte des trois derniers bloquants de la TV. |
| **M10** | **Nombres tapés à la main dans le texte** (§ 4.3 : « aucun nombre technique n'est tapé à la main ») : « = 58 jours gagnés » et « rend 58 jours ouvrés » ; « si la base-vie tient **59** personnes » ; « **67 %** d'occupation de la grue » (inventé, aucune sortie) ; « soit **cinq semaines** » (× 2) ; « ces **cent** jours » (× 2) ; « **trente-six** hypothèses » (M2) ; « vingt-sept » (× 4). Tous sauf « 67 % » sont justes aujourd'hui ; aucun ne suit `data/`. | majeur | `content/…md` l. 206, 279, 313, 368, 385, 410, 428, 469, 479. Le contrôle de balises ne couvre que les blocs normatifs. | Les passer en variables (`{{…}}`), y compris les écritures en lettres. Pour « 67 % », soit le calculer (B8), soit le marquer explicitement comme un énoncé d'exercice fictif. |
| **M11** | **Le test de recette des fenêtres est vrai par construction** : « le début tombe sur une fenêtre » vérifie `det["debut"]` contre `prochaine_fenetre(det["debut"], …)` — le point fixe de la fonction, donc toujours vrai. Aucun test ne confronte `consignations[i].debut` à `durees[i].debut_j`. C'est précisément ce trou qui laisse passer **B1**. | majeur | `calc/tests/test_planification.py` l. 88-90. | Remplacer par `abs(r["durees"][cle]["debut_j"] - det["debut"]) < 1e-6` et injecter un canari (décaler `premiere_fenetre_jour` de 1) qui doit faire sonner. |
| **M12** | **Le chantier compte 25 tâches dans `data/` et dans `calc/`, 27 dans le contenu.** `planning._role` : « une tâche parmi **vingt-cinq** » ; docstring de `planification.py` : « vingt-cinq » ; le contenu dit « vingt-sept » (× 4) et `nb_taches` en donne 27. | majeur | `data/projet-gare.json` l. 431 ; `calc/planification.py` l. 4 ; `content/…md` l. 25, 53, 159, 164. | Corriger les deux `_role`/docstring, ou mieux : ne plus écrire le compte en lettres nulle part. |
| **M13** | **Le lissage déplace les tâches dans leur marge TOTALE en laissant les successeurs à leur date au plus tôt** : l'histogramme lissé peut donc être infaisable (une tâche décalée après le démarrage de son successeur). Simplification non déclarée (R6) — le texte de `limite` ne parle que du caractère glouton. Ici sans conséquence (MEZZ +4 j ≤ 14,75 j de marge **libre**, NOYX +43 j ≤ 170,79 j), mais le garde-fou n'existe pas. | majeur | `calc/planification.py` l. 379-392 : `m = mg[i]["marge_totale_j"]`, et `histogramme_effectifs` ne décale que `i`. | Borner par la **marge libre**, ou repropager le réseau après décalage. Et déclarer la simplification dans `STATE.md`. |
| **M14** | **Figure 3, deux défauts.** (a) L'étiquette « PSOU » est tronquée en « **SOU** » par le bord gauche du cadre. (b) La légende annonce « Les deux barres de consignation sont longues et **presque vides** : leur longueur est de l'attente, pas du travail » — le Gantt les dessine **pleines**, identiques aux autres barres. La figure ne montre pas ce qu'elle prétend montrer (dette n° 13). | majeur | Capture `…figure3.png`, ligne 22 : « SOU · Raccordement du passage souterrain (consignation) ». Barres CHLV (80,13 j) et PSOU (43 j) uniformément remplies. | Élargir la marge gauche du Gantt en fonction du plus long libellé. Hachurer la part d'attente ou dessiner les fenêtres de travail en plein sur un fond d'étalement. |
| **m1** | **Quantités calculées et jamais publiées** : `deblais_transportes_m3` (6 200), `beton_semelles_m3` (170), `beton_poteaux_rdc_m3` (153) n'alimentent aucune durée, aucune figure, aucun texte. Le foisonnement est pourtant déclaré en S4b parmi « les ratios qui donnent les quantités » : le modifier ne change **rien**, contrairement à la promesse « changez une cadence et tous les nombres se recalculent ». | mineur | `calc/planification.py` l. 56-70 ; aucune occurrence de `deblais_transportes_m3` ailleurs. | Soit les publier (évacuation des terres, rotations de camions — c'est de la matière D2), soit les marquer `non_publiee` et retirer le foisonnement de la liste S4b. |
| **m2** | **Figure 4 : axe et étiquettes.** L'abscisse part de 0 alors que rien n'est tracé avant j 53 — 60 % du cadre est vide. « fin » touche le bord droit ; « début » est posée sur le trait bleu. La 3ᵉ puce parle de « deux droites de **métiers différents** qui se rapprochent » alors qu'une seule tâche est tracée. | mineur | Capture `…figure4.png`. | Cadrer sur [début − marge ; fin + marge], ancrer les étiquettes dans le cadre, reformuler la puce 3 au conditionnel. |
| **m3** | **La ligne d'équilibre ignore le lissage** : elle est tracée à `res["tot"]["MEZZ"][0] = 53,4` alors que le lissage retenu décale MEZZ de +4 j. Deux représentations du même plancher, deux dates. | mineur | `calc/planification.py` l. 512-514 ; `ressources.decalages_utilises_j = {"MEZZ": 4.0, "NOYX": 43.0}`. | Tracer la ligne d'équilibre sur le planning lissé, ou dire en légende qu'elle précède le lissage. |
| **m4** | **Figure 1 : arrondis à l'entier non signalés.** TERR 1,60 j → « 2 j » (+25 %), FOUI 3,91 → « 4 j », FOND 8,50 → « 9 j », MEZZ 31,85 → « 32 j ». | mineur | Capture `…figure1.png` contre `durees`. | Une décimale, ou mention « durées arrondies » en légende. |
| **m5** | **Deux libellés plus larges que leur métré** : « Terrassement général » n'est calculé que sur le **décapage** (la fouille est une autre tâche, mais rien d'autre n'est compté) ; « Semelles et longrines » n'est métré qu'en nombre de semelles, aucune longrine. | mineur | `calc/planification.py` l. 100-110. | Renommer, ou ajouter la quantité manquante. |
| **m6** | **Pas de double lecture entreprise / maîtrise d'œuvre.** Le module est écrit côté entreprise ; le § 1 et l'option O4 demandent aussi le regard MOE : visa du planning d'exécution, ordre de service de démarrage, constat de prolongation de délai, pénalités de retard, planning de référence opposable. L'encart « planning contractuel » effleure le sujet sans traiter l'acte de contrôle. | mineur | `content/…md` S4e ; § 6.2 O4 ; fiche de `cadrage/07-programme-31-10.md`. | Une sous-section S4f : ce que vise la MOE sur un planning, et sur quels critères elle le refuse. |
| **m7** | **Aucun chiffre de coût** (0 occurrence de « MAD ») alors que le module répète trois fois « le coût suit la durée de travail » et annonce « le pic de trésorerie ». Le critère 7 de la grille § 7.2 (lien avec le coût) n'est tenu que qualitativement. | mineur | `grep -c MAD content/02-d2-planification.md` → 0. | Acceptable tant que D1 n'est pas écrit, **à condition de le dire** : un renvoi explicite « chiffrage : module D1 ». |
| **m8** | **Le lissage ne change pas la moyenne et le module ne le dit pas** : `moyenne_avant = moyenne_apres = 24,4`. C'est le point le plus pédagogique de la section (on déplace, on ne supprime pas) et il est calculé puis jeté. | mineur | `ressources.moyenne_apres = 24.4`, jamais publié. | Publier les deux et en faire la démonstration. |
| **m9** | **La variante (c) laisse PSOU sous consignation** tout en étant présentée comme « la durée du réseau sans contrainte ». L'égalité numérique (273,87 j) ne tient que parce que PSOU porte 185,79 j de marge — elle est fortuite. | mineur | `variantes.protection_de_voie` ; `durees.PSOU.marge_totale_j = 185.79`. | Le dire, ou traiter les deux tâches. |
| **m10** | **Effet de seuil des fenêtres non commenté** : 12,13 j de travail → 5 fenêtres, dont la dernière utilisée **0,13 j**. Une période entière (20 j) est consommée pour une heure de travail. C'est un levier de conduite évident (rogner 0,13 j), jamais évoqué. | mineur | `consignations.CHLV`: `nb_fenetres = 5`, `duree_de_travail_j = 12.13`, reste = 0,13 j. | Un paragraphe : la sensibilité d'un planning sous fenêtres est **discontinue**, et c'est ce qui le distingue d'un planning ordinaire. |

**Total : 32 défauts — 8 bloquants, 14 majeurs, 10 mineurs.**

---

## 2. Les 10 points du § 12.2

**1 · Unités et homogénéité dimensionnelle.** **RAS.** $d = Q/(c \times n)$ est homogène sur les
quatre formes utilisées (m³, m², t, unités) ; j'ai refait les quatre à la main (§ 0.2). Le facteur
d'intempéries est sans dimension (21,7/20,2 = 1,074). La distinction cadence d'atelier / cadence
unitaire est explicitement portée par l'unité dans `cadences_chantier_V3._role` et dans S3a — c'est
bien fait. Seule réserve, sans gravité : `pint` ne couvre pas `planification.py` (le contrôle annonce
« 5 bibliothèques » ; `verif_unites.py` ne mentionne pas ce fichier).

**2 · Référentiels mélangés.** **RAS.** Aucun référentiel n'est invoqué, ce qui est conforme au
§ 5.0. Aucun mélange possible.

**3 · Article ou valeur normative sans V0/V1 — et respect du § 5.0.** **RAS sur l'interdit, réserve
sur la déclaration.** Zéro balise V2 dans le contenu (le contrôle 5.0 le vérifie et il est vert) ;
aucun calcul de dimensionnement ; les durées imposées (visa 40 j, fabrication 60 j, séchage 20 j)
sont présentées comme des **hypothèses V3 avec fourchette**, pas comme des délais réglementaires,
et le séchage précise qu'il remplace un critère de résistance indisponible. Les fenêtres de
consignation (3 j / 20 j) sont données comme des hypothèses, non comme une règle d'exploitant.
**Réserve** : `premiere_fenetre_jour = 40` est le seul paramètre d'exploitation publié sans aucune
déclaration (M3).

**4 · Ordres de grandeur et ratios.** **Défaut M6.** Les quantités sont cohérentes (312 t pour
4 800 m² de couverture = 65 kg/m², plausible pour des treillis de 32 m). Les cadences prises une à
une sont dans des fourchettes défendables. Mais : (a) 2 880 m² de plancher de mezzanine en 31,85 j,
soit 90 m²/j avec 27 compagnons, et 68 poteaux de 9 m en 11,33 j, c'est un gros œuvre très rapide ;
(b) une pointe de **59 personnes** pour un bâtiment voyageurs de 4 800 m² est basse ; (c) le total de
**7 863 j·h** (≈ 63 000 h, 13 h/m²) est bas pour un ERP avec couverture métallique, second œuvre et
lots techniques — et il est en plus **surestimé de 13,8 %** par B5, donc le travail réel modélisé
vaut ≈ 6 900 j·h. Surtout : la **dette n° 10** (cadences optimistes d'un facteur 2 à 3) n'est ni
citée ni répercutée. Le module la **répète en silence** et publie une date unique. Mon scénario au
bas des fourchettes donne 543 j et une fin en janvier 2029.

**5 · Cohérence data / figures / calc / durées / effectifs.** **Défauts B1, B3, M1, M2, M9, M10, M12,
m3.** La chaîne `data → calc → rendu` est réelle et la plupart des nombres sont des variables. Mais :
le réseau n'est pas dans `data/` (M1) ; la figure 5 recalcule sa propre moyenne (B3) ; `durees` et
`consignations` donnent deux dates pour CHLV (B1) ; huit nombres sont tapés à la main (M10) ; le
compte des tâches diffère entre `data/`, `calc/` et le contenu (M12).

**6 · Grille de profondeur § 7.2.** Voir § 3 ci-dessous : **deux critères sous le minimum de 2**.

**7 · Sécurité.** **Défaut B6, plus une réserve.** La rubrique S4c existe, elle est bien conçue (ce
que le planning *décide* des conditions d'exécution, et non une liste de consignes recopiées), elle
porte l'avertissement du § 3.4 et ne contient aucune valeur normative. Mais son affirmation centrale
sur le soutènement est **contredite par le réseau publié trois figures plus haut** (B6). Réserve
supplémentaire : B8 est aussi un sujet de sécurité — un levage sous pression de fenêtre avec une
grue en conflit non détecté est exactement la situation que S4c décrit comme dangereuse.

**8 · Vérité du rendu.** **Défauts B2, B3, B4, M7, M8, M14, m2, m4.** Zéro erreur console, aucune
requête réseau, toutes les figures non vides : les 16 contrôles sont verts. Mais trois légendes
décrivent ce que la figure ne montre pas (effectif lissé, palier de consignation, barres « presque
vides »), un réseau est illisible, une entrée de légende est orpheline et une étiquette est tronquée.
**Six des huit figures ont un défaut de rendu ou de légende.** C'est la dette n° 13 de `STATE.md` qui
se réalise une nouvelle fois : aucun contrôle ne vérifie qu'une figure montre ce qu'elle prétend.

**9 · Simplifications non signalées (R6).** **Défauts B5, M13, m10.** Le module déclare bien
l'heuristique gloutonne du lissage. Il ne déclare pas : que le décalage se fait dans la marge
**totale** sans repropager les successeurs (M13) ; que l'assiette jours-hommes est l'étalement et non
le travail (B5) ; que l'attente de fenêtre est calculée puis écartée du réseau (B1) ; que le modèle
de fenêtres est discontinu (m10). Le modèle de consignation est, dans son principe, le bon objet
pédagogique du module — mais trois de ses quatre propriétés ne sont pas dites.

**10 · Texte télégraphique ou remplissage / affirmation sans chiffre.** **RAS, et c'est le point
fort du module.** Chaque paragraphe porte une règle, un chiffre ou une méthode. Le propos est écrit
en phrases, les « pourquoi » sont là, l'encart sur le chemin critique contre-intuitif, la distinction
marge totale / marge libre, l'encart planning contractuel / planning de travail et l'exercice 4 sont
de la vraie matière de métier. Deux réserves de forme seulement : « 67 % d'occupation de la grue »
est une affirmation sans chiffre (M10), et la promesse « changez une cadence et tous les nombres se
recalculent » est vraie pour les cadences, fausse pour le réseau et le calendrier (M1).

### Point 11 (de mon cru) — la famille « modèle faux sous arithmétique juste »

C'est la famille qui a produit les quinze bloquants de la TV. Je l'ai cherchée en priorité ; **elle
est présente cinq fois sur huit bloquants.**

| Signature de la TV | Récidive dans D2 |
|---|---|
| Une grandeur d'état répartie au prorata au lieu d'être dérivée du réseau | **B5** : l'avancement en jours-hommes court linéairement pendant 80 j d'étalement dont 68 sans personne sur le chantier. **B4** : le palier annoncé n'est pas celui que le modèle produit. |
| Un paramètre déclaré dans `data/` mais réécrit en dur dans `calc/` | **M1** : tout le réseau, les 6 décalages négatifs et `JOURS_OUVRES_PAR_MOIS = 21,7`. C'est `cycle_zone` qui recommence, à l'échelle supérieure. |
| Un verdict écrit à la main que le chiffre d'à côté contredit | **M9** « déclarées majoritaires » contre 12 = 12. **B6** « le soutènement précède, jamais l'inverse » contre `SOUT: [("FOUI", -4)]`. **B3** « moyenne 22,9 » contre 24,4. **M2** « trente-six » contre 28. **M12** 25 contre 27. |
| Un taux appliqué à son complément | Non retrouvé. `CHAP = (1 − part)`, `CHLV = part` : **juste**, vérifié (22,53 + 12,13 = 34,67 = 312/9). |
| Une ressource vérifiée en moyenne au lieu d'être vérifiée en conflit | **B8** : identique, et cette fois le module **écrit la règle** dans sa check-list sans l'appliquer. |
| *(nouveau)* Une grandeur calculée, publiée, puis non réinjectée | **B1** : `attente_avant_premiere_fenetre_j = 17,47` est calculée, écrite dans le JSON, et n'entre jamais dans le réseau. La thèse même du module — « le chemin critique d'un chantier ferroviaire, c'est le réseau **plus** les fenêtres » — n'est qu'à moitié implémentée. |
| *(nouveau)* Un contrôle vrai par construction | **M11** (le début de fenêtre vérifié contre lui-même) et **M3** (le contrôle de registre ne voit que les objets `valeur + fourchette`). |

---

## 3. Grille § 7.2 (0 à 3, minimum 2 partout)

| Critère | Note | Justification |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | Les trois familles de durées, l'étalement contre l'allongement, la marge qui change de propriétaire, le chemin critique qui passe par un bureau d'études : chaque notion est amenée par son intuition avant sa formule. |
| Les hypothèses sont explicites | **2** | 28 V3 balisées, registrées, avec fourchette et année — rare et bien fait. Mais `premiere_fenetre_jour`, les 9 effectifs posés, les 6 décalages et `21,7` pilotent des résultats publiés sans être déclarés (M3, M1), et le compte annoncé est faux (M2). |
| Les formules sont justifiées | **2** | $d = Q/(c\,n)$ et le choix du moteur (nombre contre volume) sont démontrés et homogènes. La formule d'étalement est posée et justifiée, mais le modèle qu'elle sert est incomplet : la date de début n'en sort pas (B1). |
| L'exemple est vérifié | **1** | Trois contre-calculs (deux CPM + somme du chemin), tous verts, tous **à l'intérieur du même modèle**. Ma contre-expertise à l'aveugle sort un écart de **5,1 %** sur la durée du projet et de 27 jours calendaires sur la date contractuelle, plus 13,8 % sur l'assiette jours-hommes. Le § 3.3 plafonne à 5 %. |
| Le piège est identifié | **3** | S5, l'exercice 2 (renforcer une tâche non critique), l'exercice 4 (revue critique) et le quiz sont excellents, et le piège est systématiquement relié à son symptôme de terrain. |
| Le lien avec l'exécution est fait | **2** | Ateliers, cadences, fenêtres de consignation, pression sur les opérations à risque : le lien existe et il est juste. Mais la séquence publiée contredit la règle d'exécution que le module énonce lui-même (B6), et la ressource matérielle n'est jamais confrontée au planning (B8). |
| Le lien avec le coût et le délai est fait | **1** | Le délai est traité à fond. Le coût n'est jamais chiffré (zéro MAD), et l'assiette qui sert de proxy au coût — les jours-hommes de la courbe en S — est **fausse de 13,8 %** et contredit la phrase du module sur le coût (B5). Le renvoi à D1 n'est même pas écrit. |

**Deux critères sous le minimum de 2 (exemple vérifié, lien coût) : la grille § 7.2 n'est pas tenue.**
Le module ne peut pas être livré en l'état au titre du § 7.2, indépendamment de D-034.

---

## 4. Verdict

**32 défauts, dont 8 bloquants, 14 majeurs et 10 mineurs ; la grille § 7.2 échoue sur deux critères ;
le cœur du module — l'étalement sous consignation — publie une durée de projet inférieure de 5,1 % à
celle que son propre modèle implique, et cinq des huit bloquants sont la récidive exacte de la
famille d'erreurs des quinze bloquants de la tranche verticale.**

Note pour la suite, puisque D-034 n'autorise à corriger que les bloquants : **M1, M3, M9, M11 et M12
sont les amorces des bloquants de la prochaine passe** (réseau en dur, paramètres non déclarés,
verdicts écrits à la main, contrôles vrais par construction). Les porter en dette revient à garder
le mécanisme qui a produit B1 à B8.

---

## Suite donnée (20/10/2026, par l'auteur)

**Les 8 bloquants sont corrigés**, et chacun porte désormais un contrôle qui sonne :

| # | Correction | Contrôle ajouté |
|---|---|---|
| B1 | `Tache.au_plus_tot` dans `calc/cpm.py` : la contrainte externe passe par le moteur, honorée par **les deux** voies. Durée 341,86 → **362,92 j**, fin 2028-03-30 → **2028-05-01**. | 5 cas d'étalonnage à solution connue ; garde-fou qui lève si une tâche consignée démarre ailleurs que sur sa fenêtre ; test qui compare `durees[i].debut_j` à `consignations[i].debut` ; canari qui rejoue le réseau **sans** la contrainte et vérifie qu'il raccourcit |
| B2 | `histogramme` accepte une `serie2` et la trace en contour. | Le build **échoue** sur toute clé de directive ou option inconnue du générateur ; les générateurs déclarent leurs options (`SVGKit.OPTIONS`) |
| B3 | La moyenne n'est plus calculée dans le dessin : elle vient de `calc/`, avec sa définition en légende. | Même contrôle d'options ; la valeur est injectée par `{"$": "chemin"}` |
| B4 | Les paliers sont **cherchés** par `paliers_de_la_courbe` et leur cause nommée par `_cause_du_palier` ; la figure les dessine en bandes étiquetées. | Test : chaque palier porte une cause identifiée, et est vraiment plat sur la courbe publiée |
| B5 | `segments_de_travail` : histogramme **et** courbe en S accumulent sur le travail, pas sur l'étalement. 7 847 → 6 895 j·h. | Test qui recalcule les deux assiettes et vérifie que la publiée est la plus petite |
| B6 | Séquence inversée : `SOUT` succède à `TERR`, `FOUI` succède à `SOUT`. La paroi précède l'approfondissement, comme S4c l'écrit. | Test de séquence sur les dates publiées |
| B7 | Les recouvrements sont des **pourcentages de la durée du prédécesseur**, déclarés dans `data/planning.recouvrements_pct` avec fourchette. | `liens_resolus` lève si un recouvrement dépasse la durée qu'il recouvre ; test : aucun successeur ne démarre avant son prédécesseur |
| B8 | `conflits_de_grue` : profil **journalier**, et `resoudre_le_conflit_de_grue` cherche une résolution dans les marges libres. Verdict publié tel quel — **le conflit ne se résorbe pas**, le chantier demande une 2ᵉ grue. Nouvelle section S4g et figure 7. | Test qui recalcule le profil et un canari sur l'occupation moyenne |

**Majeurs et mineurs corrigés en plus** (au-delà de ce que D-034 exige) : M2, M4 (remplacé par la
décomposition du chemin, qui somme exactement et lève sinon), M6 (fourchette de date publiée :
×0,60 à ×2,41, 182 % d'étendue, avec renvoi explicite à la dette n° 10), M7 (réseau en serpentin,
liens routés et fléchés), M8, M9, M11, M12, M13 (lissage borné par la marge **libre**, invariant de
jours-hommes qui lève), M14, m4, m7, m8.

**Portés en dette déclarée** (`STATE.md`), conformément à D-034 : M1 (réseau en dur dans `calc/`),
M3 partiel (les 9 effectifs posés restent des nombres nus ; `premiere_fenetre_jour` est déclaré),
M5, M10 partiel, m1, m2, m3, m5, m6, m9, m10.

**Ce que cette passe a prouvé sur la méthode.** `npm run check` était vert sur 16 contrôles et n'a
vu aucun des huit bloquants. Six l'ont été par une **relecture de figure** ou une **comparaison de
deux nombres du même fichier de sortie** — jamais par un test. La dette n° 13 (« aucun contrôle ne
vérifie qu'une figure montre ce qu'elle prétend montrer ») reste la plus lourde du projet, et le
contrôle d'options ajouté ici n'en couvre qu'un bord : il attrape l'option ignorée en silence, pas
la légende qui ment.
