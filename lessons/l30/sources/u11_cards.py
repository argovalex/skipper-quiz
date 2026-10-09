"""Lesson 11 (l30): הגה אוטומטי. Realistic photos (assets/u11_*.jpg, Higgsfield nano_banana) with drawn overlays."""
import math, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U6 = _load('u06', 'u06_cards.py'); U8 = _load('u08', 'u08_cards.py')
from PIL import Image, ImageDraw
C.OUT = os.path.join(HERE, '..', 'cards', 'הגה אוטומטי'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · הגה אוטומטי'
F, text_c, text_r, label, dot, arrow = C.F, C.text_c, C.text_r, C.label, C.dot, C.arrow
base, left_panel, right_block, save, RC = C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, ORANGE, CORAL, GREEN, GREEN_L, BLUE_L, PANEL, MUTED = C.TEXT, C.ORANGE, C.CORAL, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL, C.MUTED
readout, inner, WHITE = U5.readout, U5.inner, U5.WHITE
photo, tag, photo_map, dashed, box_text, DARK = U8.photo, U8.tag, U8.photo_map, U8.dashed, U8.box_text, U8.DARK

def pointer(d, src, dst, col=ORANGE):
    d.line((src, dst), fill=col, width=4); dot(d, dst, 9, col)

def row_boxes(d, x0, x1, y, h, items, col=GREEN_L, size=36):
    n = len(items); bw = (x1 - x0 - (n - 1) * 20) / n
    for i, s in enumerate(items):
        bx = x1 - (i + 1) * bw - i * 20
        box_text(d, (bx, y, bx + bw, y + h), [(s, size, col)] if isinstance(s, str) else s, col)

def contain(im, box, name, bg=WHITE):
    """Fit assets/<name>.jpg inside box (no crop) on a bg fill; returns (draw, map original px -> card)."""
    x0, y0, x1, y1 = [int(v) for v in box]; ImageDraw.Draw(im).rectangle(box, fill=bg)
    g = Image.open(os.path.join(U8.RL.A, name + '.jpg')).convert('RGB')
    s = min((x1 - x0) / g.width, (y1 - y0) / g.height); W, H = int(g.width * s), int(g.height * s)
    ox, oy = x0 + (x1 - x0 - W) // 2, y0 + (y1 - y0 - H) // 2
    im.paste(g.resize((W, H), Image.LANCZOS), (ox, oy))
    return ImageDraw.Draw(im), (lambda x, y: (ox + x * s, oy + y * s))

# ---------- cards ----------
def s01():
    im, d = base()
    d, P = contain(im, (0, 0, 1300, 1440), 'u11_install')   # Alex's image: autopilot installation diagram
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 11', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'הגה אוטומטי', F(130), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['ממה הוא בנוי', 'AUTO ו-STANDBY', 'יתרונות וחסרונות', 'הגה רוח']):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    im, d = base(); left_panel(d, 'חלקי המערכת')
    box = inner(); x0, y0, x1, y1 = box
    d, P = contain(im, box, 'u11_install')                     # Alex's image: autopilot installation diagram
    for (ox, oy), s, an in [((365, 125), 'לוח הפעלה', 'l'), ((340, 185), 'חיישן כיוון', 'l'), ((282, 248), 'כבלי היגוי', 'l'),
                            ((215, 310), 'ציר ההגה', 'l'), ((160, 372), 'הנעה סיבובית', 'l'), ((575, 218), 'מצברים', 'c'),
                            ((790, 527), 'חלוקת חשמל', 'r'), ((660, 583), 'יחידת בקרה', 'r'), ((778, 728), 'חיישן זווית הגה', 'l'),
                            ((588, 772), 'מוט דחיפה', 'l'), ((550, 817), 'זרוע הגה', 'l'), ((655, 860), 'הנעה ליניארית', 'l')]:
        tag(d, P(ox + {'l': 28, 'r': -28, 'c': 0}[an], oy), s, ORANGE, 24, an)
    right_block(d, 'ממה הוא בנוי', 'לוח הפעלה, חיישן כיוון (מצפן חשמלי), יחידת בקרה שמשווה בין הקורס שהוזן למצפן, ויחידת הנעה שמסובבת את ההגה. החשמל מהמצברים. אפשר לחבר GPS ומד רוח.')
    save(im, 's02_system')
def s03():
    im, d = base(); left_panel(d, 'AUTO, ±1, ±10, STANDBY')
    box = inner(); x0, y0, x1, y1 = box
    d, P = contain(im, (x0, y0, x1, y0 + 760), 'u11_p70')     # Alex's image: autopilot control head
    for (ox, oy), s, col, tp in [((330, 380), 'AUTO: הגה אוטומטי', GREEN_L, (x1 - 170, y0 + 690)), ((55, 370), 'STANDBY: חזרה לידיים', CORAL, (x0 + 200, y0 + 690)),
                                 ((210, 315), '±1 מעלה', ORANGE, (x0 + 150, y0 + 420)), ((210, 390), '±10 מעלות', ORANGE, (x0 + 150, y0 + 560))]:
        p = P(ox, oy); pointer(d, tp, p, col); tag(d, tp, s, col, 34)
    row_boxes(d, x0 + 30, x1 - 30, y0 + 780, 260, [[('רגישות', 38, GREEN_L), ('לפי מצב הים', 32, TEXT)], [('התראת סטייה', 38, GREEN_L), ('מהקורס', 32, TEXT)],
                                                   [('זווית לרוח', 38, GREEN_L), ('עם מד רוח', 32, TEXT)]])
    right_block(d, 'הפעלה', 'מפליגים על הקורס ולוחצים AUTO. משנים קורס בלחצנים. STANDBY מחזיר את ההגה לידיים.')
    save(im, 's03_how_to_use')
def s04():
    im, d = base(); left_panel(d, 'הדיוק: מצפן ומהירות תגובה')
    box = inner(); x0, y0, x1, y1 = box
    d, P = contain(im, (x0, y0, x1, y0 + 820), 'u11_install')
    c = P(357, 455); d.ellipse((c[0] - 34, c[1] - 34, c[0] + 34, c[1] + 34), outline=GREEN_L, width=6); tag(d, (c[0] - 40, c[1] + 70), 'ג · חיישן הכיוון', GREEN_L, 32, 'r')
    h = P(430, 440); d.ellipse((h[0] - 38, h[1] - 38, h[0] + 38, h[1] + 38), outline=GREEN_L, width=6); tag(d, (h[0] + 40, h[1] - 80), 'ב · מהירות התגובה', GREEN_L, 32, 'l')
    dr = P(340, 715); tag(d, (dr[0] + 60, dr[1] + 40), 'א · התמסורת: רק מבצעת', CORAL, 30, 'l')
    box_text(d, (x0 + 30, y0 + 850, x1 - 30, y1 - 10), [('ההגה האוטומטי מדויק כמו המצפן שלו', 46, GREEN_L)])
    right_block(d, 'דיוק', 'תשובות ב ו-ג: כמה חזק ומהר ההגה מגיב, וכמה מדויק המצפן.',
                ('שאלה מהמאגר · 28', 'במה תלוי דיוק שמירת הקורס שמוזן להגה אוטומטי חשמלי?',
                 ['באיכות הטכנית של מערכת התמסורת', 'בשליטת המשתמש בפקדי מהירות התגובה',
                  'בסוג ובדיוק המצפן, חיישן הכיוון', 'תשובות ב ו-ג נכונות'], 3))
    save(im, 's04_accuracy_q28')
def s05():
    im, d = base(); left_panel(d, 'ידיים חופשיות לתצפית')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, box, 'u10_compass_ship', (0.55, 0.45))
    s = P(780, 632); tag(d, (s[0], s[1] - 80), 'תצפית על ספינה', GREEN_L, 36)
    tag(d, ((x0 + x1) / 2, y1 - 60), 'ההגה האוטומטי נוהג, הידיים פנויות', ORANGE, 38)
    right_block(d, 'היתרון', 'משמרות נוחות יותר, ומי שלא אוחז בהגה פנוי לתצפית ולטיפולים דחופים.',
                ('שאלה מהמאגר · 26', 'מהו יתרונו העיקרי של הגה אוטומטי?',
                 ['מאפשר השטה ב״צוות חסר״', 'משחרר מחובת תצפית',
                  'משמרות נוחות, תצפית וטיפולים דחופים', 'פינוי דרך אוטומטי באזעקת מכ״מ'], 2))
    save(im, 's05_advantage_q26')

