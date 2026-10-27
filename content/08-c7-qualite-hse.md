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
   connaît maintenant ses heures exactement, tâche par tâche ;
2. **le coût d'une non-conformité** n'est pas le coût de sa reprise : la reprise est la plus petite
   des quatre lignes, et les trois autres n'ont pas de facture ;
3. **la criticité d'un risque est un produit de rangs** : elle classe, elle ne mesure pas — et c'est
   l'outil le plus utilisé et le plus mal lu des analyses de risques.

Ce qu'il ne fait pas : citer une fréquence de prélèvement, un critère de résistance, une distance de
sécurité, un seuil d'exposition. Toutes ces valeurs sont réglementaires ou propres au marché, et
elles restent **⏸**. Un plan de contrôle qui les contiendrait serait faux dès le premier chantier
où le CPS diffère.

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
| Accidents avec arrêt attendus | {{qualite.exposition.accidents_avec_arret_attendus::n2}} |

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

### a. Ce que la non-conformité coûte vraiment

Un défaut de parement est constaté au décoffrage d'une levée de voile de noyau, en hall voyageurs :
nids de cailloux et fuites de laitance sur {{gare.qualite_hse.non_conformite.surface_m2.valeur::n0}} m².
Le réflexe est de demander un devis de reprise. Voici les quatre lignes.

| Poste | Montant | Sur un devis ? | |
|---|---:|:-:|---|
| {{qualite.non_conformite.lignes.0.poste}} | {{qualite.non_conformite.lignes.0.montant_MAD::n0}} MAD | oui | {{qualite.non_conformite.lignes.0.note}}, à ⟦V3|coût de reprise d'un parement vu|420|MAD/m²|250 à 700|2026|piquage, ragréage, reprise de parement et protection des abords : varie fortement selon que le parement reste vu ou sera doublé⟧ |
| {{qualite.non_conformite.lignes.1.poste}} | {{qualite.non_conformite.lignes.1.montant_MAD::n0}} MAD | **non** | {{qualite.non_conformite.lignes.1.note}} |
| {{qualite.non_conformite.lignes.2.poste}} | {{qualite.non_conformite.lignes.2.montant_MAD::n0}} MAD | **non** | {{qualite.non_conformite.lignes.2.note}} |
| {{qualite.non_conformite.lignes.3.poste}} | {{qualite.non_conformite.lignes.3.montant_MAD::n0}} MAD | **non** | {{qualite.non_conformite.lignes.3.note}} |
| **Total** | **{{qualite.non_conformite.total_MAD::n0}} MAD** | | dont {{qualite.non_conformite.part_visible_pct::n1}} % visibles |

{{qualite.non_conformite.lecture}}

:::figure {"fn":"cascade","args":"qualite.figures.cout_nc","titre":"De la reprise au coût réel d'une non-conformité","num":2,"large":true,"options":{"unite":"MAD"},"voir":["La première barre est la seule qui ait une facture. Les trois autres sont du temps : temps de chantier pendant la décision et la reprise, temps de contrôle sur tout ce qui suit.","Le poste le plus cher est souvent l'ATTENTE DE LA DÉCISION — expertise, avis du BET, accord sur la méthode. Personne ne le pilote, parce qu'il n'apparaît nulle part.","La quatrième barre est minuscule — {{qualite.non_conformite.lignes.3.montant_MAD::n0}} MAD, à peine visible — et il faut le dire : en argent, le durcissement du contrôle ne pèse rien. Son coût est ailleurs, dans l'attention qu'il détourne et dans la relation avec la maîtrise d'œuvre, et ce cours ne sait pas le chiffrer.","Il porte pourtant sur les {{gare.qualite_hse.non_conformite.levees_restantes.valeur}} levées restantes, c'est-à-dire sur des ouvrages qui n'ont AUCUN défaut : une non-conformité coûte aussi sur ce qui est bien fait."],"erreur":"Négocier le prix de la reprise au dirham près pendant que l'attente de la décision court. Le poste le plus cher d'une non-conformité est celui qui n'a pas de facture."}
:::

{{qualite.non_conformite._le_piege}}

**Et ce que ce chiffre ne contient pas.** {{qualite.non_conformite.ce_qui_n_est_PAS_chiffre_ici}}

### b. La même non-conformité, selon l'ouvrage qu'elle touche

{{qualite.impact_planning.lecture}}

