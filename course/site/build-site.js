// node build-site.js
// Builds the new alargov.com (staged at /v2/). Never touches the current landing page (/index.html),
// /ofnoa-yam/ or /legal/.
//
// Inputs:
//   hub.js               sections, courses, header/footer
//   content/posts.json   news posts exported from the Back Office (only status "approved" is published)
//   content/reels.json   videos: { num, title, date? } -> URL read from data/l11.json
// Outputs:
//   v2/index.html, video/, hadash/, kursim/, <section>/index.html, <section>/<slug>.html
const fs = require('fs');
const path = require('path');
const { SECTIONS, NEWS, VIDEO, COURSES, FONTS, header, footer } = require('./hub');

const ROOT = __dirname;
const SITE = 'https://www.alargov.com';
const abs = u => (/^https?:/.test(u) ? u : SITE + u);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const tile = name => `/assets/tiles/${name}.jpg`;
const fmtDate = iso => new Date(iso + 'T12:00:00Z').toLocaleDateString('he-IL', { day: 'numeric', month: 'long', year: 'numeric' });
const write = (rel, html) => { const f = path.join(ROOT, rel); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, html); };
const sectionOf = slug => SECTIONS.find(s => s.slug === slug) || { slug, name: slug };

// ---------- data ----------
// content/posts.json is the Back Office queue (back-office.html commits it). Only approved/published go up.
const posts = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'posts.json'), 'utf8'))
  .filter(d => (d.status === 'approved' || d.status === 'published') && d.out && d.out.slug)
  .map(d => ({ id: d.id, slug: d.out.slug, title: d.out.title, excerpt: d.out.excerpt, body: d.out.body, rule: d.out.rule,
    exam: d.out.exam, section: d.section, source: d.source, image: d.image, video: d.video,
    date: (d.approvedAt || d.updated || d.created).slice(0, 10),
    modified: [d.approvedAt, d.updated, d.created].filter(Boolean).sort().pop().slice(0, 10) }))
  .sort((a, b) => b.date.localeCompare(a.date))
  .map(p => ({ ...p, href: `/${p.section}/${p.slug}/`, anchor: `/hadash/#${p.slug}`, img: p.image || tile(sectionOf(p.section).img || 'coast') }));

const questions = JSON.parse(fs.readFileSync(path.join(ROOT, '..', '..', 'data', 'l11.json'), 'utf8'));
const qByNum = new Map(questions.map(q => [q.num, q]));
// A video's date is the latest of: its publish date
// (tools/tiktok-publish-history.json) and its render date (rendered_at). No manual dating needed.
// content/reels.json only sets a short title and the order of the homepage rail.
const picks = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'reels.json'), 'utf8'));
const titleOf = new Map(picks.map(r => [r.num, r.title]));
const pubFile = path.join(ROOT, '..', '..', 'tools', 'tiktok-publish-history.json');
const published = new Map();
if (fs.existsSync(pubFile)) for (const h of JSON.parse(fs.readFileSync(pubFile, 'utf8'))) {
  const d = (h.published_at || h.date || '').slice(0, 10);
  if (d && (!published.get(h.num) || d > published.get(h.num))) published.set(h.num, d);
}
// Spoken script without niqqud / pause markers = the video's transcript.
const transcriptOf = q => String(q.voiceover_text || '').replace(/\[\[PAUSE\]\]/g, ' ')
  .replace(/[\u0591-\u05C7]/g, '').replace(/\s+/g, ' ').replace(/\s+([.,?!])/g, '$1').trim();
const shortQ = t => { t = t.replace(/\s+/g, ' ').trim(); if (t.length <= 58) return t; const cut = t.slice(0, 58); return cut.slice(0, cut.lastIndexOf(' ')) + '…'; };
// Only the public rotation pool goes on the site (tools/daily-publish-pool.json — the 40 questions
// that are posted to social media again and again). The rest of the bank stays inside the paid course.
const POOL = new Set(JSON.parse(fs.readFileSync(path.join(ROOT, '..', '..', 'tools', 'daily-publish-pool.json'), 'utf8')).map(p => p.num));
for (const r of picks) if (!POOL.has(r.num)) throw new Error(`reels.json: question ${r.num} is not in the public pool`);
const allVideos = questions.filter(q => q.videoUrl && POOL.has(q.num)).map(q => {
  const dates = [published.get(q.num), (q.rendered_at || '').slice(0, 10)].filter(Boolean).sort();
  return { num: q.num, topic: q.topic, src: q.videoUrl, date: dates.pop() || '',
    title: titleOf.get(q.num) || shortQ(q.q_he), picked: titleOf.has(q.num),
    poster: q.videoUrl.replace('/video/upload/', '/video/upload/so_3,w_500,c_scale/').replace(/\.mp4$/, '.jpg'),
    q: q.q_he, options: q.options || [], answer: q.answer, explanation: q.explanation || '',
    transcript: transcriptOf(q), href: `/video/q${q.num}/` };
}).sort((a, b) => b.date.localeCompare(a.date) || b.num - a.num);
// Homepage rail: hand-picked first (reels.json order), then the newest.
const videos = [...picks.map(r => allVideos.find(v => v.num === r.num)).filter(Boolean),
  ...allVideos.filter(v => !v.picked)].slice(0, 14);

// Q&A articles under /ofnoa-yam/ (built by build-topics.js) — used to keep the news window turning.
const articles = JSON.parse(fs.readFileSync(path.join(ROOT, 'ofnoa-yam', 'topics.json'), 'utf8'))
  .map(t => ({ href: `/ofnoa-yam/${t.slug}.html`, img: t.poster, title: t.h1, topic: t.topic }));

