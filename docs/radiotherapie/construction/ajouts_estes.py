# Phase RTX, lot 6 (01/11/2026) : situations d'Estes 2025-2026 absentes du référentiel, ajoutées d'après les articles de la Bibliothèque
# (~/Downloads/Bibliothèque Onco360/Radiothérapie) ; doses recopiées des articles, rien d'Estes seul. Inventaire : docs/radiotherapie/manquants-estes.md.
# Idempotent : retire puis remet ses propres éléments. Lancer : python3 docs/radiotherapie/construction/ajouts_estes.py
import json, pathlib

R = pathlib.Path(__file__).resolve().parents[3] / "public" / "donnees-rt"
DATE = "2026-11-01"
lire = lambda f: json.loads((R / f).read_text())
def ecrire(f, d): (R / f).write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")

ESSAIS = [
  {"id": "weber2015-mpe", "acronyme": "Weber 2015 (épendymome myxopapillaire)", "type": "essai", "revue": "Neuro-Oncology", "annee": 2015, "doi": "10.1093/neuonc/nou293",
   "population": "183 épendymomes myxopapillaires médullaires (MD Anderson et Rare Cancer Network), rétrospectif", "bras": "Chirurgie seule (53 %) ou chirurgie et RT (47 %) ; dose médiane 50,4 Gy",
   "resultat": "SSP à 10 ans 61,2 % ; échec local 26,8 % ; la RT adjuvante et une dose ≥ 50,4 Gy améliorent le contrôle"},
  {"id": "wei2019-pvtt", "acronyme": "Wei 2019 (RT néoadjuvante, thrombose portale)", "type": "essai", "revue": "J Clin Oncol 37", "annee": 2019,
   "population": "164 CHC résécables avec thrombose de la veine porte, randomisé multicentrique", "bras": "RT 3D néoadjuvante 18 Gy / 6 fx puis hépatectomie vs hépatectomie seule",
   "resultat": "SG à 2 ans 27,4 vs 9,4 % ; mortalité liée au CHC HR 0,35"},
  {"id": "sun2019-pvtt", "acronyme": "Sun 2019 (IMRT adjuvante, thrombose portale)", "type": "essai", "revue": "Radiother Oncol 140:20", "annee": 2019, "doi": "10.1016/j.radonc.2019.05.006",
   "population": "52 CHC avec thrombose de la veine porte après hépatectomie ± thrombectomie, randomisé", "bras": "IMRT adjuvante 50 Gy / 25 fx vs surveillance",
   "resultat": "SG médiane 18,9 vs 10,8 mois ; SSM 9,1 vs 4,1 mois"},
  {"id": "xi2025-rfa-sbrt", "acronyme": "Xi 2025 (SBRT vs radiofréquence)", "type": "essai", "revue": "J Clin Oncol 43:1073", "annee": 2025, "doi": "10.1200/JCO-24-01532",
   "population": "166 CHC récidivants uniques ≤ 5 cm, randomisé", "bras": "SBRT 36 à 54 Gy / 3 fx (médiane 45 Gy) vs radiofréquence",
   "resultat": "Survie sans progression locale à 2 ans 92,7 vs 75,8 % (HR 0,45) ; SG identique"},
  {"id": "seegenschmiedt2012-dupuytren", "acronyme": "Seegenschmiedt (Dupuytren)", "type": "essai", "revue": "Dupuytren's Disease and Related Hyperproliferative Disorders, Springer", "annee": 2012,
   "doi": "10.1007/978-3-642-22697-7_44", "population": "489 patients, maladie de Dupuytren débutante", "bras": "Surveillance vs 21 Gy (7 × 3 Gy) vs 30 Gy (2 séries de 5 × 3 Gy, 10 à 12 semaines d'écart)",
   "resultat": "Progression 52 % (surveillance) vs 22 % (21 Gy) vs 16 % (30 Gy) ; chirurgie 30 vs 12 vs 8 %"},
  {"id": "ledrad2023", "acronyme": "LedRad", "type": "essai", "revue": "Radiother Oncol", "annee": 2023, "doi": "10.1016/j.radonc.2023.109718",
   "population": "84 maladies de Ledderhose symptomatiques, phase 3 randomisée en double aveugle", "bras": "30 Gy (2 séries de 5 × 3 Gy) vs RT simulée",
   "resultat": "Douleur à 12 mois 2,5 vs 3,6 ; soulagement 74 vs 56 % ; effets secondaires légers"},
  {"id": "canyilmaz2015", "acronyme": "Canyilmaz 2015 (fasciite plantaire)", "type": "essai", "revue": "Int J Radiat Oncol Biol Phys", "annee": 2015, "doi": "10.1016/j.ijrobp.2015.02.009",
   "population": "128 fasciites plantaires, randomisé", "bras": "RT 6 Gy (6 × 1 Gy, 3 par semaine) vs infiltration de corticoïde",
   "resultat": "Douleur et fonction meilleures à 3 mois avec la RT (p < 0,001)"},
  {"id": "arthrorad2022", "acronyme": "ArthroRad", "type": "essai", "revue": "Strahlenther Onkol 198:370", "annee": 2022, "doi": "10.1007/s00066-021-01866-2",
   "population": "172 mains et 64 genoux arthrosiques douloureux, randomisé", "bras": "3 Gy (6 × 0,5 Gy, 2 par semaine) vs 0,3 Gy (6 × 0,05 Gy)",
   "resultat": "Soulagement de la douleur dans les deux bras à 3 mois, sans différence ; essai arrêté tôt"},
  {"id": "minten2018", "acronyme": "Minten 2018 (arthrose de la main)", "type": "essai", "revue": "Osteoarthritis Cartilage", "annee": 2018, "doi": "10.1016/j.joca.2018.06.010",
   "population": "56 arthroses de la main, randomisé contre RT simulée", "bras": "6 Gy (6 × 1 Gy) vs RT simulée",
   "resultat": "Pas de différence de réponse à 3 mois (29 vs 36 %) : RT déconseillée dans l'arthrose de la main"},
]

