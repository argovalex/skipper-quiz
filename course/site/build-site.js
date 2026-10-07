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
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const tile = name => `/assets/tiles/${name}.jpg`;
const fmtDate = iso => new Date(iso + 'T12:00:00Z').toLocaleDateString('he-IL', { day: 'numeric', month: 'long', year: 'numeric' });
const write = (rel, html) => { const f = path.join(ROOT, rel); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, html); };
const sectionOf = slug => SECTIONS.find(s => s.slug === slug) || { slug, name: slug };

// ---------- data ----------
const posts = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'posts.json'), 'utf8'))
  .filter(p => p.status === 'approved')
  .sort((a, b) => b.date.localeCompare(a.date))
  .map(p => ({ ...p, href: `/${p.section}/${p.slug}.html`, img: p.image || tile(sectionOf(p.section).img || 'coast') }));

const questions = JSON.parse(fs.readFileSync(path.join(ROOT, '..', '..', 'data', 'l11.json'), 'utf8'));
const qByNum = new Map(questions.map(q => [q.num, q]));
const videos = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'reels.json'), 'utf8')).map(r => {
  const q = qByNum.get(r.num);
  if (!q || !q.videoUrl) throw new Error(`no videoUrl for question ${r.num}`);
  return { ...r, topic: q.topic, src: q.videoUrl,
    poster: q.videoUrl.replace('/video/upload/', '/video/upload/so_3,w_500,c_scale/').replace(/\.mp4$/, '.jpg'),
    href: `/video/?v=${r.num}` };
});

