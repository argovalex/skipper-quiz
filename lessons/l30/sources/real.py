"""Real-imagery helpers: NASA Blue Marble globe/Mercator, NOAA chart with graduated border and dividers."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

A = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
_BM = None
def bm():
    global _BM
    if _BM is None: _BM = np.asarray(Image.open(os.path.join(A, 'bluemarble.jpg')).convert('RGB'))
    return _BM

def globe_img(R, lat0, lon0, shade=True, sun=None, night=0.22):
    """Orthographic render of the Blue Marble texture, RGBA (2R x 2R)."""
    tex = bm(); H, W, _ = tex.shape
    y, x = np.mgrid[-R:R, -R:R].astype(np.float64) + 0.5
    xn, yn = x / R, -y / R
    rho = np.sqrt(xn ** 2 + yn ** 2); mask = rho <= 1
    c = np.arcsin(np.clip(rho, 0, 1)); la0 = math.radians(lat0)
    with np.errstate(invalid='ignore', divide='ignore'):
        lat = np.arcsin(np.cos(c) * math.sin(la0) + np.where(rho > 0, yn * np.sin(c) * math.cos(la0) / rho, 0))
        lon = math.radians(lon0) + np.arctan2(xn * np.sin(c), rho * np.cos(c) * math.cos(la0) - yn * np.sin(c) * math.sin(la0))
    u = ((np.degrees(lon) + 180) % 360) / 360 * (W - 1); v = (90 - np.degrees(lat)) / 180 * (H - 1)
    rgb = tex[np.clip(v, 0, H - 1).astype(int), np.clip(u, 0, W - 1).astype(int)].astype(np.float64)
    if sun is not None:
        sl, so = map(math.radians, sun)
        cz = np.sin(lat) * math.sin(sl) + np.cos(lat) * math.cos(sl) * np.cos(lon - so)
        light = night + 0.95 * np.clip((cz + 0.08) / 0.3, 0, 1) ** 0.8
        rgb = np.clip(rgb * light[..., None], 0, 255)
    elif shade:
        z = np.sqrt(np.clip(1 - rho ** 2, 0, 1))
        light = np.clip(0.35 + 0.75 * (z * 0.8 - xn * 0.25 + yn * 0.3), 0.25, 1.15)
        rgb = np.clip(rgb * light[..., None], 0, 255)
    alpha = (mask * 255).astype(np.uint8)
    im = Image.fromarray(np.dstack([rgb.astype(np.uint8), alpha]), 'RGBA')
    return im

def merc_y(lat): return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

def mercator_img(w, h, lon0, lon1, lat0, lat1):
    tex = bm(); H, W, _ = tex.shape
    y0, y1 = merc_y(lat0), merc_y(lat1)
    ys = y1 - (np.arange(h) + 0.5) / h * (y1 - y0)
    lats = np.degrees(2 * np.arctan(np.exp(ys)) - math.pi / 2)
    lons = lon0 + (np.arange(w) + 0.5) / w * (lon1 - lon0)
    v = ((90 - lats) / 180 * (H - 1)).astype(int); u = (((lons + 180) % 360) / 360 * (W - 1)).astype(int)
    return Image.fromarray(tex[v[:, None], u[None, :]], 'RGB')

class MercFrame:
    def __init__(s, box, lon0, lon1, lat0, lat1):
        s.box, s.lon0, s.lon1, s.y0, s.y1 = box, lon0, lon1, merc_y(lat0), merc_y(lat1)
    def pt(s, lat, lon):
        x0, y0, x1, y1 = s.box
        return (x0 + (lon - s.lon0) / (s.lon1 - s.lon0) * (x1 - x0), y1 - (merc_y(lat) - s.y0) / (s.y1 - s.y0) * (y1 - y0))

# ---------- NOAA chart ----------
CH_LAT0, CH_LAT1, CH_LON0, CH_LON1 = 41.13, 41.26, -71.66, -71.49   # bbox of chart_bi.png (EPSG:4326)

def chart_with_border(width, border=70):
    """Chart excerpt with a graduated latitude/longitude border like a paper chart. Returns (img, pt(lat,lon))."""
    ch = Image.open(os.path.join(A, 'chart_bi.png')).convert('RGB')
    inner = width - 2 * border
    ch = ch.resize((inner, inner), Image.LANCZOS)
    im = Image.new('RGB', (width, width), (250, 250, 246)); im.paste(ch, (border, border))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = border, border, border + inner, border + inner
    def pt(lat, lon):
        return (x0 + (lon - CH_LON0) / (CH_LON1 - CH_LON0) * inner, y1 - (lat - CH_LAT0) / (CH_LAT1 - CH_LAT0) * inner)
    d.rectangle((x0, y0, x1, y1), outline=(20, 20, 20), width=3)
    # latitude scale (both sides): 0.1' bars alternating, minute ticks
    bw = 22
    for side in (0, 1):
        xs = (x0 - bw, x0) if side == 0 else (x1, x1 + bw)
        d.rectangle((xs[0], y0, xs[1], y1), outline=(20, 20, 20), width=2)
        m = CH_LAT0 * 60
        k = math.ceil(m * 10)
        while k / 10 <= CH_LAT1 * 60:
            la = k / 600; a = pt(la, CH_LON0)[1]; b = pt(la + 1 / 600, CH_LON0)[1]
            if k % 2 == 0: d.rectangle((xs[0], b, xs[1], a), fill=(20, 20, 20))
            if k % 10 == 0:
                tx = (xs[0] - 34, xs[0]) if side == 0 else (xs[1], xs[1] + 34)
                d.line(((tx[0], a), (tx[1], a)), fill=(20, 20, 20), width=3)
                if side == 1:
                    from PIL import ImageFont
                    f = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 26)
                    d.text((xs[1] + 6, a - 30), "%d'" % (k // 10 - 41 * 60), font=f, fill=(20, 20, 20))
            k += 1
    for side in (0, 1):
        ys = (y0 - bw, y0) if side == 0 else (y1, y1 + bw)
        d.rectangle((x0, ys[0], x1, ys[1]), outline=(20, 20, 20), width=2)
        k = math.ceil(CH_LON0 * 600)
        while k / 600 <= CH_LON1:
            lo = k / 600; a = pt(CH_LAT0, lo)[0]; b = pt(CH_LAT0, lo + 1 / 600)[0]
            if k % 2 == 0: d.rectangle((a, ys[0], b, ys[1]), fill=(20, 20, 20))
            k += 1
    return im, pt

def draw_dividers(im, pA, pB, leg, side=1):
    """Draw steel dividers on RGBA/RGB image with needle points at pA and pB; hinge offset to one side."""
    mx, my = (pA[0] + pB[0]) / 2, (pA[1] + pB[1]) / 2
    dx, dy = pB[0] - pA[0], pB[1] - pA[1]; dist = math.hypot(dx, dy)
    h = math.sqrt(max(leg ** 2 - (dist / 2) ** 2, 1))
    nx, ny = -dy / dist * side, dx / dist * side
    hinge = (mx + nx * h, my + ny * h)
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(ov)
    for p in (pA, pB): sd.line(((hinge[0] + 12, hinge[1] + 16), (p[0] + 12, p[1] + 8)), fill=(0, 0, 0, 120), width=16)
    ov = ov.filter(ImageFilter.GaussianBlur(7))
    d = ImageDraw.Draw(ov)
    for p in (pA, pB):
        ux, uy = (p[0] - hinge[0]), (p[1] - hinge[1]); n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
        tip0 = (p[0] - ux * 34, p[1] - uy * 34)
        d.line((hinge, tip0), fill=(80, 85, 95, 255), width=18)
        d.line((hinge, tip0), fill=(195, 200, 210, 255), width=10)
        d.line(((hinge[0] - 3, hinge[1] - 3), (tip0[0] - 3, tip0[1] - 3)), fill=(250, 252, 255, 255), width=3)
        px, py = -uy * 6, ux * 6
        d.polygon([(tip0[0] + px, tip0[1] + py), (tip0[0] - px, tip0[1] - py), p], fill=(45, 47, 55, 255))
    d.ellipse((hinge[0] - 32, hinge[1] - 32, hinge[0] + 32, hinge[1] + 32), fill=(150, 155, 165, 255), outline=(70, 72, 80, 255), width=5)
    d.ellipse((hinge[0] - 11, hinge[1] - 11, hinge[0] + 11, hinge[1] + 11), fill=(225, 230, 236, 255))
    hx, hy = hinge[0] + nx * 80, hinge[1] + ny * 80
    d.line(((hinge[0] + nx * 30, hinge[1] + ny * 30), (hx, hy)), fill=(150, 125, 80, 255), width=22)
    base = im.convert('RGBA'); base.alpha_composite(ov)
    return base.convert(im.mode)

def dividers(size, spread_px, angle_deg=0):
    """Draw a steel pair of dividers on transparent RGBA. Points are spread_px apart, hinge above.
    Returns (img, (p1, p2)) with point coords inside img before rotation (no rotation used)."""
    L = size
    h = math.sqrt(max(L ** 2 - (spread_px / 2) ** 2, 1))
    W, H = int(spread_px + 160), int(h + 160)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    hinge = (W / 2, 80); p1 = (W / 2 - spread_px / 2, 80 + h); p2 = (W / 2 + spread_px / 2, 80 + h)
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    for p in (p1, p2): sd.line(((hinge[0] + 10, hinge[1] + 14), (p[0] + 10, p[1] + 6)), fill=(0, 0, 0, 110), width=14)
    sh = sh.filter(ImageFilter.GaussianBlur(6)); im.alpha_composite(sh)
    for p in (p1, p2):
        d.line((hinge, p), fill=(90, 95, 105, 255), width=16)
        d.line((hinge, p), fill=(200, 205, 215, 255), width=9)
        d.line(((hinge[0] - 2, hinge[1]), (p[0] - 2, p[1])), fill=(245, 248, 252, 255), width=3)
        d.polygon([(p[0] - 5, p[1] - 22), (p[0] + 5, p[1] - 22), p], fill=(60, 62, 70, 255))
    d.ellipse((hinge[0] - 30, hinge[1] - 30, hinge[0] + 30, hinge[1] + 30), fill=(150, 155, 165, 255), outline=(70, 72, 80, 255), width=5)
    d.ellipse((hinge[0] - 10, hinge[1] - 10, hinge[0] + 10, hinge[1] + 10), fill=(220, 225, 232, 255))
    d.rectangle((hinge[0] - 9, hinge[1] - 78, hinge[0] + 9, hinge[1] - 28), fill=(170, 150, 110, 255), outline=(90, 75, 50, 255), width=3)
    return im, p1, p2
