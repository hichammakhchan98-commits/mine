---
id: C3
titre: Gros œuvre — le cycle, le parc de coffrage et le bétonnage par temps chaud
fil: Palier 1 · module 4 — exécution et chantier
resume: Un cycle n'est pas une durée, c'est une contrainte de ressource — et la ressource qui le borne n'est presque jamais celle qu'on surveille. Trois leviers calculés, dont deux qui renversent le réflexe de chantier.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · toutes les valeurs numériques sont V3 · aucun critère de résistance n'est donné
pied: Exemple pédagogique — ne remplace ni un plan de méthode visé, ni une note d'étaiement, ni le plan de bétonnage d'un chantier réel.
donnees: gros-oeuvre, tranche-plancher, planification, prix, gare
---

## S1 · Ce que ce module fait, et ce qu'il ne refait pas

Vous savez ce qu'est une banche, un étai, une reprise de bétonnage. Ce module ne vous l'apprend pas.
Il traite trois choses qu'un manuel d'exécution ne donne pas, parce qu'elles demandent un calcul et
non une description :

1. **le parc de coffrage est une contrainte de cadence**, souvent la première, et il a un optimum
   économique qui n'est ni le plus grand ni le plus petit — et qui dépend de la **marge** du
   plancher, pas de sa durée ;
2. **par temps chaud, ce n'est pas la cadence qui commande le bétonnage**, c'est le temps de
   maniabilité : le débit minimal pour éviter une reprise froide se calcule, et il décide du nombre
   de toupies — mais ce n'est pas lui qui décide de l'heure à laquelle on finit ;
3. **un point d'arrêt est une tâche**, avec une durée, sur le chemin critique du cycle. Le traiter
   comme une formalité est la façon la plus sûre de le faire sauter.

Le cycle lui-même est celui du module TV : {{gros-oeuvre.cycle.duree_j::n2}} jours par zone, une zone
tous les {{gros-oeuvre.cycle.cadence_j::n1}} jours, bornée par
l'{{gros-oeuvre.cycle.ressource_qui_borne}}. Ce module ne le recalcule pas — il le **lit**, et c'est
une discipline : trois modules qui recalculent la même grandeur finissent par en publier trois
valeurs.

