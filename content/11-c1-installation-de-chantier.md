---
id: C1
titre: Installation de chantier — couvrir n'est pas lever
fil: Palier 1 · module 11 — exécution et chantier
resume: Un plan d'installation se décide sur trois grandeurs qui ne vont pas dans le même sens : ce que la grue atteint, ce qu'elle peut y poser, et jusqu'où son cercle empiète sur la voie. La première se dessine, la deuxième se calcule, la troisième se négocie.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · cas phare gare · aucune distance de sécurité, aucune règle de survol, aucune surface réglementaire de local social n'est chiffrée
pied: Exemple pédagogique — ne remplace ni un plan d'installation visé, ni une étude de levage, ni un plan de prévention. L'implantation d'une grue au voisinage d'une voie exploitée se décide avec l'exploitant.
donnees: installation, gare, planification, prix
---

## S1 · Ce que ce module fait, et ce qu'il ne peut pas faire

Le plan d'installation est le premier document du chantier et le plus souvent le moins travaillé.
On le dessine en une demi-journée, on y pose une grue au milieu, des baraques dans un coin, et on
n'y revient plus. Il décide pourtant de trois choses qui pèsent toute la durée du chantier : ce que
la grue peut servir, combien de manutentions se font deux fois, et quelle part du coût d'installation
est déjà engagée avant le premier levage.

Ce module traite donc quatre questions **qui se calculent sans aucune norme** :

1. **ce que la grue atteint n'est pas ce qu'elle peut y poser** — une grue qui couvre
   {{installation.couverture.0.couverture_pct::n1}} % de l'emprise n'y sert la pièce la plus lourde
   que sur {{installation.couverture.0.part_servie_pct.Élément de charpente de couverture::n1}} %
   (§ S2) ;
2. **le nombre de grues a trois raisons indépendantes de dépasser un** — le temps, le débit, la
   géométrie — et il faut savoir laquelle tranche, et laquelle n'a pas le droit de voter (§ S3c) ;
3. **le cercle de la flèche atteint le gabarit de la voie dans les
   {{installation.voisinage.lignes.0.variante}}, {{installation.voisinage.lignes.1.variante}} et
   {{installation.voisinage.lignes.2.variante}}** — c'est-à-dire dans toutes, et cet axe-là va en
   sens inverse des deux premiers (§ S3d) ;
4. **le coût d'installation se coupe en trois morceaux et deux horloges** :
   {{installation.cout.part_fixe_pct::n1}} % dépendent d'une décision, le loyer des grues court sur
   les {{installation.cout.duree_de_location_des_grues_mois::n1}} mois du gros œuvre et celui de la
   base-vie sur les {{installation.cout.duree_du_chantier_mois::n1}} mois du chantier (§ S3h).

Ce qu'il ne fait pas, et qui figurait pourtant au sommaire de l'Étape 0 : la centrale à béton sur
site ou le recours au BPE, les circulations et le lavage de roues, les réseaux provisoires. Les deux
premiers se chiffrent avec le bétonnage — c'est le module C3 qui publie la fenêtre de coulage et les
rotations — et avec le matériel (C6) ; les réseaux provisoires n'ont dans ce cours aucune donnée à
lire, et en traiter ici aurait produit un paragraphe de généralités. L'écart avec la fiche d'origine
est écrit dans le sommaire plutôt que tu (D-061).

Ce qu'il ne fait pas non plus : citer une distance de sécurité, une règle de survol, une obligation
de clôture ou de signalisation, une surface réglementaire de local social, une condition
d'implantation vis-à-vis des réseaux. Toutes ces valeurs sont réglementaires ou contractuelles, et elles restent
**⏸**. Ce module donne la géométrie, les débits et les coûts ; la réglementation et le plan HSE
donnent les contraintes. Un plan d'installation complet est l'intersection des deux, et le cours
n'en tient qu'une moitié.

**Comment les chiffres de ce module sont vérifiés.** La couverture n'est pas estimée à l'œil :
l'emprise est échantillonnée au mètre, soit {{installation.couverture.0.points_echantillonnes::n0}}
points par variante, et chaque point retient la grue qui offre la plus grande **charge**, non la plus
proche. Le résultat est étalonné sur des cas à solution fermée
(`calc/etalonnage/installation_cas_ferme.py`) : un disque clippé par un carré, dont l'aire s'écrit
exactement, et deux invariants — deux grues au même endroit couvrent ce que couvre une seule, et deux
grues disjointes couvrent la somme de leurs disques **moins le bâtiment retiré une seule fois**. Ce
second invariant, écrit d'abord sous la forme « le double », a échoué de 100 m² : l'erreur était dans
l'invariant et non dans la fonction, et le cas conservé est celui qui distingue les deux.

**Et les bornes.** Toutes les entrées sont des hypothèses déclarées à fourchette large, donc chaque
résultat est publié **avec ses deux bornes** (D-036). Deux fois dans ce module, les bornes changent
la conclusion plutôt que de l'encadrer : le taux de charge de la grue (§ S3b) et le survol du
gabarit (§ S3d). Une voie de raisonnement dont les bornes enjambent le seuil de décision **ne
tranche pas**, et le module le dit au lieu de retenir sa valeur nominale.

:::encart {"genre":"attente","titre":"Ce que ⏸ veut dire ici, concrètement"}
Ce module calcule qu'aucune des trois variantes n'évite le gabarit de la voie. Il ne dit pas ce qui
est **permis** : les règles de survol d'une voie exploitée, les dispositifs exigés, les distances de
sécurité et les conditions d'autorisation sont réglementaires et contractuelles, et le cours ne les
possède pas. La géométrie dit **que la question se pose, et pour quelles variantes** ; c'est tout, et
c'est déjà ce qu'un chef de projet doit savoir avant de prendre rendez-vous avec l'exploitant.
:::

## S2 · L'idée centrale : couvrir n'est pas lever

Une grue à tour à flèche distributrice se décrit par deux nombres, et le second est celui qu'on
oublie. Le premier est la **charge maximale** : ⟦V3|charge maximale au crochet d'une grue à tour de chantier de bâtiment|8,0 t|t|5,0 à 12,0|2026|abaque de constructeur, pas une norme ; la valeur dépend du modèle loué⟧, tant que le
moment n'est pas atteint. Le second est le **moment maximal de service** :
⟦V3|moment maximal de service de la même grue|200 t·m|t·m|140 à 320|2026|c'est ce nombre, et non la portée, qui dit ce que la grue peut faire au loin⟧.

Au-delà du rayon où la charge maximale est atteinte, la charge disponible vaut

$$ Q(r) = \min\left(Q_{\max},\ \frac{M}{r}\right) \qquad \text{[t]},\ r \text{ en m},\ M \text{ en t}\cdot\text{m} $$

Deux régimes, donc, et un coude entre les deux. Avant le coude, la grue est limitée par son crochet ;
après, par son moment — et la charge décroît comme l'inverse de la portée. Rien d'autre.

Lue dans l'autre sens, la même formule donne le **rayon limite** d'une pièce : la portée au-delà de
laquelle cette pièce ne passe plus.

$$ r_{\lim} = \frac{M}{m} \qquad \text{si } m \le Q_{\max} $$

Et c'est là que le plan d'installation se joue. Sur ce chantier :

| Pièce | Masse | Bornes | Levable jusqu'à |
|---|---:|---:|---:|
| {{installation.pieces.0.piece}} | {{installation.pieces.0.masse_t::n2}} t | {{installation.pieces.0.bornes_t.0::n1}} à {{installation.pieces.0.bornes_t.1::n1}} t | **{{installation.pieces.0.rayon_limite_m::n0}} m** |
| {{installation.pieces.1.piece}} | {{installation.pieces.1.masse_t::n2}} t | {{installation.pieces.1.bornes_t.0::n1}} à {{installation.pieces.1.bornes_t.1::n1}} t | **{{installation.pieces.1.rayon_limite_m::n0}} m** |
| {{installation.pieces.2.piece}} | {{installation.pieces.2.masse_t::n2}} t | {{installation.pieces.2.bornes_t.0::n1}} à {{installation.pieces.2.bornes_t.1::n1}} t | **{{installation.pieces.2.rayon_limite_m::n0}} m** |
| {{installation.pieces.3.piece}} | {{installation.pieces.3.masse_t::n2}} t | {{installation.pieces.3.bornes_t.0::n1}} à {{installation.pieces.3.bornes_t.1::n1}} t | **{{installation.pieces.3.rayon_limite_m::n0}} m** |

Les trois premières masses sont des hypothèses déclarées, et leurs fourchettes sont larges :
⟦V3|masse d'une banche métallique de voile de 3,00 × 2,70 m, passerelle et étais compris|1,4 t|t|0,9 à 2,2|2026|à la portée où elle est posée ; dépend du modèle de banche et de son équipement⟧ pour la banche,
⟦V3|masse d'une table coffrante de plancher levée d'un tenant, étais compris|2,6 t|t|1,6 à 4,0|2026|table de 20 à 25 m² : une table plus grande lève moins souvent, mais plus lourd⟧ pour la table et
⟦V3|masse d'une cage d'armatures de poutre préfabriquée|0,9 t|t|0,4 à 1,8|2026|ordre de grandeur recoupé sur le plan de ferraillage du module B3e, qui publie 1,74 t pour deux poutres de 24 m⟧ pour la cage.
La quatrième n'est pas déclarée ici : c'est le module B7c qui la publie (D-039).

