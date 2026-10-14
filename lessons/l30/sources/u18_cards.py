"""Lesson 18 (l30): נוהל מצוקה. Mobile-first: every card renders a native 9:16 card (_v/, visual built at 1080 wide) and the 16:9 card."""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U6 = _load('u06', 'u06_cards.py'); U8 = _load('u08', 'u08_cards.py'); U12 = _load('u12', 'u12_cards.py')
import twcard as T
from twcard import chip, glass, tile, row
from PIL import Image
NAME = 'נוהל מצוקה'
C.OUT = os.path.join(HERE, '..', 'cards', NAME); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · נוהל מצוקה'
F, text_c, text_r, dot, base, left_panel, right_block, save, RC = C.F, C.text_c, C.text_r, C.dot, C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, GREEN, GREEN_L, BLUE_L, PANEL = C.TEXT, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL
photo = U8.photo; credit = U12.credit
CR = {'u18_bounty': 'Photo: U.S. Coast Guard · Public domain'}
U12.CREDIT.update(CR)
X0, Y0, X1, Y1 = [int(v) for v in U5.inner()]; PW, PH = X1 - X0, Y1 - Y0
VOUT = os.path.join(C.OUT, '_v'); VSUB = 'שיעור 18 · נוהל מצוקה'
MOBILE = '--mobile' in sys.argv   # 9:16 cards only after Alex approves the final wide video + subtitles (Alex 2026-10-14)
if MOBILE: os.makedirs(VOUT, exist_ok=True)

def vcredit(bg):
    return f'<div class="absolute bottom-1 right-2 ltr text-white/70 text-[16px]">{CR[bg]}</div>' if bg in CR else ''

def card(sid, caption, body, title, text, q=None, bg=None, pos='center', shade=0.0):
    """Same body HTML rendered twice: 1180x1060 for the wide card, 1080 x VTOP for the phone card."""
    if MOBILE:
        vp = T.panel('v_' + sid, body, T.VW, T.VTOP, bg, pos, shade)
        T.vcard(os.path.join(VOUT, sid + '.png'), caption, T.vimg(vp) + vcredit(bg), T.vbottom(VSUB, title, text, q))
    im, d = base(); left_panel(d, caption)
    pp = T.panel(sid, body, PW, PH, bg, pos, shade); p = Image.open(pp).convert('RGBA'); im.paste(p, (X0, Y0), p)
    if bg in CR: credit(d, (X0, Y0, X1, Y1), bg)
    right_block(d, title, text, q); save(im, sid)

def top(html):
    return f'<div class="absolute top-6 inset-x-6 flex justify-center">{html}</div>'

def fill(html, t=24):
    return f'<div class="absolute inset-x-6 bottom-6 flex flex-col justify-center gap-4" style="top:{t}px">{html}</div>'

def bottom(html):
    return f'<div class="absolute bottom-6 inset-x-6">{html}</div>'

def tiles(items, h=200, hs=46, ss=26, cols=2):
    return f'<div class="grid grid-cols-{cols} gap-4">' + ''.join(tile(n, s, t, f'h-[{h}px]', hs, ss) for n, s, t in items) + '</div>'

def rows(*rs, gap=3):
    return glass(f'<div class="p-6 space-y-{gap}">' + ''.join(row(*r) for r in rs) + '</div>')

def bar(code, he, tone, dim=False):
    b = T.TONES[tone][2]
    return (f'<div class="h-[150px] rounded-3xl {b} flex items-center justify-between gap-6 px-8 {"opacity-30" if dim else ""}">'
            f'<div class="ltr text-white font-extrabold text-[50px] leading-none">{code}</div><div class="text-white text-[34px] font-semibold">{he}</div></div>')

CODES = [('SEELONCE MAYDAY', 'המפקח משתיק', 'red'), ('SEELONCE DISTRESS', 'תחנה אחרת משתיקה', 'amber'),
         ('PRUDONCE', 'לקראת סיום', 'sky'), ('SEELONCE FEENEE', 'סוף המצוקה', 'green')]

