---
id: RC1
titre: Dossier à corriger — revue critique du palier 1
fil: Palier 1 · module 10 — revue de palier (§ 5.5)
resume: Une note de fin de chantier soumise à votre visa. Elle contient sept erreurs, et elles ne sont pas inventées : ce sont celles que ce cours a réellement commises. Quatre lignes sont justes et ont l'air fausses.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · aucune erreur plantée ne porte sur une valeur normative
pied: Exemple pédagogique. Les sept erreurs de ce dossier sont documentées dans les rapports de relecture du dépôt (QA/) ; chacune a franchi une chaîne de contrôle verte avant d'être trouvée à la main.
donnees: revue, prix, planification, reception, qualite, suivi, gare
---

## S1 · Ce que cet exercice demande, et pourquoi il clôt le palier

Le § 5.5 du cadre impose, à la fin de chaque palier, un **dossier à corriger** : des documents
extraits du cas, contenant de cinq à huit erreurs, que le lecteur doit trouver. C'est l'entraînement
direct de la casquette qu'un chef de projet suivi porte tous les jours — **celle qui relit ce qu'on
lui soumet** — et c'est la seule compétence de ce cours qui ne s'acquiert pas en lisant.

Ce dossier-ci a une particularité :

{{revue.dossier._pourquoi_ces_sept_la}}

**Et ce que les relectures de ce palier ont réellement trouvé**, compté et non affirmé :

{{revue.dossier._ce_que_les_passes_ont_trouve}}

*La première version de ce module annonçait « 309 défauts dont 79 bloquants sur dix passes ». Les
trois nombres étaient faux. C'est le pire défaut qu'un module sur la relecture puisse commettre :
demander qu'on le croie sur parole au moment où il apprend à ne croire personne. Les chiffres
ci-dessus sont désormais comptés dans les rapports eux-mêmes, à chaque build.*

Chacune a donc deux vertus qu'une erreur inventée n'aurait pas. Elle est **réaliste**, puisqu'elle
a été commise par quelqu'un qui connaissait la règle et l'écrivait trois paragraphes plus loin. Et
elle est **invisible aux contrôles** : les dix passes ont toutes trouvé leurs défauts sur un dépôt
dont les seize contrôles automatiques étaient verts.

:::encart {"genre":"attente","titre":"Comment ce dossier est fabriqué, et pourquoi cela compte"}
{{revue.dossier._comment_ce_dossier_est_fabrique}}

Les erreurs sont donc **injectées par une fonction déclarée**, pas recopiées : si une donnée du
cours change, le dossier et son corrigé changent ensemble. Et un test exige que chaque erreur
**déplace réellement le nombre** — une « erreur » qui ne déplace rien n'est pas une erreur, c'est
une opinion, et le lecteur qui la cherche ne la trouvera jamais.
:::

## S2 · L'idée centrale : une erreur de relecture se cherche là où le calcul est juste

Les sept erreurs de ce dossier ont un point commun, et c'est lui qu'il faut avoir en tête avant de
commencer : **leur arithmétique est juste.** Aucune ne se trouve en refaisant une addition. Elles
se trouvent en posant une question sur une grandeur :

- **de quel calendrier** parle ce « par jour » ?
- **sous quelle condition** le prix que j'emprunte au voisin vaut-il ?
- **quelle est l'unité** de cette durée ?
- **quel domaine** borne cette fourchette ?
- **quel dénominateur** porte ce pourcentage ?
- **d'où vient** ce retard : d'une mesure ou d'une règle de trois ?
- **cet ouvrage décale-t-il quelque chose**, ou a-t-il de la marge ?

Sept questions, sept familles. Le dossier en contient une de chaque, et le corrigé le dit : un test
vérifie que les sept familles sont toutes différentes. Un relecteur qui pose ces sept questions sur
n'importe quelle note de chantier trouvera plus que celui qui recalcule tout.

## S3 · Le dossier soumis au visa

> **Note de synthèse — point d'avancement et prévision de fin**
> Gare voyageurs · situation à la date d'arrêt du module D4
> Émetteur : conduite de travaux · Destinataire : chef de projet suivi, pour visa

**Rappel des données du marché**, jointes à la note — sans elles, deux des lignes ne se vérifient
pas, et une note qui ne les rappelle pas est déjà critiquable :

