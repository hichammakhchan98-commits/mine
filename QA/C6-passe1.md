# Passe adversariale /devil — C6 (matériel)

Relecteur : sous-agent indépendant, qui n'a pas lu le raisonnement de l'auteur avant de recalculer ·
30/10/2026 · commit relu : **`721321c`** (ex-`b205074`, amendé, contenu identique — vérifié par `cmp`
sur les six fichiers suivis).

Les artefacts générés (`calc/sorties/*.json`, `modules/14-c6-materiel.html`, `tests/captures/`) ont
été copiés avant toute relecture dans le répertoire de travail du relecteur, et c'est cette copie qui
est relue. Mes scripts vivent hors du dépôt ; aucun fichier du cours n'a été modifié, à l'exception
du présent rapport.

---

## 0. Contre-expertise à l'aveugle (§ 12.2)

Cinq familles de valeurs recalculées **depuis `data/projet-gare.json` et les sorties des AUTRES
modules seulement** (`planification.json`, `prix.json`, `gros-oeuvre.json`), par des scripts écrits
pour cette passe, avant d'ouvrir `calc/cout_horaire.py`.

| Valeur recalculée | Ma voie | Mon résultat | Le module publie | Écart | Verdict |
|---|---|---|---|---|---|
| **1a.** Possession / location annuelles — pompe | parts fixes reconstruites à la main depuis les 8 V3, `v = carb × gasoil + conducteur` | 1 045 405 / 56 204 MAD/an, écart **+989 201** | 1 045 405 / 56 204 / +989 201 | 0 | **confirmé** |
| **1b.** idem — pelle | idem | 1 018 196 / 561 780, écart **+456 416** | identiques | 0 | **confirmé** |
| **1c.** idem — chariot | idem, location = 250 j × 1 450 + conducteur × h | 266 709 / 386 333, écart **−119 624** | identiques | 0 | **confirmé dans le modèle publié** — mais le modèle est faux (B1) |
| **2.** Seuils et leur sens | **balayage numérique** pas de 0,25 h puis dichotomie, sur deux fonctions de coût que j'ai écrites moi-même, sans la formule affine du module | pompe **943,2** (possession au-dessus) · pelle **3 560,9** (au-dessus) · chariot **1 883,2** (**au-dessous**) | 943,2 / 3 560,9 / 1 883,2, mêmes sens | 0 | **confirmé** (le sens inversé du chariot est exact *dans le modèle publié*) |
| **3a.** Jours de travail et fenêtres | somme des segments de `segments_de_travail` | pompe 139,83 j / [19,86 ; 300,09] · pelle 35,51 / [5,25 ; 50,45] · chariot 251,94 / [19,86 ; 574,84] | identiques | 0 | **confirmé** |
| **3b.** Les mêmes, **union** des segments (un engin ne travaille qu'une fois par jour) | union des intervalles | pompe **104,42** · pelle **30,80** · chariot **200,86** | le module publie la somme | **+34 %** sur la pompe, **+25 %** sur le chariot | **défaut B2** |
| **4.** Interventions et volume pompé | 3 postes du bordereau de D1 portant `pompe_a_beton_j` : 800 m² × 0,0016 + 800 × 0,0012 + 2 880 × 0,00114 = **5,523 j** ; ÷ 0,004 j/m³ = **1 380,8 m³** ; ÷ 98,4 = 14,03 → **15** interventions ; × 3,08 h = **46,2 h** | 5,52 j · 1 380,8 m³ · 15 · 46,2 h | identiques | 0 | **confirmé** (réserve m13 sur l'arrondi, M3 sur le périmètre) |
| **5.** Disponibilité de la chaîne | **ma propre simulation**, 2 000 000 de matinées, graine 424242 | **75,43 %** (produit 75,390 %), écart 0,043 pt ; maillon faible 88,0 % ; **1,97** coulage dérangé sur 8 | 75,4 % / 75,4 % / 12,6 pts / 2,0 sur 8 | 0 | **confirmé** — mais le contrôle ne contrôle rien (M7) |
| **6.** (en supplément) Part des tirages pro-possession | **mon propre Monte-Carlo**, 200 000 tirages uniformes, graine 7 | pompe **0,0 %** · pelle **0,0 %** · chariot **85,7 %** | 0,0 / 0,1 / 85,7 | ≤ 0,1 pt | **confirmé** |
| **7.** (en supplément) Profils du parc jour par jour | mon propre balayage des 601 jours | présence 881, travail **346**, pointe 3, 19 jours à trois engins, plages [19-24] et [38-50], trous du chariot [137-299] et [331-454] | 884 / 346 / 3 / 19 / mêmes plages et trous | 3 j sur la présence (convention de bord) | **confirmé** |

**L'arithmétique du module est juste partout où je l'ai reprise.** Les défauts qui suivent ne sont
pas des fautes de calcul : ce sont une **erreur de modèle** (B1), un **double comptage de
définition** (B2) et des **phrases fausses à côté de nombres justes** (B3, B4) — exactement les trois
familles que `STATE.md` désigne comme les plus coûteuses de ce cours.

---

## 1. Unités et homogénéité dimensionnelle

**Constat : conforme sur les formules publiées, un défaut d'unité sur le tableau des secours.**

Preuve, formule par formule : `poss(h) = F + v·h` → MAD/an + (MAD/h)(h/an) = MAD/an ✓ ·
`loc(h) = L₀ + L₁·h` idem ✓ · `h₀ = (L₀ − F)/(v − L₁)` → (MAD/an)/(MAD/h) = **h/an** ✓ ·
`F/h + v` → MAD/h ✓ · `D = Π pᵢ` sans dimension ✓ · `1 − (1 − p)²` sans dimension ✓ ·
plafond = (j/an)(h/j) = h/an ✓ · `L₁` de la pompe = (MAD/intervention)/(h/intervention) = MAD/h ✓.

**Défaut M8.** `esperance_de_gain_MAD_j = gain × 16 240,33` : `gain` est une probabilité **par
coulage**, `16 240,33` est le coût **d'un jour ouvré** de frais de durée. Le produit est donc des
**MAD par coulage**, et il est comparé dans le même tableau à un coût en **MAD par jour**
(1 800 MAD/j d'immobilisation, 120 MAD/j de vibreur), sous un en-tête « MAD/j » et une colonne
« MAD / point » qui n'a pas de dimension temporelle du tout. L'égalité « un coulage = un jour de
secours payé » n'est écrite nulle part. Elle est probablement vraie ici (on n'immobilise la seconde
pompe que les jours de coulage), et c'est précisément pour cela qu'il fallait l'écrire : c'est le
sujet du module.

---

## 2. Référentiels mélangés (phase § 5.0)

**RAS, et c'est prouvé.** `grep -o "⟦V[0-9]"` sur `content/14-c6-materiel.md` donne **33 balises,
toutes V3**, aucune V0/V1/V2. `grep -niE "BAEL|BPEL|RPS|eurocode|EN 1[09][0-9]|NF |DTU|fascicule|article [0-9]|NM "`
ne ramène que trois faux positifs (« et d'aucune norme », « c'est la norme sur un chantier »,
« la réglementation applicable », cette dernière dans un renvoi ⏸). Aucun dimensionnement, aucune
vérification réglementaire, aucun coefficient normatif. Le S1, le § S4f-3, le § S4g et la fiche mémo
nomment explicitement ce qui reste ⏸ (vérifications périodiques, habilitations, consignes,
distances et survol). Le bandeau `meta` et le `pied` portent l'avertissement du § 3.4.

---

## 3. Article ou chiffre normatif cité sans V0 ni V1

**RAS, prouvé.** Les 33 balises sont bien formées (7 champs chacune : niveau, énoncé, valeur, unité,
fourchette, année, justification — vérifié par script), toutes avec **fourchette et année 2026**, et
les 33 valeurs déclarées correspondent **au bit près** à `data/projet-gare.json`
(gasoil 11,5 · conducteur 60 · résiduelle 20 % · capital 7,0 % · pompe 4 200 000 / 7 / 9 % / 18 ·
pelle 2 600 000 / 8 / 11 % / 24 / 5,5 / 85 % · chariot 950 000 / 8 / 8 % / 7 / 3,5 / 92 % ·
rendement 90 / 0,80 / 0,70 / 0,85 · 1 450 · chaîne 96/92/88/97 · secours 1 800 · 12 % · 0,8 ·
250 j). `git show 721321c:data/registre-hypotheses.csv | grep -c C6` = **33** : toutes registrées.

**Réserve M5** (voir plus bas) : la phrase qui introduit la liste est fausse, mais aucune valeur n'est
non déclarée.

---

## 4. Ordres de grandeur et ratios

**Constat : les 33 hypothèses sont plausibles ; deux lectures sortent de leur domaine.**

Plausibilité (contrôle d'ordre de grandeur, V3 contre V3, je ne dispose d'aucun bordereau V0) :
pompe automotrice 32 m à 4,2 MMAD ≈ 390 k€, pelle 30 t à 2,6 MMAD ≈ 240 k€, chariot 4 t/17 m à
950 kMAD ≈ 88 k€ — cohérents entre eux et avec le marché 2026 ; entretien 8 à 11 % du prix d'achat
par an, consommations 7 / 18 / 24 l/h pour 4 t / pompe / 30 t, amortissements 7 à 8 ans,
disponibilités 85 à 92 % : rien d'aberrant, rien hors de sa fourchette. Le rapport
possession/location de la pelle (942 contre 520 MAD/h) raconte une histoire vraie de loueur.

**Défaut M3 — un ratio lu hors de son domaine.** Le chiffre phare du S2 — « la pompe, employée
**41,2 h/an**, coûterait **25 364 MAD l'heure** » — divise des heures déduites de **3 postes** par
une fenêtre déduite de **9 tâches**. Le volume pompé (1 380,8 m³) vient des trois seuls postes du
bordereau de D1 qui portent une ligne de pompe (radier technique, plancher haut technique,
mezzanine) ; la fenêtre (jour 19,9 → 300,1, soit 1,121 an) vient des neuf tâches déclarées dans
`materiel_engins.familles[0].taches`, dont FOND, VOIL, POTR, NOYX, MARQ et PSOU, **qu'aucun
sous-détail de D1 ne pompe** (les voiles du niveau technique et les semelles n'ont pas de ligne
`pompe_a_beton_j`). Sur le périmètre cohérent — les trois postes pompés — la fenêtre est
**25,4 → 77,7 = 52,3 j**, l'emploi **220,9 h/an** et le coût de possession **4 949 MAD/h**. Le
chiffre publié est **5,1 fois** celui-là. Verdict inchangé (LOUER dans les deux cas), nombre phare
faux d'un facteur 5.

**RAS prouvé sur l'étendue des tirages.** J'avais soupçonné que les fourchettes des prix de
location de D1 (pompe 3 000–6 000, pelle 400–700) n'entraient ni dans les 20 000 tirages ni dans
les deux coins. Vérification faite dans `_objets_tirables` et `parametres` : `prix_loc` **est**
tiré pour les trois engins et **est** porté à sa borne aux deux coins ; l'écart 9 contre 10
paramètres tirés tient au seul `heures_par_jour_servi`, que la pompe n'a pas puisque son emploi
est déduit. La phrase « aucune combinaison de ces fourchettes ne peut inverser ce résultat »
porte donc bien sur le prix de location, et elle est exacte.

**Défaut M10 — une affirmation non démontrée.** « Un rapport de **2,62** entre la pompe et la pelle,
et **il ne vient d'aucune différence de prix de marché** : il vient de l'unité. » Les deux engins ne
sont pas le même engin : 4,2 MMAD contre 2,6 MMAD de prix d'achat, soit déjà **1,62**. Le module
démontre l'effet de l'unité pour le **chariot** (1 450 MAD/j ÷ 3,5 h = 414 MAD/h s'il n'était payé
que ses jours de travail, contre 973 payé à la fenêtre : facteur 2,35, même engin, même prix) et
c'est une vraie démonstration ; il ne la fait nulle part pour la paire pompe/pelle, dont le rapport
mélange trois variables à la fois.

---

## 5. Cohérence data / figures / tableaux / autres modules

### 5.1 Avec les autres modules — bonne, sauf sur le périmètre de la pompe

- **D2** : les 27 tâches de `segments_de_travail` sont lues telles quelles, mes sommes et mes
  fenêtres les retrouvent exactement (§ 0, ligne 3a). Aucune durée redéclarée.
- **D1** : prix 4 200 MAD/j et 520 MAD/h lus dans `prix_unitaires_MAD.ressources.materiel_MAD`,
  jamais redéclarés ✓ ; frais de durée 16 240,33 MAD/j ouvré = `cout_du_retard["1"]` ✓ ;
  « énergie et divers » 534 600 MAD = 18 000 × 29,7 mois ✓ ; absence de tout prix de chariot
  télescopique au bordereau **vérifiée** (`grep -i telesco calc/sorties/prix.json` → 0) ✓ ;
  l'écart de 2,72 sur les jours de pompe est publié **et expliqué** ✓.
- **C3** : 98,4 m³ de zone, 3,08 h de coulage, 32,0 m³/h tenus, 18,9 m³/h de plancher anti-reprise,
  8 zones, « borné par la rotation des toupies » — tous repris de `gros-oeuvre.json`, et 3,08 h est
  bien l'`option_retenue` à 5 toupies, pas une variante ✓.
- **C1** : la grue est explicitement laissée à C1 ✓. **Mais** (défaut M4) la figure 2 s'intitule
  « Engins **présents sur le site** » et publie « pointe de présence **3 engins** » alors que C1 pose
  **deux grues à tour** présentes 5,8 mois : la pointe réelle du parc est 5. Le titre et l'« erreur
  courante » (« dimensionner un parc sur la pointe de présence ») prétendent à un périmètre que la
  figure n'a pas.
- **D7** : `besoin_relatif_du_second_site = 0,8` est déclaré V3 avec renvoi explicite à la dette 34 ✓.

### 5.2 Défaut B2 — deux nombres publiés pour une même grandeur (double comptage)

`jours_de_travail_j` est la **somme des segments** des tâches servies. Or ces tâches se recouvrent :
mon balayage montre que le chariot sert **2 tâches simultanées 44 jours et 3 tâches 7 jours**, la
pompe 2 tâches 22 jours et 3 tâches 10 jours. Un engin ne travaille qu'une fois par jour.

| Grandeur | Publié (somme) | Vrai (union) | Écart |
|---|---:|---:|---:|
| Chariot, jours de travail | 251,94 j | **200,86 j** | +25 % |
| Chariot, heures de travail | 881,8 h | **703,0 h** | +25 % (soit **10,5 h de manutention en un jour** les 7 jours à trois tâches, pour un engin déclaré à 3,5 h/j) |
| Chariot, emploi annuel | 397,2 h/an | **316,7 h/an** | −20 % |
| Chariot, taux de présence utile | 45,4 % | **36,2 %** | −9 pts |
| Pompe, jours de travail | 139,83 j | **104,42 j** | +34 % |
| Pelle, taux de présence utile | 78,6 % | **68,1 %** | −10 pts |

Et le module **publie les deux définitions sans le voir** :

- S3 : « on paie ses **303 jours** d'attente » et S5 n° 5 : « la différence, **303 jours**, se paie
  plein tarif » (555 − 252) ;
- figure 2 : « il totalise **350 jours** sans emploi dans sa fenêtre » (`parc.familles[2]`, calculé
  jour par jour, donc à l'union) — **mon balayage confirme 350, pas 303** ;
- glossaire : « **Taux de présence utile** : jours de travail / jours de fenêtre. **39 %** pour ce
  parc ». 39,1 % est `346/884`, calculé à l'**union** ; la définition du glossaire appliquée aux
  nombres du module donne `427,28/884 = `**48,3 %**. Le nombre et sa définition ne se parlent pas.

L'écart n'inverse aucun verdict (la possession du chariot gagne davantage à 317 h/an : écart
−126 106 au lieu de −119 624) mais il fausse six nombres publiés, dont trois en gras, et il met deux
chiffres contradictoires à six paragraphes d'écart. La note de `data/` dit d'ailleurs ce qu'il
fallait compter : « heures de travail effectif **par jour ouvré des tâches servies** » — des jours,
pas des jour-tâches.

### 5.3 Dans la figure 1 — le plafond et l'emploi réel ne sont pas dessinés (M1)

`materiel.figures.equilibre_chariot` transporte `plafond = 875` et `emploi_reel = 397,2`. La capture
`tests/captures/14-c6-materiel.html-figure1.png` ne contient que **dix textes** (vérifié dans le
SVG) : les deux extrémités, cinq graduations, le titre d'axe, la légende et le seul marqueur
« seuil 1 883 h/an ». Le « Ce qu'il faut voir » demande pourtant de lire sur la figure que « toute la
partie droite, **au-delà de ce plafond**, est hors d'atteinte » et que « l'emploi réel est très à
gauche du croisement ». Les deux séries existent dans les données, le générateur les ignore en
silence : c'est la dette 33 (« un format ignoré en silence est un défaut ») sur deux options de
figure, et la dette 11/13 (« rien ne vérifie qu'une figure montre ce qu'elle prétend montrer »).

### 5.4 Défaut M2 — « sites équivalents » n'est pas un nombre de sites

Le module calcule `sites_equivalents = seuil / heures_par_an_seul` (un simple rapport d'heures) puis
le publie sous la définition « **nombre de sites qu'il faudrait regrouper** pour que la possession
devienne avantageuse », et la `lecture` écrit « il faudrait **22,9 sites** pour pompe et **3,3
sites** pour pelle ». Or le module définit lui-même, deux lignes plus haut, le facteur de
mutualisation : `(1 + (n−1)·0,8) × 0,88` — c'est ce facteur qui donne « deux sites font 1,58 site
équivalent ». En l'inversant :

| Engin | Équivalents publiés | **Sites réels** correspondants |
|---|---:|---:|
| Pompe | 22,89 | **32,3** |
| Pelle | 3,30 | **4,4** |
| Chariot | 4,74 | **6,5** |

Le nombre est juste, sa définition publiée est fausse, et l'écart va de 33 à 41 %. La fiche mémo
reprend « Sites équivalents pour posséder la pompe : **22,9** ».

### 5.5 Deux modules qui calculent deux fois la même grandeur

Aucun — vérifié : la grue est laissée à C1 (et un test l'épingle), le parc de coffrage à C3, les
cadences de bétonnage à C3, la demande de grue jour par jour à D2. Le seul doublon assumé (jours de
pompe, D1 contre C6) est publié avec son facteur 2,72 et son explication.

---

## 6. Grille de profondeur (§ 7.2)

| Critère | Note /3 | Preuve |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | S2 construit les deux droites avant toute valeur, et l'encart « le seuil ne suffit pas : il faut son SENS » explique *physiquement* pourquoi un engin peu employé payé à la présence se possède |
| Les hypothèses sont explicites | **2** | 33 balises avec fourchette et année, toutes registrées — mais « il n'y en a pas d'autres » est faux (M5), le carburant du locataire n'est déclaré nulle part (B1) et l'indépendance des maillons non plus (M7) |
| Les formules sont justifiées | **2** | la forme affine est démontrée et son renversement de sens discuté ; mais `L₁` du chariot est faux (B1) et le quiz nie une dépendance que le modèle contient (B3) |
| L'exemple est vérifié | **2** | trois voies (nominal, deux coins, 20 000 tirages), étalonnage par balayage, 177 contrôles, 7 canaris — tous reproduits par moi ; mais une des deux « voies indépendantes » est vide (M7) et l'autre est déclarée vide par le module lui-même |
| Le piège est identifié | **3** | dix erreurs fréquentes, dont les deux que le module a lui-même commises, chiffrées et reliées à un canari |
| Le lien avec l'exécution est fait | **2** | double lecture entreprise/MOE avec trois contrôles sur pièces, § sécurité par engin, renvois ⏸ nets ; pas de séquence ni de cadence propre, ce qui est assumé |
| Le lien avec le coût et le délai est fait | **3** | coût du parc, ligne absente du bordereau (160 % du poste), coût d'un jour perdu, fenêtres lues dans le planning, exercice 3 sur un report de six mois |

**Minimum 2 partout : atteint.** La grille passe ; la livraison est refusée sur les bloquants.

---

## 7. Sécurité

**Constat : conforme, et c'est un des bons points du module.** Le § S4g ouvre par « **aucun de ses
résultats n'autorise un choix de matériel** » et rappelle l'ordre de priorité du § 2.1 ; les trois
mécanismes d'accident sont nommés par engin (éclatement de tuyauterie et fouettement, contact de
flèche avec une ligne électrique, calage et portance sous stabilisateurs ; renversement du chariot
par charge hors abaque ou sol qui cède ; zone de rotation, effondrement de fouille, angle mort
arrière) ; « le transport de personnes sur les fourches, qui n'est jamais une option » est écrit sans
nuance, ce qui est la bonne façon de l'écrire. Les périodicités, habilitations et critères
d'acceptation sont **refusés** explicitement (⏸) plutôt qu'inventés — conforme au § 5.0 et à R8.

**Aucun conseil dangereux trouvé.** Une omission mineure, non bloquante : la décision « posséder »
publiée pour le chariot n'est accompagnée d'aucun mot sur ce qu'acheter un engin engage côté
réception, conformité et maintenance — le module dit « ne dispense d'aucune des vérifications de
l'engin qu'on achète », ce qui suffit à ne pas être faux.

---

## 8. Vérité du rendu

Captures examinées : `14-c6-materiel.html-figure1/2/3.png`. Trois figures rendues, non vides, trois
séries de données vérifiées contre mon propre recalcul (profils du parc : identiques à 2 jours de
bord près ; cascade de rendement : 90 → 72 → 50,4 → 42,8 reproduit ; droite d'écart : −147,6 kMAD à
50 h et +37,6 kMAD à 2 350 h, je retrouve −147 575 et +37 575).

Défauts :

- **M1** (ci-dessus) : figure 1, deux séries annoncées par la légende et absentes du dessin.
- **m8** : figure 1, la graduation « **1500** » est traversée par la courbe — chevauchement
  texte/trait, celui que la dette 11 dit non détecté par les tests.
- **m2** : figure 3, les quatre libellés sont **sans accents** — « Debit catalogue », « Beton reel,
  tuyauterie », « Heure reellement pompee », « Nettoyages et arrets » — dans un module où tout le
  reste est accentué. Ils viennent tels quels de `rendement_de_la_pompe.etapes[].etape`.
- **m1** : « Au nominal, la possession économise **-120 000 MAD** par an » (S4a) et « d'où les
  **-120 000 MAD/an** d'écart en faveur de la possession » (figure 1) : un signe négatif dans une
  phrase qui annonce une économie. Le signe est une convention interne (`ecart = possession −
  location`) qui n'a pas à sortir dans la prose.
- **m5** : le sommaire latéral affiche « L'emploi de la pompe est entièrement `**déduit**` » —
  les astérisques du gras ne sont pas interprétés dans l'ancre de navigation.
- **m7** : « Les deux qui ne se doublent pas du tout sont la **centrale** (96 %) et la **rotation des
  toupies** (92 %) : *Une toupie de plus ne couvre pas une rotation interrompue…* » — la variable
  injectée n'apporte que la raison **des toupies** ; celle de la centrale manque, et la phrase
  redémarre par une majuscule au milieu d'une proposition.
- **m6** : « Deux sites font 1,58 site équivalent, pertes de transfert déduites […] **Deux sites font
  1,58 site équivalent, pertes de transfert déduites**, et cela ne fait basculer aucun verdict » — la
  prose et la variable `lecture` disent la même phrase deux fois de suite. Même défaut dans l'encart
  « Le résultat contre-intuitif » : « chaque heure de plus coûte du carburant et un conducteur à
  celui qui le possède » y figure deux fois à trois lignes d'écart.
- **m3** : exercice 3, « 555 × 1 450 = **804 721** » — le produit des deux nombres affichés vaut
  804 750 ; le calcul exact utilise 554,98 j. Un lecteur qui vérifie trouve un écart.
- **m4** : exercice 1, « la possession gagne encore, mais de **deux fois moins** qu'avant » pour
  47 125 contre 119 624, soit **2,54 fois**.
- **m9** : la check-list source porte deux points numérotés « 8 » (le rendu les renumérote, le défaut
  reste dans `content/`).

Aucune erreur console constatable ici (je n'ai pas relancé `npm run check`, conformément à la
consigne) ; les trois captures existent, datées du build, et les trois figures sont non vides.

---

## 9. Simplifications non signalées

- **B1 (bloquant, ci-dessous)** : le locataire du chariot ne paie pas le gasoil. Non déclaré.
- **M7** : l'**indépendance** des quatre maillons de la chaîne. Un orage, un jour férié, un blocage
  d'accès frappent la centrale *et* la rotation ensemble ; le produit suppose le contraire, et la
  « simulation directe » le suppose aussi. Nulle part écrit.
- **M6** : deux disponibilités (pelle 85 %, chariot 92 %) sont déclarées, commentées en prose (« la
  plus basse des trois », « la meilleure des trois, et c'est pourquoi tout le chantier finit par en
  dépendre ») et **ne sont lues par aucun calcul**. Preuve : j'ai copié le dépôt dans mon répertoire
  de travail, mis les deux valeurs à **5 %**, relancé `calc/cout_horaire.py` — la sortie
  `materiel.json` est **identique au caractère près**. C'est la famille « un paramètre déclaré que
  rien ne lit » de `STATE.md`, et la fiche d'Étape 0 promettait « immobilisation et pannes ».
- **m12** : `interventions = ⌈1 380,8 / 98,4⌉ = ⌈14,03⌉ = 15`, soit **+6,9 %** de location et
  d'heures pour trois centièmes de zone. L'arrondi n'est pas commenté.
- **m13** : le « volume d'un coulage » (98,4 m³, zone de mezzanine) est appliqué aussi au radier du
  niveau technique (320 m³) et au plancher haut (240 m³), qui ne se coulent pas en zones de 360 m².
- **m14** : pour la pelle, `unites_facturees = heures_de_travail` (195,3 = 195,3) : les **heures de
  compteur** sont assimilées aux heures de travail. Dans un module dont la thèse est que l'unité
  facturée diffère du travail, c'est l'hypothèse qu'il fallait déclarer.
- **m11** : `unites_facturees_par_an = 250,0` pour le chariot est **vrai par construction**
  (`fenêtre ÷ (fenêtre/250)`), et l'exercice 3 le présente comme un constat (« le nombre de jours de
  présence par an **reste** 250 ») au cœur de son « piège ».
- **m15** : « un coulage dérangé = un jour entier de frais de durée du chantier » n'est pas déclaré
  (seul le *périmètre* — frais de durée sans pénalités — l'est). J'ai vérifié que l'hypothèse n'est
  pas déterminante : même à un demi-jour, l'aiguille reste rentable (184 > 120) et la pompe ne l'est
  pas. MEZZ est bien sur le chemin critique de D2, ce qui valide le principe.

**Bien déclarées, et à porter au crédit du module** : l'absence de montée de l'entretien avec l'âge
(S5 n° 10), le périmètre du jour perdu, la limite des forfaits de D1 (`_limite`), la limite de la
cascade de rendement (« trois nombres peuvent se compenser »), et surtout l'encart « Un contrôle qui
ne contrôle rien » sur les deux voies des jours de travail — qui montre que l'auteur sait reconnaître
ce défaut quand il le voit (ce qui rend M7 d'autant plus gênant).

---

## 10. Texte télégraphique ou remplissage

**RAS sur le télégraphique** : le module est écrit en phrases, chaque paragraphe porte une règle, un
nombre ou une méthode, et la densité est celle d'une fiche d'expert [M] — conforme à R5 et R7.

**Remplissage, deux occurrences, traitées en m6** : une phrase répétée mot pour mot dans la
mutualisation, une autre répétée dans l'encart qui suit. Les deux viennent de la juxtaposition d'une
prose rédigée et d'une variable `lecture` / `_hypothese_de_fenetre` qui dit déjà la même chose.

---

## Tableau des défauts

| # | Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|---|
| **B1** | **Le locataire du chariot ne paie pas son gasoil.** La location est déclarée « **nue**, opérateur non compris » ; `couts_annuels` ajoute bien le conducteur au locataire (`location += heures × conducteur`) mais **jamais le carburant**, qui n'est compté qu'au propriétaire (`variable_h = carburant × gasoil + conducteur`). Une location nue se loue sans carburant : le locataire le paie. | **bloquant** | `L₁ = 60` alors que `v = 140,5` : la pente publiée, **+80,5 MAD/h**, est **exactement** le poste carburant (7 l/h × 11,5). Avec le gasoil des deux côtés : pente = **0**, **aucun seuil**, écart **constant à −151 600 MAD/an** (au lieu de −119 624), et mon Monte-Carlo de 200 000 tirages donne **93,3 %** de tirages pro-possession au lieu de 85,7 % — au-dessus du seuil de verdict de 90 % déclaré par le module, donc **le verdict publié passe de « NON TRANCHÉ » à « POSSÉDER »**. Tombent avec la pente : la figure 1 entière, le seuil 1 883 h/an, la comparaison seuil/plafond, l'exercice 1 (seuil 982,6 et « marge tombée à 12 % »), le « piège » de l'exercice 3, et l'encart « mutualiser un engin payé à la présence affaiblit la possession » (avec le gasoil des deux côtés, mutualiser est **exactement neutre**). | Ajouter `carburant_compris` au bloc `location` de `data/`, pour les trois familles, et le lire dans `_L0_L1` comme `operateur_compris` l'est. Si le choix est que le prix de 1 450 MAD/j comprend le gasoil — ce qui n'est pas ce que « nue » veut dire —, il faut l'écrire dans la note de `data/`, dans la balise V3 et dans le S4a, parce que c'est l'hypothèse dont dépend le résultat phare du module. Republier la figure 1, les deux exercices, la mutualisation et le verdict. |
| **B2** | **Les jours de travail comptent deux fois les tâches qui se recouvrent**, et le module publie **deux nombres** pour la même grandeur. | **bloquant** | Mon balayage : chariot = 2 tâches simultanées 44 jours, 3 tâches 7 jours ⇒ somme 251,94 j contre **union 200,86 j** ; pompe 139,83 contre **104,42**. Conséquences publiées : « **303 jours** d'attente » (S3 et S5 n° 5) contre « **350 jours** sans emploi » (figure 2, calculée à l'union — mon balayage confirme 350) ; taux de présence utile 45,4 % contre 36,2 % ; 881,8 h de manutention, soit **10,5 h en un jour** pour un engin déclaré à 3,5 h/j ; et le glossaire publie « jours de travail / jours de fenêtre = **39 %** » alors que sa propre définition appliquée aux nombres du module donne **48,3 %** (39,1 % est le ratio à l'union). | Compter les jours de travail comme **union** des segments (`parc` le fait déjà : les deux définitions coexistent dans le même fichier de sortie). Recalculer heures, emploi annuel, taux de présence utile, jours d'attente, puis réécrire les trois nombres de S3, S5 n° 5, de l'exercice 3 et du glossaire. Un test : « pour chaque famille, jours de travail = jours où le profil de travail vaut 1 ». |
| **B3** | **Le quiz et le glossaire nient une dépendance que le modèle contient.** Quiz 1 : « Un engin gardé huit ans […] **Non, c'est le même rapport**. Le seuil est un nombre d'heures par an : **la durée de détention n'y figure pas**. » Glossaire : le coût horaire de possession « décroît avec l'emploi, **jamais avec la durée de détention** ». | **bloquant** | `amortissement_ans` **est** une durée de détention, et `F = prix(1−vr)/n + entretien + capital`. À l'hypothèse du quiz (300 h/an), l'amortissement par heure vaut `prix(1−vr)/(n·h)` : pour le chariot à 300 h/an, **1 267 MAD/h si on le garde 2 ans contre 317 MAD/h si on le garde 8 ans**, soit un rapport **4**. Le seuil lui-même en dépend : avec n = 2 au lieu de 8, F passe de 210 900 à **495 900** MAD/an et le seuil du chariot de 1 883 à **−1 657** h/an, c'est-à-dire que la possession ne gagne plus à aucun emploi. Le module se contredit lui-même six lignes plus haut, en S5 n° 10 : « Croire qu'un amortissement long améliore l'affaire. **Il baisse la charge annuelle** ». | Réécrire la réponse 1 : *oui*, huit ans amortissent quatre fois mieux que deux, et c'est pourquoi `amortissement_ans` est une des 33 hypothèses ; ce qui ne dépend pas de la détention, c'est l'**unité** du seuil (des h/an, pas des années), pas sa valeur. Corriger la ligne du glossaire et la première « phrase du module » de la fiche mémo en conséquence. |
| **B4** | **Figure 2, « Ce qu'il faut voir » : « Hors de ces deux plages, il y a *toujours* au moins un engin payé qui ne fait rien. »** | **bloquant** | Faux **188 jours sur 601**. Compté sur les séries publiées (`figures.parc_presents` et `figures.parc_travail`) : 207 jours où **tout engin présent travaille**, dont **188 hors des deux plages citées** — jours 6 à 18 (seule la pelle est là, et elle travaille), 51 à 77 (pompe et chariot présents, tous deux sur MEZZ), et 148 autres. La figure elle-même le montre : le contour rouge épouse les barres bleues sur ces plages. | Remplacer par le nombre : « sur **363** des 601 jours du profil, au moins un engin présent ne travaille pas ; sur 207, tous ceux qui sont là travaillent », ou supprimer l'affirmation. Et publier le nombre, pas l'adverbe. |
| **M1** | Figure 1 : la légende fait lire un **plafond** et un **emploi réel** que la figure ne dessine pas. | majeur | `figures.equilibre_chariot` porte `plafond = 875` et `emploi_reel = 397,2` ; le SVG rendu ne contient que 10 textes et un seul marqueur (le seuil). Capture `…figure1.png`. | Dessiner les deux repères (bande grisée au-delà de 875, point à 397) ou retirer les deux lignes du « Ce qu'il faut voir ». Dette 33 : une option de figure ignorée en silence est un défaut. |
| **M2** | « **Sites équivalents** » publié comme « nombre de sites qu'il faudrait regrouper ». | majeur | `sites_equivalents = seuil / heures_seul`, sans le facteur `(1+(n−1)·0,8)·0,88` que la même section utilise pour écrire « deux sites font 1,58 site équivalent ». En l'inversant : 22,89 éq. = **32,3 sites**, 3,30 = **4,4**, 4,74 = **6,5**. La `lecture` écrit « il faudrait **22,9 sites** pour pompe et **3,3 sites** pour pelle ». | Soit publier le nombre de sites (inversion du facteur), soit renommer la colonne et la définition en « **sites équivalents** », et corriger la `lecture` et la fiche mémo. |
| **M3** | L'emploi de la pompe divise des heures déduites de **3 postes** par une fenêtre déduite de **9 tâches**. | majeur | Volume 1 380,8 m³ = radier technique + PH technique + mezzanine, les trois seuls postes de D1 portant `pompe_a_beton_j` ; les voiles et les semelles, servis par la pompe dans `data/`, n'ont aucune ligne de pompe chez D1. Sur le périmètre des 3 postes : fenêtre 25,4 → 77,7 = **52,3 j**, emploi **220,9 h/an**, possession **4 949 MAD/h** contre les **25 364 MAD/h** publiés en S2 comme « le chiffre le plus brutal de la fiche » — facteur **5,1**. | Aligner les deux périmètres : soit restreindre `taches` aux postes que D1 pompe, soit compléter D1, soit — le plus honnête ici — publier l'écart comme la troisième « seconde voie » du module, à côté de celle des 5,52 jours. |
| **M4** | La **présence** de la pompe est une fiction, et le taux de parc de 39 % en dépend. | majeur | Le S3 écrit « la pompe **ne reste pas sur le site** : elle vient et repart » ; la figure 2 la compte présente **281 jours** sur les 884 engins-jours de présence. Si on ne la compte présente que ses 15 jours d'intervention, le taux de parc passe de **39 % à 56 %**. L'« erreur courante » de la figure (« la présence dit seulement combien de temps **on les paie** ») est fausse pour deux engins sur trois : seul le chariot se paie à la présence. Et le titre « Engins présents **sur le site** » omet les deux grues à tour de C1 (pointe réelle 5, pas 3). | Distinguer « fenêtre d'emploi » et « présence facturée » dans la figure et dans le texte ; dire que le profil ne porte que les trois familles de C6 ; recalculer le taux de parc sur ce que chacun paie réellement, ou renoncer au nombre agrégé. |
| **M5** | « Tout ce qui précède sort de **vingt-cinq** nombres déclarés […] **et il n'y en a pas d'autres**. » | majeur | La liste en compte **24**. Et le tableau des verdicts lit aussi : les 250 jours ouvrés (balisés deux sections plus haut), le **1 450 MAD/j** du chariot (balisé deux sections **plus bas**, et c'est lui qui fait `L₀ = 362 500`), les 4 200 MAD/j et 520 MAD/h de D1, les 98,4 m³ de la TV et les 3,08 h de C3. | Compter juste, déplacer la balise du 1 450 MAD/j avant le tableau qui l'utilise, et remplacer « il n'y en a pas d'autres » par la liste des valeurs **héritées** des autres modules. |
| **M6** | Deux hypothèses déclarées et commentées que **rien ne lit** : disponibilité de la pelle (85 %) et du chariot (92 %). | majeur | Mutation : valeurs portées à **5 %** dans une copie du dépôt, `cout_horaire.py` relancé, `materiel.json` **identique au caractère près**. Seules les disponibilités des *maillons* de la chaîne sont lues. La fiche d'Étape 0 promettait « immobilisation et pannes ». | Soit les faire travailler (un engin indisponible ne travaille pas : `h = jours × hpjs × dispo`, ce qui change l'emploi des trois engins), soit les retirer des 25 hypothèses et de la prose qui les commente. |
| **M7** | La « **simulation directe** » de la chaîne est satisfaisable par construction, et elle est présentée comme la voie que D-067 impose. | majeur | `ok = sum(all(rng.random() < p for p in ps))` tire **les mêmes p, indépendants** : la simulation *est* la définition du produit, elle ne peut que le confirmer (mes 2 000 000 de tirages : 0,043 point). Ce qui pourrait être faux dans ce modèle — l'**indépendance** des quatre maillons — est supposé des deux côtés, et n'est déclaré nulle part. Le texte en fait pourtant un argument : « Cette double voie n'est pas une coquetterie : c'est la règle D-067, née du module C4 où une formule parfaitement homogène était fausse d'un terme. » | Le dire, comme le module le fait très bien ailleurs (« Un contrôle qui ne contrôle rien »). Une vraie seconde voie serait une simulation avec un **facteur commun** (météo, accès, jour férié) montrant de combien le produit surestime la disponibilité quand les maillons sont corrélés. |
| **M8** | Une espérance **par coulage** comparée à un coût **par jour**, sans un mot sur l'unité. | majeur | `esperance = gain × 16 240,33` : `gain` est une probabilité par coulage, `16 240` un coût par jour ouvré ; le résultat est comparé à 1 800 et 120 **MAD/j**, sous un en-tête « Espérance · MAD/j » et une colonne « MAD / point » sans dimension temporelle. Dans un module dont la thèse est « demandez dans quelle unité on paie ». | Écrire « MAD **par coulage** » et déclarer que le secours n'est immobilisé que les jours de coulage (15 sur le chantier) — sinon l'immobilisation d'une seconde pompe se paie à la **fenêtre**, et le module vient de démontrer ce que cela change. |
| **M9** | La **fiche livrée** (`cadrage/05-sommaire.md`, « écrit le 30/10/2026 ») publie la formule **périmée**. | majeur | Elle écrit : « LE POINT D'EQUILIBRE EST UN NOMBRE D'HEURES PAR AN, **h\* = F/(l-v)**, et non une duree de detention ». C'est exactement la formule que le S2 et le S5 n° 2 déclarent **fausse** (« exact quand L₀ = 0, faux sinon »), et elle porte en plus l'affirmation corrigée en B3. | Remplacer par `h₀ = (L₀ − F)/(v − L₁)` et sa condition de sens dans la fiche livrée. Les écarts avec la fiche d'Étape 0 (D-061) sont, eux, bien consignés — et c'est la seule fiche du lot qui le fasse aussi complètement. |
| **M10** | « Un rapport de 2,62 […] **il ne vient d'aucune différence de prix de marché** : il vient de l'unité. » | majeur | Les deux engins comparés ne sont pas le même engin : 4,2 MMAD contre 2,6 MMAD d'achat, soit **1,62** avant toute question d'unité. La démonstration propre existe dans le module — pour le chariot : 414 MAD/h s'il était payé ses jours de travail, 973 payé à sa fenêtre, **même engin, même prix** — mais elle n'est pas celle qui est mise en avant. | Mettre le chariot en vitrine (même engin, deux régimes, facteur 2,35) et présenter le 2,62 pour ce qu'il est : un écart où l'unité et la machine jouent ensemble. |
| m1 | « la possession économise **-120 000 MAD** par an » (S4a et figure 1). | mineur | `ecart_MAD_an = −119 624`, convention interne `possession − location`, rendue telle quelle dans une phrase qui annonce une économie. | Publier la valeur absolue dans la prose, ou renommer le champ `gain_de_la_possession`. |
| m2 | Figure 3 : les quatre libellés sont sans accents. | mineur | Capture `…figure3.png` : « Debit catalogue », « Beton reel, tuyauterie », « Heure reellement pompee », « Nettoyages et arrets ». | Accentuer `rendement_de_la_pompe.etapes[].etape`. |
| m3 | Exercice 3 : « 555 × 1 450 = **804 721** ». | mineur | 555 × 1 450 = 804 750 ; le calcul exact utilise 554,98 j. | Afficher 554,98 dans le produit, ou arrondir le résultat au produit affiché. |
| m4 | Exercice 1 : « de **deux fois moins** qu'avant ». | mineur | 119 624 / 47 125 = **2,54**. | « de plus de deux fois et demie ». |
| m5 | Sommaire latéral : « L'emploi de la pompe est entièrement `**déduit**` ». | mineur | HTML du module, `<nav class="sommaire">`. | Retirer le gras du titre, ou dé-marquer le texte de l'ancre. |
| m6 | Deux phrases publiées deux fois (mutualisation, encart suivant). | mineur | « Deux sites font 1,58 site équivalent, pertes de transfert déduites » ×2 à une ligne d'écart ; « chaque heure de plus coûte du carburant et un conducteur » ×2. | Choisir entre la prose et la variable injectée. |
| m7 | Phrase tronquée : « … la **centrale** (96 %) et la **rotation des toupies** (92 %) : *Une toupie de plus…* ». | mineur | Seule `secours[1].pourquoi` est injectée ; la raison de la centrale (`secours[0].pourquoi`, qui existe) manque. | Injecter les deux. |
| m8 | Figure 1 : la graduation « 1500 » est traversée par la courbe. | mineur | Capture `…figure1.png`. | Décaler les graduations sous l'axe (dette 11 : chevauchement texte/trait non testé). |
| m9 | Check-list : deux points numérotés « 8 » dans `content/`. | mineur | Lignes « 8. Le seuil est-il comparé au plafond… » et « 8. Le rendement réel… ». | Renuméroter (le rendu masque le défaut, la source le garde). |
| m10 | La fiche livrée annonce « Quiz : **6 questions** » ; le module en pose **7** (1, 2, 3, 3 bis, 4, 5, 6). | mineur | S7 du module. | Corriger la fiche. |
| m11 | « le nombre de jours de présence par an **reste** 250 » présenté comme un constat. | mineur | Vrai par construction : `unites_facturees_par_an = fenêtre ÷ (fenêtre/250) = 250` quelle que soit la fenêtre. | Le dire : c'est une identité du régime de présence, pas un résultat du report. |
| m12 | `interventions = ⌈14,03⌉ = 15`. | mineur | 1 380,8 / 98,4 = 14,03 ; l'arrondi ajoute **6,9 %** de location et d'heures. | Commenter l'arrondi (une venue ne se divise pas) — c'est un bon piège, il mérite une ligne. |
| m13 | Le volume d'un coulage de mezzanine (98,4 m³) est appliqué au radier (320 m³) et au PH technique (240 m³). | mineur | Ces deux postes font 800 m² chacun et ne sont pas découpés en zones de 360 m². | Déclarer la simplification, ou découper par poste. |
| m14 | Pour la pelle, heures de **compteur** = heures de **travail** (195,3 = 195,3). | mineur | `unites_facturees = heures_de_travail`. Un compteur tourne aussi au ralenti. | Déclarer l'hypothèse — c'est le sujet du module. |
| m15 | « un coulage dérangé = un jour entier de frais de durée » non déclaré. | mineur | Seul le périmètre (sans pénalités) l'est. Vérifié non déterminant : à un demi-jour, l'aiguille reste rentable (184 > 120), la pompe non. MEZZ est bien sur le chemin critique de D2. | Une ligne dans `perimetre_du_jour_perdu`. |

---

## Décompte

**29 défauts dont 4 bloquants, 10 majeurs, 15 mineurs.**

Les quatre bloquants tiennent en une phrase chacun : **le locataire du chariot ne paie pas son
gasoil** (et c'est toute la pente de la figure 1, donc le verdict publié) ; **les jours de travail
sont comptés deux fois** quand deux tâches se recouvrent (et le module publie 303 et 350 pour la même
grandeur) ; **le quiz nie une dépendance que le modèle contient** et contredit le S5 de la même page ;
**une figure affirme « toujours » là où mon balayage trouve 188 contre-exemples**.

Ce que je n'ai pas trouvé, et que je dis avec la même force : l'arithmétique est juste partout où je
l'ai refaite à l'aveugle — les trois coûts annuels, les trois seuils par balayage, les trois fenêtres,
les 15 interventions, la chaîne, les tirages, les profils du parc. Les 33 hypothèses sont toutes
déclarées avec fourchette et année, toutes registrées, toutes conformes à `data/`. Aucune valeur
normative n'est entrée dans le module, et le ⏸ est tenu. Le défaut de ce module n'est pas son calcul :
c'est **ce que ses phrases disent du calcul**.

---

## Suite donnée (auteur, 30/10/2026)

Rapport reçu sur le commit `721321c`. **Les 4 bloquants et 8 des 10 majeurs sont corrigés** ; les
2 majeurs restants et les 15 mineurs sont inscrits en dette (STATE, dette 38).

### Les quatre bloquants

- **B1 — le gasoil d'un seul côté. CONFIRMÉ, et c'est le plus grave.** Vérifié : la pente publiée
  (+80,5 MAD/h) valait exactement 7 l/h × 11,5 MAD. Corrigé en déclarant, par famille, ce que le
  prix de location **comprend** (`location.comprend`) et en ajoutant au locataire, à l'heure
  travaillée, tout ce qui n'y figure pas. Conséquence : pour le chariot $L_1 = v$, la pente est
  **nulle**, il n'y a **aucun seuil**, et l'écart vaut $F - L_0 = $ −151 600 MAD/an à tout emploi.
  Le verdict passe de « NON TRANCHÉ » (85,7 %) à **POSSÉDER** (93,3 %), comme le rapport l'annonçait.
  Figure 1 refaite — elle trace désormais l'écart contre le **prix journalier**, qui croise zéro à
  843,6 MAD/j, soit 41,8 % de remise à obtenir. Exercices 1 et 3 réécrits. Décision **D-070**.
- **B2 — les jours comptés deux fois. CONFIRMÉ.** Vérifié : 251,94 j de segments pour 206 j d'union
  sur le chariot. L'emploi se calcule désormais sur l'**union des jours de calendrier**. Les deux
  nombres de jours d'attente (303 et 350) ont disparu : il n'y en a plus qu'un, 349, et la figure
  avait raison contre le texte. **Nuance apportée au rapport** : l'écart entre union et somme a
  **deux** causes de sens contraire — le recouvrement (la somme dépasse) et les journées partielles
  (l'union dépasse, car un segment qui finit à midi occupe la journée). Le champ publié les nomme
  toutes les deux.
- **B3 — le quiz nie une dépendance du modèle. CONFIRMÉ.** Le quiz 1 et le glossaire disaient « la
  durée de détention n'y figure pas » alors que $F$ contient l'amortissement sur $n$ années. Les
  deux sont réécrits : ce qui ne compte pas est le **total d'heures accumulées** ; ce qui compte est
  l'intensité annuelle **et** la durée d'amortissement.
- **B4 — « toujours au moins un engin payé qui ne fait rien ». CONFIRMÉ, faux 188 jours sur 601.**
  La phrase est supprimée. La correction de M4 la rendait de toute façon caduque : deux des trois
  engins ont désormais présence = travail.

### Les majeurs corrigés

- **M1** les champs `plafond` et `emploi_reel` de la figure 1 n'étaient pas dessinés : la figure est
  refaite et ne publie plus que ce qu'elle trace.
- **M2** « sites équivalents » est un **rapport d'emploi** et non un nombre de sites. Les deux sont
  désormais publiés, avec l'inversion du facteur $(1 + (n-1)k)(1 - \text{perte})$ : 4,27 fois
  l'emploi = 5,8 sites pour la pompe.
- **M3** le périmètre incohérent de la pompe : ses tâches ne sont plus déclarées, elles sont
  **déduites** des postes dont le sous-détail de D1 porte une journée de pompe (RADT, PHNT, MEZZ).
  Son coût horaire de possession passe de 25 364 à **4 949 MAD/h** — le chiffre du rapport.
- **M4** la présence d'un engin dépend de son **régime** : fenêtre pour un engin payé à la présence,
  jours de travail pour un engin qui vient et repart. Le taux de parc passe de 39,1 à **44,4 %**, et
  toute l'attente du parc est celle d'un seul engin. Le périmètre du parc (ni la grue de C1, ni le
  coffrage de C3) est publié avec la figure.
- **M5** le compte « vingt-cinq nombres » est remplacé par la liste, avec la mention explicite des
  valeurs que le tableau **lit** chez D1, TV et C3 sans les redéclarer.
- **M6** les deux disponibilités que rien ne lisait alimentent désormais un résultat : les jours de
  panne attendus par famille, comparés à la **marge** de leurs tâches. Résultat non trivial — la
  seule disponibilité qui coûte un délai est celle du chariot, qui sert COUV et SECO, deux tâches
  à marge nulle : **267 641 MAD**.
- **M8** l'espérance d'un secours et son coût sont désormais tous deux **par coulage**, et
  `verif_unites.py` définit une dimension `coulage` pour que l'addition d'un MAD/coulage et d'un
  MAD/jour **lève**.
- **M9** la fiche livrée publiait la formule périmée : réécrite.
- **M10** le rapport de 2,62 était attribué à l'unité seule alors qu'il mêle trois causes. La
  démonstration qui ne change **qu'une** variable est mise en avant : le même chariot, au même prix,
  facturé à ses jours de service au lieu de sa présence, coûte 2,3 fois moins.

### Les deux majeurs non corrigés, et pourquoi

- **M7 — la « simulation » de la chaîne est tautologique.** Le rapport a raison : tirer les mêmes
  $p$ indépendants **est** la définition du produit, et l'indépendance des quatre maillons — le seul
  vrai risque du modèle — n'est déclarée nulle part. La simulation reste (elle attrape une faute de
  code, pas une faute de modèle), mais l'hypothèse d'indépendance doit être déclarée et discutée :
  une rupture de ciment et un camion en panne ne sont pas indépendants un jour de grève. **Inscrit
  en dette.**
- **M4 bis — la pointe du parc.** Les deux grues de C1 n'y sont pas, et la pointe réelle du matériel
  du site est de 5 et non de 3. Le périmètre est maintenant écrit sur la figure, mais le chiffre
  consolidé du matériel de chantier n'existe nulle part. **Inscrit en dette** : il appartient à un
  module de synthèse, pas à C6.

### Ce que cette passe a appris au cours

Trois erreurs de modèle successives sur le **même objet** — la facturation — chacune trouvée par un
instrument différent : un croisement avec le bordereau de D1, une **figure** qui ne croisait pas
zéro, et cette relecture hostile. **Aucune par un test.** C'est la onzième famille de défauts du
cours, et c'est une variante aggravée de la dixième : non pas un terme faux, mais un terme juste
**placé d'un seul côté** d'une comparaison. Les tests de C6 passent de 177 à **250 contrôles**.
