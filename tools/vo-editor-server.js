#!/usr/bin/env node
// שרת מקומי ל-vo-editor: מגיש את קבצי הפרויקט (סטטי) ומאפשר הוספה חיה למילון הניקוד.
// מחליף את http-server על :8899 כדי שכפתור "הוסף למילון" בעורך יוכל לכתוב לקובץ.
//   POST /api/lexicon  { nikud: "בַּיַּבָּשָׁה", plain?: "ביבשה" }
//     -> מוסיף/מעדכן שורה ב-references/niqqud-lexicon.md, מחזיר { status, plain, nikud }
'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const LEXICON = path.join(ROOT, 'references', 'niqqud-lexicon.md');
const PORT = Number(process.env.PORT) || 8899;
const SECTION = '## מילים';
const NEXT_SECTION = '## מקרים מיוחדים';

const MIME = {
  '.html': 'text/html; charset=utf-8', '.md': 'text/markdown; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml', '.mp3': 'audio/mpeg', '.mp4': 'video/mp4',
};

const stripNiqqud = s => s.replace(/[֑-ׇ]/g, '').trim();

// ── עדכון המילון ────────────────────────────────────────────────────────────────
function addToLexicon(nikudRaw, plainOverride) {
  const nikud = String(nikudRaw || '').trim();
  if (!nikud) return { status: 'error', message: 'לא התקבלה מילה' };
  if (!/[֑-ׇ]/.test(nikud)) return { status: 'error', message: 'המילה אינה מנוקדת' };
  const plain = (plainOverride && plainOverride.trim()) || stripNiqqud(nikud);
  if (!plain) return { status: 'error', message: 'לא נגזרה צורה רגילה' };

  const md = fs.readFileSync(LEXICON, 'utf8');
  const eol = md.includes('\r\n') ? '\r\n' : '\n';
  const lines = md.split(/\r?\n/);

  const secIdx = lines.findIndex(l => l.trim() === SECTION);
  if (secIdx === -1) return { status: 'error', message: `לא נמצאה הסקציה ${SECTION}` };
  let endIdx = lines.findIndex((l, i) => i > secIdx && l.trim() === NEXT_SECTION);
  if (endIdx === -1) endIdx = lines.length;

  const rowIdx = [];
  for (let i = secIdx + 1; i < endIdx; i++) if (lines[i].trimStart().startsWith('|')) rowIdx.push(i);
  if (!rowIdx.length) return { status: 'error', message: 'לא נמצאה טבלה בסקציית המילים' };

  // מיפוי צורה-רגילה -> אינדקס שורה (מדלג על כותרת/מפריד)
  const existing = new Map();
  for (const i of rowIdx) {
    const cells = lines[i].trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim());
    if (cells.length < 2) continue;
    const p = cells[0];
    if (p === 'רגיל' || p === '' || /^[-: ]+$/.test(p)) continue;
    existing.set(stripNiqqud(p.split('(')[0].trim()), i);
  }

  const key = stripNiqqud(plain.split('(')[0].trim());
  const row = `| ${plain} | ${nikud} |`;
  let status;
  if (existing.has(key)) {
    const i = existing.get(key);
    if (lines[i].trim() === row) { status = 'exists'; }
    else { lines[i] = row; status = 'updated'; }
  } else {
    lines.splice(rowIdx[rowIdx.length - 1] + 1, 0, row);
    status = 'added';
  }

  if (status !== 'exists') fs.writeFileSync(LEXICON, lines.join(eol), 'utf8');
  return { status, plain, nikud };
}

// ── הגשת קבצים סטטיים ────────────────────────────────────────────────────────────
function serveStatic(req, res) {
  let rel = decodeURIComponent(req.url.split('?')[0]);
  if (rel === '/' ) rel = '/vo-editor.html';
  const full = path.join(ROOT, path.normalize(rel));
  if (!full.startsWith(ROOT)) { res.writeHead(403); return res.end('forbidden'); }
  fs.readFile(full, (err, buf) => {
    if (err) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(full).toLowerCase()] || 'application/octet-stream',
      'Cache-Control': 'no-cache' });
    res.end(buf);
  });
}

const server = http.createServer((req, res) => {
  if (req.method === 'POST' && req.url === '/api/lexicon') {
    let body = '';
    req.on('data', c => { body += c; if (body.length > 1e5) req.destroy(); });
    req.on('end', () => {
      let out;
      try { const j = JSON.parse(body || '{}'); out = addToLexicon(j.nikud, j.plain); }
      catch (e) { out = { status: 'error', message: e.message }; }
      res.writeHead(out.status === 'error' ? 400 : 200, { 'Content-Type': 'application/json; charset=utf-8' });
      res.end(JSON.stringify(out));
    });
    return;
  }
  if (req.method === 'GET' || req.method === 'HEAD') return serveStatic(req, res);
  res.writeHead(405); res.end('method not allowed');
});

server.listen(PORT, () => {
  console.log(`vo-editor server on http://localhost:${PORT}/vo-editor.html  (POST /api/lexicon writes the lexicon)`);
});
