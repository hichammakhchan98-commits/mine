---
id: B7c
titre: Bâtiments ferroviaires — construire à côté d'une voie exploitée
fil: Palier 1 · module 6 — le cas phare, sa spécificité
resume: Une journée de consignation n'est pas une journée de travail. Ce module descend à l'intérieur d'une plage, y trouve une erreur de planning d'un facteur quatre, et montre que la réponse n'est pas dans le planning.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · aucune distance de sécurité, aucun gabarit, aucune charge ferroviaire n'est chiffré
pied: Exemple pédagogique — ne remplace ni une procédure de sécurité ferroviaire, ni un plan de prévention, ni les consignes de l'exploitant. Aucun travail à proximité d'une voie exploitée ne se prépare à partir d'un cours.
donnees: ferroviaire, planification, prix, gare
---

## S1 · Ce que ce module ajoute, et ce qu'il ne refait pas

Tout ce que le cours a construit jusqu'ici — le cycle, le parc de coffrage, le planning, les coûts,
le suivi — vaut pour n'importe quel bâtiment. Ce module traite ce qu'une **gare** ajoute, et qui ne
se trouve dans aucun manuel de bâtiment : **on construit à côté d'une voie exploitée.**

Trois conséquences, toutes calculables, aucune normative :

1. **une plage de consignation n'est pas un créneau de travail** : une part fixe et irréductible est
   consommée avant et après, et elle décide du rendement ;
2. **un levage ne se fractionne pas**, donc la masse des pièces et la durée des plages sont une
   seule décision, prise en études ;
3. **il n'y a pas un seul donneur d'ordre** : le gestionnaire d'infrastructure ne reçoit pas d'ordre
   du maître d'ouvrage de la gare, il se coordonne avec lui.

Le module D2 modélise déjà les consignations **à l'échelle du jour** — quand la fenêtre tombe, ce
qu'elle décale. B7c descend d'un cran et traite ce qui se passe **à l'intérieur** d'une plage. Il ne
recalcule ni le réseau, ni les quantités, ni les cadences : il les lit.

::: encart {"genre":"alerte","titre":"Ce module a trouvé une erreur dans le planning du cours"}
En descendant à l'échelle de la plage, le calcul a montré que D2 donnait à la tâche de levage sous
consignation la durée d'un **travail de jour**, puis la logeait dans des fenêtres comme si chacune
produisait huit heures. Elle n'en produit que
{{ferroviaire.plage.travail_effectif_h::n2}}. Corrigé, le levage passe de 5 à
**{{ferroviaire.leviers.reference.fenetres_CHLV}} fenêtres** et le chantier de 363 à
**{{ferroviaire.leviers.reference.duree_du_chantier_j::n0}} jours ouvrés**.

C'est beaucoup, et c'est le sujet de ce module : **ce n'est pas une réponse, c'est un signal.** Un
planning qu'on rallonge de onze mois pour absorber un rendement de
{{ferroviaire.plage.rendement_pct::n0}} % est un planning que personne n'a discuté. Le § S4c montre
où sont les leviers — et ils ne sont pas dans le planning.
:::

## S2 · L'idée centrale : la part fixe ne se rattrape pas

Voici le seul fait qu'il faut emporter de ce module, et il tient en une phrase.

Entre le moment où la voie est fermée à la circulation et celui où elle est rendue, il y a des
opérations obligatoires : prendre possession et baliser, consigner la caténaire et la mettre à la
terre, amener les moyens, puis replier, déconsigner, contrôler que le gabarit est libre, et garder
une marge avant le premier train. **Cette part ne dépend ni de l'effectif, ni de la quantité à
réaliser, ni de la motivation de l'équipe.**

Pire : {{ferroviaire.plage.part_tenue_par_l_exploitant_h::n2}} h sur les
{{ferroviaire.plage.part_fixe_h::n2}} h appartiennent à **l'exploitant**. Ce n'est pas votre
entreprise qui consigne la caténaire, et le temps qu'elle y met ne figure dans aucun de vos
sous-détails de prix.

**La conséquence est contre-intuitive et elle décide de tout** : doubler l'équipe ne raccourcit pas
d'une minute ce qui mange la plage. Sur un chantier ordinaire, un retard se rattrape avec des
moyens. Ici, non. C'est pourquoi un chef de projet suivi de chantier ferroviaire négocie des
**plages**, pas des effectifs — et il les négocie six mois à l'avance, parce que c'est le délai.

## S3 · Principes

### a. La décomposition d'une plage

| Poste | Durée | Tenu par | |
|---|---:|---|---|
| {{ferroviaire.plage.detail.0.poste}} | ⟦V3|prise de possession et balisage d'une plage|0,50|h|0,25 à 1,0|2026|vérification de la fermeture effective et mise en place de l'agent de sécurité⟧ h | {{ferroviaire.plage.detail.0.tenu_par}} | avant |
| {{ferroviaire.plage.detail.1.poste}} | ⟦V3|consignation caténaire, mise à la terre et vérification d'absence de tension|0,75|h|0,5 à 1,5|2026|opération d'un agent habilité de l'exploitant : sa durée ne se négocie pas⟧ h | {{ferroviaire.plage.detail.1.tenu_par}} | avant |
| {{ferroviaire.plage.detail.2.poste}} | ⟦V3|amenée des moyens sur la zone de travail|0,40|h|0,2 à 1,0|2026|acheminement des engins et du personnel une fois la voie prise⟧ h | {{ferroviaire.plage.detail.2.tenu_par}} | avant |
| **{{ferroviaire.plage.detail.3.poste}}** | **{{ferroviaire.plage.detail.3.h::n2}} h** | {{ferroviaire.plage.detail.3.tenu_par}} | *calculé* |
| {{ferroviaire.plage.detail.4.poste}} | ⟦V3|repli des moyens et dépose des mises à la terre|0,50|h|0,25 à 1,0|2026|évacuation des engins et nettoyage⟧ h | {{ferroviaire.plage.detail.4.tenu_par}} | après |
| {{ferroviaire.plage.detail.5.poste}} | ⟦V3|déconsignation et contrôle de libération du gabarit|0,50|h|0,25 à 1,0|2026|acte formel de l'exploitant avant restitution⟧ h | {{ferroviaire.plage.detail.5.tenu_par}} | après |
| {{ferroviaire.plage.detail.6.poste}} | ⟦V3|marge de restitution avant la première circulation|0,50|h|0,25 à 1,0|2026|marge NON NÉGOCIABLE : une voie restituée en retard arrête un train⟧ h | {{ferroviaire.plage.detail.6.tenu_par}} | après |
| **Plage nominale** | ⟦V3|durée d'une plage de consignation accordée|6,00|h|4 à 8|2026|de la dernière circulation à la première du matin⟧ h | l'exploitant l'accorde | |
| **Part fixe** | **{{ferroviaire.plage.part_fixe_h::n2}} h** | dont {{ferroviaire.plage.part_tenue_par_l_exploitant_h::n2}} h par l'exploitant | *calculé* |

