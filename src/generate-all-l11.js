// License-aware question-visual generator: `node src/generate-all-l11.js [--license N]`
// (default 11). Filters questions.json by license and writes per-license HTMLs.
const fs = require('fs');
const path = require('path');
const questions = require('../questions.json');
const vm = require('vm');
const { paths, parseLicense } = require('../tools/quiz-app/paths');
const P = paths(parseLicense());

// Load scenes.js in a sandboxed context with browser-like globals
const scenesCode = fs.readFileSync(path.join(__dirname, '..', 'scenes.js'), 'utf8');
const sandbox = {
  console,
  JSON,
  Math,
  parseInt,
  parseFloat,
  String,
  Array,
  Object,
  RegExp,
  Number,
  Date,
  currentLang: 'he',
  document: { getElementById: () => ({ value: '' }) },
  window: {},
};
vm.createContext(sandbox);
vm.runInContext(scenesCode, sandbox);

const outDir = P.htmlDir;
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const list = questions.filter(q => q.license === P.license);
let count = 0;
for (const q of list) {
  try {
    const html = sandbox.generateQuizHTML(q, 'he', true);
    const topic = (q.topic || 'quiz').replace(/[\s\/]/g, '_');
    const fname = `quiz_${String(q.num).padStart(3,'0')}_${topic}_he.html`;
    fs.writeFileSync(path.join(outDir, fname), html, 'utf8');
    count++;
  } catch(e) {
    console.error(`FAIL Q${q.num}: ${e.message}`);
  }
}
console.log(`Done: ${count}/${list.length} license-${P.license} HTMLs generated in ${path.basename(outDir)}/`);
