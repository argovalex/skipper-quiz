"""Lesson 12 (l30): GPS. Real photos (assets/u12_*.jpg from Wikimedia Commons, credits in assets/u12_credits.txt) with drawn overlays."""
import math, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U6 = _load('u06', 'u06_cards.py'); U8 = _load('u08', 'u08_cards.py'); U11 = _load('u11', 'u11_cards.py')
from PIL import Image, ImageDraw
import real as RL
C.OUT = os.path.join(HERE, '..', 'cards', 'GPS'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · GPS'
F, text_c, text_r, label, dot, arrow = C.F, C.text_c, C.text_r, C.label, C.dot, C.arrow
base, left_panel, right_block, save, RC = C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, ORANGE, CORAL, GREEN, GREEN_L, BLUE_L, PANEL, MUTED = C.TEXT, C.ORANGE, C.CORAL, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL, C.MUTED
readout, inner, sea, WHITE = U5.readout, U5.inner, U5.sea, U5.WHITE
photo, tag, photo_map, dashed, box_text, DARK = U8.photo, U8.tag, U8.photo_map, U8.dashed, U8.box_text, U8.DARK
pointer, row_boxes, contain = U11.pointer, U11.row_boxes, U11.contain
SKY = (6, 10, 20)

CREDIT = {'u12_furuno': 'Photo: umi (Flickr) · CC BY-SA 2.0', 'u12_plotter': 'Photo: RheinSkipper · CC BY-SA 3.0',
          'u12_raymarine': 'Photo: Fairley · CC BY 2.0', 'u12_antenna': 'Photo: David Monniaux · CC BY-SA 3.0', 'u12_sat': 'Image: NASA'}
def credit(d, box, name):
    f = F(20, False); s = CREDIT[name]; w = d.textlength(s, font=f)
    d.rectangle((box[2] - w - 16, box[3] - 32, box[2], box[3]), fill=(0, 0, 0)); d.text((box[2] - w - 8, box[3] - 28), s, font=f, fill=(200, 200, 200))

def sat(d, p, s=1.0, col=(230, 190, 90)):
    """Small satellite icon: body + two solar panels."""
    x, y = p; b, pw, ph = 18 * s, 46 * s, 20 * s
    for k in (-1, 1):
        x0 = x + k * (b + 6 * s); x1 = x0 + k * pw
        d.rectangle((min(x0, x1), y - ph / 2, max(x0, x1), y + ph / 2), fill=(60, 90, 170), outline=(150, 180, 240), width=2)
    d.rectangle((x - b, y - b, x + b, y + b), fill=col, outline=WHITE, width=2)

def globe(im, c, R, lat0=25, lon0=20):
    g = RL.globe_img(int(R), lat0, lon0); im.paste(g, (int(c[0] - R), int(c[1] - R)), g); return ImageDraw.Draw(im)

def circle(d, c, r, col, w=5):
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), outline=col, width=w)

def boat(d, p, ang=0, s=1.0, col=WHITE):
    """Top-view hull outline pointing at compass angle ang."""
    pts = [(0, -60), (22, -20), (22, 45), (0, 55), (-22, 45), (-22, -20)]
    a = math.radians(ang)
    q = [(p[0] + s * (x * math.cos(a) - y * math.sin(a)), p[1] + s * (x * math.sin(a) + y * math.cos(a))) for x, y in pts]
    d.polygon(q, fill=col, outline=(30, 30, 30))

def pt(c, r, deg): a = math.radians(deg); return (c[0] + r * math.sin(a), c[1] - r * math.cos(a))

