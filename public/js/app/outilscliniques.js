// ───── Espace « Outils cliniques » (lot RT.13 à RT.17, 31/10/2026, demande de Dr Bentahila) ─────
// Menu « Outils cliniques » sous Radiothérapie (module « outils ») ; menu à gauche comme Paramètres : Stadification, Échelles de toxicité, Calculateurs ;
// chaque outil avec sa source et l'avertissement en dessous. Modèle d'organisation : RadOnc Toolbox (ASTRO), sans en recopier ni le dessin ni les textes.
// Données du cabinet (bibliotheques, écrites par le médecin) : tnm (index) et tnm_<sous-localisation> (tableaux remplis depuis le manuel),
// ctcae (version, termes « tardive ») et ctcae_0…n (fichier du NCI importé), esperanceVie (table de mortalité). Calculs : moteur/calculs.js.
import { doc, getDoc, setDoc, runTransaction } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";
import { getStorage, ref as sref, uploadBytesResumable, getBlob } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-storage.js";
import { db, app } from "../config.js";
import * as C from "../moteur/calculs.js";
import { TNM_LOCS, sousTnm, tnmVide, CTCAE_TARDIFS0, CTCAE_V6, CTCAE_SITE, GROUPES_CALC, CALCS, PS, KARNOFSKY, AVERT_OUTILS } from "../donnees/outilscliniques.js";

let A = null;
export function installer(api) { A = api; }
const $ = (id) => document.getElementById(id);
const esc = (s) => A.esc(s == null ? "" : String(s));
const AVERT = () => '<p class="avert-ind">' + AVERT_OUTILS + "</p>";
const ref = (k) => doc(db, "espaces", A.ESPACE, "bibliotheques", k);
const peutEcrire = () => !!(A.estMed() && A.peut("ecrireConsultations"));
const signe = () => ({ majPar: A.D().u.uid, majParNom: $("nomMenu") ? $("nomMenu").textContent : "", majLe: new Date().toISOString() });
const fmt = (v, n = 1) => (v == null || !isFinite(v) ? "—" : Number(v).toLocaleString("fr-FR", { maximumFractionDigits: n }).replace(/[  ]/g, " "));
const ST = { sec: "tnm", arg: "", tnm: null, sousC: {}, ctcae: null, ctOng: "aigue", ctQ: "", ctSoc: "", esp: null, ed: null, ong: "c" };

// ───── Mise en page : menu à gauche (familles et outils), page à droite ─────
const FAMS = [["tnm", "liste", "Stadification"], ["ctcae", "alerte", "Échelles de toxicité"], ["calc", "courbe", "Calculateurs"]];
function menu() {
  const sous = ST.sec === "calc" ? GROUPES_CALC.map(([g, lg]) => '<div class="oc-gr">' + esc(lg) + "</div>" + CALCS.filter((c) => c[2] === g).map((c) => '<button class="' + (ST.arg === c[0] ? "on" : "") + '"' + (ST.arg === c[0] ? ' aria-current="page"' : "") + ' onclick="location.hash=\'outils/calc/' + c[0] + "'\">" + esc(c[1]) + "</button>").join("")).join("")
    : ST.sec === "tnm" ? TNM_LOCS.map((l) => '<button class="' + (ST.arg === l.id ? "on" : "") + '" onclick="location.hash=\'outils/tnm/' + l.id + "'\">" + esc(l.nom) + "</button>").join("") : "";
  return '<aside class="cf-nav oc-nav" aria-label="Outils cliniques"><div class="cf-nav-t">Outils cliniques</div><div class="cf-fam" role="tablist">' +
    FAMS.map(([k, ico, lib]) => '<div class="cf-g' + (ST.sec === k ? " ouv" : "") + '"><button role="tab" aria-selected="' + (ST.sec === k) + '" class="cf-gt' + (ST.sec === k ? " on" : "") + '" onclick="location.hash=\'outils/' + k + "'\">" + A.ic(ico) + "<span>" + lib + "</span></button>" +
      (ST.sec === k && sous ? '<nav class="cf-sous oc-sous" aria-label="' + lib + '">' + sous + "</nav>" : "") + "</div>").join("") + "</div></aside>";
}
export async function pageOutils(arg) {
  const p = String(arg || "").split("/"); ST.sec = FAMS.some((f) => f[0] === p[0]) ? p[0] : "tnm"; ST.arg = p.slice(1).join("/"); ST.ed = null;
  if (ST.sec === "calc" && !CALCS.some((c) => c[0] === ST.arg)) ST.arg = "";
  $("page").innerHTML = '<div class="cf-lay oc-lay">' + menu() + '<div class="cf-main oc-main" id="ocMain"><div class="vide-c">Chargement…</div></div></div>';
  try { if (ST.sec === "tnm") await pageTnm(); else if (ST.sec === "ctcae") await pageCtcae(); else await pageCalc(); }
  catch (e) { console.warn("outils cliniques", e); $("ocMain").innerHTML = '<div class="vide-c">Pas de connexion : réessayez.</div>'; }
}
const carteSec = (titre, corps, source) => '<section class="carte oc-c"><h2>' + esc(titre) + "</h2>" + corps + (source ? '<p class="mesures oc-src">Source : ' + source + "</p>" : "") + AVERT() + "</section>";

