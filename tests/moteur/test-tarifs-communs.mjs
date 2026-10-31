// 31/10/2026 (lots 7.1 à 7.3, accord de Dr Bentahila du 29/10) : séance de chimiothérapie et radiothérapie : taux propres du lieu, sinon tarif commun,
// sinon (comme avant) la ligne de l'établissement de repli. node tests/moteur/test-tarifs-communs.mjs
import { seanceAu, rtAu } from "../../public/js/moteur/finances.js";
let ok = 0, ko = 0;
const cas = (nom, v, d) => { if (v) { ok++; console.log("  ✔ " + nom); } else { ko++; console.log("  ✘ " + nom + (d === undefined ? "" : " " + JSON.stringify(d))); } };
const L = (type, h) => ({ type, libelle: type, historique: h });
const T = { repli: "A", etablissements: { A: { activites: [L("seance", [{ depuis: "2000-01-01", brut: 500, retro: 0, impot: 10 }]), L("rt", [{ depuis: "2000-01-01", brut: null, retro: 70, impot: 10 }])] }, B: { activites: [] } },
  seanceCommune: L("seance", [{ depuis: "2000-01-01", brut: 500, retro: 50, impot: 10 }, { depuis: "2026-11-01", brut: 600, retro: 50, impot: 10 }]), tauxRT: { retro: 60, impot: 10 } };
cas("lieu avec sa ligne « Séance » : ses taux propres", seanceAu(T, "A", "2026-10-15").retro === 0);
cas("lieu sans ligne : tarif commun (50 % / 10 %)", seanceAu(T, "B", "2026-10-15").retro === 50 && seanceAu(T, "B", "2026-10-15").brut === 500);
cas("tarif commun daté : 600 DH à partir du 01/11/2026", seanceAu(T, "B", "2026-11-02").brut === 600);
const T2 = JSON.parse(JSON.stringify(T)); delete T2.seanceCommune; delete T2.tauxRT;
cas("sans tarif commun : ligne de l'établissement de repli (comme avant)", seanceAu(T2, "B", "2026-10-15").retro === 0 && rtAu(T2, "B", "2026-10-15").retro === 70);
cas("radiothérapie, lieu avec sa ligne : ses taux propres (70 %)", rtAu(T, "A", "2026-10-15").retro === 70);
cas("radiothérapie, lieu sans ligne : taux commun (60 %)", rtAu(T, "B", "2026-10-15").retro === 60, rtAu(T, "B", "2026-10-15"));
console.log("\n" + ok + " réussis, " + ko + " échoués"); if (ko) process.exit(1);
