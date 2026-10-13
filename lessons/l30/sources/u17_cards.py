"""Lesson 17 (l30): נהלי קשר. Mobile-first: every card renders a native 9:16 card (_v/, visual built at 1080 wide) and the 16:9 card."""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U6 = _load('u06', 'u06_cards.py'); U8 = _load('u08', 'u08_cards.py'); U12 = _load('u12', 'u12_cards.py')
import twcard as T
from twcard import chip, glass, tile, row
from PIL import Image
NAME = 'נהלי קשר'
C.OUT = os.path.join(HERE, '..', 'cards', NAME); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · נהלי קשר'
F, text_c, text_r, dot, base, left_panel, right_block, save, RC = C.F, C.text_c, C.text_r, C.dot, C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, GREEN, GREEN_L, BLUE_L, PANEL = C.TEXT, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL
photo = U8.photo
X0, Y0, X1, Y1 = [int(v) for v in U5.inner()]; PW, PH = X1 - X0, Y1 - Y0
VOUT = os.path.join(C.OUT, '_v'); os.makedirs(VOUT, exist_ok=True); VSUB = 'שיעור 17 · נהלי קשר'

def card(sid, caption, body, title, text, q=None, bg=None, pos='center', shade=0.0):
    """Same body HTML rendered twice: 1180x1060 for the wide card, 1080 x VTOP for the phone card."""
    vp = T.panel('v_' + sid, body, T.VW, T.VTOP, bg, pos, shade)
    T.vcard(os.path.join(VOUT, sid + '.png'), caption, T.vimg(vp), T.vbottom(VSUB, title, text, q))
    im, d = base(); left_panel(d, caption)
    pp = T.panel(sid, body, PW, PH, bg, pos, shade); p = Image.open(pp).convert('RGBA'); im.paste(p, (X0, Y0), p)
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

def bar(n, code, he, tone, w):
    b = T.TONES[tone][2]
    return (f'<div class="h-[150px] rounded-3xl {b} flex items-center gap-6 px-8" style="width:{w}%"><div class="text-white/90 font-extrabold text-[70px]">{n}</div>'
            f'<div><div class="ltr text-white font-extrabold text-[54px] leading-none text-right">{code}</div><div class="text-white text-[34px]">{he}</div></div></div>')

SAME = top(chip('אותה שאלה · נוסח אחר', 'amber', 30))

# ---------- cards ----------
def s01():
    items = ['סדר עדיפויות', 'מפקח על הקשר', 'ערוץ 16 וקריאה לתחנה', 'PAN PAN ו-SECURITE']
    T.vcard(os.path.join(VOUT, 's01_intro.png'), 'שיעור 17', T.vphoto('u17_vhf_call', '50% 45%'), T.vbottom('קורס ניווט חופי ומכשירים', 'נהלי קשר', '<br>'.join(items)))
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u17_vhf_call', focus=(0.5, 0.45))
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 17', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'נהלי קשר', F(118), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(items):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    body = fill(bar(1, 'MAYDAY', 'מצוקה · סכנה לחיים', 'red', 100) + bar(2, 'PAN PAN', 'דחיפות · בעיה דחופה', 'amber', 88) + bar(3, 'SECURITE', 'בטיחות · אזהרות', 'sky', 76)
                + '<div class="text-white/80 text-[30px] pt-2">אחריהן: חיפוש והצלה · ניווט ותחזיות · כל השאר</div>')
    card('s02_priorities', 'סדר עדיפויות', body, 'מצוקה קודמת לכל', 'MAYDAY ראשונה, PAN PAN שנייה, SECURITE שלישית.')

def s03():
    r = lambda a, b: (f'<div class="flex items-center justify-between gap-3 rounded-2xl bg-slate-900/85 ring-1 ring-white/15 px-6 py-5">'
                      f'<div class="text-white text-[36px] font-semibold">{a}</div><div class="text-emerald-300 text-[36px] font-extrabold">{b}</div></div>')
    body = fill(r('חוף ↔ כלי שייט', 'תחנת החוף') + r('כלי שייט ↔ כלי שייט', 'מי שנקרא') + r('מצוקה', 'כלי השייט במצוקה')
                + '<div class="flex gap-3 justify-center pt-2">' + chip('ערוץ', 'sky', 28) + chip('הספק', 'sky', 28) + chip('הפסקה וחידוש', 'sky', 28) + '</div>')
    card('s03_control', 'מי מנהל את השיחה', body, 'מפקח על הקשר', 'המפקח קובע ערוץ, הספק, ומתי מפסיקים. בין חוף לספינה, תחנת החוף.',
         bg='u14_coast_station', shade=0.55)

