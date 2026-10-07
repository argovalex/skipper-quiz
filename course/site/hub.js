// New alargov.com (v2): sections from the work plan + shared header / sections grid / footer.
// Single source for every new page. Used by build-sections.js.
// Order and slugs follow the work plan (תוכנית עבודה – הרחבת alargov.com).
const SECTIONS = [
  { slug: 'magazin', name: 'מגזין', blurb: 'כל הפוסטים החדשים מכל המדורים, לפי תאריך.' },
  { slug: 'takalot', name: 'לומדים מתקלות', blurb: 'אירועים אמיתיים מהים: מה קרה, איזה כלל הופר, ומה שואלים על זה במבחן.' },
  { slug: 'sidrot', name: 'סדרות ימאות', blurb: 'סדרות ממוספרות עם אינפוגרפיקה: אורות לילה, מצבי חירום, קשר VHF, אותות.' },
  { slug: 'milon', name: 'מילון ימי', blurb: 'עמוד לכל מונח ימי, בעברית ובאנגלית.' },
  { slug: 'klim', name: 'כלים', blurb: 'סימולטור קריאת MAYDAY, משחק זכות קדימה, בוחן אורות ותנאי ים במרינות.' },
  { slug: 'israel', name: 'ישראל במים', blurb: 'מרינות, השכרת אופנוע ים, קניית סירה משומשת, ביטוח ורישוי.' },
  { slug: 'ahrei', name: 'אחרי הרישיון', blurb: 'צ\'קליסט להפלגה ראשונה, העונה הראשונה, והמעבר ל-ICC.' },
];

const COURSES = [
  { href: '/', name: 'רשיון אופנוע ים', live: true },
];

const FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&family=Karantina:wght@700&display=swap" rel="stylesheet">';

// over=true: transparent header on top of the hero video, turns navy on scroll.
function header(active, over) {
  const cur = s => (s === active ? ' aria-current="page"' : '');
  const links = SECTIONS.map(s => `<a href="/${s.slug}/"${cur(s.slug)}>${s.name}</a>`).join('\n      ');
  return `<!-- site-header:start -->
<header class="top${over ? ' top--over' : ''}" id="top">
  <div class="wrap">
    <a class="logo" href="/v2/" aria-label="אלכס ארגוב, דף הבית"><img src="/assets/logo.jpg" alt="">אלכס ארגוב</a>
    <nav class="menu" id="menu" aria-label="ניווט ראשי">
      <a href="/v2/#licenses"${cur('course')}>קורסים</a>
      <a href="/v2/#watch">סרטונים</a>
      ${links}
    </nav>
    <div class="top-cta">
      <a class="btn btn-gold btn-sm" href="/v2/#licenses">קורסים לרישיון</a>
      <button class="burger" id="burger" aria-label="תפריט" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<!-- site-header:end -->`;
}

// A section is live once its index.html is a real page (no placeholder marker).
function isLive(slug) {
  const f = require('path').join(__dirname, slug, 'index.html');
  const fs = require('fs');
  return fs.existsSync(f) && !fs.readFileSync(f, 'utf8').includes('<!-- section-placeholder -->');
}

function sectionsIndex(except) {
  return `<!-- sections-grid:start -->
    <div class="index-list">
${SECTIONS.filter(s => s.slug !== except).map(s =>
  `      <a href="/${s.slug}/"><h3>${s.name}</h3><p>${s.blurb}</p><span class="st">${isLive(s.slug) ? 'חדש' : 'בקרוב'}</span></a>`).join('\n')}
    </div>
    <!-- sections-grid:end -->`;
}
const sectionsGrid = sectionsIndex;

function footer() {
  const sec = SECTIONS.map(s => `<li><a href="/${s.slug}/">${s.name}</a></li>`).join('');
  const crs = COURSES.map(c => `<li><a href="${c.href}">${c.name}</a></li>`).join('');
  return `<!-- site-footer:start -->
<footer>
  <div class="wrap">
    <div class="fgrid">
      <div>
        <div class="logo">אלכס ארגוב</div>
        <p style="max-width:32ch">מדריך שיט. מלמד תאוריה למבחן, ומה שקורה בים אחרי שעוברים אותו.</p>
      </div>
      <div><h4>קורסים</h4><ul>${crs}<li><a href="https://app.alargov.com/">13 שאלות חינם</a></li><li><a href="/ofnoa-yam/chukim.html">שאלות לפי נושא</a></li></ul></div>
      <div><h4>באתר</h4><ul>${sec}</ul></div>
      <div><h4>דברו איתי</h4><ul><li><a href="https://wa.me/972523682486" target="_blank" rel="noopener">וואטסאפ 052-368-2486</a></li><li><a href="mailto:alex@alargov.com">alex@alargov.com</a></li><li><a href="/legal/refund-policy.html">ביטולים והחזרים</a></li></ul></div>
    </div>
    <div class="fbottom"><span>© אלכס ארגוב, סקיפר דיגיטלי</span><span>* בכפוף לתנאי ההחזר</span></div>
  </div>
</footer>
<script>
(function(){
  var b=document.getElementById('burger'),m=document.getElementById('menu'),t=document.getElementById('top');
  if(b)b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o)});
  if(t&&t.classList.contains('top--over')){var f=function(){t.classList.toggle('scrolled',scrollY>60)};addEventListener('scroll',f,{passive:true});f();}
})();
</script>
<!-- site-footer:end -->`;
}

module.exports = { SECTIONS, COURSES, FONTS, header, sectionsGrid, sectionsIndex, footer };
