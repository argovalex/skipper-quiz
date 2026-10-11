"""Lesson 14 (l30): ערוצים, MMSI ו-DSC. Left panels in Tailwind (twcard.py) over real photos / Higgsfield scenes; right block in PIL."""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U6 = _load('u06', 'u06_cards.py'); U8 = _load('u08', 'u08_cards.py'); U12 = _load('u12', 'u12_cards.py')
import twcard as T
from twcard import chip, glass, tile, row, digits
from PIL import Image
C.OUT = os.path.join(HERE, '..', 'cards', 'ערוצים, MMSI ו-DSC'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · ערוצים, MMSI ו-DSC'
F, text_c, text_r, dot, base, left_panel, right_block, save, RC = C.F, C.text_c, C.text_r, C.dot, C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, GREEN, GREEN_L, BLUE_L, PANEL = C.TEXT, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL
photo = U8.photo; U12.CREDIT.update({'u13_vhf': 'Photo: PaterMcFly · CC BY 3.0'}); credit = U12.credit
X0, Y0, X1, Y1 = [int(v) for v in U5.inner()]; PW, PH = X1 - X0, Y1 - Y0
CR = {'u13_vhf': 'Photo: PaterMcFly · CC BY 3.0'}

def card(sid, caption, body, title, text, q=None, bg=None, pos='center', shade=0.0):
    im, d = base(); left_panel(d, caption)
    p = Image.open(T.panel(sid, body, PW, PH, bg, pos, shade)).convert('RGBA'); im.paste(p, (X0, Y0), p)
    if bg in CR: credit(d, (X0, Y0, X1, Y1), bg)
    right_block(d, title, text, q); save(im, sid)

def at(x, y, html, cls=''):
    return f'<div class="absolute {cls}" style="left:{x}px;top:{y}px">{html}</div>'

def bottom(html, cls=''):
    return f'<div class="absolute bottom-6 inset-x-6 {cls}">{html}</div>'

CH = [('16', 'קריאה ומצוקה', 'red'), ('70', 'DSC בלבד', 'amber'), ('06', 'בין ספינות · חיפוש והצלה', 'green'), ('08', 'בין ספינות', 'green'),
      ('13', 'גשר לגשר', 'sky'), ('17', 'סיפון · 1W', 'slate'), ('24-26', 'DUPLEX · ציבורי', 'amber'), ('נמל', 'תפעול נמל · פיקוח תנועה', 'slate')]

def board(hi=None, dim=False):
    tiles = ''.join(tile(n, s, t if (hi is None or n in hi) else 'slate', 'h-[180px]' + (' opacity-40' if hi and n not in hi else ''), 46, 24) for n, s, t in CH)
    return f'<div class="absolute inset-6 grid grid-cols-2 gap-4 content-center">{tiles}</div>'

# ---------- cards ----------
def s01():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u13_vhf', focus=(0.6, 0.55)); credit(d, (0, 0, 1300, 1440), 'u13_vhf')
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 14', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'ערוצים, MMSI ו-DSC', F(118), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['SIMPLEX ו-DUPLEX', 'הערוצים החשובים', 'אותות קריאה ו-MMSI', 'DSC']):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    body = (at(24, 24, chip('SIMPLEX · תדר אחד', 'green', 36))
            + bottom(glass('<div class="p-6 space-y-4">' + row('1', 'מדבר ולוחץ · "עבור"') + row('2', 'רק אז השני עונה')
                           + row('✓', 'ספינה ↔ ספינה · ספינה ↔ חוף', 'sky') + '</div>')))
    card('s02_simplex', 'SIMPLEX', body, 'SIMPLEX', 'משדרים וקולטים באותו תדר, לסירוגין. עובד בין ספינות ובין ספינה לחוף.', bg='u14_two_yachts', pos='50% 40%')