# ---------- cards ----------
def s01():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u12_sat', focus=(0.55, 0.5)); credit(d, (0, 0, 1300, 1440), 'u12_sat')
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 12', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'GPS', F(150), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['איך הוא יודע איפה אתה', 'מהירות וקורס ביחס לקרקע', 'MOB ו-MARK', 'שגיאות, דאטום ואנטנה']):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    im, d = base(); left_panel(d, '24 לוויינים סביב כדור הארץ')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=SKY); c = ((x0 + x1) / 2, y0 + 470); R = 230
    d = globe(im, c, R)
    for k, (rx, ry, rot) in enumerate([(520, 170, -25), (520, 170, 25), (520, 170, 75)]):
        pts = []
        for t in range(0, 361, 4):
            a = math.radians(t); x, y = rx * math.cos(a), ry * math.sin(a); r = math.radians(rot)
            pts.append((c[0] + x * math.cos(r) - y * math.sin(r), c[1] + x * math.sin(r) + y * math.cos(r)))
        d.line(pts, fill=(90, 120, 170), width=2)
        for j in range(4):
            sat(d, pts[(j * 23 + k * 7) % len(pts)], 0.7)
    for i, (h, s, col) in enumerate([('ניווט משוער', 'מהירות, זמן, כיוון', MUTED), ('ניווט אסטרונומי', 'לפי הכוכבים', MUTED), ('GPS', 'לוויינים', GREEN_L)]):
        bx1 = x1 - 20 - i * 385
        box_text(d, (bx1 - 360, y1 - 250, bx1, y1 - 30), [(h, 40, col), (s, 32, TEXT)], col)
    right_block(d, 'מה זה GPS', 'מערכת מיקום גלובלית. 24 לוויינים, ובכל רגע המקלט רואה לפחות 4. מערכת צבאית של ארצות הברית.')
    save(im, 's02_what')

def s03():
    im, d = base(); left_panel(d, 'מיקום + שעה → טווח')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=SKY); c = ((x0 + x1) / 2, y1 + 620); R = 900
    d = globe(im, c, R, 32, 34); d.rectangle((x0, y1, x1, y1 + 700), fill=C.NAVY2)
    rx = pt(c, R, 0); dot(d, rx, 14, GREEN_L); tag(d, (rx[0], rx[1] + 60), 'המקלט', GREEN_L, 34)
    for p in [(x0 + 200, y0 + 140), ((x0 + x1) / 2, y0 + 90), (x1 - 200, y0 + 160)]:
        dashed(d, p, rx, ORANGE, 4); sat(d, p, 1.1)
    tag(d, ((x0 + x1) / 2, y0 + 190), 'אני כאן · השעה', ORANGE, 32)
    st = pt(c, R, -28); d.polygon([(st[0], st[1] - 50), (st[0] - 26, st[1]), (st[0] + 26, st[1])], fill=WHITE)
    tag(d, (st[0] + 30, st[1] - 100), 'תחנת קרקע', BLUE_L, 32)
    box_text(d, (x0 + 160, y0 + 420, x1 - 160, y0 + 560), [('טווח = מהירות × זמן', 48, GREEN_L)])
    right_block(d, 'איך זה עובד', 'כל לוויין משדר מיקום ושעה מדויקת. המקלט מחשב טווח מההפרש בזמן. תחנות קרקע מאפסות את השעון ומעדכנות מיקומי לוויינים.')
    save(im, 's03_how')

def trilat(d, box, n=3, spread=True):
    """n range circles around satellites; their meeting point is the fix."""
    x0, y0, x1, y1 = box; fix = ((x0 + x1) / 2, (y0 + y1) / 2 + 40)
    angs = [-50, 50, 180] if spread else [-25, 0, 25]
    for i, a in enumerate(angs[:n]):
        r = 260 if spread else 330; s = pt(fix, r, a)
        circle(d, s, r, [ORANGE, BLUE_L, CORAL][i], 5); sat(d, s, 0.8)
    return fix

def s04():
    im, d = base(); left_panel(d, 'שלושה טווחים = נקודה')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=SKY)
    fix = trilat(d, (x0, y0, x1, y1 - 120)); dot(d, fix, 18, GREEN_L)
    tag(d, (fix[0], fix[1] + 70), 'כאן אני', GREEN_L, 36)
    box_text(d, (x0 + 120, y1 - 150, x1 - 120, y1 - 30), [('המקלט רק מקשיב · טווחים, לא כיוונים', 40, GREEN_L)])
    right_block(d, 'איך מתקבל אתר', 'קוד זיהוי וטווח משלושה לוויינים או יותר. נקודת המפגש של הטווחים היא קו אורך וקו רוחב.',
                ('שאלה מהמאגר · 41', 'כיצד מפיק מקלט ה-GPS את האתר?',
                 ['שולח קוד ללוויינים, והם מחזירים אתר', 'קוד זיהוי וטווח מ-3 לוויינים, והמרה לאורך ורוחב',
                  'חיתוך הכיוונים אל 3 לוויינים', 'כל לוויין שולח זמן, אורך או רוחב'], 1))
    save(im, 's04_fix_q41')

