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

## D-040 — 26/10/2026 — Un effet sur le planning se mesure en rejouant le réseau, il ne se déduit pas d'un type de marge

**Décision.** Quand un module doit savoir si une décision retarde le chantier, il **rejoue le
réseau de D2** avec la nouvelle durée et lit la date de fin. Il ne compare pas la rallonge à une
marge.

**Raison.** C3 déclenchait les frais de durée dès que la rallonge dépassait la marge **libre**,
alors que la question posée — « la fin du chantier bouge-t-elle ? » — appelle la marge **totale**.
Il imputait 154 611 MAD à un parc de coffrage qui ne retardait rien, et l'optimum basculait de 430 à
850 m². Le module publiait pourtant, deux lignes plus bas, la marge totale (39,81 j) et la clé
`le_plancher_porte_t_il_la_date = false`. Choisir le bon type de marge est une question piégeuse qui
reviendra à chaque module ; la mesurer ne l'est pas.

**Impact.** `impact_sur_le_chantier` rejoue `planification` et publie `retard_du_chantier_j` et
`le_plancher_devient_critique`. Les lignes du tableau portent en plus leur **régime** — dans la
marge libre, entre libre et totale, au-delà — parce que les trois ne se traitent pas de la même
façon : gratuit au sens des frais de durée n'est pas gratuit au sens du risque.

**Portée** : toute question « est-ce que ça retarde ? » dans les modules suivants (B3e, C7, REC).

## D-041 — 26/10/2026 — Un optimum de coût n'est pas une décision, et le module doit le dire

**Décision.** Quand un module publie un optimum, il publie **à côté** ce que le modèle ne price pas,
et le prix de l'autre choix. L'optimum n'est jamais présenté comme la recommandation.

**Raison.** Corrigé de D-040, l'optimum de coût du parc de coffrage tombe sur **le plus petit parc
testé** (430 m², une seule zone de coffrage) : il coûte 85 020 MAD contre 163 265 pour le parc
déclaré, et il consomme 32,55 des 39,81 jours de marge totale du plancher. Le calcul est juste, et
suivre son verdict serait imprudent : il parie qu'aucun aléa ne touchera le plancher pendant trois
mois. Un module qui publie « optimum : 430 m² » et s'arrête enseigne le contraire du métier.