// ---------- structured data ----------
// sameAs = profiles of the same entity only. WhatsApp is a contact channel, so it sits in contactPoint.
const ORG = { '@type': 'Organization', '@id': `${SITE}/#org`, name: 'אלכס ארגוב · סקיפר דיגיטלי', url: `${SITE}/`,
  logo: `${SITE}/assets/logo.jpg`, email: 'alex@alargov.com',
  sameAs: ['https://www.instagram.com/argovalexander/',
    'https://play.google.com/store/apps/details?id=com.alexskipper.marinedictionary'],
  contactPoint: { '@type': 'ContactPoint', contactType: 'customer support', telephone: '+972-52-368-2486',
    email: 'alex@alargov.com', url: 'https://wa.me/972523682486', availableLanguage: ['he'] } };
// A real photo of Alex beats the logo for E-E-A-T: drop it at assets/alex.jpg and the build picks it up.
const PERSON_IMG = fs.existsSync(path.join(ROOT, 'assets', 'alex.jpg')) ? 'alex.jpg' : 'logo.jpg';
const PERSON = { '@type': 'Person', '@id': `${SITE}/#alex`, name: 'אלכס ארגוב', alternateName: 'Alexander Argov',
  jobTitle: 'מדריך שיט', description: 'מדריך שיט מעשי ותאוריה עם 9 שנות הדרכה. מלמד תאוריה לרישיונות שיט בישראל.',
  url: `${SITE}/`, image: `${SITE}/assets/${PERSON_IMG}`, worksFor: { '@id': `${SITE}/#org` },
  sameAs: ['https://www.instagram.com/argovalexander/'],
  knowsAbout: ['רישיון שיט', 'רישיון אופנוע ים', 'מבחן תאוריה בשיט', 'חוקי הדרך בים (COLREG)', 'ניווט חופי', 'בטיחות בים'] };
const ORG_REF = { '@id': `${SITE}/#org` };
const ALEX_REF = { '@id': `${SITE}/#alex` };
// The live course; question videos and Q&A link to it with isPartOf.
const COURSE_REF = { '@id': `${SITE}/kursim/#${COURSES.find(c => c.live).id}` };
// Video length (ISO 8601) from content/video-durations.json, filled by `node video-durations.js`.
const DURFILE = path.join(ROOT, 'content', 'video-durations.json');
const durations = fs.existsSync(DURFILE) ? JSON.parse(fs.readFileSync(DURFILE, 'utf8')) : {};
const isoDur = u => { const s = durations[u]; return s ? `PT${Math.floor(s / 60) ? Math.floor(s / 60) + 'M' : ''}${s % 60}S` : undefined; };
const WEBSITE = { '@type': 'WebSite', '@id': `${SITE}/#website`, name: 'אלכס ארגוב · סקיפר דיגיטלי', url: `${SITE}/`,
  inLanguage: 'he', publisher: { '@id': `${SITE}/#org` } };
const ld = obj => `<script type="application/ld+json">${JSON.stringify(obj).replace(/</g, '\\u003c')}</script>`;
const crumbs = items => ({ '@type': 'BreadcrumbList', itemListElement: items.map(([name, url], i) =>
  ({ '@type': 'ListItem', position: i + 1, name, item: SITE + url })) });

// ---------- shared pieces ----------
// Indexing is controlled by the deploy, not the code: the Dockerfile adds noindex + Disallow only
// when STAGING=1. A page asks for noindex here only when it is an empty placeholder.
function page({ title, desc, active, body, canonical, extraHead = '', noindex = false, image = '/assets/sea-hero.jpg', type = 'website' }) {
  return `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<script src="/assets/ga.js"></script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
${noindex ? '<meta name="robots" content="noindex">\n' : ''}<meta name="theme-color" content="#102948">
<meta name="sq-api" content="https://api.alargov.com">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:locale" content="he_IL">
<meta property="og:type" content="${type}">
<meta property="og:image" content="${esc(abs(image))}">
<meta property="og:site_name" content="אלכס ארגוב · סקיפר דיגיטלי">
${canonical ? `<meta property="og:url" content="${SITE}${canonical}">\n<link rel="canonical" href="${SITE}${canonical}">` : ''}
<link rel="alternate" type="text/plain" href="/llms.txt" title="llms.txt">
${FONTS}
<link rel="stylesheet" href="/assets/site.css">
${extraHead}
</head>
<body>
${header(active)}
${body}
${footer()}
<script src="https://unpkg.com/lenis@1.3.26/dist/lenis.min.js"></script>
<script src="/assets/motion.js" defer></script>
<script src="/assets/buy.js" defer></script>
</body>
</html>
`;
}

const PLAY = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>';

function reelCard(v) {
  return `<button class="reel" type="button" data-src="${esc(v.src)}" data-num="${v.num}"><span class="thumb"><img src="${esc(v.poster)}" alt="" loading="lazy"><span class="play">${PLAY}</span></span><span class="cap"><b>${esc(v.title)}</b><span>${esc(v.topic)}</span></span></button>`;
}

const PLAYER = `<div class="player" id="player" role="dialog" aria-modal="true" aria-label="נגן וידאו">
  <button class="x" id="playerClose" type="button" aria-label="סגור">✕</button>
  <video id="playerVid" controls playsinline></video>
</div>
<script>
(function(){
  var pl=document.getElementById('player'),pv=document.getElementById('playerVid'),x=document.getElementById('playerClose');
  function open(src){pv.src=src;pl.classList.add('open');pv.play();x.focus()}
  function close(){pv.pause();pv.removeAttribute('src');pv.load();pl.classList.remove('open')}
  document.querySelectorAll('.reel').forEach(function(r){r.addEventListener('click',function(){open(r.dataset.src)})});
  x.addEventListener('click',close);
  pl.addEventListener('click',function(e){if(e.target===pl)close()});
  addEventListener('keydown',function(e){if(e.key==='Escape'&&pl.classList.contains('open'))close()});
  var v=new URLSearchParams(location.search).get('v'),r=v&&document.querySelector('.reel[data-num="'+v+'"]');
  if(r)open(r.dataset.src);
})();
</script>`;

