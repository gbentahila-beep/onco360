// L2 (31/10/2026) : import des patients par fichier Excel (Paramètres › Cabinet › Importer des patients, titulaire). Calculs purs, sans DOM ni
// Firebase (testés par node tests/moteur/test-importpatients.mjs) : colonnes du modèle, lecture d'une ligne, contrôles, doublons.
// Le numéro de dossier Onco360 est attribué comme d'habitude (serveur) ; le numéro du logiciel d'avant est gardé dans identite.numOrig.

// [clé, titre de la colonne du modèle, obligatoire, exemple]
export const COLONNES = [
  ["nom", "Nom", true, "EXEMPLE"], ["prenom", "Prénom", true, "Fatima"], ["ddn", "Date de naissance (JJ/MM/AAAA)", false, "15/06/1965"], ["sexe", "Sexe (F ou H)", false, "F"],
  ["cin", "CIN / passeport", false, "AB123456"], ["tel", "Téléphone", false, "0600000000"], ["tel2", "Téléphone 2", false, ""], ["email", "E-mail", false, ""],
  ["adresse", "Adresse", false, ""], ["mut", "Mutuelle", false, "CNOPS"], ["numAdh", "N° d'immatriculation / d'adhérent", false, ""], ["diag", "Diagnostic (localisation)", false, "Sein"],
  ["etab", "Établissement (code ou nom)", false, ""], ["cor", "Correspondant", false, ""], ["numOrig", "N° de dossier d'origine", false, "A-0001"],
];
export const MAX_LIGNES = 2000;
const sansAcc = (s) => String(s == null ? "" : s).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
const txt = (v, n) => String(v == null ? "" : v).replace(/\s+/g, " ").trim().slice(0, n || 200);

// Colonne du fichier → clé (titre du modèle, ou titre proche : « nom », « date de naissance », « telephone »…)
const SYN = { nom: ["nom", "nom de famille"], prenom: ["prenom"], ddn: ["date de naissance", "naissance", "ddn", "ne le"], sexe: ["sexe", "genre"], cin: ["cin", "cin passeport", "passeport", "cnie"],
  tel: ["telephone", "tel", "gsm", "portable", "telephone 1"], tel2: ["telephone 2", "tel 2", "autre telephone"], email: ["e mail", "email", "mail"], adresse: ["adresse"], mut: ["mutuelle", "assurance", "couverture"],
  numAdh: ["n d immatriculation d adherent", "immatriculation", "n d adherent", "adherent", "n immatriculation"], diag: ["diagnostic localisation", "diagnostic", "localisation"],
  etab: ["etablissement code ou nom", "etablissement", "lieu", "clinique"], cor: ["correspondant", "medecin correspondant", "medecin traitant"], numOrig: ["n de dossier d origine", "n de dossier", "dossier", "numero de dossier", "n dossier", "ancien numero"] };
export function cleColonne(titre) {
  const t = sansAcc(titre).replace(/\b(f ou h|jj mm aaaa|code ou nom)\b/g, "").trim();
  for (const [k, l] of Object.entries(SYN)) if (l.indexOf(t) >= 0) return k;
  const c = COLONNES.find((z) => sansAcc(z[1]) === sansAcc(titre)); return c ? c[0] : null;
}

// Date : JJ/MM/AAAA, JJ-MM-AAAA, AAAA-MM-JJ, nombre de jours d'Excel, objet Date → AAAA-MM-JJ ; "" si vide ; null si illisible ou impossible
export function dateIso(v, auj) {
  if (v == null || v === "") return "";
  let a, m, j;
  if (v instanceof Date && !isNaN(v)) { a = v.getFullYear(); m = v.getMonth() + 1; j = v.getDate(); }
  else if (typeof v === "number" && v > 0 && v < 80000) { const d = new Date(Date.UTC(1899, 11, 30) + Math.round(v) * 86400000); a = d.getUTCFullYear(); m = d.getUTCMonth() + 1; j = d.getUTCDate(); }
  else {
    const s = String(v).trim(); let r;
    if ((r = s.match(/^(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{4})$/))) { j = +r[1]; m = +r[2]; a = +r[3]; }
    else if ((r = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/))) { a = +r[1]; m = +r[2]; j = +r[3]; }
    else return null;
  }
  const d = new Date(Date.UTC(a, m - 1, j));
  if (d.getUTCFullYear() !== a || d.getUTCMonth() !== m - 1 || d.getUTCDate() !== j) return null;
  const iso = a + "-" + String(m).padStart(2, "0") + "-" + String(j).padStart(2, "0");
  if (a < 1900 || (auj && iso > auj)) return null;
  return iso;
}
const sexe = (v) => { const s = sansAcc(v); return !s ? "" : /^(f|femme|feminin)$/.test(s) ? "F" : /^(h|m|homme|masculin)$/.test(s) ? "H" : null; };
const tel = (v) => { const s = String(v == null ? "" : v).replace(/[^\d+]/g, ""); return s.length >= 9 && s.length <= 15 ? (s.length === 9 && /^[5-7]/.test(s) ? "0" + s : s) : s ? null : ""; };