def s04():
    body = fill(tile('16', 'קריאה ומצוקה', 'red', 'h-[230px]', 110, 34) + rows(('👂', 'האזנה כל הזמן', 'green', 30), ('1′', 'שיחה שגרתית · עד דקה', 'amber', 30), ('10″', 'שידור ניסיון · עד 10 שניות', 'sky', 30)))
    card('s04_ch16', 'ערוץ 16', body, 'ערוץ 16', 'מאזינים תמיד. קוראים, ועוברים לערוץ עבודה. ניסיון עד 10 שניות.', bg='u17_vhf_call', shade=0.6)

def s05():
    step = lambda n, s, tone: f'<div class="flex items-center gap-5 rounded-2xl {T.TONES[tone][2]} px-6 py-4"><div class="text-white font-extrabold text-[46px]">{n}</div><div class="text-white font-bold text-[38px]">{s}</div></div>'
    body = fill(step(1, 'קריאה · למי אני קורא', 'sky') + step(2, 'הזדהות · מי אני', 'sky') + step(3, 'סיבת הקריאה', 'sky') + step(4, 'סיום', 'green')
                + glass('<div class="p-4 text-amber-300 text-[34px] font-bold text-center">אין מענה? מחכים 2 דקות וקוראים שוב</div>'))
    card('s05_calling', 'מבנה קריאה', body, 'ארבעה חלקים', 'קריאה, הזדהות, סיבה וסיום. בערוץ 16, אם לא קוראים ב-DSC.')

def s06():
    body = fill(tiles([('2 דקות', 'מחכים, ואז שוב · ✓', 'green'), ('30 שניות', 'קצר מדי · ✗', 'red'), ('ערוץ עבודה', 'לא מתפרצים · ✗', 'red'), ('לא עובדת?', 'לא מסיקים · ✗', 'red')], 220, 46))
    card('s06_q67', 'אין מענה', body, 'תשובה ב', 'מחכים לפחות שתי דקות, מוודאים שהערוץ פנוי, וקוראים שוב.',
         ('שאלה מהמאגר · 67', 'קראת לתחנת חוף ואין מענה. מה תעשה?',
          ['ממתין 30 שניות וקורא שוב', 'ממתין לפחות 2 דקות וקורא שוב', 'מתפרץ לערוץ העבודה', 'אין תשובה, התחנה לא עובדת'], 1), bg='u14_coast_station', shade=0.7)

CHK = [('🔋', 'מצברים', 'green', 28), ('DSC', 'פעולת ה-DSC', 'green', 28), ('10″', 'שידור ניסיון וקליטה', 'green', 28), ('📅', 'תפוגת סוללות במשואות', 'green', 28)]

def s07():
    body = top(chip('רושמים ביומן הספינה', 'amber', 30)) + bottom(rows(*CHK))
    card('s07_checks', 'בדיקות ציוד', body, 'בודקים ורושמים', 'מצברים, DSC, שידור ניסיון וקליטה, ותפוגת סוללות. ויומן בדיקות, אם יש.', bg='u17_logbook', shade=0.1)

CHQ = ['מצברים, DSC, ניסיון, קליטה ותפוגה', 'לפי יומן בדיקות מיוחד', 'רק בדיקת כשירות פעם בשנתיים', 'א׳ ו-ב׳ אם ישנו']

def chk_body(extra=''):
    return extra + bottom(rows(('א', 'הבדיקות הקבועות', 'green', 30), ('ב', 'יומן בדיקות, אם יש', 'green', 30), ('✗', 'לא מחכים שנתיים', 'red', 30)))

def s08():
    card('s08_q101', 'מה בודקים', chk_body(), 'א׳ ו-ב׳', 'הבדיקות הקבועות, ויומן הבדיקות המיוחד אם יש כזה.',
         ('שאלה מהמאגר · 101', 'אילו בדיקות יש לבצע בציוד הקשר ולרשום ביומן?', CHQ, 3), bg='u17_logbook', shade=0.15)

def s09():
    card('s09_q136', 'מה בודקים', chk_body(SAME), 'א׳ ו-ב׳', 'אותה שאלה, אותה תשובה.',
         ('שאלה מהמאגר · 136', 'אילו בדיקות יש לבצע בציוד הקשר של ספינה?', CHQ, 3), bg='u17_logbook', shade=0.15)