| | |
|---|---|
| {{revue.dossier.contexte.0.libelle}} | {{revue.dossier.contexte.0.valeur}} |
| {{revue.dossier.contexte.1.libelle}} | {{revue.dossier.contexte.1.valeur}} |
| {{revue.dossier.contexte.2.libelle}} | {{revue.dossier.contexte.2.valeur}} |
| {{revue.dossier.contexte.3.libelle}} | {{revue.dossier.contexte.3.valeur}} |
| {{revue.dossier.contexte.4.libelle}} | **{{revue.dossier.contexte.4.valeur}}** |
| {{revue.dossier.contexte.5.libelle}} | {{revue.dossier.contexte.5.valeur}} |
| {{revue.dossier.contexte.6.libelle}} | {{revue.dossier.contexte.6.valeur}} |

Le document ci-dessous est celui qu'on vous soumet. **Lisez-le avant d'ouvrir le corrigé**, et
notez sur une feuille les numéros de ligne qui vous paraissent douteux — ainsi que la raison. Le
nombre de lignes douteuses n'est pas sept : {{revue.dossier.nb_justes}} des
{{revue.dossier.nb_lignes}} lignes sont justes, et certaines ont tout pour inquiéter.

| | Ligne | Valeur annoncée |
|---|---|---:|
| **{{revue.dossier.lignes.0.id}}** | {{revue.dossier.lignes.0.intitule}} | {{revue.dossier.lignes.0.affiche}} |
| **{{revue.dossier.lignes.1.id}}** | {{revue.dossier.lignes.1.intitule}} | {{revue.dossier.lignes.1.affiche}} |
| **{{revue.dossier.lignes.2.id}}** | {{revue.dossier.lignes.2.intitule}} | {{revue.dossier.lignes.2.affiche}} |
| **{{revue.dossier.lignes.3.id}}** | {{revue.dossier.lignes.3.intitule}} | {{revue.dossier.lignes.3.affiche}} |
| **{{revue.dossier.lignes.4.id}}** | {{revue.dossier.lignes.4.intitule}} | {{revue.dossier.lignes.4.affiche}} |
| **{{revue.dossier.lignes.5.id}}** | {{revue.dossier.lignes.5.intitule}} | {{revue.dossier.lignes.5.affiche}} |
| **{{revue.dossier.lignes.6.id}}** | {{revue.dossier.lignes.6.intitule}} | {{revue.dossier.lignes.6.affiche}} |
| **{{revue.dossier.lignes.7.id}}** | {{revue.dossier.lignes.7.intitule}} | {{revue.dossier.lignes.7.affiche}} |
| **{{revue.dossier.lignes.8.id}}** | {{revue.dossier.lignes.8.intitule}} | {{revue.dossier.lignes.8.affiche}} |
| **{{revue.dossier.lignes.9.id}}** | {{revue.dossier.lignes.9.intitule}} | {{revue.dossier.lignes.9.affiche}} |
| **{{revue.dossier.lignes.10.id}}** | {{revue.dossier.lignes.10.intitule}} | {{revue.dossier.lignes.10.affiche}} |

:::encart {"genre":"voir","titre":"Trois conseils de méthode, avant de chercher"}
**Ne recalculez pas.** L'arithmétique est juste partout. Chercher une faute de calcul vous fera
perdre une demi-heure et ne trouvera rien.

**Lisez les unités et les intitulés plus attentivement que les chiffres.** Six des sept erreurs sont
dans la façon dont la grandeur est nommée ou dans ce à quoi elle est comparée.

**Cherchez les lignes qui se contredisent entre elles.** Deux lignes du dossier annoncent le même
avancement par deux chemins différents, et ne tombent pas d'accord. C'est le signal le plus fiable
d'une note de chantier, et c'est ce qui a trouvé la moitié des défauts de ce cours.
:::

## S4 · Le corrigé

Ouvrez-le après avoir écrit votre liste, pas avant. Chaque erreur porte **sa famille**, **le
symptôme** qui la trahit, **comment la trouver**, **ce qu'elle coûte**, et **où ce cours l'a
commise**.

:::exercice {"titre":"E1 · Ligne L4 — la pénalité de retard","niveau":"revue_critique"}
**Famille : {{revue.dossier.erreurs.0.famille}}.**

**Le symptôme.** {{revue.dossier.erreurs.0.symptome}}

**Comment la trouver.** {{revue.dossier.erreurs.0.comment_la_trouver}}

**Ce qu'elle coûte.** {{revue.dossier.erreurs.0.ce_qu_elle_coute}}

