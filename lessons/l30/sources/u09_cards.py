"""Lesson 9 (l30): עקרון המכ״מ. Realistic photos (assets/u9_*.jpg, Higgsfield nano_banana) with drawn overlays."""
import math, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U6 = _load('u06', 'u06_cards.py'); U8 = _load('u08', 'u08_cards.py')
from PIL import Image, ImageDraw
C.OUT = os.path.join(HERE, '..', 'cards', 'עקרון המכ״מ'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · עקרון המכ״מ'
F, text_c, text_r, label, dot, arrow = C.F, C.text_c, C.text_r, C.label, C.dot, C.arrow
base, left_panel, right_block, save, RC = C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, ORANGE, CORAL, GREEN, GREEN_L, BLUE_L, PANEL, MUTED = C.TEXT, C.ORANGE, C.CORAL, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL, C.MUTED
readout, inner, WHITE, polar_pt = U5.readout, U5.inner, U5.WHITE, U5.polar_pt
photo, tag, photo_map, dashed, box_text, DARK = U8.photo, U8.tag, U8.photo_map, U8.dashed, U8.box_text, U8.DARK
ECHO = (90, 230, 110)

def ppi(d, c, r, rings=3):
    """Small radar screen: own ship at the center, range rings, heading line."""
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=(6, 22, 14), outline=(60, 160, 90), width=4)
    for k in range(1, rings): rr = r * k / rings; d.ellipse((c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr), outline=(40, 110, 60), width=2)
    d.line((c, (c[0], c[1] - r)), fill=(160, 200, 170), width=2); dot(d, c, 8, WHITE)

def blip(d, p, w=16, h=10, col=ECHO): d.ellipse((p[0] - w, p[1] - h, p[0] + w, p[1] + h), fill=col)

# ---------- cards ----------
def s01():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u9_radome', focus=(0.5, 0.35))
    readout(d, (60, 1120, 500, 1380), 'RANGE · BRG', '2.4 NM · 045°')
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 9', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'עקרון המכ״מ', F(130), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['טווח וכיוון מהד', 'מה המכ״מ רואה', 'פולס, אנטנה ותדרים', 'GAIN, גשם וסטנד ביי']):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    im, d = base(); left_panel(d, 'גל רדיו, הד וזמן')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, (x0, y0, x1, y0 + 640), 'u9_radome', (0.5, 0.3))
    a = P(802, 722)
    for k in range(1, 4):
        r = k * 90; d.arc((a[0] - r, a[1] - r, a[0] + r, a[1] + r), -25, 25, fill=ORANGE, width=6)
    arrow(d, (a[0] + 60, a[1] - 20), (x1 - 40, a[1] - 20), ORANGE, 8, 30); arrow(d, (x1 - 40, a[1] + 30), (a[0] + 60, a[1] + 30), GREEN_L, 8, 30)
    tag(d, (x1 - 170, a[1] - 80), 'פולס', ORANGE, 36); tag(d, (x1 - 170, a[1] + 90), 'הד', GREEN_L, 36)
    tag(d, (a[0] - 30, a[1] + 120), 'אנטנה', WHITE, 36, 'r')
    box_text(d, (x0 + 30, y0 + 670, x1 - 30, y0 + 900), [('R = T × 300,000 ÷ 2', 62, TEXT), ('מהירות האור: 300,000 ק״מ בשנייה', 42, GREEN_L)])
    box_text(d, (x0 + 30, y0 + 920, x1 - 30, y1 - 10), [('RADAR', 48, BLUE_L), ('Radio Detecting And Ranging', 38, MUTED)], BLUE_L)
    right_block(d, 'כמו מד העומק', 'גל רדיו במקום קול. טווח: זמן כפול מהירות, חלקי שתיים. כיוון: לפי כיוון האנטנה ביחס לחרטום ברגע השידור.')
    save(im, 's02_principle')