def codes(hi=None, extra=''):
    return extra + fill(''.join(bar(c, h, t, hi is not None and c != hi) for c, h, t in CODES), 90 if extra else 24)

SAME = top(chip('אותה שאלה · נוסח אחר', 'amber', 30))

# ---------- cards ----------
def s01():
    items = ['מתי MAYDAY', 'קריאת המצוקה', 'קודי השתקה וסיום', 'ממסר, ביטול ו-IMOT']
    if MOBILE: T.vcard(os.path.join(VOUT, 's01_intro.png'), 'שיעור 18', T.vphoto('u18_bounty', '50% 45%') + vcredit('u18_bounty'),
            T.vbottom('קורס ניווט חופי ומכשירים', 'נוהל מצוקה', '<br>'.join(items)))
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u18_bounty', focus=(0.5, 0.45)); credit(d, (0, 0, 1300, 1440), 'u18_bounty')
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 18', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'נוהל מצוקה', F(118), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(items):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s01o():
    big = ('<div class="flex items-center justify-center gap-6 ltr"><div class="text-amber-300 font-extrabold text-[84px] italic">m&#39;aider</div>'
           '<div class="text-white/80 text-[64px]">→</div><div class="text-rose-400 font-extrabold text-[84px]">MAYDAY</div></div>'
           '<div class="text-center text-white text-[36px] pt-1">עזרו לי · בצרפתית</div>')
    body = fill(glass(f'<div class="p-6">{big}</div>') + rows(('✈', '1923 · קרוידון, לונדון ← פריז', 'sky', 32), ('🌐', '1927 · אות מצוקה בינלאומי', 'green', 32), ('×3', 'שלוש פעמים ברצף', 'red', 32)))
    card('s01_origin', 'מאיפה MAYDAY', body, 'מאיפה MAYDAY', 'מצרפתית, m’aider. מ-1927, אות המצוקה הבינלאומי בתעופה ובספנות.', bg='u18_bounty', shade=0.7)

def s02():
    sit = [('FIRE', 'שריפה'), ('SINKING', 'הצפה וטביעה'), ('COLLISION', 'התנגשות'), ('MOB', 'אדם בים'), ('ABANDON', 'נטישה'),
           ('PIRACY', 'פיראטים'), ('FLOODING', 'הצפה'), ('NO CONTROL', 'אובדן שליטה'), ('GROUNDING', 'שרטון')]
    body = top(chip('MAYDAY · עדיפות 1', 'red', 34)) + fill(tiles([(f'<span class="ltr">{e}</span>', h, 'red') for e, h in sit], 150, 34, 28, 3), 110)
    card('s02_mayday', 'מתי MAYDAY', body, 'מצוקה', 'סכנה מיידית לחיים או לכלי השייט, וצריך עזרה מיד. המפקד מחליט.', bg='u18_bounty', shade=0.6)

def s03():
    body = bottom(rows(('✓', 'סכנה מיידית וחמורה', 'green', 32), ('✓', 'והמפקד מחליט שדרושה עזרה', 'green', 32), ('✗', 'לא כל מי שמזהה סכנה', 'red', 32)))
    card('s03_q59', 'מי מפעיל', body, 'תשובה ג', 'סכנה מיידית וחמורה, והמפקד מחליט שדרושה עזרה מיידית.',
         ('שאלה מהמאגר · 59', 'מתי יופעל נוהל מצוקה מתחנת כלי שייט?',
          ['רק על דעת המפקד', 'כל מי שמזהה סכנה מיידית', 'סכנה מיידית וחמורה, והמפקד מחליט', 'רק א ו-ג נכונות'], 2), bg='u18_bounty', shade=0.15)

