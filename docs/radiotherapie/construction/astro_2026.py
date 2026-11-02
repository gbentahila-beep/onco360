# Consensus VA / ASTRO 2026 (02/11/2026, demande de Dr Bentahila : « l'article est de confiance : je préfère le croire ») : compendium des contraintes
# de dose de l'ASTRO (Puckett, Pract Radiat Oncol 2026), 25 tableaux relus sur les pages de l'article et figés dans astro-2026.json.
# - un jeu de contraintes par tableau (ct-astro-tNN ; tableau 1 aussi sans les aires ganglionnaires, ct-astro-t01-sein), rattaché aux protocoles retenus
#   par Dr Bentahila (CARTE) ; chaque ligne porte sa source (l'article et les références qu'il cite) ; couverture des cibles en lignes « cible » ;
#   lignes réservées à une localisation (loc) ou exclues d'une localisation (hors) : « oropharynx seulement », « sauf cavité buccale » ;
# - jeu FAST-Forward 40 Gy / 15 fx retiré des fiches START (40,05 Gy / 15 fx) et du CCIS (DBCG HYPO) ; l'article ajouté à l'onglet Essais ;
# - organes cités par l'article et absents du contourage de la fiche : ajoutés à la liste du contourage ;
# - page Contraintes (base) : contrainte absente ajoutée (localisations et protocoles du tableau, champ « schemas » : jamais dans une autre fiche),
#   contrainte déjà là : l'article ajouté
#   à ses sources, article cité à tort (valeur absente de l'article) : retiré des sources (MAL_ATTRIBUEES) ;
# - trois protocoles poumon neufs (tableaux 12, 17 et 18), voir NEUFS.
# Idempotent (repart des lignes ct-astro et va26- retirées). Lancer, puis essais_sources.py :
#   python3 docs/radiotherapie/construction/astro_2026.py && python3 docs/radiotherapie/construction/essais_sources.py
import json, pathlib, re

C = pathlib.Path(__file__).resolve().parent
R = C.parents[2] / "public" / "donnees-rt"
lire = lambda f: json.loads((R / f).read_text())
def ecrire(f, d): (R / f).write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
A = json.loads((C / "astro-2026.json").read_text())
VA, VA_ID, VA_ACR = A["source"], "src-va-astro-2026", "Consensus VA / ASTRO 2026"
DATE = "2026-11-02"
TYPES = {"rte_normo": "Normofractionné", "rte_hypo": "Hypofractionné", "sbrt": "Stéréotaxie", "curie_ldr": "Curiethérapie", "curie_hdr": "Curiethérapie", "curie_pdr": "Curiethérapie", "rte_plus_curie": "RTE + curiethérapie"}

