---
id: REC
titre: Réception, DOE, garanties — le jour où le risque change de mains
fil: Palier 1 · module 9 — direction de projet
resume: La réception n'est pas une formalité de fin de chantier : c'est un transfert de risque, et chaque jour qui la retarde a un prix. Ce prix change de régime au centième jour, et presque personne ne le sait avant d'y être.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · aucune durée de garantie, aucun délai de levée, aucun contenu réglementaire de DOE n'est cité
pied: Exemple pédagogique — ne remplace ni le CPS du marché, ni le CCAG-Travaux, ni l'avis d'un juriste. Les durées, les délais et les conditions de la réception se lisent dans le contrat et dans le droit applicable.
donnees: reception, prix, planification, gare
---

## S1 · Ce que ce module fait, et ce qu'il ne peut pas faire

C'est le dernier module du palier 1, et il ferme le déroulé imposé : programme, conception,
géotechnique, exécution, suivi, qualité — et maintenant la fin. Il a une particularité : **il ne
calcule presque rien lui-même.** Les frais de durée viennent de D1, la date vient de D2, la retenue
de garantie vient de la trésorerie de D1. Ce module les lit et en tire ce qu'aucun d'eux ne pouvait
voir seul.

Quatre résultats, tous **non normatifs**, c'est-à-dire qu'aucun ne dépend d'un texte :

1. **Un jour de non-réception a un prix, et ce prix change de régime.** Tant que les pénalités
   courent, il vaut {{reception.cout_d_un_jour.cout_avant_le_plafond_MAD_par_jour_ouvre::n0}} MAD ;
   une fois le plafond atteint, {{reception.cout_d_un_jour.cout_apres_le_plafond_MAD_par_jour_ouvre::n0}} —
   **{{reception.cout_d_un_jour.rapport_des_deux_regimes::n1}} fois moins**.
2. **Le jour de bascule ne dépend pas du montant du marché.** C'est le plafond en pour-cent divisé
   par la pénalité en pour-mille, et rien d'autre.
3. **L'arbitrage entre retenue de garantie et caution bancaire ne dépend pas de la durée de la
   garantie** — qui est pourtant la première chose qu'on cherche, et qui est ⏸ dans ce cours. La
   durée se simplifie.
4. **Le DOE se constitue pendant le chantier.** Reconstitué après coup, il coûte
   {{reception.doe.rapport_des_heures::n1}} fois plus d'heures de cadre, et il immobilise le
   décompte définitif pendant qu'on le reconstitue.

Ce qu'il ne fait pas : citer la durée d'une garantie, le délai de levée des réserves, les conditions
d'une réception tacite, le contenu obligatoire du DOE, le délai de paiement du décompte définitif.
Toutes ces valeurs sont réglementaires ou propres au marché, et elles restent **⏸**. Le module donne
le **mécanisme** et sa **conséquence financière** ; jamais la durée.

:::encart {"genre":"attente","titre":"Ce que ce module n'est pas"}
Ce n'est pas un cours de droit, et il ne peut pas en tenir lieu. Les mots « réception », « réserve »,
« garantie », « décompte définitif » ont un sens juridique précis qui dépend du droit applicable et
du marché — et ce sens, ici, n'est pas cité. Ce qui est décrit, c'est la **fonction** que chaque
mécanisme remplit et ce qu'il coûte par jour. Un chef de projet suivi qui connaît le coût d'un jour
de non-réception lit son CPS autrement : il sait quelles clauses chercher en premier.
:::

## S2 · L'idée centrale : la réception transfère un risque, et il a un prix par jour

Tant que la réception n'est pas prononcée, **l'entreprise porte tout** : les frais de durée de son
installation de chantier, la garde de l'ouvrage, les pénalités de retard, et le risque que quelque
chose arrive à un ouvrage terminé que personne n'habite encore. Le jour où la réception est
prononcée, tout cela s'arrête d'un coup. C'est la seule date du chantier qui change la nature des
obligations, et pas seulement leur montant.

D'où la question que ce module pose, et qui n'a rien d'une formalité : **combien coûte un jour de
plus avant cette date ?**

| | |
|---|---:|
| Montant du marché | {{reception.cout_d_un_jour.marche_MAD::n0}} MAD |
| Frais de durée, par jour ouvré | {{reception.cout_d_un_jour.frais_de_duree_MAD_par_jour_ouvre::n0}} MAD |
| Pénalités, par jour ouvré | {{reception.cout_d_un_jour.penalites_MAD_par_jour_ouvre::n0}} MAD |
| **Un jour de non-réception** | **{{reception.cout_d_un_jour.cout_avant_le_plafond_MAD_par_jour_ouvre::n0}} MAD** |
| Plafond des pénalités | {{reception.cout_d_un_jour.plafond_des_penalites_MAD::n0}} MAD |
| **Après le plafond, le même jour coûte** | **{{reception.cout_d_un_jour.cout_apres_le_plafond_MAD_par_jour_ouvre::n0}} MAD** |

{{reception.cout_d_un_jour.lecture}}

**Aucun de ces deux nombres n'est calculé ici.** Les frais de durée et la pénalité journalière sont
lus dans la sortie du module D1, qui les publie pour trois retards donnés. Ce que D1 ne cherche pas,
et que ce module trouve, c'est le **jour où le plafond est atteint** — et ce jour-là change tout.

:::encart {"genre":"piege","titre":"Le piège de calendrier, hérité de D1 et conservé tel quel"}
Les pénalités se comptent en jours **calendaires** et les frais de durée en jours **ouvrés**. Un
jour ouvré de retard porte donc
{{prix.bordereau.frais_de_duree.conversion.calendaires_par_jour_ouvre::n2}} jour de pénalité. Les
confondre sous-estime la pénalité d'un tiers — c'est le module D1 qui l'a trouvé, et ce module s'en
sert sans le refaire.

