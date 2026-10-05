"""Lesson 6 (l30): מצפן ג'יירו ושער שטף. Drawn Fluxgate sensor + display, Alex's gyro cutaway (assets/gyro_compass.jpg)."""
import math, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U4 = _load('u04', 'u04_cards.py'); U5 = _load('u05', 'u05_cards.py')
from PIL import Image, ImageDraw
import real as RL
C.OUT = os.path.join(HERE, '..', 'cards', "מצפן ג'יירו ושער שטף"); os.makedirs(C.OUT, exist_ok=True)
C.SUB = "ניווט חופי ומכשירים · מצפן ג'יירו ושער שטף"
F, text_c, text_r, label, dot, arrow = C.F, C.text_c, C.text_r, C.label, C.dot, C.arrow
base, left_panel, right_block, save, LP, RC = C.base, C.left_panel, C.right_block, C.save, C.LP, C.RC
TEXT, ORANGE, CORAL, GREEN, GREEN_L, BLUE_L, PANEL, MUTED = C.TEXT, C.ORANGE, C.CORAL, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL, C.MUTED
dashed, arc = U4.dashed, U4.arc
compass, boat, sea, readout, polar_pt, inner = U5.compass, U5.boat, U5.sea, U5.readout, U5.polar_pt, U5.inner
WHITE, RED, DARK = U5.WHITE, U5.RED, U5.DARK
COPPER = (205, 120, 60); STEEL = (150, 156, 168)

# ---------- Fluxgate drawings ----------
def sensor(d, c, R, cut=True):
    """Fluxgate sensor unit seen from above: round housing, ring core with tiny coils (electromagnets)."""
    d.ellipse((c[0] - R, c[1] - R, c[0] + R, c[1] + R), fill=(40, 44, 52), outline=STEEL, width=6)
    if not cut:
        return
    rc = R * 0.62
    d.ellipse((c[0] - rc, c[1] - rc, c[0] + rc, c[1] + rc), outline=(200, 200, 210), width=max(8, int(R * 0.09)))
    for a in range(0, 360, 90):                         # four coil packs around the core
        for k in range(-3, 4):
            p = polar_pt(c, rc, a + k * 6)
            r = R * 0.11
            d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), outline=COPPER, width=max(3, int(R * 0.025)))
    dot(d, c, R * 0.06, STEEL)

def screen(d, box, hdg='045°', tag='HDG · M'):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 24, fill=(30, 32, 38), outline=STEEL, width=5)
    d.rounded_rectangle((x0 + 22, y0 + 22, x1 - 22, y1 - 22), 14, fill=(8, 14, 22))
    cx = (x0 + x1) / 2
    label(d, (cx, y0 + 70), tag, F(34, False), MUTED)
    label(d, (cx, (y0 + y1) / 2 + 20), hdg, F(int((y1 - y0) * 0.3)), GREEN_L)

def cable(d, pts, col=(70, 70, 76)):
    d.line(pts, fill=col, width=9, joint='curve')

def tile(d, box, title, sub, col, mark=None):
    d.rounded_rectangle(box, 22, fill=PANEL, outline=col, width=4)
    x0, y0, x1, y1 = box
    if mark:
        label(d, (x1 - 50, (y0 + y1) / 2), mark, F(64), col)
        text_r(d, x1 - 100, y0 + 24, title, F(44), TEXT)
        if sub: text_r(d, x1 - 100, y0 + 84, sub, F(34, False), MUTED)
    else:
        text_r(d, x1 - 36, y0 + 24, title, F(44), TEXT)
        if sub: text_r(d, x1 - 36, y0 + 84, sub, F(34, False), MUTED)

def bolt(d, c, s, col=(250, 210, 70)):
    pts = [(0, -1), (-0.45, 0.1), (-0.05, 0.1), (-0.25, 1), (0.45, -0.15), (0.05, -0.15), (0.25, -1)]
    d.polygon([(c[0] + x * s, c[1] + y * s) for x, y in pts], fill=col)

def clock(d, c, r, col=WHITE):
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), outline=col, width=8)
    d.line((c, polar_pt(c, r * 0.65, 0)), fill=col, width=8); d.line((c, polar_pt(c, r * 0.5, 120)), fill=col, width=8)

def gyro_img(im, box):
    g = Image.open(os.path.join(RL.A, 'gyro_compass.jpg')).convert('RGB')
    x0, y0, x1, y1 = box; s = min((x1 - x0) / g.width, (y1 - y0) / g.height)
    g = g.resize((int(g.width * s), int(g.height * s)), Image.LANCZOS)
    im.paste(g, (int((x0 + x1 - g.width) / 2), int((y0 + y1 - g.height) / 2)))

