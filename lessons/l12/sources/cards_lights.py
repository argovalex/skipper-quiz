"""Cards for l12 lesson 'אורות לילה' (palette/layout per lessons/l11/cards/סימני יום)."""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display

ROOT = r"C:\Users\argov\OneDrive\Co-Work OS\SkipperQuiz"
OUT = os.path.join(ROOT, "lessons", "l12", "cards", "אורות לילה")
SIGNS = os.path.join(ROOT, "media", "signs")
NIGHT = os.path.join(ROOT, "media", "vessels", "night")
VESS = {"title": "power_big", "s_groups": "power_big", "s_headon": "power_big_bow", "s_stern": "power_big_stern",
  "s_method": "power_small", "s_white": "power_big", "s_sail": "sail", "s_pilot": "pilot", "s_fish": "trawler",
  "s_rwr": "ram", "s_diamonds": "dredge", "s_divers": "divers", "s_draft": "draft", "s_mines": "mines_port",
  "s_nuc": "nuc", "s_aground": "aground", "s_anchor": "anchor_small", "s_anchor50": "anchor_big", "s_tow": "tow",
  "s_tow200": "tow_long", "s_yellow": "tow_stern", "s_flash": "hover", "s_ex1": "tow_stern", "s_ex2": "pilot_port"}
W, H = 1280, 720
BG, BAR, PANEL, TXT, ORANGE, BLUE, LOGIC = "#0E1A2D", "#22A05A", "#182842", "#F0F5FA", "#DCA03C", "#5A96DC", "#1F2F2A"
F = r"C:\Windows\Fonts\arialbd.ttf"
FR = r"C:\Windows\Fonts\arial.ttf"
font = lambda s, b=True: ImageFont.truetype(F if b else FR, s)
he = lambda t: get_display(t)

CARDS = {
 "title":     ("אורות לילה", "רשיון סירת מנוע · מבחן תאוריה", "לא זוכרים תמונות בעל פה. מבינים את התמונה.", [5]),
 "s_groups":  ("שלוש קבוצות אורות", None, "ניווט: לאן הוא מפליג | גודל (לבן למעלה): יש מנוע | משפחה (360°): מי הוא", [15]),
 "s_sectors": ("אורות ניווט גזרתיים", None, "ירוק ימין, אדום שמאל: 112.5° כל אחד | לבן ירכתיים: 135°", "SECTORS"),
 "s_headon":  ("אדום וירוק יחד", None, "הוא בא ישר מולך. קורס התנגשות.", [5]),
 "s_stern":   ("רק לבן מאחור", None, "מאחור כולם נראים אותו דבר. בלי צבע מעליו: ממוכן או מפרשית.", [27]),
 "s_method":  ("השיטה: קו מעל אורות הניווט", None, "מתחת לקו: איפה הוא יחסית אליי | מעל הקו: מי הוא | ואז: מי מפנה", [30]),
 "s_rules":   ("אותם חוקי פינוי", None, "ממוכן ← מפרש ← דייג ← מוגבל ← חסר שליטה", "LADDER"),
 "s_white":   ("לבן למעלה = יש מנוע", None, "לבן אחד: עד 50 מ' | שניים: מעל 50 מ'. הגודל לא משנה. ממוכן.", [15, 5]),
 "s_sail":    ("אין לבן = אין מנוע", None, "רק אדום: דופן שמאל של מפרשית. אדום מעל ירוק בתורן: אורות רשות.", [24, 14]),
 "s_pilot":   ("לבן מעל אדום = נתב", None, "כמו דגל H ביום. ממוכן לכל דבר. אין לו זכות עליך.", [46]),
 "s_fish":    ("צבע מעל לבן = דייג", None, "ירוק/לבן: מכמורתן | אדום/לבן: רשתות. מפנים לו. לבן למעלה? נתב.", [64, 55]),
 "s_rwr":     ("אדום · לבן · אדום = מוגבל", None, "כמו כדור-יהלום-כדור ביום. מפנים לו.", [35]),
 "s_diamonds":("נוסעים ליהלומים", None, "שני ירוקים: עוברים | שני אדומים: לא עוברים. אדום = אזהרה.", [50]),
 "s_divers":  ("אדום·לבן·אדום בלי ניווט", None, "עומד ומוגבל: ספינת אם לצוללנים. מתרחקים 200 מ'.", [70]),
 "s_draft":   ("שלושה אדומים = מוגבל בשוקע", None, "ביום: חבית. מפנים. עוברים מאחוריו.", [25]),
 "s_mines":   ("שלושה ירוקים = שולת מוקשים", None, "מתרחקים.", [56]),
 "s_nuc":     ("שני אדומים + ניווט = חסר שליטה", None, "עושה דרכו במים, נסחף. אין לבן, אין מנוע.", [33]),
 "s_aground": ("שני אדומים בלי ניווט = שרטון", None, "עומד. שני אדומים + לבן עגינה.", [7]),
 "s_anchor":  ("עוגן עד 50 מטר: לבן אחד", None, "לבן אחד, רואים אותו מכל כיוון. בלי אורות ניווט.", [27]),
 "s_anchor50":("עוגן מעל 50 מטר: שני לבנים", None, "אחד בחרטום, אחד בירכתיים. הקדמי גבוה יותר.", [61]),
 "s_tow":     ("פעמיים אורות ניווט = גוררת", None, "בלי אדום-לבן-אדום: ממוכנת. כמות הלבנים לא משנה.", [6]),
 "s_tow200":  ("גוררת: עד 200 מ' ומעל 200 מ'", None, "משך עד 200 מ': שני לבנים בקו אחד | מעל 200 מ': שלושה", []),
 "s_yellow":  ("צהוב מאחור = גוררת", None, "צהוב קבוע מעל אור הירכתיים.", [17]),
 "s_flash":   ("צהוב מהבהב = רחפת", None, "לא גוררת.", [16]),
 "s_port":    ("יציאה מהנמל", None, "יוצא: שמאל על הירוק, ימין על האדום | חוזר: הפוך", [74, 71]),
 "s_ex1":     ("שאלה: צהוב מימין", None, "גוררת, מאחור. כבר חלפה. ממשיך בקורס ובמהירות.", [17]),
 "s_ex2":     ("שאלה: נתב משמאל לחרטום", None, "דופן שמאל מול דופן שמאל. חולפים. אין סכנת התנגשות.", [46]),
 "s_exam":    ("טיפים למבחן", None, "קרא את כל התשובות | שלול | צייר: אתה, הוא, הדופן | כמות הלבנים מבלבלת", None),
 "s_sum":     ("סיכום: האלגוריתם", None, "יש או אין אורות ניווט | איפה הוא יחסית אליי | לבן למעלה = מנוע | צבעים = המשפחה | לפי החוקים: מי מפנה", None),
}

