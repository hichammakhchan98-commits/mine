---
id: D4
titre: Suivi et contrôle d'un chantier
fil: Palier 1 · module 3 — direction de projet
resume: Il n'y a pas un avancement mais trois, et ils ne coïncident jamais. Entre ce que le planning prévoit, ce que le chantier fait et ce que l'entreprise déclare, il y a deux écarts qui ne se traitent pas de la même façon.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · toutes les valeurs numériques sont V3 · les taux contractuels se lisent dans le CPS
pied: Exemple pédagogique — ne remplace ni un rapport d'avancement visé, ni un décompte, ni l'avis d'un conseil en cas de réclamation.
donnees: suivi, prix, planification, gare
---

## S1 · Ce que ce module fait, et ce qu'il ne refait pas

C'est le cœur de votre poste. D2 a donné les durées, D1 les prix ; celui-ci les confronte à ce que le
chantier fait réellement, et transforme cet écart en décisions.

Vous connaissez la valeur acquise : CPI, SPI, EAC, les formules. Ce module ne vous les réapprend pas.
Il fait quatre choses que le référentiel générique ne fait pas, et qui décident de la justesse d'un
reporting de chantier :

1. il distingue **trois avancements** — physique, financier, temporel — qui ne coïncident jamais, et
   montre lequel répond à la question « où en est le chantier ? » ;
2. il distingue **trois états** — planifié, constaté, déclaré — et donc **deux écarts** : le premier
   est une dérive qui se pilote, le second un objet de **visa**. Les confondre fait viser une
   situation sur une déclaration ;
3. il montre qu'un **SPI global ne voit pas le chemin critique**, et calcule les deux ;
4. il **calcule** à partir de quel avancement un CPI veut dire quelque chose, au lieu de citer une
   règle d'usage.

**Prérequis** : D2 (réseau, segments de travail, chemin critique) et D1 (bordereau, situation,
courbe de dépense). **Place dans le projet** : étape 8 du déroulé (§ 10.2). D7 consolide ce module
sur plusieurs sites.

## S2 · L'idée centrale : un avancement n'est pas un avancement

Demandez « où en est le chantier ? » et vous recevrez un pourcentage. Demandez **lequel** et la
réunion change de nature. À la date d'arrêt de cet exemple — jour ouvré
{{suivi.date_arret.jour_ouvre::n0}}, soit le mois {{suivi.date_arret.mois::n0}} — les trois répondent
ceci :

| Avancement | Valeur | Ce qu'il mesure |
|---|---:|---|
| **Physique** | **{{suivi.avancements.physique_pct::n1}} %** | la part du budget que les ouvrages exécutés représentent |
| **Financier** | {{suivi.avancements.financier_pct::n1}} % | la part du marché déjà facturée, nette de retenue et d'avance |
| **Temporel** | {{suivi.avancements.temporel_pct::n1}} % | la part du délai écoulée, et rien d'autre |

{{suivi.avancements.lecture}}

:::figure {"fn":"barres","args":"suivi.figures.avancements","titre":"Trois avancements au même instant","num":1,"large":true,"options":{"unite":"% du budget, du marché ou du délai selon la ligne","bande":[0,100],"libelle_bande":"0 à 100 %"},"voir":["Les trois barres ne mesurent pas la même chose, et l'unité de l'axe le dit : un pourcentage n'a de sens qu'avec son dénominateur. C'est pour cela qu'on ne les additionne ni ne les moyenne.","Le physique dépasse le temporel de {{suivi.avancements.ecart_physique_temporel_pts::n1}} points : le chantier a produit plus que le calendrier n'a consommé. C'est normal en début de chantier, où les tâches les plus denses en budget se bousculent.","Le financier est {{suivi.avancements.ecart_physique_financier_pts::n1}} points sous le physique. L'entreprise a construit plus qu'elle n'a encaissé, et l'écart finance le maître d'ouvrage — c'est le besoin de trésorerie du module D1, vu d'un autre angle."],"erreur":"Citer « le chantier est à 25 % » sans dire de quoi. Dans une réunion où trois personnes ont trois chiffres différents, aucune n'a tort : elles ne répondent pas à la même question. Le seul qui mesure l'ouvrage est le physique."}
:::

## S3 · Principes

### a. Trois états, deux écarts, et ils ne se traitent pas pareil

| État | D'où il vient | Qui le produit |
|---|---|---|
| **Planifié** | dérivé du réseau de D2 à la date d'arrêt | le calcul |
| **Constaté** | mesuré sur site, attachement contradictoire | le chantier et la maîtrise d'œuvre, ensemble |
| **Déclaré** | la situation déposée par l'entreprise | l'entreprise seule |

De là, deux écarts qui n'ont rien en commun :

- **planifié → constaté** : la **dérive**. Elle se pilote — moyens, séquence, relance d'un
  fournisseur. C'est le sujet d'une réunion de chantier ;
- **constaté → déclaré** : l'**écart de déclaration**. Il ne se pilote pas, il se **vise**. C'est le
  sujet d'un courrier.

Les confondre produit l'erreur la plus fréquente du suivi : viser une situation sur ce que
l'entreprise déclare, puis s'étonner que l'avancement « reparte en arrière » le mois suivant.