def s05():
    im, d = base(); left_panel(d, 'Global Positioning System')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, (x0, y0, x1, y0 + 760), 'u12_furuno', focus=(0.42, 0.42)); credit(d, (x0, y0, x1, y0 + 760), 'u12_furuno')
    for i, (en, he_) in enumerate([('Global', 'גלובלית'), ('Positioning', 'מיקום'), ('System', 'מערכת')]):
        bx0 = x0 + 20 + i * 385                         # English reads left to right: G P S
        box_text(d, (bx0, y0 + 800, bx0 + 360, y1 - 20), [(en[0], 90, GREEN_L), (en, 34, TEXT), (he_, 40, ORANGE)])
    right_block(d, 'ממ״ג', 'מערכת מיקום גלובלית. היא נותנת מיקום, לא מזהה אף אחד.',
                ('שאלה מהמאגר · 42', 'ראשי תיבות G.P.S/ממ״ג, מה פירושן?',
                 ['מערכת זיהוי גלובלית', 'מערכת מיקום גלובלית · Global Positioning System',
                  'Grounding Position of Satellites', 'א ו-ב נכונות'], 1))
    save(im, 's05_name_q42')

def s06():
    im, d = base(); left_panel(d, '1, 2, 3 לוויינים')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=SKY); w = (x1 - x0) / 3
    for k in range(3):                                  # right-to-left: 1, 2, 3 satellites
        bx1 = x1 - k * w; cx = bx1 - w / 2; fix = (cx, y0 + 480); n = k + 1
        for i, a in enumerate([-60, 60, 180][:n]):
            s = pt(fix, 95, a); circle(d, s, 95, [ORANGE, BLUE_L, CORAL][i], 4); sat(d, s, 0.55)
        if n == 2:
            for a in (0, 180):
                q = pt(pt(fix, 150, -60), 150, 120 if a == 0 else 0);
            dot(d, fix, 12, ORANGE); dot(d, pt(fix, 95, 0), 12, ORANGE)
        if n == 3: dot(d, fix, 14, GREEN_L)
        label(d, (cx, y0 + 60), f'{n}', F(70), WHITE)
        label(d, (cx, y1 - 200), ['עיגול', 'שתי נקודות', 'נקודה אחת'][k], F(42), [CORAL, ORANGE, GREEN_L][k])
    box_text(d, (x0 + 120, y1 - 130, x1 - 120, y1 - 20), [('במבחן · מינימום 3 לוויינים', 44, GREEN_L)])
    right_block(d, 'כמה לוויינים', 'שלושה טווחים נותנים נקודה אחת. המקלט רואה תמיד 4, אבל במבחן המינימום הוא 3.',
                ('שאלה מהמאגר · 45', 'על מנת לקבל מיקום באמצעות ממ״ג יש צורך ב:',
                 ['קליטה של לוויין אחד לפחות', 'קליטה בו זמנית מ-2 לוויינים',
                  'קליטה בו זמנית מ-3 לוויינים לפחות', 'קליטה בו זמנית מ-4 לוויינים לפחות'], 2))
    save(im, 's06_sats_q45')

def s07():
    im, d = base(); left_panel(d, 'מדליקים, והוא עובד')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, (x0, y0, x1, y0 + 560), 'u12_furuno', focus=(0.42, 0.42)); credit(d, (x0, y0, x1, y0 + 560), 'u12_furuno')
    row_boxes(d, x0 + 10, x1 - 10, y0 + 590, 190, [[('בלי הזנת נתונים', 34, GREEN_L)], [('1200 MHz', 38, GREEN_L), ('פחות הפרעות', 30, TEXT)],
                                                  [('FIX כל שנייה', 34, GREEN_L)], [('ים, אוויר, יבשה', 32, GREEN_L)]], size=34)
    box_text(d, (x0 + 10, y0 + 810, x1 - 10, y1 - 10), [('אתחול קר · כ-15 דקות', 44, ORANGE),
                                                       ('מכשיר חדש · 6+ חודשים כבוי · 1000+ km', 36, TEXT)], ORANGE)
    right_block(d, 'מאפיינים', 'לא מכניסים נתונים. תדר גבוה, עדכון כל שנייה, ועובד בכל מקום. אתחול קר לוקח כרבע שעה.')
    save(im, 's07_features')

