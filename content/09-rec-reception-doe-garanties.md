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
calcule presque rien lui-même.** Les frais de durée et les pénalités viennent de D1, la date et le
réseau de D2, la retenue de garantie de la trésorerie de D1. Ce module les lit et en tire ce
qu'aucun d'eux ne pouvait voir seul.

Cinq résultats, tous **non normatifs**, c'est-à-dire qu'aucun ne dépend d'un texte :

1. **Un jour de non-réception n'a pas un prix, il en a deux.** Les pénalités ne courent qu'au-delà
   du terme contractuel, et elles cessent de croître au plafond : un jour coûte
   {{reception.cout_d_un_jour.cout_hors_penalites_MAD_par_jour_ouvre::k}} MAD avant le terme,
   {{reception.cout_d_un_jour.cout_sous_penalites_MAD_par_jour_ouvre::k}} entre le terme et le
   plafond, et de nouveau {{reception.cout_d_un_jour.cout_hors_penalites_MAD_par_jour_ouvre::k}}
   après. Ce n'est pas une courbe croissante, c'est une **fenêtre de cherté**.
2. **Le jour de bascule ne dépend pas du montant du marché** : le plafond en pour-cent divisé par
   la pénalité en pour-mille, et rien d'autre.
3. **L'arbitrage entre retenue de garantie et caution bancaire ne dépend pas de la durée de la
   garantie** — qui est pourtant la première chose qu'on cherche, et qui est ⏸. La durée se
   simplifie.
4. **Une liste de réserves ne se hiérarchise pas par son volume mais par son délai le plus long.**
   Les {{reception.reserves.nb_bloquantes}} réserves bloquantes de ce chantier représentent moins
   d'une journée d'atelier et {{reception.reserves.levee_des_bloquantes.duree_j::n0}} jours de
   calendrier, parce que l'une d'elles attend une pièce.
5. **Le DOE se constitue pendant le chantier.** Reconstitué après coup, il coûte
   {{reception.doe.rapport_des_heures::n1}} fois plus d'heures de cadre, et il bloque le décompte
   définitif pendant qu'on le reconstitue.

Ce qu'il ne fait pas : citer la durée d'une garantie, le délai de levée des réserves, les conditions
d'une réception tacite, le contenu obligatoire du DOE, le délai de paiement du décompte définitif —
**ni les effets juridiques de la réception**. Toutes ces règles sont réglementaires ou propres au
marché, et elles restent **⏸**. Le module donne le **mécanisme** et sa **conséquence financière**.

:::encart {"genre":"attente","titre":"Ce module n'est pas un cours de droit, et la nuance n'est pas une précaution de style"}
Les mots « réception », « réserve », « garantie », « décompte définitif » ont un sens juridique
précis qui dépend du droit applicable et du marché — et ce sens, ici, n'est pas cité. Quand ce
module écrit que la réception « arrête les frais de durée » ou « transfère la garde de l'ouvrage »,
il décrit **ce que le contrat organise d'ordinaire**, et chacune de ces affirmations est une
question à poser au CPS : **⏸**.

Ce qui est décrit sans réserve, en revanche, c'est la **fonction** que chaque mécanisme remplit et
ce qu'il coûte par jour. Un chef de projet suivi qui connaît le coût d'un jour de non-réception lit
son CPS autrement : il sait quelles clauses chercher en premier.
:::

## S2 · L'idée centrale : la réception transfère un risque, et il a deux prix

Tant que la réception n'est pas prononcée, l'entreprise porte les frais de durée de son
installation, la garde de l'ouvrage, le risque qu'il arrive quelque chose à un ouvrage terminé que
personne n'occupe encore — et, **si le terme contractuel est dépassé**, les pénalités de retard. Le
jour où la réception est prononcée, ce que le contrat a prévu d'arrêter s'arrête (⏸). C'est la seule
date du chantier qui change la nature des obligations, et pas seulement leur montant.

D'où la question que ce module pose : **combien coûte un jour de plus avant cette date ?** Et la
réponse commence par une autre question, que presque personne ne pose : **sommes-nous en retard ?**

| Période | Régime | Coût d'un jour ouvré |
|---|---|---:|
| {{reception.cout_d_un_jour.les_trois_periodes.0.periode}} | {{reception.cout_d_un_jour.les_trois_periodes.0.regime}} | **{{reception.cout_d_un_jour.les_trois_periodes.0.cout_MAD_par_jour_ouvre::k}} MAD** |
| {{reception.cout_d_un_jour.les_trois_periodes.1.periode}} | {{reception.cout_d_un_jour.les_trois_periodes.1.regime}} | **{{reception.cout_d_un_jour.les_trois_periodes.1.cout_MAD_par_jour_ouvre::k}} MAD** · bornes {{reception.cout_d_un_jour.cout_sous_penalites_bornes_MAD.0::k}} à {{reception.cout_d_un_jour.cout_sous_penalites_bornes_MAD.1::k}} |
| {{reception.cout_d_un_jour.les_trois_periodes.2.periode}} | {{reception.cout_d_un_jour.les_trois_periodes.2.regime}} | **{{reception.cout_d_un_jour.les_trois_periodes.2.cout_MAD_par_jour_ouvre::k}} MAD** |

{{reception.cout_d_un_jour.lecture}}

:::encart {"genre":"piege","titre":"La condition que la première version de ce module ne posait pas"}
{{reception.cout_d_un_jour._la_condition_qui_manquait}}

Elle n'a été trouvée ni par les tests du module, ni par les seize contrôles de la chaîne : **tous
étaient verts, et l'arithmétique était juste.** C'est la CONDITION d'emploi d'une grandeur héritée
qui n'était pas écrite — le module D1 publie un coût de **retard**, indexé par un nombre de jours
de retard, et ce module en avait fait un coût de non-réception. Il n'existe aucun test qui attrape
cela ; il faut relire le nom de la grandeur qu'on emprunte.
:::

| | |
|---|---:|
| Montant du marché | {{reception.cout_d_un_jour.marche_MAD::k}} MAD |
| Frais de durée, par jour ouvré | {{reception.cout_d_un_jour.frais_de_duree_MAD_par_jour_ouvre::k}} MAD |
| Pénalités, par jour ouvré | {{reception.cout_d_un_jour.penalites_MAD_par_jour_ouvre::k}} MAD |
| Plafond des pénalités | {{reception.cout_d_un_jour.plafond_des_penalites_MAD::k}} MAD |
| **Rapport des deux régimes** | **×{{reception.cout_d_un_jour.rapport_des_deux_regimes::n1}}** · bornes {{reception.cout_d_un_jour.rapport_bornes.0::n1}} à {{reception.cout_d_un_jour.rapport_bornes.1::n1}} |

