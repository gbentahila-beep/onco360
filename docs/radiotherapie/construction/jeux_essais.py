# Phase RTX, lot 2 (01/11/2026, demande de Dr Bentahila) : contraintes de chaque protocole. À lancer après choix_contraintes.py.
# - schéma dont l'essai publie ses contraintes : jeu propre à l'essai (jeux-essais.json « jeux », recopié du protocole publié) dans
#   contraintes.json « essais », relié par contraintes_ids ; les organes contourés que l'essai ne cite pas prennent la base (renvoi à l'écran) ;
# - autre schéma d'une localisation revue : ct_mention = « L'essai ne publie pas de contraintes : base de contraintes appliquée. »
#   (protocole institutionnel seul : « Le protocole ne publie pas de contraintes propres… »).
# Lancer : python3 docs/radiotherapie/construction/jeux_essais.py
import json, pathlib

ICI = pathlib.Path(__file__).resolve().parent
DR = ICI.parents[2] / "public" / "donnees-rt"
J = json.loads((ICI / "jeux-essais.json").read_text())
ecrire = lambda p, d: p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")

def appliquer():
  c = json.loads((DR / "contraintes.json").read_text())
  ids = {j["id"] for j in J["jeux"]}
  c["essais"] = [j for j in c["essais"] if j["id"] not in ids] + J["jeux"]
  ecrire(DR / "contraintes.json", c)
  E = {e["id"]: e for e in json.loads((DR / "essais.json").read_text())["essais"]}
  n = {"jeu": 0, "mention": 0}
  for loc in J["regions_revues"]:
    p = DR / (loc + ".json"); d = json.loads(p.read_text())
    for s in d.get("schemas", []):
      s.pop("ct_mention", None)
      r = J["schemas"].get(s["id"])
      if r:
        s["contraintes_ids"] = r["contraintes_ids"]; n["jeu"] += 1
      elif not s.get("contraintes_ids"):
        ty = [(E.get(e) or {}).get("type") for e in s.get("essai_ids", [])]
        k = "service" if not ty else "essai" if "essai" in ty else "institutionnel" if "protocole_institutionnel" in ty else "recommandation"
        s["ct_mention"] = J["mentions"][k]; n["mention"] += 1
    ecrire(p, d)
  print(len(J["jeux"]), "jeux ;", n["jeu"], "schémas reliés à un jeu ;", n["mention"], "mentions")

if __name__ == "__main__":
  appliquer()
