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

## ⏳ EN ATTENTE de validation du lecteur (Étape 0, point e)

Ces points sont **proposés**, pas décidés. Ils passent en décisions datées dès réponse aux 10 questions
de `cadrage/00-questions-etape0.md`.

| ⏳ | Proposition | Question |
|---|---|---|
| P-01 | Jeu de données du cas phare, version `0.1-propose` → **figer en 1.0** (date + commit) | 3, 4 |
| P-02 | Site **S1 région de Marrakech** pour la gare + **S2 Agadir** pour le second site de D7 *(recommandation qui s'écarte du défaut du prompt)* | 3 |
| P-03 | Géométrie : 120 × 40 m, trame 7,50 m, hall 32 m de portée, mezzanine +5,00, marquise 4,50 m, passage souterrain | 4 |
| P-04 | Matrice de référentiels : option **M** (béton, séisme) + **E 1re génération** (acier) | 2 |
| P-05 | Tableau de calibrage [M]/[C]/[N] des 35 modules du périmètre technique | 5 |
| P-06 | **Addition au périmètre : module B7c** « Bâtiments ferroviaires : interfaces voie, quais, systèmes, exploitation » (P1, [N], actif) | 5 |
| P-07 | Deux lignes ajoutées à la matrice de référentiels : `ferroviaire-batiments`, `effets-foule-gare` | 2 |
| P-08 | Ordre de livraison du palier 1 : **le métier du lecteur d'abord** (D2, D1, D3, D4, D7), puis l'exécution, puis les fondamentaux | 6 |
| P-09 | Ordre de coupe, avec **O6 et P3 inversés** par rapport à la lettre du § 5.1d et le cas R+5 ajouté en rang 5 | 6 |
| P-10 | Budget de 5 modèles 3D pour le palier 1 actif (+9 à la levée du § 5.0), révisé après la tranche verticale | 6 |
| P-11 | Passe **/devil portée par un sous-agent distinct** qui ne lit pas le raisonnement de l'auteur | 8 |
| P-12 | **Deux dates** de fin de palier 1 : une ferme (palier 1 actif), une indicative (palier 1 complet) | 1 |
| P-13 | Détacher la **partie exécution de B5a** (charpente : fabrication, soudage, levage) en module actif, puisqu'elle ne dépend d'aucune norme | 6 |
| P-14 | Prix : année de référence 2026, prix unitaires V3 en fourchettes | 7 |
| P-15 | Format : HTML responsive hors ligne, KaTeX pré-rendu, ≤ 1,5 Mo par module | 9 |