{{ferroviaire.plage.lecture}}

:::figure {"fn":"barres","args":"ferroviaire.figures.plage","titre":"Où passe une plage de consignation de 6 heures","num":1,"large":true,"options":{"unite":"heures d'une plage de consignation"},"voir":["La barre du milieu est la seule qui produise de l'ouvrage : {{ferroviaire.plage.travail_effectif_h::n2}} h sur {{ferroviaire.plage.duree_nominale_h::n0}}, soit {{ferroviaire.plage.rendement_pct::n0}} %.","Les six autres ne sont pas du temps perdu : ce sont des opérations obligatoires, et deux d'entre elles sont faites par l'exploitant, pas par vous.","En dessous de {{ferroviaire.plage.seuil_de_plage_inutile_h::n2}} h de plage, la part fixe consomme tout et la plage ne produit RIEN. Ce seuil est le premier argument d'une demande de plage, et il se calcule au lieu de se plaider."],"erreur":"Annoncer à une équipe « vous avez six heures ». Elle en a trois, et elle le découvrira la première nuit — après avoir dimensionné son opération sur six."}
:::

### b. Les deux effets se multiplient

Le rendement du **temps** n'est pas le seul handicap. À temps égal, une équipe de nuit produit moins
qu'une équipe de jour : éclairage artificiel, zone étroite, fatigue, co-activité avec l'agent de
sécurité. Ce second effet s'applique **par-dessus** le premier.

$$ \text{facteur} = \underbrace{\frac{h_{\text{journée}}}{h_{\text{utiles}}}}_{\text{rendement du temps}} \times \underbrace{\frac{1}{1 - a}}_{\text{abattement de nuit}} $$

Avec {{ferroviaire.plage.travail_effectif_h::n2}} h utiles sur une journée de 8 h et un abattement de
⟦V3|abattement de cadence du travail de nuit, à effectif égal|30|%|15 à 45|2026|éclairage artificiel, fatigue, zone étroite, co-activité avec l'agent de sécurité⟧ %, le facteur vaut
**×{{ferroviaire.plage.facteur_d_interception::n2}}**.

:::encart {"genre":"piege","titre":"L'intuition se trompe, et elle se trompe toujours dans le même sens"}
On raisonne spontanément par addition : « il reste à peu près la moitié du temps, donc il faudra
deux fois plus de nuits ». Les deux effets ne s'additionnent pas, ils se **composent** : il en faut
**{{ferroviaire.plage.facteur_d_interception::n2}} fois** plus.

C'est exactement l'erreur que portait le planning de ce cours, et elle est d'autant plus facile à
commettre que chacun des deux chiffres, pris seul, paraît raisonnable.
:::

### c. Un levage ne se fractionne pas

On peut interrompre un coulage — mal, avec une reprise froide. On n'interrompt pas la pose d'une
ferme à mi-course pour rendre la voie. D'où le **point de non-retour** : l'heure après laquelle on
ne lance plus l'opération, parce qu'on ne pourrait plus la replier.

$$ t_{\text{non-retour}} = t_{\text{fin de plage}} - \left( t_{\text{repli}} + t_{\text{déconsignation}} + t_{\text{marge}} \right) - t_{\text{opération}} $$

C'est la même déduction que la fenêtre de coulage du module C3 — on part de l'heure à laquelle il
faut avoir fini et on recule. La différence est ailleurs : **ici le dépassement n'abîme pas un
ouvrage, il arrête un train.**

{{ferroviaire.point_de_non_retour._qui_decide}}

## S4 · L'étude de cas : la charpente au-dessus des quais

### a. L'opération ne tient pas dans la plage, et les deux seuils qui le disent

{{ferroviaire.point_de_non_retour.lecture}}

| | |
|---|---:|
| Masse d'une pièce levée d'un seul tenant | ⟦V3|masse d'une pièce de charpente levée d'un seul tenant au-dessus de la voie|8|t|4 à 18|2026|fixe la durée d'une opération élémentaire, donc le point de non-retour : plus la pièce est lourde, moins il y a de levages, mais chacun devient impossible à fractionner⟧ t |
| Cadence de levage de nuit | {{ferroviaire.point_de_non_retour.cadence_de_nuit_t_h::n3}} t/h |
| Durée de l'opération | **{{ferroviaire.point_de_non_retour.duree_de_l_operation_h::n2}} h** |
| Temps utile de la plage | {{ferroviaire.plage.travail_effectif_h::n2}} h |
| **Masse maximale levable dans cette plage** | **{{ferroviaire.point_de_non_retour.masse_maximale_d_une_piece_t::n2}} t** |
| **Plage minimale pour la pièce prévue** | **{{ferroviaire.point_de_non_retour.plage_minimale_pour_cette_piece_h::n2}} h** |

{{ferroviaire.point_de_non_retour.les_deux_seuils}}

:::encart {"genre":"voir","titre":"Le vrai enseignement de cette section"}
{{ferroviaire.point_de_non_retour._un_levage_ne_se_fractionne_pas}}

