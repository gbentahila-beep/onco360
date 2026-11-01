# Tableau de comparaison des contraintes : Onco360 (contraintes.json) / RadOncCalc (relevé du 30/10/2026)
import json, re, sys, html, collections as C
def lire_fiche(L):
  # libellés de la fiche ouverte : site primitif, effet évité (valeur avant « Endpoint »), α/β, références des notes
  d = {}
  if not L: return d
  if "Primary Site" in L:
    i = L.index("Primary Site"); d["site"] = L[i + 1]
  if "Endpoint" in L:
    i = L.index("Endpoint"); d["effet"] = L[i - 1]
  if "α/β ratio" in L:
    i = L.index("α/β ratio"); d["ab"] = L[i + 1]
  if "Notes" in L and "My Notes" in L:
    a, b = L.index("Notes"), L.index("My Notes")
    d["refs"] = [x for x in L[a + 1:b] if 2 < len(x) < 60 and "\n" not in x and not re.match(r"^(Per\b|\s|:|and\b)", x) and not x.endswith(" ") and re.search(r"\d|[A-Z]{2,}", x)]
  return d
R = "/Users/ghitabentahila/Desktop/ONCO360/Chimio-HGC-Firebase/"
base = json.load(open(R + "public/donnees-rt/contraintes.json"))["base"]
O = json.load(open(R + "public/donnees-rt/oar.json"))
noms = {o["id"]: o["nom"] for o in O["oar"]}; noms.update({p["id"]: p["nom"] for p in O["paires"]})
NOUV=set(); BADGE=' <span class="b b-v">À créer dans Onco360</span>'
for o in O["paires"]:
  pass
