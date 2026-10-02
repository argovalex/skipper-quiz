"""Lesson 2 (l30): המפה הימית ומרקטור. Real imagery: NASA Blue Marble, NOAA chart, AI lamp-globe photo."""
import math, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
U1 = os.environ.get('U01', os.path.join(HERE, '..', 'l30u1', 'cards.py'))
spec = importlib.util.spec_from_file_location('u01', U1); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
from PIL import Image, ImageDraw
import real as RL
C.OUT = os.path.join(HERE, 'cards'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · המפה הימית'
F, text_c, text_r, label, dot, arrow, Globe = C.F, C.text_c, C.text_r, C.label, C.dot, C.arrow, C.Globe
base, left_panel, right_block, save, LP, RC = C.base, C.left_panel, C.right_block, C.save, C.LP, C.RC
TEXT, ORANGE, CORAL, GREEN, GREEN_L, BLUE_L, PANEL = C.TEXT, C.ORANGE, C.CORAL, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL
WHITE_T = (255, 255, 255)
A = RL.A

def panel_area(): return (LP[0], LP[1] + 300, LP[2], LP[3])

def fit_paste(im, src, box, pad=30):
    x0, y0, x1, y1 = box; w, h = x1 - x0 - 2 * pad, y1 - y0 - 2 * pad
    s = min(w / src.width, h / src.height); src = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    ox, oy = int(x0 + (x1 - x0 - src.width) / 2), int(y0 + (y1 - y0 - src.height) / 2)
    if src.mode == 'RGBA': im.paste(src, (ox, oy), src)
    else: im.paste(src, (ox, oy))
    return ox, oy, s

def merc_block(im, box, lon0, lon1, lat0, lat1, grid=None):
    """Real Mercator map (Blue Marble) filling box width; returns MercFrame in canvas coords."""
    x0, y0, x1, y1 = box; w = x1 - x0
    h = int(w * (RL.merc_y(lat1) - RL.merc_y(lat0)) / math.radians(lon1 - lon0))
    if h > y1 - y0:
        h = y1 - y0; w = int(h * math.radians(lon1 - lon0) / (RL.merc_y(lat1) - RL.merc_y(lat0)))
    ox, oy = int(x0 + (x1 - x0 - w) / 2), int(y0 + (y1 - y0 - h) / 2)
    im.paste(RL.mercator_img(w, h, lon0, lon1, lat0, lat1), (ox, oy))
    mf = RL.MercFrame((ox, oy, ox + w, oy + h), lon0, lon1, lat0, lat1)
    d = ImageDraw.Draw(im, 'RGBA')
    if grid:
        for la in range(-80, 90, grid):
            if lat0 <= la <= lat1:
                y = mf.pt(la, 0)[1]; d.line(((ox, y), (ox + w, y)), fill=(255, 255, 255, 150 if la else 230), width=3 if la else 5)
        for lo in range(-180, 181, grid):
            if lon0 <= lo <= lon1:
                x = mf.pt(0, lo)[0]; d.line(((x, oy), (x, oy + h)), fill=(255, 255, 255, 150), width=3)
    d.rectangle((ox, oy, ox + w, oy + h), outline=(230, 235, 245), width=4)
    return mf

def s01():
    im, d = base()
    merc_block(im, (110, 180, 1200, 1300), -180, 180, -70, 80, grid=30)
    d = ImageDraw.Draw(im)
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 2', F(56, False), BLUE_L)
    text_c(d, RC, 500, 'המפה הימית', F(150), TEXT)
    d.rounded_rectangle((RC - 80, 700, RC + 80, 714), 7, fill=GREEN)
    for i, s in enumerate(['היטל מרקטור ועיוותיו', 'Rhumb line ומעגל גדול', 'מייל ימי וקשר', 'הצפון האמיתי והכיוונים']):
        text_c(d, RC, 780 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    im, d = base(); left_panel(d, 'גלובוס, מנורה ודף עוטף')
    fit_paste(im, Image.open(os.path.join(A, 'lamp_b.png')).convert('RGB'), panel_area(), pad=20)
    d = ImageDraw.Draw(im)
    right_block(d, 'היטל מרקטור', 'מנורה במרכז הכדור מקרינה את קווי הרוחב והאורך על דף שעוטף אותו. פותחים את הדף ומקבלים מפה שטוחה.')
    save(im, 's02_projection')

def s03():
    im, d = base(); left_panel(d, 'מפת מרקטור אמיתית')
    ax0, ay0, ax1, ay1 = panel_area()
    mf = merc_block(im, (ax0 + 40, ay0 + 30, ax1 - 40, ay1 - 30), -80, 60, -40, 82, grid=20)
    d = ImageDraw.Draw(im)
    for la in (0, 30, 50, 65, 75):
        p = mf.pt(la, -40); r = 26 / math.cos(math.radians(la))
        d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), outline=ORANGE, width=6)
    text_c(d, RC, 150, C.SUB, F(48, False), BLUE_L)
    text_c(d, RC, 240, 'ארבעה חוקים', F(128), TEXT)
    d.rounded_rectangle((RC - 70, 410, RC + 70, 422), 6, fill=GREEN)
    rules = ['קווי הרוחב מקבילים', 'קווי האורך מקבילים', 'המרחק בין קווי האורך זהה', 'רוחב ניצב לאורך: רשת של מלבנים']
    for i, s in enumerate(rules):
        y = 470 + i * 104
        d.rounded_rectangle((1400, y, 2360, y + 86), 20, fill=PANEL)
        text_r(d, 2320, y + 18, f'{i + 1}.  ' + s, F(48, False), TEXT)
    y = 920
    d.rounded_rectangle((1400, y, 2360, y + 400), 24, fill=(60, 30, 36), outline=CORAL, width=3)
    text_r(d, 2320, y + 26, 'המחיר', F(46), CORAL)
    for i, s in enumerate(['קווי האורך לא מתכנסים לקטבים', 'המרחק בין קווי הרוחב גדל לכיוון הקטבים', 'עיגולים שווים בגודלם גדלים במפה']):
        text_r(d, 2320, y + 110 + i * 90, s, F(46, False), TEXT)
    save(im, 's03_mercator_grid')

