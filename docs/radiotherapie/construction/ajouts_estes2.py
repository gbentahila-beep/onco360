# Phase RTX, lot 6b (01/11/2026) : situations d'Estes dont Dr Bentahila a téléchargé les articles (adénopathie cervicale sans primitif, sillon
# supérieur, dermatofibrosarcome, ostéosarcome, oligométastases de la prostate). Doses recopiées des articles et protocoles de la Bibliothèque.
# Idempotent. Lancer après ajouts_estes.py, puis jeux_essais.py : python3 docs/radiotherapie/construction/ajouts_estes2.py
import json, pathlib
from ajouts_estes import R, DATE, lire, ecrire, schema, P

J = pathlib.Path(__file__).resolve().parent / "jeux-essais.json"

def Ps(vol, d, n, note=""):
  x = P(vol, d, n, note); x["mode"] = "sequentiel"; return x

ESSAIS = [
  {"id": "maghami2020-asco", "acronyme": "ASCO 2020 (sans primitif)", "type": "recommandation", "revue": "J Clin Oncol 38:2570", "annee": 2020, "doi": "10.1200/JCO.20.00275",
   "population": "Carcinome épidermoïde ganglionnaire cervical sans primitif retrouvé", "bras": "Recommandations ASCO (Maghami 2020) : bilan, chirurgie, volumes et doses de RT, chimiothérapie",
   "resultat": "RT exclusive 70 Gy aux adénopathies, environ 50 Gy aux muqueuses à risque, 40 à 50 Gy aux aires électives ; post-opératoire 60 Gy (60 à 66 Gy si rupture capsulaire)"},
  {"id": "rusch2007-swog9416", "acronyme": "SWOG 9416 / INT 0160", "type": "essai", "revue": "J Clin Oncol 25:313", "annee": 2007, "doi": "10.1200/JCO.2006.08.2826",
   "population": "110 tumeurs du sillon supérieur T3-T4 N0-N1, phase 2", "bras": "Cisplatine + étoposide et RT 45 Gy / 25 fx, puis résection",
   "resultat": "Résection complète 76 % ; réponse histologique complète ou maladie minime 56 % ; survie à 5 ans 44 % (54 % après résection complète)"},
  {"id": "rusch2001-swog9416", "acronyme": "SWOG 9416 (premiers résultats)", "type": "essai", "revue": "J Thorac Cardiovasc Surg 121:472", "annee": 2001,
   "population": "Même essai, premiers résultats", "bras": "Cisplatine + étoposide et RT 45 Gy / 25 fx, puis résection",
   "resultat": "Résection complète 92 % des patients opérés ; 3 décès liés au traitement"},
  {"id": "castle2013-dfsp", "acronyme": "Castle 2013 (dermatofibrosarcome)", "type": "essai", "revue": "Int J Radiat Oncol Biol Phys", "annee": 2013, "doi": "10.1016/j.ijrobp.2013.02.001",
   "population": "53 dermatofibrosarcomes traités par chirurgie et RT (MD Anderson), rétrospectif", "bras": "RT pré-opératoire 50–50,4 Gy (13 %) ou post-opératoire 60–66 Gy (87 %) ; dose médiane 60 Gy",
   "resultat": "Contrôle local 98 % à 5 ans, 93 % à 10 ans"},
  {"id": "delaney2005-osteo", "acronyme": "DeLaney 2005 (ostéosarcome)", "type": "essai", "revue": "Int J Radiat Oncol Biol Phys", "annee": 2005, "doi": "10.1016/j.ijrobp.2004.05.051",
   "population": "41 ostéosarcomes non opérables ou à marges insuffisantes (MGH), rétrospectif", "bras": "RT médiane 66 Gy (CTV 45–50 Gy puis complément sur le GTV)",
   "resultat": "Contrôle local 71 % au-delà de 55 Gy ; meilleur sur un reliquat microscopique ou minime"},
  {"id": "oriole-protocole", "acronyme": "ORIOLE (protocole)", "type": "protocole_institutionnel", "revue": "Johns Hopkins J15180, version 4.1", "annee": 2015,
   "population": "Prostate hormonosensible oligométastatique (1 à 3 métastases), phase 2 randomisée", "bras": "SBRT de toutes les métastases vs surveillance",
   "resultat": "Doses types 16–24 Gy / 1 fx, 48–50 Gy / 4 fx, 50–60 Gy / 5 fx ; CTV = GTV, PTV = CTV + 5 mm"},
  {"id": "extend-protocole", "acronyme": "EXTEND (protocole)", "type": "protocole_institutionnel", "revue": "MD Anderson 2018-0349", "annee": 2018,
   "population": "Oligométastases (bras prostate : hormonothérapie), phase 2 randomisée", "bras": "Traitement standard ± traitement local de toutes les métastases (SBRT, chirurgie)",
   "resultat": "Doses par site : os 12–24 Gy / 1 fx ou 27–36 Gy / 3 fx ; ganglion 30–36 Gy / 3 fx ; poumon et foie 50 Gy / 4 fx ; contraintes par nombre de fractions"},
]