def s03():
    body = (at(24, 24, chip('ערוץ 25 · DUPLEX', 'amber', 36))
            + bottom(glass('<div class="p-6 space-y-3">'
                           + row('↑', 'ספינה משדרת <span class="ltr">160.2 MHz</span>', 'sky') + row('↓', 'ספינה קולטת <span class="ltr">161.8 MHz</span>', 'green')
                           + '<div class="flex gap-3 pt-2">' + chip('✓ ספינה ↔ חוף', 'green', 26) + chip('✗ ספינה ↔ ספינה', 'red', 26) + chip('✗ חוף ↔ חוף', 'red', 26) + '</div>'
                           + '<div class="text-amber-300 text-[28px] font-semibold">המכשיר עובר לבד לפי הערוץ</div></div>')))
    card('s03_duplex', 'DUPLEX', body, 'DUPLEX', 'שני תדרים: מדברים ומקשיבים יחד, כמו בטלפון. רק בין ספינה לתחנת חוף.', bg='u14_coast_station', pos='50% 50%')

def s04():
    body = bottom(glass('<div class="p-6 space-y-4">' + row('16', 'ערוץ SIMPLEX', 'green', 32) + row('25', 'ערוץ DUPLEX', 'amber', 32)
                        + '<div class="text-white text-[32px] font-bold pt-2">אתה בוחר ערוץ, המכשיר בוחר שיטה</div></div>'))
    card('s04_q122', 'אוטומטי לפי הערוץ', body, 'אין בחירה', 'כל ערוץ מוגדר מראש. המכשיר עובר בין SIMPLEX ל-DUPLEX לבד.',
         ('שאלה מהמאגר · 122', 'מתי תבחר לשדר ב-SIMPLEX ומתי ב-DUPLEX?',
          ['רצוי לשדר תמיד ב-DUPLEX', 'המכשיר תמיד על SIMPLEX', 'המכשיר תמיד על DUPLEX', 'אין בחירה, המכשיר עובר אוטומטית לפי הערוץ'], 3),
         bg='u13_vhf', pos='62% 55%', shade=0.15)

def s05():
    card('s05_channels', 'הערוצים החשובים', board(), 'מפת ערוצים', 'לכל סוג תקשורת ערוצים משלו. 16 לקריאה ומצוקה, 70 ל-DSC, 6/8/13 בין ספינות, 24-26 DUPLEX ציבורי.',
         bg='u13_vhf', pos='62% 55%', shade=0.75)

def s06():
    card('s06_q120', 'ערוץ 25', board({'24-26'}), 'לא, DUPLEX', 'שתי יאכטות משדרות באותו תדר ומקשיבות באותו תדר. הן לא שומעות זו את זו.',
         ('שאלה מהמאגר · 120', 'האם שתי יאכטות יכולות לדבר ביניהן בערוץ 25?',
          ['לא, ערוץ מצוקה חלופי', 'כן, ערוץ תקשורת ציבורי', 'כן, ערוץ בין כלי שייט ישראלים', 'לא, זהו ערוץ דופלקס'], 3), bg='u14_two_yachts', shade=0.7)

def s07():
    card('s07_q68', 'ערוץ 26', board({'24-26'}), 'לא, DUPLEX', 'ערוץ 26 דו מגמי, לתקשורת ציבורית דרך תחנת חוף. הלאום לא משנה.',
         ('שאלה מהמאגר · 68', 'האם שתי יאכטות ישראליות יכולות לדבר ביניהן על ערוץ 26?',
          ['לא, ערוץ משני לחירום', 'כן, ערוץ תקשורת כללית', 'כן, רק ליאכטות ישראליות', 'לא, ערוץ דו מגמי לתקשורת ציבורית'], 3), bg='u14_two_yachts', shade=0.7)

def s08():
    body = at(24, 24, chip('06 · בין ספינות', 'green', 40)) + bottom(glass('<div class="p-6 space-y-3">' + row('16', 'מצוקה, דחיפות, בטיחות וקריאה', 'red', 28)
                                                                               + row('70', 'אזהרות אוטומטיות ב-DSC', 'amber', 28) + row('✗', 'NAVTEX · מקלט נפרד', 'slate', 28) + '</div>'))
    card('s08_q69', 'ערוץ 6', body, 'בין כלי שייט', 'ערוץ 6 לקשר בין ספינות, וגם בחיפוש והצלה.',
         ('שאלה מהמאגר · 69', 'מה משמש ערוץ 6 במכשיר קשר VHF?',
          ['הודעות שידורי NAVTEX', 'אזהרות בקריאה אוטומטית', 'מצוקה, דחיפות, בטיחות וקריאה', 'קשר בין כלי שייט'], 3), bg='u14_two_yachts', pos='50% 40%')

