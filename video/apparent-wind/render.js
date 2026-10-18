// Render anim.html frame-by-frame to MP4 (1280x720, 25fps, silent stereo track for tools/lesson/brand.py).
// Usage: node video/apparent-wind/render.js <out.mp4>
const puppeteer = require('puppeteer'), { spawn } = require('child_process'), path = require('path');
(async () => {
  const out = process.argv[2] || 'apparent-wind.mp4', FPS = 25;
  const b = await puppeteer.launch({ args: ['--no-sandbox', '--allow-file-access-from-files'] });
  const pg = await b.newPage(); await pg.setViewport({ width: 1280, height: 720 });
  await pg.goto('file://' + path.join(__dirname, 'anim.html'), { waitUntil: 'load' });
  await pg.evaluate(() => window.ready);
  const dur = await pg.evaluate(() => window.DURATION), n = Math.round(dur * FPS);
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'medium', '-crf', '18', '-c:a', 'aac', '-movflags', '+faststart', out], { stdio: ['pipe', 'ignore', 'inherit'], windowsHide: true });
  for (let i = 0; i < n; i++) {
    const d = await pg.evaluate(t => { renderAt(t); return document.getElementById('c').toDataURL('image/png'); }, i / FPS);
    if (!ff.stdin.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
  console.log('frames', n, '->', out);
})();
