"""Lesson 1 (l30): הרשת הגיאוגרפית. Original drawn illustrations (orthographic globe renderer)."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from bidi.algorithm import get_display

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cards')
os.makedirs(OUT, exist_ok=True)
W, H = 2560, 1440
NAVY = (14, 26, 45); NAVY2 = (10, 18, 34); PANEL = (24, 40, 66); PANEL_D = (10, 20, 38)
GREEN = (34, 160, 90); GREEN_L = (46, 204, 113); TEXT = (240, 245, 250); MUTED = (160, 178, 200)
ORANGE = (220, 160, 60); CORAL = (224, 129, 124); BLUE = (90, 150, 220); BLUE_L = (140, 190, 245)
OCEAN = (28, 78, 130); OCEAN_D = (18, 52, 92); GRID = (120, 170, 215)
FB = 'C:/Windows/Fonts/arialbd.ttf'; FR = 'C:/Windows/Fonts/arial.ttf'
SUB = 'ניווט חופי ומכשירים · הרשת הגיאוגרפית'

def F(sz, bold=True): return ImageFont.truetype(FB if bold else FR, sz)
import re as _re
# LTR runs (numbers, Latin, formulas like 154 ÷ 15 = 10, +10, 179°31'W, 7°30') are swapped for one strong-L
# placeholder each (private-use chars are class L), bidi'd, then restored intact in visual position
_LTR = _re.compile(r"""(?:(?:(?<=\s)|^)[+−-])?[0-9A-Za-z](?:[0-9A-Za-z°'".:+−\-÷=×/ ]*[0-9A-Za-z°'])?""")
def he(s):
    runs = []
    def ph(m): runs.append(m.group(0)); return chr(0xE000 + len(runs) - 1)
    v = get_display(_LTR.sub(ph, s), base_dir='R')  # placeholders are strong L; keep the RTL paragraph base
    return ''.join(runs[ord(c) - 0xE000] if 0xE000 <= ord(c) < 0xE000 + len(runs) else c for c in v)

def text_r(d, xr, y, s, font, fill):
    t = he(s); w = d.textlength(t, font=font); d.text((xr - w, y), t, font=font, fill=fill); return w
def text_c(d, xc, y, s, font, fill):
    t = he(s); w = d.textlength(t, font=font); d.text((xc - w / 2, y), t, font=font, fill=fill)

def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ''
    for w_ in words:
        cand = (cur + ' ' + w_).strip()
        if d.textlength(he(cand), font=font) <= maxw: cur = cand
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def base():
    im = Image.new('RGB', (W, H), NAVY2)
    # soft radial glow on the right
    glow = Image.new('L', (W, H), 0); g = ImageDraw.Draw(glow)
    g.ellipse((1300, -200, 2700, 1100), fill=120); glow = glow.filter(ImageFilter.GaussianBlur(260))
    im = Image.composite(Image.new('RGB', (W, H), (22, 44, 86)), im, glow)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 14), fill=GREEN)
    return im, d

LP = (48, 24, 1268, 1424)  # left panel
def left_panel(d, caption):
    x0, y0, x1, y1 = LP
    d.rectangle((x0, y0, x1, y1), fill=PANEL_D)
    d.rectangle((x0, y0 + 300, x1, y1), fill=(17, 36, 62))
    text_c(d, (x0 + x1) / 2, y0 + 205, caption, F(64), TEXT)
    return ((x0 + x1) / 2, y0 + 300 + (y1 - y0 - 300) / 2)  # center of drawing area

RX = 2400; RC = 1880; RW = 1060
def right_block(d, title, body, q=None, y=None):
    sub = F(48, False); tf = F(128); bf = F(52, False)
    lines = wrap(d, body, bf, RW) if body else []
    qh = 0
    if q:
        head, qtext, opts, ok = q
        qlines = wrap(d, qtext, F(44), RW - 80)
        of = F(42, False); ofb = F(42)
        olines = [wrap(d, o, ofb if i == ok else of, RW - 200) for i, o in enumerate(opts)]
        qh = 30 + 60 + len(qlines) * 58 + 20 + sum(len(o) * 52 + 26 for o in olines) + 24
    total = 60 + 30 + 150 + 60 + len(lines) * 72 + (40 + qh if q else 0)
    y = y or max(60, (H - total) / 2)
    text_c(d, RC, y, SUB, sub, BLUE_L); y += 90
    text_c(d, RC, y, title, tf, TEXT); y += 170
    d.rounded_rectangle((RC - 70, y, RC + 70, y + 12), 6, fill=GREEN); y += 50
    for ln in lines:
        text_c(d, RC, y, ln, bf, TEXT); y += 72
    if q:
        y += 20
        bx0, bx1 = RC - RW / 2 - 20, RC + RW / 2 + 20
        d.rounded_rectangle((bx0, y, bx1, y + qh), 26, fill=PANEL, outline=(60, 90, 130), width=3)
        yy = y + 26
        text_r(d, bx1 - 40, yy, head, F(38), ORANGE); yy += 60
        for ln in qlines: text_r(d, bx1 - 40, yy, ln, F(44), TEXT); yy += 58
        yy += 20
        for i, ol in enumerate(olines):
            good = i == ok; h = len(ol) * 52 + 14
            if good:
                d.rounded_rectangle((bx0 + 24, yy - 6, bx1 - 24, yy + h - 6), 16, fill=(24, 80, 60), outline=GREEN_L, width=3)
            letter = 'אבגד'[i] + ':'
            text_r(d, bx1 - 44, yy, letter, ofb, GREEN_L if good else MUTED)
            for j, ln in enumerate(ol):
                text_r(d, bx1 - 110, yy + j * 52, ln, ofb if good else of, GREEN_L if good else TEXT)
            yy += len(ol) * 52 + 26

# ---------- globe ----------
def proj(lat, lon, lat0, lon0):
    la, lo, la0 = map(math.radians, (lat, lon - lon0, lat0))
    x = math.cos(la) * math.sin(lo)
    y = math.cos(la0) * math.sin(la) - math.sin(la0) * math.cos(la) * math.cos(lo)
    vis = math.sin(la0) * math.sin(la) + math.cos(la0) * math.cos(la) * math.cos(lo) > 0
    return x, y, vis

def rot(x, y, ang):
    a = math.radians(ang); return x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)

class Globe:
    def __init__(s, d, cx, cy, R, lat0=20, lon0=0, tilt=0):
        s.d, s.cx, s.cy, s.R, s.lat0, s.lon0, s.tilt = d, cx, cy, R, lat0, lon0, tilt
    def pt(s, lat, lon):
        x, y, v = proj(lat, lon, s.lat0, s.lon0)
        x, y = rot(x, y, s.tilt)
        return (s.cx + s.R * x, s.cy - s.R * y), v
    def sphere(s):
        d, cx, cy, R = s.d, s.cx, s.cy, s.R
        for i in range(40, 0, -1):  # shaded sphere
            f = i / 40; c = tuple(int(OCEAN_D[k] + (OCEAN[k] - OCEAN_D[k]) * (1 - f) ** 0.6) for k in range(3))
            r = R * f; ox, oy = -R * 0.18 * (1 - f), -R * 0.22 * (1 - f)
            d.ellipse((cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r), fill=c)
        d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=(150, 195, 240), width=5)
    def path(s, pts, fill, width, dash=False, back=None):
        segs, cur = [], []
        for p, v in pts:
            if v: cur.append(p)
            else:
                if len(cur) > 1: segs.append(cur)
                cur = []
        if len(cur) > 1: segs.append(cur)
        for sg in segs:
            if dash:
                for i in range(0, len(sg) - 1, 8): s.d.line(sg[i:i + 5], fill=fill, width=width)
            else: s.d.line(sg, fill=fill, width=width, joint='curve')
    def parallel(s, lat, fill=GRID, width=2, dash=False):
        s.path([s.pt(lat, lo / 2) for lo in range(-360, 361)], fill, width, dash)
    def meridian(s, lon, fill=GRID, width=2, lat_from=-90, lat_to=90):
        s.path([s.pt(la / 2, lon) for la in range(lat_from * 2, lat_to * 2 + 1)], fill, width)
    def grid(s, step=30, fill=GRID, width=2):
        for la in range(-90 + step, 90, step): s.parallel(la, fill, width)
        for lo in range(-180, 180, step): s.meridian(lo, fill, width)
    def gc(s, a, b, fill, width, n=200):
        (la1, lo1), (la2, lo2) = a, b
        def v(la, lo):
            la, lo = math.radians(la), math.radians(lo)
            return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))
        p, q = v(la1, lo1), v(la2, lo2)
        om = math.acos(sum(i * j for i, j in zip(p, q)))
        pts = []
        for i in range(n + 1):
            t = i / n; k1 = math.sin((1 - t) * om) / math.sin(om); k2 = math.sin(t * om) / math.sin(om)
            x, y, z = (k1 * p[j] + k2 * q[j] for j in range(3))
            pts.append(s.pt(math.degrees(math.asin(z)), math.degrees(math.atan2(y, x))))
        s.path(pts, fill, width)

def dot(d, p, r, fill, outline=None):
    d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=fill, outline=outline, width=4)

def label(d, p, s, font, fill, anchor='c', dx=0, dy=0):
    t = he(s); w = d.textlength(t, font=font); h = font.size
    x = {'c': p[0] - w / 2, 'l': p[0], 'r': p[0] - w}[anchor] + dx
    d.text((x, p[1] - h / 2 + dy), t, font=font, fill=fill)

def arrow(d, a, b, fill, width=8, head=34):
    d.line((a, b), fill=fill, width=width)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p1 = (b[0] - head * math.cos(ang - 0.45), b[1] - head * math.sin(ang - 0.45))
    p2 = (b[0] - head * math.cos(ang + 0.45), b[1] - head * math.sin(ang + 0.45))
    d.polygon([b, p1, p2], fill=fill)

def save(im, sid): im.save(os.path.join(OUT, sid + '.png')); print('ok', sid)

# ---------- cards ----------
def s01():
    im, d = base()
    cx, cy = 780, 740
    g = Globe(d, cx, cy, 520, lat0=25, lon0=20); g.sphere(); g.grid(15, (95, 145, 200), 2); g.grid(30, GRID, 3)
    g.parallel(0, ORANGE, 7); g.meridian(0, CORAL, 7)
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 1', F(56, False), BLUE_L)
    text_c(d, RC, 500, 'הרשת הגיאוגרפית', F(150), TEXT)
    d.rounded_rectangle((RC - 80, 700, RC + 80, 714), 7, fill=GREEN)
    for i, s in enumerate(['ציר וקטבים · קו המשווה', 'מעגל גדול ומעגל קטן', 'קווי רוחב וקווי אורך', 'אתר גיאוגרפי']):
        text_c(d, RC, 780 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    im, d = base(); c = left_panel(d, 'ציר כדור הארץ')
    cx, cy = c[0], c[1] + 10; R = 330
    g = Globe(d, cx, cy, R, lat0=0, lon0=0, tilt=-23.5); g.sphere(); g.grid(30)
    g.parallel(0, ORANGE, 6)
    npole, _ = g.pt(90, 0); spole, _ = g.pt(-90, 0)
    vx, vy = npole[0] - cx, npole[1] - cy
    d.line(((cx - vx * 1.28, cy - vy * 1.28), (cx + vx * 1.28, cy + vy * 1.28)), fill=TEXT, width=6)
    d.line(((cx, cy - R * 1.3), (cx, cy + R * 1.3)), fill=(110, 130, 160), width=3)
    dot(d, npole, 16, CORAL); dot(d, spole, 16, CORAL)
    label(d, (cx + vx * 1.28, cy + vy * 1.28 - 50), 'קוטב צפוני N', F(44), TEXT)
    label(d, (cx - vx * 1.28, cy - vy * 1.28 + 50), 'קוטב דרומי S', F(44), TEXT)
    label(d, (cx + 70, cy - R * 1.18), '23.5°', F(50), ORANGE, 'l')
    # rotation arrow west -> east, drawn in front across the globe
    pts = [g.pt(38, lo)[0] for lo in range(-60, 61, 3)]
    d.line(pts, fill=GREEN_L, width=10); arrow(d, pts[-3], pts[-1], GREEN_L, 10, 44)
    label(d, (pts[0][0] - 20, pts[0][1] - 10), 'W', F(52), GREEN_L, 'r')
    label(d, (pts[-1][0] + 30, pts[-1][1] - 10), 'E', F(52), GREEN_L, 'l')
    right_block(d, 'הציר והסיבוב', 'הכדור מסתובב סביב צירו ממערב למזרח, סיבוב אחד ביממה. לכן השמש זורחת במזרח.',
                ('שאלה מהמאגר · 2, 151', 'מדוע רואים את השמש זורחת במזרח ושוקעת במערב?',
                 ['כדור הארץ נע במהירות מערבה סביב השמש', 'כדור הארץ סובב סביב צירו ממערב למזרח', 'ציר כדור הארץ מבצע תנועה מעגלית סביב כוכב הצפון', 'כדור הארץ סובב סביב צירו ממזרח למערב'], 1))
    save(im, 's02_axis')

def s03():
    im, d = base(); c = left_panel(d, 'קו המשווה')
    cx, cy = c[0], c[1]; R = 430
    g = Globe(d, cx, cy, R, lat0=18, lon0=0); g.sphere(); g.grid(30)
    g.parallel(0, ORANGE, 9)
    label(d, (cx, cy - 190), 'חצי צפוני', F(58), TEXT); label(d, (cx, cy + 200), 'חצי דרומי', F(58), TEXT)
    label(d, (cx, cy + R + 90), '0° · קו מזרח-מערב', F(46), ORANGE)
    right_block(d, 'קו המשווה', 'מחלק את כדור הארץ לחצי צפוני ולחצי דרומי.', y=330)
    y = 760
    d.rounded_rectangle((RC - 500, y, RC + 500, y + 250), 26, fill=PANEL, outline=(60, 90, 130), width=3)
    text_c(d, RC, y + 40, '40,000 ק"מ  =  21,600 מייל ימי', F(64), ORANGE)
    text_c(d, RC, y + 150, '360° × 60 דקות = 21,600 דקות', F(48, False), TEXT)
    save(im, 's03_equator')

def s04():
    im, d = base(); c = left_panel(d, 'הדרך הקצרה ביותר')
    cx, cy = c[0], c[1] + 20; R = 450
    R = 400; cy -= 40; g = Globe(d, cx, cy, R, lat0=48, lon0=-40); g.sphere(); g.grid(30)
    gib, ny = (36.1, -5.4), (40.7, -74.0)
    # rhumb-ish constant-latitude path (dashed) vs great circle
    rh = [g.pt(36.1 + (40.7 - 36.1) * i / 120, -5.4 + (-74 + 5.4) * i / 120) for i in range(121)]
    g.path(rh, (215, 222, 232), 7, dash=True)
    g.gc(gib, ny, ORANGE, 9)
    pg, _ = g.pt(*gib); pn, _ = g.pt(*ny)
    dot(d, pg, 16, CORAL, TEXT); dot(d, pn, 16, CORAL, TEXT)
    label(d, pg, 'גיברלטר', F(46), TEXT, 'l', 30, 30)
    label(d, pn, 'ניו יורק', F(46), TEXT, 'r', -30, 30)
    label(d, (cx, cy - R - 50), 'מעגל גדול', F(46), ORANGE)
    d.line(((LP[0] + 120, LP[3] - 90), (LP[0] + 200, LP[3] - 90)), fill=ORANGE, width=9)
    label(d, (LP[0] + 220, LP[3] - 90), 'מעגל גדול, הקצר ביותר', F(40, False), TEXT, 'l')
    for i in range(0, 80, 20): d.line(((LP[0] + 700 + i, LP[3] - 90), (LP[0] + 712 + i, LP[3] - 90)), fill=(170, 180, 195), width=5)
    label(d, (LP[0] + 800, LP[3] - 90), 'קו רוחב, ארוך יותר', F(40, False), TEXT, 'l')
    right_block(d, 'מעגל גדול', 'המישור שלו עובר דרך מרכז כדור הארץ. קו המשווה וכל קווי האורך הם מעגלים גדולים.',
                ('שאלה מהמאגר · 174', 'מהו המרחק הקצר ביותר בין מיצרי גיברלטר לעיר ניו יורק?',
                 ['קטע של המעגל הגדול העובר בין שני האתרים', 'קטע של המעגל הקטן העובר בין שני האתרים', 'קו חלזוני העובר בין שני האתרים', 'אף תשובה לא נכונה'], 0))
    save(im, 's04_great_circle')

def s05():
    im, d = base(); c = left_panel(d, 'מעגל גדול מול מעגל קטן')
    cx, cy = c[0], c[1]; R = 440
    g = Globe(d, cx, cy, R, lat0=22, lon0=0); g.sphere(); g.grid(30, (80, 125, 175), 2)
    for la in (30, 60, -30, -60): g.parallel(la, BLUE_L, 6)
    g.parallel(0, ORANGE, 8)
    label(d, g.pt(60, 0)[0], 'מעגל קטן', F(40), BLUE_L, dy=-36)
    label(d, g.pt(30, 0)[0], 'מעגל קטן', F(40), BLUE_L, dy=-36)
    label(d, g.pt(0, 0)[0], 'קו המשווה · מעגל גדול', F(40), ORANGE, dy=-36)
    right_block(d, 'מעגל קטן', 'המישור שלו לא עובר דרך המרכז. כל קווי הרוחב הם מעגלים קטנים, חוץ מקו המשווה.',
                ('שאלה מהמאגר · 147', 'קווי רוחב על פני כדור הארץ הם:',
                 ['מעגלים גדולים מקבילים לקו המשווה', 'לבד מקו המשווה, מעגלים קטנים ניצבים לציר סיבוב כדור הארץ, שקוטרם הולך וקטן כלפי הקטבים', 'הקווים שלאורכם נעה השמש בסיבוב היומי, בהתאם לדקלינציה', 'זהים באורכם לקווי האורך'], 1))
    save(im, 's05_small_circle')

def s06():
    im, d = base(); c = left_panel(d, 'קו רוחב = זווית מהמשווה')
    cx, cy = c[0] - 40, c[1] + 10; R = 430
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=OCEAN, outline=(150, 195, 240), width=5)
    for la in (-60, -30, 30, 60):
        y = cy - R * math.sin(math.radians(la)); x = R * math.cos(math.radians(la))
        d.line(((cx - x, y), (cx + x, y)), fill=GRID, width=3)
    d.line(((cx - R, cy), (cx + R, cy)), fill=ORANGE, width=7)
    d.line(((cx, cy - R), (cx, cy + R)), fill=(200, 210, 225), width=3)
    phi = math.radians(40); P = (cx + R * math.cos(phi), cy - R * math.sin(phi))
    d.line(((cx, cy), P), fill=GREEN_L, width=6); d.line(((cx, cy), (cx + R, cy)), fill=GREEN_L, width=6)
    d.arc((cx - 150, cy - 150, cx + 150, cy + 150), -40, 0, fill=GREEN_L, width=7)
    label(d, (cx + 200, cy - 70), 'φ', F(64), GREEN_L)
    d.line(((cx - R * math.cos(phi), P[1]), P), fill=BLUE_L, width=6)
    dot(d, P, 14, CORAL, TEXT); dot(d, (cx, cy), 10, TEXT)
    label(d, (cx + R + 20, cy), '0°', F(50), ORANGE, 'l')
    label(d, (cx, cy - R - 50), '90° N', F(50), TEXT); label(d, (cx, cy + R + 50), '90° S', F(50), TEXT)
    label(d, (P[0] + 24, P[1] - 30), '40° N', F(46), BLUE_L, 'l')
    right_block(d, 'קו רוחב · LAT', 'נמדד כזווית מקו המשווה צפונה (N) או דרומה (S). המשווה 0°, כל קוטב 90°.',
                ('שאלה מהמאגר · 19', 'כמה מעלות שלמות יש מקו המשווה עד לכל אחד מהקטבים?',
                 ['90° עד הקוטב הצפוני ו-90° עד הקוטב הדרומי', '45° עד הקוטב הצפוני ו-45° עד הקוטב הדרומי', '180° עד הקוטב הצפוני ו-180° עד הקוטב הדרומי', '90° שמאלה לקו גריניץ\' ו-90° ימינה לקו התאריך'], 0))
    save(im, 's06_latitude')

def s07():
    im, d = base(); c = left_panel(d, 'המרחק בין קווי רוחב')
    x0, x1 = LP[0] + 120, LP[2] - 120; ytop = c[1] - 380
    ys = [ytop + i * 190 for i in range(5)]
    for i, y in enumerate(ys):
        d.line(((x0, y), (x1, y)), fill=BLUE_L if i else GRID, width=6)
        label(d, (x1, y - 34), f'{24 - i}° N', F(40), TEXT, 'r')
    for i in range(4):
        xm = x0 + 180
        a, b = (xm, ys[i] + 10), (xm, ys[i + 1] - 10)
        arrow(d, (xm, (a[1] + b[1]) / 2), a, ORANGE, 5, 22); arrow(d, (xm, (a[1] + b[1]) / 2), b, ORANGE, 5, 22)
        label(d, (xm + 30, (ys[i] + ys[i + 1]) / 2), '60 מייל', F(44), ORANGE, 'l')
    label(d, ((x0 + x1) / 2 + 150, ys[-1] + 110), '1° רוחב = 60 מייל · 1\' = מייל אחד', F(44), TEXT)
    right_block(d, 'מרחק קבוע', 'קווי הרוחב מקבילים. מעלת רוחב = 60 מייל ימי.',
                ('שאלה מהמאגר · 179', 'מהו המרחק במיילים ימיים בין שני קווי רוחב סמוכים?',
                 ['מייל אחד', 'עשרה מיילים', '60 מיילים', '100 מיילים'], 2))
    save(im, 's07_lat_distance')

def s07b():
    im, d = base(); c = left_panel(d, 'קו רוחב הוא מעגל סגור')
    cx, cy = c[0], c[1] + 20; R = 450
    g = Globe(d, cx, cy, R, lat0=35, lon0=0); g.sphere(); g.grid(30, (80, 125, 175), 2)
    g.parallel(0, ORANGE, 4); g.parallel(20, BLUE_L, 10)
    p, _ = g.pt(20, 0); label(d, p, '20° N', F(48), BLUE_L, dy=-44)
    right_block(d, 'אין לו סוף', 'קו רוחב מקיף את כל הכדור וחוזר לנקודת ההתחלה.',
                ('שאלה מהמאגר · 181', 'היכן מסתיים קו רוחב 20° N?',
                 ['בקוטב הצפוני', 'בקו גריניץ\'', 'בקו המשווה', 'הוא לא מסתיים'], 3))
    save(im, 's07b_lat_end')

def s08():
    im, d = base(); c = left_panel(d, 'קווי אורך נפגשים בקטבים')
    cx, cy = c[0], c[1] + 20; R = 450
    g = Globe(d, cx, cy, R, lat0=28, lon0=10); g.sphere()
    for la in (-60, -30, 30, 60): g.parallel(la, (80, 125, 175), 2)
    g.parallel(0, ORANGE, 5)
    for lo in range(-180, 180, 20): g.meridian(lo, BLUE_L, 3)
    g.meridian(0, CORAL, 9)
    np_, _ = g.pt(90, 0); dot(d, np_, 14, TEXT)
    label(d, (np_[0], np_[1] - 50), 'N', F(50), TEXT)
    gp, _ = g.pt(-12, 0); label(d, gp, 'גריניץ\' 0°', F(44), CORAL, 'r', -24)
    e, _ = g.pt(8, 70); label(d, e, 'E', F(56), GREEN_L)
    w, _ = g.pt(8, -50); label(d, w, 'W', F(56), GREEN_L)
    right_block(d, 'קו אורך · LONG', 'נמדד מזרחה (E) או מערבה (W) מגריניץ\', עד 180°.',
                ('שאלה מהמאגר · 148', 'קווי האורך הם:',
                 ['מעגלים גדולים ניצבים לקו המשווה ועוברים בקטבים', 'שווים באורכם לקווי הרוחב, למעט מעגל קו המשווה', 'שווים באורכם לקוסינוס קו הרוחב', 'מעגלים גדולים שמקבילים זה לזה'], 0))
    save(im, 's08_longitude')

def s08b():
    im, d = base(); c = left_panel(d, 'המרחק מתכווץ לכיוון הקוטב')
    cx, cy = c[0], c[1] + 20; R = 450
    g = Globe(d, cx, cy, R, lat0=20, lon0=0); g.sphere()
    for la in (-60, -30, 30, 60): g.parallel(la, (80, 125, 175), 2)
    for lo in range(-180, 180, 20): g.meridian(lo, BLUE_L, 3)
    g.meridian(0, CORAL, 7); g.meridian(20, CORAL, 7)
    a, _ = g.pt(0, 0); b, _ = g.pt(0, 20); d.line((a, b), fill=ORANGE, width=10)
    a2, _ = g.pt(60, 0); b2, _ = g.pt(60, 20); d.line((a2, b2), fill=ORANGE, width=10)
    label(d, (b[0] + 40, b[1] + 44), 'רחב במשווה', F(42), ORANGE, 'l')
    label(d, (b2[0] + 60, b2[1] - 50), 'צר ליד הקוטב', F(42), ORANGE, 'l')
    right_block(d, 'מרחק משתנה', 'קווי האורך נפגשים בקטבים, ולכן המרחק ביניהם קטן ככל שמתקרבים לקוטב.',
                ('שאלה מהמאגר · 180', 'האם המרחק בין שני קווי אורך סמוכים על פני כדור הארץ הוא קבוע?',
                 ['כן', 'לא', 'כן, חוץ מאשר בקו המשווה', 'בקטבים בלבד'], 1))
    save(im, 's08b_long_distance')

def s09():
    im, d = base(); c = left_panel(d, 'מבט מעל הקוטב הצפוני')
    cx, cy = c[0], c[1] + 10; R = 440
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=OCEAN, outline=(150, 195, 240), width=5)
    for r in (R / 3, 2 * R / 3): d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(80, 125, 175), width=2)
    def ray(lon): a = math.radians(lon); return (cx + R * math.sin(a), cy + R * math.cos(a))
    for lo in range(0, 360, 20): d.line(((cx, cy), ray(lo)), fill=(90, 135, 185), width=2)
    d.line(((cx, cy), ray(0)), fill=CORAL, width=7); d.line(((cx, cy), ray(180)), fill=(200, 210, 225), width=5)
    d.line((ray(40), ray(-140)), fill=ORANGE, width=9)
    d.arc((cx - 170, cy - 170, cx + 170, cy + 170), 50, 90, fill=GREEN_L, width=6)
    dot(d, (cx, cy), 12, TEXT)
    def lab(lon, s, col, k=1.13): a = math.radians(lon); label(d, (cx + R * k * math.sin(a), cy + R * k * math.cos(a)), s, F(44), col)
    lab(0, '0° גריניץ\'', CORAL); lab(180, '180°', TEXT); lab(40, '40° E', ORANGE); lab(-140, '140° W', ORANGE)
    lab(90, 'E', GREEN_L, 1.08); lab(-90, 'W', GREEN_L, 1.08)
    right_block(d, 'מעגל שלם', 'קו אורך והקו שמולו יוצרים מעגל גדול. סכומם 180°, בצדדים הפוכים.',
                ('שאלה מהמאגר · 182', 'איזה קו אורך משלים למעגל שלם את קו האורך 40° E?',
                 ['40° W', '220° E', '140° W', '220° W'], 2))
    save(im, 's09_meridian_pair')

def s09b():
    im, d = base(); c = left_panel(d, 'קו גריניץ\', 0°')
    cx, cy = c[0], c[1] + 20; R = 450
    g = Globe(d, cx, cy, R, lat0=40, lon0=0); g.sphere(); g.grid(30, (80, 125, 175), 2)
    g.meridian(0, CORAL, 10)
    p, _ = g.pt(51.5, 0); dot(d, p, 16, TEXT, CORAL)
    label(d, p, 'לונדון · גריניץ\'', F(44), TEXT, 'l', 30)
    e, _ = g.pt(10, 60); label(d, e, 'E', F(56), GREEN_L)
    w, _ = g.pt(10, -60); label(d, w, 'W', F(56), GREEN_L)
    right_block(d, 'קו האורך הראשוני', 'ממנו סופרים מזרחה ומערבה. חציו השני הוא קו 180°.',
                ('שאלה מהמאגר · 20', 'קו אורך גריניץ\' הוא:',
                 ['קו אורך ראשוני שממנו מונים את קווי האורך מזרחה ומערבה', 'קו אורך שעובר בעיירה קטנה ליד לונדון ששמה גריניץ\'', 'חצי ממעגל גדול שחציו השני הוא קו אורך 180°', 'כל התשובות נכונות'], 3))
    save(im, 's09b_greenwich')

def s10():
    im, d = base(); c = left_panel(d, 'אתר = חיתוך רוחב ואורך')
    cx, cy = c[0], c[1] + 20; R = 450
    g = Globe(d, cx, cy, R, lat0=28, lon0=-30); g.sphere(); g.grid(15, (80, 125, 175), 2)
    g.parallel(65, BLUE_L, 8); g.meridian(-45, ORANGE, 8)
    p, _ = g.pt(65, -45); dot(d, p, 20, CORAL, TEXT)
    label(d, p, '65° N  045° W', F(46), TEXT, 'r', -30, -44)
    q1, _ = g.pt(65, 30); label(d, q1, 'LAT 65° N', F(40), BLUE_L, 'l', 10, 40)
    q2, _ = g.pt(10, -45); label(d, q2, 'LONG 045° W', F(40), ORANGE, 'r', -16)
    right_block(d, 'אתר גיאוגרפי', 'נקודת החיתוך של קו רוחב וקו אורך. כותבים קודם רוחב ואחריו אורך.',
                ('שאלה מהמאגר · 1', 'מדוע חולקה מעטפת כדור הארץ לקווי אורך ורוחב?',
                 ['כדי להגדיר אתרים בנקודות החיתוך שלהם', 'כדי להדגיש את מקום הנמלים והמעגנות', 'כדי לאפשר מדידת מרחקים', 'כדי ליצור משבצות לציור מפות'], 0))
    save(im, 's10_position')

def s11():
    im, d = base()
    g = Globe(d, 640, 760, 400, lat0=25, lon0=35); g.sphere(); g.grid(30); g.parallel(0, ORANGE, 6); g.meridian(0, CORAL, 6)
    text_c(d, 1780, 180, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1710, 340, 1850, 352), 6, fill=GREEN)
    items = ['סיבוב ממערב למזרח, השמש זורחת במזרח', 'משווה וקווי אורך: מעגלים גדולים',
             'קווי רוחב: מעגלים קטנים', 'מעגל גדול = הדרך הקצרה ביותר', 'משווה עד קוטב: 90°',
             '1° רוחב = 60 מייל ימי', 'קווי אורך נפגשים בקטבים', 'אתר = רוחב + אורך']
    for i, s in enumerate(items):
        y = 410 + i * 108
        d.rounded_rectangle((1220, y, 2400, y + 88), 20, fill=PANEL)
        dot(d, (2360, y + 44), 12, GREEN_L)
        text_r(d, 2320, y + 18, s, F(50, False), TEXT)
    save(im, 's11_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s07b, s08, s08b, s09, s09b, s10, s11]
if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only: fn()