**Aucun de ces deux nombres n'est calculé ici.** Les frais de durée et la pénalité journalière sont
lus dans la sortie du module D1. Ce que D1 ne cherche pas, et que ce module trouve, c'est le **jour
où le plafond est atteint** — et ce jour-là change tout.

:::encart {"genre":"piege","titre":"Le piège de calendrier, hérité de D1 et conservé tel quel"}
Les pénalités se comptent en jours **calendaires** et les frais de durée en jours **ouvrés**. Un
jour ouvré de retard porte donc
{{prix.bordereau.frais_de_duree.conversion.calendaires_par_jour_ouvre::n2}} jour de pénalité. Les
confondre sous-estime la pénalité d'un tiers — c'est le module D1 qui l'a trouvé, et ce module s'en
sert sans le refaire.

C'est aussi pourquoi le jour de bascule se publie **dans les deux calendriers** :
{{reception.cout_d_un_jour.jour_de_bascule_ouvre::n1}} jours ouvrés,
{{reception.cout_d_un_jour.jour_de_bascule_calendaire::n0}} jours calendaires. Annoncer l'un pour
l'autre dans une réunion est une erreur de
**{{reception.cout_d_un_jour.ecart_des_deux_calendriers_j::n0}} jours**.
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

:::figure {"fn":"diagramme","args":"reception.figures.cout_cumule","titre":"Le coût cumulé d'un retard, compté depuis le terme contractuel","num":1,"large":true,"options":{"unite":"MMAD","nom":"coût cumulé","depuisZero":true,"axeX":true,"axeY":true,"uniteX":"jours ouvrés APRÈS le terme contractuel","marqueur":{"$":"reception.figures.marqueur_bascule"}},"voir":["L'origine de l'axe n'est pas la fin des travaux : c'est le terme du marché. À gauche de l'origine, la courbe monterait de {{reception.cout_d_un_jour.cout_hors_penalites_MAD_par_jour_ouvre::k}} MAD par jour — le chantier coûte avant d'être en retard, mais huit fois moins.","La courbe est une droite tant que les pénalités courent, puis une autre droite, bien plus plate. La cassure est au {{reception.cout_d_un_jour.jour_de_bascule_ouvre::n1}}ᵉ jour ouvré — {{reception.cout_d_un_jour.jour_de_bascule_calendaire::n0}}ᵉ jour calendaire.","Avant la cassure, la pente est de {{reception.courbe_du_cout.pente_avant_MAD_par_jour::k}} MAD par jour. Après, {{reception.courbe_du_cout.pente_apres_MAD_par_jour::k}} : les frais de durée seuls, c'est-à-dire la même pente qu'avant le terme."],"erreur":"Lire la partie plate comme une bonne nouvelle. Pour l'entreprise, elle signifie que la pression contractuelle a disparu et que le maître d'ouvrage n'a plus que des moyens brutaux ; pour le maître d'ouvrage, qu'il a laissé son seul levier s'épuiser sans agir."}
:::

{{reception.cout_d_un_jour._ce_que_le_changement_de_regime_veut_dire}}

**Et ce qui n'est pas sur ce graphique.** {{reception.cout_d_un_jour._ce_qui_n_est_pas_chiffre}}

## S3 · Principes

### a. Les opérations préalables sont une tâche du planning, et la moitié ne vous appartient pas

Entre « les travaux sont finis » et « la réception est prononcée », il se passe des choses, elles
prennent du temps, et ce temps est au prix du paragraphe précédent. Les durées ci-dessous sont en
**{{reception.operations_prealables.unite}}**, comme tout le planning de ce cours.

| | Étape | Qui | Durée | Bornes | Portée par | Fin |
|---:|---|---|---:|---:|:-:|---:|
| 1 | {{reception.operations_prealables.etapes.0.etape}} | {{reception.operations_prealables.etapes.0.qui}} | {{reception.operations_prealables.etapes.0.duree_j::n0}} j | décision | {{reception.operations_prealables.etapes.0.porte_par}} | j+{{reception.operations_prealables.etapes.0.fin_j::n0}} |
| 2 | {{reception.operations_prealables.etapes.1.etape}} | *{{reception.operations_prealables.etapes.1.qui}}* | {{reception.operations_prealables.etapes.1.duree_j::n0}} j | {{reception.operations_prealables.etapes.1.duree_bornes_j.0::n0}} à {{reception.operations_prealables.etapes.1.duree_bornes_j.1::n0}} | {{reception.operations_prealables.etapes.1.porte_par}} | j+{{reception.operations_prealables.etapes.1.fin_j::n0}} |
| 3 | {{reception.operations_prealables.etapes.2.etape}} | {{reception.operations_prealables.etapes.2.qui}} | {{reception.operations_prealables.etapes.2.duree_j::n0}} j | décision | {{reception.operations_prealables.etapes.2.porte_par}} | j+{{reception.operations_prealables.etapes.2.fin_j::n0}} |
| 4 | **{{reception.operations_prealables.etapes.3.etape}}** | *{{reception.operations_prealables.etapes.3.qui}}* | **{{reception.operations_prealables.etapes.3.duree_j::n0}} j** | {{reception.operations_prealables.etapes.3.duree_bornes_j.0::n0}} à {{reception.operations_prealables.etapes.3.duree_bornes_j.1::n0}} | {{reception.operations_prealables.etapes.3.porte_par}} | j+{{reception.operations_prealables.etapes.3.fin_j::n0}} |
| 5 | {{reception.operations_prealables.etapes.4.etape}} | {{reception.operations_prealables.etapes.4.qui}} | {{reception.operations_prealables.etapes.4.duree_j::n0}} j | décision | {{reception.operations_prealables.etapes.4.porte_par}} | j+{{reception.operations_prealables.etapes.4.fin_j::n0}} |
| 6 | {{reception.operations_prealables.etapes.5.etape}} | *{{reception.operations_prealables.etapes.5.qui}}* | {{reception.operations_prealables.etapes.5.duree_j::n0}} j | {{reception.operations_prealables.etapes.5.duree_bornes_j.0::n0}} à {{reception.operations_prealables.etapes.5.duree_bornes_j.1::n0}} | {{reception.operations_prealables.etapes.5.porte_par}} | **j+{{reception.operations_prealables.etapes.5.fin_j::n0}}** |

{{reception.operations_prealables.note}}

:::encart {"genre":"voir","titre":"Une durée qu'on ne tient pas n'est pas une décision"}
{{reception.operations_prealables._a_qui_appartiennent_ces_jours}}

