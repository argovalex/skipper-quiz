// node build-sections.js
// 1) Writes /<slug>/index.html for each hub section that has no real page yet (placeholder, noindex).
//    A section that already has its own generator (e.g. build-magazin.js) is skipped once its
//    index.html exists without the placeholder marker.
// 2) Injects/refreshes the hub bar in index.html between <!-- hub:start --> and <!-- hub:end -->.
const fs = require('fs');
const path = require('path');
const { SECTIONS, hubHeader } = require('./hub');

const ROOT = __dirname;
const MARK = '<!-- section-placeholder -->';
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function placeholder(s) {
  const others = SECTIONS.filter(o => o.slug !== s.slug)
    .map(o => `      <li><a href="/${o.slug}/">${o.name} <span style="color:var(--dim);font-weight:400">· ${esc(o.blurb)}</span></a></li>`).join('\n');
  return `<!DOCTYPE html>
${MARK}
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(s.name)} | אלכס ארגוב</title>
<meta name="description" content="${esc(s.blurb)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0a1428">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/ofnoa-yam/topic.css">
<link rel="stylesheet" href="/assets/hub.css">
</head>
<body>
${hubHeader(s.slug)}

<main class="wrap">
  <span class="eyebrow" style="display:block;padding-top:40px">מדור</span>
  <h1>${esc(s.name)}</h1>
  <p class="lede">${esc(s.blurb)}</p>
  <div class="qcard">
    <p class="qtext">המדור עולה בקרוב.</p>
    <p style="color:var(--dim);margin:0">בינתיים, הקורס לרשיון אופנוע ים פתוח, ו-13 השאלות הראשונות חינם.</p>
    <p style="margin:18px 0 0"><a class="btn btn-gold" href="/">לקורס</a></p>
  </div>
  <section class="more">
    <h2>עוד באתר</h2>
    <ul>
${others}
    </ul>
  </section>
</main>

<footer>
  <div class="wrap">© אלכס ארגוב · <a href="/">לעמוד הבית</a></div>
</footer>
</body>
</html>
`;
}

let written = 0;
for (const s of SECTIONS) {
  const dir = path.join(ROOT, s.slug);
  const file = path.join(dir, 'index.html');
  if (fs.existsSync(file) && !fs.readFileSync(file, 'utf8').includes(MARK)) continue; // real page owns it
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(file, placeholder(s));
  written++;
}

// Landing page: refresh the hub bar block, or insert it right after <body>.
const idx = path.join(ROOT, 'index.html');
let html = fs.readFileSync(idx, 'utf8');
const block = hubHeader(null);
if (html.includes('<!-- hub:start -->')) {
  html = html.replace(/<!-- hub:start -->[\s\S]*?<!-- hub:end -->/, block);
} else {
  html = html.replace(/<body>\s*/, `<body>\n${block}\n\n`);
}
if (!html.includes('/assets/hub.css')) {
  html = html.replace('</head>', '<link rel="stylesheet" href="/assets/hub.css">\n</head>');
}
fs.writeFileSync(idx, html);
console.log(`sections: ${written} placeholder page(s) written; hub bar refreshed in index.html`);