def s10():
    col = lambda head, sub, items, tone: glass(f'<div class="p-6 space-y-3"><div class="ltr text-right {T.TONES[tone][1]} font-extrabold text-[44px]">{head}</div>'
                                               f'<div class="text-white/80 text-[28px]">{sub}</div>' + ''.join(f'<div class="text-white text-[32px]">• {s}</div>' for s in items) + '</div>', f'ring-2 {T.TONES[tone][0]}')
    body = fill(col('TRANSIT REPORT · TR', 'כלי שייט ← תחנת חוף', ['פרטי המסע', 'כניסה, יציאה או מעבר'], 'sky')
                + col('TRAFFIC LIST', 'תחנת חוף ← כולם · ערוץ 16', ['רשימת ספינות עם הודעות', 'שמעת את שמך? צור קשר'], 'amber'))
    card('s10_traffic', 'הודעות שגרה', body, 'TR ו-Traffic List', 'TR: אתה מדווח לתחנה. Traffic List: התחנה מודיעה שיש לך הודעה.', bg='u14_coast_station', shade=0.65)

def s11():
    body = top(chip('PAN PAN · עדיפות 2', 'amber', 34)) + bottom(rows(('+', 'MEDICO · עזרה רפואית', 'amber', 30), ('⛓', 'בקשת גרירה', 'amber', 30), ('⚠', 'אובדן יכולת תמרון', 'amber', 30))
                                                               + '<div class="flex justify-center pt-3">' + chip('קריאה ב-16 · הודעה בערוץ עבודה', 'sky', 26) + '</div>')
    card('s11_panpan', 'דחיפות', body, 'PAN PAN', 'בעיה דחופה בלי סכנה מיידית לחיים. ב-DSC: התראת URGENCY.', bg='u17_tow', shade=0.1)

def s12():
    body = fill(tiles([('MAYDAY', '1 · מצוקה', 'red'), ('PAN PAN', '2 · דחיפות · ✓', 'green'), ('SECURITE', '3 · בטיחות', 'sky'), ('אדם בים', 'נעלם מהעין · מצוקה', 'red')], 210, 44))
    card('s12_q70', 'PAN PAN', body, 'תשובה ב', 'PAN PAN מקדים הודעת דחיפות, בעדיפות שנייה.',
         ('שאלה מהמאגר · 70', 'מה פירוש הקריאה PAN PAN שלוש פעמים?',
          ['הודעת בטיחות · עדיפות שנייה', 'הודעת דחיפות · עדיפות שנייה', 'הודעת מצוקה · עדיפות ראשונה', 'הודעת דחיפות · אדם נפל לים'], 1), bg='u17_tow', shade=0.75)

def s13():
    body = bottom(rows(('א', 'עזרה רפואית · חילוץ פצועים', 'green', 30), ('ב', 'הספינה לא כשירה · גרירה', 'green', 30), ('ג', 'חירום שאינו מצוקה', 'green', 30)))
    card('s13_q60', 'מתי דחיפות', body, 'כל התשובות', 'רפואה, גרירה, וכל חירום שאינו מצוקה.',
         ('שאלה מהמאגר · 60', 'מהם המקרים שבהם יש לקיים נוהל דחיפות?',
          ['ייעוץ או עזרה רפואית, חילוץ פצועים', 'הספינה לא כשירה ודרושה גרירה', 'חירום שאינו מצוקה, אפשר לפנות את 16', 'כל התשובות נכונות'], 3), bg='u17_tow', shade=0.1)

def s14():
    body = fill(tiles([('הצלת חיים', 'זה MAYDAY · ✗', 'red'), ('EPIRB', 'לא קשור · ✗', 'red'), ('סערה', 'זה SECURITE · ✗', 'red'), ('אף תשובה', 'נכונה · ✓', 'green')], 210, 44))
    card('s14_q73', 'מה לא דחיפות', body, 'אף תשובה', 'הצלת חיים היא מצוקה, ומזג אוויר קיצוני הוא בטיחות.',
         ('שאלה מהמאגר · 73', 'לאיזה סוגי אירועים משתמשים ברמת "דחיפות"?',
          ['הודעה הקשורה להצלת חיים', 'לכל בעלי EPIRB כשנדרשת עזרה רפואית', 'תנאי מזג אוויר קיצוניים', 'אף תשובה לא נכונה'], 3), bg='u17_tow', shade=0.75)

