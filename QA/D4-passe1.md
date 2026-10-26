# D4 — Suivi et contrôle d'un chantier · passe adversariale n° 1

**Relecteur** : session distincte, n'a pas écrit le module. **Date** : 26/10/2026.
**Périmètre figé** : commit `90013a4`. Fichiers de C3 (`calc/gros_oeuvre.py`,
`content/05-c3-gros-oeuvre.md`, `QA/C3-passe1.md`) non touchés.
**Méthode** : Annexe 4 — contre-expertise à l'aveugle d'abord (scripts jetables dans le
scratchpad, **sans importer `calc/suivi.py`**), puis les dix points du § 12.2, puis un
onzième de mon cru. Aucun fichier du dépôt modifié hors ce rapport.

**État des contrôles au moment de la passe** : `npm run check` → **16/16 verts** ;
`python3 calc/run_all.py` → **VERT**. Les 39 vérifications de `test_suivi.py` sont vertes
et **n'ont vu aucun des huit bloquants ci-dessous**. C'est, pour la quatrième fois de
suite, ce que la contre-expertise trouve et que les tests ne trouvent pas.

---

## 0 · Contre-expertise à l'aveugle — cinq recalculs

Tout est reconstruit depuis `data/projet-gare.json`, `calc/sorties/planification.json`
(D2) et `calc/sorties/prix.json` (D1). `calc/suivi.py` n'a été ouvert qu'**après** ces
cinq calculs.

### 0.1 Avancement planifié de trois tâches à la date d'arrêt (j = 84 ouvrés)

Fraction des **segments de travail** de D2 écoulée à j = 84 :

| Tâche | Segments | Recalcul | `suivi.etats.planifie` | Écart |
|---|---|---:|---:|---:|
| CHFA | [40 ; 100] | **73,33 %** | 73,33 | 0,00 |
| PSOU | [60;63] [80;83] [100;103] | **66,67 %** | 66,67 | 0,00 |
| MEZZ | [45,81 ; 77,66] | **100,00 %** | 100,00 | 0,00 |

Les 27 postes concordent, ainsi que `prix.etats_a_la_date_d_arret`. **La dérivation de
l'état par `calc/etat.py` est juste, et D-039 tient à ce niveau-là.** C'est le seul des
cinq recalculs qui tombe exactement juste — les quatre autres ouvrent un défaut.

### 0.2 Valeur acquise et CPI

| | Recalcul indépendant | Publié | Écart |
|---|---:|---:|---:|
| VA sur les 27 postes de travaux (déboursé) | 21 139 037 | — | — |
| VA + frais de durée au prorata du temps | **22 505 553** | 22 505 360 | +0,001 % |
| CPI sur les seuls travaux | **0,8995** | — | — |
| CPI publié (travaux + frais au prorata) | 0,9577 | **0,9577** | 0 |

Le rapprochement n'a été obtenu qu'après avoir deviné que **5 904 000 MAD de frais de
durée entrent dans la VA au prorata du temps écoulé** (1 366 323 MAD, soit **6,1 % de la
VA**). Rien ne le dit dans le module. Sans cette ligne, le CPI tombe à **0,8995** : un
écart de 6,5 % sur l'indice de tête. → **bloquant B8**.

### 0.3 SPI global et SPI du chemin critique

Recalcul pondéré par `durees[i].duree_j` :

| | Recalcul | Publié | Écart |
|---|---:|---:|---:|
| Avancement global planifié / constaté | 47,73 / 44,57 % | 47,73 / 44,57 | 0 |
| **SPI en durée, global** | **0,9337** | 0,9337 | 0 |
| **SPI en durée, « chemin »** | **0,9774** | 0,9774 | 0 |
| SPI en valeur | 0,9141 (assiette déboursé travaux) | 0,9296 | 1,7 % |

L'arithmétique est exacte. Trois choses ne le sont pas :

- le « chemin critique » utilisé est la **chaîne la plus longue** publiée par D2
  (15 tâches), dont **neuf portent 39 à 49 jours de marge totale**. D2 publie lui-même
  `nb_taches_critiques: 6` et `les_deux_voies_designent_le_meme_chemin: false` ;
- les **six tâches à marge totale nulle** (CHLV, FACA, SECH, SECO, ESSA, RECE) sont
  **toutes à 0 % planifié et 0 % constaté** au jour 84. Le SPI des tâches qui portent
  réellement la date vaut **0/0 — il est indéfini** ;
- la totalité de la dérive de l'indice « de chemin » vient de **MEZZ** (−6 pts × 31,85 j
  / 265,4 j = **0,72 point**, soit exactement l'écart 32,17 − 31,45). MEZZ porte
  **39,81 j de marge totale et 22,34 j de marge libre**. → **bloquant B5**.

Le SPI en valeur (0,9296) rapporte une VA dérivée des **segments** à une VP lue sur la
**courbe de dépense** de D1, qui étale chaque tâche sur son *span* début→fin. Sur une VP
cohérente avec les états, SPI = **0,9189** et SV = **−1 987 483** au lieu de −1 705 517 :
**16,5 % d'erreur sur l'écart de délai publié**. → **bloquant B1**.

### 0.4 Montant retiré au visa

| | Recalcul | Publié | Écart |
|---|---:|---:|---:|
| Retrait sur les prix de vente (CHFA 1 022 112 + ETAN 118 755 + MEZZ 132 213) | **1 273 080** | 1 273 080 | 0 |
| **Net visé** (situation recalculée sur le constaté, `px.situation`) | **24 256 793** | 24 034 468 | **+222 325 MAD** |
| **Réduction du net** | **1 050 755 (4,15 %)** | 1 273 080 (5,03 %) | **21,2 %** |

Le module soustrait un montant de **travaux bruts** d'un **net révisé, après retenue de
garantie et remboursement d'avance**. → **bloquant B2**.

### 0.5 Coût complet de la modification

| | Recalcul | Publié | Écart |
|---|---:|---:|---:|
| Travaux | 1 200 000 | 1 200 000 | 0 |
| Frais de durée, 15 j × 16 268,18 MAD/j ouvré | **244 023** | 244 023 | 0 |
| **Coût complet** | **1 444 023** | 1 444 023 | **0** |

