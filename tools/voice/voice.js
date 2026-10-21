#!/usr/bin/env node
// voice.js — the one VO pipeline: text -> niqqud (vo.js engine) -> ElevenLabs (Alex's clone)
// -> mastering (voice-config.json chain) -> length check. Used by lessons (el_tts.py,
// tools/lesson/tts.py --elevenlabs), the VO editor server and local question audio.
//
//   node tools/voice/voice.js segments <vo.txt> <aud_dir> [--plain] [--model M]
//        '## sid' sections -> <aud_dir>/seg_<sid>.mp3, cached per text in <aud_dir>/raw/<sid>.txt.
//        Default = l30/l40 lesson rules (answer letters as alphabet names, 3s pause after
//        "התשובה הנכונה היא"). --plain = niqqud only (l11 lessons).
//   node tools/voice/voice.js say "<text>|@file.txt" <out.mp3> [--license N]
//        [[PAUSE]] = 2.5s silence (editor convention).
//   node tools/voice/voice.js question <num...> [--license N] [--stored-vo] [--out DIR]
//        <DIR>/<num>_q.mp3 + <num>_a.mp3 for update-question.js --audio DIR
//        (same split and model rule as the render server).
//   node tools/voice/voice.js master <in.mp3> <out.mp3>
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..', '..');
const CFG = JSON.parse(fs.readFileSync(path.join(__dirname, 'voice-config.json'), 'utf8'));
const MASTER_CHAIN = CFG.masterChain;

function loadEnv() {
  try {
    for (const line of fs.readFileSync(path.join(ROOT, '.env'), 'utf8').split(/\r?\n/)) {
      const m = line.match(/^\s*(ELEVENLABS_[A-Z0-9_]+)\s*=\s*(.*?)\s*$/);
      if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
    }
  } catch { /* no .env */ }
}
loadEnv();

// ELEVENLABS_MODEL in the environment overrides; l11 stays on eleven_v3 (Alex 2026-10-04)
function modelFor(license) {
  return process.env.ELEVENLABS_MODEL || CFG.models[String(license)] || CFG.models.default;
}

