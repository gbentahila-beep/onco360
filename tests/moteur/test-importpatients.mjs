// L2 (31/10/2026) : import des patients par fichier Excel, sans navigateur : node tests/moteur/test-importpatients.mjs
import { COLONNES, cleColonne, dateIso, lireLigne, analyser, depuisTableau, cleDoublon, MAX_LIGNES } from "../../public/js/moteur/importpatients.js";
let ok = 0, ko = 0;
const cas = (nom, v) => { if (v) { ok++; console.log("  ✔ " + nom); } else { ko++; console.log("  ✘ " + nom); } };
const ctx = { auj: "2026-10-31", etabs: [{ code: "HGC", nom: "Hôpital Général de Casablanca" }, { code: "CAB", nom: "Cabinet" }], etabDefaut: "CAB", diags: ["Sein", "Côlon"], mut: ["CNOPS", "CNSS"] };

console.log("Colonnes");
cas("titres du modèle reconnus", COLONNES.every((c) => cleColonne(c[1]) === c[0]));
cas("titres proches reconnus", cleColonne("NOM") === "nom" && cleColonne("Prénom ") === "prenom" && cleColonne("Date de naissance") === "ddn" && cleColonne("Téléphone") === "tel" && cleColonne("N° dossier") === "numOrig" && cleColonne("Mutuelle") === "mut");
cas("titre inconnu", cleColonne("Groupe sanguin") === null);

console.log("Dates");
cas("JJ/MM/AAAA", dateIso("15/06/1965", "2026-10-31") === "1965-06-15" && dateIso("5-6-1965") === "1965-06-05");
cas("AAAA-MM-JJ", dateIso("1965-06-15") === "1965-06-15");
cas("nombre d'Excel", dateIso(23908) === "1965-06-15");
cas("impossible : 31/02, futur, avant 1900", dateIso("31/02/1990") === null && dateIso("01/01/2030", "2026-10-31") === null && dateIso("01/01/1850") === null);
cas("illisible", dateIso("juin 65") === null && dateIso("") === "" && dateIso(null) === "");

console.log("Ligne");
const r = lireLigne({ nom: " benali ", prenom: "fatima zahra", ddn: "15/06/1965", sexe: "Femme", tel: "600001111", mut: "cnops", diag: "sein", etab: "hôpital général de casablanca", cin: "ab123", numOrig: "A-12" }, ctx);
cas("identité rangée", r.identite.nomF === "BENALI" && r.identite.nom === "BENALI" && r.identite.prenom === "Fatima Zahra" && r.identite.ddn === "1965-06-15" && r.identite.sexe === "F");
cas("téléphone complété (0 devant)", r.identite.tel === "0600001111");
cas("listes du cabinet : même écriture", r.identite.mut === "CNOPS" && r.clinique.diag === "Sein" && r.etab === "HGC" && !r.erreurs.length);
cas("CIN en majuscules, ancien numéro gardé", r.identite.cin === "AB123" && r.identite.numOrig === "A-12");
const r2 = lireLigne({ nom: "", prenom: "X", ddn: "31/02/1990", sexe: "X", tel: "12", etab: "Inconnu" }, ctx);
cas("erreurs : nom manquant, date impossible", r2.erreurs.length === 2);
cas("avertissements : sexe, téléphone, établissement", r2.avert.length === 3 && r2.etab === "CAB");
cas("sans établissement par défaut : erreur", lireLigne({ nom: "A", prenom: "B" }, { etabs: [] }).erreurs.indexOf("aucun établissement") >= 0);
cas("homme : H ou M", lireLigne({ nom: "A", prenom: "B", sexe: "M" }, ctx).identite.sexe === "H" && lireLigne({ nom: "A", prenom: "B", sexe: "homme" }, ctx).identite.sexe === "H");
cas("diagnostic nouveau : ajouté (avertissement)", lireLigne({ nom: "A", prenom: "B", diag: "Pancréas" }, ctx).avert.some((a) => /ajouté/.test(a)));

console.log("Fichier entier");
const T = depuisTableau([[], ["Nom", "Prénom", "Date de naissance (JJ/MM/AAAA)", "Groupe sanguin"], ["ALAMI", "Karim", "01/01/1970", "A+"], ["", "", "", ""], ["ALAMI", "karim", "01/01/1970"], ["BENALI", "Fatima", "15/06/1965"], ["", "Sans nom"]]);
cas("titres, lignes vides sautées", T.lignes.length === 4 && T.lignes[0].ligne === 3 && T.inconnues[0] === "Groupe sanguin" && !T.manquantes.length);
const A = analyser(T.lignes, [{ nomF: "BENALI", prenom: "Fatima", ddn: "1965-06-15" }], ctx);
cas("doublon dans le fichier", A.lignes[1].etat === "doublon" && /ligne 3/.test(A.lignes[1].doublon));
cas("doublon dans Onco360", A.lignes[2].etat === "doublon" && /déjà/.test(A.lignes[2].doublon));
cas("compte", A.ok === 1 && A.doublons === 2 && A.erreurs === 1);
cas("colonne obligatoire manquante", depuisTableau([["Prénom"], ["X"]]).manquantes.indexOf("Nom") >= 0);
cas("clé de doublon sans accents", cleDoublon({ nomF: "BÉNALI", prenom: "fatima" }) === cleDoublon({ nom: "Benali", prenom: "Fatima" }));
cas("limite de lignes", analyser(Array.from({ length: MAX_LIGNES + 3 }, (_, i) => ({ ligne: i, valeurs: { nom: "N" + i, prenom: "P" } })), [], ctx).tropLong === true);

console.log((ko ? "✘ " : "✔ ") + ok + " réussis, " + ko + " en échec");
process.exit(ko ? 1 : 0);
