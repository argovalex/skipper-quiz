#!/usr/bin/env node
// update-question.js — one command to re-render a question and propagate the new
// video EVERYWHERE the course reads from.
//
//   node tools/quiz-app/update-question.js <num> [num...] [--no-push] [--no-render]
//
// Steps per run:
//   1. render : build the exact editor VO and POST /render/:num (force) -> new videoUrl
//               (--no-render skips this and instead reads the new url from questions.json,
//                e.g. when you already re-rendered from the editor)
//   2. sync   : write the new videoUrl into data/l11.json (canonical)
//   3. pause  : drop the num from pause-map.json and re-run build-pausemap.js (silencedetect
//               on the NEW video -> fresh pauseAt/resumeAt)
//   4. embed  : run merge-inject.js -> rebuild quiz-data-l11.json + quiz-app.html embed
//   5. ship   : git add the 4 files, commit, pull --rebase, push (unless --no-push)
//
// questions.json is intentionally NOT touched here: the render server auto-commits
// the videoUrl to it on GitHub. The pull --rebase in step 5 absorbs that commit.

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { buildVoiceover } = require('./vo.js');
const { genHtml } = require('./scene-html.js');

const ROOT = path.resolve(__dirname, '..', '..');
const HERE = __dirname;
const RENDER_URL = process.env.RENDER_URL || 'https://skipper-quiz-publisher-production.up.railway.app';

const args = process.argv.slice(2);
const noPush = args.includes('--no-push');
const noRender = args.includes('--no-render');
const nums = args.filter(a => /^\d+$/.test(a));
if (!nums.length) {
  console.error('usage: node tools/quiz-app/update-question.js <num> [num...] [--no-push] [--no-render]');
  process.exit(1);
}

const p = f => path.join(ROOT, f);
const load = f => JSON.parse(fs.readFileSync(p(f), 'utf8'));
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function render(num, q) {
  const vo = buildVoiceover(q);
  const html = genHtml(q); // question-specific visual — REQUIRED, else the server renders a generic anchor
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
    if (!res.ok || !data.videoUrl) throw new Error(data.error || `HTTP ${res.status}`);
    return data.videoUrl;
  } finally { clearTimeout(t); }
}

function git(...a) {
  const r = spawnSync('git', a, { cwd: ROOT, encoding: 'utf8' });
  if (r.status !== 0) throw new Error(`git ${a.join(' ')} failed:\n${r.stderr || r.stdout}`);
  return (r.stdout || '').trim();
}
function node(script) {
  const r = spawnSync(process.execPath, [path.join(HERE, script)], { cwd: ROOT, encoding: 'utf8', stdio: 'inherit' });
  if (r.status !== 0) throw new Error(`${script} failed`);
}

(async () => {
  const bank = load('data/l11.json');
  const questions = load('questions.json');
  const qById = new Map(questions.map(q => [String(q.num), q]));
  const newUrls = {};

  // 1) render (or read new url from questions.json if --no-render)
  for (const num of nums) {
    const q = bank.find(x => String(x.num) === num);
    if (!q) { console.error(`! ${num} not in data/l11.json — skipping`); continue; }
    if (noRender) {
      const u = qById.get(num) && qById.get(num).videoUrl;
      if (!u) { console.error(`! ${num} has no videoUrl in questions.json — skipping`); continue; }
      newUrls[num] = u;
      console.log(`read ${num}  ${u}`);
    } else {
      process.stdout.write(`render ${num} ... `);
      const started = Date.now();
      try {
        newUrls[num] = await render(num, q);
        console.log(`${((Date.now() - started) / 1000).toFixed(0)}s  ${newUrls[num]}`);
      } catch (e) { console.log(`FAIL: ${e.message}`); }
      await sleep(1000);
    }
  }
  const done = Object.keys(newUrls);
  if (!done.length) { console.error('nothing rendered; aborting'); process.exit(1); }

  // 2) sync new videoUrl into data/l11.json (surgical raw replace; old urls are unique)
  let raw = fs.readFileSync(p('data/l11.json')).toString('utf8'); // preserves CRLF
  const l11 = new Map(bank.map(q => [String(q.num), q]));
  let synced = 0;
  for (const num of done) {
    const oldUrl = l11.get(num) && l11.get(num).videoUrl;
    const newUrl = newUrls[num];
    if (oldUrl && oldUrl !== newUrl && raw.includes(`"${oldUrl}"`)) { raw = raw.replace(`"${oldUrl}"`, `"${newUrl}"`); synced++; }
    else if (oldUrl === newUrl) synced++;
    else console.error(`! ${num}: old url not found in data/l11.json`);
  }
  fs.writeFileSync(p('data/l11.json'), raw);
  console.log(`videoUrl synced into data/l11.json: ${synced}/${done.length}`);

  // 3) invalidate pause-map for these nums, then recompute
  const PM = path.join(HERE, 'pause-map.json');
  const pm = JSON.parse(fs.readFileSync(PM, 'utf8'));
  for (const num of done) delete pm[num];
  fs.writeFileSync(PM, JSON.stringify(pm, null, 0));
  console.log(`pause-map invalidated: ${done.join(',')}`);
  node('build-pausemap.js');

  // 4) rebuild public data + embed
  node('merge-inject.js');

  // 5) ship
  git('add', 'data/l11.json', 'quiz-data-l11.json', 'quiz-app.html', 'tools/quiz-app/pause-map.json');
  const staged = git('diff', '--cached', '--name-only');
  if (!staged) { console.log('no changes to commit'); return; }
  git('commit', '-m', `update-question ${done.join(',')}: re-render + propagate to course data`);
  console.log(`committed ${done.length} question(s)`);
  if (noPush) { console.log('--no-push: leaving commit local'); return; }
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      try { git('pull', '--rebase'); } catch (e) { /* nothing to pull / diverged handled by push retry */ }
      git('push');
      console.log('pushed to origin/main');
      return;
    } catch (e) {
      console.log(`push attempt ${attempt} failed, retrying...`);
      await sleep(3000);
    }
  }
  console.error('push failed after 3 attempts — run `git pull --rebase && git push` manually');
  process.exit(1);
})();