C'est aussi pourquoi le jour de bascule se publie **dans les deux calendriers** :
{{reception.cout_d_un_jour.jour_de_bascule_ouvre::n1}} jours ouvrés,
{{reception.cout_d_un_jour.jour_de_bascule_calendaire::n0}} jours calendaires. Annoncer l'un pour
l'autre dans une réunion est une erreur de six semaines.
:::

### Le jour de bascule ne contient pas le montant du marché

$$ j_{\text{bascule}} = \frac{\text{plafond en \%} \times 10}{\text{pénalité en ‰}} \quad \text{jours calendaires} $$

{{reception.cout_d_un_jour._la_forme_fermee}}

C'est ce qui en fait une **règle de lecture d'un CPS** plutôt qu'un résultat de ce chantier-ci :
deux lignes du contrat, divisées l'une par l'autre, donnent le jour où le levier du maître d'ouvrage
s'épuise. Sur ce marché : **{{reception.cout_d_un_jour.jour_de_bascule_calendaire::n0}} jours**, avec
des bornes de {{reception.cout_d_un_jour.jour_de_bascule_bornes_calendaires.0::n0}} à
{{reception.cout_d_un_jour.jour_de_bascule_bornes_calendaires.1::n0}} jours selon les clauses
retenues — **la date de bascule est plus incertaine que le coût lui-même**, et c'est elle qui décide
de la stratégie.

:::figure {"fn":"diagramme","args":"reception.figures.cout_cumule","titre":"Le coût cumulé d'un retard de réception — une droite qui se casse","num":1,"large":true,"options":{"unite":"MMAD","nom":"coût cumulé","depuisZero":true,"axeX":true,"uniteX":"jours ouvrés de retard","marqueur":{"$":"reception.figures.marqueur_bascule"}},"voir":["La courbe est une droite tant que les pénalités courent, puis une autre droite, bien plus plate. La cassure est au {{reception.cout_d_un_jour.jour_de_bascule_ouvre::n1}}ᵉ jour ouvré — {{reception.cout_d_un_jour.jour_de_bascule_calendaire::n0}}ᵉ jour calendaire.","Avant la cassure, la pente est de {{reception.courbe_du_cout.pente_avant_MAD_par_jour::n0}} MAD par jour. Après, {{reception.courbe_du_cout.pente_apres_MAD_par_jour::n0}} MAD : les frais de durée seuls.","Ce n'est pas un adoucissement, c'est la fin d'un mécanisme. Il n'y a rien derrière, sauf la résiliation — qui n'est pas sur ce graphique et qui coûte aux deux parties."],"erreur":"Lire la partie plate comme une bonne nouvelle. Pour l'entreprise, elle signifie que la pression contractuelle a disparu et que le maître d'ouvrage n'a plus que des moyens brutaux ; pour le maître d'ouvrage, qu'il a laissé son seul levier s'épuiser sans agir."}
:::

{{reception.cout_d_un_jour._ce_que_le_changement_de_regime_veut_dire}}

**Et ce qui n'est pas sur ce graphique.** {{reception.cout_d_un_jour._ce_qui_n_est_pas_chiffre}}

## S3 · Principes

### a. Les opérations préalables à la réception sont une tâche du planning

Entre « les travaux sont finis » et « la réception est prononcée », il se passe des choses, elles
prennent du temps, et ce temps est au prix du paragraphe précédent.

| | Étape | Qui | Durée | Fin |
|---:|---|---|---:|---:|
| 1 | {{reception.operations_prealables.etapes.0.etape}} | {{reception.operations_prealables.etapes.0.qui}} | {{reception.operations_prealables.etapes.0.duree_j}} j | j+{{reception.operations_prealables.etapes.0.fin_j}} |
| 2 | {{reception.operations_prealables.etapes.1.etape}} | {{reception.operations_prealables.etapes.1.qui}} | {{reception.operations_prealables.etapes.1.duree_j}} j | j+{{reception.operations_prealables.etapes.1.fin_j}} |
| 3 | {{reception.operations_prealables.etapes.2.etape}} | {{reception.operations_prealables.etapes.2.qui}} | {{reception.operations_prealables.etapes.2.duree_j}} j | j+{{reception.operations_prealables.etapes.2.fin_j}} |
| 4 | **{{reception.operations_prealables.etapes.3.etape}}** | {{reception.operations_prealables.etapes.3.qui}} | **{{reception.operations_prealables.etapes.3.duree_j}} j** | j+{{reception.operations_prealables.etapes.3.fin_j}} |
| 5 | {{reception.operations_prealables.etapes.4.etape}} | {{reception.operations_prealables.etapes.4.qui}} | {{reception.operations_prealables.etapes.4.duree_j}} j | j+{{reception.operations_prealables.etapes.4.fin_j}} |
| 6 | {{reception.operations_prealables.etapes.5.etape}} | {{reception.operations_prealables.etapes.5.qui}} | {{reception.operations_prealables.etapes.5.duree_j}} j | **j+{{reception.operations_prealables.etapes.5.fin_j}}** |

{{reception.operations_prealables.note}}

{{reception.operations_prealables._l_essai_qui_commande}}

**Les six pièges, un par étape** — ce sont eux qui font la différence entre
{{reception.operations_prealables.duree_totale_j}} jours et trois mois :

1. {{reception.operations_prealables.etapes.0.piege}} ;
2. {{reception.operations_prealables.etapes.1.piege}} ;
3. {{reception.operations_prealables.etapes.2.piege}} ;
4. {{reception.operations_prealables.etapes.3.piege}} ;
5. {{reception.operations_prealables.etapes.4.piege}} ;
6. {{reception.operations_prealables.etapes.5.piege}}.

### b. Les réserves : deux familles, et une seule bloque

{{reception.reserves.la_regle}}

