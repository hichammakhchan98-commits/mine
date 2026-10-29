---
id: D7
titre: Pilotage et suivi multi-sites — ce qu'une agrégation vous cache
fil: Palier 1 · module 12 — direction de projet
resume: Un tableau de bord consolidé est le dernier endroit où une dérive apparaît. Chaque étage d'agrégation divise la dérive d'un site par son poids, et un site à 13 % du coût doit dériver huit fois plus que le seuil pour le franchir. Ce module chiffre ce que l'agrégation perd, et dit quel signal la remplace.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · deux sites · aucune obligation contractuelle de reporting, aucun seuil de réclamation n'est chiffré
pied: Exemple pédagogique — ne remplace ni les obligations de reporting d'un marché, ni une procédure de direction de projet. Les seuils, les destinataires et les délais de déclaration se lisent dans le CPS.
donnees: pilotage, gare, suivi, planification
---

## S1 · Ce que ce module fait, et ce qu'il ne peut pas faire

Vous pilotez deux chantiers. Le lundi matin, vous recevez deux situations, et quelqu'un au-dessus de
vous attend un chiffre. Ce chiffre sera une **agrégation** — et une agrégation, par construction,
perd de l'information. La seule question utile est : **laquelle**, et combien ça coûte de l'avoir
perdue.

Ce module traite donc cinq choses **qui se calculent sans aucune norme** :

1. **un ratio ne se consolide pas.** Le CPI d'une opération est le rapport des sommes, pas la
   moyenne des CPI : sur ce chantier, {{pilotage.consolidation.CPI_consolide::n3}} contre
   {{pilotage.consolidation.moyenne_des_CPI::n3}}, soit
   {{pilotage.consolidation.ecart_entre_les_deux_pts::n1}} points — et dans le sens qui rassure
   (§ S3b) ;
2. **l'agrégation amortit.** Le site secondaire pèse
   {{pilotage.consolidation.poids.1.poids_du_cout_pct::n1}} % du coût réel : sa dérive arrive dans
   l'indicateur consolidé divisée par {{pilotage.consolidation.poids.1.amortissement::n1}}. Il peut
   perdre {{pilotage.seuil_de_masquage.derive_supplementaire_invisible_MAD::k}} MAD de plus sans
   faire bouger le tableau de bord d'un cran (§ S3b) ;
3. **le masquage est récursif.** Ce que le consolidé fait au site, le site le fait à ses lots : un
   lot à CPI {{pilotage.masquage_recursif.CPI_du_lot::n3}} dans un site à
   {{pilotage.masquage_recursif.CPI_du_site::n3}}, et il porte
   {{pilotage.masquage_recursif.part_de_la_derive_du_site_pct::n0}} % de la dérive (§ S3b) ;
4. **la latence du reporting se paie.** {{pilotage.latence.lignes.0.latence_moyenne_j::n1}} jours en
   hebdomadaire contre {{pilotage.latence.lignes.1.latence_moyenne_j::n1}} en mensuel, soit
   {{pilotage.latence.cout_de_l_ecart_MAD::k}} MAD de frais de durée à chaque dérive (§ S3a) ;
5. **sur un chantier ferroviaire, le bon seuil d'alerte n'est pas un pourcentage, c'est une durée** :
   {{pilotage.alerte_ferroviaire.periode_entre_fenetres_j}} jours, la période entre deux fenêtres de
   consignation. En deçà un retard se rattrape ; au-delà il coûte un cycle entier, et aucun
   indicateur de coût ne le voit venir (§ S3c).

Ce qu'il ne fait pas : dire ce que votre marché vous oblige à déclarer, à qui, sous quel délai ; ni
quel seuil ouvre une réclamation ; ni quelle forme doit prendre un rapport contractuel. Tout cela est
**contractuel**, se lit dans le CPS, et reste **⏸**. Ce module donne les mécanismes de l'agrégation
et les signaux qui la contournent ; le marché donne les obligations.

**D'où viennent les chiffres.** Le site principal n'est pas recalculé ici : son budget, sa valeur
acquise et son coût réel sont ceux que le module **D4** publie à la même date d'arrêt — jour
{{pilotage.date_d_arret_j::n0}}, soit le 4ᵉ mois (D-039). Le site secondaire est déclaré **lot par
lot**, parce qu'aucun module ne le produit : un chef de projet reçoit des lots, jamais un CPI, et la
valeur acquise s'en **dérive** au lieu d'être posée.

:::encart {"genre":"attente","titre":"La première décision d'un pilotage multi-sites, et elle n'est pas technique"}
{{gare.multi_sites.date_d_arret_commune}}

Ce module suppose cette décision prise. Si elle ne l'est pas — et elle ne l'est presque jamais au
démarrage — alors aucun des calculs qui suivent ne veut dire quoi que ce soit, et c'est le premier
chantier du chef de projet suivi : obtenir deux situations arrêtées le même jour, avant d'obtenir
deux situations justes.
:::

## S2 · L'idée centrale : une agrégation divise par le poids

Prenez deux sites. Le premier a dépensé {{pilotage.sites.0.cout_reel_CR_MAD::k}} MAD, le second
{{pilotage.sites.1.cout_reel_CR_MAD::k}}. Le second dérape : son CPI tombe à
{{pilotage.sites.1.CPI::n3}} quand le premier tient {{pilotage.sites.0.CPI::n3}}.

Que montre l'indicateur consolidé ? **{{pilotage.consolidation.CPI_consolide::n3}}** — à peine
plus bas que celui du grand site. Ce n'est pas un défaut du calcul : c'est sa définition. Le CPI
consolidé est

$$ \text{CPI}_{\text{cons}} = \frac{\sum \text{VA}_i}{\sum \text{CR}_i} $$

c'est-à-dire une moyenne des CPI **pondérée par les coûts réels**. Un site qui pèse
{{pilotage.consolidation.poids.1.poids_du_cout_pct::n1}} % du coût contribue pour
{{pilotage.consolidation.poids.1.poids_du_cout_pct::n1}} % à l'indicateur : sa dérive y arrive
**divisée par {{pilotage.consolidation.poids.1.amortissement::n1}}**.

C'est la loi, et elle n'a rien de particulier à ce chantier :

> **Un indicateur consolidé divise la dérive d'un site par le poids de ce site.**

**Attention à ce que la loi ne dit pas.** Elle ne dit pas que l'erreur va toujours dans le sens qui
rassure : elle dit que le consolidé est tiré vers le site qui a le plus **dépensé**.

{{pilotage.consolidation._dans_quel_sens_va_l_ecart}}

En monnaie, l'amortissement donne un nombre qu'on peut afficher au mur —
**{{pilotage.consolidation.MAD_pour_un_centieme_de_CPI::k}} MAD** de dérive pour faire bouger le CPI
consolidé d'**un centième** — à condition de dire de quelle dérive on parle :

{{pilotage.consolidation._le_centieme_depend_du_mecanisme}}

