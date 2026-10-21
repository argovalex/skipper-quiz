#!/usr/bin/env node
// sq.js — one entry point for the recurring SkipperQuiz operations (docs/SYSTEMS.md).
// Wraps the existing scripts; adds the preflight that CLAUDE.md otherwise asks every
// session to remember: pull, regenerate the VO lexicon, and refuse to render a question
// whose mediaUrl image is not on GitHub yet.
//
//   node tools/sq.js <command> [args]        or   npm run <command> -- [args]
//
//   status                          git status + local/remote commit gap
//   sync                            pull (ff-only) + gen-vo-lexicon
//   preflight <num...> [--license N]  sync + media-on-GitHub check, nothing else
//   check   <num...> [--license N]  preflight + vo-check (new unapproved VO words)
//   render  <num...> [--license N] [update-question flags]   preflight + update-question.js
//           --local-voice: voice made here by tools/voice/voice.js, sent as --audio
//   voice   <voice.js args>         segments | say | question | master (tools/voice/voice.js)
//   stored  <num...>                l12 render from stored voiceover_text + propagate
//   propagate <num...> [--license N]  update-question --no-render (already rendered in the editor)
//   pausemap [--license N]          build-pausemap + merge-inject
//   lexicon                         gen-vo-lexicon only
//   html                            regenerate html/ (after a content change)
//   topics                          rebuild course/site topic pages + sitemap
//   brand <lesson.mp4> [out.mp4]    brand a lesson video
//   quota                           ElevenLabs character quota
//
// Preflight flags: --no-sync skips pull+lexicon, --push-media commits and pushes
// missing mediaUrl images (only those files) instead of aborting.
'use strict';
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const RAW = 'https://raw.githubusercontent.com/argovalex/skipper-quiz/main/';
const QA = path.join(ROOT, 'tools', 'quiz-app');

const [cmd, ...rest] = process.argv.slice(2);
const flag = f => rest.includes(f);
const SQ_FLAGS = new Set(['--no-sync', '--push-media', '--local-voice']);
const passArgs = rest.filter(a => !SQ_FLAGS.has(a));
const li = rest.indexOf('--license');
let LICENSE = li !== -1 ? parseInt(rest[li + 1], 10) : 11;
const nums = rest.filter((a, i) => /^\d+$/.test(a) && !(li !== -1 && i === li + 1));

function run(exe, args, opts = {}) {
  const r = spawnSync(exe, args, { cwd: ROOT, stdio: 'inherit', windowsHide: true, ...opts });
  if (r.status !== 0 && !opts.allowFail) process.exit(r.status || 1);
  return r.status;
}
function git(...args) {
  const r = spawnSync('git', args, { cwd: ROOT, encoding: 'utf8', windowsHide: true });
  return { ok: r.status === 0, out: (r.stdout || '').trim(), err: (r.stderr || '').trim() };
}
const node = (script, args = []) => run(process.execPath, [script, ...args]);
const die = msg => { console.error(`✗ ${msg}`); process.exit(1); };

function sync() {
  git('fetch', 'origin');
  const behind = git('rev-list', '--count', 'HEAD..origin/main').out;
  if (behind !== '0') {
    // ff-only: never rebase/autostash over another session's dirty files
    const p = git('merge', '--ff-only', 'origin/main');
    if (!p.ok) die(`local is ${behind} commits behind origin and fast-forward failed:\n${p.err}\nresolve manually (no autostash with foreign dirty files).`);
    console.log(`✓ pulled ${behind} commits`);
  } else console.log('✓ up to date with origin');
  node(path.join(QA, 'gen-vo-lexicon.js'));
  if (git('status', '--porcelain', 'tools/quiz-app/vo-lexicon.js').out)
    console.log('! vo-lexicon.js changed (lexicon was edited); commit it with the next push');
}

