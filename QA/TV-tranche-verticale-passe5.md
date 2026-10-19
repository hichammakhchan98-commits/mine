# Passe adversariale /devil n° 5 — module TV (tranche verticale de suivi)

**Relecteur hostile, indépendant de l'auteur. 19/10/2026. Passe BORNÉE** : vérification des
corrections annoncées pour les 3 bloquants et les 10 majeurs de la passe 4, et recherche de ce
qu'elles ont pu casser. Ce n'est pas une revue complète ; les défauts de la passe 4 laissés en dette
ne sont repris ici que lorsqu'une correction les touche ou qu'une affirmation du dépôt les nie.

**Méthode.** Contre-expertise à l'aveugle d'abord : huit grandeurs recalculées depuis
`data/projet-gare.json` **seul**, par mon propre script, avant d'ouvrir `calc/`. Puis six canaris
rejoués, neuf canaris neufs, mesure des cinq figures dans le SVG rendu, `npm run check` et
`python3 calc/run_all.py`. `QA/TV-tranche-verticale-passe4.md` et les décisions D-026 à D-030 n'ont
été lus qu'après le recalcul.

Scripts de preuve : `/tmp/claude-0/-home-user-mine/70713aa8-3622-5c6d-a7c2-bce4a8b25d73/scratchpad/blind5/`
(`aveugle.py`, `preuve_grue.py`, `run_canaris.py`, `rejeu.py`, `neufs.py`, `neufs2.py`, `neufs3.py`,
`secu.py`). **Rien du dépôt n'a été modifié** ; tous les essais ont tourné sur des copies `cp -a`.
`git status` est vide à la fin de la passe.

---

## 0. Ce que l'outillage dit de lui-même

```
npm run check            VERT — 16 contrôles passés
python3 calc/run_all.py  calc/ : VERT
```

Les trois bloquants ci-dessous franchissent ces deux commandes sans bruit. C'est la cinquième fois.

---

## 1. Contre-expertise à l'aveugle — huit grandeurs recalculées depuis `data/` seul

| # | Grandeur | Mon recalcul indépendant | Publié | |
|---|---|---:|---:|---|
| 1 | Béton d'une zone : 360 × 0,25 + 2 × 24,0 × 0,35 × 0,50 | **98,400 m³** | 98,4 | ✓ |
| 2 | Coffrage : (360 − 16,8) + 48,0 + 16,8, + 4 % de rives | **424,320 m²** | 424,3 | ✓ |
| 3 | Acier : 90 × 80 + 8,4 × 180 | **8 712 kg** (88,54 kg/m³) | 8 712 / 88,5 | ✓ |
| 4 | **Cycle**, en lisant le taux de recouvrement comme `data/` l'énonce (« part faite **avant** que le successeur démarre ») | **8,052 j** | 8,053 | ✓ **B2 de la passe 4 corrigé** |
| 5 | **Cadence** = max(équipe la plus chargée 3,000 ; grue 2,268/1) × 1,14 | **3,420 j** | 3,42 | ✓ |
| 6 | **État physique** de la zone en cours à 60 % du cycle (t = 4,831 j) : COF 100 %, FEP 100 %, **FED 97,97 %**, BET 0 % | 424,32 m² · 8 566 kg · **0,0 m³** | 424,3 / 8 565 / 0,0 | ✓ |
| 7 | **VA** = 3 zones + état physique, valorisé | **1 264 446 MAD** · CPI **0,9507** | 1 264 413 · 0,951 | ✓ **B1 de la passe 4 corrigé** |
| 8 | **VP** = état physique planifié des 8 zones à j = 19 (cadence 3,4) | **1 783 946 MAD** · SPI **0,7089** | 1 783 631 · 0,709 | ✓ |
| 9 | **Écart voie A / voie B** = (1 264 446 − 1 247 917) / 1 264 446 | **+1,31 %** pour une tolérance déclarée de **1 %** | publié « **1,30 %, sous la tolérance de 1 %** » | ✗ → **B1** |
| 10 | Variante recommandée par l'exercice 3 (2 équipes + 2 grues) : ⌈6,93 / 2,28⌉ = 4 zones coffrées à la fois | **1 697 m² pour un parc de 1 300** — déficit **397 m²** | corrigé publié sans un mot | ✗ → **B3** |

**L'arithmétique est juste partout, et les quatre grandeurs que la passe 4 avait fait refaire sont
désormais exactes.** Ce que je rapporte, ce sont trois endroits où le dépôt **dit le contraire de ce
que son propre calcul rend**.

---

## 2. Les six corrections, une par une

### 2.1 Valeur acquise physique (B1 de la passe 4) — **le modèle est corrigé, le texte ne l'est pas, et le contrôle ne peut plus sonner**

