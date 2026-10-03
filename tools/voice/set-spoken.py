# -*- coding: utf-8 -*-
"""
set-spoken.py — כותב explanation_spoken לשאלות בבנק, in-place, בפורמט הבייטים של הבנק
(CRLF, הזחה 2, UTF-8 בלי escape). השדה נכנס מיד אחרי explanation; שאר השדות לא נוגעים.

    python tools/voice/set-spoken.py <spoken.json> [--license 11]
    python tools/voice/set-spoken.py --check [--license 11]     # בדיקת roundtrip בלבד

spoken.json: {"<num>": "<טקסט מדובר אחרי 'התשובה הנכונה... X'!'>", ...}
"""
import json, sys, os

a = sys.argv[1:]
lic = a[a.index("--license") + 1] if "--license" in a else "11"
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
bank = os.path.join(root, "data", f"l{lic}.json")
raw = open(bank, "rb").read()


def dump(d):
    return (json.dumps(d, ensure_ascii=False, indent=2).replace("\n", "\r\n")).encode("utf-8")


d = json.loads(raw.decode("utf-8"))
tail = raw[len(dump(d)):]
if dump(d) + tail != raw:
    sys.exit("ABORT: bank does not roundtrip byte-identical, not writing")
if "--check" in a:
    print("roundtrip OK", len(d), "tail", tail)
    sys.exit(0)

src = json.load(open(a[0], encoding="utf-8"))
out, n = [], 0
for q in d:
    s = src.get(str(q.get("num")))
    if s is not None:
        q2 = {}
        for k, v in q.items():
            if k == "explanation_spoken":
                continue
            q2[k] = v
            if k == "explanation":
                q2["explanation_spoken"] = s.strip()
        if "explanation_spoken" not in q2:
            q2["explanation_spoken"] = s.strip()
        q, n = q2, n + 1
    out.append(q)
open(bank, "wb").write(dump(out) + tail)
print(f"wrote explanation_spoken for {n} questions -> {bank}")
