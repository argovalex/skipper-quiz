"""Lesson 5 (l30): מצפן מגנטי. Drawn marine compass, NASA Blue Marble globe, NOAA chart (Block Island)."""
import math, os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U4 = _load('u04', 'u04_cards.py')
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import real as RL
C.OUT = os.path.join(HERE, '..', 'cards', 'מצפן מגנטי'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · מצפן מגנטי'
F, text_c, text_r, label, dot, arrow = C.F, C.text_c, C.text_r, C.label, C.dot, C.arrow
base, left_panel, right_block, save, LP, RC = C.base, C.left_panel, C.right_block, C.save, C.LP, C.RC
TEXT, ORANGE, CORAL, GREEN, GREEN_L, BLUE_L, PANEL, MUTED = C.TEXT, C.ORANGE, C.CORAL, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL, C.MUTED
dashed, arc, globe_at, equirect = U4.dashed, U4.arc, U4.globe_at, U4.equirect
WHITE = (255, 255, 255); RED = (225, 60, 55); DARK = (12, 14, 18)

def panel_area(): return (LP[0], LP[1] + 300, LP[2], LP[3])
def inner(): ax0, ay0, ax1, ay1 = panel_area(); return (ax0 + 20, ay0 + 20, ax1 - 20, ay1 - 20)
def polar_pt(c, r, a): a = math.radians(a); return (c[0] + r * math.sin(a), c[1] - r * math.cos(a))

def sea(im, box, lon=(-150, -138), lat=(-22, -12), dim=1.25):
    """Open-ocean Blue Marble texture as a top-view sea surface."""
    x0, y0, x1, y1 = box
    s = equirect(x1 - x0, y1 - y0, lon[0], lon[1], lat[0], lat[1], dim).filter(ImageFilter.GaussianBlur(2))
    im.paste(s, (x0, y0)); ImageDraw.Draw(im).rectangle(box, outline=(70, 100, 140), width=3)

def chart(im, box, fx0=0.0, fy0=0.0, fx1=1.0, fy1=1.0):
    """NOAA chart (Block Island) crop scaled into box. Returns pt(fx, fy) in full-chart fractions."""
    ch = Image.open(os.path.join(RL.A, 'chart_bi.png')).convert('RGB'); W, H = ch.size
    crop = ch.crop((int(fx0 * W), int(fy0 * H), int(fx1 * W), int(fy1 * H)))
    x0, y0, x1, y1 = box; im.paste(crop.resize((x1 - x0, y1 - y0), Image.LANCZOS), (x0, y0))
    ImageDraw.Draw(im).rectangle(box, outline=(230, 235, 245), width=4)
    return lambda fx, fy: (x0 + (fx - fx0) / (fx1 - fx0) * (x1 - x0), y0 + (fy - fy0) / (fy1 - fy0) * (y1 - y0))

# chart landmarks (fractions of chart_bi.png)
NLIGHT = (0.495, 0.308); SELIGHT = (0.640, 0.730); TOWER = (0.405, 0.613)

# ---------- marine compass ----------
def compass(im, c, R, heading=0, north_up=False, deflect=0, lubber=True, needle=False):
    """Top view of a marine compass. Helm view (default): lubber line fixed at top, card turned so the
    reading under it is `heading`. north_up: card fixed with N up, bowl and lubber line turned to `heading`.
    deflect: card pulled off magnetic north by this many degrees (clockwise)."""
    d = ImageDraw.Draw(im)
    for i in range(30, 0, -1):     # bowl: brushed-metal ring
        f = i / 30; v = int(70 + 120 * (1 - f) ** 0.7)
        r = R * (0.86 + 0.14 * f); d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=(v, v, v + 8))
    d.ellipse((c[0] - R, c[1] - R, c[0] + R, c[1] + R), outline=(40, 44, 52), width=4)
    rg = R * 0.86; d.ellipse((c[0] - rg, c[1] - rg, c[0] + rg, c[1] + rg), fill=DARK, outline=(30, 30, 34), width=3)
    rot = (0 if north_up else -heading) + deflect
    rc = R * 0.82
    for b in range(0, 360, 5):
        a = b + rot; L = rc * (0.13 if b % 10 == 0 else 0.07); w = 4 if b % 30 == 0 else 2
        d.line((polar_pt(c, rc, a), polar_pt(c, rc - L, a)), fill=(235, 235, 235), width=w)
    fn = F(max(18, int(R * 0.1)))
    for b in range(0, 360, 30):
        if b % 90 == 0: continue
        d.text(polar_pt(c, rc * 0.72, b + rot), str(b), font=fn, fill=(235, 235, 235), anchor='mm')
    fc = F(max(24, int(R * 0.17)))
    for b, s in ((0, 'N'), (90, 'E'), (180, 'S'), (270, 'W')):
        d.text(polar_pt(c, rc * 0.7, b + rot), s, font=fc, fill=RED if b == 0 else WHITE, anchor='mm')
    # card's north arrow (the needle sits under the card, aligned with it)
    tip = polar_pt(c, rc * 0.52, rot); tail = polar_pt(c, rc * 0.4, rot + 180)
    l = polar_pt(c, rc * 0.07, rot - 90); r_ = polar_pt(c, rc * 0.07, rot + 90)
    d.polygon([tip, l, c, r_], fill=RED); d.polygon([tail, l, c, r_], fill=(200, 200, 205))
    dot(d, c, max(6, R * 0.04), (60, 60, 66))
    la = heading if north_up else 0
    if lubber:
        d.line((polar_pt(c, R * 0.6, la), polar_pt(c, R * 0.98, la)), fill=ORANGE, width=max(5, int(R * 0.035)))
        d.polygon([polar_pt(c, R * 1.0, la), polar_pt(c, R * 0.9, la - 4), polar_pt(c, R * 0.9, la + 4)], fill=ORANGE)
    return d