// ───── RT.14 Stadification TNM ─────
async function lireIndex() { if (!ST.tnm) { const s = await getDoc(ref("tnm")); ST.tnm = s.exists() ? s.data() : { remplis: {} }; ST.tnm.remplis = ST.tnm.remplis || {}; } return ST.tnm; }
async function pageTnm() {
  const [loc, sous] = ST.arg.split("/"); const I = await lireIndex();
  if (sous) return ficheTnm(sous);
  const L = TNM_LOCS.filter((l) => !loc || l.id === loc);
  $("ocMain").innerHTML = carteSec("Stadification TNM", '<p class="sous">Choisissez la localisation, puis la sous-localisation. Les tableaux (cTNM, pTNM, stades, tableaux annexes) sont ceux de votre manuel de référence (AJCC, dernière édition), saisis une fois par le médecin : ils ne sont pas recopiés dans Onco360.</p>' +
    (peutEcrire() ? '<div class="actr" style="justify-content:flex-start"><label class="bt clair petit oc-imp">' + A.ic("plus") + 'Importer des tableaux (fichier)<input type="file" accept="application/json,.json" onchange="ocTnmImport(this)" hidden></label></div>' : "") +
    '<div class="oc-filtre"><label for="ocLoc">Localisation</label><select id="ocLoc" onchange="location.hash=\'outils/tnm\'+(this.value?\'/\'+this.value:\'\')"><option value="">Toutes</option>' + TNM_LOCS.map((l) => '<option value="' + l.id + '"' + (l.id === loc ? " selected" : "") + ">" + esc(l.nom) + "</option>").join("") + "</select></div>" +
    L.map((l) => "<h3 class=\"oc-h3\">" + esc(l.nom) + '</h3><div class="oc-cartes">' + l.sous.map(([id, nom]) => { const r = I.remplis[id];
      return '<button type="button" class="oc-carte" onclick="location.hash=\'outils/tnm/' + l.id + "/" + id + "'\"><b>" + esc(nom) + '</b><span class="badge ' + (r ? "b-ch" : "b-gr") + '">' + (r ? "Rempli" + (r.edition ? " · " + esc(r.edition) : "") : "À remplir") + "</span></button>"; }).join("") + "</div>").join(""), "AJCC Cancer Staging Manual (dernière édition), tableaux saisis par le cabinet");
}
async function lireSous(id) { if (!ST.sousC[id]) { const s = await getDoc(ref("tnm_" + id)); ST.sousC[id] = s.exists() ? Object.assign(tnmVide(), s.data()) : tnmVide(); } return ST.sousC[id]; }
const TCOLS = [["t", "T", "Tumeur primitive (T)"], ["n", "N", "Ganglions régionaux (N)"], ["m", "M", "Métastases à distance (M)"]];
const vide = (F) => !["c", "p"].some((k) => TCOLS.some(([c]) => (F[k][c] || []).length) || (F[k].stades || []).length) && !(F.annexes || []).length;
async function ficheTnm(id) {
  const s = sousTnm(id); if (!s) { location.hash = "outils/tnm"; return; }
  const F0 = await lireSous(id), ed = ST.ed && ST.ed.id === id ? ST.ed : null, F = ed ? ed.F : F0, k = ST.ong, P = F[k];
  const tab = (rows, cols, key, ph) => ed ? edTable(key, cols, rows, ph) : rows.length ? '<div class="tableau"><table class="lc oc-t"><thead><tr>' + cols.map((c) => "<th>" + esc(c[1]) + "</th>").join("") + "</tr></thead><tbody>" + rows.map((r) => "<tr>" + cols.map((c, i) => '<td data-l="' + esc(c[1]) + '"' + (i ? "" : ' class="oc-k"') + ">" + esc(r[c[0]] || "") + "</td>").join("") + "</tr>").join("") + "</tbody></table></div>" : '<p class="mesures">À remplir.</p>';
  const opts = (c) => '<option value="">—</option>' + (P[c] || []).map((r) => '<option value="' + esc(r.cat) + '">' + esc(r.cat) + "</option>").join("");
  let h = '<button class="mini oc-ret" onclick="location.hash=\'outils/tnm/' + s.loc.id + "'\">" + A.ic("retour") + esc(s.loc.nom) + "</button>" +
    '<div class="oc-tete"><h2>' + esc(s.nom) + "</h2>" + (ed ? "" : peutEcrire() ? '<button class="bt clair petit" onclick="ocTnmModif(\'' + id + "')\">" + A.ic("crayon") + "Modifier</button>" : "") + "</div>" +
    (ed ? '<div class="form oc-src2"><div><label for="ocSrc">Source</label><input id="ocSrc" data-tf="source" value="' + esc(F.source) + '"></div><div><label for="ocEd">Édition</label><input id="ocEd" data-tf="edition" value="' + esc(F.edition) + '" placeholder="ex. 9e édition, 2024"></div></div>'
      : '<p class="mesures">Source : ' + esc([F.source, F.edition].filter(Boolean).join(", ") || "à préciser") + (F.majParNom ? " · saisi par " + esc(F.majParNom) + (F.majLe ? " le " + A.dfrA(String(F.majLe).slice(0, 10)) : "") : "") + "</p>") +
    // 31/10/2026 : les pages du manuel du cabinet (son propre exemplaire, PDF) jointes à la sous-localisation, consultables à côté des tableaux
    (ed ? "" : '<div class="actr oc-pdf" style="justify-content:flex-start">' + (F.pdf ? '<button class="bt clair petit" onclick="ocTnmPdf(\'' + id + '\')">' + A.ic("document") + "Pages du manuel (PDF)</button>" : "") +
      (peutEcrire() ? '<label class="bt clair petit oc-imp">' + A.ic("plus") + (F.pdf ? "Remplacer le PDF" : "Joindre les pages de votre manuel (PDF)") + '<input type="file" accept="application/pdf" onchange="ocTnmPdfAj(\'' + id + '\',this)" hidden></label>' : "") + "</div>") +
    '<div class="ag-vues oc-ong" role="tablist">' + [["c", "cTNM (clinique)"], ["p", "pTNM (pathologique)"]].map(([o, l]) => '<button role="tab" aria-selected="' + (o === k) + '" class="' + (o === k ? "on" : "") + '" onclick="ocTnmOng(\'' + o + "')\">" + l + "</button>").join("") + "</div>";
  if (!ed && vide(F)) h += A.etatVide({ ill: "document", titre: "Tableaux à remplir", txt: "Saisissez les catégories T, N, M et les groupes de stades depuis votre manuel de référence (AJCC, dernière édition) : ils serviront au calcul du stade.", bouton: peutEcrire() ? '<button class="bt plein" onclick="ocTnmModif(\'' + id + '\')">' + A.ic("crayon") + "Remplir les tableaux</button>" : "" });
  else {
    h += TCOLS.map(([c, , lib]) => '<h3 class="oc-h3">' + lib + "</h3>" + tab(P[c] || [], [["cat", "Catégorie"], ["def", "Définition"]], k + "." + c, ["T1", ""])).join("");
    if (!ed && (P.stades || []).length) h += '<div class="oc-calc"><h3 class="oc-h3">Calcul du stade</h3><div class="form oc-f3">' + TCOLS.map(([c, l]) => '<div><label for="ocS' + c + '">' + l + '</label><select id="ocS' + c + '" onchange="ocStade()">' + opts(c) + "</select></div>").join("") + '</div><p class="oc-res" id="ocStadeR" aria-live="polite">Choisissez T, N et M.</p></div>';
    h += '<h3 class="oc-h3">Groupes de stades</h3>' + tab(P.stades || [], [["stade", "Stade"], ["t", "T"], ["n", "N"], ["m", "M"], ["autre", "Autres critères"]], k + ".stades", ["IA", "tout"]);
    h += '<h3 class="oc-h3">Tableaux annexes</h3>' + (F.annexes || []).map((a, i) => ed ? '<div class="oc-ann"><div class="oc-annt"><input class="rtr-in" data-tf="annexes.' + i + '.titre" value="' + esc(a.titre) + '" aria-label="Titre du tableau" placeholder="Titre du tableau"><button type="button" class="rtr-sup" onclick="ocAnn(' + i + ')" aria-label="Retirer ce tableau" title="Retirer">' + A.ic("corbeille") + "</button></div>" + edTable("annexes." + i + ".lignes", [["a", "Colonne 1"], ["b", "Colonne 2"]], a.lignes || []) + "</div>"
      : "<h4>" + esc(a.titre) + "</h4>" + tab(a.lignes || [], [["a", ""], ["b", ""]].map((c, j) => [c[0], j ? "" : ""]), "")).join("") +
      (ed ? '<button type="button" class="mini rtr-aj" onclick="ocAnn()">' + A.ic("plus") + "Ajouter un tableau annexe</button>" : (F.annexes || []).length ? "" : '<p class="mesures">Aucun.</p>');
  }
  if (ed) h += '<div class="barre-enr"><button class="bt gris" onclick="ocTnmAnnuler()">Annuler</button><span></span><button class="bt plein" id="ocTnmOk" onclick="ocTnmOk(\'' + id + "')\">" + A.ic("enregistrer") + "Enregistrer</button></div>";
  $("ocMain").innerHTML = '<section class="carte oc-c">' + h + '<p class="mesures oc-src">Source : ' + esc([F.source, F.edition].filter(Boolean).join(", ") || "AJCC Cancer Staging Manual") + " (tableaux saisis par le cabinet)</p>" + AVERT() + "</section>";
}
// UX10 (01/11/2026) : import d'un fichier de tableaux préparé depuis le manuel du cabinet ({ "<sous-localisation>": fiche au format tnmVide }) ;
// écrit dans le cabinet seulement (bibliotheques/tnm_<id> + index), après confirmation ; les fiches déjà remplies sont remplacées
window.ocTnmImport = async (inp) => {
  const f = inp.files && inp.files[0]; inp.value = ""; if (!f || !peutEcrire()) return;
  let J; try { J = JSON.parse(await f.text()); } catch (e) { A.toast("Fichier illisible"); return; }
  const ok = (F) => F && typeof F === "object" && ["c", "p"].every((k) => F[k] && ["t", "n", "m", "stades"].every((c) => Array.isArray(F[k][c])));
  const ids = Object.keys(J || {}).filter((id) => sousTnm(id) && ok(J[id]));
  if (!ids.length) { A.toast("Aucune fiche reconnue dans ce fichier"); return; }
  const I = await lireIndex(), deja = ids.filter((id) => I.remplis[id]);
  const r = await A.question("<h3>Importer " + ids.length + " fiche" + (ids.length > 1 ? "s" : "") + " ?</h3><p>" + esc(ids.map((id) => sousTnm(id).nom).join(", ")) + ".</p>" + (deja.length ? "<p><b>" + deja.length + " fiche" + (deja.length > 1 ? "s" : "") + " déjà remplie" + (deja.length > 1 ? "s seront remplacées" : " sera remplacée") + ".</b></p>" : ""), [["non", "Annuler"], ["oui", "Importer", "plein"]]);
  if (r !== "oui") return;
  const tx = (L) => (L || []).map((x) => { const o = {}; Object.keys(x || {}).forEach((k) => { if (String(x[k] || "").trim()) o[k] = String(x[k]).trim(); }); return o; }).filter((o) => Object.keys(o).length);
  try {
    for (const id of ids) {
      const F = J[id], d = { source: String(F.source || "").trim(), edition: String(F.edition || "").trim(), note: String(F.note || ""), annexes: (F.annexes || []).map((a) => ({ titre: String(a.titre || "").trim(), lignes: tx(a.lignes) })) };
      ["c", "p"].forEach((k) => { d[k] = {}; ["t", "n", "m", "stades"].forEach((c) => { d[k][c] = tx(F[k][c]); }); });
      Object.assign(d, signe());
      const s = await getDoc(ref("tnm_" + id)); if (s.exists() && s.data().pdf) d.pdf = s.data().pdf;
      await setDoc(ref("tnm_" + id), d); ST.sousC[id] = Object.assign(tnmVide(), d);
    }
    await runTransaction(db, async (t) => { const s = await t.get(ref("tnm")), X = s.exists() ? s.data() : { remplis: {} }; X.remplis = Object.assign({}, X.remplis || {}); ids.forEach((id) => { X.remplis[id] = { edition: String(J[id].edition || ""), le: new Date().toISOString() }; }); t.set(ref("tnm"), Object.assign(X, signe())); ST.tnm = X; });
  } catch (e) { A.toast(e && e.code === "permission-denied" ? "Seul le médecin modifie les tableaux." : "Pas de connexion : réessayez"); return; }
  A.toast(ids.length + " fiche" + (ids.length > 1 ? "s importées" : " importée")); pageTnm();
};
// Tableau modifiable (lignes ajoutées, retirées) : data-tr = chemin de la liste, data-ti = rang, data-tc = colonne
function edTable(key, cols, rows, ph) {
  return '<div class="tableau"><table class="lc oc-t oc-ed"><thead><tr>' + cols.map((c) => "<th>" + esc(c[1]) + "</th>").join("") + "<th></th></tr></thead><tbody>" +
    rows.map((r, i) => "<tr>" + cols.map((c, j) => '<td data-l="' + esc(c[1]) + '">' + (c[0] === "def" || c[0] === "autre" || c[0] === "b" ? '<textarea class="rtr-in" rows="1" data-tr="' + key + '" data-ti="' + i + '" data-tc="' + c[0] + '" aria-label="' + esc(c[1]) + '">' + esc(r[c[0]] || "") + "</textarea>" : '<input class="rtr-in" data-tr="' + key + '" data-ti="' + i + '" data-tc="' + c[0] + '" value="' + esc(r[c[0]] || "") + '" aria-label="' + esc(c[1]) + '"' + (ph && ph[j] ? ' placeholder="' + esc(ph[j]) + '"' : "") + ">") + "</td>").join("") +
      '<td><button type="button" class="rtr-sup" onclick="ocLigne(\'' + key + "'," + i + ')" aria-label="Retirer cette ligne" title="Retirer">' + A.ic("croix") + "</button></td></tr>").join("") +
    '</tbody></table></div><button type="button" class="mini rtr-aj" onclick="ocLigne(\'' + key + '\')">' + A.ic("plus") + "Ajouter une ligne</button>";
}
const chemin = (o, p) => p.split(".").reduce((x, k) => (x == null ? x : x[k]), o);
window.ocTnmOng = (o) => { ST.ong = o; ficheTnm(ST.arg.split("/")[1]); };
window.ocTnmModif = async (id) => { if (!peutEcrire()) return; const F = JSON.parse(JSON.stringify(await lireSous(id)));
  ["c", "p"].forEach((k) => { F[k] = F[k] || {}; ["t", "n", "m", "stades"].forEach((c) => { if (!(F[k][c] || []).length) F[k][c] = [{}]; }); }); // une ligne vide à remplir
  ST.ed = { id, F }; ficheTnm(id); };
