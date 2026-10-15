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
3. **Contre-calcul (§ 3.3).** La masse d'acier est calculée deux fois par deux chemins **qui
   divergent sur le périmètre du cadre**. Ce que ces deux voies partagent, et ce qu'elles ne peuvent
   donc pas attraper, est écrit noir sur blanc plus bas — c'est une limite, pas une garantie.
4. **Étalonnage (§ 3.3).** La formule fermée du périmètre est confrontée à une polygonalisation
   indépendante du contour, et à deux cas dont la solution est connue hors de cette formule.
5. **Hors ligne (§ 4.4).** Aucune requête réseau : la page fonctionne en `file://`, formules comprises.

## La section, dessinée depuis les données

:::figure {"fn":"coupeSection","args":"demo-cage","titre":"Coupe de la section, générée depuis data/demo-cage.json","motifs":["beton"],"num":1,"legende":[{"n":1,"t":"béton"},{"n":2,"t":"barres longitudinales"},{"n":3,"t":"cadre"}],"voir":["Les barres ne sont pas posées à l'œil : leur abscisse est calculée à partir de la largeur, de l'enrobage et du diamètre, puis répartie sur la place utile.","Le cadre est tracé à l'intérieur de l'enrobage, et les barres à l'intérieur du cadre : c'est l'ordre réel d'un plan de ferraillage.","Les cotes affichées sont les variables du fichier de données, pas du texte."],"erreur":"Dessiner les barres à l'intérieur de l'enrobage en oubliant l'épaisseur du cadre : sur un plan, l'erreur se voit à peine ; au coffrage, l'enrobage réel est insuffisant."}
:::

La section est celle du prédimensionnement **V3** de la poutre `PM1` du cas phare : la démonstration
parle du même ouvrage que le cours, pour que rien ne soit gratuit.

## La cage, en trois dimensions

:::model3d {"id":"cage","titre":"Cage d'armatures paramétrique","init":"demoCage","sous":"Curseurs bornés, plan de coupe, vue éclatée et phasage. Clique une étiquette pour la déplier. Le bouton réinitialise le cadrage."}
:::

::: encart {"genre":"attente","titre":"Quatre conventions et simplifications, déclarées (R6)"}
1. **Les cadres n'ont pas de crochets d'extrémité.** Un cadre réel en porte deux. Le métré ci-dessous
   est donc **minorant d'environ 3 %** sur les cadres. La longueur d'un crochet est une valeur
   constructive : elle n'est pas avancée ici, la phase § 5.0 l'interdit.
2. **Le rayon de cintrage vaut ⟦V3|rayon de cintrage du cadre|20|mm|15 à 30|2026|paramètre de tracé, non une règle de cintrage minimal : aucun document normatif fourni⟧ mm**,
   lu dans `data/demo-cage.json`. C'est un paramètre de **tracé**, pas un rayon minimal réglementaire.
   Il porte 1,8 % du périmètre : à coins vifs, le cadre mesurerait davantage.
3. **L'enrobage vaut aussi le long de l'axe.** L'axe du premier cadre est à l'enrobage **plus** le
   demi-diamètre du cadre de l'about, exactement comme en section. Sans ce terme, la peau du cadre
   se retrouvait à 26 mm de l'about pour un enrobage annoncé de 30.
4. **Le coffrage modélisé n'a ni étaiement ni étais de reprise**, et la phase 4 retire les panneaux
   sans dire à quelle condition. Dans la réalité, le décoffrage est subordonné à une résistance
   atteinte, contrôlée sur éprouvettes ; le décoffrage prématuré est l'un des pièges listés au § 7.3.
   Le sujet est traité au module d'exécution, en attente des normes.
:::

Ce que la 3D apporte ici et qu'une coupe ne donne pas : **la répartition des cadres sur la longueur**
et l'ordre dans lequel les choses arrivent sur le chantier. Fais glisser le curseur de phase :
coffrage, ferraillage, bétonnage, décoffrage — le coffrage apparaît à la première phase et disparaît à
la dernière. Cette question — *la 3D apporte-t-elle plus qu'une bonne coupe ?* — est exactement celle
que tu trancheras à la fin de la tranche verticale (§ 5.3).

