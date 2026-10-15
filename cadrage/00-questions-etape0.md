# Étape 0 — (b) Les 10 questions, posées en une seule fois

> **« OK partout »** accepte tous les défauts et je lance l'Étape 1 immédiatement.
> Sinon réponds par numéro ; tout ce que tu ne mentionnes pas prend la valeur par défaut.
> Les réponses partent dans `DECISIONS.md` et figent `data/projet-gare.json` en version 1.0.

---

**1 · Environnement et budget.**
Mode **B** retenu : zip de reprise à chaque fin de module, zip redonné au début de chaque séance, seul le
zip fait foi. Tout l'outillage exigé par le § 4.1 est présent (Node 22, Python 3.13, Chromium headless,
git, zip) — détail et deux réserves dans `cadrage/01-environnement.md`.
Il me manque : **combien de séances par semaine**, **quel budget total**, et **la date de fin du palier 1**
(exigée par le § 5.5). Voir la réserve sur cette date au § 1 de `cadrage/06-volume-arret-coupe.md` : je
propose **deux dates**, une ferme pour le palier 1 actif, une indicative pour le palier 1 complet.
*À noter aussi :* ce bac à sable a un **dépôt git distant** qui survit entre les conversations. Tu es de
fait un cran au-dessus du mode B. Veux-tu rester en B (zip) ou basculer en **A** (reprise depuis la
branche, sans zip à manipuler) ?

**2 · Référentiels.**
*Défaut :* option **M** (BAEL 91 mod. 99 ; BPEL 91 ; RPS 2000 v. 2011 avec contrôle du catalogue
communal 2024 ; NV 65, N 84, NF P 06-001) et **Eurocodes 1re génération** pour la charpente métallique,
avec annexe comparative sur la 2e. Matrice complète : `cadrage/03-referentiels.md`.
**Situation actuelle : aucun document fourni → `normes_disponibles = false`, phase § 5.0 active.**
Les trois documents qui débloquent le plus de modules, par ordre d'effet : **BAEL 91 mod. 99** (6 modules),
**RPS 2000 + catalogue communal** (2 modules + le double zonage), **le CPS du marché** (il prime sur tout
pour D1 et D4, et il fixe le référentiel ferroviaire). Dépose-les dans `docs/` et écris
« normes disponibles » quand tu les as.

**3 · Site de la gare.**
*Défaut :* **S1, région de Marrakech** (sismicité modérée, reclassement 2024 applicable → double zonage à
traiter). Les trois options comparées : `cadrage/02-jeu-de-donnees.md` § 1.
**Ma recommandation diffère légèrement du défaut** : garder S1 pour la gare **et** prendre **S2 (Agadir,
nappe à 3,5 m, sables lâches, sismicité forte)** comme site du second site de D7. Tu obtiens le double
zonage *et* les sols difficiles — donc B1b, la liquéfaction et l'interaction sol-structure, tous classés
[N] ou [C] chez toi — sans alourdir le cas phare. Si tu ne veux qu'un site, je prends S2 : un cours où la
géotechnique est facile se prive de la moitié des pièges réels.

**4 · Géométrie de la gare.**
*Défaut :* emprise **120 × 40 m** ; trame **7,50 m** × 16 ; transversale **4 + 32 + 4** ; niveau technique
partiel à **−4,00** ; hall double hauteur **h = 9,00 m** ; mezzanine à **+5,00** sur **120 × 24 m** ;
couverture en treillis de **32 m** de portée libre, sous-face à **+12,50** ; marquise en porte-à-faux de
**4,50 m** ; accès aux quais par **passage souterrain**, 3 quais.
Élément du module témoin n° 1 : poutre **PM1**, travées **8,00 / 8,00 / 8,00 m** + console **4,50 m**,
entraxe 7,50 m, section 35 × 75 cm (**prédimensionnement V3**, pas un résultat).
**Le R+5 reste-t-il en cas secondaire léger ?** *Défaut : oui*, même site, sans plans d'exécution complets
ni maquette 3D globale.

