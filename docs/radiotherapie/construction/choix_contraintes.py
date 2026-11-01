# Choix des contraintes du 30/10/2026 (Dr Bentahila) : à appliquer après contraintes.py ecrire.
# Comparaison organe par organe et par nombre de séances entre la base (RecoRad 2025, stéréotaxie IGR 2018, compléments) et le relevé
# RadOncCalc du 30/10/2026 (docs/radiotherapie/choix-contraintes-rocc.html) ; Dr Bentahila a coché les lignes à garder
# (choix-contraintes-2026-10-30.json : « o:id » = ligne de la base gardée, « r:oar|séances|contrainte|organe RadOncCalc » = ligne ajoutée).
# - lignes de la base non cochées : retirées de la table, gardées dans retire-contraintes-2026-10-30.json ;
# - ligne de la base gardée dont RadOncCalc donne le même paramètre (Dmax / D0,03-0,1 cm³, Dmean, Vx Gy à ± 15 %, D cm³ du simple au double) :
#   les sources de RadOncCalc s'ajoutent à la sienne (plusieurs sources pour une même ligne) ;
# - lignes ajoutées : source = essais et recommandations d'origine cités par RadOncCalc (jamais RadOncCalc lui-même), effet évité si la fiche
#   a été lue ; 1 à 8 séances = stéréotaxie, 10 séances = stéréotaxie et hypofractionné, au-delà = hypofractionné, bifractionné = normofractionné
#   (1,5 Gy deux fois par jour).
# Données : radonccalc-2026-10-30.json (lignes retenues et sources ajoutées, préparé par comparer_radonccalc.py).
# Lancer : python3 docs/radiotherapie/construction/choix_contraintes.py
import json, pathlib, re, hashlib

ICI = pathlib.Path(__file__).resolve().parent
DR = ICI.parents[2] / "public" / "donnees-rt"
AVANT = ICI / "contraintes-2026-10-30-avant.json"
RETIRE = ICI / "retire-contraintes-2026-10-30.json"
CHOIX = json.loads((ICI / "choix-contraintes-2026-10-30.json").read_text())
ROCC = json.loads((ICI / "radonccalc-2026-10-30.json").read_text())

def fr(t):
  # écriture française d'une contrainte : virgule décimale, cm³, espace avant %
  t = re.sub(r"(\d)\.(\d)", r"\1,\2", t)
  t = re.sub(r"\s*-\s*(?=\d)", "–", t) if re.search(r"\d\s+-\s*\d|\d\s*-\s+\d", t) else t
  t = re.sub(r"\bcc\b", "cm³", t)
  t = re.sub(r"(\d)%", r"\1 %", t)
  return re.sub(r"\s{2,}", " ", t).strip()

SPECIALES = {"Avoid Hotspot": ("Point chaud", "à éviter"), "CV 24.8 Gy* ≥ 700 cc": ("Volume critique 700 cm³", "< 24,8 Gy"),
  "18 -20 Gy ALARA": ("Dose", "18–20 Gy, aussi basse que possible")}

# 01/11/2026 (demande de Dr Bentahila) : abréviations de RadOncCalc remplacées par le nom de la publication ou du groupe d'origine
NOMS = {"ASTRO HPV+ OP SqCC '...": "Recommandation ASTRO, oropharynx HPV+", "ASTRO Gastric '25": "Recommandation ASTRO, estomac (2025)",
  "ASTRO Pancreas '26": "Recommandation ASTRO, pancréas (2026)", "ASTRO PMRT '25": "Recommandation ASTRO, RT après mastectomie (2025)",
  "ASTRO Liver 2021": "Recommandation ASTRO, foie (2021)", "VA/ASTRO PRO '26": "Consensus VA / ASTRO, Practical Radiation Oncology 2026",
  "PRO Oligo '21": "Practical Radiation Oncology 2021, oligométastases", "Lakomy PRO '21": "Lakomy, Practical Radiation Oncology 2021",
  "NRG Heme '26": "Consensus NRG, hématologie (2026)", "NRG H&N SBRT": "NRG, stéréotaxie ORL",
  "UTSW": "UT Southwestern (Dallas)", "MDACC": "MD Anderson", "MSKCC": "Memorial Sloan Kettering", "Florida": "Université de Floride",
  "Florida - Peds": "Université de Floride, pédiatrie", "Timmerman '21": "Timmerman 2021, table des tolérances en stéréotaxie",
  "Timmerman": "Timmerman 2008, table des tolérances en stéréotaxie", "UK SABR '17": "Consensus britannique SABR 2017",
  "UK SABR '22": "Consensus britannique SABR 2022", "Casey ASO '20": "Casey, Annals of Surgical Oncology 2020",
  "Dickie IJROBP '09": "Dickie, IJROBP 2009", "Murphy IJROBP '10": "Murphy, IJROBP 2010", "George Clin Onc '20": "George, Clinical Oncology 2020",
  "Meade Clin Onc '18": "Meade, Clinical Oncology 2018", "ESTRO-EANO GBM": "Recommandation ESTRO-EANO, glioblastome",
  "ESTRO ACROP Pancreas '20": "Recommandation ESTRO-ACROP, pancréas (2020)"}
