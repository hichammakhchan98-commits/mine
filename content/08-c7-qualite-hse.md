---
id: C7
titre: Qualité, HSE, environnement — ce qui rend la sécurité pilotable
fil: Palier 1 · module 7 — exécution et chantier
resume: On ne pilote pas la sécurité avec un effectif : on la pilote avec des heures exposées. Et le coût d'une non-conformité n'est pas le coût de sa reprise — c'est ce que la reprise déclenche, et qui n'a pas de facture.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · aucune fréquence de prélèvement, aucun critère de résistance, aucune distance de sécurité n'est chiffré
pied: Exemple pédagogique — ne remplace ni un plan de contrôle, ni un plan de prévention, ni une analyse de risques de chantier. La sécurité d'un chantier réel se prépare avec les personnes qui y travaillent.
donnees: qualite, planification, prix, gare
---

## S1 · Ce que ce module fait, et ce qu'il ne peut pas faire

La qualité et la sécurité sont les deux sujets sur lesquels un cours peut faire le plus de dégâts,
parce qu'ils se prêtent au discours. « Il faut une culture sécurité », « la qualité est l'affaire de
tous » : c'est vrai, c'est inattaquable, et ça n'aide personne un mardi matin.

Ce module traite donc trois choses **qui se calculent**, et qui ne dépendent d'aucune norme :

1. **l'exposition au risque se compte en HEURES**, jamais en effectif ni en durée — et ce cours
   connaît ses heures tâche par tâche, dans un périmètre qu'il faut énoncer avant de s'en servir
   (§ S2) ;
2. **le coût d'une non-conformité dépend entièrement de l'ouvrage qu'elle touche** — un facteur
   {{qualite.non_conformite.ecart_entre_les_regimes::n0}} sur ce chantier, pour le même défaut et la
   même reprise ;
3. **la criticité d'un risque est un produit de rangs** : elle classe, elle ne mesure pas — et c'est
   l'outil le plus utilisé et le plus mal lu des analyses de risques.

Ce qu'il ne fait pas : citer une fréquence de prélèvement, un critère de résistance, une distance de
sécurité, un seuil d'exposition. Toutes ces valeurs sont réglementaires ou propres au marché, et
elles restent **⏸**. Un plan de contrôle qui les contiendrait serait faux dès le premier chantier
où le CPS diffère.

**Comment les chiffres de ce module sont vérifiés.** Les heures ne sont pas crues sur parole : le
module D2 les obtient par les cadences et les effectifs, le module D1 les retrouve par les prix et
les heures payées, et un test de la chaîne **exige qu'ils tombent d'accord tâche par tâche** — une
exception près, nommée et consignée en dette. C'est la seconde voie de ce module au sens du § 3.3 :
elle ne vérifie pas les taux, qui sont des hypothèses, elle vérifie l'assiette sur laquelle ils
s'appliquent. S'y ajoute un étalonnage sur cas fermés (`calc/etalonnage/qualite_cas_ferme.py`) :
un million d'heures à un taux de 28 doit donner 28 accidents, et un invariant — la pondération de
la nuit ne change jamais le total — est vérifié à cinq coefficients différents.

**Et les bornes.** Toutes les entrées de ce module sont des hypothèses déclarées à fourchette
large. Chaque résultat est donc publié **avec ses deux bornes** (D-036), et il y a des cas où elles
sont instructives : le coût d'une non-conformité varie d'un facteur vingt, alors que l'**écart entre
les régimes**, lui, ne bouge pas. C'est le rapport qui porte l'enseignement, jamais le montant.

:::encart {"genre":"attente","titre":"Ce qu'un cours ne remplace pas"}
Un module de huit pages ne forme personne à la sécurité d'un chantier. Ce qui suit sert à **piloter**
— dimensionner, comparer, décider où mettre l'effort — pas à prévenir. La prévention se fait avec
les compagnons, sur le terrain, avec ceux qui connaissent le geste. Le chef de projet suivi qui
croit faire de la sécurité en tenant un tableau de bord fait de la gestion ; c'est utile, et ce n'est
pas la même chose.
:::

## S2 · L'idée centrale : l'exposition se compte en heures

Prenez deux chantiers. Le premier emploie dix compagnons pendant deux ans. Le second en emploie cent
pendant deux mois. Même effectif moyen ? Non. Même durée ? Non. **Même nombre d'heures ?** Presque —
et c'est la seule grandeur qui permette de les comparer.

C'est pourquoi tous les indicateurs de sécurité ont des **heures travaillées** au dénominateur :

$$ TF = \frac{\text{accidents avec arrêt} \times 10^6}{\text{heures travaillées}} \qquad TG = \frac{\text{journées perdues} \times 10^3}{\text{heures travaillées}} $$

Et ce n'est pas une convention arbitraire : c'est le même raisonnement que le module D4 applique aux
avancements. **Un pourcentage sans dénominateur ne se compare à rien, et un indicateur de sécurité
rapporté à un effectif n'en est pas un.**

{{qualite.exposition._pourquoi_pas_l_effectif}}

### Les deux frontières de l'assiette, avant de s'en servir

**Première frontière : le site.** {{qualite.exposition.assiette.note}} Les tâches concernées sont
{{qualite.exposition.assiette.taches_sans_heures}}.

{{qualite.exposition.assiette.consequence}}

**Seconde frontière : les entreprises.** {{qualite.exposition.assiette.perimetre_des_entreprises}}

:::encart {"genre":"piege","titre":"Deux taux de fréquence ne se comparent pas sans comparer leurs périmètres"}
C'est le piège classique du métier, et il a l'élégance de ne jamais se voir : un taux calculé sur
le périmètre de l'entreprise générale seule est **structurellement meilleur** que le même taux
calculé sur toutes les entreprises présentes, puisqu'il retire du dénominateur les heures les plus
exposées — celles des sous-traitants qui font le travail manuel. Aucun accident n'a été évité, et
l'indicateur a progressé.

Un chef de projet suivi à qui l'on présente un taux pose donc toujours trois questions avant de le
lire : **sur quelles heures**, **de quelles entreprises**, et **sur quelle période**. Sans les
trois, un taux de fréquence est un nombre, pas un indicateur.
:::

### Ce que ça donne sur ce chantier

{{qualite.exposition.lecture}}

| | |
|---|---:|
| Heures travaillées | {{qualite.exposition.heures_totales::n0}} h |
| dont heures de nuit sous interception | {{qualite.exposition.heures_de_nuit::n0}} h · {{qualite.exposition.part_de_nuit_pct::n1}} % |
| Coefficient de surexposition de nuit | ⟦V3|surexposition du travail de nuit, par heure travaillée|1,8|—|1,2 à 3,0|2026|éclairage artificiel, fatigue, zone étroite, co-activité ferroviaire : ordre de grandeur déclaré, non une statistique du projet⟧ |
| **Part de la nuit dans le risque** | **{{qualite.exposition.part_de_nuit_dans_le_risque_pct::n1}} %** |
| Taux de gravité de référence | ⟦V3|taux de gravité, journées perdues par millier d'heures|1,4|—|0,6 à 3,0|2026|ordre de grandeur du BTP, à confronter aux statistiques de l'entreprise⟧ |
| Taux de fréquence de référence | ⟦V3|taux de fréquence, accidents avec arrêt par million d'heures|28|—|12 à 50|2026|ordre de grandeur du BTP, à confronter aux statistiques de l'entreprise : ce n'est pas un objectif, c'est une référence de calcul⟧ |
| Accidents avec arrêt attendus | {{qualite.exposition.accidents_avec_arret_attendus::n2}} · bornes **{{qualite.exposition.accidents_bornes.0::n2}} à {{qualite.exposition.accidents_bornes.1::n2}}** |
| dont attribuables à la nuit | {{qualite.exposition.dont_attribuables_a_la_nuit::n2}} |
| Journées perdues attendues | {{qualite.exposition.journees_perdues_attendues::n0}} · bornes **{{qualite.exposition.journees_perdues_bornes.0::n0}} à {{qualite.exposition.journees_perdues_bornes.1::n0}}** |

{{qualite.exposition._bornes}}

### Pourquoi 8 % des heures ne font pas 14 % du risque

Le lecteur qui vérifie de tête multiplie {{qualite.exposition.part_de_nuit_pct::n1}} % par
{{qualite.exposition.coefficient_de_surexposition_de_nuit}} et trouve un chiffre plus grand que
celui du tableau. Il a raison de s'en étonner, et voici le compte exact :

{{qualite.exposition._pourquoi_le_rapport_n_est_pas_le_coefficient}}

### « Nuit » et « consignation » sont ici le même mot

Le tableau parle d'heures de nuit ; la donnée, elle, parle de tâches **soumises à consignation**.
Ce n'est pas un glissement de vocabulaire :

{{qualite.exposition.presence_et_production_de_nuit.note}}