const sleep = ms => new Promise(r => setTimeout(r, ms));
async function synth(text, out, { model = modelFor(), voiceId = process.env.ELEVENLABS_VOICE_ID } = {}) {
  const key = process.env.ELEVENLABS_API_KEY;
  if (!key || !voiceId) throw new Error('ELEVENLABS_API_KEY / ELEVENLABS_VOICE_ID missing in .env');
  let errors = 0;
  for (let attempt = 0; attempt < 20; attempt++) {
    try {
      const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=${CFG.outputFormat}`, {
        method: 'POST',
        headers: { 'xi-api-key': key, 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, model_id: model }),
        signal: AbortSignal.timeout(300000),
      });
      if (r.status === 429) { await sleep(15000); continue; }   // plan concurrency limit: wait and retry
      if (!r.ok) throw new Error(`ElevenLabs ${r.status}: ${(await r.text()).slice(0, 300)}`);
      fs.writeFileSync(out, Buffer.from(await r.arrayBuffer()));
      return out;
    } catch (e) {
      if (++errors >= 3) throw e;
    }
  }
  throw new Error('ElevenLabs: still rate-limited after 20 attempts');
}

function ffmpeg(args) {
  const r = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', ...args], { windowsHide: true, encoding: 'utf8' });
  if (r.status !== 0) throw new Error('ffmpeg failed: ' + (r.stderr || '').slice(0, 400));
}
function dur(p) {
  const r = spawnSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
    { windowsHide: true, encoding: 'utf8' });
  return parseFloat((r.stdout || '').trim()) || 0;
}
const master = (src, out) => ffmpeg(['-i', src, '-af', MASTER_CHAIN, '-b:a', CFG.bitrate, out]);

// files joined with `gap` seconds of silence, mono 44.1k, then the master chain
function concatMaster(files, gap, out) {
  if (files.length === 1) return master(files[0], out);
  const args = [];
  files.forEach((f, i) => {
    if (i) args.push('-f', 'lavfi', '-t', String(gap), '-i', 'anullsrc=r=44100:cl=mono');
    args.push('-i', f);
  });
  const n = args.filter(a => a === '-i').length;
  let fc = '';
  for (let i = 0; i < n; i++) fc += `[${i}:a]aformat=sample_rates=44100:channel_layouts=mono[a${i}];`;
  for (let i = 0; i < n; i++) fc += `[a${i}]`;
  fc += `concat=n=${n}:v=0:a=1,${MASTER_CHAIN}[out]`;
  ffmpeg([...args, '-filter_complex', fc, '-map', '[out]', '-b:a', CFG.bitrate, out]);
}

// speech chars per second, pauses excluded; outside the range = truncated/garbled take
function cps(text, seconds) {
  return text.replace(/[֑-ׇ\s]|\[\[[^\]]*\]\]/g, '').length / Math.max(seconds, 0.1);
}
const cpsOk = c => c >= CFG.cps.min && c <= CFG.cps.max;

function niqqud(text, mode = 'lesson') {
  return require(path.join(ROOT, 'tools', 'quiz-app', 'vo.js')).applyLexiconText(text, { mode });
}

// ── lesson rules (Alex 2026-10-05/09, l30/l40) ────────────────────────────────
// Answer letters as alphabet names: raw ד was read "delet", ב "bayit".
//   "ב'?" -> "בֵּית."  (lone letter-question, read flat)   "וד'?" -> "דָּלֶת." (ו dropped)
//   "וג'," / "ב ו-ג" -> "וגם גִּימֶל"   "ב:" -> "בֵּית:"
const LETTER_NAME = { 'א': 'אָלֶף', 'ב': 'בֵּית', 'ג': 'גִּימֶל', 'ד': 'דָּלֶת' };
const LETTER_RE = /(?<![א-ת֑-ׇ])(ו?)([אבגד])([:'׳])(\??)(?![א-ת])/g;
const PAIR_RE = /(?<![א-ת֑-ׇ])([אבגד])['׳]? ו-?([אבגד])['׳]?(?![א-ת])/g;
// 3s pause after "התשובה הנכונה היא": split there, TTS each piece, join with silence
const ANSWER_SPLIT = /(?<=התשובה הנכונה היא)\s*/;

function letterNames(t) {
  return t
    .replace(PAIR_RE, (_, a, b) => LETTER_NAME[a] + ' וגם ' + LETTER_NAME[b])
    .replace(LETTER_RE, (_, pre, ch, mark, q) => {
      const name = LETTER_NAME[ch];
      if (q) return name + '.';
      if (mark === ':') return name + ':';
      return (pre ? 'וגם ' : '') + name;
    });
}
function lessonPieces(t) {
  return t.split(ANSWER_SPLIT).filter(p => p.trim()).map(p => niqqud(letterNames(p)));
}

function sections(vo) {
  const out = []; let sid = null, buf = [];
  for (const ln of fs.readFileSync(vo, 'utf8').split(/\r?\n/)) {
    const m = ln.match(/^##\s*(\S+)/);
    if (m) { if (sid) out.push([sid, buf.join(' ').trim()]); sid = m[1]; buf = []; }
    else if (ln.trim()) buf.push(ln.trim());
  }
  if (sid) out.push([sid, buf.join(' ').trim()]);
  return out;
}

// cache key format is "<model>|<text>" in raw/<sid>.txt (same as the former el_tts.py,
// so segments voiced before the move are not re-voiced)
async function segments(vo, aud, { plain = false, model } = {}) {
  model = model || process.env.ELEVENLABS_MODEL ||
    (plain && /(^|[\\/])l11([\\/]|$)/.test(path.resolve(vo)) ? CFG.models['11'] : modelFor());
  const PAUSE = CFG.pauseSeconds.lessonAnswer;
  const raw = path.join(aud, 'raw'); fs.mkdirSync(raw, { recursive: true });
  const jobs = sections(vo).map(([sid, t]) => [sid, plain ? [niqqud(t)] : lessonPieces(t)]);
  async function one([sid, parts]) {
    const text = parts.join(` [[${PAUSE}s]] `);
    const seg = path.join(aud, `seg_${sid}.mp3`), key = path.join(raw, sid + '.txt');
    const stamp = model + '|' + text;
    if (fs.existsSync(seg)) {
      if (fs.existsSync(key) && fs.readFileSync(key, 'utf8') === stamp) return `${sid} ${dur(seg).toFixed(1)}s cached`;
      // l11 segments voiced before keys existed: keep them when the length is plausible
      if (plain && !fs.existsSync(key) && cpsOk(cps(text, dur(seg)))) { fs.writeFileSync(key, stamp); return `${sid} ${dur(seg).toFixed(1)}s kept`; }
    }
    const rps = parts.map((_, i) => path.join(raw, `${sid}_${i}.mp3`));
    for (let i = 0; i < parts.length; i++) {
      try { await synth(parts[i], rps[i], { model }); } catch (e) { throw new Error(`${sid}: ${e.message}`); }
    }
    concatMaster(rps, PAUSE, seg);
    const d = dur(seg), c = cps(text, d - PAUSE * (parts.length - 1));
    if (!cpsOk(c)) throw new Error(`${sid}: suspicious length ${d.toFixed(1)}s (${c.toFixed(1)} chars/s)`);
    fs.writeFileSync(key, stamp);
    return `${sid} ${d.toFixed(1)}s ${c.toFixed(1)} cps`;
  }
  // 3 at a time, results printed in section order
  const results = new Array(jobs.length); let next = 0;
  await Promise.all([0, 1, 2].map(async () => {
    while (next < jobs.length) { const i = next++; results[i] = await one(jobs[i]); }
  }));
  results.forEach(r => console.log(r));
}

// [[PAUSE]]-split text -> one mastered file (editor preview, ad-hoc lines)
async function say(text, out, { license, gap = CFG.pauseSeconds.question } = {}) {
  const model = modelFor(license);
  const parts = text.split('[[PAUSE]]').map(s => s.trim()).filter(Boolean);
  const tmp = parts.map((_, i) => `${out}.part${i}.mp3`);
  await Promise.all(parts.map((p, i) => synth(p, tmp[i], { model })));
  concatMaster(tmp, gap, out);
  tmp.forEach(f => fs.rmSync(f, { force: true }));
  return out;
}

// question audio for update-question.js --audio: same split as publisher precomputeVoiceoverTiming
async function questionAudio(nums, { license = 11, storedVo = false, outDir }) {
  const { buildVoiceover } = require(path.join(ROOT, 'tools', 'quiz-app', 'vo.js'));
  const bank = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', `l${license}.json`), 'utf8'));
  fs.mkdirSync(outDir, { recursive: true });
  const model = modelFor(license);
  for (const n of nums) {
    const q = bank.find(x => String(x.num) === String(n));
    if (!q) throw new Error(`question ${n} not in data/l${license}.json`);
    const vo = storedVo && q.voiceover_text ? q.voiceover_text : buildVoiceover(q);
    const parts = vo.split('[[PAUSE]]').map(s => s.trim()).filter(Boolean);
    if (parts.length < 2) throw new Error(`Q${n}: VO has no [[PAUSE]]`);
    const texts = { q: parts[0], a: parts.slice(1).join('. ') };
    for (const [k, t] of Object.entries(texts)) {
      const out = path.join(outDir, `${n}_${k}.mp3`), rawf = out + '.raw.mp3';
      await synth(t, rawf, { model }); master(rawf, out); fs.rmSync(rawf, { force: true });
      const c = cps(t, dur(out));
      if (!cpsOk(c)) throw new Error(`Q${n}_${k}: suspicious length (${c.toFixed(1)} chars/s)`);
    }
    console.log(`Q${n} ${model} -> ${path.relative(ROOT, outDir)}`);
  }
}

module.exports = { CFG, MASTER_CHAIN, modelFor, synth, master, concatMaster, dur, cps, cpsOk, niqqud, letterNames, lessonPieces, sections, segments, say, questionAudio };

if (require.main === module) {
  const [cmd, ...a] = process.argv.slice(2);
  const opt = n => { const i = a.indexOf(n); return i !== -1 ? a[i + 1] : undefined; };
  const pos = a.filter((x, i) => !x.startsWith('--') && !(i && ['--model', '--license', '--out'].includes(a[i - 1])));
  const jobs = {
    segments: () => segments(pos[0], pos[1], { plain: a.includes('--plain'), model: opt('--model') }),
    say: () => say(pos[0].startsWith('@') ? fs.readFileSync(pos[0].slice(1), 'utf8') : pos[0], pos[1], { license: opt('--license') }),
    question: () => questionAudio(pos, { license: parseInt(opt('--license') || '11', 10), storedVo: a.includes('--stored-vo'),
      outDir: opt('--out') || path.join(ROOT, 'output', 'voice-v2', 'q') }),
    master: async () => master(pos[0], pos[1]),
  };
  if (!jobs[cmd]) { console.log(fs.readFileSync(__filename, 'utf8').split('\n').slice(1, 16).map(l => l.replace(/^\/\/ ?/, '')).join('\n')); process.exit(cmd ? 1 : 0); }
  jobs[cmd]().catch(e => { console.error('ABORT ' + e.message); process.exit(1); });
}
