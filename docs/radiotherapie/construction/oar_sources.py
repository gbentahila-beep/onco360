# Sources des définitions des organes à risque (phase RTX, lot 4h, 01/11/2026). Chaque organe renvoie à la délinéation RecoRad (Noël 2021) et aux
# atlas que cet article cite pour lui (paragraphe « Atlas reference(s) »), plus Lapeyre chapitre VI pour l'ORL. Les références et DOI sont recopiés
# de la bibliographie de Noël 2021. Un organe sans atlas publié (structure propre à un schéma) n'a pas de source : la page l'écrit. Lu par oar.py.

SOURCES = [
  {"n": 1, "ref": "Noël G, Le Fèvre C, Antoni D. Délinéation des organes à risque (RecoRad). Cancer Radiother 2021", "doi": "10.1016/j.canrad.2021.08.001"},
  {"n": 2, "ref": "Eekers DB et al. The EPTN consensus-based atlas for CT- and MR-based contouring in neuro-oncology. Radiother Oncol 2018;128:37–43", "doi": "10.1016/j.radonc.2017.12.013"},
  {"n": 3, "ref": "Scoccianti S et al. Organs at risk in the brain and their dose constraints in adults and in children. Radiother Oncol 2015", "doi": "10.1016/j.radonc.2015.01.016"},
  {"n": 4, "ref": "Gondi V et al. Hippocampal sparing whole brain radiotherapy: a « how-to » technique. Int J Radiat Oncol Biol Phys 2010;78:1244–52", "doi": "10.1016/j.ijrobp.2010.01.039"},
  {"n": 5, "ref": "Pacholke HD et al. Contouring the middle and inner ear on radiotherapy planning scans. Am J Clin Oncol 2005;28:143–7"},
  {"n": 6, "ref": "Sun Y et al. Recommendation for a contouring method and atlas of organs at risk in nasopharyngeal carcinoma. Radiother Oncol 2014;110:390–7", "doi": "10.1016/j.radonc.2013.10.035"},
  {"n": 7, "ref": "Brouwer CL et al. CT-based delineation of organs at risk in the head and neck region: DAHANCA, EORTC, GORTEC, HKNPCSG, NCIC CTG, NCRI, NRG Oncology and TROG consensus guidelines. Radiother Oncol 2015", "doi": "10.1016/j.radonc.2015.07.041"},
  {"n": 8, "ref": "Christianen ME et al. Delineation of organs at risk involved in swallowing for radiotherapy treatment planning. Radiother Oncol 2011;101:394–402", "doi": "10.1016/j.radonc.2011.05.015"},
  {"n": 9, "ref": "van de Water TA et al. Delineation guidelines for organs at risk involved in radiation-induced salivary dysfunction and xerostomia. Radiother Oncol 2009;93:545–52", "doi": "10.1016/j.radonc.2009.09.008"},
  {"n": 10, "ref": "Rouers M et al. Maxillary and mandible contouring in patients with a head and neck area irradiation. Pract Radiat Oncol 2016;6:e61–72", "doi": "10.1016/j.prro.2015.10.003"},
  {"n": 11, "ref": "Biau J et al. Practical clinical guidelines for contouring the trigeminal nerve (V) and its branches in head and neck cancers. Radiother Oncol 2019;131:192–201", "doi": "10.1016/j.radonc.2018.08.020"},
  {"n": 12, "ref": "Lapeyre M. Délinéation des volumes cibles, cancers des VADS, chapitre VI : organes à risque. Centre Jean Perrin, juin 2019"},
  {"n": 13, "ref": "Kong FM et al. Consideration of dose limits for organs at risk of thoracic radiotherapy: atlas for lung, proximal bronchial tree, esophagus, spinal cord, ribs, and brachial plexus. Int J Radiat Oncol Biol Phys 2011", "doi": "10.1016/j.ijrobp.2010.07.1977"},
  {"n": 14, "ref": "Feng M et al. Development and validation of a heart atlas to study cardiac exposure to radiation following treatment for breast cancer. Int J Radiat Oncol Biol Phys 2011", "doi": "10.1016/j.ijrobp.2009.10.058"},
  {"n": 15, "ref": "Hall WH et al. Development and validation of a standardized method for contouring the brachial plexus. Int J Radiat Oncol Biol Phys 2008", "doi": "10.1016/j.ijrobp.2008.03.004"},
  {"n": 16, "ref": "Jabbour SK et al. Upper abdominal normal organ contouring guidelines and atlas: a Radiation Therapy Oncology Group consensus. Pract Radiat Oncol 2014;4:82–9", "doi": "10.1016/j.prro.2013.06.004"},
  {"n": 17, "ref": "Lukovic J et al. MRI-based upper abdominal organs-at-risk atlas for radiation oncology. Int J Radiat Oncol Biol Phys 2020;106:743–53", "doi": "10.1016/j.ijrobp.2019.12.003"},
  {"n": 18, "ref": "Gay HA et al. Pelvic normal tissue contouring guidelines for radiation therapy: a Radiation Therapy Oncology Group consensus panel atlas. Int J Radiat Oncol Biol Phys 2012", "doi": "10.1016/j.ijrobp.2012.01.023"},
  {"n": 19, "ref": "Yi SK et al. Development of a standardized method for contouring the lumbosacral plexus. Int J Radiat Oncol Biol Phys 2012", "doi": "10.1016/j.ijrobp.2011.11.074"},
  {"n": 20, "ref": "EMBRACE II study protocol v1.0 (curiethérapie guidée par l'image du col utérin)"},
]