Ce qui est **interdit**, et qui est la faute la plus répandue de la fin de chantier : compter les
lignes. « Quatre-vingt-dix réserves, on ne peut pas réceptionner » n'est pas un raisonnement, c'est
une impression — et elle coûte le prix d'une journée de non-réception par jour d'hésitation.

### c. La retenue de garantie immobilise de l'argent, et cet argent a un prix

La retenue de garantie est prélevée sur chaque situation et conservée jusqu'à la fin de la période
de garantie. Elle n'est pas perdue : elle est **immobilisée**. Et de l'argent immobilisé coûte le
taux auquel l'entreprise se finance.

Une caution bancaire peut la remplacer. Elle coûte une commission. Comparer les deux semble demander
la **durée de la garantie** — qui est ⏸. On va voir au § S4c que non.

### d. Le DOE n'est pas un dossier, c'est une condition de paiement

Le dossier des ouvrages exécutés conditionne le décompte définitif : tant qu'il est incomplet, le
solde ne se paie pas. Son contenu réglementaire est **⏸**. Son critère pratique, lui, ne dépend
d'aucun texte :

> {{gare.reception.doe._ce_qu_il_doit_contenir}}

## S4 · L'étude de cas : la fin du chantier de la gare

### a. Le planning prévoit-il la réception qu'il annonce ?

Le § S2 a donné le prix d'un jour. Le reste de ce module consiste à compter les jours — et à
montrer qu'on les dépense presque toujours sur les mauvaises décisions. La première occasion se
présente avant même la fin des travaux, dans le planning.

| | |
|---|---:|
| Durée prévue par le planning pour la réception | {{reception.confrontation_au_planning.duree_prevue_par_le_planning_j::n0}} j |
| Durée prévue pour les essais et la mise en service | {{reception.confrontation_au_planning.duree_des_essais_au_planning_j::n0}} j |
| Durée demandée par la séquence du § S3a | **{{reception.confrontation_au_planning.duree_demandee_par_la_sequence_j::n0}} j** |
| Écart | {{reception.confrontation_au_planning.ecart_j::n0}} j |
| **Décalage de la fin, mesuré en rejouant le réseau** | **{{reception.confrontation_au_planning.decalage_mesure_de_la_fin_j::n1}} j** |
| Au prix du jour de non-réception | {{reception.confrontation_au_planning.cout_de_l_ecart_MAD::n0}} MAD |

{{reception.confrontation_au_planning.lecture}}

L'étape « {{reception.confrontation_au_planning.etape_deja_portee_par_le_planning}} » n'est pas
comptée deux fois : le planning la porte déjà sous le nom « essais et mise en service », et c'est
elle qui explique l'essentiel de la durée. Ce qui déborde, ce sont les quatre étapes qui
l'encadrent.

:::encart {"genre":"attente","titre":"Ce que cette comparaison est, et ce qu'elle n'est pas"}
{{reception.confrontation_au_planning._ce_que_cette_comparaison_est}}
:::

{{reception.confrontation_au_planning._quoi_en_faire}}

### b. Les réserves de la gare : combien bloquent, et combien coûte de se tromper

La liste rendue à la visite compte {{reception.reserves.nb_total}} lignes. {{reception.reserves.nb_bloquantes}} d'entre elles empêchent l'usage ou mettent en cause la sécurité — soit {{reception.reserves.part_bloquante_pct::n1}} %.

| Famille | Exemple | Nombre | Empêche l'usage | Heures de levée |
|---|---|---:|:-:|---:|
| {{reception.reserves.lignes.0.famille}} | {{reception.reserves.lignes.0.exemple}} | {{reception.reserves.lignes.0.nombre}} | non | {{reception.reserves.lignes.0.heures::n0}} h |
| {{reception.reserves.lignes.1.famille}} | {{reception.reserves.lignes.1.exemple}} | {{reception.reserves.lignes.1.nombre}} | non | {{reception.reserves.lignes.1.heures::n0}} h |
| {{reception.reserves.lignes.2.famille}} | {{reception.reserves.lignes.2.exemple}} | {{reception.reserves.lignes.2.nombre}} | non | {{reception.reserves.lignes.2.heures::n0}} h |
| **{{reception.reserves.lignes.3.famille}}** | {{reception.reserves.lignes.3.exemple}} | **{{reception.reserves.lignes.3.nombre}}** | **OUI** | {{reception.reserves.lignes.3.heures::n0}} h |
| **{{reception.reserves.lignes.4.famille}}** | {{reception.reserves.lignes.4.exemple}} | **{{reception.reserves.lignes.4.nombre}}** | **OUI** | {{reception.reserves.lignes.4.heures::n0}} h |
| **Total** | | **{{reception.reserves.nb_total}}** | **{{reception.reserves.nb_bloquantes}}** | **{{reception.reserves.heures_totales::n0}} h** |

{{reception.reserves.lecture}}

Le temps de levée est **mesuré**, pas posé : ⟦V3|temps moyen de levée d'une réserve, intervention et reconstat compris|6 h|h|2 à 16|2026|l'étendue est large parce qu'une retouche de peinture et une reprise d'étanchéité n'ont rien de commun⟧ par réserve,
{{reception.reserves.effectif_de_levee}} compagnons, la journée de travail du cours. D'où
{{reception.reserves.jours_de_levee_des_bloquantes::n2}} jour pour les bloquantes et
{{reception.reserves.jours_de_levee_des_autres::n1}} jours pour les autres.

:::figure {"fn":"barres","args":"reception.figures.reserves","titre":"Les réserves de la gare, par famille — et celles qui empêchent la réception","num":2,"large":true,"options":{"unite":"nombre de réserves"},"voir":["Les deux familles qui bloquent sont les deux plus courtes du graphique : {{reception.reserves.nb_bloquantes}} lignes sur {{reception.reserves.nb_total}}, soit {{reception.reserves.part_bloquante_pct::n1}} %.","La longueur des barres n'entre pas dans la décision de réceptionner. Elle entre dans l'organisation de la levée — ce n'est pas la même question, et c'est à un autre moment.","Une réserve de sécurité isolée dans une liste de quatre-vingt-dix lignes d'aspect reste une réserve de sécurité. Le classement se fait ligne à ligne."],"erreur":"Lire ce graphique comme une mesure de l'avancement de la fin de chantier. Soixante-deux retouches de peinture ne retardent pas la mise en service d'une gare ; un escalator à l'arrêt, si."}
:::

