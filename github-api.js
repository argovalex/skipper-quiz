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

// Pushes the in-memory `questions` array (global in each tool) to questions.json.
async function saveQuestionsGH(msg) {
  const result = await ghPutFile('questions.json', JSON.stringify(questions, null, 2), msg || 'update: questions');
  if (typeof questionsSHA !== 'undefined') questionsSHA = result.sha;
  return result.ok;
}

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