def s03():
    im, d = base(); left_panel(d, 'כל מה שבתוך האלומה')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, box, 'u9_plane_rain', (0.55, 0.5))
    a = P(744, 1072)
    for sgn in (-1, 1):
        e = (x1, a[1] + sgn * (x1 - a[0]) * math.tan(math.radians(12.5)))
        dashed(d, a, e, ORANGE, 5)
    tag(d, (x1 - 150, a[1] - 170), 'אלומה אנכית 20-25°', ORANGE, 32)
    pl = P(480, 852); tag(d, (pl[0], pl[1] - 70), 'מטוס מעל האלומה', CORAL, 34)
    rn = P(1820, 1260); tag(d, (rn[0] - 40, rn[1] + 60), 'גשם בתוך האלומה', GREEN_L, 34)
    right_block(d, 'מה נקלט', 'מטרות מעל קו המים, קו החוף, גשם, עננים וגלים, ואפילו מטוסים. בתנאי שהם בתוך האלומה.',
                ('שאלה מהמאגר · 50', 'האם ניתן לזהות במכ״מ כלי טיס וענני גשם?',
                 ['ניתן, רק בגבהים שבתוך האלומה האנכית', 'לא, המכ״מ קולט רק עצמים במישור',
                  'עננים רק עם גשם, מטוסים רק מול החרטום', 'רק כשהספינה מטלטלת והאלומה פונה מעלה'], 0))
    save(im, 's03_detects_q50')

def s04():
    im, d = base(); left_panel(d, 'שימושי המכ״מ')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, box, 'u9_screen', focus=(0.47, 0.45))
    for i, s in enumerate(['מניעת התנגשות', 'ניווט', 'חיפוש והצלה']):
        tag(d, (x0 + 200 + i * 390, y0 + 60), s, GREEN_L, 40)
    tag(d, ((x0 + x1) / 2, y1 - 60), 'שאלה 161: ב · צוללות? המכ״מ לא רואה מתחת למים', ORANGE, 36)
    right_block(d, 'שתי שאלות', 'שאלה 49: כל התשובות נכונות. שאלה 161: רק ב, כי שם יש מסיח על צוללות.',
                ('שאלה מהמאגר · 49', 'מהם שימושי המכ״מ?',
                 ['לזהות כלי שיט כשאין ראות', 'מניעת התנגשות, ניווט, ניתוב, חיפוש והצלה',
                  'לזהות כלי שיט ולהתריע בטווח קטן', 'כל התשובות נכונות'], 3))
    save(im, 's04_uses_q49_q161')

def s05():
    im, d = base(); left_panel(d, 'כיוון מדויק: בעין')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, (x0, y0, x1, y0 + 700), 'u9_bearing', (0.55, 0.45))
    lh = P(500, 620); cp = P(1880, 640)
    dashed(d, cp, lh, ORANGE, 4)
    tag(d, (lh[0] + 20, lh[1] - 120), 'מגדלור', WHITE, 36); tag(d, (cp[0] - 40, cp[1] + 170), 'כוונת', ORANGE, 36)
    for i, s in enumerate(['שני טווחים', 'טווח + כיוון', 'שני כיוונים']):
        bw = (x1 - x0 - 100) / 3; bx = x1 - 30 - (i + 1) * bw - i * 20
        box_text(d, (bx, y0 + 730, bx + bw, y0 + 860), [(s, 40, TEXT)], BLUE_L)
    box_text(d, (x0 + 30, y0 + 890, x1 - 30, y1 - 10), [('במכ״מ: טווח מדויק יותר מכיוון', 48, GREEN_L)])
    right_block(d, 'ניווט במכ״מ', 'שלוש דרכים לקבוע מיקום. במכ״מ מעדיפים טווחים, כי הכיוון בו פחות מדויק.',
                ('שאלה מהמאגר · 146', 'תכווין לאתר בחוף ניתן לקבל באופן המדויק ביותר על ידי:',
                 ['מכ״מ', 'GPS', 'מכ״ר (D.F)', 'פילורוס'], 3))
    save(im, 's05_nav_q146')

