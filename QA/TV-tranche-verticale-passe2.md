# Passe adversariale n° 2 — module `TV` (tranche verticale de suivi)

**Relecteur hostile, indépendant de l'auteur.** Seconde passe, après une première qui avait relevé
19 défauts (4 bloquants) déclarés corrigés.
Date : 16/10/2026 · commit relu : `17078d2` · empreinte `data/` : `2f05de1c3805`.

**Méthode.** Je n'ai lu ni `QA/TV-corrections-passe1.md` ni la section « Passe adversariale » de
`STATE.md`. J'ai recalculé **huit grandeurs clés** depuis `data/projet-gare.json` seul, par mes
propres scripts, avant d'ouvrir `calc/`. J'ai rejoué les canaris T2, T6 et les trois réseaux CPM
exigés, et j'en ai inventé **cinq nouveaux**. J'ai regardé les cinq captures. J'ai lu
`QA/TV-tranche-verticale.md` **en dernier**, pour contrôler les corrections annoncées.

---

## 1. Contre-expertise à l'aveugle — recalculs depuis `data/` seul

Scripts : `/tmp/claude-0/-home-user-mine/70713aa8-3622-5c6d-a7c2-bce4a8b25d73/scratchpad/recalc.py`,
`histo.py`, `renforce.py`. Aucun import de `calc/`.

| # | Grandeur | Mon recalcul indépendant | Publié | |
|---|---|---:|---:|---|
| 1 | **Quantité** — béton d'une zone : 360 × 0,25 + 2 × 24,0 × 0,35 × 0,50 | **98,40 m³** | 98,4 | ✓ |
| | coffrage : (360 − 16,8) + 48,0 + 16,8, +4 % | **424,32 m²** | 424,3 | ✓ |
| | acier : 80 × 90,0 + 180 × 8,40 | **8 712 kg** (ratio 88,5 kg/m³) | 8 712 / 88,5 | ✓ |
| 2 | **Durées** — 424,32/(30×8) · 1512/(150×4) · 7200/(300×8) · 98,4/30/8 | **1,768 · 2,520 · 3,000 · 0,410 j** | 1,77 · 2,52 · 3,00 · 0,41 | ✓ |
| 3 | **Cycle** — chaîne 2,40 + 3,00 + 0,25 + 0,41 + 2,00 + 0,50 | **8,556 j** ; somme 10,45 ; gain 1,89 j | 8,557 / 10,45 / 1,89 | ✓ |
| 4 | **Cadence de rotation** — max(1,77 ; 3,00) + 0,41 | **3,41 j** | 3,41 | ✓ *(mais voir B1)* |
| | durée du plancher — 7 × 3,41 + 8,556 | **32,43 j** | 32,4 | ✓ |
| 5 | **Coffrage immobilisé simultanément** — ⌈8,556/3,41⌉ = 3 ; 3 × 424,32 | **1 273 m²** pour 1 300 au parc | 1 273 / 1 300 | ✓ |
| 6 | **Coût** — 123 000 + 148 104 + 76 377,6 | **347 481,6 MAD** · 965,2 MAD/m² | 347 478 / 965 | ✓ |
| 7 | **Valeur acquise** — VA = 3,6 × 347 482 ; CPI = VA/1 330 000 | **1 250 935 MAD · CPI 0,9406** | 1 250 921 / 0,941 | ✓ |
| | voie B — 352×1250 + 30 900×17 + 1 515×180 | **1 238 000 MAD → 3,563 zones** | 1 238 000 / 3,56 | ✓ |
| | VP à j = 19 (avancement fractionnaire des 8 zones) | **4,86 zones → SPI 0,741** | 4,86 / 0,741 | ✓ |
| 8 | **Pointe d'effectif** — dates CPM réelles, 8 zones à 3,41 j | **22 compagnons au jour 5** | **23** | **✗ → B2** |

**Les sept premières familles concordent.** La huitième ne concorde pas, et le désaccord n'est pas
un arrondi : voir B2.

---

## 2. Canaris

### 2.1 Les canaris exigés par la passe 1

Rejoués sur une copie jetable (`cp -a` dans le scratchpad). `/home/user/mine` n'a pas été modifié.

| Canari | Ce que j'ai fait | Résultat |
|---|---|---|
| **T2** | `ferr_dalle` divisé par `ferrailleurs_poutres` au lieu de `ferrailleurs_dalle` | **SONNE** — 5 échecs : « durée recalculée : ferraillage_dalle_j 6,0 contre 3,0 », « ferraillage_dalle_j dépend bien de *ferrailleurs_dalle* », « doubler *ferrailleurs_poutres* ne touche pas les autres durées », « la variante renforcée NE tient PAS », « SPI dans une plage plausible — 1,417 ». La correction de **M1** de la passe 1 tient. |
| **T6 à 190 m²/j** (borne basse) | `rendement_equipe_coffrage_m2_j = 190` | **SONNE** — écart 26,32 %, 2 échecs. **Et le module le publie honnêtement** : il écrit la plage qui passe [228,6 ; 252,6], la fourchette déclarée [190, 280], le « 26,7 % de la fourchette » et la phrase « Pris à la borne basse, il échoue ». C'est la meilleure page du module. |
| **T6 à 280 m²/j** (borne haute) | idem, 280 | **SONNE** — écart 14,29 %, 2 échecs. |
| **CPM A(10)→B(1), déc. −10** | | durée **10 ✓**, verdict « OK » ✓ — mais `taches_critiques_voie_A = []` et marge de A = **9 j** → **M9** |
| **CPM A(10)→B(1), déc. −20** | | durée **10 ✓**, verdict « OK » ✓ — marge de A = **19 j** → **M9** |
| **CPM A(2)→B(5), déc. −10** | | durée **5 ✓**, verdict « OK » ✓ — chemin critique = {B} seul, marge de A = 8 j → **M9** |

Sur les trois réseaux, **les durées sont justes et le verdict n'accuse plus personne** : la
correction du bloquant B4 de la passe 1 tient **sur les durées**. Elle ne tient ni sur les marges,
ni sur le chemin critique, ni sur la phrase publiée (**M9**, **M2**).

### 2.2 Cinq canaris de mon invention