Les trois premières pièces passent partout : leur rayon limite dépasse la plus longue flèche
étudiée, ⟦V3|portée de flèche de la grue de référence — une DÉCISION, pas une hypothèse : on choisit une grue et on la paie|60 m|m|40 à 75|2026|la portée n'a pas de fourchette au sens des autres entrées ; la fourchette donnée ici décrit le choix disponible, pas l'incertitude sur un relevé. Chaque variante de calage déclare la flèche qu'elle emploie : 60 m pour les variantes à une grue, 40 m pour celle à deux⟧.
La **courbe de charge, elle, ne dépend pas de la longueur de la flèche** : elle dépend de la charge
maximale et du moment, qui sont les mêmes. Raccourcir une flèche ne rend pas la grue plus forte au
rayon où elle travaille ; cela réduit seulement le rayon où elle peut aller. La
quatrième — la pièce de charpente de couverture, la plus lourde du chantier, dont la masse est
**publiée par le module B7c et non redéclarée ici** — ne passe plus au-delà de
{{installation.pieces.3.rayon_limite_m::n0}} m — **{{installation.pieces.3.rayon_limite_m::n0}} m sur {{installation.couverture.0.grues.0.portee_m::n0}}**, deux cinquièmes de ce que la grue atteint.

:::figure {"fn":"diagramme","args":"installation.figures.courbe_de_charge","titre":"La courbe de charge : deux régimes et un coude","num":1,"large":true,"options":{"unite":"t","axeX":true,"axeY":true,"uniteX":"portée au crochet, m","depuisZero":true,"marqueur":{"$":"installation.figures.marqueur_charpente"}},"voir":["Le plateau à gauche est le régime de la CHARGE : la grue est limitée par son crochet, et la portée n'y change rien.","La branche décroissante est le régime du MOMENT : la charge disponible vaut M / r, et chaque mètre de plus coûte de la capacité.","Le marqueur est le rayon limite de la pièce de charpente : {{installation.pieces.3.rayon_limite_m::n0}} m pour {{installation.pieces.3.masse_t::n1}} t. Au-delà, cette pièce ne passe plus, alors que la grue y arrive encore.","La courbe ne dit rien de la hauteur sous crochet ni du vent : ce sont deux autres limites, et elles n'apparaissent pas ici."],"erreur":"Lire la portée d'une grue comme sa capacité. « Une grue de 60 m » dit jusqu'où le crochet va, pas ce qu'on peut y accrocher : à {{installation.couverture.0.distance_la_plus_defavorable_m::n0}} m, cette grue tient {{installation.couverture.0.charge_au_point_le_plus_defavorable_t::n2}} t, soit moins de la moitié de sa charge nominale de {{gare.installation.grue.charge_max_t.valeur::n1}} t."}
:::

**Pourquoi cela compte plus qu'il n'y paraît.** Un plan d'installation se vérifie d'habitude sur un
seul critère : est-ce que les cercles couvrent le bâtiment ? Ce critère est celui de la **couverture**,
et il est insuffisant, parce qu'il traite toutes les pièces comme si elles pesaient le même poids.
La question utile est la **part servie** : pour chaque pièce, quelle fraction de l'emprise la grue
peut-elle atteindre *avec cette pièce au crochet*. Ce sont deux grandeurs différentes, la seconde est
toujours inférieure ou égale à la première, et l'écart est d'autant plus grand que la pièce est
lourde.

## S3 · Principes

### a. Trois variantes de calage, trois résultats

Les positions ne sont pas imposées : ce sont des **décisions de calage**, et ce module les compare
au lieu d'en poser une. Le repère a son origine au coin du bâtiment côté ville ; une position
négative en *y* est hors emprise, côté ville.

| Variante | Grues | Couverture | Les trois pièces légères | La pièce de {{installation.pieces.3.masse_t::n1}} t |
|---|---:|---:|---:|---:|
| {{installation.couverture.0.variante}} | {{installation.couverture.0.nb_grues}} | {{installation.couverture.0.couverture_pct::n1}} % | {{installation.couverture.0.part_servie_pct.Banche de voile, 3,00 × 2,70 m::n1}} % | **{{installation.couverture.0.part_servie_pct.Élément de charpente de couverture::n1}} %** |
| {{installation.couverture.1.variante}} | {{installation.couverture.1.nb_grues}} | {{installation.couverture.1.couverture_pct::n1}} % | {{installation.couverture.1.part_servie_pct.Banche de voile, 3,00 × 2,70 m::n1}} % | **{{installation.couverture.1.part_servie_pct.Élément de charpente de couverture::n1}} %** |
| {{installation.couverture.2.variante}} | {{installation.couverture.2.nb_grues}} | {{installation.couverture.2.couverture_pct::n1}} % | {{installation.couverture.2.part_servie_pct.Banche de voile, 3,00 × 2,70 m::n1}} % | **{{installation.couverture.2.part_servie_pct.Élément de charpente de couverture::n1}} %** |

Trois lectures, et la troisième colonne est celle qui décide.

- La variante A couvre presque tout — {{installation.couverture.0.couverture_pct::n1}} % — et c'est
  le plan qu'on dessine spontanément : une grue au milieu d'un bâtiment de
  {{gare.geometrie.emprise_m.0::n0}} × {{gare.geometrie.emprise_m.1::n0}} m. Mais le point le plus
  défavorable y est à {{installation.couverture.0.distance_la_plus_defavorable_m::n1}} m, où la grue
  ne tient plus que {{installation.couverture.0.charge_au_point_le_plus_defavorable_t::n2}} t : la
  pièce de charpente n'y est servie que sur
  {{installation.couverture.0.part_servie_pct.Élément de charpente de couverture::n1}} % de l'emprise.
- La variante B couvre tout et sert cette même pièce sur
  {{installation.couverture.1.part_servie_pct.Élément de charpente de couverture::n1}} %, parce que
  le point le plus défavorable descend à
  {{installation.couverture.1.distance_la_plus_defavorable_m::n1}} m — où la grue tient encore
  {{installation.couverture.1.charge_au_point_le_plus_defavorable_t::n2}} t.
- La variante C, décalée côté ville, ne couvre plus que
  {{installation.couverture.2.couverture_pct::n1}} % de l'emprise, et perd surtout l'essentiel de la
  part servie : {{installation.couverture.2.part_servie_pct.Élément de charpente de couverture::n1}} %
  seulement. On y reviendra au § S3d, parce que c'est aussi la variante la moins intrusive.

:::figure {"fn":"planMasse","args":"installation.figures.plan_masse","titre":"Plan masse de la variante retenue, avec le point le plus défavorable","num":2,"large":true,"options":{"point_defavorable":{"$":"installation.figures.point_defavorable"},"gabarit":{"$":"installation.figures.plan_masse.gabarit"}},"voir":["L'emprise est le rectangle de {{gare.geometrie.emprise_m.0::n0}} × {{gare.geometrie.emprise_m.1::n0}} m ; les cercles sont les portées des grues, et ils sortent largement du bâtiment.","La ligne rouge est le gabarit de la voie, à {{installation.voisinage.y_du_gabarit_m::n0}} m de la façade côté ville. Les deux cercles la franchissent : c'est le § S3d, et il se voit ici avant d'être calculé.","Le point marqué est celui que le calcul désigne comme le plus défavorable : {{installation.figures.point_defavorable.libelle}}. Il est dans un angle, et c'est toujours dans un angle.","La zone grise au centre est l'aire commune aux deux flèches : {{installation.interference.paires.0.aire_commune_m2::n0}} m², {{installation.interference.paires.0.part_de_l_emprise_pct::n1}} % de l'emprise, et les deux crochets y travaillent à la même hauteur (§ S3e).","Les cercles ne sont pas le plan d'installation : ils disent où la grue arrive. Ce qu'elle peut y poser est l'objet de la figure 1.","Ce que ce plan ne montre pas : la parcelle. Le cours ne la déclare pas, et c'est elle qui, sur un chantier réel, limite les aires de stockage."],"erreur":"Valider un plan masse parce que les cercles couvrent le bâtiment. La variante A couvre {{installation.couverture.0.couverture_pct::n1}} % de l'emprise et ne sert la pièce la plus lourde que sur {{installation.couverture.0.part_servie_pct.Élément de charpente de couverture::n1}} % : le dessin est juste, la conclusion est fausse."}
:::

:::figure {"fn":"barres","args":"installation.figures.couverture","titre":"Couvrir et servir : six nombres pour trois variantes","num":3,"large":true,"options":{"unite":"% de l'emprise","legende_alerte":"part servie avec la pièce la plus lourde au crochet"},"voir":["Pour chaque variante, la première barre est ce que la grue ATTEINT, la seconde ce qu'elle peut SERVIR avec la pièce la plus lourde.","L'écart n'est pas un détail de calcul : il va de {{installation.couverture.1.couverture_pct::n1}} contre {{installation.couverture.1.part_servie_pct.Élément de charpente de couverture::n1}} % pour la meilleure variante, à {{installation.couverture.2.couverture_pct::n1}} contre {{installation.couverture.2.part_servie_pct.Élément de charpente de couverture::n1}} % pour la plus mauvaise.","Les trois pièces légères sont servies partout où la grue arrive : pour elles, couvrir et servir sont la même chose. C'est ce qui rend l'erreur si facile — elle ne se voit que sur la pièce lourde.","Aucune variante ne sert la pièce de charpente sur toute l'emprise. Pour y arriver il faudrait un moment de service de {{installation.couverture.1.moment_pour_tout_servir_tm::n0}} t·m dans la variante B — {{installation.couverture.1.rapport_au_moment_disponible::n2}} fois celui de cette grue — et {{installation.couverture.0.moment_pour_tout_servir_tm::n0}} t·m, soit {{installation.couverture.0.rapport_au_moment_disponible::n1}} fois, dans la variante A."],"erreur":"Conclure de la seconde série qu'il faut une grue plus puissante. La pièce de charpente de ce chantier est levée par une grue mobile, sous interception, et non par la grue à tour — c'est le module B7c qui le traite. La part servie sert ici à savoir ce que la grue à tour NE fera PAS."}
:::

