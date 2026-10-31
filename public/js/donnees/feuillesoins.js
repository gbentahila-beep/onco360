// Onco360 – feuilles de soins (lot 9, 31/10/2026, demande de Dr Bentahila) : formulaires officiels CNOPS (« Feuille de soins Maladie ») et CNSS
// (610-1-02), fournis le 31/10 en PDF (scans) ; fond = images documents/feuilles/*.jpg (pages du PDF à 150 / 120 ppp) ; chaque valeur est posée à sa
// place sur l'image, en pixels de l'image (x, y = milieu de la ligne ou de la case), puis rendue en % de la page : le même rendu sert à l'aperçu et à
// l'impression (A4 paysage). Calcul pur (aucun DOM, aucun Firebase) : rendreFeuille(f, V, { fond }) → HTML des pages. Test : tests/moteur/test-feuillesoins.mjs
// Champs : { p (page 0 | 1), k (valeur), t: "txt" (à gauche du point x) | "centre" | "cases" (un caractère par case, xs) | "date" (JJMMAAAA, 8 cases)
//   | "x" (croix si V[k] === si) | "rond" (entoure le mot si V[k] === si, l × h) }
export const FORMULAIRES = {
  cnops: {
    nom: "CNOPS", lib: "CNOPS — Caisse Nationale des Organismes de Prévoyance Sociale", w: 1666, h: 1194, pages: ["documents/feuilles/cnops-1.jpg", "documents/feuilles/cnops-2.jpg"],
    actes: { p: 1, max: 9, lignes: [154, 190, 227, 266, 306, 345, 384, 422, 460], d: 88, code: 194, lettre: 301, valeur: 402, m: 508 },
    cim: { p: 1, xs: [410, 450, 490], y: 500 },
    champs: [
      { p: 0, k: "tel", t: "txt", x: 1192, y: 141 },
      { p: 0, k: "assNom", t: "txt", x: 1048, y: 205 },
      { p: 0, k: "assAffil", t: "txt", x: 1052, y: 241 },
      { p: 0, k: "assImmat", t: "txt", x: 1086, y: 270 },
      { p: 0, k: "assCin", t: "txt", x: 1040, y: 298 },
      { p: 0, k: "lien", t: "x", si: "conjoint", x: 1230, y: 346 },
      { p: 0, k: "lien", t: "x", si: "enfant", x: 1372, y: 346 },
      { p: 0, k: "adresse", t: "txt", x: 975, y: 391 },
      { p: 0, k: "montant", t: "txt", x: 1084, y: 450 },
      { p: 0, k: "pieces", t: "txt", x: 1100, y: 478 },
      { p: 0, k: "malNom", t: "txt", x: 1032, y: 577 },
      { p: 0, k: "malDdn", t: "date", xs: [1182, 1203, 1231, 1251, 1280, 1300, 1320, 1340], y: 603 },
      { p: 0, k: "malCin", t: "cases", xs: [1192, 1212, 1232, 1252, 1273, 1293, 1313, 1333], y: 632 },
      { p: 0, k: "sexe", t: "x", si: "M", x: 1191, y: 662 },
      { p: 0, k: "sexe", t: "x", si: "F", x: 1358, y: 662 },
      { p: 0, k: "inpe", t: "cases", xs: [1191, 1211.5, 1232, 1252.5, 1273, 1293.5, 1313, 1332.5, 1353], y: 737 },
      { p: 0, k: "type", t: "x", si: "maladie", x: 1022, y: 810 },
      { p: 0, k: "type", t: "x", si: "maternite", x: 1022, y: 850 },
      { p: 0, k: "type", t: "x", si: "hospit", x: 1022, y: 890 },
      { p: 0, k: "type", t: "x", si: "accident", x: 1022, y: 931 },
      { p: 0, k: "pli", t: "rond", si: "oui", x: 1353, y: 800, l: 42, hh: 22 },
      { p: 0, k: "pli", t: "rond", si: "non", x: 1413, y: 800, l: 42, hh: 22 },
      { p: 0, k: "dGross", t: "date", xs: [1324, 1344, 1368, 1389, 1414, 1434, 1455, 1475], y: 831 },
      { p: 0, k: "dAccouch", t: "date", xs: [1324, 1344, 1368, 1389, 1414, 1434, 1455, 1475], y: 859 },
      { p: 0, k: "dHosp", t: "date", xs: [1324, 1344, 1368, 1389, 1414, 1434, 1455, 1475], y: 888 },
      { p: 0, k: "dAcc", t: "date", xs: [1324, 1344, 1368, 1389, 1414, 1434, 1455, 1475], y: 912 },
      { p: 0, k: "causes", t: "txt", x: 1175, y: 933 },
      { p: 0, k: "faitA", t: "txt", x: 986, y: 967 },
      { p: 0, k: "le", t: "date", xs: [1002, 1022, 1047, 1067, 1092, 1112, 1133, 1153], y: 994 },
      { p: 0, k: "faitM", t: "txt", x: 1370, y: 967 },
      { p: 0, k: "leM", t: "date", xs: [1378, 1398, 1423, 1444, 1469, 1489, 1510, 1530], y: 994 },
    ],
  },
  cnss: {
    nom: "CNSS", lib: "CNSS — Caisse Nationale de Sécurité Sociale (AMO)", w: 1720, h: 1214, pages: ["documents/feuilles/cnss-1.jpg", "documents/feuilles/cnss-2.jpg"],
    actes: { p: 1, max: 2, lignes: [221, 391], d: 236, code: 352, codeCases: [304, 336, 368, 401], lettre: 475, m: 588, inpe: { xs: [202.5, 221.5, 240.5, 259.5, 278.5, 297.5, 316.5, 335.5, 354.5], ys: [299, 466] } },
    cim: { p: 1, xs: [537, 583, 630], y: 552 },
    champs: [
      { p: 0, k: "dossier", t: "txt", x: 1050, y: 188 },
      { p: 0, k: "assNom", t: "txt", x: 1082, y: 249 },
      { p: 0, k: "assImmat", t: "cases", xs: [1132, 1155, 1178, 1200, 1223, 1246, 1269, 1292, 1314], y: 285 },
      { p: 0, k: "assCin", t: "cases", xs: [1326, 1349, 1371.5, 1394.5, 1417, 1440], y: 316 },
      { p: 0, k: "lien", t: "x", si: "conjoint", x: 1188, y: 385 },
      { p: 0, k: "lien", t: "x", si: "enfant", x: 1508, y: 385 },
      { p: 0, k: "adresse", t: "txt", x: 1034, y: 421 },
      { p: 0, k: "montant", t: "txt", x: 1290, y: 462 },
      { p: 0, k: "pieces", t: "centre", x: 1325, y: 494 },
      { p: 0, k: "malNom", t: "txt", x: 1082, y: 569 },
      { p: 0, k: "malDdn", t: "date", xs: [1315, 1337, 1374, 1395, 1432, 1454, 1475, 1497], y: 595 },
      { p: 0, k: "malCin", t: "cases", xs: [1112, 1134, 1155, 1176, 1198, 1220, 1241, 1262], y: 623 },
      { p: 0, k: "sexe", t: "x", si: "M", x: 1213, y: 658 },
      { p: 0, k: "sexe", t: "x", si: "F", x: 1369, y: 658 },
      { p: 0, k: "inpe", t: "cases", xs: [1116, 1136, 1156, 1176, 1196, 1216, 1236, 1255, 1275], y: 707 },
      { p: 0, k: "medNom", t: "txt", x: 1080, y: 752 },
      { p: 0, k: "etabNom", t: "txt", x: 1336, y: 776 },
      { p: 0, k: "type", t: "x", si: "hospit", x: 1086, y: 829 },
      { p: 0, k: "type", t: "x", si: "maternite", x: 1243, y: 829 },
      { p: 0, k: "type", t: "x", si: "accident", x: 1380, y: 829 },
      { p: 0, k: "type", t: "x", si: "maladie", x: 1542, y: 829 },
      { p: 0, k: "faitA", t: "txt", x: 1004, y: 906 },
      { p: 0, k: "le", t: "date", xs: [1045.5, 1064.5, 1097.5, 1116.5, 1149.5, 1168.5, 1188, 1207.5], y: 930 },
      { p: 0, k: "faitM", t: "txt", x: 1366, y: 906 },
      { p: 0, k: "leM", t: "date", xs: [1431.5, 1450.5, 1483.5, 1502.5, 1535.5, 1554.5, 1574, 1593.5], y: 930 },
    ],
  },
};
// Feuille proposée d'après la mutuelle du dossier : CNSS si elle est citée, sinon CNOPS
export const feuilleDe = (mut) => (/cnss|amo\s*cnss/i.test(String(mut || "")) ? "cnss" : "cnops");
export const nombre = (v) => { const t = String(v == null ? "" : v).replace(/[\s\u202f\u00a0]/g, "").replace(",", "."), x = Number(t); return t === "" || isNaN(x) ? null : x; };
export const totalActes = (actes) => Math.round((actes || []).reduce((s, a) => s + (nombre(a.m) || 0), 0) * 100) / 100;
export const montantTxt = (m) => (m == null || m === "" ? "" : Number(m).toLocaleString("fr-FR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }).replace(/[  ]/g, " "));
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const pct = (v, t) => (Math.round((v / t) * 100000) / 1000) + "%";
const dateCases = (d) => { const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(d || "")); return m ? m[3] + m[2] + m[1] : ""; };
// Un caractère par case ; plus long que les cases : écrit en entier, à partir de la 1re case
function cases(f, xs, y, v, cls) {
  const s = String(v || "").replace(/\s+/g, "");
  if (!s) return "";
  // plus de caractères que de cases (CIN de 8 caractères sur 6 cases) : répartis régulièrement sur toute la largeur des cases, en plus petit
  if (s.length > xs.length) { const pas = xs.length > 1 ? (xs[xs.length - 1] - xs[0]) / (xs.length - 1) : 14, x0 = xs[0] - pas / 2, l = pas * xs.length;
    return s.split("").map((c, i) => '<span class="fs-v fs-c fs-serre" style="left:' + pct(x0 + (i + 0.5) * (l / s.length), f.w) + ";top:" + pct(y, f.h) + '">' + esc(c) + "</span>").join(""); }
  return s.split("").map((c, i) => '<span class="fs-v fs-c' + (cls ? " " + cls : "") + '" style="left:' + pct(xs[i], f.w) + ";top:" + pct(y, f.h) + '">' + esc(c) + "</span>").join("");
}
export function rendreFeuille(k, V, o) {
  const f = FORMULAIRES[k], opt = o || {}; if (!f) return "";
  const P = f.pages.map(() => []);
  f.champs.forEach((c) => {
    const v = V[c.k], L = P[c.p];
    if (c.t === "txt" || c.t === "centre") { if (v != null && String(v) !== "") L.push('<span class="fs-v' + (c.t === "centre" ? " fs-c" : "") + '" style="left:' + pct(c.x, f.w) + ";top:" + pct(c.y, f.h) + '">' + esc(v) + "</span>"); }
    else if (c.t === "cases") L.push(cases(f, c.xs, c.y, v));
    else if (c.t === "date") L.push(cases(f, c.xs, c.y, dateCases(v)));
    else if (c.t === "x") { if (v === c.si) L.push('<span class="fs-v fs-c fs-x" style="left:' + pct(c.x, f.w) + ";top:" + pct(c.y, f.h) + '">X</span>'); }
    else if (c.t === "rond") { if (v === c.si) L.push('<span class="fs-rond" style="left:' + pct(c.x, f.w) + ";top:" + pct(c.y, f.h) + ";width:" + pct(c.l, f.w) + ";height:" + pct(c.hh, f.h) + '"></span>'); }
  });
  const A = f.actes, L2 = P[A.p];
  (V.actes || []).slice(0, A.max).forEach((a, i) => {
    const y = A.lignes[i], t = (x, s) => (s == null || String(s) === "" ? "" : '<span class="fs-v fs-c" style="left:' + pct(x, f.w) + ";top:" + pct(y, f.h) + '">' + esc(s) + "</span>");
    const d = /^(\d{4})-(\d{2})-(\d{2})$/.exec(a.d || ""), dd = d ? d[3] + "/" + d[2] + "/" + d[1] : a.d || "";
    L2.push(t(A.d, dd) + (A.codeCases && String(a.code || "").replace(/\s+/g, "").length <= A.codeCases.length ? cases(f, A.codeCases, y, a.code) : t(A.code, a.code)) + t(A.lettre, a.lettre) + (A.valeur ? t(A.valeur, a.valeur) : "") + t(A.m, montantTxt(nombre(a.m))));
    if (A.inpe && V.inpe) L2.push(cases(f, A.inpe.xs, A.inpe.ys[i], V.inpe));
  });
  if (V.cim) { const s = String(V.cim).replace(/\s+/g, ""), C = f.cim; P[C.p].push(s.length <= C.xs.length ? cases(f, C.xs, C.y, s) : '<span class="fs-v fs-c" style="left:' + pct((C.xs[0] + C.xs[C.xs.length - 1]) / 2, f.w) + ";top:" + pct(C.y, f.h) + '">' + esc(s) + "</span>"); }
  return f.pages.map((src, i) => '<div class="fs-p" data-p="' + i + '" style="aspect-ratio:' + f.w + "/" + f.h + '">' + (opt.fond === false ? "" : '<img class="fs-fond" src="' + esc((opt.base || "") + src) + '" alt="">') + P[i].join("") + "</div>").join("");
}
// Styles communs à l'aperçu et à l'impression (unités de la page : cqh = 1 % de la hauteur de la page)
export const CSS_FEUILLE = ".fs-p{position:relative;container-type:size;background:#fff;overflow:hidden;font-family:Arial,Helvetica,sans-serif;color:#0B1F6B}" +
  ".fs-fond{position:absolute;inset:0;width:100%;height:100%;display:block}" +
  ".fs-v{position:absolute;transform:translateY(-50%);font-size:1.45cqh;line-height:1;white-space:nowrap;font-weight:600}" +
  ".fs-c{transform:translate(-50%,-50%)}.fs-x{font-size:1.7cqh;font-weight:700}.fs-serre{font-size:1.2cqh}" +
  ".fs-rond{position:absolute;transform:translate(-50%,-50%);border:.22cqh solid #0B1F6B;border-radius:50%}";
