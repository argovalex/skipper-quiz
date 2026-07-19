"""Build the OpenStreetMap-backed scene images used as video backgrounds.

Each entry in MAPS produces media/<num>-<slug>.png, which the bank references via
mediaUrl. scenes.js lets mediaUrl win over the generated SVG scene, so whatever
this script writes IS the video background.

Coastline geometry comes from Overpass; the allowed-corridor bands are true metric
offsets of that coastline (EPSG:3857 is not equal-distance at this latitude, so we
offset in a local azimuthal projection). Tiles are cached under .tilecache/ to keep
repeat runs off the OSM tile servers.

Usage:  python src/maps/build_maps.py [num ...]
"""

import io
import json
import math
import os
import sys
import time
from pathlib import Path

import requests
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont
from pyproj import Transformer
from shapely.geometry import LineString, MultiLineString, Polygon, box
from shapely.ops import linemerge, transform, unary_union

ROOT = Path(__file__).resolve().parents[2]
MEDIA = ROOT / "media"
CACHE = ROOT / ".tilecache"
UA = {"User-Agent": "SkipperQuiz/1.0 (+https://github.com/argovalex/skipper-quiz; argovalexander@gmail.com)"}

TILE = 256
NM = 1852.0  # metres in a nautical mile

FONT_B = "C:/Windows/Fonts/arialbd.ttf"
FONT_R = "C:/Windows/Fonts/arial.ttf"

# Palette matched to the existing 1073 asset and the video's dark chrome.
C_ALLOWED = (46, 204, 113)
C_FORBID = (231, 76, 60)
C_ZONE_FILL = (150, 60, 60, 90)
C_INK = (255, 255, 255)
C_PANEL = (16, 32, 56, 235)


# ── Projection helpers ──────────────────────────────────────────────────────
def local_proj(lat, lon):
    """Azimuthal equidistant about the map centre: metres are metres."""
    fwd = Transformer.from_crs(
        "EPSG:4326", f"+proj=aeqd +lat_0={lat} +lon_0={lon} +units=m +datum=WGS84", always_xy=True
    )
    inv = Transformer.from_crs(
        f"+proj=aeqd +lat_0={lat} +lon_0={lon} +units=m +datum=WGS84", "EPSG:4326", always_xy=True
    )
    return fwd.transform, inv.transform


def deg2px(lat, lon, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n * TILE
    y = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n * TILE
    return x, y


# ── Tiles ───────────────────────────────────────────────────────────────────
def fetch_tile(z, x, y):
    CACHE.mkdir(exist_ok=True)
    p = CACHE / f"{z}_{x}_{y}.png"
    if p.exists():
        return Image.open(p).convert("RGBA")
    url = f"https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    r = requests.get(url, headers=UA, timeout=30)
    r.raise_for_status()
    p.write_bytes(r.content)
    time.sleep(0.12)  # be polite to the tile server
    return Image.open(io.BytesIO(r.content)).convert("RGBA")


def build_base(center, z, size):
    """Composite tiles into an RGBA canvas centred on `center`, returns (img, to_px)."""
    w, h = size
    cx, cy = deg2px(center[0], center[1], z)
    x0, y0 = cx - w / 2, cy - h / 2

    canvas = Image.new("RGBA", (w, h), (170, 211, 223, 255))
    tx0, ty0 = int(x0 // TILE), int(y0 // TILE)
    tx1, ty1 = int((x0 + w) // TILE), int((y0 + h) // TILE)
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            try:
                t = fetch_tile(z, tx, ty)
            except Exception as e:
                print(f"   tile {z}/{tx}/{ty} failed: {e}")
                continue
            canvas.alpha_composite(t, (int(tx * TILE - x0), int(ty * TILE - y0)))

    def to_px(lon, lat):
        px, py = deg2px(lat, lon, z)
        return px - x0, py - y0

    return canvas, to_px


# ── Coastline ───────────────────────────────────────────────────────────────
OVERPASS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.osm.ch/api/interpreter",
]


def _overpass(query, tag):
    """Cached Overpass call. The public servers rate-limit and 504 under load, so
    every answer is kept on disk; a rebuild must never depend on them being up."""
    CACHE.mkdir(exist_ok=True)
    p = CACHE / f"op_{tag}.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf8"))
    last = None
    for host in OVERPASS:
        for attempt in range(2):
            try:
                r = requests.get(host, params={"data": query}, headers=UA, timeout=120)
                if r.status_code in (429, 504):
                    time.sleep(4 + attempt * 6)
                    last = f"{r.status_code} from {host}"
                    continue
                r.raise_for_status()
                d = r.json()
                # An overloaded mirror answers 200 with zero elements. Caching that
                # freezes the empty answer forever and every later run fails with a
                # bogus "no coastline here". Every query here has a real answer, so
                # empty means try elsewhere -- and never write it down.
                if not d.get("elements"):
                    last = f"empty result from {host} (remark: {d.get('remark')})"
                    time.sleep(4 + attempt * 6)
                    continue
                p.write_text(json.dumps(d), encoding="utf8")
                return d
            except Exception as e:
                last = f"{type(e).__name__} from {host}: {e}"
                time.sleep(3)
    raise RuntimeError(f"overpass failed for {tag}: {last}")


