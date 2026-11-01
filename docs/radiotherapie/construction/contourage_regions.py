# Lot 4 RTX (01/11/2026) : page Contourage, régions autres que l'ORL (contourage_orl.py). Contenu traduit des articles et atlas publiés de la
# Bibliothèque › Contourage (jamais des fiches pratiques du service : décision du 01/11/2026). Une source numérotée par section.
# Lancer : python3 docs/radiotherapie/construction/contourage_regions.py  →  public/donnees-rt/contourage/<région>.json
import json, pathlib
DOSSIER = pathlib.Path(__file__).resolve().parents[3] / "public" / "donnees-rt" / "contourage"
R = {}
def sec(id, titre, locs, colonnes, lignes, src, notes=None):
  s = {"id": id, "titre": titre, "locs": locs, "colonnes": colonnes, "lignes": lignes, "src": src}
  if notes: s["notes"] = notes
  return s
VD = ["Volume", "Définition"]

# ───── SNC ─────
R["snc"] = {"sources": [
  {"n": 1, "ref": "Kruser TJ et al. NRG brain tumor specialists consensus guidelines for glioblastoma contouring. J Neurooncol 2019", "doi": "10.1007/s11060-019-03152-9"},
  {"n": 2, "ref": "Baumert BG et al. ESTRO-EANO guideline on target delineation and radiotherapy for IDH-mutant WHO CNS grade 2 and 3 diffuse glioma. Radiother Oncol 2025;202:110594", "doi": "10.1016/j.radonc.2024.110594"},
  {"n": 3, "ref": "Soliman H et al. Consensus contouring guidelines for postoperative completely resected cavity stereotactic radiosurgery for brain metastases. Int J Radiat Oncol Biol Phys 2018", "doi": "10.1016/j.ijrobp.2017.09.047"},
  {"n": 4, "ref": "Gondi V et al. Hippocampal-sparing whole-brain radiotherapy: a « how-to » technique using helical tomotherapy and linear accelerator-based intensity-modulated radiotherapy. Int J Radiat Oncol Biol Phys 2010", "doi": "10.1016/j.ijrobp.2010.01.039"},
  {"n": 5, "ref": "Michalski J. ACNS0331 Medulloblastoma target volumes and organ at risk atlas. Children's Oncology Group"}],
 "sections": [
  sec("gbm", "Glioblastome : volumes (schéma séquentiel 46 puis 60 Gy)", ["glioblastome"], ["Volume", "Définition", "Tronc cérébral", "Chiasma et nerfs optiques"], [
    ["GTV1", "Hypersignal T2 / FLAIR", "Inclus jusqu'à l'étendue de l'anomalie IRM", "Inclus jusqu'à l'étendue de l'anomalie IRM"],
    ["GTV2", "Cavité + prise de contraste T1", "Idem", "Idem"],
    ["CTV_4600", "2 cm autour de GTV1 et GTV2, corrigé des barrières anatomiques", "Inclus s'il est à moins de 2 cm du FLAIR et en continuité anatomique", "Inclus s'il est à moins de 2 cm du FLAIR et en continuité anatomique"],
    ["CTV_6000", "2 cm autour de GTV2, corrigé des barrières anatomiques", "À moins de 2 cm de la prise de contraste et en continuité : inclus, couvert à environ 54 Gy (PRV Dmax < 55 Gy). Atteinte macroscopique : dans le CTV_6000 sans marge ; 2 cm de tronc autour en CTV_5400 (contraintes « variation acceptable » 60 Gy cœur / 64 Gy surface)", "À moins de 2 cm de la prise de contraste et en continuité : inclus, couvert à environ 54 Gy (PRV < 55 Gy). Au contact de la tumeur : environ 60 Gy, Dmax du PRV jusqu'à 60 Gy"]], [1],
   ["Les mêmes principes s'appliquent au boost intégré 50 et 60 Gy en 30 fractions.", "Hypophyse : peut être exclue du CTV_4600.", "Faux du cerveau : ne pas déborder dans l'hémisphère controlatéral (RTOG : jusqu'à 5 mm au-delà de la faux) ; mais la faux ne descend pas jusqu'au toit des ventricules latéraux : ne pas trop retirer au niveau du corps calleux.", "Tumeur sus-tentorielle (temporale, occipitale) : retirer la partie sous-tentorielle du CTV.", "Thalamus : extension possible par le pédoncule cérébral vers le mésencéphale ; vérifier en coupes coronales. Commissures antérieure et postérieure et adhérence inter-thalamique : voies vers le côté opposé."]),
  sec("gliome", "Gliome diffus IDH-muté de grade 2 et 3", ["gliome"], VD, [
    ["GTV", "Reliquat tumoral et cavité opératoire ; prises de contraste T1 si elles évoquent un reliquat. Grade 2 : anomalies T2 / FLAIR incluses. Grade 3 : anomalies T2 / FLAIR incluses, sauf ce qui est considéré comme de l'œdème."],
    ["CTV", "GTV + 10 mm (grade 2) ; GTV + 15 mm (grade 3)."],
    ["Dose", "50,4 Gy / 28 fx (grade 2) ; 59,4 Gy / 33 fx (grade 3) ; RCMI de préférence."]], [2]),
  sec("cavite", "Métastase opérée (cavité en stéréotaxie), résection complète", ["metastases_cerebrales"], ["Situation", "CTV"], [
    ["Cavité", "Toute la cavité opératoire rehaussée (T1 gadolinium axial) ; œdème exclu."],
    ["Trajet chirurgical", "Tout le trajet visible au scanner ou à l'IRM post-opératoire."],
    ["Tumeur au contact de la dure-mère", "Marge de 5 à 10 mm le long du volet osseux au-delà de la zone de contact initiale."],
    ["Tumeur sans contact dural", "Marge de 1 à 5 mm le long du volet osseux."],
    ["Tumeur au contact d'un sinus veineux", "1 à 5 mm le long du sinus."]], [3]),
  sec("hippo", "Encéphale in toto avec épargne hippocampique", ["metastases_cerebrales"], VD, [
    ["Hippocampe", "Contouré sur l'IRM T1 axiale (coupes fines, recalée sur le scanner)."],
    ["Zone d'évitement", "Hippocampe + 5 mm (expansion volumétrique)."]], [4]),
  sec("medullo", "Médulloblastome : boost du lit tumoral (volume limité)", ["medulloblastome"], VD, [
    ["GTV", "Lit opératoire et reliquat."],
    ["CTV", "GTV + 1,5 cm, limité à la fosse postérieure."],
    ["PTV", "CTV + 0,3 à 0,5 cm."],
    ["Fosse postérieure entière (option)", "CTV = fosse postérieure, PTV autour ; GTV non tracé."],
    ["Irradiation crânio-spinale", "Inclure l'encéphale au-dessus de la lame criblée ; position couchée sur le ventre ou sur le dos ; plan composite (crânio-spinale + boosts) obligatoire."]], [5]),
 ],
 "sans_atlas": {k: "Pas d'atlas de contourage publié dans la Bibliothèque pour cette localisation." for k in ["meningiome", "schwannome", "hypophyse", "craniopharyngiome", "neurocytome", "ependymome"]}}