# Protocoles retenus par tableau (décisions de Dr Bentahila du 02/11/2026) ; « 1s » = tableau 1 sans les aires ganglionnaires
CARTE = {
  "1": "sein-gg-50-25 sein-pna-50-25 sein-occulte-50 sein-en-place-50-boost",
  "1s": "sein-50-25 sein-paroi-50-25 sein-sib-504-644 ccis-50-25 ccis-50-25-boost ccis-paget-50-25",
  "2": "sein-40-15 sein-40-15-boost16 sein-425-16 sein-paroi-40-15 ccis-40-15 ccis-425-16-boost sein-ipb-40-15",
  "3": "sein-gg-40-15", "4": "sein-ipb-30-5", "5": "sein-26-5 sein-26-5-boost-service",
  "6": "cb-70-35-curie cb-6996-33-service cav-loc-70-35-curie cav-av-70-35-curie cav-av-6996-33 cav-loc-6996-33 hyp-rct-70-35-curie hyp-induction-rt"
       " hyp-6996-33-service lar-rct-70-35-curie lar-induction-rt lar-6996-33-service oro-70-35-curie oro-70-35-6fx oro-6996-33-service sin-70-35-curie"
       " gs-70-35-curie inc-70 cb-postop-66-curie cb-postop-66-54-service cb-postop-60-54-service hyp-postop-66-curie hyp-postop-66-54-service"
       " hyp-postop-60-54-service lar-postop-66-curie lar-postop-66-54-service lar-postop-60-54-service oro-postop-66-curie oro-postop-66-54-service"
       " oro-postop-60-54-service gs-postop-66-curie gs-postop-60-54-service sin-postop-66-curie sin-postop-60-54-service inc-po-60 lar-t2-70-35",
  "7": "lar-t1-63-28 lar-t1-5625-25",
  "8": "foie-chc-45-3 foie-meta-45-3 foie-meta-60-3 foie-chc-recid-45", "9": "foie-chc-40-5", "10": "foie-cca-675-15",
  "11": "pou-rct-60-30 pou-rct-66-33 pou-cbpc-66-33 pou-cbpc-70-35 th-r2-60 th-excl-66",
  "12": "pou-sbrt-34-1", "13": "pou-sbrt-54-3 pou-sbrt-45-3", "14": "pou-sbrt-48-4", "15": "pou-sbrt-50-5 pou-sbrt-55-5-igr pro-oligo-visc-50",
  "16": "pou-sbrt-60-8", "17": "pou-sabr-70-10", "18": "pou-hypo-60-15",
  "19": "pro-fav-78-39 pro-def-78-39 pro-pelv-seq-78 pro-m1-74-37 pro-def-flame",
  "20": "pro-fav-60-20 pro-def-60-20 pro-pelv-60-54", "21": "pro-fav-70-28 pro-pelv-70-28 pro-n1-70-28",
  "22": "pro-postop-66-33 pro-postop-spport pro-postop-service", "23": "pro-fav-sbrt-36",
  "24": "rec-504-28 rec-postop-558 rec-cap50 rec-prodige23 rec-cap45", "25": "rec-5x5-tme rec-5x5-delai rec-rapido",
}
FF, SANS_FF = "ct-sein-ff-15fx", ["sein-40-15", "sein-40-15-boost16", "sein-paroi-40-15", "ccis-40-15"]
# Régime et séances des lignes ajoutées à la page Contraintes (normofractionné : toutes les séances, comme le reste de la base)
REG = {1: ("normo", None, None), 2: ("hypo", 15, None), 3: ("hypo", 15, None), 4: ("hypo", 5, 6), 5: ("hypo", 5, 5.2), 6: ("normo", None, None),
       7: ("hypo", 28, None), 8: ("stereo", 3, None), 9: ("stereo", 5, None), 10: ("hypo", 15, None), 11: ("normo", None, None), 12: ("stereo", 1, None),
       13: ("stereo", 3, None), 14: ("stereo", 4, None), 15: ("stereo", 5, None), 16: ("stereo", 8, None), 17: ("stereo", 10, None), 18: ("hypo", 15, None),
       19: ("normo", None, None), 20: ("hypo", 20, None), 21: ("hypo", 28, None), 22: ("normo", None, None), 23: ("stereo", 5, None),
       24: ("normo", None, None), 25: ("hypo", 5, None)}