:::encart {"genre":"alerte","titre":"L'avancement planifié se DÉRIVE, il ne se répartit pas"}
À la date d'arrêt, un prorata du temps écoulé donnerait
{{suivi.avancements.temporel_pct::n1}} % pour **toutes** les tâches. Le réseau en donne un tout
autre tableau : les tâches terminées sont à 100, celles qui n'ont pas commencé à 0, et seules
quelques-unes sont entre les deux. L'écart maximal entre les deux lectures dépasse 40 points, et le
test de ce module le vérifie.

C'est la leçon des quinze bloquants de la tranche verticale, appliquée au chantier entier : **une
grandeur d'état se dérive de l'état, elle ne se répartit pas au prorata**. Un prorata partage son
hypothèse avec ce qu'il prétend mesurer ; il ne peut donc rien détecter.
:::

### b. La valeur acquise se valorise sur le CONSTATÉ

$$ VA = \sum_i \text{budget}_i \times \frac{\text{avancement constaté}_i}{100} \qquad CPI = \frac{VA}{CR} \qquad SPI = \frac{VA}{VP} $$

Deux précautions, et chacune a déjà coûté un bloquant à ce cours :

1. **la VA se valorise sur le constaté, jamais sur le déclaré.** Sur ce chantier, valoriser le
   déclaré gonflerait la valeur acquise de plus d'un million de dirhams, et le CPI avec elle. Un
   indice qui se nourrit d'une déclaration mesure la déclaration ;
2. **la VP vient de la courbe de dépense, pas de la courbe de travail.** D2 publie une courbe en S
   en jours-hommes ; elle mesure le travail. D1 en publie une en dirhams. Les deux diffèrent ici de
   plus de vingt points en milieu de chantier, et c'est la seconde qui sert de référence à un indice
   exprimé en dirhams.

### c. Un indice global ne voit pas le chemin critique

Un SPI pondère les écarts par les budgets. Une dérive sur un gros poste non critique l'écrase ; une
dérive sur une petite tâche critique y disparaît. On recalcule donc la même comparaison **en durée**,
restreinte aux tâches qui portent la date.

## S4 · Étude de cas : le point mensuel

Le point du mois {{suivi.date_arret.mois::n0}}, au jour ouvré
{{suivi.date_arret.jour_ouvre::n0}} sur {{suivi.date_arret.duree_totale_j::n0}}.

### a. Ce que le chantier fait, et ce que l'entreprise en dit

:::figure {"fn":"barres","args":"suivi.figures.ecarts","titre":"Dérive constatée par poste, en points d'avancement","num":2,"large":true,"options":{"unite":"points d'écart entre le constaté et le planifié","bande":[-5,5],"libelle_bande":"dérive non significative"},"voir":["Le poste le plus en retard est {{suivi.figures.ecarts.0.libelle}} : {{suivi.figures.ecarts.0.valeur::n0}} points. C'est la fabrication de la charpente, donc un fournisseur — et c'est le genre de dérive qu'un point hebdomadaire sur le gros œuvre ne voit jamais.","Un poste est en AVANCE, et ce n'est pas une bonne nouvelle en soi : avancer une tâche hors du chemin critique consomme des moyens pour un gain de délai nul. C'est l'exercice 2 du module D2, vu depuis le suivi.","La bande grise est la zone où une dérive n'est pas significative : un constat contradictoire se fait à la règle et au décamètre, pas au millimètre. Sortir de la bande est ce qui déclenche une action, pas le signe d'un écart."],"erreur":"Classer les dérives par leur taille. Celle qui compte n'est pas la plus grande, c'est celle qui touche le chemin critique — et sur ce chantier, les deux ne sont pas la même."}
:::

### b. La valeur acquise et les indices

| | Montant |
|---|---:|
| Budget à l'achèvement (BAC) | {{suivi.valeur_acquise.budget_a_l_achevement_BAC_MAD::n0}} MAD |
| Valeur planifiée (VP) | {{suivi.valeur_acquise.valeur_planifiee_VP_MAD::n0}} MAD |
| **Valeur acquise (VA)** | **{{suivi.valeur_acquise.valeur_acquise_VA_MAD::n0}} MAD** |
| Coût réel (CR) | {{suivi.valeur_acquise.cout_reel_CR_MAD::n0}} MAD |
| Écart de coût (CV = VA − CR) | {{suivi.valeur_acquise.ecart_de_cout_CV_MAD::n0}} MAD |
| Écart de délai (SV = VA − VP) | {{suivi.valeur_acquise.ecart_de_delai_SV_MAD::n0}} MAD |
| **CPI** | **{{suivi.valeur_acquise.CPI::n3}}** |
| **SPI** | **{{suivi.valeur_acquise.SPI::n3}}** |

Un CPI de {{suivi.valeur_acquise.CPI::n3}} veut dire qu'un dirham dépensé produit
{{suivi.valeur_acquise.CPI::n2}} dirham d'ouvrage. Ce n'est pas dramatique et ce n'est pas rien :
projeté sur le reste du chantier, cela fait trois façons de prévoir la fin.

| Prévision à terminaison | Montant | Ce qu'elle suppose |
|---|---:|---|
| La dérive **cesse** | {{suivi.valeur_acquise.EAC_si_la_derive_cesse_MAD::n0}} MAD | un aléa ponctuel, une reprise isolée |
| La dérive **persiste** | {{suivi.valeur_acquise.EAC_si_la_derive_persiste_MAD::n0}} MAD | une cause systématique : prix mal estimé, cadence optimiste |
| Dérive **et rattrapage du retard** | {{suivi.valeur_acquise.EAC_cout_et_delai_MAD::n0}} MAD | il faut en plus payer des moyens pour tenir la date |