def schema(id_, sit, titre, typ, preuve, essais, presc, loc_nom, region_nom, sit_titre, vol, sim, points, tech="RT externe", syst="Aucune"):
  T = {"rte_normo": "Normofractionné", "rte_hypo": "Hypofractionné", "sbrt": "Stéréotaxie"}
  return {"id": id_, "situation_id": sit, "titre": titre, "type": typ, "preuve": preuve, "essai_ids": essais, "prescriptions": presc, "technique": tech,
          "systemique": syst, "simulation_id": sim, "volumes_id": vol, "points_attention": points, "date_verif": DATE,
          "ind": [region_nom, loc_nom, sit_titre, T[typ]], "contraintes_ids": [], "ct_mention": "L'article ne publie pas de contraintes : base de contraintes appliquée."}

def P(vol, d, n, note="", rythme="5 fx/sem"):
  x = {"volume": vol, "dose_Gy": d, "fractions": n, "dose_fx_Gy": round(d / n, 2), "mode": "seul", "rythme": rythme}
  if note: x["note"] = note
  return x

# ── Épendymome myxopapillaire ──
EP_SIT = {"id": "ep-mpe", "localisation_id": "ependymome", "titre": "Épendymome myxopapillaire médullaire opéré", "contexte": "post_op",
          "criteres": "RT adjuvante après exérèse, surtout exérèse incomplète ou patient jeune (moins de 36 ans) : meilleurs contrôle local et survie sans progression (Weber 2015)", "ordre": 2}
EP_VOL = {"id": "vol-ependymome-mpe", "cibles": [{"nom": "CTV lit tumoral", "type": "CTV", "definition": "Lit opératoire et reliquat sur l'IRM médullaire post-opératoire", "quand": "Toujours"}],
          "atlas": [], "oar_ids": ["oar-moelle", "oar-queue-cheval"]}
EP_SIM = {"id": "sim-rachis", "position": "Décubitus dorsal", "preparation": "Contention du tronc", "scanner": "Scanner de planification fusionné à l'IRM médullaire"}
EP_SCH = [schema("ep-mpe-504", "ep-mpe", "Lit tumoral 50,4 Gy / 28 fx", "rte_normo", "pratique_institutionnelle", ["weber2015-mpe"],
                 [P("PTV lit tumoral", 50.4, 28, "Dose médiane de la série ; une dose ≥ 50,4 Gy améliore le contrôle local et à distance")],
                 "Épendymome de l'adulte", "SNC", EP_SIT["titre"], "vol-ependymome-mpe", "sim-rachis",
                 ["Échecs surtout locaux (26,8 %) mais aussi rachidiens à distance (9,3 %) et cérébraux (6 %) : surveiller tout l'axe"])]