def s08():
    im, d = base(); left_panel(d, 'הגדרות והתראות')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, box, 'u12_plotter', dim=0.3, focus=(0.5, 0.45)); credit(d, box, 'u12_plotter')
    cols = [('יחידות', ['מרחק · NM, km, M', 'מהירות · kn, km/h, MPH', 'זמן · GMT או מקומי', 'קו ישר או מעגל גדול'], GREEN_L),
            ('התראות', ['סוללה חלשה', 'קליטה חלשה', 'התקרבות ל-WP', 'יציאה מהנתיב', 'יציאה מרדיוס עגינה'], ORANGE)]
    for j, (h, items, col) in enumerate(cols):
        cx = x1 - 290 - j * 580
        label(d, (cx, y0 + 70), h, F(56), col)
        for i, s in enumerate(items):
            y = y0 + 150 + i * 175
            d.rounded_rectangle((cx - 270, y, cx + 270, y + 145), 22, fill=DARK, outline=col, width=4)
            label(d, (cx, y + 72), s, F(36, False), TEXT)
    right_block(d, 'הגדרות', 'בוחרים יחידות מרחק, מהירות וזמן. ההתראות שומרות עליך כשאתה לא מסתכל על המסך.')
    save(im, 's08_settings')

def s09():
    im, d = base(); left_panel(d, 'GPS נותן רק מיקום')
    box = inner(); x0, y0, x1, y1 = box
    bx = (x0, y0, x1, y0 + 760)
    d, P = photo_map(im, bx, 'u12_raymarine', (0.6, 0.35)); credit(d, bx, 'u12_raymarine')
    s = P(2240, 300); pointer(d, (s[0] + 40, s[1] + 230), s, GREEN_L); tag(d, (s[0] + 40, s[1] + 270), 'SOG · COG', GREEN_L, 38)
    row_boxes(d, x0 + 10, x1 - 10, y0 + 790, 250, [[('מיקום', 46, GREEN_L), ('מה שה-GPS מודד', 30, TEXT)],
                                                   [('SOG', 46, ORANGE), ('מהירות ביחס לקרקע', 30, TEXT)],
                                                   [('COG', 46, ORANGE), ('קורס ביחס לקרקע', 30, TEXT)]])
    right_block(d, 'מיקום בלבד', 'כל השאר הוא חישוב: מיקום מול מיקום לאורך זמן. SOG ו-COG כבר כוללים את הזרם.')
    save(im, 's09_position_only')

def s10():
    im, d = base(); left_panel(d, 'מרחק חלקי זמן')
    box = inner(); x0, y0, x1, y1 = box
    sea(im, box); d = ImageDraw.Draw(im)
    a, b = (x0 + 250, y1 - 230), (x1 - 250, y0 + 230)
    dashed(d, a, b, WHITE, 5); boat(d, b, 45, 1.3)
    for p, t in [(a, '12:00'), (b, '12:30')]: dot(d, p, 14, ORANGE); tag(d, (p[0], p[1] + 70), t, ORANGE, 40)
    tag(d, ((a[0] + b[0]) / 2 + 120, (a[1] + b[1]) / 2 + 60), '3 NM', WHITE, 44)
    readout(d, (x0 + 40, y0 + 40, x0 + 480, y0 + 260), 'GPS · SOG', '6.0 kn')
    right_block(d, 'כן, מודד מהירות', 'הוא יודע כמה מרחק עברת ובכמה זמן.',
                ('שאלה מהמאגר · 188', 'האם ה-G.P.S יכול למדוד מהירות?', ['כן', 'לא', 'רק בשיט איטי', 'רק בים שקט'], 0))
    save(im, 's10_speed_q188')

