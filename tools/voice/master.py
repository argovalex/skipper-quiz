# -*- coding: utf-8 -*-
"""
master.py — מסטרינג קבוע לקול Alex Skipper v2 (ראה docs/voice-style-v2.md).

אין pitch-shift ואין EQ: רק highpass + compressor + loudnorm.

שימוש:
    python tools/voice/master.py <in.mp3> <out.mp3>
    python tools/voice/master.py --pause <part1.mp3> <part2.mp3> <out.mp3>   # 2.5ש׳ שקט ביניהם
    python tools/voice/master.py --check <file.mp3> <text_chars>             # אימות אורך
"""
import subprocess, sys

CHAIN = ("highpass=f=70,"
         "acompressor=threshold=-20dB:ratio=2:attack=10:release=150,"
         "loudnorm=I=-14:TP=-1:LRA=9")
PAUSE_S = 2.5
CPS_MIN, CPS_MAX = 9.0, 22.0   # תווים לשנייה; מחוץ לטווח = קיטוע או שקט חשוד


def run(args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + args, check=True)


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", p], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def master(src, out):
    run(["-i", src, "-af", CHAIN, "-b:a", "192k", out])


def pause_concat(a, b, out):
    run(["-i", a, "-i", b, "-filter_complex",
         f"anullsrc=r=44100:cl=mono,atrim=duration={PAUSE_S}[s];"
         "[0:a]aresample=44100,aformat=channel_layouts=mono[a];"
         "[1:a]aresample=44100,aformat=channel_layouts=mono[b];"
         f"[a][s][b]concat=n=3:v=0:a=1,{CHAIN}",
         "-b:a", "192k", out])


def check(p, chars):
    d = dur(p)
    cps = chars / d if d else 0
    ok = d > 0 and CPS_MIN <= cps <= CPS_MAX
    print(f"{'OK' if ok else 'FAIL'} {p} dur={d:.1f}s cps={cps:.1f}")
    return ok


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--pause"] and len(a) == 4:
        pause_concat(a[1], a[2], a[3])
    elif a[:1] == ["--check"] and len(a) == 3:
        sys.exit(0 if check(a[1], int(a[2])) else 1)
    elif len(a) == 2:
        master(a[0], a[1])
    else:
        sys.exit(__doc__)