**Ce qui tient.** `VA_A = valoriser(attendu)` où `attendu` est l'état physique dérivé du réseau ;
`VP = valoriser(planifie)` idem ; la courbe en S est tracée par `valeur_physique()`, donc en valeur.
Mon recalcul indépendant retrouve VA, VP, CPI et SPI (ligne 7-8 ci-dessus). **L'écart vertical de la
figure 5 EST bien SV** : mesuré dans le SVG, le point de constat est à y = 137,38 soit **45,50 %**
(= VA/BAC = 45,49 %), la courbe à y = 106,71 soit **64,20 %** (= VP/BAC = 64,16 %), l'écart est
**coté « 18,7 pts »** sur la figure, et 18,7 % × BAC = 519 832 MAD contre SV = −519 218 (0,12 % de
résidu d'arrondi). Avant, l'identité ne tenait que parce que les deux termes partageaient l'erreur.
C'est une vraie correction. CPI et SPI gardent leur sens : numérateur et dénominateur sont
maintenant la même grandeur, des dirhams de travail fait.

**Les deux voies sont toujours réellement différentes** — c'était la question. Voie A part de l'état
physique **calculé par le réseau** à partir de l'avancement déclaré ; voie B part des **quantités
relevées** de `data/suivi.quantites_relevees` et ne touche ni au réseau ni au déclaré. Le test le
vérifie dans les deux sens. Elles ne partent donc pas du même état physique.

**Mais c'est justement ce qui casse.** Les relevés sont posés à −0,61 %, −0,80 % et −2,00 % de l'état
physique. En dirhams, cela fait **1,305 %** d'écart pour une **tolérance déclarée de 1,0 %**, et
`valeur-acquise.json` publie :

```
verdict = "ECART — l'avancement declare ne colle pas aux quantites relevees"
```

Or le module rendu publie, mot pour mot :

> « Voie A, par les coûts : **budget à l'achèvement × avancement déclaré** → 1 264 413 MAD. Voie B,
> par les quantités relevées sur le chantier → 1 247 917 MAD. Écart : 1,30 %, **sous la tolérance de
> 1 %**. »

Trois choses fausses dans deux phrases :

1. **1,30 % n'est pas sous 1 %.** Le module affirme au lecteur qu'un contrôle est passé alors que son
   propre fichier dit qu'il a échoué.
2. **« budget à l'achèvement × avancement déclaré »** est la formule que la correction vient de
   supprimer. La prose décrit un calcul qui n'existe plus, et que l'encart situé douze lignes plus
   haut interdit. Le § 3.3 impose un contre-calcul ; ici il décrit la mauvaise voie.
3. **Le contrôle ne peut plus échouer.** Dans `calc/tests/test_plancher.py`, il n'y a plus
   d'assertion : il reste un `print("  info  ...")` dont le texte invoque une cause fausse —
   « *l'alarme d'avant venait d'un état attendu calculé au prorata uniforme, c'est-à-dire d'un
   modèle faux — pas du chantier* ». **Avant la correction il n'y avait pas d'alarme** : la passe 4
   mesure 0,888 %, sous le seuil. La correction a *créé* le dépassement, puis l'a expliqué par une
   alarme qui n'a jamais existé.

**Canari C9 — preuve que ce n'est pas un cas particulier.** `avancement_zone_en_cours_pct = 70`,
valeur parfaitement légale :

```
calc/ : VERT   (0 échec)
zones realisees PUBLIEES (temps) 3.7 | en VALEUR 4.0 | retard_en_zones publie -1.43
ecart contre-calcul 10.216 %   pour une tolerance de 1 %
```

Le module publierait « Écart : **10,22 %**, sous la tolérance de 1 % » et « **3,70** zones
réalisées » pour un chantier qui en a acquis **4,00**. Rien ne sonne.

**Résidu de B1 non traité.** `zones_prevues_equivalentes` = 5,13 est **en valeur** (VP/BAC × 8) ;
`zones_realisees_equivalentes` = 3,60 est **en temps** (3 + 0,60). Le § S6 ouvre sur « 5,13 zones
étaient prévues, 3,60 sont réalisées » — deux unités dans la même phrase — et `retard_en_zones` les
soustrait. En valeur, le réalisé vaut 3,64. L'écart est de 0,04 zone ici, de 0,30 au canari C9. La
recommandation de la passe 4 (« publier l'avancement **en valeur** à côté de l'avancement **en
temps**, et dire que les deux diffèrent ») n'a pas été suivie : aucune occurrence de « en valeur »
dans le texte hors légende de figure.

### 2.2 Taux de recouvrement (B2 de la passe 4) — **corrigé, vérifié, et vérifiable**

`-(1 - r) × durée` est bien en place. **Mesuré dans le SVG de la figure 3** (échelle 42,235 px/j) :
COF 0 → 1,770 ; FEP débute à **0,890** (50,0 % de COF) ; FED débute à **1,890**, soit
(1,892 − 0,884)/2,520 = **40,0 % de FEP**, exactement ce que `data/`, la balise et **H024** annoncent.
Le cycle lu sur la figure vaut **8,05 j**. Mon recalcul littéral depuis `data/` donne 8,052 : la
lecture du lecteur et celle du code coïncident enfin.

Le test de relecture existe et il est bon : il recalcule
`(début_successeur − début_prédécesseur)/durée_prédécesseur` **dans les dates du réseau** et le
compare au paramètre, pour **les deux** liens. **Canari C1** (réinversion du seul second taux dans le
code) : *SONNE* — « recouvrement FEP→FED : déclaré 40 %, réalisé 60,0 % ». L'inversion ne subsiste
nulle part ailleurs : `reseau_zone` est le seul endroit où un taux devient un décalage, et les
deux liens y passent par la même expression.

**C'est la meilleure correction des cinq passes** : un paramètre déclaré en mots est désormais relu
dans le résultat qu'il engendre, et la règle est généralisable.

### 2.3 Conflits de grue (B3 de la passe 4) — **la détection est bonne ; la résolution n'est vérifiée par rien, et sa justification contredit le module**

**La détection est exhaustive** et je l'ai refaite : `conflits_de_ressource` construit un intervalle
par (zone × tâche de grue), trie toutes les bornes et compte les actifs sur chaque front. Elle balaie
donc tous les fronts, pas seulement les débuts. Elle trouve 6 conflits de 0,50 j, identiques à mon
balayage indépendant. **Canari C2** (`decoffrage_j` retiré de `taches_servies_par_la_grue`) : *SONNE*.

**La résolution donne le bon résultat.** J'ai rejoué le planning **avec les décalages publiés**
(`preuve_grue.py`) : **0 conflit restant**, et le parc tient toujours (3 zones détenant du coffrage,
1 273 m² pour 1 300). Le nombre publié est juste.

**Mais la vérification est vide, et je le prouve.** Le module calcule

```python
_restants = conflits_de_ressource(reseau, plan["debuts"], [x for x in _tg if x != "DEC"], _nb_grues)
```

c'est-à-dire qu'il **retire le décoffrage de la liste des ressources** au lieu de rejouer la
détection avec le décoffrage **décalé**. Il ne reste alors que COF, une occurrence par zone, à une
cadence de 3,4 j pour une durée de 1,77 j : **le résultat est 0 par construction, quelle que soit la
résolution**.

**Canari C5** — la résolution est bridée pour ne rien décaler du tout :

```
calc/ : VERT   (0 échec)
conflits brut 6   apres 0   decalage max 0.0 j
```

Le module publierait : « *il se décale dans sa marge de **0,00 j** au plus, et les **6** conflits
tombent à **0*** ». Un contrôle qui ne peut pas échouer n'est pas un contrôle, et le test
`verifie("decaler le decoffrage dans sa marge les resout tous", ... == 0)` est de ceux-là.

**La justification publiée est fausse contre le module lui-même.** Le texte écrit : « *le décoffrage
n'est **sur le chemin critique d'aucune rotation**, il se décale **dans sa marge*** ». Le tableau des
tâches du même module publie :

| id | durée | début | **marge** | **critique** |
|---|---:|---:|---:|:--:|
| DEC | 0,50 | 7,55 | **0,00** | **oui** |

Les sept tâches sont critiques, DEC comprise ; le chemin critique publié est
`COF → FEP → FED → PTA → BET → CUR → DEC`. La marge que la résolution consomme n'est pas une marge
CPM : c'est du mou dans l'occupation du **parc de coffrage et d'étais**, puisque la zone suivante
démarre à la cadence, pas à la fin de DEC. Le décalage allonge l'immobilisation du coffrage de 8,05
à **9,10 j** (+13 %). Cela reste dans le parc (⌈9,10/3,4⌉ = 3 zones, 1 273 m²) et le nombre d'étais
est inchangé (7 zones étayées dans les deux cas) — **je l'ai vérifié, le module non**.
`coherence_materiel` recalcule tout sur `duree_zone` **sans le décalage**.

**Le module publie-t-il honnêtement ce qu'il fait ?** Pour la détection, oui, et c'est bien écrit.
Pour la résolution, non : il annonce une marge que son propre tableau nie, un contrôle qui ne peut
pas sonner, et il ne dit pas ce que le décalage coûte en immobilisation. Enfin, **la figure 2 affiche
toujours le planning brut** — j'y mesure Z1/DEC 7,55→8,05 et Z3/COF 6,80→8,57, qui se chevauchent —
sans un repère, sans profil d'occupation de la grue, et sans dire que c'est le planning *avant*
résolution.

### 2.4 Rattachement poste → tâche (M1 de la passe 4) — **corrigé, et le canari décisif sonne**

Le rattachement est juste dans son principe, et je l'ai vérifié poste par poste sur `data/` :

- **le coffrage est intégralement posé à la fin de COF** — oui : les tables et l'étaiement de la zone
  sont montés pendant COF, le ferraillage se pose dessus. Rattacher les 424,32 m² à COF est le bon
  modèle, et c'est la thèse du module.
- **l'acier suit FEP puis FED** — oui, et séparément : 1 512 kg sur FEP, 7 200 kg sur FED. À 60 % du
  cycle, FEP est fini et FED à 97,97 % → 8 566 kg. Mon recalcul indépendant donne 8 566,08 ; publié
  8 565.
- **aucun poste n'est oublié** parmi les trois que porte le métré (béton, acier, coffrage). Deux
  tâches ne produisent aucun poste — PTA et CUR — et c'est correct : un visa et une cure ne
  produisent pas d'ouvrage. DEC non plus, mais il **libère** le coffrage ; ce n'est pas un poste de
  métré, c'est ce que la section 2.3 ci-dessus montre être le vrai enjeu du décalage.

**Canari N4 de la passe 4, rejoué** (coffrage ← BET, béton ← COF) : *SONNE*, 5 échecs, dont « à 60 %
du cycle, le béton est à ZÉRO : c'est la thèse du module ». Les cinq dates (0 · 25 · 60 · 90 · 100 %)
recalculent l'état **sans appeler la fonction**. C'est une vraie correction.

*Réserve* : le test ré-énonce le rattachement au lieu de le confronter à une source indépendante. Il
attrape la permutation, ce qui était la demande ; il n'attraperait pas une erreur commise deux fois.

### 2.5 Sécurité : section S7c et 16ᵉ contrôle (M7 de la passe 4) — **bon contenu, contrôle de mot**

**Aucune valeur normative n'a fui.** J'ai relu la section entière : le tableau ne porte **aucun
nombre** ; les seules valeurs sont deux variables calculées (nombre de conflits de grue, nombre de
zones étayées). Pas de durée de maintien, pas de hauteur, pas de vitesse de vent, pas de classe de
résistance, pas d'article. Le contrôle `5.0` du build (« aucune balise V2 dans `content/` ») reste
vert. La section le dit elle-même et c'est juste : *« aucune valeur normative n'est donnée ici — la
phase § 5.0 l'interdit, et une cote de sécurité approximative serait pire qu'aucune »*.

**Rien d'y est dangereux ni faux.** La hiérarchie est la bonne : protection collective d'abord
(garde-corps en rive, trémies couvertes **dès le coffrage**), harnais en complément seulement ; note
d'étaiement visée **avant** montage ; critère de résistance **atteint et constaté** avant décoffrage,
étais de reprise maintenus, zone en dessous interdite ; zone d'évolution balisée au levage, pas de
levage au-dessus d'un poste occupé, abandon par vent fort. La colonne « ce que la maîtrise d'œuvre
vérifie » est au bon niveau. Le lien final — *les trois accidents typiques de ce cycle sont des
accidents de **planning*** — est la meilleure page du module : elle rattache la sécurité à l'objet
du module au lieu de la poser à côté.

**Le contrôle sait échouer, mais il ne contrôle qu'un mot.** Canari C7 (section S7c retirée) :
*SONNE* — « 01-tranche-verticale-suivi.md : opération à risque sans disposition de sécurité (§ 3.4) ».
Canari C8 (la section entière remplacée par le seul mot `securite`) : **VERT** — « 2 module(s) à
risque sur 2 ». D-029 annonce que `npm run check` « échoue sur tout module qui mentionne une
opération à risque **sans disposition de sécurité** » : il échoue sur tout module sans **le mot**.
Dupliqué sur C1 à C8, ce contrôle laissera passer une ligne de politesse.

### 2.6 Les autres corrections annoncées

| Correction | Constat |
|---|---|
| Durée du cycle passée en argument au lieu d'être en dur (`8.56`) | **Tient.** `cout_zone(d, q, t, cycle_j)` et `_coherence_prix_horaire(..., cycle_j)` ; les deux appelants passent `duree_zone`. Le canari implicite est le cycle lui-même, qui est passé de 8,56 à 8,05 sans laisser de trace figée. |
| Étalonnage qui appelle la bibliothèque | **Tient.** Le cas fermé (10 unités à 100 MAD) passe `_fait` et `_prevu` à `valeur_acquise()` et vérifie CPI, SPI, CV, SV, EAC contre des valeurs écrites d'avance ; le cas faux doit lever. Le `attendu` n'est plus posé sur le modèle linéaire : la réserve de la passe 4 est levée. **Canari C4** (VA majorée de 10 %) : *SONNE*, 7 échecs dont 3 dans l'étalonnage. |
| `_nature: "decision"` sur les effectifs | **Décoratif.** `grep -rn "_nature" build/ calc/ content/ src/` ne rend **rien** : aucun contrôle ne lit cette clé. Le parcours des V3 de `check.mjs` retient toujours les seules feuilles `{valeur, fourchette}` : les quatre effectifs restent hors registre exactement comme avant (M4 de la passe 4, intact). Pire, le bloc `effectifs` porte **à la fois** `niveau_preuve: "V3"` **et** `_nature: "decision"` — deux affirmations qui s'excluent ; et `materiel`, déclaré « decision », contient `etais_de_reprise_maintenus_j`, qui est une vraie hypothèse V3 à fourchette et registrée en H027. |
| SV dans le tableau S6 | **Tient**, et désormais il a un sens : CV et SV sont publiés, et SV est cohérent avec l'écart coté sur la figure 5. |

---

## 3. Canaris

### 3.1 Rejeu — les six sonnent

| Canari | Résultat |
|---|---|
| **T2** — effectifs `ferrailleurs_dalle` / `ferrailleurs_poutres` permutés | **SONNE** (4 échecs) |
| **T6** — rendement d'équipe à 190 m²/j, borne basse déclarée | **SONNE** (2 échecs) |
| **permutation de `effectif_par_tache`** (COF ↔ FED) | **SONNE** (2 échecs, nommés) |
| **recouvrement hors fourchette** (85 % pour [20 ; 60]) | **SONNE** |
| **maintien d'étais nul** (0 j pour [7 ; 28]) | **SONNE** |
| **N4 — permutation du rattachement poste → tâche** | **SONNE** (5 échecs) — *c'était le canari muet de la passe 4* |

### 3.2 Neufs

| # | Mutation | Verdict | Ce que le module publierait |
|---|---|---|---|
| **C1** | second taux de recouvrement réinversé dans le code, sur **un seul lien** | **SONNE** | — |
| **C2** | `decoffrage_j` retiré des tâches de grue | **SONNE** | — |
| **C3** | `valeur_physique` faussée d'un facteur 1,10 | **SONNE** (figure 5 contre tableau S6) | — |
| **C4** | valeur acquise majorée de 10 % | **SONNE** (7 échecs) | — |
| **C5** | **la résolution des conflits ne décale rien** | **MUET** | « il se décale dans sa marge de **0,00 j** au plus, et les 6 conflits tombent à **0** » → **B2** |
| **C6** | `valeur_acquise()` appelée **sans** `planifie` | **MUET** | VP 1 801 789 au lieu de 1 783 631, SPI 0,702 au lieu de 0,709, par le prorata linéaire condamné → **M1** |
| **C7** | section S7c retirée | **SONNE** | — |
| **C8** | S7c réduite au seul mot « securite » | **MUET** | une ligne de politesse vaut une section de sécurité → **M7** |
| **C9** | `avancement_zone_en_cours_pct = 70` (valeur légale) | **MUET** | « Écart : **10,22 %**, sous la tolérance de 1 % » et « **3,70** zones réalisées » pour 4,00 acquises → **B1** |

**C5, C6 et C9 sont les canaris décisifs de cette passe.** Les trois visent des contrôles créés ou
conservés par les corrections de la passe 4, et les trois montrent le même mécanisme : le contrôle
existe, il est calculé, il est publié — et **son consommateur ne peut pas lui dire non**.

### 3.3 Un effet de bord des corrections, trouvé par les canaris

Le test `verifie("le planning BRUT demande bien la grue en deux endroits : le controle le voit",
len(_cf) > 0)` **échoue quand le planning devient faisable**. Je l'ai vu sonner sur deux canaris qui
n'ont rien à voir avec la grue : T2 (effectifs permutés) et le recouvrement à 85 % — dans les deux
cas, le cycle raccourcit, les conflits disparaissent, et le test annonce « 0 conflit(s) » comme un
échec. C'est une assertion sur la présence d'un défaut, pas sur une propriété du modèle. Elle
sonnera à chaque recalibrage légitime, et elle gonfle artificiellement le compte d'échecs des autres
canaris.

---

## 4. Les cinq figures, mesurées dans le SVG rendu

| Figure | Prétention | Mesure | |
|---|---|---|---|
| **3** — Gantt | durées et recouvrements du tableau S4a | COF 0→1,770 · FEP **0,890**→3,410 · FED **1,890**→4,890 · PTA 4,890 · BET 5,140 · CUR 5,550 · DEC 7,550→**8,050**. FED démarre à **40,0 %** de FEP. | ✓ **preuve de B2 corrigé** |
| **5** — courbe en S | « l'écart vertical, c'est SV, et il vaut ce que le tableau S6 annonce » | point (19,0 j ; **45,50 %**) = VA/BAC ; courbe **64,20 %** = VP/BAC ; écart **coté 18,7 pts** = **519 832 MAD** contre SV = −519 218 (0,12 %). | ✓ **corrigé, et pour la bonne raison** |
| **5** | « le constat est UN point » | un seul point. | ✓ |
| **5** | — | l'axe est gradué « % » sans dire **% de quoi** (du budget à l'achèvement). | ~ m |
| **2** — rotation | les sept phases, leurs durées, la cadence | Z1 : COF 0→1,770, FEP 0,890→3,410, FED 1,890→4,890, …, DEC 7,550→8,050. Cadence lue sur la tiretée : 3,40 j/zone. Courbe du coffrage : 3 niveaux à 1 273 m², ligne de parc à 1 300 — exacte au pixel. | ✓ |
| **2** | « les phases d'une même zone SE RECOUVRENT » | lisible, chaque phase sur sa sous-bande. | ✓ |
| **2** | — | **la figure affiche le planning BRUT** : Z1/DEC 7,55→8,05 chevauche Z3/COF 6,80→8,57. Les 6 conflits que le texte annonce sont là, non repérés, sans profil d'occupation de la grue, et la figure ne dit pas qu'elle montre l'avant-résolution. | ✗ → **B2** |
| **2** | « elle oscille entre **deux et trois** zones ouvertes » | trois niveaux mesurés : 1 (j0–j3), 2, 3. *m2 de la passe 4, en dette.* | ✗ m |
| **2** | — | toujours ni légende numérotée ni échelle. *m3 de la passe 4, en dette.* | ✗ m |
| **4** — effectifs | axe gradué, pointe cotée | axe 0→25 par 5, « personnes », **pointe 29** (= max de l'histogramme, testé), moyenne 19,6. | ✓ |
| **4** | « les jours à zéro de la **fin** » | j29 = 7, **j30 = 0, j31 = 4, j32 = 0**. *m4 de la passe 4, en dette.* | ✗ m |
| **1** — zones | lisérés d'état prévu | conforme. *m1 de la passe 4 (poutres « au milieu de chaque zone ») en dette.* | ✓ / m |

**Les deux figures que les corrections touchaient sont maintenant exactes au pixel.** La figure 3
prouve B2 ; la figure 5 prouve que SV est enfin l'écart qu'elle affiche. La figure 2 est la seule que
la correction aurait dû toucher et n'a pas touchée.

---

## 5. Tableau des défauts

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **B1 · Le contre-calcul de la valeur acquise échoue sa propre tolérance, le module publie l'inverse, et il ne peut plus sonner.** | **bloquant** | `valeur-acquise.json` : `ecart_pct = 1.305`, `tolerance_pct = 1.0`, `verdict = "ECART — l'avancement declare ne colle pas aux quantites relevees"`. Module rendu : « Écart : 1,30 %, **sous la tolérance de 1 %** ». Le test est devenu un `print("info")` dont le texte invoque une alarme qui n'a jamais existé (passe 4 : 0,888 %, sous le seuil). La même phrase décrit encore voie A comme « budget à l'achèvement × **avancement déclaré** », la formule supprimée. **Canari C9** (`avancement = 70 %`, valeur légale) : écart **10,22 %**, `calc/` VERT. | Rendre l'assertion au test. Puis **choisir** : soit la tolérance en dirhams est relevée et **justifiée** par l'écart des relevés que `data/` pose volontairement (c'est défendable, et c'est même la leçon : un seuil en dirhams n'a pas de sens quand les relevés portent déjà 2 % sur l'acier), soit les relevés sont resserrés. Dans les deux cas, publier le `verdict` rendu par `calc/` au lieu d'une phrase écrite à la main, et réécrire la description de voie A. |
| **B2 · « Les 6 conflits tombent à 0 » n'est vérifié par rien, et la marge invoquée n'existe pas dans le module.** | **bloquant** | `_restants = conflits_de_ressource(..., [x for x in _tg if x != "DEC"], ...)` **retire** DEC au lieu de rejouer avec DEC décalé : le résultat est 0 par construction (une seule COF par zone, cadence 3,4 > 1,77). **Canari C5** : résolution bridée à 0,00 j de décalage → `conflits_apres_resolution = 0`, `calc/` VERT, et le module publierait « il se décale de 0,00 j et les 6 conflits tombent à 0 ». Texte : « le décoffrage n'est **sur le chemin critique d'aucune rotation**, il se décale **dans sa marge** » ; tableau du même module : DEC `marge 0,00 j`, `critique: true`, chemin critique = les sept tâches. | Rejouer `conflits_de_ressource` **sur les intervalles décalés** et asserter zéro (je l'ai fait : c'est vrai, 0 conflit). Recalculer le parc et les étais avec l'immobilisation allongée (8,05 → 9,10 j ; j'ai vérifié : 3 zones, 1 273 m², 7 zones étayées — inchangé, mais personne ne le sait). Remplacer « dans sa marge » par ce qui est vrai : le décoffrage n'a pas de marge CPM, il a du **mou dans l'occupation du parc**, et c'est ce mou que la résolution consomme. Repérer les 6 conflits sur la figure 2, ou y publier le profil d'occupation de la grue. |
| **B3 · La réponse modèle de l'exercice 3 viole la contrainte de parc que le module enseigne, et son propre calcul le dit.** | **bloquant** | `variantes.deux_equipes_et_deux_grues` : `zones_coffrees_simultanement = 4`, `coffrage_mobilise_m2 = 1697`, `stock = 1300`, **`deficit_coffrage_m2 = 397`, `coffrage_suffisant = false`**. Le corrigé publie cette variante comme la seule qui passe (« 22,9 jours — **sous la cible** »), sans un mot. Le § d du même module écrit : « **Un planning qui demande plus de tables que le parc n'existe pas** » et « réduire la cadence sans ajouter de tables est impossible : c'est la contrainte que les plannings de rotation oublient le plus souvent ». `coherence_materiel["verdict"]` n'est calculé que sur la variante de **référence** : les trois autres ont leur `coffrage_suffisant` calculé et **jamais lu**. *(Défaut antérieur à la passe 4 — vérifié sur le commit `c3c3fd2` : déficit déjà de 397 m². Quatre passes l'ont manqué.)* | Lire `coffrage_suffisant` sur **toutes** les variantes, et le dire dans le corrigé : la seconde grue atteint 22,9 j **à condition d'ajouter 400 m² de tables** — ce qui est exactement la leçon du module et rend l'exercice meilleur, pas moins bon. Test : aucune variante publiée comme solution ne peut avoir `coffrage_suffisant == false` sans que le texte le porte. |
| **M1 · `planifie` est resté optionnel, et son repli est le prorata condamné.** | majeur | **Canari C6** : `valeur_acquise()` appelée sans `planifie` → `planifie = {k: v * prevu/avancement}`, VP 1 801 789 au lieu de 1 783 631, SPI 0,702 au lieu de 0,709, **0 échec**. D-023 a rendu `attendu` obligatoire en écrivant « le rendre optionnel aurait laissé le défaut revenir en silence » ; l'argument vaut mot pour mot pour `planifie`. Le repli est d'ailleurs **exercé** sur les données réelles dans `calc/etalonnage/plancher_cas_ferme.py:68`. | Rendre `planifie` obligatoire, comme `attendu`. |
| **M2 · « 5,13 zones prévues » (valeur) contre « 3,60 zones réalisées » (temps) dans la même phrase, et `retard_en_zones` les soustrait.** | majeur | `zones_prevues_equivalentes = prevu_arret/100 × 8` est en valeur ; `avancement_zones = 3 + 0,60` est une fraction de temps. En valeur le réalisé vaut 3,64. Canari C9 : 3,70 publié pour 4,00 acquises. `avancement_implique_par_les_releves_zones` (3,59) est comparé au déclaré en temps (3,60) et non à l'acquis en valeur (3,64) : l'écart publié vaut 0,01 au lieu de 0,05. | Publier l'avancement **en valeur** à côté de l'avancement **en temps**, et commenter l'écart — c'est la leçon de l'encart, appliquée à son propre tableau. |
| **M3 · `verif_unites.py` ne couvre ni `etat_physique_de_zone`, ni `cadence_rotation`, ni la nouvelle `valeur_physique`.** | majeur | Les quatre sections du fichier couvrent `plancher.py`, `durees_taches`/`cout_zone`, `cpm.py`, `valeur_acquise.py`. En-tête : « vérification dimensionnelle de **CHAQUE** formule publiée ». `npm run check` affiche « unités (pint) des **5 bibliothèques** ». M6 de la passe 4, non corrigé — **et la correction a ajouté une cinquième fonction non couverte**, `valeur_physique`, qui multiplie des m², des kg et des m³ par des fractions de temps et les somme en MAD. | Trois sections, chacune avec son contre-contrôle qui doit lever. |
| **M4 · Le 16ᵉ contrôle est un contrôle de mot.** | majeur | **Canari C8** : S7c remplacée par le seul mot `securite` → « ok · 2 module(s) à risque sur 2 ». D-029 annonce l'inverse. La correction de `content/00-demo-cage.md` est d'ailleurs un paragraphe ajouté pour passer le contrôle — honnête dans son contenu, mais c'est bien le geste que le contrôle encourage. | Exiger une section identifiée (titre `S7c` ou directive dédiée) et un seuil de substance (n lignes, ou une ligne par opération à risque détectée), pas un mot-clé. |
| **M5 · La fiche mémo (S8), contrôle n° 5, n'a pas appris la leçon de B3 de la passe 4.** | majeur | Elle dit toujours : « ⌈cycle/cadence⌉ zones détiennent du coffrage en même temps, et **la grue cumule les tâches qu'elle sert** : comparez au parc et à la grue ». C'est la règle de **moyenne**, exactement celle dont le module démontre deux pages plus haut qu'elle ne prouve rien. Le lecteur qui n'emporte que la fiche mémo refera le planning infaisable. | Ajouter la ligne : « une occupation moyenne sous 100 % ne prouve rien — balayez les fronts et comptez les demandes simultanées ». |
| **M6 · Un test sonne sur l'**absence** de défaut.** | majeur | `verifie("le planning BRUT demande bien la grue en deux endroits", len(_cf) > 0)` échoue dès que le planning devient faisable. Observé sur T2 et sur le canari « recouvrement 85 % », deux mutations sans rapport avec la grue. | Asserter la **propriété** (« le balayage des fronts est exhaustif et le module publie le nombre qu'il trouve »), et porter le « 6 » du cas de référence dans un test de non-régression séparé. |
| **M7 · `_nature: "decision"` n'est lu par aucun contrôle, et cohabite avec `niveau_preuve: "V3"`.** | majeur | `grep -rn "_nature" build/ calc/ content/ src/` : **aucun résultat**. Le parcours des V3 de `check.mjs` retient toujours les seules feuilles `{valeur, fourchette}`. Les quatre effectifs, `heures_par_jour`, `nb_grues`, `etais_par_m2`, `jour_arret_ouvre`, `avancement_zone_en_cours_pct`, `cout_reel_constate_MAD` et les trois relevés restent hors registre — M4 de la passe 4, intact. Le bloc `effectifs` affirme **en même temps** `niveau_preuve: "V3"` et `_nature: "decision"` ; `materiel` est marqué « decision » tout en portant H027, une hypothèse V3 à fourchette. | Faire lire `_nature` par le contrôle : une feuille numérique d'un bloc V3 doit porter **soit** une fourchette et une ligne de registre, **soit** `_nature: "decision"` et une justification — et les deux clés contradictoires doivent faire échouer le build. |
| **M8 · La conséquence du décalage de 1,05 j n'est recalculée nulle part.** | majeur | `coherence_materiel` (parc, étais, `zones_coffrees_simultanement`) tourne sur `duree_zone = 8,053`, sans le décalage. Le coffrage reste pourtant immobilisé 9,10 j sur six zones. J'ai vérifié que cela tient (3 zones, 1 273 m² ; 7 zones étayées) : **la réponse est juste, la vérification n'existe pas**. | Recalculer le parc et les étais sur la durée d'immobilisation **effective**, décalage inclus, et le publier : c'est le prix de la résolution, et le module gagne à le montrer. |
| **M9 · Deux durées de plancher publiées pour le même cas de référence : 31,9 j et 32,0 j.** | majeur | § S4d et énoncé de l'exercice 3 : « le plancher complet prend **31,9** jours ouvrés », « 25 jours au lieu de **31,9** » (planning à la cadence arrondie 3,4). Corrigé de l'exercice 2 : « le plancher passe donc de **32,0** à 27,1 jours » (`variante_effectif`, cadence non arrondie 3,42). M2 de la passe 4, non corrigé et non porté en dette. | Une seule cadence, arrondie une seule fois en amont. Test : `planning_plancher.duree_totale_j == variantes.reference.duree_plancher_j`. |
| **M10 · `STATE.md` affirme « 94 défauts, tous corrigés », et trois autres choses fausses.** | majeur | « TV — quatre passes, 94 défauts, **tous corrigés** » : M2, M4, M6, M8, M10 et les onze mineurs de la passe 4 ne sont ni corrigés **ni portés en dette** (la table de dette n'a pas bougé). En-tête : « 16/10/2026 · corrigée après la passe /devil **n° 1** » et « une **passe 3** reste à lancer ». « **15 contrôles** `npm run check` » : il y en a 16. Simplification n° 9 : « l'étalonnage de la valeur acquise **n'appelle pas** `valeur_acquise()` » — il l'appelle depuis la passe 4. « toute V3 est registrée » : 20 feuilles sur 52. | Dire ce qui est corrigé, ce qui est en dette, et ce qui reste ouvert. Un bilan qui surestime ce qui est acquis est plus dangereux qu'un bilan absent — c'est l'argument du module lui-même. |
| **M11 · `QA/grilles-72.md` note TV 3/3 partout, en citant la règle de cadence que le module répudie.** | majeur | Le fichier porte toujours « la **règle de cadence** `max(coffrage, ferraillage) + bétonnage` est maintenant publiée et démontrée », « 10 V3 balisées et registrées » (27), « Minimum 2 partout : **tenu** » — alors que la passe 4 a conclu « NON TENU, deux critères à 1 ». Trois passes de retard. M8 de la passe 4, non corrigé. | Renoter après cette passe (ma grille est au § 7), et faire du fichier une sortie du build. |
| m1 · Figure 2 montre le planning brut sans le dire, sans repère de conflit ni profil d'occupation | mineur | mesuré : Z1/DEC 7,55–8,05 ∩ Z3/COF 6,80–8,57. | ajouter les six marqueurs et une bande d'occupation de la grue. |
| m2 · « les equipe ferrailleurs_poutres » dans la prose publiée | mineur | corrigé de l'exercice 2 : « ce ne sont plus les ferrailleurs de dalle, ce sont **les equipe ferrailleurs_poutres** (2,52 j…) ». `ressource_qui_borne` est une clé technique injectée telle quelle dans une phrase française. | rendre un libellé, pas une clé. |
| m3 · L'axe de la figure 5 dit « % » sans dire de quoi | mineur | l'unité est le % du budget à l'achèvement, ce qui est précisément ce qui a changé. | « % du budget (BAC) ». |
| m4 · H014 et H019 sont la même hypothèse, deux fois, avec deux valeurs | mineur | m5 de la passe 4, en dette non déclarée. | fusionner, et contrôler l'unicité de l'énoncé. |
| m5 · « deux et trois zones ouvertes » (3 niveaux mesurés), zéros de la figure 4 pas à la fin, figure 2 sans légende, poutres « au milieu de chaque zone » | mineurs | m1 à m4 de la passe 4, en dette non déclarée. | — |

**3 bloquants · 11 majeurs · 5 mineurs (+ 4 reportés) = 23 défauts.**

---

## 6. Ce que les corrections de la passe 4 ont donné, et ce qu'elles ont cassé

| Correction annoncée | Constat |
|---|---|
| **B1 p4 — valeur acquise physique** | **Tient sur le fond.** VA, VP et la courbe en S sont la valorisation de l'état physique ; mon recalcul indépendant les retrouve ; l'écart vertical de la figure 5 est enfin SV pour la bonne raison. **Mais la correction a cassé le contre-calcul** : l'écart en dirhams est passé de 0,89 % à 1,31 %, au-delà du seuil, et l'assertion a été remplacée par un `print("info")` — le module publie désormais une affirmation fausse (**B1**). |
| **B2 p4 — taux de recouvrement** | **Tient entièrement, et c'est la meilleure correction des cinq passes.** Mesurée au pixel sur la figure 3, relue par un test dans les dates du réseau, cohérente avec `data/`, la balise et H024. Canari C1 rouge. |
| **B3 p4 — conflits de grue** | **Moitié.** La détection est exhaustive et le nombre publié est juste. La **résolution** n'est vérifiée par rien (canari C5 muet), sa justification contredit le tableau des marges du même module, son coût en immobilisation n'est pas recalculé, et la figure qui porte la preuve n'a pas été touchée (**B2**). |
| **M1 p4 — rattachement poste → tâche** | **Tient.** Cinq dates, recalcul hors de la fonction, canari N4 rouge. Le rattachement est juste sur le fond, poste par poste. |
| **M5 p4 — `8.56` en dur** | **Tient.** |
| **M7 p4 — sécurité** | **Tient sur le contenu** (rien de normatif, rien de faux, rien de dangereux, et le lien planning/sécurité est le meilleur passage du module). **Le contrôle, lui, ne contrôle qu'un mot** (**M4**). |
| **Étalonnage qui appelle la bibliothèque** | **Tient.** La réserve de la passe 4 (le cas fermé posé sur le modèle linéaire) est levée. |
| **`_nature: "decision"`** | **Décoratif** : aucun contrôle ne le lit, et il cohabite avec `niveau_preuve: "V3"` (**M7**). |
| **SV dans le tableau S6** | **Tient.** |
| **M2, M3, M4, M6, M8, M9, M10 p4 et les onze mineurs** | **Non corrigés** — ce qui était la recommandation de la passe 4 — mais **non portés en dette** non plus, et `STATE.md` les déclare « tous corrigés » (**M10**). Deux d'entre eux sont aggravés : M6 (une fonction non couverte de plus) et M8/M11 (la grille vieillit d'une passe). |

