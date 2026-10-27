# B7c — passe adversariale n° 1

> Relecteur hostile et indépendant (Annexe 4). Je n'ai lu ni les commentaires de `calc/`, ni les
> encarts du module avant d'avoir recalculé. Les contrôles automatiques sont **verts (16/16)** et
> `calc/tests/test_ferroviaire.py` affiche « tous verts » : aucun des défauts ci-dessous n'est vu
> par un test.
>
> **33 défauts : 11 bloquants · 14 majeurs · 8 mineurs.**

---

## 0. Contre-expertise à l'aveugle

Recalcul depuis `data/projet-gare.json` **seul**, sans lire `calc/plage.py` ni `calc/ferroviaire.py`.

```python
import json, math
D  = json.load(open('data/projet-gare.json'))
v  = lambda x: x['valeur'] if isinstance(x, dict) and 'valeur' in x else x
P  = D['ferroviaire']['plage_travaux']
SI = D['ferroviaire']['sous_interception']
CE = D['planning']['contraintes_exploitation']
hj = D['planning']['calendrier']['heures_par_jour']            # 8

# 1 — travail effectif et rendement d'une plage
fixe = sum(v(P[k]) for k in ('prise_de_possession_h','consignation_catenaire_h',
                             'amenee_des_moyens_h','repli_des_moyens_h',
                             'deconsignation_h','marge_de_restitution_h'))      # 3,15 h
Dn   = v(P['duree_nominale_h'])                                                 # 6,0 h
trav = Dn - fixe                                                                # 2,85 h
rend = trav / Dn                                                                # 47,50 %
ab    = v(P['abattement_de_cadence_nuit_pct']) / 100                            # 0,30
equiv = trav * (1 - ab)                                                         # 1,995 h-jour

# 2 — facteur d'interception
fac = hj / equiv                                                                # 4,0100

# 3 — plages, fenêtres, étalement
surf    = D['geometrie']['emprise_m'][0] * D['geometrie']['emprise_m'][1]        # 4 800 m²
tonnage = surf * v(D['planning']['ratios_quantites_V3']['charpente_kg_m2']) / 1000   # 312 t
cad     = v(D['planning']['cadences_chantier_V3']['charpente_t_j_atelier'])      # 9 t/j
nat     = D['planning']['effectifs_chantier_V3']['ateliers_charpente']           # 1
j_total = tonnage / (cad * nat)                                                  # 34,667 j
part    = v(CE['part_levage_sous_consignation_pct']) / 100                       # 0,35
t_si    = tonnage * part                                                         # 109,20 t
t_plage = cad * nat * equiv / hj                                                 # 2,2444 t/plage
n_plages = t_si / t_plage                                                        # 48,655 -> 49
n_fen    = math.ceil(49 / v(CE['fenetre_jours']))                                # 17
etal     = (n_fen - 1) * v(CE['periode_entre_fenetres_jours']) + v(CE['fenetre_jours'])  # 323 j

# 4 — coût d'une heure utile
comp = v(D['prix_unitaires_MAD']['ressources']['main_oeuvre_MAD_h']['compagnon']) # 45 MAD/h
tn   = comp * (1 + v(P['majoration_horaire_nuit_pct']) / 100)                     # 67,5 MAD/h
cout_h_utile = tn * Dn / trav                                                     # 142,11 MAD/h
rapport_ouvrage = cout_h_utile / comp / (1 - ab)                                  # 4,511
```

| # | Grandeur | Mon recalcul | Publié | Verdict |
|---|---|---:|---:|---|
| 1 | Travail effectif d'une plage | **2,850 h** | 2,85 h | identique |
| 1 | Rendement | **47,50 %** | 47,5 % (mais « 48 % » dans tous les textes) | voir m‑1 |
| 2 | Facteur d'interception | **4,0100** | 4,01 | identique |
| 3 | Tonnage sous interception | **109,20 t** | 109,2 t | identique |
| 3 | Tonnes par plage | **2,2444 t** | 2,24 t | identique |
| 3 | Nombre de plages | **48,655 → 49** | CHLV = 48,65 « j » | identique — **mais l'unité est une plage de nuit, pas un jour** (B‑4) |
| 3 | Fenêtres | **17** | 17 | identique |
| 3 | Étalement (réseau nu, 1re fenêtre j 40) | **323 j** | 320,6 j (1re fenêtre j 140, imposée par CHAP) | cohérent |
| 4 | Coût de l'heure utile | **142,11 MAD/h** | 142,11 MAD/h | identique — **mais au mauvais taux** (M‑5) |
| 4 | Rapport à l'heure d'ouvrage de jour | **4,511** | ×4,5 | identique |

Recalculs complémentaires, tous reproduits :
`masse max en plage de 6 h = 2,85 × 0,7875 = **2,244 t**` · `plage minimale pour 8 t = 3,15 + 8/0,7875 = **13,31 h**` ·
`chantier avant correction (facteur neutralisé à 1,0) = **362,92 j**, CHLV 12,13 j, 5 fenêtres, étalement 80,13 j, immobilisation 68 j`.

**L'arithmétique du module est juste. Ce qui ne l'est pas, c'est ce que les nombres veulent dire,
ce que les autres modules en font, et ce que le module en conclut.**

Quatre recalculs qui ne figurent nulle part et qui démolissent les conclusions :

```python
# A — le même poste, vu par D2 et par D1
#     D2 : 48,65 j x 10 compagnons x 8 h           = 3 892 h
#     D2, si la « journée » est une plage de 6 h   = 2 919 h
#     D1 (bordereau, CHLV, heures_totales)         =   971 h      -> écart x4,01
# B — rendement par heure de FERMETURE (exercice 2)
#     4 h : 0,2125 h utile/h   6 h : 0,4750   8 h : 0,6062   10 h : 0,6850
#     4 h contre 10 h = 3,22 fois moins (le module écrit « cinq fois »)
#     à fermeture égale, 4 h contre 6 h = 2,24 fois moins (le module écrit « 1,7 »)
# C — masse levable sous chaque levier publié
#     plage  6 h -> 2,24 t    8 h -> 3,82 t    10 h -> 5,39 t   ... pour une pièce de 8 t
# D — fourchette du facteur, jamais publiée
#     borne haute (plage 8 h, part fixe 1,70 h, abattement 15 %) -> x1,49
#     borne basse (plage 4 h, part fixe 6,50 h, abattement 45 %) -> INFAISABLE (utile = -2,50 h)
```