| | |
|---|---:|
| Durée d'une plage de consignation | {{qualite.exposition.presence_et_production_de_nuit.duree_de_la_plage_h::n1}} h |
| dont travail effectif | {{qualite.exposition.presence_et_production_de_nuit.travail_effectif_h::n2}} h |
| dont préalables et restitution | {{qualite.exposition.presence_et_production_de_nuit.part_fixe_h::n2}} h |
| **Exposition rapportée au temps productif** | **×{{qualite.exposition.presence_et_production_de_nuit.rapport_presence_production::n2}}** |

C'est un résultat que ni le module B7c ni le module D1 ne pouvaient voir, parce qu'ils comptent
l'un et l'autre le temps **productif** : la nuit d'interception est deux fois plus exposante
qu'elle n'est productive, et les heures les plus dangereuses de la plage — consignation, amenée
des moyens, repli — sont précisément celles que personne ne facture.

:::encart {"genre":"piege","titre":"La pondération répartit le risque, elle ne l'ajoute pas"}
{{qualite.exposition._la_ponderation_repartit_elle_n_ajoute_pas}}

Le piège est subtil et il a coûté une première version de ce module : il paraît naturel d'appliquer
le taux de référence aux heures **pondérées**, puisque ce sont elles qui portent le risque. C'est un
double compte, et il se repère à un signe — **monter le coefficient rendrait le chantier plus
dangereux au total**, alors qu'on n'a fait que changer une clé de répartition.
:::

:::encart {"genre":"piege","titre":"Ce nombre n'est ni une prévision ni un objectif"}
{{qualite.exposition._ce_que_le_nombre_d_accidents_n_est_pas}}

Il sert à **dimensionner** — combien de secouristes, quelle organisation des secours, quel budget de
prévention — et à **comparer** un chantier à un autre. Il ne se communique pas tel quel, et surtout
pas au maître d'ouvrage : un nombre d'accidents annoncé devient une permission.
:::

:::figure {"fn":"barres","args":"qualite.figures.exposition","titre":"Où sont les heures travaillées, tâche par tâche","num":1,"large":true,"options":{"unite":"heures de main-d'œuvre"},"voir":["Les tâches les plus exposées ne sont pas les plus longues : une tâche de huit mois à deux compagnons expose moins qu'une tâche d'un mois à vingt. C'est pour cela qu'on classe par heures et non par durée.","Le second œuvre domine, et c'est normal : il concentre la main-d'œuvre. C'est pourtant la phase où l'attention sécurité retombe, parce que le gros œuvre paraît plus dangereux.","Les tâches de nuit sont peu d'heures et beaucoup de risque : {{qualite.exposition.part_de_nuit_pct::n1}} % des heures pour {{qualite.exposition.part_de_nuit_dans_le_risque_pct::n1}} % du risque pondéré."],"erreur":"Concentrer la prévention sur les tâches spectaculaires — levage, fouille — et la relâcher sur celles qui portent les heures. Le risque total d'une tâche est le produit de son danger par son exposition, et l'exposition se lit ici."}
:::

## S3 · Principes

### a. Les cinq colonnes d'un plan de contrôle

Un plan de contrôle n'est pas une liste de bonnes intentions. Chaque ligne porte cinq informations,
et il en manque presque toujours au moins une :

{{qualite.plan_de_controle.les_cinq_colonnes.0}} · {{qualite.plan_de_controle.les_cinq_colonnes.1}} ·
{{qualite.plan_de_controle.les_cinq_colonnes.2}} · {{qualite.plan_de_controle.les_cinq_colonnes.3}} ·
{{qualite.plan_de_controle.les_cinq_colonnes.4}}

{{qualite.plan_de_controle.la_regle}}

### b. Le délai du résultat change la nature du contrôle

C'est la colonne qu'on omet le plus souvent, et elle est décisive.

{{qualite.plan_de_controle.controles_qui_ne_protegent_pas_leur_ouvrage}}

Un contrôle dont le résultat arrive **immédiatement** protège l'ouvrage qu'il mesure : on peut encore
refuser la toupie, ne pas lever le point d'arrêt, arrêter le coulage. Un contrôle dont le résultat
arrive **après** ne le protège plus — l'ouvrage est construit. Ce sont deux outils différents, et les
traiter pareil conduit à deux erreurs symétriques : attendre un résultat qui ne viendra pas à temps,
ou ignorer un résultat parce qu'il arrive trop tard pour l'ouvrage qu'il concerne.

### c. La criticité classe, elle ne mesure pas

$$ C = f \times g \times d $$

Trois notes de 1 à 4. Le produit sert à ranger les risques. Et c'est tout ce qu'il sert à faire.

{{qualite.criticite._ce_que_la_criticite_n_est_pas}}

{{qualite.criticite._le_seuil_est_arbitraire}}

## S4 · L'étude de cas : une non-conformité de parement

### a. Ce que la non-conformité coûte, et pourquoi la question est mal posée

Un défaut de parement est constaté au décoffrage d'une levée de voile de noyau, en hall voyageurs :
nids de cailloux et fuites de laitance sur {{gare.qualite_hse.non_conformite.surface_m2.valeur::n0}} m².
Le réflexe est de demander un devis de reprise, et d'y ajouter le temps perdu. **Les deux moitiés de
ce réflexe sont fausses, et pas de la même façon.**

**La première moitié est juste mais incomplète.** La reprise n'est pas le seul coût visible : le
contrôle se durcit ensuite sur tout ce qui suit.

| Poste visible | Prix unitaire | Montant | |
|---|---:|---:|---|
| {{qualite.non_conformite.detail_de_la_part_visible.0.poste}} | ⟦V3|coût de reprise d'un parement vu|420 MAD/m²|MAD/m²|250 à 700|2026|piquage, ragréage, reprise de parement et protection des abords : varie fortement selon que le parement reste vu ou sera doublé⟧ | {{qualite.non_conformite.detail_de_la_part_visible.0.montant_MAD::n0}} MAD | {{qualite.non_conformite.detail_de_la_part_visible.0.note}} |
| {{qualite.non_conformite.detail_de_la_part_visible.1.poste}} | ⟦V3|heure de contrôle d'un cadre, charges comprises|140 MAD/h|MAD/h|90 à 240|2026|maîtrise d'œuvre, bureau d'études ou service qualité : recoupé sur les frais d'encadrement du module D1, de l'ordre de 25 000 MAD par mois et par cadre⟧ | {{qualite.non_conformite.detail_de_la_part_visible.1.montant_MAD::n0}} MAD | {{qualite.non_conformite.detail_de_la_part_visible.1.note}} |
| **Part visible, totale** | | **{{qualite.non_conformite.part_visible_sur_un_devis_MAD::n0}} MAD** | bornes **{{qualite.non_conformite.part_visible_bornes_MAD.0::n0}} à {{qualite.non_conformite.part_visible_bornes_MAD.1::n0}} MAD** — et elle **ne dépend pas** de l'ouvrage touché |

:::encart {"genre":"piege","titre":"Une heure de contrôle n'est pas une heure de production"}
{{qualite.non_conformite._pourquoi_l_heure_de_controle_coute_plus}}

C'est une erreur de taux, pas de méthode — et c'est la plus difficile à voir, parce que le résultat
reste du même ordre de grandeur et que la conclusion ne change pas. Elle n'a été trouvée qu'en
lisant la **note** attachée au prix dans les données : « compagnon, charges comprises ». Le prix
était juste ; c'est l'usage qui ne l'était pas.
:::

**La seconde moitié est une faute**, et c'est celle qu'une première version de ce module a commise :
elle imputait à la non-conformité {{qualite.non_conformite.jours_immobilises::n0}} jours de frais de
durée du chantier — l'attente de la décision plus la reprise. Or **les frais de durée du chantier ne
courent que si la fin du chantier bouge.** Les facturer à un ouvrage qui a de la marge, c'est
inventer un coût ; et le module le faisait en publiant deux sections plus loin que cet ouvrage-là ne
décalait rien.

:::encart {"genre":"attente","titre":"Ce que cette erreur enseigne, et pourquoi elle est racontée ici"}
C'est la règle D-040 du cours — *on mesure l'effet sur la date, on ne le déduit pas* — enfreinte dans
le module qui la cite. Elle n'a été trouvée ni par les 56 contrôles de ce module, ni par les seize
de la chaîne : tous étaient verts. Elle a été trouvée en rapprochant **deux nombres publiés par le
même module**, à deux sections d'intervalle.

Et la correction donne un résultat bien plus intéressant que le nombre unique qu'elle remplace.
:::

### b. La même non-conformité, selon l'ouvrage qu'elle touche

{{qualite.impact_planning.lecture}}