rocc = json.load(open(sys.argv[1]))
detail = json.load(open(sys.argv[2])) if len(sys.argv) > 3 else {}
MAP = {
 "Anal_Canal":"oar-canal-anal","Biliary_Tree":"oar-voie-biliaire","Bladder":"oar-vessie","BoneMarrow":"oar-moelle-osseuse","BoneMarrow_LSS":"oar-moelle-osseuse",
 "Bowel_Bag":"oar-grele","Bowel_Small":"oar-grele","Bowel_Loop":"oar-grele","Bowel_Large":"oar-colon","BrachialPlexs":"oar-plexus-brachiaux",
 "Brain":"oar-encephale","Brain-PTV":"oar-encephale-sain","Brain-GTV":"oar-encephale-sain","Brainstem":"oar-tronc-cerebral","Breast_Contra":"oar-sein-controlateral",
 "Carotid_A":"oar-carotides","CaudaEquina":"oar-queue-cheval","ChestWall":"oar-paroi-thoracique","Cochlea":"oar-cochlees","Constrict_Musc":"oar-constricteurs",
 "Cornea":"oar-cornees","Duodenum":"oar-duodenum","Esophagus":"oar-oesophage","Esophagus_S":"oar-oesophage-cervical","Eye":"oar-yeux","EyeBack/Retina":"oar-retines",
 "Femur_Head":"oar-tetes-femorales","Genitals":"oar-oge","Gluteal_Folds":"oar-sillon-fessier","GreatVes":"oar-gros-vaisseaux","Heart":"oar-coeur",
 "Hippocampus":"oar-hippocampes","Humeral_Head":"oar-tete-humerale","Hypothalamus":"oar-hypothalamus","Kidneys":"oar-reins","Kidney_Cortex":"oar-reins",
 "Kidney_Cortex_Contra":"oar-reins","Kidney_Cortex_Solitary":"oar-reins","Kidney_Cortex_Ipsi-ITV":"oar-reins","Kidney_Hilum":"oar-hile-renal","LAD_A":"oar-iva",
 "Lacrimal_Glnd":"oar-glandes-lacrymales","Larynx":"oar-larynx","Lens":"oar-cristallins","Lips":"oar-levres","Liver":"oar-foie","Long_Bone":"oar-os-longs",
 "Lung_Contra":"oar-poumon-controlateral","Lung_Ipsi":"oar-poumon-homolateral","Lungs":"oar-poumons","Mandible_Bone":"oar-mandibule","OpticChiasm":"oar-chiasma",
 "OpticNrv":"oar-nerfs-optiques","Oral_Cavity":"oar-cavite-orale","Pancreas":"oar-pancreas","Parotids (Each)":"oar-parotides","Parotid_Contra":"oar-parotides",
 "Parotid_Ipsi":"oar-parotides","PenileBulb":"oar-bulbe","Pituitary":"oar-hypophyse","Proximal_Bronchial_Tree":"oar-arbre-bronchique","Trachea_PBT":"oar-trachee",
 "Rectum":"oar-rectum","Rib":"oar-cotes","SacralPlex":"oar-plexus-sacre","Scalp":"oar-cuir-chevelu","Sigmoid_Colon":"oar-sigmoide","Skin":"oar-peau",
 "Skin_Inguinal":"oar-plis-inguinaux","SpinalCanal":"oar-canal-medullaire","SpinalCord":"oar-moelle","Spleen":"oar-rate","Stomach":"oar-estomac",
 "Submands_Glnd":"oar-glandes-sous-max","Submand_Glnd_Contra":"oar-glandes-sous-max","Submand_Glnd_Ipsi":"oar-glandes-sous-max","TM_Joint":"oar-atm",
 "Temporal_Lobe":"oar-lobes-temporaux","Testis_Contra":"oar-testicule-controlateral","Testis":"oar-testicule-controlateral","Thyroid_Glnd":"oar-thyroide",
 "Ureter/Urethra":"oar-uretre","Vagina":"oar-vagin","Ventricle_L":"oar-ventricule-gauche","Vulva":"oar-vulve","Ovaries":"oar-ovaires",
 "Distal_Bronchial_Tree":"oar-arbre-bronchique","Pharynx_Post_Wall":"oar-pharynx","Orbit":"oar-yeux",
 "Mitral_Valve":"oar-valves","Tricuspid_Valve":"oar-valves","Pulmonic_Valve":"oar-valves","Carotid_A_Contra":"oar-carotides","Carotid_A_Ipsi":"oar-carotides",
 "Rectovaginal":"oar-point-rv","Lung_Solitary":"oar-poumons","Hippocampus_Head":"oar-hippocampes","Hippocampus_Tail":"oar-hippocampes",
 "Brainstem-3mm":"oar-tronc-cerebral","Nerve Roots":"oar-racines-nerveuses","Transposed Ovaries":"oar-ovaires",
}
# organes absents d'Onco360 : à créer (id, nom, TG-263)
NEUF = {
 "Breast_Ipsi":("oar-sein-homolateral","Sein homolatéral","Breast_Ipsi"),"Breast":("oar-sein","Sein","Breast"),
 "Pericardium":("oar-pericarde","Péricarde","Pericardium"),"Pulmonary_A":("oar-artere-pulmonaire","Artère pulmonaire","A_Pulmonary"),
 "SVC":("oar-veine-cave-sup","Veine cave supérieure","V_Venacava_S"),"Heart_Atria":("oar-oreillettes","Oreillettes","Atria"),
 "Ventricle_R":("oar-ventricule-droit","Ventricule droit","Ventricle_R"),"Coronary_Vessels":("oar-coronaires","Artères coronaires","A_Coronary"),
 "L_Coronary_A":("oar-coronaire-gauche","Tronc coronaire gauche","A_Coronary_L"),"L_Circumflex_A":("oar-circonflexe","Artère circonflexe","A_Cflx"),
 "R_Coronary_A":("oar-coronaire-droite","Artère coronaire droite","A_Coronary_R"),"Femur":("oar-femurs","Fémurs (col et diaphyse)","Femur"),
 "Larynx_G":("oar-larynx-glottique","Larynx glottique","Larynx_Glottic"),"Larynx_SG":("oar-larynx-supraglottique","Larynx supraglottique","Larynx_SG"),
 "Constrict_Musc_S":("oar-constricteur-sup","Constricteur supérieur du pharynx","Musc_Constrict_S"),"Constrict_Musc_M":("oar-constricteur-moyen","Constricteur moyen du pharynx","Musc_Constrict_M"),
 "Constrict_Musc_I":("oar-constricteur-inf","Constricteur inférieur du pharynx","Musc_Constrict_I"),"Cricopharyngeus":("oar-cricopharyngien","Muscle cricopharyngien","Musc_Cricophar"),
 "EyeFront":("oar-segment-anterieur","Segment antérieur de l'œil","Eye_Front"),"Eyelid/Meibomian":("oar-paupieres","Paupières et glandes de Meibomius","Eyelid"),
 "Orbital_Bone":("oar-os-orbitaire","Os orbitaire","Bone_Orbit"),"Circle_of_Willis":("oar-polygone-willis","Polygone de Willis","Circle_Willis"),
 "Corpus_Callosum":("oar-corps-calleux","Corps calleux","CorpusCallosum"),"VB":("oar-corps-vertebraux","Corps vertébraux","VB"),"VB_T":("oar-corps-vertebraux","Corps vertébraux","VB"),
 "Bladder_Trigone":("oar-trigone","Trigone vésical","Bladder_Trigone"),"PubicSymphys":("oar-symphyse-pubienne","Symphyse pubienne","PubicSymphys"),
 "PenileCrura":("oar-corps-caverneux","Racines des corps caverneux","PenileCrura"),"Iliac_Crest":("oar-crete-iliaque","Crêtes iliaques","Bone_IliacCrest"),
 "Skin_Perianal":("oar-peau-perianale","Peau périanale","Skin_Perianal"),"Skin_LongStrip":("oar-bande-cutanee","Bande de peau longitudinale (membre)","Skin_Strip"),
 "GrowthPlate":("oar-cartilages-croissance","Cartilages de croissance","GrowthPlate"),"Joint_Spc":("oar-articulation","Espace articulaire","Joint"),
 "Joint_Spc/Bone":("oar-articulation","Espace articulaire","Joint"),"Bone":("oar-os","Os (hors cible)","Bone"),
 "Pterygoid_Musc":("oar-pterygoidiens","Muscles ptérygoïdiens","Musc_Pterygoid"),"Pterygoid_Musc_Lat":("oar-pterygoidiens","Muscles ptérygoïdiens","Musc_Pterygoid"),
 "Masseter_Musc":("oar-masseters","Muscles masséters","Musc_Masseter"),"BuccalMuc":("oar-muqueuse-buccale","Muqueuse buccale","Mucosa_Buccal"),
 "Teeth":("oar-dents","Dents","Teeth"),"Nerve (named)":("oar-nerfs-peripheriques","Nerfs périphériques nommés","Nrv_Periph"),
 "Pacemaker":("oar-stimulateur","Stimulateur ou défibrillateur cardiaque","Pacemaker"),
}
for k,(i,n,t) in NEUF.items(): MAP[k]=i; noms[i]=n; NOUV.add(i)
IMP = {"Mandatory":3,"Absolute":3,"Must":3,"Should":2,"Recommended":2,"Optimal":1,"Can":1,"Consensus":1,'"Low" Consensus':0,"No consensus":0,"Informational":0,"Obsolete":-9,"⚠️CAUTION⚠️":0}
REG = {"GI","CNS","Thorax","GU","H&N","Heart OARs","MSK","Target","Lymph"}
SIT = {"Re-irradiation","Intact","Postop","Brachy","Brachy/EBRT"}
def frac(s): return s.startswith("Conventional") or s in ("BID","General Metrics") or re.fullmatch(r"\d+(-\d+)?", s)
def groupe_fx(fr):
  if fr.startswith("Conventional"): return "N"
  if fr == "BID": return "BID"
  if fr == "General Metrics": return None
  return int(fr.split("-")[0])
