---
id: B7b + C4
titre: Lots techniques et second œuvre — vus par l'interface
fil: Palier 1 · module 13 — synthèse et exécution
resume: Vous n'êtes pas responsable des lots techniques. Vous en subissez deux choses, et toutes deux se calculent : la géométrie d'un trou dans une poutre, et la file d'attente des corps d'état dans un même volume. Un fourreau de 200 mm ne passe nulle part entre deux armatures, et le carnet de réservations gèle 439 jours avant qu'on s'en serve.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · aucune règle de percement, aucune section admissible, aucun degré coupe-feu n'est chiffré · chapitre plafonné à 10 % du cours avec son jumeau (§ 2.2)
pied: Exemple pédagogique — ne remplace ni une note de bureau d'études, ni un carnet de réservations visé, ni un plan de synthèse. Un percement dans un élément porteur se décide par le calcul, pas par la géométrie d'un catalogue.
donnees: synthese, gare, ferraillage, planification
---

## S1 · Ce que ce module fait, et ce qu'il refuse de faire

Ce module a une particularité : **son sujet n'est pas votre métier, et il ne doit pas le devenir.**
Vous n'êtes pas responsable du CVC, de l'électricité, des courants faibles ni de la plomberie. Le
prompt de ce cours plafonne d'ailleurs ce chapitre à 10 % de l'ensemble (§ 2.2), et c'est une
décision, pas une concession : un chef de projet suivi qui se met à piloter des lots techniques
arrête de piloter le chantier.

Vous en subissez pourtant deux choses, et elles sont entièrement de votre ressort :

1. **L'interface avec le gros œuvre.** Un trou dans une poutre est un sujet de structure, pas de
   plomberie. Et la question préalable est **géométrique** : un fourreau de
   {{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.0}} mm ne passe **nulle part**
   entre deux armatures de ce chantier, et cela se vérifie sur un plan sans attendre personne (§ S2).
2. **L'enchaînement des corps d'état.** Le second œuvre n'est pas une tâche, c'est une **file** : six
   corps d'état qui se passent le même volume. Sa durée a une forme fermée, elle bute sur un plancher
   que le découpage ne franchit pas, et ce plancher porte un nom — le corps d'état le plus lent
   (§ S3).

Et un résultat de calendrier qui surprend tout le monde la première fois : **le carnet de
réservations de la mezzanine gèle entre les jours
{{synthese.gel_des_reservations.fenetre_du_carnet_j.0::n0}} et
{{synthese.gel_des_reservations.fenetre_du_carnet_j.1::n0}}**, alors que le second œuvre qui s'en
servira commence au jour {{planification.segments_de_travail.SECO.0.0::n0}}.

Ce qu'il **refuse** de faire : dire si l'on a le droit de percer. Les règles de percement d'un
élément porteur, les sections admissibles, les distances aux armatures et aux appuis, le
rétablissement du degré coupe-feu d'une traversée sont **réglementaires** et restent **⏸**. Ce module
répond à une question plus modeste et toujours utile : **est-ce seulement géométriquement
possible ?** Quand la réponse est non, la discussion avec le bureau d'études n'a pas lieu d'être.

:::encart {"genre":"attente","titre":"Pourquoi ce module ne dira jamais « tes lots techniques »"}
Le cours s'adresse à un ingénieur qui conçoit, calcule, exécute et dirige — pas à un responsable de
lots techniques. Tout ce qui suit regarde les lots techniques **par le trou qu'ils demandent et par
la place qu'ils occupent dans la file**. C'est exactement ce qu'un chef de projet suivi en voit, et
c'est tout ce qu'il a besoin d'en voir pour tenir un planning.
:::

## S2 · B7b — l'interface : un trou, une date, un prix

### a. La géométrie d'abord : qu'est-ce qui passe entre deux armatures ?

Un fourreau se glisse entre deux armatures. L'espace dont il dispose ne dépend que de deux nombres
que le plan de ferraillage donne déjà : l'**espacement** des armatures et leur **diamètre**.

$$ \text{passage libre} = \text{espacement} - \varnothing_{\text{armature}} $$

Rien de plus. Et sur ce chantier, les armatures sont celles que le module B3e publie — elles ne sont
pas redéclarées ici :

| Endroit | Armatures | Espace libre | Plus gros fourreau qui passe |
|---|---|---:|---:|
| {{synthese.passage_libre.endroits.0.endroit}} | {{synthese.passage_libre.endroits.0.armatures}} | **{{synthese.passage_libre.endroits.0.passage_libre_mm::n0}} mm** | {{synthese.passage_libre.endroits.0.plus_gros_diametre_qui_passe_mm}} mm |
| {{synthese.passage_libre.endroits.1.endroit}} | {{synthese.passage_libre.endroits.1.armatures}} | **{{synthese.passage_libre.endroits.1.passage_libre_mm::n0}} mm** | {{synthese.passage_libre.endroits.1.plus_gros_diametre_qui_passe_mm}} mm |
| {{synthese.passage_libre.endroits.2.endroit}} | {{synthese.passage_libre.endroits.2.armatures}} | **{{synthese.passage_libre.endroits.2.passage_libre_mm::n0}} mm** | {{synthese.passage_libre.endroits.2.plus_gros_diametre_qui_passe_mm}} mm |
| {{synthese.passage_libre.endroits.3.endroit}} | {{synthese.passage_libre.endroits.3.armatures}} | **{{synthese.passage_libre.endroits.3.passage_libre_mm::n0}} mm** | {{synthese.passage_libre.endroits.3.plus_gros_diametre_qui_passe_mm}} mm |

