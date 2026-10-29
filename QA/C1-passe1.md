# C1 — Installation de chantier · passe adversariale n° 1

> Relecteur hostile, indépendant de l'auteur. Les commentaires de `calc/installation.py`, les encarts
> du module et les chaînes narratives publiées par `calc/` ont été lus **comme des affirmations à
> vérifier**, jamais comme des preuves. Les **cinq captures ont été ouvertes et regardées**. La
> contre-expertise du § 0 a été faite **avant** toute lecture du module et du calcul, depuis
> `data/projet-gare.json` seul (script jeté hors dépôt).
>
> **Avertissement sur l'état du livrable.** Le dépôt a été **modifié pendant la passe** : à 22:28,
> `calc/installation.py`, `content/11-c1-installation-de-chantier.md`, `STATE.md` et
> `data/registre-hypotheses.csv` ont changé et le build a été relancé (HTML et captures réécrits).
> Deux défauts que j'avais relevés sur le commit `996283e` — « les additionner conduirait à **quatre**
> grues » contre « cinq » dans le texte, et le massif de grue (180 000 MAD) non registré — ont été
> corrigés en cours de relecture ; un troisième (M3) ne l'a été qu'à moitié. Le présent rapport porte
> sur l'**état du 28/10 22:28**, pas sur le commit. Un livrable en relecture devrait être figé (m9).

---

## 0. Contre-expertise à l'aveugle — quatre recalculs

Faits en `python3` depuis `data/projet-gare.json` (+ `calc/sorties/planification.json`, `prix.json`,
`tranche-plancher.json` pour les grandeurs héritées), **avant** d'ouvrir `calc/installation.py` et le
module.

### 0.1 Géométrie — part de l'emprise où une pièce de 8,0 t est levable

