# D7 — Pilotage et suivi multi-sites · passe adversariale n° 1

> Relecteur hostile, indépendant de l'auteur. Les commentaires de `calc/pilotage.py`, les encarts du
> module et les chaînes narratives publiées par `calc/` ont été lus **comme des affirmations à
> vérifier**, jamais comme des preuves. Les **six captures ont été ouvertes et regardées**. La
> contre-expertise du § 0 a été faite **avant** toute lecture du module et du calcul, depuis
> `data/projet-gare.json` → `multi_sites` et les sorties héritées seules (script jeté hors dépôt).
>
> État relu : commit `0c1a219`, branche `claude/lance-etape-0-mode-b-ijn9r4`. **Aucun fichier du
> dépôt n'a été modifié pendant la passe**, et le build n'a pas été relancé.

---

## 0. Contre-expertise à l'aveugle — quatre recalculs

Faits en `python3` depuis `data/projet-gare.json` (bloc `multi_sites`) et
`calc/sorties/{suivi,reception,planification}.json`, **avant** d'ouvrir `calc/pilotage.py`,
`calc/sorties/pilotage.json` et le module.

### 0.1 La valeur acquise et le CPI du site secondaire, depuis ses lots seuls

`VA = Σ budget × avancement constaté`, `VP = Σ budget × avancement planifié`, `CR = Σ coût réel` :

```
VA = 450 000 + 1 612 000 + 384 000 + 0 + 0 = 2 446 000 MAD
VP = 450 000 + 2 210 000 +  640 000 + 0 + 0 = 3 300 000 MAD
CR = 470 000 + 2 350 000 +  450 000 + 0 + 0 = 3 270 000 MAD
CPI = 2 446 000 / 3 270 000 = 0,748 01        SPI = 2 446 000 / 3 300 000 = 0,741 21
BAC = Σ budgets = 9 500 000 MAD = le budget déclaré (cohérent)
```

| Grandeur | mon calcul | publié | écart |
|---|---:|---:|---:|
| VA du site secondaire | **2 446 000 MAD** | 2 446 000 | 0 |
| CR | **3 270 000 MAD** | 3 270 000 | 0 |
| CPI | **0,748 0** | 0,748 | 0 |
| SPI | **0,741 2** | 0,7412 | 0 |
| avancement physique | **25,75 %** | 25,7 % | arrondi |

→ **concorde.** La valeur acquise est bien **dérivée** des lots et non déclarée, et l'avancement
utilisé est le physique constaté, pas la dépense.

**Périmètre — le point que la consigne demandait de vérifier.** D4 publie sa valeur acquise « sur les
OUVRAGES seuls, hors frais de durée ». Le lot 0 du site secondaire s'appelle « Préparation et
installation » : il fallait vérifier qu'il n'introduisait pas chez le petit site ce que le grand
exclut. Vérification faite dans `calc/sorties/prix.json` → `bordereau.par_lot` : le bordereau du site
principal contient un lot **« 0 · Préparation »** (installation de chantier, grue, topo) **et un lot
séparé « 9 · Frais de durée »** ; `BAC (58 332 655) + frais (9 741 600) = 68 074 255` =
`budget_total_avec_frais_de_duree_MAD`. L'installation est donc **dans** le BAC des deux sites et les
frais de durée **hors** des deux. **Les périmètres coïncident : RAS sur ce point.** (La conséquence
se retourne contre le module ailleurs — voir B4.)

### 0.2 Le CPI consolidé et la moyenne des CPI

```
VA_tot = 19 837 792,82 + 2 446 000 = 22 283 792,82 MAD
CR_tot = 22 135 812,22 + 3 270 000 = 25 405 812,22 MAD
CPI_cons = 0,877 114     moyenne arithmétique = (0,8962 + 0,7480)/2 = 0,822 106
poids du petit site : 12,871 % du CR · 14,005 % du BAC · 10,977 % de la VA · 13,13 % de la VP
```

| Grandeur | mon calcul | publié | écart |
|---|---:|---:|---:|
| CPI consolidé | **0,877 11** | 0,8771 | 0 |
| moyenne des CPI | **0,822 11** | 0,8221 | 0 |
| écart | **5,50 pts** | 5,5 | 0 |
| poids du petit site dans le CR | **12,87 %** | 12,9 % | arrondi |

→ **concorde.** Le consolidé est bien le rapport des sommes. **Mais** le poids n'est pas unique :
12,9 % du coût réel, 14,0 % du budget, 11,0 % de la valeur acquise, 13,1 % de la valeur planifiée.
Le module publie « 7,8 » comme *le* facteur d'amortissement sans dire que ce facteur n'est l'inverse
du poids en **coût réel** que pour un mécanisme de dérive précis (voir M5).

### 0.3 Le seuil de masquage — et il dépend du mécanisme, ce que le module ne dit pas là où il compte

Le seuil de **vigilance** (0,95) est **déjà franchi** par le consolidé (0,877) : la seule question
vivante est le seuil d'**alerte** (0,85). Le module retient le bon. Mais « jusqu'où le petit site
peut-il tomber » a **deux réponses** selon ce qui dérive :

```
(A) perte de valeur acquise, CR constant :
    VA2_lim = 0,85 × 25 405 812,22 − 19 837 792,82 = 1 757 147,57 MAD
    dérive invisible = 2 446 000 − 1 757 148 = 688 852 MAD   (CPI du site : 0,537 4)
(B) surcoût, VA constante — c'est la définition de « dérive » du module (CR − VA) :
    CR2_lim = 22 283 792,82 / 0,85 − 22 135 812,22 = 4 080 414,63 MAD
    surcoût invisible = 4 080 415 − 3 270 000 = 810 415 MAD   (CPI du site : 0,599 4)
```