window.ocTnmAnnuler = () => { const id = ST.ed && ST.ed.id; ST.ed = null; if (id) ficheTnm(id); };
window.ocLigne = (key, i) => { if (!ST.ed) return; const p = key.split("."), F = ST.ed.F; let L = chemin(F, key); if (!L) { const par = chemin(F, p.slice(0, -1).join(".")); L = par[p[p.length - 1]] = []; } if (i == null) L.push({}); else L.splice(i, 1); ficheTnm(ST.ed.id); };
window.ocAnn = (i) => { if (!ST.ed) return; const A2 = ST.ed.F.annexes = ST.ed.F.annexes || []; if (i == null) A2.push({ titre: "", lignes: [{}] }); else A2.splice(i, 1); ficheTnm(ST.ed.id); };
document.addEventListener("input", (ev) => { const t = ev.target; if (!ST.ed || !t.dataset) return;
  if (t.dataset.tr != null) { const L = chemin(ST.ed.F, t.dataset.tr); if (L && L[Number(t.dataset.ti)]) L[Number(t.dataset.ti)][t.dataset.tc] = t.value; }
  else if (t.dataset.tf) { const p = t.dataset.tf.split("."), o = chemin(ST.ed.F, p.slice(0, -1).join(".")) || ST.ed.F; if (p.length === 1) ST.ed.F[p[0]] = t.value; else if (o) o[p[p.length - 1]] = t.value; } });
