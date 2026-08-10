#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
הוספה ישירה למילון הניקוד.

שימוש:
    python tools/add-niqqud.py "בַּיַּבָּשָׁה"
    python tools/add-niqqud.py "מֵיִדֵיי" --plain "מיידיי"
    python tools/add-niqqud.py "בַּיַּבָּשָׁה" "שֶׁטָּבַע" "בִּמְקוֹם"

מקבל מילה מנוקדת (או כמה), גוזר את הצורה הרגילה ע"י הסרת סימני ניקוד,
בודק כפילות לפי הצורה הרגילה, ומוסיף שורה לטבלת "## מילים"
ב-references/niqqud-lexicon.md. אם המילה כבר קיימת עם ניקוד שונה — מעדכן.
"""
import sys
import os
import argparse

LEXICON = os.path.join(os.path.dirname(__file__), "..", "references", "niqqud-lexicon.md")
SECTION = "## מילים"
NEXT_SECTION = "## מקרים מיוחדים"

# טווחי ניקוד/טעמים עבריים להסרה (נשארות רק אותיות הבסיס)
NIQQUD = set(range(0x0591, 0x05C7 + 1))  # accents, points, dagesh, meteg, etc.


def strip_niqqud(s):
    return "".join(c for c in s if ord(c) not in NIQQUD).strip()


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def save(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def table_bounds(lines):
    """מחזיר (start, end) של אינדקסי שורות הטבלה בסקציית ## מילים.
    start = אינדקס שורת הכותרת (| רגיל | מנוקד |), end = אחרי שורת הטבלה האחרונה."""
    try:
        sec = next(i for i, l in enumerate(lines) if l.strip() == SECTION)
    except StopIteration:
        raise SystemExit(f"לא נמצאה הסקציה '{SECTION}' ב-{path}")
    # גבול תחתון: הסקציה הבאה
    end_limit = next((i for i in range(sec + 1, len(lines))
                      if lines[i].strip() == NEXT_SECTION), len(lines))
    rows = [i for i in range(sec + 1, end_limit) if lines[i].lstrip().startswith("|")]
    if not rows:
        raise SystemExit("לא נמצאה טבלה בסקציית המילים")
    return rows[0], rows[-1]


def parse_rows(lines, first, last):
    """מחזיר dict של {plain: index} לכל שורות הנתונים (מדלג על כותרת ומפריד)."""
    out = {}
    for i in range(first, last + 1):
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        plain = cells[0]
        if plain in ("רגיל", "") or set(plain) <= set("-: "):
            continue  # כותרת או מפריד
        out[plain] = i
    return out


def main():
    ap = argparse.ArgumentParser(description="הוספת מילה מנוקדת למילון הניקוד")
    ap.add_argument("words", nargs="+", help="מילה/מילים מנוקדות")
    ap.add_argument("--plain", help="דריסת הצורה הרגילה (רק כשמעבירים מילה אחת)")
    args = ap.parse_args()

    if args.plain and len(args.words) != 1:
        raise SystemExit("--plain אפשרי רק עם מילה אחת")

    lines = load(LEXICON)
    first, last = table_bounds(lines)
    existing = parse_rows(lines, first, last)

    added, updated, skipped = [], [], []
    inserts = []  # (row_text) לשורות חדשות

    for w in args.words:
        niqqud = w.strip()
        plain = args.plain.strip() if args.plain else strip_niqqud(niqqud)
        if not plain:
            skipped.append((w, "לא נגזרה צורה רגילה"))
            continue
        row = f"| {plain} | {niqqud} |"
        if plain in existing:
            idx = existing[plain]
            if lines[idx].strip() == row.strip():
                skipped.append((plain, "כבר קיים זהה"))
            else:
                lines[idx] = row
                updated.append((plain, niqqud))
        else:
            inserts.append(row)
            added.append((plain, niqqud))

    # מוסיפים את החדשות אחרי שורת הטבלה האחרונה
    if inserts:
        # last עשוי להשתנות אם עדכנו במקום — נחשב מחדש
        _, last = table_bounds(lines)
        lines[last + 1:last + 1] = inserts

    save(LEXICON, lines)

    for p, n in added:
        print(f"נוסף:   {p} -> {n}")
    for p, n in updated:
        print(f"עודכן:  {p} -> {n}")
    for p, why in skipped:
        print(f"דילוג:  {p} ({why})")


if __name__ == "__main__":
    main()
