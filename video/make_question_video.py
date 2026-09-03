# -*- coding: utf-8 -*-
"""
make_question_video.py — fully-free vertical (9:16) explainer video for a quiz
question. No paid cloud: edge-tts for narration, the CANONICAL scenes.js visual
(rendered locally with puppeteer via video/render_frames.js), and FFmpeg for
assembly. Output matches the render server's look because the visual comes from
the same generateQuizHTML — see docs/video-pipeline.md.

    python -m video.make_question_video 1056 [--voice avri|hila] [--all] [--bg-clip path] [--license 11]

Per question it writes, under output/videos/:
    q<num>.mp4   q<num>.srt   q<num>.mp3
"""
import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import edge_tts

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "output", "videos")
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"          # drawtext (timer) — Hebrew-capable
SUB_FONT = "Arial"                                  # libass FontName

VOICES = {"avri": "he-IL-AvriNeural", "hila": "he-IL-HilaNeural"}
FPS = 30
W, H = 1080, 1920
PAUSE_SEC = 4.0          # the [[PAUSE]] think-gap (spec point 2)
OUTRO_SEC = 2.6
CARD_H = 1480          # rendered card height; pinned near top so the bottom band is a clean caption zone
CARD_Y = 70            # card top offset inside the 1920 frame
NIQQUD = re.compile(r"[\u0591-\u05C7]")
OUTRO_TEXT = "אלכס ארגוב · סקיפר דיגיטלי · alargov.com"


# ── FFmpeg helpers ──────────────────────────────────────────────────────────
def run(args, cwd=None):
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", cwd=cwd)
    if r.returncode:
        sys.stderr.write("FFMPEG ERR:\n" + (r.stderr or "")[-1600:] + "\n")
        raise SystemExit(f"ffmpeg failed ({args[0]})")
    return r


def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


