# B7b + C4 — Lots techniques et second œuvre · passe adversariale n° 1

> Relecteur hostile, indépendant de l'auteur. Les commentaires de `calc/synthese.py`, les encarts et
> les chaînes narratives publiées par `calc/` ont été lus **comme des affirmations à vérifier**,
> jamais comme des preuves. Les **cinq captures ont été ouvertes et regardées**. La contre-expertise
> du § 0 a été faite **avant** d'ouvrir `calc/synthese.py`, `calc/sorties/synthese.json` et le
> module, depuis `data/projet-gare.json` → `lots_techniques` et les sorties héritées seules
> (scripts jetés hors dépôt).
>
> État relu : commit `66b0a8f`, branche `claude/lance-etape-0-mode-b-ijn9r4`. **Aucun fichier du
> dépôt n'a été modifié pendant la passe**, et ni le build ni les tests n'ont été relancés.

---

## 0. Contre-expertise à l'aveugle — quatre recalculs

### 0.1 Le passage libre, et ce qui passe vraiment

Depuis `calc/sorties/ferraillage.json` seul (cadres HA8 à 10 et 20 cm ; nappes HA14 à 12,5 cm,
HA12 à 20 cm, HA14 à 12,5 cm) et le catalogue `diametres_courants_mm` :

```
espacement − Ø :  100−8 = 92 ·  200−8 = 192 ·  125−14 = 111 ·  200−12 = 188  (mm)
Ø max du catalogue :  80  ·  160  ·  100  ·  160
```

| Grandeur | mon calcul | publié | écart |
|---|---:|---:|---:|
| passage le plus étroit | **92 mm** | 92 | 0 |
| passage le plus large | **192 mm** | 192 | 0 |
| Ø qui ne passent nulle part | **200 · 250 · 315** | idem | 0 |

→ **l'arithmétique concorde exactement.** Mais j'ai ensuite calculé, **depuis les mêmes données**,
les deux autres barrières que la formule ignore — et elles changent les verdicts :

```
POUTRE, traversée verticale — largeur intérieure du cadre = 350 − 2×30 − 2×8 = 274 mm
                              3 HA25 au lit inférieur → (274 − 3×25)/2 = 99,5 mm entre barres
DALLE,  traversée (le seul cas réel) — un trou traverse les DEUX nappes :
                              l'ouverture est une maille 111 × 188 → Ø circulaire max = 111 → Ø100
```

Le tableau publié annonce **160 mm** pour « Dalle — nappe inférieure, répartition » : aucune
réservation de dalle ne peut en profiter, puisqu'elle doit aussi franchir la nappe porteuse à
111 mm. Idem pour la poutre traversée verticalement : 99,5 mm, soit Ø80, et non Ø160. S'ajoute que
`fer["nappes"]["lignes"][:2]` jette la 3ᵉ nappe (D3, chapeaux sur poutres, 144 m²) sans le dire, et
que les jeux restants — 16 mm par côté pour Ø160 dans 192, **5,5 mm** pour Ø100 dans 111 — sont du
même ordre que la tolérance de pose d'un espacement. La thèse « passage libre = espacement − Ø
suffit à conclure » est donc **nécessaire mais pas suffisante** : elle est juste pour refuser
(Ø200 ne passe nulle part : vrai), fausse pour autoriser.

### 0.2 Les huit dates de gel

Depuis `planification.json` (segment MEZZ : 45,8095 → 77,6595) et `gros-oeuvre.json`
(8 zones, cadence 3,4 j), avec le délai de 12 j :

| Grandeur | mon calcul | publié | écart |
|---|---:|---:|---:|
| premier gel | **37,2** | 37,2 | 0 |
| dernier gel | **61,0** | 61,0 | 0 |
| fenêtre | **23,8 j** | 23,8 | 0 |
| réservations (0,12 × 360 × 8) | **345,6 → 346** | 346 | 0 |

