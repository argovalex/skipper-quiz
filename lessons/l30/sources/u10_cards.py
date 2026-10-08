"""Lesson 10 (l30): מכ״מ יחסי. Realistic photos (assets/u10_*.jpg, Higgsfield nano_banana) + drawn radar screens."""
import math, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U6 = _load('u06', 'u06_cards.py')
U7 = _load('u07', 'u07_cards.py'); U8 = _load('u08', 'u08_cards.py'); U9 = _load('u09', 'u09_cards.py')
from PIL import Image, ImageDraw
C.OUT = os.path.join(HERE, '..', 'cards', 'מכ״מ יחסי'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · מכ״מ יחסי'
F, text_c, text_r, label, dot, arrow = C.F, C.text_c, C.text_r, C.label, C.dot, C.arrow
base, left_panel, right_block, save, RC = C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, ORANGE, CORAL, GREEN, GREEN_L, BLUE_L, PANEL, MUTED = C.TEXT, C.ORANGE, C.CORAL, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL, C.MUTED
readout, inner, WHITE, polar_pt = U5.readout, U5.inner, U5.WHITE, U5.polar_pt
photo, tag, photo_map, dashed, box_text, DARK = U8.photo, U8.tag, U8.photo_map, U8.dashed, U8.box_text, U8.DARK
ppi, blip, ECHO = U9.ppi, U9.blip, U9.ECHO
STB, PRT = (40, 200, 80), (225, 50, 50)
BG = (10, 20, 34)

def ppi_head(d, c, r, head, north=None, rings=3):
    """Radar screen with heading line at `head` (deg, screen-up = 0) and an optional north marker."""
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=(6, 22, 14), outline=(60, 160, 90), width=4)
    for k in range(1, rings): rr = r * k / rings; d.ellipse((c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr), outline=(40, 110, 60), width=2)
    d.line((c, polar_pt(c, r, head)), fill=ORANGE, width=4); dot(d, c, 9, WHITE)
    if north is not None:
        n = polar_pt(c, r + 34, north); label(d, n, 'N', F(34), BLUE_L)

def coast(d, c, r, rot):
    """A coastline blob on a radar screen, rotated by rot degrees."""
    pts = [polar_pt(c, r * k, a + rot) for a, k in ((300, .95), (315, .7), (330, .62), (345, .66), (0, .58), (15, .7), (30, .95))]
    d.line(pts, fill=ECHO, width=12, joint='curve')

# ---------- cards ----------
def s01():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u10_ship', focus=(0.72, 0.5))
    readout(d, (60, 1120, 500, 1380), 'REL BRG · RANGE', 'G 030 · 2 NM')
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 10', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'מכ״מ יחסי', F(130), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['ירוק ואדום: כיוון יחסי', 'תמונה יחסית ותמונה אמיתית', 'סכנת התנגשות', 'אנטנה ומחזיר הד']):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    im, d = base(); left_panel(d, 'כיוון יחסי: ביחס לחרטום')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=BG)
    c = ((x0 + x1) / 2, (y0 + y1) / 2 + 20); r = 400
    d.arc((c[0] - r, c[1] - r, c[0] + r, c[1] + r), 270, 450, fill=STB, width=14)     # starboard half
    d.arc((c[0] - r, c[1] - r, c[0] + r, c[1] + r), 90, 270, fill=PRT, width=14)
    U7.sailboat_top(im, (c[0], c[1] - 150), 0, 300); d = ImageDraw.Draw(im)
    for a in range(0, 181, 30):
        for sgn, col, nm in ((1, STB, 'ירוק'), (-1, PRT, 'אדום')):
            if sgn == -1 and a in (0, 180): continue
            p = polar_pt(c, r + 60, sgn * a); q1, q2 = polar_pt(c, r - 20, sgn * a), polar_pt(c, r + 20, sgn * a)
            d.line((q1, q2), fill=WHITE, width=4)
            s = '0' if a == 0 else ('180' if a == 180 else f'{nm} {a}')
            label(d, p, s, F(30), WHITE if a in (0, 180) else col)
    t = polar_pt(c, r * 0.8, 30); blip(d, t); dashed(d, c, t, STB, 4)
    tag(d, (t[0] + 20, t[1] - 60), 'מטרה בירוק 30', STB, 32, 'l')
    right_block(d, 'ירוק ואדום', 'החרטום הוא אפס. סופרים לכל צד עד 180. ימין = ירוק, שמאל = אדום, כמו אורות הדופן.')
    save(im, 's02_relative_bearings')

