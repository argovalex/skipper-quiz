"""Lesson 8 (l30): מד עומק. Realistic photos (assets/u8_*.jpg, Higgsfield nano_banana) with drawn overlays."""
import math, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U6 = _load('u06', 'u06_cards.py'); U7 = _load('u07', 'u07_cards.py')
from PIL import Image, ImageDraw, ImageEnhance
import real as RL
C.OUT = os.path.join(HERE, '..', 'cards', 'מד עומק'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · מד עומק'
F, text_c, text_r, label, dot, arrow = C.F, C.text_c, C.text_r, C.label, C.dot, C.arrow
base, left_panel, right_block, save, RC = C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, ORANGE, CORAL, GREEN, GREEN_L, BLUE_L, PANEL, MUTED = C.TEXT, C.ORANGE, C.CORAL, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL, C.MUTED
readout, inner, WHITE = U5.readout, U5.inner, U5.WHITE
photo, tag = U7.photo, U7.tag
DARK = (8, 14, 22)

def photo_map(im, box, name, focus=(0.5, 0.5), dim=1.0):
    """Like photo(), but also returns a function mapping original-image pixels to card coordinates."""
    d = photo(im, box, name, dim=dim, focus=focus)
    g = Image.open(os.path.join(RL.A, name + '.jpg')); x0, y0, x1, y1 = [int(v) for v in box]; W, H = x1 - x0, y1 - y0
    s = max(W / g.width, H / g.height); gw, gh = math.ceil(g.width * s), math.ceil(g.height * s)
    cx = min(max(int(gw * focus[0] - W / 2), 0), gw - W); cy = min(max(int(gh * focus[1] - H / 2), 0), gh - H)
    return d, lambda ox, oy: (x0 + ox * s - cx, y0 + oy * s - cy)

def dashed(d, a, b, col, w=5, dash=24):
    L = math.dist(a, b); n = max(1, int(L / dash))
    for i in range(0, n, 2):
        p = (a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n)
        q = (a[0] + (b[0] - a[0]) * min(i + 1, n) / n, a[1] + (b[1] - a[1]) * min(i + 1, n) / n)
        d.line((p, q), fill=col, width=w)

def bracket(d, x, ya, yb, col, w=7):
    d.line(((x, ya), (x, yb)), fill=col, width=w)
    for y in (ya, yb): d.line(((x - 18, y), (x + 18, y)), fill=col, width=w)

def box_text(d, box, lines, outline=GREEN_L):
    d.rounded_rectangle(box, 24, fill=DARK, outline=outline, width=4)
    cx = (box[0] + box[2]) / 2; h = (box[3] - box[1]) / len(lines)
    for i, (s, size, col) in enumerate(lines): label(d, (cx, box[1] + h * (i + 0.5)), s, F(size), col)

# hero photo landmarks (original px of u8_hero.jpg)
WL, KEEL, SEABED, XDUCER = 1215, 1692, 2010, (845, 1458)
HERO_FOCUS = (0.5, 0.64)

def depth_scene(im, box, draft, meas, tide=None, chart=None, datum=True):
    """Hero photo with brackets: draft (waterline→keel), measured (keel→seabed); tide + chart depth from the low-tide datum."""
    d, P = photo_map(im, box, 'u8_hero', HERO_FOCUS)
    x0, y0, x1, y1 = box
    wl, kl, sb = P(0, WL)[1], P(0, KEEL)[1], P(0, SEABED)[1]
    dashed(d, P(1070, KEEL), (x1 - 20, kl), WHITE, 4)
    d.line(((x0, sb), (x1, sb)), fill=(240, 200, 120), width=5)
    xa = x1 - 300
    bracket(d, xa, wl, kl, ORANGE); tag(d, (xa - 30, (wl + kl) / 2), draft, ORANGE, 36, 'r')
    bracket(d, xa, kl, sb, GREEN_L); tag(d, (xa - 30, (kl + sb) / 2), meas, GREEN_L, 36, 'r')
    if datum:
        dy = wl + 70
        dashed(d, (x0, dy), (x1, dy), CORAL, 5)
        tag(d, (x0 + 30, dy + 46), 'שפל · Chart Datum', CORAL, 30, 'l')
        xb = x1 - 90
        bracket(d, xb, wl, dy, CORAL);
        if tide: tag(d, (xb, wl - 46), tide, CORAL, 34)
        bracket(d, xb, dy, sb, BLUE_L)
        if chart: tag(d, (xb - 10, (dy + sb) / 2 + 60), chart, BLUE_L, 34, 'r')
    tag(d, (x0 + 30, wl - 46), 'פני המים', WHITE, 30, 'l')
    return d, sb

def hide_hole(im, P, c, r):
    """Clone hull from the left over a hole in the photo (soft elliptical mask)."""
    from PIL import ImageFilter
    a = P(c[0] - r, c[1] - r); b = P(c[0] + r, c[1] + r); w = int(b[0] - a[0]); h = int(b[1] - a[1])
    src = im.crop((int(a[0]) - int(w * 1.6), int(a[1]), int(a[0]) - int(w * 1.6) + w, int(a[1]) + h))
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).ellipse((4, 4, w - 4, h - 4), fill=255); m = m.filter(ImageFilter.GaussianBlur(5))
    im.paste(src, (int(a[0]), int(a[1])), m)

