// node video-durations.js
// Fills content/video-durations.json ({ "<videoUrl>": seconds }) with ffprobe, for the VideoObject
// `duration` that build-site.js writes. Keyed by URL, so a re-rendered video is probed again.
// Only new URLs are probed. Needs ffprobe on PATH (comes with FFmpeg).
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = __dirname;
const OUT = path.join(ROOT, 'content', 'video-durations.json');
const questions = JSON.parse(fs.readFileSync(path.join(ROOT, '..', '..', 'data', 'l11.json'), 'utf8'));
const pool = new Set(JSON.parse(fs.readFileSync(path.join(ROOT, '..', '..', 'tools', 'daily-publish-pool.json'), 'utf8')).map(p => p.num));
const posts = JSON.parse(fs.readFileSync(path.join(ROOT, 'content', 'posts.json'), 'utf8'));

const urls = [
  ...questions.filter(q => q.videoUrl && pool.has(q.num)).map(q => q.videoUrl),
  ...posts.map(p => p.video).filter(u => /^https?:/.test(u || '')),
];
const known = fs.existsSync(OUT) ? JSON.parse(fs.readFileSync(OUT, 'utf8')) : {};
const out = {};
let probed = 0, failed = 0;
for (const u of [...new Set(urls)]) {
  if (known[u]) { out[u] = known[u]; continue; }
  try {
    const s = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', u], { encoding: 'utf8', timeout: 30000 });
    const sec = Math.round(parseFloat(s));
    if (sec > 0) { out[u] = sec; probed++; }
  } catch (e) { failed++; console.warn('ffprobe failed:', u); }
}
fs.writeFileSync(OUT, JSON.stringify(out, null, 1) + '\n');
console.log(`video-durations: ${Object.keys(out).length} known, ${probed} probed now, ${failed} failed`);