{{suivi.valeur_acquise.quelle_EAC}}

Et le diagnostic, ici, penche : le module D1 a montré que les cadences du projet sont optimistes d'un
facteur ×{{prix.coherence_cadences.facteur_de_recalage_moyen::n2}}. Une dérive qui vient d'une
hypothèse d'entrée fausse est **systématique** par construction. La deuxième ligne est donc la plus
défendable des trois, et c'est elle qu'on annonce — en disant pourquoi.

:::figure {"fn":"courbeS","args":"suivi.figures.courbe","titre":"Courbe de dépense et point de valeur acquise","num":3,"large":true,"voir":["La courbe tiretée est la dépense PRÉVUE, en dirhams — celle de D1, pas la courbe en jours-hommes de D2. Les deux diffèrent de plus de vingt points en milieu de chantier, et un indice en dirhams se compare à la première.","Le point brique est la valeur acquise constatée, et l'écart coté à côté — en points de pourcentage — est l'écart de délai. C'est la même grandeur que le SV du tableau ci-dessus, dans une autre unité : {{suivi.valeur_acquise.ecart_de_delai_SV_MAD::n0}} MAD rapportés au budget de {{suivi.valeur_acquise.budget_a_l_achevement_BAC_MAD::n0}} MAD. Un écart de quelques points sur une courbe est vite jugé négligeable ; en dirhams il l'est moins.","Un seul point de constat est tracé, et c'est volontaire : relier deux relevés par une courbe donnerait l'illusion d'une tendance là où il n'y a qu'une paire de mesures."],"erreur":"Lire l'écart vertical comme un retard en jours. Il est en dirhams. Pour le convertir en temps, il faut le reporter sur la courbe prévue et lire la date correspondante — et cette conversion suppose que le reste du chantier suivra le rythme prévu, ce que rien ne garantit."}
:::

### c. Le SPI ne dit pas ce qu'on croit

| | Avancement constaté | Avancement planifié | Indice |
|---|---:|---:|---:|
| **Global**, en durée | {{suivi.spi_du_chemin.avancement_global_constate_pct::n1}} % | {{suivi.spi_du_chemin.avancement_global_planifie_pct::n1}} % | **{{suivi.spi_du_chemin.SPI_en_duree_global::n3}}** |
| **Chemin critique**, en durée | {{suivi.spi_du_chemin.avancement_du_chemin_constate_pct::n1}} % | {{suivi.spi_du_chemin.avancement_du_chemin_planifie_pct::n1}} % | **{{suivi.spi_du_chemin.SPI_en_duree_du_chemin::n3}}** |

**{{suivi.spi_du_chemin.ecart_pts::n1}} points d'écart entre les deux indices**, et ils ne pointent
pas dans le même sens. L'indice global est le plus pessimiste : il porte toute la dérive de la
fabrication de charpente, {{suivi.etats.planifie.CHFA::n0}} % prévus contre
{{suivi.etats.constate.CHFA::n0}} % constatés. Or **cette tâche n'est pas sur le chemin critique** de
ce chantier — elle dispose de {{planification.durees.CHFA.marge_totale_j::n0}} jours de marge, et son
retard y est absorbé.

:::encart {"genre":"voir","titre":"Pourquoi c'est contre-intuitif, et pourquoi il faut le calculer"}
Le réflexe est de penser l'inverse : un indice global **rassurant** qui masquerait une dérive
critique. Cela arrive, et c'est le danger qu'on enseigne. Mais sur ce chantier précis, c'est la
situation symétrique qui se produit : l'indice global **sur-alarme**, parce que la dérive la plus
visible est absorbée par une marge.

Les deux cas existent, et aucun des deux ne se devine : un indice global et un indice de chemin
critique répondent à deux questions différentes, et il faut les calculer tous les deux. Le premier
dit si le chantier produit ce qui était prévu ; le second, et lui seul, dit si la **date** tient.

Et sur ce chantier, une raison de plus de se méfier du global : une tâche en avance hors du chemin
ne rattrape rien. Le levage au-dessus de la voie est épinglé au jour
{{planification.consignations.CHLV.debut::n0}} par sa fenêtre de consignation — tout ce qui le
précède attend de toute façon.
:::

:::figure {"fn":"barres","args":"suivi.figures.indices","titre":"Quatre indices de performance au même instant","num":4,"large":true,"options":{"unite":"indice (1,00 = conforme au prévu)","bande":{"$":"suivi.figures.indices_bande"},"libelle_bande":"conforme","origine":{"$":"suivi.figures.indices_origine"}},"voir":["Le CPI et le SPI ne se lisent pas sur la même assiette : le premier compare des dirhams produits à des dirhams dépensés, le second des dirhams produits à des dirhams prévus. Les mettre côte à côte est utile ; les moyenner ne veut rien dire.","Les deux SPI de durée encadrent la question du délai. Celui du chemin critique, {{suivi.spi_du_chemin.SPI_en_duree_du_chemin::n3}}, est le seul qui engage une date.","{{suivi.figures.indices_hors_bande.length}} indices sur {{suivi.figures.indices.length}} sont hors de la bande de conformité — {{suivi.figures.indices_hors_bande.0}} et {{suivi.figures.indices_hors_bande.1}} — et pourtant aucun n'est alarmant isolément. L'axe ne part pas de zéro, et c'est volontaire : à cette échelle, quatre barres parties de zéro auraient toutes la même longueur et la figure ne montrerait rien."],"erreur":"Piloter sur un indice unique. Un tableau de bord à un chiffre est un tableau de bord qui cache trois questions — le coût, le volume produit, et la date — dont une seule intéresse le maître d'ouvrage au moment de la réception."}
:::

