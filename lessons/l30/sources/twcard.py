"""Tailwind left panels for l30 cards: HTML (Tailwind CDN, Heebo) over an optional photo, rendered by tw_render.js.
A card = PIL base + left_panel caption + this panel pasted into inner() + PIL right_block."""
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, 'assets'); WRK = os.path.join(HERE, '_tw'); os.makedirs(WRK, exist_ok=True)

HEAD = """<!doctype html><html dir="rtl" lang="he"><head><meta charset="utf-8">
<script src="https://cdn.tailwindcss.com/3.4.16"></script>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;800&display=swap" rel="stylesheet">
<style>html,body{{margin:0;background:transparent;font-family:Heebo,sans-serif}} .ltr{{direction:ltr;unicode-bidi:isolate}}</style></head>
<body><div class="relative overflow-hidden bg-slate-950" style="width:{w}px;height:{h}px">{bg}{shade}{body}</div></body></html>"""

def asset(name):
    for ext in ('.jpg', '.png'):
        p = os.path.join(A, name + ext)
        if os.path.isfile(p): return 'file:///' + p.replace('\\', '/')
    raise FileNotFoundError(name)

def panel(name, body, w, h, bg=None, pos='center', shade=0.0):
    """Render body HTML over photo `bg` (assets name) to _tw/<name>.png. shade: 0..1 dark veil for legibility."""
    bgh = f'<img src="{asset(bg)}" class="absolute inset-0 w-full h-full object-cover" style="object-position:{pos}">' if bg else ''
    sh = f'<div class="absolute inset-0" style="background:rgba(2,6,23,{shade})"></div>' if shade else ''
    hp, pp = os.path.join(WRK, name + '.html'), os.path.join(WRK, name + '.png')
    open(hp, 'w', encoding='utf-8').write(HEAD.format(w=w, h=h, bg=bgh, shade=sh, body=body))
    subprocess.run(['node', os.path.join(HERE, 'tw_render.js'), hp, pp, str(w), str(h)], check=True, capture_output=True)
    return pp

# ---------- components ----------
S = 1.3   # global type scale: panels are shown at ~half size in the 1280x720 video
TONES = {'green': ('ring-emerald-400', 'text-emerald-300', 'bg-emerald-500'), 'red': ('ring-rose-400', 'text-rose-300', 'bg-rose-500'),
         'amber': ('ring-amber-400', 'text-amber-300', 'bg-amber-500'), 'sky': ('ring-sky-400', 'text-sky-300', 'bg-sky-500'),
         'slate': ('ring-slate-500', 'text-slate-300', 'bg-slate-600')}

def chip(text, tone='green', size=30, cls=''):
    r, t, _ = TONES[tone]
    return f'<div class="inline-flex items-center px-5 py-2 rounded-full bg-slate-900/85 backdrop-blur ring-2 {r} text-white font-bold whitespace-nowrap {cls}" style="font-size:{size * S:.0f}px">{text}</div>'

def glass(inner, cls=''):
    return f'<div class="rounded-3xl bg-slate-950/80 backdrop-blur-md ring-1 ring-white/15 shadow-2xl {cls}">{inner}</div>'

def tile(head, sub, tone='green', cls='', hs=44, ss=24):
    r, t, _ = TONES[tone]
    return (f'<div class="rounded-2xl bg-slate-900/85 backdrop-blur ring-2 {r} p-3 flex flex-col items-center justify-center text-center {cls}">'
            f'<div class="{t} font-extrabold leading-none ltr" style="font-size:{hs * S:.0f}px">{head}</div>'
            f'<div class="text-white/90 mt-2 leading-tight" style="font-size:{ss * S:.0f}px">{sub}</div></div>')

def row(icon, text, tone='green', size=30):
    r, t, b = TONES[tone]
    return (f'<div class="flex items-center gap-4"><div class="w-16 h-16 rounded-full {b} flex items-center justify-center text-white font-extrabold text-[34px] shrink-0">{icon}</div>'
            f'<div class="text-white font-semibold" style="font-size:{size * S:.0f}px">{text}</div></div>')

