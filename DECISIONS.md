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
