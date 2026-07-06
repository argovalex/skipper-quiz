const fs = require('fs');
const path = require('path');
const questions = require('../questions.json');

const CX = 180, CY = 210;
const R_TIP = 55, R_BASE = 120, R_LABEL = 140;
const LETTERS = 'ABCDEFGHIJKLMNOP'.split('');

function pos(angleDeg, radius) {
  const rad = (angleDeg - 90) * Math.PI / 180;
  return { x: CX + radius * Math.cos(rad), y: CY + radius * Math.sin(rad) };
}

function vesselAngle(letter) {
  return LETTERS.indexOf(letter) * 22.5;
}

function vesselColor(idx) {
  const colors = [
    '#1a3fd6','#8a8a8a','#2ecc40','#ff8c1a',
    '#e6007a','#ff8c1a','#2ecc40','#8a8a8a',
    '#e6007a','#8a8a8a','#2ecc40','#ff8c1a',
    '#1a3fd6','#ff8c1a','#2ecc40','#8a8a8a'
  ];
  return colors[idx % colors.length];
}

function drawVessel(letter) {
  const idx = LETTERS.indexOf(letter);
  const angle = idx * 22.5;
  const color = vesselColor(idx);
  const isFlipped = (letter === 'E' || letter === 'I');

  // E and I: tip (narrow) points OUTWARD, base (wide) near center
  // All others: tip (narrow) points INWARD toward center, base (wide) far out
  const tip = pos(angle, isFlipped ? R_BASE : R_TIP);
  const baseL = pos(angle - 5, isFlipped ? R_TIP : R_BASE);
  const baseR = pos(angle + 5, isFlipped ? R_TIP : R_BASE);
  const lbl = pos(angle, R_LABEL);

  let svg = `<polygon points="${tip.x.toFixed(1)},${tip.y.toFixed(1)} ${baseL.x.toFixed(1)},${baseL.y.toFixed(1)} ${baseR.x.toFixed(1)},${baseR.y.toFixed(1)}" fill="${color}" stroke="#000" stroke-width="1.2"/>`;
  svg += `<rect x="${(lbl.x-11).toFixed(1)}" y="${(lbl.y-11).toFixed(1)}" width="22" height="22" fill="#fff" stroke="${color}" stroke-width="2.2"/>`;
  svg += `<text x="${lbl.x.toFixed(1)}" y="${(lbl.y+5).toFixed(1)}" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="900" fill="${color}">${letter}</text>`;
  return svg;
}

function drawHighlight(letter) {
  const angle = vesselAngle(letter);
  const p = pos(angle, R_LABEL);
  return `<circle cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="26" fill="none" stroke="#ffd700" stroke-width="3"><animate attributeName="r" values="20;28;20" dur="1.4s" repeatCount="indefinite"/></circle>`;
}

function drawBowLine(letter, color) {
  const idx = LETTERS.indexOf(letter);
  const angle = idx * 22.5;
  const isFlipped = (letter === 'E' || letter === 'I');
  const tipR = isFlipped ? R_BASE : R_TIP;
  const from = pos(angle, tipR);
  const to = pos(angle, isFlipped ? tipR + 50 : tipR - 45);
  return `<line x1="${from.x.toFixed(1)}" y1="${from.y.toFixed(1)}" x2="${to.x.toFixed(1)}" y2="${to.y.toFixed(1)}" stroke="#111" stroke-width="3.5" stroke-dasharray="6,3" opacity="0.9"/>`;
}

// Day shape SVG generators — drawn inside compass (below vessel) so both are visible
function dayShapeAt(letter, shapeId) {
  const angle = vesselAngle(letter);
  const shapeR = R_TIP - 32;
  const p = pos(angle, shapeR);
  const shapes = DAY_SHAPES[shapeId];
  if (!shapes) return `<!-- unknown shape ${shapeId} -->`;

  // White background circle behind the shape for visibility
  let svg = `<circle cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="32" fill="#fff" stroke="#333" stroke-width="1.5" opacity="0.92"/>`;
  svg += shapes(p.x, p.y, angle);

  // Label: letter + image number, placed further inside
  const lp = pos(angle, shapeR - 36);
  svg += `<rect x="${(lp.x - 30).toFixed(1)}" y="${(lp.y - 7).toFixed(1)}" width="60" height="14" rx="3" fill="#0c1a3a" opacity="0.85"/>`;
  svg += `<text x="${lp.x.toFixed(1)}" y="${(lp.y + 4).toFixed(1)}" text-anchor="middle" font-family="Heebo,sans-serif" font-size="8.5" font-weight="700" fill="#fff">${letter} | תמונה ${shapeId}</text>`;
  return svg;
}