def s11():
    im, d = base(); left_panel(d, 'עוגן בזרם')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, box, 'u8_anchoring', (0.5, 0.42))
    for k in range(3):
        a = P(300 + k * 260, 1900 - k * 120); arrow(d, a, (a[0] + 150, a[1] - 220), BLUE_L, 9, 34)
    tag(d, P(560, 2050), 'זרם', BLUE_L, 40)
    readout(d, (x1 - 470, y0 + 40, x1 - 40, y0 + 260), 'GPS · SOG', '0.0 kn', GREEN_L)
    readout(d, (x1 - 470, y0 + 290, x1 - 40, y0 + 510), 'LOG · STW', '1.5 kn', ORANGE)
    right_block(d, 'הסירה לא זזה', 'ביחס לקרקע אין תנועה, אז ה-GPS מראה אפס. המים זורמים מתחת, ומד המהירות מרגיש אותם.',
                ('שאלה מהמאגר · 47', 'כאשר כלי שיט עוגן במקום שבו יש זרם:',
                 ['GPS יראה את הזרם, מד המהירות אפס', 'GPS יראה אפס, מד המהירות את הזרם',
                  'מול הקרקע פלוס, מול המים מינוס', 'אפס בכל מקרה, המדים לא מדויקים'], 1))
    save(im, 's11_anchor_q47')

def s12():
    im, d = base(); left_panel(d, 'הזרם כבר בפנים')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, box, 'u7_boat_aerial', (0.5, 0.45))
    bw = P(1024, 520); arrow(d, (bw[0] + 230, bw[1] - 40), (bw[0] + 230, bw[1] + 260), CORAL, 10, 38)
    tag(d, (bw[0] + 230, bw[1] + 320), 'זרם נגדי 2 kn', CORAL, 36)
    readout(d, (x0 + 40, y0 + 40, x0 + 480, y0 + 260), 'GPS · SOG', '8.0 kn', GREEN_L)
    box_text(d, (x0 + 120, y1 - 150, x1 - 120, y1 - 30), [('ביחס לקרקע · 8 קשרים', 46, GREEN_L)])
    right_block(d, '8 זה 8', 'ה-GPS מודד ביחס לקרקע, אז הזרם כבר בחשבון. מי שמוסיף או מחסיר, סופר אותו פעמיים.',
                ('שאלה מהמאגר · 104', 'GPS מראה 8 קשר, באזור זרם נגדי של 2 קשר. מה המהירות ביחס לקרקע?',
                 ['8 קשרים', '10 קשרים', '6 קשרים', 'לא ניתן לדעת'], 0))
    save(im, 's12_current_q104')

def s13():
    im, d = base(); left_panel(d, 'מצפן מול GPS')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, box, 'u7_boat_aerial', (0.5, 0.45))
    b = P(1024, 640); top = y0 + 110
    arrow(d, b, (b[0], top), ORANGE, 10, 40); tag(d, (b[0] - 40, top + 40), 'מצפן · לאן החרטום', ORANGE, 34, 'r')
    e = pt(b, (b[1] - top) / math.cos(math.radians(28)), 28); arrow(d, b, e, GREEN_L, 10, 40); tag(d, (e[0] + 30, e[1] + 40), 'GPS · לאן זזים', GREEN_L, 34, 'l')
    row_boxes(d, x0 + 30, x1 - 30, y1 - 190, 160, ['VAR', 'DEV', 'LEEWAY'], ORANGE, 44)
    right_block(d, 'לא אותו קורס', 'המצפן מראה Compass Course. ה-GPS מראה Course Over Ground. ביניהם וריאציה, דביאציה וסחיפה.')
    save(im, 's13_compass')

def s14():
    im, d = base(); left_panel(d, 'פונקציות')
    box = inner(); x0, y0, x1, y1 = box
    bx = (x0, y0, x1, y0 + 760)
    d, P = contain(im, bx, 'u12_plotter', bg=(0, 0, 0)); credit(d, bx, 'u12_plotter')
    m = P(1987, 1298); circle(d, m, 70, ORANGE, 6); tag(d, (m[0] - 30, m[1] + 140), 'MARK', ORANGE, 38)
    row_boxes(d, x0 + 10, x1 - 10, y0 + 790, 250, [[('Way Point', 38, GREEN_L), ('נקודת ציון', 30, TEXT)], [('Route', 38, GREEN_L), ('נתיב', 30, TEXT)],
                                                   [('Go To', 38, GREEN_L), ('כיוון וטווח', 30, TEXT)], [('MOB', 38, CORAL), ('אדם במים', 30, TEXT)]], size=38)
    right_block(d, 'מה עוד', 'נקודות ציון, נתיב, Go To לנקודה. ושני כפתורים שחשוב להכיר: MOB ו-MARK.')
    save(im, 's14_functions')

