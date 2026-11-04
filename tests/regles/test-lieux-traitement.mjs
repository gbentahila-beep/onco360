// Lot LT (04/11/2026) : règles des dossiers d'un autre lieu traités dans un lieu du membre (patients/{p}.lieuxTraitement) sur l'émulateur Firestore.
// Lancer (Java 21 nécessaire) :  cd tests/regles && npm test
// Comptes : MED (médecin, tous les lieux), INFH (infirmière HGC), INFC (infirmière CIOC), SECC (secrétaire du cabinet CAB), CPT (comptable).
// Dossiers fictifs : pC (patient du cabinet, chimio à HGC), pX (patient du cabinet, sans traitement ailleurs), pH (patient de HGC).
import { readFileSync } from "node:fs";
import { initializeTestEnvironment, assertSucceeds, assertFails } from "@firebase/rules-unit-testing";
import { doc, getDoc, getDocs, setDoc, updateDoc, collection, query, where, serverTimestamp, setLogLevel } from "firebase/firestore";
setLogLevel("silent");

const E = "cabinet-test", P = "espaces/" + E;
const env = await initializeTestEnvironment({ projectId: "demo-onco360", firestore: { rules: readFileSync(new URL("../../firestore.rules", import.meta.url), "utf8"), host: "127.0.0.1", port: 8080 } });
const membre = (role, etabs, droits) => ({ role, actif: true, nom: role, tousEtablissements: etabs === "*", etablissements: etabs === "*" ? [] : etabs, droits });
const dossier = (etab, lt) => Object.assign({ etablissementId: etab, identite: { nom: "FICTIF" }, clinique: {}, lignesJson: "[]", rtsJson: "[]", planningJson: "{}", rdvsJson: "[]", resume: "{}", version: 1, majPar: "MED" }, lt ? { lieuxTraitement: lt } : {});

async function preparer() {
  await env.clearFirestore();
  await env.withSecurityRulesDisabled(async (c) => {
    const db = c.firestore();
    await setDoc(doc(db, P), { titulaire: "MED" });
    const inf = { traitements: "voir", radiotherapie: "voir", administrer: true, planningChimio: false };
    for (const [u, r, e, d] of [["MED", "medecin", "*", { traitements: "modifier", radiotherapie: "modifier", identite: true }], ["INFH", "infirmiere", ["HGC"], inf], ["INFC", "infirmiere", ["CIOC"], inf],
      ["SECC", "assistante", ["CAB"], { rendezvous: true, identite: true }], ["CPT", "comptable", "*", {}]])
      await setDoc(doc(db, P + "/membres/" + u), membre(r, e, d));
    await setDoc(doc(db, P + "/patients/pC"), dossier("CAB", ["HGC"]));
    await setDoc(doc(db, P + "/patients/pX"), dossier("CAB"));
    await setDoc(doc(db, P + "/patients/pH"), dossier("HGC"));
  });
}
const db = (u) => env.authenticatedContext(u).firestore();
const D = (u, p) => doc(db(u), P + "/patients/" + p);
const col = (u) => collection(db(u), P + "/patients");
const maj = (u, o) => Object.assign({ version: 2, maj: serverTimestamp(), majPar: u }, o);

let ok = 0, ko = 0;
async function cas(nom, f) {
  await preparer();
  try { await f(); ok++; console.log("  ✔ " + nom); } catch (e) { ko++; console.log("  ✘ " + nom + "\n      " + (e && e.message ? e.message.split("\n")[0] : e)); }
}

console.log("Lecture");
await cas("l'infirmière HGC lit le dossier du cabinet traité à HGC", () => assertSucceeds(getDoc(D("INFH", "pC"))));
await cas("refusé : l'infirmière HGC lit un dossier du cabinet sans traitement à HGC", () => assertFails(getDoc(D("INFH", "pX"))));
await cas("refusé : l'infirmière CIOC lit le dossier traité à HGC", () => assertFails(getDoc(D("INFC", "pC"))));
await cas("l'infirmière HGC liste les dossiers traités à HGC (requête de l'application)", () => assertSucceeds(getDocs(query(col("INFH"), where("lieuxTraitement", "array-contains-any", ["HGC"])))));
await cas("l'infirmière HGC liste les dossiers modifiés traités à HGC (écoute en direct)", () => assertSucceeds(getDocs(query(col("INFH"), where("lieuxTraitement", "array-contains-any", ["HGC"]), where("maj", ">", new Date(0))))));
await cas("l'infirmière HGC liste toujours les dossiers de HGC", () => assertSucceeds(getDocs(query(col("INFH"), where("etablissementId", "in", ["HGC"])))));
await cas("refusé : l'infirmière HGC liste les dossiers traités à CIOC", () => assertFails(getDocs(query(col("INFH"), where("lieuxTraitement", "array-contains-any", ["CIOC"])))));
await cas("la secrétaire du cabinet lit son patient (traité à HGC)", () => assertSucceeds(getDoc(D("SECC", "pC"))));
await cas("refusé : le comptable", () => assertFails(getDoc(D("CPT", "pC"))));
console.log("Écriture");
await cas("le médecin note les lieux de traitement", () => assertSucceeds(updateDoc(D("MED", "pX"), maj("MED", { lieuxTraitement: ["CIOC"] }))));
await cas("refusé : l'infirmière (sans droit de modifier les traitements) change les lieux de traitement", () => assertFails(updateDoc(D("INFH", "pC"), maj("INFH", { lieuxTraitement: ["HGC", "CIOC"] }))));
await cas("refusé : la secrétaire du cabinet change les lieux de traitement", () => assertFails(updateDoc(D("SECC", "pC"), maj("SECC", { lieuxTraitement: [] }))));
await cas("l'infirmière HGC note l'heure d'une séance du patient traité à HGC", () => assertSucceeds(updateDoc(D("INFH", "pC"), maj("INFH", { heures: { "L1|1|1": { seance: { h: "10:00" } } } }))));
await cas("refusé : l'infirmière HGC écrit dans un dossier du cabinet sans traitement à HGC", () => assertFails(updateDoc(D("INFH", "pX"), maj("INFH", { heures: {} }))));

console.log("\n" + ok + " réussi(s), " + ko + " échec(s)");
await env.cleanup();
process.exit(ko ? 1 : 0);