**Où ce cours l'a commise.** {{revue.dossier.erreurs.0.ou_le_cours_l_a_commise}}

*La valeur juste est {{revue.dossier.lignes.3.juste::k}} MAD.*
:::

:::exercice {"titre":"E2 · Ligne L5 — le coût d'un décalage de réception","niveau":"revue_critique"}
**Famille : {{revue.dossier.erreurs.1.famille}}.**

**Le symptôme.** {{revue.dossier.erreurs.1.symptome}}

**Comment la trouver.** {{revue.dossier.erreurs.1.comment_la_trouver}}

**Ce qu'elle coûte.** {{revue.dossier.erreurs.1.ce_qu_elle_coute}}

**Où ce cours l'a commise.** {{revue.dossier.erreurs.1.ou_le_cours_l_a_commise}}

*La valeur juste est {{revue.dossier.lignes.4.juste::k}} MAD.*

C'est **l'erreur la plus instructive du dossier**, et la plus difficile à voir : elle ne porte sur
aucun calcul. Un chiffre juste, pris chez le voisin, employé hors de sa condition. Il n'existe
aucun test qui l'attrape — il faut relire le nom de la grandeur qu'on emprunte.
:::

:::exercice {"titre":"E3 · Ligne L3 — la durée du levage sous consignation","niveau":"revue_critique"}
**Famille : {{revue.dossier.erreurs.2.famille}}.**

**Le symptôme.** {{revue.dossier.erreurs.2.symptome}}

**Comment la trouver.** {{revue.dossier.erreurs.2.comment_la_trouver}}

**Ce qu'elle coûte.** {{revue.dossier.erreurs.2.ce_qu_elle_coute}}

**Où ce cours l'a commise.** {{revue.dossier.erreurs.2.ou_le_cours_l_a_commise}}

*La valeur juste est {{revue.dossier.lignes.2.juste::n1}} jours.*
:::

:::exercice {"titre":"E4 · Ligne L6 — l'alerte sur la part de main-d'œuvre","niveau":"revue_critique"}
**Famille : {{revue.dossier.erreurs.3.famille}}.**

**Le symptôme.** {{revue.dossier.erreurs.3.symptome}}

**Comment la trouver.** {{revue.dossier.erreurs.3.comment_la_trouver}}

**Ce qu'elle coûte.** {{revue.dossier.erreurs.3.ce_qu_elle_coute}}

**Où ce cours l'a commise.** {{revue.dossier.erreurs.3.ou_le_cours_l_a_commise}}

**Et le piège dans le piège.** {{revue.dossier.erreurs.3._le_piege_dans_le_piege}}

*C'est la seule des sept qui ne déplace aucun nombre. Le test du module ne l'exempte donc pas par
son nom — ce serait épingler un choix de l'auteur (D-041) — mais par sa **propriété** : une erreur
dont l'écart est nul est une erreur de lecture, et elle doit alors porter son explication propre.
La règle reste vraie si une autre erreur de lecture est ajoutée demain.*
:::

:::exercice {"titre":"E5 · Ligne L7 — le coût de la non-conformité","niveau":"revue_critique"}
**Famille : {{revue.dossier.erreurs.4.famille}}.**

**Le symptôme.** {{revue.dossier.erreurs.4.symptome}}

**Comment la trouver.** {{revue.dossier.erreurs.4.comment_la_trouver}}

**Ce qu'elle coûte.** {{revue.dossier.erreurs.4.ce_qu_elle_coute}}

**Où ce cours l'a commise.** {{revue.dossier.erreurs.4.ou_le_cours_l_a_commise}}

*La valeur juste est {{revue.dossier.lignes.6.juste::k}} MAD.*
:::

:::exercice {"titre":"E6 · Ligne L2 — l'avancement moyenné","niveau":"revue_critique"}
**Famille : {{revue.dossier.erreurs.5.famille}}.**

**Le symptôme.** {{revue.dossier.erreurs.5.symptome}}

**Comment la trouver.** {{revue.dossier.erreurs.5.comment_la_trouver}}

**Ce qu'elle coûte.** {{revue.dossier.erreurs.5.ce_qu_elle_coute}}

**Où ce cours l'a commise.** {{revue.dossier.erreurs.5.ou_le_cours_l_a_commise}}

*La valeur juste est {{revue.dossier.lignes.1.juste::n2}} %, et elle est déjà sur la ligne L1 du
même document. **Deux lignes du dossier se contredisent**, et c'est le signal le plus facile à
repérer de tous — à condition de lire le document en entier avant de viser.*
:::

