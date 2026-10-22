"""l40 lessons 2-7 = l30 lessons 13-18 with GMDSS-course cards and a new opening; the l30 narration is reused, not re-recorded.
usage: python reuse_l30.py <l40 lesson number> <work_dir>
1. cards: the l30 card script re-run into lessons/l40/cards/<name>/ with C.SUB = 'קורס GMDSS · <name>'; new s01 title card.
2. narration: new s01 only (el_tts, Alex's voice). Every other clip keeps the l30 audio: the clip timeline is recovered from the
   l30 branded video (scene cuts, each interval matched to the old card images in VO order), and the audio is copied as one slice.
3. raw = new s01 clip + new cards on the recovered timeline + l30 audio -> brand.py -> captions (s01 from subs.py, the rest from the
   l30 srt shifted, all without niqqud) -> companion txt."""
import os, re, sys, shutil, subprocess, importlib.util
from PIL import Image, ImageChops, ImageStat
ROOT = r'C:/Users/argov/OneDrive/Co-Work OS/SkipperQuiz'
L30 = ROOT + '/lessons/l30/sources'; sys.path.insert(0, L30)
import nowin
HERE = os.path.dirname(os.path.abspath(__file__))
def load(name, path):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
I = load('intro', os.path.join(HERE, 'intro_cards.py'))
import twcard as T
sys.path.insert(0, ROOT + '/tools/lesson')
from niqqud import load_lexicon, apply as niqqud_apply

ORD = {2: 'השני', 3: 'השלישי', 4: 'הרביעי', 5: 'החמישי', 6: 'השישי', 7: 'השביעי'}
LESSONS = {
    2: dict(n=13, name='גלי רדיו ומכשיר VHF', bg='u13_vhf', focus=(0.6, 0.55), items=['מה זה גל רדיו', 'גל קרקע, רקיע וישיר', 'תחומי תדרים ואפנון', 'המכשיר והטווח'],
            s01='ברוך הבא לשיעור השני בקורס G M D S S. היום מתחילים את הקשר עצמו. נבין מה זה גל רדיו, איך הוא מגיע מאנטנה לאנטנה, ונכיר את מכשיר הקשר שעל הסירה, ה V H F. בוא נתחיל.'),
    3: dict(n=14, name='ערוצים, MMSI ו-DSC', bg='u13_vhf', focus=(0.6, 0.55), items=['SIMPLEX ו-DUPLEX', 'הערוצים החשובים', 'אותות קריאה ו-MMSI', 'DSC']),
    4: dict(n=15, name='NAVTEX', bg='u15_navtex_pro', focus=(0.5, 0.5), items=['מה זה NAVTEX', 'תדרים ואזורים', 'סוגי הודעות ועדיפות', 'הכנה לפני הפלגה']),
    5: dict(n=16, name='EPIRB, SART ו-AIS', bg='u16_epirb_bracket', focus=(0.6, 0.5), items=['משואת חירום EPIRB', 'אזורי שייט A1-A4', 'משיב מכ״מ SART', 'זיהוי אוטומטי AIS']),
    6: dict(n=17, name='נהלי קשר', bg='u17_vhf_call', focus=(0.5, 0.45), items=['סדר עדיפויות', 'מפקח על הקשר', 'ערוץ 16 וקריאה לתחנה', 'PAN PAN ו-SECURITE']),
    7: dict(n=18, name='נוהל מצוקה', bg='u18_bounty', focus=(0.5, 0.45), items=['מתי MAYDAY', 'קריאת המצוקה', 'קודי השתקה וסיום', 'ממסר, ביטול ו-IMOT']),
}
K, W = int(sys.argv[1]), sys.argv[2]
L = LESSONS[K]; NAME = L['name']
SRC_D = ROOT + '/lessons/l30/cards/' + NAME; D = ROOT + '/lessons/l40/cards/' + NAME
os.makedirs(D, exist_ok=True); os.makedirs(W, exist_ok=True)
py = sys.executable
run = lambda *a: subprocess.run([py, *a], check=True)
def probe(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip())
def ff(*a, cwd=None):
    r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *a], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode: sys.exit(r.stderr[-1500:])