G = C.defaultdict(lambda: {"o": [], "r": []})
for x in base:
  g = "N" if x["regime"] == "normo" else (x.get("fx") or "S*")
  G[(x["oar_id"], g)]["o"].append(x)
sans_map = C.Counter()
for s in rocc:
  L = s.split("\n"); org = L[0]; i = 1; cs = []
  while i < len(L) and not frac(L[i]): cs.append(L[i]); i += 1
  if i >= len(L): continue
  g = groupe_fx(L[i]); tags = L[i+1:]
  if g is None: continue
  oid = MAP.get(org)
  if not oid: sans_map[org] += 1; continue
  imp = [t for t in tags if t in IMP]; sit = [t for t in tags if t in SIT]
  src = [t for t in tags if t not in IMP and t not in REG and t not in SIT and t != "HIGH YIELD"]
  sc = (3 if "HIGH YIELD" in tags else 0) + max([IMP[t] for t in imp] or [0]) + min(len(src), 4) * 0.5 - (5 if sit and "Re-irradiation" in sit else 0)
  d = lire_fiche(detail.get(s) or [])
  for c in cs:
    G[(oid, g)]["r"].append({"s": s, "c": c, "org": org, "imp": imp, "hy": "HIGH YIELD" in tags, "sit": sit, "src": src, "sc": sc, "det": d})