function storyCard(p) {
  return `<a class="story" href="${p.href}">
        <span class="story-img"><img src="${p.img}" alt="" loading="lazy"></span>
        <span class="story-sec">${esc(sectionOf(p.section).name)}</span>
        <h3>${esc(p.title)}</h3>
        <p>${esc(p.excerpt)}</p>
        <time datetime="${p.date}">${fmtDate(p.date)}</time>
      </a>`;
}

function pagehead(name, blurb, soon, app) {
  return `<section class="pagehead">
  <div class="wrap">
    <h1>${esc(name)}</h1>
    <p>${esc(blurb)}</p>
    ${app ? `<a class="btn btn-gold app-btn" href="${app.href}" target="_blank" rel="noopener">${esc(app.label)}</a>` : soon ? '<span class="soon">עולה בקרוב</span>' : ''}
  </div>
</section>`;
}

// ---------- home ----------
// A rotating tile: slides cross-fade; the whole tile links to the slide on show.
function rotator(label, slides, cls = '') {
  return `<div class="tile rot ${cls}" data-rot>
        <span class="tile-label">${esc(label)}</span>
${slides.map((s, i) => `        <a class="slide${i === 0 ? ' on' : ''}" href="${s.href}"${s.date ? ` data-date="${s.date}"` : ''}${s.kind ? ` data-kind="${s.kind}"` : ''}>
          <img src="${s.img}" alt="" ${i ? 'loading="lazy"' : ''}>
          <span class="slide-txt">${s.badge ? `<span class="badge">${esc(s.badge)}</span>` : ''}<b>${esc(s.title)}</b>${s.text ? `<span>${esc(s.text)}</span>` : ''}</span>
        </a>`).join('\n')}
        <div class="dots" aria-hidden="true"></div>
      </div>`;
}

function home() {
  const courseSlides = COURSES.map(c => ({ href: c.href, img: tile(c.img), badge: c.state, title: c.name, text: c.text }));
  // "חדש באתר": the newest videos only. Posts live in the "חדש מהים" window beside it, so the two
  // never show the same item. Items dated today win: the script below hides the rest when any exist.
  const fresh = allVideos.slice(0, 10).map(v => ({ href: v.href, img: v.poster, badge: 'סרטון', title: v.title, date: v.date, kind: 'video' }));
  // News window: posts first; while there are fewer than 5, Q&A articles fill it so it keeps turning.
  const newsSlides = [
    ...posts.map(p => ({ href: p.href, img: p.img, badge: sectionOf(p.section).name, title: p.title, text: fmtDate(p.date) })),
    ...articles.slice(0, Math.max(0, 5 - posts.length)).map(a => ({ href: a.href, img: a.img, badge: 'שאלה מהמאגר', title: a.title, text: a.topic })),
  ];

  const body = `
<section class="strip">
  <img class="poster" src="/assets/sea-hero.jpg" alt="">
  <video id="heroVid" autoplay muted loop playsinline poster="/assets/sea-hero.jpg" aria-hidden="true"><source src="/assets/sea-hero.mp4" type="video/mp4"></video>
  <div class="wrap strip-copy">
    <h1><span class="h1-kicker">קורסי תאוריה לרישיון שיט · אלכס ארגוב</span>לצאת לים, ולדעת מה עושים.</h1>
    <p>סרטונים, חדשות מהים, מדריכים וקורסי הכנה למבחן התאוריה לרישיונות שיט. בעברית, מאת מדריך השיט אלכס ארגוב.</p>
  </div>
  <button class="mute" id="heroPause" type="button">עצור וידאו</button>
</section>

<section class="board">
  <div class="wrap">
    <div class="board-top">
      ${rotator('קורסים', courseSlides, 'tile--courses')}
      ${rotator('חדש באתר', fresh, 'tile--fresh')}
      ${rotator(NEWS.name, newsSlides, 'tile--news')}
    </div>
    <div class="board-topics">
${SECTIONS.map(s => `      <a class="tile topic" href="/${s.slug}/"><img src="${tile(s.img)}" alt="" loading="lazy"><span class="slide-txt"><b>${s.name}</b><span>${esc(s.blurb)}</span></span></a>`).join('\n')}
    </div>
  </div>
</section>

<section class="watch" id="watch">
  <div class="wrap watch-head">
    <h2>${VIDEO.name}</h2>
    <div class="watch-acts">
      <a class="more" href="/video/">כל הסרטונים</a>
      <div class="rail-nav"><button type="button" data-dir="1" aria-label="הקודם">›</button><button type="button" data-dir="-1" aria-label="הבא">‹</button></div>
    </div>
  </div>
  <div class="rail" id="rail">
    ${videos.map(reelCard).join('\n    ')}
  </div>
</section>

<section class="about">
  <div class="wrap about-grid">
    <img src="/assets/${PERSON_IMG}" alt="${PERSON_IMG === 'alex.jpg' ? 'אלכס ארגוב, מדריך שיט' : 'הלוגו של אלכס ארגוב: קטמרן בקווים לבנים על רקע כחול'}" width="240" height="240" loading="lazy">
    <div>
      <h2>אני אלכס.</h2>
      <p>מדריך שיט כבר 9 שנים. מלמד תאוריה לרישיונות שיט, ופה אני שם את מה שאני מספר לתלמידים מחוץ לשיעור: מה קרה בים, מה אפשר ללמוד מזה, ואיך מתכוננים ליציאה הבאה.</p>
      <div class="acts"><a class="btn btn-gold" href="https://wa.me/972523682486" target="_blank" rel="noopener">לכתוב לי בוואטסאפ</a></div>
    </div>
  </div>
</section>

${PLAYER}
<script>
(function(){
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var v=document.getElementById('heroVid'),pb=document.getElementById('heroPause');
  if(reduce){v.pause();pb.textContent='הפעל וידאו'}
  pb.addEventListener('click',function(){if(v.paused){v.play();pb.textContent='עצור וידאו'}else{v.pause();pb.textContent='הפעל וידאו'}});
  var rail=document.getElementById('rail');
  document.querySelectorAll('.rail-nav button').forEach(function(b){b.addEventListener('click',function(){rail.scrollBy({left:b.dataset.dir*rail.clientWidth*0.8,behavior:'smooth'})})});

  // "חדש באתר": when something went up today (Israel time), show only today's items.
  var today=new Date().toLocaleDateString('sv-SE',{timeZone:'Asia/Jerusalem'});
  var fresh=document.querySelector('.tile--fresh');
  var todays=fresh.querySelectorAll('.slide[data-date="'+today+'"]');
  if(todays.length){
    fresh.querySelector('.tile-label').textContent='היום באתר';
    fresh.querySelectorAll('.slide').forEach(function(s){if(s.dataset.date!==today)s.remove()});
    fresh.querySelectorAll('.slide').forEach(function(s,i){s.classList.toggle('on',i===0)});
  }

  // Rotating tiles: one slide at a time, every 5s, staggered; pause on hover/focus; dots switch.
  document.querySelectorAll('[data-rot]').forEach(function(t,k){
    var slides=t.querySelectorAll('.slide'),dots=t.querySelector('.dots'),i=0,timer;
    if(slides.length<2){dots.remove();return}
    slides.forEach(function(_,n){var d=document.createElement('button');d.type='button';d.setAttribute('aria-label','שקופית '+(n+1));
      d.addEventListener('click',function(e){e.preventDefault();show(n)});dots.appendChild(d)});
    dots.removeAttribute('aria-hidden');
    function show(n){slides[i].classList.remove('on');dots.children[i].classList.remove('on');i=n;slides[i].classList.add('on');dots.children[i].classList.add('on')}
    show(0);
    function start(){if(reduce)return;stop();timer=setInterval(function(){show((i+1)%slides.length)},5000)}
    function stop(){clearInterval(timer)}
    t.addEventListener('mouseenter',stop);t.addEventListener('mouseleave',start);
    t.addEventListener('focusin',stop);t.addEventListener('focusout',start);
    setTimeout(start,k*1600);
  });
})();
</script>`;
  return page({ title: 'אלכס ארגוב · סקיפר דיגיטלי | קורסי תאוריה לרישיון שיט', desc: 'קורסי הכנה למבחן התאוריה לרישיונות שיט, סרטונים עם הסבר לשאלות המבחן, וחדשות מהים. בעברית, מאת מדריך השיט אלכס ארגוב.', active: null, body, canonical: '/',
    extraHead: ld({ '@context': 'https://schema.org', '@graph': [ORG, PERSON, WEBSITE] }) });
}

