---
id: C6
titre: Matériel — l'heure d'un engin, et ce qu'elle décide
fil: Palier 1 · module 14 — exécution, fiche d'expert
resume: Ce qui décide entre louer et acheter n'est ni l'engin ni la durée du chantier : c'est l'unité dans laquelle on paie. Trois engins de cette gare, trois régimes de location, et un coût par heure de travail qui va de 520 à 1 364 MAD pour le même marché. Celui qu'on paie à la présence coûte 857 629 MAD et n'a aucune ligne au bordereau.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · niveau [M], fiche d'expert compressée · aucune vérification réglementaire d'engin, aucun contrôle périodique n'est chiffré
pied: Exemple pédagogique — ne remplace ni une consultation de loueurs, ni un calcul de prix de revient d'entreprise, ni le plan HSE. Les vérifications réglementaires des appareils de levage et des engins ne sont pas traitées ici.
donnees: materiel, gare, planification
---

## S1 · Ce que ce module ajoute, et ce qu'il ne refait pas

Vous savez choisir un engin. Cette fiche ne vous apprendra pas ce qu'est une pelle. Elle traite la
seule question de matériel qu'un chef de projet suivi tranche vraiment, et qu'aucun module de ce
cours n'avait encore ouverte : **combien coûte l'heure de cet engin, et pourquoi.**

Trois modules ont déjà parlé de matériel, et aucun n'a calculé cela. **C1** pose la grue à tour : sa
courbe de charge, son calage, sa fenêtre d'emploi. **C3** loue le parc de coffrage et en cherche
l'optimum. **D1** facture des locations dans ses sous-détails. Personne n'avait comparé le coût de
**possession** d'un engin à son **prix de location**, ni regardé dans quelle **unité** ce prix est
facturé. C'est tout le sujet, et il tient en une phrase :

:::encart {"genre":"alerte","titre":"La phrase du module"}
Ce qui décide entre louer et acheter n'est ni l'engin, ni la durée du chantier, ni même le nombre
d'heures : c'est l'**unité dans laquelle on paie**. Trois régimes coexistent sur ce chantier, et à
heures de travail égales ils ne coûtent pas du tout la même chose.
:::

Ce module ne refait donc **ni la grue** (C1), **ni le parc de coffrage** (C3), **ni la demande de
grue jour par jour** (D2). Il prend trois familles dont personne n'avait calculé l'heure — la
**pompe à béton**, la **pelle 30 t**, le **chariot télescopique** — et il les mène jusqu'au verdict.
Il ne dit rien non plus des **vérifications réglementaires** des engins et des appareils de levage,
de leur périodicité et de leurs rapports : c'est réglementaire, cela relève du plan HSE, et cela
reste **⏸**.

## S2 · L'idée centrale : deux droites qui se croisent, et il faut savoir de quel côté

Posséder un engin coûte deux choses de nature différente. Une part **fixe** $F$, qui tombe que
l'engin travaille ou non : amortissement, entretien programmé, capital immobilisé. Une part
**variable** $v$, par heure travaillée : carburant et conducteur. Le coût annuel de possession est
donc une droite en heures de travail :

$$ \text{poss}(h) = F + v\,h $$

**Et la location en est une aussi** — c'est le point que tout le monde manque :

$$ \text{loc}(h) = L_0 + L_1\,h $$

où $L_0$ est ce qu'on paie **sans travailler** et $L_1$ ce que coûte l'heure marginale. L'écart des
deux est alors une droite, et son seuil est immédiat :

$$ \text{écart}(h) = (F - L_0) + (v - L_1)\,h \qquad\Longrightarrow\qquad h_0 = \frac{L_0 - F}{v - L_1} $$

:::encart {"genre":"alerte","titre":"Le seuil ne suffit pas : il faut son SENS"}
Le signe de $v - L_1$ décide **de quel côté du seuil** la possession gagne, et c'est là que
l'énoncé des manuels se renverse :

- **$v < L_1$** — la possession coûte moins cher à l'heure marginale. Elle gagne **au-dessus** du
  seuil. C'est le cas classique, celui qu'on enseigne, et celui des régimes où la location est
  proportionnelle aux heures.
- **$v > L_1$** — la location est devenue un **coût fixe** (régime « par durée de présence » : on
  paie du calendrier). La possession gagne alors **au-dessous** du seuil. Un engin **peu employé**
  mais loué à la présence se **possède**, et c'est exactement le contraire de ce qu'on croit savoir.

Ce cours l'a appris en se trompant : la première version de ce module calculait
$h^\star = F/(\ell - v)$ avec $\ell$ pris au point de fonctionnement — exact quand $L_0 = 0$, faux
sinon, et invisible parce que les deux formules coïncident sur deux des trois régimes. Ce qui l'a vu :
la **figure 1**, qui évalue les deux coûts directement et ne croisait pas zéro là où le seuil
l'annonçait. Une figure est une exécution du modèle ; elle le contrôle (D-067).
:::

Le coût **horaire** de possession, lui, est bien l'hyperbole qu'on attend : $F/h + v$. Et il explique
le chiffre le plus brutal de la fiche — la pompe de ce chantier, employée
{{materiel.verdicts.0.heures_par_an_h::n1}} heures par an, coûterait
**{{materiel.verdicts.0.possession_MAD_h::k}} MAD l'heure** si on la possédait. Une part fixe divisée
par presque rien.

:::encart {"genre":"piege","titre":"Ce que « l'engin est amorti » veut dire, et ne veut pas dire"}
« Il est amorti » signifie que la part fixe a cessé d'être comptabilisée, pas qu'elle a cessé
d'exister. L'entretien et le capital restent ; la revente que vous n'encaissez pas est un coût. Un
engin amorti et peu employé reste un engin dont l'heure coûte cher — et la comptabilité, qui a fini
de l'écrire, est la dernière à vous le dire.
:::

### Le plafond, qui clôt la question sans aucune estimation

Avant d'estimer un emploi, regardez où tombe le seuil. L'année ne contient que
{{materiel.verdicts.0.jours_ouvres_par_an_j::n0}} jours ouvrés
⟦V3|jours ouvrés annuels d'un engin|250 j|j ouvrés/an|230 à 260|2026|congés et jours fériés déduits ; sert à convertir une fenêtre d'emploi en années, jamais à planifier⟧,
et à l'intensité d'emploi d'un engin donné cela **plafonne ses heures**. Si le seuil est au-delà du
plafond, **un seul côté du seuil est atteignable** : la question est tranchée, sans estimer quoi que
ce soit, et le camp qui gagne est celui du **sens**.

C'est le cas des **trois** engins de ce chantier, et c'est le résultat le plus rentable de la fiche —
trois décisions en trente secondes chacune, dont une qui va contre l'intuition.

## S3 · Les trois régimes de location, et pourquoi ils décident

Un prix de location ne se compare à rien tant qu'on ne sait pas **ce qu'il compte**. Sur ce chantier,
trois régimes coexistent :

| Régime | Ce que le loueur facture | L'engin de la gare |
|---|---|---|
| **Par intervention** | la **venue**, quelles que soient les heures | la pompe à béton : {{materiel.emplois.pompe.interventions}} interventions de {{materiel.emplois.pompe.duree_d_une_intervention_h::n2}} h |
| **Par heure de service** | les **heures au compteur**, conducteur compris | la pelle 30 t : {{materiel.emplois.pelle.unites_facturees::n0}} h |
| **Par durée de présence** | **tous les jours** du premier au dernier, attente comprise | le chariot : {{materiel.emplois.chariot.unites_facturees::n0}} jours pour {{materiel.emplois.chariot.jours_de_travail_j::n0}} jours de travail |

Et voici ce que cela donne, pour le **même marché de la location**, sur le même chantier :

| Engin | Prix affiché | Heures de travail | Coût du chantier | **Par heure de travail** |
|---|---:|---:|---:|---:|
| {{materiel.cout_du_parc.lignes.1.nom}} | {{materiel.cout_du_parc.lignes.1.prix_unitaire_MAD::n0}} MAD/h | {{materiel.cout_du_parc.lignes.1.heures_de_travail_h::n0}} h | {{materiel.cout_du_parc.lignes.1.cout_sur_le_chantier_MAD::k}} MAD | **{{materiel.cout_du_parc.lignes.1.cout_par_heure_de_travail_MAD::n0}} MAD/h** |
| {{materiel.cout_du_parc.lignes.2.nom}} | {{materiel.cout_du_parc.lignes.2.prix_unitaire_MAD::n0}} MAD/j | {{materiel.cout_du_parc.lignes.2.heures_de_travail_h::n0}} h | {{materiel.cout_du_parc.lignes.2.cout_sur_le_chantier_MAD::k}} MAD | **{{materiel.cout_du_parc.lignes.2.cout_par_heure_de_travail_MAD::n0}} MAD/h** |
| {{materiel.cout_du_parc.lignes.0.nom}} | {{materiel.cout_du_parc.lignes.0.prix_unitaire_MAD::n0}} MAD/j | {{materiel.cout_du_parc.lignes.0.heures_de_travail_h::n0}} h | {{materiel.cout_du_parc.lignes.0.cout_sur_le_chantier_MAD::k}} MAD | **{{materiel.cout_du_parc.lignes.0.cout_par_heure_de_travail_MAD::n0}} MAD/h** |

