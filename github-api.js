// Shared GitHub Contents API read-modify-write helpers.
// Used by index.html, queue.html and fix-requests.html instead of each
// keeping its own copy of the fetch-sha → base64-encode → PUT sequence.
const REPO = 'argovalex/skipper-quiz';

// ── Per-license bank ("שאלון" per file) ───────────────────────────────────────
// The question bank is stored one file per license under data/ (data/l11.json,
// data/l30.json, ...). questions.json is kept only as a DERIVED compat artifact
// for legacy readers (publisher, video generators). data/manifest.json lists the
// licenses so a new quiz is just a new file + a manifest entry, no code change.
const BANK_DIR = 'data';
const LICENSE_ORDER = ['30', '11'];          // canonical order; new quizzes appended
function bankPath(lic) { return `${BANK_DIR}/l${lic}.json`; }
function licenseOf(q) { return String(q.license ?? '30'); }
// Byte-identical to the Python canonical dump: 2-space indent, unicode preserved,
// CRLF line endings, no trailing newline. Verified equal for both files + rebuild.
function dumpCanonical(obj) { return JSON.stringify(obj, null, 2).replace(/\n/g, '\r\n'); }
// Orders licenses canonically (known first, then any extras sorted) so the
// rebuilt questions.json stays stable regardless of in-memory order.
function orderLicenses(lics) {
  const set = new Set(lics.map(String));
  const known = LICENSE_ORDER.filter(l => set.has(l));
  const extra = [...set].filter(l => !LICENSE_ORDER.includes(l)).sort();
  return [...known, ...extra];
}
// Per-license sha + last-loaded canonical snapshot, so a save writes only the
// files that actually changed and guards each against remote clobber.
const bankState = { shas: {}, snaps: {}, licenses: LICENSE_ORDER.slice() };

function ghNotify(msg) {
  const fn = (typeof toast === 'function') ? toast : (typeof showToast === 'function') ? showToast : null;
  if (fn) fn(msg);
}

async function ghGetFile(path) {
  const token = getToken();
  if (!token) return null;
  try {
    const res = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}`,
      { headers: { Authorization: `Bearer ${token}` } });
    if (!res.ok) return null;
    return await res.json();
  } catch { return null; }
}

// `expectedSha` is the sha the caller last saw for this file (from its own
// load/save). Passing it lets GitHub reject the write with 409 if the file
// changed remotely since then. Omitting it falls back to fetching a fresh
// sha right before writing — that always "succeeds" even when the file
// diverged in the meantime, which is how a stale tab can silently clobber
// newer remote changes. Callers that track a sha (questions.json) MUST pass it.
// `strict` (used for the per-license bank files) means: if the sha we were
// given no longer matches, DO NOT re-fetch and overwrite — bubble the conflict
// up so the caller can tell the user to refresh. Without it (html/ files and
// the derived questions.json compat artifact) a 409 falls back to last-writer-
// wins, which is what we want for generated/append-only files.
async function ghPutFile(path, content, message, expectedSha, strict) {
  const token = getToken();
  if (!token) { ghNotify('⚠ הגדר GitHub Token'); return { ok: false }; }
  try {
    let sha = expectedSha;
    if (sha == null) {
      const existing = await ghGetFile(path);
      sha = existing?.sha;
    }
    const encoded = btoa(unescape(encodeURIComponent(content)));
    const res = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, content: encoded, ...(sha ? { sha } : {}) })
    });
    if (res.status === 409) {
      if (strict) return { ok: false, conflict: true };  // caller must refresh, never clobber
      // SHA mismatch - fetch fresh SHA and retry once
      const fresh = await ghGetFile(path);
      if (fresh?.sha) {
        const retry = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}`, {
          method: 'PUT',
          headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
          body: JSON.stringify({ message, content: encoded, sha: fresh.sha })
        });
        if (retry.ok) { const b = await retry.json(); return { ok: true, sha: b.content?.sha }; }
      }
      return { ok: false, conflict: true };
    }
    if (!res.ok) {
      const errBody = await res.text().catch(() => '');
      console.error(`[ghPutFile] ${res.status} ${res.statusText} — ${errBody}`);
      ghNotify(`❌ GitHub ${res.status}: ${res.statusText}`);
      return { ok: false };
    }
    const body = await res.json();
    return { ok: true, sha: body.content?.sha };
  } catch (e) { ghNotify('❌ שמירה נכשלה: ' + e.message); return { ok: false }; }
}