# ── Adénopathie cervicale sans primitif (localisation neuve, région ORL) ──
INC = "Adénopathie cervicale sans primitif"
INC_SIT = [
  {"id": "inc-ep", "titre": "Carcinome épidermoïde cervical sans primitif : RT exclusive", "contexte": "en_place", "ordre": 1,
   "criteres": "Après bilan complet (TEP, endoscopie, amygdalectomie, mucosectomie de la base de langue). Muqueuses : amygdale, voile et toute la base de langue homolatéraux si HPV+ N1 ; oropharynx bilatéral si N2c ; cavum seul (II–V et rétropharyngés bilatéraux) si EBV+ ; pas de muqueuse si origine cutanée suspectée. Cou bilatéral si plusieurs adénopathies, N3 ou rupture capsulaire ; homolatéral si adénopathie unique sans rupture (ASCO 2020)"},
  {"id": "inc-po", "titre": "Carcinome épidermoïde cervical sans primitif : après curage", "contexte": "post_op", "ordre": 2,
   "criteres": "RT si plusieurs ganglions envahis ou rupture capsulaire ; pas de RT pour un seul pN+ sans rupture (ASCO 2020)"},
]
for s in INC_SIT: s["localisation_id"] = "orl_inconnu"
INC_VOL = {"id": "vol-inc", "cibles": [
  {"nom": "CTV haut risque", "type": "CTV", "definition": "Adénopathies (en place) ou niveaux ganglionnaires qui les contenaient (après curage)", "quand": "Toujours"},
  {"nom": "CTV muqueuses", "type": "CTV", "definition": "Muqueuses à risque selon HPV, EBV et le nombre d'adénopathies (voir l'indication)", "quand": "Sauf origine cutanée suspectée"},
  {"nom": "CTV ganglions électifs", "type": "CTV", "definition": "Aires ganglionnaires homo- ou bilatérales (voir l'indication)", "quand": "Toujours"}],
  "atlas": [], "oar_ids": ["oar-parotide-d", "oar-parotide-g", "oar-cavite-orale", "oar-mandibule", "oar-larynx", "oar-moelle", "oar-plexus-brachial-d", "oar-plexus-brachial-g"]}
INC_SIM = {"id": "sim-inc", "position": "Décubitus dorsal", "preparation": "Masque thermoformé tête et épaules", "scanner": "Scanner injecté fusionné à la TEP"}
CIS_E = "Cisplatine si HPV− N2–N3, si HPV+ avec plusieurs adénopathies, bilatérales ou > 3 cm, ou si EBV+ stade II–IVA (ASCO 2020)"
CIS_P = "Cisplatine si rupture capsulaire (ASCO 2020)"
it = {s["id"]: s["titre"] for s in INC_SIT}
INC_SCH = [
  schema("inc-70", "inc-ep", "RT exclusive 70 Gy / 35 fx", "rte_normo", "recommandation", ["maghami2020-asco"],
         [P("PTV adénopathies", 70, 35, "70 Gy ou équivalent sur 7 semaines"), P("PTV muqueuses à risque", 50, 25, "Environ 50 Gy"),
          P("PTV ganglions électifs", 50, 25, "40 à 50 Gy")], INC, "ORL", it["inc-ep"], "vol-inc", "sim-inc",
         ["Chercher le primitif avant de traiter : TEP, endoscopie, amygdalectomie, mucosectomie de la base de langue"], tech="IMRT", syst=CIS_E),
  schema("inc-po-60", "inc-po", "Post-opératoire 60 Gy / 30 fx", "rte_normo", "recommandation", ["maghami2020-asco"],
         [P("PTV niveaux envahis", 60, 30, "60 à 66 Gy si rupture capsulaire"), P("PTV autres niveaux et muqueuses", 50, 25)],
         INC, "ORL", it["inc-po"], "vol-inc", "sim-inc", ["Un seul ganglion pN+ sans rupture capsulaire : pas de RT"], tech="IMRT", syst=CIS_P),
]