Un rapport de **{{materiel.cout_du_parc.rapport_du_plus_cher_au_moins_cher::n2}}** entre
{{materiel.cout_du_parc.le_plus_cher_par_heure}} et
{{materiel.cout_du_parc.le_moins_cher_par_heure}}, et il ne vient d'aucune différence de prix de
marché : il vient de l'unité. La pompe est chère à l'heure
parce qu'on paie sa **venue** pour {{materiel.emplois.pompe.duree_d_une_intervention_h::n2}} heures
de pompage. Le chariot est cher parce qu'on paie ses
{{materiel.emplois.chariot.jours_de_presence_sans_travail_j::n0}} jours **d'attente**.

:::encart {"genre":"alerte","titre":"La règle que la passe de C1 avait réclamée, et que personne n'avait outillée"}
« Toute grandeur multipliée par une durée de chantier nomme la fenêtre d'emploi de la ressource
qu'elle loue. » C'est la dette n° 32 de ce cours, écrite après C1. Le régime « par durée de
présence » en est le cas général : il **faut** une fenêtre, elle se lit dans le planning, et elle
n'est pas le nombre de jours travaillés. {{gare.materiel_engins._les_trois_regimes_de_location}}
:::

### Le taux d'emploi ne se déclare pas : il se lit dans le planning

Pour chaque famille, les **tâches servies** donnent les jours de travail (somme de leurs segments
dans le réseau de D2) et la **première et la dernière** donnent la fenêtre de présence. Rien n'est
posé à la main.

| Engin | Tâches servies | Jours de travail | Fenêtre | Présence utile |
|---|---:|---:|---:|---:|
| Pompe | {{materiel.emplois.pompe.taches.length}} | {{materiel.emplois.pompe.jours_de_travail_j::n0}} j | jours {{materiel.emplois.pompe.fenetre_j.0::n0}} à {{materiel.emplois.pompe.fenetre_j.1::n0}} | {{materiel.emplois.pompe.taux_de_presence_utile_pct::n0}} % |
| Pelle | {{materiel.emplois.pelle.taches.length}} | {{materiel.emplois.pelle.jours_de_travail_j::n0}} j | jours {{materiel.emplois.pelle.fenetre_j.0::n0}} à {{materiel.emplois.pelle.fenetre_j.1::n0}} | {{materiel.emplois.pelle.taux_de_presence_utile_pct::n0}} % |
| Chariot | {{materiel.emplois.chariot.taches.length}} | {{materiel.emplois.chariot.jours_de_travail_j::n0}} j | jours {{materiel.emplois.chariot.fenetre_j.0::n0}} à {{materiel.emplois.chariot.fenetre_j.1::n0}} | {{materiel.emplois.chariot.taux_de_presence_utile_pct::n0}} % |

La pelle a le meilleur taux de présence utile et le chariot le plus mauvais. **Ce n'est pas une
propriété des engins, c'est une propriété de leurs fenêtres** : la pelle sert
{{materiel.emplois.pelle.taches.length}} tâches de terrassement rapprochées et n'a qu'un seul creux
de {{materiel.parc.familles.1.jours_sans_emploi::n0}} jours ; le chariot sert
{{materiel.emplois.chariot.taches.length}} tâches étalées sur presque tout le chantier et cumule
{{materiel.parc.familles.2.jours_sans_emploi::n0}} jours sans emploi.

:::encart {"genre":"voir","titre":"Un contrôle qui ne contrôle rien, et le dire vaut mieux que de s'en féliciter"}
{{materiel.emplois.pompe._les_deux_voies_ne_sont_pas_independantes}}
:::

### L'emploi de la pompe est entièrement **déduit**

La pompe ne reste pas sur le site : elle vient et repart. Son emploi ne se déclare donc pas, il se
calcule, et aucune heure n'est posée à la main : le **volume pompé** vient du bordereau de D1
({{materiel.emplois.pompe.jours_pompe_au_bordereau_de_D1_j::n2}} jours de pompe ÷ son coefficient =
{{materiel.emplois.pompe.volume_pompe_du_bordereau_m3::n0}} m³), le **volume d'un coulage** est celui
d'une zone du module témoin ({{materiel.emplois.pompe.volume_d_un_coulage_m3::n1}} m³) et la **durée
d'une intervention** est celle que C3 calcule ({{materiel.emplois.pompe.duree_d_une_intervention_h::n2}} h).
D'où {{materiel.emplois.pompe.interventions}} interventions et
{{materiel.emplois.pompe.heures_de_travail_h::n1}} heures de pompage sur tout le chantier.

## S4 · L'étude de cas : les trois engins de la gare

### a. Le verdict, engin par engin

| | Pompe | Pelle 30 t | Chariot télescopique |
|---|---:|---:|---:|
| Régime de location | intervention | heure de service | **durée de présence** |
| Amortissement | {{materiel.verdicts.0.amortissement_MAD_an::k}} MAD/an | {{materiel.verdicts.1.amortissement_MAD_an::k}} MAD/an | {{materiel.verdicts.2.amortissement_MAD_an::k}} MAD/an |
| Entretien | {{materiel.verdicts.0.entretien_MAD_an::k}} MAD/an | {{materiel.verdicts.1.entretien_MAD_an::k}} MAD/an | {{materiel.verdicts.2.entretien_MAD_an::k}} MAD/an |
| Capital immobilisé | {{materiel.verdicts.0.cout_financier_MAD_an::k}} MAD/an | {{materiel.verdicts.1.cout_financier_MAD_an::k}} MAD/an | {{materiel.verdicts.2.cout_financier_MAD_an::k}} MAD/an |
| **Part fixe $F$** | **{{materiel.verdicts.0.fixe_MAD_an::k}} MAD/an** | **{{materiel.verdicts.1.fixe_MAD_an::k}} MAD/an** | **{{materiel.verdicts.2.fixe_MAD_an::k}} MAD/an** |
| Variable $v$ | {{materiel.verdicts.0.variable_MAD_h::n0}} MAD/h | {{materiel.verdicts.1.variable_MAD_h::n0}} MAD/h | {{materiel.verdicts.2.variable_MAD_h::n0}} MAD/h |
| Location fixe $L_0$ | {{materiel.verdicts.0.equilibre.location_fixe_L0_MAD_an::n0}} | {{materiel.verdicts.1.equilibre.location_fixe_L0_MAD_an::n0}} | **{{materiel.verdicts.2.equilibre.location_fixe_L0_MAD_an::k}} MAD/an** |
| Location marginale $L_1$ | {{materiel.verdicts.0.equilibre.location_marginale_L1_MAD_h::n0}} MAD/h | {{materiel.verdicts.1.equilibre.location_marginale_L1_MAD_h::n0}} MAD/h | {{materiel.verdicts.2.equilibre.location_marginale_L1_MAD_h::n0}} MAD/h |
| Pente de l'écart $v - L_1$ | {{materiel.verdicts.0.equilibre.pente_de_l_ecart_MAD_h::n0}} | {{materiel.verdicts.1.equilibre.pente_de_l_ecart_MAD_h::n0}} | **+{{materiel.verdicts.2.equilibre.pente_de_l_ecart_MAD_h::n0}}** |
| **Seuil $h_0$** | **{{materiel.verdicts.0.equilibre.seuil_h_par_an::n0}} h/an** | **{{materiel.verdicts.1.equilibre.seuil_h_par_an::n0}} h/an** | **{{materiel.verdicts.2.equilibre.seuil_h_par_an::n0}} h/an** |
| Sens | possession au-**dessus** | possession au-**dessus** | possession au-**dessous** |
| Plafond à cette intensité | {{materiel.verdicts.0.heures_max_a_cette_intensite_h::n0}} h/an | {{materiel.verdicts.1.heures_max_a_cette_intensite_h::n0}} h/an | {{materiel.verdicts.2.heures_max_a_cette_intensite_h::n0}} h/an |
| Emploi réel | {{materiel.verdicts.0.heures_par_an_h::n1}} h/an | {{materiel.verdicts.1.heures_par_an_h::n0}} h/an | {{materiel.verdicts.2.heures_par_an_h::n0}} h/an |
| Possession / location | {{materiel.verdicts.0.possession_MAD_h::k}} / {{materiel.verdicts.0.location_MAD_h::k}} MAD/h | {{materiel.verdicts.1.possession_MAD_h::n0}} / {{materiel.verdicts.1.location_MAD_h::n0}} MAD/h | {{materiel.verdicts.2.possession_MAD_h::n0}} / {{materiel.verdicts.2.location_MAD_h::n0}} MAD/h |
| **Sans estimation** | **{{materiel.verdicts.0.conclusion_sans_estimation}}** | **{{materiel.verdicts.1.conclusion_sans_estimation}}** | **{{materiel.verdicts.2.conclusion_sans_estimation}}** |
| Possession gagne dans | {{materiel.verdicts.0.part_des_tirages_pro_possession_pct::n1}} % des tirages | {{materiel.verdicts.1.part_des_tirages_pro_possession_pct::n1}} % | {{materiel.verdicts.2.part_des_tirages_pro_possession_pct::n1}} % |
| **Verdict publié** | **{{materiel.verdicts.0.verdict}}** | **{{materiel.verdicts.1.verdict}}** | **{{materiel.verdicts.2.verdict}}** |

Trois lectures, et **aucune ne demande d'estimer l'emploi** :

1. **La pompe se loue, et on n'a rien à calculer.** Son seuil
   ({{materiel.verdicts.0.equilibre.seuil_h_par_an::n0}} h/an) est au-dessus du plafond de son
   intensité ({{materiel.verdicts.0.heures_max_a_cette_intensite_h::n0}} h/an) et la possession ne
   gagnerait qu'au-dessus de ce seuil : il est inatteignable. Appelée **tous** les jours ouvrés de
   l'année pour un coulage de {{materiel.emplois.pompe.duree_d_une_intervention_h::n2}} h, elle ne
   rattraperait pas sa location. Et c'est le seul engin dont **les deux combinaisons extrêmes de
   paramètres concordent** : au coin le plus favorable à la possession, la location gagne encore de
   {{materiel.verdicts.0.ecart_pro_possession_MAD_an::k}} MAD/an. Aucune combinaison de ces
   fourchettes ne peut inverser ce résultat — c'est la preuve la plus forte que ce module sache
   produire.
