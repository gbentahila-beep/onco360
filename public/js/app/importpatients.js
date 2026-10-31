// Onco360 – L2 (31/10/2026) : Paramètres › Cabinet › Export des données › « Importer des patients (fichier Excel) » (médecin titulaire).
// Modèle Excel à télécharger, fichier lu dans le navigateur (SheetJS, vendor/), aperçu ligne par ligne (erreurs, doublons nom + prénom +
// naissance, dans le fichier et dans Onco360), import, compte rendu (à l'écran et en Excel). Numéro de dossier Onco360 attribué comme d'habitude
// (fonction numerosManquants, par paquets) ; numéro du logiciel d'avant gardé dans identite.numOrig. Calculs : js/moteur/importpatients.js.
import { db } from "../config.js";
import { doc, setDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";
import { COLONNES, analyser, depuisTableau, MAX_LIGNES } from "../moteur/importpatients.js";
import { enrichirListes } from "./chimio.js";
import { DIAG } from "../donnees/listes.js";

let A = null;
export function installer(api) { A = api; }
const D = () => A.D();
const esc = (s) => A.esc(s);
let XLSX_P = null;
const chargerXlsx = () => (window.XLSX ? Promise.resolve() : (XLSX_P = XLSX_P || new Promise((ok, ko) => { const e = document.createElement("script"); e.src = "vendor/xlsx.full.min.js"; e.onload = ok; e.onerror = () => { XLSX_P = null; ko(new Error("Lecteur Excel indisponible : réessayez.")); }; document.head.appendChild(e); })));
const IP = { an: null, nomFichier: "", fait: null, doublons: false };
const PAQUET = 400; // dossiers créés avant chaque numérotation par le serveur (numerosManquants : 450 au plus d'un coup)

export function htmlImport() {
  const etabs = D().etabs || [];
  return '<section class="carte" id="ipCarte"><h3><span class="ic">' + A.ic("patients") + "</span>Importer des patients (fichier Excel)</h3>" +
    '<p class="sous">Reprenez vos dossiers d\'un autre logiciel : identité, CIN, téléphone, mutuelle, diagnostic, numéro de dossier d\'origine. Rien n\'est créé avant votre accord : vous voyez d\'abord chaque ligne.</p>' +
    '<div class="ip-barre"><button type="button" class="b2" id="ipModele">' + A.ic("telecharger") + "Télécharger le modèle Excel</button>" +
    '<label class="b2 ip-fic">' + A.ic("document") + 'Choisir le fichier<input type="file" id="ipFichier" accept=".xlsx,.xls,.csv" hidden></label>' +
    '<label class="ip-etab">Établissement par défaut <select id="ipEtab">' + etabs.map((e) => '<option value="' + esc(e.code) + '">' + esc(e.nom || e.code) + "</option>").join("") + "</select></label></div>" +
    '<div id="ipCorps"></div></section>';
}
export function brancherImport() {
  if (!A.$("ipCarte")) return;
  A.$("ipModele").onclick = telechargerModele;
  A.$("ipFichier").onchange = (ev) => { const f = ev.target.files && ev.target.files[0]; if (f) lireFichier(f); ev.target.value = ""; };
  A.$("ipEtab").onchange = () => { if (IP.lignes) analyserTout(); };
  dessiner();
}
async function telechargerModele() {
  try {
    await chargerXlsx();
    const X = window.XLSX, ws = X.utils.aoa_to_sheet([COLONNES.map((c) => c[1]), COLONNES.map((c) => c[3])]);
    ws["!cols"] = COLONNES.map((c) => ({ wch: Math.max(14, c[1].length + 2) }));
    const wb = X.utils.book_new(); X.utils.book_append_sheet(wb, ws, "Patients");
    X.writeFile(wb, "Onco360_modele_import_patients.xlsx");
  } catch (e) { A.toast("Modèle impossible : " + e.message); }
}
async function lireFichier(f) {
  IP.fait = null; IP.an = null; IP.lignes = null; IP.nomFichier = f.name; IP.err = "";
  A.$("ipCorps").innerHTML = '<p class="mesures">Lecture de « ' + esc(f.name) + " »…</p>";
  try {
    await chargerXlsx();
    // fichier CSV : texte en UTF-8, sinon en Windows-1252 (CSV enregistré par Excel) ; Excel : lu tel quel
    const buf = await f.arrayBuffer(), csv = /\.csv$/i.test(f.name);
    let texte = csv ? new TextDecoder("utf-8").decode(buf) : null; if (csv && texte.indexOf("\uFFFD") >= 0) texte = new TextDecoder("windows-1252").decode(buf);
    const wb = csv ? window.XLSX.read(texte.replace(/^\uFEFF/, ""), { type: "string", cellDates: true, raw: true }) : window.XLSX.read(buf, { type: "array", cellDates: true }), ws = wb.Sheets[wb.SheetNames[0]];
    const T = depuisTableau(window.XLSX.utils.sheet_to_json(ws, { header: 1, raw: true, defval: "" }));
    IP.lignes = T.lignes; IP.inconnues = T.inconnues; IP.manquantes = T.manquantes;
    analyserTout();
  } catch (e) { IP.err = "Fichier illisible : " + e.message; dessiner(); }
}
function analyserTout() {
  const L = D().listes || {}, ctx = { auj: D().t, etabs: D().etabs || [], etabDefaut: A.$("ipEtab") ? A.$("ipEtab").value : "", diags: [].concat(DIAG || [], L.diag || []), mut: [].concat(L.mut || []) };
  IP.an = IP.manquantes && IP.manquantes.length ? null : analyser(IP.lignes, D().patients.map((x) => x.doc.identite || {}), ctx);
  dessiner();
}
const ETAT = { ok: ["r-ok", "Prête"], doublon: ["r-dbl", "Doublon"], erreur: ["r-err", "Erreur"] };
function dessiner() {
  const z = A.$("ipCorps"); if (!z) return;
  if (IP.err) { z.innerHTML = '<p class="err">' + esc(IP.err) + "</p>"; return; }
  if (IP.fait) { z.innerHTML = htmlCompteRendu(); A.$("ipCR").onclick = telechargerCompteRendu; return; }
  if (!IP.lignes) { z.innerHTML = ""; return; }
  if (IP.manquantes && IP.manquantes.length) { z.innerHTML = '<p class="err">Colonne obligatoire absente du fichier : ' + esc(IP.manquantes.join(", ")) + ". Partez du modèle Excel (première ligne = titres des colonnes).</p>"; return; }
  const a = IP.an, maxP = D().abo && D().abo.max.patients, place = maxP != null ? Math.max(0, maxP - D().patients.length) : null;
  const nb = a.ok + (IP.doublons ? a.doublons : 0);
  const lignes = a.lignes.slice(0, 300).map((r) => { const e = ETAT[r.etat], I = r.identite;
    return '<tr class="ip-' + e[0] + '"><td data-l="Ligne">' + r.ligne + '</td><td data-l="Patient">' + esc([I.nomF, I.prenom].filter(Boolean).join(" ") || "—") + '</td><td data-l="Naissance">' + esc(I.ddn ? I.ddn.split("-").reverse().join("/") : "—") +
      '</td><td data-l="État"><span class="ip-et">' + e[1] + '</span></td><td data-l="Remarques">' + esc([].concat(r.erreurs, r.doublon ? [r.doublon] : [], r.avert).join(" ; ") || "—") + "</td></tr>"; }).join("");
  z.innerHTML = '<p class="ip-res"><b>' + esc(IP.nomFichier) + "</b> : " + a.lignes.length + " ligne(s) · <b>" + a.ok + " prête(s)</b> · " + a.doublons + " doublon(s) · " + a.erreurs + " erreur(s)" + (a.tropLong ? " · seules les " + MAX_LIGNES + " premières lignes sont lues" : "") + "</p>" +
    (IP.inconnues && IP.inconnues.length ? '<p class="mesures">Colonnes ignorées : ' + esc(IP.inconnues.join(", ")) + "</p>" : "") +
    (a.doublons ? '<label class="ip-dbl"><input type="checkbox" id="ipDbl"' + (IP.doublons ? " checked" : "") + "> Importer quand même les lignes signalées en doublon</label>" : "") +
    '<div class="tableau"><table class="lc ip-tab"><thead><tr><th>Ligne</th><th>Patient</th><th>Naissance</th><th>État</th><th>Remarques</th></tr></thead><tbody>' + lignes + "</tbody></table></div>" +
    (a.lignes.length > 300 ? '<p class="mesures">300 premières lignes affichées ; toutes seront traitées.</p>' : "") +
    (place != null && nb > place ? '<p class="err">Votre formule permet encore ' + place + " dossier(s) : seuls les " + place + " premiers seront créés.</p>" : "") +
    '<div class="ip-barre"><button type="button" class="b1" id="ipGo"' + (nb ? "" : " disabled") + ">Importer " + Math.min(nb, place == null ? nb : place) + " patient(s)</button></div>";
  if (A.$("ipDbl")) A.$("ipDbl").onchange = () => { IP.doublons = A.$("ipDbl").checked; dessiner(); };
  A.$("ipGo").onclick = importer;
}
async function importer() {
  const a = IP.an, maxP = D().abo && D().abo.max.patients, place = maxP != null ? Math.max(0, maxP - D().patients.length) : Infinity;
  const choisies = a.lignes.filter((r) => r.etat === "ok" || (IP.doublons && r.etat === "doublon")).slice(0, place);
  if (!choisies.length || !confirm("Créer " + choisies.length + " dossier(s) patient(s) à partir de « " + IP.nomFichier + " » ?")) return;
  const bt = A.$("ipGo"); bt.disabled = true;
  const mb = D().membre, fin = A.peut("finances"), crees = [], echecs = [], listes = new Set();
  for (let i = 0; i < choisies.length; i++) {
    const r = choisies[i];
    if (i % 10 === 0) bt.textContent = "Import… " + i + " / " + choisies.length;
    const id = "P" + (Date.now() + i).toString(36) + Math.floor(Math.random() * 1000);
    const docP = { etablissementId: r.etab, identite: r.identite, clinique: r.clinique, version: 1, maj: serverTimestamp(), majPar: D().u.uid, lignesJson: "[]", planningJson: "{}", rdvsJson: "[]" };
    if (mb.droits && mb.droits.radiotherapie === "modifier") docP.rtsJson = "[]";
    const x = { id }; A.recalculer(x, Object.assign({}, docP, { maj: null })); docP.resume = JSON.stringify(x.r);
    try {
      await setDoc(doc(db, "espaces", A.ESPACE, "patients", id), docP);
      if (fin) await setDoc(doc(db, "espaces", A.ESPACE, "patientsFinances", id), { etablissementId: r.etab, montantsJson: JSON.stringify({ rdv: {}, rt: {}, cures: {} }) });
      D().patients.push(x); crees.push({ r, x });
      listes.add(JSON.stringify([r.identite.cor || "", r.identite.mut || "", r.clinique.diag || ""]));
    } catch (e) { echecs.push({ r, erreur: (e && e.message) || String(e) }); }
    if ((i + 1) % PAQUET === 0) await numeroter();
  }
  await numeroter();
  for (const k of listes) { const [c, m, d] = JSON.parse(k); await enrichirListes(c, m, d).catch(() => {}); }
  D().patients.sort((p, z) => String(p.r.nm).localeCompare(String(z.r.nm)));
  A.journal({ id: "", r: { nm: "" } }, "Import de patients (« " + IP.nomFichier + " ») : " + crees.length + " dossier(s) créé(s)");
  IP.fait = { crees, echecs, ignores: a.lignes.filter((r) => choisies.indexOf(r) < 0) };
  dessiner();
}
// Numéros de dossier des dossiers créés (serveur, dans l'ordre de création, sans doublon)
async function numeroter() {
  try { await A.serveur("numerosManquants", { espace: A.ESPACE }); }
  catch (e) { console.warn("numéros de dossier", e); }
  try {
    const { getDocs, collection } = await import("https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js");
    const s = await getDocs(collection(db, "espaces", A.ESPACE, "patients"));
    s.forEach((d) => { const x = D().patients.find((p) => p.id === d.id); if (x && !(x.doc.identite || {}).numero && (d.data().identite || {}).numero) A.recalculer(x, d.data()); });
  } catch (e) { console.warn("relecture des numéros", e); }
}
function htmlCompteRendu() {
  const F = IP.fait;
  return '<p class="ip-res ok"><b>' + F.crees.length + " dossier(s) créé(s)</b>" + (F.echecs.length ? " · " + F.echecs.length + " en échec" : "") + " · " + F.ignores.length + " ligne(s) non importée(s) (erreurs, doublons)</p>" +
    (F.echecs.length ? '<p class="err">' + F.echecs.slice(0, 5).map((e) => "Ligne " + e.r.ligne + " : " + esc(e.erreur)).join("<br>") + "</p>" : "") +
    '<div class="ip-barre"><button type="button" class="b2" id="ipCR">' + A.ic("telecharger") + 'Télécharger le compte rendu (Excel)</button><a class="b2" href="#patients">Voir les patients</a></div>';
}
async function telechargerCompteRendu() {
  try {
    await chargerXlsx();
    const F = IP.fait, num = (x) => (x.doc && x.doc.identite && x.doc.identite.numero) || "", lig = [];
    F.crees.forEach(({ r, x }) => lig.push([r.ligne, r.identite.nomF, r.identite.prenom, r.identite.ddn || "", "créé", num(x), r.identite.numOrig || "", r.avert.join(" ; ")]));
    F.echecs.forEach(({ r, erreur }) => lig.push([r.ligne, r.identite.nomF, r.identite.prenom, r.identite.ddn || "", "échec", "", r.identite.numOrig || "", erreur]));
    F.ignores.forEach((r) => lig.push([r.ligne, r.identite.nomF || "", r.identite.prenom || "", r.identite.ddn || "", r.etat === "doublon" ? "doublon, non importé" : "erreur, non importé", "", r.identite.numOrig || "", [].concat(r.erreurs, r.doublon ? [r.doublon] : []).join(" ; ")]));
    lig.sort((p, z) => p[0] - z[0]);
    lig.unshift(["Ligne du fichier", "Nom", "Prénom", "Naissance", "Résultat", "N° de dossier Onco360", "N° de dossier d'origine", "Remarques"]);
    const X = window.XLSX, wb = X.utils.book_new(); X.utils.book_append_sheet(wb, X.utils.aoa_to_sheet(lig), "Compte rendu");
    X.writeFile(wb, "Onco360_import_compte_rendu_" + D().t + ".xlsx");
  } catch (e) { A.toast("Compte rendu impossible : " + e.message); }
}
