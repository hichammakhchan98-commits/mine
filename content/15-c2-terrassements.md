---
id: C2
titre: Terrassements, fouilles et évacuation des terres
fil: Palier 1 · module 15 — exécution, fiche d'expert
resume: Trois côtés de cette fouille se talutent, un se blinde, et ce n'est pas un calcul de stabilité qui le décide : c'est deux mètres de place. Le talus pèse 831 m³ qu'aucune ligne du bordereau ne porte, la méthode des profils les surestime d'une erreur à forme fermée, et la durée du terrassement ne dépend pas de la pelle — elle s'achète au camion.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · niveau [M], fiche d'expert · aucune stabilité de talus, aucun dimensionnement de blindage, aucun rabattement n'est chiffré (⏸ module B2)
pied: Exemple pédagogique — ne remplace ni une étude géotechnique, ni une note de stabilité, ni un plan de blindage visé. La pente admissible d'un talus et le dimensionnement d'un soutènement sont des calculs réglementaires que ce module ne fait pas.
donnees: terrassement, gare, planification
---

## S1 · Ce que ce module calcule, et ce qu'il refuse de calculer

Un terrassement est l'atelier le plus simple du chantier et celui dont la durée est la plus mal
tenue. Il n'a qu'une tâche — déplacer de la terre — et quatre questions qui se répondent par le
calcul :

1. **Jusqu'où la fouille s'ouvre-t-elle en surface ?** Un talus demande du recul, et le recul se
   mesure. Là où il tient, on talute ; là où il ne tient pas, on blinde. Côté par côté.
2. **Combien de terre, exactement ?** Un volume taluté n'est pas un prisme droit, et la méthode que
   tout le monde emploie pour le cuber est fausse — d'une quantité qui a une forme fermée.
3. **Où va-t-elle ?** Décapage, réemploi en remblai, foisonnement, dépôt. Le bilan se boucle, ou
   bien une ligne manque au bordereau.
4. **En combien de temps ?** La pelle charge, les camions roulent, et le plus lent commande. Ce
   n'est presque jamais la pelle.

:::encart {"genre":"alerte","titre":"Ce que ce module ne fait pas, et c'est l'essentiel du sujet"}
**La pente admissible d'un talus est un résultat, pas une hypothèse.** Elle sort d'un calcul de
stabilité qui demande la cohésion, l'angle de frottement, la nappe et une méthode : tout cela est
réglementaire et géotechnique, et reste **⏸** — c'est le module B2. De même le **dimensionnement du
blindage**, la **poussée des terres** et le **rabattement de nappe**.

Ce module calcule ce qu'une pente **donnée** coûte en volume et en emprise, et il le fait avec une
pente déclarée comme hypothèse, pas comme résultat. C'est utile exactement là où ça s'arrête : il
dit si la question se pose, et il la chiffre quand elle se pose.
:::

Une question se referme d'elle-même, et il faut le dire plutôt que de la traiter : **la nappe est à
{{gare.site.options.S1.nappe_m::n0}} m** et la fouille descend à
{{terrassement.geometrie.profondeur_m::n2}} m. Il n'y a **pas de rabattement** sur ce chantier, et
donc pas de pompage d'exhaure, pas de puits, pas de surveillance de piézomètres. Sur un chantier
voisin avec une nappe à 3 m, ce seul paragraphe deviendrait le plus lourd du module.

## S2 · L'idée centrale : un talus se paie en place, et la place se mesure

Un talus de **fruit** $m$ — recul horizontal par mètre de hauteur — sur une fouille de profondeur
$h$ recule de $m \cdot h$ en surface. Il faut y ajouter une **banquette en crête** : la bande qu'on
laisse libre pour circuler, et sur laquelle on ne stocke rien.

$$ \text{recul nécessaire} = m\,h + b $$

Sur cette fouille : {{terrassement.geometrie.fruit::n1}} × {{terrassement.geometrie.profondeur_m::n2}}
+ {{terrassement.geometrie.banquette_m::n1}} = **{{terrassement.geometrie.recul_necessaire_par_cote_m::n1}} m**
⟦V3|largeur libre à laisser en crête d'un talus provisoire|2,0 m|m|1,0 à 3,0|2026|circulation des engins, stockage interdit, distance de la charge au bord. La valeur réglementaire ou contractuelle, s'il en existe une, est ⏸⟧
⟦V3|fruit d'un talus provisoire en limon sableux dense|1,0|sans unité|0,6 à 1,5|2026|recul horizontal par mètre de hauteur. ATTENTION : la pente réellement admissible est un RÉSULTAT de stabilité et relève du module B2 (⏸) — ce fruit est une hypothèse de travail⟧.

On compare ce nombre à la place disponible, côté par côté. C'est tout, et cela tranche :