def boat(im, c, L, ang, fill=(240, 240, 244), outline=(90, 100, 115), alpha=255):
    """Top view of a motor boat, bow toward screen bearing `ang` (clockwise from up)."""
    a = math.radians(ang)
    def T(x, y): return (c[0] + (x * math.cos(a) + y * math.sin(a)) * L, c[1] - (-x * math.sin(a) + y * math.cos(a)) * L)
    side = [(0.17 * math.sin(math.radians(t)) ** 0.6, 0.5 - 0.45 * (1 - math.cos(math.radians(t)))) for t in range(0, 91, 6)]
    hull = [T(x, y) for x, y in side] + [T(0.17, -0.5), T(-0.17, -0.5)] + [T(-x, y) for x, y in reversed(side)]
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.polygon(hull, fill=fill + (alpha,), outline=outline + (alpha,))
    od.line(hull + [hull[0]], fill=outline + (alpha,), width=4)
    od.rectangle((0, 0, 0, 0))
    cab = [T(-0.1, 0.05), T(0.1, 0.05), T(0.11, -0.2), T(-0.11, -0.2)]
    od.polygon(cab, fill=(170, 195, 220, alpha), outline=outline + (alpha,))
    b = im.convert('RGBA'); b.alpha_composite(ov); im.paste(b.convert('RGB'))
    return T

def lighthouse(d, p, s=1.0):
    d.polygon([(p[0] - 16 * s, p[1] + 34 * s), (p[0] + 16 * s, p[1] + 34 * s), (p[0] + 9 * s, p[1] - 26 * s), (p[0] - 9 * s, p[1] - 26 * s)], fill=WHITE, outline=(40, 40, 40))
    for k in (0, 1): yy = p[1] + (10 - 24 * k) * s; d.rectangle((p[0] - 13 * s + 3 * k * s, yy - 5 * s, p[0] + 13 * s - 3 * k * s, yy + 5 * s), fill=RED)
    d.ellipse((p[0] - 11 * s, p[1] - 42 * s, p[0] + 11 * s, p[1] - 22 * s), fill=(255, 220, 90))

def readout(d, box, title, value, col=GREEN_L):
    d.rounded_rectangle(box, 22, fill=(8, 14, 22), outline=(90, 110, 140), width=4)
    cx = (box[0] + box[2]) / 2
    label(d, (cx, box[1] + 44), title, F(38, False), MUTED)
    label(d, (cx, (box[1] + box[3]) / 2 + 24), value, F(62), col)