### b. Le débit : une seconde voie vers le nombre de grues, qui n'a pas le droit de voter

La géométrie dit combien de grues il faut pour **atteindre** l'ouvrage. Elle ne dit rien de combien
il en faut pour **suivre la cadence**. C'est une seconde question, indépendante, et elle se calcule.

Une grue fait
⟦V3|cycles complets par heure d'une grue à tour en gros œuvre de bâtiment : élingage, montée, orientation, descente, pose, décrochage, retour|7,0|levages par heure|4,0 à 12,0|2026|dépend surtout de la distance et de la préparation au sol, très peu de la grue elle-même⟧
levages complets par heure — élingage, montée, orientation, descente, pose, décrochage, retour —,
travaille {{installation.debit.heures_par_jour::n0}} heures, dont
⟦V3|part des heures de présence réellement passées à lever|65|%|40 à 85|2026|le reste : attentes de l'équipe au sol, repas, vent, maintenance, tâches sans grue. La valeur est en pourcentage dans data/, et son nom le dit : écrite 0,65 et publiée « 65 % », elle mettait au registre un nombre que data/ ne contenait pas⟧ %
à lever. Soit **{{installation.debit.capacite_levages_par_jour::n1}} levages par jour**
({{installation.debit.capacite_bornes.0::n1}} à {{installation.debit.capacite_bornes.1::n1}}).

En face, la demande. Et la première question est : **qu'est-ce qui se lève ?** Pas le parc de
coffrage — le parc déclaré fait {{installation.debit.parc_declare_m2::n0}} m², mais l'essentiel est
immobilisé sur des zones en cure, et une table en cure ne passe pas au crochet. Ce qui se lève à
chaque cycle, c'est le coffrage **d'une zone** : {{installation.debit.coffrage_d_une_zone_m2::n1}} m²
(module C3 et tranche verticale), à la cadence de {{installation.debit.cadence_j::n1}} jours que le
planning tient — soit {{installation.debit.surface_manutentionnee_par_jour_m2::n1}} m² manutentionnés
par jour.

:::encart {"genre":"piege","titre":"Un stock et un flux, tous deux en mètres carrés"}
{{installation.debit._la_zone_et_le_parc}}

{{installation.debit._ce_qui_se_leve_n_est_pas_le_parc}}
:::

Et c'est ici qu'une seconde erreur se glisse presque toujours :

{{installation.debit._pourquoi_deux_levages_par_unite}}

À ⟦V3|surface de coffrage manutentionnée d'un seul levage, banches et tables confondues|10,0 m²|m²|6,0 à 18,0|2026|une table de 25 m² vaut un levage, une banche de 8 m² aussi : la moyenne dépend surtout du ratio voiles / planchers⟧
par levage, le coffrage demande {{installation.debit.levages_de_coffrage_par_jour::n1}} levages par
jour. S'y ajoutent ⟦V3|levages divers quotidiens : armatures, étais, matériel, bennes à gravats, approvisionnements|12 levages/j|levages/j|6 à 25|2026|ils ne figurent sur aucun métré et ils occupent la grue autant que le coffrage⟧,
soit **{{installation.debit.demande_levages_par_jour::n1}} levages par jour**
({{installation.debit.demande_bornes.0::n1}} à {{installation.debit.demande_bornes.1::n1}}).

Le taux de charge nominal est donc de **{{installation.debit.taux_de_charge_pct::n1}} %** : une grue
n'y suffit pas, il en faut {{installation.debit.grues_necessaires_par_le_debit}}. Et ses bornes vont
de {{installation.debit.taux_de_charge_bornes_pct.0::n1}} % à
{{installation.debit.taux_de_charge_bornes_pct.1::n1}} %.

:::encart {"genre":"alerte","titre":"Une voie dont les bornes enjambent le seuil ne tranche pas"}
{{installation.parc_de_grues._une_voie_qui_ne_tranche_pas}}

C'est une règle de ce cours, pas une précaution de style : un raisonnement dont la conclusion change
de côté entre ses deux bornes n'apporte **aucune** information sur la décision. Il peut rester au
dossier comme ordre de grandeur ; il ne peut pas voter.

Et remarquez où tombe la valeur nominale : **du bon côté**. Le débit dit
{{installation.debit.grues_necessaires_par_le_debit}} grues, comme les deux autres voies. C'est
précisément ce qui rend la règle difficile à tenir — il est facile d'écarter une voie qui dérange,
beaucoup moins d'écarter une voie qui confirme. Un faux accord est pourtant pire qu'un désaccord :
il augmente la confiance sans augmenter l'information.
:::

**Ces bornes-là valent-elles quelque chose ?** Elles combinent quatre hypothèses à leur extrême
dans le même sens : c'est une **enveloppe**, pas un intervalle de confiance, et une enveloppe
enjambe presque toujours le seuil. Le contrôle qui décide est donc celui-ci — faire varier **une
seule** hypothèse à la fois, les autres à leur valeur nominale :

| Hypothèse qui varie seule | Taux de charge |
|---|---:|
| {{installation.debit.sensibilite_une_a_une.0.hypothese}} | {{installation.debit.sensibilite_une_a_une.0.taux_min_pct::n1}} à {{installation.debit.sensibilite_une_a_une.0.taux_max_pct::n1}} % |
| {{installation.debit.sensibilite_une_a_une.1.hypothese}} | {{installation.debit.sensibilite_une_a_une.1.taux_min_pct::n1}} à {{installation.debit.sensibilite_une_a_une.1.taux_max_pct::n1}} % |
| {{installation.debit.sensibilite_une_a_une.2.hypothese}} | {{installation.debit.sensibilite_une_a_une.2.taux_min_pct::n1}} à {{installation.debit.sensibilite_une_a_une.2.taux_max_pct::n1}} % |
| {{installation.debit.sensibilite_une_a_une.3.hypothese}} | {{installation.debit.sensibilite_une_a_une.3.taux_min_pct::n1}} à {{installation.debit.sensibilite_une_a_une.3.taux_max_pct::n1}} % |

**Les quatre enjambent 100 %, seules.** Le verdict « cette voie ne tranche pas » ne tient donc pas à
une accumulation de prudences : il tient à chacune des quatre hypothèses prise isolément. Et il dit
du même coup laquelle aller mesurer en premier — celle dont la fourchette est la plus large en
pourcentage de taux de charge.

{{installation.debit._ce_que_valent_les_bornes}}

**Et la pointe.** Un taux de charge moyen ne dit rien du jour où tout tombe ensemble :

{{installation.debit._la_pointe_se_calcule}}

{{installation.debit._ce_que_le_taux_de_charge_cache}}

### c. Trois raisons indépendantes de vouloir plus d'une grue — et trois durées

{{installation.parc_de_grues.la_regle}}

| Voie | Parc | Tranche ? | **Pendant combien de temps** | D'où elle vient |
|---|---:|:---:|---|---|
| **{{installation.parc_de_grues.voies.0.voie}}** | {{installation.parc_de_grues.voies.0.parc}} | oui | {{installation.parc_de_grues.voies.0.duree}} | {{installation.parc_de_grues.voies.0.source}} |
| **{{installation.parc_de_grues.voies.1.voie}}** | {{installation.parc_de_grues.voies.1.parc}} | **non** | {{installation.parc_de_grues.voies.1.duree}} | {{installation.parc_de_grues.voies.1.source}} |
| **{{installation.parc_de_grues.voies.2.voie}}** | {{installation.parc_de_grues.voies.2.parc}} | oui | {{installation.parc_de_grues.voies.2.duree}} | {{installation.parc_de_grues.voies.2.source}} |

Le parc retenu est **{{installation.parc_de_grues.parc_retenu}} grues** : le **maximum** des voies
qui tranchent, jamais leur somme. Les additionner donnerait
{{installation.cout.parc_si_somme_des_voies}} grues sur un chantier qui en demande
{{installation.parc_de_grues.parc_retenu}} — une erreur qui vient d'une confusion entre « trois
raisons » et « trois besoins ».

{{installation.parc_de_grues._ce_que_leur_accord_vaut}}

**Le seuil de la voie « géométrie », lui, est une décision — et elle est écrite.**
{{installation.parc_de_grues._pourquoi_ce_seuil}}

:::encart {"genre":"voir","titre":"Pourquoi deux voies d'accord valent mieux qu'une voie précise"}
Les deux voies qui tranchent ici n'ont **aucun terme commun**. L'une lit un calendrier : deux tâches
servies par la grue se chevauchent, et le conflit ne se résorbe pas dans les marges — c'est le module
D2 qui l'établit, en rejouant le réseau. L'autre lit un plan : un bâtiment de
{{gare.geometrie.emprise_m.0::n0}} m ne tient pas dans un disque de
{{installation.couverture.0.grues.0.portee_m::n0}} m de rayon si la grue est en son centre. Elles
donnent le même nombre sans partager une seule donnée : c'est la définition du contre-calcul
indépendant du § 3.3, et c'est plus solide qu'un seul calcul à trois chiffres significatifs.
:::

**Et la colonne qu'on n'écrit jamais.** Les trois voies ne disent pas seulement *combien* : chacune
dit aussi *pendant combien de temps*, et ce sont trois durées différentes.

:::encart {"genre":"alerte","titre":"Le maximum des voies donne un nombre, jamais une durée"}
{{installation.parc_de_grues._le_maximum_donne_un_nombre_pas_une_duree}}

{{installation.parc_de_grues._ce_que_trois_jours_de_conflit_veulent_dire}}
:::

