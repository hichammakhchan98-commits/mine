# DECISIONS — journal daté des décisions validées

Format : **date — décision — raison — impact**.
Une décision n'entre ici qu'une fois **validée par le lecteur**. Les propositions en attente sont
marquées « ⏳ EN ATTENTE » et ne font pas foi.

---

## 2026-10-15 — Décisions actées

**D-001 · Mode d'exécution : B (chat avec bac à sable éphémère).**
*Raison* : choix explicite du lecteur (« Lance étape 0, mode b »).
*Impact* : zip de reprise à chaque fin de module (`cours-genie-civil-<palier>-<module>.zip`, `.git`
inclus, sans `node_modules` ni anciennes captures) ; au début de chaque séance, dézippage, relecture de
`CLAUDE.md`, `STATE.md`, `DECISIONS.md`, puis `npm ci --ignore-scripts && npm run check` avant de
continuer ; section « Reprise » en tête de `STATE.md` ; **seul le zip fait foi**, aucun chiffre repris de
la mémoire d'une conversation précédente.
*Réserve signalée au lecteur* : le bac à sable dispose d'un dépôt git **distant** qui survit entre les
conversations (branche `claude/lance-etape-0-mode-b-ijn9r4`). Le mode B est appliqué tel quel ; la branche
sert de seconde sauvegarde. Le passage éventuel en mode A est posé en question 1.

**D-002 · Phase « sans calculs normatifs » (§ 5.0) activée — `normes_disponibles = false`.**
*Raison* : vérification des pièces (§ 5.1a) — **aucun document normatif n'a été fourni**. Ni BAEL 91
mod. 99, ni BPEL 91, ni RPS 2000 version 2011 et son catalogue communal, ni CPS, ni bordereau de prix, ni
ancienne version du cours. Seul le prompt maître v4.1 a été remis.
*Impact* : tout calcul de dimensionnement ou de vérification réglementaire est **interdit** ; 12 modules
du palier 1 sont suspendus (⏸) et aucun n'est écrit ; la tranche verticale structurelle (§ 5.3) est
remplacée par une **tranche verticale de suivi** ; aucune valeur V2 normative n'est écrite ; toute valeur
numérique reste V3 (fourchette, année de référence). Levée par le lecteur selon la procédure du § 5.0.7.

**D-003 · Re-vérification du point de vigilance « révision du RPS 2000 » (§ 3.1).**
*Raison* : l'annexe A6.1 du prompt marquait ce point « non recoupé » (état d'avril 2026, plus de six
mois) ; le § 3.1 impose de le re-vérifier.
*Constat* : les décrets **2.24.766** (relèvement du zonage sismique de ~80 communes) et **2.24.767**
(catalogue communal) ne sont pas restés à l'état de projet — ils ont été **publiés au Bulletin officiel
n° 7351 du 11/11/2024** (source : éditeur juridique LexisNexis Maroc ; la récupération directe de la page
a été bloquée par le proxy du bac à sable, le constat reste donc **V2**, non V0). La **révision complète**
du RPS 2000 n'a pas abouti : une enquête nationale auprès des professionnels a couru jusqu'au
**05/05/2026** pour la préparer.
*Impact* : le reclassement de 2024 est traité comme **du droit en vigueur** et non comme un projet, ce
qui confirme la consigne du § 10.1 (double zonage si la commune du cas phare est concernée). Le
**catalogue communal reste à lire sur le texte officiel avant tout calcul sismique** (⚠, inscrit dans
`STATE.md` et `cadrage/registre-sources-cadrage.csv`, id E0-S01).

**D-004 · Contrôle de reprise minimal à l'Étape 0.**
*Raison* : le § 12.1k exige qu'un zip de mode B s'ouvre et repasse au vert, mais la chaîne de build
n'existe qu'à partir de l'Étape 1 (§ 5.2). Sans contrôle, le premier zip ne serait pas vérifiable.
*Impact* : `build/check-e0.mjs` contrôle ce qui existe aujourd'hui — intégrité des JSON, présence des
pièces de cadrage, en-têtes des registres, empreinte de `data/`. Il est **déclaré comme simplification**
dans `STATE.md` et remplacé par le `check.mjs` complet (§ 12.1 a–k) à l'Étape 1.

---

## 2026-10-15 — « OK partout » : l'Étape 0 est validée

**D-005 · Tous les défauts de l'Étape 0 sont acceptés.** Réponse du lecteur : « OK partout ».
*Impact* : les propositions P-01 à P-15 passent en décisions. Le jeu de données du cas phare est
**figé en version 1.0** (`data/projet-gare.json`, `fige_le: 2026-10-15`, commit `ad792eb`, tag local
`donnees-gare-v1.0`) ; idem pour `projet-r5.json` et `referentiels.json`. Détail :

