# Phase RTX, lot 6d (01/11/2026, demande de Dr Bentahila) : l'onglet Essais liste toutes les sources du référentiel, pas seulement celles des schémas :
# contraintes de dose (base et jeux), contourage (donnees-rt/contourage), définitions des organes à risque (oar.json), atlas des volumes.
# Chaque nom de source est relié à une fiche de essais.json (champ « alias ») ; une source sans fiche en reçoit une, faite avec ce que dit son nom
# (les noms des contraintes de base viennent de RadOncCalc, sans revue ni année : rien n'est ajouté). « usages » = où la fiche sert, affiché dans
# l'onglet. Idempotent ; contrôlé par tests/moteur/test-rtref-contenu.mjs. Lancer en dernier : python3 docs/radiotherapie/construction/essais_sources.py
import json, re, glob, pathlib

R = pathlib.Path(__file__).resolve().parents[3] / "public" / "donnees-rt"
lire = lambda f: json.loads((R / f).read_text())
def ecrire(f, d): (R / f).write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
SANS = {"Pratique usuelle", "Source à préciser", "Tableur du service « Canal anal » (pratique du service)", "Fiche du service", "Fiche du service (atlas RTOG, RECORAD)"}

def N(id_, acr, typ, revue="", annee=None, doi=None, pop="", pmid=None):
  x = {"id": "src-" + id_, "acronyme": acr, "type": typ}
  if revue: x["revue"] = revue
  if annee: x["annee"] = annee
  if pmid: x["pmid"] = pmid
  if doi: x["doi"] = doi
  if pop: x["population"] = pop
  return x
RAD = "Contraintes de dose (source citée par RadOncCalc)"
NRG = lambda k: N(k.lower().replace(" ", ""), k, "protocole_institutionnel", "Protocole " + k, pop=RAD)
RTOG = lambda k: N("rtog" + k, "RTOG " + k, "protocole_institutionnel", "Protocole RTOG " + k, pop=RAD)
VA = lambda k, s, a: N("va-" + k, "Consensus VA, " + s + " " + str(a), "recommandation", "Consensus des Veterans Affairs (États-Unis)", a, pop="Contraintes de dose, " + s)
NCCN = lambda k, s, v, a: N("nccn-" + k, "NCCN " + s + " (version " + v + ")", "recommandation", "Recommandations NCCN", a, pop="Contraintes de dose, " + s)
RECO = lambda k, s: N("recorad2025-" + k, "RecoRad 2025, " + s, "recommandation", "Recommandations de la SFRO (RecoRad), 2025", 2025, pop="Contraintes de dose, " + s)
ASTRO = lambda k, s, a: N("astro-" + k, "ASTRO, " + s + (" (" + str(a) + ")" if a else ""), "recommandation", "Recommandation de l'ASTRO", a, pop="Contraintes de dose, " + s)

