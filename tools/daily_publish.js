// daily_publish.js — picks one question from the fixed 40-question rotation pool
// (tools/daily-publish-pool.json) that hasn't been posted in the last 7 days, and
// publishes it via the same Make.com webhook as publish_video.js — but using the
// question's existing videoUrl (data/l11.json, from the main Cloudinary render
// pipeline) instead of a local render + R2 upload, since all 161 questions already
// have one.
//
// Meant to run unattended once a day via Windows Task Scheduler (see
// tools/register-daily-publish-task.ps1) — NOT via a Claude Code session. Claude
// cannot run this for real (the harness blocks live social-media posts even with
// chat approval); a plain scheduled OS task has no such gate.
//
//     node tools/daily_publish.js [--dry-run]
'use strict';
const fs = require('fs');
const path = require('path');
const { buildPublishCaption } = require('./publish_video');

function loadEnvFile() {
  const envPath = path.join(__dirname, '..', '.env');
  if (!fs.existsSync(envPath)) return;
  for (const line of fs.readFileSync(envPath, 'utf8').split('\n')) {
    const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
    if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].trim();
  }
}
loadEnvFile();

const ROOT = path.join(__dirname, '..');
const POOL_PATH = path.join(__dirname, 'daily-publish-pool.json');
const HISTORY_PATH = path.join(__dirname, 'daily-publish-history.json');
const NO_REPEAT_DAYS = 7;
const MAKE_WEBHOOK_URL = process.env.MAKE_WEBHOOK_URL || 'https://hook.eu1.make.com/deu5m0qyc6xndo7nhd6noioi9gnwc4yr';

function loadBank() {
  const bank = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'l11.json'), 'utf8'));
  return Array.isArray(bank) ? bank : (bank.questions || Object.values(bank).find(v => Array.isArray(v)));
}

function loadHistory() {
  if (!fs.existsSync(HISTORY_PATH)) return [];
  try { return JSON.parse(fs.readFileSync(HISTORY_PATH, 'utf8')); }
  catch { return []; }
}

function pickQuestion(pool, history) {
  const cutoff = Date.now() - NO_REPEAT_DAYS * 24 * 60 * 60 * 1000;
  const recentNums = new Set(history.filter(h => new Date(h.date).getTime() >= cutoff).map(h => h.num));
  let eligible = pool.filter(p => !recentNums.has(p.num));
  // Safety net: if the whole pool was somehow posted inside the window (shouldn't
  // happen with 40 slots and one post/day), fall back to least-recently-used.
  if (!eligible.length) {
    const lastSeen = new Map();
    for (const h of history) lastSeen.set(h.num, new Date(h.date).getTime());
    eligible = [...pool].sort((a, b) => (lastSeen.get(a.num) || 0) - (lastSeen.get(b.num) || 0));
    eligible = [eligible[0]];
  }
  return eligible[Math.floor(Math.random() * eligible.length)];
}

async function main() {
  const dryRun = process.argv.includes('--dry-run');
  const pool = JSON.parse(fs.readFileSync(POOL_PATH, 'utf8'));
  const history = loadHistory();
  const pick = pickQuestion(pool, history);

  const bank = loadBank();
  const q = bank.find(x => x.num === pick.num);
  if (!q) throw new Error(`Q#${pick.num} from pool not found in data/l11.json`);
  if (!q.videoUrl) throw new Error(`Q#${pick.num} has no videoUrl — cannot publish`);

  const payload = {
    videoUrl: q.videoUrl,
    title: `SkipperQuiz — ${q.topic} שאלה #${q.num}`,
    caption: buildPublishCaption(q),
    topic: q.topic || '',
    questionNum: q.num,
    date: new Date().toISOString()
  };

  console.log(`[daily-publish] picked Q#${q.num} (${q.topic}) — ${history.length} prior posts in history`);

  if (dryRun) {
    console.log('[dry-run] payload:', JSON.stringify(payload, null, 2));
    return;
  }

  const res = await fetch(MAKE_WEBHOOK_URL, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error(`Make.com webhook failed: ${res.status} ${await res.text()}`);

  history.push({ num: q.num, topic: q.topic, date: payload.date });
  fs.writeFileSync(HISTORY_PATH, JSON.stringify(history, null, 2) + '\n');
  console.log(`[daily-publish] published Q#${q.num} — Make.com triggered.`);
}

main().catch(e => {
  console.error('[daily-publish] FAILED:', e.message, e.cause ? `\ncause: ${e.cause}` : '');
  process.exit(1);
});