window.ocTnmOk = async (id) => {
  if (!ST.ed || !peutEcrire()) return;
  const net = (L) => (L || []).filter((r) => Object.values(r).some((v) => String(v || "").trim())).map((r) => { const x = {}; Object.keys(r).forEach((k) => { if (String(r[k] || "").trim()) x[k] = String(r[k]).trim(); }); return x; });
  const F = ST.ed.F, d = { source: String(F.source || "").trim(), edition: String(F.edition || "").trim(), note: F.note || "", annexes: (F.annexes || []).map((a) => ({ titre: String(a.titre || "").trim(), lignes: net(a.lignes) })).filter((a) => a.titre || a.lignes.length) };
  ["c", "p"].forEach((k) => { d[k] = {}; ["t", "n", "m", "stades"].forEach((c) => { d[k][c] = net(F[k] && F[k][c]); }); });
  Object.assign(d, signe());
  A.occupe($("ocTnmOk"), true);
  try {
    await setDoc(ref("tnm_" + id), d);
    await runTransaction(db, async (tx) => { const s = await tx.get(ref("tnm")), I = s.exists() ? s.data() : { remplis: {} }; I.remplis = Object.assign({}, I.remplis || {}); if (vide(d)) delete I.remplis[id]; else I.remplis[id] = { edition: d.edition, le: d.majLe }; tx.set(ref("tnm"), Object.assign(I, signe())); ST.tnm = I; });
  } catch (e) { A.occupe($("ocTnmOk"), false); A.toast(e && e.code === "permission-denied" ? "Seul le médecin modifie les tableaux." : "Pas de connexion : réessayez"); return; }
  ST.sousC[id] = Object.assign(tnmVide(), d); ST.ed = null; A.toast("Enregistré"); ficheTnm(id);
};
window.ocStade = () => {
  const id = ST.arg.split("/")[1], F = ST.sousC[id]; if (!F) return; const v = TCOLS.map(([c]) => A.val("ocS" + c)), z = $("ocStadeR");
  if (v.some((x) => !x)) { z.textContent = "Choisissez T, N et M."; return; }
  const r = C.stadeTnm(F[ST.ong].stades, v[0], v[1], v[2]);
  z.innerHTML = r.length ? "Stade : <b>" + esc([...new Set(r)].join(" ou ")) + "</b>" + (F[ST.ong].stades.some((x) => x.autre && r.indexOf(x.stade) >= 0) ? ' <span class="mesures">(voir les autres critères du tableau)</span>' : "") : "Aucun groupe de stades ne correspond dans le tableau.";
};