def s09():
    groups = [('06 · 08 · 13', 'SIMPLEX בין ספינות', 'green'), ('25 · 70 · 76', 'DUPLEX ו-DSC', 'red'), ('17 · 24 · 75', 'הספק נמוך ו-DUPLEX', 'red'), ('DUPLEX', 'ספינות לא שומעות', 'red')]
    tiles = ''.join(tile(n, s, t, 'h-[200px]', 44, 26) for n, s, t in groups)
    body = at(24, 24, chip('מצוקה ב-16 · עוברים לערוץ נקי', 'amber', 32)) + f'<div class="absolute inset-x-6 bottom-6 top-[130px] grid grid-cols-2 gap-4 content-center">{tiles}</div>'
    card('s09_q56', 'ערוץ נקי למצוקה', body, '06, 08, 13', 'במצוקה עוברים לערוץ SIMPLEX בין ספינות, שכולם שומעים בו.',
         ('שאלה מהמאגר · 56', 'מצוקה על 16 עם הפרעות. איזו קבוצת ערוצים מתאימה למעבר?',
          ['25, 70, 76', '17, 24, 75', '06, 08, 13', 'כל ערוצי ה-DUPLEX'], 2), bg='u14_bridge', shade=0.65)

def s10():
    body = (at(24, 24, chip('13 · גשר לגשר · כן מדברים', 'green', 32))
            + bottom(glass('<div class="p-6 space-y-3">' + row('25', 'DUPLEX · רק עם תחנת חוף', 'red', 28) + row('17', 'הספק 1W · טווח קטן', 'red', 28)
                           + row('70', 'רק תקשורת ספרתית', 'red', 28) + row('?', 'בלי להאזין קודם · ערוץ תפוס', 'red', 28) + '</div>')))
    card('s10_q93', 'מחפשים את הטעות', body, 'תשובה א', 'בערוץ 13 ספינות דווקא מדברות זו עם זו, אז הקשר לא יאבד. כל השאר נכונות.',
         ('שאלה מהמאגר · 93', 'במעבר לאילו ערוצים יאבד קשר דיבור בין שתי ספינות? סמן את התשובה שאינה נכונה.',
          ['13, כי הוא גשר לגשר של אניות', '25, כי הוא DUPLEX עם תחנות חוף', '17 בהספק נמוך, 70 רק ספרתי', 'מעבר בלי להאזין קודם'], 0), bg='u14_bridge', pos='50% 45%')

def s11():
    yes = ''.join(f'<div class="text-white text-[38px] font-semibold">✓ {s}</div>' for s in ['מצוקה ובטיחות', 'חיפוש והצלה', 'תפעול נמל', 'גשר לגשר', 'סיפון', 'פיקוח תנועה', 'תקשורת ציבורית', 'DSC'])
    no = ''.join(f'<div class="text-white text-[38px] font-semibold">✗ {s}</div>' for s in ['השגחה על עוגנים', 'אזעקת מכ״מ אוטומטית', 'חיוג דרך לוויין'])
    body = ('<div class="absolute inset-6 grid grid-cols-2 gap-5">'
            + glass(f'<div class="p-6 space-y-3"><div class="text-emerald-300 text-[46px] font-extrabold">יש ערוצים</div>{yes}</div>', 'ring-emerald-400/60')
            + glass(f'<div class="p-6 space-y-3"><div class="text-rose-300 text-[46px] font-extrabold">אין ערוצים</div>{no}</div>', 'ring-rose-400/60') + '</div>')
    card('s11_q92', 'למה הוקצו ערוצים', body, 'תשובה ד', 'אין ערוצי VHF להשגחה על עוגנים, לאזעקת מכ״מ או לחיוג דרך לוויין.',
         ('שאלה מהמאגר · 92', 'לאילו תחומים לא הוקצו ערוצים בתחום התג״מ הימי?',
          ['מצוקה ובטיחות, חיפוש והצלה, נמל', 'גשר לגשר, סיפון, פיקוח תנועה', 'תעבורה ציבורית, DSC', 'השגחה על עוגנים, אזעקת מכ״מ, חיוג לווייני'], 3), bg='u13_vhf', shade=0.8)