**Ce que les corrections ont cassé, en une phrase** : deux contrôles sur trois créés ou touchés par la
passe 4 ne peuvent pas échouer, et le texte publié n'a pas suivi le calcul sur les deux points où il
change de sens.

---

## 7. Grille du § 7.2

| Critère | Note | Appui |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | inchangé, et S7c ajoute le meilleur passage du module : les trois accidents du cycle sont des accidents de **planning**. |
| Les hypothèses sont explicites | **2** *(était 1)* | H023 et H024 disent enfin ce que le réseau fait, et un test le relit. Mais 32 scalaires V3 restent hors registre, `_nature: "decision"` n'est lu par rien, et deux clés contradictoires cohabitent dans `effectifs`. |
| Les formules sont justifiées | **2** | la règle de cadence est complétée par une détection de conflits instantanés — vrai progrès. Mais la résolution s'appuie sur une « marge » que le module chiffre à 0,00 j, trois fonctions n'ont aucune vérification dimensionnelle, et la variante recommandée viole la contrainte de parc. |
| L'exemple est vérifié | **2** *(était 1)* | les huit grandeurs publiées sont reproductibles depuis `data/` seul, à l'arrondi près ; six canaris rejoués et quatre neufs sonnent. Mais **trois contrôles sont prouvés incapables d'échouer** (C5, C6, C9) et une phrase publiée affirme le contraire de ce que `calc/` rend. C'est un 2 fragile, et il retombe à 1 si B1 n'est pas corrigé. |
| Le piège est identifié | **3** | toujours le meilleur critère du module. |
| Lien avec l'exécution | **3** *(était 2)* | double lecture, point d'arrêt comme tâche critique, contrainte de parc, et maintenant S7c : hiérarchie des protections juste, colonne maîtrise d'œuvre au bon niveau, aucune valeur normative. |
| Lien avec le coût et le délai | **2** | VA, VP, SV et la courbe en S parlent enfin la même langue. Mais le titre du § S6 mélange deux unités, et le corrigé de l'exercice 3 recommande un planning que le module déclare inexistant. |