# ---------- cards ----------
def s01():
    im, d = base()
    sea(im, (0, 0, 1300, 1440)); boat(im, (650, 1180), 520, 315)
    compass(im, (650, 640), 470, heading=315)
    d = ImageDraw.Draw(im)
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 5', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'מצפן מגנטי', F(150), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['חלקי המצפן ואיך הוא עובד', 'קורס וכיוון', 'וריאציה ודויאציה', 'מצפן מול GPS']):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def _s02_side():
    im, d = base(); left_panel(d, 'המצפן הימי: חתך צד')
    x0, y0, x1, y1 = inner(); d.rectangle((x0, y0, x1, y1), fill=(20, 32, 50))
    cx = (x0 + x1) / 2; ty = y0 + 330            # bowl rim height
    GR, GR_D = (150, 156, 168), (95, 100, 112)
    def ell(c, rx, ry): return (c[0] - rx, c[1] - ry, c[0] + rx, c[1] + ry)
    def half(c, rx, ry, a0, a1, n=60): return [(c[0] + rx * math.cos(math.radians(a)), c[1] + ry * math.sin(math.radians(a))) for a in np.linspace(a0, a1, n)]
    # gimbal bracket and base
    d.line([(cx - 400, ty + 20), (cx - 400, y1 - 110), (cx + 400, y1 - 110), (cx + 400, ty + 20)], fill=GR_D, width=22, joint='curve')
    d.rounded_rectangle((cx - 460, y1 - 110, cx + 460, y1 - 70), 10, fill=GR_D)
    d.line(half((cx, ty + 20), 345, 80, 180, 360), fill=GR, width=14)          # gimbal ring, back half
    # bowl body with rounded bottom
    body = [(cx - 300, ty), (cx - 300, ty + 300)] + half((cx, ty + 300), 300, 140, 180, 0) + [(cx + 300, ty)]
    d.polygon(body, fill=(70, 76, 88), outline=(40, 44, 52))
    # liquid (translucent) inside
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    liq = [(cx - 280, ty - 10), (cx - 280, ty + 300)] + half((cx, ty + 300), 280, 125, 180, 0) + [(cx + 280, ty - 10)]
    od.polygon(liq, fill=(90, 170, 230, 110))
    od.pieslice(ell((cx, ty), 300, 210), 180, 360, fill=(170, 210, 240, 55), outline=(210, 230, 250, 200), width=4)  # glass dome
    b = im.convert('RGBA'); b.alpha_composite(ov); im.paste(b.convert('RGB')); d = ImageDraw.Draw(im)
    d.ellipse(ell((cx, ty), 300, 60), outline=(200, 205, 215), width=6)     # rim
    # pivot + jewel
    cy = ty + 60
    d.polygon([(cx - 40, ty + 400), (cx + 40, ty + 400), (cx, ty + 330)], fill=GR)
    d.line(((cx, ty + 335), (cx, cy + 75)), fill=(230, 230, 235), width=6)
    d.polygon([(cx - 14, cy + 60), (cx + 14, cy + 60), (cx, cy + 82)], fill=(200, 60, 90))
    # magnets under the card
    for k, yy in enumerate((cy + 95, cy + 135)):
        d.rectangle((cx - 170, yy, cx, yy + 22), fill=RED); d.rectangle((cx, yy, cx + 170, yy + 22), fill=(205, 205, 212))
    d.line(((cx, cy + 50), (cx, cy + 160)), fill=(60, 60, 66), width=8)
    # floating card: top face + front band with degrees
    d.ellipse(ell((cx, cy), 240, 46), fill=(30, 32, 38))
    band = half((cx, cy), 240, 46, 0, 180) + half((cx, cy + 50), 240, 46, 180, 0)
    d.polygon(band, fill=DARK, outline=(120, 120, 128))
    for deg in range(-60, 61, 5):
        a = math.radians(90 - deg * 1.3); x = cx + 240 * math.cos(a); yb = cy + 46 * math.sin(a)
        d.line(((x, yb + 2), (x, yb + (14 if deg % 10 else 22))), fill=WHITE, width=2)
    for deg, s in ((-30, '330'), (0, 'N'), (30, '030')):
        a = math.radians(90 - deg * 1.3); x = cx + 240 * math.cos(a); yb = cy + 46 * math.sin(a)
        d.text((x, yb + 34), s, font=F(28), fill=RED if s == 'N' else WHITE, anchor='mm')
    # lubber line on the front of the bowl wall, gimbal ring front half, pins
    d.line(((cx, cy + 4), (cx, cy + 50)), fill=ORANGE, width=6)
    d.line(half((cx, ty + 20), 345, 80, 0, 180), fill=GR, width=14)
    for sx in (-1, 1): dot(d, (cx + sx * 370, ty + 20), 18, GR, (60, 64, 72))
    # callouts
    def call(p, q, title, en, col, side):
        d.line((p, q), fill=col, width=3); dot(d, p, 8, col)
        dx = 14 if side == 'l' else -14
        label(d, (q[0] + dx, q[1] - 18), title, F(42), col, side); label(d, (q[0] + dx, q[1] + 26), en, F(30, False), MUTED, side)
    call((cx - 200, ty + 400), (x0 + 300, ty + 480), 'בית המצפן', 'Bowl · מלא בנוזל', BLUE_L, 'r')
    call((cx - 370, ty + 20), (x0 + 200, ty - 120), 'גימבלים', 'Gimbals', (200, 205, 215), 'r')
    call((cx - 200, cy + 10), (x0 + 330, y0 + 50), 'שושנת המצפן', 'Compass Card', GREEN_L, 'r')
    call((cx + 120, cy + 135), (x1 - 300, ty + 360), 'המגנטים', 'Magnets', CORAL, 'l')
    call((cx + 10, ty + 300), (x1 - 300, ty + 560), 'ציר המצפן', 'Pivot', (230, 230, 235), 'l')
    call((cx + 4, cy + 20), (x1 - 300, y0 + 50), 'קו הכיוון', "Lubber's Line", ORANGE, 'l')
    return im

def _s02_top():
    im, d = base(); left_panel(d, '')
    x0, y0, x1, y1 = inner(); d.rectangle((x0, y0, x1, y1), fill=(20, 32, 50))
    c = ((x0 + x1) / 2, (y0 + y1) / 2 + 30); R = 330
    d.ellipse((c[0] - R * 1.16, c[1] - R * 1.16, c[0] + R * 1.16, c[1] + R * 1.16), outline=(150, 156, 168), width=16)   # gimbal ring
    for sx in (-1, 1): dot(d, (c[0] + sx * R * 1.16, c[1]), 20, (150, 156, 168), (60, 64, 72))
    compass(im, c, R, heading=30)
    d = ImageDraw.Draw(im)
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)   # magnets seen through the card
    for off in (-34, 34):
        a = polar_pt(c, R * 0.55, -30); b_ = polar_pt(c, R * 0.55, 150)
        nx, ny = math.cos(math.radians(-30)) * off, math.sin(math.radians(-30)) * off
        od.line(((a[0] + nx, a[1] + ny), (b_[0] + nx, b_[1] + ny)), fill=(225, 60, 55, 120), width=16)
    b = im.convert('RGBA'); b.alpha_composite(ov); im.paste(b.convert('RGB')); d = ImageDraw.Draw(im)
    def call(p, q, title, en, col, side):
        d.line((p, q), fill=col, width=3); dot(d, p, 8, col)
        dx = 14 if side == 'l' else -14
        label(d, (q[0] + dx, q[1] - 18), title, F(42), col, side); label(d, (q[0] + dx, q[1] + 26), en, F(30, False), MUTED, side)
    call(polar_pt(c, R * 0.97, 0), (c[0] + 330, y0 + 50), 'קו הכיוון', "Lubber's Line", ORANGE, 'l')
    call(polar_pt(c, R * 0.93, 300), (x0 + 300, y0 + 50), 'בית המצפן', 'Bowl', BLUE_L, 'r')
    call((c[0] - R * 1.16, c[1]), (x0 + 200, c[1] - 160), 'גימבלים', 'Gimbals', (200, 205, 215), 'r')
    call(polar_pt(c, R * 0.6, 235), (x0 + 300, y1 - 60), 'שושנת המצפן', 'Compass Card', GREEN_L, 'r')
    call(polar_pt(c, R * 0.42, 150), (x1 - 330, y1 - 60), 'המגנטים', 'Magnets · מתחת לשושנה', CORAL, 'l')
    call(c, (x1 - 200, c[1] - 160), 'ציר המצפן', 'Pivot', (230, 230, 235), 'l')
    label(d, (c[0] - 120, y0 + 50), 'חרטום ↑', F(40), ORANGE, 'r')
    return im