# ---------- cards ----------
def s01():
    im, d = base()
    sea(im, (0, 0, 1300, 1440))
    d = ImageDraw.Draw(im)
    sensor(d, (330, 720), 230)
    gyro_img(im, (660, 240, 1240, 1200)); d = ImageDraw.Draw(im)
    label(d, (330, 1010), 'Fluxgate', F(52), WHITE); label(d, (950, 1250), 'Gyro', F(52), WHITE)
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 6', F(56, False), BLUE_L)
    text_c(d, RC, 520, "מצפן ג'יירו ושער שטף", F(130), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['מצפן שער שטף, Fluxgate', 'יתרונות וחסרונות', "מצפן ג'יירו", 'מי מראה את הכיוון האמיתי']):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    im, d = base(); left_panel(d, 'מצפן שער שטף: חיישן + מסך')
    x0, y0, x1, y1 = inner(); d.rectangle((x0, y0, x1, y1), fill=(20, 32, 50))
    sc = (x1 - 330, y0 + 420); sensor(d, sc, 250)
    sb = (x0 + 70, y0 + 230, x0 + 470, y0 + 560); screen(d, sb)
    cable(d, [(sc[0] - 250, sc[1]), ((sb[0] + sb[2]) / 2 + 120, sc[1]), ((sb[0] + sb[2]) / 2 + 120, sb[3])])
    def call(p, q, title, en, col, side):
        d.line((p, q), fill=col, width=3); dot(d, p, 8, col)
        dx = 14 if side == 'l' else -14
        label(d, (q[0] + dx, q[1] - 18), title, F(42), col, side); label(d, (q[0] + dx, q[1] + 26), en, F(30, False), MUTED, side)
    call(polar_pt(sc, 250 * 0.62, 90), (x1 - 40, sc[1] + 330), 'אלקטרו-מגנטים זעירים', 'במקום מחט', COPPER, 'r')
    call(polar_pt(sc, 250, 20), (x1 - 40, y0 + 60), 'יחידת חיישן', 'Sensor · המצפן עצמו', BLUE_L, 'r')
    call(((sb[0] + sb[2]) / 2, sb[1]), (sb[0] + 10, y0 + 60), 'מסך תצוגה', 'Display', GREEN_L, 'l')
    yy = y1 - 200
    for i, s in enumerate(['חש את השדה המגנטי של כדור הארץ', 'מצפן מגנטי לכל דבר: וריאציה ודויאציה']):
        label(d, ((x0 + x1) / 2, yy + i * 70), s, F(42, i == 1), ORANGE if i else TEXT)
    right_block(d, 'מצפן שער שטף', 'מצפן מגנטי לכל דבר. במקום מחט או מוטות מגנטיים יש בו אלקטרו-מגנטים זעירים, שחשים כל שינוי בשדה המגנטי.')
    save(im, 's02_fluxgate_how')

def s03():
    im, d = base(); left_panel(d, 'החיישן חש את קווי השדה המגנטי')
    x0, y0, x1, y1 = inner(); d.rectangle((x0, y0, x1, y1), fill=(20, 32, 50))
    c = ((x0 + x1) / 2, (y0 + y1) / 2 + 20)
    for k in range(-4, 5):                                  # earth's field lines, south -> north
        x = c[0] + k * 120
        pts = [(x + 30 * math.sin((y - y0) / 160), y) for y in range(y0 + 40, y1 - 40, 8)]
        d.line(pts, fill=(80, 130, 190), width=3); arrow(d, pts[8], pts[2], (80, 130, 190), 3, 20)
    sensor(d, c, 230)
    label(d, (c[0], y0 + 40), 'צפון מגנטי ↑', F(42), WHITE)
    label(d, (c[0], y1 - 50), 'קווי השדה המגנטי של כדור הארץ', F(38, False), BLUE_L)
    right_block(d, 'איך הוא עובד', 'כמו מצפן מגנטי, בעזרת אלקטרו-מגנטים זעירים.',
                ('שאלה מהמאגר · 78 · 156', 'בהתייחס למצפן FLUX GATE (שער שטף מגנטי). סמן את התשובה הנכונה.',
                 ['כמו מצפן מגנטי מורה על הצפון בהשפעת הכוחות המגנטיים בסביבה', 'במקום מוטות מגנטיים מותקנים בו אלקטרו-מגנטים זעירים',
                  'מייצר שדה מגנטי עצמי, שאותו מתקן היצרן מראש לבטול הוריאציה והדויאציה', 'א ו-ב נכונים'], 3))
    save(im, 's03_fluxgate_q78')