Et surtout : ces deux seuils se calculent **avant** de dessiner la charpente. Une charpente découpée
en pièces de {{ferroviaire.point_de_non_retour.masse_d_une_piece_t::n0}} tonnes sans savoir quelles
plages seront accordées est une charpente qu'on redécoupera — après fabrication, sur des pièces
déjà peintes, avec des assemblages à recalculer. C'est le genre de reprise qui ne se voit dans
aucun planning parce qu'elle n'y était pas prévue.
:::

### b. Ce que la correction fait au planning du cours

| | Avant | Après |
|---|---:|---:|
| Durée de travail de jour (inchangée) | 12,13 j | {{planification.durees.CHLV.duree_de_travail_de_jour_j::n2}} j |
| **Plages de consignation à consommer** | — | **{{ferroviaire.leviers.reference.CHLV_travail_j::n1}}** |
| Fenêtres de consignation nécessaires | 5 | **{{ferroviaire.leviers.reference.fenetres_CHLV}}** |
| Étalement du levage | 80 j | {{ferroviaire.leviers.reference.etalement_CHLV_j::n0}} j |
| Dont immobilisation improductive | 68 j | {{ferroviaire.leviers.reference.immobilisation_improductive_j::n0}} j |
| **Durée du chantier** | 363 j | **{{ferroviaire.leviers.reference.duree_du_chantier_j::n0}} j** |

Entre deux fenêtres, la charpente au-dessus des quais n'avance pas d'un kilogramme : ce n'est pas
une durée de travail, c'est une durée **d'attente ponctuée de travail**. Et la tâche est sur le
chemin critique, donc chaque jour d'attente est un jour de chantier.

### c. Les leviers — et aucun n'est dans le planning

{{ferroviaire.leviers.lecture}}

Chaque levier ci-dessous est **mesuré** en rejouant le réseau de D2, jamais déduit d'une règle de
trois : pré-assembler au sol raccourcit la tâche sous interception **et** allonge celle au sol, et
seul le réseau dit ce qui l'emporte.

| Levier | Plage | Utile | Facteur | Pièce max | Fenêtres | Étalement | Chantier | Écart |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| {{ferroviaire.leviers.lignes.0.levier}} | {{ferroviaire.leviers.lignes.0.plage_h::n0}} h | {{ferroviaire.leviers.lignes.0.travail_effectif_h::n2}} h | ×{{ferroviaire.leviers.lignes.0.facteur_d_interception::n2}} | {{ferroviaire.leviers.lignes.0.masse_maximale_levable_t::n2}} t | {{ferroviaire.leviers.lignes.0.fenetres_CHLV}} | {{ferroviaire.leviers.lignes.0.etalement_CHLV_j::n0}} j | {{ferroviaire.leviers.lignes.0.duree_du_chantier_j::n0}} j | — |
| {{ferroviaire.leviers.lignes.1.levier}} | {{ferroviaire.leviers.lignes.1.plage_h::n0}} h | {{ferroviaire.leviers.lignes.1.travail_effectif_h::n2}} h | ×{{ferroviaire.leviers.lignes.1.facteur_d_interception::n2}} | {{ferroviaire.leviers.lignes.1.masse_maximale_levable_t::n2}} t | {{ferroviaire.leviers.lignes.1.fenetres_CHLV}} | {{ferroviaire.leviers.lignes.1.etalement_CHLV_j::n0}} j | {{ferroviaire.leviers.lignes.1.duree_du_chantier_j::n0}} j | {{ferroviaire.leviers.lignes.1.ecart_de_date_j::n0}} j |
| {{ferroviaire.leviers.lignes.2.levier}} | {{ferroviaire.leviers.lignes.2.plage_h::n0}} h | {{ferroviaire.leviers.lignes.2.travail_effectif_h::n2}} h | ×{{ferroviaire.leviers.lignes.2.facteur_d_interception::n2}} | {{ferroviaire.leviers.lignes.2.masse_maximale_levable_t::n2}} t | {{ferroviaire.leviers.lignes.2.fenetres_CHLV}} | {{ferroviaire.leviers.lignes.2.etalement_CHLV_j::n0}} j | {{ferroviaire.leviers.lignes.2.duree_du_chantier_j::n0}} j | {{ferroviaire.leviers.lignes.2.ecart_de_date_j::n0}} j |
| {{ferroviaire.leviers.lignes.3.levier}} | {{ferroviaire.leviers.lignes.3.plage_h::n0}} h | {{ferroviaire.leviers.lignes.3.travail_effectif_h::n2}} h | ×{{ferroviaire.leviers.lignes.3.facteur_d_interception::n2}} | {{ferroviaire.leviers.lignes.3.masse_maximale_levable_t::n2}} t | {{ferroviaire.leviers.lignes.3.fenetres_CHLV}} | {{ferroviaire.leviers.lignes.3.etalement_CHLV_j::n0}} j | {{ferroviaire.leviers.lignes.3.duree_du_chantier_j::n0}} j | {{ferroviaire.leviers.lignes.3.ecart_de_date_j::n0}} j |
| {{ferroviaire.leviers.lignes.4.levier}} | {{ferroviaire.leviers.lignes.4.plage_h::n0}} h | {{ferroviaire.leviers.lignes.4.travail_effectif_h::n2}} h | ×{{ferroviaire.leviers.lignes.4.facteur_d_interception::n2}} | {{ferroviaire.leviers.lignes.4.masse_maximale_levable_t::n2}} t | {{ferroviaire.leviers.lignes.4.fenetres_CHLV}} | {{ferroviaire.leviers.lignes.4.etalement_CHLV_j::n0}} j | {{ferroviaire.leviers.lignes.4.duree_du_chantier_j::n0}} j | {{ferroviaire.leviers.lignes.4.ecart_de_date_j::n0}} j |
| **{{ferroviaire.leviers.lignes.5.levier}}** | {{ferroviaire.leviers.lignes.5.plage_h::n0}} h | {{ferroviaire.leviers.lignes.5.travail_effectif_h::n2}} h | ×{{ferroviaire.leviers.lignes.5.facteur_d_interception::n2}} | {{ferroviaire.leviers.lignes.5.masse_maximale_levable_t::n2}} t | **{{ferroviaire.leviers.lignes.5.fenetres_CHLV}}** | **{{ferroviaire.leviers.lignes.5.etalement_CHLV_j::n0}} j** | **{{ferroviaire.leviers.lignes.5.duree_du_chantier_j::n0}} j** | **{{ferroviaire.leviers.lignes.5.ecart_de_date_j::n0}} j** |
| {{ferroviaire.leviers.lignes.6.levier}} | {{ferroviaire.leviers.lignes.6.plage_h::n0}} h | {{ferroviaire.leviers.lignes.6.travail_effectif_h::n2}} h | ×{{ferroviaire.leviers.lignes.6.facteur_d_interception::n2}} | {{ferroviaire.leviers.lignes.6.masse_maximale_levable_t::n2}} t | {{ferroviaire.leviers.lignes.6.fenetres_CHLV}} | {{ferroviaire.leviers.lignes.6.etalement_CHLV_j::n0}} j | {{ferroviaire.leviers.lignes.6.duree_du_chantier_j::n0}} j | {{ferroviaire.leviers.lignes.6.ecart_de_date_j::n0}} j |