| Ouvrage | Marge | Retard du chantier | Frais de durée | **Coût total** | Part visible | Régime |
|---|---:|---:|---:|---:|---:|---|
| {{qualite.non_conformite.par_ouvrage.0.tache}} · {{qualite.non_conformite.par_ouvrage.0.nom}} | {{qualite.non_conformite.par_ouvrage.0.marge_totale_j::n1}} j | {{qualite.non_conformite.par_ouvrage.0.retard_du_chantier_j::n1}} j | {{qualite.non_conformite.par_ouvrage.0.frais_de_duree_MAD::n0}} MAD | **{{qualite.non_conformite.par_ouvrage.0.total_MAD::n0}} MAD** | {{qualite.non_conformite.par_ouvrage.0.part_visible_pct::n1}} % | {{qualite.non_conformite.par_ouvrage.0.regime}} |
| {{qualite.non_conformite.par_ouvrage.1.tache}} · {{qualite.non_conformite.par_ouvrage.1.nom}} | {{qualite.non_conformite.par_ouvrage.1.marge_totale_j::n1}} j | {{qualite.non_conformite.par_ouvrage.1.retard_du_chantier_j::n1}} j | {{qualite.non_conformite.par_ouvrage.1.frais_de_duree_MAD::n0}} MAD | **{{qualite.non_conformite.par_ouvrage.1.total_MAD::n0}} MAD** | {{qualite.non_conformite.par_ouvrage.1.part_visible_pct::n1}} % | {{qualite.non_conformite.par_ouvrage.1.regime}} |
| {{qualite.non_conformite.par_ouvrage.2.tache}} · {{qualite.non_conformite.par_ouvrage.2.nom}} | {{qualite.non_conformite.par_ouvrage.2.marge_totale_j::n1}} j | {{qualite.non_conformite.par_ouvrage.2.retard_du_chantier_j::n1}} j | {{qualite.non_conformite.par_ouvrage.2.frais_de_duree_MAD::n0}} MAD | **{{qualite.non_conformite.par_ouvrage.2.total_MAD::n0}} MAD** | {{qualite.non_conformite.par_ouvrage.2.part_visible_pct::n1}} % | {{qualite.non_conformite.par_ouvrage.2.regime}} |

{{qualite.non_conformite.lecture}}

| Ouvrage | Coût total | Bornes | Retard mesuré | Bornes du retard |
|---|---:|---:|---:|---:|
| {{qualite.non_conformite.par_ouvrage.0.tache}} | {{qualite.non_conformite.par_ouvrage.0.total_MAD::n0}} MAD | {{qualite.non_conformite.par_ouvrage.0.total_bornes_MAD.0::n0}} à {{qualite.non_conformite.par_ouvrage.0.total_bornes_MAD.1::n0}} | {{qualite.non_conformite.par_ouvrage.0.retard_du_chantier_j::n1}} j | {{qualite.non_conformite.par_ouvrage.0.retard_bornes_j.0::n1}} à {{qualite.non_conformite.par_ouvrage.0.retard_bornes_j.1::n1}} j |
| {{qualite.non_conformite.par_ouvrage.1.tache}} | {{qualite.non_conformite.par_ouvrage.1.total_MAD::n0}} MAD | {{qualite.non_conformite.par_ouvrage.1.total_bornes_MAD.0::n0}} à {{qualite.non_conformite.par_ouvrage.1.total_bornes_MAD.1::n0}} | {{qualite.non_conformite.par_ouvrage.1.retard_du_chantier_j::n1}} j | {{qualite.non_conformite.par_ouvrage.1.retard_bornes_j.0::n1}} à {{qualite.non_conformite.par_ouvrage.1.retard_bornes_j.1::n1}} j |
| {{qualite.non_conformite.par_ouvrage.2.tache}} | {{qualite.non_conformite.par_ouvrage.2.total_MAD::n0}} MAD | {{qualite.non_conformite.par_ouvrage.2.total_bornes_MAD.0::n0}} à {{qualite.non_conformite.par_ouvrage.2.total_bornes_MAD.1::n0}} | {{qualite.non_conformite.par_ouvrage.2.retard_du_chantier_j::n1}} j | {{qualite.non_conformite.par_ouvrage.2.retard_bornes_j.0::n1}} à {{qualite.non_conformite.par_ouvrage.2.retard_bornes_j.1::n1}} j |

{{qualite.non_conformite._bornes}}

**Et une anomalie dans ce tableau**, qui est en réalité le plus beau résultat du module : les
bornes du retard de {{qualite.non_conformite.par_ouvrage.0.tache}} sont
**{{qualite.non_conformite.par_ouvrage.0.retard_bornes_j.0::n0}} et
{{qualite.non_conformite.par_ouvrage.0.retard_bornes_j.1::n0}} jours** — les deux mêmes. Faire
varier l'immobilisation du simple au sextuple ne change rien au retard. La section suivante
explique pourquoi, et ce n'est pas une coïncidence.

:::figure {"fn":"barres","args":"qualite.figures.cout_nc","titre":"La même non-conformité, selon l'ouvrage qu'elle touche","num":2,"large":true,"options":{"unite":"MAD — même défaut, même surface, même méthode de reprise"},"voir":["Le défaut est identique dans les trois cas. Ce qui change est l'ouvrage, et le rapport est de {{qualite.non_conformite.ecart_entre_les_regimes::n0}} à 1.","La part visible sur un devis passe de {{qualite.non_conformite.par_ouvrage.0.part_visible_pct::n0}} % à {{qualite.non_conformite.par_ouvrage.2.part_visible_pct::n0}} %. Sur l'ouvrage à marge, un devis de reprise dit presque toute la vérité ; sur l'ouvrage contraint, il n'en dit presque rien.","La barre la plus haute n'est pas celle du défaut le plus grave : c'est celle de l'ouvrage le plus contraint. Rien de cela ne se voit sur le chantier."],"erreur":"Chiffrer une non-conformité une fois pour toutes, et réutiliser le chiffre. Le même défaut vaut ici {{qualite.figures.cout_nc.2.valeur::n0}} ou {{qualite.figures.cout_nc.0.valeur::n0}} MAD selon l'ouvrage — à trois chiffres significatifs, parce que les entrées sont des hypothèses à facteur deux — et aucun des deux n'est « le » coût d'une NC de parement."}
:::

:::encart {"genre":"voir","titre":"Deux mécanismes, et il faut les deux"}
{{qualite.impact_planning.la_regle_en_deux_temps}}

**La règle en une phrase :**

> La **marge** décide si le retard passe. La **consignation** décide de combien il est amplifié.

{{qualite.impact_planning._consequence_de_pilotage}}
:::

### Sous consignation, le retard ne varie pas : il saute

Le réseau a été rejoué pour six immobilisations différentes, de une demi-journée à vingt-cinq
jours. Il ne rend que **{{qualite.quantification_du_retard.nb_paliers_observes}} retards distincts**.

| Immobilisation | {{qualite.quantification_du_retard.sondes.0.immobilisation_j::n1}} j | {{qualite.quantification_du_retard.sondes.1.immobilisation_j::n1}} j | {{qualite.quantification_du_retard.sondes.2.immobilisation_j::n1}} j | {{qualite.quantification_du_retard.sondes.3.immobilisation_j::n1}} j | {{qualite.quantification_du_retard.sondes.4.immobilisation_j::n1}} j | {{qualite.quantification_du_retard.sondes.5.immobilisation_j::n1}} j |
|---|---:|---:|---:|---:|---:|---:|
| **Retard du chantier** | {{qualite.quantification_du_retard.sondes.0.retard_j::n0}} j | {{qualite.quantification_du_retard.sondes.1.retard_j::n0}} j | {{qualite.quantification_du_retard.sondes.2.retard_j::n0}} j | {{qualite.quantification_du_retard.sondes.3.retard_j::n0}} j | {{qualite.quantification_du_retard.sondes.4.retard_j::n0}} j | {{qualite.quantification_du_retard.sondes.5.retard_j::n0}} j |

{{qualite.quantification_du_retard.note}}

{{qualite.quantification_du_retard.consequence_sur_les_bornes}}

:::encart {"genre":"voir","titre":"Le coût marginal d'un jour perdu n'est pas constant — il est nul, puis brutal"}
C'est la conséquence de pilotage, et elle est contre-intuitive pour qui lit un Gantt : sur une tâche
sous consignation, **le premier jour perdu coûte tout et les suivants ne coûtent rien** jusqu'au
palier suivant. Trois règles en découlent, et elles s'appliquent le jour du constat :

1. **Avant la fenêtre, tout se joue sur quelques heures.** Un constat le lundi pour une fenêtre le
   mercredi se traite dans la nuit, parce que la demi-journée de trop coûte
   {{qualite.quantification_du_retard.pas_j}} jours.
2. **Une fois la fenêtre ratée, se presser ne rachète rien.** On a jusqu'au créneau suivant, et la
   bonne décision est alors de faire la reprise *bien*, pas vite — et d'en profiter pour traiter
   tout ce qui devait l'être dans la même zone.
3. **Ce qui se négocie n'est pas la durée de la reprise, c'est la fenêtre.** Et cela se demande des
   mois à l'avance, à l'exploitant, pas à l'équipe.
:::

