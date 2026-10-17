// l12 stored-VO fixes (Alex 2026-10-14). Run from repo root:
//   node tools/l12/fixvo.js <n,n,n> [--keep n,n]
// EXPLICIT list only (a range once rebuilt older Alex-approved VOs).
// --keep = questions whose voiceover_text Alex hand-edited: fix that text instead of rebuilding.
// Fixes: singular כּליִ שָייט, לָמָה לא, אָלף / בֶת for answer letters, שתים..תשע עֶשְׂרֵה.
// These live only in the stored VO, so render with tools/l12/render-stored.js, never plain
// update-question.js (it rebuilds the VO and undoes them).
const fs = require('fs'), path = require('path');
const ROOT = process.cwd();
const { buildVoiceover } = require(path.join(ROOT, 'tools/quiz-app/vo.js'));
const a = process.argv.slice(2);
const NUMS = a[0].split(',').map(Number);
const ki = a.indexOf('--keep');
const KEEP = new Set(ki !== -1 ? a[ki + 1].split(',') : []);
const F = path.join(ROOT, 'data/l12.json');
const raw = fs.readFileSync(F, 'utf8');
const data = JSON.parse(raw);
const fix = v => v
  .replace(/כְּלֵי שָייט/g, 'כּליִ שָייט')
  .replace(/(ו?)(?:לֶמָה|למה) לא/g, '$1לָמָה לא')
  .replace(/(שתים|שלוש|ארבע|חמש|שש|שבע|שמונה|תשע) עָשָׂרָה/g, '$1 עֶשְׂרֵה')
  .replace(/אֶלף|אָלֶף/g, 'אָלף')
  .replace(/בֵּית/g, 'בֶת')
  .replace(/(^|[\s.!?,])(ו?)ב(?=[:?.,]|\sנכונה)/g, '$1$2בֶת')
  .replace(/(^|[\s.!?,])(ו?)א(?=[:?.,]|\sנכונה)/g, '$1$2אָלף')
  .replace(/(^|[\s.!?,])(ו?)גימל(?=[\s.,:?!]|$)/g, '$1$2גִּימֶל')
  .replace(/(^|[\s.!?,])(ו?)דלת(?=[\s.,:?!]|$)/g, '$1$2דָּלֶת');
for (const n of NUMS) {
  const q = data.find(x => x.num === n);
  if (!q || !q.answer_confirmed) continue;
  const base = KEEP.has(String(n)) ? q.voiceover_text : buildVoiceover(q);
  const v = fix(base);
  if (v !== q.voiceover_text) console.log(n, 'changed');
  q.voiceover_text = v;
}
let s = JSON.stringify(data, null, 2);
if (raw.includes('\r\n')) s = s.replace(/\n/g, '\r\n');
fs.writeFileSync(F, s);
