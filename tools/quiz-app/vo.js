// Shared VO builder for the editor (index.html loads this via <script src>) and
// the headless renderers (update-question.js, render-with-html.js require it).
// buildVoiceover now auto-vocalises its output: flag letters via LATIN_LETTER_HE
// and content words via applyLexiconText (Alex's lexicon), so every render is
// niqqud'd with no manual pass. LATIN_LETTER_HE / VO_FIXES / applyVoFixes are the
// canonical copy — index.html has no separate copy of them.
// Flag/vessel letters. The niqqud'd forms come from Alex's lexicon
// (references/niqqud-lexicon.md) and are baked in HERE, at the Latin->Hebrew
// conversion, because that only fires for real flag letters (a Latin source
// char) — never for the identical-looking Hebrew words (אם=if, אי=cannot,
// אף=none, די=enough, פי=mouth). That sidesteps the homograph trap that keeps
// these letters OUT of the whole-word lexicon. Letters Alex hasn't vocalised yet
// stay plain. Keep in sync with the lexicon's single-letter entries.
const LATIN_LETTER_HE = {
  A: 'אֶיּי', B: 'ביִ',  C: 'סִי',   D: 'דִי',  E: 'אֶיּ',   F: 'אֶף',
  G: "ג'יִ", H: "אייץ'", I: 'אֶיּי', J: "ג'יי", K: 'קֶיי', L: 'אֶל',
  M: 'אֶם',  N: 'אֶן',  O: 'או',   P: 'פִי',  Q: 'קיו',  R: 'אר',
  S: 'אס',  T: 'טי',  U: 'יו',   V: 'וי',  W: 'דאבליו', X: 'אקס',
  Y: 'וואי', Z: 'זי',
};

const VO_FIXES = [
  // Alex 2026-10-19: spoken "ערוץ 70", never "Ch70"/"CH 16".
  [/\bCH\.?\s?(\d{1,2}[A-Za-z]?)(?![A-Za-z0-9])/gi, 'ערוץ $1'],
  // Drop parenthetical Latin-word glosses like (underway), (bearing), (Kill Switch):
  // the Hebrew term precedes them and is already spoken. Require 2+ consecutive
  // Latin letters so single-letter vessel/flag labels like (K), (G), (A) are kept
  // (the bracket-strip below then exposes them for LATIN_LETTER_HE conversion).
  // Must run before that bracket-strip, which would otherwise leave the word inline.
  [/\([^)]*[A-Za-z]{2,}[^)]*\)/g, ''],
  // A single vessel/flag letter in parens (l12 writes "מנוע(J)", "( N )") must keep
  // a space on both sides, or the bracket-strip glues it to the previous word and
  // LATIN_LETTER_HE reads "מנועJ" as one token ("מנועג'יי"). Spacing it lets the
  // letter convert cleanly, exactly like l11's spaced "כלי שייט J".
  [/\(\s*([A-Za-z])\s*\)/g, ' $1 '],
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
  [/\b(\d+)%/g,       '$1 אחוז'],
  [/(\d+)\.(\d+)/g,   '$1 נקודה $2'],
  [/\//g,             ' או '],
];

// Latin vessel/flag letters -> Hebrew phonetics (J -> ג'יי). This is PRONUNCIATION
// only: apply it for the spoken (TTS) text, but NOT for the on-screen/caption text,
// which must keep the real letter "J" (Alex 2026-09-02). Kept out of VO_FIXES so a
// display build can skip it; runs last so brackets/glosses are already resolved.
// License 40 (GMDSS, Alex 2026-10-19): spaced acronyms ("R C C", "D S C") stay Latin letters, not Hebrew
// transliteration. buildVoiceover sets KEEP_SPACED_ACRONYMS for the duration of one build.
let KEEP_SPACED_ACRONYMS = false;
const inSpacedAcronym = (str, off, len) =>
  /(?:^|[^A-Za-z])[A-Za-z] $/.test(str.slice(0, off)) || /^ [A-Za-z](?![A-Za-z])/.test(str.slice(off + len));
const LETTER_RULES = [
  [/(?<=[֐-׿]-)([A-Za-z])(?![A-Za-z-])/g, (m, l, off, str) => (KEEP_SPACED_ACRONYMS && inSpacedAcronym(str, off, m.length)) ? m : (LATIN_LETTER_HE[l.toUpperCase()] || m)],
  [/(?<![A-Za-z-])([A-Za-z])(?![A-Za-z-])/g, (m, l, off, str) => (KEEP_SPACED_ACRONYMS && inSpacedAcronym(str, off, m.length)) ? m : (LATIN_LETTER_HE[l.toUpperCase()] || m)],
];

// License 40 (Alex 2026-10-20): acronyms stay Latin letters (V H F, D S C), never the Hebrew phonetic of VO_FIXES.
let L40_LATIN = false;
const ACRONYM_RULE = /^\\b(VHF|UTC|GPS|AIS|EPIRB|NUC|SOS|MMSI|DSC|MOB)\\b$/;
const ACRONYM_SPACED = { VHF: 'V H F', UTC: 'U T C', GPS: 'G P S', AIS: 'A I S', MMSI: 'M M S I', DSC: 'D S C', NUC: 'N U C', SOS: 'S O S', MOB: 'M O B' };
const ACRONYM_SPACE = /\b(VHF|UTC|GPS|AIS|MMSI|DSC|NUC|SOS|MOB)\b/g;

