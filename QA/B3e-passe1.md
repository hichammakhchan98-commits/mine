# Passe adversariale /devil — module B3e « Béton armé en exécution »

Relecteur hostile, indépendant de l'auteur. Date : 26/10/2026.
Entrées lues : `CLAUDE.md`, `DECISIONS.md` (D-033 à D-042), `STATE.md`,
`content/06-b3e-beton-arme-execution.md`, `modules/06-b3e-beton-arme-execution.html`,
`calc/ferraillage.py`, `calc/etalonnage/ferraillage_cas_ferme.py`,
`calc/tests/test_ferraillage.py`, `calc/verif_unites.py`, `data/projet-gare.json`,
`calc/sorties/{ferraillage,tranche-plancher,gros-oeuvre,prix,metre-cage}.json`,
les 5 captures de `tests/captures/`.

Les tests de l'auteur sont **tous verts** (`test_ferraillage.py`, `ferraillage_cas_ferme.py`).
Aucun des défauts ci-dessous n'est vu par eux, et le § 2 explique pourquoi : la plupart des
contrôles **retapent la formule de production au lieu de la recalculer autrement**.

---

## 0. Contre-expertise à l'aveugle

Recalculs faits **depuis `data/projet-gare.json` seul**, avant toute lecture de
`calc/ferraillage.py` et de ses sorties. Script exécuté :

```python
import json, math
d = json.load(open('data/projet-gare.json'))
A = d['armatures']; P = A['plan']['poutre_PM1']; D = A['plan']['dalle_DM1']
rho = A['conventions']['masse_volumique_acier_kg_m3']          # 7850
Lc  = A['conventions']['longueur_commerciale_m']               # 12,0
lr  = A['du_plan_a_la_commande']['longueur_de_recouvrement_du_plan_m']['valeur']   # 1,00
ml  = lambda dia: math.pi/4*(dia/1000)**2*rho
```

Masses linéiques recalculées : HA8 0,3946 · HA12 0,8878 · HA14 1,2084 · HA16 1,5783 ·
HA20 2,4662 · HA25 3,8534 kg/m. **Concordent** avec celles publiées (§ 1, point 1 : RAS).

### 0.1 — Masse du repère A1, de bout en bout (3 HA25 filantes de 24,00 m, 2 poutres)

Une filante de 24,00 m se reconstitue avec des barres de 12,00 m qui **se recouvrent sur
1,00 m**. Le recouvrement consomme de la longueur : *n* barres couvrent
`n·12,00 − (n−1)·1,00`.

| n barres | longueur couverte | suffit pour 24,00 m ? |
|---|---|---|
| 2 | 2×12 − 1×1 = **23,00 m** | **non** |
| 3 | 3×12 − 2×1 = 34,00 m | oui |

→ **2 recouvrements**, L façonnée = 24,00 + 2×1,00 = **26,00 m**
→ masse = 6 × 26,00 × 3,8534 = **601,1 kg**

**Publié : 1 recouvrement, 25,00 m, 578,0 kg** → écart **−23,1 kg (−3,8 %)** sur ce seul repère.
Même erreur sur B1 (−6,3 kg). Voir B-1.

### 0.2 — Masse totale de la nappe D1 (HA14, e = 12,5 cm, barres de 7,90 m)

