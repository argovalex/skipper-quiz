// Purchase hand-off for the new site — same flow as the current landing page (index.html):
// the site never takes payment itself. "רכוש עכשיו" opens the course app with ?buy=1, the app
// registers the student and opens the Tranzila hosted payment page through the API
// (course/api: /api/checkout -> direct.tranzila.com, /api/tranzila/notify issues the access code).
//
//   <a data-buy>      -> https://app.alargov.com/?buy=1[&ref=...]
//   <a data-trial>    -> https://app.alargov.com/[?ref=...]   (13 free questions, no signup)
//   [data-price]      -> current price (founders or regular) from /api/config
//   [data-price-regular], [data-seats], [data-founders] (hidden when the founders seats are gone)
// ?ref=<partner> is kept in localStorage (sq_ref, shared with the landing page) and carried along.
(function () {
  var APP = 'https://app.alargov.com/';
  var meta = document.querySelector('meta[name=sq-api]');
  var API = '';
  try { API = (localStorage.getItem('sq_api') || (meta && meta.content) || '').replace(/\/$/, ''); } catch (e) { API = meta ? meta.content : ''; }

  var REF = (function () {
    try {
      var r = new URLSearchParams(location.search).get('ref');
      if (r) { r = r.replace(/[^\w-]/g, '').slice(0, 32); if (r) localStorage.setItem('sq_ref', r); }
      return localStorage.getItem('sq_ref') || '';
    } catch (e) { return ''; }
  })();

  var APP_URL = APP + (REF ? '?ref=' + encodeURIComponent(REF) : '');
  var BUY_URL = APP_URL + (APP_URL.indexOf('?') > -1 ? '&' : '?') + 'buy=1';
  function wire(sel, url) {
    document.querySelectorAll(sel).forEach(function (a) {
      a.setAttribute('href', url);
      a.addEventListener('click', function (e) { e.preventDefault(); location.href = url; });
    });
  }
  wire('a[data-buy]', BUY_URL);
  wire('a[data-trial]', APP_URL);

  if (REF) document.querySelectorAll('a[href*="wa.me"]').forEach(function (a) {
    try {
      var u = new URL(a.href);
      var t = u.searchParams.get('text') || 'היי, אני מעוניין בפרטים על קורס ההכנה למבחן התאוריה';
      u.searchParams.set('text', t + ' (הגעתי דרך ' + REF + ')');
      a.href = u.toString();
    } catch (e) {}
  });

  // Live price and founders seats. On any failure the static text in the page stays.
  if (!API || !document.querySelector('[data-price],[data-seats],[data-founders]')) return;
  fetch(API + '/api/config').then(function (r) { return r.json(); }).then(function (j) {
    var p = j && j.pricing; if (!p) return;
    var left = Number(p.founders_left), slots = Number(p.founders_slots), taken = Number(p.founders_taken);
    var founders = p.is_founders && left > 0;
    document.querySelectorAll('[data-price]').forEach(function (el) { el.textContent = '₪' + p.price; });
    document.querySelectorAll('[data-price-regular]').forEach(function (el) { el.textContent = '₪' + p.price_regular; el.hidden = !founders; });
    document.querySelectorAll('[data-seats]').forEach(function (el) {
      el.textContent = founders
        ? 'נותרו ' + left + ' מקומות במחיר מייסדים מתוך ' + slots + (taken > 0 ? ' · ' + taken + ' כבר נרשמו' : '')
        : 'רישום פתוח · ₪' + p.price_regular;
      el.hidden = false;
    });
    if (!founders) document.querySelectorAll('[data-founders]').forEach(function (el) { el.hidden = true; });
    if (j.checkout_open === false) document.querySelectorAll('a[data-buy]').forEach(function (a) {
      a.textContent = 'הרשמה תיפתח בקרוב'; a.setAttribute('aria-disabled', 'true');
    });
  }).catch(function () {});
})();
