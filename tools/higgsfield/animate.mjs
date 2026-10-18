// Animate l12 stills via the Higgsfield API (Seedance 2.0 image-to-video, 720p, 8s, no audio).
//   node --env-file=.env.local tools/higgsfield/animate.mjs <out-dir> <num>=<image-url>|<prompt> ...
// Billable (~$2.4 per clip). Saves <out-dir>/<num>.mp4.
import { config, higgsfield } from '@higgsfield/client/v2';
import fs from 'fs';
import path from 'path';
config({ credentials: process.env.HF_CREDENTIALS });
const [out, ...items] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
await Promise.all(items.map(async it => {
  const [num, rest] = [it.slice(0, it.indexOf('=')), it.slice(it.indexOf('=') + 1)];
  const [image_url, prompt] = rest.split('|');
  try {
    const r = await higgsfield.subscribe('bytedance/seedance-2.0/image-to-video', {
      input: { image_url, prompt, duration: 8, resolution: '720p', aspect_ratio: '16:9', generate_audio: false },
      withPolling: true,
    });
    if (r.status !== 'completed' || !r.video?.url) { console.log(num, 'NOT COMPLETED', r.status); return; }
    const buf = Buffer.from(await (await fetch(r.video.url)).arrayBuffer());
    fs.writeFileSync(path.join(out, num + '.mp4'), buf);
    console.log(num, 'ok', buf.length);
  } catch (e) { console.log(num, 'FAILED', String(e?.message || e).slice(0, 300)); }
}));