2. **La pelle se loue, et cela dit quelque chose du marché.** Seuil
   {{materiel.verdicts.1.equilibre.seuil_h_par_an::n0}} h/an pour un plafond de
   {{materiel.verdicts.1.heures_max_a_cette_intensite_h::n0}} : à
   {{materiel.cout_du_parc.lignes.1.prix_unitaire_MAD::n0}} MAD l'heure conducteur compris, le loueur
   ne couvre pas la possession d'une pelle 30 t en dessous de
   {{materiel.verdicts.1.equilibre.seuil_h_par_an::n0}} heures par an — bien plus qu'une année n'en
   offre à un chantier. Il tient ce prix parce qu'il **ne travaille pas pour un seul chantier**
   (§ S4e).
3. **Le chariot se possède, et c'est le cas qui renverse l'intuition.** Sa pente est **positive**
   (+{{materiel.verdicts.2.equilibre.pente_de_l_ecart_MAD_h::n0}} MAD/h) : la possession gagne
   **au-dessous** du seuil, parce que sa location est un coût **fixe**
   ({{materiel.verdicts.2.equilibre.location_fixe_L0_MAD_an::k}} MAD/an de présence contre
   {{materiel.verdicts.2.fixe_MAD_an::k}} de part fixe en possession). Le seuil est à
   {{materiel.verdicts.2.equilibre.seuil_h_par_an::n0}} h/an, le plafond à
   {{materiel.verdicts.2.heures_max_a_cette_intensite_h::n0}} : l'engin **ne peut pas** travailler
   assez pour que la location redevienne avantageuse. Au nominal, la possession économise
   {{materiel.verdicts.2.ecart_MAD_an::k}} MAD par an.

   Et pourtant le verdict publié est **{{materiel.verdicts.2.verdict}}** : la possession ne gagne que
   dans {{materiel.verdicts.2.part_des_tirages_pro_possession_pct::n1}} % des tirages dans les
   fourchettes, et le seuil déclaré est de {{materiel.verdicts.2.seuil_de_verdict_pct::n0}} %. C'est
   une **forte présomption, pas une démonstration**, et ce cours ne la convertit pas en décision.
   Les deux phrases sont vraies ensemble : à **ces** valeurs la conclusion ne demande aucune
   estimation, et sur **l'étendue** des hypothèses elle n'est pas acquise.

### Les hypothèses de ce tableau, et il n'y en a pas d'autres

Tout ce qui précède sort de **vingt-cinq nombres déclarés** et d'aucune norme. Les voici, pour que
vous puissiez les remplacer par les vôtres — un bordereau de loueur et une facture d'entretien
suffisent à en vérifier la moitié.

**Communs aux trois engins** — gasoil
⟦V3|gasoil professionnel livré sur chantier|11,5 MAD/l|MAD/l|9,0 à 15,0|2026|cuve de chantier comprise⟧,
conducteur d'engin
⟦V3|conducteur d'engin, charges patronales comprises|60 MAD/h|MAD/h|48 à 80|2026|du même ordre que le grutier de D1 (62 MAD/h) ; déclaré ici parce que le tableau de main d'œuvre de D1 n'a pas cette ligne⟧,
valeur résiduelle
⟦V3|part du prix d'achat récupérée à la revente en fin d'amortissement|20 %|%|10 à 30|2026|commune aux trois engins : un paramètre par engin n'ajouterait rien à la précision de cette comparaison⟧,
coût du capital
⟦V3|coût du capital immobilisé, appliqué au capital moyen engagé|7,0 %|%/an|5,0 à 11,0|2026|demi-somme du prix d'achat et de la valeur résiduelle. Sans cette ligne la possession paraîtrait gratuite en trésorerie⟧.

**Pompe à béton automotrice 32 m** — prix d'achat
⟦V3|prix d'achat d'une pompe à béton automotrice 32 m, neuve|4 200 000 MAD|MAD|3 200 000 à 6 500 000|2026|châssis porteur compris⟧,
amortissement
⟦V3|durée d'amortissement linéaire d'une pompe à béton|7 ans|ans|5 à 10|2026|amortissement linéaire, sans montée de l'entretien avec l'âge (simplification déclarée)⟧,
entretien
⟦V3|entretien annuel d'une pompe à béton, en part du prix d'achat|9 %|%/an|6 à 14|2026|pièces d'usure (tuyauteries, lunettes, vérins) et révisions. C'est l'engin dont l'entretien pèse le plus, parce que le béton use tout ce qu'il traverse⟧,
carburant
⟦V3|consommation d'une pompe à béton en pompage effectif|18 l/h|l/h|12 à 26|2026|en pompage effectif, non en attente⟧.

**Pelle hydraulique 30 t** — prix d'achat
⟦V3|prix d'achat d'une pelle hydraulique sur chenilles 30 t, neuve|2 600 000 MAD|MAD|2 000 000 à 3 800 000|2026|godet et marteau compris⟧,
amortissement
⟦V3|durée d'amortissement linéaire d'une pelle 30 t|8 ans|ans|6 à 12|2026|amortissement linéaire⟧,
entretien
⟦V3|entretien annuel d'une pelle 30 t, en part du prix d'achat|11 %|%/an|8 à 16|2026|trains de chenilles, dents, circuit hydraulique. Un terrassement abrasif double ce poste⟧,
carburant
⟦V3|consommation d'une pelle 30 t en terrassement soutenu|24 l/h|l/h|18 à 34|2026|en terrassement soutenu⟧,
intensité d'emploi
⟦V3|heures de travail effectif d'une pelle par jour ouvré des tâches servies|5,5 h/j|h par jour servi|4,0 à 7,0|2026|une pelle en terrassement travaille presque toute la journée : c'est l'engin au meilleur taux de présence utile du chantier⟧,
disponibilité
⟦V3|disponibilité d'une pelle 30 t|85 %|%|75 à 93|2026|la plus basse des trois : une pelle travaille dans la terre, et c'est ce qui la casse⟧.

**Chariot télescopique 4 t / 17 m** — prix d'achat
⟦V3|prix d'achat d'un chariot télescopique 4 t à 17 m, neuf|950 000 MAD|MAD|700 000 à 1 400 000|2026|fourches et tablier compris⟧,
amortissement
⟦V3|durée d'amortissement linéaire d'un chariot télescopique|8 ans|ans|6 à 12|2026|amortissement linéaire⟧,
entretien
⟦V3|entretien annuel d'un chariot télescopique, en part du prix d'achat|8 %|%/an|5 à 13|2026|le poste le plus faible des trois : pas de béton, pas de terre⟧,
carburant
⟦V3|consommation d'un chariot télescopique en manutention courante|7 l/h|l/h|5 à 11|2026|manutention courante⟧,
intensité d'emploi
⟦V3|heures de manutention effective d'un chariot par jour ouvré des tâches servies|3,5 h/j|h par jour servi|2,0 à 5,5|2026|c'est l'engin que tout le monde appelle et que personne ne compte : gros œuvre, couverture, façades, quais et second œuvre⟧,
disponibilité
⟦V3|disponibilité d'un chariot télescopique|92 %|%|85 à 97|2026|la meilleure des trois, et c'est pourquoi tout le chantier finit par en dépendre⟧.

**Rendement de la pompe** — débit catalogue
⟦V3|débit catalogue d'une pompe à béton automotrice 32 m|90 m³/h|m³/h|60 à 150|2026|débit théorique du prospectus, mesuré à pression nulle avec un mélange de laboratoire. Aucun chantier ne l'a jamais vu⟧,
pompabilité
⟦V3|facteur de pompabilité du béton réel, tuyauterie comprise|0,80|sans unité|0,70 à 0,90|2026|consistance, granulométrie, longueur et coudes de la tuyauterie : le cylindre ne se remplit jamais complètement⟧,
part de l'heure pompée
⟦V3|part de l'heure de présence réellement passée à pousser du béton|0,70|sans unité|0,55 à 0,85|2026|le reste est déplacement de flèche, changement de bande, attente de toupie⟧,
arrêts
⟦V3|facteur d'arrêts et de nettoyages pendant un coulage|0,85|sans unité|0,70 à 0,95|2026|nettoyages de tuyauterie, bouchons, pauses de l'équipe de mise en œuvre⟧.

:::encart {"genre":"voir","titre":"Pourquoi un engin peu employé peut se posséder"}
Louer à la présence, c'est acheter un coût fixe. La comparaison n'est alors plus « fixe contre
variable » mais **fixe contre fixe** — et celui du loueur est plus gros, parce qu'il contient sa
marge, son immobilisation et son risque. Toute l'économie de la location repose sur le fait qu'il
remplit cette fenêtre avec plusieurs clients ; quand un seul chantier la paie en entier, il n'y a
plus rien à acheter. **Demandez toujours quelle part de la facture tombe sans que l'engin travaille.**
:::