// ── Local cache + offline queue ────────────────────────────────────────────
// GitHub is the single source of truth for questions.json; this cache exists
// only so every tool keeps working (read AND write) when there's no network,
// and syncs back to GitHub automatically once the connection returns.
const QUESTIONS_CACHE_KEY = 'sq_questions_cache';
const PENDING_SAVE_KEY = 'sq_pending_save';

function cacheQuestions(data, sha) {
  try { localStorage.setItem(QUESTIONS_CACHE_KEY, JSON.stringify({ data, sha, cachedAt: Date.now() })); } catch {}
}
function readQuestionsCache() {
  try { return JSON.parse(localStorage.getItem(QUESTIONS_CACHE_KEY) || 'null'); } catch { return null; }
}

// Loads questions.json from GitHub; falls back to the last cached copy when
// offline (or no token) so the tool stays usable without network.
async function loadQuestionsCached() {
  const file = await ghGetFile('questions.json');
  if (file) {
    try {
      const raw = atob(file.content.replace(/\n/g, ''));
      const data = JSON.parse(new TextDecoder('utf-8').decode(Uint8Array.from(raw, c => c.charCodeAt(0))));
      if (!Array.isArray(data)) throw new Error('questions.json on GitHub is not an array');
      cacheQuestions(data, file.sha);
      return { data, sha: file.sha, offline: false };
    } catch (e) {
      // Corrupted/malformed content on GitHub — fall through to the local
      // cache instead of crashing the caller with an uncaught parse error.
      ghNotify('⚠ questions.json ב-GitHub פגום — עובד מהעותק האחרון שנשמר');
    }
  }
  const cached = readQuestionsCache();
  if (cached) {
    ghNotify('⚠ אין חיבור ל-GitHub — עובד מהעותק האחרון שנשמר במכשיר');
    return { data: cached.data, sha: cached.sha, offline: true };
  }
  return { data: [], sha: null, offline: true };
}

// Decodes a GitHub Contents API file blob (base64 + utf-8) to a JS value.
function ghDecodeJSON(file) {
  const raw = atob(file.content.replace(/\n/g, ''));
  return JSON.parse(new TextDecoder('utf-8').decode(Uint8Array.from(raw, c => c.charCodeAt(0))));
}

// Loads the per-license bank files into one flat `questions`-shaped array, and
// records each file's sha + snapshot in bankState for guarded, minimal saves.
// Falls back to the legacy monolithic questions.json (pre-split, or offline).
async function loadBank() {
  let lics = LICENSE_ORDER.slice();
  const man = await ghGetFile(`${BANK_DIR}/manifest.json`);
  if (man) {
    try { const arr = ghDecodeJSON(man); if (Array.isArray(arr) && arr.length) lics = arr.map(String); }
    catch { /* bad manifest — fall back to the built-in order */ }
  }
  const buckets = {};
  let anyFile = false;
  for (const lic of lics) {
    const file = await ghGetFile(bankPath(lic));
    if (!file) continue;
    try {
      const arr = ghDecodeJSON(file);
      if (!Array.isArray(arr)) throw new Error('not an array');
      buckets[lic] = arr;
      bankState.shas[lic] = file.sha;
      bankState.snaps[lic] = dumpCanonical(arr);
      anyFile = true;
    } catch { ghNotify(`⚠ data/l${lic}.json פגום — דלגתי עליו`); }
  }
  if (anyFile) {
    bankState.licenses = orderLicenses(lics);
    const data = [];
    for (const lic of bankState.licenses) if (buckets[lic]) data.push(...buckets[lic]);
    cacheQuestions(data, null);
    return { data, offline: false };
  }
  // No per-license files reachable (offline, no token, or pre-split repo):
  // fall back to the monolithic loader so the tool still works.
  const legacy = await loadQuestionsCached();
  return { data: legacy.data, offline: legacy.offline };
}