:::exercice {"titre":"E7 · Ligne L8 — le retard déduit au lieu d'être mesuré","niveau":"revue_critique"}
**Famille : {{revue.dossier.erreurs.6.famille}}.**

**Le symptôme.** {{revue.dossier.erreurs.6.symptome}}

**Comment la trouver.** {{revue.dossier.erreurs.6.comment_la_trouver}}

**Ce qu'elle coûte.** {{revue.dossier.erreurs.6.ce_qu_elle_coute}}

**Où ce cours l'a commise.** {{revue.dossier.erreurs.6.ou_le_cours_l_a_commise}}

*La valeur juste est {{revue.dossier.lignes.7.juste::n0}} jours.*
:::

:::figure {"fn":"barres","args":"revue.dossier.figures.ecarts","titre":"De combien chaque erreur déplace son nombre, et dans quel sens","num":1,"large":true,"options":{"unite":"écart de la valeur affichée à la valeur juste, en %","legende_alerte":"erreur de lecture : le nombre est juste"},"voir":["{{revue.dossier.sens_des_ecarts.gonflent}} erreurs GONFLENT le nombre, {{revue.dossier.sens_des_ecarts.minorent}} le MINORENT, et {{revue.dossier.sens_des_ecarts.sans_ecart}} ne le déplace pas. Les deux sens sont dangereux, et le second l'est davantage : une provision surestimée se discute en réunion, une durée minorée se découvre sur le chantier.","Les écarts ne se comparent pas entre eux comme des gravités. E4 déplace le nombre de 0 % et n'est pas bénigne pour autant : elle fait classer sans suite une alerte qui, sur la bonne base, est réelle — c'est la dette n° 10 du dépôt.","Les deux plus gros écarts sont E2 et E5, et ce ne sont PAS la même faute : l'une applique un prix hors de la condition où il vaut, l'autre impute un coût à un ouvrage qui ne décale rien. Deux familles, un même ordre de grandeur — la hauteur ne dit pas la nature.","L'axe est linéaire et il flatte les surestimations : +687 % est un facteur 7,9, et −75 % un facteur 4. Une barre deux fois plus longue n'est pas une erreur deux fois plus grave, ni deux fois plus grande."],"erreur":"Trier les erreurs par la hauteur de leur barre pour décider lesquelles corriger. Cette figure mesure un écart, pas une gravité : celle qui coûte le plus cher sur ce chantier — E3, qui retire {{revue.dossier.lignes.2.juste::n1}} moins {{revue.dossier.lignes.2.valeur::n1}} plages de consignation à une tâche à marge nulle — n'est que la troisième en hauteur."}
:::

## S4g · Sécurité : ce qu'une erreur de relecture fait au chantier

Une note fausse ne reste pas sur le papier. Deux des sept erreurs de ce dossier ont une
conséquence directe sur la **sécurité des personnes**, et elles valent d'être nommées.

**E3, la durée du levage.** Le dossier annonce {{revue.dossier.lignes.2.affiche}} là où il en faut
{{revue.dossier.lignes.2.juste::n1}}. Visée telle quelle, cette note met au planning une opération
de levage sous caténaire consignée avec le quart du temps nécessaire. Ce qui se passe ensuite est
connu : on ne rallonge pas la plage de consignation — l'exploitant ne la donne pas — donc on
accélère **dedans**. On réduit les temps de consignation et de vérification d'absence de tension,
on lève avec moins de monde au sol, on empiète sur la marge de restitution. Les trois dispositions
que le module B7c décrit comme non négociables sont précisément celles qui sautent quand une plage
est trop courte.

**E7, le retard déduit au lieu d'être mesuré.** Même mécanisme, un cran plus loin : annoncer
{{revue.dossier.lignes.7.affiche}} de retard quand le réseau en donne
{{revue.dossier.lignes.7.juste::n0}} fait promettre une date intenable à l'exploitant. La promesse
se rattrape toujours au même endroit — la nuit, sur la voie.

**La règle qui en découle, et elle n'est pas sentimentale** : un visa n'est pas un acte
administratif. Viser une durée de levage, c'est décider des conditions dans lesquelles des gens
travailleront de nuit à côté d'une caténaire. Le relecteur qui laisse passer une erreur d'unité sur
une tâche de levage ne commet pas une erreur de gestion ; il déplace un risque sur quelqu'un
d'autre, et ce quelqu'un ne lira jamais la note.

