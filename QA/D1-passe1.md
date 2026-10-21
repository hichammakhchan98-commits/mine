# D1 — Métrés, prix, sous-détails et situations · passe adversariale n° 1

Relecteur hostile, indépendant de l'auteur. Livrable relu : `content/03-d1-metres-prix.md`,
`modules/03-d1-metres-prix.html`, `calc/prix.py`, `calc/sorties/prix.json`, les cinq captures,
`data/projet-gare.json` (version **commitée**, `HEAD:269ea6f`).

> **Avertissement sur l'état du dépôt, et sur B1.** Cette passe a commencé sur un arbre de travail
> **non propre** : `calc/prix.py`, `calc/tests/test_prix.py`, `content/03-d1-metres-prix.md`,
> `assets/svgkit.js` et **`data/projet-gare.json`** — jeu déclaré FIGÉ en 1.0 — portaient des
> modifications non commitées du module D4 en cours d'écriture, et `npm run check` était **rouge**.
> J'ai donc relu la version commitée de D1 (`269ea6f`). **Pendant la passe**, ce travail a été
> committé (`f562459` « D4 — Suivi et contrôle, **et une incohérence D1 corrigée au passage** »,
> décision D-039) : le contrôle est repassé au vert et **le bloquant B1 est désormais corrigé**.
> Je le maintiens dans ce rapport — c'est un défaut de D1 tel que livré, trouvé indépendamment et
> chiffré — mais il ne demande plus de correction. **Les six autres bloquants subsistent sur l'état
> actuel du dépôt** : je les ai tous revérifiés après `f562459`.

---

## 0 · Contre-expertise à l'aveugle

Cinq valeurs recalculées depuis `data/projet-gare.json` seul, **avant** toute lecture de
`calc/prix.py`, par un script jetable
(`/tmp/claude-0/-home-user-mine/70713aa8-3622-5c6d-a7c2-bce4a8b25d73/scratchpad/blind.py`).
Quantités et durées reprises des sorties de **D2** (module déjà relu), jamais de D1.

### 0.1 Un poste unitaire : POTR, un poteau de RDC de 9 m

| Ligne | Mon calcul |
|---|---:|
| Béton `0,25 × 9 = 2,25 m³` × 1,05 pertes × 900 | 2 126,3 |
| Acier `130 kg/m³ × 2,25 = 292,5 kg` × 11,5 | 3 363,8 |
| Coffrage `4 × 0,50 × 9 = 18 m²` × 38 | 684,0 |
| Main-d'œuvre `8 × 6 / 3 = 16,00 h/u` × 49,17 MAD/h (atelier : 1 chef + 2,5 qualifiés + 2,5 manœuvres) | 786,7 |
| Matériel (vibreur + pompe) | 38,9 |
| **Déboursé sec** | **6 999,5 MAD/u** |
| Prix de vente × 1,17 | 8 189 |

Publié : `pu_de_vente_MAD = 8 145,31`, soit DS **6 962,7**. **Écart +0,53 %** — il tient
entièrement à la ligne de pompe que j'ai comptée et que D1 ne compte pas (voir M10). **Concordant.**

### 0.2 Le total du bordereau et le coût au m²

| | Mon calcul | Publié | Écart |
|---|---:|---:|---:|
| Déboursé sec | 64 505 804 | 63 839 457 | **+1,04 %** |
| Prix de vente | 75 471 791 | 74 692 165 | +1,04 % |
| Coût au m² d'emprise | 15 723 | 15 561 | +1,04 % |

Écart entièrement décomposé : +497 k de main-d'œuvre que j'avais ajoutée aux forfaits d'entreprise
(D1 a raison de ne pas le faire, et le dit bien — § S2) ; +236 k de frais de durée (j'ai compté
**18 mois calendaires**, D1 compte 17,28 mois ouvrés — voir **M1**, c'est moi qui ai raison) ;
−74 k de nacelle (D1 a raison) ; +7 k de pompes. **Concordant**, et les deux écarts résiduels sont
eux-mêmes des défauts localisés.

Lot par lot, ma reconstruction recoupe la sienne à moins de 0,2 % sur les dix lots.

### 0.3 Le net d'une situation mensuelle

Même ordre d'opérations (travaux → révision → retenue → remboursement d'avance) :

| | Mon calcul | Publié | Écart |
|---|---:|---:|---:|
| Travaux cumulés | 21 632 186 | 21 503 787 | +0,60 % |
| Coefficient de révision `0,15 + 0,60×1,062 + 0,25×1,118` | 1,0667 | 1,0667 | 0 |
| Montant révisé | 23 075 053 | 22 938 089 | +0,60 % |
| Retenue 7 % | −1 615 254 | −1 605 666 | — |
| Remboursement d'avance `(28,7−20)/60 × 7,47 M` | −1 089 638 | −1 094 226 | — |
| **Net cumulé** | **20 370 161** | **20 238 198** | **+0,65 %** |

**Concordant** sur l'arithmétique. L'arithmétique n'est pas le problème : **la date de cette
situation l'est** (bloquant B1), et l'attachement qu'elle est censée illustrer n'y entre pas (B6).

### 0.4 Le besoin de trésorerie maximal

| | Valeur | % du marché |
|---|---:|---:|
| Mon calcul (encaissements au mois +2, profil mensuel) | 4 875 432 | 6,5 % |
| **Publié** | **15 357 028** | **20,56 %** |
| Algorithme **de D1 rejoué** avec le délai de paiement converti en jours ouvrés | 9 922 839 | 13,28 % |