:::figure {"fn":"barres","args":"ferroviaire.figures.leviers_dates","titre":"Durée du chantier sous chaque levier — mesurée en rejouant le réseau","num":2,"large":true,"options":{"unite":"jours ouvrés de chantier"},"voir":["La ligne en gras du tableau ramène le chantier à {{ferroviaire.leviers.lignes.5.duree_du_chantier_j::n0}} jours, c'est-à-dire exactement la durée que le planning publiait AVANT qu'on découvre le rendement de plage. Le planning avait raison — par accident.","Aucun de ces leviers n'est un levier de planificateur : ils se décident en études, dans la méthode de montage et dans la demande de plages, six mois avant le premier levage.","Deux leviers très différents — une plage de {{ferroviaire.leviers.lignes.1.plage_h::n0}} h, ou du pré-assemblage ramenant la part à {{ferroviaire.leviers.lignes.3.part_sous_interception_pct::n0}} % — donnent presque le même gain ({{ferroviaire.leviers.lignes.1.ecart_de_date_j::n0}} et {{ferroviaire.leviers.lignes.3.ecart_de_date_j::n0}} jours). Ils agissent sur les deux facteurs du même produit, et c'est pour cela qu'ils se valent ICI — pas parce que l'un vaudrait l'autre en général."],"erreur":"Lire ce graphique comme un menu où l'on prend le moins cher. La dernière ligne demande cinq nuits consécutives de consignation : c'est l'exploitant qui décide, et il décide contre la circulation."}
:::

:::figure {"fn":"barres","args":"ferroviaire.figures.leviers","titre":"Étalement du levage sous chaque levier","num":3,"large":true,"options":{"unite":"jours ouvrés entre le premier et le dernier levage"},"voir":["C'est la grandeur que le chef de projet suivi voit sur son planning : non pas le travail, mais l'ATTENTE entre deux fenêtres. Entre elles, la charpente au-dessus des quais n'avance pas d'un kilogramme.","L'écart entre la première barre et la dernière — {{ferroviaire.leviers.lignes.0.etalement_CHLV_j::n0}} contre {{ferroviaire.leviers.lignes.6.etalement_CHLV_j::n0}} jours — ne se gagne pas sur le chantier : il se gagne en études et en négociation.","Comparez avec la figure 2 : l'étalement varie plus que la durée du chantier, parce que le réseau absorbe une partie du gain. C'est la raison pour laquelle on MESURE l'effet au lieu de le déduire."],"erreur":"Confondre cet étalement avec une durée de travail. Les {{ferroviaire.leviers.reference.immobilisation_improductive_j::n0}} jours d'immobilisation improductive de la première ligne ne produisent aucun ouvrage — mais ils coûtent : ils portent les frais de durée du chantier, que le module D1 chiffre. Qui les supporte au final est une question de MARCHÉ, pas de métré, et elle se lit dans le CPS."}
:::

**Ce que ce tableau établit, et c'est le résultat du module :**

> Les {{ferroviaire.leviers.lignes.5.duree_du_chantier_j::n0}} jours du planning n'étaient pas
> atteignables en travaillant plus. Ils n'étaient atteignables qu'avec une **méthode de montage**
> et une **stratégie de plages** que personne n'avait écrites.

**Attention à ce que cette ligne est, et à ce qu'elle n'est pas.** Elle retombe à un dixième de jour
près sur la durée que le cours publiait avant la correction — mais ce n'est **pas le même
planning** : le pré-assemblage allonge la tâche au sol de sept jours, le levage se fait sur un
contenu tout autre, et le chemin critique n'a pas la même forme. Deux plannings différents qui
durent le même temps, c'est une **coïncidence**, pas une validation. Le planning initial avait
raison par accident — et un planning qui a raison par accident se trompera au premier aléa, parce
que personne ne sait pourquoi il avait raison.

:::encart {"genre":"alerte","titre":"Et pourtant aucun de ces leviers ne rend l'opération faisable"}
Lisez la colonne **Pièce max**. Elle ne dépend que de la durée de la plage, jamais de la méthode :
{{ferroviaire.leviers.lignes.0.masse_maximale_levable_t::n2}} t à
{{ferroviaire.leviers.lignes.0.plage_h::n0}} h,
{{ferroviaire.leviers.lignes.2.masse_maximale_levable_t::n2}} t à
{{ferroviaire.leviers.lignes.2.plage_h::n0}} h. La pièce prévue en pèse
{{ferroviaire.point_de_non_retour.masse_d_une_piece_t::n0}}. **Aucune ligne de ce tableau ne permet
de la lever.**

{{ferroviaire.leviers.le_piege_du_pre_assemblage}}

Et le levier le plus efficace sur les dates est précisément celui qui aggrave le problème :
pré-assembler au sol **alourdit** les pièces. Un tableau de leviers qui ne porte que des jours
laisse croire qu'on a le choix ; avec la colonne des masses, on voit que le seul levier qui déplace
la faisabilité est **la durée de la plage**.
:::

{{ferroviaire.point_de_non_retour._divisibilite}}

{{ferroviaire.leviers._le_levier_le_plus_efficace_n_est_pas_gratuit}}