{{reception.reserves._le_prix_de_la_confusion}}

:::encart {"genre":"piege","titre":"L'erreur symétrique est pire, et elle ne se voit pas"}
{{reception.reserves._et_dans_l_autre_sens}}

**Et une précision qui a son importance** : repousser la réception coûte
{{reception.reserves.cout_de_la_confusion_MAD::n0}} MAD *tant que les pénalités courent*. Au-delà du
plafond, la même hésitation ne coûte plus que
{{reception.reserves.cout_de_la_confusion_apres_le_plafond_MAD::n0}} MAD. Un chantier déjà très en
retard est donc un chantier où la pression de réceptionner s'effondre — exactement au moment où
l'exploitant, lui, l'attend le plus.
:::

### c. Retenue de garantie ou caution : la durée se simplifie

| | |
|---|---:|
| Retenue immobilisée | {{reception.portage.retenue_immobilisee_MAD::n0}} MAD |
| Taux de portage | ⟦V3|coût de l'argent pour l'entreprise, taux annuel|7,0 %|%/an|5,0 à 12,0|2026|découvert, ligne de crédit, ou coût d'opportunité des fonds propres⟧ |
| Commission de caution | ⟦V3|commission annuelle d'une caution de substitution|1,2 %|%/an|0,6 à 2,5|2026|varie avec la signature de l'entreprise et les garanties qu'elle donne à sa banque⟧ |
| Coût de la retenue | **{{reception.portage.cout_de_la_retenue_MAD_par_mois::n0}} MAD par mois** |
| Coût de la caution | **{{reception.portage.cout_de_la_caution_MAD_par_mois::n0}} MAD par mois** |
| Économie | {{reception.portage.economie_MAD_par_mois::n0}} MAD par mois · bornes {{reception.portage.economie_bornes_MAD_par_mois.0::n0}} à {{reception.portage.economie_bornes_MAD_par_mois.1::n0}} |

{{reception.portage.lecture}}

:::encart {"genre":"voir","titre":"La donnée manquante est inutile — c'est le seul endroit de ce palier où cela arrive"}
{{reception.portage._la_duree_se_simplifie}}

$$ \frac{C_{\text{retenue}}}{C_{\text{caution}}} = \frac{t \times M \times d}{c \times M \times d} = \frac{t}{c} $$

Le montant $M$ et la durée $d$ sont les mêmes des deux côtés, et ils disparaissent. Il reste deux
taux, et le rapport vaut **{{reception.portage.rapport_des_deux_couts::n2}}** — entre
{{reception.portage.rapport_bornes.0::n1}} et {{reception.portage.rapport_bornes.1::n1}} sur
l'étendue des deux fourchettes, donc toujours en faveur de la caution.

**C'est un réflexe à prendre bien au-delà de ce cas** : avant d'aller chercher une donnée qui
manque, regarder si la question posée ne porte pas sur un **rapport**. Si elle y porte, la donnée
manquante se simplifie peut-être. Le module C7 fait la même rencontre sur les taux de fréquence de
deux chantiers.
:::

{{reception.portage._ce_que_la_comparaison_ne_compte_pas}}

:::encart {"genre":"attente","titre":"Un optimum calculé n'est pas une décision (D-041)"}
{{reception.portage._et_ce_qui_n_est_pas_dans_le_calcul}}
:::

### d. Le DOE : ce que coûte de le reconstituer

| | Tenu au fil de l'eau | Reconstitué après coup |
|---|---:|---:|
| Heures de cadre | ⟦V3|heures de cadre pour tenir le DOE au fil de l'eau|80 h|h|40 à 160|2026|classer les documents à mesure qu'ils arrivent, et exiger le plan de récolement d'un lot quand il part⟧ | ⟦V3|heures de cadre pour reconstituer le même DOE après coup|320 h|h|160 à 600|2026|retrouver les sous-traitants partis, refaire relever ce qui ne l'a pas été, redemander des fiches à des fournisseurs qui ont changé de référence⟧ |
| Coût de ces heures | {{reception.doe.cout_au_fil_de_l_eau_MAD::n0}} MAD | {{reception.doe.cout_reconstitue_MAD::n0}} MAD |
| Décompte définitif bloqué | — | {{reception.doe.montant_bloque_MAD::n0}} MAD pendant ⟦V3|jours pendant lesquels le décompte définitif reste bloqué faute de DOE complet|60 j|j|20 à 180|2026|ce n'est pas une pénalité : c'est de l'argent dû, non payé, que l'entreprise porte⟧ |
| Coût de portage | — | {{reception.doe.cout_de_portage_MAD::n0}} MAD |
| **Surcoût total** | — | **{{reception.doe.cout_total_du_retard_de_DOE_MAD::n0}} MAD** |

{{reception.doe.lecture}}

:::figure {"fn":"cascade","args":"reception.figures.doe","titre":"Un DOE reconstitué : d'où vient le surcoût","num":3,"large":true,"options":{"unite":"milliers de MAD"},"voir":["La première barre est ce que le dossier aurait coûté s'il avait été tenu : c'est la seule qui soit du travail utile.","La deuxième est le surcoût en heures de cadre — retrouver, refaire relever, redemander.","La troisième est la plus grosse, et c'est la seule qui ne produise rien : de l'argent dû qui attend. Elle ne figure sur aucun devis et sur aucun budget de lot."],"erreur":"Juger le DOE sur son coût en heures. Les deux tiers du surcoût ne sont pas des heures : c'est le décompte définitif qui ne se paie pas, et il ne se voit nulle part dans les comptes du chantier."}
:::