def s15():
    body = top(chip('MEDICO · דחיפות', 'amber', 34)) + bottom(rows(('1', 'מין וגיל החולה', 'sky', 30), ('2', 'חום הגוף ודופק', 'sky', 30), ('3', 'תופעות וטיפול', 'sky', 30))
                                                             + '<div class="flex justify-center pt-3">' + chip('קריאה ב-16 · ממשיכים בערוץ אחר', 'green', 26) + '</div>')
    card('s15_q96', 'הודעת MEDICO', body, 'תשובה א', 'דחיפות. מין, גיל, חום, דופק, תופעות וטיפול.',
         ('שאלה מהמאגר · 96', 'הודעה שמקודמת במילה MEDICO:',
          ['דחיפות: מין, גיל, חום, דופק, תופעות', 'מצוקה: לחץ דם, חום, כאב, היסטוריה', 'מצוקה, רק אם המפקד חולה', 'רק בקוד INTERCO'], 0), bg='u17_vhf_call', shade=0.65)

def s16():
    body = top(chip('SECURITE · עדיפות 3', 'sky', 34)) + bottom(rows(('⚓', 'אזהרות ניווט', 'sky', 30), ('☁', 'אזהרות מזג אוויר', 'sky', 30), ('🕑', 'שעות קבועות · גם NAVTEX', 'sky', 30)))
    card('s16_securite', 'בטיחות', body, 'SECURITE', 'אזהרות ניווט ומזג אוויר. קריאה ב-16, הודעה בערוץ עבודה.', bg='u14_bridge', shade=0.2)

def s17():
    body = bottom(rows(('א', 'קצרה מדקה · אפשר ב-16', 'green', 30), ('ב', 'בטיחות · עוברים לערוץ עבודה', 'green', 30), ('ג', 'שעות קבועות · גם NAVTEX', 'green', 30)))
    card('s17_q97', 'הודעות SECURITE', body, 'כל התשובות', 'קצרות אפשר ב-16, ארוכות בערוץ עבודה, וחלקן בשעות קבועות וב-NAVTEX.',
         ('שאלה מהמאגר · 97', 'הודעות המקודמות בקריאה SECURITE שלוש פעמים:',
          ['אפשר על 16 אם קצרות מדקה', 'בטיחות, בערוץ עבודה אחרי הכרזה', 'בשעות קבועות, וגם ב-NAVTEX', 'כל התשובות נכונות'], 3), bg='u14_bridge', shade=0.2)

def s18():
    body = fill(tiles([('רפואה', 'זה PAN PAN · ✗', 'red'), ('גרירה', 'זה PAN PAN · ✗', 'red'), ('חירום', 'זה PAN PAN · ✗', 'red'), ('SECURITE', 'ניווט ומזג אוויר', 'green')], 210, 44))
    card('s18_q123', 'מתי בטיחות', body, 'אף תשובה', 'כל המקרים ברשימה הם דחיפות. בטיחות זה אזהרות ניווט ומזג אוויר.',
         ('שאלה מהמאגר · 123', 'באיזה מקרים יש לקיים נוהל בטיחות?',
          ['ייעוץ או עזרה רפואית', 'הספינה לא כשירה, דרושה גרירה', 'חירום שאינו מצוקה', 'כל התשובות אינן נכונות'], 3), bg='u14_bridge', shade=0.75)

def s19():
    items = ['MAYDAY · עדיפות 1', 'PAN PAN · עדיפות 2', 'SECURITE · עדיפות 3', 'המפקח: ערוץ, הספק, הפסקה',
             '16 · מאזינים תמיד', 'שגרה ב-16 · עד דקה', 'אין מענה · 2 דקות', 'ניסיון 10″ · רושמים ביומן']
    lst = ''.join(f'<div class="flex items-center gap-4 rounded-2xl bg-slate-800/80 px-5 py-2 text-white text-[34px]"><span class="w-4 h-4 rounded-full {"bg-emerald-400" if i < 4 else "bg-amber-400"} shrink-0"></span>{t}</div>' for i, t in enumerate(items))
    T.vcard(os.path.join(VOUT, 's19_summary.png'), 'סיכום', T.vphoto('u17_vhf_call', '50% 45%'), f'<div class="space-y-2">{lst}</div>')
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u17_vhf_call', focus=(0.5, 0.45))
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 4 else C.ORANGE)
        text_r(d, 2380, y + 20, s, F(46, False), TEXT)
    save(im, 's19_summary')