{{synthese.passage_libre.lecture}}

:::figure {"fn":"barres","args":"synthese.figures.passages","titre":"L'espace libre entre deux armatures, endroit par endroit","num":1,"large":true,"options":{"unite":"mm d'espace libre entre deux armatures","legende_alerte":"n'accepte pas un fourreau de 160 mm"},"voir":["Le passage le plus étroit est sur appui, là où les cadres sont resserrés : {{synthese.passage_libre.endroits.0.passage_libre_mm::n0}} mm. C'est aussi, exactement, l'endroit où un percement est le moins envisageable.","Le plus large est en travée courante : {{synthese.passage_libre.endroits.1.passage_libre_mm::n0}} mm. Un fourreau de {{synthese.passage_libre.endroits.1.plus_gros_diametre_qui_passe_mm}} mm y tient — de justesse, et sans tenir compte des tolérances de pose.","Aucun endroit n'accepte {{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.0}} mm. Les diamètres {{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.0}}, {{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.1}} et {{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.2}} mm — désenfumage, eaux usées, gaines principales — demandent tous une trémie prévue, jamais une réservation glissée entre deux aciers.","Ces nombres sortent du plan de ferraillage du module B3e. Ils changent avec lui : un ferraillage plus dense ferme des passages, et personne ne prévient le lot technique."],"erreur":"Lire ce tableau comme une autorisation. Il dit ce qui TIENT, pas ce qui est PERMIS — la position admissible d'une réservation dans un élément porteur est réglementaire (⏸). Sa seule vertu est de trancher instantanément les cas impossibles, et ils sont plus nombreux qu'on ne croit."}
:::

{{synthese.passage_libre._ce_que_ce_nombre_ne_dit_pas}}

:::encart {"genre":"alerte","titre":"La seule frontière que ce module ait besoin de connaître"}
{{synthese.passage_libre._la_vraie_frontiere}}
:::

### b. La date de gel : un carnet n'est pas un document, c'est une échéance

Une réservation se pose dans le coffrage **avant** qu'on le ferme. Le carnet de chaque zone a donc
une date limite : la date de coulage, moins le temps de diffuser le plan, commander les fourreaux,
les recevoir et les poser —
⟦V3|délai entre l'arrêt du carnet de réservations d'une zone et le coulage de cette zone|12 j|j ouvrés|7 à 25|2026|diffusion du plan visé, commande des fourreaux, livraison, pose et contrôle avant fermeture du coffrage. Un délai de commande plus long ne se rattrape pas : il recule la date de gel⟧.

{{synthese.gel_des_reservations.lecture}}

Le plancher en compte ⟦V3|nombre de réservations par m² de plancher dans un hall d'ERP avec plénum technique|0,12 /m²|réservations/m²|0,06 à 0,25|2026|CVC, électricité, courants faibles, plomberie, désenfumage. Un bureau en compte moins, un local technique beaucoup plus⟧,
soit {{synthese.gel_des_reservations.reservations_sur_le_plancher::n0}} au total.

:::figure {"fn":"gantt","args":"synthese.figures.gel","titre":"De la date de gel au coulage : la fenêtre où une réservation existe encore sur le papier","num":2,"large":true,"options":{},"voir":["Chaque barre court de la date de gel du carnet au coulage de sa zone : {{synthese.gel_des_reservations.delai_de_gel_j::n0}} jours, toujours les mêmes.","Les barres se décalent à la cadence du coulage, {{synthese.gel_des_reservations.cadence_j::n1}} jours. Le carnet n'a donc pas UNE date limite mais huit, échelonnées.","Pendant une barre, la réservation est encore modifiable sur le plan mais plus dans le coffrage : c'est la fenêtre où une erreur se corrige à la gomme. Après, elle se corrige à la carotteuse.","Toutes ces barres sont derrière nous à la date d'arrêt du module D4 : le carnet de la mezzanine est intégralement figé."],"erreur":"Traiter le carnet comme un document de synthèse à mettre à jour « quand la synthèse sera stabilisée ». La synthèse n'est jamais stabilisée ; le coffrage, lui, se ferme à une date connue des mois à l'avance."}
:::

:::encart {"genre":"piege","titre":"Le carnet se joue pendant le gros œuvre, par des gens qui ne seront plus là"}
{{synthese.gel_des_reservations._quand_le_carnet_se_joue}}

{{synthese.gel_des_reservations._ce_que_le_gel_veut_dire}}
:::

### c. Le prix d'un trou oublié

