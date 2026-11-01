# Sénorif 2026 (01/11/2026, demande de Dr Bentahila : « ne cite plus Sénorif 2021-2022 ») : référentiel sein de juillet 2026
# (Bibliothèque Onco360 › SENORIF-2026-09.pdf). Chaque phrase citant Sénorif a été relue dans la version 2026 : citation mise à jour, ou
# phrase réécrite quand la recommandation a changé (boost intégré 48 Gy / 15 fx de référence, hypofractionnement aussi avec chimiothérapie
# concomitante et reconstruction, CCIS hypofractionné en niveau de preuve fort, objectif cardiaque 3 / 5 Gy). Idempotent.
# Lancer : python3 docs/radiotherapie/construction/senorif_2026.py
import json, pathlib

DR = pathlib.Path(__file__).resolve().parents[3] / "public" / "donnees-rt"
NORMO = "Sénorif 2026 : le normofractionnement doit rester exceptionnel (tumeur phyllode, paroi traitée en électrons) ; le standard est 40,05 Gy / 15 fx"
NORMO_CCIS = "Sénorif 2026 : schéma recommandé 40,05 Gy / 15 fx (niveau de preuve fort), boost intégré 48 Gy / 15 fx si indiqué"
PHRASES = {
  "Le risque d'événement coronarien augmente de 7,4 % par gray de dose moyenne au cœur, sans seuil (Darby 2013) : objectif Dmoy < 5 Gy (Sénorif)":
    "Le risque d'événement coronarien augmente de 7,4 % par gray de dose moyenne au cœur, sans seuil (Darby 2013) : objectif Dmoy < 3 Gy pour le sein ou la paroi seuls, < 5 Gy avec les aires ganglionnaires (Sénorif 2026)",
  "Surimpression de référence normofractionnée (Sénorif) ; bras contrôle d'IMPORT HIGH ; option : 10 Gy / 5 fx de 2 Gy":
    "Surimpression séquentielle normofractionnée : option non inférieure, la référence étant le boost intégré 48 Gy / 15 fx (Sénorif 2026) ; bras contrôle d'IMPORT HIGH ; option : 10 Gy / 5 fx de 2 Gy",
  "Si indiquée ; surimpression de référence normofractionnée (Sénorif) ; option : 10 Gy / 5 fx de 2 Gy":
    "Si indiquée ; surimpression séquentielle normofractionnée : option non inférieure, la référence étant le boost intégré 48 Gy / 15 fx (Sénorif 2026) ; option : 10 Gy / 5 fx de 2 Gy",
  "Surimpression hypofractionnée : option de niveau de preuve très faible (Sénorif) ; FAST-Forward autorisait 10 ou 16 Gy en fractions de 2 Gy":
    "Surimpression hypofractionnée : pratique du service ; après 26 Gy / 5 fx, Sénorif 2026 recommande une surimpression normofractionnée de 10 à 16 Gy, comme FAST-Forward",
  "Sénorif : 63 à 64,4 Gy sur le lit en 28 fx": "Schéma de l'essai IMRT-MC2 ; Sénorif 2026 privilégie le boost intégré hypofractionné 48 Gy / 15 fx",
  "Normofractionné en cas de chimiothérapie concomitante (Sénorif, arbre 2)":
    "Sénorif 2026 : la chimiothérapie concomitante (capécitabine) et le trastuzumab ne contre-indiquent pas l'hypofractionnement modéré (40,05 Gy / 15 fx) ; 50 Gy / 25 fx reste possible",
  "Reconstruction mammaire : Sénorif 2021 recommande le normofractionnement ; le consensus ESTRO-ACROP 2022 admet l'hypofractionnement modéré pour le sein, la paroi (avec ou sans reconstruction) et les ganglions, et 5 fractions pour le sein ou la paroi sans reconstruction ni ganglions":
    "Reconstruction mammaire : Sénorif 2026 privilégie une RT modérément hypofractionnée en modulation d'intensité ; le consensus ESTRO-ACROP 2022 admet l'hypofractionnement modéré pour le sein, la paroi (avec ou sans reconstruction) et les ganglions, et 5 fractions pour le sein ou la paroi sans reconstruction ni ganglions",
  "Sénorif : 10 à 16 Gy en fractions de 2 Gy ; BIG 3-07 : 16 Gy / 8 fx":
    "Sénorif 2026 : boost intégré 48 Gy / 15 fx à privilégier, séquentiel de 10 à 16 Gy en fractions de 2 Gy en option ; BIG 3-07 : 16 Gy / 8 fx",
  "Bras hypofractionné de BIG 3-07 ; Sénorif écrit « 42 Gy en 16 fractions »": "Bras hypofractionné de BIG 3-07 ; Sénorif 2026 recommande 40,05 Gy / 15 fx",
  "Sénorif 2021 classe l'hypofractionnement du CCIS en niveau de preuve faible ; DBCG HYPO (2020) incluait des CCIS et BIG 3-07 (2022) a testé 42,5 Gy / 16 fx":
    "Sénorif 2026 classe l'hypofractionnement du CCIS (40,05 Gy / 15 fx) en niveau de preuve fort ; DBCG HYPO (2020) incluait des CCIS et BIG 3-07 (2022) a testé 42,5 Gy / 16 fx",
  "Lit tumoral : examen clinique préopératoire, mammographie, échographie, IRM, compte rendu opératoire, clips et anatomopathologie (Sénorif)":
    "Lit tumoral : examen clinique préopératoire, mammographie, échographie, IRM, scanner, compte rendu opératoire, clips et anatomopathologie (Sénorif 2026)",
  "Cancer du sein métastatique d'emblée bien contrôlé : RT de la maladie locorégionale macroscopique initiale, avec ou sans chirurgie ; pas de CMI sauf atteinte initiale (Sénorif)":
    "Cancer du sein métastatique d'emblée bien contrôlé : RT de la maladie locorégionale macroscopique initiale, avec ou sans chirurgie, en schéma hypofractionné ; pas de CMI sauf atteinte initiale (Sénorif 2026)",
  "Niveau de preuve faible (Sénorif)": "Niveau de preuve faible (Sénorif 2026, réirradiation)",
}
# schémas normofractionnés : point d'attention ajouté (recommandation 2026)
POINT = {"sein-50-25": NORMO, "sein-paroi-50-25": NORMO, "sein-gg-50-25": NORMO, "sein-en-place-50-boost":
  "Tumeur en place : Sénorif 2026 privilégie 40 Gy / 15 fx sur le sein et les aires ganglionnaires, puis une surimpression de la tumeur de 20 à 26 Gy en EQD2",
  "ccis-50-25": NORMO_CCIS, "ccis-50-25-boost": NORMO_CCIS, "ccis-paget-50-25": NORMO_CCIS}