def chart_panel(im, measure):
    """Paste NOAA chart with border into the left panel; draw dividers on the right latitude scale."""
    ax0, ay0, ax1, ay1 = panel_area()
    W = min(ax1 - ax0 - 60, ay1 - ay0 - 40)
    ch, pt = RL.chart_with_border(1300, border=90)
    lat_a, lat_b = measure
    xr = pt(lat_a, RL.CH_LON1)[0] + 8
    pa, pb = (xr, pt(lat_a, RL.CH_LON1)[1]), (xr, pt(lat_b, RL.CH_LON1)[1])
    ch = RL.draw_dividers(ch, pa, pb, leg=560, side=-1)
    s = W / ch.width; ch = ch.resize((W, W), Image.LANCZOS)
    ox, oy = int(ax0 + (ax1 - ax0 - W) / 2), int(ay0 + (ay1 - ay0 - W) / 2)
    im.paste(ch, (ox, oy))
    return lambda la, lo: (ox + pt(la, lo)[0] * s, oy + pt(la, lo)[1] * s), (ox + pa[0] * s, oy + pa[1] * s), (ox + pb[0] * s, oy + pb[1] * s)

def pill(d, p, s):
    f = F(44); w = d.textlength(C.he(s), font=f)
    d.rounded_rectangle((p[0] - w - 24, p[1] - 34, p[0] + 12, p[1] + 34), 18, fill=(20, 30, 50))
    label(d, p, s, f, ORANGE, 'r', -6)

