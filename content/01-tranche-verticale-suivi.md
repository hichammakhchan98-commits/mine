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

:::figure {"fn":"planZones","args":"tranche-plancher.figures.zones","titre":"Découpage du plancher de mezzanine en zones de coulage, à la date d'arrêt du suivi","num":1,"large":true,"legende":[{"n":1,"t":"zone de coulage, {{tranche-plancher.figures.zones.longueur_m::n0}} × {{tranche-plancher.figures.zones.largeur_m::n0}} m"},{"n":2,"t":"ligne de poutres PM1, entraxe {{tranche-plancher.figures.zones.entraxe_poutres_m::n2}} m"},{"n":3,"t":"trait bleu : le front PRÉVU par le planning à la même date"}],"voir":["Une zone fait deux travées de trame : le découpage suit la structure, il ne la coupe pas n'importe où.","Chaque limite de zone tombe sur une ligne de poutres, puisque la zone fait un nombre entier de trames : la reprise de bétonnage se fait au droit d'une poutre, et non en pleine dalle. Les lignes tiretées visibles sont les poutres intermédiaires, au milieu de chaque zone.","L'état de chaque zone est lu dans les données de suivi : la figure est un tableau de bord, pas un dessin.","Le trait bleu est le front PRÉVU à la même date : le planning attendait Z5 aux deux tiers et Z6 entamée. L'écart entre la couleur et le trait est le retard, et c'est lui que le § S6 chiffre en dirhams : une figure de suivi qui ne montre que le constat cache la moitié de l'information."],"erreur":"Découper en zones de surface égale sans regarder où tombent les poutres : la reprise se retrouve en pleine travée, là où l'effort tranchant est le plus fort et où le traitement de la reprise coûte le plus cher."}
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
**{{tranche-plancher.variantes.sous_estimation_si_coffrage_egale_surface_pct::n1}} %**, sur le poste
le plus cher en main-d'œuvre.

## S4 · Étude de cas chiffrée : une zone, de bout en bout

### a. Des quantités aux durées

Une durée de tâche, c'est une quantité divisée par une cadence et par un effectif :

$$d = \frac{Q}{c \times n}$$

| Tâche | Quantité | Cadence V3 | Effectif | Durée |
|---|---:|---:|---:|---:|
| Coffrage | {{tranche-plancher.quantites.coffrage_m2::n0}} m² | {{gare.cadences.coffrage_dalle_m2_j.valeur}} m²/j | {{gare.effectifs.coffreurs}} | {{tranche-plancher.durees.coffrage_j::n2}} j |
| Ferraillage des poutres | {{tranche-plancher.quantites.acier_poutres_kg::n0}} kg | {{gare.cadences.ferraillage_poutre_kg_j.valeur}} kg/j | {{gare.effectifs.ferrailleurs_poutres}} | {{tranche-plancher.durees.ferraillage_poutres_j::n2}} j |
| Ferraillage de la dalle | {{tranche-plancher.quantites.acier_dalle_kg::n0}} kg | {{gare.cadences.ferraillage_dalle_kg_j.valeur}} kg/j | {{gare.effectifs.ferrailleurs_dalle}} | {{tranche-plancher.durees.ferraillage_dalle_j::n2}} j |
| Bétonnage | {{tranche-plancher.quantites.beton_m3::n1}} m³ | {{gare.cadences.betonnage_m3_h.valeur}} m³/h | {{gare.effectifs.equipe_betonnage}} | {{tranche-plancher.durees.betonnage_j::n2}} j |

Les quatre cadences de ce tableau sont des hypothèses, et une table Markdown ne permet pas de les
baliser dans la cellule : elles le sont donc ici, une par une, et c'est à ces quatre lignes que le
registre renvoie —
⟦V3|cadence de coffrage de dalle|30 m²/j/compagnon|m²/j|25 à 35|2026|tables et étaiement, plancher courant répétitif⟧,
⟦V3|cadence de ferraillage de dalle|300 kg/j/compagnon|kg/j|250 à 400|2026|treillis et chapeaux, pose à plat⟧,
⟦V3|cadence de ferraillage de poutre|150 kg/j/compagnon|kg/j|120 à 180|2026|cages, façonnage et pose en place⟧,
⟦V3|cadence de bétonnage|30 m³/h|m³/h|25 à 40|2026|pompe à béton, équipe complète⟧.
Aucune ne vient d'un attachement réel : **ce sont elles qu'il faudra recaler en premier** sur vos
propres relevés, parce que toutes les durées du module en descendent.

:::encart {"genre":"attente","titre":"Pourquoi ceci n'est PAS un contre-calcul"}
La durée de coffrage peut se calculer de deux façons : par la **cadence unitaire** multipliée par
l'effectif ({{tranche-plancher.durees.contre_calcul_duree_coffrage.voie_A_cadence_unitaire_x_effectif_j::n3}} j),
ou par un **rendement d'équipe** déclaré séparément
({{tranche-plancher.durees.contre_calcul_duree_coffrage.voie_B_rendement_d_equipe_j::n3}} j). Écart :
**{{tranche-plancher.durees.contre_calcul_duree_coffrage.ecart_pct::n2}} %**.

Il serait tentant d'appeler cela un contre-calcul. **C'en est pas un** : les deux voies partagent
intégralement la surface de coffrage, la seule grandeur susceptible d'être fausse. Elles ne comparent
que deux taux, pas deux chemins — si la surface est erronée, elles se trompent ensemble.