| Point | Décision actée |
|---|---|
| Mode | **B** maintenu (zip de reprise ; la branche distante reste un second filet) |
| Référentiels | option **M** (BAEL 91 mod. 99, BPEL 91, RPS 2000 v. 2011) + **Eurocodes 1re génération** pour l'acier, annexe comparative sur la 2e |
| Normes | aucune fournie → `normes_disponibles = false`, phase § 5.0 active |
| Site du cas phare | **S1, région de Marrakech** — double zonage à traiter (reclassement 2024) |
| Géométrie | 120 × 40 m, trame 7,50 m, hall 32 m de portée, mezzanine +5,00, marquise 4,50 m, passage souterrain, 3 quais ; poutre témoin PM1 = 3 × 8,00 m + console 4,50 m |
| R+5 | conservé en **cas secondaire léger** |
| Calibrage | tableau des 35 modules accepté tel quel |
| Module **B7c** | **accepté** — interfaces ferroviaires, P1, [N], actif |
| Lots techniques | plafond de **10 %** (B7b + C4) conservé |
| Stade, C8 | **retenus**, tous deux en P2 |
| Priorités | P1 → P2 → P3 ; dans P1, **le métier du lecteur d'abord** (D2, D1, D3, D4, D7) |
| Ordre de coupe | 3D non structurels → O6 des [M] → P3 → O5 des [M] → cas R+5 |
| Budget 3D | 5 modèles pour le P1 actif, +9 à la levée du § 5.0, révisé après la tranche verticale |
| Prix | année **2026**, prix unitaires **V3** en fourchettes |
| /devil | porté par un **sous-agent distinct** qui ne lit pas le raisonnement de l'auteur |
| Rendu | HTML responsive hors ligne, KaTeX pré-rendu, ≤ 1,5 Mo par module |
| Ancienne version | rien à reprendre |

**D-006 · Trois points n'avaient aucun défaut à accepter. Ce que j'ai fait, à corriger d'un mot.**

1. **Séances, budget, date de fin du palier 1.** Aucune valeur n'a été donnée. Le § 5.5 exige une date
   dès l'Étape 0 ; le § 13.4 demande d'avancer sur une hypothèse déclarée plutôt que d'interrompre.
   J'inscris donc une **hypothèse V3** : 2 séances par semaine, environ 1,5 séance par livraison, soit
   **fin du palier 1 actif au 15/03/2027** (`planning.date_fin_P1_actif_hypothese`). La date du palier 1
   *complet* reste indéterminée : elle dépend de la mise à disposition des normes. Ces deux dates sont
   rappelées à chaque bilan tant qu'elles ne sont pas confirmées.
2. **Site du second site de D7.** Le défaut ne disait rien. J'ai retenu **S2 (Agadir)** comme je l'avais
   recommandé : D7 porte ainsi des sols difficiles sans alourdir le cas phare.
3. **Partie exécution de B5a** (charpente : fabrication, soudage, levage). Elle ne dépend d'aucune norme,
   et le § 5.0.2 met explicitement les méthodes d'exécution dans ce qui est « autorisé et prioritaire ».
   Je la **détache en module actif `B5a-exec`** ; la partie calcul reste ⏸. Le palier 1 actif passe de
   22 à 23 modules et de 28 à 30 livraisons.

**D-007 · Le logiciel aux éléments finis reste inconnu.** La question 5 n'a pas reçu de nom. Sans
conséquence immédiate : B6b est suspendu par le § 5.0. À redemander avant son écriture.

**D-008 · Étape 1 — choix techniques du socle.**
- **Une scène 3D par vue, initialisée à l'affichage et libérée en sortie**, avec un plafond de 4
  contextes WebGL simultanés (file LRU). C'est la **seconde** option admise par le § 4.4 ; elle est plus
  simple et plus testable que le renderer unique à viewport/scissor pour des pages portant une à trois
  vues. À revoir si une page devait en porter davantage.
- **Versions épinglées** (§ 4.4), toutes publiées depuis plus de 14 jours : `three@0.186.1`,
  `esbuild@0.28.2`, `katex@0.18.10`, `@playwright/test@1.56.1` — cette dernière calée sur le Chromium
  préinstallé du bac à sable. KaTeX est en **0.18.10 et non 0.18.0** : la 0.18.0 porte un avis de
  sécurité (pollution de prototype, GHSA-238p-pmpm-9mq7). `npm audit` : 0 vulnérabilité.
- **Séparateur de format des variables : `::` et non `|`**, parce que `|` délimite les cellules de
  tableau en Markdown et cassait les variables placées dans un tableau.

**D-009 · Limite de l'environnement : les tags git ne sont pas poussables.** Le proxy git de ce bac à
sable n'expose que `refs/heads/*` (`git ls-remote origin` ne montre aucun tag ; la poussée échoue sur
quatre tentatives avec temporisation). Conséquence : le figeage des données est référencé par son
**commit** `ad792eb`, qui est poussé et vérifiable. Le tag `donnees-gare-v1.0` existe localement et
voyage dans le zip de reprise, qui contient `.git`. Le § 5.5 prévoit « un tag par palier » : il sera
posé localement et porté par le zip, pas sur GitHub.

---

## ⏳ Reste en attente