:::figure {"fn":"barres","args":"pilotage.figures.cpi_par_site","titre":"Quatre nombres pour deux sites, et deux d'entre eux ne veulent rien dire","num":1,"large":true,"options":{"unite":"CPI — valeur acquise / coût réel","origine":0.7,"legende_alerte":{"$":"pilotage.figures.legende_seuil_alerte"}},"voir":["Les deux premières barres sont les CPI réels des deux sites : {{pilotage.sites.0.CPI::n3}} et {{pilotage.sites.1.CPI::n3}}.","La troisième est le CPI consolidé, {{pilotage.consolidation.CPI_consolide::n3}} : il est presque collé à celui du grand site, parce qu'il en est une moyenne pondérée par les coûts.","La quatrième est la moyenne arithmétique des deux CPI, {{pilotage.consolidation.moyenne_des_CPI::n3}} : elle donne le même poids à un site de {{pilotage.sites.0.cout_reel_CR_MAD::k}} MAD et à un site de {{pilotage.sites.1.cout_reel_CR_MAD::k}} MAD, et c'est pourtant celle qu'on calcule de tête.","Elle est rouge, et le consolidé ne l'est pas : sur ce chantier, le calcul faux aurait déclenché une alerte que le calcul juste ne déclenche pas. L'erreur ne va donc pas toujours dans le sens qui rassure — elle va dans le sens du site le plus lourd, et ici ce site va mieux que l'autre.","L'écart entre les deux dernières barres, {{pilotage.consolidation.ecart_entre_les_deux_pts::n1}} points, est l'erreur qu'on commet en moyennant des rapports."],"erreur":"Lire le CPI consolidé comme l'état de l'opération. Il est collé au CPI du site qui a le plus dépensé — ici {{pilotage.sites.0.CPI::n3}} contre {{pilotage.consolidation.CPI_consolide::n3}}, deux centièmes d'écart — et il ignore l'autre. Il dit où en est la MASSE d'argent ; il ne décrit aucun des deux chantiers."}
:::

**Pourquoi cela compte plus qu'il n'y paraît.** Un indicateur qui amortit n'est pas seulement
imprécis : il est **asymétrique dans le temps**. Une dérive qui commence petite sur un petit site
reste invisible longtemps ; quand elle devient visible au consolidé, elle a déjà atteint une taille
qui ne se rattrape plus. L'agrégation ne retarde pas un peu la détection, elle la retarde d'autant
plus que le site est petit — et un petit site est précisément celui où l'on a mis le moins
d'encadrement.

## S3 · Principes

### a. Le rythme du reporting, et ce que la latence coûte

Entre le moment où une dérive commence et celui où quelqu'un peut la lire, il y a deux délais, et on
n'en discute jamais qu'un seul.

Le premier est la **période de reporting** : une dérive qui démarre au hasard dans la période est
lisible, en moyenne, une demi-période plus tard. Le second est le **délai de remontée** —
⟦V3|délai entre la fin d'une période de reporting et la disponibilité des données consolidées|4 j|j ouvrés|2 à 10|2026|relevés d'attachement, saisie, vérification, consolidation. C'est le délai dont personne ne parle quand on discute du rythme des réunions⟧ —
entre la fin de la période et le moment où les données sont consolidées et vérifiées.

| Rythme | Période | Remontée | **Latence moyenne** | Pire cas | Coût de la latence |
|---|---:|---:|---:|---:|---:|
| {{pilotage.latence.lignes.0.rythme}} | {{pilotage.latence.lignes.0.periode_j::n0}} j | {{pilotage.latence.lignes.0.delai_de_remontee_j::n0}} j | **{{pilotage.latence.lignes.0.latence_moyenne_j::n1}} j** | {{pilotage.latence.lignes.0.latence_pire_cas_j::n1}} j | {{pilotage.latence.lignes.0.cout_de_la_latence_moyenne_MAD::k}} MAD |
| {{pilotage.latence.lignes.1.rythme}} | {{pilotage.latence.lignes.1.periode_j::n0}} j | {{pilotage.latence.lignes.1.delai_de_remontee_j::n0}} j | **{{pilotage.latence.lignes.1.latence_moyenne_j::n1}} j** | {{pilotage.latence.lignes.1.latence_pire_cas_j::n1}} j | {{pilotage.latence.lignes.1.cout_de_la_latence_moyenne_MAD::k}} MAD |

{{pilotage.latence.lecture}}

:::encart {"genre":"piege","titre":"Le délai de remontée ne s'achète pas avec une réunion de plus"}
{{pilotage.latence._le_delai_de_remontee_est_la_moitie_du_sujet}}
:::

{{pilotage.latence._ce_que_la_latence_n_est_pas}}

:::figure {"fn":"barres","args":"pilotage.figures.latence","titre":"Combien de temps une dérive vit avant d'être lisible","num":2,"options":{"unite":"jours ouvrés, latence moyenne (demi-période + remontée)"},"voir":["Chaque barre est une latence TOTALE : une demi-période de reporting plus le délai de remontée. La figure ne montre pas les deux termes séparément — le tableau ci-dessus les donne, et c'est là qu'il faut les lire.","Passer du mensuel à l'hebdomadaire gagne {{pilotage.latence.ecart_des_deux_rythmes_j::n0}} jours en moyenne — pas trois semaines.","Le délai de remontée pèse {{pilotage.latence.part_du_delai_de_remontee_dans_l_hebdo_pct::n0}} % de la latence hebdomadaire. En dessous de ce délai, changer de rythme ne sert plus à rien.","Ces jours ne sont pas du retard : ce sont des jours pendant lesquels personne ne peut décider."],"erreur":"Croire qu'un rapport hebdomadaire divise la latence par quatre. Il divise la PÉRIODE par quatre ; la latence, elle, contient un terme que le rythme ne touche pas, et ce terme ne se réduit qu'en saisissant les attachements le jour même."}
:::

**Ce que le chef de projet décide seul, et ce qu'il remonte.** La latence donne la règle, et elle est
désagréable : tout ce qui se décide **dans** la latence doit se décider sans le tableau de bord.
Autrement dit, les décisions que le reporting rend possibles sont celles dont l'horizon dépasse
{{pilotage.latence.lignes.1.latence_moyenne_j::n0}} jours. Les autres — réaffecter une équipe,
décaler une livraison, lancer une reprise — se prennent sur le terrain, et le reporting ne fait que
les **constater**. Un chef de projet suivi qui attend son tableau de bord pour décider d'un sujet de
trois jours ne pilote pas : il commente.

### b. Le tableau de bord consolidé, et ce qu'il masque

**Deux sites, à la même date d'arrêt.** Le site secondaire est déclaré pour ce module :
⟦V3|budget des ouvrages d'une gare de RER de 810 m² d'emprise, hors frais de durée|9 500 000 MAD|MAD|6 500 000 à 14 000 000|2026|même périmètre que celui que D4 publie pour le site principal — environ 11 700 MAD/m² contre 12 150 pour la gare à grande vitesse⟧
de budget d'ouvrages, et ses lots sont déclarés un à un dans `data/`. Sa première consignation est
attendue au ⟦V3|jour ouvré où le site secondaire a besoin de sa première interception, dans le calendrier commun de l'opération|jour 190|jour ouvré|160 à 230|2026|raccordement des quais à la voie existante. Déclaré parce qu'aucun planning de ce site n'est modélisé dans ce cours⟧,
et il accuse ⟦V3|retard calendaire constaté sur le lot de fondations du site secondaire à la date d'arrêt|22 j|j ouvrés|12 à 35|2026|tel que le site le remonte. Il est DÉCLARÉ et non déduit du SPI : un SPI est un rapport de budgets, il ne donne pas des jours⟧
de retard sur son lot de fondations.