def s04():
    im, d = base(); left_panel(d, 'מפה ימית: מחוגה על סרגל הרוחב')
    P, pa, pb = chart_panel(im, (41 + 10 / 60, 41 + 13 / 60))
    d = ImageDraw.Draw(im)
    pill(d, (pb[0] - 40, pb[1] - 60), '3 מייל ימי')
    right_block(d, 'מודדים בסרגל הרוחב', 'פותחים את המחוגה על המרחק במפה, ומעבירים אותה לסרגל קווי הרוחב בצד המפה, מול אזור השייט.',
                ('שאלה מהמאגר · 4', 'היכן יש למדוד מרחקים במפת מרקטור?',
                 ['יחידות של קווי רוחב בצד ימין או שמאל, מול אזור השייט', 'יחידות של קווי אורך בכל קצה שנבחר',
                  'ביחידה התקנית של מיל ימי שהיא 1.853 ק"מ', 'אורך הקשת של דקת רוחב על כל מעגל גדול'], 0))
    save(im, 's04_distortion')

def s05():
    im, d = base(); left_panel(d, 'קו ישר במפה, ספירלה על הכדור')
    ax0, ay0, ax1, ay1 = panel_area()
    mf = merc_block(im, (ax0 + 40, ay0 + 20, ax1 - 40, ay0 + 560), -100, 40, 0, 72, grid=20)
    d = ImageDraw.Draw(im)
    a, b = mf.pt(10, -85), mf.pt(64, 25)
    d.line((a, b), fill=ORANGE, width=8); dot(d, a, 12, CORAL, TEXT); dot(d, b, 12, CORAL, TEXT)
    R = 250; gx, gy = (ax0 + ax1) / 2, ay1 - R - 40
    gim = RL.globe_img(R, 35, -30); im.paste(gim, (int(gx - R), int(gy - R)), gim)
    d = ImageDraw.Draw(im)
    g = Globe(d, gx, gy, R, lat0=35, lon0=-30)
    pts = []
    k = math.tan(math.radians(40))  # rhumb at constant bearing ~50deg
    for i in range(0, 900):
        lon = -170 + i * 0.5
        lat = math.degrees(2 * math.atan(math.exp(math.radians(lon + 170) / k * 0.45 - 1.2)) - math.pi / 2)
        pts.append(g.pt(lat, lon))
    g.path(pts, ORANGE, 6)
    right_block(d, 'Rhumb line', 'קו ישר על מפת מרקטור. חוצה את כל קווי האורך באותה זווית, ולכן מפליגים לאורכו בכיוון קבוע.',
                ('שאלה מהמאגר · 149', 'מהו RHUMB LINE?',
                 ['הדרך הקצרה ביותר בין שתי נקודות על כדור הארץ', 'קו החוצה את קווי האורך באותה זווית במפה',
                  'קו ישר על מפת מרקטור', 'תשובות ב ו-ג נכונות'], 3))
    save(im, 's05_rhumb')

