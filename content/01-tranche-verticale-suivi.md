---
id: TV
titre: Cycle de réalisation d'un plancher de mezzanine
fil: Étape 2 — tranche verticale de suivi · module témoin n° 1
resume: Une zone de plancher, de la quantité au reporting. C'est la tranche que vous validez avant que quoi que ce soit ne soit dupliqué.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · toutes les valeurs numériques sont V3
pied: Module témoin. Exemple pédagogique — ne remplace ni une note de calcul d'exécution ni le contrôle d'un bureau d'études ou de contrôle.
donnees: tranche-plancher, valeur-acquise, gare
---

## S1 · Ce que ce module fait, et pourquoi lui d'abord

Vous pilotez le suivi d'un chantier de bâtiments ferroviaires. Votre journée n'est pas faite de
sections d'acier : elle est faite de **quantités, de cadences, de durées, de coûts et d'écarts**. Ce
module prend **une zone de plancher de la mezzanine** de la gare et la suit de bout en bout :

> quantités → cadences et effectifs → durée → coût → planning → valeur acquise → reporting

C'est la **tranche verticale** exigée avant toute duplication (§ 5.3). Elle ne sert pas à vous
apprendre un plancher : elle sert à **valider la chaîne, la forme et la profondeur** du cours. Si
quelque chose ne va pas — trop long, trop court, mauvais angle, 3D inutile — c'est maintenant qu'il
faut le dire, pas après quinze modules bâtis dessus.

**Prérequis** : aucun. **Place dans le projet** : étape 7 et 8 du déroulé du cas phare (§ 10.2).

:::encart {"genre":"attente","titre":"Ce que ce module ne fait pas, et pourquoi"}
La phase § 5.0 interdit tout calcul de dimensionnement tant que les normes ne sont pas fournies. Donc
**aucune descente de charges, aucun ferraillage, aucune vérification** ici. L'épaisseur de dalle et la
section de poutre sont des **prédimensionnements V3** ; les quantités d'acier sortent de **ratios**,
pas d'un calcul.

Cela ne diminue pas le module : le suivi de chantier ne dépend d'aucun règlement. Cela change ce que
vous avez le droit de croire des chiffres. **Le béton et le coffrage sont justes à la géométrie près ;
l'acier est un ordre de grandeur à ± 20 %.** Le module le répète là où ça compte.
:::

## S2 · L'idée centrale : la zone est l'unité de tout

Un plancher ne se suit pas au mètre carré ni à la poutre. Il se suit à la **zone de coulage** — la
surface que l'on coule en une fois, entre deux reprises de bétonnage.