// ---------- posts ----------
function md(text) {
  const inline = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  return text.split(/\n{2,}/).map(block => {
    const lines = block.split('\n');
    const items = lines.filter(l => l.startsWith('- '));
    if (items.length) {
      const lead = lines.filter(l => !l.startsWith('- ')).map(l => `<p>${inline(l)}</p>`).join('\n');
      return `${lead}\n<ul>${items.map(l => `<li>${inline(l.slice(2))}</li>`).join('')}</ul>`;
    }
    return `<p>${lines.map(inline).join('<br>')}</p>`;
  }).join('\n');
}

// Embed the source video inline (the plan: embed from the source with credit, never re-upload).
function embed(src) {
  const u = src.url || '';
  // A Facebook post (not a reel/video) only renders through the post plugin.
  if (/facebook\.com/.test(u) && !/\/(reel|videos|watch)\b|fb\.watch/.test(u))
    return `<iframe class="fb-post" src="https://www.facebook.com/plugins/post.php?href=${encodeURIComponent(u)}&show_text=true&width=500" title="הפוסט המקורי" loading="lazy" allow="clipboard-write; encrypted-media; picture-in-picture; web-share" allowfullscreen></iframe>`;
  if (/facebook\.com|fb\.watch/.test(u))
    return `<iframe src="https://www.facebook.com/plugins/video.php?href=${encodeURIComponent(u)}&show_text=false&width=320&height=568" title="הסרטון המקורי" loading="lazy" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share" allowfullscreen></iframe>`;
  const yt = u.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|shorts\/|embed\/))([\w-]{11})/);
  if (yt) return `<iframe src="https://www.youtube-nocookie.com/embed/${yt[1]}" title="הסרטון המקורי" loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe>`;
  const ig = u.match(/instagram\.com\/(?:reel|p)\/([\w-]+)/);
  if (ig) return `<iframe src="https://www.instagram.com/p/${ig[1]}/embed" title="הסרטון המקורי" loading="lazy"></iframe>`;
  return '';
}

// One news item: video beside the headline and a few lines; "קרא עוד" opens the rest in place.
function newsItem(p) {
  const src = p.source || {};
  // A video file attached in the Back Office wins over embedding the source post.
  const video = p.video
    ? `<video src="${esc(p.video)}" controls playsinline preload="metadata"${p.image ? ` poster="${esc(p.image)}"` : ''}></video>`
    : src.mediaType === 'video' ? embed(src) : '';
  const credit = src.url ? `<a class="credit" href="${esc(src.url)}" target="_blank" rel="noopener">${esc(src.author || 'המקור')}${src.platform ? `, ב${esc(src.platform)}` : ''}</a>` : '';
  return `<article class="news-item" id="${esc(p.slug)}">
    <div class="news-media">${video || `<img src="${p.img}" alt="" loading="lazy">`}${credit ? `<p class="news-credit">הסרטון: ${credit}</p>` : ''}</div>
    <div class="news-txt">
      <p class="post-meta"><a href="/${p.section}/">${esc(sectionOf(p.section).name)}</a> <time datetime="${p.date}">${fmtDate(p.date)}</time></p>
      <h2>${esc(p.title)}</h2>
      <p class="news-lede">${esc(p.excerpt)}</p>
      <div class="news-more" hidden>
${md(p.body)}
        ${p.rule ? `<div class="rule"><h3>הכלל</h3><p>${esc(p.rule)}</p></div>` : ''}
        <p class="post-sign">אלכס ארגוב, סקיפר דיגיטלי</p>
      </div>
      <button class="read-more" type="button" aria-expanded="false">קרא עוד</button>
      <a class="permalink" href="${p.href}">לכתבה המלאה</a>
    </div>
  </article>`;
}