**Minimum 2 partout : TENU** — pour la première fois depuis la passe 2, mais avec deux notes qui
tiennent à la correction de B1 et de B3.

---

## 8. La question de fond : la onzième erreur

Je dois commencer par ce qui a marché, parce que c'est nouveau.

**Pour la première fois, le dépôt contient une confrontation entre deux représentations, et elle a
attrapé un de mes canaris.** Le test « l'écart vertical de la figure EST bien SV » confronte le SVG
calculé au tableau de valeur acquise ; mon canari C3, qui faussait `valeur_physique` d'un facteur
1,10, est mort là et nulle part ailleurs. De même, le test de relecture des taux de recouvrement
confronte un **paramètre déclaré en mots** au **réseau qu'il engendre** : c'est exactement la règle
que la passe 4 demandait d'inscrire dans `DECISIONS.md`, elle est écrite (D-027), elle est
implémentée, et elle tue mon canari C1. **Ces deux-là sont des garanties réelles.**

**Et pourtant les trois bloquants de cette passe sont, encore, la même chose.** Le motif a seulement
changé de place : il n'est plus dans le modèle, il est dans **le consommateur du contrôle**.

1. **Un contrôle qui calcule juste et que personne n'interroge.** `conflits_apres_resolution` est
   calculé en retirant la ressource au lieu de la décaler : il vaut 0 par construction (C5).
   `coffrage_suffisant` est calculé pour les quatre variantes et lu pour une seule — celle qui passe
   (B3). L'écart du contre-calcul en dirhams est calculé, dépasse son seuil, rend un `verdict` qui
   dit « ECART », et finit dans un `print("info")` (B1, C9).
