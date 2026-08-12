# -*- coding: utf-8 -*-
"""
tts.py — מפיק קריינות edge-tts לכל סעיף בקובץ VO של מערך שיעור.

קול he-IL-HilaNeural, rate -10%. מחיל את מילון הניקוד הקנוני (niqqud.py) על כל
סעיף, ובודק קיטוע: edge-tts קוטע לפעמים סגמנטים, אז מודדים משך מול רצפת CPS,
מפיקים מחדש עד 3 פעמים, ועוצרים אם עדיין קצר (עדיף כשל רועש על שיעור חסר).

קלט: קובץ VO עם כותרות סעיף '## <sid>' (מזהה מילה אחת: s1, s02_intro).
פלט: seg_<sid>.mp3 בתיקיית היעד, אחד לכל סעיף.

שימוש:
    python tools/lesson/tts.py <vo.txt> <out_dir>
"""
import asyncio, os, re, sys, subprocess
import edge_tts
from niqqud import load_lexicon, apply as niqqud_apply

VOICE = "he-IL-HilaNeural"
RATE = "-10%"
MIN_CPS = 22.0                       # תווי דיבור מינימליים לשנייה — מתחת לזה = קיטוע
_MARKS = re.compile("[֑-ׇ]")


def speech_len(t):
    return len(re.sub(r"\s+", "", _MARKS.sub("", t)))


def mp3_dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", p], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def parse_segments(vofile):
    segs = []
    cur = None
    for line in open(vofile, encoding="utf-8").read().splitlines():
        m = re.match(r"^##\s*(\S+)", line)
        if m:
            cur = m.group(1)
            segs.append([cur, ""])
        elif cur and line.strip():
            segs[-1][1] += (" " if segs[-1][1] else "") + line.strip()
    return segs


async def run(vofile, out_dir):
    lex = load_lexicon()
    os.makedirs(out_dir, exist_ok=True)
    segs = parse_segments(vofile)
    bad = []
    for sid, text in segs:
        text = niqqud_apply(text, lex)
        out = os.path.join(out_dir, f"seg_{sid}.mp3")
        floor = speech_len(text) / MIN_CPS
        dur = 0.0
        for attempt in range(1, 4):
            await edge_tts.Communicate(text, VOICE, rate=RATE).save(out)
            dur = mp3_dur(out)
            if dur >= floor:
                break
            print(f"  !! {sid} truncated: {dur:.1f}s < {floor:.1f}s -> retry {attempt}/3")
        ok = dur >= floor
        print(f"wrote {sid} chars {len(text)} dur {dur:.1f}s {'ok' if ok else 'SHORT'}")
        if not ok:
            bad.append(sid)
    if bad:
        raise SystemExit(f"ABORT: truncated after retries: {bad}")
    print("segments:", len(segs))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: python tools/lesson/tts.py <vo.txt> <out_dir>")
    asyncio.run(run(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])))