// Every mediaUrl served from raw.githubusercontent must exist on origin/main,
// otherwise the render shows a broken image icon.
function checkMedia() {
  const bankFile = path.join(ROOT, 'data', `l${LICENSE}.json`);
  if (!fs.existsSync(bankFile)) die(`no bank for license ${LICENSE}`);
  const bank = JSON.parse(fs.readFileSync(bankFile, 'utf8'));
  const missing = [];
  for (const n of nums) {
    const q = bank.find(x => String(x.num) === n);
    if (!q) die(`question ${n} not in data/l${LICENSE}.json`);
    if (!q.mediaUrl || !q.mediaUrl.startsWith(RAW)) continue;
    const rel = decodeURIComponent(q.mediaUrl.slice(RAW.length).split('?')[0]);
    if (!fs.existsSync(path.join(ROOT, rel))) die(`Q${n}: mediaUrl file missing locally: ${rel}`);
    const onOrigin = git('cat-file', '-e', `origin/main:${rel}`).ok;
    const dirty = git('status', '--porcelain', '--', rel).out;
    if (!onOrigin || dirty) missing.push({ n, rel });
  }
  if (!missing.length) { console.log('✓ media on GitHub'); return; }
  const list = missing.map(m => `  Q${m.n}: ${m.rel}`).join('\n');
  if (!flag('--push-media')) die(`media not on GitHub yet:\n${list}\nrerun with --push-media to push only these files.`);
  const files = [...new Set(missing.map(m => m.rel))];
  if (!git('add', '--', ...files).ok) die('git add failed');
  const c = git('commit', '-m', `media: push images for Q${missing.map(m => m.n).join(',')}`,
    '-m', 'Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>', '--', ...files);
  if (!c.ok) die(`commit failed:\n${c.err || c.out}`);
  const p = git('push', 'origin', 'main');
  if (!p.ok) die(`push failed:\n${p.err}`);
  console.log(`✓ pushed ${files.length} media file(s)`);
}

function preflight() {
  if (!nums.length) die('give at least one question number');
  if (!flag('--no-sync')) sync();
  checkMedia();
}

const commands = {
  status() {
    run('git', ['status', '--short', '--branch']);
    git('fetch', 'origin');
    console.log(`ahead of origin: ${git('rev-list', '--count', 'origin/main..HEAD').out}, behind: ${git('rev-list', '--count', 'HEAD..origin/main').out}`);
  },
  sync,
  preflight,
  lexicon: () => node(path.join(QA, 'gen-vo-lexicon.js')),
  check() { preflight(); node(path.join(QA, 'vo-check.js'), passArgs); },
  render() {
    preflight();
    if (!flag('--local-voice')) return node(path.join(QA, 'update-question.js'), passArgs);
    // voice generated here by tools/voice/voice.js and shipped as --audio (server TTS skipped)
    const dir = path.join(ROOT, 'output', 'voice-v2', 'q');
    node(path.join(ROOT, 'tools', 'voice', 'voice.js'), ['question', ...nums, '--license', String(LICENSE),
      ...(flag('--stored-vo') ? ['--stored-vo'] : []), '--out', dir]);
    node(path.join(QA, 'update-question.js'), [...passArgs, '--audio', dir]);
  },
  voice: () => node(path.join(ROOT, 'tools', 'voice', 'voice.js'), passArgs),
  propagate() {
    if (!nums.length) die('give at least one question number');
    node(path.join(QA, 'update-question.js'), [...passArgs, '--no-render']);
  },
  stored() {
    // render-stored.js reads data/l12.json only
    if (li !== -1 && LICENSE !== 12) die('stored renders are l12 only');
    LICENSE = 12;
    preflight();
    node(path.join(ROOT, 'tools', 'l12', 'render-stored.js'), nums);
    const extra = passArgs.filter((a, i) => a.startsWith('--') && a !== '--license' && !(i > 0 && passArgs[i - 1] === '--license'));
    node(path.join(QA, 'update-question.js'), [...nums, '--license', '12', '--no-render', ...extra]);
  },
  pausemap() {
    node(path.join(QA, 'build-pausemap.js'), passArgs);
    node(path.join(QA, 'merge-inject.js'), passArgs);
  },
  html: () => node(path.join(ROOT, 'src', 'generate-all-l11.js')),
  topics: () => node(path.join(ROOT, 'course', 'site', 'build-topics.js')),
  brand() {
    if (!passArgs.length) die('usage: brand <lesson.mp4> [branded.mp4]');
    run('python', [path.join(ROOT, 'tools', 'lesson', 'brand.py'), ...passArgs],
      { env: { ...process.env, PYTHONIOENCODING: 'utf-8' } });
  },
  quota: () => node(path.join(ROOT, 'tools', 'voice', 'el-quota.js')),
};

if (!cmd || !commands[cmd]) {
  const doc = fs.readFileSync(__filename, 'utf8').split('\n').filter(l => l.startsWith('//')).slice(0, 28);
  console.log(doc.map(l => l.replace(/^\/\/ ?/, '')).join('\n'));
  process.exit(cmd ? 1 : 0);
}
commands[cmd]();