# ---------- 1. cards ----------
T.vcard = lambda *a, **k: None                                 # no 9:16 cards here (and never into the l30 _v folders)
M = load(f'u{L["n"]}', f'{L30}/u{L["n"]}_cards.py')
if hasattr(M, 'vsave'): M.vsave = lambda *a, **k: None
M.C.OUT = D; M.C.SUB = 'קורס GMDSS · ' + NAME
for fn in M.ALL:
    if fn.__name__ != 's01': fn()
if L['n'] == 13:                                                # s16 = AI video under an overlay, s17 overlay: u13_tw.py
    TW = load('u13tw', f'{L30}/u13_tw.py'); TW.OUT = D; TW.s16(); TW.s17()
I.C.OUT = D
I.title_card('s01_intro', L['bg'], f'קורס GMDSS · שיעור {K}', NAME, L['items'], L['focus'])

# ---------- 2. vo.txt and the new s01 narration ----------
vo = open(SRC_D + '/vo.txt', encoding='utf-8').read()
old1 = re.search(r'## s01_intro\n(.*?)\n', vo).group(1)
new1 = L.get('s01') or re.sub(r'^ברוך הבא לשיעור [^.]*? בקורס [^.]*\.', f'ברוך הבא לשיעור {ORD[K]} בקורס G M D S S.', old1)
assert new1 != old1, 'opening not replaced'
vo = vo.replace(old1, new1, 1)
open(D + '/vo.txt', 'w', encoding='utf-8', newline='\n').write(vo)
vo1 = os.path.join(W, 'vo_s01.txt'); open(vo1, 'w', encoding='utf-8').write('## s01_intro\n' + new1 + '\n')
aud = os.path.join(W, 'aud'); raw1 = os.path.join(W, 's01_raw.mp4')
run(L30 + '/el_tts.py', vo1, aud)
run(ROOT + '/tools/lesson/assemble.py', '--vo', vo1, '--audio', aud, '--cards', D, '--out', raw1)

# ---------- 3. recover the l30 clip timeline ----------
src = SRC_D + '/' + NAME + '.mp4'; TOT = probe(src); END = TOT - 4.0
sids = re.findall(r'^##\s*(\S+)', vo, re.M)
clips = []                                                      # (key, old image for matching, new image or video for output)
for sid in sids[1:]:
    vid = os.path.join(D, sid + '.mp4')
    clips.append((sid, os.path.join(SRC_D, sid + '.png'), vid if os.path.isfile(vid) else os.path.join(D, sid + '.png')))
    simpng = os.path.join(SRC_D, sid + '_sim.png')
    if os.path.isfile(simpng): clips.append((sid + '_sim', simpng, simpng))
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', src, '-vf', "select='gt(scene,0.03)',showinfo", '-an', '-f', 'null', '-'],
                   capture_output=True, text=True, encoding='utf-8', errors='replace')
