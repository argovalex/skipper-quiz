"""Lesson 3 (l30): אזורי זמן. Real imagery: NASA Blue Marble (sun-lit globe, world map), AI photo of Greenwich."""
import math, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
spec = importlib.util.spec_from_file_location('u01', os.path.join(HERE, 'u01_cards.py')); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
import numpy as np
from PIL import Image, ImageDraw
import real as RL
C.OUT = os.path.join(HERE, '..', 'cards', 'אזורי זמן'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · אזורי זמן'
F, text_c, text_r, label, dot, arrow, Globe = C.F, C.text_c, C.text_r, C.label, C.dot, C.arrow, C.Globe
base, left_panel, right_block, save, LP, RC = C.base, C.left_panel, C.right_block, C.save, C.LP, C.RC
TEXT, ORANGE, CORAL, GREEN, GREEN_L, BLUE_L, PANEL, MUTED = C.TEXT, C.ORANGE, C.CORAL, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL, C.MUTED
WHITE = (255, 255, 255)

def panel_area(): return (LP[0], LP[1] + 300, LP[2], LP[3])

def equirect(w, h, lon0, lon1, lat0, lat1, dim=1.0):
    tex = RL.bm(); H, W, _ = tex.shape
    lats = lat1 - (np.arange(h) + 0.5) / h * (lat1 - lat0); lons = lon0 + (np.arange(w) + 0.5) / w * (lon1 - lon0)
    v = ((90 - lats) / 180 * (H - 1)).astype(int); u = (((lons + 180) % 360) / 360 * (W - 1)).astype(int)
    a = tex[v[:, None], u[None, :]].astype(np.float64) * dim
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGB')

class Eq:
    def __init__(s, box, lon0, lon1, lat0, lat1): s.box, s.lon0, s.lon1, s.lat0, s.lat1 = box, lon0, lon1, lat0, lat1
    def pt(s, lat, lon):
        x0, y0, x1, y1 = s.box
        return (x0 + (lon - s.lon0) / (s.lon1 - s.lon0) * (x1 - x0), y0 + (s.lat1 - lat) / (s.lat1 - s.lat0) * (y1 - y0))

def zone_map(im, box, lon0=-180, lon1=180, lat0=-60, lat1=75, labels=True, hi=None, dim=0.9):
    """Blue Marble equirect map with nominal 15-degree time zones; hi = zone number to highlight."""
    x0, y0, x1, y1 = box
    im.paste(equirect(x1 - x0, y1 - y0, lon0, lon1, lat0, lat1, dim), (x0, y0))
    e = Eq(box, lon0, lon1, lat0, lat1)
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for z in range(-12, 13):
        a, b = max(z * 15 - 7.5, lon0), min(z * 15 + 7.5, lon1)
        if b <= a: continue
        xa, xb = e.pt(0, a)[0], e.pt(0, b)[0]
        if z == hi: d.rectangle((xa, y0, xb, y1), fill=(220, 160, 60, 110))
        elif z % 2: d.rectangle((xa, y0, xb, y1), fill=(0, 0, 0, 70))
        d.line(((xa, y0), (xa, y1)), fill=(255, 255, 255, 110), width=2)
    base_ = im.convert('RGBA'); base_.alpha_composite(ov); im.paste(base_.convert('RGB'))
    d = ImageDraw.Draw(im)
    if labels:
        for z in range(-12, 13):
            c = z * 15
            if (lon1 - lon0) > 180 and z % 3: continue
            if lon0 + 3 < c < lon1 - 3 or (z in (-12, 12) and lon0 <= c <= lon1):
                s = ('+' if z > 0 else '') + str(z)
                p = e.pt(lat1, min(max(c, lon0 + 4), lon1 - 4))
                label(d, (p[0], y0 - 30), s, F(30), ORANGE if z == hi else TEXT)
    d.rectangle(box, outline=(230, 235, 245), width=4)
    return e

def sunglobe(im, c, R, lat0, lon0, sun_lon):
    g = RL.globe_img(R, lat0, lon0, sun=(0, sun_lon)); im.paste(g, (int(c[0] - R), int(c[1] - R)), g)
    return Globe(ImageDraw.Draw(im), c[0], c[1], R, lat0=lat0, lon0=lon0)

def clock(d, c, r, hh, mm, title, sub):
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=(245, 247, 250), outline=(40, 50, 70), width=8)
    for i in range(12):
        a = math.radians(i * 30); L = 26 if i % 3 == 0 else 14
        d.line(((c[0] + (r - L - 10) * math.sin(a), c[1] - (r - L - 10) * math.cos(a)), (c[0] + (r - 10) * math.sin(a), c[1] - (r - 10) * math.cos(a))), fill=(40, 50, 70), width=6)
    ah = math.radians((hh % 12 + mm / 60) * 30); am = math.radians(mm * 6)
    d.line((c, (c[0] + r * 0.5 * math.sin(ah), c[1] - r * 0.5 * math.cos(ah))), fill=(30, 35, 45), width=14)
    d.line((c, (c[0] + r * 0.78 * math.sin(am), c[1] - r * 0.78 * math.cos(am))), fill=(30, 35, 45), width=8)
    dot(d, c, 12, (200, 60, 60))
    label(d, (c[0], c[1] + r + 50), title, F(46), TEXT)
    label(d, (c[0], c[1] + r + 110), sub, F(40, False), ORANGE)