:::figure {"fn":"diagramme","args":"materiel.figures.equilibre_chariot.points","titre":"Chariot télescopique : écart annuel entre posséder et louer, selon les heures travaillées","num":1,"large":true,"options":{"unite":"kMAD/an","axeX":true,"uniteX":"heures de travail par an","nom":"possession − location","marqueur":{"$":"materiel.figures.equilibre_chariot.marqueur"}},"voir":["Le zéro de l'axe EST le prix de la location : au-dessous, posséder coûte moins cher ; au-dessus, plus cher. La courbe part en bas et MONTE — c'est le sens inverse du cas classique, et il se lit directement sur la figure.","Le croisement est au seuil, {{materiel.verdicts.2.equilibre.seuil_h_par_an::n0}} h/an, en tireté. Mais le plafond d'emploi de l'engin à cette intensité n'est que de {{materiel.figures.equilibre_chariot.plafond::n0}} h/an : toute la partie droite de la figure, au-delà de ce plafond, est hors d'atteinte. C'est pourquoi la décision ne demande aucune estimation.","L'emploi réel est de {{materiel.figures.equilibre_chariot.emploi_reel::n0}} h/an, très à gauche du croisement : d'où les {{materiel.verdicts.2.ecart_MAD_an::k}} MAD/an d'écart en faveur de la possession.","C'est une DROITE, et sa pente est v − L₁ = {{materiel.verdicts.2.variable_MAD_h::n0}} − {{materiel.verdicts.2.equilibre.location_marginale_L1_MAD_h::n0}} = +{{materiel.verdicts.2.equilibre.pente_de_l_ecart_MAD_h::n0}} MAD par heure. Elle monte parce que chaque heure de travail coûte du carburant à celui qui possède et rien du tout à celui qui loue à la présence."],"erreur":"Lire cette figure comme une courbe de rentabilité générale. Elle vaut pour CE régime de location. Le même engin facturé à l'heure de service donnerait une droite DESCENDANTE, croisant zéro dans l'autre sens — et la conclusion inverse."}
:::

### b. Le parc, jour par jour : présent n'est pas au travail

:::figure {"fn":"histogramme","args":"materiel.figures.parc_presents","titre":"Engins présents sur le site, et engins au travail, jour par jour","num":2,"large":true,"options":{"unite":"engins","serie2":{"$":"materiel.figures.parc_travail"},"nom1":"présents (fenêtre d'emploi)","nom2":"au travail"},"voir":["Les barres sont les engins PRÉSENTS, le contour est ceux qui TRAVAILLENT. L'aire entre les deux est ce que personne ne compte : {{materiel.parc.engins_jours_de_travail::n0}} engins-jours de travail pour {{materiel.parc.engins_jours_de_presence::n0}} de présence, soit {{materiel.parc.taux_d_emploi_du_parc_pct::n0}} %.","La pointe de présence est à {{materiel.parc.pointe_presents}} engins, et le profil s'étend sur {{materiel.parc.jours::n0}} jours — la durée du chantier, pas celle d'une tâche.","Les deux grands trous du contour sont les attentes du chariot : du jour {{materiel.parc.familles.2.plus_longs_trous_j.0.0::n0}} au jour {{materiel.parc.familles.2.plus_longs_trous_j.0.1::n0}}, puis du {{materiel.parc.familles.2.plus_longs_trous_j.1.0::n0}} au {{materiel.parc.familles.2.plus_longs_trous_j.1.1::n0}} — le chantier lève alors sa charpente au-dessus de la voie, sous consignation, et il n'y a rien à manutentionner. L'engin, lui, est toujours là, et il totalise {{materiel.parc.familles.2.jours_sans_emploi::n0}} jours sans emploi dans sa fenêtre.","Les trois engins ne travaillent ensemble que {{materiel.parc.jours_ou_tout_le_parc_travaille}} jours, en deux plages : jours {{materiel.parc.plages_ou_tout_le_parc_travaille.0.0::n0}} à {{materiel.parc.plages_ou_tout_le_parc_travaille.0.1::n0}} (soutènement et semelles), puis {{materiel.parc.plages_ou_tout_le_parc_travaille.1.0::n0}} à {{materiel.parc.plages_ou_tout_le_parc_travaille.1.1::n0}} (la pelle revient remblayer et étancher pendant que les poteaux montent). Hors de ces deux plages, il y a toujours au moins un engin payé qui ne fait rien."],"erreur":"Dimensionner un parc sur la pointe de PRÉSENCE. C'est la pointe de TRAVAIL qui dit de combien d'engins on a besoin le même jour ; la présence dit seulement combien de temps on les paie — et les deux questions ne portent pas sur le même nombre."}
:::

Un taux d'emploi de parc de {{materiel.parc.taux_d_emploi_du_parc_pct::n0}} % n'est pas une
anomalie : c'est la norme sur un chantier de bâtiment, où les engins attendent des tâches qui
s'enchaînent mal. Il devient un problème quand on le paie **sans le savoir**.

### c. Ce que le parc coûte — et la ligne qui n'existe nulle part

Le parc de ces trois familles coûte {{materiel.cout_du_parc.total_sur_le_chantier_MAD::k}} MAD en
location sur la durée du chantier. Mais une ligne n'a **aucun prix au bordereau de D1** :
{{materiel.cout_du_parc.lignes_absentes_du_bordereau.0}}, pour
**{{materiel.cout_du_parc.montant_absent_du_bordereau_MAD::k}} MAD**
⟦V3|location journalière nue d'un chariot télescopique 4 t / 17 m|1 450 MAD|MAD/j|1 000 à 2 200|2026|transport amorti, opérateur non compris. Aucun prix de chariot télescopique n'existait au bordereau de D1 : cette ligne est déclarée par C6⟧.

Ce montant vaut **{{materiel.cout_du_parc.part_du_poste_consommee_pct::n0}} %** du seul poste des
frais de durée qui pourrait l'absorber
({{materiel.cout_du_parc.poste_qui_devrait_l_absorber}},
{{materiel.cout_du_parc.montant_de_ce_poste_MAD::k}} MAD). Autrement dit : la dépense est **plus
grosse que la ligne censée la contenir**.

:::encart {"genre":"attente","titre":"La limite de ce résultat, publiée avec lui"}
{{materiel.cout_du_parc._limite}}
:::

Et un second écart, de même famille mais plus petit : la pompe.
{{materiel.cout_du_parc.pompe_deux_voies.pourquoi}} D1 compte
{{materiel.cout_du_parc.pompe_deux_voies.voie_D1_au_volume_j::n2}} jours de pompe, C6 en compte
{{materiel.cout_du_parc.pompe_deux_voies.voie_C6_aux_interventions_j}} — un facteur
{{materiel.cout_du_parc.pompe_deux_voies.rapport::n2}}, soit
{{materiel.cout_du_parc.pompe_deux_voies.ecart_MAD::k}} MAD. Le montant est petit ; le mécanisme ne
l'est pas, et il se répète partout où un sous-détail facture au **métré** une ressource qui se paie
à la **venue**.

### d. Catalogue contre réel : un engin choisi sur prospectus est sous-dimensionné

{{materiel.rendement_de_la_pompe.lecture}}

:::figure {"fn":"barres","args":"materiel.figures.rendement","titre":"Débit d'une pompe à béton, du prospectus au chantier","num":3,"large":true,"options":{"unite":"m³/h","bande":{"$":"materiel.rendement_de_la_pompe.fourchette_declaree_par_C3"},"libelle_bande":"fourchette du débit pratique déclarée par C3"},"voir":["Trois facteurs mènent de {{materiel.rendement_de_la_pompe.debit_catalogue_m3_h::n0}} à {{materiel.rendement_de_la_pompe.debit_recalcule_m3_h::n1}} m³/h : le béton réel et la tuyauterie, la part de l'heure réellement passée à pousser du béton, les nettoyages et arrêts. Leur produit vaut {{materiel.rendement_de_la_pompe.produit_des_facteurs}}, soit {{materiel.rendement_de_la_pompe.perte_catalogue_pct::n0}} % de perte.","La bande verte est la fourchette que le module C3 déclarait déjà pour le débit PRATIQUE d'une pompe. La valeur recalculée y tombe, et à {{materiel.rendement_de_la_pompe.ecart_pct::n1}} % de la valeur nominale de C3 : deux voies indépendantes, écart sous la tolérance de 5 % du § 3.3.","Ce qui crédite l'ORDRE de la chaîne, pas chacun de ses trois facteurs : trois nombres peuvent se compenser. C'est la même limite que les six corps d'état du module B7b.","Sur le chantier, le coulage tient {{materiel.rendement_de_la_pompe.debit_tenu_au_chantier_m3_h::n1}} m³/h, borné par {{materiel.rendement_de_la_pompe.ce_qui_borne_le_coulage}}. Le débit minimal anti-reprise froide est de {{materiel.rendement_de_la_pompe.plancher_anti_reprise_m3_h::n1}} m³/h : on est au-dessus, et c'est tout ce qui compte."],"erreur":"Choisir une pompe sur son débit catalogue en croyant prendre de la marge. Un engin choisi sur prospectus arrive sur le chantier avec la moitié de la capacité annoncée — et si le calcul de cadence a été fait sur le catalogue, il est faux de 100 %."}
:::

:::encart {"genre":"alerte","titre":"L'engin n'est presque jamais la contrainte"}
Le coulage de ce chantier tient {{materiel.rendement_de_la_pompe.debit_tenu_au_chantier_m3_h::n1}} m³/h
alors que la pompe en donne {{materiel.rendement_de_la_pompe.debit_recalcule_m3_h::n1}}. Ce qui borne,
c'est {{materiel.rendement_de_la_pompe.ce_qui_borne_le_coulage}} — l'**approvisionnement**, pas la
machine. Avant d'acheter du débit, comptez les camions : C3 l'a fait, et ce module ne le refait pas.
:::

### e. La chaîne, le secours, et la mutualisation