| Côté | Place disponible | Recul nécessaire | Marge | Mode |
|---|---:|---:|---:|---|
| {{terrassement.geometrie.cotes.0.cote}} | **{{terrassement.geometrie.cotes.0.place_disponible_m::n1}} m** | {{terrassement.geometrie.cotes.0.recul_necessaire_m::n1}} m | **{{terrassement.geometrie.cotes.0.marge_m::n1}} m** | **{{terrassement.geometrie.cotes.0.mode}}** |
| {{terrassement.geometrie.cotes.1.cote}} | {{terrassement.geometrie.cotes.1.place_disponible_m::n1}} m | {{terrassement.geometrie.cotes.1.recul_necessaire_m::n1}} m | +{{terrassement.geometrie.cotes.1.marge_m::n1}} m | {{terrassement.geometrie.cotes.1.mode}} |
| {{terrassement.geometrie.cotes.2.cote}} | {{terrassement.geometrie.cotes.2.place_disponible_m::n1}} m | {{terrassement.geometrie.cotes.2.recul_necessaire_m::n1}} m | +{{terrassement.geometrie.cotes.2.marge_m::n1}} m | {{terrassement.geometrie.cotes.2.mode}} |
| {{terrassement.geometrie.cotes.3.cote}} | {{terrassement.geometrie.cotes.3.place_disponible_m::n1}} m | {{terrassement.geometrie.cotes.3.recul_necessaire_m::n1}} m | +{{terrassement.geometrie.cotes.3.marge_m::n1}} m | {{terrassement.geometrie.cotes.3.mode}} |

{{terrassement.geometrie.lecture}}

:::encart {"genre":"voir","titre":"Ce que la place disponible veut dire côté voies"}
{{terrassement.geometrie.cotes.0._place}}. Ce n'est donc **pas** le gabarit de la voie qui
contraint — il est bien plus loin — mais la **limite de l'emprise des travaux** : au-delà de la
façade côté voies, il y a le trottoir de quai et le quai, qui sont exploités. Un talus qui dépasse
cette limite n'est pas un talus plus large, c'est une intervention sur un ouvrage en service, avec
sa consignation et son autorisation. La géométrie dit que la question ne se pose pas : on blinde.
:::

:::figure {"fn":"sequence","args":"terrassement.figures.sequence","titre":"L'ordre des opérations, et il n'est pas négociable","num":1,"large":true,"voir":["Le blindage du côté voies précède la fouille en pleine masse, et ce n'est pas une préférence : on ne blinde pas une fouille déjà ouverte, on fouille derrière un blindage posé.","Le décapage est une opération à part : il produit de la terre végétale, qui se stocke et se réemploie, et non du déblai à évacuer.","Le réglage du fond de fouille est la dernière opération mécanique ; après elle, le fond ne se circule plus qu'à pied.","La réception du fond de fouille est un POINT D'ARRÊT : la maîtrise d'œuvre constate l'arase, la nature du sol rencontré et l'absence de point faible avant toute mise en œuvre de béton de propreté."],"erreur":"Fouiller d'abord et blinder ensuite parce que « la terre tient bien ». Elle tient jusqu'à ce qu'elle ne tienne plus, sans prévenir, et un blindage se pose depuis le haut, pas depuis le fond d'une fouille ouverte."}
:::

## S3 · Le volume d'un talus, et pourquoi la méthode usuelle est fausse

À la hauteur $y$ au-dessus du fond, la section horizontale d'une fouille talutée mesure
$(L + a\,y)$ par $(W + b\,y)$, où $a$ et $b$ comptent le recul de talus par mètre de hauteur dans
chaque direction — $a = c_L\,m$ avec $c_L$ le nombre de côtés talutés dans la longueur. L'aire est
donc un **polynôme de degré deux** en $y$, et son intégrale est exacte :

$$ V = L\,W\,h + \frac{(L\,b + W\,a)\,h^2}{2} + \frac{a\,b\,h^3}{3} $$

Trois voies, et deux d'entre elles sont exactes :

| Voie | Volume | Écart |
|---|---:|---:|
| **Intégrale exacte** | {{terrassement.cubatures.trois_voies_du_volume_talute.integrale_exacte_m3::n1}} m³ | référence |
| **Formule prismatique** $\frac{h}{6}(A_0 + 4A_m + A_1)$ | {{terrassement.cubatures.trois_voies_du_volume_talute.formule_prismatique_m3::n1}} m³ | **{{terrassement.cubatures.trois_voies_du_volume_talute.ecart_prismatique_exact_m3::n1}} m³** |
| Méthode des profils $\frac{h}{2}(A_0 + A_1)$ | {{terrassement.cubatures.trois_voies_du_volume_talute.methode_des_profils_m3::n1}} m³ | **+{{terrassement.cubatures.trois_voies_du_volume_talute.ecart_profils_exact_m3::n1}} m³** |

{{terrassement.cubatures.trois_voies_du_volume_talute._regle}}

L'erreur de la méthode des profils se démontre en une ligne : la moyenne des aires intègre le terme
quadratique avec un coefficient $\tfrac12$ là où l'intégrale le prend avec $\tfrac13$. L'écart vaut
donc exactement

$$ \frac{a\,b\,h^3}{2} - \frac{a\,b\,h^3}{3} = \frac{a\,b\,h^3}{6} $$