### Et les lignes qu'il ne fallait PAS signaler

Savoir dire « rien à signaler » est la moitié du métier de contrôle, et c'est ce que l'Annexe 4 du
cadre exige de ses propres relecteurs : *un « RAS » sans preuve est refusé* — mais un faux positif
l'est tout autant. Un relecteur qui barre tout n'est pas sévère, il est inutilisable : il consomme
le temps que les vraies alertes n'auront plus.

:::exercice {"titre":"Les trois appâts — pourquoi ils ont l'air faux, et pourquoi ils sont justes","niveau":"revue_critique"}
**{{revue.dossier.appats.0.ligne}}.** {{revue.dossier.appats.0.pourquoi_on_doute}}
→ *{{revue.dossier.appats.0.verdict}}.*

**{{revue.dossier.appats.1.ligne}}.** {{revue.dossier.appats.1.pourquoi_on_doute}}
→ *{{revue.dossier.appats.1.verdict}}.*

**{{revue.dossier.appats.2.ligne}}.** {{revue.dossier.appats.2.pourquoi_on_doute}}
→ *{{revue.dossier.appats.2.verdict}}.*

**Ce que les trois ont en commun** : un chiffre surprenant n'est pas un chiffre faux. Chacun des
trois est publié par un module qui explique lui-même pourquoi il surprend. Le réflexe à prendre
n'est donc pas « ce nombre me paraît bizarre, je le barre » mais « ce nombre me paraît bizarre, de
quel document vient-il et que dit ce document ? ».
:::

## S5 · Ce que le palier 1 a appris sur le contrôle

Le tableau ci-dessous n'est pas une liste d'erreurs : c'est **la méthode qui les a trouvées**. Dix
passes de relecture hostile, {{revue.dossier.nb_erreurs}} familles, et un constat qui ne varie pas.

| Ce qui N'A PAS trouvé les erreurs | Ce qui les a trouvées |
|---|---|
| Les seize contrôles de la chaîne — verts à chaque passe, à chaque fois | **Recalculer trois valeurs à partir des données seules**, sans lire le raisonnement de l'auteur |
| Les tests du module — ils vérifient que le code fait ce qu'il dit, pas que ce qu'il dit soit juste | **Rapprocher deux nombres publiés par le même document** à deux sections d'écart |
| La vérification dimensionnelle — elle a trouvé une année de 365,25 jours, et aucun des sept défauts de ce dossier | **Ouvrir les captures et les regarder** : la plupart des passes y ont trouvé un défaut |
| La relecture par l'auteur — elle lit ce qu'il a voulu écrire | **Relire le nom de la grandeur empruntée au module voisin** |

:::encart {"genre":"piege","titre":"Le constat le plus inconfortable du palier"}
**La quasi-totalité des défauts bloquants de ce palier a été trouvée par une relecture humaine,
hostile, qui recalculait** — et non par les seize contrôles de la chaîne, verts à chaque fois. Il y
a deux exceptions, et elles sont instructives : **deux canaris ont trouvé seuls une erreur que la
passe n'avait pas vue**, et la vérification dimensionnelle a trouvé une année comptée à 365,25
jours. Les trois ont un point commun : ce sont des contrôles **écrits pour chercher**, pas pour
confirmer. Un canari qui se contente de vérifier que le résultat attendu sort ne trouve rien ;
celui qui rejoue le calcul avec l'erreur et exige que le nombre publié change, oui.

Les contrôles ne sont donc pas inutiles — ils empêchent les défauts déjà rencontrés de revenir, et
c'est beaucoup. Mais ils ne trouvent que ce qu'on leur a appris à chercher.

La conséquence pratique, pour un chef de projet suivi : **le temps de relecture ne se remplace pas
par un tableau de bord.** Un indicateur vert dit qu'aucune des alarmes prévues ne s'est déclenchée.
Il ne dit pas que la note est juste.
:::

## S6 · Pour aller plus loin : construisez le vôtre

:::exercice {"titre":"Exercice de fin de palier — planter vos propres erreurs","niveau":"cas_ouvert"}
Reprenez une note de chantier réelle de votre projet — une situation, un point d'avancement, une
demande de prolongation de délai — et appliquez-lui les sept questions du § S2, une par une.

**1. De quel calendrier parle chaque « par jour » ?** Comptez combien de grandeurs de la note sont
en jours ouvrés et combien en jours calendaires. Si la note ne le dit nulle part, vous avez déjà
trouvé quelque chose.