Un coulage demande que **plusieurs maillons répondent le même matin**. La disponibilité de la chaîne
est le **produit** des disponibilités, et non la plus faible d'entre elles :

| Maillon | Disponibilité |
|---|---:|
| {{materiel.chaine_du_coulage.maillons.0.element}} | {{materiel.chaine_du_coulage.maillons.0.disponibilite_pct::n0}} % ⟦V3|disponibilité d'une centrale à béton pour un coulage programmé|96 %|%|90 à 99|2026|panne de centrale, rupture de ciment, commande non honorée⟧ |
| {{materiel.chaine_du_coulage.maillons.1.element}} | {{materiel.chaine_du_coulage.maillons.1.disponibilite_pct::n0}} % ⟦V3|disponibilité de la rotation des toupies|92 %|%|82 à 97|2026|trafic urbain, accès chantier, panne d'un camion dans la rotation⟧ |
| {{materiel.chaine_du_coulage.maillons.2.element}} | {{materiel.chaine_du_coulage.maillons.2.disponibilite_pct::n0}} % ⟦V3|disponibilité d'une pompe à béton le jour où on l'appelle|88 %|%|78 à 95|2026|pannes, révisions, et indisponibilité du loueur sur un appel non programmé⟧ |
| {{materiel.chaine_du_coulage.maillons.3.element}} | {{materiel.chaine_du_coulage.maillons.3.disponibilite_pct::n0}} % ⟦V3|disponibilité des aiguilles vibrantes|97 %|%|92 à 99|2026|panne d'aiguille ou de convertisseur⟧ |
| **La chaîne** | **{{materiel.chaine_du_coulage.disponibilite_forme_fermee_pct::n1}} %** |

{{materiel.chaine_du_coulage.lecture}} L'écart avec le maillon le plus faible est de
{{materiel.chaine_du_coulage.ecart_avec_le_maillon_le_plus_faible_points::n1}} points. La forme
fermée est un produit ; elle est vérifiée par une **simulation directe** de
{{materiel.chaine_du_coulage.nb_tirages::k}} matinées tirées au hasard, qui donne
{{materiel.chaine_du_coulage.disponibilite_simulee_pct::n1}} % — écart
{{materiel.chaine_du_coulage.ecart_des_deux_voies_points::n2}} point. Cette double voie n'est pas
une coquetterie : c'est la règle D-067, née du module C4 où une formule parfaitement homogène était
fausse d'un terme.

**Le secours ne se choisit pas sur le maillon le plus fragile.** Doubler un maillon porte sa
disponibilité de $p$ à $1-(1-p)^2$ ; ce qui compte est le prix du **point de chaîne** gagné, comparé
à ce que coûte un jour perdu — {{materiel.chaine_du_coulage.cout_d_un_jour_perdu_MAD::k}} MAD de
frais de durée, lus dans D1.

| Secours | Gain de chaîne | Coût | Espérance | MAD / point | Rentable ? |
|---|---:|---:|---:|---:|---:|
| {{materiel.chaine_du_coulage.secours.2.element}} | +{{materiel.chaine_du_coulage.secours.2.gain_en_points_de_chaine::n2}} pts | {{materiel.chaine_du_coulage.secours.2.cout_du_secours_MAD_j::n0}} MAD/j ⟦V3|immobilisation d'une seconde pompe en attente sur le site|1 800 MAD|MAD/j|1 000 à 3 200|2026|pompe immobilisée sans pompage ; ce n'est pas le prix d'une intervention⟧ | {{materiel.chaine_du_coulage.secours.2.esperance_de_gain_MAD_j::n0}} MAD/j | {{materiel.chaine_du_coulage.secours.2.MAD_par_point_de_chaine::n0}} | **non** |
| {{materiel.chaine_du_coulage.secours.3.element}} | +{{materiel.chaine_du_coulage.secours.3.gain_en_points_de_chaine::n2}} pts | {{materiel.chaine_du_coulage.secours.3.cout_du_secours_MAD_j::n0}} MAD/j | {{materiel.chaine_du_coulage.secours.3.esperance_de_gain_MAD_j::n0}} MAD/j | {{materiel.chaine_du_coulage.secours.3.MAD_par_point_de_chaine::n0}} | **oui** |

:::encart {"genre":"piege","titre":"Le secours au plus gros gain n'est pas le bon"}
La seconde pompe gagne {{materiel.chaine_du_coulage.secours.2.gain_en_points_de_chaine::n2}} points de
chaîne — quatre fois plus que l'aiguille de secours — et elle n'est **pas** rentable : son rapport
espérance / coût vaut {{materiel.chaine_du_coulage.secours.2.rapport_gain_sur_cout}}. L'aiguille
vibrante en gagne {{materiel.chaine_du_coulage.secours.3.gain_en_points_de_chaine::n2}} pour
{{materiel.chaine_du_coulage.secours.3.cout_du_secours_MAD_j::n0}} MAD par jour, soit un rapport de
{{materiel.chaine_du_coulage.secours.3.rapport_gain_sur_cout}}. **Classez les secours par MAD par
point de chaîne, jamais par points gagnés.**

Et notez où sont les maillons non doublables : ce ne sont **pas** les plus faibles. Le plus faible
est la pompe ({{materiel.chaine_du_coulage.maillons.2.disponibilite_pct::n0}} %), qui se double très
bien — mais trop cher. Les deux qui ne se doublent pas du tout sont la **centrale**
({{materiel.chaine_du_coulage.maillons.0.disponibilite_pct::n0}} %) et la **rotation des toupies**
({{materiel.chaine_du_coulage.maillons.1.disponibilite_pct::n0}} %) :
{{materiel.chaine_du_coulage.secours.1.pourquoi}} Il reste donc, sur ces deux maillons, à agir sur
la **probabilité** plutôt que sur le secours — commande fermée la veille, créneau d'accès négocié,
pénalité contractuelle à la centrale —, et cela ne se calcule pas ici.
:::

**Et la mutualisation ?** C'est la question que les verdicts laissent ouverte : si la location gagne,
comment le loueur gagne-t-il de l'argent ? Il **mutualise**, et un chef de projet suivi multi-sites
(module D7) est dans sa position. Le calcul dit exactement sur quels engins cela change quelque
chose — et la réponse est : aucun.

| Engin | Emploi seul | Avec le second site | Position vis-à-vis du seuil | Sites équivalents |
|---|---:|---:|---:|---:|
| Pompe | {{materiel.mutualisation.lignes.0.heures_par_an_seul_h::n1}} h/an | {{materiel.mutualisation.lignes.0.heures_par_an_mutualisees_h::n0}} h/an | {{materiel.mutualisation.lignes.0.part_du_seuil_atteinte_pct::n0}} % du seuil, qu'il faut **dépasser** | **{{materiel.mutualisation.lignes.0.sites_equivalents_pour_atteindre_le_seuil::n1}}** |
| Pelle | {{materiel.mutualisation.lignes.1.heures_par_an_seul_h::n0}} h/an | {{materiel.mutualisation.lignes.1.heures_par_an_mutualisees_h::n0}} h/an | {{materiel.mutualisation.lignes.1.part_du_seuil_atteinte_pct::n0}} %, qu'il faut **dépasser** | **{{materiel.mutualisation.lignes.1.sites_equivalents_pour_atteindre_le_seuil::n1}}** |
| Chariot | {{materiel.mutualisation.lignes.2.heures_par_an_seul_h::n0}} h/an | {{materiel.mutualisation.lignes.2.heures_par_an_mutualisees_h::n0}} h/an | {{materiel.mutualisation.lignes.2.part_du_seuil_atteinte_pct::n0}} %, qu'il ne faut **pas** dépasser | {{materiel.mutualisation.lignes.2.sites_equivalents_pour_atteindre_le_seuil::n1}} |

La dernière colonne ne veut pas dire la même chose d'une ligne à l'autre, et c'est pourquoi elle
porte sa définition : pour les deux premières, c'est
« {{materiel.mutualisation.lignes.0.ce_que_le_seuil_signifie}} » ; pour la troisième, c'est
« {{materiel.mutualisation.lignes.2.ce_que_le_seuil_signifie}} ». Le même nombre, deux sens opposés.

Deux sites font {{materiel.mutualisation.sites_equivalents_mutualises::n2}} site équivalent, pertes de
transfert déduites
⟦V3|heures perdues en transferts et conflits de calendrier entre deux sites|12 %|%|5 à 25|2026|transferts, remises en route, conflits de calendrier. Sans cette ligne la mutualisation paraîtrait gratuite⟧,
pour un besoin du second site estimé à
⟦V3|heures que le second site de D7 ajoute, en part du besoin de la gare|0,8|sans unité|0,4 à 1,2|2026|le second site de D7 est entièrement V3 (dette 34) : ce coefficient aussi⟧
celui de la gare. {{materiel.mutualisation.lecture}}

:::encart {"genre":"voir","titre":"Le résultat contre-intuitif, et il tient encore au régime de location"}
{{materiel.mutualisation._hypothese_de_fenetre}} Pour le chariot, la possession passe de
{{materiel.verdicts.2.part_des_tirages_pro_possession_pct::n1}} % à
{{materiel.mutualisation.lignes.2.part_des_tirages_pro_possession_pct::n1}} % des tirages quand on
mutualise : **mutualiser un engin payé à la présence affaiblit l'argument de la possession.** Et
c'est logique — sa facture ne bouge pas, mais chaque heure de travail de plus coûte du carburant et
un conducteur à celui qui le possède.
:::

### f. Double lecture : entreprise et maîtrise d'œuvre