Les cinq postes d'un percement de 160 mm dans un élément **non porteur** sont déclarés un à un :
⟦V3|carottage d'un percement de 160 mm dans une dalle de 25 cm|950 MAD|MAD|600 à 1 600|2026|amenée de la carotteuse, eau, carottage, évacuation de la carotte⟧,
⟦V3|détection d'armatures au ferroscan avant carottage|450 MAD|MAD|250 à 900|2026|sans elle, on coupe une armature sans le savoir — et on ne le sait jamais⟧,
⟦V3|note du bureau d'études et visa pour un percement non prévu|1 400 MAD|MAD|600 à 4 000|2026|vérifier qu'un trou non prévu ne remet pas en cause l'ouvrage. Sur un élément porteur, cette ligne devient la seule qui compte, et son issue n'est pas acquise⟧,
⟦V3|rebouchage, calfeutrement et reprise d'étanchéité autour d'une traversée|600 MAD|MAD|300 à 1 200|2026|le rétablissement du degré coupe-feu est réglementaire : ⏸⟧
et ⟦V3|remise en état des ouvrages déjà posés autour d'un percement après coup|350 MAD|MAD|150 à 900|2026|protection, nettoyage, reprises. C'est le poste qui explose quand le second œuvre est fini⟧.
Et une réservation prévue coûte
⟦V3|fourreau, calage, repérage et pose d'une réservation dans le coffrage avant coulage|120 MAD|MAD|60 à 250|2026|c'est le coût d'une minute de pose et d'un morceau de PVC⟧.

{{synthese.cout_du_trou_oublie.lecture}}

:::figure {"fn":"cascade","args":"synthese.figures.cout","titre":"Les postes d'un percement après coup, dans un élément NON porteur","num":3,"large":true,"options":{"unite":"MAD"},"voir":["Le carottage n'est que {{synthese.cout_du_trou_oublie.postes.0.part_pct::n0}} % du total : c'est la seule ligne à laquelle on pense, et c'est la plus petite de celles qui comptent.","Le poste le plus lourd est {{synthese.cout_du_trou_oublie.poste_le_plus_lourd}} — une étude et un visa, c'est-à-dire du temps d'ingénieur et une attente.","{{synthese.cout_du_trou_oublie.part_sans_outil_pct::n0}} % du coût ne tiennent ni à la machine ni à l'ouvrier : l'étude, le visa et la remise en état de ce qui était déjà posé autour.","Ce total suppose un élément NON porteur et un second œuvre non terminé. Les deux hypothèses sautent souvent ensemble, et alors ce n'est plus un coût, c'est une décision."],"erreur":"Négocier le prix du carottage. C'est le poste sur lequel il y a le moins à gagner et le seul que tout le monde regarde — pendant que l'étude, le visa et la remise en état, qui font {{synthese.cout_du_trou_oublie.part_sans_outil_pct::n0}} % de la facture, ne figurent sur aucun devis de carotteur."}
:::

{{synthese.cout_du_trou_oublie._ce_que_le_rapport_cache}}

:::encart {"genre":"alerte","titre":"Et sur un élément porteur, ce n'est plus un prix"}
{{synthese.cout_du_trou_oublie._sur_un_element_porteur}}
:::

## S3 · C4 — l'enchaînement : le second œuvre est une file

### a. La forme fermée d'une file de corps d'état

Six corps d'état doivent passer dans le même volume, chacun après le précédent. S'ils se suivent sur
la totalité du plancher, la durée est la **somme** : {{synthese.second_oeuvre.somme_des_durees_j::n0}}
jours. Si l'on découpe le plancher en zones, ils travaillent en parallèle dans des volumes
différents — et la durée s'écrit exactement :

$$ T(Z) = \frac{\sum W_i + (Z-1)\max W_i}{Z} + N\,(Z-1)\,f $$

où $W_i$ est la durée du corps $i$ sur la totalité du plancher, $Z$ le nombre de zones, $N$ le nombre
de corps d'état et $f$ le coût d'une frontière de zone.

| Corps d'état | Durée totale | Par zone | Reçoit son support de |
|---|---:|---:|---|
| {{synthese.second_oeuvre.corps.0.corps}} | {{synthese.second_oeuvre.corps.0.duree_totale_j::n0}} j | {{synthese.second_oeuvre.corps.0.duree_par_zone_j::n1}} j | {{synthese.second_oeuvre.corps.0.recoit_de}} |
| **{{synthese.second_oeuvre.corps.1.corps}}** | **{{synthese.second_oeuvre.corps.1.duree_totale_j::n0}} j** | {{synthese.second_oeuvre.corps.1.duree_par_zone_j::n1}} j | {{synthese.second_oeuvre.corps.1.recoit_de}} |
| {{synthese.second_oeuvre.corps.2.corps}} | {{synthese.second_oeuvre.corps.2.duree_totale_j::n0}} j | {{synthese.second_oeuvre.corps.2.duree_par_zone_j::n1}} j | {{synthese.second_oeuvre.corps.2.recoit_de}} |
| {{synthese.second_oeuvre.corps.3.corps}} | {{synthese.second_oeuvre.corps.3.duree_totale_j::n0}} j | {{synthese.second_oeuvre.corps.3.duree_par_zone_j::n1}} j | {{synthese.second_oeuvre.corps.3.recoit_de}} |
| {{synthese.second_oeuvre.corps.4.corps}} | {{synthese.second_oeuvre.corps.4.duree_totale_j::n0}} j | {{synthese.second_oeuvre.corps.4.duree_par_zone_j::n1}} j | {{synthese.second_oeuvre.corps.4.recoit_de}} |
| {{synthese.second_oeuvre.corps.5.corps}} | {{synthese.second_oeuvre.corps.5.duree_totale_j::n0}} j | {{synthese.second_oeuvre.corps.5.duree_par_zone_j::n1}} j | {{synthese.second_oeuvre.corps.5.recoit_de}} |