Pourquoi c'est elle, et pas autre chose : la zone est la seule grandeur qui soit à la fois **une
quantité** (du béton, de l'acier, du coffrage), **une durée** (un cycle), **un coût** (une ligne de
situation) et **un jalon** (coulé ou pas coulé — il n'y a pas de demi-coulage). Tout le reste —
avancement, valeur acquise, reporting — se raccroche à elle. Changez le découpage en zones, et vous
changez le planning, la trésorerie et la façon dont vous mesurez l'avancement.

La mezzanine fait {{gare.geometrie.mezzanine.largeur_m::n0}} m de large sur 120 m de long. Le
découpage retenu :

:::figure {"fn":"planZones","args":"tranche-plancher.figures.zones","titre":"Découpage du plancher de mezzanine en zones de coulage, à la date d'arrêt du suivi","num":1,"large":true,"legende":[{"n":1,"t":"zone de coulage, 15 × 24 m"},{"n":2,"t":"ligne de poutres PM1, entraxe 7,50 m"}],"voir":["Une zone fait deux travées de trame : le découpage suit la structure, il ne la coupe pas n'importe où.","Les lignes de poutres tombent sur les limites de zone : une reprise de bétonnage au droit d'une poutre est plus simple à traiter qu'en milieu de dalle.","L'état de chaque zone est lu dans les données de suivi : la figure est un tableau de bord, pas un dessin."],"erreur":"Découper en zones de surface égale sans regarder où tombent les poutres : la reprise se retrouve en pleine travée, là où l'effort tranchant est le plus fort et où le traitement de la reprise coûte le plus cher."}
:::

**Ordre de grandeur à retenir** : une zone de {{tranche-plancher.quantites.surface_m2::n0}} m² se coule
en {{tranche-plancher.durees.betonnage_h::n1}} heures de pompe. C'est la demi-journée de bétonnage qui
fixe la taille de la zone, pas l'inverse.

## S3 · Principes : d'où vient chaque nombre

C'est la partie la plus importante du module, et celle qu'on saute le plus souvent. **Trois familles
de nombres cohabitent ici, et elles n'ont pas la même valeur.**

| Famille | Exemple | Ce qu'elle vaut |
|---|---|---|
| **Géométrie** | {{tranche-plancher.quantites.beton_m3::n1}} m³ de béton, {{tranche-plancher.quantites.coffrage_m2::n0}} m² de coffrage | Juste à la géométrie près. Si la géométrie est bonne, le nombre est bon. |
| **Ratio V3** | {{tranche-plancher.quantites.acier_kg::n0}} kg d'acier | Un ordre de grandeur. Sa fourchette est celle du ratio : de {{tranche-plancher.quantites.fourchette_acier.min_kg::n0}} à {{tranche-plancher.quantites.fourchette_acier.max_kg::n0}} kg, soit une étendue de {{tranche-plancher.quantites.fourchette_acier.etendue_pct::n0}} %. |
| **Hypothèse de chantier V3** | cadences, effectifs, prix | Déclarée, avec fourchette et année. À recaler sur vos attachements dès que vous en avez. |

Le béton se calcule, il ne s'estime pas :

$$V = S \times e_{\text{dalle}} + n_{\text{poutres}} \times L_{\text{poutre}} \times b \times h_{\text{retombée}}$$

soit {{tranche-plancher.quantites.beton_dalle_m3::n1}} m³ de dalle et
{{tranche-plancher.quantites.beton_poutres_m3::n1}} m³ de poutres. L'acier, lui, ne se calcule pas
dans cette phase : il se **déduit d'un ratio**, ⟦V3|ratio d'acier d'une dalle|80 kg/m³|kg/m³|65 à 100|2026|ordre de grandeur de plancher courant, sans valeur réglementaire⟧
pour la dalle et ⟦V3|ratio d'acier d'une poutre|180 kg/m³|kg/m³|140 à 220|2026|ordre de grandeur de poutre de plancher, sans valeur réglementaire⟧
pour les poutres. D'où un ratio moyen de **{{tranche-plancher.quantites.ratio_acier_kg_m3::n1}} kg/m³**,
soit {{tranche-plancher.quantites.ratio_acier_kg_m2::n1}} kg par m² de plancher.

**Le piège du coffrage.** On écrit souvent « coffrage = surface ». C'est faux dès qu'il y a des
retombées : il faut ajouter les **joues** et le **fond** de poutre, et retirer la largeur de poutre de
la sous-face de dalle. Ici le rapport est de
{{tranche-plancher.quantites.ratio_coffrage_m2_par_m2::n2}} m² de coffrage par m² de plancher —
{{tranche-plancher.quantites.coffrage_detail_m2.sous_face_dalle::n0}} m² de sous-face,
{{tranche-plancher.quantites.coffrage_detail_m2.joues_de_poutres::n0}} m² de joues,
{{tranche-plancher.quantites.coffrage_detail_m2.fond_de_poutres::n0}} m² de fond, plus
{{tranche-plancher.quantites.coffrage_detail_m2.rives_pct::n0}} % de rives. Prendre 1,00 au lieu de
{{tranche-plancher.quantites.ratio_coffrage_m2_par_m2::n2}}, c'est sous-estimer le poste de
{{tranche-plancher.quantites.coffrage_detail_m2.rives_pct::n0}}0 % environ, sur le poste le plus cher
en main-d'œuvre.

## S4 · Étude de cas chiffrée : une zone, de bout en bout

### a. Des quantités aux durées

Une durée de tâche, c'est une quantité divisée par une cadence et par un effectif :

$$d = \frac{Q}{c \times n}$$

| Tâche | Quantité | Cadence V3 | Effectif | Durée |
|---|---:|---:|---:|---:|
| Coffrage | {{tranche-plancher.quantites.coffrage_m2::n0}} m² | 30 m²/j | {{gare.effectifs.coffreurs}} | {{tranche-plancher.durees.coffrage_j::n2}} j |
| Ferraillage des poutres | {{tranche-plancher.quantites.acier_poutres_kg::n0}} kg | 150 kg/j | {{gare.effectifs.ferrailleurs_poutres}} | {{tranche-plancher.durees.ferraillage_poutres_j::n2}} j |
| Ferraillage de la dalle | {{tranche-plancher.quantites.acier_dalle_kg::n0}} kg | 300 kg/j | {{gare.effectifs.ferrailleurs_dalle}} | {{tranche-plancher.durees.ferraillage_dalle_j::n2}} j |
| Bétonnage | {{tranche-plancher.quantites.beton_m3::n1}} m³ | 30 m³/h | {{gare.effectifs.equipe_betonnage}} | {{tranche-plancher.durees.betonnage_j::n2}} j |

:::encart {"genre":"voir","titre":"Contre-calcul n° 1 : les deux hypothèses se tiennent-elles ?"}
La durée de coffrage peut se calculer de deux façons : par la **cadence unitaire** multipliée par
l'effectif ({{tranche-plancher.durees.contre_calcul_duree_coffrage.voie_A_cadence_unitaire_x_effectif_j::n3}} j),
ou par un **rendement d'équipe** déclaré séparément
({{tranche-plancher.durees.contre_calcul_duree_coffrage.voie_B_rendement_d_equipe_j::n3}} j). Écart :
**{{tranche-plancher.durees.contre_calcul_duree_coffrage.ecart_pct::n2}} %**.

Ce que ce contrôle prouve, et seulement cela : **les deux hypothèses V3 sont mutuellement
cohérentes**. Il ne prouve pas qu'elles sont justes. Deux hypothèses fausses de la même façon
passeraient ce contrôle sans bruit. Seul un attachement réel tranche.
:::

### b. Des durées au cycle

La somme des durées vaut {{tranche-plancher.cycle_zone.somme_des_durees_j::n2}} jours. Le cycle réel
vaut **{{tranche-plancher.cycle_zone.duree_j::n2}} jours**. La différence —
{{tranche-plancher.cycle_zone.gain_du_recouvrement_j::n2}} jours, soit
{{tranche-plancher.cycle_zone.gain_pct::n0}} % — n'est pas une erreur : c'est le **recouvrement**. Le
ferraillage des poutres démarre avant que le coffrage soit terminé, celui de la dalle avant la fin
des poutres. C'est tout l'objet du chemin critique, et c'est pour cela qu'additionner des durées ne
donne jamais un planning.

:::figure {"fn":"sequence","args":"tranche-plancher.figures.sequence","titre":"Le cycle d'une zone, dans l'ordre","num":2,"large":true,"voir":["Le point d'arrêt n'est pas une étape administrative glissée entre deux tâches : c'est une tâche du planning, avec une durée, et il est sur le chemin critique.","La cure n'est pas du temps perdu : c'est du temps pendant lequel l'équipe travaille sur la zone suivante.","Le décoffrage laisse les étais de reprise en place — la zone n'est pas « finie » pour autant."]}
:::

:::figure {"fn":"gantt","args":"tranche-plancher.figures.gantt","titre":"Gantt d'une zone, avec les recouvrements","num":3,"large":true,"voir":["Les barres en brique sont sur le chemin critique : tout retard sur l'une décale la fin de la zone d'autant.","Le ferraillage des poutres commence avant la fin du coffrage : c'est un décalage négatif, pas une erreur de saisie.","Les durées ne sont pas saisies : elles viennent des quantités divisées par les cadences et les effectifs."],"erreur":"Saisir un planning en tapant des durées à dire d'expert, puis vérifier après coup si les effectifs suivent. L'ordre inverse — quantité, cadence, effectif, durée — est le seul qui permette de défendre un planning en réunion."}
:::

:::encart {"genre":"voir","titre":"Contre-calcul n° 2 : la durée du cycle, par deux algorithmes"}
La durée du cycle est calculée **deux fois par deux algorithmes différents** : le parcours
avant/arrière
({{tranche-plancher.cycle_zone.contre_calcul.voie_A_parcours_avant_arriere_j::n3}} j) et l'**énumération
exhaustive des chemins** du réseau
({{tranche-plancher.cycle_zone.contre_calcul.voie_B_enumeration_des_chemins_j::n3}} j). Écart :
**{{tranche-plancher.cycle_zone.contre_calcul.ecart_j}} jour**.

Ici les deux voies calculent exactement la même grandeur : elles **doivent** coïncider au chiffre
près. L'énumération est impraticable sur un vrai planning — le nombre de chemins explose — mais elle
est exacte sur un réseau de quelques tâches, donc idéale comme contre-calcul. Si elles divergeaient,
c'est le parcours avant/arrière qui serait faux.

Le moteur est par ailleurs **étalonné** sur quatre réseaux dont la durée se pose à la main (une
chaîne, deux branches parallèles, un recouvrement, une tâche isolée), et il refuse un circuit comme
un prédécesseur inconnu.
:::

### c. Du cycle au coût

| Poste | Quantité | Prix unitaire V3 | Montant |
|---|---:|---:|---:|
| Béton | {{tranche-plancher.quantites.beton_m3::n1}} m³ | 1 250 MAD/m³ | {{tranche-plancher.cout_zone.beton_MAD::n0}} MAD |
| Acier | {{tranche-plancher.quantites.acier_kg::n0}} kg | 17 MAD/kg | {{tranche-plancher.cout_zone.acier_MAD::n0}} MAD |
| Coffrage | {{tranche-plancher.quantites.coffrage_m2::n0}} m² | 180 MAD/m² | {{tranche-plancher.cout_zone.coffrage_MAD::n0}} MAD |
| **Total d'une zone** | | | **{{tranche-plancher.cout_zone.total_fournitures_et_mise_en_oeuvre_MAD::n0}} MAD** |

Soit **{{tranche-plancher.cout_zone.cout_au_m2_MAD::n0}} MAD/m²** de plancher, gros œuvre seul.

:::encart {"genre":"alerte","titre":"Le contrôle qui a échoué, et ce qu'il enseigne"}
La zone mobilise {{tranche-plancher.cout_zone.heures_de_main_oeuvre::n0}} heures de main-d'œuvre
directe. À ⟦V3|prix horaire d'un compagnon|45 MAD/h|MAD/h|35 à 60|2026|compagnon nu, charges comprises, sans encadrement⟧,
cela fait {{tranche-plancher.cout_zone.main_oeuvre_MAD::n0}} MAD, soit
**{{tranche-plancher.cout_zone.coherence_prix_horaire.part_constatee_pct::n1}} %** du total — alors que
la main-d'œuvre directe de production pèse normalement
⟦V3|part de main d'œuvre directe dans un prix posé|15 à 30 %|%|15 à 30|2026|gros œuvre, prix posé tout compris⟧.
Le contrôle **sort de la fourchette**.

Ce n'est pas une erreur de calcul. C'est que **les deux hypothèses ne décrivent pas la même chose** :
le prix horaire est celui d'un compagnon nu ; les heures comptées sont celles des quatre équipes de
production seules, sans encadrement, grutier, approvisionnement ni moyens ; et les prix unitaires sont
des prix **posés**, qui portent en plus les matériaux, le matériel, les frais de chantier et la marge.
Pour que les deux se rejoignent, il faudrait un taux horaire de
{{tranche-plancher.cout_zone.coherence_prix_horaire.prix_horaire_implique_par_les_prix_unitaires_MAD::n0}} MAD/h,
soit {{tranche-plancher.cout_zone.coherence_prix_horaire.facteur::n1}} fois le taux déclaré.

**La ligne « main-d'œuvre » n'est donc pas un poste à additionner au total : ce serait compter la
main-d'œuvre deux fois.** C'est l'erreur de métré la plus fréquente, et c'est exactement ce qu'un
sous-détail de prix met à plat poste par poste — module D1.
:::

### d. Du coût au planning du plancher

Les {{tranche-plancher.planning_plancher.nb_zones}} zones s'enchaînent à une cadence de
**{{tranche-plancher.planning_plancher.cadence_zone_j::n1}} jours par zone** : l'équipe de coffrage
attaque la zone suivante pendant que la précédente est en cure. Le plancher complet prend
**{{tranche-plancher.planning_plancher.duree_totale_j::n1}} jours ouvrés**.

:::figure {"fn":"histogramme","args":"tranche-plancher.figures.effectifs","titre":"Effectif présent sur le plancher, jour par jour","num":4,"large":true,"voir":["Le creux de démarrage et la décroissance de fin sont normaux : seule la partie centrale est en régime.","La pointe donne le dimensionnement de la base-vie et des moyens — c'est elle qu'il faut regarder, pas la moyenne.","La courbe est dentelée : chaque dent est un changement de poste à l'intérieur d'un cycle."],"erreur":"Lisser cet histogramme en moyenne et dimensionner la base-vie dessus. Le jour de pointe, il manque des vestiaires et des réfectoires pour tout le monde."}
:::

## S5 · Erreurs fréquentes, et ce qu'elles coûtent

| Erreur | Comment elle se voit | Ce qu'elle coûte |
|---|---|---|
| Coffrage compté à la surface de dalle | le ratio tombe à 1,00 au lieu de {{tranche-plancher.quantites.ratio_coffrage_m2_par_m2::n2}} | ~{{tranche-plancher.quantites.coffrage_detail_m2.rives_pct::n0}}0 % du poste le plus cher en main-d'œuvre |
| Main-d'œuvre additionnée à un prix posé | le total gonfle sans que les quantités bougent | double compte, et une situation rejetée au visa |
| Durées saisies à dire d'expert | aucun lien entre l'effectif et la durée | un planning indéfendable en réunion |
| Zone découpée sans regarder les poutres | reprise de bétonnage en pleine travée | traitement de reprise, et un point de contrôle en plus |
| Avancement déclaré à vue de nez | l'écart n'apparaît qu'au contre-calcul (§ S6) | une situation surévaluée, puis un rattrapage brutal |
| Cure comptée comme du temps perdu | le cycle paraît plus long qu'il n'est | une cadence annoncée trop pessimiste, et des moyens surdimensionnés |

## S6 · Du planning au reporting : la valeur acquise

À la date d'arrêt — **{{tranche-plancher.suivi.libelle_arret}}**, déduite du planning et non écrite à
la main — {{valeur-acquise.zones_prevues}} zones étaient prévues,
{{valeur-acquise.zones_realisees_equivalentes::n2}} sont réalisées.

| Indicateur | Valeur |
|---|---:|
| Budget à l'achèvement (BAC) | {{valeur-acquise.budget_a_l_achevement_BAC_MAD::n0}} MAD |
| Valeur planifiée (VP) | {{valeur-acquise.valeur_planifiee_VP_MAD::n0}} MAD |
| Valeur acquise (VA) | {{valeur-acquise.valeur_acquise_VA_MAD::n0}} MAD |
| Coût réel (CR) | {{valeur-acquise.cout_reel_CR_MAD::n0}} MAD |
| **CPI** | **{{valeur-acquise.CPI::n3}}** |
| **SPI** | **{{valeur-acquise.SPI::n3}}** |
| Prévision à terminaison (EAC) | {{valeur-acquise.prevision_a_terminaison_EAC_MAD::n0}} MAD |
| Dérive prévue | **+{{valeur-acquise.derive_prevue_MAD::n0}} MAD** |

{{valeur-acquise.lecture}}

:::figure {"fn":"courbeS","args":"tranche-plancher.figures.courbe_s","titre":"Courbe en S : avancement prévu et avancement réel à la date d'arrêt","num":5,"large":true,"voir":["La courbe réelle s'arrête à la date d'arrêt : au-delà, il n'y a pas de donnée, et une courbe qui continuerait serait une prévision déguisée en constat.","L'écart vertical à la date d'arrêt est le retard en valeur, pas en jours : c'est SV.","La pente de la courbe réelle, et non sa position, dit si le retard se creuse ou se résorbe."],"erreur":"Prolonger la courbe réelle jusqu'à la fin pour « montrer qu'on rattrape ». Un constat et une prévision ne se tracent pas du même trait."}
:::

:::encart {"genre":"alerte","titre":"Contre-calcul n° 3 : l'avancement déclaré colle-t-il aux relevés ?"}
La valeur acquise est calculée **deux fois**. Voie A, par les coûts : budget à l'achèvement ×
avancement déclaré → {{valeur-acquise.contre_calcul.voie_A_par_les_couts_MAD::n0}} MAD. Voie B, par
les **quantités relevées sur le chantier** (attachements) × prix unitaires →
{{valeur-acquise.contre_calcul.voie_B_par_les_quantites_MAD::n0}} MAD.

**Écart : {{valeur-acquise.contre_calcul.ecart_pct::n2}} %**, au-delà de la tolérance de
{{valeur-acquise.contre_calcul.tolerance_pct::n0}} %. Le contrôle **sonne**.

Traduit en avancement : les relevés impliquent
{{valeur-acquise.contre_calcul.avancement_implique_par_les_releves_zones::n2}} zones, là où
{{valeur-acquise.contre_calcul.avancement_declare_zones::n2}} sont déclarées. L'écart est de
{{valeur-acquise.contre_calcul.ecart_d_avancement_zones::n3}} zone — une poignée de pour cent sur la
zone en cours, invisible dans un tableau de bord, et pourtant suffisante pour qu'une situation soit
rejetée au visa.

C'est **la** dérive que ce contrôle existe pour attraper : un avancement estimé à vue de nez sur la
zone en cours. Ce que la maîtrise d'œuvre fera : demander les attachements, pas la déclaration.

**Pourquoi la voie B est indépendante, cette fois.** Une première version multipliait les quantités
*théoriques* par l'avancement *déclaré* : elle était algébriquement identique à la voie A, et l'écart
valait zéro par construction. Deux voies ne sont indépendantes que si elles ne partagent pas leur
entrée décisive. Ici la voie B part des relevés, pas de l'avancement.
:::

## S7 · Double lecture : entreprise et maîtrise d'œuvre

Le même plancher, vu des deux côtés. C'est la paire de casquettes qui fait l'ingénieur complet (§ 1).

| Moment | Ce que fait l'entreprise (casquette 2) | Ce que vérifie la maîtrise d'œuvre (casquette 6) |
|---|---|---|
| Avant travaux | soumet le plan de phasage et le découpage en zones | vise le phasage ; vérifie que les reprises tombent au droit des poutres et non en travée |
| Coffrage | monte tables et étaiement, règle les niveaux | contrôle la **stabilité de l'étaiement** et la géométrie avant tout ferraillage |
| Ferraillage | pose, cale, attache | **point d'arrêt** : enrobage, calage, recouvrements, propreté du fond — rien ne se coule avant levée |
| Bétonnage | coule, vibre, surface, protège | prélève les éprouvettes, note les conditions, vérifie le traitement de reprise |
| Cure et décoffrage | maintient la cure, décoffre, laisse les étais de reprise | contrôle le **critère de décoffrage** et la présence des étais de reprise |
| Situation | présente l'avancement et les attachements | **recoupe la déclaration avec les quantités relevées** (§ S6) avant de viser |

**Le point d'arrêt est une tâche du planning.** Dans le réseau de ce module il dure un quart de jour
et il est **sur le chemin critique**. Un point d'arrêt qu'on oublie de planifier devient un point
d'arrêt qu'on subit : l'équipe attend, ou — pire — on coule sans visa et la non-conformité se règle
au marteau-piqueur.

## S8 · Fiche mémo

:::memo
## Fiche mémo — cycle d'une zone de plancher

**Les cinq nombres de la zone**

| | |
|---|---:|
| Surface | {{tranche-plancher.quantites.surface_m2::n0}} m² |
| Béton | {{tranche-plancher.quantites.beton_m3::n1}} m³ |
| Coffrage | {{tranche-plancher.quantites.coffrage_m2::n0}} m² ({{tranche-plancher.quantites.ratio_coffrage_m2_par_m2::n2}} m²/m²) |
| Acier — hypothèse de ratio, ± {{tranche-plancher.quantites.fourchette_acier.etendue_pct::n0}} % | {{tranche-plancher.quantites.acier_kg::n0}} kg |
| Cycle | {{tranche-plancher.cycle_zone.duree_j::n1}} j · cadence {{tranche-plancher.planning_plancher.cadence_zone_j::n1}} j/zone |

**Les quatre contrôles avant de viser une situation**

1. Le ratio de coffrage est-il > 1,00 ? Sinon les joues de poutres ont été oubliées.
2. La main-d'œuvre est-elle additionnée à un prix posé ? Si oui, double compte.
3. L'avancement déclaré est-il recoupé par les **quantités relevées** ? Écart > 1 % → attachements.
4. Les durées viennent-elles des quantités, ou d'un dire d'expert ?

**Points d'arrêt à viser (maîtrise d'œuvre)**

