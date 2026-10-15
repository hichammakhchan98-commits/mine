# Étape 0 — (d.4 à d.6) Volume, critère d'arrêt, ordre de coupe

## 1. Estimation de volume

| Palier | Modules | Livraisons | Dont livrables **maintenant** (§ 5.0) |
|---|---|---|---|
| Palier 1 — cas phare gare (y compris Étape 1 socle et Étape 2 tranche verticale) | 34 | 49 | **28** |
| Palier 2 — ouvrages d'art et structures spéciales | 12 | 26 | 0 |
| Palier 3 — autres ouvrages | 8 | 14 | 0 |
| **Total** | **54** | **89** | **28** |

Détail du palier 1 : **22 modules actifs (28 livraisons)** immédiatement, **12 modules suspendus
(21 livraisons)** qui se rattachent à la levée du § 5.0 — soit **43 % des livraisons du palier 1
aujourd'hui inaccessibles**, faute de normes.

**Ordre de grandeur d'effort.** Je n'ai pas de mesure fiable avant le premier module : le § 13.2 impose
de reporter l'effort consommé à chaque fin de module, et c'est à ce moment que l'estimation deviendra
sérieuse. Avant cela, une seule chose est honnête à dire : une livraison du palier 1 actif est, selon le
niveau de calibrage, **une à trois séances de travail** en mode B (chargement du zip, module, tests,
passe /devil, zip de sortie). Le palier 1 actif (28 livraisons) représente donc un ordre de **30 à 60 séances**. Je
recalibrerai ce chiffre après la tranche verticale, qui est précisément là pour ça — et je te dirai si
l'écart est grand.

**Ce que je te demande de fixer (question 1)** : le nombre de séances par semaine, le budget total que tu
acceptes, et **la date de fin du palier 1 (v1 du cours)**, que le § 5.5 exige d'arrêter dès l'Étape 0.
Elle est aujourd'hui `null` dans `data/projet-gare.json` → `planning.date_fin_P1_demandee_au_lecteur`.

**Une réserve sur cette date.** Le palier 1 contient 12 modules suspendus qui dépendent d'un événement
que je ne contrôle pas : la mise à disposition de tes documents. Fixer une date de fin de palier 1 qui
les inclut, c'est fixer une date pour quelque chose dont la date de départ est inconnue. Je propose donc
**deux dates** : une pour le **palier 1 actif** (ferme, tenable), une pour le **palier 1 complet**
(indicative, recalée au jour où tu écris « normes disponibles »). Si tu préfères une date unique, dis-le
et je la consigne telle quelle — mais elle portera cette incertitude, et je le rappellerai à chaque bilan.

## 2. Critère d'arrêt (§ 5.5)

À la fin de chaque palier : bilan (modules livrés, tests, valeurs V2 à vérifier, dette) puis
**go/no-go de ta part**. Le palier suivant ne démarre pas sans validation.

Arrêt ou replanification si :
1. **deux modules consécutifs** échouent aux tests (§ 12.1) ou à la passe adversariale (§ 12.2) ;
2. tu constates une **dérive de qualité** ;
3. le **budget** de temps ou de coût fixé à l'Étape 0 est dépassé ;
4. **tu dis stop.**

S'y ajoutent deux déclencheurs propres à la situation présente, que je te propose d'inscrire :
5. **la phase § 5.0 dure si longtemps que le palier 1 actif est épuisé** : il reste alors 14 modules
   suspendus et plus rien à écrire. Ce n'est pas un échec, c'est un point d'arrêt mécanique — il faut
   soit les documents, soit décider d'ouvrir le palier 2 sur ses parties non normatives (exécution,
   méthodes), soit s'arrêter ;
6. **la tranche verticale (Étape 2) n'est pas validée** : je ne duplique pas une forme que tu n'as pas
   approuvée. Deux allers-retours sans convergence sur la TV → on re-cadre au lieu d'avancer.

## 3. Ordre de coupe (ce qui s'abandonne en premier si le budget est dépassé)

Proposition par défaut du § 5.1d, que je reprends en l'adaptant à ton poste :

| Rang | Ce qui tombe | Pourquoi en premier |
|---|---|---|
| 1 | **Modèles 3D non structurels** | la 3D est le poste le plus coûteux au gain pédagogique ; une coupe SVG animée fait souvent aussi bien (c'est d'ailleurs la question que la TV doit trancher) |
| 2 | **O6 — mini-projets et études de cas** des modules [M] | le lecteur sait déjà faire ; l'étude de cas S4 reste, elle est obligatoire |
| 3 | **Palier 3 entier** (aéroport, port, barrage, tunnel, B9, B10, D5) | tous [N], mais aucun n'est son métier actuel ; c'est de la culture d'ingénieur, pas de l'outillage de poste |
| 4 | **O5 — chiffrage et planning** des modules [M] | le chiffrage reste partout où il enseigne quelque chose ; sur un module [M], il répète |
| 5 | **Cas secondaire R+5** | redondant avec la gare pour les fondamentaux du béton armé |

**Ce qui ne se coupe jamais**, quel que soit le budget : la tranche verticale ; D1 à D4 et D7 (le poste du
lecteur) ; les fiches mémo S8 ; le contre-calcul O7 des modules de calcul ; les revues critiques de
palier ; la passe /devil. Couper là-dedans, c'est couper ce pour quoi le cours existe.

**Une divergence que je signale.** Le § 5.1d propose de couper « O6, puis P3, puis O5 des modules [M] »
après la 3D. J'ai inversé O6 et P3 par rapport à une lecture littérale, et j'ai ajouté le R+5 en rang 5 :
le R+5 coûte deux livraisons pour redire ce que la gare enseigne déjà, alors que P3 apporte au moins des
domaines neufs. Si tu préfères l'ordre littéral du prompt, dis-le : c'est ta décision, et elle part dans
`DECISIONS.md`.