### Le paramètre qui porte vraiment l'incertitude n'appartient pas au chantier

| Période entre deux fenêtres | Durée de référence du chantier | Retard de la même NC |
|---:|---:|---:|
| {{qualite.sensibilite_a_la_periode.lignes.0.periode_j}} j | {{qualite.sensibilite_a_la_periode.lignes.0.duree_de_reference_j::n0}} j | {{qualite.sensibilite_a_la_periode.lignes.0.retard_j::n0}} j |
| **{{qualite.sensibilite_a_la_periode.lignes.1.periode_j}} j** (hypothèse retenue) | **{{qualite.sensibilite_a_la_periode.lignes.1.duree_de_reference_j::n0}} j** | **{{qualite.sensibilite_a_la_periode.lignes.1.retard_j::n0}} j** |
| {{qualite.sensibilite_a_la_periode.lignes.2.periode_j}} j | {{qualite.sensibilite_a_la_periode.lignes.2.duree_de_reference_j::n0}} j | {{qualite.sensibilite_a_la_periode.lignes.2.retard_j::n0}} j |

{{qualite.sensibilite_a_la_periode.note}}

**Ce que cela dit du travail de borner.** On borne spontanément ce qu'on connaît : la surface du
défaut, le prix de la reprise, la durée de l'intervention. Ici, balayer ces trois-là ne change
**rien** au retard de l'ouvrage contraint, et balayer un paramètre dont on ne parle jamais — la
période des fenêtres — le double. Borner le mauvais paramètre est une façon très efficace de se
rassurer.

{{qualite.non_conformite.decomposition_de_l_immobilisation.note}}

**Et ce que ces chiffres ne contiennent pas.** {{qualite.non_conformite.ce_qui_n_est_PAS_chiffre_ici}}

{{qualite.non_conformite._le_piege}}

### c. Le plan de contrôle du cas phare — et les deux autres que ce cours publie

**Avant le tableau, le périmètre**, parce que ce cours publie trois listes de contrôles et qu'un
chantier n'a qu'un plan de contrôle :

{{qualite.plan_de_controle.perimetre}}

:::encart {"genre":"piege","titre":"« Qui contrôle » et « qui vise » sont deux colonnes, pas une"}
{{qualite.plan_de_controle.qui_et_visa}}
:::

| Contrôle | Exécuté par | Visé par | Quand | Critère | Résultat | Tâche · marge | Point d'arrêt | Si non conforme |
|---|---|---|---|---|---:|---:|:-:|---|
| **{{qualite.plan_de_controle.lignes.0.controle}}** | {{qualite.plan_de_controle.lignes.0.qui}} | {{qualite.plan_de_controle.lignes.0.visa}} | {{qualite.plan_de_controle.lignes.0.quand}} | {{qualite.plan_de_controle.lignes.0.critere}} | {{qualite.plan_de_controle.lignes.0.delai_du_resultat_j}} j | {{qualite.plan_de_controle.lignes.0.tache_et_marge}} | {{qualite.plan_de_controle.lignes.0.duree_h::n2}} h | {{qualite.plan_de_controle.lignes.0.si_non_conforme}} |
| **{{qualite.plan_de_controle.lignes.1.controle}}** | {{qualite.plan_de_controle.lignes.1.qui}} | {{qualite.plan_de_controle.lignes.1.visa}} | {{qualite.plan_de_controle.lignes.1.quand}} | {{qualite.plan_de_controle.lignes.1.critere}} | {{qualite.plan_de_controle.lignes.1.delai_du_resultat_j}} j | {{qualite.plan_de_controle.lignes.1.tache_et_marge}} | {{qualite.plan_de_controle.lignes.1.duree_h::n2}} h | {{qualite.plan_de_controle.lignes.1.si_non_conforme}} |
| **{{qualite.plan_de_controle.lignes.2.controle}}** | {{qualite.plan_de_controle.lignes.2.qui}} | {{qualite.plan_de_controle.lignes.2.visa}} | {{qualite.plan_de_controle.lignes.2.quand}} | {{qualite.plan_de_controle.lignes.2.critere}} | {{qualite.plan_de_controle.lignes.2.delai_du_resultat_j}} j | {{qualite.plan_de_controle.lignes.2.tache_et_marge}} | {{qualite.plan_de_controle.lignes.2.duree_h::n2}} h | {{qualite.plan_de_controle.lignes.2.si_non_conforme}} |
| **{{qualite.plan_de_controle.lignes.3.controle}}** | {{qualite.plan_de_controle.lignes.3.qui}} | {{qualite.plan_de_controle.lignes.3.visa}} | {{qualite.plan_de_controle.lignes.3.quand}} | {{qualite.plan_de_controle.lignes.3.critere}} | **{{qualite.plan_de_controle.lignes.3.delai_du_resultat_j}} j** | {{qualite.plan_de_controle.lignes.3.tache_et_marge}} | {{qualite.plan_de_controle.lignes.3.duree_h::n2}} h | {{qualite.plan_de_controle.lignes.3.si_non_conforme}} |
| **{{qualite.plan_de_controle.lignes.4.controle}}** | {{qualite.plan_de_controle.lignes.4.qui}} | {{qualite.plan_de_controle.lignes.4.visa}} | {{qualite.plan_de_controle.lignes.4.quand}} | {{qualite.plan_de_controle.lignes.4.critere}} | {{qualite.plan_de_controle.lignes.4.delai_du_resultat_j}} j | {{qualite.plan_de_controle.lignes.4.tache_et_marge}} | {{qualite.plan_de_controle.lignes.4.duree_h::n2}} h | {{qualite.plan_de_controle.lignes.4.si_non_conforme}} |
| **{{qualite.plan_de_controle.lignes.5.controle}}** | {{qualite.plan_de_controle.lignes.5.qui}} | {{qualite.plan_de_controle.lignes.5.visa}} | {{qualite.plan_de_controle.lignes.5.quand}} | {{qualite.plan_de_controle.lignes.5.critere}} | {{qualite.plan_de_controle.lignes.5.delai_du_resultat_j}} j | {{qualite.plan_de_controle.lignes.5.tache_et_marge}} | {{qualite.plan_de_controle.lignes.5.duree_h::n2}} h | {{qualite.plan_de_controle.lignes.5.si_non_conforme}} |

**Où chaque ligne se détaille**, parce que la maille de ce plan n'est pas celle du chantier :
« {{qualite.plan_de_controle.lignes.1.controle}} » →
{{qualite.plan_de_controle.lignes.1.detail}} · « {{qualite.plan_de_controle.lignes.2.controle}} » →
{{qualite.plan_de_controle.lignes.2.detail}} · « {{qualite.plan_de_controle.lignes.4.controle}} » →
{{qualite.plan_de_controle.lignes.4.detail}} · « {{qualite.plan_de_controle.lignes.5.controle}} » →
{{qualite.plan_de_controle.lignes.5.detail}}. Les deux autres lignes n'ont pas de détail ailleurs
dans ce cours.

La colonne « point d'arrêt » porte la durée à prévoir au planning :
{{qualite.plan_de_controle.nb_points_d_arret}} des {{qualite.plan_de_controle.nb_controles}}
contrôles en sont, pour {{qualite.plan_de_controle.heures_de_points_d_arret::n1}} heures, et
l'ensemble des contrôles de ce plan pèse
{{qualite.plan_de_controle.heures_de_controle_total::n2}} heures. C'est peu, et c'est le piège : un
point d'arrêt ne coûte pas sa durée, il coûte **l'attente de celui qui doit venir le viser**.

Les critères renvoient au marché ou au plan visé — ils ne les remplacent pas. **Aucun seuil chiffré
n'est donné ici**, et c'est volontaire : un plan de contrôle qui porterait des valeurs serait faux
dès le premier chantier dont le CPS diffère. La règle exacte, parce qu'elle est plus fine que
« jamais de chiffre », est au § S6, exercice 3.

{{qualite.plan_de_controle._le_cout_du_point_d_arret}}

:::encart {"genre":"voir","titre":"Sur ce chantier, aucun contrôle de gros œuvre n'arrête une tâche critique"}
La colonne « marge » le dit : toutes les tâches arrêtées par ces contrôles disposent de
{{qualite.plan_de_controle.lignes.1.marge_de_la_tache_j::n1}} jours, et
{{qualite.plan_de_controle.nb_sur_le_chemin_critique}} d'entre elles n'en a aucune. Ce n'est pas
une bonne nouvelle, c'est un **déplacement** : depuis que le levage sous consignation domine le
chemin critique, le gros œuvre a de la marge, et les contrôles qui coûtent du délai sont ceux du
levage — qui ne figurent pas dans ce plan, parce qu'ils relèvent du module B7c et de la réception
des assemblages. Un plan de contrôle complet se relit à chaque fois que le chemin critique bouge.