**Écart ×3,2 — non justifié.** J'ai reproduit l'algorithme publié au dirham près (15,29 M contre
15,36 M, l'écart tenant à mon interpolation) et isolé la cause : **60 jours calendaires ajoutés à
une échelle de jours ouvrés** (bloquant B3). À elle seule elle gonfle le besoin de **+55 %**. Le
reste de l'écart avec mon chiffre vient de ma grille mensuelle contre leur profil continu, et de la
révision que D1 n'applique pas aux encaissements alors qu'il l'applique à la situation.

### 0.5 Le coût d'un mois de retard

| | Mon calcul | Publié | Écart |
|---|---:|---:|---:|
| Frais indexés sur la durée | 328 000 | 328 000 | 0 |
| Pénalités (30 j calendaires / 31,6 j publiés) | 2 264 154 | 2 359 805 | +4,2 % |
| **Total** | **2 592 154** | **2 687 805** | **+3,7 %** |

**Concordant.** L'écart tient au facteur ouvré→calendaire : D1 utilise 1,504, qui **inclut les
intempéries**, alors que la même conversion est refusée aux frais de durée (**M1**).

---

## 1 · Défauts

### Bloquants

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **B1 · La situation n° 7 décrit l'état du jour 59, et se déclare au septième mois.** *(corrigé en vol par `f562459`, voir l'avertissement de tête — vérifié : la situation est désormais la n° 4 au jour 84, 34,8 % déclarés contre 35,7 % au réseau.)* L'avancement déclaré est posé à la main dans `data/` (27 pourcentages) et n'est **jamais confronté au réseau de D2** — la règle que STATE.md déclare absolue depuis la TV : « toute grandeur d'état est dérivée du réseau et un test refait la dérivation ». Au jour 147 (7 × 21), le réseau donne POTR, MEZZ, NOYX, ETAN, CHFA, CHAP, MARQ, PSOU, QUAI **tous à 100 %** ; la situation les déclare à 60, 25, 15, 40, 70, 0, 0, 0, 0. Le chantier déclaré vaut 51,6 % de moins que le chantier planifié. | **bloquant** | Recalcul § 0.3 étendu : travaux déclarés 18 817 193 MAD (25,2 % du marché) contre **38 536 411 MAD (51,6 %) au réseau**. Par dichotomie sur le profil du réseau, **l'état déclaré est celui du jour 59, soit 2,8 mois**. Le `_role` du bloc le dit lui-même : « au même instant d'arrêt que le suivi du module TV » — or `tranche-plancher.json → suivi.jour_arret = 19` sur un MEZZ qui démarre au jour 45,8, soit **jour 64,8 du chantier**. La seule ligne prise à l'horloge, `FRAIS-DUREE`, est donc attachée à 7 mois (40,5 %) pour un chantier physique à 18 % : **2 686 594 MAD facturés au lieu de ≈ 1 187 000**. Confirmation indépendante : `git diff calc/prix.py` (travail D4 non commité) — « la situation annonçait sept mois écoulés pour un état de chantier correspondant au deuxième ». | Dériver l'avancement déclaré de l'état du chantier à une date d'arrêt unique et déclarée (c'est ce que D4 entreprend). En attendant : ramener `mois_ecoules` à 3,1 et republier. Situation corrigée : travaux 20,0 M, net **≈ 19,0 M** au lieu de 20 238 198 (**−6,1 %**). **Et** ajouter le test qui manque : `|avancement_declare − avancement_du_reseau_a_la_date_d_arret|` borné, ou l'écart publié et commenté comme un retard de 4,2 mois — qui vaudrait, aux chiffres du § S4h du module lui-même, environ 11 MMAD. |
| **B2 · Le contre-calcul des deux voies ÉCHOUE sa propre tolérance, et le module le présente comme expliqué.** `ecart_pct = −22,32` pour `tolerance_pct = 20,0` ; `calc/` rend `"verdict": "ECART"`. Le module (§ S3d) écrit « Écart : −22,3 %, pour une tolérance déclarée de 20 % », puis explique longuement pourquoi la tolérance de 5 % du § 3.3 ne s'applique pas — **sans jamais dire que la tolérance de 20 %, elle, est dépassée**. La justification du calcul dit pourtant : « Un écart de 20 % entre un prix construit et un prix de marché est normal ; **au-delà, l'un des deux est faux**. » | **bloquant** | `calc/sorties/prix.json → ecart_des_deux_voies.verdict = "ECART"`. `grep -n "verdict\|ECART" content/03-d1-metres-prix.md` : la chaîne « ECART » n'apparaît nulle part dans le contenu. `calc/tests/test_prix.py` teste le périmètre, la somme et le signe de l'écart — **jamais le verdict**. | Publier le verdict. Soit l'écart est acceptable et la tolérance est à relever **avec sa raison**, soit il ne l'est pas et le module doit dire lequel des deux chiffrages il tient pour faux. Ajouter au test : `assert ecart["verdict"] == "OK"`, et un canari qui le fait rougir. |
| **B3 · La trésorerie additionne des jours ouvrés et des jours calendaires.** `tresorerie()` parcourt `j` en **jours ouvrés** (l'axe de la figure 5 est légendé « jours ouvrés ») et teste `if depot + delai > j` avec `depot = mois × 21` (ouvrés) et `delai = 60` (**calendaires**, « du dépôt de la situation à l'encaissement »). Chaque encaissement est donc retardé de 60 jours ouvrés ≈ 84 jours calendaires, soit 40 % de trop. | **bloquant** | `calc/prix.py` l. 790-797. Rejeu § 0.4 : besoin **15,29 M** avec le code publié, **9,92 M** avec `delai` converti en jours ouvrés (`60 × 362,92/546 = 39,9 j`) — **+54 % d'inflation**. Le pic publié (jour 78) est l'artefact direct : la courbe bleue reste plate 84 jours ouvrés avant le premier encaissement. Ironie : c'est le module qui enseigne au § S4h que « les pénalités se comptent en jours calendaires, les frais de durée en jours ouvrés ». | Convertir le délai de paiement en jours ouvrés avant de l'ajouter, ou porter toute la trésorerie sur un axe calendaire. Republier besoin, pourcentage, jour du pic, la figure 5, les deux reprises en S5 et S7, et la fiche mémo. Ajouter un contrôle d'homogénéité : toute somme de deux durées vérifie qu'elles sont dans le même calendrier. |
| **B4 · Le seul ratio tous-corps-d'état du projet rend un verdict VERT sur une base où il n'est pas défini.** `controle_ratios.cout_par_m2_emprise` : `ratio_defini_sur_cette_base = true`, `dans_la_fourchette = true` (15 560,9 dans 7 000–16 000). Or la note du ratio dans `data/` dit : « tous corps d'état, **hors VRD et hors interfaces ferroviaires** » — et le bordereau contient le lot « **6 · Interfaces ferroviaires** » (PSOU + QUAI), 6 800 000 MAD, **10,65 %** du déboursé. De plus la base est l'**emprise** (4 800 m²) et non la surface de plancher (4 800 + 2 880 mezzanine + 800 niveau technique = 8 480 m²). C'est exactement la faute que le § S4e consacre une page à dénoncer et que D-037 prétend avoir corrigée. | **bloquant** | `data/projet-gare.json → ratios_de_controle.cout_MAD_m2_batiment_voyageurs.note`. `bordereau.par_lot["6 · Interfaces ferroviaires"].part_pct = 10,65`. Hors interfaces : `(63 839 457 − 6 800 000) × 1,17 / 4 800 = 13 903 MAD/m²` ; sur la surface de plancher : **8 808 MAD/m²**. Le chiffre publié est à **97 % du plafond** de la fourchette. | Retirer le lot 6 du numérateur, nommer la surface (emprise ou plancher) et la rendre explicite dans le libellé du ratio, ou passer `ratio_defini_sur_cette_base = false` comme le module le fait pour la part de main-d'œuvre. Le contrôle doit comparer la liste des lots du bordereau à la liste des exclusions écrites dans la note du ratio, et **refuser** le verdict si l'une est présente. |
| **B5 · D-036 n'est pas appliquée : aucun coût n'est publié avec ses bornes.** La décision D-036 du 20/10 dit mot pour mot : « Tout module qui publie une date ou une durée de projet publie aussi les deux bornes […] **le même traitement est attendu de D1 sur les coûts**. » D1 publie un total unique, un coût au m² unique, un besoin de trésorerie unique et un coût de retard unique, tous issus de 148 hypothèses V3 déclarées avec leur fourchette — le défaut même que le module reproche aux bordereaux qu'il critique (« un ratio hors fourchette est une question »). | **bloquant** | `grep -n "borne\|aux bornes" content/03-d1-metres-prix.md` → aucun résultat. Aucun équivalent de `variante_aux_bornes` dans `calc/prix.py`. Estimation (script `bornes.py`) : forfaits [22,2 ; 51,6] M, frais de durée [3,8 ; 8,2] M, postes unitaires ×0,64 à ×1,57 → **DS ×0,65 à ×1,52 ; PV ×0,60 à ×1,69**, soit un coût au m² de **9 283 à 26 260 MAD/m²**. La borne haute sort largement de la fourchette de contrôle 7 000–16 000 : la valeur unique publiée masque une distribution qui échoue au contrôle sur une bonne part de son étendue. | Ajouter `variante_aux_bornes` sur le modèle de D2 et publier la fourchette partout où un coût est publié : S4b, S4g, S4h, la fiche mémo. Un montant de marché sans ses bornes, dans un module qui n'a aucun bordereau réel, est une fausse précision. |
| **B6 · Le paramètre `ecart_attachement` est déclaré dans `data/`, porte la leçon centrale du module, et n'est lu nulle part.** `situation_exemple.ecart_attachement` : poste FOUI, +9 % (fourchette 0–20), avec sa leçon — « La quantité payée est celle de l'attachement contradictoire, pas celle du métré d'étude. Un métré juste qui n'est pas attaché ne se paie pas. » La ligne FOUI de la situation publiée porte `quantite_attachee = 3 520,0`, c'est-à-dire **exactement le métré**. La figure 4 et le § S5 enseignent le contraire de ce que le calcul fait. | **bloquant** | `grep -rn "ecart_attachement" --include=*.py --include=*.js --include=*.md .` → **0 occurrence hors du fichier de données**. `situation.lignes[FOUI].quantite_attachee = 3520.0` contre `3520 × 1,09 = 3 836,8 m³`, soit **+30 258 MAD** non facturés. Règle de STATE.md : « tout paramètre déclaré est relu dans le résultat qu'il engendre ». | Appliquer l'écart d'attachement à la ligne FOUI, afficher les deux quantités côte à côte dans le tableau du § S4f (métré / attaché), et ajouter le contrôle générique qui manque : **toute clé de `data/` non lue par un `calc/` échoue le build**, comme les V3 non registrées le font déjà. |
| **B7 · La légende de la figure 5 affirme ce que son propre dessin contredit, dans la phrase suivante.** Puce 1 : « quand la bleue repasse devant — ici entre les jours 180 et 230 — c'est l'inverse ». Puce 2 : « Le décrochement initial de la courbe bleue est l'avance de 10 % : **c'est le seul moment où l'entreprise est devant**. » Les deux affirmations sont dans la même légende et s'excluent. | **bloquant** (critère de la passe : une légende qui affirme ce que le dessin ne montre pas) | `tresorerie.points` : `besoin_MAD < 0` de `j = 0` à `j = 24` **et** de `j = 186` à `j = 228`. Capture `03-d1-metres-prix.html-figure5.png` : la courbe bleue pointillée est nettement au-dessus de la rouge sur toute la plage 185–230. C'est la famille exacte du bloquant B4 de la passe D2 (« une légende qui commentait un palier qui n'était pas celui-là »). | Supprimer « le seul ». Mieux : faire produire par `calc/` la liste des intervalles où `besoin_MAD < 0` et l'injecter par variable, pour qu'aucune des deux phrases ne reste écrite à la main. |

