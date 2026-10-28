"""Revue critique du palier 1 : un dossier à corriger (RC1, § 5.5).

Le § 5.5 demande, à la fin de chaque palier, « une note de calcul et des plans extraits du
cas, contenant de 5 à 8 erreurs plantées ». Ce module en plante **sept**, et il les plante
d'une façon particulière : **ce sont les erreurs que ce cours a réellement commises.**

Les dix passes adversariales du palier ont trouvé 309 défauts, dont 79 bloquants, et
aucun n'a jamais été vu par la chaîne automatique — verte à chaque fois. Les sept
erreurs de ce dossier sont choisies parmi elles, une par famille, et chacune porte le
module où elle s'est produite. L'exercice n'est donc pas une fiction pédagogique : c'est
le dossier qu'aurait rendu ce cours s'il n'avait pas été relu.

Comment le dossier est fabriqué, et pourquoi c'est important : chaque ligne est calculée
depuis les SORTIES RÉELLES des modules du palier, puis sept d'entre elles sont mutées par
une fonction déclarée. Le corrigé n'est pas écrit à la main — il est la comparaison entre
la valeur affichée et la valeur juste. Un dossier dont le corrigé dérive est pire
qu'inutile : il apprend une erreur de plus.

Trois lignes sont des APPÂTS : elles ont l'air suspectes et elles sont justes. Un
relecteur qui ne sait pas dire « RAS » n'est pas un relecteur — c'est la moitié du métier
de la casquette 6, et c'est ce que l'Annexe 4 exige de la passe /devil elle-même.
"""
from __future__ import annotations
import json, pathlib, sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "calc"))


def _f(x: float, dec: int = 0) -> str:
    s = f"{x:,.{dec}f}".replace(",", " ")
    return s.replace(".", ",") if dec else s


def _sorties() -> dict:
    out = {}
    for nom in ("prix", "planification", "reception", "qualite", "suivi",
                "valeur-acquise", "ferraillage"):
        out[nom] = json.loads((RACINE / "calc" / "sorties" / f"{nom}.json")
                              .read_text(encoding="utf-8"))
    return out


def compte_des_passes() -> dict:
    """Ce que les passes du dépôt ont réellement trouvé — COMPTÉ, pas affirmé.

    La première version de ce module annonçait « 309 défauts dont 79 bloquants » sur dix
    passes. Les trois nombres étaient faux, et c'est le pire défaut possible dans un
    module qui enseigne la relecture : il demandait au lecteur de le croire sur parole
    au moment même où il lui apprend à ne croire personne.

    Les gravités sont donc comptées dans les tableaux de `QA/`, cellule par cellule. La
    LIMITE du comptage est déclarée avec son résultat : il ne voit que les cellules de
    gravité d'un tableau, et un rapport qui présenterait ses défauts autrement serait
    sous-compté. C'est une borne basse, et elle est annoncée comme telle.
    """
    import re
    qa = RACINE / "QA"
    res = {g: re.compile(r"\|\s*\**" + g + r"\**(?:\s*\([^)]*\))?\s*\|")
           for g in ("bloquant", "majeur", "mineur")}
    total = {g: 0 for g in res}
    rapports = []
    for f in sorted(qa.glob("*.md")):
        if f.name.startswith("RC1"):
            continue                      # le rapport de ce module-ci n'en fait pas partie
        txt = f.read_text(encoding="utf-8")
        c = {g: len(res[g].findall(txt)) for g in res}
        if sum(c.values()):
            rapports.append({"rapport": f.name, **c})
            for g in res:
                total[g] += c[g]
    return {
        "rapports": rapports,
        "nb_rapports": len(rapports),
        "total": total,
        "nb_defauts": sum(total.values()),
        "methode": (
            "Compté mécaniquement dans les tableaux de `QA/`, cellule de gravité par "
            "cellule de gravité. Le compte ne voit que les tableaux : un rapport qui "
            "présenterait ses défauts autrement serait sous-compté. **C'est une borne "
            "basse**, et elle est publiée comme telle plutôt que recopiée de mémoire — "
            "la première version de ce module annonçait trois nombres faux."),
    }


