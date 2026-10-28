# RC1 — traçabilité des erreurs plantées (§ 5.5)

Le § 5.5 exige que « chaque erreur plantée soit tracée dans `QA/RC1.md` avec sa rubrique
d'origine ». Ce dossier va plus loin que l'exigence : **aucune des sept erreurs n'est inventée.**
Chacune a été commise par ce cours, trouvée par une passe adversariale, corrigée, et documentée
dans le rapport de la passe correspondante.

## Les sept erreurs, leur origine et leur rubrique

| # | Famille | Ligne du dossier | Erreur réelle du cours | Rapport | Décision née de l'erreur | Rubrique S5 |
|---|---|---|---|---|---|---|
| **E1** | calendrier | L4 — pénalités pour 10 jours de retard | Les pénalités se comptent en jours calendaires et les frais de durée en jours ouvrés ; le cours a failli les confondre dans le chiffrage du coût du retard | `QA/D1-passe1.md` | — (le piège est publié dans la sortie de D1) | D1 · S5 « confondre les deux calendriers » |
| **E2** | condition d'emploi d'une grandeur | L5 — coût d'un décalage de réception | Le module REC appliquait le coût d'un jour **de retard** publié par D1 à des journées qui ne sont pas en retard. Les cinq montants de sa fiche mémo étaient multipliés par 7,9 | `QA/REC-passe1.md` · B1 | **D-056** | REC · S5 « chiffrer un jour sans demander si l'on est en retard » |
| **E3** | unité et double compte | L3 — durée du levage sous consignation | La durée de la tâche sous interception est un nombre de **plages**, pas de journées ; le changement d'unité était silencieux et D1 et D2 trouvaient 971 h et 2 919 h pour la même tâche | `QA/B7c-passe1.md` | **D-045** | B7c · S5 « un changement d'unité silencieux » |
| **E4** | domaine d'un ratio | L6 — alerte sur la part de main-d'œuvre | La fourchette de main-d'œuvre du **gros œuvre** a été appliquée à un bordereau qui porte aussi la charpente, la façade et les lots techniques : fausse alerte, et elle a tenu plusieurs modules | `QA/D1-passe1.md` · dette n° 10 | **D-037** | D1 · S5 « un ratio sans sa base » |
| **E5** | coût inventé | L7 — coût de la non-conformité | Le module C7 imputait 7 jours de frais de durée à un ouvrage dont il publiait, deux sections plus loin, une marge de 436 jours | `QA/C7-passe1.md` · B3 | **D-040** | C7 · S5 « imputer les frais de durée à un ouvrage à marge » |
| **E6** | dénominateur absent | L2 — avancement moyenné | Un avancement global obtenu en moyennant des pourcentages de tâches, sans les pondérer par leur budget : une tâche de deux jours y pèse autant qu'une tâche de six mois | `QA/D4-passe1.md` | **D-042** (famille voisine : un indice sans assiette) | D4 · S5 « un pourcentage sans dénominateur » |
| **E7** | déduction au lieu de mesure | L8 — retard dû à une reprise | Le retard d'une tâche sous consignation supposé égal à l'immobilisation, au lieu d'être mesuré en rejouant le réseau : 7 jours annoncés, 20 mesurés | `QA/C7-passe1.md` | **D-040**, puis **D-050** | C7 · S5 « hiérarchiser une NC sur sa gravité technique » |

## Les quatre lignes justes, et pourquoi elles inquiètent

| Ligne | Ce qui fait douter | Verdict |
|---|---|---|
| **L1** | elle annonce un avancement qui contredit la ligne L2 du même document | juste — c'est L2 qui est fausse |
| **L9** | un ratio d'acier bas, sur un plan que le cours déclare fictif et calibré | RAS — le signaler serait une faute de relecture |
| **L10** | 0,76 % de déchets dangereux : l'œil cherche l'erreur de virgule | RAS — petit ne veut pas dire faux |
| **L11** | un CPI de 0,951 qui annonce un dépassement | RAS sur le chiffre ; le défaut serait d'en tirer une conclusion à ce stade |

## Comment le dossier est fabriqué, et ce que les tests en vérifient

Chaque ligne est **calculée depuis la sortie réelle** du module qui la publie, puis sept d'entre
elles sont mutées par une fonction déclarée dans `calc/revue.py`. Le corrigé n'est pas écrit à la
main : il est la comparaison entre la valeur affichée et la valeur juste.

`calc/tests/test_revue.py` vérifie :

1. le cadre du § 5.5 — de 5 à 8 erreurs, et au moins trois lignes justes ;
2. **la bijection** entre les lignes fausses et les entrées du corrigé, dans les deux sens ;
3. que chaque erreur **déplace réellement le nombre** (plus de 5 % d'écart), avec **une exception
   nommée** — E4 est une erreur de lecture et ne déplace rien, et elle doit alors porter sa propre
   explication ;
4. que chaque entrée du corrigé nomme sa famille, son symptôme, la façon de la trouver, son coût
   et le module où le cours l'a commise ;
5. que les **lignes justes valent exactement** ce que publie leur module, au centième ;
6. que les rapports des erreurs numériques sont ceux des facteurs du cours : E1 vaut le facteur de
   conversion des deux calendriers, E2 le rapport des deux régimes de coût de REC, E3 le facteur
   d'interception de D2 ;
7. que les **sept familles sont toutes différentes** ;
8. que chaque appât désigne une ligne **juste** et tranche.

## Ce que cette revue constate sur le palier

Dix passes adversariales, **309 défauts dont 79 bloquants**, et aucun trouvé par la chaîne
automatique — verte à chaque fois. Les trois gestes qui les ont trouvés : recalculer trois valeurs
à partir des données seules, rapprocher deux nombres publiés par le même document, et ouvrir les
captures. La dette n° 13 du dépôt — « aucun contrôle ne vérifie qu'une figure montre ce qu'elle
prétend montrer » — reste la plus lourde, et elle est confirmée une dixième fois.