const NEWS_JS = `<script>
(function(){
  function toggle(a,open){var m=a.querySelector('.news-more'),b=a.querySelector('.read-more');
    m.hidden=!open;b.setAttribute('aria-expanded',open);b.textContent=open?'סגור':'קרא עוד'}
  document.querySelectorAll('.news-item').forEach(function(a){
    a.querySelector('.read-more').addEventListener('click',function(){toggle(a,a.querySelector('.news-more').hidden)})});
  var h=decodeURIComponent(location.hash.slice(1)),t=h&&document.getElementById(h);
  if(t&&t.classList.contains('news-item')){toggle(t,true);t.scrollIntoView()}
})();
</script>`;

function feed(slug, name, blurb, list, app) {
  // The feed only lists the articles; each article's own page carries the Article markup.
  const list_ld = { '@context': 'https://schema.org', '@type': 'ItemList', name,
    itemListElement: list.map((p, i) => ({ '@type': 'ListItem', position: i + 1, url: SITE + p.href, name: p.title })) };
  const body = `
${pagehead(name, blurb, !list.length && !app, app)}
${app && app.shots ? `<section class="app-show">
  <div class="wrap app-show-in">
    <div class="app-copy"><h2>מה יש במילון</h2>${(app.intro || []).map(t => `<p>${esc(t)}</p>`).join('')}</div>
    <div class="app-shots">${app.shots.map(s => `<figure><img src="${s.img}" alt="${esc(s.cap)}" loading="lazy" width="480" height="924"><figcaption>${esc(s.cap)}</figcaption></figure>`).join('')}</div>
  </div>
</section>` : ''}
${list.length || !app ? `<section class="feed">
  <div class="wrap news-list">
  ${list.map(newsItem).join('\n  ')}
  </div>
</section>` : ''}
${NEWS_JS}`;
  // An empty section is a placeholder: keep it out of search until it has something to say.
  // A section that is an app page (the dictionary) describes the app itself.
  const app_ld = app && { '@context': 'https://schema.org', '@graph': [
    { '@type': 'MobileApplication', '@id': `${SITE}/${slug}/#app`, name, alternateName: 'Marine Dictionary',
      description: blurb, url: `${SITE}/${slug}/`, installUrl: app.href.replace(/&hl=\w+$/, ''),
      operatingSystem: 'Android', applicationCategory: 'EducationalApplication', inLanguage: ['he', 'en', 'fr'],
      offers: { '@type': 'Offer', price: '0', priceCurrency: 'ILS' },
      ...(app.shots ? { screenshot: app.shots.map(s => abs(s.img)) } : {}),
      author: ALEX_REF, publisher: ORG_REF },
    ORG, PERSON] };
  return page({ title: `${name} | אלכס ארגוב`, desc: blurb, active: slug, body, canonical: `/${slug}/`,
    noindex: !list.length && !app, extraHead: [list.length ? ld(list_ld) : '', app_ld ? ld(app_ld) : ''].filter(Boolean).join('\n') });
}

// ---------- article page (one permanent URL per post) ----------
function postPage(p) {
  const sec = sectionOf(p.section);
  const src = p.source || {};
  const media = p.video
    ? `<video src="${esc(p.video)}" controls playsinline preload="metadata"${p.image ? ` poster="${esc(p.image)}"` : ''}></video>`
    : src.mediaType === 'video' || /facebook\.com/.test(src.url || '') ? embed(src) : '';
  const credit = src.url ? `<a class="credit" href="${esc(src.url)}" target="_blank" rel="noopener">${esc(src.author || 'המקור')}${src.platform ? `, ב${esc(src.platform)}` : ''}</a>` : '';
  const others = posts.filter(o => o.slug !== p.slug).slice(0, 3);
  const graph = [
    { '@type': 'Article', '@id': `${SITE}${p.href}#article`, headline: p.title, description: p.excerpt,
      url: SITE + p.href, mainEntityOfPage: SITE + p.href, image: [abs(p.img)], inLanguage: 'he',
      datePublished: p.date, dateModified: p.modified, articleSection: sec.name,
      author: ALEX_REF, publisher: ORG_REF,
      ...(src.url ? { isBasedOn: src.url } : {}),
      ...(p.video ? { video: { '@type': 'VideoObject', name: p.title, description: p.excerpt, contentUrl: abs(p.video),
        thumbnailUrl: abs(p.img), uploadDate: p.date, duration: isoDur(p.video) } } : {}) },
    crumbs([['בית', '/'], [sec.name, `/${p.section}/`], [p.title, p.href]]),
    ORG, PERSON,
  ];
  const body = `
<article class="post-page">
  <div class="wrap">
    <nav class="crumbs" aria-label="פירורי לחם"><a href="/v2/">בית</a> › <a href="/${p.section}/">${esc(sec.name)}</a></nav>
    <div class="news-item news-item--open">
      <div class="news-media">${media || `<img src="${p.img}" alt="" loading="lazy">`}${credit ? `<p class="news-credit">המקור: ${credit}</p>` : ''}</div>
      <div class="news-txt">
        <p class="post-meta"><a href="/${p.section}/">${esc(sec.name)}</a> <time datetime="${p.date}">${fmtDate(p.date)}</time></p>
        <h1>${esc(p.title)}</h1>
        <p class="news-lede">${esc(p.excerpt)}</p>
        <div class="news-more">
${md(p.body)}
          ${p.rule ? `<div class="rule"><h2>הכלל</h2><p>${esc(p.rule)}</p></div>` : ''}
          <p class="post-sign">אלכס ארגוב, מדריך שיט · <a href="/kursim/">קורסי תאוריה לרישיון שיט</a></p>
        </div>
      </div>
    </div>
  </div>
</article>
${others.length ? `<section class="feed related">
  <div class="wrap">
    <h2>עוד מ${esc(NEWS.name)}</h2>
    <div class="stories">
      ${others.map(storyCard).join('\n      ')}
    </div>
  </div>
</section>` : ''}`;
  return page({ title: `${p.title} | אלכס ארגוב`, desc: p.excerpt, active: p.section, body, canonical: p.href,
    image: p.img, type: 'article', extraHead: ld({ '@context': 'https://schema.org', '@graph': graph }) });
}

