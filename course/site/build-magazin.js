// node build-magazin.js   (run after build-sections.js)
// Reads magazin/posts.json (exported from the Back Office) and writes:
//   /<section>/<slug>.html      one page per approved post
//   /magazin/index.html         feed of all posts, newest first
//   /<section>/index.html       feed for each section that has posts (replaces its placeholder)
//   v2/index.html               the "news" block between <!-- news:start --> and <!-- news:end -->
// Only status "approved" is published. The exam question is shown only once it is marked official
// (exam.official === true), per the work plan: questions on the site come from the RASPAN bank.
const fs = require('fs');
const path = require('path');
const { SECTIONS, FONTS, header, footer } = require('./hub');

const ROOT = __dirname;
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const secName = slug => (SECTIONS.find(s => s.slug === slug) || {}).name || slug;
const fmtDate = iso => new Date(iso + 'T12:00:00Z').toLocaleDateString('he-IL', { day: 'numeric', month: 'long', year: 'numeric' });
const url = p => `/${p.section}/${p.slug}.html`;

// Minimal markdown: paragraphs, **bold**, "- " bullet lists.
function md(text) {
  const inline = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  return text.split(/\n{2,}/).map(block => {
    const lines = block.split('\n');
    const items = lines.filter(l => l.startsWith('- '));
    if (items.length && items.length === lines.length - (lines[0].startsWith('- ') ? 0 : 1)) {
      const lead = lines[0].startsWith('- ') ? '' : `<p>${inline(lines[0])}</p>\n`;
      return `${lead}<ul>${items.map(l => `<li>${inline(l.slice(2))}</li>`).join('')}</ul>`;
    }
    return `<p>${lines.map(inline).join('<br>')}</p>`;
  }).join('\n');
}

function head(title, desc, canonical) {
  return `<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#102948">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:locale" content="he_IL">
<link rel="canonical" href="https://www.alargov.com${canonical}">
${FONTS}
<link rel="stylesheet" href="/assets/site.css">`;
}

function postPage(p) {
  const ld = { '@context': 'https://schema.org', '@type': 'Article', headline: p.title, description: p.excerpt,
    datePublished: p.date, inLanguage: 'he', author: { '@type': 'Person', name: 'אלכס ארגוב' } };
  const src = p.source || {};
  return `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
${head(`${p.title} | אלכס ארגוב`, p.excerpt, url(p))}
<script type="application/ld+json">${JSON.stringify(ld)}</script>
</head>
<body>
${header(p.section, false)}

<article class="post">
  <header class="post-head">
    <div class="wrap">
      <p class="post-meta"><a href="/${p.section}/">${esc(secName(p.section))}</a> <time datetime="${p.date}">${fmtDate(p.date)}</time></p>
      <h1>${esc(p.title)}</h1>
      <p class="post-lede">${esc(p.excerpt)}</p>
    </div>
  </header>
  <div class="wrap post-grid">
    <div class="post-body">
${md(p.body)}
    </div>
    <aside class="post-side">
      ${src.url ? `<a class="source" href="${esc(src.url)}" target="_blank" rel="noopener">
        <span class="source-play" aria-hidden="true"><svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>
        <span><b>הסרטון המקורי</b>${esc(src.author || '')}${src.platform ? `, ב${esc(src.platform)}` : ''}</span>
      </a>` : ''}
      <div class="rule"><h2>הכלל</h2><p>${esc(p.rule)}</p></div>
      <div class="side-cta">
        <p>רוצה להגיע מוכן למבחן התאוריה?</p>
        <a class="btn btn-gold" href="https://app.alargov.com/">13 שאלות חינם</a>
      </div>
    </aside>
  </div>
  <p class="wrap post-sign">אלכס ארגוב, סקיפר דיגיטלי</p>
</article>

${footer()}
</body>
</html>
`;
}

function card(p, big) {
  return `<a class="story${big ? ' story--lead' : ''}" href="${url(p)}">
        <span class="story-sec">${esc(secName(p.section))}</span>
        <h3>${esc(p.title)}</h3>
        <p>${esc(p.excerpt)}</p>
        <time datetime="${p.date}">${fmtDate(p.date)}</time>
      </a>`;
}

function feedPage(title, blurb, slug, posts) {
  return `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
${head(`${title} | אלכס ארגוב`, blurb, `/${slug}/`)}
</head>
<body>
${header(slug, false)}

<section class="pagehead">
  <div class="wrap">
    <h1>${esc(title)}</h1>
    <p>${esc(blurb)}</p>
  </div>
</section>

<section class="feed">
  <div class="wrap stories">
      ${posts.map((p, i) => card(p, i === 0)).join('\n      ')}
  </div>
</section>

${footer()}
</body>
</html>
`;
}

const all = JSON.parse(fs.readFileSync(path.join(ROOT, 'magazin', 'posts.json'), 'utf8'))
  .filter(p => p.status === 'approved')
  .sort((a, b) => b.date.localeCompare(a.date));

for (const p of all) {
  fs.mkdirSync(path.join(ROOT, p.section), { recursive: true });
  fs.writeFileSync(path.join(ROOT, p.section, `${p.slug}.html`), postPage(p));
}

const mag = SECTIONS.find(s => s.slug === 'magazin');
fs.writeFileSync(path.join(ROOT, 'magazin', 'index.html'), feedPage(mag.name, mag.blurb, 'magazin', all));
for (const s of SECTIONS) {
  if (s.slug === 'magazin') continue;
  const posts = all.filter(p => p.section === s.slug);
  if (posts.length) fs.writeFileSync(path.join(ROOT, s.slug, 'index.html'), feedPage(s.name, s.blurb, s.slug, posts));
}

const home = path.join(ROOT, 'v2', 'index.html');
let html = fs.readFileSync(home, 'utf8');
const block = `<!-- news:start -->
      ${all.slice(0, 3).map((p, i) => card(p, i === 0)).join('\n      ')}
      <!-- news:end -->`;
html = html.replace(/<!-- news:start -->[\s\S]*?<!-- news:end -->/, () => block);
fs.writeFileSync(home, html);

console.log(`magazin: ${all.length} post(s) published`);