def battery(d, box, frac, col):
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, 14, outline=WHITE, width=5); d.rectangle((x1, (y0 + y1) / 2 - 20, x1 + 16, (y0 + y1) / 2 + 20), fill=WHITE)
    d.rounded_rectangle((x0 + 10, y0 + 10, x0 + 10 + (x1 - x0 - 20) * frac, y1 - 10), 8, fill=col)

def s06():
    im, d = base(); left_panel(d, 'צרכן גדול של חשמל')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, (x0, y0, x1, y0 + 760), 'u11_rough', focus=(0.5, 0.45))
    tag(d, ((x0 + x1) / 2, y0 + 60), 'ים סוער: המנוע מתקן בלי הפסקה', ORANGE, 38)
    for i, (frac, col, s) in enumerate([(0.9, GREEN_L, 'ים שקט'), (0.25, CORAL, 'ים סוער')]):
        bx = x1 - 520 - i * 540; battery(d, (bx, y0 + 820, bx + 380, y0 + 960), frac, col)
        label(d, (bx + 190, y0 + 1010), s, F(40), col)
    right_block(d, 'חשמל', 'המנוע עובד כל הזמן. בים גבוה הוא מתקן בלי הפסקה, והמצברים מתרוקנים.',
                ('שאלה מהמאגר · 10', 'מה החיסרון בהגה חשמלי אוטומטי?',
                 ['מושפע מאוד מרוח ומתיחת המפרשים', 'צרכן גדול של חשמל, בעיקר בים סוער',
                  'מסובב את הספינה כשהרוח משתנה', 'אף תשובה אינה נכונה'], 1))
    save(im, 's06_power_q10')