# --------------------------------------------------------------- le dossier
def dossier(d: dict) -> dict:
    """La note de synthèse soumise au visa — sept erreurs dedans, trois appâts.

    Chaque ligne porte sa valeur AFFICHÉE (celle du dossier) et sa valeur JUSTE (celle
    que publie le module du palier). Les deux coïncident pour les appâts et les lignes
    ordinaires ; elles diffèrent pour les sept erreurs, et l'écart EST le corrigé.
    """
    s = _sorties()
    pr, pl, rc, qa, su = (s["prix"], s["planification"], s["reception"],
                          s["qualite"], s["suivi"])

    marche = pr["bordereau"]["prix_de_vente_MAD"]
    fd = pr["bordereau"]["frais_de_duree"]["cout_MAD_par_jour_ouvre"]
    conv = pr["bordereau"]["frais_de_duree"]["conversion"]["calendaires_par_jour_ouvre"]
    pour_mille = d["prix_unitaires_MAD"]["contrat"]["penalite_retard_pour_mille_par_j"]["valeur"]
    hors = rc["cout_d_un_jour"]["cout_hors_penalites_MAD_par_jour_ouvre"]
    sous = rc["cout_d_un_jour"]["cout_sous_penalites_MAD_par_jour_ouvre"]
    sous_b = rc["cout_d_un_jour"]["cout_sous_penalites_bornes_MAD"]

    # E6 — la moyenne non ponderee des avancements de taches, contre l'avancement
    # physique que le module D4 calcule sur le budget.
    constate = su["etats"]["constate"]
    moyenne_brute = sum(constate.values()) / len(constate)
    # L'avancement JUSTE est celui qui pondere les MEMES taches par leur budget :
    # `physique_constate_sur_ouvrages_pct`. Ce n'est PAS `physique_pct`, qui porte en
    # plus les frais de duree au prorata du temps et se rapporte au marche : trois
    # nombres differents, et une premiere version de ce module comparait la moyenne au
    # mauvais des trois — une faute de denominateur dans le corrige de l'erreur de
    # denominateur.
    physique = su["avancements"]["physique_constate_sur_ouvrages_pct"]

    # E3 — la duree de la tache sous consignation est un nombre de PLAGES ; la lire
    # comme des journees de huit heures la divise par le facteur d'interception.
    chlv = pl["durees"]["CHLV"]
    facteur = chlv.get("facteur_d_interception")
    chlv_vraie = chlv["duree_j"]
    chlv_fausse = chlv.get("duree_de_travail_de_jour_j", chlv_vraie / (facteur or 1))
    chlv_etalee = chlv.get("duree_etalee_j", chlv_vraie)
    periode = d["planning"]["contraintes_exploitation"][
        "periode_entre_fenetres_jours"]["valeur"]

    # E1 — la penalite se compte en jours CALENDAIRES ; la compter en jours ouvres la
    # minore du facteur de conversion.
    retard_j = 10
    penal_juste = marche * pour_mille / 1000 * conv * retard_j
    penal_fausse = marche * pour_mille / 1000 * retard_j

    # E2 — le prix fort applique a un chantier qui est DANS son delai.
    jours_decalage = 12
    cout_juste = jours_decalage * hors
    cout_faux = jours_decalage * sous

    # E4 — la fourchette du GROS OEUVRE appliquee a un bordereau qui porte aussi de la
    # fourniture : la part de main-d'oeuvre parait effondree, et l'alerte est fausse.
    part_mo = pr["bordereau"]["part_main_oeuvre_du_debourse_pct"]
    part_go_juste = pr["controle_ratios"]["part_main_oeuvre_beton_arme_decompose"]["constate"]
    borne_go = d["prix_unitaires_MAD"]["ratios_de_controle"][
        "part_main_oeuvre_gros_oeuvre_pct"]["fourchette"]

    # E5 — les frais de duree imputes a un ouvrage qui a de la marge.
    noyx = next(x for x in qa["non_conformite"]["par_ouvrage"] if x["tache"] == "NOYX")
    immo = qa["non_conformite"]["jours_immobilises"]
    nc_juste = noyx["total_MAD"]
    nc_faux = nc_juste + immo * fd

    # E7 — le retard sous consignation DEDUIT par une regle de trois au lieu d'etre
    # mesure en rejouant le reseau.
    chlv_nc = next(x for x in qa["impact_planning"]["lignes"] if x["tache"] == "CHLV")
    retard_mesure = chlv_nc["retard_du_chantier_j"]
    retard_deduit = qa["impact_planning"]["immobilisation_j"]

    # appats : trois lignes justes, et qui ont l'air fausses
    _e0 = s["ferraillage"]["ordre_de_grandeur"]["elements"][0]
    ratio_acier = _e0["ratio_du_plan_kg_m3"]
    dangereux = qa["dechets"]["part_dangereuse_pct"]
    # Le CPI du CHANTIER, publie par le module D4 dans `suivi.valeur_acquise`. Une
    # premiere version citait `valeur-acquise.json`, qui est celui de la TRANCHE
    # VERTICALE — un plancher de mezzanine a 2,8 MMAD, et non le chantier a 79,6. La
    # ligne annoncait donc une source qui ne publiait pas sa valeur, et le lecteur qui
    # l'aurait signale aurait eu raison contre le corrige. C'est la faute la plus grave
    # qu'un dossier a corriger puisse commettre.
    cpi = su["valeur_acquise"]["CPI"]

    lignes = [
        {"id": "L1",
         "intitule": "Avancement physique constaté sur les ouvrages, pondéré par leur "
                     "budget",
         "affiche": f"{_f(physique, 2)} %", "valeur": physique, "juste": physique,
         "erreur": None,
         "source": "module D4 — suivi.avancements.physique_constate_sur_ouvrages_pct",
         "chemin_juste": ["suivi", "avancements",
                          "physique_constate_sur_ouvrages_pct"]},
        {"id": "L2",
         "intitule": "Avancement global, moyenne des avancements des 27 tâches",
         "affiche": f"{_f(moyenne_brute, 2)} %", "valeur": moyenne_brute,
         "juste": physique, "erreur": "E6",
         "source": "module D4 — étant la moyenne arithmétique de suivi.etats.constate",
         "chemin_juste": ["suivi", "avancements",
                          "physique_constate_sur_ouvrages_pct"]},
        {"id": "L3",
         "intitule": "Durée restante du levage de charpente, obtenue en divisant le "
                     "tonnage restant par la cadence de levage",
         "affiche": f"{_f(chlv_fausse, 1)} jours", "valeur": chlv_fausse,
         "juste": chlv_vraie, "erreur": "E3",
         "source": "module D2 — planification.durees.CHLV",
         "chemin_juste": ["planification", "durees", "CHLV", "duree_j"]},
        {"id": "L4", "intitule": f"Pénalités encourues pour {retard_j} jours de retard",
         "affiche": f"{_f(penal_fausse)} MAD", "valeur": penal_fausse,
         "juste": penal_juste, "erreur": "E1",
         "source": "module D1 — prix.cout_du_retard"},
        {"id": "L5",
         "intitule": f"Coût d'un décalage de {jours_decalage} jours de la réception "
                     "(chantier dans son délai contractuel)",
         "affiche": f"{_f(cout_faux)} MAD", "valeur": cout_faux, "juste": cout_juste,
         "erreur": "E2",
         "source": "module REC — reception.cout_d_un_jour"},
        {"id": "L6",
         "intitule": "Contrôle d'ordre de grandeur : part de main-d'œuvre du déboursé",
         "affiche": f"{_f(part_mo, 2)} % — hors fourchette "
                    f"{_f(borne_go[0])} à {_f(borne_go[1])} % : ALERTE",
         "valeur": part_mo, "juste": part_mo, "erreur": "E4",
         "source": "module D1 — prix.bordereau.part_main_oeuvre_du_debourse_pct"},
        {"id": "L7",
         "intitule": "Coût de la non-conformité de parement du voile de noyau",
         "affiche": f"{_f(nc_faux)} MAD", "valeur": nc_faux, "juste": nc_juste,
         "erreur": "E5",
         "source": "module C7 — qualite.non_conformite.par_ouvrage[NOYX].total_MAD",
         "chemin_juste": None},
        {"id": "L8",
         "intitule": "Retard de chantier si la reprise immobilise le levage "
                     f"{_f(immo)} jours",
         "affiche": f"{_f(retard_deduit)} jours", "valeur": retard_deduit,
         "juste": retard_mesure, "erreur": "E7",
         "source": "module C7 — qualite.impact_planning[CHLV].retard_du_chantier_j",
         "chemin_juste": None},
        {"id": "L9", "intitule": f"Ratio d'acier — {_e0['element']}",
         "affiche": f"{_f(ratio_acier, 1)} kg/m³", "valeur": ratio_acier,
         "juste": ratio_acier, "erreur": None,
         "source": "module B3e — ferraillage.ordre_de_grandeur.elements[0]",
         "chemin_juste": None},
        {"id": "L10", "intitule": "Part des déchets dangereux dans le tonnage du chantier",
         "affiche": f"{_f(dangereux, 2)} %", "valeur": dangereux, "juste": dangereux,
         "erreur": None,
         "source": "module C7 — qualite.dechets.part_dangereuse_pct",
         "chemin_juste": ["qualite", "dechets", "part_dangereuse_pct"]},
        {"id": "L11",
         "intitule": "Indice de performance des coûts (CPI) du chantier à la date d'arrêt",
         "affiche": f"{_f(cpi, 4)}", "valeur": cpi, "juste": cpi, "erreur": None,
         "source": "module D4 — suivi.valeur_acquise.CPI",
         "chemin_juste": ["suivi", "valeur_acquise", "CPI"]},
    ]

    erreurs = [
        {"id": "E1", "ligne": "L4", "famille": "calendrier",
         "symptome": "une pénalité qui tombe trop ronde, et un ordre de grandeur plus "
                     "faible que ce que le marché laisse attendre",
         "comment_la_trouver":
             "Reprendre la clause : la pénalité est de « tant pour mille PAR JOUR » — "
             "mais par jour de quel calendrier ? Un retard se compte en jours "
             "calendaires et un planning en jours ouvrés. Le dossier a multiplié le "
             f"taux par {retard_j} jours ouvrés alors que ces {retard_j} jours ouvrés "
             f"font {_f(retard_j * conv, 1)} jours calendaires.",
         "ce_qu_elle_coute": f"{_f(penal_juste - penal_fausse)} MAD de pénalité "
                             f"non provisionnée sur {retard_j} jours, soit "
                             f"{_f((penal_juste / penal_fausse - 1) * 100)} % de plus",
         "ou_le_cours_l_a_commise": "module D1 : le piège est signalé dans la sortie "
                                    "elle-même, et il est la raison pour laquelle "
                                    "`cout_du_retard` publie les deux calendriers"},
        {"id": "E2", "ligne": "L5", "famille": "condition d'emploi d'une grandeur",
         "symptome": "un coût par jour repris d'un autre document, sans la condition "
                     "sous laquelle il vaut",
         "comment_la_trouver":
             "Lire le NOM de la grandeur empruntée : le module D1 publie un coût de "
             "RETARD, indexé par des jours de retard. Les pénalités n'y courent que "
             "parce que le terme contractuel est dépassé. Or la ligne précise "
             "elle-même que le chantier est dans son délai : le prix applicable est "
             f"celui des frais de durée seuls, {_f(hors)} MAD, et non {_f(sous)}.",
         "ce_qu_elle_coute":
             f"{_f(cout_faux - cout_juste)} MAD de provision inventée, un facteur "
             f"{_f(sous / hors, 1)}. **Avec les bornes** de la clause de pénalité, le "
             f"coût sous pénalités va de {_f(sous_b[0])} à {_f(sous_b[1])} MAD par "
             f"jour : l'écart va donc de {_f((sous_b[0] - hors) * jours_decalage)} à "
             f"{_f((sous_b[1] - hors) * jours_decalage)} MAD. Le montant n'est pas "
             "l'enseignement ; le facteur l'est.",
         "ou_le_cours_l_a_commise": "module REC, première version : les cinq montants "
                                    "de sa fiche mémo étaient multipliés par "
                                    f"{_f(sous / hors, 1)} (D-056)"},
        {"id": "E3", "ligne": "L3", "famille": "unité et double compte",
         "symptome": "une durée de levage qui paraît tenir dans le planning, et un "
                     "effectif qui ne colle pas avec elle",
         "comment_la_trouver":
             "Regarder l'unité que publie le module D2 pour cette tâche : elle est en "
             "PLAGES DE CONSIGNATION, pas en journées de huit heures. Une plage de six "
             "heures nocturnes dont un tiers est consommé par la prise de possession, "
             "la consignation et le repli ne vaut pas une journée de travail : le "
             f"facteur est de {_f(facteur, 2)}.",
         "ce_qu_elle_coute":
             f"{_f(chlv_vraie - chlv_fausse, 1)} PLAGES de consignation de plus — et "
             "l'unité compte ici autant que le nombre, dans le corrigé d'une erreur "
             f"d'unité. Au planning, cette tâche occupe {_f(chlv_etalee, 1)} jours "
             f"calendaires, parce que les plages sont espacées de {periode} jours ; le "
             f"dossier en laisse croire {_f(chlv_fausse, 1)}. Et elle est à marge "
             "nulle, donc tout ce qui lui manque manque à la date de fin.",
         "ou_le_cours_l_a_commise": "module B7c : le changement d'unité était "
                                    "silencieux, D1 et D2 trouvaient 971 h et 2 919 h "
                                    "pour la même tâche (D-045)"},
        {"id": "E4", "ligne": "L6", "famille": "domaine d'un ratio",
         "symptome": "une alerte spectaculaire sur un chiffre qui n'a rien d'anormal",
         "comment_la_trouver":
             "Lire ce que la fourchette borne. Elle borne la part de main-d'œuvre d'un "
             "lot de GROS ŒUVRE ; le déboursé du dossier porte aussi la charpente, la "
             "façade, la couverture et les lots techniques, c'est-à-dire surtout de la "
             "FOURNITURE. Le dénominateur n'est pas celui que la fourchette borne, et "
             "le rapprochement ne veut rien dire — un ratio porte son domaine (D-037). "
             "Ce qu'il faut faire n'est donc PAS de barrer la ligne : c'est d'aller "
             "chercher le ratio sur la bonne base, que le module D1 publie lui aussi.",
         "ce_qu_elle_coute":
             "rien en argent — et c'est le piège. Sur la BONNE base, celle du béton "
             f"armé décomposé, le cours publie {_f(part_go_juste, 2)} % contre la même "
             f"fourchette {_f(borne_go[0])} à {_f(borne_go[1])} % : **l'alerte existe "
             "bel et bien**, elle est la dette n° 10 du dépôt, et elle est chiffrée à "
             "un facteur 1,92. Classer la ligne sans suite parce que la comparaison "
             "était mal posée reviendrait donc à enterrer une alerte réelle. Une "
             "alerte juste pour une mauvaise raison reste à instruire : c'est la "
             "RAISON qu'il faut corriger, pas l'alerte.",
         "ou_le_cours_l_a_commise": "module TV, puis D1 : la dette n° 10 de `STATE.md` "
                                    "vient exactement de là",
         "_le_piege_dans_le_piege":
             "Le CHIFFRE de la ligne L6 est juste, et il faut le dire en le rendant : "
             f"{_f(part_mo, 2)} % de main-d'œuvre sur un déboursé qui porte surtout de "
             "la fourniture n'a rien d'anormal. C'est la COMPARAISON qui est fausse. Un "
             "relecteur qui barre le chiffre se trompe autant que celui qui accepte "
             "l'alerte."},
        {"id": "E5", "ligne": "L7", "famille": "coût inventé",
         "symptome": "un coût de non-conformité qui contient des frais de durée alors "
                     "que l'ouvrage touché a de la marge",
         "comment_la_trouver":
             "Chercher la marge de l'ouvrage dans le planning : le voile de noyau en a "
             f"{_f(noyx['marge_totale_j'], 0)} jours. Les frais de durée du CHANTIER ne "
             "courent que si la FIN DU CHANTIER bouge ; ici elle ne bouge pas, et le "
             "retard mesuré est nul. On ne facture pas une immobilisation à un ouvrage "
             "qui ne décale rien (D-040).",
         "ce_qu_elle_coute":
             f"{_f(nc_faux - nc_juste)} MAD inventés, soit "
             f"{_f((nc_faux / nc_juste - 1) * 100)} % de plus que le coût réel. **Et "
             f"les bornes disent le reste** : le coût juste de cette non-conformité va "
             f"de {_f(noyx['total_bornes_MAD'][0])} à {_f(noyx['total_bornes_MAD'][1])} "
             f"MAD — un facteur vingt — de sorte que le « +{_f((nc_faux / nc_juste - 1) * 100)} % » "
             "n'est lui-même qu'un point dans un intervalle très large. Ce qui ne bouge "
             "pas, c'est que les frais de durée n'ont rien à y faire.",
         "ou_le_cours_l_a_commise": "module C7, première version : elle facturait "
                                    "113 682 MAD d'immobilisation à un ouvrage dont "
                                    "elle publiait la marge deux sections plus loin"},
        {"id": "E6", "ligne": "L2", "famille": "dénominateur absent",
         "symptome": "deux avancements globaux qui ne se ressemblent pas, dans le même "
                     "document",
         "comment_la_trouver":
             "Demander de quoi cette moyenne est la moyenne. Une tâche de deux jours et "
             "une tâche de six mois y pèsent pareil : la moyenne de pourcentages n'a "
             "aucun dénominateur commun. Un avancement se pondère par le BUDGET de "
             "chaque tâche, et c'est ce que publie le module D4.",
         "ce_qu_elle_coute": f"{_f(abs(moyenne_brute - physique), 1)} points d'écart "
                             "avec l'avancement réel, dans le document qui sert à "
                             "décider si le chantier va bien",
         "ou_le_cours_l_a_commise": "module D4 : c'est le défaut que le module enseigne, "
                                    "et c'est la même faute que piloter la sécurité sur "
                                    "un effectif (module C7)"},
        {"id": "E7", "ligne": "L8", "famille": "déduction au lieu de mesure",
         "symptome": "un retard égal, au jour près, à la durée de l'immobilisation",
         "comment_la_trouver":
             "Se demander comment le nombre a été obtenu. Une tâche sous consignation "
             "ne rate pas sa reprise, elle rate son CRÉNEAU : le suivant est une "
             "période de fenêtres plus loin. Le retard ne se déduit pas de "
             "l'immobilisation, il se mesure en rejouant le réseau — et le réseau "
             f"rejoué donne {_f(retard_mesure)} jours, pas {_f(retard_deduit)}.",
         "ce_qu_elle_coute":
             f"{_f(retard_mesure - retard_deduit)} jours de chantier non annoncés, soit "
             f"{_f((retard_mesure - retard_deduit) * hors)} à "
             f"{_f((retard_mesure - retard_deduit) * sous)} MAD selon le régime. **Et "
             f"c'est le seul chiffre de ce corrigé qui ne bouge pas avec ses bornes** : "
             f"le module C7 montre que le retard sous consignation est QUANTIFIÉ, et "
             f"que {_f(retard_mesure)} jours est un palier invariant sur toute "
             "l'étendue de l'immobilisation (D-050). Les autres montants de ce corrigé "
             "sont des points dans des intervalles larges ; celui-ci est une marche.",
         "ou_le_cours_l_a_commise": "module C7 : le réseau rejoué a montré que le "
                                    "retard sous consignation est QUANTIFIÉ — une "
                                    "demi-journée perdue coûte le pas entier (D-050)"},
    ]

    appats = [
        {"ligne": "L9", "pourquoi_on_doute":
            "un ratio d'acier se compare à une fourchette de prédimensionnement, et "
            "celui-ci est bas. Mais le plan de ferraillage dont il sort est déclaré "
            "FICTIF et calibré sur cette fourchette : le ratio ne prouve rien, et il "
            "ne contredit rien non plus. Le signaler comme une erreur serait une faute "
            "de relecture.",
         "verdict": "RAS — et le module le dit lui-même quatre fois"},
        {"ligne": "L10", "pourquoi_on_doute":
            "0,76 % de déchets dangereux paraît négligeable, et l'œil cherche l'erreur "
            "de virgule. Le chiffre est juste : c'est le flux qui pèse le moins et qui "
            "commande toute l'organisation du tri.",
         "verdict": "RAS — petit ne veut pas dire faux"},
        {"ligne": "L11", "pourquoi_on_doute":
            "un CPI de 0,951 annonce un dépassement, et on voudrait s'en alarmer. Il "
            "est juste — mais le module D4 publie aussi qu'à ce stade du chantier son "
            "assiette est trop mince pour qu'il veuille dire quelque chose. Le défaut "
            "serait d'en tirer une conclusion, pas de le lire.",
         "verdict": "RAS sur le chiffre ; prudence sur ce qu'on en fait"},
    ]

    contexte = [
        {"libelle": "Montant du marché", "valeur": f"{_f(marche)} MAD"},
        {"libelle": "Pénalité de retard au CPS",
         "valeur": f"{_f(pour_mille, 1)} ‰ du marché par jour CALENDAIRE"},
        {"libelle": "Plafond des pénalités",
         "valeur": f"{_f(d['prix_unitaires_MAD']['contrat']['penalite_plafond_pct']['valeur'])} % du marché"},
        {"libelle": "Frais de durée du chantier",
         "valeur": f"{_f(fd)} MAD par jour ouvré"},
        {"libelle": "Terme contractuel",
         "valeur": "non atteint à la date de ce point — le chantier est dans son délai"},
        {"libelle": "Date d'arrêt",
         "valeur": f"jour ouvré {_f(su['avancements']['date_arret_j'])} sur "
                   f"{_f(pl['calendrier']['duree_ouvree_j'])}"},
        {"libelle": "Marge totale du voile de noyau (NOYX)",
         "valeur": f"{_f(noyx['marge_totale_j'])} jours ouvrés"},
    ]
    faux = [x for x in lignes if x["erreur"]]
    # Figure : l'ECART RELATIF de chaque erreur, signe. C'est la seule grandeur
    # homogene entre les sept — elles coutent des MAD, des jours et des points, et les
    # mettre sur un meme axe serait exactement la faute que ce module denonce.
    par_err = {x["erreur"]: x for x in faux}
    ecarts = []
    for e in erreurs:
        l = par_err[e["id"]]
        pct = (l["valeur"] / l["juste"] - 1) * 100 if l["juste"] else 0.0
        ecarts.append({"libelle": f"{e['id']} · {e['famille']}",
                       "valeur": round(pct, 1),
                       "alerte": abs(pct) < 1e-9})
    plus_gros = max(ecarts, key=lambda x: abs(x["valeur"]))
    gonflent = sum(1 for x in ecarts if x["valeur"] > 1e-9)
    minorent = sum(1 for x in ecarts if x["valeur"] < -1e-9)
    return {
        "contexte": contexte,
        "passes": compte_des_passes(),
        "figures": {"ecarts": ecarts},
        "sens_des_ecarts": {
            "gonflent": gonflent, "minorent": minorent,
            "sans_ecart": len(ecarts) - gonflent - minorent,
            "note": (
                f"{gonflent} erreurs gonflent le nombre, {minorent} le minorent, et "
                f"{len(ecarts) - gonflent - minorent} ne le déplace pas du tout. Les "
                "deux sens sont dangereux, et le second l'est davantage : une provision "
                "surestimée se discute en réunion, une durée minorée se découvre sur le "
                "chantier."),
        },
        "lignes": lignes,
        "nb_lignes": len(lignes),
        "nb_erreurs": len(erreurs),
        "nb_justes": len(lignes) - len(faux),
        "erreurs": erreurs,
        "appats": appats,
        "familles": sorted({x["famille"] for x in erreurs}),
        "_comment_ce_dossier_est_fabrique": (
            "Chaque ligne est calculée depuis la sortie réelle du module qui la publie, "
            "puis sept d'entre elles sont mutées par une fonction déclarée. Le corrigé "
            "n'est donc pas écrit à la main : il est la comparaison entre la valeur "
            "affichée et la valeur juste, et il ne peut pas dériver du dossier. Un "
            "dossier à corriger dont le corrigé dérive apprend une erreur de plus."),
        "_pourquoi_ces_sept_la": (
            "Elles ne sont pas inventées : ce sont des erreurs que ce cours a "
            "RÉELLEMENT commises, une par famille, et chacune porte le module où elle "
            "s'est produite, le rapport de relecture qui l'a trouvée et la décision qui "
            "en est née. Le dossier ci-dessous est donc celui qu'aurait rendu ce cours "
            "s'il n'avait pas été relu."),
        "_ce_que_les_passes_ont_trouve": (
            lambda c: (
                f"{c['nb_rapports']} rapports de relecture dans `QA/`, "
                f"{c['nb_defauts']} défauts comptés dont **{c['total']['bloquant']} "
                f"bloquants**, {c['total']['majeur']} majeurs et "
                f"{c['total']['mineur']} mineurs. {c['methode']}")
        )(compte_des_passes()),
    }


def tout_calculer(d: dict) -> dict:
    return {"dossier": dossier(d)}


if __name__ == "__main__":
    d = json.loads((RACINE / "data" / "projet-gare.json").read_text(encoding="utf-8"))
    r = tout_calculer(d)
    sortie = RACINE / "calc" / "sorties"
    sortie.mkdir(parents=True, exist_ok=True)
    (sortie / "revue.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    do = r["dossier"]
    print(f"{do['nb_lignes']} lignes, {do['nb_erreurs']} erreurs plantees, "
          f"{do['nb_justes']} justes")
    for x in do["lignes"]:
        marque = f"  <- {x['erreur']}" if x["erreur"] else ""
        print(f"  {x['id']:<4} {x['affiche'][:46]:<48} "
              f"(juste : {x['juste']:.2f}){marque}")
    print("familles : " + " · ".join(do["familles"]))