R["snc"]["sans_atlas"]["meningiome"] = "Pas d'atlas de contourage publié dans la Bibliothèque : la recommandation EANO 2021 donne les indications et les doses, pas les volumes."

# ───── Thorax ─────
R["thorax"] = {"sources": [
  {"n": 1, "ref": "Nestle U et al. ESTRO ACROP guidelines for target volume definition in the treatment of locally advanced non-small cell lung cancer. Radiother Oncol 2018", "doi": "10.1016/j.radonc.2018.02.023"},
  {"n": 2, "ref": "Le Pechoux C et al. ESTRO ACROP guidelines for target volume definition in the thoracic radiation treatment of small cell lung cancer. Radiother Oncol 2020", "doi": "10.1016/j.radonc.2020.07.012"},
  {"n": 3, "ref": "Gomez D et al. Radiation therapy definitions and reporting guidelines for thymic malignancies (ITMIG). J Thorac Oncol 2011;6:S1743-S1748"},
  {"n": 4, "ref": "Gomez DR et al. The use of radiation therapy for the treatment of malignant pleural mesothelioma: expert opinion from the NCI Thoracic Malignancy Steering Committee, IASLC and Mesothelioma Applied Research Foundation. J Thorac Oncol 2019;14:1172-1183", "doi": "10.1016/j.jtho.2019.03.030"}],
 "sections": [
  sec("cbnpc", "Cancer bronchique non à petites cellules localement avancé", ["poumon"], VD, [
    ["Imagerie", "TEP-scanner de planification recommandé, en position de traitement ; 4D-CT ; fenêtre pulmonaire (W 1600 / L −600) pour la tumeur entourée de poumon, médiastinale (W 400 / L 20) pour les ganglions et l'envahissement du médiastin ou de la paroi."],
    ["GTV", "Tumeur et ganglions tracés séparément ; scanner et TEP. Atélectasie hors de la fixation : peut être exclue. Après chimiothérapie d'induction : tumeur sur l'imagerie actuelle ; ganglions : tous ceux atteints avant chimiothérapie, même disparus. Ganglion TEP+ et EBUS− : inclus."],
    ["CTV de la tumeur", "GTV + 5 à 8 mm, corrigé des barrières (os, cœur)."],
    ["CTV ganglionnaire, option 1", "Toute la station ganglionnaire atteinte, avec au moins 5 à 8 mm autour du GTV."],
    ["CTV ganglionnaire, option 2", "Expansion géométrique de 5 à 8 mm, adaptée à la taille et à l'histologie, en épargnant l'œsophage."],
    ["Irradiation ganglionnaire prophylactique", "Hile et stations voisines : optionnel ; au-delà : non recommandé."],
    ["Post-opératoire (PORT)", "Régions ganglionnaires médiastinales atteintes réséquées, moignon bronchique, hile homolatéral, stations 4 et 7."],
    ["PTV", "Selon l'ICRU et les incertitudes propres au service (ITV, mid-ventilation, gating) ; ne pas retoucher le PTV à la main."]], [1]),
  sec("cbpc", "Cancer bronchique à petites cellules", ["poumon"], VD, [
    ["GTV", "Tumeur (GTVp) et ganglions atteints (GTVn), sur scanner et TEP."],
    ["CTV", "GTV (ou GTV avec gestion du mouvement) + 5 mm dans toutes les directions ; retouche manuelle au cœur et aux vertèbres recommandée, aux gros vaisseaux, œsophage et voies aériennes discutée."],
    ["Réponse complète de la tumeur", "CTVp tracé d'après l'imagerie avant traitement."],
    ["Réponse complète ganglionnaire", "Option 1 : 5 à 6 mm autour du GTVn d'avant traitement. Option 2 : toute la station atteinte avant chimiothérapie."],
    ["Ganglions prophylactiques", "Non recommandés ; zones non atteintes entre stations et tumeur (hile) : optionnel ; atteinte des stations 2 ou 3A sans TEP : sus-claviculaire homolatéral à discuter. Tous les ganglions entre deux stations atteintes non contiguës : inclus."],
    ["Post-opératoire", "Régions médiastinales et hilaires atteintes réséquées, moignon bronchique et station 7 ; stations atteintes avant chimiothérapie incluses même après réponse."],
    ["Organes à risque", "Poumons (séparés et ensemble, moins CTV ou GTV), cœur avec le péricarde, œsophage du cricoïde à la jonction, canal médullaire (PRV de la moelle)."]], [2]),
  sec("thymome", "Tumeurs thymiques", ["thymome"], VD, [
    ["CTV", "Lit tumoral à risque d'après l'imagerie avant et après chirurgie et les constatations opératoires (clips) ; le médiastin entier n'est plus la règle."],
    ["Marge GTV → CTV", "0,5 à 1,0 cm."],
    ["Marge CTV → PTV sans 4D-CT ni imagerie kV quotidienne", "1,0 à 1,5 cm."],
    ["Marge ITV → PTV avec 4D-CT sans imagerie kV quotidienne", "0,5 à 1,0 cm."],
    ["Marge ITV → PTV avec 4D-CT et imagerie kV quotidienne", "0,5 cm."]], [3], ["Préciser si l'on traite les sites atteints (tumeur ou lit) avec une marge, ou aussi des sites prophylactiques (ganglions, médiastin)."]),
  sec("meso", "Mésothéliome pleural", ["mesotheliome"], VD, [
    ["Imagerie", "GTV et CTV sur le TEP-scanner de planification, ajustés à l'ITV du 4D-CT ; IRM pour la plèvre et les T3-T4."],
    ["Après pleuro-pneumonectomie", "CTV = tout le lit pleural homolatéral, côtes comprises en dehors, marge de 0,5 à 1,0 cm à l'interface médiastin-plèvre ; jusqu'au sternum en avant (péricarde et plèvre antérieurs), jusqu'au corps vertébral en arrière, jusqu'à l'insertion diaphragmatique en bas (émergence du psoas) ; pas de ganglions médiastinaux prophylactiques."],
    ["Poumon en place (RCMI hémithoracique)", "Sur les coupes avec GTV : CTV externe et interne à 3 mm du GTV ; sur les coupes sans tumeur : CTV réduit à l'interface poumon-paroi ; sous le diaphragme : croissant couvrant la plèvre vers le sternum, le diaphragme et les piliers. PTV externe = CTV externe + 1 cm dans la paroi, ajusté à toute l'épaisseur de la paroi."],
    ["Pleurectomie complète", "Seul un CTV est tracé."],
    ["Avant chirurgie (SMART)", "CTV = réunion de la cavité thoracique entière, des stations médiastinales homolatérales, des ganglions rétropéritonéaux hauts et des orifices de trocart ; boost sur les plaques, la maladie TEP+ et les orifices ; ITV inspiration-expiration ; PTV = ITV + 5 mm."]], [4]),
 ], "sans_atlas": {}}