| Ouvrage | Marge totale | Immobilisation | Retard du **chantier** | |
|---|---:|---:|---:|---|
| {{qualite.impact_planning.lignes.0.tache}} · {{qualite.impact_planning.lignes.0.nom}} | {{qualite.impact_planning.lignes.0.marge_totale_j::n1}} j | {{qualite.impact_planning.immobilisation_j::n0}} j | **{{qualite.impact_planning.lignes.0.retard_du_chantier_j::n1}} j** | amplifié |
| {{qualite.impact_planning.lignes.1.tache}} · {{qualite.impact_planning.lignes.1.nom}} | {{qualite.impact_planning.lignes.1.marge_totale_j::n1}} j | {{qualite.impact_planning.immobilisation_j::n0}} j | {{qualite.impact_planning.lignes.1.retard_du_chantier_j::n1}} j | transmis |
| {{qualite.impact_planning.lignes.2.tache}} · {{qualite.impact_planning.lignes.2.nom}} | {{qualite.impact_planning.lignes.2.marge_totale_j::n1}} j | {{qualite.impact_planning.immobilisation_j::n0}} j | {{qualite.impact_planning.lignes.2.retard_du_chantier_j::n1}} j | absorbé |

:::encart {"genre":"voir","titre":"Le régime qui surprend : sous consignation, le retard est amplifié"}
Les {{qualite.impact_planning.immobilisation_j::n0}} jours d'immobilisation deviennent
**{{qualite.impact_planning.lignes.0.retard_du_chantier_j::n1}} jours** de chantier sur
{{qualite.impact_planning.lignes.0.tache}}. Ce n'est pas une erreur de calcul : une tâche qui attend
une fenêtre de consignation et rate son créneau n'attend pas la fin de sa reprise — elle attend la
**fenêtre suivante**, un mois plus tard. Le module B7c a montré pourquoi ; C7 en tire la
conséquence pour le pilotage de la qualité.

**Trois régimes, donc, pour la même non-conformité**, et ils ne se devinent pas sur le chantier : les
trois ouvrages se ressemblent, et c'est le **réseau** qui fait la différence. D'où la règle :

> Une non-conformité se hiérarchise sur sa **marge**, pas sur sa gravité technique.

{{qualite.impact_planning._consequence_de_pilotage}}
:::

{{qualite.impact_planning._ce_que_ce_chantier_montre_en_particulier}}

### c. Le plan de contrôle du cas phare

| Contrôle | Qui | Quand | Critère | Résultat | Si non conforme |
|---|---|---|---|---:|---|
| **{{qualite.plan_de_controle.lignes.0.controle}}** | {{qualite.plan_de_controle.lignes.0.qui}} | {{qualite.plan_de_controle.lignes.0.quand}} | {{qualite.plan_de_controle.lignes.0.critere}} | {{qualite.plan_de_controle.lignes.0.delai_du_resultat_j}} j | {{qualite.plan_de_controle.lignes.0.si_non_conforme}} |
| **{{qualite.plan_de_controle.lignes.1.controle}}** | {{qualite.plan_de_controle.lignes.1.qui}} | {{qualite.plan_de_controle.lignes.1.quand}} | {{qualite.plan_de_controle.lignes.1.critere}} | {{qualite.plan_de_controle.lignes.1.delai_du_resultat_j}} j | {{qualite.plan_de_controle.lignes.1.si_non_conforme}} |
| **{{qualite.plan_de_controle.lignes.2.controle}}** | {{qualite.plan_de_controle.lignes.2.qui}} | {{qualite.plan_de_controle.lignes.2.quand}} | {{qualite.plan_de_controle.lignes.2.critere}} | {{qualite.plan_de_controle.lignes.2.delai_du_resultat_j}} j | {{qualite.plan_de_controle.lignes.2.si_non_conforme}} |
| **{{qualite.plan_de_controle.lignes.3.controle}}** | {{qualite.plan_de_controle.lignes.3.qui}} | {{qualite.plan_de_controle.lignes.3.quand}} | {{qualite.plan_de_controle.lignes.3.critere}} | **{{qualite.plan_de_controle.lignes.3.delai_du_resultat_j}} j** | {{qualite.plan_de_controle.lignes.3.si_non_conforme}} |
| **{{qualite.plan_de_controle.lignes.4.controle}}** | {{qualite.plan_de_controle.lignes.4.qui}} | {{qualite.plan_de_controle.lignes.4.quand}} | {{qualite.plan_de_controle.lignes.4.critere}} | {{qualite.plan_de_controle.lignes.4.delai_du_resultat_j}} j | {{qualite.plan_de_controle.lignes.4.si_non_conforme}} |
| **{{qualite.plan_de_controle.lignes.5.controle}}** | {{qualite.plan_de_controle.lignes.5.qui}} | {{qualite.plan_de_controle.lignes.5.quand}} | {{qualite.plan_de_controle.lignes.5.critere}} | {{qualite.plan_de_controle.lignes.5.delai_du_resultat_j}} j | {{qualite.plan_de_controle.lignes.5.si_non_conforme}} |