// Pushes the in-memory `questions` array (global in each tool) to questions.json.
// If the write fails (offline, no token, conflict), the change is kept in the
// local cache and queued so flushPendingSave() can retry once back online —
// the tool keeps working, it just hasn't reached GitHub yet.
// Partitions the in-memory `questions` array by license and writes only the
// per-license file(s) that actually changed, each guarded by the sha we last
// saw (strict: a remote change makes the save fail loudly instead of clobbering
// a parallel edit — e.g. license 30 can never be overwritten by a license 11
// save). Then regenerates the derived questions.json + manifest for legacy
// readers. Offline/error paths keep the local cache + retry queue behaviour.
async function saveQuestionsGH(msg) {
  const message = msg || 'update: questions';
  const present = orderLicenses([...new Set(questions.map(licenseOf))]);
  const buckets = {};
  for (const lic of present) buckets[lic] = [];
  for (const q of questions) buckets[licenseOf(q)].push(q);

  const queueForRetry = () => {
    cacheQuestions(questions, null);
    try { localStorage.setItem(PENDING_SAVE_KEY, JSON.stringify({ message, queuedAt: Date.now() })); } catch {}
    ghNotify('⚠ אין חיבור — נשמר מקומית, יסונכרן עם GitHub כשהרשת תחזור');
  };

  let wroteAny = false;
  for (const lic of present) {
    const serial = dumpCanonical(buckets[lic]);
    if (bankState.snaps[lic] === serial) continue;              // unchanged → skip
    const res = await ghPutFile(bankPath(lic), serial, `${message} [L${lic}]`, bankState.shas[lic], true);
    if (res.conflict) {
      ghNotify(`⚠ שאלון ${lic} עודכן במקום אחר — רענן (F5) ובצע את השינוי שוב`);
      return false;                                             // never clobber
    }
    if (!res.ok) { queueForRetry(); return false; }
    bankState.shas[lic] = res.sha;
    bankState.snaps[lic] = serial;
    wroteAny = true;
  }

  if (!wroteAny) { localStorage.removeItem(PENDING_SAVE_KEY); return true; }

  // Derived artifacts for legacy consumers — last-writer-wins is correct here.
  const combined = [];
  for (const lic of present) combined.push(...buckets[lic]);
  await ghPutFile('questions.json', dumpCanonical(combined), `${message} [compat]`);
  if (JSON.stringify(present) !== JSON.stringify(bankState.licenses)) {
    await ghPutFile(`${BANK_DIR}/manifest.json`, dumpCanonical(present), `${message} [manifest]`);
    bankState.licenses = present;
  }
  cacheQuestions(questions, null);
  localStorage.removeItem(PENDING_SAVE_KEY);
  return true;
}

// Retries a queued save once network is back. Wired to the 'online' event below
// and should also be called once after the initial load in each tool.
let flushingPendingSave = false;
async function flushPendingSave() {
  if (flushingPendingSave) return;
  let pending;
  try { pending = JSON.parse(localStorage.getItem(PENDING_SAVE_KEY) || 'null'); } catch { pending = null; }
  if (!pending || typeof questions === 'undefined' || !questions.length) return;
  flushingPendingSave = true;
  try {
    // Route through the per-license saver; it clears PENDING_SAVE_KEY on success
    // and re-queues (or reports a conflict) on failure.
    const ok = await saveQuestionsGH(pending.message);
    if (ok) ghNotify('✅ סונכרן עם GitHub');
  } finally {
    flushingPendingSave = false;
  }
}
window.addEventListener('online', flushPendingSave);

// Same write, kept under its legacy name for index.html's approve/unapprove flow.
async function ghPushQuestions() {
  const num = (typeof currentIdx !== 'undefined' && currentIdx >= 0) ? questions[currentIdx]?.num : '';
  return saveQuestionsGH(`approve: Q#${num}`);
}

// Renders q via the shared generateQuizHTML (scenes.js) and pushes it as the
// prebuilt HTML the publisher uses for this question.
async function ghPushHTML(q) {
  const html = generateQuizHTML(q, 'he', true); // autoPlay=true for video recording
  const fname = `quiz_${String(q.num).padStart(3,'0')}_${(q.topic||'quiz').replace(/[\s\/"]/g,'_')}_he.html`;
  const result = await ghPutFile(`html/${fname}`, html, `html: Q#${q.num} ${q.topic}`);
  return result.ok;
}
