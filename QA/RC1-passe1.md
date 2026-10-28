# RC1 — passe /devil n° 1 (Annexe 4, § 12.2)

Relecteur hostile, indépendant de l'auteur. Le raisonnement du module n'a été lu qu'**après**
le recalcul du § 1 : les valeurs ci-dessous sont reconstruites depuis `calc/sorties/` seul, par
des scripts écrits pour cette passe
(`/tmp/claude-0/-home-user-mine/70713aa8-3622-5c6d-a7c2-bce4a8b25d73/scratchpad/devil-rc1/`,
`blind1.py` à `blind5.py`, `hist.py`).

Capture `tests/captures/10-rc1-revue-critique-palier-1.html-figure1.png` : **ouverte et regardée**
(§ 12.1 b). Elle porte trois des défauts ci-dessous, dont aucun n'est vu par la chaîne.

**Ce qui est bien fait, en une ligne pour chaque :** le refus de mettre des MAD, des jours et des
points sur un même axe, et le choix de l'écart relatif à la place — c'est la faute que le module
dénonce, et il ne la commet pas. La fiche mémo S8 : sept questions, sept familles, aucun doublon,
aucun manque, et l'ordre est celui du § S2. Les appâts L9 et L10 sont des appâts honnêtes. Le
chiffrage de E7 (13 j → 211 124 à 1 662 044 MAD « selon le régime ») est la seule ligne du corrigé
qui porte à la fois son unité, son régime et sa dépendance.

---

## 1. Contre-expertise à l'aveugle

Huit recalculs depuis les sorties des autres modules, sans ouvrir `calc/revue.py`.

### 1.1 Les valeurs du dossier — ce que publient réellement les modules

| Ligne | Affiché | Recalculé par moi, depuis la sortie du module | Verdict |
|---|---:|---|---|
| L2 | 57,41 % | moyenne arithmétique de `suivi.etats.constate` (27 tâches) = **57,4059 %** | conforme |
| L3 | 12,1 j | `planification.durees.CHLV.duree_de_travail_de_jour_j` = **12,13** ; `duree_j` = 48,64 ; `facteur_d_interception` = 4,01 | conforme |
| L4 | 796 469 MAD | 10 × 79 646 878,79 × 1,0 ‰ = **796 468,79** | conforme |
| L5 | 1 534 194 MAD | 12 × `cout_sous_penalites_MAD_par_jour_ouvre` (127 849,50) = **1 534 194,00** | conforme |
| L7 | 134 997 MAD | 21 315 + 7 × 16 240,33 = **134 997,31** | conforme |
| L8 | 7 j | `qualite.impact_planning.immobilisation_j` = **7,0** | conforme |
| L1 / L9 / L10 | 31,15 % / 207,0 / 0,76 % | `suivi.avancements.physique_pct` / `ferraillage…ratio_du_plan_kg_m3` / `qualite.dechets.part_dangereuse_pct` | conformes |
| **L11** | **0,951** | `valeur-acquise.CPI` = 0,951, **mais c'est le CPI de la TRANCHE VERTICALE** (BAC 2 779 824 MAD). **D4 publie `suivi.valeur_acquise.CPI` = 0,8962** à la date d'arrêt | **FAUX** → B1 |

### 1.2 Les facteurs entre affiché et juste

| | Affiché / juste | Recalculé | Référence publiée | Verdict |
|---|---|---|---|---|
| E1 | 796 468,79 → 1 116 091,71 | **×1,4013** | `conversion.calendaires_par_jour_ouvre` = 1,4013 | exact |
| E2 | 1 534 194 → 194 883,96 | **×7,871** → +687,1 % | `rapport_des_deux_regimes` = 7,9 | exact (figure : 687,2) |
| E3 | 12,13 → 48,64 | **×4,010** → −75,1 % | `facteur_d_interception` = 4,01 | exact |
| E5 | 21 315 → 134 997,31 | **+533,3 %** | 7 × 16 240,33 = 113 682,31 | exact |
| E6 | 31,15 → 57,41 | **+84,3 %** | — | **faux dénominateur** → B2 |
| E7 | 7 → 20 | **−65,0 %** | `retard_du_chantier_j` CHLV = 20 | exact |

### 1.3 Moyenne non pondérée contre moyenne pondérée (E6)

Recalculé depuis `prix.bordereau.postes` et `suivi.etats.constate`, poste par poste :

```
moyenne non ponderee  (27 taches)        = 57,41 %   <- la ligne L2
moyenne ponderee par le PRIX des postes  = 34,01 %   <- = physique_constate_sur_ouvrages_pct
suivi.avancements.physique_pct           = 31,15 %   <- la "valeur juste" du corrige
```

