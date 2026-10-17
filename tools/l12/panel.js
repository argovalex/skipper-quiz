// Booklet panel (640x960, navy) for the l12 clip+booklet composite, matching
// media/bgclips/l12_q2278_night.mp4. Run from repo root:
//   node tools/l12/panel.js <img1.png[,img2.png]> <label> <out.png> [v]
// One image: title "תמונה N". Two: "תמונות N, M" side by side, or stacked with "v"
// (for "one above the other" questions, e.g. N over C).
const puppeteer = require('puppeteer');
const fs = require('fs');
const [imgs, label, out, mode] = process.argv.slice(2);
const vert = mode === 'v';
const list = imgs.split(',');
const tags = list.map(f => `<img src="data:image/png;base64,${fs.readFileSync(f).toString('base64')}">`).join('');
const title = list.length > 1 ? `תמונות ${label}` : `תמונה ${label}`;
const html = `<!doctype html><html dir="rtl"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@700;900&display=swap" rel="stylesheet">
<style>html,body{margin:0;width:640px;height:960px;background:#0E1A2D;font-family:Heebo,Arial,sans-serif}
.t{color:#fff;font-weight:900;font-size:${list.length > 1 ? 56 : 64}px;text-align:center;margin-top:${vert ? 60 : 150}px}
.c{margin:50px auto 0;width:${list.length > 1 ? 580 : 520}px;background:#fff;border-radius:10px;padding:16px;box-sizing:border-box;display:flex;gap:12px;direction:rtl;${vert ? 'flex-direction:column;width:300px' : ''}}
.c img{flex:1;min-width:0;display:block}</style></head><body>
<div class="t">${title}</div><div class="c">${tags}</div></body></html>`;
(async () => {
  const b = await puppeteer.launch({ headless: 'new' });
  const p = await b.newPage();
  await p.setViewport({ width: 640, height: 960 });
  await p.setContent(html, { waitUntil: 'networkidle0' });
  await p.screenshot({ path: out });
  await b.close();
})();
