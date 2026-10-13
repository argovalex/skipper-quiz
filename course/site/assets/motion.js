// Site motion: Lenis smooth scroll + hero parallax + reveal-on-scroll.
// Loaded on every page built by build-site.js. Does nothing under prefers-reduced-motion.
(function () {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || typeof Lenis === 'undefined') return;

  var lenis = new Lenis({ lerp: 0.09, wheelMultiplier: 1, anchors: { offset: -80 }, autoRaf: true });
  window.lenis = lenis;

  // Pause page scroll while the video player overlay is open.
  var pl = document.getElementById('player');
  if (pl) new MutationObserver(function () {
    pl.classList.contains('open') ? lenis.stop() : lenis.start();
  }).observe(pl, { attributes: true, attributeFilter: ['class'] });

  // Hero strip: media drifts slower than the page, copy lifts and fades out.
  var strip = document.querySelector('.strip');
  if (strip) {
    var media = strip.querySelectorAll('video,.poster'), copy = strip.querySelector('.strip-copy');
    lenis.on('scroll', function (e) {
      var h = strip.offsetHeight, y = Math.min(e.scroll, h);
      media.forEach(function (m) { m.style.transform = 'translate3d(0,' + (y * 0.35) + 'px,0) scale(1.08)'; });
      if (copy) { copy.style.transform = 'translate3d(0,' + (y * -0.15) + 'px,0)'; copy.style.opacity = 1 - y / h * 1.2; }
    });
  }

  // Reveal: fade-up as items enter the viewport, staggered within the same parent.
  var sel = '.app-shots figure,.app-copy,.board .tile,.story,.reel,.course,.news-item,.pagehead,.about,.watch-head,.feed h2';
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px 15% 0px', threshold: 0 }); // fire just before an item scrolls in, so fast scrolling never shows empty gaps
  document.querySelectorAll(sel).forEach(function (el) {
    var sibs = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
    el.style.setProperty('--rv-d', Math.min(sibs, 8) * 70 + 'ms');
    el.classList.add('rv');
    io.observe(el);
  });
})();