### Majeurs

| Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|
| **M1 · Les frais indexés sur la durée sont comptés sur 17,28 mois ouvrés, pendant que les pénalités sont converties avec les intempéries.** Un encadrement, une base-vie et une location de grue se paient au **mois calendaire**, intempéries comprises — c'est la thèse même du module (« des frais qui continuent de courir pendant que rien ne se construit »). D2 publie `duree_ouvree_avec_intemperies_j = 389,9` et `mois_calendaires = 18,0` ; D1 prend `362,92 / 21 = 17,28`. Le même chantier est donc converti en calendrier de deux façons selon qu'il s'agit de dépenser ou de pénaliser. | majeur | `calc/prix.py → frais_de_duree()` : `mois = duree_j / jours_ouvres_par_mois` avec `duree_j = 362,92`. `cout_du_retard()` : `ratio = semaines_calendaires × 7 / duree_j = 1,504`, où `semaines_calendaires = 78` **inclut** les 26,9 j d'intempéries. Manque : `328 000 × (18,0 − 17,28) = 236 000 MAD`, et davantage si l'on retient 18,57 mois (389,9/21). | Une seule conversion, déclarée une fois : les frais de durée courent sur la durée **calendaire avec aléas** publiée par D2. Republier le total, la part du lot 9, le coût au m², la situation et la trésorerie. Ajouter un test qui compare la durée vue par D1 à celle publiée par D2. |
| **M2 · `part_gros_oeuvre` : verdict hors fourchette, base non interrogée, explication narrative.** `constate = 19,88 %`, `ratio_defini_sur_cette_base = true`, `dans_la_fourchette = false`. Le dénominateur est le bordereau entier, lot 6 « Interfaces ferroviaires » (10,65 %) et lot 9 « Frais de durée » (8,88 %) compris. La légende de la figure 2 tranche en prose : « ce bâtiment est plus un ouvrage d'enveloppe et de systèmes qu'un ouvrage de béton » — alors que l'exercice 3 du même module enseigne qu'« un ratio hors fourchette est une **question**, jamais une conclusion ». | majeur | `controle_ratios.part_gros_oeuvre`. Hors interfaces ferroviaires : `12 691 786 / 57 039 457 = 22,25 %` → **dans** la fourchette 22–40. Le verdict bascule avec la base, et rien dans le module ne le signale. | Interroger la base avant de conclure, comme le module l'exige partout ailleurs : publier les deux lectures (avec et sans interfaces) et laisser le lecteur voir que le verdict dépend du périmètre. C'est un meilleur enseignement que la narration. |
| **M3 · Le facteur de recalage ×2,52 est une moyenne non pondérée, prise là où elle n'est pas mesurée, puis appliquée partout.** Les cinq facteurs (0,78 · 4,25 · 1,93 · 4,08 · 1,57) sont moyennés sans pondération. Or **RADT et PHNT partagent la même cadence** (`dalle_pleine_m2_j_atelier`), comptée deux fois : elle pèse 40 % de la moyenne. Et **le terrassement est absent** alors que `productivites_par_compagnon_et_par_jour.terrassement_m3` est déclaré en V3, registré, cité dans la liste S4b du module — et jamais lu. Le facteur est ensuite appliqué à **toutes** les cadences dans `variante_recalee`, y compris charpente, couverture et façade, pour lesquelles aucune productivité de référence n'existe. | majeur | `coherence_cadences()` : `cas` ne contient que FOND, RADT, VOIL, PHNT, POTR ; `facteur_de_recalage_moyen = sum/len`. Mon recalcul du terrassement : `8 × 4 / 450 = 0,0711 h/m³ = 0,00889 j·compagnon/m³` contre une référence de `1/110 = 0,00909` → **facteur 1,02**, parfaitement crédible. En dédoublonnant la cadence de dalle et en ajoutant le terrassement : moyenne **≈ 1,9** au lieu de 2,52. D-038 et la dette n° 10 de STATE.md reposent sur le 2,52. | Pondérer par les jours-compagnon ou par le déboursé de chaque poste ; dédoublonner par **cadence** et non par poste ; ajouter TERR/FOUI puisque leur référence est déclarée ; et publier la sensibilité du facteur à ces choix. Un chiffre qui varie de 1,9 à 2,5 selon une convention non écrite ne peut pas solder une dette. |
| **M4 · Les « productivités par métier » de la figure 3 ne distinguent pas les métiers.** L'hypothèse (« les trois métiers se partagent les jours-compagnon au prorata du temps qu'ils prendraient à la productivité de référence ») est **circulaire** : la productivité implicite de chaque métier redonne mécaniquement le facteur du poste. La légende affirme pourtant tenir un diagnostic métier : « sa cadence implique de poser 637 kg d'acier par compagnon et par jour ». | majeur | RADT : `637,4/150 = 4,249` · `76,8/18 = 4,267` · `51,0/12 = 4,250` — les trois métiers rendent le même nombre, qui est `facteur_de_recalage = 4,25`. Idem sur les cinq postes. L'hypothèse n'est écrite que dans un **commentaire de `calc/prix.py`** (l. 500-502), nulle part dans le module (R6). | Déclarer l'hypothèse dans le module, ou abandonner l'affichage par métier et ne publier que le facteur du poste. Le § S4e promet « seule une productivité individuelle le dit » : en l'état le modèle n'en produit pas une. |
| **M5 · La ligne « divers de chantier » de 28,7 % est diagnostiquée puis jamais intégrée, et rien ne le déclare.** Le § S4d établit qu'il manque 28,7 % de divers pour recoller aux prix de marché ; le § S4c en fait un **risque d'exécution**. Tous les montants publiés — bordereau, coût au m², trésorerie, coût du retard, fiche mémo — restent calculés **sans** cette ligne. | majeur (R6) | `ecart_des_deux_voies.divers_necessaire_pct = 28,7`. Aucune ligne « divers » dans `bordereau.postes`. Aucune mention dans la liste des simplifications de STATE.md. | Soit ajouter la ligne et republier, soit écrire noir sur blanc que le bordereau publié est sous-estimé de l'ordre de 28,7 % sur ses postes décomposés, et porter la simplification dans STATE.md. Un module qui démontre qu'il lui manque une ligne ne peut pas publier ses totaux comme si elle y était. |
| **M6 · La figure 4 est une file de sept boîtes génériques sans une seule donnée.** Son contenu est une liste de chaînes **écrite en dur** dans `figures()`. Elle ne porte ni délai, ni montant, ni date, ni quantité. Le § 8 l'interdit explicitement (« blocs et flèches génériques sans contenu technique ») et le § 2.2 en fait le défaut n° 4 de l'ancienne version. Sa légende cite « 60 jours » que le dessin ne montre pas. | majeur | `calc/prix.py → figures()` : `"situation": ["Constat contradictoire sur site", …]`. Capture `…-figure4.png` : sept rectangles identiques, numérotés, aucune grandeur. Violation R1/R2 (« aucun nombre technique n'est tapé à la main », « génération, pas dessin à la main »). | Porter la séquence dans `data/` avec les délais de chaque étape et le montant de la situation, et la dessiner comme une **frise de temps** : constat → attachement → dépôt → visa → ordonnancement → paiement à J+60. La figure dirait alors ce que la légende promet, et expliquerait la trésorerie du § S4g. |
| **M7 · « Se tromper d'un cinquième » est un chiffre que rien ne produit.** L'encart du § S4g écrit : « L'écart maximal entre les deux est de **24,7 points** au jour 260. Prendre l'une pour l'autre, c'est se tromper **d'un cinquième** sur un besoin de financement. » Aucun calcul ne relie l'écart des deux courbes à un besoin de financement, et 24,7 points ne valent un cinquième d'aucune des bases en présence. | majeur (R7/R8) | `ecart_depense_travail.ecart_maximal = {j: 260, depense_pct: 73,41, travail_pct: 48,7, ecart_pts: 24,7}`. 24,7/100 = un quart ; 24,7/73,41 = un tiers ; 24,7/48,7 = la moitié. Aucune n'est un cinquième. La série `figures.depense_contre_travail` est par ailleurs construite et **jamais dessinée**. | Calculer la trésorerie sur le profil de travail et publier l'écart réel des deux besoins — c'est trois lignes de code et cela transformerait une affirmation en démonstration. À défaut, retirer la phrase. |
| **M8 · L'exercice 4 annonce quatre erreurs, en contient trois, en manque une, et son troisième point se contredit en deux lignes.** Énoncé : « **Quatre** choses ne vont pas. Lesquelles ? ». Le corrigé donne : (1) acier au prix posé — vraie erreur ; (2) heures du m² au m³ — vraie erreur ; (3) « **Le coffrage de 8 m²/m³ ne correspond à rien de déclaré** » puis, deux lignes plus bas, « celle-ci est **juste** » ; (4) frais de chantier 12 % — vraie erreur. Soit trois erreurs. Et une quatrième, réelle, n'est pas relevée : **le béton est compté à 900 MAD/m³ sans les 5 % de pertes** que le sous-détail du § S4a applique. | majeur | `content/03-d1-metres-prix.md`, exercice 4. Le sous-détail de référence du § S4a porte « 5 % de pertes sur 0,25 m » ; la ligne « Béton prêt à l'emploi 900 MAD/m³ » du sujet ne les porte pas (il faudrait 945). Un titre en gras contredit par son propre corps : famille des trois derniers bloquants de la TV. | Corriger l'énoncé (« trois choses ne vont pas, une quatrième ligne est correcte : trouvez-les ») ou ajouter les pertes de béton comme quatrième erreur. Et réécrire le titre du point 3 : « Le coffrage de 8 m²/m³ **est juste** — et c'est le piège ». |
| **M9 · Un seul canari pour cinq verdicts publiés.** STATE.md : « chaque contrôle rendant un verdict porte son canari rouge ». D1 publie au moins cinq verdicts (coût au m², part de main-d'œuvre du béton armé, part du gros œuvre, écart des deux voies, besoin de trésorerie) et `test_prix.py` ne porte **qu'un** canari, sur la somme `a+b+c=1`. Aucun des bloquants B1 à B7 n'est vu par les 34 vérifications du test. | majeur | `git show HEAD:calc/tests/test_prix.py | grep canari` → une occurrence. Les 34 `verifie(...)` sont tous des contrôles de cohérence interne : ils reconstruisent le calcul, jamais son modèle. | Un canari par verdict : fausser la base d'un ratio, inverser retenue et révision, décaler d'un mois l'avancement déclaré, ajouter un jour calendaire à un jour ouvré — et vérifier que le contrôle rougit. |
| **M10 · Quatre hypothèses de modèle ne sont déclarées nulle part.** (a) Le coefficient `pompe_j_par_m3`, déclaré dans `data/` et registré en V3, n'est appliqué qu'à **RADT et PHNT** : FOND (170 m³), VOIL (96 m³) et POTR (153 m³) sont coulés sans aucun moyen de mise en place, sans un mot. (b) La trésorerie suppose que l'entreprise **paie tous ses fournisseurs et sous-traitants comptant, le jour du travail** — l'hypothèse qui pèse le plus lourd sur le besoin, et la seule que l'encart `hypothese_de_profil` ne mentionne pas. (c) Les encaissements de la trésorerie ne sont **pas révisés** alors que la situation l'est (+6,67 %). (d) Les heures de MEZZ sont payées au taux de l'atelier « fondations » alors qu'elles viennent de quatre équipes différentes du module TV. | majeur (R6) | (a) `consommations()` : `engs = [_eng(d,"vibreur_j",…)]` pour FOND, VOIL, POTR. (b,c) `tresorerie()` : `decaisse = ds × frac_avancement(j)` et `encaisse = avance + cum × (1−rg) − avance × fr`, sans coefficient de révision. (d) `_mezzanine()` : `taux = taux_horaire_atelier(d, "fondations")`. | Déclarer les quatre dans le module **et** dans STATE.md, ou les corriger. (b) est de loin la plus importante : avec 60 jours de crédit fournisseur, le besoin de trésorerie publié s'effondrerait. |
| **M11 · D4 a été ouvert sur l'arbre de D1 avant la passe adversariale de D1.** Au début de cette passe, `npm run check` échouait (« 5.2 · dépôt git : arbre de travail non propre », et « k · zip de reprise » en cascade), et les fichiers sales comprenaient **`data/projet-gare.json`**, jeu déclaré FIGÉ en 1.0. Le § 13.1 impose un commit par module **puis** la passe ; le § 12.3 impose des tests verts à la livraison. Ici D1 a été publié, puis modifié par le module suivant avant d'être relu. | majeur (procédé) | `npm run check` au début de la passe : « 3 echec(s) sur 16 controles ». Le diff alors en cours supprimait `situation_exemple.avancement_declare_pct` et passait `numero` de 7 à 4 dans le jeu figé. Depuis `f562459` le contrôle est vert et D-039 consigne la décision — mais la correction d'un bloquant de D1 est entrée dans le dépôt par le commit d'un autre module, sans passe de contrôle propre. | Brancher pour le module suivant, ou corriger et committer D1 avant d'ouvrir D4. Et vérifier que D-039 couvre bien la modification du jeu figé au titre du § 10.1 : la revue des modules impactés (TV, D2, D1) n'est pas tracée. |

**Total : 28 défauts — 7 bloquants, 11 majeurs, 10 mineurs.**

---

## 2 · Les dix points du § 12.2

1. **Unités et homogénéité.** **Défaut (B3)** : `depot + delai` additionne jours ouvrés et jours
   calendaires dans `tresorerie()`. **Défaut (M1)** : la même durée de chantier est convertie en
   calendrier avec les intempéries pour les pénalités, sans elles pour les frais de durée.
   Pour le reste, **RAS vérifié** : j'ai recalculé à la main les conversions m³ en place → m³
   foisonné (×1,25), cadence d'atelier → h/unité (`8 n / c × k`), unités → m³ sur FOND
   (`conversion = 0,4 = 1/2,5`), tonne → kg sur CHAP/CHLV (`0,001`), et les cinq tombent juste.
   La conversion FOND est celle que le module annonce comme la plus piégeuse : elle est correcte.
2. **Référentiels mélangés.** **RAS.** Aucun référentiel normatif n'est invoqué, et c'est conforme
   au § 5.0. Le CPS est systématiquement nommé comme la source qui prime (S4f, S4b, l'encart de
   tête, `avertissement_CPS` injecté par variable).
3. **Valeur normative sans V0/V1.** **RAS, et bien tenu.** `npm run check` confirme « aucune balise
   V2 dans content/ » ; les 148 V3 sont registrées et les 144 V3 de `data/` lues sont couvertes.
   J'ai relu une à une les valeurs contractuelles (avance 10 %, retenue 7 %, plafond 7 %,
   cautionnement 3 %, délai 60 j, pénalité 1 ‰, plafond 10 %, a/b/c de la révision) : **toutes sont
   balisées V3 avec fourchette et année**, et toutes renvoient au CPS. Aucune ne se fait passer
   pour une règle. C'est le point le mieux traité du module.
4. **Ordres de grandeur.** Les prix de ressource marocains 2026 sont plausibles et tous fourchettés.
   Le ratio d'acier (88,5 kg/m³ sur la mezzanine, 60 à 130 ailleurs) est cohérent. **Défauts** :
   le coût au m² (B4) et la part du gros œuvre (M2) sont jugés sur des bases qui ne sont pas celles
   de leurs ratios ; le besoin de trésorerie (B3) est hors d'ordre de grandeur de 55 % ; et aucun
   coût n'est publié avec ses bornes (B5), alors que l'étendue réelle est ×0,60 à ×1,69.
5. **Cohérence data / figures / calc / planning.** Les prix et les durées partent bien des mêmes
   cadences — c'est la réussite du module, et je l'ai vérifiée : `h/unité × quantité` redonne
   exactement `durée × ateliers × compagnons × 8` sur les sept postes décomposés. **Défauts** : la
   situation ignore le réseau (B1) ; les frais de durée ignorent la durée calendaire que D2 publie
   (M1) ; la figure 4 ne sort pas de `data/` (M6) ; `ecart_attachement` n'est lu par rien (B6).
6. **Grille § 7.2.** Voir § 3 — **échec sur deux critères.**
7. **Sécurité (§ 3.4).** La section S4c est **réelle, pas décorative** : elle ne récite pas des
   consignes générales, elle relie quatre lignes de prix à quatre risques d'exécution
   (rotations de coffrage → décoffrage prématuré ; heures de levage → temps de vérification ;
   installation → protections collectives ; divers → encombrement), et elle s'appuie sur le calcul
   du § S4d. Elle est conforme au § 5.0 (aucune valeur normative). Deux réserves : elle n'est
   chiffrée qu'une fois (M5 montre que ce chiffre n'est pas intégré au bordereau), et m6.