- stabilité de l'étaiement et géométrie, **avant** ferraillage ;
- **ferraillage avant coulage** : enrobage, calage, recouvrements, propreté — le seul qui soit
  irréversible une fois le béton coulé ;
- critère de décoffrage atteint, et étais de reprise en place.

**Les pièges, en une ligne chacun** — coffrage compté à la surface · main-d'œuvre comptée deux fois ·
durées à dire d'expert · reprise en pleine travée · avancement à vue de nez · cure comptée comme
perdue.
:::

## S6b · Exercices

:::exercice {"titre":"1 · Refaire le métré d'une zone à la main","niveau":"application"}
Reprenez la géométrie : zone de {{tranche-plancher.quantites.surface_m2::n0}} m²,
dalle de 25 cm, {{tranche-plancher.quantites.n_poutres}} poutres de 24,00 m, retombée 0,50 m sous
dalle, largeur 0,35 m.

Calculez le volume de béton, puis la surface de coffrage en détaillant sous-face, joues et fond.

**Corrigé.** Dalle : 360 × 0,25 = {{tranche-plancher.quantites.beton_dalle_m3::n1}} m³. Poutres :
2 × 24,00 × 0,35 × 0,50 = {{tranche-plancher.quantites.beton_poutres_m3::n1}} m³. Total
**{{tranche-plancher.quantites.beton_m3::n1}} m³**.
Coffrage : sous-face 360 − (2 × 24,00 × 0,35) = {{tranche-plancher.quantites.coffrage_detail_m2.sous_face_dalle::n0}} m² ;
joues 2 × 24,00 × 0,50 × 2 = {{tranche-plancher.quantites.coffrage_detail_m2.joues_de_poutres::n0}} m² ;
fond 2 × 24,00 × 0,35 = {{tranche-plancher.quantites.coffrage_detail_m2.fond_de_poutres::n0}} m².
Plus {{tranche-plancher.quantites.coffrage_detail_m2.rives_pct::n0}} % de rives →
**{{tranche-plancher.quantites.coffrage_m2::n0}} m²**.
:::