Les critères renvoient au marché ou au plan visé — ils ne les remplacent pas. **Aucun seuil chiffré
n'est donné ici**, et c'est volontaire : un plan de contrôle qui porterait des valeurs serait faux
dès le premier chantier dont le CPS diffère.

{{qualite.plan_de_controle._le_cout_du_point_d_arret}}

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

:::figure {"fn":"barres","args":"qualite.figures.criticite","titre":"Les risques classés par criticité — un rang, pas une mesure","num":3,"large":true,"options":{"unite":"criticité f × g × d, échelles ordinales de 1 à 4"},"voir":["Les longueurs de barre se comparent, mais elles ne se soustraient pas : une barre deux fois plus longue n'est pas un risque deux fois plus grand. L'axe porte des rangs multipliés.","{{qualite.criticite.ex_aequo_en_tete.length}} risques sont EX ÆQUO en tête, tous à {{qualite.criticite.lignes.0.criticite}}. Avec des notes de 1 à 4, le produit ne prend que peu de valeurs : le classement ne départage pas, et c'est à l'équipe de le faire — pas au tableau.","Parmi eux, deux ont la fréquence la plus haute et la gravité la plus basse : {{qualite.criticite.risques_a_faible_gravite_mais_frequents.0}} et {{qualite.criticite.risques_a_faible_gravite_mais_frequents.1}}. Ils ne font pas d'accident, ils font des carrières écourtées, et aucun tableau de bord hebdomadaire ne les voit.","Un risque de gravité 4 se traite même s'il se classe mal : on n'arbitre pas une vie contre un rang."],"erreur":"Tirer un trait de seuil sur ce graphique et traiter ce qui dépasse. Le seuil dépend entièrement du choix des échelles ; deux équipes avec deux échelles différentes traiteront deux listes différentes, et aucune n'aura tort."}
:::

{{qualite.criticite._ce_que_les_ex_aequo_disent}}

{{qualite.criticite.pourquoi_lire_aussi_la_gravite_seule}}

### e. Les déchets : celui qui pèse le moins commande le plus

{{qualite.dechets.lecture}}

| Flux | kg/m² | Tonnes | Valorisation |
|---|---:|---:|---:|
| {{qualite.dechets.lignes.0.flux}} | {{qualite.dechets.lignes.0.kg_m2::n1}} | {{qualite.dechets.lignes.0.tonnes::n1}} t | {{qualite.dechets.lignes.0.valorisation_pct}} % |
| {{qualite.dechets.lignes.1.flux}} | ⟦V3|déchets d'acier et de métaux d'un chantier de gros œuvre|4,5|kg/m²|2,0 à 9,0|2026|chutes de façonnage et emballages métalliques, rapportées à l'emprise construite⟧ | {{qualite.dechets.lignes.1.tonnes::n1}} t | {{qualite.dechets.lignes.1.valorisation_pct}} % |
| {{qualite.dechets.lignes.2.flux}} | {{qualite.dechets.lignes.2.kg_m2::n1}} | {{qualite.dechets.lignes.2.tonnes::n1}} t | {{qualite.dechets.lignes.2.valorisation_pct}} % |
| {{qualite.dechets.lignes.3.flux}} | ⟦V3|déchets d'emballages et divers d'un chantier de gros œuvre|3,5|kg/m²|1,5 à 8,0|2026|films, palettes, cartons et divers non triés à la source⟧ | {{qualite.dechets.lignes.3.tonnes::n1}} t | {{qualite.dechets.lignes.3.valorisation_pct}} % |
| {{qualite.dechets.lignes.4.flux}} | {{qualite.dechets.lignes.4.kg_m2::n1}} | {{qualite.dechets.lignes.4.tonnes::n1}} t | {{qualite.dechets.lignes.4.valorisation_pct}} % |
| **Total** | | **{{qualite.dechets.total_tonnes::n1}} t** | **{{qualite.dechets.taux_de_valorisation_pct::n1}} %** |

