const fs = require('fs');
const path = require('path');
const questions = require('../questions.json');
const vm = require('vm');

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

const outDir = path.join(__dirname, '..', 'html');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const l11 = questions.filter(q => q.license === 11);
let count = 0;
for (const q of l11) {
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
console.log(`Done: ${count}/${l11.length} license-11 HTMLs generated in html/`);
