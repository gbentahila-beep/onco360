// Onco360 – feuille de soins (lot 9, 31/10/2026, demande de Dr Bentahila) : bouton « Feuille de soins » de la barre du dossier (entre Doc. et
// + RCP, ouvert au centre comme les autres, 3.2) et action rapide du tableau de bord. Le modèle suit la mutuelle du dossier (CNSS, sinon CNOPS),
// modifiable. Consultation du dossier : « Saisie libre » par défaut, ou une consultation enregistrée (sa date remplace la date des soins : actes,
// « Le » de l'assuré et du médecin) ; type de soins Maladie par défaut ; pli confidentiel (CNOPS) ; malade et assuré(e) depuis le dossier ; médecin
// traitant depuis sa carte (signataires/{uid}) ; actes : une ligne, « + Ajouter un acte », total = montant des frais. Aperçu des pages remplies,
// puis Imprimer (A4 paysage ; « Imprimer le fond » décoché pour imprimer sur la feuille officielle). Placement : donnees/feuillesoins.js.
import { FORMULAIRES, feuilleDe, rendreFeuille, totalActes, montantTxt, CSS_FEUILLE } from "../donnees/feuillesoins.js";
import { assurerConsultations } from "./consultations.js";

let A = null;
export function installer(api) { A = api; if (!document.getElementById("styleFeuilles")) { const st = document.createElement("style"); st.id = "styleFeuilles"; st.textContent = CSS_FEUILLE; document.head.appendChild(st); } }
const D = () => A.D();
const $ = (i) => document.getElementById(i);
let F = null; // { pid, k (cnops | cnss), V (valeurs), cons (consultations), fond }
const TYPES = [["maladie", "Maladie"], ["maternite", "Maternité"], ["hospit", "Hospitalisation"], ["accident", "Accident"]];
const nomP = (I, x) => [String(I.nomF || I.nom || x.r.nm || "").toUpperCase(), I.prenom ? I.prenom.charAt(0).toUpperCase() + I.prenom.slice(1) : ""].filter(Boolean).join(" ");
function medecinDe(x) {
  const I = x.doc.identite || {}, uid = I.med || (D().espaceDoc && D().espaceDoc.titulaire) || "", c = (A.signataires() || {})[uid];
  return c && c.nom ? c : A.medecinFiche() || {};
}
function valeursDepart(x) {
  const I = x.doc.identite || {}, et = A.etabDe(x.doc.etablissementId) || {}, med = medecinDe(x), ville = et.ville || "", d = D().t, nm = nomP(I, x);
  return { tel: I.tel || "", assNom: nm, assAffil: "", assImmat: I.numAdh || "", assCin: I.cin || "", lien: "", adresse: I.adresse || "", pieces: "", dossier: "",
    malNom: nm, malDdn: I.ddn || "", malCin: I.cin || "", sexe: /^f/i.test(I.sexe || "") ? "F" : /^m/i.test(I.sexe || "") ? "M" : "", inpe: med.inpe || "", medNom: med.nom || "", etabNom: et.nom || "",
    type: "maladie", pli: "", dGross: "", dAccouch: "", dHosp: "", dAcc: "", causes: "", cim: "", faitA: ville, faitM: ville, le: d, leM: d, d,
    actes: [{ d, code: "", lettre: "", valeur: "", m: "" }], consId: "" };
}
window.fsOuvrir = async (pid) => {
  const x = D().patients.find((p) => p.id === pid); if (!x) return;
  if (!A.peut("ecrireConsultations")) { A.toast("Vous n'avez pas le droit de faire une feuille de soins."); return; }
  F = { pid, k: feuilleDe((x.doc.identite || {}).mut), V: valeursDepart(x), cons: [], fond: true };
  dessiner();
  const L = await assurerConsultations(x).catch(() => null);
  if (F && F.pid === pid && Array.isArray(L)) { F.cons = L.slice().sort((a, b) => String(b.d).localeCompare(String(a.d))); const s = $("fsCons"); if (s) s.outerHTML = selCons(); }
};
const x0 = () => F && D().patients.find((p) => p.id === F.pid);
const selCons = () => { const esc = A.esc, x = x0(), loc = x ? [x.r.diag, (x.doc.clinique || {}).diagP].filter(Boolean).join(" – ") : "";
  return '<select id="fsCons" data-k="consId"><option value="">Saisie libre</option>' + F.cons.map((c) => '<option value="' + esc(c.id) + '"' + (F.V.consId === c.id ? " selected" : "") + ">" + esc(A.dfrA(c.d) + " · " + (c.titre || "Consultation") + (loc ? " · " + loc : "")) + "</option>").join("") + "</select>"; };