def s04():
    body = fill(rows(('🔇', 'דממת רדיו בערוץ 16', 'red', 32), ('M', 'כל הודעה מתחילה ב-MAYDAY', 'red', 32),
                     ('⚓', 'התחנה המפקחת מנהלת ומסיימת', 'sky', 32), ('🤝', 'חובה לעזור', 'green', 32)))
    card('s04_rules', 'מרגע הקריאה', body, 'עדיפות מוחלטת', 'בערוץ 16 רק המצוקה. התחנה המפקחת מנהלת, ורק היא מסיימת.', bg='u14_coast_station', shade=0.6)

def s05():
    st = [('MAYDAY ×3', 'red'), ('THIS IS · NAME ×3 · MMSI', 'sky'), ('MAYDAY · NAME', 'red'), ('POSITION · LAT first', 'amber'),
          ('NATURE · ASSISTANCE', 'sky'), ('PERSONS ON BOARD', 'sky'), ('OVER', 'green')]
    lst = ''.join(f'<div class="ltr text-left rounded-2xl {T.TONES[t][2]} px-6 py-2 text-white font-extrabold text-[36px]">{s}</div>' for s, t in st)
    body = top(chip('קודם DSC · כפתור המצוקה', 'red', 30)) + fill(lst, 100)
    card('s05_call', 'קריאת MAYDAY', body, 'הקריאה בערוץ 16', 'קודם DSC, אחר כך בקול. במיקום, קו רוחב קודם.', bg='u18_vhf16', shade=0.8)

DCQ = ['פנייה לכולם להפסיק ולהקשיב', 'MAYDAY THIS IS וכל הפרטים', 'תחנות החוף מאשרות ראשונות', 'כל התשובות נכונות']

def dc_body(extra=''):
    return extra + bottom(rows(('א', 'כולם מפסיקים ומקשיבים', 'green', 30), ('ב', 'MAYDAY · THIS IS · פרטים', 'green', 30), ('ג', 'תחנת החוף מאשרת ומפקחת', 'green', 30)))

def s06():
    card('s06_q94', 'קריאת מצוקה', dc_body(), 'כל התשובות', 'כולם מקשיבים, משדרים את כל הפרטים, ותחנת החוף לוקחת פיקוח.',
         ('שאלה מהמאגר · 94', 'מהי קריאת מצוקה (DISTRESS CALL)?', DCQ, 3), bg='u18_vhf16', shade=0.2)

def s07():
    card('s07_q173', 'קריאת מצוקה', dc_body(SAME), 'כל התשובות', 'אותה שאלה, אותה תשובה.',
         ('שאלה מהמאגר · 173', 'מהו "קריאת מצוקה" DISTRESS CALL?',
          ['ערוץ 16, לכולם, להפסיק ולהקשיב', '3 פעמים MAYDAY, THIS IS וזיהוי', 'תחנות חוף מאשרות ראשונות', 'כל התשובות נכונות'], 3), bg='u18_vhf16', shade=0.2)

def s08():
    ln = lambda s, c='text-white': f'<div class="ltr text-left {c} text-[30px] font-semibold">{s}</div>'
    call = glass('<div class="p-6 space-y-2">' + ln('MAYDAY ×3 THIS IS SONDRA ×3') + ln('MMSI 356004420 · MAYDAY SONDRA')
                 + '<div class="rounded-2xl ring-4 ring-rose-400 bg-rose-500/25 px-3 py-2">' + ln('35°44′ E · 32°59′ N', 'text-rose-200')
                 + '<div class="text-rose-200 text-[28px] font-bold">✗ קו אורך לפני קו רוחב</div></div>'
                 + ln('DANGER OF SINKING · 8 PERSONS') + ln('OVER') + '</div>')
    card('s08_q113', 'מצא את השגיאה', fill(call), 'תשובה א', 'קו רוחב קודם. SONDRA מסרה קודם את קו האורך.',
         ('שאלה מהמאגר · 113', 'בקריאת המצוקה של SONDRA יש שגיאה. מה נכון?',
          ['במיקום, קודם קו הרוחב', 'השגיאה היחידה: מספר ה-MMSI', 'הסיומת צריכה להיות OUT', 'חובה לציין את הזמן'], 0), bg='u18_vhf16', shade=0.8)

