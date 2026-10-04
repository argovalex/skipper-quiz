"""Lesson narration in Alex's voice: ElevenLabs clone (eleven_v4), lexicon applied, mastered (tools/voice/master.py chain).
usage: python el_tts.py <vo.txt> <aud_dir>      -> <aud_dir>/seg_<sid>.mp3 for every '## sid' section
Skips sections whose seg file already exists for the same text (cache key in <aud_dir>/raw/<sid>.txt)."""
import os, re, sys, json, subprocess, urllib.request
from concurrent.futures import ThreadPoolExecutor
ROOT = r'C:/Users/argov/OneDrive/Co-Work OS/SkipperQuiz'
sys.path.insert(0, ROOT + '/tools/lesson')
from niqqud import load_lexicon, apply as niqqud_apply

env = {}
for ln in open(ROOT + '/.env', encoding='utf-8'):
    m = re.match(r'\s*(ELEVENLABS_[A-Z0-9_]+)\s*=\s*(.*?)\s*$', ln)
    if m: env[m.group(1)] = m.group(2).strip('"\'')
KEY, VOICE = env['ELEVENLABS_API_KEY'], env['ELEVENLABS_VOICE_ID']
MODEL = env.get('ELEVENLABS_MODEL', 'eleven_v4')
CHAIN = 'highpass=f=70,acompressor=threshold=-20dB:ratio=2:attack=10:release=150,loudnorm=I=-14:TP=-1:LRA=9'

def sections(vo):
    out, sid, buf = [], None, []
    for ln in open(vo, encoding='utf-8').read().splitlines():
        m = re.match(r'^##\s*(\S+)', ln)
        if m:
            if sid: out.append((sid, ' '.join(buf).strip()))
            sid, buf = m.group(1), []
        elif ln.strip(): buf.append(ln.strip())
    if sid: out.append((sid, ' '.join(buf).strip()))
    return out

def dur(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)

def tts(text, out):
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128',
                                 data=json.dumps({'text': text, 'model_id': MODEL}).encode('utf-8'),
                                 headers={'xi-api-key': KEY, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=300) as r: open(out, 'wb').write(r.read())

def main(vo, aud):
    raw = os.path.join(aud, 'raw'); os.makedirs(raw, exist_ok=True)
    lex = load_lexicon()
    jobs = []
    for sid, t in sections(vo):
        n = niqqud_apply(t, lex)
        n = re.sub(r"(?<![\u0590-\u05FF])אֹ(?=')", 'א', n)   # answer letter א' (lexicon maps bare א -> אֹ)
        jobs.append((sid, n))
    def one(job):
        sid, text = job
        seg, key = os.path.join(aud, f'seg_{sid}.mp3'), os.path.join(raw, sid + '.txt')
        if os.path.exists(seg) and os.path.exists(key) and open(key, encoding='utf-8').read() == MODEL + '|' + text:
            return sid, dur(seg), 'cached'
        rp = os.path.join(raw, sid + '.mp3')
        for attempt in range(3):
            try: tts(text, rp); break
            except Exception as e:
                if attempt == 2: raise RuntimeError(f'{sid}: {e}')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', rp, '-af', CHAIN, '-b:a', '192k', seg], check=True)
        d = dur(seg); cps = len(re.sub(r'[\u0591-\u05C7\s]', '', text)) / max(d, 0.1)
        if not 5 <= cps <= 22: raise RuntimeError(f'{sid}: suspicious length {d:.1f}s ({cps:.1f} chars/s)')
        open(key, 'w', encoding='utf-8').write(MODEL + '|' + text)
        return sid, d, f'{cps:.1f} cps'
    with ThreadPoolExecutor(3) as ex:
        for sid, d, note in ex.map(one, jobs): print(f'{sid} {d:.1f}s {note}', flush=True)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