**Conséquence de pilotage** : l'effort de contrôle se met là où le planning est contraint, et il
s'y met *avant*. Un plan de contrôle rédigé une fois pour toutes ne peut pas le savoir — il faut le
relire à chaque fois que le chemin critique bouge, ce qui est arrivé deux fois dans ce cours.
:::

### d. L'analyse de risques, et ce qu'on en fait

| Rang | Risque | f | g | d | C | Parade essentielle |
|---:|---|:-:|:-:|:-:|---:|---|
| {{qualite.criticite.lignes.0.rang}} | **{{qualite.criticite.lignes.0.risque}}** | {{qualite.criticite.lignes.0.f}} | {{qualite.criticite.lignes.0.g}} | {{qualite.criticite.lignes.0.d}} | **{{qualite.criticite.lignes.0.criticite}}** | {{qualite.criticite.lignes.0.parade}} |
| {{qualite.criticite.lignes.1.rang}} | **{{qualite.criticite.lignes.1.risque}}** | {{qualite.criticite.lignes.1.f}} | {{qualite.criticite.lignes.1.g}} | {{qualite.criticite.lignes.1.d}} | **{{qualite.criticite.lignes.1.criticite}}** | {{qualite.criticite.lignes.1.parade}} |
| {{qualite.criticite.lignes.2.rang}} | {{qualite.criticite.lignes.2.risque}} | {{qualite.criticite.lignes.2.f}} | {{qualite.criticite.lignes.2.g}} | {{qualite.criticite.lignes.2.d}} | {{qualite.criticite.lignes.2.criticite}} | {{qualite.criticite.lignes.2.parade}} |
| {{qualite.criticite.lignes.3.rang}} | {{qualite.criticite.lignes.3.risque}} | {{qualite.criticite.lignes.3.f}} | {{qualite.criticite.lignes.3.g}} | {{qualite.criticite.lignes.3.d}} | {{qualite.criticite.lignes.3.criticite}} | {{qualite.criticite.lignes.3.parade}} |
| {{qualite.criticite.lignes.4.rang}} | {{qualite.criticite.lignes.4.risque}} | {{qualite.criticite.lignes.4.f}} | {{qualite.criticite.lignes.4.g}} | {{qualite.criticite.lignes.4.d}} | {{qualite.criticite.lignes.4.criticite}} | {{qualite.criticite.lignes.4.parade}} |
| {{qualite.criticite.lignes.5.rang}} | {{qualite.criticite.lignes.5.risque}} | {{qualite.criticite.lignes.5.f}} | {{qualite.criticite.lignes.5.g}} | {{qualite.criticite.lignes.5.d}} | {{qualite.criticite.lignes.5.criticite}} | {{qualite.criticite.lignes.5.parade}} |
| {{qualite.criticite.lignes.6.rang}} | {{qualite.criticite.lignes.6.risque}} | {{qualite.criticite.lignes.6.f}} | {{qualite.criticite.lignes.6.g}} | {{qualite.criticite.lignes.6.d}} | {{qualite.criticite.lignes.6.criticite}} | {{qualite.criticite.lignes.6.parade}} |
| {{qualite.criticite.lignes.7.rang}} | {{qualite.criticite.lignes.7.risque}} | {{qualite.criticite.lignes.7.f}} | {{qualite.criticite.lignes.7.g}} | {{qualite.criticite.lignes.7.d}} | {{qualite.criticite.lignes.7.criticite}} | {{qualite.criticite.lignes.7.parade}} |

:::figure {"fn":"barres","args":"qualite.figures.criticite","titre":"Les risques classés par criticité — un rang, pas une mesure","num":3,"large":true,"options":{"unite":"criticité f × g × d, échelles ordinales de 1 à 4"},"voir":["Les longueurs de barre se comparent, mais elles ne se soustraient pas : une barre deux fois plus longue n'est pas un risque deux fois plus grand. L'axe porte des rangs multipliés.","{{qualite.criticite.nb_ex_aequo_en_tete}} risques sont EX ÆQUO en tête, tous à {{qualite.criticite.lignes.0.criticite}}. Avec des notes de 1 à 4, le produit ne prend que peu de valeurs : le classement ne départage pas, et c'est à l'équipe de le faire — pas au tableau.","Parmi eux, deux ont la fréquence la plus haute et la gravité la plus basse : {{qualite.criticite.risques_a_faible_gravite_mais_frequents.0}} et {{qualite.criticite.risques_a_faible_gravite_mais_frequents.1}}. Ils ne font pas d'accident, ils font des carrières écourtées, et aucun tableau de bord hebdomadaire ne les voit.","Un risque de gravité 4 se traite même s'il se classe mal : on n'arbitre pas une vie contre un rang."],"erreur":"Tirer un trait de seuil sur ce graphique et traiter ce qui dépasse. Le seuil dépend entièrement du choix des échelles ; deux équipes avec deux échelles différentes traiteront deux listes différentes, et aucune n'aura tort."}
:::

{{qualite.criticite._ce_que_les_ex_aequo_disent}}

{{qualite.criticite.pourquoi_lire_aussi_la_gravite_seule}}

:::encart {"genre":"piege","titre":"Le risque que personne ne voit venir se classe sixième"}
Regardez la ligne « {{qualite.criticite.lignes.5.risque}} » :
f = {{qualite.criticite.lignes.5.f}}, g = {{qualite.criticite.lignes.5.g}},
d = {{qualite.criticite.lignes.5.d}}. C'est le **seul** risque de ce tableau dont la détection est
notée au maximum, c'est-à-dire qu'on ne le voit pas venir, et sa gravité est maximale elle aussi.
Il se classe **{{qualite.criticite.lignes.5.rang}}ᵉ**, derrière deux troubles de santé au travail.

Ce n'est pas un défaut du tableau : c'est sa définition. Le produit f × g × d récompense la
fréquence, et un effondrement d'étaiement est rare. Ce qu'il faut en faire est simple et ne se
discute pas : **les risques de gravité maximale se traitent quel que soit leur rang**, et la note
d'étaiement se vise avant le montage, pas après. Le tableau sert à répartir l'attention sur le
reste.
:::

### e. Les déchets : celui qui pèse le moins commande le plus

{{qualite.dechets.lecture}}

Les cinq ratios sont des hypothèses déclarées, et **les cinq portent leur balise** : en baliser deux
et laisser les trois autres en nombres nus donnerait à croire que ces trois-là sont mesurées.

| Flux | kg/m² | Tonnes | Valorisation |
|---|---:|---:|---:|
| {{qualite.dechets.lignes.0.flux}} | ⟦V3|déchets de béton et gravats d'un chantier de gros œuvre|38|kg/m²|20 à 70|2026|chutes de coulage, démolition d'ouvrages provisoires, reprises et parements piqués, rapportées à l'emprise construite⟧ | {{qualite.dechets.lignes.0.tonnes::n1}} t | {{qualite.dechets.lignes.0.valorisation_pct}} % |
| {{qualite.dechets.lignes.1.flux}} | ⟦V3|déchets d'acier et de métaux d'un chantier de gros œuvre|4,5|kg/m²|2,0 à 9,0|2026|chutes de façonnage et emballages métalliques, rapportées à l'emprise construite⟧ | {{qualite.dechets.lignes.1.tonnes::n1}} t | {{qualite.dechets.lignes.1.valorisation_pct}} % |
| {{qualite.dechets.lignes.2.flux}} | ⟦V3|déchets de bois de coffrage|6,0|kg/m²|3,0 à 12,0|2026|bois de calage, chutes de coffrage traditionnel et contreplaqué en fin de rotation⟧ | {{qualite.dechets.lignes.2.tonnes::n1}} t | {{qualite.dechets.lignes.2.valorisation_pct}} % |
| {{qualite.dechets.lignes.3.flux}} | ⟦V3|déchets d'emballages et divers d'un chantier de gros œuvre|3,5|kg/m²|1,5 à 8,0|2026|films, palettes, cartons et divers non triés à la source⟧ | {{qualite.dechets.lignes.3.tonnes::n1}} t | {{qualite.dechets.lignes.3.valorisation_pct}} % |
| {{qualite.dechets.lignes.4.flux}} | ⟦V3|déchets dangereux d'un chantier de gros œuvre|0,4|kg/m²|0,2 à 0,8|2026|huiles de décoffrage, fonds d'adjuvants, aérosols, chiffons souillés, cartouches de mastic⟧ | {{qualite.dechets.lignes.4.tonnes::n1}} t | {{qualite.dechets.lignes.4.valorisation_pct}} % |
| **Total** | | **{{qualite.dechets.total_tonnes::n1}} t** | **{{qualite.dechets.taux_de_valorisation_pct::n1}} %** |

{{qualite.dechets._bornes}}

{{qualite.dechets._dangereux}}

