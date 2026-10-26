---
id: B3e
titre: Béton armé en exécution — lire un plan, le métrer, le contrôler
fil: Palier 1 · module 5 — conception et calcul, volet exécution
resume: Sur un chantier, vous ne calculez pas le ferraillage : vous vérifiez que ce qui est posé est ce que le plan visé montre. Ce module traite ce qui ne dépend d'aucune norme — lire, métrer, contrôler — et dit exactement où s'arrête ce qu'on peut affirmer sans elles.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · le plan de ferraillage est FICTIF et non dimensionné · aucune disposition constructive n'est avancée
pied: Exemple pédagogique — ne remplace ni une note de calcul, ni un plan d'exécution visé, ni le contrôle d'un bureau d'études ou de contrôle.
donnees: ferraillage, tranche-plancher, gare
---

## S1 · Ce que ce module fait, et ce qu'il refuse de faire

Vous connaissez le béton armé. Ce module ne vous réapprend ni ce qu'est un chapeau, ni pourquoi
l'acier est en bas en travée. Il traite la partie du métier que personne n'enseigne et que vous
faites tous les jours : **ce qu'on fait d'un plan de ferraillage quand on est du côté du chantier.**

Cette partie-là ne dépend d'**aucune** norme, et c'est ce qui la rend accessible aujourd'hui, en
pleine phase § 5.0 :

1. **lire** un plan dans le bon ordre, et savoir ce qu'on y cherche à chaque étape ;
2. **métrer** une nomenclature, c'est-à-dire transformer des traits en kilogrammes — un calcul qui
   ne repose que sur des longueurs et une masse volumique, donc **sûr** ;
3. **contrôler** un ferraillage posé, contre le plan visé et non contre un règlement ;
4. **savoir où s'arrête** ce qu'on peut affirmer sans les normes, et le dire plutôt que de l'inventer.

Ce que ce module ne fait pas, et ne fera pas tant que les documents manquent : dimensionner. Aucune
section n'est justifiée ici, aucune longueur d'ancrage n'est avancée, aucun espacement maximal de
cadres n'est cité. Le module **B3c** le fera le jour où BAEL, RPS et CPS seront fournis.

::: encart {"genre":"attente","titre":"Le plan de ce module est FICTIF, et c'est une donnée, pas un résultat"}
Tout ce module s'appuie sur un plan de ferraillage d'une zone de plancher de mezzanine : deux poutres
PM1 de {{ferraillage.nomenclature.longueur_de_poutre_m::n2}} m et la dalle DM1 de
{{ferraillage.nappes.surface_m2::n0}} m². **Rien dans ce plan n'est dimensionné.** Les diamètres et
les espacements ont été **calibrés** sur les ratios V3 du projet pour que le plan ait l'ordre de
grandeur d'un plancher de ce type — un calibrage n'est pas un dimensionnement et ne vaut pas
vérification.

Ce n'est pas une faiblesse du module, c'est sa thèse : **vous ne produisez pas le plan, vous le
recevez.** Le plan est une entrée de votre travail, exactement comme ici. Ce que vous en faites —
lire, métrer, contrôler — ne change pas selon que le calcul derrière est juste ou faux. Et c'est
heureux, parce que vous n'êtes pas en position de le refaire.
:::

## S2 · L'idée centrale : vous ne contrôlez pas un calcul, vous contrôlez une conformité

Voici la confusion la plus coûteuse du métier, et elle se joue en une phrase.

Un ingénieur de suivi qui reçoit un plan de ferraillage a deux réflexes possibles. Le premier :
« est-ce que ce ferraillage est suffisant ? ». Le second : « est-ce que ce qui est posé est ce que ce
plan montre ? ». **Les deux questions sont légitimes ; une seule est la vôtre.**

La première appartient au bureau d'études, qui l'a instruite dans sa note de calcul, et au contrôle
technique, qui l'a visée. Elle a été traitée **avant** que le plan n'arrive sur le chantier, par des
gens qui avaient les charges, les combinaisons et le temps. La reprendre sur un coin de table, entre
deux coulages, c'est faire mal un travail qui a déjà été fait bien.

La seconde n'appartient qu'à vous. **Personne d'autre ne verra jamais ce qui a été réellement
posé.** Le bureau d'études ne vient pas compter les barres ; le contrôle technique passe par
sondage ; et deux heures après le coulage, plus personne ne peut rien constater. Vous êtes le seul
témoin d'un événement irréversible.

:::encart {"genre":"voir","titre":"La conséquence pratique"}
Le temps que vous passez à vous demander si trois HA25 suffisent est du temps que vous ne passez pas
à compter les barres posées. Le premier travail est redondant ; le second est unique. Quand le
planning serre — et il serre toujours au moment du visa de ferraillage, parce que le coulage est
derrière — c'est le second qui doit survivre.

Cela ne veut **pas** dire qu'on se tait quand quelque chose choque. Un plan qui paraît anormalement
léger, un chapeau qui s'arrête visiblement trop tôt, une poutre qui n'a pas le même ferraillage que
sa jumelle : ça se signale, par écrit, au BET. Signaler n'est pas recalculer. C'est même tout
l'inverse : on signale **parce qu'on ne peut pas trancher**.
:::

## S3 · Principes

### a. Lire un plan de ferraillage : sept étapes, dans cet ordre

L'ordre n'est pas décoratif. Il va du général au détail, et chaque étape conditionne la suivante. Un
plan lu en commençant par les diamètres se lit deux fois.

| | Où on regarde | Ce qu'on y cherche | Pourquoi là, et pas ailleurs |
|---:|---|---|---|
| {{ferraillage.lire_un_plan.etapes.0.n}} | **{{ferraillage.lire_un_plan.etapes.0.quoi}}** | {{ferraillage.lire_un_plan.etapes.0.ce_qu_on_y_cherche}} | {{ferraillage.lire_un_plan.etapes.0.pourquoi}} |
| {{ferraillage.lire_un_plan.etapes.1.n}} | **{{ferraillage.lire_un_plan.etapes.1.quoi}}** | {{ferraillage.lire_un_plan.etapes.1.ce_qu_on_y_cherche}} | {{ferraillage.lire_un_plan.etapes.1.pourquoi}} |
| {{ferraillage.lire_un_plan.etapes.2.n}} | **{{ferraillage.lire_un_plan.etapes.2.quoi}}** | {{ferraillage.lire_un_plan.etapes.2.ce_qu_on_y_cherche}} | {{ferraillage.lire_un_plan.etapes.2.pourquoi}} |
| {{ferraillage.lire_un_plan.etapes.3.n}} | **{{ferraillage.lire_un_plan.etapes.3.quoi}}** | {{ferraillage.lire_un_plan.etapes.3.ce_qu_on_y_cherche}} | {{ferraillage.lire_un_plan.etapes.3.pourquoi}} |
| {{ferraillage.lire_un_plan.etapes.4.n}} | **{{ferraillage.lire_un_plan.etapes.4.quoi}}** | {{ferraillage.lire_un_plan.etapes.4.ce_qu_on_y_cherche}} | {{ferraillage.lire_un_plan.etapes.4.pourquoi}} |
| {{ferraillage.lire_un_plan.etapes.5.n}} | **{{ferraillage.lire_un_plan.etapes.5.quoi}}** | {{ferraillage.lire_un_plan.etapes.5.ce_qu_on_y_cherche}} | {{ferraillage.lire_un_plan.etapes.5.pourquoi}} |
| {{ferraillage.lire_un_plan.etapes.6.n}} | **{{ferraillage.lire_un_plan.etapes.6.quoi}}** | {{ferraillage.lire_un_plan.etapes.6.ce_qu_on_y_cherche}} | {{ferraillage.lire_un_plan.etapes.6.pourquoi}} |

