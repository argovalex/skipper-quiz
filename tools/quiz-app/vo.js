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
  // Drop parenthetical Latin-word glosses like (underway), (bearing), (Kill Switch):
  // the Hebrew term precedes them and is already spoken. Require 2+ consecutive
  // Latin letters so single-letter vessel/flag labels like (K), (G), (A) are kept
  // (the bracket-strip below then exposes them for LATIN_LETTER_HE conversion).
  // Must run before that bracket-strip, which would otherwise leave the word inline.
  [/\([^)]*[A-Za-z]{2,}[^)]*\)/g, ''],
  [/=/g,              ' '],
  [/[(){}\[\]]/g,     ''],
  [/[_|]/g,           ' '],
  [/\s*[,;]\s*/g,     ', '],
  [/\.{2,}/g,         '.'],
  [/\s{2,}/g,         ' '],
  // "אופנוע-ים" / "אופנוע – ים": the dash is read aloud by the TTS. Collapse both
  // the tight hyphen and the spaced en-dash variants to a plain space.
  [/אופנוע\s*[-–]\s*ים/g, 'אופנוע ים'],
  [/קוי/g,            'קווי'],
  [/מפרשית/g,         'מִפְרָשִׂית'],
  [/התכוון/g,         'התַכְוִין'],
  [/כשתכוון/g,        'כְּשֶׁתַכְוִן'],
  [/המצפן/g,          'הַמַּצְפֵּן'],
  [/מצפן/g,           'מַצְפֵּן'],
  // Approved niqqud forms from the Hebrew-TTS niqqud dictionary, applied to the
  // words that actually occur in the quiz bank. A leading prefix (ב/ה/ל/מ/ו/ש/כ)
  // is captured and re-emitted so prefixed forms (בחרטום, למתרחצים) keep it, and
  // the Hebrew-letter lookarounds keep us from matching inside longer inflections
  // (עוגן gets niqqud, the verb עוגנת is left alone). Longer forms precede shorter.
  [/(?<![א-ת])([בהלמושכו]?)חבל(?![א-ת])/g,      '$1חֶבֶל'],
  [/(?<![א-ת])([בהלמושכו]?)חרטום(?![א-ת])/g,    '$1חַרְטוֹם'],
  [/(?<![א-ת])([בהלמושכו]?)מתרחצים(?![א-ת])/g,  '$1מִתְרַחֲצִים'],
  [/(?<![א-ת])([בהלמושכו]?)עוגן(?![א-ת])/g,     '$1עֹגֶן'],
  [/(?<![א-ת])([בהלמושכו]?)קרקעית(?![א-ת])/g,   '$1קַרְקָעִית'],
  [/(?<![א-ת])([בהלמושכו]?)מדחף(?![א-ת])/g,     '$1מַדְחֵף'],
  [/(?<![א-ת])([בהלמושכו]?)מצוף(?![א-ת])/g,      '$1מָצוֹף'],
  [/(?<![א-ת])([בהלמושכו]?)פירוטכני(?![א-ת])/g, '$1פֵּירוּטְכְנִי'],
  [/(?<![א-ת])([בהלמושכו]?)רוכב(?![א-ת])/g,      '$1רוֹכֵב'],
  [/(?<![א-ת])([בהלמושכו]?)דיג(?![א-ת])/g,       '$1דַּיג'],
  [/(?<![א-ת])([בהלמושכו]?)מדוזה(?![א-ת])/g,     '$1מֵדוּזָה'],
  [/(?<![א-ת])([בהלמושכו]?)בריזה(?![א-ת])/g,     '$1בְּרִיזָה'],
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
  [/\bIV\b/g,         'ארבע'],
  [/\bmaking way\b/gi, 'מפליג במים'],
  [/\bunderway\b/gi,  'בדרך'],
  [/\bSOG\b/g,        'מהירות על הקרקע'],
  [/\bCOG\b/g,        'כיוון על הקרקע'],
  [/\bMMSI\b/g,       'אם, אם, אס, איי'],
  [/\bDSC\b/g,        'די, אס, סי'],
  [/\bMOB\b/g,        'אם, או, בי'],
  [/מכ"ם/g,           'מכמ'],
  [/נק'/g,            'נקודה'],
  [/\bAlpha\b/gi,     'אלפא'],
  [/\bOscar\b/gi,     'אוסקר'],
  [/\bNC\b/g,         'אן, סי'],
  [/\bNM\b/g,         'מייל ימי'],
  // "מיל"/"מייל" (nautical mile) is masculine, so a preceding digit must be spelled
  // in the masculine form, and "1" is post-posed ("מייל אחד"). edge-tts otherwise
  // reads the bare digit as the feminine "שתיים", "שלוש"... Runs before the
  // מיל->מייל normalization below so the output is already the doubled-yod spelling.
  [/(?<![א-ת0-9])([0-9]{1,2})\s*מיי?ל(?![א-ת])/g, (m, d) => {
    const masc = { 1:'אחד', 2:'שני', 3:'שלושה', 4:'ארבעה', 5:'חמישה',
      6:'שישה', 7:'שבעה', 8:'שמונה', 9:'תשעה', 10:'עשרה' };
    const n = Number(d);
    if (n === 1) return 'מייל אחד';
    return masc[n] ? masc[n] + ' מייל' : d + ' מייל';
  }],
  [/(?<![א-ת])מיל(?![א-ת])/g,  'מייל'],
  [/\bm\/s\b/g,       'מטר לשנייה'],
  [/\bkm\/h\b/gi,     'קילומטר לשעה'],
  [/°/g,              ' מעלות '],
  [/\bknots?\b/gi,    'קשרים'],
  [/"/g,              ''],
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
// index.html buildVoiceover.
const ANSWER_PROMPT_NUMS = new Set([1053, 1054]);

// heNum spells a number in Hebrew words. It USED to wrap the question number in
// buildVoiceover because edge-tts once misread the digit string ("1002" ->
// "10020"). Alex's decision (2026-08-19): the narration says the number in
// DIGITS ("שאלה מספר 1024"), not words — verify one render if edge-tts ever
// regresses. heNum is kept exported for any caller that still wants words.
function heNum(n){
  n=Number(n);
  if(!Number.isInteger(n)||n<1||n>9999) return String(n);
  const o=['','אחד','שניים','שלושה','ארבעה','חמישה','שישה','שבעה','שמונה','תשעה'];
  const teen=['עשרה','אחד עשר','שנים עשר','שלושה עשר','ארבעה עשר','חמישה עשר','שישה עשר','שבעה עשר','שמונה עשר','תשעה עשר'];
  const t=['','','עשרים','שלושים','ארבעים','חמישים','שישים','שבעים','שמונים','תשעים'];
  const hd=['','מאה','מאתיים','שלוש מאות','ארבע מאות','חמש מאות','שש מאות','שבע מאות','שמונה מאות','תשע מאות'];
  const thc=['','','','שלושת','ארבעת','חמשת','ששת','שבעת','שמונת','תשעת'];
  const p=[]; const th=Math.floor(n/1000); n%=1000;
  if(th===1)p.push('אלף'); else if(th===2)p.push('אלפיים'); else if(th>=3)p.push(thc[th]+' אלפים');
  const h=Math.floor(n/100); n%=100; if(h>0)p.push(hd[h]);
  if(n>=10&&n<20){p.push(teen[n-10]);} else {const tt=Math.floor(n/10),oo=n%10; if(tt>0)p.push(t[tt]); if(oo>0)p.push(o[oo]);}
  if(p.length>1)p[p.length-1]='ו'+p[p.length-1];
  return p.join(' ');
}

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

// Dual-use module. In Node (update-question.js, render-with-html.js) it exports
// via CommonJS. In the browser editor (index.html) it is loaded with <script src>;
// the top-level const/function declarations above then live in the shared global
// scope where index.html's inline scripts resolve buildVoiceover/applyVoFixes by
// name. Guard the export so the browser doesn't throw on `module` being undefined.
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { buildVoiceover, applyVoFixes, heNum, VO_FIXES, LATIN_LETTER_HE, ANSWER_PROMPT_NUMS };
}
