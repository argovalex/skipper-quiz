"""Lesson 13 (l30): גלי רדיו ומכשיר VHF. Real photos (assets/u13_*.jpg from Wikimedia Commons, credits in assets/u13_credits.txt) with drawn diagrams."""
import math, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U6 = _load('u06', 'u06_cards.py'); U8 = _load('u08', 'u08_cards.py')
U11 = _load('u11', 'u11_cards.py'); U12 = _load('u12', 'u12_cards.py')
from PIL import Image, ImageDraw
import real as RL
C.OUT = os.path.join(HERE, '..', 'cards', 'גלי רדיו ומכשיר VHF'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · גלי רדיו ומכשיר VHF'
F, text_c, text_r, label, dot, arrow = C.F, C.text_c, C.text_r, C.label, C.dot, C.arrow
base, left_panel, right_block, save, RC = C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, ORANGE, CORAL, GREEN, GREEN_L, BLUE_L, PANEL, MUTED = C.TEXT, C.ORANGE, C.CORAL, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL, C.MUTED
readout, inner, WHITE = U5.readout, U5.inner, U5.WHITE
photo, tag, photo_map, dashed, box_text, DARK = U8.photo, U8.tag, U8.photo_map, U8.dashed, U8.box_text, U8.DARK
pointer, row_boxes, contain = U11.pointer, U11.row_boxes, U11.contain
circle, globe, pt, SKY = U12.circle, U12.globe, U12.pt, U12.SKY
U12.CREDIT.update({'u13_vhf': 'Photo: PaterMcFly · CC BY 3.0', 'u13_handheld': 'Photo: Ulflarsen · CC BY-SA 3.0',
                   'u13_longwave': 'Photo: JohnnyWiki · CC BY-SA 3.0', 'u13_vhf_whip': 'Photo: F1jmm · CC BY-SA 3.0'})
credit = U12.credit

def wave(d, x0, x1, yc, amp, wl, col, w=5, am=None, fm=None):
    """Sine from x0 to x1. am: amplitude envelope f(t); fm: wavelength factor f(t), t in 0..1."""
    pts, ph = [], 0.0
    for i in range(0, int(x1 - x0) + 1, 2):
        t = i / (x1 - x0); k = fm(t) if fm else 1.0; ph += 2 * math.pi * 2 / (wl * k)
        a = amp * (am(t) if am else 1.0); pts.append((x0 + i, yc - a * math.sin(ph)))
    d.line(pts, fill=col, width=w)

def mast(d, base_pt, h, col=WHITE):
    x, y = base_pt; d.line(((x, y), (x, y - h)), fill=col, width=7); dot(d, (x, y - h), 9, col); return (x, y - h)

# ---------- cards ----------
def s01():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u13_vhf', focus=(0.6, 0.55)); credit(d, (0, 0, 1300, 1440), 'u13_vhf')
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 13', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'גלי רדיו ומכשיר VHF', F(110), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['מה זה גל רדיו', 'גל קרקע, רקיע וישיר', 'תחומי תדרים ואפנון', 'המכשיר והטווח']):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    im, d = base(); left_panel(d, 'GMDSS')
    box = inner(); x0, y0, x1, y1 = box
    d = photo(im, box, 'u13_vhf', dim=0.3, focus=(0.6, 0.55)); credit(d, box, 'u13_vhf')
    items = [('VHF', 'קשר בשגרה ובמצוקה', GREEN_L), ('DSC', 'קריאה ספרתית ומצוקה', ORANGE), ('NAVTEX', 'הודעות בטיחות כתובות', ORANGE),
             ('EPIRB', 'משואה לאיתור בחירום', ORANGE), ('SART', 'משיב מכ״מ להצלה', ORANGE)]
    for i, (h, s, col) in enumerate(items):
        y = y0 + 30 + i * 205
        box_text(d, (x0 + 60, y, x1 - 60, y + 175), [(h, 50, col), (s, 34, TEXT)], col)
    right_block(d, 'GMDSS', 'המערכת העולמית למצוקה ובטיחות בים. היום ה-VHF, ובשיעורים הבאים כל השאר.')
    save(im, 's02_gmdss')

def s03():
    im, d = base(); left_panel(d, 'תדר ואורך גל')
    box = inner(); x0, y0, x1, y1 = box; d.rectangle(box, fill=SKY)
    for yc, wl, col, s in [(y0 + 230, 480, BLUE_L, 'תדר נמוך · גל ארוך'), (y0 + 640, 160, ORANGE, 'תדר גבוה · גל קצר')]:
        wave(d, x0 + 60, x1 - 60, yc, 110, wl, col, 6)
        xa = x0 + 60 + wl / 4; d.line(((xa, yc - 150), (xa + wl, yc - 150)), fill=WHITE, width=4)
        for xx in (xa, xa + wl): d.line(((xx, yc - 165), (xx, yc - 135)), fill=WHITE, width=4)
        tag(d, (xa + wl / 2, yc - 195), 'אורך גל', WHITE, 30); tag(d, ((x0 + x1) / 2, yc + 175), s, col, 38)
    box_text(d, (x0 + 120, y1 - 140, x1 - 120, y1 - 30), [('מהירות האור · תדר גבוה = גל קצר', 40, GREEN_L)])
    right_block(d, 'גל רדיו', 'זרם באנטנה יוצר גל אלקטרומגנטי שנע במהירות האור. תדר: כמה תנודות בשנייה. אורך גל: משיא לשיא.')
    save(im, 's03_waves')

def antennas(d, box):
    x0, y0, x1, y1 = box; d.rectangle(box, fill=SKY); g = y1 - 160
    d.line(((x0, g), (x1, g)), fill=MUTED, width=3)
    for cx, h, wl, col, s in [(x0 + 280, 600, 520, BLUE_L, 'תדר נמוך'), (x1 - 280, 200, 170, ORANGE, 'תדר גבוה')]:
        top = mast(d, (cx, g), h, col); wave(d, cx - 230, cx + 230, g - h - 90 if h < 400 else y0 + 90, 40, wl, col, 4)
        label(d, (cx, g + 60), s, F(40), col); label(d, (cx + 80, g - h / 2), 'אנטנה', F(32, False), TEXT, 'l')

def s04():
    im, d = base(); left_panel(d, 'גל קצר, אנטנה קצרה')
    box = inner(); x0, y0, x1, y1 = box; mid = (x0 + x1) / 2
    for b, n, foc, h, s, col in [((mid + 5, y0, x1, y1 - 200), 'u13_longwave', (0.5, 0.5), 'גל ארוך · תדר נמוך', 'תורן של 330 m', BLUE_L),
                                 ((x0, y0, mid - 5, y1 - 200), 'u13_vhf_whip', (0.5, 0.35), 'VHF · תדר גבוה', 'מוט של כמטר', ORANGE)]:
        d = photo(im, b, n, focus=foc); credit(d, b, n)
        box_text(d, (b[0] + 10, y1 - 190, b[2] - 10, y1 - 10), [(h, 36, col), (s, 34, TEXT)], col)
    right_block(d, 'גודל האנטנה', 'האנטנה בנויה לפי אורך הגל, רבע או חצי ממנו. ככל שהתדר גבוה יותר, היא קטנה יותר.',
                ('שאלה מהמאגר · 111', 'במה תלוי גודלה הפיזי של האנטנה?',
                 ['תדר גבוה יותר, אנטנה קטנה יותר', 'קצב הנתונים שרוצים להעביר', 'אם האנטנה לשידור או לקליטה', 'כל התשובות נכונות'], 0))
    save(im, 's04_antenna_q111')
def s05():
    im, d = base(); left_panel(d, 'אורך מותאם לתדר')
    box = inner(); x0, y0, x1, y1 = box
    d, P = photo_map(im, box, 'u10_arch', (0.45, 0.25))
    w = P(1160, 60); tag(d, (w[0] + 60, w[1] + 120), 'אנטנת VHF', ORANGE, 34, 'l'); pointer(d, (w[0] + 50, w[1] + 90), w)
    box_text(d, (x0 + 60, y1 - 210, x1 - 60, y1 - 40), [('האנטנה מוליכה ובאורך שמתאים לתחום', 38, GREEN_L), ('את הערוץ והקול מטפל המכשיר', 34, TEXT)])
    right_block(d, 'מה נדרש מהאנטנה', 'אורך שמתאים לתחום התדר של המכשיר, לשידור ולקליטה.',
                ('שאלה מהמאגר · 72', 'מה נדרש מאנטנת מכשיר הקשר?',
                 ['מחומרים אקריליים בלבד לבידוד', 'אורך מתאים לתחום תדר השידור והקליטה', 'לפרק את גל השמע מהגל הנושא', 'לברור את הערוץ שייקלט'], 1))
    save(im, 's05_antenna_q72')

def sub(box):
    """Off-screen canvas for a panel, so globe drawings stay inside it; paste with sub_paste."""
    x0, y0, x1, y1 = [int(v) for v in box]; s = Image.new('RGB', (x1 - x0, y1 - y0), SKY); return s, ImageDraw.Draw(s), (x0, y0)

def propagation(night=False, W=1180, H=1060):
    s, d, _ = sub((0, 0, W, H)); c = (W / 2, H + 1500); R = 1700
    g = RL.globe_img(R, 30, 30); s.paste(g, (int(c[0] - R), int(c[1] - R)), g); d = ImageDraw.Draw(s)
    ion = 2250
    d.arc((c[0] - ion, c[1] - ion, c[0] + ion, c[1] + ion), 240, 300, fill=(200, 110, 190), width=40)
    return s, d, c, R, ion

def s06():
    im, d = base(); left_panel(d, 'קרקע, רקיע, ישיר')
    box = inner(); x0, y0, x1, y1 = box
    s, e, c, R, ion = propagation(W=int(x1 - x0), H=int(y1 - y0))
    a, b = pt(c, R, -18), pt(c, R, 18)
    e.arc((c[0] - R - 22, c[1] - R - 22, c[0] + R + 22, c[1] + R + 22), 252, 288, fill=GREEN_L, width=7)
    top = pt(c, ion - 20, 0); e.line((a, top, b), fill=CORAL, width=6)
    m1, m2 = pt(c, R + 160, -9), pt(c, R + 160, 9); e.line((m1, m2), fill=ORANGE, width=7)
    for k in (-9, 9): e.line((pt(c, R, k), pt(c, R + 160, k)), fill=WHITE, width=6)
    for p in (m1, m2): dot(e, p, 10, ORANGE)
    tag(e, (top[0], top[1] - 70), 'יונוספירה · 60-400 km', (230, 160, 220), 32)
    tag(e, (top[0] + 260, top[1] + 200), 'גל רקיע', CORAL, 36); tag(e, ((m1[0] + m2[0]) / 2, m1[1] - 60), 'גל ישיר · VHF', ORANGE, 34)
    tag(e, (200, s.height - 170), 'גל קרקע', GREEN_L, 36)
    im.paste(s, (int(x0), int(y0))); d = ImageDraw.Draw(im)
    right_block(d, 'שלוש דרכים', 'גל קרקע עוקב אחרי פני הארץ. גל רקיע מוחזר מהיונוספירה: ככל שהיא גבוהה יותר, הוא נוחת רחוק יותר. בלילה היא עולה. גל ישיר צריך קשר עין.')
    save(im, 's06_propagation')

def s07():
    im, d = base(); left_panel(d, 'יום ולילה')
    box = inner(); x0, y0, x1, y1 = box
    s, e, c, R, ion = propagation(W=int(x1 - x0), H=int(y1 - y0))
    e.arc((c[0] - ion - 170, c[1] - ion - 170, c[0] + ion + 170, c[1] + ion + 170), 240, 300, fill=(120, 90, 160), width=24)
    for night, col, t in [(False, ORANGE, 'יום'), (True, BLUE_L, 'לילה')]:
        h = ion - 20 + (170 if night else 0); a = pt(c, R, -18); top = pt(c, h, -3 if night else -3); b = pt(c, R, 18 if night else 12)
        e.line((a, top, b), fill=col, width=6); tag(e, (b[0] + 10, b[1] - 60), t, col, 36)
    im.paste(s, (int(x0), int(y0))); d = ImageDraw.Draw(im)
    right_block(d, 'H F בלילה', 'היונוספירה עולה בלילה, והגל חוזר למקום אחר. לכן מחליפים תדר.',
                ('שאלה מהמאגר · 124', 'מדוע לפעמים משנים תדר בלילה, בהקמת קשר בתדרי H.F?',
                 ['בגלל שינוי גובה היונוספירה', 'תנאי קליטה גרועים יותר בלילה', 'תנאי קליטה טובים יותר בלילה', 'רק בטווח של מעל 1000 מייל'], 0))
    save(im, 's07_hf_night_q124')
def s08():
    im, d = base(); left_panel(d, 'MF, VHF, UHF')
    box = inner(); x0, y0, x1, y1 = box; d.rectangle(box, fill=SKY)
    cols = [('MF', ['300 kHz-3 MHz', '100-1000 m', 'גל קרקע', 'עד 400 מייל', 'NAVTEX']),
            ('VHF', ['30-300 MHz', '1-10 m', 'גל ישיר', 'גובה האנטנה', 'קשר + DSC']),
            ('UHF', ['300 MHz-3 GHz', '0.1-1 m', 'גל ישיר', 'גובה האנטנה', 'EPIRB'])]
    heads = ['תדר', 'אורך גל', 'התפשטות', 'טווח', 'מכשיר']; cw = (x1 - x0 - 200) / 3
    for r, h in enumerate(heads): text_r(d, x1 - 20, y0 + 160 + r * 175, h, F(34), MUTED)
    for j, (h, vals) in enumerate(cols):
        cx = x1 - 200 - cw * (j + 0.5); col = GREEN_L if h == 'VHF' else ORANGE
        if h == 'VHF': d.rounded_rectangle((cx - cw / 2 + 8, y0 + 20, cx + cw / 2 - 8, y1 - 20), 24, outline=GREEN_L, width=4)
        label(d, (cx, y0 + 80), h, F(56), col)
        for r, v in enumerate(vals): label(d, (cx, y0 + 180 + r * 175), v, F(34, False), TEXT)
    right_block(d, 'שלושה תחומים', 'MF לגל קרקע ול-NAVTEX. VHF לקשר ול-DSC. UHF ל-EPIRB. ב-VHF וב-UHF הטווח תלוי בגובה האנטנה.')
    save(im, 's08_bands')

def band_bar(d, box, note=None):
    x0, y0, x1, y1 = box; d.rectangle(box, fill=SKY)
    bx0, bx1, by = x0 + 80, x1 - 80, y0 + 360; f = lambda mhz: bx0 + (mhz - 30) / 270 * (bx1 - bx0)
    d.rounded_rectangle((bx0, by - 40, bx1, by + 40), 20, fill=(40, 60, 95))
    d.rounded_rectangle((f(156), by - 70, f(174), by + 70), 10, fill=GREEN_L)
    for v in (30, 300): label(d, (f(v), by + 100), f'{v}', F(36), MUTED)
    label(d, ((bx0 + bx1) / 2, by - 130), 'VHF · 30-300 MHz', F(42), MUTED)
    tag(d, ((f(156) + f(174)) / 2, by + 190), 'ימי · 156-174 MHz', GREEN_L, 44)
    if note: box_text(d, (x0 + 100, y1 - 300, x1 - 100, y1 - 60), note)

def s08b():
    im, d = base(); left_panel(d, 'הרץ, קילו, מגה, ג׳יגה')
    box = inner(); x0, y0, x1, y1 = box; d.rectangle(box, fill=SKY)
    for i, (u, v) in enumerate([('Hz', '1 בשנייה'), ('kHz', '1,000'), ('MHz', '1,000,000'), ('GHz', '1,000,000,000')]):
        bx1 = x1 - 20 - i * 290
        box_text(d, (bx1 - 270, y0 + 30, bx1, y0 + 230), [(u, 48, GREEN_L), (v, 30, TEXT)])
    bx0, bx1, by = x0 + 70, x1 - 70, y0 + 560; f = lambda mhz: bx0 + (mhz - 30) / 270 * (bx1 - bx0)
    label(d, ((bx0 + bx1) / 2, by - 230), 'VHF · 30-300 MHz', F(42), MUTED)
    d.rounded_rectangle((bx0, by - 40, bx1, by + 40), 20, fill=(40, 60, 95))
    for lo, hi, s, col, dy in [(88, 108, 'רדיו FM', BLUE_L, 1), (118, 137, 'מטוסים', ORANGE, -1), (156, 174, 'ימי', GREEN_L, 1)]:
        d.rounded_rectangle((f(lo), by - 70, f(hi), by + 70), 10, fill=col)
        tag(d, ((f(lo) + f(hi)) / 2, by + dy * 140), s, col, 38)
    for v in (30, 300): label(d, (f(v), by + 100), f'{v}', F(34), MUTED)
    box_text(d, (x0 + 100, y1 - 260, x1 - 100, y1 - 40), [('ITU מחלק את התדרים', 44, GREEN_L), ('לים · 156-174 MHz', 40, TEXT)])
    right_block(d, 'יחידות תדר', 'הרץ זו תנודה בשנייה. ה-VHF כולו 30 עד 300 מגה הרץ, וה-ITU מקצה לכל שירות פרוסה. לים: 156 עד 174.')
    save(im, 's08b_units')
def s09():
    im, d = base(); left_panel(d, 'ה-VHF הימי')
    box = inner(); band_bar(d, box, [('חלק קטן מתחום ה-VHF', 42, GREEN_L)])
    right_block(d, '156-174 MHz', 'תחום ה-VHF כולו הוא 30 עד 300 מגה הרץ. הימי הוא רק פרוסה ממנו.',
                ('שאלה מהמאגר · 125', 'מהו תחום התדרים במכשיר V.H.F הימי?',
                 ['30 מ״הרץ עד 300 ק״הרץ', '30 מ״הרץ עד 300 מ״הרץ', '156 מ״הרץ עד 174 מ״הרץ', '1600 מ״הרץ עד 2850 מ״הרץ'], 2))
    save(im, 's09_vhf_band_q125')

def s10():
    im, d = base(); left_panel(d, 'למה דווקא שם')
    box = inner(); band_bar(d, box, [('הוקצה לשירות הימי הנייד', 42, GREEN_L), ('ע״י הארגון הבין לאומי לתקשורת', 36, TEXT)])
    right_block(d, 'הקצאה בינלאומית', 'כך הוחלט בהסכם בין המדינות. הגל הקצר והטווח המוגבל הם תוצאה, לא הסיבה.',
                ('שאלה מהמאגר · 91', 'ספינות מחויבות במכשיר קשר בתחום 156 עד 174 MHz. מדוע?',
                 ['התחום שהוקצב לשירות הימי הנייד', 'גל קצר מ-2 מטר, אנטנות קטנות', 'טווח מוגבל, פחות הפרעות הדדיות', 'FM מונע הפרעות ברקים'], 0))
    save(im, 's10_why_band_q91')

def s11():
    im, d = base(); left_panel(d, 'A M מול F M')
    box = inner(); x0, y0, x1, y1 = box; d.rectangle(box, fill=SKY)
    rows = [('גל נושא', None, None, MUTED), ('A M · משנים גובה', lambda t: 0.35 + 0.65 * abs(math.sin(t * math.pi * 2)), None, ORANGE),
            ('F M · משנים תדר', None, lambda t: 0.45 + 0.9 * (0.5 + 0.5 * math.sin(t * math.pi * 2)), GREEN_L)]
    for i, (s, am, fm, col) in enumerate(rows):
        yc = y0 + 170 + i * 330; wave(d, x0 + 60, x1 - 60, yc, 95, 70, col, 4, am, fm)
        tag(d, ((x0 + x1) / 2, yc + 140), s, col, 38)
    right_block(d, 'אפנון', 'על גל נושא מעמיסים את המידע. A M משנה את הגובה, F M משנה את התדר.',
                ('שאלה מהמאגר · 112', 'בשיטת אפנון מסוג FM:',
                 ['משנים את אמפליטודת הגל הנושא', 'משנים את פאזת הגל הנושא', 'משנים את תדר הגל הנושא לפי המידע', 'משנים את אורך האנטנה'], 2))
    save(im, 's11_modulation_q112')

VHF = {'screen': (2116, 1367), 'dw': (1920, 1823), 'c16': (2943, 1543), 'distress': (1406, 1725), 'volsql': (3145, 1725), 'chan': (2702, 1758), 'mic': (293, 781)}

def s12():
    im, d = base(); left_panel(d, 'הפקדים')
    box = inner(); x0, y0, x1, y1 = box
    bx = (x0, y0, x1, y0 + 760)
    d, P = photo_map(im, bx, 'u13_vhf', (0.62, 0.6)); credit(d, bx, 'u13_vhf')
    for k, s, col, dxy in [('volsql', 'VOL · SQL', GREEN_L, (-60, -170)), ('c16', '16', CORAL, (40, -230)), ('dw', 'DW', ORANGE, (0, 120)),
                           ('distress', 'DISTRESS', CORAL, (-40, 130)), ('screen', 'ערוץ · מיקום', BLUE_L, (0, -240))]:
        p = P(*VHF[k]); q = (p[0] + dxy[0], p[1] + dxy[1]); pointer(d, q, p, col); tag(d, q, s, col, 32)
    row_boxes(d, x0 + 10, x1 - 10, y0 + 790, 250, [[('SQUELCH', 36, GREEN_L), ('משקט רחש', 30, TEXT)], [('16', 40, CORAL), ('מעבר מהיר', 30, TEXT)],
                                                   [('Hi / Lo', 36, ORANGE), ('הספק', 30, TEXT)], [('DW', 40, ORANGE), ('האזנה כפולה', 30, TEXT)]], size=36)
    right_block(d, 'המכשיר', 'הדלקה ועוצמה, משקט רחש, בורר ערוצים, ערוץ 16, הספק, האזנה כפולה, וכפתור מצוקה מתחת למכסה.')
    save(im, 's12_controls')

def dual(d, box):
    x0, y0, x1, y1 = box; d.rectangle(box, fill=SKY); c = ((x0 + x1) / 2, y0 + 420)
    d.rounded_rectangle((c[0] - 170, c[1] - 110, c[0] + 170, c[1] + 110), 26, fill=(30, 36, 44), outline=WHITE, width=4)
    label(d, c, 'DW', F(70), ORANGE)
    for side, ch, s, col in [(-1, '16', 'קריאה ומצוקה', CORAL), (1, '72', 'ערוץ עבודה', GREEN_L)]:
        p = (c[0] + side * 380, c[1]); arrow(d, p, (c[0] + side * 185, c[1]), col, 8, 30)
        label(d, (p[0] + side * 60, p[1] - 30), ch, F(80), col); label(d, (p[0] + side * 60, p[1] + 60), s, F(34, False), TEXT)
    return c

def s13():
    im, d = base(); left_panel(d, 'DUAL WATCH')
    box = inner(); x0, y0, x1, y1 = box
    dual(d, box)
    box_text(d, (x0 + 80, y1 - 330, x1 - 80, y1 - 60), [('מדברים בערוץ הנבחר', 40, GREEN_L), ('שידור ב-16 פורץ פנימה', 40, CORAL)])
    right_block(d, 'האזנה כפולה', 'אתה בערוץ עבודה, ולא מפספס את ערוץ הקריאה והמצוקה.',
                ('שאלה מהמאגר · 55', 'מה תפקידו של פקד DUAL WATCH במכשיר הקשר?',
                 ['האזנה לנבחר, שידור רק ב-16', 'האזנה ושידור בנבחר, פריצה כשיש הודעה ב-16', 'משמרת כפולה ליד המכשיר וליד ההגה', 'משמרת כפולה DSC וקשר דיבור'], 1))
    save(im, 's13_dualwatch_q55')

def s14():
    im, d = base(); left_panel(d, '16 + ערוץ נבחר')
    box = inner(); x0, y0, x1, y1 = box
    bx = (x0, y0, x1, y0 + 760)
    d, P = photo_map(im, bx, 'u13_vhf', (0.55, 0.62)); credit(d, bx, 'u13_vhf')
    p = P(*VHF['dw']); circle(d, p, 70, ORANGE, 7); tag(d, (p[0], p[1] - 130), 'DW', ORANGE, 40)
    row_boxes(d, x0 + 10, x1 - 10, y0 + 790, 250, [[('16', 60, CORAL), ('קריאה ומצוקה', 32, TEXT)], [('+', 70, WHITE)], [('ערוץ נבחר', 44, GREEN_L), ('לבחירתך', 32, TEXT)]])
    right_block(d, 'שני ערוצים', 'DUAL WATCH מאזין ל-16 ולעוד ערוץ אחד שבחרת. בלי קשר ל-SIMPLEX או DUPLEX.',
                ('שאלה מהמאגר · 116', 'למה משמש כפתור ה-DUAL-WATCH במכשיר ה-V.H.F?',
                 ['16 וערוץ SIMPLEX בלבד', 'מבטל את ערוצי ה-DUPLEX', 'מאזין גם ל-SIMPLEX בנוסף ל-DUPLEX', 'מאזין לערוץ 16 ולערוץ נבחר נוסף'], 3))
    save(im, 's14_dualwatch_q116')

def s15():
    im, d = base(); left_panel(d, 'כיוון שדורש ניסיון')
    box = inner(); x0, y0, x1, y1 = box; mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    tiles = [((mx + 5, y0, x1, my - 5), 'u13_vhf', (0.82, 0.68), 'משקט רחש'), ((x0, y0, mx - 5, my - 5), 'u9_screen', (0.5, 0.5), 'הפרעות במכ״מ'),
             ((mx + 5, my + 5, x1, y1), 'u7_helm_displays', (0.5, 0.5), 'היגוי ידני'), ((x0, my + 5, mx - 5, y1), 'u7_cruise_anemo', (0.5, 0.4), 'מתיחת מפרש')]
    for b, n, foc, s in tiles:
        d = photo(im, b, n, focus=foc); tag(d, ((b[0] + b[2]) / 2, b[3] - 50), s, ORANGE, 36)
    right_block(d, 'כל התשובות', 'תלוי בתנאים, צריך ניסיון, וכיוון קיצוני עובד הפוך. SQUELCH חזק מדי משתיק גם תחנה חלשה.',
                ('שאלה מהמאגר · 57', 'מה משותף למשקט רחש, למנתחי הפרעות במכ״מ, להיגוי ידני ולמתיחת מפרש?',
                 ['הכיוון אינו חד משמעי בכל תנאי', 'דרושה מיומנות מניסיון מצטבר', 'כיוון קיצוני יפעל הפוך', 'כל התשובות נכונות'], 3))
    save(im, 's15_squelch_q57')

def horizon(W, H, h1, h2, col=ORANGE):
    s, d, _ = sub((0, 0, W, H)); c = (W / 2, H + 2600); R = 2800
    g = RL.globe_img(R, 20, 0); s.paste(g, (int(c[0] - R), int(c[1] - R)), g); d = ImageDraw.Draw(s)
    a, b = pt(c, R, -9), pt(c, R, 9); ta, tb = pt(c, R + h1, -9), pt(c, R + h2, 9)
    d.line((a, ta), fill=WHITE, width=7); d.line((b, tb), fill=WHITE, width=7)
    d.line((ta, tb), fill=col, width=6); dot(d, ta, 10, col); dot(d, tb, 10, col)
    return s, d, ta, tb
def s16():
    im, d = base(); left_panel(d, 'טווח = אופק')
    box = inner(); x0, y0, x1, y1 = box
    s, e, ta, tb = horizon(int(x1 - x0), 560, 120, 320)
    tag(e, (ta[0], ta[1] - 60), 'יאכטה', WHITE, 32); tag(e, (tb[0], tb[1] - 60), 'תחנת חוף', WHITE, 32)
    im.paste(s, (int(x0), int(y0))); d = ImageDraw.Draw(im)
    for i, (s, nm) in enumerate([('יאכטה ליאכטה', 16), ('יאכטה לספינה', 30), ('יאכטה לתחנת חוף', 50)]):
        y = y0 + 610 + i * 140; w = (x1 - x0 - 460) * nm / 60
        d.rounded_rectangle((x1 - 40 - w, y, x1 - 40, y + 100), 18, fill=(30, 110, 80))
        text_r(d, x1 - 60, y + 26, f'{nm} NM', F(40), WHITE); text_r(d, x1 - 70 - w, y + 26, s, F(36, False), TEXT)
    right_block(d, 'טווחי קשר', 'גל ישיר, אז הטווח הוא טווח האופק. בתיאוריה עד 60 מייל. אנטנה גבוהה רואה רחוק יותר.')
    save(im, 's16_range')

def s17():
    im, d = base(); left_panel(d, 'מה קובע את הטווח')
    box = inner(); x0, y0, x1, y1 = box
    s, e, ta, tb = horizon(int(x1 - x0), 560, 200, 200, GREEN_L); im.paste(s, (int(x0), int(y0))); d = ImageDraw.Draw(im)
    row_boxes(d, x0 + 10, x1 - 10, y0 + 600, 400, [[('קו ראייה', 36, GREEN_L), ('בלי מכשולים', 30, TEXT)], [('הספק', 36, GREEN_L), ('השידור', 30, TEXT)],
                                                   [('גובה', 36, GREEN_L), ('האנטנות', 30, TEXT)], [('התפשטות', 36, GREEN_L), ('גלי הרדיו', 30, TEXT)]], size=36)
    right_block(d, 'הטווח ב-VHF', 'קו ראייה בין האנטנות, הספק, גובה האנטנות ותנאי התפשטות. דילוגים מהיונוספירה זה H F.',
                ('שאלה מהמאגר · 58, 172', 'מה משפיע בעיקר על טווח הקשר בתחום התג״מ?',
                 ['שעת היממה, מליחות, מהירות הספינה', 'מרחב בלי מכשולים, הספק, גובה אנטנות, התפשטות',
                  'הערוץ, עוצמת הדיבור, עונת השנה', 'טמפרטורה, דילוגים מהיונוספירה'], 1))
    save(im, 's17_range_q58')

def s18():
    im, d = base(); left_panel(d, 'VHF נייד')
    box = inner(); x0, y0, x1, y1 = box; mid = (x0 + x1) / 2
    pb = (mid + 5, y0, x1, y1)
    d, P = photo_map(im, pb, 'u13_handheld', (0.45, 0.5)); credit(d, pb, 'u13_handheld')
    for i, (t, v, col) in enumerate([('הספק מרבי', '5 W', ORANGE), ('מצב Lo', '1 W', GREEN_L), ('טווח', '~3 NM', BLUE_L)]):
        readout(d, (x0 + 30, y0 + 30 + i * 300, mid - 30, y0 + 270 + i * 300), t, v, col)
    tag(d, ((x0 + mid) / 2, y1 - 80), 'עמיד למים · סוללה נוספת', TEXT, 30)
    right_block(d, 'נייד', 'ציוד חובה ב-GMDSS. עמיד למים, 5 וואט מרבי, ובמצב Lo וואט אחד.',
                ('שאלה מהמאגר · 127', 'למשדר V.H.F נייד יש יכולת להקטין את הספק השידור עד:', ['0.1W', '1W', '5W', '10W'], 1))
    save(im, 's18_handheld_q127')

def s19():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u13_vhf', focus=(0.6, 0.55)); credit(d, (0, 0, 1300, 1440), 'u13_vhf')
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['GMDSS · VHF, DSC, NAVTEX, EPIRB, SART', 'תדר גבוה · גל קצר · אנטנה קצרה', 'גל קרקע, רקיע וישיר', 'VHF · גל ישיר, טווח לפי גובה',
             'ימי · 156-174 MHz', 'F M משנה את התדר', 'DW · ערוץ 16 + ערוץ נבחר', 'נייד · 5W, במצב Lo 1W']
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 6 else ORANGE)
        text_r(d, 2380, y + 20, s, F(46, False), TEXT)
    save(im, 's19_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s08b, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19]
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
