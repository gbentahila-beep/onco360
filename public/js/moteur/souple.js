// IG5 (03/11/2026, audit UX : FN3, FN4) : recherche souple, une seule règle pour Protocoles, Nouvelle ligne (chimio) et Médic.
// Tirets, espaces, points, apostrophes, accents et majuscules ignorés (5FU = 5-FU = 5 fu), synonymes (Taxol = paclitaxel, CDDP = cisplatine),
// et les mots séparés par des espaces peuvent aussi se lire ensemble (« 5 fu cisplatine » : « 5 fu » puis « cisplatine »).
// Calcul pur (sans DOM ni Firebase) : node tests/moteur/test-souple.mjs
import { SYNONYMES } from "../donnees/synonymes.js";

export const plat = (x) => String(x || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/œ/g, "oe").replace(/[\s\-_.,;:/'’()+]/g, "");

// Index : nom aplati → groupe (noms aplatis, nom affiché)
let INDEX = null;
function index(table) {
  const m = new Map();
  (table || SYNONYMES).forEach((g) => { const L = [...new Set(g.map(plat).filter(Boolean))]; L.forEach((k) => { if (!m.has(k)) m.set(k, { L, nom: g[0] }); }); });
  return m;
}
const idx = (table) => (table ? index(table) : (INDEX = INDEX || index()));

// Variantes d'un morceau de recherche (déjà aplati) : lui-même et ses synonymes
export function variantes(w, table) { const g = idx(table).get(w); return g ? g.L : [w]; }

// Découpe la recherche en mots (espaces) ; chaque mot aplati
const motsDe = (q) => String(q || "").trim().split(/\s+/).map(plat).filter(Boolean);

// Le texte (déjà aplati) contient-il toute la recherche ? Les mots se lisent seuls ou collés à leurs voisins (jusqu'à 3)
function couvre(t, mots, i, table) {
  if (i >= mots.length) return true;
  for (let n = Math.min(3, mots.length - i); n >= 1; n--) {
    const w = mots.slice(i, i + n).join("");
    if (variantes(w, table).some((v) => t.includes(v)) && couvre(t, mots, i + n, table)) return true;
  }
  return false;
}

// Prépare une recherche : { vide, test(texte), aussi: noms des synonymes cherchés en plus (pour « Cherché aussi : … ») }
export function recherche(q, table) {
  const mots = motsDe(q);
  const aussi = [];
  for (let i = 0; i < mots.length; i++) for (let n = 1; n <= Math.min(3, mots.length - i); n++) {
    const w = mots.slice(i, i + n).join(""), g = idx(table).get(w);
    if (g && plat(g.nom) !== w && aussi.indexOf(g.nom) < 0) aussi.push(g.nom);
  }
  return { vide: !mots.length, mots, aussi, test: (texte) => !mots.length || couvre(plat(texte), mots, 0, table) };
}

// Ligne « Cherché aussi : … » (texte seul, à échapper par l'appelant) ; vide si aucun synonyme
export const chercheAussi = (r) => (r && r.aussi.length ? "Cherché aussi : " + r.aussi.join(", ") : "");