{{reception.doe._pourquoi_c_est_sous_estime}}

{{reception.doe._le_montant_bloque_est_une_borne_basse}}

:::encart {"genre":"piege","titre":"La base de calcul des intérêts est une clause, pas une constante"}
{{reception.doe._la_base_est_une_clause}}
:::

## S4g · Sécurité : qui garde l'ouvrage entre la fin des travaux et la réception ?

C'est la période la plus mal couverte d'un chantier, et elle ne figure dans aucun plan de
prévention : les travaux sont finis, les équipes sont parties sur l'opération suivante, la base-vie
se démonte, et l'ouvrage — une gare, c'est-à-dire un bâtiment ouvert sur l'espace public et sur une
voie exploitée — est terminé, accessible, et gardienné par personne en particulier.

**Ce qui se passe réellement dans ces semaines-là**, et qui n'est pas une hypothèse d'école : les
clôtures se relâchent parce que plus personne n'a de raison de les refermer ; les protections
provisoires disparaissent avec les équipes qui les avaient posées ; les trappes et les regards
restent ouverts après le dernier essai ; l'éclairage provisoire est déposé avant que le définitif ne
soit réceptionné ; et des gens entrent — des curieux, des riverains, parfois des enfants.

**Trois dispositions qui ne se négocient pas**, et aucune ne coûte cher au regard du prix d'un jour
de non-réception :

1. **Un responsable nommé de la garde de l'ouvrage**, et une date de transfert écrite. Pas « la
   réception » en général : une date, un nom, un procès-verbal. Tant que cette date n'est pas
   passée, c'est l'entreprise, et elle doit le savoir.
2. **Les protections se déposent APRÈS la réception, pas après les travaux.** C'est l'inverse de ce
   que fait la pression de repli, et c'est le même mécanisme que le module C7 décrit pour les
   protections périphériques : la parade la plus efficace est celle qui s'installe avant et se
   dépose après.
3. **Une visite de fermeture, avec une liste.** Trappes, regards, gaines techniques, accès en
   toiture, locaux électriques, quais. La même liste que celle des essais, relue dans l'autre sens.

**Et le cas particulier d'une gare** : la voie reste exploitée pendant toute cette période. Un
ouvrage accessible à moins de quelques mètres d'une voie circulée, sans gardiennage, n'est pas un
problème de chantier — c'est un problème d'exploitation ferroviaire, et il se traite avec
l'exploitant, pas entre soi.

## S4h · La double lecture : entreprise et maîtrise d'œuvre

| | **Côté entreprise** | **Côté maîtrise d'œuvre** |
|---|---|---|
| **L'avis de fin de travaux** | il déclenche le compte à rebours : on ne l'envoie pas avant d'être prêt, et on ne l'envoie pas tard non plus — chaque jour coûte {{reception.cout_d_un_jour.cout_avant_le_plafond_MAD_par_jour_ouvre::n0}} MAD | il déclenche son obligation de convoquer la visite. Un avis reçu et non traité engage sa responsabilité, et la date qui compte est celle de la réception de l'avis, pas celle de la visite |
| **Les réserves** | une liste de travaux à faire, avec un coût et un délai — et une négociation sur ce qui relève du marché | un **constat**, écrit, daté, sur place. Elle ne se lève pas sur une photo. Et elle engage : une réserve oubliée est une réserve non opposable |
| **La décision de réceptionner** | elle arrête les frais de durée et les pénalités, elle libère la caution, elle fait courir les garanties | elle n'est pas la sienne : elle **propose**, le maître d'ouvrage décide. Proposer une réception sur un ouvrage dangereux l'engage lourdement |
| **Le DOE** | une tâche sans cadence qu'on repousse, et qui bloque le solde | le document dont **lui** aura besoin pour la vie de l'ouvrage, et qu'il est le seul à pouvoir exiger au bon moment — quand le sous-traitant est encore là |
| **Les essais de systèmes** | une prestation à organiser, souvent avec des tiers qu'il ne maîtrise pas | la **preuve** que l'ouvrage fonctionne, et la seule qui vaille devant l'exploitant. Un essai non constaté n'a pas eu lieu |
| **La retenue de garantie** | de la trésorerie immobilisée, qu'une caution peut libérer | une **garantie** d'exécution, qu'il doit pouvoir mobiliser si l'entreprise disparaît. Accepter une caution n'est pas une formalité : c'est accepter un autre débiteur |

**Ce qui se joue dans l'écart.** L'entreprise veut une date ; la maîtrise d'œuvre veut une preuve.
Les deux ont raison, et le conflit n'est pas dans les intentions mais dans le calendrier : la preuve
prend du temps, et le temps coûte. C'est pourquoi la seule façon de réceptionner vite est de
**préparer tôt** — les essais, les documents, la liste — et non de presser le jour venu.

## S5 · Erreurs fréquentes, et ce qu'elles coûtent