# ── Sillon supérieur (poumon) ──
PAN_SIT = {"id": "pou-pancoast", "localisation_id": "poumon", "titre": "Tumeur du sillon supérieur (Pancoast) T3–T4 N0–N1 résécable", "contexte": "en_place", "ordre": 7,
           "criteres": "CBNPC du sillon supérieur T3–T4 N0–N1 : radiochimiothérapie d'induction puis résection (SWOG 9416)"}
PAN_VOL = {"id": "vol-pou-pancoast", "cibles": [{"nom": "CTV tumeur", "type": "CTV", "definition": "Tumeur primitive et ganglions envahis", "quand": "Toujours"}], "atlas": [],
           "oar_ids": ["oar-poumons", "oar-moelle", "oar-plexus-brachial-d", "oar-plexus-brachial-g", "oar-oesophage", "oar-coeur"]}
PAN_SCH = [schema("pou-pancoast-45", "pou-pancoast", "Induction 45 Gy / 25 fx puis chirurgie", "rte_normo", "pratique_institutionnelle", ["rusch2007-swog9416", "rusch2001-swog9416"],
                  [P("PTV", 45, 25, "1,8 Gy par fraction ; résection 3 à 5 semaines après")], "Poumon", "Thorax", PAN_SIT["titre"], "vol-pou-pancoast", "sim-pou",
                  ["Bilan après induction avant la chirurgie ; 2 cycles de cisplatine–étoposide de consolidation après la résection"],
                  syst="Cisplatine 50 mg/m² J1, J8, J29, J36 + étoposide 50 mg/m² J1–5 et J29–33, pendant la RT (SWOG 9416)")]