# ── Canonical frames + VO via the Node helper ───────────────────────────────
def render_frames(num, work, license):
    helper = os.path.join(ROOT, "video", "render_frames.js")
    r = subprocess.run(["node", helper, str(num), work, "--license", str(license)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        sys.stderr.write((r.stderr or r.stdout or "")[-1200:] + "\n")
        raise SystemExit(f"render_frames.js failed for Q{num}")
    line = [l for l in r.stdout.strip().splitlines() if l.strip().startswith("{")][-1]
    meta = json.loads(line)
    meta["vo"] = open(meta["voPath"], encoding="utf-8").read().strip()
    # display/caption text: vessel letters kept as "J" (not the spoken "ג'יי")
    dp = meta.get("voDisplayPath")
    meta["voDisplay"] = open(dp, encoding="utf-8").read().strip() if dp and os.path.isfile(dp) else meta["vo"]
    return meta


# ── edge-tts: MP3 + word boundaries (for synced SRT) ────────────────────────
async def tts_part(text, voice, mp3_path, rate="+0%"):
    """Synthesize one narration part; return list of (start_s, end_s, word)."""
    text = text.strip()
    last_err = None
    for attempt in range(1, 4):
        try:
            boundaries = []
            with open(mp3_path, "wb") as f:
                comm = edge_tts.Communicate(text, voice, rate=rate)
                async for ch in comm.stream():
                    if ch["type"] == "audio":
                        f.write(ch["data"])
                    elif ch["type"] in ("WordBoundary", "SentenceBoundary"):
                        s = ch["offset"] / 1e7
                        boundaries.append((s, s + ch["duration"] / 1e7, ch["text"]))
            if os.path.getsize(mp3_path) > 0 and dur(mp3_path) > 0.3:
                return boundaries
            last_err = "empty/short audio"
        except Exception as e:                       # NoAudioReceived etc.
            last_err = str(e)
        print(f"  !! TTS retry {attempt}/3 ({last_err})")
        await asyncio.sleep(1.5 * attempt)
    raise SystemExit(f"TTS failed: {last_err}")


def srt_time(t):
    if t < 0:
        t = 0
    h = int(t // 3600); m = int(t % 3600 // 60); s = int(t % 60); ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s += 1; ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


MAX_CUE_CHARS = 34


def _chunk_words(text, limit=MAX_CUE_CHARS):
    """Split a caption into <=limit-char chunks on word boundaries."""
    chunks, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > limit:
            chunks.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        chunks.append(cur)
    return chunks


def group_cues(boundaries, offset):
    """Turn (start,end,text) boundaries — word- OR sentence-level, whichever the
    voice emits (Hebrew edge-tts gives SentenceBoundary) — into short RTL cues,
    splitting a long span across its time window proportionally by length."""
    cues = []
    for s, e, text in boundaries:
        text = NIQQUD.sub("", text).strip()
        if not text:
            continue
        chunks = _chunk_words(text)
        span = max(0.001, e - s)
        total = sum(len(c) for c in chunks) or 1
        t = s
        for c in chunks:
            ct = span * (len(c) / total)
            cues.append((t + offset, t + ct + offset, c))
            t += ct
    return cues


def write_srt(cues, path):
    with open(path, "w", encoding="utf-8") as f:
        for i, (s, e, txt) in enumerate(cues, 1):
            f.write(f"{i}\n{srt_time(s)} --> {srt_time(e)}\n{txt}\n\n")


def ass_time(t):
    if t < 0:
        t = 0
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def write_ass(cues, path):
    """Real-pixel ASS (PlayRes 1080x1920) so caption size/position are in true px —
    an SRT is interpreted in libass's 384x288 default space and scales unpredictably."""
    head = (
        "[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n"
        "WrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
        "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
        "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: Def,Arial,46,&H00FFFFFF,&H000000FF,&H00301A0C,&H64000000,"
        "-1,0,0,0,100,100,0,0,1,4,1,2,70,70,110,1\n\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(head)
        for s, e, txt in cues:
            txt = txt.replace("\n", " ").strip()
            f.write(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},Def,,0,0,0,,{txt}\n")


# ── Segment builders (each -> uniform mp4 so we can concat by demuxer) ───────
VENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS)]
AENC = ["-c:a", "aac", "-ar", "44100", "-ac", "2", "-b:a", "192k"]


def _bg_filter(seconds, bg_clip):
    if bg_clip:
        return ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,eq=brightness=-0.22:saturation=0.85,"
                f"trim=duration={seconds:.3f},setsar=1,fps={FPS}[bg]")
    frames = max(1, int(seconds * FPS))
    # subtle Ken Burns zoom on a deep-blue gradient
    return (f"[0:v]scale=1296:2304,zoompan=z='min(zoom+0.00035,1.10)':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={FPS},"
            f"trim=duration={seconds:.3f},setsar=1[bg]")


def build_segment(out, png, seconds, bg_clip, work, audio=None, timer=False):
    inp = []
    if bg_clip:
        inp += ["-stream_loop", "-1", "-i", bg_clip]
    else:
        inp += ["-f", "lavfi", "-i",
                f"gradients=s=1080x1920:c0=0x0c1a3a:c1=0x050d1a:c2=0x0a2148:"
                f"nb_colors=3:speed=0.008:duration={seconds:.3f}"]
    inp += ["-loop", "1", "-t", f"{seconds:.3f}", "-i", png]

    fc = _bg_filter(seconds, bg_clip)
    fc += f";[1:v]scale=-1:{CARD_H}:force_original_aspect_ratio=decrease,setsar=1[card]"
    fc += f";[bg][card]overlay=(W-w)/2:{CARD_Y}[v]"
    if timer:
        # relative fontfile (resolved via cwd=work); drawtext+fontconfig segfaults on this build
        fc += (";[v]drawtext=fontfile=f.ttf:"
               f"text='%{{eif\\:max(1\\,ceil({seconds:.0f}-t))\\:d}}':"
               "fontsize=150:fontcolor=white:x=(w-tw)/2:y=h*0.10:"
               "box=1:boxcolor=0x0c1a3a@0.75:boxborderw=40[v]")

    args = ["ffmpeg", "-y", *inp]
    if audio:
        args += ["-i", audio]
        amap = f"{2}:a"
    else:
        args += ["-f", "lavfi", "-t", f"{seconds:.3f}", "-i", "anullsrc=r=44100:cl=stereo"]
        amap = f"{2}:a"
    args += ["-filter_complex", fc, "-map", "[v]", "-map", amap,
             "-t", f"{seconds:.3f}", *VENC, *AENC, "-shortest", out]
    run(args, cwd=work)


# ── One question ────────────────────────────────────────────────────────────
def setup_fonts(work):
    """Copy a Hebrew-capable font into the work dir so drawtext (fontfile=f.ttf) and
    libass (fontsdir=.) resolve it WITHOUT fontconfig, which segfaults drawtext here."""
    for src in ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"):
        if os.path.isfile(src):
            shutil.copy(src, os.path.join(work, "f.ttf"))
            return
    raise SystemExit("no Arial font found under C:/Windows/Fonts")


async def make_one(num, voice_key, bg_clip, license, work):
    voice = VOICES[voice_key]
    setup_fonts(work)
    print(f"[{num}] rendering canonical frames...")
    meta = render_frames(num, work, license)
    vo = meta["vo"]
    # VO-text sidecar next to the video (project rule: every video ships with its VO).
    # Uses the display text so the letters read as "J", matching the captions.
    with open(os.path.join(OUT_DIR, f"q{num}.vo.txt"), "w", encoding="utf-8") as f:
        f.write(meta.get("voDisplay", vo).replace(" [[PAUSE]] ", "\n\n[[PAUSE]]\n\n"))
    if "[[PAUSE]]" in vo:
        part1, part2 = [p.strip() for p in vo.split("[[PAUSE]]", 1)]
    else:
        part1, part2 = vo, ""

    print(f"[{num}] TTS ({voice})...")
    p1_mp3 = os.path.join(work, "p1.mp3")
    p2_mp3 = os.path.join(work, "p2.mp3")
    b1 = await tts_part(part1, voice, p1_mp3)
    b2 = await tts_part(part2, voice, p2_mp3) if part2 else []
    d1, d2 = dur(p1_mp3), dur(p2_mp3) if part2 else 0.0

    # combined narration track (q<num>.mp3 sidecar): part1 + 4s silence + part2
    mp3_out = os.path.join(OUT_DIR, f"q{num}.mp3")
    sil = os.path.join(work, "sil.mp3")
    run(["ffmpeg", "-y", "-f", "lavfi", "-t", f"{PAUSE_SEC:.3f}", "-i",
         "anullsrc=r=44100:cl=stereo", "-c:a", "libmp3lame", sil])
    concat_txt = os.path.join(work, "acat.txt")
    parts = [p1_mp3, sil] + ([p2_mp3] if part2 else [])
    with open(concat_txt, "w", encoding="utf-8") as f:
        for p in parts:
            f.write(f"file '{p.replace(chr(92), '/')}'\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c:a", "libmp3lame", mp3_out])

    # Captions use the DISPLAY text (vessel letters as "J", not the spoken "ג'יי").
    # It differs from the spoken text only in those letters, so distributing it
    # across each part's measured audio duration keeps the caption timing.
    vo_disp = meta.get("voDisplay", vo)
    if "[[PAUSE]]" in vo_disp:
        disp1, disp2 = [p.strip() for p in vo_disp.split("[[PAUSE]]", 1)]
    else:
        disp1, disp2 = vo_disp, ""
    cues = group_cues([(0.0, d1, disp1)], 0.0)
    if part2:
        cues += group_cues([(0.0, d2, disp2)], d1 + PAUSE_SEC)
    tail = d1 + PAUSE_SEC + d2
    cues.append((tail + 0.15, tail + OUTRO_SEC, OUTRO_TEXT))
    srt_out = os.path.join(OUT_DIR, f"q{num}.srt")
    write_srt(cues, srt_out)
    # ASS in the work dir (colon-free relative name) drives the burn
    write_ass(cues, os.path.join(work, "subs.ass"))

    # segments
    print(f"[{num}] building segments...")
    s_q = os.path.join(work, "seg_q.mp4")
    s_p = os.path.join(work, "seg_p.mp4")
    s_a = os.path.join(work, "seg_a.mp4")
    s_o = os.path.join(work, "seg_o.mp4")
    build_segment(s_q, meta["questionPng"], d1, bg_clip, work, audio=p1_mp3)
    build_segment(s_p, meta["questionPng"], PAUSE_SEC, bg_clip, work, audio=None, timer=True)
    segs = [s_q, s_p]
    if part2:
        build_segment(s_a, meta["answerPng"], d2, bg_clip, work, audio=p2_mp3)
        segs.append(s_a)
    build_segment(s_o, meta["answerPng"], OUTRO_SEC, bg_clip, work, audio=None)
    segs.append(s_o)

    vcat = os.path.join(work, "vcat.txt")
    with open(vcat, "w", encoding="utf-8") as f:
        for s in segs:
            f.write(f"file '{s.replace(chr(92), '/')}'\n")
    joined = os.path.join(work, "joined.mp4")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", vcat, "-c", "copy", joined])

    # burn subtitles (run in work dir so the filter path has no drive colon)
    out_mp4 = os.path.join(OUT_DIR, f"q{num}.mp4")
    run(["ffmpeg", "-y", "-i", joined, "-vf", "subtitles=subs.ass:fontsdir=.",
         *VENC, "-c:a", "copy", out_mp4], cwd=work)
    print(f"[{num}] OK -> {out_mp4}  ({dur(out_mp4):.1f}s)")
    return out_mp4