def s09():
    body = fill(tiles([('לכולם', 'לא רק לנמל חיפה', 'green'), ('<span class="ltr">COLLISION</span>', 'סוג המצוקה ב-DSC', 'green'),
                       ('3 + 3 = 6', 'נוסעים וצוות', 'green'), ('9 ✗', 'וגם לא רק 3', 'red')], 210, 44))
    card('s09_q132', 'יכטה MARNI', body, 'תשובה ג', 'לכולם, COLLISION ב-DSC, ושישה אנשים על הסיפון.',
         ('שאלה מהמאגר · 132', 'MARNI על עוגן מול חיפה. התנגשות, סכנת טביעה. 3 נוסעים ו-3 צוות.',
          ['לנמל חיפה · SINKING · 9 אנשים', 'לנמל חיפה · COLLISION · 9 אנשים', 'לכולם · COLLISION · 6 אנשים', 'לכולם · COLLISION · 3 אנשי צוות'], 2),
         bg='u16_ships', shade=0.75)

def s10():
    body = fill(tiles([('כל מי ששומע', 'חייב להגיב · ✓', 'green'), ('רק מי שיכול', 'לעזור · ✗', 'red'), ('רק מי שקרוב', '✗', 'red'), ('רק גופי הצלה', '✗', 'red')], 210, 42))
    card('s10_q193', 'מי עונה', body, 'תשובה א', 'כל מי ששומע את הקריאה חייב להגיב.',
         ('שאלה מהמאגר · 193', 'מי צריך להשיב מיד לקריאה "MAYDAY"?',
          ['כל מי ששומע את הקריאה', 'כל מי שמסוגל לעזור מיידית', 'כל מי שנמצא בקרבת הספינה', 'כל מי שעוסק בהצלה'], 0), bg='u16_ships', shade=0.75)

def s11():
    body = f'<div class="absolute top-6 inset-x-6">{rows(("M", "מצוקה, לא דחיפות", "red", 32), ("📍", "המקום והזמן שנראה לאחרונה", "amber", 32))}</div>'
    card('s11_q95', 'אדם בים', body, 'תשובה א', 'מצוקה. בהודעה, המקום והזמן שבהם נראה לאחרונה.',
         ('שאלה מהמאגר · 95', 'אדם נפל לים מכלי שייט ואבד קשר עין איתו:',
          ['מצוקה · מקום וזמן אחרונים', 'דחיפות · לדווח על גופים במים', 'להטיל לים כל אמצעי ציפה', 'רק DSC בערוץ 70'], 0), bg='u18_mob', pos='35% 50%', shade=0.1)

def s12():
    step = lambda n, s, tone: f'<div class="flex items-center gap-5 rounded-2xl {T.TONES[tone][2]} px-6 py-4"><div class="text-white font-extrabold text-[44px]">{n}</div><div class="text-white font-bold text-[36px]">{s}</div></div>'
    body = fill(step(1, 'כל מי שקלט מתייצב', 'sky') + step(2, 'מיקום וזמן הגעה משוער', 'sky') + step(3, 'שולחים כלי שייט לחילוץ', 'sky')
                + step(4, 'אפשר להעביר פיקוח', 'amber') + step(5, 'פינוי זהיר, ואז סיום', 'green'))
    card('s12_control', 'אחרי הקריאה', body, 'ניהול המצוקה', 'התחנה המפקחת מתכננת את החילוץ, ובסוף מסיימת את המצוקה.', bg='u14_coast_station', shade=0.6)

def s13():
    card('s13_codes', 'קודי מצוקה', codes(), 'ארבעה קודים', 'שניים להשתקה, אחד לפינוי זהיר, ואחד לסיום. מצרפתית.', bg='u14_coast_station', shade=0.75)

