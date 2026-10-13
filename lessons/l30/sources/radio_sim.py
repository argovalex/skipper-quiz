"""Simulated VHF exchanges for lesson cards about radio calls (Alex 2026-10-13).
Each line is TTS'd (ElevenLabs: 'me' = Alex's clone, 'coast' = a second voice), passed through a VHF filter
(band-limited, compressed, light hiss) with a squelch burst at the end of every transmission, and joined into
<aud_dir>/sim_<sid>.mp3. assemble.py plays it right after the section's narration, over <sid>_sim.png.
usage: python radio_sim.py <lesson-number> <aud_dir>      (SIMS dict is read from u<NN>_cards.py)"""
import os, sys, json, hashlib, subprocess, importlib.util, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import el_tts
VOICES = {'me': el_tts.VOICE, 'coast': el_tts.env.get('ELEVENLABS_COAST_VOICE_ID', 'onwK4e9ZLuTAKqWW03F9')}
VHF = 'highpass=f=320,lowpass=f=3000,acompressor=threshold=-24dB:ratio=6:attack=5:release=80,volume=1.4,aformat=sample_rates=44100:channel_layouts=mono'

def run(a):
    subprocess.run(a, check=True, capture_output=True)

def tts(voice, text, out):
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128',
                                 data=json.dumps({'text': text, 'model_id': el_tts.MODEL}).encode('utf-8'),
                                 headers={'xi-api-key': el_tts.KEY, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=300) as r: open(out, 'wb').write(r.read())

def line(wrk, who, text):
    h = hashlib.sha1(f'{who}|{el_tts.MODEL}|{text}'.encode('utf-8')).hexdigest()[:12]
    raw, fx = os.path.join(wrk, f'{h}_raw.mp3'), os.path.join(wrk, f'{h}_fx.wav')
    if not os.path.isfile(raw): tts(VOICES[who], text, raw)
    if not os.path.isfile(fx):   # VHF voice + hiss bed, then a 0.25 s squelch burst when the PTT is released
        run(['ffmpeg', '-y', '-i', raw, '-f', 'lavfi', '-i', 'anoisesrc=color=pink:amplitude=0.02:sample_rate=44100',
             '-f', 'lavfi', '-i', 'anoisesrc=color=white:amplitude=0.18:sample_rate=44100:duration=0.25',
             '-filter_complex', f'[0:a]{VHF}[v];[1:a]{VHF}[h];[v][h]amix=inputs=2:duration=first:normalize=0[vh];[2:a]{VHF}[sq];[vh][sq]concat=n=2:v=0:a=1[o]',
             '-map', '[o]', fx])
    return fx

def build(sid, script, aud):
    wrk = os.path.join(aud, 'sim'); os.makedirs(wrk, exist_ok=True)
    parts = [line(wrk, who, text) for who, text in script]
    inp = sum((['-i', p] for p in parts), [])
    gap = ''.join(f'[{i}:a]apad=pad_dur=0.6[p{i}];' for i in range(len(parts)))
    fc = gap + ''.join(f'[p{i}]' for i in range(len(parts))) + f'concat=n={len(parts)}:v=0:a=1,loudnorm=I=-16:TP=-1.5[o]'
    out = os.path.join(aud, f'sim_{sid}.mp3')
    run(['ffmpeg', '-y', *inp, '-filter_complex', fc, '-map', '[o]', '-ar', '44100', '-ac', '2', '-c:a', 'libmp3lame', '-b:a', '160k', out])
    return out

if __name__ == '__main__':
    n, aud = int(sys.argv[1]), sys.argv[2]
    spec = importlib.util.spec_from_file_location('u', os.path.join(HERE, f'u{n:02d}_cards.py')); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for sid, script in m.SIMS.items():
        print('sim', sid, build(sid, script, aud), flush=True)