Tout le reste a été tranché par le « OK partout ». Ne subsistent que des points qui dépendent d'un
document ou d'une information que le lecteur n'a pas encore.

| ⏳ | En attente de | Effet |
|---|---|---|
| A-01 | **Les documents normatifs** (BAEL, BPEL, RPS + catalogue communal, CPS) | lève le § 5.0 et débloque 12 modules du palier 1 |
| A-02 | **Un bordereau de prix** non confidentiel, même ancien | ferait passer tout le volet économique de V3 à V0 recalé |
| A-03 | **Le logiciel aux éléments finis** pratiqué par le lecteur | nécessaire avant d'écrire B6b (suspendu) |
| A-04 | **Confirmation des dates** du palier 1 (hypothèse V3 en place) | § 5.5 |
| A-05 | **Référentiel ferroviaire** (quais, gabarits, caténaire), à fixer par le CPS | nécessaire pour les parties chiffrées de B7c |

---

## 2026-10-15 — Étape 2, tranche verticale de suivi

**D-010 · La fiche du module annonçait un contre-calcul qui n'en était pas un.** Elle prévoyait
« durée par cadences contre durée par chemin critique ». Ces deux grandeurs ne sont pas comparables :
la somme des durées et le chemin critique diffèrent **par construction**, et c'est tout l'objet du
CPM. Les comparer ne vérifie rien ; leur écart est un **résultat** à commenter (le gain du
recouvrement, 18 % ici), pas un contrôle.
*Décision* : trois contre-calculs réels à la place.
1. **Durée de tâche** : cadence unitaire × effectif, contre un **rendement d'équipe** déclaré
   séparément. Vérifie que deux hypothèses V3 sont mutuellement cohérentes — rien de plus, et le
   module le dit.
2. **Durée du cycle** : parcours avant/arrière contre **énumération exhaustive des chemins**. Deux
   algorithmes pour la même grandeur : ils doivent coïncider exactement.
3. **Valeur acquise** : par les coûts contre les **quantités relevées** sur le chantier.

**D-011 · La première version du contre-calcul de valeur acquise était tautologique.** Elle
multipliait les quantités *théoriques* par l'avancement *déclaré* : algébriquement identique à la
voie A, écart nul par construction. Même piège que le contre-calcul du socle. La voie B part
désormais des **quantités relevées**, qui ne passent pas par l'avancement déclaré. Un test vérifie
cette indépendance en changeant l'avancement déclaré et en constatant que la voie B ne bouge pas.

**D-012 · Deux contrôles sonnent volontairement dans ce module, et c'est le sujet.**
- Le contre-calcul de valeur acquise sort de sa tolérance (1,03 % pour 1 %) : l'avancement déclaré ne
  colle pas aux relevés. C'est la dérive que le contrôle existe pour attraper.
- Le contrôle de cohérence du prix horaire sort de sa fourchette (5,2 % contre 15 à 30 %) : le prix
  horaire d'un compagnon nu et un prix unitaire posé ne décrivent pas la même chose.
Un module où tous les voyants sont au vert n'apprend rien sur les voyants.

**D-013 · La date d'arrêt du suivi est déduite, plus écrite.** Elle était posée à « fin de la
semaine 6 » dans les données, ce que le planning contredisait. Elle se calcule maintenant à partir du
nombre de zones prévues et de la cadence.

**D-014 · 16/10/2026 — Le seuil de 1 % du recoupement n'appartient qu'aux postes géométriques.**
*Raison* : la passe /devil a montré que l'alarme de D-012 était du **bruit**. En dirhams, l'écart de
1,03 % est noyé dans l'incertitude des entrées : l'acier fait 43 % du coût de zone et son ratio V3
ouvre une fourchette de ± 44 %, soit plus de quarante fois le seuil. En unités physiques, le béton
est à −0,63 % et le coffrage à −0,82 % : sous le seuil, donc rien à signaler.
*Décision* : le recoupement fait foi **en m³ et en m²**, poste par poste ; le seuil de 1 % ne
s'applique qu'au béton et au coffrage, qui sont géométriques, jamais à l'acier ni aux dirhams. La
fiche mémo publie cette règle et non plus « écart > 1 % → attachements ».
*Impact* : `calc/valeur_acquise.py` (seuil nommé et publié), fiche mémo S8, D-012 corrigé sur ce
point — le contrôle de prix horaire, lui, sonne toujours et reste ouvert (dette 10).

**D-015 · 16/10/2026 — Le planning est contraint par le parc de coffrage, et ce contrôle entre dans
la chaîne.** *Raison* : le planning publié demandait environ 2,5 fois le coffrage que `data/`
déclarait posséder, et un exercice affirmait le contraire. Le matériel était posé a priori au lieu
d'être déduit du planning. *Décision* : `⌈cycle / cadence⌉` zones détiennent du coffrage
simultanément ; `cycle_plancher.py` publie `coherence_materiel` (immobilisé, stock, marge, verdict),
un test exige que le planning de référence tienne et que la variante renforcée **échoue**, et le parc
de `data/` passe de 420 à 1 300 m², les étais devenant une densité au m².
*Impact* : `data/projet-gare.json`, `calc/cycle_plancher.py`, `calc/tests/test_plancher.py`, § d et
exercices 2 et 3 du module. L'exercice 3 change de conclusion sur un point : renforcer l'équipe tient
la cible de 25 jours, mais coûte 397 m² de tables en plus — ce qui reste trois fois moins qu'un
dédoublement de front.