soit {{terrassement.cubatures.trois_voies_du_volume_talute.forme_fermee_de_l_erreur::n2}} m³ ici, et
c'est **exactement** l'écart mesuré. Une première version de ce module publiait $a\,b\,h^3/3$ — le
double — à côté d'un nombre juste : la phrase était fausse et le calcul l'ignorait.

:::encart {"genre":"piege","titre":"0,65 %, et pourquoi ça compte quand même"}
Sur cette fouille l'erreur des profils vaut
{{terrassement.cubatures.trois_voies_du_volume_talute.ecart_profils_pct::n2}} % :
négligeable. Elle croît comme le **cube** de la profondeur et comme le **carré** du fruit. Sur une
fouille de 12 m au fruit 1,5, le même calcul donnerait un écart cent fois plus grand, et
l'évacuation se paie au mètre cube. Retenez la formule prismatique : elle est exacte, elle demande
une aire de plus, et elle ne coûte rien.
:::

## S4 · Le bilan des terres, et la ligne que le bordereau n'a pas

Le décapage et la fouille **verticale** ne sont pas calculés ici : ce sont les quantités du
bordereau de D1, lues telles quelles —
{{terrassement.cubatures.decapage_m3::n0}} m³ et {{terrassement.cubatures.fouille_verticale_m3::n0}} m³.
Un contrôle le vérifie : la quantité FOUI du bordereau **est** le prisme
$L \times W \times h$ de la géométrie, à
{{terrassement.cubatures.controle_la_fouille_verticale_est_le_prisme.ecart_m3::n1}} m³ près.

Ce que C2 ajoute, c'est le reste du bilan :

:::figure {"fn":"barres","args":"terrassement.figures.bilan","titre":"Le bilan des terres, du décapage au dépôt","num":2,"large":true,"options":{"unite":"m³","legende_alerte":"n'a aucune ligne au bordereau"},"voir":["Le talus pèse {{terrassement.cubatures.talus_m3::n0}} m³, soit {{terrassement.cubatures.talus_pct_du_prisme::n1}} % du prisme vertical — et il n'a aucune ligne au bordereau, parce que D1 a cubé la fouille comme un prisme droit.","Le réemploi en remblai retire {{terrassement.cubatures.reutilise_en_remblai_m3::n0}} m³ du volume à évacuer : c'est la seule ligne du bilan qu'on décide, et elle tombe à zéro si le sol est argileux ou pollué.","Le volume transporté ({{terrassement.cubatures.transporte_foisonne_m3::n0}} m³) dépasse le volume au dépôt en place ({{terrassement.cubatures.au_depot_en_place_m3::n0}} m³) de {{terrassement.cubatures.foisonnement_pct::n0}} % : c'est le foisonnement, et c'est lui qu'on paie au transporteur.","Les deux premières barres sont les quantités de D1, les quatre autres sont calculées par C2 à partir d'elles. Aucune n'est saisie."],"erreur":"Payer l'évacuation au mètre cube EN PLACE. Le transporteur facture du foisonné, et l'écart est d'un quart. C'est l'erreur d'unité la plus coûteuse du terrassement, et le bordereau de D1 la traite correctement — son sous-détail porte un coefficient de {{terrassement.cubatures.evacuation_du_bordereau_de_D1.coefficient_du_sous_detail::n2}}."}
:::

Et voici la ligne manquante, chiffrée : **{{terrassement.cubatures.manque_au_bordereau.volume_m3::n0}} m³
de talus**, au prix du poste FOUI
({{terrassement.cubatures.manque_au_bordereau.pu_du_poste_FOUI_MAD_m3::n2}} MAD/m³), soit
**{{terrassement.cubatures.manque_au_bordereau.montant_MAD::k}} MAD**.
{{terrassement.cubatures.manque_au_bordereau._pourquoi}}

:::encart {"genre":"alerte","titre":"Deux erreurs de sens contraire, et un total juste par compensation"}
Le bordereau de D1 facture l'évacuation de
{{terrassement.cubatures.evacuation_du_bordereau_de_D1.volume_facture_foisonne_m3::n0}} m³ foisonnés,
soit {{terrassement.cubatures.evacuation_du_bordereau_de_D1.montant_MAD::k}} MAD. Le bilan de C2 en
trouve {{terrassement.cubatures.transporte_foisonne_m3::n0}} m³, soit
{{terrassement.cubatures.evacuation_du_bordereau_de_D1.montant_de_C2_MAD::k}} MAD — un écart de
{{terrassement.cubatures.evacuation_du_bordereau_de_D1.ecart_MAD::k}} MAD, **en faveur du
chantier**.

{{terrassement.cubatures.evacuation_du_bordereau_de_D1._deux_erreurs_de_sens_contraire}}
:::

Le blindage, lui, se chiffre à part : {{terrassement.geometrie.surface_de_blindage_m2::n0}} m² de
paroi soutenue, soit **{{terrassement.cubatures.cout_du_blindage_MAD::k}} MAD**
⟦V3|blindage provisoire d'une fouille de quelques mètres, posé et replié|850 MAD/m²|MAD/m²|500 à 1 600|2026|le choix du procédé et son dimensionnement sont ⏸ (module B2) : ce prix sert à comparer un ordre de grandeur, pas à chiffrer un marché⟧.
C'est le prix de la place qui manque de deux mètres.

