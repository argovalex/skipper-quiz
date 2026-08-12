# -*- coding: utf-8 -*-
"""
assemble.py — מרכיב את סרטון השיעור הגולמי מכרטיסים + קריינות.

לכל סעיף בקובץ ה-VO ('## <sid>'): מגזם שקט בקצוות של seg_<sid>.mp3, מוסיף ריפוד
זנב קצר, יוצר קליפ סטילס מהכרטיס <sid>.png באורך הקריינות, ומשרשר הכל לפי סדר
הסעיפים. הסדר והמזהים נגזרים מאותו קובץ VO ששימש ל-tts.py — אין manifest נפרד.

הפלט גולמי (בלי מיתוג). המיתוג נעשה אחריו: tools/lesson/brand.py.

שימוש:
    python tools/lesson/assemble.py --vo <vo.txt> --audio <aud_dir> --cards <cards_dir> --out <lesson.mp4>
"""
import os, re, sys, argparse, subprocess

AAC = ["-c:a", "aac", "-ar", "44100", "-ac", "2", "-b:a", "192k"]
VENC = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "25", "-preset", "medium"]


def run(a):
    r = subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print("ERR", a[-1])
        print((r.stderr or "")[-800:])
        raise SystemExit(1)


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", p], capture_output=True, text=True)
    return float(r.stdout.strip())


def sids_from_vo(vofile):
    ids = []
    for line in open(vofile, encoding="utf-8").read().splitlines():
        m = re.match(r"^##\s*(\S+)", line)
        if m:
            ids.append(m.group(1))
    return ids


def trim(aud, out):
    run(["ffmpeg", "-y", "-i", aud, "-af",
         "silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.08,areverse,"
         "silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.12,areverse",
         "-c:a", "libmp3lame", out])


def pad(aud, out, sec=0.5):
    run(["ffmpeg", "-y", "-i", aud, "-af", f"apad=pad_dur={sec}", "-c:a", "libmp3lame", out])


def clip_card(out, img, aud):
    run(["ffmpeg", "-y", "-loop", "1", "-i", img, "-i", aud,
         "-vf", "scale=1280:720,setsar=1", "-c:v", "libx264", "-tune", "stillimage",
         "-pix_fmt", "yuv420p", "-r", "25", *AAC, "-shortest", out])


def main():
    ap = argparse.ArgumentParser(description="הרכבת סרטון שיעור גולמי מכרטיסים + קריינות")
    ap.add_argument("--vo", required=True, help="קובץ VO עם '## <sid>' (אותו אחד של tts.py)")
    ap.add_argument("--audio", required=True, help="תיקיית seg_<sid>.mp3")
    ap.add_argument("--cards", required=True, help="תיקיית <sid>.png")
    ap.add_argument("--out", required=True, help="פלט lesson.mp4 גולמי")
    ap.add_argument("--workdir", help="תיקיית ביניים (ברירת מחדל: <audio>/wrk)")
    a = ap.parse_args()

    vo, aud, cards = map(os.path.abspath, (a.vo, a.audio, a.cards))
    out = os.path.abspath(a.out)
    wrk = os.path.abspath(a.workdir) if a.workdir else os.path.join(aud, "wrk")
    os.makedirs(wrk, exist_ok=True)

    sids = sids_from_vo(vo)
    if not sids:
        sys.exit(f"לא נמצאו סעיפי '## <sid>' ב-{vo}")

    segfiles = []
    for idx, sid in enumerate(sids, 1):
        raw = os.path.join(aud, f"seg_{sid}.mp3")
        png = os.path.join(cards, f"{sid}.png")
        for pth, what in ((raw, "קריינות"), (png, "כרטיס")):
            if not os.path.isfile(pth):
                sys.exit(f"חסר {what} ל-{sid}: {pth}")
        t = os.path.join(wrk, f"{sid}_t.mp3"); trim(raw, t)
        p = os.path.join(wrk, f"{sid}_p.mp3"); pad(t, p, 0.5)
        o = os.path.join(wrk, f"{idx:02d}_{sid}.mp4")
        clip_card(o, png, p)
        segfiles.append(o)
        print("seg", sid)

    inp = []
    for s in segfiles:
        inp += ["-i", s]
    n = len(segfiles)
    fc = "".join("[%d:v][%d:a]" % (i, i) for i in range(n)) + "concat=n=%d:v=1:a=1[v][a]" % n
    run(["ffmpeg", "-y", *inp, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
         *VENC, *AAC, "-movflags", "+faststart", out])
    print("FINAL:", out, "|", round(dur(out), 1), "s")


if __name__ == "__main__":
    main()