:::encart {"genre":"voir","titre":"Techniques employées, pour mémoire"}
Les cadres sont un **InstancedMesh** : une seule géométrie, {{metre-cage.n_cadres}} instances, un seul appel de rendu.
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

**Contre-calcul.** Les deux voies divergent sur le chemin de longueur du cadre.

| | Longueur d'un cadre | Masse |
|---|---|---|
| **Voie A** | contour **discrétisé** (droites + arcs), celui-là même que suit le tube de la scène 3D → {{metre-cage.contre_calcul.perimetre_voie_A_m::n3s}} m | aire de la section droite × longueur × masse volumique |
| **Voie B** | **formule fermée** $P = 2(b-2r) + 2(h-2r) + 2\pi r$ → {{metre-cage.contre_calcul.perimetre_voie_B_m::n3s}} m | coefficient tabulé des plans de ferraillage, $m = 0{,}00617\,d^2$ en kg/m, $d$ en mm |

Elles ne divergent **pas** sur le reste, et c'est une limite qu'il faut écrire plutôt que masquer :
le coefficient tabulé $0{,}00617$ dérive lui-même de $\pi/4 \times 7850 \times 10^{-6} = 0{,}0061654$,
si bien que l'écart de masse entre les deux voies n'est pour l'essentiel que cet arrondi. Les deux
partagent aussi **le nombre de cadres**, **la règle d'axe du cadre** et **les longueurs de barres**.

**Ce que ce contre-calcul n'attrape donc pas** : une erreur commune aux deux voies — un comptage de
cadres faux, une règle d'axe fausse, une longueur de barre fausse.

Il faut être précis sur ce qui les rattrape, parce que désigner un filet qui n'existe pas est pire que
de n'en désigner aucun. **Ce n'est pas l'étalonnage** : `calc/etalonnage/` ne manipule que des triplets
(largeur, hauteur, rayon) et ignore tout du comptage, de la règle d'axe et des longueurs. Ce sont des
**tests qui recalculent ces trois grandeurs dans le test lui-même**, à partir de `data/` et de la
convention publiée, sans appeler le code qu'ils contrôlent. C'est la seule parade contre une erreur de
modèle partagée (§ 3.3) : une seconde voie écrite par le même auteur ne suffit jamais.

Résultats : {{metre-cage.contre_calcul.voie_A_kg::n2}} kg contre
{{metre-cage.contre_calcul.voie_B_kg::n2}} kg, soit un **écart de
{{metre-cage.contre_calcul.ecart_pct::n2}} %** pour une tolérance de
{{metre-cage.contre_calcul.tolerance_pct::n0}} % (§ 3.3). Sur le périmètre seul, les deux chemins
s'écartent de {{metre-cage.contre_calcul.ecart_perimetre_pct::n3s}} %.

:::encart {"genre":"alerte","titre":"La première version de ce contre-calcul n'en était pas un"}
Les deux voies partaient de la même formule, la seconde n'étant que la première avec une constante
arrondie : $\pi/4 \times 7850 \times 10^{-6} = 0{,}0061654$ contre $0{,}00617$. L'« écart » publié,
0,075 %, n'était rien d'autre que cet arrondi. Pire, les deux voies partageaient **toute la
géométrie** : nombre de cadres, périmètre, longueurs. Aucune erreur géométrique n'était visible par
ce contrôle.

C'est la « limite et parade » du § 3.3 — deux voies écrites par le même auteur partagent volontiers
la même erreur de modèle. La parade n'est pas de multiplier les voies, c'est de les faire diverger
sur les facteurs qui comptent, et de les **étalonner** sur autre chose qu'elles-mêmes.
:::

## L'étalonnage, sur une solution fermée

