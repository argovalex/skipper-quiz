// New alargov.com (v2): site structure + shared header/footer. Used by build-site.js.

// Topic sections (each gets /<slug>/). Magazine and series were dropped (Alex, 2026-10-07).
const SECTIONS = [
  { slug: 'takalot', name: 'לומדים מתקלות', blurb: 'אירועים אמיתיים מהים: מה קרה, איזה כלל הופר, ומה לומדים מזה.', img: 'crew' },
  { slug: 'milon', name: 'מילון ימי', blurb: 'עמוד לכל מונח ימי, בעברית ובאנגלית.', img: 'globe' },
  { slug: 'klim', name: 'כלים', blurb: 'סימולטור קריאת MAYDAY, משחק זכות קדימה, בוחן אורות ותנאי ים במרינות.', img: 'vhf' },
  { slug: 'israel', name: 'ישראל במים', blurb: 'מרינות, השכרת אופנוע ים, קניית סירה משומשת, ביטוח ורישוי.', img: 'motorboat' },
  { slug: 'ahrei', name: 'אחרי הרישיון', blurb: 'צ\'קליסט להפלגה ראשונה, העונה הראשונה, והמעבר ל-ICC.', img: 'night' },
];

// Feed pages that are not topic sections.
const NEWS = { slug: 'hadash', name: 'חדש מהים', blurb: 'חדשות וסיפורים מהים, כפי שאני מעלה אותם.' };
const VIDEO = { slug: 'video', name: 'סרטונים', blurb: 'סרטונים קצרים: שאלות מהמבחן, הסברים ומקרים מהים.' };

// Licenses. href: the course page; the rest go to /kursim/ until they open.
const COURSES = [
  { id: 'ofnoa', name: 'אופנוע ים', state: 'פתוח להרשמה', live: true, href: '/', img: 'jetski',
    text: '13 שיעורים, כל שאלות המאגר הרשמי והסבר בקול לכל שאלה.' },
  { id: '12', name: 'משיט 12', state: 'בהכנה', href: '/kursim/#12', img: 'speedboat', text: 'סירת מנוע.' },
  { id: '30', name: 'משיט 30', state: 'בהמשך', href: '/kursim/#30', img: 'sail', text: '' },
  { id: '40', name: 'משיט 40', state: 'בהמשך', href: '/kursim/#40', img: 'chart', text: '' },
];

const FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&family=Karantina:wght@700&display=swap" rel="stylesheet">';

const NAV = [
  { slug: 'kursim', name: 'קורסים' },
  { slug: VIDEO.slug, name: VIDEO.name },
  { slug: NEWS.slug, name: NEWS.name },
  ...SECTIONS,
];

function header(active) {
  const cur = s => (s === active ? ' aria-current="page"' : '');
  return `<!-- site-header:start -->
<header class="top" id="top">
  <div class="wrap">
    <a class="logo" href="/v2/" aria-label="אלכס ארגוב, דף הבית"><img src="/assets/logo.jpg" alt="">אלכס ארגוב</a>
    <nav class="menu" id="menu" aria-label="ניווט ראשי">
      ${NAV.map(n => `<a href="/${n.slug}/"${cur(n.slug)}>${n.name}</a>`).join('\n      ')}
    </nav>
    <button class="burger" id="burger" aria-label="תפריט" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
  </div>
</header>
<!-- site-header:end -->`;
}

function footer() {
  const sec = NAV.map(s => `<li><a href="/${s.slug}/">${s.name}</a></li>`).join('');
  const crs = COURSES.map(c => `<li><a href="${c.href}">${c.name}</a></li>`).join('');
  return `<!-- site-footer:start -->
<footer>
  <div class="wrap">
    <div class="fgrid">
      <div>
        <div class="logo">אלכס ארגוב</div>
        <p style="max-width:32ch">מדריך שיט. מלמד תאוריה למבחן, ומה שקורה בים אחרי שעוברים אותו.</p>
      </div>
      <div><h4>קורסים</h4><ul>${crs}</ul></div>
      <div><h4>באתר</h4><ul>${sec}</ul></div>
      <div><h4>דברו איתי</h4><ul><li><a href="https://wa.me/972523682486" target="_blank" rel="noopener">וואטסאפ 052-368-2486</a></li><li><a href="mailto:alex@alargov.com">alex@alargov.com</a></li><li><a href="/legal/refund-policy.html">ביטולים והחזרים</a></li></ul></div>
    </div>
    <div class="fbottom"><span>© אלכס ארגוב, סקיפר דיגיטלי</span><span>* בכפוף לתנאי ההחזר</span></div>
  </div>
</footer>
<script>
(function(){
  var b=document.getElementById('burger'),m=document.getElementById('menu');
  if(b)b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o)});
})();
</script>
<!-- site-footer:end -->`;
}

module.exports = { SECTIONS, NEWS, VIDEO, COURSES, NAV, FONTS, header, footer };