def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(he(t), font=fnt) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def rtext(d, x_right, y, text, fnt, fill):
    s = he(text); d.text((x_right - d.textlength(s, font=fnt), y), s, font=fnt, fill=fill)

def sign(n, box):
    im = Image.open(os.path.join(SIGNS, f"tmuna_{n:03d}.png")).convert("RGB")
    im.thumbnail(box); return im

def sectors(c, d, x0, y0, w, h):
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 24, fill="#000000")
    cx, cy, r = x0 + w // 2, y0 + h // 2 + 10, min(w, h) // 2 - 40
    # heading up; PIL angles: 0=east, clockwise. Bow = -90.
    d.pieslice((cx - r, cy - r, cx + r, cy + r), -90, -90 + 112.5, fill="#1E6B3A")
    d.pieslice((cx - r, cy - r, cx + r, cy + r), -90 - 112.5, -90, fill="#7A2020")
    d.pieslice((cx - r, cy - r, cx + r, cy + r), 22.5, 157.5, fill="#7A7A7A")
    d.polygon([(cx, cy - 50), (cx + 18, cy + 30), (cx - 18, cy + 30)], fill=TXT)
    rtext(d, cx + 95, cy - r + 60, "ירוק", font(26), TXT)
    rtext(d, cx - 40, cy - r + 60, "אדום", font(26), TXT)
    rtext(d, cx + 30, cy + r - 60, "לבן", font(26), TXT)

