// GMDSS simulator server (lessons/l40/simulator): serves the page and answers free-form transmissions.
// POST /api/reply {text, state} -> {station, text, audio:<mp3 base64>}
//   Haiku writes the shore/rescue station reply, ElevenLabs voices it (same coast voices as l30 radio_sim.py),
//   ffmpeg applies the same VHF chain + squelch burst. Run: node tools/gmdss-sim-server.js  (port 8911)
const http = require('http'), fs = require('fs'), path = require('path'), { spawn } = require('child_process');
const ROOT = path.join(__dirname, '..'), DIR = path.join(ROOT, 'lessons', 'l40', 'simulator'), PORT = +process.env.PORT || 8911;
const env = {};
for (const ln of fs.readFileSync(path.join(ROOT, '.env'), 'utf8').split(/\r?\n/)) { const m = ln.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$/); if (m) env[m[1]] = m[2].replace(/^["']|["']$/g, ''); }
const VOICES = { haifa: env.ELEVENLABS_COAST_VOICE_ID || 'onwK4e9ZLuTAKqWW03F9', rcc: env.ELEVENLABS_COAST_VOICE_ID || 'onwK4e9ZLuTAKqWW03F9', rescue: 'pNInz6obpgDQGcFmaJgB' };
const NAMES = { haifa: 'Haifa Radio', rcc: 'RCC Haifa', rescue: 'Rescue vessel' };
const VHF = 'highpass=f=320,lowpass=f=3000,acompressor=threshold=-24dB:ratio=6:attack=5:release=80,volume=1.4,aformat=sample_rates=44100:channel_layouts=mono';
const MIME = { '.html': 'text/html; charset=utf-8', '.mp3': 'audio/mpeg', '.js': 'text/javascript', '.json': 'application/json' };

function system(st) {
  return `You are the shore/rescue side of a GMDSS training simulator. A student on ${(st && st.scenario && st.scenario.cls) || 'sailing yacht'} ${(st && st.scenario && st.scenario.vessel) || 'SONDRA'} (MMSI ${(st && st.scenario && st.scenario.mmsi) || '428123456'}, ${(st && st.scenario && st.scenario.pob) || 4} persons on board, position ${(st && st.position) || '32 45N 034 52E'}, ${(st && st.scenario && st.scenario.what) || 'fire in the engine room'}) transmits on VHF channel 16. Reply as a real Israeli coast radio operator would, in correct GMDSS radio procedure, in English only, 1 to 3 short sentences, ending with "Over" (or "Out" if the exchange is finished).
Scenario state: ${JSON.stringify(st || {})}.
Rules:
- Pick who answers: "haifa" (Haifa Radio, the default), "rcc" (RCC Haifa, coordinates SAR and EPIRB alerts), or "rescue" (the rescue vessel, only if the student calls it or is talking about radar/SART/pickup). If the student addresses a station by name, that station answers.
- Answer what the student actually said or asked (position, status, number of people, what to do next, whether the SART/EPIRB is seen). Use only facts from the state; if a fact is unknown, tell them to say again or report it.
- If the transmission breaks procedure (no station name, no Over, wrong channel logic), still answer the content, and add a short correction in procedure language such as "Say again, station name unclear".
- Numbers in digits are fine, say "niner" for 9 only in MMSI.
- Never invent rescue times shorter than the state gives. Do not break character. No markdown.
Return ONLY JSON: {"station":"haifa|rcc|rescue","text":"..."}`;
}

async function haiku(text, st) {
  const r = await fetch('https://api.anthropic.com/v1/messages', { method: 'POST',
    headers: { 'x-api-key': env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
    body: JSON.stringify({ model: 'claude-haiku-4-5-20251001', max_tokens: 250, system: system(st), messages: [{ role: 'user', content: `Student transmission: "${String(text).slice(0, 600)}"` }] }) });
  const j = await r.json(); if (!r.ok) throw new Error(JSON.stringify(j).slice(0, 200));
  const raw = j.content[0].text; return JSON.parse(raw.slice(raw.indexOf('{'), raw.lastIndexOf('}') + 1));
}
async function tts(voice, text) {
  const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice}?output_format=mp3_44100_128`, { method: 'POST',
    headers: { 'xi-api-key': env.ELEVENLABS_API_KEY, 'content-type': 'application/json' }, body: JSON.stringify({ text, model_id: env.ELEVENLABS_MODEL || 'eleven_v4' }) });
  if (!r.ok) throw new Error('tts ' + r.status); return Buffer.from(await r.arrayBuffer());
}
function vhf(mp3) {
  return new Promise((res, rej) => {
    const p = spawn('ffmpeg', ['-y', '-i', 'pipe:0', '-f', 'lavfi', '-i', 'anoisesrc=color=pink:amplitude=0.02:sample_rate=44100', '-f', 'lavfi', '-i', 'anoisesrc=color=white:amplitude=0.18:sample_rate=44100:duration=0.25',
      '-filter_complex', `[0:a]${VHF}[v];[1:a]${VHF}[h];[v][h]amix=inputs=2:duration=first:normalize=0[vh];[2:a]${VHF}[sq];[vh][sq]concat=n=2:v=0:a=1,loudnorm=I=-16:TP=-1.5[o]`,
      '-map', '[o]', '-ac', '1', '-c:a', 'libmp3lame', '-b:a', '96k', '-f', 'mp3', 'pipe:1'], { windowsHide: true });
    const out = []; p.stdout.on('data', d => out.push(d)); p.on('error', rej); p.on('close', c => c === 0 ? res(Buffer.concat(out)) : rej(new Error('ffmpeg ' + c)));
    p.stdin.on('error', () => {}); p.stdin.end(mp3);
  });
}

http.createServer(async (req, res) => {
  try {
    if (req.method === 'POST' && req.url === '/api/reply') {
      let b = ''; for await (const c of req) b += c; const { text, state } = JSON.parse(b || '{}');
      const a = await haiku(text, state); const st = VOICES[a.station] ? a.station : 'haifa';
      const audio = (await vhf(await tts(VOICES[st], a.text))).toString('base64');
      res.writeHead(200, { 'content-type': 'application/json' }); return res.end(JSON.stringify({ station: NAMES[st], text: a.text, audio }));
    }
    if (req.url === '/api/ping') { res.writeHead(200); return res.end('ok'); }
    let p = decodeURIComponent(req.url.split('?')[0]); if (p === '/') p = '/index.html';
    const f = path.join(DIR, path.normalize(p)); if (!f.startsWith(DIR) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { 'content-type': MIME[path.extname(f)] || 'application/octet-stream', 'cache-control': 'no-cache' }); fs.createReadStream(f).pipe(res);
  } catch (e) { console.error(e.message); res.writeHead(500, { 'content-type': 'application/json' }); res.end(JSON.stringify({ error: e.message })); }
}).listen(PORT, () => console.log('GMDSS sim on http://localhost:' + PORT));
