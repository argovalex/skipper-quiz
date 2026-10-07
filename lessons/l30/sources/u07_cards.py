"""Lesson 7 (l30): מד מהירות ומד רוח. Realistic photos (assets/u7_*.jpg, Higgsfield nano_banana) with drawn overlays."""
import math, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U6 = _load('u06', 'u06_cards.py')
from PIL import Image, ImageDraw, ImageEnhance
import real as RL
C.OUT = os.path.join(HERE, '..', 'cards', 'מד מהירות ומד רוח'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · מד מהירות ומד רוח'
F, text_c, text_r, label, dot, arrow = C.F, C.text_c, C.text_r, C.label, C.dot, C.arrow
base, left_panel, right_block, save, LP, RC = C.base, C.left_panel, C.right_block, C.save, C.LP, C.RC
TEXT, ORANGE, CORAL, GREEN, GREEN_L, BLUE_L, PANEL, MUTED = C.TEXT, C.ORANGE, C.CORAL, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL, C.MUTED
readout, polar_pt, inner = U5.readout, U5.polar_pt, U5.inner
WHITE = U5.WHITE

def photo(im, box, name, rot=0, dim=1.0, focus=(0.5, 0.5)):
    """Cover-fit assets/<name>.jpg into box (cropped around focus), optionally rotated and darkened."""
    g = Image.open(os.path.join(RL.A, name + '.jpg')).convert('RGB')
    if rot: g = g.rotate(rot, expand=True)
    x0, y0, x1, y1 = [int(v) for v in box]; W, H = x1 - x0, y1 - y0
    s = max(W / g.width, H / g.height); g = g.resize((math.ceil(g.width * s), math.ceil(g.height * s)), Image.LANCZOS)
    cx = min(max(int(g.width * focus[0] - W / 2), 0), g.width - W); cy = min(max(int(g.height * focus[1] - H / 2), 0), g.height - H)
    g = g.crop((cx, cy, cx + W, cy + H))
    if dim != 1.0: g = ImageEnhance.Brightness(g).enhance(dim)
    im.paste(g, (x0, y0)); return ImageDraw.Draw(im)

def tag(d, p, s, col=WHITE, size=40, anchor='c'):
    """Label on a dark pill so it reads over a photo."""
    f = F(size); t = C.he(s); w = d.textlength(t, font=f)
    x = {'c': p[0] - w / 2, 'l': p[0], 'r': p[0] - w}[anchor]
    d.rounded_rectangle((x - 18, p[1] - size * 0.75, x + w + 18, p[1] + size * 0.75), 14, fill=(8, 14, 22))
    d.text((x, p[1] - size / 2), t, font=f, fill=col)

def vec(d, a, deg, L, col, w=10):
    b = polar_pt(a, L, deg); arrow(d, a, b, col, w, 40); return b

# ---------- cards ----------
def s01():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u7_boat_aerial', focus=(0.5, 0.45))
    readout(d, (60, 1120, 500, 1380), 'LOG · STW', '6.0 kn')
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 7', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'מד מהירות ומד רוח', F(130), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['למה קוראים לזה קשר', 'מטר לשנייה ≈ 2 קשרים', 'מד מהירות מול GPS', 'רוח אמיתית ורוח יחסית']):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    im, d = base(); left_panel(d, 'חבל עם קשרים ושעון חול')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, box, 'u7_chip_log', focus=(0.5, 0.6))
    tag(d, (x0 + 330, y0 + 140), 'חבל עם קשרים', CORAL)
    tag(d, (x1 - 200, y0 + 330), 'שעון חול', WHITE)
    tag(d, (x0 + 260, y1 - 330), 'משקולת עץ', WHITE)
    by = y1 - 220
    d.rounded_rectangle((x0 + 60, by, x1 - 60, by + 180), 26, fill=(8, 14, 22), outline=GREEN_L, width=4)
    label(d, ((x0 + x1) / 2, by + 60), 'קשר אחד = מייל ימי אחד בשעה', F(54), GREEN_L)
    label(d, ((x0 + x1) / 2, by + 130), '1 kn = 1 NM / h', F(44, False), TEXT)
    right_block(d, 'למה קשר', 'זורקים משקולת עץ קשורה לחבל עם קשרים. סופרים כמה קשרים עברו ביד עד שנגמר שעון החול. מכאן השם: מהירות בים נמדדת בקשרים.')
    save(im, 's02_log_history')

def s03():
    im, d = base(); left_panel(d, 'כלל אצבע למבחן')
    x0, y0, x1, y1 = inner(); cx = (x0 + x1) / 2
    d = photo(im, (x0, y0, x1, y1), 'u7_boat_aerial', dim=0.35, focus=(0.5, 0.5))
    d.rounded_rectangle((x0 + 60, y0 + 40, x1 - 60, y0 + 300), 26, fill=(8, 14, 22), outline=BLUE_L, width=4)
    label(d, (cx, y0 + 120), 'S = V × T', F(96), TEXT)
    label(d, (cx, y0 + 230), 'דרך = מהירות × זמן', F(46, False), MUTED)
    d.rounded_rectangle((x0 + 60, y0 + 360, x1 - 60, y0 + 620), 26, fill=(8, 14, 22), outline=GREEN_L, width=5)
    label(d, (cx, y0 + 450), '1 m/s ≈ 2 kn', F(96), GREEN_L)
    label(d, (cx, y0 + 560), 'מטר לשנייה × 2 = קשרים', F(46, False), TEXT)
    for i, (a, b) in enumerate([('1 m/s', '2 kn'), ('2.5 m/s', '5 kn'), ('3 m/s', '6 kn')]):
        y = y0 + 740 + i * 140
        label(d, (cx - 260, y), a, F(64), BLUE_L); arrow(d, (cx - 80, y), (cx + 80, y), WHITE, 6, 26); label(d, (cx + 260, y), b, F(64), GREEN_L)
    right_block(d, 'מטר לשנייה', 'מטר אחד בשנייה הוא בערך שני קשרים. יש מהירות במטרים לשנייה? כפול שתיים, וקיבלת קשרים.')
    save(im, 's03_speed_formula')

def s04():
    im, d = base(); left_panel(d, '15 מטר ב-5 שניות')
    x0, y0, x1, y1 = inner(); ph = (x0, y0, x1, y0 + 800)
    d = photo(im, ph, 'u7_buoy_twopanel', focus=(0.5, 0.0))   # Alex's image: sailboat, buoy at the bow (t=0) and at the stern (t=5)
    tag(d, (x1 - 220, y0 + 330), 'אורך 15 m', ORANGE, 40)
    for i, (s, col) in enumerate([('15 ÷ 5 = 3 m/s', TEXT), ('3 × 2 = 6 kn', GREEN_L)]):
        label(d, ((x0 + x1) / 2, y0 + 880 + i * 110), s, F(70), col)
    right_block(d, 'חישוב', 'אורך הסירה חלקי הזמן, כפול שתיים.',
                ('שאלה מהמאגר · 12', 'מכלי שיט שאורכו 15 מטרים מושלך בחרטום חפץ שצף בחלקו, חולפות 5 שניות עד הגעתו לירכתיים, מה מהירות כלי השיט בקשרים?',
                 ['3 קשרים', '1.853 קשרים', '6 קשרים בקירוב', '5.5 קשרים בדיוק'], 2))
    save(im, 's04_speed_q12')

def s05():
    im, d = base(); left_panel(d, '5 קשרים × 5 מטר = 25 מטר')
    x0, y0, x1, y1 = inner()
    d = photo(im, (x0, y0, x1, y0 + 560), 'u7_chip_log', focus=(0.55, 0.45))
    tag(d, (x0 + 300, y0 + 60), 'קשר כל 5 m', CORAL); tag(d, (x1 - 200, y0 + 60), '10 s', WHITE, 48)
    label(d, ((x0 + x1) / 2, y0 + 650), '25 m ÷ 10 s = 2.5 m/s', F(64), TEXT)
    w = (x1 - x0 - 100) / 3
    for i, (v, l) in enumerate([('5 kn', 'א'), ('5 NM / h', 'ב'), ('2.5 m/s', 'ג')]):
        bx = x1 - 30 - (i + 1) * w - i * 20
        d.rounded_rectangle((bx, y0 + 760, bx + w, y0 + 1000), 24, fill=PANEL, outline=GREEN_L, width=4)
        label(d, (bx + w / 2, y0 + 820), l, F(52), MUTED); label(d, (bx + w / 2, y0 + 920), v, F(60), GREEN_L)
    label(d, ((x0 + x1) / 2, y1 - 50), 'שלוש דרכים לכתוב את אותה מהירות', F(46), ORANGE)
    right_block(d, 'החבל עם הקשרים', 'כל התשובות נכונות.',
                ('שאלה מהמאגר · 13', 'מירכתי ספינה בתנועה, שוחרר חבל שעליו קשרים במרווחים קבועים של 5 מטרים בין קשר לקשר, מה מהירות כלי השיט, אם נמנו (בלי הקצה) חמישה קשרים בעשר שניות?',
                 ['5 קשרים', '5 מילים ימיים בשעה', '2.5 מטרים בשנייה', 'כל התשובות נכונות'], 3))
    save(im, 's05_speed_q13')

def s06():
    im, d = base(); left_panel(d, 'מד מהירות עם אימפלר')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=WHITE)
    d = photo(im, (x0 + 110, y0 + 20, x1 - 110, y1 - 140), 'u7_paddlewheel')   # Alex's photo: paddle-wheel log, thru-hull fitting
    arrow(d, (x0 + 360, y0 + 720), (x0 + 480, y0 + 620), ORANGE, 8, 30)
    tag(d, (x0 + 330, y0 + 760), 'אימפלר', ORANGE, 46)
    tag(d, ((x0 + x1) / 2, y1 - 70), 'מודד מהירות ביחס למים, לא ביחס לקרקע', ORANGE, 42)
    right_block(d, 'אימפלר', 'גלגל קטן עם להבים מתחת לגוף הסירה. המים מסובבים אותו, והמכשיר מתרגם את הסיבובים למהירות. הוא מודד ביחס למים. אם המים זזים, הוא לא יודע.')
    save(im, 's06_impeller_log')