def s03():
    im, d = base(); left_panel(d, 'תמונה אמיתית מול יחסית')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=BG)
    course = 60
    for j, (title, sub, head, north, rot, col) in enumerate([('תמונה אמיתית', 'צפון למעלה · החרטום זז', course, 0, 0, BLUE_L),
                                                              ('תמונה יחסית', 'חרטום למעלה · העולם זז', 0, -course, -course, ORANGE)]):
        c = (x1 - 290 - j * 590, y0 + 470); r = 240
        ppi_head(d, c, r, head, north); coast(d, c, r, rot); blip(d, polar_pt(c, r * 0.55, 150 + rot), 14, 9)
        label(d, (c[0], y0 + 110), title, F(48), col); label(d, (c[0], y0 + 170), sub, F(34, False), TEXT)
    box_text(d, (x0 + 30, y1 - 250, x1 - 30, y1 - 20), [('אמיתית: יש נתון מהמצפן · כיוונים אמיתיים', 38, BLUE_L), ('יחסית: אין מצפן · כיוונים ביחס לחרטום', 38, ORANGE)], BLUE_L)
    right_block(d, 'שתי תצוגות', 'אותה סירה, אותו מקום. באמיתית החרטום מסתובב, ביחסית העולם מסתובב. קורס 060 בשתיהן.')
    save(im, 's03_head_up_north_up')

def rose(d, c, r, course, rel, side):
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), outline=MUTED, width=3)
    label(d, polar_pt(c, r + 30, 0), 'N', F(32), BLUE_L)
    tb = (course + side * rel) % 360; col = STB if side > 0 else PRT
    a0, a1 = sorted((course - 90, tb - 90)) if abs(course - tb) < 180 else (max(course, tb) - 90, min(course, tb) + 270)
    d.arc((c[0] - r * 0.45, c[1] - r * 0.45, c[0] + r * 0.45, c[1] + r * 0.45), a0, a1, fill=col, width=10)
    arrow(d, c, polar_pt(c, r, course), ORANGE, 8, 28); d.line((c, polar_pt(c, r, tb)), fill=col, width=6); blip(d, polar_pt(c, r, tb), 14, 9, col)
    label(d, polar_pt(c, r + 40, tb), f'{tb:03d}', F(32), col)
    label(d, polar_pt(c, r + 34, course), f'{course:03d}', F(30), ORANGE)
    return tb

def s04():
    im, d = base(); left_panel(d, 'מיחסי לאמיתי')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=BG)
    for j, (course, rel, side, calc) in enumerate([(350, 30, -1, ['אדום 30 · מפחיתים', '350 − 30 = 320']),
                                                     (280, 90, 1, ['ירוק 90 · מוסיפים', '280 + 90 = 370', '370 − 360 = 010'])]):
        c = (x1 - 290 - j * 590, y0 + 330); r = 210
        rose(d, c, r, course, rel, side)
        for i, s in enumerate(calc):
            label(d, (c[0], y0 + 640 + i * 80), s, F(46 if i else 42), (STB if side > 0 else PRT) if i == 0 else TEXT)
    box_text(d, (x0 + 30, y1 - 190, x1 - 30, y1 - 20), [('קורס ± כיוון יחסי = כיוון אמיתי', 50, GREEN_L)])
    right_block(d, 'החישוב', 'ירוק: מוסיפים לקורס. אדום: מפחיתים. עברת 360? מורידים 360.')
    save(im, 's04_true_bearing_calc')

def s05():
    im, d = base(); left_panel(d, 'שאלה מהמבחן')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=BG)
    for j, (title, rel) in enumerate([('קורס 180', 30), ('קורס 150', 60)]):
        c = (x1 - 290 - j * 590, y0 + 380); r = 240
        ppi_head(d, c, r, 0, rings=3)
        t = polar_pt(c, r * 2 / 3, rel); blip(d, t); dashed(d, c, t, STB, 3)
        label(d, (c[0], y0 + 90), title, F(50), ORANGE)
        tag(d, (c[0], c[1] + r + 60), f'ירוק {rel} · 2 מייל', STB, 40)
    arrow(d, (x0 + 640, y0 + 380), (x0 + 560, y0 + 380), WHITE, 6, 26)
    box_text(d, (x0 + 30, y1 - 300, x1 - 30, y1 - 20), [('פנית 30° שמאלה: המטרה זזה 30° ימינה', 40, TEXT), ('180 + 30 = 210 אמיתי', 42, BLUE_L), ('210 − 150 = ירוק 60', 46, GREEN_L)])
    right_block(d, 'המטרה לא זזה', 'אתה מפליג בכיוון אמיתי 180 עם מכ״מ יחסי, מטרה בירוק 30 בטווח 2 מייל. משנה ל-150. היכן תראה את המטרה? ירוק 60, עדיין 2 מייל.')
    save(im, 's05_exam_turn')