# ───── Sein ─────
SC = "Selon les repères palpables ou visibles ; sein controlatéral si utile"
SEIN = [
 ["Aisselle niveau 1 (CTVn_L1)", "En dedans : 5 mm au-dessus de la veine axillaire ; en dehors : jusqu'à 1 cm sous le bord de la tête humérale, 5 mm autour de la veine axillaire", "Niveau des côtes 4-5, selon les effets visibles de la biopsie du ganglion sentinelle", "Grand et petit pectoraux", "En haut, vaisseaux thoraco-dorsaux ; plus bas, ligne entre le bord antérieur du grand dorsal et les intercostaux", "Niveau 2, niveau interpectoral et paroi thoracique", "En haut, ligne entre grand pectoral et deltoïde ; plus bas, ligne entre grand pectoral et grand dorsal"],
 ["Aisselle niveau 2 (CTVn_L2)", "Extrémité crâniale de l'artère axillaire (5 mm au-dessus de la veine axillaire)", "Bord caudal du petit pectoral ; le cas échéant, sommet du curage", "Petit pectoral", "Jusqu'à 5 mm en arrière de la veine axillaire, ou côtes et intercostaux", "Bord médial du petit pectoral", "Bord latéral du petit pectoral"],
 ["Aisselle niveau 3 (CTVn_L3)", "Extrémité crâniale de l'artère sous-clavière (5 mm au-dessus de la veine sous-clavière)", "5 mm sous la veine sous-clavière ; le cas échéant, sommet du curage", "Grand pectoral", "Jusqu'à 5 mm en arrière de la veine sous-clavière, ou côtes et intercostaux", "Jonction des veines sous-clavière et jugulaire interne (puis niveau 4)", "Bord médial du petit pectoral"],
 ["Niveau 4 (CTVn_L4, sus-claviculaire)", "Extrémité crâniale de l'artère sous-clavière (5 mm au-dessus de la veine sous-clavière)", "Inclut la veine sous-clavière avec 5 mm, rejoint le bord crânial de la chaîne mammaire interne", "Sterno-cléido-mastoïdien, bord dorsal de la clavicule", "Plèvre", "Inclut la veine jugulaire sans marge ; exclut la thyroïde et l'artère carotide commune", "Inclut les scalènes antérieurs et rejoint le bord médial du niveau 3"],
 ["Chaîne mammaire interne (CTVn_IMN)", "Limite caudale du niveau 4", "Bord crânial de la 3e côte (4e dans certains cas)", "Limite ventrale de la zone vasculaire", "Plèvre", "5 mm autour de la veine mammaire interne (de l'artère en haut, jusqu'au 1er espace intercostal inclus)", "5 mm autour de la veine mammaire interne (idem)"],
 ["Ganglions interpectoraux (Rotter)", "Extrémité crâniale de l'artère axillaire (5 mm au-dessus de la veine axillaire)", "Limite caudale du niveau 2", "Grand pectoral", "Petit pectoral", "Bord médial du petit pectoral", "Bord latéral du petit pectoral"],
 ["Sein restant (CTVp_breast)", "Bord supérieur du tissu mammaire palpable ou visible ; au plus haut, bord inférieur de l'articulation sterno-claviculaire", "Dernière coupe où le sein est visible", "5 mm sous la peau", "Grand pectoral, ou côtes et intercostaux là où il n'y a pas de muscle", "En dehors des vaisseaux perforants mammaires internes ; au plus, bord du sternum", "Pli mammaire latéral ; en avant de l'artère thoracique latérale"],
 ["Paroi thoracique (CTVp_thoracic wall)", SC + " ; au plus haut, bord inférieur de l'articulation sterno-claviculaire", SC, "5 mm sous la peau", "Grand pectoral, ou côtes et intercostaux là où il n'y a pas de muscle", SC, SC + " ; en général en avant de la ligne axillaire moyenne"],
]
R["sein"] = {"sources": [
  {"n": 1, "ref": "Offersen BV et al. ESTRO consensus guideline on target volume delineation for elective radiation therapy of early stage breast cancer. Radiother Oncol 2015;114:3-10 (version 1.1 : Radiother Oncol 2016)", "doi": "10.1016/j.radonc.2014.11.030"}],
 "sections": [sec("estro", "Volumes cibles du sein, de la paroi et des aires ganglionnaires (consensus ESTRO)", ["sein", "sein_ccis"], ["Volume", "Crânial", "Caudal", "Ventral", "Dorsal", "Médial", "Latéral"], SEIN, [1],
   ["ALND = curage axillaire.", "Chaîne mammaire interne : la veine est toujours en dedans de l'artère."])], "sans_atlas": {}}