def digits(groups):
    """groups: [(digits, tone_or_None, label)] -> boxed digit strip, left-to-right."""
    out = []
    for ds, tone, lab in groups:
        cls = (TONES[tone][2] + ' text-white') if tone else 'bg-slate-800 text-white/90'
        boxes = ''.join(f'<div class="w-[62px] h-[78px] rounded-xl {cls} flex items-center justify-center font-extrabold text-[44px]">{c}</div>' for c in ds)
        out.append(f'<div class="flex flex-col items-center gap-2"><div class="flex gap-1.5">{boxes}</div>'
                   f'<div class="text-white/80 text-[22px] font-semibold">{lab}</div></div>')
    return '<div class="flex gap-4 justify-center" dir="ltr">' + ''.join(out) + '</div>'


# ---------- vertical (9:16) cards: one phone screen, no scrolling ----------
VW, VH = 1080, 1920
VTOP = 1080 * 1060 // 1180          # the 1180x1060 visual panel, scaled to full width

VHEAD = """<!doctype html><html dir="rtl" lang="he"><head><meta charset="utf-8">
<script src="https://cdn.tailwindcss.com/3.4.16"></script>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;800&display=swap" rel="stylesheet">
<style>html,body{{margin:0;font-family:Heebo,sans-serif}} .ltr{{direction:ltr;unicode-bidi:isolate}}
body{{background:radial-gradient(120% 60% at 50% 35%,#16305a 0%,#0b1a33 70%)}}</style></head>
<body><div data-page class="relative overflow-hidden flex flex-col" style="width:{w}px;height:{h}px">{body}</div></body></html>"""

def _fit(tag, name, n, cls, html):
    return f'<{tag} data-name="{name}" data-max-lines="{n}" class="{cls}">{html}</{tag}>'

def vbottom(sub, title, text, q=None):
    """Title / explanation / question block, sized for a phone. Line limits are enforced by tw_render.js."""
    out = (f'<div class="text-sky-300 text-[30px] text-center">{sub}</div>'
           + _fit('div', 'title', 1, 'text-white font-extrabold text-[66px] leading-[1.15] text-center mt-1', title)
           + '<div class="mx-auto my-3 h-[10px] w-[120px] rounded-full bg-emerald-500"></div>'
           + _fit('div', 'text', 3 if q else 6, 'text-white leading-[1.35] text-center ' + ('text-[38px]' if q else 'text-[46px]'), text))
    if q:
        head, qtext, opts, ok = q
        rows = ''.join(
            _fit('div', f'opt{i}', 1, 'rounded-xl px-4 py-[6px] text-[33px] leading-[1.3] '
                 + ('bg-emerald-900/70 ring-2 ring-emerald-400 text-emerald-300 font-bold' if i == ok else 'text-white/90'),
                 f'<span class="{"text-emerald-300" if i == ok else "text-slate-400"} font-bold">{"אבגד"[i]}:</span> {o}')
            for i, o in enumerate(opts))
        out += ('<div class="mt-5 rounded-3xl bg-slate-800/80 ring-1 ring-white/15 px-6 py-5 space-y-2">'
                f'<div class="text-amber-400 font-bold text-[28px]">{head}</div>'
                + _fit('div', 'question', 2, 'text-white font-semibold text-[35px] leading-[1.3]', qtext) + rows + '</div>')
    return out

def vcard(path, caption, visual, bottom):
    """visual: html for the top area (VW x VTOP) ; bottom: html from vbottom(). Raises if any text overflows."""
    body = (f'<div class="h-[120px] flex items-center justify-center text-white font-extrabold text-[52px] shrink-0">{caption}</div>'
            f'<div class="relative shrink-0 overflow-hidden" style="height:{VTOP}px">{visual}</div>'
            f'<div class="flex-1 flex flex-col justify-center px-10 pb-6">{bottom}</div>')
    hp = os.path.join(WRK, 'v_' + os.path.basename(path).replace('.png', '.html'))
    open(hp, 'w', encoding='utf-8').write(VHEAD.format(w=VW, h=VH, body=body))
    r = subprocess.run(['node', os.path.join(HERE, 'tw_render.js'), hp, path, str(VW), str(VH)], check=True, capture_output=True, text=True, encoding='utf-8')
    if 'OVERFLOW' in r.stdout:
        raise ValueError(f'{os.path.basename(path)}: ' + r.stdout.split('OVERFLOW', 1)[1].strip())
    return path

def vimg(png):
    return f'<img src="file:///{png.replace(chr(92), "/")}" class="absolute inset-0 w-full h-full">'

def vphoto(name, pos='center'):
    return f'<img src="{asset(name)}" class="absolute inset-0 w-full h-full object-cover" style="object-position:{pos}">'