### d. À partir de quand un CPI veut-il dire quelque chose ?

Un CPI calculé à 5 % d'avancement ne mesure pas le chantier : il mesure la comptabilité analytique.
Plutôt que de citer une règle d'usage, on la fabrique — on simule un chantier qui dérive d'un taux
constant de {{suivi.fiabilite_du_cpi.derive_simulee_pct::n0}} %, on y ajoute le bruit d'un relevé de
coût imprécis (ici un mois de frais de chantier mal imputé, soit
{{suivi.fiabilite_du_cpi.bruit_suppose_MAD::n0}} MAD), et on regarde quand le CPI calculé se
distingue du bruit.

| Avancement | Incertitude sur le CPI | Lisible ? |
|---:|---:|---|
| {{suivi.fiabilite_du_cpi.points.0.avancement_pct::n1}} % | {{suivi.fiabilite_du_cpi.points.0.incertitude_pts::n1}} points | non |
| {{suivi.fiabilite_du_cpi.points.2.avancement_pct::n1}} % | {{suivi.fiabilite_du_cpi.points.2.incertitude_pts::n1}} points | non |
| **{{suivi.fiabilite_du_cpi.avancement_ou_le_CPI_devient_lisible_pct::n1}} %** | — | **oui, à partir d'ici** |
| {{suivi.fiabilite_du_cpi.points.9.avancement_pct::n1}} % | {{suivi.fiabilite_du_cpi.points.9.incertitude_pts::n1}} points | oui |

{{suivi.fiabilite_du_cpi.lecture}}

{{suivi.fiabilite_du_cpi.ce_que_ce_calcul_ne_prouve_pas}}

### e. Le visa de la situation, côté maîtrise d'œuvre

L'entreprise dépose une situation sur son **déclaré**. La maîtrise d'œuvre la vise sur le
**constaté**. L'écart, ici, fait {{suivi.visa.montant_retire_MAD::n0}} MAD, soit
{{suivi.visa.reduction_pct::n1}} % de la situation.

| Poste | Déclaré | Constaté | Écart | À retirer |
|---|---:|---:|---:|---:|
| {{suivi.visa.lignes_reduites.0.poste}} · {{suivi.visa.lignes_reduites.0.libelle}} | {{suivi.visa.lignes_reduites.0.declare_pct::n1}} % | {{suivi.visa.lignes_reduites.0.constate_pct::n1}} % | {{suivi.visa.lignes_reduites.0.ecart_pts::n1}} pts | {{suivi.visa.lignes_reduites.0.ecart_MAD::n0}} MAD |
| {{suivi.visa.lignes_reduites.1.poste}} · {{suivi.visa.lignes_reduites.1.libelle}} | {{suivi.visa.lignes_reduites.1.declare_pct::n1}} % | {{suivi.visa.lignes_reduites.1.constate_pct::n1}} % | {{suivi.visa.lignes_reduites.1.ecart_pts::n1}} pts | {{suivi.visa.lignes_reduites.1.ecart_MAD::n0}} MAD |
| {{suivi.visa.lignes_reduites.2.poste}} · {{suivi.visa.lignes_reduites.2.libelle}} | {{suivi.visa.lignes_reduites.2.declare_pct::n1}} % | {{suivi.visa.lignes_reduites.2.constate_pct::n1}} % | {{suivi.visa.lignes_reduites.2.ecart_pts::n1}} pts | {{suivi.visa.lignes_reduites.2.ecart_MAD::n0}} MAD |
| | | | **Total** | **{{suivi.visa.montant_retire_MAD::n0}} MAD** |

Net déclaré {{suivi.visa.net_declare_MAD::n0}} MAD → **net visé
{{suivi.visa.net_vise_MAD::n0}} MAD**.

**Les six contrôles d'un visa**, dans cet ordre, parce que chacun conditionne le suivant :

1. l'**attachement est signé** avant la situation — seul contrôle non calculable, et le plus
   important : il se vérifie sur la pièce ;
2. les **quantités déclarées** correspondent au constat ;
3. **a + b + c = 1** dans la formule de révision ;
4. la **retenue de garantie** porte sur le montant **révisé**, et non sur le montant initial ;
5. la retenue cumulée reste sous son **plafond** ;
6. le **remboursement d'avance** a démarré au taux d'avancement prévu.

{{suivi.visa.double_lecture.maitrise_d_oeuvre}}

**Côté entreprise.** {{suivi.visa.double_lecture.entreprise}}

{{suivi.visa.avertissement_CPS}}

### f. Une modification en cours de route

{{suivi.modification.objet}}.

| | Montant |
|---|---:|
| Travaux supplémentaires | {{suivi.modification.montant_des_travaux_MAD::n0}} MAD |
| Délai supplémentaire | {{suivi.modification.delai_supplementaire_j::n0}} jours ouvrés |
| Frais indexés sur la durée, qui courent pendant ces jours | {{suivi.modification.frais_indexes_sur_la_duree_MAD::n0}} MAD |
| **Coût complet** | **{{suivi.modification.cout_complet_MAD::n0}} MAD** |
| Nouveau budget à l'achèvement | {{suivi.modification.nouveau_BAC_MAD::n0}} MAD |
| Nouvelle prévision à terminaison | {{suivi.modification.nouvelle_EAC_MAD::n0}} MAD |