| # | Canari | Passe ou sonne |
|---|---|---|
| **C1** | prix de l'acier et du coffrage **permutés** dans `data/` (17 ↔ 180) | **sonne**, mais par la bande : seul « CPI dans une plage plausible — 4,597 » tombe. Aucun contrôle ne regarde la cohérence d'un prix unitaire avec sa fourchette déclarée. |
| **C2** | `longueur_dans_zone_m` lue à **15 m** au lieu de 24 (quantité lue dans la mauvaise direction) | **sonne**, mais uniquement grâce à un littéral : « volume de béton recalculé à la main — 95,25 contre 98,4 ». Voir **M5** : ce « recalcul à la main » est une copie des données, pas une seconde voie. |
| **C3** | **date d'arrêt** décalée de 19 à 24 jours ouvrés | **sonne** — « SPI dans une plage plausible — 0,575 ». Un décalage plus petit (19 → 21, SPI 0,66) passerait sous le garde-fou… lequel est une fourchette de plausibilité, pas un contrôle de cohérence. |
| **C4** | **signe de SV inversé** (VP − VA au lieu de VA − VP) | **sonne** — 2 échecs, dont « l'écart vertical de la figure EST bien SV » : le test ajouté après la passe 1 fait son travail. |
| **C5** | **VA minorée de 20 %** dans la grandeur elle-même (pas dans les identités) | **sonne** — mais les **cinq identités** de l'étalonnage de `valeur_acquise` passent toutes (CPI = VA/CR ✓, SPI ✓, CV ✓, SV ✓, EAC×CPI ✓). Seul le cas trivial « CPI = SPI = 1 » mord. Voir **m10**. |

**Observation commune aux onze canaris** : `node build/build.mjs` a **réussi dans tous les cas** —
le module est republié avec les chiffres faux. Le garde-fou est `npm run check`, qui lance `calc/`
d'abord. C'est suffisant tant que personne ne publie sans passer par `npm run check`.

---

## 3. Tests réellement lancés

```
$ python3 calc/run_all.py        → calc/ : VERT
$ npm run check                  → VERT — 14 controles passes
```

Les 14 contrôles passent, y compris le rendu Playwright (14 passed, 17,1 s), la reprise du zip mode B
et l'empreinte `data/`. **Aucun des défauts ci-dessous n'est vu par un seul de ces contrôles.**

Deux notes sur ce vert :
- `calc/run_all.py` imprime deux lignes `info` que `npm run check` n'affiche pas : « recoupement en
  dirhams : écart 1,033 % > tolérance 1,0 % » et « le contrôle de prix horaire sort de sa fourchette
  (5,2 % contre [15, 30]) ». Les deux sont traitées honnêtement dans le module. C'est bien.
- `13.3 · STATE.md court — 150 lignes sur 150` : zéro marge (**m5**).

---

## 4. Grille des 10 points du § 12.2

