const U = window.__uid ? { uid: window.__uid, email: window.__uid.toLowerCase() + "@test.ma" } : { uid: "UIDRITA", email: "ritabentahila@gmail.com" }; // window.__uid : autre membre (tests)
export function getAuth() { return { currentUser: U }; }
export function onAuthStateChanged(a, f) { setTimeout(() => f(window.__deconnecte ? null : U), 0); return () => {}; } // window.__deconnecte : page de connexion (test_lot_l)
export async function signOut() {}
export async function createUserWithEmailAndPassword(a, e) { return { user: { uid: "U" + Math.random().toString(36).slice(2, 8), email: e } }; }
export async function sendPasswordResetEmail() {}
export async function updatePassword() {}
export async function reauthenticateWithCredential() {}
export const EmailAuthProvider = { credential: () => ({}) };
export const browserLocalPersistence = { type: "LOCAL" };
export const browserSessionPersistence = { type: "SESSION" };
export async function setPersistence(a, p) { window.__persistance = p && p.type; }
export async function signInWithEmailAndPassword() {}
// L0 (31/10/2026) : conditions générales déjà acceptées par la personne connectée (version lue dans js/donnees/cgu.js par base.py,
// window.__cguV) ; window.__cguVierge = true : pas encore acceptées (test_lot_l)
if (window.__fs && window.__cguV && !window.__cguVierge) { const k = "utilisateurs/" + U.uid; const v = window.__fs[k] || {}; if (!v.cgu) window.__fs[k] = Object.assign({}, v, { cgu: { version: window.__cguV } }); }