def s14():
    card('s14_q98', 'המפקח משתיק', codes('SEELONCE MAYDAY'), 'תשובה ג', 'SEELONCE MAYDAY. רק התחנה המפקחת.',
         ('שאלה מהמאגר · 98', 'התחנה המנהלת את המצוקה רוצה להפסיק הפרעה בערוץ 16:',
          ['EMERGENCY STOP SENDING', 'SEELONCE DISTRESS', 'SEELONCE MAYDAY', 'RESCUE OPERATION KEEP SILENT'], 2), bg='u14_coast_station', shade=0.75)

def s15():
    card('s15_q99', 'תחנה אחרת משתיקה', codes('SEELONCE DISTRESS'), 'תשובה ג', 'SEELONCE DISTRESS. תחנה שאינה המפקחת.',
         ('שאלה מהמאגר · 99', 'תחנה שאינה מפקחת, באזור המצוקה, רוצה להפסיק הפרעה:',
          ['PLEASE LISTEN MAYDAY', 'SWITCH TO OTHER CHANNEL', 'SEELONCE DISTRESS', 'CLOSE TRANSMITTER'], 2), bg='u14_coast_station', shade=0.75)

def s16():
    card('s16_q100', 'לקראת סיום', codes('PRUDONCE'), 'תשובה ב', 'PRUDONCE. המצוקה עוד לא נגמרה, מפנים בזהירות.',
         ('שאלה מהמאגר · 100', 'המצוקה קרובה לסיום, ואין צורך רצוף בערוץ 16:',
          ['BACK TO NORMAL', 'PRUDONCE', 'KEEP LISTENING', 'EASE THE TRAFFIC'], 1), bg='u14_coast_station', shade=0.75)

def s17():
    card('s17_q61', 'סוף המצוקה', codes('SEELONCE FEENEE'), 'תשובה א', 'SEELONCE FEENEE. ערוץ 16 חוזר לשגרה.',
         ('שאלה מהמאגר · 61', 'איך תודיע התחנה המפקחת שהמצוקה הסתיימה?',
          ['SEELONCE FEENEE', 'RESUME NORMAL TRAFFIC', 'PRUDONCE', 'FINISH OF SILENCE PERIOD'], 0), bg='u14_coast_station', shade=0.75)

def s18():
    card('s18_q115', 'סוף המצוקה', codes('SEELONCE FEENEE', SAME), 'תשובה ב', 'אותה שאלה, התשובות בסדר אחר.',
         ('שאלה מהמאגר · 115', 'המצוקה הסתיימה. משחררים את ערוץ 16 לשגרה:',
          ['PRUDONCE', 'SEELONCE FEENEE', 'RESUME NORMAL TRAFFIC', 'FINISH OF SILENCE PERIOD'], 1), bg='u14_coast_station', shade=0.75)

def s19():
    body = top(chip('MAYDAY RELAY · ממסר מצוקה', 'red', 32)) + bottom(rows(('📡', 'הספינה במצוקה לא יכולה לשדר', 'amber', 30), ('✂', 'שמעת קריאה שנקטעה', 'amber', 30),
                                                                        ('70', 'התראה בערוץ 70 או SART, בלי קריאה', 'amber', 30), ('?', 'אף תחנה לא אישרה', 'amber', 30)))
    card('s19_relay', 'ממסר מצוקה', body, 'ממסר מצוקה', 'מעבירים לתחנת חוף, והיא משדרת לכולם. ב-DSC: DISTRESS RELAY.', bg='u14_coast_station', shade=0.5)

def s20():
    body = fill(rows(('1', 'DSC · כיבוי והדלקה · ביטול לכל התחנות', 'sky', 30), ('2', 'SART · כיבוי · ביטול לכל התחנות', 'amber', 30),
                     ('3', 'EPIRB · כיבוי, ניתוק סוללה · לתחנת החוף', 'red', 30), gap=5)
                + glass('<div class="p-5 text-rose-300 text-[36px] font-extrabold text-center">MAYDAY לשווא · עבירה פלילית</div>', 'ring-2 ring-rose-400'))
    card('s20_cancel', 'שידור בטעות', body, 'ביטול מצוקה', 'כיבוי והודעת ביטול. MAYDAY לשווא, בכוונה, הוא עבירה פלילית חמורה.', bg='u16_ships', shade=0.7)