# ---------- simulated radio exchanges (radio_sim.py) ----------
# (who, display text, optional TTS text). 'me' = our yacht in Alex's voice, 'coast' = Haifa Radio.
SAY = lambda t: t.replace('SECURITE', 'Say-cure-ee-tay').replace('PAN PAN', 'Pahn Pahn').replace('MEDICO', 'Med-ee-co').replace('E T A', 'E.T.A.')
SIMS_DEF = {
    's05_calling': ('קריאה לתחנת חוף', 'קריאה, הזדהות, סיבה. התחנה מעבירה לערוץ עבודה, וסוגרים ב-OUT.', [
        ('me', 'Haifa Radio, Haifa Radio, Haifa Radio. This is sailing yacht Lilach, Lilach, Lilach. Request a link call. Over.'),
        ('coast', 'Lilach, this is Haifa Radio. Switch to channel two six. Over.'),
        ('me', 'Channel two six. Lilach. Out.')]),
    's10_traffic': ('דיווח מעבר · TR', 'כלי השייט מדווח לתחנה את פרטי המסע שלו.', [
        ('me', 'Haifa Radio, this is sailing yacht Lilach. Transit report. Departed Herzliya marina, bound for Haifa. E T A one five zero zero. Four persons on board. Over.'),
        ('coast', 'Lilach, this is Haifa Radio. Transit report received. Good voyage. Out.')]),
    's11_panpan': ('קריאת PAN PAN', 'שלוש פעמים PAN PAN, למי, מי, מיקום, מה קרה ומה צריך.', [
        ('me', 'PAN PAN, PAN PAN, PAN PAN. All stations, all stations, all stations. This is sailing yacht Lilach, Lilach, Lilach. Position three two degrees four five minutes north, zero three four degrees five two minutes east. Engine failure, drifting towards the shore. Request tow. Over.'),
        ('coast', 'Lilach, this is Haifa Radio. PAN PAN received. Switch to channel two four. Over.')]),
    's15_q96': ('קריאת MEDICO', 'מין, גיל, תופעות, חום ודופק. התחנה מעבירה לערוץ אחר, לרופא.', [
        ('me', 'PAN PAN, PAN PAN, PAN PAN. Haifa Radio, Haifa Radio, Haifa Radio. This is sailing yacht Lilach, Lilach, Lilach. MEDICO. Male, forty five years old. Strong chest pain for thirty minutes. Temperature thirty seven point two. Pulse one two zero. Request medical advice. Over.'),
        ('coast', 'Lilach, this is Haifa Radio. Switch to channel two six. A doctor will speak with you. Over.')]),
    's16_securite': ('הודעת SECURITE', 'ההכרזה בערוץ 16, וההודעה עצמה בערוץ עבודה.', [
        ('coast', 'SECURITE, SECURITE, SECURITE. All stations, all stations, all stations. This is Haifa Radio, Haifa Radio, Haifa Radio. Navigational warning. Listen on channel two six. Out.'),
        ('coast', 'SECURITE. This is Haifa Radio. Floating container reported in position three two degrees five zero minutes north, zero three four degrees five zero minutes east. Vessels keep a sharp lookout. Out.')]),
}
SIMS = {sid: [(who, SAY(t)) for who, t in lines] for sid, (_, _, lines) in SIMS_DEF.items()}

def bubble(who, text):
    me = who == 'me'
    lab = 'S/Y LILACH' if me else 'HAIFA RADIO'
    return (f'<div class="flex {"justify-start" if me else "justify-end"}" dir="ltr"><div class="max-w-[90%] rounded-3xl px-5 py-3 {"bg-sky-700/90" if me else "bg-emerald-800/90"} ring-1 ring-white/20">'
            f'<div class="text-[24px] font-extrabold {"text-sky-200" if me else "text-emerald-200"}">📻 {lab}</div>'
            f'<div class="text-white text-[31px] leading-snug">{text}</div></div></div>')

def sim_cards():
    for sid, (title, gloss, lines) in SIMS_DEF.items():
        body = (top(chip('🔊 סימולציה בקשר', 'amber', 30))
                + f'<div class="absolute inset-x-6 bottom-6 top-[110px] flex flex-col justify-center gap-4">' + ''.join(bubble(w, t) for w, t in lines) + '</div>')
        card(sid + '_sim', 'סימולציה בקשר', body, title, gloss, bg='u17_vhf_call', shade=0.82)

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, sim_cards]

def vsheet():
    fs = sorted(f for f in os.listdir(VOUT) if f.startswith('s') and f.endswith('.png'))
    c = 7; sh = Image.new('RGB', (c * 300, ((len(fs) + c - 1) // c) * 533))
    for i, f in enumerate(fs):
        sh.paste(Image.open(os.path.join(VOUT, f)).convert('RGB').resize((300, 533)), ((i % c) * 300, (i // c) * 533))
    sh.save(os.path.join(VOUT, '_sheet.png'))

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:                              # OneDrive can lock a freshly written PNG
                    import time; time.sleep(2)
    U6.sheet.__globals__.__setitem__('C', C); U6.sheet(); vsheet()
