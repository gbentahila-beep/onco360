// L5 (31/10/2026) : contrôle d'un dossier patient au chargement (calculs purs, sans DOM ni Firebase ; test : node tests/moteur/test-controle.mjs).
// Champs mal rangés : réparés dans la copie lue (jamais écrits sans un enregistrement du dossier) ; rendez-vous orphelins, dates impossibles,
// contenus illisibles : signalés (ce qui est illisible n'est jamais effacé). Retour : { doc (copie, réparée), reparations [], signalements [] },
// chaque élément = { k (type, sans donnée du patient), txt (phrase pour le médecin) }.

const JSONS = ["lignesJson", "planningJson", "rdvsJson", "rtsJson"];
// Champs de la fiche qui vont dans clinique (pas dans identite) et l'inverse
const VERS_CLINIQUE = ["poids", "taille", "diag", "diagP", "allergies", "allergie"];
const VERS_IDENTITE = ["nom", "nomF", "prenom", "ddn", "sexe", "tel", "tel2", "cin", "mut", "cor"];
export const dateValide = (s, min, max) => {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s || "")); if (!m) return false;
  const a = +m[1], d = new Date(Date.UTC(a, +m[2] - 1, +m[3]));
  return d.getUTCMonth() === +m[2] - 1 && d.getUTCDate() === +m[3] && a >= (min || 1900) && a <= (max || 2100);
};
const lire = (s, def) => { if (s == null || s === "") return { v: def, ok: true }; try { const v = JSON.parse(s); return { v: v == null ? def : v, ok: true }; } catch (e) { return { v: def, ok: false }; } };

export function controlerDossier(d0, auj) {
  const doc = JSON.parse(JSON.stringify(d0 || {})), rep = [], sig = [];
  doc.identite = doc.identite && typeof doc.identite === "object" ? doc.identite : {};
  doc.clinique = doc.clinique && typeof doc.clinique === "object" ? doc.clinique : {};
  const I = doc.identite, C = doc.clinique;
  // 1. Champs mal rangés (valeur dans la mauvaise partie, place libre dans la bonne) : déplacés
  for (const k of VERS_CLINIQUE) if (I[k] != null && I[k] !== "" && (C[k] == null || C[k] === "")) { C[k] = I[k]; delete I[k]; rep.push({ k: "range:" + k, txt: "« " + k + " » rangé dans les informations médicales" }); }
  for (const k of VERS_IDENTITE) if (C[k] != null && C[k] !== "" && (I[k] == null || I[k] === "")) { I[k] = C[k]; delete C[k]; rep.push({ k: "range:" + k, txt: "« " + k + " » rangé dans l'identité" }); }
  if (!I.nomF && I.nom) { I.nomF = String(I.nom); rep.push({ k: "nomF", txt: "nom de famille repris du nom" }); }
  // 2. Contenus illisibles : signalés, gardés tels quels
  const L = {};
  for (const k of JSONS) { const r = lire(doc[k], k === "planningJson" ? {} : []); L[k] = r.v; if (!r.ok) sig.push({ k: "illisible:" + k, txt: "partie illisible du dossier (" + k.replace("Json", "") + ") : gardée sans changement, à vérifier" }); }
  // 3. Dates impossibles
  if (I.ddn && !dateValide(I.ddn, 1900, auj ? +auj.slice(0, 4) : 2100)) sig.push({ k: "ddn", txt: "date de naissance impossible (" + String(I.ddn).slice(0, 12) + ")" });
  else if (I.ddn && auj && I.ddn > auj) sig.push({ k: "ddn", txt: "date de naissance dans le futur" });
  const rdvs = Array.isArray(L.rdvsJson) ? L.rdvsJson : [], rts = Array.isArray(L.rtsJson) ? L.rtsJson : [], lignes = Array.isArray(L.lignesJson) ? L.lignesJson : [];
  rdvs.forEach((r, i) => {
    if (!r || typeof r !== "object") { sig.push({ k: "rdv:vide", txt: "rendez-vous n° " + (i + 1) + " vide" }); return; }
    if (!r.id) sig.push({ k: "rdv:id", txt: "rendez-vous du " + (r.d || "?") + " sans identifiant" });
    if (!dateValide(r.d)) sig.push({ k: "rdv:date", txt: "rendez-vous avec une date impossible (" + String(r.d || "vide").slice(0, 12) + ")" });
    // Rendez-vous orphelin : fin de radiothérapie dont la radiothérapie n'existe plus
    if (r.rtfin && !rts.some((t) => t && t.id === r.rtfin)) sig.push({ k: "rdv:orphelin", txt: "rendez-vous de fin de radiothérapie du " + (r.d || "?") + " sans radiothérapie" });
  });
  const ids = rdvs.filter((r) => r && r.id).map((r) => r.id), dbl = ids.filter((v, i) => ids.indexOf(v) !== i);
  if (dbl.length) sig.push({ k: "rdv:double", txt: dbl.length + " rendez-vous en double (même identifiant)" });
  lignes.forEach((l) => {
    (l && Array.isArray(l.cures) ? l.cures : []).forEach((c, n) => {
      if (c && c.st === "recue" && c.reelle && !dateValide(c.reelle)) sig.push({ k: "cure:date", txt: "cure " + (n + 1) + " validée avec une date impossible" });
      if (c && c.st === "recue" && !c.reelle && !c.valLe) sig.push({ k: "cure:sansdate", txt: "cure " + (n + 1) + " validée sans date" });
    });
  });
  rts.forEach((t) => { if (t) ["scan", "deb", "fin"].forEach((z) => { if (t[z] && !dateValide(t[z])) sig.push({ k: "rt:date", txt: "radiothérapie : date « " + z + " » impossible" }); }); });
  // Planning d'une ligne de chimio qui n'existe plus : signalé (le planning n'est jamais effacé ici)
  const P = L.planningJson && typeof L.planningJson === "object" ? L.planningJson : {};
  const orph = Object.keys(P).filter((id) => !lignes.some((l) => l && l.id === id));
  if (orph.length) sig.push({ k: "planning:orphelin", txt: orph.length + " planning(s) de chimio sans ligne de traitement" });
  return { doc, reparations: rep, signalements: sig };
}
