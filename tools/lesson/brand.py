# -*- coding: utf-8 -*-
"""
מיתוג סרטון שיעור — כרטיס לוגו סטטי בפתיח/סיום + סימן מים לכל האורך.

זה הקוד הקבוע של המיתוג (הוצא מ-scratch_brand_u12.py, שהיה נמחק עם ה-scratchpad
וגרם לכל סשן להרכיב את המיתוג מחדש). המיתוג = הרצת הסקריפט הזה, לא פסקה לקרוא.

שימוש:
    python tools/lesson/brand.py <lesson.mp4> [branded.mp4] [--workdir DIR]

אם branded.mp4 לא ניתן, נשמר לצד הקלט בשם "<שם>_branded.mp4".
תלות: ffmpeg ב-PATH, Pillow, python-bidi, media/my_logo.jpg בריפו.
"""
import os, sys, subprocess, tempfile, argparse
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONT = "C:/Windows/Fonts/arial.ttf"
FONTB = "C:/Windows/Fonts/arialbd.ttf"
W, H = 1280, 720
VENC = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "25", "-preset", "medium"]
AENC = ["-c:a", "aac", "-ar", "44100", "-ac", "2", "-b:a", "192k"]


def f(s, b=False):
    return ImageFont.truetype(FONTB if b else FONT, s)


def P(*a):
    return os.path.join(*a)


def ctr(d, cx, y, text, font, fill):
    if any('\u0590' <= c <= '\u05ff' for c in text):
        text = get_display(text)
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)
    return w


def run(a):
    r = subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print("ERR", (r.stderr or "")[-800:])
        raise SystemExit(1)


def build(in_mp4, out_mp4, workdir):
    os.makedirs(workdir, exist_ok=True)

    logo = Image.open(P(REPO, "media", "my_logo.jpg")).convert("RGB")
    navy = logo.getpixel((6, 6))
    boat = logo.crop((40, 60, logo.width - 40, 770))

    def brand_card(path, tagline=None):
        img = Image.new("RGB", (W, H), navy)
        d = ImageDraw.Draw(img)
        bw = 560
        bh = int(boat.height * bw / boat.width)
        b = boat.resize((bw, bh), Image.LANCZOS)
        img.paste(b, ((W - bw) // 2, 70))
        y = 70 + bh - 20
        ctr(d, W / 2, y, "Alex Argov", f(66, True), (245, 248, 252)); y += 86
        ctr(d, W / 2, y, "Sailing Instructor", f(34), (150, 175, 205)); y += 52
        ctr(d, W / 2, y, "www.alargov.com", f(30, True), (90, 150, 220))
        if tagline:
            ctr(d, W / 2, 40, tagline, f(30), (150, 175, 205))
        img.save(path)

    brand_card(P(workdir, "intro.png"))
    brand_card(P(workdir, "outro.png"), tagline="תודה שצפיתם")

    # סימן מים — פינה שמאלית-עליונה
    wm = Image.new("RGBA", (430, 84), (0, 0, 0, 0))
    d = ImageDraw.Draw(wm)
    d.rounded_rectangle([0, 0, 430, 84], radius=42, fill=(12, 22, 40, 175))
    d.polygon([(60, 20), (60, 58), (96, 58)], fill=(240, 245, 250))
    d.line([(60, 14), (60, 58)], fill=(240, 245, 250), width=3)
    d.line([(40, 60), (104, 60)], fill=(240, 245, 250), width=4)
    d.text((150, 14), "Alex Argov", font=f(30, True), fill=(245, 248, 252))
    d.text((150, 50), "alargov.com", font=f(22), fill=(150, 175, 205))
    wm.save(P(workdir, "wm.png"))
    print("navy", navy, "| brand assets ready")

    wmmain = P(workdir, "main_wm.mp4")
    run(["ffmpeg", "-y", "-i", in_mp4, "-i", P(workdir, "wm.png"),
         "-filter_complex", "[0:v][1:v]overlay=28:24[v]",
         "-map", "[v]", "-map", "0:a", *VENC, *AENC, wmmain])

    def still(img, dur, out):
        run(["ffmpeg", "-y", "-loop", "1", "-r", "25", "-t", f"{dur}", "-i", img,
             "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", f"{dur}",
             "-vf", "scale=1280:720,setsar=1", *VENC, *AENC, "-shortest", out])

    still(P(workdir, "intro.png"), 3.0, P(workdir, "intro.mp4"))
    still(P(workdir, "outro.png"), 4.0, P(workdir, "outro.mp4"))

    segs = [P(workdir, "intro.mp4"), wmmain, P(workdir, "outro.mp4")]
    inp = []
    for s in segs:
        inp += ["-i", s]
    fc = "".join("[%d:v][%d:a]" % (i, i) for i in range(len(segs)))
    fc += "concat=n=%d:v=1:a=1[v][a]" % len(segs)
    run(["ffmpeg", "-y", *inp, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
         *VENC, *AENC, "-movflags", "+faststart", out_mp4])
    print("FINAL", out_mp4)


def main():
    ap = argparse.ArgumentParser(description="מיתוג סרטון שיעור (פתיח/סיום לוגו + סימן מים)")
    ap.add_argument("in_mp4", help="סרטון השיעור הגולמי")
    ap.add_argument("out_mp4", nargs="?", help="פלט ממותג (ברירת מחדל: <שם>_branded.mp4)")
    ap.add_argument("--workdir", help="תיקיית נכסי ביניים (ברירת מחדל: temp)")
    args = ap.parse_args()

    in_mp4 = os.path.abspath(args.in_mp4)
    if not os.path.isfile(in_mp4):
        sys.exit(f"לא נמצא קלט: {in_mp4}")
    if args.out_mp4:
        out_mp4 = os.path.abspath(args.out_mp4)
    else:
        base, ext = os.path.splitext(in_mp4)
        out_mp4 = base + "_branded" + (ext or ".mp4")
    workdir = args.workdir or tempfile.mkdtemp(prefix="lesson_brand_")

    build(in_mp4, out_mp4, workdir)


if __name__ == "__main__":
    main()