**D-016 · 16/10/2026 — Le build échoue sur les accidents de gabarit.**
*Raison* : trois erreurs publiées dans ce dépôt ne venaient d'aucun raisonnement faux, mais de la
mise en forme : un chiffre littéral collé derrière une variable (`{{…::n0}}0 %` affichait « 40 % »
pour 4), un repère de rédaction laissé dans un corrigé (« un pic d'effectif de **X** personnes »), et
une variable placée dans une formule, que KaTeX compose littéralement.
*Décision* : ces trois motifs font **échouer le build** (`controlerAccidentsDeGabarit`), et chaque
règle porte son canari dans `build/tests/test-gabarit.mjs` — un contrôle qu'aucun cas ne fait sonner
ne prouve rien. Les champs d'une balise de preuve sont par ailleurs résolus **avant** extraction,
pour qu'une V3 puisse lire sa valeur dans `data/` au lieu de la recopier.
*Impact* : `build/md.mjs`, `build/build.mjs`, `build/check.mjs`, `build/tests/`.

**D-017 · 16/10/2026 — La courbe en S est ancrée sur la date d'arrêt.**
*Raison* : la figure et le tableau de valeur acquise du même module donnaient deux avancements
différents à la même date, pendant que la légende affirmait que l'écart vertical *était* SV.
*Décision* : la date d'arrêt est ajoutée aux abscisses de la courbe, et un test exige
prévu = VP/BAC et réalisé = VA/BAC à 0,5 point près, puis que l'écart vertical soit bien SV
(15,80 points contre 15,75). *Impact* : `calc/cycle_plancher.py`, `calc/tests/test_plancher.py`.

**D-018 · 16/10/2026 — Un contrôle publie la largeur sur laquelle il tient.**
*Raison* : le contre-calcul de la durée de coffrage passait avec 3,45 % d'écart, mais seulement parce
que le rendement d'équipe avait été choisi près du point qui le fait passer : la tolérance n'est
respectée que sur 27 % de la fourchette déclarée, et le contrôle échoue à sa borne basse.
*Décision* : `calc/` calcule et le module publie la **plage de rendements qui passe** et la part de
la fourchette qu'elle couvre. Règle générale pour la suite du cours : un contrôle qui ne dit pas sur
quelle largeur il tient parle du choix de son auteur, pas des données.
*Impact* : `calc/cycle_plancher.py`, encart « Pourquoi ceci n'est PAS un contre-calcul ».

**D-019 · 19/10/2026 — La cadence de rotation est bornée par TOUTES les équipes dédiées.**
*Raison* : la règle publiée était `max(coffrage ; ferraillage de dalle) + bétonnage` et oubliait le
**ferraillage des poutres**. Sur le cas de référence, le ferraillage de dalle est le plus long et
masque l'oubli : la cadence de 3,41 j était juste **par coïncidence**. Dès qu'on renforce l'équipe de
dalle — l'exercice même que le module propose — la borne passe aux poutres : cadence 2,93 j et non
2,41, plancher 28,1 j et non 24,4, c'est-à-dire **au-dessus** de la cible de 25 que le module
annonçait tenue. Le module énonçait pourtant la règle qui l'aurait sauvé (« renforcer une tâche
critique ne garantit un gain que jusqu'à ce qu'un autre chemin prenne le relais ») et sa formule la
violait. *Décision* : `cadence_rotation()` prend le maximum sur les trois tâches à équipe dédiée,
publie laquelle borne, et les tests vérifient que renforcer la dalle fait bien passer la borne aux
poutres. L'exercice 3 conclut désormais qu'il faut renforcer **les deux** équipes (23,9 j), et le
module publie l'erreur comme leçon de contrôle. *Impact* : `calc/cycle_plancher.py`,
`calc/tests/test_plancher.py`, § d et exercices 2 et 3 du module.

**D-020 · 19/10/2026 — Un constat n'est pas une courbe.**
*Raison* : la courbe « réalisé » était la courbe prévue multipliée par une constante (0,740 vérifié
point par point) : vingt points fabriqués à partir d'un seul relevé, tracés en trait plein, sous une
légende qui interdisait justement de confondre constat et prévision. *Décision* : tant que `data/`
ne porte qu'un relevé, on publie **un point**, avec l'écart à la courbe prévue coté sur la figure.
Règle générale : une figure ne publie pas plus d'information que les données n'en portent.
*Impact* : `calc/cycle_plancher.py`, `assets/svgkit.js` (`courbeS` accepte un constat),
`calc/tests/test_plancher.py`, figure 5.