# ── Dermatofibrosarcome et ostéosarcome (sarcome des membres et du tronc) ──
SM = "Membres et tronc"
SM_SIT = [
  {"id": "sm-dfsp", "localisation_id": "sarcome_membres", "titre": "Dermatofibrosarcome protubérant", "contexte": "post_op", "ordre": 3,
   "criteres": "RT si marges positives ou proches, tumeur volumineuse ou récidivante, ou si une exérèse large serait mutilante (Castle 2013)"},
  {"id": "sm-osteo", "localisation_id": "sarcome_membres", "titre": "Ostéosarcome non opérable ou à marges insuffisantes", "contexte": "post_op", "ordre": 4,
   "criteres": "Ostéosarcome inopérable (rachis, bassin) ou réséqué avec marges positives ou proches ; efficacité meilleure sur un reliquat microscopique ou minime (DeLaney 2005)"},
]
SM_VOL = [
  {"id": "vol-sm-dfsp", "cibles": [{"nom": "CTV", "type": "CTV", "definition": "Lit opératoire (ou tumeur en pré-opératoire) avec une marge large dans le plan cutané", "quand": "Toujours"}],
   "atlas": [], "oar_ids": ["oar-peau"]},
  {"id": "vol-sm-osteo", "cibles": [{"nom": "CTV", "type": "CTV", "definition": "Tumeur ou lit opératoire avec marge", "quand": "Toujours"},
                                    {"nom": "GTV", "type": "GTV", "definition": "Tumeur ou reliquat macroscopique", "quand": "Complément"}],
   "atlas": [], "oar_ids": ["oar-moelle", "oar-peau"]},
]
ss = {s["id"]: s["titre"] for s in SM_SIT}
SM_SCH = [
  schema("sm-dfsp-60", "sm-dfsp", "Post-opératoire 60 Gy / 30 fx", "rte_normo", "pratique_institutionnelle", ["castle2013-dfsp"],
         [P("PTV", 60, 30, "60 à 66 Gy ; 66 Gy si marges positives")], SM, "Sarcomes", ss["sm-dfsp"], "vol-sm-dfsp", "sim-sarcome-service",
         ["Contrôle local 98 % à 5 ans (Castle 2013)"], tech="Électrons ou photons, bolus"),
  schema("sm-dfsp-pre-50", "sm-dfsp", "Pré-opératoire 50 Gy / 25 fx", "rte_normo", "pratique_institutionnelle", ["castle2013-dfsp"],
         [P("PTV", 50, 25, "50 à 50,4 Gy")], SM, "Sarcomes", ss["sm-dfsp"], "vol-sm-dfsp", "sim-sarcome-service",
         ["Pré-opératoire si la tumeur est volumineuse ou l'exérèse large difficile"], tech="Électrons ou photons, bolus"),
  schema("sm-osteo-66", "sm-osteo", "CTV 50 Gy puis complément jusqu'à 66 Gy", "rte_normo", "pratique_institutionnelle", ["delaney2005-osteo"],
         [Ps("PTV CTV", 50, 25, "45 à 50 Gy"), Ps("PTV GTV", 16, 8, "Complément, cumul 66 Gy (dose médiane) ; viser plus de 55 Gy")],
         SM, "Sarcomes", ss["sm-osteo"], "vol-sm-osteo", "sim-sarcome-service",
         ["Au rachis et au bassin : 20 Gy pré-opératoires possibles contre l'ensemencement"], tech="RT conformationnelle ou protons", syst="Chimiothérapie de l'ostéosarcome selon le protocole"),
]

# ── Prostate oligométastatique : SBRT des métastases ──
PO_SIT = {"id": "pro-oligo", "localisation_id": "prostate", "titre": "Récidive oligométastatique hormonosensible (1 à 3 métastases) : stéréotaxie", "contexte": "oligometastatique", "ordre": 10,
          "criteres": "1 à 3 métastases (os, ganglions, viscères) d'un cancer de la prostate hormonosensible ; SBRT de toutes les lésions (ORIOLE) ; avec hormonothérapie dans EXTEND"}
PO_VOL = {"id": "vol-pro-oligo", "cibles": [{"nom": "GTV = CTV", "type": "CTV", "definition": "Métastase visible au scanner, à l'IRM ou à la TEP, CTV = GTV ; PTV = CTV + 5 mm (plus si mouvement respiratoire > 5 mm)", "quand": "Toujours"}],
          "atlas": [], "oar_ids": ["oar-moelle", "oar-poumons", "oar-coeur", "oar-oesophage", "oar-duodenum", "oar-rectum", "oar-peau"]}
