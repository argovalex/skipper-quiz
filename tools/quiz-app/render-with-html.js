// Renders questions WITH the question-specific visual (the html param), the way
// the editor does. Fixes the generic-video regression from API renders that
// omitted `html`. Loads scenes.js in a vm sandbox (same as src/generate-all-l11.js)
// to produce generateQuizHTML(q,'he',true), and POSTs it alongside the VO.
//
//   node tools/quiz-app/render-with-html.js <num> [num...]
//
// Prints "OK <num> <videoUrl>" per success. Does NOT commit — a caller (or a
// follow-up sync + merge-inject) handles propagation. Audio/VO is unchanged, so
// pause points do not need recomputing.
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { buildVoiceover } = require('./vo.js');

const ROOT = path.resolve(__dirname, '..', '..');
const RENDER_URL = process.env.RENDER_URL || 'https://skipper-quiz-publisher-production.up.railway.app';

// --- load scenes.js exactly like src/generate-all-l11.js ---
const scenesCode = fs.readFileSync(path.join(ROOT, 'scenes.js'), 'utf8');
const sandbox = {
  console, JSON, Math, parseInt, parseFloat, String, Array, Object, RegExp, Number, Date,
  currentLang: 'he',
  document: { getElementById: () => ({ value: '' }) },
  window: {},
};
vm.createContext(sandbox);
vm.runInContext(scenesCode, sandbox);

const questions = JSON.parse(fs.readFileSync(path.join(ROOT, 'questions.json'), 'utf8'));
const qById = new Map(questions.map(q => [String(q.num), q]));

const nums = process.argv.slice(2).filter(a => /^\d+$/.test(a));
if (!nums.length) { console.error('usage: node render-with-html.js <num> [num...]'); process.exit(1); }
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function renderOne(num) {
  const q = qById.get(String(num));
  if (!q) return { num, ok: false, err: 'not in questions.json' };
  let html;
  try { html = sandbox.generateQuizHTML(q, 'he', true); }
  catch (e) { return { num, ok: false, err: 'generateQuizHTML: ' + e.message }; }
  if (!html || html.length < 500) return { num, ok: false, err: 'html too short (' + (html ? html.length : 0) + ')' };
  const vo = buildVoiceover(q);
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 180000);
  try {
    const res = await fetch(`${RENDER_URL}/render/${num}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ voiceover_text: vo, force: true, html }),
      signal: ctrl.signal,
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.videoUrl) return { num, ok: false, err: data.error || `HTTP ${res.status}` };
    return { num, ok: true, videoUrl: data.videoUrl, htmlLen: html.length };
  } catch (e) { return { num, ok: false, err: e.name === 'AbortError' ? 'TIMEOUT' : e.message }; }
  finally { clearTimeout(t); }
}

(async () => {
  let ok = 0, fail = 0;
  for (const num of nums) {
    const s = Date.now();
    const r = await renderOne(num);
    const secs = ((Date.now() - s) / 1000).toFixed(0);
    if (r.ok) { ok++; console.log(`OK   ${num}  ${secs}s  html=${r.htmlLen}b  ${r.videoUrl}`); }
    else { fail++; console.log(`FAIL ${num}  ${secs}s  ${r.err}`); }
    await sleep(1200);
  }
  console.log(`\n--- ${ok} ok, ${fail} fail of ${nums.length} ---`);
})();
