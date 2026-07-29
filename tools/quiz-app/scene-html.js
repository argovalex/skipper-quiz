// Shared: produce the exact question visual HTML the editor sends to the render
// server, by running scenes.js's generateQuizHTML in a vm sandbox (same setup as
// src/generate-all-l11.js). Render calls MUST send this as the `html` param —
// without it the server falls back to a generic anchor visual.
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..', '..');
const scenesCode = fs.readFileSync(path.join(ROOT, 'scenes.js'), 'utf8');
const sandbox = {
  console, JSON, Math, parseInt, parseFloat, String, Array, Object, RegExp, Number, Date,
  currentLang: 'he',
  document: { getElementById: () => ({ value: '' }) },
  window: {},
};
vm.createContext(sandbox);
vm.runInContext(scenesCode, sandbox);

function genHtml(q) {
  const html = sandbox.generateQuizHTML(q, 'he', true);
  if (!html || html.length < 500) throw new Error(`generateQuizHTML returned too little (${html ? html.length : 0}b) for Q${q.num}`);
  return html;
}

module.exports = { genHtml };
