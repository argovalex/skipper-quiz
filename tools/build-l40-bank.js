// Builds data/l40.json from lessons/l40/exam-bank.json: drops duplicate questions, numbers the rest 4001.. in exam order.
const fs = require('fs');
const src = JSON.parse(fs.readFileSync('lessons/l40/exam-bank.json', 'utf8')).questions;
const norm = s => s.replace(/[^\p{L}\p{N}]/gu, '').toLowerCase();
const key = q => norm(q.question) + '|' + q.options.map(norm).sort().join('|');
const L = 'אבגדה';
const seen = new Map(), out = [], dropped = [];
for (const q of src) {
  const k = key(q);
  if (q.duplicate_of || seen.has(k)) { dropped.push([q.id, q.duplicate_of || seen.get(k)]); continue; }
  seen.set(k, q.id);
  out.push({
    num: 4000 + out.length + 1, source: `מבחן ${q.exam} שאלה ${q.num}`, topic: 'GMDSS', q_he: q.question, q_en: '',
    options: q.options.map((o, i) => `${L[i]}. ${o}`), answer: q.answer_letter, answer_confirmed: true,
    explanation: '', approved_for_publish: false, exam_id: q.id,
  });
}
fs.writeFileSync('data/l40.json', JSON.stringify(out, null, 2));
console.log('kept', out.length, 'dropped', dropped.length, JSON.stringify(dropped));
