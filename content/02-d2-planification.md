---
id: D2
titre: Planification d'un chantier de gare
fil: Palier 1 · module 1 — direction de projet
resume: Vingt-sept tâches, trois familles de durées, et un chemin critique qui ne passe pas où l'on croit. Le planning d'un chantier ferroviaire se calcule ; il ne s'estime pas.
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

La conséquence se lit sur le chemin critique de ce chantier :
**{{planification.familles.sur_le_chemin_critique_j.imposee::n0}} jours sur
{{planification.reseau.duree_avec_fenetres_j::n0}}**, soit
**{{planification.familles.part_imposee_du_chemin_pct::n1}} %**, sont des durées **imposées**. Doubler
tous les effectifs du chantier ne les touche pas d'un jour. C'est le genre de phrase qu'il faut
pouvoir dire en réunion avec le calcul derrière.

:::figure {"fn":"wbs","args":"planification.figures.wbs","titre":"Organigramme des tâches (WBS), coloré par famille de durée","num":1,"large":true,"racine":"Gare voyageurs — chantier","voir":["La couleur n'est pas décorative : vert = durée calculée, brique = durée imposée, gris = durée déclarée. Un planning dont les barres brique sont sur le chemin critique ne s'accélère pas avec des hommes.","Le lot 4 (charpente) porte deux durées imposées à la suite — études puis fabrication — avant la moindre heure de chantier.","Les durées déclarées sont majoritaires en nombre mais minoritaires en enjeu : elles se transforment en durées calculées au fur et à mesure que les quantités arrivent."],"erreur":"Produire un WBS qui décalque l'organigramme de l'entreprise plutôt que le découpage physique de l'ouvrage. Un WBS sert à accrocher des quantités et des coûts à des tâches, pas à nommer des services."}
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

:::encart {"genre":"alerte","titre":"Le résultat le plus contre-intuitif de ce module"}
Le chemin critique de ce chantier est :

**{{planification.reseau.chemin_critique.0}} → {{planification.reseau.chemin_critique.1}} →
{{planification.reseau.chemin_critique.2}} → {{planification.reseau.chemin_critique.3}} →
{{planification.reseau.chemin_critique.4}} → {{planification.reseau.chemin_critique.5}} →
{{planification.reseau.chemin_critique.6}} → {{planification.reseau.chemin_critique.7}} →
{{planification.reseau.chemin_critique.8}}**

Regardez ce qui n'y est pas : **ni les terrassements, ni les fondations, ni le plancher de
mezzanine**. Tout le gros œuvre — celui sur lequel se concentrent les réunions de chantier, les
effectifs et l'attention du conducteur de travaux — dispose de marge. Le chantier est piloté par la
**charpente**, et plus précisément par les deux durées imposées qui la précèdent.

Ce que cela change dans votre travail : le point de suivi hebdomadaire sur l'avancement du gros
œuvre est rassurant et **ne dit rien du délai**. Le vrai point de suivi, les six premiers mois, est
la relance du bureau d'études de charpente et du fournisseur. Un planning qui ne montre pas cela est
un planning qui vous fera arriver en retard en ayant tenu toutes les cadences.
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

| | Travail réel | Étalement | Fenêtres | Immobilisation improductive |
|---|---:|---:|---:|---:|
| Levage au-dessus de la voie | {{planification.consignations.CHLV.duree_de_travail_j::n2}} j | **{{planification.consignations.CHLV.etalement_j::n2}} j** | {{planification.consignations.CHLV.nb_fenetres}} | {{planification.consignations.CHLV.immobilisation_improductive_j::n0}} j |
| Raccordement du passage souterrain | {{planification.consignations.PSOU.duree_de_travail_j::n2}} j | {{planification.consignations.PSOU.etalement_j::n2}} j | {{planification.consignations.PSOU.nb_fenetres}} | {{planification.consignations.PSOU.immobilisation_improductive_j::n0}} j |

**Le chantier passe de {{planification.reseau.duree_sans_contrainte_j::n0}} à
{{planification.reseau.duree_avec_fenetres_j::n0}} jours ouvrés** — soit
**{{planification.reseau.surcout_de_delai_j::n0}} jours, {{planification.reseau.surcout_de_delai_pct::n1}} %** — à cause de
**{{planification.consignations.CHLV.duree_de_travail_j::n0}} jours de travail**. Il n'y a pas
d'erreur : le levage ne dure pas plus longtemps, il **s'étale**. La distinction est capitale, parce
que le **coût** suit la durée de travail tandis que le **délai** suit l'étalement, et parce qu'un
étalement ne se résorbe pas avec des moyens.