Ce que ce contrôle vaut réellement : il vérifie que **deux hypothèses V3 sont mutuellement cohérentes
au point retenu**. Et il faut dire sur quelle largeur il tient, sinon il se fait passer pour plus
qu'il n'est. La tolérance de
{{tranche-plancher.durees.contre_calcul_duree_coffrage.tolerance_pct::n0}} % n'est respectée que si le
rendement d'équipe tombe entre
**{{tranche-plancher.durees.contre_calcul_duree_coffrage.plage_de_rendement_qui_passe_m2_j.0::n0}} et
{{tranche-plancher.durees.contre_calcul_duree_coffrage.plage_de_rendement_qui_passe_m2_j.1::n0}} m²/j** —
alors que la fourchette déclarée pour cette même hypothèse va de
{{tranche-plancher.durees.contre_calcul_duree_coffrage.fourchette_declaree_m2_j.0::n0}} à
{{tranche-plancher.durees.contre_calcul_duree_coffrage.fourchette_declaree_m2_j.1::n0}} m²/j. Le
contrôle ne passe donc que sur
**{{tranche-plancher.durees.contre_calcul_duree_coffrage.part_de_la_fourchette_qui_passe_pct::n0}} %
de ce que les données elles-mêmes donnent pour plausible** : il est satisfait par le point choisi par
l'auteur, pas par les données. Pris à la borne basse, il échoue.

C'est l'information utile, et elle ne se lit pas sur un verdict « OK ». **Demandez toujours à un
contrôle quelle est la largeur de ce qui le fait passer** : un contrôle qui ne tient que sur un quart
du domaine déclaré est un contrôle qui parle du choix de son auteur.

**Ce module a donc deux contre-calculs, pas trois** : celui du cycle (deux algorithmes) et le
recoupement physique de l'avancement (deux sources).
:::

### b. Des durées au cycle

La somme des durées vaut {{tranche-plancher.cycle_zone.somme_des_durees_j::n2}} jours. Le cycle réel
vaut **{{tranche-plancher.cycle_zone.duree_j::n2}} jours**. La différence —
{{tranche-plancher.cycle_zone.gain_du_recouvrement_j::n2}} jours, soit
{{tranche-plancher.cycle_zone.gain_pct::n0}} % — n'est pas une erreur : c'est le **recouvrement**. Le
ferraillage des poutres démarre avant que le coffrage soit terminé, celui de la dalle avant la fin
des poutres. C'est tout l'objet du chemin critique, et c'est pour cela qu'additionner des durées ne
donne jamais un planning.

:::figure {"fn":"rotation","args":"tranche-plancher.figures.rotation","titre":"Rotation des huit zones, et le coffrage qu'elle immobilise","num":2,"large":true,"voir":["Chaque ligne est une zone, chaque couleur une phase : bleu clair le coffrage, jaune le ferraillage des poutres, vert celui de la dalle, brique le point d'arrêt, bleu le bétonnage, puis la cure en gris clair et le décoffrage en gris. Les phases d'une même zone SE RECOUVRENT : c'est ce recouvrement qui fait le cycle.","La droite tiretée joint les débuts de zone : sa pente est la cadence. Une cadence qui fléchit se voit ici avant d'apparaître dans un indicateur.","La courbe du bas est le coffrage immobilisé jour par jour. Elle oscille entre deux et trois zones ouvertes, et ses sommets frôlent la ligne du parc : c'est la contrainte que le planning doit respecter, et elle ne se lit sur aucun Gantt."],"erreur":"Lire la rotation sur un Gantt d'une seule zone. Un Gantt de zone montre le cycle ; il ne montre ni la cadence, ni le nombre de zones ouvertes en même temps, ni le matériel que cela mobilise — c'est-à-dire précisément ce qui décide si le planning est tenable."}
:::

:::figure {"fn":"gantt","args":"tranche-plancher.figures.gantt","titre":"Gantt d'une zone, avec les recouvrements","num":3,"large":true,"voir":["Ici les sept tâches sont critiques — la couleur ne distingue donc rien sur ce réseau : tout retard, où qu'il soit, décale la fin d'autant. C'est la situation d'un cycle en chaîne, sans tâche de réserve.","Le ferraillage des poutres commence avant la fin du coffrage : c'est un décalage négatif, pas une erreur de saisie.","Les durées ne sont pas saisies : elles viennent des quantités divisées par les cadences et les effectifs."],"erreur":"Saisir un planning en tapant des durées à dire d'expert, puis vérifier après coup si les effectifs suivent. L'ordre inverse — quantité, cadence, effectif, durée — est le seul qui permette de défendre un planning en réunion."}
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
est exacte sur un réseau de quelques tâches, donc utile comme contre-calcul.

**Si elles divergeaient, le contrôle ne dirait pas laquelle est fausse** — et il ne faut surtout pas
désigner un coupable d'avance. Ce module a d'abord publié le contraire : « c'est le parcours
avant/arrière qui serait faux ». C'était l'inverse de la vérité. Sur un réseau à décalage négatif
important, c'est l'**énumération** qui rendait 1 jour là où la réponse était 10, parce qu'elle ne
lisait la fin du projet qu'aux tâches sans successeur. Une « référence » n'est une référence que
tant qu'elle a été mise à l'épreuve.

C'est à quoi sert l'**étalonnage** : le moteur est confronté à **neuf** réseaux dont la durée se pose
à la main — chaîne, branches parallèles, recouvrement, tâche isolée, jalons de durée nulle, deux
départs, deux fins, et les trois régimes à décalage négatif qui l'avaient mis en défaut. Il refuse
par ailleurs un circuit comme un prédécesseur inconnu.
:::

### c. Du cycle au coût