8. **Vérité du rendu.** Les 29 tests de rendu passent, zéro erreur console, aucune requête réseau.
   Les cinq captures ont été **regardées**. Figures 1, 2, 5 : correctes dans leur tracé.
   **Défauts** : légende auto-contradictoire (B7), légendes fausses (m1, m2), figure sans données
   (M6), barre invisible (m3), chevauchement texte/bande (m7).
9. **Simplifications non signalées.** **Défauts** : M5 (la ligne de divers), M10 (quatre hypothèses
   de modèle), M4 (le prorata des métiers, en commentaire de code seulement), M3 (la moyenne non
   pondérée). **À l'inverse, bien déclaré** : l'étalement uniforme des dépenses *est* déclaré
   (`hypothese_de_profil`, et l'encart « Pourquoi la courbe de dépense n'est pas la courbe en S ») ;
   le remboursement d'avance *est* explicite (fraction publiée, bornes 20–80 % dans `data/`) ; et la
   reprise du métré de la mezzanine depuis le module TV *est* dite trois fois (type
   `unitaire_herite_TV`, docstring `_mezzanine`, « D1 ne refait pas le métré du TV : il le re-PRIX »).
   Ces trois points, visés par la commande de cette passe, sont donc **RAS**.
10. **Texte télégraphique ou remplissage.** **RAS.** Le texte est dense, en phrases, chaque
    paragraphe porte une règle ou un chiffre. Le glossaire et la check-list sont substantiels.
    Seule exception : M7, une affirmation chiffrée que rien ne produit.