// ---------- video pages ----------
const LETTERS = ['א', 'ב', 'ג', 'ד'];
function videoItemPage(v) {
  const related = allVideos.filter(o => o.topic === v.topic && o.num !== v.num).slice(0, 6);
  const more = related.length < 6 ? related.concat(allVideos.filter(o => o.topic !== v.topic).slice(0, 6 - related.length)) : related;
  const correct = Number.isInteger(v.answer) ? v.answer : LETTERS.indexOf(String(v.answer).trim());
  const opt = o => String(o).replace(/^[אבגד][.)]\s*/, '');
  // Same shape as the /ofnoa-yam/ Q&A pages: QAPage > Question > acceptedAnswer. No embedUrl: the
  // page is not a player, and contentUrl already points at the file.
  const answered = correct >= 0 && v.options[correct];
  const graph = [
    { '@type': 'VideoObject', '@id': `${SITE}${v.href}#video`, name: v.q, description: v.explanation || v.q,
      thumbnailUrl: [v.poster], uploadDate: v.date || undefined, duration: isoDur(v.src), contentUrl: v.src,
      inLanguage: 'he', transcript: v.transcript, isFamilyFriendly: true, learningResourceType: 'הסבר לשאלת מבחן',
      about: { '@type': 'DefinedTerm', name: v.topic }, isPartOf: COURSE_REF,
      creator: ALEX_REF, publisher: ORG_REF },
    ...(answered ? [{ '@type': 'QAPage', '@id': `${SITE}${v.href}#page`, url: SITE + v.href, inLanguage: 'he',
      mainEntity: { '@type': 'Question', name: v.q, text: `שאלה ${v.num} מתוך מאגר מבחן התאוריה לרישיון אופנוע ים.`,
        answerCount: 1, ...(v.date ? { datePublished: v.date } : {}), author: ALEX_REF,
        acceptedAnswer: { '@type': 'Answer', text: `${opt(v.options[correct])} ${v.explanation}`.trim(),
          url: SITE + v.href, author: ALEX_REF, ...(v.date ? { datePublished: v.date } : {}) } } }] : []),
    crumbs([['בית', '/'], ['סרטונים', '/video/'], [v.title, v.href]]),
    ORG, PERSON,
  ];
  const body = `
<article class="video-page">
  <div class="wrap">
    <nav class="crumbs" aria-label="פירורי לחם"><a href="/v2/">בית</a> › <a href="/video/">סרטונים</a> › ${esc(v.topic)}</nav>
    <div class="vp-grid">
      <div class="vp-media"><video src="${esc(v.src)}" poster="${esc(v.poster)}" controls playsinline preload="metadata"></video></div>
      <div class="vp-txt">
        <p class="post-meta"><span class="topic-tag">${esc(v.topic)}</span>${v.date ? ` <time datetime="${v.date}">${fmtDate(v.date)}</time>` : ''}</p>
        <h1>${esc(v.q)}</h1>
        ${v.options.length ? `<ol class="vp-opts">${v.options.map((o, i) => `<li${i === correct ? ' class="ok"' : ''}><b>${LETTERS[i] || i + 1}</b> ${esc(opt(o))}${i === correct ? ' <span>התשובה הנכונה</span>' : ''}</li>`).join('')}</ol>` : ''}
        ${v.explanation ? `<div class="rule"><h2>ההסבר</h2><p>${esc(v.explanation)}</p></div>` : ''}
        <details class="transcript" open><summary>תמליל הסרטון</summary><p>${esc(v.transcript)}</p></details>
        <div class="side-cta"><p>זו שאלה מתוך מאגר מבחן התאוריה לרישיון אופנוע ים. בקורס יש הסבר כזה לכל שאלה במאגר.</p><div class="acts"><a class="btn btn-gold" href="https://app.alargov.com/" data-trial>13 שאלות חינם</a> <a class="btn btn-navy" href="/kursim/#buy">לקורס המלא</a></div></div>
      </div>
    </div>
  </div>
</article>
<section class="feed related">
  <div class="wrap">
    <h2>עוד סרטונים</h2>
    <div class="vgrid">
    ${more.map(videoLink).join('\n    ')}
    </div>
  </div>
</section>`;
  return page({ title: `${v.title} · סרטון הסבר | אלכס ארגוב`, desc: `${v.q} ${v.explanation}`.slice(0, 155), active: VIDEO.slug, body,
    canonical: v.href, image: v.poster, type: 'video.other', extraHead: ld({ '@context': 'https://schema.org', '@graph': graph }) });
}
// Crawlable card: a real link to the video's own page.
function videoLink(v) {
  return `<a class="reel" href="${v.href}" data-topic="${esc(v.topic)}"><span class="thumb"><img src="${esc(v.poster)}" alt="" loading="lazy"><span class="play">${PLAY}</span></span><span class="cap"><b>${esc(v.title)}</b><span>${esc(v.topic)}</span></span></a>`;
}