Les six durées sont déclarées une à une dans `data/`, et le coût d'une frontière de zone l'est
aussi : ⟦V3|jours perdus par corps d'état et par frontière de zone|0,4 j|j ouvrés|0,15 à 1,0|2026|réinstallation, reprise d'approvisionnement, re-calage des équipes. C'est ce qui empêche de découper à l'infini, et personne ne le chiffre jamais⟧.

{{synthese.second_oeuvre.lecture}}

:::figure {"fn":"diagramme","args":"synthese.figures.file","titre":"La durée de la file en fonction du nombre de zones","num":4,"large":true,"options":{"unite":"j","axeX":true,"axeY":true,"uniteX":"nombre de zones","nom":"durée du second œuvre","depuisZero":true,"marqueur":{"$":"synthese.figures.marqueur_zones"}},"voir":["À une seule zone, la file dure {{synthese.second_oeuvre.duree_en_serie_pure_j::n0}} jours : chaque corps attend que le précédent ait fini tout le plancher.","La courbe tombe vite, puis s'aplatit : le découpage rattrape le temps d'attente, et rien de plus.","Deux planchers, qu'il ne faut pas confondre. SANS coût de frontière, la file tendrait vers {{synthese.second_oeuvre.plancher_incompressible_j::n0}} jours — la durée du corps le plus lent — et jamais en dessous. AVEC lui, la courbe remonte avant d'y arriver : son minimum est à {{synthese.second_oeuvre.duree_optimale_j::n0}} jours.","Le marqueur est le découpage que le gros œuvre a déjà choisi ({{synthese.second_oeuvre.nb_zones_du_gros_oeuvre}} zones de coulage) : {{synthese.second_oeuvre.duree_a_Z_zones_j::n0}} jours. L'optimum est à {{synthese.second_oeuvre.zone_optimale}} zones — le second œuvre n'a donc pas de raison de redécouper le plancher autrement.","La courbe remonte à droite : chaque frontière de zone oblige chaque corps d'état à se réinstaller, et à partir d'un certain point ces réinstallations coûtent plus que le parallélisme ne rapporte."],"erreur":"Croire qu'un découpage plus fin accélère toujours. Il accélère tant que des corps d'état attendent, et il ralentit dès que les frontières coûtent plus que l'attente qu'elles suppriment. Les deux effets sont dans la même formule."}
:::

{{synthese.second_oeuvre._la_forme_fermee}}

### b. Deux voies, et elles s'accordent

Le module D2 donne au second œuvre une durée unique et déclarée :
**{{synthese.second_oeuvre.duree_declaree_par_D2_j::n0}} jours**, sur le chemin critique, sans marge.
La forme fermée ci-dessus, alimentée par six durées de corps d'état et un coût de frontière tous
déclarés séparément, en donne **{{synthese.second_oeuvre.duree_a_Z_zones_j::n0}}**.

**{{synthese.second_oeuvre.ecart_avec_D2_j::n1}} jour d'écart sur 75**, par deux chemins qui ne
partagent aucune donnée : l'un est un jugement d'expérience posé à l'Étape 0, l'autre une
décomposition par corps d'état avec sa formule. C'est le contre-calcul indépendant du § 3.3, et son
accord vaut plus que la précision de chacun.

:::encart {"genre":"voir","titre":"Ce qu'un accord à 4 % autorise — et ce qu'il n'autorise pas"}
Il autorise à **utiliser la décomposition pour piloter** : puisqu'elle reproduit la durée globale,
ses termes sont crédibles, et c'est eux qu'on suit semaine après semaine. Il n'autorise pas à dire
que les six durées sont justes : six nombres peuvent se compenser. Ce que l'accord prouve, c'est que
le **modèle** — une file pipelinée sur huit zones avec un coût de frontière — décrit bien ce que le
planificateur avait en tête sans le formuler.
:::

### c. Le goulot, et pourquoi accélérer ailleurs ne sert à rien

:::figure {"fn":"barres","args":"synthese.figures.corps","titre":"Les six corps d'état par durée, et celui qui commande","num":5,"large":true,"options":{"unite":"jours ouvrés sur la totalité du plancher","legende_alerte":"le goulot : il fixe le plancher de toute la file"},"voir":["Un seul corps dépasse les autres : {{synthese.second_oeuvre.goulot}}, {{synthese.second_oeuvre.duree_du_goulot_j::n0}} jours.","Et ce n'est pas UN corps d'état : ce sont quatre lots — CVC, électricité, courants faibles, plomberie — qui partagent le même plénum et qui se gênent les uns les autres.","Sa durée est le plancher de la file entière : {{synthese.second_oeuvre.plancher_incompressible_j::n0}} jours, quel que soit le découpage.","Diviser par deux la durée de TOUS les autres corps ne descendrait pas sous ce plancher. C'est vérifié par un canari des tests, pas affirmé."],"erreur":"Mettre la pression sur le corps d'état qu'on voit, qui est généralement le dernier — la peinture, parce que c'est lui qui est là quand la date approche. Les jours gagnés sur un corps qui n'est pas le goulot sont des jours gagnés sur une file qui attend ailleurs."}
:::

