// L5 (31/10/2026) : contrôle des dossiers au chargement et aller-retour d'un dossier (enregistré puis relu : aucun champ perdu), sans navigateur :
// node tests/moteur/test-controle.mjs
import { readFileSync } from "node:fs";
import { controlerDossier, dateValide } from "../../public/js/moteur/controle.js";
import { separer, fusionner } from "../../public/js/donnees/conversion.js";
let ok = 0, ko = 0;
const cas = (nom, v, d) => { if (v) { ok++; console.log("  ✔ " + nom); } else { ko++; console.log("  ✘ " + nom + (d ? " : " + JSON.stringify(d).slice(0, 400) : "")); } };

console.log("Contrôle");
cas("dates", dateValide("2026-02-28") && !dateValide("2026-02-30") && !dateValide("1850-01-01") && !dateValide("15/06/1965") && !dateValide(""));
const d0 = { identite: { nom: "A", prenom: "B", poids: "60", ddn: "1965-02-30" }, clinique: { mut: "CNOPS" }, rdvsJson: JSON.stringify([{ id: "r1", d: "2026-10-01" }, { id: "r1", d: "2026-13-01" }, { id: "r2", d: "2026-11-01", rtfin: "rtX" }, null]), lignesJson: "[{", rtsJson: JSON.stringify([{ id: "rt1", scan: "2026-10-40" }]), planningJson: JSON.stringify({ L9: { 1: { fixe: "2026-10-01" } } }) };
const r = controlerDossier(d0, "2026-10-31"), ks = r.signalements.map((s) => s.k);
cas("champs mal rangés réparés", r.doc.clinique.poids === "60" && !("poids" in r.doc.identite) && r.doc.identite.mut === "CNOPS" && !("mut" in r.doc.clinique) && r.doc.identite.nomF === "A");
cas("date de naissance impossible signalée", ks.indexOf("ddn") >= 0);
cas("rendez-vous : date impossible, double, orphelin, vide", ["rdv:date", "rdv:double", "rdv:orphelin", "rdv:vide"].every((k) => ks.indexOf(k) >= 0), ks);
cas("partie illisible signalée et gardée", ks.indexOf("illisible:lignesJson") >= 0 && r.doc.lignesJson === "[{");
cas("radiothérapie : date impossible", ks.indexOf("rt:date") >= 0);
cas("planning sans ligne", ks.indexOf("planning:orphelin") >= 0);
cas("aucune donnée du patient dans les types", ks.every((k) => !/A|B|CNOPS/.test(k)));
cas("dossier d'origine intact", d0.identite.poids === "60" && d0.clinique.mut === "CNOPS");
const propre = controlerDossier({ identite: { nom: "X", nomF: "X", prenom: "Y", ddn: "1970-01-01" }, clinique: { poids: "70" }, rdvsJson: "[]", lignesJson: "[]", rtsJson: "[]", planningJson: "{}" }, "2026-10-31");
cas("dossier sain : rien", !propre.reparations.length && !propre.signalements.length);

console.log("Jeu de test fictif : contrôle et aller-retour de chaque dossier");
const S = JSON.parse(readFileSync(new URL("../seed-fictif.json", import.meta.url), "utf8"));
const cles = Object.keys(S).filter((k) => /^espaces\/[^/]+\/patients\/[^/]+$/.test(k));
const plat = (o, p, out) => { if (o && typeof o === "object" && !Array.isArray(o)) Object.keys(o).forEach((k) => plat(o[k], p ? p + "." + k : k, out)); else if (Array.isArray(o)) o.forEach((v, i) => plat(v, p + "[" + i + "]", out)); else out.set(p, o); return out; };
const ignore = (p) => /(^|\.)(hc|hcm|_h)$|\.hc\.|\.hcm\./.test(p); // calculés à la lecture (heures de consultation), jamais enregistrés
let pertes = [], signal = 0;
for (const k of cles) {
  const d = S[k], id = k.split("/").pop(), c = controlerDossier(d, "2026-10-31"); signal += c.signalements.length;
  const fin = S[k.replace("/patients/", "/patientsFinances/")], m = fin ? JSON.parse(fin.montantsJson || "{}") : null;
  const P = fusionner(id, d, m), s = separer(P).patient;
  const avant = { identite: d.identite || {}, clinique: d.clinique || {}, lignes: JSON.parse(d.lignesJson || "[]"), rdvs: JSON.parse(d.rdvsJson || "[]"), rts: JSON.parse(d.rtsJson || "[]") };
  const apres = { identite: s.identite, clinique: s.clinique, lignes: JSON.parse(s.lignesJson), rdvs: JSON.parse(s.rdvsJson), rts: JSON.parse(s.rtsJson) };
  // champs de la fiche rangés à part par separer (clinique._autres) : comparés une fois remis à plat
  const cl = Object.assign({}, apres.clinique, apres.clinique._autres || {}); delete cl._autres; apres.clinique = cl;
  const A0 = plat(avant, "", new Map()), A1 = plat(apres, "", new Map());
  for (const [p, v] of A0) { if (ignore(p)) continue; const p2 = p.replace(/^identite\./, "identite.").replace(/^clinique\./, "clinique."); if (!A1.has(p2) && !A1.has(p2.replace(/^identite\./, "clinique.")) && !A1.has(p2.replace(/^clinique\./, "identite."))) pertes.push(id + " " + p); else if (A1.has(p2) && JSON.stringify(A1.get(p2)) !== JSON.stringify(v)) pertes.push(id + " " + p + " changé"); }
}
cas(cles.length + " dossiers relus : aucun champ perdu ni changé à l'aller-retour", pertes.length === 0, pertes.slice(0, 10));
console.log("  (" + signal + " signalement(s) dans le jeu fictif)");
console.log((ko ? "✘ " : "✔ ") + ok + " réussis, " + ko + " en échec");
process.exit(ko ? 1 : 0);
