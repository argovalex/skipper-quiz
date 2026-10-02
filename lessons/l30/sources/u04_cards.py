"""Lesson 4 (l30): אופק, כוכבים וכוכב הצפון. Real imagery: NASA Blue Marble globes, star charts from real RA/Dec."""
import math, os, sys, random, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
spec = importlib.util.spec_from_file_location('u01', os.path.join(HERE, 'u01_cards.py')); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import real as RL
C.OUT = os.path.join(HERE, '..', 'cards', 'אופק כוכבים וכוכב הצפון'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · אופק וכוכבים'
F, text_c, text_r, label, dot, arrow, Globe = C.F, C.text_c, C.text_r, C.label, C.dot, C.arrow, C.Globe
base, left_panel, right_block, save, LP, RC = C.base, C.left_panel, C.right_block, C.save, C.LP, C.RC
TEXT, ORANGE, CORAL, GREEN, GREEN_L, BLUE_L, PANEL, MUTED = C.TEXT, C.ORANGE, C.CORAL, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL, C.MUTED
WHITE = (255, 255, 255); STAR = (255, 244, 210); RED = (230, 70, 70)

def panel_area(): return (LP[0], LP[1] + 300, LP[2], LP[3])

# ---------- real stars (RA hours, Dec deg, magnitude) ----------
UMI = [('Polaris', 2.53, 89.26, 2.0), ('d', 17.54, 86.59, 4.4), ('e', 16.77, 82.04, 4.2), ('z', 15.73, 77.79, 4.3),
       ('Kochab', 14.85, 74.16, 2.1), ('Pherkad', 15.35, 71.83, 3.0), ('h', 16.29, 75.76, 5.0)]
UMI_L = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 3)]
UMA = [('Dubhe', 11.06, 61.75, 1.8), ('Merak', 11.03, 56.38, 2.3), ('Phecda', 11.90, 53.69, 2.4), ('Megrez', 12.26, 57.03, 3.3),
       ('Alioth', 12.90, 55.96, 1.8), ('Mizar', 13.40, 54.93, 2.2), ('Alkaid', 13.79, 49.31, 1.9)]
UMA_L = [(0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6)]
CAS = [('Caph', 0.15, 59.15, 2.3), ('Schedar', 0.68, 56.54, 2.2), ('g', 0.95, 60.72, 2.2), ('Ruchbah', 1.43, 60.24, 2.7), ('Segin', 1.91, 63.67, 3.4)]
CAS_L = [(0, 1), (1, 2), (2, 3), (3, 4)]
ORI = [('Betelgeuse', 5.92, 7.41, 0.5), ('Bellatrix', 5.42, 6.35, 1.6), ('Mintaka', 5.53, -0.30, 2.2), ('Alnilam', 5.60, -1.20, 1.7),
       ('Alnitak', 5.68, -1.94, 1.7), ('Saiph', 5.80, -9.67, 2.1), ('Rigel', 5.24, -8.20, 0.1)]
ORI_L = [(0, 1), (0, 4), (1, 2), (2, 3), (3, 4), (4, 5), (2, 6), (5, 6)]

def polar(c, k, rot):
    """North-polar sky chart, as seen looking north: RA runs counter-clockwise around the pole."""
    def pt(ra, dec):
        r = (90 - dec) * k; a = math.radians(ra * 15 + rot)
        return (c[0] + r * math.cos(a), c[1] - r * math.sin(a))
    return pt

def local(c, k, ra0, dec0):
    def pt(ra, dec): return (c[0] - (ra - ra0) * 15 * math.cos(math.radians(dec0)) * k, c[1] - (dec - dec0) * k)
    return pt

def star(im, p, mag, col=STAR, scale=1.0):
    r = max(3, (5.2 - mag) * 5.5 * scale)
    g = Image.new('RGBA', im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse((p[0] - r * 3, p[1] - r * 3, p[0] + r * 3, p[1] + r * 3), fill=col + (70,))
    g = g.filter(ImageFilter.GaussianBlur(r * 1.2)); gd = ImageDraw.Draw(g)
    gd.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=col + (255,))
    b = im.convert('RGBA'); b.alpha_composite(g); im.paste(b.convert('RGB'))

def constellation(im, stars, lines, pt, col=(120, 160, 220), width=4, scale=1.0, starcol=STAR):
    d = ImageDraw.Draw(im); P = [pt(s[1], s[2]) for s in stars]
    for a, b in lines: d.line((P[a], P[b]), fill=col, width=width)
    for s, p in zip(stars, P): star(im, p, s[3], starcol, scale)
    return P

def night(im, box, seed=4, n=520, horizon=None):
    """Night-sky gradient with random faint stars, optional dark sea below `horizon` y."""
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    t = np.linspace(0, 1, h)[:, None, None]
    top, bot = np.array([6, 10, 24]), np.array([24, 40, 78])
    sky = (top + (bot - top) * t ** 1.4) * np.ones((1, w, 1))
    if horizon is not None:
        hy = horizon - y0
        sea = np.linspace(0, 1, max(h - hy, 1))[:, None, None]
        sky[hy:] = (np.array([18, 30, 52]) * (1 - sea) + np.array([6, 10, 20]) * sea) * np.ones((1, w, 1))
    im.paste(Image.fromarray(sky.astype(np.uint8), 'RGB'), (x0, y0))
    d = ImageDraw.Draw(im); rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, (horizon or y1) - 6)
        r = rnd.choice([1, 1, 1, 2, 2, 3]); v = rnd.randint(120, 235)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(v, v, min(255, v + 15)))
    if horizon is not None:
        d.line(((x0, horizon), (x1, horizon)), fill=(90, 120, 170), width=3)