Autrement dit, sur ce chantier : c'est la **géométrie** qui paie la seconde grue, pas le conflit de
calendrier. Si le bâtiment avait tenu sous un seul cercle, le bon arbitrage pour
{{installation.parc_de_grues.voies.0.duree}} aurait été une grue mobile ou un décalage de tâche —
et le budget d'installation aurait été plus léger de
{{installation.cout.cout_d_une_grue_de_plus_MAD::k}} MAD. Savoir **laquelle des voies paie** est ce
qui distingue un plan d'installation d'une liste de matériel.

### d. Le troisième axe : le cercle de la flèche et le gabarit de la voie

Les deux premiers axes — couvrir, servir — se lisent sur un plan et vont dans le même sens : plus la
grue est au centre et proche, mieux c'est. Le troisième va en sens inverse, et il n'existe que sur un
chantier ferroviaire.

Une grue à tour hors service est mise en **girouette** : la flèche est libérée et tourne au vent,
balayant tout son cercle et non le seul secteur utile. C'est la pratique courante, et ses modalités
— quand, comment, avec quelles vérifications — se lisent dans la notice du constructeur et dans le
marché : **⏸**. Ce qui compte ici est géométrique et ne dépend d'aucune règle : si la flèche est
libre, c'est le **cercle entier** qu'il faut regarder. La question n'est donc pas « survole-t-on la voie
pendant le travail » — on peut s'en abstenir — mais « **le cercle atteint-il le gabarit** ».

Le gabarit de la voie la plus proche est à
{{installation.voisinage.y_du_gabarit_m::n0}} m de la façade côté ville :
{{gare.geometrie.emprise_m.1::n0}} m d'emprise, plus
⟦V3|distance du nu de la façade côté voies au bord du gabarit de la voie la plus proche|12,0 m|m|6,0 à 25,0|2026|trottoir de quai, quai lui-même, puis gabarit : c'est une donnée de site relevée sur le plan de masse de l'exploitant, pas un choix de chantier⟧.

| Variante | Dépassement du gabarit | Bornes | Grues concernées | Famille du module B7c |
|---|---:|---:|---:|---|
| {{installation.voisinage.lignes.0.variante}} | **{{installation.voisinage.lignes.0.survol_du_gabarit_m::n1}} m** | {{installation.voisinage.lignes.0.survol_bornes_m.0::n1}} à {{installation.voisinage.lignes.0.survol_bornes_m.1::n1}} m | {{installation.voisinage.lignes.0.nb_grues_concernees}} | {{installation.voisinage.lignes.0.famille_B7c}} |
| {{installation.voisinage.lignes.1.variante}} | **{{installation.voisinage.lignes.1.survol_du_gabarit_m::n1}} m** | {{installation.voisinage.lignes.1.survol_bornes_m.0::n1}} à {{installation.voisinage.lignes.1.survol_bornes_m.1::n1}} m | {{installation.voisinage.lignes.1.nb_grues_concernees}} | {{installation.voisinage.lignes.1.famille_B7c}} |
| {{installation.voisinage.lignes.2.variante}} | **{{installation.voisinage.lignes.2.survol_du_gabarit_m::n1}} m** | {{installation.voisinage.lignes.2.survol_bornes_m.0::n1}} à {{installation.voisinage.lignes.2.survol_bornes_m.1::n1}} m | {{installation.voisinage.lignes.2.nb_grues_concernees}} | {{installation.voisinage.lignes.2.famille_B7c}} |

{{installation.voisinage.lecture}}

{{installation.voisinage._ce_qui_resiste_aux_bornes}}

:::figure {"fn":"barres","args":"installation.figures.survol","titre":"De combien le cercle de la flèche dépasse le gabarit, par variante","num":4,"large":true,"options":{"unite":"m de dépassement du gabarit de la voie — les trois barres sont positives","origine":0},"voir":["Les trois barres sont positives : les trois variantes atteignent le gabarit, et aucune ne l'évite.","L'ordre est l'INVERSE de celui de la couverture. A couvre bien et dépasse de {{installation.voisinage.lignes.0.survol_du_gabarit_m::n0}} m ; C couvre mal et ne dépasse que de {{installation.voisinage.lignes.2.survol_du_gabarit_m::n0}} m.","Une seule variante atteint le gabarit même avec la distance de site la plus favorable de la fourchette : {{installation.voisinage.variantes_concernees_quelles_que_soient_les_bornes.0}}. Pour les deux autres, la réponse dépend d'un relevé que le cours n'a pas.","Le dépassement se mesure en mètres ; ce qu'il autorise ou interdit ne se mesure pas, et ne se lit ni ici ni dans ce cours — c'est une règle, et elle est en attente."],"erreur":"Traiter ce dépassement comme un problème de travail, à résoudre en limitant la rotation de la flèche pendant les levages. En girouette, la flèche tourne seule : ce qui compte est le cercle entier, et la limitation éventuelle est un dispositif à justifier, pas une consigne de grutier."}
:::

{{installation.voisinage._le_sens_inverse}}

{{installation.voisinage._ce_que_cela_change}}

### e. Deux flèches qui se croisent : ce que la seconde grue n'apporte pas

Décider « deux grues » n'est pas décider « deux fois une grue ». Dans la variante retenue, les deux
cercles se recoupent — on le voit sur la figure 2 — et ce recouvrement se chiffre.

{{installation.interference.lecture}}

| | |
|---|---:|
| Entraxe des deux grues | {{installation.interference.paires.0.entraxe_m::n0}} m |
| Aire commune aux deux cercles | **{{installation.interference.paires.0.aire_commune_m2::n0}} m²** |
| Part de l'emprise concernée | {{installation.interference.paires.0.part_de_l_emprise_pct::n1}} % |
| Hauteur sous crochet déclarée | {{installation.interference.hauteur_sous_crochet_m::n0}} m, **une seule** |

L'aire commune se calcule exactement — c'est la lentille de deux disques sécants, et sa formule
fermée sert d'étalonnage à ce module. Ce qui en découle, en revanche, n'est pas une formule :

:::encart {"genre":"alerte","titre":"Deux grues sécantes ne font pas deux fois une grue"}
{{installation.interference._ce_que_la_geometrie_impose}}
:::

C'est une limite de ce module, et elle est déclarée : le taux de charge du § S3b compare la demande
à **une** grue. Le lecteur qui en déduirait « deux grues, donc
{{installation.debit.capacite_levages_par_jour::n0}} × 2 levages par jour » se tromperait d'autant
plus que les deux flèches se recoupent sur
{{installation.interference.paires.0.part_de_l_emprise_pct::n1}} % de l'emprise — c'est-à-dire sur la
zone centrale, celle où le gros œuvre travaille le plus longtemps.

:::encart {"genre":"attente","titre":"Ce que le cours ne peut pas dire ici"}
{{installation.interference._ce_qui_reste_en_attente}}
:::

### f. La base-vie se dimensionne sur la pointe, pas sur la moyenne

Le planning du module D2 publie, après lissage, un effectif de pointe de
{{installation.base_vie.effectif_de_pointe::n0}} personnes et un effectif moyen de
{{installation.base_vie.effectif_moyen::n1}} — un rapport de
{{installation.base_vie.rapport_pointe_sur_moyen::n2}}. Deux nombres, deux plans d'installation
possibles, et un seul est juste.

{{installation.base_vie._pourquoi_la_pointe}}

À ⟦V3|surface de locaux sociaux par compagnon : réfectoire, vestiaires, sanitaires|4,5 m²/personne|m²/personne|3,0 à 7,0|2026|⚠ les surfaces minimales sont réglementaires (⏸) : cette valeur sert à dimensionner un plan d'installation, pas à justifier une conformité⟧
pour les compagnons et
⟦V3|surface de bureaux de chantier par personne d'encadrement : bureaux, salle de réunion, local de sécurité|9,0 m²/personne|m²/personne|6,0 à 14,0|2026|l'encadrement occupe des bureaux, pas des vestiaires : deux surfaces unitaires, et une part à déclarer⟧,
avec ⟦V3|part de l'effectif de pointe qui occupe des bureaux plutôt que des vestiaires|12 %|%|7 à 20|2026|encadrement de chantier, conducteurs de travaux, bureau de contrôle en visite⟧
d'encadrement :

| | Surface | Modules de {{gare.installation.base_vie.module_m2::n0}} m² |
|---|---:|---:|
| Dimensionnée sur la **pointe** ({{installation.base_vie.effectif_de_pointe::n0}}) | **{{installation.base_vie.surface_necessaire_m2::n1}} m²** ({{installation.base_vie.surface_bornes_m2.0::n0}} à {{installation.base_vie.surface_bornes_m2.1::n0}}) | {{installation.base_vie.modules}} → {{installation.base_vie.surface_installee_m2::n0}} m² |
| Dimensionnée sur la **moyenne** ({{installation.base_vie.effectif_moyen::n1}}) | {{installation.base_vie.surface_si_dimensionnee_sur_la_moyenne_m2::n1}} m² | — |

{{installation.base_vie._l_arrondi_n_est_pas_une_perte}}

:::encart {"genre":"piege","titre":"L'effectif de pointe d'avant lissage n'est pas le bon non plus"}
Le module D2 publie deux pointes : {{installation.base_vie.effectif_de_pointe_avant_lissage::n0}}
avant lissage des ressources, {{installation.base_vie.effectif_de_pointe::n0}} après. C'est la
seconde qu'il faut, parce que c'est le planning qu'on exécute. Prendre la première
surdimensionnerait la base-vie de près d'un tiers — et l'erreur est d'autant plus tentante qu'elle a
l'air prudente. Dimensionner sur un planning qu'on a renoncé à suivre n'est pas de la prudence :
c'est une incohérence entre deux documents du même dossier.
:::