def s15():
    im, d = base(); left_panel(d, 'ROUTE, TRACK, CTS')
    box = inner(); x0, y0, x1, y1 = box
    sea(im, box); d = ImageDraw.Draw(im)
    wps = [(x1 - 160, y1 - 160), (x1 - 420, y0 + 420), (x0 + 380, y0 + 560), (x0 + 180, y0 + 140)]
    for a, b in zip(wps, wps[1:]): d.line((a, b), fill=GREEN_L, width=7)
    for i, p in enumerate(wps):
        dot(d, p, 16, GREEN_L); tag(d, (p[0], p[1] - 55), f'WP{i + 1}', GREEN_L, 32)
    trk = [wps[0]] + [((wps[0][0] * (1 - t) + wps[1][0] * t) + 70 * math.sin(t * 6), wps[0][1] * (1 - t) + wps[1][1] * t) for t in [i / 10 for i in range(1, 8)]]
    d.line(trk, fill=ORANGE, width=5); me = trk[-1]; boat(d, me, -20, 0.9)
    dashed(d, me, wps[1], CORAL, 5); tag(d, (me[0] - 210, me[1] + 20), 'CTS', CORAL, 38)
    tag(d, (x0 + 330, y1 - 240), 'ROUTE · כל הנתיב', GREEN_L, 36); tag(d, (x0 + 330, y1 - 150), 'TRACK · המסלול', ORANGE, 36)
    right_block(d, 'שלושה מושגים', 'ROUTE: כמה קטעים בין נקודות ציון, שמור בשם. TRACK: הדרך בין יציאה ליעד. CTS: הקורס המתוקן לנקודה שבחרת.',
                ('שאלה מהמאגר · 160', 'במקלט GPS מה פירוש ROUTE, TRACK ו-Course To Steer?',
                 ['קטע אחד בין 2 נקודות; עקום התנועה; חזרה ל-ROUTE', 'כמה קטעים שמורים בשם; הנתיב ליעד; קורס מתוקן לנקודה',
                  'הקורס האמיתי; עקבות ההגה; בלי Cross Track Error', 'מסלול תחרות; צלע; קורס למצוף ראשון'], 1))
    save(im, 's15_route_q160')

def s16():
    im, d = base(); left_panel(d, 'MOB מול MARK')
    box = inner(); x0, y0, x1, y1 = box; mid = (x0 + x1) / 2
    d, P = photo_map(im, (mid + 5, y0, x1, y0 + 720), 'u12_raymarine', (0.84, 0.2))
    m = P(2900, 300); circle(d, m, 80, CORAL, 7); tag(d, (m[0] - 30, m[1] + 160), 'MOB', CORAL, 40)
    credit(d, (mid + 5, y0, x1, y0 + 720), 'u12_raymarine')
    d, P = photo_map(im, (x0, y0, mid - 5, y0 + 720), 'u12_plotter', (0.8, 0.55))
    k = P(1987, 1298); circle(d, k, 70, ORANGE, 7); tag(d, (k[0] - 40, k[1] + 140), 'MARK', ORANGE, 40)
    credit(d, (x0, y0, mid - 5, y0 + 720), 'u12_plotter')
    box_text(d, (mid + 10, y0 + 750, x1 - 10, y1 - 10), [('MOB', 56, CORAL), ('נקודה פעילה', 34, TEXT), ('כיוון וטווח ברציפות', 34, TEXT)], CORAL)
    box_text(d, (x0 + 10, y0 + 750, mid - 10, y1 - 10), [('MARK', 56, ORANGE), ('רק שומר', 34, TEXT), ('את המיקום', 34, TEXT)], ORANGE)
    right_block(d, 'אדם במים', 'MOB הופך את המיקום לנקודה פעילה ומוביל אותך בחזרה. MARK רק שומר.',
                ('שאלה מהמאגר · 44, 159', 'מה ההבדל בין פקד MOB ופקד MARK?',
                 ['אין הבדל, שניהם מסמנים נקודת דרך', 'MOB: נקודה פעילה עם כיוון וטווח; MARK רק מסמן',
                  'MARK: כיוון הפוך 180°; MOB: Miles Off Buoy', 'MARK: אזעקת טווח; MOB: מצב תחזוקה'], 1))
    save(im, 's16_mob_q44')

