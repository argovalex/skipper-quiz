"""Lesson 19 (l30): השלמות. The SQ5 questions no earlier lesson asked (151, 103, 155, 156, 121, 43, 77, 65, 109), each with a short recap.
Wide 16:9 cards by default; 9:16 phone cards (_v/) only with --mobile, after Alex approves the final video + subtitles."""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U6 = _load('u06', 'u06_cards.py'); U8 = _load('u08', 'u08_cards.py'); U12 = _load('u12', 'u12_cards.py')
import twcard as T
from twcard import chip, glass, tile, row
from PIL import Image
NAME = 'השלמות'
C.OUT = os.path.join(HERE, '..', 'cards', NAME); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · השלמות'
F, text_c, text_r, dot, base, left_panel, right_block, save, RC = C.F, C.text_c, C.text_r, C.dot, C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, GREEN, GREEN_L, BLUE_L, PANEL = C.TEXT, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL
photo = U8.photo; credit = U12.credit
CR = {'bluemarble': 'Image: NASA · Public domain', 'u12_plotter': 'Photo: RheinSkipper · CC BY-SA 3.0',
      'u18_vhf16': 'Photo: PaterMcFly · CC BY 3.0 · edited'}
U12.CREDIT.update(CR)
X0, Y0, X1, Y1 = [int(v) for v in U5.inner()]; PW, PH = X1 - X0, Y1 - Y0
VOUT = os.path.join(C.OUT, '_v'); VSUB = 'שיעור 19 · השלמות'
MOBILE = '--mobile' in sys.argv   # 9:16 cards only after Alex approves the final wide video + subtitles (Alex 2026-10-14)
if MOBILE: os.makedirs(VOUT, exist_ok=True)

def vcredit(bg):
    return f'<div class="absolute bottom-1 right-2 ltr text-white/70 text-[16px]">{CR[bg]}</div>' if bg in CR else ''

def card(sid, caption, body, title, text, q=None, bg=None, pos='center', shade=0.0):
    """Same body HTML rendered twice: 1180x1060 for the wide card, 1080 x VTOP for the phone card (--mobile)."""
    if MOBILE:
        vp = T.panel('v_' + sid, body, T.VW, T.VTOP, bg, pos, shade)
        T.vcard(os.path.join(VOUT, sid + '.png'), caption, T.vimg(vp) + vcredit(bg), T.vbottom(VSUB, title, text, q))
    im, d = base(); left_panel(d, caption)
    pp = T.panel(sid, body, PW, PH, bg, pos, shade); p = Image.open(pp).convert('RGBA'); im.paste(p, (X0, Y0), p)
    if bg in CR: credit(d, (X0, Y0, X1, Y1), bg)
    right_block(d, title, text, q); save(im, sid)

def top(html):
    return f'<div class="absolute top-6 inset-x-6 flex justify-center">{html}</div>'

def fill(html, t=24):
    return f'<div class="absolute inset-x-6 bottom-6 flex flex-col justify-center gap-4" style="top:{t}px">{html}</div>'

def bottom(html):
    return f'<div class="absolute bottom-6 inset-x-6">{html}</div>'

def tiles(items, h=200, hs=46, ss=26, cols=2):
    return f'<div class="grid grid-cols-{cols} gap-4">' + ''.join(tile(n, s, t, f'h-[{h}px]', hs, ss) for n, s, t in items) + '</div>'

def rows(*rs, gap=3):
    return glass(f'<div class="p-6 space-y-{gap}">' + ''.join(row(*r) for r in rs) + '</div>')

# ---------- cards ----------
ITEMS = ['שמיים · השמש והעגלה הגדולה', 'מצפנים · וריאציה ושער שטף', 'הגה אוטומטי · GPS', 'קשר · טווח, הספק ו-MMSI']

def s01():
    if MOBILE: T.vcard(os.path.join(VOUT, 's01_intro.png'), 'שיעור 19', T.vphoto('u14_chart_table', '50% 45%'),
                       T.vbottom('קורס ניווט חופי ומכשירים', 'השלמות', '<br>'.join(ITEMS)))
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u14_chart_table', focus=(0.5, 0.45))
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 19', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'השלמות', F(118), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(ITEMS):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

import subprocess
A = os.path.join(HERE, 'assets'); BG = '#030a18'   # background colour of the l30 Q102 animation