**D-021 · 19/10/2026 — Un contrôle doit pouvoir échouer, et partir d'ailleurs que de ce qu'il vérifie.**
*Raison* : le contrôle « chaque V3 publiée a sa ligne de registre » comparait les balises de
`content/` à un registre que le build **génère depuis ces mêmes balises** : vrai par construction,
incapable de détecter une V3 non déclarée — et quatre l'étaient (deux cadences, deux prix).
De même, le test « recalcul indépendant à la main » du béton recopiait les cotes en clair, donc ne
bougeait pas si `data/` changeait. *Décision* : un second contrôle part de `data/`, énumère les
hypothèses V3 (valeur + fourchette), et exige une ligne de registre pour chacune qui est lue par un
module ; le recalcul du béton lit les cotes dans `data/` et passe par un **autre découpage
géométrique**. *Impact* : `build/check.mjs`, `calc/tests/test_plancher.py`, sept balises ajoutées.

**D-022 · 19/10/2026 — Les contrôles vérifient les nombres, pas les modèles. C'est la dette la plus lourde.**
*Raison* : les trois bloquants de la passe 2 ont franchi **14 contrôles verts**. Aucun ne portait sur
un nombre faux : une règle incomplète, un histogramme bâti sur une hypothèse d'enchaînement fausse,
une figure qui affirmait plus que ses données. *Décision* : consignée comme dette 13, et traitée
module par module par des tests qui confrontent une sortie à une **construction indépendante** (les
dates du réseau pour l'histogramme, l'équipe qui borne pour la cadence, le nombre de relevés pour le
constat). Aucune solution générale n'est promise : ce serait une promesse qu'on ne tiendrait pas.
*Impact* : `STATE.md` (dette 13), et la méthode de tous les modules à venir.

**D-023 · 19/10/2026 — Un avancement se dérive du réseau ; il ne se répartit pas au prorata.**
*Raison* : la passe 3 a montré que le module appliquait l'avancement déclaré d'une zone à **chaque
poste** — 60 % du béton, 60 % de l'acier, 60 % du coffrage. Or son propre cycle dit qu'à 60 % du
cycle le bétonnage n'a **pas commencé** et que le coffrage est **entièrement posé**. Le module
publiait donc 59 m³ de béton pour une zone où rien n'est coulé, et sous-comptait le coffrage de 40 %.
Pire : les relevés de `data/` avaient été fabriqués sur ce même prorata, de sorte que le recoupement
« qui fait foi » comparait deux calculs partageant l'hypothèse fausse — il ne pouvait rien détecter.
*Décision* : `etat_physique_de_zone()` rattache chaque poste à la tâche qui le produit et lit son
avancement dans le réseau à la date voulue ; `suivi.quantites_relevees` est refait sur cet état ; le
recoupement compare au **réseau** et non à un prorata ; `valeur_acquise()` exige désormais
l'argument `attendu` (le rendre optionnel aurait laissé le défaut revenir en silence). Le module en
tire un encart — « 60 % d'une zone, ce n'est pas 60 % de chaque poste » — et l'exercice 4 a changé
de corrigé : le béton demandé **n'existe pas**, et le coffrage est sous-facturé.
*Impact* : `calc/cycle_plancher.py`, `calc/valeur_acquise.py`, `data/projet-gare.json`, § S6,
exercice 4, fiche mémo.