| Erreur | Comment elle se voit | Ce qu'elle coûte |
|---|---|---|
| Attendre une réception **sans réserve** | « on finit les détails et on réceptionne » | {{reception.cout_d_un_jour.cout_avant_le_plafond_MAD_par_jour_ouvre::n0}} MAD par jour d'attente, pour des retouches de peinture |
| Compter les réserves au lieu de les **qualifier** | « quatre-vingt-dix, c'est trop » | {{reception.reserves.cout_de_la_confusion_MAD::n0}} MAD sur ce chantier |
| Classer une réserve de **sécurité** en finition | elle est seule de sa famille dans une longue liste | un ouvrage reçu avec un garde-corps non conforme, et la responsabilité qui a changé de mains |
| Oublier les **opérations préalables** au planning | le planning finit au dernier coup de peinture | {{reception.operations_prealables.duree_totale_j}} jours de décalage, au prix du jour de non-réception |
| Porter une tâche « Réception » **non décomposée** | une ligne de {{reception.confrontation_au_planning.duree_prevue_par_le_planning_j::n0}} jours en fin de Gantt | il en faut {{reception.confrontation_au_planning.duree_demandee_par_la_sequence_j::n0}} : {{reception.confrontation_au_planning.decalage_mesure_de_la_fin_j::n0}} jours de fin, {{reception.confrontation_au_planning.cout_de_l_ecart_MAD::n0}} MAD |
| Lancer les **essais de systèmes** en dernier | ils révèlent des défauts d'interface entre lots | l'étape la plus longue ({{reception.operations_prealables.etapes.3.duree_j}} j) et celle qu'on ne maîtrise pas |
| Reconstituer le **DOE** après coup | personne ne l'a réclamé pendant le chantier | {{reception.doe.cout_total_du_retard_de_DOE_MAD::n0}} MAD, dont les deux tiers en argent qui attend |
| Ignorer le **plafond** des pénalités | on découvre au 90ᵉ jour que le levier a disparu | une stratégie construite sur un mécanisme qui s'arrête au {{reception.cout_d_un_jour.jour_de_bascule_calendaire::n0}}ᵉ jour |
| Confondre jours **ouvrés** et **calendaires** | la pénalité annoncée ne tombe pas juste | un tiers d'écart, et une date de bascule fausse de six semaines |
| Laisser l'ouvrage **sans gardien** après les travaux | rien, jusqu'au jour où quelqu'un entre | la responsabilité est encore celle de l'entreprise, et l'ouvrage est accessible |
| Accepter une **caution** sans regarder la ligne de crédit | le calcul montre une économie | la ligne qui garantit ce chantier ne garantira pas la soumission du mois prochain |
| Prendre la **base 365** pour une constante | les intérêts tombent presque juste | 1,4 % d'écart, et une clause qu'on n'a pas lue |

## S6 · Exercices

:::exercice {"titre":"1 · Deux clauses, un jour de bascule","niveau":"application"}
Un CPS prévoit une pénalité de retard de **2 ‰ par jour** et un plafond de **5 % du montant du
marché**. Le marché vaut 240 millions de dirhams. Au bout de combien de jours la pénalité
plafonne-t-elle ? Et si le marché valait 24 millions ?

**Corrigé.** Le montant du marché ne sert à rien.

$$ j_{\text{bascule}} = \frac{5 \times 10}{2} = 25 \text{ jours calendaires} $$

**Dans les deux cas.** Le montant figure au numérateur du plafond (5 % de M) et au dénominateur de
la pénalité (2 ‰ de M par jour) : il se simplifie. Vingt-cinq jours, que le marché vaille 24 ou 240
millions.

*Ce que l'exercice enseigne, et qui vaut plus que la formule : ces deux lignes d'un CPS ne se lisent
jamais séparément. « 2 ‰ par jour » paraît sévère et « plafond 5 % » paraît protecteur ; ensemble,
ils disent que la pénalité cesse de croître au bout de vingt-cinq jours. Sur le marché de ce cours
— ⟦V3|pénalité de retard, pour mille du montant du marché par jour|1,0 ‰|‰/j|0,5 à 2,0|2026|clause du CPS, à lire et non à supposer⟧ et
⟦V3|plafond des pénalités de retard, en pour-cent du marché|10 %|%|5 à 10|2026|clause du CPS, à lire et non à supposer⟧ — la bascule tombe au
{{reception.cout_d_un_jour.jour_de_bascule_calendaire::n0}}ᵉ jour. Quatre fois plus tard.*
:::

:::exercice {"titre":"2 · Réceptionner ou pas — cas ouvert","niveau":"cas_ouvert"}
Vendredi. La visite des opérations préalables est faite. Vous êtes chef de projet suivi côté
entreprise. L'exploitant veut ouvrir la gare dans trois semaines. La liste des réserves compte
{{reception.reserves.nb_total}} lignes, dont :

- un **escalator à l'arrêt**, en attente d'une pièce annoncée sous dix jours ;
- un **désenfumage non essayé** dans le hall, faute de créneau avec le lot technique ;
- {{reception.reserves.lignes.0.nombre}} retouches de peinture et calfeutrements ;
- les **plans de récolement** d'un lot manquent, le sous-traitant a quitté le chantier.

Le maître d'ouvrage vous demande ce qu'il doit faire. Que lui répondez-vous, et dans quel ordre
traitez-vous ces quatre points ?

**Corrigé — il n'y a pas une réponse, il y a une méthode.**

**1. Qualifier, pas compter.** Deux de ces quatre points empêchent l'usage ou mettent en cause la
sécurité : l'escalator (fonctionnement d'un ouvrage) et le désenfumage (sécurité des personnes). Les
deux autres non. La question n'est donc pas « peut-on réceptionner avec
{{reception.reserves.nb_total}} réserves ? » mais « peut-on réceptionner avec un désenfumage non
essayé ? » — et la réponse à celle-là est non, sans discussion.

**2. Le désenfumage d'abord, et il n'est pas négociable.** Ce n'est pas une réserve, c'est un
essai manquant. Un ouvrage recevant du public dont le désenfumage n'a pas été essayé ne se
réceptionne pas, et aucun calcul de coût n'entre dans cette décision. On cherche le créneau dans la
semaine, quitte à payer une intervention de nuit : c'est moins cher qu'un jour de non-réception, et
ce n'est pas la raison pour laquelle on le fait.

**3. L'escalator ensuite, et c'est une négociation.** Dix jours annoncés pour une pièce, c'est le
genre de délai qui en fait vingt. Deux options honnêtes : réceptionner avec réserve et une date
ferme de levée, si l'exploitant accepte d'ouvrir avec un escalator sur deux — c'est à **lui** de le
dire, pas à vous ; ou attendre, et payer
{{reception.cout_d_un_jour.cout_avant_le_plafond_MAD_par_jour_ouvre::n0}} MAD par jour. Le chiffre
se pose sur la table, il ne se cache pas.

