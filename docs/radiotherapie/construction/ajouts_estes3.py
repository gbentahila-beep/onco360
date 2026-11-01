# Phase RTX, lot 6c (01/11/2026) : stéréotaxie du cancer du rein primitif (localisation neuve, région Uro), d'après Bibliothèque › Urologie › Rein
# (FASTRACK II, IROCK). Idempotent. Lancer après ajouts_estes2.py, puis jeux_essais.py : python3 docs/radiotherapie/construction/ajouts_estes3.py
import json, pathlib
from ajouts_estes import DATE, lire, ecrire, schema, P

J = pathlib.Path(__file__).resolve().parent / "jeux-essais.json"

ESSAIS = [
  {"id": "fastrack2", "acronyme": "FASTRACK II (TROG 15.03)", "type": "essai", "revue": "Lancet Oncol 25:308", "annee": 2024,
   "population": "70 cancers du rein primitifs uniques, inopérables, à haut risque chirurgical ou refusant la chirurgie, ≤ 10 cm, DFG ≥ 30 mL/min, phase 2",
   "bras": "SABR 26 Gy / 1 fx (≤ 4 cm) ou 42 Gy / 3 fx (> 4 à 10 cm)",
   "resultat": "Contrôle local 100 % à 1 an ; toxicité de grade 3 : 10 %, aucune de grade 4 ; baisse moyenne du DFG 14,6 mL/min à 2 ans ; 1 dialyse"},
  {"id": "siva2022-irock5", "acronyme": "IROCK, résultats à 5 ans", "type": "essai", "revue": "Lancet Oncol 23:1508", "annee": 2022,
   "population": "190 cancers du rein primitifs traités par SABR, 12 centres, méta-analyse sur données individuelles",
   "bras": "SABR en 1 fraction (43 %) ou plusieurs fractions (57 %)",
   "resultat": "Échec local à 5 ans 5,5 % (moins en 1 fraction) ; baisse du DFG 14,2 mL/min à 5 ans ; 4 % de dialyses"},
  {"id": "siva2016-irock", "acronyme": "IROCK (consensus)", "type": "recommandation", "revue": "Future Oncol 12:637", "annee": 2016, "doi": "10.2217/fon.16.2",
   "population": "Pratiques de 8 centres de stéréotaxie rénale", "bras": "Consensus : sélection, simulation, volumes, doses, suivi",
   "resultat": "TDM 4D ou en phases respiratoires pour l'ITV ; PTV de 3 à 10 mm ; 1 à 12 fractions ; trajet de biopsie non couvert"},
]

LOC = "Rein"
SIT = {"id": "rein-sbrt", "localisation_id": "rein", "titre": "Cancer du rein primitif non opéré : stéréotaxie", "contexte": "en_place", "ordre": 1,
       "criteres": "Cancer du rein prouvé par biopsie, lésion unique ≤ 10 cm, T1–T2a N0–N1, inopérable, à haut risque chirurgical ou refusant la chirurgie ; DFG ≥ 30 mL/min ; pas de contact direct avec le tube digestif ; décision de RCP (FASTRACK II). Rein unique possible (IROCK)"}
VOL = {"id": "vol-rein", "cibles": [
  {"nom": "GTV", "type": "GTV", "definition": "Tumeur rénale sur le scanner injecté (± IRM)", "quand": "Toujours"},
  {"nom": "ITV", "type": "ITV", "definition": "GTV sur toutes les phases du scanner 4D (mouvement respiratoire)", "quand": "Toujours"}],
  "atlas": [], "oar_ids": ["oar-rein-d", "oar-rein-g", "oar-grele", "oar-duodenum", "oar-colon", "oar-estomac", "oar-foie", "oar-moelle"]}
SIM = {"id": "sim-rein", "position": "Décubitus dorsal, bras au-dessus de la tête", "preparation": "Contention du corps entier ; compression abdominale ou asservissement respiratoire selon le centre",
       "scanner": "Scanner 4D injecté (ITV) ; contrôle par imagerie volumique avant chaque séance"}
PTS = ["Marge de 3 mm (PRV) autour des organes creux (FASTRACK II)", "Surveiller la fonction rénale : baisse moyenne du DFG d'environ 14 mL/min, plus forte si le DFG de départ est bas"]
SCH = [
  schema("rein-26-1", "rein-sbrt", "Tumeur ≤ 4 cm : 26 Gy / 1 fx", "sbrt", "pratique_institutionnelle", ["fastrack2", "siva2022-irock5", "siva2016-irock"],
         [P("PTV", 26, 1, "99 % du PTV reçoit la dose prescrite", "1 fx")], LOC, "Uro", SIT["titre"], "vol-rein", "sim-rein", PTS, tech="SABR guidée par l'image"),
  schema("rein-42-3", "rein-sbrt", "Tumeur > 4 à 10 cm : 42 Gy / 3 fx", "sbrt", "pratique_institutionnelle", ["fastrack2", "siva2022-irock5", "siva2016-irock"],
         [P("PTV", 42, 3, "99 % du PTV reçoit la dose prescrite")], LOC, "Uro", SIT["titre"], "vol-rein", "sim-rein", PTS, tech="SABR guidée par l'image"),
]

def main():
  ess = lire("essais.json"); ids = {e["id"] for e in ESSAIS}
  ess["essais"] = [e for e in ess["essais"] if e["id"] not in ids] + ESSAIS; ecrire("essais.json", ess)
  A = {e["id"]: e["acronyme"] for e in ess["essais"]}
  idx = lire("index.json"); mes = {s["id"] for s in SCH}
  idx["schemas"] = [s for s in idx["schemas"] if s["id"] not in mes]
  idx["situations"] = [s for s in idx["situations"] if s["id"] != SIT["id"]]
  idx["localisations"] = [l for l in idx["localisations"] if l["id"] != "rein"]
  ordre = max(l["ordre"] for l in idx["localisations"]) + 1
  ref = lire("vessie.json")
  d = {"version": ref["version"], "id": "rein", "region_id": "uro", "nom": LOC, "ordre": ordre, "date_maj": DATE, "situations": [SIT], "schemas": SCH,
       "simulations": [SIM], "volumes": [VOL], "curie_indications": [], "systemique": [], "hormonotherapie": [], "points_attention": []}
  ecrire("rein.json", d)
  idx["situations"].append({k: SIT[k] for k in ("id", "localisation_id", "titre", "contexte", "criteres", "ordre")})
  for s in SCH:
    idx["schemas"].append({"id": s["id"], "localisation_id": "rein", "situation_id": s["situation_id"], "titre": s["titre"], "type": s["type"], "preuve": s["preuve"],
                           "essais": [A[e] for e in s["essai_ids"]], "doses": [{k: p.get(k) for k in ("volume", "dose_Gy", "fractions", "dose_fx_Gy")} for p in s["prescriptions"]], "ind": s["ind"]})
  idx["localisations"].append({"id": "rein", "nom": LOC, "region_id": "uro", "ordre": ordre, "date_maj": DATE, "nb_schemas": len(SCH), "curietherapie": False})
  ecrire("index.json", idx)
  j = json.loads(J.read_text())
  if "rein" not in j["regions_revues"]: j["regions_revues"].append("rein")
  J.write_text(json.dumps(j, ensure_ascii=False, indent=1) + "\n")
  print(len(SCH), "schémas,", len(ESSAIS), "essais")

if __name__ == "__main__":
  main()