def s06():
    im, d = base(); left_panel(d, 'המסך: EBL, VRM וסמן')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, (x0, y0, x1, y0 + 720), 'u9_screen', (0.47, 0.47))
    c = P(1140, 860); s = P(1140 + 380, 860)[0] - c[0]
    e = polar_pt(c, s, 60); d.line((c, e), fill=ORANGE, width=6)
    rr = s * 0.62; d.ellipse((c[0] - rr, c[1] - rr, c[0] + rr, c[1] + rr), outline=CORAL, width=5)
    cu = polar_pt(c, s * 0.45, 300); d.line(((cu[0] - 22, cu[1]), (cu[0] + 22, cu[1])), fill=WHITE, width=4); d.line(((cu[0], cu[1] - 22), (cu[0], cu[1] + 22)), fill=WHITE, width=4)
    tag(d, (x1 - 150, y0 + 60), 'EBL', ORANGE, 40); tag(d, (x0 + 150, y0 + 60), 'VRM', CORAL, 40); tag(d, (x0 + 150, y0 + 660), 'סמן', WHITE, 40)
    for i, (k, v, col) in enumerate([('EBL', 'קו מהמרכז · כיוון', ORANGE), ('VRM', 'טבעת טווח · טווח', CORAL), ('סמן', 'טווח וכיוון', WHITE)]):
        y = y0 + 750 + i * 102
        d.rounded_rectangle((x0 + 30, y, x1 - 30, y + 90), 20, fill=PANEL, outline=col, width=3)
        label(d, (x1 - 80, y + 45), k, F(44), col, 'r'); label(d, (x1 - 300, y + 45), v, F(42, False), TEXT, 'r')
    right_block(d, 'המסך', 'הספינה במרכז. קרן סורקת בקצב סיבוב האנטנה. קו חרטום מראה לאן אתה מכוון. EBL לכיוון, VRM לטווח, והסמן לשניהם.')
    save(im, 's06_display_ebl_vrm')

def s07():
    im, d = base(); left_panel(d, 'כמה רחוק הוא רואה')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, (x0, y0, x1, y0 + 700), 'u9_radome', (0.5, 0.32))
    a = P(802, 722); tag(d, (a[0] + 170, a[1] - 20), 'גובה אנטנה', ORANGE, 40, 'l')
    for i, s in enumerate(['גובה אנטנה', 'עוצמת שידור', 'אקלים ואטמוספרה']):
        bw = (x1 - x0 - 100) / 3; bx = x1 - 30 - (i + 1) * bw - i * 20
        box_text(d, (bx, y0 + 740, bx + bw, y0 + 900), [(s, 40, GREEN_L)])
    label(d, ((x0 + x1) / 2, y0 + 980), 'משדר ממוצע: 1.5 עד 5 KW', F(44, False), MUTED)
    right_block(d, 'טווח הגילוי', 'אנטנה גבוהה רואה מעבר לעקמומיות. משדר חזק נותן הד חזק. ומזג האוויר משנה את דרכו של הגל.',
                ('שאלה מהמאגר · 63', 'במה מותנה טווח הגילוי של מכ״מ?',
                 ['מחירו של המכ״מ', 'רוחב האלומה האופקית של האנטנה',
                  'גובה אנטנה, עוצמת שידור, אקלים ואטמוספרה', 'גובה האנטנה ועוצמת השידור בלבד'], 2))
    save(im, 's07_range_q63')

def s08():
    im, d = base(); left_panel(d, 'מה משפיע על הקליטה')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, box, 'u9_screen', dim=0.3, focus=(0.47, 0.45))
    cols = [('חיצוניים', ['מזג אוויר', 'מצב ים', 'גשם ולחות', 'גודל המטרה', 'חומר המטרה', 'זווית ומהירות'], BLUE_L),
            ('פנימיים', ['גובה אנטנה', 'עוצמת שידור', 'רוחב פולס', 'רגישות המקלט', 'כיוון הפקדים'], GREEN_L)]
    for j, (h, items, col) in enumerate(cols):
        cx = x1 - 290 - j * 580
        label(d, (cx, y0 + 70), h, F(52), col)
        for i, s in enumerate(items):
            y = y0 + 150 + i * 132
            d.rounded_rectangle((cx - 250, y, cx + 250, y + 110), 20, fill=DARK, outline=col, width=3)
            label(d, (cx, y + 55), s, F(42, False), TEXT)
    right_block(d, 'שתי שאלות זהות', 'שאלה 80 ושאלה 164: כל התשובות נכונות.',
                ('שאלה מהמאגר · 164', 'במה תלוי האיכות וטווח הגילוי של עצם במכ״מ?',
                 ['תחום הטווחים שבוחרים (RANGE)', 'משדר, מקלט, אנטנה והתפשטות הגל',
                  'כיוון נכון של TUNE, GAIN, PULSE', 'כל התשובות נכונות'], 3))
    save(im, 's08_quality_q80_q164')