### Point 11 — la famille « arithmétique juste, modèle faux »

Elle est présente, et elle a produit **six des sept bloquants**.

- *Une grandeur d'état déclarée au lieu d'être dérivée du réseau* : **B1**, récidive exacte des
  quinze bloquants de la TV et du bloquant B1 de D2.
- *Un paramètre déclaré dans `data/` que rien ne relit* : **B6** (`ecart_attachement`), **M3**
  (la productivité de référence du terrassement).
- *Un verdict publié que le chiffre d'à côté contredit* : **B2** (ECART présenté comme expliqué),
  **B7**, **M2**, **M8**, m1, m2.
- *Une base de ratio prise là où elle n'est pas définie* : **B4**, **M2** — dans le module même qui
  consacre sa plus longue section à dénoncer cette faute et dont D-037 prétend l'avoir éliminée.
- *Une ressource prise en moyenne au lieu d'être prise là où elle est définie* : **M3**.
- *Un taux appliqué à la mauvaise base de temps* : **B3**, **M1**.
- *Une fausse précision* : **B5** (un marché au dirham près pour une étendue de ×0,60 à ×1,69).

**Ce qui les a trouvés** : une contre-expertise à l'aveugle, deux nombres du même fichier de sortie,
cinq captures regardées, et un `grep` sur une clé de `data/`. **Aucun test**, encore une fois : les
34 vérifications de `test_prix.py` sont toutes vertes.