| | Site principal | Site secondaire | **Opération** |
|---|---:|---:|---:|
| Budget des ouvrages (BAC) | {{pilotage.sites.0.budget_a_l_achevement_BAC_MAD::k}} MAD | {{pilotage.sites.1.budget_a_l_achevement_BAC_MAD::k}} MAD | {{pilotage.consolidation.budget_a_l_achevement_BAC_MAD::k}} MAD |
| Valeur acquise (VA) | {{pilotage.sites.0.valeur_acquise_VA_MAD::k}} | {{pilotage.sites.1.valeur_acquise_VA_MAD::k}} | {{pilotage.consolidation.valeur_acquise_VA_MAD::k}} |
| Coût réel (CR) | {{pilotage.sites.0.cout_reel_CR_MAD::k}} | {{pilotage.sites.1.cout_reel_CR_MAD::k}} | {{pilotage.consolidation.cout_reel_CR_MAD::k}} |
| **CPI** | {{pilotage.sites.0.CPI::n3}} | **{{pilotage.sites.1.CPI::n3}}** | {{pilotage.consolidation.CPI_consolide::n3}} |
| **SPI** | {{pilotage.sites.0.SPI::n3}} | {{pilotage.sites.1.SPI::n3}} | {{pilotage.consolidation.SPI_consolide::n3}} |
| Dérive à la date d'arrêt | {{pilotage.sites.0.derive_MAD::k}} | {{pilotage.sites.1.derive_MAD::k}} | {{pilotage.consolidation.derive_totale_MAD::k}} |
| Poids dans le coût réel | {{pilotage.consolidation.poids.0.poids_du_cout_pct::n1}} % | {{pilotage.consolidation.poids.1.poids_du_cout_pct::n1}} % | 100 % |

{{pilotage.consolidation._un_ratio_ne_se_consolide_pas}}

**Jusqu'où le petit site peut-il tomber sans qu'on le voie ?** La question se pose exactement, et
elle se résout en une ligne :

{{pilotage.seuil_de_masquage.lecture}}

**Et ce nombre dépend du mécanisme de la dérive**, ce qui double presque la réponse :

{{pilotage.seuil_de_masquage._les_deux_mecanismes}}

:::encart {"genre":"alerte","titre":"La loi d'amortissement, et pourquoi un seuil unique n'existe pas"}
{{pilotage.seuil_de_masquage._la_loi}}
:::

**Et un étage plus bas, la même chose recommence.**

{{pilotage.masquage_recursif.lecture}}

:::figure {"fn":"barres","args":"pilotage.figures.lots_du_site_secondaire","titre":"Les lots démarrés du site secondaire, par leur dérive","num":3,"large":true,"options":{"unite":"k MAD de dérive (coût réel − valeur acquise)","legende_alerte":{"$":"pilotage.figures.legende_seuil_alerte"}},"voir":["Un seul lot porte {{pilotage.masquage_recursif.part_de_la_derive_du_site_pct::n0}} % de la dérive du site : les terrassements et fondations spéciales.","Son CPI vaut {{pilotage.masquage_recursif.CPI_du_lot::n3}} ; celui du site, {{pilotage.masquage_recursif.CPI_du_site::n3}}. Le site amortit déjà son propre lot d'un facteur {{pilotage.masquage_recursif.amortissement_du_lot_par_le_site::n1}}.","La barre rouge utilise le seuil de l'OPÉRATION appliqué tel quel à un lot : c'est précisément ce que le § S3b déconseille, et la figure le montre pour qu'on le voie. Un lot n'a pas le même seuil qu'une opération, et inventer ici un troisième seuil n'aurait été décidé par personne.","Le lot « Structure » est à {{pilotage.sites.1.lots.2.CPI::n3}} et sa dérive est onze fois plus petite : il démarre à peine, et son CPI est encore du bruit au sens de la courbe de fiabilité.","Le lot en cause est celui qu'un sol difficile était censé rendre risqué : le risque avait été identifié, et c'est l'indicateur qui ne l'a pas suivi."],"erreur":"Demander au site « pourquoi ton CPI baisse ? » au lieu de regarder ses lots. La réponse est toujours la même — un lot, parfois deux — et la question fait perdre une semaine à celui qui la reçoit."}
:::

{{pilotage.masquage_recursif._les_amortissements_se_multiplient}}

**Alors que faut-il consolider ?** Des montants.

{{pilotage.consolidation._ce_qui_se_consolide_vraiment}}

:::figure {"fn":"barres","args":"pilotage.figures.derive_par_site","titre":"La même information en monnaie : la dérive par site","num":4,"options":{"unite":"k MAD de dérive à la date d'arrêt","legende_alerte":{"$":"pilotage.figures.legende_seuil_alerte"}},"voir":["Les dérives s'ADDITIONNENT : {{pilotage.consolidation.derive_totale_MAD::k}} MAD au total. Les CPI, non.","Le site principal porte la plus grosse dérive en valeur absolue, parce qu'il est {{pilotage.consolidation.rapport_des_tailles_en_budget::n1}} fois plus gros en budget et {{pilotage.consolidation.rapport_des_tailles_en_cout_reel::n1}} fois en dépense. Cela ne dit pas qu'il va plus mal.","Rapporté à son budget, c'est l'inverse : le site secondaire pèse {{pilotage.consolidation.poids.1.poids_du_budget_pct::n1}} % du budget et {{pilotage.consolidation.poids.1.part_du_depassement_prevu_pct::n1}} % du dépassement prévu à terminaison.","Deux lectures, deux décisions : la première dit où est l'argent, la seconde dit où aller."],"erreur":"Choisir entre les deux lectures. Il en faut deux : le montant dit ce que l'opération va coûter, le rapport dit quel site le cause. Un tableau de bord qui n'en porte qu'une produit soit de la panique sur le petit site, soit de l'aveuglement sur lui."}
:::

**La fiabilité de ce qu'on lit.** Un CPI calculé tôt n'est pas un CPI : c'est du bruit. Le module D4
publie la courbe — à {{suivi.fiabilite_du_cpi.points.0.avancement_pct::n1}} % d'avancement,
l'incertitude du CPI vaut {{suivi.fiabilite_du_cpi.points.0.incertitude_pts::n1}} points ; il faut
attendre {{suivi.fiabilite_du_cpi.points.4.avancement_pct::n1}} % pour qu'elle tombe à
{{suivi.fiabilite_du_cpi.points.4.incertitude_pts::n1}}. Cette courbe est celle du site **principal**, et c'est une limite qu'il faut dire : sur un site
{{pilotage.consolidation.rapport_des_tailles_en_budget::n1}} fois plus petit, les mêmes pour cent
d'avancement portent beaucoup moins d'ouvrages, donc l'incertitude est **plus** grande au même
pourcentage — la courbe du grand site en donne une borne optimiste, pas une mesure. En multi-sites,
la conséquence est la même mais plus forte : **un site qui démarre n'a pas de CPI lisible**, et le
consolider avec un site avancé mêle une mesure et une rumeur. Le site secondaire est ici à
{{pilotage.sites.1.avancement_physique_pct::n1}} % d'avancement physique : c'est tout juste
suffisant, et c'est à dire dans le rapport.

### c. Interfaces, et le signal qui arrive à temps

Les deux sections précédentes mesurent la dérive avec des **indicateurs de coût**. Sur un chantier
ferroviaire, ils ont un angle mort, et il est large.