### g. Les aires : ce qui doit être sous la grue, et ce qui n'a pas à y être

Un plan d'installation ne se résume pas à des cercles : il place des **aires**, et chacune porte une
question binaire — doit-elle être dans le rayon de la grue ?

| Aire | Surface | Sous la grue ? |
|---|---:|:---:|
| {{installation.aires.lignes.0.aire}} | {{installation.aires.lignes.0.surface_m2::n0}} m² | oui |
| {{installation.aires.lignes.1.aire}} | {{installation.aires.lignes.1.surface_m2::n0}} m² | oui |
| {{installation.aires.lignes.2.aire}} | {{installation.aires.lignes.2.surface_m2::n0}} m² | **non** |
| {{installation.aires.lignes.3.aire}} | {{installation.aires.lignes.3.surface_m2::n0}} m² *(calculée au § S3f)* | non |
| {{installation.aires.lignes.4.aire}} | {{installation.aires.lignes.4.surface_m2::n0}} m² | oui |

{{installation.aires.lecture}}

{{installation.aires._l_aire_qui_n_est_pas_sous_la_grue}}

{{installation.aires._pourquoi_un_majorant}}

### h. Le coût : un forfait et deux loyers, qui ne comptent pas la même durée

{{installation.cout.lecture}}

Quatre de ses entrées sont des hypothèses déclarées ici :
⟦V3|montage, transport, essais de réception et démontage d'une grue à tour|420 000 MAD|MAD|250 000 à 700 000|2026|coût FIXE, indépendant de la durée de location — et c'est ce qui rend une deuxième grue chère même pour quelques semaines⟧
et
⟦V3|massif de fondation d'une grue à tour, ancrages et démolition en fin de chantier|180 000 MAD|MAD|110 000 à 320 000|2026|coût fixe lui aussi, et il se décide au moment des terrassements : un massif oublié se paie en reprise⟧
par grue,
⟦V3|installation de la base-vie : plateforme, raccordements provisoires eau, électricité et assainissement, clôtures, amenée et repli|260 000 MAD|MAD|150 000 à 450 000|2026|coût fixe, engagé avant le premier levage⟧
pour la base-vie, et
⟦V3|location mensuelle d'un module de base-vie, raccordements et entretien compris|2 600 MAD/mois|MAD/mois|1 600 à 4 200|2026|le loyer d'un module, à multiplier par leur nombre et par la durée du chantier⟧
par module loué. Les loyers mensuels de la grue et de la base-vie, eux, viennent du bordereau du
module D1.

**Et la durée ? Il y en a deux.** C'est le point où ce module s'est trompé lui-même, et la
correction vaut plus que le chiffre : une première version louait les deux grues pendant les
{{installation.cout.duree_du_chantier_mois::n1}} mois du chantier, comme un frais de durée. Or une
grue à tour n'est pas un frais de durée.

| | Durée | Ce qu'elle porte |
|---|---:|---|
| Chantier entier | {{installation.cout.duree_du_chantier_mois::n1}} mois | base-vie, encadrement, gardiennage |
| Fenêtre de la grue | **{{installation.cout.duree_de_location_des_grues_mois::n1}} mois** | les {{installation.cout.nb_grues}} grues à tour |

{{installation.fenetre_de_grue.lecture}}

{{installation.fenetre_de_grue._une_grue_n_est_pas_un_frais_de_duree}}

:::encart {"genre":"voir","titre":"Une seconde voie sur le loyer de la base-vie"}
{{installation.cout._deux_voies_sur_la_base_vie}}
:::

:::figure {"fn":"cascade","args":"installation.figures.cout","titre":"Le coût d'installation en trois marches, et deux durées différentes","num":5,"large":true,"options":{"unite":"k MAD"},"voir":["La première marche est le coût FIXE : montage et démontage des grues, massifs, raccordements, installation de la base-vie. Il se décide une fois, et il pèse {{installation.cout.part_fixe_pct::n1}} % du total.","La deuxième est le loyer des {{installation.cout.nb_grues}} grues, et il ne court que {{installation.cout.duree_de_location_des_grues_mois::n1}} mois — la fenêtre du gros œuvre.","La troisième est le loyer de la base-vie, qui court lui sur les {{installation.cout.duree_du_chantier_mois::n1}} mois du chantier. Deux loyers, deux horloges.","Le total représente {{installation.cout.part_du_marche_pct::n2}} % du marché. Louer les grues sur toute la durée du chantier, comme le fait un modèle de frais de durée, le porterait bien au-delà."],"erreur":"Écrire « coût d'installation » sur une seule ligne du bordereau. Le poste contient alors trois grandeurs qui n'obéissent à rien de commun — une décision, une fenêtre de gros œuvre, une durée de chantier — et plus personne ne sait laquelle on paie quand le chantier glisse."}
:::

{{installation.cout._les_deux_morceaux_n_obeissent_pas_a_la_meme_chose}}

**Où se gagne un mois ?** La question n'a pas une réponse, elle en a deux :

{{installation.cout._ou_se_gagne_un_mois}}

:::encart {"genre":"piege","titre":"Le trou : les grues attendent la marquise"}
{{installation.cout._le_trou}}
:::

{{installation.cout._le_prix_d_une_grue_de_plus}}

:::encart {"genre":"alerte","titre":"Ce module et le module D1 ne comptent pas la même chose"}
{{installation.cout._ce_que_D1_a_budgete}}
:::

## S4 · Étude de cas chiffrée : le dossier d'installation de la gare, de bout en bout

Reprenons les six décisions dans l'ordre où elles se prennent, chacune avec le nombre qui la porte.

**1. Combien de grues ?** {{installation.parc_de_grues.parc_retenu}}, parce que deux voies
indépendantes et sans terme commun le disent (§ S3c), et qu'une troisième — le débit — ne tranche
pas. Coût de la décision : **{{installation.cout.cout_d_une_grue_de_plus_MAD::k}} MAD** pour la
seconde grue sur la fenêtre du gros œuvre — un fixe engagé avant le premier levage, puis un loyer
mensuel pendant {{installation.cout.duree_de_location_des_grues_mois::n1}} mois. Et c'est la voie de
la **géométrie** qui la paie : le conflit de calendrier, lui, ne dure que
{{installation.parc_de_grues.voies.0.duree_j}} jours, et trois jours ne justifient pas le montage
d'une grue à tour.

**2. Où les placer ?** Variante {{installation.figures.plan_masse.variante}} : c'est la seule qui
couvre toute l'emprise, et celle qui sert le mieux la pièce lourde
({{installation.couverture.1.part_servie_pct.Élément de charpente de couverture::n1}} % contre
{{installation.couverture.0.part_servie_pct.Élément de charpente de couverture::n1}} % pour une grue
centrale). Elle n'est pas la moins intrusive vis-à-vis de la voie, et c'est le point qu'il faut
porter à l'exploitant au lieu de le découvrir.

**3. Que ne lèvera-t-on pas avec ces grues ?** La pièce de charpente au-delà de
{{installation.pieces.3.rayon_limite_m::n0}} m, soit sur
{{installation.couverture.1.part_servie_pct.Élément de charpente de couverture::n1}} % de l'emprise
seulement dans la variante retenue. Conséquence directe : la couverture se lève à la grue mobile,
sous interception, et cette décision-là appartient au module B7c — mais elle est **prise ici**, au
plan d'installation, le jour où l'on choisit la grue à tour.

**4. Une grue suit-elle la cadence ?** Nominalement non :
{{installation.debit.demande_levages_par_jour::n1}} levages demandés contre
{{installation.debit.capacite_levages_par_jour::n1}} disponibles, soit
{{installation.debit.taux_de_charge_pct::n1}} %. Mais la réponse n'est pas exploitable comme
décision : ses bornes vont de {{installation.debit.taux_de_charge_bornes_pct.0::n1}} à
{{installation.debit.taux_de_charge_bornes_pct.1::n1}} %, et elles enjambent le seuil. La voie dit
le même nombre que les deux autres, et elle n'a pas pour autant le droit de voter. Ce qu'il faut en retenir n'est pas le
pourcentage : c'est **quelles mesures iraient le resserrer** — le nombre réel de cycles par heure et
le taux d'utilisation effectif, qui se relèvent en une semaine de suivi et valent plus que tout le
calcul.

**5. Quelle base-vie ?** {{installation.base_vie.modules}} modules,
{{installation.base_vie.surface_installee_m2::n0}} m² installés pour
{{installation.base_vie.surface_necessaire_m2::n1}} m² nécessaires, dimensionnés sur la pointe de
{{installation.base_vie.effectif_de_pointe::n0}} et non sur la moyenne de
{{installation.base_vie.effectif_moyen::n1}}.

**6. Combien ça coûte, et à qui le dire ?** {{installation.cout.total_MAD::k}} MAD, soit
{{installation.cout.part_du_marche_signe_pct::n2}} % du prix qu'on signe — ou
{{installation.cout.part_du_marche_pct::n2}} % du bordereau de référence, et il faut dire lequel :

{{installation.cout._deux_bases_de_prix}}

Et une divergence à verser au dossier :

:::encart {"genre":"alerte","titre":"D1 compte une grue sur 29,7 mois, C1 en compte deux sur 5,8"}
{{installation.cout._ce_que_D1_a_budgete}}

Les deux écarts vont en sens inverse — un de plus en nombre, cinq de moins en durée — et le second
l'emporte : **{{installation.cout.ecart_avec_D1_MAD::k}} MAD**, en faveur de ce module. Ce module ne
corrige pas le bordereau de D1 : il **publie l'écart**, le verse en dette, et laisse la correction à
une révision explicite du prix de revient (D-055). Un cours qui réécrirait silencieusement le chiffre
du module précédent perdrait la seule chose qui rend la chaîne vérifiable : l'obligation que deux
modules qui parlent de la même grandeur tombent d'accord, ou disent pourquoi non.