:::exercice {"titre":"2 · L'effet d'un effectif sur le cycle","niveau":"application"}
Les ferrailleurs de dalle passent de {{gare.effectifs.ferrailleurs_dalle}} à 12. Que devient la durée
de ferraillage de dalle, et le cycle de la zone gagne-t-il autant ?

**Corrigé.** La durée passe de {{tranche-plancher.durees.ferraillage_dalle_j::n2}} j à
{{tranche-plancher.quantites.acier_dalle_kg::n0}} / (300 × 12) = 2,42 j, soit 0,58 j de moins. Mais le
cycle **ne gagne pas 0,58 j** : le ferraillage de dalle est sur le chemin critique, donc le gain s'y
reporte, *jusqu'à ce qu'un autre chemin devienne critique*. C'est la règle qu'il faut retenir :
**renforcer une tâche critique déplace le problème, elle ne le supprime pas.** Refaites tourner le
réseau avant d'annoncer un gain en réunion.
:::

:::exercice {"titre":"3 · Défendre une cadence en réunion","niveau":"probleme"}
Le maître d'ouvrage demande le plancher en 25 jours ouvrés au lieu de
{{tranche-plancher.planning_plancher.duree_totale_j::n1}}. Vous ne pouvez ni changer les quantités ni
toucher à la cure. Quels leviers reste-t-il, et lequel défendez-vous ?