**5 · Calibrage et ajouts.**
Tableau [M]/[C]/[N] pré-rempli pour les 35 modules du périmètre technique : `cadrage/04-calibrage.md`. Corrige la colonne « Niv. ».
Quatre points à trancher :
- **Le logiciel aux éléments finis que tu pratiques** (pour B6b) : Robot, ETABS, SAP2000, Advance Design,
  autre ? Les pièges se nomment différemment selon l'outil.
- **Plafond de 10 %** pour les lots techniques (B7b + C4) : *gardé par défaut*.
- **Cas « stade » et module C8 (démolition)** : *retenus par défaut*, tous deux en P2.
- **Module ajouté B7c — « Bâtiments ferroviaires : interfaces voie, quais, systèmes, exploitation »** :
  le § 1.1 classe ce sujet en **[N]** et c'est ton quotidien, mais **aucun module du § 11 ne le porte**.
  Je propose de l'ajouter en P1, actif dès maintenant (2 livraisons). **C'est une addition au périmètre :
  elle demande ton accord.**

**6 · Priorités et ordre de coupe.**
*Défaut :* P1 → P2 → P3, chaque palier conditionné à ton go/no-go. Ordre de livraison **dans** le palier 1
proposé au § 6 de `cadrage/05-sommaire.md` : **D2, D1, D3, D4, D7 d'abord** (ton métier), puis l'exécution
C1–C7, puis B7c, puis les fondamentaux qualitatifs. C'est l'inverse de l'ordre alphabétique du § 11, et
c'est volontaire.
*Ordre de coupe (défaut, § 3 de `cadrage/06-volume-arret-coupe.md`)* : 3D non structurels → O6 des [M] →
palier 3 → O5 des [M] → cas R+5. J'ai inversé O6 et P3 par rapport à la lettre du § 5.1d et ajouté le R+5 :
raison donnée, à toi de trancher.
*Une question en plus :* `B5a` (charpente de la couverture) est suspendu parce que son calcul l'est — mais
sa **partie exécution** (fabrication, soudage, levage au-dessus de la voie) est en [M] et **ne dépend
d'aucune norme**. Veux-tu que je la détache en module actif dès maintenant ?

**7 · Prix.**
*Défaut :* année de référence **2026**, prix unitaires **V3** en fourchettes, inscrits dans
`registre-hypotheses.csv`. **As-tu un bordereau non confidentiel, même ancien, même partiel ?** C'est, après
le BAEL, le document le plus rentable du projet : il ferait passer tout le volet économique de « fourchettes
déclarées » à « valeurs recalées », et c'est le cœur de ton poste.

**8 · Revue indépendante « /devil ».**
*Défaut :* auto-revue hostile à chaque module (changement explicite de casquette, Annexe 4), **plus** une
session distincte à chaque fin de palier. Des sous-agents sont disponibles dans ce bac à sable : je peux
faire porter la passe par un agent séparé qui ne lit pas mon raisonnement et recalcule trois valeurs clés
depuis `data/` seulement — c'est plus proche de l'esprit du § 12.2 qu'une auto-revue. *Je propose de le
faire par défaut.* Le contrôle « canari » tous les cinq modules reste en place.

**9 · Format de rendu.**
*Défaut :* HTML responsive **hors ligne** (aucun CDN à l'exécution), formules KaTeX **pré-rendues au
build**, sommaire latéral, exercices dépliables, feuille d'impression pour exercices et fiches mémo,
contrastes AA, repli lisible si WebGL2 absent, ≤ 1,5 Mo par module. D'accord, ou autre exigence ?

**10 · Ancienne version et documents.**
*Défaut :* **rien à reprendre** — aucun fichier de l'ancienne version n'a été fourni, donc navigation, mise
en page et modules de gestion sont refaits. Les fichiers du projet réel (plans, IFC) **ne sont pas versés
au cours sans anonymisation**, et le § 10.1 impose de toute façon un programme fictif.

---

## Ce qui part dès ton « go »

**Étape 1 — socle** (§ 5.2) : charte graphique, navigation, chaîne de build, bibliothèque `civil3d`,
`svgkit.js`, scripts de test, squelette de `data/`, `STATE.md`, `DECISIONS.md`, dépôt git, `pint` installé,
**plus une page de démonstration testée** (cage d'armatures paramétrique) avec la sortie des tests.
Puis **Étape 2 — tranche verticale de suivi**, que tu valides avant toute duplication.
