// Espace « Outils cliniques » (lot RT.13 à RT.17, 31/10/2026, sous Radiothérapie) : localisations de la stadification, calculateurs et leurs sources.
// Stadification TNM (RT.14, décidé le 31/10/2026) : seule la structure est fournie (localisations, sous-localisations, onglets, calcul du stade) ;
// les tableaux de l'AJCC ne sont pas recopiés (protégés) : ils sont remplis par le médecin depuis son manuel, dans le cabinet
// (bibliotheques/tnm_<sous-localisation>), avec la source et l'édition. Échelles de toxicité (RT.15) : fichier officiel du NCI importé par le médecin.
export const AVERT_OUTILS = "Contenus indicatifs, à vérifier avant toute prescription ; la prescription reste sous la responsabilité du médecin.";

// Localisations et sous-localisations (noms seulement, comme les chapitres du manuel)
export const TNM_LOCS = [
  { id: "orl", nom: "Tête et cou", sous: [["cavite-buccale", "Lèvre et cavité buccale"], ["oropharynx-p16p", "Oropharynx p16+ (HPV)"], ["oropharynx-p16n", "Oropharynx p16−"], ["nasopharynx", "Nasopharynx"], ["hypopharynx", "Hypopharynx"],
    ["larynx", "Larynx"], ["sinus", "Cavité nasale et sinus"], ["salivaires", "Glandes salivaires"], ["thyroide", "Thyroïde"], ["inconnu-orl", "Adénopathie cervicale sans primitif"]] },
  { id: "thorax", nom: "Thorax", sous: [["poumon", "Poumon"], ["mesotheliome", "Mésothéliome pleural"], ["thymus", "Thymus"]] },
  { id: "digestif", nom: "Digestif", sous: [["oesophage", "Œsophage et jonction œso-gastrique"], ["estomac", "Estomac"], ["pancreas", "Pancréas exocrine"], ["foie", "Foie"], ["voies-biliaires", "Voies biliaires"],
    ["colon-rectum", "Côlon et rectum"], ["anus", "Canal anal"]] },
  { id: "sein", nom: "Sein", sous: [["sein", "Sein"]] },
  { id: "gyneco", nom: "Gynécologie", sous: [["col", "Col de l'utérus"], ["endometre", "Corps de l'utérus"], ["ovaire", "Ovaire et trompe"], ["vulve", "Vulve"], ["vagin", "Vagin"]] },
  { id: "uro", nom: "Urologie", sous: [["prostate", "Prostate"], ["vessie", "Vessie"], ["rein", "Rein"], ["testicule", "Testicule"], ["penis", "Pénis"]] },
  { id: "peau", nom: "Peau", sous: [["melanome", "Mélanome cutané"], ["merkel", "Carcinome de Merkel"], ["epidermoide-peau", "Carcinome épidermoïde cutané"]] },
  { id: "sarcome", nom: "Tissus mous et os", sous: [["sarcome-membres", "Sarcome des tissus mous (tronc et membres)"], ["os", "Os"]] },
];
export const sousTnm = (id) => { for (const l of TNM_LOCS) { const s = l.sous.find((x) => x[0] === id); if (s) return { id: s[0], nom: s[1], loc: l }; } return null; };
// Fiche vide d'une sous-localisation : catégories T, N, M (clinique et pathologique), groupes de stades, tableaux annexes
export const tnmVide = () => ({ source: "AJCC Cancer Staging Manual", edition: "", c: { t: [], n: [], m: [], stades: [] }, p: { t: [], n: [], m: [], stades: [] }, annexes: [], note: "" });

// Échelles de toxicité CTCAE (NCI, domaine public) : termes suivis en « Tardive » par défaut (noms anglais du fichier du NCI), modifiables par le cabinet
export const CTCAE_TARDIFS0 = ["Fibrosis deep connective tissue", "Superficial soft tissue fibrosis", "Skin hyperpigmentation", "Telangiectasia", "Lymphedema", "Dry mouth", "Osteonecrosis of jaw", "Trismus",
  "Hypothyroidism", "Pulmonary fibrosis", "Proctitis", "Cystitis noninfective", "Urinary frequency", "Urinary incontinence", "Erectile dysfunction", "Vaginal stricture", "Myelitis",
  "Cognitive disturbance", "Osteonecrosis", "Osteoporosis", "Cataract", "Hearing impaired", "Small intestinal obstruction", "Bladder spasm"];
// RT.15 (31/10/2026) : CTCAE v6.0 (NCI, domaine public) fourni avec Onco360 : public/donnees-outils/ctcae-v6.json, lu dans le PDF officiel du NCI
// (outils/ctcae-pdf.py) ; un fichier importé par le cabinet le remplace
export const CTCAE_V6 = { fichier: "donnees-outils/ctcae-v6.json", version: "6.0 (MedDRA 28.0, publiée le 22/07/2025)" };
export const CTCAE_SITE = "https://dctd.cancer.gov/research/ctep-trials/for-sites/adverse-events";