2. **Une prose qui n'a pas suivi le calcul.** « budget à l'achèvement × avancement déclaré » décrit
   une formule supprimée. « sous la tolérance de 1 % » décrit un contrôle qui a échoué. « dans sa
   marge, pas sur le chemin critique » décrit une tâche que le tableau voisin donne critique à marge
   nulle. Les trois sont des phrases écrites **à la main** à côté d'un nombre **calculé**, et c'est
   précisément le geste que le § 4.3 interdit pour les nombres. La règle n'a pas été étendue aux
   **qualifications** de ces nombres : « sous le seuil », « dans sa marge », « suffisant » sont des
   verdicts, et un verdict se calcule.
3. **Un garde-fou posé d'un côté seulement.** `attendu` est obligatoire parce que le rendre optionnel
   « aurait laissé le défaut revenir en silence » ; `planifie`, qui porte exactement le même risque,
   est resté optionnel avec le modèle condamné en repli (C6).

**Ce qui garantit maintenant ce qui n'était pas garanti.** Le dépôt a six représentations réellement
indépendantes, et je peux dire ce que chacune contrôle :

| Représentation | Ce qu'elle contrôle | Preuve dans cette passe |
|---|---|---|
| **Le réseau** (`cpm.py`, deux algorithmes, étalonné sur 9 cas fermés) | les dates, le cycle, le chemin critique, les marges | cycle 8,052 recalculé à l'aveugle = 8,053 publié |
| **Le réseau relu par ses paramètres déclarés** (D-027, **nouveau**) | qu'un taux écrit en mots dans `data/` produise ce qu'il annonce | **canari C1 rouge** |
| **L'état physique recalculé hors de la fonction, à 5 dates** (**nouveau**) | le rattachement poste → tâche | **canari N4 rouge**, muet à la passe 4 |
| **Les quantités relevées** (voie B) | que l'avancement déclaré colle aux attachements ; elle ne passe ni par le réseau ni par le déclaré | elle **diverge réellement** de 1,31 % — la voie est bonne, c'est son seuil qui est mort (B1) |
| **Le SVG rendu** | que la figure montre ce que la légende promet | FED à 1,890 j = 40,0 % de FEP ; écart coté 18,7 pts = SV |
| **Les fourchettes déclarées** (20 feuilles sur 52) | qu'une valeur ne sorte pas de son intervalle | canaris de borne rouges |
| **La confrontation figure ↔ tableau** (**nouveau**) | que la courbe en S et le § S6 disent la même chose | **canari C3 rouge** |

