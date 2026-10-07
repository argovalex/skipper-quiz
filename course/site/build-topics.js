#!/usr/bin/env node
// Generates the /ofnoa-yam/ topic SEO pages from ofnoa-yam/topics.json.
// Re-run after editing topics.json (verified answers/explanations) or swapping video URLs.
//   node build-topics.js
'use strict';
const fs = require('fs');
const path = require('path');

const SITE = __dirname;
const DIR = path.join(SITE, 'ofnoa-yam');
const BASE = 'https://www.alargov.com';
const topics = JSON.parse(fs.readFileSync(path.join(DIR, 'topics.json'), 'utf8'));

const esc = s => String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const firstSentences = (s, n = 2) => {
  const parts = String(s || '').split(/(?<=[.!?])\s+/);
  return parts.slice(0, n).join(' ').trim();
};

function moreLinks(cur) {
  return topics.filter(t => t.slug !== cur.slug).slice(0, 6)
    .map(t => `      <li><a href="/ofnoa-yam/${t.slug}.html">${esc(t.topic)}</a></li>`).join('\n');
}

function optsHtml(t) {
  return t.options.map((o, i) =>
    `      <li class="opt${i === t.correct ? ' correct' : ''}">${esc(o)}</li>`).join('\n');
}

function ld(t, url) {
  const accepted = (t.options[t.correct] || '') + ' ' + firstSentences(t.explanation);
  const graph = [
    { '@type': 'BreadcrumbList', itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'מבחן תיאוריה אופנוע ים', item: BASE + '/' },
      { '@type': 'ListItem', position: 2, name: t.topic, item: url },
    ] },
    { '@type': 'QAPage', mainEntity: {
      '@type': 'Question', name: t.question,
      text: 'שאלה מתוך מאגר מבחן התיאוריה של רישיון אופנוע ים (11).',
      answerCount: 1,
      acceptedAnswer: { '@type': 'Answer', text: accepted.trim() },
    } },
  ];
  if (t.video) graph.push({
    '@type': 'VideoObject', name: t.h1 + ' — הסבר',
    description: 'הסבר קולי ומצולם לשאלה מתוך מבחן התיאוריה של אופנוע ים.',
    thumbnailUrl: t.poster, contentUrl: t.video, uploadDate: '2026-08-20',
  });
  return JSON.stringify({ '@context': 'https://schema.org', '@graph': graph }, null, 2);
}

function videoHtml(t) {
  if (!t.video) return '';
  return `  <div class="vwrap">
    <video controls preload="none" playsinline poster="${esc(t.poster)}">
      <source src="${esc(t.video)}" type="video/mp4">
    </video>
  </div>\n`;
}

function page(t) {
  const url = `${BASE}/ofnoa-yam/${t.slug}.html`;
  const title = `${t.h1} · מבחן תיאוריה אופנוע ים | אלכס ארגוב`;
  const desc = `שאלה מתוך מאגר מבחן התיאוריה (טסט) של רישיון אופנוע ים: ${t.h1}. תשובה נכונה, הסבר מלא וסרטון הדגמה.`;
  return `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<meta name="theme-color" content="#0a1428">
<link rel="canonical" href="${url}">
<meta property="og:site_name" content="אלכס ארגוב · הכנה לתיאוריה בשיט">
<meta property="og:title" content="${esc(t.h1)} · מבחן תיאוריה אופנוע ים">
<meta property="og:description" content="תשובה נכונה, הסבר מלא וסרטון הדגמה לשאלה מתוך מאגר רספ״ן.">
<meta property="og:type" content="article">
<meta property="og:url" content="${url}">
<meta property="og:locale" content="he_IL">
${t.poster ? `<meta property="og:image" content="${esc(t.poster)}">` : ''}
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/ofnoa-yam/topic.css">
<script type="application/ld+json">
${ld(t, url)}
</script>
</head>
<body>
<header>
  <div class="wrap">
    <a class="brand" href="/">אלכס ארגוב <span>· תיאוריה בשיט</span></a>
    <a class="btn btn-gold" href="https://app.alargov.com/?buy=1">רכוש עכשיו</a>
  </div>
</header>

<main class="wrap">
  <nav class="crumb"><a href="/">מבחן תיאוריה אופנוע ים</a> › ${esc(t.topic)}</nav>
  <span class="eyebrow">${esc(t.keyword)} · מבחן תיאוריה אופנוע ים</span>
  <h1>${esc(t.h1)}</h1>
  <p class="lede">שאלה מתוך מאגר רספ״ן הרשמי לרישיון אופנוע ים (11), עם התשובה הנכונה, הסבר מלא וסרטון הדגמה.</p>

  <div class="qcard">
    <p class="qtext">${esc(t.question)}</p>
    <ul class="opts">
${optsHtml(t)}
    </ul>
    <div class="exp">
      <h2>למה זו התשובה</h2>
      <p>${esc(t.explanation)}</p>
    </div>
  </div>

${videoHtml(t)}
  <section class="cta">
    <h2>זו רק שאלה אחת. <span class="g">המאגר כולו מחכה לך.</span></h2>
    <p>כל שאלות המאגר הרשמי, הסבר קולי לכל שאלה, מערכי שיעור מצולמים ומבחני דמה.</p>
    <div class="row">
      <a class="btn btn-gold" href="https://app.alargov.com/?buy=1">רכוש עכשיו</a>
      <a class="btn btn-ghost" href="https://app.alargov.com/">התחל חינם</a>
    </div>
    <div class="grd">לא עברת? קבל את כספך חזרה.<span class="ast">*</span></div>
  </section>

  <section class="more">
    <h2>עוד שאלות לפי נושא</h2>
    <ul>
${moreLinks(t)}
    </ul>
  </section>
</main>

<footer>
  <div class="wrap">
    © אלכס ארגוב · הכנה לתיאוריה בשיט ·
    <a href="/legal/refund-policy.html">ביטולים והחזרים</a> ·
    <a href="/">לעמוד הבית</a>
    <p style="margin-top:8px"><span style="color:var(--faint)">*</span> בכפוף לתנאי ההחזר.</p>
  </div>
</footer>
</body>
</html>
`;
}

// ── write pages ────────────────────────────────────────────────────────────
let n = 0;
for (const t of topics) {
  fs.writeFileSync(path.join(DIR, t.slug + '.html'), page(t));
  n++;
}

// ── regenerate sitemap.xml (home + topics + legal) ─────────────────────────
const legal = ['refund-policy', 'terms-of-service', 'privacy-policy', 'accessibility-statement'];
const url = (loc, freq, pri) => `  <url>\n    <loc>${loc}</loc>\n    <changefreq>${freq}</changefreq>\n    <priority>${pri}</priority>\n  </url>`;
const sm = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  url(BASE + '/', 'weekly', '1.0'),
  ...topics.map(t => url(`${BASE}/ofnoa-yam/${t.slug}.html`, 'monthly', '0.8')),
  ...legal.map(l => url(`${BASE}/legal/${l}.html`, 'yearly', '0.2')),
  '</urlset>', '',
].join('\n');
fs.writeFileSync(path.join(SITE, 'sitemap.xml'), sm);

console.log(`generated ${n} topic pages + sitemap (${topics.length + 5} urls)`);