def globe_at(im, c, R, lat0, lon0, sun=None, tilt=0, night=0.22):
    g = RL.globe_img(R, lat0, lon0, sun=sun, shade=sun is None, night=night)
    if tilt: g = g.rotate(tilt, resample=Image.BICUBIC, expand=False)
    im.paste(g, (int(c[0] - R), int(c[1] - R)), g)
    return Globe(ImageDraw.Draw(im), c[0], c[1], R, lat0=lat0, lon0=lon0, tilt=tilt)

def sun_glow(im, c, r):
    g = Image.new('RGBA', im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse((c[0] - r * 2.2, c[1] - r * 2.2, c[0] + r * 2.2, c[1] + r * 2.2), fill=(255, 190, 80, 90))
    g = g.filter(ImageFilter.GaussianBlur(r * 0.8)); gd = ImageDraw.Draw(g)
    gd.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=(255, 214, 110, 255))
    gd.ellipse((c[0] - r * 0.7, c[1] - r * 0.7, c[0] + r * 0.7, c[1] + r * 0.7), fill=(255, 240, 190, 255))
    b = im.convert('RGBA'); b.alpha_composite(g); im.paste(b.convert('RGB'))

def moon(im, c, r, lit_from=-1):
    y, x = np.mgrid[-r:r, -r:r].astype(np.float64) + 0.5
    rho = np.sqrt(x ** 2 + y ** 2) / r; m = rho <= 1
    rnd = np.random.default_rng(7)
    tex = 150 + rnd.normal(0, 10, (2 * r, 2 * r))
    for _ in range(26):
        cx, cy, cr = rnd.uniform(-r, r), rnd.uniform(-r, r), rnd.uniform(r * 0.05, r * 0.22)
        dd = np.sqrt((x - cx) ** 2 + (y - cy) ** 2); tex -= 38 * np.clip(1 - dd / cr, 0, 1) ** 0.5
    z = np.sqrt(np.clip(1 - rho ** 2, 0, 1)); light = np.clip(0.15 + 1.0 * (z * 0.5 + lit_from * -x / r * 0.6), 0.12, 1.1)
    v = np.clip(tex * light, 0, 255).astype(np.uint8)
    rgba = np.dstack([v, v, (v * 1.02).clip(0, 255).astype(np.uint8), (m * 255).astype(np.uint8)])
    g = Image.fromarray(rgba, 'RGBA'); im.paste(g, (int(c[0] - r), int(c[1] - r)), g)

def arc(d, c, r, a0, a1, col, width=6):
    """Arc between screen angles a0..a1 (degrees, 0=east, counter-clockwise)."""
    pts = [(c[0] + r * math.cos(math.radians(a)), c[1] - r * math.sin(math.radians(a))) for a in np.linspace(a0, a1, 60)]
    d.line(pts, fill=col, width=width)

def fill_box(im, box, col): ImageDraw.Draw(im).rectangle(box, fill=col)

def equirect(w, h, lon0, lon1, lat0, lat1, dim=1.0):
    tex = RL.bm(); H, W, _ = tex.shape
    lats = lat1 - (np.arange(h) + 0.5) / h * (lat1 - lat0); lons = lon0 + (np.arange(w) + 0.5) / w * (lon1 - lon0)
    v = ((90 - lats) / 180 * (H - 1)).astype(int); u = (((lons + 180) % 360) / 360 * (W - 1)).astype(int)
    return Image.fromarray(np.clip(tex[v[:, None], u[None, :]] * dim, 0, 255).astype(np.uint8), 'RGB')

class Eq:
    def __init__(s, box, lon0, lon1, lat0, lat1): s.box, s.lon0, s.lon1, s.lat0, s.lat1 = box, lon0, lon1, lat0, lat1
    def pt(s, lat, lon):
        x0, y0, x1, y1 = s.box
        return (x0 + (lon - s.lon0) / (s.lon1 - s.lon0) * (x1 - x0), y0 + (s.lat1 - lat) / (s.lat1 - s.lat0) * (y1 - y0))

def map_box(im, box, lon0, lon1, lat0, lat1):
    x0, y0, x1, y1 = box; im.paste(equirect(x1 - x0, y1 - y0, lon0, lon1, lat0, lat1), (x0, y0))
    ImageDraw.Draw(im).rectangle(box, outline=(230, 235, 245), width=4)
    return Eq(box, lon0, lon1, lat0, lat1)