def world_box(): ax0, ay0, ax1, ay1 = panel_area(); return (ax0 + 30, ay0 + 120, ax1 - 30, ay0 + 120 + int((ax1 - ax0 - 60) * 135 / 360))

# ---------- cards ----------
def s01():
    im, d = base()
    zone_map(im, (80, 420, 1240, 420 + int(1160 * 135 / 360)))
    d = ImageDraw.Draw(im)
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 3', F(56, False), BLUE_L)
    text_c(d, RC, 500, 'אזורי זמן', F(150), TEXT)
    d.rounded_rectangle((RC - 80, 700, RC + 80, 714), 7, fill=GREEN)
    for i, s in enumerate(['UTC וגריניץ\'', '24 אזורי זמן', 'זמן מקומי מול זמן אזורי', 'קו התאריך וחישובים']):
        text_c(d, RC, 780 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    im, d = base(); left_panel(d, 'כדור הארץ מסתובב מזרחה')
    ax0, ay0, ax1, ay1 = panel_area(); c = ((ax0 + ax1) / 2, (ay0 + ay1) / 2 + 20); R = 430
    g = sunglobe(im, c, R, 15, 20, 35)
    d = ImageDraw.Draw(im); g.d = d
    for lo in range(-60, 91, 15): g.meridian(lo, (255, 255, 255), 2)
    pts = [g.pt(-38, lo)[0] for lo in range(-20, 61, 3)]
    d.line(pts, fill=GREEN_L, width=10); arrow(d, pts[-3], pts[-1], GREEN_L, 10, 44)
    label(d, (pts[-1][0] + 20, pts[-1][1] + 10), 'מזרח', F(44), GREEN_L, 'l')
    a, _ = g.pt(8, 20); b, _ = g.pt(8, 35)
    d.line((a, b), fill=ORANGE, width=8); label(d, ((a[0] + b[0]) / 2, a[1] - 40), '15° = שעה', F(44), ORANGE)
    right_block(d, '15 מעלות בשעה', 'סיבוב שלם של 360° ב-24 שעות. 360 חלקי 24 = 15° בכל שעה.')
    save(im, 's02_rotation')

def fit_photo(im, path, box, pad=20):
    src = Image.open(path).convert('RGB'); x0, y0, x1, y1 = box
    s = min((x1 - x0 - 2 * pad) / src.width, (y1 - y0 - 2 * pad) / src.height)
    src = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    im.paste(src, (int(x0 + (x1 - x0 - src.width) / 2), int(y0 + (y1 - y0 - src.height) / 2)))

def s03():
    im, d = base(); left_panel(d, 'קו האורך אפס, גריניץ\'')
    fit_photo(im, os.path.join(RL.A, 'greenwich.png'), panel_area())
    d = ImageDraw.Draw(im)
    right_block(d, 'UTC', 'זמן אוניברסלי מתואם, נמדד על קו האורך אפס בגריניץ\'. בעבר: GMT.',
                ('שאלה מהמאגר · 139', 'הגדרת המושג U.T.C. היא:',
                 ['צהרה עליונה לפי זמן מתואם', 'זמן אוניברסלי על פי הכוכב CANOPUS',
                  'זמן אוניברסלי מתואם השווה לזמן הממוצע בגריניץ\'', 'זמן ממוצע של אזור הקרוב לקו אורך גריניץ\''], 2))
    save(im, 's03_utc')

def s04():
    im, d = base(); left_panel(d, '24 אזורי זמן, 15° כל אחד')
    ax0, ay0, ax1, ay1 = panel_area()
    e = zone_map(im, (ax0 + 30, ay0 + 80, ax1 - 30, ay1 - 260), lon0=-60, lon1=60, lat0=-40, lat1=65, hi=0)
    d = ImageDraw.Draw(im)
    xa, xb, xc = e.pt(0, -7.5)[0], e.pt(0, 7.5)[0], e.pt(0, 0)[0]
    y = ay1 - 200
    arrow(d, (xc, y), (xa, y), ORANGE, 6, 24); arrow(d, (xc, y), (xb, y), ORANGE, 6, 24)
    label(d, (xc, y + 60), '7.5° מערב · 7.5° מזרח', F(42), ORANGE)
    label(d, (xc, y + 120), 'מזרחה: מאוחר יותר · מערבה: מוקדם יותר', F(40, False), TEXT)
    right_block(d, 'אזור זמן', 'רצועה של 15° סביב קו אורך מרכזי. אזור אפס סביב גריניץ\'.',
                ('שאלה מהמאגר · 15', 'מה מציין "זמן אזורי" (ZONE TIME)?',
                 ['הזמן האחיד שמקיימים 7.5 מעלות מצד מערב של מעלת אורך שלמה', 'הזמן שבוחרת כל מדינה לפי עונות השנה',
                  'הזמן האחיד בתחום של 15°, 7.5° מזרחה ו-7.5° מערבה מקו אורך מרכזי', 'זמן הצהריים בכל מקום ביחס לצהריים בקו גריניץ\''], 2))
    save(im, 's04_zones')

def s05():
    im, d = base(); left_panel(d, 'כל השעונים באזור מראים אותה שעה')
    ax0, ay0, ax1, ay1 = panel_area()
    e = zone_map(im, (ax0 + 30, ay0 + 80, ax1 - 30, ay1 - 40), lon0=5, lon1=55, lat0=10, lat1=50, hi=2)
    d = ImageDraw.Draw(im)
    for name, la, lo in (('ישראל', 32.0, 34.8), ('קפריסין', 35.1, 33.4), ('יוון', 38.0, 23.7)):
        p = e.pt(la, lo); dot(d, p, 12, CORAL, WHITE)
    p = e.pt(32.0, 34.8); label(d, p, 'ישראל', F(40), WHITE, 'r', -24)
    label(d, e.pt(46, 30), 'אזור +2', F(48), ORANGE)
    right_block(d, 'זמן אזורי', 'השעה האחידה של כל אזור הזמן, בלי קשר למקום המדויק בתוכו.',
                ('שאלה מהמאגר · 138', 'הגדרת המושג זמן אזורי (ZT) היא:',
                 ['הזמן באזור שנקבע על פי רוחב הצופה', 'הזמן באזור שנקבע על פי אורך הצופה',
                  'הזמן באזור שנקבע לפי אזור הזמן', 'הזמן באזור שנקבע על פי מהלך השמש'], 2))
    save(im, 's05_zone_time')

def s06():
    im, d = base(); left_panel(d, 'זמן מקומי לפי קו האורך')
    ax0, ay0, ax1, ay1 = panel_area(); c = ((ax0 + ax1) / 2, (ay0 + ay1) / 2 + 40); R = 430
    g = sunglobe(im, c, R, 20, 35, 35)
    d = ImageDraw.Draw(im); g.d = d
    for lo, t, col in ((20, '11:00', BLUE_L), (35, '12:00', ORANGE), (50, '13:00', BLUE_L)):
        g.meridian(lo, col, 6 if lo == 35 else 4)
        p, _ = g.pt(52, lo); label(d, p, t, F(44), col, dy=-40)
    s_, _ = g.pt(0, 35); label(d, (s_[0], s_[1] + 60), 'השמש מעל', F(40), ORANGE)
    right_block(d, 'זמן מקומי', 'נקבע לפי קו האורך המדויק של כלי השיט. כל 15° מזרחה = שעה מאוחר יותר.',
                ('שאלה מהמאגר · 9', 'כיצד מחושב הזמן המקומי (LOCAL TIME)?',
                 ['על פי קו האורך הנוכחי של כלי השיט, מזרחה או מערבה לגריניץ\'', 'הממוצע של קווי האורך בכל מדינה',
                  'המרכז של כל אזור זמן', 'זמן הזריחה במקום בו נמצא המודד'], 0))
    save(im, 's06_local_time')

def s07():
    im, d = base(); left_panel(d, 'בתוך אזור +2: מקומי מול אזורי')
    ax0, ay0, ax1, ay1 = panel_area()
    e = zone_map(im, (ax0 + 30, ay0 + 80, ax1 - 30, ay1 - 220), lon0=15, lon1=45, lat0=20, lat1=45, hi=2, labels=False)
    d = ImageDraw.Draw(im)
    for lo, t in ((23.5, '11:34'), (30, '12:00'), (36.5, '12:26')):
        x = e.pt(0, lo)[0]; d.line(((x, ay0 + 80), (x, ay1 - 220)), fill=WHITE, width=4)
        label(d, (x, ay0 + 40), t, F(40), WHITE)
    y = ay1 - 150
    label(d, ((ax0 + ax1) / 2, y), 'זמן מקומי: משתנה עם קו האורך', F(42), TEXT)
    label(d, ((ax0 + ax1) / 2, y + 70), 'זמן אזורי: 12:00 בכל הרצועה', F(42), ORANGE)
    right_block(d, 'זמן מקומי ממוצע', 'LOCAL MEAN TIME: הזמן לפי קו האורך של הצופה.',
                ('שאלה מהמאגר · 140', 'מהו LOCAL MEAN TIME?',
                 ['הזמן באזור על פי שעון אטומי', 'הזמן באזור על פי הרוחב הממוצע (MEAN LATITUDE)',
                  'הזמן באזור על פי אזור הזמן', 'הזמן באזור על פי קו האורך שבו נמצא הצופה'], 3))
    save(im, 's07_lmt')

def s08():
    im, d = base(); left_panel(d, 'UTC+3: שלוש שעות מזרחה')
    ax0, ay0, ax1, ay1 = panel_area()
    e = zone_map(im, (ax0 + 30, ay0 + 60, ax1 - 30, ay0 + 480), lon0=-30, lon1=60, lat0=15, lat1=62, hi=3, dim=0.75)
    d = ImageDraw.Draw(im)
    g0, il = e.pt(51.5, 0), e.pt(32, 35)
    dot(d, g0, 12, CORAL, WHITE); dot(d, il, 12, CORAL, WHITE)
    arrow(d, (g0[0] + 20, g0[1] + 10), (il[0] - 20, il[1] - 10), ORANGE, 6, 26)
    clock(d, (ax0 + 300, ay1 - 330), 150, 6, 0, 'גריניץ\' · UTC', '06:00')
    clock(d, (ax1 - 300, ay1 - 330), 150, 9, 0, 'ישראל · UTC+3', '09:00')
    right_block(d, 'UTC+3', 'פלוס = מזרחה לגריניץ\'. השעה אצלנו מאוחרת בשלוש שעות. ישראל: +2 בחורף, +3 בקיץ.',
                ('שאלה מהמאגר · 22', 'למה הכוונה כאשר אומרים שהזמן האזורי הוא UTC+3?',
                 ['שאתה נמצא מזרחה לאזור זמן 0', 'שאם בגריניץ\' 0600, באזורך השעה 0900',
                  'שאצלך השעה מאוחרת בשלוש שעות מ-U.T.C', 'כל התשובות נכונות'], 3))
    save(im, 's08_utc_plus3')

def s09():
    im, d = base(); left_panel(d, 'קו התאריך הבינלאומי, 180°')
    ax0, ay0, ax1, ay1 = panel_area(); c = ((ax0 + ax1) / 2, (ay0 + ay1) / 2 + 20); R = 430
    g = sunglobe(im, c, R, 12, 180, 150)
    d = ImageDraw.Draw(im); g.d = d
    g.meridian(180, (230, 60, 60), 8)
    pw, _ = g.pt(-5, 179.5); pe, _ = g.pt(-5, -179.5)
    label(d, (c[0] - 40, c[1] - 120), '+12', F(56), ORANGE, 'r'); label(d, (c[0] - 40, c[1] - 50), '31 בדצמבר', F(40), TEXT, 'r')
    label(d, (c[0] + 40, c[1] - 120), '-12', F(56), BLUE_L, 'l'); label(d, (c[0] + 40, c[1] - 50), '30 בדצמבר', F(40), TEXT, 'l')
    label(d, (c[0], c[1] + R + 60), 'אותה שעה, תאריך שונה ביום', F(42), TEXT)
    right_block(d, 'קו התאריך', 'ממזרח למערב: מורידים יום. ממערב למזרח: מוסיפים יום. השעה לא משתנה.',
                ('שאלה מהמאגר · 21', '31 בדצמבר, 179°31\'E, השעה 23:59, מה השעה והתאריך ב-179°31\'W?',
                 ['30 בדצמבר, 22:59', '30 בדצמבר, 23:59', '1 בינואר בשנה הבאה, 23:59', 'אותה שעה, אותו תאריך'], 1))
    save(im, 's09_date_line')

def steps_card(d, x_r, y, rows, w=1060):
    for i, (t, col) in enumerate(rows):
        yy = y + i * 118
        d.rounded_rectangle((x_r - w, yy, x_r, yy + 96), 22, fill=PANEL, outline=col, width=3)
        text_r(d, x_r - 36, yy + 22, t, F(46, False), TEXT)

def steps3(d, x_r, y, steps, w=1100):
    """steps = [(header, color, [rows])]: numbered step header + its calculation rows."""
    for n, (hd, col, rows) in enumerate(steps, 1):
        d.rounded_rectangle((x_r - w, y, x_r, y + 66), 18, fill=col)
        text_r(d, x_r - 30, y + 10, f'שלב {n}: {hd}', F(44), C.NAVY2)
        y += 82
        for t in rows:
            d.rounded_rectangle((x_r - w + 40, y, x_r, y + 80), 18, fill=PANEL, outline=col, width=3)
            text_r(d, x_r - 30, y + 16, t, F(44, False), TEXT)
            y += 94
        y += 14

def s10():
    im, d = base(); left_panel(d, 'שלושה שלבים לכל שאלת חישוב')
    ax0, ay0, ax1, ay1 = panel_area()
    steps3(d, ax1 - 40, ay0 + 10, [
        ('אזור הזמן (ZD)', ORANGE, ['דקות ÷ 60 → קו אורך עשרוני', 'קו אורך ÷ 15', 'מעגלים לשלם הקרוב (חצי = 7.5°)', 'מזרח: פלוס · מערב: מינוס']),
        ('השעה', BLUE_L, ['גריניץ\' = שעה אזורית − ZD', 'שעה אזורית = גריניץ\' + ZD']),
        ('התאריך', GREEN_L, ['עברנו חצות קדימה: מוסיפים יום', 'עברנו חצות אחורה: מורידים יום']),
    ])
    right_block(d, 'שלושה שלבים', '1. אזור הזמן: ממירים לעשרוני, מחלקים ב-15 ומעגלים. 2. השעה: מוסיפים או מחסירים את אזור הזמן. 3. התאריך: בודקים אם עברנו חצות.')
    save(im, 's10_method')

def s11():
    im, d = base(); left_panel(d, 'פתרון: 154°39\'E, השעה 10:42')
    ax0, ay0, ax1, ay1 = panel_area()
    steps3(d, ax1 - 40, ay0 + 10, [
        ('אזור הזמן (ZD)', ORANGE, ['154°39\' = 154 + 39/60 = 154.65°', '154.65 ÷ 15 = 10.31', '0.31 < 0.5 → מעגלים ל-10', 'מזרח → ZD = +10']),
        ('השעה בגריניץ\'', BLUE_L, ['גריניץ\' = שעה אזורית − ZD', '10:42 − 10 = 00:42']),
        ('התאריך', GREEN_L, ['לא עברנו חצות אחורה → 24.06.11']),
    ])
    right_block(d, 'שאלת חישוב', '',
                ('שאלה מהמאגר · 108', 'תאריך 24.06.11, השעה האזורית 10:42, קו האורך 154°39\'E. מה השעה והתאריך בגריניץ\'?',
                 ['השעה תהיה 23:42 בתאריך 24.06.11', '21:42 בתאריך 24.06.11', '00:42 בתאריך 24.06.11', '23:42 בתאריך 24.06.11'], 2))
    save(im, 's11_q108')

def s12():
    im, d = base(); left_panel(d, 'פתרון: 157°42\'E, 17:53 UTC')
    ax0, ay0, ax1, ay1 = panel_area()
    steps3(d, ax1 - 40, ay0 + 10, [
        ('אזור הזמן (ZD)', ORANGE, ['157°42\' = 157 + 42/60 = 157.7°', '157.7 ÷ 15 = 10.51', '0.51 > 0.5 → מעגלים ל-11', 'מזרח → ZD = +11']),
        ('השעה האזורית', BLUE_L, ['שעה אזורית = UTC + ZD', '17:53 + 11 = 28:53']),
        ('התאריך', GREEN_L, ['28:53 − 24 = 04:53, יום למחרת']),
    ])
    right_block(d, 'שאלת חישוב', 'קו הרוחב לא משפיע על השעה.',
                ('שאלה מהמאגר · 133', 'מקומך 32°17\'N 157°42\'E, השעה 17:53 U.T.C. מה השעה האזורית?',
                 ['15:53', '04:53', '00:53', '18:00'], 1))
    save(im, 's12_q133')

def s13():
    im, d = base()
    zone_map(im, (80, 420, 1240, 420 + int(1160 * 135 / 360)))
    d = ImageDraw.Draw(im)
    text_c(d, 1780, 180, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1710, 340, 1850, 352), 6, fill=GREEN)
    items = ['15° אורך = שעה אחת', 'UTC: הזמן בגריניץ\'', '24 אזורים, 7.5° לכל צד', 'זמן מקומי: לפי קו האורך',
             'זמן אזורי: לפי אזור הזמן', 'מזרחה מאוחר, מערבה מוקדם', 'קו התאריך: אותה שעה, יום שונה', 'ZD: אורך עשרוני ÷ 15, מעגלים']
    for i, s in enumerate(items):
        y = 410 + i * 108
        d.rounded_rectangle((1220, y, 2400, y + 88), 20, fill=PANEL)
        dot(d, (2360, y + 44), 12, GREEN_L)
        text_r(d, 2320, y + 18, s, F(50, False), TEXT)
    save(im, 's13_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13]
if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only: fn()