def pulse_row(d, y, x0, x1, pw, title, col):
    label(d, (x1 - 20, y - 120), title, F(46), col, 'r')
    d.line(((x0, y), (x1, y)), fill=MUTED, width=3)
    for t in (x1 - 760, x1 - 640):                     # two targets close in range
        d.polygon([(t, y - 18), (t + 14, y), (t, y + 18), (t - 14, y)], fill=WHITE)
    for t in (x1 - 760, x1 - 640):
        d.rectangle((t - pw, y - 70, t, y - 30), fill=col)
    merged = pw > 120
    tag(d, ((x0 + x1) / 2, y + 70), 'ההדים מתמזגים: כתם אחד' if merged else 'שני הדים נפרדים', CORAL if merged else GREEN_L, 36)

def s09():
    im, d = base(); left_panel(d, 'פולס קצר מול פולס ארוך')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, box, 'u9_screen', dim=0.25, focus=(0.47, 0.45))
    pulse_row(d, y0 + 280, x0 + 40, x1 - 40, 200, 'פולס ארוך · רואה רחוק', ORANGE)
    pulse_row(d, y0 + 640, x0 + 40, x1 - 40, 60, 'פולס קצר · מפריד טוב', GREEN_L)
    box_text(d, (x0 + 30, y1 - 220, x1 - 30, y1 - 20), [('טווח קטן: פולס קצר', 46, GREEN_L), ('טווח גדול: פולס ארוך', 46, ORANGE)])
    right_block(d, 'אורך הפולס', 'פולס ארוך נושא יותר אנרגיה ורואה רחוק, אבל מטרות קרובות מתמזגות. פולס קצר מפריד טוב.',
                ('שאלה מהמאגר · 163', 'סמן את המשפט שתוכנו הנכון ביותר ביחס למכ״מ הימי:',
                 ['פולס קצר: אבחנה טובה בטווח (חלקי)', 'טווח גדול: אבחנה טובה בכיוון',
                  'פולס ארוך: טווח הגילוי קטן', 'קרוב: פולס קצר. רחוק: פולס ארוך'], 3))
    save(im, 's09_pulse_q163')

def s10():
    im, d = base(); left_panel(d, 'אותו כיוון, טווח שונה')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=(10, 20, 34))
    for j, (title, merged, col) in enumerate([('פולס ארוך', True, ORANGE), ('פולס קצר', False, GREEN_L)]):
        c = (x1 - 290 - j * 580, y0 + 470); r = 250
        ppi(d, c, r)
        p1, p2 = polar_pt(c, r * 0.55, 30), polar_pt(c, r * 0.72, 30)
        if merged:
            q1, q2 = polar_pt(c, r * 0.5, 30), polar_pt(c, r * 0.77, 30); d.line((q1, q2), fill=ECHO, width=34)
        else:
            blip(d, p1); blip(d, p2)
        label(d, (c[0], y0 + 120), title, F(50), col)
        tag(d, (c[0], c[1] + r + 70), 'כתם אחד' if merged else 'שתי מטרות', CORAL if merged else GREEN_L, 38)
    box_text(d, (x0 + 30, y1 - 190, x1 - 30, y1 - 20), [('מטרות באותו כיוון נפרדות לפי טווח: פולס קצר', 40, GREEN_L)])
    right_block(d, 'הפרדה בטווח', 'שתי מטרות באותו כיוון, אחת מאחורי השנייה. מה שמפריד ביניהן הוא הטווח, וזה תלוי באורך הפולס.',
                ('שאלה מהמאגר · 114', 'בין 2 מטרות קרובות (פיזית) הנמצאות באותו כיוון במכ״מ, מתי תהיה הבחנה טובה יותר?',
                 ['כאשר האלומה האנכית גדולה יותר', 'כאשר האלומה האופקית קטנה יותר',
                  'כאשר הספק השידור גדול יותר', 'כאשר רוחב הפולס קטן יותר'], 3))
    save(im, 's10_discrimination_q114')