def s06():
    im, d = base(); left_panel(d, 'כיוון קבוע, טווח נסגר')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, (x0, y0, x1, y0 + 700), 'u10_ship', (0.6, 0.5))
    tag(d, (x1 - 220, y0 + 60), 'כיוון לא משתנה', ORANGE, 40); tag(d, (x0 + 220, y0 + 60), 'הטווח נסגר', CORAL, 40)
    for i, (t, b, rg) in enumerate([('12:00', '045°', '3.0'), ('12:06', '045°', '2.2'), ('12:12', '045°', '1.4')]):
        y = y0 + 730 + i * 95
        d.rounded_rectangle((x0 + 30, y, x1 - 30, y + 82), 18, fill=PANEL)
        label(d, (x1 - 120, y + 41), t, F(40), MUTED); label(d, ((x0 + x1) / 2, y + 41), b, F(44), ORANGE); label(d, (x0 + 180, y + 41), rg + ' NM', F(44), CORAL)
    right_block(d, 'סכנת התנגשות', 'שני סימנים: הטווח נסגר, והכיוון למטרה לא משתנה.',
                ('שאלה מהמאגר · 189', 'מתי אפשר לקבוע על-פי המכ״ם שספינתך נתונה בסכנת התנגשות?',
                 ['טווח קבוע והתכווין משתנה', 'תכווין קבוע והטווח קטן', 'תכווין קבוע והטווח גדל', 'המטרה מתקרבת בקצב קבוע'], 1))
    save(im, 's06_collision_q189')

def s07():
    im, d = base(); left_panel(d, 'הקו עובר דרך המרכז')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=BG)
    c = ((x0 + x1) / 2, y0 + 470); r = 400
    ppi_head(d, c, r, 0, rings=4)
    pts = [polar_pt(c, r * k, 45) for k in (0.9, 0.7, 0.5)]
    dashed(d, pts[0], polar_pt(c, r * 0.15, 45), ORANGE, 5)
    for p, tm in zip(pts, ('12:00', '12:06', '12:12')):
        blip(d, p, 15, 10); tag(d, (p[0] + 30, p[1] + 10), tm, WHITE, 30, 'l')
    tag(d, (c[0] - 40, c[1] + 70), 'מרכז = אתה', WHITE, 34, 'r')
    box_text(d, (x0 + 30, y1 - 160, x1 - 30, y1 - 20), [('מסמנים כל כמה דקות ומחברים לקו', 42, ORANGE)], ORANGE)
    right_block(d, 'שרטוט על המסך', 'אם קו הנקודות עובר דרך המרכז או קרוב אליו, המטרה בדרך אליך.',
                ('שאלה מהמאגר · 81', 'מה צריך כדי לזהות במכ״מ סכנת התנגשות?',
                 ['קו הנקודות עובר ליד מרכז המכ״מ', 'שרטוט בדף תנועה יחסית או במפה',
                  'מכ״מ מתקדם: המחשב מציג את התנועה', 'כל התשובות נכונות'], 3))
    save(im, 's07_plot_q81')

def s08():
    im, d = base(); left_panel(d, 'בלי מכ״מ: מצפן ושעון')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, (x0, y0, x1, y0 + 700), 'u10_compass_ship', (0.55, 0.45))
    s = P(780, 632); tag(d, (s[0], s[1] - 80), 'הספינה הנבדקת', WHITE, 34)
    cp = P(1380, 500); tag(d, (cp[0] + 120, cp[1] - 140), 'מצפן תכווינים', ORANGE, 36)
    for i, (t, b) in enumerate([('12:00', '045°'), ('12:06', '045°'), ('12:12', '045°')]):
        bw = (x1 - x0 - 100) / 3; bx = x1 - 30 - (i + 1) * bw - i * 20
        box_text(d, (bx, y0 + 730, bx + bw, y0 + 880), [(t, 36, MUTED), (b, 46, ORANGE)], ORANGE)
    box_text(d, (x0 + 30, y0 + 900, x1 - 30, y1 - 10), [('כיוון קבוע ומתקרב: סכנה', 48, CORAL)], CORAL)
    right_block(d, 'בעין', 'לוקחים כיוון במצפן, לפחות שלוש פעמים, ורושמים שעה. כיוון יחסי לא מספיק: הוא משתנה גם כשאתה זז.',
                ('שאלה מהמאגר · 23', 'מה דרוש לבדיקת סכנת התנגשות עם כלי שיט בסביבה?',
                 ['מצפן תכווינים, שעון, 3 מדידות ואומדן טווח', 'מצפן גירו עם טלסקופ ראיית לילה',
                  'מצפן עם שגיאה ידועה ומשקפת 7x50', 'מצפן עם טבעת כיוון יחסי'], 0))
    save(im, 's08_compass_q23')