# ───── Digestif ─────
R["digestif"] = {"sources": [
  {"n": 1, "ref": "Wu AJ et al. Expert consensus contouring guidelines for intensity modulated radiation therapy in esophageal and gastroesophageal junction cancer. Int J Radiat Oncol Biol Phys 2015;92:911-920", "doi": "10.1016/j.ijrobp.2015.03.030"},
  {"n": 2, "ref": "Matzinger O et al. EORTC-ROG expert opinion: radiotherapy volume and treatment guidelines for neoadjuvant radiation of adenocarcinomas of the gastroesophageal junction and the stomach. Radiother Oncol 2009;92:164-175"},
  {"n": 3, "ref": "Brunner TB et al. ESTRO ACROP guidelines for target volume definition in pancreatic cancer. Radiother Oncol 2021;154:60-69", "doi": "10.1016/j.radonc.2020.07.052"},
  {"n": 4, "ref": "Protocole NRG Oncology / RTOG 1112 (carcinome hépatocellulaire : sorafénib ± radiothérapie stéréotaxique)"},
  {"n": 5, "ref": "Valentini V et al. International consensus guidelines on clinical target volume delineation in rectal cancer. Radiother Oncol 2016;120:195-201", "doi": "10.1016/j.radonc.2016.07.017"},
  {"n": 6, "ref": "Ng M et al. Australasian Gastrointestinal Trials Group (AGITG) contouring atlas and planning guidelines for intensity-modulated radiotherapy in anal cancer. Int J Radiat Oncol Biol Phys 2012", "doi": "10.1016/j.ijrobp.2011.12.058"}],
 "sections": [
  sec("oeso", "Œsophage et jonction œso-gastrique (RCMI)", ["oesophage"], VD, [
    ["CTV", "Lit tumoral et ganglions à risque : ganglions péri-œsophagiens, médiastinaux pour le tiers moyen et supérieur, extension sous-muqueuse ; en général GTV + 3 à 4 cm en haut et en bas, + 1,0 cm radial."],
    ["Tumeur au-dessus de la carène", "Aires sus-claviculaires des deux côtés (limites analogues au niveau IV ORL, limite crâniale au cricoïde) ; au-dessus de la crosse aortique, CTV étendu vers le sternum et les clavicules (ganglions prévasculaires, station 3 IASLC)."],
    ["Tumeur distale ou de la jonction", "CTV jusqu'à l'origine du tronc cœliaque (ganglions cœliaques, en général en regard de T12) ; entre la jonction et le tronc cœliaque : ganglions para-aortiques et du petit épiploon (petite courbure, gastrique gauche) et graisse entre petite courbure et foie (ganglions paracardiaux)."],
    ["Ganglions cœliaques : limites", "À droite, bord latéral du corps vertébral (T12) ; à gauche, 0,5 à 1 cm au-delà du bord latéral de l'aorte ; en arrière, corps vertébral ; en avant, corps du pancréas ; reins exclus."]], [1]),
  sec("estomac", "Estomac et jonction œso-gastrique, préopératoire (EORTC)", ["estomac", "oesophage"], VD, [
    ["GTV", "Tumeur et extension périgastrique (GTV tumeur) ; ganglions atteints (GTV ganglionnaire)."],
    ["CTV tumeur", "GTV tumeur + 1,5 cm."],
    ["CTV ganglionnaire", "GTV ganglionnaire + 0,5 cm."],
    ["CTV gastrique, tiers proximal", "Estomac sans pylore ni antre (au moins 5 cm du GTV)."],
    ["CTV gastrique, tiers moyen", "Estomac du cardia au pylore."],
    ["CTV gastrique, tiers distal", "Estomac sans cardia ni fundus (au moins 5 cm du GTV) ; pylore ou duodénum envahi : le long du duodénum, 3 cm au-delà de la tumeur."],
    ["CTV prophylactique", "Stations ganglionnaires selon le siège : 5 mm autour des vaisseaux correspondants."],
    ["ITV sans mesure du mouvement", "Jonction : 1 cm radial, 1,5 cm distal, 1 cm proximal. Estomac : 1,5 cm dans toutes les directions."],
    ["PTV", "ITV + 5 mm (sauf mesures propres au service)."]], [2]),
  sec("pancreas", "Pancréas", ["pancreas"], ["Situation", "CTV", "PTV"], [
    ["Néoadjuvant", "Volume tumoral (marge selon la taille et le siège) ; ganglions prophylactiques optionnels (tête : hépatiques communs, cœliaques, hépatoduodénaux, pancréatico-duodénaux antérieurs et postérieurs, mésentériques supérieurs, para-aortiques ; corps et queue : hépatiques communs, cœliaques, hépatoduodénaux, mésentériques supérieurs, para-aortiques, sous-pancréatiques, artère splénique)", "Avec 4D : ITV + 0,5 à 1 cm ; sans 4D : GTV (et CTV ganglionnaire) + 1,5 cm (antéro-postérieur, latéral) et ≥ 2 cm (crânio-caudal)"],
    ["Localement avancé ou récidive", "Volume tumoral ; pas de CTV ganglionnaire prophylactique", "Avec 4D : ITV + 0,5 à 1 cm ; sans 4D : GTV + 1,5 cm et ≥ 2 cm en crânio-caudal"],
    ["Stéréotaxie", "Volume tumoral sur toutes les phases respiratoires (ITV) ; pas de CTV ganglionnaire", "ITV + 0 à 5 mm (mesuré par le service)"],
    ["Adjuvant (consensus RTOG)", "Volume tumoral préopératoire (clips) + 5–10 mm ; tronc cœliaque (10–15 mm proximaux) + 10 (−15) mm ; artère mésentérique supérieure (25–30 mm proximaux) + 10 (−15) mm ; veine porte (du confluent à la bifurcation hilaire) + 10 (−15) mm ; anastomose pancréatico-jéjunale + 5–10 mm ; aorte du haut des autres volumes au bas de L2 : à droite 25–30 mm, à gauche 10 mm, en avant 20–25 mm, en arrière 2 mm", "—"]], [3],
   ["Organes à risque : estomac, duodénum, grêle, moelle, reins droit et gauche séparés, foie. En stéréotaxie : estomac et duodénum en entier, autres anses au moins à hauteur du PTV."]),
  sec("foie", "Carcinome hépatocellulaire, stéréotaxie (RTOG 1112)", ["foie"], VD, [
    ["CTV", "CTV = GTV, sans expansion."],
    ["PTV", "Au moins 4 mm autour du CTV dans toutes les directions ; au plus 20 mm (rarement) ; objectif ≤ 10 mm ; marges asymétriques permises selon la gestion du mouvement."]], [4]),
  sec("rectum", "Rectum : sous-régions à inclure dans le CTV selon le stade", ["rectum"], ["Stade", "À inclure"], [
    ["Toujours", "Mésorectum, espace présacré pelvien, ganglions latéraux postérieurs."],
    ["cT3", "+ ganglions latéraux antérieurs si nombreux ganglions du mésorectum (N2) ; espace présacré abdominal si ganglions atteints."],
    ["cT4 (organe pelvien antérieur)", "+ ganglions latéraux antérieurs, iliaques externes ; inguinaux si envahissement du tiers inférieur du vagin."],
    ["cT4 (sphincter anal)", "+ ganglions latéraux antérieurs, fosse ischio-rectale et complexe sphinctérien ; inguinaux si envahissement direct de la fosse ischio-rectale ou du sphincter externe."],
    ["cT3 avec ganglion hors du mésorectum", "+ ganglions latéraux antérieurs et iliaques externes."],
    ["Limite haute des ganglions latéraux", "cT3 N0 sans atteinte du fascia recti : peut être abaissée à la limite crâniale du mésorectum (bifurcation de l'artère rectale supérieure)."]], [5]),
  sec("anal", "Canal anal (RCMI)", ["canal_anal"], VD, [
    ["CTV de la tumeur", "GTV, tout le canal anal de la jonction ano-rectale à la marge, sphincters interne et externe, + 20 mm isotropes en respectant les barrières anatomiques ; tumeur de la marge ou périanale : 20 mm radial et caudal pour couvrir la peau périanale."],
    ["CTV ganglionnaire atteint", "Ganglion ou région ganglionnaire + 10 à 20 mm, en respectant les barrières."],
    ["CTV ganglionnaire prophylactique", "Marge de 7 mm autour des vaisseaux pelviens (iliaques internes en haut, iliaques externes en avant ; obturateurs 3 à 5 mm au-dessus du canal obturateur) ; présacré : 10 mm en avant du sacrum ; mésorectum : marge interne de 10 mm en avant sur les coupes avec vessie, vésicules ou utérus ; inguinaux : au moins 20 mm en avant des vaisseaux, 10 à 20 mm en dedans des vaisseaux fémoraux."],
    ["PTV", "CTV + 10 mm isotropes ; 5 à 7 mm avec imagerie quotidienne."],
    ["Intestin", "Grêle et côlon tracés de 15 mm au-dessus du PTV jusqu'à la jonction recto-sigmoïdienne."]], [6]),
 ], "sans_atlas": {}}

