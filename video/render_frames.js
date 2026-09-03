// render_frames.js — emits the two CANONICAL question visuals (question state and
// answer-revealed state) as PNGs, plus the canonical voiceover text, for the local
// free video pipeline (video/make_question_video.py). Reuses scenes.js's
// generateQuizHTML (the exact visual the render server produces) via a vm sandbox,
// exactly like tools/quiz-app/scene-html.js and src/generate-all-l11.js — so the
// vertical video's visuals never drift from the canonical ones.
//
//   node video/render_frames.js <num> <outDir> [--license 11]
//
// Writes  <outDir>/q<num>_question.png , <outDir>/q<num>_answer.png , <outDir>/q<num>.vo.txt
// Prints one JSON line: {num, topic, voPath, questionPng, answerPng}
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const http = require('http');
const puppeteer = require('puppeteer');
const { buildVoiceover } = require('../tools/quiz-app/vo.js');

const ROOT = path.resolve(__dirname, '..');

// Serve media/ over localhost so l12's compass-rose boat/sign images (referenced
// by raw.githubusercontent in scenes.js) load into the about:blank render even
// before those assets are pushed. Harmless for l11 (no boat images requested).
const MIME = { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml' };
function startMediaServer() {
  return new Promise(resolve => {
    const srv = http.createServer((req, res) => {
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
      const fp = path.join(ROOT, rel);
      if (!fp.startsWith(path.join(ROOT, 'media'))) { res.writeHead(403); return res.end(); }
      fs.readFile(fp, (e, b) => {
        if (e) { res.writeHead(404); return res.end(); }
        res.writeHead(200, { 'Content-Type': MIME[path.extname(fp).toLowerCase()] || 'application/octet-stream', 'Access-Control-Allow-Origin': '*' });
        res.end(b);
      });
    });
    srv.listen(0, () => resolve(srv));
  });
}

function arg(flag, def) {
  const i = process.argv.indexOf(flag);
  return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : def;
}

const num = String(process.argv[2] || '').trim();
const outDir = process.argv[3];
const license = arg('--license', '11');
if (!/^\d+$/.test(num) || !outDir) {
  console.error('usage: node video/render_frames.js <num> <outDir> [--license 11]');
  process.exit(1);
}
fs.mkdirSync(outDir, { recursive: true });

// --- load the question from the canonical per-license bank ---
function loadQuestion() {
  const bankPath = path.join(ROOT, 'data', `l${license}.json`);
  let arr;
  if (fs.existsSync(bankPath)) {
    arr = JSON.parse(fs.readFileSync(bankPath, 'utf8'));
    arr = Array.isArray(arr) ? arr : (arr.questions || Object.values(arr).find(Array.isArray));
  } else {
    // fall back to derived questions.json (runtime artifact) if the bank is missing
    arr = JSON.parse(fs.readFileSync(path.join(ROOT, 'questions.json'), 'utf8'));
  }
  const q = arr.find(x => String(x.num) === num);
  if (!q) throw new Error(`Q${num} not found in l${license} bank`);
  return q;
}

// --- load scenes.js in a vm sandbox (same setup as scene-html.js) ---
function makeGenHtml(mediaBase) {
  const scenesCode = fs.readFileSync(path.join(ROOT, 'scenes.js'), 'utf8');
  const sandbox = {
    console, JSON, Math, parseInt, parseFloat, String, Array, Object, RegExp, Number, Date,
    currentLang: 'he',
    document: { getElementById: () => ({ value: '' }) },
    window: {},
    VESSEL_IMG_BASE: `${mediaBase}/vessels`,
    SIGN_IMG_BASE: `${mediaBase}/signs`,
  };
  vm.createContext(sandbox);
  vm.runInContext(scenesCode, sandbox);
  return q => sandbox.generateQuizHTML(q, 'he', true);
}

(async () => {
  const q = loadQuestion();
  const server = await startMediaServer();
  const mediaBase = `http://127.0.0.1:${server.address().port}/media`;
  const genHtml = makeGenHtml(mediaBase);
  let html = genHtml(q);
  if (!html || html.length < 500) throw new Error(`generateQuizHTML too short for Q${num}`);
  // Speed the auto-play clock so the reveal happens fast for the second screenshot.
  html = html.replace('const DELAY=15000', 'const DELAY=40');

  const vo = buildVoiceover(q);                 // spoken (letters -> ג'יי for TTS)
  const voDisplay = buildVoiceover(q, true);    // caption text (letters stay "J")
  const voPath = path.join(outDir, `q${num}.vo.txt`);
  const voDisplayPath = path.join(outDir, `q${num}.disp.txt`);
  fs.writeFileSync(voPath, vo, 'utf8');
  fs.writeFileSync(voDisplayPath, voDisplay, 'utf8');

  const questionPng = path.join(outDir, `q${num}_question.png`);
  const answerPng = path.join(outDir, `q${num}_answer.png`);

  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
    headless: 'new',
  });
  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 390, height: 625, deviceScaleFactor: 3 });
    await page.setContent(html, { waitUntil: 'networkidle0', timeout: 60000 });
    // fonts + any mediaUrl image
    await page.evaluate(() => document.fonts && document.fonts.ready).catch(() => {});
    await page.evaluate(async () => {
      const imgs = Array.from(document.images || []);
      await Promise.all(imgs.map(im => im.complete ? 0 : new Promise(r => { im.onload = im.onerror = r; })));
    }).catch(() => {});
    await new Promise(r => setTimeout(r, 350));

    const reel = await page.$('#reel');
    await reel.screenshot({ path: questionPng });

    // reveal the answer, then screenshot the answer state
    await page.evaluate(() => window.__startAutoPlay && window.__startAutoPlay());
    await new Promise(r => setTimeout(r, 1300));
    await reel.screenshot({ path: answerPng });
  } finally {
    await browser.close();
    server.close();
  }

  process.stdout.write(JSON.stringify({
    num, topic: q.topic || '', voPath, voDisplayPath, questionPng, answerPng,
  }) + '\n');
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