def s12():
    idc = glass('<div class="p-6 grid grid-cols-3 gap-4">' + tile('Haifa Radio', 'שם התחנה', 'sky', '', 34) + tile('4XO', 'אות קריאה', 'amber', '', 44) + tile('004280001', 'מספר DSC', 'green', '', 34) + '</div>')
    st = glass('<div class="p-6 space-y-3">' + row('4X', 'קוד המדינה · ישראל', 'amber', 28) + row('+1', 'אות אחת · תחנת חוף', 'sky', 28)
               + row('+2', 'שתי אותיות · כלי שייט', 'green', 28) + row('+3', 'שלוש אותיות · מטוס', 'slate', 28) + '</div>')
    body = f'<div class="absolute inset-6 flex flex-col justify-between">{idc}{st}</div>'
    card('s12_callsigns', 'שלושה מזהים', body, 'אותות קריאה', 'שם, אות קריאה ומספר DSC. שני הסימנים הראשונים הם המדינה, ומה שאחריהם מגלה את סוג התחנה.',
         bg='u14_coast_station', shade=0.2)

def s13():
    ex = ''.join(tile(n, s, t, 'h-[150px]', 40, 24) for n, s, t in [('4X3738', 'אות קריאה', 'amber'), ('5BCT', 'אות קריאה', 'amber'), ('ELMR2', 'אות קריאה', 'amber'), ('Lilach', 'Cabin Cruiser · סוג + שם', 'green')])
    body = f'<div class="absolute inset-x-6 bottom-6 grid grid-cols-2 gap-4">{ex}</div>'
    card('s13_q90', 'זיהוי בקשר בינלאומי', body, 'ב ו-ג', 'אות קריאה, או שם כלי השייט עם סוג העיסוק או ההנעה. מספר הפלגה הוא לא זיהוי.',
         ('שאלה מהמאגר · 90', 'מהו זיהוי תחנת רדיו של כלי שיט בתקשורת בינלאומית?',
          ['מספר ההפלגה ונמל היציאה', 'שם כלי השיט עם סוג העיסוק או ההנעה', '4X3738, 5BCT, ELMR2, Cabin Cruiser Lilach', 'תשובות ב ו-ג נכונות'], 3), bg='u14_two_yachts', pos='50% 35%')

MM = [([('428', 'green', 'MID'), ('xxxxxx', None, '')], 'כלי שייט'), ([('00', 'sky', ''), ('428', 'green', 'MID'), ('xxxx', None, '')], 'תחנת חוף'),
      ([('0', 'amber', ''), ('428', 'green', 'MID'), ('xxxxx', None, '')], 'קבוצת כלי שייט')]

def mmsi_rows():
    return ''.join(glass(f'<div class="px-5 py-4 flex items-center justify-between gap-4"><div class="text-white text-[30px] font-bold w-[230px]">{lab}</div>{digits(g)}</div>') for g, lab in MM)

def s14():
    body = at(24, 24, chip('MMSI · 9 ספרות · ישראל 428', 'green', 34)) + f'<div class="absolute inset-x-6 bottom-6 space-y-4">{mmsi_rows()}</div>'
    card('s14_mmsi', 'מבנה ה-MMSI', body, 'MMSI', 'תשע ספרות, ושלוש מהן קוד המדינה. מיקום הקוד מגלה אם זה כלי שייט, תחנת חוף או קבוצה.', bg='u13_vhf', pos='62% 30%', shade=0.35)

def s15():
    body = at(24, 24, chip('MMSI', 'green', 40)) + bottom(glass('<div class="p-6 space-y-3">' + row('א', '9 ספרות · DSC · לאום וסוג תחנה', 'green', 28)
                                                                  + row('ב', 'בורר את ההודעות שלך', 'green', 28) + row('ג', 'ברשיון ובמסמכים · זמין להקראה', 'green', 28) + '</div>'))
    card('s15_q52', 'כל התשובות', body, 'כל התשובות', 'ה-MMSI מזהה אותך ב-DSC, בורר הודעות, ורשום ברשיון תחנת האלחוט.',
         ('שאלה מהמאגר · 52', 'מהו ה-MMSI של כלי שייט?',
          ['9 ספרות, קריאה ספרתית, לאום וסוג תחנה', 'מאפשר ברירה של הודעות לכלי השיט', 'במסמכי כלי השיט וזמין להקראה', 'כל התשובות נכונות'], 3), bg='u13_vhf', pos='62% 30%', shade=0.3)