NCCN = {"H&N": "ORL", "NSCLC": "poumon non à petites cellules", "EsophGEJ": "œsophage et jonction", "Gastric": "estomac", "Pancreas": "pancréas",
  "Cervical": "col utérin", "Anal": "canal anal", "Hodgkin": "lymphome de Hodgkin", "Peds MB": "médulloblastome de l'enfant", "Wilms": "néphroblastome"}
def propre(s):
  s = re.sub(r"\s*🥇\s*", " ", s).strip()
  m = re.match(r"^VA (Breast|H&N|Lung|Prostate|Rectal) (\d{4})$", s)
  if m: return "Consensus VA (Veterans Affairs), " + {"Breast": "sein", "H&N": "ORL", "Lung": "poumon", "Prostate": "prostate", "Rectal": "rectum"}[m.group(1)] + " " + m.group(2)
  m = re.match(r"^NCCN (.+) (\d\.\d{4})$", s)
  if m and m.group(1) in NCCN: return "Recommandations NCCN, " + NCCN[m.group(1)] + " (version " + m.group(2) + ")"
  return NOMS.get(s, s)
# ligne à deux valeurs selon le stade (lisible : une ligne par stade)
COUPER = {"cb-e96dd7e0": [("ideal", "< 65 Gy", "cancer du cavum, stade précoce"), ("ideal", "< 70 Gy", "cancer du cavum, stade localement avancé")],
  "cb-6d8888dc": [("limitant", "< 65 Gy", "cancer du cavum, stade précoce"), ("limitant", "< 70 Gy", "cancer du cavum, stade localement avancé")]}

def couper(c):
  if c in SPECIALES: return SPECIALES[c]
  m = re.match(r"^([DV][^≤≥<>]*?)\s*([≤≥<>])\s*(.+)$", c)
  if not m: return fr(c), ""
  return fr(m.group(1)).replace(" ", ""), m.group(2) + " " + fr(m.group(3))

def regimes(g):
  if g == "N": return [("normo", None, None, "")]
  if g == "BID": return [("normo", None, 1.5, "bifractionné : 1,5 Gy deux fois par jour")]
  n = int(g)
  if n <= 8: return [("stereo", n, None, "")]
  if n == 10: return [("stereo", n, None, ""), ("hypo", n, None, "")]
  return [("hypo", n, None, "")]

def ecrire():
  if not AVANT.exists(): AVANT.write_text((DR / "contraintes.json").read_text())
  avant = json.loads(AVANT.read_text())
  gardes = {c[2:] for c in CHOIX if c.startswith("o:")}
  plus = ROCC["sources_plus"]
  base, retire = [], []
  for l in avant["base"]:
    if l["id"] not in gardes: retire.append(l); continue
    x = dict(l)
    p = plus.get(l["id"])
    if p:
      deja = x.get("source", "")
      ajout = [propre(s) for s in p["src"] if propre(s) not in deja]
      if ajout: x["source"] = deja + " ; " + " ; ".join(ajout)
      if p.get("effet"): x["effet"] = p["effet"]
    x["source"] = " ; ".join(dict.fromkeys(propre(s) for s in x.get("source", "").split(" ; ") if s.strip()))
    if l["id"] in COUPER:
      for i, (k, v, n) in enumerate(COUPER[l["id"]]):
        y = dict(x, id=l["id"] + ("" if i == 0 else "-" + str(i + 1)), note=n); y[k] = v; base.append(y)
      continue
    base.append(x)
  for a in ROCC["ajouts"]:
    ind, lim = couper(a["c"])
    src = [propre(s) for s in (list(a["src"]) or list((a["det"] or {}).get("refs") or []))]
    for reg, fx, dpf, note in regimes(a["g"]):
      x = {"oar_id": a["oar_id"], "regime": reg}
      if fx: x["fx"] = fx
      if dpf: x["dpf"] = dpf
      x["indicateur"] = ind
      if lim: x["limitant"] = lim
      n = "; ".join(v for v in [fr(a["prv"]).replace("PRV ", "PRV, marge ") if a["prv"] else "", note] if v)
      if n: x["note"] = n
      x["source"] = " ; ".join(src) if src else "Source à préciser"
      e = (a["det"] or {}).get("effet_fr")
      if e: x["effet"] = e
      h = hashlib.sha1(json.dumps(x, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:8]
      x = {"id": "cr-" + h, **x}
      if not any(y["id"] == x["id"] for y in base): base.append(x)
  sortie = dict(avant, base=base,
    note=avant["note"] + " Choix du 30/10/2026 : lignes gardées par Dr Bentahila, sources des essais ajoutées quand RadOncCalc donne le même paramètre, lignes des essais (High Yield, Must) ajoutées.")
  (DR / "contraintes.json").write_text(json.dumps(sortie, ensure_ascii=False, indent=1) + "\n")
  RETIRE.write_text(json.dumps(retire, ensure_ascii=False, indent=1) + "\n")
  print(len(base), "lignes de base ;", len(retire), "retirées ;", sum(1 for l in base if l["id"].startswith("cr-")), "ajoutées")

if __name__ == "__main__":
  ecrire()