Trois leviers existent, et un seul est bon marché : négocier une fenêtre plus longue, réduire la part
levée au-dessus de la voie (pré-assemblage au sol, levage par l'autre côté), ou installer une
protection de voie qui supprime la consignation pour une partie des opérations. L'exercice 3 les
chiffre.

:::figure {"fn":"reseau","args":"planification.figures.reseau","titre":"Réseau de la chaîne critique : charpente, couverture et finitions","num":2,"large":true,"voir":["Le réseau publié ici est la partie qui porte le délai, pas les vingt-sept tâches : un PERT illisible n'est pas un PERT.","Les deux premières boîtes sont des durées imposées — études et fabrication — et elles commencent au jour zéro du chantier. Les décaler d'une semaine décale la livraison d'une semaine.","Les tâches hors chemin critique portent leur marge totale : c'est ce que le planificateur peut dépenser, et c'est fini quand c'est dépensé."],"erreur":"Afficher un réseau de cent tâches « pour être complet ». Un réseau sert à montrer une structure de dépendances ; au-delà d'une vingtaine de nœuds, il ne montre plus rien et c'est le Gantt qui prend le relais."}
:::

### b. Le Gantt, et la lecture des marges

:::figure {"fn":"gantt","args":"planification.figures.gantt","titre":"Gantt du chantier — les barres brique sont critiques","num":3,"large":true,"voir":["Les barres de la charpente démarrent au jour zéro : ce sont les études, pas des travaux. Un Gantt qui ne les porte pas est un Gantt qui ment sur la date de livraison.","Le plancher de mezzanine — tout le module TV — est une barre parmi vingt-sept, et elle n'est pas critique.","Les deux barres de consignation sont longues et presque vides : leur longueur est de l'attente, pas du travail."],"erreur":"Lire un Gantt comme un calendrier de travaux. Une barre longue n'est pas forcément une tâche lourde : elle peut être une tâche courte qui attend une fenêtre."}
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

L'effectif présent chaque jour est la somme des tâches en cours. Brut, il monte à
**{{planification.ressources.pointe_avant}} personnes** pour une moyenne de
{{planification.ressources.moyenne_avant::n1}} : une pointe que la base-vie, les vestiaires et le
parking doivent encaisser pour quelques jours.

**Lisser** consiste à décaler les tâches non critiques **dans leur marge**, sans changer aucune durée
ni la date de fin. Résultat ici : pointe ramenée à **{{planification.ressources.pointe_apres}}**, soit
**{{planification.ressources.gain_de_pointe_pct::n1}} % de moins**, en décalant
{{planification.durees.NOYX.nom}} et {{planification.durees.MEZZ.nom}}.

Le prix : **{{planification.ressources.marge_totale_consommee_j::n0}} jours de marge totale
consommés**. C'est le vrai sujet, et il est rarement posé. Une marge dépensée en confort
d'exploitation n'est plus disponible pour l'aléa. La question à se poser n'est donc pas « peut-on
lisser ? » mais « **la pointe était-elle infaisable ?** ». Si la base-vie tient 59 personnes, le
lissage est un luxe payé en marge.

:::figure {"fn":"histogramme","args":"planification.figures.effectifs","serie2":"planification.figures.effectifs_lisses","titre":"Effectif présent, brut et après lissage","num":5,"large":true,"voir":["Le contour foncé est l'effectif après lissage : la pointe tombe, la surface ne change pas — on n'a pas supprimé du travail, on l'a déplacé.","Les creux de début et de fin sont normaux ; seul le plateau central est en régime.","C'est la pointe, et non la moyenne, qui dimensionne la base-vie, le parking et les réfectoires."],"erreur":"Niveler au lieu de lisser sans le dire. Lisser déplace des tâches dans leur marge et ne change pas la fin ; niveler plafonne l'effectif et ALLONGE le projet. Les deux mots désignent deux décisions différentes."}
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

:::figure {"fn":"courbeS","args":"planification.figures.courbe_s","titre":"Courbe en S du chantier, en jours-hommes","num":6,"large":true,"voir":["L'assiette est le travail consommé (jours-hommes), pas le temps écoulé : une courbe bâtie sur le temps serait une droite, et une droite n'est pas une courbe en S.","Le palier au milieu de la courbe n'est pas une erreur : c'est l'attente des fenêtres de consignation, pendant laquelle le chantier avance peu.","La pente maximale donne le pic de trésorerie et de besoin en main-d'œuvre — c'est là que le préfinancement se joue."],"erreur":"Présenter une courbe en S construite sur l'écoulement du temps. Elle est toujours jolie, toujours en S, et ne mesure rien."}
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

**Ce qu'il faut en faire.** Ces trente-six hypothèses sont dans `data/`, pas dans le texte : changez
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
| **Soutènement** périphérique | s'il est posé avant ou pendant l'excavation | le soutènement précède l'approfondissement, jamais l'inverse |
| **Levage** de la charpente, dont au-dessus de la voie | les fenêtres, donc la pression horaire sur l'équipe de levage | zone d'exclusion au sol, pas de levage au-dessus d'un poste occupé, abandon par vent fort |
| **Travaux sous consignation** | le nombre de fenêtres, donc la tentation de déborder | la consignation est une **limite**, pas un objectif : déborder d'une fenêtre, c'est travailler sur une voie remise sous tension |

**Le lien avec tout ce module, et c'est le plus important.** Un planning trop serré ne produit pas du
retard : il produit de la **pression sur les opérations à risque**. Les {{planification.consignations.CHLV.nb_fenetres}} fenêtres
de levage calculées plus haut sont le bon exemple — si l'une est manquée, la suivante est à
{{planification.consignations.CHLV.etalement_j::n0}} jours, et c'est là que quelqu'un propose de
« finir vite » pendant que la voie est encore consignée. **La marge d'un planning est une mesure de
sécurité avant d'être une mesure de confort.**

## S5 · Erreurs fréquentes, et ce qu'elles coûtent

| Erreur | Comment elle se voit | Ce qu'elle coûte |
|---|---|---|
| Durées estimées à dire d'expert | aucun lien entre quantité, cadence et durée | un planning indéfendable, et des effectifs posés après coup |
| Cadence d'atelier confondue avec cadence par compagnon | durées divisées par l'effectif deux fois | des durées jusqu'à huit fois trop courtes |
| Effectifs mis sur une durée imposée | le planning ne bouge pas malgré les moyens | la dépense sans le gain, et la confiance perdue |
| Fenêtres de consignation oubliées | le planning tient jusqu'au premier levage | {{planification.reseau.surcout_de_delai_j::n0}} jours ici, découverts trop tard |
| Intempéries non provisionnées | le planning est juste en jours ouvrés et faux en dates | {{planification.calendrier.jours_perdus_intemperies_j::n0}} jours, soit cinq semaines |
| Lissage présenté comme gratuit | la pointe baisse, personne ne regarde la marge | {{planification.ressources.marge_totale_consommee_j::n0}} jours de marge dépensés avant le premier aléa |
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
{{planification.variantes.reference.duree_projet_j::n2}} j : rien du tout.** Les poteaux ne sont pas
sur le chemin critique — ils disposent de marge, et le troisième atelier la consomme sans toucher à
la date de fin. Vous avez dépensé une équipe entière pour un gain nul.

*C'est l'erreur la plus coûteuse du métier, et la plus naturelle : on renforce ce qu'on voit en
retard sur le terrain, pas ce qui porte le délai. Le chemin critique de ce chantier passe par un
bureau d'études, pas par une grue.*
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
raccourcir. Elles ne pèsent que {{planification.familles.sur_le_chemin_critique_j.calculee::n0}} jours
du chemin critique, contre {{planification.familles.sur_le_chemin_critique_j.imposee::n0}} jours
d'imposées et l'étalement des consignations.*
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
   imposés** que rien ne raccourcit. Les lancer après le gros œuvre ajoute ces cent jours **à la fin
   du chantier** au lieu de les y superposer. C'est l'erreur de planning la plus chère qui existe, et
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
fenêtres ne figurent pas au planning. Et on le dit par écrit, avec les cent jours imposés en toutes
lettres.*
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

**3. Votre planning montre 67 % d'occupation de la grue. Pouvez-vous conclure qu'elle suffit ?**
**Non.** Une occupation moyenne ne dit rien des **conflits instantanés** : la grue peut être libre les trois quarts du temps et demandée deux fois le quart restant. Il faut balayer les fronts, pas faire une moyenne.

**4. Quelle est la différence entre lisser et niveler ?**
**Lisser** déplace des tâches dans leur marge : la pointe baisse, la **fin ne bouge pas**. **Niveler** plafonne la ressource : le projet **s'allonge**. Les deux mots désignent deux décisions différentes, et l'une se présente en réunion autrement que l'autre.

**5. Le chemin critique de ce chantier passe par les études et la fabrication de charpente. Qu'est-ce que cela change à votre suivi hebdomadaire ?**
Le point sur l'avancement du gros œuvre est **rassurant et muet sur le délai**. Les six premiers mois, le vrai point de suivi est la **relance du bureau d'études et du fournisseur** de charpente.

**6. Pourquoi convertir un planning en dates civiles **avant** de le contractualiser ?**
Parce que deux conversions allongent : les week-ends, puis les **intempéries**. Ici {{planification.calendrier.jours_perdus_intemperies_j::n0}} jours, soit cinq semaines. S'engager sur des jours ouvrés convertis à la louche, c'est s'engager sur une date qu'on ne tiendra pas.

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
| Part **imposée** du chemin critique | {{planification.familles.part_imposee_du_chemin_pct::n0}} % |
| Pointe d'effectif, brute puis lissée | {{planification.ressources.pointe_avant}} → {{planification.ressources.pointe_apres}} |
| Marge consommée par le lissage | {{planification.ressources.marge_totale_consommee_j::n0}} j |
| Fin, intempéries comprises | **{{planification.calendrier.fin_avec_alea}}** |

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