def s06():
    im, d = base(); left_panel(d, 'ניו יורק - גיברלטר על מפת מרקטור')
    ax0, ay0, ax1, ay1 = panel_area()
    mf = merc_block(im, (ax0 + 40, ay0 + 40, ax1 - 40, ay1 - 130), -85, 5, 20, 62, grid=10)
    d = ImageDraw.Draw(im)
    A_, B_ = (40.7, -74.0), (36.1, -5.4)
    pa, pb = mf.pt(*A_), mf.pt(*B_)
    for i in range(0, 60, 2):
        t0, t1 = i / 60, (i + 1) / 60
        d.line(((pa[0] + (pb[0] - pa[0]) * t0, pa[1] + (pb[1] - pa[1]) * t0), (pa[0] + (pb[0] - pa[0]) * t1, pa[1] + (pb[1] - pa[1]) * t1)), fill=WHITE_T, width=7)
    def v(la, lo):
        la, lo = math.radians(la), math.radians(lo); return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))
    p, q = v(*A_), v(*B_); om = math.acos(sum(i * j for i, j in zip(p, q))); pts = []
    for i in range(101):
        t = i / 100; k1 = math.sin((1 - t) * om) / math.sin(om); k2 = math.sin(t * om) / math.sin(om)
        x, y, z = (k1 * p[j] + k2 * q[j] for j in range(3))
        pts.append(mf.pt(math.degrees(math.asin(z)), math.degrees(math.atan2(y, x))))
    d.line(pts, fill=ORANGE, width=9, joint='curve')
    dot(d, pa, 16, CORAL, TEXT); dot(d, pb, 16, CORAL, TEXT)
    label(d, pa, 'ניו יורק', F(42), TEXT, 'l', 24, 40); label(d, pb, 'גיברלטר', F(42), TEXT, 'r', -24, 40)
    y = ay1 - 70
    d.line(((LP[0] + 120, y), (LP[0] + 200, y)), fill=ORANGE, width=9)
    label(d, (LP[0] + 220, y), 'מעגל גדול, קצר יותר', F(40, False), TEXT, 'l')
    for i in range(0, 80, 20): d.line(((LP[0] + 700 + i, y), (LP[0] + 712 + i, y)), fill=WHITE_T, width=6)
    label(d, (LP[0] + 800, y), 'קו ישר, ארוך יותר', F(40, False), TEXT, 'l')
    right_block(d, 'מה הקצר ביותר?', 'במפת מרקטור המעגל הגדול נראה כקשת לכיוון הקוטב, והקו הישר ארוך יותר. בהפלגה קצרה ההבדל זניח. בחציית אוקיינוס מתכננים על מעגל גדול.')
    save(im, 's06_gc_vs_rhumb')

def s07():
    im, d = base(); left_panel(d, 'דקת רוחב על קו אורך')
    ax0, ay0, ax1, ay1 = panel_area()
    R = 440; gx, gy = (ax0 + ax1) / 2, (ay0 + ay1) / 2 + 20
    gim = RL.globe_img(R, 20, -30); im.paste(gim, (int(gx - R), int(gy - R)), gim)
    d = ImageDraw.Draw(im)
    g = Globe(d, gx, gy, R, lat0=20, lon0=-30)
    g.parallel(0, ORANGE, 5); g.meridian(-30, WHITE_T, 5)
    g.path([g.pt(la / 4, -30) for la in range(28 * 4, 36 * 4 + 1)], CORAL, 16)
    p, _ = g.pt(36, -30); label(d, (p[0] + 30, p[1] - 30), 'דקה = מייל ימי', F(46), CORAL, 'l')
    q, _ = g.pt(-4, 10); label(d, q, 'קו המשווה', F(40), ORANGE)
    label(d, (gx, ay0 + 40), '40,000 ק"מ ÷ 360° ÷ 60\' ≈ 1,852 מ\'', F(44), TEXT)
    right_block(d, 'המייל הימי', 'דקת רוחב אחת, 1,852 מטר. קשר = מייל ימי בשעה.',
                ('שאלה מהמאגר · 7', 'מייל ימי שווה באורכו ל:',
                 ['דקה אחת על קו רוחב 45', '1650 מטרים', 'דקה על גבי מעגל גדול', "תשובות ב' ו-ג' נכונות"], 2))
    save(im, 's07_nautical_mile')

def s08():
    im, d = base(); left_panel(d, 'מחוגה על דקת רוחב אחת')
    P, pa, pb = chart_panel(im, (41 + 11 / 60, 41 + 12 / 60))
    d = ImageDraw.Draw(im)
    pill(d, (pb[0] - 40, pb[1] - 60), 'מייל ימי אחד')
    right_block(d, 'אורך המייל', 'מייל ימי אחד הוא דקת רוחב אחת: 1,852 מטר. מעלה שלמה היא 60 מייל.',
                ('שאלה מהמאגר · 16', 'מה אורכו של מיל ימי אחד?',
                 ['המרחק של מעלת רוחב הנמדדת על קו אורך', 'המרחק של מעלת אורך הנמדד על קו רוחב, פרט לקו המשווה',
                  '1852.5 מטרים', "תשובה א' ו-ג' נכונות"], 2))
    save(im, 's08_mile_length')