function ball(cx, cy, r = 8) {
  return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="#111"/>`;
}

function diamond(cx, cy, s = 9) {
  return `<polygon points="${cx},${cy-s} ${cx+s},${cy} ${cx},${cy+s} ${cx-s},${cy}" fill="#111"/>`;
}

function coneDown(cx, cy, s = 9) {
  return `<polygon points="${cx-s},${cy-s} ${cx+s},${cy-s} ${cx},${cy+s}" fill="#111"/>`;
}

function coneUp(cx, cy, s = 9) {
  return `<polygon points="${cx},${cy-s} ${cx+s},${cy+s} ${cx-s},${cy+s}" fill="#111"/>`;
}

function cylinder(cx, cy) {
  return `<rect x="${cx-7}" y="${cy-10}" width="14" height="20" rx="3" fill="#111"/>`;
}

const DAY_SHAPES = {
  // NUC: 2 black balls
  80: (cx, cy) => {
    return `<g transform="translate(${cx},${cy})">` +
      ball(0, -12, 6) + ball(0, 12, 6) +
      `<line x1="0" y1="-20" x2="0" y2="20" stroke="#111" stroke-width="2"/>` +
      `</g>`;
  },
  // Aground: 3 black balls (vertical)
  10: (cx, cy) => {
    return `<g transform="translate(${cx},${cy})">` +
      ball(0, -16, 6) + ball(0, 0, 6) + ball(0, 16, 6) +
      `<line x1="0" y1="-24" x2="0" y2="24" stroke="#111" stroke-width="2"/>` +
      `</g>`;
  },
  // At anchor: 1 black ball
  77: (cx, cy) => ball(cx, cy, 10),
  // Sailing under engine: cone point down
  20: (cx, cy) => coneDown(cx, cy, 10),
  // Constrained by draught: cylinder
  75: (cx, cy) => `<rect x="${cx-9}" y="${cy-14}" width="18" height="28" rx="3" fill="#111"/>`,
  // Minesweeping: 3 balls in triangle
  76: (cx, cy) => {
    return `<g transform="translate(${cx},${cy})">` +
      ball(0, -14, 6) + ball(-14, 10, 6) + ball(14, 10, 6) +
      `<line x1="0" y1="-20" x2="0" y2="4" stroke="#111" stroke-width="2"/>` +
      `<line x1="-14" y1="4" x2="14" y2="4" stroke="#111" stroke-width="2"/>` +
      `</g>`;
  },
  // RAM (restricted ability to maneuver): ball-diamond-ball
  79: (cx, cy) => {
    return `<g transform="translate(${cx},${cy})">` +
      ball(0, -16, 6) + diamond(0, 0, 7) + ball(0, 16, 6) +
      `<line x1="0" y1="-24" x2="0" y2="24" stroke="#111" stroke-width="1.5"/>` +
      `</g>`;
  },
  // Distress signal: square flag + ball
  83: (cx, cy) => {
    return `<g transform="translate(${cx},${cy})">` +
      `<rect x="-8" y="-18" width="16" height="14" fill="#e74c3c" stroke="#111" stroke-width="1.2"/>` +
      ball(0, 10, 6) +
      `<line x1="0" y1="-18" x2="0" y2="18" stroke="#111" stroke-width="1.5"/>` +
      `</g>`;
  },
  // Towing: 2 cones (hourglass)
  81: (cx, cy) => {
    return `<g transform="translate(${cx},${cy})">` +
      coneDown(0, -8, 9) + coneUp(0, 10, 9) +
      `<line x1="0" y1="-18" x2="0" y2="20" stroke="#111" stroke-width="1.5"/>` +
      `</g>`;
  },
  // Fishing: 2 cones (basket shape)
  84: (cx, cy) => {
    return `<g transform="translate(${cx},${cy})">` +
      coneDown(0, -8, 9) + coneUp(0, 10, 9) +
      `<line x1="0" y1="-18" x2="0" y2="20" stroke="#111" stroke-width="1.5"/>` +
      `</g>`;
  },
  // Towing >200m: diamond
  86: (cx, cy) => diamond(cx, cy, 12),
  // Vessel engaged in work (RAM variant): ball-diamond-ball + side diamonds
  87: (cx, cy) => {
    return `<g transform="translate(${cx},${cy})">` +
      ball(0, -16, 6) + diamond(0, 0, 7) + ball(0, 16, 6) +
      `<line x1="0" y1="-24" x2="0" y2="24" stroke="#111" stroke-width="1.5"/>` +
      diamond(18, -8, 5) + diamond(18, 8, 5) +
      `</g>`;
  },
  // Vessel engaged in work variant (obstructed side): ball-diamond-ball + side balls
  89: (cx, cy) => {
    return `<g transform="translate(${cx},${cy})">` +
      ball(0, -16, 6) + diamond(0, 0, 7) + ball(0, 16, 6) +
      `<line x1="0" y1="-24" x2="0" y2="24" stroke="#111" stroke-width="1.5"/>` +
      ball(18, -8, 5) + ball(18, 8, 5) +
      `</g>`;
  },
  // Vessel engaged in work variant (both sides)
  90: (cx, cy) => {
    return `<g transform="translate(${cx},${cy})">` +
      ball(0, -16, 6) + diamond(0, 0, 7) + ball(0, 16, 6) +
      `<line x1="0" y1="-24" x2="0" y2="24" stroke="#111" stroke-width="1.5"/>` +
      diamond(-18, -8, 5) + diamond(-18, 8, 5) +
      ball(18, -8, 5) + ball(18, 8, 5) +
      `</g>`;
  },
  // Flags — rendered as swallowtail flags on a pole
  92: (cx, cy) => `<g transform="translate(${cx},${cy})"><line x1="0" y1="-20" x2="0" y2="10" stroke="#333" stroke-width="2"/><rect x="1" y="-20" width="18" height="14" fill="#fff" stroke="#111" stroke-width="1"/><line x1="1" y1="-20" x2="19" y2="-6" stroke="#e74c3c" stroke-width="2"/><line x1="1" y1="-6" x2="19" y2="-20" stroke="#e74c3c" stroke-width="2"/><text x="10" y="-10" text-anchor="middle" font-family="Arial" font-size="9" font-weight="900" fill="#e74c3c">V</text></g>`,
  93: (cx, cy) => `<g transform="translate(${cx},${cy})"><line x1="0" y1="-20" x2="0" y2="10" stroke="#333" stroke-width="2"/><rect x="1" y="-20" width="18" height="14" fill="#0055BF" stroke="#111" stroke-width="1"/><rect x="5" y="-17" width="5" height="4" fill="#fff"/><rect x="10" y="-13" width="5" height="4" fill="#fff"/><rect x="5" y="-9" width="5" height="4" fill="#fff"/><text x="10" y="-3" text-anchor="middle" font-family="Arial" font-size="9" font-weight="900" fill="#0055BF">N</text></g>`,
  95: (cx, cy) => `<g transform="translate(${cx},${cy})"><line x1="0" y1="-20" x2="0" y2="10" stroke="#333" stroke-width="2"/><polygon points="1,-20 20,-20 14,-13 20,-6 1,-6" fill="#e74c3c" stroke="#111" stroke-width="1"/><text x="9" y="-10" text-anchor="middle" font-family="Arial" font-size="10" font-weight="900" fill="#fff">B</text></g>`,
  98: (cx, cy) => `<g transform="translate(${cx},${cy})"><line x1="0" y1="-20" x2="0" y2="10" stroke="#333" stroke-width="2"/><polygon points="1,-20 20,-20 14,-13 20,-6 1,-6" fill="#0055BF" stroke="#111" stroke-width="1"/><polygon points="1,-13 14,-13 11,-10 14,-6 1,-6" fill="#fff" stroke="none"/><text x="9" y="-3" text-anchor="middle" font-family="Arial" font-size="9" font-weight="900" fill="#0055BF">A</text></g>`,
  104: (cx, cy) => `<g transform="translate(${cx},${cy})"><line x1="0" y1="-20" x2="0" y2="10" stroke="#333" stroke-width="2"/><polygon points="1,-20 20,-20 14,-13 20,-6 1,-6" fill="#e74c3c" stroke="#111" stroke-width="1"/><rect x="4" y="-17" width="9" height="4" fill="#ffd700"/><rect x="4" y="-9" width="9" height="4" fill="#ffd700"/><text x="9" y="-3" text-anchor="middle" font-family="Arial" font-size="9" font-weight="900" fill="#e74c3c">B</text></g>`,
  106: (cx, cy) => `<g transform="translate(${cx},${cy})"><line x1="0" y1="-20" x2="0" y2="10" stroke="#333" stroke-width="2"/><rect x="1" y="-20" width="6" height="14" fill="#0055BF" stroke="none"/><rect x="7" y="-20" width="6" height="14" fill="#fff" stroke="none"/><rect x="13" y="-20" width="6" height="14" fill="#e74c3c" stroke="none"/><rect x="1" y="-20" width="18" height="14" fill="none" stroke="#111" stroke-width="1"/><text x="10" y="-3" text-anchor="middle" font-family="Arial" font-size="9" font-weight="900" fill="#0055BF">W</text></g>`,
};

// Reusable compass rose SVG (just the arrows + labels, no question-specific elements)
function buildCompassRoseSvg() {
  let svg = '';
  svg += `<rect x="10" y="10" width="340" height="400" fill="#fff" stroke="#0c1a3a" stroke-width="2"/>`;
  const D = R_LABEL + 20;
  svg += `<line x1="${CX}" y1="${CY-D}" x2="${CX}" y2="${CY+D}" stroke="#333" stroke-width="0.6" stroke-dasharray="2,2"/>`;
  svg += `<line x1="${CX-D}" y1="${CY}" x2="${CX+D}" y2="${CY}" stroke="#333" stroke-width="0.6" stroke-dasharray="2,2"/>`;
  const d45 = Math.round(D * 0.707);
  svg += `<line x1="${CX-d45}" y1="${CY-d45}" x2="${CX+d45}" y2="${CY+d45}" stroke="#333" stroke-width="0.5" stroke-dasharray="2,2"/>`;
  svg += `<line x1="${CX+d45}" y1="${CY-d45}" x2="${CX-d45}" y2="${CY+d45}" stroke="#333" stroke-width="0.5" stroke-dasharray="2,2"/>`;
  for (const letter of LETTERS) svg += drawVessel(letter);
  return svg;
}

function buildScene(observer, target, shapeId, headerText) {
  let svg = `<svg width="100%" height="100%" viewBox="0 0 360 420" preserveAspectRatio="xMidYMid slice">`;
  // White card background
  svg += `<rect x="10" y="10" width="340" height="400" fill="#fff" stroke="#0c1a3a" stroke-width="2"/>`;
  // Compass crosshairs
  const D = R_LABEL + 20;
  svg += `<line x1="${CX}" y1="${CY-D}" x2="${CX}" y2="${CY+D}" stroke="#333" stroke-width="0.6" stroke-dasharray="2,2"/>`;
  svg += `<line x1="${CX-D}" y1="${CY}" x2="${CX+D}" y2="${CY}" stroke="#333" stroke-width="0.6" stroke-dasharray="2,2"/>`;
  const d45 = Math.round(D * 0.707);
  svg += `<line x1="${CX-d45}" y1="${CY-d45}" x2="${CX+d45}" y2="${CY+d45}" stroke="#333" stroke-width="0.5" stroke-dasharray="2,2"/>`;
  svg += `<line x1="${CX+d45}" y1="${CY-d45}" x2="${CX-d45}" y2="${CY+d45}" stroke="#333" stroke-width="0.5" stroke-dasharray="2,2"/>`;

  // Header banner (drawn first so vessels render on top)
  svg += `<rect x="30" y="18" width="300" height="30" rx="6" fill="#0c1a3a" stroke="#7eb8f7" stroke-width="1"/>`;
  svg += `<text x="180" y="38" text-anchor="middle" fill="#7eb8f7" font-size="10.5" font-family="Heebo,sans-serif" font-weight="900">${headerText}</text>`;

  // Draw all 16 vessels
  for (const letter of LETTERS) {
    svg += drawVessel(letter);
  }

  // Day shape on target vessel
  if (target && shapeId) {
    svg += dayShapeAt(target, shapeId);
  }

  // Bow heading lines for selected vessels
  if (observer) svg += drawBowLine(observer, '#ffd700');
  if (target) svg += drawBowLine(target, '#e74c3c');

  // Highlight observer and target
  if (observer) svg += drawHighlight(observer);
  if (target) svg += drawHighlight(target);

  // Answer overlay (hidden, shown by script)
  svg += `<g id="ov" opacity="0">`;
  svg += `<rect x="60" y="365" width="240" height="38" rx="19" fill="#0d3d2a" stroke="#2ecc71" stroke-width="2" opacity="0.95"/>`;
  svg += `<text id="ovText" x="180" y="389" text-anchor="middle" fill="#2ecc71" font-size="20" font-family="Heebo,sans-serif" font-weight="900">✅ נכון!</text>`;
  svg += `</g>`;

  svg += `</svg>`;
  return svg;
}

function buildHtml(q, scene) {
  const optLetters = ['א', 'ב', 'ג', 'ד'];
  const correctIdx = optLetters.indexOf(q.answer);
  const cleanOpts = q.options.map(o => o.replace(/^[א-ד]\.\s*/, ''));

  const optsHtml = cleanOpts.map((o, i) =>
    `<div class="opt" id="o${i}"><div class="ltr">${optLetters[i]}</div>${o}</div>`
  ).join('');

  return `<!DOCTYPE html>
<html dir="rtl" lang="he"><head><meta charset="UTF-8">
<title>Skipper Quiz #${q.num} — רישיון 11</title>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;display:flex;align-items:center;justify-content:center;height:100vh;overflow:hidden}
#reel{width:390px;height:625px;background:#0c1a3a;overflow:hidden;position:relative;display:flex;flex-direction:column;font-family:'Heebo',sans-serif;direction:rtl}
#hdr{background:#0c1a3a;padding:14px 16px 10px;flex-shrink:0;border-bottom:2px solid #1e3a6e;text-align:center}
.brand{color:#7eb8f7;font-size:11px;font-weight:700;letter-spacing:2px;margin-bottom:2px}
.htitle{color:#fff;font-size:18px;font-weight:900}
#scene{flex:1;position:relative;overflow:hidden}
#ftr{background:#0c1a3a;padding:12px 16px;flex-shrink:0;border-top:2px solid #1e3a6e}
.ql{color:#7eb8f7;font-size:11px;font-weight:700;letter-spacing:1px;margin-bottom:5px}
.qt{color:#fff;font-size:13px;font-weight:700;line-height:1.4;margin-bottom:8px}
.opts{display:flex;flex-direction:column;gap:5px}
.opt{background:#1a2f5e;border:1px solid #2a4a8a;border-radius:7px;padding:7px 10px;color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center;gap:8px;transition:all 0.5s}
.ltr{background:#0c1a3a;color:#7eb8f7;font-size:11px;min-width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-weight:900}
.opt.correct{background:#0d3d2a;border-color:#2ecc71;color:#2ecc71}
.opt.correct .ltr{background:#2ecc71;color:#0d3d2a}
.opt.wrong{background:#3d1a1a;border-color:#e74c3c;color:#e74c3c}
.opt.wrong .ltr{background:#e74c3c;color:#fff}
.opt.dim{opacity:0.3}
#prog{position:absolute;bottom:0;left:0;height:2px;background:#4a90d9;width:0;z-index:5}
</style></head><body>
<div id="reel">
  <div id="hdr"><div class="brand">⚓ SKIPPER QUIZ</div><div class="htitle">מבחן הסקיפר היומי של אלכס ארגוב</div></div>
  <div id="scene">
    ${scene}
    <div id="prog"></div>
  </div>
  <div id="ftr">
    <div class="ql" id="ql">❓ שאלה ${q.num}</div>
    <div class="qt" id="qt">${q.q_he}</div>
    <div class="opts" id="opts">${optsHtml}</div>
  </div>
</div>
<script>
const C=${correctIdx};
const OPTS=${JSON.stringify(cleanOpts)};
const E=${JSON.stringify(q.explanation || '')};
window.__startAutoPlay = function(){
const prog=document.getElementById('prog');
const DELAY=15000;
prog.style.transition='none';prog.style.width='0%';
setTimeout(()=>{prog.style.transition='width '+DELAY+'ms linear';prog.style.width='100%';},30);
setTimeout(()=>{
  document.querySelectorAll('.opt').forEach((o,j)=>{
    o.style.transition='all 0.6s';
    if(j===C)o.classList.add('correct'); else o.classList.add('dim');
  });
  const ov=document.getElementById('ov');
  const txt=document.getElementById('ovText');
  const rect=ov.querySelector('rect');
  txt.textContent='\\u2705 תשובה נכונה!';txt.setAttribute('fill','#2ecc71');
  rect.setAttribute('fill','#0d3d2a');rect.setAttribute('stroke','#2ecc71');
  ov.setAttribute('opacity','1');
  setTimeout(()=>{
    document.getElementById('ql').textContent='\\u2705 התשובה הנכונה:';
    document.getElementById('qt').innerHTML='<span style="color:#2ecc71;font-size:11px;font-weight:900">'+OPTS[C]+'</span>'+(E?'<br><span style="color:#aac4e8;font-size:10px;font-weight:400">'+E+'</span>':'');
    const prog2=document.getElementById('prog');
    prog2.style.transition='none';prog2.style.width='0%';
    setTimeout(()=>{prog2.style.transition='width 4000ms linear';prog2.style.width='100%';},30);
  },600);
},DELAY+50);
};
</script></body></html>`;
}

function parseQuestion(q) {
  const vesselMatch = q.q_he.match(/\(([A-P])\)/g);
  const vessels = vesselMatch ? vesselMatch.map(v => v.replace(/[()]/g, '')) : [];
  const imgMatch = q.q_he.match(/תמונה (\d+)/);
  return {
    observer: vessels[0] || null,
    target: vessels[1] || null,
    imageId: imgMatch ? parseInt(imgMatch[1]) : null
  };
}

function makeHeaderText(observer, target, shapeId) {
  const shapeNames = {
    10: 'על שרטון (3 כדורים)',
    20: 'מפרשית תחת מנוע (חרוט)',
    75: 'מוגבל שוקע (גליל)',
    76: 'שולת מוקשים',
    77: 'עוגן (כדור)',
    79: 'מוגבל בתמרון (כדור-יהלום-כדור)',
    80: 'ללא שליטה (2 כדורים)',
    83: 'מצוקה (דגל+כדור)',
    84: 'דייג (2 חרוטים)',
    86: 'גורר >200מ (יהלום)',
    87: 'מוגבל עיסוק + צד בטוח',
    89: 'מוגבל עיסוק + צד פנוי',
    90: 'מוגבל עיסוק + שני צדדים',
    93: 'דגל A (צולל)',
    92: 'דגל N',
    95: 'דגל B (חומ"ס)',
    98: 'דגל A (ספינת אם)',
    104: 'דגל O (חיפוש)',
  };
  const shapeName = shapeNames[shapeId] || `תמונה ${shapeId}`;
  if (observer && target) {
    return `${observer} מבחין ב-${target} המציג סימן יום`;
  }
  return `סימן יום: ${shapeName}`;
}

// Main — output to html/ with filename matching publisher's fetchPrebuiltHTML format
const outDir = path.join(__dirname, '..', 'html');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const compassQuestions = questions
  .filter(q => q.license === 11 && q.q_he.includes('תמונה'))
  .map(q => {
    const parsed = parseQuestion(q);
    return { ...q, ...parsed };
  })
  .filter(q => q.observer && q.target && q.imageId);

const l11Dir = path.join(outDir, 'license11');
if (!fs.existsSync(l11Dir)) fs.mkdirSync(l11Dir, { recursive: true });

let generated = 0;
for (const q of compassQuestions) {
  const headerText = makeHeaderText(q.observer, q.target, q.imageId);
  const scene = buildScene(q.observer, q.target, q.imageId, headerText);
  const html = buildHtml(q, scene);
  // Match publisher's naming: quiz_NUM_TOPIC_he.html
  const topic = (q.topic || 'quiz').replace(/[\s\/]/g, '_');
  const filename = `quiz_${String(q.num).padStart(3, '0')}_${topic}_he.html`;
  fs.writeFileSync(path.join(outDir, filename), html, 'utf8');
  // Also save to license11 directory
  const l11Filename = `quiz_${String(q.num).padStart(4, '0')}_L11_he.html`;
  fs.writeFileSync(path.join(l11Dir, l11Filename), html, 'utf8');
  generated++;
  console.log(`Generated: ${filename} (obs:${q.observer} tgt:${q.target} img:${q.imageId})`);
}

// Save standalone compass rose SVG for reuse
const roseSvg = `<svg width="360" height="420" viewBox="0 0 360 420" xmlns="http://www.w3.org/2000/svg">\n${buildCompassRoseSvg()}\n</svg>`;
fs.writeFileSync(path.join(outDir, 'compass-rose.svg'), roseSvg, 'utf8');
fs.writeFileSync(path.join(l11Dir, 'compass-rose.svg'), roseSvg, 'utf8');
console.log(`\nSaved: compass-rose.svg (standalone reusable compass rose)`);
console.log(`Total: ${generated} quiz reels generated in html/ and html/license11/`);
