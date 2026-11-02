// IG1 (02/11/2026, audit UX : FN1, FN2) : recherche de patient, une seule règle pour la recherche du haut et la page Patients.
// Avant : un mot était cherché n'importe où (aussi au milieu du n° de dossier) et les premiers dossiers de la base étaient gardés :
// « test 80 » proposait TEST 57 à 64 (n° 2026080…) et Entrée ouvrait un autre patient. Maintenant chaque dossier trouvé a un rang
// (0 = le meilleur) et la liste est classée : nom qui commence par le mot, mot entier du nom, n° qui commence par les chiffres, téléphone,
// date de naissance, CIN, puis le reste. Calcul pur (sans DOM ni Firebase) : node tests/moteur/test-cherchepatient.mjs

export const sansAcc = (x) => String(x || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
const chiffres = (x) => String(x || "").replace(/\D/g, "");
// Téléphone : +212 6… ou 00212 6… = 06…
export const telNormal = (x) => { const c = chiffres(x).replace(/^00/, ""); return /^212\d{9}$/.test(c) ? "0" + c.slice(3) : c; };
// Date de naissance AAAA-MM-JJ → JJMMAAAA (« 15/06/1959 », « 15061959 », « 15/06 » retrouvent le patient)
const ddnChiffres = (d) => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(d || "")); return m ? m[3] + m[2] + m[1] : ""; };

// Découpe la recherche en mots ; un numéro écrit avec des espaces ou des tirets (« 06 00 00 00 00 », « +212 600… ») reste un seul mot
export function motsRecherche(q) {
  const t = String(q || "").trim();
  if (!t) return [];
  if (/^[+\d][\d\s.\-/]*$/.test(t) && chiffres(t).length >= 6) return [t.replace(/[\s.\-]/g, "")];
  return sansAcc(t).split(/\s+/).filter(Boolean);
}

// Rang d'un mot dans un dossier (null = absent). f = { nom, num, nums (autres n°), tels, ddn (AAAA-MM-JJ), cin, autres (texte libre) }
export function rangMot(f, w) {
  const nom = sansAcc(f.nom), mots = nom.split(/[\s'’\-]+/).filter(Boolean), r = [];
  if (nom.startsWith(w)) r.push(0);
  if (mots.includes(w)) r.push(0);
  if (mots.some((m) => m.startsWith(w))) r.push(1);
  if (nom.includes(w)) r.push(3);
  const c = chiffres(w), seulChiffres = c && /^[+\d][\d/]*$/.test(w);
  if (seulChiffres) {
    const nums = [f.num].concat(f.nums || []).map(chiffres).filter(Boolean);
    if (nums.some((n) => n === c)) r.push(0);
    if (nums.some((n) => n.startsWith(c))) r.push(1);
    const tc = telNormal(w);
    if (tc.length >= 6) (f.tels || []).map(telNormal).filter(Boolean).forEach((t) => { if (t === tc) r.push(0); else if (t.startsWith(tc) || t.replace(/^0/, "").startsWith(tc.replace(/^0/, ""))) r.push(1); else if (t.includes(tc.replace(/^0/, ""))) r.push(2); });
    const dd = ddnChiffres(f.ddn);
    if (dd && c.length >= 4 && (w.includes("/") || c.length === 8)) { if (dd === c) r.push(0); else if (dd.startsWith(c)) r.push(1); }
    if (c.length >= 3 && nums.some((n) => n.includes(c))) r.push(4);
  }
  const cin = sansAcc(f.cin).replace(/\s/g, "");
  if (cin && w.length >= 2) { if (cin === w) r.push(0); else if (cin.startsWith(w)) r.push(1); }
  if (f.autres && sansAcc(f.autres).includes(w)) r.push(3);
  return r.length ? Math.min(...r) : null;
}

// Rang d'un dossier pour toute la recherche : somme des rangs des mots (null si un mot manque)
export function rangPatient(f, mots) {
  let s = 0;
  for (const w of mots) { const r = rangMot(f, w); if (r == null) return null; s += r; }
  return s;
}

// Classe les dossiers : liste de { x, f } (f = champs ci-dessus) → [x…] trouvés, les meilleurs d'abord (à rang égal, ordre alphabétique du nom)
export function chercherPatients(liste, q) {
  const mots = motsRecherche(q);
  if (!mots.length) return liste.map((e) => e.x);
  return liste.map((e, i) => ({ e, i, r: rangPatient(e.f, mots) })).filter((z) => z.r != null)
    .sort((a, b) => a.r - b.r || sansAcc(a.e.f.nom).localeCompare(sansAcc(b.e.f.nom), "fr", { numeric: true }) || a.i - b.i).map((z) => z.e.x);
}

// Parties du nom à surligner (pour l'affichage) : [[début, fin]…] des mots trouvés dans le nom
export function partiesTrouvees(nom, q) {
  const n = sansAcc(nom), out = [];
  motsRecherche(q).forEach((w) => { if (!/[a-z]/.test(w) && !/^\d+$/.test(w)) return; let i = n.indexOf(w); if (i >= 0) out.push([i, i + w.length]); });
  return out.sort((a, b) => a[0] - b[0]).filter((p, k, l) => !k || p[0] >= l[k - 1][1]);
}