C'est pourquoi la colonne « bornes » est vide sur trois lignes et pleine sur les trois autres. Les
étapes en *italique* dans le tableau appartiennent à un tiers : on ne décide pas la durée de la
visite de la maîtrise d'œuvre, ni celle des essais de l'exploitant, ni le temps que le maître
d'ouvrage met à signer. **Toute l'étendue des bornes vient de ces trois lignes** — de
{{reception.operations_prealables.duree_bornes_j.0::n0}} à
{{reception.operations_prealables.duree_bornes_j.1::n0}} jours ouvrés pour la séquence entière.
:::

{{reception.operations_prealables._l_essai_qui_commande}}

**Les six pièges, un par étape** — ce sont eux qui font la différence entre
{{reception.operations_prealables.duree_totale_j::n0}} jours et quatre mois :

1. {{reception.operations_prealables.etapes.0.piege}} ;
2. {{reception.operations_prealables.etapes.1.piege}} ;
3. {{reception.operations_prealables.etapes.2.piege}} ;
4. {{reception.operations_prealables.etapes.3.piege}} ;
5. {{reception.operations_prealables.etapes.4.piege}} ;
6. {{reception.operations_prealables.etapes.5.piege}}.

### b. Les réserves : deux familles, une seule bloque — et un délai qui commande

{{reception.reserves.la_regle}}

Ce qui est **interdit**, et qui est la faute la plus répandue de la fin de chantier : compter les
lignes. « Quatre-vingt-dix réserves, on ne peut pas réceptionner » n'est pas un raisonnement, c'est
une impression.

Et une seconde règle, qui ne se voit qu'en calculant :

{{reception.reserves.le_delai_de_tiers}}

### c. La retenue de garantie immobilise de l'argent, et cet argent a un prix

La retenue de garantie est prélevée sur chaque situation et conservée jusqu'à une date que le
marché fixe (**⏸**). Elle n'est pas perdue : elle est **immobilisée**. Et de l'argent immobilisé
coûte le taux auquel l'entreprise se finance.

Une caution bancaire peut la remplacer. Elle coûte une commission. Comparer les deux semble demander
la **durée de l'immobilisation** — qui est ⏸. On va voir au § S4c que non.

### d. Le DOE n'est pas un dossier, c'est une condition de paiement

Le dossier des ouvrages exécutés conditionne le décompte définitif : tant qu'il est incomplet, le
**solde des travaux** ne se paie pas. À ne pas confondre avec la retenue de garantie, qui est
immobilisée par la clause de garantie, que le dossier soit remis ou non — deux montants cohabitent
à la fin d'un chantier, et seul le premier dépend du DOE.

Son contenu réglementaire est **⏸**. Son critère pratique, lui, ne dépend d'aucun texte :

> {{gare.reception.doe._ce_qu_il_doit_contenir}}

## S4 · L'étude de cas : la fin du chantier de la gare

### a. Le planning prévoit-il la réception qu'il annonce ?

Le § S2 a donné le prix d'un jour. Le reste de ce module consiste à compter les jours — et à
montrer qu'on les dépense presque toujours sur les mauvaises décisions. La première occasion se
présente avant même la fin des travaux, dans le planning.

| Tâche du planning | Prévu | Étapes qu'elle porte | Demandé | Bornes | Écart |
|---|---:|---|---:|---:|---:|
| {{reception.confrontation_au_planning.lignes.0.tache}} · {{reception.confrontation_au_planning.lignes.0.nom}} | {{reception.confrontation_au_planning.lignes.0.duree_prevue_j::n0}} j | essais de fonctionnement, mise en service | **{{reception.confrontation_au_planning.lignes.0.besoin_j::n0}} j** | {{reception.confrontation_au_planning.lignes.0.besoin_bornes_j.0::n0}} à {{reception.confrontation_au_planning.lignes.0.besoin_bornes_j.1::n0}} | {{reception.confrontation_au_planning.lignes.0.ecart_j::n0}} j |
| {{reception.confrontation_au_planning.lignes.1.tache}} · {{reception.confrontation_au_planning.lignes.1.nom}} | {{reception.confrontation_au_planning.lignes.1.duree_prevue_j::n0}} j | avis, visite, remise du DOE, procès-verbal | **{{reception.confrontation_au_planning.lignes.1.besoin_j::n0}} j** | {{reception.confrontation_au_planning.lignes.1.besoin_bornes_j.0::n0}} à {{reception.confrontation_au_planning.lignes.1.besoin_bornes_j.1::n0}} | {{reception.confrontation_au_planning.lignes.1.ecart_j::n0}} j |
| **Total** | | | | | **{{reception.confrontation_au_planning.ecart_total_j::n0}} j** |

| | |
|---|---:|
| **Décalage de la fin, mesuré en rejouant le réseau** | **{{reception.confrontation_au_planning.decalage_mesure_de_la_fin_j::n1}} j** |
| Bornes, mesurées elles aussi | {{reception.confrontation_au_planning.decalage_bornes_j.0::n0}} à {{reception.confrontation_au_planning.decalage_bornes_j.1::n0}} j |
| Au prix d'un jour, hors pénalités | {{reception.confrontation_au_planning.cout_hors_penalites_MAD::k}} MAD |
| Au prix d'un jour, sous pénalités | {{reception.confrontation_au_planning.cout_sous_penalites_MAD::k}} MAD |

{{reception.confrontation_au_planning.lecture}}

:::encart {"genre":"piege","titre":"Le double compte que cette version a corrigé"}
{{reception.confrontation_au_planning._le_double_compte_evite}}
:::

:::encart {"genre":"attente","titre":"Ce que cette comparaison est, et ce qu'elle n'est pas"}
{{reception.confrontation_au_planning._ce_que_cette_comparaison_est}}
:::

{{reception.confrontation_au_planning._quoi_en_faire}}

### b. Les réserves de la gare : combien bloquent, et ce que coûte de se tromper

La liste rendue à la visite compte {{reception.reserves.nb_total}} lignes.
{{reception.reserves.nb_bloquantes}} d'entre elles empêchent l'usage ou mettent en cause la
sécurité — soit {{reception.reserves.part_bloquante_pct::n1}} %.

