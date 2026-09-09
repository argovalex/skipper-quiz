# -*- coding: utf-8 -*-
"""
integrate_real_video.py — one-command pipeline for wiring a real video clip
into an l12 (or l11) question's mediaUrl, rendering it locally through the
canonical scenes.js visual, and publishing the result via git-raw hosting
(no Railway, no Cloudinary — matches the L12 local-only policy in CLAUDE.md).

    python -m tools.integrate_real_video <num> --clip <path> --slug <slug> [--license 12] [--voice hila]

Steps:
  1. Copy <clip> to media/bgclips/<num>-<slug>-vN.mp4 (the raw source clip).
  2. Set mediaUrl/mediaType on the question in data/l<license>.json.
  3. Render locally via video.make_question_video --bg-clip.
  4. Copy the rendered output to media/videos/<num>-<slug>-vN.mp4.
     N is shared across both files and is one more than any existing vN found
     for this num+slug — raw.githubusercontent caches by path, so re-using a
     filename after changing its content serves stale bytes. Always version up,
     never overwrite.
  5. Set videoUrl + rendered_at on the question, remove superseded vN files.
  6. git add the touched files, commit, rebase onto origin/main, push — stashing
     any unrelated pre-existing tracked changes around the rebase so they
     survive untouched (this repo often has other in-progress edits sitting
     dirty; this script must not swallow or lose them).

Never touches l11 unless --license 11 is passed explicitly, and only ever
edits the one question object matched by --num (text-scoped substitution,
not a JSON re-serialize — the rest of the file stays byte-identical).
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GH_RAW = "https://raw.githubusercontent.com/argovalex/skipper-quiz/main"


def run(args, cwd=None, check=True):
    print("+", " ".join(args))
    r = subprocess.run(args, cwd=cwd or ROOT, text=True)
    if check and r.returncode != 0:
        sys.exit(f"command failed ({r.returncode}): {' '.join(args)}")
    return r


def run_out(args, cwd=None):
    r = subprocess.run(args, cwd=cwd or ROOT, text=True, capture_output=True)
    return r.stdout


def data_path_for(license):
    return os.path.join(ROOT, "data", f"l{license}.json")


def question_block(text, num):
    """Span of this question's object in the raw file text: from its
    "num": N, line up to (not including) the next question's "num": line, or
    end of file. Deliberately not a JSON parse+dump — keeps every other byte
    in the file untouched."""
    m = re.search(r'"num":\s*' + str(num) + r'\s*,', text)
    if not m:
        sys.exit(f"question {num} not found in data file")
    start = m.start()
    nxt = re.search(r'"num":\s*\d+\s*,', text[m.end():])
    end = m.end() + nxt.start() if nxt else len(text)
    return start, end


def set_field(block, field, value):
    """Replace an existing "field": "..." inside block, or insert a new one
    right after videoUrl (same indentation) if the field doesn't exist yet —
    used the first time rendered_at is added to a question."""
    pat = re.compile(r'"' + field + r'":\s*"[^"]*"')
    new = f'"{field}": "{value}"'
    if pat.search(block):
        return pat.sub(new, block, count=1)
    vpat = re.compile(r'"videoUrl":\s*"[^"]*",?\n')
    m = vpat.search(block)
    if not m:
        sys.exit(f'could not find "videoUrl" in question block to anchor insertion of "{field}"')
    line_start = block.rfind("\n", 0, m.start()) + 1
    indent = re.match(r"[ \t]*", block[line_start:m.start()]).group(0)
    insertion = f'{indent}"{field}": "{value}",\n'
    return block[: m.end()] + insertion + block[m.end() :]


def git_dirty_tracked():
    out = run_out(["git", "status", "--porcelain"])
    files = []
    for line in out.splitlines():
        if not line or line.startswith("??"):
            continue
        files.append(line[3:].strip())
    return files


def existing_versions(directory, num, slug):
    pat = re.compile(rf"^{num}-{re.escape(slug)}-v(\d+)\.mp4$")
    found = []
    if os.path.isdir(directory):
        for name in os.listdir(directory):
            m = pat.match(name)
            if m:
                found.append((int(m.group(1)), name))
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("num", type=int)
    ap.add_argument("--clip", required=True, help="path to the real video file to use as background")
    ap.add_argument("--slug", required=True, help="short kebab slug for filenames, e.g. port-exit-buoys")
    ap.add_argument("--license", default="12")
    ap.add_argument("--voice", default="hila", choices=["avri", "hila"])
    ap.add_argument("--no-push", action="store_true", help="do everything except git commit/push")
    a = ap.parse_args()

    if not os.path.isfile(a.clip):
        sys.exit(f"clip not found: {a.clip}")

    bg_dir = os.path.join(ROOT, "media", "bgclips")
    vid_dir = os.path.join(ROOT, "media", "videos")
    prior = existing_versions(bg_dir, a.num, a.slug) + existing_versions(vid_dir, a.num, a.slug)
    nextv = (max(v for v, _ in prior) + 1) if prior else 1

    bgclip_name = f"{a.num}-{a.slug}-v{nextv}.mp4"
    bgclip_rel = f"media/bgclips/{bgclip_name}"
    os.makedirs(bg_dir, exist_ok=True)
    shutil.copyfile(a.clip, os.path.join(bg_dir, bgclip_name))
    print(f"[1/6] copied clip -> {bgclip_rel}")

    data_path = data_path_for(a.license)
    with open(data_path, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    start, end = question_block(text, a.num)
    block = set_field(text[start:end], "mediaUrl", f"{GH_RAW}/{bgclip_rel}")
    block = set_field(block, "mediaType", "video")
    with open(data_path, "w", encoding="utf-8", newline="") as f:
        f.write(text[:start] + block + text[end:])
    print(f"[2/6] set mediaUrl/mediaType on Q{a.num} in data/l{a.license}.json")

    run([sys.executable, "-m", "video.make_question_video", str(a.num),
         "--license", a.license, "--voice", a.voice,
         "--bg-clip", os.path.join(bg_dir, bgclip_name)])
    print("[3/6] rendered locally")

    out_name = f"{a.num}-{a.slug}-v{nextv}.mp4"
    out_rel = f"media/videos/{out_name}"
    local_render = os.path.join(ROOT, "output", "videos", f"q{a.num}.mp4")
    os.makedirs(vid_dir, exist_ok=True)
    shutil.copyfile(local_render, os.path.join(vid_dir, out_name))
    print(f"[4/6] published rendered video -> {out_rel}")

    stale = [name for v, name in existing_versions(vid_dir, a.num, a.slug) if v != nextv]
    for name in stale:
        run(["git", "rm", "-q", f"media/videos/{name}"], check=False)
        also_bg = os.path.join(bg_dir, name)
        if os.path.isfile(also_bg):
            run(["git", "rm", "-q", f"media/bgclips/{name}"], check=False)
    if stale:
        print(f"      removed {len(stale)} superseded version(s): {', '.join(stale)}")

    with open(data_path, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    start, end = question_block(text, a.num)
    rendered_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    block = set_field(text[start:end], "videoUrl", f"{GH_RAW}/{out_rel}")
    block = set_field(block, "rendered_at", rendered_at)
    with open(data_path, "w", encoding="utf-8", newline="") as f:
        f.write(text[:start] + block + text[end:])
    print(f"[5/6] set videoUrl+rendered_at on Q{a.num}")

    if a.no_push:
        print("[6/6] --no-push: leaving changes staged locally, not committing")
        return

    rel_data = os.path.relpath(data_path, ROOT).replace(os.sep, "/")
    ours = {bgclip_rel, out_rel, rel_data}
    dirty = git_dirty_tracked()
    to_stash = [f for f in dirty if f not in ours]
    stashed = False
    if to_stash:
        run(["git", "stash", "push", "-m", "integrate_real_video: pre-existing unrelated changes", "--", *to_stash])
        stashed = True

    run(["git", "add", bgclip_rel, out_rel, rel_data])
    msg = (f"content(l{a.license}): Q#{a.num} integrate real video clip ({a.slug}, v{nextv})\n\n"
           "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>")
    run(["git", "commit", "-m", msg])
    run(["git", "pull", "--rebase", "origin", "main"])
    run(["git", "push"])
    if stashed:
        run(["git", "stash", "pop"])
    print(f"[6/6] committed and pushed -> {out_rel}")
    print(f"\nlocal file for review: output/videos/q{a.num}.mp4")


if __name__ == "__main__":
    main()