**Un cycle perdu ne produit ni valeur acquise ni dépense d'ouvrage — et il coûte pourtant.** Quand
un retard fait manquer une fenêtre de consignation, le travail n'est pas fait, donc il n'est pas
payé : dans le périmètre où ce cours calcule le CPI — les ouvrages seuls, frais de durée exclus,
comme D4 les publie — l'indicateur ne bouge pas d'un millième. L'opération, elle, paie les
{{pilotage.alerte_ferroviaire.periode_entre_fenetres_j}} jours d'attente au tarif des frais de
durée : **{{pilotage.alerte_ferroviaire.cout_d_un_cycle_perdu_en_frais_de_duree_MAD::k}} MAD**, soit
{{pilotage.consolidation.MAD_pour_un_centieme_de_CPI::k}} MAD de plus qu'il n'en faudrait pour
déplacer le CPI consolidé d'un centième — si seulement cette dépense était dans son périmètre.

C'est le pire des deux mondes : **une dépense réelle qu'aucun indicateur de performance ne montre,
parce qu'elle est hors de son périmètre par construction.** Le SPI finit par bouger, avec la latence
du § S3a et l'amortissement du § S3b. L'information arrive quand elle ne sert plus.

Or le module B7c l'a établi : **sous consignation, un retard ne grandit pas, il saute**.

{{pilotage.alerte_ferroviaire.lecture}}

:::figure {"fn":"diagramme","args":"pilotage.figures.retard_quantise","titre":"Sous consignation, le retard est un escalier","num":5,"large":true,"options":{"unite":"j","axeX":true,"axeY":true,"uniteX":"retard constaté sur le site, j ouvrés","nom":"retard effectif","depuisZero":true,"marqueur":{"$":"pilotage.figures.marqueur_retard"}},"voir":["L'axe horizontal est le retard constaté sur le site ; l'axe vertical, le retard réellement subi sur la première interception.","La courbe est un escalier de marches de {{pilotage.alerte_ferroviaire.periode_entre_fenetres_j}} jours : la période entre deux fenêtres. Entre deux marches, un jour de retard de plus ne coûte rien.","Le marqueur est le retard constaté : {{pilotage.alerte_ferroviaire.retard_constate_du_site_j}} jours, qui coûtent {{pilotage.alerte_ferroviaire.retard_effectif_j}} jours — une amplification de {{pilotage.alerte_ferroviaire.amplification::n2}}.","Juste avant une marche, un jour gagné en vaut {{pilotage.alerte_ferroviaire.periode_entre_fenetres_j}}. Juste après, il n'en vaut aucun. C'est tout l'art du pilotage d'un chantier sous interception."],"erreur":"Piloter ce retard comme un retard de bâtiment, en négociant des moyens pour « rattraper trois semaines ». Il n'y a rien à rattraper entre deux marches, et tout à rattraper juste avant la suivante — le seul calendrier qui compte est celui des fenêtres."}
:::

{{pilotage.alerte_ferroviaire._le_seuil_est_une_duree_pas_un_ratio}}

{{pilotage.alerte_ferroviaire._pourquoi_le_CPI_ne_sert_a_rien_ici}}

**Le registre des interfaces, rangé autrement.** Le module B7c publie les interfaces de l'opération
et leur délai de demande. Un chef de projet suivi n'a pas besoin de la liste : il a besoin de la
**soustraction**. Pour chaque interface et chaque site, la date limite de dépôt est la date de besoin
moins le délai — et la marge à la date d'arrêt se lit d'un coup d'œil.

| Site | Objet | Délai | Besoin | **Date limite** | Marge | Statut |
|---|---|---:|---:|---:|---:|---|
| {{pilotage.interfaces.lignes.0.site}} | {{pilotage.interfaces.lignes.0.objet}} | {{pilotage.interfaces.lignes.0.delai_calendaire_j}} j | j {{pilotage.interfaces.lignes.0.date_de_besoin_j::n0}} | j {{pilotage.interfaces.lignes.0.date_limite_de_demande_j::n0}} | **{{pilotage.interfaces.lignes.0.marge_a_la_date_d_arret_j::n0}} j** | {{pilotage.interfaces.lignes.0.statut}} |
| {{pilotage.interfaces.lignes.1.site}} | {{pilotage.interfaces.lignes.1.objet}} | {{pilotage.interfaces.lignes.1.delai_calendaire_j}} j | j {{pilotage.interfaces.lignes.1.date_de_besoin_j::n0}} | j {{pilotage.interfaces.lignes.1.date_limite_de_demande_j::n0}} | {{pilotage.interfaces.lignes.1.marge_a_la_date_d_arret_j::n0}} j | {{pilotage.interfaces.lignes.1.statut}} |
| {{pilotage.interfaces.lignes.2.site}} | {{pilotage.interfaces.lignes.2.objet}} | {{pilotage.interfaces.lignes.2.delai_calendaire_j}} j | j {{pilotage.interfaces.lignes.2.date_de_besoin_j::n0}} | j {{pilotage.interfaces.lignes.2.date_limite_de_demande_j::n0}} | {{pilotage.interfaces.lignes.2.marge_a_la_date_d_arret_j::n0}} j | {{pilotage.interfaces.lignes.2.statut}} |
| {{pilotage.interfaces.lignes.3.site}} | {{pilotage.interfaces.lignes.3.objet}} | {{pilotage.interfaces.lignes.3.delai_calendaire_j}} j | j {{pilotage.interfaces.lignes.3.date_de_besoin_j::n0}} | j {{pilotage.interfaces.lignes.3.date_limite_de_demande_j::n0}} | {{pilotage.interfaces.lignes.3.marge_a_la_date_d_arret_j::n0}} j | {{pilotage.interfaces.lignes.3.statut}} |
| {{pilotage.interfaces.lignes.4.site}} | {{pilotage.interfaces.lignes.4.objet}} | {{pilotage.interfaces.lignes.4.delai_calendaire_j}} j | j {{pilotage.interfaces.lignes.4.date_de_besoin_j::n0}} | j {{pilotage.interfaces.lignes.4.date_limite_de_demande_j::n0}} | {{pilotage.interfaces.lignes.4.marge_a_la_date_d_arret_j::n0}} j | {{pilotage.interfaces.lignes.4.statut}} |
| {{pilotage.interfaces.lignes.5.site}} | {{pilotage.interfaces.lignes.5.objet}} | {{pilotage.interfaces.lignes.5.delai_calendaire_j}} j | j {{pilotage.interfaces.lignes.5.date_de_besoin_j::n0}} | j {{pilotage.interfaces.lignes.5.date_limite_de_demande_j::n0}} | {{pilotage.interfaces.lignes.5.marge_a_la_date_d_arret_j::n0}} j | {{pilotage.interfaces.lignes.5.statut}} |

*({{pilotage.interfaces.nb_besoins_deja_servis}} autres lignes concernent le site principal, dont le
besoin est déjà passé : elles ne portent plus de décision et ferment la liste.)*

{{pilotage.interfaces.lecture}}

{{pilotage.interfaces._ce_que_cette_table_remplace}}

