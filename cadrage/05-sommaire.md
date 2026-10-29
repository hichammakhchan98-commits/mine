# Étape 0 — (d.3) Sommaire détaillé et fiches-module

> Statut : **proposition** (questions 5 et 6). Une fiche par module, au format de l'Annexe 1.
>
> Les fiches du **palier 1** sont détaillées : c'est ce qui se livre maintenant. Celles des paliers 2 et 3
> sont volontairement plus sobres — elles seront revues à l'ouverture de leur palier, quand le calibrage
> réel sera connu. Les fixer finement aujourd'hui serait du faux travail.

## Légende
`✓` option obligatoire · `○` option décidée ici module par module · `–` sans objet (justifié)
**⏸** module ou partie suspendue par le § 5.0 (en attente des normes) · **▶** actif maintenant

---

## 1. Vue d'ensemble

### Palier 1 — Cas phare : gare voyageurs (priorité absolue)

| ID | Titre | Type | Niv. | État | Livr. |
|---|---|---|---|---|---|
| **E1** | Socle : charte, navigation, build, `civil3d`, `svgkit`, tests, démo cage d'armatures | socle | — | ▶ | 1 |
| **TV** | **Tranche verticale de suivi** : cycle de réalisation d'un plancher de mezzanine, de bout en bout | témoin | — | ▶ | 1 |
| A1 | Métier, acteurs, contrats, cycle de vie d'un projet | gestion | C | ▶ | 1 |
| A2a | Matériaux — partie qualitative (rôle, essais, durabilité, temps chaud) | fondamentaux | M | ▶ | 1 |
| A2b | Matériaux — classes, valeurs de calcul, formulation chiffrée | fondamentaux | M | ⏸ | 1 |
| A3 | Mécanique des structures | fondamentaux | M | ⏸ | 1 |
| A4 | Actions et combinaisons, descente de charges | fondamentaux | C | ⏸ | 2 |
| A5a | Topographie, implantation, reconnaissance — partie qualitative | fondamentaux | C | ▶ | 1 |
| A5b | Exploitation chiffrée d'une reconnaissance, hydrologie de base | fondamentaux | C | ⏸ | 1 |
| B1 | Géotechnique et fondations superficielles, radiers | calcul | C | ⏸ | 2 |
| B2 | Terrassements et soutènements (paroi, rabattement, talus) | calcul | C | ⏸ | 2 |
| B3 | Béton armé : poutres, poteaux, dalles, voiles, consoles, fondations | structures | M | ⏸ | 3 |
| **B5a-exec** | **Charpente : fabrication, soudage, CND, levage, montage** *(détaché — actif)* | exécution | M | ▶ | 2 |
| B5a-calc | Charpente métallique — calcul de la couverture (flambement, déversement, vent) | structures | C | ⏸ | 1 |
| B6 | Séisme et dynamique — analyse de la gare | calcul | C | ⏸ | 2 |
| B6b | Lire et contrôler un modèle aux éléments finis | calcul | C | ⏸ | 1 |
| B7a | Bâtiments : conception globale et sécurité incendie | calcul | C/N | ⏸ | 2 |
| B7b | Lots techniques : synthèse (plafonné à 10 % avec C4) | synthèse | C | ▶ | 1 |
| **B7c** | **Bâtiments ferroviaires : interfaces voie, quais, systèmes, exploitation** *(ajouté)* | synthèse | N | ▶ | 2 |
| C1 | Installation de chantier | exécution | M | ▶ | 1 |
| C2 | Terrassements, soutènements provisoires, évacuation des terres | exécution | M | ▶ | 1 |
| C3 | Gros œuvre : coffrage, ferraillage, bétonnage, cycle par niveau | exécution | M | ▶ | 2 |
| C4 | Second œuvre et lots techniques | exécution | C | ▶ | 1 |
| C6 | Matériel : engins, grues, pompes, coffrages | exécution | M | ▶ | 1 |
| C7 | Qualité, HSE, environnement | exécution | C | ▶ | 1 |
| D1 | Métrés, bordereaux, sous-détails de prix, révision, cautionnement | gestion | C | ▶ | 2 |
| D2 | Planification : WBS, cadences, CPM, Gantt, courbe en S, lissage | gestion | M | ▶ | 1 |
| D3 | Moyens humains et matériels | gestion | M | ▶ | 1 |
| D4 | Suivi et contrôle — double lecture entreprise / maîtrise d'œuvre | gestion | C | ▶ | 2 |
| D6 | BIM de suivi et outils numériques (module **court**) | synthèse | C | ▶ | 1 |
| D7 | **Pilotage et suivi de projet multi-sites** | gestion | N | ▶ | 3 |
| M3D | Maquette 3D globale de la gare avec phasage de construction | 3D | — | ▶ | 1 |
| REC | Réception, DOE, garanties | gestion | C | ▶ | 1 |
| RC1 | **Revue critique du palier 1** : dossier à corriger (5 à 8 erreurs plantées) | revue | — | ▶ | 1 |
| R5 | Cas secondaire R+5 : fondamentaux BA + séisme de base | calcul | M/C | ⏸ | 2 |

**Palier 1 : 35 modules, 50 livraisons.** Dont **▶ 23 modules / 30 livraisons livrables maintenant**, et
**⏸ 12 modules / 20 livraisons** en attente des normes.

### Palier 2 — Ouvrages d'art et structures spéciales

| ID | Titre | Type | Niv. | Livr. |
|---|---|---|---|---|
| PONT | Cas : pont à poutres précontraintes, puis voussoirs ou haubané | cas | M/C | 3 |
| B4 | Béton précontraint — **module témoin n° 2** : poutre de 30 m, post-tension | structures | M | 2 |
| B1p | Fondations profondes : pieux, micropieux, barrettes, liquéfaction, ISS | calcul | C | 2 |
| B1b | Amélioration et renforcement de sols | calcul | N | 2 |
| B5b | Charpente métallique complète : soudage, CND, fatigue, hangar | structures | M/C | 3 |
| B8 | Ponts et ouvrages d'art : typologies, appuis, joints, méthodes, inspection | structures | M/C | 3 |
| B6c | Séisme avancé : isolation, dissipation | calcul | C | 2 |
| C5 | Méthodes spéciales : mise en tension, injection, lançage, levage lourd | exécution | M | 2 |
| STADE | Cas : stade — tribunes, toiture en grande portée, effets de foule | cas | C | 2 |
| B11 | Pathologies, diagnostic d'ouvrage existant, réparation | synthèse | C | 2 |
| C8 | Démolition et déconstruction | exécution | N | 2 |
| RC2 | Revue critique du palier 2 | revue | — | 1 |

**Palier 2 : 12 modules, 26 livraisons.**

### Palier 3 — Autres ouvrages

| ID | Titre | Type | Niv. | Livr. |
|---|---|---|---|---|
| AERO | Cas : aéroport (piste, taxiways, aires, terminal) | cas | N | 2 |
| PORT | Cas : port (quai sur pieux ou caissons, digue à talus) | cas | N | 2 |
| BARR | Cas : barrage ou digue en remblai | cas | N | 2 |
| TUN | Cas : tunnel, ou route avec ouvrages hydrauliques | cas | N | 2 |
| B9 | Hydraulique et maritime | calcul | N | 2 |
| B10 | Routes, aéroports, ferroviaire, tunnels | calcul | N | 2 |
| D5 | Gestion d'une entreprise de BTP | gestion | N | 1 |
| RC3 | Revue critique du palier 3 | revue | — | 1 |

**Palier 3 : 8 modules, 14 livraisons.**

### Total

| | Modules | Livraisons |
|---|---|---|
| Palier 1 — dont livrables maintenant | 35 — *dont 23* | 50 — *dont 30* |
| Palier 2 | 12 | 26 |
| Palier 3 | 8 | 14 |
| **Total** | **55** | **90** |

Un module = une livraison, sauf découpage annoncé en parties a, b, c (§ 13.4). Les comptes de livraisons
tiennent compte de ces découpages.

---

## 2. Budget de modèles 3D (§ 9.3) — à arbitrer

La 3D n'est `✓` par défaut que pour les modules de structures, et elle **n'est jamais ajoutée pour cocher
une case** (§ 6.3). Or en phase § 5.0, les modules actifs sont presque tous non structurels. Le budget
proposé est donc volontairement **maigre** pour le palier 1 actif :

| # | Modèle | Module | Pourquoi il apprend quelque chose qu'une coupe SVG n'apprend pas |
|---|---|---|---|
| 1 | Cage d'armatures paramétrique (démonstration) | E1 | exigé par le § 5.2 ; c'est la recette de la bibliothèque |
| 2 | Installation de chantier complète + grue à tour (portée, giration, interférences) | C1 | l'interférence de deux grues et les zones de survol **ne se lisent pas** sur un plan masse plat |
| 3 | Cycle de coffrage : banche, table, étaiement, phasage 4D | C3 | le cycle de rotation est un objet dans le temps |
| 4 | Passage souterrain sous voie en exploitation, phasage 4D | B7c | les phases, les consignations et les emprises se comprennent en volume |
| 5 | Maquette globale de la gare avec phasage de construction | M3D | exigé par le § 10.2 point 10 |

**+9 modèles rattachés à la levée du § 5.0** (cage de PM1 avec curseurs, radier, paroi moulée, noyau et
voiles, escalier, console de marquise, treillis de couverture et assemblages, bâtiment en vue éclatée,
mode propre animé) et le catalogue P2/P3 du § 9.3 ensuite.

**Ce budget est révisé après la tranche verticale** (§ 5.3) : si la 3D n'apporte pas plus de compréhension
qu'une bonne coupe SVG animée, tu le dis, je réduis, et c'est consigné dans `DECISIONS.md`.

---

## 3. Fiches-module — Palier 1, modules ACTIFS (▶)

### E1 — Socle technique (Étape 1)
```text
ID : E1               Titre : Socle — charte, navigation, chaine de build, bibliotheques, tests
Palier : P1           Type : socle (aucun contenu pedagogique)
Niveau lecteur : —    Etat : ▶ actif
Livrables : charte graphique + style.css ; navigation + index.html ; build/build.mjs + build/check.mjs ;
            assets/civil3d.bundle.js (Three.js epingle, bundle IIFE, OrbitControls) ; assets/svgkit.js ;
            tests/ (Playwright) ; squelette data/ ; STATE.md ; DECISIONS.md ; depot git ; pint installe
Demonstration exigee (§ 5.2) : page d'une cage d'armatures parametrique, testee, avec sortie des tests
Controles : npm ci --ignore-scripts, npm audit, zero requete reseau, zero erreur console,
            contexte WebGL cree, capture non vide examinee, empreinte de data/ affichee
Tests : npm run check (§ 12.1 a-k)
```

