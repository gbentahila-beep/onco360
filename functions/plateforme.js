// Onco360 – lot L (31/10/2026) : logique pure de l'exploitation de la plateforme, sans Firebase (testée par functions/test-plateforme.js).
//   • L1 : erreurs JavaScript des utilisateurs, nettoyées de toute donnée de patient (nettoyerErreur), regroupées par jour (ajouterErreur) ;
//          résultat des traitements de nuit (resultatNuit) ;
//   • L6 : avis au titulaire quand l'Administration agit dans son cabinet (avisTitulaire), état du démarrage d'un cabinet (etatDemarrage),
//          date d'effacement d'un cabinet supprimé (dateEffacement, 30 jours) ;
//   • L9 : registre d'usage du mois par cabinet, sans aucune donnée de patient (usageCabinet).
"use strict";
const crypto = require("crypto");

// ───── L1 : erreurs ─────
const MAX_PAR_JOUR = 200; // empreintes différentes gardées par jour (les suivantes ne sont que comptées)
// Message d'erreur : sans texte entre guillemets (souvent une valeur saisie), sans nombre de 3 chiffres ou plus (téléphone, CIN, n° de dossier,
// identifiant), sans adresse e-mail ; 240 caractères au plus
function nettoyerMessage(m) {
  let s = String(m == null ? "" : m).replace(/[\r\n\t]+/g, " ");
  s = s.replace(/[\w.+-]+@[\w-]+(\.[\w-]+)+/g, "@");
  s = s.replace(/"[^"]*"|'[^']*'|`[^`]*`|«[^»]*»|“[^”]*”/g, "…");
  s = s.replace(/\d{3,}/g, "#");
  s = s.replace(/\s{2,}/g, " ").trim();
  return s.slice(0, 240);
}
// Fichier : chemin dans le site seulement (js/app/v2.js), sans adresse ni paramètres
function nettoyerFichier(f) {
  let s = String(f || "").split("?")[0].split("#")[0];
  const i = s.indexOf("/js/"); if (i >= 0) s = s.slice(i + 1); else s = s.replace(/^[a-z]+:\/\/[^/]+\//i, "");
  return /^[\w/.-]{1,120}$/.test(s) ? s : "";
}
const nombre = (n) => (Number.isFinite(+n) && +n >= 0 && +n < 1e7 ? Math.floor(+n) : 0);
// Page : premier mot de l'adresse (#dossier/…, #parametres/…) seulement, jamais l'identifiant d'un patient
const nettoyerPage = (p) => { const s = String(p || "").replace(/^#/, "").split(/[/?]/)[0]; return /^[a-z]{1,20}$/.test(s) ? s : ""; };
const nettoyerVersion = (v) => (/^[0-9a-z]{4,14}$/i.test(String(v || "")) ? String(v) : "");
function nettoyerErreur(x) {
  x = x || {};
  return { msg: nettoyerMessage(x.msg) || "(sans message)", src: nettoyerFichier(x.src), ligne: nombre(x.ligne), col: nombre(x.col), page: nettoyerPage(x.page), version: nettoyerVersion(x.version), type: x.type === "promesse" ? "promesse" : "erreur" };
}
const empreinte = (e) => crypto.createHash("sha1").update([e.type, e.msg, e.src, e.ligne].join("|")).digest("hex").slice(0, 12);
// Ajoute une erreur nettoyée au document du jour { total, l: { empreinte: { …, n, roles, cabinets, premier, dernier } }, debordement }
function ajouterErreur(jour, e, qui, le) {
  const j = jour && typeof jour === "object" ? JSON.parse(JSON.stringify(jour)) : {};
  j.total = (j.total || 0) + 1; j.l = j.l || {};
  const k = empreinte(e), r = String((qui && qui.role) || "").replace(/[^a-z]/g, "").slice(0, 20) || "inconnu", c = String((qui && qui.espace) || "").replace(/[^\w-]/g, "").slice(0, 60) || "aucun";
  if (!j.l[k]) {
    if (Object.keys(j.l).length >= MAX_PAR_JOUR) { j.debordement = (j.debordement || 0) + 1; return j; }
    j.l[k] = Object.assign({}, e, { n: 0, roles: {}, cabinets: {}, premier: le });
  }
  const o = j.l[k]; o.n++; o.dernier = le; o.roles[r] = (o.roles[r] || 0) + 1; o.cabinets[c] = (o.cabinets[c] || 0) + 1;
  return j;
}
// Erreurs d'un jour, les plus fréquentes d'abord
const erreursTriees = (jour) => Object.entries((jour && jour.l) || {}).map(([k, v]) => Object.assign({ k }, v)).sort((a, b) => b.n - a.n);

// Traitement de nuit : { le, ok, n (cabinets ou comptes traités), echecs [{ espace, erreur }] (20 au plus), duree (s) }
function resultatNuit(debut, fin, n, echecs) {
  const l = (echecs || []).slice(0, 20).map((x) => ({ espace: String(x.espace || "").slice(0, 60), erreur: nettoyerMessage(x.erreur && x.erreur.message ? x.erreur.message : x.erreur) }));
  return { le: new Date(fin).toISOString(), ok: !(echecs || []).length, n: n || 0, echecs: l, nbEchecs: (echecs || []).length, duree: Math.round((fin - debut) / 1000) };
}
// Alerte de la page « État de la plateforme » : traitement qui n'a pas tourné depuis plus de 30 h (7 jours 6 h pour l'export de la semaine)
const NUITS = [
  { k: "tachesAutoNuit", lib: "Tâches automatiques", h: 30 }, { k: "agendaNuit", lib: "Google Agenda (remise à plat)", h: 30 },
  { k: "releveNuit", lib: "Relevé du comptable", h: 30 }, { k: "fichiersNuit", lib: "Copie de secours des fichiers", h: 30 },
  { k: "abonnementsNuit", lib: "Abonnements", h: 30 }, { k: "suppressionsNuit", lib: "Cabinets supprimés (effacement après 30 jours)", h: 30 },
  { k: "exportsHebdo", lib: "Export de la semaine", h: 174 }, { k: "usageNuit", lib: "Registre d'usage", h: 30 },
];
function etatNuits(nuits, now) {
  return NUITS.map((d) => {
    const r = (nuits || {})[d.k] || null, t = r && r.le ? Date.parse(r.le) : 0;
    const alerte = !r ? "jamais exécuté depuis la mise en place du suivi" : now - t > d.h * 3600000 ? "pas exécuté depuis plus de " + d.h + " h" : r.ok ? "" : r.nbEchecs + " échec(s)";
    return Object.assign({ k: d.k, lib: d.lib }, r || {}, { alerte });
  });
}

// ───── L6 : Administration et cabinets ─────
// Actions de l'Administration dont le titulaire est prévenu (tableau de bord et journal du cabinet) ; jamais les siennes, jamais le modèle ni une
// bibliothèque, ni les actions qui ne touchent pas son cabinet
const SANS_AVIS = ["signalement", "bibliotheque", "demo", "heure", "packs", "creation", "specialite"];
function avisTitulaire({ par, type, espace, titulaire, demo, bib }) {
  if (!espace || bib || demo || /^bib-/.test(espace)) return false;
  if (!par || par === titulaire) return false;
  return SANS_AVIS.indexOf(type) < 0;
}
const JOURS_EFFACEMENT = 30;
const dateEffacement = (le) => new Date(new Date(le).getTime() + JOURS_EFFACEMENT * 86400000).toISOString();
const aEffacer = (x, now) => !!(x && x.actif === false && x.suppressionPrevue && Date.parse(x.suppressionPrevue) <= now);
// État du démarrage d'un cabinet (fiche de l'Administration) : rien de médical, seulement ce qui est réglé
function etatDemarrage(o) {
  o = o || {};
  const l = [
    { k: "profil", lib: "Profil du médecin (nom, INPE)", ok: !!o.profil },
    { k: "lieu", lib: "Lieu d'exercice", ok: (o.lieux || 0) > 0 },
    { k: "tarifs", lib: "Tarifs", ok: !!o.tarifs },
    { k: "equipe", lib: "Équipe (au moins un autre membre)", ok: (o.membres || 0) > 1 },
    { k: "agenda", lib: "Google Agenda relié", ok: !!o.agenda },
    { k: "export", lib: "Export des données (au moins un)", ok: !!o.export },
    { k: "patients", lib: "Premier dossier patient", ok: (o.patients || 0) > 0 },
  ];
  return { l, faits: l.filter((x) => x.ok).length, total: l.length };
}

// ───── L9 : registre d'usage ─────
// mois = "AAAA-MM" ; patients = données des dossiers (seuls lignesJson est lu, pour compter les séances validées du mois) ;
// consultations = [{ d }] ; membres = [{ actif, role }] ; actif = cabinet non suspendu
function usageCabinet({ espace, cabinet, actif, patients, consultations, membres }, mois) {
  let cures = 0, seances = 0;
  for (const p of patients || []) {
    let L = []; try { L = JSON.parse((p && p.lignesJson) || "[]") || []; } catch (e) { L = []; }
    for (const l of Array.isArray(L) ? L : []) for (const c of (l && l.cures) || []) {
      if (!c) continue;
      if (c.st === "recue" && String(c.reelle || "").slice(0, 7) === mois) { cures++; seances++; }
      for (const s of Object.values(c.sea || {})) if (s && s.st === "recue" && String(s.reelle || s.d || "").slice(0, 7) === mois) seances++;
    }
  }
  const actifs = (membres || []).filter((m) => m && m.actif !== false);
  const roles = {}; actifs.forEach((m) => { roles[m.role || "?"] = (roles[m.role || "?"] || 0) + 1; });
  return {
    espace, cabinet: String(cabinet || "").slice(0, 120), actif: actif !== false,
    dossiers: (patients || []).length, curesValidees: cures, seancesValidees: seances,
    consultations: (consultations || []).filter((c) => c && String(c.d || "").slice(0, 7) === mois).length,
    membres: actifs.length, roles,
  };
}
// Mois précédent d'une date (le registre du mois est écrit le 1er du mois suivant, puis tenu à jour chaque nuit pour le mois en cours)
const moisDe = (d) => new Date(d).toISOString().slice(0, 7);
const moisPrecedent = (m) => { const [a, n] = m.split("-").map(Number); return n === 1 ? (a - 1) + "-12" : a + "-" + String(n - 1).padStart(2, "0"); };

module.exports = { nettoyerMessage, nettoyerFichier, nettoyerPage, nettoyerErreur, empreinte, ajouterErreur, erreursTriees, MAX_PAR_JOUR, resultatNuit, NUITS, etatNuits,
  SANS_AVIS, avisTitulaire, JOURS_EFFACEMENT, dateEffacement, aEffacer, etatDemarrage, usageCabinet, moisDe, moisPrecedent };