`physique_pct` n'est **pas** la pondération par le budget des mêmes 27 avancements. Lecture de
`calc/suivi.py` l. 42-52 après coup : le numérateur ajoute
`frais_de_duree × coefficient_de_vente × min(1 ; j/durée_totale)`, et le dénominateur est le
marché entier (79,65 MMAD) et non la somme des postes (68,25 MMAD). C'est une mesure **plus une
horloge** — ce que `suivi.valeur_acquise.frais_de_duree.pourquoi_a_part` condamne mot pour mot.
La pondération par le budget des 27 mêmes tâches vaut **34,01 %**.

### 1.4 Les coûts annoncés par le corrigé

| | Annoncé | Mon recalcul | Libellé | Verdict |
|---|---|---|---|---|
| E1 | 319 623 MAD, +40 % | 1 116 091,71 − 796 468,79 = **319 622,92** ; +40,1 % | MAD | **juste** |
| E2 | 1 339 310 MAD, ×7,9 | 1 534 194 − 194 883,96 = **1 339 310,04** | MAD | **juste** |
| E3 | **36,5 jours de chantier** | 48,64 − 12,13 = 36,51 — mais **en plages de consignation** (unité déclarée par la source), pas en jours de chantier. Étalement réel 320,64 j ; à 12,13 plages il faudrait 5 fenêtres, soit ≈ 80,7 j : **le manque au planning est ≈ 240 j calendaires** | jours | **FAUX** → B5 |
| E4 | « rien en argent » | contredit par la dette n° 10 : sur la base définie, 7,77 % contre 15–30 % — **hors fourchette**, facteur **×1,92** « confirmé, chiffré, non soldé » | — | **FAUX** → B6 |
| E5 | 113 682 MAD, +533 % | 7 × 16 240,33 = **113 682,31** ; +533,3 % | MAD | juste en nominal, **non borné** → M2 |
| E6 | **26,3 points** | 57,41 − 31,15 = 26,26, mais contre le mauvais repère ; contre 34,01 : **23,40 points** | points | **FAUX** → B2 |
| E7 | 13 j, 211 124 à 1 662 044 MAD | 20 − 7 = 13 ; 13 × 16 240,33 = **211 124,29** ; 13 × 127 849,50 = **1 662 043,50** | j + MAD + régime | **juste** |

Quatre sur sept justes, trois faux. Les trois unités sont correctement distinguées (MAD, jours,
points) — sauf E3, où le corrigé de l'erreur d'unité se trompe d'unité.

### 1.5 Bornes publiées, que le corrigé ignore (D-049)

```
E5 : juste = 21 315 MAD   bornes publiees [5 000 ; 101 280]        -> facteur 20
     part "inventee"      de 40 601 a 259 845 MAD selon l'immobilisation [2,5 ; 16,0] j
     ecart relatif        de +40 % a +5 197 %   (le corrige et la figure publient 533,3 %)
E7 : 20 j est un PALIER mesure, invariant entre 0,5 et 16 j d'immobilisation (D-050) -> robuste
```

### 1.6 L'histoire du palier — recomptage depuis `QA/` et `STATE.md`

| Source | Passes | Défauts | Bloquants |
|---|---:|---:|---:|
| Somme des 16 rapports de `QA/` (mon recomptage) | **16** | **434** | **93** |
| `STATE.md` § « Défauts et passe adversariale » (50+117+32+28+33+32+36+33+45+28) | 16 sur 10 modules | **434** | 93 |
| Dernier rapport de chaque module seulement | 10 | 300 | 75 |
| **RC1, D-058 et `QA/RC1.md`** | **« dix passes »** | **309** | **79** |

Aucune combinaison que j'aie pu construire ne rend 309/79. → B4.

### 1.7 « Aucun bloquant trouvé par un contrôle automatique »

Trois contre-exemples trouvés dans le dépôt :

1. `QA/B3e-passe1.md` l. 294 : **« B-2b · Trouvé par le canari du B-2 »** — un bloquant numéroté,
   trouvé par un test. Dalle 6 818 → **7 708 kg**, chiffre qui est aujourd'hui dans
   `ferraillage.ordre_de_grandeur` (7 707,6 kg).
2. `STATE.md` l. 97 : « **73 canaris, tous rouges** — et **deux d'entre eux ont trouvé seuls une
   erreur que la passe n'avait pas vue** ».
3. Le tableau du § S5 de RC1 lui-même : « La vérification dimensionnelle — elle a trouvé une année
   de 365,25 jours » (`QA/REC-passe1.md` M6). Le module concède donc à la ligne 3 de son tableau ce
   que son encart nie dix lignes plus bas.

→ B3.

---

