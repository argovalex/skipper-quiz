"""Burned-in Hebrew subtitles for a branded lesson video.
usage: python subs.py <vo.txt> <aud_dir> <branded.mp4> <out.mp4> [--intro 3.0]
Timing: per-section offsets from assemble.py clips (<aud>/wrk/NN_<sid>.mp4); inside a section, sentence
boundaries are estimated by character share and snapped to detected pauses in the trimmed narration.
Display text: TTS-only spellings mapped back (אָלֶף -> א, גברַאלְטָר -> גיברלטר), lexicon niqqud applied.
"""
import os, re, sys, subprocess, shutil
sys.path.insert(0, r'C:/Users/argov/OneDrive/Co-Work OS/SkipperQuiz/tools/lesson')
from niqqud import load_lexicon, apply as niqqud_apply
from PIL import ImageFont

VO, AUD, SRC, OUT = sys.argv[1:5]
INTRO = 3.0
HERE = os.environ.get('SUBS_WORK') or os.path.join(__import__('tempfile').gettempdir(), 'lesson_subs'); os.makedirs(HERE, exist_ok=True)
DISPLAY = [('אָלֶף', 'א'), ('גברַאלְטָר', 'גיברלטר'), ('הרָאם לַיְין', 'ה-Rhumb line'), ('רָאם לַיְין', 'Rhumb line'), ('U T C', 'UTC'), ('G M T', 'GMT'), ('Z D', 'ZD'), ('G P S', 'GPS')]
FONT = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 40)
MAXW = 1120
NIQ = re.compile(r'[\u0591-\u05C7]')

def probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                       capture_output=True, text=True)
    return float(r.stdout.strip())

def silences(p):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', p, '-af', 'silencedetect=noise=-32dB:d=0.18', '-f', 'null', '-'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', r.stderr)]
    en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', r.stderr)]
    return [(a + b) / 2 for a, b in zip(st, en)]

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

lex = load_lexicon()
def display(t):
    for a, b in DISPLAY: t = t.replace(a, b)
    t = niqqud_apply(t, lex)
    t = re.sub(r'(?<![\u0590-\u05FF])אֹ(?![\u0590-\u05FF])', 'א', t)
    return t

def width(s): return FONT.getlength(s)
def plain_len(s): return len(NIQ.sub('', s))

def split_sentence(s):
    """Split into chunks that fit in <=2 lines; prefer comma/colon breaks."""
    if width(s) <= 2 * MAXW * 0.92: return [s]
    parts = re.split(r'(?<=[,:])\s+', s)
    chunks, cur = [], ''
    for p in parts:
        cand = (cur + ' ' + p).strip()
        if width(cand) <= 2 * MAXW * 0.92: cur = cand
        else:
            if cur: chunks.append(cur)
            cur = p
    if cur: chunks.append(cur)
    final = []
    for c in chunks:  # still too long: split by words in half
        while width(c) > 2 * MAXW * 0.92:
            w = c.split(); h = len(w) // 2
            final.append(' '.join(w[:h])); c = ' '.join(w[h:])
        final.append(c)
    return final

def two_lines(s):
    if width(s) <= MAXW: return [s]
    w = s.split(); best = None
    for i in range(1, len(w)):
        a, b = ' '.join(w[:i]), ' '.join(w[i:])
        if width(a) <= MAXW and width(b) <= MAXW:
            sc = abs(width(a) - width(b))
            if best is None or sc < best[0]: best = (sc, [a, b])
    assert best, 'line too long: ' + s
    return best[1]

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h}:{m:02d}:{s:05.2f}'

events = []
secs = sections(VO)
off = INTRO
for idx, (sid, text) in enumerate(secs, 1):
    clip = os.path.join(AUD, 'wrk', f'{idx:02d}_{sid}.mp4')
    trimmed = os.path.join(AUD, 'wrk', f'{sid}_t.mp3')
    cdur, adur = probe(clip), probe(trimmed)
    pauses = silences(trimmed)
    disp = display(text)
    sents = [x for x in re.split(r'(?<=[.?!])\s+', disp) if x]
    total = sum(plain_len(x) for x in sents)
    bounds, acc = [0.0], 0
    for sct in sents[:-1]:
        acc += plain_len(sct); est = adur * acc / total
        near = [p for p in pauses if abs(p - est) < 1.5 and p > bounds[-1] + 0.4]
        bounds.append(min(near, key=lambda p: abs(p - est)) if near else est)
    bounds.append(adur)
    for i, sct in enumerate(sents):
        a, b = bounds[i], bounds[i + 1]
        chunks = split_sentence(sct); ctot = sum(plain_len(c) for c in chunks); t0 = a
        for c in chunks:
            t1 = t0 + (b - a) * plain_len(c) / ctot
            events.append((off + t0, off + t1, c)); t0 = t1
    off += cdur

# extend each event to the next start (no flicker), cap tail
ev2 = []
for i, (a, b, c) in enumerate(events):
    nxt = events[i + 1][0] if i + 1 < len(events) else b + 0.6
    ev2.append((a, nxt - 0.02 if nxt - b <= 1.2 else b + 0.3, c))

RLM = '\u200f'
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,40,&H00FFFFFF,&H00FFFFFF,&H50101820,&H50101820,-1,0,0,0,100,100,0,0,3,9,0,2,60,60,22,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lines = [hdr]
srt = []
for n, (a, b, c) in enumerate(ev2, 1):
    ls = two_lines(c)
    lines.append(f'Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,' + r'\N'.join('‫' + l + '‬' for l in ls) + '\n')
    f = lambda t: f'{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d},{int(round((t%1)*1000)) % 1000:03d}'
    srt.append(f'{n}\n{f(a)} --> {f(b)}\n' + '\n'.join(RLM + l for l in ls) + '\n')
open(os.path.join(HERE, 'subs.ass'), 'w', encoding='utf-8-sig').write(''.join(lines))
open(os.path.splitext(OUT)[0] + '.srt', 'w', encoding='utf-8-sig').write('\n'.join(srt))
os.makedirs(os.path.join(HERE, 'fonts'), exist_ok=True)
for fn in ('arial.ttf', 'arialbd.ttf'):
    shutil.copy('C:/Windows/Fonts/' + fn, os.path.join(HERE, 'fonts', fn))
print('events', len(ev2), 'last end', round(ev2[-1][1], 1))
r = subprocess.run(['ffmpeg', '-y', '-i', os.path.abspath(SRC), '-vf', 'ass=subs.ass:fontsdir=fonts',
                    '-c:v', 'libx264', '-crf', '21', '-preset', 'medium', '-pix_fmt', 'yuv420p',
                    '-c:a', 'copy', '-movflags', '+faststart', os.path.abspath(OUT)],
                   cwd=HERE, capture_output=True, text=True, encoding='utf-8', errors='replace')
if r.returncode: print(r.stderr[-1500:]); sys.exit(1)
print('OUT', OUT, round(probe(OUT), 1))