// ---------- shared pieces ----------
function page({ title, desc, active, body, canonical, extraHead = '' }) {
  return `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#102948">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:locale" content="he_IL">
${canonical ? `<link rel="canonical" href="https://www.alargov.com${canonical}">` : ''}
${FONTS}
<link rel="stylesheet" href="/assets/site.css">
${extraHead}
</head>
<body>
${header(active)}
${body}
${footer()}
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

function pagehead(name, blurb, soon) {
  return `<section class="pagehead">
  <div class="wrap">
    <h1>${esc(name)}</h1>
    <p>${esc(blurb)}</p>
    ${soon ? '<span class="soon">עולה בקרוב</span>' : ''}
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
  // Items dated today win: the script below hides the rest when any exist.
  // Videos lead so this window differs from the news window beside it.
  const fresh = [
    ...videos.map(v => ({ href: v.href, img: v.poster, badge: 'סרטון', title: v.title, date: v.date, kind: 'video' })),
    ...posts.map(p => ({ href: p.href, img: p.img, badge: 'פוסט', title: p.title, date: p.date, kind: 'post' })),
  ];
  const newsSlides = posts.map(p => ({ href: p.href, img: p.img, badge: sectionOf(p.section).name, title: p.title, text: fmtDate(p.date) }));

  const body = `
<section class="strip">
  <img class="poster" src="/assets/sea-hero.jpg" alt="">
  <video id="heroVid" autoplay muted loop playsinline poster="/assets/sea-hero.jpg" aria-hidden="true"><source src="/assets/sea-hero.mp4" type="video/mp4"></video>
  <div class="wrap strip-copy">
    <h1>לצאת לים, ולדעת מה עושים.</h1>
    <p>סרטונים, חדשות מהים, מדריכים וקורסים לרישיונות שיט. בעברית, מאת מדריך שיט.</p>
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
    <img src="/assets/logo.jpg" alt="הלוגו של אלכס ארגוב: קטמרן בקווים לבנים על רקע כחול">
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
  return page({ title: 'אלכס ארגוב · סקיפר דיגיטלי', desc: 'סרטונים, חדשות מהים, מדריכים וקורסים לרישיונות שיט, בעברית. מאת מדריך השיט אלכס ארגוב.', active: null, body, canonical: '/' });
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

function postPage(p) {
  const ld = { '@context': 'https://schema.org', '@type': 'Article', headline: p.title, description: p.excerpt,
    datePublished: p.date, inLanguage: 'he', author: { '@type': 'Person', name: 'אלכס ארגוב' } };
  const src = p.source || {};
  const sec = sectionOf(p.section);
  const body = `
<article class="post">
  <header class="post-head" style="--img:url(${p.img})">
    <div class="wrap">
      <p class="post-meta"><a href="/${p.section}/">${esc(sec.name)}</a> <time datetime="${p.date}">${fmtDate(p.date)}</time></p>
      <h1>${esc(p.title)}</h1>
      <p class="post-lede">${esc(p.excerpt)}</p>
    </div>
  </header>
  <div class="wrap post-grid">
    <div class="post-body">
${md(p.body)}
      <p class="post-sign">אלכס ארגוב, סקיפר דיגיטלי</p>
    </div>
    <aside class="post-side">
      ${src.url ? `<a class="source" href="${esc(src.url)}" target="_blank" rel="noopener"><span class="source-play">${PLAY}</span><span><b>הסרטון המקורי</b>${esc(src.author || '')}${src.platform ? `, ב${esc(src.platform)}` : ''}</span></a>` : ''}
      ${p.rule ? `<div class="rule"><h2>הכלל</h2><p>${esc(p.rule)}</p></div>` : ''}
      <div class="side-cta"><p>מתכוננים למבחן התאוריה?</p><a class="btn btn-gold" href="/kursim/">לקורסים</a></div>
    </aside>
  </div>
</article>`;
  return page({ title: `${p.title} | אלכס ארגוב`, desc: p.excerpt, active: p.section, body, canonical: p.href,
    extraHead: `<script type="application/ld+json">${JSON.stringify(ld)}</script>` });
}

function feed(slug, name, blurb, list) {
  const body = `
${pagehead(name, blurb, !list.length)}
<section class="feed">
  <div class="wrap stories">
      ${list.map(storyCard).join('\n      ')}
  </div>
</section>`;
  return page({ title: `${name} | אלכס ארגוב`, desc: blurb, active: slug, body, canonical: `/${slug}/` });
}

function videoPage() {
  const body = `
${pagehead(VIDEO.name, VIDEO.blurb)}
<section class="vgrid-wrap">
  <div class="wrap vgrid">
    ${videos.map(reelCard).join('\n    ')}
  </div>
</section>
${PLAYER}`;
  return page({ title: `${VIDEO.name} | אלכס ארגוב`, desc: VIDEO.blurb, active: VIDEO.slug, body, canonical: '/video/' });
}

function coursesPage() {
  const body = `
${pagehead('קורסים לרישיונות שיט', 'הכנה למבחן התאוריה: כל שאלות המאגר הרשמי, הסבר בקול לכל שאלה ומערכי שיעור מצולמים.')}
<section class="feed">
  <div class="wrap courses">
${COURSES.map(c => `    <${c.live ? `a href="${c.href}"` : 'div'} class="course${c.live ? ' course--live' : ''}" id="${c.id}">
      <span class="course-img"><img src="${tile(c.img)}" alt="" loading="lazy"></span>
      <span class="course-txt"><span class="badge">${esc(c.state)}</span><b>${esc(c.name)}</b>${c.text ? `<span>${esc(c.text)}</span>` : ''}${c.live ? '<span class="btn btn-gold">לקורס</span>' : ''}</span>
    </${c.live ? 'a' : 'div'}>`).join('\n')}
  </div>
</section>`;
  return page({ title: 'קורסים | אלכס ארגוב', desc: 'קורסי הכנה למבחן התאוריה לרישיונות שיט.', active: 'kursim', body, canonical: '/kursim/' });
}

// ---------- write ----------
write('v2/index.html', home());
write('video/index.html', videoPage());
write('kursim/index.html', coursesPage());
write(`${NEWS.slug}/index.html`, feed(NEWS.slug, NEWS.name, NEWS.blurb, posts));
for (const s of SECTIONS) write(`${s.slug}/index.html`, feed(s.slug, s.name, s.blurb, posts.filter(p => p.section === s.slug)));
for (const p of posts) write(`${p.section}/${p.slug}.html`, postPage(p));

console.log(`site: home, video (${videos.length}), kursim, ${NEWS.slug} + ${SECTIONS.length} sections, ${posts.length} post page(s)`);