{{synthese.second_oeuvre._ce_que_le_goulot_impose}}

### d. La réception des supports : la seule décision irréversible de la journée

Chaque corps d'état reçoit un support du précédent. C'est à ce moment, et à ce moment seulement, que
la responsabilité change de main.

| Corps d'état | Reçoit de | Ce qu'il doit réceptionner |
|---|---|---|
| {{synthese.chaine_des_supports.lignes.0.corps}} | {{synthese.chaine_des_supports.lignes.0.recoit_de}} | {{synthese.chaine_des_supports.lignes.0.support}} |
| {{synthese.chaine_des_supports.lignes.1.corps}} | {{synthese.chaine_des_supports.lignes.1.recoit_de}} | {{synthese.chaine_des_supports.lignes.1.support}} |
| {{synthese.chaine_des_supports.lignes.2.corps}} | {{synthese.chaine_des_supports.lignes.2.recoit_de}} | {{synthese.chaine_des_supports.lignes.2.support}} |
| {{synthese.chaine_des_supports.lignes.3.corps}} | {{synthese.chaine_des_supports.lignes.3.recoit_de}} | {{synthese.chaine_des_supports.lignes.3.support}} |
| {{synthese.chaine_des_supports.lignes.4.corps}} | {{synthese.chaine_des_supports.lignes.4.recoit_de}} | {{synthese.chaine_des_supports.lignes.4.support}} |
| {{synthese.chaine_des_supports.lignes.5.corps}} | {{synthese.chaine_des_supports.lignes.5.recoit_de}} | {{synthese.chaine_des_supports.lignes.5.support}} |

{{synthese.chaine_des_supports._la_regle}}

{{synthese.chaine_des_supports._ce_qui_la_rend_difficile}}

:::encart {"genre":"voir","titre":"Ce que le suivi peut exiger sans attendre personne"}
{{synthese.chaine_des_supports._le_seul_critere_qui_tienne}}
:::

## S4 · Étude de cas : un conflit réservation / poutre, un lundi matin

Le lot CVC demande une réservation de
{{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.0}} mm dans la poutre PM1, à 2 m de
l'appui, pour un collecteur de désenfumage. Le carnet de la zone concernée gèle dans six jours.

**1. Vous ouvrez le plan de ferraillage avant d'ouvrir un débat.** À 2 m de l'appui, on est dans la
zone de cadres resserrés : espacement {{synthese.passage_libre.endroits.0.armatures}}, donc
{{synthese.passage_libre.endroits.0.passage_libre_mm::n0}} mm d'espace libre. Le fourreau demandé en
fait {{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.0}}. **C'est non, et ce n'est
pas une opinion.**

**2. Vous ne dites pas « non ».** Vous dites : *« cette réservation coupe au moins un cadre ; ce
n'est plus une réservation, c'est une modification de structure. Deux chemins : un tracé qui sort de
la poutre, ou une note du bureau d'études. Le second ne tient pas dans les six jours qui restent. »*
La différence entre les deux formulations est que la seconde donne une décision à prendre, pas un
conflit à arbitrer.

**3. Vous regardez où le tracé pourrait passer.** En travée courante, l'espace libre monte à
{{synthese.passage_libre.endroits.1.passage_libre_mm::n0}} mm — toujours insuffisant pour
{{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.0}} mm. **Aucun point de cette poutre
ne l'accepte.** Le collecteur passera donc sous la poutre, en plénum, ou par une trémie prévue dans
la dalle. C'est une décision de tracé, elle appartient au lot technique et à la synthèse, et vous
venez de leur faire gagner la semaine qu'ils auraient passée à la demander.

**4. Vous chiffrez l'autre branche, pour qu'elle soit décidée et non subie.** Si la demande arrive
après coulage et qu'elle est accordée sur un élément non porteur, le trou coûte
{{synthese.cout_du_trou_oublie.cout_du_percement_MAD::k}} MAD au lieu de
{{synthese.cout_du_trou_oublie.cout_d_une_reservation_prevue_MAD}} —
**×{{synthese.cout_du_trou_oublie.rapport::n1}}**. Sur les
{{synthese.gel_des_reservations.reservations_sur_le_plancher::n0}} réservations du plancher, deux
pour cent d'oublis coûteraient à eux seuls plus que l'ensemble du carnet.

**5. Vous notez la date, pas le sujet.** Le carnet de cette zone gèle dans six jours ; celui de la
zone suivante, {{synthese.gel_des_reservations.cadence_j::n1}} jours plus tard. Ce qui entre à
l'ordre du jour de la réunion de synthèse n'est pas « réservation CVC poutre PM1 » mais **« zone 5 :
gel dans 6 jours »**. C'est la même information et ce n'est pas le même document : l'une se discute,
l'autre se solde.

:::encart {"genre":"piege","titre":"Ce que cette matinée a coûté, et ce qu'elle a évité"}
Elle a coûté vingt minutes et un plan ouvert. Elle a évité une note de bureau d'études qui ne serait
pas arrivée à temps, un percement à {{synthese.cout_du_trou_oublie.cout_du_percement_MAD::k}} MAD, et
— le plus cher — la semaine pendant laquelle trois personnes auraient discuté d'une solution
géométriquement impossible.

