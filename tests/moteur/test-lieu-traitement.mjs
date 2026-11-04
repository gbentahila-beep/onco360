// Lot LT (04/11/2026, demande de Dr Bentahila) : lieu de traitement d'une ligne de chimio (L.hop) ; taux commun de la radiothérapie daté.
// Séances comptées au lieu de la ligne ; consultations (dont celle du jour de chimio) au lieu du patient ; RT à son lieu (inchangé).
// Données fictives. node tests/moteur/test-lieu-traitement.mjs
import { evtsFin, tauxRT, rtAu } from "../../public/js/moteur/finances.js";
import { evtsAgenda } from "../../public/js/moteur/agenda.js";
let ok = 0, ko = 0;
const cas = (nom, v, d) => { if (v) { ok++; console.log("  ✔ " + nom); } else { ko++; console.log("  ✘ " + nom + (d === undefined ? "" : " " + JSON.stringify(d))); } };
const H = (brut, retro, impot) => [{ depuis: "2000-01-01", brut, retro, impot }];
const act = (type, h) => ({ type, libelle: type, historique: h });
const T = {
  repli: "CAB",
  etablissements: {
    CAB: { activites: [act("cchimio", H(400, 0, 0)), act("suivi", H(300, 0, 0))] },
    HGC: { activites: [act("seance", H(1000, 50, 10)), act("cchimio", H(250, 0, 10))] },
    CIOC: { activites: [act("seance", H(800, 40, 10))] },
  },
  seanceCommune: act("seance", H(500, 0, 10)), actesRT: [{ nom: "Sein 3D", prix: 20000 }], tauxRT: { retro: 60, impot: 10 },
};
const PR = { id: "pr1", nom: "PACLITAXEL HEBDO", c: 21, dr: [{ id: "d1", p: "PACLITAXEL", u: "mg/m²", d: 80, j: [1] }] };
const ligne = (hop) => Object.assign({ id: "L1", protoId: PR.id, pr: PR, j1: "2026-10-01", poids: "70", cures: [{ st: "recue", reelle: "2026-10-01" }, { st: "recue", reelle: "2026-10-22" }, {}] }, hop ? { hop } : {});
const ctx = { table: T, bib: {}, feries: [], aujourdhui: "2026-10-25" };
const M = { cures: { L1: { 1: { consJ: { 1: null } } } }, rdv: {} };
const patient = (hop, L, extra) => Object.assign({ id: "p1", nom: "PATIENT FICTIF", hop, lignes: [L], rdvs: [{ id: "r1", type: "Suivi", d: "2026-10-10", st: "fait" }], rts: [] }, extra || {});

// Cas 2 : patient rattaché au cabinet, chimio faite à HGC
const e2 = evtsFin(patient("CAB", ligne("HGC")), M, ctx);
const sea2 = e2.filter((e) => e[1] === "seance"), cc2 = e2.filter((e) => e[1] === "cchimio"), rv2 = e2.filter((e) => e[1] === "suivi");
cas("cas 2 : les séances sont comptées à HGC (lieu de la ligne)", sea2.length === 2 && sea2.every((e) => e[2] === "HGC"), sea2.map((e) => e[2]));
cas("cas 2 : séance au tarif de HGC (1 000 DH, net 450)", sea2[0][4] === 1000 && sea2[0][6] === 450, sea2[0]);
cas("cas 2 : consultation du jour de chimio au cabinet (lieu du patient, 400 DH)", cc2.length === 1 && cc2[0][2] === "CAB" && cc2[0][4] === 400, cc2);
cas("cas 2 : consultation ordinaire au cabinet", rv2.length === 1 && rv2[0][2] === "CAB" && rv2[0][4] === 300, rv2);
// Cas 1 : patient rattaché à HGC, ligne à HGC : tout à HGC
const e1 = evtsFin(patient("HGC", ligne("HGC")), M, ctx);
cas("cas 1 : patient de HGC : séances et consultation de chimio à HGC", e1.filter((e) => e[1] === "seance" || e[1] === "cchimio").every((e) => e[2] === "HGC"));
// Ligne sans lieu (lignes d'avant le lot) : lieu du patient, comme avant
const e0 = evtsFin(patient("CAB", ligne("")), M, ctx);
cas("ligne sans lieu : séances au lieu du patient (comme avant), tarif commun 500 DH", e0.filter((e) => e[1] === "seance").every((e) => e[2] === "CAB" && e[4] === 500));
// Changement de lieu du patient (hopHist) : sans effet sur une ligne qui a son lieu
const eh = evtsFin(patient("CIOC", ligne("HGC"), { hopHist: [{ hop: "CAB", avant: "2026-10-15" }] }), M, ctx);
cas("patient changé de lieu : séances restent au lieu de la ligne", eh.filter((e) => e[1] === "seance").every((e) => e[2] === "HGC"));
cas("patient changé de lieu : consultation de chimio du 01/10 à l'ancien lieu (cabinet)", eh.find((e) => e[1] === "cchimio")[2] === "CAB");
// RT : son lieu (inchangé)
const PR2 = patient("CAB", ligne("HGC"), { rts: [{ id: "rt1", acte: "Sein 3D", hop: "CIOC", deb: "2026-09-01", fin: "2026-09-30", nb: 20 }] });
const rt = evtsFin(PR2, M, ctx).find((e) => e[1] === "rt");
cas("RT comptée à son lieu (CIOC), taux commun 60 % / 10 % : 7 200 DH", rt && rt[2] === "CIOC" && rt[6] === 7200, rt);

// Taux commun de la radiothérapie daté
const TT = { tauxRT: { retro: 55, impot: 10, historique: [{ depuis: "2000-01-01", retro: 60, impot: 10 }, { depuis: "2026-11-01", retro: 55, impot: 10 }] }, etablissements: {} };
cas("taux commun daté : 60 % avant le 01/11/2026", tauxRT(TT, "2026-10-15").retro === 60);
cas("taux commun daté : 55 % à partir du 01/11/2026", tauxRT(TT, "2026-11-02").retro === 55 && rtAu(TT, "X", "2026-11-02").retro === 55);
cas("ancien format sans date : comme avant", tauxRT({ tauxRT: { retro: 60, impot: 10 } }, "2026-11-02").retro === 60 && tauxRT({}, "2026-11-02") === null);
cas("taux commun vide : sans tarif", tauxRT({ tauxRT: { historique: [{ depuis: "2000-01-01", retro: null, impot: null }] } }, "2026-11-02") === null);

// Agenda : lieu de l'événement (« l ») et titre
const PA = { id: "p1", nom: "PATIENT FICTIF", hop: "CAB", lignes: [Object.assign(ligne("HGC"), { cures: [{ st: "recue", reelle: "2026-10-01" }, {}, {}] })], rdvs: [{ id: "r2", type: "Suivi", d: "2026-11-10", st: "prevu" }], rts: [{ id: "rt2", hop: "CIOC", scan: "2026-11-12" }] };
const ag = evtsAgenda(PA, { aujourdhui: "2026-10-25", bib: {}, feries: [] });
const c = ag.find((e) => /\|c\|/.test(e.k)), r = ag.find((e) => /\|r\|/.test(e.k)), s = ag.find((e) => /\|rt\|/.test(e.k));
cas("agenda : cure à HGC (titre et lieu)", c && c.l === "HGC" && /\(HGC\)$/.test(c.t), c);
cas("agenda : consultation au cabinet", r && r.l === "CAB", r);
cas("agenda : radiothérapie à CIOC", s && s.l === "CIOC", s);
console.log("\n" + ok + " réussi(s), " + ko + " échec(s)"); process.exit(ko ? 1 : 0);