{{suivi.modification.lecture}}

Et l'autre côté de la table : **refuser le délai coûte plus cher que l'accorder**. Sans les
{{suivi.modification.delai_supplementaire_j::n0}} jours, le chantier les prend quand même et paie
{{suivi.modification.si_le_delai_n_est_pas_accorde_MAD::n0}} MAD de frais et de pénalités — contre
{{suivi.modification.frais_indexes_sur_la_duree_MAD::n0}} MAD si le délai est accordé. C'est un
argument qui se pose sur la table avec son calcul, et il vaut mieux que « nous demandons un délai ».

{{suivi.modification.regle}}

## S4b · Les hypothèses de ce suivi, déclarées

Tout ce qui décrit l'**état du chantier** à la date d'arrêt est fabriqué pour la démonstration : il
n'existe aucun attachement réel dans ce cours.

⟦V3|date d'arrêt du suivi|84 jours ouvrés|j|0 à 363|2026|le 4e mois ; date choisie pour que plusieurs tâches soient en cours, dont une sur le chemin critique⟧,
⟦V3|dérive constatée de la fabrication de charpente|−18 points|points|−30 à 0|2026|retard du fournisseur, constaté contradictoirement⟧,
⟦V3|dérive constatée du plancher de mezzanine|−6 points|points|−15 à 0|2026|une zone en retard de cycle⟧,
⟦V3|dérive constatée de l'étanchéité et des remblais|−12 points|points|−20 à 0|2026⟧,
⟦V3|dérive constatée des noyaux et escaliers|−8 points|points|−15 à 0|2026⟧,
⟦V3|dérive constatée du passage souterrain|+4 points|points|0 à 10|2026|en avance, et hors chemin critique : un gain de délai nul⟧,
⟦V3|optimisme déclaré sur le plancher de mezzanine|+6 points|points|0 à 10|2026|ce que l'entreprise déclare au-delà du constat⟧,
⟦V3|optimisme déclaré sur la fabrication de charpente|+10 points|points|0 à 15|2026⟧,
⟦V3|optimisme déclaré sur l'étanchéité|+7 points|points|0 à 12|2026⟧,
⟦V3|coût réel imputé à la date d'arrêt|23500000 MAD|MAD|20000000 à 27000000|2026|issu des attachements et de la comptabilité analytique ; posé à partir de l'ordre de grandeur de la valeur acquise, majoré de quelques pour cent, AVANT de regarder le CPI⟧,
⟦V3|bruit sur le coût réel|1 mois de frais de chantier|mois|1 à 1|2026|ordre de grandeur de l'imprécision d'une comptabilité analytique en cours de chantier ; sert à dater la lisibilité du CPI⟧,
⟦V3|montant des travaux supplémentaires|1200000 MAD|MAD|700000 à 1900000|2026|renforcement des massifs de grue mobile⟧,
⟦V3|délai supplémentaire de la modification|15 jours|j|8 à 25|2026|la tâche touchée est sur le chemin critique : le délai se répercute entier⟧.

## S4c · Sécurité : ce qu'un reporting décide sans le dire

Ce module ne prescrit aucune opération, mais la façon dont on mesure l'avancement **décide** de la
pression qui s'exerce sur le chantier. Le § 3.4 impose de le dire. Les dispositions ci-dessous sont
**essentielles et non exhaustives** ; elles ne remplacent ni le plan de sécurité du chantier, ni les
obligations réglementaires du marché. **Aucune valeur normative n'est donnée** (§ 5.0).

| Ce que le suivi décide | Le risque | Disposition essentielle |
|---|---|---|
| Le **rythme du reporting** sur un indicateur de production | on produit pour le tableau de bord, pas pour l'ouvrage | un indicateur d'avancement n'est jamais publié seul : il va avec son indicateur sécurité et son indicateur qualité |
| La **pression de rattrapage** quand le SPI décroche | heures supplémentaires, co-activité, travail de nuit | un plan de rattrapage se chiffre **aussi** en risque : il passe par le même visa que le reste |
| Le **constat contradictoire** sur ouvrage en cours | on constate en montant sur un ouvrage non étayé ou non protégé | un constat se prépare : accès, protections, consignation si l'ouvrage est en interface avec la voie |
| La **levée d'un point d'arrêt** sous contrainte de situation | on lève pour pouvoir facturer | un point d'arrêt se lève sur un essai, pas sur un calendrier de paiement |

**Le lien avec tout ce module.** Le § S4e montre qu'un visa retire
{{suivi.visa.montant_retire_MAD::n0}} MAD à une situation. Ce refus est légitime et il a un effet de
bord : l'entreprise cherchera à avancer plus vite le mois suivant. **Un visa bien fait s'accompagne
d'une date de reconstat**, pas seulement d'une réduction — sans quoi la réduction se transforme en
pression sur le chantier, et la pression se transforme en risque.

## S5 · Erreurs fréquentes, et ce qu'elles coûtent

