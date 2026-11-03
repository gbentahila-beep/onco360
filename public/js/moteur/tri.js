// IG5 (03/11/2026, audit UX, idée 11 ; FN5) : tri d'un tableau au clic sur le titre d'une colonne. Calcul pur : node tests/moteur/test-tri.mjs
// val(x) → texte, nombre ou date AAAA-MM-JJ ; sens 1 (▲) ou -1 (▼) ; cases vides toujours en dernier ; à égalité, l'ordre d'avant est gardé.
export function trierPar(liste, val, sens) {
  const s = sens < 0 ? -1 : 1, vide = (v) => v == null || v === "" || (typeof v === "number" && isNaN(v));
  return liste.map((x, i) => ({ x, i, v: val(x) })).sort((a, b) => {
    const va = vide(a.v), vb = vide(b.v);
    if (va || vb) return va - vb || a.i - b.i;
    const c = typeof a.v === "number" && typeof b.v === "number" ? a.v - b.v : String(a.v).localeCompare(String(b.v), "fr", { numeric: true, sensitivity: "base" });
    return c * s || a.i - b.i;
  }).map((z) => z.x);
}
// Clic suivant sur une colonne : ▲, puis ▼, puis l'ordre par défaut ; autre colonne : ▲
export const triSuivant = (t, k) => (!t || t.k !== k ? { k, s: 1 } : t.s > 0 ? { k, s: -1 } : { k: "", s: 0 });