# Règles : (expression régulière sur le nom de la source, id d'une fiche existante ou fiche neuve). Première règle qui correspond.
REGLES = [
  (r"AEWS 1031$", N("aews1031", "COG AEWS1031", "protocole_institutionnel", "Protocole du Children's Oncology Group", pop=RAD)),
  (r"AREN 1921$", N("aren1921", "COG AREN1921", "protocole_institutionnel", "Protocole du Children's Oncology Group", pop=RAD)),
  (r"ARST 1431$", N("arst1431", "COG ARST1431", "protocole_institutionnel", "Protocole du Children's Oncology Group", pop=RAD)),
  (r"CALGB 30610$|RTOG 0538$", "calgb30610"),
  (r"CALGB 80803$", N("calgb80803", "CALGB 80803", "protocole_institutionnel", "Protocole CALGB 80803", pop=RAD)),
  (r"CHHiP$|Protocole CHHiP", "chhip"),
  (r"CORSAIR$", N("corsair", "CORSAIR", "recommandation", pop=RAD)),
  (r"Casey, Annals of Surgical Oncology 2020$", N("casey2020", "Casey 2020", "essai", "Ann Surg Oncol", 2020, pop=RAD)),
  (r"Consensus NRG, hématologie \(2026\)$", N("nrg-hemato-2026", "Consensus NRG, hématologie", "recommandation", "NRG Oncology", 2026, pop=RAD)),
  (r"Consensus VA \(Veterans Affairs\), ORL 2022$", VA("orl", "ORL", 2022)),
  (r"Consensus VA \(Veterans Affairs\), poumon 2023$", VA("poumon", "poumon", 2023)),
  (r"Consensus VA \(Veterans Affairs\), prostate 2022$", VA("prostate", "prostate", 2022)),
  (r"Consensus VA \(Veterans Affairs\), rectum 2022$", VA("rectum", "rectum", 2022)),
  (r"Consensus VA \(Veterans Affairs\), sein 2022$", VA("sein", "sein", 2022)),
  (r"Consensus VA / ASTRO, Practical Radiation Oncology 2026(, tableau \d+)?$", dict(N("va-astro-2026", "Consensus VA / ASTRO 2026", "recommandation", "Pract Radiat Oncol", 2026,
    "10.1016/j.prro.2025.11.003", "Compendium des contraintes de dose (histogrammes dose-volume) pour la planification, 25 tableaux par localisation et fractionnement"),
    resultat="Objectifs principaux et secondaires par organe et par fractionnement (sein, ORL, foie, poumon, prostate, rectum), avec les références de chaque valeur")),
  (r"Consensus britannique SABR 2017$", N("uk-sabr-2017", "Consensus britannique SABR 2017", "recommandation", "UK SABR Consortium", 2017, pop="Contraintes de dose en stéréotaxie")),
  (r"Consensus britannique SABR 2022$", N("uk-sabr-2022", "Consensus britannique SABR 2022", "recommandation", "UK SABR Consortium", 2022, pop="Contraintes de dose en stéréotaxie")),
  (r"DAHANCA 20$", NRG("DAHANCA 20")), (r"DAHANCA 25$", NRG("DAHANCA 25")),
  (r"DBCG SKAGEN$", N("skagen", "DBCG SKAGEN Trial 1", "protocole_institutionnel", "Protocole DBCG", pop=RAD)),
  (r"DELINEATE$", NRG("DELINEATE")), (r"DOSE-Pro Thoracic$", N("dose-pro-thoracic", "DOSE-Pro Thoracic", "recommandation", pop=RAD)),
  (r"Dickie, IJROBP 2009$", N("dickie2009", "Dickie 2009", "essai", "Int J Radiat Oncol Biol Phys", 2009, pop=RAD)),
  (r"EA2183$", NRG("EA2183")), (r"EMBRACE II|Protocole EMBRACE II", "embrace2"),
  (r"FASTRACK II$", "fastrack2"), (r"FIL Chest$", N("fil-chest", "FIL Chest", "protocole_institutionnel", "Fondazione Italiana Linfomi", pop=RAD)),
  (r"(hypo-)?FLAME", "flame"), (r"Florence", "florence"),
  (r"George, Clinical Oncology 2020$", N("george2020", "George 2020", "essai", "Clin Oncol", 2020, pop=RAD)),
  (r"Gustave Roussy, RCMI", "igr-orl-rcmi"),
  (r"Gustave Roussy, stéréotaxie 2018$", N("igr-stereo-2018", "Gustave Roussy, stéréotaxie 2018", "protocole_institutionnel", "Gustave Roussy", 2018, pop="Tableau des contraintes de dose en stéréotaxie")),
  (r"Gustave Roussy, stéréotaxie hépatique", "igr-foie-sbrt"), (r"Gustave Roussy \(Achkar 2025\)", "achkar2025-penis"),
  (r"HYPORT-STS", "hyport-sts"), (r"HyTEC 2021 \(Sahgal", "hytec-moelle"),
  (r"HyTEC$", N("hytec", "HyTEC (ensemble des articles)", "recommandation", "Int J Radiat Oncol Biol Phys (numéro spécial)", 2021, pop="Contraintes de dose en hypofractionnement et stéréotaxie")),
  (r"ILROG$", N("ilrog", "ILROG", "recommandation", "International Lymphoma Radiation Oncology Group", pop=RAD)),
  (r"IROCK$", "siva2016-irock"),
  (r"Institut Curie 2021 \(protocoles col", N("curie-gyn-2021", "Institut Curie, protocoles col-vagin, endomètre, vulve", "protocole_institutionnel", "Institut Curie", 2021, pop="Contraintes de dose")),
  (r"Institut Curie 2021, protocoles RT des VADS", N("curie-vads-2021", "Institut Curie, protocoles RT des VADS", "protocole_institutionnel", "Institut Curie", 2021, pop="Contraintes de dose, tumeur en place et opérée")),
  (r"Institut Curie, SBRT d'un nodule pulmonaire", N("curie-sbrt-poumon", "Institut Curie, SBRT d'un nodule pulmonaire", "protocole_institutionnel", "Institut Curie (version du 05/12/2021)", 2021, pop="Contraintes de dose")),
  (r"Institut Curie, stéréotaxie des métastases cérébrales", N("curie-stereo-crane", "Institut Curie, stéréotaxie des métastases cérébrales", "protocole_institutionnel", "Institut Curie (version de travail du 05/12/2021)", 2021, pop="Contraintes de dose, d'après l'AAPM")),
  (r"Procédure Curie", N("curie-volumes-stereo", "Institut Curie, volumes de stéréotaxie intracrânienne", "protocole_institutionnel", "Institut Curie", pop="Modèle « Volumes Stéréotaxie intracrânienne »")),
  (r"Lakomy, Practical Radiation Oncology 2021$", N("lakomy2021", "Lakomy 2021", "essai", "Pract Radiat Oncol", 2021, pop=RAD)),
  (r"LungTECH$", NRG("LungTECH")), (r"LymphoTEC$", NRG("LymphoTEC")),
  (r"MD Anderson \(Garg 2011\)", "garg2011"), (r"MD Anderson$", N("mdacc", "MD Anderson", "protocole_institutionnel", "MD Anderson Cancer Center", pop=RAD)),
  (r"Meade, Clinical Oncology 2018$", N("meade2018", "Meade 2018", "essai", "Clin Oncol", 2018, pop=RAD)),
  (r"Memorial Sloan Kettering \(Lee 2007\)", "lee2007-reirr"), (r"Memorial Sloan Kettering$", N("mskcc", "Memorial Sloan Kettering", "protocole_institutionnel", "Memorial Sloan Kettering Cancer Center", pop=RAD)),
  (r"Miami SMART$", N("miami-smart", "Miami SMART", "protocole_institutionnel", "Miami Cancer Institute", pop=RAD)),
  (r"Murphy, IJROBP 2010$", N("murphy2010", "Murphy 2010", "essai", "Int J Radiat Oncol Biol Phys", 2010, pop=RAD)),
  (r"NCIC CTV BR.25$", NRG("NCIC CTG BR.25")),
  (r"NRG CC001", "nrg-cc001"),
  (r"NRG BR002$", NRG("NRG BR002")), (r"NRG DT001$", NRG("NRG DT001")), (r"NRG GI002$", NRG("NRG GI002")), (r"NRG GU001$", NRG("NRG GU001")),
  (r"NRG GU005$", NRG("NRG GU005")), (r"NRG GU013$", NRG("NRG GU013")), (r"NRG HN003$", NRG("NRG HN003")), (r"NRG HN005$", NRG("NRG HN005")),
  (r"NRG LU004$", NRG("NRG LU004")), (r"NRG LU005$", NRG("NRG LU005")),
  (r"NRG Pancreas 2024$", N("nrg-pancreas-2024", "NRG, pancréas 2024", "recommandation", "NRG Oncology", 2024, pop=RAD)),
  (r"NRG Prostate 2020$", N("nrg-prostate-2020", "NRG, prostate 2020", "recommandation", "NRG Oncology", 2020, pop=RAD)),
  (r"NRG, stéréotaxie ORL$", N("nrg-stereo-orl", "NRG, stéréotaxie ORL", "recommandation", "NRG Oncology", pop=RAD)),
  (r"NSABP B-51$", NRG("NSABP B-51")),
  (r"Noël 2025 SFRO$", N("noel2025", "Noël 2025 (SFRO)", "recommandation", "Société française de radiothérapie oncologique", 2025, pop="Contraintes de dose")),
  (r"Protocole PACE \(version 1", N("pace-protocole-v1", "PACE, protocole (version 1)", "protocole_institutionnel", "Protocole PACE", 2011, pop="Contraintes de dose, tableau 9")),
  (r"Guide de planification PACE", N("pace-guide-v22", "PACE, guide de planification (version 2.2)", "protocole_institutionnel", "Protocole PACE", 2020, pop="Contraintes de dose, tableau 6")),
  (r"PACE$", "paceb"),
  (r"PENTEC$", N("pentec", "PENTEC", "recommandation", "Int J Radiat Oncol Biol Phys (numéro spécial, pédiatrie)", 2024, pop=RAD)),
  (r"PIVOTALboost$", NRG("PIVOTALboost")), (r"PIVOTAL$", NRG("PIVOTAL")), (r"PREMER$", NRG("PREMER")), (r"PROSPECT$", NRG("PROSPECT")),
  (r"Practical Radiation Oncology 2021, oligométastases$", N("pro-oligo-2021", "Practical Radiation Oncology 2021, oligométastases", "recommandation", "Pract Radiat Oncol", 2021, pop="Contraintes de dose en stéréotaxie des oligométastases")),
  (r"QUANTEC$", N("quantec", "QUANTEC (ensemble des articles)", "recommandation", "Int J Radiat Oncol Biol Phys 76 (numéro spécial)", 2010, pop="Contraintes de dose des organes à risque")),
  (r"RAIDER$", NRG("RAIDER")), (r"RADICALS|Protocole RADICALS", "radicals-rt"),
  (r"RTOG 0126$", RTOG("0126")), (r"RTOG 0415$", "rtog0415"), (r"RTOG 0418$", RTOG("0418")), (r"RTOG 0438$", RTOG("0438")),
  (r"RTOG 0529", "rtog0529"), (r"RTOG 0534$|Protocole RTOG 0534|SPPORT$", "spport"), (r"RTOG 0539$", "rtog0539-int"),
  (r"RTOG 0617$", "rtog0617"), (r"RTOG 0618$", RTOG("0618")), (r"RTOG 0630$", "rtog0630"), (r"RTOG 0631$", "rtog0631"), (r"RTOG 0724$", RTOG("0724")),
  (r"RTOG 0813$|Protocole RTOG 0813", "rtog0813"), (r"RTOG 0815$", RTOG("0815")), (r"RTOG 0822$", RTOG("0822")), (r"RTOG 0825$", "rtog0825"),
  (r"RTOG 0915$", "rtog0915"), (r"RTOG 0933", "rtog0933"), (r"RTOG 0938$", RTOG("0938")), (r"RTOG 1005$", RTOG("1005")), (r"RTOG 1010$", RTOG("1010")),
  (r"RTOG 1016", "rtog1016"), (r"RTOG 1112$", "rtog1112"), (r"RTOG 1203$", RTOG("1203")), (r"RTOG 1205$", "rtog1205"), (r"RTOG 1308$", RTOG("1308")),
  (r"RTOG 0225", "rtog0225"), (r"RTOG 0236", "rtog0236"),
  (r"RecoRad 2022", N("recorad2022", "RecoRad 2022", "recommandation", "Recommandations de la SFRO (RecoRad), 2022", 2022, pop="Contraintes de dose")),
  (r"RecoRad 2025 \(ORL\)$", RECO("orl", "ORL")), (r"RecoRad 2025 \(canal anal\)$", RECO("canal-anal", "canal anal")), (r"RecoRad 2025 \(encéphale\)$", RECO("encephale", "encéphale")),
  (r"RecoRad 2025 \(foie\)$", RECO("foie", "foie")), (r"RecoRad 2025 \(gynécologie\)$", RECO("gyneco", "gynécologie")), (r"RecoRad 2025 \(pancréas\)$", RECO("pancreas", "pancréas")),
  (r"RecoRad 2025 \(poumon\)$", RECO("poumon", "poumon")), (r"RecoRad 2025 \(prostate\)$", RECO("prostate", "prostate")), (r"RecoRad 2025 \(rectum\)$", RECO("rectum", "rectum")),
  (r"RecoRad 2025 \(rein\)$", RECO("rein", "rein")), (r"RecoRad 2025 \(sein\)$", RECO("sein", "sein")), (r"RecoRad 2025 \(testicule\)$", RECO("testicule", "testicule")),
  (r"RecoRad 2025 \(vessie\)$", RECO("vessie", "vessie")), (r"RecoRad 2025 \(œsophage\)$", RECO("oesophage", "œsophage")),
  (r"RecoRad, délinéation 2021$", "src-noel2021-oar"),
  (r"Recommandation ASTRO, RT après mastectomie \(2025\)$", ASTRO("pmrt", "RT après mastectomie", 2025)), (r"Recommandation ASTRO, estomac \(2025\)$", ASTRO("estomac", "estomac", 2025)),
  (r"Recommandation ASTRO, foie \(2021\)$", ASTRO("foie", "foie", 2021)), (r"Recommandation ASTRO, oropharynx HPV\+$", ASTRO("oropharynx", "oropharynx HPV+", None)),
  (r"Recommandation ASTRO, pancréas \(2026\)$", ASTRO("pancreas", "pancréas", 2026)), (r"Recommandation ESTRO-ACROP, pancréas", "acrop-pancreas"),
  (r"Recommandation ESTRO-EANO, glioblastome$", N("estro-eano-gbm", "ESTRO-EANO, glioblastome", "recommandation", pop=RAD)),
  (r"Recommandations NCCN, ORL", NCCN("orl", "ORL", "1.2026", 2026)), (r"Recommandations NCCN, canal anal", NCCN("canal-anal", "canal anal", "1.2026", 2026)),
  (r"Recommandations NCCN, col utérin", NCCN("col", "col utérin", "2.2026", 2026)), (r"Recommandations NCCN, estomac", NCCN("estomac", "estomac", "2.2026", 2026)),
  (r"Recommandations NCCN, lymphome de Hodgkin", NCCN("hodgkin", "lymphome de Hodgkin", "1.2026", 2026)),
  (r"Recommandations NCCN, médulloblastome", NCCN("medullo", "médulloblastome de l'enfant", "1.2026", 2026)),
  (r"Recommandations NCCN, néphroblastome", NCCN("nephro", "néphroblastome", "2.2025", 2025)), (r"Recommandations NCCN, pancréas", NCCN("pancreas", "pancréas", "2.2025", 2025)),
  (r"Recommandations NCCN, poumon non à petites", NCCN("cbnpc", "poumon non à petites cellules", "3.2026", 2026)),
  (r"Recommandations NCCN, œsophage", NCCN("oesophage", "œsophage et jonction", "2.2026", 2026)),
  (r"S2427$", NRG("SWOG S2427")), (r"SC.24|Protocole CCTG SC.24", "sc24"), (r"STAMPEDE M1$", "stampede-h"), (r"SUNSET$", N("sunset", "SUNSET", "essai", "Int J Radiat Oncol Biol Phys", 2024, pop="Stéréotaxie des CBNPC ultra-centraux 60 Gy / 8 fx, phase 1")),
  (r"Sunnybrook", "morton-hdr"),
  (r"TG-101$", N("tg101", "AAPM TG-101", "recommandation", "Med Phys", 2010, pop="Contraintes de dose en stéréotaxie")),
  (r"TIME-C$", RTOG("1203")),
  (r"Timmerman 2008, table", N("timmerman2008", "Timmerman 2008, table des tolérances", "recommandation", "Semin Radiat Oncol", 2008, pop="Contraintes de dose en stéréotaxie")),
  (r"Timmerman 2021, table", N("timmerman2021", "Timmerman 2021, table des tolérances", "recommandation", "Semin Radiat Oncol", 2021, pop="Contraintes de dose en stéréotaxie")),
  (r"UCLA$", N("ucla", "UCLA", "protocole_institutionnel", "University of California, Los Angeles", pop=RAD)),
  (r"UT Southwestern \(Dallas\)$", N("utsw", "UT Southwestern (Dallas)", "protocole_institutionnel", "UT Southwestern Medical Center", pop=RAD)),
  (r"Université de Floride, pédiatrie$", N("uf-pediatrie", "Université de Floride, pédiatrie", "protocole_institutionnel", "University of Florida", pop=RAD)),
  (r"Université de Floride$", N("uf", "Université de Floride", "protocole_institutionnel", "University of Florida", pop=RAD)),
  # Jeux de contraintes (contraintes.json « essais »)
  (r"GEC-ESTRO ACROP 2022|Recommandation GEC-ESTRO ACROP curiethérapie de prostate", "gec-estro-prostate"), (r"ABS 2012$", "abs-hdr-col"),
  (r"Protocole Neo-AEGIS", "neoaegis-protocole"), (r"FAST-Forward", "fastforward"), (r"DeLaney 2009|Massachusetts General Hospital \(DeLaney 2009\)", "delaney2009"),
  (r"Hypo Trial", "porceddu2007"), (r"GORTEC 2000-01", "gortec2000-01"), (r"Sénorif 2026", "senorif-2026"), (r"Brest \(Lucia 2019\)", "lucia2019"),
  (r"Thésaurus français méningiomes", N("cat-meningiome-2021", "Thésaurus français des méningiomes (CAT-MENINGIOME)", "recommandation", "Thésaurus national", 2021, pop="Radiochirurgie des méningiomes")),
  (r"Consensus NCI / IASLC / MARF mésothéliome", "gomez-meso"), (r"Essai norvégien \(Grønberg 2021\)", "gronberg"),
  (r"CONCORDE / PRODIGE 26", "concorde"), (r"SWOG S0809", "s0809"), (r"Herman 2015", "herman"), (r"Essai français \(Durand-Labrunie 2020\)", "durand-labrunie"),
  (r"Hong 2016", "hong-protons"), (r"Recommandations du GETUG", N("getug-crevoisier2018", "GETUG (de Crevoisier 2018)", "recommandation", "Recommandations du GETUG reprises dans l'essai GETUG-AFU", 2018, pop="Contraintes de dose, prostate")),
  (r"Consensus international, sarcome rétropéritonéal \(Baldini 2015\)", "baldini2015-rps"), (r"Consensus mondial sur le chordome", "stacchiotti2015"),
  (r"Protocole IMPORT HIGH", "import-high"), (r"Protocole CONVERT", "convert"), (r"Protocole CROSS", "cross"), (r"Protocole HILUS", "hilus"),
  (r"Protocole HYPO-RT-PC", "hyportpc"), (r"Protocole POP-RT", "poprt"), (r"Sun 2019, Radiother Oncol", "sun2019-pvtt"),
  (r"Protocole EXTEND", "extend-protocole"), (r"Protocole NRG-GU003", "nrg-gu003"),
  # Atlas cités par les volumes (sans DOI)
  (r"Consensus NCI/IASLC 2019$", "gomez-meso"), (r"EORTC-ROG \(Matzinger 2009\)$", "matzinger"), (r"ESTRO ACROP aires ganglionnaires digestives hautes", "acrop-ggl-gi"),
  (r"RTOG 2012, OAR du pelvis$", "rtog-atlas-oar"), (r"NRG/RTOG 2021, CTV post-opératoire$", "nrg-atlas-postop"), (r"Neo-AEGIS \(protocole\)$", "neoaegis-protocole"),
  (r"Wu 2015$", "wu-oeso"), (r"AGITG 2012$", "agitg-atlas"), (r"RTOG 2009, CTV ano-rectaux$", "myerson-atlas"), (r"Gaffney 2016", "gaffney-vulve"),
  (r"Valentini 2016", "valentini-atlas"), (r"Lim 2011$", "lim-atlas-col"), (r"ESTRO ACROP pancréas 2021$", "acrop-pancreas"), (r"ESTRO ACROP CBNPC 2018$", "acrop-cbnpc"),
  (r"(a|A)tlas OAR thoraciques RTOG \(Kong 2011\)$|Atlas RTOG$", "kong2011"), (r"ESTRO ACROP CBPC 2020$", "acrop-cbpc"), (r"GEC-ESTRO ACROP 2020", "gec-estro-vagin"),
  # Contourage et organes à risque (références sans DOI)
  (r"Matzinger O et al", "matzinger"), (r"Protocole NRG Oncology / RTOG 1112", "rtog1112"), (r"Protocole EMBRACE II \(Image guided", "embrace2"),
  (r"EMBRACE II study protocol", "embrace2"),
  (r"Lapeyre M\. Délinéation des volumes cibles des cancers des VADS, chapitre II", N("lapeyre-ch2", "Lapeyre, délinéation des VADS, chapitre II (CTV-P)", "atlas", "Centre Jean Perrin", 2019, pop="Délinéation des CTV-P (T) des cancers des VADS")),
  (r"Lapeyre M\. Délinéation des volumes cibles, cancers des VADS, chapitre VI", N("lapeyre-ch6", "Lapeyre, délinéation des VADS, chapitre VI (organes à risque)", "atlas", "Centre Jean Perrin", 2019, pop="Délinéation des organes à risque ORL")),
  (r"Redmond KJ et al\. Consensus contouring guidelines for postoperative", "redmond2017"),
  (r"Michalski J\. ACNS0331", N("acns0331-atlas", "ACNS0331, atlas des volumes du médulloblastome", "atlas", "Children's Oncology Group", pop="Volumes cibles et organes à risque du médulloblastome")),
  (r"Gomez D et al\. Radiation therapy definitions and reporting guidelines for thymic", "itmig-gomez2011"),
  (r"eContour\. Intact prostate", N("econtour-prostate", "eContour, prostate en place", "atlas", "eContour (d'après RTOG 0126 et RTOG 0815)", pop="Guide de contourage de la prostate en place")),
  (r"NRG Oncology\. Protocole type, section radiothérapie, vessie", N("nrg-vessie-2020", "NRG, protocole type vessie (section radiothérapie)", "protocole_institutionnel", "NRG Oncology", 2020, pop="Volumes de la vessie")),
  (r"Pacholke HD et al", N("pacholke2005", "Pacholke 2005 (oreille moyenne et interne)", "atlas", "Am J Clin Oncol 28:143", 2005, pop="Contourage de l'oreille moyenne et interne")),
]
# Références citées par le consensus VA / ASTRO 2026 (astro-2026.json, 02/11/2026) : fiche existante (« id ») ou fiche neuve (« fiche »), avant les autres règles
def _astro():
  A = json.loads((pathlib.Path(__file__).resolve().parent / "astro-2026.json").read_text()); r = []
  for x in A["references"].values():
    if "id" in x: r.append((re.escape(x["nom"]) + "$", x["id"]))
    elif "fiche" in x:
      f = dict(x["fiche"]); f["id"] = "src-" + f["id"].removeprefix("src-"); r.append((re.escape(x["nom"]) + "$", f))
  return r