`geometrie.mezzanine.zones_de_coulage` : zone = **15,00 × 24,00 m = 360 m²**.
`elements.dalles[DM1].portee_m = 7,50` ; la barre fait 7,90 m (7,50 de portée + 0,40 d'about).
Le sens porteur est le sens de la portée, donc la nappe se déroule sur une largeur
`360 / 7,50 = 48,00 m` (2 travées de dalle × 24,00 m de largeur de zone).

```
nombre de barres = 48,00 / 0,125 = 384
L totale = 384 × 7,90 = 3 033,6 m
masse    = 3 033,6 × 1,2084 = 3 665,8 kg
```

**Publié : 365 barres, 2 883,5 m, 3 484,5 kg** → écart **−181,3 kg (−4,9 %)**.
Contrôle de couverture décisif : `365 × 0,125 = 45,63 m` **< 48,00 m** → avec la nappe
publiée, **2,38 m de largeur développée de dalle (≈ 18 m²) n'ont aucune armature inférieure**.
Voir B-2.

Nappe D2 recoupée : 360/0,20 = 1 800 m → 1 598,1 kg — **concorde**, mais sans aucun
recouvrement sur des lignes de 24,00 m faites de barres de 12,00 m (voir M-7).

### 0.3 — Nombre de cadres et leur masse

Poutre continue de 24,00 m : 9,00 m à 10 cm + 15,00 m à 20 cm (la somme fait bien 24,00 m).

```
intervalles = 9,00/0,10 + 15,00/0,20 = 90 + 75 = 165
cadres      = 165 + 1 = 166        ← « intervalles + 1 », UNE fois, pour la poutre
```

Périmètre d'axe = 2 × (0,282 + 0,682) = **1,928 m** — **concorde**.
166 × 2 poutres = 332 cadres → 640,1 m → **252,6 kg**.

**Publié : 167 par poutre, 334 au total, 254,1 kg.** Le « +1 » est appliqué **par zone**, alors
que les deux zones sont contiguës sur la même poutre : le cadre de jonction est compté deux
fois. Voir B-3.

### 0.4 — Ratio kg/m³ des poutres

| Base du volume | Volume | Ratio du plan | Fourchette [140 ; 220] |
|---|---:|---:|---|
| Retombée seule (2 × 24 × 0,35 × 0,50) | 8,40 m³ | **173,1 kg/m³** | DANS |
| Section pleine (2 × 24 × 0,35 × 0,75) | 12,60 m³ | **115,4 kg/m³** | **HORS** |

Le module publie 173,1 et le verdict « dans la fourchette ». **La base n'est nommée nulle
part** — ni dans `ratios_V3.acier_poutre_kg_m3` (qui, contrairement à `coffrage_rives_pct` et
`part_main_oeuvre_directe_pct`, n'a pas de champ `note`), ni dans le module. Le verdict bascule
avec la base. Voir B-5 (D-037).

### 0.5 — Voie A recalculée en entier

| Poste | Recalcul indépendant | Publié | Écart |
|---|---:|---:|---:|
| A1 (6 × 26,00 m) | 601,1 kg | 578,0 | −23,1 |
| A2 (18 × 6,40 m) | 284,1 kg | 284,1 | 0 |
| B1 (4 × 26,00 m) | 164,1 kg | 157,8 | −6,3 |
| B2 (12 × 4,80 m) | 142,1 kg | 142,1 | 0 |
| B3 (8 × 3,00 m) | 37,9 kg | 37,9 | 0 |
| C1 (332 cadres) | 252,6 kg | 254,1 | +1,5 |
| **Poutres** | **1 481,9 kg** | 1 454,0 | **−27,9** |
| D1 (384 barres) | 3 665,8 kg | 3 484,5 | −181,3 |
| D2 | 1 598,1 kg | 1 598,1 | 0 |
| D3 | 1 392,1 kg | 1 392,1 | 0 |
| **Dalle** | **6 656,0 kg** | 6 474,7 | **−181,3** |
| **VOIE A** | **8 137,9 kg** | **7 928,7** | **−209,2 (−2,6 %)** |

Cascade aval fausse d'autant : chutes, ligatures, commande, écart au ratio, « −9,0 % »,
ratio global « 80,6 kg/m³ », fiche mémo.

### 0.6 — Deux recoupements supplémentaires

**Ligatures.** `data` définit le taux comme « part de la masse d'acier **POSÉE** » (1 %).
1 % de l'acier du plan = **79,3 kg**. Publié : **83,3 kg**, soit 1 % de *plan + chutes*.
On ne ligature pas des chutes. Voir M-1.

**Crochets.** Le module écrit « l'écart mesuré… était d'environ **3 %** de la masse des cadres.
Appliqué ici, cela représente **une trentaine de kilogrammes** ». 3 % × 254,1 = **7,6 kg**.
Les deux nombres de la même phrase sont incompatibles d'un facteur 4. Voir B-9.

---

## 1. Les dix points du § 12.2

**1 · Unités et homogénéité dimensionnelle.** RAS sur l'homogénéité : `calc/verif_unites.py`
l. 198-240 vérifie π/4·d²·ρ → kg/m, L façonnée → m, masse → kg, 1/espacement → m⁻¹,
ratio → kg/m³, périmètre → m, avec trois contre-contrôles qui lèvent bien. Preuve :
exécution du fichier. **Mais** la formule fautive du § 0.2 est dimensionnellement correcte
(m²/m × m⁻¹ = sans dimension) : l'homogénéité ne pouvait pas l'attraper, et rien d'autre ne
la contrôle. Le passage « plan → commande » (pourcentages) n'est pas dimensionné du tout.

**2 · Référentiels mélangés.** RAS. Preuve : aucun référentiel n'est cité dans le module ;
`referentiels.json` n'est pas lu par `ferraillage.py` ; les sept lignes de `controles` portent
« ⏸ » ou « non normatif » dans la colonne `statut_de_la_regle`.

**3 · Valeur citée sans V0/V1 — et violations du § 5.0.** Pas de violation frontale du § 5.0 :
l'enrobage (3 cm), le recouvrement (1,00 m) et les espacements (10/20 cm) sont présentés comme
**cotes du plan fictif**, avec la règle marquée ⏸ (`calc/ferraillage.py` l. 495-530). C'est
correct. Trois réserves, toutes instruites en § 2 :
(a) le plan est **calibré** sur les ratios V3, et le module s'appuie sur ce calibrage pour
affirmer que « l'ordre de grandeur tient » — c'est circulaire (B-4) ;
(b) le plan prétend illustrer « la forme du moment » alors qu'il la contredit (B-11) ;
(c) le tableau des dix masses linéiques du `ferraillage_cas_ferme.py` est donné comme
« publié par les producteurs d'acier » **sans aucune source**, puis utilisé comme étalonnage
externe (M-11).

**4 · Ordres de grandeur et ratios.** Deux constats.
(a) Base non déclarée du ratio poutre : le verdict bascule DANS/HORS selon qu'on prend la
retombée ou la section pleine (§ 0.4) → B-5.
(b) Plausibilité du plan « fictif mais calibré » : acier de travée = 3 HA25 + 3 HA20 =
**24,15 cm²** ; acier sur appui intermédiaire = 2 HA16 + 3 HA20 = **13,44 cm²**. Or pour trois
travées égales sous charge uniforme, |M_appui| = 0,100 wL² et M_travée = 0,080 wL², soit un
**rapport 1,25 en faveur de l'appui** (RDM pure, V1, aucune norme requise). Le plan donne
**0,56**. → B-11.

**5 · Cohérence data / SVG / métré / coût / planning / autres modules.** Six défauts prouvés :
B-2 (nappe qui ne couvre pas la dalle), B-6/B-7/B-8 (figures contre données), M-5 (trois
listes fermées différentes pour le même point d'arrêt, entre C3 et B3e), M-6 (« elle se place
la veille » contre `points_d_arret.le_piege` de C3), M-12 (console de marquise de PM1
supprimée sans un mot). L'estimation reprise de TV (8 712 kg) et sa fourchette
[7 026 ; 10 848] concordent avec `tranche-plancher.json` : RAS sur ce point.

**6 · Grille de profondeur § 7.2.** Trois critères sur sept sous le minimum de 2. Détail § 3.

**7 · Sécurité.** La rubrique S4g existe et est bonne sur l'essentiel (embouts sur **toutes**
les attentes, palonnier et stabilisation avant approche, passerelles posées avant le
ferraillage, constat sur l'ouvrage jamais pendant le coulage), et elle porte l'avertissement
« essentielles et non exhaustives » exigé par le § 3.4. Pas de conseil dangereux.
Une omission : **rien sur le risque de renversement d'une cage de poutre en attente de pose**
(les cages de 24,00 m de ce plan pèsent 742 kg à l'unité) ni sur le stockage debout.
→ mineur m-8.

**8 · Vérité du rendu.** Zéro `{{`, `NaN`, `undefined` dans le HTML (preuve : `grep -c`).
Mais **trois défauts de figure prouvés aux captures** : B-6, B-7 (figure 1), B-8 (figure 2),
plus quatre mineurs. Les cinq figures rendent non vides, la bande de la figure 4 est
géométriquement juste (vérifiée : rect x=505,47 w=107,29 avec échelle 0,028072 px/kg →
[7 026 ; 10 848] exactement).

**9 · Simplifications non signalées (R6).** Quatre : zones de cadres traitées comme des
longueurs continues alors qu'elles sont **cumulées** (B-3, M-8) ; recouvrements absents des
nappes alors qu'ils sont comptés sur les poutres (M-7) ; console de 4,50 m de PM1 supprimée
(M-12) ; 82 % de la masse métrée (la dalle) jamais tabulée dans le module (M-9).

**10 · Texte télégraphique ou remplissage.** RAS. Le module est dense, en phrases, chaque
paragraphe porte une règle ou un chiffre. S2 est la meilleure page du module. Preuve : lecture
intégrale des 508 lignes de `content/06-b3e-beton-arme-execution.md`.

---

## 2. Défauts

### Bloquants

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **B-1 · La formule du nombre de recouvrements est géométriquement fausse, et le module l'affirme comme une évidence** — `n_rec = ⌈L/L_c⌉ − 1` donne 1 recouvrement pour 24,00 m en barres de 12,00 m. Deux barres de 12 m recouvertes sur 1,00 m ne couvrent que **23,00 m**. Il en faut trois, donc **2 recouvrements**, L façonnée **26,00 m**. L'incohérence est visible dans la nomenclature elle-même : on ne coupe pas 25,00 m de barre dans 2 × 12 m de stock. | bloquant | `calc/ferraillage.py` l. 93 : `n_rec = math.ceil(Lu / Lc) - 1`. Sortie `ferraillage.json` → `nomenclature.lignes[0]` : `recouvrements_par_barre: 1`, `longueur_faconnee_m: 25.0`. Module l. 130-135 : « une filante de 24 m faite de barres de 12 m en demande **un**, et aucun règlement n'y peut rien ». Recalcul § 0.1. | `n_rec = ceil((L − L_c)/(L_c − L_rec))` si `L > L_c`, sinon 0. Vérifier A1 = 601,1 kg, B1 = 164,1 kg. Corriger la formule KaTeX de S3c **et** de la fiche mémo, l'exercice 1 et le quiz 2 (qui répondent tous « 25,00 m » et « un recouvrement »). |
| **B-2 · La nappe D1 ne couvre pas la dalle : 365 barres au lieu de 384, et 2,38 m de largeur développée sans armature inférieure** — la largeur à armer est `surface / portée` (7,50 m), pas `surface / longueur de barre` (7,90 m). La surlongueur d'about est comptée comme de la couverture. | bloquant | `calc/ferraillage.py` l. 227-229 : `largeur = n["developpe_sur_m2"] / n["longueur_barre_m"]`. `data` → `elements.dalles[DM1].portee_m = 7.5` et `armatures.plan.dalle_DM1.ouvrage` : « portée 7,50 m entre poutres ». Contrôle de couverture : 365 × 0,125 = 45,63 m < 48,00 m. Recalcul § 0.2 : 3 665,8 kg contre 3 484,5 publiés (−4,9 %). | Lire la portée dans `elements.dalles` et calculer `largeur = surface / portee_m`. Ajouter le test manquant, le seul qui attrape la famille entière : `nombre × espacement ≈ largeur à couvrir` pour chaque nappe. Répercuter sur voie A, commande, ratios, fiche mémo. |
| **B-3 · Le « piège du comptage » des cadres est lui-même faux : 167 publiés au lieu de 166** — le « +1 » est ajouté **par zone d'espacement**, mais les deux zones sont contiguës sur la même poutre de 24,00 m : il n'y a qu'un cadre d'extrémité supplémentaire pour toute la poutre, pas un par zone. Le module en fait un enseignement (tableau S4b, formule, quiz 3, S5) et publie donc une règle de comptage erronée. | bloquant | `calc/ferraillage.py` l. 176 : `n = math.floor(L/s) + 1` **dans la boucle sur les zones**. `ferraillage.json` → `cadres.nombre_par_poutre: 167`, `_piege_du_comptage` : « Compter L/s au lieu de L/s + 1 en donnerait 165, soit 2 de moins : **un par zone d'espacement** ». Recalcul § 0.3 : 165 intervalles sur 24,00 m → **166** cadres. | Compter les intervalles zone par zone et ajouter **un seul** cadre pour la poutre : `sum(L_i/s_i) + 1`. Réécrire `_piege_du_comptage`, la formule KaTeX de S4b et de la fiche mémo, le quiz 3 et la ligne S5. |
| **B-4 · Le § 3.3 n'est pas satisfait : les deux voies ne sont pas indépendantes, et le module affirme le contraire au moment où il conclut** — le plan a été **calibré sur `ratios_V3`** ; la voie B est `ratios_V3 × béton`. La voie A tombe donc dans la bande **par construction**, et la comparaison n'établit rien, pas même l'ordre de grandeur. | bloquant | `data.armatures._calibrage` : « Les diamètres et les espacements de ce plan fictif sont **CALIBRÉS sur les ratios V3 du projet** (`ratios_V3.acier_poutre_kg_m3` et `acier_dalle_kg_m3`) ». Figure 4, « ce qu'il faut voir », puce 2 : « La voie A tombe dans la bande. **C'est tout ce que la comparaison établit : l'ordre de grandeur tient.** » Et `test_ferraillage.py` l. 139-141 : `verifie("le plan fictif reste dans la fourchette V3 de CHAQUE element", dv["tous_dans_la_fourchette"])`. | Dire la circularité **à l'endroit de la conclusion**, pas seulement dans `_calibrage` : « cette comparaison ne prouve rien ici, parce que le plan a été fabriqué pour la satisfaire ; sur un plan reçu du BET, elle prouverait l'ordre de grandeur ». Ou produire une vraie seconde voie indépendante (métré par section d'acier × longueur, ou par masse au m² de nappe). Sans cela, O7 est « sans objet » non justifié pour un module de calcul, ce que le § 6.3 interdit. |
| **B-5 · Un ratio de contrôle est publié et rend un verdict sans que sa base soit définie — D-037 en toutes lettres** — 180 kg/m³ est appliqué à la **retombée seule** (8,40 m³). Sur la section pleine (12,60 m³) le plan tombe à 115,4 kg/m³ et sort de la fourchette. Rien, ni dans `ratios_V3`, ni dans `deux_voies`, ni dans le module, ne nomme la base. | bloquant | `calc/plancher.py` l. 32 : `beton_poutres = n_poutres * long_poutre * b * retombee`. `data.ratios_V3.acier_poutre_kg_m3` = `{valeur, fourchette}` **sans champ `note`**, là où `coffrage_rives_pct` et `part_main_oeuvre_directe_pct` en portent un. `ferraillage.json` → `deux_voies.elements[0].dans_la_fourchette: true`. Recalcul § 0.4. D-037 : « Tout ratio de vérification publié par le cours **nomme la base** sur laquelle il est calculé, et le calcul **refuse de rendre un verdict** sur une base où le ratio n'est pas défini ». | Ajouter `note` à `ratios_V3.acier_poutre_kg_m3` : base = volume de **retombée** sous dalle. Publier `ratio_defini_sur_cette_base` dans `deux_voies.elements[]`, comme `calc/prix.py` le fait déjà pour `controle_ratios`, et un test qui interdit le verdict sans la base. Dire dans S4c que sur la section pleine le verdict serait l'inverse. |
| **B-6 · La figure 1 est titrée « coupe en travée » mais ne dessine pas la section en travée** — à mi-travée, le lit inférieur porte A1 (3 HA25) **et** A2 (3 HA20, qui court de 0,80 à 7,20 m). La figure ne montre que les filantes. Sa légende affirme pourtant la complétude. | bloquant | `calc/ferraillage.py` l. 566-573 : `_filante(p, "inf")` ne retient que la barre `filante: true`. Capture `…figure1.png` : 3 cercles à y=268,65 (r=3,8 → HA25) et 2 à y=69,98 (r=2,43 → HA16), rien d'autre. Texte « ce qu'il faut voir » : « **Les lits se comptent ici et nulle part ailleurs** : 3 HA25 en bas (repère A1) ». Données : `armatures.plan.poutre_PM1.barres[A2].positions[0] = {de_m: 0.8, a_m: 7.2, n: 3}`. | Soit dessiner la coupe réelle à une abscisse donnée (filantes + tous les repères dont l'intervalle contient l'abscisse, abscisse affichée dans le titre), soit retitrer « coupe des armatures filantes » et retirer « et nulle part ailleurs ». La première solution est la seule compatible avec l'étape 3 de S3a, qui dit que la coupe est l'endroit où l'on compte les lits. |
| **B-7 · La figure 1 dessine un élément qui n'est pas dans sa légende** — le lit supérieur (2 HA16, repère B1) est tracé, mais la légende ne compte que trois entrées, dont « 2 · barres longitudinales, **lit inférieur** ». Le § 8 impose que chaque numéro du dessin figure dans la légende et inversement. | bloquant | SVG de la figure 1 dans `modules/06-b3e-beton-arme-execution.html` : `<circle cx="110.78" cy="69.98" r="2.43">` et `cx="189.22"` (lit supérieur, non repéré) ; légende = 3 `<text class="leg-txt">` : « béton », « barres longitudinales, lit inférieur », « cadre, tracé sur son axe ». | Ajouter un repère 4 « barres longitudinales, lit supérieur (B1) », ou fusionner en « barres longitudinales » avec les deux lits repérés. Ajouter au `check.mjs` le contrôle « tout élément dessiné porte un numéro » pour les coupes, pas seulement « tout numéro a une légende ». |
| **B-8 · Le plan dessiné et la nomenclature ne disent PAS la même chose sur B3, et le test hardcode l'exception pour que ça passe** — B3 est chiffré 3,00 m (2,40 droit + 0,60 de retour d'équerre) et dessiné 2,40 m, sans retour. Or le module fait de cette égalité le contrôle n° 5 de la lecture d'un plan, et les données affirment qu'il est « vrai par construction dans ce cours ». | bloquant | `data.armatures.plan.poutre_PM1._elevation_note` : « le contrôle n° 5 — le plan dessine et la nomenclature chiffre la même chose — est ainsi **vrai par construction** dans ce cours ». `calc/ferraillage.py` l. 585-589 : `figures.elevation.aciers` ne porte que `de_m`/`a_m`, jamais `retours_m`. Capture `…figure2.png` : les deux segments B3 sont rectilignes, sans retour. `calc/tests/test_ferraillage.py` l. 251-255 : `abs((a_m − de_m) − longueur_unitaire + (0.6 if a["repere"] == "B3" else 0)) < 0.02` — **le 0,6 est écrit en dur pour neutraliser l'écart**. | Dessiner les retours sur l'élévation (un repli vertical de 0,60 m en about), ou retirer la phrase « vrai par construction ». Dans le test, lire `sum(retours_m)` depuis les données au lieu d'écrire 0,6 : un test qui connaît par cœur la valeur de l'écart qu'il tolère ne teste plus rien. |
| **B-9 · Deux nombres incompatibles dans la même phrase, et un « écart mesuré » qui n'a jamais été mesuré** — « l'écart **mesuré** entre un cadre fermé sans crochets et un cadre réel était d'environ **3 %** de la masse des cadres. Appliqué ici, cela représente **une trentaine de kilogrammes** ». 3 % × 254,1 kg = **7,6 kg**. Et l'origine du « 3 % » est une phrase d'intention du module de démonstration, pas une mesure : la longueur d'un crochet y est explicitement non calculée (⏸). | bloquant | Module l. 180-186. `calc/sorties/metre-cage.json` : `"crochets": false`, `crochets_note` : « Le métré est donc MINORANT d'**environ 3 %** sur les cadres. **La longueur d'un crochet est une valeur constructive : elle n'est pas avancée ici (§ 5.0)** ». `calc/cage.py` l. 96-97 lève si `crochets_extremite ≠ false` : aucun calcul avec crochets n'existe dans le dépôt. Masse des cadres publiée : 254,1 kg. | Retirer « mesuré ». Soit publier le minorant sans chiffrer ce qui manque (« de combien, on ne peut pas le dire sans le BAEL » — c'est la position du module ailleurs et elle est la bonne), soit déclarer une hypothèse V3 de longueur de crochet avec sa fourchette et calculer l'écart depuis les données. Ne pas garder deux nombres qui se contredisent d'un facteur 4. |
| **B-10 · L'effet que le module prétend démontrer n'existe pas dans ses propres chiffres** — « une poutre lourde compense une dalle légère » : les **deux** éléments sont plus légers que leur référence (−3,8 % et −10,1 %). Rien n'est compensé ; le global (−9,0 %) est simplement dilué de 1,1 point. L'argument du « ratio global » est juste en principe et faux sur ce cas. | bloquant | `ferraillage.json` → `deux_voies.elements[0].ecart_pct = −3.8`, `elements[1].ecart_pct = −10.1`, `ecart_pct = −9.0`. `_pourquoi_element_par_element` : « Comparer élément par élément évite qu'une **poutre lourde compense une dalle légère** ». S5, ligne 6 : « −9,0 % globalement, contre −10,1 % sur la dalle : une poutre lourde compense une dalle légère ». Le canari `test_ferraillage.py` l. 143-146 ne passe que grâce à ces 1,1 point d'écart. | Soit énoncer la règle sans prétendre que ce cas l'illustre (« ici les deux sont légers, donc le global ne masque rien — mais il le ferait si… »), soit construire l'illustration sur un cas où l'effet existe. Et remplacer le canari par le test de la **règle** (le verdict doit être rendu élément par élément), comme D-041 l'a imposé à C3. |
| **B-11 · Le plan fictif contredit la forme du moment qu'il prétend illustrer** — acier de travée 24,15 cm² (3 HA25 + 3 HA20) contre acier sur appui intermédiaire 13,44 cm² (2 HA16 + 3 HA20), soit **0,56**, alors que pour trois travées égales sous charge uniforme \|M_appui\|/M_travée = 0,100/0,080 = **1,25**. Un plancher continu a plus d'acier sur ses appuis qu'en travée ; celui-ci a l'inverse. Le module affirme pourtant que la logique du plan « se voit sans aucun calcul, c'est la forme du moment ». | bloquant | Figure 2, « ce qu'il faut voir », puce 2 : « les chapeaux B2 à cheval sur les appuis intermédiaires : **la logique se voit sans aucun calcul, c'est la forme du moment** ». Sections recalculées depuis `armatures.plan.poutre_PM1.barres` : A1 3 HA25 = 14,73 cm², A2 3 HA20 = 9,42 ; B1 2 HA16 = 4,02, B2 3 HA20 = 9,42. Les coefficients 0,100 / 0,080 sont de la RDM de poutre continue (V1, recalculable, aucune norme en jeu). | Recalibrer le plan en déplaçant de l'acier de A2 vers B2 pour que le rapport appui/travée dépasse 1 — c'est une correction de **forme**, pas un dimensionnement, et elle reste permise en § 5.0. À défaut, retirer la phrase « c'est la forme du moment » et écrire franchement que la **répartition** du plan fictif est arbitraire, le calibrage n'ayant porté que sur la masse totale. Se réfugier derrière « fictif » après avoir affirmé que le plan illustre le diagramme des moments n'est pas tenable (R8). |

### Majeurs

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **M-1 · Les ligatures sont calculées sur une base que les données interdisent, avec une justification physiquement fausse** — 1 % appliqué à *plan + chutes*. Les chutes sont les tombées de façonnage : elles ne sont pas dans la cage, donc pas ligaturées. | majeur | `data.armatures.du_plan_a_la_commande.ligatures_pct.note` : « fil à ligaturer, **en part de la masse d'acier posée** ». `calc/ferraillage.py` l. 350 : `ligat = (masse_plan + chutes) * …`. Figure 5 : « on ligature l'acier qu'on a façonné, **chutes comprises dans le flux d'atelier** ». 79,3 kg contre 83,3 publiés. | Appliquer le taux à l'acier posé. Supprimer la justification. Le test l. 196-199, qui épingle la base fautive, doit tester la **définition des données**, pas l'implémentation. |
| **M-2 · Les cales sont publiées « pour la zone » alors qu'elles ne couvrent que la dalle — et l'exercice 3 du même module fait des cales de poutre son constat central** | majeur | `calc/ferraillage.py` l. 355 : `cales = nap["surface_m2"] * cales_par_m2` (360 m², domaine déclaré « partie courante de dalle »). Module : « **1440 cales d'enrobage pour la zone** ». Exercice 3 : « les cales d'enrobage sont en place sur la dalle mais **pas sous les poutres** […] sans cale sous la poutre, la cage descend au vibrage ». 2 poutres × 24,00 m de fond et de joues ne reçoivent aucune cale au métré. | Ajouter une ligne « cales de poutre » (par mètre de fond et de joue, hypothèse V3 déclarée) ou renommer la grandeur `cales_de_dalle_u` et dire que les cales de poutre sont à compter à part. Le test l. 215-217 doit vérifier la couverture, pas la formule. |
| **M-3 · L'étalonnage n'étalonne presque rien : trois de ses six cas retapent la formule de production au lieu d'appeler la bibliothèque** — les cas 4 (périmètre), 5 (comptage) et 6 (nappe) n'appellent aucune fonction de `ferraillage.py`. Aucun cas ne couvre `nomenclature_poutre`, `cadres_poutre`, `nappes_dalle`, `du_plan_a_la_commande`. Le § 3.3 est donc inopérant : sans étalonnage, ces résultats restent V3. | majeur | `calc/etalonnage/ferraillage_cas_ferme.py` l. 56-73 : `cas("perimetre analytique", 2*(b_ax+h_ax), 2*(0.2820+0.6820), …)` — les deux membres viennent de la même expression ; `cas("10,00 m a 20 cm", math.floor(10.0/0.20)+1, 51, …)` ; `cas("10 m de largeur a 12,5 cm", math.ceil(10.0*(100/12.5)), 80, …)`. Seules les l. 33-44 (`fe.masse_lineique_kg_m`) et 47-51 (`fe.longueur_developpee_m`) appellent la bibliothèque. | Faire porter chaque cas sur la **fonction** : `fe.cadres_poutre` sur une poutre d'essai à une seule zone, `fe.nappes_dalle` sur une dalle carrée où le compte de barres est évident à la main, `fe.nomenclature_poutre` sur une barre unique. Sinon, déclarer dans le module que ces fonctions ne sont pas étalonnées. |
| **M-4 · Le cas 6 de l'étalonnage valide une arithmétique fausse, et entérine deux règles de comptage contradictoires dans le même module** — « 10 m de largeur à 12,5 cm : **79 intervalles + 1**, arrondi supérieur du produit : 80 ». 10/0,125 = **80 intervalles**, donc 81 barres. Et surtout : les cadres comptent `floor(L/s) + 1`, les nappes `ceil(largeur × 100/s)` **sans +1**. Deux conventions pour le même problème géométrique, jamais rapprochées. | majeur | `ferraillage_cas_ferme.py` l. 69-71 (commentaire et cas). `calc/ferraillage.py` l. 176 (cadres, `+1`) contre l. 230 (nappes, pas de `+1`). | Trancher une règle et la justifier (la nappe de rive est-elle posée sur le bord ou à un demi-espacement ?), puis l'appliquer aux deux. Corriger le commentaire. |
| **M-5 · Trois listes fermées et différentes décrivent le même point d'arrêt, réparties entre C3 et B3e, sans qu'aucune renvoie aux autres** — C3 publie 6 « contrôles avant coulage » (« Ces **six** contrôles se font coffrage FERMÉ ») et un critère de point d'arrêt en 5 items ; B3e publie 7 « contrôles » et « les **sept** points d'un visa de ferraillage ». Elles se recoupent partiellement et se contredisent sur le périmètre : C3 omet diamètres/nombre, arrêts de barres et espacement des cadres — c'est-à-dire le cœur du visa de ferraillage. | majeur | `calc/sorties/gros-oeuvre.json` → `controles_avant_coulage.liste` (6) et `regle` ; `points_d_arret.liste[1].critere` = « sections, recouvrements, enrobages, cales, propreté du fond » (5) ; `calc/sorties/ferraillage.json` → `controles.liste` (7) ; fiche mémo B3e, « Les sept points d'un visa de ferraillage ». Aucun renvoi croisé dans les deux `content/`. D-039 : « quand deux modules ont besoin de la même grandeur d'état, la question n'est pas comment la recalculer pareil, mais **où la mettre pour qu'elle n'existe qu'une fois** ». | Mettre la liste **une seule fois** dans `data/` (ou dans un module de calcul commun), et faire que C3 et B3e la lisent, chacun filtrant ce qui le concerne. Un test vérifie que les items de C3 sont un sous-ensemble de la liste unique. |
| **M-6 · B3e contredit C3 sur le moment du visa** — B3e : « Le visa de ferraillage est une tâche du planning — 0,25 jour dans le cycle du module C3 — et **elle se place la veille** ». C3 : le point d'arrêt **tombe juste avant le bétonnage** ; c'est la **pré-visite** qui se fait la veille. | majeur | `gros-oeuvre.json` → `points_d_arret.le_piege` : « Le point d'arrêt du ferraillage tombe **juste avant le bétonnage** […] Un ferraillage se **pré-visite** la veille » ; `double_lecture.entreprise` : « prévenir la maîtrise d'œuvre la veille ». Exercice 3 de B3e, dernier paragraphe. | Écrire « la pré-visite se place la veille ; le visa reste juste avant le coulage, et c'est précisément pour cela qu'il faut l'avoir préparé » — ce qui est aussi la vraie leçon de l'exercice 3. |
| **M-7 · Les recouvrements sont comptés sur les filantes de poutre et oubliés sur les nappes de dalle, sans un mot** — les lignes de répartition D2 font 24,00 m de large et sont faites de barres de 12,00 m : elles demandent un recouvrement par ligne (≈ 75 lignes × 1,00 m ≈ +67 kg). Le métré les ignore, alors que le module construit tout un développement sur « les filantes plus longues qu'une barre du commerce portent-elles leurs recouvrements ? » (check-list, point 5). | majeur | `calc/ferraillage.py` l. 232 : `nb * n["longueur_barre_m"]`, aucun terme de recouvrement dans `nappes_dalle`. À comparer à l. 93. Check-list S7, point 5. | Compter les recouvrements de nappe, ou déclarer explicitement la simplification et son montant (R6). Le second choix est acceptable ; le silence ne l'est pas. |
| **M-8 · Les zones de cadres n'ont que des longueurs cumulées, sans bornes — et le module demande pourtant de contrôler l'espacement « dans chaque zone »** — 9,00 m « d'about et appuis » sur une poutre à 4 appuis correspond à 4 segments disjoints, 15,00 m de travée courante à 3 segments. Ni les données, ni l'élévation ne disent où ces segments commencent. Le contrôle publié est inexécutable sur le plan publié, et le comptage des cadres (B-3) en dépend. | majeur | `data.armatures.plan.poutre_PM1.cadres.zones[].longueur_cumulee_m`. `ferraillage.json` → `controles.liste[4]` : « Espacement des cadres — **au mètre, dans chaque zone** ». Capture `…figure2.png` : aucun cadre, aucune limite de zone n'est dessinée. D-042 : « un indice qu'on ne peut pas définir se publie comme indéfini ». | Donner les bornes des segments dans `data` (`segments_m: [[0,1.2],[6.8,9.2],…]`), les dessiner sur l'élévation, et en déduire le comptage. À défaut, écrire que le plan fictif ne porte pas le repérage des zones et que le contrôle correspondant est, sur ce plan, indéfini. |
| **M-9 · 82 % de la masse métrée n'est jamais montrée au lecteur** — S3d annonce « deux ouvrages, deux méthodes de métré », puis seule la poutre (1 454 kg, 18 %) reçoit un tableau, une figure par diamètre et un tableau de cadres. La dalle (6 475 kg) n'apparaît que par son total, dans la fiche mémo. La méthode des nappes est énoncée en une phrase et jamais appliquée sous les yeux du lecteur. | majeur | `content/06-b3e-beton-arme-execution.md` : `ferraillage.nappes.*` n'apparaît que 3 fois (l. 33 surface, l. 142 la phrase de méthode, l. 487 fiche mémo). Aucun tableau D1/D2/D3. C'est aussi pourquoi B-2 était invisible. | Ajouter en S4 le tableau des trois nappes (repère, Ø, espacement, barres/m, nombre, longueur, masse, masse au m²), avec la ligne de contrôle « nombre × espacement = largeur à couvrir ». |
| **M-10 · Les masses au m² des nappes sont publiées sur deux bases différentes et ne s'additionnent pas** — D1 et D2 sur 360 m², D3 sur 144 m² ; leur somme (23,79 kg/m²) ne vaut pas le total publié (17,99 kg/m²). Le module recommande pourtant cette grandeur comme **le** contrôle d'un métreur expérimenté. | majeur | `ferraillage.json` → `nappes.lignes[].masse_par_m2_kg` = 9,68 / 4,44 / 9,67 et `nappes.masse_par_m2_kg` = 17,99. `_controle_de_la_methode` : « c'est le nombre qu'un métreur expérimenté vérifie en premier ». D-037. | Publier chaque masse au m² **avec sa base** (`rapportee_a_m2`), ou toutes sur la surface de la zone. Un test qui vérifie l'additivité quand la base est commune. |
| **M-11 · L'« étalonnage externe » n'est pas externe, et sa table n'a pas de source** — le module écrit « le tableau du commerce sert d'**étalonnage externe** à la bibliothèque (§ 3.3) » deux lignes après avoir écrit que ces valeurs « sont des **sorties arrondies de cette formule** ». Les dix valeurs du `TABLEAU` ne portent ni référence, ni URL, ni date, ni niveau de preuve. | majeur | Module l. 116-121 ; `ferraillage_cas_ferme.py` l. 34-36 : « Valeurs publiées par les producteurs d'acier, arrondies au mg/m. **Source indépendante de la formule** ». Aucune ligne correspondante dans `data/registre-sources.csv`. (L'écart maximal annoncé, 0,5 g/m, est lui exact : 0,462 g/m sur HA10 — recalculé.) | Soit citer une source réelle (norme produit, catalogue daté) et l'inscrire au registre, soit requalifier : ces dix valeurs sont un contrôle d'**arrondi**, pas un étalonnage externe, et le § 3.3 reste à satisfaire par un autre cas (M-3). |
| **M-12 · La console de marquise de PM1 disparaît sans un mot** — `elements.poutres[PM1]` porte `console_m: 4.5`, et `geometrie.mezzanine.poutre_type_module_temoin` décrit « 3 travées **+ console de marquise** ». Le plan de B3e traite PM1 comme une poutre de 24,00 m qui finit sur deux appuis de rive, avec des chapeaux de rive de 2,40 m là où un porte-à-faux de 4,50 m devrait continuer. La figure 2 lit `travees_m` dans cet objet-là et laisse tomber `console_m`. | majeur | `calc/ferraillage.py` l. 578-583 : `el = d["elements"]["poutres"][0]` puis `"travees_m": el["travees_m"]` seulement. Capture `…figure2.png` : App. 4 est un appui de rive, rien au-delà. Aucune occurrence de « console » ou « marquise » dans `content/06-…md`. | Une phrase : « la marquise est exclue de la zone de coulage (`zones_de_coulage.marquise_exclue`) ; le plan de ce module s'arrête à l'appui de rive ». Sinon un lecteur confronte deux PM1 différentes entre le § 7.3 et B3e. |
| **M-13 · La note de données qui déclare le recouvrement se trompe de diamètres** — « longueur portée par le plan fictif **pour les filantes HA20 et HA14** ». Les seules filantes du plan sont A1 (HA25) et B1 (HA16) ; aucune barre HA20 ou HA14 ne porte de recouvrement dans le métré. C'est le reliquat de la version antérieure du plan, avant recalibrage — la même famille de défaut que le commentaire de `figures()` dit avoir corrigée sur la coupe. | majeur | `data.armatures.du_plan_a_la_commande.longueur_de_recouvrement_du_plan_m.note`. À comparer à `barres[A1].dia_mm = 25` et `barres[B1].dia_mm = 16`. Cette note est reprise telle quelle dans le registre : `registre-hypotheses.csv` H162. | Corriger la note et la ligne H162 du registre. Ajouter un test qui vérifie que les diamètres cités dans les notes de `data` existent dans le plan. |
| **M-14 · La surface 144 m² de la nappe D3 ne se dérive de rien, et contredit la longueur de poutre du même plan** — 144/3,2 = 45,00 m de ligne de poutre, alors que la zone porte 2 × 24,00 = **48,00 m** de poutres à chapeauter. | majeur | `data.armatures.plan.dalle_DM1.nappes[D3].developpe_sur_m2 = 144.0` et `longueur_barre_m = 3.2`, contre `poutre_PM1.longueur_m = 24.0`, `nb_dans_la_zone = 2`. | Dériver la surface des chapeaux de la géométrie (`2 × 24,00 × largeur de bande`) au lieu de la saisir, et ajouter le test de cohérence. D-040, transposé : une surface se mesure sur la géométrie, elle ne se saisit pas. |
| **M-15 · Les tests ne sont pas des contre-calculs : ils retapent la formule de production, et un « test » épingle une conclusion narrative** — recouvrements (l. 68-73), cadres (l. 83-86), base des ligatures (l. 196-199), cales (l. 215-217) : chacun réécrit l'expression de `ferraillage.py` et vérifie l'égalité. Et `verifie("le plan fictif reste dans la fourchette V3 de CHAQUE élément")` ne peut échouer que si l'on modifie le plan — c'est exactement le défaut que D-041 a fait supprimer de C3. | majeur | `calc/tests/test_ferraillage.py` l. 68-73, 83-86, 139-141, 196-199, 215-217. D-041, dernière ligne : « le test qui épinglait la conclusion narrative […] est remplacé par le test de la **règle** ». | Remplacer chaque épinglage par le test d'une propriété vérifiable autrement : couverture d'une nappe, somme des longueurs de cadres = longueur de poutre, 2 barres de 12 m ne peuvent pas faire 25 m. Les « canaris » doivent rejouer le calcul avec l'erreur et vérifier que le nombre **publié** change, pas constater qu'un terme positif est positif (l. 75-78). |
| **M-16 · Les grandeurs de commande sont publiées sans leurs bornes, alors que toutes leurs hypothèses ont une fourchette (D-036, étendu aux coûts et quantités)** — 8 408,4 kg et 1 440 cales sortent de chutes [3 ; 10] %, ligatures [0,5 ; 2] % et cales [2 ; 6]/m². Bornes réelles : commande 8 206 à 8 896 kg (+3,5 % à +12,2 %, contre « +6,1 % » publié) ; cales **720 à 2 160**. Le lecteur passe une commande sur le nombre du milieu. | majeur | `ferraillage.json` → `commande.{acier_commande_kg, ecart_commande_plan_pct, cales_d_enrobage_u}`, aucune clé de bornes. `data.armatures.du_plan_a_la_commande.{chutes_pct, ligatures_pct, cales_par_m2}.fourchette`. D-036 et son impact : « le même traitement est attendu de D1 sur les coûts ». | Publier `commande_aux_bornes` et `cales_aux_bornes`, comme `variante_aux_bornes` le fait dans `planification.py`, et les afficher dans la cascade et la fiche mémo. |
| **M-17 · Exercice 1 : « 4,2 % de moins » est faux (4,0 %), et le sera deux fois plus après correction de B-1** — oublier le recouvrement donne 554,9 kg contre 578,0, soit −4,0 %. Le 4,2 % est 1/24, c'est-à-dire l'écart rapporté à la longueur droite au lieu de la longueur façonnée. Avec les 2 recouvrements réels, l'écart devient −7,7 %. | majeur | Module, corrigé de l'exercice 1 : « soit **4,2 %** de moins ». Recalcul § 0.6 (point 8). | En faire une variable issue de `calc/`, pas un nombre tapé. |

### Mineurs

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **m-1 · Une vingtaine de nombres techniques sont tapés à la main dans le contenu**, contre le § 4.3 (« aucun nombre technique n'est tapé à la main dans un module ») : « 14 % », « 0,888 / 2,466 / 3,853 », « 0,5 g/m », « 3 % », « une trentaine de kilogrammes », « 4,2 % », « 95 kg/m³ », « 2 000 kg », « 76 », « 80 », « 5,60 », et les sept masses linéiques de la fiche mémo. | mineur | `grep` sur `content/06-…md` hors `{{…}}`, `$…$` et `⟦…⟧`. Plusieurs d'entre eux portent d'ailleurs les erreurs B-9 et M-17. | Les faire sortir de `calc/` ; le build échoue déjà sur une variable absente, il ne voit pas un nombre écrit en clair. Un contrôle `check.mjs` « chiffre technique hors variable » serait le bon garde-fou. |
| **m-2 · Figure 1 : la cote « h = 75 cm » touche le cadre de la figure** — texte `x=239,2`, ancre `start`, 9 caractères monospace à 10,5 → fin ≈ 296 sur une `viewBox` de largeur 300. Visible sur la capture. | mineur | SVG figure 1 ; `…figure1.png`. | Élargir la `viewBox` ou ancrer la cote à l'intérieur. |
| **m-3 · Figure 3 : formats décimaux incohérents** — « 578 » à côté de « 426,2 », « 254,1 », « 195,7 ». | mineur | `…figure3.png`. | Un format unique dans `svgkit`. |
| **m-4 · Figure 3 : « les cadres pèsent 254 kg — plus que n'importe quel repère de chapeau »** est faux hors des poutres : D3, « chapeaux sur poutres », pèse 1 392 kg. | mineur | `ferraillage.json` → `nappes.lignes[2].masse_kg`. | Préciser « de la poutre ». |
| **m-5 · Figure 4 : aucune graduation d'axe.** Le § 8 demande cotes et échelle indicative ; seule l'unité est donnée. Les deux valeurs sont lisibles en bout de barre, mais la largeur de la bande n'est pas quantifiable à l'œil. | mineur | SVG figure 4 : aucun `line` de tick, aucun label de valeur d'axe. | Deux graduations suffisent (0 et la borne haute). |
| **m-6 · Figure 5 : l'échelle part de 0, et tout le sujet de la figure tient dans 6 % de sa hauteur.** Les segments « chutes » et « ligatures » sont des traits. | mineur | `…figure5.png`. | Axe tronqué avec rupture déclarée, ou cascade en valeurs relatives. |
| **m-7 · Figure 2 : « à l'échelle, une poutre de 0,75 m sur 24 m ferait quelques pixels de haut »** — à l'échelle horizontale du dessin (≈ 34,6 px/m), elle ferait 26 px. L'exagération verticale réelle est de ×6,5 et n'est pas chiffrée. | mineur | Mesures sur `…figure2.png` et le SVG. | Chiffrer l'exagération (« ×6,5 ») plutôt que de l'imager. |
| **m-8 · S4g ne dit rien du stockage et de la manutention des cages avant pose** — une cage de poutre de ce plan pèse 742 kg et fait 24,00 m ; le risque de renversement en attente de levage n'est pas cité, alors que le stockage des fagots l'est. | mineur | `ferraillage.json` n'a pas de rubrique sécurité ; tableau S4g du module, 5 lignes. | Une ligne de plus dans le tableau. |
| **m-9 · Les cinq figures ont un `<desc>` identique à leur `<title>`** — le texte alternatif n'apporte rien à un lecteur d'écran (§ 4.4). | mineur | SVG : `<title id="t-…">Coupe transversale…</title><desc>Coupe transversale…</desc>`. | Décrire ce que la figure montre, pas la renommer. |

---

## 3. Grille d'auto-évaluation § 7.2

| Critère | Note | Justification |
|---|---:|---|
| Le « pourquoi » est expliqué | **3** | S2 est la meilleure page du module : la distinction « ce ferraillage est-il suffisant ? » / « ce qui est posé est-il ce que le plan montre ? », et l'argument de l'irréversibilité (« vous êtes le seul témoin d'un événement irréversible »), sont justes, tenus et utiles. S3a et S4f en découlent sans rupture. |
| Les hypothèses sont explicites | **1** | Les V3 portent fourchette, année et note, et les ⏸ sont tenus. Mais l'hypothèse la plus porteuse du module — **la base du ratio kg/m³** — n'est déclarée nulle part et fait basculer le verdict (B-5) ; les zones de cadres n'ont pas de bornes (M-8) ; la surface des chapeaux D3 est saisie sans dérivation (M-14) ; trois simplifications ne sont pas signalées (M-7, M-9, M-12). |
| Les formules sont justifiées | **1** | Trois des quatre formules publiées sont fausses ou mal domaine-définies : `n_rec = ⌈L/L_c⌉ − 1` (B-1, affirmée comme une évidence géométrique), `floor(L/s)+1` appliquée à des longueurs cumulées (B-3), `largeur = surface / longueur de barre` (B-2). Seule `m = π/4·d²·ρ` est juste et justifiée. |
| L'exemple est vérifié | **1** | Les tests sont verts et ne vérifient presque rien : ils retapent la formule de production (M-15), l'étalonnage n'appelle pas la bibliothèque sur ses cas décisifs (M-3) et valide une arithmétique fausse (M-4), et le contre-calcul du § 3.3 est circulaire (B-4). Ma contre-expertise trouve 209 kg d'écart (−2,6 %) sur la grandeur centrale du module. |
| Le piège est identifié | **2** | La rubrique S5 est riche et bien visée (métré sur la cote du dessin, attachement sur bon de livraison, ratio gardé au bordereau après visa). Mais le piège vedette du module — le comptage des cadres — est lui-même faux (B-3), et un autre repose sur un effet que les chiffres ne montrent pas (B-10). |
| Le lien avec l'exécution est fait | **3** | S4f (contrôles avec leur référence et le statut de leur règle), la double lecture entreprise / MOE, S4g, l'exercice 3 et la check-list forment la meilleure partie du module ; c'est exactement le métier du lecteur. Réserve de forme : M-5 et M-6 (cohérence avec C3). |
| Le lien avec le coût et le délai est fait | **2** | La chaîne plan → commande → payé → attachement → BAC de la valeur acquise est bien articulée, et le refus délibéré de rebasculer le bordereau est honnête et déclaré. Mais les nombres de la chaîne sont faux (B-1, B-2, M-1) et publiés sans bornes (M-16). |

**Trois critères sur sept sont sous le minimum de 2** exigé avant livraison. Le module ne passe
pas la grille du § 7.2 en l'état.

---

## 4. Verdict

Module solide sur ce qu'il voulait être — la pédagogie du rôle, des contrôles et du rapport au
plan visé est juste et souvent excellente — mais **le métré qui en est le cœur est faux de
−2,6 % par trois erreurs de calcul indépendantes, sa seconde voie est circulaire, et trois de
ses cinq figures ne montrent pas ce que leur légende annonce** : à corriger avant livraison.

**36 défauts : 11 bloquants · 17 majeurs · 8 mineurs.** Aucun n'était détecté par les tests
automatiques, tous verts.

---

## Suite donnée (26/10/2026, par l'auteur)

**Les 11 bloquants sont corrigés.** Trois ont été re-vérifiés indépendamment avant correction
(recouvrements, nappe D1, acier d'appui) : le relecteur avait raison sur les trois.

| # | Correction | Contrôle ajouté |
|---|---|---|
| B-1 | `nb_recouvrements(L, Lc, Lr) = ⌈(L − Lr)/(Lc − Lr)⌉ − 1`, fonction dédiée et documentée. A1 passe de 1 à **2 recouvrements**, 25,00 → 26,00 m, 578 → **601 kg**. | Test géométrique : k barres couvrent bien L, et k−1 **ne suffisent pas** ; canari qui rejoue `⌈L/Lc⌉−1` et vérifie qu'il sous-compte |
| B-2 | `largeur = surface / PORTÉE`, et chaque nappe déclare `portee_armee_m` et son débord d'ancrage. D1 passe de 365 à **384 barres**. | Test : les barres couvrent toute la largeur à armer ; canari qui divise par la longueur de barre et montre la bande nue |
| B-2b | **Trouvé par le canari du B-2** : les chapeaux D3 avaient hérité d'une portée de 7,5 m alors qu'ils franchissent une bande de 3,0 m. Dalle 6 818 → **7 708 kg**. | le même canari |
| B-3 | Les cadres se comptent **par segment continu**, déclarés dans `data` (4 + 3 segments). 334 → **342 cadres**. | Trois tests : comptage par segment, canari `l/s`, canari « totaliser la zone avant d'ajouter 1 » ; et les segments doivent couvrir la poutre sans trou |
| B-4 | La section « deux voies » devient **« contrôle d'ordre de grandeur »** et le module écrit que ce n'en est pas une : le plan ayant été calibré sur ces ratios, la comparaison vérifie le calibrage. Ce qui garantit le métré est nommé — étalonnage externe, vérification dimensionnelle, et une **seconde traversée depuis le dessin** (écart 0,005 %). | Le test « le plan reste dans la fourchette » est **supprimé** (épinglage de conclusion, défaut C3-M1) et remplacé par le test de la règle ; nouveau test sur la seconde traversée |
| B-5 | Chaque ratio porte sa **base** dans `ratios_V3` et dans le tableau du module : 180 kg/m³ est rapporté à la **retombée sous dalle**, pas à la section pleine. | Test : tout ratio publié a une base d'au moins 30 caractères |
| B-6 | La figure 1 est retitrée « **les barres filantes** » et dit ce qu'elle ne montre pas : à mi-travée le lit inférieur en porte trois de plus, sur appui le lit supérieur cinq de plus. Un plan réel dessine plusieurs coupes — c'est devenu la leçon. | la coupe est dérivée du plan (test déjà en place) |
| B-7 | L'entrée 2 de la légende couvre les deux lits. | — |
| B-8 | Le test ne code plus `+0,6` en dur : il compare **droit dessiné + retours déclarés = développé chiffré**, les retours venant des données. | le test lui-même |
| B-9 | « Une trentaine de kilogrammes » était faux : 3 % de la masse des **cadres** font **7,8 kg**, soit 0,08 % du métré. Et « l'écart mesuré » devient « ordre de grandeur V3, non mesuré » — le cours ne peut pas mesurer ce qu'il n'a pas le droit de citer. | la valeur est calculée et publiée, plus écrite |
| B-10 | La ligne de S5 est chiffrée sur les écarts publiés, et deux lignes sont ajoutées (ratio sans base, comparaison circulaire). | — |
| B-11 | **Le plan contredisait la forme du moment qu'il prétend illustrer** : 13,4 cm² sur appui contre 24,2 en travée, quand la RDM d'une poutre continue à trois travées égales demande ~1,25 fois plus sur appui. B2 passe à 5 HA25 : **28,6 cm², rapport 1,18**. | Test : l'acier d'appui dépasse celui de travée, et le rapport reste entre 1,0 et 1,6 |

**Également corrigés** : D-036 (la commande et les cales portent leur fourchette — 9 778 à 10 599 kg,
720 à 2 160 cales), les nombres écrits à la main de l'exercice 1, du quiz 2, du quiz 3 et de la
fiche mémo.

**Ce que cette passe a prouvé.** Les onze bloquants sont de trois familles, et deux étaient déjà
connues : une figure ou un texte écrit à côté de ses données (B-6 à B-10), un test qui épingle une
conclusion au lieu de contrôler une règle (B-4). La troisième est nouvelle et plus grave : **B-1,
B-2 et B-11 sont des erreurs de MODÈLE PHYSIQUE** — une formule de recouvrement qui ne couvre pas
l'ouvrage, une nappe qui laisse 18 m² de dalle nue, un plan qui met l'acier du mauvais côté. Aucune
n'aurait été vue par un contrôle de cohérence : il fallait refaire la géométrie. Et la correction de
B-2 a fait sonner son propre canari sur une quatrième erreur (B-2b) que personne n'avait vue.

