// Real OSM map image for geographic questions (style of l11 1073/1076 maps). Run from repo root:
//   NODE_PATH=node_modules node tools/l12/map.js <spec.json> <out.png>
// spec: { center:[lat,lng], zoom, title, answer?,
//         markers:[{name, lat, lng, kind:'start'|'answer'|'other'}],
//         route?:[[lat,lng],...], zones?:[{name, poly:[[lat,lng],...]}], lines?:[{name, pts:[[lat,lng],...]}] }
// 1200x850 PNG (the question card shows ~1.4:1); keep key content inside x 130..1070. No answer box: the video reveals the answer itself.
const puppeteer = require('puppeteer');
const fs = require('fs'), path = require('path');
const [specFile, out] = process.argv.slice(2);
const spec = JSON.parse(fs.readFileSync(specFile, 'utf8'));
const html = `<!doctype html><html dir="rtl"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@700;900&display=swap" rel="stylesheet">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>html,body{margin:0}#map{width:1200px;height:850px}
.title{position:absolute;top:24px;left:50%;transform:translateX(-50%);z-index:1000;background:#0c1a3a;color:#fff;font:900 40px Heebo,Arial;padding:14px 28px;border-radius:14px;box-shadow:0 4px 14px rgba(0,0,0,.35);white-space:nowrap}
.ans{position:absolute;bottom:40px;left:50%;transform:translateX(-50%);z-index:1000;background:#0b7a3b;color:#fff;font:900 36px Heebo,Arial;padding:12px 26px;border-radius:14px;white-space:nowrap}
.chip{background:#0c1a3a;color:#fff;font:700 26px Heebo,Arial;padding:4px 12px;border-radius:10px;white-space:nowrap;display:inline-block}
.chip.answer{background:#0b7a3b}.chip.start{background:#1d4ed8}
.dot{width:22px;height:22px;border-radius:50%;background:#e11d48;border:3px solid #fff;box-shadow:0 0 0 2px #0c1a3a}
.dot.answer{background:#16a34a}.dot.start{background:#2563eb}
.rose{position:absolute;right:150px;bottom:60px;z-index:1000;width:110px;height:110px}
</style></head><body><div id="map"></div>
<div class="title">${spec.title}</div>${spec.answer ? `<div class="ans">${spec.answer}</div>` : ''}
<svg class="rose" viewBox="0 0 100 100"><circle cx="50" cy="50" r="46" fill="#fff" fill-opacity=".85" stroke="#0c1a3a" stroke-width="3"/>
<polygon points="50,8 58,50 50,44 42,50" fill="#e11d48"/><polygon points="50,92 58,50 50,56 42,50" fill="#0c1a3a"/>
<text x="50" y="30" text-anchor="middle" font-family="Arial" font-weight="900" font-size="16" fill="#0c1a3a">N</text></svg>
<script>
const S=${JSON.stringify(spec)};
const map=L.map('map',{zoomControl:false,attributionControl:true,zoomSnap:0.25}).setView(S.center,S.zoom);
const tl=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap'}).addTo(map);
(S.zones||[]).forEach(z=>{const pg=L.polygon(z.poly,{color:'#e11d48',weight:3,fillColor:'#e11d48',fillOpacity:.35}).addTo(map);if(z.name)pg.bindTooltip(z.name,{permanent:true,direction:'center',className:'chip'});});
(S.lines||[]).forEach(l=>L.polyline(l.pts,{color:'#e11d48',weight:4,dashArray:'10 8'}).addTo(map).bindTooltip(l.name,{permanent:true,direction:'bottom',className:'chip'}));
if(S.route) L.polyline(S.route,{color:'#2563eb',weight:6,dashArray:'14 10'}).addTo(map);
(S.markers||[]).forEach(m=>{const k=m.kind||'other';
  L.marker([m.lat,m.lng],{icon:L.divIcon({className:'',html:'<div class="dot '+k+'"></div>',iconSize:[28,28],iconAnchor:[14,14]})}).addTo(map)
   .bindTooltip('<span class="chip '+k+'">'+m.name+'</span>',{permanent:true,direction:m.dir||'left',offset:[m.dir==='right'?6:-6,m.dy||0],opacity:1,className:''});});
let loaded=false;tl.on('load',()=>{if(!loaded){loaded=true;setTimeout(()=>window.__mapReady=true,2500)}});
setTimeout(()=>window.__mapReady=true,15000);
</script></body></html>`;
(async () => {
  const tmp = path.resolve(out + '.html');
  fs.writeFileSync(tmp, html);
  const b = await puppeteer.launch({ headless: 'new' });
  const p = await b.newPage();
  await p.setViewport({ width: 1200, height: 850 });
  await p.goto('file:///' + tmp.replace(/\\/g, '/'), { waitUntil: 'networkidle0', timeout: 60000 });
  await p.waitForFunction('window.__mapReady===true', { timeout: 30000 });
  await p.screenshot({ path: out });
  await b.close();
  fs.unlinkSync(tmp);
})();