{{qualite.dechets._dangereux}}

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

**Le lien avec le reste du module.** Le § S4b montre qu'une non-conformité se hiérarchise sur sa
marge. La sécurité, elle, ne se hiérarchise pas ainsi : **un risque de gravité maximale se traite
quel que soit son rang et quelle que soit la marge de la tâche.** C'est la seule différence de fond
entre piloter la qualité et piloter la sécurité, et elle doit être dite, parce que les deux se
tiennent dans le même tableau de bord et obéissent à deux logiques opposées.

## S5 · Erreurs fréquentes, et ce qu'elles coûtent

| Erreur | Comment elle se voit | Ce qu'elle coûte |
|---|---|---|
| Rapporter un indicateur de sécurité à un **effectif** | deux chantiers incomparables ont le même chiffre | on compare des chantiers qui n'ont rien de comparable |
| Concentrer la prévention sur les tâches **spectaculaires** | le levage est surveillé, le second œuvre non | la phase qui porte le plus d'heures est la moins suivie |
| Oublier la surexposition de nuit | les heures de nuit comptent comme les autres | {{qualite.exposition.part_de_nuit_pct::n1}} % des heures portent {{qualite.exposition.part_de_nuit_dans_le_risque_pct::n1}} % du risque |
| Chiffrer une NC sur sa **reprise** | le devis fait foi | {{qualite.non_conformite.part_visible_pct::n1}} % du coût réel ; le reste est du temps |
| Négocier le prix de la reprise pendant que la décision attend | on gagne 5 % sur la plus petite ligne | l'attente coûte {{qualite.non_conformite.frais_de_duree_MAD_par_jour_ouvre::n0}} MAD par jour |
| Hiérarchiser les NC sur leur **gravité technique** | la plus visible passe en premier | celle qui est sur une tâche à marge nulle attend, et coûte {{qualite.impact_planning.lignes.0.retard_du_chantier_j::n0}} jours |
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

À 1 800 h par compagnon et par an, A totalise environ 21 600 h et B 108 000 h. Les taux de fréquence
sont alors de $2 \times 10^6 / 21\,600 = 93$ pour A et $5 \times 10^6 / 108\,000 = 46$ pour B.
**A est deux fois plus accidentogène que B**, et c'est lui qu'on félicite.

*Et une seconde réserve, qui vaut la première : avec 2 et 5 accidents, les deux taux sont des
estimations très incertaines. Un accident de plus ou de moins déplace le taux de moitié. Un TF sur
un petit chantier et une seule année ne se compare pas — il se cumule sur plusieurs années ou sur
plusieurs chantiers avant de vouloir dire quelque chose. C'est la même limite que le CPI du module
D4 en début de chantier : un indicateur a besoin d'une assiette avant d'avoir un sens.*
:::

:::exercice {"titre":"2 · Deux non-conformités le même matin","niveau":"probleme"}
Lundi, deux constats. Le premier : un défaut de parement sur un voile de hall, très visible, le
maître d'ouvrage l'a vu. Le second : un défaut d'enrobage sur une pièce de charpente à lever sous
consignation la semaine suivante, que personne n'a remarqué. Vous avez une équipe disponible. Par
quoi commencez-vous ?

**Corrigé. Par le second, et ce n'est pas discutable.**

Le défaut de parement touche un ouvrage qui a de la marge : sa reprise coûte de l'argent et
**{{qualite.impact_planning.lignes.2.retard_du_chantier_j::n0}} jour de chantier**. Le défaut sur la
charpente touche une tâche à marge nulle, soumise à consignation : s'il fait rater la fenêtre, il
coûte **{{qualite.impact_planning.lignes.0.retard_du_chantier_j::n0}} jours**, parce que la fenêtre
suivante est un mois plus tard.

**Le rapport est de 1 à {{qualite.impact_planning.lignes.0.retard_du_chantier_j::n0}}**, et il ne se
lit ni sur la gravité technique, ni sur la visibilité, ni sur la surface concernée. Il se lit sur le
planning.

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