**Corrigé.** Trois leviers, et un seul est honnête.
**(a) Augmenter les effectifs.** Le cycle est piloté par la tâche la plus longue, le ferraillage de
dalle. Passer de {{gare.effectifs.ferrailleurs_dalle}} à 12 ferrailleurs ramène la cadence de
{{tranche-plancher.planning_plancher.cadence_zone_j::n1}} à environ 2,8 j, soit 8 × 2,8 + cycle ≈
28 j. Insuffisant, et l'histogramme d'effectifs passe au-dessus de la base-vie.
**(b) Découper en zones plus petites.** Plus de zones, cycle plus court chacune, mais plus de reprises
de bétonnage et plus de points d'arrêt. On gagne sur le papier, on perd en qualité et en contrôle.
**(c) Dédoubler les équipes sur deux zones en parallèle.** C'est le seul levier qui tienne : deux
fronts indépendants, chacun à sa cadence. Il faut deux jeux de tables coffrantes —
{{gare.materiel.tables_coffrantes_m2}} m² de plus — et la grue doit suivre.
**Ce qu'il faut dire en réunion** : « 25 jours est atteignable en dédoublant le front, au prix d'un
second jeu de coffrage et d'un pic d'effectif de X personnes. Voici les deux plannings. » Pas « on
va essayer ».
:::