{{ferroviaire.leviers._hors_fourchette}}

### d. Le coût d'une heure utile

On paie la plage **entière**, majorée de la nuit, pour les
{{ferroviaire.plage.travail_effectif_h::n2}} h qu'elle contient.

| | |
|---|---:|
| Taux horaire de jour | {{ferroviaire.cout.taux_horaire_de_jour_MAD::n0}} MAD/h |
| Majoration de nuit | ⟦V3|majoration du taux horaire pour le travail de nuit|50|%|30 à 100|2026|valeur CONTRACTUELLE et non technique : à vérifier dans le CPS et la convention applicable⟧ % |
| Coût d'une plage, par compagnon | {{ferroviaire.cout.cout_d_une_plage_MAD_par_compagnon::n0}} MAD |
| **Coût de l'heure UTILE** | **{{ferroviaire.cout.cout_de_l_heure_UTILE_MAD::n0}} MAD/h** |
| Rapport à une heure d'**ouvrage** de jour | **×{{ferroviaire.cout.rapport_a_l_heure_d_OUVRAGE_de_jour::n1}}** |

{{ferroviaire.cout.lecture}}

**Le domaine de ce ratio.** {{ferroviaire.cout.ratio_defini_sur_cette_base}}

{{ferroviaire.cout._avertissement_contractuel}}

### e. Les interfaces : il n'y a pas un seul donneur d'ordre

{{ferroviaire.interfaces.lecture}}

| Délai | De → à | Objet | Nature |
|---:|---|---|---|
| **{{ferroviaire.interfaces.liste.0.delai_de_demande_j}} j** | {{ferroviaire.interfaces.liste.0.de}} → {{ferroviaire.interfaces.liste.0.a}} | {{ferroviaire.interfaces.liste.0.objet}} | {{ferroviaire.interfaces.liste.0.nature}} |
| {{ferroviaire.interfaces.liste.1.delai_de_demande_j}} j | {{ferroviaire.interfaces.liste.1.de}} → {{ferroviaire.interfaces.liste.1.a}} | {{ferroviaire.interfaces.liste.1.objet}} | {{ferroviaire.interfaces.liste.1.nature}} |
| {{ferroviaire.interfaces.liste.2.delai_de_demande_j}} j | {{ferroviaire.interfaces.liste.2.de}} → {{ferroviaire.interfaces.liste.2.a}} | {{ferroviaire.interfaces.liste.2.objet}} | {{ferroviaire.interfaces.liste.2.nature}} |
| {{ferroviaire.interfaces.liste.3.delai_de_demande_j}} j | {{ferroviaire.interfaces.liste.3.de}} → {{ferroviaire.interfaces.liste.3.a}} | {{ferroviaire.interfaces.liste.3.objet}} | {{ferroviaire.interfaces.liste.3.nature}} |
| {{ferroviaire.interfaces.liste.4.delai_de_demande_j}} j | {{ferroviaire.interfaces.liste.4.de}} → {{ferroviaire.interfaces.liste.4.a}} | {{ferroviaire.interfaces.liste.4.objet}} | {{ferroviaire.interfaces.liste.4.nature}} |
| {{ferroviaire.interfaces.liste.5.delai_de_demande_j}} j | {{ferroviaire.interfaces.liste.5.de}} → {{ferroviaire.interfaces.liste.5.a}} | {{ferroviaire.interfaces.liste.5.objet}} | {{ferroviaire.interfaces.liste.5.nature}} |
| {{ferroviaire.interfaces.liste.6.delai_de_demande_j}} j | {{ferroviaire.interfaces.liste.6.de}} → {{ferroviaire.interfaces.liste.6.a}} | {{ferroviaire.interfaces.liste.6.objet}} | {{ferroviaire.interfaces.liste.6.nature}} |

{{ferroviaire.interfaces.la_regle_du_delai}}

{{ferroviaire.interfaces.decision_contre_information}}

## S4g · Sécurité : le seul module où une erreur tue directement

Le § 3.4 impose de dire ce qu'une phase décide en matière de risque. Ici les dispositions ne sont
pas « essentielles et non exhaustives » comme ailleurs : elles sont **un rappel de l'existence d'un
domaine entier qui ne s'apprend pas dans un cours**. Aucune distance, aucun gabarit, aucune règle de
consignation n'est chiffré — toutes sont réglementaires et relèvent des procédures de l'exploitant.

| Ce que le chantier décide | Le risque | La disposition, et qui la tient |
|---|---|---|
| **Travailler près d'une voie circulée** | heurt par circulation | personne n'approche d'une voie ouverte sans dispositif d'annonce ou fermeture effective. L'**agent de sécurité ferroviaire** n'est pas un figurant : il a le pouvoir d'arrêter le chantier, et il l'exerce seul |
| **Lever au-dessus d'une voie** | chute de charge sur la voie, déraillement | aucun levage au-dessus ou à proximité d'une voie non fermée, quel que soit l'horaire et quelle que soit la pression du planning. La mise en girouette d'une grue par grand vent doit être étudiée pour ne pas survoler la voie |
| **Approcher d'une caténaire** | électrisation, arc à distance | la consignation et la vérification d'absence de tension sont faites par un **agent habilité de l'exploitant**, jamais par l'entreprise, et la mise à la terre se pose avant toute approche |
| **Rendre la voie** | train sur obstacle | le contrôle de libération du gabarit est un acte formel, tracé, fait avant la déconsignation — pas un coup d'œil en repliant |
| **Travailler de nuit** | fatigue, visibilité, improvisation | éclairage de l'aire et des circulations, balisage des zones de manœuvre, un homme dédié au guidage des camions. Un travail de nuit improvisé pour tenir une plage échange un risque contre un autre |
| **Coactivité avec les voyageurs** | chute, heurt, panique | les circulations voyageurs d'une gare en service ne se ferment pas : elles se dévient, et la déviation se conçoit avec l'exploitant, pas avec le chef de chantier |