def coastline(bbox, tag):
    """bbox = (s, w, n, e). Returns the longest coastline LineString in lon/lat.

    Only the longest run is kept: offsetting a MultiLineString is not defined, and
    the short runs are marina jetties and breakwaters that would knot the offset.
    """
    q = f"[out:json][timeout:90];way[natural=coastline]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});out geom;"
    lines = [
        LineString([(p["lon"], p["lat"]) for p in e["geometry"]])
        for e in _overpass(q, tag).get("elements", [])
        if len(e.get("geometry", [])) > 1
    ]
    if not lines:
        raise RuntimeError(f"no coastline in {bbox}")
    merged = linemerge(unary_union(lines))
    parts = list(merged.geoms) if isinstance(merged, MultiLineString) else [merged]
    return max(parts, key=lambda g: g.length)


def water_ring(bbox, tag, name):
    """Outline of an inland water body (Kinneret, Dead Sea) as a lon/lat LineString."""
    q = (
        f'[out:json][timeout:90];relation["natural"="water"]["name"="{name}"]'
        f"({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});out geom;"
    )
    rings = []
    for e in _overpass(q, tag).get("elements", []):
        for m in e.get("members", []):
            if m.get("role") == "outer" and len(m.get("geometry", [])) > 1:
                rings.append(LineString([(p["lon"], p["lat"]) for p in m["geometry"]]))
    if not rings:
        raise RuntimeError(f"no water ring for {name}")
    merged = linemerge(unary_union(rings))
    parts = list(merged.geoms) if isinstance(merged, MultiLineString) else [merged]
    return max(parts, key=lambda g: g.length)


class Frame:
    """A local metric working frame: geometry in metres, plus the view rectangle.

    Bands are cut as polygons rather than offset as lines. Offsetting a 40 km
    coastline full of bays self-intersects and silently drops most of its length
    (1 nm came back empty, 300 m came back 18 km of a 41 km shore); buffering and
    clipping is exact and total.
    """

    def __init__(self, center, view_bbox, coast, sea_side):
        self.center = center
        self.sea_side = sea_side
        self.fwd, self.inv = local_proj(*center)
        self.coast = self._to_m(coast)
        s, w, n, e = view_bbox
        self.view = self._to_m(box(w, s, e, n))
        self.sea = self._sea_half()

    def _to_m(self, g):
        return transform(lambda x, y, z=None: self.fwd(x, y), g)

    def to_deg(self, g):
        return transform(lambda x, y, z=None: self.inv(x, y), g)

    def _sea_half(self):
        """The view rectangle minus the land, found by splitting on the coastline."""
        pieces = list(split_poly(self.view, self.coast))
        if len(pieces) < 2:
            return self.view.difference(self.coast.buffer(1))
        key = {
            "W": lambda g: -g.centroid.x, "E": lambda g: g.centroid.x,
            "S": lambda g: -g.centroid.y, "N": lambda g: g.centroid.y,
        }[self.sea_side]
        return max(pieces, key=key)

    def band(self, inner_m, outer_m):
        """Sea water between two distances from shore, as a polygon."""
        b = self.coast.buffer(outer_m)
        if inner_m:
            b = b.difference(self.coast.buffer(inner_m))
        return b.intersection(self.sea)

    def contour(self, metres):
        """The isodistance line at `metres` from shore, sea side only."""
        return self.coast.buffer(metres).boundary.intersection(self.sea.buffer(-1))


def split_poly(poly, line):
    """Split `poly` with `line`, tolerating lines that only partly cross it."""
    from shapely.ops import split as _split

    try:
        return list(_split(poly, line).geoms)
    except Exception:
        cut = poly.difference(line.buffer(0.5))
        return list(cut.geoms) if hasattr(cut, "geoms") else [cut]


# ── Drawing ─────────────────────────────────────────────────────────────────
def he(t):
    return get_display(t)


# ── Firing zones (official order, see firing_zones.json) ────────────────────
def dms(s):
    d, m, sec = s.split()
    return int(d) + int(m) / 60 + float(sec) / 3600