Le périmètre d'un cadre à coins arrondis a une solution analytique : les quatre quarts de cercle
forment un cercle complet, donc

$$P = 2\,(b - 2r) + 2\,(h - 2r) + 2\pi r$$

`calc/etalonnage/perimetre_cadre.py` l'étalonne de trois façons : une **polygonalisation indépendante
du contour entier** (le contour est l'ensemble des points à distance $r$ du rectangle réduit — aucun
terme n'est repris de la formule) ; deux **cas à solution connue hors formule**, le cercle
($b = h = 2r$, périmètre $2\pi r$) et le rectangle à coins vifs ($r = 0$, périmètre $2(b+h)$) ; et la
vérification qu'un rayon de cintrage impossible est **refusé** au lieu d'être accepté en silence.

Là aussi, la première version était creuse : elle recopiait le terme droit de la formule et ne
discrétisait que les quatre arcs, soit 6,5 % du périmètre. Une erreur sur la partie droite serait
passée des deux côtés.

:::encart {"genre":"alerte","titre":"Ce que l'étalonnage a réellement attrapé"}
La première version de la cage 3D construisait le cadre comme une courbe de Catmull-Rom passant par
les coins. Une spline ne suit pas un rectangle à coins arrondis : elle **gonfle entre les points**, de
près de **24 %** sur le périmètre.

À l'écran, rien ne se voyait : la cage avait l'air juste. C'est le croisement entre le métré de `calc/`
et celui de la 3D qui a révélé l'écart. Le contour est maintenant suivi exactement (droites et arcs) :
le périmètre vaut {{metre-cage.perimetre_cadre_m::n3s}} m, à
{{metre-cage.contre_calcul.ecart_perimetre_pct::n3s}} % de la formule fermée.

**La leçon vaut pour tout le cours : un modèle 3D peut être faux sans en avoir l'air.** C'est pourquoi
la 3D vient toujours après le calcul, jamais à sa place.
:::

:::encart {"genre":"alerte","titre":"Le piège que le ratio d'acier enseigne"}
Le ratio obtenu est de **{{metre-cage.ratio_kg_m3::n1}} kg/m³**, alors que la fourchette usuelle d'une
poutre **dimensionnée** est de l'ordre de ⟦V3|ratio d'acier d'une poutre dimensionnée|80 à 150 kg/m³|kg/m³|80 à 150|2026|ordre de grandeur usuel, sans valeur réglementaire⟧. L'écart n'est pas une erreur
de calcul : il vient de ce que cette cage **n'a jamais été dimensionnée**. Les diamètres et le nombre
de barres sont des paramètres de démonstration.

Le contrôle d'ordre de grandeur de `calc/tests/test_cage.py` a signalé cet écart dès la première
exécution. Deux réactions étaient possibles : élargir la fourchette jusqu'à ce que le test passe, ou
inventer un ferraillage plus lourd pour y entrer. Les deux sont malhonnêtes — la seconde fabriquerait
un dimensionnement que la phase § 5.0 interdit. Le contrôle a donc été ramené à ce qu'il sert
vraiment : **attraper une erreur d'unité ou de facteur** (⟦V3|garde-fou d'unité sur le ratio d'acier|fourchette géométrique 30 à 250 kg/m³|kg/m³|30 à 250|2026|borne large, choisie pour n'attraper qu'une erreur de facteur⟧), et
l'écart avec une poutre dimensionnée est **rapporté** sans faire échouer le test.

On ne lit pas un ferraillage dimensionné sur un modèle 3D.
:::

## Ce que ces kilos coûtent, et ce qu'ils prennent de temps

Un métré n'a d'intérêt que s'il se transforme en argent et en jours. Deux ordres de grandeur, tous
deux **V3 déclarés**, pour montrer le chemin — ils seront repris sérieusement dans les modules D1 et D3 :

- **Coût.** À ⟦V3|prix de l'acier HA façonné et posé|14 à 20 MAD/kg|MAD/kg|14 à 20|2026|aucun bordereau fourni : fourchette large assumée⟧, les
  {{metre-cage.masse_acier_kg::n1}} kg de ce tronçon représentent
  **{{metre-cage.economie.cout_acier_MAD_min}} à {{metre-cage.economie.cout_acier_MAD_max}} MAD**
  d'acier, pour {{metre-cage.volume_beton_m3::n3s}} m³ de béton. Le ratio de
  {{metre-cage.ratio_kg_m3::n1}} kg/m³ est la grandeur qui pilote ce poste : c'est pour cela qu'un
  ratio d'acier se surveille sur un chantier, pas seulement sur une note de calcul.
- **Délai.** À ⟦V3|cadence de façonnage et pose d'armatures|90 à 130 kg par ferrailleur et par jour|kg/jour|90 à 130|2026|ordre de grandeur de chantier, à recaler sur des attachements réels⟧,
  ce tronçon représente **{{metre-cage.economie.heures_ferrailleur_min::n1}} à
  {{metre-cage.economie.heures_ferrailleur_max::n1}} heures** d'un ferrailleur. Mais la grandeur qui commande le planning
  n'est pas la masse : c'est le **nombre de cadres** — {{metre-cage.n_cadres}} ici, et
  {{metre-cage.variante_exercice.n_cadres}} si l'espacement passe à
  {{metre-cage.variante_exercice.espacement_cm}} cm. Un cadre se façonne, se transporte et se pose à
  l'unité : resserrer les cadres coûte proportionnellement plus en main-d'œuvre qu'en acier.

C'est le genre de lien que chaque module du cours devra faire, et que la grille du § 7.2 contrôle.

## Ce que le contrôle vérifie

:::figure {"fn":"sequence","args":["Données data/","Calcul calc/ + étalonnage","Build : SVG, 3D, variables","Tests : rendu, captures, réseau","Module publié"],"titre":"La chaîne de génération, et où chaque contrôle intervient","num":2,"voir":["Aucune flèche ne revient en arrière : un nombre ne remonte jamais du rendu vers les données.","Le build échoue si une variable manque, si une légende est incomplète, ou si un nombre d'un bloc normatif n'est pas balisé.","Les tests examinent le rendu réel dans un navigateur, pas une déclaration de l'auteur."]}
:::

La commande `npm run check` enchaîne : étalonnage et tests de `calc/`, build, puis contrôle du rendu
dans un Chromium sans affichage — zéro erreur de console, contexte WebGL créé, captures non vides
(variance de pixels mesurée), étiquettes sans chevauchement, curseurs testés **à leurs bornes**,
**aucune requête réseau**, poids des fichiers, empreinte de `data/` identique partout. Elle vérifie
enfin que le **zip de reprise du mode B** se rouvre dans un répertoire neuf et y repasse au vert.

:::exercice {"titre":"Vérifier soi-même que la chaîne tient","niveau":"application"}
Ouvre `data/demo-cage.json`, remplace l'espacement des cadres par
{{metre-cage.variante_exercice.espacement_cm}} cm, puis relance `npm run calc && npm run build`.

**Attendu** : le nombre de cadres passe de {{metre-cage.n_cadres}} à
{{metre-cage.variante_exercice.n_cadres}}, la masse d'acier augmente de
{{metre-cage.variante_exercice.delta_masse_kg::n1}} kg, la figure 1 est **inchangée** (l'espacement ne
se voit pas en coupe), la cage 3D montre les cadres resserrés, et l'empreinte de `data/` affichée en
pied de page change. Si l'un de ces cinq effets manque, la chaîne est rompue quelque part : c'est
exactement ce que le contrôle d'empreinte du § 4.3 sert à détecter.

*(Ces valeurs attendues sont elles-mêmes calculées par `calc/cage.py`, pas écrites dans le texte : si
la règle de placement des cadres change, l'énoncé de l'exercice suit.)*
:::