| Grandeur | mon calcul (A) | mon calcul (B) | publié | écart |
|---|---:|---:|---:|---:|
| CPI du site au seuil consolidé | **0,537 4** | 0,599 4 | 0,5374 | 0 / +11,5 % |
| dérive supplémentaire invisible | **688 852 MAD** | 810 415 MAD | 688 702 MAD | −150 / +17,7 % |

→ **concorde sur (A)**, à 150 MAD près — écart assumé dans un commentaire de `pilotage.py` (le CPI
limite est arrondi à 4 décimales *avant* de recalculer la dérive, pour que le lecteur qui multiplie
les deux nombres imprimés retrouve le troisième). L'intention est bonne ; elle n'est écrite nulle
part dans le module, et la formule que donne l'exercice 2 rend 688 852 (m1). **Et l'écart de fond est
ailleurs** : le texte vend ce nombre comme « il peut **perdre** 689 000 MAD de plus » (S1, S5 § 2),
c'est-à-dire le mécanisme (B), qui vaut 810 415 (M4).

### 0.4 La latence des deux rythmes, et le retard effectif du site secondaire

```
latence moyenne = période/2 + délai de remontée
  hebdomadaire : 5/2 + 4 = 6,5 j   (pire cas 9 j)
  mensuel      : 20/2 + 4 = 14,0 j (pire cas 24 j)
  écart = 7,5 j  →  7,5 × 16 240,33 = 121 802 MAD
retard effectif = ⌈22/20⌉ × 20 = 2 × 20 = 40 j ouvrés ; amplification 40/22 = 1,818
```

| Grandeur | mon calcul | publié | écart |
|---|---:|---:|---:|
| latence hebdo / mensuel | **6,5 / 14,0 j** | 6,5 / 14,0 | 0 |
| écart des deux rythmes | **7,5 j** | `ecart_des_deux_rythmes_j = 7,5` — **texte imprimé : « 8 jours »** | **M1** |
| coût de l'écart | **121 802 MAD** | 121 802 | 0 (mais ≠ 8 × 16 240 = 129 923) |
| cycles perdus / retard effectif | **2 cycles / 40 j** | 2 / 40 | 0 (mais le texte dit « un cycle », M14) |
| amplification | **1,818** | 1,82 | 0 |

→ **concorde sur les nombres calculés, pas sur les nombres imprimés.** Le champ vaut 7,5 j ; le
module imprime « 8 jours » trois fois et le multiplie par un coût qui, lui, vaut 7,5 jours.

**Vérification d'alignement non déclarée.** `retard_effectif = ⌈r/P⌉ × P` n'est exact que si la date
de besoin (j 190) **tombe sur une fenêtre**. Rien dans `data/` ne le dit : 190 est déclaré V3 par
D7, la période de 20 j vient du planning. Avec un décalage quelconque de la grille, le retard subi
est compris entre `r` et `⌈r/P⌉ × P`. L'hypothèse est juste à publier — elle n'est écrite nulle part.

---

## 1. Les dix points du § 12.2

| # | Point | Constat |
|---|---|---|
| 1 | Unités, homogénéité | **Deux défauts.** « 8 jours × 16 240 MAD/j = 121 802 MAD » est faux de 7 % (M1) ; « 254 000 MAD pour un centième de CPI » homogénéise une perte de VA et un surcoût qui ne sont pas la même grandeur (M3). Ailleurs RAS : jours ouvrés et calendaires sont distingués et convertis par le ratio 20,20 déclaré (`interfaces._la_limite_declaree`), les MAD portent leur année, la latence est en jours ouvrés comme le coût d'un jour. |
| 2 | Référentiels mélangés | **RAS.** Aucun référentiel normatif n'est invoqué. Le module est bien dans la phase § 5.0 : pas un coefficient, pas un article, pas une charge. Le ⏸ contractuel est posé au bon endroit (en-tête `meta`, fin de S1, bloc « Ce qui reste ⏸ » de la fiche mémo), et il couvre les seuils imposés, les délais de déclaration et l'ouverture d'une réclamation — exactement ce que ce module frôle. |
| 3 | Article cité sans V0/V1 | **RAS.** Quatre balises V3 (budget du second site, date de besoin j 190, retard 22 j, délai de remontée 4 j), aucune V2, aucun numéro d'article. Les seuils 0,95 / 0,85 sont présentés comme des **décisions** de direction de projet et non comme des valeurs normatives — correct. **Réserve mineure** : le seuil de 0,90 de la figure 3 n'est ni dans `data/`, ni balisé, ni décidé (m5). |
| 4 | Ordres de grandeur, ratios | **Trois défauts.** « trois fois plus gros » pour un rapport de 6,1 à 6,8 (M11) ; le coût d'un jour du **grand** site appliqué à une dérive « où qu'elle se produise » (M8) ; la courbe d'incertitude du CPI de D4, construite sur un bruit absolu de 328 000 MAD et sur la VA du grand site, lue pour un site six fois plus petit (M7). Le ratio 11 700 MAD/m² contre 12 150 du cas phare, lui, est cohérent et justifié. |
| 5 | Cohérence data / figures / montants / planning | **Quatre défauts.** Légendes de figures contre règle de calcul (B2) ; table d'interfaces à 4 lignes contre figure 6 à 6 lignes et note « 6 autres … ferment la liste » (M9) ; date de besoin après retard = 212 dans `interfaces` contre 230 dans `alerte_ferroviaire` (M15) ; `cycles_perdus = 2` contre « un cycle » dans trois textes (M14). Les grandeurs héritées, elles, sont **lues** et non recopiées : test vérifié, `sites[0]` est l'identité de `suivi.valeur_acquise` sur les six champs, la date d'arrêt est celle de D4, le coût d'un jour celui de REC, la période des fenêtres celle du planning. D-039 et D-055 tenus. |
| 6 | Grille de profondeur § 7.2 | **Un critère sous le minimum** : « l'exemple est vérifié » à 1/3 (B1, M1, M2). Détail au § 3. |
| 7 | Sécurité, conseil dangereux | **RAS.** Aucune opération physique n'est prescrite. Le seul conseil opérationnel — ne pas dépenser pour rattraper dix jours — est faux (B1), mais son risque est économique, pas humain. |
| 8 | Vérité du rendu | **Six captures ouvertes.** Figure 2 ne montre pas la décomposition dont parle sa propre légende (M13) ; figure 6 coupe cinq libellés sur six en plein mot (m2) ; figure 5 n'a pas d'unité en ordonnée, ses contremarches sont obliques et son étiquette la plus grosse (« 60,0 j ») n'est pas celle du marqueur (m3). Pas de chevauchement de texte, pas d'erreur console signalée par les tests. |
| 9 | Simplifications non signalées | **Deux.** L'alignement de la grille de fenêtres sur la date de besoin (§ 0.4), dont tout l'escalier dépend ; et le mécanisme de dérive qui sous-tend l'amortissement 7,8 et les 689 000 MAD (M4, M5). La conversion jours ouvrés / calendaires, elle, est déclarée et renvoyée en ⏸ — bien fait. |
| 10 | Télégraphie, remplissage | **RAS.** Le module écrit en phrases, chaque paragraphe porte une règle, un nombre ou une méthode. Les encarts « ce que la revue n'a pas produit » et « l'erreur de posture » ajoutent du contenu, pas du volume. Densité élevée, aucun passage de garnissage repéré. |