### TV — Tranche verticale de suivi (Étape 2, module témoin n° 1 adapté au § 5.0)
```text
ID : TV               Titre : Cycle de realisation d'un plancher de mezzanine, de bout en bout
Palier : P1           Type : module temoin (valide la chaine, la forme et la profondeur)
Niveau lecteur : —    Etat : ▶ actif (substitut de la tranche structurelle, suspendue par le § 5.0)
Socle : S1 a S8 (tous)
Options : O1 – · O2 ✓ (n = 5 : plan de zone de coulage, cycle de rotation, Gantt, courbe en S, histogramme
          d'effectifs) · O3 – (renvoi au modele 3 de C3) · O4 ✓ · O5 ✓ · O6 – · O7 ✓
Sans objet : O1 — aucun plan de ferraillage : le ferraillage chiffre est ⏸. O3 — le phasage 3D est porte
          par C3, le dupliquer ici serait cocher une case. O6 — c'est deja une etude de cas de bout en bout.
Chaine imposee : quantites d'ordre de grandeur V3 (ratios) -> cadences et effectifs -> duree -> cout ->
          planning -> valeur acquise -> reporting. Tout passe par data -> calc -> rendu.
Donnees lues : data/projet-gare.json -> geometrie.mezzanine, geometrie.niveaux, quantites, cadences,
          prix_unitaires_MAD, effectifs, materiel
Donnees ecrites : quantites.beton_m3.mezzanine, quantites.coffrage_m2.mezzanine, quantites.acier_kg.mezzanine,
          cadences.*, planning.taches[], effectifs.*
Contre-calcul : calc/cycle_plancher.py (duree par cadences contre duree par chemin critique) ;
          calc/valeur_acquise.py (CPI/SPI par deux voies)
Etalonnage : calc/etalonnage/cpm_cas_ferme.py (reseau a solution connue a la main)
Double lecture entreprise / MOE : ✓     Fiche memo S8 : ✓ (points d'arret du plancher)
Exemples chiffres : 1 complet (une zone de coulage de la mezzanine)
Exercices : 2 application + 1 probleme + 1 revue critique « trouve l'erreur »   Quiz : 6 questions
Tests : coherence quantites = base du cout ; durees Gantt = quantites / cadences / effectifs ;
          empreinte data/ ; verification dimensionnelle (pint) ; grille SVG
A VALIDER PAR LE LECTEUR AVANT TOUTE DUPLICATION : forme, profondeur, ergonomie, chaine data -> calc -> rendu
```

### A1 — Métier, acteurs, contrats
```text
ID : A1               Titre : Metier, acteurs, cycle de vie d'un projet, contrats et marches
Palier : P1           Type : gestion     Niveau : [C]     Etat : ▶ actif
Socle : S1 a S8
Options : O1 – · O2 ✓ (n = 3 : organigramme des acteurs, cycle de vie et jalons, circuit d'un OS) ·
          O3 – · O4 ○ non retenu · O5 ✓ · O6 ✓ · O7 ○ non retenu
Sans objet : O1/O3 — module sans ouvrage ni geometrie. O4 — pas de mise en oeuvre propre.
          O7 — aucun calcul non trivial.
Contenu propre : MOA/MOE/BET/entreprise/controle/laboratoire ; les DEUX positions du lecteur (entreprise
          et maitrise d'oeuvre) ; missions de la MOE, visa, points d'arret, reception ; CPS et CCAG-T :
          mecanique contractuelle (cautionnement, retenue de garantie, revision, penalites, delais de
          paiement) SANS citer de valeur, le CPS du marche primant
Donnees lues : data/referentiels.json -> marches-contrats ; projet-gare.json -> batiment.contraintes_exploitation
Etude de cas chiffree (S4) : montage contractuel de la gare, allotissement, interfaces avec le
          gestionnaire d'infrastructure, chiffrage V3 des enjeux de delai
Fiche memo S8 : ✓ (qui signe quoi, qui vise quoi, dans quel delai)
Exercices : 1 application + 1 cas ouvert   Quiz : 5 questions
Tests : liens internes, grille SVG, registres
```

### A2a — Matériaux, partie qualitative
```text
ID : A2a              Titre : Materiaux — role, essais, durabilite, mise en oeuvre par temps chaud
Palier : P1           Type : fondamentaux     Niveau : [M] (fiche d'expert)     Etat : ▶ actif
Socle : S1 a S8 (compresses : pas de rappel des bases)
Options : O1 – · O2 ✓ (n = 3) · O3 – · O4 – · O5 – · O6 ○ non retenu · O7 ○ non retenu
Sans objet : O1/O3/O4/O5 — module de fondamentaux (§ 6.3). O7 — la partie chiffree est en A2b (⏸).
Partie ⏸ renvoyee a A2b : classes de beton, valeurs de calcul, formulation chiffree, enrobages
Contenu propre : ce que chaque materiau « cherche a faire » ; essais et ce qu'ils prouvent reellement
          (affaissement, eprouvettes, scleromètre, essai de traction d'armature) ; retrait et fluage en
          intuition ; betonnage par temps chaud et vent sec : cure, fissuration thermique, ressuage ;
          durabilite (carbonatation, chlorures) en mecanisme, sans classe ; geosynthetiques et bitumes [N]
Fiche memo S8 : ✓ (controles de reception des materiaux sur chantier)
Exercices : 2 application + 1 revue critique (PV d'essai a interpreter)   Quiz : 6 questions
```

### A5a — Topographie, implantation, reconnaissance (qualitatif)
```text
ID : A5a              Titre : Topographie et implantation, reconnaissance geotechnique — lecture et methode
Palier : P1           Type : fondamentaux     Niveau : [C]     Etat : ▶ actif
Socle : S1 a S8        Options : O1 – · O2 ✓ (n = 4) · O3 – · O4 ✓ · O5 ✓ · O6 ○ non retenu · O7 ○ non retenu
Sans objet : O1/O3 — pas d'ouvrage. O6 — couvert par le cas. O7 — exploitation chiffree en A5b (⏸).
Partie ⏸ renvoyee a A5b : exploitation chiffree d'une reconnaissance, hydrologie de base
Contenu propre : implantation d'un batiment de 120 m (chaine de tolerances, polygonale, reports,
          controles) ; implantation en zone ferroviaire (reference a la voie, gabarits, consignation) ;
          ce que chaque essai mesure vraiment (SPT, CPT, pressiometre, laboratoire) et ce qu'il ne dit
          pas ; comment LIRE un rapport de sol et ce qu'il faut exiger qu'il contienne
Donnees lues : projet-gare.json -> site.options.S*.coupe_geotechnique_V3
Double lecture entreprise / MOE : ✓     Fiche memo S8 : ✓
Exercices : 1 application + 1 revue critique (rapport de sol incomplet)   Quiz : 5 questions
```

### B7b — Lots techniques : synthèse
```text
ID : B7b              Titre : Lots techniques — synthese et interfaces avec le gros oeuvre
Palier : P1           Type : synthese     Niveau : [C]     Etat : ▶ actif
PLAFOND : B7b + C4 <= 10 % du cours (§ 2.2, defaut 1)
Socle : S1 a S8        Options : O1 ○ retenu (reservations) · O2 ✓ (n = 3) · O3 – · O4 ○ non retenu ·
          O5 ○ non retenu · O6 ✓ · O7 –
Sans objet : O3 — la synthese 3D est le sujet de D6, pas d'ici. O4/O5 — ce ne sont pas ses lots (§ 1).
Contenu propre : CVC, plomberie, electricite, courants faibles — vus UNIQUEMENT par l'interface gros
          oeuvre : reservations, charges suspendues, gaines, trémies, scellements, percements interdits,
          qui decide quoi et quand. Jamais « tes lots techniques ».
Etude de cas (S4) : carnet de reservations de la mezzanine, conflit reservation / poutre, cout d'un
          percement apres coup (V3)
Exercices : 1 application + 1 cas ouvert   Quiz : 5 questions
```

### B5a-exec — Charpente : fabrication, soudage, levage *(détaché du B5a, actif)*
```text
ID : B5a-exec         Titre : Charpente metallique — fabrication, soudage, CND, levage, montage
Palier : P1           Type : execution     Niveau : [M] fiche d'expert     Etat : ▶ actif
Parties : B5a-exec-a (atelier : fabrication, soudage, qualification, CND) ·
          B5a-exec-b (chantier : logistique, levage, montage, reglage, boulonnage)
Pourquoi ce module est actif alors que B5a-calc est ⏸ : l'execution ne depend d'AUCUNE norme de
          calcul. Le § 5.0.2 met explicitement « methodes d'execution, sequences, cadences, effectifs,
          materiel (V3) » dans ce qui est autorise et prioritaire.
Socle : S1 a S8        Options : O1 ○ retenu (plans de montage, sans cotes de calcul) · O2 ✓ (n = 5) ·
          O3 ○ non retenu (le modele du treillis appartient a B5a-calc) · O4 ✓ · O5 ✓ · O6 ○ non retenu ·
          O7 ✓ (cadences de levage et de montage — non normatif)
Sans objet : O3 — dupliquer le treillis ici serait cocher une case ; il arrive avec son calcul.
Partie ⏸ : sections, assemblages dimensionnes, vent et soulevement, feu -> B5a-calc
Contenu propre : procedes de soudage et leur choix ; qualification des modes operatoires et des
          soudeurs (PRINCIPE, aucun numero sans V0) ; CND — visuel, ressuage, magnetoscopie, ultrasons,
          radiographie : ce que chacun voit et ce qu'il ne voit pas, qui les prescrit, qui les lit ;
          tolerances de fabrication et de montage ; logistique des grandes pieces (transport, stockage,
          pre-assemblage au sol) ; levage au-dessus d'une voie en exploitation (renvoi B7c-b) ;
          reglage, boulonnage de chantier, serrage controle ; receptions en atelier et sur site
Double lecture entreprise / MOE : ✓     Fiche memo S8 : ✓ (points d'arret d'une charpente)
Exercices : 2 application + 1 probleme + 1 revue critique   Quiz : 7 questions
Securite (§ 3.4) : levage lourd — dispositions essentielles explicites
```