# Groupes d'organes → sources (numéros ci-dessus), d'après le paragraphe de Noël 2021 consacré à l'organe (ses « Atlas reference(s) »)
_G = [
  ((1, 2), "encephale encephale-sain cervelet lobe-frontal"),
  ((1, 2, 12), "fosse-posterieure cristallin-d cristallin-g"),
  ((1, 2, 3), "cornee-d cornee-g"),
  ((1, 2, 6), "tronc-cerebral"),
  ((1, 6), "lobe-temporal-d lobe-temporal-g"),
  ((1, 2, 4), "hippocampe-d hippocampe-g hippocampes zone-evitement-hippocampique"),
  ((1, 2, 3, 7), "chiasma nerf-optique-d nerf-optique-g glande-lacrymale-d glande-lacrymale-g"),
  ((1, 2, 3, 7, 12), "retine-d retine-g"),
  ((1, 7), "oeil-d oeil-g hypothalamus moelle canal-medullaire"),
  ((1, 2, 3, 5, 6, 7, 12), "cochlee-d cochlee-g"),
  ((1, 3, 5, 6, 7), "oreille-interne-d oreille-interne-g"),
  ((1, 7, 12), "hypophyse atm-d atm-g"),
  ((1, 7, 11), "nerfs-craniens"),
  ((1, 2, 6, 7), "cuir-chevelu peau"),
  ((1, 9, 12), "parotide-d parotide-g glande-sous-max-d glande-sous-max-g"),
  ((1, 7, 8), "cavite-orale"),
  ((1, 7, 8, 9), "levres"),
  ((1, 7, 10, 12), "mandibule"),
  ((1, 6, 7), "thyroide carotide-d carotide-g"),
  ((1, 6, 7, 8, 12), "constricteurs constricteur-sup constricteur-moyen constricteur-inf pharynx larynx larynx-supraglottique larynx-glottique oesophage-cervical"),
  ((1, 13), "poumons poumon-d poumon-g poumon-homolateral poumon-controlateral trachee arbre-bronchique paroi-thoracique cotes"),
  ((1, 7, 13), "oesophage"),
  ((1, 13, 14), "coeur iva ventricule-gauche valves coronaires coronaire-droite circonflexe gros-vaisseaux artere-pulmonaire"),
  ((1, 6, 7, 8, 13, 15), "plexus-brachial-d plexus-brachial-g"),
  ((1, 16, 17, 18), "grele colon"),
  ((1, 16, 17), "foie duodenum reins rein-d rein-g hile-renal"),
  ((1, 16), "voie-biliaire pancreas rate estomac"),
  ((1, 18), "vessie rectum sigmoide canal-anal tete-femorale-d tete-femorale-g bulbe uterus ovaire-d ovaire-g"),
  ((1, 19), "plexus-sacre"),
  ((1,), "testicule-controlateral sein-controlateral sein-homolateral oge segment-anterieur vagin vulve os-pelviens aile-iliaque-d aile-iliaque-g moelle-osseuse sac-dural queue-cheval racines-nerveuses"),
  ((20,), "point-rv help-ctvhr10"),
]
SRC = {}
for nums, ids in _G:
  for i in ids.split():
    assert "oar-" + i not in SRC, i
    SRC["oar-" + i] = list(nums)
