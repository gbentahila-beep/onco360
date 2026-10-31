// Tests des règles de l'acceptation des conditions générales (utilisateurs/{uid}.cgu, L0 du 31/10/2026) sur l'émulateur Firestore.
// Lancer (Java 21 nécessaire) :  cd tests/regles && npm test
import { readFileSync } from "node:fs";
import { initializeTestEnvironment, assertSucceeds, assertFails } from "@firebase/rules-unit-testing";
import { doc, setDoc, updateDoc, serverTimestamp, setLogLevel } from "firebase/firestore";
setLogLevel("silent");

const env = await initializeTestEnvironment({ projectId: "demo-onco360", firestore: { rules: readFileSync(new URL("../../firestore.rules", import.meta.url), "utf8"), host: "127.0.0.1", port: 8080 } });
const cgu = (le) => ({ version: "1.0", le, email: "a@test.ma", espace: "cabinet-test", cabinet: "Cabinet test" });
async function preparer() {
  await env.clearFirestore();
  await env.withSecurityRulesDisabled(async (c) => {
    const db = c.firestore();
    await setDoc(doc(db, "utilisateurs/DEJA"), { nom: "Déjà", cgu: cgu("2026-10-31T09:00:00Z") });
    await setDoc(doc(db, "utilisateurs/VIDE"), { nom: "Vide" });
  });
}
const db = (u) => env.authenticatedContext(u).firestore();
let ok = 0, ko = 0;
async function cas(nom, f) {
  await preparer();
  try { await f(); ok++; console.log("  ✔ " + nom); } catch (e) { ko++; console.log("  ✘ " + nom + "\n      " + (e && e.message ? e.message.split("\n")[0] : e)); }
}
console.log("Conditions générales");
await cas("la personne accepte, date du serveur", () => assertSucceeds(setDoc(doc(db("VIDE"), "utilisateurs/VIDE"), { cgu: cgu(serverTimestamp()) }, { merge: true })));
await cas("première acceptation à la création du profil", () => assertSucceeds(setDoc(doc(db("NEUF"), "utilisateurs/NEUF"), { cgu: cgu(serverTimestamp()) })));
await cas("refusé : date choisie par le navigateur", () => assertFails(setDoc(doc(db("VIDE"), "utilisateurs/VIDE"), { cgu: cgu("2026-01-01T00:00:00Z") }, { merge: true })));
await cas("le reste du profil se modifie sans toucher l'acceptation", () => assertSucceeds(updateDoc(doc(db("DEJA"), "utilisateurs/DEJA"), { nom: "Déjà 2" })));
await cas("nouvelle version acceptée", () => assertSucceeds(updateDoc(doc(db("DEJA"), "utilisateurs/DEJA"), { cgu: Object.assign(cgu(serverTimestamp()), { version: "1.1" }) })));
await cas("refusé : acceptation écrite pour quelqu'un d'autre", () => assertFails(setDoc(doc(db("DEJA"), "utilisateurs/VIDE"), { cgu: cgu(serverTimestamp()) }, { merge: true })));
console.log((ko ? "✘ " : "✔ ") + ok + " réussis, " + ko + " en échec");
await env.cleanup();
process.exit(ko ? 1 : 0);
