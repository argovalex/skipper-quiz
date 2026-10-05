// publish_video.js — publish an already-rendered local video (output/videos/q<num>.mp4,
// from video/make_question_video.py) by uploading it to R2 and firing the same
// Make.com webhook the production auto-publish scheduler uses (payload shape and
// caption format mirrored from argovalex/skipper-quiz-publisher's publishDueQuestions
// / buildPublishCaption — see docs/video-pipeline.md).
//
// This is a manual "publish now" path, independent of that scheduler: it does not
// touch approved_for_publish/scheduled_date or any publish-log, so it can't collide
// with the scheduler's own bookkeeping.
//
//     node tools/publish_video.js <num> [--license 11] [--dry-run]
const fs = require('fs');
const path = require('path');
const { uploadToR2 } = require('./r2_upload');

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
const MAKE_WEBHOOK_URL = process.env.MAKE_WEBHOOK_URL || 'https://hook.eu1.make.com/deu5m0qyc6xndo7nhd6noioi9gnwc4yr';

function loadQuestion(num, license) {
  const bank = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', `l${license}.json`), 'utf8'));
  const arr = Array.isArray(bank) ? bank : (bank.questions || Object.values(bank).find(v => Array.isArray(v)));
  const q = arr.find(q => q.num === Number(num));
  if (!q) throw new Error(`Q#${num} not found in data/l${license}.json`);
  return q;
}

// Based on buildPublishCaption() in argovalex/skipper-quiz-publisher/index.js, plus a
// CTA block driving to the marketing site — not in the scheduler's original, so the
// two have diverged. The caption is editable in publish-review.html before publish;
// this default CTA is a starting point, not fixed copy — tailor it per post there.
function buildPublishCaption(q) {
  // Engagement-first caption (Alex 2026-10-05, replaces the 2026-09-16 pinned copy):
  // hook → question → options → ask for a comment. The answer/explanation are NOT in
  // the caption (the video reveals them) so viewers have a reason to comment; the
  // sales CTA moves to the end. Reel captions have no clickable links → "לינק בפרופיל".
  const opts = (q.options || []).map(o => o.replace(/^[אבגד]\.\s*/, '').trim());
  const optLines = ['א', 'ב', 'ג', 'ד'].map((l, i) => `${l}. ${opts[i] || ''}`).join('\n');
  const HOOKS = [
    '🚤 רוב הנבחנים טועים בשאלה הזאת. אתה?',
    '⚠️ שאלת מלכודת מהמבחן העיוני. תענה לפני שאתה ממשיך לגלול.',
    '🤔 10 שניות. יודע את התשובה?',
    '🎯 בדוק את עצמך: שאלה אמיתית ממבחן רישיון אופנוע ים.'
  ];
  const hook = HOOKS[(Number(q.num) || 0) % HOOKS.length];
  const ask = '👇 כתבו בתגובות א / ב / ג / ד לפני שהסרטון חושף את התשובה';
  const cta = '🎓 עוד מאות שאלות כאלה בתרגול חינם, בלי הרשמה. לינק בפרופיל | alargov.com\nהקורס המלא: לא עברת? לא שילמת.';
  const hashtags = '#רישיון_אופנוע_ים #אופנוע_ים #רישיון_שייט #SkipperQuiz';
  return `${hook}\n\n❓ ${q.q_he || ''}\n\n${optLines}\n\n${ask}\n\n${cta}\n\n${hashtags}`;
}

// Text for an optional pinned comment (Make: Facebook "Create a Comment" step).
function buildAnswerComment(q) {
  const idx = { 'א': 0, 'ב': 1, 'ג': 2, 'ד': 3 }[(q.answer || 'א').trim()] ?? 0;
  const ans = ((q.options || [])[idx] || '').replace(/^[אבגד]\.\s*/, '').trim();
  return `✅ התשובה: ${['א','ב','ג','ד'][idx]}. ${ans}\n\n💡 ${q.explanation || ''}`;
}

function localVideoPath(num) {
  return path.join(ROOT, 'output', 'videos', `q${num}.mp4`);
}

// Builds the title/caption for review, without uploading or publishing anything.
function buildPreview(num, license) {
  const q = loadQuestion(num, license);
  const localPath = localVideoPath(num);
  return {
    num: q.num,
    license: Number(license),
    topic: q.topic || '',
    q_he: q.q_he || '',
    answer: q.answer || '',
    rendered: fs.existsSync(localPath),
    videoPath: `/output/videos/q${num}.mp4`,
    // גיבוי: שאלות שפורסמו דרך שרת ה-Railway (לא הצינור המקומי) מעולם לא
    // קיבלו קובץ ב-output/videos/ — ה-videoUrl (Cloudinary) השמור בבנק הוא
    // הדרך היחידה להציג אותן כאן, למשל כשמגיעים מקישור "צפה" ב-monitor.html.
    remoteVideoUrl: q.videoUrl || '',
    title: `SkipperQuiz — ${q.topic} שאלה #${q.num}`,
    caption: buildPublishCaption(q)
  };
}

async function publishVideo(num, license, { dryRun = false, caption, title } = {}) {
  const q = loadQuestion(num, license);
  const localPath = localVideoPath(num);
  if (!fs.existsSync(localPath)) throw new Error(`Not rendered: ${localPath} (run video.make_question_video first)`);

  console.log(`[Q${num}] uploading to R2...`);
  const videoUrl = dryRun
    ? '<dry-run: would upload>'
    : await uploadToR2(localPath, `videos/l${license}/q${num}.mp4`);
  console.log(`[Q${num}] videoUrl: ${videoUrl}`);

  const payload = {
    videoUrl,
    title: title || `SkipperQuiz — ${q.topic} שאלה #${q.num}`,
    caption: caption || buildPublishCaption(q),
    topic: q.topic || '',
    questionNum: q.num,
    date: new Date().toISOString()
  };

  if (dryRun) {
    console.log('[dry-run] payload:', JSON.stringify(payload, null, 2));
    return payload;
  }

  console.log(`[Q${num}] posting to Make.com...`);
  const res = await fetch(MAKE_WEBHOOK_URL, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error(`Make.com webhook failed: ${res.status} ${await res.text()}`);
  console.log(`[Q${num}] published — Make.com triggered.`);
  return payload;
}

module.exports = { publishVideo, buildPublishCaption, buildAnswerComment, buildPreview };

if (require.main === module) {
  const args = process.argv.slice(2);
  const num = args.find(a => !a.startsWith('--'));
  const licenseIdx = args.indexOf('--license');
  const license = licenseIdx >= 0 ? args[licenseIdx + 1] : '11';
  const dryRun = args.includes('--dry-run');
  if (!num) {
    console.error('usage: node tools/publish_video.js <num> [--license 11] [--dry-run]');
    process.exit(1);
  }
  publishVideo(num, license, { dryRun }).catch(e => {
    // fetch()'s own error message is always the unhelpful generic "fetch failed" —
    // the real reason (DNS, TLS, ECONNRESET, IPv6 routing...) is on e.cause.
    console.error(e.message, e.cause ? `\ncause: ${e.cause}` : '');
    process.exit(1);
  });
}