def overlay(name, body, w, h):
    """Transparent Tailwind overlay (no panel background) for a video card."""
    hp, pp = os.path.join(T.WRK, name + '.html'), os.path.join(T.WRK, name + '.png')
    open(hp, 'w', encoding='utf-8').write(T.HEAD.replace(' bg-slate-950', '').format(w=w, h=h, bg='', shade='', body=body))
    subprocess.run(['node', os.path.join(HERE, 'tw_render.js'), hp, pp, str(w), str(h)], check=True, capture_output=True)
    return pp

def rotation_assets():
    """Sun + orbiting Earth from the l30 Q102 question video (Alex 2026-10-14), cropped to the animation, padded to the panel."""
    src = os.path.join(A, 'u19_rotation_src.mp4'); vid = os.path.join(A, 'u19_rotation.mp4'); still = os.path.join(A, 'u19_rotation.jpg')
    if os.path.isfile(vid) and os.path.isfile(still): return vid
    vf = f'crop=1080:760:0:300,scale={PW}:-2,pad={PW}:{PH}:0:0:{BG},setsar=1'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '2', '-t', '20', '-i', src, '-an', '-vf', vf, '-r', '25', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', vid], check=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '3', '-i', vid, '-frames:v', '1', '-q:v', '2', still], check=True)
    return vid

def s02():
    head = top(chip('W ⟶ E · כדור הארץ מסתובב ממערב למזרח', 'sky', 30))
    body = head + bottom(rows(('☀', 'לכן השמש זורחת במזרח', 'amber', 32), ('✗', 'הסיבוב סביב השמש · עונות', 'red', 32)))
    q = ('שאלה מהמאגר · 151', 'השמש זורחת במזרח ושוקעת במערב בגלל ש:',
         ['כדור הארץ נע מערבה סביב השמש', 'כדור הארץ סובב סביב צירו ממערב למזרח', 'ציר כדור הארץ סובב סביב כוכב הצפון', 'כדור הארץ סובב סביב צירו ממזרח למערב'], 1)
    vid = rotation_assets()
    card('s02_q151', 'זריחה ושקיעה', '', 'תשובה ב', 'כדור הארץ סובב סביב צירו ממערב למזרח.', q)        # base: right block, empty panel
    base = os.path.join(C.OUT, 's02_q151.png'); ov = overlay('s02_ov', body, PW, PH)
    fc = f'[0:v][1:v]overlay={X0}:{Y0}[b];[b][2:v]overlay={X0}:{Y0},scale=1280:720,format=yuv420p[o]'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-i', base, '-i', vid, '-loop', '1', '-i', ov, '-filter_complex', fc,
                    '-map', '[o]', '-t', '20', '-r', '25', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', os.path.join(C.OUT, 's02_q151.mp4')], check=True)
    card('s02_q151', 'זריחה ושקיעה', body, 'תשובה ב', 'כדור הארץ סובב סביב צירו ממערב למזרח.', q, bg='u19_rotation')   # poster still
    if MOBILE:   # phone card video: empty-visual card + clip + overlay, placed where vcard puts the visual
        from PIL import ImageChops
        poster = os.path.join(VOUT, 's02_q151.png'); vbase = os.path.join(T.WRK, 'v_s02_base.png')
        T.vcard(vbase, 'זריחה ושקיעה', '', T.vbottom(VSUB, 'תשובה ב', 'כדור הארץ סובב סביב צירו ממערב למזרח.', q))
        x0, y0, x1, y1 = ImageChops.difference(Image.open(poster).convert('RGB'), Image.open(vbase).convert('RGB')).getbbox()
        vov = overlay('v_s02_ov', body, T.VW, T.VTOP)
        fc = (f'[1:v]scale={T.VW}:{T.VTOP},setsar=1[v];[0:v][v]overlay=0:{y0}[b];[b][2:v]overlay=0:{y0},format=yuv420p[o]')
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-i', vbase, '-i', vid, '-loop', '1', '-i', vov, '-filter_complex', fc,
                        '-map', '[o]', '-t', '20', '-r', '25', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', os.path.join(VOUT, 's02_q151.mp4')], check=True)
        print('visual top', y0, '(diff box', x0, y0, x1, y1, ')')

def s03():
    img = f'<img src="{T.asset("u19_q103")}" class="w-full rounded-2xl bg-white p-2">'
    body = fill(img + '<div class="flex justify-center gap-3">' + chip('ד · 4 כוכבים בארגז + 3 בידית', 'green', 30) + '</div>')
    card('s03_q103', 'העגלה הגדולה', body, 'תשובה ד', 'ארבעה כוכבים בארגז ושלושה בידית. שני כוכבי הקצה מצביעים על כוכב הצפון.',
         ('שאלה מהמאגר · 103', 'בחר מהאיורים את קבוצת הכוכבים "העגלה הגדולה".', ['איור א', 'איור ב', 'איור ג', 'איור ד'], 3))

