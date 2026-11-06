// Images des états vides (06/11/2026, demande de Dr Bentahila : « plus pro », comme les sites de santé) : scènes avec personnages sans visage,
// fond de forme libre, deux tons par couleur, couleurs d'Onco360 ; même format qu'avant (260 × 170). Lues par v2.js (ILL_VIDE, etatVide) et
// configuration.js (ILL_PARAM, accueil des Paramètres). Avant le 06/11/2026 : dessins au trait dans v2.js et configuration.js (historique Git).
const C = {
  bl: "#3563B0", blF: "#284C8C", blC: "#C9D9F2", blT: "#E4ECF8", tr: "#C9D5EA", pa: "#F1F5FB", l1: "#9AAAC4", l2: "#D5DDEB",
  ve: "#2FA37A", veF: "#238463", veC: "#E3F4EC", teal: "#4DB6AC", tealF: "#3A9A90", jau: "#F5C451", jauF: "#E0A92E", ros: "#EE8FA3", rosF: "#D9748A",
  pe1: "#F3C2A7", pe1F: "#E2A587", pe2: "#C68A6A", pe2F: "#AD7255", pe3: "#8B5A43", pe3F: "#744734", che: "#2B2733", che2: "#6A4434",
  bas: "#283D73", basF: "#1F3060", bl0: "#FFFFFF", blS: "#E3EAF5", sol: "#D7E2F3", rou: "#E5566F"
};
const FOND = ['M58 78C56 40 98 18 140 22C186 26 222 52 220 92C218 128 186 152 140 152C96 152 60 120 58 78Z',
  'M48 88C44 52 80 24 124 22C172 20 214 44 216 84C218 124 190 150 146 152C98 154 52 126 48 88Z'];
const svg = (c, v) => '<svg class="ev-ill" viewBox="0 0 260 170" aria-hidden="true"><path d="' + FOND[v || 0] + '" fill="' + C.blT + '"/>' +
  '<circle cx="' + (v ? 214 : 46) + '" cy="' + (v ? 40 : 46) + '" r="5" fill="' + C.blC + '"/><circle cx="' + (v ? 40 : 222) + '" cy="' + (v ? 120 : 128) + '" r="3.5" fill="' + C.blC + '"/>' + c + "</svg>";
const sol = (x, w) => '<ellipse cx="' + x + '" cy="152" rx="' + w + '" ry="5" fill="' + C.sol + '"/>';
const r = (x, y, w, h, rx, f, s) => '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + rx + '" fill="' + f + '"' + (s ? ' stroke="' + s + '" stroke-width="2"' : "") + "/>";
const p = (d, f, s, w) => '<path d="' + d + '" fill="' + (f || "none") + '"' + (s ? ' stroke="' + s + '" stroke-width="' + (w || 2) + '" stroke-linecap="round" stroke-linejoin="round"' : "") + "/>";
const ci = (x, y, rr, f) => '<circle cx="' + x + '" cy="' + y + '" r="' + rr + '" fill="' + f + '"/>';
const trait = (x, y, w, fort, h) => r(x, y, w, h || 4, (h || 4) / 2, fort ? C.l1 : C.l2);
const pastille = (x, y, f, ic) => ci(x, y, 17, "#fff") + ci(x, y, 13.5, f) + ({
  check: p("M" + (x - 6) + " " + y + "l4.5 4.5 8-9", null, "#fff", 3.2),
  plus: p("M" + x + " " + (y - 6) + "v12M" + (x - 6) + " " + y + "h12", null, "#fff", 3.2),
  sablier: p("M" + (x - 5.5) + " " + (y - 7) + "h11l-5.5 7zM" + (x - 5.5) + " " + (y + 7) + "h11l-5.5-7z", "#fff", "#fff", 1.5)
})[ic];
const etoile = (x, y, rr, f) => p("M" + x + " " + (y - rr) + "Q" + x + " " + y + " " + (x + rr) + " " + y + "Q" + x + " " + y + " " + x + " " + (y + rr) + "Q" + x + " " + y + " " + (x - rr) + " " + y + "Q" + x + " " + y + " " + x + " " + (y - rr) + "Z", f);
const plante = (x) => p("M" + x + " 128c-10-6-14-18-8-28c6 8 9 18 8 28z", C.teal) + p("M" + x + " 128c8-8 18-10 22-4c-6 6-14 8-22 4z", C.tealF) + p("M" + x + " 128c-2-12 2-24 10-30c3 10 0 22-10 30z", C.ve) +
  p("M" + (x - 10) + " 128h22l-3 22h-16z", C.jau) + p("M" + (x + 1) + " 128h11l-3 22h-8z", C.jauF);