**Côté entreprise.** Le choix se fait en quatre gestes : lire la fenêtre d'emploi dans le planning
avant de consulter ; demander au loueur **dans quelle unité** il facture, et refuser un prix sans son
unité ; comparer au coût de possession complet, capital compris ; et rapporter le tout à l'**heure de
travail**, seule grandeur comparable d'un régime à l'autre.

**Côté maîtrise d'œuvre.** Vous ne choisissez pas le matériel de l'entreprise, et vous n'avez pas à
l'approuver. Trois contrôles vous appartiennent pourtant, et tous se font sur des pièces :

1. **L'adéquation des moyens aux cadences visées.** Le planning visé suppose un débit ; le matériel
   déclaré doit le tenir **à son rendement réel**, pas au catalogue. C'est le calcul du § S4d, et
   c'est le seul qui attrape un planning infaisable avant le premier retard.
2. **La cohérence du parc avec le planning.** Un engin annoncé pour une tâche et absent des autres
   est un point à soulever en réunion, pas une non-conformité. L'histogramme du § S4b est l'outil :
   la **pointe de travail** dit combien d'engins doivent être là le même jour.
3. **Les pièces réglementaires** — rapports de vérification des appareils de levage, habilitations
   des conducteurs, consignes d'exploitation. Leur contenu, leur périodicité et leurs critères sont
   **réglementaires** : ⏸. Ce module ne les invente pas, et un visa ne se donne pas sur une
   hypothèse.

### g. Sécurité : ce qu'un calcul de coût ne tranche jamais

Ce module compare des coûts. **Aucun de ses résultats n'autorise un choix de matériel** : une
économie de 100 000 MAD par an ne rachète pas un engin sous-dimensionné pour la charge qu'on lui
demande, et la décision « posséder » du chariot ne dispense d'aucune des vérifications de l'engin
qu'on achète. L'ordre de priorité du § 2.1 de ce cours est explicite : la sécurité des personnes
passe avant tout le reste, le coût vient après.

Les trois engins de cette fiche ont chacun leur mécanisme d'accident, et il est utile de les nommer
même sans en chiffrer la prévention :

- **Pompe à béton** : éclatement de tuyauterie sur bouchon, fouettement du tuyau de sortie,
  renversement sur calage insuffisant, contact de la flèche avec une ligne électrique. Le calage et
  la portance du sol sous les stabilisateurs sont les deux points du jour de coulage ; la zone sous
  la flèche se tient dégagée.
- **Chariot télescopique** : renversement, et c'est de très loin le premier risque. Il vient de deux
  causes — une charge hors de l'abaque à la portée demandée, et un sol qui cède. Les deux se
  vérifient avant le levage, pas pendant. S'y ajoute le transport de personnes sur les fourches, qui
  n'est jamais une option.
- **Pelle hydraulique** : la zone de rotation, l'effondrement de fouille et la présence de piétons
  dans l'angle mort arrière. Le talutage et le blindage des fouilles appartiennent au module C2 ; la
  séparation des engins et des piétons, au plan d'installation de C1.

**Ce qui est chiffré ailleurs, et ce qui reste ⏸.** L'abaque de charge d'un appareil de levage est
traitée au module C1 (la courbe de charge de la grue à tour) et elle se lit de la même façon pour un
chariot : une charge admissible décroît avec la portée. En revanche les **vérifications
réglementaires** — périodicité, contenu, critères d'acceptation, autorisations de conduite,
habilitations — sont réglementaires et restent **⏸** : ce cours n'invente pas une périodicité, et un
visa ne se donne pas sur une hypothèse. Elles se lisent dans la réglementation applicable et dans le
**plan HSE** du chantier, qui est la pièce de référence du module C7.

## S5 · Erreurs fréquentes

1. **Comparer un prix de location à un coût de possession sans savoir ce que le prix compte.** C'est
   l'erreur mère, et elle est invisible : les deux nombres ont l'air comparables. Ce module l'a
   commise dans sa première version — il facturait à la pompe un jour de location par **jour de
   tâche**, soit {{materiel.emplois.pompe.jours_de_travail_j::n0}} jours au lieu de
   {{materiel.emplois.pompe.interventions}} interventions, et neuf fois le vrai montant ; et au
   chariot ses **jours de travail** au lieu de sa fenêtre, soit
   {{materiel.emplois.chariot.jours_de_travail_j::n0}} au lieu de
   {{materiel.emplois.chariot.unites_facturees::n0}}. Les deux erreurs vont en sens inverse et
   chacune **inversait un verdict**.
2. **Chercher un seuil sans chercher son sens.** $h_0 = (L_0 - F)/(v - L_1)$ ne dit rien tant qu'on
   n'a pas regardé le signe de $v - L_1$. La formule des manuels, $F/(\ell - v)$, suppose
   $L_0 = 0$ : elle est fausse dès que la location porte un terme fixe, et elle l'est **sans
   bruit**, parce qu'elle donne le même nombre dans deux régimes sur trois.
3. **Oublier le capital.** Un engin payé comptant ne coûte rien en trésorerie courante, et c'est
   exactement ce qui trompe : son capital travaille ailleurs. Ici
   {{materiel.verdicts.0.cout_financier_MAD_an::k}} MAD par an pour la pompe, qui ne figurent sur
   aucune facture.
4. **Oublier la valeur de revente.** Elle allège l'amortissement d'un cinquième ici. La négliger
   charge la possession et fait choisir la location pour une mauvaise raison — un bon choix tiré
   d'un calcul faux reste un calcul faux.
5. **Payer une fenêtre de présence sans le savoir.** Le chariot est sur le site
   {{materiel.emplois.chariot.fenetre_duree_j::n0}} jours et travaille
   {{materiel.emplois.chariot.jours_de_travail_j::n0}} jours ; la différence,
   {{materiel.emplois.chariot.jours_de_presence_sans_travail_j::n0}} jours, se paie plein tarif.
6. **Croire que la chaîne vaut son maillon le plus faible.** Elle vaut
   {{materiel.chaine_du_coulage.disponibilite_forme_fermee_pct::n1}} % quand le plus faible est à
   {{materiel.chaine_du_coulage.maillon_le_plus_faible_pct::n0}} %, soit
   {{materiel.chaine_du_coulage.coulages_derangeables::n1}} coulages dérangés sur
   {{materiel.chaine_du_coulage.coulages_derangeables_sur}} au lieu de 1.
7. **Choisir un secours sur le gain qu'il apporte** au lieu du prix de ce gain. La seconde pompe
   gagne quatre fois plus de points que l'aiguille de secours et coûte quinze fois plus cher.
8. **Choisir un engin sur son débit catalogue.** Il en donnera
   {{materiel.rendement_de_la_pompe.perte_catalogue_pct::n0}} % de moins, et si la cadence a été
   calculée sur le prospectus, le planning est faux dès sa première ligne.
9. **Dimensionner le parc sur la pointe de présence** au lieu de la pointe de travail — ou
   l'inverse. Deux questions, deux nombres : la présence dit ce qu'on paie, le travail dit de
   combien d'engins on a besoin le même jour.
10. **Croire qu'un amortissement long améliore l'affaire.** Il baisse la charge annuelle, mais
    l'entretien et les pannes montent avec l'âge, et cette fiche ne modélise pas cette montée :
    c'est une **simplification déclarée** du module.

## S6 · Exercices

:::exercice {"titre":"1 · Le loueur du chariot baisse son prix de 20 % : la décision change-t-elle ?","niveau":"application"}
Le loueur propose {{materiel.cout_du_parc.lignes.2.prix_unitaire_MAD::n0}} MAD/j moins 20 %, soit
1 160 MAD/j, toujours sur toute la fenêtre de présence et sans opérateur. Les autres paramètres sont
inchangés : part fixe $F$ = {{materiel.verdicts.2.fixe_MAD_an::k}} MAD/an, variable $v$ =
{{materiel.verdicts.2.variable_MAD_h::n0}} MAD/h, conducteur 60 MAD/h, emploi
{{materiel.verdicts.2.heures_par_an_h::n0}} h/an,
{{materiel.verdicts.2.unites_facturees_par_an::n0}} jours de présence facturés par an, plafond
{{materiel.verdicts.2.heures_max_a_cette_intensite_h::n0}} h/an.

Calculez $L_0$, $L_1$, le nouveau seuil et son sens. La conclusion « sans estimation » tient-elle
encore ?

**Corrigé.** $L_0$ = 250 × 1 160 = **290 000 MAD/an** ; $L_1$ = 60 MAD/h (le conducteur seul, comme
avant). La pente reste $v - L_1$ = {{materiel.verdicts.2.variable_MAD_h::n0}} − 60 =
**+{{materiel.verdicts.2.equilibre.pente_de_l_ecart_MAD_h::n0}} MAD/h**, donc le **sens ne change
pas** : la possession gagne au-dessous du seuil.

Écart à emploi nul : $F - L_0$ = {{materiel.verdicts.2.fixe_MAD_an::n0}} − 290 000 = −79 100 MAD/an.
Seuil : 79 100 / 80,5 = **982,6 h/an**, contre
{{materiel.verdicts.2.equilibre.seuil_h_par_an::n0}} avant. À l'emploi réel, l'écart vaut −79 100 +
80,5 × {{materiel.verdicts.2.heures_par_an_h::n0}} = **−47 125 MAD/an** : la possession gagne encore,
mais de deux fois moins qu'avant ({{materiel.verdicts.2.ecart_MAD_an::k}} MAD/an).

