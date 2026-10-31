// Lot 9 (31/10/2026) : feuilles de soins CNOPS et CNSS, rendu des valeurs à leur place. node tests/moteur/test-feuillesoins.mjs
import { FORMULAIRES, feuilleDe, rendreFeuille, totalActes, montantTxt, nombre } from "../../public/js/donnees/feuillesoins.js";
let ok = 0, ko = 0;
const cas = (nom, v, d) => { if (v) { ok++; console.log("  ✔ " + nom); } else { ko++; console.log("  ✘ " + nom + (d === undefined ? "" : " " + JSON.stringify(d).slice(0, 300))); } };
const V = { malNom: "TEST Patiente", malDdn: "1965-06-15", sexe: "F", type: "maladie", pli: "non", inpe: "123456789", le: "2026-10-30", leM: "2026-10-30", malCin: "AB123456", assCin: "AB123456",
  actes: [{ d: "2026-10-30", code: "1234", lettre: "CS", valeur: "1", m: "300" }, { d: "2026-10-30", m: "150,5" }, { d: "2026-10-30", m: "10" }], cim: "C50" };
cas("feuille d'après la mutuelle : CNSS si citée, sinon CNOPS", feuilleDe("AMO CNSS") === "cnss" && feuilleDe("CNOPS") === "cnops" && feuilleDe("") === "cnops" && feuilleDe("AXA") === "cnops");
cas("total des actes (virgule acceptée)", totalActes(V.actes) === 460.5 && montantTxt(460.5) === "460,50" && nombre(" 1 200,5 ") === 1200.5 && nombre("") === null);
for (const k of ["cnops", "cnss"]) {
  const h = rendreFeuille(k, V, { base: "" }), f = FORMULAIRES[k];
  cas(k + " : deux pages, fond de chaque page", (h.match(/class="fs-p"/g) || []).length === 2 && f.pages.every((p) => h.indexOf('src="' + p + '"') >= 0));
  cas(k + " : sans le fond, aucune image (impression sur la feuille officielle)", rendreFeuille(k, V, { fond: false }).indexOf("<img") < 0);
  const dn = (h.match(/>(\d)<\/span>/g) || []).map((z) => z.slice(1, 2)).join("");
  cas(k + " : date de naissance en cases (JJMMAAAA)", dn.indexOf("15061965") >= 0, dn.slice(0, 40));
  cas(k + " : sexe F coché, M non", (h.match(/fs-x/g) || []).length === 2, (h.match(/fs-x/g) || []).length);
  cas(k + " : actes limités au nombre de lignes de la feuille (" + f.actes.max + ")", (h.match(/150,50/g) || []).length === (f.actes.max >= 2 ? 1 : 0) && (h.indexOf(">10,00<") >= 0) === (f.actes.max >= 3));
  cas(k + " : toutes les positions dans la page (0 à 100 %)", (h.match(/(left|top):(-?[\d.]+)%/g) || []).every((z) => { const v = parseFloat(z.split(":")[1]); return v >= 0 && v <= 100; }));
}
const hc = rendreFeuille("cnops", V, {}), hs = rendreFeuille("cnss", V, {});
cas("CNOPS : pli confidentiel « non » entouré", (hc.match(/fs-rond/g) || []).length === 1);
cas("CNSS : pas de pli confidentiel", hs.indexOf("fs-rond") < 0);
cas("CNSS : CIN de 8 caractères sur 6 cases : répartis en plus petit", (hs.match(/fs-serre/g) || []).length === 8, (hs.match(/fs-serre/g) || []).length);
cas("CNSS : code de l'acte (4 chiffres) dans ses 4 cases", /fs-c" style="left:[\d.]+%;top:[\d.]+%">1<\/span><span class="fs-v fs-c" style="left:[\d.]+%;top:[\d.]+%">2/.test(hs));
console.log("\n" + ok + " réussis, " + ko + " échoués"); if (ko) process.exit(1);