def s07():
    im, d = base(); left_panel(d, 'מים מול קרקע')
    x0, y0, x1, y1 = inner(); top = (x0, y0, x1, y0 + 620)
    d = photo(im, top, 'u7_boat_aerial', rot=90, focus=(0.45, 0.5))
    arrow(d, (x0 + 40, y0 + 70), (x0 + 330, y0 + 70), WHITE, 9, 36); tag(d, (x0 + 360, y0 + 70), 'רוח מערבית 10 kn · באה ממערב', WHITE, 36, 'l')
    arrow(d, (x1 - 60, y0 + 560), (x1 - 360, y0 + 560), BLUE_L, 9, 36); tag(d, (x1 - 390, y0 + 560), 'זרם מערבי 2 kn · זורם למערב', BLUE_L, 36, 'r')
    tag(d, (x0 + 140, y0 + 310), '270°', ORANGE, 40)
    d = photo(im, (x0, y0 + 640, x1, y1), 'u7_helm_displays', focus=(0.6, 0.62))
    hy = y0 + 700
    tag(d, (x0 + 380, hy), 'LOG · ביחס למים', ORANGE, 36); tag(d, (x1 - 250, hy), 'GPS · ביחס לקרקע', GREEN_L, 36)
    tag(d, ((x0 + x1) / 2, y1 - 60), '8 + 2 = 10', TEXT, 64)
    right_block(d, 'מים מול קרקע', 'רוח נקראת לפי מאיפה היא באה, זרם לפי לאן הוא זורם.',
                ('שאלה מהמאגר · 48', 'שט בכוון 270°, רוח מערבית 10 קשרים, זרם מערבי 2 קשרים. מד המהירות מראה 8, ה-GPS מראה 10. מה הסיבה להבדל?',
                 ['מד המהירות ביחס למים, ה-GPS ביחס לקרקע', 'רוח נגדית מאטה, וב-GPS אי-דיוק של 2 קשר',
                  'גלגל הכנפיים צובר זיהום וצמחייה', 'תחתית הספינה גוררת שכבת מים ("גרר")'], 0))
    save(im, 's07_log_gps_q48')