def cle_tri(k):
  g = k[1]; return (noms.get(k[0], k[0]), 0 if g == "N" else (1 if g == "BID" else (2 + (g if isinstance(g, int) else 99))))
e = html.escape
# Clé d'un paramètre, pour repérer doublons et contraintes très proches
def nombre(t):
  m = re.findall(r"\d+(?:[.,]\d+)?", t); return float(m[0].replace(",", ".")) if m else None
def cle_param(ind):
  t = ind.replace(" ", "").replace("cm³", "cc").replace("cm3", "cc").lower()
  t = re.sub(r"\(.*", "", t)
  if t.startswith("dmax") or re.match(r"d0[.,]0\d*", t) or re.match(r"d0[.,]1(cc|-|$)", t) or re.match(r"d0[.,]03", t): return ("Dpt",)
  if "mean" in t or "moy" in t: return ("Dmean",)
  m = re.match(r"d(\d+(?:[.,]\d+)?)(cc|%)", t)
  if m: return ("D" + m.group(2), float(m.group(1).replace(",", ".")))
  m = re.match(r"v(\d+(?:[.,]\d+)?)(gy|%)", t)
  if m: return ("VGy" if m.group(2) == "gy" else "V%", float(m.group(1).replace(",", ".")))
  return ("?", t)
def proches(a, b):
  if a[0] != b[0]: return False
  if len(a) == 1: return True
  if a[0] == "?": return a[1] == b[1]
  x, y = a[1], b[1]
  if a[0] == "Dcc": return max(x, y) <= 2 * min(x, y) if min(x, y) > 0 else x == y
  if a[0] == "D%": return abs(x - y) <= 10
  return abs(x - y) <= max(2, 0.15 * max(x, y))
def vers_dcc(k, seuil):
  # « Vy Gy ≤ x cc » = « Dx cc ≤ y Gy » : même contrainte écrite autrement
  if k[0] == "VGy" and "ircumf" in (seuil or ""): return ("Circ", k[1])
  if k[0] == "VGy" and re.search(r"(cc|cm³|cm3)", seuil or ""):
    v = nombre(seuil); return ("Dcc", v) if v is not None else k
  return k
def param_rocc(c):
  parts = re.split(r"[≤≥<>]", c, 1)
  return vers_dcc(cle_param(parts[0]), parts[1] if len(parts) > 1 else "")
