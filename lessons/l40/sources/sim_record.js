// Records real screen clips of the l40 GMDSS simulator (lessons/l40/simulator) for lesson 9.
// usage: node sim_record.js <clip|shot> <outfile>   clips: dsc | mayday | abandon ; 'shot' = screenshot after the DSC+MAYDAY exchange
// Needs the simulator server (node tools/gmdss-sim-server.js, port 8911). NODE_PATH=<project>/node_modules
const puppeteer = require('puppeteer');
const URL = 'http://localhost:8911/';
const MAYDAY = 'Mayday mayday mayday. This is motor yacht Noa Noa Noa. MMSI 4 2 8 6 5 4 3 2 1. Mayday Noa. Position 3 2 degrees 5 0 minutes North, 0 3 4 degrees 4 8 minutes East. On fire in the engine room. Require immediate assistance. 6 persons on board. Over';
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function center(p, sel) { const b = await (await p.$(sel)).boundingBox(); return [b.x + b.width / 2, b.y + b.height / 2]; }
async function click(p, sel, wait = 900) { const [x, y] = await center(p, sel); await p.mouse.move(x, y, {steps: 8}); await p.mouse.click(x, y); await sleep(wait); }
async function hold(p, sel, ms) { const [x, y] = await center(p, sel); await p.mouse.move(x, y, {steps: 8}); await p.mouse.down(); await sleep(ms); await p.mouse.up(); }
async function soft(p, s, wait = 700) { await click(p, `.softkeys .k[data-s="${s}"]`, wait); }

async function open(p) {
  await p.goto(URL, {waitUntil: 'networkidle0'});
  await sleep(600);
  const skip = await p.evaluateHandle(() => [...document.querySelectorAll('#gcard button')].find(b => /דלג/.test(b.textContent)));
  if (skip.asElement()) await skip.asElement().click();
  await sleep(500);
  await p.select('#scSel', 'noa'); await sleep(600);
  await p.evaluate(() => window.scrollTo(0, 0));
}
async function power(p) { await hold(p, '#kPwr', 150); await sleep(900); }
async function dsc(p, pace = 1) {
  await click(p, '#cover', 900 * pace);
  await click(p, '#kDis', 900 * pace);              // short press: nature list
  await soft(p, 1, 800 * pace); await soft(p, 2, 900 * pace);   // down to FIRE/EXPLOSION, select
  await hold(p, '#kDis', 5700);                    // hold 5 s: DSC sent
  await sleep(1500);
}
async function sendMayday(p, typeDelay) {
  await p.click('#typed'); await p.type('#typed', MAYDAY, {delay: typeDelay});
  await sleep(600); await click(p, '#sendTyped', 500);
}

(async () => {
  const [what, out] = process.argv.slice(2);
  const b = await puppeteer.launch({headless: 'new', args: ['--autoplay-policy=no-user-gesture-required']});
  const p = await b.newPage();
  await p.setViewport({width: 1600, height: 900});
  await open(p);
  let rec = null;
  const start = async () => { rec = await p.screencast({path: out}); await sleep(500); };
  if (what === 'dsc') { await start(); await power(p); await dsc(p); await sleep(7000); }
  else if (what === 'mayday') { await power(p); await dsc(p, 0.4); await start(); await sleep(800); await sendMayday(p, 28); await sleep(9000); }
  else if (what === 'abandon') {
    await power(p); await dsc(p, 0.4); await sendMayday(p, 1); await sleep(26000);
    await start(); await sleep(800);
    await click(p, '#eRelease', 1100); await click(p, '#eGuard', 1100); await click(p, '#eOn', 1800);
    await click(p, '#sOn', 1200); await click(p, '#sHigh', 1500);
    await click(p, '#speed', 500); await sleep(9000);
  }
  else if (what === 'shot') { await power(p); await dsc(p, 0.4); await sendMayday(p, 1); await sleep(8000); await p.screenshot({path: out}); }
  if (rec) await rec.stop();
  await b.close();
})();