def s17():
    im, d = base(); left_panel(d, 'דיוק, DGPS, DATUM')
    box = inner(); x0, y0, x1, y1 = box
    bx = (x0, y0, x1, y0 + 700)
    d, P = contain(im, bx, 'u12_plotter', bg=(0, 0, 0)); credit(d, bx, 'u12_plotter')
    t = P(1180, 1050); dot(d, t, 16, GREEN_L); tag(d, (t[0] + 40, t[1]), 'DATUM נכון', GREEN_L, 30, 'l')
    w = P(800, 760); dot(d, w, 16, CORAL); tag(d, (w[0] - 40, w[1]), 'DATUM שגוי', CORAL, 30, 'r'); dashed(d, w, t, CORAL, 4)
    row_boxes(d, x0 + 10, x1 - 10, y0 + 730, 300, [[('תצוגה', 38, MUTED), ('אלפית דקה', 30, TEXT), ('1.85 m', 30, TEXT)],
                                                   [('שגיאה', 38, CORAL), ('GPS רגיל', 30, TEXT), ('3-5 m', 30, TEXT)],
                                                   [('DGPS', 38, GREEN_L), ('1-3 m', 30, TEXT), ('היום פחות ממטר', 26, TEXT)],
                                                   [('DATUM', 38, ORANGE), ('כמו במפה', 30, TEXT), ('WGS 84', 30, TEXT)]], size=38)
    right_block(d, 'שגיאות', 'אלפית דקה היא רק פירוט התצוגה. השגיאה של GPS רגיל: 3 עד 5 מטר. DGPS מוריד אותה. הדאטום חייב להתאים למפה.')
    save(im, 's17_errors')

def dop_panel(d, box, close, col):
    x0, y0, x1, y1 = box; rx = ((x0 + x1) / 2, y1 - 120)
    angs = [-12, 0, 12] if close else [-60, 0, 60]
    for a in angs:
        s = pt(rx, 330, a); d.line((s, rx), fill=(120, 140, 170), width=3); sat(d, s, 0.6)
    ew, eh = (120, 34) if close else (40, 34)
    d.ellipse((rx[0] - ew, rx[1] - eh, rx[0] + ew, rx[1] + eh), fill=col)
    dot(d, rx, 8, WHITE)

def s18():
    im, d = base(); left_panel(d, 'לוויינים צפופים = דיוק נמוך')
    box = inner(); x0, y0, x1, y1 = box; mid = (x0 + x1) / 2
    d.rectangle(box, fill=SKY)
    dop_panel(d, (mid + 10, y0 + 40, x1 - 10, y0 + 640), False, GREEN)
    dop_panel(d, (x0 + 10, y0 + 40, mid - 10, y0 + 640), True, CORAL)
    label(d, ((mid + x1) / 2, y0 + 700), 'פרושים · PDOP נמוך', F(38), GREEN_L)
    label(d, ((x0 + mid) / 2, y0 + 700), 'צפופים · PDOP גבוה', F(38), CORAL)
    row_boxes(d, x0 + 10, x1 - 10, y0 + 790, 230, [[('TDOP', 38, MUTED), ('זמן', 32, TEXT)], [('VDOP', 38, MUTED), ('גובה', 32, TEXT)],
                                                   [('GDOP', 38, MUTED), ('הכל יחד', 32, TEXT)], [('PDOP', 38, GREEN_L), ('מיקום', 32, TEXT)]], size=38)
    right_block(d, 'PDOP', 'כמו חיתוך קווי כיוון בזווית חדה. לוויינים קרובים זה לזה נותנים מיקום מרוח.',
                ('שאלה מהמאגר · 137', 'הפחתת הדיוק באתר בגלל קליטת לוויינים קרובים זה לזה מסומנת ב:',
                 ['TDOP · Time', 'VDOP · Vertical', 'GDOP · Geometric', 'PDOP · Position Dilution Of Precision'], 3))
    save(im, 's18_dop_q137')