function videoPage() {
  // News posts built around a video show here too, newest first.
  const seaVideos = posts.filter(p => p.video || (p.source || {}).mediaType === 'video');
  const topics = [...new Set(allVideos.map(v => v.topic))];
  const body = `
${pagehead(VIDEO.name, VIDEO.blurb)}
<section class="vgrid-wrap">
  <div class="wrap">
${seaVideos.length ? `<h2 class="vsec">מקרים מהים</h2>
    <div class="stories vstories">
      ${seaVideos.map(storyCard).join('\n      ')}
    </div>
    <h2 class="vsec">שאלות מהמבחן</h2>` : ''}
    <div class="chips" role="group" aria-label="סינון לפי נושא">
      <button type="button" class="chip on" data-t="">הכל</button>
      ${topics.map(t => `<button type="button" class="chip" data-t="${esc(t)}">${esc(t)}</button>`).join('\n      ')}
    </div>
    <div class="vgrid">
    ${allVideos.map(videoLink).join('\n    ')}
    </div>
  </div>
</section>
<script>
document.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){
  document.querySelectorAll('.chip').forEach(function(x){x.classList.toggle('on',x===c)});
  document.querySelectorAll('.vgrid .reel').forEach(function(r){r.hidden=!!c.dataset.t&&r.dataset.topic!==c.dataset.t});
})});
// old links /video/?v=1154 -> /video/q1154/
(function(){var v=new URLSearchParams(location.search).get('v');if(v)location.replace('/video/q'+v+'/')})();
</script>`;
  const list = { '@context': 'https://schema.org', '@type': 'ItemList', name: VIDEO.name,
    itemListElement: allVideos.map((v, i) => ({ '@type': 'ListItem', position: i + 1, url: SITE + v.href, name: v.title })) };
  return page({ title: `${VIDEO.name}: הסברים לשאלות מבחן התאוריה בשיט | אלכס ארגוב`, desc: VIDEO.blurb, active: VIDEO.slug, body, canonical: '/video/', extraHead: ld(list) });
}

// ---------- courses ----------
const FAQ = [
  ['לאיזה רישיון הקורס מיועד?', 'הקורס הפתוח היום מכין למבחן התאוריה של רישיון אופנוע ים של רשות הספנות והנמלים (רספ״ן). קורסים למשיט 12, 30 ו-40 בהכנה.'],
  ['מה כולל הקורס?', 'כל שאלות המאגר הרשמי, הסבר קולי לכל שאלה, 13 מערכי שיעור מצולמים שמכסים את כל נושאי הסילבוס, ומבחני דמה בפורמט האמיתי.'],
  ['כמה עולה הקורס?', '10 הנרשמים הראשונים מקבלים גישה מלאה ב-199 ש״ח במסלול המייסדים. אחר כך המחיר 349 ש״ח.'],
  ['יש אחריות אם לא עברתי?', 'כן. מי שלמד ולא עבר את המבחן הרשמי זכאי להחזר מלא, בכפוף לתנאי מדיניות הביטולים.'],
  ['אפשר להתנסות בחינם?', 'כן. 13 השאלות הראשונות פתוחות לתרגול חינם, בלי הרשמה.'],
  ['מאיזה מכשיר לומדים?', 'מכל מכשיר: טלפון, טאבלט או מחשב. ההתקדמות נשמרת ועוברת איתך.'],
];
const WHAT = [
  ['מאגר רספ״ן המלא', 'כל השאלות מהמאגר הרשמי, בנוסח המדויק, מסודרות לפי נושאי הסילבוס.'],
  ['הסבר בקול לכל שאלה', 'המדריך מסביר בקול למה התשובה נכונה, ולמה האחרות לא.'],
  ['13 מערכי שיעור מצולמים', 'שיעור לכל נושא בסילבוס, מזכות מעבר ועד עזרה ראשונה.'],
  ['מבחני דמה בפורמט האמיתי', 'מספר שאלות, טיימר, ציון עובר ומד מוכנות שאומר מתי אפשר לגשת.'],
  ['חזרה חכמה על טעויות', 'שאלה שטעית בה חוזרת במרווחים עד שהיא יושבת.'],
];
function coursesPage() {
  const live = COURSES.filter(c => c.live);
  const graph = [
    ...live.map(c => ({ '@type': 'Course', '@id': `${SITE}/kursim/#${c.id}`, name: `קורס תאוריה לרישיון ${c.name}`,
      description: 'הכנה מלאה למבחן התאוריה: כל שאלות המאגר הרשמי של רספ״ן, הסבר קולי לכל שאלה, 13 מערכי שיעור מצולמים ומבחני דמה בפורמט האמיתי.',
      inLanguage: 'he', provider: ORG_REF, instructor: ALEX_REF,
      // Google's Course info accepts only Free / Partially Free / Subscription / Paid in category.
      offers: { '@type': 'Offer', name: 'מסלול מייסדים', category: 'Paid', price: '199', priceCurrency: 'ILS',
        priceSpecification: [
          { '@type': 'UnitPriceSpecification', price: '199', priceCurrency: 'ILS' },
          { '@type': 'UnitPriceSpecification', priceType: 'https://schema.org/StrikethroughPrice', price: '349', priceCurrency: 'ILS' }],
        availability: 'https://schema.org/InStock', url: `${SITE}/kursim/#${c.id}` },
      hasCourseInstance: { '@type': 'CourseInstance', courseMode: 'online', courseWorkload: 'PT10H', instructor: ALEX_REF },
      teaches: [...new Set(questions.map(q => q.topic).filter(Boolean))],
      educationalLevel: 'Beginner', isAccessibleForFree: false })),
    { '@type': 'FAQPage', mainEntity: FAQ.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) },
    ORG, PERSON,
  ];
  const body = `
${pagehead('קורסי תאוריה לרישיון שיט', 'הכנה למבחן התאוריה של רשות הספנות והנמלים: כל שאלות המאגר הרשמי, הסבר בקול לכל שאלה, מערכי שיעור מצולמים ומבחני דמה.')}
<section class="feed">
  <div class="wrap courses">
${COURSES.map(c => `    <${c.live ? `a href="${c.href}"` : 'div'} class="course${c.live ? ' course--live' : ''}" id="${c.id}">
      <span class="course-img"><img src="${tile(c.img)}" alt="" loading="lazy"></span>
      <span class="course-txt"><span class="badge">${esc(c.state)}</span><b>${esc(c.name)}</b>${c.text ? `<span>${esc(c.text)}</span>` : ''}${c.live ? '<span class="btn btn-gold">למחיר ולרכישה</span>' : ''}</span>
    </${c.live ? 'a' : 'div'}>`).join('\n')}
  </div>
</section>

<section class="kursim-what">
  <div class="wrap">
    <h2>מה מקבלים בקורס לרישיון אופנוע ים</h2>
    <ul class="what-list">
${WHAT.map(([h, t]) => `      <li><h3>${h}</h3><p>${t}</p></li>`).join('\n')}
    </ul>
    <div class="price-box" id="buy">
      <p class="price"><b data-price>₪199</b> <s data-price-regular>₪349</s></p>
      <p data-founders>מסלול מייסדים: 10 הנרשמים הראשונים ב-199 ש״ח, אחר כך 349 ש״ח.</p>
      <p class="seats" data-seats hidden></p>
      <p>גישה מלאה מיד אחרי התשלום. לא עברת את המבחן? הכסף חוזר אליך.*</p>
      <div class="acts"><a class="btn btn-gold" href="https://app.alargov.com/?buy=1" data-buy>רכוש עכשיו</a> <a class="btn btn-navy" href="https://app.alargov.com/" data-trial>13 שאלות חינם</a></div>
      <p class="fine">תשלום מאובטח בכרטיס אשראי דרך טרנזילה. * בכפוף ל<a href="/legal/refund-policy.html">מדיניות הביטולים</a>.</p>
    </div>
  </div>
</section>

<section class="kursim-faq">
  <div class="wrap">
    <h2>שאלות נפוצות</h2>
${FAQ.map(([q, a]) => `    <details><summary>${q}</summary><p>${a}</p></details>`).join('\n')}
  </div>
</section>

<section class="feed">
  <div class="wrap">
    <h2>שאלות מהמאגר, עם הסבר מלא</h2>
    <ul class="qa-links">
${articles.map(a => `      <li><a href="${a.href}"><b>${esc(a.title)}</b><span>${esc(a.topic)}</span></a></li>`).join('\n')}
    </ul>
  </div>
</section>`;
  return page({ title: 'קורסי תאוריה לרישיון שיט: אופנוע ים, משיט 12, 30, 40 | אלכס ארגוב', desc: 'קורס הכנה למבחן התאוריה לרישיון אופנוע ים: כל שאלות מאגר רספ״ן, הסבר קולי לכל שאלה, 13 מערכי שיעור ומבחני דמה. החזר כספי למי שלא עבר.', active: 'kursim', body, canonical: '/kursim/',
    image: tile('jetski'), extraHead: ld({ '@context': 'https://schema.org', '@graph': graph }) });
}