# ───── Gynécologie ─────
R["gyneco"] = {"sources": [
  {"n": 1, "ref": "Protocole EMBRACE II (Image guided intensity modulated external beam radiochemotherapy and MRI based adaptive brachytherapy in locally advanced cervical cancer), chapitre 9"},
  {"n": 2, "ref": "Small W Jr et al. NRG Oncology/RTOG consensus guidelines for delineation of clinical target volume for intensity-modulated pelvic radiation therapy in postoperative treatment of endometrial and cervical cancer: an update. Int J Radiat Oncol Biol Phys 2021;109:413-424", "doi": "10.1016/j.ijrobp.2020.08.061"}],
 "sections": [
  sec("embrace_t", "Col utérin en place : volumes de la tumeur (EMBRACE II)", ["col"], VD, [
    ["GTV-T", "Extension de la tumeur du col, dans et hors du col (IRM T2, examen clinique, TEP)."],
    ["CTV-T HR initial", "GTV-T et reste du col non envahi."],
    ["CTV-T LR initial", "CTV-T HR ; les deux paramètres en entier ; l'utérus en entier ; le vagin non envahi avec 20 mm sous le bord inférieur du CTV-T HR, le long de l'axe vaginal ; environ 5 mm en avant et en arrière vers vessie et rectum (parois non envahies exclues) ; paroi pelvienne, ligaments utéro-sacrés ou mésorectum envahis : 20 mm autour du CTV-T HR dans ces structures ; ganglions des paramètres possibles."],
    ["ITV-T LR (marge standard)", "CTV-T LR + 10 mm antéro-postérieur, 10 mm supéro-inférieur, 5 mm latéral ; pas de marge vers le bas au vagin distal ; ni muscle ni os ; utérus haut envahi : + 5 mm autour du corps utérin."],
    ["GTV-N et CTV-N", "Ganglion pathologique ; CTV-N = GTV-N, marge individuelle de 0 à 3 mm."],
    ["ITV45", "ITV-T LR + CTV-E (pas d'ITV pour le CTV-E)."]], [1]),
  sec("embrace_n", "Col utérin en place : aires ganglionnaires selon le risque (EMBRACE II)", ["col"], ["Groupe", "Définition", "Aires du CTV-E"], [
    ["Bas risque", "Tumeur ≤ 4 cm et stade IA / IB1 / IIA1, N0, carcinome épidermoïde, sans envahissement utérin", "« Petit bassin » : iliaques internes, iliaques externes, obturateurs, présacrés"],
    ["Risque intermédiaire", "Ni bas ni haut risque", "« Grand bassin » : petit bassin + iliaques communs (avec la bifurcation aortique) ; + inguinaux si vagin distal envahi ; + espace mésorectal si ganglions mésorectaux ou maladie localement avancée"],
    ["Haut risque", "≥ 1 ganglion pathologique iliaque commun ou plus haut, ou ≥ 3 ganglions pathologiques", "« Grand bassin + lombo-aortique » : limite haute au moins aux veines rénales (en général L2) et au moins 3 cm au-dessus du ganglion le plus haut"]], [1],
   ["Aires = vaisseaux avec au moins 7 mm de tissu périvasculaire (clips ou lymphocèles compris) ; tout ganglion pathologique inclus en entier ; envahissement important de l'utérus ou du ligament large : discuter les ovaires."]),
  sec("nrg_postop", "Après chirurgie (endomètre, col) : CTV pelvien (NRG 2021)", ["endometre", "col"], VD, [
    ["Lombo-aortique", "Si atteinte prouvée ou suspicion forte. Haut : veine rénale gauche (col) ou 1–1,5 cm au-dessus des vaisseaux rénaux gauches (endomètre) ; bas : bifurcation aortique ; avant : 3–5 mm devant la veine cave, jusqu'à 7 mm devant l'aorte ; arrière : corps vertébral ; à droite 3–5 mm autour de la veine cave, à gauche 1–2 cm autour de l'aorte jusqu'au bord interne du psoas. Tracer sur un scanner sans injection."],
    ["Iliaques communs", "De la bifurcation aortique à la bifurcation iliaque commune ; 7 mm autour des vaisseaux sans os ni muscle ; 1 cm en avant à partir du milieu des vaisseaux, au contact du psoas."],
    ["Présacrés", "Pour tous les cancers du col opérés et les cancers de l'endomètre avec envahissement du stroma cervical. De la bifurcation iliaque interne / externe au premier niveau où apparaît le piriforme ; bande de 1 à 1,5 cm devant le sacrum."],
    ["Iliaques externes", "De la bifurcation iliaque commune jusqu'à la sortie du bassin (ou l'artère circonflexe iliaque profonde) ; 7 mm autour des vaisseaux, jusqu'à 10 mm en avant."],
    ["Iliaques internes", "De la bifurcation iliaque commune jusqu'à la sortie des vaisseaux du bassin ; 7 mm autour des vaisseaux."],
    ["Obturateurs", "Bande de 15 à 18 mm en dedans de l'obturateur interne, entre vaisseaux iliaques externes et internes, jusqu'au trou obturé."],
    ["Vagin", "3,5 à 4 cm proximaux du vagin et tissu paravaginal ou paramétrial visible ; en arrière jusqu'à la paroi rectale antérieure avec le tiers antérieur du mésorectum ; en avant, paroi postérieure de la vessie ; en dehors, bord interne du CTV obturateur ou diaphragme uro-génital ; urètre exclu en général."],
    ["ITV", "Scanners vessie pleine et vide pour l'ITV, ou PTV plus large ; imagerie quotidienne recommandée."]], [2]),
 ], "sans_atlas": {
  "vagin": "Pas d'atlas publié propre au cancer du vagin dans les sources du référentiel.",
  "vulve": "Pas d'atlas de la vulve dans les sources du référentiel."}}