def list_license_nums(license):
    bank = os.path.join(ROOT, "data", f"l{license}.json")
    arr = json.load(open(bank, encoding="utf-8"))
    if not isinstance(arr, list):
        arr = arr.get("questions") or next(v for v in arr.values() if isinstance(v, list))
    return [q["num"] for q in arr]


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("num", nargs="?", help="question number (e.g. 1056)")
    ap.add_argument("--voice", choices=list(VOICES), default="avri")
    ap.add_argument("--all", action="store_true", help="every license-11 question, skipping existing")
    ap.add_argument("--bg-clip", default=None, help="looping background video (darkened 40%%)")
    ap.add_argument("--license", default="11")
    a = ap.parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)
    if a.bg_clip and not os.path.isfile(a.bg_clip):
        sys.exit(f"--bg-clip not found: {a.bg_clip}")

    if a.all:
        nums = list_license_nums(a.license)
    elif a.num:
        nums = [a.num]
    else:
        sys.exit("give a question number or --all")

    ok = fail = skip = 0
    for i, num in enumerate(nums, 1):
        out_mp4 = os.path.join(OUT_DIR, f"q{num}.mp4")
        if a.all and os.path.isfile(out_mp4):
            skip += 1
            continue
        print(f"--- ({i}/{len(nums)}) Q{num} ---")
        with tempfile.TemporaryDirectory(prefix=f"skq_{num}_") as work:
            try:
                await make_one(str(num), a.voice, a.bg_clip, a.license, work)
                ok += 1
            except SystemExit as e:
                fail += 1
                print(f"[{num}] FAIL: {e}")
    print(f"\n=== {ok} ok, {fail} fail, {skip} skipped of {len(nums)} ===")


if __name__ == "__main__":
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