# ── Foie : CHC avec thrombose portale, CHC récidivant ──
TVP = "CHC avec invasion vasculaire macroscopique"
FO_SCH = [
  schema("foie-tvp-neo-18", "foie-chc-tvp", "Thrombose portale résécable : 18 Gy / 6 fx avant hépatectomie", "rte_hypo", "essai_phase3", ["wei2019-pvtt"],
         [P("PTV (tumeur + thrombus)", 18, 6, "RT 3D ; hépatectomie ensuite")], "Foie et voies biliaires", "Digestif", TVP, "vol-foie-tvp", "sim-foie",
         ["Réponse partielle 20,7 % ; SG à 2 ans 27,4 vs 9,4 % sans RT (Wei 2019)"], tech="RT 3D conformationnelle"),
  schema("foie-tvp-adj-50", "foie-chc-tvp", "Thrombose portale opérée : IMRT adjuvante 50 Gy / 25 fx", "rte_normo", "essai_phase3", ["sun2019-pvtt"],
         [P("PTV lit opératoire et thrombus", 50, 25)], "Foie et voies biliaires", "Digestif", TVP, "vol-foie-tvp", "sim-foie",
         ["SG médiane 18,9 vs 10,8 mois sans RT (Sun 2019)"], tech="IMRT"),
  schema("foie-chc-recid-45", "foie-chc", "CHC récidivant unique ≤ 5 cm : SBRT 45 Gy / 3 fx", "sbrt", "essai_phase3", ["xi2025-rfa-sbrt"],
         [P("PTV", 45, 3, "Dose médiane ; 36 à 54 Gy / 3 fx selon le foie et les organes voisins", "1 fx tous les 2 jours")],
         "Foie et voies biliaires", "Digestif", "CHC non éligible aux traitements locaux standard : stéréotaxie", "vol-foie-sbrt", "sim-foie-sbrt",
         ["Meilleur contrôle local que la radiofréquence (2 ans : 92,7 vs 75,8 %), survie identique (Xi 2025)"], tech="VMAT stéréotaxique"),
]

# ── Pathologies bénignes (localisation neuve, région Autres) ──
BN = "Pathologies bénignes"
BN_SIT = [
  {"id": "bn-dupuytren", "titre": "Maladie de Dupuytren débutante", "criteres": "Stade N ou N/I (nodules, cordes, flessum ≤ 10°) en progression ; au-delà, contrôle moindre", "ordre": 1},
  {"id": "bn-ledderhose", "titre": "Maladie de Ledderhose symptomatique", "criteres": "Nodules plantaires douloureux", "ordre": 2},
  {"id": "bn-fasciite", "titre": "Fasciite plantaire (talalgie)", "criteres": "Douleur persistante malgré le traitement médical", "ordre": 3},
  {"id": "bn-arthrose", "titre": "Arthrose douloureuse (genou, main)", "criteres": "Douleur malgré le traitement médical ; pas d'efficacité démontrée contre RT simulée dans l'arthrose de la main (Minten 2018)", "ordre": 4},
]
for s in BN_SIT: s.update({"localisation_id": "benin", "contexte": "en_place"})
BN_VOL = {"id": "vol-benin", "cibles": [{"nom": "CTV", "type": "CTV", "definition": "Zone atteinte (nodules et cordes, aponévrose, articulation) avec une marge clinique", "quand": "Toujours"}],
          "atlas": [], "oar_ids": ["oar-peau"]}
BN_SIM = {"id": "sim-benin", "position": "Selon la zone (main ou pied à plat, genou)", "preparation": "Contention de la main ou du pied ; repérage clinique des nodules", "scanner": "Champ direct ou scanner selon la zone"}
st = {s["id"]: s["titre"] for s in BN_SIT}
BN_SCH = [
  schema("bn-dup-30", "bn-dupuytren", "30 Gy : 2 séries de 5 × 3 Gy à 10–12 semaines", "rte_hypo", "essai_phase3", ["seegenschmiedt2012-dupuytren"],
         [P("CTV + marge", 30, 10, "Deux séries de 5 × 3 Gy séparées de 10 à 12 semaines")], BN, "Autres", st["bn-dupuytren"], "vol-benin", "sim-benin",
         ["21 Gy en 7 × 3 Gy tous les 2 jours : aussi efficace, plus de toxicité aiguë (32 vs 24 %)"], tech="Électrons ou photons de basse énergie"),
  schema("bn-led-30", "bn-ledderhose", "30 Gy : 2 séries de 5 × 3 Gy", "rte_hypo", "essai_phase3", ["ledrad2023"],
         [P("CTV + marge", 30, 10, "Deux séries de 5 × 3 Gy")], BN, "Autres", st["bn-ledderhose"], "vol-benin", "sim-benin",
         ["Effets secondaires légers (érythème, sécheresse), disparus à 18 mois dans 87 % des cas"]),
  schema("bn-fas-6", "bn-fasciite", "6 Gy en 6 × 1 Gy, 3 par semaine", "rte_hypo", "essai_phase3", ["canyilmaz2015"],
         [P("Calcanéum et insertion de l'aponévrose", 6, 6, "", "3 fx/sem")], BN, "Autres", st["bn-fasciite"], "vol-benin", "sim-benin",
         ["Seconde série possible ; délai avant un 2e traitement plus long qu'après infiltration"]),
  schema("bn-art-3", "bn-arthrose", "3 Gy en 6 × 0,5 Gy, 2 par semaine", "rte_hypo", "essai_phase3", ["arthrorad2022", "minten2018"],
         [P("Articulation", 3, 6, "", "2 fx/sem")], BN, "Autres", st["bn-arthrose"], "vol-benin", "sim-benin",
         ["0,3 Gy aussi efficace que 3 Gy à 3 mois (ArthroRad) ; 6 × 1 Gy pas mieux qu'une RT simulée dans l'arthrose de la main (Minten 2018)"]),
]

