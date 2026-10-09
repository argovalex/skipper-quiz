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

# Answer letters (Alex 2026-10-05): raw \u05D3 read as "delet", \u05D1 as "bayit". TTS-only; display text keeps the bare letter.
LETTER_NAME = {'\u05D0': '\u05D0\u05B8\u05DC\u05B6\u05E3', '\u05D1': '\u05D1\u05B5\u05BC\u05D9\u05EA', '\u05D2': '\u05D2\u05B4\u05BC\u05D9\u05DE\u05B6\u05DC', '\u05D3': '\u05D3\u05B8\u05BC\u05DC\u05B6\u05EA'}
# Alex 2026-10-09: every answer letter must sound like the alphabet name, including "\u05D5\u05D3'?" and "\u05D1 \u05D5-\u05D2".
#   "\u05D1'?" -> "\u05D1\u05B5\u05BC\u05D9\u05EA."   (a lone letter-question is read flat, like reciting the alphabet)
#   "\u05D5\u05D3'?" -> "\u05D3\u05B8\u05BC\u05DC\u05B6\u05EA."  (the \u05D5 prefix is dropped: "\u05D5\u05D1\u05B5\u05BC\u05D9\u05EA" came out unintelligible)
#   "\u05D5\u05D2'," / "\u05D1 \u05D5-\u05D2" -> "\u05D5\u05D2\u05DD \u05D2\u05B4\u05BC\u05D9\u05DE\u05B6\u05DC"  (mid-sentence "and C" keeps its meaning)
LETTER_RE = re.compile(r"(?<![\u05D0-\u05EA\u0591-\u05C7])(\u05D5?)([\u05D0\u05D1\u05D2\u05D3])([:'\u05F3])(\??)(?![\u05D0-\u05EA])")
PAIR_RE = re.compile(r"(?<![\u05D0-\u05EA\u0591-\u05C7])([\u05D0\u05D1\u05D2\u05D3])['\u05F3]? \u05D5-?([\u05D0\u05D1\u05D2\u05D3])['\u05F3]?(?![\u05D0-\u05EA])")

def letter_sub(m):
    pre, ch, mark, q = m.groups(); name = LETTER_NAME[ch]
    if q: return name + '.'                                   # "\u05D1'?" / "\u05D5\u05D3'?": standalone, flat
    if mark == ':': return name + ':'
    return ('\u05D5\u05D2\u05DD ' if pre else '') + name
# 3s pause after "\u05D4\u05EA\u05E9\u05D5\u05D1\u05D4 \u05D4\u05E0\u05DB\u05D5\u05E0\u05D4 \u05D4\u05D9\u05D0" (Alex 2026-10-05): split there, TTS each piece, join with silence.
ANSWER_SPLIT = re.compile(r'(?<=\u05D4\u05EA\u05E9\u05D5\u05D1\u05D4 \u05D4\u05E0\u05DB\u05D5\u05E0\u05D4 \u05D4\u05D9\u05D0)\s*')
PAUSE = 3.0

def pieces(t, lex):
    pair = lambda m: LETTER_NAME[m.group(1)] + ' וגם ' + LETTER_NAME[m.group(2)]
    return [niqqud_apply(LETTER_RE.sub(letter_sub, PAIR_RE.sub(pair, p)), lex)
            for p in ANSWER_SPLIT.split(t) if p.strip()]

def main(vo, aud):
    raw = os.path.join(aud, 'raw'); os.makedirs(raw, exist_ok=True)
    lex = load_lexicon()
    jobs = [(sid, pieces(t, lex)) for sid, t in sections(vo)]
    def one(job):
        sid, parts = job
        text = f' [[{PAUSE:g}s]] '.join(parts)
        seg, key = os.path.join(aud, f'seg_{sid}.mp3'), os.path.join(raw, sid + '.txt')
        if os.path.exists(seg) and os.path.exists(key) and open(key, encoding='utf-8').read() == MODEL + '|' + text:
            return sid, dur(seg), 'cached'
        rps = [os.path.join(raw, f'{sid}_{i}.mp3') for i in range(len(parts))]
        for part, rp in zip(parts, rps):
            for attempt in range(3):
                try: tts(part, rp); break
                except Exception as e:
                    if attempt == 2: raise RuntimeError(f'{sid}: {e}')
        args, labels = [], []
        for i, rp in enumerate(rps):
            if i: args += ['-f', 'lavfi', '-t', str(PAUSE), '-i', 'anullsrc=r=44100:cl=mono']
            args += ['-i', rp]
        n = args.count('-i')
        fc = ''.join(f'[{i}:a]aformat=sample_rates=44100:channel_layouts=mono[a{i}];' for i in range(n))
        fc += ''.join(f'[a{i}]' for i in range(n)) + f'concat=n={n}:v=0:a=1,{CHAIN}[out]'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *args, '-filter_complex', fc, '-map', '[out]', '-b:a', '192k', seg], check=True)
        d = dur(seg); cps = len(re.sub(r'[\u0591-\u05C7\s]|\[\[[^\]]*\]\]', '', text)) / max(d - PAUSE * (len(parts) - 1), 0.1)
        if not 5 <= cps <= 22: raise RuntimeError(f'{sid}: suspicious length {d:.1f}s ({cps:.1f} chars/s)')
        open(key, 'w', encoding='utf-8').write(MODEL + '|' + text)
        return sid, d, f'{cps:.1f} cps'
    with ThreadPoolExecutor(3) as ex:
        for sid, d, note in ex.map(one, jobs): print(f'{sid} {d:.1f}s {note}', flush=True)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