**D-024 · 19/10/2026 — La cadence est fixée par une ressource, et la marge est publiée séparément.**
*Raison* : la règle `max(équipes dédiées) + bétonnage` n'était justifiée par aucun modèle. Le
« + bétonnage » était en réalité une marge de conduite de chantier, déguisée en contrainte ; et la
liste blanche des équipes excluait le décoffrage sur une justification que `data/` contredit.
*Décision* : la borne est `max(équipe la plus chargée ; occupation cumulée des moyens partagés ÷
nombre de moyens)`, les tâches servies par la grue sont **déclarées dans `data/`** (elles changent
selon qu'on coule à la pompe ou à la benne), et la cadence retenue est `borne × (1 + marge)` avec la
marge déclarée en V3. *Impact* : l'exercice 3 a de nouveau changé de réponse, et c'est la bonne :
renforcer les deux équipes de ferraillage plafonne à 25,2 j parce que **la grue** devient la
ressource qui borne ; seule une seconde grue passe sous la cible (23,0 j). Un levier matériel que
personne ne trouve en regardant les effectifs.

**D-025 · 19/10/2026 — Toute hypothèse V3 de `data/` est registrée, et vérifiée dans sa fourchette.**
*Raison* : le contrôle de D-021 ne regardait que les V3 citées en variable dans `content/` — huit sur
vingt. Les douze autres transitent par `calc/` et arrivent tout autant dans le module. Et aucune
n'était confrontée à sa **propre fourchette** : une valeur pouvait en sortir sans que rien ne bouge.
*Décision* : toute feuille `{valeur, fourchette}` de `data/` doit avoir sa ligne de registre, sauf
mention explicite `non_publiee` ; un test vérifie que chaque valeur est dans son intervalle. Les
quatre canaris que la passe 3 avait fait passer (recouvrement à 120 %, maintien d'étais nul, maintien
saturant, effectifs permutés) sonnent tous désormais. *Impact* : `build/check.mjs`,
`calc/tests/test_plancher.py`, 27 hypothèses registrées contre 18.

**D-026 · 19/10/2026 — La valeur acquise est ce qui est FAIT, pas une fraction de temps.**
*Raison* : la passe 4 a montré que `VA = BAC × avancement_en_zones` appliquait à des dirhams le
prorata uniforme que D-023 venait d'interdire, douze lignes sous l'encart qui l'interdit. L'écart au
modèle physique atteint 26 % à 70 % du cycle ; il tombe à 2,5 % au seul point publié, parce que 60 %
du cycle est l'unique fenêtre où le coffrage à 100 % compense le béton à 0 %. *Décision* : VA et VP
sont la **valorisation de l'état physique** — quantités réellement faites (ou planifiées) × prix —
et la courbe en S est tracée dans la même unité, sans quoi son écart vertical n'est pas SV.
*Impact* : `calc/valeur_acquise.py`, `calc/cycle_plancher.py` (`valeur_physique`), le tableau S6, la
figure 5. CPI passe de 0,941 à 0,951, SPI de 0,741 à 0,709.

**D-027 · 19/10/2026 — Un taux de recouvrement déclaré doit être relu dans le réseau qu'il engendre.**
*Raison* : le décalage fin-début valait `-r × durée` au lieu de `-(1 − r) × durée`. Le taux était
donc appliqué à son **complément** : 40 % déclaré produisait 60 % réalisé, et le cycle était 6,3 %
trop long. Quatre passes l'ont manqué parce que l'autre taux, 50 %, est auto-complémentaire et
masquait le premier. *Décision* : un test relit chaque taux **dans les dates du réseau** et le
compare à sa déclaration. Règle générale : tout paramètre déclaré en mots dans `data/` doit avoir un
test qui le relit dans le résultat. *Impact* : `calc/cycle_plancher.py`, `calc/tests/`, et toutes les
durées du module, le cycle passant de 8,56 à 8,05 j.

**D-028 · 19/10/2026 — Un moyen partagé se vérifie en conflits, pas en moyenne.**
*Raison* : la règle de D-024 contrôlait l'occupation **moyenne** de la grue — 67 %, donc « ça
passe ». Le planning en demandait pourtant deux à la fois six fois, à chaque décoffrage.
*Décision* : `conflits_de_ressource()` balaie les fronts et liste les moments où la demande dépasse
le nombre de moyens ; `decaler_pour_liberer()` montre que le décoffrage, qui a de la marge, les
résout tous pour 1,05 j de décalage. Le module publie les deux. *Impact* : `calc/cycle_plancher.py`,
`calc/tests/`, § d du module.

**D-029 · 19/10/2026 — Un module qui décrit une opération à risque porte ses dispositions de sécurité.**
*Raison* : la tranche verticale parlait d'étaiement, de décoffrage, de travail en hauteur et de
levage sans une seule ligne de sécurité, alors que le § 3.4 l'exige. Dupliqué sur C1 à C8, le défaut
se serait dupliqué. *Décision* : une section S7c nomme les quatre opérations, leurs dispositions
essentielles et ce que la maîtrise d'œuvre vérifie — **sans aucune valeur normative**, que la phase
§ 5.0 interdit — et montre que les trois accidents typiques du cycle sont des accidents de
**planning**. `npm run check` échoue désormais sur tout module qui mentionne une opération à risque
sans disposition de sécurité. *Impact* : `content/`, `build/check.mjs` (16ᵉ contrôle).

**D-030 · 19/10/2026 — Un effectif est une décision, pas une hypothèse.**
*Raison* : les effectifs étaient marqués V3 sans fourchette ni ligne de registre, ce que le contrôle
de D-025 ne voyait pas. *Décision* : `data/effectifs` et `data/materiel` portent `_nature:
"decision"`. Une hypothèse décrit ce qu'on ignore et porte une fourchette ; une décision décrit ce
qu'on choisit et porte une justification. Les confondre fait croire qu'un effectif se négocie comme
on borne une incertitude. *Impact* : `data/projet-gare.json`.

**D-031 · 19/10/2026 — Un verdict publié au lecteur est une sortie de `calc/`, jamais une phrase.**
*Raison* : les trois bloquants de la passe 5 sont trois verdicts **écrits à la main** qui
contredisaient le chiffre placé juste à côté. Le module publiait « écart de 1,30 %, **sous la
tolérance de 1 %** » alors que `calc/` rendait « ECART » ; il affirmait que les six conflits de grue
« tombent à zéro » par une vérification qui **retirait** la tâche décalée au lieu de la rejouer
décalée, donc rendait zéro par construction ; et son exercice 3 recommandait une variante dont le
module avait lui-même calculé qu'elle dépasse le parc de tables de 397 m², sans jamais lire ce
résultat. *Décision* : tout verdict affiché est injecté par variable depuis `calc/` ; une variante
recommandée au lecteur ne passe le contrôle que si son éventuel déficit est publié ; et **tout
contrôle qui rend un verdict porte un canari versé au dépôt qui le fait passer au rouge** — celui de
la résolution de grue bride le décalage à zéro et doit faire remonter les six conflits.
*Impact* : `calc/cycle_plancher.py`, `calc/tests/test_plancher.py`, § S6 et exercice 3 du module.

**D-032 · 19/10/2026 — Une marge consommée sur une ressource se paie sur une autre.**
*Raison* : décaler le décoffrage libère la grue, mais retarde la **libération du coffrage** —
l'immobilisation passe de 8,05 à 9,10 jours. La première version du texte présentait la résolution
comme gratuite. *Décision* : le module publie les deux effets, vérifie que le parc tient malgré le
décalage, et en tire la règle générale. Le texte ne dit plus que le décoffrage « n'est pas sur le
chemin critique » — il l'est, dans le cycle de sa zone — mais que le décaler **ne retarde pas le
démarrage de la zone suivante**, ce qui est la propriété réellement utilisée.

**D-033 · 20/10/2026 — Recentrage demandé par le lecteur : gare ferroviaire et bâtiment, rien d'autre.**
*Décision du lecteur, le 20/10/2026* : abandonner **aéroport, port, barrage/digue, tunnel, hydraulique
et routes** (tout le palier 3 et les cas exotiques du palier 2), et concentrer le cours sur les
**gares ferroviaires** : béton armé, gros œuvre, second œuvre, lots techniques, et le pilotage qui va
avec. *Raison* : ce sont les seuls ouvrages de son poste ; le reste était du périmètre encyclopédique.
*Impact* : le palier 3 (8 modules, 14 livraisons) est **supprimé**, pas reporté. Du palier 2 ne
survivent que les sujets qui touchent une gare. Le cours passe de **90 à ~40 livraisons**, et
l'ordre de livraison est reconstruit autour du quotidien du Chef de Projet Suivi. L'ancien sommaire
reste dans git pour mémoire.

**D-034 · 20/10/2026 — Échéance au 31/10/2026, et ce qu'elle coûte au § 12.2.**
*Décision du lecteur* : une version utilisable du cours **fin octobre**, soit onze jours.
*Conséquence assumée* : le cycle « passe adversariale relancée jusqu'à zéro bloquant » (§ 12.2) est
remplacé, pour les modules de cette série, par **une passe par module — bloquants corrigés, majeurs
et mineurs portés en dette déclarée**. *Raison* : la tranche verticale a demandé cinq passes et
quatre séances ; à ce rythme, huit modules demandent un mois et demi. La contrepartie est écrite ici
pour que personne ne la découvre plus tard : **des défauts mineurs seront publiés**, et les modules
de cette série ne portent pas la même garantie que la tranche verticale. Ce qui ne change pas : la
chaîne `data → calc → rendu`, les contre-calculs, le balisage V3, les contrôles automatiques, et le
refus de publier un chiffre non calculé.

## D-035 — 20/10/2026 — Les huit bloquants de D2 sont corrigés, pas portés en dette

**Décision.** La passe adversariale n° 1 de D2 a trouvé 32 défauts, dont 8 bloquants. Tous les
bloquants sont corrigés et republiés, ainsi que treize majeurs et mineurs que D-034 autorisait à
porter en dette — parce que cinq d'entre eux étaient les amorces directes des bloquants suivants.

**Raison.** Six des huit bloquants sont de la famille identifiée par la tranche verticale : une
arithmétique juste sous un modèle faux. Le plus grave (B1) publiait la date d'une fenêtre de
consignation puis faisait démarrer la tâche ailleurs, perdant 17,5 jours ouvrés et un mois de date
contractuelle. Les porter en dette aurait laissé dans le cours un planning dont la thèse centrale
n'était implémentée qu'à moitié.

**Impact.** Durée du chantier 341,86 → **362,92 jours ouvrés** ; fin 2028-03-30 → **2028-05-01** ;
chemin critique recomposé (il est désormais **coupé en deux** par la fenêtre de consignation, ce qui
est le résultat pédagogique le plus fort du module) ; assiette de la courbe en S et de l'histogramme
ramenée au travail (7 847 → 6 895 jours-hommes) ; séquence terrassement corrigée pour respecter la
rubrique de sécurité du module lui-même ; conflit de grue publié et **non résolu** — le chantier
demande une seconde grue, et le module le dit. Deux sections nouvelles (S4f décomposition du chemin,
S4g ressources en conflit), une figure de plus, et une fourchette de date remplaçant la date unique.

**Ce que cela change pour la suite.** `calc/cpm.py` accepte une contrainte de début au plus tôt
(étalonnée sur 5 cas fermés) ; le build **échoue** sur toute option de figure inconnue du générateur ;
les options de figure lisent `data/` par `{"$": "chemin"}`. Ces trois garde-fous servent tous les
modules suivants.

## D-036 — 20/10/2026 — Une fourchette de date, jamais une date seule

**Décision.** Tout module qui publie une date ou une durée de projet publie aussi les deux bornes
obtenues en poussant toutes ses hypothèses V3 au même bout de leur fourchette.

**Raison.** D2 publiait une date unique issue d'une trentaine d'hypothèses déclarées avec leur
fourchette, sans jamais les exploiter — le défaut qu'il reproche aux plannings qu'il critique. Les
bornes donnent ici ×0,60 et ×2,41, soit 182 % d'étendue : le chiffre est inconfortable et il est la
mesure honnête de ce que vaut la date.

**Impact.** `variante_aux_bornes` et `fourchette_de_date` dans `calc/planification.py` ; le même
traitement est attendu de D1 sur les coûts et de D4 sur les prévisions à terminaison.

## D-037 — 21/10/2026 — Un ratio de contrôle ne vaut que sur son domaine de définition

**Décision.** Tout ratio de vérification publié par le cours nomme la **base** sur laquelle il est
calculé, et le calcul **refuse de rendre un verdict** sur une base où le ratio n'est pas défini.

**Raison.** La dette n° 10 vient d'une part de main-d'œuvre comparée à une fourchette de gros œuvre
alors qu'elle était calculée sur un bordereau entier — qui porte des fournitures sans heures et des
forfaits dont les heures existent sans être visibles. Le module D1 le montre : sur la bonne base, la
part vaut 7,8 % au lieu de 1,0 %. L'alerte était réelle, la base ne l'était pas.

**Impact.** `controle_ratios` dans `calc/prix.py` porte un champ `ratio_defini_sur_cette_base`, et un
test vérifie qu'une base non définie ne peut jamais être déclarée « dans la fourchette ». La règle
s'applique à D4 (indices de performance) et à D7 (consolidation multi-sites).

## D-038 — 21/10/2026 — La dette n° 10 est chiffrée, et elle n'est pas soldée

**Décision.** Les cadences V3 du cours restent en l'état pour la v1, et D1 publie leur **facteur de
recalage** poste par poste au lieu de les corriger en silence.

**Raison.** Retourner chaque cadence d'atelier en productivité par compagnon — kilos d'acier posés,
m² de coffrage, m³ de béton par homme et par jour — donne un facteur **pondéré par le travail** de
**×1,92**, obtenu par un chemin indépendant de celui qui avait produit le soupçon. Mais les cadences
n'en sortent pas du même côté : celle des dalles est à ×4,17, celle des semelles à ×0,78. Corriger
par un facteur global écraserait cette information ; corriger cadence par cadence reviendrait à
inventer des valeurs que rien n'étaye mieux que les précédentes.

**Correction du 21/10 (passe adversariale de D1).** La première version annonçait ×2,52, obtenu par
une moyenne **non pondérée** sur les postes : elle comptait deux fois la cadence des dalles, que le
radier et le plancher haut partagent, et omettait le terrassement, dont la productivité de référence
était pourtant déclarée. Le facteur pondéré est ×1,92. Le soupçon de la dette n° 10 — « optimistes
d'un facteur 2 à 3 » — est donc **confirmé dans son sens et revu à la baisse dans son ampleur**, et
c'est ainsi qu'il faut l'écrire.

**Impact.** `variante_recalee` publie ce que deviendraient durée (+59 %), déboursé (+8 %) et part de
main-d'œuvre (7,8 → 13,1 %) si l'on recalait. Même recalée, la part reste sous la fourchette : le
recalage explique l'essentiel de l'écart, pas tout. Seuls des attachements réels trancheraient, et
le cours n'en a aucun. C'est écrit dans le module, pas en note de bas de page.

## D-039 — 21/10/2026 — L'état d'avancement est partagé entre les modules, pas recalculé par chacun

**Décision.** L'avancement d'un chantier à une date — planifié, constaté, déclaré — vit dans
`calc/etat.py`, et les modules qui en ont besoin le lisent. Aucun ne le saisit.

**Raison.** En écrivant D4, l'avancement déclaré de la situation de D1 s'est révélé incohérent avec
le planning : il était saisi à la main dans `data/`, décrivait un état de chantier correspondant au
2ᵉ mois, et la situation s'annonçait au 7ᵉ. Aucun contrôle ne pouvait le voir — les deux nombres
étaient justes séparément. Pire, D4 allait viser une situation calculée sur un tableau d'avancement
différent du sien : le montant retiré au visa n'aurait eu aucun rapport avec le montant déposé.

**Impact.** `avancement_planifie` est dérivé des segments de travail de D2 ; `trois_etats` en déduit
le constaté et le déclaré à partir des écarts déclarés dans `data/suivi_chantier`. La situation de
D1 et le visa de D4 portent désormais sur le même tableau, et un test le vérifie. La date d'arrêt
est unique et vit dans `suivi_chantier.date_arret_j`.

**La leçon, pour les modules suivants** : quand deux modules ont besoin de la même grandeur d'état,
la question n'est pas « comment la recalculer pareil ? » mais « où la mettre pour qu'elle n'existe
qu'une fois ? ».