def transducer(d, P, bottom):
    """Small flush transducer fairing on the hull bottom; returns its face point."""
    a = P(bottom[0] - 38, bottom[1] - 14); b = P(bottom[0] + 38, bottom[1] + 16)
    d.rounded_rectangle((a[0], a[1], b[0], b[1]), 8, fill=(20, 22, 26), outline=(70, 75, 85), width=2)
    return ((a[0] + b[0]) / 2, b[1])

def tilt_inset(im, c, r, src):
    """Zoom circle: transducer on the hull bottom, vertical vs. tilted axis, max 10 degrees."""
    S = 2 * r; z = Image.new('RGB', (S, S), (150, 195, 215)); g = ImageDraw.Draw(z)
    hy = r - 10
    g.rectangle((0, 0, S, hy), fill=(235, 238, 240)); g.line(((0, hy), (S, hy)), fill=(30, 120, 200), width=6)
    g.rounded_rectangle((r - 30, hy - 6, r + 30, hy + 18), 6, fill=(20, 22, 26))
    for k in range(1, 4):
        rr = 25 + k * 28; g.arc((r - rr, hy + 18 - rr * 0.55, r + rr, hy + 18 + rr * 0.55), 55, 125, fill=(20, 40, 120), width=4)
    dashed(g, (r, hy - 120), (r, hy + 130), (60, 60, 60), 3, 12)
    dx = math.tan(math.radians(10)) * 125
    g.line(((r - dx, hy + 125), (r + dx, hy - 125)), fill=(200, 30, 40), width=4)
    label(g, (r + 30, hy - 95), '10° max', F(28), (200, 30, 40), 'l')
    m = Image.new('L', (S, S), 0); ImageDraw.Draw(m).ellipse((0, 0, S - 1, S - 1), fill=255)
    d = ImageDraw.Draw(im); d.line((src, (c[0] - r * 0.7, c[1] + r * 0.7)), fill=ORANGE, width=4)
    im.paste(z, (int(c[0] - r), int(c[1] - r)), m); d = ImageDraw.Draw(im)
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), outline=ORANGE, width=6)
    tag(d, (c[0], c[1] + r + 40), 'סטייה מהאנך: עד 10°', ORANGE, 32)
    return d
# ---------- cards ----------
def s01():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u8_hero', focus=(0.5, 0.55))
    readout(d, (60, 1120, 500, 1380), 'DEPTH', '10.0 m')
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 8', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'מד עומק', F(130), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['חבל ומשקולת', 'עקרון ההד', 'התקנה ואחזקה של הממיר', 'עומק, שוקע וגאות']):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    im, d = base(); left_panel(d, 'מד עומק ידני')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, box, 'u8_lead_line', focus=(0.62, 0.62))
    tag(d, (x0 + 300, y0 + 380), 'סימון כל מטר', CORAL)
    tag(d, (x1 - 200, y1 - 330), 'משקולת', WHITE)
    tag(d, ((x0 + x1) / 2, y1 - 60), 'רדוד: חבל · עמוק: המפה', GREEN_L, 46)
    right_block(d, 'חבל ומשקולת', 'מורידים את החבל עד שהמשקולת נוגעת בקרקעית, וקוראים כמה מטרים ירדו למים.',
                ('שאלה מהמאגר · 40', 'אילו חלופות אפשריות להערכת העומק כשאין מד עומק או שהוא אינו תקין? סמן את התשובה המעשית ביותר.',
                 ['להזין ל-GPS את ה-Chart Datum ולהפעיל 3D', 'לחפש את תאור האזור בספר חופאות',
                  'רדוד: חבל עם משקולת. עמוק: חישוב מהמפה', 'לשוט עם עוגן מורד 1-2 מ׳ מתחת לשוקע'], 2))
    save(im, 's02_lead_line_q40')

