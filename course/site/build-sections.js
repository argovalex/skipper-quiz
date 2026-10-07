// node build-sections.js
// New alargov.com (v2) only. Never touches the current landing page (/index.html) or /ofnoa-yam/.
// 1) Writes /<slug>/index.html for each section in hub.js that has no real page yet (placeholder, noindex).
//    A section whose index.html exists without the placeholder marker belongs to its own generator
//    (e.g. build-magazin.js) and is skipped.
// 2) Refreshes the shared header / sections grid / footer blocks in v2/index.html.
const fs = require('fs');
const path = require('path');
const { SECTIONS, FONTS, header, sectionsGrid, footer } = require('./hub');

const ROOT = __dirname;
const MARK = '<!-- section-placeholder -->';
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function head(title, desc) {
  return `<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#102948">
${FONTS}
<link rel="stylesheet" href="/assets/site.css">`;
}

function placeholder(s) {
  return `<!DOCTYPE html>
${MARK}
<html lang="he" dir="rtl">
<head>
${head(`${s.name} | אלכס ארגוב`, s.blurb)}
</head>
<body>
${header(s.slug, false)}

<section class="pagehead">
  <div class="wrap">
    <h1>${esc(s.name)}</h1>
    <p>${esc(s.blurb)}</p>
    <span class="soon">המדור עולה בקרוב</span>
  </div>
</section>

<section class="index">
  <div class="wrap">
    <h2>בינתיים באתר</h2>
    <div class="index-list">
      <a href="/v2/#watch"><h3>סרטונים</h3><p>שאלות מהמבחן, דקה של הסבר לכל אחת.</p><span class="st">פתוח</span></a>
      <a href="/"><h3>קורס רשיון אופנוע ים</h3><p>13 שיעורים, כל שאלות המאגר, ו-13 שאלות ראשונות חינם.</p><span class="st">פתוח</span></a>
    </div>
    ${sectionsGrid(s.slug).replace('<div class="index-list">', '<div class="index-list" style="border-top:0;margin-top:0">')}
  </div>
</section>

${footer()}
</body>
</html>
`;
}

// Vertical question videos for the homepage rail. Titles in v2/reels.json, video URLs from the
// canonical question data (data/l11.json), so a re-rendered question updates here on the next build.
function reels() {
  const list = JSON.parse(fs.readFileSync(path.join(ROOT, 'v2', 'reels.json'), 'utf8'));
  const qs = JSON.parse(fs.readFileSync(path.join(ROOT, '..', '..', 'data', 'l11.json'), 'utf8'));
  const byNum = new Map(qs.map(q => [q.num, q]));
  const cards = list.map(r => {
    const q = byNum.get(r.num);
    if (!q || !q.videoUrl) throw new Error(`no videoUrl for question ${r.num}`);
    const poster = q.videoUrl.replace('/video/upload/', '/video/upload/so_3,w_500,c_scale/').replace(/\.mp4$/, '.jpg');
    return `    <button class="reel" type="button" data-src="${esc(q.videoUrl)}"><span class="thumb"><img src="${esc(poster)}" alt="" loading="lazy"><span class="play" aria-hidden="true"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span></span><span class="cap"><b>${esc(r.title)}</b><span>${esc(q.topic)}</span></span></button>`;
  });
  return `<!-- reels:start -->\n${cards.join('\n')}\n    <!-- reels:end -->`;
}

const swap = (html, name, block) => {
  const re = new RegExp(`[ \\t]*<!-- ${name}:start -->[\\s\\S]*?<!-- ${name}:end -->`);
  if (!re.test(html)) throw new Error(`missing ${name} markers`);
  return html.replace(re, () => block);
};

let written = 0;
for (const s of SECTIONS) {
  const dir = path.join(ROOT, s.slug);
  const file = path.join(dir, 'index.html');
  if (fs.existsSync(file) && !fs.readFileSync(file, 'utf8').includes(MARK)) continue;
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(file, placeholder(s));
  written++;
}

const home = path.join(ROOT, 'v2', 'index.html');
let html = fs.readFileSync(home, 'utf8');
html = swap(html, 'site-header', header(null, true));
html = swap(html, 'reels', '    ' + reels());
html = swap(html, 'sections-grid', '    ' + sectionsGrid(null));
html = swap(html, 'site-footer', footer());
fs.writeFileSync(home, html);

console.log(`sections: ${written} placeholder page(s); v2/index.html header/grid/footer refreshed`);