EFFETS = {"Cystitis/Fistula":"cystite, fistule","G3+ Neuritis":"névrite grade ≥ 3","Pain or fracture":"douleur ou fracture","Colitis/Fistula":"colite, fistule",
 "G3+ cranial neuropathy":"neuropathie crânienne grade ≥ 3","Ulceration":"ulcération","Enteritis/obstruction":"entérite, occlusion","Proctitis/Fistula":"rectite, fistule",
 "G3+ Myelitis":"myélite grade ≥ 3","G3+ Pericarditis":"péricardite grade ≥ 3","sphincter dysfunction":"trouble sphinctérien","Necrosis":"nécrose","Neuropathy":"neuropathie",
 "Erectile dysfunction":"dysfonction érectile","Laryngeal edema, dysphagia":"œdème laryngé, dysphagie","Esophagitis":"œsophagite","G3+ RILD":"hépatopathie radique grade ≥ 3",
 "Necrosis, laryngeal edema, Dysphagia and aspiration":"nécrose, œdème laryngé, dysphagie, inhalation","Xerostomia, dysgeusia, oral mucositis":"xérostomie, dysgueusie, mucite",
 "G3+ optic neuritis":"névrite optique grade ≥ 3","G3+ Hearing loss":"surdité grade ≥ 3","Symptomatic necrosis":"radionécrose symptomatique","Cognitive Deterioration":"déclin cognitif",
 "Xerophthalmia":"xérophtalmie","Memory loss (short term), free delayed recall":"troubles de la mémoire (rappel différé)","Fracture":"fracture","G5 Pneumonitis":"pneumopathie mortelle (grade 5)",
 "G3+ Pneumonitis":"pneumopathie grade ≥ 3","Renal Insufficiency":"insuffisance rénale","Grade 3+ renal function":"atteinte rénale grade ≥ 3","Basic Renal Function":"fonction rénale",
 "Breast adenocarcinoma":"cancer du sein radio-induit"}
def det_html(d):
  if not d: return ""
  v = [("Effet évité : " + e(EFFETS.get(d["effet"].strip(), d["effet"]))) if d.get("effet") else "", ("Site : " + e(d["site"])) if d.get("site") else "",
       ("α/β " + e(d["ab"])) if d.get("ab") else "", ("Articles : " + e(", ".join(d["refs"]))) if d.get("refs") else ""]
  v = [x for x in v if x]
  return f'<div class=det>{" · ".join(v)}</div>' if v else ""
FORT = {"Must", "Mandatory", "Absolute"}
def choisir(gen, loc, r):
  # 1. Onco360 (RecoRad 2025 surtout) : toutes les lignes générales, sans doublon ; les lignes par localisation gardées (doublons retirés dans la même localisation)
  pro_o, pris, raison = set(), [], {}
  for x in gen:
    k = vers_dcc(cle_param(x["indicateur"]), x.get("limitant", ""))
    if any(proches(k, y) for y in pris): continue
    pro_o.add(x["id"]); pris.append(k)
  vu_loc = {}
  for x in loc:
    k = vers_dcc(cle_param(x["indicateur"]), x.get("limitant", "")); L = vu_loc.setdefault(tuple(x["loc"]), [])
    if any(proches(k, y) for y in L): continue
    pro_o.add(x["id"]); L.append(k)
  # 2. RadOncCalc : High Yield, Must, Mandatory, Absolute d'office ; puis Should / Recommended / Optimal / Consensus si citées par 2 sources ou plus ;
  #    jamais réirradiation ni curiethérapie (fiches à part) ; jamais un paramètre déjà pris ou très proche
  pro_r = set()
  def essai(j, x):
    k = param_rocc(x["c"])
    if k[0] == "?": raison[j] = "Contrainte non chiffrée, laissée de côté"; return
    dbl = next((y for y in pris if proches(k, y)), None)
    if dbl: raison[j] = "Même paramètre qu'une ligne déjà retenue"; return
    pro_r.add(j); pris.append(k)
  hors = lambda x: any(t in ("Re-irradiation", "Brachy", "Brachy/EBRT") for t in x["sit"])
  for j, x in enumerate(r):
    if hors(x): raison[j] = "Réirradiation ou curiethérapie : fiche à part"; continue
    if x["hy"] or FORT & set(x["imp"]): essai(j, x)
  for j, x in enumerate(r):
    if j in pro_r or j in raison or hors(x): continue
    if set(x["imp"]) & {"Should", "Recommended", "Optimal", "Consensus"} and len(x["src"]) >= 2: essai(j, x)
  return pro_o, pro_r, raison