| Erreur | Comment elle se voit | Ce qu'elle coûte |
|---|---|---|
| Un seul « avancement » cité en réunion | trois personnes ont trois chiffres et personne n'a tort | des décisions prises sur le mauvais dénominateur |
| Avancement planifié calculé au prorata du temps | toutes les tâches au même pourcentage | un écart qui ne peut rien détecter : il partage son hypothèse avec ce qu'il mesure |
| Valeur acquise valorisée sur le **déclaré** | le CPI s'améliore au moment où la situation est déposée | ici, plus d'un million de dirhams de VA fictive |
| VP prise sur la courbe en jours-hommes | les indices bougent sans que rien ne bouge sur le chantier | plus de vingt points d'écart en milieu de chantier |
| Pilotage sur le SPI global seul | le tableau de bord est rouge, la date tient — ou l'inverse | {{suivi.spi_du_chemin.ecart_pts::n1}} points d'écart ici, et dans le sens qu'on n'attendait pas |
| CPI annoncé trop tôt | une alerte sur les deux premières situations | on mesure la comptabilité analytique, pas le chantier |
| Situation visée sans attachement signé | la quantité payée n'a pas de constat | un litige au décompte final, et il se gagne sur la pièce |
| Avenant chiffré sur les seuls travaux | le délai n'y figure pas | {{suivi.modification.part_cachee_pct::n1}} % du coût réel de la modification |
| EAC choisie sans diagnostic | on prend la formule la plus douce | une prévision qu'on révisera tous les mois, donc à laquelle personne ne croira |

## S6 · Exercices

:::exercice {"titre":"1 · Trois avancements, trois réponses","niveau":"application"}
À la date d'arrêt, le chantier est à {{suivi.avancements.physique_pct::n1}} % physique,
{{suivi.avancements.financier_pct::n1}} % financier et
{{suivi.avancements.temporel_pct::n1}} % temporel. Le maître d'ouvrage vous demande : « on est à
combien ? ». Que répondez-vous, et pourquoi pas les deux autres ?

**Corrigé.** « **{{suivi.avancements.physique_pct::n1}} % d'ouvrage exécuté**, pour
{{suivi.avancements.temporel_pct::n1}} % du délai consommé. » C'est le physique qui répond à la
question, parce que c'est le seul qui mesure de l'ouvrage.

Les deux autres répondent à d'autres questions, qu'il faut poser avant de les citer. Le **financier**
({{suivi.avancements.financier_pct::n1}} %) répond à « combien a-t-on payé ? » — il est plus bas que
le physique parce que la retenue de garantie et le remboursement d'avance s'y soustraient, et il
intéresse le service comptable, pas la réunion de chantier. Le **temporel**
({{suivi.avancements.temporel_pct::n1}} %) ne mesure que le calendrier : il serait identique sur un
chantier à l'arrêt.

*Le piège : citer le temporel parce qu'il est le plus facile à calculer. Sur ce chantier il est le
plus bas des trois, ce qui donnerait une impression de retard là où le chantier est en avance de
{{suivi.avancements.ecart_physique_temporel_pts::n1}} points sur sa production.*
:::

:::exercice {"titre":"2 · Lire deux SPI qui ne disent pas la même chose","niveau":"probleme"}
Le SPI global en durée vaut {{suivi.spi_du_chemin.SPI_en_duree_global::n3}}, celui du chemin critique
{{suivi.spi_du_chemin.SPI_en_duree_du_chemin::n3}}. Votre directeur veut savoir si la date tient.
Que lui dites-vous, et quelle action proposez-vous ?

**Corrigé.** « **La date tient mieux que le tableau de bord ne le suggère.** L'indice global est tiré
vers le bas par la fabrication de charpente, {{suivi.etats.constate.CHFA::n0}} % constatés contre
{{suivi.etats.planifie.CHFA::n0}} % prévus — mais cette tâche dispose de
{{planification.durees.CHFA.marge_totale_j::n0}} jours de marge et son retard y est absorbé. Sur les
tâches qui portent réellement la date, l'indice est de
{{suivi.spi_du_chemin.SPI_en_duree_du_chemin::n3}}. »

**L'action n'est pourtant pas « ne rien faire »**, et c'est le second temps du raisonnement : une
marge consommée n'est plus disponible. La charpente a mangé une partie de la sienne ; si elle
continue au même rythme, elle deviendra critique. L'action est donc de **relancer le fournisseur
maintenant**, pendant que le retard est encore gratuit, et de suivre la marge restante comme un
indicateur à part entière.

*Le piège, dans les deux sens : conclure « tout va bien » d'un bon indice de chemin critique, ou
déclencher un plan de rattrapage coûteux sur un mauvais indice global. Les deux indices se lisent
ensemble, et aucun ne se lit sans la marge.*
:::

:::exercice {"titre":"3 · Choisir une prévision à terminaison","niveau":"probleme"}
Trois EAC sont calculées : {{suivi.valeur_acquise.EAC_si_la_derive_cesse_MAD::n0}},
{{suivi.valeur_acquise.EAC_si_la_derive_persiste_MAD::n0}} et
{{suivi.valeur_acquise.EAC_cout_et_delai_MAD::n0}} MAD. Laquelle annoncez-vous, et sur quel argument ?

**Corrigé.** La **deuxième** — {{suivi.valeur_acquise.EAC_si_la_derive_persiste_MAD::n0}} MAD — et
l'argument n'est pas dans la formule, il est dans le **diagnostic de la cause**.

Si la dérive venait d'un aléa ponctuel — une reprise, une intempérie — la première serait la bonne :
ce qui est passé est passé, le reste se fera au budget. Mais le module D1 a montré que les cadences
du projet sont optimistes d'un facteur ×{{prix.coherence_cadences.facteur_de_recalage_moyen::n2}}, et
qu'elles portent **toutes** les durées et tous les prix. Une dérive qui vient d'une hypothèse
d'entrée fausse est systématique par construction : elle ne cessera pas.