def s02():
    ax0, ay0, ax1, ay1 = panel_area(); pw, ph = ax1 - ax0, ay1 - ay0
    sv = _s02_side().crop((ax0, ay0, ax1, ay1)); tv = _s02_top().crop((ax0, ay0, ax1, ay1))
    im, d = base()
    text_c(d, C.W / 2, 60, C.SUB, F(48, False), BLUE_L)
    text_c(d, C.W / 2, 130, 'חלקי המצפן הימי', F(110), TEXT)
    xr = C.W - 48 - pw; xl = 48; y = C.H - 24 - ph
    im.paste(sv, (xr, y)); im.paste(tv, (xl, y)); d = ImageDraw.Draw(im)
    for x, s in ((xr, 'חתך צד'), (xl, 'מבט על')):
        d.rounded_rectangle((x + pw / 2 - 150, y - 26, x + pw / 2 + 150, y + 40), 18, fill=PANEL)
        label(d, (x + pw / 2, y + 6), s, F(46), TEXT)
    save(im, 's02_parts')

def s03():
    im, d = base(); left_panel(d, 'צפון, קורס וכיוון לאתר')
    box = inner(); pt = chart(im, box, 0.0, 0.08, 0.75, 0.78)
    d = ImageDraw.Draw(im)
    bp = pt(0.15, 0.55); T = boat(im, bp, 150, 40); d = ImageDraw.Draw(im)
    arrow(d, bp, (bp[0], box[1] + 70), RED, 7, 36); label(d, (bp[0] - 14, box[1] + 60), '1 · צפון', F(42), RED, 'r')
    bow = T(0, 0.5); tipc = polar_pt(bp, 420, 40); arrow(d, bow, tipc, GREEN_L, 8, 38)
    label(d, (tipc[0] + 10, tipc[1] - 40), '2 · קורס', F(42), (20, 120, 60), 'l')
    nl = pt(*NLIGHT); dashed(d, bp, nl, ORANGE, 6); lighthouse(d, (nl[0], nl[1] - 30), 1.2)
    label(d, (nl[0] + 40, nl[1] + 50), '3 · כיוון למגדלור', F(42), (190, 110, 20), 'l')
    right_block(d, 'למה צריך מצפן', '1. למצוא את הצפון. 2. לדעת לאן אתה מפליג: הקורס. 3. למדוד כיוון לאתר ניווט, מגדלור, מבנה על החוף או מצוף, כדי למצוא את מיקומך על המפה הימית.')
    save(im, 's03_why')

def s04():
    im, d = base(); left_panel(d, 'קורס וכיוון נמדדים מהצפון')
    box = inner(); sea(im, box)
    x0, y0, x1, y1 = box; bp = ((x0 + x1) / 2 + 60, y1 - 330)
    T = boat(im, bp, 230, 60); d = ImageDraw.Draw(im)
    dashed(d, bp, (bp[0], y0 + 60), WHITE, 5); label(d, (bp[0], y0 + 40), 'צפון 000°', F(40), WHITE)
    kt = polar_pt(bp, 470, 60); dashed(d, bp, kt, GREEN_L, 5); arrow(d, polar_pt(bp, 400, 60), kt, GREEN_L, 6, 30)
    arc(d, bp, 190, 90, 30, GREEN_L, 7); label(d, polar_pt(bp, 260, 30), 'קורס 060°', F(46), GREEN_L)
    lp = polar_pt(bp, 520, 315); dashed(d, bp, lp, ORANGE, 6); lighthouse(d, (lp[0], lp[1] + 10), 1.3)
    arc(d, bp, 130, 90, 135, ORANGE, 7); label(d, polar_pt(bp, 230, 335), 'כיוון 315°', F(46), ORANGE)
    label(d, (lp[0], lp[1] + 90), 'מגדלור', F(38), WHITE)
    right_block(d, 'קורס מול כיוון', 'קורס: לאן החרטום מכוון. כיוון: ממך אל נקודה מסביבך.',
                ('שאלה מהמאגר · 14', 'מהו קורס מגנטי?',
                 ['הזווית שבין קו השדרית של הספינה והצפון המגנטי', 'הזווית שבין קו השדרית של הספינה וקו הרוחב עליו היא נמצאת',
                  'זווית שבין קו השדרית של הספינה והצפון הגיאוגרפי + סטייה עקב זרם', 'הזווית שבין קו השדרית של הספינה ובין הצפון של טבלת המצפן + סטייה עקב רוח'], 0))
    save(im, 's04_course_bearing')

