---
id: E1-demo
titre: Cage d'armatures paramétrique
fil: Étape 1 — socle · page de démonstration
resume: Démonstration de la chaîne data → calc → rendu et de la bibliothèque civil3d. Ce n'est pas un module de cours.
meta: Mode B · phase § 5.0 (sans calculs normatifs) · figures générées par svgkit · métré recalculé par calc/
pied: Page de démonstration du socle. Aucun dimensionnement, aucune vérification réglementaire.
donnees: demo-cage, metre-cage
---

:::encart {"genre":"attente","titre":"Ce que cette page est, et ce qu'elle n'est pas"}
C'est la **page de démonstration exigée par l'Étape 1** : elle prouve que la chaîne de génération
fonctionne de bout en bout et que la bibliothèque 3D tient sa recette. Elle **n'enseigne pas le
ferraillage**. La géométrie que tu vois est dessinée à partir de paramètres choisis pour exercer la
bibliothèque — pas issus d'un calcul. La phase § 5.0 interdit tout dimensionnement tant que les normes
ne sont pas fournies, et cette page respecte cette interdiction.
:::

## Ce que la démonstration doit prouver

Le § 5.2 demande une page testée, avec la sortie des tests. Voici les cinq affirmations qu'elle met à
l'épreuve, chacune vérifiable dans le rapport de contrôle :

1. **Source de vérité unique (R1).** La section dessinée en SVG, la cage en 3D et le métré en kilos
   lisent le **même** fichier de données. Change `data/demo-cage.json`, et les trois changent ensemble.
2. **Génération, pas dessin à la main (R2).** Aucune coordonnée n'est tapée : les figures sortent de
   fonctions paramétriques de `svgkit.js`, la cage sort de `civil3d`.
3. **Contre-calcul (§ 3.3).** La masse d'acier est calculée **deux fois par deux voies indépendantes**,
   et l'écart est affiché.
4. **Étalonnage (§ 3.3).** La routine géométrique est calée sur une solution analytique fermée.
5. **Hors ligne (§ 4.4).** Aucune requête réseau : la page fonctionne en `file://`, formules comprises.

## La section, dessinée depuis les données

:::figure {"fn":"coupeSection","args":"demo-cage.section","titre":"Coupe de la section, générée depuis data/demo-cage.json","motifs":["beton"],"num":1,"legende":[{"n":1,"t":"béton"},{"n":2,"t":"barres longitudinales"},{"n":3,"t":"cadre"}],"legendeXY":[196,250],"voir":["Les barres ne sont pas posées à l'œil : leur abscisse est calculée à partir de la largeur, de l'enrobage et du diamètre, puis répartie sur la place utile.","Le cadre est tracé à l'intérieur de l'enrobage, et les barres à l'intérieur du cadre : c'est l'ordre réel d'un plan de ferraillage.","Les cotes affichées sont les variables du fichier de données, pas du texte."],"erreur":"Dessiner les barres à l'intérieur de l'enrobage en oubliant l'épaisseur du cadre : sur un plan, l'erreur se voit à peine ; au coffrage, l'enrobage réel est insuffisant."}
:::

La section est celle du prédimensionnement **V3** de la poutre `PM1` du cas phare : la démonstration
parle du même ouvrage que le cours, pour que rien ne soit gratuit.

## La cage, en trois dimensions

:::model3d {"id":"cage","titre":"Cage d'armatures paramétrique","init":"demoCage","sous":"Curseurs bornés, plan de coupe, vue éclatée et phasage. Clique une étiquette pour la déplier. Le bouton réinitialise le cadrage."}
:::

Ce que la 3D apporte ici et qu'une coupe ne donne pas : **la répartition des cadres sur la longueur**
et l'ordre dans lequel les choses arrivent sur le chantier. Fais glisser le curseur de phase :
coffrage, ferraillage, bétonnage, décoffrage — le coffrage apparaît à la première phase et disparaît à
la dernière. Cette question — *la 3D apporte-t-elle plus qu'une bonne coupe ?* — est exactement celle
que tu trancheras à la fin de la tranche verticale (§ 5.3).

:::encart {"genre":"voir","titre":"Techniques employées, pour mémoire"}
Les cadres sont un **InstancedMesh** : une seule géométrie, treize instances, un seul appel de rendu.
C'est ce qui permettra plus tard de dessiner des milliers de cadres sans effondrer la cadence
d'affichage. Le rendu est **à la demande** : aucune boucle d'animation ne tourne quand rien ne bouge.
La scène est initialisée à l'affichage et **libérée** en sortie, avec un plafond de contextes WebGL
simultanés.
:::

## Le métré, recalculé par deux voies

Le tableau ci-dessous n'est pas saisi : chaque nombre est une variable produite par `calc/cage.py`.

| Grandeur | Valeur |
|---|---:|
| Nombre de cadres | {{metre-cage.n_cadres}} |
| Périmètre d'un cadre | {{metre-cage.perimetre_cadre_m::n3s}} m |
| Longueur développée de cadres | {{metre-cage.longueur_cadres_m::n2}} m |
| Barres longitudinales | {{metre-cage.n_barres}} de {{metre-cage.longueur_barre_m::n2}} m |
| Masse des cadres | {{metre-cage.masse_cadres_kg::n1}} kg |
| Masse des barres | {{metre-cage.masse_barres_kg::n1}} kg |
| **Masse totale d'acier** | **{{metre-cage.masse_acier_kg::n1}} kg** |
| Volume de béton | {{metre-cage.volume_beton_m3::n3s}} m³ |
| Ratio | {{metre-cage.ratio_kg_m3::n1}} kg/m³ |

