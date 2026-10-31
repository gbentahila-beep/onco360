// Calculateurs cliniques de l'espace « Outils cliniques » (lot RT.16 et RT.17, 31/10/2026) : calculs purs, sans DOM ni Firebase.
// Chaque formule est celle de la publication d'origine (source citée dans donnees/outilscliniques.js) ; résultats indicatifs, à vérifier.
// Test : node tests/moteur/test-calculs.mjs
export const num = (v) => { if (v == null || v === "") return NaN; const n = parseFloat(String(v).replace(/[\s  ]/g, "").replace(",", ".")); return isFinite(n) ? n : NaN; };
const ok = (...v) => v.every((x) => isFinite(x));
const r1 = (x, n = 1) => Math.round(x * 10 ** n) / 10 ** n;
// Créatinine : µmol/L ↔ mg/dL (1 mg/dL = 88,4 µmol/L)
export const creatMg = (v, unite) => (unite === "mg" ? num(v) : num(v) / 88.4);
export const creatUmol = (v, unite) => (unite === "mg" ? num(v) * 88.4 : num(v));

// IMC (OMS)
export function imc(poids, taille) {
  const p = num(poids), t = num(taille) / 100; if (!ok(p, t) || p <= 0 || t <= 0) return null;
  const v = p / (t * t), c = v < 18.5 ? "Insuffisance pondérale" : v < 25 ? "Corpulence normale" : v < 30 ? "Surpoids" : v < 35 ? "Obésité (classe I)" : v < 40 ? "Obésité (classe II)" : "Obésité (classe III)";
  return { imc: r1(v), classe: c };
}
// Surface corporelle (m²) : Du Bois et Du Bois (1916) ; Mosteller (1987)
export function surface(poids, taille) {
  const p = num(poids), t = num(taille); if (!ok(p, t) || p <= 0 || t <= 0) return null;
  return { dubois: r1(0.007184 * p ** 0.425 * t ** 0.725, 2), mosteller: r1(Math.sqrt((p * t) / 3600), 2) };
}
// Cockcroft-Gault (1976), mL/min : (140 − âge) × poids / (72 × créatinine en mg/dL), × 0,85 chez la femme
export function cockcroft(age, poids, creat, unite, sexe) {
  const a = num(age), p = num(poids), c = creatMg(creat, unite); if (!ok(a, p, c) || c <= 0 || a <= 0 || p <= 0) return null;
  return r1(((140 - a) * p) / (72 * c) * (sexe === "F" ? 0.85 : 1));
}
// MDRD à 4 variables, créatinine standardisée IDMS (Levey 2006), mL/min/1,73 m² : 175 × Cr^−1,154 × âge^−0,203 × 0,742 (femme)
export function mdrd(age, creat, unite, sexe) {
  const a = num(age), c = creatMg(creat, unite); if (!ok(a, c) || c <= 0 || a <= 0) return null;
  return r1(175 * c ** -1.154 * a ** -0.203 * (sexe === "F" ? 0.742 : 1));
}
// Schwartz « au lit du malade » (2009), enfant, mL/min/1,73 m² : 0,413 × taille (cm) / créatinine (mg/dL)
export function schwartz(taille, creat, unite) {
  const t = num(taille), c = creatMg(creat, unite); if (!ok(t, c) || c <= 0 || t <= 0) return null;
  return r1((0.413 * t) / c);
}
// Carboplatine, Calvert (1989) : dose (mg) = AUC × (DFG + 25) ; plafond du DFG à 125 mL/min si demandé (règle d'Onco360)
export function calvert(auc, dfg, plafond) {
  const A = num(auc); let g = num(dfg); if (!ok(A, g) || A <= 0 || g < 0) return null;
  const plaf = plafond && g > 125; if (plaf) g = 125;
  return { dose: Math.round(A * (g + 25)), dfg: g, plafonne: !!plaf };
}
// Carboplatine, Chatelut (1995) : clairance (mL/min) = 0,134 × poids + 218 × poids × (1 − 0,00457 × âge) × (1 − 0,314 × sexe) / créatinine (µmol/L),
// sexe = 0 (homme) ou 1 (femme) ; dose = AUC × clairance
export function chatelut(auc, age, poids, creat, unite, sexe) {
  const A = num(auc), a = num(age), p = num(poids), c = creatUmol(creat, unite); if (!ok(A, a, p, c) || c <= 0 || p <= 0 || A <= 0) return null;
  const cl = 0.134 * p + (218 * p * (1 - 0.00457 * a) * (1 - 0.314 * (sexe === "F" ? 1 : 0))) / c;
  return { clairance: r1(cl), dose: Math.round(A * cl) };
}
// Calcémie corrigée par l'albumine (Payne 1973) : mmol/L et g/L : Ca + 0,02 × (40 − albumine) ; mg/dL et g/dL : Ca + 0,8 × (4 − albumine)
export function calcemie(ca, alb, unite) {
  const c = num(ca), a = num(alb); if (!ok(c, a) || c <= 0 || a <= 0) return null;
  return unite === "mg" ? r1(c + 0.8 * (4 - a), 2) : r1(c + 0.02 * (40 - a), 2);
}
// Équivalences des opioïdes (référentiels AFSOS « Douleur et cancer ») : dose de chaque forme équivalente à 1 mg de morphine orale par 24 h
// (fentanyl transdermique : µg/h ; 25 µg/h ≈ 60 mg de morphine orale par 24 h)
export const OPIOIDES = [
  ["morphine-po", "Morphine orale", "mg/24 h", 1], ["morphine-sc", "Morphine sous-cutanée", "mg/24 h", 1 / 2], ["morphine-iv", "Morphine intraveineuse", "mg/24 h", 1 / 3],
  ["oxycodone-po", "Oxycodone orale", "mg/24 h", 1 / 2], ["hydromorphone-po", "Hydromorphone orale", "mg/24 h", 1 / 7.5], ["fentanyl-td", "Fentanyl transdermique", "µg/h", 25 / 60],
  ["tramadol-po", "Tramadol oral", "mg/24 h", 5], ["codeine-po", "Codéine orale", "mg/24 h", 6],
];
export function opioides(de, dose, vers) {
  const a = OPIOIDES.find((o) => o[0] === de), b = OPIOIDES.find((o) => o[0] === vers), d = num(dose); if (!a || !b || !ok(d) || d < 0) return null;
  const morphine = d / a[3];
  return { morphine: r1(morphine), dose: r1(morphine * b[3]), unite: b[2] };
}
// Modèle linéaire-quadratique : BED = n × d × (1 + d / (α/β)) ; EQD2 = BED / (1 + 2 / (α/β)) ; dose équivalente à une autre dose par fraction :
// D2 = D × (d + α/β) / (d2 + α/β) (Withers 1983)
export function bedEqd2(d, n, ab) {
  const D = num(d), N = num(n), A = num(ab); if (!ok(D, N, A) || D <= 0 || N <= 0 || A <= 0) return null;
  const bed = N * D * (1 + D / A); return { total: r1(N * D, 2), bed: r1(bed, 1), eqd2: r1(bed / (1 + 2 / A), 1) };
}
export function conversionDose(dTot, d, d2, ab) {
  const D = num(dTot), x = num(d), y = num(d2), A = num(ab); if (!ok(D, x, y, A) || D <= 0 || x <= 0 || y <= 0 || A <= 0) return null;
  const D2 = (D * (x + A)) / (y + A); return { dose: r1(D2, 1), seances: r1(D2 / y, 1) };
}
// Temps de doublement du PSA : ln 2 / pente de la droite de régression de ln(PSA) en fonction du temps (au moins deux dosages, PSA > 0) ; en mois
export function tdPSA(points) {
  const P = (points || []).map((p) => ({ t: Date.parse(p.d), v: num(p.psa) })).filter((p) => isFinite(p.t) && p.v > 0);
  if (P.length < 2) return null;
  const x = P.map((p) => (p.t - P[0].t) / (1000 * 3600 * 24 * 30.4375)), y = P.map((p) => Math.log(p.v)), n = P.length, mx = x.reduce((s, v) => s + v, 0) / n, my = y.reduce((s, v) => s + v, 0) / n;
  const sxx = x.reduce((s, v) => s + (v - mx) ** 2, 0); if (!sxx) return null;
  const pente = x.reduce((s, v, i) => s + (v - mx) * (y[i] - my), 0) / sxx;
  return { pente: pente, td: pente > 0 ? r1(Math.LN2 / pente, 1) : null, baisse: pente <= 0, n };
}
// Groupes de risque de D'Amico (JAMA 1998) : faible = PSA ≤ 10, Gleason ≤ 6 et T1c–T2a ; intermédiaire = PSA 10–20, Gleason 7 ou T2b ; élevé = PSA > 20,
// Gleason ≥ 8 ou ≥ T2c
const T_ORDRE = ["T1a", "T1b", "T1c", "T2a", "T2b", "T2c", "T3a", "T3b", "T4"];
export function damico(psa, gleason, t) {
  const p = num(psa), g = num(gleason), k = T_ORDRE.indexOf(t); if (!ok(p, g) || k < 0) return null;
  if (p > 20 || g >= 8 || k >= T_ORDRE.indexOf("T2c")) return "Risque élevé";
  if (p > 10 || g === 7 || t === "T2b") return "Risque intermédiaire";
  return "Risque faible";
}
// Formules de Roach (1994 ; Diaz 1994), en % (bornées de 0 à 100) : ganglions = 2/3 PSA + (Gleason − 6) × 10 ; extension extracapsulaire =
// 3/2 PSA + (Gleason − 3) × 10 ; vésicules séminales = PSA + (Gleason − 6) × 10
export function roach(psa, gleason) {
  const p = num(psa), g = num(gleason); if (!ok(p, g)) return null;
  const b = (v) => Math.max(0, Math.min(100, r1(v)));
  return { ganglions: b((2 / 3) * p + (g - 6) * 10), capsule: b((3 / 2) * p + (g - 3) * 10), vesicules: b(p + (g - 6) * 10) };
}
// Index pronostique de Van Nuys (USC/VNPI, Silverstein 2003) : taille, marge, classe histologique, âge (1 à 3 points chacun)
export function vanNuys(taille, marge, classe, age) {
  const t = num(taille), m = num(marge), c = num(classe), a = num(age); if (!ok(t, m, c, a) || [1, 2, 3].indexOf(c) < 0) return null;
  const s = (t <= 15 ? 1 : t <= 40 ? 2 : 3) + (m >= 10 ? 1 : m >= 1 ? 2 : 3) + c + (a > 60 ? 1 : a >= 40 ? 2 : 3);
  return { score: s, groupe: s <= 6 ? "4 à 6 : risque faible (exérèse seule discutée)" : s <= 9 ? "7 à 9 : risque intermédiaire (radiothérapie discutée)" : "10 à 12 : risque élevé (mastectomie discutée)" };
}
// IPI (Shipp, NEJM 1993) : âge > 60, LDH > normale, ECOG ≥ 2, stade III–IV, plus d'un site extraganglionnaire
export function ipi(f) {
  const s = ["age", "ldh", "ecog", "stade", "extra"].filter((k) => f && f[k]).length;
  return { score: s, groupe: s <= 1 ? "Faible (0–1)" : s === 2 ? "Faible-intermédiaire (2)" : s === 3 ? "Intermédiaire-élevé (3)" : "Élevé (4–5)" };
}
// FLIPI (Solal-Céligny, Blood 2004) : âge > 60, stade III–IV, hémoglobine < 12 g/dL, LDH > normale, plus de 4 aires ganglionnaires
export function flipi(f) {
  const s = ["age", "stade", "hb", "ldh", "aires"].filter((k) => f && f[k]).length;
  return { score: s, groupe: s <= 1 ? "Faible (0–1)" : s === 2 ? "Intermédiaire (2)" : "Élevé (≥ 3)" };
}
// Child-Pugh : bilirubine, albumine, INR, ascite (1 absente, 2 minime, 3 modérée à importante), encéphalopathie (1 absente, 2 grade I–II, 3 grade III–IV)
export function childPugh(bili, uniteB, alb, uniteA, inr, ascite, enceph) {
  let b = num(bili), a = num(alb); const i = num(inr), as = num(ascite), e = num(enceph); if (!ok(b, a, i, as, e)) return null;
  if (uniteB === "mg") b *= 17.1; if (uniteA === "gdl") a *= 10;
  const s = (b < 34 ? 1 : b <= 50 ? 2 : 3) + (a > 35 ? 1 : a >= 28 ? 2 : 3) + (i < 1.7 ? 1 : i <= 2.3 ? 2 : 3) + as + e;
  return { score: s, classe: s <= 6 ? "A (5–6)" : s <= 9 ? "B (7–9)" : "C (10–15)" };
}
// Maladie de Hodgkin, stades I–II : facteurs de risque de l'EORTC (masse médiastinale > 0,35 du thorax, âge ≥ 50 ans, VS élevée, ≥ 4 aires) et du GHSG
// (masse médiastinale > 1/3, atteinte extraganglionnaire, VS élevée, ≥ 3 aires) ; VS élevée = ≥ 50 mm sans signes B, ≥ 30 mm avec signes B
export function hodgkin(f) {
  const st = f.stade, B = !!f.b, vs = num(f.vs), aires = num(f.aires), age = num(f.age);
  const vsHaute = isFinite(vs) && vs >= (B ? 30 : 50);
  const eortc = { masse: !!f.masse, age: age >= 50, vs: vsHaute, aires: aires >= 4 }, ghsg = { masse: !!f.masse, extra: !!f.extra, vs: vsHaute, aires: aires >= 3 };
  const nE = Object.values(eortc).filter(Boolean).length, nG = Object.values(ghsg).filter(Boolean).length, precoce = st === "I" || st === "II";
  const resE = !precoce ? "Stade avancé (III–IV) : hors classement favorable / défavorable" : nE ? "Défavorable (" + nE + " facteur" + (nE > 1 ? "s" : "") + ")" : "Favorable (aucun facteur)";
  let resG;
  if (!precoce) resG = "Avancé (stade III–IV)";
  else if (!nG) resG = "Précoce favorable";
  else if (st === "II" && B && (ghsg.masse || ghsg.extra)) resG = "Avancé (stade IIB avec masse médiastinale ou atteinte extraganglionnaire)";
  else resG = "Précoce défavorable (intermédiaire)";
  return { eortc: resE, ghsg: resG, facteursE: eortc, facteursG: ghsg };
}
// Classes RPA du RTOG pour le glioblastome (Curran 1993) : III à VI
export function rpaGbm(age, kps, resection, neuro, mental) {
  const a = num(age), k = num(kps); if (!ok(a, k)) return null;
  if (a < 50) return k >= 90 ? "Classe III" : "Classe IV";
  if (k >= 70) return resection && neuro ? "Classe IV" : "Classe V";
  return mental ? "Classe V" : "Classe VI";
}
// Irradiation partielle du sein : consensus ASTRO 2016 (Correa, Pract Radiat Oncol 2017) : « adaptée », « avec prudence », « non adaptée »
export function apbi(f) {
  const age = num(f.age), taille = num(f.taille), marge = f.margePos ? 0 : num(f.marge), eic = num(f.eic), ccis = !!f.ccis;
  if (!ok(age)) return null;
  const non = [], pru = [];
  if (age < 40) non.push("âge < 40 ans");
  if (f.brca) non.push("mutation BRCA1/2");
  if (isFinite(taille) && taille > 3) non.push("taille > 3 cm");
  if (f.t === "T3" || f.t === "T4") non.push("T3–T4");
  if (f.margePos) non.push("marges atteintes");
  if (f.lvsi === "etendu") non.push("emboles étendus");
  if (f.multicentrique) non.push("multicentrique");
  if (f.multifocal && isFinite(taille) && taille > 3) non.push("multifocal > 3 cm");
  if (isFinite(eic) && eic > 3) non.push("composante intracanalaire étendue > 3 cm");
  if (f.n) non.push("atteinte ganglionnaire (pN+)");
  if (f.neoadj) non.push("traitement néoadjuvant");
  if (ccis && isFinite(taille) && taille > 3) non.push("CCIS > 3 cm");
  if (isFinite(taille) && taille > 2 && taille <= 3) pru.push("taille 2,1 à 3 cm");
  if (f.t === "T2") pru.push("T2");
  if (!f.margePos && isFinite(marge) && marge < (ccis ? 3 : 2)) pru.push("marges proches (< " + (ccis ? 3 : 2) + " mm)");
  if (f.lvsi === "limite") pru.push("emboles limités ou focaux");
  if (f.re === "neg") pru.push("RE négatifs");
  if (f.histo === "lobulaire") pru.push("carcinome lobulaire infiltrant");
  if (f.multifocal && !(isFinite(taille) && taille > 3)) pru.push("multifocal (taille totale 2,1 à 3 cm)");
  if (isFinite(eic) && eic > 0 && eic <= 3) pru.push("composante intracanalaire étendue ≤ 3 cm");
  if (ccis && (f.grade === "haut" || (isFinite(taille) && taille > 2.5) || !f.depistage)) pru.push("CCIS pur sans tous les critères « adaptée » (dépisté, bas ou moyen grade, ≤ 2,5 cm, marges ≥ 3 mm)");
  if (non.length) return { avis: "Non adaptée", raisons: non };
  if (age < 50) return pru.length ? { avis: "Non adaptée", raisons: ["âge 40 à 49 ans sans tous les critères « adaptée »"].concat(pru) } : { avis: "Avec prudence", raisons: ["âge 40 à 49 ans"] };
  return pru.length ? { avis: "Avec prudence", raisons: pru } : { avis: "Adaptée", raisons: [] };
}
// Espérance de vie : table du cabinet [{ age, h, f }] (années restantes à cet âge) ; l'âge le plus proche en dessous
export function esperance(table, age, sexe) {
  const a = num(age), L = (table || []).map((l) => ({ age: num(l.age), h: num(l.h), f: num(l.f) })).filter((l) => isFinite(l.age)).sort((x, y) => x.age - y.age);
  if (!isFinite(a) || !L.length) return null;
  const l = L.filter((x) => x.age <= a).pop() || L[0], v = sexe === "F" ? l.f : l.h;
  return isFinite(v) ? { age: l.age, annees: v } : null;
}
// Stadification TNM : stade d'après la table du cabinet [{ stade, t, n, m }] ; « tout » ou vide = toute valeur ; plusieurs valeurs séparées par des virgules
export function stadeTnm(stades, t, n, m) {
  const va = (cell, v) => { const s = String(cell == null ? "" : cell).trim(); if (!s || /^tou(t|s|te)\b/i.test(s) || s === "*") return true; return s.split(/[,;/]/).map((x) => x.trim().toLowerCase()).indexOf(String(v || "").trim().toLowerCase()) >= 0; };
  return (stades || []).filter((r) => r && r.stade && va(r.t, t) && va(r.n, n) && va(r.m, m)).map((r) => r.stade);
}