def s05():
    im, d = base(); left_panel(d, 'מד זווית: צפון המצפן ← אתר')
    box = inner(); pt = chart(im, box, 0.3, 0.45, 1.0, 1.0)
    d = ImageDraw.Draw(im)
    bp = pt(0.88, 0.97); boat(im, bp, 120, 330); d = ImageDraw.Draw(im)
    sl = pt(*SELIGHT); dashed(d, bp, sl, ORANGE, 6); lighthouse(d, (sl[0], sl[1] - 30), 1.2)
    brg = round(math.degrees(math.atan2(sl[0] - bp[0], -(sl[1] - bp[1])))) % 360
    cc = (box[0] + 230, box[1] + 230); compass(im, cc, 200, heading=brg)
    d = ImageDraw.Draw(im)
    label(d, (cc[0], cc[1] + 240), f'כיוון {brg:03d}°', F(46), ORANGE)
    right_block(d, 'מצפן = מד זווית', 'המצפן מודד את הזווית מהצפון המגנטי אל גוף שאתה רואה באופק.',
                ('שאלה מהמאגר · 134', 'מצפן הוא מד-זווית המראה את הזווית שבין:',
                 ['צפון המצפן וגוף מסוים באופק', 'הצפון הגיאוגרפי ותו הכוון', 'כוכב הצפון וכוון חרטום כלי השיט',
                  'הצפון האמיתי (גיאוגרפי) לאחר תיקון שגיאות של השדה המגנטי של כדור הארץ'], 0))
    save(im, 's05_angle')

def s06():
    im, d = base(); left_panel(d, 'הלוח נשאר, קו הכיוון זז')
    x0, y0, x1, y1 = inner(); R = 225
    cr = (x1 - R - 60, y0 + 400); cl = (x0 + R + 60, y0 + 400)
    compass(im, cr, R, heading=0, north_up=True); compass(im, cl, R, heading=270, north_up=True)
    d = ImageDraw.Draw(im)
    label(d, (cr[0], y0 + 40), 'לפני', F(48), TEXT); label(d, (cl[0], y0 + 40), 'אחרי סיבוב 90° שמאלה', F(44), TEXT)
    pts = [(cr[0] - 60 + (cl[0] + 60 - (cr[0] - 60)) * t, y0 + 140 - 40 * math.sin(math.pi * t)) for t in np.linspace(0, 1, 40)]
    d.line(pts, fill=ORANGE, width=7); arrow(d, pts[-3], pts[-1], ORANGE, 7, 30)
    label(d, (cr[0], y0 + 400 + R + 60), 'קו הכיוון: צפון', F(44), ORANGE)
    label(d, (cl[0], y0 + 400 + R + 60), 'קו הכיוון: מערב', F(44), ORANGE)
    yy = y1 - 220
    for i, s in enumerate(['המחט מתיישרת עם השדה המגנטי של כדור הארץ', 'הסירה, הגוף וקו הכיוון מסתובבים סביב הלוח']):
        label(d, ((x0 + x1) / 2, yy + i * 70), s, F(40, False), TEXT)
    right_block(d, 'איך המצפן עובד', 'המחט תמיד מצביעה לצפון המגנטי. מה שזז הוא הסירה וקו הכיוון.',
                ('שאלה מהמאגר · 192', 'קו-הכיוון במצפן הימי נמצא מול הצפון. אם נסובב את המצפן שמאלה בזווית של 90°, לאיזה כיוון יצביע קו-הכיוון?',
                 ['מערבה', 'צפונה', 'מזרחה', 'דרומה'], 0))
    save(im, 's06_how')

def three_norths(d, o, L, var=12, dev=10):
    t, m, c = 0, var, var + dev
    for a, col, name, sub in ((t, WHITE, 'T.N', 'צפון אמיתי'), (m, BLUE_L, 'M.N', 'צפון מגנטי'), (c, CORAL, 'C.N', 'צפון מצפני')):
        p = polar_pt(o, L, a); arrow(d, o, p, col, 7, 34)
        label(d, (p[0], p[1] - 70), name, F(46), col); label(d, (p[0], p[1] - 24), sub, F(34, False), col)
    arc(d, o, L * 0.55, 90 - t, 90 - m, ORANGE, 8); arc(d, o, L * 0.42, 90 - m, 90 - c, GREEN_L, 8)
    return polar_pt(o, L * 0.55 + 30, (t + m) / 2), polar_pt(o, L * 0.42 + 30, (m + c) / 2)

def s07():
    im, d = base(); left_panel(d, 'שלושה צפונים, שתי שגיאות')
    x0, y0, x1, y1 = inner(); o = ((x0 + x1) / 2 - 120, y1 - 120)
    pv, pd = three_norths(d, o, 780, 14, 14)
    label(d, (pv[0] - 230, pv[1] + 40), 'וריאציה', F(50), ORANGE, 'r')
    dashed(d, (pv[0] - 220, pv[1] + 40), pv, ORANGE, 3)
    label(d, (pd[0] + 260, pd[1] + 120), 'דויאציה', F(50), GREEN_L, 'l')
    dashed(d, (pd[0] + 250, pd[1] + 120), pd, GREEN_L, 3)
    dot(d, o, 14, ORANGE, WHITE)
    label(d, ((x0 + x1) / 2, y1 - 40), 'הזוויות מוגדלות לצורך ההמחשה', F(34, False), MUTED)
    right_block(d, 'שגיאות המצפן', 'וריאציה: בין הצפון האמיתי לצפון המגנטי. דויאציה: בין הצפון המגנטי לצפון המצפני.')
    save(im, 's07_errors')

def rose(im, c, R, var=5):
    """Chart compass rose: outer true ring, inner magnetic ring turned by the variation."""
    d = ImageDraw.Draw(im)
    d.ellipse((c[0] - R, c[1] - R, c[0] + R, c[1] + R), fill=(250, 248, 240), outline=(120, 40, 120), width=3)
    for ring, rot, rr in ((0, 0, R), (1, var, R * 0.68)):
        for b in range(0, 360, 5):
            L = rr * (0.12 if b % 30 == 0 else 0.06); d.line((polar_pt(c, rr - 4, b + rot), polar_pt(c, rr - 4 - L, b + rot)), fill=(120, 40, 120), width=3 if b % 30 == 0 else 1)
        star = polar_pt(c, rr * 0.86, rot); d.polygon([polar_pt(c, rr * 0.98, rot), polar_pt(c, rr * 0.8, rot - 5), polar_pt(c, rr * 0.8, rot + 5)], fill=(120, 40, 120))
    d.line((polar_pt(c, R * 0.6, 0), polar_pt(c, R * 0.6, 180)), fill=(120, 40, 120), width=2)
    d.line((polar_pt(c, R * 0.55, var), polar_pt(c, R * 0.55, var + 180)), fill=(120, 40, 120), width=2)
    d.text(c, 'VAR 5°E', font=F(int(R * 0.14)), fill=(120, 40, 120), anchor='mm')