## S5 · La cadence : la pelle charge, les camions roulent

### a. Le débit d'une pelle, et le piège d'unité qui le double

$$ Q_{\text{foisonné}} = V_{\text{godet}} \times k \times \frac{3600}{t_{\text{cycle}}}
   \qquad\qquad Q_{\text{en place}} = \frac{Q_{\text{foisonné}}}{1 + f} $$

Avec un godet de {{terrassement.pelle.godet_m3::n1}} m³
⟦V3|godet de terrassement d'une pelle 30 t|1,8 m³|m³|1,2 à 2,5|2026|volume ras⟧,
un cycle de {{terrassement.pelle.temps_de_cycle_s::n0}} s
⟦V3|temps de cycle complet d'une pelle 30 t en pleine masse|22 s|s|16 à 30|2026|remplissage, relevage, orientation, déversement, retour. Dépend surtout de l'angle d'orientation, très peu de la machine⟧
et un coefficient de remplissage de {{terrassement.pelle.coefficient_de_remplissage::n2}}
⟦V3|coefficient de remplissage d'un godet en terrain foisonné|0,85|sans unité|0,70 à 0,95|2026|part du godet réellement remplie à la reprise⟧ :
**{{terrassement.pelle.debit_foisonne_m3_h::n1}} m³/h foisonnés**, soit
**{{terrassement.pelle.debit_en_place_m3_h::n1}} m³/h en place**.

:::encart {"genre":"piege","titre":"Le godet charge du foisonné, le métré compte de l'en place"}
{{terrassement.pelle._piege}} Un quart d'écart, dans le sens qui flatte : oublier le foisonnement
fait croire à une cadence que la pelle ne tient pas, et le planning bâti dessus est faux de 25 %
dès sa première ligne.
:::

### b. Le cycle d'un camion, et la flotte qu'il impose

| Poste du cycle | Durée | Part |
|---|---:|---:|
| Chargement | {{terrassement.rotation_saturante.temps_de_chargement_min::n2}} min | |
| **Trajet aller-retour** | **{{terrassement.rotation_saturante.temps_de_trajet_aller_retour_min::n1}} min** | **{{terrassement.rotation_saturante.part_du_cycle_en_route_pct::n0}} %** |
| Déchargement | {{terrassement.rotation_saturante.temps_de_dechargement_min::n0}} min | |
| Manœuvre | {{terrassement.rotation_saturante.temps_de_manoeuvre_min::n0}} min | |
| **Cycle complet** | **{{terrassement.rotation_saturante.temps_de_cycle_min::n1}} min** | |

Un camion revient toutes les
{{terrassement.rotation_saturante.temps_de_cycle_min::n0}} minutes et la pelle le charge en
{{terrassement.rotation_saturante.temps_de_chargement_min::n1}}. Le rapport des deux est le nombre de
camions qu'il faut pour que la pelle ne s'arrête jamais :

$$ N_{\text{saturation}} = \frac{t_{\text{cycle}}}{t_{\text{chargement}}} $$

soit {{terrassement.rotation_saturante.temps_de_cycle_min::n1}} ÷
{{terrassement.rotation_saturante.temps_de_chargement_min::n2}} =
{{terrassement.rotation_saturante.flotte_qui_sature_la_pelle_exacte::n2}}, arrondi au-dessus :
**{{terrassement.rotation_saturante.flotte_qui_sature_la_pelle}} camions**.

**Quinze camions pour une pelle.** C'est le chiffre qui surprend, et il ne dépend presque pas de la
machine : il dépend de la **distance au dépôt**
⟦V3|distance du chantier à la décharge autorisée|14 km|km|5 à 35|2026|un seul sens. La fourchette est large parce qu'elle décide de tout : le nombre de camions en est proportionnel⟧
et de la vitesse moyenne
⟦V3|vitesse moyenne d'un camion chargé en milieu périurbain|28 km/h|km/h|18 à 45|2026|arrêts et traversées compris. Jamais la vitesse autorisée⟧,
qui font à eux deux {{terrassement.rotation_saturante.part_du_cycle_en_route_pct::n0}} % du cycle.

:::figure {"fn":"diagramme","args":"terrassement.figures.flotte_vs_distance.points","titre":"Camions nécessaires pour tenir la cadence d'un atelier, selon la distance au dépôt","num":3,"large":true,"options":{"unite":"camions","axeX":true,"uniteX":"distance au dépôt, km","depuisZero":true,"nom":"flotte pour un atelier","marqueur":{"$":"terrassement.figures.flotte_vs_distance.marqueur"}},"voir":["La flotte est proportionnelle à la distance, parce que le trajet est proportionnel à la distance et qu'il fait l'essentiel du cycle. La courbe est une droite, et sa pente est une décision de maître d'ouvrage — le choix du lieu de dépôt.","À la distance retenue, il faut {{terrassement.cadence_declaree.flotte_par_atelier}} camions par atelier, donc {{terrassement.cadence_declaree.flotte_du_chantier}} pour le chantier, puisque D2 en prévoit {{terrassement.cadence_declaree.nb_ateliers::n0}}.","Sur la fourchette déclarée de la distance — 5 à 35 km — la flotte va de 2 à 10 camions. Un facteur CINQ sur un poste de coût, pour une donnée que personne ne vérifie au moment de signer.","Cette courbe se lit aussi à l'envers : si l'on ne dispose que de quatre camions, elle donne la distance maximale du dépôt qui tient la cadence."],"erreur":"Négocier le prix du camion avant d'avoir négocié la distance du dépôt. Le second décide du nombre de camions, donc du coût total, et il se décide une fois pour tout le chantier."}
:::

