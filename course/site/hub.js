// New alargov.com (v2): sections from the work plan + shared header / sections grid / footer.
// Single source for every new page. Used by build-sections.js.
const I = {
  magazin: '<path d="M4 4h12v16H6a2 2 0 0 1-2-2z"/><path d="M16 8h4v10a2 2 0 0 1-2 2"/><path d="M8 8h4M8 12h4M8 16h4"/>',
  takalot: '<path d="M12 3l9 16H3z"/><path d="M12 10v4M12 17v.5"/>',
  sidrot: '<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M10 9l5 2-5 2z"/><path d="M7 21h10"/>',
  milon: '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/><path d="M9 8h6"/>',
  klim: '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 11h2M12 11h2M8 15h2M12 15h4"/>',
  israel: '<path d="M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11z"/><circle cx="12" cy="10" r="2"/>',
  ahrei: '<circle cx="12" cy="5" r="2"/><path d="M12 7v14M5 13a7 7 0 0 0 14 0M8 11h8"/>',
};

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

const icon = slug => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${I[slug]}</svg>`;

function header(active) {
  const cur = s => (s === active ? ' aria-current="page"' : '');
  const links = SECTIONS.map(s => `<a href="/${s.slug}/"${cur(s.slug)}>${s.name}</a>`).join('\n      ');
  return `<!-- site-header:start -->
<header class="top">
  <div class="wrap">
    <a class="logo" href="/v2/" aria-label="אלכס ארגוב, דף הבית">
      <svg viewBox="0 0 40 40" fill="none" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#0b5cad"/><path d="M20 8 L20 26 M20 10 L29 24 L20 24 Z" stroke="#f3c24c" stroke-width="2" stroke-linejoin="round"/><path d="M10 27 h20 l-3 4 H13 Z" fill="#fff"/></svg>
      <span>אלכס ארגוב<small>ללמוד ים בעברית</small></span>
    </a>
    <nav class="menu" id="menu" aria-label="ניווט ראשי">
      <a href="/" class="menu-course"${cur('course')}>קורסים</a>
      ${links}
    </nav>
    <div class="top-cta">
      <a class="btn btn-sea btn-sm" href="https://app.alargov.com/">13 שאלות חינם</a>
      <button class="burger" id="burger" aria-label="תפריט" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<!-- site-header:end -->`;
}

function sectionsGrid(except) {
  return `<!-- sections-grid:start -->
    <div class="hubgrid">
${SECTIONS.filter(s => s.slug !== except).map(s =>
  `      <a class="card" href="/${s.slug}/"><div class="ico">${icon(s.slug)}</div><div><h3>${s.name}<span class="soon">בקרוב</span></h3><p>${s.blurb}</p></div></a>`).join('\n')}
    </div>
    <!-- sections-grid:end -->`;
}

function footer() {
  const sec = SECTIONS.map(s => `<li><a href="/${s.slug}/">${s.name}</a></li>`).join('');
  const crs = COURSES.map(c => `<li><a href="${c.href}">${c.name}</a></li>`).join('');
  return `<!-- site-footer:start -->
<footer>
  <div class="wrap">
    <div class="fgrid">
      <div>
        <div class="logo" style="color:#fff;margin-bottom:12px">אלכס ארגוב</div>
        <p style="margin:0;font-size:.93rem;max-width:34ch">מדריך שיט. קורסי הכנה למבחן התאוריה וידע ימי בעברית.</p>
      </div>
      <div><h4>קורסים</h4><ul>${crs}<li><a href="https://app.alargov.com/">13 שאלות חינם</a></li><li><a href="/ofnoa-yam/chukim.html">שאלות לפי נושא</a></li></ul></div>
      <div><h4>ידע ימי</h4><ul>${sec}</ul></div>
      <div><h4>קשר</h4><ul><li><a href="https://wa.me/972523682486" target="_blank" rel="noopener">וואטסאפ · 052-368-2486</a></li><li><a href="/legal/refund-policy.html">ביטולים והחזרים</a></li></ul></div>
    </div>
    <div class="fbottom"><span>© אלכס ארגוב · סקיפר דיגיטלי</span><span>* בכפוף לתנאי ההחזר.</span></div>
  </div>
</footer>
<script>
  (function(){var b=document.getElementById('burger'),m=document.getElementById('menu');
  if(b)b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o)});})();
</script>
<!-- site-footer:end -->`;
}

module.exports = { SECTIONS, COURSES, header, sectionsGrid, footer, icon };
