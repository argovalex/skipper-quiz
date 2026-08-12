# -*- coding: utf-8 -*-
"""
niqqud.py — מחיל את מילון הניקוד הקנוני על טקסט VO של מערכי שיעור.

מקור האמת: references/niqqud-lexicon.md (טבלת "## מילים"). זה הטוען היחיד שקורא
את המילון בפועל — שני עותקי apply_niqqud.py הישנים החזיקו רשימה מוקשחת שלא קראה
את הקובץ. אל תשכפל מילון; ערוך את ה-md ותוסיף דרך tools/add-niqqud.py.

שימוש כמסנן (מנקד את הקלט):
    python tools/lesson/niqqud.py "כלי שיט נמצא במצוקה"
    echo "..." | python tools/lesson/niqqud.py
כמודול:
    from niqqud import load_lexicon, apply
    lex = load_lexicon(); text = apply(raw, lex)
"""
import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEXICON = os.path.join(REPO, "references", "niqqud-lexicon.md")
_MARK = "֑-ׇ"      # סימני ניקוד/טעמים
_LETTER = "א-ת"    # אותיות עבריות
_ROW = re.compile(r"^\|(.+?)\|(.+?)\|\s*$")


def load_lexicon(path=LEXICON):
    """קורא את טבלת '## מילים' ומחזיר רשימת (מקור, מנוקד) ממוינת מהארוך לקצר."""
    pairs = []
    in_words = False
    for line in open(path, encoding="utf-8"):
        s = line.rstrip("\n")
        if s.startswith("## "):
            in_words = s.strip() == "## מילים"
            continue
        if not in_words:
            continue
        m = _ROW.match(s)
        if not m:
            continue
        src, dst = m.group(1).strip(), m.group(2).strip()
        if src in ("רגיל",) or set(src) <= set("-: "):   # כותרת/מפריד
            continue
        src = src.split(" (")[0].strip()                  # מסיר רמז בסוגריים
        if src and dst:
            pairs.append((src, dst))
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    return pairs


def apply(text, lex=None):
    """מחליף כל מילה במילון בצורתה המנוקדת, גבולות-מילה, בלי לגעת בטקסט שכבר מנוקד."""
    if lex is None:
        lex = load_lexicon()
    for src, dst in lex:
        pat = r"(?<![%s%s])%s(?![%s%s])" % (_LETTER, _MARK, re.escape(src), _LETTER, _MARK)
        text = re.sub(pat, dst, text)
    return text


if __name__ == "__main__":
    inp = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read()
    sys.stdout.write(apply(inp))