### c. Ce qui borne vraiment : la cadence tenue

:::figure {"fn":"diagramme","args":"terrassement.figures.cadence_vs_camions.points","titre":"Cadence tenue selon le nombre de camions, et le plafond de la pelle","num":4,"large":true,"options":{"unite":"m³/h en place","axeX":true,"uniteX":"nombre de camions","depuisZero":true,"nom":"cadence tenue","marqueur":{"$":"terrassement.figures.cadence_vs_camions.marqueur"}},"voir":["La cadence croît LINÉAIREMENT avec le nombre de camions, puis plafonne : au-delà de {{terrassement.rotation_saturante.flotte_qui_sature_la_pelle}} camions, c'est la pelle qui borne et un camion de plus ne sert à rien.","Le plafond est à {{terrassement.pelle.debit_en_place_m3_h::n0}} m³/h en place — le débit de la pelle. Tant qu'on est à gauche du marqueur, la durée du terrassement s'ACHÈTE : un camion de plus, c'est {{terrassement.rotation_retenue.cadence_tenue_m3_h_en_place::n0}} ÷ {{terrassement.rotation_retenue.nb_camions}} ≈ 13 m³/h de plus.","À la flotte retenue ({{terrassement.cadence_declaree.flotte_par_atelier}} camions par atelier), la pelle n'est employée qu'à {{terrassement.rotation_retenue.taux_d_emploi_de_la_pelle_pct::n0}} % : elle attend ses camions les deux tiers du temps. C'est normal, et c'est économique — un camion coûte moins cher qu'une pelle.","C'est la seule tâche du chantier dont la durée se règle par une variable continue. Partout ailleurs, accélérer demande une équipe de plus, un coffrage de plus, une grue de plus."],"erreur":"Dimensionner la flotte sur le débit de la PELLE au lieu de la cadence demandée. Ici cela ferait acheter {{terrassement.rotation_saturante.flotte_qui_sature_la_pelle}} camions au lieu de {{terrassement.cadence_declaree.flotte_par_atelier}}, pour une cadence dont le planning n'a pas besoin."}
:::

## S6 · La cadence déclarée par D2, relue par la rotation

