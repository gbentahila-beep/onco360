// Tests de functions/plateforme.js (lot L, 31/10/2026) : node functions/test-plateforme.js
"use strict";
const P = require("./plateforme");
let ok = 0, ko = 0;
const t = (nom, c) => { if (c) { ok++; } else { ko++; console.log("✘ " + nom); } };

// L1 : aucune donnée de patient dans le message
const m = P.nettoyerMessage("Cannot read properties of undefined (reading 'Benali Fatima') at 0600001111, dossier 202610003, a.b@gmail.com\n« Rita »");
t("guillemets retirés", m.indexOf("Benali") < 0 && m.indexOf("Rita") < 0);
t("nombres retirés", m.indexOf("0600001111") < 0 && m.indexOf("202610003") < 0 && /#/.test(m));
t("e-mail retiré", m.indexOf("gmail") < 0);
t("message gardé", /Cannot read properties of undefined/.test(m));
t("longueur limitée", P.nettoyerMessage("x".repeat(1000)).length === 240);
t("fichier : chemin du site", P.nettoyerFichier("https://chimio-hgc.web.app/js/app/v2.js?v=20261031f") === "js/app/v2.js");
t("fichier étrange refusé", P.nettoyerFichier("javascript:alert(<b>)") === "");
t("page sans identifiant", P.nettoyerPage("#dossier/PTA1") === "dossier" && P.nettoyerPage("#Benali Fatima") === "");
const e = P.nettoyerErreur({ msg: "TypeError: x is null", src: "https://a.b/js/app/chimio.js", ligne: 120, col: "8", page: "#dossier/P1", version: "20261031f", nom: "Benali", type: "x" });
t("champs nettoyés", e.src === "js/app/chimio.js" && e.ligne === 120 && e.col === 8 && e.page === "dossier" && e.version === "20261031f" && e.type === "erreur" && !("nom" in e));
t("version étrange refusée", P.nettoyerErreur({ version: "<script>" }).version === "");
// Regroupement
let j = P.ajouterErreur(null, e, { role: "assistante", espace: "cab-a" }, "2026-10-31T09:00:00Z");
j = P.ajouterErreur(j, e, { role: "medecin", espace: "cab-b" }, "2026-10-31T10:00:00Z");
const k = P.empreinte(e);
t("même erreur regroupée", j.total === 2 && Object.keys(j.l).length === 1 && j.l[k].n === 2);
t("rôles et cabinets comptés", j.l[k].roles.assistante === 1 && j.l[k].roles.medecin === 1 && j.l[k].cabinets["cab-b"] === 1);
t("premier et dernier", j.l[k].premier === "2026-10-31T09:00:00Z" && j.l[k].dernier === "2026-10-31T10:00:00Z");
let g = null; for (let i = 0; i < P.MAX_PAR_JOUR + 5; i++) g = P.ajouterErreur(g, Object.assign({}, e, { ligne: i }), {}, "x");
t("limite par jour", Object.keys(g.l).length === P.MAX_PAR_JOUR && g.debordement === 5 && g.total === P.MAX_PAR_JOUR + 5);
t("tri par nombre", P.erreursTriees(j)[0].n === 2);
// Nuits
const r = P.resultatNuit(0, 65000, 3, [{ espace: "cab-a", erreur: new Error("quota dépassé pour 0600001111") }]);
t("résultat de nuit", !r.ok && r.n === 3 && r.duree === 65 && r.nbEchecs === 1 && r.echecs[0].erreur.indexOf("0600001111") < 0);
const now = Date.parse("2026-10-31T12:00:00Z");
const en = P.etatNuits({ releveNuit: { le: "2026-10-31T01:45:00Z", ok: true }, agendaNuit: { le: "2026-10-28T02:30:00Z", ok: true }, exportsHebdo: { le: "2026-10-25T00:30:00Z", ok: true } }, now);
t("nuit à l'heure", en.find((x) => x.k === "releveNuit").alerte === "");
t("nuit en retard", /plus de 30 h/.test(en.find((x) => x.k === "agendaNuit").alerte));
t("export de la semaine : 7 jours", en.find((x) => x.k === "exportsHebdo").alerte === "");
t("jamais exécuté", /jamais/.test(en.find((x) => x.k === "tachesAutoNuit").alerte));

// L6
t("avis : action de l'Administration", P.avisTitulaire({ par: "ADM", type: "reglage", espace: "cab-a", titulaire: "T" }));
t("pas d'avis : action du titulaire", !P.avisTitulaire({ par: "T", type: "abonnement", espace: "cab-a", titulaire: "T" }));
t("pas d'avis : bibliothèque, démo, signalement", !P.avisTitulaire({ par: "ADM", type: "reglage", espace: "bib-oncologie", titulaire: "T" }) && !P.avisTitulaire({ par: "ADM", type: "reglage", espace: "cab-d", titulaire: "T", demo: true }) && !P.avisTitulaire({ par: "ADM", type: "signalement", espace: "cab-a", titulaire: "T" }));
t("effacement à 30 jours", P.dateEffacement("2026-10-31T10:00:00.000Z") === "2026-11-30T10:00:00.000Z");
t("à effacer", P.aEffacer({ actif: false, suppressionPrevue: "2026-10-30T00:00:00Z" }, now) && !P.aEffacer({ actif: false, suppressionPrevue: "2026-11-30T00:00:00Z" }, now) && !P.aEffacer({ actif: true, suppressionPrevue: "2026-10-01T00:00:00Z" }, now));
const d = P.etatDemarrage({ profil: true, lieux: 2, tarifs: false, membres: 1, agenda: true, export: false, patients: 0 });
t("état du démarrage", d.faits === 3 && d.total === 7 && d.l.find((x) => x.k === "equipe").ok === false);

// L9
const pat = [{ lignesJson: JSON.stringify([{ cures: [{ st: "recue", reelle: "2026-10-05", sea: { 8: { st: "recue", reelle: "2026-10-12" }, 15: { st: "prevue" } } }, { st: "recue", reelle: "2026-09-20" }, { st: "prevue" }] }]), identite: { nom: "Benali" } }, { lignesJson: "pas du json" }, {}];
const u = P.usageCabinet({ espace: "cab-a", cabinet: "Cabinet A", actif: true, patients: pat, consultations: [{ d: "2026-10-03" }, { d: "2026-09-30" }, { d: "2026-10-31" }], membres: [{ actif: true, role: "medecin" }, { actif: false, role: "assistante" }, { role: "assistante" }] }, "2026-10");
t("dossiers", u.dossiers === 3);
t("cures et séances du mois", u.curesValidees === 1 && u.seancesValidees === 2);
t("consultations du mois", u.consultations === 2);
t("membres actifs", u.membres === 2 && u.roles.medecin === 1 && u.roles.assistante === 1);
t("aucune donnée de patient", JSON.stringify(u).indexOf("Benali") < 0);
t("suspendu", P.usageCabinet({ actif: false }, "2026-10").actif === false);
t("mois précédent", P.moisPrecedent("2026-01") === "2025-12" && P.moisPrecedent("2026-10") === "2026-09" && P.moisDe("2026-10-31T12:00:00Z") === "2026-10");

console.log((ko ? "✘ " : "✔ ") + "plateforme : " + ok + " réussis, " + ko + " en échec");
process.exit(ko ? 1 : 0);
