// Site sections + the shared hub bar markup. Single source for every page's top strip.
// Used by build-sections.js (section pages + landing page) and build-topics.js (topic pages).
const SECTIONS = [
  { slug: 'magazin', name: 'מגזין', blurb: 'סיפורים מהים, תקלות אמיתיות ומה לומדים מהן.' },
  { slug: 'sidrot', name: 'סדרות', blurb: 'סדרות קצרות שעוברות נושא אחד לעומק, פרק אחרי פרק.' },
  { slug: 'milon', name: 'מילון', blurb: 'מונחי ים בעברית ובאנגלית, עם הסבר קצר לכל מונח.' },
  { slug: 'kelim', name: 'כלים', blurb: 'מחשבונים וכלים קטנים ליציאה לים.' },
  { slug: 'israel-bamayim', name: 'ישראל במים', blurb: 'מרינות, חופים ואזורי שיט לאורך החוף.' },
  { slug: 'acharei-harishayon', name: 'אחרי הרישיון', blurb: 'מה עושים כשהרישיון כבר בכיס.' },
];

function hubHeader(active) {
  const links = SECTIONS.map(s =>
    `<a href="/${s.slug}/"${s.slug === active ? ' aria-current="page"' : ''}>${s.name}</a>`
  ).join('\n      ');
  return `<!-- hub:start -->
<div class="hub">
  <div class="hub-in">
    <a class="hub-home" href="/">⚓ <b>ידע ימי</b></a>
    <div class="hub-links" role="navigation" aria-label="מדורי האתר">
      ${links}
    </div>
    <a class="hub-course" href="/">קורס רשיון אופנוע ים</a>
  </div>
</div>
<!-- hub:end -->`;
}

module.exports = { SECTIONS, hubHeader };
