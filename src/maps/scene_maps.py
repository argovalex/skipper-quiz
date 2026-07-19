"""Build labelled coast/orientation maps for the scenario questions that are not
firing-zone maps (tow-to-shore scenarios, gulf wind orientation).

Reuses the OSM basemap + drawing helpers in build_maps.py, but the composition is
different: named place markers, the boat's position, a wind arrow, and a highlight
ring on the correct answer location. Each SCENES entry writes media/<num>-<slug>.png,
which the bank references via mediaUrl (mediaType=image); scenes.js lets it win over
the SVG scene, so this PNG IS the video background.

Usage:  python src/maps/scene_maps.py [num ...]
"""

import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import build_maps as bm

ROOT = Path(__file__).resolve().parents[2]
MEDIA = ROOT / "media"

FB = bm.FONT_B
FR = bm.FONT_R
C_INK = (255, 255, 255)
C_GOOD = (46, 204, 113)
C_BOAT = (241, 196, 15)
C_WIND = (52, 152, 219)
C_BAD = bm.C_FORBID


def _f(size, bold=True):
    return ImageFont.truetype(FB if bold else FR, size)


def marker(img, to_px, lon, lat, text, kind="place", side="right", size=27):
    """A dot (or boat) with a haloed Hebrew label offset to one side."""
    d = ImageDraw.Draw(img, "RGBA")
    x, y = to_px(lon, lat)
    if kind == "boat":
        r = 13
        d.ellipse([x - r, y - r, x + r, y + r], fill=C_BOAT + (255,), outline=(20, 20, 20, 255), width=3)
        d.text((x, y), bm.he("⛵"), font=_f(16), fill=(20, 20, 20, 255), anchor="mm")
    elif kind in ("good", "bad"):
        ring = C_GOOD if kind == "good" else C_BAD
        r = 15
        d.ellipse([x - r - 6, y - r - 6, x + r + 6, y + r + 6], outline=ring + (255,), width=5)
        d.ellipse([x - r, y - r, x + r, y + r], fill=ring + (255,), outline=(255, 255, 255, 255), width=3)
    else:
        r = 8
        d.ellipse([x - r, y - r, x + r, y + r], fill=(20, 20, 20, 255), outline=(255, 255, 255, 255), width=3)
    # label
    color = (20, 90, 45) if kind == "good" else (140, 25, 20) if kind == "bad" else (20, 20, 20)
    dx = 18 if side == "right" else -18
    anchor = "lm" if side == "right" else "rm"
    d.text((x + dx, y), bm.he(text), font=_f(size), fill=color + (255,), anchor=anchor,
           stroke_width=max(4, size // 6), stroke_fill=(255, 255, 255, 235))


def wind_arrow(img, xy, bearing_deg, text, length=140):
    """A broad arrow pointing in the direction the wind blows TOWARD, with a label.

    bearing_deg is the compass bearing the wind blows toward (a north wind blows
    toward the south = 180)."""
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = xy
    th = math.radians(bearing_deg)
    dx, dy = math.sin(th), -math.cos(th)  # screen y is down
    tipx, tipy = cx + dx * length / 2, cy + dy * length / 2
    tailx, taily = cx - dx * length / 2, cy - dy * length / 2
    # shaft
    d.line([(tailx, taily), (tipx, tipy)], fill=C_WIND + (255,), width=13)
    # head
    px, py = -dy, dx
    hw, hl = 22, 34
    d.polygon([
        (tipx, tipy),
        (tipx - dx * hl + px * hw, tipy - dy * hl + py * hw),
        (tipx - dx * hl - px * hw, tipy - dy * hl - py * hw),
    ], fill=C_WIND + (255,))
    # label near the tail, haloed
    d.text((tailx, taily - 22), bm.he(text), font=_f(26), fill=C_WIND + (255,), anchor="mm",
           stroke_width=5, stroke_fill=(255, 255, 255, 240))


def title_bar(img, text):
    d = ImageDraw.Draw(img, "RGBA")
    f = _f(30)
    w = d.textlength(bm.he(text), font=f) + 36
    d.rounded_rectangle([16, 14, 16 + w, 60], radius=10, fill=bm.C_PANEL)
    d.text((16 + w - 18, 37), bm.he(text), font=f, fill=C_INK + (255,), anchor="rm")


# ── Scene specs ─────────────────────────────────────────────────────────────
# center=(lat,lon). markers: (lon,lat,text,kind,side). wind: (bearing_toward, text).
SCENES = {
    1146: {
        "slug": "tlv-tow",
        "center": (32.108, 34.775),
        "z": 13,
        "size": (1200, 1050),
        "title": "גרירה לחוף, רוח צפונית",
        "markers": [
            (34.7925, 32.1631, "מרינה הרצליה (מוצא)", "place", "right"),
            (34.770, 32.128, "מיקומכם (מול תל־ברוך)", "boat", "left"),
            (34.7745, 32.0994, "מעגן רידינג", "place", "left"),
            (34.7665, 32.0872, 'מעגן תל־אביב', "good", "left"),
            (34.7519, 32.0533, "נמל יפו", "place", "left"),
        ],
        "wind": (180, "רוח צפונית חזקה"),
        "wind_xy": (250, 300),
    },
    1145: {
        "slug": "carmel-tow",
        "center": (32.589, 34.900),
        "z": 13,
        "size": (1200, 1050),
        "title": "גרירה לחוף, רוח דרום מערבית",
        "markers": [
            (34.9195, 32.6320, "נק' המוצא, חוף הבונים", "good", "right"),
            (34.9045, 32.6130, "מיקומכם, מול נחשולים", "boat", "left"),
            (34.9186, 32.6155, "חוף נחשולים", "place", "right"),
            (34.9161, 32.6060, "חוף דור (טנטורה)", "place", "right"),
            (34.8987, 32.5405, "מעגן ג'יסר א-זרקא", "place", "right"),
        ],
        "wind": (45, "רוח דרום מערבית"),
        "wind_xy": (300, 540),
    },
    1093: {
        "slug": "eilat-south-wind",
        "center": (29.505, 34.968),
        "z": 13,
        "size": (1200, 1050),
        "title": "מפרץ אילת, רוח דרומית",
        "markers": [
            (34.9560, 29.5480, "החוף הצפוני, ים סוער", "good", "left"),
            (34.9494, 29.5364, "בסיס חיל הים", "place", "left"),
            (35.0000, 29.5300, "עקבה (ירדן)", "place", "right"),
        ],
        "wind": (0, "רוח דרומית חזקה"),
        "wind_xy": (470, 760),
    },
    1094: {
        "slug": "eilat-north-wind",
        "center": (29.505, 34.968),
        "z": 13,
        "size": (1200, 1050),
        "title": "מפרץ אילת, רוח צפונית",
        "markers": [
            (34.9560, 29.5480, "החוף הצפוני, ים שקט", "good", "left"),
            (34.9494, 29.5364, "בסיס חיל הים", "place", "left"),
            (35.0000, 29.5300, "עקבה (ירדן)", "place", "right"),
        ],
        "wind": (180, "רוח צפונית"),
        "wind_xy": (540, 560),
    },
    1095: {
        "slug": "eilat-east-wind",
        "center": (29.505, 34.968),
        "z": 13,
        "size": (1200, 1050),
        "title": "מפרץ אילת, רוח מזרחית",
        "markers": [
            (34.9494, 29.5364, "היסחפות לבסיס חיל הים", "bad", "left"),
            (34.9660, 29.5395, "אופנוע הים", "boat", "right"),
            (34.9560, 29.5480, "החוף הצפוני", "place", "left"),
            (35.0000, 29.5300, "עקבה (ירדן)", "place", "right"),
        ],
        "wind": (270, "רוח מזרחית"),
        "wind_xy": (700, 470),
    },
    # Kinneret. The land wind is the dangerous one: it blows off the shore you
    # launched from and pushes you out into the deep.
    1101: {
        "slug": "kinneret-east-shore",
        "center": (32.800, 35.585),
        "z": 12,
        "size": (1200, 1050),
        "title": "הכנרת, החוף המזרחי",
        "markers": [
            (35.6414, 32.7783, "עין גב", "bad", "left"),
            (35.5312, 32.7922, "טבריה", "place", "right"),
            (35.5800, 32.7080, "חוף צמח", "place", "right"),
            (35.5950, 32.8780, "צפון הכנרת", "place", "left"),
        ],
        "wind": (270, "רוח מזרחית, דוחפת לעומק"),
        "wind_xy": (640, 380),
    },
    1102: {
        "slug": "kinneret-west-shore",
        "center": (32.800, 35.585),
        "z": 12,
        "size": (1200, 1050),
        "title": "הכנרת, החוף המערבי",
        "markers": [
            (35.5312, 32.7922, "טבריה", "bad", "right"),
            (35.6414, 32.7783, "עין גב", "place", "left"),
            (35.5800, 32.7080, "חוף צמח", "place", "right"),
            (35.5950, 32.8780, "צפון הכנרת", "place", "left"),
        ],
        "wind": (90, "רוח מערבית, דוחפת לעומק"),
        "wind_xy": (560, 380),
    },
    1115: {
        "slug": "kinneret-drift-east",
        "center": (32.800, 35.585),
        "z": 12,
        "size": (1200, 1050),
        "title": "הכנרת, מנוע כבוי ברוח מערבית",
        "markers": [
            (35.6414, 32.7783, "עין גב", "good", "right"),
            (35.6340, 32.7960, "מיקומכם", "boat", "left"),
            (35.5312, 32.7922, "טבריה", "place", "right"),
            (35.5800, 32.7080, "חוף צמח", "place", "right"),
            (35.5950, 32.8780, "צפון הכנרת", "place", "left"),
        ],
        "wind": (90, "רוח מערבית"),
        "wind_xy": (500, 660),
    },
}


def build(num):
    spec = SCENES[num]
    img, to_px = bm.build_base(spec["center"], spec["z"], spec["size"])
    if spec.get("title"):
        title_bar(img, spec["title"])
    for lon, lat, text, kind, side in spec["markers"]:
        marker(img, to_px, lon, lat, text, kind, side)
    if spec.get("wind"):
        wind_arrow(img, spec["wind_xy"], spec["wind"][0], spec["wind"][1])
    w, h = spec["size"]
    bm.compass(img, (w - 70, h - 80), r=44)
    bm.attribution(img)
    out = MEDIA / f"{num}-{spec['slug']}.png"
    img.convert("RGB").save(out, "PNG")
    print("wrote", out)


if __name__ == "__main__":
    nums = [int(a) for a in sys.argv[1:]] or list(SCENES)
    for n in nums:
        build(n)