---

## 2. Défauts

| # | Défaut | Gravité | Preuve | Correction proposée |
|---|---|---|---|---|
| **B1** | **Le corrigé de l'exercice 4 est faux, et il contredit la figure 5 du même module.** « Rattraper dix jours le ramènerait à 18 jours de moins que le cycle suivant — c'est-à-dire **exactement rien** », puis « rattraper assez pour repasser sous un cycle **demande ici plus que dix jours** ». | **bloquant** | `figures.retard_quantise` : `x=12 → v=20`, `x=22 → v=40`. Rattraper 10 j fait passer le retard de 22 à 12, donc le retard subi de **40 à 20 jours** : un cycle entier gagné, la fenêtre précédente retrouvée. Et repasser sous un cycle demande d'aller de 22 à 20, soit **2 jours**, pas « plus que dix ». La figure 5 l'affiche à l'écran (marche à x = 21). L'erreur est reprise telle quelle dans `DECISIONS.md` **D-064** : « un conducteur de travaux qui propose de rattraper dix jours sur un retard de 22 dépense sans rien produire ». | Réécrire le corrigé : rattraper 2 j suffit à sauver un cycle (20 j), rattraper 10 j le sauve aussi ; ce qui ne sert à rien, c'est de rattraper **moins que la distance à la marche inférieure** (ici 2 j) ou de rattraper **au-delà sans atteindre la marche suivante**. Corriger D-064 dans le même mouvement, puis relire l'encart « juste avant une marche, un jour gagné en vaut 20 » — qui, lui, est juste et dit le contraire du corrigé. |
| **B2** | **Les légendes des figures 1 et 4 annoncent un seuil qui n'est pas celui qui colore les barres.** Légende : « sous le seuil de **vigilance** ». Règle appliquée : `s["CPI"] < cons["seuil_d_alerte_CPI"]`, soit 0,85. | **bloquant** | `calc/pilotage.py` l. 541 et 546. Captures `…figure1.png` et `…figure4.png` : « Gare de RER 0,748 **sous le seuil de vigilance** » en rouge, tandis que « Gare a grande vitesse 0,896 » et « Consolidé 0,877 » restent bleus — **tous deux sous 0,95**, et le module publie lui-même `niveau_atteint = "vigilance"` pour le consolidé. Par la lettre de la légende, trois barres sur quatre devraient être rouges. Dans la figure 1, le même rouge marque en plus « Moyenne des CPI (faux) » (`"alerte": True` codé en dur) : une couleur, deux significations. | Faire dire à la légende ce que la règle fait : « sous le seuil d'alerte (0,85) ». Distinguer la barre « fausse par construction » par un autre encodage (hachure, libellé) que le rouge d'alerte. `STATE.md` l. 115 annonce « deux légendes fausses de D7 trouvées à l'œil sur les captures » : elles sont **toujours dans le livrable**. |
| **B3** | **« Dans le sens qui rassure » est publié comme une loi, et l'une de ses occurrences est à l'envers.** S5 § 1 : « Moyenner des ratios. **0,822 au lieu de 0,877** : 5,5 points, dans le sens qui rassure. » Le défaut décrit consiste à afficher 0,822 — plus **alarmant** que la vérité, pas rassurant. D-063 généralise : « toujours dans le sens du plus gros site, c'est-à-dire dans le sens qui rassure ». | **bloquant** | Contre-exemple calculé : grand site CPI 0,75 (CR 22,1 MMAD), petit site 0,90 (CR 3,27 MMAD) → consolidé **0,769**, moyenne **0,825**. Le consolidé est alors **plus bas** que la moyenne : il alarme. Le sens du biais suit le signe de `(CPI_gros − CPI_petit)`, il n'est pas constant. Seul le **poids** est systématique, pas la direction. | En S1 et dans `consolidation.lecture`, écrire « ici, dans le sens qui rassure, parce que c'est le petit site qui dérive ». En S5 § 1, inverser : la moyenne de ratios donne ici un chiffre **pessimiste**, et c'est pourquoi un tableau de bord faux se discrédite. Corriger « toujours » dans D-063. |
| **B4** | **« Un cycle perdu ne dépense rien : il attend » contredit le § S3a du même module, qui facture 16 240 MAD chaque jour d'attente.** S3c : « le travail n'est pas fait, donc il n'est pas payé, **donc le coût réel ne bouge pas**, donc le CPI ne bouge pas » ; quiz 7 : « le CPI ne bouge pas d'un millième ». | **bloquant** | Le module chiffre lui-même un jour d'attente à `latence.cout_d_un_jour_MAD = 16 240,33` MAD (frais de durée, hérités de REC). Un cycle perdu = 20 jours ouvrés = **324 807 MAD** de frais de durée réellement dépensés. Portés au coût réel du site, ils feraient tomber son CPI de 0,748 à **0,680** : **68 millièmes**, pas « pas un millième ». L'énoncé n'est littéralement vrai que dans le périmètre « ouvrages seuls » de D4 — périmètre que le module ne rappelle **à aucun** de ces trois endroits, et qu'il contredit en facturant la latence à ces mêmes frais. | Écrire la restriction : « un cycle perdu ne produit ni valeur acquise ni dépense **d'ouvrage** — le CPI, qui est mesuré sur les ouvrages seuls, ne bouge pas ; les frais de durée, eux, courent, et un cycle perdu en coûte 325 000 MAD. L'angle mort du CPI est précisément là. » L'argument du module en sort **renforcé**, pas affaibli. |
| **M1** | « **8 jours** d'écart, soit **121 802 MAD** » : les deux nombres imprimés ne se multiplient pas. | majeur | `latence.ecart_des_deux_rythmes_j = 7,5` ; 7,5 × 16 240,33 = 121 802 ✓ ; **8 × 16 240,33 = 129 923** ✗. Le « 8 » vient d'un `::n0` sur 7,5. Trois occurrences : `latence.lecture` (imprimée telle quelle), figure 2 « gagne 8 jours en moyenne », exercice 3 « Vous gagnez 8 jours … soit 122 000 MAD ». | Afficher `::n1` partout (7,5 j) — un demi-jour est parfaitement lisible, et c'est le seul affichage qui laisse le lecteur refaire la multiplication. |
| **M2** | Exercice 3 : « Le ramener de 4 à 1 jour **gagnerait autant que le changement de rythme** ». | majeur | 4 → 1 jour de remontée gagne **3 j**. Le passage mensuel → hebdomadaire gagne **7,5 j**. Rapport 2,5. La recommandation finale du module (« attaquer d'abord le délai de remontée ») repose sur cette égalité fausse. | « gagnerait 3 jours, soit 40 % de ce que gagne le changement de rythme — sans une réunion de plus », et conclure sur le coût des deux leviers, pas sur une égalité. |
| **M3** | « 254 000 MAD de dérive supplémentaire, **où qu'elle se produise**, pour faire bouger le CPI consolidé d'un centième » (S2, quiz 3). | majeur | Vrai seulement si la dérive est une **perte de valeur acquise** à coût réel constant. Avec la définition de « dérive » du module lui-même (`derive_MAD = CR − VA`, donc un surcoût), 254 058 MAD de surcoût font passer le consolidé de 0,8771 à **0,8684** : **0,87 centième**. Pour un centième plein il faut **292 993 MAD**. Le test `test_pilotage.py` vérifie `MAD_pour_un_centieme == 0,01 × CR` — il contrôle l'implémentation, pas l'énoncé. | Nommer le mécanisme : « 254 000 MAD de valeur acquise en moins, ou 293 000 MAD de coût en plus ». Les deux nombres sont instructifs, et leur écart est l'enseignement. |
| **M4** | Le seuil de masquage, calculé à **coût réel constant**, est vendu comme de l'argent perdu : « Il peut **perdre 689 000 MAD** de plus sans faire bouger le tableau de bord d'un cran » (S1 § 2), « jusqu'au jour où il l'est de 689 000 MAD d'un coup » (S5 § 2), D-063 « il peut perdre 689 000 MAD de plus ». | majeur | § 0.3 : à coût réel constant la réponse est 688 852 MAD de **valeur acquise** en moins ; en surcoût — ce que « perdre » veut dire, et ce que décrit le lot 1 (rendement inférieur à l'offre, donc plus d'heures pour le même ouvrage) — la réponse est **810 415 MAD**, soit **+17,7 %**. Le mécanisme n'est écrit qu'en S3b et dans l'exercice 2, jamais là où le nombre sert d'argument. | Publier les deux (689 000 en valeur acquise, 810 000 en surcoût) ou, à défaut, écrire « peut voir sa valeur acquise tomber de 689 000 MAD » partout où le nombre apparaît. |
| **M5** | **L'amortissement 7,8 est donné comme une loi pour toute dérive ; il n'est exact que pour un mécanisme, et l'étalonnage ne teste que celui-là.** « Un indicateur consolidé divise la dérive d'un site par le poids de ce site » + « divisée par 7,8 », sans condition. | majeur | Dérivation : à CR constant, `ΔCPI_cons = (CR_i/CR_tot)·ΔCPI_i` — exact, et c'est le seul cas que `calc/etalonnage/pilotage_cas_ferme.py` § 2 vérifie (il ne déplace que la VA). À VA constante (surcoût), la relation devient `ΔCPI_cons/CPI_cons = (CR_i/CR_tot)·ΔCPI_i/CPI_i` : **relative**, pas absolue. Mesuré : +824 000 MAD de surcoût sur le petit site font −0,1506 sur son CPI et −0,0276 sur le consolidé, soit un amortissement de **5,5**, non 7,8 (−30 %). Un étalonnage qui n'exerce que le mécanisme favorable **confirme** la loi au lieu de la chercher (D-041). | Énoncer la loi avec son domaine : « divise la dérive **de valeur acquise** d'un site par son poids en coût réel ; pour un surcoût, la division porte sur les **écarts relatifs** et vaut ici entre 5,5 et 6,6 selon l'ampleur ». Ajouter au moins un cas de surcoût à l'étalonnage. |
| **M6** | « **La moitié de la latence** est dans la remontée des données » est généralisé (titre d'encart, S5 § 4, glossaire) alors que le module publie 62 % en hebdomadaire et que c'est 29 % en mensuel. | majeur | `part_du_delai_de_remontee_dans_l_hebdo_pct = 61,5` ; en mensuel, 4 / 14,0 = **28,6 %**. Le glossaire écrit « Délai de remontée — **la moitié de la latence** », sans rythme. En mensuel — le rythme que le module recommande d'abandonner — c'est le tiers. | Rattacher la fraction à son rythme : « en hebdomadaire, 62 % ; en mensuel, 29 % — et c'est pour cela que raccourcir la remontée compte d'autant plus qu'on resserre le rythme ». |
| **M7** | **La courbe de fiabilité du CPI de D4 est lue hors de son domaine** pour dire que le site secondaire est « tout juste suffisant » à 25,7 % d'avancement. | majeur | `suivi.fiabilite_du_cpi` est construite sur `bruit_suppose_MAD = 328 000` — qui est exactement le coût mensuel des frais de durée **du site principal** — et sur la VA du site principal : à 25,6 % d'avancement, VA ≈ 14,9 MMAD, incertitude 3,35 pts. Le site secondaire a une VA de **2,45 MMAD** : le même bruit absolu y vaut environ **25 points** d'incertitude. Lire son avancement sur une abscisse construite pour un site six fois plus gros est précisément ce que D-037 interdit. | Soit recalculer la courbe pour le second site, soit écrire : « la courbe de D4 est celle du site principal ; pour un site six fois plus petit, le même bruit absolu pèse six fois plus, et 25,7 % d'avancement **ne suffisent pas** ». La conclusion s'inverse — et elle renforce le § 3 du module. |
| **M8** | **Le coût de la latence est celui du grand site, appliqué à une dérive « où qu'elle se produise ».** | majeur | `cout_d_un_jour_MAD = 16 240,33` = 9 741 600 / 599,84 j, frais de durée **du site principal** (`prix.bordereau.frais_de_duree` : encadrement, base-vie, grue, énergie). Le site secondaire, six fois plus petit, n'a **aucun** frais de durée déclaré. « 121 802 MAD de frais de durée à chaque dérive détectée » est donc le tarif du seul grand site, présenté comme celui de l'opération. | Déclarer la base : « au tarif de frais de durée du site principal ; pour le site secondaire, l'ordre de grandeur est six fois moindre ». Ou publier un coût par site. |
| **M9** | **La table des interfaces est incomplète et la note qui la ferme dit faux.** Quatre lignes S-RER affichées, puis « (**6 autres lignes** concernent le site principal, dont le besoin est déjà passé : elles ne portent plus de décision et **ferment la liste**) ». | majeur | `interfaces.lignes` compte **12** entrées : 6 pour S-RER, 6 pour S-GV. 4 + 6 = 10 ≠ 12. Les lignes S-RER « modifications de programme » (marge 86,1 j) et « dispositif de sécurité de chaque plage » (96,0 j) sont supprimées sans mention — et **la figure 6 les affiche toutes les deux**. La table et sa propre figure se contredisent à l'écran. | Afficher les 6 lignes S-RER (la table en porte déjà 4, deux de plus ne coûtent rien) et corriger la note : « 6 autres lignes concernent le site principal ». |
| **M10** | « Une demande est **en retard de −13 jours** » — deux fois. | majeur | Rendu HTML, S4 étape 6 et exercice 5 : le champ imprimé est `marge_a_la_date_d_arret_j = −13,4`. Une marge de −13 j est un retard de **+13 j**. La figure 6 écrit correctement « une marge de −13 jours » ; le texte transpose le signe sans changer le mot. | « en retard de 13 jours », ou publier un champ `retard_de_depot_j = 13,4` et l'utiliser dans les phrases qui disent « retard ». |
| **M11** | Figure 4 : « Le site principal porte la plus grosse dérive en valeur absolue, **parce qu'il est trois fois plus gros**. » | majeur | 58 332 655 / 9 500 000 = **6,14×** en budget ; 22 135 812 / 3 270 000 = **6,77×** en coût réel. « Trois fois » est le rapport des **dérives** (2 298 / 824 = 2,79), pas des tailles — et c'est justement ce que la phrase veut expliquer. Le texte de la figure 1, lui, donne les bons ordres (22,1 contre 3,3 MMAD). | « parce qu'il est six fois plus gros — et sa dérive n'est que trois fois plus grande, ce qui est déjà la réponse ». |
| **M12** | **Le premier canari de `test_pilotage.py` ne peut pas échouer pour la raison qu'il nomme.** Nom : « canari : un avancement physique **différent** du coût donne un CPI **différent de 1** ». Assertion : `abs(_faux["CPI"] - 1.0) < 1e-9`. Détail : « CPI = 1, et c'est juste ». | majeur | `calc/tests/test_pilotage.py` l. 74-79. Le cas choisi (budget 1 000, physique 60 %, coût 600) est **précisément** celui où la méthode physique et la méthode par dépense coïncident : VA = 600 = CR. Il ne distingue donc rien, et son intitulé affirme le contraire de ce qu'il vérifie. Le second canari (40 % pour 600 MAD → 0,667), lui, est bon. | Supprimer le premier canari ou le réécrire sur un cas discriminant (physique 40 %, coût 600 → la méthode par dépense donnerait 1, la bonne donne 0,667) — c'est exactement le second. Un canari qui confirme est pire qu'absent (D-041). |
| **M13** | **La figure 2 ne montre pas ce que sa légende explique.** Deux barres (6,5 et 14,0) pour un commentaire entièrement consacré à la **décomposition** demi-période / remontée et à la part de 62 %. | majeur | Capture `…figure2.png` : aucune des deux composantes n'est visible, ni empilée, ni annotée. Le lecteur ne peut vérifier aucune des quatre lignes de « ce qu'il faut voir » sur le dessin. § 8 : « un schéma qui n'apprend rien n'a pas sa place ». | Barres **empilées** (demi-période + remontée) : le segment de remontée devient visiblement identique sur les deux lignes, et les 62 % se lisent sans calcul. C'est la même donnée et toute la démonstration. |
| **M14** | `cycles_perdus = 2`, mais trois textes disent « le retard a franchi **un** cycle » et « **la** fenêtre visée est perdue ». | majeur | `alerte_ferroviaire.cycles_perdus = 2`, `retard_effectif_j = 40` = 2 × 20. Avec une grille alignée sur j 190, les fenêtres de j 190 **et** de j 210 sont manquées. `lecture`, exercice 4 et S4 étape 7 disent « un cycle ». | « a franchi **deux** cycles : les fenêtres de j 190 et de j 210 sont perdues, la première utilisable est celle de j 230 ». Le nombre 40 devient alors évident au lieu d'être à croire. |
| **M15** | **Deux dates de besoin après retard dans la même sortie** : 212 et 230. | majeur | `alerte_ferroviaire.date_de_besoin_apres_retard_j = 230` (quantisée). `interfaces.lignes[0].marge_apres_le_retard_du_site_j = 8,6` = 190 + **22** − 119,4 − 84, donc besoin à **212**, non quantisé. Tout l'encart « un retard peut sauver une interface » repose sur +8,6 j ; avec la date que le module défend par ailleurs (230), la marge serait **+26,6 j**. Le paradoxe est réel dans les deux cas, mais le module applique sa propre loi dans une section et l'oublie dans l'autre. | Quantiser la date de besoin dans `interfaces_a_date` aussi, ou écrire pourquoi non (« l'interface se prépare pour la date de besoin du travail, pas pour la fenêtre »). Dans les deux cas, le dire. |
| **m1** | L'exercice 2 donne `VA_B = s × (CR_A + CR_B) − VA_A` et annonce 688 702 MAD ; la formule rend **688 852**. | mineur | § 0.3. L'écart de 150 MAD vient d'un arrondi délibéré du CPI limite à 4 décimales dans `pilotage.py`, expliqué dans un commentaire de code que le lecteur ne voit pas. | Ajouter une ligne au corrigé : « le module publie 688 702 parce qu'il recalcule la dérive sur le CPI limite arrondi, pour que les deux nombres imprimés se multiplient ». |
| **m2** | Figure 6 : cinq libellés sur six coupés en plein mot. | mineur | Capture : « pendant les tr », « habilita », « existant », « systeme », « de chaque p ». Troncature à 34 caractères dans `figures()`. | Raccourcir les objets dans `data/` (le registre de B7c les porte), ou couper sur un mot avec une ellipse. |
| **m3** | Figure 5 : ordonnée sans unité ; contremarches obliques ; l'étiquette la plus grosse (« 60,0 j ») est le maximum de la courbe, pas le marqueur. | mineur | Capture : axe Y gradué 0 / 20 / 40 sans « j » ; les sauts à x = 21 et x = 41 sont des rampes sur un pas. | Porter « j ouvrés » en ordonnée, tracer les contremarches verticales (c'est le sujet de la figure), et mettre en avant l'étiquette du marqueur plutôt que celle du maximum. |
| **m4** | « **1 des 6** demandes d'interface encore à venir **sont** déjà en retard — la plus ancienne de 13 jours ». | mineur | `interfaces.lecture`. Accord fautif, et « la plus ancienne » pour un singleton. | « 1 des 6 demandes encore à venir est déjà en retard, de 13 jours ». |
| **m5** | Figure 3 : un troisième seuil, **0,90**, apparaît en légende sans être décidé nulle part. | mineur | `figures()` : `x["CPI"] < 0.9`, codé en dur ; `data/multi_sites.seuils_du_tableau_de_bord` ne contient que 0,95 et 0,85. Le module enseigne pourtant « un seuil par étage, **écrit avant** de lire ». | Déclarer `alerte_lot_CPI` dans `data/` à côté des deux autres — c'est l'occasion d'illustrer la règle au lieu de l'enfreindre. |
| **m6** | Figure 6 : « rangées par marge, et non par objet » ne démontre rien, parce que **toutes** les interfaces partagent la même date de besoin (j 190). | mineur | `interfaces.lignes[0..5].date_de_besoin_j = 190` partout. Le classement par marge est alors l'exact inverse du classement par délai : la figure ne peut pas faire apparaître l'ordre que la liste par objet cacherait. | Donner au second site deux ou trois dates de besoin distinctes dans `data/` : la démonstration devient réelle, pour le prix d'une ligne de données. |
| **m7** | Les bornes des deux latences se chevauchent ([4,5 ; 12,5] hebdo contre [12 ; 21,5] mensuel) sans que le module dise si la comparaison tranche encore (D-059). | mineur | `latence.lignes[*].latence_moyenne_bornes_j`. En fait **elle tranche** : le délai de remontée s'annule dans la différence, et le gain reste dans [7,5 ; 9] j sur toute la fourchette — c'est le canari du test qui le montre, pas le module. | Publier le gain **avec ses bornes** (7,5 à 9 j) et dire que le chevauchement des latences ne compromet pas la comparaison, parce que le terme commun s'élimine. C'est exactement ce que D-059 demande. |
| **m8** | « dépassement prévu … **14,7 % du budget** » sans dire de quel budget. | mineur | 9 957 610 / 67 832 655 = 14,7 % sur les **ouvrages seuls**. Rapporté au budget du grand site frais de durée compris (68,07 MMAD à lui seul), le pourcentage tombe vers 12,8 %. | « 14,7 % du budget des ouvrages ». |
| **m9** | Fiche mémo : la ligne « **Interface la plus urgente** » porte la demande déjà dépassée (−13 j), alors que `la_plus_urgente_encore_tenable` (26,4 j) existe. | mineur | Bloc `:::memo`, ligne 6 du tableau. | « Interface en retard » pour cette ligne, et ajouter « la plus urgente encore tenable : 26 j ». |
| **m10** | « Le site amortit déjà son lot d'un facteur **1,4** » : même réserve de mécanisme que M5, à l'étage du lot. | mineur | `amortissement_du_lot_par_le_site = 1,4` = 1 / 0,719 (poids du lot dans le coût du site). Exact à VA constante côté site, approché pour un surcoût. | Renvoyer à la condition énoncée en M5 plutôt que de répéter le facteur nu. |

