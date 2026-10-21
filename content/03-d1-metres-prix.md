---
id: D1
titre: Métrés, prix, sous-détails et situations de travaux
fil: Palier 1 · module 2 — direction de projet
resume: Un prix n'est pas un nombre qu'on pose, c'est une décomposition qu'on construit — et sa main-d'œuvre vient du planning, pas d'une estimation séparée.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · toutes les valeurs numériques sont V3 · les taux contractuels se lisent dans le CPS
pied: Exemple pédagogique — ne remplace ni un bordereau de marché, ni un sous-détail visé, ni l'avis d'un économiste de la construction.
donnees: prix, planification, gare
---

## S1 · Ce que ce module fait, et ce qu'il ne refait pas

Le module D2 a donné au chantier ses durées. Celui-ci lui donne ses prix. Et il les fait sortir des
**mêmes hypothèses** — c'est tout l'enjeu : un planning et un bordereau qui ne partagent pas leurs
cadences se contredisent sans que personne ne s'en aperçoive, parce que les deux documents sont lus
par des gens différents, à des réunions différentes.

Trois choses que ce module fait, et qu'un bordereau de ratios ne peut pas faire :

1. le prix unitaire n'est pas saisi, il est **construit** — et la part de main-d'œuvre qu'il porte
   est **déduite de la cadence et de l'effectif du planning**, jamais estimée à part ;
2. le **type** d'un poste suit la **famille de sa durée** (D2) : tâche calculée → prix unitaire,
   tâche déclarée → forfait, tâche imposée → fourniture sans heure de chantier ; et certains coûts
   ne dépendent d'**aucune quantité** : ils sont indexés sur la durée, et c'est par eux qu'un retard
   coûte de l'argent sans qu'un m³ de plus soit coulé ;
3. retourner les cadences en **productivités par compagnon** localise une erreur qu'un ratio global
   ne faisait que signaler — c'est ici que la dette n° 10 du projet se règle, ou du moins se chiffre.

Ce module ne vous réapprend ni ce qu'est un métré, ni comment on remplit un bordereau. Il traite ce
qui se passe **entre** les deux, et ce qui se passe quand le chantier commence à les contredire.