**4. Les retouches : réserves, et on réceptionne.** Elles n'empêchent rien. Les traiter comme
bloquantes coûterait {{reception.reserves.cout_de_la_confusion_MAD::n0}} MAD sur l'ensemble de ce
chantier — plus de quarante fois le prix de les lever toutes.

**5. Les plans de récolement : le vrai problème est ailleurs.** Ils ne bloquent pas la réception,
mais ils bloqueront le **décompte définitif**, et le sous-traitant est parti. C'est la seule des
quatre lignes qui coûte plus cher chaque semaine qui passe, et c'est celle dont personne ne parle
vendredi. À traiter lundi matin, pendant qu'on retrouve encore quelqu'un au téléphone.

*Ce que le cas enseigne : la liste des réserves hiérarchise mal. Elle mélange une obligation de
sécurité, une négociation commerciale, un travail de finition et un problème de paiement — quatre
natures différentes, quatre interlocuteurs différents, et une seule colonne.*
:::

:::exercice {"titre":"3 · Revue critique — un DOE à refuser","niveau":"revue_critique"}
Voici le sommaire d'un DOE remis à la réception. Qu'est-ce qui ne va pas ?

> **1.** *Plans d'exécution — dossier de 340 plans au format PDF, nommés `PLAN-001.pdf` à
> `PLAN-340.pdf`.*
> **2.** *Notes de calcul — « voir dossier BET ».*
> **3.** *Fiches techniques des matériaux — classeur de 600 pages, non indexé.*
> **4.** *Plans de récolement des réseaux — « conformes aux plans d'exécution ».*
> **5.** *Notices d'entretien — notices constructeur en anglais, sans liste des équipements posés.*

**Corrigé.** Les cinq lignes ont un défaut commun et chacune en a un propre.

**Le défaut commun** : rien dans ce dossier ne permet de répondre aux quatre questions qui font un
DOE utilisable — **où** passe un réseau, **de quoi** est faite une paroi, **qui** a posé quoi,
**comment** on le remplace. C'est un volume d'archives.

**Ligne 1 — des plans sans nomenclature ne sont pas des plans.** Trois cent quarante fichiers
numérotés sans table des matières, sans indice de révision et sans correspondance avec les ouvrages
réalisés : retrouver le plan d'un local technique demandera d'en ouvrir cinquante. Un DOE se
parcourt par **l'ouvrage**, pas par le numéro de fichier.

**Ligne 2 — un renvoi n'est pas un document.** « Voir dossier BET » suppose que le dossier existe,
qu'il est accessible dix ans plus tard et que quelqu'un sait de quel BET il s'agit. Les trois
suppositions tomberont.

**Ligne 3 — six cents pages non indexées sont équivalentes à zéro page.** Le critère : retrouver la
fiche du produit posé dans un local donné en moins de deux minutes.

**Ligne 4 — c'est la ligne grave, et elle est fausse par construction.** « Conformes aux plans
d'exécution » est exactement ce qu'un plan de récolement n'est pas. Un récolement constate ce qui a
été **posé**, là où ça a été posé. Si c'était conforme à l'exécution, il n'y aurait pas besoin de
récoler. Cette ligne dit en réalité : *nous n'avons pas relevé*. Dans dix ans, quelqu'un percera un
mur en se fiant à ce document.

**Ligne 5 — une notice sans inventaire ne sert à personne.** Il manque la **liste des équipements
réellement posés**, avec leur emplacement, leur référence et leur date de pose. Et la langue n'est
pas un détail : une notice que l'équipe de maintenance ne peut pas lire n'est pas une notice.

*Ce qu'il faut en faire, côté maîtrise d'œuvre : refuser, et dire précisément pourquoi ligne par
ligne. Un refus motivé se corrige en quelques semaines ; un « dossier incomplet » sans précision
revient identique un mois plus tard. Et côté entreprise : ce dossier-là ne se corrige pas vraiment
après coup — la ligne 4 est irrattrapable sans rouvrir les ouvrages. C'est pour cela que le DOE se
constitue pendant le chantier.*
:::

## S7 · Check-list, glossaire et quiz

**Check-list : avant d'envoyer l'avis de fin de travaux**