def s09():
    im, d = base(); left_panel(d, 'שושנת כיוונים על המפה')
    ax0, ay0, ax1, ay1 = panel_area()
    ch, _ = RL.chart_with_border(1300, border=90)
    W = min(ax1 - ax0 - 60, ay1 - ay0 - 40); ch = ch.resize((W, W), Image.LANCZOS)
    ox, oy = int(ax0 + (ax1 - ax0 - W) / 2), int(ay0 + (ay1 - ay0 - W) / 2); im.paste(ch, (ox, oy))
    d = ImageDraw.Draw(im, 'RGBA')
    cx, cy = ox + W / 2, oy + W / 2; R = W * 0.36
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(255, 255, 255, 170), outline=(150, 40, 110, 255), width=5)
    d.ellipse((cx - R * 0.82, cy - R * 0.82, cx + R * 0.82, cy + R * 0.82), outline=(150, 40, 110, 255), width=3)
    for a in range(0, 360, 5):
        L = 34 if a % 30 == 0 else (22 if a % 10 == 0 else 12); r = math.radians(a)
        d.line(((cx + (R - L) * math.sin(r), cy - (R - L) * math.cos(r)), (cx + R * math.sin(r), cy - R * math.cos(r))), fill=(150, 40, 110, 255), width=3)
    for a, s in ((0, '000'), (90, '090'), (180, '180'), (270, '270')):
        r = math.radians(a); label(d, (cx + (R - 80) * math.sin(r), cy - (R - 70) * math.cos(r)), s, F(42), (120, 20, 90))
    d.polygon([(cx, cy - R * 0.8), (cx - 22, cy - R * 0.55), (cx + 22, cy - R * 0.55)], fill=(150, 40, 110, 255))
    arrow(d, (cx, cy), (cx, cy - R * 0.55), CORAL, 10, 36)
    arrow(d, (cx, cy), (cx - R * 0.55, cy), ORANGE, 10, 36)
    d.arc((cx - 130, cy - 130, cx + 130, cy + 130), 180, 270, fill=ORANGE, width=7)
    right_block(d, 'הצפון האמיתי', 'הכיוון לקוטב הצפוני הגיאוגרפי. כיוונים נמדדים בשלוש ספרות, בכיוון השעון.',
                ('שאלה מהמאגר · 192', 'תו הכיוון במצפן מול הצפון. מסובבים את המצפן 90° שמאלה. לאן יצביע תו הכיוון?',
                 ['מערבה', 'צפונה', 'מזרחה', 'דרומה'], 0))
    save(im, 's09_true_north')

def s10():
    im, d = base()
    merc_block(im, (110, 250, 1150, 1250), -100, 30, 0, 72, grid=20)
    d = ImageDraw.Draw(im)
    text_c(d, 1780, 180, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1710, 340, 1850, 352), 6, fill=GREEN)
    items = ['מרקטור: רשת ישרה של מלבנים', 'מתיחה לכיוון הקטבים', 'מודדים מרחק בסרגל הרוחב, במחוגה', 'Rhumb line: קו ישר, זווית קבועה',
             'מעגל גדול: הדרך הקצרה ביותר', 'מייל ימי = דקת רוחב = 1,852 מטר', 'קשר = מייל ימי בשעה', 'כיוונים מהצפון האמיתי, עם השעון']
    for i, s in enumerate(items):
        y = 410 + i * 108
        d.rounded_rectangle((1220, y, 2400, y + 88), 20, fill=PANEL)
        dot(d, (2360, y + 44), 12, GREEN_L)
        text_r(d, 2320, y + 18, s, F(50, False), TEXT)
    save(im, 's10_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10]
if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only: fn()