### B7c — Bâtiments ferroviaires : interfaces *(module ajouté — à valider)*
```text
ID : B7c              Titre : Batiments ferroviaires — interfaces voie, quais, systemes, exploitation
Palier : P1           Type : synthese / conception     Niveau : [N] traitement complet     Etat : ▶ actif
Parties : B7c-a (interfaces physiques) · B7c-b (travaux sous exploitation)
Socle : S1 a S8        Options : O1 ○ retenu · O2 ✓ (n = 6) · O3 ✓ (modele 4 : passage souterrain,
          phasage 4D) · O4 ✓ · O5 ○ non retenu · O6 ✓ · O7 ○ non retenu
Sans objet : O5 — le chiffrage des interfaces vit dans D7 et D1. O7 — aucun calcul reglementaire
          (⏸ : gabarits, distances de securite, charges de quai : aucun numero sans V0).
Contenu propre B7c-a : quais (hauteur, bordure, lacune, ecoulement), gabarits et distances de securite
          (PRINCIPES, valeurs ⏸), catenaire et mise a la terre, interfaces avec la signalisation et
          l'information voyageurs, flux voyageurs et evacuation d'un grand volume (qualitatif),
          qui est maitre d'ouvrage de quoi
Contenu propre B7c-b : travailler au-dessus et a cote d'une voie en exploitation — plages horaires,
          consignation et mise hors tension, agent de securite, emprises, levage au-dessus de la voie,
          phasage du passage souterrain, remise en exploitation
Donnees lues : projet-gare.json -> geometrie.circulations, quais_desservis, batiment.contraintes_exploitation
Donnees ecrites : contraintes de phasage reprises par D2 et D7
Double lecture entreprise / MOE : ✓     Fiche memo S8 : ✓ (points d'arret d'une intervention sous
          exploitation ferroviaire)
Exercices : 2 application + 1 probleme + 1 cas ouvert   Quiz : 7 questions
Securite (§ 3.4) : module a risque — dispositions essentielles explicites, renvoi au plan HSE et au
          referentiel du gestionnaire d'infrastructure
```

### C1 — Installation de chantier
```text
ID : C1               Titre : Installation de chantier
Palier : P1           Type : execution     Niveau : [M] fiche d'expert     Etat : ▶ actif
Socle : S1 a S8        Options : O1 ○ non retenu · O2 ✓ (n = 4 : plan masse, courbes de charge de grue,
          circulations, reseaux provisoires) · O3 ✓ (modele 2 : installation + grue a tour) · O4 ✓ ·
          O5 ✓ · O6 ○ non retenu · O7 ○ non retenu
Sans objet : O1 — pas de plan d'ouvrage. O6 — couvert par le cas phare. O7 — la verification de charge
          de grue est un abaque fournisseur, pas un calcul normatif ; traitee en O5.
Contenu propre : plan d'installation d'une emprise de 120 x 40 m contrainte par la voie ; choix et
          implantation de 2 grues a tour (portee, charge en bout, interferences, zones de survol
          interdites au-dessus de la voie) ; base-vie dimensionnee a l'effectif de pointe ; stockages
          et aires de ferraillage ; centrale a beton sur site ou BPE ; circulations et lavage de roues ;
          reseaux provisoires ; cout de l'installation (poste souvent sous-estime)
Donnees lues : projet-gare.json -> geometrie.emprise_m, multi_sites, effectifs, materiel
Donnees ecrites : materiel.grues[], effectifs.pointe, prix_unitaires_MAD.postes.installation
Double lecture entreprise / MOE : ✓     Fiche memo S8 : ✓
Exercices : 1 application + 1 probleme (implanter les grues) + 1 revue critique   Quiz : 6 questions
```

### C2 — Terrassements et soutènements provisoires
```text
ID : C2               Titre : Terrassements, fouilles, soutenements provisoires, evacuation des terres
Palier : P1           Type : execution     Niveau : [M] fiche d'expert     Etat : ▶ actif
Socle : S1 a S8        Options : O1 ○ non retenu · O2 ✓ (n = 4) · O3 ○ non retenu · O4 ✓ · O5 ✓ ·
          O6 ○ non retenu · O7 ✓ (cubatures, rotations de camions — non normatif, conserve par § 5.0.3)
Sans objet : O1/O3 — la geometrie de soutenement chiffree est en B2 (⏸).
Partie ⏸ : stabilite des talus, dimensionnement du soutenement, rabattement chiffre -> B2
Contenu propre : terrassement du niveau technique (40 x 20 x 4 m) ; cubatures et bilan deblais/remblais ;
          rotations de camions et cadence d'evacuation ; choix d'engins ; blindage et talutage
          (PRINCIPES et securite, dimensionnement ⏸) ; fouilles pres d'une voie en exploitation ;
          terres excedentaires et depot
Contre-calcul : calc/cubatures.py (methode des prismes contre methode des profils) ;
          calc/rotations.py (cadence par cycle camion contre cadence par capacite de pelle)
Etalonnage : calc/etalonnage/cubature_volume_ferme.py (volume a solution analytique)
Double lecture entreprise / MOE : ✓     Fiche memo S8 : ✓
Exercices : 2 application + 1 probleme   Quiz : 6 questions
Securite (§ 3.4) : fouilles — dispositions essentielles explicites
```

### C3 — Gros œuvre (2 parties)
```text
ID : C3               Titre : Gros oeuvre — coffrage, ferraillage, betonnage, cycle par niveau
Palier : P1           Type : execution     Niveau : [M] fiche d'expert dense     Etat : ▶ actif
Parties : C3-a (coffrage et ferraillage) · C3-b (betonnage, decoffrage, cycle)
Socle : S1 a S8        Options : O1 ○ retenu (plans de coffrage et d'etaiement — SANS cotes de
          ferraillage, ⏸) · O2 ✓ (n = 6) · O3 ✓ (modele 3 : banche, table, etaiement, phasage 4D) ·
          O4 ✓ · O5 ✓ · O6 ○ non retenu · O7 ✓ (durees de cycle, non normatif)
Sans objet : O6 — la TV en est deja une.
Partie ⏸ : sections d'acier, nomenclature chiffree, contraintes de decoffrage -> B3
Contenu propre C3-a : banches, tables, coffrage grimpant, cintres, etaiement (PRINCIPES de descente de
          charge d'etaiement, valeurs ⏸) ; faconnage et pose des armatures, calage et enrobage
          (le geste, le controle, le pourquoi) ; tolerances geometriques
Contenu propre C3-b : pompage, vibration, cure, reprises et joints, betonnage par temps chaud, ordre de
          coulage, decoffrage (criteres de maturite en PRINCIPE, valeurs ⏸), cycle de rotation par
          niveau et son calcul de duree, zones de coulage de la mezzanine
Contre-calcul : calc/cycle_rotation.py (duree de cycle par chemin critique contre somme des taches
          avec recouvrements)
Donnees lues/ecrites : cadences.*, materiel.coffrage, effectifs.equipes
Double lecture entreprise / MOE : ✓     Fiche memo S8 : ✓ (points d'arret : ferraillage avant coulage,
          enrobage, eprouvettes, geometrie)
Exercices : 3 application + 1 probleme + 1 revue critique   Quiz : 8 questions
```

### C4 — Second œuvre et lots techniques
```text
ID : C4               Titre : Second oeuvre et lots techniques — enchainement et interfaces
Palier : P1           Type : execution     Niveau : [C]     Etat : ▶ actif
PLAFOND : B7b + C4 <= 10 % du cours
Socle : S1 a S8        Options : O1 ○ non retenu · O2 ✓ (n = 3) · O3 – · O4 ✓ · O5 ✓ · O6 ○ non retenu · O7 –
Sans objet : O1/O3 — pas d'ouvrage structurel. O6/O7 — couverts ailleurs.
Contenu propre : enchainement des corps d'etat dans un hall de gare (facades, murs-rideaux,
          faux-plafonds de grande hauteur, sols de forte fréquentation) ; co-activite et nuisances
          croisees ; reception des supports ; points de blocage classiques du planning
Fiche memo S8 : ✓     Exercices : 1 application + 1 cas ouvert   Quiz : 5 questions
```

### C6 — Matériel
```text
ID : C6               Titre : Materiel — engins, grues, pompes, coffrages : choix, cadences, couts horaires
Palier : P1           Type : execution     Niveau : [M] fiche d'expert     Etat : ▶ actif
Socle : S1 a S8        Options : O1 – · O2 ✓ (n = 3 : courbes de charge, histogramme de materiel,
          arbre de decision location/achat) · O3 ○ non retenu (couvert par C1) · O4 ✓ · O5 ✓ ·
          O6 ○ non retenu · O7 ✓ (cout horaire, amortissement — non normatif)
Sans objet : O1 — pas de plan d'ouvrage. O3 — dupliquer la grue de C1 serait cocher une case.
Contenu propre : choisir un engin par la cadence exigee et non par habitude ; cout horaire complet
          (amortissement, carburant, entretien, operateur) contre prix de location ; rendements reels
          contre rendements catalogue ; immobilisation et pannes ; parc multi-sites (lien D7)
Contre-calcul : calc/cout_horaire.py (cout complet contre prix de location, point d'equilibre)
Fiche memo S8 : ✓     Exercices : 2 application + 1 probleme   Quiz : 6 questions
```

### C7 — Qualité, HSE, environnement
```text
ID : C7               Titre : Qualite, HSE, environnement — plans de controle, essais, risques
Palier : P1           Type : execution     Niveau : [C]     Etat : ▶ actif
Socle : S1 a S8        Options : O1 ○ non retenu · O2 ✓ (n = 4 : heures exposees par tache, cout
          d'une NC par ouvrage, risques classes par criticite, flux de dechets) · O3 – ·
          O4 ✓ PARTIEL · O5 ✓ · O6 ✓ · O7 ✓ (etalonnage sur cas fermes + seconde voie D1/D2)
Sans objet : O1/O3 — pas d'ouvrage.
O4 partiel, et c'est declare : le module livre les CONTROLES, les points d'arret avec leur duree,
          la securite et la double lecture entreprise / MOE. Il ne livre ni sequence, ni materiel,
          ni cadence, ni effectif : ils vivent en C1 a C3 et en C6, et les y dupliquer ferait deux
          sources pour une meme grandeur (D-039). La fiche cochait O4 en plein ; la passe
          adversariale a montre que quatre des six elements manquaient.
O7 : pas de contre-calcul normatif — il n'y a rien a dimensionner — mais le module a son
          etalonnage sur cas fermes (calc/etalonnage/qualite_cas_ferme.py, dont deux INVARIANTS)
          et sa seconde voie : D1 et D2 doivent trouver les memes heures, tache par tache.
Contenu propre : construire un plan de controle qui sert a quelque chose (qui controle, quand, sur quel
          critere, que se passe-t-il si c'est non conforme) ; points d'arret et leur negociation ;
          traitement d'une non-conformite de bout en bout ; echafaudages, fouilles, travail en hauteur,
          levage : dispositions essentielles ; dechets, bruit, poussieres, eaux de lavage ;
          HSE en milieu ferroviaire (renvoi B7c-b)
Double lecture entreprise / MOE : ✓     Fiche memo S8 : ✓
Etude de cas (S4) : une NC de parement sur voile de noyau, cout et delai du traitement (V3)
Exercices : 1 application + 1 probleme + 1 revue critique   Quiz : 7 questions
```

