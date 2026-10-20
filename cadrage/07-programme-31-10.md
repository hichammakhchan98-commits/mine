# Programme recentré — livraison au 31/10/2026

Décisions D-033 (recentrage) et D-034 (échéance). Ce fichier **remplace l'ordre de livraison** du
§ 6 de `05-sommaire.md` ; l'ancien périmètre reste dans git pour mémoire.

## Ce qui est abandonné

**Tout le palier 3** : aéroport, port, barrage et digue, tunnel, hydraulique et maritime, routes et
chaussées, gestion d'entreprise de BTP. **Du palier 2**, ne survivent que les sujets qui touchent une
gare — le pont, le stade, la précontrainte et la démolition sortent aussi. Ce n'est pas un report :
c'est une suppression, décidée par le lecteur le 20/10/2026.

Le cours passe de **90 à 24 livraisons**, dont 2 déjà faites.

## Les dix modules de la série, dans l'ordre de livraison

L'ordre suit le quotidien d'un Chef de Projet Suivi : d'abord ce qui sert tous les jours, ensuite ce
qui sert à comprendre ce qu'on suit.

| # | ID | Titre | Pourquoi à cette place | Livr. |
|---|---|---|---|---|
| 1 | **D2** | Planification : WBS, familles de durées, CPM, fenêtres de consignation, lissage | tout s'y accroche ; le moteur est écrit et testé | 1 |
| 2 | **D1** | Métrés, prix, sous-détails, situations de travaux | la deuxième colonne du suivi ; alimente D4 | 2 |
| 3 | **D4** | Suivi et contrôle : avancement, attachements, valeur acquise, visas | le cœur du poste ; D2 et D1 le rendent possible | 2 |
| 4 | **C3** | Gros œuvre : coffrage, ferraillage, bétonnage, cycle par niveau | l'exécution que D1–D4 pilotent | 2 |
| 5 | **B3e** | Béton armé **en exécution** : lire un plan, dispositions, nomenclature, métré, contrôle | ce qu'on vise et ce qu'on refuse, sans calcul réglementaire | 2 |
| 6 | **B7c** | Bâtiments ferroviaires : quais, voie, systèmes, travaux sous exploitation | la spécificité du cas phare, et de votre poste | 2 |
| 7 | **C4+B7b** | Second œuvre et lots techniques : synthèse, interfaces, réservations | plafonné à 10 % du cours (§ 2.2) | 2 |
| 8 | **C1** | Installation de chantier : plan masse, grues, base-vie, circulations | se lit après avoir vu le cycle et les moyens | 1 |
| 9 | **C7** | Qualité, HSE, environnement : plans de contrôle, essais, risques | clôt l'exécution | 1 |
| 10 | **REC** | Réception, DOE, garanties | fin du déroulé du § 10.2 | 1 |

**Total : 16 livraisons**, plus les 2 faites (socle et tranche verticale) = **18**. Les 6 restantes
(A1 acteurs et contrats, A2a matériaux, D3 moyens, D6 BIM de suivi, M3D maquette, RC1 revue critique)
sont **optionnelles** et ne seront écrites que si le temps le permet.

## Ce qui reste suspendu faute de documents (§ 5.0)

Le **calcul** du béton armé — descente de charges, combinaisons, sections, ferraillage chiffré,
séisme, feu — reste fermé tant que BAEL, RPS et le CPS ne sont pas fournis. Le module **B3e** livre
tout ce qui n'en dépend pas, et c'est l'essentiel du travail de suivi : lire, vérifier, métrer,
viser. Le jour où les documents arrivent, un module **B3c** s'ajoute et reprend les renvois « ⏸ ».

## Ce que l'échéance coûte

Une passe adversariale par module au lieu du cycle « jusqu'à zéro bloquant ». Les bloquants sont
corrigés ; les majeurs et mineurs partent en **dette déclarée** dans `STATE.md`. Les modules de cette
série ne portent donc pas la garantie de la tranche verticale, et `STATE.md` le dit module par module.