def s21():
    items = ['שם הסקיפר', 'צוות ונוסעים', 'אזרחות ודגל', 'מאיפה באנו', 'נמל בית', 'מהירות', 'קורס', 'מיקום']
    grid = '<div class="grid grid-cols-2 gap-3">' + ''.join(f'<div class="rounded-2xl bg-slate-900/85 ring-1 ring-white/15 px-5 py-3 text-white text-[32px] font-semibold">{s}</div>' for s in items) + '</div>'
    body = top(chip('דיווח לרדיו חיפה', 'sky', 32)) + fill(grid + '<div class="flex gap-4 justify-center pt-2">' + chip('50 מייל', 'amber', 34) + chip('ושוב ב-25 מייל', 'amber', 34) + '</div>', 100)
    card('s21_imot', 'כניסה לישראל', body, 'נוהל IMOT', 'כל כלי שייט שנכנס לישראל מדווח לרדיו חיפה. ב-50 מייל, ושוב ב-25.', bg='u14_chart_table', shade=0.6)

def s22():
    items = ['MAYDAY · סכנה מיידית, המפקד מחליט', 'קודם DSC, אחר כך ערוץ 16', 'מיקום · קו רוחב קודם', 'סופרים את כל מי שעל הסיפון',
             'כל מי ששומע · חייב להגיב', 'SEELONCE MAYDAY / DISTRESS · השתקה', 'PRUDONCE · לקראת סיום', 'SEELONCE FEENEE · סוף']
    lst = ''.join(f'<div class="flex items-center gap-4 rounded-2xl bg-slate-800/80 px-5 py-2 text-white text-[32px]"><span class="w-4 h-4 rounded-full {"bg-emerald-400" if i < 5 else "bg-amber-400"} shrink-0"></span>{t}</div>' for i, t in enumerate(items))
    if MOBILE: T.vcard(os.path.join(VOUT, 's22_summary.png'), 'סיכום', T.vphoto('u18_bounty', '50% 45%') + vcredit('u18_bounty'), f'<div class="space-y-2">{lst}</div>')
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u18_bounty', focus=(0.5, 0.45)); credit(d, (0, 0, 1300, 1440), 'u18_bounty')
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 5 else C.ORANGE)
        text_r(d, 2380, y + 20, s, F(42, False), TEXT)
    save(im, 's22_summary')

# ---------- simulated radio exchanges (radio_sim.py) ----------
# (who, display text). 'me' = our yacht in Alex's voice, 'coast' = Haifa Radio. SAY() spells the procedure words for TTS.
SAY = lambda t: (t.replace('SEELONCE FEENEE', 'See-lonce Fee-nay').replace('SEELONCE', 'See-lonce').replace('MAYDAY', 'Mayday')
                 .replace('MMSI', 'M.M.S.I.').replace('UTC', 'U.T.C.').replace('IMOT', 'I-mot'))