def s03():
    im, d = base(); left_panel(d, 'בטיחות · ניווט · עגינה')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, box, 'u8_anchoring', focus=(0.45, 0.55))
    tag(d, (x0 + 220, y0 + 80), 'בטיחות', GREEN_L, 46); tag(d, ((x0 + x1) / 2, y0 + 80), 'ניווט', GREEN_L, 46); tag(d, (x1 - 200, y0 + 80), 'עגינה', GREEN_L, 46)
    tag(d, ((x0 + x1) / 2, y1 - 60), 'גם בשאלה 35: לבטיחות השייט, ניווט ועגינה', ORANGE, 38)
    right_block(d, 'שימושים', 'בטיחות, ניווט ועגינה. תשובה עם "בלבד" שגויה. צוללות ולהקות דגים, זה סונאר.',
                ('שאלה מהמאגר · 31', 'מהם שימושי מד עומק הדי (ECHO SOUNDER)?',
                 ['בטיחות השיט, נווט, ניתוב, עגינה', 'דייג, מיפוי ולוחמה ימית',
                  'מכשולים, צוללות, להקות דגים', 'אף תשובה לא נכונה'], 0))
    save(im, 's03_uses_q31_q35')

def s04():
    im, d = base(); left_panel(d, 'שולח קול, מחכה להד')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, box, 'u8_hero', HERO_FOCUS)
    t = P(*XDUCER); sb = P(0, SEABED)[1]
    for k in range(1, 5):
        r = k * 70; yy = t[1] + k * 80
        d.arc((t[0] - r, yy - r * 0.5, t[0] + r, yy + r * 0.5), 20, 160, fill=ORANGE, width=6)
    arrow(d, (t[0] - 40, t[1] + 30), (t[0] - 40, sb - 10), ORANGE, 9, 34)
    arrow(d, (t[0] + 40, sb - 10), (t[0] + 40, t[1] + 30), GREEN_L, 9, 34)
    tag(d, (t[0] - 70, (t[1] + sb) / 2 + 120), 'פולס', ORANGE, 38, 'r'); tag(d, (t[0] + 70, (t[1] + sb) / 2 + 120), 'הד', GREEN_L, 38, 'l')
    tag(d, (t[0] - 60, t[1] - 50), 'ממיר', WHITE, 36, 'r')
    box_text(d, (x0 + 60, y1 - 210, x1 - 60, y1 - 20), [('S = V × T', 64, TEXT), ('עומק = מהירות הקול × זמן ÷ 2', 44, GREEN_L)])
    right_block(d, 'עקרון ההד', 'הממיר הופך פולס חשמלי לגל קול. הקול פוגע בקרקעית וחוזר. המכשיר מודד את הזמן, ומחלק בשתיים כי הקול עשה את הדרך פעמיים. רק כשההד חזר, יוצא הפולס הבא.')
    save(im, 's04_echo_principle')

