# Passe adversariale n° 3 — module `TV` (tranche verticale de suivi)

**Relecteur hostile, indépendant de l'auteur.** Troisième passe, après une première qui avait relevé
19 défauts (4 bloquants) et une seconde 25 de plus (3 bloquants, 12 majeurs, 10 mineurs), tous
déclarés corrigés.
Date : 19/10/2026 · commit relu : `b22684a` · empreinte `data/` : `d50cd3e4e18c`.

**Méthode.** Je n'ai lu `QA/TV-tranche-verticale-passe2.md`, la section « Passe adversariale » de
`STATE.md` et `DECISIONS.md` D-019 à D-022 qu'**à la fin**, une fois mes constats écrits. J'ai
recalculé **onze grandeurs** depuis `data/projet-gare.json` seul, par mes propres scripts, avant
d'ouvrir `calc/` (scripts dans mon bac à sable : `indep/mine.py`, `indep/histo.py`,
`indep/prorata.py`, `indep/cpm_fuzz.py`). J'ai rejoué T2 et T6, inventé **six** canaris neufs, fuzzé
le moteur CPM sur 40 000 réseaux, regardé les cinq captures et mesuré les SVG rendus. `npm run check`
et `python3 calc/run_all.py` ont été exécutés.

---

## 1. Contre-expertise à l'aveugle — recalculs depuis `data/` seul

| # | Grandeur | Mon recalcul indépendant | Publié | |
|---|---|---:|---:|---|
| 1 | Béton d'une zone : 360 × 0,25 + 2 × 24,0 × 0,35 × 0,50 | **98,40 m³** | 98,4 | ✓ |
| 2 | Coffrage : (360 − 16,8) + 48,0 + 16,8, +4 % | **424,32 m²** | 424,3 | ✓ |
| 3 | Acier : 80 × 90,0 + 180 × 8,40 | **8 712 kg** (88,5 kg/m³) | 8 712 / 88,5 | ✓ |
| 4 | Durées : 424,32/(30×8) · 1512/(150×4) · 7200/(300×8) · 98,4/30/8 | **1,768 · 2,520 · 3,000 · 0,410 j** | 1,77 · 2,52 · 3,00 · 0,41 | ✓ |
| 5 | **Cycle** — lecture *littérale* de `data` (« part faite **avant** le démarrage ») | **8,048 j** | 8,557 | ✗ **voir M3** |
| | **Cycle** — lecture « recouvrement » (celle du code) | **8,552 j** | 8,557 | ✓ |
| 6 | **Cadence** — max(équipes dédiées) | **3,000 j** | — | **voir M2** |
| | **Cadence** — max(dédiées) + bétonnage | **3,410 j** | 3,41 | ✓ |
| 7 | Coût d'une zone : 98,4×1250 + 8712×17 + 424,32×180 | **347 478 MAD** ; BAC **2 779 824** | 347 478 / 2 779 824 | ✓ |
| 8 | PV(j 19) par le réseau, avancement fractionnaire zone par zone | **4,855 zones** ; SPI **0,7415** ; retard **1,255 z.** | 4,86 / 0,741 / −1,26 | ✓ |
| 9 | CPI = 3,6 × 347 478 / 1 330 000 | **0,9405** | 0,941 | ✓ |
| 10 | **Histogramme** reconstruit depuis `data/` + réseau, jour par jour | **identique aux 34 valeurs publiées** ; pointe **24** | 24 | ✓ |
| | Vrai maximum par **balayage de tous les fronts** (et non aux instants entiers) | **24, à t = 25,06 j** | 24 | ✓ |
| 11 | Part de main-d'œuvre directe : 401,7 h × 45 / 347 478 | **5,21 %** (5,31 % si l'on compte le décoffrage) | 5,2 % | ✓ |
| 12 | Écart coté figure 5 : SV/BAC = −437 822 / 2 779 824 | **−15,75 pt** | 15,8 pts | ✓ |

**L'arithmétique est juste de bout en bout.** Les trois écarts de la colonne de droite ne sont pas
des erreurs de calcul : ce sont des écarts de **modèle** (M2, M3). C'est exactement le genre que la
passe 2 avait identifié, et que les contrôles ne regardent toujours pas.

---

## 2. Canaris

### 2.1 Les deux canaris exigés

| Canari | Résultat |
|---|---|
| **T2** — `ferr_dalle` divisé par `ferrailleurs_poutres` | **SONNE** — 6 échecs : « durée recalculée : ferraillage_dalle_j — 6,0 contre 3,0 », « ferraillage_dalle_j dépend bien de *ferrailleurs_dalle* », « doubler *ferrailleurs_poutres* ne touche pas les autres durées », « renforcer la seule équipe de dalle fait passer la borne aux POUTRES », « renforcer les DEUX équipes passe sous la cible — 39,9 j », « SPI — 1,417 ». La correction tient. |
| **T6 à 190 m²/j** (borne basse déclarée) | **SONNE** — écart 26,32 %, 2 échecs. |
| **T6 à 280 m²/j** (borne haute déclarée) | **SONNE** — écart 14,29 %, 2 échecs. |

### 2.2 Six canaris de mon invention

| # | Mutation | 15 contrôles | Ce que le module publie alors |
|---|---|---|---|
| **N1** | `recouvrement_ferraillage_poutres_dalle_pct` = **120** (fourchette déclarée [20 ; 60]) | **TOUS VERTS** | cycle **7,93 j** au lieu de 8,56 ; plancher 31,7 j au lieu de 32,4. → **M4** |
| **N2** | `etais_de_reprise_maintenus_j` = **0** | **TOUS VERTS** | « il faut **2 700 étais** là où un décompte sur les seules zones coffrées en annoncerait **2 700**. **Un facteur deux** sur un poste de location ». → **M6** |
| **N3b** | `effectif_par_tache` permuté COF ↔ FEP | **TOUS VERTS** | histogramme publié modifié sur **19 jours sur 34** (j0 : 10 → 6 ; j2 : 6 → 10 ; j6 : 19 → 23…), pointe inchangée à 24. → **M13** |
| **N4** | `longueur_zone_m` 15 → 20 m | **SONNE** (5 échecs) | — |
| **N5** | `decoffrage_j` = **1,0** (haut de sa fourchette) + équipes de ferraillage à 40 | sonne, **mais jamais sur le défaut visé** | cadence publiée **1,01 j/zone** pour un décoffrage de **1,0 j** tenu par **2 compagnons** : rotation infaisable, non détectée. → **M1** |
| **N6** | `etais_de_reprise_maintenus_j` = **28** (**haut de sa propre fourchette déclarée [7 ; 28]**) | **TOUS VERTS** | « Le nombre de zones étayées vaut ⌈(cycle + maintien)/cadence⌉ = **11 zones** » — sur un plancher qui n'en compte que **8** — « il faut **9 900 étais** » ; et la balise affiche toujours « restent en place **14 jours** ». → **M5, M7** |
| **N7** | `EAC = BAC / CPI` → `BAC × CPI` dans `valeur_acquise.py` | sonne (identité `EAC × CPI = BAC`) | mais l'**étalonnage « cas à solution posée d'avance »** imprime `ok EAC du cas fermé — 1200,0000 contre 1200,0000` pendant que le module publie un EAC faux. |
| **N8** | `VA_A` minorée de **20 %** — *le canari que le commentaire de l'étalonnage dit viser* | sonne par ailleurs | les **6 lignes** du « cas fermé » impriment **ok**. L'étalonnage n'appelle jamais la bibliothèque. → **M11** |

