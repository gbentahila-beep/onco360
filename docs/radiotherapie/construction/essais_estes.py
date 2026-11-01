# Phase RTX, lot 6e (01/11/2026, demande de Dr Bentahila) : les essais d'Estes (Key Studies) dont l'article est dans la Bibliothèque Onco360
# et qui n'étaient pas encore dans le référentiel deviennent des fiches de l'onglet Essais (identifiants « es-… »).
# Fiches écrites site par site dans estes_<site>.py (chiffres d'Estes seulement), rassemblées dans estes-essais.json par estes_assembler.py ;
# ce script les verse dans essais.json : « localisation » = dossier de l'article dans la Bibliothèque, « bibliotheque » = son chemin.
# Une fiche dont le DOI ou l'acronyme existe déjà n'est pas ajoutée. Idempotent ; lancer avant ajouts_estes5.py puis essais_sources.py :
#   cd docs/radiotherapie/construction && python3 essais_estes.py && python3 ajouts_estes5.py && python3 essais_sources.py
import json, re, unicodedata, pathlib

ICI = pathlib.Path(__file__).resolve().parent
R = ICI.parents[2] / "public" / "donnees-rt"
DOSSIER = {
  "Cavité orale": "Cavité buccale", "Nasopharynx": "Cavum", "Poumon non à petites cellules": "Poumon", "Testicule": "Séminome testiculaire",
  "Méningiomes": "Méningiome", "Palliatif et métastases": "Palliatif", "Système nerveux central": "SNC",
}
# Articles rangés dans un autre dossier de la Bibliothèque que leur sujet
SUJET = {"POLCAGB (protocole)": "Foie et voies biliaires", "RPA RTOG (Gaspar)": "Métastases cérébrales"}

def cle(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())

def main():
  ess = json.loads((R / "essais.json").read_text())
  E = [e for e in ess["essais"] if not e["id"].startswith("es-")]
  dois = {e["doi"].lower() for e in E if e.get("doi")}
  acrs = {cle(e["acronyme"]) for e in E}
  neufs, ecartes = [], []
  for x in json.loads((ICI / "estes-essais.json").read_text())["essais"]:
    if (x.get("doi") and x["doi"].lower() in dois) or cle(x["acronyme"]) in acrs: ecartes.append(x["acronyme"]); continue
    x = dict(x)
    dos = x["bibliotheque"].split("/")[1:-1]
    x["localisation"] = SUJET.get(x["acronyme"]) or DOSSIER.get(dos[-1], dos[-1]) if dos else x["localisation"]
    neufs.append(x)
  ess["essais"] = E + neufs
  (R / "essais.json").write_text(json.dumps(ess, ensure_ascii=False, indent=1) + "\n")
  print(len(neufs), "fiches d'Estes versées ;", len(ecartes), "déjà présentes" + (" : " + ", ".join(ecartes) if ecartes else ""), ";", len(ess["essais"]), "fiches en tout")

main()