:::figure {"fn":"barres","args":"pilotage.figures.interfaces","titre":"Les interfaces rangées par marge, et non par objet","num":6,"large":true,"options":{"unite":"jours ouvrés de marge à la date d'arrêt","origine":0,"legende_alerte":"demande en retard"},"voir":["Une seule barre est négative : la demande de maintien du service du site secondaire, à déposer {{pilotage.interfaces.lignes.0.delai_calendaire_j}} jours à l'avance, a une marge de {{pilotage.interfaces.lignes.0.marge_a_la_date_d_arret_j::n0}} jours — elle aurait dû être déposée.","Les marges croissent quand le délai de demande décroît : ce sont les interfaces les plus LONGUES à obtenir qui arrivent à échéance en premier, et ce sont celles qu'on découvre en dernier.","Ici chaque site n'a qu'une date de besoin, donc l'ordre par marge se confond avec l'ordre par délai. Sur un chantier réel, chaque interface a sa propre date de besoin et les deux ordres n'ont plus rien à voir : c'est là que le classement par marge devient indispensable.","Aucune de ces lignes n'apparaît dans un indicateur de coût ou de délai. Elles ne se lisent que sur un calendrier et un registre d'interfaces.","Les lignes du site principal sont absentes : leur besoin est derrière nous, donc elles ne portent plus de décision."],"erreur":"Ranger un registre d'interfaces par intervenant ou par objet. Rangé ainsi, il se lit une fois à la signature du marché. Rangé par marge, il se lit à chaque revue — et c'est la même donnée."}
:::

:::encart {"genre":"piege","titre":"Le paradoxe qu'il faut avoir vu une fois : un retard peut sauver une interface"}
La demande en retard porte sur un besoin situé au jour
{{pilotage.interfaces.lignes.0.date_de_besoin_j::n0}}. Si le site prend les
{{pilotage.alerte_ferroviaire.retard_constate_du_site_j}} jours de retard qu'il a constatés, ce
besoin se décale d'autant — et la date limite de dépôt avec lui : la marge passe de
{{pilotage.interfaces.lignes.0.marge_a_la_date_d_arret_j::n0}} à
**+{{pilotage.interfaces.lignes.0.marge_apres_le_retard_du_site_j::n0}} jours**. Le retard rend la
demande faisable.

Ce n'est pas un argument pour prendre du retard, et c'en est un pour ne jamais piloter sur un seul
signal. Les deux indicateurs de ce module pointent ici en sens **inverse** : le retard coûte un cycle
de consignation (§ S3c) et sauve une demande d'interface. Aucun tableau de bord ne tranche cela ;
c'est une décision, elle se prend avec l'exploitant, et elle s'écrit.
:::

## S4 · Étude de cas : la revue du 4ᵉ mois, de bout en bout

Vous êtes le lundi du 4ᵉ mois, jour {{pilotage.date_d_arret_j::n0}}. Voici ce que vous faites, dans
l'ordre, et pourquoi.

**1. Vous vérifiez que les deux situations sont arrêtées au même jour.** Si elles ne le sont pas,
vous ne consolidez rien et vous le dites. C'est la décision la moins technique et la plus souvent
sautée.

**2. Vous lisez les montants avant les ratios.** Dérive totale
{{pilotage.consolidation.derive_totale_MAD::k}} MAD, dépassement prévu à terminaison
{{pilotage.consolidation.depassement_prevu_total_MAD::k}} MAD, soit
{{pilotage.consolidation.depassement_prevu_pct::n1}} % du budget. Ce sont les deux nombres que votre
direction retiendra, et ce sont les seuls qui s'additionnent sans précaution.

**3. Vous regardez la répartition, pas la moyenne.** Le site secondaire fait
{{pilotage.consolidation.poids.1.poids_du_budget_pct::n1}} % du budget et
{{pilotage.consolidation.poids.1.part_du_depassement_prevu_pct::n1}} % du dépassement prévu. C'est
là qu'il faut aller — et le CPI consolidé, lui, ne vous y aurait pas envoyé : il est en
{{pilotage.consolidation.niveau_atteint}}, pas en alerte.

**4. Vous descendez d'un étage, une seule fois.** Sur le site secondaire, le lot
« {{pilotage.masquage_recursif.lot_le_plus_degrade}} » porte
{{pilotage.masquage_recursif.part_de_la_derive_du_site_pct::n0}} % de la dérive. Vous n'avez pas
besoin d'un troisième étage : un lot suffit à expliquer le site, et c'est presque toujours le cas.

**5. Vous posez la seule question qui vaille sur ce lot.** Non pas « pourquoi dérive-t-il », dont la
réponse est connue — un sol que l'offre a sous-estimé — mais **« la dérive est-elle terminée ou
continue-t-elle ? »**. De la réponse dépend l'EAC qu'on annonce :
{{pilotage.sites.1.EAC_si_la_derive_persiste_MAD::k}} MAD si elle persiste, contre un budget de
{{pilotage.sites.1.budget_a_l_achevement_BAC_MAD::k}}. C'est une question de méthode de travail, pas
de comptabilité, et elle se pose au conducteur de travaux, pas au tableau de bord.

**6. Vous sortez du tableau de bord et vous ouvrez le registre des interfaces.** Une demande est en
retard de {{pilotage.interfaces.lignes.0.marge_a_la_date_d_arret_j::n0}} jours ; la suivante a
{{pilotage.interfaces.lignes.1.marge_a_la_date_d_arret_j::n0}} jours de marge. Aucun des cinq
indicateurs précédents ne vous l'aurait dit.

**7. Vous rapprochez le retard du site de la période des fenêtres.**
{{pilotage.alerte_ferroviaire.retard_constate_du_site_j}} jours contre un cycle de
{{pilotage.alerte_ferroviaire.periode_entre_fenetres_j}} : le seuil est franchi, la fenêtre est
perdue, le retard effectif est de {{pilotage.alerte_ferroviaire.retard_effectif_j}} jours. **C'est
le point le plus grave du dossier, et c'est le seul qui ne figure sur aucune de vos courbes.**

**8. Vous écrivez trois lignes, pas trente.** Ce que l'opération va coûter, quel site le cause, et
quelle décision vous demandez à qui. Le reste est en annexe.

:::encart {"genre":"voir","titre":"Ce que cette revue a produit, et ce qu'elle n'a pas produit"}
Elle a produit **deux décisions** : déposer immédiatement la demande d'interface en retard, et
convoquer l'exploitant pour la fenêtre perdue. Elle n'a produit **aucune action corrective sur le
CPI**, et c'est normal : un CPI ne se corrige pas, il constate. Ce qui se corrige est une méthode de
travail sur un lot, et cette décision-là appartient au conducteur de travaux du site — pas à vous.

Un chef de projet suivi qui sort d'une revue avec huit actions correctives sur des indicateurs a
confondu l'instrument et le chantier.
:::

## S5 · Erreurs fréquentes

**1. Moyenner des ratios.** {{pilotage.consolidation.moyenne_des_CPI::n3}} au lieu de
{{pilotage.consolidation.CPI_consolide::n3}} : {{pilotage.consolidation.ecart_entre_les_deux_pts::n1}}
points, dans le sens qui rassure. **Symptôme** : un tableau de bord qui s'écarte du compte du
contrôle de gestion sans que personne sache dire pourquoi, et qui finit par être refait à la main.

**2. Appliquer le même seuil à tous les étages.** Un seuil de CPI 0,95 sur l'opération, sur un site
qui pèse {{pilotage.consolidation.poids.1.poids_du_cout_pct::n1}} % et sur un lot qui pèse 10 % de ce
site, ce sont trois seuils différents dont personne n'a décidé. **Symptôme** : le petit site n'est
jamais en alerte, jusqu'au jour où il l'est de
{{pilotage.seuil_de_masquage.derive_supplementaire_invisible_MAD::k}} MAD d'un coup.