{{ferraillage.lire_un_plan.la_regle}}

:::figure {"fn":"coupeSection","args":"ferraillage.figures.coupe","titre":"Coupe de la poutre PM1 — les barres filantes","num":1,"motifs":["beton"],"legende":[{"n":1,"t":"béton — b × h de la section"},{"n":2,"t":"barres longitudinales filantes, lits inférieur et supérieur"},{"n":3,"t":"cadre, tracé sur son axe"}],"options":{"cotes":true,"aciers":true,"enrobage":true},"voir":["La coupe est la seule vue où l'enrobage se lit. Il vaut {{gare.armatures.plan.poutre_PM1.section_cm.enrobage}} cm ici, mesuré à la peau du CADRE et non à celle des barres longitudinales : c'est le cadre qui est le plus à l'extérieur.","Cette coupe ne montre QUE les filantes : {{ferraillage.figures.coupe.section.inf.n}} HA{{ferraillage.figures.coupe.section.inf.dia_mm}} en bas ({{ferraillage.figures.coupe.section.inf.repere}}), {{ferraillage.figures.coupe.section.sup.n}} HA{{ferraillage.figures.coupe.section.sup.dia_mm}} en haut ({{ferraillage.figures.coupe.section.sup.repere}}). À mi-travée le lit inférieur en porte trois de plus (A2), sur appui le lit supérieur cinq de plus (B2) : un plan réel dessine PLUSIEURS coupes, précisément parce que les lits changent le long de la poutre. L'élévation, elle, dira où chacune commence et s'arrête — jamais combien il y en a dans l'épaisseur.","Un cadre se dessine sur son AXE. Son périmètre vaut {{ferraillage.cadres.perimetre_m::n3}} m, soit la section d'axe {{ferraillage.cadres.section_axe_cadre_m.b::n3}} × {{ferraillage.cadres.section_axe_cadre_m.h::n3}} m — et non le périmètre de la section de béton, qui le surestimerait de 14 %."],"erreur":"Mesurer l'enrobage à la barre longitudinale. On gagne un demi-diamètre de cadre sur le papier et on le perd sur l'ouvrage : la peau du cadre se retrouve plus près du coffrage que l'enrobage annoncé, et c'est elle qui rouille en premier."}
:::

### b. L'élévation : là où se lisent les arrêts de barres

Une coupe dit **combien**. Une élévation dit **où**. C'est l'information la plus dense d'un plan de
ferraillage, et la plus souvent mal posée, parce qu'elle ne se vérifie plus après coulage.

:::figure {"fn":"elevationPoutre","args":"ferraillage.figures.elevation","titre":"Élévation ferraillée de la poutre PM1 — trois travées de 8,00 m","num":2,"large":true,"options":{"aciers":true,"cotes":true,"appuis":true},"voir":["Chaque trait est un repère, et chaque trait a DEUX extrémités marquées : c'est là qu'est l'enseignement. Une barre n'est pas « dans la poutre », elle commence quelque part et s'arrête quelque part.","Les filantes A1 et B1 courent sur les {{ferraillage.nomenclature.longueur_de_poutre_m::n2}} m. Les renforts A2 sont centrés sur les travées, les chapeaux B2 à cheval sur les appuis intermédiaires : la logique se voit sans aucun calcul, c'est la forme du moment.","Chaque repère occupe sa propre ligne : c'est une convention de LECTURE, pas la position réelle dans l'épaisseur. Où se trouve chaque lit se lit en coupe (figure 1), jamais en élévation — et c'est la raison d'être des deux vues.","L'échelle verticale est EXAGÉRÉE. À l'échelle, une poutre de {{gare.elements.poutres.0.h_m::n2}} m sur {{ferraillage.nomenclature.longueur_de_poutre_m::n0}} m ferait quelques pixels de haut et aucun lit n'y serait lisible. Les cotes, elles, restent celles des données."],"erreur":"Lire une élévation comme un schéma de principe. Les abscisses d'arrêt sont des cotes, pas des intentions : la barre B2 va de 5,60 à 10,40 m, et une barre arrêtée à 9,00 m n'est pas « à peu près la même »."}
:::

**D'où viennent ces abscisses ?** D'une règle de dimensionnement, et elle est **⏸** : une longueur
d'arrêt de barre se déduit du diagramme des moments et des longueurs d'ancrage, qui sont dans le
BAEL. Ce module ne peut donc pas vous dire si 5,60 est juste. Il peut vous dire — et c'est ce qui
vous sert — que **5,60 est ce que le plan visé porte**, et que c'est contre ce 5,60 que vous
contrôlerez la pose.

### c. Métrer : des traits vers des kilogrammes

Le métré d'un plan de ferraillage est le seul calcul de ce module qui soit **sûr**. Il ne repose que
sur deux choses : des longueurs, qui sont des cotes du plan, et la masse d'un mètre de barre, qui
est une constante physique.

$$ m_\ell = \frac{\pi}{4}\, d^2\, \rho \qquad\text{avec } \rho = 7\,850\ \text{kg/m}^3 $$

HA12 donne 0,888 kg/m, HA20 donne 2,466, HA25 donne 3,853. Ce ne sont pas des valeurs
réglementaires : ce sont des sorties arrondies de cette formule, et c'est pourquoi le tableau du
commerce sert d'**étalonnage externe** à la bibliothèque de calcul (§ 3.3). Les dix diamètres
courants ont été recalculés et comparés au tableau : écart maximal 0,5 g/m.

La longueur à façonner n'est **pas** la cote du dessin : c'est la **longueur développée**, partie
droite plus retours d'équerre. Et pour une filante plus longue qu'une barre du commerce, il faut
ajouter les recouvrements :

$$ L_{\text{façonnée}} = L_{\text{droite}} + \sum L_{\text{retours}} + n_{\text{rec}} \cdot L_{\text{rec}} $$

Le **nombre** de recouvrements est géométrique, et il se compte en raisonnant sur la **couverture**,
pas sur une simple division. $k$ barres de $L_c$ recouvertes de $L_r$ ne couvrent que
$k L_c - (k-1) L_r$ : chaque recouvrement consomme de la barre sans couvrir d'ouvrage. D'où

$$ k = \left\lceil \frac{L - L_r}{L_c - L_r} \right\rceil \qquad n_{\text{rec}} = k - 1 $$

Une filante de {{ferraillage.nomenclature.longueur_de_poutre_m::n0}} m faite de barres de
{{gare.armatures.conventions.longueur_commerciale_m::n0}} m en demande
**{{ferraillage.nomenclature.lignes.0.recouvrements_par_barre}}**, et aucun règlement n'y peut rien.

