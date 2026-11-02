// Onco360 – code CIM-10 proposé sur la feuille de soins d'après la localisation du dossier (UX13, P18, 02/11/2026). Table préparée par Claude
// d'après la CIM-10 publiée par l'OMS (catégories à 3 caractères, un code plus précis seulement quand la localisation le dit), À RELIRE par
// Dr Bentahila ; le code reste modifiable dans la fenêtre. Localisation sans code sûr (GIST, tumeur neuroendocrine, ORL sans précision,
// pathologies bénignes…) : rien n'est proposé. Clés = noms de la liste de départ DIAG (donnees/listes.js) ; un nom du cabinet absent de la
// table est cherché par mots (MOTS), sinon rien.
export const CIM10_LOC = {
  "Cancer du sein RH+ / HER2−": "C50", "Cancer du sein HER2+": "C50", "Cancer du sein triple négatif": "C50", "Cancer du sein": "C50",
  "Carcinome canalaire in situ du sein": "D05", "Cancer du sein chez l’homme": "C50",
  "Cancer de l’œsophage": "C15", "Cancer de la jonction œso-gastrique": "C16.0", "Cancer de l’estomac": "C16", "Cancer du côlon": "C18",
  "Cancer du rectum": "C20", "Cancer du canal anal": "C21", "Cancer de l’intestin grêle": "C17", "Cancer de l’appendice": "C18.1",
  "Cancer du pancréas": "C25", "Cancer de l’ampoule de Vater": "C24.1", "Carcinome hépatocellulaire": "C22.0", "Cancer des voies biliaires": "C24",
  "Cancer de la vésicule biliaire": "C23", "Carcinose péritonéale / pseudomyxome": "C48",
  "Cancer du poumon non à petites cellules – adénocarcinome": "C34", "Cancer du poumon non à petites cellules – épidermoïde": "C34",
  "Cancer du poumon": "C34", "Cancer du poumon à petites cellules": "C34", "Tumeur carcinoïde bronchique": "C34", "Mésothéliome": "C45",
  "Thymome / carcinome thymique": "C37",
  "Cancer de la cavité buccale": "C06", "Cancer de la langue": "C02", "Cancer de la lèvre": "C00", "Cancer de l’oropharynx": "C10",
  "Cancer de l’hypopharynx": "C13", "Cancer du larynx": "C32", "Cancer du nasopharynx": "C11", "Cancer des fosses nasales et des sinus": "C30",
  "Cancer des glandes salivaires": "C08", "Adénopathie cervicale sans primitif": "C77.0",
  "Cancer de la thyroïde": "C73", "Cancer médullaire de la thyroïde": "C73", "Cancer anaplasique de la thyroïde": "C73", "Corticosurrénalome": "C74.0",
  "Phéochromocytome / paragangliome": "C74.1",
  "Cancer du col de l’utérus": "C53", "Cancer de l’endomètre": "C54.1", "Sarcome utérin": "C54", "Cancer de l’ovaire": "C56", "Cancer de la vulve": "C51",
  "Cancer du vagin": "C52", "Tumeur trophoblastique gestationnelle": "C58",
  "Cancer de la prostate": "C61", "Cancer de la vessie / voies urinaires": "C67", "Cancer des voies excrétrices supérieures": "C65", "Cancer du rein": "C64",
  "Tumeur germinale du testicule": "C62", "Cancer du pénis": "C60", "Cancer de l’urètre": "C68.0",
  "Mélanome": "C43", "Mélanome de l’uvée": "C69.4", "Carcinome basocellulaire": "C44", "Carcinome épidermoïde cutané": "C44", "Carcinome de Merkel": "C44",
  "Lymphome cutané": "C84", "Sarcome des tissus mous": "C49", "Sarcome": "C49", "Ostéosarcome": "C41", "Sarcome d’Ewing": "C41", "Chondrosarcome": "C41",
  "Sarcome de Kaposi": "C46", "Tumeur desmoïde": "D48.1",
  "Tumeur cérébrale (gliome)": "C71", "Glioblastome": "C71", "Gliome de bas grade": "C71", "Méningiome": "D32", "Médulloblastome": "C71.6",
  "Lymphome cérébral primitif": "C83.3", "Métastases cérébrales": "C79.3", "Tumeur de la moelle épinière": "C72.0",
  "Lymphome": "C85", "Lymphome de Hodgkin": "C81", "Lymphome non hodgkinien": "C85", "Myélome": "C90.0", "Plasmocytome solitaire": "C90.3", "Leucémie": "C95",
  "Rétinoblastome": "C69.2", "Néphroblastome": "C64", "Neuroblastome": "C74.9",
  "Cancer de primitif inconnu": "C80", "Métastases osseuses": "C79.5", "Métastases hépatiques": "C78.7",
};
// Nom du cabinet hors de la table : premiers mots reconnus (ordre = du plus précis au plus large)
const MOTS = [[/in situ.*sein|sein.*in situ/, "D05"], [/sein/, "C50"], [/oesophag/, "C15"], [/estomac|gastrique/, "C16"], [/colon\b|colique|colorectal/, "C18"], [/rectum|rectal/, "C20"],
  [/canal anal/, "C21"], [/pancrea/, "C25"], [/hepatocell/, "C22.0"], [/poumon|bronch/, "C34"], [/larynx/, "C32"], [/nasopharynx|cavum/, "C11"], [/oropharynx/, "C10"],
  [/hypopharynx/, "C13"], [/thyroide/, "C73"], [/col (de l.)?uterus|col uterin/, "C53"], [/endometre/, "C54.1"], [/ovaire/, "C56"], [/prostate/, "C61"],
  [/vessie/, "C67"], [/\brein\b|renal/, "C64"], [/testicule/, "C62"], [/melanome/, "C43"], [/glioblastome|gliome/, "C71"], [/hodgkin/, "C81"], [/myelome/, "C90.0"]];
const norm = (s) => String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[’']/g, "'").replace(/œ/g, "oe").replace(/\s+/g, " ").trim();
const TABLE = new Map(Object.entries(CIM10_LOC).map(([k, v]) => [norm(k), v]));
export function cimDe(loc) {
  const n = norm(loc); if (!n) return "";
  if (TABLE.has(n)) return TABLE.get(n);
  if (/benign|^metastases?\b/.test(n)) return ""; // « Métastases … » sans primitif, pathologie bénigne : rien
  const m = MOTS.find(([re]) => re.test(n)); return m ? m[1] : "";
}