REGLES = _astro() + REGLES

# Références de contourage et d'organes à risque avec DOI, absentes de essais.json : fiche faite à partir de la référence complète
def depuis_ref(ref, doi, usage):
  m = re.match(r"(.+?) [A-Z]{1,3} et al\.|(.+?) [A-Z]{1,3}[,.] ", ref); aut = (m.group(1) or m.group(2) or ref.split()[0]) if m else ref.split()[0]
  an = re.findall(r"\b(19\d\d|20\d\d)\b", ref); an = int(an[0]) if an else None
  rev = re.search(r"\. ((?:Radiother Oncol|Int J Radiat Oncol Biol Phys|Pract Radiat Oncol|J Thorac Oncol|Clin Transl Radiat Oncol|J Neurooncol|Am J Clin Oncol|Cancer Radiother|Brachytherapy|Lancet Oncol)[^.]*)", ref)
  titre = re.sub(r"^.+?et al\. ", "", ref).split(". ")[0]
  rv = re.sub(r"\s*\(.*$", "", re.sub(r" (19|20)\d\d;", " ", rev.group(1))).strip() if rev else ""
  return N(re.sub(r"[^a-z0-9]", "", aut.lower()) + str(an or ""), aut + " " + str(an or "") + " (" + usage + ")", "atlas", rv, an, doi, titre)

