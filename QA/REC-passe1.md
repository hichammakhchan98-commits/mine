# Passe adversariale « /devil » — module REC (Réception, DOE, garanties)

Relecteur hostile, indépendant de l'auteur. Cahier des charges : `CLAUDE.md` § 3.2, § 3.3, § 5.0,
§ 7.2, § 12.2 et Annexe 4. Décisions opposées au module : D-036, D-037, D-039 à D-044, D-049 à
D-055.

Pièces examinées : `content/09-rec-reception-doe-garanties.md`,
`modules/09-rec-reception-doe-garanties.html`, les **trois captures ouvertes et regardées**,
`calc/reception.py`, `calc/etalonnage/reception_cas_ferme.py`, `calc/tests/test_reception.py`,
`calc/verif_unites.py` (section reception), `calc/sorties/reception.json`, les blocs `reception` et
`prix_unitaires_MAD.contrat` de `data/projet-gare.json`, et les sorties héritées `prix.json` (D1) et
`planification.json` (D2).

**Chaîne automatique : verte.** `test_reception.py` « tous verts », étalonnage « tous les cas fermés
vérifiés », vérification dimensionnelle « tout est homogène ». Aucun des huit bloquants ci-dessous
n'a été vu par elle. C'est la sixième passe consécutive de ce dépôt où les défauts de figure
franchissent tous les contrôles (dette n° 13).

**Ce qui est bien fait, et il faut le dire** : la forme fermée du jour de bascule
(plafond % × 10 / pénalité ‰, sans le montant du marché) et la simplification de la durée dans
l'arbitrage retenue/caution sont deux résultats réels, démontrés et **étalonnés par invariants** sur
trois marchés d'un facteur mille et trois durées — c'est la meilleure méthode d'étalonnage du dépôt
à ce jour. Et l'exercice 3 (le DOE à refuser, ligne 4 sur le récolement) est le meilleur morceau
d'enseignement contractuel du palier.

---

## 1. Contre-expertise à l'aveugle

Six grandeurs recalculées à partir de `data/projet-gare.json`, `prix.json` et `planification.json`
**seulement**, avant toute lecture du raisonnement de l'auteur. Scripts :
`/tmp/claude-0/-home-user-mine/70713aa8-3622-5c6d-a7c2-bce4a8b25d73/scratchpad/devil-rec/recalc.py`
et `.../recalc2.py`.

Socle hérité : marché 79 646 878,79 MAD (`prix.bordereau.prix_de_vente_MAD`) ; frais de durée
16 240,33 MAD/j **ouvré** ; conversion 1,4013 calendaire par ouvré ; pénalité 1,0 ‰/j **calendaire** ;
plafond 10 %.

| # | Grandeur | Mon recalcul | Le module | Verdict |
|---|---|---:|---:|---|
| 1 | Jour de bascule des pénalités | 7 964 687,88 / 79 646,88 = **100,00 j cal** ; /1,4013 = **71,36 j ouvrés** | 100,0 / 71,4 | **identique** |
| 2 | Coût d'une journée de non-réception | 111 609,17 + 16 240,33 = **127 849,50 MAD/j ouvré** (et 91 236,35 /j cal) | 127 849,50 | **identique en arithmétique, faux en définition — voir B1** |
| 3 | Coût de la confusion sur les réserves | 94 × 6 h / (6 × 8) = **11,750 j** × 127 849,50 = **1 502 231,64 MAD** | 1 502 231,62 | **identique en arithmétique, non robuste — voir B5** |
| 4 | Portage de la retenue (60 j) | 5 575 281,5 × 7 % × 60/365 = **64 153,92 MAD** ; caution 10 997,82 ; rapport 5,83 | 64 153,93 / 5 575,28 /mois / 5,83 | **identique en arithmétique, mal imputé — voir B7** |
| 5 | Surcoût du DOE | 240 h × 140 = 33 600 + 64 154 = **97 753,92 MAD** | 97 753,93 | **identique en arithmétique — voir B7, B8** |
| 6 | Écart OPR / planning | 41 − (15 + 10) = **16 j** × 127 849,50 = **2 045 592,02 MAD** | 16,0 j / 2 045 592,00 | **identique en arithmétique, mappage contestable — voir B2** |

**L'arithmétique du module est juste partout.** Je n'ai trouvé aucune erreur de calcul au sens
étroit : les six valeurs que j'ai refaites de mon côté tombent au centime. Les défauts sont ailleurs,
et ils sont plus graves qu'une faute d'arithmétique, parce qu'une faute d'arithmétique se voit.

### 1.1 Ce que le recalcul a trouvé que le module ne publie pas

**(a) Le mappage ESSA décide du tiers du résultat de S4a.** Le planning D2 porte une tâche
`ESSA` de 15 j dont le nom est « **Essais et** mise en service » et dont la clé de données est
`essais_mise_en_service_j`. La séquence du § S3a porte une étape 3 « Essais de fonctionnement des
installations » (10 j) **et** une étape 4 « Mise en service des systèmes » (15 j). Le code ne retire
du besoin que l'étape 4 (`"ise en service" in x["etape"]`, `calc/reception.py` l. 466-470) :