ESSAI = {"id": "senorif-2026", "acronyme": "Sénorif 2026 — Référentiel sein (juillet 2026)", "type": "recommandation", "revue": "Réseau Sénorif (Île-de-France)",
  "annee": 2026, "population": "Cancers du sein", "bras": "Référentiel régional ; chapitres de radiothérapie (formes infiltrantes et in situ)",
  "resultat": "Indications, volumes, dose et fractionnement (hypofractionnement modéré standard, boost intégré 48 Gy / 15 fx) ; renvoie à RecoRad 2025 pour les contraintes, objectif cardiaque Dmoy < 3 Gy (sein seul) ou < 5 Gy (aires ganglionnaires)"}

def remplacer(x):
  if isinstance(x, dict): return {k: remplacer(v) for k, v in x.items()}
  if isinstance(x, list): return [remplacer(v) for v in x]
  if isinstance(x, str):
    if x == "senorif-2021": return "senorif-2026"
    if x == "Sénorif — Référentiel cancers du sein 2021-2022": return ESSAI["acronyme"]
    x = PHRASES.get(x, x)
    return x.replace("(Sénorif)", "(Sénorif 2026)").replace("(FAST-Forward ; Sénorif)", "(FAST-Forward ; Sénorif 2026)").replace("prolongements axillaires (Sénorif)", "prolongements axillaires (Sénorif 2026)").replace("(Sénorif, arbre 2)", "(Sénorif 2026)")
  return x

def appliquer():
  for p in sorted(DR.glob("*.json")):
    t = p.read_text()
    if "norif" not in t: continue
    d = remplacer(json.loads(t))
    if p.name == "essais.json":
      d["essais"] = [ESSAI if e["id"] == "senorif-2026" else e for e in d["essais"]]
    for s in d.get("schemas", []) if isinstance(d, dict) else []:
      if s.get("id") in POINT and POINT[s["id"]] not in s.get("points_attention", []): s.setdefault("points_attention", []).append(POINT[s["id"]])
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
  reste = [p.name for p in DR.glob("*.json") if "Sénorif)" in p.read_text() or "senorif-2021" in p.read_text() or "Sénorif 2021" in p.read_text() or "Sénorif :" in p.read_text()]
  print("restes :", reste)

if __name__ == "__main__":
  appliquer()