:::exercice {"titre":"4 · Trouver l'erreur dans cette situation de travaux","niveau":"revue critique"}
Un sous-traitant présente la situation suivante pour la zone 4, déclarée à 60 % :

| Poste | Quantité déclarée | Prix unitaire | Montant |
|---|---:|---:|---:|
| Béton | 59,0 m³ | 1 250 | 73 750 |
| Acier | 5 227 kg | 17 | 88 859 |
| Coffrage | 255 m² | 180 | 45 900 |
| Main-d'œuvre | 241 h | 45 | 10 845 |
| **Total** | | | **219 354** |

Trois choses ne vont pas. Lesquelles ?

**Corrigé.**
1. **La main-d'œuvre est additionnée** à des prix unitaires qui sont des prix posés : double compte de
   10 845 MAD. Le total correct est 208 509 MAD.
2. **Le coffrage est sous-compté.** 60 % de {{tranche-plancher.quantites.coffrage_m2::n0}} m² font
   255 m² — ce qui est juste *si* le ratio retenu est le bon. Mais 255 / (0,60 × 360) = 1,18 :
   cohérent. Le vrai problème est ailleurs → voir 3.
3. **L'avancement de 60 % n'est recoupé par rien.** C'est une déclaration, pas un relevé. Le contrôle
   du § S6 montre qu'à l'échelle du plancher, l'écart entre déclaration et relevés atteint déjà
   {{valeur-acquise.contre_calcul.ecart_pct::n2}} %. **Ce qu'il faut exiger avant de viser : les
   attachements**, pas un pourcentage.

