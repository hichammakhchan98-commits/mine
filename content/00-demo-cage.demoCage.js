/* Initialisation de la démonstration 3D. Aucun nombre technique n'est écrit ici :
   tout vient de window.DONNEES, embarqué au build depuis data/demo-cage.json. */
(function () {
  var D = window.DONNEES["demo-cage"];
  var b = D.bornes_curseurs;

  Civil3D.vue("#vue-cage", {
    titre: "Cage d'armatures paramétrique",
    alt: "Cage d'armatures d'un tronçon de poutre : cadres, barres longitudinales et béton translucide",
    axeCoupe: "z",
    phases: ["Coffrage", "Ferraillage", "Bétonnage", "Décoffrage"],
    outils: { coupe: true, eclate: true, phasage: true },
    legende: ["coffrage", "acierHA", "beton"],
    params: {
      L_cm:   { min: b.L_cm[0],   max: b.L_cm[1],   pas: 10, valeur: D.troncon.L_cm,       libelle: "longueur", unite: "cm" },
      esp_cm: { min: b.espacement_cm[0], max: b.espacement_cm[1], pas: 1, valeur: D.cadres.espacement_cm, libelle: "espacement des cadres", unite: "cm" },
      n_inf:  { min: b.n_inf[0],  max: b.n_inf[1],  pas: 1,  valeur: D.section.inf.n,      libelle: "barres inférieures" },
      dia_inf:{ min: b.dia_inf_mm[0], max: b.dia_inf_mm[1], pas: 1, valeur: D.section.inf.dia_mm, libelle: "diamètre inférieur", unite: "mm" }
    },
    construire: function (p) {
      return Civil3D.cage({
        b_cm: D.section.b_cm,
        h_cm: D.section.h_cm,
        L_cm: p.L_cm,
        enrobage_cm: D.section.enrobage_cm,
        inf: { n: p.n_inf, dia_mm: p.dia_inf },
        sup: { n: D.section.sup.n, dia_mm: D.section.sup.dia_mm },
        cadres: { dia_mm: D.cadres.dia_mm, espacement_cm: p.esp_cm,
                  rayon_cintrage_mm: D.conventions.rayon_cintrage_mm,
                  conventions: D.conventions }
      });
    }
  });
})();