:::encart {"genre":"piege","titre":"Le réflexe qui manque une barre sur deux"}
On écrit volontiers $\lceil L/L_c \rceil - 1$ : pour 24,00 m en barres de 12,00 m, cela donne
**1 recouvrement, donc 2 barres**. Or deux barres de 12 m recouvertes de 1 m ne couvrent que
**23,00 m**. Il en faut trois, et la filante pèse
{{ferraillage.nomenclature.lignes.0.longueur_faconnee_m::n2}} m d'acier pour
{{ferraillage.nomenclature.longueur_de_poutre_m::n2}} m d'ouvrage.

L'erreur n'est pas de 4 % sur le métré : elle est **physique**. On ne coupe pas 25 m de barre dans
du stock de 12 m. Un métré faux de ce côté-là se solde par une livraison qui ne permet pas de poser
le ferraillage, le jour où l'on pose.
:::

Leur **longueur**, en revanche, est réglementaire : elle reste **⏸**. Celle du plan
fictif vaut ⟦V3|longueur de recouvrement portée par le plan fictif|1,00|m|0,60 à 1,60|2026|hypothèse de métré, non une disposition : une longueur de recouvrement réelle se lit dans le BAEL et dépend du diamètre, de l'adhérence et de la position de la barre⟧ m, déclarée comme hypothèse de métré.

### d. Deux ouvrages, deux méthodes de métré

Une poutre a une **nomenclature** : une ligne par repère. Une dalle a des **nappes** : on compte
$100/s$ barres par mètre et on multiplie. Chercher une nomenclature de dalle sur un plan, c'est
chercher une pièce qui n'existe pas — c'est la première maladresse d'un métreur qui débute, et elle
coûte une demi-journée.

{{ferraillage.nappes.lecture}}

## S4 · L'étude de cas : métrer, cadrer, commander

### a. La nomenclature de la poutre PM1

| Repère | Rôle | Nb | Ø | L. unitaire | Recouvr. | L. façonnée | L. totale | Masse |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **{{ferraillage.nomenclature.lignes.0.repere}}** | {{ferraillage.nomenclature.lignes.0.role}} | {{ferraillage.nomenclature.lignes.0.nombre}} | HA{{ferraillage.nomenclature.lignes.0.dia_mm}} | {{ferraillage.nomenclature.lignes.0.longueur_unitaire_m::n2}} m | {{ferraillage.nomenclature.lignes.0.recouvrements_par_barre}} | {{ferraillage.nomenclature.lignes.0.longueur_faconnee_m::n2}} m | {{ferraillage.nomenclature.lignes.0.longueur_totale_m::n1}} m | **{{ferraillage.nomenclature.lignes.0.masse_kg::n1}} kg** |
| **{{ferraillage.nomenclature.lignes.1.repere}}** | {{ferraillage.nomenclature.lignes.1.role}} | {{ferraillage.nomenclature.lignes.1.nombre}} | HA{{ferraillage.nomenclature.lignes.1.dia_mm}} | {{ferraillage.nomenclature.lignes.1.longueur_unitaire_m::n2}} m | {{ferraillage.nomenclature.lignes.1.recouvrements_par_barre}} | {{ferraillage.nomenclature.lignes.1.longueur_faconnee_m::n2}} m | {{ferraillage.nomenclature.lignes.1.longueur_totale_m::n1}} m | **{{ferraillage.nomenclature.lignes.1.masse_kg::n1}} kg** |
| **{{ferraillage.nomenclature.lignes.2.repere}}** | {{ferraillage.nomenclature.lignes.2.role}} | {{ferraillage.nomenclature.lignes.2.nombre}} | HA{{ferraillage.nomenclature.lignes.2.dia_mm}} | {{ferraillage.nomenclature.lignes.2.longueur_unitaire_m::n2}} m | {{ferraillage.nomenclature.lignes.2.recouvrements_par_barre}} | {{ferraillage.nomenclature.lignes.2.longueur_faconnee_m::n2}} m | {{ferraillage.nomenclature.lignes.2.longueur_totale_m::n1}} m | **{{ferraillage.nomenclature.lignes.2.masse_kg::n1}} kg** |
| **{{ferraillage.nomenclature.lignes.3.repere}}** | {{ferraillage.nomenclature.lignes.3.role}} | {{ferraillage.nomenclature.lignes.3.nombre}} | HA{{ferraillage.nomenclature.lignes.3.dia_mm}} | {{ferraillage.nomenclature.lignes.3.longueur_unitaire_m::n2}} m | {{ferraillage.nomenclature.lignes.3.recouvrements_par_barre}} | {{ferraillage.nomenclature.lignes.3.longueur_faconnee_m::n2}} m | {{ferraillage.nomenclature.lignes.3.longueur_totale_m::n1}} m | **{{ferraillage.nomenclature.lignes.3.masse_kg::n1}} kg** |
| **{{ferraillage.nomenclature.lignes.4.repere}}** | {{ferraillage.nomenclature.lignes.4.role}} | {{ferraillage.nomenclature.lignes.4.nombre}} | HA{{ferraillage.nomenclature.lignes.4.dia_mm}} | {{ferraillage.nomenclature.lignes.4.longueur_unitaire_m::n2}} m | {{ferraillage.nomenclature.lignes.4.recouvrements_par_barre}} | {{ferraillage.nomenclature.lignes.4.longueur_faconnee_m::n2}} m | {{ferraillage.nomenclature.lignes.4.longueur_totale_m::n1}} m | **{{ferraillage.nomenclature.lignes.4.masse_kg::n1}} kg** |
| **{{ferraillage.nomenclature.lignes.5.repere}}** | {{ferraillage.nomenclature.lignes.5.role}} | {{ferraillage.nomenclature.lignes.5.nombre}} | HA{{ferraillage.nomenclature.lignes.5.dia_mm}} | {{ferraillage.nomenclature.lignes.5.longueur_unitaire_m::n3}} m | — | {{ferraillage.nomenclature.lignes.5.longueur_faconnee_m::n3}} m | {{ferraillage.nomenclature.lignes.5.longueur_totale_m::n1}} m | **{{ferraillage.nomenclature.lignes.5.masse_kg::n1}} kg** |
| | | | | | | | **Total** | **{{ferraillage.nomenclature.masse_kg::n1}} kg** |

Les quantités sont celles des **deux** poutres de la zone, comme sur une nomenclature de chantier.

{{ferraillage.nomenclature._pourquoi_le_recapitulatif}}

:::figure {"fn":"barres","args":"ferraillage.figures.par_diametre","titre":"Où est la masse d'acier des poutres, par diamètre","num":3,"options":{"unite":"kg d'acier pour les deux poutres de la zone"},"voir":["Un diamètre porte {{ferraillage.nomenclature.recapitulatif_par_diametre.0.part_pct::n0}} % de la masse à lui seul. C'est la ligne qu'on vérifie deux fois avant de passer commande, parce qu'une erreur de saisie y coûte le plus.","Les cadres, qu'on néglige volontiers parce qu'ils sont petits, pèsent {{ferraillage.nomenclature.lignes.5.masse_kg::n0}} kg — plus que n'importe quel repère de chapeau. Le petit diamètre revient {{ferraillage.cadres.nombre_total}} fois.","Le récapitulatif par diamètre est la pièce qui passe commande : le ferrailleur n'achète pas des repères, il achète des tonnes de HA20 et de HA25."],"erreur":"Commander sur le total en kilogrammes. On reçoit le bon tonnage dans les mauvais diamètres, et c'est irrattrapable à J+1 du coulage."}
:::