**La conclusion « sans estimation » tient encore, mais de justesse**, et c'est tout l'intérêt de
l'exercice. Le plafond est à {{materiel.verdicts.2.heures_max_a_cette_intensite_h::n0}} h/an et le
seuil à 983 : la marge est tombée de 115 % à **12 %**. Il suffirait que l'intensité d'emploi du
chariot soit de 5,5 h par jour servi au lieu de
{{materiel.emplois.chariot.heures_par_jour_servi_h::n1}} — ce que la fourchette déclarée autorise —
pour que le plafond passe à 1 375 h/an, dépasse le seuil, et **rouvre la question**. À ce prix, la
décision redevient une affaire d'estimation, et il faut la traiter comme telle.
:::

:::exercice {"titre":"2 · La chaîne du coulage avec deux maillons doublés","niveau":"application"}
On double **à la fois** la pompe et les aiguilles vibrantes. Quelle est la disponibilité de la
chaîne ? Le gain est-il la somme des deux gains individuels ? L'opération est-elle rentable ?

Rappel : les quatre maillons sont à {{materiel.chaine_du_coulage.maillons.0.disponibilite_pct::n0}},
{{materiel.chaine_du_coulage.maillons.1.disponibilite_pct::n0}},
{{materiel.chaine_du_coulage.maillons.2.disponibilite_pct::n0}} et
{{materiel.chaine_du_coulage.maillons.3.disponibilite_pct::n0}} % ; un jour perdu coûte
{{materiel.chaine_du_coulage.cout_d_un_jour_perdu_MAD::k}} MAD ; les deux secours coûtent
{{materiel.chaine_du_coulage.secours.2.cout_du_secours_MAD_j::n0}} et
{{materiel.chaine_du_coulage.secours.3.cout_du_secours_MAD_j::n0}} MAD/j.

**Corrigé.** Pompe doublée : $1 - 0{,}12^2 = 0{,}9856$. Aiguilles doublées :
$1 - 0{,}03^2 = 0{,}9991$. Chaîne : $0{,}96 \times 0{,}92 \times 0{,}9856 \times 0{,}9991 =$
**0,8697**, soit **87,0 %**, contre
{{materiel.chaine_du_coulage.disponibilite_forme_fermee_pct::n1}} % sans secours. Gain : **11,6
points**.

**Non, ce n'est pas la somme** des gains individuels
({{materiel.chaine_du_coulage.secours.2.gain_en_points_de_chaine::n2}} +
{{materiel.chaine_du_coulage.secours.3.gain_en_points_de_chaine::n2}} = 11,31 points) : c'est un peu
plus. Les gains d'un produit ne s'additionnent pas, ils se composent — le second s'applique à une
chaîne déjà meilleure. L'écart est petit ici (0,3 point) parce que les disponibilités sont hautes ;
sur des maillons à 60 % il serait considérable.

Rentabilité : espérance = 0,116 × {{materiel.chaine_du_coulage.cout_d_un_jour_perdu_MAD::n0}} =
1 884 MAD/j, contre un coût de 1 800 + 120 = **1 920 MAD/j**. **Non rentable**, de justesse — et
c'est entièrement la faute de la seconde pompe, qui coûte quinze fois l'aiguille pour quatre fois son
gain. Doubler l'aiguille **seule** reste la seule opération rentable des deux.
:::

:::exercice {"titre":"3 · Le chantier est reporté de six mois : que devient le parc ?","niveau":"probleme"}
Le maître d'ouvrage décale le démarrage du second œuvre de six mois (125 jours ouvrés) sans toucher
au reste du planning. La tâche SECO est servie par le chariot télescopique. Ses jours de **travail**
ne changent pas ; sa **fenêtre** s'allonge de 125 jours, de
{{materiel.emplois.chariot.fenetre_duree_j::n0}} à 680 jours.

1. Que devient le coût de location du chariot sur le chantier ?
2. Que deviennent son taux de présence utile et son emploi annuel ?
3. Que deviennent le seuil et le verdict ? Attention au piège.
4. Quelle décision de pilotage proposez-vous, et quand faut-il la prendre ?

**Corrigé.**

**1.** Le chariot étant facturé à la présence, la location nue passe de
{{materiel.emplois.chariot.unites_facturees::n0}} × {{materiel.cout_du_parc.lignes.2.prix_unitaire_MAD::n0}}
= 804 721 à 680 × {{materiel.cout_du_parc.lignes.2.prix_unitaire_MAD::n0}} = **986 000 MAD** — plus
**181 279 MAD** pour **exactement zéro heure de travail de plus**. C'est la définition du régime : on
paie du calendrier.

**2.** Taux de présence utile : {{materiel.emplois.chariot.jours_de_travail_j::n0}} / 680 = **37,1 %**,
contre {{materiel.emplois.chariot.taux_de_presence_utile_pct::n0}} %. La fenêtre vaut maintenant
680 / {{materiel.verdicts.2.jours_ouvres_par_an_j::n0}} = 2,72 ans, donc l'emploi annuel **baisse** :
{{materiel.emplois.chariot.heures_de_travail_h::n0}} / 2,72 = **324 h/an**, contre
{{materiel.verdicts.2.heures_par_an_h::n0}}.

**3. Le piège.** On pourrait croire que la possession y perd, puisque l'engin travaille moins par an.
**C'est le contraire**, et il faut regarder le sens. $L_0$ ne change pas — la fenêtre s'allonge, mais
le nombre de jours de présence **par an** reste
{{materiel.verdicts.2.unites_facturees_par_an::n0}}, soit toute l'année ouvrée. $F$, $v$ et $L_1$ ne
changent pas non plus : **le seuil reste à {{materiel.verdicts.2.equilibre.seuil_h_par_an::n0}} h/an**.
Et comme la possession gagne **au-dessous** du seuil, descendre à 324 h/an l'améliore :
écart = −151 600 + 80,5 × 324 = **−125 502 MAD/an**, contre
{{materiel.verdicts.2.ecart_MAD_an::k}} avant. **Un report de chantier renforce l'argument d'acheter
un engin payé à la présence.**

Deux énoncés à ne pas confondre : *par an*, l'écart se creuse en faveur de la possession ; *en
absolu sur le chantier*, celui qui loue paie 181 279 MAD de plus. Les deux sont vrais, et le second
est celui qui sort de votre budget.

**4.** Deux décisions, et seule la première est de votre ressort. **À l'annonce du report** :
renégocier le régime — prix mensuel avec clause de suspension, ou restitution de l'engin pendant le
creux. Les 181 279 MAD sont intégralement évitables, et ils ne se négocient qu'**avant** que la
fenêtre ne soit entamée. **Pour le reste** : l'achat se décide au début du chantier, pas au sixième
mois ; à ce stade la question n'est plus « acheter ou louer » mais « comment arrêter de payer les
jours d'attente ». Et c'est le vrai sujet du module : la décision de matériel se prend au moment où
l'on lit la fenêtre, c'est-à-dire **quand le planning est visé**.
:::

## S7 · Check-list, glossaire et quiz

**Check-list : avant de consulter un loueur**

1. La **fenêtre d'emploi** est-elle lue dans le planning, et non devinée ?
2. Les **jours de travail** sont-ils distingués des **jours de présence** ?
3. Le prix demandé est-il assorti de son **unité** : intervention, heure de compteur, jour de
   présence, mois ?
4. L'**opérateur** est-il compris, et à quel taux ?
5. Le coût de possession comprend-il l'**entretien** et le **capital**, pas seulement
   l'amortissement ?
6. La **valeur de revente** est-elle déduite ?
7. Le **sens** du seuil a-t-il été établi — $v$ contre $L_1$ — avant de regarder sa valeur ?
8. Le seuil est-il comparé au **plafond d'emploi** de l'engin à cette intensité ?
8. Le **rendement réel** a-t-il été substitué au rendement catalogue dans le calcul de cadence ?
9. La **disponibilité de la chaîne** a-t-elle été calculée comme un produit ?
10. Le secours est-il classé par **MAD par point de chaîne** et non par points gagnés ?
11. Chaque engin du parc a-t-il une **ligne au bordereau** — et sinon, quel poste le porte ?

**Glossaire**

| Terme | Ce que c'est |
|---|---|
| **Coût horaire de possession** | $F/h + v$ : part fixe annuelle divisée par les heures, plus la part variable. Décroît avec l'emploi, jamais avec la durée de détention |
| **$L_0$, $L_1$** | la location annuelle est affine : $L_0$ tombe sans travailler, $L_1$ est l'heure marginale. $L_0 = 0$ dans deux régimes sur trois |
| **Seuil $h_0$** | $(L_0 - F)/(v - L_1)$, en **heures par an**. Ne vaut rien sans son **sens** |
| **Sens du seuil** | donné par le signe de $v - L_1$. Possession au-dessus si $v < L_1$ (cas classique), **au-dessous** si $v > L_1$ (location devenue fixe) |
| **Plafond d'emploi** | jours ouvrés de l'année × heures par unité de service. Un seuil au-delà clôt la question **sans estimation** |
| **Régime de location** | l'unité facturée : intervention, heure de service, durée de présence. Décide plus que le prix |
| **Fenêtre d'emploi** | du premier au dernier jour de besoin d'un engin. Ce qu'on paie en régime de présence |
| **Taux de présence utile** | jours de travail / jours de fenêtre. {{materiel.parc.taux_d_emploi_du_parc_pct::n0}} % pour ce parc |
| **Rendement catalogue** | le débit du prospectus, mesuré à pression nulle. Il perd {{materiel.rendement_de_la_pompe.perte_catalogue_pct::n0}} % en arrivant sur un chantier |
| **Disponibilité de chaîne** | le **produit** des disponibilités des maillons. Jamais le minimum |
| **MAD par point de chaîne** | prix d'un secours divisé par les points de chaîne qu'il gagne. Le seul critère de choix d'un secours |