cuts = sorted(float(x) for x in re.findall(r'pts_time:([\d.]+)', r.stderr))
T0 = next(c for c in cuts if c > 4.0)                           # end of the old s01
crop = lambda im: im.crop((64, 10, 160, 90))                    # right part of a 160x90 thumb: right block, no watermark corner
refs = [crop(Image.open(c[1]).convert('L').resize((160, 90))) for c in clips]
FPS = 5
raw_fr = subprocess.run(['ffmpeg', '-loglevel', 'error', '-ss', f'{T0 + 0.1:.3f}', '-to', f'{END - 0.05:.3f}', '-i', src,
                         '-vf', f'fps={FPS},scale=160:90,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
frames = [crop(Image.frombytes('L', (160, 90), raw_fr[k:k + 14400])) for k in range(0, len(raw_fr) - 14399, 14400)]
dist = lambda a, b: ImageStat.Stat(ImageChops.difference(a, b)).mean[0]
C_ = [[dist(f, r_) for r_ in refs] for f in frames]
N, Mn = len(frames), len(refs); INF = float('inf')
acc = [[INF] * Mn for _ in range(N)]; back = [[0] * Mn for _ in range(N)]
acc[0][0] = C_[0][0]
for i in range(1, N):                                           # monotonic alignment: each frame stays on its clip or moves to the next
    for j in range(Mn):
        stay, move = acc[i - 1][j], (acc[i - 1][j - 1] if j else INF)
        back[i][j] = 0 if stay <= move else 1; acc[i][j] = min(stay, move) + C_[i][j]
assert acc[-1][-1] < INF, 'alignment failed'
path, j = [], Mn - 1
for i in range(N - 1, -1, -1):
    path.append(j); j -= back[i][j]
path.reverse()
starts = [T0]
for i in range(1, N):
    if path[i] != path[i - 1]:
        t = T0 + 0.1 + (i - 0.5) / FPS                          # change between frames i-1 and i; snap to the exact scene cut
        near = [c for c in cuts if abs(c - t) <= 0.25]
        starts.append(min(near, key=lambda c: abs(c - t)) if near else round(t / 0.04) * 0.04)
assert len(starts) == len(clips), f'{len(starts)} starts for {len(clips)} clips'
spans = list(zip(starts, starts[1:] + [END]))
worst = max(min(C_[i][path[i]] for i in [k]) for k in range(N))
print('alignment: worst frame distance', round(worst, 1))
print('clips', len(clips), 'first', [round(s, 2) for s in starts[:5]])

# ---------- 4. raw video: new s01 + new cards on the old timeline + old audio ----------
parts = []
for i, ((key, _, img), (a, b)) in enumerate(zip(clips, spans)):
    o = os.path.join(W, f'c{i:02d}.mp4'); d = f'{b - a:.3f}'
    if img.endswith('.mp4'):
        ff('-stream_loop', '-1', '-i', img, '-t', d, '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1',
           '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '25', '-an', o)
    else:
        ff('-loop', '1', '-i', img, '-t', d, '-vf', 'scale=1280:720,setsar=1', '-c:v', 'libx264', '-tune', 'stillimage', '-pix_fmt', 'yuv420p', '-r', '25', o)
    parts.append(o)
lst = os.path.join(W, 'parts.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
rest_v = os.path.join(W, 'rest_v.mp4'); ff('-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', rest_v)
d1 = probe(raw1)                                                # audio built separately as PCM (mixing mp4 audio in concat broke timestamps)
a1, a2, aa = (os.path.join(W, x) for x in ('a_s01.wav', 'a_rest.wav', 'a_all.wav'))
ff('-i', raw1, '-vn', '-af', f'apad,atrim=0:{d1:.3f}', '-ar', '44100', '-ac', '2', '-c:a', 'pcm_s16le', a1)
ff('-ss', f'{T0:.3f}', '-to', f'{END:.3f}', '-i', src, '-vn', '-ar', '44100', '-ac', '2', '-c:a', 'pcm_s16le', a2)
ff('-i', a1, '-i', a2, '-filter_complex', '[0:a][1:a]concat=n=2:v=0:a=1[a]', '-map', '[a]', '-c:a', 'pcm_s16le', aa)
raw = os.path.join(W, 'lesson_raw.mp4')
ff('-i', raw1, '-i', rest_v, '-i', aa, '-filter_complex', '[0:v][1:v]concat=n=2:v=1:a=0[v]', '-map', '[v]', '-map', '2:a',
   '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '25', '-preset', 'medium', '-c:a', 'aac', '-ar', '44100', '-ac', '2', '-b:a', '192k', '-movflags', '+faststart', raw)
print('raw', round(probe(raw), 2), 'expected', round(d1 + END - T0, 2))
out = os.path.join(D, NAME + '.mp4')
run(ROOT + '/tools/lesson/brand.py', raw, out)
NEW = 3.0 + probe(raw1); shift = NEW - T0
print(f'old s01 ended {T0:.2f}s, new s01 ends {NEW:.2f}s, total {probe(out):.0f}s (l30 {TOT:.0f}s)')

# ---------- 5. captions without niqqud ----------
os.environ['SUBS_WORK'] = os.path.join(W, 'subs'); os.environ['SUBS_PLAIN'] = '1'
b1 = os.path.join(W, 's01_branded.mp4'); run(ROOT + '/tools/lesson/brand.py', raw1, b1)
cap1 = os.path.join(W, 's01_cap.mp4'); run(L30 + '/subs.py', vo1, aud, b1, cap1)
NIQ = re.compile(r'[\u0591-\u05C7]')
ACRO = [('G M D S S', 'GMDSS'), ('M M S I', 'MMSI'), ('V H F', 'VHF'), ('D S C', 'DSC'), ('R C C', 'RCC'), ('M S I', 'MSI'), ('L U T', 'LUT'),
        ('M C C', 'MCC'), ('M F', 'MF'), ('H F', 'HF'), ('A אחת', 'A1'), ('A שתיים', 'A2'), ('A שלוש', 'A3'), ('A ארבע', 'A4')]
def parse(p):
    out = []
    for blk in open(p, encoding='utf-8-sig').read().strip().split('\n\n'):
        ln = blk.split('\n'); a, b = [sum(float(x) * m for x, m in zip(t.replace(',', '.').split(':'), (3600, 60, 1))) for t in ln[1].split(' --> ')]
        out.append((a, b, [l.lstrip('\u200f') for l in ln[2:]]))
    return out
def clean(l):
    l = NIQ.sub('', l)
    for x, y in ACRO: l = l.replace(x, y)
    return l
ev = [(a, b, ls) for a, b, ls in parse(os.path.splitext(cap1)[0] + '.srt') if a < NEW]
ev += [(a + shift, b + shift, [clean(l) for l in ls]) for a, b, ls in parse(SRC_D + '/' + NAME + ' - כתוביות.srt') if a >= T0 - 0.05]
hdr = re.search(r'hdr = """(.*?)"""', open(L30 + '/subs.py', encoding='utf-8').read(), re.S).group(1)
ts = lambda t: f'{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}'
st = lambda t: f'{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d},{int(round((t%1)*1000)) % 1000:03d}'
sub = os.path.join(W, 'subs'); os.makedirs(os.path.join(sub, 'fonts'), exist_ok=True)
for fn in ('arial.ttf', 'arialbd.ttf'): shutil.copy('C:/Windows/Fonts/' + fn, os.path.join(sub, 'fonts', fn))
open(os.path.join(sub, 'all.ass'), 'w', encoding='utf-8-sig').write(hdr + ''.join(
    f'Dialogue: 0,{ts(a)},{ts(b)},Default,,0,0,0,,' + r'\N'.join('\u202b' + l + '\u202c' for l in ls) + '\n' for a, b, ls in ev))
capd = os.path.join(D, NAME + ' - כתוביות')
open(capd + '.srt', 'w', encoding='utf-8-sig').write('\n'.join(f'{n}\n{st(a)} --> {st(b)}\n' + '\n'.join('\u200f' + l for l in ls) + '\n' for n, (a, b, ls) in enumerate(ev, 1)))
ff('-i', out, '-vf', 'ass=all.ass:fontsdir=fonts', '-c:v', 'libx264', '-crf', '21', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', capd + '.mp4', cwd=sub)

# ---------- 6. companion: the l30 companion with the new title line and s01 paragraph ----------
comp = open(SRC_D + '/' + NAME + '.txt', encoding='utf-8').read().split('\n')
comp[0] = f'{NAME} · קורס GMDSS · שיעור {K}'
i = next(n for n, l in enumerate(comp) if l.startswith('# ')) + 1
comp[i] = niqqud_apply(new1, load_lexicon())
open(os.path.join(D, NAME + '.txt'), 'w', encoding='utf-8', newline='\n').write('\n'.join(comp))
print('DONE', K, NAME, f'{probe(out):.0f}s')