// ───── RT.15 Échelles de toxicité CTCAE (fichier du NCI importé par le médecin) ─────
async function lireCtcae() {
  if (ST.ctcae) return ST.ctcae;
  // CTCAE v6.0 fourni avec Onco360 (donnees-outils/ctcae-v6.json) ; un fichier importé par le cabinet (bibliotheques/ctcae, ctcae_0…) le remplace ;
  // les termes « tardive » du cabinet sont gardés dans bibliotheques/ctcae dans les deux cas
  const s = await getDoc(ref("ctcae")), M = s.exists() ? s.data() : {};
  let termes = [];
  if (M.parts) { const parts = await Promise.all(Array.from({ length: M.parts }, (_, i) => getDoc(ref("ctcae_" + i)))); termes = [].concat(...parts.map((p) => (p.exists() ? JSON.parse(p.data().data || "[]") : []))); }
  if (!termes.length) { const r = await fetch(CTCAE_V6.fichier, { cache: "no-cache" }); if (!r.ok) return (ST.ctcae = { vide: true }); termes = await r.json(); Object.assign(M, { version: CTCAE_V6.version, fourni: true, majParNom: "", majLe: "" }); }
  return (ST.ctcae = Object.assign({}, M, { termes, tardifs: Array.isArray(M.tardifs) ? M.tardifs : CTCAE_TARDIFS0 }));
}
async function pageCtcae() {
  const D = await lireCtcae(), imp = peutEcrire() ? '<label class="bt clair petit oc-imp">' + A.ic("telecharger") + 'Importer une autre version (Excel du NCI)<input type="file" accept=".xlsx,.xls,.csv" onchange="ocCtImport(this)" hidden></label>' : "";
  const src = 'Common Terminology Criteria for Adverse Events (CTCAE), National Cancer Institute (domaine public) : <a href="' + CTCAE_SITE + '" target="_blank" rel="noopener">site du NCI</a>';
  if (D.vide) { $("ocMain").innerHTML = carteSec("Échelles de toxicité (CTCAE)", '<p class="sous">Les grades 0 à 5 de chaque effet indésirable, d\'après le fichier officiel du NCI (version 6.0, ou 5.0). Téléchargez le fichier Excel sur le site du NCI, puis importez-le ici une fois : toute l\'équipe le consulte ensuite.</p>' + (imp ? '<div class="actr" style="justify-content:flex-start">' + imp + "</div>" : '<p class="mesures">Le médecin importe le fichier.</p>'), src); return; }
  const socs = [...new Set(D.termes.map((t) => t.soc).filter(Boolean))].sort((a, b) => a.localeCompare(b));
  $("ocMain").innerHTML = '<section class="carte oc-c"><div class="oc-tete"><h2>Échelles de toxicité (CTCAE ' + esc(D.version || "") + ")</h2>" + imp + '</div><p class="mesures">' + D.termes.length + " termes · " + (D.fourni ? "fourni avec Onco360 (PDF officiel du NCI)" : "importé" + (D.majParNom ? " par " + esc(D.majParNom) : "") + (D.majLe ? " le " + A.dfrA(String(D.majLe).slice(0, 10)) : "")) + "</p>" +
    '<div class="ag-vues oc-ong" role="tablist">' + [["aigue", "Aiguë"], ["tardive", "Tardive"]].map(([o, l]) => '<button role="tab" aria-selected="' + (ST.ctOng === o) + '" class="' + (ST.ctOng === o ? "on" : "") + '" onclick="ocCtOng(\'' + o + "')\">" + l + "</button>").join("") + "</div>" +
    '<div class="oc-filtre2"><div class="recherche"><svg class="i"><use href="#i-loupe"/></svg><input id="ocCtQ" type="search" placeholder="Rechercher un effet (terme, définition)" aria-label="Rechercher un effet" value="' + esc(ST.ctQ) + '"></div>' +
    '<div><label for="ocCtSoc">Classe d\'organes</label><select id="ocCtSoc" onchange="ocCtSoc(this.value)"><option value="">Toutes</option>' + socs.map((s) => '<option value="' + esc(s) + '"' + (s === ST.ctSoc ? " selected" : "") + ">" + esc(s) + "</option>").join("") + "</select></div></div>" +
    '<div id="ocCtL"></div><p class="mesures oc-src">Source : ' + src + (D.version ? ", version " + esc(D.version) : "") + "</p>" + AVERT() + "</section>";
  $("ocCtQ").oninput = (e) => { ST.ctQ = e.target.value; listeCt(); };
  listeCt();
}
const sansAcc = (s) => String(s || "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
function listeCt() {
  const D = ST.ctcae, q = sansAcc(ST.ctQ).trim(), tard = new Set(D.tardifs), z = $("ocCtL"); if (!z) return;
  const L = D.termes.filter((t) => (ST.ctOng !== "tardive" || tard.has(t.terme)) && (!ST.ctSoc || t.soc === ST.ctSoc) && (!q || sansAcc(t.terme + " " + (t.def || "")).indexOf(q) >= 0)), N = L.slice(0, 200);
  z.innerHTML = '<p class="mesures">' + L.length + " effet" + (L.length > 1 ? "s" : "") + (L.length > N.length ? " (200 affichés : affinez la recherche)" : "") + "</p>" + (N.length ? '<div class="oc-cartes oc-ct">' + N.map((t) => { const i = D.termes.indexOf(t);
    return '<div class="oc-carte oc-ctc" tabindex="0" role="button" aria-expanded="false" data-i="' + i + '" onclick="ocCtCarte(this,event)" onkeydown="if(event.key===\'Enter\')ocCtCarte(this,event)"><b>' + esc(t.terme) + '</b><span class="mesures">' + esc(t.soc || "") + '</span><span class="oc-def">' + esc(t.def || "") + '</span><div class="oc-gr5"></div></div>'; }).join("") + "</div>"
    : '<div class="vide-c">' + (ST.ctOng === "tardive" && !D.tardifs.length ? "Aucun effet suivi en tardive : ouvrez un effet dans « Aiguë » et cochez « Suivi en tardive »." : "Aucun effet ne correspond") + "</div>");
}
window.ocCtOng = (o) => { ST.ctOng = o; pageCtcae(); };
window.ocCtSoc = (v) => { ST.ctSoc = v; listeCt(); };
// RT.15 : un clic déplie le tableau des grades 0 à 5 (source dessous), un second clic le replie ; une carte ouverte à la fois
window.ocCtCarte = (el, ev) => {
  if (ev && ev.target.closest(".oc-gr5 input, .oc-gr5 label")) return;
  const ouv = !el.classList.contains("ouv"); document.querySelectorAll(".oc-ctc.ouv").forEach((x) => { x.classList.remove("ouv"); x.setAttribute("aria-expanded", "false"); x.querySelector(".oc-gr5").innerHTML = ""; });
  if (!ouv) return;
  const D = ST.ctcae, t = D.termes[Number(el.dataset.i)]; el.classList.add("ouv"); el.setAttribute("aria-expanded", "true");
  el.querySelector(".oc-gr5").innerHTML = '<table class="lc oc-t"><thead><tr><th>Grade</th><th>Description</th></tr></thead><tbody><tr><td class="oc-k">0</td><td>Aucun</td></tr>' +
    [1, 2, 3, 4, 5].map((g) => '<tr><td class="oc-k">' + g + "</td><td>" + esc(t.g[g - 1] || "—") + "</td></tr>").join("") + "</tbody></table>" +
    '<p class="mesures oc-src">Source : CTCAE ' + esc(D.version || "") + " (NCI)" + (t.note ? " · " + esc(t.note) : "") + "</p>" +
    (peutEcrire() ? '<label class="chk oc-tard"><input type="checkbox"' + (D.tardifs.indexOf(t.terme) >= 0 ? " checked" : "") + ' onchange="ocCtTard(' + el.dataset.i + ',this.checked)"> Suivi en tardive</label>' : "");
};
window.ocCtTard = async (i, oui) => {
  const D = ST.ctcae, t = D.termes[i]; if (!t || !peutEcrire()) return;
  const L = D.tardifs.filter((x) => x !== t.terme).concat(oui ? [t.terme] : []);
  try { await runTransaction(db, async (tx) => { const s = await tx.get(ref("ctcae")); tx.set(ref("ctcae"), Object.assign({}, s.exists() ? s.data() : {}, { tardifs: L }, signe())); }); D.tardifs = L; A.toast(oui ? "Ajouté à « Tardive »" : "Retiré de « Tardive »"); if (ST.ctOng === "tardive") listeCt(); }
  catch (e) { A.toast("Pas de connexion : réessayez"); }
};
let XLSX_P = null;
const chargerXlsx = () => (window.XLSX ? Promise.resolve() : (XLSX_P = XLSX_P || new Promise((ok, ko) => { const e = document.createElement("script"); e.src = "vendor/xlsx.full.min.js"; e.onload = ok; e.onerror = () => { XLSX_P = null; ko(new Error("Lecteur Excel indisponible : réessayez")); }; document.head.appendChild(e); })));
// Lecture du fichier du NCI : ligne d'en-tête avec « CTCAE Term » (ou « Term »), « Grade 1 » … « Grade 5 », « Definition », « MedDRA SOC »
export function lireTableauCtcae(rows) {
  const n = (s) => sansAcc(s).replace(/[^a-z0-9]/g, "");
  const h = rows.findIndex((r) => (r || []).some((c) => /^(ctcae)?(v\d+)?term/.test(n(c))) && (r || []).some((c) => n(c) === "grade1")); if (h < 0) return null;
  const H = rows[h].map(n), col = (f) => H.findIndex(f), cT = col((c) => /^(ctcae)?(v\d+)?term$/.test(c) || c === "ctcaeterm"), cS = col((c) => /soc/.test(c)), cD = col((c) => /definition/.test(c)), cN = col((c) => /navigationalnote|note/.test(c));
  const cG = [1, 2, 3, 4, 5].map((g) => col((c) => c === "grade" + g));
  if (cT < 0 || cG.some((x) => x < 0)) return null;
  const clean = (v) => String(v == null ? "" : v).replace(/\s+/g, " ").trim().replace(/^[-–]$/, "");
  return rows.slice(h + 1).filter((r) => r && clean(r[cT])).map((r) => Object.assign({ terme: clean(r[cT]), soc: cS >= 0 ? clean(r[cS]) : "", def: cD >= 0 ? clean(r[cD]) : "", g: cG.map((c) => clean(r[c])) }, cN >= 0 && clean(r[cN]) ? { note: clean(r[cN]) } : {}));
}
window.ocCtImport = async (inp) => {
  const f = inp.files && inp.files[0]; inp.value = ""; if (!f || !peutEcrire()) return;
  try { await chargerXlsx(); } catch (e) { A.toast(e.message); return; }
  let T = null;
  try { const wb = /\.csv$/i.test(f.name) ? window.XLSX.read(await f.text(), { type: "string" }) : window.XLSX.read(await f.arrayBuffer(), { type: "array" });
    for (const nm of wb.SheetNames) { T = lireTableauCtcae(window.XLSX.utils.sheet_to_json(wb.Sheets[nm], { header: 1, raw: false, defval: "" })); if (T && T.length) break; } }
  catch (e) { console.warn("CTCAE", e); }
  if (!T || !T.length) { A.toast("Fichier non reconnu : il faut le fichier Excel du NCI (colonnes « CTCAE Term », « Grade 1 » … « Grade 5 »)."); return; }
  const v0 = (f.name.match(/v\s*(\d+(?:[._]\d+)?)/i) || [])[1];
  const version = window.prompt ? (window.prompt("Version du CTCAE (" + T.length + " termes lus) :", v0 ? v0.replace("_", ".") : "6.0") || "").trim() : v0 || "";
  const parts = []; let cur = [], taille = 0;
  T.forEach((t) => { const s = JSON.stringify(t).length; if (taille + s > 700000 && cur.length) { parts.push(cur); cur = []; taille = 0; } cur.push(t); taille += s; }); if (cur.length) parts.push(cur);
  try {
    for (let i = 0; i < parts.length; i++) await setDoc(ref("ctcae_" + i), { data: JSON.stringify(parts[i]) });
    const s = await getDoc(ref("ctcae")), anc = s.exists() ? s.data() : {};
    await setDoc(ref("ctcae"), Object.assign({ version, parts: parts.length, n: T.length, source: "NCI", fichier: f.name.slice(0, 120), tardifs: Array.isArray(anc.tardifs) ? anc.tardifs : CTCAE_TARDIFS0 }, signe()));
  } catch (e) { A.toast(e && e.code === "permission-denied" ? "Seul le médecin importe le fichier." : "Pas de connexion : réessayez"); return; }
  ST.ctcae = null; A.toast(T.length + " termes importés"); pageCtcae();
};

// ───── RT.16, RT.17 Calculateurs ─────
const n0 = (k, lib, unite, o) => ({ k, lib, unite, t: "num", ...(o || {}) });
const sel = (k, lib, opts, o) => ({ k, lib, t: "sel", opts, ...(o || {}) });
const coche = (k, lib) => ({ k, lib, t: "chk" });
const SEXE = sel("sexe", "Sexe", [["M", "Homme"], ["F", "Femme"]]), CREAT = n0("cr", "Créatinine", ""), UCR = sel("ucr", "Unité", [["umol", "µmol/L"], ["mg", "mg/dL"]]);
const ligne = (lib, v) => '<div class="oc-r"><span>' + lib + "</span><b>" + v + "</b></div>";
const CALC_UI = {
  bed: { champs: [n0("d", "Dose par séance", "Gy"), n0("n", "Nombre de séances", ""), n0("ab", "α/β", "Gy", { v: "3" })], calc: (v) => { const r = C.bedEqd2(v.d, v.n, v.ab); return r && ligne("Dose totale", fmt(r.total, 2) + " Gy") + ligne("BED", fmt(r.bed) + " Gy") + ligne("EQD2", fmt(r.eqd2) + " Gy"); },
    plus: '<p class="mesures">Plusieurs phases, α/β par organe : <a href="#radiotherapie/calcul">calcul détaillé du référentiel de radiothérapie</a>.</p>' },
  conversion: { champs: [n0("D", "Dose totale prescrite", "Gy"), n0("d", "Dose par séance", "Gy"), n0("d2", "Nouvelle dose par séance", "Gy", { v: "2" }), n0("ab", "α/β", "Gy", { v: "3" })], calc: (v) => { const r = C.conversionDose(v.D, v.d, v.d2, v.ab); return r && ligne("Dose totale équivalente", fmt(r.dose) + " Gy") + ligne("Soit", fmt(r.seances) + " séances de " + fmt(C.num(v.d2), 2) + " Gy"); } },
  tdpsa: { champs: "psa", calc: (v) => { const r = C.tdPSA(v.psa); return !r ? "" : r.baisse ? ligne("PSA", "en baisse ou stable : pas de temps de doublement") : ligne("Temps de doublement", fmt(r.td) + " mois") + ligne("Dosages", String(r.n)); } },
  damico: { champs: [n0("psa", "PSA", "ng/mL"), sel("gl", "Score de Gleason", [6, 7, 8, 9, 10].map((x) => [String(x), String(x)])), sel("t", "Stade clinique (T)", ["T1a", "T1b", "T1c", "T2a", "T2b", "T2c", "T3a", "T3b", "T4"].map((x) => [x, x]))], calc: (v) => { const r = C.damico(v.psa, v.gl, v.t); return r && ligne("Groupe", r); } },
  roach: { champs: [n0("psa", "PSA", "ng/mL"), sel("gl", "Score de Gleason", [6, 7, 8, 9, 10].map((x) => [String(x), String(x)]))], calc: (v) => { const r = C.roach(v.psa, v.gl); return r && ligne("Atteinte ganglionnaire", fmt(r.ganglions) + " %") + ligne("Extension extracapsulaire", fmt(r.capsule) + " %") + ligne("Vésicules séminales", fmt(r.vesicules) + " %"); } },
  apbi: { champs: [n0("age", "Âge", "ans"), n0("taille", "Taille tumorale", "cm"), sel("t", "T", [["Tis", "Tis"], ["T1", "T1"], ["T2", "T2"], ["T3", "T3"], ["T4", "T4"]]), n0("marge", "Marge la plus proche", "mm"), coche("margePos", "Marges atteintes"),
    sel("lvsi", "Emboles (LVSI)", [["aucun", "Aucun"], ["limite", "Limités ou focaux"], ["etendu", "Étendus"]]), sel("re", "Récepteurs aux œstrogènes", [["pos", "Positifs"], ["neg", "Négatifs"]]), sel("histo", "Histologie", [["canalaire", "Canalaire ou autre favorable"], ["lobulaire", "Lobulaire infiltrant"]]),
    coche("ccis", "CCIS pur"), sel("grade", "Grade du CCIS", [["bas", "Bas ou intermédiaire"], ["haut", "Haut"]]), coche("depistage", "CCIS découvert au dépistage"), n0("eic", "Composante intracanalaire étendue", "cm"), coche("multicentrique", "Multicentrique"), coche("multifocal", "Multifocal"),
    coche("brca", "Mutation BRCA1/2"), coche("n", "Atteinte ganglionnaire (pN+)"), coche("neoadj", "Traitement néoadjuvant")], calc: (v) => { const r = C.apbi(v); return r && ligne("Irradiation partielle", r.avis) + (r.raisons.length ? '<ul class="oc-ul">' + r.raisons.map((x) => "<li>" + esc(x) + "</li>").join("") + "</ul>" : ""); } },
  vnpi: { champs: [n0("t", "Taille", "mm"), n0("m", "Marge la plus proche", "mm"), sel("c", "Classe histologique", [["1", "Non haut grade, sans nécrose"], ["2", "Non haut grade, avec nécrose"], ["3", "Haut grade"]]), n0("age", "Âge", "ans")], calc: (v) => { const r = C.vanNuys(v.t, v.m, v.c, v.age); return r && ligne("Score", String(r.score)) + ligne("Groupe", r.groupe); } },
  rpa: { champs: [n0("age", "Âge", "ans"), n0("kps", "Indice de Karnofsky", "%"), coche("res", "Exérèse chirurgicale (pas une biopsie seule)"), coche("neuro", "Fonction neurologique permettant de travailler"), coche("mental", "État mental normal")], calc: (v) => { const r = C.rpaGbm(v.age, v.kps, v.res, v.neuro, v.mental); return r && ligne("RPA (glioblastome)", r); } },
  hodgkin: { champs: [sel("stade", "Stade", [["I", "I"], ["II", "II"], ["III", "III"], ["IV", "IV"]]), coche("b", "Signes B"), n0("age", "Âge", "ans"), n0("vs", "Vitesse de sédimentation", "mm"), n0("aires", "Aires ganglionnaires atteintes", ""), coche("masse", "Masse médiastinale volumineuse"), coche("extra", "Atteinte extraganglionnaire")],
    calc: (v) => { const r = C.hodgkin(v); return ligne("EORTC", r.eortc) + ligne("GHSG", r.ghsg); } },
  ipi: { champs: [coche("age", "Âge > 60 ans"), coche("ldh", "LDH > normale"), coche("ecog", "ECOG ≥ 2"), coche("stade", "Stade III ou IV"), coche("extra", "Plus d'un site extraganglionnaire")], calc: (v) => { const r = C.ipi(v); return ligne("Score", String(r.score)) + ligne("Risque", r.groupe); } },
  flipi: { champs: [coche("age", "Âge > 60 ans"), coche("stade", "Stade III ou IV"), coche("hb", "Hémoglobine < 12 g/dL"), coche("ldh", "LDH > normale"), coche("aires", "Plus de 4 aires ganglionnaires")], calc: (v) => { const r = C.flipi(v); return ligne("Score", String(r.score)) + ligne("Risque", r.groupe); } },
  childpugh: { champs: [n0("bili", "Bilirubine totale", ""), sel("ub", "Unité", [["umol", "µmol/L"], ["mg", "mg/dL"]]), n0("alb", "Albumine", ""), sel("ua", "Unité", [["gl", "g/L"], ["gdl", "g/dL"]]), n0("inr", "INR", ""),
    sel("asc", "Ascite", [["1", "Absente"], ["2", "Minime"], ["3", "Modérée à importante"]]), sel("enc", "Encéphalopathie", [["1", "Absente"], ["2", "Grade I–II"], ["3", "Grade III–IV"]])], calc: (v) => { const r = C.childPugh(v.bili, v.ub, v.alb, v.ua, v.inr, v.asc, v.enc); return r && ligne("Score", String(r.score)) + ligne("Classe", r.classe); } },
  imc: { champs: [n0("p", "Poids", "kg"), n0("t", "Taille", "cm")], calc: (v) => { const r = C.imc(v.p, v.t); return r && ligne("IMC", fmt(r.imc) + " kg/m²") + ligne("Classe (OMS)", r.classe); } },
  surface: { champs: [n0("p", "Poids", "kg"), n0("t", "Taille", "cm")], calc: (v) => { const r = C.surface(v.p, v.t); return r && ligne("Du Bois", fmt(r.dubois, 2) + " m²") + ligne("Mosteller", fmt(r.mosteller, 2) + " m²"); } },
  mdrd: { champs: [n0("age", "Âge", "ans"), SEXE, CREAT, UCR], calc: (v) => { const r = C.mdrd(v.age, v.cr, v.ucr, v.sexe); return r && ligne("DFG estimé", fmt(r) + " mL/min/1,73 m²"); } },
  cockcroft: { champs: [n0("age", "Âge", "ans"), n0("p", "Poids", "kg"), SEXE, CREAT, UCR], calc: (v) => { const r = C.cockcroft(v.age, v.p, v.cr, v.ucr, v.sexe); return r && ligne("Clairance de la créatinine", fmt(r) + " mL/min"); } },
  schwartz: { champs: [n0("t", "Taille", "cm"), CREAT, UCR], calc: (v) => { const r = C.schwartz(v.t, v.cr, v.ucr); return r && ligne("DFG estimé (enfant)", fmt(r) + " mL/min/1,73 m²"); } },
  carbo: { champs: [n0("auc", "AUC cible", "mg/mL·min", { v: "5" }), n0("age", "Âge", "ans"), n0("p", "Poids", "kg"), SEXE, CREAT, UCR, n0("dfg", "DFG pour Calvert (vide : Cockcroft-Gault)", "mL/min"), coche("plaf", "Plafonner le DFG à 125 mL/min (Calvert)")],
    calc: (v) => { const g = C.num(v.dfg), cg = C.cockcroft(v.age, v.p, v.cr, v.ucr, v.sexe), dfg = isFinite(g) ? g : cg, ca = dfg != null ? C.calvert(v.auc, dfg, v.plaf) : null, ch = C.chatelut(v.auc, v.age, v.p, v.cr, v.ucr, v.sexe);
      return (ca ? ligne("Calvert", ca.dose + " mg") + '<p class="mesures">DFG utilisé : ' + fmt(ca.dfg) + " mL/min" + (isFinite(g) ? "" : " (Cockcroft-Gault)") + (ca.plafonne ? ", plafonné" : "") + "</p>" : "") + (ch ? ligne("Chatelut", ch.dose + " mg") + '<p class="mesures">Clairance du carboplatine : ' + fmt(ch.clairance) + " mL/min</p>" : ""); } },
  calcemie: { champs: [n0("ca", "Calcium total", ""), n0("alb", "Albumine", ""), sel("u", "Unités", [["mmol", "mmol/L et g/L"], ["mg", "mg/dL et g/dL"]])], calc: (v) => { const r = C.calcemie(v.ca, v.alb, v.u); return r != null && ligne("Calcémie corrigée", fmt(r, 2) + (v.u === "mg" ? " mg/dL" : " mmol/L")); } },
  opioides: { champs: [sel("de", "Opioïde actuel", C.OPIOIDES.map((o) => [o[0], o[1]])), n0("dose", "Dose actuelle", "mg/24 h ou µg/h"), sel("vers", "Vers", C.OPIOIDES.map((o) => [o[0], o[1]]), { v: "oxycodone-po" })],
    calc: (v) => { const r = C.opioides(v.de, v.dose, v.vers); return r && ligne("Équivalent morphine orale", fmt(r.morphine) + " mg/24 h") + ligne("Dose équivalente", fmt(r.dose) + " " + r.unite) + '<p class="mesures">Rotation d\'opioïde : la dose est habituellement réduite de 25 à 50 % (tolérance croisée incomplète), puis adaptée à la douleur.</p>'; } },
  esperance: { champs: "esp" },
  ps: { champs: "ps" },
};
async function pageCalc() {
  if (!ST.arg) {
    $("ocMain").innerHTML = '<section class="carte oc-c"><h2>Calculateurs</h2><p class="sous">Formules prises dans les publications d\'origine, chacune avec sa source.</p>' +
      GROUPES_CALC.map(([g, lg]) => '<h3 class="oc-h3">' + esc(lg) + '</h3><div class="oc-cartes">' + CALCS.filter((c) => c[2] === g).map((c) => '<button type="button" class="oc-carte" onclick="location.hash=\'outils/calc/' + c[0] + "'\"><b>" + esc(c[1]) + '</b><span class="mesures">' + esc(c[3]) + "</span></button>").join("") + "</div>").join("") + AVERT() + "</section>";
    return;
  }
  const c = CALCS.find((x) => x[0] === ST.arg), U = CALC_UI[c[0]];
  const src = esc(c[3]) + (c[4] ? ' · <a href="' + esc(c[4]) + '" target="_blank" rel="noopener">ouvrir</a>' : "");
  if (c[4] && !U) { $("ocMain").innerHTML = carteSec(c[1], '<p class="sous">Outil protégé : il n\'est pas recopié dans Onco360. Il s\'ouvre sur le site de son auteur.</p><a class="bt plein" href="' + esc(c[4]) + '" target="_blank" rel="noopener">' + A.ic("agrandir") + "Ouvrir l'outil</a>", src); return; }
  if (U.champs === "ps") { $("ocMain").innerHTML = carteSec(c[1], '<div class="tableau"><table class="lc oc-t"><thead><tr><th>OMS / ECOG</th><th>Description</th><th>Karnofsky (équivalent)</th></tr></thead><tbody>' + PS.map((r) => '<tr><td class="oc-k">' + r[0] + "</td><td>" + esc(r[1]) + "</td><td>" + esc(r[2]) + "</td></tr>").join("") + "</tbody></table></div>" +
    '<h3 class="oc-h3">Indice de Karnofsky</h3><div class="tableau"><table class="lc oc-t"><thead><tr><th>%</th><th>Description</th></tr></thead><tbody>' + KARNOFSKY.map((r) => '<tr><td class="oc-k">' + r[0] + "</td><td>" + esc(r[1]) + "</td></tr>").join("") + "</tbody></table></div>", src); return; }
  if (U.champs === "esp") return pageEsperance(c, src);
  const champs = U.champs === "psa" ? '<div id="ocPsa"></div><button type="button" class="mini rtr-aj" onclick="ocPsaL()">' + A.ic("plus") + "Ajouter un dosage</button>" : '<div class="form oc-f">' + U.champs.map(champ).join("") + "</div>";
  $("ocMain").innerHTML = carteSec(c[1], champs + '<div class="oc-res" id="ocRes" aria-live="polite"></div>' + (U.plus || ""), src);
  if (U.champs === "psa") { ST.psa = ST.psa || [{ d: "", psa: "" }, { d: "", psa: "" }]; dessinerPsa(); }
  document.querySelectorAll("#ocMain [data-c]").forEach((e) => { e.oninput = recalc; e.onchange = recalc; }); recalc();
}
function champ(f) {
  const id = "oc_" + f.k;
  if (f.t === "chk") return '<div class="large oc-chk"><label class="chk"><input type="checkbox" id="' + id + '" data-c="' + f.k + '"> ' + esc(f.lib) + "</label></div>";
  if (f.t === "sel") return '<div><label for="' + id + '">' + esc(f.lib) + '</label><select id="' + id + '" data-c="' + f.k + '">' + f.opts.map(([k, l]) => '<option value="' + esc(k) + '"' + (f.v === k ? " selected" : "") + ">" + esc(l) + "</option>").join("") + "</select></div>";
  return '<div><label for="' + id + '">' + esc(f.lib) + (f.unite ? ' <span class="mesures">(' + esc(f.unite) + ")</span>" : "") + '</label><input id="' + id + '" data-c="' + f.k + '" inputmode="decimal" value="' + esc(f.v || "") + '"></div>';
}
function recalc() {
  const c = CALCS.find((x) => x[0] === ST.arg), U = c && CALC_UI[c[0]], z = $("ocRes"); if (!U || !z) return;
  const v = {}; document.querySelectorAll("#ocMain [data-c]").forEach((e) => { v[e.dataset.c] = e.type === "checkbox" ? e.checked : e.value; });
  if (U.champs === "psa") v.psa = ST.psa;
  let h = ""; try { h = U.calc(v) || ""; } catch (e) { h = ""; }
  z.innerHTML = h || '<p class="mesures">Renseignez les champs pour obtenir le résultat.</p>';
}
function dessinerPsa() {
  $("ocPsa").innerHTML = '<div class="tableau"><table class="lc oc-t oc-ed"><thead><tr><th>Date du dosage</th><th>PSA (ng/mL)</th><th></th></tr></thead><tbody>' + ST.psa.map((p, i) => '<tr><td data-l="Date"><input type="date" class="rtr-in" value="' + esc(p.d) + '" oninput="ocPsa(' + i + ',\'d\',this.value)" aria-label="Date"></td><td data-l="PSA"><input class="rtr-in" inputmode="decimal" value="' + esc(p.psa) + '" oninput="ocPsa(' + i + ',\'psa\',this.value)" aria-label="PSA"></td>' +
    '<td><button type="button" class="rtr-sup" onclick="ocPsaL(' + i + ')" aria-label="Retirer ce dosage" title="Retirer">' + A.ic("croix") + "</button></td></tr>").join("") + "</tbody></table></div>";
}
window.ocPsa = (i, k, v) => { ST.psa[i][k] = v; recalc(); };
window.ocPsaL = (i) => { if (i == null) ST.psa.push({ d: "", psa: "" }); else ST.psa.splice(i, 1); dessinerPsa(); recalc(); };
// Espérance de vie : table de mortalité du cabinet (âge, hommes, femmes : années restantes), saisie par le médecin avec sa source
async function pageEsperance(c, src) {
  if (!ST.esp) { const s = await getDoc(ref("esperanceVie")); ST.esp = s.exists() ? s.data() : { source: "", lignes: [] }; }
  const E = ST.esp, ed = ST.ed && ST.ed.esp;
  const table = ed ? '<div class="form"><div class="large"><label for="ocEspS">Source de la table</label><input id="ocEspS" value="' + esc(ST.ed.F.source) + '" oninput="ST_esp(\'source\',this.value)" placeholder="ex. OMS, table de mortalité du Maroc, 2021"></div></div>' + edTable("lignes", [["age", "Âge"], ["h", "Hommes (années)"], ["f", "Femmes (années)"]], ST.ed.F.lignes) +
    '<div class="barre-enr"><button class="bt gris" onclick="ocEspAnn()">Annuler</button><span></span><button class="bt plein" id="ocEspOk" onclick="ocEspOk()">' + A.ic("enregistrer") + "Enregistrer</button></div>"
    : (E.lignes || []).length ? '<div class="form oc-f"><div><label for="oc_age">Âge</label><input id="oc_age" data-c="age" inputmode="decimal"></div><div><label for="oc_sexe">Sexe</label><select id="oc_sexe" data-c="sexe"><option value="M">Homme</option><option value="F">Femme</option></select></div></div><div class="oc-res" id="ocRes"></div>' +
      '<p class="mesures">Table : ' + esc(E.source || "source à préciser") + "</p>" + (peutEcrire() ? '<button class="bt clair petit" onclick="ocEspModif()">' + A.ic("crayon") + "Modifier la table</button>" : "")
      : A.etatVide({ ill: "document", titre: "Table à remplir", txt: "Saisissez une table de mortalité (âge, années restantes pour les hommes et les femmes) avec sa source, par exemple celle de l'OMS pour le Maroc.", bouton: peutEcrire() ? '<button class="bt plein" onclick="ocEspModif()">' + A.ic("crayon") + "Remplir la table</button>" : "" });
  $("ocMain").innerHTML = carteSec(c[1], table, ed ? src : esc(E.source || c[3]));
  const z = $("ocRes"); if (z) { const f = () => { const r = C.esperance(E.lignes, A.val("oc_age"), A.val("oc_sexe")); z.innerHTML = r ? ligne("Espérance de vie à " + fmt(r.age, 0) + " ans", fmt(r.annees) + " ans") : '<p class="mesures">Indiquez l\'âge.</p>'; }; $("oc_age").oninput = f; $("oc_sexe").onchange = f; f(); }
}
window.ST_esp = (k, v) => { if (ST.ed && ST.ed.esp) ST.ed.F[k] = v; };
window.ocEspModif = () => { if (!peutEcrire()) return; ST.ed = { esp: true, F: JSON.parse(JSON.stringify(Object.assign({ source: "", lignes: [] }, ST.esp))) }; if (!ST.ed.F.lignes.length) ST.ed.F.lignes = [{}]; pageCalc(); };
window.ocEspAnn = () => { ST.ed = null; pageCalc(); };
window.ocEspOk = async () => {
  if (!ST.ed || !ST.ed.esp) return;
  const d = Object.assign({ source: String(ST.ed.F.source || "").trim(), lignes: ST.ed.F.lignes.filter((l) => String(l.age || "").trim()).map((l) => ({ age: String(l.age).trim(), h: String(l.h || "").trim(), f: String(l.f || "").trim() })) }, signe());
  try { await setDoc(ref("esperanceVie"), d); } catch (e) { A.toast("Pas de connexion : réessayez"); return; }
  ST.esp = d; ST.ed = null; A.toast("Enregistré"); pageCalc();
};
// lignes de la table d'espérance de vie : même tableau modifiable que la stadification (chemin « lignes »)
const ocLigne0 = window.ocLigne;
window.ocLigne = (key, i) => { if (ST.ed && ST.ed.esp) { const L = ST.ed.F.lignes; if (i == null) L.push({}); else L.splice(i, 1); pageCalc(); return; } ocLigne0(key, i); };

// Pages du manuel jointes (PDF du cabinet) : Cloud Storage espaces/{e}/documentation/tnm-<id>-<ms>/<nom> (même règle que la documentation : médecin, PDF,
// 25 Mo), chemin noté dans bibliotheques/tnm_<id>.pdf ; jamais recopié dans Onco360 ni dans les autres cabinets
window.ocTnmPdfAj = async (id, inp) => {
  const f = inp.files && inp.files[0]; inp.value = ""; if (!f || !peutEcrire()) return;
  if (f.type !== "application/pdf" || f.size > 25 * 1024 * 1024) { A.toast("Un fichier PDF de moins de 25 Mo."); return; }
  const nom = f.name.replace(/[^\w.\- ]+/g, "_").slice(0, 100), chemin = "espaces/" + A.ESPACE + "/documentation/tnm-" + id + "-" + Date.now() + "/" + nom;
  try {
    A.toast("Envoi du PDF…"); await new Promise((ok, ko) => { uploadBytesResumable(sref(getStorage(app), chemin), f, { contentType: "application/pdf", customMetadata: { creePar: A.D().u.uid } }).on("state_changed", () => {}, ko, ok); });
    const F = Object.assign({}, await lireSous(id), { pdf: { chemin, nom, taille: f.size, le: new Date().toISOString() } }, signe());
    await setDoc(ref("tnm_" + id), F); ST.sousC[id] = F;
  } catch (e) { console.warn("PDF du manuel", e); A.toast("Envoi impossible : réessayez."); return; }
  A.toast("PDF joint"); ficheTnm(id);
};
window.ocTnmPdf = async (id) => {
  const F = ST.sousC[id]; if (!F || !F.pdf) return; const w = window.open("", "_blank");
  try { const b = await getBlob(sref(getStorage(app), F.pdf.chemin)); const u = URL.createObjectURL(b); if (w) w.location.href = u; else window.open(u, "_blank"); }
  catch (e) { if (w) w.close(); A.toast("PDF introuvable : réessayez."); }
};