**Quiz**

**1. Un engin gardé huit ans et employé 300 h/an s'amortit-il mieux qu'un engin gardé deux ans au même rythme ?**
**Non, c'est le même rapport.** Le seuil est un nombre d'**heures par an** : la durée de détention
n'y figure pas. Seule l'intensité d'emploi compte.

**2. Pourquoi la pompe de ce chantier coûte-t-elle {{materiel.cout_du_parc.lignes.0.cout_par_heure_de_travail_MAD::n0}} MAD l'heure de travail alors qu'elle est affichée à {{materiel.cout_du_parc.lignes.0.prix_unitaire_MAD::n0}} MAD la journée ?**
Parce qu'on paie la **venue**, et qu'une venue ne dure que
{{materiel.emplois.pompe.duree_d_une_intervention_h::n2}} h de pompage. Le régime de facturation,
pas le prix, fait le coût horaire.

**3. Le seuil de la pompe est à {{materiel.verdicts.0.equilibre.seuil_h_par_an::n0}} h/an et son plafond d'emploi à {{materiel.verdicts.0.heures_max_a_cette_intensite_h::n0}} h/an. Que conclure, et en combien de temps ?**
**Qu'on la loue, et en trente secondes.** Son sens est « possession au-dessus du seuil », et le
seuil est inatteignable : appelée tous les jours ouvrés de l'année pour un coulage, elle resterait en
dessous. Aucune estimation d'emploi n'est nécessaire.

**3 bis. Le chariot a lui aussi un seuil hors d'atteinte. Pourquoi la conclusion est-elle l'inverse ?**
Parce que son **sens** est l'inverse : sa location est un coût fixe
({{materiel.verdicts.2.equilibre.location_fixe_L0_MAD_an::k}} MAD/an) et sa pente est positive, donc
la possession gagne **au-dessous** du seuil. Un seuil hors d'atteinte ne dit « louer » que dans le
cas classique.

**4. Le chariot : la possession gagne dans {{materiel.verdicts.2.part_des_tirages_pro_possession_pct::n1}} % des tirages. Le cours conclut-il qu'il faut l'acheter ?**
**Non.** Le seuil de verdict déclaré est de
{{materiel.verdicts.2.seuil_de_verdict_pct::n0}} % dans les deux sens, et
{{materiel.verdicts.2.part_des_tirages_pro_possession_pct::n1}} % ne le franchit pas. Aux valeurs
nominales la conclusion ne demande aucune estimation ; sur l'étendue des fourchettes elle n'est pas
acquise. Les deux énoncés tiennent ensemble, et le second est celui qui se publie.

**5. Quatre maillons à {{materiel.chaine_du_coulage.maillons.0.disponibilite_pct::n0}}, {{materiel.chaine_du_coulage.maillons.1.disponibilite_pct::n0}}, {{materiel.chaine_du_coulage.maillons.2.disponibilite_pct::n0}} et {{materiel.chaine_du_coulage.maillons.3.disponibilite_pct::n0}} % : la chaîne répond-elle {{materiel.chaine_du_coulage.maillon_le_plus_faible_pct::n0}} % des matinées ?**
**Non : {{materiel.chaine_du_coulage.disponibilite_forme_fermee_pct::n1}} %.** C'est un produit.
{{materiel.chaine_du_coulage.ecart_avec_le_maillon_le_plus_faible_points::n1}} points de moins que
le maillon le plus faible, soit {{materiel.chaine_du_coulage.coulages_derangeables::n1}} coulages
dérangés sur {{materiel.chaine_du_coulage.coulages_derangeables_sur}}.

**6. Faut-il immobiliser une seconde pompe, qui gagne {{materiel.chaine_du_coulage.secours.2.gain_en_points_de_chaine::n2}} points de chaîne — quatre fois le gain de l'aiguille de secours ?**
**Non.** Son espérance de gain
({{materiel.chaine_du_coulage.secours.2.esperance_de_gain_MAD_j::n0}} MAD/j) est inférieure à son
coût ({{materiel.chaine_du_coulage.secours.2.cout_du_secours_MAD_j::n0}} MAD/j). L'aiguille, elle,
rapporte {{materiel.chaine_du_coulage.secours.3.rapport_gain_sur_cout}} fois son prix. Le critère
est le **MAD par point**, pas le point.

:::memo
## Fiche mémo — matériel

**Les trois phrases du module**

> Le seuil est un nombre d'heures par an, jamais une durée de détention — et il ne vaut rien sans son sens.
> Ce qui décide n'est pas l'engin, c'est l'unité dans laquelle on le paie.
> Une chaîne vaut le produit de ses maillons, et un secours se classe en MAD par point.

**Les deux formules**

$$ \text{écart}(h) = (F - L_0) + (v - L_1)\,h \qquad\qquad h_0 = \frac{L_0 - F}{v - L_1} $$

avec $F$ = amortissement + entretien + capital (MAD/an), $v$ = carburant + conducteur (MAD/h),
$L_0$ = la part de la location qui tombe **sans travailler**, $L_1$ = son heure marginale, $h$ =
heures de travail par an. **Le signe de $v - L_1$ donne le sens** : possession au-dessus du seuil si
$v < L_1$, **au-dessous** si $v > L_1$.

$$ D_{\text{chaîne}} = \prod_i p_i \qquad\qquad p_i^{\text{doublé}} = 1 - (1 - p_i)^2 $$

**Les trois régimes, et ce qu'ils coûtent ici**

| | Unité facturée | MAD par heure de travail |
|---|---|---:|
| Pelle 30 t | heure de service | {{materiel.cout_du_parc.lignes.1.cout_par_heure_de_travail_MAD::n0}} |
| Chariot télescopique | **jour de présence** | {{materiel.cout_du_parc.lignes.2.cout_par_heure_de_travail_MAD::n0}} |
| Pompe à béton | **intervention** | {{materiel.cout_du_parc.lignes.0.cout_par_heure_de_travail_MAD::n0}} |

**Les chiffres de ce chantier**

| | |
|---|---:|
| Pompe : seuil / plafond / emploi | {{materiel.verdicts.0.equilibre.seuil_h_par_an::n0}} / {{materiel.verdicts.0.heures_max_a_cette_intensite_h::n0}} / {{materiel.verdicts.0.heures_par_an_h::n1}} h/an → **{{materiel.verdicts.0.conclusion_sans_estimation}}** |
| Pelle : seuil / plafond / emploi | {{materiel.verdicts.1.equilibre.seuil_h_par_an::n0}} / {{materiel.verdicts.1.heures_max_a_cette_intensite_h::n0}} / {{materiel.verdicts.1.heures_par_an_h::n0}} h/an → **{{materiel.verdicts.1.conclusion_sans_estimation}}** |
| Chariot : seuil (sens inversé) / plafond / emploi | {{materiel.verdicts.2.equilibre.seuil_h_par_an::n0}} / {{materiel.verdicts.2.heures_max_a_cette_intensite_h::n0}} / {{materiel.verdicts.2.heures_par_an_h::n0}} h/an → **{{materiel.verdicts.2.verdict}}** ({{materiel.verdicts.2.part_des_tirages_pro_possession_pct::n1}} % des tirages, nominal : {{materiel.verdicts.2.conclusion_sans_estimation}}) |
| Parc : travail / présence | {{materiel.parc.engins_jours_de_travail::n0}} / {{materiel.parc.engins_jours_de_presence::n0}} engins-jours = **{{materiel.parc.taux_d_emploi_du_parc_pct::n0}} %** |
| Location du parc sur le chantier | {{materiel.cout_du_parc.total_sur_le_chantier_MAD::k}} MAD, dont **{{materiel.cout_du_parc.montant_absent_du_bordereau_MAD::k}} MAD sans ligne au bordereau** |
| Pompe : débit catalogue → réel | {{materiel.rendement_de_la_pompe.debit_catalogue_m3_h::n0}} → {{materiel.rendement_de_la_pompe.debit_recalcule_m3_h::n1}} m³/h (−{{materiel.rendement_de_la_pompe.perte_catalogue_pct::n0}} %) |
| Chaîne du coulage | **{{materiel.chaine_du_coulage.disponibilite_forme_fermee_pct::n1}} %** pour un maillon faible à {{materiel.chaine_du_coulage.maillon_le_plus_faible_pct::n0}} % |
| Seul secours rentable | {{materiel.chaine_du_coulage.secours_le_plus_rentable}}, {{materiel.chaine_du_coulage.secours.3.MAD_par_point_de_chaine::n0}} MAD/point |
| Sites équivalents pour posséder la pompe | **{{materiel.mutualisation.lignes.0.sites_equivalents_pour_atteindre_le_seuil::n1}}** |

**Les six réflexes**

1. Demander l'unité avant le prix. Un prix sans son unité n'est pas un prix.
2. Lire la fenêtre d'emploi dans le planning, et la comparer aux jours de travail.
3. Établir le SENS du seuil, puis le comparer au plafond d'emploi — **avant** d'estimer quoi que ce soit.
4. Remplacer tout rendement catalogue par un rendement réel dans un calcul de cadence.
5. Calculer une disponibilité de chaîne comme un produit, et classer les secours en MAD par point.
6. Vérifier que chaque engin du parc a une ligne quelque part au bordereau.

**Ce qui reste ⏸**

Vérifications réglementaires des engins et des appareils de levage · périodicités et critères
d'acceptation · habilitations et autorisations de conduite · consignes réglementaires
d'exploitation · règles de distance et de survol (⏸ depuis C1) · toute obligation issue du plan HSE.
:::
