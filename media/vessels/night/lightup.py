"""Overlay navigation lights (glowing dots) on an unlit night vessel image.
usage: python lightup.py <in.png> <out.png> "<x,y,color[,r]>;..."   colors: w r g y
"""
import sys
from PIL import Image, ImageDraw, ImageFilter

COL = {"w": (255, 255, 240), "r": (255, 40, 30), "g": (40, 255, 90), "y": (255, 210, 40)}

def lightup(src, dst, spec):
    base = Image.open(src).convert("RGB")
    glow = Image.new("RGB", base.size, (0, 0, 0))
    core = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gd, cd = ImageDraw.Draw(glow), ImageDraw.Draw(core)
    for item in spec.split(";"):
        p = item.split(","); x, y, c = int(p[0]), int(p[1]), p[2]; r = int(p[3]) if len(p) > 3 else 9
        col = COL[c]
        gd.ellipse((x - r * 4, y - r * 4, x + r * 4, y + r * 4), fill=tuple(v // 2 for v in col))
        cd.ellipse((x - r, y - r, x + r, y + r), fill=col + (255,))
        cd.ellipse((x - r // 2, y - r // 2, x + r // 2, y + r // 2), fill=(255, 255, 255, 230))
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    from PIL import ImageChops
    out = ImageChops.screen(base, glow)
    out.paste(core, (0, 0), core)
    out.save(dst)

if __name__ == "__main__":
    lightup(sys.argv[1], sys.argv[2], sys.argv[3])
