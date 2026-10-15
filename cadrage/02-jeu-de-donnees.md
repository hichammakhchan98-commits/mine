# Étape 0 — (c) Jeu de données du cas phare : proposition justifiée

> **Statut : PROPOSITION.** `data/projet-gare.json` est en version `0.1-propose`. Il ne passe en **1.0
> figée** (date + commit) qu'après ta validation (§ 5.1c/e). Après quoi il ne change plus sans décision
> consignée dans `DECISIONS.md`, et tout changement déclenche le build complet et la revue des modules
> impactés.

**Avertissement** : programme fictif et générique, inspiré du *type* de projet, ne reproduisant aucun
projet réel. Toutes les valeurs ci-dessous sont **V3** (hypothèses déclarées) : aucune ne vient d'une
reconnaissance réelle ni d'un règlement.

---

## 1. Site — trois options à sismicité contrastée (question 3)

Le choix du site n'est pas décoratif : il décide quels modules deviennent riches et quels modules
deviennent vides. C'est le paramètre le plus structurant du cours.

| | **S1 — région de Marrakech** *(défaut proposé)* | **S2 — Agadir** | **S3 — Casablanca** |
|---|---|---|---|
| Sismicité | modérée | **forte** | faible |
| Reclassement 2024 | **oui** (préfecture de Marrakech, 8 communes) → double zonage à traiter | non | non |
| Sol | alluvions limono-sableuses denses du Haouz sur conglomérat | sables dunaires lâches à moyennement denses | schistes et quartzites sous faible couverture |
| Nappe | 18,0 m | **3,5 m** | 12,0 m |
| q_adm (V3) | 250 kPa | 120 kPa | 600 kPa |
| Fondations probables | superficielles / radier | **profondes** ou amélioration de sols | semelles isolées, excavation en rocher |
| Liquéfaction | sans objet | **à vérifier** — déclencheur du volet liquéfaction + interaction sol-structure | sans objet |
| Ce que le site rend vivant | B1 superficielles, B2, double zonage sismique | B1 profondes, **B1b**, liquéfaction, ISS, corrosion marine, rabattement de nappe | presque rien en géotechnique et en séisme |
| Coût pédagogique | moyen | **élevé** (modules en plus) | faible |

Détail des coupes géotechniques fictives (SPT, pressiomètre, CPT, laboratoire) : `data/projet-gare.json`
→ `site.options.S*.coupe_geotechnique_V3`.

**Ma recommandation : S1 (région de Marrakech), comme le propose le prompt — mais sans enthousiasme, et
voici pourquoi.**

S1 a un vrai atout pédagogique que les deux autres n'ont pas : le reclassement de 2024 s'y applique, donc
le cours traite **deux zonages pour un même bâtiment**, l'un en cas principal, l'autre en annexe
comparative. C'est exactement la situation qu'un chef de projet rencontre quand un règlement bouge en
cours d'opération, et ça force la discipline du § 3.1 (ne jamais mélanger deux cadres dans un même
calcul).

Mais S1 appauvrit la géotechnique : nappe à 18 m, sols denses, radier — B1 et B2 deviennent des modules
de routine, et B1b (amélioration de sols), que ton calibrage classe en **[N] nouveau**, n'a plus de
raison d'exister sur le cas phare. S2 (Agadir) est l'inverse : il active la liquéfaction, l'interaction
sol-structure, les fondations profondes, le rabattement de nappe et la corrosion marine — tout ce qui est
en [C] ou [N] chez toi — au prix de deux ou trois modules supplémentaires et d'un cas phare plus lourd.

**Arbitrage que je te propose** : garder **S1** pour le cas phare (gare), et poser **S2 comme site du
second site de D7** (la gare de RER, § `multi_sites`). Tu obtiens le double zonage *et* les sols
difficiles, sans alourdir le cas phare. Si tu préfères un seul site, prends S2 : un cours de génie civil
où la géotechnique est facile se prive de la moitié des pièges réels.

**Note de méthode** : les champs `zone_sismique.acceleration` et `.vitesse` restent à `null` avec la
mention « ⏸ en attente des normes ». Je **n'écrirai pas** de numéro de zone de mémoire : il se lit dans le
catalogue communal officiel en vigueur, et c'est précisément le point que la re-vérification du 15/10/2026
laisse « à lire sur le texte » (`cadrage/01-environnement.md` § 3).

---

## 2. Géométrie de départ de la gare (question 4)

Proposition cohérente avec le § 10.1 (emprise ≈ 120 × 40 m, grandes portées, couverture 30–40 m,
marquise 4–6 m) :