| Poste | Quantité | Prix unitaire V3 | Montant |
|---|---:|---:|---:|
| Béton | {{tranche-plancher.quantites.beton_m3::n1}} m³ | {{gare.prix_unitaires_MAD.postes.beton_m3.valeur}} MAD/m³ | {{tranche-plancher.cout_zone.beton_MAD::n0}} MAD |
| Acier | {{tranche-plancher.quantites.acier_kg::n0}} kg | {{gare.prix_unitaires_MAD.postes.acier_kg.valeur}} MAD/kg | {{tranche-plancher.cout_zone.acier_MAD::n0}} MAD |
| Coffrage | {{tranche-plancher.quantites.coffrage_m2::n0}} m² | {{gare.prix_unitaires_MAD.postes.coffrage_m2.valeur}} MAD/m² | {{tranche-plancher.cout_zone.coffrage_MAD::n0}} MAD |
| **Total d'une zone** | | | **{{tranche-plancher.cout_zone.total_fournitures_et_mise_en_oeuvre_MAD::n0}} MAD** |

Les trois prix unitaires, déclarés de la même façon :
⟦V3|prix du béton posé|1 250 MAD/m³|MAD/m³|1 100 à 1 450|2026|béton prêt à l'emploi, pompé, mis en œuvre⟧,
⟦V3|prix de l'acier posé|17 MAD/kg|MAD/kg|14 à 20|2026|acier HA façonné et posé⟧,
⟦V3|prix du coffrage posé|180 MAD/m²|MAD/m²|150 à 220|2026|tables et étaiement, amortissement inclus⟧.
Aucun bordereau n'ayant été fourni (question 7 de l'Étape 0, restée sans réponse), ces trois
fourchettes sont larges à dessein.

Soit **{{tranche-plancher.cout_zone.cout_au_m2_MAD::n0}} MAD/m²** de plancher, gros œuvre seul.

:::encart {"genre":"alerte","titre":"Le contrôle qui échoue, et ce qu'il révèle vraiment"}
La zone mobilise {{tranche-plancher.cout_zone.heures_de_main_oeuvre::n0}} heures de main-d'œuvre
directe. À ⟦V3|prix horaire d'un compagnon|45 MAD/h|MAD/h|35 à 60|2026|compagnon nu, charges comprises, sans encadrement⟧,
cela fait {{tranche-plancher.cout_zone.main_oeuvre_MAD::n0}} MAD, soit
**{{tranche-plancher.cout_zone.coherence_prix_horaire.part_constatee_pct::n1}} %** du total — alors que
la main-d'œuvre directe pèse normalement
⟦V3|part de main d'œuvre directe dans un prix posé|15 à 30 %|%|15 à 30|2026|gros œuvre, prix posé tout compris⟧.

**Première explication, partielle.** Les prix unitaires sont des prix **posés** : la main-d'œuvre y
est déjà. L'additionner au total la compterait deux fois — c'est l'erreur de métré la plus fréquente,
et la ligne « main-d'œuvre » ci-dessus est donc un **contrôle**, pas un poste.

**Mais cela n'explique pas l'écart.** Chiffrons chaque cause au lieu de les énumérer :

| Ce qu'on ajoute | Part de main-d'œuvre |
|---|---:|
| équipes de production seules, prix horaire au point déclaré | {{tranche-plancher.cout_zone.coherence_prix_horaire.causes_chiffrees.0.part_pct::n2}} % |
| + chef d'équipe et grutier | {{tranche-plancher.cout_zone.coherence_prix_horaire.causes_chiffrees.1.part_pct::n2}} % |
| + prix horaire au haut de sa fourchette | {{tranche-plancher.cout_zone.coherence_prix_horaire.causes_chiffrees.2.part_pct::n2}} % |
| **fourchette attendue** | **15 à 30 %** |

Même en empilant toutes les causes invoquées, il reste un facteur
**{{tranche-plancher.cout_zone.coherence_prix_horaire.facteur_encore_inexplique::n1}}**. Il faut donc
le dire : **cet écart n'est pas expliqué.** Le suspect le plus probable est ailleurs — des **cadences
optimistes d'un facteur deux à trois**, qui sont l'entrée de *toutes* les durées publiées dans ce
module. Ce n'est pas une conclusion, c'est une hypothèse : seuls des attachements réels trancheraient.

**Ce qu'il faut en retenir, et c'est le plus important de ce module.** Un contrôle qui échoue et qu'on
habille d'une explication plausible est pire qu'un contrôle absent : il donne la paix de l'esprit sans
la mériter. Ici le contrôle a fait son travail — il désigne les cadences, c'est-à-dire la racine de
tout le reste. **C'est la première chose à recaler sur vos attachements**, avant les prix.
:::

### d. Du coût au planning du plancher

Les {{tranche-plancher.planning_plancher.nb_zones}} zones s'enchaînent à une cadence de
**{{tranche-plancher.planning_plancher.cadence_zone_j::n1}} jours par zone** : l'équipe de coffrage
attaque la zone suivante pendant que la précédente est en cure. Le plancher complet prend
**{{tranche-plancher.planning_plancher.duree_totale_j::n1}} jours ouvrés**.

**D'où vient ce {{tranche-plancher.planning_plancher.cadence_zone_j::n1}}, et pourquoi ce n'est pas le
cycle.** Le cycle d'une zone vaut {{tranche-plancher.cycle_zone.duree_j::n2}} jours, mais une zone ne
démarre pas tous les {{tranche-plancher.cycle_zone.duree_j::n2}} jours : la cure et le décoffrage
n'occupent aucune équipe. La cadence est bornée par les tâches qui mobilisent une équipe **dédiée**,
donc une seule zone à la fois :

$$ \text{cadence} = \max_{\text{équipes dédiées}} (d_i) + d_{\text{bétonnage}} $$

