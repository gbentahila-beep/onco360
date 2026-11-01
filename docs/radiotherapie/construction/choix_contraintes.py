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

def propre(s): return re.sub(r"\s*🥇\s*", " ", s).strip()

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