**La compétence utile ici n'est pas de connaître le CVC. C'est de savoir lire un plan de ferraillage
et de faire une soustraction.**
:::

## S5 · Erreurs fréquentes

**1. Traiter une réservation comme un sujet de lot technique.** C'est un sujet de structure dès que
l'élément est porteur. **Symptôme** : une demande qui circule trois semaines entre le CVC et la
synthèse avant d'arriver au bureau d'études — qui la refuse en dix minutes.

**2. Attendre « la synthèse stabilisée » pour figer le carnet.** La synthèse n'est jamais
stabilisée ; le coffrage, lui, se ferme à une date connue d'avance. **Symptôme** : des zones coulées
sans leurs réservations, et un budget de carottage qui apparaît au cinquième mois.

**3. Négocier le prix du carottage.** C'est {{synthese.cout_du_trou_oublie.postes.0.part_pct::n0}} %
de la facture. **Symptôme** : trois devis de carotteur comparés au dirham près, pendant que l'étude
et la remise en état — {{synthese.cout_du_trou_oublie.part_sans_outil_pct::n0}} % du coût — ne
figurent sur aucun des trois.

**4. Prendre la durée du second œuvre pour une tâche.** C'est une file. **Symptôme** : un planning
qui montre « second œuvre, 75 jours » et qui ne dit rien quand un corps d'état glisse — alors que
seul le glissement du goulot compte.

**5. Mettre la pression sur le dernier corps d'état.** C'est celui qu'on voit quand la date approche,
et c'est rarement le goulot. **Symptôme** : un peintre à trois équipes sur un chantier où les
réseaux ne sont pas finis.

**6. Découper en zones de plus en plus fines pour accélérer.** Au-delà de l'optimum, les
réinstallations coûtent plus que le parallélisme ne rapporte. **Symptôme** : des corps d'état qui
passent leur temps à déplacer leur base et des cadences qui baissent à mesure qu'on « optimise ».

**7. Accepter un support sans critère écrit.** **Symptôme** : une reprise à la réception, et deux
entreprises qui ont chacune raison parce que personne n'avait écrit le seuil.

## S6 · Exercices

:::exercice {"titre":"1 · Un fourreau de 200 mm dans une poutre : possible ?","niveau":"application"}
Le lot plomberie demande un passage de {{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.0}} mm
dans la poutre PM1, en travée courante. Le plan de ferraillage indique des cadres
{{synthese.passage_libre.endroits.1.armatures}}. Que répondez-vous, et en combien de temps ?

**Corrigé — en une soustraction.** L'espace libre vaut
{{synthese.passage_libre.endroits.1.espacement_mm::n0}} −
{{synthese.passage_libre.endroits.1.dia_armature_mm}} =
**{{synthese.passage_libre.endroits.1.passage_libre_mm::n0}} mm**. Le fourreau en demande
{{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.0}} : il ne passe pas, et il ne
passera nulle part sur cette poutre puisque c'est l'endroit le plus large.

**Ce que vous répondez** n'est pas « non » mais : *cette réservation coupe un cadre, donc elle n'est
plus une réservation. Soit le tracé sort de la poutre, soit il faut une note du bureau d'études —
et son délai n'est pas celui du carnet.*

**Le piège à voir** : la géométrie dit que c'est impossible, elle ne dit jamais que c'est permis. Un
fourreau de {{synthese.passage_libre.endroits.1.plus_gros_diametre_qui_passe_mm}} mm **tiendrait**
entre deux cadres ; savoir si on a le droit de le mettre là est une autre question, et elle est
réglementaire (⏸).
:::

:::exercice {"titre":"2 · Le second œuvre glisse de dix jours : lequel ?","niveau":"probleme"}
Trois corps d'état annoncent chacun dix jours de retard : les cloisons, les réseaux en plénum, la
peinture. Vous ne pouvez en aider qu'un. Lequel, et pourquoi ?

**Corrigé — les réseaux, et de très loin.**

Les réseaux sont le **goulot** : {{synthese.second_oeuvre.duree_du_goulot_j::n0}} jours contre
{{synthese.second_oeuvre.corps.0.duree_totale_j::n0}} pour les cloisons et
{{synthese.second_oeuvre.corps.5.duree_totale_j::n0}} pour la peinture. Dans la forme fermée
$T(Z) = (\sum W + (Z-1)\max W)/Z + N(Z-1)f$, seule la durée du corps le plus lent est multipliée par
$(Z-1)$ : avec {{synthese.second_oeuvre.nb_zones_du_gros_oeuvre}} zones, **dix jours de plus sur le
goulot en coûtent près de dix à la file entière ; dix jours sur un autre corps n'en coûtent qu'un
peu plus d'un.**

Autrement dit : aider les cloisons ou la peinture revient à payer pour qu'une file attende plus
confortablement.

**Et le second réflexe**, qui est le vrai sujet : les réseaux en plénum ne sont pas un corps d'état,
ce sont **quatre lots dans le même volume**. Les « aider » ne veut rien dire tant qu'on n'a pas
demandé lequel des quatre bloque les trois autres — et la réponse est presque toujours celui qui
pose le plus gros et en premier.