Les **trois** tâches à équipe dédiée sont le coffrage
({{tranche-plancher.regle_cadence.durees_des_equipes_dediees_j.coffrage_j::n2}} j), le ferraillage des
**poutres** ({{tranche-plancher.regle_cadence.durees_des_equipes_dediees_j.ferraillage_poutres_j::n2}} j)
et le ferraillage de la **dalle**
({{tranche-plancher.regle_cadence.durees_des_equipes_dediees_j.ferraillage_dalle_j::n2}} j) : chacune
mobilise une équipe qui ne peut être que sur une zone à la fois. La plus longue borne la rotation ; le
bétonnage s'ajoute, parce qu'il immobilise la zone, la pompe et la grue pour tout le monde. La cure et
le décoffrage ne comptent pas : ils n'occupent aucune équipe.

Ici la borne est le **{{tranche-plancher.regle_cadence.tache_qui_borne}}**, et la cadence vaut
**{{tranche-plancher.planning_plancher.cadence_zone_j::n1}} j**.

:::encart {"genre":"alerte","titre":"Cette formule a été publiée fausse, et voici comment"}
La première version de ce module écrivait `max(coffrage ; ferraillage de dalle) + bétonnage` : elle
**oubliait le ferraillage des poutres**. Sur le cas de référence, l'oubli ne se voit pas — le
ferraillage de dalle est le plus long et masque celui des poutres —, et la cadence de
{{tranche-plancher.planning_plancher.cadence_zone_j::n1}} j était juste **par coïncidence**.

Elle devenait fausse dès qu'on renforçait l'équipe de dalle, c'est-à-dire exactement dans l'exercice
que le module propose. Et le module énonçait pourtant la règle qui l'aurait sauvé : *renforcer une
tâche critique ne garantit un gain que jusqu'au moment où un autre chemin prend le relais.* Il
l'écrivait en toutes lettres, et sa propre formule la violait.

**La leçon de contrôle** : une formule juste sur le cas publié n'est pas une formule juste. C'est
pourquoi `calc/tests/` vérifie désormais que la règle couvre les trois équipes, et qu'un renfort de
l'équipe de dalle fait bien **passer la borne au ferraillage des poutres**.
:::

Deux conséquences, et ce sont elles qui rendent l'exercice 3 calculable : la cadence ne descend pas
sous {{tranche-plancher.durees.betonnage_j::n2}} j plus la plus longue des trois tâches d'équipe, et
renforcer une équipe ne sert que **si c'est elle** qui tient le `max` — après quoi c'est une autre
qui borne.

:::encart {"genre":"voir","titre":"La contrainte que les plannings de rotation oublient : le parc de coffrage"}
Le coffrage d'une zone n'est pas libéré au coulage : il reste en place pendant toute la cure et
jusqu'au décoffrage, soit **un cycle entier**. À une cadence plus courte que le cycle, plusieurs zones
en détiennent donc en même temps :

$$ n_{\text{zones coffrées}} = \left\lceil \frac{\text{cycle}}{\text{cadence}} \right\rceil $$

soit ⌈{{tranche-plancher.cycle_zone.duree_j::n2}} / {{tranche-plancher.planning_plancher.cadence_zone_j::n1}}⌉ =
**{{tranche-plancher.coherence_materiel.zones_coffrees_simultanement}} zones**. Il faut donc **{{tranche-plancher.coherence_materiel.coffrage_mobilise_m2::n0}} m²** de tables et de
joues disponibles simultanément, pour
⟦V3|parc de tables coffrantes du chantier|{{tranche-plancher.coherence_materiel.stock_declare_m2::n0}} m²|m²|1 000 à 1 500|2026|parc affecté au plancher de la mezzanine, déduit du planning et non posé a priori⟧
déclarés : une marge de {{tranche-plancher.coherence_materiel.marge_m2::n0}} m², c'est-à-dire
**rien**.

Et les **étais** ne se comptent pas sur les mêmes zones. Une zone décoffrée n'est pas libérée : ses
étais de reprise restent en place
⟦V3|maintien des étais de reprise après décoffrage|14 jours|j|7 à 28|2026|le critère réel est une résistance et une redistribution de charges, pas une durée ; aucune valeur normative n'est disponible en § 5.0⟧.
Le nombre de zones étayées vaut donc ⌈(cycle + maintien) / cadence⌉ =
**{{tranche-plancher.coherence_materiel.zones_etayees_simultanement}} zones**, et non les
{{tranche-plancher.coherence_materiel.zones_coffrees_simultanement}} zones coffrées : il faut
**{{tranche-plancher.coherence_materiel.etais_necessaires::n0}} étais** là où un décompte fait sur les
seules zones coffrées en annoncerait
{{tranche-plancher.coherence_materiel.etais_si_on_ne_comptait_que_les_zones_coffrees::n0}}. **Un
facteur deux sur un poste de location**, et il vient d'une question de définition, pas de calcul.

C'est un **contrôle de cohérence du module**, pas un commentaire : `coherence_materiel.verdict` vaut
*{{tranche-plancher.coherence_materiel.verdict}}*, et il passerait au rouge si la cadence descendait
sans que le parc suive. Une cadence annoncée en réunion sans ce calcul est une cadence qui sera tenue
par le parc, pas par le planning — et c'est le parc qui aura raison.
:::