**Prérequis** : le module D2 (durées, cadences, familles) et le module TV (le métré géométrique
d'une zone de plancher). **Place dans le projet** : étape 8 du déroulé du cas phare (§ 10.2) ;
D4 s'y accroche entièrement, D3 et D7 en dépendent.

:::encart {"genre":"note","titre":"Aucun chiffre de ce module n'est un prix de marché"}
Les prix de ressource, les coefficients de consommation et les taux contractuels sont tous **V3** :
des hypothèses déclarées avec leur fourchette et leur année de référence, posées pour faire tourner
l'exemple. Aucun bordereau réel n'a été fourni (question 7 de l'Étape 0, restée sans réponse). Les
taux contractuels — avance, retenue, délai de paiement, révision, pénalités — se lisent **dans le
CPS du marché**, qui prime sur tout ce qui est écrit ici.

Ce que vous pouvez reprendre de ce module : la **méthode**, les **ordres de grandeur relatifs** (la
part d'un lot dans un total, le rapport entre frais de durée et pénalités), et les **contrôles**.
Pas les chiffres.
:::

## S2 · L'idée centrale : un prix est une décomposition, pas un nombre

Posez un prix de {{gare.prix_unitaires_MAD.postes.beton_m3.valeur}} MAD le m³ de béton posé et vous
avez un chiffre. Décomposez-le et vous avez **une décision par ligne** : quel béton, livré ou
fabriqué sur place, pompé ou à la benne, avec quel ratio d'acier, combien de rotations de coffrage,
et surtout — combien d'heures.

La ligne d'heures est la seule qui relie le prix au chantier, et c'est pour cela qu'elle ne se
saisit pas. Elle se **déduit** :

$$ h_{\text{par unité}} = \frac{h_{\text{par jour}} \times n_{\text{compagnons par atelier}}}{c_{\text{cadence d'atelier}}} \times k_{\text{conversion}} $$

où $k$ est le nombre d'unités de cadence par unité de bordereau — 1 quand les deux coïncident.
Remarquez ce qui n'y figure **pas** : le nombre d'ateliers. Doubler les ateliers divise la durée par
deux et laisse le prix **inchangé**. C'est exact et c'est contre-intuitif : les moyens achètent du
délai, pas du prix. Le test de ce module le vérifie en rejouant le bordereau entier avec deux fois
plus d'ateliers de voiles.

**La conséquence pratique** : changez une cadence dans `data/`, et la durée du chantier **et** le
prix du poste bougent ensemble, du même mouvement. C'est la seule architecture dans laquelle on peut
répondre « et si ? » en réunion sans refaire deux documents.

### Trois types de postes, parce qu'il y a trois familles de durées

| Famille de durée (D2) | Type de poste (D1) | Sa main-d'œuvre | Combien ici |
|---|---|---|---:|
| **Calculée** | prix unitaire, construit par sous-détail | déduite de la cadence | {{planification.familles.nb_taches.calculee::n0}} |
| **Déclarée** | **forfait**, tout compris | présente, mais **invisible** | {{planification.familles.nb_taches.declaree::n0}} |
| **Imposée** | **fourniture**, sans heure de chantier | chez le fournisseur | {{planification.familles.nb_taches.imposee::n0}} |

Cette correspondance n'est pas une commodité de présentation : elle décide de ce qu'on sait et de ce
qu'on ne sait pas. Un forfait de {{gare.prix_unitaires_MAD.forfaits_MAD.NOYX.valeur}} MAD pour les
noyaux et escaliers **contient** ses ferrailleurs et ses coffreurs — mais on ne sait pas combien. Y
ajouter des heures calculées depuis le planning, comme la première version de ce module le faisait,
revient à les compter deux fois. L'erreur ne pesait que quelques pour cent du total ; elle rendait
en revanche toute part de main-d'œuvre **ininterprétable**, parce qu'elle mêlait des heures connues
et des heures inventées.

## S3 · Principes

### a. Le métré n'est pas une mesure, c'est une convention

La même paroi n'a pas une quantité : elle en a plusieurs, selon ce qu'on décide de compter. Trois
conventions suffisent à faire varier un métré de 30 % :

| Convention | Les deux réponses possibles | Où elle mord ici |
|---|---|---|
| Déduction des ouvertures | on déduit à partir de tant de m², ou on ne déduit pas | façades, voiles |
| Unité du poste | le m³ **en place** ou le m³ **foisonné** | déblais : {{gare.planning.ratios_quantites_V3.foisonnement_pct.valeur}} % d'écart entre les deux |
| Surface de coffrage | sous-face seule, ou sous-face + joues + fonds de poutres + rives | {{tranche-plancher.quantites.ratio_coffrage_m2_par_m2::n3}} m² de coffrage par m² de plancher, mesuré sur la géométrie au module TV |

La règle de conduite tient en une phrase : **le métré et le prix doivent parler la même unité, et
c'est écrit avant de chiffrer, pas après.** Le poste de terrassement de ce bordereau se paie au m³
**en place** ; l'évacuation, elle, se paie au m³ **foisonné**, et le facteur de foisonnement est le
pont entre les deux. L'oublier fait perdre un quart du poste transport, et personne ne le voit avant
le premier attachement contradictoire.

### b. Du déboursé sec au prix de vente

$$ PV = \big(MO + \text{matériaux} + \text{matériel}\big) \times \big(1 + f_{\text{siège}} + a + m\big) $$

Le déboursé sec est ce que le poste coûte **sur le chantier**. Le coefficient d'entreprise y ajoute
les frais généraux du siège, les aléas et la marge — ici
{{gare.prix_unitaires_MAD.composition_prix_pct.frais_generaux_siege.valeur}} %,
{{gare.prix_unitaires_MAD.composition_prix_pct.aleas.valeur}} % et
{{gare.prix_unitaires_MAD.composition_prix_pct.marge.valeur}} %, soit un coefficient de
**{{prix.bordereau.coefficient_de_vente::n4}}**.

:::encart {"genre":"alerte","titre":"Le double compte le plus courant du métré"}
Beaucoup de bordereaux ajoutent en plus un taux de « frais de chantier » de 10 à 15 % : installation,
encadrement, base-vie, grue, énergie. **Ce bordereau-ci ne le fait pas, et c'est délibéré** — parce
que ces frais y sont déjà, en **postes** : l'installation, le montage de la grue, et une ligne de
frais indexés sur la durée. Les compter aux deux endroits les compte deux fois.

Un bordereau fait l'un **ou** l'autre. Le vérifier prend trente secondes et c'est la première chose
à regarder dans un sous-détail qu'on vous soumet au visa : si vous trouvez à la fois un poste
« installation de chantier » et un taux de frais de chantier, demandez lequel des deux est en trop.
:::

### c. Les coûts qui ne dépendent d'aucune quantité

Encadrement, base-vie, location de grue, énergie : ces postes ne se métrent pas, ils **durent**.
Ici {{prix.bordereau.frais_de_duree.cout_MAD_par_mois::n0}} MAD par mois, soit
{{prix.bordereau.frais_de_duree.total_MAD::n0}} MAD sur
{{prix.bordereau.frais_de_duree.duree_mois::n1}} mois — **{{prix.bordereau.par_lot.9 · Frais de duree.part_pct::n1}} %** du déboursé du chantier.

C'est par eux que le planning et le coût se touchent vraiment. Un mois de retard ne coûte pas « du
retard » : il coûte **{{prix.bordereau.frais_de_duree.cout_MAD_par_mois::n0}} MAD** de frais qui
continuent de courir pendant que rien ne se construit — plus les pénalités, qui sont une autre
histoire et qu'on chiffre au § S4h.

### d. Le contre-calcul : deux voies qui ne mesurent pas la même chose

Le bordereau est chiffré **deux fois** sur le même périmètre — les six postes de béton armé qu'un
ratio sait chiffrer :

| | Voie A · sous-détail construit | Voie B · prix posés du marché |
|---|---:|---:|
| Montant | {{prix.ecart_des_deux_voies.voie_A_sous_detail_MAD::n0}} MAD | {{prix.ecart_des_deux_voies.voie_B_prix_poses_MAD::n0}} MAD |

Écart : **{{prix.ecart_des_deux_voies.ecart_pct::n1}} %**, pour une tolérance déclarée de
{{prix.ecart_des_deux_voies.tolerance_pct::n0}} %. La tolérance de 5 % du § 3.3 ne s'applique pas
ici, et il faut dire pourquoi : les deux voies **ne chiffrent pas le même objet**. L'une construit un
prix à partir de ressources nommées, l'autre lit un prix de marché qui porte des sujétions que
personne ne détaille. Le § S4d en tire la conséquence utile.

## S4 · Étude de cas : le bordereau de la gare

### a. Un sous-détail, ligne par ligne

Le m² de voile du niveau technique, construit de bas en haut. Chaque ligne vient de `data/` ; aucune
n'est saisie dans ce texte.

| Ligne | Quantité par m² | Prix unitaire | Montant |
|---|---:|---:|---:|
| Béton prêt à l'emploi | {{gare.prix_unitaires_MAD.coefficients_sous_detail.pertes_beton_pct.valeur::n0}} % de pertes sur {{gare.planning.ratios_quantites_V3.voile_epaisseur_m.valeur}} m | {{gare.prix_unitaires_MAD.ressources.materiaux_MAD.beton_bpe_m3.valeur::n0}} MAD/m³ | |
| Acier HA | {{gare.prix_unitaires_MAD.coefficients_sous_detail.acier_kg_par_m3.voile.valeur::n0}} kg/m³ × {{gare.planning.ratios_quantites_V3.voile_epaisseur_m.valeur}} m | {{gare.prix_unitaires_MAD.ressources.materiaux_MAD.acier_ha_kg.valeur}} MAD/kg | |
| Coffrage | {{gare.prix_unitaires_MAD.coefficients_sous_detail.coffrage_m2_par_unite.voile_par_m2.valeur}} m² de banche par m² de voile | {{gare.prix_unitaires_MAD.ressources.materiaux_MAD.coffrage_rotation_m2.valeur::n0}} MAD/rotation | |
| **Main-d'œuvre** | **{{prix.bordereau.par_poste.VOIL.main_oeuvre.h_par_unite::n3}} h/m²**, déduites de la cadence | {{prix.bordereau.par_poste.VOIL.main_oeuvre.taux.taux_MAD_h::n2}} MAD/h | |
| **Déboursé sec** | | | **{{prix.bordereau.par_poste.VOIL.debourse_sec_par_unite_MAD::n2}} MAD/m²** |
| **Prix de vente** | × {{prix.bordereau.coefficient_de_vente::n4}} | | **{{prix.bordereau.par_poste.VOIL.pu_de_vente_MAD::n2}} MAD/m²** |

Le taux horaire de {{prix.bordereau.par_poste.VOIL.main_oeuvre.taux.taux_MAD_h::n2}} MAD n'est pas celui
d'un compagnon : c'est celui d'un **atelier**, déduit de sa composition — un chef d'équipe,
{{gare.prix_unitaires_MAD.ressources.composition_atelier.part_compagnons_qualifies_pct.valeur::n0}} %
de compagnons qualifiés, le reste en manœuvres. Sans cette ligne, un sous-détail paie des
ferrailleurs au prix du manœuvre, et se trompe de 20 à 30 % sur sa main-d'œuvre.

:::figure {"fn":"cascade","args":"prix.figures.cascade","titre":"Construction du prix du m² de voile, du déboursé sec au prix de vente","num":1,"large":true,"options":{"unite":"MAD par m² de voile"},"voir":["Les matériaux écrasent tout : {{prix.bordereau.par_poste.VOIL.materiaux.0.montant_MAD::n0}} MAD de béton, {{prix.bordereau.par_poste.VOIL.materiaux.1.montant_MAD::n0}} MAD d'acier et {{prix.bordereau.par_poste.VOIL.materiaux.2.montant_MAD::n0}} MAD de coffrage — ensemble {{prix.bordereau.par_poste.VOIL.materiaux.0.montant_MAD::n0}} + {{prix.bordereau.par_poste.VOIL.materiaux.1.montant_MAD::n0}} + {{prix.bordereau.par_poste.VOIL.materiaux.2.montant_MAD::n0}} = {{prix.figures.cascade.1.montant::n0}} MAD, soit la quasi-totalité du déboursé sec, contre {{prix.bordereau.par_poste.VOIL.main_oeuvre.montant_MAD_par_unite::n0}} MAD de main-d'œuvre.","L'acier arrive presque au niveau du béton sur ce voile de {{gare.planning.ratios_quantites_V3.voile_epaisseur_m.valeur}} m : {{prix.bordereau.par_poste.VOIL.materiaux.1.montant_MAD::n0}} contre {{prix.bordereau.par_poste.VOIL.materiaux.0.montant_MAD::n0}} MAD. C'est le ratio d'acier, {{gare.prix_unitaires_MAD.coefficients_sous_detail.acier_kg_par_m3.voile.valeur::n0}} kg/m³, qui le décide — et c'est l'hypothèse la plus incertaine de la colonne, puisque le calcul réglementaire qui la fixerait est suspendu (§ 5.0).","Les trois dernières barres ne sont pas du chantier : frais de siège, aléas et marge. Elles transforment un coût en prix, et c'est la seule partie du dessin qui relève d'une décision d'entreprise.","Le trait pointillé reporte le cumul d'une barre à la suivante : c'est ce report qui fait qu'une cascade se lit, là où un camembert de pourcentages ne dirait pas d'où l'on part."],"erreur":"Lire la part de main-d'œuvre d'UN poste comme si c'était celle du chantier. Un voile est un ouvrage de matière ; un poste de ferraillage pur donnerait l'image inverse. La part de main-d'œuvre ne se lit que sur un périmètre qu'on a nommé — c'est tout le § S4e."}
:::

### b. Le bordereau par lot

Vingt-sept postes, un par tâche du planning, plus la ligne des frais indexés sur la durée. Total :
**{{prix.bordereau.prix_de_vente_MAD::n0}} MAD**, soit
{{prix.bordereau.cout_MAD_par_m2_emprise::n0}} MAD/m² d'emprise.

:::figure {"fn":"barres","args":"prix.figures.lots","titre":"Déboursé sec par lot","num":2,"large":true,"options":{"unite":"millions de MAD"},"voir":["Les deux premiers lots ne sont pas du gros œuvre : finitions et clos-couvert pèsent à eux seuls {{prix.bordereau.par_lot.7 · Finitions.part_pct::n1}} % et {{prix.bordereau.par_lot.5 · Clos et couvert.part_pct::n1}} %. C'est l'ordre de grandeur habituel d'un bâtiment recevant du public, et c'est pourquoi un chef de projet qui ne suit que le gros œuvre ne suit que le quart de son budget.","Le lot « frais de durée » — {{prix.bordereau.par_lot.9 · Frais de duree.part_pct::n1}} % — n'a aucune quantité. Il est proportionnel au PLANNING, et c'est la seule ligne du bordereau qu'un retard fait grossir toute seule.","Le gros œuvre proprement dit (terrassements, infrastructure, superstructure) ne fait que {{prix.controle_ratios.part_gros_oeuvre.constate::n1}} % du déboursé, en dessous de la fourchette de référence {{prix.controle_ratios.part_gros_oeuvre.fourchette.0}} à {{prix.controle_ratios.part_gros_oeuvre.fourchette.1}} % : ce bâtiment est plus un ouvrage d'enveloppe et de systèmes qu'un ouvrage de béton."],"erreur":"Chiffrer finement le gros œuvre et estimer le second œuvre au ratio. C'est exactement l'inverse du poids des deux lots, et c'est l'erreur qui fait exploser les estimations d'avant-projet."}
:::

### c. Ce que le bordereau sait, et ce qu'il ne sait pas

| | Postes | Déboursé | Heures connues |
|---|---:|---:|---:|
| Prix unitaires construits | {{prix.controle_ratios._perimetres.tous_postes_decomposes.length}} | — | {{prix.bordereau.heures_de_main_oeuvre_de_chantier::n0}} h |
| Forfaits tout compris | {{prix.controle_ratios._perimetres.forfaits_sans_part_de_main_oeuvre.length}} | — | **aucune** |
| Fournitures | 3 | — | aucune, et c'est normal |

Les heures des forfaits existent — des gens travaillent sur ces postes, le planning leur donne même
un effectif — mais elles ne sont pas **dans le prix**, donc elles ne sont pas connues **du
bordereau**. Cette distinction paraît scolastique ; elle décide de la validité de tous les ratios de
contrôle, comme le § suivant le montre.

### d. Les deux voies, et la ligne qui manque

L'écart entre le prix construit et le prix de marché est de
**{{prix.ecart_des_deux_voies.ecart_pct::n1}} %** — et il est **de même signe sur les six postes**,
de {{prix.ecart_des_deux_voies.par_poste.VOIL.ecart_pct::n0}} % à
{{prix.ecart_des_deux_voies.par_poste.FOND.ecart_pct::n0}} %.

Un écart systématique n'est pas une dispersion : c'est **une ligne qui manque**. Un sous-détail
porte les ressources qu'on sait nommer — béton, acier, coffrage, heures, engins — et pas celles
qu'on oublie : consommables, nettoyage, reprises de parement, calage, attente d'approvisionnement,
encadrement d'équipe. Il faudrait ajouter
**{{prix.ecart_des_deux_voies.divers_necessaire_pct::n1}} %** de « divers de chantier » sur le
déboursé sec pour recoller au prix de marché.

**C'est ainsi qu'un métreur calibre sa ligne de divers** : contre des prix de marché, poste par
poste, et non en recopiant un pourcentage d'usage. Et c'est une information qu'on ne peut obtenir
qu'en ayant fait les deux calculs — raison pour laquelle on les fait tous les deux.

### e. Les productivités, ou comment on localise une erreur qu'un ratio signale

Le module TV avait trouvé une part de main-d'œuvre de 5,2 % là où le métier en attend 15 à 30 %, et
en avait conclu — prudemment — que les cadences étaient probablement optimistes d'un facteur 2 à 3.
C'est la **dette n° 10** du projet. Ce module peut enfin l'instruire, et la réponse tient en deux
temps.

**Premier temps : le ratio était appliqué à une base où il n'est pas défini.**

| Base | Part de main-d'œuvre | Verdict |
|---|---:|---|
| Béton armé décomposé ({{prix.controle_ratios._perimetres.beton_arme_decompose.length}} postes) | {{prix.controle_ratios.part_main_oeuvre_beton_arme_decompose.constate::n2}} % | la fourchette {{prix.controle_ratios.part_main_oeuvre_beton_arme_decompose.fourchette.0}}–{{prix.controle_ratios.part_main_oeuvre_beton_arme_decompose.fourchette.1}} % s'applique |
| Tous postes décomposés | {{prix.controle_ratios.part_main_oeuvre_tous_postes_decomposes.constate::n2}} % | **aucun** : la base mêle béton et fournitures |
| Bordereau entier | {{prix.controle_ratios.part_main_oeuvre_bordereau_entier.constate::n2}} % | **aucun** : la base contient des forfaits aux heures invisibles |

Le calcul **refuse** de rendre un verdict sur les deux dernières lignes, et il le dit dans sa sortie.
Un ratio a un domaine de définition ; l'écrire est la moitié du travail. Le module TV comparait la
dernière ligne à la fourchette de la première.

**Second temps : et pourtant le soupçon tenait.** Sur la bonne base, la part reste de
{{prix.controle_ratios.part_main_oeuvre_beton_arme_decompose.constate::n2}} %, sous la fourchette.
Pour savoir **où**, on retourne chaque cadence d'atelier en **productivité par compagnon** — ce qu'un
homme pose en une journée — et on la compare à ce que le métier constate.

:::figure {"fn":"barres","args":"prix.figures.recalage","titre":"Facteur de recalage par poste : de combien la cadence du planning est optimiste","num":3,"large":true,"options":{"bande":[0.8,1.2],"libelle_bande":"cadence crédible","unite":"facteur (jours-compagnon de référence ÷ jours-compagnon du planning)"},"voir":["Un facteur de 1 veut dire que la cadence du planning demande exactement le travail qu'un compagnon fournit. Au-delà de 1, elle en demande plus : elle est optimiste.","Les {{prix.coherence_cadences.postes_hors_bande.length}} postes sont hors de la bande {{prix.coherence_cadences.bande_de_credibilite.0}}–{{prix.coherence_cadences.bande_de_credibilite.1}}, et c'est pour cela qu'ils sont tous en brique. Le pire est {{prix.coherence_cadences.poste_le_plus_optimiste}}, à ×{{prix.coherence_cadences.facteur_de_recalage_max::n2}} : sa cadence implique de poser {{prix.coherence_cadences.cas.1.metiers.ferraillage_kg.productivite_implicite::n0}} kg d'acier par compagnon et par jour, pour une référence de {{prix.coherence_cadences.cas.1.metiers.ferraillage_kg.fourchette_de_reference.0}} à {{prix.coherence_cadences.cas.1.metiers.ferraillage_kg.fourchette_de_reference.1}}.","Mais ils n'en sortent pas du même côté : {{prix.coherence_cadences.poste_le_plus_prudent}} est à ×{{prix.coherence_cadences.facteur_de_recalage_min::n2}}, c'est-à-dire que sa cadence est au contraire PRUDENTE. Un facteur global unique aurait écrasé cette nuance, et c'est tout l'intérêt de faire le calcul poste par poste : on ne recale pas un chantier, on recale des cadences."],"erreur":"Conclure d'une part de main-d'œuvre globale que « les cadences sont fausses ». C'est une alerte, pas un diagnostic : elle ne dit ni quel poste, ni dans quel sens, ni de combien. Seule une productivité individuelle le dit, parce qu'elle se compare à quelque chose qu'on a vu sur un chantier."}
:::

Facteur moyen : **×{{prix.coherence_cadences.facteur_de_recalage_moyen::n2}}**, obtenu par un chemin
entièrement indépendant de celui qui avait produit le soupçon. Il tombe dans le facteur 2 à 3
annoncé. Ce que cela donne si l'on recale :

| | Référence | Cadences ÷ {{prix.variante_recalee.facteur::n2}} |
|---|---:|---:|
| Durée du chantier | {{prix.variante_recalee.duree_j.reference::n0}} j | **{{prix.variante_recalee.duree_j.recalee::n0}} j** (+{{prix.variante_recalee.duree_j.ecart_pct::n1}} %) |
| Déboursé | {{prix.variante_recalee.debourse_MAD.reference::n0}} MAD | {{prix.variante_recalee.debourse_MAD.recalee::n0}} MAD (+{{prix.variante_recalee.debourse_MAD.ecart_pct::n1}} %) |
| Part de main-d'œuvre du béton armé | {{prix.variante_recalee.part_main_oeuvre_beton_arme_pct.reference::n2}} % | {{prix.variante_recalee.part_main_oeuvre_beton_arme_pct.recalee::n2}} % |

**Une cadence optimiste se paie deux fois** : en heures de main-d'œuvre, et en mois de frais indexés
sur la durée, qui passent de {{prix.variante_recalee.frais_de_duree_MAD.reference::n0}} à
{{prix.variante_recalee.frais_de_duree_MAD.recalee::n0}} MAD. C'est la plus coûteuse des hypothèses
d'un dossier, et c'est aussi celle qu'on vérifie le moins.

Honnêteté sur ce que ce calcul ne fait pas : même recalée, la part de main-d'œuvre
({{prix.variante_recalee.part_main_oeuvre_beton_arme_pct.recalee::n2}} %) reste sous la fourchette.
Le recalage explique l'essentiel de l'écart, pas tout. **La dette n° 10 est chiffrée, elle n'est pas
soldée** : il y faudrait des attachements réels, et le cours n'en a aucun.

### f. La situation de travaux mensuelle

La situation n° {{prix.situation.numero}} de ce chantier. Un chantier ne se paie pas à la fin : il se paie tous les mois, sur **attachement contradictoire**.
L'ordre des opérations n'est pas décoratif — inverser deux lignes change le net à payer.

:::figure {"fn":"sequence","args":"prix.figures.situation","titre":"Le cycle mensuel d'une situation de travaux","num":4,"large":true,"voir":["Le constat contradictoire précède tout : c'est lui qui fixe la quantité payée, et non le métré d'étude. Un métré juste qui n'est pas attaché ne se paie pas.","Entre le dépôt et le paiement, le CPS de cet exemple pose {{gare.prix_unitaires_MAD.contrat.delai_de_paiement_j.valeur}} jours. Ce délai n'est pas une formalité : c'est lui qui crée le besoin de trésorerie du § S4g.","Le visa de la maîtrise d'œuvre porte sur les quantités ET sur la conformité : une situation peut être réduite pour un ouvrage exécuté mais non conforme, et c'est là que le suivi qualité rejoint le suivi financier."],"erreur":"Préparer une situation depuis son métré d'étude et aller la faire signer. Le sens est l'inverse : on constate sur site, on signe l'attachement, et la situation en découle. Une situation qui précède son attachement finit en litige."}
:::

| Ligne | Montant |
|---|---:|
| Travaux cumulés ({{prix.situation.travaux_cumules_pct_du_marche::n1}} % du marché) | {{prix.situation.travaux_cumules_MAD::n0}} MAD |
| Révision des prix (coefficient {{prix.situation.revision.coefficient::n4}}) | + {{prix.situation.revision.revision_MAD::n0}} MAD |
| **Montant révisé** | **{{prix.situation.montant_revise_MAD::n0}} MAD** |
| Retenue de garantie ({{gare.prix_unitaires_MAD.contrat.retenue_de_garantie_pct.valeur}} %) | − {{prix.situation.retenue_retenue_MAD::n0}} MAD |
| Remboursement d'avance ({{prix.situation.fraction_de_remboursement::n3}} de l'avance versée) | − {{prix.situation.avance_remboursee_cumul_MAD::n0}} MAD |
| **Net cumulé à payer** | **{{prix.situation.net_cumule_a_payer_MAD::n0}} MAD** |

La **révision** se vérifie d'abord par une addition : $a + b + c = 1$. Ici
{{prix.situation.revision.a}} + {{prix.situation.revision.b}} + {{prix.situation.revision.c}} =
{{prix.situation.revision.somme_abc::n0}}. Le calcul de ce module **lève une erreur** si ce n'est pas
le cas, et c'est la première chose à vérifier dans un CPS : une somme différente de 1 fausse toutes
les révisions du marché, dans un sens ou dans l'autre, et personne ne s'en aperçoit avant le
décompte final.

{{prix.situation.avertissement_CPS}}

### g. La trésorerie : ce qu'un chantier rentable peut coûter

Les décaissements suivent l'avancement ; les encaissements le suivent **avec un mois de constat, le
délai de paiement, et moins la retenue de garantie**. L'écart entre les deux courbes est ce que
l'entreprise finance.

:::figure {"fn":"tresorerie","args":"prix.figures.tresorerie","titre":"Décaissements et encaissements cumulés, et le besoin de trésorerie","num":5,"large":true,"options":{"besoin_max":{"$":"prix.tresorerie.besoin_maximal_MAD"},"j_max":{"$":"prix.tresorerie.besoin_maximal_au_jour"}},"voir":["L'aire rosée est l'écart entre les deux courbes. Quand la rouge est au-dessus, l'entreprise avance de l'argent au maître d'ouvrage ; quand la bleue repasse devant — ici entre les jours 180 et 230 — c'est l'inverse, et l'avance non encore remboursée y est pour beaucoup. Le besoin de financement est le MAXIMUM de cet écart : {{prix.tresorerie.besoin_maximal_MAD::n0}} MAD au jour {{prix.tresorerie.besoin_maximal_au_jour::n0}}, soit {{prix.tresorerie.besoin_maximal_pct_du_marche::n1}} % du marché. Une moyenne ne dirait rien : c'est la pointe qu'il faut financer.","Le décrochement initial de la courbe bleue est l'avance de {{gare.prix_unitaires_MAD.contrat.avance_pct.valeur}} % : c'est le seul moment où l'entreprise est devant. Elle la rembourse ensuite progressivement, ce qui aplatit la courbe au moment où le chantier dépense le plus.","La courbe bleue est en escalier et la rouge est continue : on dépense tous les jours, on encaisse une fois par mois. C'est cette asymétrie, et non la marge, qui met des entreprises en défaut."],"erreur":"Confondre le besoin de trésorerie et la perte. Un chantier parfaitement rentable peut demander {{prix.tresorerie.besoin_maximal_pct_du_marche::n0}} % de son montant en financement : la marge est au bilan, la trésorerie est à la banque, et ce sont deux questions différentes."}
:::

:::encart {"genre":"note","titre":"Pourquoi la courbe de dépense n'est pas la courbe en S du planning"}
Le module D2 publie une courbe en S **en jours-hommes** : elle mesure le travail. Celle-ci est en
**dirhams**. Les deux ne peuvent pas coïncider, parce que des postes dépensent sans mobiliser
personne sur le chantier — fabrication de la charpente, lots techniques sous-traités — et que
d'autres mobilisent beaucoup pour peu d'argent.

L'écart maximal entre les deux est de
**{{prix.ecart_depense_travail.ecart_maximal.ecart_pts::n1}} points** au jour
{{prix.ecart_depense_travail.ecart_maximal.j::n0}}. Prendre l'une pour l'autre, c'est se tromper
d'un cinquième sur un besoin de financement — la même famille d'erreur que de répartir un avancement
au prorata du temps au lieu de le dériver de l'état physique.
:::

### h. Ce que coûte un mois de retard

| | 1 jour | 1 mois (21 j ouvrés) | 3 mois |
|---|---:|---:|---:|
| Frais indexés sur la durée | {{prix.cout_du_retard.1.frais_de_duree_MAD::n0}} | {{prix.cout_du_retard.21.frais_de_duree_MAD::n0}} | {{prix.cout_du_retard.63.frais_de_duree_MAD::n0}} |
| Pénalités de retard | {{prix.cout_du_retard.1.penalites_MAD::n0}} | {{prix.cout_du_retard.21.penalites_MAD::n0}} | {{prix.cout_du_retard.63.penalites_MAD::n0}} |
| **Total (MAD)** | **{{prix.cout_du_retard.1.total_MAD::n0}}** | **{{prix.cout_du_retard.21.total_MAD::n0}}** | **{{prix.cout_du_retard.63.total_MAD::n0}}** |

Deux choses à retenir, et la seconde est un piège de calcul :

1. **Les pénalités dominent les frais de durée d'un facteur sept.** Le raisonnement « on prendra un
   mois, ça nous coûtera un mois de frais généraux » est faux d'un ordre de grandeur dès qu'un marché
   porte des pénalités journalières.
2. **Les pénalités se comptent en jours calendaires, les frais de durée en jours ouvrés.** Un mois
   ouvré de retard, c'est {{prix.cout_du_retard.21.retard_j_ouvres::n0}} jours de frais mais
   {{prix.cout_du_retard.21.retard_j_calendaires::n1}} jours de pénalité. Confondre les deux
   calendriers sous-estime la pénalité d'un tiers.

## S4b · Les hypothèses de ce chiffrage, déclarées

Aucun bordereau réel n'ayant été fourni, **tout ce qui suit est V3**.

**Les prix de ressource** —
⟦V3|coût horaire d'un manœuvre|32 MAD/h|MAD/h|25 à 40|2026|charges patronales comprises⟧,
⟦V3|coût horaire d'un compagnon|45 MAD/h|MAD/h|35 à 60|2026|même valeur que le prix horaire du module TV, pour que les deux voies de chiffrage soient comparables⟧,
⟦V3|coût horaire d'un compagnon qualifié|58 MAD/h|MAD/h|45 à 75|2026|ferrailleur, coffreur-banche, monteur de charpente, vitrier⟧,
⟦V3|coût horaire d'un chef d'équipe|70 MAD/h|MAD/h|55 à 95|2026⟧,
⟦V3|coût horaire d'un grutier|62 MAD/h|MAD/h|48 à 80|2026|compté dans l'encadrement de chantier, pas dans les ateliers⟧,
⟦V3|béton prêt à l'emploi livré|900 MAD/m³|MAD/m³|800 à 1050|2026|hors pompage et hors mise en œuvre⟧,
⟦V3|acier HA livré façonné|11,5 MAD/kg|MAD/kg|9,5 à 14|2026|hors pose⟧,
⟦V3|amortissement d'une rotation de coffrage|38 MAD/m²|MAD/m²|28 à 55|2026|banche ou table, huile et consommables compris⟧,
⟦V3|amortissement d'une rotation d'étaiement|14 MAD/m²|MAD/m²|9 à 22|2026⟧,
⟦V3|charpente métallique fournie en atelier|28 MAD/kg|MAD/kg|22 à 38|2026|profilés, assemblages, galvanisation et peinture, hors pose⟧,
⟦V3|couverture fournie|520 MAD/m²|MAD/m²|380 à 700|2026|pannes, bac acier, isolant, étanchéité⟧,
⟦V3|mur-rideau vitré fourni|2400 MAD/m²|MAD/m²|1600 à 3600|2026|poste le plus sensible du bordereau : l'étendue dépasse le double⟧,
⟦V3|transport et mise en décharge des déblais|55 MAD/m³|MAD/m³|40 à 80|2026|au m³ foisonné⟧,
⟦V3|location d'une grue à tour|95000 MAD/mois|MAD/mois|70000 à 130000|2026|location nue, montage et grutier comptés à part⟧,
⟦V3|location d'une grue mobile de 200 t|18000 MAD/j|MAD/j|12000 à 28000|2026⟧,
⟦V3|pompe à béton|4200 MAD/j|MAD/j|3000 à 6000|2026⟧,
⟦V3|pelle de 30 t avec conducteur|520 MAD/h|MAD/h|400 à 700|2026⟧,
⟦V3|nacelle|1100 MAD/j|MAD/j|800 à 1600|2026⟧,
⟦V3|vibreur|120 MAD/j|MAD/j|80 à 200|2026⟧.

**La composition d'un atelier et du prix** —
⟦V3|part de compagnons qualifiés dans un atelier|50 %|%|30 à 70|2026|le reste est compté en manœuvres ; un chef d'équipe par atelier⟧,
⟦V3|frais généraux de siège|7 %|%|4 à 10|2026|politique d'entreprise, pas une règle⟧,
⟦V3|provision pour aléas|4 %|%|2 à 8|2026⟧,
⟦V3|marge|6 %|%|2 à 12|2026⟧.

**Les consommations par unité d'ouvrage** —
⟦V3|pertes de béton|5 %|%|3 à 8|2026|fonds de benne, tolérances de coffrage, reprises⟧,
⟦V3|ratio d'acier des semelles|60 kg/m³|kg/m³|45 à 80|2026⟧,
⟦V3|ratio d'acier d'un radier|90 kg/m³|kg/m³|70 à 120|2026⟧,
⟦V3|ratio d'acier d'une dalle pleine|90 kg/m³|kg/m³|70 à 120|2026⟧,
⟦V3|ratio d'acier d'un voile|75 kg/m³|kg/m³|55 à 100|2026⟧,
⟦V3|ratio d'acier d'un poteau|130 kg/m³|kg/m³|100 à 180|2026|un poteau de 9 m est l'élément le plus ferraillé du gros œuvre au m³⟧,
⟦V3|coffrage d'une semelle par m³|2,5 m²/m³|m²/m³|1,8 à 3,4|2026|coffrage bois perdu ou à faible rotation⟧,
⟦V3|coffrage de rive d'un radier|0,15 m²/m²|m²/m²|0,08 à 0,25|2026|un radier est coulé sur béton de propreté : pas de sous-face à coffrer⟧,
⟦V3|coffrage d'un plancher par m² coulé|1,179 m²/m²|m²/m²|1,10 à 1,30|2026|sous-face + joues + fonds de poutres + rives — MESURÉ sur la géométrie du plancher au module TV, pas posé ici ; la fourchette couvre d'autres géométries de plancher⟧,
⟦V3|étaiement par m² de dalle|1,0 m²/m²|m²/m²|1,0 à 1,0|2026|une surface étayée par surface coulée : ce n'est pas une hypothèse, c'est une géométrie⟧,
⟦V3|journées de pompe par m³|0,004 j/m³|j/m³|0,002 à 0,008|2026|une journée de pompe pour environ 250 m³⟧,
⟦V3|journées de vibreur par m³|0,004 j/m³|j/m³|0,002 à 0,008|2026⟧.

**Les productivités de référence**, qui servent à contrôler et jamais à calculer —
⟦V3|ferraillage posé par compagnon et par jour|150 kg/j|kg/j|100 à 250|2026|façonnage exclu, pose et ligature comprises⟧,
⟦V3|coffrage posé par compagnon et par jour|18 m²/j|m²/j|12 à 28|2026|banches ou tables, pose et dépose⟧,
⟦V3|béton mis en œuvre par compagnon et par jour|12 m³/j|m³/j|8 à 20|2026|mise en œuvre, vibration, surfaçage⟧,
⟦V3|terrassement par compagnon et par jour|110 m³/j|m³/j|70 à 180|2026|conduite d'engin et aide au sol⟧.

**Les frais indexés sur la durée** —
⟦V3|encadrement de chantier|180000 MAD/mois|MAD/mois|120000 à 260000|2026|conducteur de travaux, chef de chantier, topographe, qualité, HSE, secrétariat⟧,
⟦V3|base-vie et fonctionnement|35000 MAD/mois|MAD/mois|22000 à 55000|2026⟧,
⟦V3|énergie et divers|18000 MAD/mois|MAD/mois|10000 à 30000|2026⟧.

**Les ratios de contrôle** —
⟦V3|part de main-d'œuvre d'un lot de gros œuvre|20 %|%|15 à 30|2026|du déboursé sec, et sur CE périmètre seulement⟧,
⟦V3|coût tous corps d'état d'un bâtiment voyageurs|11000 MAD/m²|MAD/m²|7000 à 16000|2026|hors VRD et hors interfaces ferroviaires⟧,
⟦V3|part du gros œuvre dans le coût total|30 %|%|22 à 40|2026⟧,
⟦V3|ratio d'acier moyen du gros œuvre|95 kg/m³|kg/m³|70 à 130|2026⟧.

**Les montants forfaitaires** — les douze postes à durée déclarée, de
⟦V3|forfait d'implantation topographique|85000 MAD|MAD|55000 à 130000|2026⟧ à
⟦V3|forfait de second œuvre et lots techniques|14500000 MAD|MAD|9000000 à 22000000|2026|cloisons, plafonds, sols, CVC, électricité, courants faibles, plomberie, ascenseurs, escalators — sous-traité, tout compris⟧,
en passant par
⟦V3|forfait d'installation de chantier|620000 MAD|MAD|420000 à 900000|2026⟧,
⟦V3|forfait de montage et démontage de la grue|240000 MAD|MAD|160000 à 350000|2026⟧,
⟦V3|forfait de soutènement périphérique|3800000 MAD|MAD|2500000 à 5500000|2026|berlinoise et tirants, sous-traité⟧,
⟦V3|forfait d'étanchéité et remblais|1450000 MAD|MAD|950000 à 2100000|2026⟧,
⟦V3|forfait de noyaux et escaliers|2900000 MAD|MAD|2000000 à 4200000|2026⟧,
⟦V3|forfait de marquise en porte-à-faux|1900000 MAD|MAD|1200000 à 2900000|2026⟧,
⟦V3|forfait de raccordement du passage souterrain|2600000 MAD|MAD|1700000 à 3900000|2026|travaux sous consignation : le forfait porte la sujétion de travail en fenêtre⟧,
⟦V3|forfait de quais et équipements|4200000 MAD|MAD|2800000 à 6200000|2026⟧,
⟦V3|forfait d'études et de visa de la charpente|1350000 MAD|MAD|900000 à 2000000|2026|ne consomme aucune heure de chantier et occupe pourtant le chemin critique⟧,
⟦V3|forfait d'essais et de mise en service|680000 MAD|MAD|420000 à 1100000|2026⟧,
⟦V3|forfait de réception et de DOE|190000 MAD|MAD|110000 à 300000|2026⟧,
⟦V3|forfait de séchage avant second œuvre|0 MAD|MAD|0 à 0|2026|zéro dirham et vingt jours de chemin critique : un séchage ne se paie pas, il se subit⟧.

**Les taux contractuels**, qui se lisent dans le CPS et sont posés ici pour faire tourner l'exemple —
⟦V3|avance forfaitaire|10 %|%|0 à 20|2026|remboursée par prélèvement progressif sur les situations⟧,
⟦V3|retenue de garantie|7 %|%|5 à 10|2026|sur chaque situation, plafonnée⟧,
⟦V3|plafond de la retenue de garantie|7 %|%|5 à 10|2026|du montant du marché⟧,
⟦V3|cautionnement définitif|3 %|%|2 à 5|2026⟧,
⟦V3|délai de paiement|60 jours|j|30 à 90|2026|du dépôt de la situation à l'encaissement⟧,
⟦V3|pénalité de retard journalière|1 pour mille|‰|0,5 à 2|2026|du montant du marché, par jour calendaire⟧,
⟦V3|plafond des pénalités|10 %|%|5 à 10|2026⟧,
⟦V3|part fixe de la formule de révision|0,15|—|0,10 à 0,20|2026|part non révisable⟧,
⟦V3|part de l'index bâtiment dans la révision|0,60|—|0,50 à 0,70|2026⟧,
⟦V3|part de l'index acier dans la révision|0,25|—|0,15 à 0,35|2026⟧,
⟦V3|rapport de l'index bâtiment au mois de base|1,062|—|1,00 à 1,15|2026⟧,
⟦V3|rapport de l'index acier au mois de base|1,118|—|1,00 à 1,30|2026|plus volatil que l'index bâtiment⟧.

## S4c · Sécurité : ce qu'un prix décide sans le dire

Ce module ne prescrit aucune opération, mais un prix **décide** des conditions dans lesquelles le
travail sera fait. Le § 3.4 impose de le dire. Les dispositions ci-dessous sont **essentielles et
non exhaustives** ; elles ne remplacent ni le plan de sécurité du chantier, ni les obligations
réglementaires du marché. **Aucune valeur normative n'est donnée** — la phase § 5.0 l'interdit.

| Ce que le prix décide | Le risque quand il est sous-évalué | Disposition essentielle |
|---|---|---|
| Le nombre de **rotations de coffrage et d'étaiement** payées | on décoffre plus tôt pour faire tourner le matériel | le délai de décoffrage est une donnée de résistance, pas d'ordonnancement ; il ne se négocie pas en réunion de prix |
| Les **heures** de l'atelier de levage | on tient la cadence en raccourcissant les temps morts, qui sont les temps de vérification | élingues, zone d'exclusion, abandon par vent fort : ces temps sont dans le prix ou ils ne seront pas pris |
| Le poste **installation de chantier** | protections collectives, accès et éclairage rabotés les premiers, parce qu'ils ne se voient pas dans l'ouvrage fini | les protections collectives ne sont pas une variable d'ajustement du déboursé |
| La ligne **divers de chantier** | nettoyage, rangement et évacuation des gravats disparaissent | un chantier encombré est la première cause de chute de plain-pied |

**Le lien avec tout ce module.** Un bordereau trop serré ne produit pas une perte : il produit de la
**pression sur ce qui ne se voit pas dans l'ouvrage fini**. Le § S4d l'a montré par le calcul — le
sous-détail était {{prix.ecart_des_deux_voies.ecart_pct::n0}} % sous le prix de marché, et ce qui
manquait était exactement la ligne des temps improductifs. Côté maîtrise d'œuvre, c'est une raison
de regarder un prix anormalement bas comme un **risque d'exécution** et non comme une bonne affaire.

## S5 · Erreurs fréquentes, et ce qu'elles coûtent

| Erreur | Comment elle se voit | Ce qu'elle coûte |
|---|---|---|
| Main-d'œuvre estimée à part du planning | le bordereau et le planning n'ont pas la même cadence | deux documents qui se contredisent, et un chantier qui tranche à votre place |
| Heures ajoutées sur un forfait tout compris | la part de main-d'œuvre devient ininterprétable | le double compte, et tous les ratios de contrôle faussés |
| Frais de chantier comptés en postes **et** en pourcentage | un poste « installation » et un taux de 12 % dans le même bordereau | 10 à 15 % de prix en trop, et un marché perdu |
| Métré en m³ en place payé au m³ foisonné, ou l'inverse | le poste transport ne tombe jamais juste | {{gare.planning.ratios_quantites_V3.foisonnement_pct.valeur}} % du poste évacuation |
| Ratio de contrôle appliqué hors de son domaine | une alerte qu'on ne sait pas interpréter | la dette n° 10 de ce projet, et deux modules pour la lever |
| Situation préparée depuis le métré d'étude | l'attachement est signé après coup, ou pas signé | la quantité payée est celle de l'attachement : le reste est un litige |
| Révision appliquée sans vérifier $a+b+c=1$ | rien ne se voit avant le décompte final | toutes les révisions du marché, dans un sens ou dans l'autre |
| Besoin de trésorerie confondu avec la perte | « le chantier est rentable, donc tout va bien » | {{prix.tresorerie.besoin_maximal_pct_du_marche::n0}} % du marché à financer, ici |
| Retard chiffré en frais généraux seuls | on oublie les pénalités, sept fois plus lourdes | {{prix.cout_du_retard.21.penalites_MAD::n0}} MAD par mois ici |

## S6 · Exercices

:::exercice {"titre":"1 · Construire un prix unitaire","niveau":"application"}
Reconstruisez le déboursé sec du m² de voile du niveau technique à partir des seules données :
épaisseur {{gare.planning.ratios_quantites_V3.voile_epaisseur_m.valeur}} m, ratio d'acier
{{gare.prix_unitaires_MAD.coefficients_sous_detail.acier_kg_par_m3.voile.valeur}} kg/m³,
{{gare.prix_unitaires_MAD.coefficients_sous_detail.coffrage_m2_par_unite.voile_par_m2.valeur}} m² de
coffrage par m², cadence d'atelier
{{gare.planning.cadences_chantier_V3.voile_m2_j_atelier.valeur}} m²/j pour
{{gare.planning.effectifs_chantier_V3.compagnons_par_atelier.voiles}} compagnons.

**Corrigé.** Main-d'œuvre : 8 × {{gare.planning.effectifs_chantier_V3.compagnons_par_atelier.voiles}} /
{{gare.planning.cadences_chantier_V3.voile_m2_j_atelier.valeur}} =
**{{prix.bordereau.par_poste.VOIL.main_oeuvre.h_par_unite::n3}} h/m²**, au taux d'atelier de
{{prix.bordereau.par_poste.VOIL.main_oeuvre.taux.taux_MAD_h::n2}} MAD/h, soit
{{prix.bordereau.par_poste.VOIL.main_oeuvre.montant_MAD_par_unite::n2}} MAD. Matériaux :
{{prix.bordereau.par_poste.VOIL.materiaux.0.montant_MAD::n2}} +
{{prix.bordereau.par_poste.VOIL.materiaux.1.montant_MAD::n2}} +
{{prix.bordereau.par_poste.VOIL.materiaux.2.montant_MAD::n2}} MAD. Matériel :
{{prix.bordereau.par_poste.VOIL.materiel.0.montant_MAD::n2}} MAD.
**Déboursé sec : {{prix.bordereau.par_poste.VOIL.debourse_sec_par_unite_MAD::n2}} MAD/m².**

*Le piège : prendre {{gare.prix_unitaires_MAD.ressources.main_oeuvre_MAD_h.compagnon.valeur}} MAD/h
comme taux. C'est le taux d'un compagnon, pas celui d'un atelier qui porte un chef d'équipe et des
compagnons qualifiés. L'écart est de
{{prix.bordereau.par_poste.VOIL.main_oeuvre.taux.taux_MAD_h::n2}} contre
{{gare.prix_unitaires_MAD.ressources.main_oeuvre_MAD_h.compagnon.valeur}} MAD/h — 7 % sur la ligne
main-d'œuvre, et davantage sur un poste de ferraillage.*
:::

:::exercice {"titre":"2 · Doubler les ateliers","niveau":"application"}
Vous passez de {{gare.planning.effectifs_chantier_V3.ateliers_voiles}} à 2 ateliers de voiles.
Que deviennent la durée du poste et son prix unitaire ?

**Corrigé.** La **durée du poste** est divisée par deux, de
{{prix._durees_reference.VOIL::n2}} j à {{prix.exercices.voil_deux_ateliers_j::n2}} j. Le
**prix unitaire ne bouge pas d'un centime** : {{prix.bordereau.par_poste.VOIL.pu_de_vente_MAD::n2}} MAD/m²
dans les deux cas.

C'est l'identité du § S2 : le nombre d'ateliers n'apparaît pas dans h/unité. Deux ateliers font le
même travail en deux fois moins de temps, avec deux fois plus de monde — le total d'heures est
inchangé, donc le coût de main-d'œuvre aussi.

*Ce qui bouge, en revanche : les **frais indexés sur la durée**, si le poste est sur le chemin
critique. Les moyens achètent du délai, et le délai coûte
{{prix.bordereau.frais_de_duree.cout_MAD_par_jour_ouvre::n0}} MAD par jour ouvré. C'est là, et
seulement là, qu'un atelier supplémentaire se rentabilise.*
:::

:::exercice {"titre":"3 · Instruire une alerte de ratio","niveau":"probleme"}
Un contrôle vous signale une part de main-d'œuvre de
{{prix.controle_ratios.part_main_oeuvre_bordereau_entier.constate::n2}} % sur votre bordereau, pour
une fourchette attendue de {{prix.controle_ratios.part_main_oeuvre_beton_arme_decompose.fourchette.0}}
à {{prix.controle_ratios.part_main_oeuvre_beton_arme_decompose.fourchette.1}} %. Que concluez-vous ?

**Corrigé. Rien — pas encore.** Trois questions avant toute conclusion :

1. **Sur quelle base ?** Le bordereau entier contient des fournitures (charpente, façade,
   couverture) qui n'ont aucune heure de chantier, et des forfaits dont les heures existent sans être
   visibles. Le ratio n'y est pas défini. Sur la seule base où il l'est — le béton armé décomposé —
   il vaut {{prix.controle_ratios.part_main_oeuvre_beton_arme_decompose.constate::n2}} %.
2. **Toujours hors fourchette ?** Oui. L'alerte était donc réelle, même si la base était fausse.
3. **Où, et de combien ?** Un ratio global ne le dit pas. En retournant les cadences en
   productivités par compagnon, on trouve
   {{prix.coherence_cadences.postes_hors_bande.length}} postes sur
   {{prix.coherence_cadences.nb_postes::n0}} hors de la bande de crédibilité, un facteur moyen de
   ×{{prix.coherence_cadences.facteur_de_recalage_moyen::n2}} — et un poste, les semelles,
   dont la cadence est au contraire **prudente** (×{{prix.coherence_cadences.cas.0.facteur_de_recalage::n2}}).

*La leçon : un ratio hors fourchette est une **question**, jamais une conclusion. Il ne dit ni quel
poste, ni dans quel sens. Le diagnostic demande de descendre à une grandeur qu'on a déjà vue sur un
chantier — des kilos d'acier par homme et par jour — et c'est pour cela qu'on garde ces ordres de
grandeur en tête.*
:::

:::exercice {"titre":"4 · Trouver les erreurs dans ce sous-détail","niveau":"revue critique"}
Une entreprise vous soumet au visa le sous-détail suivant, pour un m³ de béton armé en voile :

| Ligne | Valeur |
|---|---:|
| Béton prêt à l'emploi | 900 MAD/m³ |
| Acier, 75 kg à 17 MAD/kg | 1 275 MAD |
| Coffrage, 8 m² à 38 MAD | 304 MAD |
| Main-d'œuvre, 1,07 h à 45 MAD | 48 MAD |
| Déboursé sec | 2 527 MAD |
| Frais de chantier 12 % + frais généraux 7 % + marge 6 % | + 631 MAD |
| **Prix de vente** | **3 158 MAD/m³** |

**Quatre choses ne vont pas. Lesquelles ?**

**Corrigé.**

1. **L'acier est payé au prix POSÉ dans un sous-détail qui facture déjà la pose.**
   {{gare.prix_unitaires_MAD.postes.acier_kg.valeur}} MAD/kg est un prix d'acier façonné **et posé** ;
   la fourniture seule vaut {{gare.prix_unitaires_MAD.ressources.materiaux_MAD.acier_ha_kg.valeur}}
   MAD/kg. La main-d'œuvre de ferraillage est comptée deux fois.
2. **Les heures sont celles du m², pas du m³.** 1,07 h est la consommation d'un **m² de voile** ;
   pour un m³, il faut la diviser par l'épaisseur, soit environ
   {{prix.bordereau.par_poste.VOIL.main_oeuvre.h_par_unite::n3}} / {{gare.planning.ratios_quantites_V3.voile_epaisseur_m.valeur}} ≈ 4,3 h/m³.
   L'erreur d'unité la plus commune du sous-détail, et elle fait un facteur 4.
3. **Le coffrage de 8 m²/m³ ne correspond à rien de déclaré.** Pour un voile de
   {{gare.planning.ratios_quantites_V3.voile_epaisseur_m.valeur}} m avec deux faces, c'est 2 /
   {{gare.planning.ratios_quantites_V3.voile_epaisseur_m.valeur}} = 8 m²/m³ — celle-ci est juste, et
   c'est le piège : dans une liste d'erreurs, il y a toujours une ligne correcte, et la refuser coûte
   autant que d'en laisser passer une fausse.
4. **Frais de chantier 12 % *et* une ligne d'installation ailleurs au bordereau** : le double compte
   du § S3b. Il faut demander lequel des deux est en trop — et la réponse n'est pas toujours le
   pourcentage.

*Ce qu'on vise : rien, tant que l'acier n'est pas repris en fourniture seule et que les heures ne
sont pas ramenées au m³. Et on le dit par écrit, avec le calcul, pas « le prix paraît élevé ».*
:::

## S7 · Check-list, glossaire et quiz

**Check-list avant de viser un sous-détail**

1. Les **unités** du métré et du prix sont-elles les mêmes ? (m³ en place ou foisonné, m² de
   parement ou de coffrage, unité ou mètre linéaire)
2. La **main-d'œuvre** vient-elle de la même cadence que le planning, ou a-t-elle été estimée à part ?
3. Les **frais de chantier** sont-ils en postes **ou** en pourcentage — jamais les deux ?
4. Les matériaux sont-ils comptés en **fourniture seule**, la pose étant dans la ligne main-d'œuvre ?
5. Le **taux horaire** est-il celui d'un atelier (avec encadrement et qualifiés), ou celui d'un
   compagnon nu ?
6. Les **ratios de contrôle** sont-ils appliqués sur une base où ils sont définis ?
7. La formule de **révision** vérifie-t-elle $a+b+c=1$, et les index cités existent-ils ?
8. Le **besoin de trésorerie** a-t-il été calculé, et pas seulement la marge ?

**Glossaire**

| | |
|---|---|
| **Déboursé sec** | ce qu'un ouvrage coûte sur le chantier : main-d'œuvre, matériaux, matériel. Ni frais de siège, ni marge |
| **Sous-détail de prix** | la décomposition d'un prix unitaire en ressources et en consommations par unité d'ouvrage |
| **Prix posé** | un prix de marché qui contient déjà la pose, donc la main-d'œuvre. Ne jamais lui ajouter une ligne de main-d'œuvre |
| **Coefficient d'entreprise** | le facteur qui transforme un déboursé sec en prix de vente : frais généraux, aléas, marge |
| **Frais indexés sur la durée** | les coûts qui ne dépendent d'aucune quantité et durent ce que le chantier dure |
| **Attachement** | le constat contradictoire des quantités exécutées, signé sur site. C'est lui qui fait foi, pas le métré |
| **Situation de travaux** | la demande de paiement périodique, établie depuis les attachements |
| **Révision des prix** | l'actualisation contractuelle d'un prix par des index. Sa formule est dans le CPS |
| **Retenue de garantie** | la fraction retenue sur chaque situation et restituée après la garantie |
| **Besoin de trésorerie** | l'écart maximal entre dépenses et encaissements. Ce n'est pas une perte, c'est un financement |

:::exercice {"titre":"Sept questions pour vérifier","niveau":"application"}
**1. Vous doublez les ateliers d'un poste. Son prix unitaire change-t-il ?**
**Non.** Le nombre d'ateliers n'entre pas dans h/unité : il divise la durée et multiplie l'effectif, laissant le total d'heures — donc le coût — inchangé. Ce qui change, c'est le délai, et donc les frais indexés sur la durée si le poste est critique.

**2. Un bordereau porte un poste « installation de chantier » et un taux de frais de chantier de 12 %. Que demandez-vous ?**
Lequel des deux est en trop. Les frais de chantier se comptent **en postes ou en pourcentage**, jamais les deux : c'est un double compte de 10 à 15 % du prix.

**3. Pourquoi ne peut-on pas calculer la part de main-d'œuvre d'un forfait ?**
Parce qu'un forfait est **tout compris** : sa main-d'œuvre y est, mais elle n'est pas visible. On peut l'estimer par ailleurs — le planning donne un effectif — mais on ne peut pas la lire dans le prix, et l'y ajouter la compterait deux fois.

**4. Votre sous-détail tombe {{prix.ecart_des_deux_voies.ecart_pct::n0}} % sous le prix de marché, sur tous les postes. Est-ce une bonne nouvelle ?**
**Non.** Un écart systématique et de même signe n'est pas une dispersion : c'est une ligne qui manque — consommables, nettoyage, reprises, attentes. Ici il faudrait {{prix.ecart_des_deux_voies.divers_necessaire_pct::n1}} % de divers pour recoller. Un prix bas par omission se paie en exécution.

**5. Quelle est la première vérification d'une formule de révision ?**
Que $a+b+c=1$. Une somme différente de 1 fausse **toutes** les révisions du marché, et l'erreur n'apparaît qu'au décompte final.

**6. Le chantier est rentable et vous demandez un découvert. Contradiction ?**
**Non.** La marge est au bilan, la trésorerie est à la banque. On dépense tous les jours et on encaisse une fois par mois, avec {{gare.prix_unitaires_MAD.contrat.delai_de_paiement_j.valeur}} jours de délai et une retenue de garantie : le besoin maximal atteint ici {{prix.tresorerie.besoin_maximal_pct_du_marche::n1}} % du marché.

**7. Un mois de retard, combien ?**
Ici {{prix.cout_du_retard.21.total_MAD::n0}} MAD : {{prix.cout_du_retard.21.frais_de_duree_MAD::n0}} de frais qui continuent de courir, et {{prix.cout_du_retard.21.penalites_MAD::n0}} de pénalités — **sept fois plus**. Et attention au calendrier : les pénalités comptent en jours calendaires, les frais en jours ouvrés.

:::

## S8 · Fiche mémo

:::memo
## Fiche mémo — métrés, prix et situations

**La chaîne d'un prix**

$$ h_{\text{unité}} = \frac{8 \times n_{\text{compagnons}}}{c_{\text{atelier}}} \times k \quad\rightarrow\quad DS = MO + \text{mat.} + \text{matériel} \quad\rightarrow\quad PV = DS \times (1 + f + a + m) $$

Le nombre d'**ateliers** n'y est pas : il achète du délai, pas du prix.

**Trois types de postes, trois familles de durées**

| Durée (D2) | Poste (D1) | Main-d'œuvre |
|---|---|---|
| Calculée | prix unitaire | déduite de la cadence |
| Déclarée | forfait tout compris | présente, **invisible** |
| Imposée | fourniture | chez le fournisseur |

**Les chiffres de ce chantier**

| | |
|---|---:|
| Déboursé sec | {{prix.bordereau.debourse_sec_MAD::n0}} MAD |
| Prix de vente | **{{prix.bordereau.prix_de_vente_MAD::n0}} MAD** |
| Coût au m² d'emprise | {{prix.bordereau.cout_MAD_par_m2_emprise::n0}} MAD/m² |
| Frais indexés sur la durée | {{prix.bordereau.frais_de_duree.cout_MAD_par_mois::n0}} MAD/mois |
| Besoin de trésorerie maximal | {{prix.tresorerie.besoin_maximal_MAD::n0}} MAD ({{prix.tresorerie.besoin_maximal_pct_du_marche::n1}} %) |
| Un mois de retard | {{prix.cout_du_retard.21.total_MAD::n0}} MAD |
| Facteur de recalage des cadences | ×{{prix.coherence_cadences.facteur_de_recalage_moyen::n2}} |

**Les huit réflexes**

1. Vérifier l'**unité** avant le prix : m³ en place ou foisonné, m² de parement ou de coffrage.
2. Déduire la main-d'œuvre de la **cadence du planning**, jamais l'estimer à part.
3. Frais de chantier : **en postes ou en pourcentage**, jamais les deux.
4. Matériaux en **fourniture seule** quand la pose est dans la ligne main-d'œuvre.
5. Taux horaire d'**atelier**, pas de compagnon nu.
6. Un ratio ne se lit que sur la base où il est **défini**.
7. $a+b+c=1$ avant toute révision.
8. Calculer le **besoin de trésorerie**, pas seulement la marge.

**Points d'arrêt côté maîtrise d'œuvre**

Visa d'un sous-détail : unités, double compte, prix posés, taux d'atelier. Visa d'une situation :
attachement signé **avant**, quantités conformes au constat, révision vérifiée, retenue et
remboursement d'avance dans l'ordre. Un prix anormalement bas se traite comme un **risque
d'exécution**, pas comme une bonne affaire.
:::