**Ligne 2 — le piège du cours.** Le critère est **chiffré**. Il est peut-être juste sur ce
chantier-ci ; il sera faux sur le suivant, et il le sera en silence. Un critère d'enrobage se lit
dans le plan visé et dans le marché, et la ligne doit y **renvoyer** au lieu de le recopier. Second
défaut : le responsable est **celui qui exécute**. Un contrôle fait par celui qui a fait le travail
n'est pas un contrôle, c'est une relecture — utile, mais elle ne remplace pas le regard extérieur.

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
| **Bordereau de suivi** | document qui accompagne un déchet dangereux de sa production à son traitement |
| **PPSPS** | plan de sécurité propre à l'entreprise sur un chantier donné |

**Quiz**

**1. Un chantier a 3 accidents, un autre 6. Lequel est le plus sûr ?**
**On ne peut pas le dire** sans les heures travaillées. C'est le dénominateur qui fait l'indicateur,
exactement comme pour un avancement (module D4).

**2. Les heures de nuit représentent {{qualite.exposition.part_de_nuit_pct::n1}} % des heures. Quelle part du risque ?**
**{{qualite.exposition.part_de_nuit_dans_le_risque_pct::n1}} %**, avec un coefficient de
surexposition de {{qualite.exposition.coefficient_de_surexposition_de_nuit}}. Une heure de nuit n'est
pas une heure.

**3. Une reprise de parement coûte {{qualite.non_conformite.lignes.0.montant_MAD::n0}} MAD. Combien coûte la non-conformité ?**
**{{qualite.non_conformite.total_MAD::n0}} MAD**, dont seulement
{{qualite.non_conformite.part_visible_pct::n1}} % ont une facture. Le reste est de l'attente, de
l'immobilisation et du contrôle supplémentaire sur des ouvrages sans défaut.

**4. Deux NC de même gravité. Laquelle traiter en premier ?**
**Celle qui touche l'ouvrage à marge nulle.** La gravité technique ne hiérarchise pas : la marge le
fait. Et sous consignation, le retard est **amplifié** — on ne rate pas sa reprise, on rate sa
fenêtre.

**5. Un essai rend son résultat à {{qualite.plan_de_controle.delai_le_plus_long_j}} jours. À quoi sert-il ?**
**À protéger les ouvrages SUIVANTS**, pas celui qu'il mesure — il est déjà construit. Ce n'est donc
pas un point d'arrêt, et on ne l'attend pas pour avancer.

**6. La criticité d'un risque passe de 36 à 24. Que peut-on en dire ?**
**Qu'il a changé de rang**, et rien de plus. Ce sont des échelles ordinales : la différence, le
rapport et le pourcentage n'ont aucun contenu.

**7. Pourquoi lire aussi la gravité seule ?**
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
| Heures travaillées | {{qualite.exposition.heures_totales::n0}} h |
| dont de nuit | {{qualite.exposition.part_de_nuit_pct::n1}} % des heures · **{{qualite.exposition.part_de_nuit_dans_le_risque_pct::n1}} % du risque** |
| Coût réel d'une NC de parement | {{qualite.non_conformite.total_MAD::n0}} MAD, dont {{qualite.non_conformite.part_visible_pct::n1}} % facturables |
| La même NC, selon l'ouvrage | {{qualite.impact_planning.lignes.0.retard_du_chantier_j::n0}} j / {{qualite.impact_planning.lignes.1.retard_du_chantier_j::n0}} j / {{qualite.impact_planning.lignes.2.retard_du_chantier_j::n0}} j de chantier |
| Déchets | {{qualite.dechets.total_tonnes::n0}} t · {{qualite.dechets.taux_de_valorisation_pct::n0}} % valorisées |
| Dont dangereux | {{qualite.dechets.part_dangereuse_pct::n2}} % du poids, 100 % de l'organisation |

**Les quatre réflexes**

1. Tout indicateur de sécurité porte des **heures** au dénominateur.
2. Une NC se hiérarchise sur sa **marge**, pas sur sa gravité technique — la sécurité, elle, non.
3. Un critère de contrôle **renvoie** au marché, il ne le recopie pas.
4. La criticité **classe**. Elle ne mesure pas, ne se moyenne pas, ne varie pas en pourcentage.

**⏸ Ce qui reste fermé sans les documents** — fréquences de prélèvement, critères de résistance et
de conformité, tolérances géométriques, distances de sécurité, seuils d'exposition au bruit et aux
poussières, obligations de tri. Toutes ces valeurs sont réglementaires ou propres au marché. Le
module en donne la méthode et la place dans le plan, jamais la valeur.
:::