| Poste | Valeur proposée | Justification |
|---|---|---|
| Emprise | **120 × 40 m** | borne haute du § 10.1 |
| Trame longitudinale | **7,50 m** × 16 travées = 120,00 m | 7,5 m tombe juste sur 120 m (7,2 m ne tombe pas) ; c'est aussi un entraxe courant de treillis de couverture |
| Découpage transversal | nef ville 4,0 + **hall 32,0** + nef voies 4,0 = 40,0 m | portée libre de 32 m : dans la fourchette 30–40 m, et assez pour que le treillis soit un vrai sujet |
| Niveau technique | **−4,00 m**, partiel 40 × 20 m | locaux techniques + raccordement du passage souterrain. Un seul sous-sol partiel : le § 10.1 ne demande pas 2 sous-sols (c'est le R+5 qui les porte) |
| RDC — hall | **+0,00**, h libre **9,00 m** | hall double hauteur |
| Mezzanine | **+5,00**, bande continue 120 × 24 m, h libre 4,00 m | salles d'attente, restauration, bureaux d'exploitation |
| Sous-face de couverture | **+12,50 m** | treillis plans, membrures parallèles, hauteur 2,20 m (h/L ≈ 1/14,5 — ordre de grandeur V3) |
| Marquise | porte-à-faux **4,50 m** au niveau mezzanine, côté voies | dans la fourchette 4–6 m ; c'est la console du module témoin n° 1 |
| Accès aux quais | **passage souterrain** (2 escaliers + 2 escalators + 1 ascenseur par quai), 3 quais | le souterrain donne de la géotechnique et du phasage sous exploitation ; une passerelle aurait donné une seconde charpente redondante avec la couverture |
| Noyaux | 2 | contreventement + gaines |

**Élément du module témoin n° 1** (§ 7.3), tel que le prompt l'exige — « poutre continue de plancher de
la mezzanine, à trois travées, avec console de marquise » :

```
PM1 — poutre transversale de plancher de mezzanine
  travées : 8,00 / 8,00 / 8,00 m   +   console : 4,50 m (marquise)
  entraxe : 7,50 m                     section : 35 × 75 cm
```

La section 35 × 75 est un **prédimensionnement V3** par élancement usuel (h ≈ L/11). Ce n'est pas un
résultat : aucune vérification réglementaire n'est faite tant que le § 5.0 n'est pas levé, et la section
pourra changer quand elle le sera.

**R+5 en cas secondaire léger** : confirmé tel quel (25 × 40 m, 2 sous-sols, RDC 4 m, étages 3 m,
balcons en console 1,40 m), même site que la gare pour ne pas multiplier les hypothèses géotechniques,
**sans** plans d'exécution complets ni maquette 3D globale. → `data/projet-r5.json`.

---

## 3. Bâtiment et matériaux : ce qui reste volontairement vide

| Champ | État | Pourquoi |
|---|---|---|
| `classe_importance` | `null` + ⏸ | se lit dans le RPS (classe des bâtiments recevant du public). Je ne l'écris pas de mémoire |
| `classe_exposition` | `null` + ⏸ | se fixe avec la norme béton applicable |
| `resistance_feu_min` | `null` + ⏸ | se fixe par le règlement de sécurité incendie applicable et le CPS |
| `materiaux.beton.classe`, `acier_ha`, nuance de charpente | `null` + ⏸ | valeurs normatives |
| `charges.*` (G, Q, vent, neige, sismique) | **vides, bloquées** | § 5.0.1 : aucune descente de charges, aucune combinaison avant levée |
| `effectif_public` | **1 800** (V3) | hypothèse de programme, pas une valeur normative : elle sert aux flux et à l'évacuation en qualitatif |

C'est la différence entre « je ne sais pas » et « ce n'est pas encore le moment » : ces champs sont
identifiés, nommés, et attendent un document. Ils ne sont pas oubliés.

---

## 4. Interfaces ferroviaires : une lacune que je signale

Le cas phare est une gare, et le § 1.1 classe « bâtiments ferroviaires (interfaces voie, caténaire,
quais, systèmes, exploitation) » en **[N] nouveau** pour toi. Or le périmètre du § 11 n'a **aucun module**
qui porte ce sujet : B7a traite la conception globale et l'incendie, D7 le pilotage multi-sites, B10 la
voie ferrée mais en P3 et du point de vue de l'infrastructure.

Je propose donc un module en plus — **B7c, Bâtiments ferroviaires : interfaces voie, quais, systèmes et
exploitation** (P1, [N], actif en phase § 5.0 car essentiellement qualitatif). C'est une **addition au
périmètre**, elle demande donc ta validation (question 5). La matrice de référentiels reçoit en parallèle
deux lignes nouvelles (`ferroviaire-batiments`, `effets-foule-gare`), toutes deux « ⚠ à identifier » :
aucun numéro de référentiel ferroviaire ne sera écrit sans V0.