:::figure {"fn":"histogramme","args":"tranche-plancher.figures.effectifs","titre":"Effectif présent sur le plancher, jour par jour","num":4,"large":true,"voir":["Les jours les plus chargés sont ceux où deux équipes se recouvrent sur deux zones voisines : c'est le recouvrement du cycle, vu côté effectif.","La pointe donne le dimensionnement de la base-vie et des moyens — c'est elle qu'il faut regarder, pas la moyenne.","Les jours à zéro de la fin ne sont pas une erreur : la cure n'occupe personne. Un histogramme qui n'en montre jamais est un histogramme qui compte des présents imaginaires."],"erreur":"Lisser cet histogramme en moyenne et dimensionner la base-vie dessus. Le jour de pointe, il manque des vestiaires et des réfectoires pour tout le monde."}
:::

## S5 · Erreurs fréquentes, et ce qu'elles coûtent

| Erreur | Comment elle se voit | Ce qu'elle coûte |
|---|---|---|
| Coffrage compté à la surface de dalle | le ratio tombe à 1,00 au lieu de {{tranche-plancher.quantites.ratio_coffrage_m2_par_m2::n2}} | {{tranche-plancher.variantes.sous_estimation_si_coffrage_egale_surface_pct::n1}} % du poste le plus cher en main-d'œuvre |
| Main-d'œuvre additionnée à un prix posé | le total gonfle sans que les quantités bougent | double compte, et une situation rejetée au visa |
| Durées saisies à dire d'expert | aucun lien entre l'effectif et la durée | un planning indéfendable en réunion |
| Zone découpée sans regarder les poutres | reprise de bétonnage en pleine travée | traitement de reprise, et un point de contrôle en plus |
| Avancement déclaré à vue de nez | l'écart n'apparaît qu'au contre-calcul (§ S6) | une situation surévaluée, puis un rattrapage brutal |
| Cure comptée comme du temps perdu | le cycle paraît plus long qu'il n'est | une cadence annoncée trop pessimiste, et des moyens surdimensionnés |

## S6 · Du planning au reporting : la valeur acquise

À la date d'arrêt — **{{tranche-plancher.suivi.libelle_arret}}**, déduite du planning et non écrite à
la main — {{valeur-acquise.zones_prevues_equivalentes::n2}} zones étaient prévues,
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
| Dérive prévue | **{{valeur-acquise.derive_signe}} {{valeur-acquise.derive_prevue_abs_MAD::n0}} MAD** |

{{valeur-acquise.lecture}}

:::figure {"fn":"courbeS","args":"tranche-plancher.figures.courbe_s","titre":"Courbe en S prévue, et le constat à la date d'arrêt","num":5,"large":true,"voir":["Le constat est UN point, pas une courbe : les données ne portent qu'un relevé, celui de la date d'arrêt. Tant qu'il n'y en a qu'un, tracer une ligne reviendrait à publier une prévision déguisée en constat — ce que l'erreur courante ci-dessous interdit.","L'écart vertical entre la courbe et le point est le retard en valeur, pas en jours : c'est SV, et il vaut ici ce que le tableau S6 annonce.","La courbe prévue, elle, est bien une courbe : elle vient du réseau, zone par zone. Sa pente maximale est le moment où le chantier consomme le plus de moyens."],"erreur":"Tracer un « réalisé » en multipliant la courbe prévue par le taux d'avancement constaté. La figure est alors jolie, continue, et ne contient aucune information que le point unique ne portait déjà — c'est exactement l'erreur que cette figure a commise dans sa première version."}
:::

:::encart {"genre":"voir","titre":"Contre-calcul : l'avancement déclaré colle-t-il aux relevés ?"}
La valeur acquise se calcule **deux fois**. Voie A, par les coûts : budget à l'achèvement × avancement
déclaré → {{valeur-acquise.contre_calcul.voie_A_par_les_couts_MAD::n0}} MAD. Voie B, par les
**quantités relevées** sur le chantier → {{valeur-acquise.contre_calcul.voie_B_par_les_quantites_MAD::n0}} MAD.
Écart : {{valeur-acquise.contre_calcul.ecart_pct::n2}} %, au-delà de la tolérance de
{{valeur-acquise.contre_calcul.tolerance_pct::n0}} %.

**Et pourtant ce n'est pas un signal.** Voici pourquoi, et c'est le vrai sujet de ce paragraphe.

Comparer deux montants en dirhams mélange des postes dont la fiabilité n'a rien à voir. Le
recoupement qui fait foi se fait **en unités physiques, poste par poste** :

| Poste | Nature | Théorique × avancement | Relevé | Écart |
|---|---|---:|---:|---:|
| Béton | **géométrique** | {{valeur-acquise.recoupement_physique.postes.0.theorique_x_avancement::n1}} m³ | {{valeur-acquise.recoupement_physique.postes.0.releve::n1}} m³ | {{valeur-acquise.recoupement_physique.postes.0.ecart_pct::n2}} % |
| Coffrage | **géométrique** | {{valeur-acquise.recoupement_physique.postes.1.theorique_x_avancement::n1}} m² | {{valeur-acquise.recoupement_physique.postes.1.releve::n1}} m² | {{valeur-acquise.recoupement_physique.postes.1.ecart_pct::n2}} % |
| Acier | issu d'un **ratio V3** | {{valeur-acquise.recoupement_physique.postes.2.theorique_x_avancement::n0}} kg | {{valeur-acquise.recoupement_physique.postes.2.releve::n0}} kg | {{valeur-acquise.recoupement_physique.postes.2.ecart_pct::n2}} % |

Les deux postes **géométriques** sont sous le pour cent : l'avancement déclaré tient. L'écart vient
surtout de l'acier — dont le ratio V3 ouvre une étendue de
{{valeur-acquise.recoupement_physique.rapports.etendue_du_ratio_pct::n1}} %, soit
**{{valeur-acquise.recoupement_physique.rapports.fourchette_du_ratio_sur_ecart_constate::n0}} fois**
l'écart constaté sur ce poste
({{valeur-acquise.recoupement_physique.postes.2.ecart_pct::n2}} %). Autrement dit : **l'alarme en
dirhams était du bruit promu au rang de signal.**