def s08():
    im, d = base(); left_panel(d, 'הקוטב המגנטי ≠ הקוטב הגיאוגרפי')
    x0, y0, x1, y1 = inner(); U4.night(im, (x0, y0, x1, y1), n=160)
    c = ((x0 + x1) / 2 + 120, y0 + 470); R = 380
    g = globe_at(im, c, R, 58, 40); d = ImageDraw.Draw(im); g.d = d
    g.grid(30, (110, 150, 200), 1)
    il = (32, 35); tn = (90, 0); mn = (85.8, 139.3)
    g.gc(il, (89.9, 35), WHITE, 6); g.gc(il, mn, BLUE_L, 6)
    pi, _ = g.pt(*il); ptn, _ = g.pt(*tn); pmn, _ = g.pt(*mn)
    dot(d, pi, 12, CORAL, WHITE); label(d, (pi[0] + 20, pi[1] + 34), 'ישראל', F(40), WHITE, 'l')
    dot(d, ptn, 12, WHITE); q = (ptn[0] - 70, y0 + 40); d.line((ptn, (q[0] + 10, q[1] + 20)), fill=WHITE, width=3); label(d, q, 'קוטב צפוני אמיתי', F(38), WHITE, 'r')
    dot(d, pmn, 12, BLUE_L); q = (pmn[0] + 70, y0 + 40); d.line((pmn, (q[0] - 10, q[1] + 20)), fill=BLUE_L, width=3); label(d, q, 'קוטב מגנטי', F(38), BLUE_L, 'l')
    rc = (x0 + 200, y1 - 190); rose(im, rc, 170)
    d = ImageDraw.Draw(im)
    label(d, (rc[0] + 230, rc[1] - 40), 'שושנת הרוחות במפה:', F(38), TEXT, 'l')
    label(d, (rc[0] + 230, rc[1] + 20), 'וריאציה באזור, כ-5° מזרח', F(38, False), TEXT, 'l')
    label(d, (rc[0] + 230, rc[1] + 80), 'משפיעה על כל מצפן מגנטי', F(38), ORANGE, 'l')
    right_block(d, 'וריאציה', 'ההפרש בין הצפון האמיתי לצפון המגנטי. מוצאים אותה במפה, והיא משפיעה על כל מצפן מגנטי.',
                ('שאלה מהמאגר · 24 · 155', 'על אלו מצפנים משפיעה הוריאציה באותה מידה?',
                 ['מצפן מגנטי ומצפן "שער שטף" (Flux Gate)', 'מצפן סביבוני (Gyroscopic) ומצפן אזימוט',
                  'מצפנים שלא בוצעה טבלת דוויאציה ביחס אליהם', 'מצפנים בכלי שיט שאינם בנויים ממתכת ולכן חשופים להשפעות הסביבה'], 0))
    save(im, 's08_variation')

def s09():
    im, d = base(); left_panel(d, 'הסירה עצמה מסיטה את המחט')
    box = inner(); sea(im, box); x0, y0, x1, y1 = box
    bc = ((x0 + x1) / 2, (y0 + y1) / 2 - 20); T = boat(im, bc, 820, 0); d = ImageDraw.Draw(im)
    cp = T(0, 0.2); compass(im, cp, 80, heading=0, deflect=14); d = ImageDraw.Draw(im)
    items = [(T(0, -0.42), 'מנוע', (90, 95, 105), (150, 70)), (T(-0.09, -0.12), 'מצברים', (60, 60, 64), (70, 50)),
             (T(0.09, 0.08), 'רמקול', (40, 40, 44), (44, 44)), (T(-0.08, 0.32), 'מסות מתכת', (120, 125, 135), (60, 40))]
    for p, s, col, (w, h) in items:
        d.rounded_rectangle((p[0] - w / 2, p[1] - h / 2, p[0] + w / 2, p[1] + h / 2), 10, fill=col, outline=WHITE, width=3)
        for k in (1, 2): r = (w / 2) + 26 * k; arc(d, p, r, 0, 360, (240, 200, 90) if k == 1 else (200, 160, 70), 2)
        side = 'l' if p[0] > bc[0] - 5 else 'r'
        label(d, (p[0] + (w / 2 + 70) * (1 if side == 'l' else -1), p[1]), s, F(40), WHITE, side)
    d.line((T(-0.06, -0.3), T(-0.06, 0.15), cp), fill=(230, 80, 60), width=5)
    label(d, (T(-0.2, 0.0)[0] - 30, T(-0.2, 0.0)[1]), 'כבלי חשמל', F(38), (240, 120, 100), 'r')
    label(d, ((x0 + x1) / 2, y1 - 30), 'הדויאציה משתנה לפי הקורס', F(42), ORANGE)
    right_block(d, 'דויאציה', 'ההפרש בין הצפון המגנטי לצפון המצפני. נוצרת ממתכת וחשמל בסירה.',
                ('שאלה מהמאגר · 8', 'מהי שגיאת הדוויאציה?',
                 ['שגיאה הנוצרת בעקבות ההפרש בין הצפון המגנטי לגיאוגרפי', 'שגיאה הנוצרת עקב מסות מתכת וחשמל בספינה',
                  'קיימת רק בספינות העשויות ממתכת', 'שגיאה הקיימת במצפן מגנטי, חשמלי וג\'יירו'], 1))
    save(im, 's09_deviation')

