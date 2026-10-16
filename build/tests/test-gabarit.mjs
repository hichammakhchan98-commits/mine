/* Les controles de source du build doivent ATTRAPER les accidents deja publies dans ce
   depot. Un controle qu'aucun cas ne fait sonner ne prouve rien : chaque regle porte ici
   son cas qui DOIT echouer et son cas voisin qui DOIT passer. */
import { controlerAccidentsDeGabarit, controlerBlocsNormatifs } from "../md.mjs";

let echecs = 0;
const dit = (bon, nom, detail = "") => {
  if (!bon) echecs++;
  console.log(`  ${bon ? "ok   " : "ECHEC"} ${nom}${detail ? ` — ${detail}` : ""}`);
};
const attrape = (src, nom) => {
  const f = controlerAccidentsDeGabarit(src, "cas.md");
  dit(f.length > 0, nom, f.length ? f[0].cause : "RIEN ATTRAPE");
};
const laisse = (src, nom) => {
  const f = controlerAccidentsDeGabarit(src, "cas.md");
  dit(f.length === 0, nom, f.length ? `faux positif : ${f[0].cause}` : "");
};

console.log("accidents de gabarit (§ 4.3)");
// (a) l'accident B1 reellement publie : « {{…rives_pct::n0}}0 % » affichait 40 % pour 4
attrape("sous-estimer le poste de {{tranche.quantites.rives_pct::n0}}0 %", "chiffre colle derriere une variable");
laisse("sous-estimer le poste de {{tranche.quantites.rives_pct::n0}} %", "la meme phrase sans le zero litteral");
laisse("la zone 4 est coulee a 60 % et {{tranche.quantites.rives_pct::n0}} suit", "un chiffre ailleurs dans la phrase");

// (b) une variable dans une formule : KaTeX la compose au lieu de la resoudre
attrape("$$ n = \\lceil {{tranche.cycle.duree_j::n2}} / 3 \\rceil $$", "variable dans une formule en bloc");
attrape("la regle $n = {{tranche.cycle.duree_j::n2}}$ ne tient pas", "variable dans une formule en ligne");
laisse("la formule $P = 2(b-2r) + 2\\pi r$ donne {{metre.perimetre_m::n3s}} m", "formule et variable sur la meme ligne, separees");

// (c) le repere de redaction publie dans l'exercice 3 : « un pic d'effectif de X personnes »
attrape("un pic d'effectif de X personnes, voici les plannings", "repere « X » isole");
attrape("reprendre le metre (TODO) avant la situation", "repere « TODO »");
laisse("la zone X1 est coulee, et $X$ designe la portee", "un X collé a un indice ou pose en variable mathematique");
laisse("le coffrage de {{tranche.quantites.coffrage_m2::n0}} m2 est pose", "une phrase ordinaire");

console.log("\nblocs normatifs (§ 3.2)");
const nb = controlerBlocsNormatifs(":::normatif\nla contrainte vaut 25 MPa\n:::", "cas.md");
dit(nb.length > 0, "un nombre non balise dans un bloc normatif est attrape", nb[0]?.nombre ?? "RIEN");
const nb2 = controlerBlocsNormatifs(
  ":::normatif\nla contrainte vaut ⟦V2|classe de beton|25 MPa⟧\n:::", "cas.md");
dit(nb2.length === 0, "le meme nombre balise passe", nb2.length ? `faux positif ${nb2[0].nombre}` : "");

console.log(echecs ? `\n${echecs} echec(s).` : "\nControles de source : tous verts.");
process.exit(echecs ? 1 : 0);