def s05():
    im, d = base(); left_panel(d, 'הממיר עובד בשני הכיוונים')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, (x0, y0, x1, y0 + 760), 'u8_hull_xducer', (0.45, 0.5))
    hide_hole(im, P, (1176, 902), 52); d = ImageDraw.Draw(im)
    t = transducer(d, P, (1056, 952))
    for k in range(1, 5):
        r = 40 + k * 55; d.arc((t[0] - r, t[1] - r * 0.55, t[0] + r, t[1] + r * 0.55), 50, 130, fill=ORANGE, width=6)
    tag(d, (t[0] - 60, t[1] - 70), 'ממיר בתחתית', ORANGE, 40, 'r')
    d = tilt_inset(im, (x1 - 200, y0 + 200), 175, t)
    for i, (a, b, col) in enumerate([('שידור', 'חשמל → קול', ORANGE), ('קליטה', 'קול → חשמל', GREEN_L)]):
        bx0 = x0 + 40 + (1 - i) * ((x1 - x0 - 100) / 2 + 20); bw = (x1 - x0 - 100) / 2
        box_text(d, (bx0, y0 + 800, bx0 + bw, y1 - 20), [(a, 48, MUTED), (b, 56, col)], col)
    right_block(d, 'תפקיד הממיר', 'בשידור הופך חשמל לקול. בקליטה הופך את ההד בחזרה לחשמל.',
                ('שאלה מהמאגר · 165', 'מה תפקיד הממיר במד העומק?',
                 ['פולס רדיו לקול בשידור, הד לרדיו בקליטה', 'לעצב את האלומה רק מתחת לסירה',
                  'לסרוק חתך עומק ולתת כיוונים לעצמים', 'א ו-ג נכונות'], 0))
    save(im, 's05_transducer_q165')

def s06():
    im, d = base(); left_panel(d, 'מכיילים לשוקע המרבי')
    box = inner(); x0, y0, x1, y1 = box
    d, sb = depth_scene(im, box, 'שוקע', 'מוצג', datum=False)
    d.rounded_rectangle((x1 - 370, y0 + 10, x1 - 10, y0 + 370), 20, fill=WHITE)
    d = photo(im, (x1 - 360, y0 + 20, x1 - 20, y0 + 360), 'u8_clipper')   # Alex's photo: depth display + transducer
    tag(d, (x1 - 190, y0 + 400), 'תצוגה וממיר', WHITE, 34)
    tag(d, ((x0 + x1) / 2, y1 - 50), 'חשוב: אלומה בלי בועות ובלי עצמים בדרך', ORANGE, 38)
    right_block(d, 'איפה הממיר', 'לא משנה באיזה עומק. מכיילים את התצוגה, והיא מציגה עומקים מנקודת השוקע המרבי.',
                ('שאלה מהמאגר · 32', 'היכן מותקן הממיר של מד העומק הדי?',
                 ['בקו המים, בציפה מרבית', 'בנקודה העמוקה ביותר, בטעינה מרבית',
                  'בחרטום, בזווית קדימה', 'אין חשיבות לעומק, מכיילים לשוקע המרבי'], 3))
    save(im, 's06_transducer_q32')

def s07():
    im, d = base(); left_panel(d, 'אחזקת הממיר')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle((x0, y0, x1, y0 + 620), fill=WHITE)
    px = x1 - 640; d = photo(im, (px, y0 + 10, px + 600, y0 + 610), 'u8_clipper')   # Alex's photo: depth display + transducer
    t = (px + 0.45 * 600, y0 + 10 + 0.88 * 600)
    arrow(d, (x0 + 380, t[1] - 40), (t[0] - 60, t[1] - 10), ORANGE, 8, 30)
    tag(d, (x0 + 230, t[1] - 110), 'פני הממיר', ORANGE, 40)
    tag(d, (x0 + 270, y0 + 120), 'לשמור נקי', GREEN_L, 44); tag(d, (x0 + 270, y0 + 230), 'בלי צבע מתכתי', GREEN_L, 44)
    for i, (n, s) in enumerate([('33', 'להסיר בעדינות צמחיה וחי ימי'), ('34', 'לצבוע בחומר בלי מתכת'), ('176', 'קרמי טבול בשמן: להשלים שמן')]):
        y = y0 + 660 + i * 130
        d.rounded_rectangle((x0 + 30, y, x1 - 30, y + 112), 22, fill=PANEL, outline=GREEN_L, width=3)
        label(d, (x1 - 90, y + 56), n, F(46), MUTED); label(d, (x1 - 170, y + 56), 'ב · ' + s, F(44), GREEN_L, 'r')
    right_block(d, 'אחזקה', 'שלוש שאלות עם אותו נוסח, ובכולן התשובה ב. ממיר נקי, ניקוי עדין, ובלי צבע עם מתכת.',
                ('שאלה מהמאגר · 33', 'כיצד יש לטפל בממיר מד העומק?',
                 ['ליטוש וצבע שמכיל מתכת', 'להסיר בעדינות צמחיה וחי ימי',
                  'להשאיר חשוף ולחדש מגנטיות במגנט', 'אין לבצע כל פעולת אחזקה'], 1))
    save(im, 's07_care_q33_34_176')

