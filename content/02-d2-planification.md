---
id: D2
titre: Planification d'un chantier de gare
fil: Palier 1 · module 1 — direction de projet
resume: Vingt-sept tâches, trois familles de durées, et une fenêtre de consignation qui coupe le chemin critique en deux. Le planning d'un chantier ferroviaire se calcule ; il ne s'estime pas.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · toutes les valeurs numériques sont V3
pied: Exemple pédagogique — ne remplace ni un planning d'exécution visé ni l'analyse de délai d'un expert.
donnees: planification, tranche-plancher, gare
---

## S1 · Ce que ce module fait, et ce qu'il ne refait pas

Vous connaissez le CPM. Ce module ne vous réapprend ni le parcours avant/arrière, ni la définition
d'une marge, ni comment lire un Gantt. Il fait trois choses que le référentiel générique de gestion
de projet ne fait pas, et qui décident de la justesse d'un planning de bâtiment ferroviaire :

1. il **calcule** les durées au lieu de les estimer, et il montre que toutes ne se calculent pas de
   la même façon — ni ne se pilotent de la même façon ;
2. il traite les **fenêtres de consignation** de l'exploitant comme ce qu'elles sont : des
   contraintes dures qui déplacent le chemin critique ;
3. il distingue le **planning de travail** du **planning contractuel**, qui ne sont pas le même
   objet et n'engagent pas les mêmes choses.

Le module TV a suivi **une zone de plancher**. Celui-ci prend le **chantier entier** : la zone y
devient une tâche sur vingt-sept. La méthode ne change pas ; l'échelle, si.