# Essais des contraintes résumés dans les tables d'Estes (Key Studies 2025) : revue, année, population, bras, résultat
ESTES = {
  "ilrog": ("Binkley 2020, ILROG", "Blood", 2020, "559 lymphomes folliculaires de stade I–II, rétrospectif multicentrique", "RT, chimiothérapie + RT, chimiothérapie, rituximab ± RT ou surveillance", "SSP à 5 ans 91 % avec la RT seule ou associée à la chimiothérapie, 78 % chimiothérapie seule, 73 % surveillance"),
  "nrgbr002": ("NRG-BR002", "J Clin Oncol", 2026, "125 cancers du sein avec 4 métastases ou moins, sous traitement de 1re ligne depuis 12 mois ou moins, phase II/III", "Stéréotaxie (93 %) ou chirurgie des métastases + traitement standard vs traitement standard", "SSP médiane 19,5 vs 23 mois (p = 0,36) ; SSP à 2 ans 47 % dans les deux bras"),
  "nrggu005": ("NRG GU005", "JAMA", 2026, "698 cancers de la prostate de risque intermédiaire, phase III", "Stéréotaxie 36,25 Gy / 5 fx en 2,5 semaines vs 70 Gy / 28 fx ou 60 Gy / 20 fx", "Survie sans maladie à 3 ans 89 vs 92 % ; toxicité urinaire de grade 3–4 0,6 vs 2,5 % ; moins d'incontinence et de troubles sexuels avec la stéréotaxie"),
  "nrghn005": ("NRG HN005", "ASTRO", 2024, "532 cancers de l'oropharynx HPV+ de bon pronostic, phase II/III", "70 Gy en 6 semaines + cisplatine vs 60 Gy / 30 fx + cisplatine vs 60 Gy / 30 fx + nivolumab", "60 Gy + cisplatine non retenu (non-infériorité non atteinte, bras fermé)"),
  "nsabpb-51": ("NSABP B-51 / RTOG 1304", "N Engl J Med", 2025, "1 641 cancers du sein cN1 devenus ypN0 après chimiothérapie néoadjuvante, phase III", "Sein ou paroi ± aires ganglionnaires (après mastectomie : surveillance vs RT de la paroi et des aires)", "SSR à 5 ans 92 vs 93 % (HR 0,88) : pas de bénéfice de l'irradiation ganglionnaire si ypN0"),
  "premer": ("PREMER", "J Clin Oncol", 2021, "120 cancers bronchiques à petites cellules, phase III", "IPC 25 Gy / 10 fx vs IPC en IMRT avec épargne hippocampique", "Mémoire différée mieux conservée avec l'épargne hippocampique (déclin 11 vs 33 %), bénéfice persistant à 6 mois et 1 an"),
  "prospect": ("PROSPECT", "N Engl J Med", 2023, "1 194 cancers du rectum T2N+ à T3N0–1 candidats à une chirurgie conservatrice, non-infériorité", "Chimiothérapie FOLFOX première avec radiochimiothérapie sélective vs radiochimiothérapie longue avant TME", "Survie sans maladie à 5 ans 81 vs 79 % (non inférieure) ; récidive locale 1,8 vs 1,6 %"),
  "rtog0126": ("RTOG 0126", "Int J Radiat Oncol Biol Phys", 2013, "748 cancers de la prostate de risque intermédiaire", "70,2 Gy vs 79,2 Gy", "Escalade de dose : moins d'échecs biochimiques et de métastases, sans gain de survie ; doses à la vessie et au rectum plus basses en IMRT"),
  "rtog0618": ("RTOG 0618", "JAMA Oncol", 2018, "33 CBNPC T1–T2 N0 opérables, phase II", "Stéréotaxie 54 Gy / 3 fx en 1,5 à 2 semaines", "Contrôle tumoral et local à 4 ans 96 % ; survie sans maladie 57 % et survie globale 56 % à 4 ans"),
  "rtog0724": ("RTOG 0724", "ASCO", 2024, "285 cancers du col opérés à haut risque (marges, ganglions, paramètres)", "Radiochimiothérapie 45–50,4 Gy + cisplatine ± carboplatine–paclitaxel adjuvant", "Survie sans maladie à 4 ans 76–77 % et survie globale 87 % : pas de bénéfice de la chimiothérapie ajoutée"),
  "rtog0815": ("RTOG 0815", "J Clin Oncol", 2023, "1 538 cancers de la prostate de risque intermédiaire", "79,2 Gy (ou 45 Gy + curiethérapie) ± hormonothérapie 6 mois", "Échec biochimique à 5 ans 21 vs 10 %, métastases 4 vs 1 % avec l'hormonothérapie"),
  "rtog0822": ("RTOG 0822", "Int J Radiat Oncol Biol Phys", 2015, "68 cancers du rectum localement avancés, phase II", "IMRT 45 Gy puis complément 3D 5,4 Gy + capécitabine–oxaliplatine, puis chirurgie", "Toxicité digestive de grade ≥ 2 : 51,5 % contre 57,7 % dans RTOG 0247 (différence non significative)"),
  "rtog0938": ("NRG RTOG 0938", "Int J Radiat Oncol Biol Phys", 2018, "240 cancers de la prostate de faible risque, phase II", "36,25 Gy / 5 fx en 2,5 semaines vs 51,6 Gy / 12 fx", "Qualité de vie digestive et urinaire à 1 an identique dans les deux bras"),
  "rtog1005": ("RTOG 1005", "J Clin Oncol", 2026, "2 262 cancers du sein à haut risque après tumorectomie, non-infériorité", "50 Gy / 25 fx ou 42,7 Gy / 16 fx + complément séquentiel 12–14 Gy vs 40 Gy / 15 fx avec complément intégré 48 Gy", "Rechute mammaire à 5 ans 2,1 vs 1,9 % (non inférieure) ; pas plus de toxicité de grade ≥ 3"),
  "rtog1203": ("TIME-C (NRG RTOG 1203)", "J Clin Oncol", 2020, "289 cancers du col ou de l'endomètre opérés, RT pelvienne post-opératoire", "RT 3D vs IMRT", "Moins de diarrhée et d'incontinence rapportées par les patientes avec l'IMRT"),
  "skagen": ("DBCG SKAGEN Trial 1", "ESTRO", 2025, "2 963 cancers du sein avec irradiation ganglionnaire, phase III", "40 Gy / 15–18 fx vs 50 Gy / 25–28 fx, aires ganglionnaires incluses", "Lymphœdème à 3 ans 8,0 vs 9,4 % (non inférieur) ; pas de différence de rechute ni de métastases"),
  "sunset": ("SUNSET", "Int J Radiat Oncol Biol Phys", 2024, "30 CBNPC ultra-centraux, phase I", "Stéréotaxie 60 Gy / 8 fx (désescalade si toxicité)", "Toxicité de grade 3–5 : 7 % (1 décès par pneumopathie) ; contrôle local à 3 ans 90 %"),
}
FR_ATLAS = {
  "biau2019": "Contourage du nerf trijumeau (V) et de ses branches en ORL", "christianen2011": "Organes à risque de la déglutition",
  "feng2011": "Atlas du cœur (exposition cardiaque après irradiation du sein)", "hall2008": "Contourage standardisé du plexus brachial",
  "jabbour2014": "Organes de l'abdomen supérieur (consensus RTOG)", "khan2012": "Marges du CTV des cancers cutanés non mélanomes",
  "lukovic2020": "Organes de l'abdomen supérieur sur IRM", "offersen2015": "Aires ganglionnaires du sein (consensus ESTRO)",
  "rouers2016": "Contourage du maxillaire et de la mandibule", "sun2014": "Organes à risque du cancer du nasopharynx",
  "vandewater2009": "Organes à risque de la xérostomie (glandes salivaires)", "yi2012": "Contourage standardisé du plexus lombo-sacré",
}
def enrichir(x):
  k = x["id"][4:]
  if k in FR_ATLAS: x["population"] = FR_ATLAS[k]
  if x.get("revue") and x.get("annee"): x["revue"] = re.sub(r" " + str(x["annee"]) + r"$", "", x["revue"])
  if k in ESTES:
    a, rv, an, pop, bras, res = ESTES[k]
    x.update({"acronyme": a, "type": "essai", "revue": rv, "annee": an, "population": pop, "bras": bras, "resultat": res})
  return x