---

## 1. Les dix points du § 12.2

**(1) Unités et homogénéité.** **DÉFAUT.** `calc/verif_unites.py:253-266` vérifie bien les dimensions
(h, t/h, MAD/h) — mais la dimension n'est pas l'unité. `durees_chantier` écrit
`CHLV.duree_j = 48,65` : ce nombre est un **nombre de plages de nuit de 6 h**, pas un nombre de
jours ouvrés de 8 h. `pint` ne peut pas le voir, tout est en « jours ». Tout l'aval le lit comme un
jour de 8 h (B‑4). Preuve : `t_plage = 9 t/j × 1,995 h / 8 h = 2,2444 t` et `109,2 / 2,2444 =
48,655` — le « 48,65 j » publié **est** le compte de plages.

**(2) Référentiels mélangés.** RAS — aucun référentiel n'est invoqué (§ 5.0 respecté sur ce point).
Preuve : `grep "⟦V2\|⟦V1\|⟦V0" content/07-b7c-*.md` → 0 occurrence ; les 10 balises sont V3.

**(3) Article cité sans V0 ni V1.** **DÉFAUT** (B‑8) : « les 272 jours d'immobilisation improductive
**ne sont facturables à personne** » (figure 3, encart « erreur courante ») est une affirmation
**contractuelle** sans V0, en phase § 5.0, et contredite par `calc/sorties/prix.json` →
`frais_de_duree.total_MAD = 9 741 600` au déboursé **et** au prix de vente.