**Ce que la frontière déboursé sec / prix de vente donne** : elle est, elle, **correcte et tenue**.
La séparation des deux voies (prix de ressource contre prix posés) est propre, le refus d'ajouter
des heures aux forfaits est juste et bien argumenté, et la correction du double compte des forfaits
est un vrai progrès sur la version précédente. L'**ordre des opérations de la situation** (travaux →
révision → retenue sur le **montant révisé** → remboursement d'avance sur le cumul) est **juste** :
je l'ai refait indépendamment et je tombe à 0,65 %. Aucun taux n'est appliqué à son complément.

**Ce que le module affirme avoir prouvé sur la dette n° 10, contre ce que son calcul montre.** Le
module dit : « la base du ratio était fausse, **et** les cadences sont optimistes d'un facteur 2,52
obtenu par un chemin entièrement indépendant ». Son calcul montre : (a) la base était effectivement
fausse — **acquis, bien démontré, c'est le meilleur résultat du module** ; (b) le facteur 2,52 est
une moyenne non pondérée de cinq postes dont deux partagent une cadence et dont un sixième,
mesurable et déclaré, a été omis — il vaudrait ≈ 1,9 autrement (M3) ; (c) le chemin n'est pas
entièrement indépendant, les deux lectures partageant cadences et effectifs (m9) ; (d) les
productivités par métier qui portent la démonstration sont une identité, pas une mesure (M4).
La dette n° 10 est donc **mieux instruite qu'avant et moins solidement chiffrée que le module ne
l'écrit**. La phrase de STATE.md « facteur ×2,52 obtenu par les productivités individuelles, chemin
indépendant » doit être nuancée.