### b. Les cadres : compter des intervalles, plus un

{{ferraillage.cadres._piege_du_comptage}}

| Zone | Segments | Longueur | Espacement | Cadres par segment | Total |
|---|---|---:|---:|---|---:|
| {{ferraillage.cadres.zones.0.nom}} | {{ferraillage.cadres.zones.0.segments_m.length}} | {{ferraillage.cadres.zones.0.longueur_m::n2}} m | {{ferraillage.cadres.zones.0.espacement_cm}} cm | {{ferraillage.cadres.zones.0.cadres_par_segment}} | {{ferraillage.cadres.zones.0.nombre}} |
| {{ferraillage.cadres.zones.1.nom}} | {{ferraillage.cadres.zones.1.segments_m.length}} | {{ferraillage.cadres.zones.1.longueur_m::n2}} m | {{ferraillage.cadres.zones.1.espacement_cm}} cm | {{ferraillage.cadres.zones.1.cadres_par_segment}} | {{ferraillage.cadres.zones.1.nombre}} |
| | **{{ferraillage.cadres.nb_de_segments}} segments** | {{ferraillage.nomenclature.longueur_de_poutre_m::n2}} m | | **par poutre** | **{{ferraillage.cadres.nombre_par_poutre}}** |

$$ n = \sum_{\text{segments}} \left( \left\lfloor \frac{\ell_i}{s} \right\rfloor + 1 \right) $$