**Le contre-test** : diviser par deux la durée de tous les corps *sauf* le goulot ne descend pas
sous {{synthese.second_oeuvre.plancher_incompressible_j::n0}} jours. C'est vérifié par un canari des
tests du module, pas affirmé.
:::

:::exercice {"titre":"3 · Revue critique : un carnet de réservations à viser","niveau":"revue"}
On vous soumet le carnet de réservations du plancher de mezzanine. Il porte : la liste des
{{synthese.gel_des_reservations.reservations_sur_le_plancher::n0}} percements avec leur diamètre et
leur coordonnée ; la mention « plan de synthèse en cours, indice B » ; une note « les réservations
dans les poutres seront confirmées après validation du BET ». Que relevez-vous ?

**Corrigé — trois observations, dont deux bloquantes.**

**a. Bloquante — « seront confirmées » n'est pas compatible avec une date de gel.** Le carnet de la
première zone gèle au jour {{synthese.gel_des_reservations.fenetre_du_carnet_j.0::n0}} et le dernier
au jour {{synthese.gel_des_reservations.fenetre_du_carnet_j.1::n0}}. Une confirmation ultérieure ne
peut pas exister : après le coulage, ce n'est plus une confirmation, c'est un percement. **Demande** :
la liste des réservations en poutre, triées par zone, avec la date de gel de chaque zone en regard.

**b. Bloquante — aucun diamètre n'est confronté au ferraillage.** La vérification est une
soustraction, elle prend dix minutes pour tout le carnet, et elle écarte d'emblée tous les diamètres
≥ {{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.0}} mm en poutre. **Demande** :
la colonne « espace libre à cet endroit » en face de chaque réservation en élément porteur.

**c. Majeure — l'indice du plan de synthèse n'engage personne.** « En cours, indice B » ne dit ni qui
a visé, ni ce qui change entre B et C. **Demande** : un indice visé par zone, figé à la date de gel —
le carnet n'a pas besoin que toute la synthèse soit stable, seulement que la zone qui coule le soit.

**Ce que la double lecture change.** Côté entreprise, ce carnet est un document de travail normal à
ce stade. Côté maîtrise d'œuvre, c'est un document **non visable** : il ne permet pas de vérifier
qu'on peut couler. La différence n'est pas la qualité du travail, c'est la question à laquelle le
document doit répondre.
:::

## S7 · Check-list, glossaire et quiz

**Check-list : avant de viser un carnet de réservations**

1. Chaque réservation en élément porteur porte-t-elle son **espace libre** à cet endroit ?
2. Les diamètres impossibles sont-ils écartés **avant** toute discussion avec les lots ?
3. Le carnet est-il trié **par zone de coulage**, et chaque zone porte-t-elle sa **date de gel** ?
4. Le délai de gel tient-il compte de la **commande et de la livraison** des fourreaux, pas seulement
   du plan ?
5. Qui vise, et à quelle date ? Un indice « en cours » ne gèle rien.
6. Les réservations qui coupent une armature sont-elles sorties du carnet et transformées en
   **demande de modification** ?
7. Pour le second œuvre : la durée est-elle **décomposée par corps d'état**, ou déclarée en bloc ?
8. Le **goulot** est-il nommé, et suivi à part ?
9. Chaque réception de support a-t-elle un **critère écrit** et un **instrument** ?
10. Le découpage en zones du second œuvre est-il celui du gros œuvre — et sinon, pourquoi ?

**Glossaire**

| Terme | Ce que c'est |
|---|---|
| **Réservation** | un trou prévu, posé dans le coffrage avant coulage. Coûte {{synthese.cout_du_trou_oublie.cout_d_une_reservation_prevue_MAD}} MAD |
| **Percement** | le même trou, fait après coup. Coûte ×{{synthese.cout_du_trou_oublie.rapport::n1}}, et seulement s'il est accordé |
| **Trémie** | une grande ouverture prévue dans un plancher, dimensionnée avec la structure. Ce n'est pas une grosse réservation : c'est un autre ouvrage |
| **Passage libre** | espacement des armatures moins leur diamètre. Dit ce qui TIENT, jamais ce qui est PERMIS |
| **Date de gel** | date de coulage de la zone moins le délai de diffusion, commande, livraison et pose |
| **Plénum** | le volume entre le faux-plafond et la dalle. Quatre lots s'y croisent, et c'est le goulot du second œuvre |
| **File de corps d'état** | T(Z) = (ΣW + (Z−1)·maxW)/Z + N(Z−1)f. Décroît avec le découpage, bute sur le corps le plus lent |
| **Goulot** | le corps d'état le plus long. Sa durée est le plancher de toute la file |
| **Réception de support** | le moment où la responsabilité change de main. La seule décision irréversible d'une journée de second œuvre |

**Quiz**

**1. Un fourreau de {{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.0}} mm passe-t-il entre deux cadres de cette poutre ?**
**Non, nulle part.** L'espace libre maximal est de
{{synthese.passage_libre.endroits.1.passage_libre_mm::n0}} mm en travée et de
{{synthese.passage_libre.endroits.0.passage_libre_mm::n0}} mm sur appui.

