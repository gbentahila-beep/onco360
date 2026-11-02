// IG1 (02/11/2026) : recherche de patient classée. node tests/moteur/test-cherchepatient.mjs
import { chercherPatients, motsRecherche, rangMot, telNormal, partiesTrouvees } from "../../public/js/moteur/cherchepatient.js";
let ok = 0, ko = 0;
const cas = (nom, v, d) => { if (v) { ok++; console.log("  ✔ " + nom); } else { ko++; console.log("  ✘ " + nom + (d === undefined ? "" : "  " + JSON.stringify(d))); } };
const P = (nom, num, o = {}) => ({ x: nom, f: Object.assign({ nom, num }, o) });
const L = [P("PATIENT TEST 57", "202608057"), P("PATIENT TEST 58", "202608058"), P("PATIENT TEST 8", "202601008", { tels: ["06 11 22 33 44"] }),
  P("PATIENT TEST 80", "202610080", { ddn: "1959-06-15", cin: "BE123456", tels: ["+212 6 00 00 00 01"] }), P("PATIENT REF 1", "202609001", { autres: "Cancer de l’oropharynx" })];
const r = chercherPatients(L, "test 80");
cas("« test 80 » : TEST 80 en tête (avant les n° qui contiennent 80)", r[0] === "PATIENT TEST 80", r);
cas("« test 80 » : TEST 8 n'est pas proposé (son n° ne contient pas 80)", !r.includes("PATIENT TEST 8"), r);
cas("« 202610 » : n° qui commence par les chiffres", chercherPatients(L, "202610")[0] === "PATIENT TEST 80");
cas("téléphone avec espaces, avec +212 ou sans le 0", chercherPatients(L, "06 00 00 00 01")[0] === "PATIENT TEST 80" && chercherPatients(L, "+212600000001")[0] === "PATIENT TEST 80" && chercherPatients(L, "600000001")[0] === "PATIENT TEST 80");
cas("date de naissance 15/06/1959 et 15061959", chercherPatients(L, "15/06/1959")[0] === "PATIENT TEST 80" && chercherPatients(L, "15061959").length === 1);
cas("CIN (majuscules ou non)", chercherPatients(L, "be123456")[0] === "PATIENT TEST 80" && chercherPatients(L, "BE12").length === 1);
cas("autres champs (localisation) en dernier recours", chercherPatients(L, "oropharynx")[0] === "PATIENT REF 1");
cas("sans recherche : tous, ordre d'origine", chercherPatients(L, "").length === L.length && chercherPatients(L, "")[0] === "PATIENT TEST 57");
cas("rangs : début du nom 0, début d'un mot 1, milieu 3", rangMot({ nom: "PATIENT TEST" }, "pat") === 0 && rangMot({ nom: "PATIENT TEST" }, "tes") === 1 && rangMot({ nom: "PATIENT TEST" }, "ien") === 3);
cas("accents ignorés", chercherPatients([P("Élodie Bénani", "1")], "elodie benani").length === 1);
cas("mots : un numéro avec espaces = un seul mot", JSON.stringify(motsRecherche("06 00 00 00 01")) === '["0600000001"]' && motsRecherche("test 80").length === 2);
cas("téléphone normalisé", telNormal("+212 6 12 34 56 78") === "0612345678" && telNormal("00212612345678") === "0612345678");
cas("parties surlignées du nom", JSON.stringify(partiesTrouvees("PATIENT TEST 80", "test 80")) === "[[8,12],[13,15]]", partiesTrouvees("PATIENT TEST 80", "test 80"));
console.log(ko ? `\n❌ ${ko} échec(s), ${ok} réussi(s)` : `\n✅ ${ok} réussis`);
process.exit(ko ? 1 : 0);
