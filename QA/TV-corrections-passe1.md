# TV — journal des corrections de la passe /devil n° 1

Rapport d'origine : `QA/TV-tranche-verticale.md` (19 défauts : 4 bloquants, 9 majeurs, 6 mineurs).
Ce journal dit, défaut par défaut, ce qui a été changé et **par quoi la correction est tenue**.

## Ce que la passe a appris, au-delà des corrections

- **Deux chiffres faux étaient publiés**, et l'un renversait une conclusion d'ingénierie : un corrigé
  annonçait 7 200/(300 × 12) = 2,42 j là où la division donne 2,00, et le module recommandait de
  dédoubler le front alors que quatre ferrailleurs de plus atteignent la cible. Tous les corrigés
  chiffrés sont désormais **calculés par `calc/`** et injectés par variable.
- **Un accident de gabarit** (`{{…rives_pct::n0}}0 %` affichait « 40 % » pour 4) publiait une erreur
  d'un facteur 2,6 dans le paragraphe même qui enseigne à ne pas sous-estimer un poste. Le build
  **échoue** désormais sur un chiffre collé derrière une variable, sur une variable placée dans une
  formule, et sur un repère de rédaction laissé dans le texte (`build/tests/test-gabarit.mjs`).
- **Le moteur CPM était faux hors du domaine utilisé** (décalage négatif supérieur à la durée du
  prédécesseur : 1 pour 10, ou une durée négative) et son verdict accusait le bon algorithme.
  Corrigé, et `calc/etalonnage/cpm_cas_ferme.py` compte maintenant **9 cas**, dont les trois régimes
  qui mettaient le moteur en défaut.
- **Le canari T2** (ferraillage de dalle divisé par l'effectif des poutres, +74 % sur le planning)
  franchissait les douze contrôles. Les **quatre durées** sont maintenant recalculées à la main dans
  le test, chacune confrontée à son propre effectif ; rejoué, le canari est rouge.
- **La courbe en S contredisait le tableau de valeur acquise du même module.** Elle porte désormais un
  point à la date d'arrêt, et un test exige prévu = VP/BAC et réalisé = VA/BAC à 0,5 point près :
  l'écart vertical vaut 15,80 points contre SV = 15,75.
- **L'alarme du recoupement était du bruit** : en unités physiques, les postes géométriques sont à
  −0,63 % et −0,82 %, sous le seuil ; l'écart venait du poste d'acier, issu d'un ratio V3 à ± 44 %.
  La fiche mémo ne publie plus un seuil de 1 % sur les dirhams.
- **Le contrôle de main-d'œuvre reste ouvert, et c'est dit comme tel** : les causes invoquées sont
  chiffrées (5,21 % → 6,98 % → 9,31 %) et ne couvrent pas la fourchette de 15 à 30 % ; le module
  nomme les cadences comme suspect probable au lieu d'habiller l'écart.

**Reste à faire : relancer la passe** (§ 12.2 — « jusqu'à zéro bloquant »), en rejouant T2, T6 et les
trois réseaux CPM du § 2.1 du rapport.