| Famille | Exemple | Nombre | Bloque | Atelier | Délai d'un tiers |
|---|---|---:|:-:|---:|---:|
| {{reception.reserves.lignes.0.famille}} | {{reception.reserves.lignes.0.exemple}} | {{reception.reserves.lignes.0.nombre}} | non | {{reception.reserves.lignes.0.jours_d_atelier::n1}} j | — |
| {{reception.reserves.lignes.1.famille}} | {{reception.reserves.lignes.1.exemple}} | {{reception.reserves.lignes.1.nombre}} | non | {{reception.reserves.lignes.1.jours_d_atelier::n1}} j | {{reception.reserves.lignes.1.delai_de_tiers_j::n0}} j |
| {{reception.reserves.lignes.2.famille}} | {{reception.reserves.lignes.2.exemple}} | {{reception.reserves.lignes.2.nombre}} | non | {{reception.reserves.lignes.2.jours_d_atelier::n1}} j | — |
| **{{reception.reserves.lignes.3.famille}}** | {{reception.reserves.lignes.3.exemple}} | **{{reception.reserves.lignes.3.nombre}}** | **OUI** | {{reception.reserves.lignes.3.jours_d_atelier::n1}} j | {{reception.reserves.lignes.3.delai_de_tiers_j::n0}} j |
| **{{reception.reserves.lignes.4.famille}}** | {{reception.reserves.lignes.4.exemple}} | **{{reception.reserves.lignes.4.nombre}}** | **OUI** | {{reception.reserves.lignes.4.jours_d_atelier::n1}} j | {{reception.reserves.lignes.4.delai_de_tiers_j::n0}} j |
| **Total** | | **{{reception.reserves.nb_total}}** | **{{reception.reserves.nb_bloquantes}}** | **{{reception.reserves.levee_de_toutes.jours_d_atelier::n1}} j** | |

Le temps d'atelier vient de ⟦V3|heures-homme de levée d'une réserve, intervention et reconstat compris|6 h·homme|h·homme|2 à 16|2026|l'unité compte : six heures-homme à six compagnons ne font pas six heures de délai, et la durée de levée se calcule sur la capacité de l'atelier⟧ par réserve et d'une
capacité de {{reception.reserves.capacite_h_homme_par_jour::n0}} heures-homme par jour
({{reception.reserves.effectif_de_levee}} compagnons). Le délai d'un tiers, lui, ne se raccourcit
avec aucun effectif.

| | Heures-homme | Atelier | Délai le plus long | **Durée** | Commandée par |
|---|---:|---:|---:|---:|---|
| Les {{reception.reserves.nb_bloquantes}} bloquantes seules | {{reception.reserves.levee_des_bloquantes.heures::n0}} | {{reception.reserves.levee_des_bloquantes.jours_d_atelier::n2}} j | {{reception.reserves.levee_des_bloquantes.delai_de_tiers_le_plus_long_j::n0}} j | **{{reception.reserves.levee_des_bloquantes.duree_j::n1}} j** | {{reception.reserves.levee_des_bloquantes.commande_par}} |
| Toutes les réserves | {{reception.reserves.levee_de_toutes.heures::n0}} | {{reception.reserves.levee_de_toutes.jours_d_atelier::n2}} j | {{reception.reserves.levee_de_toutes.delai_de_tiers_le_plus_long_j::n0}} j | **{{reception.reserves.levee_de_toutes.duree_j::n1}} j** | {{reception.reserves.levee_de_toutes.commande_par}} |

{{reception.reserves.lecture}}

{{reception.reserves._ce_qui_commande_la_duree}}

:::figure {"fn":"barres","args":"reception.figures.reserves","titre":"Les réserves de la gare, par famille — et celles qui empêchent la réception","num":2,"large":true,"options":{"unite":"nombre de réserves","legende_alerte":"empêche l'usage ou met en cause la sécurité"},"voir":["Les deux familles en rouge sont celles qui bloquent : {{reception.reserves.nb_bloquantes}} lignes sur {{reception.reserves.nb_total}}, soit {{reception.reserves.part_bloquante_pct::n1}} %. Ce sont aussi les deux plus courtes.","La longueur des barres n'entre pas dans la décision de réceptionner. Elle entre dans l'organisation de la levée, et même là elle ne décide pas : la famille de {{reception.reserves.lignes.4.nombre}} lignes attend {{reception.reserves.lignes.4.delai_de_tiers_j::n0}} jours une pièce que personne n'accélère.","Une réserve de sécurité isolée dans une liste de {{reception.reserves.lignes.0.nombre}} lignes d'aspect reste une réserve de sécurité. Le classement se fait ligne à ligne."],"erreur":"Lire ce graphique comme une mesure de l'avancement de la fin de chantier. {{reception.reserves.lignes.0.nombre}} retouches de peinture ne retardent pas la mise en service d'une gare ; un escalator à l'arrêt, si."}
:::

{{reception.reserves._le_prix_de_la_confusion}}

| | |
|---|---:|
| Jours de non-réception en plus | **{{reception.reserves.jours_de_non_reception_en_plus::n1}} j** · bornes {{reception.reserves.jours_en_plus_bornes.0::n1}} à {{reception.reserves.jours_en_plus_bornes.1::n1}} |
| Coût si le chantier est dans son délai | {{reception.reserves.cout_de_la_confusion_hors_penalites_MAD::k}} MAD |
| Coût s'il est déjà sous pénalités | **{{reception.reserves.cout_de_la_confusion_sous_penalites_MAD::k}} MAD** |
| Bornes, tous régimes et toutes hypothèses | {{reception.reserves.cout_de_la_confusion_bornes_MAD.0::k}} à {{reception.reserves.cout_de_la_confusion_bornes_MAD.1::k}} MAD |

:::encart {"genre":"piege","titre":"L'erreur symétrique est pire, et elle ne se voit pas"}
{{reception.reserves._et_dans_l_autre_sens}}
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
| Heures de cadre | {{reception.doe.heures_au_fil_de_l_eau}} h | {{reception.doe.heures_reconstitue}} h |
| Coût de ces heures | {{reception.doe.cout_au_fil_de_l_eau_MAD::k}} MAD | {{reception.doe.cout_reconstitue_MAD::k}} MAD |
| Surcoût en heures | — | {{reception.doe.surcout_en_heures_MAD::k}} MAD · bornes {{reception.doe.surcout_en_heures_bornes_MAD.0::k}} à {{reception.doe.surcout_en_heures_bornes_MAD.1::k}} |
| Solde des travaux bloqué | — | {{reception.doe.solde_bloque_MAD::k}} MAD pendant {{reception.doe.retard_du_solde_j}} j |
| Coût de portage du solde | — | {{reception.doe.cout_de_portage_MAD::k}} MAD · bornes {{reception.doe.cout_de_portage_bornes_MAD.0::k}} à {{reception.doe.cout_de_portage_bornes_MAD.1::k}} |
| **Surcoût total** | — | **{{reception.doe.cout_total_du_retard_de_DOE_MAD::k}} MAD** · bornes {{reception.doe.cout_total_bornes_MAD.0::k}} à {{reception.doe.cout_total_bornes_MAD.1::k}} |