def fan(im, o, deg, half, L, col):
    """Translucent beam wedge from o toward deg (0 = right, 180 = left), +-half degrees, length L."""
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(ov)
    pts = [o] + [(o[0] + L * math.cos(math.radians(deg + a)), o[1] - L * math.sin(math.radians(deg + a))) for a in (half, -half)]
    g.polygon(pts, fill=col + (110,)); g.line(pts[1:2] + [o] + pts[2:], fill=col + (255,), width=4)
    im.paste(Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')); return ImageDraw.Draw(im)

def s11():
    im, d = base(); left_panel(d, 'X ו-S, ורוחב האלומה')
    box = inner(); x0, y0, x1, y1 = box
    hw = (x1 - x0 - 20) / 2
    d = photo(im, (x1 - hw, y0, x1, y0 + 330), 'u9_radome', focus=(0.45, 0.3))
    d = photo(im, (x0, y0, x0 + hw, y0 + 330), 'u9_ship_arrays', focus=(0.5, 0.3))
    tag(d, (x1 - hw / 2, y0 + 290), 'כיפת מכ״מ · X', GREEN_L, 34); tag(d, (x0 + hw / 2, y0 + 290), 'אנטנה פתוחה · S', BLUE_L, 34)
    box_text(d, (x1 - hw, y0 + 345, x1, y0 + 565), [('X · 9 GHz · 3 cm', 38, GREEN_L), ('תמונה חדה', 32, TEXT), ('גשם מפריע, טווח קצר', 32, TEXT)])
    box_text(d, (x0, y0 + 345, x0 + hw, y0 + 565), [('S · 3 GHz · 10 cm', 38, BLUE_L), ('רואה רחוק, טוב במז״א', 32, TEXT), ('אנטנה גדולה, הפרדה פחותה', 32, TEXT)], BLUE_L)
    # beam drawings: right = top view (horizontal ~4 deg), left = side view (vertical 20-25 deg)
    by0, by1 = y0 + 585, y1 - 75
    for bx0 in (x0, x1 - hw): d.rounded_rectangle((bx0, by0, bx0 + hw, by1), 20, fill=(12, 30, 50), outline=ORANGE, width=3)
    o = (x1 - 60, (by0 + by1) / 2 + 20)
    d = fan(im, o, 180, 2, hw - 90, ORANGE)
    d.arc((o[0] - 46, o[1] - 46, o[0] + 46, o[1] + 46), 200, 340, fill=WHITE, width=3); dot(d, o, 12, WHITE)
    label(d, (x1 - hw / 2, by0 + 50), 'מבט מלמעלה · אופקית ~4°', F(36), ORANGE)
    sea = by1 - 60; mx = x0 + hw - 80
    d.rectangle((x0 + 3, sea, x0 + hw - 3, by1 - 3), fill=(18, 70, 110))
    d.polygon([(mx - 70, sea - 10), (mx + 50, sea - 10), (mx + 30, sea + 14), (mx - 55, sea + 14)], fill=WHITE)
    d.line(((mx, sea - 10), (mx, sea - 210)), fill=WHITE, width=5); ra = (mx, sea - 140); dot(d, ra, 14, WHITE)
    d = fan(im, ra, 180, 12.5, hw - 130, ORANGE)
    label(d, (x0 + hw / 2, by0 + 50), 'מבט מהצד · אנכית 20-25°', F(36), ORANGE)
    tag(d, ((x0 + x1) / 2, y1 - 35), 'קרינת המכ״מ מסוכנת', CORAL, 38)
    right_block(d, 'תדרים ואנטנה', 'X: חד, אבל גשם מפריע. S: רואה רחוק ובמזג אוויר גרוע, אבל צריך אנטנה גדולה. אלומה אופקית צרה, אנכית רחבה, כדי לראות את האופק גם בטלטולים.')
    save(im, 's11_bands_beam')
def s12():
    im, d = base(); left_panel(d, 'הגל מתעקם עם כדור הארץ')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=(14, 30, 52))
    xa = x1 - 140; mx, sy, R = xa, y0 + 380, 1350                # earth surface drops away from the antenna: y = sy + (x - mx)^2 / 2R
    surf = lambda x: sy + (x - mx) ** 2 / (2 * R)
    d.polygon([(x, surf(x)) for x in range(int(x0), int(x1) + 1, 10)] + [(x1, y1), (x0, y1)], fill=(18, 70, 110))
    ya = surf(xa) - 90
    d.line(((xa, surf(xa)), (xa, ya)), fill=WHITE, width=6); dot(d, (xa, ya), 12, ORANGE)
    xt = x0 + 140; th = 40; yt = surf(xt) - th
    d.polygon([(xt - 30, surf(xt)), (xt + 30, surf(xt)), (xt + 18, yt), (xt - 18, yt)], fill=WHITE)
    d.line(((xa, ya), (x0 + 20, ya)), fill=MUTED, width=4)
    Rr = (xt - xa) ** 2 / (2 * (yt + 6 - ya))
    d.line([(x, ya + (x - xa) ** 2 / (2 * Rr)) for x in range(int(xa), int(xt) - 1, -10)], fill=ORANGE, width=7)
    tag(d, (x0 + 330, ya - 50), 'קו ישר: עובר מעל המטרה', MUTED, 32)
    xm = (xa + xt) / 2; tag(d, (xm, ya + (xm - xa) ** 2 / (2 * Rr) + 70), 'גל מתעקם', ORANGE, 36)
    tag(d, (xt - 20, surf(xt) + 70), 'מטרה מעבר לאופק', GREEN_L, 32, 'l')
    tag(d, (xa - 20, ya - 60), 'אנטנה', WHITE, 32, 'r')
    box_text(d, (x0 + 30, y1 - 250, x1 - 30, y1 - 20), [('טווח גדל', 50, GREEN_L), ('מדידת מרחק פחות מדויקת', 46, ORANGE)])
    right_block(d, 'התעקמות', 'הגל עוקב אחרי עקמומיות כדור הארץ ורואה רחוק יותר. אבל הדרך כבר לא ישרה, אז המרחק פחות מדויק.',
                ('שאלה מהמאגר · 131', 'למה גורמת התעקמות גלי המכ״מ?',
                 ['הקטנת טווח המכ״מ', 'הגדלת טווח המכ״מ', 'אי דיוק במדידת מרחק המטרה', 'תשובה ב׳ וג׳ נכונות'], 3))
    save(im, 's12_refraction_q131')