def main():
  ess = lire("essais.json"); E = [e for e in ess["essais"] if not e["id"].startswith("src-")]
  for e in E: e.pop("alias", None); e.pop("usages", None)
  par_id = {e["id"]: e for e in E}; par_doi = {e["doi"].lower(): e["id"] for e in E if e.get("doi")}
  neufs = {}
  def fiche(cible):
    if isinstance(cible, str): return cible
    if cible["id"] not in neufs: neufs[cible["id"]] = dict(cible)
    return cible["id"]
  def resoudre(nom, doi=""):
    if nom in SANS: return None
    if doi and doi.lower() in par_doi: return par_doi[doi.lower()]
    if doi and doi.lower() in {x.get("doi", "").lower() for x in neufs.values()}: return next(k for k, x in neufs.items() if x.get("doi", "").lower() == doi.lower())
    for rx, cible in REGLES:
      if re.match(rx, nom): return fiche(cible)
    return False
  # Fiches neuves des références de contourage / OAR qui ont un DOI
  regions = {r["id"]: r["nom"] for r in lire("index.json")["regions"]}
  usages, alias, manque = {}, {}, []
  def noter(id_, nom, us):
    alias.setdefault(id_, set()).add(nom); usages.setdefault(id_, {}).setdefault(us[0], set()).update(us[1:])
  ctg = {}
  for f in sorted(glob.glob(str(R / "contourage" / "*.json"))):
    reg = pathlib.Path(f).stem; ctg[reg] = json.loads(pathlib.Path(f).read_text())
  ctg_noms = {"orl": "ORL", "digestif": "Digestif", "gyneco": "Gynéco", "uro": "Uro", "thorax": "Thorax", "sein": "Sein", "snc": "SNC", "os_palliatif": "Os et palliatif", "sarcome": "Sarcomes", "peau": "Peau", "autres": "Autres"}
  oar = lire("oar.json")
  todo = [(s["ref"], (s.get("doi") or ""), ("Contourage", ctg_noms.get(reg, reg))) for reg, d in ctg.items() for s in d.get("sources", [])]
  todo += [(s["ref"], (s.get("doi") or ""), ("Définitions des organes à risque",)) for s in oar["sources"]]
  for ref, doi, us in todo:
    r = resoudre(ref, doi)
    if r is False and doi:
      x = depuis_ref(ref, doi, "contourage" if us[0] == "Contourage" else "organes à risque")
      if ref.startswith("Noël G"): x["id"] = "src-noel2021-oar"; x["acronyme"] = "RecoRad, délinéation des organes à risque (Noël 2021)"; x["type"] = "recommandation"
      neufs[x["id"]] = x; r = x["id"]
    if r is False: manque.append(ref)
    elif r: noter(r, ref, us)
  if "src-noel2021-oar" not in neufs:
    neufs["src-noel2021-oar"] = N("noel2021-oar", "RecoRad, délinéation des organes à risque (Noël 2021)", "recommandation", "Cancer Radiother", 2021, "10.1016/j.canrad.2021.08.001", "Délinéation des organes à risque")
  # Atlas des volumes
  locs = {l["id"]: l["nom"] for l in lire("index.json")["localisations"]}
  for lid in locs:
    d = lire(lid + ".json")
    for v in d.get("volumes", []):
      for a in v.get("atlas") or []:
        nom = a["nom"] if isinstance(a, dict) else str(a); doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", a.get("url", "")) if isinstance(a, dict) else ""
        r = resoudre(nom, doi)
        if r is False: manque.append(nom)
        elif r: noter(r, nom, ("Volumes", locs[lid]))
  # Contraintes de dose (base) et jeux
  c = lire("contraintes.json"); nb = {}
  for l in c["base"]:
    for s in [x.strip() for x in l.get("source", "").split(" ; ") if x.strip()]:
      r = resoudre(s)
      if r is False: manque.append(s)
      elif r: alias.setdefault(r, set()).add(s); nb[r] = nb.get(r, 0) + 1
  for r, k in nb.items(): usages.setdefault(r, {})["Contraintes de dose (" + str(k) + " ligne" + ("s" if k > 1 else "") + ")"] = set()
  for j in c["essais"]:
    r = resoudre(j["source"])
    if r is False: manque.append(j["source"])
    elif r: noter(r, j["source"], ("Jeu de contraintes", j["titre"]))
    # source propre à une ligne (consensus VA / ASTRO : l'article et les références qu'il cite)
    for l in j["lignes"]:
      for s in [x.strip() for x in l.get("source", "").split(" ; ") if x.strip()]:
        r = resoudre(s)
        if r is False: manque.append(s)
        elif r: noter(r, s, ("Jeu de contraintes", j["titre"]))
  if manque: raise SystemExit("Sources sans fiche :\n  " + "\n  ".join(sorted(set(manque))))
  E += [enrichir(neufs[k]) for k in sorted(neufs)]
  connus = {e["id"] for e in E}
  inconnus = [k for k in list(alias) + list(usages) if k not in connus]
  if inconnus: raise SystemExit("Fiches inconnues : " + ", ".join(sorted(set(inconnus))))
  for e in E:
    if e["id"] in alias: e["alias"] = sorted(alias[e["id"]])
    if e["id"] in usages: e["usages"] = [k + (" : " + ", ".join(sorted(v)) if v else "") for k, v in sorted(usages[e["id"]].items())]
  ess["essais"] = E; ecrire("essais.json", ess)
  print(len(neufs), "fiches ajoutées ;", len(alias), "fiches reliées à une source ;", len(E), "fiches en tout")

if __name__ == "__main__":
  main()