### D1 — Métrés, prix, révision (2 parties)
```text
ID : D1               Titre : Metres, bordereaux, sous-details de prix, deboursé sec, revision, garanties
Palier : P1           Type : gestion     Niveau : [C]     Etat : ▶ actif
Parties : D1-a (metres et sous-details de prix) · D1-b (bordereau, revision, cautionnement, penalites)
Socle : S1 a S8        Options : O1 – · O2 ✓ (n = 4) · O3 – · O4 ○ non retenu · O5 ✓ · O6 ✓ · O7 ✓
Sans objet : O1/O3 — module economique. O4 — la mise en oeuvre vit en C1 a C7.
Contenu propre D1-a : metré par ratios et metré detaille, et l'ecart entre les deux ; sous-detail de prix
          (main d'oeuvre, materiaux, materiel, deboursé sec, frais de chantier, frais generaux, alea,
          marge) ; ratios MAD/m2 d'une gare contre un batiment courant (V3, fourchettes, annee 2026)
Contenu propre D1-b : structure d'un bordereau ; prix unitaire contre prix forfaitaire ; mecanique de la
          revision des prix, du cautionnement, de la retenue de garantie et des penalites — SANS valeur :
          le CPS du marche prime et n'est pas fourni (⚠ a verifier)
Donnees lues/ecrites : quantites.*, prix_unitaires_MAD.postes.*
Contre-calcul : calc/metre.py (quantites par ratios contre quantites geometriques, ecart commente) ;
          calc/sous_detail.py (deboursé par ressource contre prix de vente)
Etalonnage : calc/etalonnage/metre_volume_ferme.py
Fiche memo S8 : ✓     Exercices : 3 application + 1 probleme + 1 cas ouvert   Quiz : 7 questions
```

### D2 — Planification
```text
ID : D2               Titre : Planification — WBS, cadences, CPM, Gantt, courbe en S, lissage
Palier : P1           Type : gestion     Niveau : [M] fiche d'expert, traitee par les specificites BTP
Etat : ▶ actif        (consigne du § 1.1 : NE PAS re-enseigner le referentiel generique de gestion de projet)
Socle : S1 a S8        Options : O1 – · O2 ✓ (n = 5 : WBS, Gantt, reseau PERT, courbe en S,
          histogramme lisse) · O3 – · O4 ○ non retenu · O5 ✓ · O6 ✓ · O7 ✓
Sans objet : O1/O3 — module de gestion. O4 — renvoi a C1-C7.
Contenu propre (ce que le referentiel generique ne donne pas) : durees issues de cadences REELLES et non
          d'estimations a dire d'expert ; chemin critique d'un chantier de batiment ferroviaire ou les
          contraintes d'exploitation (plages horaires, consignations) sont des contraintes dures ;
          lignes d'equilibre pour les taches repetitives (cycle de niveau) ; lissage des ressources
          contre nivellement ; marges et leur appropriation contractuelle ; pourquoi un planning
          contractuel et un planning de travail ne sont pas le meme objet
Donnees lues/ecrites : cadences.*, quantites.*, effectifs.*, planning.taches[], planning.dependances[]
Contre-calcul : calc/cpm.py (chemin critique par parcours avant/arriere contre enumeration des chemins)
Etalonnage : calc/etalonnage/cpm_cas_ferme.py
Fiche memo S8 : ✓     Exercices : 2 application + 1 probleme + 1 revue critique   Quiz : 7 questions
```

### D3 — Moyens humains et matériels
```text
ID : D3               Titre : Moyens humains et materiels — organigramme, effectifs, productivites
Palier : P1           Type : gestion     Niveau : [M] fiche d'expert     Etat : ▶ actif
Socle : S1 a S8        Options : O1 – · O2 ✓ (n = 3 : organigramme, histogramme d'effectifs,
          courbe de productivite) · O3 – · O4 ○ non retenu · O5 ✓ · O6 ✓ · O7 ✓
Sans objet : O1/O3 — module de gestion. O4 — renvoi a C1-C7.
Contenu propre : organigramme d'un chantier multi-sites et qui rend compte a qui ; effectifs par phase
          deduits des cadences et non l'inverse ; productivite reelle (apprentissage, rotation,
          sur-effectif qui ralentit), heures supplementaires et leur rendement decroissant ;
          sous-traitance et encadrement
Contre-calcul : calc/effectifs.py (effectif par quantite/cadence contre effectif par duree imposee)
Fiche memo S8 : ✓     Exercices : 2 application + 1 probleme   Quiz : 6 questions
```

### D4 — Suivi et contrôle (2 parties)
```text
ID : D4               Titre : Suivi et controle — avancement, attachements, valeur acquise ; et le visa MOE
Palier : P1           Type : gestion     Niveau : [C]     Etat : ▶ actif
Parties : D4-a (cote entreprise : avancement, attachements, situations, valeur acquise, reclamations) ·
          D4-b (cote maitrise d'oeuvre : visa, agrement, points d'arret, OS, NC, decomptes)
Socle : S1 a S8        Options : O1 – · O2 ✓ (n = 5) · O3 – · O4 ○ non retenu · O5 ✓ · O6 ✓ · O7 ✓
Sans objet : O1/O3 — module de gestion.
Contenu propre D4-a : mesurer un avancement physique sans se mentir (methodes 0/100, 50/50, unites
          physiques) ; attachements et situations ; valeur acquise (CPI, SPI) et ce qu'elle ne dit pas ;
          previsions a terminaison ; modifications et reclamations : la chaine de preuve
Contenu propre D4-b : visa des plans d'execution et des notes de calcul de l'entreprise — ce qu'on vise
          vraiment et ce qu'on n'endosse pas ; agrement des materiaux ; points d'arret ; ordres de
          service ; traitement d'une NC ; verification des attachements et des decomptes
Donnees lues/ecrites : planning.taches[], quantites.*, prix_unitaires_MAD.*
Contre-calcul : calc/valeur_acquise.py (CPI/SPI par deux voies : par couts et par quantites)
Etalonnage : calc/etalonnage/valeur_acquise_cas_ferme.py
Double lecture entreprise / MOE : ✓ (c'est la structure meme du module)
Fiche memo S8 : ✓ (une page par casquette)
Exercices : 3 application + 1 probleme + 1 revue critique (situation gonflee a detecter)  Quiz : 8 questions
```

### D6 — BIM de suivi (module court)
```text
ID : D6               Titre : BIM de suivi et outils numeriques
Palier : P1           Type : synthese — MODULE COURT (§ 2.2 defaut 1)     Niveau : [C]     Etat : ▶ actif
Socle : S1 a S8 (compresses)
Options : O1 ○ non retenu · O2 ✓ (n = 3 : circuit de synthese, matrice de conflits, lien maquette-planning)
          · O3 ○ non retenu · O4 ○ non retenu · O5 ○ non retenu · O6 ✓ · O7 –
Sans objet : O3 — la 3D du cours n'est pas une maquette BIM ; confondre les deux serait reproduire le
          defaut n° 1 du § 2.2. O1/O4/O5 — le lecteur LIT et coordonne une maquette, il ne la produit pas.
Contenu propre : lire une maquette IFC et savoir ce qu'elle ne garantit pas ; detection de conflits et tri
          du bruit (un conflit « reel » contre un conflit de modelisation) ; coordination de synthese :
          qui arbitre, dans quel delai, avec quelle trace ; extraction de quantites POUR LE SUIVI et ses
          pieges ; lien maquette-planning 4D ; AutoCAD / Civil 3D (tracé, profils, cubatures) ;
          logiciels de planification. Un support au suivi, jamais un sujet central.
Etude de cas (S4) : 12 conflits extraits de la maquette de la gare, a trier et a arbitrer, avec le cout
          et le delai de chacun (V3)
Fiche memo S8 : ✓     Exercices : 1 application + 1 cas ouvert   Quiz : 5 questions
```

### D7 — Pilotage et suivi multi-sites (3 parties) — module le plus épais du palier
```text
ID : D7               Titre : Pilotage et suivi de projet multi-sites
Palier : P1           Type : gestion     Niveau : [N] traitement complet     Etat : ▶ actif
Parties : D7-a (organisation et reporting) · D7-b (tableau de bord et valeur acquise consolidee) ·
          D7-c (interfaces, modifications, alerte precoce)
Socle : S1 a S8        Options : O1 – · O2 ✓ (n = 6) · O3 – · O4 ○ non retenu · O5 ✓ · O6 ✓ · O7 ✓
Sans objet : O1/O3 — module de pilotage. O4 — renvoi a C1-C7 et B7c-b.
Contenu propre D7-a : le role du Chef de Projet Suivi face a plusieurs sites et plusieurs entreprises ;
          ce qu'il decide seul et ce qu'il remonte ; rythme de reporting hebdomadaire et mensuel et
          contenu utile de chacun ; comment un reporting devient un rituel vide et comment l'eviter ;
          planning maitre contre plannings de site et leur reconciliation
Contenu propre D7-b : tableau de bord (avancement physique, couts, delais, qualite, securite) et le
          choix des indicateurs ; valeur acquise CONSOLIDEE sur deux sites et pourquoi la somme des
          CPI n'est pas le CPI de l'operation ; suivi des sous-traitants ; fiabilite de la donnee
          remontee du terrain
Contenu propre D7-c : gestion des interfaces (voie, systemes, exploitation, autre maitre d'ouvrage) ;
          gestion des modifications et des reclamations multi-sites ; alerte precoce sur les derives :
          quels signaux, a quel seuil, a qui ; reunions de coordination qui servent a quelque chose
Donnees lues : projet-gare.json -> multi_sites.sites[], planning.*, quantites.*, prix_unitaires_MAD.*
Donnees ecrites : tableau de bord consolide (data/ -> suivi/)
Etude de cas chiffree (S4) : la gare GV + la gare de RER, deux mois d'avancement, derive a detecter
Contre-calcul : calc/valeur_acquise.py en version consolidee (agregation par couts contre agregation
          ponderee par quantites) ; calc/consolidation.py
Etalonnage : calc/etalonnage/valeur_acquise_cas_ferme.py
Double lecture entreprise / MOE : ✓     Fiche memo S8 : ✓ (une page de tableau de bord)
Exercices : 3 application + 2 problemes + 1 cas ouvert + 1 revue critique   Quiz : 8 questions
```