CONTROLS = [  # (label on the unit, Hebrew meaning, button centre in u9_furuno.jpg px)
    ('MENU · ENTER', 'תפריט ובחירה', (516, 200)), ('CANCEL HL OFF', 'ביטול · הסתרת קו חרטום', (537, 175)),
    ('EBL', 'קו כיוון', (496, 275)), ('VRM', 'טבעת טווח', (537, 275)), ('OFF CENTER', 'הזזת המרכז', (496, 313)),
    ('TARGET ALARM', 'התראת מטרה', (537, 313)), ('TLL', 'סימון מיקום מטרה', (496, 350)), ('RANGE ±', 'תחום הטווח', (537, 368)),
    ('GAIN', 'רגישות המקלט', (493, 395)), ('SEA · STC', 'הנחתת הדי ים', (493, 450)), ('RAIN · FTC', 'הנחתת גשם', (493, 505)),
    ('CUSTOM', 'מקש מותאם אישית', (537, 420)), ('TRAILS', 'שובל מטרות', (537, 458)), ('STBY TX', 'המתנה · שידור', (537, 495)),
    ('BRILL', 'בהירות המסך', (540, 530))]

def s13():
    im, d = base(); left_panel(d, 'לוח הבקרה')
    box = inner(); x0, y0, x1, y1 = box
    d.rectangle(box, fill=WHITE)
    crop = (128, 122, 600, 584); s = min((x1 - x0) / (crop[2] - crop[0]), (y1 - y0) / (crop[3] - crop[1]))
    g = Image.open(os.path.join(U8.RL.A, 'u9_furuno.jpg')).convert('RGB').crop(crop)
    W, H = int(g.width * s), int(g.height * s); g = g.resize((W, H), Image.LANCZOS)
    ox, oy = int(x0 + (x1 - x0 - W) / 2), int(y0 + (y1 - y0 - H) / 2); im.paste(g, (ox, oy)); d = ImageDraw.Draw(im)
    P = lambda x, y: (ox + (x - crop[0]) * s, oy + (y - crop[1]) * s)
    sc0, sc1 = P(182, 186), P(432, 520); d.rectangle((sc0[0], sc0[1], sc1[0], sc1[1]), fill=(6, 12, 20))
    n = len(CONTROLS); lh = (sc1[1] - sc0[1] - 20) / n
    for i, (k, v, p) in enumerate(CONTROLS):
        col = ORANGE if k == 'GAIN' else (GREEN_L if i % 2 == 0 else BLUE_L)
        y = sc0[1] + 10 + lh * (i + 0.5)
        label(d, (sc1[0] - 12, y), k, F(26), col, 'r'); label(d, (sc0[0] + 12, y), v, F(26, False), TEXT, 'l')
    g0 = P(493, 395); d.ellipse((g0[0] - 44, g0[1] - 44, g0[0] + 44, g0[1] + 44), outline=ORANGE, width=6)
    right_block(d, 'GAIN', 'קובע כמה המקלט מגביר את ההדים. מעט מדי: מטרות חלשות נעלמות. יותר מדי: רעש.',
                ('שאלה מהמאגר · 76', 'למה משמש כפתור ה-GAIN במכ״מ?',
                 ['להבהרת התמונה בעיקר בלילה', 'להנחתת או הגברת עצמת המשדר',
                  'להנחתת השפעות גשם והפרעות מרכז', 'להנחתת או הגברת רגישות הקליטה'], 3))
    save(im, 's13_gain_q76')