Et notez la direction : c'est le module **le plus tardif** qui corrige à la baisse. Un budget
d'installation se trompe presque toujours dans ce sens — il facture au mois ce qu'il ne sait pas
dater, parce que c'est l'hypothèse prudente. Prudente pour l'offre, chère pour la compétitivité.
:::

## S5 · Erreurs fréquentes

**1. Confondre portée et capacité.** « Une grue de 60 mètres » ne dit rien de ce qu'elle peut poser
à 60 mètres — ici {{installation.couverture.0.charge_au_point_le_plus_defavorable_t::n2}} t, contre
{{installation.pieces.3.masse_t::n1}} t pour la pièce qu'on voudrait y lever. **Symptôme sur
chantier** : une pièce élinguée qui ne décolle pas, ou un grutier qui refuse le levage — et un
planning qui s'arrête pendant qu'on cherche une solution qui n'existe pas.

**2. Valider un plan masse sur la couverture.** Le défaut précédent, à l'échelle du dossier. Les
cercles couvrent le bâtiment, donc le plan est bon. Sauf que la part servie de la pièce la plus
lourde est de {{installation.couverture.0.part_servie_pct.Élément de charpente de couverture::n1}} %
dans la variante qu'on avait spontanément dessinée. **Symptôme** : une grue mobile qu'on n'avait pas
prévue, louée au mois, dans un budget qui ne l'attendait pas.

**3. Additionner les voies au lieu de prendre leur maximum.** Trois raisons de vouloir plus d'une
grue ne font pas trois grues de plus. **Symptôme** : un parc surdimensionné que le contrôle de
gestion découvre au troisième mois, et une installation à {{installation.cout.part_du_marche_si_somme_des_voies_pct::n2}} % du marché au lieu de {{installation.cout.part_du_marche_pct::n2}} % — plus du double, pour des grues qui attendraient.

**4. Confondre le parc de coffrage et ce qui se lève.** Deux fautes se superposent ici, et elles jouent en sens inverse. Un coffrage se pose ET se dépose : deux levages par rotation, et l'oublier divise la demande par deux. Mais le parc n'est pas ce qui se lève : {{installation.debit.parc_declare_m2::n0}} m² possédés pour {{installation.debit.coffrage_d_une_zone_m2::n1}} m² manutentionnés par cycle, le reste étant immobilisé en cure. Prendre le parc pour la zone multiplie la demande par trois. **Symptôme** : une grue saturée les jours de rotation, des équipes qui attendent le
crochet, et une cadence qui dérive sans qu'aucun poste ne paraisse en cause.

**5. Dimensionner la base-vie sur l'effectif moyen.** {{installation.base_vie.surface_si_dimensionnee_sur_la_moyenne_m2::n0}} m²
au lieu de {{installation.base_vie.surface_necessaire_m2::n0}} m². **Symptôme** : le jour de la
pointe, {{installation.base_vie.effectif_de_pointe::n0}} personnes pour un réfectoire de
{{installation.base_vie.effectif_moyen::n0}} — donc des repas pris sur le chantier, des vestiaires
saturés, et une dégradation de la tenue générale qui ne se rattrape pas.

**6. Placer une aire de stockage hors du rayon de la grue qui doit la servir.** La manutention se
fait alors deux fois : une fois pour amener la charge sous la grue, une fois pour la lever.
**Symptôme** : une chargeuse ou un chariot télescopique « en renfort » qui devient permanent, et
dont personne ne sait dire à quelle décision il répond.

**7. Traiter le survol de la voie comme une consigne de grutier.** En girouette, la flèche tourne
seule : c'est le cercle entier qui compte, pas le secteur de travail. **Symptôme** : une
autorisation d'implantation refusée ou conditionnée, découverte après la commande de la grue — donc
un délai d'instruction en plein sur le chemin critique.

**8. Facturer au mois ce qu'on ne sait pas dater.** C'est l'erreur que ce module a commise sur
lui-même : deux grues à tour louées pendant les
{{installation.cout.duree_du_chantier_mois::n1}} mois du chantier, alors qu'elles servent
{{installation.cout.duree_de_location_des_grues_mois::n1}} mois — un rapport de
{{installation.cout.rapport_des_deux_durees::n1}}. **Symptôme** : aucun. C'est ce qui la rend
durable. Un surcoût de durée ne déclenche ni alerte ni dépassement : il se fond dans un poste
forfaitaire que personne ne rapproche d'un calendrier.

:::encart {"genre":"piege","titre":"L'erreur qui ne se voit sur aucun plan : trois grandeurs dans la même ligne"}
Un bordereau qui porte « installation de chantier : {{installation.cout.total_MAD::k}} MAD » en une
seule ligne mélange trois grandeurs qui n'obéissent à rien de commun : une **décision**
({{installation.cout.part_fixe_pct::n1}} % du total), une **fenêtre de gros œuvre**
({{installation.cout.duree_de_location_des_grues_mois::n1}} mois) et une **durée de chantier**
({{installation.cout.duree_du_chantier_mois::n1}} mois). Trois lignes au bordereau, et la discussion
change de sujet : elle passe du prix des grues à la question « quel mois sommes-nous en train de
payer ? », qui est là où elle doit être.
:::

## S6 · Exercices

:::exercice {"titre":"1 · Une grue couvre tout : que peut-elle y poser ?","niveau":"application"}
Une grue de moment de service {{gare.installation.grue.moment_max_tm.valeur::n0}} t·m et de charge
maximale {{gare.installation.grue.charge_max_t.valeur::n1}} t couvre un bâtiment dont le point le
plus éloigné est à {{installation.couverture.0.distance_la_plus_defavorable_m::n0}} m. Peut-elle y
poser une table coffrante de {{installation.pieces.1.masse_t::n1}} t ? Une pièce de charpente de
{{installation.pieces.3.masse_t::n1}} t ?

**Corrigé.** La charge disponible au point le plus éloigné vaut

$$ Q(r) = \min\left(Q_{\max},\ \frac{M}{r}\right) $$

soit, à {{installation.couverture.0.distance_la_plus_defavorable_m::n0}} m : le minimum de
{{gare.installation.grue.charge_max_t.valeur::n1}} t et de
{{gare.installation.grue.moment_max_tm.valeur::n0}} ÷
{{installation.couverture.0.distance_la_plus_defavorable_m::n0}}, c'est-à-dire
**{{installation.couverture.0.charge_au_point_le_plus_defavorable_t::n2}} t**. C'est le second terme
qui gouverne : on est après le coude.

La table de {{installation.pieces.1.masse_t::n1}} t passe : son rayon limite est de
{{installation.pieces.1.rayon_limite_m::n0}} m, bien au-delà. La pièce de charpente ne passe pas :
son rayon limite est de {{installation.pieces.3.rayon_limite_m::n0}} m, et au point considéré la
grue ne tient que {{installation.couverture.0.charge_au_point_le_plus_defavorable_t::n2}} t pour
{{installation.pieces.3.masse_t::n1}} t demandées — il en manque plus de la moitié. **La grue couvre, elle ne sert pas** — et c'est
tout le module en une ligne.

**La question de contrôle** : à quelle portée cette grue tient-elle encore
{{installation.pieces.3.masse_t::n1}} t ? Réponse : **{{installation.pieces.3.rayon_limite_m::n0}} m** sur une portée de
{{installation.couverture.0.grues.0.portee_m::n0}} m, soit deux cinquièmes — et c'est cette fraction
qu'il faut avoir en tête avant de poser une grue sur un plan.
:::

:::exercice {"titre":"2 · Les trois voies disent 2. Combien en commande-t-on, et pour combien de temps ?","niveau":"probleme"}
Le planning dit qu'il faut {{installation.parc_de_grues.voies.0.parc}} grues (deux tâches servies par
la grue se chevauchent sans marge). Le débit dit {{installation.parc_de_grues.voies.1.parc}} (taux de
charge {{installation.debit.taux_de_charge_pct::n1}} %). La géométrie dit
{{installation.parc_de_grues.voies.2.parc}} (le bâtiment ne tient pas dans un disque). Combien de
grues, et pourquoi ?

**Corrigé.** **{{installation.parc_de_grues.parc_retenu}}**, et le raisonnement compte plus que le
nombre.

D'abord, on ne somme pas : les trois voies décrivent le **même** besoin sous trois angles, pas trois
besoins qui s'ajoutent. Les additionner donnerait
{{installation.cout.parc_si_somme_des_voies}} grues, et
{{installation.cout.part_du_marche_si_somme_des_voies_pct::n2}} % du marché en installation.

Ensuite, on écarte la voie du débit — **et c'est le point difficile, parce qu'elle donne le bon
nombre**. Ses bornes vont de {{installation.debit.taux_de_charge_bornes_pct.0::n1}} à
{{installation.debit.taux_de_charge_bornes_pct.1::n1}} % : à la borne basse une grue travaille au
quart de sa capacité, à la borne haute il en faudrait six. Une voie qui dit « 1 » et « 5 » selon la borne ne
dit rien, même quand sa valeur nominale tombe juste. L'écarter quand elle dérange est facile ;
l'écarter quand elle confirme est la vraie discipline.

Restent deux voies, qui donnent toutes deux {{installation.parc_de_grues.parc_retenu}} **sans
partager aucune donnée** : l'une lit un calendrier rejoué, l'autre un plan.