**Impact.** `plus_petit_parc_sans_rallonge` (1 300 m²), `ecart_entre_les_deux_choix_MAD` (78 245 MAD
— le prix de l'assurance) et `ce_que_le_cout_ne_decide_pas` sont publiés et lus par le module. La
thèse de C3 est désormais celle-là. Et le test qui épinglait la conclusion narrative (« l'optimum
n'est ni le plus petit ni le plus grand ») est remplacé par le test de la **règle**.

## D-042 — 26/10/2026 — Un indice qu'on ne peut pas définir se publie comme indéfini

**Décision.** Un indice de performance dont l'assiette est vide ne reçoit pas de valeur de
substitution : le module publie l'absence et nomme ce qui répond à la place.

**Raison.** D4 annonçait comme contribution un « SPI du chemin critique ». À la date d'arrêt, aucune
des six tâches à marge nulle n'a commencé : l'indice est un 0/0. Le nombre publié
(0,9774) portait en réalité sur la plus **longue chaîne** démarrée, dont la plupart des tâches ont
jusqu'à 199 jours de marge. Le calcul était juste, l'objet mesuré ne l'était pas — et un indice qui
porte un nom qu'il ne mérite pas se lit comme s'il le méritait.

**Impact.** `ce_qui_porte_la_date` remplace `spi_du_chemin_critique` et publie
`un_indice_sur_elles_est_il_defini: false`, puis la **marge totale restante** par tâche dérivée
(CHFA : 6,67 j sur 17,47). S3c, S4c, l'exercice 2, le quiz Q4 et la fiche mémo sont réécrits autour
de cette réponse. Même règle pour les pourcentages : l'écart entre avancement physique et
avancement temporel compare deux dénominateurs différents et ne conclut aucun avance-retard — le
seul lisible est constaté contre planifié à la même date (−3,42 points, un retard, là où l'écart au
temporel suggérait +11,98 d'avance).

**Portée** : prolonge D-037 (domaine de définition d'un ratio) au cas où le domaine est **vide**.

## D-043 — 26/10/2026 — Une comparaison circulaire n'est pas une seconde voie, et le module doit le dire

**Décision.** Quand les deux termes d'une comparaison viennent de la même source, le module écrit
que ce n'est pas une vérification au sens du § 3.3, et nomme ce qui garantit vraiment le résultat.

**Raison.** B3e comparait le métré de son plan au ratio kg/m³ et concluait « l'ordre de grandeur
tient ». Mais le plan fictif avait été *calibré* sur ce même ratio quelques heures plus tôt : la
comparaison vérifiait le calibrage, et le résultat était une tautologie. Pire, un test épinglait la
conclusion — « le plan reste dans la fourchette » — c'est-à-dire exactement le défaut que C3 avait
dû corriger (D-041). Un cours qui se décerne une vérification qu'il n'a pas faite enseigne la
mauvaise habitude en même temps que la bonne méthode.

**Impact.** La section devient « contrôle d'ordre de grandeur », `_ce_n_est_pas_une_seconde_voie`
est publié et lu, le test de conclusion est remplacé par le test de la règle, et le module nomme ce
qui garantit le métré : l'étalonnage externe de la masse linéique, la vérification dimensionnelle,
et une **seconde traversée depuis le dessin** (0,005 % d'écart), dont la portée exacte est écrite —
elle vérifie la chaîne de calcul, pas le plan.

**Portée** : tout module qui calibre une donnée sur une référence perd le droit de s'en servir comme
contre-calcul. À vérifier dans B7c, où les deux voies du nombre de plages partagent le rendement.

## D-044 — 26/10/2026 — Un plan pédagogique n'a pas le droit de contredire ce que le module en dit

**Décision.** Une donnée fictive peut être non dimensionnée ; elle ne peut pas contredire une
affirmation du module qui la commente. Quand le module dit « la logique se voit », la donnée doit la
montrer.

**Raison.** Le plan de ferraillage de B3e portait 13,4 cm² d'acier sur appui intermédiaire contre
24,2 cm² en travée, pendant que la légende de sa figure 2 écrivait « les chapeaux à cheval sur les
appuis : la logique se voit sans aucun calcul, c'est la forme du moment ». Sur trois travées égales,
le moment sur appui vaut environ 1,25 fois celui de travée : l'acier supérieur devait dépasser
l'inférieur. C'est de la RDM pure, V1, et la phase § 5.0 ne protège pas de cette erreur-là — elle
interdit de dimensionner, pas de respecter l'équilibre.

**Impact.** B2 passe à 5 HA25, rapport 1,18, et un test l'impose avec ses bornes. Le mot « fictif »
ne couvre plus rien : il dit que le plan n'est pas vérifié, pas qu'il peut être incohérent.

## D-045 — 27/10/2026 — Une plage de consignation est une plage de NUIT, et la tâche sous interception paie son rendement

**Décision.** Les consignations du cas phare sont des plages de **nuit de 6 h**. La durée d'une tâche
sous interception est multipliée par le **facteur d'interception** — rendement du temps × abattement
de cadence de nuit — calculé une seule fois dans `calc/plage.py` et lu par D2 comme par B7c.

**Raison.** D2 donnait à la tâche de levage sous consignation la durée d'un travail de jour, puis la
logeait dans des fenêtres comme si chacune produisait huit heures. Or une plage de 6 h ne laisse que
**2,85 h** de travail : prise de possession, consignation caténaire, amenée, repli, déconsignation et
marge de restitution en consomment 3,15 h, dont 1,25 h tenues par l'exploitant et que rien
n'accélère. Avec l'abattement de cadence de nuit, le facteur vaut **×4,01**. Le lecteur a tranché
entre l'hypothèse « journée » que `data` déclarait et l'hypothèse « nuit », plus conforme à une
ligne en service.

**Impact.** Chantier **363 → 600 jours ouvrés**, fin 2028-05-01 → **2029-04-23**. Le levage passe de
5 à 17 fenêtres. D1 (frais de durée, trésorerie) et D4 (BAC, avancements) suivent par le build ;
C3 rejouait déjà le réseau et suit seul. La phrase de D2 qui disait « un chantier de dix-huit mois »
est devenue une variable.

**Ce qui n'est PAS décidé ici** : la méthode de montage. Voir D-046.

## D-046 — 27/10/2026 — 600 jours n'est pas une réponse : les leviers sont en études, et ils se mesurent

**Décision.** B7c publie les leviers et l'effet **mesuré** de chacun en rejouant le réseau, nomme ce
que le calcul ne price pas, et **ne choisit pas** à la place du lecteur. La durée de référence du
cours reste celle de la méthode déclarée aujourd'hui.

**Raison.** Un planning qu'on rallonge de onze mois pour absorber un rendement de 48 % est un
planning que personne n'a discuté. Les leviers existent et aucun n'est dans le planning : négocier
une plage plus longue (−137 j pour 8 h), pré-assembler au sol pour réduire la part levée sous
interception (−195 j à 15 %), ou les deux (**−237 j**, soit 363 jours — exactement la durée que le
cours publiait avant la correction). Le planning initial avait raison **par accident** : il était
atteignable, mais seulement avec une méthode de montage et une stratégie de plages que personne
n'avait écrites.

**Impact.** `leviers()` rejoue le réseau pour chaque combinaison (D-040). Chaque ligne porte sa
contrepartie — emprise au sol, grue plus forte, arbitrage de l'exploitant contre la circulation — et
le module signale les leviers qui **sortent de la fourchette déclarée** : réduire la part sous
interception à 15 % n'est pas choisir une valeur basse de l'hypothèse, c'est adopter une autre
méthode de montage.

**Ce qui reste au lecteur** : adopter ou non une combinaison. Tant qu'il ne l'a pas fait, le cours
porte la durée de la méthode actuelle, et dit pourquoi.

## D-047 — 27/10/2026 — L'exposition au risque se compte en heures, et le cours en a désormais le droit

**Décision.** Tous les indicateurs de sécurité du cours portent des **heures travaillées** au
dénominateur, lues dans `planification.json → heures_de_main_oeuvre_par_tache`. Jamais un effectif,
jamais une durée.

**Raison.** C'est la seule assiette qui absorbe à la fois l'effectif et la durée : dix compagnons
pendant deux ans et cent pendant deux mois n'ont ni le même risque ni le même nombre d'heures. C'est
le même raisonnement que D4 applique aux avancements — un pourcentage sans dénominateur ne se
compare à rien.

**Ce qui l'a rendu possible.** Jusqu'à la passe de B7c, le cours n'avait pas d'heures fiables : D1
et D2 en publiaient deux jeux, dans un rapport de quatre sur la tâche sous consignation. Le contrôle
croisé mis en place à cette occasion garantit maintenant qu'ils trouvent les mêmes. **Sans lui,
l'indicateur central de C7 aurait été faux, et il aurait eu l'air juste.**

**Impact.** C7 publie l'exposition par tâche, la part de la nuit dans les heures (8,0 %) et dans le
risque pondéré (13,5 %), et le nombre d'accidents qu'un taux de référence appliqué à ces heures
donnerait — avec la mention explicite que ce n'est ni une prévision ni un objectif.

## D-048 — 27/10/2026 — Une non-conformité se hiérarchise sur sa marge ; un risque, jamais

**Décision.** Le cours distingue explicitement deux logiques de priorisation qui cohabitent dans le
même tableau de bord : la **qualité** se hiérarchise sur la marge de l'ouvrage, la **sécurité** ne
se hiérarchise pas ainsi.

**Raison.** La même non-conformité, sept jours d'immobilisation, donne trois résultats mesurés en
rejouant le réseau : **absorbée** sur un ouvrage à grande marge, **transmise** intégralement sur un
ouvrage à marge nulle, et **amplifiée d'un facteur six** sur une tâche sous consignation — qui ne
rate pas sa reprise mais sa fenêtre, un mois plus tard. Rien de cela ne se voit sur le chantier :
les trois ouvrages se ressemblent.

Mais appliquer la même règle à la sécurité serait une faute : un risque de gravité maximale se
traite quelle que soit la marge de la tâche. On n'arbitre pas une vie contre un rang, et les deux
logiques doivent être nommées pour ne pas se contaminer.

**Impact.** `impact_sur_le_planning` choisit les tâches comparées **par leur marge**, jamais en dur —
le classement change dès que le planning change, ce qui vient d'arriver. Et C7 publie la criticité
comme un **ordre** : cinq risques y sont ex æquo, et le module dit que c'est une propriété des
échelles courtes, pas une équivalence des risques.

---

## D-049 — 27/10/2026 — Un résultat publié sans ses bornes est une fausse précision

**Décision.** Tout résultat chiffré d'un module publie ses **deux bornes** à côté de sa valeur, et
le module dit **laquelle de ses entrées** porte l'incertitude. La règle D-036, qui n'imposait les
bornes qu'aux dates et aux durées, est étendue aux coûts, aux taux, aux tonnages et aux parts.

**Raison.** La passe adversariale de C7 a recalculé le module à ses propres fourchettes : coût
d'une non-conformité de 45 601 à 348 165 MAD, accidents attendus de 0,71 à 3,38, part de la nuit
dans le risque de 9,4 à 20,7 %. Le module publiait une valeur unique, au centime dans les figures.
Toutes ses entrées sont pourtant des hypothèses déclarées à fourchette large : la précision
affichée était celle de l'arithmétique, pas celle de la connaissance.

**Et une conséquence qui ne se voyait pas sans les bornes** : ce qui résiste au balayage n'est
jamais le montant, c'est le **rapport**. L'écart entre les trois régimes de coût reste d'un ordre
de grandeur quelles que soient les bornes retenues ; c'est donc lui que le module enseigne, et le
montant n'est qu'une illustration. Publier les bornes a changé ce que le module dit, pas seulement
ce qu'il affiche.

**Impact.** `calc/qualite.py` publie des bornes sur l'exposition, le coût, les déchets et les
taux ; cinq tests de règle vérifient que la valeur nominale tombe entre ses bornes, dans l'ordre.
Les figures sont arrondies à trois chiffres significatifs (§ 3.6), et un canari refuse toute valeur
de figure publiée au centime.

---

## D-050 — 27/10/2026 — Les bornes d'un retard se mesurent ; et sous consignation, le retard est quantifié

**Décision.** Les bornes d'un retard ne se déduisent jamais d'une règle de trois sur
l'immobilisation : le réseau est **rejoué** à chaque borne (D-040 appliqué aux bornes elles-mêmes).
Et les paliers obtenus sont publiés comme tels.

**Raison.** Six rejeux du réseau, de une demi-journée à vingt-cinq jours d'immobilisation, ne
rendent que **deux retards distincts** : 20 et 40 jours ouvrés, soit un et deux fois la période
entre deux fenêtres de consignation. Une demi-journée perdue coûte déjà le palier entier ; les
dix-neuf jours suivants ne coûtent rien de plus. La règle de trois, elle, aurait donné 7 et 46
jours — deux nombres qui ne sortent d'aucun réseau, et une pente là où il y a une marche.

Trois conséquences de pilotage en découlent, et aucune n'était dans le module avant la mesure :
avant la fenêtre tout se joue sur quelques heures ; une fois la fenêtre ratée, se presser ne
rachète rien ; et ce qui se négocie n'est pas la durée de la reprise mais la **période des
fenêtres**, qui appartient à l'exploitant et que personne ne borne jamais — alors qu'elle déplace
la fin du chantier de 510 à 750 jours ouvrés à elle seule.

**Correction d'un chiffre de D-048.** Cette décision-là, écrite avant la correction des bloquants
de B7c, citait « un facteur six » et « deux fenêtres ». Le réseau corrigé donne **×2,86 et une
seule fenêtre** pour sept jours d'immobilisation. La thèse de D-048 est inchangée ; son chiffre
était celui d'un réseau faux, et l'explication « la fenêtre suivante, un mois plus tard » n'aurait
de toute façon expliqué que la moitié du retard qu'elle accompagnait.

---

## D-051 — 27/10/2026 — Un prix porte une note qui dit à quoi il s'applique ; l'ignorer est une erreur invisible

**Décision.** Avant d'employer un prix de `data/`, on lit la **note** qui l'accompagne. Un poste
dont la note dit « compagnon, charges comprises » ne paie pas une heure de contrôle, une heure
d'encadrement ni une heure d'études.

**Raison.** C7 chiffrait le durcissement du contrôle après une non-conformité — des heures de
maîtrise d'œuvre et de bureau d'études — au taux horaire du compagnon, et concluait sur cette
ligne-là que « le durcissement ne pèse rien ». Le taux était sous-estimé d'un facteur trois. La
conclusion survit au bon taux, et c'est précisément ce qui rend l'erreur dangereuse : rien dans le
résultat ne la signale. Elle n'a été trouvée qu'en lisant la note attachée au prix.

**Impact.** `prix_unitaires_MAD.ressources.main_oeuvre_MAD_h.controleur` : 140 MAD/h (90 à 240),
recoupé sur les frais d'encadrement du module D1. Un test exige que ce taux soit strictement
supérieur à celui du compagnon, et la vérification dimensionnelle contrôle que la ligne vaut bien
un taux horaire multiplié par des heures.

---

## D-052 — 27/10/2026 — Un chantier n'a qu'un plan de contrôle, à trois mailles emboîtées

**Décision.** Quand plusieurs modules publient des contrôles du même ouvrage, chacun **déclare sa
maille** et **renvoie** aux deux autres. Et chaque ligne porte deux colonnes distinctes : qui
**exécute** le contrôle, qui le **vise**.

**Raison.** Trois listes coexistaient sans se connaître : six contrôles d'ensemble (C7), cinq
points d'arrêt du cycle de gros œuvre (C3), sept contrôles d'armatures (B3e). Deux d'entre elles
attribuaient le même acte à des acteurs différents — l'affaissement au cône à l'entreprise ici, à
la maîtrise d'œuvre là. Les deux attributions étaient justes, parce que ce ne sont pas les mêmes
actes : l'entreprise fait l'essai, la maîtrise d'œuvre vise l'autorisation de bétonnage dans la
minute qui suit. Une seule colonne « qui » ne pouvait pas porter les deux, et c'est ainsi qu'un
contrôle finit par n'être fait par personne — chacun croyant que c'est l'autre.

**Impact.** Les six lignes de C7 portent `qui`, `visa`, `point_d_arret`, `duree_h` et
`detaille_par` ; le périmètre du plan et l'articulation des trois mailles sont publiés et testés.
La règle sur les critères chiffrés est précisée au passage : un critère **peut** porter une valeur
à condition de nommer le document dont elle vient et de marquer ⏸ ce qui est normatif. C'est la
forme que B3e emploie ; C7 la condamnait sans la nuancer, et condamnait donc un module livré.

---

## D-053 — 27/10/2026 — Un indicateur se publie avec son assiette, ou il ne se publie pas

**Décision.** Tout indicateur rapporté à un dénominateur publie **le périmètre de ce
dénominateur** : quelles heures, de quelles entreprises, sur quelle période.

**Raison.** C7 écrivait que le cours connaît ses heures « exactement, tâche par tâche ». Deux
frontières étaient tues. La première : l'assiette ne couvre que les heures **sur site** — les
études, le séchage et surtout la **fabrication en atelier** de 312 tonnes de charpente en sont
exclus, avec tout le soudage et le meulage qu'ils représentent. La seconde, plus piégeuse : la
tâche la plus lourde de l'assiette pèse 46 % des heures et est très probablement sous-traitée. Un
taux de fréquence calculé sur le seul périmètre de l'entreprise générale serait structurellement
meilleur sans qu'aucun accident ait été évité — il aurait simplement retiré du dénominateur les
heures les plus exposées.

**Impact.** C7 publie ses deux frontières, leur conséquence (un taux de chantier ne couvre pas
l'atelier : il faut le demander au fabricant) et la règle des trois questions à poser devant tout
taux présenté. Même raisonnement que D4 sur les avancements : un pourcentage sans dénominateur
n'est pas un indicateur.

---

## D-054 — 28/10/2026 — Avant de chercher une donnée qui manque, regarder si la question porte sur un rapport

**Décision.** Quand une décision bute sur une donnée indisponible, on écrit d'abord la comparaison
en entier : si la donnée manquante figure des deux côtés, elle se simplifie et la décision se prend
sans elle.

**Raison.** Le module REC devait comparer le coût de porter la retenue de garantie à celui d'une
caution qui la remplace. Les deux coûtent « taux × montant × durée », et la durée est celle de la
garantie — une valeur réglementaire, donc **⏸** dans ce cours. Le réflexe était de déclarer le
calcul impossible. Or le montant et la durée sont les mêmes des deux côtés : leur rapport vaut
7,0 ÷ 1,2 = 5,83, et il ne contient ni l'un ni l'autre. La donnée manquante était inutile.

Le même réflexe sert ailleurs : dans l'exercice 1 du module C7, les heures annuelles d'un compagnon
sont une hypothèse à ±10 % qui porte tout le calcul — et le **rapport** des deux taux de fréquence
n'en dépend pas du tout. Et dans l'exercice 1 de REC, le montant du marché disparaît du jour de
bascule des pénalités pour la même raison : il est au numérateur et au dénominateur.

**Impact.** Deux invariants étalonnés sur cas fermes (`calc/etalonnage/reception_cas_ferme.py`) :
le jour de bascule ne dépend pas du montant du marché, vérifié sur trois marchés d'un facteur mille ;
l'arbitrage retenue/caution ne dépend ni de la durée ni du montant, vérifié sur trois montants. Ce
sont des invariants, pas des valeurs : ils restent vrais quand les hypothèses changent.

---

## D-055 — 28/10/2026 — Un module qui arrive après confronte ses chiffres à ceux dont il hérite

**Décision.** Quand un module tardif pose une grandeur qu'un module antérieur avait déjà posée
autrement, il **publie l'écart** plutôt que de choisir en silence — et il dit explicitement que
l'écart oppose deux chiffres de ce cours, non qu'il révèle une erreur du monde réel.

**Raison.** Le module D2 porte une tâche « Réception » de dix jours ouvrés, posée sans la
décomposer. Le module REC décompose la séquence et en demande vingt-six, une fois retirée la mise
en service que le planning porte déjà sous un autre nom. Le réseau rejoué décale la fin de
**16 jours ouvrés**, soit 2 045 592 MAD au prix du jour de non-réception.

Deux pièges étaient à éviter, et ils tirent en sens contraire. Taire l'écart aurait laissé deux
nombres incompatibles dans le même cours. Le présenter comme une découverte aurait été malhonnête :
les deux durées sont des décisions de ce cours, et l'écart mesure surtout l'ordre dans lequel les
modules ont été écrits. Ce qui se généralise n'est donc pas le chiffre, c'est le **mécanisme** —
une tâche « Réception » non décomposée est presque toujours trop courte, parce qu'on y pense comme
à une signature alors que c'est une séquence, et parce que la moitié de sa durée n'appartient pas à
l'entreprise.

**Impact.** `confrontation_au_planning` mesure le décalage en rejouant le réseau (D-040) au lieu de
le déduire de la marge ; un test vérifie que le décalage mesuré ne dépasse jamais l'allongement
appliqué, et que la mise en service n'est pas comptée deux fois. L'écart est versé en dette : la
date de fin publiée par D2 ne comprend pas une réception décomposée.

---

## D-056 — 28/10/2026 — Une grandeur empruntée porte une condition d'emploi, et elle est dans son nom

**Décision.** Quand un module lit une grandeur publiée par un autre, il vérifie **sous quelle
condition elle vaut**, et pas seulement son unité. La condition se cherche dans le NOM de la
grandeur et dans ce qui l'indexe ; quand elle existe, le module qui emprunte la publie avec elle.

**Raison.** Le module D1 publie `cout_du_retard`, indexé par un nombre de jours **de retard** : les
pénalités n'y courent que parce que le terme contractuel est dépassé. Le module REC en a fait un
« coût d'une journée de non-réception » et l'a appliqué à des journées qui ne sont pas en retard —
les opérations préalables, l'hésitation sur une liste de réserves, le vendredi d'un exercice. Les
cinq montants de sa fiche mémo étaient multipliés par **7,9**.

Rien ne pouvait le détecter. L'arithmétique était juste au centime, les unités étaient homogènes,
l'étalonnage passait, les seize contrôles de la chaîne étaient verts, et la passe adversariale
elle-même a recalculé les six grandeurs du module et les a toutes retrouvées. Ce qui était faux
n'était pas un nombre : c'était le DOMAINE d'emploi d'un nombre juste. C'est la même faute que
D-037 nomme pour les ratios, portée cette fois d'un module à l'autre.

**Et la correction a produit un meilleur résultat que la version fautive.** Il n'y a pas un prix
mais deux, parce qu'il y a trois périodes dont la première et la dernière se ressemblent : avant le
terme contractuel et après le plafond des pénalités, un jour coûte les frais de durée seuls ; entre
les deux, huit fois plus. Le coût d'un jour n'est donc pas croissant dans le temps — c'est une
**fenêtre de cherté**, et savoir si l'on est dedans change toutes les décisions de fin de chantier.

**Impact.** REC publie trois périodes, deux régimes de coût et toutes ses conséquences chiffrées
dans les deux ; un invariant d'étalonnage vérifie que les deux régimes extrêmes coûtent exactement
la même chose. Et la première question de sa check-list de fin de chantier est devenue : *sommes-
nous en retard ?*

---

## D-057 — 28/10/2026 — Une liste se hiérarchise par son délai le plus long, pas par son volume

**Décision.** La durée de traitement d'un ensemble de tâches qui se recouvrent est le **maximum**
de son temps de travail cumulé et du plus long délai de tiers qu'il contient — jamais leur somme,
jamais le seul temps de travail.

**Raison.** REC chiffrait la levée de sept réserves bloquantes à 0,88 jour, en divisant des
heures-homme par une capacité d'atelier, alors que l'exercice du même module décrivait l'une
d'elles comme un escalator « en attente d'une pièce annoncée sous dix jours ». Un plan fictif ne
doit pas contredire ce que le module en dit (D-044), et ici c'est le texte qui avait raison contre
le calcul. Avec le délai de tiers, la levée des bloquantes passe de 0,88 à **10 jours**, et le coût
de les confondre avec les autres tombe d'un facteur 4,5.

Le résultat qui en sort vaut mieux que celui qu'il remplace : **ce n'est pas le volume qui fait la
durée, c'est l'attente**. Les sept réserves bloquantes représentent moins d'une journée de travail
et dix jours de calendrier ; les quatre-vingt-quatorze autres représentent douze jours de travail et
aucune attente. Mettre plus de monde ne sert à rien dans le premier cas et à tout dans le second —
c'est le chemin critique d'un planning, appliqué à une liste de réserves, et c'est la même leçon que
le module D2 enseigne sur un réseau.

**Impact.** `_duree_de_levee` publie, pour chaque ensemble, son temps d'atelier, son plus long délai
de tiers, la durée retenue et **ce qui la commande**. Deux invariants étalonnés : doubler la
capacité ne change rien quand un tiers commande, et divise la durée par deux quand c'est l'atelier.

---

## D-058 — 28/10/2026 — Un dossier à corriger se plante avec les erreurs qu'on a vraiment commises

**Décision.** Les erreurs de la revue critique de palier (§ 5.5) ne sont pas inventées : elles sont
choisies parmi celles que le cours a **réellement commises**, une par famille, et chacune porte le
module où elle s'est produite, le rapport de la passe qui l'a trouvée et la décision qui en est née.

**Raison.** Une erreur inventée se repère à son air d'erreur. Celles-ci ont deux propriétés qu'on
ne fabrique pas. Elles sont **réalistes**, puisqu'elles ont été commises par quelqu'un qui
connaissait la règle et l'écrivait trois paragraphes plus loin — le module C7 imputait des frais de
durée à un ouvrage dont il publiait la marge deux sections après. Et elles sont **presque
invisibles aux contrôles** : les rapports de `QA/` comptent plus de quatre-vingt-dix bloquants sur
un dépôt dont les seize contrôles de la chaîne étaient verts à chaque fois, et deux seulement ont
été trouvés par un contrôle écrit — deux canaris, c'est-à-dire des tests écrits pour **chercher**.

Le compte lui-même est une leçon. La première version de cette décision annonçait « 309 défauts
dont 79 bloquants sur dix passes » : les trois nombres étaient faux, et c'est le pire défaut qu'un
module sur la relecture puisse commettre. Ils sont maintenant **comptés dans les rapports à chaque
build**, avec la limite du comptage déclarée à côté du résultat.

Elles ont aussi une propriété commune qui fait toute la valeur de l'exercice : **leur arithmétique
est juste**. Aucune ne se trouve en refaisant une addition. Elles se trouvent en posant sept
questions sur une grandeur — de quel calendrier, sous quelle condition, quelle unité, quel domaine,
quel dénominateur, mesuré ou déduit, quelle marge. C'est cela qu'un chef de projet suivi doit
savoir faire, et aucun tableau de bord ne le fait à sa place.

**Impact.** `calc/revue.py` construit le dossier depuis les sorties réelles des modules du palier,
puis mute sept lignes par une fonction déclarée : le corrigé est la comparaison, il ne peut pas
dériver. Trois tests le tiennent : la **bijection** entre lignes fausses et corrigé ; qu'une erreur
**déplace réellement son nombre**, sauf si son écart est nul — elle est alors une erreur de lecture
et doit porter son explication propre, règle nommée par sa **propriété** et non par l'identifiant
de l'erreur ; et que **le chemin annoncé par chaque ligne donne bien sa valeur**. Ce dernier
manquait, et c'est ainsi qu'une ligne a pu citer un module qui ne publiait pas sa valeur : le
lecteur qui l'aurait signalée aurait eu raison contre le corrigé.

Quatre lignes justes servent d'appâts : un relecteur qui ne sait pas dire « RAS » avec sa preuve
n'est pas un relecteur, et l'Annexe 4 l'exige déjà de ses propres passes. Et une règle en est
sortie pour les appâts eux-mêmes : **un appât doit être défendable**, c'est-à-dire que le lecteur
qui le signale doit avoir tort — s'il a raison, ce n'est pas un appât, c'est un défaut.

---

## D-059 — 28/10/2026 — Une voie de raisonnement dont les bornes enjambent le seuil ne tranche pas

**Décision.** Quand un calcul sert à décider — franchir un seuil, choisir un nombre d'unités,
déclencher une dépense — et que ses **deux bornes tombent de part et d'autre du seuil**, sa valeur
nominale n'est pas publiée comme un argument. La voie est publiée avec son résultat, son incertitude
et la mention explicite qu'**elle ne tranche pas** ; la décision se prend sur les voies restantes.
Un champ `tranche` accompagne chaque voie dans la sortie de `calc/`, et un test vérifie que le
résultat retenu est le maximum des seules voies qui tranchent.

**Pourquoi.** C1 calcule le taux de charge d'une grue : **62,3 %**, donc une grue suffit. Ses bornes
vont de **14,6 à 334,4 %** : à la borne haute il en faudrait trois. Publier « 62 %, donc une grue »
aurait donné à la décision l'apparence d'un calcul, alors que le calcul ne dit rien — il dit « entre
une et trois » sur une question qui n'admet que des entiers. Deux autres voies, indépendantes et sans
terme commun, donnent toutes deux deux grues ; c'est elles qui décident, et le module le dit.

Le piège est subtil parce que la valeur nominale **tombe du bon côté**. Elle paraît confirmer la voie
géométrique, et un lecteur pressé y verra trois voies d'accord au lieu de deux. Un faux accord est
pire qu'un désaccord : il augmente la confiance sans augmenter l'information. Compter les voies qui
s'accordent n'a de sens que si chacune avait le droit de voter.

**Ce que ça ne veut pas dire.** Une voie qui ne tranche pas n'est pas une voie inutile : elle reste au
dossier comme ordre de grandeur, et surtout elle **désigne la mesure à aller chercher**. C1 en fait
un exercice : des trois hypothèses qui portent la largeur de la fourchette, laquelle se relève le
plus vite sur le chantier, et dans quel ordre. Le travail du chef de projet suivi n'est pas de
calculer mieux avec les mêmes hypothèses ; c'est de savoir quelle mesure rapporte le plus.

**Impact.** Rétroactif sur toute voie de décision du cours : `pourquoi_ce_parc` de C1 le porte, et la
règle s'appliquera à chaque module qui compare plusieurs chemins vers une même décision.

---

## D-060 — 28/10/2026 — La vérification dimensionnelle passe en dernier, parce qu'elle lit des sorties

**Décision.** `calc/verif_unites.py` est la **dernière** étape de `calc/run_all.py`, après tous les
calculs et tous les tests.

**Pourquoi.** Cette vérification ne relit pas le code source des bibliothèques : elle réécrit chaque
formule avec ses unités et la confronte aux **sorties publiées** dans `calc/sorties/`. Placée au
milieu de la chaîne, comme elle l'était depuis la tranche verticale, elle contrôlait donc les sorties
de l'exécution **précédente** pour tous les modules calculés après elle — c'est-à-dire, au dernier
état, pour sept modules sur onze. Une modification de `reception.py` n'était vérifiée
dimensionnellement qu'au build suivant, et une exécution entière pouvait passer au vert sur un
module dont les unités n'avaient jamais été contrôlées dans leur version courante.

Le défaut n'a produit aucune erreur connue, et c'est précisément ce qui le rendait durable : rien ne
le signalait. Il a été vu en ajoutant la section C1, dont la vérification lisait un fichier qui
n'existait pas encore au moment où elle s'exécutait.

**Impact.** Ordre de `ETAPES` modifié ; un commentaire en place explique pourquoi cette étape ne peut
pas remonter. La limite déjà déclarée en tête du fichier — une formule qui change dans la
bibliothèque sans changer ici n'est pas vue — reste entière : c'est une vérification de **cohérence
entre une écriture annotée et un résultat**, pas une analyse du code.

---

## D-061 — 28/10/2026 — Une fiche livrée écrit ses écarts avec la fiche d'origine, et leur raison

**Décision.** La fiche-module rédigée à la livraison (celles marquées « écrit le … » dans
`cadrage/05-sommaire.md`) **nomme chaque option qu'elle relève ou qu'elle abandonne** par rapport à la
fiche de l'Étape 0, avec la raison en une ou deux lignes. La fiche d'origine n'est pas réécrite : les
deux coexistent, et l'écart est lisible.

**Pourquoi.** Deux modules ont déjà dévié de leur fiche. C7 a **relevé** son O7 (contre-calcul), que
la fiche d'origine disait sans objet faute de calcul normatif : il y avait un noyau calculable, et
entièrement non normatif. C1 **abandonne** son O3 (modèle 3D), que la fiche d'origine portait comme
obligatoire : ce que la 3D y apporterait est la giration et l'interférence des flèches, alors que ce
que le module enseigne est la courbe de charge et la part servie, qui se lisent mieux sur un
diagramme et un plan masse cotés. Ajouter la maquette aurait été cocher une case, ce que le § 6.2
interdit explicitement.

Les deux écarts sont défendables ; aucun des deux n'était tracé. Sans trace, une fiche d'Étape 0
devient un document faux que personne ne relit, et le lecteur qui compare le sommaire au cours livré
y trouve des promesses non tenues sans savoir si elles ont été instruites ou oubliées. La différence
entre les deux est tout ce qui compte.

**Impact.** Les fiches livrées de B7c, C7 et C1 portent leurs écarts. Les fiches livrées de REC et de
RC1 ne sont pas encore écrites : versé en dette.

---

## D-062 — 29/10/2026 — Le maximum des voies donne un NOMBRE, jamais une durée

**Décision.** Quand plusieurs raisonnements indépendants mènent à la même décision de ressource, on
retient le **maximum** de ce qu'ils demandent — c'était déjà la règle — mais **chaque voie porte en
plus sa propre durée**, et la durée ne se prend pas au maximum. Elle se lit voie par voie, et celle
qui est retenue est celle de la voie qui **impose** le nombre retenu. Toute sortie de `calc/` qui
publie un besoin de ressource publie donc aussi sa fenêtre d'emploi, et le module nomme la voie qui
la paie.

**Pourquoi.** C1 conclut à deux grues à tour par deux voies indépendantes. La première — un conflit
de calendrier chez D2 — demande deux grues pendant **trois jours**. La seconde — un bâtiment de
120 m sous des flèches de 40 — en demande deux pendant toute la fenêtre du gros œuvre. Le module a
d'abord pris le nombre de l'une et la durée du chantier entier : **deux grues pendant 29,7 mois,
pour 117 jours ouvrés de besoin**. Le loyer publié valait cinq fois le besoin, la part fixe du coût
d'installation tombait à 17,9 % au lieu de 40,6 %, et la phrase « les quatre cinquièmes se jouent
sur la date de fin » était fausse : les grues sont démontées vingt mois avant la fin.

Le défaut est passé entre seize contrôles verts, cent vingt-huit tests, l'étalonnage et la
vérification dimensionnelle. Aucun ne pouvait le voir : les deux nombres sont des durées en mois,
ils sont homogènes, et ils vivent dans deux sections distantes du même module. Ce qui l'a trouvé est
une relecture qui a rapproché le profil de grue (jour 20 à jour 137) de la durée de location
(29,7 mois).

**La règle générale.** Un **frais de durée** se paie tant que le chantier dure : encadrement,
base-vie, gardiennage. Une **ressource** s'amène, sert, et s'en va. Un modèle de prix qui ne connaît
que des mois facture la seconde comme la première, parce que c'est l'hypothèse prudente — prudente
pour l'offre, chère pour la compétitivité. Trois conséquences que ce cours applique désormais :

1. « Gagner un mois » n'est pas une grandeur tant qu'on n'a pas dit **lequel** : sur ce chantier,
   225 000 MAD sur le gros œuvre et 35 000 MAD à la fin, un rapport de 6,4.
2. Un **trou** dans l'emploi d'une ressource est une décision chiffrable : garder les grues pendant
   les 2,2 mois qui précèdent la marquise coûte 421 800 MAD, les démonter et les remonter 840 000.
3. Une voie qui demande une ressource **trois jours** ne justifie pas de la louer à l'année : elle
   appelle un autre moyen, et c'est ce que le module D2 écrivait déjà sans que personne le lise.

**Impact.** `calc/installation.py` publie `fenetre_de_grue`, chaque voie porte sa `duree`, et le coût
se calcule avec deux horloges. L'écart avec le bordereau de D1 **change de signe** : D1 surestime de
1 723 300 MAD au lieu de sous-estimer de 2 821 500. Il reste publié et en dette (D-055), non corrigé
en silence. Le contrôle qui attraperait la même faute ailleurs — « toute grandeur multipliée par une
durée de chantier nomme la fenêtre d'emploi de ce qu'elle loue » — n'est pas outillé : dette 32.

---

## D-063 — 29/10/2026 — Un ratio ne se consolide pas ; un montant, si

**Décision.** Tout indicateur consolidé publié par ce cours est accompagné des **sommes** dont il
est le rapport, et tout tableau de bord multi-niveaux publie, à côté de ses ratios, les **montants**
qui s'additionnent : dérive à date et dépassement prévu par site. Un ratio agrégé n'est jamais
calculé comme une moyenne de ratios, et la moyenne, quand elle est montrée, est montrée **comme
fausse**.

**Pourquoi.** Le CPI d'une opération est ΣVA / ΣCR : une moyenne des CPI pondérée par les coûts
réels. La moyenne arithmétique des CPI donne ici 0,822 contre 0,877 — 5,5 points, et toujours dans
le sens du plus gros site, c'est-à-dire dans le sens qui rassure. Les deux nombres s'appellent « CPI
de l'opération » et un seul veut dire quelque chose.

La conséquence est plus large que l'arithmétique. Un indicateur consolidé **divise la dérive d'un
site par le poids de ce site** : le site secondaire pèse 12,9 % du coût réel, donc sa dérive arrive
amortie 7,8 fois. Il peut perdre 689 000 MAD de plus — 7 % de son budget — sans que le CPI consolidé
franchisse le seuil d'alerte. Et le mécanisme est **récursif** : ce que l'opération fait au site, le
site le fait à ses lots, de sorte qu'une dérive de lot arrive au sommet divisée par le produit des
poids.

Ce qui échappe à l'amortissement, ce sont les montants. La dérive de l'opération est la somme des
dérives, et le dépassement prévu à terminaison aussi. Mieux : leur **répartition** porte
l'information que les ratios cachent — le site secondaire fait 14 % du budget et 32 % du dépassement
prévu. C'est ce rapport-là qui dit où aller, et il ne se lit sur aucun CPI.

**Trois règles qui en sortent**, appliquées à partir de D7 :

1. un seuil d'alerte est fixé **par étage** d'agrégation et **avant** de lire les chiffres ; un seuil
   unique cascadé est un seuil différent à chaque étage, que personne n'a décidé ;
2. un site peu avancé n'a pas de CPI lisible (D4 publie la courbe d'incertitude) : on le **dit**
   plutôt que de le consolider en silence ;
3. ce que la direction lit en premier, ce sont deux montants — ce que l'opération va coûter, et quel
   site le cause.

**Impact.** `calc/pilotage.py` publie les quatre sommes, les poids, l'amortissement par site, le
seuil de masquage et le dépassement prévu par site. La figure 1 du module D7 montre la moyenne des
CPI **étiquetée comme fausse**, à côté du consolidé.

---

## D-064 — 29/10/2026 — Sur un chantier sous interception, le seuil d'alerte est une durée

**Décision.** Pour tout site dont le travail dépend de fenêtres de consignation, le seuil d'alerte
publié par ce cours est **la période entre deux fenêtres**, exprimée en jours, et non un pourcentage
de dérive ni une valeur de CPI. Il est publié à côté des indicateurs de coût, pas à leur place.

**Pourquoi.** Un cycle de consignation perdu ne produit **ni dépense ni valeur acquise** : le CPI du
site ne bouge pas d'un millième. Le SPI finit par bouger, mais il arrive amorti par l'agrégation
(D-063) et retardé par la latence du reporting — soit, sur ce chantier, 14 jours en moyenne en
rythme mensuel. L'information arrive quand elle ne sert plus.

Le module B7c avait établi la mécanique : sous consignation, un retard ne grandit pas, il **saute**
(D-050). D7 en tire la conséquence de pilotage. Le site secondaire accuse 22 jours de retard pour
une période de fenêtre de 20 : le retard effectif sur sa première interception n'est pas de 22 jours
mais de 40 — une amplification de 1,82. Et l'escalier a une propriété que le pilotage doit connaître
: **juste avant une marche, un jour gagné en vaut vingt ; juste après, il n'en vaut aucun.** Un
conducteur de travaux qui propose de « rattraper dix jours » sur un retard de 22 dépense sans rien
produire, parce que le travail attendra la même fenêtre.

**Le signal qui arrive à temps**, et c'est le second volet de la décision : la **marge à la date
limite de demande** de chaque interface. Le registre que B7c publie donne les délais ; la
soustraction donne les dates ; le classement par marge donne l'ordre du jour d'une revue. Sur ce
chantier, une demande à 180 jours de délai est déjà en retard de 13 jours à la date d'arrêt, et
aucun des cinq autres indicateurs du module ne le montre.

**Et le paradoxe, qui est publié plutôt que tu** : le retard du site **recule** sa date de besoin,
donc sa date limite de demande, donc il rend faisable la demande en retard (+8,6 jours de marge). Les
deux signaux pointent en sens inverse. Aucun tableau de bord ne tranche cela ; c'est une décision,
elle se prend avec l'exploitant, et elle s'écrit.

**Impact.** `calc/pilotage.py` publie `alerte_ferroviaire` (période, cycles perdus, amplification,
seuil) et `interfaces_a_date` (date limite, marge, statut par site), avec une figure en escalier et
une figure des marges. Les interfaces dont le besoin est déjà passé sont marquées « besoin déjà
servi » et ne comptent pas comme des retards : une liste d'alarmes éteintes ne se lit pas.