**2. Quelle grandeur vient d'un autre document ?** Pour chacune, allez lire son NOM dans le
document d'origine, et la condition sous laquelle elle vaut.

**3. Quelle unité porte chaque durée ?** Une durée en plages de consignation, en jours ouvrés, en
jours calendaires et en mois ne se comparent pas, et elles se ressemblent toutes à l'écran.

**4. Quelle fourchette borne quoi ?** Pour chaque contrôle d'ordre de grandeur, vérifiez que le
numérateur et le dénominateur de votre ratio sont ceux de la fourchette.

**5. Quel dénominateur porte chaque pourcentage ?** Et s'il y a une moyenne de pourcentages
quelque part, c'est presque toujours une erreur.

**6. Chaque retard est-il mesuré ou déduit ?** Un retard égal à la durée de l'incident est
suspect : il suppose que rien ne l'absorbe et que rien ne l'amplifie.

**7. Quels ouvrages ont de la marge ?** Un coût de retard imputé à un ouvrage qui ne décale pas la
fin du chantier est un coût inventé.

*Il n'y a pas de corrigé à cet exercice : c'est votre note, votre projet, et c'est exactement ce
que la casquette de contrôle demande. Si vous ne trouvez rien, la note est peut-être bonne — ou
vous l'avez lue comme son auteur l'a écrite.*
:::

## S7 · Check-list de relecture, et bilan du palier

**Check-list : relire une note de chantier en dix minutes**

1. Les **calendriers** sont-ils nommés partout où il y a un « par jour » ?
2. Chaque grandeur **empruntée** porte-t-elle sa condition d'emploi ?
3. Chaque **durée** porte-t-elle son unité, et est-ce la même partout ?
4. Chaque **ratio** porte-t-il son domaine, et la fourchette borne-t-elle la même chose ?
5. Chaque **pourcentage** a-t-il un dénominateur, et est-ce le bon ?
6. Chaque **retard** est-il mesuré sur le réseau, ou déduit ?
7. Chaque **coût de retard** est-il imputé à un ouvrage qui décale vraiment la fin ?
8. Deux lignes du document **se contredisent-elles** ?
9. Les **figures** disent-elles la même chose que les tableaux qu'elles accompagnent ?
10. Y a-t-il une ligne que je trouve bizarre et qui est simplement **juste** ?

:::memo
## Fiche mémo — les sept questions de la relecture

**La règle du palier**

> L'arithmétique d'une note est presque toujours juste. Ce qui est faux, c'est le domaine
> d'emploi d'un nombre juste.

**Les sept questions, dans l'ordre où elles paient**

| # | Question | Famille |
|---:|---|---|
| 1 | De quel **calendrier** parle ce « par jour » ? | {{revue.dossier.erreurs.0.famille}} |
| 2 | Sous quelle **condition** ce prix emprunté vaut-il ? | {{revue.dossier.erreurs.1.famille}} |
| 3 | Quelle est l'**unité** de cette durée ? | {{revue.dossier.erreurs.2.famille}} |
| 4 | Quel **domaine** borne cette fourchette ? | {{revue.dossier.erreurs.3.famille}} |
| 5 | Quel **dénominateur** porte ce pourcentage ? | {{revue.dossier.erreurs.5.famille}} |
| 6 | Ce retard est-il **mesuré** ou déduit ? | {{revue.dossier.erreurs.6.famille}} |
| 7 | Cet ouvrage a-t-il de la **marge** ? | {{revue.dossier.erreurs.4.famille}} |

**Les trois signaux les plus fiables**

1. **Deux lignes du même document qui ne tombent pas d'accord.** C'est ce qui a trouvé la moitié
   des défauts de ce cours.
2. **Un nombre trop rond, ou trop précis.** Les deux trahissent : l'un une estimation déguisée,
   l'autre une hypothèse prise pour une mesure.
3. **Une alerte spectaculaire.** Avant de la relayer, vérifier que la fourchette borne bien la
   même grandeur que le ratio.

**Et le réflexe inverse, aussi important**

Un chiffre surprenant n'est pas un chiffre faux. {{revue.dossier.nb_justes}} des
{{revue.dossier.nb_lignes}} lignes de ce dossier sont justes, et trois d'entre elles sont
déconcertantes. **Savoir dire RAS, avec sa preuve, est la moitié du métier.**
:::