def s04():
    body = bottom(tiles([('מגנטי', 'וריאציה · ✓', 'green'), ('שער שטף', 'וריאציה · ✓', 'green'), ("ג'יירו", 'צפון אמיתי · ✗', 'red'), ('דויאציה', 'זה של הסירה', 'amber')], 150, 40, 24, 4))
    card('s04_q155', 'וריאציה', body, 'תשובה א', 'מצפן מגנטי ושער שטף מודדים צפון מגנטי, ולכן הווריאציה זהה בשניהם.',
         ('שאלה מהמאגר · 155', 'הווריאציה משפיעה באותה מידה על:',
          ['מצפן מגנטי ומצפן שער שטף', 'מצפן סביבוני ומצפן אזימוט', 'מצפנים בלי טבלת דויאציה', 'מצפנים בכלי שייט שאינם ממתכת'], 0), bg='u19_flux_coils', pos='50% 30%', shade=0.1)

def s05():
    body = bottom(rows(('א', 'כמו מצפן מגנטי · כוחות מגנטיים', 'green', 30), ('ב', 'אלקטרומגנטים זעירים במקום מוטות', 'green', 30), ('✗', 'לא מבטל וריאציה ודויאציה', 'red', 30)))
    card('s05_q156', 'שער שטף', top(chip('אותו נושא · נוסח אחר', 'amber', 30)) + body, 'א׳ ו-ב׳', 'מורה על הצפון המגנטי, עם אלקטרומגנטים זעירים במקום מוטות.',
         ('שאלה מהמאגר · 156', 'כיצד פועל מצפן FLUX GATE (שער שטף מגנטי)?',
          ['כמו מצפן מגנטי, בהשפעת כוחות מגנטיים', 'אלקטרומגנטים זעירים במקום מוטות', 'שדה עצמי שמבטל וריאציה ודויאציה', 'א ו-ב נכונים'], 3), bg='u19_flux_coils', pos='50% 35%', shade=0.15)

def s06():
    body = fill(tiles([('רגישות גבוהה', 'מתקן כל סטייה · עוד חשמל', 'amber'), ('רגישות נמוכה', 'מחכה לסטייה · ים גבוה', 'sky')], 260, 46, 28)
                + rows(('⏱', 'קובעת כמה מהר ההגה מתקן', 'green', 32)))
    card('s06_q121', 'רגישות', body, 'תשובה ד', 'רגישות מגדילה או מקטינה את מהירות התגובה לשינויים בקורס.',
         ('שאלה מהמאגר · 121', 'למה יגרום שינוי רגישות התגובה בהגה האוטומטי?',
          ['ניתוק מהמצברים וחיבור לאלטרנטור', 'חיבור ההגה למעקב אחרי ה-GPS', 'שינויי קורס קיצוניים', 'שינוי מהירות התגובה לשינויי קורס'], 3), bg='u11_p70', shade=0.65)

def s07():
    body = fill(tiles([('SET UP', 'תצוגות ויחידות · בחירה שלך', 'sky'), ('אתחול', 'מציאת הלוויינים מחדש', 'amber')], 220, 46, 28)
                + rows(('⏸', 'כבוי הרבה זמן', 'amber', 30), ('500', 'הועבר כבוי מעל 500 ק״מ', 'amber', 30)))
    card('s07_q43', 'SET UP ואתחול', body, 'כל התשובות', 'SET UP הוא בחירה שלך. אתחול נדרש אחרי הרבה זמן כבוי, או מעבר של יותר מ-500 ק״מ.',
         ('שאלה מהמאגר · 43', 'ההבדל בין SET UP ו-INITIALISATION (אתחול) הוא:',
          ['יש מקלטים שדורשים הזנת אתר, תקן וגובה', 'SET UP לתצוגות, אתחול אחרי זמן כבוי', 'במקלטים חדשים SET UP כולל הכל', 'כל התשובות נכונות'], 3), bg='u12_plotter', shade=0.7)

def s08():
    body = fill(tiles([('קו ראייה', 'בין האנטנות · ✓', 'green'), ('מזג אוויר', 'כמעט לא משפיע · ✗', 'red'), ('יום ולילה', 'זה HF · ✗', 'red'), ('הספק', 'לא עובר את האופק · ✗', 'red')], 210, 44))
    card('s08_q77', 'טווח VHF', body, 'תשובה ד', 'גלי VHF עוברים בקו ישר. הטווח תלוי בקו הראייה בין האנטנות.',
         ('שאלה מהמאגר · 77', 'מהו התנאי העיקרי הקובע את טווח השידור ב-VHF?',
          ['תנאי מזג אוויר', 'יום או לילה', 'הספק שידור', 'קו ראייה בין האנטנות'], 3), bg='u13_range', shade=0.6)