**À quoi ressemblerait un vrai signal.** Le même contrôle, si le relevé de béton était court de 5 % :

| Poste | Écart | |
|---|---:|---|
| Béton | {{valeur-acquise.recoupement_contre_exemple.postes.0.ecart_pct::n2}} % | ← **signal** |
| Coffrage | {{valeur-acquise.recoupement_contre_exemple.postes.1.ecart_pct::n2}} % | |
| Acier | {{valeur-acquise.recoupement_contre_exemple.postes.2.ecart_pct::n2}} % | attendu |

Là, le béton décroche alors qu'il est **géométrique** : il ne dépend d'aucune hypothèse. C'est une
vraie dérive de l'avancement déclaré, et c'est à ce moment-là qu'on demande les attachements.

**La leçon, qui vaut pour tout tableau de bord** : un seuil n'a de sens qu'au regard de l'incertitude
de ce qu'il mesure. Un contrôle réglé plus fin que ses entrées sonne tout le temps, et un contrôle qui
sonne tout le temps ne se regarde plus.

**Pourquoi la voie B est indépendante.** Une première version multipliait les quantités *théoriques*
par l'avancement *déclaré* : algébriquement identique à la voie A, écart nul par construction. Deux
voies ne sont indépendantes que si elles ne partagent pas leur entrée décisive.
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

**Les cinq contrôles avant de viser une situation**

1. Le ratio de coffrage est-il > 1,00 ? Sinon les joues de poutres ont été oubliées.
2. La main-d'œuvre est-elle additionnée à un prix posé ? Si oui, double compte.
3. L'avancement déclaré est-il recoupé **en m³ et en m², jamais en dirhams** ? Sur le béton et le
   coffrage, qui sont géométriques, un écart au-delà de
   {{valeur-acquise.recoupement_physique.seuil_poste_geometrique_pct::n0}} % met en cause
   l'avancement : demandez les attachements. Sur l'**acier**, un écart ne prouve rien — il vient
   d'un ratio dont l'étendue vaut
   {{valeur-acquise.recoupement_physique.rapports.etendue_du_ratio_pct::n1}} %, soit
   {{valeur-acquise.recoupement_physique.rapports.fourchette_du_ratio_sur_seuil_geometrique::n0}} fois
   le seuil.
4. Les durées viennent-elles des quantités, ou d'un dire d'expert ?
5. La cadence annoncée tient-elle **en tables** ? ⌈cycle / cadence⌉ zones détiennent du coffrage en
   même temps : comparez au parc avant d'annoncer une date.

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
dalle de {{gare.elements.dalles.0.epaisseur_m::n2}} m,
{{tranche-plancher.quantites.n_poutres}} poutres de
{{gare.elements.poutres.0.longueur_dans_zone_m::n2}} m, retombée
{{gare.elements.poutres.0.retombee_sous_dalle_m::n2}} m sous dalle, largeur
{{gare.elements.poutres.0.b_m::n2}} m.

Calculez le volume de béton, puis la surface de coffrage en détaillant sous-face, joues et fond.

**Corrigé.** Dalle : {{tranche-plancher.quantites.surface_m2::n0}} ×
{{gare.elements.dalles.0.epaisseur_m::n2}} = {{tranche-plancher.quantites.beton_dalle_m3::n1}} m³.
Poutres : {{tranche-plancher.quantites.n_poutres}} ×
{{gare.elements.poutres.0.longueur_dans_zone_m::n2}} × {{gare.elements.poutres.0.b_m::n2}} ×
{{gare.elements.poutres.0.retombee_sous_dalle_m::n2}} =
{{tranche-plancher.quantites.beton_poutres_m3::n1}} m³. Total
**{{tranche-plancher.quantites.beton_m3::n1}} m³**.
Coffrage : sous-face {{tranche-plancher.quantites.surface_m2::n0}} −
({{tranche-plancher.quantites.n_poutres}} × {{gare.elements.poutres.0.longueur_dans_zone_m::n2}} ×
{{gare.elements.poutres.0.b_m::n2}}) =
{{tranche-plancher.quantites.coffrage_detail_m2.sous_face_dalle::n0}} m² ;
joues {{tranche-plancher.quantites.n_poutres}} ×
{{gare.elements.poutres.0.longueur_dans_zone_m::n2}} ×
{{gare.elements.poutres.0.retombee_sous_dalle_m::n2}} × 2 =
{{tranche-plancher.quantites.coffrage_detail_m2.joues_de_poutres::n0}} m² ;
fond {{tranche-plancher.quantites.n_poutres}} ×
{{gare.elements.poutres.0.longueur_dans_zone_m::n2}} × {{gare.elements.poutres.0.b_m::n2}} =
{{tranche-plancher.quantites.coffrage_detail_m2.fond_de_poutres::n0}} m².
Plus {{tranche-plancher.quantites.coffrage_detail_m2.rives_pct::n0}} % de rives →
**{{tranche-plancher.quantites.coffrage_m2::n0}} m²**.
:::

:::exercice {"titre":"2 · L'effet d'un effectif sur le cycle","niveau":"application"}
Les ferrailleurs de dalle passent de {{gare.effectifs.ferrailleurs_dalle}} à 12. Que devient la durée
de ferraillage de dalle, et le cycle de la zone gagne-t-il autant ?

**Corrigé.** La durée de ferraillage de dalle passe de
{{tranche-plancher.variantes.reference.ferraillage_dalle_j::n2}} j à
**{{tranche-plancher.variantes.effectif_renforce.ferraillage_dalle_j::n2}} j**.