1. Les **essais de systèmes** sont-ils faits, constatés et signés — ou seulement programmés ?
2. Le **DOE** est-il remis, et son sommaire permet-il de trouver un ouvrage en deux minutes ?
3. La liste des réserves est-elle **qualifiée** (empêche l'usage : oui / non) et non seulement comptée ?
4. Les réserves bloquantes ont-elles une **date de levée** et un responsable nommé ?
5. Les **opérations préalables** sont-elles au planning, avec leur durée ?
6. La **garde de l'ouvrage** a-t-elle un responsable nommé et une date de transfert écrite ?
7. A-t-on lu, dans le CPS, la **pénalité** et son **plafond** — et calculé le jour de bascule ?
8. La **retenue de garantie** peut-elle être remplacée par une caution, et la banque suivra-t-elle ?

**Glossaire**

| Terme | Ce que c'est |
|---|---|
| **Opérations préalables** | les constats et essais qui précèdent la décision de réceptionner. Une tâche du planning, avec une durée |
| **Réserve** | un écart constaté au moment de la réception. Deux familles seulement : elle empêche l'usage, ou non |
| **Réception** | la décision qui transfère la garde de l'ouvrage et arrête les frais de durée et les pénalités. Ses conditions et ses effets juridiques : **⏸** |
| **Retenue de garantie** | part de chaque situation conservée par le maître d'ouvrage jusqu'à la fin de la garantie. Immobilisée, pas perdue |
| **Caution de substitution** | garantie bancaire qui remplace la retenue. Coûte une commission, consomme une ligne de crédit |
| **DOE** | dossier des ouvrages exécutés. Son contenu réglementaire est **⏸** ; son critère pratique est qu'on y retrouve un ouvrage dix ans plus tard |
| **Plan de récolement** | ce qui a été **posé**, là où ça a été posé — et non ce qui avait été prévu |
| **Décompte définitif** | le dernier compte du marché. Conditionné par le DOE, et c'est par là que le DOE coûte cher |
| **Base de calcul des intérêts** | 365 ou 360 jours selon la convention de crédit. Une clause, pas une constante |

**Quiz**

**1. Un chantier a {{reception.reserves.nb_total}} réserves. Peut-on réceptionner ?**
**La question est mal posée.** Le nombre n'entre pas dans la décision. Seule compte la réponse à
« laquelle empêche l'usage ou met en cause la sécurité ? » — ici
{{reception.reserves.nb_bloquantes}} sur {{reception.reserves.nb_total}}.

**2. Le marché double. Le jour de bascule des pénalités change-t-il ?**
**Non.** Le montant est au numérateur du plafond et au dénominateur de la pénalité : il se simplifie.
Seules les deux clauses comptent.

**3. Un jour de retard coûte-t-il toujours la même chose ?**
**Non**, et le rapport est de {{reception.cout_d_un_jour.rapport_des_deux_regimes::n1}}. Avant le
plafond, {{reception.cout_d_un_jour.cout_avant_le_plafond_MAD_par_jour_ouvre::n0}} MAD ; après,
{{reception.cout_d_un_jour.cout_apres_le_plafond_MAD_par_jour_ouvre::n0}} — les frais de durée seuls.

**4. Pour comparer retenue et caution, de quelle donnée a-t-on besoin ?**
**De deux taux, et c'est tout.** La durée de la garantie et le montant immobilisé figurent des deux
côtés et se simplifient. C'est utile, parce que la durée est ⏸.

**5. Le DOE est-il un sujet de fin de chantier ?**
**Non**, c'est un sujet de chantier. Reconstitué après coup il coûte
{{reception.doe.rapport_des_heures::n1}} fois plus d'heures, et les deux tiers de son surcoût ne
sont pas des heures : c'est le décompte définitif qui attend.

**6. Qui garde l'ouvrage entre la fin des travaux et la réception ?**
**L'entreprise**, jusqu'à la date écrite du transfert. C'est la période où les protections
disparaissent et où personne ne se sent responsable — et c'est pour cela qu'elle se prépare comme
une phase de travaux, avec un nom et une date.

:::memo
## Fiche mémo — réception, DOE, garanties

**Les deux phrases du module**

> La réception transfère un risque, et chaque jour qui la retarde a un prix.
> Le nombre de réserves n'entre jamais dans la décision de réceptionner.

**La formule qui se lit dans un CPS**

$$ j_{\text{bascule}} = \frac{\text{plafond en \%} \times 10}{\text{pénalité en ‰}} \quad \text{jours calendaires, sans le montant du marché} $$

**Les chiffres de ce chantier**

| | |
|---|---:|
| Un jour de non-réception | **{{reception.cout_d_un_jour.cout_avant_le_plafond_MAD_par_jour_ouvre::n0}} MAD** |
| Après le plafond | {{reception.cout_d_un_jour.cout_apres_le_plafond_MAD_par_jour_ouvre::n0}} MAD — ×{{reception.cout_d_un_jour.rapport_des_deux_regimes::n1}} moins |
| Jour de bascule | {{reception.cout_d_un_jour.jour_de_bascule_calendaire::n0}} j calendaires ({{reception.cout_d_un_jour.jour_de_bascule_bornes_calendaires.0::n0}} à {{reception.cout_d_un_jour.jour_de_bascule_bornes_calendaires.1::n0}}) |
| Opérations préalables | {{reception.operations_prealables.duree_totale_j}} j, dont {{reception.operations_prealables.etapes.3.duree_j}} j d'essais de systèmes |
| Ce que le planning en prévoit | {{reception.confrontation_au_planning.duree_prevue_par_le_planning_j::n0}} j pour {{reception.confrontation_au_planning.duree_demandee_par_la_sequence_j::n0}} demandés — **{{reception.confrontation_au_planning.decalage_mesure_de_la_fin_j::n0}} j de fin** |
| Réserves | {{reception.reserves.nb_total}} dont **{{reception.reserves.nb_bloquantes}} bloquantes** · les confondre coûte {{reception.reserves.cout_de_la_confusion_MAD::n0}} MAD |
| Retenue immobilisée | {{reception.portage.retenue_immobilisee_MAD::n0}} MAD · {{reception.portage.cout_de_la_retenue_MAD_par_mois::n0}} MAD/mois contre {{reception.portage.cout_de_la_caution_MAD_par_mois::n0}} en caution |
| DOE reconstitué | {{reception.doe.cout_total_du_retard_de_DOE_MAD::n0}} MAD, dont {{reception.doe.cout_de_portage_MAD::n0}} d'argent qui attend |

**Les cinq réflexes**

1. Qualifier les réserves, ne jamais les compter.
2. Lire la pénalité ET son plafond, et calculer le jour de bascule avant de signer.
3. Mettre les opérations préalables au planning, avec leur durée.
4. Exiger les documents du DOE **quand le sous-traitant est encore là**.
5. Nommer un responsable de la garde de l'ouvrage, avec une date de transfert écrite.
6. Décomposer la ligne « Réception » du planning : la moitié de sa durée n'appartient pas à l'entreprise.

**⏸ Ce qui reste fermé sans les documents** — durées des garanties (parfait achèvement, bon
fonctionnement, décennale), délai de levée des réserves, conditions d'une réception tacite, contenu
obligatoire du DOE, délai de paiement du décompte définitif. Le module donne le mécanisme et sa
conséquence financière, jamais la durée.
:::
