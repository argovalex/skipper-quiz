# -*- coding: utf-8 -*-
"""
niqqud.py — מחיל את מילון הניקוד על טקסט VO של מערכי שיעור.

המנוע עצמו הוא אחד: applyLexiconText ב-tools/quiz-app/vo.js (אותו מנוע של רינדור
השאלות). הקובץ הזה רק מעביר אליו את הטקסט דרך tools/quiz-app/niqqud-cli.js, כך
שאין שני מימושים שנפרדים זה מזה. כללים: reports/niqqud-engines-2026-10-21.md.
מקור האמת למילים: references/niqqud-lexicon.md (רק אלכס עורך).

שימוש כמסנן:
    python tools/lesson/niqqud.py "כלי שיט נמצא במצוקה"
    echo "..." | python tools/lesson/niqqud.py
כמודול:
    from niqqud import load_lexicon, apply
    text = apply(raw)                 # mode="lesson" כברירת מחדל
"""
import os, re, subprocess, sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEXICON = os.path.join(REPO, "references", "niqqud-lexicon.md")
CLI = os.path.join(REPO, "tools", "quiz-app", "niqqud-cli.js")
_ROW = re.compile(r"^\|(.+?)\|(.+?)\|\s*$")
_NOWIN = getattr(subprocess, "CREATE_NO_WINDOW", 0)


def load_lexicon(path=LEXICON):
    """רשימת (מקור, מנוקד) מטבלת '## מילים'. נשמר לתאימות; apply לא צריך אותו."""
    pairs, in_words = [], False
    for line in open(path, encoding="utf-8"):
        s = line.rstrip("\n")
        if s.startswith("## "):
            in_words = s.strip() == "## מילים"
            continue
        m = _ROW.match(s) if in_words else None
        if not m:
            continue
        src, dst = m.group(1).strip(), m.group(2).strip()
        if src == "רגיל" or set(src) <= set("-: "):
            continue
        src = src.split(" (")[0].strip()
        if src and dst:
            pairs.append((src, dst))
    return pairs


def apply(text, lex=None, mode="lesson", override=False):
    """מנקד דרך המנוע של vo.js. lex נשאר בחתימה לתאימות ולא בשימוש."""
    if not text:
        return text
    args = ["node", CLI, "--mode", mode] + (["--override"] if override else [])
    r = subprocess.run(args, input=text.encode("utf-8"), capture_output=True,
                       cwd=REPO, creationflags=_NOWIN)
    if r.returncode != 0:
        raise RuntimeError("niqqud-cli failed: " + r.stderr.decode("utf-8", "replace"))
    return r.stdout.decode("utf-8")


if __name__ == "__main__":
    inp = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    sys.stdout.write(apply(inp))
