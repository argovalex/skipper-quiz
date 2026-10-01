#!/usr/bin/env node
// יוצר את שיבוט הקול של אלכס ב-ElevenLabs (Instant Voice Clone) ושומר ELEVENLABS_VOICE_ID ב-.env.
// אותה הקלטה ששובטה ב-Higgsfield (Alex Skipper v2), כך שהעורך מנגן קול זהה בזמן אמת.
//   node tools/voice/elevenlabs-clone.js <Alex_voice.m4a>
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const ENV = path.join(ROOT, '.env');

function envVal(name) {
  const m = fs.readFileSync(ENV, 'utf8').match(new RegExp(`^\\s*${name}\\s*=\\s*(.+?)\\s*$`, 'm'));
  return m && m[1].replace(/^["']|["']$/g, '');
}

(async () => {
  const src = process.argv[2];
  if (!src || !fs.existsSync(src)) { console.error('usage: elevenlabs-clone.js <voice-sample.m4a>'); process.exit(1); }
  const key = envVal('ELEVENLABS_API_KEY');
  if (!key) { console.error('ELEVENLABS_API_KEY missing in .env'); process.exit(1); }
  if (envVal('ELEVENLABS_VOICE_ID')) { console.log('ELEVENLABS_VOICE_ID already set, nothing to do'); return; }

  const form = new FormData();
  form.append('name', 'Alex Skipper v2');
  form.append('description', 'SkipperQuiz narrator, cloned from Alex_voice.m4a (phone, clean)');
  form.append('remove_background_noise', 'false');
  form.append('files', new Blob([fs.readFileSync(src)], { type: 'audio/mp4' }), path.basename(src));

  const r = await fetch('https://api.elevenlabs.io/v1/voices/add', { method: 'POST', headers: { 'xi-api-key': key }, body: form });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || !j.voice_id) { console.error('clone failed', r.status, JSON.stringify(j).slice(0, 300)); process.exit(1); }
  fs.appendFileSync(ENV, `\nELEVENLABS_VOICE_ID=${j.voice_id}\n`);
  console.log('voice_id saved to .env:', j.voice_id);
})();