**3. Demander un CPI à un site qui démarre.** À {{suivi.fiabilite_du_cpi.points.0.avancement_pct::n1}} %
d'avancement, l'incertitude vaut {{suivi.fiabilite_du_cpi.points.0.incertitude_pts::n1}} points.
**Symptôme** : des réunions sur un indicateur qui oscille, et une perte de crédibilité de
l'indicateur quand il devient enfin significatif.

**4. Croire qu'un rapport plus fréquent raccourcit la boucle.** En hebdomadaire, la remontée des
données pèse {{pilotage.latence.part_du_delai_de_remontee_dans_l_hebdo_pct::n0}} % de la latence —
et elle ne bouge pas quand le rythme change. **Symptôme** : une réunion de plus par semaine, les mêmes chiffres, et des
conducteurs de travaux qui passent leur vendredi à faire du reporting au lieu de préparer la semaine.

**5. Piloter un chantier sous interception avec des indicateurs de coût.** Un cycle perdu ne dépense
rien : le CPI ne bouge pas. **Symptôme** : une date de mise en service qui recule par paliers de
{{pilotage.alerte_ferroviaire.periode_entre_fenetres_j}} jours, et un tableau de bord resté vert
jusqu'au mois précédent.

**6. Ranger le registre des interfaces par intervenant.** C'est l'ordre dans lequel on l'écrit, pas
celui dans lequel on l'utilise. **Symptôme** : des demandes déposées en retard sur les interfaces les
plus longues — exactement celles qui ne se rattrapent pas.

**7. Consolider deux situations arrêtées à deux dates.** **Symptôme** : un CPI consolidé qui bouge
quand un site change de date de facturation, et personne ne fait le lien.

:::encart {"genre":"piege","titre":"L'erreur de posture, qui ne se voit dans aucun chiffre"}
Un tableau de bord est fait pour **remonter** de l'information, et il est très mauvais pour en
**descendre**. Le chef de projet suivi qui réclame des explications sur un indicateur demande à un
conducteur de travaux de traduire son chantier dans la langue d'un ratio — un travail qui ne produit
rien et qui prend une demi-journée par site et par semaine.

La question qui marche n'est pas « pourquoi ton CPI baisse-t-il ? » mais « **de quoi as-tu besoin
que je débloque cette semaine ?** ». Elle produit une liste courte, vérifiable, et elle vous donne
en prime l'information que l'indicateur mettra trois semaines à vous donner.
:::

## S6 · Exercices

:::exercice {"titre":"1 · Deux sites, deux CPI : quel est celui de l'opération ?","niveau":"application"}
Site A : valeur acquise {{pilotage.sites.0.valeur_acquise_VA_MAD::k}} MAD, coût réel
{{pilotage.sites.0.cout_reel_CR_MAD::k}} MAD. Site B : valeur acquise
{{pilotage.sites.1.valeur_acquise_VA_MAD::k}} MAD, coût réel
{{pilotage.sites.1.cout_reel_CR_MAD::k}} MAD. Quel est le CPI de l'opération ?

**Corrigé.** {{pilotage.consolidation.CPI_consolide::n3}} — le rapport des sommes :
{{pilotage.consolidation.valeur_acquise_VA_MAD::k}} divisé par
{{pilotage.consolidation.cout_reel_CR_MAD::k}}.

La moyenne des deux CPI vaut {{pilotage.consolidation.moyenne_des_CPI::n3}}, soit
{{pilotage.consolidation.ecart_entre_les_deux_pts::n1}} points de moins. Les deux nombres sont des
« CPI de l'opération » en apparence ; un seul a un sens, parce qu'un CPI est un rapport et qu'une
moyenne de rapports ne veut dire quelque chose que si les dénominateurs sont égaux.

**Le réflexe à prendre** : quand on vous donne une moyenne d'indicateurs, demandez les deux sommes.
Si on ne les a pas, l'indicateur n'a pas été consolidé, il a été résumé.
:::

:::exercice {"titre":"2 · De combien le petit site doit-il dériver pour déclencher l'alerte ?","niveau":"application"}
Le seuil d'alerte de l'opération est CPI {{pilotage.consolidation.seuil_d_alerte_CPI::n2}}. Le CPI
consolidé vaut {{pilotage.consolidation.CPI_consolide::n3}}. À coût réel constant, jusqu'où le site
secondaire peut-il tomber sans déclencher l'alerte ?

**Corrigé.** Jusqu'à CPI **{{pilotage.seuil_de_masquage.CPI_du_site_au_seuil_consolide::n3}}**, soit
{{pilotage.seuil_de_masquage.derive_supplementaire_invisible_MAD::k}} MAD de dérive supplémentaire —
{{pilotage.seuil_de_masquage.part_du_budget_du_site_pct::n0}} % du budget de ce site.