def firing_zones():
    """Zone rings from the closure order.

    The order tabulates each zone's corners but not in ring order (82 as listed
    self-intersects), so corners are sorted by bearing about their centroid. These
    are illustration backdrops for a teaching video, not a navigation chart; the
    reconstruction is accurate to the zone's position and extent, which is the
    entire teaching point.
    """
    spec = json.loads((Path(__file__).parent / "firing_zones.json").read_text(encoding="utf8"))
    out = []
    for z in spec["zones"]:
        pts = [(dms(lo), dms(la)) for lo, la in z["points"]]
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        pts.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
        out.append({**z, "ring": Polygon(pts)})
    return out


def draw_zone(img, zone, to_px, show_label=True):
    d = ImageDraw.Draw(img, "RGBA")
    pts = [to_px(x, y) for x, y in zone["ring"].exterior.coords]
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).polygon(pts, fill=C_ZONE_FILL)
    img.alpha_composite(ov)
    d.line(pts + [pts[0]], fill=C_FORBID + (255,), width=4, joint="curve")
    if show_label:
        c = zone["ring"].centroid
        label(img, to_px(c.x, c.y), f'שטח אש {zone["id"]}', 30, (150, 25, 25))


def draw_line(d, geom, to_px, color, width):
    geoms = geom.geoms if isinstance(geom, MultiLineString) else [geom]
    for g in geoms:
        pts = [to_px(x, y) for x, y in g.coords]
        if len(pts) > 1:
            d.line(pts, fill=color + (255,), width=width, joint="curve")


def compass(img, xy, r=42):
    """North-up rose with all four cardinals, per Alex: every map carries it."""
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = xy
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(10, 24, 44, 205), outline=(255, 255, 255, 230), width=2)
    d.polygon([(cx, cy - r + 8), (cx + 7, cy + 3), (cx, cy - 2), (cx - 7, cy + 3)], fill=(231, 76, 60, 255))
    d.polygon([(cx, cy + r - 8), (cx + 7, cy - 3), (cx, cy + 2), (cx - 7, cy - 3)], fill=(235, 235, 235, 255))
    f = ImageFont.truetype(FONT_B, 15)
    for label, (dx, dy) in {
        "צ": (0, -r - 13), "ד": (0, r + 13), "מז": (r + 15, 0), "מע": (-r - 15, 0),
    }.items():
        d.text((cx + dx, cy + dy), he(label), font=f, fill=(255, 255, 255, 255), anchor="mm",
               stroke_width=3, stroke_fill=(10, 24, 44, 255))


def legend(img, rows, xy=(18, 16)):
    d = ImageDraw.Draw(img, "RGBA")
    f = ImageFont.truetype(FONT_B, 19)
    pad, sw, lh = 12, 34, 30
    w = max(d.textlength(he(t), font=f) for _, t in rows) + sw + pad * 3
    h = lh * len(rows) + pad * 2
    x, y = xy
    d.rounded_rectangle([x, y, x + w, y + h], radius=9, fill=C_PANEL)
    for i, (kind, text) in enumerate(rows):
        ly = y + pad + i * lh + lh // 2
        sx = x + w - pad - sw
        if kind == "band":
            d.rectangle([sx, ly - 8, sx + sw, ly + 8], fill=C_ALLOWED + (200,))
        elif kind == "dash":
            for k in range(0, sw, 10):
                d.line([(sx + k, ly), (sx + min(k + 6, sw), ly)], fill=(255, 255, 255, 255), width=3)
        elif kind == "forbid":
            d.rectangle([sx, ly - 8, sx + sw, ly + 8], fill=C_ZONE_FILL)
            d.rectangle([sx, ly - 8, sx + sw, ly + 8], outline=C_FORBID + (255,), width=2)
        d.text((sx - pad, ly), he(text), font=f, fill=C_INK + (255,), anchor="rm")


def attribution(img):
    d = ImageDraw.Draw(img, "RGBA")
    f = ImageFont.truetype(FONT_R, 13)
    t = "© OpenStreetMap contributors"
    w = d.textlength(t, font=f)
    d.rectangle([img.width - w - 12, img.height - 22, img.width, img.height], fill=(255, 255, 255, 175))
    d.text((img.width - 6, img.height - 19), t, font=f, fill=(60, 60, 60, 255), anchor="ra")


def label(img, xy, text, size, color, anchor="mm"):
    d = ImageDraw.Draw(img, "RGBA")
    f = ImageFont.truetype(FONT_B, size)
    d.text(xy, he(text), font=f, fill=color + (255,), anchor=anchor,
           stroke_width=max(3, size // 8), stroke_fill=(255, 255, 255, 210))