def s04():
    im, d = base(); left_panel(d, 'חיישן רחוק מההפרעות, מסכים איפה שנוח')
    box = inner(); sea(im, box); x0, y0, x1, y1 = box
    bc = ((x0 + x1) / 2, (y0 + y1) / 2 - 20); T = boat(im, bc, 900, 0); d = ImageDraw.Draw(im)
    eng = T(0, -0.43); d.rounded_rectangle((eng[0] - 75, eng[1] - 35, eng[0] + 75, eng[1] + 35), 10, fill=(90, 95, 105), outline=WHITE, width=3)
    def side(p, s, col, right):
        q = (bc[0] + (240 if right else -240), p[1]); d.line((p, q), fill=col, width=3)
        label(d, (q[0] + (12 if right else -12), q[1]), s, F(40), col, 'l' if right else 'r')
    side(eng, 'מנוע', WHITE, True)
    sp = T(0, 0.3); sensor(d, sp, 55)
    hm = T(0, -0.02); d.rounded_rectangle((hm[0] - 60, hm[1] - 40, hm[0] + 60, hm[1] + 40), 10, fill=(8, 14, 22), outline=GREEN_L, width=4)
    label(d, (hm[0], hm[1]), '045°', F(34), GREEN_L)
    ap = T(-0.08, -0.22); d.rounded_rectangle((ap[0] - 55, ap[1] - 30, ap[0] + 55, ap[1] + 30), 8, fill=(40, 44, 52), outline=ORANGE, width=3)
    vh = T(0.08, -0.22); d.rounded_rectangle((vh[0] - 55, vh[1] - 30, vh[0] + 55, vh[1] + 30), 8, fill=(40, 44, 52), outline=CORAL, width=3)
    for q in (hm, ap, vh): dashed(d, sp, q, BLUE_L, 4)
    side(sp, 'חיישן', BLUE_L, True); side(hm, 'מסך', GREEN_L, False)
    side(ap, 'הגה אוטומטי', ORANGE, False); side(vh, 'מכשיר קשר', CORAL, True)
    label(d, ((x0 + x1) / 2, y1 - 30), 'חסרונות: וריאציה ודויאציה, ותלוי בחשמל', F(40), ORANGE)
    right_block(d, 'יתרונות וחסרונות', 'יתרונות: דיוק של חצי מעלה. מפרידים את המסך מהחיישן. מזין את ההגה האוטומטי ומכשיר הקשר. כמה מסכים בסירה. קטן וקל להתקנה. חסרונות: מושפע מוריאציה ודויאציה. צריך חשמל, ולכן לא יכול להיות המצפן היחיד.')
    save(im, 's04_fluxgate_pros')

def s05():
    im, d = base(); left_panel(d, 'מחפשים את מה שאינו יתרון')
    x0, y0, x1, y1 = inner()
    rows = [('א', 'דיוק של חצי מעלה', 'יתרון', GREEN_L, '✓'), ('ב', 'נוח לתקן וריאציה ודויאציה', 'לא נכון: הוא מושפע משתיהן', CORAL, '✗'),
            ('ג', 'קטן וקל להתקנה', 'יתרון', GREEN_L, '✓'), ('ד', 'חיישן נפרד מהמסך', 'יתרון', GREEN_L, '✓')]
    h = (y1 - y0 - 60) / 4
    for i, (l, t, s, col, mk) in enumerate(rows):
        by = y0 + 20 + i * (h + 10)
        tile(d, (x0 + 20, by, x1 - 20, by + h - 10), f'{l}: {t}', s, col)
        mc = (x0 + 110, by + (h - 10) / 2); s = 38
        if mk == '✓': d.line([(mc[0] - s, mc[1]), (mc[0] - s * 0.3, mc[1] + s * 0.7), (mc[0] + s, mc[1] - s * 0.8)], fill=col, width=14, joint='curve')
        else: d.line((mc[0] - s, mc[1] - s, mc[0] + s, mc[1] + s), fill=col, width=14); d.line((mc[0] - s, mc[1] + s, mc[0] + s, mc[1] - s), fill=col, width=14)
    right_block(d, 'שימו לב', 'השאלה מחפשת את מה שאינו מתאים.',
                ('שאלה מהמאגר · 141', 'למצפן אלקטרוני (FLUX GATE) היתרונות הבאים. סמן את זה שאינו מתאים:',
                 ['ניתן לקבל בו דיוק של כחצי מעלה', 'נוח לתקן בו את שגיאות הדויאציה והוריאציה',
                  'אינו תופס מקום וקל להתקנה בכל מקום', 'ניתן להפריד את התצוגה מהחיישן ולהתקין אותו במקום שאינו מושפע משדות מגנטיים'], 1))
    save(im, 's05_fluxgate_q141')

