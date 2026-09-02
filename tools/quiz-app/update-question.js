#!/usr/bin/env node
// update-question.js — one command to re-render a question and propagate the new
// video EVERYWHERE the course reads from.
//
//   node tools/quiz-app/update-question.js <num> [num...] [--license N] [--no-push] [--no-render]
//   --license N (default 11) selects the bank/derived files: data/l<N>.json,
//   quiz-data-l<N>.json, pause-map[-l<N>].json, quiz-app[-l<N>].html.
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
const { paths, parseLicense } = require('./paths');

const ROOT = path.resolve(__dirname, '..', '..');
const HERE = __dirname;
const RENDER_URL = process.env.RENDER_URL || 'https://skipper-quiz-publisher-production.up.railway.app';

const args = process.argv.slice(2);
const noPush = args.includes('--no-push');
const noRender = args.includes('--no-render');
const noDb = args.includes('--no-db');
const LICENSE = parseLicense(args);
const P = paths(LICENSE);
// repo-relative paths (for git add / p()/load()); default license 11 keeps the old names
const rel = f => path.relative(ROOT, f).replace(/\\/g, '/');
const BANK = rel(P.bank), QUIZDATA = rel(P.quizData), PAUSEMAP = rel(P.pauseMap), QUIZAPP = rel(P.quizApp);
// nums = digit args, minus the value that follows --license
const li = args.indexOf('--license');
const nums = args.filter((a, i) => /^\d+$/.test(a) && !(li !== -1 && i === li + 1));
if (!nums.length) {
  console.error('usage: node tools/quiz-app/update-question.js <num> [num...] [--license N] [--no-push] [--no-render]');
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
function node(script, extra = []) {
  const r = spawnSync(process.execPath, [path.join(HERE, script), ...extra], { cwd: ROOT, encoding: 'utf8', stdio: 'inherit' });
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

// Step 6: push the changed questions into the course Postgres via the server's
// admin endpoint (runs inside Railway — no local DB access needed). Sends the FRESH
// objects from data/l11.json so there is no GitHub cache lag. The endpoint reloads
// the content cache itself. Best-effort: missing token or unreachable API warns only.
async function propagateToCourseDb(done) {
  if (noDb) { console.log('--no-db: skipping course propagation'); return; }
  const env = readEnvFile(path.join(ROOT, 'course', 'api', '.env'));
  const apiUrl = (process.env.COURSE_API_URL || env.COURSE_API_URL || 'https://skipper-quiz-production.up.railway.app').replace(/\/$/, '');
  const token = process.env.ADMIN_TOKEN || env.ADMIN_TOKEN;
  if (!token) { console.log('course: no ADMIN_TOKEN (course/api/.env) — paid app refreshes within 5 min (cache TTL)'); return; }
  // re-read the file we just wrote so the objects carry the new videoUrl
  const all = JSON.parse(fs.readFileSync(p(BANK), 'utf8'));
  const want = new Set(done.map(String));
  const questions = all.filter(q => q.num != null && want.has(String(q.num)));
  process.stdout.write(`course: bank-import ${done.join(',')} ... `);
  try {
    const res = await fetch(`${apiUrl}/api/admin/bank-import`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-admin': token },
      body: JSON.stringify({ questions }),
    });
    const data = await res.json().catch(() => ({}));
    console.log((res.ok && data.ok)
      ? `ok (${data.imported} upserted — paid app updated)`
      : `FAIL: HTTP ${res.status} ${data.error || ''}`);
  } catch (e) { console.log(`FAIL: ${e.message} (paid app refreshes within 5 min)`); }
}

(async () => {
  const bank = load(BANK);
  const questions = load('questions.json');
  const qById = new Map(questions.map(q => [String(q.num), q]));
  const newUrls = {};

  // 1) render (or read new url from questions.json if --no-render)
  for (const num of nums) {
    const q = bank.find(x => String(x.num) === num);
    if (!q) { console.error(`! ${num} not in ${BANK} — skipping`); continue; }
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

  // 2) sync new videoUrl into the bank (surgical raw replace; old urls are unique)
  let raw = fs.readFileSync(p(BANK)).toString('utf8'); // preserves CRLF
  const byNum = new Map(bank.map(q => [String(q.num), q]));
  let synced = 0;
  for (const num of done) {
    const oldUrl = byNum.get(num) && byNum.get(num).videoUrl;
    const newUrl = newUrls[num];
    if (oldUrl && oldUrl !== newUrl && raw.includes(`"${oldUrl}"`)) { raw = raw.replace(`"${oldUrl}"`, `"${newUrl}"`); synced++; }
    else if (oldUrl === newUrl) synced++;
    else console.error(`! ${num}: old url not found in ${BANK}`);
  }
  fs.writeFileSync(p(BANK), raw);
  console.log(`videoUrl synced into ${BANK}: ${synced}/${done.length}`);

  // 3) invalidate pause-map for these nums, then recompute
  const PM = P.pauseMap;
  const pm = fs.existsSync(PM) ? JSON.parse(fs.readFileSync(PM, 'utf8')) : {};
  for (const num of done) delete pm[num];
  fs.writeFileSync(PM, JSON.stringify(pm, null, 0));
  console.log(`pause-map invalidated: ${done.join(',')}`);
  node('build-pausemap.js', ['--license', String(LICENSE)]);

  // 4) rebuild public data + embed
  node('merge-inject.js', ['--license', String(LICENSE)]);

  // 5) ship (only stage files that actually exist — e.g. a license may have no player yet)
  const toAdd = [BANK, QUIZDATA, QUIZAPP, PAUSEMAP].filter(f => fs.existsSync(p(f)));
  git('add', ...toAdd);
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