# Tableaux de même localisation, régime et séances : la note de la ligne ajoutée dit duquel il s'agit
CONTEXTE = {2: "sein ou paroi sans aires ganglionnaires", 3: "sein ou paroi avec aires ganglionnaires", 19: "prostate en place", 22: "loge prostatique"}
GG = re.compile(r"^(Sus-claviculaire|Axillaire|CMI) :")
# Lignes de la base qui citent l'article sans que la valeur y soit (relu le 02/11/2026) : l'article est retiré de leurs sources
MAL_ATTRIBUEES = {
  "cb-7ea7e8e5": "arbre bronchique, 3 fx : Dmax < 32–43 Gy, l'article dit D0,035cm³ ≤ 30 Gy",
  "cb-642338c0": "trachée, 3 fx : Dmax < 32–43 Gy, l'article dit ≤ 30 Gy",
  "cb-df027d08": "trachée, 5 fx : Dmax < 35 / < 38 Gy, l'article dit ≤ 40 Gy",
  "cb-5918fd6c": "trachée, 8 fx : Dmax < 40 Gy, l'article dit < 46,3 / < 56 Gy",
  "cb-d2238ce0": "canal médullaire, 8 fx : Dmax < 33,6 Gy, l'article dit < 32 Gy",
  "cb-4ae44786": "plexus brachial, 5 fx : Dmax < 30,5 / < 32,5 Gy, l'article dit ≤ 32 Gy",
  "cb-163379fc": "grêle, 5 fx : Dmax < 32–35 Gy, absent de l'article",
  "cr-e755e864": "grêle, 5 fx : V20Gy ≤ 50 cm³, absent de l'article",
  "cr-b00880b1": "vessie, 5 fx : V15Gy ≤ 50 %, l'article dit V18,1Gy < 40 %",
  "cb-3fb10d2e": "glandes sous-maxillaires : Dmean ≤ 35 Gy, l'article dit ≤ 39 / ≤ 10 Gy (controlatérale)",
  "cb-d9811151": "parotides : Dmean des deux ≤ 26 Gy, l'article dit parotide controlatérale",
  "cb-7d2c1f87": "mandibule : Dmax < 65 Gy, l'article dit ≤ 70 / ≤ 73,5 Gy",
  "cb-30659224": "tronc cérébral : Dmax ≤ 54 Gy, l'article dit ≤ 50 / < 52 Gy",
  "cb-8b79400c": "œsophage : V60Gy ≤ 30 %, l'article dit ≤ 15,3 / ≤ 17 %",
  "cb-3c4ce2dc": "poumon homolatéral (sein) : V20Gy ≤ 25 %, l'article dit ≤ 35 / ≤ 40 %",
  "cb-b33d9252": "vessie (rectum) : V40Gy < 35 %, absent de l'article",
}
# Lignes qui citent l'article pour une valeur voisine, gardées : arbre bronchique = « trachée et bronches souches » de l'article ; sigmoïde = côlon
GARDEES = {"cr-7cd6981f", "cr-2957d39d", "cr-31c331da", "cr-50584c19", "cr-dbd21a8c", "cr-a366719b"}

# Trois protocoles poumon neufs (décision de Dr Bentahila du 02/11/2026 : « on les crée en entier »), situation « Stéréotaxie pulmonaire »
COMMUNS = [  # points des fiches de stéréotaxie pulmonaire
  "Lésion centrale = PTV à moins de 2 cm de toute structure sensible (définition IASLC). Ultracentrale = PTV au contact de l'arbre bronchique proximal, du cœur, des vaisseaux pulmonaires ou de l'œsophage",
  "Patient opérable : SBRT non inférieure à la lobectomie dans STARS révisé (bras unique, comparaison appariée). Décision en RCP",
  "Surveillance : TDM à 3, 6 et 12 mois, puis tous les 6 mois pendant 3 ans, puis annuelle"]
def neuf(id_, titre, typ, preuve, essais, dose, fx, rythme, note, technique, sim, vol, points):
  return {"id": id_, "situation_id": "pou-sbrt", "titre": titre, "type": typ, "preuve": preuve, "essai_ids": essais,
          "prescriptions": [{"volume": "PTV", "dose_Gy": dose, "fractions": fx, "dose_fx_Gy": round(dose / fx, 4), "mode": "seul", "rythme": rythme, "note": note}],
          "technique": technique, "systemique": "Aucune", "simulation_id": sim, "volumes_id": vol, "contraintes_ids": [], "couverture": "",
          "points_attention": points, "date_verif": DATE, "couverture_lignes": []}