def sailboat_top(im, bow, heading, L):
    """Paste the real sailboat from u7_boat_aerial (hull cut-out) with its bow at `bow`, pointing to `heading` (deg, clockwise from up)."""
    from PIL import ImageFilter
    g = Image.open(os.path.join(RL.A, 'u7_boat_aerial.jpg')).convert('RGB').crop((873, 400, 1193, 1285))
    s = L / g.height; g = g.resize((int(g.width * s), int(g.height * s)), Image.LANCZOS)
    m = Image.new('L', g.size, 0); ImageDraw.Draw(m).ellipse((2, -g.height * 0.05, g.width - 2, g.height * 1.02), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(3)); g.putalpha(m)
    r = g.rotate(-heading, resample=Image.BICUBIC, expand=True)
    c = (r.width / 2, r.height / 2); v = polar_pt((0, 0), g.height / 2 - 2, heading)
    im.paste(r, (int(bow[0] - c[0] - v[0]), int(bow[1] - c[1] - v[1])), r)

def wind_triangle(d, bow, heading, true_kn, boat_kn, k):
    """Green = true wind (from north), black = headwind (from ahead, = boat speed), red = apparent (sum). Tips meet at the bow."""
    tw = polar_pt((0, 0), true_kn * k, 0); hw = polar_pt((0, 0), boat_kn * k, heading)
    tt = (bow[0] + tw[0], bow[1] + tw[1]); ht = (bow[0] + hw[0], bow[1] + hw[1]); at = (tt[0] + hw[0], tt[1] + hw[1])
    d.line((tt, at), fill=(230, 230, 230), width=3); d.line((ht, at), fill=(230, 230, 230), width=3)
    d.line((ht, bow), fill=WHITE, width=14); arrow(d, ht, bow, (10, 10, 10), 9, 30)
    arrow(d, tt, bow, (40, 220, 60), 10, 32)
    arrow(d, at, bow, (230, 40, 50), 10, 32)