**Le lien avec tout ce module, et il est direct.** Le § S4a montre qu'une opération de levage ne
tient pas dans la plage prévue. La tentation, à trois heures du matin, après avoir tout préparé, est
de lancer quand même « parce qu'on devrait y arriver ». **C'est précisément pour cela que la
décision de lancement se délègue par écrit, avant la plage, à quelqu'un dont le travail n'est pas en
jeu.** Un point de non-retour qui se discute dans l'instant n'est pas un point de non-retour.

## S5 · Erreurs fréquentes, et ce qu'elles coûtent

| Erreur | Comment elle se voit | Ce qu'elle coûte |
|---|---|---|
| Chiffrer une tâche sous consignation comme une tâche de jour | le planning est beau | ×{{ferroviaire.plage.facteur_d_interception::n2}} sur la durée, et c'est l'erreur que portait ce cours |
| Additionner les deux effets au lieu de les composer | on prévoit deux fois plus de nuits | il en faut {{ferroviaire.plage.facteur_d_interception::n2}} fois plus |
| Annoncer la durée de la **plage** à l'équipe | l'opération est dimensionnée sur {{ferroviaire.plage.duree_nominale_h::n0}} h | elle en a {{ferroviaire.plage.travail_effectif_h::n2}} |
| Dimensionner la charpente sans connaître les plages | tout va bien jusqu'au montage | des pièces de {{ferroviaire.point_de_non_retour.masse_d_une_piece_t::n0}} t à redécouper après fabrication |
| Laisser le chef d'équipe décider du lancement | il décide de lancer, toujours | une voie restituée en retard, et un train arrêté |
| Rallonger le planning au lieu de changer la méthode | personne ne conteste un planning | {{ferroviaire.leviers.lignes.5.ecart_de_date_j::n0}} jours qu'on pouvait gagner en études |
| Traiter une interface de **décision** par courriel | tout le monde a l'information, personne n'a tranché | une plage demandée trop tard, qui ne revient pas avant {{ferroviaire.interfaces.delai_le_plus_long_j}} jours |
| Comparer le coût de nuit au **taux horaire** de jour | l'écart paraît être la majoration | ×{{ferroviaire.cout.rapport_a_l_heure_d_OUVRAGE_de_jour::n1}} en réalité, contre ×{{ferroviaire.cout.rapport_au_taux_de_jour::n1}} au taux brut |
| Croire qu'une plage perdue se rattrape | « on la reprendra la semaine prochaine » | elle se reprend au cycle suivant, soit un mois |

## S6 · Exercices

:::exercice {"titre":"1 · Combien de temps avez-vous vraiment ?","niveau":"application"}
L'exploitant vous accorde une plage de {{ferroviaire.plage.duree_nominale_h::n0}} h, de 23 h à 5 h.
Votre chef de chantier prévoit une opération de 5 h et vous annonce « ça passe large ». Qu'en
dites-vous ?

**Corrigé.** Ça ne passe pas du tout, et l'écart n'est pas une question de marge.

Le travail effectif de la plage vaut {{ferroviaire.plage.travail_effectif_h::n2}} h :
{{ferroviaire.plage.avant_travail_h::n2}} h sont consommées avant que le premier geste utile soit
possible, {{ferroviaire.plage.apres_travail_h::n2}} h après le dernier. Une opération de 5 h ne tient
pas dans {{ferroviaire.plage.travail_effectif_h::n2}} h — elle n'en est même pas près.

**Et la réponse à donner n'est pas « réduisez votre opération ».** C'est :

1. **de combien de temps l'opération a-t-elle vraiment besoin ?** Si c'est 5 h, il faut une plage
   d'au moins {{ferroviaire.plage.seuil_de_plage_inutile_h::n2}} + 5 = 8,15 h ;
2. **peut-elle se fractionner ?** Un levage, non. Un ferraillage de quai, oui ;
3. **sinon, la demande de plage est à refaire**, et elle prend
   ⟦V3|délai entre la demande d'une plage de consignation et son obtention|120|jours|60 à 240|2026|c'est ce délai qui rend une plage perdue irrattrapable : on ne la redemande pas pour la semaine suivante⟧ jours dans le pire des cas.

*Le piège est de croire que le sujet est l'opération. Le sujet est la plage, et elle se négocie des
mois avant — pas la veille avec le chef de chantier.*
:::

:::exercice {"titre":"2 · L'exploitant propose des plages de 4 h","niveau":"probleme"}
Négociation en cours. L'exploitant refuse les plages de
{{ferroviaire.plage.duree_nominale_h::n0}} h et propose à la place **deux fois plus de plages de
4 h**. Son argument : « vous aurez deux fois plus d'heures de fermeture ». Acceptez-vous ?

**Corrigé. Non, et c'est démontrable en une soustraction.**

La part fixe vaut {{ferroviaire.plage.seuil_de_plage_inutile_h::n2}} h **par plage**, qu'elle dure
4 h ou 10 h. Deux plages courtes la paient donc **deux fois**.

| Plage | Utile | Rendement | Utile par heure de **fermeture** |
|---:|---:|---:|---:|
| {{ferroviaire.comparaison_de_plages.lignes.0.plage_h::n0}} h | {{ferroviaire.comparaison_de_plages.lignes.0.utile_h::n2}} h | {{ferroviaire.comparaison_de_plages.lignes.0.rendement_pct::n1}} % | {{ferroviaire.comparaison_de_plages.lignes.0.utile_par_heure_de_fermeture::n3}} |
| {{ferroviaire.comparaison_de_plages.lignes.1.plage_h::n0}} h | {{ferroviaire.comparaison_de_plages.lignes.1.utile_h::n2}} h | {{ferroviaire.comparaison_de_plages.lignes.1.rendement_pct::n1}} % | {{ferroviaire.comparaison_de_plages.lignes.1.utile_par_heure_de_fermeture::n3}} |
| {{ferroviaire.comparaison_de_plages.lignes.2.plage_h::n0}} h | {{ferroviaire.comparaison_de_plages.lignes.2.utile_h::n2}} h | {{ferroviaire.comparaison_de_plages.lignes.2.rendement_pct::n1}} % | {{ferroviaire.comparaison_de_plages.lignes.2.utile_par_heure_de_fermeture::n3}} |
| {{ferroviaire.comparaison_de_plages.lignes.3.plage_h::n0}} h | {{ferroviaire.comparaison_de_plages.lignes.3.utile_h::n2}} h | {{ferroviaire.comparaison_de_plages.lignes.3.rendement_pct::n1}} % | {{ferroviaire.comparaison_de_plages.lignes.3.utile_par_heure_de_fermeture::n3}} |