Le cycle, lui, passe de {{tranche-plancher.variantes.reference.cycle_j::n2}} à
**{{tranche-plancher.variantes.effectif_renforce.cycle_j::n2}} j** : il gagne exactement ce que la
tâche a gagné, parce qu'elle est sur le chemin critique **et qu'aucun autre chemin ne devient
critique** à ce niveau de renfort. Ce n'est pas toujours le cas, et c'est la règle à retenir :
**renforcer une tâche critique ne garantit un gain que jusqu'au moment où un autre chemin prend le
relais.** Refaites tourner le réseau avant d'annoncer un gain en réunion — ne le déduisez jamais de
la seule tâche renforcée.

Effet sur l'ensemble, et c'est là que l'exercice se joue : la cadence ne descend **pas** autant que la
tâche. Elle passe de {{tranche-plancher.variantes.reference.cadence_j::n2}} à
**{{tranche-plancher.variantes.effectif_renforce.cadence_j::n2}} j/zone seulement**, parce que la
borne a changé d'équipe : ce n'est plus le ferraillage de dalle qui tient le `max`, c'est le
**ferraillage des poutres**
({{tranche-plancher.variantes.effectif_renforce.ferraillage_poutres_j::n2}} j pour une équipe de
{{gare.effectifs.ferrailleurs_poutres}}, inchangée). Le plancher passe donc de
{{tranche-plancher.variantes.reference.duree_plancher_j::n1}} à
**{{tranche-plancher.variantes.effectif_renforce.duree_plancher_j::n1}} jours**, et non à ce que la
seule tâche renforcée laissait espérer. L'effectif de pointe, lui, monte de
{{tranche-plancher.variantes.reference.pointe_effectif}} à
{{tranche-plancher.variantes.effectif_renforce.pointe_effectif}} personnes, et le coffrage mobilisé
reste à {{tranche-plancher.variantes.effectif_renforce.coffrage_mobilise_m2::n0}} m² pour
{{tranche-plancher.coherence_materiel.stock_declare_m2::n0}} m² au parc.

Retenez le cheminement : un effectif change une durée, la durée change une cadence — **jusqu'à ce
qu'une autre équipe prenne la borne**. C'est l'objet de l'exercice suivant.
:::

:::exercice {"titre":"3 · Défendre une cadence en réunion","niveau":"probleme"}
Le maître d'ouvrage demande le plancher en 25 jours ouvrés au lieu de
{{tranche-plancher.planning_plancher.duree_totale_j::n1}}. Vous ne pouvez ni changer les quantités ni
toucher à la cure. Quels leviers reste-t-il, et lequel défendez-vous ?

**Corrigé.** Trois leviers, et le premier ne suffit **pas** — c'est précisément ce qu'il faut
vérifier avant d'annoncer quoi que ce soit.

**(a) Renforcer la tâche qui borne la cadence.** Elle est aujourd'hui le ferraillage de dalle. Passer
de {{gare.effectifs.ferrailleurs_dalle}} à {{tranche-plancher.variantes.effectif_renforce.ferrailleurs_dalle}}
ferrailleurs ramène cette tâche à
{{tranche-plancher.variantes.effectif_renforce.ferraillage_dalle_j::n2}} j — mais la cadence ne tombe
qu'à **{{tranche-plancher.variantes.effectif_renforce.cadence_j::n2}} j/zone**, parce que le
**ferraillage des poutres** ({{tranche-plancher.variantes.effectif_renforce.ferraillage_poutres_j::n2}} j)
reprend aussitôt la borne. Le plancher tombe à
**{{tranche-plancher.variantes.effectif_renforce.duree_plancher_j::n1}} jours** : **au-dessus de la
cible de 25**. Quatre ferrailleurs de plus, et la promesse n'est pas tenue.

**(a bis) Renforcer les deux équipes de ferraillage.** C'est le levier qui marche, et il ne se devine
pas : il se calcule. En portant la dalle à
{{tranche-plancher.variantes.effectif_renforce_deux_equipes.ferrailleurs_dalle}} **et** les poutres à
{{tranche-plancher.variantes.effectif_renforce_deux_equipes.ferrailleurs_poutres}}, la borne revient
au {{tranche-plancher.variantes.effectif_renforce_deux_equipes.tache_qui_borne_la_cadence}}, la
cadence tombe à **{{tranche-plancher.variantes.effectif_renforce_deux_equipes.cadence_j::n2}} j/zone**
et le plancher à **{{tranche-plancher.variantes.effectif_renforce_deux_equipes.duree_plancher_j::n1}}
jours** — **sous la cible**. Le prix : effectif de pointe à
{{tranche-plancher.variantes.effectif_renforce_deux_equipes.pointe_effectif}} personnes contre
{{tranche-plancher.variantes.reference.pointe_effectif}}, et
{{tranche-plancher.variantes.effectif_renforce_deux_equipes.coffrage_mobilise_m2::n0}} m² de tables
immobilisées pour {{tranche-plancher.coherence_materiel.stock_declare_m2::n0}} au parc — le parc
suit, de justesse.

**(b) Découper en zones plus petites.** Plus de zones, cycle plus court chacune, mais plus de reprises
de bétonnage et plus de points d'arrêt. On gagne sur le papier, on perd en qualité et en contrôle.

**(c) Dédoubler le front sur deux zones en parallèle.** Le levier le plus puissant, et le plus cher :
un **second jeu complet** de tables — de l'ordre de
{{tranche-plancher.coherence_materiel.coffrage_mobilise_m2::n0}} m² de plus — et une grue qui suive.
**Inutile ici**, puisque (a bis) atteint la cible sans toucher au parc.