def s08():
    im, d = base(); left_panel(d, 'רוח מדומה = רוח אמיתית + רוח פנים')
    box = inner(); x0, y0, x1, y1 = box
    g = Image.open(os.path.join(RL.A, 'u7_boat_aerial.jpg')).convert('RGB').crop((0, 0, 700, 2048)).resize((x1 - x0, y1 - y0))
    im.paste(g, (x0, y0)); d = ImageDraw.Draw(im)
    H, k = 300, 32                                     # all boats head 300; true wind 7 kn from 000
    for bow, kn in (((x0 + 300, y0 + 380), 7), ((x0 + 620, y0 + 590), 4), ((x0 + 900, y0 + 790), 1)):
        sailboat_top(im, bow, H, 260); d = ImageDraw.Draw(im)
        wind_triangle(d, bow, H, 7, kn, k)
        sp = polar_pt(bow, 200, H + 180); tag(d, (sp[0] - 40, sp[1] + 90), f'הפלגה {kn} kn', WHITE, 34)
    lg = (x1 - 440, y0 + 20, x1 - 20, y0 + 230); d.rounded_rectangle(lg, 18, fill=WHITE)
    for i, (s, col) in enumerate([('ירוק: רוח אמיתית', (20, 150, 40)), ('שחור: רוח פנים', (10, 10, 10)), ('אדום: רוח מדומה', (210, 30, 40))]):
        label(d, (lg[2] - 30, lg[1] + 45 + i * 62), s, F(40), col, 'r')
    right_block(d, 'שלוש רוחות', 'רוח אמיתית: נושבת בטבע, קבועה ביחס לקרקע. רוח פנים: נוצרת מהתנועה, שווה למהירות הסירה ונושבת הפוך לה. רוח מדומה = רוח אמיתית + רוח פנים. זו הרוח שמרגישים על הסירה, ולפיה מכוונים את המפרשים.')
    save(im, 's08_wind_true_apparent')
