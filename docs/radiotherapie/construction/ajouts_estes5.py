# Phase RTX, lot 6e (01/11/2026) : les essais d'Estes versés dans l'onglet Essais (essais_estes.py) sont cités par les schémas dont ils ont testé
# le fractionnement ou l'indication ; un schéma neuf : liposarcome myxoïde 36 Gy / 18 fx (DOREMY, article dans la Bibliothèque › Sarcomes).
# Idempotent. Lancer après essais_estes.py, avant essais_sources.py : python3 docs/radiotherapie/construction/ajouts_estes5.py
from ajouts_estes import lire, ecrire, schema, P, DATE

LIENS = {
  "benin": {"bn-art-3": ["es-lordknea", "es-vanderbiltdovearthrose"], "bn-dup-30": ["es-depart"]},
  "poumon": {"pou-sbrt-48-4": ["es-lustre"], "pou-sbrt-60-8": ["es-lustre"]},
  "thymome": {"th-r0-50": ["es-jartomasathymus"]},
  "rectum": {"rec-5x5-tme": ["es-swedishrectalcancertrial", "es-mrccr07ncicctgc016", "es-polonaisi", "es-trog0104"],
             "rec-504-28": ["es-polonaisi", "es-trog0104", "es-nsabpr03", "es-caoaroaio12"],
             "rec-rapido": ["es-stellar", "es-polonaisii"], "rec-5x5-delai": ["es-startrec"]},
  "sein_ccis": {"ccis-50-25": ["es-swedcis", "es-eortc10853", "es-nsabpb17", "es-rtog9804", "es-ukanzdcis", "es-nsabpb24"]},
  "sein": {"sein-50-25": ["es-nsabpb06", "es-lyoncomplementde10gy"], "sein-ipb-hdr-32": ["es-budapestpolgar"]},
  "col": {"col-rch-hdr-5x55": ["es-metaanalyseradiochimiotherap", "es-rtog9001", "es-gog120"], "col-rch-hdr-5x6": ["es-metaanalyseradiochimiotherap", "es-rtog9001", "es-gog120"]},
  "endometre": {"endo-vbt-7x3-hir": ["es-portec4a", "es-orebrostadeiarisquesorbe2012"],
                "endo-pelv-46-23": ["es-gog99", "es-osloaalderssuivia20ansonsrud", "es-orebrostadeiarisquesorbe2012"]},
  "prostate": {"pro-fav-78-39": ["es-mdanderson70vs78gy"], "pro-def-78-39": ["es-mdanderson70vs78gy"]},
  "vessie": {"ves-pelv-65": ["es-rtog8903", "es-rtogpreservationvesicalemake"]},
  "seminome": {"se-20-10": ["es-mrcte19eortc30982"], "se-30-15": ["es-mrcte19eortc30982"]},
  "gliome": {"gli-oligo-594-33": ["es-codel"]},
  "meningiome": {"men-g1-srs": ["es-radiochirurgiedesmeningiomes", "es-pittsburghkondziolkameningio"]},
  "schwannome": {"sch-srs-12-1": ["es-thomasjeffersonandrewsschwan"]},
  "penis": {"pn-ldr-60": ["es-novasoutheasternhasancurieth"]},
  "rein": {"rein-26-1": ["es-londonontariocorreastereotax", "es-princessmargarethuangablatio"], "rein-42-3": ["es-londonontariocorreastereotax"]},
  "oropharynx": {"oro-70-35-6fx": ["es-iaeaacc"]},
  "cavum": {"cav-loc-70-35-curie": ["es-sunyatsennasopharynxbasrisqu"]},
  "pancreas": {"panc-adj-504-28": ["es-rtog9704"]},
  "estomac": {"est-int0116-45-25": ["es-seoulkim2005"]},
  "canal_anal": {"anal-act2-504": ["es-rtog8704"]},
}
SIT = "Sarcome localisé des membres ou du tronc : RT pré-opératoire"
DOREMY = schema("sm-preop-36-18", "sm-preop", "Liposarcome myxoïde : RT pré-opératoire 36 Gy / 18 fx", "rte_normo", "option", ["es-doremy"],
                [P("PTV", 36, 18, "Dose réduite, réservée au liposarcome myxoïde (DOREMY)")], "Membres et tronc", "Sarcomes", SIT, "vol-sm-preop-service", "sim-sarcome-service",
                ["Liposarcome myxoïde seulement : réponse histologique ≥ 50 % chez 91 %, contrôle local 100 %, complications de la plaie 16 % (DOREMY, phase 2 non randomisée, n = 79)",
                 "Chirurgie au moins 4 semaines après la fin de la RT"], tech="RT hautement conformationnelle, imagerie volumique quotidienne")

def main():
  A = {e["id"]: e["acronyme"] for e in lire("essais.json")["essais"]}
  idx = lire("index.json"); I = {s["id"]: s for s in idx["schemas"]}
  n = 0
  for f, L in LIENS.items():
    d = lire(f + ".json")
    for s in d["schemas"]:
      for e in L.get(s["id"], []):
        assert e in A, e
        if e not in s["essai_ids"]: s["essai_ids"].append(e); n += 1
      if s["id"] in L: I[s["id"]]["essais"] = [A[e] for e in s["essai_ids"]]
    assert all(k in {s["id"] for s in d["schemas"]} for k in L), f
    ecrire(f + ".json", d)
  sm = lire("sarcome_membres.json")
  sm["schemas"] = [s for s in sm["schemas"] if s["id"] != DOREMY["id"]]
  i = next(k for k, s in enumerate(sm["schemas"]) if s["id"] == "sm-preop-4275-15")
  sm["schemas"].insert(i + 1, DOREMY); sm["date_maj"] = DATE; ecrire("sarcome_membres.json", sm)
  idx["schemas"] = [s for s in idx["schemas"] if s["id"] != DOREMY["id"]]
  s = DOREMY
  idx["schemas"].append({"id": s["id"], "localisation_id": "sarcome_membres", "situation_id": s["situation_id"], "titre": s["titre"], "type": s["type"], "preuve": s["preuve"],
                         "essais": [A[e] for e in s["essai_ids"]], "doses": [{k: p.get(k) for k in ("volume", "dose_Gy", "fractions", "dose_fx_Gy")} for p in s["prescriptions"]], "ind": s["ind"]})
  for l in idx["localisations"]:
    if l["id"] == "sarcome_membres": l["nb_schemas"] = len(sm["schemas"]); l["date_maj"] = DATE
  ecrire("index.json", idx)
  print(n, "citations ajoutées ; 1 schéma (DOREMY)")

if __name__ == "__main__":
  main()
