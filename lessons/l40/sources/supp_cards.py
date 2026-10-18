"""l40 lesson: השלמות למבחן GMDSS (the 7 exam questions the l30 radio lessons don't cover).
Same look as the l30 cards: Tailwind left panel (twcard.py) over a photo, PIL right block. Reuses l30 helpers and assets."""
import os, sys, importlib.util
L30 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'l30', 'sources'); sys.path.insert(0, L30)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(L30, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U8 = _load('u08', 'u08_cards.py'); U12 = _load('u12', 'u12_cards.py')
import twcard as T
from twcard import chip, glass, tile, row
from PIL import Image
NAME = 'השלמות למבחן GMDSS'
C.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cards', NAME); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'קורס GMDSS · השלמות למבחן'
F, text_c, text_r, dot, base, left_panel, right_block, save, RC = C.F, C.text_c, C.text_r, C.dot, C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, GREEN, GREEN_L, BLUE_L, PANEL = C.TEXT, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL
photo = U8.photo; credit = U12.credit
CR = {'u16_cospas': 'Image: NOAA · Public domain', 'u16_epirb_bracket': 'Photo: Marwan Mohamad · CC BY-SA 4.0',
      'u18_bounty': 'Photo: U.S. Coast Guard · Public domain'}
U12.CREDIT.update(CR)
X0, Y0, X1, Y1 = [int(v) for v in U5.inner()]; PW, PH = X1 - X0, Y1 - Y0

def card(sid, caption, body, title, text, q=None, bg=None, pos='center', shade=0.0):
    im, d = base(); left_panel(d, caption)
    p = Image.open(T.panel('l40s_' + sid, body, PW, PH, bg, pos, shade)).convert('RGBA'); im.paste(p, (X0, Y0), p)
    if bg in CR: credit(d, (X0, Y0, X1, Y1), bg)
    right_block(d, title, text, q); save(im, sid)

def at(x, y, html):
    return f'<div class="absolute" style="left:{x}px;top:{y}px">{html}</div>'

def bottom(html):
    return f'<div class="absolute bottom-6 inset-x-6">{html}</div>'

def grid(items, cols=2, top=24, h=230, hs=50, ss=26):
    t = ''.join(tile(n, s, tone, f'h-[{h}px]', hs, ss) for n, s, tone in items)
    return f'<div class="absolute inset-x-6 bottom-6 grid grid-cols-{cols} gap-4 content-center" style="top:{top}px">{t}</div>'

def rows(*rs, gap=3):
    return glass(f'<div class="p-6 space-y-{gap}">' + ''.join(row(*r) for r in rs) + '</div>')

def flow(steps, size=34):
    bg = {'red': 'bg-rose-500/90', 'sky': 'bg-sky-500/90', 'amber': 'bg-amber-500/90', 'green': 'bg-emerald-500/90', 'slate': 'bg-slate-600/90'}
    out = []
    for i, (s, t) in enumerate(steps):
        if i: out.append('<div class="text-white text-[46px] leading-none text-center">↓</div>')
        out.append(f'<div class="rounded-2xl {bg[t]} px-6 py-4 text-white font-extrabold text-center" style="font-size:{size * T.S:.0f}px">{s}</div>')
    return '<div class="flex flex-col gap-2">' + ''.join(out) + '</div>'

def centered(html, top=24):
    return f'<div class="absolute inset-x-8 bottom-8 flex flex-col justify-center" style="top:{top}px">{html}</div>'

EXAM = 'שאלה מהמבחן · {}'

# ---------- cards ----------
def s01():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u14_coast_station', focus=(0.5, 0.5))
    text_c(d, RC, 380, 'קורס GMDSS · מבחן משרד התקשורת', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'השלמות למבחן', F(124), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['הדרישות התפקודיות', 'On-Scene · במקום האירוע', 'COSPAS-SARSAT · מי מוצא את המשואה', 'אתרעת שווא · SART · Traffic List']):
        text_c(d, RC, 810 + i * 84, s, F(52, False), TEXT)
    save(im, 's01_intro')

FUNCS = [('1', 'מצוקה · ספינה ← חוף', 'red'), ('2', 'מצוקה · חוף ← ספינה', 'red'), ('3', 'מצוקה · ספינה ← ספינה', 'red'),
         ('4', 'תיאום חיפוש והצלה', 'sky'), ('5', 'במקום האירוע', 'sky'), ('6', 'איתור', 'sky'),
         ('7', 'מידע בטיחות · MSI', 'amber'), ('8', 'קשר רדיו כללי', 'amber'), ('9', 'גשר לגשר', 'green')]

def s02():
    body = at(24, 24, chip('9 דרישות · כל ספינה, כל ציוד', 'green', 32)) + grid(FUNCS, 3, top=130, h=280, hs=64, ss=26)
    card('s02_functions', 'הדרישות התפקודיות', body, '9 דרישות', 'שלוש התראות מצוקה, תיאום, במקום האירוע, איתור, מידע בטיחות, קשר כללי, וגשר לגשר.',
         bg='u14_bridge', shade=0.75)

def s03():
    body = (at(24, 24, chip('גשר לגשר · דרישה 9', 'green', 34))
            + bottom(rows(('✓', 'תקשורת גשר לגשר', 'green', 30), ('✗', 'פקס מזג אוויר · לא ברשימה', 'red', 28),
                          ('✗', 'שני הנ״ל · ב׳ שגויה', 'red', 28), ('✗', 'אף אחד · יש נכונה', 'red', 28))))
    card('s03_q11', 'דרישה תפקודית', body, 'תשובה א', 'תקשורת גשר לגשר היא אחת מתשע הדרישות. מזג אוויר מגיע ב-MSI, לא בפקס.',
         (EXAM.format(11), 'איזו מהדרישות הבאות היא דרישה תפקודית ב-GMDSS?',
          ['תקשורת גשר לגשר', 'קליטת מפות שידורי מזג אוויר בפקס', 'שני הנ״ל', 'אף אחד מהנ״ל'], 0),
         bg='u14_bridge', pos='50% 40%', shade=0.2)

def s04():
    body = (at(24, 24, chip('On-Scene Communications', 'sky', 34))
            + bottom(rows(('16', 'VHF · ערוץ 16', 'green', 32), ('6', 'ערוץ 6 · גם מטוס חיפוש', 'sky', 30),
                          ('MF', '2182 kHz · בתדר בינוני', 'amber', 30))))
    card('s04_onscene', 'במקום האירוע', body, 'On-Scene', 'הקשר בין מי שבמצוקה לבין מי שבא לעזור. ב-VHF זה ערוץ 16.',
         bg='u18_bounty', pos='50% 40%', shade=0.15)

def s05():
    body = centered(flow([('כלי שייט או מטוס במצוקה', 'red'), ('ערוץ 16 · קשר ישיר', 'amber'), ('ספינות, מסוקים, מטוסי חיפוש', 'green')]))
    card('s05_q19', 'On-Scene Communications', body, 'תשובה ב', 'כלי נייד במצוקה מדבר עם התחנות הניידות שבאות לעזור לו.',
         (EXAM.format(19), 'לאיזה סוג תקשורת מיועד השירות של On-Scene Communications?',
          ['תקשורת פנים בזמן הפלגה', 'בין כלי נייד במצוקה לבין תחנות ניידות המגישות עזרה', 'בין אניות בנושא בטיחות השייט', 'תקשורת המותרת בנמלים בלבד'], 1),
         bg='u18_bounty', shade=0.6)

def s06():
    body = at(24, 24, chip('השאלה: ב-VHF', 'amber', 34)) + grid(
        [('24', 'דופלקס · תחנת חוף', 'red'), ('2182', 'kHz · MF, לא VHF', 'red'), ('70', 'DSC בלבד', 'red'), ('16', 'VHF · במקום האירוע', 'green')], top=130)
    card('s06_q8', 'ערוץ במקום האירוע', body, 'ערוץ 16', '2182 הוא תדר אמיתי למקום האירוע, אבל ב-MF. בשאלה כתוב VHF.',
         (EXAM.format(8), 'איזה מהבאים הוקצה ב-GMDSS VHF לתקשורת במקום האירוע?', ['ערוץ 24', 'ערוץ 2182', 'ערוץ 70', 'ערוץ 16'], 3),
         bg='u18_bounty', shade=0.75)

CHAIN = [('EPIRB · 406 MHz', 'red'), ('לוויין COSPAS-SARSAT', 'sky'), ('LUT · מחשבת מיקום', 'amber'), ('MCC · מנתב', 'sky'), ('RCC · מזניק הצלה', 'green')]

def s07():
    card('s07_cospas', 'מסלול אות המצוקה', centered(flow(CHAIN, 32)), 'L U T', 'תחנת הקרקע מחשבת את המיקום לפי דופלר. ה-RCC הוא שמזניק את ההצלה.',
         bg='u16_cospas', shade=0.7)

def s08():
    body = (at(24, 24, chip('החישוב · על הקרקע', 'amber', 34))
            + bottom(rows(('✓', 'LUT · מחשבת לפי דופלר', 'green', 30), ('✗', 'MCC · מקבל מיקום מוכן', 'red', 28),
                          ('✗', 'הלוויין · רק קולט ומעביר', 'red', 28), ('✗', 'לא ״רק״ GPS · גם בלעדיו', 'red', 28))))
    card('s08_q15', 'מי קובע את המיקום', body, 'תשובה ב', 'ה-LUT קולטת מהלוויין ומחשבת את המיקום. גם משואה בלי GPS מאותרת.',
         (EXAM.format(15), 'מי קובע את מיקום ה-EPIRB הפועלת במערכת ה-Cospas Sarsat?',
          ['תחנת ה-MCC הקולטת מה-LUT', 'תחנת ה-LUT הקולטת את התשדורת מהלוויין', 'הלוויין מחשב בעצמו את המיקום', 'רק ה-EPIRB, בתנאי שיש לה GPS'], 1),
         bg='u16_cospas', shade=0.75)

def s09():
    body = centered(flow([('EPIRB נדלקה בטעות', 'red'), ('מכבים', 'amber'), ('ערוץ 16 · תחנת חוף או RCC', 'sky'), ('MMSI + אתרעת שווא', 'green')]))
    card('s09_false_epirb', 'נדלקה בטעות', body, 'מודיעים', 'לכבות לא מספיק. האות כבר יצא, ולכן מודיעים לתחנת חוף או ל-RCC בערוץ 16.',
         bg='u16_epirb_bracket', pos='60% 50%', shade=0.55)

def s10():
    body = (at(24, 24, chip('ערוץ 16 · למי שמזניק', 'green', 34))
            + bottom(rows(('✓', 'תחנת חוף או RCC', 'green', 30), ('✗', 'כל התחנות · לא מטפלות', 'red', 28),
                          ('✗', 'LUT · תחנה אוטומטית', 'red', 28), ('✗', 'MCC · מרכז ניתוב', 'red', 28))))
    card('s10_q6', 'אתרעת שווא', body, 'תשובה ד', 'מודיעים למי שמטפל בהצלה: תחנת חוף או RCC, בערוץ 16.',
         (EXAM.format(6), 'מה עליך לעשות כאשר EPIRB של COSPAS_SARSAT הופעל בטעות?',
          ['אודיע לכל התחנות בסביבה על ערוץ 16', 'אודיע לתחנת ה-LUT הקרובה על ערוץ 16', 'אודיע לתחנת ה-MCC הקרובה על ערוץ 16', 'אודיע לתחנת חוף או ל-RCC קרובים על ערוץ 16'], 3),
         bg='u16_epirb_bracket', pos='60% 50%', shade=0.2)

def s11():
    body = (at(24, 24, chip('גובה = טווח', 'green', 36))
            + bottom(glass('<div class="p-6 space-y-5"><div class="grid grid-cols-2 gap-4">'
                           + tile('~5 NM', 'ממכ״מ של ספינה', 'sky', 'h-[200px]', 56, 26) + tile('הרבה יותר', 'ממטוס גבוה', 'green', 'h-[200px]', 48, 26) + '</div>'
                           + row('↑', 'לפחות מטר מעל המים', 'green', 30) + '</div>')))
    card('s11_sart', 'טווח ה-SART', body, 'גבוה', 'גלי מכ״מ נעים בקו ישר. ככל שה-SART גבוה יותר, האופק שלו רחוק יותר.',
         bg='u16_sart_radar', shade=0.3)

def s12():
    body = (at(24, 24, chip('גבוה ככל האפשר', 'green', 36))
            + bottom(rows(('✓', 'למקם גבוה ככל האפשר', 'green', 30), ('✗', 'במים · נמוך, טווח קצר', 'red', 28),
                          ('✗', 'אין מצב הספק · ההספק קבוע', 'red', 28), ('✗', 'אין כיול · משיב לבד', 'red', 28))))
    card('s12_q1', 'להגדיל את הטווח', body, 'תשובה ב', 'הטווח תלוי בגובה. אין ל-SART כפתור הספק ואין כיול.',
         (EXAM.format(1), 'כיצד ניתן להגדיל את טווח ה-SART באופן מקסימלי?',
          ['להכניס את ה-SART למים מיד עם הפעלתו', 'למקם את ה-SART גבוה ככל האפשר', 'להפעיל את ה-SART במצב הספק מקסימלי', 'לכייל את תדר השידור בנורית בקרה'], 1),
         bg='u16_sart_pro', shade=0.2)

MSG = ('<div class="ltr font-mono text-[34px] leading-snug text-emerald-200 p-6">'
       '<div class="text-amber-300 font-bold">CH 16</div><div>ALL SHIPS ×3</div><div>THIS IS HAIFA RADIO ×3</div>'
       '<div>TRAFFIC LIST</div><div class="text-amber-300 font-bold">LISTEN ON CHANNEL 25</div></div>')

def s13():
    body = ('<div class="absolute inset-6 flex flex-col justify-between gap-4">' + glass(MSG)
            + flow([('ערוץ 25 · רשימת שמות', 'sky'), ('השם שלך ברשימה? קוראים לתחנה', 'green')], 30) + '</div>')
    card('s13_traffic', 'Traffic List', body, 'רשימת תעבורה', 'לתחנת החוף יש הודעות לכמה ספינות. היא מכריזה ב-16 ומקריאה את הרשימה בערוץ עבודה.',
         bg='u14_coast_station', shade=0.6)

def s14():
    body = (at(24, 24, chip('Traffic = הודעות', 'sky', 34))
            + bottom(rows(('✓', 'הודעות לכמה ספינות · ערוץ 25', 'green', 30), ('✗', 'בטיחות · נפתחת ב-SECURITE', 'red', 28),
                          ('✗', 'לא תנועה צפופה של ספינות', 'red', 28), ('✗', 'יש תשובה נכונה', 'red', 28))))
    card('s14_q2', 'רשימת תעבורה', body, 'תשובה ב', 'חיפה רדיו מחזיקה הודעות לכמה ספינות, ותקריא את הרשימה בערוץ 25.',
         (EXAM.format(2), 'All ships ×3 this is Haifa Radio ×3 Traffic list Listen on channel 25. מה המשמעות?',
          ['לחיפה רדיו יש תעבורת בטיחות חשובה', 'יש לה תעבורה למספר כלי שייט, ברשימות על ערוץ 25', 'יש תנועה צפופה, להאזין על 25 לאזהרות', 'כל התשובות אינן נכונות'], 1),
         bg='u14_coast_station', shade=0.2)

def s15():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u16_raft_epirb', focus=(0.5, 0.5))
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['9 דרישות · אחת מהן גשר לגשר', 'On-Scene · מצוקה מול העוזרים', 'במקום האירוע ב-VHF · ערוץ 16', 'LUT · מחשבת את המיקום',
             'RCC · מזניק את ההצלה', 'נדלקה בטעות · מודיעים ב-16', 'SART · גבוה ככל האפשר', 'Traffic List · הודעות בערוץ עבודה']
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 5 else C.ORANGE)
        text_r(d, 2380, y + 20, s, F(46, False), TEXT)
    save(im, 's15_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15]

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:                              # OneDrive can lock a freshly written PNG
                    import time; time.sleep(2)