### M3D — Maquette 3D globale avec phasage
```text
ID : M3D              Titre : Maquette 3D de la gare avec phasage de construction
Palier : P1           Type : 3D     Niveau : —     Etat : ▶ actif
Socle : S1, S2, S3, S7 (module de visualisation : S4 a S6 sans objet, S8 ✓)
Options : O1 – · O2 ✓ (n = 2 : plan de phasage, logigramme des contraintes) · O3 ✓ (modele 5) ·
          O4 ✓ · O5 ○ non retenu · O6 – · O7 –
Sans objet : S4/S5/S6 — pas d'exemple chiffre propre : la maquette LIT les donnees des autres modules.
          O5 — le chiffrage est en D1/D2. O7 — aucun calcul.
Contenu : maquette parametrique de la gare generee depuis projet-gare.json (jamais modelisee a la main) ;
          calques (gros oeuvre, charpente, facades, quais, installations) ; plan de coupe ; vue eclatee ;
          etiquettes cliquables ; phasage 4D cale sur planning.taches[] ; contraintes d'exploitation
          ferroviaire visibles par phase
Recette (§ 9.4) : rendu non vide, zero erreur console, curseurs aux bornes, etiquettes sans
          chevauchement, memoire liberee, <= 150 000 triangles, captures de chaque etat EXAMINEES
Tests : un seul renderer partage, IntersectionObserver, repli lisible si WebGL2 absent
```

### REC — Réception, DOE, garanties
```text
ID : REC              Titre : Reception, DOE, garanties
Palier : P1           Type : gestion     Niveau : [C]     Etat : ▶ actif
Socle : S1 a S8        Options : O1 – · O2 ✓ (n = 3 : cout cumule du retard, reserves par famille,
          cascade du DOE) · O3 – · O4 ✓ PARTIEL · O5 ✓ · O6 ✓ · O7 ✓ (etalonnage sur cas fermes)
Sans objet : O1/O3 — module de gestion.
O4 partiel : la sequence des operations prealables, ses responsables et ses pieges sont livres, avec
          la double lecture ; il n'y a ni materiel ni cadence a cette etape, et les effectifs de
          levee des reserves sont une decision posee, pas une organisation de chantier.
O7 : pas de contre-calcul normatif — rien a dimensionner — mais deux INVARIANTS etalonnes sur cas
          fermes (calc/etalonnage/reception_cas_ferme.py) : le jour de bascule des penalites ne
          depend pas du montant du marche, et l'arbitrage retenue/caution ne depend ni de la duree
          ni du montant. Plus la confrontation au planning de D2, mesuree en rejouant le reseau.
Contenu propre : operations prealables a la reception ; reserves et leur levee ; reception avec ou sans
          reserves et ses effets ; DOE : ce qu'il doit contenir pour etre utilisable 10 ans apres ;
          garanties (parfait achevement, bon fonctionnement, decennale) — mecanique, valeurs et delais
          ⚠ a verifier dans le CPS et le CCAG-T ; reception d'un batiment remis a un exploitant
          ferroviaire (essais de systemes, mise en service)
Double lecture entreprise / MOE : ✓     Fiche memo S8 : ✓ (check-list de reception)
Exercices : 1 application + 1 cas ouvert + 1 revue critique (DOE inexploitable)   Quiz : 6 questions
```

### RC1 — Revue critique du palier 1
```text
ID : RC1              Titre : Dossier a corriger — revue critique du palier 1
Palier : P1           Type : revue (§ 5.5)     Niveau : —     Etat : ▶ actif (en fin de palier)
Contenu : un dossier extrait du cas phare (planning, situation, metré, plan de coffrage, plan
          d'installation, carnet de reservations) contenant 5 a 8 ERREURS PLANTEES, tirees des rubriques
          S5 des modules actifs : unites, quantite comptee deux fois, cadence incoherente avec
          l'effectif, phase oubliee, contrainte d'exploitation ignoree, avancement gonfle, reservation
          en conflit, cout de l'installation sous-estime.
Le lecteur les cherche ; le corrige detaille est depliable (<details>). C'est l'entrainement direct de la
casquette « controle » (casquette 6).
Options : O2 ✓ (n = 1 : ecart relatif des sept erreurs, signe) · O6 ✓ (construire le sien sur une note
          reelle) · O1/O3/O5 – · O4 – sauf le § S4g, qui dit ce qu'une erreur de relecture fait a la
          securite d'une operation de levage sous consignation
PARTI PRIS : les sept erreurs ne sont pas inventees. Ce sont celles que ce cours a REELLEMENT commises,
          une par famille, chacune tracee a sa passe adversariale et a la decision qui en est nee.
          Le dossier est donc celui qu'aurait rendu ce cours s'il n'avait pas ete relu.
          Quatre lignes justes servent d'appats : savoir dire RAS est la moitie du metier.
Tests : chaque erreur plantee est tracee dans QA/RC1.md avec sa rubrique d'origine. calc/tests/
          test_revue.py verifie la BIJECTION ligne <-> corrige, que chaque erreur deplace reellement
          son nombre (avec une exception nommee), et que les lignes justes valent ce que publie leur
          module au centieme.
```

---

## 4. Fiches-module — Palier 1, modules SUSPENDUS (⏸)

> Ces modules **restent au sommaire avec leur fiche, et aucun n'est écrit** (§ 5.0.4). Ils se rattachent
> dès que tu écris « normes disponibles » et déposes les documents. L'ordre de rattachement proposé est
> au § 6 de ce document.

```text
ID : A2b   Titre : Materiaux — classes, valeurs de calcul, formulation chiffree
⏸ Bloque par : beton-arme (BAEL), materiaux (norme NM / EN 206)
Type : fondamentaux · Niveau [M] · Options : O2 ✓ (n = 2) · O7 ✓ · reste ○ ou –
Reprend : A2a, qui renvoie explicitement ici pour toute valeur

ID : A3    Titre : Mecanique des structures
⏸ Partiellement : l'intuition et les modeles sont ecrivables, mais l'exemple chiffre de S4 (flambement,
   hyperstaticite) s'appuie sur des sections et des materiaux a valeurs reglementaires -> suspendu en bloc
   pour ne pas livrer un module a trou
Type : fondamentaux · Niveau [M] fiche d'expert · Options : O2 ✓ (n = 4) · O3 ○ · O7 ✓
Contre-calcul : calc/rdm.py (methode des deplacements contre coefficients forfaitaires)
Etalonnage : calc/etalonnage/poutre_continue_solution_fermee.py

ID : A4    Titre : Actions et combinaisons, descente de charges          (2 parties)
⏸ Bloque par : charges-batiments (NF P 06-001, NV 65, N 84), beton-arme, seisme-batiments
Type : fondamentaux · Niveau [C] · Options : O2 ✓ (n = 5) · O7 ✓
C'EST LE MODULE PIVOT : tant qu'il est ⏸, B1, B2, B3, B5a, B6, B7a le sont aussi

ID : A5b   Titre : Exploitation chiffree d'une reconnaissance, hydrologie de base
⏸ Bloque par : geotechnique · Type : fondamentaux · Niveau [C] · Options : O2 ✓ (n = 3) · O7 ✓

ID : B1    Titre : Geotechnique — fondations superficielles et radiers   (2 parties)
⏸ Bloque par : geotechnique, beton-arme, seisme-batiments
Type : calcul · Niveau [C] · Options : O1 ○ · O2 ✓ (n = 5) · O3 ○ (radier) · O4 ✓ · O5 ✓ · O7 ✓
Donnees lues : site.options.S1.coupe_geotechnique_V3, q_adm_kPa · Ecrites : elements.fondations[]
Contre-calcul : portance par deux voies + tassement · Etalonnage : cas publie V0 a fournir

ID : B2    Titre : Terrassements et soutenements — paroi, butons, rabattement, talus   (2 parties)
⏸ Bloque par : geotechnique, beton-arme
Type : calcul · Niveau [C] · Options : O1 ○ · O2 ✓ (n = 5) · O3 ○ (paroi moulee) · O4 ✓ · O5 ✓ · O7 ✓
Reprend : C2, qui renvoie ici pour tout dimensionnement

ID : B3    Titre : Beton arme — poutres, poteaux, dalles, voiles, consoles, fondations   (3 parties)
⏸ Bloque par : beton-arme (BAEL 91 mod. 99)
Type : structures · Niveau [M] fiche d'expert · Options : O1 ✓ · O2 ✓ (n = 6) · O3 ✓ (cage PM1,
   console, voile) · O4 ✓ · O5 ✓ · O7 ✓
PORTE LA TRANCHE VERTICALE STRUCTURELLE (module temoin n° 1, § 7.3) : poutre PM1, 3 x 8,00 m + console
   4,50 m, de la descente de charges au metré d'acier
Contre-calcul : analyse de section par compatibilite des deformations contre formule simplifiee ;
   poutre continue par methode des deplacements contre coefficients forfaitaires
Etalonnage : calc/etalonnage/ — cas a solution fermee + exemple publie V0 (a fournir)

ID : B5a-calc   Titre : Charpente metallique — calcul de la couverture de la gare   (1 livraison)
⏸ Bloque par : acier (EN 1993), charges-batiments (vent, soulevement)
Type : structures · Niveau [C] · Options : O1 ✓ · O2 ✓ (n = 4) · O3 ✓ (treillis 32 m + assemblages) ·
   O5 ✓ · O7 ✓

ID : B6    Titre : Seisme et dynamique — analyse de la gare   (2 parties)
⏸ Bloque par : seisme-batiments (RPS 2000 v. 2011 + catalogue communal)
Type : calcul · Niveau [C] · Options : O2 ✓ (n = 5) · O3 ○ (mode propre anime) · O4 ✓ · O5 ✓ · O7 ✓
Specificite du site S1 : DOUBLE ZONAGE (avant / apres reclassement 2024), l'un en cas principal,
   l'autre en annexe comparative — jamais dans le meme calcul (§ 3.1)

ID : B6b   Titre : Lire et controler un modele aux elements finis
⏸ Bloque par : seisme-batiments, beton-arme (il faut un modele cale sur un referentiel)
Type : calcul · Niveau [C] · Options : O2 ✓ (n = 4) · O4 ✓ · O7 ✓
A preciser par le lecteur : le logiciel qu'il pratique (question 5)

ID : B7a   Titre : Batiments — conception globale et securite incendie   (2 parties)
⏸ Bloque par : incendie, effets-foule-gare, beton-arme, acier
Type : calcul · Niveau [C] conception / [N] desenfumage de grands volumes et evacuation ERP
Options : O1 ○ · O2 ✓ (n = 5) · O3 ○ · O4 ✓ · O5 ✓ · O7 ✓ (obligatoire, § 11)

ID : R5    Titre : Cas secondaire R+5 — fondamentaux BA et seisme de base   (2 parties)
⏸ Bloque par : beton-arme, seisme-batiments
Type : calcul · Niveau [M]/[C] · Options : O1 ○ · O2 ✓ (n = 4) · O3 ○ · O4 ○ · O5 ○ · O7 ✓
Perimetre LEGER (§ 10.1b) : pas de plans d'execution complets, pas de maquette 3D globale
```