NEUFS = [  # (protocole, inséré après)
  (neuf("pou-sbrt-34-1", "SBRT 34 Gy / 1 fx (petite tumeur périphérique)", "sbrt", "recommandation", ["rtog0915", "src-nccn-cbnpc"], 34, 1, "Séance unique",
        "Tumeur périphérique T1–T2 N0, à plus de 2 cm de l'arbre bronchique proximal", "VMAT, inspiration bloquée ou 4D, CBCT avant et pendant la séance", "sim-pou-sbrt", "vol-pou-sbrt",
        ["RTOG 0915 (phase 2 randomisée, 94 patients) : 34 Gy / 1 fx aussi bien toléré que 48 Gy / 4 fx (toxicité de grade ≥ 3 : 10,3 vs 13,3 %) ; contrôle tumoral à 1 an 97 vs 92,7 %",
         "Tumeur périphérique seulement, à plus de 2 cm de l'arbre bronchique proximal (critère de RTOG 0915) ; NCCN : surtout tumeur de moins de 2 cm, à plus de 1 cm de la paroi thoracique",
         "Séance unique : CBCT avant le premier arc et entre les arcs ; écart os / tissu mou > 1 cm : appeler médecin et physicien"] + COMMUNS), "pou-sbrt-48-4"),
  (neuf("pou-sabr-70-10", "SBRT 70 Gy / 10 fx (central, volumineux ou au contact de la paroi)", "sbrt", "recommandation", ["src-li2014", "src-nccn-cbnpc"], 70, 10, "5 fx/sem",
        "Tumeur centrale, volumineuse ou au contact de la paroi thoracique ou du plexus brachial, non éligible à 50 Gy / 4 fx", "VMAT, scanner 4D, CBCT quotidien", "sim-pou-sbrt", "vol-pou-sbrt",
        ["MD Anderson (Li 2014, 82 patients non éligibles à 50 Gy / 4 fx) : survie à 2 ans 66,9 %, contrôle local 96,2 % ; pneumopathie de grade 3 : 2,4 %",
         "Mieux toléré que 50 Gy / 4 fx par la paroi thoracique et le plexus brachial. Paroi : V50Gy ≤ 60 cm³ (douleur pariétale au-delà, Li 2014)",
         "Tumeur envahissant l'arbre bronchique proximal : non indiqué (un décès par hémoptysie dans la série de Li 2014)"] + COMMUNS), "pou-sbrt-60-8"),
  (neuf("pou-hypo-60-15", "RT hypofractionnée 60 Gy / 15 fx (stade I, si la stéréotaxie n'est pas possible)", "rte_hypo", "essai_phase3", ["es-lustre", "src-nrglu004"], 60, 15, "5 fx/sem",
        "CBNPC stade I inopérable ; tumeur centrale ou ultracentrale", "VMAT, scanner 4D, CBCT quotidien", "sim-pou-sbrt-igr", "vol-pou-hypo",
        ["LUSTRE (phase 3, 233 CBNPC stade I inopérables) : contrôle local à 3 ans 82 % vs 88 % en stéréotaxie (p = 0,15), survie identique ; toxicité de grade 3-4 des tumeurs centrales 5 vs 11 %",
         "Option quand la stéréotaxie n'est pas réalisable : tumeur ultracentrale, gros volume, contraintes des organes non tenues",
         "Objectifs de couverture du PTV repris du protocole NRG LU004 (60 Gy / 15 fx)",
         "Séances quotidiennes ; CBCT quotidien"] + COMMUNS[:1] + COMMUNS[2:]), "pou-sbrt-50-10-igr"),
]
# Contourage : organe déjà contouré sous un nom voisin (pas de doublon dans la liste) ; volume commun à des fiches d'autres sites, laissé tel quel
VOISINS = [{"oar-moelle", "oar-canal-medullaire"}, {"oar-cochlees", "oar-oreilles-internes"}, {"oar-oesophage", "oar-oesophage-cervical"}]
VOL_LAISSES = {"vol-pro-oligo"}  # oligométastases (os, ganglions, viscères) : les organes du poumon n'y sont pas ajoutés
# organe sans valeur dans une autre fiche du même contourage (il reste dans l'onglet Contraintes par le jeu de l'article)
EXCLUS = {("vol-sein-ipb", "oar-sein-homolateral")}
VOL_NEUF = ("vol-pou-hypo", "vol-pou-sbrt-igr")  # contourage du 60 Gy / 15 fx : copie de celui de la SBRT 50 Gy / 10 fx, faite une fois
NON_RETENU = ("34 Gy / 1 fx (RTOG 0915, phase 2) : non retenu", "34 Gy / 1 fx (RTOG 0915, phase 2) : fiche à part, tumeur périphérique de petite taille")