// ---------- write ----------
write('v2/index.html', home());
write('video/index.html', videoPage());
for (const v of allVideos) write(`video/q${v.num}/index.html`, videoItemPage(v));
write('kursim/index.html', coursesPage());
write(`${NEWS.slug}/index.html`, feed(NEWS.slug, NEWS.name, NEWS.blurb, posts));
const sectionLists = SECTIONS.map(s => [s, posts.filter(p => p.section === s.slug)]);
for (const [s, list] of sectionLists) write(`${s.slug}/index.html`, feed(s.slug, s.name, s.blurb, list, s.app));
for (const p of posts) write(`${p.section}/${p.slug}/index.html`, postPage(p));

// ---------- sitemap.xml (everything indexable) + llms.txt ----------
const today = new Date().toISOString().slice(0, 10);
const urls = [
  ['/', today, '1.0'], ['/kursim/', today, '0.9'], ['/video/', today, '0.8'], [`/${NEWS.slug}/`, posts[0]?.date || today, '0.8'],
  ...sectionLists.filter(([s, l]) => l.length || s.app).map(([s, l]) => [`/${s.slug}/`, l[0]?.date || today, '0.6']),
  ...posts.map(p => [p.href, p.date, '0.7']),
  ...allVideos.map(v => [v.href, v.date || today, '0.6']),
  ...articles.map(a => [a.href, null, '0.7']),
  ...['refund-policy', 'privacy-policy', 'terms-of-service', 'accessibility-statement'].map(l => [`/legal/${l}.html`, null, '0.2']),
];
fs.writeFileSync(path.join(ROOT, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(([u, d, pr]) => `  <url><loc>${SITE}${u}</loc>${d ? `<lastmod>${d}</lastmod>` : ''}<priority>${pr}</priority></url>`).join('\n')}
</urlset>
`);
fs.writeFileSync(path.join(ROOT, 'llms.txt'), `# אלכס ארגוב · סקיפר דיגיטלי (alargov.com)

> אתר בעברית של מדריך השיט אלכס ארגוב: קורסי הכנה למבחן התאוריה לרישיונות שיט בישראל (רשות הספנות והנמלים, מאגר רספ״ן), סרטוני הסבר לשאלות המבחן, וחדשות ומקרים מהים עם ניתוח של מדריך.

## קורסים
- [קורסי תאוריה לרישיון שיט](${SITE}/kursim/): קורס רישיון אופנוע ים (פתוח), משיט 12, 30, 40 (בהכנה). מחיר, מה כלול, שאלות נפוצות.

## חדש מהים
${posts.map(p => `- [${p.title}](${SITE}${p.href}): ${p.excerpt}`).join('\n')}

## סרטוני הסבר לשאלות המבחן (עם תמליל)
${allVideos.map(v => `- [${v.title}](${SITE}${v.href}): ${v.topic}`).join('\n')}

## שאלות מהמאגר עם הסבר מלא
${articles.map(a => `- [${a.title}](${SITE}${a.href}): ${a.topic}`).join('\n')}

## עוד
- [מילון ימי](${SITE}/milon/): מילון מונחים ימיים בעברית, אנגלית וצרפתית (אפליקציה)
- [מדיניות ביטולים והחזרים](${SITE}/legal/refund-policy.html)
- קשר: alex@alargov.com · וואטסאפ 052-368-2486
`);

console.log(`site: home, video (${allVideos.length} pages), kursim, ${NEWS.slug} + ${SECTIONS.length} sections, ${posts.length} article page(s), sitemap ${urls.length} urls, llms.txt`);