Les deux volumes d'heures sont ⟦V3|heures de cadre pour tenir le DOE au fil de l'eau|80 h|h|40 à 160|2026|classer les documents à mesure qu'ils arrivent, et exiger le plan de récolement d'un lot quand il part⟧ et ⟦V3|heures de cadre pour reconstituer le même DOE après coup|320 h|h|160 à 600|2026|retrouver les sous-traitants partis, refaire relever ce qui ne l'a pas été, redemander des fiches à des fournisseurs qui ont changé de référence⟧ ; le solde bloqué vaut ⟦V3|solde des travaux restant au décompte définitif, en pour-cent du marché|4,0 %|%|1,5 à 10,0|2026|dernière situation, révisions de prix non encore réglées, travaux supplémentaires acceptés⟧ du marché, pendant ⟦V3|jours pendant lesquels le décompte définitif reste bloqué faute de DOE complet|60 j|j|20 à 180|2026|ce n'est pas une pénalité : c'est de l'argent dû, non payé, que l'entreprise porte⟧.

{{reception.doe.lecture}}

:::encart {"genre":"piege","titre":"Le DOE bloque le solde, pas la retenue — et la première version de ce module les a confondus"}
{{reception.doe._ce_que_le_solde_contient}}
:::

:::figure {"fn":"cascade","args":"reception.figures.doe","titre":"D'où vient le surcoût d'un DOE reconstitué","num":3,"large":true,"options":{"unite":"milliers de MAD"},"voir":["La première barre est le surcoût en heures de cadre : retrouver, refaire relever, redemander. C'est la seule partie qui ressemble à du travail.","La seconde est le solde des travaux qui attend, et c'est la plus grosse : {{reception.doe.part_du_portage_dans_le_surcout_pct::n0}} % du surcoût. Elle ne figure sur aucun devis et sur aucun budget de lot.","Le total de la cascade est exactement le « surcoût total » du tableau ci-dessus : {{reception.doe.cout_total_du_retard_de_DOE_MAD::k}} MAD. Le coût d'un DOE correctement tenu, lui, n'est pas sur cette figure — ce n'est pas un surcoût, c'est le prix normal du dossier."],"erreur":"Juger le DOE sur son coût en heures. La moitié du surcoût n'est pas une heure : c'est le solde des travaux qui ne se paie pas, et il ne se voit nulle part dans les comptes du chantier."}
:::

{{reception.doe._pourquoi_c_est_sous_estime}}

**Et ce que les bornes disent.** {{reception.doe._bornes}}

:::encart {"genre":"piege","titre":"La base de calcul des intérêts est une clause, pas une constante"}
{{reception.doe._la_base_est_une_clause}}
:::

## S4g · Sécurité : qui garde l'ouvrage entre la fin des travaux et la réception ?

C'est la période la plus mal couverte d'un chantier, et elle ne figure dans aucun plan de
prévention : les travaux sont finis, les équipes sont parties sur l'opération suivante, la base-vie
se démonte, et l'ouvrage — une gare, c'est-à-dire un bâtiment ouvert sur l'espace public et sur une
voie exploitée — est terminé, accessible, et gardienné par personne en particulier.

**Ce qui se passe réellement dans ces semaines-là** : les clôtures se relâchent parce que plus
personne n'a de raison de les refermer ; les protections provisoires disparaissent avec les équipes
qui les avaient posées ; les trappes et les regards restent ouverts après le dernier essai ;
l'éclairage provisoire est déposé avant que le définitif ne soit réceptionné ; et des gens entrent.

**Quatre dispositions**, dont aucune ne coûte cher au regard du prix d'un jour de non-réception :

1. **Un responsable nommé de la garde de l'ouvrage**, et une date de transfert écrite. Pas « la
   réception » en général : une date, un nom, un procès-verbal. **Qui porte cette garde, et
   jusqu'à quand, se lit dans le marché et dans le droit applicable (⏸)** — ce qui ne se discute
   pas, c'est qu'il faut l'avoir écrit avant d'en avoir besoin.
2. **Les protections se déposent APRÈS la réception, pas après les travaux.** C'est l'inverse de ce
   que fait la pression de repli, et c'est le même mécanisme que le module C7 décrit pour les
   protections périphériques : la parade la plus efficace est celle qui s'installe avant et se
   dépose après.
3. **Une visite de fermeture, avec une liste.** Trappes, regards, gaines techniques, accès en
   toiture, locaux électriques, quais. La même liste que celle des essais, relue dans l'autre sens.
4. **Les installations de sécurité restent-elles en service ?** C'est le point qu'on oublie, et il
   est particulier à cette période : la détection incendie, le désenfumage et l'éclairage de
   sécurité viennent d'être essayés, ils fonctionnent, et **personne n'en a encore la charge** —
   l'entreprise a replié, l'exploitant n'a pas pris l'ouvrage, et aucun contrat de maintenance n'a
   commencé. Un défaut survenu pendant ces semaines-là n'est vu par personne. Il faut donc nommer
   qui les surveille, et le faire avant de démobiliser.

**Et le cas particulier d'une gare** : la voie reste exploitée pendant toute cette période. Un
ouvrage accessible à quelques mètres d'une voie circulée, sans gardiennage, n'est pas un problème
de chantier — c'est un problème d'exploitation ferroviaire, et il se traite avec l'exploitant.

## S4h · La double lecture : entreprise et maîtrise d'œuvre