def lib_g(g):
  return "Normofractionné" if g == "N" else ("Bifractionné" if g == "BID" else ("Stéréotaxie, toutes séances" if g == "S*" else f"{g} séance" + ("s" if g > 1 else "")))
CIBLES = set(); TEMOINS = []; parties = []; n_prop = 0; stats = C.Counter()
par_oar = C.defaultdict(list)
for k in sorted(G, key=cle_tri): par_oar[k[0]].append(k)
for oid in sorted(par_oar, key=lambda o: noms.get(o, o)):
  blocs = []
  for k in par_oar[oid]:
    o = G[k]["o"]; r = [x for x in G[k]["r"] if "Obsolete" not in x["imp"]]
    obs = len(G[k]["r"]) - len(r)
    gen = [x for x in o if not x.get("loc")]; loc = [x for x in o if x.get("loc")]
    r.sort(key=lambda x: -x["sc"])
    pro_o, pro_r, raison = choisir(gen, loc, r)
    CIBLES.update(r[j]["s"] for j in pro_r)
    stats["groupes"] += 1; stats["onco_seul" if not r else ("rocc_seul" if not o else "les_deux")] += 1
    stats["ajouts_proposes"] += len(pro_r); stats["retenues"] += len(pro_o) + len(pro_r)
    lo = "".join(f'<li><label><input type=checkbox data-k="o:{e(x["id"])}" {"checked" if x["id"] in pro_o else ""}> <b>{e(x["indicateur"])}</b> '
      + (f'idéal {e(x["ideal"])} · ' if x.get("ideal") else "") + f'{e(x.get("limitant",""))}'
      + (f' <span class=loc>{e(", ".join(x["loc"]))}</span>' if x.get("loc") else "")
      + f' <span class=src>{e(x["source"])}</span>' + (f'<div class=note>{e(x["note"])}</div>' if x.get("note") else "") + "</label></li>" for x in gen + loc)
    lr = "".join(f'<li><label><input type=checkbox data-k="r:{e(oid)}|{e(str(k[1]))}|{e(x["c"])}|{e(x["org"])}" {"checked" if j in pro_r else ""}> <b>{e(x["c"])}</b>'
      + (f' <span class=org>{e(x["org"])}</span>' if x["org"] not in (oid,) else "")
      + "".join(f' <span class="b {"b-r" if t in ("Must","Mandatory","Absolute") else "b-o"}">{e(t.replace("⚠️CAUTION⚠️","Prudence"))}</span>' for t in x["imp"])
      + (' <span class="b b-v">High Yield</span>' if x["hy"] else "") + "".join(f' <span class="b b-g">{e(t)}</span>' for t in x["sit"])
      + f' <span class=src>{e(" ; ".join(x["src"]))}</span>'  + det_html(x["det"]) + (f'<div class=note>{e(raison[j])}</div>' if j in raison else "") + '</label></li>' for j, x in enumerate(r) if j < 12 or j in pro_r)
    plus = f'<div class=m>+ {len(r) - len([j for j in range(len(r)) if j < 12 or j in pro_r])} autres lignes RadOncCalc, moins citées</div>' if len(r) - len([j for j in range(len(r)) if j < 12 or j in pro_r]) > 0 else ""
    blocs.append(f'<tr><td data-l="Séances">{e(lib_g(k[1]))}</td><td data-l="Onco360 aujourd’hui"><ul>{lo or "<span class=m>Aucune</span>"}</ul></td>'
      f'<td data-l="RadOncCalc"><ul>{lr or "<span class=m>Aucune</span>"}</ul>{plus}' + (f'<div class=m>{obs} ligne(s) « Obsolete » écartée(s)</div>' if obs else "") + "</td></tr>")
  TEMOINS.append((oid, [(lib_g(k[1]), [x["indicateur"]+" "+x.get("limitant","") for x in G[k]["o"] if x["id"] in choisir([y for y in G[k]["o"] if not y.get("loc")],[y for y in G[k]["o"] if y.get("loc")],[z for z in G[k]["r"] if "Obsolete" not in z["imp"]])[0] and not x.get("loc")], [z["c"] for j,z in enumerate(sorted([z for z in G[k]["r"] if "Obsolete" not in z["imp"]],key=lambda z:-z["sc"])) if j in choisir([y for y in G[k]["o"] if not y.get("loc")],[y for y in G[k]["o"] if y.get("loc")],sorted([z for z in G[k]["r"] if "Obsolete" not in z["imp"]],key=lambda z:-z["sc"]))[1]]) for k in par_oar[oid]]))
  parties.append(f'<section class=carte id="{e(oid)}"><h2>{e(noms.get(oid, oid))}{BADGE if oid in NOUV else ""}</h2><table><thead><tr><th>Séances</th><th>Onco360 aujourd’hui</th><th>RadOncCalc</th></tr></thead><tbody>{"".join(blocs)}</tbody></table></section>')
