"""Lesson 13 s16/s17: realistic media + Tailwind overlay (rendered by tw_render.js).
s16 = AI video (u13_range.mp4) under a transparent Tailwind overlay -> cards/<s16>.mp4 (+ poster .png)
s17 = AI photo (u13_block.jpg) as the HTML background -> cards/<s17>.png
usage: python u13_tw.py"""
import os, sys, subprocess, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); import nowin  # child processes (ffmpeg, node) without a console window
spec = importlib.util.spec_from_file_location('u13', os.path.join(HERE, 'u13_cards.py')); U = importlib.util.module_from_spec(spec); spec.loader.exec_module(U)
from PIL import Image
A = os.path.join(HERE, 'assets'); OUT = U.C.OUT; WRK = os.path.join(HERE, '_tw'); os.makedirs(WRK, exist_ok=True)
X0, Y0, X1, Y1 = [int(v) for v in U.inner()]; PW, PH = X1 - X0, Y1 - Y0

HEAD = """<!doctype html><html dir="rtl" lang="he"><head><meta charset="utf-8">
<script src="https://cdn.tailwindcss.com/3.4.16"></script>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;800&display=swap" rel="stylesheet">
<style>html,body{margin:0;background:transparent;font-family:Heebo,sans-serif}</style></head>
<body><div class="relative overflow-hidden" style="width:%dpx;height:%dpx;%s">%s</div></body></html>"""

def pin(x, y, text, tone):
    return (f'<div class="absolute -translate-x-1/2 flex flex-col items-center" style="left:{x}px;top:{y}px">'
            f'<div class="px-4 py-1.5 whitespace-nowrap rounded-full bg-slate-900/80 backdrop-blur ring-2 {tone} text-white text-[28px] font-semibold shadow-xl">{text}</div>'
            f'<div class="w-1 h-10 bg-white/80"></div><div class="w-4 h-4 rounded-full bg-white ring-4 ring-white/40"></div></div>')

def render(name, html):
    hp, pp = os.path.join(WRK, name + '.html'), os.path.join(WRK, name + '.png')
    open(hp, 'w', encoding='utf-8').write(html)
    subprocess.run(['node', os.path.join(HERE, 'tw_render.js'), hp, pp, str(PW), str(PH)], check=True)
    return pp

def s16():
    rows = [('יאכטה ↔ יאכטה', 16), ('יאכטה ↔ ספינה', 30), ('יאכטה ↔ תחנת חוף', 50)]
    bars = ''.join(
        f'<div class="flex items-center gap-4"><div class="w-[300px] text-white/90 text-[30px] font-semibold">{s}</div>'
        f'<div class="flex-1 h-12 rounded-full bg-white/10 overflow-hidden"><div class="h-full rounded-full bg-gradient-to-l from-emerald-400 to-teal-600 flex items-center justify-start pr-4" style="width:{nm / 60 * 100:.0f}%">'
        f'<span class="text-white text-[28px] font-extrabold" dir="ltr">{nm} NM</span></div></div></div>' for s, nm in rows)
    body = (pin(1030, 95, 'תחנת חוף', 'ring-amber-400')         # the yacht and ship move in the clip, so only the static mast is pinned
            + '<div class="absolute top-6 left-6 px-5 py-2 rounded-2xl bg-slate-900/80 ring-1 ring-white/20 text-white text-[30px] font-bold">גל ישיר · טווח אופק</div>'
            + f'<div class="absolute bottom-6 inset-x-6 rounded-3xl bg-slate-950/75 backdrop-blur-md ring-1 ring-white/15 p-6 space-y-4 shadow-2xl">{bars}'
            + '<div class="text-amber-300 text-[28px] font-semibold pt-1">בתיאוריה עד <span dir="ltr">60 NM</span> · אנטנה גבוהה = טווח ארוך</div></div>')
    ov = render('s16_overlay', HEAD % (PW, PH, '', body))
    base_png = os.path.join(OUT, 's16_range.png')        # card with the right block; panel area gets the video
    vid = os.path.join(A, 'u13_range.mp4')
    out = os.path.join(OUT, 's16_range.mp4')
    fc = (f'[1:v]scale={PW}:{PH}:force_original_aspect_ratio=increase,crop={PW}:{PH},setsar=1[v];'
          f'[0:v][v]overlay={X0}:{Y0}[b];[b][2:v]overlay={X0}:{Y0},scale=1280:720,format=yuv420p[o]')
    subprocess.run(['ffmpeg', '-y', '-loop', '1', '-i', base_png, '-stream_loop', '-1', '-i', vid, '-loop', '1', '-i', ov,
                    '-filter_complex', fc, '-map', '[o]', '-t', '8', '-r', '25', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', out], check=True,
                   capture_output=True)
    poster = Image.open(base_png).convert('RGB')                 # poster frame for the sheet: still + overlay
    g = Image.open(os.path.join(A, 'u13_range.jpg')).convert('RGB'); s = max(PW / g.width, PH / g.height)
    g = g.resize((round(g.width * s), round(g.height * s))); cx = (g.width - PW) // 2; g = g.crop((cx, 0, cx + PW, PH))
    poster.paste(g, (X0, Y0)); o = Image.open(ov).convert('RGBA'); poster.paste(o, (X0, Y0), o); poster.save(base_png)
    print('ok s16 video + poster')

def s17():
    bg = 'file:///' + os.path.join(A, 'u13_block.jpg').replace('\\', '/')
    cards = [('קו ראייה', 'בלי מכשולים בין האנטנות'), ('הספק', 'שידור חזק מגיע רחוק'), ('גובה', 'אנטנה גבוהה רואה רחוק'), ('התפשטות', 'תנאי האוויר')]
    grid = ''.join(f'<div class="rounded-2xl bg-slate-950/75 backdrop-blur ring-1 ring-emerald-400/60 p-4 text-center">'
                   f'<div class="text-emerald-300 text-[34px] font-extrabold">{h}</div><div class="text-white/90 text-[24px] mt-1">{s}</div></div>' for h, s in cards)
    body = (pin(180, 60, 'אנטנה גבוהה על הר', 'ring-amber-400') + pin(330, 360, 'מכשול', 'ring-rose-400') + pin(1110, 440, 'יאכטה', 'ring-emerald-400')
            + f'<div class="absolute bottom-6 inset-x-6 grid grid-cols-4 gap-4">{grid}</div>')
    style = f"background:url('{bg}') 3% 0/auto 100% no-repeat"
    pp = render('s17_panel', HEAD % (PW, PH, style, body))
    card = Image.open(os.path.join(OUT, 's17_range_q58.png')).convert('RGB'); o = Image.open(pp).convert('RGBA')
    card.paste(o, (X0, Y0), o); card.save(os.path.join(OUT, 's17_range_q58.png')); print('ok s17')

if __name__ == '__main__':
    U.s16(); U.s17()                       # fresh base cards (right block + empty panel)
    s17()
    if os.path.isfile(os.path.join(A, 'u13_range.mp4')): s16()
    else: print('missing assets/u13_range.mp4')
    U.sheet()
