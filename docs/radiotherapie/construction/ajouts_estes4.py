# Phase RTX, lot 6d (01/11/2026) : rattrapage après prostatectomie hypofractionné, d'après les protocoles de la Bibliothèque › Dosimétrie › Urologie :
# NRG-GU003 (COPORT / HYPORT, version du 26/04/2019 : volumes, simulation, contraintes du bras 62,5 Gy) et SHARE (version 1.8 du 02/09/2021).
# Idempotent. Lancer après ajouts_estes3.py, puis jeux_essais.py : python3 docs/radiotherapie/construction/ajouts_estes4.py
import json, pathlib
from ajouts_estes import DATE, lire, ecrire, schema, P

J = pathlib.Path(__file__).resolve().parent / "jeux-essais.json"
SIT = "Après prostatectomie — rattrapage précoce ou adjuvant"

GU003 = {"acronyme": "NRG-GU003 (HYPORT vs COPORT)",
         "population": "Après prostatectomie, pT2–pT3 pN0/Nx, PSA < 2 ng/mL, sans récidive locale ni métastase ; RT adjuvante ou de rattrapage ± hormonothérapie ≤ 6 mois, sans pelvis (n = 296)",
         "bras": "Loge 62,5 Gy / 25 fx de 2,5 Gy vs 66,6 Gy / 37 fx de 1,8 Gy ; PTV = CTV + 7 à 10 mm"}
SHARE = {"id": "share", "acronyme": "SHARE", "type": "essai", "revue": "J Clin Oncol", "annee": 2026,
         "population": "Récidive biologique après prostatectomie (PSA > 0,2 et ≤ 1 ng/mL), risque intermédiaire ou élevé (NCCN), sans récidive locale, ganglionnaire ni métastase, phase 3 (n = 316)",
         "bras": "Loge 65 Gy / 26 fx de 2,5 Gy vs 66 Gy / 33 fx ; pelvis au choix ; PTV = CTV + 3 à 7 mm ; IMRT",
         "resultat": "Contrôle biochimique à 4 ans 80 vs 78 % ; toxicité digestive de grade ≥ 2 : 8 vs 1 % (surtout rectorragies, toutes résolutives)"}

JEU = {"id": "ct-uro-hyport-62", "titre": "Loge prostatique, 62,5 Gy / 25 fx (NRG-GU003, HYPORT)", "fractionnement": "62,5 Gy / 25 fx",
       "source": "Protocole NRG-GU003 (version du 26/04/2019), § 5.2.7, contraintes du bras HYPORT", "verification": "verifie", "lignes": [
  {"oar_id": "oar-rectum", "indicateur": "V36Gy", "ideal": "< 55 %", "limitant": "< 60 %"},
  {"oar_id": "oar-rectum", "indicateur": "V59Gy", "ideal": "< 35 %", "limitant": "< 39 %"},
  {"oar_id": "oar-vessie", "indicateur": "V35Gy", "ideal": "< 70 %", "limitant": "< 77 %", "note": "vessie sans le CTV (le col vésical est dans le CTV)"},
  {"oar_id": "oar-vessie", "indicateur": "V57Gy", "ideal": "< 50 %", "limitant": "< 55 %"},
  {"oar_id": "oar-tete-femorale-d", "indicateur": "V44Gy", "ideal": "< 10 %", "limitant": "< 11 %"},
  {"oar_id": "oar-tete-femorale-g", "indicateur": "V44Gy", "ideal": "< 10 %", "limitant": "< 11 %"}]}

PTS_GU003 = ["Rectum le plus vide possible (< 3 cm d'avant en arrière, lavement 1 à 2 h avant), vessie confortablement pleine ; IGRT quotidienne, idéalement sur grains d'or (NRG-GU003)",
             "CTV de la loge selon le consensus RTOG (Michalski 2010) ; 95 % du PTV reçoit la dose prescrite, D0,03cc ≤ 115 %"]
SCH_SHARE = schema("pro-postop-65-26", "pro-postop", "Loge 65 Gy / 26 fx", "rte_hypo", "essai_phase3", ["share"],
                   [P("PTV_LOGE", 65, 26, "Pelvis possible au choix du radiothérapeute (dose non fixée par le protocole)")], "Prostate", "Uro", SIT, "vol-pro-loge", "sim-pro-loge",
                   ["Rattrapage pour PSA > 0,2 et ≤ 1 ng/mL ; hormonothérapie selon le centre",
                    "Plus de rectorragies qu'en 66 Gy / 33 fx (grade ≥ 2 : 8 vs 1 %) ; moins avec un ballonnet rectal (SHARE)"], tech="IMRT, IGRT", syst="Hormonothérapie selon le centre")

def main():
  ess = lire("essais.json")
  for e in ess["essais"]:
    if e["id"] == "nrg-gu003": e.update(GU003)
  ess["essais"] = [e for e in ess["essais"] if e["id"] != "share"] + [SHARE]; ecrire("essais.json", ess)
  A = {e["id"]: e["acronyme"] for e in ess["essais"]}

  pro = lire("prostate.json")
  for s in pro["schemas"]:
    if s["id"] == "pro-postop-62-25":
      s["points_attention"] = [p for p in s["points_attention"] if p not in PTS_GU003] + PTS_GU003
      s["technique"] = "IMRT ou VMAT, IGRT quotidienne"; s["date_verif"] = DATE
  pro["schemas"] = [s for s in pro["schemas"] if s["id"] != SCH_SHARE["id"]]
  i = next(k for k, s in enumerate(pro["schemas"]) if s["id"] == "pro-postop-62-25")
  pro["schemas"].insert(i + 1, SCH_SHARE); pro["date_maj"] = DATE; ecrire("prostate.json", pro)

  idx = lire("index.json")
  idx["schemas"] = [s for s in idx["schemas"] if s["id"] != SCH_SHARE["id"]]
  for s in idx["schemas"]:
    if s["id"] == "pro-postop-62-25": s["essais"] = [A["nrg-gu003"]]
  s = SCH_SHARE
  idx["schemas"].append({"id": s["id"], "localisation_id": "prostate", "situation_id": s["situation_id"], "titre": s["titre"], "type": s["type"], "preuve": s["preuve"],
                         "essais": [A[e] for e in s["essai_ids"]], "doses": [{k: p.get(k) for k in ("volume", "dose_Gy", "fractions", "dose_fx_Gy")} for p in s["prescriptions"]], "ind": s["ind"]})
  for l in idx["localisations"]:
    if l["id"] == "prostate": l["nb_schemas"] = len(pro["schemas"]); l["date_maj"] = DATE
  ecrire("index.json", idx)

  j = json.loads(J.read_text())
  j["jeux"] = [x for x in j["jeux"] if x["id"] != JEU["id"]] + [JEU]
  j["schemas"]["pro-postop-62-25"] = {"contraintes_ids": [JEU["id"]]}
  J.write_text(json.dumps(j, ensure_ascii=False, indent=1) + "\n")
  print("1 schéma, 1 essai, 1 jeu")

if __name__ == "__main__":
  main()
