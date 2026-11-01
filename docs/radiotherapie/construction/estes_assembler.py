# Phase RTX, lot 6e (01/11/2026) : rassemble les fiches de estes_<site>.py dans estes-essais.json, en reliant chaque fiche à son article.
# Entrées : un index texte de la Bibliothèque (chemin <tab> texte des 2 premières pages, un article par ligne, fichier bib_tout.tsv du dossier donné).
# Usage : python3 estes_assembler.py <dossier de bib_tout.tsv> <dépôt> <site>   (ex. sein, digestif, orl…)
import json, re, sys, importlib.util, unicodedata, pathlib
S, depot, site = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3]
C = depot / "docs/radiotherapie/construction"
spec = importlib.util.spec_from_file_location("m", C / f"estes_{site}.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
bib = [l.rstrip("\n").split("\t", 1) for l in open(S + "/bib_tout.tsv")]; bib = [(b[0], b[1] if len(b) > 1 else "") for b in bib]
def n(s): return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())
out = json.loads((C / "estes-essais.json").read_text()) if (C / "estes-essais.json").exists() else {"essais": []}
out["essais"] = [e for e in out["essais"] if e["localisation"] != m.LOC]
ids = {e["id"] for e in out["essais"]}
for acr, revue, an, pop, bras, res, f in m.F:
  tr = [(p, t) for p, t in bib if p.endswith(f)]
  if not tr: print("INTROUVABLE", acr, f); continue
  # préférer Radiothérapie/, sinon le premier
  tr.sort(key=lambda x: (not x[0].startswith("Radiothérapie/"), x[0])); p, t = tr[0]
  ok = str(an) in t[:4000] or str(an) in p
  doi = None
  mm = re.match(r"(10\.\d{4,}@.+)\.pdf$", f)
  if mm: doi = mm.group(1).replace("@", "/")
  else:
    d = re.search(r"(?:doi\.org/|DOI:? ?|doi:? ?)(10\.\d{4,}/[^\s,;]+)", t[:2500], re.I)
    if d: doi = d.group(1).rstrip(".")
  if doi and (doi.count("(") != doi.count(")")): doi = doi.rstrip(")") if doi.count(")") > doi.count("(") else None
  if doi and (len(doi) < 18 or doi[-1] in "-./" or re.search(r"\.(19|20)\d\d$", doi)): doi = None
  base = "es-" + n(acr)[:28]; i = base; k = 2
  while i in ids: i = base + str(k); k += 1
  ids.add(i)
  x = {"id": i, "acronyme": acr, "type": "essai", "revue": revue, "annee": an, "population": pop, "bras": bras, "resultat": res, "localisation": m.LOC, "bibliotheque": p}
  if doi: x["doi"] = doi
  out["essais"].append(x)
  print(("   " if ok else "AN?"), acr[:40].ljust(40), an, (doi or "")[:40], "|", re.sub(r"\s+", " ", t[:90]))
(C / "estes-essais.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
print(len(out["essais"]), "fiches au total")
