// Render l12 questions from their STORED voiceover_text (manual-niqqud path). Run from repo root:
//   node tools/l12/render-stored.js <num...>
// Then sync: node tools/quiz-app/update-question.js <nums> --license 12 --no-render
// (videoUrl into data/l12.json, pause map, merge-inject, commit+push; l12 never goes to the paid app).
const path = require('path');
const ROOT = process.cwd();
const { genHtml } = require(path.join(ROOT, 'tools/quiz-app/scene-html.js'));
const data = require(path.join(ROOT, 'data/l12.json'));
const RENDER_URL = process.env.RENDER_URL || 'https://skipper-quiz-publisher-production.up.railway.app';
(async () => {
  for (const n of process.argv.slice(2)) {
    const q = data.find(x => String(x.num) === n);
    for (let attempt = 1; attempt <= 2; attempt++) {
      const t0 = Date.now();
      try {
        const res = await fetch(`${RENDER_URL}/render/${n}`, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ voiceover_text: q.voiceover_text, html: genHtml(q), force: true }),
        });
        const d = await res.json().catch(() => ({}));
        console.log(n, res.status, ((Date.now() - t0) / 1000).toFixed(0) + 's', d.videoUrl || d.error);
        if (d.videoUrl) break;
      } catch (e) { console.log(n, 'ERR', e.message); }
    }
  }
})();
