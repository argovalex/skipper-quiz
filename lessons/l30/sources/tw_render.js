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
  await page.screenshot({ path: out, omitBackground: true });
  await browser.close();
  console.log('ok', out);
})();