| | **Côté entreprise** | **Côté maîtrise d'œuvre** |
|---|---|---|
| **L'avis de fin de travaux** | il déclenche le compte à rebours : on ne l'envoie pas avant d'être prêt, et on ne l'envoie pas tard non plus — chaque jour coûte de {{reception.cout_d_un_jour.cout_hors_penalites_MAD_par_jour_ouvre::k}} à {{reception.cout_d_un_jour.cout_sous_penalites_MAD_par_jour_ouvre::k}} MAD selon qu'on est ou non en retard | il déclenche son obligation de convoquer la visite. Un avis reçu et non traité engage sa responsabilité, et la date qui compte est celle de la réception de l'avis, pas celle de la visite |
| **Les réserves** | une liste de travaux à faire, avec un coût et un délai — et une négociation sur ce qui relève du marché | un **constat**, écrit, daté, sur place. Elle ne se lève pas sur une photo. Et elle engage : une réserve oubliée est une réserve non opposable |
| **La qualification d'une réserve** | elle décide de la date de réception, donc de la trésorerie | elle décide de ce qu'elle vise. Et sur l'usage, **ni l'une ni l'autre n'a le dernier mot** : c'est l'exploitant qui dit si une gare s'ouvre avec un escalator sur deux |
| **La décision de réceptionner** | elle arrête ce que le contrat prévoit d'arrêter (⏸) et libère la suite | elle n'est pas la sienne : elle **propose**, le maître d'ouvrage décide. Proposer une réception sur un ouvrage dangereux l'engage lourdement |
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
| Chiffrer un jour de fin de chantier **sans demander si l'on est en retard** | un seul prix circule dans toutes les réunions | un facteur {{reception.cout_d_un_jour.rapport_des_deux_regimes::n1}} dans un sens ou dans l'autre — c'est l'erreur que la première version de ce module a commise |
| Attendre une réception **sans réserve** | « on finit les détails et on réceptionne » | de {{reception.cout_d_un_jour.cout_hors_penalites_MAD_par_jour_ouvre::k}} à {{reception.cout_d_un_jour.cout_sous_penalites_MAD_par_jour_ouvre::k}} MAD par jour d'attente, pour des retouches de peinture |
| Compter les réserves au lieu de les **qualifier** | « {{reception.reserves.lignes.0.nombre}} lignes, c'est trop » | jusqu'à {{reception.reserves.cout_de_la_confusion_sous_penalites_MAD::k}} MAD sur ce chantier |
| Croire que **plus de monde** lève les réserves plus vite | l'effectif de levée est doublé | rien : {{reception.reserves.levee_des_bloquantes.duree_j::n0}} jours d'attente d'une pièce que personne n'accélère |
| Classer une réserve de **sécurité** en finition | elle est seule de sa famille dans une longue liste | un ouvrage reçu avec un garde-corps non conforme, et la responsabilité qui a changé de mains |
| Oublier les **opérations préalables** au planning | le planning finit au dernier coup de peinture | {{reception.operations_prealables.duree_totale_j::n0}} jours ouvrés entre la fin des travaux et la décision |
| Porter une tâche « Réception » **non décomposée** | une ligne de {{reception.confrontation_au_planning.lignes.1.duree_prevue_j::n0}} jours en fin de Gantt | il en faut {{reception.confrontation_au_planning.lignes.1.besoin_j::n0}} : avec les essais, **{{reception.confrontation_au_planning.decalage_mesure_de_la_fin_j::n0}} jours de fin** mesurés |
| Lancer les **essais de systèmes** en dernier | ils révèlent des défauts d'interface entre lots | l'étape la plus longue ({{reception.operations_prealables.etapes.3.duree_j::n0}} j, borne haute {{reception.operations_prealables.etapes.3.duree_bornes_j.1::n0}}) et celle qu'on ne maîtrise pas |
| Reconstituer le **DOE** après coup | personne ne l'a réclamé pendant le chantier | {{reception.doe.cout_total_du_retard_de_DOE_MAD::k}} MAD, dont {{reception.doe.part_du_portage_dans_le_surcout_pct::n0}} % en argent dû qui attend |
| Imputer au DOE le portage de la **retenue** | le chiffre paraît plus gros, donc plus convaincant | une grandeur à la place d'une autre : la retenue est immobilisée que le dossier soit remis ou non |
| Ignorer le **plafond** des pénalités | on découvre tard que le levier a disparu | une stratégie construite sur un mécanisme qui s'arrête au {{reception.cout_d_un_jour.jour_de_bascule_calendaire::n0}}ᵉ jour calendaire |
| Confondre jours **ouvrés** et **calendaires** | la pénalité annoncée ne tombe pas juste | un tiers d'écart, et une date de bascule fausse de {{reception.cout_d_un_jour.ecart_des_deux_calendriers_j::n0}} jours |
| Laisser l'ouvrage **sans gardien** après les travaux | rien, jusqu'au jour où quelqu'un entre | les installations de sécurité ne sont surveillées par personne, et la garde n'a pas été transférée par écrit |
| Accepter une **caution** sans regarder la ligne de crédit | le calcul montre une économie | la ligne qui garantit ce chantier ne garantira pas la soumission du mois prochain |
| Prendre la **base 365** pour une constante | les intérêts tombent presque juste | 1,4 % d'écart, et une clause qu'on n'a pas lue |

## S6 · Exercices

:::exercice {"titre":"1 · Deux clauses, un jour de bascule","niveau":"application"}
Un CPS prévoit une pénalité de retard de **2 ‰ par jour** et un plafond de **5 % du montant du
marché**. Le marché vaut 240 millions de dirhams. Au bout de combien de jours la pénalité
plafonne-t-elle ? Et si le marché valait 24 millions ?

**Corrigé.** Le montant du marché ne sert à rien.

$$ j_{\text{bascule}} = \frac{5 \times 10}{2} = 25 \text{ jours} $$

**Dans les deux cas.** Le montant figure au numérateur du plafond (5 % de M) et au dénominateur de
la pénalité (2 ‰ de M par jour) : il se simplifie. Vingt-cinq jours, que le marché vaille 24 ou 240
millions.

**Et la question qui manque dans l'énoncé** : vingt-cinq jours de quel calendrier ? L'énoncé dit
« 2 ‰ par jour » sans préciser, et c'est exactement ce qu'un CPS fait. Si ce sont des jours
calendaires, cela fait environ
{{prix.bordereau.frais_de_duree.conversion.ouvres_par_jour_calendaire::n2}} × 25 ≈ 18 jours
ouvrés de chantier ; si ce sont des jours ouvrés, 25 jours ouvrés, soit plus d'un mois de
calendrier. **C'est la première question à poser**, avant même de calculer, et elle vaut un tiers
du résultat.

*Ce que l'exercice enseigne : ces deux lignes d'un CPS ne se lisent jamais séparément. « 2 ‰ par
jour » paraît sévère et « plafond 5 % » paraît protecteur ; ensemble, ils disent que la pénalité
cesse de croître au bout de vingt-cinq jours. Sur le marché de ce cours —
⟦V3|pénalité de retard, pour mille du montant du marché par jour|1,0 ‰|‰/j|0,5 à 2,0|2026|clause du CPS, à lire et non à supposer⟧ et
⟦V3|plafond des pénalités de retard, en pour-cent du marché|10 %|%|5 à 10|2026|clause du CPS, à lire et non à supposer⟧ — la bascule tombe au
{{reception.cout_d_un_jour.jour_de_bascule_calendaire::n0}}ᵉ jour calendaire. Quatre fois plus tard.*
:::

