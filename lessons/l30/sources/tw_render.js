// tw_render.js: render an HTML overlay (Tailwind via CDN) to a transparent PNG.
//   node tw_render.js <in.html> <out.png> <width> <height>
const puppeteer = require('puppeteer');
const path = require('path');
(async () => {
  const [inp, out, w, h] = process.argv.slice(2);
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: +w, height: +h, deviceScaleFactor: 1 });
  await page.goto('file:///' + path.resolve(inp).replace(/\\/g, '/'), { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts.ready);
  const fit = await page.evaluate(() => {                       // vertical cards: [data-max-lines] must not wrap past N lines
    const bad = [];
    document.querySelectorAll('[data-max-lines]').forEach(el => {
      const lh = parseFloat(getComputedStyle(el).lineHeight); const n = Math.round(el.scrollHeight / lh);
      if (n > +el.dataset.maxLines) bad.push(el.dataset.name + ' ' + n + '>' + el.dataset.maxLines);
    });
    const root = document.querySelector('[data-page]');
    if (root && root.scrollHeight > root.clientHeight + 1) bad.push('page height ' + root.scrollHeight);
    return bad;
  });
  if (fit.length) console.log('OVERFLOW ' + fit.join(' | '));
  await page.screenshot({ path: out, omitBackground: true });
  await browser.close();
  console.log('ok', out);
})();