SIMS_DEF = {
    's05_call': ('קריאת MAYDAY', 'קודם DSC. אחר כך בקול: מי, מיקום, מה קרה, איזו עזרה, וכמה אנשים.', [
        ('me', 'MAYDAY, MAYDAY, MAYDAY. This is sailing yacht Lilach, Lilach, Lilach. MMSI four two eight one two three four five six. MAYDAY Lilach. Position three two degrees four five minutes north, zero three four degrees five two minutes east. On fire. Require immediate assistance. Four persons on board. Over.'),
        ('coast', 'MAYDAY. Lilach, Lilach, Lilach. This is Haifa Radio, Haifa Radio, Haifa Radio. Received MAYDAY. Over.')]),
    's13_codes': ('SEELONCE MAYDAY', 'התחנה המפקחת משתיקה את כל מי שמפריע בערוץ 16.', [
        ('coast', 'MAYDAY. All stations, all stations, all stations. This is Haifa Radio. SEELONCE MAYDAY. Out.')]),
    's18_q115': ('SEELONCE FEENEE', 'התחנה המפקחת מודיעה שהמצוקה של Lilach הסתיימה.', [
        ('coast', 'MAYDAY. All stations, all stations, all stations. This is Haifa Radio, Haifa Radio, Haifa Radio. Time one six three zero UTC. Sailing yacht Lilach, MMSI four two eight one two three four five six. SEELONCE FEENEE. Out.')]),
    's19_relay': ('MAYDAY RELAY', 'Lilach שמעה קריאה שנקטעה, ומעבירה אותה לרדיו חיפה.', [
        ('me', 'MAYDAY RELAY, MAYDAY RELAY, MAYDAY RELAY. Haifa Radio, Haifa Radio, Haifa Radio. This is sailing yacht Lilach, Lilach, Lilach. Following received on channel one six at one four zero five UTC. MAYDAY fishing vessel Dalia. Position three two degrees five zero minutes north, zero three four degrees four eight minutes east. Taking water. Transmission interrupted. Over.'),
        ('coast', 'Lilach, this is Haifa Radio. MAYDAY RELAY received. Haifa Radio will relay to all stations. Out.')]),
    's21_imot': ('דיווח IMOT', 'דיווח לרדיו חיפה בחמישים מייל מהחוף.', [
        ('me', 'Haifa Radio, Haifa Radio, Haifa Radio. This is sailing yacht Lilach, Lilach, Lilach. IMOT report. Skipper Alex Argov. Two crew, three passengers. Israeli citizens, Israeli flag. From Larnaca, home port Herzliya. Speed six knots, course one five zero. Position three three degrees three three minutes north, zero three four degrees three zero minutes east. Over.'),
        ('coast', 'Lilach, this is Haifa Radio. IMOT report received. Report again at two five miles. Out.')]),
}
SIMS = {sid: [(who, SAY(t)) for who, t in lines] for sid, (_, _, lines) in SIMS_DEF.items()}

def bubble(who, text, size=31):
    me = who == 'me'
    lab = 'S/Y LILACH' if me else 'HAIFA RADIO'
    return (f'<div class="flex {"justify-start" if me else "justify-end"}" dir="ltr"><div class="max-w-[92%] rounded-3xl px-5 py-3 {"bg-sky-700/90" if me else "bg-emerald-800/90"} ring-1 ring-white/20">'
            f'<div class="text-[24px] font-extrabold {"text-sky-200" if me else "text-emerald-200"}">📻 {lab}</div>'
            f'<div class="text-white text-[{size}px] leading-snug">{text}</div></div></div>')

def sim_cards():
    for sid, (title, gloss, lines) in SIMS_DEF.items():
        size = 26 if sum(len(t) for _, t in lines) > 380 else 31
        body = (top(chip('🔊 סימולציה בקשר', 'amber', 30))
                + f'<div class="absolute inset-x-6 bottom-6 top-[110px] flex flex-col justify-center gap-4">' + ''.join(bubble(w, t, size) for w, t in lines) + '</div>')
        card(sid + '_sim', 'סימולציה בקשר', body, title, gloss, bg='u17_vhf_call', shade=0.82)

ALL = [s01, s01o, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, sim_cards]

def vsheet():
    fs = sorted(f for f in os.listdir(VOUT) if f.startswith('s') and f.endswith('.png'))
    c = 7; sh = Image.new('RGB', (c * 300, ((len(fs) + c - 1) // c) * 533))
    for i, f in enumerate(fs):
        sh.paste(Image.open(os.path.join(VOUT, f)).convert('RGB').resize((300, 533)), ((i % c) * 300, (i // c) * 533))
    sh.save(os.path.join(VOUT, '_sheet.png'))

if __name__ == '__main__':
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:                              # OneDrive can lock a freshly written PNG
                    import time; time.sleep(2)
    U6.sheet.__globals__.__setitem__('C', C); U6.sheet()
    if MOBILE: vsheet()