---

## 5. Fiches-module — Paliers 2 et 3 (sobres, revues à l'ouverture du palier)

```text
P2 · PONT  Cas : pont a poutres precontraintes, puis voussoirs ou haubane   (3 livr.)
   Noyau propre (§ 10.3) : charges routieres et lignes d'influence, repartition transversale,
   precontrainte, appareils d'appui et joints. Execution : prefabrication et lancage, ou encorbellement
   equilibre, mise en tension, injection, phasage. Niveau [M] execution / [C] conception.
   O1 ✓ · O2 ✓ · O3 ✓ · O4 ✓ · O5 ✓ · O7 ✓

P2 · B4    Beton precontraint — MODULE TEMOIN N° 2 (§ 7.4) : poutre de 30 m, post-tension   (2 livr.)
   Bareme impose par le § 7.4 : section justifiee, force deduite des limites ELS, trace et fuseau,
   pertes instantanees et differees, ELS en TROIS phases, ELU flexion et tranchant, zone d'about,
   ratio d'acier de precontrainte, 3D du cable, sequence de mise en tension, securite (recul du verin).
   Niveau [M] -> compresse SAUF le bareme temoin, qui reste complet. O1-O5, O7 ✓

P2 · B1p   Fondations profondes : pieux, micropieux, barrettes, liquefaction, ISS   (2 livr.)
   O1 ○ · O2 ✓ · O3 ✓ (pieu fore avec cage et tubes de reservation — remonte en P2 par le § 2.2) ·
   O4 ✓ · O5 ✓ · O7 ✓ · Niveau [C]

P2 · B1b   Amelioration et renforcement de sols   (2 livr.)
   Colonnes ballastees, inclusions rigides, compactage dynamique, prechargement avec drains, injection
   et jet grouting, substitution ; criteres de choix, controles. Niveau [N] -> traitement complet.
   O2 ✓ · O3 ✓ (colonnes ballastees / inclusions) · O4 ✓ · O5 ✓ · O7 ✓

P2 · B5b   Charpente metallique complete : soudage, CND, fatigue, hangar   (3 livr.)
   Soudage (procedes, qualification des modes operatoires et des soudeurs), CND (visuel, ressuage,
   magnetoscopie, ultrasons, radiographie), fatigue (categories de detail, etendue de contrainte,
   courbes S-N). Niveau [M] execution / [C] calcul. O1-O5, O7 ✓

P2 · B8    Ponts et ouvrages d'art : typologies, appuis, joints, methodes, inspection   (3 livr.)
   O1 ✓ · O2 ✓ · O3 ✓ (appareils d'appui en coupe, pile et culee, voussoirs) · O4 ✓ · O5 ✓ · O7 ✓

P2 · B6c   Seisme avance : isolation, dissipation   (2 livr.)
   O2 ✓ · O3 ✓ (isolateur, mode propre anime) · O4 ✓ · O7 ✓ · Niveau [C]

P2 · C5    Methodes speciales : mise en tension, injection, lancage, levage lourd, beton projete   (2 livr.)
   Niveau [M] fiche d'expert. O2 ✓ · O3 ○ · O4 ✓ · O5 ✓ · Securite § 3.4 : module a risque eleve

P2 · STADE Cas : stade — tribunes, toiture en grande portee, effets de foule   (2 livr.)
   Gradins prefabriques, toiture en porte-a-faux, vent (soulevement, pressions locales), seisme,
   effets de foule (charges dynamiques rythmees, frequence propre minimale), lignes de visibilite,
   evacuation. Referentiel des effets de foule : ⚠ A IDENTIFIER, aucun numero sans V0.
   O1 ○ · O2 ✓ · O3 ✓ (gradin prefabrique, toiture en porte-a-faux) · O4 ✓ · O5 ✓ · O7 ✓

P2 · B11   Pathologies, diagnostic d'ouvrage existant, reparation, renforcement   (2 livr.)
   Corrosion, fissuration, RAG, defauts de parement ; essais non destructifs ; capacite residuelle ;
   verification avant demolition ou transformation. Niveau [C]. O1 ○ · O2 ✓ · O4 ○ · O6 ✓

P2 · C8    Demolition et deconstruction   (2 livr.)
   Etude prealable, choix de methode (mecanique, sciage, hydrodemolition ; l'explosif est CITE comme
   methode specialisee reservee a des entreprises agreees, SANS AUCUN DETAIL DE MISE EN OEUVRE),
   stabilite provisoire, sequence de depose, tri et valorisation, poussieres, bruit, vibrations, zones
   d'exclusion. Niveau [N] -> complet. O2 ✓ · O3 ✓ (sequence etayee, phasage 4D) · O4 ✓ · O5 ✓
   Securite § 3.4 : module a risque eleve

P2 · RC2   Revue critique du palier 2 : dossier a corriger, 5 a 8 erreurs plantees   (1 livr.)

P3 · AERO  Cas aeroport : avion critique et trafic, chaussees par methodes dediees, publication
   ACR-PCR (ne plus ecrire « PCN »), pentes, drainage, balisage ; terrassements en grande masse,
   planeite, joints des dalles rigides.   (2 livr.) Niveau [N]
P3 · PORT  Cas port : houle, maree, accostage, stabilite de caisson, pieux sous efforts lateraux et
   corrosion marine, dragage ; flottage, immersion, fenetres meteo-marines.   (2 livr.) Niveau [N]
P3 · BARR  Cas barrage ou digue : stabilite des talus, infiltrations et filtres, tassements,
   enrochements (⚠), evacuateur de crues ; compactage, planches d'essai.   (2 livr.) Niveau [N]
P3 · TUN   Cas tunnel ou route avec ouvrages hydrauliques : convergence-confinement, NATM ou tunnelier,
   ventilation et securite ; ou trace, hydrologie, dalots et buses.   (2 livr.) Niveau [N]
P3 · B9    Hydraulique et maritime   (2 livr.) Niveau [N] · O2 ✓ · O3 ○ · O4 ✓ · O5 ✓ · O7 ✓
P3 · B10   Routes, aeroports, ferroviaire, tunnels   (2 livr.) Niveau [N] · idem
P3 · D5    Gestion d'une entreprise de BTP : appel d'offres, tresorerie, achats, sous-traitance
   (1 livr.) Niveau [N] · O2 ✓ · O5 ✓ · O6 ✓
P3 · RC3   Revue critique du palier 3   (1 livr.)
```

---

## 6. Ordre de livraison proposé

### Maintenant (phase § 5.0) — palier 1 actif

**Étape 1** : `E1` socle.
**Étape 2** : `TV` tranche verticale de suivi → **tu valides forme, profondeur, ergonomie et chaîne de
données avant toute duplication**. C'est le point de contrôle le plus important du projet.

Puis, dans cet ordre — **le métier du lecteur d'abord**, ce qui inverse l'ordre alphabétique du § 11 :

| # | Module | Pourquoi à cette place |
|---|---|---|
| 1 | **D2** Planification | tout le reste s'y accroche (durées, cadences) ; [M] donc rapide |
| 2 | **D1** (a, b) Métrés et prix | la deuxième colonne du suivi ; alimente D4 et D7 |
| 3 | **D3** Moyens | ferme le triangle quantités / durées / effectifs |
| 4 | **D4** (a, b) Suivi et contrôle | le cœur du poste ; les trois précédents le rendent possible |
| 5 | **D7** (a, b, c) Multi-sites | [N] + poste actuel → le plus épais ; a besoin de D1–D4 |
| 6 | **C1** Installation de chantier | entrée dans l'exécution, avec son 3D |
| 7 | **C2** Terrassements | suit le déroulé du § 10.2 |
| 8 | **C3** (a, b) Gros œuvre | le module d'exécution central, avec son phasage 4D |
| 9 | **C6** Matériel | s'appuie sur C1–C3 |
| 10 | **C7** Qualité, HSE | s'appuie sur C1–C3 |
| 11 | **B7c** (a, b) Interfaces ferroviaires | [N] ; a besoin de C1–C3 pour parler de travaux sous exploitation |
| 11b | **B5a-exec** (a, b) Charpente : atelier et montage | [M] ; suit B7c car le levage au-dessus de la voie en dépend |
| 12 | **A1** Métier, acteurs, contrats | mieux compris après avoir vu le chantier qu'avant |
| 13 | **A2a**, **A5a** Fondamentaux qualitatifs | [M]/[C], compressés |
| 14 | **C4** Second œuvre · **B7b** Lots techniques | plafonnés à 10 % à eux deux |
| 15 | **D6** BIM de suivi | court ; a besoin de D2 et D4 pour le lien 4D |
| 16 | **M3D** Maquette globale + phasage | a besoin du planning de D2 |
| 17 | **REC** Réception et DOE | fin du déroulé du § 10.2 |
| 18 | **RC1** Revue critique du palier 1 | clôture → **go/no-go** |

### À la levée du § 5.0 — ordre de rattachement

`A4` (module pivot) → **tranche verticale structurelle** (module témoin n° 1 dans `B3`, § 7.3, que
**tu valides** comme la TV) → `A2b`, `A3`, `A5b` → `B1`, `B2` → `B3` (suite) → `B5a-calc` → `B6`, `B6b` →
`B7a` → `R5`. Puis relecture des modules déjà livrés qui portaient un renvoi « ⏸ » ou une valeur V3
qu'un document V0 peut remplacer (§ 5.0.7d), corrections listées dans `STATE.md`.