**Prérequis** : le module TV (cycle d'une zone), D2 (marges), D1 (frais de durée).
**Place dans le projet** : étape 7 du déroulé (§ 10.2).

## S2 · L'idée centrale : un cycle est borné par une ressource, pas par une durée

Un cycle de gros œuvre a trois bornes possibles, et il prend la plus contraignante :

| Borne | Ce qu'elle vaut ici | Comment on la desserre |
|---|---:|---|
| L'**équipe** la plus lente | {{gros-oeuvre.cycle.cadence_j::n1}} j | un atelier de plus, ou une cadence meilleure |
| La **grue**, si elle est partagée | voir D2 · § S4g | une seconde grue, ou sortir une tâche de la grue |
| Le **parc de coffrage** | {{gros-oeuvre.parc.cadence_du_parc_declare_j::n2}} j avec le parc déclaré | louer plus de tables |

La troisième est celle qu'on surveille le moins, et c'est souvent elle qui borne — parce qu'elle ne
se voit pas sur un planning. Un planning montre des tâches ; il ne montre pas qu'il n'y a plus de
tables.

### Ce qui immobilise le coffrage n'est pas ce qui occupe les équipes

Une zone retient son coffrage pendant **{{gros-oeuvre.immobilisation_du_coffrage.duree_j::n2}} jours**,
dont **{{gros-oeuvre.immobilisation_du_coffrage.dont_cure_j::n1}} jours de cure**, soit
{{gros-oeuvre.immobilisation_du_coffrage.part_de_cure_pct::n1}} % du total.

{{gros-oeuvre.immobilisation_du_coffrage.lecture}}

C'est la clé du dimensionnement du parc : on ne divise pas la surface par le nombre d'équipes, on la
divise par le nombre de zones **simultanément coffrées**, qui vaut l'immobilisation divisée par la
cadence.

$$ T \geq \frac{I}{\left\lfloor \text{parc} / S_{\text{zone}} \right\rfloor} $$

Le plancher dans la formule n'est pas un détail d'écriture : un parc de 2,6 zones n'en porte que
deux.

:::figure {"fn":"gantt","args":"gros-oeuvre.figures.cycle","titre":"Le cycle d'une zone de plancher, et ce qui tient le coffrage","num":1,"large":true,"voir":["Les sept tâches sont toutes critiques : un cycle de zone n'a pas de marge interne, et c'est normal — on l'a construit en resserrant les recouvrements jusqu'à la limite.","Le point d'arrêt (visa du ferraillage) est une barre comme les autres, de {{gros-oeuvre.points_d_arret.duree_dans_le_cycle_j::n2}} jour, soit {{gros-oeuvre.points_d_arret.part_du_cycle_pct::n1}} % du cycle. Il se planifie ; il ne s'improvise pas la veille du coulage.","La cure occupe {{gros-oeuvre.immobilisation_du_coffrage.part_de_cure_pct::n0}} % du cycle sans occuper personne. Mettre plus d'hommes sur ce cycle ne la touche pas — c'est une durée imposée au sens du module D2."],"erreur":"Lire ce diagramme comme la charge de travail d'une zone. Il montre l'IMMOBILISATION du coffrage ; les effectifs, eux, montent et descendent à l'intérieur, et deux des sept barres n'occupent personne."}
:::

## S3 · Principes

### a. Le parc de coffrage a un optimum, et il dépend de la marge

Trois termes, et le troisième est celui qu'on oublie :

- le **loyer** du parc, proportionnel à sa taille **et** à la durée ;
- le **montage et le repli**, proportionnels à sa taille seulement ;
- les **frais de durée** du chantier — mais **seulement si l'allongement dépasse la marge** du
  plancher.

C'est ce dernier point qui décide de tout. Un parc plus petit allonge le plancher ; tant que
l'allongement tient dans la marge, il ne coûte **rien au chantier**. Ce qu'un petit parc achète,
ce n'est pas du délai : c'est de la **marge**.

### b. Par temps chaud : deux contraintes, pas une

Une dalle ne se coule pas en nappe : elle se coule **par bandes** qui avancent. La bande suivante
doit rejoindre la précédente avant que celle-ci n'ait pris, sans quoi la vibration ne les mélange
plus et il se forme un plan de faiblesse qui ne se répare pas.

$$ \dot{V}_{\min} = \frac{\ell \times L \times e}{t_{\text{maniabilité}}} $$

où $\ell$ est la largeur de bande, $L$ la largeur traversée et $e$ l'épaisseur de dalle. Le débit
minimal ne dépend **ni de l'effectif ni de la cadence** : c'est une contrainte physique.

Mais ce débit minimal est un **plancher**, pas le débit auquel on coule. Le débit réellement tenu
dépend de la rotation des toupies, et c'est lui qui décide de l'heure à laquelle on finit — donc de
la température à laquelle on finit. **Deux contraintes, deux décisions différentes.**

## S4 · Étude de cas : le plancher de mezzanine de la gare

### a. Quel parc de coffrage commander ?

| Parc | Zones | Cadence du parc | Cadence tenue | Durée | Rallonge | Marge restante | Loyer + montage | Frais de durée | **Total** |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| {{gros-oeuvre.parc.lignes.0.parc_m2}} m² | {{gros-oeuvre.parc.lignes.0.zones_simultanees}} | {{gros-oeuvre.parc.lignes.0.cadence_du_parc_j::n2}} j | {{gros-oeuvre.parc.lignes.0.cadence_tenue_j::n2}} j | {{gros-oeuvre.parc.lignes.0.duree_du_plancher_j::n1}} j | +{{gros-oeuvre.parc.lignes.0.rallonge_j::n1}} j | **dépasse de {{gros-oeuvre.parc.lignes.0.depassement_j::n1}} j** | {{gros-oeuvre.parc.lignes.0.loyer_et_montage_MAD::n0}} | {{gros-oeuvre.parc.lignes.0.frais_de_duree_MAD::n0}} | {{gros-oeuvre.parc.lignes.0.total_MAD::n0}} |
| **{{gros-oeuvre.parc.lignes.1.parc_m2}} m²** | {{gros-oeuvre.parc.lignes.1.zones_simultanees}} | {{gros-oeuvre.parc.lignes.1.cadence_du_parc_j::n2}} j | {{gros-oeuvre.parc.lignes.1.cadence_tenue_j::n2}} j | {{gros-oeuvre.parc.lignes.1.duree_du_plancher_j::n1}} j | +{{gros-oeuvre.parc.lignes.1.rallonge_j::n1}} j | {{gros-oeuvre.parc.lignes.1.marge_restante_j::n1}} j | {{gros-oeuvre.parc.lignes.1.loyer_et_montage_MAD::n0}} | 0 | **{{gros-oeuvre.parc.lignes.1.total_MAD::n0}}** |
| {{gros-oeuvre.parc.lignes.2.parc_m2}} m² *(déclaré)* | {{gros-oeuvre.parc.lignes.2.zones_simultanees}} | {{gros-oeuvre.parc.lignes.2.cadence_du_parc_j::n2}} j | {{gros-oeuvre.parc.lignes.2.cadence_tenue_j::n2}} j | {{gros-oeuvre.parc.lignes.2.duree_du_plancher_j::n1}} j | — | {{gros-oeuvre.parc.lignes.2.marge_restante_j::n1}} j | {{gros-oeuvre.parc.lignes.2.loyer_et_montage_MAD::n0}} | 0 | {{gros-oeuvre.parc.lignes.2.total_MAD::n0}} |
| {{gros-oeuvre.parc.lignes.3.parc_m2}} m² | {{gros-oeuvre.parc.lignes.3.zones_simultanees}} | {{gros-oeuvre.parc.lignes.3.cadence_du_parc_j::n2}} j | {{gros-oeuvre.parc.lignes.3.cadence_tenue_j::n2}} j | {{gros-oeuvre.parc.lignes.3.duree_du_plancher_j::n1}} j | — | {{gros-oeuvre.parc.lignes.3.marge_restante_j::n1}} j | {{gros-oeuvre.parc.lignes.3.loyer_et_montage_MAD::n0}} | 0 | {{gros-oeuvre.parc.lignes.3.total_MAD::n0}} |
| {{gros-oeuvre.parc.lignes.4.parc_m2}} m² | {{gros-oeuvre.parc.lignes.4.zones_simultanees}} | {{gros-oeuvre.parc.lignes.4.cadence_du_parc_j::n2}} j | {{gros-oeuvre.parc.lignes.4.cadence_tenue_j::n2}} j | {{gros-oeuvre.parc.lignes.4.duree_du_plancher_j::n1}} j | — | {{gros-oeuvre.parc.lignes.4.marge_restante_j::n1}} j | {{gros-oeuvre.parc.lignes.4.loyer_et_montage_MAD::n0}} | 0 | {{gros-oeuvre.parc.lignes.4.total_MAD::n0}} |
| {{gros-oeuvre.parc.lignes.5.parc_m2}} m² | {{gros-oeuvre.parc.lignes.5.zones_simultanees}} | {{gros-oeuvre.parc.lignes.5.cadence_du_parc_j::n2}} j | {{gros-oeuvre.parc.lignes.5.cadence_tenue_j::n2}} j | {{gros-oeuvre.parc.lignes.5.duree_du_plancher_j::n1}} j | — | {{gros-oeuvre.parc.lignes.5.marge_restante_j::n1}} j | {{gros-oeuvre.parc.lignes.5.loyer_et_montage_MAD::n0}} | 0 | {{gros-oeuvre.parc.lignes.5.total_MAD::n0}} |

**L'optimum est à {{gros-oeuvre.parc.optimum.parc_m2}} m²** —
{{gros-oeuvre.parc.optimum.zones_simultanees}} zones simultanées — et il n'est **ni le plus petit ni
le plus grand**. Trois lectures de ce tableau :

1. **En dessous, le parc devient la borne.** À {{gros-oeuvre.parc.lignes.0.parc_m2}} m², une seule
   zone tient à la fois : la cadence tombe à {{gros-oeuvre.parc.lignes.0.cadence_du_parc_j::n2}} jours,
   le plancher double de durée, l'allongement **dépasse la marge** de
   {{gros-oeuvre.parc.lignes.0.depassement_j::n1}} jours et les frais de durée du chantier entier se
   réveillent. L'économie de loyer est largement reperdue.
2. **Au-dessus de l'optimum, on paie sans rien acheter.** Dès
   {{gros-oeuvre.parc.lignes.2.parc_m2}} m², ce sont les **équipes** qui bornent : ajouter des tables
   ne raccourcit plus rien. Chaque m² de plus est du loyer pur.
3. **Le parc déclaré dans les données du projet coûte
   {{gros-oeuvre.parc.lignes.2.total_MAD::n0}} MAD contre
   {{gros-oeuvre.parc.optimum.total_MAD::n0}}** pour l'optimum. Ce que cet écart achète, ce n'est pas
   du délai — c'est {{gros-oeuvre.parc.lignes.1.rallonge_j::n1}} jours de marge rendue au plancher.

:::figure {"fn":"barres","args":"gros-oeuvre.figures.parc","titre":"Coût total du coffrage selon la taille du parc","num":2,"large":true,"options":{"unite":"milliers de MAD — loyer, montage et frais de durée"},"voir":["Les barres dessinent un U, et c'est tout l'intérêt : le plus petit parc n'est pas le moins cher, parce qu'il fait dépasser la marge et réveille les frais de durée du chantier entier.","À droite du minimum, le coût remonte linéairement : ce sont les équipes qui bornent, et chaque m² de table en plus est du loyer qui n'achète rien.","Le minimum est à {{gros-oeuvre.parc.optimum.parc_m2}} m², soit {{gros-oeuvre.parc.optimum.zones_simultanees}} zones de coffrage simultanées — et non les {{gros-oeuvre.parc.parc_declare_m2}} m² que le projet avait posés. Un parc se compte en m² de TABLES : une zone en demande {{tranche-plancher.quantites.coffrage_m2::n1}} pour {{tranche-plancher.quantites.surface_m2::n0}} m² de plancher coulé."],"erreur":"Dimensionner un parc sur la surface d'une zone multipliée par le nombre d'équipes. La bonne grandeur est l'IMMOBILISATION divisée par la cadence : une zone retient son coffrage pendant sa cure, où aucune équipe n'est présente."}
:::

:::encart {"genre":"alerte","titre":"Ce que ce calcul ne chiffre pas"}
{{gros-oeuvre.parc.ce_que_le_calcul_ne_price_pas}}
:::

### b. Combien de toupies commander pour le coulage de demain ?

Le débit minimal, d'abord — celui en dessous duquel il se forme une reprise froide entre deux bandes :

| Température du béton frais | Temps de maniabilité | Débit minimal |
|---|---:|---:|
| 20 °C | {{gros-oeuvre.betonnage.par_temperature.a_20_degres.temps_de_maniabilite_h::n1}} h | {{gros-oeuvre.betonnage.par_temperature.a_20_degres.debit_minimal_m3_h::n1}} m³/h |
| 30 °C | {{gros-oeuvre.betonnage.par_temperature.a_30_degres.temps_de_maniabilite_h::n1}} h | {{gros-oeuvre.betonnage.par_temperature.a_30_degres.debit_minimal_m3_h::n1}} m³/h |
| **{{gros-oeuvre.betonnage.temperature_de_calcul_C::n0}} °C** | {{gros-oeuvre.betonnage.par_temperature.a_35_degres.temps_de_maniabilite_h::n1}} h | **{{gros-oeuvre.betonnage.par_temperature.a_35_degres.debit_minimal_m3_h::n1}} m³/h** |

Le débit à tenir est **×{{gros-oeuvre.betonnage.rapport_35_sur_20::n2}} plus élevé** à
{{gros-oeuvre.betonnage.temperature_de_calcul_C::n0}} °C qu'à 20 °C, pour exactement le même ouvrage.
C'est le même béton, la même dalle, la même équipe — et une contrainte d'organisation qui double.

:::figure {"fn":"barres","args":"gros-oeuvre.figures.debits","titre":"Débit minimal pour éviter une reprise froide, selon la température du béton frais","num":3,"large":true,"options":{"unite":"m³/h — volume d'une bande divisé par le temps de maniabilité"},"voir":["Le volume en jeu est celui d'une BANDE — {{gros-oeuvre.betonnage.volume_d_une_bande_m3::n1}} m³ — et non celui de la zone entière. Une dalle se coule par bandes qui se rattrapent, pas en couches superposées.","Le temps de maniabilité se contracte plus vite que la température ne monte : de 20 à {{gros-oeuvre.betonnage.temperature_de_calcul_C::n0}} °C, il est divisé par {{gros-oeuvre.betonnage.rapport_35_sur_20::n2}}.","Ce débit est un PLANCHER, pas un objectif : il dit à quelle vitesse il faut avancer pour que les bandes se rejoignent. Il ne dit rien de l'heure à laquelle on finit."],"erreur":"Raisonner en couches horizontales sur toute la surface. Une première version de ce calcul le faisait et demandait 138 m³/h et vingt-deux toupies pour une dalle de 25 cm. L'arithmétique était juste ; l'image de l'ouvrage était fausse."}
:::

Le débit **tenu**, ensuite — celui qui décide de l'heure de fin. Une toupie de
{{gare.gros_oeuvre.betonnage_temps_chaud.volume_toupie_m3.valeur}} m³ qui boucle sa rotation en
{{gare.gros_oeuvre.betonnage_temps_chaud.rotation_toupie_min.valeur}} minutes livre
{{gros-oeuvre.betonnage.debit_d_une_toupie_m3_h::n1}} m³/h.

| Toupies | Débit tenu | Durée du coulage | |
|---:|---:|---:|---|
| {{gros-oeuvre.betonnage.options_de_rotation.0.toupies}} | {{gros-oeuvre.betonnage.options_de_rotation.0.debit_tenu_m3_h::n1}} m³/h | {{gros-oeuvre.betonnage.options_de_rotation.0.duree_du_coulage_h::n2}} h | tient le minimum, finit en pleine chaleur |
| {{gros-oeuvre.betonnage.options_de_rotation.1.toupies}} | {{gros-oeuvre.betonnage.options_de_rotation.1.debit_tenu_m3_h::n1}} m³/h | {{gros-oeuvre.betonnage.options_de_rotation.1.duree_du_coulage_h::n2}} h | |
| **{{gros-oeuvre.betonnage.options_de_rotation.2.toupies}}** | **{{gros-oeuvre.betonnage.options_de_rotation.2.debit_tenu_m3_h::n1}} m³/h** | **{{gros-oeuvre.betonnage.options_de_rotation.2.duree_du_coulage_h::n2}} h** | **retenu** — sous la cible de {{gros-oeuvre.betonnage.duree_cible_du_coulage_h::n0}} h |
| {{gros-oeuvre.betonnage.options_de_rotation.4.toupies}} | {{gros-oeuvre.betonnage.options_de_rotation.4.debit_tenu_m3_h::n1}} m³/h | {{gros-oeuvre.betonnage.options_de_rotation.4.duree_du_coulage_h::n2}} h | |
| {{gros-oeuvre.betonnage.options_de_rotation.6.toupies}} | {{gros-oeuvre.betonnage.options_de_rotation.6.debit_tenu_m3_h::n1}} m³/h | {{gros-oeuvre.betonnage.options_de_rotation.6.duree_du_coulage_h::n2}} h | la pompe commence à borner |

{{gros-oeuvre.betonnage.deux_contraintes}}

:::figure {"fn":"barres","args":"gros-oeuvre.figures.toupies","titre":"Durée du coulage selon le nombre de toupies en rotation","num":4,"large":true,"options":{"unite":"heures de coulage pour une zone de plancher","bande":{"$":"gros-oeuvre.figures.toupies_cible"},"libelle_bande":"avant la chaleur"},"voir":["Deux toupies suffisent à tenir le débit minimal — à ne pas faire de reprise froide — et pourtant le coulage durerait {{gros-oeuvre.betonnage.options_de_rotation.0.duree_du_coulage_h::n1}} heures et finirait à la pire heure de la journée.","Le gain s'écrase : passer de deux à quatre toupies divise la durée par deux, passer de six à huit ne gagne plus rien parce que la pompe borne à {{gros-oeuvre.betonnage.debit_pratique_d_une_pompe_m3_h::n0}} m³/h.","C'est la deuxième contrainte — finir avant la chaleur — qui décide de la commande, pas la première."],"erreur":"Commander les toupies sur le débit minimal. Le minimum interdit un défaut ; il ne fait pas finir le coulage à temps. Les deux nombres ne répondent pas à la même question et le second est plus grand."}
:::

**Quand le débit n'est pas tenable.** {{gros-oeuvre.betonnage.parade_si_le_debit_n_est_pas_tenable}}

Et la décision de la veille : {{gros-oeuvre.fenetre_de_coulage.regle}} Avec
{{gros-oeuvre.betonnage.duree_du_coulage_h::n1}} h de coulage, un démarrage à
{{gros-oeuvre.fenetre_de_coulage.demarrage_conseille}} fait finir vers
{{gros-oeuvre.fenetre_de_coulage.fin_attendue}}.

### c. Les points d'arrêt, et pourquoi ils sautent

{{gros-oeuvre.points_d_arret.nombre}} points d'arrêt sur ce cycle. Celui du ferraillage pèse
{{gros-oeuvre.points_d_arret.duree_dans_le_cycle_j::n2}} jour, soit
{{gros-oeuvre.points_d_arret.part_du_cycle_pct::n1}} % du cycle — et il est **sur le chemin critique
du cycle**.

| Étape | Visée par | Critère |
|---|---|---|
| {{gros-oeuvre.points_d_arret.liste.0.etape}} | {{gros-oeuvre.points_d_arret.liste.0.vise_par}} | {{gros-oeuvre.points_d_arret.liste.0.critere}} |
| {{gros-oeuvre.points_d_arret.liste.1.etape}} | {{gros-oeuvre.points_d_arret.liste.1.vise_par}} | {{gros-oeuvre.points_d_arret.liste.1.critere}} |
| {{gros-oeuvre.points_d_arret.liste.2.etape}} | {{gros-oeuvre.points_d_arret.liste.2.vise_par}} | {{gros-oeuvre.points_d_arret.liste.2.critere}} |
| {{gros-oeuvre.points_d_arret.liste.3.etape}} | {{gros-oeuvre.points_d_arret.liste.3.vise_par}} | {{gros-oeuvre.points_d_arret.liste.3.critere}} |
| {{gros-oeuvre.points_d_arret.liste.4.etape}} | {{gros-oeuvre.points_d_arret.liste.4.vise_par}} | {{gros-oeuvre.points_d_arret.liste.4.critere}} |

:::encart {"genre":"alerte","titre":"Le piège structurel du point d'arrêt"}
{{gros-oeuvre.points_d_arret.le_piege}}
:::

**Côté entreprise.** {{gros-oeuvre.points_d_arret.double_lecture.entreprise}}

**Côté maîtrise d'œuvre.** {{gros-oeuvre.points_d_arret.double_lecture.maitrise_d_oeuvre}}

### d. Les six contrôles du dernier quart d'heure

{{gros-oeuvre.controles_avant_coulage.regle}}

| Contrôle | Ce qu'on regarde | Le symptôme si on l'a raté |
|---|---|---|
| {{gros-oeuvre.controles_avant_coulage.liste.0.controle}} | {{gros-oeuvre.controles_avant_coulage.liste.0.comment}} | {{gros-oeuvre.controles_avant_coulage.liste.0.symptome_si_rate}} |
| {{gros-oeuvre.controles_avant_coulage.liste.1.controle}} | {{gros-oeuvre.controles_avant_coulage.liste.1.comment}} | {{gros-oeuvre.controles_avant_coulage.liste.1.symptome_si_rate}} |
| {{gros-oeuvre.controles_avant_coulage.liste.2.controle}} | {{gros-oeuvre.controles_avant_coulage.liste.2.comment}} | {{gros-oeuvre.controles_avant_coulage.liste.2.symptome_si_rate}} |
| {{gros-oeuvre.controles_avant_coulage.liste.3.controle}} | {{gros-oeuvre.controles_avant_coulage.liste.3.comment}} | {{gros-oeuvre.controles_avant_coulage.liste.3.symptome_si_rate}} |
| {{gros-oeuvre.controles_avant_coulage.liste.4.controle}} | {{gros-oeuvre.controles_avant_coulage.liste.4.comment}} | {{gros-oeuvre.controles_avant_coulage.liste.4.symptome_si_rate}} |
| {{gros-oeuvre.controles_avant_coulage.liste.5.controle}} | {{gros-oeuvre.controles_avant_coulage.liste.5.comment}} | {{gros-oeuvre.controles_avant_coulage.liste.5.symptome_si_rate}} |

## S4b · Les hypothèses de ce module, déclarées

**Le parc de coffrage** —
⟦V3|location d'un parc de coffrage|48 MAD/m²/mois|MAD/m²/mois|32 à 70|2026|tables coffrantes et étaiement associé, location nue, transport amorti⟧,
⟦V3|montage et repli d'un parc de coffrage|55 MAD/m²|MAD/m²|35 à 85|2026|première mise en place et repli, indépendants de la durée⟧.

**Le bétonnage par temps chaud** —
⟦V3|temps de maniabilité à 20 °C|3,0 h|h|2,0 à 4,5|2026|délai utile entre deux bandes successives⟧,
⟦V3|temps de maniabilité à 30 °C|1,8 h|h|1,2 à 2,5|2026⟧,
⟦V3|temps de maniabilité à 35 °C|1,3 h|h|0,8 à 2,0|2026|régime d'été de la région de Marrakech : c'est le cas dimensionnant⟧,
⟦V3|température du béton frais retenue|35 °C|°C|25 à 42|2026|température du BÉTON, non de l'air : la différence se joue sur le transport et la cure des granulats⟧,
⟦V3|largeur d'une bande de coulage|4,0 m|m|3,0 à 6,0|2026|fixée par la portée de flèche de pompe et la largeur de règle vibrante⟧,
⟦V3|volume d'une toupie|8 m³|m³|6 à 10|2026⟧,
⟦V3|durée de rotation d'une toupie|75 min|min|45 à 120|2026|aller, attente, vidange, retour, lavage — centrale à une vingtaine de minutes⟧,
⟦V3|débit pratique d'une pompe automotrice|45 m³/h|m³/h|25 à 70|2026|débit de chantier, déplacements de flèche et attentes de toupie compris — et non le débit catalogue⟧,
⟦V3|durée cible d'un coulage|4 h|h|3 à 6|2026|pour qu'un coulage démarré à l'aube finisse avant la montée en température ; décision de conduite, pas contrainte physique⟧.

Le **cycle**, la **cadence** et la **marge** ne sont pas déclarés ici : ils viennent des modules TV
et D2, et ce module les lit.

## S4c · Sécurité : quatre opérations que ce cycle décide

Le § 3.4 impose de dire ce qu'un cycle décide en matière de risque. Les dispositions ci-dessous sont
**essentielles et non exhaustives** ; elles ne remplacent ni le plan de sécurité du chantier, ni les
obligations réglementaires du marché. **Aucun critère de résistance n'est donné** — la phase § 5.0
l'interdit, et c'est précisément le cœur du premier point.

| Opération | Ce que le cycle décide | Disposition essentielle |
|---|---|---|
| **Décoffrage** | le moment où l'on dépose les tables | le critère est une **résistance**, jamais une durée. La durée de {{gare.cycle_zone.cure_avant_decoffrage_j.valeur}} jour(s) de ce module est une hypothèse de planification, pas un critère d'exécution : sur un chantier, on décoffre sur essai |
| **Étaiement de reprise** | combien de niveaux restent étayés sous celui qu'on coule | un plancher jeune ne porte pas seul le poids du plancher suivant ; la dépose des étais de reprise suit une note, pas une place à libérer |
| **Travail en hauteur** sur le coffrage | la pression de rotation sur la pose et la dépose | protections périphériques posées **avant** le coffrage et déposées **après** — une rotation serrée pousse exactement à l'inverse |
| **Coulage par temps chaud** | l'heure et la durée du coulage | un coulage qui déborde dans la chaleur, c'est une équipe sous contrainte thermique **et** un béton qui prend plus vite : le risque pour les hommes et le risque pour l'ouvrage montent ensemble |

**Le lien avec tout ce module, et c'est le plus important.** Le § S4a montre qu'un parc plus petit
coûte moins cher tant que l'allongement tient dans la marge. Il montre aussi ce qui arrive quand la
marge est épuisée : la pression revient sur le cycle, et le premier poste qu'on comprime est celui
qui n'occupe personne — **la cure**. Un parc serré n'est pas dangereux en soi ; il le devient le jour
où le chantier a pris du retard ailleurs et qu'on cherche des jours là où il n'y en a pas.

## S5 · Erreurs fréquentes, et ce qu'elles coûtent

| Erreur | Comment elle se voit | Ce qu'elle coûte |
|---|---|---|
| Parc dimensionné sur la surface d'une zone | il manque des tables dès la troisième zone | la cadence tombe à {{gros-oeuvre.parc.lignes.0.cadence_du_parc_j::n1}} j, le plancher double |
| Parc commandé large « pour être tranquille » | aucun symptôme, et c'est le problème | {{gros-oeuvre.parc.lignes.5.loyer_et_montage_MAD::n0}} MAD au lieu de {{gros-oeuvre.parc.optimum.total_MAD::n0}} |
| Durée de décoffrage traitée comme un critère | le planning tient, les éprouvettes suivent de loin | un plancher décoffré trop tôt ne se répare pas |
| Toupies commandées sur le débit minimal | le coulage s'éternise et finit à 13 h | {{gros-oeuvre.betonnage.options_de_rotation.0.duree_du_coulage_h::n1}} h au lieu de {{gros-oeuvre.betonnage.duree_du_coulage_h::n1}} h, en pleine chaleur |
| Bétonnage raisonné en couches, pas en bandes | des débits absurdes, qu'on finit par ignorer | un calcul faux abandonné vaut un calcul pas fait |
| Point d'arrêt demandé le matin pour couler l'après-midi | le visa est donné à la légère ou refusé | dans les deux cas, personne n'a vu le ferraillage |
| Protections déposées avant la dépose du coffrage | le gain de dix minutes par zone | le seul risque de ce module qui ne se répare pas |

## S6 · Exercices

:::exercice {"titre":"1 · Dimensionner un parc de coffrage","niveau":"application"}
Une zone fait {{tranche-plancher.quantites.surface_m2::n0}} m² et immobilise son coffrage pendant
{{gros-oeuvre.immobilisation_du_coffrage.duree_j::n2}} jours. Vous voulez tenir la cadence des
équipes, {{gros-oeuvre.cycle.cadence_j::n1}} jours par zone. Quel parc minimum ?

**Corrigé.** Deux pièges, et le premier se voit à l'unité.

Nombre de zones simultanément coffrées :
{{gros-oeuvre.immobilisation_du_coffrage.duree_j::n2}} / {{gros-oeuvre.cycle.cadence_j::n1}} = 2,37,
soit **3 zones** — on arrondit vers le haut, parce qu'une fraction de zone coffrée occupe quand même
un jeu de tables.

Parc minimum : 3 × **{{tranche-plancher.quantites.coffrage_m2::n1}}** =
**{{gros-oeuvre.parc.lignes.2.parc_m2}} m²**, et c'est précisément le parc déclaré au projet. Le
piège est le facteur qu'on multiplie : un parc est un stock de **tables**, donc on multiplie la
surface de **coffrage** d'une zone ({{tranche-plancher.quantites.coffrage_m2::n1}} m²), pas sa
surface de plancher ({{tranche-plancher.quantites.surface_m2::n0}} m²). L'écart est de
{{tranche-plancher.quantites.ratio_coffrage_m2_par_m2::n3}}, soit 18 % — assez pour croire qu'on a
trois zones de parc quand on n'en a que deux et demie.

*Et pourtant l'optimum économique est à {{gros-oeuvre.parc.optimum.parc_m2}} m², avec
{{gros-oeuvre.parc.optimum.zones_simultanees}} zones seulement. La différence : le dimensionnement
ci-dessus répond à « quel parc pour ne pas ralentir ? », l'optimum à « quel parc pour dépenser le
moins ? ». Ralentir de {{gros-oeuvre.parc.lignes.1.rallonge_j::n1}} jours ne coûte rien ici, parce
que le plancher a {{gros-oeuvre.parc.marge_disponible_j::n1}} jours de marge libre. Les deux
questions sont légitimes ; ce sont les réponses qu'il ne faut pas confondre.*
:::

:::exercice {"titre":"2 · Combien de toupies pour demain ?","niveau":"application"}
Zone de {{gros-oeuvre.betonnage.volume_de_la_zone_m3::n1}} m³, coulage prévu en juillet, béton frais
attendu à {{gros-oeuvre.betonnage.temperature_de_calcul_C::n0}} °C. Toupies de
{{gare.gros_oeuvre.betonnage_temps_chaud.volume_toupie_m3.valeur}} m³, rotation
{{gare.gros_oeuvre.betonnage_temps_chaud.rotation_toupie_min.valeur}} min. Combien en commandez-vous ?

**Corrigé.** Deux calculs, et le second commande.

**Le minimum**, pour ne pas faire de reprise froide : une bande de
{{gros-oeuvre.betonnage.largeur_de_bande_m::n0}} m × {{gros-oeuvre.betonnage.longueur_de_bande_m::n0}} m
× {{gros-oeuvre.betonnage.epaisseur_de_dalle_m::n2}} m =
{{gros-oeuvre.betonnage.volume_d_une_bande_m3::n1}} m³, à rattraper en
{{gros-oeuvre.betonnage.par_temperature.a_35_degres.temps_de_maniabilite_h::n1}} h →
**{{gros-oeuvre.betonnage.debit_dimensionnant_m3_h::n1}} m³/h**, soit
{{gros-oeuvre.betonnage.toupies_pour_tenir_le_minimum}} toupies.

**L'heure de fin**, pour ne pas couler dans la chaleur : avec
{{gros-oeuvre.betonnage.toupies_pour_tenir_le_minimum}} toupies, le coulage dure
{{gros-oeuvre.betonnage.options_de_rotation.0.duree_du_coulage_h::n1}} h — il finirait au plus chaud.
Pour tenir sous {{gros-oeuvre.betonnage.duree_cible_du_coulage_h::n0}} h, il en faut
**{{gros-oeuvre.betonnage.toupies_retenues}}**, et le coulage dure
{{gros-oeuvre.betonnage.duree_du_coulage_h::n1}} h.

**Réponse : {{gros-oeuvre.betonnage.toupies_retenues}} toupies**, démarrage
{{gros-oeuvre.fenetre_de_coulage.demarrage_conseille}}.

*Le piège : s'arrêter au premier calcul parce qu'il est le plus technique. Le minimum interdit un
défaut ; il ne fait pas finir le coulage à temps. Et au-delà de
{{gros-oeuvre.betonnage.options_de_rotation.6.toupies}} toupies, la pompe borne : commander plus
n'achète plus rien, sinon des camions qui attendent et du béton qui vieillit dans la cuve.*
:::

:::exercice {"titre":"3 · Le parc est arrivé en retard","niveau":"probleme"}
La livraison du parc de coffrage glisse de deux semaines. Pour tenir le démarrage, le loueur vous
propose {{gros-oeuvre.parc.lignes.1.parc_m2}} m² tout de suite au lieu des
{{gros-oeuvre.parc.parc_declare_m2}} m² commandés. Acceptez-vous ?

**Corrigé. Oui, et sans hésiter** — mais pas pour la raison qu'on donne d'habitude.

Avec {{gros-oeuvre.parc.lignes.1.parc_m2}} m², la cadence tombe de
{{gros-oeuvre.parc.lignes.2.cadence_tenue_j::n2}} à
{{gros-oeuvre.parc.lignes.1.cadence_tenue_j::n2}} jours et le plancher s'allonge de
{{gros-oeuvre.parc.lignes.1.rallonge_j::n1}} jours. Le plancher dispose de
{{gros-oeuvre.parc.marge_disponible_j::n1}} jours de marge libre : l'allongement y tient, aucune
autre tâche ne bouge, la date du chantier **ne bouge pas**. Et le loyer est plus faible :
{{gros-oeuvre.parc.lignes.1.total_MAD::n0}} MAD au lieu de
{{gros-oeuvre.parc.lignes.2.total_MAD::n0}}.

**Ce qu'il faut dire en plus, et qui est le vrai sujet** : vous venez de dépenser
{{gros-oeuvre.parc.lignes.1.rallonge_j::n1}} jours d'une marge qui en comptait
{{gros-oeuvre.parc.marge_disponible_j::n1}}. Il en reste
{{gros-oeuvre.parc.lignes.1.marge_restante_j::n1}}. Ce n'est pas gratuit : c'est payé en marge, et la
marge sert à encaisser les aléas qui n'ont pas encore eu lieu. La bonne formulation en réunion est
« j'accepte, et je note que le plancher descend à
{{gros-oeuvre.parc.lignes.1.marge_restante_j::n1}} jours de marge », pas « ça passe ».

*Et si la livraison glissait encore, jusqu'à {{gros-oeuvre.parc.lignes.0.parc_m2}} m² — une seule zone de coffrage ? Là, non :
l'allongement dépasserait la marge de {{gros-oeuvre.parc.lignes.0.depassement_j::n1}} jours, la date
du chantier bougerait, et les frais de durée réveillés —
{{gros-oeuvre.parc.lignes.0.frais_de_duree_MAD::n0}} MAD — coûteraient bien plus que le loyer
économisé.*
:::

:::exercice {"titre":"4 · Trouver les erreurs dans ce plan de bétonnage","niveau":"revue critique"}
Une entreprise vous soumet au visa le plan de bétonnage d'une zone de mezzanine :

> « Coulage de la zone 5 le 14 juillet. Volume {{gros-oeuvre.betonnage.volume_de_la_zone_m3::n1}} m³.
> Démarrage 9 h 00. Une pompe automotrice (débit catalogue 90 m³/h), 2 toupies en rotation.
> Coulage par couches de 50 cm. Décoffrage le surlendemain, J+2, conformément au planning.
> Contrôle du ferraillage par le chef de chantier le matin même avant coulage. »

**Cinq choses ne vont pas. Lesquelles ?**

**Corrigé.**

1. **Démarrage à 9 h en juillet.** Avec {{gros-oeuvre.betonnage.duree_du_coulage_h::n1}} h de
   coulage, on finit vers 13 h, au plus chaud. Le démarrage se cale sur l'heure à laquelle on veut
   avoir **fini** : {{gros-oeuvre.fenetre_de_coulage.demarrage_conseille}} ici.
2. **Le débit catalogue de la pompe n'existe pas sur un chantier.** 90 m³/h est une valeur d'essai ;
   le débit pratique, déplacements de flèche et attentes de toupie compris, est de l'ordre de
   {{gros-oeuvre.betonnage.debit_pratique_d_une_pompe_m3_h::n0}} m³/h. Chiffrer sur le catalogue fait
   croire à un coulage deux fois plus rapide qu'il ne sera.
3. **2 toupies tiennent le minimum, pas l'horaire.** Elles donnent
   {{gros-oeuvre.betonnage.options_de_rotation.0.debit_tenu_m3_h::n1}} m³/h, soit
   {{gros-oeuvre.betonnage.options_de_rotation.0.duree_du_coulage_h::n1}} h de coulage. Il en faut
   {{gros-oeuvre.betonnage.toupies_retenues}}.
4. **« Par couches de 50 cm » ne décrit pas une dalle.** Une dalle de
   {{gros-oeuvre.betonnage.epaisseur_de_dalle_m::n2}} m se coule par **bandes** qui avancent. La
   phrase trahit qu'on a repris le plan de bétonnage d'un voile ou d'un radier — et avec lui le
   mauvais calcul de débit.
5. **« Décoffrage à J+2 conformément au planning » inverse le critère.** On décoffre sur une
   **résistance**, constatée ; le planning dit quand on l'espère, pas quand on y a droit. Et le
   contrôle du ferraillage par le seul chef de chantier n'est pas le point d'arrêt prévu : celui-ci
   est visé par la {{gros-oeuvre.points_d_arret.liste.1.vise_par}}, la veille.

*Ce qu'on vise : rien. Et on demande un plan corrigé la veille au plus tard, pas le matin même —
sinon le visa du ferraillage se donne entre deux toupies.*
:::

## S7 · Check-list, glossaire et quiz

**Check-list avant de lancer un cycle de gros œuvre**

1. Le **parc de coffrage** a-t-il été dimensionné sur l'**immobilisation** divisée par la cadence, et
   non sur la surface d'une zone ?
2. Sait-on **quelle ressource borne** la cadence — équipe, grue ou parc ?
3. L'allongement qu'un parc plus petit entraînerait tient-il dans la **marge** du plancher ?
4. Le **débit minimal** de bétonnage a-t-il été calculé à la température d'été, en **bandes** ?
5. Le nombre de **toupies** tient-il l'**heure de fin**, et pas seulement le débit minimal ?
6. Le **débit de pompe** retenu est-il le débit pratique, et non le catalogue ?
7. Les **points d'arrêt** figurent-ils au planning avec leur durée, et la maîtrise d'œuvre est-elle
   prévenue la veille ?
8. Le critère de **décoffrage** est-il une résistance, avec les éprouvettes qui vont avec ?
9. Les **protections** périphériques sont-elles posées avant le coffrage et déposées après ?

**Glossaire**

| | |
|---|---|
| **Cycle de zone** | la durée entre le début du coffrage d'une zone et la fin de son décoffrage |
| **Cadence de rotation** | l'intervalle entre deux démarrages de zone. Elle est bornée par la ressource la plus contraignante |
| **Immobilisation du coffrage** | la durée pendant laquelle une zone retient son jeu de tables, cure comprise |
| **Parc de coffrage** | la surface de tables et d'étaiement dont on dispose. Il décide d'une cadence |
| **Temps de maniabilité** | la durée pendant laquelle une bande de béton accepte encore d'être vibrée avec la suivante |
| **Reprise froide** | un plan de faiblesse non prévu, créé quand deux bandes ne se rejoignent pas à temps. Il ne se répare pas |
| **Étai de reprise** | l'étai maintenu après décoffrage, parce qu'un plancher jeune ne porte pas seul le niveau suivant |
| **Point d'arrêt** | une étape que l'exécution ne franchit pas sans accord écrit. C'est une tâche du planning |

:::exercice {"titre":"Sept questions pour vérifier","niveau":"application"}
**1. Sur quoi dimensionne-t-on un parc de coffrage ?**
Sur l'**immobilisation divisée par la cadence**, et non sur la surface d'une zone. Une zone retient ses tables pendant sa cure, où aucune équipe n'est présente : ici {{gros-oeuvre.immobilisation_du_coffrage.part_de_cure_pct::n0}} % du cycle.

**2. Un parc plus petit allonge le plancher de trois jours. Combien cela coûte-t-il ?**
**Rien, tant que l'allongement tient dans la marge.** Ce qu'un petit parc achète n'est pas du délai, c'est de la marge — et la marge sert aux aléas. Au-delà, chaque jour de dépassement fait courir les frais de durée du chantier entier.

**3. Quelle est la ressource qui borne la cadence de ce plancher ?**
L'{{gros-oeuvre.cycle.ressource_qui_borne}}. Pas la grue, pas le parc — mais il a fallu calculer les trois pour le savoir, et la réponse change dès qu'on touche à l'une d'elles.

**4. Pourquoi le débit minimal de bétonnage double-t-il entre 20 et 35 °C ?**
Parce que le **temps de maniabilité** se contracte : il passe de {{gros-oeuvre.betonnage.par_temperature.a_20_degres.temps_de_maniabilite_h::n1}} à {{gros-oeuvre.betonnage.par_temperature.a_35_degres.temps_de_maniabilite_h::n1}} h. Le volume d'une bande ne change pas ; le temps pour la rattraper, si.

**5. Combien de toupies commandez-vous : celles du débit minimal, ou plus ?**
**Plus.** Le minimum interdit la reprise froide ; il ne dit rien de l'heure de fin. Ici {{gros-oeuvre.betonnage.toupies_pour_tenir_le_minimum}} toupies suffisent au minimum mais font durer le coulage {{gros-oeuvre.betonnage.options_de_rotation.0.duree_du_coulage_h::n1}} h ; il en faut {{gros-oeuvre.betonnage.toupies_retenues}} pour finir avant la chaleur.

**6. Le planning dit « décoffrage à J+2 ». Est-ce un critère ?**
**Non.** Le critère est une **résistance**, constatée sur éprouvette. Le planning dit quand on l'espère. Confondre les deux est la seule erreur de ce module qui ne se répare pas.

**7. Quand demande-t-on le visa du ferraillage ?**
**La veille**, avec une pré-visite. Le point d'arrêt tombe juste avant le bétonnage, c'est-à-dire au moment où la toupie est commandée et l'équipe en place : structurellement le moment où il coûte le plus cher de dire non, donc celui où il faut l'avoir préparé.

:::

## S8 · Fiche mémo

:::memo
## Fiche mémo — cycle de gros œuvre

**Les trois bornes d'une cadence**

$$ T = \max\left(\underbrace{T_{\text{équipe la plus lente}}}_{\text{moyens}},\ \underbrace{\frac{\sum t_{\text{grue}}}{n_{\text{grues}}}}_{\text{matériel}},\ \underbrace{\frac{I_{\text{immobilisation}}}{\lfloor \text{parc}/S \rfloor}}_{\text{coffrage}}\right) $$

La troisième est celle qu'on oublie, et souvent celle qui borne.

**Les chiffres de ce plancher**

| | |
|---|---:|
| Cycle d'une zone | {{gros-oeuvre.cycle.duree_j::n2}} j |
| Cadence de rotation | {{gros-oeuvre.cycle.cadence_j::n1}} j · bornée par l'{{gros-oeuvre.cycle.ressource_qui_borne}} |
| Immobilisation du coffrage | {{gros-oeuvre.immobilisation_du_coffrage.duree_j::n2}} j, dont {{gros-oeuvre.immobilisation_du_coffrage.part_de_cure_pct::n0}} % de cure |
| **Parc optimal** | **{{gros-oeuvre.parc.optimum.parc_m2}} m²** ({{gros-oeuvre.parc.optimum.zones_simultanees}} zones) — déclaré {{gros-oeuvre.parc.parc_declare_m2}} m² |
| Marge libre du plancher | {{gros-oeuvre.parc.marge_disponible_j::n1}} j |
| Débit minimal à {{gros-oeuvre.betonnage.temperature_de_calcul_C::n0}} °C | {{gros-oeuvre.betonnage.debit_dimensionnant_m3_h::n1}} m³/h |
| **Toupies à commander** | **{{gros-oeuvre.betonnage.toupies_retenues}}** → {{gros-oeuvre.betonnage.duree_du_coulage_h::n1}} h de coulage |
| Démarrage conseillé | {{gros-oeuvre.fenetre_de_coulage.demarrage_conseille}} |

**Les deux contraintes du bétonnage par temps chaud**

Le **minimum** ($\ell L e / t$) interdit la reprise froide. Le **débit tenu** (toupies, plafonné par
la pompe) décide de l'heure de fin. Commander sur le premier, c'est finir dans la chaleur.

**Les six contrôles, coffrage fermé**

Enrobage · recouvrements · propreté du fond · réservations · étaiement et contreventement · bon de
livraison. Après l'arrivée de la première toupie, le coût de dire non est multiplié par le nombre de
camions commandés.

**Points d'arrêt côté maîtrise d'œuvre**

Implantation · ferraillage avant coulage · fermeture de coffrage · autorisation de bétonnage ·
décoffrage. Chacun porte un **critère écrit**. Le décoffrage porte un critère de **résistance**,
jamais un délai. Un visa donné sans être allé voir engage celui qui l'a signé.
:::