// Une ligne lue (objet { clé: valeur }) → { identite, clinique, etab, erreurs [texte], avert [texte] }
// ctx : { auj: "AAAA-MM-JJ", etabs: [{ code, nom }], etabDefaut, diags: [noms de la liste], mut: [noms] }
export function lireLigne(o, ctx) {
  const c = ctx || {}, erreurs = [], avert = [], I = {}, C = {};
  const nom = txt(o.nom, 80).toUpperCase(), prenom = txt(o.prenom, 80);
  if (!nom) erreurs.push("nom manquant"); if (!prenom) erreurs.push("prénom manquant");
  I.nom = nom; I.nomF = nom; I.prenom = prenom.replace(/(^|[\s-])(\p{L})/gu, (z, a, b) => a + b.toUpperCase());
  const d = dateIso(o.ddn, c.auj); if (d === null) erreurs.push("date de naissance illisible ou impossible (« " + txt(o.ddn, 20) + " »)"); else if (d) I.ddn = d;
  const sx = sexe(o.sexe); if (sx === null) avert.push("sexe non reconnu (« " + txt(o.sexe, 10) + " ») : laissé vide"); else if (sx) I.sexe = sx;
  for (const k of ["tel", "tel2"]) { const t = tel(o[k]); if (t === null) avert.push((k === "tel" ? "téléphone" : "téléphone 2") + " illisible : laissé vide"); else if (t) I[k] = t; }
  const em = txt(o.email, 120); if (em && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)) avert.push("e-mail illisible : laissé vide"); else if (em) I.email = em;
  for (const k of ["cin", "adresse", "numAdh", "cor", "numOrig"]) { const v = txt(o[k], k === "adresse" ? 200 : 80); if (v) I[k] = v; }
  if (I.cin) I.cin = I.cin.toUpperCase();
  const mu = txt(o.mut, 80); if (mu) { const m0 = (c.mut || []).find((z) => sansAcc(z) === sansAcc(mu)); I.mut = m0 || mu; }
  const dg = txt(o.diag, 120); if (dg) { const d0 = (c.diags || []).find((z) => sansAcc(z) === sansAcc(dg)); C.diag = d0 || dg; if (!d0 && (c.diags || []).length) avert.push("diagnostic « " + dg + " » ajouté à la liste"); }
  let etab = c.etabDefaut || ""; const et = txt(o.etab, 80);
  if (et) { const e0 = (c.etabs || []).find((z) => sansAcc(z.code) === sansAcc(et) || sansAcc(z.nom) === sansAcc(et)); if (e0) etab = e0.code; else avert.push("établissement « " + et + " » inconnu : " + (etab ? "établissement par défaut" : "aucun")); }
  if (!etab) erreurs.push("aucun établissement");
  return { identite: I, clinique: C, etab, erreurs, avert };
}
// Clé de doublon : nom + prénom + date de naissance (sans accents ni casse) ; sans date : nom + prénom
export const cleDoublon = (I) => [sansAcc(I.nomF || I.nom), sansAcc(I.prenom), I.ddn || ""].join("|");
// Toutes les lignes : lignes = [{ ligne (n° dans le fichier), valeurs }] ; existants = identités des dossiers du cabinet
export function analyser(lignes, existants, ctx) {
  const deja = new Map(); (existants || []).forEach((I) => { if (I) deja.set(cleDoublon(I), I); });
  const vus = new Map(), out = [];
  for (const l of (lignes || []).slice(0, MAX_LIGNES)) {
    const r = Object.assign({ ligne: l.ligne }, lireLigne(l.valeurs || {}, ctx)), k = cleDoublon(r.identite);
    if (!r.erreurs.length) {
      if (deja.has(k)) r.doublon = "déjà dans Onco360";
      else if (vus.has(k)) r.doublon = "même patient que la ligne " + vus.get(k);
      else vus.set(k, l.ligne);
    }
    r.etat = r.erreurs.length ? "erreur" : r.doublon ? "doublon" : "ok";
    out.push(r);
  }
  const n = (e) => out.filter((r) => r.etat === e).length;
  return { lignes: out, ok: n("ok"), doublons: n("doublon"), erreurs: n("erreur"), tropLong: (lignes || []).length > MAX_LIGNES };
}
// Feuille lue par SheetJS (sheet_to_json avec header: 1) : 1re ligne non vide = titres → [{ ligne, valeurs }], colonnes inconnues
export function depuisTableau(rows) {
  const R = (rows || []).map((r) => (Array.isArray(r) ? r : []));
  const i0 = R.findIndex((r) => r.some((v) => String(v == null ? "" : v).trim())); if (i0 < 0) return { lignes: [], inconnues: [], manquantes: COLONNES.filter((c) => c[2]).map((c) => c[1]) };
  const cles = R[i0].map(cleColonne), inconnues = R[i0].filter((t, i) => String(t || "").trim() && !cles[i]).map((t) => String(t).trim());
  const manquantes = COLONNES.filter((c) => c[2] && cles.indexOf(c[0]) < 0).map((c) => c[1]);
  const lignes = [];
  for (let i = i0 + 1; i < R.length; i++) {
    if (!R[i].some((v) => String(v == null ? "" : v).trim())) continue;
    const valeurs = {}; cles.forEach((k, j) => { if (k && valeurs[k] == null) valeurs[k] = R[i][j]; });
    lignes.push({ ligne: i + 1, valeurs });
  }
  return { lignes, inconnues, manquantes };
}