def s09():
    im, d = base(); left_panel(d, 'עוד שני פקדים')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=BG)
    c = ((x0 + x1) / 2, y0 + 380); r = 320
    ppi_head(d, c, r, 0, rings=3); coast(d, c, r, 0)
    for arm in (20, 140, 260):                                   # interference: dotted spiral arms
        for k in range(4, 40):
            p = polar_pt(c, r * k / 40, arm + k * 4); d.ellipse((p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4), fill=(200, 210, 120))
    tag(d, (c[0] + r - 60, c[1] - r + 20), 'הפרעה ממכ״מ שכן', CORAL, 32)
    for i, (k, v, col) in enumerate([('TUNING', 'כוונון עדין של תדר המקלט', GREEN_L), ('INTERFERENCE REJECTION', 'מעלים הפרעות ממכ״מים שכנים', ORANGE)]):
        box_text(d, (x0 + 30, y0 + 750 + i * 150, x1 - 30, y0 + 880 + i * 150), [(k, 40, col), (v, 34, TEXT)], col)
    right_block(d, 'TUNING · IR', 'TUNING מכוון את המקלט להדים החזקים ביותר. INTERFERENCE REJECTION מעלים את הקווים המנוקדים של מכ״מים אחרים.')
    save(im, 's09_more_controls')

def s10():
    im, d = base(); left_panel(d, 'איפה האנטנה')
    box = inner(); x0, y0, x1, y1 = box
    hh = (y1 - y0 - 20) / 2
    d, P = photo_map(im, (x0, y0, x1, y0 + hh), 'u10_arch', (0.4, 0.4))
    a = P(992, 300); tag(d, (a[0] + 110, a[1] + 10), 'מפרשית: עמוד בירכתיים או תורן', GREEN_L, 34, 'l')
    d, P = photo_map(im, (x0, y1 - hh, x1, y1), 'u10_motoryacht', (0.45, 0.4))
    m = P(840, 480); tag(d, (m[0] + 110, m[1]), 'יאכטה מנועית: על הגג', GREEN_L, 34, 'l')
    tag(d, ((x0 + x1) / 2, y1 - 50), 'רחוק מהמצפן ומה-GPS', ORANGE, 36)
    right_block(d, 'מיקום האנטנה', 'בתיאוריה, בראש התורן: גבוה יותר רואה רחוק יותר. אבל יש משקל, גישה לתחזוקה ושטחים מתים.')
    save(im, 's10_antenna_location')

def s11():
    im, d = base(); left_panel(d, 'מחזיר הד מכ״מ')
    box = inner(); x0, y0, x1, y1 = box
    sx = x0 + 700
    d, P = photo_map(im, (sx, y0, x1, y0 + 760), 'u10_reflector_mast', (0.5, 0.3))
    rf = P(880, 660); tag(d, (rf[0], rf[1] + 170), 'גבוה על התורן', ORANGE, 38)
    d.rectangle((x0, y0, sx - 10, y0 + 760), fill=WHITE)
    d = photo(im, (x0 + 40, y0 + 10, sx - 50, y0 + 690), 'u10_tube_reflector')   # Alex's photo: tube reflector
    tag(d, ((x0 + sx) / 2, y0 + 720), 'מחזיר צינור', ORANGE, 36)
    for i, (k, v, col) in enumerate([('מחזיר הד', 'לא משדר, רק מחזיר · תמיד', GREEN_L), ('SART', 'משיב משדר · רק במצוקה', CORAL)]):
        bw = (x1 - x0 - 80) / 2; bx = x1 - 30 - (i + 1) * bw - i * 20
        box_text(d, (bx, y0 + 790, bx + bw, y1 - 20), [(k, 44, col), (v, 32, TEXT)], col)
    right_block(d, 'רואים אותך', 'פיברגלאס ועץ לא מחזירים טוב גלי מכ״מ. מחזיר ההד מגדיל את ההד שלך על המסך של אחרים.',
                ('שאלה מהמאגר · 105', 'מהו ההבדל בין (ראשון) RADAR REFLECTOR ו-(שני) S.A.R.T?',
                 ['הראשון: לסירות מחומר שלא מחזיר הד', 'השני: רק במצוקה, בחיפוש והצלה',
                  'הראשון לא משדר, השני משיב משדר', 'כל התשובות נכונות'], 3))
    save(im, 's11_reflector_q105')

def s12():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u10_ship', focus=(0.72, 0.5))
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['כיוון יחסי: ביחס לחרטום', 'ירוק מימין, אדום משמאל', 'ירוק מוסיפים, אדום מפחיתים', 'יחסית: חרטום למעלה',
             'אמיתית: צפון למעלה', 'התנגשות: כיוון קבוע, טווח נסגר', 'בדיקה במצפן: 3 מדידות ושעון', 'מחזיר הד: אחרים רואים אותך']
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 5 else ORANGE)
        text_r(d, 2380, y + 20, s, F(48, False), TEXT)
    save(im, 's12_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12]
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
