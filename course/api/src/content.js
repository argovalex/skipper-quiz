// Loads the canonical bank (data/l11.json) and shapes it into lessons.
// Source of truth stays data/l11.json. Local file first for dev; remote for prod.
// Every edit Alex makes propagates on next reload (POST /api/admin/reload) or restart.
const fs = require('fs');
const path = require('path');
const db = require('./db');

const DATA_URL = process.env.DATA_URL ||
  'https://raw.githubusercontent.com/argovalex/skipper-quiz/main/data/l11.json';
const LOCAL = path.join(__dirname, '..', '..', '..', 'data', 'l11.json');

const L2I = { 'א': 0, 'ב': 1, 'ג': 2, 'ד': 3 };
const cleanOpt = o => String(o).replace(/^[אבגד][.)]\s*/, '').trim();
const FIRST_AID = new Set([1108, 1109, 1110, 1111, 1113, 1114]);

const TITLES = {
  '1': 'כללי וחוקים', '2': 'אזורי שיט', '3': 'זכות מעבר', '4': 'אותות קוליים',
  '5': 'סימני יום', '6': 'דגלים', '7': 'אותות מצוקה', '8': 'מזג אוויר',
  '9': 'ניווט וכניסה לנמל', '10': 'סכנות רכיבה ותמרון', '11': 'תמרוני ספינה',
  '12': 'עזרה ראשונה', '13': 'בטיחות: אש ותדלוק',
};

function pauseRatio(vo) {
  vo = vo || '';
  if (!vo.includes('[[PAUSE]]')) return null;
  const i = vo.indexOf('[[PAUSE]]');
  const before = vo.slice(0, i).replace(/\[\[PAUSE\]\]/g, ' ').trim();
  const full = vo.replace(/\[\[PAUSE\]\]/g, ' ').trim();
  return full ? Math.round((before.length / full.length) * 1000) / 1000 : null;
}

function pack(q) {
  const o = {
    num: q.num,
    q: q.q_he,
    opts: (q.options || []).map(cleanOpt),
    c: L2I[q.answer] ?? 0,
    exp: q.explanation || '',
    vid: q.videoUrl || '',
  };
  const p = pauseRatio(q.voiceover_text);
  if (p != null) o.p = p;
  return o;
}

function buildLessons(raw) {
  const by = {};
  for (const q of raw) (by[q.topic] = by[q.topic] || []).push(q);
  const g = t => by[t] || [];
  const daySigns = g('זכות מעבר').filter(x => /תמונה\s*(7\d|8\d|9\d)/.test(x.q_he || ''));
  const map = {
    '1': [...g('אופנוע ים - כללי'), ...g('חוקים ותקנות')],
    '2': g('אזורי שיט'),
    '3': g('זכות מעבר'),
    '4': g('אותות קוליים'),
    '5': daySigns,
    '6': g('דגלים'),
    '7': g('אותות מצוקה'),
    '8': g('מזג אוויר'),
    '9': [...g('ניווט'), ...g('כניסה לנמל')],
    '10': g('סכנות רכיבה ותמרון'),
    '11': g('תמרוני ספינה'),
    '12': g('בטיחות').filter(x => FIRST_AID.has(x.num)),
    '13': g('בטיחות').filter(x => !FIRST_AID.has(x.num)),
  };
  const lessons = {};
  for (const id of Object.keys(map)) {
    lessons[id] = { id, title: TITLES[id] || id, questions: map[id].map(pack) };
  }
  return lessons;
}

let cache = { at: 0, lessons: null };
const TTL = 5 * 60 * 1000;

async function readRaw() {
  // Private source: serve the bank from Postgres, decoupled from the public repo URL.
  if (process.env.DATA_SOURCE === 'db' && db.hasDb()) {
    const r = await db.q('select data from bank');
    if (r.rows.length) return r.rows.map(x => x.data);
    console.warn('content: DATA_SOURCE=db but bank is empty — run `node admin.js bank import`');
  }
  const preferLocal = !process.env.FORCE_REMOTE && fs.existsSync(LOCAL);
  if (preferLocal) {
    try { return JSON.parse(fs.readFileSync(LOCAL, 'utf8')); }
    catch (e) { console.warn('content: local read failed (' + e.message + '), trying remote'); }
  }
  try {
    const res = await fetch(DATA_URL);
    if (!res.ok) throw new Error('HTTP ' + res.status);
    return await res.json();
  } catch (e) {
    if (fs.existsSync(LOCAL)) {
      console.warn('content: remote failed (' + e.message + '), using local');
      return JSON.parse(fs.readFileSync(LOCAL, 'utf8'));
    }
    throw e;
  }
}

async function load(force) {
  if (!force && cache.lessons && Date.now() - cache.at < TTL) return cache.lessons;
  cache = { at: Date.now(), lessons: buildLessons(await readRaw()) };
  return cache.lessons;
}

// Free window: the first question of each of the 13 topics — one sample per type.
// A fixed deterministic set (identical for everyone, every time), so re-registering
// with a new email never yields different questions — no farming the whole bank.
function freeSubset(lessons) {
  const out = {};
  for (let i = 1; i <= 13; i++) {
    const l = lessons[String(i)];
    if (l && l.questions.length) {
      out[String(i)] = { id: l.id, title: l.title, questions: [l.questions[0]] };
    }
  }
  return out;
}

// Raw canonical array (data/l11.json) from local/remote — bypasses the DB source.
// Used by the admin bank-import endpoint to seed/refresh Postgres from the repo.
async function fetchCanonical() {
  const preferLocal = !process.env.FORCE_REMOTE && fs.existsSync(LOCAL);
  if (preferLocal) {
    try { return JSON.parse(fs.readFileSync(LOCAL, 'utf8')); }
    catch (e) { console.warn('fetchCanonical: local read failed (' + e.message + '), trying remote'); }
  }
  const res = await fetch(DATA_URL, { cache: 'no-store' });
  if (!res.ok) throw new Error('HTTP ' + res.status);
  return await res.json();
}

module.exports = { load, freeSubset, fetchCanonical };