La troisième suppose en plus qu'on paiera des moyens pour rattraper le retard. Ce n'est pas la
prévision, c'est le **coût d'une décision** — elle s'annonce comme telle, le jour où la décision se
pose.

*Ce qu'on vise : une EAC qui change tous les mois n'est pas une prévision, c'est un thermomètre.
Annoncez celle que votre diagnostic soutient, écrivez le diagnostic à côté, et ne la révisez que
quand le diagnostic change.*
:::

:::exercice {"titre":"4 · Trouver les erreurs dans ce point mensuel","niveau":"revue critique"}
Un conducteur de travaux vous remet ce point mensuel :

> « Chantier à 23 % — nous avons consommé 23 % du délai. CPI 1,02, tout va bien côté coût.
> L'avancement est calculé au prorata : 4 mois sur 17, soit 23 % sur chaque tâche. La situation du
> mois est de {{prix.situation.net_cumule_a_payer_MAD::n0}} MAD, conforme à notre métré. Nous
> proposons de passer le point mensuel au trimestre, le chantier étant stable. »

**Cinq choses ne vont pas. Lesquelles ?**

**Corrigé.**

1. **« 23 % » est l'avancement temporel**, présenté comme l'avancement du chantier. Le physique est à
   {{suivi.avancements.physique_pct::n1}} % : le chantier est en **avance** de
   {{suivi.avancements.ecart_physique_temporel_pts::n1}} points sur sa production, et le point mensuel
   annonce l'inverse.
2. **L'avancement au prorata est faux par construction.** Mettre 23 % sur chaque tâche donne 23 % à
   des tâches terminées et 23 % à des tâches jamais commencées. Un avancement se **dérive** de l'état
   du réseau — et surtout, un prorata ne peut rien détecter, puisqu'il partage son hypothèse avec ce
   qu'il prétend mesurer.
3. **Un CPI de 1,02 à ce stade ne veut rien dire — sauf qu'ici il veut dire quelque chose.** Le § S4d
   montre que le CPI devient lisible à partir de
   {{suivi.fiabilite_du_cpi.avancement_ou_le_CPI_devient_lisible_pct::n1}} % d'avancement ; à
   {{suivi.avancements.physique_pct::n1}} % physique, on y est. Le vrai défaut est ailleurs : le CPI
   réel est de {{suivi.valeur_acquise.CPI::n3}}, pas 1,02. Un CPI calculé sur un avancement au
   prorata est un CPI faux.
4. **« Conforme à notre métré » n'est pas le critère.** La situation se vise sur l'**attachement
   contradictoire**, pas sur le métré d'étude. Ici le visa retire
   {{suivi.visa.montant_retire_MAD::n0}} MAD sur {{suivi.visa.lignes_reduites.length}} postes.
5. **Passer au trimestre est l'inverse de ce que la situation demande.** Le SPI est à
   {{suivi.valeur_acquise.SPI::n3}} et une tâche a consommé une partie de sa marge. On espace un
   reporting quand les indices sont stables **et** que la marge ne se consomme pas — pas quand on
   manque d'information.

*Ce qu'on vise : rien. Et on demande trois choses — l'avancement physique par poste, les
attachements signés, et la marge restante sur les tâches qui ont dérivé.*
:::

## S7 · Check-list, glossaire et quiz

**Check-list d'un point mensuel**

1. Les **trois avancements** sont-ils publiés, chacun avec son dénominateur ?
2. L'avancement planifié est-il **dérivé du réseau**, ou réparti au prorata du temps ?
3. La valeur acquise est-elle valorisée sur le **constaté**, pas sur le déclaré ?
4. La valeur planifiée vient-elle de la courbe de **dépense**, pas de celle du travail ?
5. Le **SPI du chemin critique** est-il calculé à côté du SPI global ?
6. L'avancement est-il suffisant pour que le **CPI** veuille dire quelque chose ?
7. La **marge restante** des tâches qui ont dérivé est-elle suivie comme un indicateur ?
8. Le **visa** de la situation porte-t-il un chiffre et un motif par poste réduit ?
9. Les **modifications** sont-elles chiffrées en trois lignes : travaux, délai, effet sur l'EAC ?
10. L'**EAC** annoncée est-elle accompagnée du diagnostic qui la soutient ?

**Glossaire**

| | |
|---|---|
| **VA · valeur acquise** | le budget des ouvrages réellement exécutés, valorisé sur le constaté |
| **VP · valeur planifiée** | le budget de ce qui devait être exécuté à cette date |
| **CR · coût réel** | ce qui a été dépensé, issu de la comptabilité analytique |
| **CPI** | VA / CR — ce qu'un dirham dépensé produit d'ouvrage |
| **SPI** | VA / VP — ce qui est produit rapporté à ce qui était prévu |
| **EAC · prévision à terminaison** | le coût final prévu, qui dépend du diagnostic sur la dérive |
| **Avancement planifié** | l'état que le réseau prévoit à une date — dérivé, jamais réparti |
| **Avancement constaté** | l'état mesuré contradictoirement sur site |
| **Avancement déclaré** | ce que l'entreprise porte dans sa situation ; il se vise |
| **Attachement** | le constat contradictoire signé. C'est lui qui fait foi |
| **Point d'arrêt** | une étape que l'exécution ne franchit pas sans accord écrit |
| **Ordre de service** | l'acte par lequel le maître d'ouvrage prescrit, y compris une modification |

