// paths.js — resolve the per-license file paths the pipeline reads/writes, so the
// same scripts serve any license instead of hardcoding l11. Default license is 11,
// so callers that pass nothing behave exactly as before.
//
//   const { paths, parseLicense } = require('./paths');
//   const P = paths(parseLicense());          // reads --license N from argv (default 11)
//   fs.readFileSync(P.bank)                    // data/l<N>.json
//
// Backward-compat: for license 11 the pause-map keeps its original unsuffixed name
// (pause-map.json) and the player stays quiz-app.html, so no existing file moves.
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');

function parseLicense(argv = process.argv) {
  const i = argv.indexOf('--license');
  if (i !== -1 && argv[i + 1] && /^\d+$/.test(argv[i + 1])) return parseInt(argv[i + 1], 10);
  const eq = argv.find(a => a.startsWith('--license='));
  if (eq && /^\d+$/.test(eq.split('=')[1])) return parseInt(eq.split('=')[1], 10);
  return 11;
}

function paths(license = 11) {
  const L = parseInt(license, 10);
  return {
    license: L,
    root: ROOT,
    bank: path.join(ROOT, `data/l${L}.json`),
    questions: path.join(ROOT, 'questions.json'), // shared derived file (all licenses)
    quizData: path.join(ROOT, `quiz-data-l${L}.json`),
    pauseMap: path.join(__dirname, L === 11 ? 'pause-map.json' : `pause-map-l${L}.json`),
    quizApp: path.join(ROOT, L === 11 ? 'quiz-app.html' : `quiz-app-l${L}.html`),
    htmlDir: path.join(ROOT, L === 11 ? 'html' : `html-l${L}`),
  };
}

module.exports = { paths, parseLicense, ROOT };