def s07():
    im, d = base(); left_panel(d, 'החסרונות')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, box, 'u11_rough', dim=0.35, focus=(0.5, 0.45))
    for i, s in enumerate(['צורך חשמל ברציפות', 'דורש אחזקה, צפוי לתקלות', 'ירידה בערנות התצפית', 'לא מגיב לשינויי רוח', 'לא יעיל בים גבוה ובגלים מהירכתיים']):
        y = y0 + 60 + i * 190
        d.rounded_rectangle((x0 + 60, y, x1 - 60, y + 150), 24, fill=DARK, outline=CORAL, width=4)
        label(d, ((x0 + x1) / 2, y + 75), s, F(46), TEXT)
    right_block(d, 'כל התשובות', 'חשמל, תקלות, ירידה בערנות, ואין תגובה לשינויי רוח בשיט מפרשים.',
                ('שאלה מהמאגר · 29', 'מה הם חסרונותיו העיקריים של הגה אוטומטי חשמלי?',
                 ['צורך חשמל, דורש אחזקה, צפוי לתקלות', 'ירידה בערנות התצפית ובשיקולי ההגוי',
                  'אינו מגיב לשינויים ברוח בשיט מפרשים', 'כל התשובות נכונות'], 3))
    save(im, 's07_disadvantages_q29')