def dashed(d, a, b, col, width=5, seg=22):
    L = math.hypot(b[0] - a[0], b[1] - a[1]); n = int(L // seg)
    for i in range(0, n, 2):
        t0, t1 = i / n, min((i + 1) / n, 1)
        d.line(((a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)), fill=col, width=width)

def latitude_diagram(im, lat, R=360):
    """Globe seen from the equator plane; observer on the right limb at `lat`; horizon, ray to Polaris, angle."""
    ax0, ay0, ax1, ay1 = panel_area(); c = ((ax0 + ax1) / 2 - 120, (ay0 + ay1) / 2 + 90)
    g = globe_at(im, c, R, 0, 25)
    d = ImageDraw.Draw(im)
    np_ = (c[0], c[1] - R); dashed(d, (c[0], c[1] + R + 40), (c[0], ay0 + 40), (200, 210, 230), 4)
    label(d, (c[0], ay0 + 30), 'ציר כדור הארץ', F(36, False), MUTED, dy=-4)
    a = math.radians(lat); o = (c[0] + R * math.cos(a), c[1] - R * math.sin(a))
    tn = (-math.sin(a), math.cos(a))  # tangent toward north
    L = 330
    if lat < 0:
        ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        far = 2000; n_out = (math.cos(a), -math.sin(a))
        poly = [(o[0] + tn[0] * far, o[1] - tn[1] * far), (o[0] - tn[0] * far, o[1] + tn[1] * far),
                (o[0] - tn[0] * far - n_out[0] * far, o[1] + tn[1] * far - n_out[1] * far),
                (o[0] + tn[0] * far - n_out[0] * far, o[1] - tn[1] * far - n_out[1] * far)]
        od.polygon(poly, fill=(0, 0, 0, 0))
    d.line(((o[0] - tn[0] * L, o[1] + tn[1] * L), (o[0] + tn[0] * L, o[1] - tn[1] * L)), fill=GREEN_L, width=7)
    hp = (o[0] + tn[0] * (L + 20), o[1] - tn[1] * (L + 20))
    label(d, hp, 'אופק', F(42), GREEN_L, 'l' if lat < 0 else 'r', dx=10 if lat < 0 else -10)
    top = (o[0], ay0 + 90)
    if lat >= 0:
        arrow(d, o, top, ORANGE, 7, 34); star(im, (top[0], top[1] - 30), 1.0)
        d = ImageDraw.Draw(im); label(d, (top[0] + 40, top[1] - 30), 'אל כוכב הצפון', F(40), ORANGE, 'l')
        a_h = math.degrees(math.atan2(tn[1], tn[0]))
        arc(d, o, 130, 90, a_h, ORANGE, 6)
        m = math.radians((90 + a_h) / 2); label(d, (o[0] + 185 * math.cos(m), o[1] - 185 * math.sin(m)), f'{lat}°', F(50), ORANGE)
    dot(d, o, 14, CORAL, WHITE)
    return g, o, c, top

# ---------- cards ----------
def s01():
    im, d = base()
    night(im, (0, 0, 1300, 1440), horizon=1150)
    pt = polar((650, 560), 9.5, -70)
    constellation(im, UMA, UMA_L, pt); constellation(im, CAS, CAS_L, pt); P = constellation(im, UMI, UMI_L, pt)
    d = ImageDraw.Draw(im); label(d, (P[0][0], P[0][1] - 60), 'כוכב הצפון', F(44), ORANGE)
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 4', F(56, False), BLUE_L)
    text_c(d, RC, 500, 'אופק, כוכבים', F(130), TEXT)
    text_c(d, RC, 650, 'וכוכב הצפון', F(130), TEXT)
    d.rounded_rectangle((RC - 80, 830, RC + 80, 844), 7, fill=GREEN)
    for i, s in enumerate(['זריחה, שקיעה וטווח האופק', 'עונות השנה והירח', 'כוכב הצפון וקו הרוחב', 'העגלה הקטנה']):
        text_c(d, RC, 900 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    im, d = base(); left_panel(d, 'כדור הארץ מסתובב ממערב למזרח')
    ax0, ay0, ax1, ay1 = panel_area(); c = ((ax0 + ax1) / 2, (ay0 + ay1) / 2 + 20); R = 430
    g = globe_at(im, c, R, 15, 20, sun=(5, 80))
    d = ImageDraw.Draw(im); g.d = d
    pts = [g.pt(-40, lo)[0] for lo in range(-30, 71, 3)]
    d.line(pts, fill=GREEN_L, width=10); arrow(d, pts[-3], pts[-1], GREEN_L, 10, 44)
    label(d, (pts[-1][0] + 16, pts[-1][1] + 16), 'מזרח', F(44), GREEN_L, 'l')
    label(d, (pts[0][0] - 16, pts[0][1] + 16), 'מערב', F(44), GREEN_L, 'r')
    p, _ = g.pt(28, -10); label(d, (p[0], p[1] - 10), 'זריחה', F(46), ORANGE)
    label(d, (c[0] + R - 20, ay0 + 40), 'השמש ←', F(42), ORANGE, 'r')
    right_block(d, 'זריחה במזרח', 'אנחנו מסתובבים עם כדור הארץ מזרחה, ולכן השמש נראית נעה מערבה.',
                ('שאלה מהמאגר · 2', 'מדוע רואים את השמש זורחת במזרח ושוקעת במערב?',
                 ['כדור הארץ נע במהירות מערבה סביב השמש', 'כדור הארץ סובב סביב צירו ממערב למזרח',
                  'ציר רוחבי של כדור הארץ מבצע תנועה מעגלית סביב כוכב הצפון', 'כדור הארץ סובב סביב צירו ממזרח למערב'], 1))
    save(im, 's02_rotation')

def s03():
    im, d = base(); left_panel(d, 'טווח האופק: צופה ומגדלור')
    ax0, ay0, ax1, ay1 = panel_area(); box = (ax0 + 20, ay0 + 20, ax1 - 20, ay1 - 20)
    night(im, box, n=120)
    Rb = 1100; cx = (box[0] + box[2]) / 2; top = box[1] + 520; cen = (cx, top + Rb)
    sea = equirect(box[2] - box[0], box[3] - box[1], -170, -120, -30, 10, 1.7)
    y, x = np.mgrid[box[1]:box[3], box[0]:box[2]]
    m = ((x - cen[0]) ** 2 + (y - cen[1]) ** 2 <= Rb ** 2).astype(np.uint8) * 255
    im.paste(sea, (box[0], box[1]), Image.fromarray(m, 'L'))
    d = ImageDraw.Draw(im)
    def on(a, h=0):
        a = math.radians(a); return (cen[0] + (Rb + h) * math.sin(a), cen[1] - (Rb + h) * math.cos(a))
    th_o, th_l = math.degrees(math.acos(Rb / (Rb + 90))), math.degrees(math.acos(Rb / (Rb + 75)))
    ao, al = -th_o, th_l
    # observer boat + mast
    b0 = on(ao); eye = on(ao, 90)
    d.polygon([(b0[0] - 50, b0[1] - 8), (b0[0] + 50, b0[1] - 18), (b0[0] + 38, b0[1] + 10), (b0[0] - 40, b0[1] + 16)], fill=(235, 235, 240))
    d.line((b0, eye), fill=(235, 235, 240), width=7); dot(d, eye, 12, CORAL, WHITE)
    # lighthouse
    l0 = on(al); lt = on(al, 75)
    d.polygon([(l0[0] - 22, l0[1]), (l0[0] + 22, l0[1] - 4), (lt[0] + 12, lt[1]), (lt[0] - 12, lt[1] + 2)], fill=(235, 235, 240))
    for k in (0.3, 0.6): q = (l0[0] + (lt[0] - l0[0]) * k, l0[1] + (lt[1] - l0[1]) * k); d.line(((q[0] - 18, q[1]), (q[0] + 18, q[1] - 3)), fill=RED, width=12)
    star(im, lt, 1.2, (255, 230, 150)); d = ImageDraw.Draw(im)
    tp = on(0)
    d.line((eye, tp), fill=ORANGE, width=6); d.line((tp, lt), fill=BLUE_L, width=6); dot(d, tp, 10, WHITE)
    label(d, ((eye[0] + tp[0]) / 2, (eye[1] + tp[1]) / 2 - 50), 'אופק הצופה', F(40), ORANGE)
    label(d, ((tp[0] + lt[0]) / 2, (tp[1] + lt[1]) / 2 - 50), 'אופק המגדלור', F(40), BLUE_L)
    label(d, (eye[0], eye[1] - 50), 'גובה עין', F(38, False), TEXT)
    y0 = box[1] + 60
    d.rounded_rectangle((cx - 400, y0, cx + 400, y0 + 130), 26, fill=PANEL, outline=ORANGE, width=4)
    d.text((cx - d.textlength('D = 2.1 × √h', font=F(60)) / 2, y0 + 30), 'D = 2.1 × √h', font=F(60), fill=ORANGE)
    label(d, (cx, y0 + 180), 'D = מרחק במיילים, h = גובה העין במטרים', F(40, False), TEXT)
    label(d, (cx, y0 + 240), 'רואים מגדלור: אופק הצופה + אופק המגדלור', F(40, False), TEXT)
    right_block(d, 'טווח האופק', 'שורש של גובה העין במטרים, כפול 2.1. גובה 9 מ\': √9 = 3, 3 × 2.1 = 6.3 מייל.',
                ('שאלה מהמאגר · 18', 'מהו מרחק האופק של צופה בגובה 9 מטרים?',
                 ['כ-9.6 מייל', 'כ-6.3 מייל', 'כ-3 מייל', 'כ-2.1 מייל'], 1))
    save(im, 's03_horizon')

def s04():
    im, d = base(); left_panel(d, 'הציר נטוי 23.5° כל השנה')
    ax0, ay0, ax1, ay1 = panel_area(); box = (ax0 + 20, ay0 + 20, ax1 - 20, ay1 - 20)
    night(im, box, n=160)
    # 3-D scene: orbit in the X-Z plane, camera raised `el` above it; Earth's axis fixed in space, tilted 23.5 deg toward +X
    el = math.radians(31); cam = np.array([0, math.sin(el), math.cos(el)]); up = np.array([0, math.cos(el), -math.sin(el)])
    t = math.radians(23.5); n = np.array([math.sin(t), math.cos(t), 0.0])
    cx, cy = (ax0 + ax1) / 2, ay0 + 500; A = 430
    def scr(P): return (cx + P[0], cy - P @ up)
    d = ImageDraw.Draw(im)
    orb = [scr(np.array([A * math.cos(a), 0, A * math.sin(a)])) for a in np.linspace(0, 2 * math.pi, 240)]
    d.line(orb + [orb[0]], fill=(120, 130, 150), width=5)
    for a0 in (20, 110, 200, 290):   # counter-clockwise seen from above the north side
        pts = [scr(np.array([A * math.cos(math.radians(a)), 0, A * math.sin(math.radians(a))])) for a in range(a0 + 30, a0 - 16, -3)]
        d.line(pts, fill=(170, 180, 200), width=9); arrow(d, pts[-3], pts[-1], (170, 180, 200), 9, 34)
    # (theta, month, season line, colour): theta=180 left, 0 right, 90 near (bottom), 270 far (top)
    spots = [(270, 'מרץ', 'יום ולילה שווים', TEXT), (180, 'יוני', 'קיץ בצפון', ORANGE), (0, 'דצמבר', 'חורף בצפון', BLUE_L), (90, 'ספטמבר', 'יום ולילה שווים', TEXT)]
    e1 = cam - (cam @ n) * n; e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
    lat_v = math.degrees(math.asin(n @ cam))
    ax_s = (n[0], n @ up); tilt = -math.degrees(math.atan2(ax_s[0], ax_s[1]))
    def draw_earth(th, month, season, col):
        P = np.array([A * math.cos(math.radians(th)), 0, A * math.sin(math.radians(th))])
        depth = (P @ cam) / A; R = int(125 * (1 + 0.22 * depth))
        s = -P / np.linalg.norm(P)
        sun = (math.degrees(math.asin(s @ n)), 20 + math.degrees(math.atan2(s @ e2, s @ e1)))
        c = scr(P); g = globe_at(im, c, R, lat_v, 20, sun=sun, tilt=tilt, night=0.08)
        dd = ImageDraw.Draw(im); g.d = dd
        g.parallel(0, (235, 70, 60), 4)
        npt, _ = g.pt(90, 0); spt, _ = g.pt(-90, 0)
        ux, uy = npt[0] - c[0], npt[1] - c[1]; L = math.hypot(ux, uy) or 1; ux, uy = ux / L, uy / L
        tipn = (c[0] + ux * (R + 75), c[1] + uy * (R + 75)); tips = (c[0] - ux * (R + 55), c[1] - uy * (R + 55))
        dd.line((npt, tipn), fill=(250, 220, 150), width=5); dd.line((spt, tips), fill=(250, 220, 150), width=5)
        rc = (c[0] + ux * (R + 40), c[1] + uy * (R + 40))
        rp = [(rc[0] + 40 * math.cos(math.radians(a)), rc[1] + 12 * math.sin(math.radians(a))) for a in range(520, 200, -8)]
        dd.line(rp, fill=(235, 70, 60), width=5); arrow(dd, rp[-2], rp[-1], (235, 70, 60), 5, 20)
        yl = c[1] + R + 50 if th != 270 else c[1] - R - 150
        label(dd, (c[0], yl), month, F(46), col); label(dd, (c[0], yl + 54), season, F(36, False), col if col != TEXT else MUTED)
    draw_earth(*spots[0])
    sun_glow(im, (cx, cy), 90); d = ImageDraw.Draw(im)
    label(d, (cx + 200, cy - 40), 'השמש', F(42), ORANGE)
    for sp in spots[1:]: draw_earth(*sp)
    d = ImageDraw.Draw(im)
    label(d, (cx, ay1 - 50), 'הציר נטוי תמיד לאותו כיוון בחלל', F(40, False), TEXT)
    right_block(d, 'עונות השנה', 'ביוני חצי הכדור הצפוני נוטה אל השמש, ובדצמבר חצי הכדור הדרומי.',
                ('שאלה מהמאגר · 152', 'כיצד נוצרות עונות השנה?',
                 ['השמש לא נמצאת במרכז המסלול של כדור הארץ', 'מישור הקו המשווה של כדור הארץ נטוי 23.5° ביחס למישור המסלול סביב השמש',
                  'מהירות כדור הארץ משתנה לפי המרחק שלו מהשמש', 'כל התשובות נכונות'], 1))
    save(im, 's04_seasons')

def s05():
    im, d = base(); left_panel(d, 'הירח מושך את המים: גאות ושפל')
    ax0, ay0, ax1, ay1 = panel_area(); box = (ax0 + 20, ay0 + 20, ax1 - 20, ay1 - 20)
    night(im, box, n=160)
    c = ((ax0 + ax1) / 2 - 80, (ay0 + ay1) / 2 + 20); R = 260
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse((c[0] - R - 110, c[1] - R - 25, c[0] + R + 110, c[1] + R + 25), fill=(90, 160, 240, 90), outline=(140, 200, 255, 200), width=4)
    b = im.convert('RGBA'); b.alpha_composite(ov); im.paste(b.convert('RGB'))
    globe_at(im, c, R, 30, 30, sun=(0, -60))
    mc = (ax1 - 130, c[1]); moon(im, mc, 75)
    sun_glow(im, (ax0 + 70, c[1]), 60)
    d = ImageDraw.Draw(im)
    arrow(d, (mc[0] - 95, mc[1]), (c[0] + R + 130, c[1]), (200, 210, 230), 5, 26)
    label(d, (mc[0], mc[1] + 120), 'הירח', F(44), TEXT); label(d, (ax0 + 70, c[1] + 110), 'השמש', F(40), ORANGE)
    label(d, (c[0] + R + 60, c[1] - R - 20), 'גאות', F(44), BLUE_L); label(d, (c[0], c[1] - R - 70), 'שפל', F(44), BLUE_L)
    label(d, ((ax0 + ax1) / 2, ay1 - 150), 'ירח מלא או חדש: גאות גבוהה', F(42), ORANGE)
    label(d, ((ax0 + ax1) / 2, ay1 - 90), 'ירח ברבע: גאות חלשה', F(40, False), TEXT)
    right_block(d, 'הירח', 'מקום הירח קובע את מחזור הגאות והשפל ואת גובהם.',
                ('שאלה מהמאגר · 153', 'על מה משפיע מקומו של הירח ביחס לכדור הארץ והשמש?',
                 ['המחזור והרמה של הגאות והשפל', 'הממוצע החודשי של גובה האוקיינוסים',
                  'הגאות והשפל ככל שמתרחקים צפונה ודרומה מהקו המשווה', 'א ו-ג נכונות'], 3))
    save(im, 's05_moon')

def s06():
    im, d = base(); left_panel(d, 'כוכב הצפון בהמשך ציר כדור הארץ')
    ax0, ay0, ax1, ay1 = panel_area(); box = (ax0 + 20, ay0 + 20, ax1 - 20, ay1 - 20)
    night(im, box, n=200)
    cx = (ax0 + ax1) / 2; pol = (cx, ay0 + 230)
    d = ImageDraw.Draw(im)
    for r_, a0 in ((55, 20), (95, 140), (135, 250), (175, 60)):
        arc(d, pol, r_, a0, a0 + 110, (110, 140, 190), 3)
    star(im, pol, 0.8)
    R = 330; c = (cx, ay1 - R - 60)
    g = globe_at(im, c, R, 22, 35)
    d = ImageDraw.Draw(im); g.d = d
    npt, _ = g.pt(90, 0); spt, _ = g.pt(-90, 0)
    dashed(d, npt, (pol[0], pol[1] + 40), ORANGE, 6)
    d.line((npt, (npt[0], npt[1] + 2)), fill=ORANGE, width=6); dot(d, npt, 10, ORANGE)
    label(d, (pol[0] + 60, pol[1]), 'כוכב הצפון', F(46), ORANGE, 'l')
    label(d, (npt[0] + 40, npt[1] - 60), 'הקוטב הצפוני', F(40), TEXT, 'l')
    label(d, (pol[0] - 60, (pol[1] + npt[1]) / 2), 'כיוון 000° = צפון אמיתי', F(42), GREEN_L, 'r')
    right_block(d, 'כוכב הצפון', 'נמצא מעל הקוטב הצפוני, בהמשך ציר הסיבוב. כמעט לא זז, ולכן מראה צפון אמיתי.',
                ('שאלה מהמאגר · 184', 'מהו מיקומו של כוכב הצפון ביחס לכדור הארץ?',
                 ['בהמשכו הדמיוני של קו המשווה של כדור הארץ', 'בהמשכו הדמיוני של הקו הצפוני של ציר הסיבוב של כדור הארץ',
                  'במחצית המרחק בין הקטבים של כדור הארץ', 'המיקום משתנה בהתאם לעונות השנה בכדור הארץ'], 1))
    save(im, 's06_polaris_axis')

def s07():
    im, d = base(); left_panel(d, 'גובה כוכב הצפון = קו הרוחב')
    ax0, ay0, ax1, ay1 = panel_area(); night(im, (ax0 + 20, ay0 + 20, ax1 - 20, ay1 - 20), n=120)
    latitude_diagram(im, 45)
    d = ImageDraw.Draw(im)
    rows = [('קוטב צפוני, 90°N', '90°'), ('ישראל, 32°N', '32°'), ('קו המשווה, 0°', '0°')]
    y = ay1 - 250
    for i, (a, b) in enumerate(rows):
        yy = y + i * 72; d.rounded_rectangle((ax1 - 520, yy, ax1 - 50, yy + 60), 16, fill=PANEL)
        text_r(d, ax1 - 70, yy + 10, a, F(36, False), TEXT); d.text((ax1 - 500, yy + 10), b, font=F(38), fill=ORANGE)
    right_block(d, 'קו הרוחב מהכוכב', 'הזווית של כוכב הצפון מעל האופק שווה לקו הרוחב של הצופה.',
                ('שאלה מהמאגר · 118', 'אם גובהו של כוכב הצפון 45° מעל האופק, הצופה נמצא בערך ב:',
                 ['קו רוחב 45° דרום', 'קו רוחב 45° מזרח', 'קו רוחב 45° צפון', 'קו רוחב 45° מערב'], 2))
    save(im, 's07_polaris_alt')

def s08():
    im, d = base(); left_panel(d, 'בין חיפה לקפריסין, 36°N')
    ax0, ay0, ax1, ay1 = panel_area()
    e = map_box(im, (ax0 + 30, ay0 + 20, ax1 - 30, ay0 + 560), 26, 40, 30, 39)
    d = ImageDraw.Draw(im)
    a, b = e.pt(36, 26), e.pt(36, 40); dashed(d, a, b, ORANGE, 5); label(d, (a[0] + 110, a[1] - 34), '36°N', F(40), ORANGE)
    hf, cy_ = e.pt(32.8, 35.0), e.pt(35.0, 33.4)
    d.line((hf, cy_), fill=GREEN_L, width=6); dot(d, hf, 11, CORAL, WHITE); dot(d, cy_, 11, CORAL, WHITE)
    label(d, hf, 'חיפה', F(38), WHITE, 'l', 20); label(d, cy_, 'קפריסין', F(38), WHITE, 'r', -20, -30)
    box = (ax0 + 30, ay0 + 600, ax1 - 30, ay1 - 30); hy = box[3] - 140
    night(im, box, n=140, horizon=hy)
    d = ImageDraw.Draw(im); o = (box[0] + 260, hy)
    a36 = math.radians(36); tip = (o[0] + 560 * math.cos(a36), o[1] - 560 * math.sin(a36))
    d.line((o, tip), fill=ORANGE, width=6); star(im, tip, 0.9); d = ImageDraw.Draw(im)
    arc(d, o, 170, 0, 36, ORANGE, 6); label(d, (o[0] + 240, o[1] - 70), '36°', F(52), ORANGE)
    label(d, (tip[0] + 30, tip[1]), 'כוכב הצפון', F(40), ORANGE, 'l')
    label(d, (box[2] - 150, hy + 60), 'אופק', F(38), GREEN_L)
    right_block(d, 'כוכב הצפון בים שלנו', 'בקו רוחב 36° צפון, כוכב הצפון נמצא 36° מעל האופק.',
                ('שאלה מהמאגר · 175', 'מה יהיה גובה כוכב הצפון לספינה בין חיפה לקפריסין, בקו רוחב של כ-36° צפון?',
                 ['כ-90° מעל האופק', 'כ-36° מעל האופק', 'כ-54° מעל האופק', 'אין חשיבות לקו הרוחב, כל עוד אני בחצי הכדור הצפוני'], 1))
    save(im, 's08_q175')

def s09():
    im, d = base(); left_panel(d, 'זווית קבועה = קו רוחב קבוע')
    ax0, ay0, ax1, ay1 = panel_area()
    e = map_box(im, (ax0 + 30, ay0 + 20, ax1 - 30, ay1 - 30), -6, 38, 28, 47)
    d = ImageDraw.Draw(im)
    a, b = e.pt(35, 2), e.pt(35, 30)
    d.line((a, b), fill=GREEN_L, width=9); arrow(d, a, b, GREEN_L, 9, 40); arrow(d, b, a, GREEN_L, 9, 40)
    label(d, ((a[0] + b[0]) / 2, a[1] - 50), 'מערב ↔ מזרח: הזווית לא משתנה', F(42), GREEN_L)
    p, q = e.pt(31, 20), e.pt(44, 20)
    d.line((p, q), fill=CORAL, width=9); arrow(d, p, q, CORAL, 9, 40)
    label(d, (q[0] + 30, q[1] + 40), 'צפון: הזווית גדלה', F(40), CORAL, 'l')
    for lat in (35, 40, 45):
        y = e.pt(lat, 0)[1]; d.text((e.box[0] + 12, y - 22), f'{lat}°N', font=F(34), fill=WHITE)
    right_block(d, 'אותה זווית כל ערב', 'קו הרוחב לא השתנה: שטים ממערב למזרח או ממזרח למערב.',
                ('שאלה מהמאגר · 3', 'מה מסיק כלי שיט שמודד בכל ערב את אותה זווית מעל האופק לכוכב הצפון?',
                 ['שהוא שט בחפיפה לקו רוחב קבוע', 'שהוא שט ממערב למזרח או ממזרח למערב',
                  'שהוא שט מדרום לצפון או מצפון לדרום', 'א ו-ב נכונות'], 3))
    save(im, 's09_same_angle')

def s10():
    im, d = base(); left_panel(d, 'מדרום לקו המשווה: לא רואים אותו')
    ax0, ay0, ax1, ay1 = panel_area(); night(im, (ax0 + 20, ay0 + 20, ax1 - 20, ay1 - 20), n=120)
    g, o, c, top = latitude_diagram(im, -30)
    d = ImageDraw.Draw(im)
    dashed(d, o, (o[0], ay0 + 120), RED, 6)
    label(d, (o[0] + 30, ay0 + 110), 'כוכב הצפון', F(40), RED, 'l')
    label(d, (o[0] + 30, ay0 + 170), 'מתחת לאופק', F(40), RED, 'l')
    label(d, (o[0] + 30, o[1] + 60), '30°S', F(42), CORAL, 'l')
    right_block(d, 'חצי הכדור הדרומי', 'כוכב הצפון מתחת לאופק. שם מנווטים לפי כוכבים אחרים, כמו הצלב הדרומי.',
                ('שאלה מהמאגר · 183', 'אתה מפליג מזרחה בקו רוחב 30°S. באיזה כיוון תוכל לראות את כוכב הצפון?',
                 ['000°', '90° לשמאל', '30° לימין', 'הכוכב לא נראה לעין'], 3))
    save(im, 's10_south')

def s11():
    im, d = base(); left_panel(d, 'מוצאים את כוכב הצפון')
    ax0, ay0, ax1, ay1 = panel_area(); box = (ax0 + 20, ay0 + 20, ax1 - 20, ay1 - 20)
    night(im, box, n=260)
    pt = polar(((ax0 + ax1) / 2 + 40, (ay0 + ay1) / 2 - 20), 11.5, -60)
    d = ImageDraw.Draw(im)
    PA = constellation(im, UMA, UMA_L, pt, (110, 150, 210)); PC = constellation(im, CAS, CAS_L, pt, (110, 150, 210))
    PU = constellation(im, UMI, UMI_L, pt, (120, 200, 140), 5)
    d = ImageDraw.Draw(im)
    dashed(d, PA[1], PU[0], ORANGE, 5)
    star(im, PU[0], 1.0, (255, 220, 140), 1.3); d = ImageDraw.Draw(im)
    label(d, (PU[0][0] + 30, PU[0][1] - 50), 'כוכב הצפון', F(44), ORANGE, 'l')
    label(d, (sum(p[0] for p in PA) / 7, max(p[1] for p in PA) + 60), 'העגלה הגדולה', F(42), BLUE_L)
    label(d, (sum(p[0] for p in PU) / 7 - 40, max(p[1] for p in PU) + 70), 'העגלה הקטנה', F(42), GREEN_L)
    label(d, (sum(p[0] for p in PC) / 5, min(p[1] for p in PC) - 50), 'קסיופאה', F(42), BLUE_L)
    mp = ((PA[1][0] + PU[0][0]) / 2, (PA[1][1] + PU[0][1]) / 2); label(d, (mp[0] - 30, mp[1] + 40), 'פי 5', F(40), ORANGE, 'r')
    right_block(d, 'העגלה הקטנה', 'כוכב הצפון בקצה היצול. מוצאים אותו מהמשך הדלי של העגלה הגדולה, בערך פי חמישה.',
                ('שאלה מהמאגר · 185', 'היכן ממוקם כוכב הצפון במערכת הכוכבים?',
                 ['במרכז שביל החלב', 'במרכז העגלה הקטנה', 'בתחתית קבוצת הכוכבים קסיופאה', 'בקצה היצול של העגלה הקטנה'], 3))
    save(im, 's11_little_dipper')

def s12():
    im, d = base(); left_panel(d, 'זיהוי קבוצות כוכבים')
    ax0, ay0, ax1, ay1 = panel_area()
    cw, ch = (ax1 - ax0 - 90) // 2, (ay1 - ay0 - 90) // 2
    cells = [(ax1 - 30 - cw, ay0 + 30), (ax0 + 30, ay0 + 30), (ax1 - 30 - cw, ay0 + 60 + ch), (ax0 + 30, ay0 + 60 + ch)]
    specs = [('א', 'קסיופאה', CAS, CAS_L, 'loc'), ('ב', 'העגלה הקטנה', UMI, UMI_L, 'pol'), ('ג', 'אוריון', ORI, ORI_L, 'loc'), ('ד', 'העגלה הגדולה', UMA, UMA_L, 'loc')]
    for (x, y), (let, name, st, ln, kind) in zip(cells, specs):
        box = (x, y, x + cw, y + ch); ok = let == 'ב'
        night(im, box, seed=ord(let), n=60)
        d = ImageDraw.Draw(im); d.rounded_rectangle(box, 20, outline=GREEN_L if ok else (80, 100, 140), width=6 if ok else 3)
        ras = [s[1] for s in st]; decs = [s[2] for s in st]
        if kind == 'pol':
            pt0 = polar((0, 0), 1, 110); P = [pt0(s[1], s[2]) for s in st]
        else:
            ra0 = (min(ras) + max(ras)) / 2; dec0 = (min(decs) + max(decs)) / 2; pt0 = local((0, 0), 1, ra0, dec0); P = [pt0(s[1], s[2]) for s in st]
        xs, ys = [p[0] for p in P], [p[1] for p in P]
        k = min((cw - 160) / max(max(xs) - min(xs), 1), (ch - 200) / max(max(ys) - min(ys), 1))
        mx, my = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        cc = (x + cw / 2, y + ch / 2 + 20)
        def ptf(ra, dec, pt0=pt0, k=k, mx=mx, my=my, cc=cc):
            p = pt0(ra, dec); return (cc[0] + (p[0] - mx) * k, cc[1] + (p[1] - my) * k)
        Pp = constellation(im, st, ln, ptf, GREEN_L if ok else (120, 160, 220), 4, 0.8)
        d = ImageDraw.Draw(im)
        text_r(d, x + cw - 24, y + 16, let + ':', F(56), GREEN_L if ok else TEXT)
        if ok: label(d, (Pp[0][0], Pp[0][1] - 45), 'כוכב הצפון', F(34), ORANGE)
        label(d, (x + cw / 2, y + ch - 36), name, F(38, False), GREEN_L if ok else MUTED)
    right_block(d, 'שאלת ציורים', 'העגלה הקטנה: דלי של ארבעה כוכבים ויצול של שלושה, וכוכב הצפון בקצה היצול.',
                ('שאלה מהמאגר · 102', 'באיזו מהקבוצות הבאות מופיע כוכב הצפון?',
                 ['ציור א: קסיופאה', 'ציור ב: העגלה הקטנה', 'ציור ג: אוריון', 'ציור ד: העגלה הגדולה'], 1))
    save(im, 's12_q102')

def s13():
    im, d = base(); left_panel(d, 'כוכבים הם שמשות רחוקות')
    ax0, ay0, ax1, ay1 = panel_area(); box = (ax0 + 20, ay0 + 20, ax1 - 20, ay1 - 20)
    night(im, box, n=300)
    d = ImageDraw.Draw(im)
    big = (ax1 + 260, (ay0 + ay1) / 2 - 120); Rg = 620
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse((big[0] - Rg, big[1] - Rg, big[0] + Rg, big[1] + Rg), fill=(230, 110, 60, 255))
    od.ellipse((big[0] - Rg * 0.8, big[1] - Rg * 0.8, big[0] + Rg * 0.8, big[1] + Rg * 0.8), fill=(245, 140, 80, 255))
    mask = Image.new('L', im.size, 0); ImageDraw.Draw(mask).rectangle(box, fill=255)
    ov.putalpha(Image.fromarray(np.minimum(np.asarray(ov.split()[3]), np.asarray(mask))))
    b = im.convert('RGBA'); b.alpha_composite(ov); im.paste(b.convert('RGB'))
    sun_glow(im, (ax0 + 200, (ay0 + ay1) / 2 - 120), 22)
    d = ImageDraw.Draw(im)
    label(d, (ax0 + 200, (ay0 + ay1) / 2 - 50), 'השמש', F(40), ORANGE)
    label(d, (ax1 - 220, (ay0 + ay1) / 2 - 120), 'כוכב ענק', F(44), WHITE)
    y = ay1 - 230
    dashed(d, (ax0 + 120, y), (ax1 - 200, y), (180, 190, 210), 4)
    star(im, (ax0 + 100, y), 3.5); d = ImageDraw.Draw(im)
    label(d, ((ax0 + ax1) / 2, y - 50), 'מרחק עצום', F(42), TEXT)
    label(d, (ax0 + 110, y + 60), 'כך נראה מכאן', F(36, False), MUTED, 'l')
    right_block(d, 'למה הם נראים קטנים', 'רבים מהכוכבים גדולים מהשמש. הם נראים כנקודות בגלל המרחק.',
                ('שאלה מהמאגר · 186', 'מדוע הכוכבים נראים קטנים?',
                 ['כי הם רחוקים מאיתנו', 'כי הם אכן קטנים', 'כי אנו רואים רק את החלק השטוח שלהם', 'בגלל העיוות האופטי שיוצרת האטמוספרה'], 0))
    save(im, 's13_stars_far')

def s14():
    im, d = base()
    night(im, (0, 0, 1300, 1440), horizon=1150)
    pt = polar((650, 560), 9.5, -70)
    constellation(im, UMA, UMA_L, pt); constellation(im, CAS, CAS_L, pt); P = constellation(im, UMI, UMI_L, pt)
    d = ImageDraw.Draw(im); label(d, (P[0][0], P[0][1] - 60), 'כוכב הצפון', F(44), ORANGE)
    text_c(d, 1780, 180, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1710, 340, 1850, 352), 6, fill=GREEN)
    items = ['סיבוב ממערב למזרח: זריחה במזרח', 'אופק (מייל) = 2.1 × √ גובה (מ\')', 'עונות: ציר נטוי 23.5°', 'הירח: גאות ושפל',
             'כוכב הצפון: המשך הציר, 000°', 'גובה כוכב הצפון = קו הרוחב', 'מדרום לקו המשווה: לא נראה', 'קצה היצול של העגלה הקטנה']
    for i, s in enumerate(items):
        y = 410 + i * 108
        d.rounded_rectangle((1340, y, 2400, y + 88), 20, fill=PANEL)
        dot(d, (2360, y + 44), 12, GREEN_L)
        text_r(d, 2320, y + 18, s, F(48, False), TEXT)
    save(im, 's14_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14]
if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only: fn()