Le module D2 calcule la durée du terrassement par « volume ÷ (cadence d'atelier × nombre
d'ateliers) », soit {{terrassement.cadence_declaree.cadence_d_atelier_m3_j::n0}} m³/j ×
{{terrassement.cadence_declaree.nb_ateliers::n0}} ateliers =
**{{terrassement.cadence_declaree.cadence_du_chantier_m3_j::n0}} m³/j**. La note de cette cadence dit
« pelle 30 t + rotation de camions, **trajet court** », sans chiffrer ni la flotte ni le trajet.
C2 les chiffre : {{terrassement.cadence_declaree._note_trajet_court}}

**Trois conséquences, et aucune n'était écrite.**

| | |
|---|---|
| **{{terrassement.cadence_declaree.flotte_du_chantier}} camions** sont nécessaires | {{terrassement.cadence_declaree.flotte_par_atelier}} par atelier, et aucun module ne les porte au budget |
| La pelle est employée à **{{terrassement.cadence_declaree.taux_d_emploi_de_la_pelle_a_cette_cadence_pct::n1}} %** | la cadence déclarée est trois fois sous le débit de la machine : ce n'est pas la pelle qui fixe la durée |
| **{{terrassement.cadence_declaree.nb_ateliers::n0}} ateliers, c'est {{terrassement.cadence_declaree.nb_ateliers::n0}} pelles** | et le module C6 n'en compte qu'une |

### Le talus allonge la tâche, et cela ne coûte aucun jour

Le volume que D2 a cubé est {{terrassement.cadence_declaree.volume_que_D2_a_cube_m3::n0}} m³ ; le
volume réel, talus compris, est {{terrassement.cadence_declaree.volume_reel_avec_talus_m3::n0}} m³.
À la même cadence, la tâche passe de
{{terrassement.cadence_declaree.duree_declaree_par_D2_j::n2}} à
**{{terrassement.cadence_declaree.duree_avec_le_talus_j::n2}} jours**, soit
+{{terrassement.cadence_declaree.allongement_j::n2}} j.

{{terrassement.cadence_declaree._perimetre}}

:::encart {"genre":"voir","titre":"Deux ateliers, donc deux pelles : l'écart avec C6"}
{{terrassement.cadence_declaree.deux_pelles._pourquoi}}

Chiffré : C6 compte {{terrassement.cadence_declaree.deux_pelles.heures_comptees_par_C6_h::n1}} h de
pelle sur ces deux tâches, il en faut
{{terrassement.cadence_declaree.deux_pelles.heures_reelles_h::n1}} — soit
**{{terrassement.cadence_declaree.deux_pelles.ecart_MAD::k}} MAD**, ou
{{terrassement.cadence_declaree.deux_pelles.part_du_cout_pelle_de_C6_pct::n1}} % du coût de pelle que
C6 publie. Ce n'est pas une faute de C6 : son modèle déduit les heures d'un engin des **jours** de
ses tâches, et il n'a nulle part la notion de **nombre de machines par famille**. La correction
appartient à C6, et elle est inscrite en dette.
:::

## S7 · Sécurité des fouilles, et double lecture

### Sécurité — dispositions essentielles

Une fouille de {{terrassement.geometrie.profondeur_m::n2}} m tue par **ensevelissement**, et presque
toujours de la même façon : un homme au fond, un talus qui part sans bruit, et un volume de terre
dont une fraction de mètre cube suffit à immobiliser une poitrine. Les dispositions ci-dessous sont
les dispositions **de principe** ; les exigences réglementaires — profondeur à partir de laquelle un
blindage est obligatoire, distances imposées, obligations de contrôle — relèvent de la
réglementation du travail et du plan HSE du chantier, et restent **⏸**.

1. **Personne au fond d'une fouille non protégée.** Soit la paroi est blindée, soit elle est talutée
   à une pente justifiée par un calcul — et ce calcul n'est pas dans ce module.
2. **La banquette en crête est une zone interdite au stockage et au stationnement.** Une charge en
   crête, c'est une surcharge sur le talus ; un engin en crête, c'est une surcharge qui vibre.
   {{terrassement.geometrie.banquette_m::n1}} m ici, et ils ne servent qu'à circuler.
3. **Des accès aménagés**, échelles ou rampes, en nombre suffisant et jamais à plus de quelques
   mètres d'un point de travail : une fouille dont on ne sort pas vite est une fouille dont on ne
   sort pas.
4. **Le balisage de la crête**, et la séparation des circulations d'engins et de piétons — c'est le
   plan d'installation du module C1 qui la porte.
5. **Une surveillance après chaque pluie et après chaque gel**, parce qu'un talus stable ne reste
   pas stable : l'eau change tout, et c'est le seul paramètre qui bouge tout seul.
6. **Les réseaux existants repérés et sondés avant tout engin**, à la main si nécessaire. Le
   terrassement est l'atelier qui coupe les réseaux, et un réseau coupé sur une emprise ferroviaire
   est un incident d'exploitation.

### Double lecture

**Côté entreprise.** Lire la place disponible avant de choisir le mode de soutènement, négocier la
distance du dépôt avant le prix du camion, dimensionner la flotte sur la **cadence demandée** et non
sur le débit de la pelle, et cuber le talus — il est à déblayer, à charger, à transporter et à
payer.

**Côté maîtrise d'œuvre.** Trois contrôles, et ils se font tous sur des pièces :

1. **L'adéquation de la flotte à la cadence du planning visé.** Le planning suppose
   {{terrassement.cadence_declaree.cadence_du_chantier_m3_j::n0}} m³/j ; l'entreprise doit montrer
   les {{terrassement.cadence_declaree.flotte_du_chantier}} camions, et le calcul de la figure 3 est
   celui qui le vérifie en deux minutes.
2. **La cohérence du métré avec la géométrie réelle de la fouille.** Un métré établi sur un prisme
   vertical alors que la fouille est talutée est un métré minorant de
   {{terrassement.cubatures.talus_pct_du_prisme::n1}} % — et c'est un attachement que l'on signe.
3. **Le point d'arrêt du fond de fouille** : arase, nature du sol rencontrée comparée à la
   reconnaissance, absence de point faible. C'est le seul moment où l'on voit le sol sur lequel on
   va construire, et il est irréversible — après, il y a du béton de propreté.

## S8 · Check-list, glossaire et quiz

**Check-list : avant d'ouvrir une fouille**

1. La **place disponible** est-elle mesurée côté par côté, et comparée au recul nécessaire ?
2. Le **fruit** retenu vient-il d'un calcul de stabilité, ou est-ce une hypothèse ? (Si c'est une
   hypothèse, elle est à faire confirmer.)
3. La **banquette en crête** est-elle comptée dans le recul, et matérialisée sur le terrain ?
4. Le **blindage** est-il posé **avant** la fouille qu'il soutient ?
5. La **nappe** est-elle au-dessus ou au-dessous du fond de fouille ? (Ici :
   {{gare.site.options.S1.nappe_m::n0}} m contre {{terrassement.geometrie.profondeur_m::n2}} m.)