On écrit que le CPI consolidé vaut le seuil : $(VA_A + VA_B) / (CR_A + CR_B) = s$, d'où
$VA_B = s \times (CR_A + CR_B) - VA_A$. Tout le reste est connu. *(Le module publie la dérive
calculée sur le CPI limite **arrondi** à quatre décimales, pour qu'un lecteur qui multiplie les deux
nombres imprimés retrouve le troisième : 150 MAD d'écart avec la forme fermée, sur 689 000.)*

**Et la réponse dépend du mécanisme de la dérive** : à coût réel constant —
une valeur acquise en moins — c'est {{pilotage.seuil_de_masquage.derive_supplementaire_invisible_MAD::k}} MAD.
Si la dérive est une **dépense en plus**, il en faut
{{pilotage.seuil_de_masquage.derive_invisible_si_surcout_MAD::k}} MAD, parce que le dénominateur
grandit avec elle — et c'est le cas le plus fréquent sur un chantier, donc le plus favorable au
masquage.

**Ce que l'exercice enseigne** : ce nombre est le vrai contenu d'un seuil d'alerte consolidé. Le
publier à côté du seuil change la discussion — on ne demande plus « sommes-nous en alerte ? » mais
« de combien un site peut-il déraper sans que ce tableau le dise ? ».
:::

:::exercice {"titre":"3 · Le rythme du reporting : que gagne-t-on à passer à l'hebdomadaire ?","niveau":"probleme"}
Votre direction propose de passer du reporting mensuel à l'hebdomadaire sur les deux sites. Le délai
de remontée des données est de {{pilotage.latence.lignes.0.delai_de_remontee_j::n0}} jours ouvrés.
Que gagnez-vous, et que proposez-vous à la place — ou en plus ?

**Corrigé.** Vous gagnez {{pilotage.latence.ecart_des_deux_rythmes_j::n0}} jours de latence moyenne,
soit {{pilotage.latence.cout_de_l_ecart_MAD::k}} MAD de frais de durée par dérive détectée. C'est
réel, et c'est quatre fois moins que ce qu'on attend d'un facteur quatre sur la période.

La raison est arithmétique : la latence vaut une demi-période **plus** le délai de remontée. En
mensuel, {{pilotage.latence.lignes.1.periode_j::n0}}/2 + {{pilotage.latence.lignes.1.delai_de_remontee_j::n0}}
= {{pilotage.latence.lignes.1.latence_moyenne_j::n1}} jours. En hebdomadaire,
{{pilotage.latence.lignes.0.periode_j::n0}}/2 + {{pilotage.latence.lignes.0.delai_de_remontee_j::n0}}
= {{pilotage.latence.lignes.0.latence_moyenne_j::n1}}. Le terme de remontée, lui, n'a pas bougé : il
pèse désormais {{pilotage.latence.part_du_delai_de_remontee_dans_l_hebdo_pct::n0}} % de la latence.

**Ce que vous proposez** : attaquer **aussi** le délai de remontée, qui ne se négocie pas en
réunion mais en organisation — attachements saisis le jour même sur le site, un seul format, une
seule personne qui consolide. Le ramener de
{{pilotage.latence.lignes.0.delai_de_remontee_j::n0}} à 1 jour gagne 3 jours de latence, contre
{{pilotage.latence.ecart_des_deux_rythmes_j::n1}} pour le changement de rythme : moins, mais sans
une réunion de plus, et les deux gains s'additionnent. Et surtout, sans ce travail-là, le rythme
hebdomadaire plafonne : la remontée pèserait alors
{{pilotage.latence.part_du_delai_de_remontee_dans_l_hebdo_pct::n0}} % de ce qui reste.

**Et la question qui fâche** : quelles décisions prendrez-vous en hebdomadaire que vous ne preniez
pas en mensuel ? Si la réponse est « aucune », le rythme n'est pas le problème.
:::

:::exercice {"titre":"4 · Un retard de trois semaines : combien coûte-t-il, et que vaut un jour rattrapé ?","niveau":"probleme"}
Le site secondaire annonce {{pilotage.alerte_ferroviaire.retard_constate_du_site_j}} jours ouvrés de
retard sur son lot de fondations. Le conducteur de travaux propose de renforcer les équipes pour en
rattraper dix. Qu'en pensez-vous — et que proposez-vous ?

**Corrigé — la réponse ne se lit pas sur le retard, elle se lit sur l'escalier.** La période entre
deux fenêtres de consignation vaut {{pilotage.alerte_ferroviaire.periode_entre_fenetres_j}} jours.

À {{pilotage.alerte_ferroviaire.retard_constate_du_site_j}} jours, le site a franchi la première
marche : le travail attend la {{pilotage.alerte_ferroviaire.cycles_perdus}}ᵉ fenêtre et le retard
effectif est de {{pilotage.alerte_ferroviaire.retard_effectif_j}} jours.

**Les dix jours proposés sont utiles — et beaucoup plus que proposés.** Rattraper dix jours ramène
le retard à {{pilotage.alerte_ferroviaire.effet_de_rattraper_10_j::n0}} jours effectifs : un cycle
entier de gagné, soit {{pilotage.alerte_ferroviaire.periode_entre_fenetres_j}} jours sur la date
d'interception.

**Mais il n'en faut pas dix.**

{{pilotage.alerte_ferroviaire._ce_que_rattraper_veut_dire}}

Autrement dit : **deux jours rattrapés en valent vingt ; les huit suivants n'en valent aucun.** Ce
que vous proposez n'est donc pas « renforcez les équipes », c'est « trouvez-moi deux jours avant la
date de la fenêtre, et ne dépensez pas un dirham de plus ». Les huit autres jours d'effort seraient
à garder pour la marche suivante — ou à ne pas dépenser.

**Et la question à poser à l'exploitant** : la fenêtre suivante peut-elle être allongée ou doublée ?
C'est la seule négociation qui change l'escalier lui-même, et elle vaut plus que n'importe quel
renfort d'équipe.

**Ce que coûte le cycle perdu, si personne ne trouve ces deux jours** :
{{pilotage.alerte_ferroviaire.cout_d_un_cycle_perdu_en_frais_de_duree_MAD::k}} MAD de frais de
durée — et pas un centième de CPI, puisque cette dépense est hors du périmètre de l'indicateur.
:::

:::exercice {"titre":"5 · Revue critique : un tableau de bord à refuser","niveau":"revue"}
On vous remet le tableau de bord mensuel de l'opération : « CPI opération **0,82** · SPI **0,83** ·
avancement **28 %** · deux sites, tous deux en vigilance · 14 actions correctives ouvertes ».
Que relevez-vous ?

**Corrigé — quatre observations, dont deux de fond.**

**a. Le CPI de 0,82 est une moyenne de ratios.** Le vrai consolidé vaut
{{pilotage.consolidation.CPI_consolide::n3}}. L'écart est de
{{pilotage.consolidation.ecart_entre_les_deux_pts::n1}} points et il n'est pas aléatoire : moyenner
donne toujours plus de poids au petit site. **Demande** : les quatre sommes (VA et CR par site), et
le rapport des sommes.

**b. « Tous deux en vigilance » est faux et masque l'essentiel.** Le site secondaire est à CPI
{{pilotage.sites.1.CPI::n3}} — sous le seuil d'alerte de
{{pilotage.consolidation.seuil_d_alerte_CPI::n2}}, pas en vigilance. Et sa dérive prévue représente
{{pilotage.consolidation.poids.1.part_du_depassement_prevu_pct::n1}} % du dépassement de l'opération
pour {{pilotage.consolidation.poids.1.poids_du_budget_pct::n1}} % du budget. **Demande** : le
dépassement prévu à terminaison par site, en MAD.

**c. L'avancement de 28 % n'a pas de dénominateur.** Avancement de quoi — du budget, de la surface,
des heures ? Ce module et D4 l'ont montré : trois dénominateurs, trois réponses. **Demande** : le
dénominateur, écrit à côté du nombre.

**d. Quatorze actions correctives sur des indicateurs.** Un indicateur ne se corrige pas. **Demande** :
combien de ces actions portent sur une méthode de travail, et combien sur un chiffre. Les secondes se
ferment séance tenante.

**Et ce qui manque, qui est le plus grave** : pas une ligne sur les interfaces. Une demande est en
retard de {{pilotage.interfaces.lignes.0.marge_a_la_date_d_arret_j::n0}} jours et un cycle de
consignation est perdu. Un tableau de bord d'opération ferroviaire qui ne porte pas la marge des
interfaces mesure le chantier d'hier.
:::

## S7 · Check-list, glossaire et quiz

**Check-list : avant d'envoyer un rapport consolidé**

1. Les situations des sites sont-elles arrêtées **au même jour** ?
2. Le CPI consolidé est-il le **rapport des sommes** — et les quatre sommes figurent-elles au
   rapport ?
3. Le **dépassement prévu par site**, en MAD, est-il écrit ? C'est lui qui s'additionne.
4. Le seuil d'alerte a-t-il été fixé **par étage** d'agrégation, et avant de lire les chiffres ?
5. Pour chaque site : quelle **dérive supplémentaire** passerait inaperçue au niveau consolidé ?
6. Pour chaque site en écart : la **ligne qui a bougé** est-elle nommée, un étage plus bas ?
7. Les sites peu avancés sont-ils signalés comme **non significatifs** plutôt que consolidés en
   silence ?
8. La **latence** du dispositif est-elle connue, et les décisions à horizon plus court sont-elles
   explicitement hors du reporting ?
9. Le registre des **interfaces** est-il rangé par marge, et la plus urgente figure-t-elle au
   rapport ?
10. Le **retard de chaque site** est-il comparé à la période entre deux fenêtres de consignation ?
11. Les actions ouvertes portent-elles sur des **méthodes**, ou sur des indicateurs ?

**Glossaire**

| Terme | Ce que c'est |
|---|---|
| **VA, valeur acquise** | budget × avancement **physique**. Jamais budget × avancement de dépense, qui donnerait CPI = 1 par construction |
| **CPI** | VA / CR. Un rapport : il ne se moyenne pas, il se recompose |
| **CPI consolidé** | ΣVA / ΣCR. Une moyenne des CPI pondérée par les **coûts réels** |
| **Amortissement d'un site** | l'inverse de son poids : de combien l'indicateur consolidé divise sa dérive |
| **Seuil de masquage** | la dérive qu'un site peut encore prendre sans faire franchir le seuil au consolidé |
| **Latence de détection** | demi-période de reporting + délai de remontée. Ce n'est pas la période |
| **Délai de remontée** | de la fin de période à la donnée vérifiée. {{pilotage.latence.part_du_delai_de_remontee_dans_l_hebdo_pct::n0}} % de la latence en hebdomadaire, et la seule part qu'une réunion ne réduit pas |
| **Date limite de demande** | date de besoin − délai d'instruction de l'interface. Une soustraction, et le seul vrai indicateur avancé |
| **Retard quantisé** | sous consignation, un retard ne croît pas continûment : il saute d'une période de fenêtre (B7c, D-050) |
| **EAC** | prévision à terminaison. Trois formules selon que la dérive est systématique, accidentelle, ou que le délai se paie (D4) |

**Quiz**

**1. Deux sites, CPI 0,90 et 0,75. Quel est le CPI de l'opération ?**
**On ne peut pas le dire.** Il faut les coûts réels. Ici, avec
{{pilotage.consolidation.poids.0.poids_du_cout_pct::n1}} / {{pilotage.consolidation.poids.1.poids_du_cout_pct::n1}},
il vaut {{pilotage.consolidation.CPI_consolide::n3}} — pas la moyenne
{{pilotage.consolidation.moyenne_des_CPI::n3}}.

**2. De combien l'indicateur consolidé divise-t-il la dérive du petit site ?**
**Par {{pilotage.consolidation.poids.1.amortissement::n1}}**, c'est-à-dire par l'inverse de son poids
dans le coût réel. C'est une loi, pas une particularité de ce chantier.

**3. Combien faut-il de dérive pour faire bouger le CPI consolidé d'un centième ?**
**{{pilotage.consolidation.MAD_pour_un_centieme_de_CPI::k}} MAD**, où qu'elle se produise : un
centième de CPI vaut un centième du coût réel total.

**4. Le CPI d'un site vaut 0,75, celui de son plus mauvais lot 0,69. Lequel pilote-t-on ?**
**Le lot** — il porte {{pilotage.masquage_recursif.part_de_la_derive_du_site_pct::n0}} % de la dérive
du site. Le CPI du site est déjà une moyenne : il amortit son propre lot d'un facteur
{{pilotage.masquage_recursif.amortissement_du_lot_par_le_site::n1}}.

**5. Passer du mensuel à l'hebdomadaire divise-t-il la latence par quatre ?**
**Non** : de {{pilotage.latence.lignes.1.latence_moyenne_j::n1}} à
{{pilotage.latence.lignes.0.latence_moyenne_j::n1}} jours. La période est divisée par quatre, pas le
délai de remontée — qui pèse ensuite
{{pilotage.latence.part_du_delai_de_remontee_dans_l_hebdo_pct::n0}} % du total.

**6. Quel est le bon seuil d'alerte d'un site sous consignation ?**
**{{pilotage.alerte_ferroviaire.periode_entre_fenetres_j}} jours de retard** — la période entre deux
fenêtres. Ce n'est pas un pourcentage, et aucun indicateur de coût ne le mesure.

**7. Un cycle de consignation perdu fait-il baisser le CPI ?**
**Non.** Le travail n'est pas fait, donc pas payé : ni valeur acquise ni coût réel. Le CPI ne bouge
pas d'un millième, et c'est l'angle mort le plus large d'un tableau de bord ferroviaire.

**8. Quelle est la première question d'une revue multi-sites ?**
**« Les situations sont-elles arrêtées au même jour ? »** Tout le reste en dépend, et c'est la seule
question de la liste qui ne demande aucun calcul.

:::memo
## Fiche mémo — pilotage multi-sites : une page de tableau de bord

**Les trois phrases du module**

> Un ratio ne se consolide pas : ΣVA / ΣCR, jamais la moyenne des CPI.
> Chaque étage d'agrégation divise la dérive d'un site par son poids.
> Sous consignation, le seuil d'alerte est une DURÉE, pas un pourcentage.

**Les deux formules**

$$ \text{CPI}_{\text{cons}} = \frac{\sum \text{VA}_i}{\sum \text{CR}_i} \qquad \text{latence} = \frac{T_{\text{reporting}}}{2} + T_{\text{remontée}} $$

**Le tableau de bord de ce mois (jour {{pilotage.date_d_arret_j::n0}})**

| | Principal | Secondaire | Opération |
|---|---:|---:|---:|
| CPI | {{pilotage.sites.0.CPI::n3}} | **{{pilotage.sites.1.CPI::n3}}** | {{pilotage.consolidation.CPI_consolide::n3}} ({{pilotage.consolidation.niveau_atteint}}) |
| SPI | {{pilotage.sites.0.SPI::n3}} | {{pilotage.sites.1.SPI::n3}} | {{pilotage.consolidation.SPI_consolide::n3}} |
| Dérive à date | {{pilotage.sites.0.derive_MAD::k}} | {{pilotage.sites.1.derive_MAD::k}} | **{{pilotage.consolidation.derive_totale_MAD::k}} MAD** |
| Dépassement prévu | {{pilotage.consolidation.poids.0.depassement_prevu_MAD::k}} | {{pilotage.consolidation.poids.1.depassement_prevu_MAD::k}} | **{{pilotage.consolidation.depassement_prevu_total_MAD::k}} MAD** ({{pilotage.consolidation.depassement_prevu_pct::n1}} %) |
| Part du budget / du dépassement | {{pilotage.consolidation.poids.0.poids_du_budget_pct::n1}} / {{pilotage.consolidation.poids.0.part_du_depassement_prevu_pct::n1}} % | {{pilotage.consolidation.poids.1.poids_du_budget_pct::n1}} / **{{pilotage.consolidation.poids.1.part_du_depassement_prevu_pct::n1}} %** | — |
| Interface en retard | — | {{pilotage.interfaces.lignes.0.objet}} : {{pilotage.interfaces.lignes.0.marge_a_la_date_d_arret_j::n0}} j | — |
| Prochaine à déposer | — | {{pilotage.interfaces.la_plus_urgente_encore_tenable.objet}} : {{pilotage.interfaces.la_plus_urgente_encore_tenable.marge_a_la_date_d_arret_j::n0}} j de marge | — |
| Retard contre cycle de fenêtre | — | {{pilotage.alerte_ferroviaire.retard_constate_du_site_j}} j / {{pilotage.alerte_ferroviaire.periode_entre_fenetres_j}} j → **{{pilotage.alerte_ferroviaire.retard_effectif_j}} j** | — |

**Les six réflexes**

1. Même date d'arrêt, sinon on ne consolide pas.
2. Les montants avant les ratios ; les ratios disent qui, les montants disent combien.
3. Un seuil par étage, écrit avant de lire.
4. Descendre d'un étage, une fois : la ligne qui a bougé.
5. Un site peu avancé n'a pas de CPI — le dire plutôt que le consolider.
6. Ouvrir le registre des interfaces à chaque revue, rangé par marge.

**Ce qui reste ⏸**

Obligations contractuelles de reporting (contenu, destinataires, délais) · seuils de déclaration et
d'alerte imposés par le marché · conditions d'ouverture d'une réclamation · formes et délais des
ordres de service · règles d'accès et d'autorisation propres au gestionnaire d'infrastructure.
:::