// Personnage debout, sans visage ; origine = pieds, hauteur ~ 122 ; o = { peau, cheveux: court|long|chignon, haut, hautF, bas, blouse, bras: [g, d] (bas|hanche|tient|leve|devant), steth }
function perso(x, y, s, o) {
  const pe = C[o.peau] || C.pe1, peF = C[o.peau + "F"] || C.pe1F, ch = o.ch || C.che, haut = o.haut || C.bl, hautF = o.hautF || C.blF, ba = o.bas || C.bas, baF = o.basF || C.basF;
  const veste = o.blouse ? "#fff" : haut, vesteF = o.blouse ? C.blS : hautF;
  let g = "";
  if (o.cheveux === "long") g += p("M-13 -110C-15 -128 15 -129 13 -110L15 -86Q0 -82 -15 -86Z", ch);
  // jambes et chaussures
  g += r(-12, -52, 12, 50, 5, ba) + r(0, -52, 12, 50, 5, baF) + '<ellipse cx="-8" cy="-2" rx="9" ry="4" fill="' + C.che + '"/><ellipse cx="8" cy="-2" rx="9" ry="4" fill="' + C.che + '"/>';
  // bras (derrière le corps : ceux qui pendent)
  const bras = (cote, pose) => { const sx = cote === "g" ? -1 : 1, e = sx * 21;
    const d = { bas: [e + sx * 5, -70, e + sx * 3, -52], hanche: [e + sx * 9, -72, e + sx * 2, -58], tient: [e + sx * 4, -70, sx * 6, -64], leve: [e + sx * 12, -104, e + sx * 8, -124], devant: [e + sx * 2, -68, sx * 4, -70] }[pose];
    const dd = "M" + e + " -86Q" + d[0] + " " + d[1] + " " + d[2] + " " + d[3];
    return (o.blouse ? p(dd, null, C.tr, 11.5) : "") + p(dd, null, cote === "g" ? veste : vesteF, 9) + ci(d[2], d[3], 4.6, pe); };
  // cou, corps
  g += r(-5, -101, 10, 10, 3, peF);
  const corps = "M-14 -94h28a10 10 0 0 1 10 10l-3 " + (o.blouse ? 48 : 36) + "h-42l-3-" + (o.blouse ? 48 : 36) + "a10 10 0 0 1 10-10z";
  g += p(corps, veste, o.blouse ? C.tr : null, 2.5) +
    p("M0 -94h14a10 10 0 0 1 10 10l-3 " + (o.blouse ? 48 : 36) + "h-21z", vesteF);
  if (o.blouse) g += p("M-7 -94l7 14 7-14z", haut) + p("M-6 -94h12l-2 56h-8z", haut) + p("M0 -94h6l-2 56h-4z", hautF) + p("M-1 -80v42", null, C.blS, 1.4);
  else g += p("M-6 -94l6 9 6-9", null, peF, 3);
  if (o.steth) g += p("M-8 -93Q-11 -74 -3 -70M8 -93Q11 -78 6 -72", null, C.che, 1.8) + ci(-3, -69, 3, C.l1);
  g += bras("g", (o.bras || [])[0] || "bas") + bras("d", (o.bras || [])[1] || "bas");
  // tête
  g += '<ellipse cx="0" cy="-112" rx="11" ry="13" fill="' + pe + '"/>';
  g += ({ court: p("M-12 -109C-13 -124 -4 -128 2 -127C10 -126 14 -120 12 -110C8 -117 0 -118 -6 -116C-9 -115 -11 -112 -12 -109Z", ch),
    long: p("M-12 -108C-13 -124 -2 -128 4 -127C11 -125 14 -118 12 -108C9 -116 4 -119 -2 -117C-6 -115 -10 -111 -12 -108Z", ch),
    chignon: ci(9, -122, 6, ch) + p("M-12 -108C-13 -124 -2 -128 4 -127C11 -125 14 -118 12 -108C9 -116 4 -119 -2 -117C-6 -115 -10 -111 -12 -108Z", ch) })[o.cheveux || "court"];
  return '<g transform="translate(' + x + " " + y + ") scale(" + s + ')">' + g + (o.plus || "") + "</g>";
}
// presse-papiers tenu (coordonnées du personnage)
const pp = (x, y) => r(x, y, 20, 26, 3, C.jau) + r(x + 3, y + 4, 14, 19, 2, "#fff") + r(x + 6, y - 2, 8, 5, 2, C.blF) + trait(x + 5, y + 8, 10, true, 2) + trait(x + 5, y + 13, 8, false, 2) + trait(x + 5, y + 18, 9, false, 2);