6. Le **talus est-il cubé** dans le métré, ou la fouille a-t-elle été cubée comme un prisme ?
7. Le volume d'évacuation est-il compté en **foisonné** ?
8. Le **réemploi en remblai** est-il décidé, et sur quel critère de sol ?
9. La **distance au dépôt** est-elle une donnée confirmée, et la **flotte** dimensionnée dessus ?
10. La flotte est-elle dimensionnée sur la **cadence demandée** et non sur le débit de la pelle ?
11. Les **réseaux** sont-ils repérés et sondés ?
12. Le **point d'arrêt du fond de fouille** est-il au plan de contrôle, avec son délai de
    convocation ?

**Glossaire**

| Terme | Ce que c'est |
|---|---|
| **Fruit** | recul horizontal d'un talus par mètre de hauteur. 1/1 = 45°. Ce n'est pas une hypothèse de confort : c'est un résultat de stabilité (⏸ B2) |
| **Banquette en crête** | bande libre en haut d'un talus, interdite au stockage. S'ajoute au recul |
| **Foisonnement** | augmentation de volume d'un sol remanié. {{terrassement.cubatures.foisonnement_pct::n0}} % ici. Le transport se facture en foisonné, le métré se compte en place |
| **Formule prismatique** | $\frac{h}{6}(A_0 + 4A_m + A_1)$. **Exacte** pour une fouille talutée |
| **Méthode des profils** | $\frac{h}{2}(A_0 + A_1)$. Surestime de $a\,b\,h^3/6$ |
| **Flotte de saturation** | nombre de camions au-delà duquel la pelle devient la contrainte : $t_{\text{cycle}} / t_{\text{chargement}}$ |
| **Cadence tenue** | le MINIMUM du débit de la pelle et du débit de la rotation. Jamais la pelle seule |
| **Point d'arrêt du fond de fouille** | constat contradictoire de l'arase et du sol avant béton de propreté. Irréversible |

**Quiz**

**1. Pourquoi le côté voies de cette fouille se blinde-t-il ?**
**Parce qu'il n'y a que {{terrassement.geometrie.cotes.0.place_disponible_m::n1}} m de place** et
qu'un talus en demande {{terrassement.geometrie.cotes.0.recul_necessaire_m::n1}}. Ce n'est pas un
problème de stabilité du sol — c'est un problème de place, et il se tranche sur un plan.

**2. La fouille fait {{terrassement.geometrie.longueur_m::n0}} × {{terrassement.geometrie.largeur_m::n0}} × {{terrassement.geometrie.profondeur_m::n2}} m. Le volume est-il {{terrassement.cubatures.fouille_verticale_m3::n0}} m³ ?**
**Non : {{terrassement.cubatures.trois_voies_du_volume_talute.integrale_exacte_m3::n0}} m³.** Les
trois côtés talutés ajoutent {{terrassement.cubatures.talus_m3::n0}} m³, soit
{{terrassement.cubatures.talus_pct_du_prisme::n1}} %. Le prisme vertical est le volume d'une fouille
blindée sur ses quatre côtés, et de rien d'autre.

**3. Quelle méthode de cubature employer, et laquelle éviter ?**
La **formule prismatique**, exacte ici. Éviter la **méthode des profils**, qui surestime de
$a\,b\,h^3/6$ — négligeable sur cette fouille
({{terrassement.cubatures.trois_voies_du_volume_talute.ecart_profils_pct::n2}} %), lourde dès que la
profondeur grandit, puisque l'erreur croît comme son cube.

**4. La pelle sort {{terrassement.pelle.debit_foisonne_m3_h::n0}} m³/h. Combien de mètres cubes de métré par heure ?**
**{{terrassement.pelle.debit_en_place_m3_h::n0}} m³/h**, pas
{{terrassement.pelle.debit_foisonne_m3_h::n0}}. Le godet charge du foisonné, le métré compte de
l'en place, et le rapport est le foisonnement.

**5. Combien de camions pour que cette pelle ne s'arrête jamais, et pourquoi n'en prend-on que {{terrassement.cadence_declaree.flotte_par_atelier}} ?**
**{{terrassement.rotation_saturante.flotte_qui_sature_la_pelle}}**, parce que le cycle d'un camion
({{terrassement.rotation_saturante.temps_de_cycle_min::n0}} min) vaut
{{terrassement.rotation_saturante.flotte_qui_sature_la_pelle_exacte::n1}} fois son chargement. On
n'en prend que {{terrassement.cadence_declaree.flotte_par_atelier}} parce que la cadence **demandée**
par le planning est trois fois plus faible que le débit de la pelle : saturer la machine
coûterait dix camions pour une durée dont personne n'a besoin.

**6. Le talus ajoute {{terrassement.cadence_declaree.allongement_j::n2}} jour à la tâche. Combien de jours de chantier cela coûte-t-il ?**
**Aucun.** La tâche porte {{terrassement.cadence_declaree.marge_totale_de_FOUI_j::n1}} jours de marge
totale : l'allongement s'y absorbe. Ce qu'il coûte est un **volume**, et le volume se paie à
l'évacuation — {{terrassement.cubatures.manque_au_bordereau.montant_MAD::k}} MAD. Confondre les deux
périmètres ferait annoncer un retard qui n'existe pas.