PO_SIM = {"id": "sim-pro-oligo", "position": "Décubitus dorsal", "preparation": "Contention personnalisée (Alpha Cradle) ; TDM 4D si lésion mobile", "scanner": "Scanner, ± IRM ; TEP au PSMA si possible"}
PS = "Récidive oligométastatique hormonosensible (1 à 3 métastases) : stéréotaxie"
PR = "Prostate"
PO_SCH = [
  schema("pro-oligo-os-24", "pro-oligo", "Métastase osseuse : 24 Gy / 1 fx", "sbrt", "pratique_institutionnelle", ["oriole-protocole", "extend-protocole"],
         [P("PTV", 24, 1, "16 à 24 Gy / 1 fx ; ou 27–36 Gy / 3 fx (EXTEND)", "1 fx")], PR, "Uro", PS, "vol-pro-oligo", "sim-pro-oligo",
         ["5 fractions si l'intestin grêle est proche (ORIOLE)"], tech="SBRT guidée par l'image"),
  schema("pro-oligo-gg-30", "pro-oligo", "Métastase ganglionnaire : 30 Gy / 3 fx", "sbrt", "pratique_institutionnelle", ["extend-protocole"],
         [P("PTV", 30, 3, "30 à 36 Gy / 3 fx un jour sur deux ; ou 30–45 Gy / 5–6 fx", "1 fx tous les 2 jours")], PR, "Uro", PS, "vol-pro-oligo", "sim-pro-oligo",
         [], tech="SBRT guidée par l'image", syst="Hormonothérapie (bras prostate d'EXTEND)"),
  schema("pro-oligo-visc-50", "pro-oligo", "Métastase pulmonaire ou hépatique : 50 Gy / 5 fx", "sbrt", "pratique_institutionnelle", ["oriole-protocole", "extend-protocole"],
         [P("PTV", 50, 5, "50 à 60 Gy / 5 fx (ORIOLE) ; 50 Gy / 4 fx en périphérie (EXTEND)", "1 fx tous les 2 jours")], PR, "Uro", PS, "vol-pro-oligo", "sim-pro-oligo",
         ["5 fractions si lésion ≥ 3 cm ou proche du médiastin (ORIOLE)"], tech="SBRT guidée par l'image"),
]

def L(o, i, v, n=""):
  x = {"oar_id": o, "indicateur": i, "limitant": v}
  if n: x["note"] = n
  return x
SRC = "Protocole EXTEND (MD Anderson 2018-0349), tableau des contraintes"
JEUX = [
  {"id": "ct-extend-1fx", "titre": "Stéréotaxie en 1 fraction (EXTEND)", "fractionnement": "1 fx", "source": SRC, "verification": "verifie", "lignes": [
    L("oar-moelle", "Dmax", "< 10 Gy"), L("oar-coeur", "Dmax", "< 22 Gy"), L("oar-oesophage", "Dmax", "< 15,4 Gy"), L("oar-poumons", "D1000cc", "< 7 Gy"),
    L("oar-duodenum", "Dmax", "< 12,4 Gy"), L("oar-rectum", "Dmax", "< 18,4 Gy"), L("oar-peau", "Dmax", "< 26 Gy")]},
  {"id": "ct-extend-3fx", "titre": "Stéréotaxie en 3 fractions (EXTEND)", "fractionnement": "3 fx", "source": SRC, "verification": "verifie", "lignes": [
    L("oar-moelle", "Dmax", "< 21,9 Gy"), L("oar-coeur", "Dmax", "< 30 Gy"), L("oar-oesophage", "Dmax", "< 25,2 Gy"), L("oar-poumons", "D1000cc", "< 12,4 Gy"),
    L("oar-duodenum", "Dmax", "< 22,2 Gy"), L("oar-rectum", "Dmax", "< 28,2 Gy"), L("oar-peau", "Dmax", "< 33 Gy")]},
  {"id": "ct-extend-5fx", "titre": "Stéréotaxie en 5 fractions (EXTEND)", "fractionnement": "5 fx", "source": SRC, "verification": "verifie", "lignes": [
    L("oar-moelle", "Dmax", "< 30 Gy"), L("oar-coeur", "Dmax", "< 38 Gy"), L("oar-oesophage", "Dmax", "< 35 Gy"), L("oar-poumons", "D1000cc", "< 13,5 Gy"),
    L("oar-duodenum", "Dmax", "< 35 Gy"), L("oar-duodenum", "V20Gy", "< 30 cc"), L("oar-duodenum", "V30Gy", "< 10 cc"), L("oar-rectum", "Dmax", "< 38 Gy"), L("oar-peau", "Dmax", "< 39,5 Gy")]},
]
LIENS = {"pro-oligo-os-24": ["ct-extend-1fx"], "pro-oligo-gg-30": ["ct-extend-3fx"], "pro-oligo-visc-50": ["ct-extend-5fx"]}