### B3e — Béton armé en exécution (module créé par D-033, écrit le 26/10/2026)
```text
ID : B3e              Titre : Beton arme EN EXECUTION — lire un plan, le metrer, le controler
Palier : P1           Type : calcul non normatif + execution     Niveau : [C]     Etat : LIVRE
Socle : S1 a S8 (tous)
Options : O1 ✓ (coupe et elevation ferraillees, nomenclature) · O2 ✓ (n = 5) · O3 — sans objet
          (la cage 3D parametrique existe deja a la page de demonstration du socle ; la dupliquer
          ici ne ferait que cocher une case, § 6.2) · O4 ✓ (double lecture) · O5 ○ partiel (metre
          et commande ; le prix reste chez D1) · O6 ○ non retenu · O7 ✓ (deux voies + etalonnage)
Sans objet : O3, justifie ci-dessus. O6 — les 3 exercices couvrent le cas ouvert.
Partie ⏸ : TOUT le dimensionnement — sections, longueurs d'ancrage et de recouvrement, arrets de
          barres, enrobages minimaux, espacements maximaux, longueurs de crochets. Module B3c a la
          levee du § 5.0.
Contenu propre : les 7 etapes de lecture d'un plan ; metre par nomenclature (poutre) et par nappes
          (dalle) ; masse lineique comme grandeur PHYSIQUE ; longueur developpee contre cote du
          dessin ; recouvrements de livraison (nombre geometrique, longueur ⏸) ; comptage des
          cadres ; les deux voies element par element ; le metre contre l'estimation par ratio, et
          quand l'un remplace l'autre ; du plan a la commande a ce qui se paie ; 7 controles avec
          leur REFERENCE et le statut de leur regle
Donnees lues : data/projet-gare.json -> armatures.plan (PLAN FICTIF, calibre sur ratios_V3, non
          dimensionne), armatures.conventions, armatures.du_plan_a_la_commande, ratios_V3.acier
Donnees ecrites : calc/sorties/ferraillage.json
Contre-calcul : voie A nomenclature x masse lineique contre voie B ratio kg/m3, element par element
Etalonnage : calc/etalonnage/ferraillage_cas_ferme.py (10 diametres contre le tableau du commerce,
          perimetre de cadre analytique, comptage, analyse dimensionnelle)
Double lecture entreprise / MOE : ✓     Fiche memo S8 : ✓ (7 points du visa de ferraillage)
Schemas : coupe ferraillee · elevation ferraillee (nouveau generateur) · masse par diametre ·
          les deux voies avec fourchette · cascade plan -> commande
Exercices : 1 application + 1 probleme + 1 cas ouvert   Quiz : 7 questions
Tests : calc/tests/test_ferraillage.py (60 controles, 6 canaris) + verif_unites + rendu
```

### B7c — Bâtiments ferroviaires (écrit le 27/10/2026)
```text
ID : B7c              Titre : Batiments ferroviaires — construire a cote d'une voie exploitee
Palier : P1           Type : conception + execution, non normatif     Niveau : [N]     Etat : LIVRE
Socle : S1 a S8 (tous)
Options : O1 — sans objet (aucun plan : le module porte des DUREES et des interfaces) · O2 ✓ (n = 3)
          · O3 — sans objet · O4 ✓ (double lecture implicite : l'exploitant tient deux postes de la
          part fixe) · O5 ✓ (cout de l'heure utile) · O6 ○ non retenu · O7 ✓ (rendement etalonne sur
          solution fermee ; les leviers MESURES en rejouant le reseau)
Partie ⏸ : gabarit, distances de securite aux catenaires, hauteur et lacune quai-materiel, charges
          ferroviaires, resistance au feu des locaux techniques. PRINCIPE et consequence chantier
          seulement, jamais la valeur.
Contenu propre : decomposition d'une plage de consignation et part fixe irreductible ; les deux
          effets qui se multiplient (rendement du temps x abattement de nuit) ; point de non-retour
          et ses DEUX seuils de conception (masse maximale levable, plage minimale) ; les leviers,
          chacun mesure en rejouant le reseau de D2 ; cout de l'heure UTILE avec son domaine ;
          matrice d'interfaces et la distinction decision / information ; plusieurs maitres
          d'ouvrage
Donnees lues : data/projet-gare.json -> ferroviaire.*, planning.contraintes_exploitation ;
          calc/sorties/planification.json (tonnage, durees), prix.json (taux horaire)
Donnees ecrites : calc/sorties/ferroviaire.json ; et calc/plage.py est LU PAR D2 (D-039)
Contre-calcul : le rendement est une soustraction, etalonnee sur cas fermes ; les leviers sont
          mesures en rejouant le reseau (D-040), jamais deduits. Les deux voies du nombre de plages
          partageraient le rendement : le module ne les presente donc PAS comme independantes (D-043)
Etalonnage : calc/etalonnage/plage_cas_ferme.py (soustraction, composition des deux effets, cas
          limites qui levent, monotonie, jeu reel recalcule)
Double lecture entreprise / MOE : ✓     Fiche memo S8 : ✓ (4 reflexes, 2 seuils)
Schemas : decomposition d'une plage · duree de chantier par levier · etalement du levage par levier
Exercices : 1 application + 1 probleme + 1 cas ouvert   Quiz : 7 questions
Tests : calc/tests/test_ferroviaire.py (40 controles, 3 canaris) + etalonnage + verif_unites + rendu
EFFET SUR LE COURS : ce module a corrige le planning de D2 (tache sous consignation chiffree comme
          un travail de jour). Chantier 363 -> 600 j ouvres, fin 2028-05-01 -> 2029-04-23.
```

### C7 — Qualité, HSE, environnement (écrit le 27/10/2026)
```text
ID : C7               Titre : Qualite, HSE, environnement — ce qui rend la securite pilotable
Palier : P1           Type : execution     Niveau : [C]     Etat : LIVRE
Socle : S1 a S8 (tous)
Options : O1 — sans objet · O2 ✓ (n = 3) · O3 — sans objet · O4 ✓ · O5 ✓ (cout de non-qualite) ·
          O6 ○ non retenu · O7 ✓ — RELEVE par rapport a la fiche d'origine, qui le disait « non
          retenu, aucun calcul normatif ». Il y a bien un noyau calculable, et il est entierement
          non normatif : l'exposition en heures, le cout complet d'une NC, l'effet planning mesure
          en rejouant le reseau, et la criticite comme ordre et non comme grandeur.
Partie ⏸ : frequences de prelevement, criteres de resistance et de conformite, tolerances,
          distances de securite, seuils d'exposition, obligations de tri. METHODE et place dans le
          plan seulement, jamais la valeur.
Contenu propre : l'exposition se compte en HEURES (TF, TG) et la nuit pese plus que ses heures ;
          les cinq colonnes d'un plan de controle, plus le DELAI DU RESULTAT qui change la nature
          du controle ; le cout complet d'une non-conformite, dont 85 % sans facture ; la meme NC
          selon la marge de l'ouvrage — absorbee, transmise, ou AMPLIFIEE sous consignation ; la
          criticite comme produit de rangs, ses ex aequo et son seuil arbitraire ; les dechets et
          le flux qui pese le moins en commandant le plus
Donnees lues : data/projet-gare.json -> qualite_hse.* ; calc/sorties/planification.json (heures
          par tache, reseau), prix.json (frais de duree, taux horaire)
Donnees ecrites : calc/sorties/qualite.json
Contre-calcul : l'effet planning est MESURE en rejouant le reseau sur trois taches choisies par
          leur MARGE (D-040), jamais deduit ; les trois regimes sortent du calcul, pas du texte
Double lecture entreprise / MOE : ✓     Fiche memo S8 : ✓ (4 reflexes, 5+1 colonnes)
Schemas : heures par tache · cascade du cout d'une NC · criticite classee
Exercices : 1 application + 1 probleme + 1 revue critique   Quiz : 7 questions
Tests : calc/tests/test_qualite.py (56 controles, 4 canaris) + verif_unites + rendu
EFFET SUR LE COURS : premier module a consommer les heures par tache que la correction de B7c a
          rendues fiables. Sans le controle croise D1/D2, son indicateur central etait faux.
```

### C1 — Installation de chantier (écrit le 28/10/2026)
```text
ID : C1               Titre : Installation de chantier — couvrir n'est pas lever
Palier : P1           Type : execution     Niveau : [M] fiche d'expert     Etat : LIVRE
Socle : S1 a S8 (tous)
Options : O1 — sans objet · O2 ✓ (n = 5 : courbe de charge, plan masse, couvrir/servir, survol du
          gabarit, cascade du cout) · O3 ○ NON RETENU — ECART ASSUME par rapport a la fiche
          d'origine, qui portait « O3 ✓ (modele 2 : installation + grue a tour) ». Ce que la 3D
          apporterait ici est la giration et l'interference de deux fleches ; ce que le module
          enseigne est la COURBE DE CHARGE et la part servie, qui se lisent mieux sur un
          diagramme et un plan masse cotes. Ajouter la maquette serait cocher une case (§ 6.2).
          Le modele reste au catalogue P1 (§ 9.3) et se decidera avec la maquette globale.
          · O4 ✓ · O5 ✓ · O6 ○ non retenu · O7 ✓ — RELEVE : la fiche d'origine le disait « non
          retenu, abaque fournisseur ». L'abaque est bien une donnee, mais tout ce qu'on en tire
          est calculable et non normatif : part servie par echantillonnage, debit, aire couverte
          hors batiment, survol du gabarit.
Partie ⏸ : distances de securite, regles de survol d'une voie exploitee et d'un tiers, obligations
          de cloture et de signalisation, surfaces reglementaires des locaux sociaux, conditions
          d'implantation vis-a-vis des reseaux, verifications de mise en service des appareils de
          levage. GEOMETRIE, debits et couts seulement ; la reglementation donne les contraintes.
Contenu propre : COUVRIR N'EST PAS LEVER — la part servie d'une piece vaut toujours moins que la
          couverture, et l'ecart croit avec la masse (98,2 % contre 36,8 % pour la piece de 8 t) ;
          la courbe de charge et ses deux regimes, lue dans les deux sens (charge a une portee,
          rayon limite d'une masse) ; trois voies independantes vers le nombre de grues, dont une
          QUI NE TRANCHE PAS parce que ses bornes enjambent le seuil ; le troisieme axe, propre au
          ferroviaire : le cercle de la fleche en girouette atteint le gabarit dans les TROIS
          variantes, et cet axe va en SENS INVERSE de la couverture ; la base-vie sur la pointe du
          planning execute, ni sur la moyenne ni sur la pointe d'avant lissage ; les aires et le
          majorant sous grue hors batiment ; le cout coupe en fixe (17,9 %) et loyer.
Donnees lues : data/projet-gare.json -> installation.* (grue, variantes_de_calage, pieces_a_lever,
          levages, base_vie, aires, voisinage), geometrie.emprise_m, ferroviaire.sous_interception
          (masse d'une piece — LUE, jamais redeclaree, D-039) ; calc/sorties/planification.json
          (effectifs apres lissage, conflit de grue), prix.json (frais de duree), gros-oeuvre.json
          (parc de coffrage et cadence retenus)
Donnees ecrites : calc/sorties/installation.json
Contre-calcul : etalonnage sur cas fermes (calc/etalonnage/installation_cas_ferme.py) — disque
          clippe par un carre, aire couverte hors batiment contre pi.R2 moins le disque clippe,
          et DEUX INVARIANTS : deux grues au meme endroit couvrent ce que couvre une seule ; deux
          grues disjointes couvrent le double MOINS le batiment compte une fois de trop. Ce second
          invariant, d'abord ecrit « le double », a echoue de 100 m2 : l'erreur etait dans
          l'invariant, pas dans la fonction, et le cas conserve distingue les deux.
ECARTS DE CONTENU avec la fiche d'origine, nommes (D-061) : la fiche promettait aussi la
          centrale a beton sur site OU le BPE, les circulations et le lavage de roues, et les
          reseaux provisoires. Aucun des trois n'est traite ici. Raison : les deux premiers se
          chiffrent avec le betonnage (C3, qui publie deja la fenetre de coulage et les rotations)
          et avec le materiel (C6) ; les reseaux provisoires n'ont dans ce cours aucune donnee a
          lire et auraient produit un paragraphe de generalites, ce que le § 2.2 interdit. Ils
          sont renvoyes a C3 et C6, et le module le dit dans son S1 au lieu de le taire.
Double lecture entreprise / MOE : ✓ (l'exercice 4 est un plan d'installation a viser, 5 observations
          dont 2 bloquantes et 3 d'OMISSION DE PIECE)   Fiche memo S8 : ✓ (3 phrases, 9 controles)
Schemas : courbe de charge avec marqueur · plan masse et point defavorable · couvrir contre servir
          (6 barres) · survol du gabarit par variante · cascade du cout
Exercices : 1 application + 2 problemes (dont « le releve qui vaut plus que le calcul ») + 1 revue
          critique   Quiz : 7 questions
Tests : calc/tests/test_installation.py (128 controles, 3 canaris) + etalonnage (disque clippe,
          lentille de deux disques, quatre invariants) + verif_unites (section C1, dont 3 LIMITES
          DECLAREES dimensionnellement invisibles) + rendu
EFFET SUR LE COURS : publie un ecart avec D1 — qui facture UNE grue au mois sur toute la duree du
          chantier quand C1 en retient DEUX sur la seule fenetre du gros oeuvre, 5,8 mois sur 29,7.
          Les deux ecarts vont en sens inverse et celui de la DUREE l'emporte : D1 surestime de
          1 723 300 MAD. Verse en dette (D-055), pas corrige en silence. La passe adversariale a
          trouve cette erreur dans ce module meme : il louait deux grues pendant 29,7 mois. Deplace aussi la verification dimensionnelle en DERNIERE etape de
          calc/run_all.py : placee avant les calculs, elle controlait les sorties de l'execution
          precedente, et laissait un module entier non verifie.
```