| # | Point | Constat |
|---|---|---|
| 1 | Unités, homogénéité | **RAS, prouvé.** `calc/verif_unites.py` couvre les 4 bibliothèques, avec contre-contrôles qui lèvent (j'ai vérifié qu'ils lèvent : 10 `leve()` passent). J'ai refait l'homogénéité à la main : `m²/(m²·j⁻¹·comp⁻¹ × comp) = j` ✓, `m³/(m³·h⁻¹)/(h·j⁻¹) = j` ✓, `kg × MAD·kg⁻¹ = MAD` ✓, CPI/SPI sans dimension ✓. **M7 de la passe 1 est corrigé.** |
| 2 | Référentiels mélangés | **RAS, prouvé.** `grep -ocE "BAEL\|BPEL\|RPS\|Eurocode\|EN 199\|NF P\|fck\|C25/30"` sur `modules/01-…html` → 0. `check.mjs` vérifie en plus l'absence de balise V2 et le vide de `charges.*`. Phase § 5.0 respectée. |
| 3 | Article cité sans V0/V1 | **RAS, prouvé.** Zéro balise V2, zéro numéro d'article, 10 balises V3 toutes pourvues de fourchette et d'année. **Mais** le registre est incomplet par construction : **M4**. |
| 4 | Ordres de grandeur et ratios | **Défauts M3, M11.** Les ordres de grandeur sont bons (88,5 kg/m³, 965 MAD/m², 1,18 m²/m², 3,28 h de pompe) ; ce sont les **multiplicateurs de commentaire** qui sont faux (« quarante fois », « ± 44 % ») et une justification de `data/` qui annonce un retard six fois trop petit. |
| 5 | Cohérence data / figures / métré / coût / planning | **Défauts B1, B2, B3, M10, M12.** C'est le point le plus atteint : l'histogramme contredit le Gantt, la figure 2 contredit la figure 3, la courbe « réalisé » n'est pas un constat, la variante des exercices viole la règle de cadence du module, l'inventaire d'étais contredit le texte sur les étais de reprise. |
| 6 | Grille de profondeur § 7.2 | **Défaut** : minimum de 2 **non tenu** sur « l'exemple est vérifié ». Voir § 6. |
| 7 | Sécurité : conseil dangereux ou omission | **RAS sur le danger physique** (étaiement, décoffrage, étais de reprise, point d'arrêt irréversible sont tous traités et mis en avant). **Mais B1 est un conseil professionnel faux** : le module dicte au lecteur une phrase à prononcer en réunion qui engage sur un délai inatteignable. Ce n'est pas de la sécurité des personnes, c'en est l'équivalent contractuel. |
| 8 | Vérité du rendu | **Défauts B2, B3, M7, m1, m2, m3, m8.** Zéro erreur console, zéro requête externe, zéro chevauchement texte/texte — tous prouvés par Playwright. Les défauts sont ailleurs : une figure sans échelle, une figure fabriquée, une figure décorative, des libellés non francisés. |
| 9 | Simplifications non signalées | **Défauts M1, B3.** 2,75 j de cycle (cure, décoffrage, point d'arrêt) et les deux coefficients de recouvrement sont des hypothèses non déclarées, codées en dur. La courbe « réalisé » est une interpolation non signalée. |
| 10 | Texte télégraphique, remplissage | **RAS, et c'est remarquable.** J'ai cherché le paragraphe qui ne porte ni règle, ni chiffre, ni méthode : je n'en ai pas trouvé. L'encart « Le contrôle qui échoue, et ce qu'il révèle vraiment » et celui « Pourquoi ceci n'est PAS un contre-calcul » sont au-dessus de ce que le § 7.1 demande. |

---

## 5. Tableau des défauts

| défaut | gravité | preuve | correction proposée |
|---|---|---|---|
| **B1 · La cadence de la variante renforcée (2,41 j) est infaisable, et elle renverse la conclusion des exercices 2 et 3.** | **bloquant** | Le module publie et justifie sa règle : « la cadence est bornée par les tâches qui mobilisent une **équipe dédiée**, donc une seule zone à la fois », puis `cadence = max(d_coffrage ; d_ferraillage de dalle) + d_bétonnage`. **Le ferraillage des poutres est une tâche à équipe dédiée** (`data/effectifs.ferrailleurs_poutres = 4`) et il dure **2,52 j** — il est absent du `max`. Sans effet sur le cas de référence (max(1,77 ; 3,00) = 3,00 > 2,52) ; **décisif sur la variante renforcée** : `cycle_plancher.py:variante_effectif` rend `cad = max(1,77 ; 2,00) + 0,41 = 2,41 j`, alors que les 4 ferrailleurs de poutres ne peuvent pas livrer une zone tous les 2,41 j. Valeur juste : `max(1,77 ; 2,52 ; 2,00) + 0,41 = **2,93 j**`. Conséquences, toutes publiées : durée du plancher **24,4 j → 28,1 j** ; « **sous la cible** » (25 j) devient **au-dessus de la cible** ; zones coffrées simultanément **4 → 3** ; déficit de tables **397 m² → 0** ; effectif de pointe 31 → faux. L'exercice 3 écrit *« Ce qu'il faut dire en réunion : 25 jours est atteignable en portant le ferraillage de dalle à 12 compagnons : 24,4 jours… »* — **un engagement de délai intenable dicté au lecteur**, dans le module qui enseigne qu'« une cadence annoncée en réunion sans ce calcul est une cadence qui sera tenue par le parc ». Preuve numérique : `scratchpad/renforce.py`. **Effet de bord** : le test « la variante renforcée NE tient PAS : le contrôle sait donc sonner » est la **seule** démonstration que `coherence_materiel` sache sonner — elle repose entièrement sur cette cadence infaisable. Corrigé B1, ce contrôle ne sonne plus nulle part. | (1) Écrire `cadence = max(toutes les tâches à équipe dédiée) + d_bétonnage`, en itérant sur les postes de `data/effectifs` au lieu d'en nommer deux. (2) Ajouter un test : `cadence >= max(durée de chaque tâche à équipe dédiée)`, qui aurait attrapé ceci. (3) Refaire les exercices 2 et 3 : à 12 ferrailleurs de dalle le levier (a) **n'atteint plus la cible**, ce qui est une leçon **meilleure** que la leçon actuelle (il faut renforcer *le deuxième* goulot, les ferrailleurs de poutres, avant de gagner quoi que ce soit). (4) Donner à `coherence_materiel` un autre cas qui le fasse sonner. |
| **B2 · L'histogramme d'effectifs (figure 4) ne suit pas le Gantt (figure 3) du même module : 26 jours sur 33 sont faux.** | **bloquant** | `cycle_plancher.py` construit `figures.effectifs` par une **chaîne de `elif` sur des durées enchaînées** (`deb+cof`, `deb+cof+fep`, `deb+cycle−2,5`), c'est-à-dire sur un ordonnancement **séquentiel**, alors que la figure 3 publie l'ordonnancement **CPM avec recouvrements** (COF 0→1,77 ; FEP 0,88→3,40 ; FED 2,40→5,40 ; BET 5,65→6,06). Comparaison jour par jour (`scratchpad/cmp_histo.py`) : **26 jours sur 33 diffèrent**. Exemples : jour 1 → publié 10, vrai 14 (la structure `elif` ne peut **jamais** représenter COF et FEP présents ensemble, ce que la figure 3 montre pourtant) ; jour 9 → publié 14, vrai 6 ; **jours 30, 31, 32 → publié 7 (l'équipe de bétonnage), vrai 2** (il ne reste que la cure et le décoffrage de Z8 : aucune équipe de production n'est sur le plancher). **Pointe publiée 23, pointe vraie 22.** La « Ce qu'il faut voir » affirme « chaque dent est un changement de poste à l'intérieur d'un cycle » : les dents sont des artefacts du mauvais modèle. Le 23 et le 31 sont republiés **six fois** dans les exercices 2 et 3 et dans la phrase de réunion. | Construire l'histogramme depuis `cc["detail"]["tot"]` — les dates que la figure 3 affiche déjà — et **additionner** les équipes présentes au lieu de les sélectionner par `elif`. Ajouter un test : « l'effectif du jour *k* de la figure 4 est la somme des équipes dont la barre du Gantt couvre *k* », sur au moins trois jours dont un de recouvrement et un de fin de chantier. |
| **B3 · La courbe « réalisé » (figure 5) n'est pas un constat : c'est la courbe prévue multipliée par une constante, et sa légende annonce une lecture impossible.** | **bloquant** | `cycle_plancher.py` : `pt["realise"] = avancement_prevu(j) * (reel_zones / zones_prevues_arret)`. J'ai vérifié le rapport point par point dans `figures.courbe_s` : 0,733 · 0,759 · 0,727 · 0,746 · 0,748 … 0,739 · 0,740 · **0,740** — **constant**. Il n'existe **qu'un seul point de constat réel**, celui du jour 19 ; les 20 autres points du trait plein sont la prévision remise à l'échelle. Deux conséquences. (a) La « Ce qu'il faut voir » dit : « **La pente de la courbe réelle, et non sa position, dit si le retard se creuse ou se résorbe** » — par construction le rapport réalisé/prévu est constant, donc cette courbe **ne peut jamais** montrer un retard qui se creuse ou se résorbe : la légende annonce une lecture que la donnée ne porte pas. (b) L'« Erreur courante » de la **même figure** dit : « Un constat et une prévision ne se tracent pas du même trait » — or le trait plein *est* une prévision sur 20 de ses 21 points, sans que rien ne le dise. R6 (« aucune simplification silencieuse ») et R8. Le test ajouté après la passe 1 (« l'écart vertical EST bien SV ») ne contrôle que **le point du jour 19** : il valide le seul point vrai et ne voit pas les vingt autres. | Soit tracer le constat comme ce qu'il est — **un point** (ou les 4 jalons de zones coulées, qui sont de vraies dates), avec le trait plein réservé à ce qui est relevé ; soit, s'il faut un trait, le tirer des **quantités relevées cumulées** (`suivi.quantites_relevees` existe déjà) et non du plan remis à l'échelle. Dans les deux cas, retirer la phrase sur la pente ou lui donner de quoi se lire. |
| **M1 · Un tiers du cycle est fait d'hypothèses codées en dur : ni dans `data/`, ni balisées, ni dans le registre, ni pourvues d'une fourchette.** | majeur | `grep -in "cure\|decoffr\|point d.arret" data/projet-gare.json` → **rien**. Les valeurs vivent uniquement dans `calc/cycle_plancher.py:reseau_zone` : `cure_j = 2.0`, `Tache("DEC", …, 0.5)`, `Tache("PTA", …, 0.25)`. Total **2,75 j sur 8,556 — 32 % du cycle**, donc 32 % de la durée du plancher, de la cadence et du planning. S'y ajoutent les **deux coefficients de recouvrement**, `-t["coffrage_j"]*0.5` et `-t["ferraillage_poutres_j"]*0.4`, qui produisent à eux seuls la totalité du « gain du recouvrement » de **1,89 j (18,1 %)** que le module met en avant. Aucune de ces cinq valeurs n'a de fourchette, de balise `⟦V3|…⟧` ni de ligne de `registre-hypotheses.csv`, alors que le § 5.0.6 exige que « **toute** valeur numérique reste V3, hypothèse déclarée, fourchette, année ». Troisième nombre en dur : `_coherence_prix_horaire` contient `h_enc = (chef + grutier) * h * **8.56**` — la durée du cycle recopiée à la main, qui ne suivra pas si le cycle change. | Porter les cinq valeurs dans `data/` (`cycle.cure_j`, `cycle.decoffrage_j`, `cycle.point_arret_j`, `cycle.recouvrement_coffrage_pct`, `cycle.recouvrement_ferraillage_pct`) avec fourchette et année ; les baliser dans le contenu ; remplacer `8.56` par la variable du cycle. Le module gagnerait au passage sa vraie leçon : à 2 j de cure déclarée sans fourchette, la cadence annoncée est une hypothèse, pas un résultat. |
| **M2 · La phrase publiée sur le CPM est fausse — et c'est un défaut bloquant de la passe 1 déclaré corrigé.** | majeur | `modules/01-tranche-verticale-suivi.html` publie encore : « **Si elles divergeaient, c'est le parcours avant/arrière qui serait faux.** » La docstring de `cpm.py`, elle, a été corrigée et dit l'inverse : « *si elles diffèrent, l'une des deux est fausse — et le contrôle ne dit **PAS** laquelle. L'énumération n'est pas une référence par nature : sa première version rendait 1 jour là où la réponse était 10* ». Le `verdict` du code a été corrigé aussi (« l'un des deux est faux, le contrôle ne dit pas lequel »). **Seule la phrase publiée ne l'a pas été** : le module enseigne au lecteur une règle que son propre historique réfute, et que sa propre bibliothèque contredit. | Remplacer par « si elles divergent, l'une des deux est fausse et le contrôle ne dit pas laquelle — c'est l'étalonnage qui tranche », et raconter en deux lignes le cas réel (l'énumération rendait 1 au lieu de 10) : c'est une bien meilleure leçon que la phrase actuelle. |
| **M3 · Trois multiplicateurs de commentaire tapés à la main, deux faux, et une incertitude annoncée de deux façons contradictoires.** | majeur | Rendu, § S6 : « le ratio V3 a une fourchette de **44 %**, soit **quarante fois** l'écart constaté ». L'écart constaté sur l'acier est **−1,48 %** (`valeur-acquise.json`) : 43,9/1,48 = **29,7**, pas 40. Rendu, fiche mémo S8 : « il vient d'un ratio dont la fourchette vaut **± 44 %**, soit **vingt fois** le seuil ». `etendue_pct = 43,9` est l'**étendue totale** (7 026 → 10 848 kg autour de 8 712), soit **−19,4 %/+24,5 %** : écrire « ± 44 % » double l'incertitude. Et « vingt fois le seuil » n'est cohérent qu'avec **± 22 %**, pas avec le « ± 44 % » de la même phrase. Troisième lecture dans le **même module**, § S1 : « l'acier est un ordre de grandeur à **± 20 %** ». Trois valeurs pour une seule grandeur, dont deux fausses. Même famille : « (a) atteint la cible pour **moins d'un tiers** de ce supplément » (397/1 273 = 31,2 %) est juste mais tapé à la main, donc périmable en silence. | Publier `etendue_pct` et `demi_etendue_pct` comme **deux** variables distinctes de `calc/`, et faire calculer les rapports (`etendue / |ecart_acier|`, `demi_etendue / seuil`) plutôt que de les écrire. Aligner le § S1 sur la même source. |
| **M4 · Le contrôle « chaque V3 publiée a sa ligne de registre » est tautologique : il ne peut pas détecter une V3 non déclarée.** | majeur | `build/check.mjs` compte les balises `⟦V3…⟧` de `content/` et les compare au nombre de lignes de `data/registre-hypotheses.csv` — **registre que `build/build.mjs` génère depuis ces mêmes balises**. `10 == 10` est vrai par construction. Le seul filet complémentaire est un `grep` de la chaîne littérale `« (V3 »` hors balise. Conséquence concrète : les hypothèses qui pilotent **tous** les nombres publiés du module sont V3, déclarées avec fourchette dans `data/`, et **absentes du registre** — les 4 cadences (30 m²/j, 300 kg/j, 150 kg/j, 30 m³/h), le rendement d'équipe (232), les 3 prix unitaires (1 250, 17, 180), `coffrage_rives_pct` (4 %), les 6 effectifs, et les 3 valeurs de `suivi`. Le registre du module témoin déclare **10** hypothèses là où il en publie une trentaine. | Faire le contrôle dans l'autre sens : parcourir `data/` à la recherche des objets `{valeur, fourchette}` **effectivement lus** par `calc/` (ils sont identifiables), et exiger une ligne de registre pour chacun. Le registre devient alors une sortie de la chaîne de données, pas un reflet du balisage. |
| **M5 · Le seul « recalcul indépendant à la main » des quantités est une copie littérale des données.** | majeur | `calc/tests/test_plancher.py`, sous le commentaire « *béton : recalcul **INDÉPENDANT**, à la main, sans appeler plancher.py* » : `beton_main = 360 * 0.25 + 2 * 24.0 * 0.35 * 0.50`. Les six littéraux sont la recopie de `longueur×largeur`, `epaisseur_m`, `n_poutres`, `longueur_dans_zone_m`, `b_m`, `retombee_sous_dalle_m`. Ce n'est pas une seconde voie (§ 3.3) mais un **verrou de non-régression sur les données** : (a) il n'attrape mon canari **C2** que parce que le littéral `24.0` cesse de correspondre à `data/` ; (b) un changement **légitime** de géométrie — que le § 10.1 prévoit explicitement, consigné dans `DECISIONS.md` — le fait échouer alors que rien n'est faux, et il **accuse le code** ; (c) c'est une violation de R1 à l'intérieur de `calc/tests/`. Par contraste, les quatre durées du même fichier sont, elles, bien recalculées depuis `data["cadences"]` et `data["effectifs"]` — la bonne méthode existe dans le fichier, dix lignes plus bas. | Recalculer le béton par **une autre route** depuis `data/` : volume total de la mezzanine divisé par `nb_zones`, ou nombre de poutres déduit de `trame_longitudinale_m` au lieu de `entraxe_m`. Une seconde voie, pas une copie. |
| **M6 · L'exercice 4 annonce trois défauts, en démentit un, et sa preuve n° 3 contredit la leçon du § S6.** | majeur | L'énoncé : « **Trois choses ne vont pas. Lesquelles ?** ». Le corrigé n° 2 est titré en gras « **Le coffrage est sous-compté.** » puis se réfute immédiatement : « 255/(0,60 × 360) = 1,18 : **cohérent**. Le vrai problème est ailleurs → voir 3 », et la note finale avoue « le point 2 est un **leurre** ». Il n'y a donc que **deux** défauts, et le corrigé publie en gras une affirmation fausse. Plus grave, le corrigé n° 3 écrit : « *le contrôle du § S6 montre qu'à l'échelle du plancher, l'écart entre déclaration et relevés atteint déjà **1,03 %*** » — c'est exactement le chiffre que le § S6, dix paragraphes plus haut, vient de disqualifier : « **Et pourtant ce n'est pas un signal** […] l'alarme en dirhams était du **bruit promu au rang de signal** ». L'exercice utilise comme preuve ce que le cours vient d'apprendre à ne pas prendre pour une preuve. | Écrire « Deux choses ne vont pas, et une troisième a l'air fausse sans l'être » — l'intention pédagogique (apprendre à reconnaître ce qui est juste) est bonne, c'est l'énoncé qui la trahit. Et remplacer la preuve n° 3 par le recoupement **en unités physiques**, qui est la leçon réellement enseignée. |
| **M7 · La figure 4 n'a ni axe des ordonnées, ni unité, ni cotation de la pointe — alors que sa légende dit que c'est la pointe qu'il faut lire.** | majeur | `assets/svgkit.js:histogramme` ne trace que l'axe horizontal, les barres, et une ligne de moyenne. Aucune graduation verticale, aucune unité (« compagnons »), aucun titre d'axe, aucune étiquette sur la barre maximale. **Le seul nombre de la figure est la moyenne** (« moyenne 14.5 ») — précisément ce que la « Ce qu'il faut voir » dit de ne pas regarder : « *La pointe donne le dimensionnement de la base-vie et des moyens — c'est **elle** qu'il faut regarder, **pas la moyenne*** », et l'« Erreur courante » condamne de « lisser cet histogramme en moyenne ». La figure rend la faute inévitable et la lecture juste impossible. Le § 8 exige « cotes issues des données, **unités**, échelle indicative » ; le § 12.1 c vérifie les chevauchements, pas l'échelle. | Ajouter l'axe des ordonnées gradué, l'unité, et l'étiquette de la barre de pointe (la valeur existe : `max(figures.effectifs[].n)`). Ajouter au test de rendu un contrôle « toute figure à grandeur continue porte une graduation verticale ». |
| **M8 · Le tableau de la situation de travaux de l'exercice 4 est entièrement tapé à la main.** | majeur | Six quantités et six montants en clair dans `content/01-…md` : 59,0 m³ · 5 227 kg · 255 m² · 241 h · 219 354 · 208 509. Je les ai tous recalculés : ils sont **justes aujourd'hui** (0,60 × 98,4 = 59,04 ; 0,60 × 8 712 = 5 227 ; 0,60 × 424,3 = 254,6 ; 0,60 × 402,3 = 241,4 ; total 219 354 ; sans la main-d'œuvre 208 509). Mais ils dérivent de `ratios_V3` et de `prix_unitaires_MAD` : **toute** modification de `data/` rend l'exercice faux **sans qu'aucun contrôle ne bouge**. Le test `d · les valeurs publiées sont celles de calc/` vérifie qu'une valeur attendue **figure** dans la page ; il ne peut pas voir un nombre en trop. R1, § 4.3. | Calculer la situation dans `calc/` (`situation_exercice_4` : 60 % des quantités de zone, les quatre lignes, les deux totaux) et l'injecter par variables, comme l'ont été les variantes des exercices 2 et 3 après la passe 1. |
| **M9 · Marges et chemin critique de la voie A sont faux dès qu'un décalage négatif est important, et le drapeau qui le détecte est ignoré.** | majeur | Sur les trois réseaux du § 2.1 de la passe 1, la **durée** est juste — mais : A(10)→B(1), déc. −10 → `marges = {A: 9, B: 9}`, `taches_critiques_voie_A = []` : **chemin critique vide sur un projet de 10 jours**, et la tâche qui fixe la durée se voit attribuer 9 jours de marge. Avec −20, la marge de A passe à **19 j**. A(2)→B(5), déc. −10 → chemin critique = {B} seul, A à 8 j de marge. Cause : le parcours arrière de `voie_A_parcours` ne borne la date au plus tard d'une tâche que par ses successeurs (`fin = min([tard[s][0] - dec …], default=duree)`) ; une tâche **ayant** un successeur n'est jamais bornée par la fin de projet. Le drapeau qui le dit, `les_deux_voies_designent_le_meme_chemin`, vaut **False** dans les trois cas — mais il n'entre pas dans `verdict`, aucun étalonnage ne l'assert, et `cpm_cas_ferme.py` ne contrôle que `duree` et `verdict`. Le réseau publié est une chaîne pure, donc les marges du module sont justes — **par choix de réseau, pas par construction**. `cpm.py` est la bibliothèque de planification de tout le cours (D2, D7). | `fin = min(duree, min([tard[s][0] - dec …], default=duree))`. Faire entrer `les_deux_voies_designent_le_meme_chemin` dans le `verdict`. Ajouter aux cas fermés le **chemin critique attendu**, et pas seulement la durée. |
| **M10 · La figure 2 est un enchaînement de blocs et de flèches sans contenu technique, qui duplique la figure 3 et la contredit.** | majeur | Sept rectangles, six flèches, aucune cote, aucune durée, aucune donnée — alors que la figure 3, deux paragraphes plus bas, montre **les mêmes sept tâches, dans le même ordre, avec leurs durées et leurs recouvrements**. Le § 8 est explicite : « **Interdit : schémas décoratifs, blocs et flèches génériques sans contenu technique** » et « un schéma qui n'apprend rien n'a pas sa place » ; c'est le défaut n° 4 du § 2.2 que le prompt interdit de reproduire. Et elle **contredit** la figure 3 : ses flèches disent un enchaînement strict fin-début, là où le module passe un encart entier à expliquer que FEP démarre avant la fin de COF. Les trois lignes de « Ce qu'il faut voir » sont bonnes — mais elles tiendraient sous la figure 3. | Supprimer la figure 2 et déplacer ses trois lignes de lecture sous le Gantt. Le module descend à 4 figures, ce qui reste au-dessus du minimum du § 8 et renforce les trois qui restent. |
| **M11 · `data/suivi.base_du_choix` justifie le cas par « un retard d'une demi-zone » ; le retard calculé est de 1,26 zone.** | majeur | `data/projet-gare.json` : « *un chantier en légère difficulté — quelques pour cent de dépassement de coût **ET un retard d'une demi-zone***. […] La valeur n'a PAS été ajustée pour obtenir un résultat ». Sortie réelle : `retard_en_zones = **−1,26**`, `SPI = **0,741**`. Un SPI de 0,74 au jour 19 d'un plancher de 32 jours n'est pas une « légère difficulté » : c'est près de **cinq jours ouvrés de retard** sur dix-neuf. Deux problèmes. (1) La justification d'un choix V3 est démentie par la sortie qu'elle justifie — personne n'a relu l'une contre l'autre. (2) Elle attribue le retard à `cout_reel_constate_MAD`, qui **n'entre pas** dans SPI : SPI ne dépend que de `zones_realisees_a_date` et de `avancement_zone_en_cours_pct`. Et le module, qui publie « SPI = 0,741 : l'avancement vaut 74 % de ce qui était planifié », **ne dit nulle part que c'est grave** ni ce qu'un chef de projet suivi en fait — alors que c'est le cœur de son métier. | Soit ramener le constat à ce que `data/` annonce (4,3 zones réalisées donneraient SPI ≈ 0,89, « une demi-zone »), soit réécrire la justification pour ce que le cas montre vraiment, et ajouter au § S6 le paragraphe qui manque : à SPI 0,74, qu'est-ce qu'on fait lundi matin. |
| **M12 · L'inventaire d'étais ne compte que les zones coffrées, alors que le module enseigne que les étais de reprise restent sous les zones décoffrées.** | majeur | `coherence_materiel` : `etais_necessaires = zones_coffrees_simultanement × surface × etais_par_m2 = 3 × 360 × 2,5 = **2 700**`, et le module publie « **2 700 étais**, puisque les étais de reprise restent sous les zones décoffrées » — la phrase dit exactement ce que le calcul ne fait pas. La tâche DEC s'appelle « **Décoffrage, étais de reprise maintenus** », la double lecture S7 en fait un point d'arrêt MOE (« contrôle […] la présence des étais de reprise ») et la figure 2 le répète : les zones décoffrées en gardent. Elles ne sont pas comptées. À une durée d'étaiement de reprise de ne serait-ce qu'un cycle après décoffrage, le besoin double. La passe 1 avait signalé le point (« *le décoffrage « étais de reprise maintenus » les immobilise plus longtemps encore* ») ; seul le parc de **tables** a été traité. | Porter dans `data/` la durée de maintien des étais de reprise (V3, avec fourchette), et compter `ceil((cycle + maintien)/cadence)` zones étayées. Ou, à défaut, écrire que le chiffre ne couvre que les zones coffrées — mais alors retirer le « puisque ». |
| **m1 · « jours ouvres » sans accent, sur l'axe de la figure 5.** | mineur | `assets/svgkit.js:285` : `texte(…, "jours ouvres", …)`, visible sur la capture `…-figure5.png`. Le dépôt porte pourtant un commit « Français accentué dans tout ce que le lecteur voit » (`c0b1d06`), et le contenu écrit bien « jours ouvrés » deux fois. | `"jours ouvrés"`. |
| **m2 · « moyenne 14.5 » : point décimal dans une figure, dans un module qui virgule tout le reste.** | mineur | `svgkit.js:312` : `moy.toFixed(1)` sans conversion. Le build convertit systématiquement `.` → `,` pour les variables (`substituerDans`) ; les textes SVG échappent à cette règle. Capture `…-figure4.png`. | Passer les nombres des figures par le même formateur que les variables. |
| **m3 · Figure 1 : la puce ① est posée sur une ligne de poutres, exactement comme la puce ②.** | mineur | `svgkit.js:365-367` : `puce(r.x(longueur_m * 1.5), …, 1)` et `puce(r.x(entraxe_poutres_m), …, 2)`. `1,5 × 15 = 22,5 m` est un multiple de 7,50 : la puce ① — légendée « **zone de coulage** » — surplombe une ligne de poutres, et la puce ② — légendée « **ligne de poutres** » — surplombe celle de la zone 1. Le contrôle du build (« chaque numéro figure dans la légende et inversement ») est satisfait, mais le repère ne désigne pas ce que la légende annonce. | Poser ① au centre d'une zone **hors** multiple d'entraxe (par exemple à `0,5 × longueur_zone`), ou l'accrocher au bord de zone avec un trait de rappel. |
| **m4 · « jour 19, soit la fin de la semaine 4 ».** | mineur | `semaine_arret = 19/5 = 3,8`, affiché par `f"{3.8:.0f}"` → « 4 ». À 5 jours ouvrés, le jour 19 est le **4ᵉ jour de la semaine 4** ; la fin de la semaine 4 est le jour 20. Sans conséquence de calcul, mais le module insiste sur la date d'arrêt comme **donnée**. | `f"le jour {j%5 or 5} de la semaine {ceil(j/5)}"`, ou simplement « jour 19 (semaine 4) ». |
| **m5 · `STATE.md` fait exactement 150 lignes sur 150 autorisées.** | mineur | `check.mjs` : `if (n > 150) E(...)`. Sortie : « 13.3 · STATE.md court — **150 lignes sur 150** ». La **prochaine ligne ajoutée** fait échouer `npm run check`, donc la reprise mode B et le commit du module suivant. Un contrôle de forme à marge nulle placé sur le chemin critique de la livraison. | Ramener `STATE.md` à ~135 lignes maintenant, ou faire du dépassement un avertissement plutôt qu'un échec. |
| **m6 · `data/materiel` recopie en prose des valeurs calculées ailleurs.** | mineur | `pompe_a_beton: "pompe automotrice, **30 m3/h** retenus (V3)"` double `cadences.betonnage_m3_h.valeur = 30`, et n'est lu par aucun script (`grep` : zéro occurrence hors `data/`). `tables_note` écrit « *trois zones se recouvrent à la cadence de **3,4 j** pour un cycle de **8,6 j** : il faut environ 3 × **424** m²* » — trois résultats de `calc/` figés dans une chaîne de caractères de `data/`. Deux sources de vérité pour la même grandeur, dont l'une ne sera jamais mise à jour. R1. | Retirer les nombres des notes de `data/` (« 30 m³/h » → « cadence lue dans `cadences.betonnage_m3_h` »), ou générer ces notes. |
| **m7 · Le signe « + » de la dérive est écrit en dur dans le tableau S6.** | mineur | `content` : `| Dérive prévue | **+{{valeur-acquise.derive_prevue_MAD::n0}} MAD** |`. La dérive est positive aujourd'hui (+175 732) ; à CPI > 1 elle serait négative et la page afficherait « **+−…** ». | Publier un `derive_signee` formaté par `calc/`. |
| **m8 · Gantt : formats de durée mêlés.** | mineur | Capture `…-figure3.png` : « 1,77 j », « 2,52 j », « 0,25 j », « 0,41 j » à côté de « **3 j** », « **2 j** », « **0,5 j** ». Les durées sont justes ; c'est la mise en forme qui change selon que la décimale tombe ou non. | Format fixe à deux décimales dans `svgkit.gantt`. |
| **m9 · Figure 1 « à la date d'arrêt » n'affiche que le constat.** | mineur | Le titre annonce « *à la date d'arrêt du suivi* ». La figure montre Z1–Z3 coulées, Z4 en cours, Z5–Z8 « à venir ». Le **prévu** à cette même date est de **4,86 zones** : Z5 devrait être aux deux tiers et Z6 au quart. Le tableau de bord le plus lisible du module tait précisément l'écart que le § S6 passe deux pages à établir. | Doubler le contour des zones prévues (ou tramer la fraction prévue), avec une entrée de légende. |
| **m10 · L'étalonnage de `valeur_acquise.py` est à 5/6 une vérification d'identités.** | mineur | `plancher_cas_ferme.py` lignes 66-75 : CPI = VA/CR, SPI = VA/VP, CV = VA−CR, SV = VA−VP, EAC×CPI = BAC — toutes recalculées **depuis les sorties de la fonction**. Canari **C5** (VA minorée de 20 %) : les cinq identités passent ; seul le sixième cas, « chantier parfaitement à l'heure et au budget → CPI = SPI = 1 », mord. L'étalonnage tient donc par un seul cas. *(Par contraste, la partie « a » du même fichier, pour `plancher.py`, est un vrai cas à solution fermée posé à la main : c'est la bonne méthode, et elle est dans le même fichier.)* | Ajouter un second cas externe non trivial : un avancement et un coût posés à la main pour lesquels CPI, SPI et EAC sont écrits d'avance. |

---

## 6. Grille du § 7.2, notée par moi

| Critère | Ma note | Appui |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | S2 justifie la zone par quatre propriétés simultanées ; l'encart « Pourquoi ceci n'est PAS un contre-calcul » et celui sur le contrôle qui échoue vont au-delà du § 7.1. |
| Les hypothèses sont explicites | **2** | Les trois familles de nombres sont distinguées et les 10 balises sont irréprochables — mais 32 % du cycle et 100 % du gain de recouvrement reposent sur cinq valeurs non déclarées (**M1**), et le registre omet les cadences et les prix (**M4**). |
| Les formules sont justifiées | **2** | La règle de cadence est publiée et démontrée, ce qui est un vrai progrès — mais elle est **incomplète** et c'est exactement là qu'elle casse (**B1**). |
| **L'exemple est vérifié** | **1** | **Sous le minimum.** La variante publiée dans deux exercices est infaisable (**B1**) ; l'histogramme contredit le Gantt sur 26 jours sur 33 (**B2**) ; le « constat » de la courbe en S est le plan remis à l'échelle (**B3**) ; le « recalcul indépendant » du béton est une copie des données (**M5**) ; six nombres d'un exercice sont tapés à la main (**M8**). |
| Le piège est identifié | **3** | Six pièges chiffrés, un piège par figure, et le piège que le module s'applique à lui-même. |
| Lien avec l'exécution | **3** | Double lecture entreprise/MOE, point d'arrêt modélisé en tâche critique, étais de reprise, critère de décoffrage renvoyé en ⏸. |
| Lien avec le coût et le délai | **3** | C'est l'objet du module, et la chaîne est complète de bout en bout. |

**Minimum de 2 partout : NON tenu** (« l'exemple est vérifié » à 1). L'auto-évaluation de
`QA/grilles-72.md` donne 3 partout ; je ne la retiens pas sur trois critères.

---

## 7. Contrôle des corrections annoncées à la passe 1

| Passe 1 | État réel |
|---|---|
| **B1** chiffre faux « 40 % » | **corrigé** — 15,2 %, variabilisé, plus un canari de build qui attrape la concaténation. |
| **B2** corrigés d'exercice faux | **non corrigé sur le fond.** L'arithmétique est maintenant produite par `calc/`, mais le **modèle** est faux et la recommandation d'ingénierie est de nouveau renversée — dans l'autre sens cette fois (**B1** ci-dessus). *La passe 1 a elle-même validé la valeur fautive de 2,4 j : l'erreur a survécu aux deux passes.* |
| **B3** courbe en S contradictoire | **corrigé sur le point d'arrêt** (point ajouté, écart vertical = SV, testé) — **mais la correction a introduit B3 (nouveau)** : les vingt autres points du constat sont fabriqués. |
| **B4** moteur CPM | **corrigé sur les durées** (vérifié sur les trois réseaux) — **non corrigé** sur les marges et le chemin critique (**M9**) ni sur la phrase publiée (**M2**). |
| **M1** chaîne des durées non gardée | **corrigé** — les quatre durées sont recalculées depuis `data/`, T2 sonne. |
| **M2** explication du contrôle de main-d'œuvre | **corrigé, et bien** — les causes sont chiffrées une à une et le module conclut « cet écart n'est pas expliqué ». |
| **M3** contre-calcul n° 1 | **corrigé, et bien** — la plage qui passe et le « 26,7 % de la fourchette » sont publiés. |
| **M4** nombres tapés à la main | **corrigé** pour les cadences et les prix — **rouvert** ailleurs (**M8**, **M3**). |
| **M5** repère « X » | **corrigé**, avec canari de build. |
| **M6** parc de coffrage | **corrigé pour les tables** (1 300 m², contrôle `coherence_materiel`) — **non corrigé pour les étais** (**M12**), et le contrôle ne sait sonner que grâce à **B1**. |
| **M7** vérification dimensionnelle | **corrigé** — `verif_unites.py` couvre les 4 bibliothèques, avec contre-contrôles qui lèvent. |
| **M8** étalonnage | **corrigé** pour `plancher.py` (cas fermé réel) ; **partiellement** pour `valeur_acquise.py` (**m10**). |
| **M9** tolérance de 1 % | **corrigé, et bien** — le recoupement physique poste par poste, le contre-exemple à −5 %, et la leçon sur les seuils sont le meilleur passage du § S6. |
| **m1** traits sur les libellés | **corrigé** (traits interrompus dans la bande centrale). |
| **m2** légende du Gantt | **corrigé** (« les sept tâches sont critiques — la couleur ne distingue donc rien »). |
| **m3** formule de durée totale | **corrigé** ((n−1) × cadence + cycle, testé). |
| **m4** grille § 7.2 | **produite** — mais elle note 3 ce que je note 1 (§ 6). |
| **m5** règle de cadence non publiée | **corrigée** — publiée et démontrée… et c'est en la publiant qu'on voit qu'elle est incomplète (**B1**). |
| **m6** captures | **corrigé** — les cinq figures sont capturées et conservées. |
| **m7** calcul obscurci | **corrigé**. |

**12 corrections tiennent, 3 ne tiennent pas, 2 ont introduit un défaut nouveau.** Les deux
régressions sont du type annoncé dans la consigne : une correction ajoutée (le point de la courbe en
S à la date d'arrêt) a rendu vert un test tout en laissant la figure fausse ailleurs, et une règle
publiée pour répondre à un mineur a exposé un bloquant qui dormait.

---

## 8. Synthèse

| Gravité | Nombre |
|---|---:|
| **Bloquant** | **3** (B1, B2, B3) |
| **Majeur** | **12** (M1 à M12) |
| **Mineur** | **10** (m1 à m10) |
| **Total** | **25** |

### Zéro bloquant ? **NON.**

Trois bloquants, tous dans la même zone : **ce qui est publié à partir du planning**. Les quantités,
les durées élémentaires, le cycle, le coût et les indicateurs de valeur acquise, je les ai tous
recalculés et ils sont justes. Ce qui ne l'est pas, c'est tout ce qui dérive de la **cadence de
rotation** et de la **répartition dans le temps** : la variante des exercices, l'histogramme
d'effectifs, la courbe de constat.

### Ce module peut-il servir de modèle à la duplication ?

**Pas en l'état — mais oui après correction des trois bloquants, et sans réserve sur la forme.**

Ce qu'il faut garder tel quel, et dupliquer : la discipline des trois familles de nombres (géométrie
/ ratio / hypothèse de chantier) ; l'habitude de dire **ce qu'un contrôle ne prouve pas** et **sur
quelle largeur il tient** ; le refus d'habiller un contrôle qui échoue (§ S4c) ; la double lecture
entreprise/MOE ; la fiche mémo. Le § S6 sur les seuils et le bruit est au-dessus de ce que le § 7.2
exige, et c'est le passage que les autres modules devraient imiter.

Ce qu'il ne faut **pas** dupliquer avant de l'avoir réparé : la fabrique des figures. Trois des cinq
figures ont un défaut de fond — l'une est décorative (**M10**), l'une n'a pas d'échelle (**M7**),
l'une trace une donnée inventée (**B3**) — et la chaîne de contrôle ne voit rien, parce qu'elle
vérifie les chevauchements de textes et la non-vacuité des pixels, jamais **ce que la figure
prétend montrer**. Si ce gabarit est dupliqué sur quarante modules, ce défaut-là se duplique
quarante fois. C'est, à mon avis, la décision la plus importante à prendre avant l'étape 3 : ajouter
à la recette des figures un contrôle de cohérence **figure contre calcul** (l'histogramme contre les
dates du Gantt, la courbe de constat contre les relevés), au même titre que celui qui existe déjà
pour la section d'armatures du socle.

### Lui manque-t-il un modèle 3D ?

**Non — l'absence de 3D est le bon choix, et le module a raison de le défendre.** Rien dans ce
module n'est tridimensionnel : la zone est un rectangle, le cycle est un axe du temps, la valeur
acquise est un rapport. Une cage d'armatures en 3D n'apprendrait rien **ici** (elle appartient à B3),
et le phasage 3D appartient à C3. Le § 6.2 dit que la 3D n'est jamais ajoutée pour cocher une case :
c'est appliqué.

**Mais il manque une figure, et ce n'est pas une 3D.** Le module publie une cadence de 3,41 j, un
cycle de 8,56 j, trois zones qui détiennent du coffrage en même temps et une pointe d'effectif — et
**aucune figure ne montre les huit zones se recouvrant dans le temps**. Le Gantt ne montre qu'une
zone ; l'histogramme, qui devrait le montrer, est faux (**B2**). Un diagramme de rotation — huit
barres décalées de 3,41 j, avec la bande de coffrage immobilisé hachurée et la ligne du parc déclaré
— rendrait visibles d'un coup d'œil la cadence, le recouvrement, la contrainte de parc et l'erreur
de **B1**. C'est la figure que je demanderais avant toute 3D.

---

*Relecture hostile, § 12.2 et Annexe 4. Aucun « RAS » ci-dessus n'est donné sans preuve. Les scripts
de recalcul et les copies jetables du dépôt sont dans
`/tmp/claude-0/-home-user-mine/70713aa8-3622-5c6d-a7c2-bce4a8b25d73/scratchpad/`. Le dépôt
`/home/user/mine` n'a été modifié qu'en `QA/`.*
