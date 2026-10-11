// Google Analytics 4 (stream "Alargov", G-83P9GF8N1N). Only on the real domain, so staging/localhost don't pollute the data.
(function () {
  if (!/(^|\.)alargov\.com$/.test(location.hostname)) return;
  var id = 'G-83P9GF8N1N', s = document.createElement('script');
  s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { dataLayer.push(arguments); };
  gtag('js', new Date()); gtag('config', id);
})();
