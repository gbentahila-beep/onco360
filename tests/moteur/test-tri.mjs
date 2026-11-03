// IG5 (03/11/2026) : tri au clic sur le titre d'une colonne. node tests/moteur/test-tri.mjs
import { trierPar, triSuivant } from "../../public/js/moteur/tri.js";
let ok = 0, ko = 0;
const cas = (nom, v, d) => { if (v) { ok++; console.log("  ✔ " + nom); } else { ko++; console.log("  ✘ " + nom + (d === undefined ? "" : "  " + JSON.stringify(d))); } };
const L = [{ n: "Émile", d: "2026-10-06", k: 10 }, { n: "anne", d: "", k: 2 }, { n: "Bruno", d: "2025-01-01", k: null }, { n: "Patient 10", d: "2026-01-01", k: 1 }, { n: "Patient 9", d: "2026-01-01", k: 1 }];
const noms = (l) => l.map((x) => x.n);
cas("texte : accents et majuscules ignorés, nombres dans l'ordre (9 avant 10)", JSON.stringify(noms(trierPar(L, (x) => x.n, 1))) === JSON.stringify(["anne", "Bruno", "Émile", "Patient 9", "Patient 10"]), noms(trierPar(L, (x) => x.n, 1)));
cas("▼ : ordre inverse", noms(trierPar(L, (x) => x.n, -1))[0] === "Patient 10");
cas("dates : vides en dernier dans les deux sens", noms(trierPar(L, (x) => x.d, 1)).pop() === "anne" && noms(trierPar(L, (x) => x.d, -1)).pop() === "anne");
cas("à égalité : ordre d'avant gardé", JSON.stringify(noms(trierPar(L, (x) => x.d, 1)).slice(1, 3)) === JSON.stringify(["Patient 10", "Patient 9"]));
cas("nombres", noms(trierPar(L, (x) => x.k, 1)).slice(0, 2).join() === "Patient 10,Patient 9" && noms(trierPar(L, (x) => x.k, 1)).pop() === "Bruno");
cas("clics : ▲, ▼, puis défaut ; autre colonne : ▲", JSON.stringify(triSuivant(null, "a")) === '{"k":"a","s":1}' && triSuivant({ k: "a", s: 1 }, "a").s === -1 && triSuivant({ k: "a", s: -1 }, "a").k === "" && triSuivant({ k: "a", s: -1 }, "b").s === 1);
cas("liste d'origine non modifiée", L[0].n === "Émile");
console.log(ko ? `\n❌ ${ko} échoués, ${ok} réussis` : `\n✅ ${ok} réussis`);
if (ko) process.exit(1);