Rayon limite : `r_lim = M/m = 200 / 8,0 = 25,0 m` (< portée, donc c'est le moment qui borne).
Aire d'un disque de rayon R clippé par le rectangle 120 × 40, centre à `y = 20` : le disque dépasse
les deux grands côtés sans atteindre les coins, donc

```
A = πR² − 2[ R²·acos(d/R) − d·√(R²−d²) ],  d = 20, R = 25
  = 1 963,50 − 2(402,24 − 300,00) = 1 759,06 m²   sur 4 800 m² → 36,65 %
```

| Variante | pièce 8,0 t — mon calcul | publié | écart | couverture — mon calcul | publié |
|---|---:|---:|---:|---:|---:|
| A — une grue au centre (60 ; 20) | **36,6 %** (1 759 m², forme fermée) | 36,8 % | 0,2 pt | 98,1 % | 98,2 % |
| B — deux grues aux tiers | **73,3 %** (2 × 1 759, disques disjoints) | 73,7 % | 0,4 pt | 100,0 % | 100,0 % |
| C — une grue en (60 ; −6) | **14,3 %** (684,7 m², segment d = 6) | 14,4 % | 0,1 pt | 87,5 % | 87,4 % |

→ **concorde.** L'écart est celui de l'échantillonnage au mètre (4 800 points) contre la forme
fermée ; il est partout ≤ 0,5 pt. La géométrie du module est juste, et son étalonnage
(`installation_cas_ferme.py`) est le meilleur morceau du livrable.

### 0.2 Débit — levages demandés par jour → **l'écart est de 63 %, et il change le verdict**

Ma voie : la demande de levage suit la **cadence du plancher que le cours exécute**. D2 donne
`MEZZ = 31,85 j` pour 8 zones, C3 donne `cadence des équipes = 3,4 j/zone`, le module TV donne
**424,3 m² de tables par zone**, posées puis déposées :

```
coffrage manutentionné   = 2 × 424,3 / 3,4   = 249,6 m²/j
levages de coffrage      = 249,6 / 10        = 25,0 /j
+ divers                                      = 12   /j
demande                                       = 37,0 /j
capacité = 7,0 × 8 × 0,65                     = 36,4 /j     → taux de charge = 101,6 %
```

Publié : **22,7 levages/j**, taux de charge **62,3 %**. Écart **+63 %** sur la demande, et le
résultat **traverse le seuil de 100 %**. Cause trouvée ensuite dans le code : la demande est calculée
sur la ligne « optimum de coût » de C3 (parc 430 m², cadence 8,05 j) — un scénario que le cours ne
retient pas et que C3 désigne explicitement comme n'étant pas une décision. → **B1**.

### 0.3 Dimensionnement — surface de base-vie

```
pointe D2 après lissage = 45 ; encadrement 12 % → 5,4 pers · ouvriers 39,6 pers
S = 39,6 × 4,5 + 5,4 × 9,0 = 178,2 + 48,6 = 226,8 m²
modules = ceil(226,8 / 15) = 16 → 240 m² installés, 13,2 m² d'arrondi
(sur la pointe AVANT lissage, 59 : 297,4 m² → 20 modules)
```

→ **concorde au chiffre près** avec `base_vie` (226,8 · 16 · 240 · 13,2). La pointe est bien lue chez
D2 et non redéclarée (D-039 respecté, et le test le vérifie).

### 0.4 Coût total, et part du marché

```
fixe  = 2 × (420 000 + 180 000) + 260 000              = 1 460 000 MAD
loyer = (2 × 95 000 + 35 000) × 29,7 mois              = 6 682 500 MAD
total                                                   = 8 142 500 MAD → 10,22 % de 79 646 879
```

→ **concorde** avec `cout`. Et le **fixe recolle exactement à D1** : 420 000 + 180 000 + 260 000 =
860 000 = `INST` (620 000) + `GRUE` (240 000) du bordereau. Bonne cohérence, à porter au crédit du
module.

**Mais deux dénominateurs sont faux.** (a) `durée` : le profil de grue que le module lit lui-même
(D2) ne demande de grue tour que du jour **19,9** (FOND) au jour **136,5** (MARQ), soit ≈ 5,4 mois
calendaires, et non 29,7. Loyer grue réel ≈ 1 030 000 MAD au lieu de 5 643 000 → **total ≈ 3,53 MMAD,
part fixe 41 %** et non 17,9 %, **part du marché ≈ 4,4 %** et non 10,22 % (→ **B2**). (b) `marché` :
D1 écrit que le bordereau qu'on signe est celui **avec divers** (102,5 MMAD) ; sur cette base,
10,22 % devient 7,94 % (→ **M8**).

---

## 1. Les dix points du § 12.2

| # | Point | Constat |
|---|---|---|
| 1 | Unités, homogénéité | **RAS.** `Q = M/r` (t·m / m = t), `r_lim = M/m` (t·m / t = m), levages/j = levages/h × h/j × sans dimension, m²/j × 2 ÷ m²/levage = levages/j, MAD = MAD + MAD/mois × mois. `verif_unites.py` section C1 les reprend une à une et **déclare** deux erreurs dimensionnellement invisibles. Le taux d'utilisation est divisé **une seule fois** (`/100`, calc:312) et publié sous un nom qui dit sa forme — le défaut B7c (changement d'unité silencieux) ne se reproduit pas. |
| 2 | Référentiels mélangés | **RAS.** Aucun référentiel n'est mobilisé : le module ne contient ni combinaison, ni coefficient partiel, ni article. |
| 3 | Valeur normative sans preuve / § 5.0 | **RAS sur le fond.** Vérifié ligne à ligne : aucune distance de sécurité, aucune règle de survol, aucune surface réglementaire de local social, aucune obligation de clôture n'est chiffrée. Les 4,5 et 9,0 m²/personne portent une balise V3 + la mention « les surfaces minimales sont réglementaires (⏸) » ; le bloc `_pause` de `data/` et le § S1 listent les six familles ⏸ ; la fiche mémo les redonne. Une seule réserve de forme : m7. |
| 4 | Ordres de grandeur, ratios | **Deux défauts.** La location de deux grues à tour pendant 29,7 mois pour 117 jours ouvrés de besoin (**B2**) ; la part du marché rapportée au bordereau de référence et non à l'offre (**M8**). Le reste tient : 25 m de rayon limite pour 8 t sur 200 t·m, 4,5 m²/personne, 16 modules de 15 m², 1 460 000 MAD de fixe. |
| 5 | Cohérence data / figures / calc / coût / planning / modules livrés | **Trois défauts, deux bloquants.** B1 (parc et cadence pris hors du plan retenu, contre C3, D2, D1 et TV), B2 (durée de location contre le profil de grue de D2), M4 (loyer de base-vie : 41 600 MAD/mois ici, 35 000 chez D1, écart tu alors que celui de la grue est publié). À l'inverse, trois cohérences **vérifiées et justes** : masse de charpente lue chez B7c et jamais redéclarée ; pointe et moyenne lues chez D2 après lissage ; cage de poutre 0,9 t contre 1 738,6 kg pour deux poutres de 24 m chez B3e (869 kg/cage). |
| 6 | Grille de profondeur § 7.2 | Voir § 3 : **deux critères sous le minimum de 2**. |
| 7 | Sécurité | **Un bloquant par omission : B3** — la variante retenue met deux flèches sécantes (lentille de 725 m², visible en gris sur la capture 2) à la **même hauteur sous crochet** (45 m), et le module ne dit pas un mot d'anti-collision, de décalage de niveau, de zonage ni de survol de charge. Le reste est bien traité : girouette, famille « à proximité » de B7c, convention avec l'exploitant, pied de page qui renvoie à l'étude de levage et au plan de prévention. |
| 8 | Vérité du rendu | **Cinq captures ouvertes.** Figures 1, 3, 5 : lisibles, axes cotés, totaux qui recollent (1 460 + 6 682 = 8 142). Figure 4 : le badge d'alerte ne dit pas ce que la figure montre (**M9**). Figure 2 : collisions trait/texte (**m5**). Figure 3 : « 100 » sans décimale quand les autres en portent une (**m6**). Aucun `{{…}}` ni `⟦…⟧` résiduel dans la page. |
| 9 | Simplifications non signalées | **Trois.** La ligne de parc hors plan retenu, présentée comme « les retenus » dans la fiche livrée (**B1**) ; la location sur toute la durée, jamais déclarée comme majorant (**B2**) ; les bornes du taux de charge, combinaison des quatre extrêmes dans le même sens, dont on tire une règle de décision sans dire que ce n'est pas un intervalle de confiance (**M5**). Bien signalées, en revanche : le majorant sous grue sans parcelle, l'arrondi des modules, l'écart avec D1 sur la grue. |
| 10 | Télégraphique ou remplissage | **RAS sur la forme** — prose pleine, chaque paragraphe porte une règle, un nombre ou un piège. Une réserve de fond : une statistique inventée (**M7**) et une pointe annoncée puis non calculée (**M6**) tiennent lieu de calcul là où les données étaient à portée. |