:::figure {"fn":"barres","args":"qualite.figures.dechets","titre":"Les flux de déchets du gros œuvre, et celui qui commande le tri","num":4,"large":true,"options":{"unite":"tonnes sur la durée du chantier"},"voir":["Les gravats écrasent tout le reste : c'est le flux qu'on dimensionne, en nombre de bennes et en rotations.","La dernière barre tient en un trait — {{qualite.dechets.part_dangereuse_pct::n2}} % du poids total. C'est pourtant elle qui décide de l'organisation de l'aire de tri, du stockage couvert et du document de suivi.","Les taux de valorisation ne se lisent pas sur ce graphique : un flux lourd mal trié pèse plus qu'un flux léger bien trié, et c'est le produit des deux qui fait le taux global de {{qualite.dechets.taux_de_valorisation_pct::n1}} %."],"erreur":"Dimensionner l'aire de tri sur les tonnages. Le flux dangereux ne demande pas du volume, il demande un emplacement séparé, couvert, sur bac de rétention, et une traçabilité — soit l'exact inverse de ce que son poids suggère."}
:::

## S4g · Sécurité : les dispositions qui ne se négocient pas

Les parades du tableau ci-dessus sont **essentielles et non exhaustives**. Elles ne remplacent ni le
plan de prévention du chantier, ni le PPSPS, ni les obligations réglementaires du marché, et aucune
distance ni aucun seuil n'y est chiffré. Trois remarques, qui valent plus que la liste.

**La première.** Les parades les plus efficaces sont celles qui s'installent **avant** l'opération et
se déposent **après** : protections périphériques posées avant le coffrage, blindage avant la
descente en fouille, zone d'exclusion avant l'élingage. Or la pression de cadence pousse exactement
à l'inverse — on pose la protection quand on en a besoin, c'est-à-dire trop tard. **C'est le cycle de
rotation qui décide de la sécurité du travail en hauteur**, pas l'affiche à la base-vie.

**La deuxième.** Une parade qui dépend de la vigilance de celui qui prend le risque n'est pas une
parade : c'est un espoir. Les dispositions qui tiennent sont celles qui sont **matérielles** (un
garde-corps), **organisationnelles** (un agent qui a le pouvoir d'arrêter) ou **géométriques** (une
zone physiquement inaccessible).

**La troisième, et c'est celle de ce module.** La prévention se met là où sont les **heures**, et
elles ne sont pas là où l'on croit. Le second œuvre concentre la main-d'œuvre et paraît inoffensif à
côté d'un levage ; il porte pourtant la plus grosse part de l'exposition de ce chantier. Le gros
œuvre impressionne, le second œuvre expose.

**Une précaution de vocabulaire, et elle n'est pas formelle.** Les documents cités dans ce module
portent des noms qui **dépendent du droit applicable**. Ce cours décrit la **fonction** que chacun
remplit — qui écrit, pour qui, et ce que ça engage — et renvoie au marché pour le nom, le contenu et
le caractère obligatoire. Nommer un instrument d'un droit étranger dans un cours marocain serait une
faute de même nature que citer un article de norme sans l'avoir lu.

**Le lien avec le reste du module.** Le § S4b montre qu'une non-conformité se hiérarchise sur sa
marge. La sécurité, elle, ne se hiérarchise pas ainsi : **un risque de gravité maximale se traite
quel que soit son rang et quelle que soit la marge de la tâche.** C'est la seule différence de fond
entre piloter la qualité et piloter la sécurité, et elle doit être dite, parce que les deux se
tiennent dans le même tableau de bord et obéissent à deux logiques opposées.

## S4h · La double lecture : entreprise et maîtrise d'œuvre

Les mêmes faits, deux métiers, et deux documents qui ne disent pas la même chose.

| | **Côté entreprise** | **Côté maîtrise d'œuvre** |
|---|---|---|
| **Le plan de contrôle** | il organise la production : qui vérifie quoi avant d'appeler. Appeler sur un ouvrage non terminé coûte une demi-journée de cycle et la confiance pour les zones suivantes | il organise le **visa** : sur quoi il s'engage, et ce qu'il refuse de viser. Un contrôle que la MOE n'a pas vu n'existe pas dans son dossier, quelle qu'en soit la qualité |
| **Une non-conformité** | un coût et un délai à traiter au plus vite, et une négociation sur l'étendue de la reprise | un **constat écrit, daté, sur place**, qui engage sa responsabilité. Il ne se lève pas sur une photo ni par téléphone |
| **Le point d'arrêt** | une tâche du planning, avec sa durée, à préparer pour qu'elle ne saute pas | un **pouvoir**, et le seul moment où il s'exerce sans rapport de force : après coulage, il n'y a plus de levier |
| **L'analyse de risques** | elle doit être applicable par les compagnons, sinon elle reste au bureau | elle doit être **vérifiable sur le terrain** : une parade qu'on ne peut pas constater ne se vise pas |
| **Les indicateurs** | ils servent à piloter, et ils remontent au siège | ils servent à **alerter le maître d'ouvrage**, et ils engagent la MOE si elle les relaie sans les avoir regardés |

**Ce qui se joue dans l'écart.** L'entreprise optimise un cycle, la maîtrise d'œuvre protège un
ouvrage et une signature. Les deux lectures sont légitimes, et le chef de projet suivi passe d'une
chaise à l'autre selon les projets — c'est pourquoi il doit savoir ce que l'autre voit. Le danger
n'est pas le désaccord, qui se traite : c'est le **faux accord**, quand les deux signent la même
ligne en lui donnant deux sens.

## S5 · Erreurs fréquentes, et ce qu'elles coûtent

| Erreur | Comment elle se voit | Ce qu'elle coûte |
|---|---|---|
| Rapporter un indicateur de sécurité à un **effectif** | deux chantiers incomparables ont le même chiffre | on compare des chantiers qui n'ont rien de comparable |
| Concentrer la prévention sur les tâches **spectaculaires** | le levage est surveillé, le second œuvre non | la phase qui porte le plus d'heures est la moins suivie |
| Oublier la surexposition de nuit | les heures de nuit comptent comme les autres | {{qualite.exposition.part_de_nuit_pct::n1}} % des heures portent {{qualite.exposition.part_de_nuit_dans_le_risque_pct::n1}} % du risque |
| Chiffrer une NC **une fois pour toutes** | un chiffre circule et sert partout | le même défaut vaut {{qualite.non_conformite.par_ouvrage.2.total_MAD::n0}} ou {{qualite.non_conformite.par_ouvrage.0.total_MAD::n0}} MAD selon l'ouvrage |
| Imputer les frais de durée du chantier à un ouvrage **à marge** | le coût paraît complet | un coût inventé : ils ne courent que si la date bouge (D-040) |
| Négocier le prix de la reprise pendant que la décision attend | on gagne 5 % sur la plus petite ligne | l'attente coûte {{qualite.non_conformite.frais_de_duree_MAD_par_jour_ouvre::n0}} MAD par jour |
| Hiérarchiser les NC sur leur **gravité technique** | la plus visible passe en premier | celle qui est sur une tâche à marge nulle attend, et coûte {{qualite.impact_planning.lignes.0.retard_du_chantier_j::n0}} jours |
| Payer une heure de **contrôle** au taux d'une heure de **production** | la ligne paraît négligeable | elle est sous-estimée d'un facteur trois ; ici la conclusion survit, ailleurs non |
| Comparer deux **taux de fréquence** sans comparer leurs périmètres | le meilleur des deux a l'air meilleur | il a seulement un dénominateur plus petit : aucun accident évité |
| Croire l'assiette des heures **complète** | le tableau de bord est vert | l'atelier de charpente n'y est pas, et c'est là que se soudent {{planification.quantites.charpente_t::n0}} tonnes |
| Borner ce qu'on connaît plutôt que ce qui porte le résultat | l'étude de sensibilité rassure | balayer la surface et le prix ne change rien ; la période des fenêtres double le retard |
| Se presser **après** avoir raté une fenêtre de consignation | l'équipe est mobilisée, tout le monde court | le palier est déjà payé : la vitesse ne rachète rien avant le palier suivant |
| Oublier le **délai du résultat** dans le plan de contrôle | on attend un essai à {{qualite.plan_de_controle.delai_le_plus_long_j}} jours pour avancer | soit on bloque, soit on ignore le résultat — les deux sont faux |
| Lire la criticité comme une **grandeur** | « la criticité a baissé de 30 % » | une phrase sans contenu : on a multiplié des rangs |
| Tirer un **seuil** sur la criticité | la liste à traiter paraît objective | elle dépend entièrement du choix des échelles |
| Mélanger un déchet dangereux à une benne de gravats | rien, sur le moment | la benne entière est déclassée, et la filière avec |
| Écrire un critère de contrôle **chiffré** dans un plan générique | le plan paraît précis | il est faux dès le premier chantier dont le CPS diffère |

## S6 · Exercices

:::exercice {"titre":"1 · Deux chantiers, deux taux de fréquence","niveau":"application"}
Le chantier A déclare 2 accidents avec arrêt sur l'année, le chantier B en déclare 5. Le directeur
régional félicite A. A emploie 12 compagnons, B en emploie 60. Qu'en dites-vous ?