def s16():
    body = ('<div class="absolute inset-6 flex flex-col justify-center gap-6">' + glass('<div class="p-6">' + digits([('428', 'green', 'MID · ישראל'), ('000500', None, '')]) + '</div>')
            + glass('<div class="p-6 space-y-3">' + row('✓', 'מתחיל ב-428 · כלי שייט', 'green', 30) + row('✗', 'קבוצה מתחילה ב-0', 'red', 30) + row('✗', 'תחנת חוף מתחילה ב-00', 'red', 30) + '</div>') + '</div>')
    card('s16_q142', '428000500', body, 'א ו-ב', 'מתחיל ב-428 בלי אפס לפני: MMSI של כלי שייט, במדינה עם MID 428.',
         ('שאלה מהמאגר · 142', 'מהו הצירוף 428000500?',
          ['MMSI של מתקן DSC של כלי שייט', 'MMSI של מדינה בעלת MID 428', 'MMSI של קבוצת מתקני DSC', 'תשובות א ו-ב נכונות'], 3), bg='u13_vhf', shade=0.8)

def s17():
    body = (at(24, 24, chip('DSC · ערוץ 70', 'amber', 36))
            + bottom(glass('<div class="p-6 space-y-3">' + row('1', 'מרימים את המכסה', 'red', 30) + row('2', 'לוחצים 5 שניות', 'red', 30)
                           + row('↻', 'חוזר עד שמאשרים', 'amber', 30) + row('ID', 'MMSI בכל שידור · מיקום ושעה עם GPS', 'green', 28) + '</div>')))
    card('s17_dsc', 'קריאת ברירה ספרתית', body, 'DSC', 'מקודד ומפענח הודעות ספרתיות בערוץ 70. התראת מצוקה, פחות עומס על 16, והקמת קשר.', bg='u13_vhf', pos='35% 62%')

def s18():
    body = at(24, 24, chip('מקודד ומפענח', 'green', 36)) + bottom(glass('<div class="p-6 space-y-3">' + row('✓', 'בתוך מכשיר הקשר', 'green', 30) + row('✓', 'לא תלוי במיומנות המפעיל', 'green', 30)
                                                                          + row('✗', 'לא ממסר לוויין · ערוץ 70', 'red', 30) + '</div>'))
    card('s18_q53', 'המכלול DSC', body, 'תשובה ג', 'מכלול בתוך מכשיר הקשר שמקודד ומפענח הודעות ספרתיות, בלי תלות במפעיל.',
         ('שאלה מהמאגר · 53, 171', 'מהו המכלול האלקטרוני המכונה DSC?',
          ['עיבוד הודעות מתפריטים', 'קשר מיידי דרך ממסר לוויין', 'מכלול לפענוח וקידוד הודעות ספרתיות', 'תשובות א ו-ב נכונות'], 2), bg='u13_vhf', pos='62% 55%', shade=0.3)

def s19():
    body = '<div class="absolute inset-6 grid grid-cols-2 gap-5 content-center">' + tile('DSC', 'המכלול · מזהה, מפענח ומעבד', 'green', 'h-[300px]', 70, 30) + tile('MMSI', 'המספר · 9 ספרות', 'amber', 'h-[300px]', 70, 30) + '</div>'
    card('s19_q89', 'מכלול מול מספר', body, 'תשובה ב', 'קריאת ברירה ספרתית היא המכלול. המספר הייחודי הוא ה-MMSI.',
         ('שאלה מהמאגר · 89', 'למה מתכוונים כשאומרים "קריאת ברירה ספרתית"?',
          ['מספר ייחודי לכל כלי שיט', 'המכשיר או המכלול שמזהה, מפענח ומעבד הודעות ספרתיות', 'המספר המקודד באתחול מכשיר DSC', 'כל התשובות נכונות'], 1), bg='u13_vhf', shade=0.8)