---

## 3 · Grille § 7.2 (minimum 2 partout)

| Critère | Note | Justification |
|---|---:|---|
| Le « pourquoi » est expliqué | **3** | Pourquoi le nombre d'ateliers n'est pas dans h/unité, pourquoi un forfait n'a pas de part de main-d'œuvre, pourquoi un ratio a un domaine, pourquoi un prix posé ne se décompose pas : l'intuition précède chaque formule. Remarquable. |
| Les hypothèses sont explicites | **1** | Les hypothèses de **données** sont exemplaires (S4b, 148 V3 registrées, fourchettes et année). Les hypothèses de **modèle** ne le sont pas : le prorata des trois métiers (M4), la pompe absente sur trois postes, le paiement comptant des fournisseurs, le taux d'atelier de MEZZ (M10), la moyenne non pondérée (M3), le calendrier des frais de durée (M1). Ce sont précisément celles qui pilotent les chiffres publiés. **Échec.** |
| Les formules sont justifiées | **3** | `h = 8n/c × k` est démontrée, testée et retournée en productivité ; la révision est démontrée et son contrôle `a+b+c=1` lève une exception ; la cascade du déboursé au prix de vente est explicite. |
| L'exemple est vérifié | **1** | Le contre-calcul existe, est exécuté — et **échoue sa propre tolérance sans que le module le dise** (B2). La situation n'est confrontée à rien (B1). La trésorerie mélange deux calendriers (B3). Deux ratios de contrôle rendent des verdicts sur des bases interdites (B4, M2). La vérification est outillée mais ne vérifie pas. **Échec.** |
| Le piège est identifié | **3** | S5, l'exercice 4, les « erreur courante » de chaque figure, les huit réflexes du mémo : c'est la meilleure partie du module, malgré M8. |
| Le lien avec l'exécution | **2** | S4c relie le prix aux conditions de travail, le mémo porte les points d'arrêt côté maîtrise d'œuvre. Mais la double lecture entreprise / MOE n'existe que dans le mémo, et le lien reste surtout argumentatif. |
| Le lien avec le coût et le délai | **3** | C'est l'objet du module et il est tenu : frais indexés sur la durée, coût d'un mois de retard, variante recalée qui montre qu'une cadence optimiste se paie deux fois. |