# ───── Urologie ─────
R["uro"] = {"sources": [
  {"n": 1, "ref": "Dal Pra A et al. ESTRO ACROP guideline on prostate bed delineation for postoperative radiotherapy in prostate cancer. Clin Transl Radiat Oncol 2023;41:100638", "doi": "10.1016/j.ctro.2023.100638"},
  {"n": 2, "ref": "eContour. Intact prostate contouring guide (d'après les protocoles RTOG 0126 et RTOG 0815)"},
  {"n": 3, "ref": "NRG Oncology. Protocole type, section radiothérapie, vessie (09/2020)"}],
 "sections": [
  sec("prostate", "Prostate en place", ["prostate"], VD, [
    ["CTV", "Prostate + 1 cm proximal des vésicules séminales (RTOG 0126 : chez tous les patients) ; la part des vésicules dépend du risque d'envahissement."],
    ["Limite inférieure", "Diaphragme uro-génital ; sinon au moins 0,7 cm au-dessus du bulbe pénien."],
    ["PTV", "CTV + 5 à 10 mm (RTOG 0126 et 0815), selon contention et imagerie quotidienne ; marge postérieure souvent réduite (exemple : 7 mm, 5 mm en arrière)."]], [2]),
  sec("lit", "Loge de prostatectomie (ESTRO-ACROP 2023)", ["prostate"], ["Limite", "Définition"], [
    ["Inférieure", "8 à 12 mm sous l'anastomose vésico-urétrale (coupe sous la dernière coupe avec de l'urine) ; si non visible, coupe juste au-dessus du bulbe pénien."],
    ["Antérieure", "En haut : 1 à 2 cm de la paroi postérieure de la vessie, ou s'arrêter au bord postérieur de la paroi vésicale ; en bas : bord postérieur du pubis, sur la moitié à deux tiers de la symphyse."],
    ["Postérieure", "Paroi antérieure du rectum ; en haut, fascia mésorectal s'il est visible ; inclure les angles antéro-latéraux du rectum et les clips."],
    ["Latérale", "Bords internes des obturateurs internes, sans s'étendre en avant vers les ganglions obturateurs ; plus bas, bords internes des obturateurs internes ou des releveurs de l'anus."],
    ["Supérieure", "Région des deux vésicules avec un « pont » de 3 à 5 mm ; sans envahissement des vésicules : base (tiers inférieur) du lit des vésicules, au niveau des canaux déférents sectionnés ; avec envahissement : tout le lit des vésicules ; inclure les clips du haut."]], [1]),
  sec("vessie", "Vessie (protocole type NRG)", ["vessie"], VD, [
    ["CTVbt", "Tumeur vésicale d'origine (résection, scanner, IRM, TEP, examen sous anesthésie, compte rendu de cystoscopie) ; marqueurs possibles."],
    ["CTVwb", "Vessie entière avec la paroi externe + CTVbt."],
    ["CTVn", "Ganglions pelviens sous la bifurcation iliaque commune : présacrés de S1 à S3 avec 1 cm devant le sacrum ; iliaques (vaisseaux depuis S1, externes jusqu'aux têtes fémorales, internes jusqu'à la sortie du bassin) + 7 mm en avant, en arrière et en dehors ; obturateurs, bande de 1 cm en dedans de l'obturateur interne jusqu'au haut de la symphyse ; sans muscle, os ni organe."],
    ["PTVbt et PTVwb", "CTV + 1 à 1,5 cm (3D ; jusqu'à 2 cm autour de la tumeur pour la vessie entière) ou 0,5 à 1 cm (RCMI)."],
    ["PTVn", "CTVn + 0,5 cm."]], [3]),
 ], "sans_atlas": {
  "seminome": "Pas d'atlas de contourage du séminome dans les sources du référentiel.",
  "penis": "Pas d'atlas publié pour le cancer du pénis."}}