def s08():
    im, d = base(); left_panel(d, 'מה משפיע על הדיוק')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, (x0, y0, x1, y0 + 560), 'u8_echo_display', focus=(0.48, 0.3))
    for i, s in enumerate(['טמפרטורת המים', 'מליחות המים', 'אורך הפולס']):
        y = y0 + 600 + i * 120
        d.rounded_rectangle((x0 + 30, y, x1 - 30, y + 102), 22, fill=PANEL, outline=GREEN_L, width=3)
        label(d, ((x0 + x1) / 2, y + 51), 'משפיע · ' + s, F(46), GREEN_L)
    y = y0 + 960
    d.rounded_rectangle((x0 + 30, y, x1 - 30, y + 90), 22, fill=DARK, outline=CORAL, width=4)
    label(d, ((x0 + x1) / 2, y + 45), 'שדה חשמלי מלוח ההגה: לא קיים', F(44), CORAL)
    right_block(d, 'דיוק', 'מהירות הקול במים משתנה לפי טמפרטורה ומליחות. גם אורך הפולס משפיע.',
                ('שאלה מהמאגר · 37', 'ממה לא מושפע הדיוק במד עומק?',
                 ['מטמפרטורת המים', 'ממליחות המים', 'מאורך הפולס', 'מהשדה החשמלי מחיכוך לוח ההגה'], 3))
    save(im, 's08_accuracy_q37')

def s09():
    im, d = base(); left_panel(d, 'טווח גדול, פחות פולסים')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, box, 'u8_echo_display', dim=0.3, focus=(0.48, 0.3))
    for r, (title, n) in enumerate([('טווח קטן', 8), ('טווח גדול', 3)]):
        ty = y0 + 120 + r * 470
        label(d, (x1 - 60, ty), title, F(54), TEXT, 'r')
        ax0, ax1, ay = x0 + 60, x1 - 60, ty + 230
        d.line(((ax0, ay), (ax1, ay)), fill=MUTED, width=4)
        step = (ax1 - ax0) / n
        for k in range(n):
            px = ax1 - k * step - 20                        # time runs right to left
            d.line(((px, ay), (px, ay - 140)), fill=ORANGE, width=10)
            ex = px - step * 0.85
            d.line(((ex, ay), (ex, ay - 80)), fill=GREEN_L, width=8)
            if k == 0: d.arc((ex - 4, ay - 200, px + 4, ay - 40), 200, 340, fill=WHITE, width=3)
        label(d, ((x0 + x1) / 2, ay + 60), f'{n} פולסים', F(44), ORANGE)
    label(d, (x1 - 60, y1 - 60), 'כתום: פולס · ירוק: הד', F(38, False), MUTED, 'r')
    right_block(d, 'טווח ופולסים', 'הפולס הבא יוצא רק כשההד חזר. בטווח גדול ההמתנה ארוכה יותר, ולכן יש פחות פולסים בשנייה.',
                ('שאלה מהמאגר · 135', 'כאשר מגדילים את טווח העומק במכשיר מד עומק אז:',
                 ['משודרים יותר פולסים ביחידת זמן', 'משודרים פחות פולסים ביחידת זמן', 'אין שינוי',
                  'תדירות זהה, אורך הפולס משתנה'], 1))
    save(im, 's09_range_q135')

def s10():
    im, d = base(); left_panel(d, 'עומק נמדד, שוקע וגאות')
    box = inner(); x0, y0, x1, y1 = box
    d, sb = depth_scene(im, box, 'שוקע', 'עומק נמדד', 'גאות', 'עומק במפה')
    box_text(d, (x0 + 30, y1 - 250, x1 - 350, y1 - 20), [('עומק מים = עומק נמדד + שוקע', 46, TEXT), ('עומק במפה = עומק מים − גאות', 46, BLUE_L)], BLUE_L)
    right_block(d, 'החשבון', 'מד העומק מודד מתחת לממיר. עומק המים = עומק נמדד + שוקע. העומק במפה מצוין בשפל, אז: עומק במפה = עומק מים פחות גאות.')
    save(im, 's10_depth_formula')