def s06():
    im, d = base(); left_panel(d, "מצפן ג'יירו: חתך")
    box = inner(); d.rectangle(box, fill=(10, 18, 34)); gyro_img(im, box)
    d = ImageDraw.Draw(im)
    right_block(d, "מצפן ג'יירו", 'סביבון מתכת בתוך מערכת קרדנית. הציר מתיישר עם ציר כדור הארץ, צפון-דרום, ולכן הוא מראה צפון אמיתי. אינו מצפן מגנטי: אין וריאציה ואין דויאציה. שגיאת כיול בלבד.')
    save(im, 's06_gyro_how')

def s07():
    im, d = base(); left_panel(d, "ג'יירו: יתרונות וחסרונות")
    x0, y0, x1, y1 = inner(); xm = (x0 + x1) / 2
    label(d, (xm + (x1 - xm) / 2, y0 + 40), 'יתרונות', F(54), GREEN_L); label(d, (x0 + (xm - x0) / 2, y0 + 40), 'חסרונות', F(54), CORAL)
    pros = ['דיוק גבוה מאוד', 'בלי וריאציה ודויאציה', 'מזין הגה אוטומטי', 'רפיטרים בכל הספינה']
    cons = ['תלוי בחשמל', 'יקר', 'זמן עד שמתייצב', 'מייצר שדה מגנטי']
    h = 200
    for i, (p, c) in enumerate(zip(pros, cons)):
        by = y0 + 110 + i * (h + 26)
        tile(d, (xm + 10, by, x1 - 10, by + h), p, '', GREEN_L)
        tile(d, (x0 + 10, by, xm - 10, by + h), c, '', CORAL)
    right_block(d, 'מה מייחד אותו', 'מדויק מאוד ולא מגנטי. אבל תלוי בחשמל, יקר, צריך זמן להתייצב, ומסיט מצפן מגנטי שקרוב אליו.')
    save(im, 's07_gyro_pros')

def _gyro_cons(d, extra=False):
    x0, y0, x1, y1 = inner(); n = 3 if extra else 2
    h = (y1 - y0 - 40 - (n - 1) * 30) / n
    items = [('צורך חשמל רציף ותלוי בו', 'בלי חשמל אין מצפן', 'bolt'), ('אינו מתייצב מייד', 'אחרי הדלקה צריך לחכות', 'clock'),
             ('שגיאה לפי קו רוחב', 'ולפי הכיוון והמהירות', 'globe')][:n]
    for i, (t, s, ic) in enumerate(items):
        by = y0 + 20 + i * (h + 30)
        tile(d, (x0 + 20, by, x1 - 20, by + h), t, s, ORANGE)
        c = (x0 + 160, by + h / 2)
        if ic == 'bolt': bolt(d, c, h * 0.32)
        elif ic == 'clock': clock(d, c, h * 0.28)
        else:
            r = h * 0.28; d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), outline=BLUE_L, width=6)
            for f in (-0.5, 0, 0.5): d.line((c[0] - r * math.sqrt(1 - f * f), c[1] + f * r, c[0] + r * math.sqrt(1 - f * f), c[1] + f * r), fill=BLUE_L, width=3)

GYRO_OPTS = ['אינו יכול לשמש כחיישן להגה אוטומטי, ואינו מפיק את הצפון המגנטי', 'מייצר שדה מגנטי שמסיט מצפנים נוספים בסביבתו', 'ניתן להתקנה רק בכלי שיט גדולים ומבנה מתכת']

def s08():
    im, d = base(); left_panel(d, 'החסרונות המשמעותיים')
    _gyro_cons(d)
    right_block(d, "חסרונות הג'יירו", 'חשמל רציף, וזמן התייצבות.',
                ('שאלה מהמאגר · 51', 'מהם החסרונות המשמעותיים של המצפן הסביבוני המכני (ג\'יירו)?',
                 ['צורך חשמל רציף ותלוי בו, אינו מתייצב מייד ברגע הפעלתו'] + GYRO_OPTS, 0))
    save(im, 's08_gyro_q51')