def s09():
    im, d = base(); left_panel(d, 'הסירה עומדת: רוח אמיתית')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=WHITE)
    d = photo(im, (x0 + 470, y0, x1, y1), 'u7_moored_anemo', focus=(0.72, 0.5))   # cropped past the pole-mounted vane
    d = photo(im, (x0 + 15, y0 + 300, x0 + 455, y0 + 740), 'u7_wind_instr')       # Alex's photo: wind instrument
    for k in range(3): arrow(d, (x1 - 40, y0 + 120 + k * 80), (x1 - 330, y0 + 120 + k * 80), (0, 60, 150), 10, 32)
    tag(d, (x1 - 190, y0 + 50), 'רוח אמיתית', BLUE_L, 40)
    tag(d, (x0 + 235, y0 + 240), 'מד רוח', ORANGE, 40)
    tag(d, ((x0 + x1) / 2, y1 - 60), 'אין תנועה, אין רוח מהתנועה', ORANGE, 44)
    right_block(d, 'סירה עומדת', 'כשהסירה לא זזה, מד הרוח מראה את הרוח האמיתית.',
                ('שאלה מהמאגר · 11', 'איזה רוח מראה מד הרוח כאשר הספינה לא בתנועה?',
                 ['רוח אמיתית', 'רוח יחסית (מדומה)', 'רוח פנים', 'כל התשובות נכונות'], 0))
    save(im, 's09_wind_q11')

def s10():
    im, d = base(); left_panel(d, 'הסירה שטה: רוח יחסית')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, box, 'u7_cruise_anemo', focus=(0.55, 0.25))
    for k in range(3): arrow(d, (x1 - 40, y0 + 110 + k * 80), (x1 - 330, y0 + 150 + k * 80), ORANGE, 8, 30)
    tag(d, (x1 - 190, y0 + 50), 'רוח יחסית', ORANGE, 40)
    tag(d, ((x0 + x1) / 2, y1 - 60), 'התנועה מוסיפה רוח, המכשיר מודד את השילוב', ORANGE, 40)
    right_block(d, 'סירה בתנועה', 'בזמן הפלגה, מד הרוח מראה רוח יחסית.',
                ('שאלה מהמאגר · 25', 'מה מראה מד הרוח שבספינה בעת הפלגה?',
                 ['רוח אמיתית', 'רוח פנים', 'רוח יחסית (מדומה)', 'רוח גבית'], 2))
    save(im, 's10_wind_q25')

def s11():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u7_helm_displays', focus=(0.6, 0.55))
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['קשר = מייל ימי אחד בשעה', 'מטר לשנייה ≈ 2 קשרים', 'אורך ÷ זמן × 2 = קשרים', 'מד מהירות: ביחס למים',
             'GPS: ביחס לקרקע', 'ההבדל ביניהם: הזרם', 'סירה עומדת: רוח אמיתית', 'סירה בתנועה: רוח יחסית']
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 6 else ORANGE)
        text_r(d, 2380, y + 20, s, F(48, False), TEXT)
    save(im, 's11_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11]
sheet = lambda: U6.sheet.__globals__.__setitem__('C', C) or U6.sheet()

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only: fn()
    sheet()