// keepLatin=true returns DISPLAY text (letters stay "J"); default transliterates
// them for the TTS voice.
function applyVoFixes(text, keepLatin) {
  let t = text;
  for (const [pat, rep] of VO_FIXES) {
    if (L40_LATIN && ACRONYM_RULE.test(pat.source)) continue;
    t = t.replace(pat, rep);
  }
  if (L40_LATIN) t = t.replace(ACRONYM_SPACE, (m, a) => ACRONYM_SPACED[a] || m);
  if (!keepLatin && !L40_LATIN) for (const [pat, rep] of LETTER_RULES) t = t.replace(pat, rep);   // l40: single Latin letters stay Latin too
  return t.replace(/\s{2,}/g, ' ').trim();
}

// Applies Alex's niqqud lexicon (references/niqqud-lexicon.md -> vo-lexicon.js)
// to content words (מָצוֹף, מֶמוּכַּנִים, סִימָן, עֹגֶן...), so every render is
// vocalised automatically without a manual pass. Whole-word, matched THROUGH any
// existing niqqud so a form is re-set to Alex's. Collision-prone shorts and the
// multi-letter homographs (למנוע/צופה) are already filtered out of vo-lexicon.js;
// flag letters are handled separately in LATIN_LETTER_HE above. [[PAUSE]] has no
// Hebrew so it survives untouched. Same logic as index.html's applyLexiconText.
const HE_MARKS = '[\\u0591-\\u05C7]*';
function lexiconPairs() {
  if (typeof VO_LEXICON !== 'undefined') return VO_LEXICON;          // browser global (vo-lexicon.js)
  try { return require('./vo-lexicon.js').VO_LEXICON; } catch (e) { return []; }  // Node
}
// Single pass (one alternation, longest entry first): a phrase entry ("שלוש עֶשְׂרֵה") must not
// be re-vocalised afterwards by a shorter homograph entry ("עשרה" → עָשָׂרָה).
function applyLexiconText(text) {
  const pairs = lexiconPairs();
  if (!pairs.length) return text;
  const map = new Map();
  const alts = pairs.map(([src, dst], i) => {
    map.set(i, dst);
    return `(?<g${i}>` + [...src].map(ch =>
      /[א-ת]/.test(ch) ? ch + HE_MARKS
      : /\s/.test(ch) ? '\\s+'
      : ch.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    ).join('') + ')';
  });
  const pat = new RegExp(`(?<![\\u05D0-\\u05EA\\u0591-\\u05C7])(?:${alts.join('|')})(?![\\u05D0-\\u05EA\\u0591-\\u05C7])`, 'g');
  return text.replace(pat, (...args) => {
    const groups = args[args.length - 1];
    for (const k in groups) if (groups[k] !== undefined) return map.get(Number(k.slice(1)));
    return args[0];
  });
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

// keepLatin=true builds the DISPLAY/caption text (vessel letters stay "J"); the
// default builds the spoken text (letters transliterated for the TTS voice). The
// two differ ONLY in the letters, so their [[PAUSE]] split and word order match,
// which lets the caption timing (built on the spoken audio) reuse the display text.
// Voice v2 (docs/voice-style-v2.md): the spoken explanation keeps its "..." breath
// marks, which VO_FIXES would otherwise collapse to ".". Shield them with U+2026
// while the fixes run, then restore.
function applySpokenFixes(text, keepLatin) {
  return applyVoFixes(text.replace(/\.{3,}/g, '…'), keepLatin).replace(/…/g, '...');
}

function buildVoiceoverRaw(q, keepLatin) {
  const idx = { 'א': 0, 'ב': 1, 'ג': 2, 'ד': 3 }[(q.answer || 'א').trim()] ?? 0;
  const ans = ((q.options || [])[idx] || '').replace(/^[אבגד]\.\s*/, '');
  const letter = (q.answer || 'א').trim();
  let q1 = applyVoFixes(`שאלה מספר ${q.num}... ${q.q_he}.`, keepLatin);
  if (ANSWER_PROMPT_NUMS.has(Number(q.num))) q1 += ' מה התשובה הנכונה?';
  let q2;
  if (q.explanation_spoken) {
    // v2 spoken style: "התשובה הנכונה היא ב:" (colon, no geresh: eleven_v4 misreads "ב'", Alex 2026-10-04) then the spoken text (which restates
    // the answer itself). A field that already opens with the cue is used as-is.
    const sp = q.explanation_spoken.trim();
    // License 11 keeps the v3-era cue "... ב'!" it was rendered with (Alex 2026-10-04: l11 stays as is).
    // Other licenses speak the letter's alphabet name: a bare "ב:" came out as "bayit" (Alex 2026-10-09, same rule as l30 el_tts).
    const LETTER_NAME = { 'א': 'אָלֶף', 'ב': 'בֵּית', 'ג': 'גִּימֶל', 'ד': 'דָּלֶת' };
    // l12 cue letters (Alex 2026-10-14): "אָלף" and "בֶת". They are lexicon variants, not defaults
    // (the lexicon would turn them into אֶלף / skip בת), so the l12 cue is added AFTER the lexicon pass.
    const l12 = Number(q.license) === 12 || Number(q.license) === 40;   // l40 (Alex 2026-10-19): same cue letters as l12
    if (l12) Object.assign(LETTER_NAME, { 'א': 'אָלף', 'ב': 'בֶת' });
    const cue = (q.license == null || Number(q.license) === 11) ? `התשובה הנכונה... ${letter}'!` : `התשובה הנכונה היא ${LETTER_NAME[letter] || letter}:`;
    if (l12 && !/^התשובה הנכונה/.test(sp)) {
      q1 = applyLexiconText(q1);
      return q1 + ' [[PAUSE]] ' + cue + ' ' + applyLexiconText(applySpokenFixes(sp, keepLatin));
    }
    q2 = applySpokenFixes(/^התשובה הנכונה/.test(sp) ? sp : `${cue} ${sp}`, keepLatin);
  } else {
    q2 = applyVoFixes(`התשובה הנכונה היא ${letter}: ${ans}.`, keepLatin);
    if (q.explanation) q2 += ` ... ${applyVoFixes(q.explanation, keepLatin)}`;
  }
  // Auto-niqqud content words from Alex's lexicon (flag letters already done via
  // LATIN_LETTER_HE inside applyVoFixes) so every render is vocalised, no manual pass.
  q1 = applyLexiconText(q1);
  q2 = applyLexiconText(q2);
  return q1 + ' [[PAUSE]] ' + q2;
}

// Answer letters as the alphabet names (Alex 2026-10-19: the l12 convention "אָלף/בֶת/גִּימֶל/דָּלֶת" sounds right, "א'" and bare letters do not).
// Mirrors tools/l12/fixvo.js, plus the geresh forms ("ב'?", "וד'?") and the plain names. Applied to license 40.
const LETTER_BY = { 'א': 'אָלף', 'ב': 'בֶת', 'ג': 'גִּימֶל', 'ד': 'דָלֶת' };
const NAME_BY = { 'אלף': 'א', 'אֶלף': 'א', 'אָלֶף': 'א', 'אָלף': 'א', 'בית': 'ב', 'בֵּית': 'ב', 'בֶת': 'ב', 'גימל': 'ג', 'גִּימֶל': 'ג', 'דלת': 'ד', 'דָּלֶת': 'ד', 'דָלֶת': 'ד' };
function fixAnswerLetters(t) {
  return t
    .replace(/(^|[\s.!?,])(ו?)(אלף|אֶלף|אָלֶף|אָלף|בית|בֵּית|בֶת|גימל|גִּימֶל|דלת|דָּלֶת|דָלֶת)(?=[\s:?.,!]|$)/g, (m, pre, v, w) => pre + v + LETTER_BY[NAME_BY[w]])
    .replace(/(^|[\s.!?,])(ו?)([אבגד])['׳]?(?=[:?.,!]|\s(?:נכונה|שגויה|וב|ו)|$)/g, (m, pre, v, l) => pre + v + LETTER_BY[l]);
}

// Alex 2026-10-19: "לָמָה לא א'" always, never the lexicon's "לֶמָה לא" (he corrected it by hand on every render).
function buildVoiceover(q, keepLatin) {
  KEEP_SPACED_ACRONYMS = L40_LATIN = Number(q.license) === 40;
  try {
    let v = buildVoiceoverRaw(q, keepLatin).replace(/לֶמָה(?= לא )/g, 'לָמָה');
    if (L40_LATIN) v = v.replace(/מכמ(?![א-ת"])/g, 'מכ"מ');
    if (L40_LATIN) v = v.replace(/(שתים|שלוש|ארבע|חמש|שש|שבע|שמונ[א-ת\u0591-\u05C7]?|תשע)\s+ע[\u0591-\u05C7]*ש[\u0591-\u05C7]*ר[\u0591-\u05C7]*ה(?![א-ת])/g, (m, a) => a + ' עֶשְׂרֵה');   // lexicon gives עָשָׂרָה
    return (Number(q.license) === 40 && !keepLatin) ? fixAnswerLetters(v) : v;
  }
  finally { KEEP_SPACED_ACRONYMS = L40_LATIN = false; }
}

// Dual-use module. In Node (update-question.js, render-with-html.js) it exports
// via CommonJS. In the browser editor (index.html) it is loaded with <script src>;
// the top-level const/function declarations above then live in the shared global
// scope where index.html's inline scripts resolve buildVoiceover/applyVoFixes by
// name. Guard the export so the browser doesn't throw on `module` being undefined.
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { fixAnswerLetters, buildVoiceover, applyVoFixes, applySpokenFixes, applyLexiconText, heNum, VO_FIXES, LATIN_LETTER_HE, ANSWER_PROMPT_NUMS };
}
