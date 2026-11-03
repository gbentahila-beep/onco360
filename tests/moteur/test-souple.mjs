// IG5 (03/11/2026) : recherche souple (tirets, espaces, accents, synonymes). node tests/moteur/test-souple.mjs
import { recherche, plat, variantes, chercheAussi } from "../../public/js/moteur/souple.js";
import { SYNONYMES } from "../../public/js/donnees/synonymes.js";
let ok = 0, ko = 0;
const cas = (nom, v, d) => { if (v) { ok++; console.log("  ✔ " + nom); } else { ko++; console.log("  ✘ " + nom + (d === undefined ? "" : "  " + JSON.stringify(d))); } };
const t = (q, texte) => recherche(q).test(texte);
cas("aplatir : accents, tirets, espaces, majuscules", plat("5-Fluoro Uracile") === "5fluorouracile" && plat("Épirubicine") === "epirubicine");
cas("5FU = 5-FU = 5 fu", ["5FU", "5-FU", "5 fu", "5 FU"].every((q) => t(q, "FOLFOX : 5-FU + oxaliplatine")));
cas("5-FU trouve « 5-FLUORO-URACILE »", t("5-FU", "5-FLUORO-URACILE 400 mg/m²"));
cas("Taxol trouve le paclitaxel", t("taxol", "Paclitaxel hebdomadaire 80 mg/m²"));
cas("CDDP trouve le cisplatine (accents ignorés)", t("cddp", "CISPLATINE 75") && t("CDDP", "Cisplatine"));
cas("Herceptin trouve le trastuzumab", t("herceptin", "Trastuzumab + docétaxel"));
cas("docetaxel sans accent trouve Docétaxel", t("docetaxel", "Docétaxel 75 mg/m²"));
cas("plusieurs mots : tous présents", t("cddp 5fu", "Cisplatine + 5-FU (ORL)") && !t("cddp 5fu", "Cisplatine + vinorelbine"));
cas("« 5 fu cisplatine » : « 5 fu » lu ensemble", t("5 fu cisplatine", "Cisplatine - 5-fluorouracile"));
cas("début de mot (saisie en cours)", t("cispl", "Cisplatine") && t("pacli", "PACLITAXEL"));
cas("rien ne correspond", !t("zzz", "Cisplatine") && !t("taxol", "Docétaxel"));
cas("recherche vide : tout passe", recherche("").vide && t("", "n'importe quoi"));
cas("« Cherché aussi » : nom du groupe", chercheAussi(recherche("taxol")) === "Cherché aussi : Paclitaxel" && chercheAussi(recherche("paclitaxel")) === "" && chercheAussi(recherche("xyz")) === "", chercheAussi(recherche("taxol")));
cas("variantes : groupe entier", variantes("cddp").includes("cisplatine") && variantes("inconnu").length === 1);
cas("XELOX = CAPOX", t("capox", "XELOX (capécitabine + oxaliplatine)"));
// Table : pas de nom en double dans deux groupes différents (un nom = un seul produit)
const vu = new Map(), doubles = [];
SYNONYMES.forEach((g, i) => new Set(g.map(plat)).forEach((k) => { if (vu.has(k) && vu.get(k) !== i) doubles.push(k); vu.set(k, i); }));
cas("table : chaque nom dans un seul groupe", !doubles.length, doubles);
cas("table : au moins 100 groupes", SYNONYMES.length >= 100, SYNONYMES.length);
console.log(ko ? `\n❌ ${ko} échoués, ${ok} réussis` : `\n✅ ${ok} réussis`);
if (ko) process.exit(1);