:::memo
## Fiche mémo — terrassements et évacuation

**Les trois phrases du module**

> Le mode de soutènement se décide à la place disponible, pas à la nature du sol — et la place se
> mesure côté par côté.
> Un volume taluté se cube par la formule prismatique ; la méthode des profils surestime de a·b·h³/6.
> La durée d'un terrassement s'achète au camion, jamais à la pelle.

**Les quatre formules**

$$ \text{recul} = m\,h + b \qquad\qquad
   V = L W h + \frac{(Lb + Wa)h^2}{2} + \frac{a\,b\,h^3}{3} $$

$$ Q_{\text{pelle}} = \frac{V_{\text{godet}}\,k\,3600}{t_{\text{cycle}}} \qquad\qquad
   N_{\text{sat}} = \frac{t_{\text{cycle}}}{t_{\text{chargement}}} $$

avec $a = c_L m$ et $b = c_W m$ (nombre de côtés talutés × fruit), et la cadence tenue =
$\min(Q_{\text{pelle}},\ N \cdot C / t_{\text{cycle}})$.

**Les chiffres de ce chantier**

| | |
|---|---:|
| Fouille | {{terrassement.geometrie.longueur_m::n0}} × {{terrassement.geometrie.largeur_m::n0}} × {{terrassement.geometrie.profondeur_m::n2}} m |
| Recul nécessaire par côté | **{{terrassement.geometrie.recul_necessaire_par_cote_m::n1}} m** ({{terrassement.geometrie.fruit::n1}} × {{terrassement.geometrie.profondeur_m::n2}} + {{terrassement.geometrie.banquette_m::n1}}) |
| Modes | {{terrassement.geometrie.nb_cotes_talutes}} côtés talutés, {{terrassement.geometrie.nb_cotes_blindes}} blindé ({{terrassement.geometrie.surface_de_blindage_m2::n0}} m², {{terrassement.cubatures.cout_du_blindage_MAD::k}} MAD) |
| Prisme / volume taluté | {{terrassement.cubatures.fouille_verticale_m3::n0}} / **{{terrassement.cubatures.trois_voies_du_volume_talute.integrale_exacte_m3::n0}} m³** (+{{terrassement.cubatures.talus_pct_du_prisme::n1}} %) |
| Talus **hors bordereau** | {{terrassement.cubatures.manque_au_bordereau.volume_m3::n0}} m³ = **{{terrassement.cubatures.manque_au_bordereau.montant_MAD::k}} MAD** |
| Bilan : en place / réemployé / transporté | {{terrassement.cubatures.volume_en_place_m3::n0}} / {{terrassement.cubatures.reutilise_en_remblai_m3::n0}} / **{{terrassement.cubatures.transporte_foisonne_m3::n0}} m³** |
| Évacuation | {{terrassement.cubatures.cout_evacuation_MAD::k}} MAD à {{terrassement.cubatures.prix_evacuation_MAD_m3_foisonne::n0}} MAD/m³ foisonné |
| Pelle : foisonné / en place | {{terrassement.pelle.debit_foisonne_m3_h::n0}} / {{terrassement.pelle.debit_en_place_m3_h::n0}} m³/h |
| Cycle camion / flotte de saturation | {{terrassement.rotation_saturante.temps_de_cycle_min::n0}} min dont {{terrassement.rotation_saturante.part_du_cycle_en_route_pct::n0}} % de route / **{{terrassement.rotation_saturante.flotte_qui_sature_la_pelle}} camions** |
| Flotte retenue | **{{terrassement.cadence_declaree.flotte_du_chantier}} camions** ({{terrassement.cadence_declaree.flotte_par_atelier}} × {{terrassement.cadence_declaree.nb_ateliers::n0}} ateliers), pelle à {{terrassement.cadence_declaree.taux_d_emploi_de_la_pelle_a_cette_cadence_pct::n1}} % |
| Durée : D2 / avec le talus | {{terrassement.cadence_declaree.duree_declaree_par_D2_j::n2}} / {{terrassement.cadence_declaree.duree_avec_le_talus_j::n2}} j, pour {{terrassement.cadence_declaree.marge_totale_de_FOUI_j::n1}} j de marge |
| Nappe | {{gare.site.options.S1.nappe_m::n0}} m — **aucun rabattement** |

**Les six réflexes**

1. Mesurer la place côté par côté **avant** de parler de stabilité.
2. Poser le blindage avant de fouiller derrière lui.
3. Cuber par la formule prismatique, et compter le talus.
4. Compter l'évacuation en **foisonné**.
5. Négocier la distance du dépôt avant le prix du camion.
6. Dimensionner la flotte sur la cadence **demandée**, puis vérifier que la pelle suit.

**Ce qui reste ⏸**

Stabilité des talus et pente admissible · dimensionnement du blindage et poussée des terres ·
rabattement de nappe · profondeur réglementaire d'obligation de blindage · distances imposées en
crête · obligations de contrôle et de vérification des fouilles. Tout cela est le module **B2** et
le plan HSE.
:::