**Et maintenant la seconde moitié de la question, celle qu'on n'écrit jamais : pour combien de
temps ?** Les deux voies ne répondent pas pareil. Le temps demande deux grues
{{installation.parc_de_grues.voies.0.duree}} — trois jours, pendant lesquels on ne monte pas une
grue à tour : on appelle une grue mobile, ou on déplace une tâche. La géométrie, elle, en demande
deux {{installation.parc_de_grues.voies.2.duree}}, soit
{{installation.cout.duree_de_location_des_grues_mois::n1}} mois. **C'est elle qui paie la seconde
grue**, et la facture est de {{installation.cout.cout_d_une_grue_de_plus_MAD::k}} MAD.

Le maximum des voies donne un **nombre**. La **durée**, elle, se lit voie par voie — et prendre en
même temps le plus grand nombre et la plus longue durée est exactement ce qui fait passer un budget
d'installation de {{installation.cout.total_MAD::k}} à plus du double.

**Le piège à voir** : si les deux voies qui tranchent avaient donné des nombres différents, le
maximum resterait la réponse, mais il faudrait écrire **pourquoi** l'autre voie se trompe, ou ce
qu'elle ignore. Un désaccord entre deux voies indépendantes est une information, jamais un détail
d'arrondi.
:::

:::exercice {"titre":"3 · Le relevé qui vaut plus que le calcul","niveau":"probleme"}
Le taux de charge de la grue est de {{installation.debit.taux_de_charge_pct::n1}} %, avec des bornes
de {{installation.debit.taux_de_charge_bornes_pct.0::n1}} à
{{installation.debit.taux_de_charge_bornes_pct.1::n1}} %. Vous avez une semaine de chantier devant
vous et un carnet. Que relevez-vous, et dans quel ordre, pour resserrer ces bornes ?

**Corrigé.** Trois grandeurs portent toute la largeur de la fourchette, et deux d'entre elles se
relèvent sans rien installer.

1. **Le nombre de cycles par heure**, en comptant les levages sur trois plages d'une heure, à des
   moments différents de la journée. L'hypothèse va de 4 à 12 — un facteur 3, soit à elle seule
   l'essentiel de la fourchette. Un comptage d'une heure la ramène à ±15 %.
2. **Le taux d'utilisation**, en relevant les temps morts du crochet sur une demi-journée : attente
   d'élingage, attente d'équipe au sol, repas, vent. L'hypothèse va de 40 à 85 %. C'est le relevé le
   plus pénible et le plus instructif : il ne mesure pas la grue, il mesure la **préparation au
   sol**, qui est la vraie variable.
3. **La surface moyenne manutentionnée par levage**, en notant ce que chaque levage emporte réellement
   pendant une rotation complète de coffrage. L'hypothèse va de 6 à 18 m².

**Ce que l'exercice enseigne.** Un calcul à bornes larges ne se raffine pas en calculant mieux : il
se raffine en **allant mesurer**. Le travail du chef de projet suivi n'est pas de produire un taux
de charge plus précis à partir des mêmes hypothèses — c'est de savoir laquelle des trois mesures
rapporte le plus, et d'envoyer quelqu'un la faire. Ici, c'est la première : un carnet et une heure.
:::

:::exercice {"titre":"4 · Revue critique : un plan d'installation à viser","niveau":"revue"}
Vous êtes en maîtrise d'œuvre. L'entreprise soumet au visa un plan d'installation portant : une grue
à tour au centre de l'emprise, portée {{installation.couverture.0.grues.0.portee_m::n0}} m ; une
aire d'armatures de {{installation.aires.lignes.0.surface_m2::n0}} m² à l'extrémité ouest de la
parcelle, hors cercle ; une base-vie de {{installation.base_vie.surface_si_dimensionnee_sur_la_moyenne_m2::n0}} m²
« dimensionnée sur l'effectif moyen du chantier » ; une note : « la couverture de la grue est de
{{installation.couverture.0.couverture_pct::n1}} %, l'ouvrage est entièrement desservi ». Que
relevez-vous, et dans quel ordre ?

**Corrigé — quatre observations, dont une bloquante.**

**a. Bloquante — « entièrement desservi » est faux.** La couverture est bien de
{{installation.couverture.0.couverture_pct::n1}} %, mais la part servie de la pièce la plus lourde
est de {{installation.couverture.0.part_servie_pct.Élément de charpente de couverture::n1}} %. Le
plan ne dit pas comment se lève la charpente, et c'est une question de méthode qui engage le délai et
le coût. **Demande** : la note de levage des pièces de plus de
{{installation.pieces.3.masse_t::n1}} t, et le moyen associé.

**b. Bloquante — le voisinage de la voie n'est pas traité.** Le cercle de cette grue dépasse le
gabarit de {{installation.voisinage.lignes.0.survol_du_gabarit_m::n0}} m, et il le dépasse même avec
la distance de site la plus favorable. Le plan ne porte ni la mise en girouette, ni la convention
avec l'exploitant. **Demande** : le relevé de la distance au gabarit et la justification du
dispositif — dont les exigences sont ⏸ et relèvent du marché.

**c. Majeure — l'aire d'armatures est hors rayon.** Elle devra être manutentionnée deux fois.
**Demande** : la rapprocher, ou chiffrer le moyen complémentaire et le porter au plan.

**d. Majeure — la base-vie est dimensionnée sur la moyenne.** {{installation.base_vie.surface_si_dimensionnee_sur_la_moyenne_m2::n0}} m²
pour une pointe de {{installation.base_vie.effectif_de_pointe::n0}} personnes, là où le calcul sur la
pointe donne {{installation.base_vie.surface_necessaire_m2::n0}} m². Les surfaces minimales étant
réglementaires (⏸), le visa ne peut pas se prononcer sur la conformité — mais il peut constater
l'incohérence entre le plan et le planning du même dossier, et c'est suffisant pour refuser.

**e. Majeure — la durée de location n'est pas datée.** Le plan chiffre une installation sans dire
*de quand à quand* la grue reste sur site. Le bordereau, lui, la porte en frais de durée sur toute la
durée du chantier. Sur ce chantier l'écart est de
{{installation.cout.ecart_avec_D1_MAD::k}} MAD. **Demande** : la fenêtre d'amenée et de repli de
chaque engin majeur, et son rapprochement avec le planning.

**Ce que la double lecture change.** Côté entreprise, ces cinq points sont des choix d'organisation
qu'on peut assumer. Côté maîtrise d'œuvre, trois d'entre eux sont des **omissions de pièce** : le
plan ne dit pas ce qu'il devrait dire. Un visa ne juge pas d'abord la qualité du choix : il vérifie que le
dossier permet de juger.
:::

## S7 · Check-list, glossaire et quiz

**Check-list : avant de viser un plan d'installation**

1. Pour **chaque pièce** à lever, son rayon limite est-il écrit — et comparé à la position où elle
   doit être posée ?
2. La note dit-elle ce que la grue **ne lèvera pas**, et par quel moyen ces pièces se lèvent ?
3. Le nombre de grues est-il justifié par une voie **nommée** — temps, débit, géométrie — et non par
   l'habitude ?
4. Une voie dont les bornes enjambent le seuil a-t-elle été **écartée explicitement**, ou comptée
   comme si elle tranchait ?
5. Les levages ont-ils été comptés **deux fois par rotation** de coffrage ?
6. La base-vie est-elle dimensionnée sur la pointe du planning **qu'on exécute**, et non sur la
   moyenne ni sur une pointe d'avant lissage ?
7. Chaque aire porte-t-elle la mention « sous la grue : oui / non », et les « oui » tiennent-ils dans
   ce que la grue couvre **hors bâtiment** ?
8. Le cercle de chaque grue atteint-il le gabarit d'une voie, d'un tiers, d'une voirie ? La distance
   a-t-elle été **relevée** ou supposée ?
9. Le coût d'installation est-il coupé en **fixe** et **loyers**, et chaque loyer rattaché à **sa**
   durée — la fenêtre de l'engin, pas la durée du chantier ?
10. Pour chaque engin majeur, la **date d'amenée et de repli** est-elle écrite, et rapprochée du
    planning ?
11. Le nombre de grues du plan est-il le même que celui du bordereau de prix ? Sinon, l'écart est-il
    écrit ?
12. Si deux grues se recoupent : la **surface commune** est-elle chiffrée, et le plan dit-il comment
    l'overlap est organisé ?

**Glossaire**

| Terme | Ce que c'est |
|---|---|
| **Moment de service** | le produit charge × portée que la grue admet, en t·m. C'est lui, et non la portée, qui dit ce qu'elle peut faire au loin |
| **Courbe de charge** | la charge disponible en fonction de la portée : un plateau, un coude, puis une décroissance en M/r |
| **Rayon limite d'une pièce** | M / m : la portée au-delà de laquelle cette pièce ne passe plus |
| **Couverture** | part de l'emprise que la grue **atteint**. Se dessine |
| **Part servie** | part de l'emprise où la grue peut poser **une pièce donnée**. Se calcule, et vaut toujours moins |
| **Girouette** | mise hors service d'une grue à tour, flèche libre au vent : elle balaie tout son cercle, pas le secteur de travail |
| **Famille « à proximité »** | classification du module B7c : pas d'entrée dans le gabarit, mais une défaillance y conduirait. Demande un dispositif, pas une fermeture de voie |
| **Taux d'utilisation** | part des heures de présence réellement passées à lever. Mesure la préparation au sol, pas la grue |
| **Majorant sous grue** | surface couverte hors bâtiment, **sans** limite de parcelle. Insuffisant, il conclut ; suffisant, il ne prouve rien |
| **Frais de durée** | les dépenses proportionnelles au temps — encadrement, base-vie, gardiennage. Elles ne se négocient pas, elles se raccourcissent. Une grue à tour n'en est **pas** une : elle a sa propre fenêtre |
| **Fenêtre d'un engin** | de l'amenée au repli. Se lit dans le planning, jamais dans la durée du marché |
| **Aire commune de deux flèches** | la lentille des deux cercles. Deux grues sécantes à la même hauteur ne travaillent pas simultanément dedans : leur capacité n'est pas la somme des deux |