### D7 — Pilotage et suivi multi-sites (écrit le 29/10/2026)
```text
ID : D7               Titre : Pilotage et suivi multi-sites — ce qu'une agregation vous cache
Palier : P1           Type : gestion     Niveau : [N]     Etat : LIVRE
Socle : S1 a S8 (tous)
Parties : livre en UN module a trois sections (a organisation et reporting · b tableau de bord
          consolide · c interfaces et alerte precoce) plutot qu'en trois livraisons. Ecart assume
          avec la fiche d'origine (D-061) : les trois parties partagent les memes donnees et la
          meme these, et les separer aurait oblige a redire deux fois la loi d'amortissement.
Options : O1 – · O2 ✓ (n = 6 : CPI par site, latence, lots du site secondaire, derive par site,
          escalier du retard quantise, interfaces par marge) · O3 – · O4 ○ non retenu · O5 ✓ ·
          O6 ✓ (la revue du 4e mois, de bout en bout, en S4) · O7 ✓
Partie ⏸ : obligations contractuelles de reporting (contenu, destinataires, delais), seuils de
          declaration imposes par le marche, conditions d'ouverture d'une reclamation, formes et
          delais des ordres de service, regles d'acces du gestionnaire d'infrastructure.
Contenu propre : UN RATIO NE SE CONSOLIDE PAS — CPI consolide 0,877 contre une moyenne des CPI a
          0,822, et l'ecart va toujours dans le sens du plus gros site ; la LOI D'AMORTISSEMENT —
          un indicateur consolide divise la derive d'un site par son poids, x7,8 ici, et
          254 058 MAD de derive pour un centieme de CPI ; le SEUIL DE MASQUAGE — le site
          secondaire peut perdre 689 000 MAD de plus sans faire franchir le seuil d'alerte ; le
          MASQUAGE RECURSIF — un lot a 0,686 dans un site a 0,748, et les amortissements se
          multiplient d'un etage a l'autre ; la LATENCE — demi-periode + delai de remontee, dont
          la remontee fait 62 % en hebdomadaire ; et le resultat le plus utile au lecteur : sur un
          chantier ferroviaire LE SEUIL D'ALERTE EST UNE DUREE, la periode entre deux fenetres de
          consignation, parce qu'un cycle perdu ne depense rien et n'apparait dans aucun CPI.
Donnees lues : calc/sorties/suivi.json (D4 : BAC, VP, VA, CR, CPI, SPI du site principal — jamais
          recopies), planification.json (segments, consignations, calendrier), prix.json (duree en
          mois), reception.json (cout d'un jour hors penalites), ferroviaire.json (registre des
          interfaces et delais de demande) ; data/ -> multi_sites.* (site secondaire declare lot
          par lot, seuils du tableau de bord, rythmes de reporting)
Donnees ecrites : calc/sorties/pilotage.json
Contre-calcul : etalonnage sur cas fermes (calc/etalonnage/pilotage_cas_ferme.py) — le cas
          degenere ou la moyenne des CPI EST juste (couts reels egaux), la loi d'amortissement
          verifiee exactement, la forme fermee du seuil de masquage, et cinq points de rupture de
          l'escalier du retard quantise.
Double lecture entreprise / MOE : ✓ (la revue critique de l'exercice 5 est un tableau de bord a
          refuser)     Fiche memo S8 : ✓ (une page de tableau de bord + 6 reflexes)
Exercices : 2 application + 2 problemes + 1 revue critique   Quiz : 8 questions
Tests : calc/tests/test_pilotage.py (90 controles, 4 canaris) + etalonnage + verif_unites + rendu
EFFET SUR LE COURS : le format « ::n3 » n'existait pas et rendait la valeur BRUTE — 45 occurrences
          dans six modules deja livres, dont des CPI a quatre decimales a cote des memes a trois.
          Le build echoue desormais sur un format inconnu, et n3/n4 sont implementes.
```

### B7b + C4 — Lots techniques et second œuvre (écrit le 29/10/2026)
```text
ID : B7b + C4         Titre : Lots techniques et second oeuvre — vus par l'interface
Palier : P1           Type : synthese + execution     Niveau : [C]     Etat : LIVRE
PLAFOND TENU : un seul module pour les deux fiches, parce qu'elles partagent le meme sujet —
          l'INTERFACE. Les separer aurait double les generalites sans doubler le contenu, et
          le § 2.2 plafonne l'ensemble a 10 % du cours. Ecart assume avec les deux fiches
          d'origine (D-061), qui prevoyaient deux livraisons.
Socle : S1 a S8 (tous)
Options : O1 ○ retenu (le carnet de reservations EST le plan annote) · O2 ✓ (n = 5) · O3 – ·
          O4 ✓ (la chaine de reception des supports) · O5 ✓ (le prix d'un trou oublie) ·
          O6 ✓ (l'etude de cas du lundi matin) · O7 ✓ — RELEVE : les deux fiches le disaient
          sans objet. Il y a bien deux calculs non normatifs, et l'un a une forme fermee.
Partie ⏸ : regles de percement d'un element porteur, sections et positions admissibles,
          distances aux armatures et aux appuis, retablissement du degre coupe-feu d'une
          traversee, classements au feu, tolerances contractuelles de planeite et d'humidite.
Contenu propre : LA GEOMETRIE AVANT LE DEBAT — passage libre = espacement moins diametre, lu
          sur le ferraillage de B3e : 92 mm sur appui, 192 en travee, et les diametres 200,
          250 et 315 mm ne passent NULLE PART ; LA DATE DE GEL — un carnet n'est pas un
          document mais huit echeances, et elles tombent aux jours 37 a 61 quand le second
          oeuvre commence au jour 500, soit 439 jours plus tard ; LE PRIX D'UN TROU OUBLIE —
          x31, dont 47 % ne tiennent ni a la machine ni a l'ouvrier ; LA FILE DE CORPS
          D'ETAT — forme fermee T(Z) = (SW + (Z-1).maxW)/Z + N(Z-1)f, qui decroit, bute sur
          le corps le plus lent et remonte quand les frontieres l'emportent ; LA RECEPTION
          DES SUPPORTS — la seule decision irreversible d'une journee de second oeuvre.
Donnees lues : calc/sorties/ferraillage.json (cadres et nappes de B3e — aucun espacement
          redeclare), planification.json (segments MEZZ et SECO, duree declaree du second
          oeuvre), gros-oeuvre.json (zones et cadence de C3), suivi.json (date d'arret) ;
          data/ -> lots_techniques.* (diametres, densite, delai de gel, postes d'un percement,
          six corps d'etat, cout de frontiere)
Donnees ecrites : calc/sorties/synthese.json
Contre-calcul : SECONDE VOIE sur la duree du second oeuvre — la forme fermee donne 78 j contre
          75 j declares par D2, deux chemins sans donnee commune, 4 % d'ecart. Etalonnage sur
          cas fermes (calc/etalonnage/synthese_cas_ferme.py) : serie pure en Z=1, plancher
          quand Z tend vers l'infini, forme (N+Z-1).W/Z a durees egales, decroissance stricte
          sans frontiere, optimum interieur avec, et le passage libre endroit par endroit.
Double lecture entreprise / MOE : ✓ (l'exercice 3 est un carnet de reservations a viser, deux
          observations bloquantes)     Fiche memo S8 : ✓ (5 reflexes, 2 formules)
Exercices : 1 application + 1 probleme + 1 revue critique   Quiz : 7 questions
Tests : calc/tests/test_synthese.py (56 controles, 3 canaris) + etalonnage + verif_unites + rendu
EFFET SUR LE COURS : premiere SECONDE VOIE sur une duree declaree a l'Etape 0. Les 75 jours de
          second oeuvre de D2 etaient un jugement d'experience ; la decomposition en six corps
          avec sa forme fermee en donne 78. L'accord credite la decomposition, donc on peut
          desormais piloter le second oeuvre par ses termes — et le goulot a un nom.
```