Exact, et la double conversion ouvré/calendaire que D1 vient de réconcilier est
respectée (16 268,18 = 5 904 000 / 362,92, cohérent avec les 18 mois calendaires ;
pénalités à 1,4004 j calendaire par jour ouvré, comme `px.cout_du_retard`). **RAS sur
l'arithmétique** — mais le délai de 15 jours n'a jamais été passé au réseau (→ M14) et
le nouveau BAC mélange deux assiettes (→ M12).

---

## 1 · Les dix points du § 12.2

### Point 1 — unités, homogénéité, assiettes
**Défaut.** Trois mélanges d'assiette : VP/VA (B1), visa brut/net (B2), ordre de service
/ déboursé sec (M12). Les deux calendriers de D1 sont en revanche **correctement**
utilisés (§ 0.5). Jours-hommes et dirhams sont bien séparés (S3b).

### Point 2 — référentiels mélangés
**RAS, prouvé.** `grep -n "BAEL\|RPS\|CCAG\|décret\|article\|NF \|EN 19\|Eurocode"
content/04-d4-suivi-controle.md` → **0 occurrence**. Les taux contractuels sont renvoyés
au CPS (`visa.avertissement_CPS`, repris dans le bandeau `meta`).

### Point 3 — valeur normative sans V0/V1 (§ 5.0 interdit toute V2)
**RAS, prouvé.** Aucune balise `⟦V2` dans le module ; les 13 balises sont toutes V3 et
toutes registrées (H136–H148). Contrôle `5.0` de `check.mjs` vert. Réserve mineure : la
règle « a + b + c = 1 » est énoncée comme un fait (→ m8).

### Point 4 — ordres de grandeur
CPI 0,96, SPI 0,93, part du visa 5 %, part cachée d'un avenant 17 % : tous plausibles.
**Mais** l'EAC est publiée sans bornes alors que la seule fourchette du coût réel la fait
varier de **56,9 à 76,9 MMAD** et **fait changer le CPI de côté** (0,83 à 1,13) →
**bloquant B6**.

### Point 5 — cohérence data / figures / calc / D1 / D2
**D-039 ne tient qu'à moitié.** Les **états** sont bien partagés (§ 0.1) : la situation de
D1 et le visa de D4 portent sur le même tableau d'avancement, et le test l.133-140 le
vérifie. Mais la **valeur planifiée** du même instant ne l'est pas : elle est lue sur la
courbe de D1, qui étale PSOU sur son span 60→103 (55,81 %) pendant que l'état le dérive
de ses trois fenêtres (66,67 %). Deux modèles d'avancement planifié coexistent dans le
même SPI (B1). Autres incohérences : le mois 4 de D4 contre 3,88 de D1 (M2), le
« financier » déclaré contre le visa de la section suivante (M1).

### Point 6 — grille § 7.2
Voir § 4 : **deux critères sous le minimum de 2**.

### Point 7 — sécurité (§ 3.4) : S4c est-elle réelle ou décorative ?
**Réelle, et c'est la bonne surprise du module.** Quatre risques qui appartiennent
vraiment au suivi (production pour le tableau de bord, pression de rattrapage, constat
contradictoire sur ouvrage en cours, levée d'un point d'arrêt sous contrainte de
facturation), chacun avec sa disposition, un renvoi explicite au plan HSE et aux
obligations du marché, et le lien chiffré avec le visa du module (« un visa qui réduit
s'accompagne d'une date de reconstat »). La ligne « consignation si l'ouvrage est en
interface avec la voie » est spécifique au cas ferroviaire. **RAS.** Réserve : rien de
tout cela n'est outillé — le 16ᵉ contrôle de `check.mjs` ne cherche qu'un mot
(simplification déclarée n° 9 de STATE.md).

### Point 8 — vérité du rendu
Quatre captures examinées. Défauts : figure 2 triée par une grandeur qui n'est pas la
sienne (M10) et légende qui enseigne sur un point tombant dans la bande « non
significative » (M11) ; figure 1 avec une bande [0 ; 100] qui couvre tout le dessin
(m2) ; figure 3 dont la cote « 2,7 pts » est non signée et sans trait de rappel (m3).
Aucun chevauchement de texte, aucune variable non résolue
(`grep -o "{{[^}]*}}" modules/04-*.html` → vide ; `NaN`, `undefined`, `Infinity` → 0).

### Point 9 — simplifications non signalées (R6)
Quatre, aucune déclarée : **(a)** les frais de durée entrent dans la VA **au prorata du
temps** (B8) ; **(b)** la VP vient d'un étalement uniforme sur le span (B1) ; **(c)** la
dérive constatée est un **décalage constant en points** appliqué à l'avancement planifié
— elle grandit donc avec la taille de la tâche et ne dépend pas de la date où celle-ci a
commencé, et elle n'est jamais convertie en jours (M7) ; **(d)** la simulation de
fiabilité du CPI n'utilise quasiment pas la dérive qu'elle prétend simuler (M6).

### Point 10 — remplissage ou télégraphie
**RAS pour l'essentiel.** 5 279 mots, écrits en phrases, chaque paragraphe porte une
règle, un chiffre ou une méthode. Trois répétitions littérales (m7).

---

## 2 · Point 11 — la famille « arithmétique juste, modèle faux »

La question posée : **le module affirme que l'indice global « sur-alarme » parce que la
dérive la plus visible est absorbée par une marge. Que montre exactement son calcul ?**

Il montre quatre choses, et aucune n'est celle-là.

1. **Il ne compare jamais le retard à la marge.** Le seul calcul fait est
   0,9337 contre 0,9774. La phrase « elle dispose de 17 jours de marge, et son retard y
   est absorbé » repose sur une comparaison — 18 points × 60 jours = **10,8 jours de
   retard** contre **17,47 jours de marge** — qui **n'existe nulle part**, ni dans
   `calc/suivi.py`, ni dans `suivi.json`, ni dans `test_suivi.py`. Le test l.114-117 se
   contente de vérifier que le poste le plus en retard n'est pas dans la liste du chemin,
   et **écrit la conclusion dans sa propre chaîne de détail** (« la derive la plus visible
   est absorbee par la marge »). C'est un verdict écrit à la main, pas une sortie de
   `calc/` — la règle que STATE.md déclare absolue depuis la TV.
