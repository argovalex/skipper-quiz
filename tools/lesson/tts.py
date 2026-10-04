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
    python tools/lesson/tts.py <vo.txt> <out_dir> --from-dir <v2_dir>
    python tools/lesson/tts.py <vo.txt> <out_dir> --elevenlabs     # קול v2, ברירת המחדל מ-2026-10-02

--from-dir (קול v2, docs/voice-style-v2.md): לא מפיק כלום. לוקח seg_<sid>.mp3 מוכנים
(Alex Skipper v2 מ-Higgsfield, אחרי tools/voice/master.py) מ-<v2_dir>, מוודא שיש קובץ
לכל סעיף ושהאורך סביר (master.py --check), ומעתיק ל-<out_dir>. סעיף חסר/חשוד = עצירה.
"""
import asyncio, os, re, shutil, sys, subprocess
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


def from_dir(vofile, out_dir, src_dir):
    master = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "voice", "master.py")
    os.makedirs(out_dir, exist_ok=True)
    segs = parse_segments(vofile)
    bad = []
    for sid, text in segs:
        src = os.path.join(src_dir, f"seg_{sid}.mp3")
        if not os.path.exists(src):
            print(f"  !! {sid} missing {src}")
            bad.append(sid)
            continue
        r = subprocess.run([sys.executable, master, "--check", src, str(len(_MARKS.sub("", text)))],
                           capture_output=True, text=True)
        print(r.stdout.strip())
        if r.returncode != 0:
            bad.append(sid)
            continue
        dst = os.path.join(out_dir, f"seg_{sid}.mp3")
        if os.path.abspath(src) != os.path.abspath(dst):
            shutil.copyfile(src, dst)
    if bad:
        raise SystemExit(f"ABORT: missing/failed v2 segments: {bad}")
    print("segments:", len(segs))


def elevenlabs(vofile, out_dir):
    """קול v2 (docs/voice-style-v2.md): ElevenLabs ישירות, ELEVENLABS_* מ-.env, מסטרינג master.py."""
    import json, urllib.request, urllib.error
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    env = dict(re.findall(r"^\s*(ELEVENLABS_\w+)\s*=\s*(.+?)\s*$",
                          open(os.path.join(root, ".env"), encoding="utf-8").read(), re.M))
    key, voice = env["ELEVENLABS_API_KEY"], env["ELEVENLABS_VOICE_ID"]
    sys.path.insert(0, os.path.join(root, "tools", "voice"))
    import master as mst
    lex = load_lexicon()
    os.makedirs(out_dir, exist_ok=True)
    segs = parse_segments(vofile)
    bad = []
    for sid, text in segs:
        text = niqqud_apply(text, lex)
        out = os.path.join(out_dir, f"seg_{sid}.mp3")
        if os.path.exists(out) and mst.check(out, len(_MARKS.sub("", text))):
            continue                                   # כבר הופק (המשך אחרי עצירה, חוסך מכסה)
        raw = out + ".raw.mp3"
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
            data=json.dumps({"text": text, "model_id": os.environ.get("ELEVENLABS_MODEL", "eleven_v4")}).encode(),
            headers={"xi-api-key": key, "Content-Type": "application/json"})
        for attempt in range(20):
            try:
                with urllib.request.urlopen(req, timeout=180) as r:
                    open(raw, "wb").write(r.read())
                break
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < 19:      # מגבלת בקשות מקבילות בתוכנית, מחכים ומנסים שוב
                    import time; time.sleep(15)
                    continue
                raise SystemExit(f"ABORT {sid}: ElevenLabs {e.code} {e.read()[:300]!r}")
        mst.master(raw, out)
        os.remove(raw)
        if not mst.check(out, len(_MARKS.sub("", text))):
            bad.append(sid)
    if bad:
        raise SystemExit(f"ABORT: suspicious length: {bad}")
    print("segments:", len(segs))


async def run(vofile, out_dir):
    import edge_tts
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
    a = sys.argv[1:]
    if "--elevenlabs" in a:
        a.remove("--elevenlabs")
        elevenlabs(os.path.abspath(a[0]), os.path.abspath(a[1]))
    elif "--from-dir" in a:
        i = a.index("--from-dir")
        src = a[i + 1] if i + 1 < len(a) else None
        a = a[:i] + a[i + 2:]
        if len(a) < 2 or not src:
            sys.exit("usage: python tools/lesson/tts.py <vo.txt> <out_dir> --from-dir <v2_dir>")
        from_dir(os.path.abspath(a[0]), os.path.abspath(a[1]), os.path.abspath(src))
    else:
        if len(a) < 2:
            sys.exit("usage: python tools/lesson/tts.py <vo.txt> <out_dir> [--from-dir <v2_dir>]")
        asyncio.run(run(os.path.abspath(a[0]), os.path.abspath(a[1])))
