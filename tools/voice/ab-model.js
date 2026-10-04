// ab-model.js <num> [license] : render the question's VO with eleven_v3 and eleven_v4 for an A/B listen.
// Output: output/ab/q<num>-<model>.mp3 (raw API audio, no mastering). Reads ELEVENLABS_* from .env.
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..', '..');
for (const l of fs.readFileSync(path.join(root, '.env'), 'utf8').split(/\r?\n/)) {
  const m = l.match(/^\s*(ELEVENLABS_\w+)\s*=\s*(.*)\s*$/);
  if (m) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
}
const { buildVoiceover } = require('../quiz-app/vo.js');
const num = String(process.argv[2]);
const lic = process.argv[3] || '11';
const bank = JSON.parse(fs.readFileSync(path.join(root, 'data', `l${lic}.json`), 'utf8'));
const qs = Array.isArray(bank) ? bank : bank.questions;
const q = qs.find(x => String(x.num) === num);
if (!q) throw new Error('no question ' + num);
const text = buildVoiceover(q).replace(/\[\[PAUSE\]\]/g, ' ');
const outDir = path.join(root, 'output', 'ab');
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, `q${num}-vo.txt`), text);
(async () => {
  for (const model of ['eleven_v3', 'eleven_v4']) {
    const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${process.env.ELEVENLABS_VOICE_ID}?output_format=mp3_44100_128`, {
      method: 'POST',
      headers: { 'xi-api-key': process.env.ELEVENLABS_API_KEY, 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, model_id: model }),
    });
    if (!r.ok) { console.log(model, 'FAIL', r.status, (await r.text()).slice(0, 300)); continue; }
    const f = path.join(outDir, `q${num}-${model}.mp3`);
    fs.writeFileSync(f, Buffer.from(await r.arrayBuffer()));
    console.log(model, 'OK', f);
  }
})();