2. **La « marge de 17 jours » de CHFA EST l'attente de la fenêtre de consignation.**
   CHAP finit au jour 122,53, CHLV est épinglé au jour 140 : **140 − 122,53 = 17,47**,
   exactement la marge totale de CHET, CHFA et CHAP. Le module en fait **deux arguments
   indépendants** dans le même encart — la marge d'abord, puis « une raison de plus […]
   le levage est épinglé au jour 140 ». C'est un double compte du même objet.
   Accessoirement, la marge **libre** de CHFA est **nulle** : le retard pousse CHAP
   immédiatement et consomme la marge de toute la chaîne, pas la sienne.
3. **L'indice censé dire si la date tient ne dit rien de la date.** Les six tâches à
   marge nulle sont à 0/0 au jour 84 (§ 0.3). L'indice publié mesure une chaîne dont
   neuf tâches sur quinze ont 39 à 49 jours de marge.
4. **La dérive de cet indice est elle-même absorbée par une marge.** Elle vient
   intégralement de MEZZ, 39,81 j de marge totale. L'indice « du chemin critique »
   est donc construit sur exactement ce que l'encart reproche à l'indice global.

**Réponse courte** : son calcul montre que la dérive pondérée par les durées vaut 3,16
points sur l'ensemble et 0,72 point sur une chaîne dont il a exclu CHFA par construction.
Il ne montre pas qu'une marge absorbe quoi que ce soit — il montre qu'une tâche a été
retirée du dénominateur.

Les cinq autres figures imposées de la famille, toutes trouvées :

| Figure cherchée | Trouvée |
|---|---|
| Une grandeur d'état répartie au prorata au lieu d'être dérivée | **B8** : 1,37 MMAD de frais de durée au prorata du temps dans la VA — dans le module dont l'encart central dit « une grandeur d'état se dérive, elle ne se répartit pas ». Et **B1** : la VP est un étalement uniforme |
| Un paramètre déclaré jamais relu | **M4** : `suivi_chantier.incertitude_sur_le_cout_reel` — `grep -rn` → **une seule occurrence, dans `data/`**. Récidive exacte du bloquant **B6 de D1** |
| Un verdict écrit à la main que le chiffre d'à côté contredit | **B3** « ils ne pointent pas dans le même sens » (0,9337 et 0,9774 sont tous deux sous 1) et **B4** « le chantier est en avance de 11,98 points » (les trois SPI disent l'inverse) |
| Une base de ratio ou d'indice prise là où elle n'est pas définie | **B7** : la bande 0,95–1,05 rend un verdict sur quatre indices de trois assiettes — D-037 nommait D4 explicitement |
| Un taux appliqué à son complément | **B2** : un retrait de travaux bruts soustrait d'un net révisé, retenue et avance déduites |
| Un double compte | **point 2 ci-dessus** : la marge de CHFA et la fenêtre de consignation sont le même objet, comptés deux fois |

---

## 3 · Tableau des défauts

| # | Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|---|
| **B1** | **La VP et la VA du même SPI reposent sur deux modèles d'avancement planifié différents.** `valeur_acquise()` l.84 prend `vp = depense["cumul"](84)` — la courbe de D1, qui étale chaque poste **uniformément sur son span début→fin** (`prix.json → courbe_de_depense.hypothese_de_profil`). La VA, elle, est dérivée des **segments de travail**. Pour PSOU les deux divergent : span 60→103 ⇒ 55,81 %, segments ⇒ 66,67 %. | **bloquant** (cohérence entre modules) | VP interpolée sur la courbe = 24 210 877 = la valeur publiée, au dirham près. VP reconstruite sur les états = **24 493 036**. Seul PSOU diffère : 2 600 000 × (0,6667 − 0,5581) = **282 171 MAD**. Conséquence : SV publié **−1 705 517** contre **−1 987 483** → **16,5 % d'erreur**, et la cote « 2,7 pts » de la figure 3 vaut en réalité 3,1. SPI 0,9296 contre 0,9189. | Construire la VP depuis les **mêmes états planifiés** que la VA (`Σ budget × planifié + frais × j/durée`), ou faire produire par D1 une courbe de dépense bâtie sur les segments et non sur le span. Puis un test qui compare les deux voies à 1 MAD près — c'est le test que D-039 aurait dû entraîner. Republier SV, SPI, la cote de la figure 3 et les trois EAC. |
| **B2** | **Le net visé soustrait un montant brut d'un montant net.** `visa_de_situation()` l.239 : `net_vise = sit["net_cumule_a_payer_MAD"] - retire`, où `retire` est une somme de **prix de travaux**, non révisés, avant retenue de garantie et avant remboursement d'avance. Le module enseigne au contrôle n° 4 que « la retenue porte sur le montant **révisé** » et commet la faute symétrique sur sa propre réduction. | **bloquant** (erreur de calcul) | `px.situation(d, bord, etats["constate"])` — la machinerie existe déjà — donne net = **24 256 793**, contre **24 034 468** publié : **222 325 MAD d'écart, 17,5 % du retrait**. Décomposition : révision +84 914, retenue de garantie −95 060, remboursement d'avance −212 180. Réduction réelle du net : **1 050 755 (4,15 %)**, pas 1 273 080 (5,03 %). Le chiffre est republié **six fois** (S4c, S4e ×2, S5, S8, exercice 4). | Calculer la situation visée en rejouant `px.situation` sur l'état **constaté**, et publier côte à côte : retrait sur les travaux (1 273 080) **et** effet sur le net (1 050 755). Ajouter le canari : fausser l'assiette doit faire rougir. |
| **B3** | **« Ils ne pointent pas dans le même sens » — les deux indices pointent dans le même sens.** S4c : « **4,4 points d'écart entre les deux indices**, et ils ne pointent pas dans le même sens ». 0,9337 et 0,9774 sont **tous deux inférieurs à 1** : les deux disent « en retard », avec deux amplitudes. | **bloquant** (verdict contredit par le chiffre d'à côté) | Rendu HTML de S4c, et figure 4 : les quatre barres sont sous 1,00. `suivi.json → spi_du_chemin`. | « Les deux disent la même chose — en retard — mais pas avec la même gravité : 0,93 déclenche un plan de rattrapage, 0,98 n'en déclenche pas. » Et faire produire la phrase par `calc/` à partir du signe des deux écarts. |
| **B4** | **« Le chantier est en avance de 11,98 points » contredit les trois SPI du module.** Exercice 1 (*piège*) : « là où le chantier est en avance de 11,98 points sur sa production ». Exercice 4, point 1 : « le chantier est en **avance** de 11,98 points sur sa production, et le point mensuel annonce l'inverse ». Les 11,98 points sont l'écart physique − **temporel** : comparer un avancement à un prorata du temps est exactement l'erreur que l'encart de S3a et l'« erreur courante » de la figure 1 dénoncent. | **bloquant** (verdict contredit par ses propres chiffres) | SPI valeur **0,9296**, SPI durée global **0,9337**, SPI chemin **0,9774** : le chantier a produit **moins** que le plan ne le prévoyait à cette date. Le seul référentiel par rapport auquel il est « en avance » est le prorata du temps, que le module déclare incapable de rien mesurer. | Écrire : « il a produit 35,1 % pour 23,2 % du délai consommé — ce qui ne veut **pas** dire qu'il est en avance : par rapport au plan, il est à 0,93. Le prorata du temps n'est pas une référence. » C'est d'ailleurs une bien meilleure leçon. |
| **B5** | **Le « SPI du chemin critique » n'est pas celui des tâches qui portent la date.** `spi_du_chemin_critique()` reçoit `f["contre_calcul"]["chemin_critique"]`, la chaîne la plus longue de D2 (15 tâches). Neuf d'entre elles portent 39 à 49 jours de marge totale. Les **six** tâches à marge nulle sont toutes à **0 % planifié** au jour 84 : l'indice qui « engage une date » vaut **0/0**. | **bloquant** (modèle faux ; le module l'annonce comme sa contribution n° 3) | `durees[i].critique = True` pour CHLV, FACA, SECH, SECO, ESSA, RECE uniquement ; `segments_de_travail` les place toutes après le jour 140. D2 publie `nb_taches_critiques: 6` et `les_deux_voies_designent_le_meme_chemin: **false**`. L'écart 32,17 → 31,45 vient à 100 % de MEZZ : 6 pts × 31,85 j / 265,4 j = **0,72 point** ; MEZZ a **39,81 j de marge totale**. | Publier les deux : l'indice de la chaîne, et celui des tâches à marge nulle — **en disant qu'il est indéfini à cette date parce qu'aucune n'a commencé**. C'est le résultat pédagogique le plus fort disponible ici : au 4ᵉ mois d'un chantier sous fenêtre, **aucun indice ne peut rien dire de la date**, et seule la marge le peut. Le module arrive à cette conclusion dans l'exercice 2 sans jamais la calculer. |
| **B6** | **D-036 n'est pas appliquée, alors qu'elle nomme D4.** « le même traitement est attendu de D1 sur les coûts et **de D4 sur les prévisions à terminaison** ». D4 publie trois EAC, une EAC retenue et une nouvelle EAC après modification — **toutes en valeur unique**. | **bloquant** (décision validée non appliquée ; D-036) | `grep -c "borne" content/04-d4-suivi-controle.md` → **0**. `grep "fourchette"` → 0. Sur la seule fourchette déclarée du coût réel (20 à 27 MMAD, H145) : CPI de **1,1253 à 0,8335**, EAC retenue de **56 942 025 à 76 871 734 MAD** (±30 %). **À la borne basse le CPI passe au-dessus de 1** : le diagnostic « dérive systématique, c'est la deuxième EAC qu'on annonce », martelé en S4b et en exercice 3, **change de signe à l'intérieur de la fourchette que le module déclare lui-même**. | Ajouter une `variante_aux_bornes` sur le modèle de `calc/planification.py` : pousser les 13 V3 au même bout et publier CPI, SPI et EAC entre bornes. Et dire que le diagnostic ne survit pas à la borne basse du coût réel — c'est la leçon, pas une faiblesse. |
| **B7** | **D-037 n'est pas appliquée, alors qu'elle nomme D4.** « La règle s'applique à **D4 (indices de performance)** ». `figures()` l.314 : `BANDE = (0.95, 1.05)`, en dur, appliquée indifféremment au CPI, au SPI en valeur et aux deux SPI en durée — trois assiettes différentes, comme la première puce de la légende le dit elle-même (« Le CPI et le SPI ne se lisent pas sur la même assiette »). Aucun champ `ratio_defini_sur_cette_base`, aucune ligne de registre, aucune source. | **bloquant** (verdict rendu sur une base non définie) | `calc/prix.py:1117` porte `ratio_defini_sur_cette_base` ; `grep "ratio_defini" calc/suivi.py` → **0**. Figure 4 : deux barres sont peintes en rouge « hors de la bande de conformité », et la légende ajoute « et pourtant aucun n'est alarmant isolément » — une bande qui classe puis se désavoue. | Soit une bande par assiette, justifiée et registrée en V3 ; soit pas de bande du tout et un commentaire par indice. Dans tous les cas, sortir le seuil de `calc/` vers `data/` et lui donner sa ligne de registre. |
| **B8** | **La valeur acquise contient 1,37 MMAD répartis au prorata du temps.** `valeur_acquise()` l.83 : `va += frais_de_duree_total × min(1, j/duree_totale)`. Le module définit la VA au glossaire comme « le budget des **ouvrages réellement exécutés** », et son encart de S3a interdit le prorata en toutes lettres. Rien, nulle part, ne signale ce traitement (R6). | **bloquant** (R6 + contradiction avec la thèse centrale du module) | 5 904 000 × 84/362,92 = **1 366 323 MAD**, soit **6,1 % de la VA** et 9,2 % du BAC. Sans cette ligne : CPI **0,8995** au lieu de 0,9577 (**−6,1 %**), CV **−2 360 963** au lieu de −994 640 (le signe du commentaire change de ton). Le prorata porte en outre sur la durée **planifiée** : un chantier en retard acquiert ses frais plus vite que son ouvrage. | Garder le traitement — il est défendable pour des coûts indexés sur le temps — mais **le déclarer** comme simplification dans le module et dans STATE.md, le sortir du total « physique » ou l'afficher en ligne séparée, et préférer `min(1, j/durée **prévisionnelle à date**)`. Ajouter le test qui isole les deux composantes de la VA. |
| **M1** | **L'« avancement financier » publié est le net DÉCLARÉ.** `trois_avancements()` l.53 lit `sit["net_cumule_a_payer_MAD"]`, et `sit` est calculée sur `etats["declare"]` (l.356). Le module publie donc en figure 1 un avancement bâti sur l'état que sa thèse centrale interdit d'utiliser — et que son propre visa ampute de 1,27 MMAD deux sections plus loin, sans un mot. La légende ajoute « L'entreprise a construit plus qu'elle n'a **encaissé** » : à 60 jours de délai de paiement, elle n'a **rien** encaissé de cette situation. | majeur | Sur l'état constaté : **32,36 %** au lieu de 33,76 ; l'écart physique − financier passe de **1,37 à 2,76 points**, soit le double de ce que la légende commente. `prix.json → tresorerie.delai_de_paiement_j_calendaires = 60`. | Publier le financier **déclaré et visé** (33,76 / 32,36 %), remplacer « encaissé » par « facturé », et renvoyer à la trésorerie de D1 pour l'encaissement. |
| **M2** | **`mois = j / 21`, en dur dans `calc/`.** l.365. D1 dérive le mois du calendrier (`jours_ouvres_par_mois_calendaire = 21,66`) et publie `mois_ecoules = 3,88` pour **le même instant**. D4 publie « le mois 4 ». | majeur (R1 ; récidive de la dette n° 14 de D2, « `21,7` en dur dans `calc/` ») | `calc/suivi.py:365` contre `calc/prix.py:849`. `data/projet-gare.json:433` porte même `jours_ouvres_par_mois: 21` — D4 n'utilise ni la donnée ni la valeur dérivée, mais un littéral. | Lire `fd["conversion"]["jours_ouvres_par_mois_calendaire"]`, et ajouter au contrôle de cohérence : deux modules qui datent le même instant doivent le dater pareil. |
| **M3** | **Deux seuils V3 vivent dans `calc/`, hors `data/` et hors registre, et pilotent deux verdicts publiés.** `derive_pct = 6.0` (l.145) et `BANDE = (0.95, 1.05)` (l.314). | majeur (R1, § 3.2) | `derive_simulee_pct` est **publié dans le module** (ligne 183 du contenu) et n'a **aucune ligne** dans `registre-hypotheses.csv` — le contrôle `3.2` ne voit rien parce qu'il ne balaie que `data/`. | Les deux dans `data/suivi_chantier`, avec fourchette et note, donc dans le registre. |
| **M4** | **`incertitude_sur_le_cout_reel` est déclaré, registré (H146), et jamais lu.** `fiabilite_du_cpi()` prend son bruit de `bord["frais_de_duree"]["cout_MAD_par_mois"]` : la valeur coïncide, mais la donnée ne pilote rien. La passer à 3 mois ne change pas un chiffre du module. | majeur (récidive exacte du **bloquant B6 de D1**) | `grep -rn "incertitude_sur_le_cout_reel"` → **une occurrence, dans `data/projet-gare.json:1873`**. Le contrôle de `check.mjs` annonce « chaque V3 de data/ **lue par un module** est registrée » alors qu'il ne vérifie **aucune lecture** (il compare des nombres au registre) : la correction proposée par D1-B6 — « toute clé de `data/` non lue par un `calc/` échoue le build » — n'a pas été mise en place, et le défaut est revenu au module suivant. | Multiplier le bruit par ce coefficient (`bruit = cout_MAD_par_mois × incertitude.valeur`), et implémenter enfin le contrôle de lecture. |
| **M5** | **Le seuil de lisibilité du CPI est un artefact de grille, publié à 0,1 point près.** `pas = 10` jours. Entre j = 40 et j = 50, l'avancement saute de **14,6 % à 21,9 %** : la résolution du résultat est de **± 7 points**, et la valeur publiée partout (S4d, fiche mémo, exercice 4) est « **21,9 %** ». | majeur (fausse précision) | `fiabilite_du_cpi.points` : j40 → 14,6 % / 6,24 pts ; j50 → 21,9 % / 4,17 pts. Le premier point sous 6 est j50 **parce que** j45 n'est pas échantillonné. | Dichotomie sur `j`, ou publication d'un encadrement « entre 15 % et 22 % ». |
| **M6** | **La « simulation d'un chantier qui dérive » ne fait pas dériver grand-chose, et compare une largeur à une demi-grandeur.** L'incertitude vaut `va·2b/(cr²−b²)` avec `cr = va(1+δ)` : δ n'y entre que par (1+δ)² ≈ 1,12. Le calcul se réduit à « quand CR dépasse-t-il 2·bruit/δ ? ». Et `incertitude_pts` est une **largeur totale** (± 1 mois de frais, pic à pic) comparée à une dérive **unilatérale** de 6 % — qui vaut d'ailleurs 5,66 points de CPI, pas 6. | majeur (modèle) | Trois critères également défendables : demi-largeur < δ → **8,3 %** ; la barre d'erreur exclut 1,00 (CPI_max < 1 à j30) → **12,0 %** ; largeur totale < δ (publié) → **21,9 %**. Un facteur **2,6** entre le plus et le moins exigeant. `ce_que_ce_calcul_ne_prouve_pas` ne mentionne que la dépendance au bruit, pas le choix du critère. | Écrire le critère en une ligne de formule, le nommer, et publier les trois seuils : c'est plus honnête et c'est le même travail. |
| **M7** | **Le retard n'est jamais converti en jours, et la « marge restante » que le module ordonne trois fois de suivre n'est publiée nulle part.** | majeur | Check-list n° 7, exercice 2 (« suivre la marge restante comme un indicateur à part entière »), exercice 4 (« on demande […] la marge restante sur les tâches qui ont dérivé »). `grep "marge restante"` dans `suivi.json` → **0**. Calcul immédiat depuis D2 : CHFA 10,80 j de retard sur 17,47 de marge → **6,67 j restants** ; MEZZ 1,91 sur 39,81 ; NOYX 2,00 sur 199,47 ; ETAN 1,44 sur 214,47 ; PSOU **+0,36 j d'avance**. | Une fonction `marges_apres_derive()` et un tableau de cinq lignes. Trois lignes de code pour le seul indicateur que le module déclare décisif. |
| **M8** | **Double compte : la marge de CHFA et la fenêtre de consignation sont le même objet.** L'encart de S4c donne la marge comme raison, puis la fenêtre comme « une raison de plus ». | majeur | **140 − 122,53 = 17,47 j** = `durees.CHFA.marge_totale_j` au centième. De plus `marge_libre_j = 0` : le retard de CHFA **pousse CHAP immédiatement**, et la marge consommée est celle de toute la chaîne CHET-CHFA-CHAP. | Une seule phrase : « sa marge **est** l'attente de la fenêtre — 17,5 jours entre la fin de la charpente d'appui et le jour 140 ; et elle n'est pas à elle, elle est à toute la chaîne ». |
| **M9** | **« Plus de vingt points en milieu de chantier » : au milieu, c'est 13,4 points.** Affirmation écrite à la main **trois fois** (S3b, légende de la figure 3, tableau S5) alors que `calc/` publie la valeur. | majeur (R1, § 4.3 : aucun nombre technique tapé à la main) | `prix.json → ecart_depense_travail` : j = 181 (vrai milieu) → **13,4 points** ; le maximum **24,7** est au **jour 260**, soit **71,6 %** de la durée. | `{{prix.ecart_depense_travail.ecart_maximal.ecart_pts}}` et `…​.j`, et « au jour 260, soit aux trois quarts du chantier ». |
| **M10** | **Figure 2 : les barres sont triées par une grandeur qui n'est pas celle qu'elles portent.** `figures()` l.312 trie par `-|declare − constate|` (l'optimisme déclaré) une figure dont le sujet est la dérive `constate − planifie`. | majeur (rendu) | Capture `figure2.png` : CHFA −18, ETAN −12, **MEZZ −6, NOYX −8**, PSOU +4. Ni croissant, ni décroissant. La légende affirme « Le poste le plus en retard est [le premier] » — vrai ici par coïncidence — et l'« erreur courante » reproche de « classer les dérives par leur taille », alors que la figure les classe par une troisième chose, non dite. | Trier par la valeur tracée, ou trier par criticité **et le dire dans la légende**. |
| **M11** | **Figure 2 : la légende enseigne sur un point que son propre dessin déclare non significatif.** Puce 2 : « Un poste est en AVANCE, et ce n'est pas une bonne nouvelle en soi ». Ce poste est PSOU, **+4 points**, et la bande grise du dessin — « dérive non significative », [−5 ; +5] — le contient. | majeur (rendu : la légende affirme ce que le dessin ne montre pas) | Capture `figure2.png` : la barre PSOU se termine à l'intérieur de la bande. En jours : **0,36 jour d'avance**. | Porter l'avance de PSOU à l'extérieur de la bande dans `data/`, ou réécrire la puce : « le seul poste en avance l'est de 0,4 jour, dans le bruit de mesure — et même s'il l'était vraiment, il ne rattraperait rien ». |
| **M12** | **`nouveau_BAC` additionne un prix et un déboursé.** l.279 : `bac2 = BAC_deboursé_sec + montant_travaux + frais`. Or `montant_travaux_MAD` est un **ordre de service** (`_nature` : « travaux supplémentaires » de la maîtrise d'ouvrage), donc un prix de vente. | majeur (assiette) | `bac = bord["debourse_sec_MAD"]` (l.80) ; coefficient de vente 1,17 ⇒ l'équivalent déboursé serait ≈ 1 025 600, soit **174 400 MAD** de trop dans le nouveau BAC, et autant ×1/CPI dans la nouvelle EAC. | Convertir au déboursé avant d'ajouter, ou publier le nouveau BAC en prix de vente et le dire. |
| **M13** | **« Refuser le délai coûte plus cher que l'accorder » ne nomme pas le côté de la table.** Pour l'entreprise, oui. Pour le maître d'ouvrage, refuser **rapporte 1 574 774 MAD de pénalités** et lui épargne les 244 023 MAD de frais. Dans un module qui pratique la double lecture entreprise / MOE, l'affirmation est à moitié fausse selon le lecteur. | majeur | `modification.penalites_evitees_MAD = 1 574 773,52`. `test_suivi.py` l.155 « verifie » la phrase par `total > frais` — une tautologie (a + b > a) qui n'interroge jamais qui paie. | « Du point de vue de l'entreprise, refuser coûte 1,82 MMAD contre 0,24 ; du point de vue du maître d'ouvrage, c'est exactement l'inverse, et c'est pourquoi l'argument se pose avec le coût du **chantier**, pas avec celui de l'entreprise. » |
| **M14** | **Le délai de 15 jours « se répercute entier » : affirmé, jamais passé au réseau.** La tâche touchée est le levage au-dessus de la voie (CHLV), **épinglée sur des fenêtres de consignation tous les 20 jours**. Un retard de 15 jours en amont ne se répercute ni entier ni proportionnellement : il disparaît dans l'attente, ou il coûte une fenêtre entière. | majeur (modèle) | `segments_de_travail.CHLV = [140;143] [160;163] [180;183] [200;203] [220;220,13]`. `decomposition_du_chemin` : 48,67 j d'attente de fenêtre + 68 j d'immobilisation entre fenêtres, soit **32,1 % de la durée du chantier**, et sa `lecture` dit « doubler les équipes ne les touche pas d'un jour ». `impact_modification()` ne touche jamais au réseau : il multiplie 15 par un taux journalier. | Rejouer le CPM avec la contrainte décalée et publier le délai **obtenu**, pas le délai supposé. C'est la démonstration la plus parlante du module, et elle est à portée de main : `pln.voie_A_parcours` est déjà importé. |
| **M15** | **Le contre-calcul O7 ne contre-calcule presque rien.** Sur 39 vérifications (30 appels, dont plusieurs en boucle) : huit réécrivent une définition (CPI = VA/CR, SV = VA − VP, part cachée = frais / total…), une est circulaire (l.124-129 : le seuil est **défini** comme le premier point sous δ, et le test vérifie qu'il est sous δ), une est une tautologie (l.155, a + b > a), une **écrit la conclusion dans sa chaîne de détail** (l.114-117). Le seul contrôle qui touchait à B1 (l.93-96) vérifie que VP/BAC s'écarte de plus de 5 points du prorata temporel — il ne compare **jamais** la VP aux états planifiés. | majeur | `calc/tests/test_suivi.py`, lignes citées. Les 39 sont vertes ; aucune ne voit B1 à B8. Deux canaris seulement (l.42-46 et l.98-105), pour **huit** verdicts publiés (physique, CPI, SPI, SPI de chemin, seuil de lisibilité, montant retiré, coût complet, nouveau BAC) — récidive du majeur M9 de D1. | Un canari par verdict : étaler PSOU sur son span et vérifier que la VP rougit ; retirer les frais de la VA et vérifier que le CPI bouge ; supprimer MEZZ du chemin et vérifier que le SPI de chemin devient 1,000 ; soustraire le retrait du brut et vérifier l'écart sur le net. |
| **m1** | « L'écart maximal entre les deux lectures **dépasse 40 points**, et le test de ce module le vérifie » : 40 est le **seuil** du test, pas le résultat. | mineur | `test_suivi.py` l.45-46 : `max(ecarts) > 40`, détail imprimé **76,8**. Le vrai écart maximal est 100 − 23,15 = **76,85 points**. | Publier la valeur, pas le seuil. |
| **m2** | Figure 1 : `bande: [0,100]` légendée « 0 à 100 % » — elle couvre l'intégralité du graphique et n'apprend rien. | mineur | Capture `figure1.png` : le rectangle vert couvre toute la zone de traçage. | Retirer l'option, ou la remplacer par un repère utile (l'avancement temporel, par exemple). |
| **m3** | Figure 3 : la cote « **2,7 pts** » est **non signée** alors que l'écart est négatif, et aucun trait ne relie le point à la courbe, alors que la légende parle d'« écart coté à côté ». | mineur | Capture `figure3.png`. SV = −1 705 517 MAD ⇒ −2,66 points. | « −2,7 pts » et un segment vertical entre le point et la courbe. |
| **m4** | Figure 2 : les libellés sont des codes de poste (« CHFA · planifié 73 % ») que la légende doit traduire en français. | mineur | Capture `figure2.png` ; `figures()` l.328 construit `f"{i} · planifié …"` au lieu d'utiliser `par_id[i]["libelle"]`, disponible. | Utiliser le libellé, garder le code entre parenthèses. |
| **m5** | `_clamp` plafonne silencieusement constaté et déclaré à 100 : une déclaration supérieure à 100 — le cas qu'un visa rencontre vraiment — disparaîtrait sans trace. | mineur | `calc/etat.py`, `_clamp(c + optimisme)`. MEZZ atteint exactement 100,0 (94 + 6). | Signaler le plafonnement quand il mord. |
| **m6** | `max(1.0, cr_vrai - bruit)` (l.165) : garde-fou silencieux qui produirait une incertitude de plusieurs milliers de points s'il mordait. | mineur | Il ne mord pas aux valeurs actuelles (j = 10 : CR − bruit = 1,94 MMAD). | Exclure le point au lieu de le borner. |
| **m7** | Répétitions littérales : « un prorata partage son hypothèse avec ce qu'il mesure » **3 fois**, « une marge consommée n'est plus disponible » **2 fois**. | mineur | `grep -c` sur le contenu. | Garder l'encart, alléger les reprises. |
| **m8** | « a + b + c = 1 dans la formule de révision » est énoncé comme une règle du marché, sans niveau de preuve à la ligne (le renvoi global au CPS est deux paragraphes plus bas). | mineur | Liste des six contrôles, S4e. Le contrôle `5.0` ne cherche que les balises `⟦V2`. | Accrocher le renvoi CPS à la ligne elle-même. |
| **m9** | Le contrôle de `check.mjs` annonce « chaque V3 de `data/` **lue par un module** est registrée » alors qu'il ne vérifie aucune lecture : il compare des nombres au registre. C'est ce libellé qui fait croire que M4 ne peut pas arriver. | mineur (outillage partagé, mais c'est D4 qui le met en défaut) | `build/check.mjs`, bloc `V3 de data/ contre registre` : `lues = feuilles.filter(f => !f.nonPubliee)` — aucune lecture n'est testée. | Renommer le contrôle, et implémenter celui que D1-B6 demandait. |

**Total : 32 défauts — 8 bloquants, 15 majeurs, 9 mineurs.**

### Ce qui n'a pas été retrouvé (vérification de non-régression)

Les trouvailles des passes D2 et D1 ont été recherchées une à une dans D4. **Deux sont
revenues** : le paramètre déclaré jamais relu (D1-B6 → M4) et le littéral de calendrier
en dur dans `calc/` (D2-M1 → M2). **Deux décisions prises à la suite de ces passes, et
qui nomment D4 explicitement, ne sont pas appliquées** : D-036 (B6) et D-037 (B7). Les
autres — fenêtre de consignation jetée, courbe en S sur la mauvaise assiette, délai
calendaire comparé à des jours ouvrés, légende contradictoire sur une période lue à l'œil
— **ne sont pas réapparues** ; la conversion ouvré/calendaire de D1 est correctement
réutilisée (§ 0.5).

---

## 4 · Grille d'auto-évaluation § 7.2

| Critère | Note | Justification |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | Trois états / deux écarts, l'un se pilote l'autre se vise : c'est une idée juste, neuve pour le lecteur et tenue de bout en bout. |
| Les hypothèses sont explicites | **1** | S4b est exemplaire sur les treize V3 de `data/`. Mais `derive_pct = 6`, la bande 0,95–1,05, le prorata des frais dans la VA et le mélange des deux modèles d'avancement planifié sont tous invisibles. **Sous le minimum.** |
| Les formules sont justifiées | **2** | VA, CPI, SPI, les trois EAC sont posées et commentées. La pondération en durée du « SPI de chemin » et le modèle de fiabilité du CPI ne sont jamais écrits. |
| L'exemple est vérifié | **1** | Sur cinq recalculs indépendants, deux s'écartent de plus de 16 % (SV, net visé), et les 39 vérifications n’en voient aucun — pour l'essentiel parce qu'ils réécrivent les définitions au lieu de refaire le modèle. **Sous le minimum.** |
| Le piège est identifié | **3** | S5 est le meilleur tableau d'erreurs du cours à ce jour, et chaque ligne porte son coût. |
| Le lien avec l'exécution est fait | **2** | Les six contrôles du visa, la double lecture, S4c. Manque le passage « points d'avancement → jours », qui est le geste de chantier réel. |
| Le lien avec le coût et le délai est fait | **3** | C'est le sujet, et il est tenu : situation, retenue, avance, pénalités, EAC, frais de durée. |

**Deux critères sous 2 : la grille § 7.2 n'est pas franchie.**

---

## 5 · Verdict

Le module tient une idée juste et la tient bien, mais il publie huit verdicts que ses
propres chiffres contredisent ou ne soutiennent pas — dont deux décisions validées,
D-036 et D-037, qui le nommaient — et son indice « du chemin critique », qui est sa
contribution annoncée, mesure une chaîne dont les tâches critiques n'ont pas commencé.

---

## Suite donnée (26/10/2026, par l'auteur)

**Les 8 bloquants sont corrigés** :

| # | Correction | Contrôle ajouté |
|---|---|---|
| B1 | La VP et la VA sortent du **même modèle d'avancement planifié** : `calc/etat.py` (nouveau) porte `avancement_planifie(segments, durees, j)`, et `courbe_de_depense` de D1 étale chaque poste sur ses **segments de travail**. Vérification indépendante : VP publiée 23 126 520 MAD contre 23 126 315 recalculée depuis la table d'état — **0,001 %**. | Test : la VP est bâtie sur les segments, comme la VA ; canari qui l'étale sur le span début→fin et vérifie que le nombre change |
| B2 | Le net visé est obtenu en **rejouant la situation** sur le constaté : mêmes formules, retenue de garantie et remboursement d'avance recalculés. Travaux retirés **1 273 080 MAD**, baisse du net **1 050 755 MAD** (4,15 %) — deux nombres différents, publiés tous les deux, avec la raison. | Test : la réduction du net est **plus faible** que les travaux retirés ; canari qui fait la soustraction brute et montre que c'est la faute symétrique du contrôle n° 4 |
| B3 | La section disparaît : les deux indices pointaient dans le même sens, et la contribution annoncée du module était fausse. S3c et S4c sont réécrites autour de ce qui répond vraiment — la **marge totale restante**, tâche par tâche. | — |
| B4 | « En avance de 11,98 points » retiré des trois endroits où il figurait. L'écart physique/temporel compare une part de **budget** à une part de **délai** : il ne conclut rien. L'avance-retard se mesure au constaté contre le planifié de la même date : **−3,42 points, un retard**. | Test de l'identité, et **canari de signe** : l'écart au temporel conclurait l'inverse du vrai avance-retard (+11,98 contre −3,42) |
| B5 | `spi_du_chemin_critique` est supprimé et remplacé par `ce_qui_porte_la_date`. À cette date **aucune** des 6 tâches à marge nulle n'a commencé : un indice sur elles est un 0/0, et le module le **publie comme résultat** au lieu de publier un nombre. Ce qui reste est la marge : CHFA, 10,8 j de retard sur 17,47 de marge totale, **6,67 j restants**, marge libre déjà épuisée. | Tests : les tâches à marge nulle sont celles que D2 publie ; aucune n'a démarré et le module le dit ; « menace la date » si et seulement si le retard dépasse la marge totale |
| B6 | D-036 appliquée : le coût réel est une V3 entre 20 et 27 MMAD, donc le CPI va de **0,82 à 1,13** et **le diagnostic change de signe**. Publié avec les EAC correspondantes. | Test : les indices sont publiés avec leurs bornes, et le module dit si le diagnostic change de signe |
| B7 | La bande de conformité est déclarée dans `data/` (`bande_de_conformite_des_indices`, `_nature: decision`) avec la note qui dit qu'elle ne vaut **que pour des indices définis sur leur base** (D-037). | Le build échoue sur toute option de figure non déclarée ; la bande est injectée, plus écrite en dur |
| B8 | Les frais de durée (1,37 MMAD, répartis au prorata du temps) sortent de la VA, du BAC et du CR : le CPI porte sur les **ouvrages**, la seule chose dont l'avancement a été constaté. CPI 0,96 → **0,9551** sur une assiette propre, et les frais sont publiés à part. | Test : les frais sont exclus du périmètre ; canari qui les réintègre au prorata et montre le CPI remonter |

**Majeurs et mineurs** : traités avec les bloquants pour ceux que la réécriture de S3c, S4c, de
l'exercice 2, du quiz Q4 et de la fiche mémo emportait ; les autres sont portés en dette déclarée
dans `STATE.md`.

**Ce que cette passe a prouvé.** B5 est le défaut le plus instructif du projet à ce stade : la
**contribution annoncée** du module était un indice qui portait un nom qu'il ne méritait pas. Le
calcul était juste ; l'objet mesuré ne l'était pas. Et le module s'est corrigé en publiant une
absence — « aucun indice n'est défini ici » — ce qui est un meilleur enseignement que le nombre qu'il
publiait avant. B4 ajoute la contre-épreuve : le module qui dénonce la comparaison de pourcentages à
dénominateurs différents en faisait une, trois fois, dans ses propres corrigés.