```
lecture AUTEUR : ESSA(15) = étape 4 seule   -> besoin 26, écart 16 j, 2 045 592 MAD
lecture du NOM : ESSA(15) = étapes 3+4 (25) -> besoin 16, écart  6 j,   767 097 MAD
rapport des deux lectures : 2,67
```

**(b) Les bornes que D-049 impose et que le module n'a pas publiées.** Calculées à partir des
fourchettes de `data/` :

```
frais de durée  : 10 230 .. 21 889 MAD/j ouvré   (publié 16 240, nominal seul)
pénalités       : 55 805 .. 223 218 MAD/j ouvré  (publié 111 609, nominal seul)
=> un jour de non-réception : 66 035 .. 245 108 MAD   (publié 127 850, SANS bornes)
=> rapport des deux régimes :      3,0 .. 24,0        (publié 7,9,    SANS bornes)
écart au planning (reception_j [7;15]) : 11 .. 19 j = 1 406 345 .. 2 429 141 MAD (publié 16 j, SANS bornes)
rapport des heures de DOE   : 1,00 .. 15,0            (publié 4,0,    SANS bornes)
surcoût total du DOE        : 21 385 .. 270 862 MAD   (publié 97 754, SANS bornes)
```

La borne basse du surcoût **en heures** du DOE est **nulle** (320 bas = 160 h = 160 h haut du fil de
l'eau). Sur ses propres fourchettes, reconstituer le DOE peut ne coûter aucune heure de plus. Le
module publie « 4,0 fois plus » quatre fois, dont dans la fiche mémo.

**(c) La sensibilité du coût de la confusion à une donnée que le module ne pose pas.** Le calcul
suppose que les 7 réserves bloquantes se lèvent en 0,875 j. Si elles en prennent davantage — ce que
l'exercice 2 du **même module** affirme (« une pièce annoncée sous dix jours ») — la confusion se
réduit d'autant, parce que l'on attend la pièce de toute façon :

```
bloquantes en  0,875 j : confusion 11,750 j -> 1 502 232 MAD   (publié)
bloquantes en  5     j : confusion  7,625 j ->   974 852 MAD
bloquantes en 10     j : confusion  2,625 j ->   335 605 MAD   (facteur 4,5)
```

**(d) L'unité des 41 j.** `data/.../operations_prealables.etapes[].duree_j` ne dit nulle part en
quel calendrier elle compte. Le module les traite en **ouvrés** (il les compare à `ESSA`+`RECE` de
D2, qui sont ouvrés, et multiplie l'écart par un MAD/**j ouvré**) mais les narre en **calendaires**
(« ment d'un mois et demi ») :

```
41 j calendaires = 1,35 mois -> « un mois et demi » : plausible
41 j OUVRÉS = 57,5 j calendaires = 1,89 mois -> « un mois et demi » : FAUX
```

**(e) « Une erreur de six semaines ».** 100 − 71,4 = 28,6. En calendaire : 4,1 semaines. L'énoncé
« annoncer l'un pour l'autre » couvre les deux sens ; il n'est vrai que dans un seul
(28,6 × 1,4013 / 7 = 5,7 semaines).

---

## 2. Défauts

| # | Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|---|
| **B1** | Le module rebaptise « coût d'une **journée de non-réception** » ce que D1 publie comme « coût d'un jour de **retard** », et l'applique à des jours qui ne sont pas des jours de retard : les six étapes d'OPR, les 11,75 j d'hésitation sur les réserves, le vendredi de l'exercice 2. **Les pénalités ne courent qu'au-delà du délai contractuel.** Si la réception intervient dans le délai, un jour coûte 16 240 MAD, pas 127 850 — facteur **7,9**, et c'est le facteur par lequel tout l'argent du module est multiplié. La condition n'est écrite nulle part. | **bloquant** | `prix.json` → clé `cout_du_retard`, indexée par `retard_j_ouvres` ; `content/03-d1-metres-prix.md` l. 345 « Ce que coûte un mois **de retard** ». REC : `calc/reception.py` l. 48-60 et le titre de la figure 1 (« d'un **retard** de réception ») contre le texte S2 (« un jour de **non-réception** »). Exercice 2 : rien dans l'énoncé ne dit que le chantier est en retard, et le corrigé facture 127 850 MAD/jour. | Publier **deux régimes de plus** : avant le terme contractuel (frais de durée seuls, 16 240 MAD) et après (127 850). Renommer la grandeur. Reprendre les exercices 2 et la fiche mémo en conséquence. |
| **B2** | Les essais de fonctionnement (étape 3, 10 j) sont comptés comme absents du planning alors que la tâche D2 qui les porterait s'appelle « **Essais** et mise en service » (clé `essais_mise_en_service_j`). Le module affirme pourtant, en toutes lettres et dans un test, qu'il n'y a pas de double compte. | **bloquant** | `calc/planification.py` l. 161 et 197 ; `calc/reception.py` l. 466-470 ne retire que `"ise en service"` ; `content` S4a : « L'étape « Mise en service » n'est pas comptée deux fois : le planning la porte déjà sous le nom « **essais et** mise en service » » — la phrase nomme elle-même la tâche qui porte aussi les essais. Recalcul § 1.1(a) : écart 6 j / 767 097 MAD dans l'autre lecture, soit **2,67×** d'écart. | Trancher le périmètre d'`ESSA` et l'**écrire dans `data/`** ; publier les deux lectures et leur écart, puisque c'est exactement ce que D-055 demande. En l'état la dette n° 25 publie le mauvais chiffre. |
| **B3** | **Figure 3 — deux libellés tronqués, et la troncature rend le libellé faux.** `svgkit.js` l. 890 fait `lignes.slice(0, 2)` et supprime en silence la troisième ligne. « Heures de reconstitution **en plus** » est rendu « Heures de reconstitution » au-dessus d'une barre qui vaut 34 kMAD, alors que le tableau de la même section chiffre les heures de reconstitution à **44 800 MAD**. « Portage du décompte **bloqué** » est rendu « Portage du décompte ». | **bloquant** | Capture `…-figure3.png` ouverte ; extraction des nœuds `<text>` du HTML : `['11','DOE tenu au',"fil de l'eau",'34','Heures de','reconstitution','64','Portage du','décompte','109',…]`. Données source : `figures.doe[1].libelle = "Heures de reconstitution en plus"`. | Raccourcir les libellés à deux lignes de 14 caractères (« Heures en plus », « Décompte bloqué »), et **ajouter au contrôle** un test qui compare le texte rendu au libellé de `data/` (dette n° 13). |
| **B4** | **Figure 3 — le total affiché contredit le tableau de la même section.** La cascade titrée « d'où vient le **surcoût** » additionne la barre de référence (11 kMAD, qui n'est pas un surcoût) et totalise **109 kMAD**, quand le tableau immédiatement au-dessus publie « **Surcoût total — 97 754 MAD** ». Et la légende « les deux tiers du surcoût ne sont pas des heures » vaut 66 % de 97 754 mais **59 %** de 109. | **bloquant** | Capture `…-figure3.png` : barres 11 / 34 / 64 / **109**. `content` S4d, dernière ligne du tableau : 97 754. `calc/reception.py` l. 530-533 : le total de la cascade vaut `cout_reconstitue + portage`, pas `surcout + portage`. Le test l. 290 vérifie seulement que le total recolle à la somme des barres — il valide l'incohérence. | Retirer la barre de référence de la cascade, ou retitrer la figure « le coût total d'un DOE reconstitué » et publier les deux totaux côte à côte avec leur différence. |
| **B5** | Le coût de la confusion (1 502 232 MAD, répété six fois dont dans la fiche mémo) suppose que les 7 réserves bloquantes se lèvent en **0,88 jour**. L'exercice 2 du même module décrit deux de ces bloquantes comme un escalator « en attente d'une pièce annoncée sous dix jours » et un désenfumage « faute de créneau avec le lot technique ». **Un plan fictif ne doit pas contredire ce que le module en dit (D-044).** | **bloquant** | `calc/reception.py` l. 275-277 : `jours_bloq = 42 h / 48 h/j = 0,875`. `content` S6 exercice 2. Recalcul § 1.1(c) : à dix jours de pièce, la confusion tombe à 335 605 MAD — facteur **4,5**. | Modéliser la levée d'une bloquante par `max(heures/capacité, délai d'approvisionnement)` et poser ce délai en V3 borné ; ou retirer de l'exercice 2 le détail qui contredit le calcul. La seconde solution est la mauvaise : c'est l'exercice qui a raison. |
| **B6** | **Rendu : tout le § S3a et tout le § S3b sont publiés en français sans accents.** Le tableau des six étapes (« Visite des **operations prealables** », « en **presence** de la **maîtrise** d'œuvre », « Mise en service des **systemes** »), les six pièges, et la **règle centrale du module** : « Une seule question **decide** : la **reserve** EMPECHE-T-ELLE l'usage ou met-elle en cause la **securite** des personnes ? […] Si non, elle se prononce AVEC **reserves**, et celles-ci se **levent** sous **delai**. Il n'y a pas de **troisieme** famille […] ». | **bloquant** | Texte extrait du HTML rendu ; source : les champs `_la_regle`, `piege`, `etape`, `qui` de `data/projet-gare.json`, saisis en ASCII et publiés verbatim par `{{reception.reserves.la_regle}}` et le tableau S3a. | Accentuer les champs de `data/` destinés à être publiés tels quels, et ajouter au `check` un contrôle qui refuse un texte publié contenant « reserve », « securite », « delai », « decide ». |
| **B7** | **Le portage du DOE est imputé à la mauvaise grandeur, et les deux modules se contredisent sur cette grandeur.** Le DOE bloque le **décompte définitif** (le solde) ; le module chiffre le portage de la **retenue de garantie**, qui est immobilisée par la clause de garantie que le DOE retarde ou non. Pire : D1 écrit « la retenue de garantie ne revient qu'**après la réception** », REC écrit « conservée jusqu'à la **fin de la période de garantie** ». **66 % du surcoût publié du DOE** (64 154 sur 97 754) repose sur cette imputation. | **bloquant** | `calc/reception.py` l. 345 `bloque = po["retenue_immobilisee_MAD"]` ; `prix.json` → `tresorerie.lecture` ; `content` S3c. L'encart `_le_montant_bloque_est_une_borne_basse` reconnaît la substitution (« parce que c'est le seul montant que ce cours publie ») mais une **borne basse d'une autre grandeur** n'est pas une borne basse. | Soit publier le portage du **solde** (et le poser en V3 si D1 ne le publie pas), soit retirer le portage du surcoût du DOE et le publier à part comme un coût de la clause de garantie. Et aligner D1 et REC sur une seule date de restitution (D-039). |
| **B8** | **D-049 non appliqué aux cinq chiffres de tête du module.** Sont publiés sans bornes : le coût d'un jour (127 850), le rapport des régimes (7,9), l'écart au planning (16 j) et son coût (2 045 592 MAD), le surcoût total du DOE (97 754), le rapport des heures de DOE (4,0). Les cinq figurent dans la fiche mémo A4. Les bornes honnêtes, calculées § 1.1(b), vont de **66 035 à 245 108 MAD** pour le coût d'un jour et de **1,0 à 15,0** pour un rapport publié à « 4,0 ». | **bloquant** | `calc/sorties/reception.json` : `cout_d_un_jour`, `confrontation_au_planning` et `doe.cout_total…` ne portent aucun champ `*_bornes`, alors que `jour_de_bascule`, `cout_de_la_confusion`, `surcout_en_heures` et `economie` en portent. D-049 : « **Tout** résultat chiffré d'un module publie ses deux bornes ». | Ajouter les bornes partout, et appliquer la leçon de D-049 : ce qui résiste au balayage ici, c'est le **rapport** (la bascule reste une règle de lecture de CPS quelles que soient les bornes) ; le montant n'est qu'une illustration et doit être présenté comme tel. |
| **M1** | L'unité des 41 j d'OPR n'est déclarée nulle part, et le module l'emploie dans les deux sens : en **ouvrés** pour la comparaison et le prix, en **calendaires** pour le récit (« ment d'un mois et demi »). Dans le module qui se vante de ne jamais confondre les deux. | majeur | `data/.../operations_prealables` : `duree_j` sans unité. `calc/reception.py` l. 471-475 compare à des durées ouvrées de D2 et multiplie par un MAD/j ouvré. `operations_prealables.note` : « un mois et demi » = 1,35 mois en calendaire, 1,89 en ouvré (§ 1.1(d)). | Déclarer l'unité dans `data/`, et retirer ou recalculer « un mois et demi ». |
| **M2** | Les six durées d'OPR sont exemptées de fourchette au motif que ce sont « des **DÉCISIONS** d'organisation, comme les effectifs : on prévoit, on annonce, on s'y tient ». Le module dit l'inverse deux sections plus loin : l'étape 4 est « la seule que l'entreprise **ne maîtrise pas** : c'est l'exploitant ferroviaire qui la conduit », et l'étape 6 est la décision du maître d'ouvrage. On ne décide pas une durée qui appartient à quelqu'un d'autre. | majeur | `data/.../operations_prealables._role` contre `operations_prealables._l_essai_qui_commande` et `_quoi_en_faire` (« la moitié de sa durée n'appartient pas à l'entreprise »). | Scinder : durées de l'entreprise = décisions sans fourchette ; durées des tiers (étapes 2, 4, 6) = hypothèses V3 **bornées**. C'est la condition pour que B8 soit corrigeable sur l'écart au planning. |
| **M3** | S5 : « Ignorer le plafond des pénalités \| on découvre au **90ᵉ jour** que le levier a disparu \| une stratégie construite sur un mécanisme qui s'arrête au **100ᵉ jour** ». Les deux cases de la même ligne se contredisent : au 90ᵉ jour calendaire le levier n'a pas disparu. Le « 90 » est écrit à la main, contre § 4.3 (aucun nombre technique tapé à la main). | majeur | Texte rendu ; `cout_d_un_jour.jour_de_bascule_calendaire = 100,0`. Même nombre en dur dans `_ce_que_le_changement_de_regime_veut_dire` (« pas au quatre-vingt-dixième jour »). | Remplacer par la variable, dans les deux endroits. |
| **M4** | S5 : « Oublier les opérations préalables au planning → **41 jours de décalage** », quand S4a mesure **16 j** en rejouant le réseau sur ce même planning, qui porte déjà `ESSA`+`RECE` = 25 j. Deux décalages contradictoires à trois paragraphes d'écart. | majeur | `content` S5 l. 5 du tableau contre S4a (`decalage_mesure_de_la_fin_j = 16,0`). | Dire de quel planning on parle, ou n'en publier qu'un. |
| **M5** | **L'étalonnage ne couvre que trois fonctions sur sept.** `reserves`, `doe`, `operations_prealables` et `confrontation_au_planning` n'ont **aucun** cas fermé et **aucune** vérification dimensionnelle. Ce sont les fonctions d'où sortent 1 502 232, 97 754 et 2 045 592 MAD. § 3.3 : « sans étalonnage, ses résultats restent V3 et **ne servent pas d'exemple de référence** » — or ils sont dans la fiche mémo. | majeur | `calc/etalonnage/reception_cas_ferme.py` : sections 1 à 7, toutes sur `cout_d_un_jour`, `courbe_du_cout`, `portage_de_la_retenue`. `grep reserve\|confrontation` dans l'étalonnage et dans `verif_unites.py` : **zéro occurrence**. | Étalonner les trois fonctions manquantes, au minimum par invariants (la confusion est proportionnelle au nombre de non-bloquantes ; le surcoût du DOE est nul si les deux scénarios sont égaux). |
| **M6** | La formule `heures / (effectif × heures_par_jour)` est dimensionnellement ambiguë — elle n'est juste que si les 6 h sont des **heures-homme**, alors que `data/` les décrit comme « temps moyen de levée d'une réserve, intervention et reconstat compris », c'est-à-dire un temps écoulé. La vérification dimensionnelle, dont le module se vante (elle a trouvé l'année de 365,25 j), **ne regarde pas cette formule**. Et les 18 « Documents manquants » sont levées par des compagnons qualifiés à 58 MAD/h, 6 h chacune, six en parallèle — alors que la note de `data/` dit « beaucoup **attendent un fournisseur** ». | majeur | `calc/reception.py` l. 275-278 ; `data/.../reserves._effectif_de_levee` ; `calc/verif_unites.py` section reception : aucune ligne sur les réserves. | Déclarer les 6 h en **h·homme**, sortir la famille « Documents manquants » du calcul d'atelier (elle se lève au taux `controleur` et à un délai de tiers), et ajouter la formule à `verif_unites.py`. |
| **M7** | **Figure 2 : la figure enseigne l'inverse de sa légende.** Les cinq barres sont de la même couleur ; les deux familles bloquantes ne se distinguent que par le mot « BLOQUANTE » ajouté au libellé. L'œil lit d'abord la barre de 62. La figure dont tout le propos est « la longueur n'entre pas dans la décision » place donc la longueur au premier plan et la qualification en note. L'« erreur courante » admet d'ailleurs que le lecteur va se tromper. | majeur | Capture `…-figure2.png` ouverte ; `calc/reception.py` l. 522-525 (le libellé porte l'information, pas la forme). | Colorer les deux familles bloquantes différemment, ou mieux : passer à deux barres empilées (bloque / ne bloque pas) et garder le détail par famille en tableau. |
| **M8** | **L'exercice 2 viole la règle binaire du § S3b.** La règle dit : « Si oui [elle empêche l'usage], la réception **ne se prononce pas**. […] Il n'y a pas de troisième famille. » Le corrigé propose, pour l'escalator — classé `empeche_l_usage = true` dans `data/` — de « réceptionner avec réserve et une date ferme de levée, si l'exploitant accepte ». C'est la troisième famille, et le module ne dit pas qu'il vient de l'introduire. | majeur | `data/.../familles[4].empeche_l_usage = true` (« escalator à l'arrêt ») contre `content` S6 exercice 2, point 3. | Soit assouplir la règle de S3b (la qualification est un **jugement**, et l'exploitant en est juge pour l'usage), soit retirer l'option du corrigé. La première est la bonne et enrichit le module. |
| **M9** | Les effets juridiques de la réception sont énoncés comme des faits, sans ⏸ ni niveau de preuve, en pleine phase § 5.0 : « le jour où la réception est prononcée, **tout cela s'arrête d'un coup** » ; « elle **libère la caution**, elle **fait courir les garanties** » ; quiz 6 : « Qui garde l'ouvrage ? **L'entreprise**, jusqu'à la date écrite du transfert ». Ce sont des règles de droit, pas des mécanismes physiques. R8 : « N'avance jamais […] comme un fait ». | majeur | `content` S2, S4h, S7 quiz 6. L'encart « Ce que ce module n'est pas » prévient au niveau du module, mais la discipline du § 5.0 est appliquée **au point d'usage** partout ailleurs dans ce cours. | Mettre un ⏸ au point d'usage sur les trois effets, et reformuler en « ce que le contrat organise », comme le module le fait très bien pour le DOE. |
| **M10** | Le test `« la mise en service n'est PAS comptée deux fois »` vérifie que le code fait `41 − 15`, c'est-à-dire qu'il **épingle le choix de l'auteur** au lieu de le contrôler. C'est le défaut nommé par D-043 (« un cours qui se décerne une vérification qu'il n'a pas faite »). | majeur | `calc/tests/test_reception.py` l. 259-266. | Remplacer par un test de **règle** : aucune étape de la séquence ne doit être portée par deux tâches du planning — ce qui exige d'écrire dans `data/` le périmètre de chaque tâche (voir B2). |
| **m1** | « Annoncer l'un pour l'autre dans une réunion est une erreur de **six semaines** » (S2, et repris en S5). 100 − 71,4 = 28,6 j = **4,1 semaines** en calendaire ; six ne s'obtient que dans un seul des deux sens de confusion. | mineur | § 1.1(e). | Publier l'écart calculé, dans son calendrier. |
| **m2** | Fiche mémo : « **Les cinq réflexes** » suivi de **six** items numérotés 1 à 6. | mineur | Texte rendu du bloc `:::memo`. | Compter. |
| **m3** | « La moitié de sa durée n'appartient pas à l'entreprise » (S4a, D-055, et réflexe 6 de la mémo). Appliqué à la ligne « Réception » décomposée (26 j), les étapes de tiers font 3 + 7 = **10 j, soit 38 %**. La moitié ne s'obtient que sur les 41 j, qui ne sont pas la ligne dont parle la phrase. | mineur | `data/.../etapes` ; `calc/reception.py` `_quoi_en_faire`. | Publier la part calculée. |
| **m4** | Figure 1 : « **10.6** MMAD » — point décimal dans un document qui écrit « 71,4ᵉ », « 6,9 % » et « 127 850 » partout ailleurs. | mineur | Capture `…-figure1.png` ; nœuds `<text>` du HTML. | Appliquer le `.replace(".", ",")` que `svgkit` fait déjà pour les barres de la cascade (l. 879) à l'annotation du diagramme. |
| **m5** | Légende de la figure 2 : « une réserve de sécurité isolée dans une liste de **quatre-vingt-dix lignes d'aspect** » — juste sous une figure qui montre **62** lignes d'aspect (94 non bloquantes toutes familles). Même expression dans `_et_dans_l_autre_sens` et dans S5. | mineur | Capture `…-figure2.png` ; `data/.../familles[0].nombre = 62`. | Utiliser la variable, ou écrire « une longue liste ». |
| **m6** | Exercice 1 : l'énoncé dit « une pénalité de 2 ‰ **par jour** », sans calendrier, et le corrigé conclut « 25 **jours calendaires** ». Dans le module qui enseigne précisément que cette précision manque toujours dans un CPS. | mineur | `content` S6 exercice 1. | Faire de l'omission le sujet : « et si le CPS ne dit pas en quel calendrier, c'est la première question à poser ». |
| **m7** | Précision affichée : 2 045 592, 1 502 232, 97 754, 5 575 282 — six et sept chiffres significatifs sur des produits d'hypothèses V3 à fourchette large. § 3.6 impose trois chiffres significatifs ; D-049 impose « un canari qui refuse toute valeur de figure publiée au centime ». | mineur | Texte rendu ; `reception.json`. | Arrondir à l'affichage (2,0 MMAD ; 1,5 MMAD ; 98 kMAD) et garder la valeur exacte dans la sortie. |
| **m8** | « L'étape « Mise en service des **systemes** et essais d'exploitation » » dans le corps du texte de S4a — champ `data/` non accentué réinjecté dans une phrase française. Cas particulier de B6, listé à part parce qu'il survit même si B6 n'est corrigé que dans les tableaux. | mineur | Texte rendu, S4a. | Voir B6. |
| **m9** | § S4g : la liste des dispositions ne mentionne pas l'**état des systèmes de sécurité incendie** (détection, désenfumage, éclairage de sécurité) pendant la période de garde, alors que ce sont précisément les installations qui viennent d'être essayées, qui ne sont pas encore sous contrat de maintenance, et que le module décrit un ERP « ouvert sur l'espace public » où « des gens entrent ». | mineur | `content` S4g, points 1 à 3 et « le cas particulier d'une gare ». | Ajouter un quatrième point : qui surveille les installations de sécurité entre le dernier essai et la prise en charge par l'exploitant. |
| **m10** | Figure 1 : l'axe des ordonnées n'a ni graduation ni unité — seule l'annotation du point final (« 10.6 MMAD ») porte l'unité. Le lecteur ne peut pas lire la valeur à la cassure. | mineur | Capture `…-figure1.png`. | Graduer l'axe, ou annoter le point de cassure comme le point final. |

**Compte** : 8 bloquants, 10 majeurs, 10 mineurs.

---

## 3. Grille d'auto-évaluation § 7.2

| Critère | Note | Justification |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | S2 est le meilleur morceau du module : le transfert de risque, le changement de régime, et la raison pour laquelle le montant du marché disparaît de la bascule. Chaque mécanisme est justifié avant d'être chiffré. |
| Les hypothèses sont explicites | **1** | Six V3 correctement balisées, mais : les 41 j d'OPR n'ont ni balise, ni bornes, ni unité, et leur exemption est contredite par le module (M2) ; cinq chiffres de tête sortent sans bornes contre D-049 (B8) ; le mappage `ESSA` est une hypothèse présentée comme un constat (B2) ; et la condition « le chantier est déjà en retard », qui vaut un facteur 7,9, n'est écrite nulle part (B1). |
| Les formules sont justifiées | **3** | La forme fermée de la bascule et la simplification de la durée sont démontrées, pas assénées, et étalonnées par **invariants** sur trois marchés et trois durées — la meilleure forme d'étalonnage, et le module le dit. |
| L'exemple est vérifié | **1** | Quatre des sept fonctions n'ont **aucun** étalonnage ni vérification dimensionnelle (M5), et ce sont celles d'où sortent trois des cinq chiffres de la fiche mémo. Le seul test qui porte sur le point contesté épingle la conclusion de l'auteur (M10). Mon recalcul indépendant retombe au centime partout — mais sur l'arithmétique seule, qui n'était pas en cause. |
| Le piège est identifié | **2** | Douze pièges en S5, six attachés aux étapes, et l'erreur **symétrique** sur la réserve de sécurité noyée dans la liste : c'est de la vraie pédagogie de chantier. Deux de ces pièges sont cependant faux ou contradictoires (M3, M4). |
| Lien avec l'exécution | **3** | S4g (la garde de l'ouvrage, et la voie exploitée) et S4h (double lecture entreprise / maîtrise d'œuvre, six lignes, toutes concrètes) sont substantiels et utilisables tels quels. |
| Lien avec le coût et le délai | **2** | C'est l'objet du module et il est traité de bout en bout — mais le chiffre de délai repose sur un mappage contestable (B2) et tous les chiffres de coût sur une condition non déclarée (B1). |

**Total : 15 / 21. Minimum 2 partout : NON TENU** (deux notes à 1). Le § 7.2 interdit la livraison en
l'état.

---

## 4. Verdict

**Non livrable.**

Le module est bien conçu et mal garanti. Son idée centrale est juste et neuve pour ce cours — la
réception est un transfert de risque dont le prix par jour change de régime, et la date de ce
changement se lit dans deux lignes d'un CPS sans connaître le montant du marché. Cette partie-là est
démontrée, étalonnée par invariants, et elle survivra à la correction. De même pour S4g, S4h et
l'exercice 3, qui sont du métier.

Ce qui interdit la livraison tient en trois phrases.

**Premièrement, tout l'argent du module repose sur une condition qu'il n'énonce pas** (B1). D1
publie un coût de **retard** ; REC le rebaptise coût de **non-réception** et l'applique à des
journées qui ne sont pas en retard. Facteur 7,9 sur les cinq montants de la fiche mémo.

**Deuxièmement, les deux confrontations dont le module tire ses plus gros chiffres choisissent
chacune, sans le dire, l'hypothèse qui maximise le résultat** (B2 et B5). Les essais de
fonctionnement sont comptés comme absents d'une tâche qui s'appelle « Essais et mise en service » —
2,67× ; et les réserves bloquantes sont supposées levées en sept heures par un module dont
l'exercice, deux pages plus loin, les fait attendre dix jours — 4,5×. Dans les deux cas le module
écrit un paragraphe d'honnêteté méthodologique (« ce que cette comparaison est, et ce qu'elle n'est
pas ») qui porte à côté du vrai problème. Un paragraphe de prudence ne remplace pas une hypothèse
déclarée.

**Troisièmement, le rendu ment trois fois** (B3, B4, B6). Une barre étiquetée « Heures de
reconstitution » qui vaut le surcoût et non le coût ; une cascade titrée « surcoût » qui totalise
autre chose que le surcoût du tableau d'à côté ; et la règle centrale du module publiée en français
sans accents. Les trois ont franchi une chaîne verte, ce qui confirme pour la sixième fois
consécutive la dette n° 13 — et cette fois le défaut ne se voit pas seulement, il **dit faux**.

S'y ajoute l'application partielle de D-049, un jour après que la décision a été prise (B8) : les
chiffres qui portent des bornes sont ceux qui en avaient déjà, et les cinq qui n'en ont pas sont
exactement les cinq de la fiche mémo.

**À corriger avant relivraison** : les huit bloquants, puis M1, M2, M5 et M6, qui conditionnent la
correction propre de B2, B5 et B8. Les six autres majeurs et les dix mineurs peuvent être versés en
dette si le lecteur l'accepte, mais M9 (les effets juridiques énoncés comme des faits) est à
reprendre tant que la phase § 5.0 dure : c'est le seul endroit du palier où le cours franchit la
ligne qu'il s'est tracée.

**Passe à relancer après correction**, par une session distincte, avec un canari : ce module est le
neuvième, et le § 12.2 impose un contrôle du relecteur tous les cinq modules.

---

## 5. Suite donnée (28/10/2026)

**8 bloquants : tous corrigés.** **10 majeurs : 10 corrigés.** **10 mineurs : 9 corrigés, 1 traité
en déclarant la limite.** La correction a changé le module sur le fond, pas seulement sur ses
nombres.

### B1 — la condition qui manquait, et c'est la plus instructive

Le reproche est juste et il était le plus grave : le module D1 publie un coût de **retard**, et ce
module en avait fait un coût de **non-réception**. La correction ne consiste pas à ajouter une
phrase. Le module publie désormais **trois périodes et deux prix**, parce que le premier et le
troisième sont le même :

| Période | Régime | Coût d'un jour ouvré |
|---|---|---:|
| avant le terme contractuel | hors pénalités | 16 240 MAD |
| du terme au plafond | sous pénalités | 127 850 MAD (bornes 72 000 – 239 000) |
| après le plafond | hors pénalités | 16 240 MAD |

Ce n'est donc pas une courbe croissante, c'est une **fenêtre de cherté** — un résultat que la
version fautive ne pouvait pas voir, et qui vaut mieux que ce qu'elle disait. Toutes les
conséquences chiffrées du module (réserves, confrontation au planning) sont publiées **dans les deux
régimes**, et la première question de la check-list est désormais « sommes-nous en retard ? ». Un
invariant d'étalonnage vérifie que les deux régimes extrêmes coûtent exactement la même chose.

### B2 — l'attribution, et non le total

La correction ne change pas le total (16 jours) mais elle change ce qui le compose, et c'est elle
qui dit quoi corriger. Chaque étape de la séquence déclare désormais dans `data/` **la tâche du
planning qui la porte** (`porte_par`), et la comparaison se fait tâche par tâche :

| Tâche | Prévu | Demandé | Écart |
|---|---:|---:|---:|
| ESSA · Essais et mise en service | 15 j | 25 j | 10 j |
| RECE · Réception | 10 j | 16 j | 6 j |

Le test qui « épinglait le choix de l'auteur » (M10) est remplacé par deux tests de règle : aucune
étape n'est portée par deux tâches, et toutes les étapes de la séquence sont portées. Un canari
vérifie que l'ancienne lecture donnait une attribution différente.

### B5 — le délai commande, pas le volume

La durée de levée d'un ensemble de réserves est désormais `max(heures-homme / capacité, plus long
délai de tiers)`. Les sept bloquantes demandent 0,88 jour d'atelier et **10 jours** de calendrier,
parce que l'escalator attend une pièce — ce que l'exercice du même module annonçait déjà (D-044).
Le coût de la confusion tombe de 1 502 232 à **335 000 MAD sous pénalités, 42 600 hors pénalités**,
et le module y gagne son cinquième résultat : *une liste de réserves se hiérarchise par son délai le
plus long, pas par son volume*. Un invariant d'étalonnage vérifie que doubler l'effectif ne change
rien tant qu'un tiers commande, et divise la durée par deux quand c'est l'atelier.

### B7 — la bonne grandeur

Le DOE bloque le **solde des travaux**, pas la retenue de garantie, qui est immobilisée par la
clause de garantie que le dossier soit remis ou non. Le solde est désormais une hypothèse déclarée
(4 % du marché, 1,5 à 10) : le portage passe de 64 154 à **36 659 MAD** et le surcoût total de
97 754 à **70 259**. Deux invariants d'étalonnage et un contrôle de valeur vérifient que les deux
montants ne se confondent pas.

### B3, B4, B6, B8 et les majeurs

- **B3** : `cascade` acceptait deux lignes de libellé et supprimait la troisième **en silence**. Le
  générateur lève maintenant une erreur au lieu de tronquer, et les libellés ont été raccourcis.
- **B4** : la cascade part du surcoût et son total est exactement celui du tableau (70 300 MAD à
  trois chiffres significatifs). La barre de référence, qui n'est pas un surcoût, en est sortie.
- **B6** et **m8** : tout le bloc `reception` de `data/` est accentué.
- **B8** : bornes ajoutées sur le coût d'un jour, le rapport des régimes, l'écart au planning (et
  son décalage, **mesuré** aux deux bornes), le surcoût du DOE et le portage. La borne basse du
  surcoût en heures est publiée **nulle**, comme la passe le demandait.
- **M1, M2** : l'unité des durées d'OPR est déclarée (`jours ouvrés`), et les trois étapes tenues
  par des tiers portent désormais une fourchette — d'où toute l'étendue de 27 à 94 jours. Les trois
  étapes de l'entreprise restent des décisions sans fourchette.
- **M5, M6** : l'étalonnage couvre six fonctions sur sept et porte quatre invariants de plus ; la
  vérification dimensionnelle contrôle la formule de levée. Sa **limite est déclarée** : `pint` ne
  distingue pas l'heure-homme de l'heure, et ce contrôle-là repose sur la note de `data/`.
- **M7** : la figure 2 colore les familles bloquantes et porte une légende d'alerte ; un test exige
  que la qualification soit dans la **forme** et non dans le libellé.
- **M8** : la règle du § S3b est précisée — la qualification est un **jugement**, et sur l'usage
  c'est l'exploitant qui en est juge ; la sécurité, elle, ne se juge avec personne. L'exercice 2
  explicite ce point au lieu de l'enfreindre.
- **M9** : les effets juridiques de la réception portent ⏸ au point d'usage, dans le corps, le
  glossaire, le quiz et la fiche mémo.
- **m1 à m10** : écart des calendriers calculé (28,6 j), « cinq réflexes » devenus six, part tenue
  par des tiers publiée (61 %), virgule décimale dans le diagramme, « 62 lignes d'aspect » lu dans
  les données, calendrier de la pénalité posé comme la question de l'exercice 1, format `::k` à
  trois chiffres significatifs ajouté au build, et un quatrième point au § S4g sur les installations
  de sécurité pendant la garde.

### Ce qui reste, et qui est versé en dette

Le module D1 écrit que la retenue de garantie « ne revient qu'après la réception » ; REC dit
qu'elle est immobilisée jusqu'à une date que le marché fixe (⏸), qui lui est postérieure. REC ne
contredit plus D1 frontalement, mais la courbe de trésorerie de D1 reste optimiste de la durée de
la garantie. Versé en dette plutôt que corrigé à la hâte dans un module livré.

### Ce que cette passe apprend sur le contrôle

C'est la dixième passe du dépôt, et la dixième fois qu'aucun bloquant n'est trouvé par la chaîne
automatique. Mais celle-ci a trouvé autre chose que les précédentes : **une arithmétique juste au
centime partout, et un sens faux**. B1 et B7 ne sont pas des erreurs de calcul — ce sont des
grandeurs employées hors de leur condition d'emploi, et aucun test d'égalité ne peut les voir. Le
seul contrôle qui les attrape est de **relire le nom de la grandeur qu'on emprunte au module
voisin** (D-056).