**Total : 4 bloquants · 15 majeurs · 10 mineurs.**

---

## 3. Grille de profondeur (§ 7.2)

| Critère | Note | Justification |
|---|:--:|---|
| Le « pourquoi » est expliqué | **3** | L'amortissement n'est pas posé, il est **dérivé** : le consolidé est une moyenne pondérée par les coûts réels, donc un site pèse ce qu'il a dépensé. La récursivité d'un étage à l'autre et le produit des poids sont le meilleur passage du module. |
| Les hypothèses sont explicites | **2** | La date d'arrêt commune, la conversion ouvré/calendaire et le caractère V3 du second site sont déclarés, avec leur ⏸. Mais le **mécanisme de dérive** sous-jacent à 7,8, à 689 000 MAD et à 254 000 MAD ne l'est pas (M3, M4, M5), ni l'**alignement de la grille de fenêtres** dont dépend tout l'escalier (§ 0.4). |
| Les formules sont justifiées | **2** | ΣVA/ΣCR et demi-période + remontée sont démontrées et étalonnées. `⌈r/P⌉·P` est posée sans sa condition d'alignement, et la loi d'amortissement est énoncée sans son domaine — l'étalonnage ne teste que le cas qui l'arrange (M5). |
| L'exemple est vérifié | **1** | **Sous le minimum.** Le corrigé de l'exercice 4 est faux et contredit la figure 5 (B1) ; « 8 jours × 16 240 » ne donne pas 121 802 (M1) ; « 4 → 1 jour gagne autant que le changement de rythme » est faux d'un facteur 2,5 (M2). Trois des cinq exercices portent une erreur arithmétique ou une affirmation que les données réfutent. |
| Le piège est identifié | **3** | Moyenner des ratios, seuil unique cascadé, CPI d'un site qui démarre, réunion de plus contre remontée plus rapide, registre rangé par objet, dates d'arrêt différentes : sept pièges, chacun avec son symptôme observable. L'encart « l'erreur de posture » vaut à lui seul la section. |
| Le lien avec l'exécution est fait | **3** | La revue du 4ᵉ mois en huit gestes, la question à poser au conducteur de travaux plutôt qu'au tableau de bord, la négociation du contenu de la fenêtre avec l'exploitant : le module parle du métier, pas de l'instrument. |
| Le lien avec le coût et le délai est fait | **2** | La latence est chiffrée en MAD et le retard en cycles — c'est l'apport du module. Mais le tarif employé est celui du grand site appliqué partout (M8), et le lien coût/délai le plus fort du dossier — un cycle perdu se paie en frais de durée — est **nié** par le texte (B4). |