*Le point 2 est un leurre : les chiffres sont cohérents entre eux. Savoir reconnaître ce qui est juste
fait partie du contrôle — un visa qui refuse tout ne vaut pas mieux qu'un visa qui accepte tout.*
:::

## S7b · Quiz

:::exercice {"titre":"Six questions pour vérifier","niveau":"application"}
**1. Pourquoi la zone de coulage, et pas le mètre carré, est-elle l'unité de suivi ?**
Parce qu'elle est à la fois une quantité, une durée, un coût et un jalon binaire — coulé ou non. Tout
le reste s'y raccroche.

**2. Pourquoi la somme des durées ne donne-t-elle pas le cycle ?**
À cause des recouvrements : ici {{tranche-plancher.cycle_zone.gain_pct::n0}} % de différence. Seul le
chemin critique donne la durée.

**3. Le contre-calcul de la durée de coffrage prouve quoi, exactement ?**
Que les deux hypothèses V3 sont **mutuellement cohérentes**. Rien de plus. Deux hypothèses fausses de
la même façon le passeraient.

**4. Pourquoi ne faut-il pas additionner la main-d'œuvre au total ?**
Parce que les prix unitaires sont des prix **posés** : la main-d'œuvre y est déjà. L'additionner la
compte deux fois.

**5. Qu'est-ce qui rend la voie B de la valeur acquise indépendante ?**
Elle part des **quantités relevées**, pas de l'avancement déclaré. Si elle partait du déclaré, elle
serait algébriquement identique à la voie A.

