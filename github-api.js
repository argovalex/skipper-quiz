// Shared GitHub Contents API read-modify-write helpers.
// Used by index.html, queue.html and fix-requests.html instead of each
// keeping its own copy of the fetch-sha → base64-encode → PUT sequence.
const REPO = 'argovalex/skipper-quiz';

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

async function ghPutFile(path, content, message) {
  const token = getToken();
  if (!token) { ghNotify('⚠ הגדר GitHub Token'); return { ok: false }; }
  try {
    const existing = await ghGetFile(path);
    const sha = existing?.sha;
    const encoded = btoa(unescape(encodeURIComponent(content)));
    const res = await fetch(`https://api.github.com/repos/${REPO}/contents/${path}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, content: encoded, ...(sha ? { sha } : {}) })
    });
    return { ok: res.ok, sha };
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
    const raw = atob(file.content.replace(/\n/g, ''));
    const data = JSON.parse(new TextDecoder('utf-8').decode(Uint8Array.from(raw, c => c.charCodeAt(0))));
    cacheQuestions(data, file.sha);
    return { data, sha: file.sha, offline: false };
  }
  const cached = readQuestionsCache();
  if (cached) {
    ghNotify('⚠ אין חיבור ל-GitHub — עובד מהעותק האחרון שנשמר במכשיר');
    return { data: cached.data, sha: cached.sha, offline: true };
  }
  return { data: [], sha: null, offline: true };
}

// Pushes the in-memory `questions` array (global in each tool) to questions.json.
// If the write fails (offline, no token, conflict), the change is kept in the
// local cache and queued so flushPendingSave() can retry once back online —
// the tool keeps working, it just hasn't reached GitHub yet.
async function saveQuestionsGH(msg) {
  const message = msg || 'update: questions';
  const result = await ghPutFile('questions.json', JSON.stringify(questions, null, 2), message);
  if (result.ok) {
    if (typeof questionsSHA !== 'undefined') questionsSHA = result.sha;
    cacheQuestions(questions, result.sha);
    localStorage.removeItem(PENDING_SAVE_KEY);
    return true;
  }
  cacheQuestions(questions, null);
  try { localStorage.setItem(PENDING_SAVE_KEY, JSON.stringify({ message, queuedAt: Date.now() })); } catch {}
  ghNotify('⚠ אין חיבור — נשמר מקומית, יסונכרן עם GitHub כשהרשת תחזור');
  return false;
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
    const result = await ghPutFile('questions.json', JSON.stringify(questions, null, 2), pending.message);
    if (result.ok) {
      if (typeof questionsSHA !== 'undefined') questionsSHA = result.sha;
      cacheQuestions(questions, result.sha);
      localStorage.removeItem(PENDING_SAVE_KEY);
      ghNotify('✅ סונכרן עם GitHub');
    }
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