**Contre-calcul.** Voie A, premiers principes : aire de la section droite × longueur × masse
volumique, soit {{metre-cage.contre_calcul.voie_A_premiers_principes_kg::n2}} kg. Voie B, coefficient
tabulé des plans de ferraillage $m = 0{,}00617\,d^2$ en kg/m avec $d$ en mm, soit
{{metre-cage.contre_calcul.voie_B_coefficient_tabule_kg::n2}} kg. **Écart :
{{metre-cage.contre_calcul.ecart_pct::n2}} %**, pour une tolérance de
{{metre-cage.contre_calcul.tolerance_pct::n0}} % (§ 3.3).

Un écart aussi faible est attendu : les deux voies décrivent la même géométrie et la seconde dérive
historiquement de la première. Ce n'est donc **pas** une preuve que le modèle est juste — c'est un
filet qui attrape les erreurs d'unité, de facteur et de saisie. La vraie parade contre une erreur de
modèle partagée, c'est l'étalonnage ci-dessous, et la contre-expertise à l'aveugle du § 12.2.

## L'étalonnage, sur une solution fermée

Le périmètre d'un cadre à coins arrondis a une solution analytique : les quatre quarts de cercle
forment un cercle complet, donc

$$P = 2\,(b - 2r) + 2\,(h - 2r) + 2\pi r$$

`calc/etalonnage/perimetre_cadre.py` compare cette formule à une **discrétisation numérique du même
contour** (200 000 segments) sur trois cas, dont un cas limite à rayon nul, et vérifie qu'un rayon de
cintrage impossible est **refusé** au lieu d'être accepté en silence. Sans cet étalonnage, les sorties
de `calc/` resteraient V3 et ne pourraient pas servir d'exemple de référence.

:::encart {"genre":"alerte","titre":"Ce que l'étalonnage a réellement attrapé"}
La première version de la cage 3D construisait le cadre comme une courbe de Catmull-Rom passant par
les coins. Une spline ne suit pas un rectangle à coins arrondis : elle **gonfle entre les points**. Le
périmètre sortait à 2,386 m au lieu de 1,926 m, soit **+ 23,9 %**, et la masse de cadres à 12,24 kg au
lieu de 9,88 kg.

À l'écran, rien ne se voyait : la cage avait l'air juste. C'est le croisement entre le métré de `calc/`
et celui de la 3D qui a révélé l'écart. Le contour est maintenant suivi exactement (droites et arcs),
à 0,007 % de la formule fermée.

**La leçon vaut pour tout le cours : un modèle 3D peut être faux sans en avoir l'air.** C'est pourquoi
la 3D vient toujours après le calcul, jamais à sa place.
:::

:::encart {"genre":"alerte","titre":"Le piège que le ratio d'acier enseigne"}
Le ratio obtenu est de **{{metre-cage.ratio_kg_m3::n1}} kg/m³**, alors que la fourchette usuelle d'une
poutre **dimensionnée** est de l'ordre de 80 à 150 kg/m³ (V3, déclarée). L'écart n'est pas une erreur
de calcul : il vient de ce que cette cage **n'a jamais été dimensionnée**. Les diamètres et le nombre
de barres sont des paramètres de démonstration.

Le contrôle d'ordre de grandeur de `calc/tests/test_cage.py` a signalé cet écart dès la première
exécution. Deux réactions étaient possibles : élargir la fourchette jusqu'à ce que le test passe, ou
inventer un ferraillage plus lourd pour y entrer. Les deux sont malhonnêtes — la seconde fabriquerait
un dimensionnement que la phase § 5.0 interdit. Le contrôle a donc été ramené à ce qu'il sert
vraiment : **attraper une erreur d'unité ou de facteur** (fourchette géométrique 30 à 250 kg/m³), et
l'écart avec une poutre dimensionnée est **rapporté** sans faire échouer le test.

On ne lit pas un ferraillage dimensionné sur un modèle 3D.
:::

## Ce que le contrôle vérifie

:::figure {"fn":"sequence","args":["Données data/","Calcul calc/ + étalonnage","Build : SVG, 3D, variables","Tests : rendu, captures, réseau","Module publié"],"titre":"La chaîne de génération, et où chaque contrôle intervient","num":2,"voir":["Aucune flèche ne revient en arrière : un nombre ne remonte jamais du rendu vers les données.","Le build échoue si une variable manque, si une légende est incomplète, ou si un nombre d'un bloc normatif n'est pas balisé.","Les tests examinent le rendu réel dans un navigateur, pas une déclaration de l'auteur."]}
:::

La commande `npm run check` enchaîne : étalonnage et tests de `calc/`, build, puis contrôle du rendu
dans un Chromium sans affichage — zéro erreur de console, contexte WebGL créé, captures non vides
(variance de pixels mesurée), étiquettes sans chevauchement, curseurs testés **à leurs bornes**,
**aucune requête réseau**, poids des fichiers, empreinte de `data/` identique partout. Elle vérifie
enfin que le **zip de reprise du mode B** se rouvre dans un répertoire neuf et y repasse au vert.

:::exercice {"titre":"Vérifier soi-même que la chaîne tient","niveau":"application"}
Ouvre `data/demo-cage.json`, remplace l'espacement des cadres par 7 cm, puis relance
`npm run calc && npm run build`.

**Attendu** : le nombre de cadres passe de 13 à 28, la masse d'acier augmente d'environ 11 kg, la
figure 1 est inchangée (l'espacement ne se voit pas en coupe), la cage 3D montre les cadres resserrés,
et l'empreinte de `data/` affichée en pied de page change. Si l'un de ces cinq effets manque, la chaîne
est rompue quelque part : c'est exactement ce que le contrôle d'empreinte du § 4.3 sert à détecter.
:::