def s09():
    body = fill(tiles([('25W', 'הספק גבוה', 'amber'), ('1W', 'הספק נמוך · ברירת מחדל', 'green')], 200, 60, 28)
                + rows(('א', 'נמוך, וגבוה רק כשלא שומעים', 'green', 30), ('ב', 'ניסיון ותקשורת בתוך הספינה', 'green', 30), ('ג', 'בתוך הנמל או המרינה', 'green', 30)))
    card('s09_q65', 'הספק נמוך', body, 'כל התשובות', 'משדרים בוואט אחד, ועוברים לעשרים וחמישה רק כשלא שומעים אותנו.',
         ('שאלה מהמאגר · 65', 'אילו שידורים משודרים בהספק נמוך?',
          ['נמוך, וגבוה רק אם לא שומעים', 'שידורי ניסוי ותקשורת פנים ספינתית', 'שידורים בתוך הנמל או המרינה', 'כל התשובות נכונות'], 3), bg='u18_vhf16', shade=0.75)

def s10():
    dig = lambda s, c: f'<span class="{c}">{s}</span>'
    num = ('<div class="ltr text-center font-extrabold text-[72px] tracking-wider">' + dig('232', 'text-amber-300') + dig('000432', 'text-white') + '</div>'
           '<div class="flex justify-center gap-8 text-[30px] text-white/85"><span>קוד מדינה · ישראל 428</span><span>9 ספרות</span></div>')
    body = fill(glass(f'<div class="p-6 space-y-2">{num}</div>') + rows(('2-7', 'ספינה · מתחיל בקוד המדינה', 'green', 30), ('0', 'קבוצה', 'amber', 30), ('00', 'תחנת חוף', 'sky', 30)))
    card('s10_q109', 'זיהוי ספינה', body, 'תשובה ב', 'תשע ספרות, ומתחיל בקוד המדינה. א׳ קצר מדי, ו-ג׳ מתחיל באפס, זו קבוצה.',
         ('שאלה מהמאגר · 109', 'מה מהתשובות הרשומות מציין זיהוי של ספינה?',
          ['42800501', '232000432', '042811111', 'תשובה א+ב נכונות'], 1), bg='u18_vhf16', shade=0.8)

def s11():
    items = ['השמש זורחת במזרח · סיבוב ממערב למזרח', 'העגלה הגדולה · 4 + 3 כוכבים', 'וריאציה · מגנטי ושער שטף, לא ג׳יירו', 'רגישות ההגה · מהירות התיקון',
             'אתחול GPS · אחרי זמן כבוי', 'טווח VHF · קו ראייה', 'הספק נמוך · כשאפשר', 'MMSI ספינה · 9 ספרות, קוד מדינה']
    lst = ''.join(f'<div class="flex items-center gap-4 rounded-2xl bg-slate-800/80 px-5 py-2 text-white text-[32px]"><span class="w-4 h-4 rounded-full {"bg-emerald-400" if i < 4 else "bg-amber-400"} shrink-0"></span>{t}</div>' for i, t in enumerate(items))
    if MOBILE: T.vcard(os.path.join(VOUT, 's11_summary.png'), 'סיכום', T.vphoto('u14_chart_table', '50% 45%'), f'<div class="space-y-2">{lst}</div>')
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u14_chart_table', focus=(0.5, 0.45))
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 4 else C.ORANGE)
        text_r(d, 2380, y + 20, s, F(42, False), TEXT)
    save(im, 's11_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11]

def vsheet():
    fs = sorted(f for f in os.listdir(VOUT) if f.startswith('s') and f.endswith('.png'))
    c = 6; sh = Image.new('RGB', (c * 300, ((len(fs) + c - 1) // c) * 533))
    for i, f in enumerate(fs):
        sh.paste(Image.open(os.path.join(VOUT, f)).convert('RGB').resize((300, 533)), ((i % c) * 300, (i // c) * 533))
    sh.save(os.path.join(VOUT, '_sheet.png'))

if __name__ == '__main__':
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:                              # OneDrive can lock a freshly written PNG
                    import time; time.sleep(2)
    U6.sheet.__globals__.__setitem__('C', C); U6.sheet()
    if MOBILE: vsheet()