def s20():
    f = [('MMSI', 'תמיד', 'green'), ('מיקום', 'רק עם GPS', 'slate'), ('שעה', 'רק עם GPS', 'slate'), ('מצוקה', 'רק בהתראה', 'slate')]
    body = '<div class="absolute inset-6 grid grid-cols-2 gap-5 content-center">' + ''.join(tile(n, s, t, 'h-[240px]', 54, 30) for n, s, t in f) + '</div>'
    card('s20_q143', 'מה יוצא בכל שידור', body, 'MMSI', 'בכל שידור DSC יוצא ה-MMSI. מיקום ושעה רק עם GPS, ומצב מצוקה רק בהתראה.',
         ('שאלה מהמאגר · 143', 'איזה נתונים יוצאים אוטומטית מ-DSC בכל שידור?', ['זמן', 'מיקום', 'MMSI', 'מצב המצוקה'], 2), bg='u13_vhf', shade=0.8)

def s21():
    steps = ''.join(f'<div class="flex-1 h-[150px] rounded-2xl bg-rose-500/85 flex items-center justify-center text-white font-extrabold text-[34px]">{s}</div>' for s in ['שידור', 'חוזר', 'חוזר'])
    body = (at(24, 24, chip('התראת מצוקה DSC', 'red', 36))
            + bottom(glass(f'<div class="p-6 space-y-5"><div class="flex gap-3" dir="rtl">{steps}<div class="flex-1 h-[150px] rounded-2xl bg-emerald-500 flex items-center justify-center text-white font-extrabold text-[30px] text-center leading-tight">אישור<br>קבלה</div></div>'
                           + '<div class="text-white text-[30px] font-semibold">עוצר רק כשתחנת חוף או כלי שייט מאשרים</div></div>')))
    card('s21_q74', 'עד שמאשרים', body, 'תשובה ד', 'ההתראה חוזרת שוב ושוב, עד שתחנת חוף או כלי שייט אחר מאשרים שקיבלו.',
         ('שאלה מהמאגר · 74', 'עד מתי ימשיך מכשיר ה-DSC לשדר התראת מצוקה?',
          ['עד שכלי שיט אחר יקבל', 'רק פעם אחת', 'עד שהמפעיל לוחץ הפסקה', 'עד שתחנת חוף או כלי שיט יאשרו קבלה'], 3), bg='u13_vhf', pos='35% 62%', shade=0.2)

def s22():
    body = at(24, 24, chip('הסמכה למפעיל קשר', 'green', 36)) + bottom(glass('<div class="p-6 space-y-3">' + row('!', 'בלי נוהל ופקדים · אין עזרה במצוקה', 'red', 28)
                                                                               + row('!', 'מפריע לתקשורת הצלה של אחרים', 'red', 28) + '</div>'))
    card('s22_q54', 'למה צריך הסמכה', body, 'תשובה א', 'מי שלא מכיר נהלים ופקדים עלול לא לקבל עזרה, או להפריע להצלה של אחרים.',
         ('שאלה מהמאגר · 54', 'מדוע נדרשת הסמכה להפעלת ציוד קשר בתקשורת בין-לאומית?',
          ['אי ידיעת הנוהל והפקדים מונעת עזרה או מפריעה להצלה', 'היגוי לא נכון של ביטוי יגרום "VHF collision"', 'מפעיל הרדיו לא יודע את שפת מי שבמצוקה', 'כך נהוג לפי הימאות הטובה'], 0), bg='u14_chart_table')

def s23():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u13_vhf', focus=(0.6, 0.55)); credit(d, (0, 0, 1300, 1440), 'u13_vhf')
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['SIMPLEX · תדר אחד, לסירוגין', 'DUPLEX · שני תדרים, רק מול חוף', 'הערוץ קובע את השיטה', '16 מצוקה · 70 DSC',
             '6, 8, 13 · בין ספינות', '25, 26 · DUPLEX ציבורי', 'MMSI · 9 ספרות · ישראל 428', 'DSC · MMSI תמיד, חוזר עד אישור']
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 6 else C.ORANGE)
        text_r(d, 2380, y + 20, s, F(46, False), TEXT)
    save(im, 's23_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23]
sheet = lambda: U6.sheet.__globals__.__setitem__('C', C) or U6.sheet()

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:                              # OneDrive can lock a freshly written PNG
                    import time; time.sleep(2)
    sheet()