→ **concorde**, mais seulement parce que j'ai repris l'hypothèse du calcul : `coulage =
début MEZZ + z × cadence`. Cette hypothèse n'est écrite nulle part et ne vient pas de C3. Le cycle
de C3/TV place le bétonnage **à l'intérieur** du cycle de 8,05 j : coffrage 1,77 + ferraillage 3,87
= bétonnage à ≈ 5,6 j du début de zone (immobilisation 8,05 − cure 2,0 = 6,05 j de travaux). Les
dates deviennent alors 51,4 … 75,3 au coulage et **39,4 … 63,3 au gel**, soit **+2,2 j** sur les
huit dates publiées (et dans D-066).

### 0.3 Le coût d'un percement après coup

```
950 + 450 + 1 400 + 600 + 350 = 3 750 MAD   ·   3 750 / 120 = 31,25
bornes : (600+250+600+300+150)=1 900 ; (1 600+900+4 000+1 200+900)=8 600
         1 900/250 = 7,6   ·   8 600/60 = 143,3
```

| Grandeur | mon calcul | publié | écart |
|---|---:|---:|---:|
| percement | **3 750 MAD** | 3 750 | 0 |
| rapport | **31,25 → 31,2** | 31,2 | 0 |
| bornes du rapport | **7,6 – 143,3** | idem | 0 |

→ **concorde.** Deux remarques que les nombres imposent : les bornes croisent les extrêmes opposés
de deux fourchettes V3 indépendantes (à réservation nominale, le rapport va de 15,8 à 71,7) ; et
surtout **le carnet entier coûte 346 × 120 = 41 520 MAD**, alors que 2 % d'oublis coûtent
6,9 × 3 750 = **25 950 MAD**, soit 62 % du carnet. Le seuil d'équivalence est 120/3 750 = **3,2 %**.
La phrase du § S4 est fausse (→ B4).

### 0.4 La file de corps d'état — par simulation, pas par l'algèbre

File d'atelier (flow shop) : 6 corps, Z zones, durée par zone Wᵢ/Z, chaque corps enchaîne ses zones
dans l'ordre et ne peut entrer dans une zone qu'après le corps précédent. Tâches placées **une à
une**, sans forme fermée :

| Z | simulation f = 0 | forme fermée, 1ᵉʳ terme | simulation f = 0,4 | publié |
|---:|---:|---:|---:|---:|
| 8 | **61,25** | 61,25 ✔ | **65,65** | **78,05** |
| 18 | 52,22 | 52,22 ✔ | **60,62 ← vrai optimum** | 93,02 |

→ **le premier terme est exact** (61,25 au mm près, pour tout Z : la forme fermée du flow shop à
lignes identiques est bien (ΣW + (Z−1)·maxW)/Z). **Le second terme est faux.** `N·(Z−1)·f` additionne
à la durée les jours perdus par **tous** les corps, alors que seuls ceux qui tombent sur le chemin
critique l'allongent : les autres sont absorbés par l'attente que ces corps ont déjà. Le terme exact
est de l'ordre de (N + Z − 1)·f ≈ 5,2 j à Z = 8, et non 16,8 j. Conséquences : **78,0 j publiés
contre 65,7 j réels (+19 %)**, et un **optimum à 18 zones, pas à 7**. La thèse qualitative (un
optimum existe, il n'est pas à l'infini) survit ; le nombre, sa position et la conclusion de gestion
qu'on en tire ne survivent pas.

Le modèle suppose en outre, sans le dire : une seule équipe par corps, un travail parfaitement
divisible et de productivité indépendante de la taille de zone, le même ordre de zones pour tous,
aucun retour d'un corps dans une zone déjà quittée (or le plénum revient après les essais, la
peinture après les menuiseries), et aucun recouvrement partiel à l'intérieur d'une zone.

---

## 1. Les dix points du § 12.2