:::exercice {"titre":"Sept questions pour vérifier","niveau":"application"}
**1. « Le chantier est à 30 % ». Quelle question posez-vous ?**
**30 % de quoi ?** Physique, financier ou temporel — trois dénominateurs, trois réponses différentes au même instant. Ici, {{suivi.avancements.physique_pct::n1}} / {{suivi.avancements.financier_pct::n1}} / {{suivi.avancements.temporel_pct::n1}} %.

**2. Pourquoi ne calcule-t-on pas l'avancement planifié au prorata du temps écoulé ?**
Parce qu'il serait identique pour toutes les tâches, y compris celles qui sont finies et celles qui n'ont pas commencé — et surtout parce qu'un prorata **partage son hypothèse** avec ce qu'il mesure : il ne peut rien détecter. L'avancement se dérive des segments de travail du réseau.

**3. Sur quel état valorise-t-on la valeur acquise ?**
Le **constaté**. Valoriser le déclaré ferait monter le CPI au moment où l'entreprise dépose sa situation : un indice qui se nourrit d'une déclaration mesure la déclaration.

**4. Votre SPI global est à {{suivi.spi_du_chemin.SPI_en_duree_global::n2}}. La date est-elle en danger ?**
**On ne peut pas le dire avec ce chiffre.** Un indice global pondère par les budgets et ne voit pas le chemin critique. Ici celui du chemin vaut {{suivi.spi_du_chemin.SPI_en_duree_du_chemin::n3}} : la date tient mieux que le tableau de bord. Mais une marge consommée n'est plus disponible — c'est elle qu'il faut suivre.

**5. À partir de quel avancement un CPI devient-il un indicateur ?**
Quand l'incertitude sur le coût réel passe sous la dérive qu'on cherche. Ici, {{suivi.fiabilite_du_cpi.avancement_ou_le_CPI_devient_lisible_pct::n1}} % d'avancement — et ce seuil dépend du bruit supposé, pas d'une règle universelle.

**6. Laquelle des trois EAC annoncez-vous ?**
Celle que **le diagnostic de la cause** soutient. Dérive accidentelle → la dérive cesse. Cause systématique (hypothèse d'entrée fausse) → elle persiste. Et on écrit le diagnostic à côté du chiffre.

**7. Un avenant de 1,2 MMAD avec 15 jours de délai. Combien coûte-t-il vraiment ?**
{{suivi.modification.cout_complet_MAD::n0}} MAD, parce que les {{suivi.modification.delai_supplementaire_j::n0}} jours font courir {{suivi.modification.frais_indexes_sur_la_duree_MAD::n0}} MAD de frais de chantier que l'avenant ne mentionne pas — {{suivi.modification.part_cachee_pct::n1}} % du coût réel. Et refuser le délai coûterait {{suivi.modification.si_le_delai_n_est_pas_accorde_MAD::n0}} MAD.

:::

## S8 · Fiche mémo

:::memo
## Fiche mémo — suivre et contrôler un chantier

**Trois avancements, trois dénominateurs**

| | Mesure | Ici |
|---|---|---:|
| Physique | ouvrages exécutés / budget | {{suivi.avancements.physique_pct::n1}} % |
| Financier | net facturé / marché | {{suivi.avancements.financier_pct::n1}} % |
| Temporel | délai écoulé / délai total | {{suivi.avancements.temporel_pct::n1}} % |

**Trois états, deux écarts**

Planifié →(dérive, **se pilote**)→ Constaté →(déclaration, **se vise**)→ Déclaré

**Les indices de ce chantier**

| | |
|---|---:|
| CPI | {{suivi.valeur_acquise.CPI::n3}} |
| SPI (valeur) | {{suivi.valeur_acquise.SPI::n3}} |
| SPI en durée, global | {{suivi.spi_du_chemin.SPI_en_duree_global::n3}} |
| **SPI en durée, chemin critique** | **{{suivi.spi_du_chemin.SPI_en_duree_du_chemin::n3}}** |
| EAC retenue (dérive systématique) | {{suivi.valeur_acquise.EAC_si_la_derive_persiste_MAD::n0}} MAD |
| Retiré au visa | {{suivi.visa.montant_retire_MAD::n0}} MAD ({{suivi.visa.reduction_pct::n1}} %) |
| CPI lisible à partir de | {{suivi.fiabilite_du_cpi.avancement_ou_le_CPI_devient_lisible_pct::n1}} % d'avancement |

**Les six contrôles d'un visa de situation**

Attachement signé · quantités contre constat · a+b+c=1 · retenue sur le **révisé** · plafond de
retenue · remboursement d'avance démarré. Chaque refus porte **un chiffre et un motif**.

**Les huit réflexes**

1. Toujours dire de **quoi** est le pourcentage.
2. Dériver l'avancement planifié du réseau, jamais le répartir.
3. Valoriser la VA sur le **constaté**.
4. Prendre la VP sur la courbe de **dépense**.
5. Calculer les **deux** SPI, et suivre la **marge** à côté.
6. Ne pas conclure d'un CPI avant qu'il soit lisible.
7. Chiffrer une modification en **trois** lignes.
8. Annoncer une EAC avec son **diagnostic**.

**Points d'arrêt côté maîtrise d'œuvre**

Un point d'arrêt se lève sur un **essai**, jamais sur un calendrier de paiement. Un visa qui réduit
s'accompagne d'une **date de reconstat** : sinon la réduction devient une pression, et la pression
devient un risque.
:::