# ───── Os et palliatif ─────
R["os_palliatif"] = {"sources": [
  {"n": 1, "ref": "Cox BW et al. International Spine Radiosurgery Consortium consensus guidelines for target volume definition in spinal stereotactic radiosurgery. Int J Radiat Oncol Biol Phys 2012;83:e597-e605", "doi": "10.1016/j.ijrobp.2012.03.009"},
  {"n": 2, "ref": "Redmond KJ et al. Consensus contouring guidelines for postoperative stereotactic body radiation therapy for metastatic solid tumor malignancies to the spine. Int J Radiat Oncol Biol Phys 2017"}],
 "sections": [
  sec("rachis", "Stéréotaxie du rachis : CTV osseux (ISRC)", ["sbrt_os", "metastases_osseuses"], ["Atteinte (GTV)", "CTV"], [
    ["Une partie du corps vertébral", "Corps vertébral entier."],
    ["Corps vertébral, d'un côté", "Corps vertébral entier + pédicule et apophyse transverse du même côté."],
    ["Corps vertébral en entier", "Corps vertébral entier + pédicules et apophyses transverses des deux côtés."],
    ["Corps vertébral et un pédicule", "Corps vertébral entier, pédicule, apophyse transverse et lame du même côté."],
    ["Corps vertébral et deux pédicules", "Corps vertébral entier, pédicules et apophyses transverses et lames des deux côtés."],
    ["Un pédicule", "Pédicule, apophyse transverse et lame du même côté ± corps vertébral."],
    ["Une lame", "Lame, pédicule et apophyse transverse du même côté, apophyse épineuse."],
    ["Apophyse épineuse", "Apophyse épineuse entière et les deux lames."]], [1],
   ["GTV : tumeur visible, composantes épidurale et paravertébrale comprises.", "CTV : moelle anormale suspecte et espace médullaire normal voisin ; pas d'expansion hors de l'os (épidurale, paravertébrale) en l'absence d'atteinte ; CTV circulaire autour de la moelle seulement dans des cas choisis.", "PTV : expansion uniforme ≤ 3 mm, retouchée au contact de la dure-mère, sans jamais chevaucher la moelle ou la queue de cheval."]),
  sec("rachis_po", "Stéréotaxie du rachis après chirurgie", ["sbrt_os", "metastases_osseuses"], VD, [
    ["GTV", "Reliquat sur le scanner et l'IRM postopératoires, composantes épidurale et paravertébrale comprises."],
    ["CTV", "Région opérée et tout le compartiment anatomique correspondant aux anomalies de l'IRM préopératoire ; matériel et cicatrice exclus sauf atteinte ; CTV circulaire seulement si atteinte préopératoire circulaire (ou presque, épidurale) ; jusqu'à 5 mm de plus au-delà de l'extension paravertébrale et en crânio-caudal pour une atteinte épidurale."],
    ["PTV", "CTV + jusqu'à 2,5 mm, retouché au contact des organes critiques ; la moelle à éviter peut être soustraite du PTV."]], [2]),
 ], "sans_atlas": {
  "surrenale": "Pas d'atlas publié pour la surrénale.",
  "reirradiation": "Pas d'atlas publié pour la réirradiation."}}