def speaker(d, c, s):
    d.rounded_rectangle((c[0] - 70 * s, c[1] - 110 * s, c[0] + 70 * s, c[1] + 110 * s), 16, fill=(30, 30, 34), outline=(150, 150, 160), width=4)
    for cy, r in ((c[1] - 50 * s, 32 * s), (c[1] + 35 * s, 52 * s)):
        d.ellipse((c[0] - r, cy - r, c[0] + r, cy + r), fill=(60, 60, 66), outline=(170, 170, 180), width=3)
        d.ellipse((c[0] - r * 0.35, cy - r * 0.35, c[0] + r * 0.35, cy + r * 0.35), fill=(110, 110, 118))

def s10():
    im, d = base(); left_panel(d, 'מגנט ליד המצפן = שגיאה')
    x0, y0, x1, y1 = inner(); d.rectangle((x0, y0, x1, y1), fill=(22, 30, 44))
    c = ((x0 + x1) / 2 - 140, (y0 + y1) / 2); R = 330
    compass(im, c, R, heading=0, north_up=True, deflect=28)
    d = ImageDraw.Draw(im)
    dashed(d, c, polar_pt(c, R * 1.25, 0), WHITE, 5); label(d, (c[0], c[1] - R * 1.25 - 30), 'צפון מגנטי', F(40), WHITE)
    a = polar_pt(c, R * 1.18, 28); arrow(d, c, a, RED, 6, 30); label(d, (a[0] + 20, a[1] - 20), 'המחט הוסטה', F(40), RED, 'l')
    sp = (x1 - 150, c[1] - 40); speaker(d, sp, 1.2)
    for k in (1, 2, 3): arc(d, (sp[0] - 60, sp[1]), 60 + 45 * k, 140, 220, (240, 200, 90), 3)
    label(d, (sp[0], sp[1] + 180), 'רמקול, אזניות, סוללות', F(36), TEXT)
    right_block(d, 'מכשירים עם מגנטים', 'רמקולים, אזניות, מיקרופון וסוללות מוציאים את המצפן המגנטי מאיזון.',
                ('שאלה מהמאגר · 5 · 154', 'כיצד ישפיעו מכשירים המכילים רמקולים, אזניות, מיקרופון וסוללות על מצפן הספינה?',
                 ['יוציאו את מצפן מגנטי מאיזון', 'ישפיעו על המצפן הסביבוני המכני (ג\'יירו) ויגרמו לו לחפש את הדרום במקום צפון',
                  'ישפרו את הדיוק של כל מצפן שתלוי במגנטיות', 'המכשירים עלולים להינזק בגלל עצמתם של המגנטים במצפן'], 0))
    save(im, 's10_speakers')

def s11():
    im, d = base(); left_panel(d, 'טבלת דויאציה: שתי דרכים')
    x0, y0, x1, y1 = inner(); cb = (x0, y0, x1, y0 + 620)
    pt = chart(im, cb, 0.0, 0.3, 0.8, 0.85)
    d = ImageDraw.Draw(im)
    a, b = pt(*SELIGHT), pt(*TOWER); dx, dy = b[0] - a[0], b[1] - a[1]
    bp = (a[0] + dx * 2.3, a[1] + dy * 2.3)
    d.line((a, bp), fill=ORANGE, width=6); boat(im, bp, 110, 105); d = ImageDraw.Draw(im)
    lighthouse(d, (a[0], a[1] - 30), 1.1); dot(d, b, 14, ORANGE, WHITE)
    label(d, (bp[0] + 10, bp[1] - 90), 'כיוון מעבר: שני אתרים על קו אחד', F(36), (150, 80, 10), 'l')
    ty = y0 + 660
    label(d, ((x0 + x1) / 2, ty), 'סיבוב 360° במקום קבוע, השוואה בכל קורס', F(40), TEXT)
    rows = [('000°', '2°E'), ('045°', '3°E'), ('090°', '1°E'), ('135°', '1°W'), ('180°', '3°W'), ('225°', '2°W')]
    cw = (x1 - x0 - 40) / 3
    for i, (cr, dv) in enumerate(rows):
        col, row = i % 3, i // 3
        bx = x1 - 20 - (col + 1) * cw; by = ty + 60 + row * 150
        d.rounded_rectangle((bx + 10, by, bx + cw - 10, by + 130), 18, fill=PANEL)
        label(d, (bx + cw / 2, by + 40), f'קורס {cr}', F(36, False), MUTED)
        label(d, (bx + cw / 2, by + 92), dv, F(46), GREEN_L)
    right_block(d, 'טבלת דויאציה', 'הדויאציה שונה בכל קורס. מסובבים את הסירה, או משתמשים בכיוון מעבר.',
                ('שאלה מהמאגר · 27', 'מה נדרש כדי להכין טבלת דוויאציה למצפנים מגנטיים?',
                 ['לזהות במדויק, במפה ובתצפית עם המצפן, שני אתרים על קו אחד', 'לסובב את כלי השיט 360° באתר קבוע, ולרשום את קורס המצפן ברווחים קבועים',
                  'לשוט הלוך וחזור במהירות קבועה בין שני מצופים, ולרשום כיוון לאתר קבוע כל 4 דקות', 'א ו-ב נכונות'], 3))
    save(im, 's11_table')