def s14():
    im, d = base(); left_panel(d, 'גשם על המסך')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, (x0, y0, x1, y0 + 640), 'u9_rain', (0.55, 0.45))
    fb = P(2060, 1020); tag(d, (fb[0] - 30, fb[1] - 90), 'סירה קטנה בגשם', WHITE, 34, 'r')
    tag(d, (x0 + 220, y0 + 60), 'גשם סמיך', BLUE_L, 38)
    box_text(d, (x0 + 30, y0 + 670, x1 - 30, y0 + 820), [('גשם: FTC · Anti-Clutter Rain', 46, GREEN_L)])
    box_text(d, (x0 + 30, y0 + 840, x1 - 30, y0 + 990), [('גלים ליד המרכז: STC · Anti-Clutter Sea', 40, ORANGE)], ORANGE)
    right_block(d, 'גשם', 'ניתן לזהות, תלוי בגודל ובחומר של העצם ובסמיכות הגשם. גם בשאלה 162 התשובה א.',
                ('שאלה מהמאגר · 79', 'האם ניתן לזהות במכ״מ כלי שיט קטנים וכניסה למרינה בגשם סמיך, ואיזה פקד יש להפעיל?',
                 ['ניתן, תלוי בעצם ובגשם. פקד FTC', 'גילוי מיידי עם Anti-Clutter Sea או STC',
                  'פקד להגברת עצמת השידור', 'לא ניתן: להוריד מהירות ולהמתין'], 0))
    save(im, 's14_rain_q79_q162')

def s15():
    im, d = base(); left_panel(d, 'מצב המתנה')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, box, 'u9_screen', dim=0.35, focus=(0.47, 0.45))
    cx = (x0 + x1) / 2
    d.rounded_rectangle((x0 + 120, y0 + 200, x1 - 120, y0 + 420), 30, fill=DARK, outline=ORANGE, width=5)
    label(d, (cx, y0 + 310), 'STAND-BY', F(110), ORANGE)
    for i, (s, col) in enumerate([('לא משדר', CORAL), ('לא קולט', CORAL), ('מסך חם, מוכן מיד', GREEN_L)]):
        box_text(d, (x0 + 150, y0 + 480 + i * 140, x1 - 150, y0 + 590 + i * 140), [(s, 46, col)], col)
    right_block(d, 'סטנד ביי', 'המכ״מ חי אבל שקט. לוחצים, והוא עובד מיד.',
                ('שאלה מהמאגר · 82', 'מצב STAND-BY במכ״מ הימי:',
                 ['המכ״מ רק קולט ואינו משדר', 'פעולה מלאה, התצוגה כבויה זמנית',
                  'הפקדים חוזרים למצב התחלתי', 'לא משדר ולא קולט, המסך חם ומוכן'], 3))
    save(im, 's15_standby_q82')

def s16():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u9_screen', focus=(0.45, 0.45))
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['טווח: זמן × 300,000 ÷ 2', 'כיוון: לפי האנטנה', 'רואה כל מה שבתוך האלומה', 'טווח מדויק יותר מכיוון',
             'טווח גילוי: אנטנה, עוצמה, אטמוספרה', 'פולס קצר מפריד, ארוך רואה רחוק', 'GAIN: רגישות · FTC: גשם', 'STAND-BY: לא משדר, מוכן מיד']
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 6 else ORANGE)
        text_r(d, 2380, y + 20, s, F(48, False), TEXT)
    save(im, 's16_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16]
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