def s19():
    im, d = base(); left_panel(d, 'בדיקה ליד הרציף')
    box = inner(); x0, y0, x1, y1 = box
    pb = (x0, y0, x1, y0 + 800)
    d, P = photo_map(im, pb, 'u12_pier', (0.5, 0.35))          # AI scene (nano_banana): yacht at the quay, 3 landmarks
    for n, (ox, oy), s in [(1, (318, 640), 'מגדלור'), (2, (1471, 520), 'מגדל כנסייה'), (3, (2160, 360), 'אנטנה')]:
        p = P(ox, oy); circle(d, p, 46, ORANGE, 6); label(d, (p[0], p[1] - 90), str(n), F(48), ORANGE)
        tag(d, (p[0], p[1] + 85), s, ORANGE, 30)
    b = P(1100, 1000); dot(d, b, 14, GREEN_L); tag(d, (b[0], b[1] + 60), 'קשורים לרציף', GREEN_L, 32)
    box_text(d, (x0 + 10, y0 + 830, x1 - 500, y1 - 10), [('3 כיוונים = אתר ידוע', 40, ORANGE), ('משווים ל-GPS', 36, TEXT)], ORANGE)
    readout(d, (x1 - 470, y0 + 830, x1 - 10, y1 - 10), 'GPS · SOG', '0.0 kn', GREEN_L)
    right_block(d, 'מול מקום ידוע', 'קשורים לרציף: משווים את ה-GPS לחיתוך של 3 כיוונים, ובודקים שהמהירות אפס.',
                ('שאלה מהמאגר · 158', 'כיצד תדע את רמת הדיוק של המקלט שברשותך?',
                 ['לבדוק בספר ההוראות', 'לבחור את האפשרות באתחול', 'D3 ליד המים, לפי גאות ושפל',
                  'ברציף: השוואה לחיתוך 3 כיוונים, ומהירות אפס'], 3))
    save(im, 's19_accuracy_q158')

def s20():
    im, d = base(); left_panel(d, 'איפה מתקינים את האנטנה')
    box = inner(); x0, y0, x1, y1 = box; mid = (x0 + x1) / 2
    d, P = photo_map(im, (mid + 5, y0, x1, y1), 'u12_antenna_alex', (0.5, 0.4))   # Alex's photo: antenna low on the stern rail
    a = P(410, 370); circle(d, a, 170, GREEN_L, 7); tag(d, ((mid + x1) / 2, y1 - 60), 'כך · נמוך, יציב, שמיים פתוחים', GREEN_L, 32)
    d, Q = photo_map(im, (x0, y0, mid - 5, y1), 'u10_arch', (0.42, 0.3))
    r = Q(1060, 445); circle(d, r, 70, CORAL, 7); tag(d, ((x0 + mid) / 2, y1 - 60), 'לא ליד המכ״מ', CORAL, 34)
    right_block(d, 'נמוך ופתוח', 'הלוויינים מעליך, אין צורך בגובה. רחוק מאנטנות VHF ומכ״מ, ולא במקום שנתפסים בו.',
                ('שאלה מהמאגר · 46', 'היכן מומלץ להתקין בספינה את אנטנת הממ״ג?',
                 ['גבוה ככל האפשר', 'נמוך ככל האפשר, עם שדה ראייה לרקיע ומסביב',
                  'גבוה, סמוך לאנטנת המכ״ם', 'אין חשיבות לגובה ולמיקום'], 1))
    save(im, 's20_antenna_q46')

def s21():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u12_sat', focus=(0.55, 0.5)); credit(d, (0, 0, 1300, 1440), 'u12_sat')
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['24 לוויינים · מיקום ושעה', '3 טווחים = מיקום', 'GPS נותן רק מיקום', 'SOG ו-COG כוללים את הזרם',
             'עוגן בזרם · GPS מראה אפס', 'MOB מוביל חזרה · MARK שומר', 'הדאטום חייב להתאים למפה', 'אנטנה נמוכה, רחוק מ-VHF ומכ״מ']
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 6 else ORANGE)
        text_r(d, 2380, y + 20, s, F(48, False), TEXT)
    save(im, 's21_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21]
sheet = lambda: U6.sheet.__globals__.__setitem__('C', C) or U6.sheet()

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:                              # OneDrive can lock a freshly written PNG
                    import time; time.sleep(2)
    sheet()