**Quatre canaris sur six passent les quinze contrôles sans en faire bouger un seul** (N1, N2, N3b,
N6). Trois d'entre eux sont des valeurs **à l'intérieur ou au bord des fourchettes que `data/`
déclare lui-même**.

### 2.3 Fuzz du moteur CPM — **RAS, avec preuve**

Le bornage du parcours arrière à la fin de projet (`fin = min([tard[s][0] − dec …] + [duree])`) est
le point que la consigne me demandait d'attaquer. J'ai engendré **40 000 réseaux** de 2 à 5 tâches,
durées 0 à 10, décalages dans {0 ; −d ; −d/2 ; −1,5 d ; −2 ; +1}, et j'ai confronté chaque marge
annoncée à sa **définition** (retard maximal du début d'une tâche qui ne change pas la durée du
projet), recalculée par un parcours avant indépendant :

```
reseaux testes 40000 ; marges fausses : 0 ; levees a tort : 0
```

Aucune marge fausse, aucune levée abusive des deux invariants. **M9 de la passe 2 est corrigé, et il
tient.** C'est le seul point de cette passe où je n'ai rien trouvé.

---

## 3. Les 10 points du § 12.2

### 3.1 Tableau des défauts

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **B1 · L'avancement d'une zone est un prorata uniforme de tous les postes — un modèle que le cycle du module contredit. Tout le § S6, la figure 5, le mémo et l'exercice 4 reposent dessus.** | **bloquant** | `data/suivi.avancement_zone_en_cours_pct = 60` est appliqué tel quel à chaque poste (`cycle_plancher.py`, bloc `situation`, et `valeur_acquise` via `avancement_zones = 3 + 0,60`). Le **réseau du même module** dit qu'à 60 % du cycle (t = 5,13 j) : coffrage **terminé** (fin à 1,77 j), ferraillage des poutres **terminé** (3,41 j), dalle à 91 %, et **bétonnage pas commencé** (BET démarre à **5,65 j**). État physique : **424,3 m²** de coffrage, **8 074 kg** d'acier, **0,0 m³** de béton. Le module publie : 254,6 m² · 5 227 kg · **59,0 m³**. Conséquence sur les relevés : le relevé physiquement cohérent à la date d'arrêt vaut **295,2 m³** de béton et **1 697 m²** de coffrage, contre 352,0 et 1 515 publiés. Le « contrôle qui fait foi » (recoupement géométrique à 1 %) annonce alors **−0,63 %** et **−0,82 %** (« l'avancement déclaré tient ») ; appliqué au relevé cohérent, le même contrôle donnerait **−16,7 %** sur le béton et **+11,1 %** sur le coffrage, c'est-à-dire **SIGNAL** sur un chantier en ordre. Les relevés publiés échappent au contrôle parce que `data/suivi.quantites_relevees.base_du_choix` les a fabriqués **sur le même prorata** : voie A et voie B partagent leur entrée décisive — le piège que le module dénonce lui-même deux paragraphes plus bas. Enfin l'**exercice 4** déclare la ligne « coffrage 254,6 m² » **« Correct, et c'est le piège … Rien à redire »**, alors que la bonne réponse de contrôle est que la ligne est minorée de 170 m² et que la ligne béton facture **59 m³ qui n'existent pas**. | Déclarer explicitement le modèle d'avancement. Soit (a) l'avancement d'une zone est **pondéré par les postes** (coffrage 22,0 %, acier 42,6 %, béton 35,4 % du coût de zone) et les quantités de la situation, les relevés et le tableau S6 en découlent — à 60 % de valeur : coffrage 100 %, acier ≈ 89 %, béton 0 % ; soit (b) le prorata uniforme est conservé comme **simplification déclarée** (R6), signalée dans `STATE.md` et dans le module, et l'exercice 4 en fait sa **quatrième erreur plantée**. Dans les deux cas, recalculer `quantites_relevees` depuis le réseau plutôt que de les poser, et ajouter un test qui confronte les quantités d'une situation à l'état du réseau à la même fraction de cycle. |
| **B2 · Figure 2 : les phases d'une zone sont peintes l'une sur l'autre ; les durées qu'on y lit sont fausses et contredisent le tableau S4a et la figure 3 du même module — sous une légende qui affirme l'inverse.** | **bloquant** | `svgkit.js:rotation` dessine les sept `<rect>` dans l'ordre COF, FEP, FED, … à opacité pleine. Mesure faite sur le SVG rendu de `modules/01-tranche-verticale-suivi.html` (échelle 19,28 px/j, zone Z1) : <br>`COF  réelle 1,77 j → VISIBLE 0,89 j` <br>`FEP  réelle 2,52 j → VISIBLE 1,51 j` <br>Le lecteur qui mesure la barre lit **0,89 j** de coffrage et **1,51 j** de ferraillage de poutres, contre **1,77** et **2,52** au tableau S4a et sur la figure 3. Et la légende dit : « Les phases d'une même zone **SE RECOUVRENT** : c'est ce recouvrement qui fait le cycle » — or la peinture **efface** exactement les parties recouvertes, et la barre se lit comme une file indienne. La figure est donc l'inverse de ce qu'elle annonce. Aucun contrôle ne voit cela : la dette 11 ne couvre que « texte contre trait », pas « rect contre rect ». | Dessiner chaque phase sur sa **propre sous-ligne** (sept bandes fines décalées en *y* à l'intérieur de la ligne de zone), ou peindre les phases avec un contour et une opacité partielle, ou les ordonner de la plus longue à la plus courte avec un hachurage pour les zones communes. Ajouter un contrôle : pour chaque rect de phase, la largeur **visible** après occlusion doit valoir sa durée. |
| **M1 · La règle de cadence exclut le décoffrage sur une justification que `data/` contredit, et le test épingle le défaut au lieu de le chercher.** | majeur | `cycle_plancher.py:cadence_rotation` : `dediees` est un **dictionnaire en dur de trois clés**. La règle publiée (§ S4d et `regle_cadence.regle`) dit : « la cure et le décoffrage ne comptent pas, **ils n'occupent aucune équipe** ». Or `data/cycle_zone/effectif_par_tache.DEC = 2`, avec la note « *le décoffrage mobilise deux compagnons* », et la **figure 4 les compte** (jours 15, 22, 32). La règle affirme donc le contraire de la donnée, dans le même module. Canari **N5** : avec `decoffrage_j = 1,0` (haut de sa fourchette déclarée) et des équipes de ferraillage renforcées, la cadence publiée tombe à **1,01 j/zone** pour un décoffrage de **1,0 j** tenu par 2 compagnons — rotation à 99 % d'occupation, publiée sans alerte ; les échecs observés portent sur d'autres contrôles. Enfin le test `calc/tests/test_plancher.py:203` écrit `verifie("la regle de cadence couvre les trois equipes dediees", len(_dur_ded) == 3)` : il **échouerait si l'auteur corrigeait**. C'est le bloquant B1 de la passe 2 répété un cran plus bas — une liste blanche au lieu d'une dérivation. | Dériver `dediees` de `data/cycle_zone/effectif_par_tache` : toute tâche d'effectif non nul mobilise une équipe. Remplacer le test par « l'ensemble des tâches dédiées est exactement celui des tâches d'effectif > 0 », et ajouter un test de **faisabilité** : pour chaque tâche dédiée, `durée ≤ cadence`. |
| **M2 · « Le bétonnage s'ajoute parce qu'il immobilise la zone entière » : l'argument ne tient pas, et il allonge de 9,5 % la durée que l'exercice 3 fait défendre en réunion.** | majeur | Qu'une zone soit immobilisée pendant son bétonnage borne **son propre cycle** (c'est déjà dans les 8,56 j), pas le rythme auquel la zone **suivante** démarre. Sous le modèle de ressources que la règle énonce elle-même — « une équipe ne peut être que sur une zone à la fois » — la cadence minimale est `max(1,77 ; 2,52 ; 3,00) = 3,00 j`, et elle est faisable : j'ai vérifié que chaque équipe reste sous 100 % d'occupation à 3,00 j. Le `+ bétonnage` ajoute 0,41 j, soit une durée de plancher de **32,4 j** au lieu de **29,6 j** — **9,5 %**. Le second argument invoqué (« la pompe et la grue pour tout le monde ») est incohérent avec le reste du modèle : la **même grue unique** sert le coffrage et le ferraillage de zones qui se recouvrent sans que cela borne quoi que ce soit. Le test `cadence = max(équipes dédiées) + bétonnage, recalculé à la main` ré-implémente la formule depuis le même dictionnaire publié : il contrôle l'arithmétique, pas le modèle. | Choisir et défendre **un** modèle de ressources. Soit la cadence est `max(tâches à équipe dédiée)` et le bétonnage n'y entre pas ; soit la grue et la pompe sont modélisées comme des ressources partagées **sur toutes les tâches**, et la cadence sort d'un calcul d'occupation, pas d'une formule. Dans les deux cas publier le taux d'occupation de chaque équipe à la cadence retenue : c'est la preuve que le planning est tenable. |
| **M3 · Sept hypothèses V3 publiées sans balise et sans ligne de registre — dont les cinq que `data/` désigne lui-même comme pesant « 32 % du cycle et la totalité du gain de recouvrement ».** | majeur | Le contrôle ajouté par D-021 imprime « 8 lue(s) sur 19 déclarée(s) ». Les 11 autres ne sont **jamais confrontées au registre**, parce que le filtre est `contenu.includes("gare." + chemin)` : une V3 qui atteint le module **par `calc/`** et non par `{{gare.…}}` est invisible. Énumération faite depuis `data/` : `cycle_zone.cure_avant_decoffrage_j` (2 j), `cycle_zone.decoffrage_j` (0,5 j), `cycle_zone.point_arret_visa_ferraillage_j` (0,25 j), `cycle_zone.recouvrement_coffrage_ferraillage_poutres_pct` (50 %), `cycle_zone.recouvrement_ferraillage_poutres_dalle_pct` (40 %), `cadences.rendement_equipe_coffrage_m2_j` (232, fourchette [190 ; 280] **publiée dans le module**), `ratios_V3.coffrage_rives_pct` (4 %, **publié : « plus 4 % de rives »**) — **aucune** n'a de balise `⟦V3…⟧` ni de ligne dans `registre-hypotheses.csv` (18 lignes, H006–H018 pour TV). Le `_role` de `data/cycle_zone` écrit pourtant noir sur blanc : « *ils doivent donc être déclarés, bornés et **registrés** comme le reste* ». Bornés : oui. Registrés : non. M1 de la passe 2 n'est donc corrigé qu'**à moitié**, et le contrôle écrit pour le garantir ne le voit pas. | Étendre le contrôle : toute feuille `{valeur, fourchette}` de `data/` **atteinte par une bibliothèque de `calc/`** (instrumenter les lectures, ou simplement exiger une ligne de registre pour **toutes** les feuilles V3 du fichier) doit avoir sa ligne. Puis baliser les sept. Et faire les balises **lire** leur valeur (`⟦V3|…|{{gare.cycle_zone.cure_avant_decoffrage_j.valeur}} j|…⟧`), ce que `build.mjs` sait déjà faire. |
| **M4 · Aucun contrôle ne confronte une V3 à sa propre fourchette.** | majeur | Canari **N1** : `recouvrement_ferraillage_poutres_dalle_pct = 120`, alors que la fourchette déclarée dans le même objet est `[20, 60]` et qu'un taux de recouvrement > 100 % n'a pas de sens physique. **Les quinze contrôles restent verts** et le module publie un cycle de 7,93 j. De même aucun contrôle ne vérifie qu'un pourcentage est dans [0 ; 100], ni qu'un effectif est entier positif. | Contrôle de build, cinq lignes : pour toute feuille `{valeur, fourchette}` de `data/`, exiger `fourchette[0] ≤ valeur ≤ fourchette[1]` et `fourchette[0] < fourchette[1]`. C'est le contrôle le moins cher du dépôt et il attrape N1 et plusieurs canaris de la passe 2. |
| **M5 · L'inventaire d'étais compte les étais de reprise à la densité de l'étaiement complet, et la formule n'est pas bornée par le nombre de zones.** | majeur | `coherence_materiel` : `etais_zone = surface × etais_par_m2` avec **la même densité 2,5/m²** pour les zones en cours de coffrage et pour les zones décoffrées qui ne portent plus que des **étais de reprise** — or une reprise est par définition une grille **réduite** ; c'est le principe même que le module enseigne (« ses étais de reprise restent en place »). Le poste est donc surestimé d'un facteur de l'ordre de 3 sur les 4 zones concernées. Second défaut : `zones_etayees = max(1, ceil((cycle + maintien)/cadence))` n'est pas plafonné à `nb_zones`. Canari **N6** (`maintien = 28 j`, **le haut de sa propre fourchette déclarée**) : le module publie « **11 zones** étayées » sur un plancher qui en compte **8**, et « **9 900 étais** » (le maximum physique est 7 200), **quinze contrôles verts**. | Déclarer dans `data/` **deux** densités — `etais_etaiement_par_m2` et `etais_de_reprise_par_m2` — avec leurs fourchettes, et sommer `zones_coffrées × d₁ + (zones_étayées − zones_coffrées) × d₂`. Plafonner `zones_etayees` à `nb_zones` et **lever** si le plafond mord : un maintien qui dépasse la durée du plancher est une information, pas un arrondi. |
| **M6 · « Un facteur deux sur un poste de location » : un rapport écrit à la main, faux aujourd'hui et contredit par les données sous deux variations.** | majeur | `content/01-…md:314`. Le rapport calculé vaut **2,33** aujourd'hui (6 300 / 2 700), **3,67** sous N6, et **1,00** sous N2 — où le module écrit alors « il faut **2 700** étais là où un décompte sur les seules zones coffrées en annoncerait **2 700**. **Un facteur deux** ». C'est un nombre technique tapé dans la prose, ce que le § 4.3 interdit (« aucun nombre technique n'est tapé à la main dans un module »). Même défaut que le M3 de la passe 2 (« quarante fois », « vingt fois »), rouvert. | `{{tranche-plancher.coherence_materiel.rapport_etais::n1}}`, calculé dans `coherence_materiel`. |
| **M7 · La balise `⟦V3\|maintien des étais…\|14 jours\|…⟧` recopie sa valeur à la main : sous N6 le module affiche « 14 jours » et calcule avec 28.** | majeur | Rendu de N6 : « *ses étais de reprise restent en place **14 jours** V3 … il faut **9 900 étais*** ». Le build sait substituer dans les balises (`build.mjs` : « *sur les champs des balises de preuve AVANT extraction, pour qu'une balise V3 puisse lire sa valeur dans `data/` au lieu de la recopier à la main (§ 3.2, R1)* ») — la capacité existe et n'est pas employée ici. Le contrôle de D-021 ne peut pas voir la dérive, puisque ce chemin n'est pas « lu » au sens du filtre (**M3**). | Faire lire toutes les balises V3 dans `data/`, et ajouter au contrôle de registre la comparaison **valeur de la balise ↔ valeur de `data/`**, pas seulement l'existence d'une ligne. |
| **M8 · L'histogramme d'effectifs est un échantillonnage aux instants entiers : 6 bétonnages sur 8 et 5 décoffrages sur 8 n'y apparaissent jamais, et le test qui le valide est tautologique.** | majeur | `histogramme_plancher` teste `debut ≤ k < fin` pour `k` **entier**. Les tâches plus courtes qu'un jour tombent entre deux entiers : bétonnages des zones 1, 2, 3, 5, 7, 8 (5 compagnons chacun) et décoffrages des zones 1, 2, 4, 6, 7 (2 compagnons) **ne sont comptés aucun jour**. Au **jour 19 — la date d'arrêt du module** — la figure 4 annonce **6 présents** sur un plancher où le § S4d dit que trois zones sont ouvertes. La somme des barres (479 j·homme) dépasse de 2,8 % le total réel. Le test `verifie("la pointe publiée est bien le maximum de l'histogramme", pointe == max(_h.values()))` compare `pointe_effectif`, qui **est** `max(histogramme_plancher(…))`, à `max` du même tableau : il ne peut pas échouer. Je confirme par ailleurs que la pointe **24** est juste (balayage de tous les fronts : 24 à t = 25,06 j, COF 8 + FEP 4 + FED 8 + DEC 2 + encadrement 2) — la correction B2 de la passe 2 tient sur ce point précis. Canari **M13** ci-dessous. | Intégrer l'effectif sur chaque **journée** (moyenne pondérée par le temps passé) au lieu d'échantillonner à l'instant `k`, ou échantillonner au pas de 0,05 j et agréger. Remplacer le test par une construction indépendante : l'aire de l'histogramme doit égaler Σ(durée × effectif) sur les 8 zones, à l'arrondi près. |
| **M9 · `build.mjs` transforme en virgules les points de **toute** chaîne substituée : la phrase de lecture du § S6 est publiée avec sa ponctuation détruite, et sans accents.** | majeur | `build/build.mjs:71` : `return grouper(String(v).replace(/\./g, ","));`, appliqué sans distinguer un nombre d'une chaîne. `{{valeur-acquise.lecture}}` est la seule variable-chaîne du module, et elle est publiée **juste sous le tableau S6** : <br>« *CPI = 0,941 : chaque dirham **depense** produit 0,94 dirham de valeur**,** SPI = 0,741 : l'avancement vaut 74% de ce qui **etait planifie** a cette date**,*** » <br>Deux points de phrase devenus virgules, phrase terminée par une virgule, et trois mots non accentués — dans un dépôt qui porte un commit « *Français accentué dans tout ce que le lecteur voit* ». | N'appliquer la conversion décimale **que** lorsqu'un format `::nX` a été demandé, ou lorsque la valeur résolue est de type `number`. Et accentuer la chaîne `lecture` dans `valeur_acquise.py`, comme les autres textes destinés au lecteur. |
| **M10 · La légende de la figure 5 renvoie à un chiffre que le module ne publie pas.** | majeur | « *L'écart vertical … c'est SV, et il vaut ici **ce que le tableau S6 annonce*** ». Le tableau S6 publie BAC, VP, VA, CR, CPI, SPI, EAC et « Dérive prévue » — **SV n'y figure pas** (`ecart_de_delai_SV_MAD` = −437 822 est calculé et jamais affiché, de même que CV). Le lecteur ne peut pas faire le rapprochement que la légende lui demande. Accessoirement la cote est en **points de pourcentage** (15,8) alors que SV est en MAD : l'identité n'est vraie qu'après division par le BAC, ce que rien ne dit. | Ajouter deux lignes au tableau S6 — « Écart de coût (CV) » et « Écart de délai (SV) » — et coter la figure en MAD, ou écrire « SV / BAC » dans la légende. |
| **M11 · L'étalonnage « cas à solution posée d'avance » de `valeur_acquise.py` n'appelle jamais la bibliothèque : il est vide.** | majeur | `calc/etalonnage/plancher_cas_ferme.py`, bloc « b bis ». `obtenu = {"CPI": VA_f/CR_f, "SPI": VA_f/VP_f, …}` est calculé **à la main dans le fichier d'étalonnage** et comparé à `attendu` écrit à la main : c'est un test de la division de Python. Le commentaire du bloc annonce pourtant sa cible : « *Un canari minorant VA de 20 % les franchissait toutes. Il faut donc un cas dont la réponse est ÉCRITE D'AVANCE, sans la bibliothèque.* » Canari **N8** (VA minorée de 20 % dans `valeur_acquise.py`) : les **six lignes du cas fermé impriment `ok`**. Canari **N7** (EAC inversé) : `ok EAC du cas fermé — 1200,0000 contre 1200,0000` pendant que le module publie 2 614 541 MAD au lieu de 2 955 556. Le § 3.3 est explicite : « *sans étalonnage, ses résultats restent V3 et ne servent pas d'exemple de référence* ». m10 de la passe 2 n'est pas corrigé sur le fond. | Construire un `data/` minimal (10 unités à 100 MAD, 1/jour, jour 6, 5 faites, 600 MAD) et **appeler `valeur_acquise()` dessus**, puis comparer ses sorties aux cinq nombres posés à la main. Vérifier que N7 et N8 le font sonner. |
| **M12 · Figure 1 : le « front prévu » porte une fraction de TEMPS sur un axe de LONGUEUR, et la lecture que la légende promet est impossible.** | majeur | `figures.zones.avancement_prevu[i] = (jour_arrêt − début_Zi)/cycle` — une fraction du **cycle**. `svgkit.js:planZones` la trace à `x₀ + longueur_zone × f`, c'est-à-dire comme une **position dans la zone**. Or une zone à 63 % de son cycle n'est pas « construite sur 63 % de sa longueur » : chaque phase balaie la zone **entière**. Second défaut : la zone en cours (Z4, 60 %) est peinte **en entier** en jaune, sans aucune fraction, et ne reçoit pas de trait bleu (`f ≥ 1` → `continue`). La légende dit « *L'écart entre la couleur et le trait est le retard* » : il n'existe nulle part sur la figure un couple couleur/trait sur la même zone. Capture `…-figure1.png` à l'appui. | Soit remplacer le plan par une **barre d'avancement** par zone (prévu en contour, constaté en plein) sous le plan, soit ne tracer le front que comme une limite **entre zones** (ici : entre Z4 et Z5) et porter les pourcentages en étiquette. Et fractionner la zone en cours selon `avancement_zone_en_cours_pct`. |
| **M13 · Une permutation de `effectif_par_tache` change l'histogramme publié jour par jour sans faire bouger un seul contrôle.** | majeur | Canari **N3b** (COF ↔ FEP) : **15 contrôles verts**, `calc/` vert, build OK ; l'histogramme publié passe de `[10, 14, 6, 14, 18, 22, 19, …]` à `[6, 14, 10, 18, 14, 22, 23, …]` — 19 jours sur 34 modifiés. Le test « au jour du recouvrement, les DEUX équipes sont comptées » additionne `coffreurs + ferrailleurs_poutres` : il est **invariant par permutation**. Rien ne confronte `effectif_par_tache` à autre chose qu'à lui-même. | Tester tâche par tâche : sur un jour où **seule** la tâche X tourne, l'effectif publié doit valoir `effectif_par_tache[X] + encadrement`. Sept assertions, une par tâche. |
| **M14 · La durée du cycle est écrite en dur dans `_coherence_prix_horaire`, et elle alimente deux lignes publiées.** | majeur | `cycle_plancher.py` : `h_enc = (e["chef_equipe"] + e["grutier"]) * h * **8.56**`. 8,56 est la durée du cycle, recopiée. Elle alimente `causes_chiffrees[1]` et `[2]`, publiées dans le tableau « Ce qu'on ajoute / Part de main-d'œuvre » du § S4c. Au premier changement de `data/` qui déplace le cycle, les deux lignes deviennent fausses en silence. § 4.3, R1. | `duree_zone` est déjà calculée dans le `__main__` : la passer à `cout_zone()` et à `_coherence_prix_horaire()`. |

### 3.2 Les dix points, un par un

1. **Unités et homogénéité** — RAS. `verif_unites.py` et le bloc `pint` de l'étalonnage couvrent les cinq bibliothèques, avec des contre-contrôles qui lèvent (« une cadence sans unité de temps lève bien »). J'ai refait les quatre divisions de durée à la main : homogènes.
2. **Référentiels mélangés** — RAS, et c'est structurel : `normes_disponibles = false`, zéro balise V2 dans `content/`, les cinq jeux de charges vides, contrôlés par `check.mjs`. Aucune valeur normative ne fuit.
3. **Article cité sans V0 ni V1** — RAS : aucun article n'est cité. En revanche **sept valeurs V3 sont publiées sans déclaration** (M3) : c'est le même manquement au § 3.2, côté hypothèses.
4. **Ordres de grandeur et ratios** — partiellement. Les ratios publiés (88,5 kg/m³, 1,179 m²/m², 965 MAD/m²) sont plausibles et leurs fourchettes publiées. Mais le module ne publie **aucun taux d'occupation d'équipe**, qui est l'ordre de grandeur décisif d'un planning de rotation (M2), et la part de main-d'œuvre reste à 5,2 % pour 15–30 % attendus — honnêtement signalée, dette 10.
5. **Cohérence data / SVG / 3D / métré / coût / planning** — **deux ruptures** : figure 2 contre tableau S4a et figure 3 (**B2**) ; quantités de situation et relevés contre le réseau (**B1**). Plus `3,4` / `3,41` (m1) et deux calculs de la durée du plancher (m2).
6. **Grille de profondeur § 7.2** — voir § 4 : **minimum de 2 non tenu**, deux critères à 1.
7. **Sécurité** — RAS sur les conseils : la cure, le critère de décoffrage et les étais de reprise sont traités comme des points d'arrêt, et le § 5.0 interdit la valeur chiffrée de résistance, ce que le module dit. **Une réserve** : M5 sous-tend un parc d'étais de reprise dont la densité n'est pas distinguée de l'étaiement complet ; dans l'autre sens cela donnerait un étaiement de reprise insuffisant. Le module ne le dit pas.
8. **Vérité du rendu** — **B2** (occlusion), **M9** (ponctuation), **M12** (front prévu), **M10** (légende sans référent), m3 à m6. Les captures sont bien produites et conservées ; zéro erreur console.
9. **Simplifications non signalées** — **B1** est une simplification de modèle non signalée (R6). Le reste est bien déclaré, y compris les échecs (contre-calcul n° 1 à 26,7 % de la fourchette, part de main-d'œuvre non expliquée, « ce module a deux contre-calculs, pas trois ») : c'est le meilleur de ce module.
10. **Texte télégraphique ou remplissage** — RAS. Aucun paragraphe ne tourne à vide ; chaque encart porte une règle, un chiffre ou une méthode. Le § S4c (« le contrôle qui échoue, et ce qu'il révèle vraiment ») et l'encart du contre-calcul n° 1 sont d'un niveau que le reste du cours devra tenir.

### 3.3 Mineurs

| # | Défaut | Preuve |
|---|---|---|
| m1 | La cadence est publiée **3,4 j** six fois (§ S4d, figure 2, mémo) et **3,41 j** une fois (exercice 2). | `planning_chantier` reçoit `round(cadence, 1)`, `variante_effectif` reçoit `cadence_j` non arrondi. |
| m2 | Deux calculs de la durée du plancher : 32,36 j (cadence 3,4) et 32,43 j (cadence 3,41). L'arrondi `::n1` les masque tous deux en « 32,4 ». | `planning_plancher.duree_totale_j` = 32,36 ; `variantes.reference.duree_plancher_j` = 32,4. |
| m3 | Figure 2 : la courbe du coffrage immobilisé est tracée jusqu'à j = 33 alors que l'axe s'arrête à `fin` = 32,36 : elle déborde à droite de son propre repère. | `coffrage_immobilise` va de 0 à `ceil(duree_totale)` ; `X(j)` n'est pas borné. |
| m4 | Figure 4 : « *Les jours à zéro de la **fin*** ne sont pas une erreur ». La séquence réelle est 0, 0, **4**, 0 : les zéros ne sont pas à la fin. | Capture `…-figure4.png`, jours 30 à 33. |
| m5 | Figure 2 : ni légende numérotée, ni échelle ; les sept couleurs ne sont expliquées qu'en prose dans « ce qu'il faut voir ». Le § 8 demande « éléments numérotés + légende ». | Directive `:::figure` sans clé `legende`. |
| m6 | Figure 1, légende ③ : « **le** front PRÉVU » au singulier, pour **deux** traits (Z5 et Z6). | Capture `…-figure1.png`. |
| m7 | `QA/grilles-72.md` cite encore la règle de cadence **fausse** `max(coffrage, ferraillage) + bétonnage` comme justification d'un 3, et annonce « 10 V3 balisées et registrées » là où il y en a 13 pour TV. | Fichier non mis à jour après D-019. |
| m8 | `STATE.md` : la table « Défauts et passe adversariale » annonce « TV … **19** (4 bloquants, 9 majeurs, 6 mineurs) » alors que le paragraphe suivant en compte 44 sur deux passes ; et « 14 canaris joués (12 socle, **2 TV**) » ignore les 5 de la passe 2. | `STATE.md`, section § 12.2. |
| m9 | `calc/tests/test_plancher.py` : terme mort `_l * (_ep + _h) * 0` dans le recalcul du béton. | Ligne `_vide = …`. |
| m10 | `situation_exercice.ratio_coffrage_de_la_situation` vaut 1,179 **par construction** (numérateur et dénominateur multipliés par le même `frac`) : le corrigé n° 2 de l'exercice 4 en fait une preuve, alors que le rapport ne peut pas valoir autre chose. | `(q["coffrage_m2"] * frac) / (q["surface_m2"] * frac)`. |

---

## 4. Grille d'auto-évaluation § 7.2 — ma notation

| Critère | Note | Appui |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | S2 justifie la zone par quatre propriétés simultanées ; le § S4c explique pourquoi un contrôle qui échoue vaut mieux qu'un contrôle habillé. |
| Les hypothèses sont explicites | **1** | Sept V3 publiées sans balise ni registre (**M3**), dont les cinq qui portent 32 % du cycle et tout le gain de recouvrement ; aucune V3 n'est confrontée à sa propre fourchette (**M4**) ; une balise recopie sa valeur à la main (**M7**). Le module *dit* distinguer trois familles de nombres ; sur ce point précis il ne le fait pas. |
| Les formules sont justifiées | **1** | La règle de cadence est publiée avec une justification que `data/` contredit (**M1**) et une seconde qui ne tient pas (**M2**) ; le **modèle d'avancement** — l'entrée de tout le § S6 — n'est ni énoncé ni justifié, et le cycle du module le réfute (**B1**). |
| L'exemple est vérifié | **2** | Deux algorithmes CPM concordants et un moteur qui résiste à 40 000 réseaux fuzzés ; étalonnage géométrique réel ; quatre durées recalculées. Mais l'étalonnage de la valeur acquise est vide (**M11**) et quatre de mes six canaris franchissent les quinze contrôles. |
| Le piège est identifié | **3** | Six pièges chiffrés, plus ceux que le module retourne contre lui-même. C'est sa meilleure qualité, et elle est réelle. |
| Lien avec l'exécution | **2** | Double lecture entreprise/MOE juste, point d'arrêt modélisé en tâche critique, contrainte de parc. Mais l'exercice 4 enseigne de **viser** une situation physiquement impossible (**B1**) et l'inventaire d'étais confond deux ouvrages (**M5**). |
| Lien avec le coût et le délai | **2** | La chaîne est complète et de bout en bout. Mais la durée publiée est 9,5 % au-dessus de ce que son propre modèle implique (**M2**) et la composition physique de la valeur acquise est fausse (**B1**). |

**Minimum de 2 partout : NON TENU** (deux critères à 1). La grille de l'auteur
(`QA/grilles-72.md`) note **3 partout** ; deux de ces 3 s'appuient sur des éléments que cette passe
infirme (la règle de cadence « démontrée », les « 10 V3 balisées et registrées »).

---

## 5. Contrôles exécutés

```
$ npm run check
VERT — 15 controles passes. Captures : tests/captures/
$ python3 calc/run_all.py
calc/ : VERT
```

Tout est vert, y compris la reprise mode B (le zip se rouvre, `npm ci --ignore-scripts` puis
`npm run check` repassent au vert dans un répertoire neuf) et les 14 tests Playwright. Deux lignes
`info` sont émises honnêtement par `calc/tests/` : le recoupement en dirhams dépasse sa tolérance
(1,033 % pour 1,0 %) et le contrôle de prix horaire reste hors fourchette — les deux sont expliqués
dans le module. **Ce vert n'a toutefois détecté aucun des seize défauts ci-dessus**, et il reste vert
sous quatre de mes six canaris.

---

## 6. La question de fond : les contrôles ciblés suffisent-ils ?

**Non.** Les corrections de la passe 2 ont ajouté des tests qui portent sur **les trois modèles déjà
pris en défaut**, et seulement sur eux. Elles n'ont pas changé la nature des contrôles. Trois d'entre
elles sont même **tautologiques** :

- la règle de cadence est « vérifiée » par `len(dediees) == 3` et par une ré-implémentation de la
  même formule lue dans le même dictionnaire publié ;
- la pointe d'effectif est « vérifiée » en la comparant au maximum du tableau dont elle est le
  maximum ;
- le registre des V3 est « vérifié » par un second contrôle qui ne regarde que les V3 atteignant le
  module par `{{gare.…}}`, c'est-à-dire **aucune** de celles qui passent par `calc/`.

Un contrôle qui part du même objet que ce qu'il vérifie ne peut rien trouver ; c'est la leçon que le
module enseigne au § S6 sur l'indépendance des deux voies, et qu'il ne s'applique pas à ses propres
tests.

### La quatrième erreur de ce type — et c'est la plus coûteuse des quatre

> **L'avancement d'une zone est traité comme un prorata uniforme de chaque poste, et le cycle du
> module dit que c'est impossible.**

Le module mesure l'avancement en « zones équivalentes » et applique cette fraction **à l'identique**
au béton, à l'acier et au coffrage. À 60 % du cycle (5,13 j), le réseau publié dans la figure 3 du
même module dit : coffrage **terminé**, ferraillage des poutres **terminé**, dalle à 91 %, bétonnage
**pas commencé** (BET démarre à 5,65 j). L'état réel est donc 424,3 m² · 8 074 kg · **0 m³**. Le
module publie 254,6 m² · 5 227 kg · **59,0 m³** — et l'exercice 4 demande au lecteur de **viser** ce
tableau, en déclarant la ligne de coffrage « *Correct … Rien à redire* ».

Ce n'est pas une imprécision de présentation : c'est l'entrée de tout le reporting.

| | relevé publié | relevé physiquement cohérent |
|---|---:|---:|
| béton | 352,0 m³ (**−0,63 %**, « muet ») | 295,2 m³ (**−16,7 %**, SIGNAL) |
| coffrage | 1 515,0 m² (**−0,82 %**, « muet ») | 1 697,2 m² (**+11,1 %**, SIGNAL) |

Le « recoupement en unités physiques, poste par poste » — que le module appelle *« le contrôle qui
fait foi »* et place en n° 3 de la fiche mémo — conclut que « *les deux postes géométriques sont sous
le pour cent : l'avancement déclaré tient* ». Il ne le peut que parce que `data/` a **fabriqué** les
relevés sur le même prorata (`quantites_relevees.base_du_choix` : « *posées légèrement en retrait des
quantités théoriques de 3,6 zones* »). Appliqué à de vrais attachements, ce contrôle hurlerait à
17 % sur le poste dont le module affirme qu'« *il ne dépend d'aucune hypothèse* ».

**Pourquoi aucun des quinze contrôles ne le voit.** Parce qu'ils vérifient tous que la voie A et la
voie B concordent — et que les deux voies partagent leur entrée décisive, le prorata. Le module
diagnostique cette maladie exactement (« *deux voies ne sont indépendantes que si elles ne partagent
pas leur entrée décisive* ») et la contracte un cran au-dessus.

**Ce qu'il faut en tirer pour les cinquante modules à venir.** Un test de modèle ne peut pas être
écrit en relisant le modèle : il faut une **seconde représentation du même objet physique**, déjà
présente dans le dépôt, et les confronter. Ici elle existait : le **réseau de la zone**. La règle
générale, qui est contrôlable :

> toute grandeur publiée qui décrit l'**état** du chantier à une date doit être dérivable du réseau à
> cette date, et un test doit faire cette dérivation.

C'est ce test-là qui aurait attrapé B1 — et aussi B2 de la passe 2 (l'histogramme), et M12 de cette
passe (le front prévu de la figure 1).

---

## 7. Corrections de la passe 2 : ce qui tient, ce qui ne tient pas

| Défaut de la passe 2 | Vérifié ici |
|---|---|
| **B1** règle de cadence incomplète | **corrigé pour les poutres** — rejoué, la borne passe bien aux poutres et l'exercice 3 conclut qu'il faut renforcer les deux équipes. **Non corrigé sur le fond** : liste blanche de trois tâches, décoffrage exclu sur une justification fausse, test qui épingle le défaut (**M1**), et la justification du `+ bétonnage` ne tient pas (**M2**). |
| **B2** histogramme en file indienne | **corrigé** — il est bâti sur les dates du réseau, j'ai reconstruit les 34 valeurs à l'identique et confirmé la pointe de 24 par balayage des fronts. **Nouveau défaut introduit** : échantillonnage aux instants entiers (**M8**), et une permutation d'effectifs passe (**M13**). |
| **B3** courbe « réalisé » fabriquée | **corrigé** — un seul point de constat, à la date d'arrêt, écart coté, aucun `realise` dans les 34 points de la courbe ; vérifié dans `figures.courbe_s`. La **légende**, elle, renvoie à un SV absent du tableau (**M10**). |
| **M1** hypothèses de cycle codées en dur | **à moitié** — les cinq sont dans `data/` avec leurs fourchettes, mais ni balisées ni registrées (**M3**), et la note de `data/` exige explicitement qu'elles le soient. |
| **M2** phrase du CPM | **corrigé** — « le contrôle ne dirait pas laquelle est fausse ». |
| **M3** multiplicateurs à la main | **corrigé** (`rapports` calculés) — **rouvert ailleurs** : « un facteur deux » (**M6**), `8.56` en dur (**M14**). |
| **M4** contrôle de registre tautologique | **non corrigé** — le second contrôle ajouté ne voit que 8 feuilles sur 19 et aucune de celles qui comptent (**M3**). |
| **M5** recalcul du béton copié | **corrigé** — autre découpage géométrique, cotes lues dans `data/`, et le canari N4 le fait sonner. |
| **M6** exercice 4 | **réécrit** — et le fond est de nouveau faux, dans l'autre sens : le corrigé déclare juste une ligne physiquement impossible (**B1**). |
| **M7** figure 4 sans axe | **corrigé** — axe, unité, cotation de la pointe, moyenne. |
| **M8** situation tapée à la main | **corrigé** quant à la provenance (calculée), **faux** quant au modèle (**B1**). |
| **M9** marges et chemin critique du CPM | **corrigé, et il tient** — 40 000 réseaux fuzzés, 0 marge fausse, 0 levée abusive. |
| **M10** figure 2 sans contenu technique | **remplacée** par le diagramme de rotation, qui apporte beaucoup — et qui ment sur deux de ses sept durées (**B2**). |
| **M11** `base_du_choix` incohérent | **corrigé** — « 1,26 zone », conforme à la sortie. |
| **M12** étais | **corrigé quant au périmètre** (zones décoffrées comptées), **faux quant à la densité et non borné** (**M5**). |
| **m1** à **m9** | **corrigés** — accents sur « jours ouvrés », « moyenne 14,1 », puces ① et ② séparées, « 4ᵉ jour de la semaine 4 », `STATE.md` à 148 lignes, `data/materiel` sans doublon, `derive_signe` porté par la valeur, Gantt en formats homogènes, prévu ajouté à la figure 1. |
| **m10** étalonnage de la valeur acquise | **non corrigé** — le « cas fermé » ajouté n'appelle pas la bibliothèque (**M11**). |

**Trois corrections de la passe 2 ne tiennent pas sur le fond** (B1, M4, m10), **deux ont introduit un
défaut neuf** (B2 → M8/M13, M10 → B2), **une a été réécrite en conservant son erreur de fond**
(M6 → B1). C'est le même ratio qu'entre la passe 1 et la passe 2.

---

## 8. Bilan

| Gravité | Nombre |
|---|---:|
| **Bloquant** | **2** |
| **Majeur** | **14** |
| **Mineur** | **10** |
| **Total** | **26** |

### Zéro bloquant ? — **NON.**

Deux bloquants : **B1** (le modèle d'avancement contredit par le cycle du module, qui porte tout le
§ S6, la figure 5, l'exercice 4 et la fiche mémo) et **B2** (la figure 2 publie deux durées fausses
et contredit deux autres publications du même module, sous une légende qui affirme l'inverse).

### Verdict sur la question du § 5.3 : ce module peut-il servir de modèle à la duplication ?

**Pas encore — mais il n'en est pas loin, et ce qu'il faut corriger est identifié.**

Ce qui est **mûr pour la duplication**, et qui vaut d'être copié tel quel :
- la chaîne `data/ → calc/ → figures → module`, avec échec du build sur variable absente, empreinte
  de `data/` et reconstruction complète par `npm run check` ;
- la **méthode de contre-calcul** : deux algorithmes pour le CPM, deux sources pour l'avancement, et
  surtout la discipline de **publier ce qu'un contrôle ne prouve pas** (le « 26,7 % de la fourchette »
  et le « cet écart n'est pas expliqué » sont du meilleur niveau pédagogique du dépôt) ;
- la **double lecture entreprise / maîtrise d'œuvre** et le point d'arrêt modélisé en tâche critique ;
- le moteur CPM, désormais éprouvé.

Ce qui **ne doit pas être dupliqué en l'état**, parce que chaque module de suivi le recopierait :
1. **B1** — le modèle d'avancement. C'est le défaut à traiter en premier : il se propage mécaniquement
   à D2, D4 et D7, qui sont le cœur du métier du lecteur.
2. **B2** — la fonction `rotation` de `svgkit.js`, qui servira à tous les plannings de rotation du cours.
3. **M1 et M2** — la règle de cadence, qui sera reprise dans C3, D2 et D7.
4. **M3, M4, M7** — la chaîne de déclaration des V3 : tant qu'une hypothèse peut atteindre un module
   par `calc/` sans balise ni registre, le § 3.2 n'est pas tenu, et le lecteur ne reçoit pas la liste
   qu'on lui promet à chaque livraison.
5. **M11** — l'étalonnage vide : § 3.3 interdit d'utiliser comme référence des résultats non étalonnés.

**Recommandation au lecteur.** Ne validez pas encore la tranche verticale comme gabarit. Demandez une
quatrième passe **limitée à B1, B2, M1 à M5, M7, M11 et M13** — huit corrections, toutes locales —
puis validez. La forme, la longueur, la densité et l'angle du module, eux, me paraissent **bons** :
c'est la question que le § 5.3 vous pose en premier, et sur celle-là ma réponse est oui. Sur la 3D :
son absence ne m'a pas manqué une seule fois ; les figures 1, 3, 4 et 5 portent tout ce qu'il faut, et
la figure 2 portera tout ce qu'il faut une fois B2 corrigé.

**Un dernier mot sur la méthode.** Trois passes, 70 défauts, 9 bloquants, et la troisième en trouve
encore deux que quinze contrôles verts ne voient pas. Ce n'est pas un échec du dispositif : c'est sa
mesure. La conclusion de D-022 — « les contrôles vérifient les nombres, pas les modèles » — est juste
et reste entière. Ce que cette passe ajoute, c'est qu'un test de modèle **a besoin d'une seconde
représentation du même objet physique**, et que le dépôt en possède déjà une (le réseau de la zone)
qu'il n'utilise pas pour se contrôler.

---

*Relecture conduite sans modifier le dépôt. Essais menés sur des copies dans un bac à sable isolé.
Seul ce fichier a été écrit.*