## 2. Défauts

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **B1 · L11 : le CPI de l'appât n'est ni celui de D4, ni celui de la date d'arrêt — et le corrigé donne tort au relecteur qui le signale.** La note annonce « situation à la date d'arrêt du module D4 » et « CPI à la date d'arrêt = 0,951 ». D4 publie **0,8962**. 0,951 est le CPI de la **tranche verticale** — un plancher de mezzanine, BAC 2 779 824 MAD — pas celui du chantier (BAC 58,3 MMAD). | **bloquant** | `suivi.json → valeur_acquise.CPI = 0.8962` contre `valeur-acquise.json → CPI = 0.951` et `budget_a_l_achevement_BAC_MAD = 2 779 824`. `calc/revue.py` l. « `cpi = s["valeur-acquise"]["CPI"]` » étiqueté `"source": "module D4 — valeur-acquise.CPI"` : le fichier lu n'est pas celui de D4. Les deux seules occurrences de `0.951` dans `suivi.json` sont des `CPI_max` de la courbe de sensibilité à j 330-350, sans rapport. Et `calc/tests/test_revue.py` § 3 **épingle cette erreur** : `"L11": S["valeur-acquise"]["CPI"]`. | Lire `suivi.valeur_acquise.CPI` (0,8962) et corriger la `source`. Ou faire de L11 une **huitième erreur** — « un indice emprunté à un autre périmètre » — ce qui serait la meilleure du dossier. En l'état, un relecteur qui écrit « ce CPI ne peut pas être celui de ce chantier » a raison, et le corrigé le déclare en faute. |
| **B2 · E6 : la « valeur juste » n'est pas la grandeur que le corrigé dit qu'elle est.** Le corrigé écrit « un avancement se pondère par le BUDGET de chaque tâche, et c'est ce que publie le module D4 », et donne 31,15 %. Ce n'est pas cette pondération : c'est elle **plus** un terme de frais de durée au prorata du temps, sur un dénominateur plus large. | **bloquant** | `calc/suivi.py` l. 42-52 : `physique = Σ(prix_total_i × constate_i)` **puis** `physique += fd["total_MAD"] × coefficient_de_vente × min(1, j/durée)`, le tout `/ prix_de_vente_MAD` (79,65 MMAD) alors que la somme des postes vaut 68,25 MMAD. Mon recalcul (§ 1.3) : la pondération par le budget des mêmes 27 valeurs vaut **34,01 %**, que D4 publie sous `physique_constate_sur_ouvrages_pct`. Conséquences : « 26,3 points d'écart » → **23,4** ; barre E6 de la figure « +84,3 % » → **+68,8 %**. Le module `suivi` condamne lui-même ce mélange : « Les additionner dans une seule valeur acquise mélange une mesure et une horloge ». | Prendre `physique_constate_sur_ouvrages_pct` (34,01 %) comme valeur juste, et le dire : c'est la moyenne pondérée par le budget des **mêmes** tâches. Republier L1 sur le même repère, sans quoi L1 et L2 n'opposent pas deux chemins vers la même grandeur mais trois grandeurs. Ajouter le test de règle : la valeur juste de E6 **est** `Σ(budget×constate)/Σ(budget)`, recalculée dans le test. |
| **B3 · « Aucun des 79 défauts bloquants de ce palier n'a été trouvé par un contrôle automatique » est faux, et le module le sait trois lignes plus haut.** | **bloquant** | § 1.7 ci-dessus : `QA/B3e-passe1.md` l. 294 (**B-2b, bloquant, « Trouvé par le canari du B-2 »**) ; `STATE.md` l. 97 (« deux d'entre eux ont trouvé seuls une erreur que la passe n'avait pas vue ») ; et le tableau du § S5 de RC1 qui crédite la vérification dimensionnelle de l'année de 365,25 j. L'encart est titré « Le constat le plus inconfortable du palier » : c'est une affirmation absolue, dans un module qui enseigne qu'un nombre invérifiable est un défaut. | Écrire ce qui est vrai et qui reste fort : *« Sur 93 bloquants, un seul a été trouvé par un contrôle automatique — un canari posé après coup, pour empêcher le retour d'un défaut déjà trouvé à la main. »* La leçon est intacte ; la phrase devient exacte, et le contre-exemple la renforce (un canari utile cherche, il ne confirme pas). |
| **B4 · « Dix passes, 309 défauts dont 79 bloquants » n'est reconstructible depuis aucun comptage du dépôt, et contredit `STATE.md`.** | **bloquant** | § 1.6 : `STATE.md` donne E1 : 50 (3 passes) · TV : 117 (5 passes) · D2 : 32 · D1 : 28 · C3 : 33 · D4 : 32 · B3e : 36 · B7c : 33 · C7 : 45 · REC : 28 = **434 défauts** sur **16 rapports**, et 93 bloquants. « Dix » est le nombre de **modules**, pas de passes. (`STATE.md` est d'ailleurs lui-même incohérent : B7c y vaut 39 l. 37 et 33 l. 62 ; et sa liste de bloquants « 15 · 8 · 7 · 6 · 8 · 11 · 11 » porte sept nombres pour huit modules.) Le chiffre est repris tel quel dans `D-058` et dans `QA/RC1.md`. Précédent dans ce dépôt : `QA/TV-tranche-verticale-passe5.md` M10 classe **majeur** un bilan de `STATE.md` qui annonce « 94 défauts, tous corrigés » à tort. | Recompter, publier « 16 passes sur 10 modules, 434 défauts dont 93 bloquants », et **dériver ces nombres d'un script** qui lit `QA/` au lieu de les écrire à la main — c'est la règle que le module enseigne au paragraphe suivant. Corriger D-058 et `QA/RC1.md` dans le même geste. |
| **B5 · E3 : le corrigé de l'erreur d'unité se trompe d'unité, et minore de 6,5 fois le manque au planning.** « 36,5 **jours de chantier** absents du planning » : 36,51 est la différence de deux durées **de travail**, et la source déclare que leur unité est « plages de consignation, et non journées de 8 h ». | **bloquant** | `planification.durees.CHLV` : `"unite": "plages de consignation, et non journees de 8 h"`, `duree_etalee_j = 320.64`, `consignations.CHLV.nb_fenetres = 17`, `immobilisation_improductive_j = 272.0`. Mon recalcul (`blind5.py`) : 48,64 plages = 2,86 par fenêtre ; 12,13 plages tiendraient en 5 fenêtres, soit ≈ 80,7 j d'étalement contre 320,64 → **≈ 240 jours calendaires** manquent au planning, sur une tâche critique (`marge_totale_j = -0.0`). Le même « 36,5 jours » est repris dans la légende « erreur courante » de la figure 1 pour désigner E3 comme la plus coûteuse. Et le § S4g écrit « le quart du temps nécessaire », ce qui n'est vrai que du contenu de travail. | Deux nombres, pas un : « **36,5 plages de consignation** de travail non comptées, soit **≈ 240 jours calendaires** d'étalement absents du planning, sur une tâche à marge nulle. » C'est plus fort, pas moins, et c'est exactement la leçon de la famille. Ajouter le test de règle : l'unité d'une durée citée dans `ce_qu_elle_coute` doit être celle que publie sa source. |
| **B6 · E4 : le corrigé apprend à classer sans suite une alerte qui est réelle.** « une alerte spectaculaire sur un chiffre qui **n'a rien d'anormal** » ; « Comparer les deux **n'alerte sur rien** ». | **bloquant** | `prix.controle_ratios.part_main_oeuvre_beton_arme_decompose` : constaté **7,77 %**, fourchette [15 ; 30], `ratio_defini_sur_cette_base: true`, **`dans_la_fourchette: false`**. Sur la base où le ratio EST défini, il reste hors fourchette d'un facteur 2. `STATE.md` dette n° 10 : « la base du ratio était fausse **et** les cadences sont optimistes — facteur **×1,92** pondéré par le travail, chemin indépendant. Le soupçon “2 à 3” est **confirmé dans son sens** […] **Chiffrée, non soldée** ». `prix.json._lecture` dit la même chose. | Corriger la thèse de E4 : la **comparaison** est nulle sur cette base, et le bon geste n'est pas de classer l'alerte mais de **refaire le ratio sur sa base définie** — où il alerte encore, moins fort, et où il porte la dette n° 10. Sinon le module enseigne au lecteur le réflexe qu'il dénonce ailleurs : accepter un verdict parce qu'on a trouvé une raison de l'écarter. |

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **M1 · E1 est indécidable avec le dossier seul, et son corrigé érige une hypothèse V3 du cours en règle.** | majeur | La ligne L4 dit « Pénalités encourues pour 10 jours de retard » : aucun calendrier n'est nommé. 796 469 MAD est **exactement juste** si ces 10 jours sont calendaires. Rien dans le dossier — ni le montant du marché, ni la clause, ni la date — ne permet de trancher. Et `data/projet-gare.json → prix_unitaires_MAD.contrat.penalite_retard_pour_mille_par_j.note` dit seulement « pour mille du montant du marché, **par jour de retard** », sans calendrier ; le bloc porte en tête « AUCUNE de ces valeurs n'est une règle ». Le symptôme proposé est inutilisable pour la même raison : « une pénalité qui tombe trop ronde » (796 469 n'est rond que rapporté à un marché que le lecteur ne connaît pas) et « un ordre de grandeur plus faible que ce que le marché laisse attendre » (idem). | Soit écrire la clause dans le dossier (« pénalité de 1 ‰ du marché par jour calendaire de retard ; marché 79 646 879 MAD ») et l'erreur devient trouvable ; soit déplacer l'erreur : **la faute est le silence sur le calendrier**, les deux nombres sont défendables, et c'est cela qu'un visa refuse. La seconde version est meilleure et respecte le § 5.0 — en l'état, le corrigé présente une convention du cours comme la bonne réponse. |
| **M2 · D-049 : aucune borne nulle part, et le cas de E5 n'y survit pas.** | majeur | `qualite.non_conformite.par_ouvrage[NOYX].total_bornes_MAD = [5 000 ; 101 280]` (facteur 20) ; `jours_immobilises_bornes = [2,5 ; 16,0]`. Mon recalcul : la part « inventée » va de **40 601 à 259 845 MAD**, et l'écart relatif de **+40 % à +5 197 %** là où le corrigé et la figure publient 533,3 %. D-049 : « Tout résultat chiffré d'un module publie ses **deux bornes** ». | **Ma tranche, motivée** : les bornes n'ont rien à faire sur les lignes du **dossier** — une note de chantier porte un chiffre, et des bornes désigneraient les lignes instrumentées, donc détruiraient l'exercice. Elles sont **obligatoires dans le corrigé**, où le cours parle en son nom : valeur juste, « ce qu'elle coûte », et barres de la figure. E7 est le contre-exemple utile et il faut le dire : 20 j est un **palier**, invariant sur toute la fourchette d'immobilisation (D-050) — c'est le seul chiffre du dossier qui n'a pas besoin de bornes, et c'est une leçon en soi. |
| **M3 · Figure 1, 3ᵉ « ce qu'il faut voir » : elle fusionne deux familles que le module déclare distinctes, et rebaptise E2.** « Les deux plus gros écarts — E2 et E5 — sont des **coûts inventés**, et tous deux viennent de **la même faute** : appliquer une grandeur hors de la condition sous laquelle elle vaut. » | majeur | Capture lue. E2 a pour famille « condition d'emploi d'une grandeur », E5 « coût inventé » ; le § S2 en fait les questions **2** et **7**, la fiche mémo les lignes 2 et 7, et `test_revue.py` § 1 exige que « chaque erreur appartienne à une famille DIFFÉRENTE ». Les deux mécanismes sont d'ailleurs distincts : E2 applique un prix hors de sa condition, E5 impute des frais de durée à un ouvrage qui a 436 j de marge — c'est une faute de **causalité**, pas de condition. | « Les deux plus gros écarts sont des provisions inventées, par deux fautes différentes : E2 emprunte un prix hors de sa condition, E5 impute un retard à un ouvrage qui n'en provoque aucun. Deux familles, un même symptôme financier. » Et ajouter le test : aucun texte de figure ne nomme la famille d'une autre erreur que la sienne. |
| **M4 · L'axe de la figure n'est pas honnête pour la grandeur qu'il porte.** Un rapport est tracé sur un axe linéaire de pourcentage, de −75 à +687. | majeur | Capture lue. Une **sous-estimation d'un facteur 4** (E3, −75,1 %) y occupe une barre 9 fois plus courte qu'une **surestimation d'un facteur 7,9** (E2, +687,2 %), alors que les deux fautes sont du même ordre ; E1 (facteur 1,40) et E7 (facteur 2,86) sont réduits à des moignons. La légende « erreur courante » reconnaît le problème (« ne pas trier par la hauteur ») : le dessin est corrigé par un avertissement au lieu d'être corrigé. | Tracer le **facteur** `affiché / juste` sur un axe logarithmique centré sur 1 (E3 à ÷4,0 et E5 à ×6,3 deviennent voisins, ce qui est la vérité), ou tracer deux séries. Et garder l'avertissement, qui reste vrai. |
| **M5 · La légende de la barre rouge est rendue comme un titre, sans aucun lien visuel avec sa barre.** | majeur | Capture lue : « erreur de lecture : le nombre est juste » s'affiche en rouge, **centré en haut du cadre**, à la place d'un titre de figure. La barre E4 est un filet rouge de ~3 px à l'abscisse 0, à 150 px de là, étiqueté « 0 ». Aucune pastille, aucun repère, aucune clé de couleur. Un lecteur ne peut pas relier les deux — et c'est la seule information que la figure apporte sur E4. Dette n° 13 du dépôt : « aucun contrôle ne vérifie qu'une figure montre ce qu'elle prétend montrer ». | Une pastille de couleur devant le texte, et le texte posé à côté de la barre E4 (ou en note sous l'axe). Ajouter au `svgkit` la règle : toute option `legende_alerte` produit un échantillon de couleur, jamais un texte seul. |
| **M6 · Le document n'est pas crédible comme note de chantier, et son en-tête contredit sa première ligne.** | majeur | En-tête : « Note de synthèse — **point de fin de chantier** ». Première ligne : avancement **31,15 %** ; `suivi.date_arret` : **j 84 sur 599,84**, soit 14 % du délai. Les onze lignes appartiennent à cinq documents différents (situation mensuelle, rapport qualité, plan de levage, bilan déchets, note de réclamation) ; aucun conducteur de travaux n'écrit « Contrôle d'ordre de grandeur : part de main-d'œuvre du déboursé — hors fourchette 15 à 30 % : ALERTE » dans une colonne « Valeur annoncée ». Il manque, sans quoi plusieurs lignes ne veulent rien dire : la **date** d'arrêt, le **montant du marché** (indispensable à E1), le **périmètre** (chantier entier ? zone ?) et la **clause de pénalité**. | Retitrer « Point d'avancement mensuel n° 4 — situation au j 84 » ; ajouter un cartouche de trois lignes (date, marché, périmètre, référence CPS) ; réécrire les intitulés en langue de chantier. Le cartouche rend E1 et E5 trouvables (M1, M7) : c'est la même correction. |
| **M7 · La difficulté est bimodale : trois erreurs sont avouées par leur propre intitulé, deux sont indécidables sans les sorties internes.** | majeur | Avouées : L2 « Avancement global, **moyenne des avancements des 27 tâches** » (l'erreur est son nom) ; L8 « Retard de chantier si la reprise immobilise le levage **7 jours** » → « 7 jours » ; L3 « **obtenue en divisant le tonnage restant par la cadence** ». Indécidables : E1 (M1) et E5, qui demande de connaître la marge de 436 j du noyau, publiée dans C7 et absente du dossier. | Retirer la méthode des intitulés de L2, L3 et L8 — un dossier à corriger ne dit pas comment il a calculé. Donner dans le dossier, pour E5, la ligne qui rend la déduction possible : une ligne de planning ou une colonne « marge » sur les ouvrages cités. Le dossier doit être auto-suffisant : c'est la condition pour qu'un lecteur qui n'a pas écrit le cours puisse réussir. |
| **M8 · Trois des six bloquants étaient à portée d'un test de règle qui n'existe pas.** | majeur | `calc/tests/test_revue.py` : (a) aucun test ne vérifie que le champ `source` d'une ligne désigne le fichier et la clé réellement lus — ce test seul attrapait **B1**, et le test § 3 **épingle** au contraire la mauvaise source ; (b) aucun test ne recalcule `ce_qu_elle_coute` ni ne contrôle son unité contre celle de la source — il attrapait **B5** et **B2** ; (c) `ou_le_cours_l_a_commise` n'est contrôlé que par `len(...) > 30`, donc **B3** et **B4** (309/79, « aucun contrôle automatique », D-045, D-056) ne sont vérifiés par rien. | Trois tests de règle : `source` → fichier+clé effectivement lus ; `ce_qu_elle_coute` → recalculé depuis `valeur` et `juste`, et son unité tirée de la source ; toute affirmation historique → un script qui recompte `QA/` et compare. Le troisième est le plus important : c'est le seul endroit du cours où des nombres sont écrits à la main (§ 4.3). |
| **M9 · L'exception nommée de E4 épingle un identifiant, pas une règle (D-041, D-043).** | majeur | `test_revue.py` : `_SANS_ECART = {"E4": "…"}`. Si une future erreur à écart nul apparaissait, le test échouerait sans raison ; si E4 cessait d'être celle à écart nul, l'exemption la couvrirait en silence. Le module s'en prévaut pourtant comme d'une vertu : « un test du module la déclare comme une exception nommée, au lieu de la laisser passer en silence ». `STATE.md` : « deux fois — C3 puis B3e — un test épinglait la conclusion narrative au lieu de la règle. Un test vérifie une règle, jamais un résultat raconté. » | Règle à la place de l'identifiant : *toute* erreur dont l'écart est nul **doit** porter `_le_piege_dans_le_piege` **et** un verdict dans son `affiche` ; toute erreur dont l'écart est non nul **ne doit pas** porter `_le_piege_dans_le_piege`. Le test devient vrai pour n'importe quel dossier, et l'exception n'est plus une liste. |
| **M10 · `D-058` ne décrit pas le module qu'il justifie.** | majeur | D-058 : « **Quatre** lignes justes servent d'appâts » — `calc/revue.py` en définit **trois** (L9, L10, L11), et le module titre « Les **trois** appâts ». D-058 : « depuis les sorties réelles des **neuf** modules du palier » — `revue.py` lit **sept** fichiers. D-058 reprend aussi « dix passes, 309 défauts, 79 bloquants » (B4). Une décision qui décrit mal son impact ne sert plus de preuve. | Aligner D-058 sur le code : trois appâts, sept sorties, 16 passes / 434 défauts / 93 bloquants, et un contre-exemple nommé pour la phrase sur les contrôles automatiques. |

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **m1 · Formats décimaux hétérogènes sur la figure.** | mineur | Capture : « −28,6 », « −75,1 », « 84,3 », « 533,3 », « 687,2 » — mais « **−65** » et « **0** ». | Un seul format, une décimale (§ 3.6). |
| **m2 · L'axe de la figure ne porte qu'une graduation.** | mineur | Capture : un seul repère, « 0 ». Aucune échelle : les valeurs ne sont lisibles que par les étiquettes des barres. | Trois à cinq graduations, ou assumer la figure comme un tableau ordonné. |
| **m3 · Fiche mémo, ligne 7 : la question et la famille ne se répondent pas.** | mineur | La question dit « Cet ouvrage a-t-il de la **marge** ? », la colonne famille dit « coût inventé » (nom du symptôme) ; les six autres lignes font écho mot pour mot. **Pour le reste la fiche est juste** : sept familles, aucun doublon, aucun manque, ordre identique à celui du § S2 — vérifié ligne à ligne. | Renommer la famille de E5 « coût imputé à un ouvrage à marge », ou reformuler la question. |
| **m4 · L'ordre du corrigé n'est pas l'ordre des sept questions.** | mineur | § S2 et fiche mémo : calendrier, condition, unité, domaine, dénominateur, mesuré/déduit, marge. § S4 : E1, E2, E3, E4, **E5 (marge)**, E6 (dénominateur), E7. Le lecteur qui applique la méthode rencontre les familles dans le désordre. | Renuméroter le corrigé dans l'ordre des questions, ou renvoyer explicitement chaque exercice à son numéro de question. |
| **m5 · « Six passes sur dix y ont trouvé un défaut » (captures) : invérifiable.** | mineur | Les 16 rapports de `QA/` mentionnent tous des figures ou des captures (comptage : de 3 à 23 occurrences chacun). Aucun critère ne permet de retrouver « six sur dix ». | Compter les défauts dont la preuve est une capture, et publier ce nombre — ou écrire « toutes les passes ». |
| **m6 · § S4g, E7 : le seul passage de la section qui ne soit pas étayé.** | mineur | « La promesse se rattrape toujours au même endroit — la nuit, sur la voie » ne renvoie à aucune sortie. Le reste de S4g **l'est** : la cascade de E3 s'appuie sur B7c et sur `qualite.criticite` (« Électrisation à proximité de la caténaire · consignation par agent habilité, vérification d'absence de tension »), et D-050 fournit le mécanisme (« avant la fenêtre tout se joue sur quelques heures »). Aucun retour d'expérience n'est inventé (R8 respectée). | Rattacher la phrase à `qualite.criticite` et à `impact_planning_bornes`, ou l'écrire comme ce qu'elle est : une règle professionnelle, pas un constat. |
| **m7 · La « mutation » de E4 n'en est pas une.** | mineur | `revue.py` : pour E4, `valeur == juste == part_mo` ; ce qui est muté est le **libellé** (ajout de « — hors fourchette 15 à 30 % : ALERTE »). Le § S1 annonce pourtant « sept d'entre elles sont mutées par une fonction déclarée ». | Écrire « six valeurs sont mutées, la septième est **étiquetée** » — c'est plus intéressant, et c'est la définition même de l'erreur de lecture. |

**Compte : 6 bloquants · 10 majeurs · 7 mineurs — 23 défauts.**

---

## 3. Grille d'auto-évaluation § 7.2

Notée pour ce qu'est ce module — une **revue**, pas un module de calcul : « formules justifiées »
se lit comme « le mécanisme de fabrication et de correction est démontré », et « exemple vérifié »
comme « le corrigé dit vrai ».

| # | Critère | Note | Justification |
|---|---|---:|---|
| 1 | Le « pourquoi » est expliqué | **3** | Le § S2 (sept questions sur une grandeur, pas sur une addition) est la meilleure page du module ; le parti pris des erreurs réellement commises est argumenté et tenu. |
| 2 | Les hypothèses sont explicites | **1** | Aucune borne (M2) ; aucun calendrier déclaré pour la pénalité alors que tout E1 en dépend (M1) ; ni date, ni marché, ni périmètre dans la note (M6). Le module demande au lecteur ce qu'il ne fait pas lui-même. |
| 3 | Les formules sont justifiées | **2** | La fonction de mutation est déclarée et la bijection testée — c'est la bonne méthode. Mais l'exception E4 épingle un identifiant (M9) et trois tests de règle manquent (M8). |
| 4 | L'exemple est vérifié | **1** | Sur sept « ce qu'elle coûte », trois sont faux (E3 unité, E6 repère, E4 substance) ; une « valeur juste » sur sept est fausse (B2) ; un appât sur trois est faux (B1) ; et deux affirmations historiques sur deux sont fausses (B3, B4). Dans un module qui enseigne la relecture, c'est le critère qui coûte le plus. |
| 5 | Le piège est identifié | **3** | Le « piège dans le piège » de E4, les trois appâts, et le § sur le faux positif (« un relecteur qui barre tout est inutilisable ») sont du vrai métier de contrôle. |
| 6 | Le lien avec l'exécution est fait | **3** | Le § S4g est précis et rattaché : consignation, vérification d'absence de tension, marge de restitution, travail de nuit. Il ne verse pas dans la rhétorique sauf sur une phrase (m6). |
| 7 | Le lien avec le coût et le délai est fait | **2** | Chaque erreur est chiffrée en MAD et en jours, et E7 l'est par régime — exemplaire. Mais E3 et E6 chiffrent faux, et rien n'est borné. |

**Total : 15 / 21. Deux critères sous le minimum de 2 (§ 7.2) : la grille échoue.**

---

## 4. Verdict

**Non livrable.** Six bloquants, dont quatre portent sur le corrigé et sur le bilan du palier —
c'est-à-dire sur les deux seuls endroits où ce module parle en son nom propre.

Le parti pris est bon et mérite d'être défendu : planter les erreurs que le cours a réellement
commises, les fabriquer par une fonction déclarée depuis les sorties réelles, et tester la
bijection entre les lignes fausses et le corrigé. Rien de cela n'est à refaire.

Mais un dossier à corriger a une obligation que les autres modules n'ont pas, et le module l'écrit
lui-même : **« un corrigé qui dérive apprend une erreur de plus »**. Ici il dérive quatre fois.

1. **Le corrigé se trompe sur deux de ses sept valeurs** : E6 compare la moyenne non pondérée à un
   nombre qui n'est pas la moyenne pondérée des mêmes tâches (34,01 % et non 31,15 %), et E3 chiffre
   en « jours de chantier » un écart que sa propre source déclare en plages de consignation, ce qui
   minore de 6,5 fois le manque au planning. Les deux fautes sont **celles des familles qu'elles
   corrigent** : un dénominateur qui change sans le dire, une unité qui change sans le dire.
2. **Un appât donne tort au relecteur qui a raison.** Le CPI de L11 n'est pas celui de D4 ni celui
   de la date d'arrêt : c'est celui d'un plancher de mezzanine. Un lecteur qui le signale fait
   exactement ce que le module lui demande, et le corrigé le déclare en faute. C'est le défaut le
   plus grave qu'un dossier à corriger puisse porter.
3. **E4 apprend à classer sans suite une alerte réelle.** La dette n° 10 du dépôt dit que le ratio
   reste hors fourchette sur sa base définie, d'un facteur ×1,92 « confirmé, chiffré, non soldé ».
   Le corrigé écrit « n'a rien d'anormal ».
4. **Le bilan du palier est faux dans les deux affirmations qu'il met en gras.** « 309 défauts dont
   79 bloquants » n'est reconstructible depuis aucun comptage (`STATE.md` en donne 434 et 93, sur
   16 passes et non dix), et « aucun bloquant trouvé par un contrôle automatique » est démenti par
   `QA/B3e-passe1.md` (B-2b, trouvé par un canari), par `STATE.md` (« deux d'entre eux ont trouvé
   seuls une erreur que la passe n'avait pas vue ») et par le tableau du § S5 lui-même, trois lignes
   plus haut. Ce dépôt a déjà classé majeur un bilan de `STATE.md` qui surestimait ce qui était
   acquis (`QA/TV-tranche-verticale-passe5.md`, M10) ; la même règle s'applique ici, et plus
   durement, parce que c'est le module qui enseigne à ne pas croire un bilan.

À quoi s'ajoute une question d'exercice, et elle est centrale : **un lecteur qui n'a pas écrit ce
cours ne peut pas réussir ce dossier.** Trois erreurs sont avouées par leur propre intitulé, deux
sont indécidables sans les sorties internes — E1 parce que ni le calendrier ni le montant du marché
ne figurent nulle part, E5 parce que la marge du noyau est dans C7 et pas dans la note. Le dossier
doit être auto-suffisant ; un cartouche de trois lignes et le retrait des méthodes des intitulés y
suffiraient (M6, M7).

Sur les deux points que la consigne demandait de trancher :

- **Bornes (D-049)** : les bornes ne doivent **pas** figurer sur les lignes du dossier — elles
  désigneraient les lignes instrumentées et détruiraient l'exercice. Elles sont **obligatoires dans
  le corrigé**, et leur absence y est aujourd'hui une fausse précision caractérisée : la valeur
  juste de E5 est connue à un facteur 20 près, et son « +533 % » va de +40 % à +5 197 % sur les
  bornes publiées par C7. Le cas de E7 est l'exception à montrer, pas à taire : 20 j est un palier
  mesuré, invariant sur toute la fourchette (D-050).
- **E4 et son exception** : E4 est une **vraie** erreur plantée, et la meilleure idée du dossier —
  un chiffre juste, une comparaison fausse. Ce n'est pas une facilité. En revanche le test qui
  l'exempte est une échappatoire de forme : il nomme l'identifiant « E4 » au lieu de la propriété
  « écart nul ⇒ explication obligatoire ». La règle existe, elle est écrite en commentaire ; il
  suffit de la coder.

**Reprise demandée** : les six bloquants, puis les majeurs M1, M2, M6, M7, M8 (qui rouvriraient
trois bloquants s'ils n'étaient pas traités). Nouvelle passe ensuite, par une session distincte,
avec un **canari** : fausser la `source` d'une ligne juste et vérifier que les tests rougissent.
Aujourd'hui ils ne rougissent pas — c'est ainsi que B1 est passé.