**Ce qu'il faut dire en réunion** : « 25 jours est atteignable en portant le ferraillage de dalle à
{{tranche-plancher.variantes.effectif_renforce_deux_equipes.ferrailleurs_dalle}} compagnons **et celui
des poutres à {{tranche-plancher.variantes.effectif_renforce_deux_equipes.ferrailleurs_poutres}}** :
{{tranche-plancher.variantes.effectif_renforce_deux_equipes.duree_plancher_j::n1}} jours, pointe à
{{tranche-plancher.variantes.effectif_renforce_deux_equipes.pointe_effectif}} personnes,
{{tranche-plancher.variantes.effectif_renforce_deux_equipes.coffrage_mobilise_m2::n0}} m² de tables
contre {{tranche-plancher.coherence_materiel.stock_declare_m2::n0}} au parc. Renforcer la seule équipe
de dalle ne donnerait que {{tranche-plancher.variantes.effectif_renforce.duree_plancher_j::n1}} jours :
je l'ai vérifié. Je confirme la base-vie vendredi. » Pas « on va essayer » ; et surtout pas la
première réponse venue, qui était fausse de
{{tranche-plancher.variantes.effectif_renforce.duree_plancher_j::n1}} contre 25.


*Le piège de cet exercice : croire qu'une tâche renforcée se traduit en cadence. Elle ne s'y traduit
que tant qu'elle **tient la borne** — après quoi une autre équipe la reprend, et le gain s'arrête
sans prévenir. Refaites tourner le réseau avant toute annonce : c'est trente secondes de calcul
contre une date intenable annoncée en réunion. Le second piège, plus discret, est de s'arrêter à la
durée : une cadence tenable en jours peut être intenable en tables, et le parc a le dernier mot.*
:::

:::exercice {"titre":"4 · Viser, ou refuser de viser, une situation de travaux","niveau":"revue critique"}
Un sous-traitant présente la situation suivante pour la zone en cours, qu'il déclare à
{{tranche-plancher.situation_exercice.avancement_declare_pct::n0}} % :

| Poste | Quantité déclarée | Prix unitaire | Montant |
|---|---:|---:|---:|
| Béton | {{tranche-plancher.situation_exercice.postes.0.quantite::n1}} m³ | {{tranche-plancher.situation_exercice.postes.0.prix_unitaire}} | {{tranche-plancher.situation_exercice.postes.0.montant_MAD::n0}} |
| Acier | {{tranche-plancher.situation_exercice.postes.1.quantite::n0}} kg | {{tranche-plancher.situation_exercice.postes.1.prix_unitaire}} | {{tranche-plancher.situation_exercice.postes.1.montant_MAD::n0}} |
| Coffrage | {{tranche-plancher.situation_exercice.postes.2.quantite::n0}} m² | {{tranche-plancher.situation_exercice.postes.2.prix_unitaire}} | {{tranche-plancher.situation_exercice.postes.2.montant_MAD::n0}} |
| Main-d'œuvre | {{tranche-plancher.situation_exercice.main_oeuvre_h::n0}} h | {{gare.prix_unitaires_MAD.postes.main_oeuvre_h.valeur}} | {{tranche-plancher.situation_exercice.main_oeuvre_MAD::n0}} |
| **Total** | | | **{{tranche-plancher.situation_exercice.total_presente_MAD::n0}}** |

**Trois points appellent une vérification. Deux sont des erreurs, un est correct — lequel ?**
Dites aussi ce que vous visez, et ce que vous refusez de viser.

**Corrigé.**

1. **Erreur — la main-d'œuvre est additionnée** à des prix unitaires qui sont des **prix posés** : la
   main-d'œuvre y est déjà. Double compte de
   {{tranche-plancher.situation_exercice.double_compte_MAD::n0}} MAD. Le total à viser est
   **{{tranche-plancher.situation_exercice.total_juste_MAD::n0}} MAD**, et la ligne de main-d'œuvre
   redevient ce qu'elle aurait toujours dû être : un **contrôle**, pas un poste.

2. **Correct, et c'est le piège.** Le coffrage paraît surévalué : on attendrait
   {{tranche-plancher.situation_exercice.avancement_declare_pct::n0}} % de la surface de dalle, soit
   moins que les {{tranche-plancher.situation_exercice.postes.2.quantite::n0}} m² annoncés. Mais le
   rapport coffrage/surface de cette situation vaut
   **{{tranche-plancher.situation_exercice.ratio_coffrage_de_la_situation::n2}}**, exactement le ratio
   du métré : les joues de poutres sont comptées, et elles doivent l'être. **Rien à redire.** Savoir
   reconnaître ce qui est juste fait partie du contrôle : un visa qui refuse tout ne vaut pas mieux
   qu'un visa qui accepte tout, et il coûte la confiance de l'entreprise.

3. **Erreur — l'avancement n'est recoupé par rien.** {{tranche-plancher.situation_exercice.avancement_declare_pct::n0}} %
   est une **déclaration**, pas un relevé : les trois quantités du tableau en descendent toutes, donc
   aucune ne le contrôle. Le § S6 montre comment le recouper — en m³ et en m², poste par poste, sur
   les quantités **relevées**. **Ce qu'il faut exiger avant de viser : les attachements.**

*Ce qu'on vise : les trois postes de fournitures, à {{tranche-plancher.situation_exercice.total_juste_MAD::n0}} MAD,
sous réserve des attachements. Ce qu'on refuse : la ligne de main-d'œuvre, et le pourcentage tant
qu'il n'est pas adossé à un relevé. Et on le dit par écrit — un visa partiel non motivé se transforme
en litige trois mois plus tard.*
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