:::exercice {"titre":"2 · Réceptionner ou pas — cas ouvert","niveau":"cas_ouvert"}
Vendredi. La visite des opérations préalables est faite. Vous êtes chef de projet suivi côté
entreprise, **et le chantier est dans son délai contractuel**. L'exploitant veut ouvrir la gare dans
trois semaines. La liste des réserves compte {{reception.reserves.nb_total}} lignes, dont :

- un **escalator à l'arrêt**, en attente d'une pièce annoncée sous dix jours ;
- un **désenfumage non essayé** dans le hall, faute de créneau avec le lot technique ;
- {{reception.reserves.lignes.0.nombre}} retouches de peinture et calfeutrements ;
- les **plans de récolement** d'un lot manquent, le sous-traitant a quitté le chantier.

Le maître d'ouvrage vous demande ce qu'il doit faire. Que lui répondez-vous, et dans quel ordre
traitez-vous ces quatre points ?

**Corrigé — il n'y a pas une réponse, il y a une méthode.**

**0. D'abord, le prix du temps.** Le chantier est dans son délai : un jour de retard à
réceptionner coûte {{reception.cout_d_un_jour.cout_hors_penalites_MAD_par_jour_ouvre::k}} MAD de
frais de durée, et non {{reception.cout_d_un_jour.cout_sous_penalites_MAD_par_jour_ouvre::k}}. La
différence change le ton de la discussion, et c'est la première chose à vérifier avant de mettre un
chiffre sur la table. Si le chantier avait déjà dépassé son terme, tout ce qui suit coûterait
{{reception.cout_d_un_jour.rapport_des_deux_regimes::n1}} fois plus.

**1. Qualifier, pas compter.** Deux de ces quatre points empêchent l'usage ou mettent en cause la
sécurité : l'escalator et le désenfumage. Les deux autres non. La question n'est donc pas
« peut-on réceptionner avec {{reception.reserves.nb_total}} réserves ? » mais « peut-on
réceptionner avec un désenfumage non essayé ? ».

**2. Le désenfumage d'abord, et il n'est pas négociable.** Ce n'est pas une réserve, c'est un essai
manquant sur une installation de sécurité dans un bâtiment qui recevra du public. On cherche le
créneau dans la semaine, quitte à payer une intervention de nuit. Aucun calcul de coût n'entre dans
cette décision, et c'est le seul point du corrigé où le chiffre ne sert à rien.

**3. L'escalator : la règle dit non, et c'est l'exploitant qui peut dire oui.** La règle du § S3b
est binaire — une réserve qui empêche l'usage empêche la réception. Mais **la qualification est un
jugement**, et sur l'usage, c'est l'exploitant qui en est juge : lui seul peut dire qu'une gare
s'ouvre avec un escalator sur deux, avec une signalétique et un cheminement accessible maintenus.
S'il le dit **par écrit**, la réserve cesse d'empêcher l'usage et la réception se prononce avec
elle ; s'il ne le dit pas, on attend la pièce, et cela coûte
{{reception.reserves.levee_des_bloquantes.duree_j::n0}} jours. Ce qui serait faux, c'est de le
décider à sa place parce que le calendrier nous arrange. Noter au passage que la sécurité, elle, ne
se négocie avec personne : le point 2 n'est pas de même nature que celui-ci.

**4. Les retouches : réserves, et on réceptionne.** Elles n'empêchent rien. Les traiter comme
bloquantes ajouterait {{reception.reserves.jours_de_non_reception_en_plus::n1}} jours — pas les
{{reception.reserves.levee_de_toutes.duree_j::n1}} jours de la levée complète, car les bloquantes
prennent déjà {{reception.reserves.levee_des_bloquantes.duree_j::n0}} jours qu'on aurait attendus
de toute façon.

**5. Les plans de récolement : le vrai problème est ailleurs.** Ils ne bloquent pas la réception,
mais ils bloqueront le **décompte définitif**, et le sous-traitant est parti. C'est la seule des
quatre lignes qui coûte plus cher chaque semaine qui passe, et c'est celle dont personne ne parle
vendredi. À traiter lundi matin, pendant qu'on retrouve encore quelqu'un au téléphone.

*Ce que le cas enseigne : la liste des réserves hiérarchise mal. Elle mélange une obligation de
sécurité, un jugement d'exploitation, un travail de finition et un problème de paiement — quatre
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

1. Le chantier est-il **dans son délai** ? La réponse change le prix de chaque jour qui suit d'un
   facteur {{reception.cout_d_un_jour.rapport_des_deux_regimes::n1}}.