def s08():
    im, d = base(); left_panel(d, 'הגה רוח: זווית קבועה לרוח')
    box = inner(); x0, y0, x1, y1 = box
    sx = x0 + 560
    d, P = photo_map(im, (sx, y0, x1, y1), 'u11_aries', (0.6, 0.5))   # Alex's photo: windvane on the stern
    v = P(790, 110); tag(d, (v[0] - 40, v[1] + 260), 'כנף', ORANGE, 40); pointer(d, (v[0] - 40, v[1] + 220), v)
    bl = P(575, 525); tag(d, (bl[0] + 170, bl[1] + 150), 'הגה עזר במים', ORANGE, 36); pointer(d, (bl[0] + 120, bl[1] + 120), bl)
    d.rectangle((x0, y0, sx - 10, y1), fill=(10, 20, 34))
    for i, s in enumerate(['נועלים את הכנף בזווית לרוח', 'הסירה סוטה, הכנף נוטה', 'הגה העזר מסתובב', 'הסירה חוזרת לקורס']):
        y = y0 + 60 + i * 250
        box_text(d, (x0 + 30, y, sx - 40, y + 170), [(s, 36, GREEN_L)])
        if i < 3: arrow(d, ((x0 + sx) / 2 - 5, y + 175), ((x0 + sx) / 2 - 5, y + 245), WHITE, 6, 22)
    right_block(d, 'הגה רוח', 'מכני, בלי חשמל. לא יודע איפה הצפון, רק מאיפה הרוח.',
                ('שאלה מהמאגר · 17', 'על איזה קורס הפלגה שומר הגה רוח?',
                 ['קורס קבוע ביחס למים', 'זווית קבועה בין השדרה לרוח היחסית',
                  'קורס קבוע לפי מצפן שמחובר ל-GPS', 'פתיחה וסגירה של החלוץ לפי הרוח'], 1))
    save(im, 's08_windvane_q17')

def s09():
    im, d = base(); left_panel(d, 'הגה רוח: בעד ונגד')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, box, 'u11_aries', dim=0.32, focus=(0.55, 0.5))
    for j, (h, items, col) in enumerate([('בעד', ['לא צריך חשמל', 'שומר זווית לרוח', 'הכי יעיל ברוח צד'], GREEN_L),
                                         ('נגד', ['לא לספינות מנוע וכבדות', 'רוח משתנה = קורס משתנה', 'ברוח גבית: סכנת מהפך', 'דיוק נמוך'], CORAL)]):
        cx = x1 - 290 - j * 580
        label(d, (cx, y0 + 70), h, F(56), col)
        for i, s in enumerate(items):
            y = y0 + 150 + i * 170
            d.rounded_rectangle((cx - 260, y, cx + 260, y + 140), 22, fill=DARK, outline=col, width=4)
            label(d, (cx, y + 70), s, F(38, False), TEXT)
    right_block(d, 'כל התשובות', 'בלי חשמל, לא למנוע ולספינות כבדות, ומחייב ערנות לשינויי רוח.',
                ('שאלה מהמאגר · 30', 'ביחס להגה רוח סמן את המשפט שתוכנו נכון ביותר:',
                 ['לא תלוי בחשמל, שומר על הזווית לרוח', 'לא לספינות מנוע ולא לספינות כבדות',
                  'מחייב ערנות לשינויים ברוח', 'כל התשובות נכונות'], 3))
    save(im, 's09_windvane_q30')

def s10():
    im, d = base()
    d, P = contain(im, (0, 0, 1300, 1440), 'u11_p70', bg=(236, 238, 240))
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['הגה חשמלי: קורס לפי מצפן', 'AUTO: הפעלה · STANDBY: ידני', 'דיוק: מצפן ומהירות תגובה', 'יתרון: משמרות נוחות ותצפית',
             'חיסרון: חשמל, בעיקר בים סוער', 'תקלות, ירידה בערנות, לא מגיב לרוח', 'הגה רוח: זווית קבועה לרוח', 'בלי חשמל, אבל דורש ערנות']
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 6 else ORANGE)
        text_r(d, 2380, y + 20, s, F(48, False), TEXT)
    save(im, 's10_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10]
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