**Quiz**

**1. Une grue couvre 100 % de l'emprise. Le plan est-il bon ?**
**On ne peut pas le dire.** Il faut la **part servie**, pièce par pièce. Dans la variante retenue de
ce chantier, la couverture est de {{installation.couverture.1.couverture_pct::n1}} % et la part
servie de la pièce la plus lourde de
{{installation.couverture.1.part_servie_pct.Élément de charpente de couverture::n1}} %.

**2. Quel nombre de la fiche technique d'une grue dit ce qu'elle peut faire au loin ?**
**Le moment de service**, en t·m — pas la portée, et pas la charge maximale. La charge disponible
vaut M/r au-delà du coude.

**3. Les trois voies disent {{installation.parc_de_grues.parc_retenu}}. Combien, et pour combien de temps ?**
**{{installation.parc_de_grues.parc_retenu}} grues, pendant
{{installation.cout.duree_de_location_des_grues_mois::n1}} mois.** Le maximum des voies qui tranchent
donne le **nombre** ; la **durée** se lit voie par voie, et c'est la géométrie qui l'impose ici — le
conflit de calendrier, lui, ne dure que {{installation.parc_de_grues.voies.0.duree_j}} jours. Et la
voie du débit ne tranche pas, bien qu'elle donne le même nombre : ses bornes
({{installation.debit.taux_de_charge_bornes_pct.0::n1}} à
{{installation.debit.taux_de_charge_bornes_pct.1::n1}} %) enjambent le seuil.

**4. Un parc de {{installation.debit.parc_declare_m2::n0}} m² tournant en
{{installation.debit.cadence_j::n1}} jours : combien de levages par jour ?**
**La question est piégée deux fois.** Ce qui se lève n'est pas le parc mais le coffrage d'une zone,
{{installation.debit.coffrage_d_une_zone_m2::n1}} m², le reste étant immobilisé en cure. Et chaque
m² se pose ET se dépose : {{installation.debit.surface_manutentionnee_par_jour_m2::n1}} m² par jour
× 2 ÷ {{gare.installation.levages.surface_par_levage_m2.valeur::n0}} m² par levage =
{{installation.debit.levages_de_coffrage_par_jour::n1}} levages, plus
{{installation.debit.levages_divers_par_jour}} divers.

**5. Sur quel effectif dimensionne-t-on la base-vie, et pourquoi ?**
**Sur la pointe du planning exécuté** ({{installation.base_vie.effectif_de_pointe::n0}} ici), parce
qu'une base-vie est une **capacité**, pas un service moyen. Sur la moyenne, elle ferait
{{installation.base_vie.surface_si_dimensionnee_sur_la_moyenne_m2::n0}} m² au lieu de
{{installation.base_vie.surface_necessaire_m2::n0}}.

**6. La variante qui couvre le mieux est-elle la meilleure ?**
**Pas nécessairement.** Sur un chantier ferroviaire, elle est aussi celle qui empiète le plus sur la
voie : {{installation.voisinage.lignes.0.survol_du_gabarit_m::n0}} m de dépassement pour A contre
{{installation.voisinage.lignes.2.survol_du_gabarit_m::n0}} m pour C. Les deux grandeurs vont en sens
inverse, et la seconde ne se calcule pas seule : elle se négocie.

**7. Où se joue le coût d'installation ?**
**À {{installation.cout.part_fixe_pct::n1}} % sur une décision, et pour le reste sur des durées —
mais pas n'importe lesquelles.** Un mois gagné sur le gros œuvre vaut
{{installation.cout.un_mois_gagne_sur_le_gros_oeuvre_MAD::k}} MAD : les grues et la base-vie. Un mois
gagné à la fin n'en vaut que {{installation.cout.un_mois_gagne_a_la_fin_MAD::k}} —
{{installation.cout.rapport_des_deux_mois::n1}} fois moins, parce que les grues sont démontées
depuis longtemps.

:::memo
## Fiche mémo — installation de chantier

**Les trois phrases du module**

> Couvrir n'est pas lever : la part servie d'une pièce vaut toujours moins que la couverture.
> Le maximum des voies donne un NOMBRE de grues ; la DURÉE se lit voie par voie.
> Une voie dont les bornes enjambent le seuil ne tranche pas, même quand elle a raison.

**Les deux formules**

$$ Q(r) = \min\left(Q_{\max},\ \frac{M}{r}\right) \qquad r_{\lim} = \frac{M}{m} $$

**Les chiffres de ce chantier**

| | |
|---|---:|
| Grue : charge max / moment | {{gare.installation.grue.charge_max_t.valeur::n1}} t · {{gare.installation.grue.moment_max_tm.valeur::n0}} t·m |
| Rayon limite de la pièce de {{installation.pieces.3.masse_t::n1}} t | **{{installation.pieces.3.rayon_limite_m::n0}} m** sur {{installation.couverture.0.grues.0.portee_m::n0}} m de portée |
| Variante retenue | {{installation.figures.plan_masse.variante}} |
| Couverture / part servie (pièce lourde) | {{installation.couverture.1.couverture_pct::n1}} % / **{{installation.couverture.1.part_servie_pct.Élément de charpente de couverture::n1}} %** |
| Parc de grues | **{{installation.parc_de_grues.parc_retenu}}** ({{installation.parc_de_grues.nb_voies_qui_tranchent}} voies d'accord sur 3) |
| Taux de charge d'UNE grue | {{installation.debit.taux_de_charge_pct::n1}} % — bornes {{installation.debit.taux_de_charge_bornes_pct.0::n1}} à {{installation.debit.taux_de_charge_bornes_pct.1::n1}} % : **ne tranche pas** |
| Ce qui se lève par cycle | {{installation.debit.coffrage_d_une_zone_m2::n1}} m² (une zone), pas les {{installation.debit.parc_declare_m2::n0}} m² du parc |
| Fenêtre des grues | **{{installation.cout.duree_de_location_des_grues_mois::n1}} mois** sur {{installation.cout.duree_du_chantier_mois::n1}} — rapport {{installation.cout.rapport_des_deux_durees::n1}} |
| Aire commune des deux flèches | {{installation.interference.paires.0.aire_commune_m2::n0}} m², {{installation.interference.paires.0.part_de_l_emprise_pct::n1}} % de l'emprise, même hauteur sous crochet |
| Un mois gagné | {{installation.cout.un_mois_gagne_sur_le_gros_oeuvre_MAD::k}} MAD sur le gros œuvre · {{installation.cout.un_mois_gagne_a_la_fin_MAD::k}} MAD à la fin |
| Base-vie | {{installation.base_vie.modules}} modules, {{installation.base_vie.surface_installee_m2::n0}} m² (pointe {{installation.base_vie.effectif_de_pointe::n0}}) |
| Aires sous grue | {{installation.aires.surface_a_mettre_sous_la_grue_m2::n0}} m² sur {{installation.aires.surface_totale_m2::n0}} m² |
| Survol du gabarit | {{installation.voisinage.lignes.1.survol_du_gabarit_m::n0}} m (variante retenue) — famille « {{installation.voisinage.lignes.1.famille_B7c}} » |
| Coût | **{{installation.cout.total_MAD::k}} MAD** = {{installation.cout.cout_fixe_MAD::k}} fixe + {{installation.cout.loyer_des_grues_MAD::k}} de grues ({{installation.cout.duree_de_location_des_grues_mois::n1}} mois) + {{installation.cout.loyer_de_la_base_vie_MAD::k}} de base-vie ({{installation.cout.duree_du_chantier_mois::n1}} mois) |
| Écart avec le bordereau D1 | {{installation.cout.ecart_avec_D1_MAD::k}} MAD — **en dette** |

**Les neuf contrôles de chantier**

1. Rayon limite écrit pour chaque pièce, comparé à sa position de pose.
2. Ce que la grue ne lèvera pas : nommé, et son moyen chiffré.
3. Ce qui se lève est une ZONE de coffrage, pas le parc — et chaque m² compte deux levages.
4. Base-vie sur la pointe du planning exécuté.
5. Chaque aire : « sous la grue — oui / non ».
6. Distance au gabarit **relevée**, pas supposée.
7. Nombre de grues du plan = nombre de grues du bordereau.
8. **Fenêtre** de chaque engin majeur écrite, et confrontée au planning : une grue n'est pas un
   frais de durée.
9. Deux flèches sécantes : surface commune chiffrée, organisation de l'overlap écrite.

**Points d'arrêt à viser (côté maîtrise d'œuvre)**

Plan d'installation visé avant toute amenée de matériel · note de levage des pièces hors capacité de
la grue à tour · justification du dispositif vis-à-vis de la voie (exigences ⏸) · implantation et
réception du massif de grue · essais et vérification de mise en service de la grue (⏸) · dispositif
entre grues sécantes (⏸) · plan de circulation et de clôture (⏸) · constat d'amenée et de repli de
chaque engin majeur, daté.

**Ce qui reste ⏸**

Distances de sécurité · règles de survol d'une voie exploitée et d'un tiers · obligations de clôture
et de signalisation · surfaces réglementaires des locaux sociaux · conditions d'implantation
vis-à-vis des réseaux · vérifications réglementaires de mise en service des appareils de levage ·
règles d'implantation et dispositifs d'anti-collision entre deux grues à tour.
:::
