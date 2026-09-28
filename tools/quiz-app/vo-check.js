#!/usr/bin/env node
// vo-check.js — pronunciation check BEFORE render, on the new words only.
//
//   node tools/quiz-app/vo-check.js <num> [num...] [--license N]   list new words + short mp3
//   node tools/quiz-app/vo-check.js --approve <num> [--license N]   mark that question's new words OK
//   node tools/quiz-app/vo-check.js --approve-words w1 w2 ...       mark specific words OK
//   node tools/quiz-app/vo-check.js --seed                          seed from approved_for_publish questions
//
// A word is "new" when the VO (exactly as buildVoiceover renders it) leaves it without
// niqqud (so the lexicon did not cover it) AND it is not in references/vo-approved-words.txt.
// For each new word the clip reads the phrase around it, so Alex listens ~10s instead of
// the whole video. A wrong word gets fixed in the lexicon (vo-editor), never here.

const fs = require('fs');
const path = require('path');
const { buildVoiceover } = require('./vo.js');
const { paths, parseLicense } = require('./paths');

const ROOT = path.resolve(__dirname, '..', '..');
const APPROVED = path.join(ROOT, 'references', 'vo-approved-words.txt');
const OUT = path.join(ROOT, 'output', 'vo-check');
const RENDER_URL = process.env.RENDER_URL || 'https://skipper-quiz-publisher-production.up.railway.app';

const args = process.argv.slice(2);
const LICENSE = parseLicense(args);
const li = args.indexOf('--license');
const nums = args.filter((a, i) => /^\d+$/.test(a) && !(li !== -1 && i === li + 1));

const MARKS = /[֑-ׇ]/;
const plain = w => w.replace(/[֑-ׇ]/g, '');
// Hebrew word tokens with their position; geresh/gershayim stay inside the word
const tokens = text => [...text.matchAll(/[א-ת֑-ׇ'"׳״]+/g)]
  .map(m => ({ raw: m[0].replace(/^['"׳״]+|['"׳״]+$/g, ''), index: m.index }))
  .filter(t => /[א-ת]/.test(t.raw));

function loadApproved() {
  try { return new Set(fs.readFileSync(APPROVED, 'utf8').split(/\r?\n/).map(s => s.trim()).filter(Boolean)); }
  catch { return new Set(); }
}
function saveApproved(set) {
  fs.writeFileSync(APPROVED, [...set].sort((a, b) => a.localeCompare(b, 'he')).join('\n') + '\n');
}
function bank(license) { return JSON.parse(fs.readFileSync(paths(license).bank, 'utf8')); }
function voOf(q) { return buildVoiceover(q).replace(/\[\[PAUSE\]\]/g, ' '); }

function newWords(q, approved) {
  const text = voOf(q);
  const seen = new Map();
  for (const t of tokens(text)) {
    if (MARKS.test(t.raw)) continue;           // lexicon (or Alex) vocalised it
    const w = plain(t.raw);
    if (approved.has(w) || seen.has(w)) continue;
    // phrase context: 2 words before, the word, 2 after
    const before = text.slice(0, t.index).split(/\s+/).slice(-3).join(' ');
    const after = text.slice(t.index).split(/\s+/).slice(0, 3).join(' ');
    seen.set(w, (before + ' ' + after).replace(/\s+/g, ' ').replace(/[.:,]+$/, '').trim());
  }
  return seen;
}

async function tts(text, file) {
  const res = await fetch(`${RENDER_URL}/tts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
  if (!res.ok) throw new Error(`TTS HTTP ${res.status}`);
  fs.writeFileSync(file, Buffer.from(await res.arrayBuffer()));
}

async function main() {
  const approved = loadApproved();

  if (args.includes('--seed')) {
    // every VO Alex already approved for publish counts as heard and accepted
    const before = approved.size;
    for (const lic of JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'manifest.json'), 'utf8'))) {
      for (const q of bank(lic)) {
        if (!q.approved_for_publish) continue;
        for (const t of tokens(voOf(q))) if (!MARKS.test(t.raw)) approved.add(plain(t.raw));
      }
    }
    saveApproved(approved);
    console.log(`seeded ${approved.size - before} words (total ${approved.size})`);
    return;
  }
  if (args.includes('--approve-words')) {
    const ws = args.slice(args.indexOf('--approve-words') + 1).filter(a => !a.startsWith('--')).map(plain);
    ws.forEach(w => approved.add(w));
    saveApproved(approved);
    console.log(`approved: ${ws.join(' ')}`);
    return;
  }
  if (!nums.length) { console.error('usage: vo-check.js <num...> [--license N] | --approve <num> | --approve-words w... | --seed'); process.exit(1); }

  const all = bank(LICENSE);
  const approveMode = args.includes('--approve');
  fs.mkdirSync(OUT, { recursive: true });
  for (const num of nums) {
    const q = all.find(x => String(x.num) === num);
    if (!q) { console.error(`! ${num} not in l${LICENSE}`); continue; }
    const words = newWords(q, approved);
    if (approveMode) {
      for (const w of words.keys()) approved.add(w);
      saveApproved(approved);
      console.log(`${num}: approved ${words.size} words`);
      continue;
    }
    if (!words.size) { console.log(`${num}: אין מילים חדשות, אפשר לרנדר`); continue; }
    const list = [...words].map(([w, ctx], i) => `${i + 1}. ${w}  |  ${ctx}`);
    const txt = path.join(OUT, `q${num}_l${LICENSE}_words.txt`);
    fs.writeFileSync(txt, list.join('\n') + '\n');
    console.log(`${num}: ${words.size} מילים חדשות\n${list.join('\n')}`);
    // one clip: each phrase separated by a pause so the words are easy to tell apart
    const mp3 = path.join(OUT, `q${num}_l${LICENSE}_words.mp3`);
    try { await tts([...words.values()].join('. \n'), mp3); console.log(`clip: ${mp3}`); }
    catch (e) { console.log(`clip FAIL: ${e.message}`); }
  }
}

module.exports = { newWords, loadApproved };
if (require.main === module) main();
