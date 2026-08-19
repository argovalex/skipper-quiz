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
//   6. course : upsert data/l11.json into the course Postgres `bank` table and reload
//               the course API, so the PAID app serves the new video (unless --no-db).
//               Needs course/api/.env with DATABASE_URL (+ ADMIN_TOKEN for instant reload).
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
const noDb = args.includes('--no-db');
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

// minimal .env parser (same shape as course/api/src/loadenv.js) — read secrets
// from course/api/.env without importing them into this process.
function readEnvFile(file) {
  const out = {};
  try {
    for (const line of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
      if (line.trim().startsWith('#')) continue;
      const m = line.match(/^\s*([A-Za-z0-9_]+)\s*=\s*(.*?)\s*$/);
      if (!m) continue;
      let v = m[2];
      if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
      out[m[1]] = v;
    }
  } catch { /* no file — fine */ }
  return out;
}

// Step 6: mirror data/l11.json into the course Postgres and reload the paid API.
// Best-effort: a missing DB config or an unreachable API warns but never fails the run.
async function propagateToCourseDb(done) {
  if (noDb) { console.log('--no-db: skipping course DB propagation'); return; }
  const apiDir = path.join(ROOT, 'course', 'api');
  const env = readEnvFile(path.join(apiDir, '.env'));
  if (!(process.env.DATABASE_URL || env.DATABASE_URL)) {
    console.log('course DB: no DATABASE_URL in course/api/.env — skipping (paid app keeps old video)');
    return;
  }
  process.stdout.write(`course DB: bank import ... `);
  // admin.js loads course/api/.env via its own __dirname, so cwd doesn't matter for DATABASE_URL.
  const r = spawnSync(process.execPath, [path.join(apiDir, 'admin.js'), 'bank', 'import'], { cwd: apiDir, encoding: 'utf8' });
  if (r.status !== 0) { console.log(`FAIL\n${(r.stderr || r.stdout || '').trim()}`); return; }
  const m = (r.stdout || '').match(/imported\s+(\d+)/i);
  console.log(m ? `ok (${m[1]} questions)` : 'ok');
  const apiUrl = (process.env.COURSE_API_URL || env.COURSE_API_URL || 'https://skipper-quiz-production.up.railway.app').replace(/\/$/, '');
  const token = process.env.ADMIN_TOKEN || env.ADMIN_TOKEN;
  if (!token) { console.log('course API: no ADMIN_TOKEN — server refreshes within 5 min (cache TTL)'); return; }
  try {
    const res = await fetch(`${apiUrl}/api/admin/reload`, { method: 'POST', headers: { 'x-admin': token } });
    console.log(res.ok ? 'course API: reloaded (paid app now serves new video)' : `course API: reload HTTP ${res.status} — refreshes within 5 min`);
  } catch (e) { console.log(`course API: reload failed (${e.message}) — refreshes within 5 min`); }
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
  if (noPush) {
    console.log('--no-push: leaving commit local');
    await propagateToCourseDb(done);
    return;
  }
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      try { git('pull', '--rebase'); } catch (e) { /* nothing to pull / diverged handled by push retry */ }
      git('push');
      console.log('pushed to origin/main');
      await propagateToCourseDb(done);
      return;
    } catch (e) {
      console.log(`push attempt ${attempt} failed, retrying...`);
      await sleep(3000);
    }
  }
  console.error('push failed after 3 attempts — run `git pull --rebase && git push` manually');
  process.exit(1);
})();