Le « + 1 » se compte **par segment continu**, pas par zone d'espacement : chaque segment a ses deux
extrémités. Les zones de ce plan ne sont pas des tronçons uniques — la zone resserrée couvre
{{ferraillage.cadres.zones.0.segments_m.length}} segments disjoints (l'about de rive, les deux
appuis intermédiaires, l'about opposé) et la zone courante
{{ferraillage.cadres.zones.1.segments_m.length}}. Totaliser les longueurs d'une zone avant
d'ajouter un seul cadre fait la même erreur que compter $\ell/s$, en plus discret.

{{ferraillage.cadres.lecture}}

:::encart {"genre":"attente","titre":"Le métré des cadres est MINORANT, et voici de combien"}
{{ferraillage.cadres._crochets}}

Les cadres de cette zone pèsent {{ferraillage.commande.crochets_non_metres.masse_des_cadres_kg::n1}} kg.
Si l'on retient **{{ferraillage.commande.crochets_non_metres.part_estimee_pct::n0}} %** pour les
crochets — un **ordre de grandeur déclaré, et non une mesure** —, cela fait
{{ferraillage.commande.crochets_non_metres.masse_non_metree_kg::n1}} kg, soit
{{ferraillage.commande.crochets_non_metres.part_du_metre_total_pct::n2}} % du métré total.

Ce n'est pas corrigé, et c'est volontaire : **on ne corrige pas un métré d'une valeur qu'on ne peut
pas citer.** On publie le minorant et on nomme ce qui manque. Et on ne dit pas « mesuré » : le cours
n'a pas mesuré cet écart et ne le peut pas, puisque la longueur d'un crochet est précisément ce qui
est ⏸. Le jour où le BAEL est fourni, elle entre dans la formule et le métré monte.
:::

### c. Le contrôle d'ordre de grandeur — et pourquoi ce n'est PAS une seconde voie

Le § 3.3 impose deux voies indépendantes. **Ce module ne les a pas pour sa masse totale, et il le
dit.** Le plan fictif de ce cours a été *calibré* sur les ratios kg/m³ du projet ; comparer ensuite
son métré à ces mêmes ratios vérifie le **calibrage**, pas le métré. Un résultat « dans la
fourchette » serait ici une tautologie, et la présenter comme une vérification serait exactement le
défaut que le module C3 a dû corriger : un test qui épingle une conclusion au lieu de contrôler une
règle.

| Ouvrage | Métré du plan | Béton | Base du ratio | Ratio du plan | Référence | Fourchette | Écart |
|---|---:|---:|---|---:|---:|---:|---:|
| {{ferraillage.ordre_de_grandeur.elements.0.element}} | {{ferraillage.ordre_de_grandeur.elements.0.masse_du_plan_kg::n0}} kg | {{ferraillage.ordre_de_grandeur.elements.0.beton_m3::n1}} m³ | retombée sous dalle | **{{ferraillage.ordre_de_grandeur.elements.0.ratio_du_plan_kg_m3::n0}}** | ⟦V3|ratio d'acier d'une poutre de plancher, rapporté à la retombée sous dalle|180|kg/m³|140 à 220|2026|ordre de grandeur de prédimensionnement, aucun document normatif fourni ; la base — retombée et non section pleine — change entièrement le verdict⟧ | {{ferraillage.ordre_de_grandeur.elements.0.fourchette_kg_m3.0}} à {{ferraillage.ordre_de_grandeur.elements.0.fourchette_kg_m3.1}} | {{ferraillage.ordre_de_grandeur.elements.0.ecart_pct::n1}} % |
| {{ferraillage.ordre_de_grandeur.elements.1.element}} | {{ferraillage.ordre_de_grandeur.elements.1.masse_du_plan_kg::n0}} kg | {{ferraillage.ordre_de_grandeur.elements.1.beton_m3::n1}} m³ | dalle seule | **{{ferraillage.ordre_de_grandeur.elements.1.ratio_du_plan_kg_m3::n0}}** | ⟦V3|ratio d'acier d'une dalle de plancher, rapporté au volume de dalle seul|80|kg/m³|65 à 100|2026|ordre de grandeur de prédimensionnement, aucun document normatif fourni⟧ | {{ferraillage.ordre_de_grandeur.elements.1.fourchette_kg_m3.0}} à {{ferraillage.ordre_de_grandeur.elements.1.fourchette_kg_m3.1}} | {{ferraillage.ordre_de_grandeur.elements.1.ecart_pct::n1}} % |

**La colonne « base du ratio » n'est pas un détail de présentation.** 180 kg/m³ s'applique ici à la
**retombée sous dalle** ({{ferraillage.ordre_de_grandeur.elements.0.beton_m3::n1}} m³), la table
étant comptée avec la dalle. Rapporté à la section pleine de la poutre, le même plan donnerait un
ratio bien plus bas et le verdict basculerait. Un ratio d'acier sans sa base ne rend aucun verdict.

{{ferraillage.ordre_de_grandeur._pourquoi_element_par_element}}

:::figure {"fn":"barres","args":"ferraillage.figures.ordre_de_grandeur","titre":"Métré du plan et masse au ratio — un contrôle de cohérence, pas une vérification","num":4,"options":{"unite":"kg d'acier sur la zone","bande":{"$":"ferraillage.figures.ordre_de_grandeur_bande"},"libelle_bande":"fourchette du ratio"},"voir":["La bande grise est LARGE : c'est la marque d'une hypothèse V3. Elle dit ce que la comparaison peut prouver — peu de choses, et c'est normal.","Les deux barres ne sont pas indépendantes : le plan de ce cours a été calibré sur ce ratio. La comparaison vérifie le calibrage, pas le métré, et le module préfère le dire plutôt que de se décerner une vérification qu'il n'a pas faite.","Ce qui garantit le métré est ailleurs : l'étalonnage externe de la masse linéique (dix diamètres contre le tableau du commerce, écart maximal 0,5 g/m) et la seconde traversée depuis le dessin, ci-dessous."],"erreur":"Appeler « seconde voie » une comparaison dont les deux termes viennent de la même source. Sur un chantier réel — plan du BET, ratio d'ailleurs — la comparaison redevient un vrai contrôle ; dans un cours qui a calibré son propre plan, non."}
:::

**La seconde traversée, elle, est réelle.** La masse de la poutre se recalcule depuis le **dessin** —
positions de l'élévation, section, segments de cadres — sans passer par la nomenclature :
{{ferraillage.metre_depuis_le_dessin.masse_depuis_le_dessin_kg::n1}} kg contre
{{ferraillage.metre_depuis_le_dessin.masse_depuis_la_nomenclature_kg::n1}} kg, soit
{{ferraillage.metre_depuis_le_dessin.ecart_pct::n3}} % d'écart. Ce qu'elle vérifie :
{{ferraillage.metre_depuis_le_dessin.ce_que_cette_voie_verifie}}

### d. Ce que le métré change pour le budget, et quand

{{ferraillage.metre_contre_estimation.lecture}}

| | |
|---|---:|
| Estimation par ratio (module TV, avant tout plan) | {{ferraillage.metre_contre_estimation.estimation_par_ratio_kg::n0}} kg |
| Fourchette déclarée de cette estimation | {{ferraillage.metre_contre_estimation.fourchette_de_l_estimation_kg.0::n0}} à {{ferraillage.metre_contre_estimation.fourchette_de_l_estimation_kg.1::n0}} kg |
| **Métré du plan visé** | **{{ferraillage.metre_contre_estimation.metre_du_plan_kg::n0}} kg** |
| Écart | {{ferraillage.metre_contre_estimation.ecart_kg::n0}} kg ({{ferraillage.metre_contre_estimation.ecart_pct::n1}} %) |

{{ferraillage.metre_contre_estimation.ce_qui_change_en_aval}}

:::encart {"genre":"voir","titre":"Pourquoi ce cours ne rebascule pas son bordereau sur ce métré"}
{{ferraillage.metre_contre_estimation._pourquoi_ce_module_ne_le_fait_pas}}

La règle, elle, vaut sur un chantier réel : **à partir du visa, la quantité d'un attachement d'acier
se prend sur la nomenclature, pas sur le ratio qui a servi à chiffrer le marché.** Tant que ce
basculement n'est pas fait, on compare un avancement mesuré sur des plans à un budget bâti sur une
hypothèse — exactement la faute d'assiette que le module D4 corrige sur sa valeur acquise.
:::

### e. Du plan à la commande, et à ce qui se paie

Trois masses d'acier pour le même ouvrage, et elles ne sont jamais égales.

:::figure {"fn":"cascade","args":"ferraillage.commande.cascade","titre":"De l'acier du plan à l'acier à commander","num":5,"options":{"unite":"kg"},"voir":["L'écart vaut {{ferraillage.commande.ecart_commande_plan_pct::n1}} % — {{ferraillage.commande.chutes_kg::n0}} kg de chutes de façonnage et {{ferraillage.commande.ligatures_kg::n0}} kg de fil. Commander le poids du plan, c'est manquer d'acier à J-1.","Les ligatures se calculent sur le plan PLUS les chutes, pas sur le plan seul : on ligature l'acier qu'on a façonné, chutes comprises dans le flux d'atelier.","Ce qui se PAIE n'est sur aucune de ces barres : c'est le CPS qui le dit, et l'usage le plus répandu est le poids théorique du plan. Les chutes sont alors dans le PRIX unitaire, pas dans la quantité."],"erreur":"Attacher une quantité d'acier sur un bon de livraison. Le bon de livraison porte l'acier commandé, chutes et ligatures comprises : on réclame une quantité qui n'est pas due, et on perd la réclamation au décompte."}
:::

{{ferraillage.commande.ce_qui_se_paie}}

Et la ligne qu'on oublie : **{{ferraillage.commande.cales_d_enrobage_u}} cales d'enrobage** pour la
zone, à ⟦V3|cales d'enrobage en partie courante de dalle|4|cales/m²|2 à 6|2026|hypothèse de commande, dépend du type de cale et du diamètre de la nappe⟧ par m².
{{ferraillage.commande.cales_note}}

### f. Contrôler un ferraillage posé

Chaque ligne porte sa **référence de contrôle**, et c'est tout l'enjeu : aucune de ces valeurs ne se
juge de mémoire. Là où le critère est réglementaire, la colonne le dit **⏸** au lieu d'avancer un
chiffre.

| Contrôle | Ce qu'on regarde | Contre quoi | Statut de la règle | Symptôme si on l'a raté |
|---|---|---|---|---|
| **{{ferraillage.controles.liste.0.controle}}** | {{ferraillage.controles.liste.0.comment}} | {{ferraillage.controles.liste.0.reference}} | {{ferraillage.controles.liste.0.statut_de_la_regle}} | {{ferraillage.controles.liste.0.symptome_si_rate}} |
| **{{ferraillage.controles.liste.1.controle}}** | {{ferraillage.controles.liste.1.comment}} | {{ferraillage.controles.liste.1.reference}} | {{ferraillage.controles.liste.1.statut_de_la_regle}} | {{ferraillage.controles.liste.1.symptome_si_rate}} |
| **{{ferraillage.controles.liste.2.controle}}** | {{ferraillage.controles.liste.2.comment}} | {{ferraillage.controles.liste.2.reference}} | {{ferraillage.controles.liste.2.statut_de_la_regle}} | {{ferraillage.controles.liste.2.symptome_si_rate}} |
| **{{ferraillage.controles.liste.3.controle}}** | {{ferraillage.controles.liste.3.comment}} | {{ferraillage.controles.liste.3.reference}} | {{ferraillage.controles.liste.3.statut_de_la_regle}} | {{ferraillage.controles.liste.3.symptome_si_rate}} |
| **{{ferraillage.controles.liste.4.controle}}** | {{ferraillage.controles.liste.4.comment}} | {{ferraillage.controles.liste.4.reference}} | {{ferraillage.controles.liste.4.statut_de_la_regle}} | {{ferraillage.controles.liste.4.symptome_si_rate}} |
| **{{ferraillage.controles.liste.5.controle}}** | {{ferraillage.controles.liste.5.comment}} | {{ferraillage.controles.liste.5.reference}} | {{ferraillage.controles.liste.5.statut_de_la_regle}} | {{ferraillage.controles.liste.5.symptome_si_rate}} |
| **{{ferraillage.controles.liste.6.controle}}** | {{ferraillage.controles.liste.6.comment}} | {{ferraillage.controles.liste.6.reference}} | {{ferraillage.controles.liste.6.statut_de_la_regle}} | {{ferraillage.controles.liste.6.symptome_si_rate}} |

{{ferraillage.controles.la_regle}}

**Côté entreprise.** {{ferraillage.controles.double_lecture.entreprise}}

**Côté maîtrise d'œuvre.** {{ferraillage.controles.double_lecture.maitrise_d_oeuvre}}

## S4g · Sécurité : ce qu'un ferraillage décide

Le § 3.4 impose de dire ce que cette phase d'exécution décide en matière de risque. Les dispositions
ci-dessous sont **essentielles et non exhaustives** ; elles ne remplacent ni le plan de sécurité du
chantier ni les obligations réglementaires du marché.

| Opération | Ce que le ferraillage décide | Disposition essentielle |
|---|---|---|
| **Levage des cages préfabriquées** | la masse d'une cage, donc l'élingage et la portée de grue | une cage de poutre n'est rigide que dans un sens : elle se lève avec un palonnier ou à deux points, et elle se stabilise **avant** qu'un homme n'approche |
| **Circulation sur la nappe** | la densité des barres, donc où l'on peut poser le pied | des passerelles de circulation sur la nappe supérieure, posées avant le ferraillage de la dalle, pas improvisées pendant le coulage |
| **Aciers en attente verticaux** | nombre et position des attentes de poteaux et de voiles | embouts de protection sur **toutes** les attentes, dès la pose. C'est le risque le plus banal et le plus grave d'un chantier de gros œuvre, et il ne coûte rien à supprimer |
| **Stockage et façonnage** | les longueurs façonnées, donc l'encombrement de l'aire | aire de stockage plane et calée — un fagot de HA25 de 12 m qui roule ne se retient pas à la main — et séparation entre l'aire de façonnage et les circulations |
| **Visa avant coulage** | le moment du point d'arrêt | le constat se fait **sur** l'ouvrage : accès sûr, protections périphériques en place, et jamais pendant le coulage |

**Le lien avec le reste du module.** Le § S4f demande de compter les barres avant de couler. Compter
suppose de marcher sur la nappe : si personne n'a prévu de passerelle, le contrôle se fera depuis le
bord, c'est-à-dire mal. **Un contrôle qu'on ne peut pas faire en sécurité est un contrôle qui ne se
fera pas**, et ce n'est pas au moment du visa qu'on s'en aperçoit — c'est au moment de l'installation
du coffrage.

## S5 · Erreurs fréquentes, et ce qu'elles coûtent

| Erreur | Comment elle se voit | Ce qu'elle coûte |
|---|---|---|
| Métrer la cote du dessin au lieu de la longueur **développée** | les barres façonnées sont trop courtes | un retour en atelier, et le coulage décalé d'un jour |
| Oublier les recouvrements de filante | le métré est juste jusqu'au jour de la pose | {{ferraillage.nomenclature.lignes.0.recouvrements_par_barre}} recouvrement par filante ici, soit {{gare.armatures.du_plan_a_la_commande.longueur_de_recouvrement_du_plan_m.valeur::n2}} m par barre non commandés |
| Compter $L/s$ cadres au lieu de $L/s + 1$ | rien au métré | le cadre manquant est celui de l'about, là où il sert le plus |
| Commander le poids du plan | il manque de l'acier à J-1 | {{ferraillage.commande.ecart_commande_plan_pct::n1}} % de l'acier de la zone |
| Attacher sur un bon de livraison | la quantité est supérieure à celle du plan | une réclamation perdue au décompte : le CPS paie le poids théorique |
| Comparer les deux ouvrages à un ratio **global** | le verdict est rassurant | ici {{ferraillage.ordre_de_grandeur.ecart_pct::n1}} % globalement, qui masquent {{ferraillage.ordre_de_grandeur.elements.0.ecart_pct::n1}} % sur la poutre et {{ferraillage.ordre_de_grandeur.elements.1.ecart_pct::n1}} % sur la dalle |
| Publier un ratio d'acier **sans sa base** | le nombre a l'air d'un fait | 180 kg/m³ sur la retombée ou sur la section pleine, ce n'est pas le même ouvrage et le verdict bascule |
| Appeler « seconde voie » une comparaison **circulaire** | on se décerne une vérification | le plan de ce cours est calibré sur le ratio : la comparaison vérifie le calibrage, pas le métré |
| Corriger le métré pour entrer dans le ratio | plus aucun écart nulle part | on a remplacé une mesure sûre par une hypothèse V3 |
| Garder le ratio au bordereau après le visa des plans | les indices de D4 dérivent sans raison | un avancement mesuré sur des plans comparé à un budget bâti sur une hypothèse |
| Viser un ferraillage sur photo | le visa est tracé, le constat ne l'est pas | une non-conformité invisible, et un visa qu'on ne pourra pas défendre |
| Reprendre le calcul du BET au lieu de compter les barres | on y passe l'après-midi | le seul contrôle que personne d'autre ne peut faire n'est pas fait, et le béton est coulé |

## S6 · Exercices

:::exercice {"titre":"1 · Métrer un repère, de bout en bout","niveau":"application"}
Le repère **{{ferraillage.nomenclature.lignes.0.repere}}** du plan : {{ferraillage.nomenclature.lignes.0.nombre}} barres HA{{ferraillage.nomenclature.lignes.0.dia_mm}}
filantes sur {{ferraillage.nomenclature.longueur_de_poutre_m::n2}} m, barres du commerce de
{{gare.armatures.conventions.longueur_commerciale_m::n0}} m, recouvrement porté au plan
{{gare.armatures.du_plan_a_la_commande.longueur_de_recouvrement_du_plan_m.valeur::n2}} m. Quelle masse
d'acier ?

**Corrigé.** Trois étapes, et la deuxième est celle qu'on saute.

1. **Masse linéique.** $\frac{\pi}{4} d^2 \rho$ avec $d = 25$ mm et $\rho = 7\,850$ kg/m³ donne
   **{{ferraillage.nomenclature.lignes.0.masse_lineique_kg_m::n3}} kg/m**. On peut la lire dans un
   tableau, mais il faut savoir qu'elle se recalcule : c'est une grandeur physique, pas une valeur à
   retenir.
2. **Longueur façonnée.** $\lceil L / L_c \rceil - 1$ avec
   {{ferraillage.nomenclature.longueur_de_poutre_m::n0}} m de poutre et des barres de
   {{gare.armatures.conventions.longueur_commerciale_m::n0}} m donne
   **{{ferraillage.nomenclature.lignes.0.recouvrements_par_barre}}** recouvrement, donc
   {{ferraillage.nomenclature.longueur_de_poutre_m::n2}} +
   {{gare.armatures.du_plan_a_la_commande.longueur_de_recouvrement_du_plan_m.valeur::n2}} =
   **{{ferraillage.nomenclature.lignes.0.longueur_faconnee_m::n2}} m** par barre.
3. **Masse** : {{ferraillage.nomenclature.lignes.0.nombre}} × {{ferraillage.nomenclature.lignes.0.longueur_faconnee_m::n2}} ×
   {{ferraillage.nomenclature.lignes.0.masse_lineique_kg_m::n3}} = **{{ferraillage.nomenclature.lignes.0.masse_kg::n1}} kg**
   pour les deux poutres.

*Le piège est l'étape 2, et il a deux étages. Oublier complètement les recouvrements donne
{{ferraillage.nomenclature.lignes.0.nombre}} × {{ferraillage.nomenclature.longueur_de_poutre_m::n2}} ×
{{ferraillage.nomenclature.lignes.0.masse_lineique_kg_m::n3}}, soit
{{ferraillage.nomenclature.lignes.0.ecart_sans_recouvrement_pct::n1}} % de moins. Les compter par
$\lceil L/L_c \rceil - 1$ — le réflexe — en trouve un au lieu de deux, et commande des barres qui
ne couvrent pas la poutre. Dans les deux cas, le chantier s'en aperçoit le jour de la pose, et une
barre trop courte ne se rattrape pas en poussant les autres.*
:::

:::exercice {"titre":"2 · Un plan arrive à 95 kg/m³ sur la dalle","niveau":"probleme"}
Le BET envoie l'indice B du plan de la dalle. Votre métré donne cette fois **95 kg/m³** au lieu des
{{ferraillage.ordre_de_grandeur.elements.1.ratio_du_plan_kg_m3::n0}} de l'indice A. La fourchette de
référence est {{ferraillage.ordre_de_grandeur.elements.1.fourchette_kg_m3.0}} à
{{ferraillage.ordre_de_grandeur.elements.1.fourchette_kg_m3.1}} kg/m³. Que faites-vous ?

**Corrigé. Rien qui ressemble à une alerte, et deux choses précises.**

D'abord ce qu'il ne faut **pas** conclure. 95 est dans la fourchette : le ratio ne dit donc rien
d'anormal. Mais même s'il en sortait, il ne dirait toujours rien sur la justesse du plan — un ratio
mesure à quoi ressemble une dalle en général, et une dalle de hall de gare n'est pas une dalle en
général. Un plan hors fourchette est une **question**, jamais un verdict.

Les deux choses à faire sont ailleurs :

1. **Chiffrer l'écart sur la commande**, parce qu'il est réel, lui. De
   {{ferraillage.ordre_de_grandeur.elements.1.ratio_du_plan_kg_m3::n0}} à 95 kg/m³ sur
   {{ferraillage.ordre_de_grandeur.elements.1.beton_m3::n0}} m³ de dalle, la zone prend environ
   **2 000 kg** de plus, soit +{{ferraillage.commande.chutes_pct::n0}} % de chutes par-dessus, et
   huit zones derrière. Si la commande est déjà passée sur l'indice A, elle est fausse — et c'est
   cela l'urgence, pas le ratio.
2. **Vérifier que l'indice A n'est pas déjà posé quelque part.** Un changement d'indice entre deux
   zones coulées est la cause classique du ferraillage à refaire, et elle est entièrement
   administrative : c'est la première étape de la lecture d'un plan, celle du cartouche.

*Ce que cet exercice enseigne : un écart de ratio déclenche un travail de métreur et d'acheteur,
jamais une discussion de calcul. La discussion de calcul, si elle a lieu d'être, est au BET.*
:::

:::exercice {"titre":"3 · Le visa de ferraillage, un quart d'heure avant la toupie","niveau":"cas_ouvert"}
Il est 7 h 30. Le coulage est annoncé pour 9 h. Vous montez pour le visa de ferraillage de la zone.
Vous constatez : les cales d'enrobage sont en place sur la dalle mais **pas sous les poutres** ; les
chapeaux B2 de la poutre de rive s'arrêtent, à vue, un bon mètre avant la cote du plan ; et le plan
affiché sur la zone porte l'indice A alors que le dernier indice reçu au bureau est le B. Que
faites-vous, dans quel ordre, et qu'écrivez-vous ?

**Corrigé.** L'ordre n'est pas l'ordre de gravité : c'est l'ordre de **ce qui conditionne le reste**.

1. **L'indice d'abord.** Tant qu'on ne sait pas quel plan fait foi, les deux autres constats n'ont
   pas de référence — « un mètre avant la cote » ne veut rien dire si c'est la cote d'un plan
   périmé. C'est l'étape 1 de la lecture, et c'est elle qui décide si la question suivante est
   « corriger » ou « tout reprendre ». Appel au bureau, comparaison des deux indices sur le repère
   B2 : si l'indice B a changé les chapeaux, le ferraillage est à reprendre et il n'y aura pas de
   coulage à 9 h.
2. **Les chapeaux ensuite**, parce que c'est le constat irréversible. On mesure, on ne juge pas à
   vue : un mètre d'écart se vérifie au décamètre en deux minutes. S'il est confirmé, c'est une
   non-conformité, et elle est bloquante — un chapeau trop court se voit en fissuration, et après
   coulage il n'y a plus de reprise possible sans démolition.
3. **Les cales enfin**, qui est le plus facile à corriger et le plus facile à oublier. Reprise
   immédiate, sans débat : sans cale sous la poutre, la cage descend au vibrage et l'enrobage
   disparaît là où il protège l'acier le plus sollicité.

**Ce qu'on écrit**, et c'est la vraie réponse à l'exercice. Un constat écrit, daté, signé, qui porte
quatre choses : **ce qui a été constaté** (les trois points, factuellement, avec les cotes
mesurées) ; **l'indice du plan contre lequel le constat a été fait** ; **la décision** (point
d'arrêt non levé) ; et **l'heure du reconstat**. Sans cette dernière ligne, le chantier n'a pas de
porte de sortie et la pression se reporte sur vous dans l'heure.

*Ce qu'on n'écrit pas : une appréciation sur la qualité du BET ou de l'équipe de ferraillage. Un
constat qui contient un jugement se discute ; un constat qui contient des cotes ne se discute pas.*

*Et le vrai sujet, celui qu'on ne voit qu'après coup : si vous montez à 7 h 30 pour un coulage à 9 h,
vous n'avez pas le temps de faire ce travail. Le visa de ferraillage est une tâche du planning —
{{gare.cycle_zone.point_arret_visa_ferraillage_j.valeur::n2}} jour dans le cycle du module C3 — et
elle se place la veille.*
:::

## S7 · Check-list, glossaire et quiz

**Check-list : recevoir un plan de ferraillage**

1. Le **cartouche** porte-t-il un indice, une date, et la mention qui autorise l'exécution ?
2. Cet indice est-il bien le **dernier** reçu, et est-il celui qui est affiché sur la zone ?
3. La **nomenclature** et le **dessin** disent-ils la même chose — nombre de barres par repère,
   longueurs ?
4. Les longueurs de la nomenclature sont-elles des longueurs **développées** ?
5. Les **filantes** plus longues qu'une barre du commerce portent-elles leurs recouvrements ?
6. Le métré tombe-t-il dans la **fourchette** du ratio, élément par élément ?
7. Les **réservations** et les **attentes** des autres lots y figurent-elles ?
8. Le métré du plan a-t-il **remplacé** l'estimation par ratio dans le bordereau et les attachements ?

**Glossaire**

| Terme | Ce que c'est |
|---|---|
| **Repère** | un identifiant de barre sur un plan : un repère = une forme, un diamètre, une longueur façonnée. Deux longueurs différentes, ce sont deux repères |
| **Longueur développée** | la longueur de la barre une fois dépliée : partie droite plus retours. C'est elle qu'on commande, pas la cote du dessin |
| **Filante** | barre qui court sur toute la longueur de l'ouvrage, par opposition à un renfort ou à un chapeau, localisés |
| **Chapeau** | barre supérieure placée à cheval sur un appui, là où la fibre tendue est en haut |
| **Nappe** | ensemble de barres parallèles d'une dalle, défini par un diamètre et un espacement — jamais par un nombre |
| **Cale d'enrobage** | pièce qui maintient l'armature à distance du coffrage. Sans elle, l'enrobage du plan est une intention |
| **Point d'arrêt** | étape qu'on ne dépasse pas sans un visa écrit. Ici : le ferraillage avant coulage |
| **Indice** | numéro de version d'un plan. L'information la plus banale et la plus souvent fatale |

**Quiz**

**1. Un plan de ferraillage vous paraît léger. Que faites-vous ?**
**On le signale par écrit au BET, et on ne recalcule pas.** Signaler n'est pas trancher : c'est
précisément parce qu'on ne peut pas trancher qu'on signale. Et surtout, on ne retarde pas pour cela
le seul contrôle que personne d'autre ne fera — compter ce qui est posé.

**2. La nomenclature dit 24,00 m pour une filante. Que commande-t-on ?**
**{{ferraillage.nomenclature.lignes.0.longueur_faconnee_m::n2}} m par barre** :
{{ferraillage.nomenclature.lignes.0.nb_de_barres_par_filante}} barres du commerce de
{{gare.armatures.conventions.longueur_commerciale_m::n0}} m et donc
{{ferraillage.nomenclature.lignes.0.recouvrements_par_barre}} recouvrements. Deux barres ne
suffiraient pas : elles ne couvriraient que 23,00 m. Le nombre de recouvrements est géométrique ;
leur longueur, elle, est réglementaire et reste ⏸.

**3. Combien de cadres sur un tronçon continu de 15,00 m à 20 cm ?**
**76**, soit $\lfloor 15{,}00/0{,}20 \rfloor + 1$. Compter 75 oublie le cadre d'extrémité, celui qui
tient la cage contre l'about. Et si ces 15,00 m ne sont pas continus mais répartis sur trois
tronçons, la réponse n'est plus 76 mais **78** : le « + 1 » est par **segment**, pas par total.

**4. Votre métré donne {{ferraillage.ordre_de_grandeur.elements.1.ratio_du_plan_kg_m3::n0}} kg/m³ sur la dalle, le ratio de référence est 80. Le plan est-il faux ?**
**La question n'a pas de sens sous cette forme**, et trois choses manquent avant d'y répondre. La
**base** du ratio — 80 kg/m³ de quoi : la dalle seule, ou dalle et retombées ? Le **métré**, lui, est
sûr : il ne repose que sur des longueurs et une masse volumique. Et le ratio est une hypothèse V3 de
fourchette {{ferraillage.ordre_de_grandeur.elements.1.fourchette_kg_m3.0}} à
{{ferraillage.ordre_de_grandeur.elements.1.fourchette_kg_m3.1}}. L'écart interroge le plan ; il ne
condamne jamais le métré. *Et dans ce cours en particulier, il ne prouve rien du tout : le plan a été
calibré sur ce ratio.*

**5. Le bon de livraison porte {{ferraillage.commande.acier_commande_kg::n0}} kg. Qu'attache-t-on ?**
**{{ferraillage.commande.acier_du_plan_kg::n0}} kg**, le poids de la nomenclature — sauf mention
contraire du CPS, qu'il faut avoir lue. Les {{ferraillage.commande.ecart_commande_plan_pct::n1}} %
d'écart sont les chutes et les ligatures : ils sont dans le prix unitaire de l'entreprise, pas dans
la quantité du maître d'ouvrage.

**6. Pourquoi le métré des cadres de ce module est-il minorant ?**
Parce que les **crochets d'extrémité** n'y sont pas : leur longueur est une disposition
constructive, et la phase § 5.0 interdit de l'avancer. On publie le minorant et on nomme ce qui
manque, plutôt que de corriger d'une valeur qu'on ne peut pas citer.

**7. À quel moment l'estimation par ratio cesse-t-elle de valoir ?**
**Au visa du plan.** À partir de là, la quantité d'un attachement se prend sur la nomenclature. Tant
que le basculement n'est pas fait, les indices de performance comparent un avancement mesuré sur des
plans à un budget bâti sur une hypothèse.

:::memo
## Fiche mémo — béton armé en exécution

**Le partage des rôles, en une ligne**

> Le BET et le contrôle technique répondent à « *ce ferraillage est-il suffisant ?* ».
> Vous répondez à « *ce qui est posé est-il ce que le plan visé montre ?* », et vous êtes le seul à
> pouvoir le faire.

**Les trois formules du métré**

$$ m_\ell = \frac{\pi}{4} d^2 \rho \qquad n_{\text{rec}} = \left\lceil \frac{L - L_r}{L_c - L_r} \right\rceil - 1 \qquad n_{\text{cadres}} = \sum_i \left( \left\lfloor \frac{\ell_i}{s} \right\rfloor + 1 \right) $$

Le premier « + 1 » est **par segment**. Le nombre de recouvrements se compte sur la **couverture**
($k L_c - (k-1) L_r \geq L$), jamais par une simple division.

**Masses linéiques à retenir** (recalculables, non réglementaires)

| HA8 | HA10 | HA12 | HA14 | HA16 | HA20 | HA25 |
|---:|---:|---:|---:|---:|---:|---:|
| 0,395 | 0,617 | 0,888 | 1,208 | 1,578 | 2,466 | 3,853 |

**Les chiffres de cette zone**

| | |
|---|---:|
| Acier des 2 poutres PM1 | {{ferraillage.nomenclature.masse_kg::n0}} kg · {{ferraillage.ordre_de_grandeur.elements.0.ratio_du_plan_kg_m3::n0}} kg/m³ |
| Acier de la dalle DM1 | {{ferraillage.nappes.masse_kg::n0}} kg · {{ferraillage.nappes.masse_par_m2_kg::n1}} kg/m² |
| **Acier du plan** | **{{ferraillage.ordre_de_grandeur.masse_du_plan_kg::n0}} kg** |
| Acier à commander | {{ferraillage.commande.acier_commande_kg::n0}} kg (+{{ferraillage.commande.ecart_commande_plan_pct::n1}} %) · fourchette {{ferraillage.commande.fourchette.acier_commande_kg.0::n0}} à {{ferraillage.commande.fourchette.acier_commande_kg.1::n0}} |
| Cadres | {{ferraillage.cadres.nombre_total}} · périmètre {{ferraillage.cadres.perimetre_m::n3}} m |
| Cales d'enrobage | {{ferraillage.commande.cales_d_enrobage_u}} · fourchette {{ferraillage.commande.fourchette.cales_u.0}} à {{ferraillage.commande.fourchette.cales_u.1}} |

**Les sept points d'un visa de ferraillage** — à viser côté maîtrise d'œuvre

Enrobage et cales · diamètres et nombre contre la nomenclature · arrêts de barres contre
l'élévation · recouvrements (longueur et non-alignement) · espacement des cadres · propreté et
stabilité de la cage · réservations et attentes.

**Les trois réflexes qui coûtent le plus cher**

1. Métrer la cote du dessin au lieu de la longueur développée.
2. Attacher sur un bon de livraison au lieu de la nomenclature.
3. Reprendre le calcul du BET pendant que le béton arrive.

**⏸ Ce qui reste fermé sans les normes** — longueurs d'ancrage et de recouvrement, arrêts de barres,
enrobages minimaux, espacements maximaux de cadres, longueurs de crochets. Tout cela est dans le
BAEL. Le module **B3c** l'ouvrira ; aucune de ces valeurs n'est avancée ici.
:::