**Ce qui manque n'est plus une représentation, ni même une confrontation : c'est que chaque
confrontation ait le droit de dire non.** Trois des sept ci-dessus produisent un nombre que rien
n'autorise à faire échouer le build. La règle à inscrire dans `DECISIONS.md` avant toute duplication
est la suite directe de celle de la passe 4 :

> **Tout verdict publié au lecteur — « sous le seuil », « suffisant », « résolu », « OK » — est une
> sortie de `calc/`, jamais une phrase écrite à la main à côté d'un nombre calculé. Et tout contrôle
> qui rend un verdict doit avoir un canari qui le fait passer au rouge, versé au dépôt.**

Un contrôle sans canari n'est pas un contrôle : c'est une case cochée par l'auteur, et le § 12 dit
depuis le début que cela ne prouve rien.

---

## 9. Verdict

**Reste-t-il un bloquant ? OUI — trois.**

1. **B1** : le module publie « Écart : 1,30 %, sous la tolérance de 1 % » quand son propre fichier
   rend `verdict = "ECART"` ; et le contrôle ne peut plus sonner (canari C9 : 10,22 %, tout vert).
2. **B2** : « les 6 conflits tombent à 0 » est vérifié par un calcul qui vaut 0 par construction
   (canari C5), et justifié par une marge que le module chiffre lui-même à 0,00 j.