function dessiner() {
  const esc = A.esc, x = x0(); if (!x) return;
  const V = F.V, f = FORMULAIRES[F.k], cnops = F.k === "cnops", loc = [x.r.diag, (x.doc.clinique || {}).diagP].filter(Boolean).join(" – ");
  const ch = (k, lib, o) => '<div' + (o && o.large ? ' class="large"' : "") + '><label for="fs_' + k + '">' + lib + "</label><input id=\"fs_" + k + '" data-k="' + k + '"' + (o && o.type ? ' type="' + o.type + '"' : "") + (o && o.num ? ' inputmode="numeric"' : "") + ' value="' + esc(V[k] || "") + '"' + (o && o.ph ? ' placeholder="' + esc(o.ph) + '"' : "") + "></div>";
  const sel = (k, lib, l) => '<div><label for="fs_' + k + '">' + lib + '</label><select id="fs_' + k + '" data-k="' + k + '">' + l.map(([v, t]) => '<option value="' + v + '"' + (V[k] === v ? " selected" : "") + ">" + esc(t) + "</option>").join("") + "</select></div>";
  const total = totalActes(V.actes);
  A.fenetre('<div class="pg-form fs-form"><h3>Feuille de soins — ' + esc(x.r.nm) + "</h3>" +
    '<section class="pg-sec"><h4 class="soustitre">Organisme</h4><div class="form"><div><label for="fsK">Feuille de soins</label><select id="fsK">' + Object.keys(FORMULAIRES).map((k) => '<option value="' + k + '"' + (k === F.k ? " selected" : "") + ">" + esc(FORMULAIRES[k].nom) + "</option>").join("") + "</select></div>" +
      '<div class="fs-lib"><span class="mesures">' + esc(f.lib) + ((x.doc.identite || {}).mut ? " · mutuelle du dossier : " + esc(x.doc.identite.mut) : "") + "</span></div></div></section>" +
    '<section class="pg-sec"><h4 class="soustitre">Soins</h4><div class="form"><div class="large"><label for="fsCons">Consultation du dossier</label>' + selCons() + (loc ? '<p class="mesures" style="margin:4px 0 0">Localisation (fiche tumeur) : ' + esc(loc) + "</p>" : "") + "</div>" +
      ch("d", "Date de la consultation", { type: "date" }) + sel("type", "Type de soins", TYPES) +
      (cnops ? sel("pli", "Pli confidentiel remis", [["", "Non renseigné"], ["oui", "Oui"], ["non", "Non"]]) : "") +
      ch("cim", "Code CIM-10", { ph: "Ex. C50" }) + ch("pieces", "Pièces jointes", { num: true }) +
      (cnops && V.type === "maternite" ? ch("dGross", "Date de grossesse", { type: "date" }) + ch("dAccouch", "Date prévue d'accouchement", { type: "date" }) : "") +
      (cnops && V.type === "hospit" ? ch("dHosp", "Date d'hospitalisation", { type: "date" }) : "") +
      (cnops && V.type === "accident" ? ch("dAcc", "Date d'accident", { type: "date" }) + ch("causes", "Causes") : "") + "</div></section>" +
    '<section class="pg-sec"><h4 class="soustitre">Malade (bénéficiaire des soins)</h4><div class="form">' + ch("malNom", "Nom et prénom", { large: true }) + ch("malDdn", "Date de naissance", { type: "date" }) +
      sel("sexe", "Sexe", [["", "—"], ["M", "Masculin"], ["F", "Féminin"]]) + ch("malCin", "N° CIN du malade") +
      '<div class="large"><label>Le malade est</label><div class="fp-seg fs-seg" role="group" aria-label="Le malade est">' + [["", "l'assuré(e)"], ["conjoint", "le conjoint"], ["enfant", "un enfant"]].map(([v, t]) => '<button type="button" data-lien="' + v + '" class="' + (V.lien === v ? "on" : "") + '" aria-pressed="' + (V.lien === v) + '">' + t + "</button>").join("") + "</div></div></div></section>" +
    '<section class="pg-sec"><h4 class="soustitre">Assuré(e)' + (V.lien ? "" : ' <span class="mesures">même personne que le malade</span>') + '</h4><div class="form">' +
      (V.lien ? ch("assNom", "Nom et prénom de l'assuré(e)", { large: true }) + ch("assCin", "N° CIN de l'assuré(e)") : "") +
      ch("assImmat", "N° d'immatriculation") + (cnops ? ch("assAffil", "N° d'affiliation") + ch("tel", "Téléphone (facultatif)") : ch("dossier", "N° de dossier (CNSS)")) +
      ch("adresse", "Adresse", { large: true }) + ch("faitA", "Fait à (assuré)") + ch("le", "Le (assuré)", { type: "date" }) + "</div></section>" +
    '<section class="pg-sec"><h4 class="soustitre">Médecin traitant</h4><div class="form">' + ch("medNom", "Médecin") + ch("inpe", "INPE", { num: true }) + (cnops ? "" : ch("etabNom", "Établissement de soins")) +
      ch("faitM", "Fait à (médecin)") + ch("leM", "Le (médecin)", { type: "date" }) + "</div></section>" +
    '<section class="pg-sec"><h4 class="soustitre">Actes effectués</h4><div class="fs-actes"><div class="fs-a fs-ah"><span>Date</span><span>Code</span><span>Lettre clé + cotation</span>' + (cnops ? "<span>Valeur clé</span>" : "") + "<span>Montant (DH)</span><span></span></div>" +
      V.actes.map((a, i) => '<div class="fs-a" data-i="' + i + '"><input type="date" data-a="d" value="' + esc(a.d) + '" aria-label="Date de l\'acte"><input data-a="code" value="' + esc(a.code) + '" aria-label="Code de l\'acte"><input data-a="lettre" value="' + esc(a.lettre) + '" placeholder="Ex. CS" aria-label="Lettre clé et cotation">' +
        (cnops ? '<input data-a="valeur" value="' + esc(a.valeur) + '" aria-label="Valeur clé">' : "") + '<input data-a="m" inputmode="decimal" value="' + esc(a.m) + '" aria-label="Montant en dirhams">' +
        (V.actes.length > 1 ? '<button type="button" class="ico rouge" data-sup="' + i + '" title="Retirer cet acte" aria-label="Retirer cet acte">' + A.ic("corbeille") + "</button>" : "<span></span>") + "</div>").join("") + "</div>" +
      '<div class="fs-tot">' + (V.actes.length < f.actes.max ? '<button type="button" class="bt clair petit" id="fsAj">' + A.ic("plus") + "Ajouter un acte</button>" : '<span class="mesures">' + f.actes.max + " actes au plus sur cette feuille</span>") +
      '<span>Montant total des frais : <b id="fsTot">' + (total ? montantTxt(total) + " DH" : "—") + "</b></span></div></section>" +
    '<div class="err" id="fErr"></div><div class="boutons"><button class="bt gris" onclick="fsFermer()">Annuler</button><button class="bt plein" id="fsVoir">' + A.ic("document") + "Aperçu du PDF</button></div></div>", "page");
  brancher();
}
function brancher() {
  const z = $("fenetreCorps"); if (!z) return;
  z.oninput = (e) => { const t = e.target; if (t.dataset.k && t.dataset.k !== "consId" && t.id !== "fsK") F.V[t.dataset.k] = t.value;
    const r = t.closest(".fs-a[data-i]"); if (r && t.dataset.a) { F.V.actes[+r.dataset.i][t.dataset.a] = t.value; if (t.dataset.a === "m") { const tt = totalActes(F.V.actes); $("fsTot").textContent = tt ? montantTxt(tt) + " DH" : "—"; } } };
  z.onchange = (e) => { const t = e.target;
    if (t.id === "fsK") { F.k = t.value; F.V.actes = F.V.actes.slice(0, FORMULAIRES[F.k].actes.max); dessiner(); return; }
    if (t.dataset.k === "type") { F.V.type = t.value; dessiner(); return; }
    if (t.dataset.k === "consId") { choisirCons(t.value); return; }
    if (t.dataset.k === "d") { const d = t.value || D().t; F.V.le = d; F.V.leM = d; F.V.actes.forEach((a) => { a.d = d; }); dessiner(); } };
  z.onclick = (e) => { const b = e.target.closest("button"); if (!b) return;
    if (b.dataset.lien != null) { F.V.lien = b.dataset.lien; if (!F.V.lien) { const x = x0(), I = x.doc.identite || {}; F.V.assNom = nomP(I, x); F.V.assCin = I.cin || ""; } else { F.V.assNom = ""; F.V.assCin = ""; } dessiner(); }
    else if (b.id === "fsAj") { F.V.actes.push({ d: F.V.d, code: "", lettre: "", valeur: "", m: "" }); dessiner(); }
    else if (b.dataset.sup != null) { F.V.actes.splice(+b.dataset.sup, 1); dessiner(); }
    else if (b.id === "fsVoir") apercu(); };
}
// Consultation choisie : sa date (date des soins des actes, « Le » de l'assuré et du médecin) ; « Saisie libre » : aujourd'hui
function choisirCons(id) {
  const c = F.cons.find((z) => z.id === id), d = c && c.d ? c.d : D().t;
  F.V.consId = c ? c.id : ""; F.V.d = d; F.V.le = d; F.V.leM = d; F.V.actes.forEach((a) => { a.d = d; });
  dessiner();
}
const valeursFeuille = () => Object.assign({}, F.V, { montant: totalActes(F.V.actes) ? montantTxt(totalActes(F.V.actes)) : "", assNom: F.V.lien ? F.V.assNom : F.V.malNom, assCin: F.V.lien ? F.V.assCin : F.V.malCin });
// Format de la page imprimée : A4 paysage, la feuille aussi grande que possible sans être déformée
const tailleMm = (f) => { const ar = f.w / f.h, W = Math.min(295, 208 * ar); return [Math.round(W * 10) / 10, Math.round((W / ar) * 10) / 10]; };
function apercu() {
  const esc = A.esc, x = x0(), f = FORMULAIRES[F.k], V = valeursFeuille();
  if (!V.malNom) { A.erreur("Indiquez le nom du malade."); return; }
  A.fenetre('<div class="pg-form fs-form"><h3>Aperçu — feuille de soins ' + esc(f.nom) + " — " + esc(x.r.nm) + "</h3>" +
    '<label class="chk" style="margin:0 0 10px"><input type="checkbox" id="fsFond"' + (F.fond ? " checked" : "") + "> Imprimer le fond du formulaire (à décocher pour imprimer sur la feuille officielle)</label>" +
    '<div class="fs-apercu" id="fsAp">' + rendreFeuille(F.k, V, { fond: true }) + "</div>" +
    '<div class="boutons"><button class="bt gris" id="fsRet">Modifier</button><button class="bt gris" onclick="fsFermer()">Annuler</button><button class="bt plein" id="fsImp">' + A.ic("imprimer") + "Imprimer</button></div></div>", "page");
  $("fsFond").onchange = () => { F.fond = $("fsFond").checked; };
  $("fsRet").onclick = () => dessiner();
  $("fsImp").onclick = () => imprimer();
}
function imprimer() {
  const x = x0(), f = FORMULAIRES[F.k], [W, H] = tailleMm(f), base = location.href.replace(/[#?].*$/, "").replace(/[^/]*$/, "");
  let w = null; try { w = window.open("", "_blank"); } catch (e) { w = null; }
  if (!w || !w.document) { A.toast("Autorisez l'ouverture des fenêtres pour imprimer la feuille de soins."); return; }
  const html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Feuille de soins ' + A.esc(f.nom) + "</title><style>@page{size:A4 landscape;margin:0}html,body{margin:0;padding:0}" + CSS_FEUILLE +
    ".fs-p{width:" + W + "mm;height:" + H + "mm;margin:" + Math.max(0, (210 - H) / 2).toFixed(1) + "mm auto 0;page-break-after:always;break-after:page}.fs-p:last-child{page-break-after:auto;break-after:auto}</style></head><body>" +
    rendreFeuille(F.k, valeursFeuille(), { fond: F.fond, base }) +
    "<script>(function(){var im=[].slice.call(document.images),n=im.length,go=function(){setTimeout(function(){window.focus();window.print();},150)};if(!n){go();return;}im.forEach(function(i){if(i.complete){if(!--n)go();}else{i.onload=i.onerror=function(){if(!--n)go();};}});})();<\/script></body></html>";
  w.document.open(); w.document.write(html); w.document.close();
  A.journal(x, "Feuille de soins " + f.nom + " imprimée (" + A.dfrA(F.V.d) + (totalActes(F.V.actes) ? ", " + montantTxt(totalActes(F.V.actes)) + " DH" : "") + ")");
}
window.fsFermer = () => { F = null; A.fermerFenetre(); };