2. Les **essais de systèmes** sont-ils faits, constatés et signés — ou seulement programmés ?
3. Le **DOE** est-il remis, et son sommaire permet-il de trouver un ouvrage en deux minutes ?
4. La liste des réserves est-elle **qualifiée** (empêche l'usage : oui / non) et non seulement comptée ?
5. Pour chaque réserve bloquante : **qu'attend-elle**, et de qui ? C'est le délai le plus long qui
   fixe la date, pas le volume de travail.
6. Les **opérations préalables** sont-elles au planning, avec leur durée et leurs responsables ?
7. La **garde de l'ouvrage** a-t-elle un responsable nommé et une date de transfert écrite — et qui
   surveille les installations de sécurité d'ici là ?
8. A-t-on lu, dans le CPS, la **pénalité**, son **plafond** et leur **calendrier** ?
9. La **retenue de garantie** peut-elle être remplacée par une caution, et la banque suivra-t-elle ?

**Glossaire**

| Terme | Ce que c'est |
|---|---|
| **Opérations préalables** | les constats et essais qui précèdent la décision de réceptionner. Une tâche du planning, avec une durée, dont {{reception.operations_prealables.part_tenue_par_des_tiers_pct::n0}} % n'appartient pas à l'entreprise |
| **Réserve** | un écart constaté au moment de la réception. Deux familles seulement : elle empêche l'usage, ou non |
| **Réception** | la décision qui clôt les travaux. Ses conditions, ses effets juridiques et ce qu'elle transfère : **⏸** — ils se lisent dans le marché et dans le droit applicable |
| **Retenue de garantie** | part de chaque situation conservée par le maître d'ouvrage jusqu'à une date que le marché fixe (**⏸**). Immobilisée, pas perdue |
| **Caution de substitution** | garantie bancaire qui remplace la retenue. Coûte une commission, consomme une ligne de crédit |
| **DOE** | dossier des ouvrages exécutés. Son contenu réglementaire est **⏸** ; son critère pratique est qu'on y retrouve un ouvrage dix ans plus tard |
| **Plan de récolement** | ce qui a été **posé**, là où ça a été posé — et non ce qui avait été prévu |
| **Décompte définitif** | le dernier compte du marché. Il porte le **solde des travaux**, que le DOE bloque — à ne pas confondre avec la retenue de garantie |
| **Base de calcul des intérêts** | 365 ou 360 jours selon la convention de crédit. Une clause, pas une constante |

**Quiz**

**1. Un chantier a {{reception.reserves.nb_total}} réserves. Peut-on réceptionner ?**
**La question est mal posée.** Le nombre n'entre pas dans la décision. Seule compte la réponse à
« laquelle empêche l'usage ou met en cause la sécurité ? » — ici
{{reception.reserves.nb_bloquantes}} sur {{reception.reserves.nb_total}}.

**2. Le marché double. Le jour de bascule des pénalités change-t-il ?**
**Non.** Le montant est au numérateur du plafond et au dénominateur de la pénalité : il se simplifie.
Seules les deux clauses comptent.

**3. Un jour de non-réception coûte-t-il toujours la même chose ?**
**Non, et il y a deux prix, pas trois.** Avant le terme contractuel et après le plafond :
{{reception.cout_d_un_jour.cout_hors_penalites_MAD_par_jour_ouvre::k}} MAD, les frais de durée
seuls. Entre les deux : {{reception.cout_d_un_jour.cout_sous_penalites_MAD_par_jour_ouvre::k}} MAD.
La première question à poser est donc : **sommes-nous en retard ?**

**4. Doubler l'effectif de levée divise-t-il par deux le délai des réserves ?**
**Non**, pas tant qu'un tiers commande. Les {{reception.reserves.nb_bloquantes}} bloquantes de ce
chantier représentent {{reception.reserves.levee_des_bloquantes.jours_d_atelier::n2}} jour
d'atelier et {{reception.reserves.levee_des_bloquantes.duree_j::n0}} jours d'attente. C'est le
chemin critique d'un planning, appliqué à une liste de réserves.

**5. Pour comparer retenue et caution, de quelle donnée a-t-on besoin ?**
**De deux taux, et c'est tout.** La durée de l'immobilisation et le montant figurent des deux côtés
et se simplifient. C'est utile, parce que la durée est ⏸.

**6. Le DOE est-il un sujet de fin de chantier ?**
**Non**, c'est un sujet de chantier. Reconstitué après coup il coûte
{{reception.doe.rapport_des_heures::n1}} fois plus d'heures, et
{{reception.doe.part_du_portage_dans_le_surcout_pct::n0}} % de son surcoût ne sont pas des heures :
c'est le solde des travaux qui attend.

:::memo
## Fiche mémo — réception, DOE, garanties

**Les trois phrases du module**

> Avant de chiffrer un jour de fin de chantier : sommes-nous en retard ?
> Le nombre de réserves n'entre jamais dans la décision de réceptionner.
> Une liste se hiérarchise par son délai le plus long, pas par son volume.

**La formule qui se lit dans un CPS**

$$ j_{\text{bascule}} = \frac{\text{plafond en \%} \times 10}{\text{pénalité en ‰}} \quad \text{jours calendaires, sans le montant du marché} $$

**Les chiffres de ce chantier**

| | |
|---|---:|
| Un jour, hors pénalités | **{{reception.cout_d_un_jour.cout_hors_penalites_MAD_par_jour_ouvre::k}} MAD** |
| Un jour, sous pénalités | **{{reception.cout_d_un_jour.cout_sous_penalites_MAD_par_jour_ouvre::k}} MAD** · ×{{reception.cout_d_un_jour.rapport_des_deux_regimes::n1}} ({{reception.cout_d_un_jour.rapport_bornes.0::n1}} à {{reception.cout_d_un_jour.rapport_bornes.1::n1}}) |
| Fenêtre de cherté | {{reception.cout_d_un_jour.jour_de_bascule_calendaire::n0}} j calendaires ({{reception.cout_d_un_jour.jour_de_bascule_bornes_calendaires.0::n0}} à {{reception.cout_d_un_jour.jour_de_bascule_bornes_calendaires.1::n0}}) |
| Opérations préalables | {{reception.operations_prealables.duree_totale_j::n0}} j ouvrés ({{reception.operations_prealables.duree_bornes_j.0::n0}} à {{reception.operations_prealables.duree_bornes_j.1::n0}}), dont {{reception.operations_prealables.part_tenue_par_des_tiers_pct::n0}} % tenus par des tiers |
| Ce que le planning en prévoit | {{reception.confrontation_au_planning.ecart_total_j::n0}} j de trop, **{{reception.confrontation_au_planning.decalage_mesure_de_la_fin_j::n0}} j de fin** mesurés ({{reception.confrontation_au_planning.decalage_bornes_j.0::n0}} à {{reception.confrontation_au_planning.decalage_bornes_j.1::n0}}) |
| Réserves | {{reception.reserves.nb_total}} dont **{{reception.reserves.nb_bloquantes}} bloquantes** · les confondre ajoute {{reception.reserves.jours_de_non_reception_en_plus::n1}} j |
| Retenue immobilisée | {{reception.portage.retenue_immobilisee_MAD::k}} MAD · {{reception.portage.cout_de_la_retenue_MAD_par_mois::k}} MAD/mois contre {{reception.portage.cout_de_la_caution_MAD_par_mois::k}} en caution |
| DOE reconstitué | {{reception.doe.cout_total_du_retard_de_DOE_MAD::k}} MAD, dont {{reception.doe.part_du_portage_dans_le_surcout_pct::n0}} % d'argent dû qui attend |

**Les six réflexes**

1. Demander si le chantier est dans son délai **avant** de chiffrer un jour.
2. Qualifier les réserves, ne jamais les compter — et chercher ce que chacune attend.
3. Lire la pénalité, son plafond ET leur calendrier, et calculer le jour de bascule avant de signer.
4. Mettre les opérations préalables au planning, avec leurs responsables.
5. Exiger les documents du DOE **quand le sous-traitant est encore là**.
6. Nommer un responsable de la garde de l'ouvrage, et de ses installations de sécurité.

**⏸ Ce qui reste fermé sans les documents** — durées des garanties, délai de levée des réserves,
conditions d'une réception tacite, contenu obligatoire du DOE, délai de paiement du décompte
définitif, et **les effets juridiques de la réception**. Le module donne le mécanisme et sa
conséquence financière, jamais la durée ni la règle de droit.
:::
