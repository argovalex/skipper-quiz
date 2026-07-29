// Verbatim port of index.html buildVoiceover (the editor's VO builder).
// Keep in sync with index.html lines ~383-467 (LATIN_LETTER_HE, VO_FIXES,
// applyVoFixes, buildVoiceover). Used by update-question.js to render the exact
// same VO the editor would, headlessly. Validated byte-identical against Q1001.
const LATIN_LETTER_HE = {
  A: 'איי', B: 'בי',  C: 'סי',   D: 'די',  E: 'אי',   F: 'אף',
  G: "ג'י", H: "אייץ'", I: 'איי', J: "ג'יי", K: 'קיי', L: 'אל',
  M: 'אם',  N: 'אן',  O: 'או',   P: 'פי',  Q: 'קיו',  R: 'אר',
  S: 'אס',  T: 'טי',  U: 'יו',   V: 'וי',  W: 'דאבליו', X: 'אקס',
  Y: 'וואי', Z: 'זי',
};

const VO_FIXES = [
  [/=/g,              ' '],
  [/[(){}\[\]]/g,     ''],
  [/[_|]/g,           ' '],
  [/\s*[,;]\s*/g,     ', '],
  [/\.{2,}/g,         '.'],
  [/\s{2,}/g,         ' '],
  [/קוי/g,            'קווי'],
  [/מפרשית/g,         'מִפְרָשִׂית'],
  [/התכוון/g,         'התַכְוִין'],
  [/כשתכוון/g,        'כְּשֶׁתַכְוִן'],
  [/המצפן/g,          'הַמַּצְפֵּן'],
  [/מצפן/g,           'מַצְפֵּן'],
  [/\bVHF\b/g,        'וי, אייץ\', אף'],
  [/\bUTC\b/g,        'יו, טי, סי'],
  [/\bGPS\b/g,        'ג\'י, פי, אס'],
  [/\bAIS\b/g,        'איי, איי, אס'],
  [/\bEPIRB\b/g,      'איי, פירב'],
  [/מכ"מ/g,           'מכמ'],
  [/ע"י/g,            'על ידי'],
  [/ע"פ/g,            'על פי'],
  [/סה"כ/g,           'סך הכל'],
  [/ק"מ/g,            'קילומטר'],
  [/ס"מ/g,            'סנטימטר'],
  [/(\d+)\s*מ'/g,     '$1 מטר'],
  [/\bNUC\b/g,        'אן, יו, סי'],
  [/\bSOS\b/g,        'אס, או, אס'],
  [/\bCOLREGS\b/gi,   'קולרגס'],
  [/\bAnnex\s+IV\b/g, 'נספח ארבע'],
  [/\bSOG\b/g,        'מהירות על הקרקע'],
  [/\bCOG\b/g,        'כיוון על הקרקע'],
  [/\bMMSI\b/g,       'אם, אם, אס, איי'],
  [/\bDSC\b/g,        'די, אס, סי'],
  [/\bMOB\b/g,        'אם, או, בי'],
  [/\bNM\b/g,         'מייל ימי'],
  [/\bm\/s\b/g,       'מטר לשנייה'],
  [/\bkm\/h\b/gi,     'קילומטר לשעה'],
  [/°/g,              ' מעלות '],
  [/\bknots?\b/gi,    'קשרים'],
  [/(?<=[֐-׿]-)([A-Za-z])(?![A-Za-z-])/g,
                      (m, l) => LATIN_LETTER_HE[l.toUpperCase()] || m],
  [/(?<![A-Za-z-])([A-Za-z])(?![A-Za-z-])/g,
                      (m, l) => LATIN_LETTER_HE[l.toUpperCase()] || m],
  [/\b(\d+)%/g,       '$1 אחוז'],
  [/(\d+)\.(\d+)/g,   '$1 נקודה $2'],
  [/\//g,             ' או '],
];

function applyVoFixes(text) {
  let t = text;
  for (const [pat, rep] of VO_FIXES) t = t.replace(pat, rep);
  return t.replace(/\s{2,}/g, ' ').trim();
}

// Questions whose pre-pause narration gets an explicit "מה התשובה הנכונה?" cue
// right before the pause, so the viewer has a clear prompt to answer (and the
// silencedetect pass gets a clean gap to lock the pause onto). Keep in sync with
// index.html / queue.html buildVoiceover.
const ANSWER_PROMPT_NUMS = new Set([1053, 1054]);

function buildVoiceover(q) {
  const idx = { 'א': 0, 'ב': 1, 'ג': 2, 'ד': 3 }[(q.answer || 'א').trim()] ?? 0;
  const ans = ((q.options || [])[idx] || '').replace(/^[אבגד]\.\s*/, '');
  const letter = (q.answer || 'א').trim();
  let q1 = applyVoFixes(`שאלה מספר ${q.num}... ${q.q_he}.`);
  if (ANSWER_PROMPT_NUMS.has(Number(q.num))) q1 += ' מה התשובה הנכונה?';
  let q2 = applyVoFixes(`התשובה הנכונה היא ${letter}: ${ans}.`);
  if (q.explanation) q2 += ` ... ${applyVoFixes(q.explanation)}`;
  return q1 + ' [[PAUSE]] ' + q2;
}

module.exports = { buildVoiceover, applyVoFixes };