**Corrigé.** Rien, tant qu'on n'a pas les **heures**.

À ⟦V3|heures travaillées par compagnon et par an|1 800 h|h/an|1 600 à 1 950|2026|intempéries, congés et absences déduits : recoupé sur le calendrier de ce cours, qui donne environ 2 080 heures brutes avant retenues⟧ par compagnon et par an :

| | Accidents | Effectif | Heures | **Taux de fréquence** | Bornes du taux |
|---|---:|---:|---:|---:|---:|
| Chantier A | {{qualite.comparaison_de_deux_chantiers.chantiers.0.accidents}} | {{qualite.comparaison_de_deux_chantiers.chantiers.0.effectif}} | {{qualite.comparaison_de_deux_chantiers.chantiers.0.heures::n0}} h | **{{qualite.comparaison_de_deux_chantiers.chantiers.0.tf::n1}}** | {{qualite.comparaison_de_deux_chantiers.chantiers.0.tf_bornes.0::n1}} à {{qualite.comparaison_de_deux_chantiers.chantiers.0.tf_bornes.1::n1}} |
| Chantier B | {{qualite.comparaison_de_deux_chantiers.chantiers.1.accidents}} | {{qualite.comparaison_de_deux_chantiers.chantiers.1.effectif}} | {{qualite.comparaison_de_deux_chantiers.chantiers.1.heures::n0}} h | **{{qualite.comparaison_de_deux_chantiers.chantiers.1.tf::n1}}** | {{qualite.comparaison_de_deux_chantiers.chantiers.1.tf_bornes.0::n1}} à {{qualite.comparaison_de_deux_chantiers.chantiers.1.tf_bornes.1::n1}} |

**A est {{qualite.comparaison_de_deux_chantiers.rapport_des_taux::n0}} fois plus accidentogène que
B**, et c'est lui qu'on félicite.

{{qualite.comparaison_de_deux_chantiers._le_rapport_ne_depend_pas_de_l_hypothese}}

*Et une seconde réserve, qui vaut la première : avec 2 et 5 accidents, les deux taux sont des
estimations très incertaines. Un accident de plus ou de moins déplace le taux de moitié. Un TF sur
un petit chantier et une seule année ne se compare pas — il se cumule sur plusieurs années ou sur
plusieurs chantiers avant de vouloir dire quelque chose. C'est la même limite que le CPI du module
D4 en début de chantier : un indicateur a besoin d'une assiette avant d'avoir un sens.*
:::

:::exercice {"titre":"2 · Deux non-conformités le même matin","niveau":"probleme"}
Lundi, deux constats. Le premier : un défaut de parement sur un voile de hall, très visible, le
maître d'ouvrage l'a vu. Le second : un **défaut de soudure détecté au ressuage** sur une pièce de
charpente à lever sous consignation la semaine suivante, que personne n'a remarqué. Vous avez une
équipe disponible. Par quoi commencez-vous ?

**Corrigé. Par le second, et ce n'est pas discutable.**

Le défaut de parement touche un ouvrage qui a de la marge — **{{qualite.impact_planning.lignes.2.marge_totale_j::n0}} jours** : sa reprise coûte de l'argent et
**{{qualite.impact_planning.lignes.2.retard_du_chantier_j::n0}} jour de chantier**. Le défaut de
soudure touche une tâche à marge nulle, soumise à consignation : s'il fait rater la fenêtre, il
coûte **{{qualite.impact_planning.lignes.0.retard_du_chantier_j::n0}} jours de chantier** pour
{{qualite.impact_planning.immobilisation_j::n0}} jours d'immobilisation, soit
×{{qualite.impact_planning.lignes.0.amplification::n1}}.

{{qualite.impact_planning._le_mecanisme_de_l_amplification}}

**Le rapport est de 1 à {{qualite.impact_planning.lignes.0.retard_du_chantier_j::n0}}**, et il ne se
lit ni sur la gravité technique, ni sur la visibilité, ni sur la surface concernée. Il se lit sur le
planning.

*Et une précision de vocabulaire qui n'est pas un détail : une pièce de charpente métallique n'a
pas d'enrobage — l'enrobage est la distance entre le béton et l'armature. Sur un profilé, on parle
de défaut de **soudure** (ressuage, magnétoscopie, ultrasons selon le cas), de **galvanisation**,
de **revêtement** ou d'**épaisseur de protection au feu**. Le délai du résultat n'est pas le même
non plus, et c'est lui qui décide : un ressuage se lit tout de suite, un contrôle par ultrasons
demande un opérateur qualifié qu'il faut faire venir.*

**Ce qu'il faut dire au maître d'ouvrage**, et c'est la deuxième moitié de l'exercice : « le défaut
de parement est constaté, l'ordre de reprise est émis, l'intervention est programmée tel jour. » On
ne lui explique pas qu'on a priorisé autre chose — on lui montre que son sujet est traité, avec une
date. Un maître d'ouvrage qui a vu un défaut veut savoir qu'il est pris en charge ; il ne demande
pas qu'on arrête le reste.

*Le piège de l'exercice est la pression sociale : le défaut visible crée une demande immédiate, le
défaut invisible n'en crée aucune. C'est exactement l'inverse de leur importance.*
:::

:::exercice {"titre":"3 · Revue critique — un plan de contrôle à corriger","niveau":"revue_critique"}
Voici trois lignes d'un plan de contrôle rendu par une entreprise. Trouvez ce qui ne va pas dans
chacune.

> **1.** *Béton — résistance. Contrôle : essais. Fréquence : selon la norme. Responsable : le
> chantier.*
> **2.** *Enrobage des armatures. Critère : enrobage de 3 cm minimum. Responsable : chef de chantier.
> Si non conforme : reprise.*
> **3.** *Parement. Critère : aspect soigné. Responsable : conducteur de travaux. Si non conforme :
> à voir avec la maîtrise d'œuvre.*

**Corrigé.**

**Ligne 1 — trois manques.** « Selon la norme » n'est pas une fréquence : si personne ne l'a ouverte,
personne ne la suivra, et la ligne ne se contrôle pas. « Le chantier » n'est pas un responsable
nommé. Et surtout : **le délai du résultat manque**, alors qu'il est de
{{qualite.plan_de_controle.delai_le_plus_long_j}} jours — c'est l'information qui change tout, parce
qu'elle dit que ce contrôle ne protège pas l'ouvrage qu'il mesure.

**Ligne 2 — le piège du cours, et il faut être précis sur la règle.** Le critère est **chiffré et
orphelin** : « 3 cm minimum », sans dire d'où vient le 3. C'est cela qui est fautif, et non le
chiffre lui-même. La règle exacte tient en une phrase :

> Un critère peut porter une valeur **à condition de nommer le document dont elle vient**, et de
> marquer ⏸ ce qui est normatif tant que le document n'est pas au dossier. Ce qui est interdit,
> c'est la valeur orpheline dans un plan générique.

Le module B3e de ce cours en donne la bonne forme : il publie « enrobage — référence : la cote du
plan (3 cm ici) », et il marque le critère réglementaire ⏸. Le chiffre est là, il sert au
compagnon qui mesure, et la ligne dit à quel document il faut revenir si le marché diffère. Le
contre-exemple, c'est la ligne 2 de cet exercice : le même chiffre, sans source, dans un plan que
l'on recopiera sur le chantier suivant.

Second défaut de la ligne : le responsable est **celui qui exécute**, et rien n'est dit du visa. Un
contrôle fait par celui qui a fait le travail est un **autocontrôle** — nécessaire, contractuel,
et ce n'est pas un visa. Les deux colonnes du § S4c existent pour cela.

**Ligne 3 — la plus dangereuse, parce qu'elle a l'air complète.** « Aspect soigné » n'est pas un
critère : il n'est pas mesurable, et il sera contesté le jour où il faudra trancher. Un parement se
contrôle contre un **échantillon de référence accepté avant le début des travaux** — c'est le seul
critère d'aspect qui tienne. Et « à voir avec la maîtrise d'œuvre » reporte la décision au pire
moment : la cinquième colonne existe précisément pour décider **à froid** ce qu'on fera d'une
non-conformité, pas devant l'ouvrage.

*Ce que les trois lignes ont en commun : elles sont rédigées pour être rendues, pas pour être
utilisées. C'est le défaut le plus répandu des plans de contrôle, et il se repère à un signe —
aucune des trois ne permet de dire, en la lisant, ce qui se passera exactement si le résultat est
mauvais.*
:::

## S7 · Check-list, glossaire et quiz

**Check-list : une ligne de plan de contrôle**

1. **Qui** contrôle — et est-il indépendant de celui qui exécute ?
2. **Quand** — avant, pendant ou après l'opération ?
3. **Sur quel critère** — mesurable, écrit avant, et **renvoyant** au marché plutôt que le recopiant ?
4. **En combien de temps** le résultat arrive — et protège-t-il encore l'ouvrage qu'il mesure ?
5. **Que se passe-t-il** si c'est non conforme — décidé à froid ?
6. Ce contrôle est-il un **point d'arrêt**, et a-t-il sa durée au planning ?
7. Le constat sera-t-il **traçable** : écrit, daté, sur place ?