def nom_ref(n): return A["references"][str(n)]["nom"]
def source(l): return " ; ".join([VA] + [nom_ref(r) for r in l["refs"]])
def tab(n): return next(t for t in A["tableaux"] if t["n"] == n)
def jid(k): return "ct-astro-t01-sein" if k == "1s" else "ct-astro-t%02d" % int(k)
def ligne_jeu(l):
  x = {k: l[k] for k in ("oar_id", "indicateur", "ideal", "limitant", "note", "loc", "hors") if k in l}
  x["source"] = source(l); return x

def jeux():
  J = []
  for k in CARTE:
    t = tab(int(k[:-1]) if k == "1s" else int(k)); L = [l for l in t["lignes"] if not (k == "1s" and GG.match(l["indicateur"]))]
    titre = t["titre"].replace("avec aires ganglionnaires", "sans les aires ganglionnaires") if k == "1s" else t["titre"]
    J.append({"id": jid(k), "titre": "Consensus VA / ASTRO 2026 : " + titre[0].lower() + titre[1:], "fractionnement": t["fractionnement"],
              "source": VA + ", tableau " + str(t["n"]), "verification": "verifie", "doi": A["doi"], "lignes": [ligne_jeu(l) for l in L]})
  return J

NUM = re.compile(r"\d+(?:,\d+)?")
def nombres(v): return {float(x.replace(",", ".")) for x in NUM.findall(v or "")}
def bornes(v): n = sorted(nombres(v)); return (n[0], n[-1]) if n else None
def classe(ind):
  i = re.sub(r"\s*\(.*\)$", "", ind or "")
  return "Dmax" if re.match(r"^(Dmax|D0,03(5)?cm³|D0,035–0,1cm³)$", i) else i
# précision entre parenthèses : sans effet quand elle redit l'organe (« poumons − ITV », « trachée et bronches souches ») ; absente d'un côté = compatible
NEUTRES = {"poumons − itv", "trachée et bronches souches"}
def precision(ind):
  m = re.search(r"\((.*)\)$", ind or ""); p = (m.group(1) if m else "").lower().replace("sain ", "")
  return "" if p in NEUTRES else p
def memes_precisions(a, b): pa, pb = precision(a), precision(b); return not pa or not pb or pa == pb
# V(x)Gy ≤ y cm³ = D(y)cm³ ≤ x Gy
def en_dose(ind, v):
  m, n = re.match(r"^V(\d+(?:,\d+)?)Gy", ind or ""), re.search(r"(\d+(?:,\d+)?)\s*cm³", v or "")
  return ("D" + n.group(1) + "cm³", "≤ " + m.group(1) + " Gy") if m and n else (ind, v)
def meme_valeur(a, b):
  # même nombre, ou nombre de l'article dans l'intervalle publié (« < 20,2–30 Gy »)
  for va, vb in ((a.get("limitant"), b.get("limitant")), (a.get("ideal"), b.get("ideal")), (a.get("limitant"), b.get("ideal")), (a.get("ideal"), b.get("limitant"))):
    na, bb = nombres(va), bornes(vb)
    if na and bb and any(bb[0] - 1e-6 <= x <= bb[1] + 1e-6 for x in na): return True
  return False