export const ILL_VIDE = {
  // tableau des tâches, une médecin y ajoute une carte
  taches: svg(sol(126, 80) + r(104, 30, 120, 92, 12, C.sol) + r(100, 26, 120, 92, 12, "#fff", C.tr) + p("M112 26h96a12 12 0 0 1 12 12v6H100v-6a12 12 0 0 1 12-12z", C.bl) +
    [108, 145, 182].map((x, c) => r(x, 52, 31, 58, 6, C.pa) + trait(x + 5, 57, [14, 18, 12][c], true, 3) +
      [0, 1].slice(0, c === 2 ? 1 : 2).map((i) => r(x + 3, 66 + i * 20, 25, 16, 3, "#fff", null) + r(x + 3, 66 + i * 20, 3, 16, 1.5, [C.l1, C.jau, C.ve][c]) + trait(x + 9, 70 + i * 20, [14, 10][i], false, 3)).join("")).join("") +
    p("M196 74l2.6 2.6 5-5.6", null, C.ve, 2) + perso(70, 150, 1, { peau: "pe2", cheveux: "chignon", blouse: true, haut: C.teal, hautF: C.tealF, bras: ["bas", "leve"], steth: true }) +
    pastille(212, 122, C.ve, "plus")),
  // salle d'attente vide : horloge, chaises, plante, fenêtre
  salle: svg(r(150, 26, 50, 42, 6, "#fff", C.tr) + p("M175 26v42M150 47h50", null, C.tr) + ci(98, 46, 17, "#fff") + '<circle cx="98" cy="46" r="17" fill="none" stroke="' + C.bl + '" stroke-width="3"/>' +
    p("M98 46v-9M98 46l7 4", null, C.bl, 2.6) + ci(98, 46, 2, C.bl) + sol(128, 86) + r(56, 116, 150, 6, 3, C.l1) +
    [76, 116, 156].map((x, i) => { const f = i === 1 ? C.bl : C.blC, fF = i === 1 ? C.blF : C.l1;
      return r(x - 2, 84, 32, 30, 9, f) + r(x - 5, 108, 38, 12, 6, fF) + p("M" + (x + 2) + " 122v26M" + (x + 26) + " 122v26", null, C.l1, 3); }).join("") +
    plante(214), 1),
  // toutes les tâches faites : une médecin lève le bras devant le presse-papiers coché
  fete: svg(sol(138, 82) + r(134, 34, 76, 100, 12, C.sol) + r(130, 30, 76, 100, 12, "#fff", C.tr) + r(150, 22, 36, 16, 6, C.bl) + ci(168, 28, 2.6, "#fff") +
    [0, 1, 2, 3].map((i) => r(142, 50 + i * 18, 13, 13, 4, C.veC, "#BFE5D4") + p("M145.5 " + (56.5 + i * 18) + "l2.6 2.6 4.6-5.2", null, C.ve, 2.1) + trait(161, 54.5 + i * 18, [32, 24, 28, 20][i], !i)).join("") +
    pastille(204, 122, C.ve, "check") + perso(92, 150, 1, { peau: "pe1", cheveux: "long", ch: C.che2, blouse: true, haut: C.bl, hautF: C.blF, bras: ["leve", "hanche"], steth: true }) +
    etoile(56, 50, 7, C.jau) + etoile(70, 30, 4.5, C.bl) + etoile(226, 52, 6, C.ve) + etoile(214, 84, 4, C.ros) + etoile(48, 96, 4, C.l1), 1),
  // consultation : un médecin avec stéthoscope et dossier, bureau et écran
  consult: svg(sol(130, 88) + r(138, 52, 72, 48, 6, "#fff", C.tr) + r(144, 58, 60, 32, 3, C.blT) + trait(150, 64, 30, true, 3) + trait(150, 71, 40, false, 3) + trait(150, 78, 24, false, 3) +
    r(168, 100, 12, 11, 2, C.l1) + r(156, 110, 36, 4, 2, C.l1) + r(126, 114, 104, 8, 4, C.jau) + r(126, 118, 104, 4, 2, C.jauF) + p("M134 122v28M222 122v28", null, C.jauF, 4) +
    perso(92, 150, 1.02, { peau: "pe3", cheveux: "court", blouse: true, haut: C.bl, hautF: C.blF, bras: ["bas", "tient"], steth: true, plus: pp(-2, -76) })),
  // chimiothérapie : fauteuil de l'hôpital de jour, pied à perfusion avec poche, « + »
  chimio: svg(sol(124, 84) + p("M86 28v120M74 150h24", null, C.l1, 3) + p("M76 28h20", null, C.l1, 3) + r(72, 34, 28, 38, 9, "#fff", C.tr) +
    p("M74 54q6-4 12 0t12 0v8a8 8 0 0 1-8 8h-8a8 8 0 0 1-8-8z", C.ros) + r(80, 40, 12, 8, 2, "#fff", C.l2) + r(83, 72, 6, 10, 2, "#fff", C.l1) +
    p("M86 82c0 20 18 26 34 18", null, C.l1, 2.4) +
    p("M134 124l-6 26M184 124l6 26", null, C.l1, 4) + r(130, 50, 58, 62, 16, C.teal) + p("M159 50h13a16 16 0 0 1 16 16v46h-29z", C.tealF) +
    r(124, 98, 70, 20, 9, "#7DCCC3") + r(124, 108, 70, 16, 7, C.teal) + r(114, 80, 20, 44, 10, C.tealF) + r(184, 80, 20, 44, 10, C.tealF) + r(114, 80, 20, 8, 4, C.teal) + r(184, 80, 20, 8, 4, C.teal) + pastille(212, 52, C.ve, "plus")),
  // radiothérapie : appareil en anneau, table, manipulatrice qui prépare la séance
  rt: svg(sol(140, 92) + r(110, 30, 96, 100, 30, C.sol) + r(106, 26, 96, 100, 30, "#fff", C.tr) + ci(154, 76, 31, C.blT) + '<circle cx="154" cy="76" r="31" fill="none" stroke="' + C.bl + '" stroke-width="8"/>' +
    p("M154 50v52M128 76h52", null, C.ve, 1.4) + ci(154, 76, 3.5, C.ve) + r(142, 32, 24, 5, 2.5, C.blC) +
    r(120, 88, 116, 9, 4.5, "#fff", C.l1) + r(196, 97, 16, 44, 3, C.tr) + r(184, 140, 40, 8, 4, C.l1) +
    perso(78, 150, 1, { peau: "pe1", cheveux: "chignon", haut: C.teal, hautF: C.tealF, bas: C.teal, basF: C.tealF, bras: ["bas", "devant"], plus: r(-2, -80, 16, 22, 2, C.che) + r(0, -78, 12, 15, 1.5, C.blC) })),
  // agenda vide : grand calendrier, une secrétaire, une tasse
  agenda: svg(cal(false) + perso(64, 150, 0.98, { peau: "pe2", cheveux: "long", haut: C.ros, hautF: C.rosF, bras: ["bas", "devant"] })),
  agendaOk: svg(cal(true) + perso(64, 150, 0.98, { peau: "pe1", cheveux: "court", ch: C.che2, blouse: true, haut: C.bl, hautF: C.blF, bras: ["hanche", "leve"], steth: true }) + etoile(42, 60, 5, C.jau) + etoile(36, 92, 3.5, C.ve)),
  // aucune notification : cloche au repos, pastille cochée, médecin avec sa tasse
  notif: svg(sol(146, 80) + ci(160, 46, 6, C.jauF) + p("M132 112c6-6 9-15 9-32c0-17 8-30 19-30s19 13 19 30c0 17 3 26 9 32z", C.jau) + p("M160 50c11 0 19 13 19 30c0 17 3 26 9 32h-28z", C.jauF) +
    r(126, 108, 68, 10, 5, C.jauF) + ci(160, 126, 8, C.jauF) + p("M146 70q2-10 9-14", null, "#FBE3A6", 3) + pastille(196, 116, C.ve, "check") +
    perso(82, 150, 1, { peau: "pe1", cheveux: "court", ch: C.che2, blouse: true, haut: C.teal, hautF: C.tealF, bras: ["hanche", "tient"], steth: true, plus: r(2, -72, 11, 12, 3, C.bl) + p("M13 -69q5 1 0 7", null, C.bl, 2) }), 1),
  // aucun patient vu pour l'instant : médecin qui attend, tasse à la main, fiche patient et sablier
  dossier: svg(sol(136, 86) + r(124, 44, 92, 72, 12, C.sol) + r(120, 40, 92, 72, 12, "#fff", C.tr) + ci(146, 68, 14, C.blT) + ci(146, 64, 5.5, C.l1) + p("M136 78a10 8 0 0 1 20 0z", C.l1) +
    trait(166, 58, 34, true) + trait(166, 68, 26, false) + trait(166, 78, 30, false) + r(132, 92, 68, 8, 4, C.pa) + r(132, 92, 24, 8, 4, C.blC) + pastille(210, 108, C.bl, "sablier") +
    perso(80, 150, 1, { peau: "pe3", cheveux: "chignon", blouse: true, haut: C.teal, hautF: C.tealF, bras: ["bas", "tient"], steth: true, plus: r(2, -72, 11, 12, 3, C.jau) + p("M13 -69q5 1 0 7", null, C.jau, 2) }), 1),
  // aucun patient : grand dossier avec fiche, « + », un patient
  patients: svg(sol(144, 86) + p("M112 46a8 8 0 0 1 8-8h30l10 10h56a8 8 0 0 1 8 8v80H112z", C.blC) + r(116, 62, 112, 80, 10, C.sol) + r(112, 58, 112, 80, 10, "#fff", C.tr) +
    ci(144, 92, 18, C.blT) + ci(144, 87, 7, C.bl) + p("M131 106a13 10 0 0 1 26 0z", C.bl) + trait(172, 80, 38, true) + trait(172, 90, 28, false) + trait(172, 100, 32, false) +
    pastille(224, 132, C.ve, "plus") + perso(72, 150, 1, { peau: "pe1", cheveux: "court", haut: C.jau, hautF: C.jauF, bras: ["bas", "bas"] })),
  // documents : pile de feuilles, croix médicale, nuage d'envoi
  document: svg(sol(130, 70) + r(86, 42, 72, 94, 10, C.blC, null).replace("/>", ' transform="rotate(-9 122 89)"/>') +
    p("M112 34h40l24 24v76a10 10 0 0 1-10 10h-54a10 10 0 0 1-10-10V44a10 10 0 0 1 10-10z", C.sol).replace("/>", ' transform="translate(4 5)"/>') +
    p("M112 34h40l24 24v76a10 10 0 0 1-10 10h-54a10 10 0 0 1-10-10V44a10 10 0 0 1 10-10z", "#fff", C.tr) + p("M152 34v14a10 10 0 0 0 10 10h14z", C.bl) +
    ci(132, 76, 16, "#FDECEF") + r(127.5, 66, 9, 20, 2.5, C.rou) + r(122, 71.5, 20, 9, 2.5, C.rou) + trait(114, 104, 44, true) + trait(114, 114, 36, false) + trait(114, 124, 40, false) +
    p("M182 128h26a12 12 0 0 0 0-24a16 16 0 0 0-30-4a12 12 0 0 0 4 28z", C.bl) + p("M196 124v-14M190 115l6-6 6 6", null, "#fff", 2.6) + etoile(68, 64, 6, C.jau) + etoile(80, 110, 4, C.ve)),
  // RCP : trois médecins autour de la table, écran avec une image
  rcp: svg(r(150, 10, 64, 40, 5, C.che) + r(154, 14, 56, 32, 3, C.blF) + '<ellipse cx="172" cy="30" rx="9" ry="11" fill="' + C.blC + '" opacity=".8"/><ellipse cx="192" cy="30" rx="9" ry="11" fill="' + C.blC + '" opacity=".8"/>' + ci(188, 27, 3, C.jau) + p("M182 50v6", null, C.che, 3) +
    perso(78, 160, 0.9, { peau: "pe2", cheveux: "court", blouse: true, haut: C.teal, hautF: C.tealF, bras: ["bas", "bas"] }) +
    perso(128, 156, 0.9, { peau: "pe1", cheveux: "long", ch: C.che2, blouse: true, haut: C.bl, hautF: C.blF, bras: ["bas", "tient"], steth: true, plus: pp(-2, -76) }) +
    perso(180, 160, 0.9, { peau: "pe3", cheveux: "chignon", blouse: true, haut: C.ros, hautF: C.rosF, bras: ["bas", "bas"] }) +
    sol(130, 90) + p("M48 104h164a6 6 0 0 1 6 6v6H42v-6a6 6 0 0 1 6-6z", C.bl) + r(42, 112, 176, 6, 3, C.blF) + r(54, 118, 152, 44, 4, C.blC) + r(130, 118, 76, 44, 4, "#B5C9EA") +
    r(70, 96, 28, 8, 2, "#fff", C.tr) + r(160, 96, 28, 8, 2, "#fff", C.tr))
};
function cal(ok) {
  return sol(150, 74) + r(110, 38, 108, 98, 12, C.sol) + r(106, 34, 108, 98, 12, "#fff", C.tr) + p("M118 34h84a12 12 0 0 1 12 12v14H106V46a12 12 0 0 1 12-12z", C.bl) +
    r(128, 24, 9, 20, 4.5, "#fff", C.blF) + r(183, 24, 9, 20, 4.5, "#fff", C.blF) +
    [0, 1, 2].map((rr) => [0, 1, 2, 3].map((c) => { const x = 117 + c * 23, y = 70 + rr * 19, auj = !ok && rr === 1 && c === 2, fait = ok && (rr < 1 || (rr === 1 && c < 2));
      return r(x, y, 17, 13, 3.5, auj ? "#fff" : fait ? C.veC : C.pa, auj ? C.bl : null) + (fait ? p("M" + (x + 5) + " " + (y + 6.5) + "l2.4 2.4 4.4-4.8", null, C.ve, 1.8) : ""); }).join("")).join("") +
    (ok ? pastille(212, 124, C.ve, "check") : r(196, 116, 16, 18, 4, C.jau) + p("M212 120q6 1 0 9", null, C.jau, 2.2) + p("M200 110q2-4 0-7M206 110q2-4 0-7", null, C.l1, 1.6));
}
// Paramètres (accueil) : panneau de réglages, curseurs, roue dentée, une personne qui règle
export const ILL_PARAM = svg(sol(140, 84) + r(116, 40, 104, 80, 12, C.sol) + r(112, 36, 104, 80, 12, "#fff", C.tr) +
  [0, 1, 2].map((i) => { const y = 58 + i * 20, w = [44, 26, 58][i]; return r(126, y, 76, 4, 2, C.l2) + r(126, y, w, 4, 2, [C.bl, C.teal, C.jau][i]) + ci(126 + w, y + 2, 6.5, "#fff") + '<circle cx="' + (126 + w) + '" cy="' + (y + 2) + '" r="6.5" fill="none" stroke="' + [C.bl, C.teal, C.jauF][i] + '" stroke-width="2.4"/>'; }).join("") +
  ci(212, 112, 17, "#fff") + ci(212, 112, 13.5, C.bl) + '<circle cx="212" cy="112" r="4.5" fill="none" stroke="#fff" stroke-width="2.2"/>' +
  [0, 45, 90, 135, 180, 225, 270, 315].map((d) => '<rect x="210.8" y="102.5" width="2.4" height="4" rx="1" fill="#fff" transform="rotate(' + d + ' 212 112)"/>').join("") +
  perso(80, 150, 1, { peau: "pe2", cheveux: "long", haut: C.bl, hautF: C.blF, bras: ["bas", "leve"] })).replace('class="ev-ill"', 'class="cf-acc-ill"');