def main():
  ess = lire("essais.json"); ids = {e["id"] for e in ESSAIS}
  ess["essais"] = [e for e in ess["essais"] if e["id"] not in ids] + ESSAIS; ecrire("essais.json", ess)
  A = {e["id"]: e["acronyme"] for e in ess["essais"]}
  idx = lire("index.json")
  tous = INC_SCH + PAN_SCH + SM_SCH + PO_SCH; mes = {s["id"] for s in tous}
  sits = {s["id"] for s in INC_SIT + SM_SIT} | {PAN_SIT["id"], PO_SIT["id"]}
  idx["schemas"] = [s for s in idx["schemas"] if s["id"] not in mes]
  idx["situations"] = [s for s in idx["situations"] if s["id"] not in sits]
  idx["localisations"] = [l for l in idx["localisations"] if l["id"] != "orl_inconnu"]

  def poser(d, S, H, V, M):
    d["situations"] = [s for s in d["situations"] if s["id"] not in sits] + S
    d["schemas"] = [s for s in d["schemas"] if s["id"] not in mes] + H
    vi = {v["id"] for v in V}; d["volumes"] = [v for v in d["volumes"] if v["id"] not in vi] + V
    mi = {m["id"] for m in M}; d["simulations"] = [m for m in d["simulations"] if m["id"] not in mi] + M
  pou = lire("poumon.json"); poser(pou, [PAN_SIT], PAN_SCH, [PAN_VOL], [])
  sm = lire("sarcome_membres.json"); poser(sm, SM_SIT, SM_SCH, SM_VOL, [])
  pro = lire("prostate.json"); poser(pro, [PO_SIT], PO_SCH, [PO_VOL], [PO_SIM])
  ordre = max(l["ordre"] for l in idx["localisations"]) + 1
  ref = lire("cavum.json")
  inc = {"version": ref["version"], "id": "orl_inconnu", "region_id": "orl", "nom": INC, "ordre": ordre, "date_maj": DATE, "situations": INC_SIT, "schemas": INC_SCH,
         "simulations": [INC_SIM], "volumes": [INC_VOL], "curie_indications": [], "systemique": [], "hormonotherapie": [],
         "points_attention": [{"cible": "orl_inconnu", "point": "HPV (p16) et EBV sur l'adénopathie orientent les muqueuses à traiter", "portee": "localisation"}]}
  for f, d in (("poumon.json", pou), ("sarcome_membres.json", sm), ("prostate.json", pro), ("orl_inconnu.json", inc)):
    d["date_maj"] = DATE; ecrire(f, d)
    for s in d["situations"]:
      if s["id"] in sits: idx["situations"].append({k: s[k] for k in ("id", "localisation_id", "titre", "contexte", "criteres", "ordre")})
    for s in d["schemas"]:
      if s["id"] in mes:
        idx["schemas"].append({"id": s["id"], "localisation_id": d["id"], "situation_id": s["situation_id"], "titre": s["titre"], "type": s["type"], "preuve": s["preuve"],
                               "essais": [A[e] for e in s["essai_ids"]], "doses": [{k: p.get(k) for k in ("volume", "dose_Gy", "fractions", "dose_fx_Gy")} for p in s["prescriptions"]], "ind": s["ind"]})
  for l in idx["localisations"]:
    if l["id"] in ("poumon", "sarcome_membres", "prostate"): l["nb_schemas"] = len(lire(l["id"] + ".json")["schemas"]); l["date_maj"] = DATE
  idx["localisations"].append({"id": "orl_inconnu", "nom": INC, "region_id": "orl", "ordre": ordre, "date_maj": DATE, "nb_schemas": len(INC_SCH), "curietherapie": False})
  ecrire("index.json", idx)

  j = json.loads(J.read_text()); ji = {x["id"] for x in JEUX}
  j["jeux"] = [x for x in j["jeux"] if x["id"] not in ji] + JEUX
  for k, v in LIENS.items(): j["schemas"][k] = {"contraintes_ids": v}
  if "orl_inconnu" not in j["regions_revues"]: j["regions_revues"].append("orl_inconnu")
  J.write_text(json.dumps(j, ensure_ascii=False, indent=1) + "\n")
  print(len(tous), "schémas,", len(ESSAIS), "essais,", len(JEUX), "jeux")

if __name__ == "__main__":
  main()