sommaire = " · ".join(f'<a href="#{e(o)}">{e(noms.get(o, o))}</a>' for o in sorted(par_oar, key=lambda o: noms.get(o, o)))
page = open(sys.argv[-1] + ".modele").read() if False else None
CSS = """:root{--f:#F1F5FB;--b:#3563B0;--t:#1d2433;--m:#5b6475;--l:#dfe5ef;--r:#B3261E;--rc:#FBEAEA;--v:#1F8A4C;--vc:#DFF3E6;--o:#9A5B00;--oc:#FFF2D9;--g:#3c4a63;--gc:#E8ECF3}
body{margin:0;background:var(--f);font:14px/1.45 Arial,sans-serif;color:var(--t)}main{max-width:1300px;margin:0 auto;padding:20px 16px 90px}
h1{font-size:22px;margin:0 0 6px}h2{font-size:17px;margin:0 0 8px}.m{color:var(--m);font-size:12px}.carte{background:#fff;border-radius:10px;padding:14px 16px;margin:12px 0;box-shadow:0 1px 2px #0001}
table{width:100%;border-collapse:collapse}th,td{text-align:left;vertical-align:top;padding:7px 8px;border-bottom:1px solid var(--l)}th{background:#E3ECF9;font-size:12px}td:first-child{width:130px;font-weight:bold}
td:nth-child(2),td:nth-child(3){width:45%}ul{margin:0;padding:0;list-style:none}li{margin:3px 0}label{cursor:pointer}input{vertical-align:-2px}
.src{color:var(--m);font-size:12px}.loc{background:var(--gc);color:var(--g);border-radius:8px;padding:0 6px;font-size:11px}.org{color:var(--m);font-size:11px;font-style:italic}
.det{color:#1F5E3A;font-size:12px;margin-left:22px}.note{color:var(--m);font-size:12px;margin-left:22px}.b{display:inline-block;font-size:11px;border-radius:8px;padding:0 6px}.b-r{background:var(--rc);color:var(--r)}.b-o{background:var(--oc);color:var(--o)}
.b-v{background:var(--vc);color:var(--v)}.b-g{background:var(--gc);color:var(--g)}.som{font-size:12px;line-height:1.9}.som a{color:var(--b);text-decoration:none}
.barre{position:fixed;bottom:0;left:0;right:0;background:#fff;border-top:1px solid var(--l);padding:10px 16px;display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap}
button{background:var(--b);color:#fff;border:0;border-radius:8px;padding:9px 16px;font:bold 14px Arial;cursor:pointer}
@media(max-width:760px){thead{display:none}tr{display:block;border-bottom:2px solid var(--l)}td{display:block;border:0;width:auto!important}td:before{content:attr(data-l);display:block;font-size:11px;color:var(--m);font-weight:normal}}"""
JS = """const K='onco360.choixRocc2';function lire(){try{return JSON.parse(localStorage.getItem(K)||'{}')}catch(e){return{}}}
const S=lire();document.querySelectorAll('input[data-k]').forEach(i=>{if(i.dataset.k in S)i.checked=S[i.dataset.k];i.addEventListener('change',()=>{S[i.dataset.k]=i.checked;try{localStorage.setItem(K,JSON.stringify(S))}catch(e){}compter()})});
function compter(){document.getElementById('n').textContent=document.querySelectorAll('input[data-k]:checked').length+' lignes retenues'}compter();
document.getElementById('exp').onclick=()=>{const t=[...document.querySelectorAll('input[data-k]:checked')].map(i=>i.dataset.k);const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(t,null,1)],{type:'application/json'}));a.download='choix-contraintes.json';a.click()};"""
out = f"""<!doctype html><html lang=fr><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Contraintes : choix des lignes</title><style>{CSS}</style></head><body><main>
<h1>Contraintes des organes à risque : quelles lignes garder ?</h1>
<p class=m>Pour chaque organe et chaque nombre de séances : à gauche ce qu’affiche Onco360 aujourd’hui (RecoRad 2025 surtout), à droite RadOncCalc (relevé du 30/10/2026, lignes « Obsolete » écartées, les plus citées en premier).
Cases cochées = ma proposition : toutes les lignes d’Onco360 sans doublon ; RadOncCalc « High Yield », « Must », « Mandatory », « Absolute » d’office ; « Should », « Recommended », « Optimal », « Consensus » si au moins deux sources ; jamais un paramètre déjà retenu ou très proche (même Dmax / D0.03-0.1 cc, même Dmean, Vx Gy à ± 15 %, D cc du simple au double) ; réirradiation et curiethérapie à part. Cochez ou décochez ; vos choix restent enregistrés dans ce navigateur. À la fin : « Enregistrer mes choix » et envoyez-moi le fichier.</p>
<p class=m>{stats['groupes']} couples organe × séances · {stats['les_deux']} avec les deux sources · {stats['onco_seul']} Onco360 seul · {stats['rocc_seul']} RadOncCalc seul · {stats['retenues']} lignes retenues dont {stats['ajouts_proposes']} venues de RadOncCalc.
Les lignes avec une localisation (gris) ne s’affichent que dans les fiches de cette localisation. La source affichée dans Onco360 sera l’essai ou la recommandation d’origine, pas RadOncCalc.</p>
<div class="carte som">{sommaire}</div>{''.join(parties)}</main>
<div class=barre><span id=n class=m></span><button id=exp>Enregistrer mes choix</button></div><script>{JS}</script></body></html>"""
open(sys.argv[-1], "w").write(out)
print(dict(stats)); json.dump(sorted(CIBLES), open("cibles.json","w"), ensure_ascii=False); print(len(CIBLES), "fiches à ouvrir")
for oid, gs in TEMOINS:
  if oid in ("oar-coeur","oar-moelle","oar-poumons","oar-rectum"):
    print("==", oid)
    for g, o, r in gs: print("  ", g, "| O:", o, "| R:", r)
