// l12 batch writer. Run from repo root:
//   node tools/l12/apply.js <batch.json> [media.json]
// batch.json: { "<num>": { "explanation": "...", "explanation_spoken": "..." } }
// media.json: { "<num>": { "url": "...", "type": "video" } }
// Sets answer_confirmed, voiceover_text = buildVoiceover(q), content_updated_at.
// Writes data/l12.json byte-identical to JSON.stringify(.., 2) with the file's own EOL.
// After this, run tools/l12/fixvo.js on the same nums (Alex's l12 VO rules).
const fs = require('fs'), path = require('path');
const ROOT = process.cwd();
const { buildVoiceover } = require(path.join(ROOT, 'tools/quiz-app/vo.js'));
const F = path.join(ROOT, 'data/l12.json');
const raw = fs.readFileSync(F, 'utf8');
const data = JSON.parse(raw);
const batch = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const media = process.argv[3] ? JSON.parse(fs.readFileSync(process.argv[3], 'utf8')) : {};
const now = new Date().toISOString();
for (const [num, c] of Object.entries(batch)) {
  const q = data.find(x => String(x.num) === num);
  if (!q) throw new Error('missing ' + num);
  if (c.explanation) q.explanation = c.explanation;
  if (c.explanation_spoken) q.explanation_spoken = c.explanation_spoken;
  q.answer_confirmed = true;
  if (media[num]) { q.mediaUrl = media[num].url; q.mediaType = media[num].type; }
  q.voiceover_text = buildVoiceover(q);
  q.content_updated_at = now;
}
let s = JSON.stringify(data, null, 2);
if (raw.includes('\r\n')) s = s.replace(/\n/g, '\r\n');
fs.writeFileSync(F, s);
console.log('updated', Object.keys(batch).join(','));
