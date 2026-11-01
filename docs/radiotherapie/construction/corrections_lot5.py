# Lot 5 RTX (01/11/2026) : corrections des protocoles après comparaison avec les tables d'Estes (Oral Boards 2026, Key Studies 2025)
# et relecture des articles de la Bibliothèque. Seulement ce qu'un article de la Bibliothèque établit ; le reste est noté dans
# docs/radiotherapie/lot5-comparaison-estes.md. Lancer : python3 docs/radiotherapie/construction/corrections_lot5.py (idempotent).
import json, pathlib
DR = pathlib.Path(__file__).resolve().parents[2].parent / "public" / "donnees-rt"
# (fichier, schéma, n° de prescription, fractions, dose par fraction, rythme, source)
FX = [
  ("seminome", "se-iia-30", 0, 15, 2, "5 fx/sem", "Classen 2003 : 2,0 Gy par jour, 5 jours par semaine"),
  ("seminome", "se-iib-36", 0, 18, 2, "5 fx/sem", "Classen 2003 : 2,0 Gy par jour, 5 jours par semaine"),
  ("ependymome", "ep-g2-54", 0, 30, 1.8, "5 fx/sem", "Wee 2020 : dose médiane 54,0 Gy en 30 fractions (grade II)"),
  ("ependymome", "ep-g3-594", 0, 33, 1.8, "5 fx/sem", "Wee 2020 : dose médiane 59,4 Gy en 33 fractions (grade III)"),
  ("medulloblastome", "md-csi-352-552", 0, 22, 1.6, "5 fx/sem", "NOA-07 (Beier 2017) : irradiation craniospinale 1,6 Gy jusqu'à 35,2 Gy"),
]
for f, sid, i, n, dpf, ry, src in FX:
  p = DR / (f + ".json"); d = json.loads(p.read_text())
  s = next(x for x in d["schemas"] if x["id"] == sid); pr = s["prescriptions"][i]
  pr["fractions"], pr["dose_fx_Gy"], pr["rythme"] = n, dpf, ry
  note = pr.get("note", "")
  if src not in note: pr["note"] = (note + " ; " if note else "") + src
  p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
  print(sid, n, "fx")
# index : doses recopiées des fichiers de localisation
ip = DR / "index.json"; idx = json.loads(ip.read_text())
for f, sid, *_ in FX:
  s = next(x for x in json.loads((DR / (f + ".json")).read_text())["schemas"] if x["id"] == sid)
  e = next(x for x in idx["schemas"] if x["id"] == sid)
  e["doses"] = [{k: p[k] for k in ("volume", "dose_Gy", "fractions", "dose_fx_Gy") if p.get(k) is not None} for p in s["prescriptions"]]
ip.write_text(json.dumps(idx, ensure_ascii=False, indent=1) + "\n")