def s12():
    im, d = base(); left_panel(d, 'מפליגים לאחור, מזרחה')
    x0, y0, x1, y1 = inner(); sb = (x0, y0, x1, y0 + 560); sea(im, sb)
    bc = ((x0 + x1) / 2, y0 + 280); boat(im, bc, 380, 270); d = ImageDraw.Draw(im)
    arrow(d, (bc[0] + 220, bc[1] + 150), (x1 - 40, bc[1] + 150), GREEN_L, 10, 44)
    label(d, (bc[0] + 330, bc[1] + 210), 'תנועה: מזרח', F(42), GREEN_L)
    arrow(d, (bc[0] - 200, bc[1] - 150), (x0 + 60, bc[1] - 150), ORANGE, 8, 38)
    label(d, (bc[0] - 330, bc[1] - 210), 'חרטום: מערב', F(42), ORANGE)
    cy = y0 + 790; cc = (x1 - 270, cy); compass(im, cc, 200, heading=270); d = ImageDraw.Draw(im)
    label(d, (cc[0], cy + 240), 'המצפן: W', F(48), ORANGE)
    readout(d, (x0 + 60, cy - 180, x0 + 500, cy + 180), 'GPS · COG', '090° E')
    label(d, (x0 + 280, cy + 240), 'ה-GPS: E', F(48), GREEN_L)
    right_block(d, 'מצפן מול GPS', 'המצפן מראה לאן החרטום מכוון. ה-GPS מראה לאן אתה זז בפועל.',
                ('שאלה מהמאגר · 190', 'ספינתך מפליגה לאחור לכיוון מזרח. על איזה קורס יצביע המצפן המגנטי, ועל איזה קורס יצביע מכשיר ה-GPS?',
                 ['המצפן המגנטי E · מכשיר ה-GPS E', 'המצפן המגנטי E · מכשיר ה-GPS W', 'המצפן המגנטי W · מכשיר ה-GPS E', 'המצפן המגנטי W · מכשיר ה-GPS W'], 2))
    save(im, 's12_gps')

def s13():
    im, d = base(); left_panel(d, 'סיבוב במקום: 150° ← 120°')
    x0, y0, x1, y1 = inner(); sb = (x0, y0, x1, y0 + 560); sea(im, sb)
    bc = ((x0 + x1) / 2, y0 + 280)
    boat(im, bc, 400, 150, alpha=90); boat(im, bc, 400, 120); d = ImageDraw.Draw(im)
    arc(d, bc, 240, 90 - 150, 90 - 120, ORANGE, 8)
    p = polar_pt(bc, 240, 120); arrow(d, polar_pt(bc, 240, 128), p, ORANGE, 8, 34)
    label(d, (bc[0] + 250, bc[1] + 230), '30° שמאלה', F(42), ORANGE, 'l')
    label(d, (x0 + 40, y0 + 50), 'הסירה לא זזה ממקומה', F(40), WHITE, 'l')
    cy = y0 + 790; cc = (x1 - 270, cy); compass(im, cc, 200, heading=120); d = ImageDraw.Draw(im)
    label(d, (cc[0], cy + 240), 'המצפן: 120°', F(48), ORANGE)
    readout(d, (x0 + 60, cy - 180, x0 + 500, cy + 180), 'GPS · COG', '- - -', MUTED)
    label(d, (x0 + 280, cy + 240), 'ה-GPS: לא יגיב', F(48), GREEN_L)
    right_block(d, 'סיבוב במקום', 'המצפן מראה את החרטום החדש. ה-GPS לא מרגיש סיבוב, רק תנועה.',
                ('שאלה מהמאגר · 191', 'סובבו 30° שמאלה ספינה שעמדה כשחרטומה בכיוון 150°. על איזה קורס יצביע המצפן המגנטי, ועל איזה קורס יצביע מכשיר ה-GPS?',
                 ['המצפן המגנטי 120° · מכשיר ה-GPS 120°', 'המצפן המגנטי 120° · מכשיר ה-GPS לא יגיב',
                  'המצפן המגנטי 180° · מכשיר ה-GPS 120°', 'המצפן המגנטי 150° · מכשיר ה-GPS לא יגיב'], 1))
    save(im, 's13_rotate')

def s14():
    im, d = base()
    sea(im, (0, 0, 1300, 1440)); compass(im, (650, 720), 480, heading=60)
    d = ImageDraw.Draw(im)
    text_c(d, 1780, 180, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1710, 340, 1850, 352), 6, fill=GREEN)
    items = ['המחט מתיישרת עם השדה המגנטי', 'הלוח נשאר, קו הכיוון זז', 'קורס: לאן החרטום מכוון', 'כיוון: ממך אל האתר',
             'וריאציה: אמיתי ← מגנטי, מהמפה', 'דויאציה: מגנטי ← מצפני, מהסירה', 'טבלת דויאציה: סיבוב או כיוון מעבר', 'GPS = תנועה, מצפן = חרטום']
    for i, s in enumerate(items):
        y = 410 + i * 108
        d.rounded_rectangle((1340, y, 2400, y + 88), 20, fill=PANEL)
        dot(d, (2360, y + 44), 12, GREEN_L)
        text_r(d, 2320, y + 18, s, F(48, False), TEXT)
    save(im, 's14_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14]

def sheet():
    fs = [f.__name__ for f in ALL]; names = sorted(n for n in os.listdir(C.OUT) if n.endswith('.png') and not n.startswith('_'))
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