# ───── Sarcomes ─────
R["sarcome"] = {"sources": [
  {"n": 1, "ref": "Wang D et al. Variation in the gross tumor volume and clinical target volume for preoperative radiotherapy of primary large high-grade soft tissue sarcoma of the extremity among RTOG sarcoma radiation oncologists. Int J Radiat Oncol Biol Phys 2011;81:e525-e528", "doi": "10.1016/j.ijrobp.2011.04.038"},
  {"n": 2, "ref": "Baldini EH et al. Variability in target volume delineation for retroperitoneal sarcoma among sarcoma radiation oncologists. Int J Radiat Oncol Biol Phys 2015", "doi": "10.1016/j.ijrobp.2015.04.039"}],
 "sections": [
  sec("membres", "Sarcome des membres, radiothérapie préopératoire (RTOG)", ["sarcome_membres"], VD, [
    ["GTV", "Tumeur visible en IRM T1 avec injection ; fusion IRM et scanner recommandée."],
    ["CTV (haut grade, ≥ 5 cm)", "GTV + 3 cm en longitudinal (proximal et distal), raccourci à la fin du compartiment s'il le dépasse ; + 1,5 cm radial, y compris toute partie non limitée par un fascia intact, l'os ou la peau ; œdème péritumoral de l'IRM T2 inclus en général (jugement clinique)."]], [1],
   ["Non adapté à certaines histologies : rhabdomyosarcome, PNET extra-osseux, Ewing des tissus mous, Kaposi, angiosarcome, tumeur desmoïde, dermatofibrosarcome."]),
  sec("rp", "Sarcome du rétropéritoine, radiothérapie préopératoire", ["sarcome_retroperitoine"], VD, [
    ["CTV (ou ITV en scanner 4D)", "GTV + 1,5 cm uniforme, réduit à 0 mm à l'os, 5 mm vers le sac digestif et les cavités aériennes, 0 mm au rein et au foie (version amendée ; 2 mm dans la version initiale), 3 mm sous la peau ; s'étend en entier dans les muscles rétropéritonéaux."],
    ["CTV haut risque (complément)", "Zone à risque de marge positive : en général le long de la paroi abdominale postérieure, espace para- et prévertébral homolatéral, gros vaisseaux ou organes laissés en place ; avec l'avis du chirurgien."],
    ["Sac digestif", "Cavité péritonéale jusqu'au diaphragme, estomac et duodénum compris (atlas RTOG)."]], [2]),
 ], "sans_atlas": {"chordome": "Pas d'atlas publié pour le chordome dans les sources du référentiel."}}

# ───── Peau ─────
R["peau"] = {"sources": [
  {"n": 1, "ref": "Khan L et al. Recommendations for CTV margins in radiotherapy planning for non melanoma skin cancer. Radiother Oncol 2012;104:263-266", "doi": "10.1016/j.radonc.2012.06.013"}],
 "sections": [
  sec("marges", "Carcinomes cutanés : marge du CTV autour de la lésion visible", ["peau_carcinome"], ["Lésion", "Marge GTV → CTV"], [
    ["Basocellulaire < 2 cm", "10 mm"],
    ["Basocellulaire > 2 cm", "13 mm"],
    ["Épidermoïde < 2 cm", "11 mm"],
    ["Épidermoïde > 2 cm", "14 mm"]], [1],
   ["Marges couvrant l'extension microscopique dans au moins 95 % des cas (extension mesurée : 1 à 15 mm, moyenne 5,3 mm)."]),
 ], "sans_atlas": {
  "merkel": "Pas d'atlas publié pour le carcinome de Merkel dans les sources du référentiel.",
  "melanome": "Pas d'atlas publié pour le mélanome dans les sources du référentiel."}}

R["autres"] = {"sources": [], "sections": [], "sans_atlas": {"melanome_uveal": "Pas d'atlas publié pour le mélanome uvéal."}}

if __name__ == "__main__":
  for k, v in R.items():
    d = {"region": k, "maj": "2026-11-01", **v}
    (DOSSIER / (k + ".json")).write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    print(k, len(v["sections"]), "sections")
