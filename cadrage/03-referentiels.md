# Étape 0 — (d.1) Matrice de référentiels

> Statut : **proposition** (question 2). Enregistrée dans `data/referentiels.json` après validation.
>
> **Règle du § 3.1** : un référentiel principal par domaine de calcul et par cas ; l'autre apparaît en
> annexe comparative, **jamais dans le même calcul**. Mélanger des coefficients partiels, des
> combinaisons et des notations venant de deux cadres est une source classique d'erreurs.

**Option proposée** : **M (pratique marocaine)** pour le béton armé, le béton précontraint et le séisme ;
**E, 1re génération** pour l'acier et les assemblages, avec annexe comparative sur la 2e génération.
Raison : c'est le cadre du marché marocain, celui de ton CPS probable, et le mélange est cantonné à deux
domaines qui ne partagent pas de combinaison (béton / acier) — à la réserve près que les actions, elles,
sont communes : d'où NV 65 / N 84 / NF P 06-001 côté actions, pour rester cohérent avec le BAEL.

| Domaine de calcul | Référentiel proposé | Génération / millésime | Statut de vérification | Doc. à fournir |
|---|---|---|---|---|
| Charges d'exploitation, vent, neige des bâtiments | NF P 06-001, NV 65, N 84 ; option E : EN 1991-1-1/-1-3/-1-4 | versions modifiées en vigueur à identifier | V2 — ⚠ à vérifier | oui |
| Charges routières et ferroviaires des ponts | Fascicule 61 titre II ; ferroviaire à fixer par le CPS | à identifier | V2 — ⚠ à vérifier | oui |
| Béton armé | BAEL 91 mod. 99 | modificatif 99 | V2 — ⚠ **document à fournir** | **oui** |
| Béton précontraint | BPEL 91 | — | V2 — ⚠ **document à fournir** | **oui** |
| Acier et assemblages | EN 1993-1-1, -1-8, -1-9 ; exécution EN 1090 ; soudures EN ISO 5817 ; CM 66 en alternative historique | 1re génération + annexe comparative 2e | V2 — ⚠ à vérifier | oui |
| Séisme des bâtiments | RPS 2000 v. 2011 + catalogue communal à jour (décrets 2.24.766 / 2.24.767) | v. 2011 ; reclassement 2024 **publié au BO n° 7351 du 11/11/2024** | V2 + vigilance — ⚠ **lire le texte officiel et l'annexe communale avant tout calcul** | **oui** |
| Séisme des ponts | le décret du RPS vise les bâtiments → à fixer par le CPS ; à défaut EN 1998-2 | 1re génération | V2 — ⚠ à fixer | oui |
| Géotechnique | Fascicule 62 titre V et DTU 13.12, ou EN 1997-1 | 1re génération | V2 — ⚠ à vérifier | oui |
| Incendie | EN 1992-1-2 et EN 1993-1-2 ; règlement marocain de sécurité incendie à identifier | 1re gén. ; EN 1992-1-2:2023 existe | V2 — ⚠ ; existence de l'EN 1992-1-2:2023 : **V0** | oui |
| Chaussées routières | Catalogue marocain des structures types de chaussées (à identifier) | à identifier | V2 — ⚠ à identifier | oui |
| Chaussées aéroportuaires | dimensionnement : méthode dédiée à choisir ; publication : **ACR–PCR** (OACI ; SIA Maroc AIC A03-25) | ACR–PCR applicable depuis le 28/11/2024 | publication : **V0** ; dimensionnement : V2 — ⚠ | non |
| Marchés et contrats | **CPS du marché (prime)** ; CCAG-T décret 2-14-394 (13/05/2016) ; décret 2-22-431 (2023) ; FIDIC en appui | — | CCAG-T : **V0** ; 2-22-431 : ⚠ à vérifier | oui (CPS) |
| Matériaux (béton, armatures) | norme marocaine équivalente à l'EN 206 et normes NM des armatures (à identifier) | à identifier | V2 — ⚠ à identifier | oui |
| Démolition et déconstruction | références marocaines et européennes à identifier — **aucun numéro sans V0** | — | ⚠ à identifier | oui |
| Tribunes et effets de foule | à identifier — **aucun numéro sans V0** | — | ⚠ à identifier | oui |
| **Bâtiments ferroviaires** : quais, gabarits, caténaire, interfaces *(ligne ajoutée)* | référentiels du gestionnaire d'infrastructure, à fixer par le CPS — **aucun numéro sans V0** | à identifier | ⚠ à identifier | **oui** |
| **Flux de voyageurs et évacuation d'un grand volume ERP** *(ligne ajoutée)* | règlement de sécurité incendie applicable + référentiel d'exploitation | à identifier | ⚠ à identifier | oui |

Les deux dernières lignes sont des **ajouts** : la matrice A6.2 du prompt a été écrite quand le cas phare
était un R+5, et elle ne couvre pas le ferroviaire. Comme le cas phare est maintenant une gare, cette
lacune devait être nommée.

## Ce que la matrice signifie en pratique, aujourd'hui

Aucun de ces référentiels n'est utilisé comme source de valeurs tant que `normes_disponibles = false`. La
matrice ne sert pas encore à calculer : elle sert à **cadrer** et à te donner la liste exacte des
documents à réunir. Les trois premiers par ordre d'effet de déblocage :

1. **BAEL 91 mod. 99** → débloque A4, B1, B2, **B3**, B7a et la tranche verticale structurelle. C'est le
   document qui rend le plus de modules au cours.
2. **RPS 2000 v. 2011 + catalogue communal** → débloque B6 et B6b, et tranche le double zonage du site S1.
3. **CPS du marché** (même partiel, même anonymisé) → il *prime* sur tout le reste pour D1 et D4
   (cautionnement, retenue de garantie, révision des prix, pénalités, délais de paiement) et il fixe le
   référentiel ferroviaire et les annexes nationales.

Un quatrième, moins évident mais très rentable : **un bordereau de prix non confidentiel**, même ancien
(question 7). Il ferait passer tout le volet économique de V3 (fourchettes inventées) à V0 recalé — et
c'est le cœur de ton métier.