**6. Quel est le seul point d'arrêt irréversible du cycle ?**
Le visa du **ferraillage avant coulage**. Après le bétonnage, une non-conformité d'enrobage ou de
recouvrement ne se corrige qu'en démolissant.
:::

## Ce qui reste suspendu, et ce que vous devez valider

:::encart {"genre":"attente","titre":"Trois renvois au module de calcul, en attente des normes"}
1. **L'épaisseur de dalle et la section de poutre** sont des prédimensionnements V3. La vérification
   — flexion, effort tranchant, flèche — appartient au module **B3**, suspendu.
2. **Le ratio d'acier** remplace un métré de ferraillage. Le vrai métré sort de la nomenclature, donc
   de **B3** également.
3. **Le critère de décoffrage** est cité comme point d'arrêt sans valeur chiffrée : la résistance à
   atteindre est une valeur normative, interdite ici (§ 5.0).

À la levée de la suspension, ce module sera relu : les ratios céderont la place aux quantités
calculées, et l'écart entre les deux sera lui-même instructif.
:::

**Ce que vous validez maintenant** (§ 5.3) : la **forme** — longueur, densité, équilibre entre texte,
tableaux et figures ; la **profondeur** — chaque nombre arrive-t-il avec son origine et sa limite ;
l'**angle** — la double lecture entreprise/maîtrise d'œuvre est-elle au bon niveau ; et la question
que le prompt pose explicitement : **la 3D apporterait-elle ici plus qu'une bonne figure ?** Ce module
n'en contient aucune, délibérément — le phasage 3D appartient à C3. Dites-moi si elle vous manque.