**Prérequis** : le module TV (d'où vient la durée du plancher de mezzanine). **Place dans le
projet** : étape 8 du déroulé du cas phare (§ 10.2) ; D1, D3, D4 et D7 s'y accrochent.

## S2 · L'idée centrale : une durée n'est pas une durée

Le réflexe du planificateur pressé est de traiter toutes les barres du Gantt de la même façon.
C'est l'erreur qui coûte le plus cher, parce qu'elle conduit à mettre des moyens là où ils ne
produisent rien. Les {{planification.familles.nb_taches.calculee}} + {{planification.familles.nb_taches.imposee}} + {{planification.familles.nb_taches.declaree}} tâches de ce chantier
appartiennent à **trois familles**, et une seule obéit aux effectifs.

| Famille | D'où vient la durée | Ce qui la raccourcit | Nombre ici |
|---|---|---|---:|
| **Calculée** | quantité ÷ (cadence × ateliers) | plus d'ateliers, meilleure cadence | {{planification.familles.nb_taches.calculee}} |
| **Imposée** | la physique ou un tiers : séchage, fabrication, visa | **rien** — seulement anticiper le départ | {{planification.familles.nb_taches.imposee}} |
| **Déclarée** | une hypothèse, faute de quantité à diviser | rien tant qu'elle n'est pas transformée en calculée | {{planification.familles.nb_taches.declaree}} |

Et ces trois familles ne suffisent pas à décomposer une durée de projet : il en manque deux, que
le § S4a introduira — l'**attente** d'une fenêtre de consignation, et l'**immobilisation** entre deux
fenêtres. Le compte complet, le long du chemin critique de ce chantier, est le tableau de S4f. Sa
ligne importante est celle-ci :
**{{planification.decomposition_du_chemin.part_que_les_effectifs_ne_touchent_pas_pct::n1}} %** de la
durée du projet — durées imposées, attente et immobilisation réunies — sont **hors d'atteinte des
moyens**. Doubler tous les effectifs du chantier ne les touche pas d'un jour. C'est le genre de
phrase qu'il faut pouvoir dire en réunion avec le calcul derrière.

:::figure {"fn":"wbs","args":"planification.figures.wbs","titre":"Organigramme des tâches (WBS), coloré par famille de durée","num":1,"large":true,"options":{"racine":"Gare voyageurs — chantier"},"voir":["La couleur n'est pas décorative : vert = durée calculée, brique = durée imposée, gris = durée déclarée. Un planning dont les barres brique sont sur le chemin critique ne s'accélère pas avec des hommes.","Le lot 4 (charpente) porte deux durées imposées à la suite — études puis fabrication — avant la moindre heure de chantier.","Les durées déclarées et les durées calculées sont à égalité en nombre — {{planification.familles.nb_taches.declaree::n0}} contre {{planification.familles.nb_taches.calculee::n0}} — mais pas en enjeu : une durée déclarée se transforme en durée calculée dès que sa quantité arrive."],"erreur":"Produire un WBS qui décalque l'organigramme de l'entreprise plutôt que le découpage physique de l'ouvrage. Un WBS sert à accrocher des quantités et des coûts à des tâches, pas à nommer des services."}
:::

## S3 · Principes : d'où sortent les vingt-sept durées

### a. Les durées calculées

Même formule qu'au module TV, à l'échelle de l'atelier :

$$ d = \frac{Q}{c \times n} $$

où $Q$ est la quantité, $c$ la cadence **d'atelier** et $n$ le nombre d'ateliers en parallèle.
L'unité le dit : une cadence d'atelier est en m³/j ou en m²/j, jamais en m³/j/compagnon. Confondre
les deux est l'erreur d'unité la plus commune de la planification, et elle se voit à l'œil nu :
elle produit des durées huit fois trop courtes.

Trois cadences méritent qu'on s'arrête sur leur **moteur**, parce que c'est là que les plannings
d'ordre de grandeur se trompent :

| Tâche | Ce qui pilote vraiment | Pourquoi pas le volume |
|---|---|---|
| Semelles isolées | le **nombre** de semelles ⟦V3|cadence de semelles isolées|4 unités/jour/atelier|u/j|2,5 à 6|2026|cycle complet : implantation, coffrage bois, cage, coulage⟧ | implanter, coffrer et ferrailler une petite semelle prend presque le temps d'une grande |
| Radier et plancher plein | la **surface** ⟦V3|cadence de dalle pleine|120 m²/jour/atelier|m²/j|80 à 180|2026|cycle complet coffrage-ferraillage-coulage, hors cure⟧ | le coffrage et le ferraillage se mesurent au m², le coulage est une demi-journée |
| Poteaux de 9 m | le **nombre** ⟦V3|cadence de poteaux de grande hauteur|3 unités/jour/atelier|u/j|2 à 5|2026|coffrage grimpant, étaiement, travail en hauteur⟧ | la hauteur impose un cycle par unité, quel que soit le volume |

Le chantier compte {{planification.quantites.n_poteaux}} poteaux de
{{planification.quantites.hauteur_poteau_rdc_m::n1}} m, déduits de la trame : quatre files
longitudinales sur {{gare.geometrie.nb_travees_longitudinales}} travées de
{{gare.geometrie.trame_longitudinale_m::n2}} m. Aucun de ces nombres n'est saisi.

### b. Les durées imposées

Trois tâches ne répondent à aucun effectif :

| Tâche | Durée | Ce que c'est |
|---|---:|---|
| Études, visa et approbation de la charpente | {{planification.durees.CHET.duree_j::n0}} j | ⟦V3|délai d'études et de visa d'une charpente|40 jours|j|25 à 60|2026|plans d'exécution, note de calcul, visa de la maîtrise d'œuvre, approbation⟧ |
| Fabrication en atelier | {{planification.durees.CHFA.duree_j::n0}} j | ⟦V3|délai de fabrication d'une charpente en atelier|60 jours|j|45 à 90|2026|débit, soudage, contrôles non destructifs, galvanisation, transport⟧ |
| Séchage avant second œuvre | {{planification.durees.SECH.duree_j::n0}} j | ⟦V3|séchage du gros œuvre avant second œuvre|20 jours|j|14 à 30|2026|avant chapes et cloisons⟧ |

Ces trois-là totalisent {{planification.familles.somme_des_durees_j.imposee::n0}} jours et sont
**toutes sur le chemin critique**. Le seul levier qui existe sur elles est le **départ** : lancer les
études de charpente le premier jour du chantier, et non quand le gros œuvre est fini.

:::encart {"genre":"alerte","titre":"Le résultat le plus contre-intuitif de ce module : un chemin critique coupé en deux"}
Le plus long chemin de ce réseau compte
{{planification.reseau.chemin_critique.length::n0}} tâches, de
**{{planification.reseau.chemin_critique.0}}** à **{{planification.reseau.chemin_critique.14}}**.
Mais les tâches à **marge nulle** ne sont que
{{planification.reseau.nb_taches_critiques::n0}} :
**{{planification.reseau.contre_calcul_cpm.chemin_en_aval_de_la_contrainte.0}} →
{{planification.reseau.contre_calcul_cpm.chemin_en_aval_de_la_contrainte.1}} →
{{planification.reseau.contre_calcul_cpm.chemin_en_aval_de_la_contrainte.2}} →
{{planification.reseau.contre_calcul_cpm.chemin_en_aval_de_la_contrainte.3}} →
{{planification.reseau.contre_calcul_cpm.chemin_en_aval_de_la_contrainte.4}} →
{{planification.reseau.contre_calcul_cpm.chemin_en_aval_de_la_contrainte.5}}**.

Les deux ensembles ne coïncident pas, et ce n'est pas une anomalie de calcul : c'est la signature
d'un planning **sous fenêtres**. La tâche {{planification.reseau.contre_calcul_cpm.taches_contraintes_actives.0}}
est **épinglée** au jour {{planification.consignations.CHLV.debut::n0}}, celui de sa consignation.
En amont de cette épingle, la durée des tâches ne commande plus rien : elles finissent toutes avant,
et reçoivent de la marge. En aval, la chaîne redevient critique au sens ordinaire.

Ce que cela change dans votre travail, et c'est vérifiable sur les variantes du § S4e : faire
travailler **trois ateliers de poteaux au lieu de deux** raccourcit la tâche de
{{planification.exercices.gain_poteaux_j::n2}} jours et le projet de **zéro**. Le point de suivi
hebdomadaire sur l'avancement du gros œuvre est rassurant et **ne dit presque rien du délai** ; les
deux points qui le disent sont la date de consignation obtenue de l'exploitant et l'avancement des
études et de la fabrication de charpente, qui doivent être prêtes **avant** cette date.
:::

### c. Le contre-calcul, et pourquoi il en faut un second

La durée du réseau est calculée **deux fois** par `calc/cpm.py` : parcours avant/arrière contre
énumération exhaustive des chemins —
{{planification.reseau.contre_calcul_cpm.voie_A_parcours_avant_arriere_j::n2}} j contre
{{planification.reseau.contre_calcul_cpm.voie_B_enumeration_des_chemins_j::n2}} j.

Mais ces deux voies **partagent le réseau**. Si un lien est faux, elles se trompent ensemble. D'où un
**second contre-calcul, hors CPM** : on additionne à la main les durées et les décalages du chemin
annoncé critique, et on vérifie que la somme rend bien la durée du projet —
{{planification.reseau.contre_calcul_chemin.somme_du_chemin_j::n2}} j contre
{{planification.reseau.contre_calcul_chemin.duree_du_reseau_j::n2}} j :
*{{planification.reseau.contre_calcul_chemin.verdict}}*. Ce contrôle attrape une erreur que les deux
autres ne voient pas : un chemin critique publié qui ne porte pas la durée annoncée.

## S4 · Étude de cas : le planning de la gare

### a. Le réseau, et ce que les fenêtres lui font

Une gare se construit **à côté d'une voie exploitée**. Les tâches qui la surplombent ou la coupent
ne se font pas quand le planning le voudrait : elles se font quand l'exploitant **consigne**. Deux
tâches sont dans ce cas ici — le levage des treillis au-dessus de la voie, et le raccordement du
passage souterrain.

Les fenêtres déclarées : ⟦V3|durée d'une fenêtre de consignation|3 jours ouvrés consécutifs|j|2 à 5|2026|consignation accordée par l'exploitant⟧,
tous les ⟦V3|période entre deux consignations|20 jours ouvrés|j|15 à 30|2026|une fenêtre par mois calendaire environ, demandée six mois à l'avance⟧.

Une fenêtre agit sur une tâche de **deux** façons, et il faut les tenir séparées :

1. elle l'**étale** — le travail se fait par tranches, une par consignation ;
2. elle la **décale** — la tâche ne peut pas commencer avant la première fenêtre disponible, même
   si le réseau, lui, serait prêt plus tôt.

| | Travail réel | Prêt au réseau | Fenêtre retenue | Attente | Étalement | Fenêtres | Immobilisation |
|---|---:|---:|---:|---:|---:|---:|---:|
| Levage au-dessus de la voie | {{planification.consignations.CHLV.duree_de_travail_j::n2}} j | j {{planification.consignations.CHLV.debut_du_reseau_nu::n0}} | **j {{planification.consignations.CHLV.debut::n0}}** | {{planification.consignations.CHLV.attente_avant_premiere_fenetre_j::n2}} j | **{{planification.consignations.CHLV.etalement_j::n2}} j** | {{planification.consignations.CHLV.nb_fenetres}} | {{planification.consignations.CHLV.immobilisation_improductive_j::n0}} j |
| Raccordement du passage souterrain | {{planification.consignations.PSOU.duree_de_travail_j::n2}} j | j {{planification.consignations.PSOU.debut_du_reseau_nu::n0}} | j {{planification.consignations.PSOU.debut::n0}} | {{planification.consignations.PSOU.attente_avant_premiere_fenetre_j::n2}} j | {{planification.consignations.PSOU.etalement_j::n2}} j | {{planification.consignations.PSOU.nb_fenetres}} | {{planification.consignations.PSOU.immobilisation_improductive_j::n0}} j |

**Le chantier passe de {{planification.reseau.duree_sans_contrainte_j::n0}} à
{{planification.reseau.duree_avec_fenetres_j::n0}} jours ouvrés** — soit
**{{planification.reseau.surcout_de_delai_j::n0}} jours, {{planification.reseau.surcout_de_delai_pct::n1}} %** — à cause de
**{{planification.consignations.CHLV.duree_de_travail_j::n0}} jours de travail**. Il n'y a pas
d'erreur : le levage ne dure pas plus longtemps. Il attend
{{planification.consignations.CHLV.attente_avant_premiere_fenetre_j::n1}} jours sa première fenêtre,
puis il **s'étale** sur {{planification.consignations.CHLV.nb_fenetres}} consignations. La
distinction est capitale, parce que le **coût** suit la durée de travail tandis que le **délai** suit
l'attente et l'étalement, et parce que ni l'une ni l'autre ne se résorbe avec des moyens.

:::encart {"genre":"note","titre":"Ce que la première version de ce calcul faisait, et ce que cela a coûté"}
La première version de ce module calculait la date de la fenêtre, la publiait dans ses sorties — et
laissait quand même la tâche démarrer à la date du réseau. Elle n'appliquait que l'effet n° 1.
Résultat : {{planification.consignations.CHLV.attente_avant_premiere_fenetre_j::n1}} jours ouvrés
perdus et une date contractuelle fausse d'environ un mois. La thèse du module — « le chemin critique
d'un chantier ferroviaire, c'est le réseau **plus** les fenêtres » — n'était implémentée qu'à moitié,
et aucun des seize contrôles automatiques ne le voyait : les deux voies du CPM, qui partagent le
réseau, se trompaient ensemble, et le test de recette comparait la fenêtre à elle-même.

Ce qui l'a trouvé est une **contre-expertise à l'aveugle** : un relecteur qui refait le CPM depuis
`data/` seul, sans lire le code, et qui compare deux nombres du même fichier de sortie — la date de
début publiée dans `durees` et celle publiée dans `consignations`. Ils différaient de
{{planification.consignations.CHLV.attente_avant_premiere_fenetre_j::n1}} jours. La contrainte passe
maintenant par le moteur de CPM lui-même (`Tache.au_plus_tot`), elle est étalonnée sur cinq cas à
solution connue, et un garde-fou lève si une tâche consignée démarre ailleurs que sur sa fenêtre.
:::

Trois leviers existent, et un seul est bon marché : négocier une fenêtre plus longue, réduire la part
levée au-dessus de la voie (pré-assemblage au sol, levage par l'autre côté), ou installer une
protection de voie qui supprime la consignation pour une partie des opérations. L'exercice 3 les
chiffre.

:::figure {"fn":"reseau","args":"planification.figures.reseau","titre":"Réseau de la chaîne critique : charpente, couverture et finitions","num":2,"large":true,"voir":["Le réseau publié ici est la partie qui porte le délai — douze tâches sur {{planification.familles.nb_taches.calculee::n0}} + {{planification.familles.nb_taches.declaree::n0}} + {{planification.familles.nb_taches.imposee::n0}} : un PERT illisible n'est pas un PERT.","CHET et CHFA — études et fabrication de la charpente — sont deux durées IMPOSÉES enchaînées, et elles démarrent au jour zéro du chantier. Les décaler d'une semaine décale la livraison d'une semaine, et aucun effectif ne les rattrape.","Les boîtes brique sont à marge nulle, les grises portent leur marge en clair. Remarquez où la couleur bascule : à CHLV, la tâche épinglée par sa fenêtre de consignation. Tout ce qui est à sa gauche a de la marge ; tout ce qui est à sa droite n'en a plus."],"erreur":"Afficher un réseau de cent tâches « pour être complet ». Un réseau sert à montrer une structure de dépendances ; au-delà d'une vingtaine de nœuds, il ne montre plus rien et c'est le Gantt qui prend le relais."}
:::

### b. Le Gantt, et la lecture des marges

:::figure {"fn":"gantt","args":"planification.figures.gantt","titre":"Gantt du chantier — les barres brique sont critiques","num":3,"large":true,"voir":["Les barres de la charpente démarrent au jour zéro : ce sont les études, pas des travaux. Un Gantt qui ne les porte pas est un Gantt qui ment sur la date de livraison.","Le plancher de mezzanine — tout le module TV — est une barre parmi vingt-sept, et elle n'est pas critique.","Les deux barres de consignation sont dessinées PLEINES, comme les autres, et c'est une limite de ce Gantt : une barre représente l'étalement, pas le travail. Pour le levage, {{planification.consignations.CHLV.etalement_j::n0}} jours de barre portent {{planification.consignations.CHLV.duree_de_travail_j::n1}} jours de travail. Le tableau du § S4a donne la décomposition que le dessin ne porte pas."],"erreur":"Lire un Gantt comme un calendrier de travaux. Une barre longue n'est pas forcément une tâche lourde : elle peut être une tâche courte qui attend une fenêtre — et le Gantt ne le dit pas, il faut aller chercher le chiffre."}
:::

Deux marges, et elles ne se dépensent pas de la même façon :

- la **marge totale** est le retard qu'une tâche peut prendre sans décaler la **fin du projet** ;
  elle appartient au chantier, et la consommer décale les successeurs ;
- la **marge libre** est le retard qu'elle peut prendre sans décaler **la moindre tâche** ; c'est la
  seule qu'un conducteur de travaux puisse dépenser sans rien demander à personne.

Sur ce chantier, le plancher de mezzanine porte
{{planification.durees.MEZZ.marge_totale_j::n1}} j de marge totale et
{{planification.durees.MEZZ.marge_libre_j::n1}} j de marge libre. Les noyaux et escaliers, eux, en
portent {{planification.durees.NOYX.marge_totale_j::n0}} et
{{planification.durees.NOYX.marge_libre_j::n0}} : ce sont des tâches qu'on peut déplacer presque
librement — et c'est précisément pour cela qu'elles servent au lissage.

### c. Les tâches répétitives : la ligne d'équilibre

Le plancher de mezzanine est répétitif : {{tranche-plancher.planning_plancher.nb_zones}} zones
identiques à {{tranche-plancher.planning_plancher.cadence_zone_j::n1}} j/zone. Sur un Gantt, cela
fait huit barres décalées, et on n'y voit rien. Sur une **ligne d'équilibre**, cela fait deux droites
dont la **pente est la cadence**.

:::figure {"fn":"ligneEquilibre","args":"planification.figures.ligne_equilibre","titre":"Ligne d'équilibre du plancher de mezzanine","num":4,"large":true,"voir":["La pente des deux droites est la cadence : une zone tous les {{tranche-plancher.planning_plancher.cadence_zone_j::n1}} jours. Un fléchissement de pente est un retard de cadence, visible avant d'avoir coûté.","L'épaisseur entre les deux droites est le cycle d'une zone : c'est le nombre de zones ouvertes en même temps, donc le coffrage immobilisé.","Deux droites de métiers différents qui se rapprochent annoncent une collision d'équipes. Le Gantt ne la montre qu'une fois arrivée."],"erreur":"Suivre des tâches répétitives au Gantt. Huit barres identiques ne disent pas si la cadence tient ; une droite, si."}
:::

### d. Les ressources : lisser, et ce que le lissage coûte

L'effectif présent chaque jour est la somme des tâches **en cours de travail**. La nuance compte :
une tâche consignée ne mobilise personne entre deux fenêtres, et la compter sur tout son étalement
dimensionnerait une base-vie pour des gens qui ne sont pas là. L'histogramme est donc bâti sur les
**segments de travail**, pas sur les barres du Gantt.

Brut, il monte à **{{planification.ressources.pointe_avant}} personnes** pour une moyenne de
{{planification.ressources.moyenne_avant::n1}} sur les
{{planification.ressources.jours_travailles_avant::n0}} jours travaillés : une pointe que la
base-vie, les vestiaires et le parking doivent encaisser pour quelques jours.

**Lisser** consiste à décaler les tâches non critiques **dans leur marge libre**, sans changer aucune
durée, aucune date de fin, et sans repousser le début d'aucun successeur. Le choix de la marge
**libre** et non de la marge totale n'est pas un détail : dans la marge totale, une tâche se décale
sans toucher la fin du projet mais en repoussant son successeur, et l'histogramme publié décrit alors
un planning que le reste du module ne décrit plus.

Résultat ici : pointe ramenée à **{{planification.ressources.pointe_apres}}**, soit
**{{planification.ressources.gain_de_pointe_pct::n1}} % de moins**, en décalant
{{planification.durees.MEZZ.nom}} de {{planification.ressources.decalages_utilises_j.MEZZ::n0}} jours.

Ce que le lissage conserve, et ce qu'il ne conserve pas :

| Grandeur | Avant | Après |
|---|---:|---:|
| Pointe | {{planification.ressources.pointe_avant}} | **{{planification.ressources.pointe_apres}}** |
| Jours-hommes de travail | {{planification.ressources.jours_hommes_avant::n0}} | {{planification.ressources.jours_hommes_apres::n0}} |
| Jours travaillés | {{planification.ressources.jours_travailles_avant::n0}} | {{planification.ressources.jours_travailles_apres::n0}} |
| Moyenne sur les jours travaillés | {{planification.ressources.moyenne_avant::n1}} | {{planification.ressources.moyenne_apres::n1}} |

Les **jours-hommes sont identiques** — le calcul lève une erreur s'ils ne le sont pas : lisser
déplace du travail, il n'en supprime aucun. La **moyenne baisse pourtant**, et ce n'est pas une
contradiction : le même travail s'étale désormais sur plus de jours travaillés. C'est une moyenne à
dénominateur variable, et c'est la raison pour laquelle on ne pilote pas un effectif à la moyenne.

Le prix : **{{planification.ressources.marge_totale_consommee_j::n0}} jours de marge libre
consommés**. C'est le vrai sujet, et il est rarement posé. Une marge dépensée en confort
d'exploitation n'est plus disponible pour l'aléa. La question n'est donc pas « peut-on lisser ? »
mais « **la pointe était-elle infaisable ?** ». Si la base-vie tient
{{planification.ressources.pointe_avant}} personnes, le lissage est un luxe payé en marge.

:::figure {"fn":"histogramme","args":"planification.figures.effectifs","titre":"Effectif présent, brut et après lissage","num":5,"large":true,"options":{"serie2":{"$":"planification.figures.effectifs_lisses"},"moyenne":{"$":"planification.ressources.moyenne_avant"},"libelle_moyenne":"moyenne sur les jours travaillés","nom1":"avant lissage","nom2":"après lissage"},"voir":["Le contour brique est l'effectif après lissage : la pointe tombe de {{planification.ressources.pointe_avant}} à {{planification.ressources.pointe_apres}}, et l'aire sous la courbe ne change pas — on n'a pas supprimé du travail, on l'a déplacé.","Le trait vert tireté est la moyenne sur les jours travaillés, {{planification.ressources.moyenne_avant::n1}} personnes, calculée par `calc/` et non par le dessin : c'est la même définition que celle du tableau ci-dessus.","C'est la pointe, et non la moyenne, qui dimensionne la base-vie, le parking et les réfectoires."],"erreur":"Niveler au lieu de lisser sans le dire. Lisser déplace des tâches dans leur marge et ne change pas la fin ; niveler plafonne l'effectif et ALLONGE le projet. Les deux mots désignent deux décisions différentes."}
:::

### e. Du planning de travail au planning contractuel

Les {{planification.reseau.duree_avec_fenetres_j::n0}} jours ci-dessus sont des **jours ouvrés**.
Un marché, lui, s'engage sur des **dates**. Entre les deux, deux conversions, et chacune allonge :

| Étape | Valeur |
|---|---:|
| Durée en jours ouvrés | {{planification.calendrier.duree_ouvree_j::n0}} j |
| Jours perdus pour intempéries ⟦V3|jours non ouvrés pour intempéries|1,5 jour par mois|j/mois|0,5 à 3|2026|région de Marrakech : pluie et vent fort empêchant grue et bétonnage ; aucune statistique météo fournie⟧ | + {{planification.calendrier.jours_perdus_intemperies_j::n1}} j |
| **Durée à contracter** | **{{planification.calendrier.duree_ouvree_avec_intemperies_j::n0}} j ouvrés** |
| Démarrage | {{planification.calendrier.origine}} |
| **Fin** | **{{planification.calendrier.fin_avec_alea}}**, soit {{planification.calendrier.mois_calendaires::n1}} mois |

Sans les intempéries, la fin tomberait le {{planification.calendrier.fin_sans_alea}}. **Cinq semaines
d'écart** sur une seule hypothèse, et c'est celle qu'on oublie le plus souvent de poser.

:::figure {"fn":"courbeS","args":"planification.figures.courbe_s","titre":"Courbe en S du chantier, en jours-hommes de travail","num":6,"large":true,"options":{"paliers":{"$":"planification.figures.paliers"}},"voir":["L'assiette est le travail consommé (jours-hommes), pas le temps écoulé et pas l'étalement : une courbe bâtie sur le temps serait une droite, et une courbe bâtie sur l'étalement compterait des jours-hommes que personne ne fait.","Les {{planification.resume_des_paliers.nb_paliers}} bandes grises sont les paliers, et leur cause est CHERCHÉE par le calcul, pas devinée par cette légende : {{planification.resume_des_paliers.phrase}}.","La pente maximale donne le pic de besoin en main-d'œuvre. Le pic de TRÉSORERIE, lui, ne se lit pas ici : il suit les dirhams, pas les heures, et c'est le module D1 qui le trace."],"erreur":"Présenter une courbe en S construite sur l'écoulement du temps. Elle est toujours jolie, toujours en S, et ne mesure rien. La variante plus subtile est de la bâtir sur la durée des barres du Gantt : elle compte alors le travail d'une équipe qui attend une fenêtre, et gonfle le total."}
:::

#### La date n'est pas un nombre, c'est un intervalle

Les {{planification.calendrier.duree_ouvree_avec_intemperies_j::n0}} jours ci-dessus sortent d'une
trentaine d'hypothèses V3, toutes déclarées avec leur fourchette au § S4b — et jusqu'ici, aucune
variante ne les exploitait. Le module exhibait ses incertitudes, puis publiait **un** nombre. C'est
exactement ce qu'il reproche aux plannings qu'il critique.

Voici donc les trois dates. Chaque borne pousse **toutes** les hypothèses au même bout de leur
fourchette : cadences basses, forfaits et délais imposés hauts, recouvrements faibles, fenêtres
courtes et plus espacées, intempéries maximales — et l'inverse pour l'optimiste.

| | Jours ouvrés | Intempéries comprises | Fin |
|---|---:|---:|---:|
| Optimiste (×{{planification.fourchette_de_date.facteur_optimiste::n2}}) | {{planification.fourchette_de_date.optimiste.duree_j::n0}} | {{planification.fourchette_de_date.optimiste.duree_avec_intemperies_j::n0}} | {{planification.fourchette_de_date.optimiste.fin}} |
| **Retenue** | **{{planification.fourchette_de_date.retenue.duree_j::n0}}** | **{{planification.fourchette_de_date.retenue.duree_avec_intemperies_j::n0}}** | **{{planification.fourchette_de_date.retenue.fin}}** |
| Pessimiste (×{{planification.fourchette_de_date.facteur_pessimiste::n2}}) | {{planification.fourchette_de_date.pessimiste.duree_j::n0}} | {{planification.fourchette_de_date.pessimiste.duree_avec_intemperies_j::n0}} | {{planification.fourchette_de_date.pessimiste.fin}} |

**{{planification.fourchette_de_date.etendue_j::n0}} jours d'étendue, soit
{{planification.fourchette_de_date.etendue_pct_de_la_retenue::n0}} % de la durée retenue**, pour un
chantier de {{planification.calendrier.mois_calendaires::n0}} mois calendaires.

Ce chiffre est inconfortable et il est juste. Il ne dit pas que le planning est faux : il dit que
**la précision d'une date ne peut pas dépasser celle de ses entrées**, et qu'annoncer
« {{planification.calendrier.fin_avec_alea}} » sans dire d'où vient ce nombre est un engagement pris
sur des hypothèses que personne n'a vérifiées. Les deux bornes ne sont pas des probabilités — rien
ne dit que toutes les hypothèses se trompent dans le même sens — mais elles mesurent la
**sensibilité**, et c'est la seule chose défendable quand on demande de s'engager.

Ce qu'on en fait, concrètement : on ne négocie pas la date, on négocie les **trois ou quatre
hypothèses** qui portent l'essentiel de l'étendue, et on va chercher pour elles une donnée réelle —
un attachement, un devis de fournisseur, un engagement écrit de l'exploitant sur les consignations.
Chaque hypothèse qui passe de V3 à V0 resserre l'intervalle ; aucune réunion ne le resserre.

:::encart {"genre":"alerte","titre":"Et ce n'est probablement pas encore assez pessimiste"}
La borne haute ci-dessus descend les cadences au bas de leur **fourchette déclarée**, soit environ un
tiers. Or la dette n° 10 du projet soupçonne ces cadences d'être optimistes d'un **facteur 2 à 3**,
pour une raison indépendante : la part de main-d'œuvre qu'elles impliquent est très en dessous des
ordres de grandeur du métier. Si ce soupçon se confirme, la date pessimiste est encore au-delà de
{{planification.fourchette_de_date.pessimiste.fin}}.

Ce soupçon ne se lève pas ici : il se lève en ouvrant les prix poste par poste, c'est-à-dire au
module **D1**. C'est le genre de dette qu'on écrit en toutes lettres à côté de la date, et non en
note de bas de page.
:::

:::encart {"genre":"voir","titre":"Planning contractuel et planning de travail ne sont pas le même objet"}
Le **planning contractuel** est une pièce du marché : il porte des jalons, des dates, et il est
opposable. Le **planning de travail** est l'outil du conducteur de travaux : il porte des cadences,
des ateliers, des rotations, et il change toutes les semaines.

Les confondre a une conséquence précise : **la marge y change de propriétaire**. Une marge montrée
dans un planning contractuel est une marge que le maître d'ouvrage considère comme acquise et
pourra mobiliser lors d'une modification ; une marge gardée dans le planning de travail reste à
l'entreprise. Ce n'est pas une ruse, c'est la raison pour laquelle on tient deux documents : l'un
engage, l'autre pilote.

Règle de conduite, et elle n'a rien de normatif : **ne contractualisez jamais un planning plus
détaillé que ce que vous acceptez de justifier à chaque réunion.** Chaque tâche contractualisée est
une tâche sur laquelle on vous demandera des comptes, et une tâche dont la marge vous échappe.
:::

### f. De quoi la durée du projet est faite

Les trois familles de durées classent les **tâches**. Elles ne décomposent pas une **durée de
projet**, et il faut dire pourquoi : additionner les durées des tâches à marge nulle ne redonne pas
la durée du chantier dès qu'une fenêtre en épingle une — l'ensemble à marge nulle se réduit à l'aval
de l'épingle, et sa somme ne fait plus le compte.

La bonne décomposition suit le **chemin**, qui lui, par construction, somme exactement :

| Poste | Jours | Part | Les effectifs y changent-ils quelque chose ? |
|---|---:|---:|---|
| Durées **calculées** | {{planification.decomposition_du_chemin.postes_j.calculee::n1}} | {{planification.decomposition_du_chemin.postes_pct.calculee::n1}} % | oui, proportionnellement |
| Durées **déclarées** | {{planification.decomposition_du_chemin.postes_j.declaree::n1}} | {{planification.decomposition_du_chemin.postes_pct.declaree::n1}} % | pas tant qu'elles ne sont pas devenues calculées |
| Durées **imposées** | {{planification.decomposition_du_chemin.postes_j.imposee::n1}} | {{planification.decomposition_du_chemin.postes_pct.imposee::n1}} % | non |
| **Attente** d'une fenêtre | {{planification.decomposition_du_chemin.postes_j.attente_de_fenetre::n1}} | {{planification.decomposition_du_chemin.postes_pct.attente_de_fenetre::n1}} % | non |
| **Immobilisation** entre fenêtres | {{planification.decomposition_du_chemin.postes_j.immobilisation_entre_fenetres::n1}} | {{planification.decomposition_du_chemin.postes_pct.immobilisation_entre_fenetres::n1}} % | non |
| **Recouvrements** (négatifs) | {{planification.decomposition_du_chemin.postes_j.recouvrements::n1}} | {{planification.decomposition_du_chemin.postes_pct.recouvrements::n1}} % | ils gagnent du temps, et ils ont une limite physique |
| **Total** | **{{planification.decomposition_du_chemin.total_j::n2}}** | 100 % | — |

Le total retrouve la durée du réseau à {{planification.decomposition_du_chemin.ecart_j::n2}} jour
près, et le calcul **lève une erreur** si l'écart dépasse deux centièmes de jour : une décomposition
qui ne somme pas à ce qu'elle décompose n'est pas une décomposition, c'est un camembert.

**La ligne à retenir** :
{{planification.decomposition_du_chemin.part_que_les_effectifs_ne_touchent_pas_pct::n1}} % de la
durée de ce chantier — imposées, attente et immobilisation — **ne répond à aucun effectif**. C'est le
chiffre à avoir en tête avant de promettre une date, et c'est aussi celui qui dit où regarder : chez
le fournisseur de charpente et chez l'exploitant ferroviaire, pas sur le front de taille.

### g. Les ressources en conflit, et non en moyenne

Un histogramme d'effectifs dit si la base-vie suffit. Il ne dit **rien** d'une ressource unique
demandée en deux endroits le même jour. La grue à tour de ce chantier est dans ce cas : parc de
{{planification.grue.parc_de_grues::n0}}, et
{{planification.grue.taches_servies.length::n0}} tâches qui la demandent.

| | Avant lissage | Après lissage | Après recherche de résolution |
|---|---:|---:|---:|
| Demande simultanée maximale | **{{planification.grue.demande_maximale::n0}}** | {{planification.grue_apres_lissage.demande_maximale::n0}} | {{planification.grue_resolution.resultat.demande_maximale::n0}} |
| Jours en conflit | {{planification.grue.nb_jours_en_conflit::n0}} | {{planification.grue_apres_lissage.nb_jours_en_conflit::n0}} | {{planification.grue_resolution.resultat.nb_jours_en_conflit::n0}} |
| Occupation **moyenne** | {{planification.grue.occupation_moyenne_pct::n1}} % | {{planification.grue.occupation_moyenne_pct::n1}} % | {{planification.grue.occupation_moyenne_pct::n1}} % |

Lisez la dernière ligne : l'occupation moyenne est de
{{planification.grue.occupation_moyenne_pct::n1}} % et **ne bouge jamais**. Elle est rassurante dans
les trois colonnes, y compris celle où {{planification.grue.demande_maximale::n0}} tâches —
{{planification.grue.taches_au_pire_jour.0}}, {{planification.grue.taches_au_pire_jour.1}} et
{{planification.grue.taches_au_pire_jour.2}} — réclament la même grue le jour
{{planification.grue.jour_de_la_demande_maximale::n0}}. Une moyenne ne peut pas détecter un conflit :
elle le dilue.

Le calcul cherche ensuite une résolution **dans les marges libres**, et voici son verdict, publié
tel quel :

> {{planification.grue_resolution.verdict}}

C'est inconfortable, et c'est le point de ce paragraphe. Un planning se publie avec ses conflits
ouverts et leurs trois issues chiffrées, pas sans eux. Celui-ci demande une décision de **moyens** —
une seconde grue sur une période courte, ou une grue mobile en appoint — et cette décision appartient
au chiffrage, donc au module D1.

:::figure {"fn":"histogramme","args":"planification.figures.grue","titre":"Demande de grue à tour, jour par jour","num":7,"large":true,"options":{"unite":"grues demandées","moyenne":{"$":"planification.grue.parc_de_grues"},"libelle_moyenne":"parc disponible"},"voir":["Le trait vert tireté est le parc : {{planification.grue.parc_de_grues::n0}} grue. Toute barre qui le dépasse est un jour où le planning est infaisable tel qu'il est écrit.","La pointe est à {{planification.grue.demande_maximale::n0}} au jour {{planification.grue.jour_de_la_demande_maximale::n0}} : trois ateliers du gros œuvre se recouvrent et demandent le même appareil.","Le reste du temps la grue est libre, et c'est exactement ce qui rend la moyenne trompeuse : {{planification.grue.occupation_moyenne_pct::n1}} % d'occupation avec {{planification.grue.nb_jours_en_conflit::n0}} jours infaisables."],"erreur":"Conclure d'un taux d'occupation moyen qu'une ressource suffit. La moyenne répond à « la grue travaille-t-elle assez ? », pas à « le planning est-il faisable ? » — deux questions différentes, et seule la seconde intéresse le conducteur de travaux."}
:::

## S4b · Les hypothèses du planning, déclarées

Un planning n'est pas une prévision : c'est une **arithmétique sur des hypothèses**. Les voici,
toutes, avec leur fourchette. Changez-en une et la date de fin bouge — c'est exactement ce qui rend
un planning défendable en réunion.

**Les ratios qui donnent les quantités** (§ 5.0 : aucune ne sort d'un dimensionnement) —
⟦V3|épaisseur de décapage|0,3 m|m|0,2 à 0,5|2026|terre végétale et remblais superficiels⟧,
⟦V3|surprofondeur de forme sous dallage|0,4 m|m|0,3 à 0,6|2026|forme et béton de propreté⟧,
⟦V3|foisonnement des déblais|25 %|%|15 à 35|2026|augmentation de volume des déblais transportés⟧,
⟦V3|volume de béton par semelle|2,5 m³|m³|1,5 à 4|2026|semelle isolée et amorce ; prédimensionnement, le calcul appartient au module de fondations⟧,
⟦V3|épaisseur de dalle du niveau technique|0,3 m|m|0,25 à 0,4|2026|prédimensionnement⟧,
⟦V3|épaisseur de radier du niveau technique|0,4 m|m|0,3 à 0,6|2026|prédimensionnement⟧,
⟦V3|masse de charpente par m² couvert|65 kg/m²|kg/m²|45 à 90|2026|treillis de 32 m de portée et pannes⟧,
⟦V3|hauteur vitrée moyenne du hall|9 m|m|8 à 12,5|2026|façades du hall voyageurs⟧.

**Les cadences d'atelier** —
⟦V3|cadence de terrassement par atelier|450 m³/j|m³/j|300 à 700|2026|pelle 30 t et rotation de camions, trajet court⟧,
⟦V3|cadence de charpente par atelier|9 t/j|t/j|5 à 15|2026|pré-assemblage au sol et levage, grue mobile⟧,
⟦V3|cadence de couverture par atelier|250 m²/j|m²/j|150 à 400|2026|pannes, bac et étanchéité⟧.

**Les forfaits**, faute de quantités à diviser —
⟦V3|montage de la grue à tour|5 jours|j|3 à 8|2026|montage et réception de l'appareil⟧,
⟦V3|soutènement périphérique de la fouille|18 jours|j|12 à 30|2026|forfait, le calcul appartient au module de soutènements⟧,
⟦V3|étanchéité et remblais périphériques|12 jours|j|8 à 20|2026⟧,
⟦V3|noyaux et escaliers|25 jours|j|18 à 40|2026|forfait de synthèse⟧,
⟦V3|raccordement du passage souterrain|9 jours|j|6 à 15|2026|la durée est courte, l'attente de la fenêtre ne l'est pas⟧,
⟦V3|second œuvre et lots techniques|75 jours|j|55 à 110|2026|forfait de synthèse : le détail appartient aux modules C4 et B7b⟧,
⟦V3|réception et levée des réserves|10 jours|j|7 à 15|2026⟧,
et la part de charpente levée au-dessus de la voie,
⟦V3|part du tonnage levée sous consignation|35 %|%|25 à 50|2026|tonnage levé au-dessus ou à proximité immédiate de la voie exploitée⟧.

**La phase des fenêtres**, qui décale la tâche consignée et, par elle, la date de fin —
⟦V3|jour de la première consignation accordée|40 jours ouvrés|j|25 à 60|2026|fixe la phase de toutes les fenêtres suivantes ; dépend de la date de dépôt de la demande auprès de l'exploitant, six mois à l'avance⟧.
Ce paramètre a longtemps traîné dans les données sans fourchette ni déclaration, alors qu'il porte à
lui seul {{planification.consignations.CHLV.attente_avant_premiere_fenetre_j::n1}} jours de la durée
du projet.

**Les recouvrements entre tâches**, en pourcentage de la durée du prédécesseur et non en jours —
⟦V3|recouvrement du montage de grue sur l'installation|60 %|%|40 à 80|2026|la grue se monte dès que l'aire de levage et son massif sont prêts⟧,
⟦V3|recouvrement de l'implantation sur l'installation|85 %|%|60 à 95|2026|l'implantation suit l'accès et le bornage, sans attendre la base-vie⟧,
⟦V3|recouvrement du soutènement sur le décapage|50 %|%|30 à 70|2026|la paroi se réalise depuis la plateforme décapée⟧,
⟦V3|recouvrement de la fouille sur le soutènement|45 %|%|25 à 65|2026|avance que la paroi garde sur l'approfondissement — jamais l'inverse (§ S4c)⟧,
⟦V3|recouvrement du radier sur les fondations|35 %|%|20 à 50|2026|le radier démarre sur la partie déjà fondée⟧,
⟦V3|recouvrement de la mezzanine sur les poteaux|35 %|%|20 à 50|2026|la première zone de plancher se coffre dès que ses poteaux portent⟧,
⟦V3|recouvrement de la façade sur le levage|10 %|%|5 à 20|2026|la façade démarre quand la première file de charpente est posée et stable⟧.

**Pourquoi en pourcentage.** Un recouvrement écrit en jours ignore la durée qu'il recouvre. Celui du
décapage était posé à −2 jours quand la durée calculée du décapage est tombée à
{{planification.durees.TERR.duree_j::n2}} jours : le successeur démarrait **avant** son
prédécesseur, et le Gantt le publiait sans que rien ne sonne. Un pourcentage borné à 100 % ne peut
pas produire cela, et un contrôle lève désormais si un recouvrement dépasse la durée qu'il recouvre.

**Ce qu'il faut en faire.** Ces hypothèses sont dans `data/`, pas dans le texte : changez
une cadence et **tous** les nombres de ce module se recalculent, figures comprises. C'est la seule
façon de répondre « et si ? » en réunion sans refaire un planning à la main.

## S4c · Sécurité : ce que ce planning décide sans le dire

Ce module ne donne aucune prescription d'exécution, mais le planning qu'il construit **décide** des
conditions dans lesquelles quatre opérations à risque seront faites. Le § 3.4 impose de le dire. Les
dispositions ci-dessous sont **essentielles et non exhaustives** : elles ne remplacent ni le plan de
sécurité du chantier, ni les obligations réglementaires du marché. **Aucune valeur normative n'est
donnée** — la phase § 5.0 l'interdit.

| Opération du planning | Ce que le planning décide | Disposition essentielle |
|---|---|---|
| **Terrassement et fouille** du niveau technique | la profondeur ouverte et la durée pendant laquelle elle reste ouverte | talutage ou blindage **avant** toute descente ; la fouille n'est pas un passage |
| **Soutènement** périphérique | s'il est posé avant ou pendant l'excavation | le soutènement précède l'approfondissement, jamais l'inverse — et le réseau le fait : {{planification.durees.SOUT.nom}} court du jour {{planification.durees.SOUT.debut_j::n1}} au jour {{planification.durees.SOUT.fin_j::n1}}, {{planification.durees.FOUI.nom}} du jour {{planification.durees.FOUI.debut_j::n1}} au jour {{planification.durees.FOUI.fin_j::n1}} |
| **Levage** de la charpente, dont au-dessus de la voie | les fenêtres, donc la pression horaire sur l'équipe de levage | zone d'exclusion au sol, pas de levage au-dessus d'un poste occupé, abandon par vent fort |
| **Travaux sous consignation** | le nombre de fenêtres, donc la tentation de déborder | la consignation est une **limite**, pas un objectif : déborder d'une fenêtre, c'est travailler sur une voie remise sous tension |

:::encart {"genre":"alerte","titre":"Ce que ce tableau a corrigé dans le réseau lui-même"}
La ligne « le soutènement précède l'approfondissement, jamais l'inverse » était écrite dans cette
rubrique, et le réseau faisait **l'inverse** : la fouille précédait le soutènement, qui finissait
quatorze jours après la fin de la fouille. Quatorze jours de fouille profonde non soutenue, dans un
planning dont la rubrique sécurité interdit exactement cela.

Ce n'était pas une faute de frappe mais une faute de **modèle** : le lien était écrit en dur, en
jours, dans le code, et personne ne l'avait relu contre le texte d'à côté. Les décalages sont
désormais des **pourcentages de la durée du prédécesseur**, déclarés dans `data/`, et un contrôle
lève si un recouvrement dépasse la durée qu'il recouvre — ce qui arrivait aussi, deux fois : un
successeur démarrait avant son prédécesseur. Une rubrique de sécurité qui ne commande pas le calcul
n'est pas une rubrique de sécurité, c'est une précaution d'écriture.
:::

**Le lien avec tout ce module, et c'est le plus important.** Un planning trop serré ne produit pas du
retard : il produit de la **pression sur les opérations à risque**. Les {{planification.consignations.CHLV.nb_fenetres}} fenêtres
de levage calculées plus haut sont le bon exemple — si l'une est manquée, la suivante est à
{{planification.consignations.CHLV.etalement_j::n0}} jours, et c'est là que quelqu'un propose de
« finir vite » pendant que la voie est encore consignée. **La marge d'un planning est une mesure de
sécurité avant d'être une mesure de confort.**

:::encart {"genre":"note","titre":"Où est le chiffrage"}
Ce module ne porte **aucun montant**, et c'est délibéré : il produit des durées, des effectifs et
des quantités, qui sont les trois entrées du chiffrage. Les dirhams — déboursés, sous-détails de
prix, courbe de trésorerie, coût d'un mois de retard — sont le sujet du module **D1**, qui lit
exactement les mêmes cadences et les mêmes quantités. Les deux modules partagent leurs hypothèses :
c'est la seule façon qu'un planning et un bordereau ne se contredisent pas.
:::

## S5 · Erreurs fréquentes, et ce qu'elles coûtent

| Erreur | Comment elle se voit | Ce qu'elle coûte |
|---|---|---|
| Durées estimées à dire d'expert | aucun lien entre quantité, cadence et durée | un planning indéfendable, et des effectifs posés après coup |
| Cadence d'atelier confondue avec cadence par compagnon | durées divisées par l'effectif deux fois | des durées jusqu'à huit fois trop courtes |
| Effectifs mis sur une durée imposée | le planning ne bouge pas malgré les moyens | la dépense sans le gain, et la confiance perdue |
| Fenêtres de consignation oubliées | le planning tient jusqu'au premier levage | {{planification.reseau.surcout_de_delai_j::n0}} jours ici, découverts trop tard |
| Intempéries non provisionnées | le planning est juste en jours ouvrés et faux en dates | {{planification.calendrier.jours_perdus_intemperies_j::n0}} jours ouvrés |
| Lissage présenté comme gratuit | la pointe baisse, personne ne regarde la marge | {{planification.ressources.marge_totale_consommee_j::n0}} jours de marge dépensés avant le premier aléa |
| Fenêtre calculée puis non appliquée | deux dates de début pour la même tâche dans la même sortie | {{planification.consignations.CHLV.attente_avant_premiere_fenetre_j::n1}} jours ouvrés, et une date contractuelle fausse d'un mois |
| Ressource vérifiée en moyenne | « {{planification.grue.occupation_moyenne_pct::n0}} % d'occupation, ça passe » | un planning infaisable {{planification.grue.nb_jours_en_conflit::n0}} jours sur sa durée |
| Recouvrement écrit en jours sur une durée calculée | un successeur démarre avant son prédécesseur | un Gantt que personne ne relit, parce qu'il a l'air normal |
| Planning contractuel trop détaillé | chaque tâche devient opposable | la marge change de propriétaire |

## S6 · Exercices

:::exercice {"titre":"1 · Calculer une durée, et dire à quelle famille elle appartient","niveau":"application"}
Le décapage porte sur {{planification.quantites.decapage_m3::n0}} m³. La cadence déclarée est de
{{gare.planning.cadences_chantier_V3.terrassement_m3_j_atelier.valeur}} m³/j **par atelier**.
Calculez la durée avec un atelier, puis avec deux. À quelle famille appartient cette durée, et que
devient la question si l'on passe à trois ateliers ?

**Corrigé.** Un atelier : {{planification.quantites.decapage_m3::n0}} /
{{gare.planning.cadences_chantier_V3.terrassement_m3_j_atelier.valeur}} =
**{{planification.exercices.terrassement_un_atelier_j::n2}} j**. Deux ateliers :
**{{planification.exercices.terrassement_deux_ateliers_j::n2}} j**.

C'est une durée **calculée** : elle répond aux moyens, exactement proportionnellement. Mais la
question « et avec trois ateliers ? » n'a plus de réponse arithmétique — elle devient une question de
**place**. Deux pelles et leurs camions tiennent sur l'emprise ; trois se gênent, et la cadence
réelle n'est plus 3 × 450. **Une durée calculée ne l'est que dans le domaine où la cadence reste
vraie**, et ce domaine n'est jamais écrit dans le tableau des cadences. C'est à vous de le connaître.
:::

:::exercice {"titre":"2 · Renforcer une tâche qui n'est pas critique","niveau":"application"}
Les poteaux du RDC durent {{planification.exercices.poteaux_deux_ateliers_j::n2}} j avec
{{gare.planning.effectifs_chantier_V3.ateliers_poteaux}} ateliers. Vous en ajoutez un troisième.
Que gagne le **projet** ?

**Corrigé.** La tâche passe à **{{planification.exercices.poteaux_trois_ateliers_j::n2}} j**, soit
{{planification.exercices.gain_poteaux_j::n2}} j de gagnés sur elle.

Le projet, lui, gagne **{{planification.variantes.poteaux_trois_ateliers.duree_projet_j::n2}} j contre
{{planification.variantes.reference.duree_projet_j::n2}} j : rien du tout.** Et le piège est plus
retors qu'il n'y paraît, parce que les poteaux **sont** sur le plus long chemin du réseau. Ce qui
annule le gain n'est pas leur position : c'est la **fenêtre de consignation**, qui épingle le levage
au jour {{planification.consignations.CHLV.debut::n0}}. Tout ce qui précède cette épingle finit de
toute façon avant, et gagner du temps en amont ne fait qu'allonger l'attente. Vous avez dépensé une
équipe entière pour transformer trois jours de travail en trois jours d'attente.

*C'est l'erreur la plus coûteuse du métier, et la plus naturelle : on renforce ce qu'on voit en
retard sur le terrain, pas ce qui porte le délai. Et le réflexe « est-ce sur le chemin critique ? »
ne suffit pas quand une contrainte externe coupe ce chemin en deux : la bonne question est « cette
tâche décale-t-elle la première date contrainte en aval ? »*
:::

:::exercice {"titre":"3 · Défendre une date face aux consignations","niveau":"probleme"}
Le maître d'ouvrage veut gagner deux mois sur les
{{planification.reseau.duree_avec_fenetres_j::n0}} jours ouvrés. Le levage au-dessus de la voie coûte
{{planification.consignations.CHLV.duree_de_travail_j::n1}} jours de travail **étalés sur
{{planification.consignations.CHLV.etalement_j::n0}}**. Trois leviers existent. Lequel défendez-vous,
et combien rapporte chacun ?

**Corrigé.** Les trois sont calculés, et leur hiérarchie n'est pas celle qu'on croit.

**(a) Négocier une fenêtre plus longue** — passer de
{{gare.planning.contraintes_exploitation.fenetre_jours.valeur}} à 10 jours ouvrés consécutifs :
projet à **{{planification.variantes.fenetre_longue.duree_projet_j::n0}} j**, soit
**{{planification.reseau.duree_avec_fenetres_j::n0}} − {{planification.variantes.fenetre_longue.duree_projet_j::n0}}
= 58 jours gagnés**. Le levage se fait en
{{planification.variantes.fenetre_longue.nb_fenetres_levage}} fenêtres au lieu de
{{planification.consignations.CHLV.nb_fenetres}}. **Coût pour l'entreprise : zéro.** C'est une
négociation avec l'exploitant, pas un achat.

**(b) Réduire la part levée au-dessus de la voie** — de
{{gare.planning.contraintes_exploitation.part_levage_sous_consignation_pct.valeur}} % à 15 % par
pré-assemblage au sol et levage depuis l'autre côté : projet à
**{{planification.variantes.moins_de_levage_sur_voie.duree_projet_j::n0}} j**. Coût : une aire de
pré-assemblage et une grue mobile supplémentaire.

**(c) Supprimer la consignation** par une protection de voie : projet à
**{{planification.variantes.protection_de_voie.duree_projet_j::n0}} j**, c'est-à-dire la durée du
réseau sans contrainte. Le levier le plus puissant, et le plus cher — et il demande l'accord de
l'exploitant autant que (a).

**Ce qu'il faut dire en réunion** : « Deux mois se gagnent, mais pas sur le chantier : ils se gagnent
**chez l'exploitant**. Une fenêtre de dix jours au lieu de trois rend 58 jours ouvrés et ne coûte
rien en travaux. Je demande ce créneau six mois à l'avance ; sans lui, aucun effectif ne rattrapera
ces deux mois. » Pas « on va serrer le planning ».

*Le piège : chercher les deux mois dans les durées calculées, qui sont les seules qu'on sache
raccourcir. Le tableau de décomposition du § S4f le chiffre : elles ne pèsent que
{{planification.decomposition_du_chemin.postes_pct.calculee::n1}} % de la durée du projet, contre
{{planification.decomposition_du_chemin.part_que_les_effectifs_ne_touchent_pas_pct::n1}} % que les
moyens ne touchent pas — durées imposées, attente de fenêtre et immobilisation entre fenêtres.*
:::

:::exercice {"titre":"4 · Trouver l'erreur dans ce planning","niveau":"revue critique"}
Une entreprise présente le planning suivant pour la charpente :

| Tâche | Durée annoncée | Démarrage annoncé |
|---|---:|---|
| Études et visa de la charpente | {{planification.durees.CHET.duree_j::n0}} j | après la fin du gros œuvre |
| Fabrication en atelier | {{planification.durees.CHFA.duree_j::n0}} j | après les études |
| Levage | {{planification.durees.CHLV.duree_etalee_j::n0}} j | « dès réception en atelier » |

**Trois choses ne vont pas. Lesquelles ?**

**Corrigé.**

1. **Les études ne démarrent pas après le gros œuvre : elles démarrent au jour zéro.** Études et
   fabrication totalisent **{{planification.exercices.charpente_etudes_plus_fabrication_j::n0}} jours
   imposés** que rien ne raccourcit. Les lancer après le gros œuvre ajoute ces
   {{planification.exercices.charpente_etudes_plus_fabrication_j::n0}} jours **à la fin du
   chantier** au lieu de les y superposer. C'est l'erreur de planning la plus chère qui existe, et
   elle ne se voit pas sur un Gantt où tout paraît s'enchaîner proprement.

2. **« Dès réception en atelier » n'est pas une date.** Le levage au-dessus de la voie ne se fait pas
   quand la charpente arrive : il se fait quand l'exploitant **consigne**. Entre les deux, il y a
   jusqu'à {{gare.planning.contraintes_exploitation.periode_entre_fenetres_jours.valeur}} jours
   ouvrés d'attente, et la demande se dépose six mois à l'avance. Un planning qui ne porte pas les
   fenêtres de consignation est un planning faux dès le premier levage.

3. **La durée de levage annoncée confond travail et étalement.** Les
   {{planification.durees.CHLV.duree_etalee_j::n0}} jours ne sont pas du travail : il y a
   {{planification.consignations.CHLV.duree_de_travail_j::n1}} jours de levage réel et
   {{planification.consignations.CHLV.immobilisation_improductive_j::n0}} jours d'attente entre
   fenêtres. La distinction n'est pas académique : le **coût** suit le travail, le **délai** suit
   l'étalement, et une équipe de levage immobilisée se facture.

*Ce qu'on vise : rien, tant que les études ne sont pas repositionnées au jour zéro et que les
fenêtres ne figurent pas au planning. Et on le dit par écrit, avec les
{{planification.exercices.charpente_etudes_plus_fabrication_j::n0}} jours imposés en chiffres.*
:::

## S7 · Check-list, glossaire et quiz

**Check-list avant de diffuser un planning**

1. Chaque durée porte-t-elle sa **famille** — calculée, imposée, déclarée ? Les imposées sont-elles
   lancées au plus tôt ?
2. Les durées calculées viennent-elles d'une **quantité ÷ cadence ÷ ateliers**, avec la cadence dans
   la bonne unité (atelier, pas compagnon) ?
3. Les **contraintes externes** — consignations, fenêtres d'exploitation, délais d'approvisionnement —
   figurent-elles comme des tâches, et non comme des notes de bas de page ?
4. Le **chemin critique** a-t-il été lu, ou seulement affiché ? Passe-t-il où vous croyez ?
5. Les **ressources** sont-elles vérifiées en conflit instantané, pas seulement en moyenne ?
6. Le planning est-il converti en **dates civiles**, intempéries comprises, avant d'être contractualisé ?
7. Savez-vous **combien de marge** il contient, et où elle est ?

**Glossaire**

| Terme | Ce que c'est, précisément |
|---|---|
| **Chemin critique** | la suite de tâches dont tout retard décale la fin du projet ; sa marge totale est nulle |
| **Marge totale** | le retard qu'une tâche peut prendre sans décaler la **fin du projet** ; la consommer décale les successeurs |
| **Marge libre** | le retard qu'elle peut prendre sans décaler **aucune** tâche ; la seule qu'on dépense sans rien demander |
| **Décalage négatif** | un successeur qui démarre avant la fin de son prédécesseur — un recouvrement, pas une erreur de saisie |
| **Durée imposée** | une durée qu'aucun moyen ne raccourcit : séchage, fabrication, visa, délai de livraison |
| **Lissage** | déplacer des tâches **dans leur marge** pour abaisser la pointe de ressources, sans changer la fin |
| **Nivellement** | plafonner une ressource en **allongeant** le projet ; ce n'est pas le lissage, et ça ne s'annonce pas pareil |
| **Ligne d'équilibre** | représentation des tâches répétitives où la pente est la cadence |
| **Étalement** | la durée pendant laquelle une tâche occupe le calendrier sans occuper personne, faute de fenêtre |
| **Planning contractuel** | la pièce opposable du marché ; distinct du planning de travail, et la marge n'y appartient pas aux mêmes |

:::exercice {"titre":"Sept questions pour vérifier","niveau":"application"}
**1. Une tâche de fabrication en atelier dure 60 jours. Vous doublez l'effectif du chantier. Que gagnez-vous ?**
**Rien.** C'est une durée **imposée** : elle ne dépend d'aucun moyen du chantier. Le seul levier est de la **lancer plus tôt**, ou d'en négocier le délai avec le fournisseur.

**2. Une cadence est donnée en « 450 m³/j ». Quelle question posez-vous avant de l'utiliser ?**
**Par quoi ?** Par atelier, par équipe ou par compagnon. Confondre une cadence d'atelier et une cadence unitaire produit des durées fausses d'un facteur égal à l'effectif — l'erreur d'unité la plus commune de la planification.

**3. Le planning de ce chantier montre {{planification.grue.occupation_moyenne_pct::n0}} % d'occupation moyenne de la grue à tour. Pouvez-vous conclure qu'elle suffit ?**
**Non — et sur ce chantier précis, elle ne suffit pas.** Le balayage jour par jour du § S4g trouve {{planification.grue.demande_maximale::n0}} tâches qui la demandent en même temps au jour {{planification.grue.jour_de_la_demande_maximale::n0}}, et {{planification.grue.nb_jours_en_conflit::n0}} jours de conflit en tout, pour un parc de {{planification.grue.parc_de_grues::n0}}. Une occupation moyenne ne dit rien des **conflits instantanés** : il faut balayer les fronts, pas faire une moyenne.

**4. Quelle est la différence entre lisser et niveler ?**
**Lisser** déplace des tâches dans leur marge : la pointe baisse, la **fin ne bouge pas**. **Niveler** plafonne la ressource : le projet **s'allonge**. Les deux mots désignent deux décisions différentes, et l'une se présente en réunion autrement que l'autre.

**5. Sur ce chantier, le plus long chemin compte {{planification.reseau.chemin_critique.length::n0}} tâches, mais seulement {{planification.reseau.nb_taches_critiques::n0}} ont une marge nulle. Comment est-ce possible, et qu'est-ce que cela change à votre suivi hebdomadaire ?**
Parce qu'une **fenêtre de consignation épingle** le levage au jour {{planification.consignations.CHLV.debut::n0}} : tout ce qui est en amont finit de toute façon avant cette date et reçoit de la marge. Pour le suivi : le point sur l'avancement du gros œuvre est **rassurant et presque muet sur le délai** ; les deux points qui le portent sont la date de consignation obtenue et l'avancement des études et de la fabrication de charpente, qui doivent être prêtes avant elle.

**6. Pourquoi convertir un planning en dates civiles **avant** de le contractualiser ?**
Parce que deux conversions allongent : les week-ends, puis les **intempéries**. Ici {{planification.calendrier.jours_perdus_intemperies_j::n0}} jours ouvrés de plus, et une fin au {{planification.calendrier.fin_avec_alea}} au lieu du {{planification.calendrier.fin_sans_alea}}. S'engager sur des jours ouvrés convertis à la louche, c'est s'engager sur une date qu'on ne tiendra pas.

**7. Une tâche de 12 jours de travail apparaît sur 80 jours au planning. Est-ce une erreur ?**
**Non**, si c'est un **étalement** sous consignation : la tâche ne dure pas plus longtemps, elle attend ses fenêtres. Le coût suit les 12 jours, le délai suit les 80. Mais si personne ne l'a écrit, c'est une erreur de **lecture** qui coûtera cher en réunion.

:::
## S8 · Fiche mémo

:::memo
## Fiche mémo — planifier un chantier de gare

**Les trois familles de durées**

| Famille | D'où elle vient | Ce qui la raccourcit |
|---|---|---|
| Calculée | quantité ÷ (cadence × ateliers) | plus d'ateliers, meilleure cadence — **dans le domaine où la cadence reste vraie** |
| Imposée | physique ou tiers : séchage, fabrication, visa | **rien** — seulement un départ plus tôt |
| Déclarée | une hypothèse, faute de quantité | rien, tant qu'elle n'est pas devenue calculée |

**Les chiffres de ce chantier**

| | |
|---|---:|
| Durée sans contrainte externe | {{planification.reseau.duree_sans_contrainte_j::n0}} j ouvrés |
| Avec les fenêtres de consignation | **{{planification.reseau.duree_avec_fenetres_j::n0}} j** (+{{planification.reseau.surcout_de_delai_pct::n0}} %) |
| Part de la durée **hors d'atteinte des moyens** | {{planification.decomposition_du_chemin.part_que_les_effectifs_ne_touchent_pas_pct::n1}} % |
| Attente de la première fenêtre, sur le chemin | {{planification.decomposition_du_chemin.postes_j.attente_de_fenetre::n0}} j |
| Immobilisation entre fenêtres, sur le chemin | {{planification.decomposition_du_chemin.postes_j.immobilisation_entre_fenetres::n0}} j |
| Conflit de grue, parc de {{planification.grue.parc_de_grues::n0}} | {{planification.grue.demande_maximale::n0}} demandes simultanées, {{planification.grue.nb_jours_en_conflit::n0}} j |
| Pointe d'effectif, brute puis lissée | {{planification.ressources.pointe_avant}} → {{planification.ressources.pointe_apres}} |
| Marge consommée par le lissage | {{planification.ressources.marge_totale_consommee_j::n0}} j |
| Fin, intempéries comprises | **{{planification.calendrier.fin_avec_alea}}** |
| Fourchette de fin, hypothèses aux bornes | {{planification.fourchette_de_date.optimiste.fin}} à {{planification.fourchette_de_date.pessimiste.fin}} |

**Les sept réflexes**

1. Classer chaque durée par famille **avant** de chercher à la réduire.
2. Lancer les durées imposées au **jour zéro**, pas à leur place logique.
3. Vérifier l'unité de chaque cadence : atelier, équipe ou compagnon.
4. Porter les **fenêtres d'exploitation** comme des tâches.
5. Lire le chemin critique, pas seulement l'afficher.
6. Vérifier les ressources en **conflit**, pas en moyenne.
7. Convertir en dates **avec** les intempéries avant de signer.

**Le piège de réunion** : annoncer un gain obtenu en renforçant une tâche non critique. Refaites
tourner le réseau avant d'annoncer quoi que ce soit — c'est trente secondes contre une date
intenable.
:::