**Glossaire**

| Terme | Ce que c'est |
|---|---|
| **TF** (taux de fréquence) | accidents avec arrêt par million d'heures travaillées |
| **TG** (taux de gravité) | journées perdues par millier d'heures travaillées |
| **Point d'arrêt** | étape qu'on ne dépasse pas sans visa écrit. Il a une durée, et elle est au planning |
| **Non-conformité** | écart constaté entre l'ouvrage et ce qui était prescrit. Un constat, pas un jugement |
| **Criticité** | $f \times g \times d$ sur des échelles ordinales : un rang, jamais une grandeur |
| **Échantillon de référence** | ouvrage témoin accepté avant travaux, qui sert de critère d'aspect |
| **Document de suivi d'un déchet dangereux** | pièce qui accompagne le déchet de sa production à son traitement et qui prouve la filière. Nom et forme **selon le droit applicable** : ⏸ |
| **Plan de sécurité d'entreprise** | document par lequel chaque entreprise décrit ses propres dispositions sur ce chantier. Son nom, son contenu et son caractère obligatoire **dépendent du droit applicable** : ⏸ à lire dans le CPS et la réglementation marocaine |

**Quiz**

**1. Un chantier a 3 accidents, un autre 6. Lequel est le plus sûr ?**
**On ne peut pas le dire** sans les heures travaillées. C'est le dénominateur qui fait l'indicateur,
exactement comme pour un avancement (module D4).

**2. Les heures de nuit représentent {{qualite.exposition.part_de_nuit_pct::n1}} % des heures. Quelle part du risque ?**
**{{qualite.exposition.part_de_nuit_dans_le_risque_pct::n1}} %**, avec un coefficient de
surexposition de {{qualite.exposition.coefficient_de_surexposition_de_nuit}}. Une heure de nuit n'est
pas une heure.

**3. Une reprise de parement coûte {{qualite.non_conformite.detail_de_la_part_visible.0.montant_MAD::n0}} MAD. Combien coûte la non-conformité ?**
**La question est mal posée** : ça dépend de l'ouvrage. La part visible —
{{qualite.non_conformite.part_visible_sur_un_devis_MAD::n0}} MAD — ne dépend de rien. Le reste
dépend entièrement du retard **mesuré** : de {{qualite.non_conformite.par_ouvrage.2.total_MAD::n0}}
à {{qualite.non_conformite.par_ouvrage.0.total_MAD::n0}} MAD, un facteur
{{qualite.non_conformite.ecart_entre_les_regimes::n0}}. Et sur un ouvrage à marge, **aucun** frais de
durée n'est dû : les facturer serait inventer un coût.

**4. Deux NC de même gravité. Laquelle traiter en premier ?**
**Celle qui touche l'ouvrage à marge nulle.** La gravité technique ne hiérarchise pas : la marge le
fait. Et sous consignation, le retard est **amplifié** — on ne rate pas sa reprise, on rate sa
fenêtre.

**5. Un essai rend son résultat à {{qualite.plan_de_controle.delai_le_plus_long_j}} jours. À quoi sert-il ?**
**À protéger les ouvrages SUIVANTS**, pas celui qu'il mesure — il est déjà construit. Ce n'est donc
pas un point d'arrêt, et on ne l'attend pas pour avancer.

**6. La criticité d'un risque passe de {{qualite.criticite.valeurs_distinctes.0}} à {{qualite.criticite.valeurs_distinctes.1}}. Que peut-on en dire ?**
**Qu'il a changé de rang**, et rien de plus. Ce sont des échelles ordinales : la différence, le
rapport et le pourcentage n'ont aucun contenu. Et sur ce tableau, les huit risques ne prennent que
trois valeurs distinctes — {{qualite.criticite.valeurs_distinctes.0}},
{{qualite.criticite.valeurs_distinctes.1}} et {{qualite.criticite.valeurs_distinctes.2}} : l'outil
range, grossièrement, et c'est tout ce qu'on lui demande.

**7. Une reprise sous consignation prend 3 jours au lieu de 2. Combien coûte le jour de plus ?**
**Rien, ou {{qualite.quantification_du_retard.pas_j}} jours** — et c'est la question qui est mal
posée. Le retard est **quantifié** par la période des fenêtres : si les deux durées font rater le
même créneau, le jour de plus ne coûte rien ; s'il fait franchir le palier, il coûte la période
entière. Ce qu'il faut savoir avant de répondre n'est pas la durée de la reprise, c'est la date de
la prochaine fenêtre.

**8. Pourquoi lire aussi la gravité seule ?**
Parce qu'un risque **rare, détectable et mortel** se classe mal en criticité et se traite quand même.
On n'arbitre pas une vie contre un rang — et c'est la différence de fond entre piloter la qualité et
piloter la sécurité.

:::memo
## Fiche mémo — qualité, HSE, environnement

**Les deux phrases du module**

> L'exposition se compte en **heures**, jamais en effectif ni en durée.
> Le coût d'une non-conformité n'est pas le coût de sa reprise.

**Les deux formules**

$$ TF = \frac{\text{accidents} \times 10^6}{\text{heures}} \qquad TG = \frac{\text{journées perdues} \times 10^3}{\text{heures}} $$

**Les cinq colonnes d'un plan de contrôle** — plus la sixième, qu'on oublie

Qui · Quand · Sur quel critère · **En combien de temps le résultat arrive** · Ce qui se passe si
c'est non conforme. Et : ce contrôle est-il un point d'arrêt, avec sa durée au planning ?

**Les chiffres de ce chantier**

| | |
|---|---:|
| Heures travaillées, sur site, toutes entreprises | {{qualite.exposition.heures_totales::n0}} h |
| dont de nuit sous consignation | {{qualite.exposition.part_de_nuit_pct::n1}} % des heures · **{{qualite.exposition.part_de_nuit_dans_le_risque_pct::n1}} % du risque** ({{qualite.exposition.part_de_nuit_dans_le_risque_bornes_pct.0::n1}} à {{qualite.exposition.part_de_nuit_dans_le_risque_bornes_pct.1::n1}}) |
| Exposition d'une nuit d'interception | ×{{qualite.exposition.presence_et_production_de_nuit.rapport_presence_production::n2}} son temps productif |
| Coût d'une NC de parement | part visible {{qualite.non_conformite.part_visible_sur_un_devis_MAD::n0}} MAD · total de {{qualite.non_conformite.par_ouvrage.2.total_MAD::n0}} à {{qualite.non_conformite.par_ouvrage.0.total_MAD::n0}} selon l'ouvrage |
| L'écart entre les régimes | **×{{qualite.non_conformite.ecart_entre_les_regimes::n1}}** — c'est le seul nombre que les fourchettes ne bougent pas |
| La même NC, selon l'ouvrage | {{qualite.impact_planning.lignes.0.retard_du_chantier_j::n0}} / {{qualite.impact_planning.lignes.1.retard_du_chantier_j::n0}} / {{qualite.impact_planning.lignes.2.retard_du_chantier_j::n0}} j de chantier — amplifié, transmis, absorbé |
| Retard sous consignation | **quantifié** par pas de {{qualite.quantification_du_retard.pas_j}} j — une demi-journée coûte le pas entier |
| Déchets | {{qualite.dechets.total_tonnes::n0}} t ({{qualite.dechets.total_bornes_tonnes.0::n0}} à {{qualite.dechets.total_bornes_tonnes.1::n0}}) · {{qualite.dechets.taux_de_valorisation_pct::n0}} % valorisées |
| Dont dangereux | {{qualite.dechets.part_dangereuse_pct::n2}} % du poids, 100 % de l'organisation |

**Les quatre réflexes**

1. Tout indicateur de sécurité porte des **heures** au dénominateur — et on demande toujours de **quelles** heures, de **quelles** entreprises, sur **quelle** période.
2. La **marge** dit si le retard passe, la **consignation** de combien il est amplifié — et la sécurité, elle, ne se hiérarchise sur aucune des deux.
3. Un critère de contrôle peut porter une valeur à condition de **nommer son document** ; ce qui est interdit, c'est la valeur orpheline.
4. La criticité **classe**. Elle ne mesure pas, ne se moyenne pas, ne varie pas en pourcentage.
5. Sous consignation, le premier jour perdu coûte tout et les suivants ne coûtent rien : **tout se joue avant la fenêtre**.

**⏸ Ce qui reste fermé sans les documents** — fréquences de prélèvement, critères de résistance et
de conformité, tolérances géométriques, distances de sécurité, seuils d'exposition au bruit et aux
poussières, obligations de tri. Toutes ces valeurs sont réglementaires ou propres au marché. Le
module en donne la méthode et la place dans le plan, jamais la valeur.
:::