**La comparaison à durée de fermeture égale.** Deux plages de 4 h, c'est 8 h de voie fermée, et
elles donnent {{ferroviaire.comparaison_de_plages.deux_courtes_contre_une_longue.deux_de_4h_utile_h::n2}} h
utiles. **Une seule** plage de 8 h ferme la voie aussi longtemps et en donne
{{ferroviaire.comparaison_de_plages.deux_courtes_contre_une_longue.une_de_8h_utile_h::n2}} h, soit
**{{ferroviaire.comparaison_de_plages.deux_courtes_contre_une_longue.rapport::n2}} fois plus**.

Et d'une plage à l'autre, le rendement par heure de fermeture varie d'un facteur
**{{ferroviaire.comparaison_de_plages.rapport_meilleure_sur_pire::n2}}** entre la plus courte et la
plus longue.

{{ferroviaire.comparaison_de_plages.lecture}}

*Ce que cet exercice enseigne : la part fixe est l'argument de négociation le plus solide d'un
chantier ferroviaire, et c'est une soustraction. Elle déplace aussi la discussion — du confort de
l'entreprise vers l'efficacité de la fermeture, qui est l'intérêt de l'exploitant.*

*Et le piège du piège : « deux fois plus d'heures de fermeture » n'est pas « deux fois plus
d'heures ». Raisonner en total d'heures de fermeture est exactement le raisonnement que tient
naturellement celui qui accorde les plages. Il n'est pas de mauvaise foi : il compte une grandeur
qui n'est pas celle qui produit.*
:::

:::exercice {"titre":"3 · Le planning est en retard de onze mois. Que proposez-vous ?","niveau":"cas_ouvert"}
Vous reprenez le dossier. Le levage de charpente au-dessus des quais, chiffré 12 jours de travail,
s'étale en réalité sur {{ferroviaire.leviers.reference.etalement_CHLV_j::n0}} jours et porte la fin
du chantier à {{ferroviaire.leviers.reference.duree_du_chantier_j::n0}} jours ouvrés. Le maître
d'ouvrage demande un plan de rattrapage sous quinze jours.

**Corrigé.** Trois choses, et la première n'est pas un levier.

**1. Dire d'où vient l'écart, avant de proposer quoi que ce soit.** La tâche n'a pas dérivé : elle a
été **mal chiffrée dès l'origine**, comme un travail de jour. Présenter des leviers sans dire cela,
c'est laisser croire à un problème d'exécution — et la première question du maître d'ouvrage sera
« pourquoi votre entreprise n'avance-t-elle pas ? », qui est la mauvaise question.

**2. Proposer les leviers avec leur effet MESURÉ et leur contrepartie**, pas une liste d'intentions :

- négocier une plage de {{ferroviaire.leviers.lignes.1.plage_h::n0}} h →
  {{ferroviaire.leviers.lignes.1.ecart_de_date_j::n0}} jours, mais c'est l'exploitant qui arbitre,
  contre la circulation ;
- pré-assembler au sol pour ramener la part levée sous interception à
  {{ferroviaire.leviers.lignes.4.part_sous_interception_pct::n0}} % →
  {{ferroviaire.leviers.lignes.4.ecart_de_date_j::n0}} jours, mais emprise au sol, pièces plus
  lourdes, grue plus forte ;
- **les deux** → {{ferroviaire.leviers.lignes.5.ecart_de_date_j::n0}} jours, ce qui ramène le
  chantier à {{ferroviaire.leviers.lignes.5.duree_du_chantier_j::n0}} jours.

**3. Dire ce que le calcul ne price pas.** Le réseau mesure les jours ; il ne mesure ni l'emprise
au sol dont on ne dispose peut-être pas, ni la capacité de la grue, ni le risque propre à un levage
de pièce plus lourde. Un levier qui gagne deux cents jours et demande une grue qu'on n'a pas n'est
pas un levier — c'est une ligne de tableau.

*Et le vrai sujet, celui qu'on ne voit qu'après coup : les deux leviers se décident en **études**,
pas en travaux. Quinze jours avant le premier levage, aucun des deux n'est actionnable — la
charpente est fabriquée et les plages de l'année sont réservées. La seule chose qu'on puisse
encore faire est de les activer pour les **phases suivantes**, et de le dire.*
:::

## S7 · Check-list, glossaire et quiz

**Check-list : une tâche sous interception, en études**

1. La tâche est-elle classée **sous interception**, **à proximité**, ou **hors interception** — et
   qui l'a classée ?
2. Le **rendement** de la plage a-t-il été appliqué à sa durée, ou l'a-t-on chiffrée comme un
   travail de jour ?
3. La **masse d'une pièce** et la **durée de plage** sont-elles compatibles, dans les deux sens ?
4. L'opération peut-elle se **fractionner** ? Si non, le point de non-retour est une contrainte
   dure.
5. Les plages sont-elles **demandées** avec le délai nécessaire — et par qui ?
6. Qui **décide** du lancement la nuit, et est-ce écrit avant la plage ?
7. Les interfaces de **décision** sont-elles distinguées de celles d'information ?
8. Le coût est-il chiffré sur l'heure **utile**, et non sur la plage ?

**Glossaire**

| Terme | Ce que c'est |
|---|---|
| **Plage travaux** | période pendant laquelle la voie est fermée à la circulation et remise à l'entreprise |
| **Consignation** | mise hors tension de la caténaire, suivie de la mise à la terre et de la vérification d'absence de tension. Acte de l'exploitant |
| **Restitution** | remise de la voie à la circulation. L'heure n'est pas négociable |
| **Gabarit** | volume autour de la voie dans lequel rien ne doit pénétrer. Les valeurs sont réglementaires — ⏸ |
| **Agent de sécurité ferroviaire** | agent qui tient la sécurité de la zone et peut arrêter le chantier seul |
| **Interception** | fait qu'une tâche nécessite la fermeture d'une voie |
| **Point de non-retour** | heure après laquelle une opération ne peut plus être lancée, faute de pouvoir la replier |
| **Gestionnaire d'infrastructure** | propriétaire de la voie et des systèmes. Un **autre** maître d'ouvrage, pas un prestataire |

