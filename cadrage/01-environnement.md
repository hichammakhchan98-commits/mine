# Étape 0 — (a) Vérification de l'environnement et des fichiers

Date : 15/10/2026 · Mode retenu par le lecteur : **B**

## 1. Fichiers annoncés : ce qui est réellement présent

| Fichier attendu (§ 5.1a) | Présent ? | Conséquence |
|---|---|---|
| Le prompt maître (`CLAUDE.md`, v4.1) | **Oui** — fourni en pièce jointe, copié à la racine | Relu à chaque séance (§ 13.3) |
| Ancienne version du cours (HTML ~8 Mo) | **Non** | Rien à reprendre : navigation, mise en page et modules de gestion sont refaits (question 10) |
| BAEL 91 mod. 99, BPEL 91 | **Non** | Modules béton armé / précontraint **⏸** |
| RPS 2000 version 2011 + catalogue communal | **Non** | Modules séisme **⏸** |
| CPS du marché, CCAG-T | **Non** | D1 et D4 traités sur la mécanique contractuelle, sans citer d'article de valeur |
| Bordereau de prix, cadences réelles | **Non** | Tous les prix et cadences restent **V3** (fourchettes, année 2026) |
| Maquette IFC, plans du projet réel | **Non** | D6 travaillera sur une maquette fabriquée pour le cours (§ 10.1 : programme fictif) |

**Conclusion imposée par le § 5.0 : `normes_disponibles = false`.** La phase « sans calculs normatifs » est
active. Elle n'est pas un choix de confort : aucun calcul de dimensionnement ou de vérification
réglementaire ne sera écrit avant que le lecteur ne dépose ses documents dans `docs/` et n'écrive
« normes disponibles ».

## 2. Outils disponibles dans le bac à sable

| Outil | État | Version |
|---|---|---|
| Système de fichiers | ✓ | conteneur cloud, `/home/user/mine` |
| Node.js | ✓ | 22.22.0 |
| npm | ✓ | 10.9.4 |
| Python | ✓ | 3.13.16 |
| Navigateur headless | ✓ | Chromium via Playwright (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`) — **ne jamais lancer `playwright install`** |
| git | ✓ | 2.43.0 (+ dépôt distant, voir § 4) |
| zip / unzip | ✓ | — |
| Sous-agents (pour la passe /devil) | ✓ | disponibles dans cette session |
| `pint` (vérification dimensionnelle, § 3.3) | **manquant** | à installer à l'Étape 1 (`pip install pint`) |

Rien ne manque de ce qu'exige le § 4.1. Les trois contraintes réelles sont ailleurs :

1. **Réseau sortant filtré.** Les requêtes HTTPS passent par un proxy et plusieurs domaines ne
   résolvent pas. La recherche web fonctionne ; la récupération directe d'une page officielle a échoué
   sur deux domaines marocains (voir § 3). Conséquence : **je ne pourrai pas toujours remonter à la
   source primaire** d'un point de vigilance. Quand ce sera le cas, je le dirai au lieu de laisser croire
   à un V0.
2. **`npm` : installation sans scripts** (§ 4.4) — `npm ci --ignore-scripts`, lockfile commité,
   versions épinglées publiées depuis plus de 14 jours, puis `npm audit`.
3. **Bac à sable vidé entre deux conversations** : c'est la définition du mode B (§ 4).

## 3. Points de vigilance : re-vérification du 15/10/2026

Le § 3.1 impose de re-vérifier tout point de plus de six mois. Les points de l'annexe A6.1 datent du
11/10/2026 — quatre jours : **repris tels quels**, sauf celui qui était marqué « non recoupé ».

**Point re-vérifié — révision du RPS 2000 et décrets de reclassement.** Résultat : *du nouveau par
rapport à l'annexe A6.1.*

| Constat | Statut | Source |
|---|---|---|
| Les décrets **2.24.766** (bâtiments, zonage de ~80 communes) et **2.24.767** (constructions en terre) ne sont pas restés à l'état de projet : ils ont été **publiés au Bulletin officiel n° 7351 du 11/11/2024** | **V2 fort** — la publication est rapportée par un éditeur juridique, pas lue sur le texte officiel. ⚠ **Le catalogue communal annexé reste à lire sur le texte lui-même avant tout calcul sismique** | LexisNexis Maroc (06/01/2025), via recherche du 15/10/2026 ; récupération directe du site **bloquée par le proxy** |
| La **révision complète** du RPS 2000 n'a toujours pas abouti : une enquête nationale auprès des professionnels a couru **jusqu'au 05/05/2026** pour la préparer | V2 | Médias24, 16/04/2026 |

Ce que cela change pour le cours : l'annexe A6.1 disait « publication au BO non confirmée ». Elle l'est
maintenant à un niveau de preuve raisonnable. Le reclassement de 2024 est donc à traiter comme **du
droit en vigueur**, et non comme un projet — ce qui confirme la consigne du § 10.1 (si la commune du cas
phare relève du reclassement, traiter les deux zonages : l'un en cas principal, l'autre en annexe
comparative). La préfecture de Marrakech en fait partie (8 communes), donc l'option de site S1 déclenche
bien ce double traitement.

Les quatre autres points (ACR–PCR, Eurocodes 2e génération, CCAG-T, décret 2-22-431) sont repris de
l'annexe A6.1 sans modification : moins de six mois, et rien dans la recherche ne les contredit.

## 4. Mode B : ce que j'applique, et une remarque

J'applique le § 12.5 B dans son intégralité :

1. **Zip de reprise à chaque fin de module** : `cours-genie-civil-<palier>-<module>.zip`, `.git` inclus,
   sans `node_modules` ni anciennes captures.
2. **Au début de chaque séance** : tu me redonnes le dernier zip → je le dézippe, je relis `CLAUDE.md`,
   `STATE.md`, `DECISIONS.md`, je lance `npm ci --ignore-scripts && npm run check`, et **je ne continue
   que si tout est vert**.
3. `STATE.md` porte une section **« Reprise »** (dernier module livré, commande de test, prochain module).
4. **Seul le zip fait foi** : aucun chiffre n'est repris de la mémoire d'une conversation précédente.
5. Tu conserves les zips successifs : ce sont tes sauvegardes.

**Remarque honnête, à toi de trancher (question 1).** Ce bac à sable a un dépôt git *distant* :
le travail est poussé sur la branche `claude/lance-etape-0-mode-b-ijn9r4` du dépôt `mine`, qui
**survit à la fermeture de la conversation**. Tu es donc, de fait, un cran au-dessus du mode B : la
branche distante est une seconde sauvegarde, et une prochaine séance peut repartir du dépôt plutôt que
du zip. Je ne change rien sans ton accord : le zip reste la pièce qui fait foi, la branche n'est qu'un
filet. Si tu préfères basculer en **mode A** (reprise depuis la branche, sans manipuler de zip), dis-le
et je le consigne dans `DECISIONS.md`.

Ce que la branche distante ne remplace pas : elle ne garantit pas que le projet *repasse au vert*. C'est
le rôle du contrôle de reprise (§ 12.1k), que j'exécute à chaque début de séance dans les deux modes.