**Minimum de 2 partout : non atteint** (« l'exemple est vérifié » à 1). Le module ne peut pas être
livré en l'état : B1 à B4 sont à corriger, puis la passe est à relancer.

---

## 4. Ce qui est juste, et qu'il faut garder

Pour que la liste ci-dessus ne fasse pas croire à un module faible — il ne l'est pas :

- **Les grandeurs héritées sont lues, jamais recopiées.** Les six champs du site principal sont
  l'identité stricte de `suivi.valeur_acquise`, la date d'arrêt celle de D4, le coût d'un jour celui
  de REC, la période des fenêtres celle du planning. Les tests le vérifient par égalité, pas par
  valeur épinglée. D-039 et D-055 sont tenus, et le **périmètre** — le piège le plus probable d'une
  consolidation — est correct : les deux sites comptent leur installation dans leur BAC et leurs
  frais de durée hors, vérifié dans `prix.json` (§ 0.1).
- **La valeur acquise du second site est dérivée de ses lots**, avancement physique constaté par
  lot, et non déclarée en bloc. C'est la bonne façon de fabriquer une situation de site, et le
  second canari du test le protège.
- **Les montants priment sur les ratios** : la répartition 14 % du budget / 32 % du dépassement
  prévu est le vrai résultat du module, et elle est obtenue, pas annoncée.
- **La thèse centrale est vraie**, sous sa condition : un indicateur consolidé divise bien la dérive
  d'un site par son poids — exactement pour une dérive de valeur acquise, à 20-30 % près pour un
  surcoût. Ce qui manque est la condition, pas la loi (M5).
- **Le § 5.0 est respecté sans réserve** : aucune valeur normative, aucun seuil contractuel, et le ⏸
  est posé précisément là où le module frôle le marché.

---

## 5. Suite donnée (par l'auteur, le 29/10/2026)

**Les quatre bloquants sont corrigés, et trois d'entre eux changeaient un enseignement.**

**B1 — le corrigé de l'exercice 4 était faux, et l'escalier publié par le module disait déjà
l'inverse.** Vérifié : à 22 jours de retard pour une période de 20, rattraper 10 jours ramène le
retard subi de 40 à 20 — **un cycle entier de gagné** — et il suffit d'en rattraper **2** pour
descendre d'une marche. J'avais écrit « exactement rien » et « plus que dix jours ». L'exercice est
réécrit autour de la vraie arithmétique, qui est un meilleur enseignement que celle que j'avais
inventée : *deux jours rattrapés en valent vingt ; les huit suivants n'en valent aucun*. Le module
publie désormais `jours_a_rattraper_pour_gagner_un_cycle` et `effet_de_rattraper_10_j`, un cas
fermé d'étalonnage les fige, et deux tests les rejouent. D-064 est corrigé du même coup.

**B2 — une couleur, deux sens.** La règle de coloration est `CPI < seuil d'ALERTE` et les légendes
annonçaient « sous le seuil de vigilance » : par la lettre de la légende, le site principal et le
consolidé auraient dû être rouges. Les légendes sont corrigées, et elles ne portent plus de nombre
écrit à la main — la chaîne de caractères est publiée par `calc/`. Et la barre « moyenne des CPI »
ne porte plus l'alerte pour une autre raison que les autres : elle est rouge **parce qu'elle passe
sous le seuil**, ce qui donne le fait le plus parlant de la figure et que j'avais manqué — **sur ce
chantier, le calcul faux aurait déclenché une alerte que le calcul juste ne déclenche pas.**

**B3 — « toujours dans le sens qui rassure » est faux.** Le contre-exemple du relecteur tient : gros
site à 0,75 et petit à 0,90 donnent un consolidé de 0,765 sous une moyenne de 0,825. Ce qui est
vrai, et seul : **le consolidé est tiré vers le site qui a le plus dépensé.** Le sens de l'écart
dépend de quel site va mal. Le module publie la loi correcte, le contre-exemple, et la raison pour
laquelle le cas « rassurant » est le plus fréquent — un petit site reçoit moins d'encadrement — en
disant que fréquent n'est pas toujours. D-063 est corrigé.

**B4 — « un cycle perdu ne dépense rien » contredisait le § S3a du même module.** Exact. Un cycle
perdu ne produit ni valeur acquise ni dépense **d'ouvrage** — le CPI, calculé sur les ouvrages seuls
comme D4 le publie, ne bouge pas. Mais l'opération paie 20 jours de frais de durée :
**324 807 MAD**. La correction rend le résultat plus fort qu'il ne l'était : une dépense réelle
qu'aucun indicateur de performance ne montre, parce qu'elle est hors de son périmètre par
construction. Le périmètre est désormais nommé à chaque occurrence.

**Les quinze majeurs.** M1 (7,5 j imprimés « 8 »), M2 (le gain de la remontée est de 3 j, pas 7,5),
M3 et M4 (**les deux mécanismes d'une dérive** — valeur acquise en moins ou dépense en plus — sont
maintenant publiés tous les deux : 689 000 MAD contre 810 415 pour le masquage, 254 000 contre
293 000 pour le centième de CPI, avec leurs deux formes fermées étalonnées), M5 et m10
(l'amortissement est exact à coût réel constant, déclaré), M6 (« la moitié » n'est vrai qu'en
hebdomadaire : 62 % contre 29 % en mensuel, les deux publiés), M7 (la courbe de fiabilité est celle
du **grand** site : sur un site 6,1 fois plus petit elle donne une borne optimiste, dit), M8 (le
coût d'un jour est celui de l'opération, domaine déclaré), M9 (la table porte ses six lignes), M10
(« en retard de −13 jours » supprimé), M11 (6,1 et 6,8 fois, calculés), M12 (le canari disait le
contraire de son assertion : renommé pour ce qu'il montre), M13 (la légende de la figure 2 décrivait
une décomposition absente), M14 (« la première marche », et le rang de la fenêtre), M15 (**le besoin
se décale du retard EFFECTIF, pas du retard brut** — 212 et 230 ne coexistent plus).

**Les mineurs** : m1 (l'écart de 150 MAD entre la forme fermée et la valeur publiée sur le CPI
arrondi est expliqué dans l'exercice), m2 (libellés tronqués au mot), m3 (escalier ramené à
2,5 cycles), m4 (accord), m5 (**le seuil de 0,90 n'existait nulle part** : la figure des lots
utilise désormais le seuil déclaré de l'opération, et sa légende dit que c'est exactement ce que le
§ S3b déconseille), m6 (l'ordre par marge se confond ici avec l'ordre par délai, parce que chaque
site n'a qu'une date de besoin : dit), m7 (le chevauchement des bornes de latence est publié), m8
(« du budget des ouvrages des deux sites »), m9 (la fiche mémo distingue l'interface en retard de la
prochaine à déposer).

**Ce qui reste.** La grille § 7.2 notait « exemple vérifié » à 1 : les quatre bloquants et les
quinze majeurs étaient tous dans cette case. Après correction, les trois résultats qui portaient une
erreur — l'exercice du rattrapage, le sens de l'écart, le coût d'un cycle — sont chacun couverts par
un cas fermé d'étalonnage **et** un test de règle. Le module compte 97 contrôles.

**Une remarque de méthode, pour la prochaine fois.** Les quatre bloquants ont une propriété commune :
aucun n'est une erreur de calcul. Les calculs étaient justes ; ce sont les **phrases** qui étaient
fausses — une arithmétique faite de tête dans un corrigé, une légende qui nomme le mauvais seuil, une
loi énoncée plus large qu'elle n'est, un périmètre oublié. C'est la famille de défaut que ce cours
produit le plus, et aucun test ne la voit : il faut lire la phrase à côté du nombre.
