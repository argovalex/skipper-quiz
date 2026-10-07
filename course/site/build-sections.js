// node build-sections.js
// New alargov.com (v2) only. Never touches the current landing page (/index.html) or /ofnoa-yam/.
// 1) Writes /<slug>/index.html for each section in hub.js that has no real page yet (placeholder, noindex).
//    A section whose index.html exists without the placeholder marker belongs to its own generator
//    (e.g. build-magazin.js) and is skipped.
// 2) Refreshes the shared header / sections grid / footer blocks in v2/index.html.
const fs = require('fs');
const path = require('path');
const { SECTIONS, header, sectionsGrid, footer } = require('./hub');

const ROOT = __dirname;
const MARK = '<!-- section-placeholder -->';
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

function head(title, desc) {
  return `<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#ffffff">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;800;900&display=swap" rel="stylesheet">
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
${header(s.slug)}

<section class="hero" style="padding-bottom:40px">
  <div class="wrap">
    <span class="kicker">מדור</span>
    <h1 style="font-size:clamp(2rem,4.4vw,3.2rem)">${esc(s.name)}</h1>
    <p class="lead">${esc(s.blurb)}</p>
    <div class="hero-actions"><span class="tag" style="position:static;background:var(--sea-soft)">המדור בבנייה</span></div>
  </div>
</section>

<section style="padding-top:20px">
  <div class="wrap">
    <div class="band">
      <div>
        <h2>13 שאלות ראשונות חינם.</h2>
        <p>בינתיים, הקורס לרשיון אופנוע ים פתוח. בלי הרשמה ובלי כרטיס אשראי.</p>
      </div>
      <div class="hero-actions" style="margin:0">
        <a class="btn btn-gold" href="https://app.alargov.com/">התחל חינם</a>
        <a class="btn" style="border-color:#fff;color:#fff" href="/">לקורס</a>
      </div>
    </div>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <span class="kicker">עוד באתר</span>
    <h2>שאר המדורים</h2>
    ${sectionsGrid(s.slug)}
  </div>
</section>

${footer()}
</body>
</html>
`;
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
html = swap(html, 'site-header', header(null));
html = swap(html, 'sections-grid', '    ' + sectionsGrid(null));
html = swap(html, 'site-footer', footer());
fs.writeFileSync(home, html);

console.log(`sections: ${written} placeholder page(s); v2/index.html header/grid/footer refreshed`);