**La grille échoue sur deux critères** (hypothèses explicites, exemple vérifié), comme celle de D2.

---

## 4 · Verdict

**28 défauts, dont 7 bloquants — un corrigé en vol pendant la passe, six ouverts : le module enseigne mieux qu'aucun autre du cours qu'un ratio n'a de
sens que sur sa base et qu'une situation se bâtit sur un constat — et il publie un verdict vert sur
une base que son propre ratio exclut, un contre-calcul qui échoue sa tolérance sans le dire, une
trésorerie qui additionne jours ouvrés et jours calendaires, et une situation au septième mois pour
un chantier qui en est au troisième.**

---

## Suite donnée (21/10/2026, par l'auteur)

**Les six bloquants ouverts sont corrigés** (B1 l'était déjà, par le commit de D4 — voir la note de
procédé ci-dessous), ainsi que cinq majeurs dont trois étaient des affirmations fausses dans le texte
publié.

| # | Correction | Contrôle ajouté |
|---|---|---|
| B2 | Le rapprochement des deux voies n'est plus présenté comme un contrôle de tolérance : c'est une **calibration**, son résultat est la ligne de divers, et le seul verdict possible est un seuil d'inexplicabilité (40 %, déclaré). Le verdict est publié dans le module. | Deux tests : le verdict est publié, et il bascule au-delà du seuil |
| B3 | `tresorerie` comparait un délai de paiement de 60 jours **calendaires** à des jours ouvrés. Une fonction `conversion_calendaire` établit le pont une fois pour toutes. Besoin de trésorerie **15,36 → 10,40 MMAD (20,6 → 13,9 %)**. | Test de la conversion + canari : comparer sans convertir gonfle le besoin |
| B4 | Le coût au m² est comparé à sa fourchette sur le périmètre du ratio — **hors interfaces ferroviaires, par m² de plancher** : 7 902 MAD/m², dans la fourchette. Le coût par m² d'emprise tout compris reste publié, sans verdict. | Test du domaine de définition et du recalcul des surfaces |
| B5 | **Fourchette de prix publiée** (D-036) : ×0,63 à ×1,62, **99 % d'étendue**, avec ce qu'on en fait. | Test de l'ordre des trois bornes et du recalcul de l'étendue |
| B6 | L'écart d'attachement est **appliqué** : la situation paie la quantité constatée (+9 % sur FOUI, 30 258 MAD), pas le métré d'étude — ce que le module enseignait en trois endroits sans le faire. | Trois tests : quantité attachée, montant payé, un seul poste concerné |
| B7 | La légende de la figure 5 citait des plages lues à l'œil et se contredisait. Les périodes où l'entreprise est devant sont **calculées** (`periodes_ou_l_entreprise_est_devant`) et la légende les lit. | — |
| M1 | Les frais de durée sont comptés en **mois calendaires** (18,0) et non en « mois » de 21 jours ouvrés (17,28) : un encadrement et une grue se paient au calendrier. | Canari : les compter en mois ouvrés donne un autre total |
| M3 | Le facteur de recalage est **pondéré par le travail** et couvre le terrassement : **×1,92** au lieu de ×2,52. La cadence des dalles n'est plus comptée deux fois. Le soupçon de la dette n° 10 est confirmé **dans son sens** et **revu à la baisse dans son ampleur**. | Recalcul du facteur, canari sur la moyenne naïve, test de non-doublon, test du périmètre |
| M4 | La **circularité** des productivités par métier est dite dans le module, pas seulement en commentaire de code : elles traduisent le facteur, elles ne le démontrent pas. Le périmètre exclu (charpente, couverture, façade) est déclaré. | — |
| M5 | La ligne de divers est **intégrée dans une variante publiée** (96,5 MMAD contre 75,0), avec la question « lequel signeriez-vous ? » et la **simplification déclarée** : tous les autres totaux du module sont des bornes basses. | Test du calcul et de la présence de la déclaration |
| M8 | L'exercice 4 annonçait quatre erreurs et en contenait trois, dont une se contredisant en deux lignes. La quatrième erreur réelle (pertes de béton) y est, et la ligne correcte est annoncée comme un piège. | — |

**Portés en dette déclarée** (D-034) : M2, M6 (figure 4 écrite en dur dans `figures()`), M7, M9
partiel, M10, M11, et les dix mineurs.

**Note de procédé — le reproche est fondé.** Le module D4 a été écrit pendant cette passe et a
modifié `calc/prix.py`, `content/03-d1-metres-prix.md` et `data/projet-gare.json` sous le relecteur,
dont un bloquant (B1) qu'il a corrigé par effet de bord. C'est une faute de séquencement : une passe
adversariale doit porter sur un livrable figé. Pour les modules suivants, le module en cours
d'écriture ne touche plus aux fichiers d'un module en cours de relecture — et si c'est inévitable,
la passe est relancée.

**Ce que cette passe a prouvé, et qui vaut plus que les 28 défauts.** Les 34 vérifications de
`test_prix.py` étaient toutes vertes et n'ont vu aucun des sept bloquants. Six appartiennent à la
famille « arithmétique juste, modèle faux », et deux d'entre eux — la base du ratio au m², le facteur
moyenné — sont des récidives **dans le module même qui enseigne à ne pas les commettre**. Écrire la
règle ne suffit pas à la suivre : il faut un contrôle qui la vérifie, et un relecteur qui ne lit pas
le raisonnement de l'auteur.