**(4) Ordres de grandeur et ratios.** **DÉFAUT.** Aucune vérification d'ordre de grandeur dans S4
(socle S4 : « … → résultat → **vérification d'ordre de grandeur** »). Et le seul ratio qui en tient
lieu — 2,24 t par nuit — n'est jamais confronté au fait qu'une grue lève une pièce en une heure :
le module conclut « 49 nuits » sans jamais dire que cela représente **moins d'un tiers de pièce par
nuit** alors qu'une pièce ne se fractionne pas (B‑5).

**(5) Cohérence data / SVG / 3D / métré / coût / planning.** **DÉFAUT MAJEUR, démontré poste par
poste.** `durée × effectif × 8 h` (D2) contre `heures_totales` (D1) :

| tâche | durée D2 | eff. | D2 (h) | D1 (h) | écart |
|---|---:|---:|---:|---:|---:|
| TERR, FOUI, FOND, RADT, VOIL, PHNT, POTR, COUV, FACA | — | — | — | — | **×1,00** |
| CHAP | 22,53 j | 10 | 1 802 | 1 803 | ×1,00 |
| **CHLV** | **48,65 j** | **10** | **3 892** | **971** | **×4,01** |
| MEZZ | 31,85 j | 27 | 6 880 | 3 219 | ×2,14 *(dette antérieure)* |

Les deux modules étaient d'accord **partout** avant B7c. B7c a cassé l'accord sur exactement une
tâche, d'exactement le facteur d'interception. (B‑3)

**(6) Grille de profondeur (§ 7.2).** **DÉFAUT** : 1/3 sur « l'exemple est vérifié » et sur « lien
avec le coût et le délai ». Détail au § 3. Le minimum de 2 partout n'est pas atteint.

**(7) Sécurité : conseil dangereux ou omission.** **DÉFAUT** (B‑6). Le module démontre en S4a qu'une
pièce de 8 t ne tient dans aucune plage, puis recommande en S4c, comme meilleur levier, de **réduire
la part levée sous interception en pré-assemblant au sol** — c'est‑à‑dire de **lever des pièces plus
lourdes** au‑dessus de la voie. À 18 t (haut de la fourchette déclarée de H173), il faudrait une
plage de **26,0 h**. Le module nomme la contrepartie (« pièces plus lourdes, grue plus forte ») mais
ne refait jamais le calcul du point de non‑retour avec la pièce alourdie : il recommande ce qui
aggrave la seule contrainte dont il a dit qu'elle arrête un train.

**(8) Vérité du rendu.** **DÉFAUT BLOQUANT** (B‑1, B‑2). Le tableau central du module (S3a,
« La décomposition d'une plage ») est **cassé au rendu** et **décalé d'un cran dans la source**. Voir
la preuve HTML au § 2.

**(9) Simplifications non signalées.** **DÉFAUT.** Trois, aucune déclarée : le levage est traité
comme divisible (B‑5) ; PSOU, soumise à consignation, ne reçoit pas le facteur (B‑10) ; la
« mesure » des leviers rejoue le code de D2 avec les données de D2 — c'est la même voie, pas une
seconde (M‑2, D‑043 impose de le dire).

**(10) Texte télégraphique ou remplissage.** RAS. Preuve : S2, S3b, S3c, S4a et S4c enchaînent
intuition → modèle → formule → exemple → piège sans paragraphe creux ; les exercices sont corrigés
en pleine phrase. C'est le point fort du module, et c'est ce qui rend ses erreurs convaincantes.

---

## 2. Défauts

### Bloquants

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **B‑1 · Le tableau central de la plage attribue 6 h à la prise de possession et totalise 11,6 h pour une plage de 6 h** | bloquant | `content/07-b7c-*.md:66-72` : la ligne `{{…detail.0.poste}}` (« Prise de possession, balisage ») porte la balise `⟦V3\|durée d'une plage de consignation accordée\|6\|h…⟧`, la ligne `detail.1` (« Consignation caténaire ») porte `0,50`, la ligne `detail.2` (« Amenée des moyens ») porte `0,75`. Les libellés viennent de `detail[0..2]`, les valeurs des balises **décalées d'un rang**. Somme affichée : 6 + 0,50 + 0,75 + 2,85 + 0,50 + 0,50 + 0,50 = **11,60 h** pour une plage de 6 h. La figure 1 juste en dessous (capture `07-b7c-…figure1.png`) affiche 0,5 / 0,75 / 0,4 : **le tableau et la figure se contredisent sur la même page.** Le test `test_ferroviaire.py:37` « le detail publie totalise exactement la plage » contrôle le JSON, pas le tableau — il est vert. | Ne pas réécrire les valeurs dans les balises : balise porteuse de la seule référence, valeur injectée par `{{ferroviaire.plage.detail.N.h::n2}}`. Ajouter au build un contrôle « une ligne de tableau dont la 2ᵉ cellule est un nombre doit être une variable ». |
| **B‑2 · 8 balises de preuve sur 10 sont rendues en syntaxe brute et font éclater les tableaux** | bloquant | `modules/07-b7c-*.html` : `grep -c "⟦V3"` → **8** ; `grep -c 'class="preuve preuve-V3"'` → **2**. Cause : `build/md.mjs:106` découpe la ligne de tableau sur `\|` **avant** `inline()`, donc `⟦V3\|réf\|valeur\|unité\|fourchette\|année\|note⟧` devient 7 cellules. Rendu réel : `<td>⟦V3</td><td>durée d'une plage…</td><td>6</td><td>h</td><td>4 à 8</td><td>2026</td>…` dans un tableau à 4 colonnes d'en‑tête. Le même bug existe dans D2 (7 occurrences) et B3e (2) et a franchi leurs passes. | Protéger les balises avant le découpage des cellules (masquage `\u0000B<n>\u0000` comme pour les maths et le code), puis les restituer dans `inline()`. Ajouter un contrôle : `⟦` ne doit jamais subsister dans un `modules/*.html`. |
| **B‑3 · D1 et D2 publient deux nombres d'heures pour le même levage, dans un rapport de 4,01** | bloquant | Tableau du § 1‑(5). `prix.py:194-217` ne lit pas la durée : `h/unité = heures_par_jour × compagnons / cadence_atelier = 8 × 10 / 9 = 8,889 h/t`, inchangée par la correction. `prix.json` → CHLV : `heures_totales 970.8`, `taux 47,5 MAD/h`, aucune majoration de nuit. `planification.json` → CHLV : 48,65 j × 10 compagnons. **D‑045 affirme « D1 (frais de durée, trésorerie) et D4 suivent par le build » : les frais de durée ont suivi (5,9 → 9,74 MMAD), la main‑d'œuvre du poste n'a pas bougé d'une heure.** | Trancher explicitement : soit la sujétion de nuit entre dans le sous‑détail de CHLV (heures = plages × effectif × durée de plage, taux majoré), soit D1 déclare que le poste est chiffré hors sujétion et le dit. Dans les deux cas, un contrôle `heures D1 == durée D2 × effectif × h/jour` pour toute tâche calculée, avec CHLV et MEZZ comme exceptions **nommées**. |
| **B‑4 · La durée de CHLV est un nombre de nuits de 6 h, consommé partout comme des jours de 8 h** | bloquant | `planification.py:148-152` : `CHLV = j_total × part × facteur`. Or `j_total × part × facteur = (t_si / t_plage)` exactement : 109,2 / 2,2444 = **48,655 = le nombre de plages**. En aval : `effectifs_par_tache` donne 10 compagnons, `histogramme_effectifs` les pose sur 49 **jours**, `courbe_en_s` compte 487 jours‑hommes (contre 121 avant) sur un total de 7 265, `prix.frais_de_duree` les facture en jours ouvrés. Le travail n'a pas quadruplé : **le temps s'est étiré.** Si la « journée » est une plage de 6 h, les heures‑hommes réelles sont 2 919 et non 3 892 : **surcompte de 33 %** même après correction. Et le tableau S4b les nomme « **Durée de travail** de la tâche de levage ». | Publier deux grandeurs distinctes : `nb_plages` (48,65) et `duree_calendaire_j`. Faire porter aux ressources et au coût la durée de plage réelle (`nb_plages × durée_de_plage_h`) et non `× heures_par_jour`. Renommer la ligne du tableau S4b en « nuits de consignation nécessaires ». |
| **B‑5 · Le compte de 49 plages suppose le levage divisible, que le module démontre indivisible deux sections plus haut** | bloquant | S4a : `masse_maximale_d_une_piece_t = 2,24 t`, `masse_d_une_piece_t = 8 t`, `l_operation_tient_dans_la_plage = false`, et l'encart « _un_levage_ne_se_fractionne_pas ». S4b/S4c : les 49 plages viennent de `109,2 t ÷ 2,2444 t/plage`, c'est‑à‑dire de **tranches de 2,24 t**, soit 0,28 pièce par nuit. Les deux modèles ne peuvent pas être vrais ensemble : ou les pièces pèsent ≤ 2,24 t (et H173 est faux), ou le planning de 600 j est infaisable, pas « long ». Le module publie les deux sans les confronter. | Calculer le nombre de plages par **pièces entières** : `plages = nb_pièces × ⌈durée_opération / travail_effectif⌉`, qui lève si une pièce ne tient pas dans la plage. Le résultat n'est alors pas « 600 jours » mais « la méthode déclarée est infaisable » — ce qui est le vrai enseignement. |
| **B‑6 · Le levier recommandé alourdit les pièces, donc aggrave le point de non-retour, et le module ne le calcule pas** | bloquant | S4c, lignes 4 à 7 : « Pré‑assembler au sol : part 35 → 15 % », donné comme le meilleur levier mesuré (−195 j, puis −237 j combiné). `ce_que_le_calcul_ne_price_pas` mentionne « pièces plus lourdes » **en prose**, jamais en chiffres. Recalcul : plage minimale = 3,15 + m/0,7875 → 12 t : **18,4 h** ; 18 t (haut de H173) : **26,0 h**. Aucune des plages proposées (6, 8, 10 h) ne permet de lever la pièce de 8 t actuelle (max 2,24 / 3,82 / 5,39 t), *a fortiori* une pièce pré‑assemblée. | Rejouer le point de non‑retour **dans chaque ligne de leviers**, avec la masse de pièce qu'implique la part retenue. Un levier qui rend l'opération plus infaisable n'est pas un levier : la ligne doit le dire, et la figure 2 ne doit pas le classer « meilleur ». |
| **B‑7 · La démonstration de l'exercice 2 compare 8 h de fermeture à 6 h en les déclarant égales, et ses deux ratios sont faux** | bloquant | S6, exercice 2 : « Deux plages de 4 h donnent 1,7 h utile, là où une seule plage de 6 h en donne 2,85. **Le même nombre d'heures de fermeture** produit 2,85 / 1,7 ≈ 1,7 fois moins d'ouvrage. » Deux plages de 4 h = **8 h** de fermeture ; une plage de 6 h = **6 h**. Ce ne sont pas les mêmes heures. À fermeture égale (6 h) : 1,5 × 0,85 = 1,275 h utiles contre 2,85 → **2,24 fois moins**, pas 1,7. Plus loin : « à 4 h elle produit **cinq fois moins** par heure de fermeture qu'à 10 h » — recalcul : 0,6850 / 0,2125 = **3,22**. L'argument est vendu au lecteur comme « un calcul, il se vérifie » : il ne se vérifie pas. | Reconstruire le corrigé sur l'heure de fermeture : rendement = (p − 3,15)/p, et comparer à p égal. Les deux ratios deviennent des variables (`::n2`) tirées de `calc/`, pas des nombres tapés. |
| **B‑8 · « Les 272 jours d'immobilisation improductive ne sont facturables à personne » est contredit par le bordereau du cours** | bloquant | Figure 3, encart « erreur courante ». `prix.json` → `frais_de_duree` : 29,7 mois × 328 000 MAD = **9 741 600 MAD**, portés au **déboursé sec** (67,9 MMAD) et au **prix de vente** (79,5 MMAD) ; `cout_du_retard.1.frais_de_duree_MAD = 16 240 MAD par jour ouvré`. Ces 272 jours sont donc facturés — dans le prix. Par ailleurs l'affirmation est **contractuelle** (qui supporte une sujétion connue au marché), sans V0, ce que le § 5.0 interdit. | Remplacer par ce que le cours sait prouver : « ces 272 jours ne produisent aucun ouvrage, et ils coûtent 16 240 MAD/j de frais indexés sur la durée, soit 4,4 MMAD, qu'il faut avoir mis dans le prix — ou perdre ». |
| **B‑9 · « Les deux premiers leviers gagnent presque autant l'un que l'autre. Ce n'est pas une coïncidence » : faux deux fois** | bloquant | Figure 2, « ce qu'il faut voir », 3ᵉ puce (capture `07-b7c-…figure2.png`). (a) Les deux premiers **leviers** du graphique sont « plage 8 h » (−137,1 j) et « plage 10 h » (−195,6 j) : ils ne gagnent pas autant. (b) Les deux lignes qui s'égalisent sont « plage 8 h » (−137,1) et « part 20 % » (−137,8), et leur égalité vient de ce que les produits `part × facteur` valent 0,826 et 0,802 — deux nombres choisis — **puis** de la quantification en fenêtres (10 fenêtres dans les deux cas). Agir « sur les deux facteurs du même produit » n'impose aucune égalité : c'est exactement une coïncidence, et la légende affirme le contraire. | Supprimer l'affirmation ou la remplacer par le fait mesurable : « ces deux leviers agissent sur les deux facteurs d'un même produit ; ils s'égalisent ici parce que les valeurs retenues donnent des produits voisins et tombent sur le même nombre de fenêtres. » |
| **B‑10 · PSOU est soumise à consignation et ne reçoit pas le facteur : la thèse du module n'est appliquée qu'à une tâche sur deux** | bloquant | `data/projet-gare.json` → `planning.contraintes_exploitation.taches_soumises = ["CHLV","PSOU"]`. `planification.py:146-152` n'applique le facteur qu'à CHLV ; PSOU reste un forfait de 9 j (`forfaits_V3.passage_souterrain_j`, note : « raccordement **sous consignation** »). `planification.json` → PSOU : 9 j de travail, 3 fenêtres, 43 j d'étalement — sans rendement de plage. B7c ne mentionne jamais PSOU. | Soit appliquer le facteur aux deux tâches, soit déclarer dans `data/` que le forfait PSOU est **déjà exprimé en plages** — et l'écrire dans le module. Un contrôle : toute tâche de `taches_soumises` porte le facteur ou une exemption nommée. |
| **B‑11 · « Les 363 jours n'étaient atteignables qu'avec cette méthode » : conclusion tirée d'une coïncidence de quantification** | bloquant | S4c, encadré « ce que ce tableau établit, et c'est le résultat du module », et figure 2 1re puce. Recalcul du planning d'avant correction (facteur neutralisé) : **362,92 j**, CHLV 12,13 j, 5 fenêtres. Levier « 15 % + plage 8 h » : **363,02 j**, CHLV **12,25 j**, 5 fenêtres. L'égalité vient de ce que `0,35 × 1,00 = 0,350` et `0,15 × 2,36 = 0,354` — et de l'arrondi des deux à « 363 ». Les deux plannings ne sont pas le même : CHAP passe de 22,53 à **29,47 j**, le profil de ressources change. Une infinité d'autres combinaisons donnent le même produit : rien n'établit que *cette* méthode‑là était celle qu'il fallait. D‑046 grave cette coïncidence en décision. | Publier le fait, pas l'interprétation : « il existe des combinaisons méthode × plages qui ramènent le chantier à sa durée d'origine ; en voici une. » Et publier la courbe `durée = f(part × facteur)` plutôt qu'un point qui tombe juste. |

### Majeurs

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **M‑1 · Aucune durée publiée ne porte sa fourchette (D‑036), et les bornes de D2 ignorent les sept paramètres qui portent désormais le chemin critique** | majeur | Le module publie 600 j, 363 j, 17 fenêtres, 320,6 j, ×4,01 et sept durées de leviers : aucune borne. `planification.py:945-957` (`variante_aux_bornes`) borne les cadences, forfaits, délais, recouvrements, `fenetre_jours`, `periode`, `premiere_fenetre_jour`, `part_levage` — et **aucun** paramètre de `ferroviaire.plage_travaux`. Recalcul des bornes réelles du facteur : haute **×1,49** (plage 8 h, part fixe 1,70 h, abattement 15 %) ; basse **infaisable** (plage 4 h, part fixe 6,50 h → travail = −2,50 h, `plage.rendement` lève). | Ajouter les sept paramètres de plage à `variante_aux_bornes`, et publier dans B7c la fourchette du facteur et de la date. Déclarer que la borne pessimiste rend la plage impossible — c'est un résultat, pas un plantage. |
| **M‑2 · La « mesure par rejeu » est circulaire, et le module ne le dit pas (D‑043)** | majeur | `ferroviaire.py:_rejoue` appelle `pln.quantites_chantier`, `pln.durees_chantier`, `pln.planning_avec_fenetres`, `pln.voie_A_parcours` — le code **de D2**, sur les données **de D2**. Le test `test_ferroviaire.py:109` « la référence reproduit la durée de chantier que D2 publie » est donc une tautologie : il ne peut pas échouer. Aucune seconde voie n'existe pour la grandeur centrale du module (le nombre de plages). D‑043 impose au module de signaler une comparaison circulaire ; `grep "circulaire\|seconde voie\|contre-calcul"` dans le contenu → **0**. | Écrire la seconde voie à la main (49 plages = 109,2 t / 2,2444 t, 17 fenêtres = ⌈49/3⌉, étalement = 16 × 20 + 3) et la comparer. Remplacer le test tautologique par ce contre‑calcul, et dire dans le module que le rejeu n'est pas une vérification indépendante. |
| **M‑3 · La cadence de levage « dérivée » reconstitue exactement la donnée déclarée** | majeur | `ferroviaire.py:357-360` : `cad_jour = tonnage_SI / CHLV_j × facteur / h_j`. Or `CHLV_j = j_total × part × facteur` et `tonnage_SI = t_total × part`, donc `cad_jour = t_total / j_total / h_j = cadences_chantier_V3.charpente_t_j_atelier / 8 = 1,125 t/h` **par construction**. Le commentaire de `data/projet-gare.json` (`sous_interception._cadence`) affirme : « La cadence de levage n'est PAS déclarée ici : elle se DÉRIVE ». Elle ne se dérive pas, elle revient à son point de départ (9,0009 t/j au lieu de 9, l'écart étant l'arrondi de CHLV à 2 décimales). | Lire la cadence directement dans `cadences_chantier_V3` et le dire. Supprimer le commentaire, qui transforme une identité en justification. |
| **M‑4 · L'amenée des moyens (0,40 h) n'est ni balisée ni registrée, alors qu'elle entre dans tous les résultats** | majeur | `grep "amen" data/registre-hypotheses.csv` → aucune ligne. Les six autres postes sont H166 à H171. La valeur 0,40 h entre dans la part fixe (3,15 h), donc dans le facteur ×4,01, donc dans les 600 j. Cause probable : le décalage d'un rang de B‑1 a fait sauter la dernière balise. | Baliser l'amenée et vérifier au build que chaque clé numérique de `ferroviaire.plage_travaux` a exactement une balise dans le module. |
| **M‑5 · Le coût de l'heure utile n'est lu par personne, et il est calculé sur un taux que D1 n'applique pas à ce poste** | majeur | `grep -r "cout_de_l_heure_UTILE"` → seulement `ferroviaire.py` et son test. `ferroviaire.py:270` lit `prix_unitaires_MAD.postes.main_oeuvre_h` (45 MAD/h) — que `data` déclare être la **seconde voie de chiffrage**, « jamais additionnée à la première ». D1 applique à CHAP/CHLV le taux d'atelier charpente **47,5 MAD/h** (`prix.json` → CHLV → `taux.taux_MAD_h`). Au taux réel, l'heure utile vaut **150,00 MAD/h** et non 142,11. C'est la famille de défaut n° 2 de `STATE.md` : un paramètre publié que rien ne lit. | Lire `taux_horaire_atelier(d,"charpente")`, et brancher le résultat : le sous‑détail de CHLV doit consommer ce coût. |
| **M‑6 · Les leviers sont chiffrés en jours et jamais en dirhams, alors que le cours publie le prix du jour** | majeur | S4c donne −137 j, −195 j, −237 j, −275 j ; aucun montant. `prix.json` → `cout_du_retard.1` : 16 240 MAD/j ouvré de frais de durée (et 127 584 MAD/j pénalités comprises). −237 j = **3,85 MMAD** de frais de durée. § 7.2 exige le lien coût‑délai ; § 6.2 O5 le chiffrage rattaché au cas. | Ajouter une colonne « effet sur les frais de durée » au tableau des leviers, calculée, et la contrepartie estimée (grue plus forte, emprise) en fourchette V3. |
| **M‑7 · Aucune double lecture entreprise / maîtrise d'œuvre, aucun point d'arrêt dans la fiche mémo** | majeur | `grep "MOE\|maîtrise d'œuvre\|visa\|point d'arrêt"` dans le contenu → une seule occurrence, et c'est « visibilité » dans le tableau S4g. § 6.2 O4 et § 6.1 S8 (« pour les modules d'exécution, la fiche mémo porte aussi les points d'arrêt à viser côté maîtrise d'œuvre ») ; § 12.3 en fait une case de livraison. Or la plage de consignation est **le** point d'arrêt type : demande de plage visée, dispositif de sécurité agréé, procès‑verbal de restitution. | Ajouter une colonne « ce que vise la MOE » au tableau S4g et trois points d'arrêt à la fiche mémo (visa du mode opératoire de levage, agrément du dispositif de sécurité, PV de libération du gabarit). |
| **M‑8 · Le périmètre annoncé par la fiche-module n'est pas tenu** | majeur | `cadrage/07-programme-31-10.md:27` : « B7c — Bâtiments ferroviaires : **quais, voie, systèmes**, travaux sous exploitation ». Le module traite les plages et les interfaces ; quais, voie et systèmes n'apparaissent que dans la liste « ⏸ » de la fiche mémo. Aucune justification « sans objet » (§ 6.2 l'exige en une ligne). | Soit traiter le qualitatif des quais et des systèmes (ce que le § 5.0 autorise : séquences, interfaces, contrôles), soit modifier la fiche et le justifier dans `STATE.md`. |
| **M‑9 · Une vingtaine de nombres techniques sont tapés à la main (§ 4.3)** | majeur | `content/07-b7c-*.md` : `12,13 j` et `5` et `80 j` et `68 j` et `363 j` (l. 149‑153, colonne « Avant ») ; `363` (l. 35, 185) ; `8,15 h` (l. 284) ; `21 %`, `1,7 h`, `1,7 fois`, `cinq fois` (l. 303‑310) ; `×2,1` (l. 395) ; `onze mois` (l. 39, 318) ; `12 jours` (l. 319). Tous sont justes sauf trois (B‑7) — et aucun ne se corrigera seul au prochain build. `_resume_des_paliers` de D2 existe précisément parce que ce défaut a déjà produit un texte faux. | Sortir l'état « avant correction » de `calc/` (une fonction `avant_correction()` qui neutralise le facteur et publie les cinq valeurs), et faire des exercices des variables. |
| **M‑10 · Deux textes d'autres modules sont devenus faux et portent encore les anciens nombres** | majeur | `content/04-d4-suivi-controle.md:286` : balise V3 « date d'arrêt du suivi \| 84 jours ouvrés \| **0 à 363** » — le chantier en fait 600. `content/02-d2-planification.md:699` (quiz 7) : « Une tâche de **12** jours de travail apparaît sur **80** jours au planning […] **le coût suit les 12 jours**, le délai suit les 80 » : les deux nombres sont périmés (48,65 et 320,6), et la phrase sur le coût est l'énoncé exact du bug B‑3. `STATE.md` dette 21 reconnaît que les textes n'ont pas été relus ; ces deux‑là sont faux, pas seulement non relus. | Reprendre les deux passages, la balise H‑date d'arrêt et le quiz 7, et ajouter au build un contrôle « aucun nombre de la famille durée‑de‑chantier n'est écrit en dur dans un contenu ». |
| **M‑11 · « Le réseau absorbe une partie du gain » : 1 à 3 %, et le test canari certifie cette thèse avec un seuil de 1 jour** | majeur | Figure 3, 3ᵉ puce, et S4c (« seul le réseau dit ce qui l'emporte »). Recalcul : levier 15 % → étalement −197,8 j, date −195,1 j, écart **2,7 j (1,4 %)** ; dernier levier → −278,4 contre −274,8, écart 3,6 j (1,3 %). La règle de trois que le module dénonce donnerait donc le bon résultat à 1,4 % près. `test_ferroviaire.py:131` exige `|Δdate − Δétalement| > 1.0` : le canari valide un écart de 1,4 % comme preuve que la déduction échoue. | Garder la méthode (mesurer est juste) mais dire ce qu'elle a mesuré : « ici le réseau n'absorbe que 1 à 3 % du gain, parce que CHAP dispose de 17,5 j de marge totale ; ce n'est pas toujours le cas ». Le canari doit porter sur un cas où la marge est nulle. |
| **M‑12 · Le délai d'obtention d'une plage est déclaré deux fois, lu nulle part, et jamais confronté à la date de la première fenêtre** | majeur | `data` → `ferroviaire.interfaces.delai_de_demande_de_plage_j = 120` **et** `interfaces_actives[0].delai_de_demande_j = 120` (GI → ENT‑CM) : une grandeur, deux endroits (D‑039). `grep -r "delai_de_demande_de_plage_j" calc/` → **aucune lecture**. Et la première fenêtre tombe au jour ouvré 40 (`premiere_fenetre_jour`) : avec 120 j de délai, elle doit être demandée **80 jours ouvrés avant l'ouverture du chantier**. Le module tient tout le discours « on la demande six mois à l'avance » sans jamais faire cette soustraction, qui est pourtant son meilleur argument. | Supprimer le doublon, dériver le délai de la matrice d'interfaces, et publier `jour_de_depot_de_la_demande = premiere_fenetre_jour − delai` avec son signe. |
| **M‑13 · L'exercice 3 associe l'ancienne durée de travail au nouvel étalement** | majeur | S6, exercice 3 : « Le levage de charpente, **chiffré 12 jours de travail**, s'étale en réalité sur {{321}} jours ». Dans le modèle corrigé, 12 j de travail s'étalent sur ~80 j (c'est le calcul d'avant) et 321 j d'étalement correspondent à 48,65 j de travail. Le module, qui passe trois sections à séparer travail et étalement, les remélange dans son cas ouvert. | « Chiffré 12 jours de travail de jour, il en demande 49 de nuit et s'étale sur 321 ». |
| **M‑14 · L'histogramme d'effectifs et la pointe mélangent une équipe de nuit et les équipes de jour** | majeur | `planification.py:475-491` pose `eff[CHLV] = 10` sur les 49 jours de segments de travail, dans le même histogramme que SECO (45), QUAI (14), etc. `ressources.pointe_apres = 45`, `moyenne_apres = 23,9`. Ces 10 compagnons ne sont pas là le jour : ils sont là la nuit, et ils ne partagent ni la base‑vie, ni la grue, ni l'encadrement aux mêmes heures. Rien ne le signale (§ R6). | Publier l'histogramme par **poste** (jour / nuit) ou, à défaut, déclarer la simplification dans le module et dans `STATE.md`. |

### Mineurs

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **m‑1 · Deux rendements pour la même plage sur la même page** | mineur | `ferroviaire.json` → `rendement_pct: 47.5` ; toutes les `lecture` générées écrivent « soit **48** % » (`f"{47.5:.0f}"` → arrondi au pair). Le tableau S3a, la figure 1 et l'encart d'alerte affichent donc 48 % à côté de 47,5 %. | Formater en `::n1` partout, ou arrondir une fois dans `calc/`. |
| **m‑2 · « H−05:39 » est présenté comme une heure d'horloge** | mineur | `ferroviaire.py:105-108` (`hhmm`) ; sortie `point_de_non_retour: "H-05:39"`. Une heure limite de lancement située 5 h 39 **avant le début de la plage** n'est pas une heure : c'est un déficit. | Afficher « néant — l'opération dépasse la plage de 7,31 h » quand `marge_de_decision_h < 0`. |
| **m‑3 · Le cas n° 6 de l'étalonnage se vérifie avec sa propre formule** | mineur | `calc/etalonnage/plage_cas_ferme.py:78-83` : `attendu = duree − somme(POSTES_AVANT + POSTES_APRES)`, comparé à `pg.rendement(d)` qui fait la même soustraction sur les mêmes clés. Les cas 1 à 5 sont, eux, de vrais cas fermés. | Retirer le cas 6 ou le remplacer par un cas chiffré à la main (plage 7 h, part fixe 2 h → 5 h, ×2,29). |
| **m‑4 · `heures_par_jour` a une valeur par défaut silencieuse** | mineur | `plage.py:62` : `heures_par_jour: float = 8.0`. `ferroviaire.py` appelle `pg.facteur_d_interception(d)` **sans** l'argument (l. 60, 67, 359) tandis que D2 le passe depuis `calendrier`. Les deux coïncident aujourd'hui ; changer le calendrier désynchroniserait D2 et B7c sans aucun signal. | Rendre l'argument obligatoire, ou le lire dans `d`. |
| **m‑5 · Le coût de l'heure utile ne vaut que pour un compagnon, pas pour l'opération** | mineur | `cout_de_l_heure_utile` : « par compagnon ». Ne sont comptés ni le chef d'équipe, ni le grutier, ni l'agent de sécurité ferroviaire (qui est pourtant présent toute la plage et payé par quelqu'un), ni la grue mobile. Le ratio ×4,5 est donc une borne basse non déclarée. | Le dire dans `ratio_defini_sur_cette_base` (D‑037 est respecté sur la base, pas sur le périmètre). |
| **m‑6 · Décimales anglaises dans les textes générés** | mineur | HTML rendu : « il reste **2.85** h de travail », « une journée de travail normale demande **4.01** plages ». Le reste du module écrit 2,85 et 4,01. | Formater les nombres des chaînes de `calc/` comme le fait le gabarit (`::n2`). |
| **m‑7 · La disposition « mise en girouette » demande une étude là où il faut une implantation** | mineur | S4g : « La mise en girouette d'une grue par grand vent **doit être étudiée** pour ne pas survoler la voie ». Une grue en girouette tourne librement : ce qui se décide, c'est l'implantation et la longueur de flèche, pas une étude. Formulé ainsi, le conseil laisse croire qu'une note suffit. | « La grue est implantée de façon qu'en girouette sa flèche ne puisse atteindre la voie ; si l'implantation ne le permet pas, c'est la flèche qu'on raccourcit. » |
| **m‑8 · Le module ne renvoie ni à ses décisions ni à la dette qu'il crée** | mineur | `grep "D-04"` dans le contenu → 0. B7c crée la dette 21 de `STATE.md` (600 j non répercutés dans les textes de D1 et D4) et s'appuie sur D‑045 et D‑046 : le lecteur n'a aucun moyen de le savoir depuis le module. | Une ligne en S1, comme les autres modules le font. |

---

## 3. Grille d'auto-évaluation § 7.2

| Critère | Note | Justification |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | S2 est le meilleur passage du cours : la part fixe, qui la tient, pourquoi l'effectif n'y peut rien. |
| Les hypothèses sont explicites | **2** | Dix balises V3, fourchettes en registre — mais aucune fourchette sur les **résultats** (M‑1), une hypothèse manquante (M‑4), et huit balises illisibles au rendu (B‑2). |
| Les formules sont justifiées | **2** | Le facteur est démontré et vérifié dimensionnellement ; mais la formule du nombre de plages suppose la divisibilité sans jamais l'écrire (B‑5), et la cadence « dérivée » est une identité (M‑3). |
| L'exemple est vérifié | **1** | **Sous le minimum.** Aucune seconde voie pour la grandeur centrale ; le « rejeu » est le code de D2 sur les données de D2 (M‑2) ; le test de référence est une tautologie ; et l'exercice 2, présenté comme « un calcul qui se vérifie », est faux (B‑7). |
| Le piège est identifié | **3** | S5 est juste et dense ; le piège central (chiffrer une plage comme une journée) est celui que le cours s'est fait à lui‑même, et il le dit. |
| Le lien avec l'exécution est fait | **2** | Séquence de plage, point de non‑retour, qui décide du lancement : excellent. Mais aucune lecture MOE, aucun point d'arrêt (M‑7), et un levier recommandé qui aggrave le risque (B‑6). |
| Le lien avec le coût et le délai est fait | **1** | **Sous le minimum.** Le délai est traité ; le coût ne l'est pas : l'heure utile n'est lue par rien (M‑5), D1 chiffre le même poste quatre fois moins cher (B‑3), les leviers n'ont pas de prix (M‑6), et le seul énoncé de coût du module est faux (B‑8). |

**Deux critères sous 2 : la condition de livraison du § 7.2 n'est pas remplie.**

---

## 4. Verdict

**Non livrable en l'état. 11 bloquants.**

Le module est le mieux écrit de la série et il a trouvé une vraie erreur — une tâche sous
consignation chiffrée comme un travail de jour. Mais la correction a été posée **au mauvais endroit
et dans la mauvaise unité**, et le module conclut sur des nombres qu'il n'a pas vérifiés.

Trois constats dominent les huit autres :

1. **L'unité.** Les « 48,65 jours » de CHLV sont 49 **nuits de 6 h**. Tout l'aval les lit comme des
   jours de 8 h : les jours‑hommes du chantier gonflent de 366 (B‑4) pendant que le bordereau de D1
   continue de payer 971 heures pour le même tonnage (B‑3). Le cours publie aujourd'hui deux
   nombres d'heures pour un seul levage, dans un rapport de 4,01 — et il était cohérent avant.
2. **Le modèle.** Le compte de 49 plages suppose qu'on lève 2,24 t par nuit ; la section d'à côté
   démontre qu'une pièce pèse 8 t et ne se fractionne pas (B‑5). Aucun des sept leviers publiés ne
   rend l'opération faisable, et le meilleur d'entre eux alourdit les pièces (B‑6). Le résultat
   honnête n'est pas « 600 jours », c'est « la méthode déclarée ne se réalise pas ».
3. **Le rendu.** Le tableau central affiche 11,60 h pour une plage de 6 h, attribue la durée de la
   plage à la prise de possession, et montre à l'écran la syntaxe brute des balises (B‑1, B‑2). La
   figure juste en dessous affiche les bonnes valeurs. Les 16 contrôles sont verts : aucun ne
   regarde un tableau.

Ordre de correction proposé : B‑1 et B‑2 (le lecteur voit un tableau faux) → B‑4 puis B‑3 (l'unité,
puis la propagation au prix) → B‑5 et B‑6 (le modèle et le levier dangereux) → B‑7, B‑8, B‑9, B‑11
(quatre affirmations fausses) → B‑10 (PSOU).

Deux remarques de méthode pour `STATE.md` :

- **La famille de défaut n° 7 (erreur de modèle physique) a frappé une deuxième fois**, et ailleurs
  qu'en géométrie : ici c'est l'hypothèse de divisibilité d'un levage. Elle se cherche partout où un
  module **divise une quantité par une cadence** sans se demander si l'objet se coupe.
- **Une huitième famille apparaît : le changement d'unité silencieux.** Une grandeur garde son nom
  (« jours ») et change de contenu (des nuits de 6 h). Aucun contrôle dimensionnel ne la voit —
  `pint` lit des heures des deux côtés. Le seul contrôle qui l'aurait vue est celui que personne
  n'avait écrit : *deux modules qui chiffrent la même tâche doivent trouver les mêmes heures*. Ce
  contrôle existe désormais implicitement dans le tableau du § 1‑(5) ; il devrait devenir un test.

---

## Suite donnée (27/10/2026, par l'auteur)

**Les 11 bloquants sont corrigés.** Trois ont été re-vérifiés indépendamment avant correction
(le changement d'unité, l'écart D1/D2, les balises décalées) : le relecteur avait raison sur les
trois, et sa contre-expertise reproduit exactement les quatre valeurs recalculées.

| # | Correction | Contrôle ajouté |
|---|---|---|
| B-1, B-2 | Les balises V3 de S3a étaient **décalées d'un rang** et écrites en dur. Le tableau est refait : chaque ligne porte son libellé depuis `calc/`, la balise la déclare. Et la cause racine est corrigée dans `build/md.mjs` : **une balise `⟦V3|…|…⟧` contient des `\|` et le parseur de tableau les découpait en sept cellules.** Le registre, lui, était juste — il se génère depuis la source — si bien que sept passes et seize contrôles n'ont rien vu. Le bug touchait aussi D2 et B3e. | Les balises sont masquées avant le découpage des cellules ; le libellé du tooltip, **décalé d'un champ dans tous les modules**, est corrigé au passage |
| B-3, B-4 | **Changement d'unité silencieux.** Après multiplication par le facteur, `CHLV.duree_j` n'est plus un nombre de journées mais un nombre de **plages** — et tout l'aval la lisait comme 8 h. Les jours-hommes du levage avaient quadruplé (121 → 486 j·h, +5,3 % sur le chantier) alors que le travail n'avait pas bougé, pendant que D1 les chiffrait à la cadence : 2 919 h contre 971. Corrigé par `heures_sur_site_par_jour` (une plage vaut 6 h, pas 8) et par `_heures_sous_interception` chez D1, qui paie désormais la plage entière majorée de la nuit. | **Le contrôle croisé qui manquait** : pour chaque tâche, D1 et D2 doivent trouver les mêmes heures. Douze tâches à ×1,00 ; un canari vérifie que les heures *payées* et les heures de *travail* diffèrent bien |
| B-5 | Le nombre de plages suppose le levage divisible : c'est une **borne inférieure**, publiée comme telle, et le module dit que si une seule pièce ne tient pas dans une plage, aucun nombre de plages ne suffit. | — |
| B-6 | **Le levier recommandé aggrave le problème qu'il prétend résoudre** : pré-assembler alourdit les pièces. Chaque levier publie désormais sa **masse maximale levable**, qui ne dépend que de la plage — 2,24 t à 6 h, 5,40 t à 10 h. Résultat : **aucun des sept leviers ne permet de lever la pièce de 8 t prévue**, et seul l'allongement de la plage déplace la faisabilité. C'est devenu la conclusion de la section. | la colonne elle-même |
| B-7 | L'exercice 2 comparait 8 h de fermeture à 6 h en les disant égales. Refait sur un tableau calculé : à durée de fermeture égale, deux plages de 4 h donnent 1,70 h utile contre 4,85 pour une seule de 8 h — **×2,85**, et le rendement par heure de fermeture varie d'un facteur **3,23** entre 4 h et 10 h. | `comparaison_de_plages` publie les quatre lignes ; plus un seul chiffre écrit à la main |
| B-8 | « Ne sont facturables à personne » : faux, ces jours portent les frais de durée que D1 chiffre. Qui les supporte est une question de **marché**, et elle se lit dans le CPS. | — |
| B-9 | Légende de la figure 2 : ce ne sont pas « les deux premiers » leviers qui se valent, mais le 2ᵉ et le 4ᵉ, et la légende dit maintenant qu'ils se valent **ici**, pas en général. | — |
| B-10 | **PSOU recevait la thèse du module, mais pas son facteur.** Il est désormais appliqué à **toutes** les tâches de `taches_soumises`, une seule fois, au même endroit. PSOU : 9,00 j de jour → 36,09 plages. | — |
| B-11 | Les « 363 j » du dernier levier **sont** une coïncidence, et le module le dit : deux plannings différents qui durent le même temps (le pré-assemblage allonge la tâche au sol de sept jours, le chemin critique n'a pas la même forme). Ce n'est pas une validation. | — |

**Ce que la correction a révélé en plus.** Le contrôle croisé D1/D2, écrit pour B-3, a immédiatement
exposé un **second écart, antérieur et sans rapport** : le plancher de mezzanine, hérité du module
TV, est chiffré 3 219 h par D1 et 6 880 par D2 — ×2,1. D1 compte les heures *productives* de chaque
équipe à sa cadence, D2 tout l'effectif de zone présent pendant tout le cycle, cure et point d'arrêt
compris. L'écart est déclaré comme **exception nommée** dans le test, avec sa raison, pour qu'il ne
puisse plus dériver en silence, et porté en dette.

**Ce que cette passe a prouvé.** La huitième famille de défaut que le relecteur nomme est juste, et
c'est la plus insidieuse rencontrée jusqu'ici : **le changement d'unité silencieux.** La grandeur
garde son nom (« jours »), change de contenu (des plages de 6 h), et `pint` lit des heures des deux
côtés sans rien voir. Aucun contrôle dimensionnel ne l'attrape. Le seul qui l'attrape est celui que
personne n'avait écrit — *deux modules qui chiffrent la même tâche doivent trouver les mêmes
heures* — et il est maintenant en place, avec sa liste d'exceptions nommées.

