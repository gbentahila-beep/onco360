// UX3 (02/11/2026) : fenêtres d'avertissement dans l'application, à la place de celles du navigateur (confirm, alert, prompt), pour Onco360
// et l'Administration. confirmer(texte, o) → vrai / faux ; alerte(texte, o) ; saisir(texte, valeur, o) → texte ou null. Ton : « rouge »
// (clinique), « orange » (à vérifier), « neutre ». Texte simple : un paragraphe par ligne vide, « • » = liste ; o.html = texte déjà en HTML.
// Échap = Annuler (ou Fermer) ; Entrée = le bouton qui a la main ; boutons nommés d'après la question (Supprimer, Retirer…) sauf o.oui / o.non.
const CSS = `.dlg-f{position:fixed;inset:0;background:rgba(30,42,68,.45);z-index:200;display:flex;align-items:center;justify-content:center;padding:16px}
.dlg-b{background:#fff;border-radius:14px;width:100%;max-width:520px;max-height:90vh;overflow:auto;box-shadow:0 24px 60px rgba(30,42,68,.28);border-top:5px solid #3563B0;font-family:inherit;color:#1E2A44}
.dlg-b.rouge{border-top-color:#C62828}.dlg-b.orange{border-top-color:#E08A00}
.dlg-c{display:flex;gap:12px;padding:20px 20px 6px}
.dlg-i{flex:none;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:18px;background:#E8EFFA;color:#3563B0}
.dlg-b.rouge .dlg-i{background:#FDECEC;color:#C62828}.dlg-b.orange .dlg-i{background:#FFF3DF;color:#B36B00}
.dlg-t{min-width:0;flex:1;font-size:15px;line-height:1.45;overflow-wrap:anywhere}
.dlg-t h4{margin:4px 0 8px;font-size:17px;color:#1E2A44}.dlg-t p{margin:0 0 8px}.dlg-t ul{margin:4px 0 8px 18px;padding:0}.dlg-t li{margin:3px 0}
.dlg-t input{display:block;width:100%;box-sizing:border-box;min-height:44px;margin:6px 0 4px;padding:8px 12px;border:1px solid #C9D3E3;border-radius:10px;font:inherit}
.dlg-p{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:10px;padding:12px 20px 18px}
.dlg-p button{min-height:44px;padding:0 18px;border-radius:10px;font:inherit;font-weight:bold;font-size:15px;cursor:pointer;border:1px solid #C9D3E3;background:#fff;color:#1E2A44}
.dlg-p button.oui{background:#3563B0;border-color:#3563B0;color:#fff}.dlg-p button.oui.rouge{background:#C62828;border-color:#C62828}.dlg-p button.oui.orange{background:#B36B00;border-color:#B36B00}
.dlg-p button:focus-visible{outline:3px solid #9DB8E6;outline-offset:2px}
@media (max-width:480px){.dlg-p button{flex:1}}`;
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
const enHtml = (t) => String(t == null ? "" : t).split(/\n\s*\n/).map((bloc) => {
  const l = bloc.split("\n").filter((x) => x.trim() !== ""), puces = l.filter((x) => /^\s*[•-]\s/.test(x));
  if (!l.length) return "";
  if (puces.length && puces.length === l.length) return "<ul>" + l.map((x) => "<li>" + esc(x.replace(/^\s*[•-]\s+/, "")) + "</li>").join("") + "</ul>";
  if (puces.length) { const i = l.findIndex((x) => /^\s*[•-]\s/.test(x)); return "<p>" + l.slice(0, i).map(esc).join("<br>") + "</p><ul>" + l.slice(i).map((x) => "<li>" + esc(x.replace(/^\s*[•-]\s+/, "")) + "</li>").join("") + "</ul>"; }
  return "<p>" + l.map(esc).join("<br>") + "</p>";
}).join("");
const style = () => { if (document.getElementById("dlgCss")) return; const s = document.createElement("style"); s.id = "dlgCss"; s.textContent = CSS; document.head.appendChild(s); };
// Boutons d'après la question : « Supprimer … ? » → Supprimer (rouge) ; « Annuler … ? » → Non / Oui, annuler ; sinon Confirmer
const VERBES = /^(Supprimer|Retirer|Effacer|Remettre|Rétablir|Reprendre|Rouvrir|Réattribuer|Se déconnecter|Récupérer|Remplacer|Délier|Quitter)\b/;
// « … Enregistrer quand même ? » → bouton « Enregistrer quand même », fenêtre orange (à vérifier)
function boutons(t, o) {
  const x = String(t || "").trim(), v = x.match(VERBES), ann = /^Annuler\b/.test(x), detruit = /^(Supprimer|Retirer|Effacer)\b/.test(x), qm = x.match(/([A-ZÉ][a-zéèêàç]+(?: le prix)? quand même)\b/);
  if (o.ton == null && /quand même/.test(x)) o.ton = "orange";
  return { oui: o.oui || (ann ? "Oui, annuler" : qm ? qm[1] : v ? v[1] : "Confirmer"), non: o.non || (ann ? "Non" : "Annuler"), rouge: o.ton === "rouge" || (o.ton == null && detruit) };
}
function ouvrir(o, corps, btn, lire) {
  style();
  return new Promise((res) => {
    const prec = document.activeElement, f = document.createElement("div"), ton = o.ton || "neutre";
    f.className = "dlg-f"; f.setAttribute("role", "alertdialog"); f.setAttribute("aria-modal", "true");
    f.innerHTML = '<div class="dlg-b ' + ton + '"><div class="dlg-c"><div class="dlg-i" aria-hidden="true">' + (ton === "neutre" ? "i" : "!") + '</div><div class="dlg-t">' +
      (o.titre ? "<h4>" + esc(o.titre) + "</h4>" : "") + corps + '</div></div><div class="dlg-p">' +
      btn.map(([k, l, c]) => '<button type="button" data-k="' + k + '" class="' + (c || "") + '">' + esc(l) + "</button>").join("") + "</div></div>";
    const fin = (k) => { f.remove(); document.removeEventListener("keydown", cle, true); try { if (prec && prec.focus && document.contains(prec)) prec.focus(); } catch (e) { /* rien */ } res(lire(k, f)); };
    const cle = (e) => {
      if (e.key === "Escape") { e.preventDefault(); e.stopImmediatePropagation(); fin(btn[0][0]); }
      else if (e.key === "Enter" && e.target && e.target.tagName === "INPUT" && f.contains(e.target)) { e.preventDefault(); e.stopImmediatePropagation(); fin("oui"); }
      else if (e.key === "Tab") { const l = [...f.querySelectorAll("button,input")]; const i = l.indexOf(document.activeElement);
        if (e.shiftKey ? i <= 0 : i === l.length - 1) { e.preventDefault(); l[e.shiftKey ? l.length - 1 : 0].focus(); } }
    };
    f.addEventListener("click", (e) => { const b = e.target.closest && e.target.closest("[data-k]"); if (b) fin(b.dataset.k); });
    document.addEventListener("keydown", cle, true); document.body.appendChild(f);
    const champ = f.querySelector("input"), oui = f.querySelector("button.oui");
    (champ || (o.focusNon || (oui && oui.classList.contains("rouge")) ? f.querySelector("button") : oui) || f.querySelector("button")).focus();
    if (champ) champ.select();
  });
}
export function confirmer(texte, o = {}) {
  const b = boutons(o.html ? "" : texte, o);
  return ouvrir(o, o.html ? texte : enHtml(texte), [["non", b.non, ""], ["oui", b.oui, "oui" + (b.rouge ? " rouge" : o.ton === "orange" ? " orange" : "")]], (k) => k === "oui");
}
export function alerte(texte, o = {}) {
  return ouvrir(o, o.html ? texte : enHtml(texte), [["ok", o.oui || "Fermer", "oui" + (o.ton === "rouge" ? " rouge" : o.ton === "orange" ? " orange" : "")]], () => undefined);
}
export function saisir(texte, valeur, o = {}) {
  return ouvrir(o, (o.html ? texte : enHtml(texte)) + '<input type="text" value="' + esc(valeur == null ? "" : valeur) + '" aria-label="' + esc(o.titre || String(texte || "").split("\n")[0]) + '">',
    [["non", o.non || "Annuler", ""], ["oui", o.oui || "Valider", "oui"]], (k, f) => (k === "oui" ? f.querySelector("input").value : null));
}
window.confirmer = confirmer; window.alerte = alerte; window.saisir = saisir;