def ladder(d, x0, y0, w):
    steps = ["ממוכן", "מפרש", "דייג", "מוגבל", "חסר שליטה"]
    for i, s in enumerate(steps):
        bw = 220 + i * 50; x = x0 + (w - bw) // 2; y = y0 + i * 70
        d.rounded_rectangle((x, y, x + bw, y + 54), 12, fill=BAR if i == 4 else PANEL)
        t = he(s); f = font(28); d.text((x + (bw - d.textlength(t, font=f)) // 2, y + 10), t, font=f, fill=TXT)

def make(sid, spec):
    title, sub, logic, imgs = spec
    c = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 8), fill=BAR)
    rtext(d, 1190, 40, "אורות לילה", font(34), BAR)
    if imgs is None or sid in ("s_exam", "s_sum"):
        rtext(d, 1190, 130, title, font(56), TXT)
        y = 240
        for part in logic.split(" | "):
            d.rounded_rectangle((120, y, 1190, y + 70), 16, fill=PANEL)
            rtext(d, 1160, y + 16, part, font(32, False), TXT); y += 88
        c.save(os.path.join(OUT, sid + ".png")); return
    # left visual panel
    px, py, pw, ph = 90, 150, 470, 470
    if imgs == "SECTORS": sectors(c, d, px, py, pw, ph)
    elif imgs == "LADDER": ladder(d, px, py + 60, pw)
    elif sid in VESS:
        fam = VESS[sid]
        def put(name, x, y, w, h, label=None):
            vi = Image.open(os.path.join(NIGHT, name + ".jpg")).convert("RGB")
            if vi.width / vi.height > 1.6:      # wide tow scene: fit, keep both vessels
                s_ = w / vi.width; vi = vi.resize((w, int(vi.height * s_)))
                bg = Image.new("RGB", (w, h), vi.getpixel((5, 5))); bg.paste(vi, (0, (h - vi.height) // 2)); vi = bg
            else:
                s_ = max(w / vi.width, h / vi.height); vi = vi.resize((int(vi.width * s_), int(vi.height * s_)))
                l, t = (vi.width - w) // 2, (vi.height - h) // 2; vi = vi.crop((l, t, l + w, t + h))
            m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), 18, fill=255)
            c.paste(vi, (x, y), m)
            if label:
                f = font(22); t_ = he(label); tw = d.textlength(t_, font=f)
                d.rounded_rectangle((x + w - tw - 26, y + 10, x + w - 10, y + 42), 8, fill=PANEL)
                d.text((x + w - tw - 18, y + 13), t_, font=f, fill=TXT)
        if os.path.exists(os.path.join(NIGHT, fam + "_bow.jpg")) or os.path.exists(os.path.join(NIGHT, fam + "_port.jpg")):
            put(fam + "_port", 40, 90, 560, 330, "דופן שמאל")
            if os.path.exists(os.path.join(NIGHT, fam + "_bow.jpg")):
                put(fam + "_bow", 40, 432, 275, 260, "חרטום")
            stern = fam + "_stern" if os.path.exists(os.path.join(NIGHT, fam + "_stern.jpg")) else "tow_stern"
            if os.path.exists(os.path.join(NIGHT, stern + ".jpg")):
                put(stern, 325, 432, 275, 260, "ירכתיים")
        else:
            put(fam, 40, 100, 560, 420)
        x = 1210
        for k in imgs:
            im = sign(k, (130, 130)); tag = he(f"תמונה {k}"); f = font(24); tw = d.textlength(tag, font=f)
            x -= im.width; c.paste(im, (x, 560))
            d.text((int(x - tw - 12), 560 + im.height // 2 - 14), tag, font=f, fill=TXT)
            x = int(x - tw - 40)
    else:
        d.rounded_rectangle((px, py, px + pw, py + ph), 24, fill="#000000")
        n = len(imgs); cellw = (pw - 20) // n
        for i, k in enumerate(imgs):
            im = sign(k, (cellw - 20, ph - 90))
            x = px + 10 + i * cellw + (cellw - im.width) // 2; y = py + 20 + (ph - 90 - im.height) // 2
            c.paste(im, (x, y))
            tag = he(f"תמונה {k}"); f = font(26); tw = d.textlength(tag, font=f)
            tx = px + 10 + i * cellw + (cellw - tw) // 2
            d.rounded_rectangle((tx - 14, py + ph - 56, tx + tw + 14, py + ph - 14), 10, fill=PANEL)
            d.text((tx, py + ph - 52), tag, font=f, fill=TXT)
    # right text
    tf = font(50 if len(title) < 22 else 42)
    lines = wrap(d, title, tf, 560); y = 200 if sub is None else 170
    for ln in lines: rtext(d, 1190, y, ln, tf, TXT); y += 64
    if sub: rtext(d, 1190, y, sub, font(30, False), BLUE); y += 50
    y += 20
    parts = logic.split(" | "); lf = font(30, False)
    body = [l for p in parts for l in wrap(d, p, lf, 520)]
    bh = 70 + len(body) * 44
    d.rounded_rectangle((620, y, 1210, y + bh), 20, fill=LOGIC)
    rtext(d, 1180, y + 16, "ההיגיון:", font(28), ORANGE)
    yy = y + 58
    for l in body: rtext(d, 1180, yy, l, lf, TXT); yy += 44
    c.save(os.path.join(OUT, sid + ".png"))

os.makedirs(OUT, exist_ok=True)
for sid, spec in CARDS.items(): make(sid, spec)
print("cards:", len(CARDS))