// Calculateurs (RT.16, RT.17) : [id, nom, groupe, source] ; liens externes (outils protégés) : lien au lieu du calcul
export const GROUPES_CALC = [["rt", "Radiothérapie"], ["prostate", "Prostate"], ["sein", "Sein"], ["hemato", "Hématologie"], ["neuro", "Neuro-oncologie"], ["rein", "Rein et doses"], ["general", "Général"]];
export const CALCS = [
  ["bed", "BED / EQD2", "rt", "Modèle linéaire-quadratique (Fowler, Br J Radiol 1989 ; Withers 1983)"],
  ["conversion", "Conversion de dose", "rt", "Modèle linéaire-quadratique : D2 = D × (d + α/β) / (d2 + α/β) (Withers, Int J Radiat Oncol Biol Phys 1983)"],
  ["esperance", "Espérance de vie", "general", "Table du cabinet (à remplir depuis une table de mortalité : OMS, HCP Maroc…)"],
  ["stephenson", "Radiothérapie de rattrapage de la prostate (Stephenson)", "prostate", "Stephenson, J Clin Oncol 2007 ; nomogramme du MSKCC (lien externe, outil protégé)", "https://mskcc.org/nomograms/prostate/salvage-radiation-therapy"],
  ["tdpsa", "Temps de doublement du PSA", "prostate", "ln 2 / pente de ln(PSA) en fonction du temps (Pound, JAMA 1999)"],
  ["damico", "Groupes de risque de D'Amico", "prostate", "D'Amico, JAMA 1998;280:969-74"],
  ["roach", "Formules de Roach", "prostate", "Roach, Int J Radiat Oncol Biol Phys 1994 ; Diaz, Int J Radiat Oncol Biol Phys 1994"],
  ["partin", "Tables de Partin", "prostate", "Johns Hopkins Brady Urology Institute (lien externe, outil protégé)", "https://www.hopkinsmedicine.org/brady-urology-institute/conditions-and-treatments/prostate-cancer/risk-assessment-tools/partin-tables"],
  ["mskcc", "Nomogrammes du MSKCC (prostate)", "prostate", "Memorial Sloan Kettering Cancer Center (lien externe, outils protégés)", "https://mskcc.org/nomograms/prostate"],
  ["nsabp", "Récidive locorégionale du sein après chimiothérapie néoadjuvante (NSABP B-18 / B-27)", "sein", "Mamounas, J Clin Oncol 2012;30:3960-6 (nomogrammes de l'article : lien externe)", "https://doi.org/10.1200/JCO.2011.40.8369"],
  ["apbi", "Irradiation partielle du sein (critères ASTRO)", "sein", "Correa, Pract Radiat Oncol 2017;7:73-79 (consensus ASTRO 2016)"],
  ["vnpi", "Index pronostique de Van Nuys (CCIS)", "sein", "Silverstein, Am J Surg 2003;186:337-43"],
  ["rpa", "Classes RPA du glioblastome", "neuro", "Curran, J Natl Cancer Inst 1993;85:704-10 (RTOG)"],
  ["hodgkin", "Maladie de Hodgkin : facteurs de risque (EORTC, GHSG)", "hemato", "EORTC-LYSA ; German Hodgkin Study Group (stades I–II)"],
  ["ipi", "IPI (lymphome diffus à grandes cellules B)", "hemato", "Shipp, N Engl J Med 1993;329:987-94"],
  ["flipi", "FLIPI (lymphome folliculaire)", "hemato", "Solal-Céligny, Blood 2004;104:1258-65"],
  ["childpugh", "Score de Child-Pugh", "general", "Pugh, Br J Surg 1973;60:646-9"],
  ["imc", "Indice de masse corporelle", "general", "OMS (classes de corpulence)"],
  ["ps", "Statut de performance (OMS / ECOG, Karnofsky)", "general", "Oken, Am J Clin Oncol 1982 (ECOG) ; Karnofsky 1949"],
  ["mdrd", "DFG : MDRD", "rein", "Levey, Ann Intern Med 2006 (MDRD à 4 variables, créatinine IDMS)"],
  ["cockcroft", "DFG : Cockcroft-Gault", "rein", "Cockcroft et Gault, Nephron 1976;16:31-41"],
  ["schwartz", "DFG de l'enfant : Schwartz", "rein", "Schwartz, J Am Soc Nephrol 2009;20:629-37 (formule « au lit du malade »)"],
  ["surface", "Surface corporelle (Du Bois, Mosteller)", "rein", "Du Bois, Arch Intern Med 1916 ; Mosteller, N Engl J Med 1987"],
  ["carbo", "Carboplatine : Calvert et Chatelut", "rein", "Calvert, J Clin Oncol 1989 ; Chatelut, J Natl Cancer Inst 1995"],
  ["calcemie", "Calcémie corrigée par l'albumine", "general", "Payne, Br Med J 1973"],
  ["opioides", "Équivalences des opioïdes", "general", "Référentiels AFSOS « Douleur et cancer »"],
];
// Statut de performance : OMS / ECOG et Karnofsky (équivalences habituelles)
export const PS = [
  [0, "Activité normale, sans restriction", "100 – 90"], [1, "Restreint pour les efforts importants, ambulatoire, travail léger possible", "80 – 70"],
  [2, "Ambulatoire, capable de s'occuper de lui-même, incapable de travailler ; debout plus de 50 % de la journée", "60 – 50"],
  [3, "Capable de soins limités ; alité ou au fauteuil plus de 50 % de la journée", "40 – 30"], [4, "Totalement dépendant, alité ou au fauteuil en permanence", "20 – 10"], [5, "Décès", "0"],
];
export const KARNOFSKY = [[100, "Normal, aucun signe de maladie"], [90, "Activité normale, signes mineurs"], [80, "Activité normale avec effort, quelques signes"], [70, "S'occupe de lui-même, incapable d'une activité normale ou de travailler"],
  [60, "A besoin d'une aide occasionnelle, assure la plupart de ses besoins"], [50, "A besoin d'une aide importante et de soins médicaux fréquents"], [40, "Handicapé, a besoin d'aide et de soins particuliers"],
  [30, "Sévèrement handicapé, hospitalisation indiquée"], [20, "Très malade, hospitalisation et traitement de soutien nécessaires"], [10, "Moribond"], [0, "Décès"]];