**Quiz**

**1. Une plage de 6 h, c'est combien de travail ?**
**{{ferroviaire.plage.travail_effectif_h::n2}} h**, soit {{ferroviaire.plage.rendement_pct::n0}} %.
La part fixe vaut {{ferroviaire.plage.part_fixe_h::n2}} h, dont
{{ferroviaire.plage.part_tenue_par_l_exploitant_h::n2}} h tenues par l'exploitant.

**2. Doubler l'équipe réduit-il la part fixe ?**
**Non, d'aucune minute.** C'est ce qui distingue un chantier ferroviaire : un retard ne se rattrape
pas avec des moyens, il se rattrape avec des **plages** — et elles se demandent des mois à l'avance.

**3. Le rendement est de {{ferroviaire.plage.rendement_pct::n0}} % et l'abattement de nuit de {{ferroviaire.plage.abattement_de_cadence_nuit_pct::n0}} %. Facteur ?**
**×{{ferroviaire.plage.facteur_d_interception::n2}}**, et non ×2,1. Les deux effets se
**multiplient** : le rendement porte sur le temps, l'abattement sur le travail fait pendant ce temps.

**4. Quelle est la pièce la plus lourde qu'on puisse lever dans cette plage ?**
**{{ferroviaire.point_de_non_retour.masse_maximale_d_une_piece_t::n2}} t.** Et pour la pièce de
{{ferroviaire.point_de_non_retour.masse_d_une_piece_t::n0}} t prévue, il faudrait une plage de
{{ferroviaire.point_de_non_retour.plage_minimale_pour_cette_piece_h::n2}} h. Ces deux nombres sont
les deux faces du même fait, et ils se calculent en études.

**5. Qui décide de lancer une opération à vingt minutes du point de non-retour ?**
**Pas celui qui l'a préparée.** La décision se délègue par écrit, avant la plage, à quelqu'un dont
le travail n'est pas en jeu — le plus souvent le responsable de la sécurité ferroviaire.

**6. Une heure de travail sous interception coûte combien de fois une heure de jour ?**
**×{{ferroviaire.cout.rapport_a_l_heure_d_OUVRAGE_de_jour::n1}}**, à ouvrage égal. La majoration de
nuit n'en explique qu'une petite part : l'essentiel vient de ce qu'on paie la plage entière pour
{{ferroviaire.plage.travail_effectif_h::n2}} h utiles.

**7. Le gestionnaire d'infrastructure refuse une plage. Qui tranche ?**
**Personne au-dessus de lui, de votre côté.** C'est un **autre maître d'ouvrage** : votre maître
d'ouvrage ne lui donne pas d'ordre. L'interface est une coordination, pas une hiérarchie, et c'est
la différence de fond avec un chantier de bâtiment ordinaire.

:::memo
## Fiche mémo — construire à côté d'une voie exploitée

**La seule chose à retenir**

> Une plage de consignation n'est pas un créneau de travail. La part fixe ne dépend ni de
> l'effectif, ni de la quantité, ni de la motivation — et une partie appartient à l'exploitant.

**Les trois formules**

$$ h_{\text{utiles}} = h_{\text{plage}} - h_{\text{fixe}} \qquad \text{facteur} = \frac{h_{\text{journée}}}{h_{\text{utiles}}} \cdot \frac{1}{1-a} \qquad t_{\text{non-retour}} = h_{\text{plage}} - h_{\text{après}} - t_{\text{op}} $$

**Les chiffres de ce chantier**

| | |
|---|---:|
| Plage nominale | {{ferroviaire.plage.duree_nominale_h::n0}} h |
| Part fixe (dont {{ferroviaire.plage.part_tenue_par_l_exploitant_h::n2}} h exploitant) | {{ferroviaire.plage.part_fixe_h::n2}} h |
| **Travail effectif** | **{{ferroviaire.plage.travail_effectif_h::n2}} h · {{ferroviaire.plage.rendement_pct::n0}} %** |
| Facteur d'interception | ×{{ferroviaire.plage.facteur_d_interception::n2}} |
| Plage en dessous de laquelle rien ne se produit | {{ferroviaire.plage.seuil_de_plage_inutile_h::n2}} h |
| Pièce maximale levable | {{ferroviaire.point_de_non_retour.masse_maximale_d_une_piece_t::n2}} t |
| Heure utile | {{ferroviaire.cout.cout_de_l_heure_UTILE_MAD::n0}} MAD · ×{{ferroviaire.cout.rapport_a_l_heure_d_OUVRAGE_de_jour::n1}} une heure de jour |
| Interfaces actives (dont décisions) | {{ferroviaire.interfaces.interfaces_actives}} ({{ferroviaire.interfaces.dont_decisions}}) sur {{ferroviaire.interfaces.interfaces_possibles}} possibles |
| Délai d'interface le plus long | {{ferroviaire.interfaces.delai_le_plus_long_j}} j |

**Les quatre réflexes**

1. Ne jamais annoncer la durée de la **plage** à une équipe : annoncer le temps **utile**.
2. Vérifier dans les **deux sens** que la pièce et la plage sont compatibles — en études.
3. Déléguer par **écrit**, avant la plage, la décision de lancement.
4. Distinguer une interface de **décision** d'une interface d'information : la première produit un
   document signé, la seconde une diffusion.

**⏸ Ce qui reste fermé sans les documents** — gabarit, distances de sécurité aux caténaires, hauteur
et lacune quai–matériel, charges ferroviaires, résistance au feu des locaux techniques. Toutes ces
valeurs sont réglementaires ou propres à l'exploitant. Le module en donne le principe et la
conséquence sur le chantier, jamais la valeur.
:::
