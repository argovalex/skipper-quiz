// Rasterize a Leaflet map page to PNG. usage: NODE_PATH=<project>/node_modules node map_shot.js <page.html> <out.png> <w> <h>
const puppeteer = require('puppeteer');
const [src, out, w, h] = process.argv.slice(2);
(async () => {
  const b = await puppeteer.launch({headless: 'new'});
  const p = await b.newPage();
  await p.setViewport({width: +w, height: +h});
  await p.goto('file:///' + src.replace(/\\/g, '/'), {waitUntil: 'networkidle0'});
  await p.waitForFunction('window.__mapReady === true', {timeout: 60000});
  await p.screenshot({path: out});
  await b.close();
})();