3. **B3** : la réponse modèle de l'exercice 3 demande 1 697 m² de tables pour un parc de 1 300 —
   déficit de 397 m² calculé par le module, jamais lu, jamais publié, contre la règle que le module
   enseigne deux pages plus haut.

**Les corrections de la passe 4 ont-elles cassé quelque chose ?** Oui, deux choses, et les deux sont
des effets de bord de corrections justes :

- la correction de la valeur acquise a **créé** le dépassement de tolérance du contre-calcul (0,89 %
  → 1,31 %), parce que les relevés de `data/` sont volontairement en retrait de l'état physique ;
  au lieu d'être traité, le dépassement a été dégradé en `info` et expliqué par une alarme qui
  n'avait jamais existé ;
- la correction de la grue a ajouté une fonction de résolution dont la vérification est vide, et une
  phrase d'explication qui contredit le tableau des marges publié par le même module.

Le reste des corrections tient, et deux d'entre elles sont excellentes : **le taux de recouvrement
relu dans les dates du réseau** et **l'état physique testé à cinq dates** — toutes deux ont tué des
canaris qui passaient à la passe 4.

**Ce module peut-il servir de modèle aux cinquante suivants (§ 5.3) ? Pas encore, mais la distance
est désormais mesurable et courte.** La forme est acquise et stable : la chaîne `data → calc → rendu`
tient, les cinq figures sont générées et mesurables, deux d'entre elles exactes au pixel, la double
lecture entreprise/MOE est au bon niveau, S7c donne enfin au gabarit sa section de sécurité, les
pièges restent les meilleurs du dépôt, et six canaris sur six rejoués sonnent. La grille du § 7.2
tient son minimum de 2 partout pour la première fois depuis la passe 2.

Ce qui reste n'est plus un modèle faux : **ce sont trois verdicts écrits à la main qui contredisent
le calcul placé juste à côté**. Les trois tiennent dans une demi-page de `content/` et une vingtaine
de lignes de `calc/`. Dupliqué tel quel, le gabarit transmettrait aux cinquante modules l'habitude
d'écrire « sous le seuil » à côté d'un chiffre qui ne l'est pas — dans un cours destiné à un chef de
projet suivi, dont tout le métier est de ne pas signer un verdict qu'il n'a pas recalculé.

**Ce que je recommande.** Corriger B1, B2, B3 et M1 — quatre points, tous dans `calc/` et dans une
demi-page de texte —, verser au dépôt les canaris C5, C6 et C9 pour qu'ils restent rouges, porter
M2 à M11 et les mineurs en **dette déclarée** dans `STATE.md` (et corriger les quatre affirmations
fausses de ce fichier), puis une passe n° 6 **très courte**, bornée à ces quatre points et à leurs
canaris. Après quoi le go de l'Étape 2 me paraît justifié : les onze premiers bloquants portaient sur
ce que le module **calcule**, ces trois-ci sur ce qu'il **dit de son calcul**, et c'est un progrès
réel.