def main():
  ess = lire("essais.json"); ids = {e["id"] for e in ESSAIS}
  ess["essais"] = [e for e in ess["essais"] if e["id"] not in ids] + ESSAIS; ecrire("essais.json", ess)
  idx = lire("index.json"); A = {e["id"]: e["acronyme"] for e in ess["essais"]}
  mes = {s["id"] for s in EP_SCH + FO_SCH + BN_SCH}
  idx["schemas"] = [s for s in idx["schemas"] if s["id"] not in mes]
  idx["situations"] = [s for s in idx["situations"] if s["id"] not in {"ep-mpe"} | set(st)]
  idx["localisations"] = [l for l in idx["localisations"] if l["id"] != "benin"]

  ep = lire("ependymome.json")
  ep["situations"] = [s for s in ep["situations"] if s["id"] != "ep-mpe"] + [EP_SIT]
  ep["schemas"] = [s for s in ep["schemas"] if s["id"] not in mes] + EP_SCH
  ep["volumes"] = [v for v in ep["volumes"] if v["id"] != EP_VOL["id"]] + [EP_VOL]
  ep["simulations"] = [s for s in ep["simulations"] if s["id"] != EP_SIM["id"]] + [EP_SIM]
  fo = lire("foie.json"); fo["schemas"] = [s for s in fo["schemas"] if s["id"] not in mes] + FO_SCH
  ordre = max(l["ordre"] for l in idx["localisations"]) + 1
  bn = {"version": ep["version"], "id": "benin", "region_id": "autres", "nom": BN, "ordre": ordre, "date_maj": DATE, "situations": BN_SIT, "schemas": BN_SCH,
        "simulations": [BN_SIM], "volumes": [BN_VOL], "curie_indications": [], "systemique": [], "hormonotherapie": [],
        "points_attention": [{"cible": "benin", "point": "Pathologie bénigne : expliquer le faible risque de cancer radio-induit, protéger les zones hors champ", "portee": "localisation"}]}
  for f, d in (("ependymome.json", ep), ("foie.json", fo), ("benin.json", bn)):
    d["date_maj"] = DATE; ecrire(f, d)
    loc = d["id"]
    for s in d["situations"]:
      if s["id"] in {"ep-mpe"} | set(st): idx["situations"].append({k: s[k] for k in ("id", "localisation_id", "titre", "contexte", "criteres", "ordre")})
    for s in d["schemas"]:
      if s["id"] in mes:
        idx["schemas"].append({"id": s["id"], "localisation_id": loc, "situation_id": s["situation_id"], "titre": s["titre"], "type": s["type"], "preuve": s["preuve"],
                               "essais": [A[e] for e in s["essai_ids"]], "doses": [{k: p.get(k) for k in ("volume", "dose_Gy", "fractions", "dose_fx_Gy")} for p in s["prescriptions"]], "ind": s["ind"]})
  for l in idx["localisations"]:
    if l["id"] in ("ependymome", "foie"): l["nb_schemas"] = len(lire(l["id"] + ".json")["schemas"]); l["date_maj"] = DATE
  idx["localisations"].append({"id": "benin", "nom": BN, "region_id": "autres", "ordre": ordre, "date_maj": DATE, "nb_schemas": len(BN_SCH), "curietherapie": False})
  ecrire("index.json", idx)
  print(len(EP_SCH) + len(FO_SCH) + len(BN_SCH), "schémas,", len(ESSAIS), "essais")

if __name__ == "__main__":
  main()