---

## 2. Défauts

| # | Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|---|
| **B1** | **Le débit est calculé sur un chantier que le cours ne construit pas.** La demande de levage sort de la ligne « optimum de coût » de C3 — parc 430 m², cadence 8,05 j, plancher en 64,4 j — alors que D2, D1 et TV sont bâtis sur le parc **déclaré** 1 300 m², cadence 3,4 j, plancher en 31,85 j. C3 écrit noir sur blanc que cet optimum **n'est pas une décision** (D-041). Rien dans le module ne le dit ; la fiche livrée affirme même le contraire. | **bloquant** | `calc/installation.py:321` `ligne = next(x for x in go["parc"]["lignes"] if x.get("optimum_de_cout"))` ; `gros-oeuvre.json → parc.optimum_de_cout.duree_du_plancher_j = 64,4` contre `planification.json → durees.MEZZ.duree_j = 31,85` (= ligne 1 300 m²) ; `gros_oeuvre.coffrage.parcs_a_comparer` + `parc.parc_declare_m2 = 1300` ; `cadrage/05-sommaire.md:926` « gros-oeuvre.json (parc de coffrage et cadence **retenus**) » — faux. Recalcul § 0.2 : **37,0 levages/j et 101,6 %** au lieu de 22,7 et 62,3 %. | Lire `parc.parc_declare_m2` / `cadence_tenue_j` de la ligne correspondante, **ou** publier les deux lignes en disant laquelle le chantier exécute. Conséquence à assumer : la voie du débit passe au-dessus du seuil et son nominal vote pour 2 grues — ce qui renforce la conclusion mais détruit le § S3b, l'exercice 2, le quiz 3 et la ligne « ne tranche pas » de la fiche mémo tels qu'ils sont écrits. Corriger aussi le test (m1). |
| **B2** | **Deux grues à tour louées 29,7 mois pour 117 jours ouvrés de besoin.** Le module lit le profil de grue de D2 pour la voie « le temps », et lit la durée totale du chantier pour le loyer, sans voir que les deux se contredisent d'un facteur 5,4. Toutes les conclusions économiques du module en dépendent. | **bloquant** | `calc/installation.py:447` `loyer = (loyer_grue_mois × nb_grues + loyer_bv_mois) × duree_mois` avec `duree_mois = 29,7` ; `planification.json → durees` : tâches servies par la grue de `FOND` (j 19,86) à `MARQ` (j 136,53), `grue_resolution.resultat.profil` nul au-delà de j 136 ; fin de chantier j 599,84. Recalcul § 0.4 : loyer grue **1,03 MMAD** au lieu de 5,64 ; total **3,53 MMAD**, **part fixe 41 %**, **4,4 % du marché**. | Loyer de grue sur la **fenêtre d'emploi** (premier au dernier jour de tâche servie, convertie en mois calendaires par le facteur de D1), base-vie sur la durée totale. À défaut, déclarer explicitement le majorant et publier les deux chiffres. Et **réécrire les conclusions** : « la part fixe ne pèse que 18 % », « les quatre cinquièmes se jouent sur la date de fin », « un mois gagné rapporte 225 000 MAD » (figure 5, encart S5, § S3g) sont tous faux en l'état — un mois gagné **à la fin** ne rend aucun loyer de grue, les grues étant démontées depuis vingt mois. |
| **B3** | **Deux flèches sécantes, et pas un mot sur l'interférence.** La variante retenue pose G1 (30 ; 20) et G2 (90 ; 20), portée 40 m, entraxe 60 m : les cercles se recoupent sur **725 m²**, et les deux grues ont la même hauteur sous crochet (45 m). Aucune ligne sur l'anti-collision, le décalage de hauteur, le zonage, ni sur le survol de charge. Ce n'est pas un sujet ⏸ : c'est de la géométrie, c'est-à-dire exactement le domaine que le module revendique. | **bloquant** (sécurité, par omission) | `data → installation.variantes_de_calage[1]` et `grue.hauteur_sous_crochet_m = 45` ; capture figure 2, zone grise d'intersection ; `cadrage/05-sommaire.md:117` qui justifiait le modèle 3D de C1 par « **l'interférence de deux grues** et les zones de survol ne se lisent pas sur un plan masse plat » ; D-061 abandonne la 3D au motif que l'interférence « n'est pas ce que le module enseigne » — puis le module retient la variante à deux flèches sécantes. `grep -i "interfér\|collision"` sur le contenu : **0 occurrence**. | Un paragraphe en § S3a ou S3d : aire d'interférence calculée depuis `data/` (elle l'est en deux lignes), conséquence d'exploitation (décalage de hauteur sous crochet, dispositif anti-collision, grue amont/aval), et renvoi ⏸ pour les **exigences** de mise en service. Ajouter la ligne à la check-list S7 et aux points d'arrêt S8. |
| **M1** | **Trois jours de conflit transformés en une grue permanente.** D2 publie `nb_jours_en_conflit = 3` et trois issues, dont « compléter par une **grue mobile** » ou « déplacer une tâche ». C1 lit `parc_necessaire_si_non_resolu = 2` et en fait un vote pour une seconde grue à tour sur tout le chantier, à 3 421 500 MAD. | majeur | `planification.json → grue_resolution` : `nb_jours_en_conflit: 3`, `premier/dernier_jour_en_conflit: 26 / 28`, `verdict` qui énumère les trois issues ; `calc/installation.py:523` `par_temps = pl[...]["parc_necessaire_si_non_resolu"]`. | Reprendre la **condition d'emploi** de la grandeur empruntée (D-056) : la voie du temps dit « 2 grues **pendant 3 jours** ». Comparer les trois issues de D2 au coût publié de la seconde grue — c'est l'arbitrage que le module prétend enseigner au § S4-1. |
| **M2** | **La voie « géométrie » tranche sur un seuil non déclaré.** Elle retient la première variante dont la couverture ≥ **99,9 %**. La variante A en couvre 98,2 % : le manque est de **87 m² aux quatre coins**. Avec un critère à 98 %, la géométrie dit 1 grue, il ne reste qu'une voie qui tranche, et la décision change. | majeur | `calc/installation.py:528` `par_geometrie = min(... if c["couverture_pct"] >= 99.9 ...)` ; `couverture[0].couverture_pct = 98,2`. Le seuil n'apparaît ni dans le module, ni dans la sortie, ni dans un test. | Publier le seuil comme une **décision** (avec sa raison : ce qui reste non couvert est un angle, et un angle non couvert se manutentionne deux fois), et donner sa sensibilité — le module fait exactement cela pour le survol et pour le taux de charge, pas pour sa propre voie décisive. |
| **M3** | **« quinze pour cent du marché » contredit le 23,11 % que le module calcule lui-même.** Le nombre est écrit à la main dans le texte (§ 4.3 l'interdit) et il est faux depuis que `part_du_marche_si_somme_des_voies_pct` existe. | majeur | `content:400` « une installation qui pèse quinze pour cent du marché au lieu de 10,22 % » ; `installation.json → cout.part_du_marche_si_somme_des_voies_pct = 23,11` pour `parc_si_somme_des_voies = 5`. Présent dans le HTML reconstruit à 22:28. | Remplacer par la variable. |
| **M4** | **Le loyer d'un module de base-vie est présenté comme une entrée du coût ; il n'entre dans aucun résultat — et il contredit D1.** Le § S3g annonce « quatre de ses entrées » dont 2 600 MAD/mois par module ; le coût utilise la ligne forfaitaire de D1 (35 000 MAD/mois). Or 16 × 2 600 = **41 600 MAD/mois**, soit +19 % et ≈ 196 000 MAD sur la durée. L'écart avec D1 est publié pour la grue, tu pour la base-vie. | majeur | `calc/installation.py:439,447` (`loyer_bv_mois = fd["lignes"]["base_vie_et_fonctionnement"]["MAD_mois"]`) ; `content` § S3g ; `base_vie.modules = 16` ; `prix.json → frais_de_duree.lignes.base_vie_et_fonctionnement.MAD_mois = 35 000`. | Soit utiliser le loyer unitaire × le nombre de modules **calculé par ce module** et publier l'écart avec D1 comme pour la grue (D-055), soit retirer 2 600 MAD/mois de la liste des entrées et dire que la base-vie est chiffrée au forfait de D1. Un module qui dimensionne la base-vie et ne la chiffre pas sur son propre dimensionnement se contredit. |
| **M5** | **Les bornes qui « enjambent le seuil » sont la combinaison des quatre extrêmes dans le même sens** — capacité à 4 cycles/h **et** 40 % d'utilisation contre demande à 6 m²/levage **et** 25 divers. C'est une enveloppe de sensibilité, pas un intervalle : D1 le déclare explicitement pour sa propre fourchette, C1 ne le redit pas et en tire une **règle de décision** (D-059). | majeur | `calc/installation.py:316-318, 326-328` ; `debit.capacite_bornes = [12,8 ; 81,6]`, `demande_bornes = [11,9 ; 42,8]` → `[14,6 ; 334,4] %` ; `prix.json → fourchette_de_cout.lecture` (« Les deux bornes ne sont pas des probabilités […] elles mesurent la SENSIBILITÉ »). | Reprendre cette phrase dans C1, et montrer ce que donnent des bornes non corrélées (p. ex. une entrée à la fois) : avec le parc corrigé de B1, la voie trancherait probablement, et la règle D-059 se trouverait illustrée par un cas où elle **ne** s'applique pas — ce qui vaut mieux que par un cas construit sur une enveloppe maximale. |
| **M6** | **La pointe de demande est annoncée puis jamais calculée**, alors que les données lues la donnent. Le module écrit « le jour où l'on décoffre une zone et où l'on coffre la suivante, la demande double », et s'arrête. | majeur | `installation.json → debit._ce_que_le_taux_de_charge_cache` ; les entrées existent : `tranche-plancher.durees.coffrage_j = 1,77`, `cycle_zone.decoffrage_j = 0,5`, `coffrage_m2 = 424,3` → `2 × 424,3 / 2,27 = 37,4` levages de coffrage + 12 = **49/j, soit 136 % de la capacité**. D-040 : une conséquence se mesure, elle ne se déduit pas. | Calculer le jour de pointe et le publier à côté du taux moyen. C'est le seul chiffre de la section qui décide vraiment, et c'est le seul qui manque. |
| **M7** | **Statistique inventée** : « Une grue chargée à 80 % en moyenne est saturée un jour sur trois ». Aucun calcul, aucune borne, aucune balise V3 — R8. | majeur | `calc/installation.py:356-359`, publié tel quel dans § S3b. | Supprimer, ou la remplacer par le profil journalier de M6, qui dit la même chose en la mesurant. |
| **M8** | **Part du marché calculée sur la mauvaise base.** `marche = bordereau.prix_de_vente_MAD` (79,6 MMAD) alors que D1 écrit que le bordereau qu'on **signe** est celui avec la ligne de divers (102,5 MMAD). Sur cette base : **7,94 %**, pas 10,22 %. Ratio lu hors de son domaine (D-037, D-056). | majeur | `calc/installation.py:450` ; `prix.json → bordereau_avec_divers.lequel_on_signe` (« Celui-ci »). Le chiffre est répété cinq fois dans le module (S1, S4-6, S5-3, figure 5, fiche mémo). | Rapporter à l'offre, ou nommer la base dans le libellé (« % du bordereau de référence »), comme D1 le fait pour ses propres ratios. |
| **M9** | **Figure 4 : le badge dit le contraire de la figure.** L'étiquette d'alerte « le cercle atteint le gabarit » n'est posée que sur la barre A ; les trois variantes l'atteignent, et la première ligne du « ce qu'il faut voir » le dit. Un lecteur pressé conclut que seule A est concernée — c'est-à-dire exactement l'erreur que la section combat. | majeur | Capture `…figure4.png` : badge sur A seule, barres B (8 m) et C (2 m) sans badge ; `voisinage.aucune_variante_n_evite_le_gabarit = true`. | Badge sur les trois barres, ou badge réservé à la propriété qu'il désigne vraiment (« atteint le gabarit **même à la borne favorable** »), avec ce libellé-là. |
| **M10** | **D-061 appliqué à moitié.** La fiche livrée nomme l'abandon de O3 et la reprise de O7, mais pas l'abandon de la moitié du « contenu propre » de la fiche d'origine : **circulations et lavage de roues, réseaux provisoires, centrale à béton ou BPE, stockages**, ni le remplacement des quatre schémas annoncés (dont « circulations » et « réseaux provisoires ») par cinq autres. Un module « installation de chantier » sans circulations ni réseaux provisoires est un écart de **périmètre**. | majeur | `cadrage/05-sommaire.md:295-310` (fiche d'origine) contre `:893-947` (fiche livrée) ; `grep -i "circulation\|lavage de roues\|réseaux provisoires\|centrale"` sur le contenu : aucune occurrence hors de la liste ⏸. | Nommer les abandons et leur raison, ou dire qu'ils partent en C2/C6 — et le dire dans `STATE.md`, pas seulement dans la fiche. |
| **m1** | Tests : deux contrôles **dupliqués mot pour mot** (« le parc “somme des voies” est bien la somme » et « et il coûte strictement plus cher », deux fois chacun) ; et le contrôle « le parc de coffrage est celui que C3 publie, pas un autre » est **tautologique** : il relit la ligne `optimum_de_cout` que le code a choisie, donc il ne peut pas échouer et il **épingle** le défaut B1 au lieu de le chercher (D-041/D-043). | mineur | `calc/tests/test_installation.py`, sections 3 et 6. | Dédupliquer ; faire du test une **règle** : la cadence du débit doit être celle qui donne la durée de MEZZ au planning. |
| **m2** | « À la borne haute, une grue est chargée à plus de 300 % et **il en faudrait trois** » : 334 % en demande **quatre**. | mineur | `content:481` ; `taux_de_charge_bornes_pct[1] = 334,4`. | `ceil(3,34) = 4`, ou tourner la phrase sans le nombre. |
| **m3** | « Soit un peu plus du **tiers** de la portée » pour 25/60 = **41,7 %** (deux occurrences, dont l'exercice 1). | mineur | `content:103` et § S6-1. | « Un peu plus des deux cinquièmes », ou donner le rapport. |
| **m4** | Nombres techniques écrits à la main : « donnerait **cinq** grues » (l. 210), « donnerait **5** » (l. 476) — § 4.3. Ils sont justes aujourd'hui, et le seront jusqu'à ce qu'une voie change. | mineur | `content:210, 476` ; la sortie porte déjà `parc_si_somme_des_voies`. | Variabiliser. |
| **m5** | Figure 2 : l'arc du cercle G1 **traverse** les libellés « emprise 120 × 40 m » et « 25 m » de l'échelle. Le contrôle automatique ne voit que les collisions texte/texte. | mineur | Capture `…figure2.png`. | Halo blanc sous les libellés, ou déplacer l'échelle hors des cercles. |
| **m6** | Figure 3 : la barre B porte « 100 », les cinq autres une décimale. | mineur | Capture `…figure3.png`. | Format unique. |
| **m7** | La mise en girouette est énoncée comme une règle générale (« Une grue à tour hors service **est** mise en girouette ») sans balise ni renvoi ⏸, alors que c'est une prescription d'emploi — tout le reste du module est scrupuleux sur ce point. | mineur | `content:232` ; glossaire S7. | Une incise (« la pratique courante, dont les conditions sont ⏸ »). |
| **m8** | La portée déclarée de la grue — 60 m, registrée comme une **décision** — n'est celle d'aucune grue de la variante retenue (deux grues de 40 m). La fiche mémo publie pourtant « 25 m sur **60 m** de portée », et le coût applique à deux grues de 40 m le montage, le massif et le loyer d'une grue de 60 m. | mineur | `data → installation.grue.portee_m = 60` et `variantes_de_calage[1].grues[*].portee_m = 40` ; fiche mémo S8 ; `cout` (mêmes montants quelle que soit la portée). | Dire que les montants d'une grue de 40 m sont pris égaux à ceux d'une grue de 60 m (hypothèse conservatrice, à déclarer), et caler la ligne de la fiche mémo sur la variante retenue. |
| **m9** | **Le livrable a été modifié pendant la passe** (voir l'avertissement en tête) : quatre fichiers réécrits et build relancé à 22:28, deux défauts corrigés et un à moitié pendant la relecture. Une passe adversariale ne prouve rien si l'objet bouge : elle ne peut plus dire sur quelle version elle a conclu. | mineur | `git status` : `M STATE.md`, `M calc/installation.py`, `M content/11-…md`, `M data/registre-hypotheses.csv` à 22:27-22:28 ; `modules/…html` et captures réécrits à 22:28 ; HEAD = `996283e`. | Figer (commit) avant d'appeler la passe, et traiter les corrections **après** le rapport. |
| **m10** | `modules/*.html`, `calc/sorties/*.json` et `tests/captures/` sont hors git (`.gitignore`) : une passe ne peut rattacher ni une sortie ni une capture à un commit. C'est un choix assumé pour le zip de reprise, mais il prive la relecture de toute traçabilité — et c'est ce qui a rendu m9 invisible jusqu'au `ls -l`. | mineur | `.gitignore` ; `git show 996283e:calc/sorties/installation.json` → « exists on disk, but not in 996283e ». | Au minimum, que `check.mjs` écrive dans chaque rapport QA le hash de `data/` **et** l'horodatage du build qu'il a contrôlé. |

**Bilan : 3 bloquants · 10 majeurs · 10 mineurs.**

---

## 3. Grille de profondeur (§ 7.2) — minimum exigé : 2 partout

| Critère | Note | Justification |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | « Couvrir n'est pas lever » est une vraie idée, démontrée par la formule, mesurée sur trois variantes et retournée en piège. Le troisième axe (le cercle contre le gabarit) est posé comme allant en **sens inverse** des deux autres : c'est le genre de structure qu'un cours moyen n'a pas. |
| Les hypothèses sont explicites | **2** | Toutes les entrées V3 sont balisées, bornées et registrées. Mais trois hypothèses décisives ne le sont pas : le choix de la ligne de parc (B1), le seuil de couverture à 99,9 % (M2), et la nature des bornes du taux de charge (M5). |
| Les formules sont justifiées | **3** | `Q(r) = min(Qmax, M/r)` démontrée par ses deux régimes, lue dans les deux sens, étalonnée sur cas fermés (disque clippé, invariant d'additivité) ; l'étalonnage raconte même l'erreur qu'il a trouvée dans son propre invariant. |
| L'exemple est vérifié | **1** | La géométrie l'est (§ 0.1, écart ≤ 0,5 pt). Le débit et le coût — deux des quatre résultats du module — reposent l'un sur une entrée prise hors du plan retenu (B1), l'autre sur une durée que le planning du module dément (B2). Deux contrôles sur quatre ne valident rien. |
| Le piège est identifié | **3** | Sept erreurs fréquentes, toutes avec leur **symptôme de chantier**, et la revue critique de l'exercice 4 est la meilleure du palier : elle distingue le mauvais choix de l'**omission de pièce**. |
| Le lien avec l'exécution | **2** | Girouette, familles B7c, points d'arrêt, double lecture : solides. Mais l'interférence des flèches (B3), les circulations, le lavage de roues et les réseaux provisoires (M10) manquent, et ce sont des sujets d'installation, pas de calcul. |
| Le lien avec le coût et le délai | **1** | C'est la section la plus faible : le loyer court cinq fois trop longtemps (B2), la part du marché est rapportée à la mauvaise base (M8), le loyer de base-vie déclaré n'entre dans rien (M4), et la seconde grue est commandée pour trois jours de conflit (M1). Les quatre vont dans le même sens — ils **gonflent** le poste. |

**Verdict : deux critères sous le minimum de 2 — le module n'est pas livrable en l'état.** Les trois
bloquants se corrigent sans toucher au cœur du module : B1 est un changement de ligne lue, B2 un
changement de durée, B3 un paragraphe à écrire. Mais les trois **déplacent des conclusions publiées**,
et deux d'entre elles (« le débit ne tranche pas », « les quatre cinquièmes se jouent sur la date de
fin ») sont reprises dans la fiche mémo, dans deux exercices, dans le quiz et dans `DECISIONS.md`
(D-059) : la correction ne s'arrête pas au module.

---

## 4. Ce que cette passe apprend sur le contrôle

Les 16 contrôles de `npm run check`, les 69 contrôles de `test_installation.py`, l'étalonnage et la
vérification dimensionnelle étaient **tous verts** et aucun ne voit les trois bloquants. Ce qui les a
trouvés :

1. **Recalculer la demande de levage depuis `data/` par un autre chemin** — la cadence du plancher
   plutôt que le parc divisé par sa rotation. Les deux chemins donnent 37 et 23 : c'est l'écart qui
   dit qu'une des deux entrées vient d'ailleurs.
2. **Rapprocher deux nombres publiés par le même module à quatre sections d'écart** — le profil de
   grue de la voie « le temps » (j 20 → j 136) et la durée de location du § S3g (29,7 mois).
3. **Regarder les captures** — le badge de la figure 4, les collisions de la figure 2, et surtout la
   zone grise d'intersection des deux cercles de la figure 2, qui est le seul endroit du livrable où
   l'interférence des flèches apparaît.

Aucun des trois n'est outillable tel quel, mais deux le deviennent : un test « la cadence du débit
est celle qui produit la durée de MEZZ », et un test « toute grandeur multipliée par
`duree_mois_calendaires` nomme la fenêtre d'emploi de la ressource qu'elle loue ». Le second
attraperait aussi la ligne de frais de durée de D1, qui porte le même défaut depuis trois modules.

---

## 5. Suite donnée (par l'auteur, le 29/10/2026)

**Les trois bloquants sont corrigés, et chacun a déplacé un résultat publié.**

**B1 — le débit lisait un chantier que le cours ne construit pas.** `debit()` lisait la ligne
« optimum de coût » du tableau de parc de C3 (430 m² / 8,05 j) — une ligne dont C3 écrit lui-même
que ce n'est **pas** une décision. Elle lit désormais le coffrage **d'une zone**
(424,3 m², publié par la tranche verticale) et la **cadence du cycle** que le planning tient
(3,4 j, publiée par C3). Le relecteur avait raison sur le chemin et sur le chiffre : la demande
passe de 22,7 à **37,0 levages par jour**, et le taux de charge de 62,3 à **101,5 %**. Une erreur de
modèle s'ajoutait à l'erreur de source : le **parc** est un stock (ce qu'on possède,
1 300 m²), la **zone** est un flux (ce qui passe au crochet). Les deux s'écrivent en mètres carrés,
et c'est ce qui rend la confusion invisible. Le module en fait désormais un piège explicite, et un
canari du test vérifie que prendre l'un pour l'autre **change** le nombre publié.

*Et le verdict de D-059 survit, renforcé* : la voie du débit donne maintenant **le même nombre que
les deux autres** et ne tranche toujours pas. Une voie qui tombe du bon côté n'a pas plus le droit
de voter — c'est plus difficile à tenir, et plus utile à enseigner.

**B2 — deux grues louées 29,7 mois pour 117 jours ouvrés de besoin.** Exact, et c'est la faute que
le module dénonce ailleurs : confondre une ressource et un frais de durée. Nouvelle fonction
`fenetre_de_grue()` : les tâches que D2 déclare servies par la grue vont du jour 20 au jour 137, soit
**5,8 mois sur 29,7** — 19 % du chantier. Le coût se calcule maintenant avec **deux horloges** : les
grues sur leur fenêtre, la base-vie sur la durée du chantier. Total **3 597 700 MAD** au lieu de
8 142 500, part fixe **40,6 %** au lieu de 17,9, et l'écart avec D1 **change de signe** :
D1 surestime de 1 723 300 MAD au lieu de sous-estimer de 2 821 500. Trois conséquences écrites :
« un mois gagné » n'est plus une grandeur (225 000 MAD sur le gros œuvre, 35 000 à la fin, rapport
6,4) ; le **trou** de 2,2 mois avant la marquise se tranche par calcul (garder 421 800 MAD contre
démonter-remonter 840 000) ; et M1 est traité du même coup — 3 jours de conflit ne justifient pas une
grue à tour, c'est la **géométrie** qui paie la seconde.

**B3 — deux flèches sécantes, rien sur l'interférence.** Fondé. Nouvelle fonction
`interference()` et nouvelle section § S3e : lentille de **725,3 m²** (forme fermée, étalonnée sur
trois cas), **15,1 %** de l'emprise, deux crochets à la même hauteur puisque `data/` n'en déclare
qu'une. Le module énonce ce que la géométrie impose — **deux grues sécantes ne font pas deux fois une
grue**, et le taux de charge du § S3b compare à **une** — et met en ⏸ ce qu'il ne possède pas :
règles d'implantation, anti-collision, décalages de hauteur, priorités.

**Les dix majeurs.** M1 traité avec B2 · M2 : le seuil de 99,9 % est déclaré, avec les mètres carrés
qu'une variante à une grue laisse hors d'atteinte · M3 : le nombre était déjà calculé avant la passe
(23,11 %) · M4 : seconde voie publiée sur le loyer de base-vie — 16 modules à 2 600 font
41 600 MAD/mois contre 35 000 chez D1, **+18,9 %**, et le total garde la ligne de D1 pour rester
comparable · M5 : **sensibilité une à une** publiée, et les **quatre** hypothèses enjambent 100 %
chacune prise seule — le verdict ne tient donc pas à l'accumulation des extrêmes · M6 : la pointe se
calcule (61,9 levages, **170 %** d'une grue) · M7 : la statistique inventée est supprimée · M8 : les
**deux** bases de prix sont publiées, 3,51 % du prix qu'on signe et 4,52 % du bordereau de référence
· M9 : le badge de la figure 4 est retiré, l'axe porte l'information · M10 : les trois morceaux de
« contenu propre » abandonnés (centrale à béton ou BPE, circulations et lavage de roues, réseaux
provisoires) sont nommés dans le S1 et dans la fiche livrée, avec leur raison.

**Les mineurs.** m1 (tests dupliqués), m2 (« trois » au lieu de six à la borne haute), m3 (25/60
n'est pas « un peu plus du tiers »), m4 (nombres écrits à la main), m6 (format des barres), m7
(girouette énoncée comme une règle), m8 (la portée de 60 m n'est celle d'aucune grue de la variante
retenue) : tous corrigés. m5 (un arc de cercle traverse deux libellés de la figure 2) reste :
c'est la **dette 11** du cours, le contrôle de chevauchement ne compare que texte contre texte.
m10 est un choix d'architecture documenté.

**Et m9, qui est le plus important pour la suite.** Le livrable a été modifié pendant la passe. Le
relecteur a raison de le relever : c'est exactement la faute que D4 avait commise et que le cours
s'était interdite. Un livrable en relecture est figé. Le coût ici a été modeste — deux défauts
corrigés avant d'être lus, un à moitié — mais la règle n'a pas de bonne exception, et elle est
rappelée dans `STATE.md`.

**Ce que la passe laisse en dette.** Les deux contrôles qu'elle propose au § 4 ne sont pas
outillés : (1) « la cadence du débit est celle qui produit la durée de MEZZ » ; (2) « toute grandeur
multipliée par une durée de chantier nomme la fenêtre d'emploi de la ressource qu'elle loue ». Le
second attraperait la ligne de frais de durée de D1, qui porte le même défaut depuis trois modules —
et c'est précisément ce que ce module vient de découvrir par un autre chemin. Versé en dette 32.