def s09():
    im, d = base(); left_panel(d, 'אותה תשובה, עם תוספת')
    _gyro_cons(d, extra=True)
    right_block(d, 'כמעט זהה', 'אותה תשובה, ועוד שגיאה לפי קו הרוחב, הכיוון והמהירות.',
                ('שאלה מהמאגר · 157', 'מה הם החסרונות המשמעותיים של מצפן סביבוני מכני (Gyrocompass)?',
                 ['צורך חשמל רציף ותלוי בו, אינו מתייצב מייד ברגע הפעלתו, מפתח שגיאה בתלות בקו הרוחב ובכוון/מהירות של כלי השיט'] + GYRO_OPTS, 0))
    save(im, 's09_gyro_q157')

def s10():
    im, d = base(); left_panel(d, 'חרטום מול תנועה')
    x0, y0, x1, y1 = inner(); sb = (x0, y0, x1, y0 + 600); sea(im, sb)
    bc = ((x0 + x1) / 2 - 80, y0 + 380); boat(im, bc, 300, 0); d = ImageDraw.Draw(im)
    dashed(d, bc, (bc[0], y0 + 40), ORANGE, 5); label(d, (bc[0] - 20, y0 + 50), 'חרטום 000°', F(40), ORANGE, 'r')
    tip = polar_pt(bc, 360, 20); arrow(d, bc, tip, GREEN_L, 9, 40); label(d, (tip[0] + 20, tip[1] + 30), 'תנועה 020°', F(40), GREEN_L, 'l')
    label(d, (x1 - 40, y0 + 560), 'זרם ←', F(38), BLUE_L, 'r')
    cy = y0 + 830; cc = (x1 - 270, cy); compass(im, cc, 190, heading=0); d = ImageDraw.Draw(im)
    label(d, (cc[0], cy + 230), 'מצפן: חרטום, צפון מגנטי', F(38), ORANGE)
    readout(d, (x0 + 60, cy - 170, x0 + 500, cy + 170), 'GPS · COG · T', '020°')
    label(d, (x0 + 280, cy + 230), 'GPS: תנועה, צפון אמיתי', F(38), GREEN_L)
    right_block(d, 'הכיוון האמיתי', 'ה-GPS מחשב את התנועה על פני הקרקע, ביחס לצפון האמיתי. בלי וריאציה ובלי דויאציה.',
                ('שאלה מהמאגר · 187', 'איזה מהמכשירים שלהלן מראה את כיוון ההפלגה האמיתי של ספינה ביחס לכיוון הצפון האמיתי?',
                 ['G.P.S.', 'מצפן מגנטי', 'מצפן חשמלי', 'מצפן שטף מגנטי'], 0))
    save(im, 's10_true_course_q187')

def s11():
    im, d = base()
    box = (0, 0, 1300, 1440); d.rectangle(box, fill=(10, 18, 34)); gyro_img(im, (40, 40, 1260, 1400))
    d = ImageDraw.Draw(im)
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['שער שטף = מצפן מגנטי', 'אלקטרו-מגנטים במקום מחט', 'מדויק, חיישן נפרד, מזין הגה אוטומטי', 'מושפע מוריאציה ודויאציה, צריך חשמל',
             "ג'יירו אינו מגנטי", 'צפון אמיתי, שגיאת כיול בלבד', 'חסרונות: חשמל, מחיר, זמן התייצבות', 'כיוון אמיתי ביחס לצפון אמיתי: GPS']
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 4 else ORANGE)
        text_r(d, 2380, y + 20, s, F(48, False), TEXT)
    save(im, 's11_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11]

def sheet():
    names = sorted(n for n in os.listdir(C.OUT) if n.endswith('.png') and not n.startswith('_'))
    th = [Image.open(os.path.join(C.OUT, n)).resize((640, 360)) for n in names]
    cols = 4; rows = (len(th) + cols - 1) // cols
    sh = Image.new('RGB', (cols * 650 + 10, rows * 370 + 10), (0, 0, 0))
    for i, t in enumerate(th): sh.paste(t, (10 + (i % cols) * 650, 10 + (i // cols) * 370))
    sh.save(os.path.join(C.OUT, '_sheet.png')); print('ok _sheet', len(th))

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only: fn()
    sheet()