def s11():
    im, d = base(); left_panel(d, '10 + 2 − 1 = 11')
    box = inner(); x0, y0, x1, y1 = box
    d, sb = depth_scene(im, box, 'שוקע 2 m', 'מד העומק 10 m', 'גאות 1 m', 'במפה ?')
    box_text(d, (x0 + 30, y1 - 250, x1 - 350, y1 - 20), [('10 + 2 = 12 m מים', 50, TEXT), ('12 − 1 = 11 m במפה', 56, GREEN_L)])
    right_block(d, 'חישוב', 'מוסיפים את השוקע, מחסירים את הגאות.',
                ('שאלה מהמאגר · 38', 'מה יהיה העומק שצריך להופיע במפה כאשר מד העומק מראה 10 מטרים, שוקע ספינתך 2 מטרים והגאות היא של 1 מטר?',
                 ['13 מטרים', '10 מטרים', '9 מטרים', '11 מטרים'], 3))
    save(im, 's11_depth_q38')

def s12():
    im, d = base(); left_panel(d, 'מאיפה ההבדל')
    box = inner(); x0, y0, x1, y1 = box
    d, sb = depth_scene(im, box, 'שוקע 1.2 m', 'מד העומק 12 m', 'גאות ?', 'במפה 10 m')
    box_text(d, (x0 + 30, y1 - 300, x1 - 350, y1 - 20), [('12 + 1.2 = 13.2 m מים', 46, TEXT), ('36 · מפה 10  →  גאות 3.2 m', 48, GREEN_L), ('39 · מפה 10.8  →  גאות 2.4 m', 48, GREEN_L)])
    right_block(d, 'שתי שאלות', 'אותו נוסח, מספרים אחרים. בשתיהן התשובה ג: המפה בשפל, ועכשיו יש גאות.',
                ('שאלה מהמאגר · 36', 'נמדד במד העומק 12 מטרים, במפה מצוין 10 מטרים, שוקע הספינה 1.2 מטרים. ממה נובע ההבדל?',
                 ['אורך הפולס לא מאפשר דיוק כזה', 'גלים בגובה ממוצע של 1.2 מ׳',
                  'המפה בשיא השפל, ועכשיו גאות 3.2 מ׳', 'המפה בשיא הגאות, הממיר בקו המים'], 2))
    save(im, 's12_depth_q36_q39')

def s13():
    im, d = base(); left_panel(d, 'המכשיר מכויל לשוקע')
    box = inner(); x0, y0, x1, y1 = box
    d, sb = depth_scene(im, box, 'שוקע 1.5 m', 'מד העומק 1 m', 'גאות ?', 'במפה 2 m')
    box_text(d, (x0 + 30, y1 - 250, x1 - 350, y1 - 20), [('1 + 1.5 = 2.5 m מים', 50, TEXT), ('2.5 − 2 = 0.5 m גאות', 56, GREEN_L)])
    right_block(d, 'מכויל', 'המכשיר מציג עומק מתחת לשוקע. מוסיפים שוקע, ומשווים למפה.',
                ('שאלה מהמאגר · 178', 'מד העומק מציג מנקודת השוקע המרבי. שוקע 1.5 מטרים, נמדד 1 מטר, במפה 2 מטרים. מה הסיבה להבדל?',
                 ['המפה בשיא הגאות, ועכשיו שפל 0.5 מ׳', 'המפה בשיא השפל, ועכשיו גאות 0.5 מ׳',
                  'הקרקעית גבוהה ב-0.5 מ׳ מה-Chart Datum', 'ב ו-ג נכונות'], 1))
    save(im, 's13_depth_q178')

def s14():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u8_echo_display', focus=(0.45, 0.4))
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['קול למטה, הד למעלה, זמן ÷ 2', 'ממיר: חשמל לקול, קול לחשמל', 'עומק ההתקנה לא משנה: מכיילים', 'ממיר נקי, בלי צבע מתכתי',
             'טמפרטורה, מליחות, פולס: משפיעים', 'טווח גדול = פחות פולסים', 'עומק מים = נמדד + שוקע', 'עומק במפה: תמיד בשפל']
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 6 else ORANGE)
        text_r(d, 2380, y + 20, s, F(48, False), TEXT)
    save(im, 's14_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14]
sheet = lambda: U6.sheet.__globals__.__setitem__('C', C) or U6.sheet()

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only: fn()
    sheet()