| # | Point | Constat |
|---|---|---|
| 1 | Unités et homogénéité | **RAS.** `verif_unites.py` l. 667-700 vérifie passage libre (longueur), densité × surface (sans dimension), date − délai (jours), file (jours). Recalculé : toutes homogènes. L'erreur de B1 est un défaut de **modèle**, pas de dimension — ce que la vérification dimensionnelle ne peut pas voir, et c'est la limite à connaître ici. |
| 2 | Référentiels mélangés | **RAS.** Aucun référentiel n'est invoqué : le module tient la phase § 5.0 avec constance (percement, coupe-feu, tolérances de planéité et d'humidité tous ⏸, y compris dans la fiche mémo). |
| 3 | Article cité sans V0/V1 | **RAS au sens strict** (aucun numéro d'article nulle part, aucune valeur V2). Réserve m9 : la règle centrale « une réservation qui coupe un cadre n'est plus une réservation » est publiée comme décision (D-065) sans niveau de preuve — c'est une convention professionnelle, sûre, mais non étiquetée. |
| 4 | Ordres de grandeur et ratios | **Défaut.** Le rapport 31,2 est juste ; l'usage qu'en fait le § S4 ne l'est pas (B4). Les bornes 7,6-143,3 croisent des extrêmes opposés (m5). Le prix Ø160 sert à chiffrer un trou Ø200 (m6). |
| 5 | Cohérence data / SVG / 3D / métré / coût / planning | **Défaut.** Dates de gel non lues dans le cycle de C3 (M1) ; 75 j de D2 lus hors de leur périmètre (B2) ; figure 2 : 8 × 43 = 344 ≠ 346 (m3) ; 5,62 × 8 = 44,96 ≠ 45 (m4). Le reste (346, 3 750, 31,2, 175, 45, 8 zones, 360 m²) recolle. |
| 6 | Grille de profondeur § 7.2 | **Défaut.** Trois critères sous le minimum de 2 — voir § 3. |
| 7 | Sécurité : conseil dangereux ou omission | **RAS.** La détection d'armatures avant carottage est posée en poste obligatoire et commentée ; le refus de chiffrer un percement en élément porteur est net ; la géométrie n'est jamais présentée comme une autorisation (répété quatre fois). Rien de dangereux. |
| 8 | Vérité du rendu | **Défaut.** Légende de la figure 2 inversée (B3) ; `**` littéraux × 7 dans la page rendue (M8) ; trois libellés tronqués en plein mot figure 5 (M9) ; ⏸ rendu en carré vide dans la capture 1 (m8) ; libellés sans accents figures 1 et 3 (m11). |
| 9 | Simplifications non signalées | **Défaut.** Le modèle de passage libre ignore les barres longitudinales et le croisement des nappes sans le dire (B5) ; la 3ᵉ nappe est jetée par `[:2]` (m12) ; les hypothèses de la file ne sont pas énoncées (§ 0.4) ; la date de coulage est supposée, pas lue (M1). |
| 10 | Texte télégraphique ou remplissage | **RAS.** Aucun paragraphe creux ; chaque section porte une règle, un nombre ou une méthode. Le défaut du module est inverse : des phrases trop affirmatives à côté de nombres justes. |

---

## 2. Défauts

| # | Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|---|
| **B1** | Le second terme de la forme fermée, `N(Z−1)f`, est faux pour une file pipelinée : il additionne au chemin critique les jours perdus par les corps qui attendent déjà. | bloquant | Simulation directe (placement tâche par tâche) : à Z = 8, **65,65 j** contre 78,05 publiés (+19 %) ; vrai optimum **Z = 18 à 60,6 j** contre « 7 zones, 78 j ». Le 1ᵉʳ terme, lui, est exact (61,25 = 61,25). | Remplacer par le terme exact (≈ (N+Z−1)f) ou, mieux, **calculer la file par simulation** et garder la forme fermée pour le seul cas f = 0 ; reprendre figure 4, `duree_a_Z_zones_j`, `zone_optimale`, l'exercice 2, le glossaire et la fiche mémo ; ajouter un cas d'étalonnage « forme fermée = simulation » qui aurait arrêté ce défaut. |
| **B2** | « Deux chemins qui ne partagent aucune donnée », « c'est le contre-calcul indépendant du § 3.3 » : la comparaison 78 / 75 est circulaire **et** hors périmètre. | bloquant | `data` → `forfaits_V3.second_oeuvre_lots_techniques_j` = 75, note : « forfait de synthèse : **le détail appartient à C4 et B7b** » ; le poste SECO couvre toute la gare, ascenseurs et escalators compris (14,5 MMAD, sous-traité), quand les 6 corps couvrent le **seul plancher de mezzanine** (2 880 m²). Les 7 paramètres V3 (6 durées + f) sont déclarés dans le **même commit** `66b0a8f`. D-043 et D-037. | Supprimer « accord à 4 % », « contre-calcul indépendant », « sans données communes » (S3b, encart, quiz 7) ; publier `_ce_n_est_pas_une_seconde_voie` comme B3e l'a fait après D-043, et dire que les deux nombres n'ont pas le même périmètre. |
| **B3** | La légende de la figure 2 dit l'inverse de ce que la figure montre : la barre va du **gel** au coulage, et la légende y place la fenêtre où « la réservation est encore modifiable… l'erreur se corrige à la gomme ». | bloquant | Capture 2, puce 3 et titre de la figure ; contredit `_ce_que_le_gel_veut_dire` (« après cette date, une réservation oubliée ne s'ajoute plus : elle se perce ») et toute la thèse D-066. La fenêtre « à la gomme » est **avant** la date de gel ; la barre tracée est celle de la commande, de la livraison et de la pose. | Retitrer la figure (« du gel au coulage : ce qui reste à faire quand il est trop tard pour décider ») et réécrire la puce ; ou tracer en plus la fenêtre ouverte, qui est celle qui intéresse le lecteur. |
| **B4** | « Sur les 346 réservations du plancher, deux pour cent d'oublis coûteraient à eux seuls plus que l'ensemble du carnet » : faux. | bloquant | 2 % × 346 × 3 750 = **25 950 MAD** contre 346 × 120 = **41 520 MAD** pour tout le carnet, soit 62 %. Seuil d'équivalence : 120/3 750 = **3,2 %**. | Écrire « au-delà de 3,2 % d'oublis, les percements coûtent plus que le carnet entier » — le chiffre est plus parlant que le faux. |
| **B5** | Le verdict « ce qui passe » est faux pour une traversée réelle : la formule ne regarde qu'une direction d'armatures. | bloquant | Depuis les mêmes données : dalle = maille **111 × 188** → Ø max **100**, et non 160 comme l'annoncent le tableau S2a, la figure 1 et le `_ce_que_ce_nombre_ne_dit_pas` ; poutre traversée verticalement = (274 − 3×25)/2 = **99,5 mm** entre les 3 HA25, soit Ø80. | Publier le passage libre comme une **maille** (min des deux directions) et ajouter la barrière des armatures longitudinales ; dire que la formule sert à **refuser**, jamais à retenir un Ø sans vérifier l'autre direction et le jeu de pose. |
| **M1** | La date de coulage de chaque zone est **supposée** (`début MEZZ + z × cadence`) au lieu d'être lue dans le cycle de C3, dans un module qui écrit « on LIT le réseau, on ne le suppose pas ». | majeur | `calc/synthese.py` l. 142, sans commentaire. Le cycle C3/TV place le bétonnage à ≈ 5,6 j du début de zone (1,77 coffrage + 3,87 ferraillage ; 8,05 − 2,0 de cure = 6,05 j de travaux) → gels à **39,4 … 63,3** au lieu de 37,2 … 61,0. D-039. | Lire la position du bétonnage dans le cycle, ou déclarer l'hypothèse et son biais (+2,2 j) ; corriger D-066 en conséquence. |
| **M2** | Deux canaris sur trois ne peuvent pas échouer, et le module s'en prévaut deux fois (« c'est vérifié par un canari des tests, pas affirmé »). | majeur | `test_synthese.py` l. 187-199 : « diviser par deux tous les corps sauf le goulot ne suffit pas » et « diviser le goulot par deux abaisse le plancher » sont vraies par construction de `max(W)`. Aucun cas de `calc/etalonnage/synthese_cas_ferme.py` ne teste le **terme de frontière** — exactement là où est B1. D-041. | Remplacer par un canari qui peut échouer : comparer la forme fermée à une **simulation** indépendante, avec et sans frontière. |
| **M3** | « L'optimum est à 7 zones » ne survit pas à sa propre fourchette, et l'écart avec Z = 8 est de 0,08 j. | majeur | Z* = √(ΣW−maxW)/(N·f) : **12 zones à f = 0,15 · 5 zones à f = 1,0**, les deux bornes déclarées. T(7) = 77,97 et T(8) = 78,05, tous deux imprimés « 78 j » (capture 4 : le marqueur et le minimum portent le même nombre). D-059. | Dire que le découpage du gros œuvre est **dans le plat** de la courbe, sans désigner d'optimum ; ou publier Z* pour les trois valeurs de f. |
| **M4** | « 47 % de ce coût ne tiennent ni à la machine ni à l'ouvrier : l'étude, le visa **et la remise en état** » — la remise en état (350 MAD) est de la main-d'œuvre pure (protection, nettoyage, reprises). | majeur | Capture 3, puce 3 et « erreur courante » ; § S5 n° 3 ; encart `_ce_que_le_rapport_cache`. Le chiffre défendable est **37,3 %** (étude et visa). | Garder 47 % mais changer la phrase (« ne tiennent pas à la machine »), ou garder la phrase et publier 37 %. |
| **M5** | « Le carottage n'est que 25 % du total : …et c'est la plus petite de celles qui comptent » — c'est le **deuxième plus gros** des cinq postes. | majeur | Capture 3 : 950 contre 1 400, 600, 450, 350. | « …et ce n'est que le deuxième poste : l'étude et le visa le dépassent. » |
| **M6** | « À 2 m de l'appui, on est dans la zone de cadres resserrés » contredit le ferraillage de B3e dont le § S4 tire son 92 mm. | majeur | `data` → `cadres.zones[0].segments_m` = [1,5 ; 2,5 ; 2,5 ; 2,5], « about de rive, deux appuis intermédiaires, about opposé » : 1,5 m depuis l'about, ± 1,25 m autour d'un appui intermédiaire. À 2 m d'un appui on est en **travée courante** (192 mm), pas à 92. | Dire « à 1 m de l'appui » (ou donner l'étendue du resserrement dans `data` et la lire). La conclusion du cas — Ø200 ne passe nulle part — reste vraie. |
| **M7** | « Un fourreau de 200 mm ne passe nulle part entre deux armatures **de ce chantier** » généralise une poutre et une dalle à toute la gare. | majeur | Résumé, § S1, D-065. Le calcul ne couvre que les cadres et nappes publiés par B3e pour **une zone** du plancher de mezzanine ; voiles, noyaux, poteaux, passerelle et quais n'ont pas d'armatures publiées. | Écrire « nulle part dans le plancher de mezzanine » — c'est tout aussi frappant et c'est vrai. |
| **M8** | La page rendue affiche **7 fois** des `**` littéraux : tout gras markdown venant d'une chaîne de `calc/sorties/` n'est pas interprété. | majeur | `modules/13-….html`, hors `<script>` : « ne passe donc `**`nulle part`**` », « sont `**`réglementaires`**` », « `**`Le carnet de réservations se joue…`**` », etc. Défaut récurrent : 5 en 09, 6 en 10, 8 en 11, 2 en 12, **7 ici**. | Passer les chaînes injectées dans le rendu inline du markdown (ou interdire le gras dans `calc/`), et ajouter un contrôle de build : aucun `**` dans la page hors `<script>`. |
| **M9** | Figure 5 : trois libellés coupés en plein mot, dont une parenthèse non fermée. | majeur | Capture 5 : « Réseaux en plénum (CVC, élec, CFa, », « Revêtements de sol de forte fréque », « Menuiseries, agencement, signaléti » ; `figures()` tronque à `[:34]`. | Tronquer au mot avec « … », ou publier un libellé court par corps d'état dans `data`. |
| **m1** | « Le second œuvre commence au jour 500 — **plus de** 439 jours plus tard » : l'écart vaut 438,84 j. | mineur | `_quand_le_carnet_se_joue` ; 499,84 − 61,0. | « près de 439 jours » ou arrondir à 440. |
| **m2** | Nombres techniques tapés à la main dans le contenu (§ 4.3, R1). | mineur | Résumé : « un fourreau de 200 mm », « gèle 439 jours avant » ; titre de l'exercice 1 : « 200 mm ». | Passer par les variables, comme le reste du module le fait. |
| **m3** | Figure 2 : 8 zones × « 43 réservations » = 344, alors que le texte en annonce 346. | mineur | Capture 2 et `reservations_sur_le_plancher`. | Afficher 43,2 ou écrire « ≈ 43 ». |
| **m4** | Durée par zone tronquée : 5,62 × 8 = 44,96 ≠ 45 j. | mineur | Tableau § S3a ; `round(45/8, 2)` = 5,62. | Trois chiffres significatifs (5,63) ou publier la somme contrôlée. |
| **m5** | Les bornes du rapport (7,6 – 143,3) croisent les extrêmes opposés de deux fourchettes V3 indépendantes. | mineur | `rapport_bornes` = [1 900/250 ; 8 600/60]. À réservation nominale : 15,8 à 71,7. | Publier les deux lectures, ou dire que les bornes sont le pire croisement possible. |
| **m6** | Le prix de 3 750 MAD (déclaré « percement de 160 mm ») sert à chiffrer le trou **Ø200** du cas du § S4. | mineur | § S4 point 4 et encart ; `percement_apres_coup_MAD._role`. D-037. | Dire « ordre de grandeur, établi sur un Ø160 ». |
| **m7** | « À la date d'arrêt, 8 zones sur 8 sont irrévocables, soit 100 % » ne peut pas être autre chose : le dernier coulage est au jour 73 et la date d'arrêt au jour 84. | mineur | `gel_des_reservations.lignes` ; marges toutes négatives (−46,8 à −23,0). | Dire que le plancher est coulé depuis onze jours ; le 100 % n'apprend rien. |
| **m8** | Le caractère ⏸ est rendu par un carré vide dans la capture 1 — sur le symbole qui porte toute la convention § 5.0. | mineur | Capture 1, bloc « erreur courante » : « réglementaire (▯) ». | Embarquer une police qui couvre U+23F8, ou remplacer par un libellé « ⏸ suspendu » stylé en CSS. |
| **m9** | La règle centrale du module (« une réservation qui coupe un cadre n'est plus une réservation ») ne porte aucun niveau de preuve. | mineur | § S2a, D-065, glossaire. Convention professionnelle, sûre, mais ni V0 ni V3. | L'étiqueter V3 (règle de conduite déclarée) et dire que le seuil réel est ⏸. |
| **m10** | La puce 4 de la figure 2 raisonne sur la date d'arrêt (jour 84) qui n'est pas sur le graphique (axe arrêté à ~75). | mineur | Capture 2. | Tracer le repère de la date d'arrêt. |
| **m11** | Libellés sans accents dans les figures 1 et 3 (« resserres », « travee », « inferieure », « repartition », « Detection d armatures », « etancheite »), alors que le corps du texte est accentué. | mineur | Captures 1 et 3 ; libellés hérités de `ferraillage.json` et clés `snake_case` retournées telles quelles. | Table de libellés d'affichage. |
| **m12** | `fer["nappes"]["lignes"][:2]` écarte la 3ᵉ nappe (D3, chapeaux sur poutres, 144 m²) sans que rien ne le dise. | mineur | `calc/synthese.py` l. 71. Elle donne le même 111 mm, donc le résultat ne change pas — mais la troncature est muette. | Boucler sur toutes les nappes, ou écrire pourquoi deux suffisent. |

**Total : 5 bloquants · 9 majeurs · 12 mineurs.**

---

## 3. Grille du § 7.2

| Critère | Note | Justification |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | Le gel, le goulot, la réception de support et la frontière géométrique sont expliqués par leur mécanisme, pas par leur définition. |
| Les hypothèses sont explicites | **1** | La date de coulage est supposée (M1), le modèle de file ne dit aucune de ses six hypothèses (§ 0.4), la formule de passage libre ne dit pas qu'elle ne regarde qu'une direction (B5). |
| Les formules sont justifiées | **1** | Le premier terme de la file est exact et bien expliqué ; le second est faux et n'est jamais dérivé (B1) ; la soustraction du passage libre est justifiée pour un cas de figure qui n'est pas celui d'une traversée (B5). |
| L'exemple est vérifié | **1** | L'étalonnage ne teste pas le terme fautif, deux canaris sur trois ne peuvent pas échouer (M2), et la seule « seconde voie » revendiquée est circulaire et hors périmètre (B2). Une arithmétique de tête est fausse (B4). |
| Le piège est identifié | **3** | Sept erreurs fréquentes, toutes avec leur symptôme de chantier ; les pièges nommés sont ceux qui coûtent vraiment. |
| Le lien avec l'exécution est fait | **3** | Carnet par zone, réception de support, double lecture entreprise / MOE dans l'exercice 3, check-list de visa : c'est le point fort du module. |
| Le lien avec le coût et le délai est fait | **2** | La chaîne de coût est juste (3 750, ×31) ; la chaîne de délai porte l'erreur de la file (B1) et le biais des dates de gel (M1). |

**Trois critères sous le minimum de 2** (hypothèses, formules, exemple vérifié) : le module ne passe
pas la § 7.2 en l'état.

---

## 4. La remarque de méthode

Comme pour D7, aucun des cinq bloquants n'est une faute d'arithmétique du `calc/` : les quatre
recalculs de la contre-expertise retombent **au chiffre près** sur les valeurs publiées. Ce qui est
faux, ce sont **le modèle** (un terme de file inventé plutôt que dérivé, une soustraction
unidirectionnelle présentée comme un verdict) et **les phrases** (une légende inversée, une
arithmétique de tête, une indépendance revendiquée qui n'existe pas). Un test qui recalcule la même
formule ne verra jamais cela ; une **simulation indépendante** du phénomène, elle, l'aurait vu en
une ligne — et c'est la seule parade à ajouter à `calc/etalonnage/`.

---

## 5. Suite donnée (par l'auteur, le 29/10/2026)

**Les cinq bloquants sont corrigés. Deux étaient des erreurs de MODÈLE — les premières de ce cours —
et trois des phrases fausses à côté de nombres justes.**

**B1 — le coût de frontière ne s'ajoute pas au makespan.** Fondé, et vérifié par ma propre
simulation avant toute correction : `forme fermée + N(Z−1)f` donne 78,0 j à huit zones quand la
simulation directe en donne **64,0**, et place l'optimum à 7 zones au lieu de 17. La raison est la
même que celle du module D7 sur les indicateurs consolidés : **ce qui est absorbé par une attente ne
se retrouve pas dans le total.** Chaque corps paie bien sa réinstallation, mais seuls les jours du
corps qui se trouve alors sur le chemin critique comptent. Le module calcule désormais la file **par
simulation** — on place les tâches une à une — et garde la forme fermée pour ce qu'elle est : exacte
à coût de transition nul, et référence de son étalonnage. Deux cas fermés figent l'écart pour qu'il
ne revienne pas, dont un qui rejoue explicitement la formule fausse.

**B2 — l'« accord à 4 % » était doublement illégitime.** Périmètre : D2 chiffre le second œuvre de
toute la gare (4 800 m²), la décomposition ne couvre que le plancher de mezzanine (2 880 m²).
Indépendance : les sept paramètres ont été posés dans le même mouvement que le module, en sachant
quel ordre de grandeur D2 affichait. **Deux voies ne sont indépendantes que si l'une ignore
l'autre.** La comparaison est retirée ; les deux périmètres sont publiés ; et le module écrit
pourquoi il ne compare pas — *une fausse preuve est plus nuisible qu'une absence de preuve*. Ce que
la décomposition apporte reste, et c'est dit : un **modèle pilotable** là où D2 ne donne qu'un bloc.

**B3 — la légende de la figure 2 inversait la thèse.** Exact. La barre court du gel au coulage :
c'est la période où le carnet est **clos** et le béton pas encore coulé, donc la dernière fenêtre
avant l'irréversible — et non « celle où l'erreur se corrige à la gomme », qui est la période
d'**avant**. Les trois temps sont maintenant nommés : la gomme avant le gel, la reprise pendant, la
carotteuse après.

**B4 — « 2 % d'oublis coûtent plus que tout le carnet » est faux**, et le seuil se calcule en une
division : c'est l'inverse du rapport, soit **3,2 %**, soit onze oublis sur 346. Publié comme tel.

**B5 — « espacement − diamètre » ne suffit pas, et c'est la correction la plus utile du lot.** Un
fourreau rond ne passe pas entre deux armatures : il passe dans une **maille**, et il y tient par la
plus petite de ses deux dimensions. La dalle n'est pas deux endroits mais une seule maille de
111 × 188 mm : le plus gros fourreau y est de **Ø100**, et non Ø160 comme le module l'écrivait. La
poutre a gagné sa largeur d'âme (274 mm entre les branches du cadre) et une troisième ligne — le
niveau des aciers inférieurs, où l'espacement libre entre les 3 HA25 tombe à 99,5 mm. Un canari
vérifie que prendre la plus grande dimension changerait le verdict. **La conclusion de tête survit a
fortiori : 200, 250 et 315 mm ne passent nulle part.**

**Les neuf majeurs.** Les dates de coulage étaient **supposées** (`début + i × cadence`) : elles se
déduisent désormais de la fin du segment MEZZ que D2 publie, en remontant à la cadence de C3 — les
huit gels se décalent de 2,2 j, et un canari refuse l'ancienne formule (D-039). L'optimum de
découpage est publié **avec sa plage** (11 à 29 zones selon le coût de frontière) parce qu'une voie
qui sert à décider porte ses bornes (D-059) ; et l'enseignement devient la **forme** de la courbe,
pas le nombre. « 47 % ni machine ni ouvrier » comptait de la main-d'œuvre : l'étude et son visa font
**37,3 %** à eux seuls, et tout ce qui n'est pas le trou en fait 62,7. « Le carottage est le plus
petit poste qui compte » : il est le **deuxième plus gros**, et un test le fige. « À 2 m de l'appui,
cadres resserrés » contredisait les segments de B3e : la distance disparaît du texte, qui dit
« près d'un appui » — et l'étude de cas vérifie aussitôt la question d'après, *et ailleurs sur la
poutre ?*, ce qui évite un second aller-retour.

**Et un défaut de chaîne que ce module a révélé pour tout le cours** : les chaînes publiées par
`calc/` portent du `**gras**` Markdown, mais elles sont injectées dans du HTML **déjà compilé** —
le gras sortait donc en toutes lettres. **62 occurrences dans six modules livrés.** Le build
convertit désormais le gras à l'injection, dans le HTML seulement. Aucun contrôle ne le voyait :
c'est la dette 13 — rien ne vérifie qu'une page montre ce qu'elle prétend montrer.

**Les mineurs** : libellés tronqués au mot (figure 5), canaris renforcés, et la grille § 7.2 reprise
— les trois critères sous le minimum portaient tous sur les deux erreurs de modèle, qui sont
corrigées et chacune couverte par un cas fermé **et** un test de règle.

**Ce que cette passe apprend, et qui vaut pour la suite.** Pour la première fois, une erreur n'a été
trouvée ni par un recalcul ni par une capture, mais par une **simulation indépendante du modèle**.
Une forme fermée se vérifie contre un cas limite ; un modèle, lui, se vérifie contre une exécution
directe. Les deux prochains modules qui poseront une formule de planning devront porter leur
simulation dès l'écriture — c'est versé en dette.