**2. Cette réponse autorise-t-elle un fourreau de {{synthese.passage_libre.endroits.1.plus_gros_diametre_qui_passe_mm}} mm ?**
**Non.** Elle dit qu'il **tient**. Savoir s'il est permis est réglementaire : ⏸.

**3. Quand se joue le carnet de réservations ?**
**Pendant le gros œuvre** — ici entre les jours
{{synthese.gel_des_reservations.fenetre_du_carnet_j.0::n0}} et
{{synthese.gel_des_reservations.fenetre_du_carnet_j.1::n0}}, alors que le second œuvre commence au
jour {{planification.segments_de_travail.SECO.0.0::n0}}.

**4. Quel est le poste le plus lourd d'un percement après coup ?**
**L’{{synthese.cout_du_trou_oublie.poste_le_plus_lourd}}**, pas le carottage — qui ne fait
que {{synthese.cout_du_trou_oublie.postes.0.part_pct::n0}} % du total.

**5. Le découpage en zones peut-il descendre sous la durée du corps d'état le plus lent ?**
**Jamais.** C'est le plancher de la forme fermée :
{{synthese.second_oeuvre.plancher_incompressible_j::n0}} jours ici.

**6. Découper plus fin accélère-t-il toujours ?**
**Non.** Chaque frontière coûte une réinstallation à chaque corps. L'optimum est à
{{synthese.second_oeuvre.zone_optimale}} zones, et au-delà la courbe remonte.

**7. Deux voies donnent {{synthese.second_oeuvre.duree_declaree_par_D2_j::n0}} et {{synthese.second_oeuvre.duree_a_Z_zones_j::n0}} jours. Que conclure ?**
**Qu'elles s'accordent** — {{synthese.second_oeuvre.ecart_avec_D2_j::n1}} jour d'écart sans données
communes. Cela crédite la décomposition, donc on peut piloter avec ; cela ne prouve pas que chacune
des six durées soit juste.

:::memo
## Fiche mémo — lots techniques et second œuvre

**Les trois phrases du module**

> Un trou dans un élément porteur est un sujet de structure, jamais un sujet de lot technique.
> Un carnet de réservations n'est pas un document : c'est une échéance par zone.
> Le second œuvre est une file, et seul le goulot compte.

**La soustraction qui tranche en dix secondes**

$$ \text{passage libre} = \text{espacement des armatures} - \varnothing_{\text{armature}} $$

**La forme fermée de la file**

$$ T(Z) = \frac{\sum W_i + (Z-1)\max W_i}{Z} + N\,(Z-1)\,f \qquad \xrightarrow[Z \to \infty]{} \ \max W_i $$

**Les chiffres de ce chantier**

| | |
|---|---:|
| Espace libre, poutre sur appui / en travée | {{synthese.passage_libre.endroits.0.passage_libre_mm::n0}} mm / {{synthese.passage_libre.endroits.1.passage_libre_mm::n0}} mm |
| Espace libre, dalle | {{synthese.passage_libre.endroits.2.passage_libre_mm::n0}} mm |
| Diamètres qui ne passent **nulle part** | {{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.0}} · {{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.1}} · {{synthese.passage_libre.diametres_qui_ne_passent_nulle_part_mm.2}} mm |
| Réservations du plancher | {{synthese.gel_des_reservations.reservations_sur_le_plancher::n0}} ({{synthese.gel_des_reservations.reservations_bornes.0::n0}} à {{synthese.gel_des_reservations.reservations_bornes.1::n0}}) |
| Fenêtre de gel du carnet | jours {{synthese.gel_des_reservations.fenetre_du_carnet_j.0::n0}} à {{synthese.gel_des_reservations.fenetre_du_carnet_j.1::n0}} — second œuvre au jour {{planification.segments_de_travail.SECO.0.0::n0}} |
| Réservation prévue / percement après coup | {{synthese.cout_du_trou_oublie.cout_d_une_reservation_prevue_MAD}} MAD / **{{synthese.cout_du_trou_oublie.cout_du_percement_MAD::k}} MAD** — ×{{synthese.cout_du_trou_oublie.rapport::n1}} |
| Second œuvre : série / {{synthese.second_oeuvre.nb_zones_du_gros_oeuvre}} zones / plancher | {{synthese.second_oeuvre.duree_en_serie_pure_j::n0}} j / **{{synthese.second_oeuvre.duree_a_Z_zones_j::n0}} j** / {{synthese.second_oeuvre.plancher_incompressible_j::n0}} j |
| Goulot | {{synthese.second_oeuvre.goulot}} |

**Les cinq réflexes**

1. Ouvrir le plan de ferraillage avant d'ouvrir un débat.
2. Trier le carnet par zone de coulage, avec la date de gel en tête de colonne.
3. Sortir du carnet toute réservation qui coupe une armature : ce n'est plus la même procédure.
4. Décomposer le second œuvre par corps d'état, et ne suivre que le goulot.
5. Exiger un critère écrit et un instrument pour chaque réception de support.

**Ce qui reste ⏸**

Règles de percement d'un élément porteur · sections et positions admissibles · distances aux
armatures et aux appuis · rétablissement du degré coupe-feu d'une traversée · classements au feu des
matériaux · tolérances contractuelles de planéité et d'humidité des supports.
:::