def main():
  c = lire("contraintes.json"); idx = lire("index.json"); oar = lire("oar.json"); O = oar["oar"] if "oar" in oar else oar
  cle = {o["id"]: o.get("somme") or o.get("paire") or o["id"] for o in O}
  membres = {}
  for o in O: membres.setdefault(cle[o["id"]], []).append(o["id"])
  J = jeux(); par_jeu = {j["id"]: j for j in J}
  c["essais"] = [j for j in c["essais"] if not j["id"].startswith("ct-astro-")] + J
  # trois protocoles poumon neufs (fichier de la localisation et index)
  pm = lire("poumon.json"); reg = {r["id"]: r["nom"] for r in idx["regions"]}; li = next(l for l in idx["localisations"] if l["id"] == "poumon")
  sit = next(x for x in pm["situations"] if x["id"] == "pou-sbrt")["titre"]; ids = {n["id"] for n, _ in NEUFS}
  pm["schemas"] = [x for x in pm["schemas"] if x["id"] not in ids]; idx["schemas"] = [x for x in idx["schemas"] if x["id"] not in ids]
  for n, apres in NEUFS:
    n = json.loads(json.dumps(n)); n["ind"] = [reg[pm["region_id"]], pm["nom"], sit, TYPES[n["type"]]]
    pm["schemas"].insert(next(i for i, x in enumerate(pm["schemas"]) if x["id"] == apres) + 1, n)
    e = {"id": n["id"], "localisation_id": "poumon", "situation_id": n["situation_id"], "titre": n["titre"], "type": n["type"], "preuve": n["preuve"], "essais": [],
         "doses": [{k: p[k] for k in ("volume", "dose_Gy", "fractions", "dose_fx_Gy")} for p in n["prescriptions"]], "ind": n["ind"]}
    idx["schemas"].insert(next(i for i, x in enumerate(idx["schemas"]) if x["id"] == apres) + 1, e)
  for x in pm["schemas"]: x["points_attention"] = [NON_RETENU[1] if q == NON_RETENU[0] else q for q in x["points_attention"]]
  for q in pm["points_attention"]:
    if q.get("point") == NON_RETENU[0]: q["point"] = NON_RETENU[1]
  if not any(v["id"] == VOL_NEUF[0] for v in pm["volumes"]):
    v = json.loads(json.dumps(next(v for v in pm["volumes"] if v["id"] == VOL_NEUF[1]))); v["id"] = VOL_NEUF[0]
    pm["volumes"].insert(next(i for i, x in enumerate(pm["volumes"]) if x["id"] == VOL_NEUF[1]) + 1, v)
  li["nb_schemas"] = len(pm["schemas"]); ecrire("poumon.json", pm)
  # protocoles : jeux, onglet Essais, contourage
  locs = {l["id"] for l in idx["localisations"]}; schemas, docs, avant = {}, {}, {}
  for lid in locs:
    d = lire(lid + ".json"); docs[lid] = d; avant[lid] = json.dumps(d, ensure_ascii=False)
    for s in d.get("schemas", []): schemas[s["id"]] = (lid, d, s)
  locs_tab, sch_tab, vus = {}, {}, set()
  for k, ids in CARTE.items():
    for sid in ids.split():
      lid, d, s = schemas[sid]; locs_tab.setdefault(int(k[:-1]) if k == "1s" else int(k), set()).add(lid); sch_tab.setdefault(int(k[:-1]) if k == "1s" else int(k), []).append(sid)
      ct = [x for x in s.get("contraintes_ids", []) if not x.startswith("ct-astro-") and not (sid in SANS_FF and x == FF)]
      s["contraintes_ids"] = ct + [jid(k)]
      if VA_ID not in s["essai_ids"]: s["essai_ids"] = s["essai_ids"] + [VA_ID]
      s.pop("ct_mention", None)
      if sid in SANS_FF:  # couverture de la fiche gardée, sans l'étiquette FAST-Forward (ce n'est pas le schéma de FAST-Forward)
        s["couverture"] = s.get("couverture", "").replace(" (FAST-Forward)", "")
        for cv in s.get("couverture_lignes", []):
          if cv.get("note") == "FAST-Forward": cv["note"] = ""
      vol = next(v for v in d["volumes"] if v["id"] == s["volumes_id"]); deja = {cle.get(x, x) for x in vol["oar_ids"]}
      deja |= {y for g in VOISINS if g & deja for y in g}
      if vol["id"] in VOL_LAISSES: deja = None
      for l in par_jeu[jid(k)]["lignes"]:
        if deja is None or l["oar_id"].startswith("cible-") or (l.get("loc") and lid not in l["loc"]) or (l.get("hors") and lid in l["hors"]): continue
        kk = cle.get(l["oar_id"], l["oar_id"])
        if kk not in deja and (vol["id"], kk) not in EXCLUS:
          vol["oar_ids"] += [x for x in (membres.get(kk) if kk not in cle else [kk]) if x not in vol["oar_ids"]]; deja.add(kk)
      vus.add(sid)
  # contourage commun à plusieurs localisations (vol-orl-igr…) : mêmes organes dans chaque fichier
  par_vol = {}
  for d in docs.values():
    for v in d["volumes"]: par_vol.setdefault(v["id"], []).append(v)
  for V in par_vol.values():
    tous = []
    for v in V: tous += [x for x in v["oar_ids"] if x not in tous]
    for v in V: v["oar_ids"] = [x for x in V[0]["oar_ids"]] + [x for x in tous if x not in V[0]["oar_ids"]]
  for lid, d in docs.items():
    if json.dumps(d, ensure_ascii=False) != avant[lid]: ecrire(lid + ".json", d)
  # index : essais affichés dans la liste (acronymes des fiches, dans l'ordre du protocole ; fiches neuves : celles d'astro-2026.json)
  ess = {e["id"]: e["acronyme"] for e in lire("essais.json")["essais"]}; ess[VA_ID] = VA_ACR
  ess.update({"src-nrglu004": "NRG LU004"}); ess.update({x["fiche"]["id"]: x["fiche"]["acronyme"] for x in A["references"].values() if "fiche" in x})
  for e in idx.get("schemas", []):
    if e["id"] in vus: e["essais"] = [ess[x] for x in schemas[e["id"]][2]["essai_ids"]]
  ecrire("index.json", idx)
  # page Contraintes
  base = [l for l in c["base"] if not l["id"].startswith("va26-")]
  for l in base: l["source"] = " ; ".join(s for s in l["source"].split(" ; ") if s != VA or l["id"] not in MAL_ATTRIBUEES) if l["id"] in MAL_ATTRIBUEES else l["source"]
  ajout, cites = [], set()
  for t in A["tableaux"]:
    n = t["n"]; rg, fx, dpf = REG[n]; lt = sorted(locs_tab.get(n, []))
    for i, l in enumerate(t["lignes"]):
      if l["oar_id"].startswith("cible-"): continue
      k = cle.get(l["oar_id"], l["oar_id"]); L = [l]
      # même régime ; 10 séances : hypofractionné ou stéréotaxie selon la page
      sl = [b for b in base if b["oar_id"] == k and (b["regime"] == rg or (fx and b.get("fx") == fx and {b["regime"], rg} <= {"hypo", "stereo"}))
            and (not b.get("fx") or not fx or b["fx"] == fx) and (not b.get("loc") or set(b["loc"]) & set(lt))]
      def pareil(b):
        ib, vb = en_dose(b["indicateur"], b.get("limitant")); il, vl = en_dose(l["indicateur"], l.get("limitant"))
        bb = dict(b, limitant=vb) if ib != b["indicateur"] else b; ll = dict(l, limitant=vl) if il != l["indicateur"] else l
        return classe(ib) == classe(il) and memes_precisions(ib, il) and meme_valeur(ll, bb)
      same = [b for b in sl if pareil(b)]
      if same:
        for b in same:
          cites.add(b["id"])
          if VA not in b["source"].split(" ; "): b["source"] += " ; " + VA
        continue
      x = {"id": "va26-t%02d-%02d" % (n, i), "oar_id": k, "regime": rg}
      if fx: x["fx"] = fx
      if dpf: x["dpf"] = dpf
      if lt: x["loc"] = lt
      # réservée aux protocoles du tableau : les autres fiches de la localisation gardent leurs contraintes
      x["schemas"] = sch_tab.get(n, [])
      x.update({kk: l[kk] for kk in ("indicateur", "ideal", "limitant") if kk in l})
      note = "; ".join(filter(None, [CONTEXTE.get(n, ""), l.get("note", "")])).replace("; ", " ; ")
      if note: x["note"] = note
      x["source"] = source(l); ajout.append(x)
  c["base"] = base + ajout
  ecrire("contraintes.json", c)
  restes = [b for b in base if VA in b["source"].split(" ; ") and b["id"] not in cites and b["id"] not in GARDEES]
  print(len(J), "jeux ;", len(vus), "protocoles ;", len(ajout), "contraintes ajoutées à la page Contraintes ;", len(cites), "déjà là (article ajouté aux sources)")
  for b in restes: print("  cite l'article sans valeur retrouvée :", b["id"], b["oar_id"], b["regime"], b.get("fx", ""), b["indicateur"], b.get("ideal", ""), b.get("limitant", ""))

if __name__ == "__main__":
  main()
