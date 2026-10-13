"""Lesson 16 (l30): EPIRB, SART ו-AIS. Left panels in Tailwind (twcard.py) over Commons photos / Higgsfield scenes; right block in PIL."""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U6 = _load('u06', 'u06_cards.py'); U8 = _load('u08', 'u08_cards.py'); U12 = _load('u12', 'u12_cards.py')
import twcard as T
from twcard import chip, glass, tile, row, digits
from PIL import Image
C.OUT = os.path.join(HERE, '..', 'cards', 'EPIRB, SART ו-AIS'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · EPIRB, SART ו-AIS'
F, text_c, text_r, dot, base, left_panel, right_block, save, RC = C.F, C.text_c, C.text_r, C.dot, C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, GREEN, GREEN_L, BLUE_L, PANEL = C.TEXT, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL
photo = U8.photo; credit = U12.credit
CR = {'u16_epirb_bracket': 'Photo: Marwan Mohamad · CC BY-SA 4.0', 
      'u16_cospas': 'Image: NOAA · Public domain'}
U12.CREDIT.update(CR)
X0, Y0, X1, Y1 = [int(v) for v in U5.inner()]; PW, PH = X1 - X0, Y1 - Y0
VOUT = os.path.join(C.OUT, '_v'); os.makedirs(VOUT, exist_ok=True); VSUB = 'שיעור 16 · EPIRB, SART ו-AIS'
vsave = lambda sid, cap, vis, bot: T.vcard(os.path.join(VOUT, sid + '.png'), cap, vis, bot)

def card(sid, caption, body, title, text, q=None, bg=None, pos='center', shade=0.0):
    im, d = base(); left_panel(d, caption)
    pp = T.panel(sid, body, PW, PH, bg, pos, shade); p = Image.open(pp).convert('RGBA'); im.paste(p, (X0, Y0), p)
    if bg in CR: credit(d, (X0, Y0, X1, Y1), bg)
    right_block(d, title, text, q); save(im, sid)
    vsave(sid, caption, T.vimg(pp) + (f'<div class="absolute bottom-1 right-2 ltr text-white/70 text-[16px]">{CR[bg]}</div>' if bg in CR else ''), T.vbottom(VSUB, title, text, q))

def at(x, y, html, cls=''):
    return f'<div class="absolute {cls}" style="left:{x}px;top:{y}px">{html}</div>'

def bottom(html, cls=''):
    return f'<div class="absolute bottom-6 inset-x-6 {cls}">{html}</div>'

def grid(tiles, cols=2, top=24, h=None):
    return f'<div class="absolute inset-x-6 bottom-6 grid grid-cols-{cols} gap-4 content-center" style="top:{top}px">{tiles}</div>'

def tiles(items, h=230, hs=50, ss=26):
    return ''.join(tile(n, s, t, f'h-[{h}px]', hs, ss) for n, s, t in items)

def rows(*rs, gap=3):
    return glass(f'<div class="p-6 space-y-{gap}">' + ''.join(row(*r) for r in rs) + '</div>')

SAME = at(24, 24, chip('אותה שאלה · נוסח אחר', 'amber', 32))

# ---------- cards ----------
def s01():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u16_epirb_bracket', focus=(0.6, 0.5)); credit(d, (0, 0, 1300, 1440), 'u16_epirb_bracket')
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 16', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'EPIRB · SART · AIS', F(112), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['משואת חירום EPIRB', 'אזורי שייט A1-A4', 'משיב מכ״מ SART', 'זיהוי אוטומטי AIS']):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')
    vsave('s01_intro', 'שיעור 16', T.vphoto('u16_epirb_bracket', '50% 40%'),
          T.vbottom('קורס ניווט חופי ומכשירים', 'EPIRB · SART · AIS', '<br>'.join(['משואת חירום EPIRB', 'אזורי שייט A1-A4', 'משיב מכ״מ SART', 'זיהוי אוטומטי AIS'])))

def s02():
    body = (f'<img src="{T.asset("u16_epirb_parts")}" class="absolute top-0 inset-x-0 w-full h-[900px] object-contain">'
            + '<div class="absolute inset-x-6 bottom-5 flex gap-3 justify-center">' + chip('מצוקה + MMSI', 'red', 26) + chip('48 שעות', 'green', 26)
            + chip('ידני · מגע במים', 'sky', 26) + chip('FLOAT FREE', 'amber', 26) + '</div>')
    card('s02_epirb', 'משואת EPIRB', body, 'EPIRB', 'משואה צפה שמשדרת מצוקה עם ה-MMSI. מותקנת בקופסה הידרוסטטית, ומשתחררת לבד.')

HRU = (f'<div class="absolute inset-y-0 left-0 w-[440px] bg-white"></div><img src="{T.asset("u16_hru")}" class="absolute inset-y-0 left-0 w-[440px] h-full object-contain">')

def side(html, top=24):
    return f'<div class="absolute right-6 bottom-6 left-[464px] flex flex-col justify-center gap-4" style="top:{top}px">{html}</div>'

FF = [('1', 'לחץ המים מפעיל את המשחרר', 'sky', 24), ('2', 'המשחרר דוחף את המכסה', 'sky', 24), ('3', 'המשואה צפה ומשדרת', 'green', 24)]
FFQ = ['התנתקות עצמית וציפה של המשואות', 'חופשי מיכולת לצוף', 'מתקן שמנפח רפסודה', 'אריזה מיוחדת לציפה']

def s03():
    body = HRU + side(chip('משחרר הידרוסטטי · HRU', 'green', 28) + rows(*FF))
    card('s03_q6', 'FLOAT FREE', body, 'תשובה א', 'לחץ המים מפעיל את המשחרר. הוא דוחף את המכסה, והמשואה צפה ומתחילה לשדר.',
         ('שאלה מהמאגר · 6', 'מה פירוש התכונה המכונה FLOAT FREE?', FFQ, 0))

def s04():
    body = HRU + side(chip('אותה שאלה · נוסח אחר', 'amber', 28) + rows(*FF))
    card('s04_q170', 'FLOAT FREE', body, 'תשובה א', 'סידור טכני שמאפשר התנתקות עצמית וציפה של המשואה.',
         ('שאלה מהמאגר · 170', 'מה פרוש התכונה המכונה "FLOAT FREE"?', FFQ, 0))
def s05():
    body = bottom(rows(('✓', 'במים, ליד האסדה', 'green', 32), ('↑', 'האנטנה זקופה', 'green', 30), ('✗', 'בתוך האסדה · השידור נחסם', 'red', 28)))
    card('s05_q64', 'איפה שמים את המשואה', body, 'במים', 'המשואה משדרת הכי טוב כשהיא צפה, קשורה לרפסודה.',
         ('שאלה מהמאגר · 64', 'איפה באסדת ההצלה להניח את ה-EPIRB?', ['בתוך המים בסמוך לאסדה', 'בתוך האסדה, כמה שיותר גבוה', 'בתוך האסדה, במקום מוגן ויבש', 'מיקומו לא משנה'], 0),
         bg='u16_raft_epirb', pos='50% 55%')

def zones(hi=None):
    Z = [('A1', 'טווח VHF · 20-30 מייל', 'green', 46), ('A2', 'טווח MF · עד 150 מייל', 'sky', 64), ('A3', 'לוויין · 70° צפון עד 70° דרום', 'amber', 84), ('A4', 'הקטבים', 'slate', 100)]
    out = ''
    for n, s, t, w in Z:
        b = T.TONES[t if (hi is None or n in hi) else 'slate'][2]
        out += (f'<div class="h-[100px] rounded-r-3xl {b} flex items-center justify-between px-5" style="width:{w}%">'
                f'<span class="ltr text-white font-extrabold text-[46px]">{n}</span><span dir="rtl" class="text-white text-[28px] font-semibold whitespace-nowrap">{s}</span></div>')
    return f'<div class="space-y-4" dir="ltr"><div dir="rtl" class="text-white/80 text-[26px] text-left">מהחוף →</div>{out}</div>'
def s06():
    body = (at(24, 24, chip('אזורי השייט · GMDSS', 'sky', 32))
            + f'<div class="absolute inset-x-6 top-[120px]">{glass("<div class=\"p-6\">" + zones() + "</div>")}</div>'
            + bottom(glass('<div class="p-5 text-white text-[32px] font-bold">EPIRB ערוץ 70 · ~8 מייל · רק A1</div>', 'ring-2 ring-amber-400')))
    card('s06_areas', 'אזורי שייט', body, 'A1 עד A4', 'A1 בטווח VHF, A2 בטווח MF, A3 בכיסוי לוויין, A4 הקטבים. משואת ערוץ 70 מתאימה רק ל-A1.',
         bg='u14_coast_station', shade=0.55)

def s07():
    body = (at(24, 24, chip('COSPAS-SARSAT · דופלר → LUT', 'green', 30))
            + bottom(rows(('406', 'ללוויין · ~5 ק״מ · שומר מידע', 'green', 28), ('121.5', 'ביות למטוסים · ~15 ק״מ', 'amber', 28), ('⏱', 'איתור עד שעה וחצי', 'slate', 28))))
    card('s07_cospas', 'משואה לוויינית', body, '406 MHz', 'לוויינים מקוטב לקוטב מכסים את כל העולם. המיקום מחושב בתחנת הקרקע לפי דופלר.',
         bg='u16_cospas', pos='50% 60%', shade=0.15)

CS = [('406 MHz', 'התדר · ✓', 'green'), ('שייט חופי', 'מותרת · ✓', 'green'), ('דיבור', 'אין · ✗', 'red'), ('כיוון וטווח', 'זה SART · ✗', 'red')]

def s08():
    card('s08_q85', 'משואת Cospas-Sarsat', grid(tiles(CS)), 'תשובה א', 'פועלת על 406 MHz. מותרת בשייט חופי, בלי דיבור, והביות בכיוון וטווח הוא של ה-SART.',
         ('שאלה מהמאגר · 85', 'משואת חירום המשויכת למערכת Cospas-Sarsat:',
          ['פועלת על תדר 406 MHz', 'אסורה בשיט חופי, תזעיק את כל הלוויין', 'מאפשרת קשר בדיבור', 'מאפשרת התבייתות בכיוון וטווח'], 0), bg='u16_cospas', shade=0.8)

def s09():
    card('s09_q169', 'משואת Cospas-Sarsat', SAME + grid(tiles(CS, 200), top=130), 'תשובה א', '406 MHz אל מערך לווייני, ומותרת כחלופה למשואת ערוץ 70.',
         ('שאלה מהמאגר · 169', 'סמן את המשפט הנכון ביחס למשואת Cospas-Sarsat.',
          ['406 MHz ללוויין, מותרת כחלופה למשואת ערוץ 70', 'אסורה בשיט חופי, תזעיק את כל הלוויין', 'מאפשרת קשר בדיבור', 'מאפשרת התבייתות בכיוון וטווח'], 0), bg='u16_cospas', shade=0.8)

def s10():
    body = at(24, 24, chip('לוויינים מקוטב לקוטב', 'green', 34)) + grid(tiles([(z, '✓ מכוסה', 'green') for z in ('A1', 'A2', 'A3', 'A4')], 240, 64), top=130)
    card('s10_q145', 'בכל האזורים', body, 'כל התשובות', 'לוויינים שעוברים מקוטב לקוטב מכסים את כל העולם, כולל הקטבים.',
         ('שאלה מהמאגר · 145', 'באיזה אזורים שימושי EPIRB שעובד עם לוויינים מקוטב לקוטב?', ['A1', 'A2, A3', 'A4', 'כל התשובות נכונות'], 3), bg='u16_cospas', shade=0.75)

def s11():
    f = [('COSPAS-SARSAT', 'דופלר · ✓', 'green'), ('ג׳יירו', 'סביבון · ✗', 'red'), ('SOG', 'מה-GPS · ✗', 'red'), ('מגנטי', 'שדה מגנטי · ✗', 'red')]
    card('s11_q150', 'אפקט דופלר', grid(tiles(f, 230, 40)), 'תשובה א', 'תחנת הקרקע מחשבת את מיקום המשואה לפי השינוי בתדר שהלוויין קולט.',
         ('שאלה מהמאגר · 150', 'באילו מכשירים או מערכות מנוצלת תופעת דופלר?', ['מערך לוויני COSPAS-SARSAT', 'מצפן ג׳ירוסקופי', 'מד מהירות לקריאת SOG', 'מצפן מגנטי'], 0),
         bg='u16_cospas', shade=0.8)

PROD = f'<div class="absolute inset-y-0 left-0 w-[440px] bg-white"></div><img src="{T.asset("u16_sart_pro")}" class="absolute inset-y-0 left-0 w-[440px] h-full object-contain">'

def s12():
    body = PROD + side(chip('SART · משיב מכ״מ', 'red', 32) + rows(('1', 'מפעילים · המתנה', 'slate', 26), ('2', 'מכ״מ X מעיר אותו', 'amber', 26), ('3', 'מהבהב ומצפצף', 'sky', 26), ('4', 'משיב · עד 8 מייל', 'green', 26))
                       + chip('96 שעות המתנה', 'green', 26))
    card('s12_sart', 'משיב מכ״מ SART', body, 'SART', 'רדום עד שמכ״מ בתחום X מקרין עליו. אז הוא משיב, ומופיע על מסך המכ״מ המחפש.')

def s13():
    f = [('X-BAND', 'מעיר אותו · ✓', 'green'), ('S-BAND', 'לא מעיר · ✗', 'red'), ('מים', 'לא מעיר · ✗', 'red'), ('SART אחר', 'לא מעיר · ✗', 'red')]
    card('s13_q75', 'מה מעיר את ה-SART', PROD + side(tiles(f, 190, 42)), 'תשובה ד', 'רק מכ״מ בתחום X מעיר אותו. לא כל מכ״מ, לא מים, ולא SART אחר.',
         ('שאלה מהמאגר · 75', 'כיצד "יתעורר" מכשיר ה-SART לפעולה?', ['הפעלה ידנית ומגע עם מים', 'קליטת פולס של כל מכ״מ', 'הפעלת SART אחר בסביבה', 'רק כאשר מכ״מ ב-X-band מפעיל אותו'], 3))

def s14():
    body = PROD + side(rows(('א', 'משיב הד מכ״מ אקטיבי', 'green', 26), ('ב', 'מפעילים במצוקה', 'green', 26), ('ג', 'SART · השם שלו', 'green', 26)))
    card('s14_q86', 'משיב מכ״מ', body, 'כל התשובות', 'משיב הד אקטיבי, מפעילים אותו במצוקה, ושמו SART.',
         ('שאלה מהמאגר · 86', 'מהו משיב מכ״מ לצורך חיפוש והצלה?', ['קולט מכ״מ ומשמש משיב הד אקטיבי', 'חובה להפעילו במצוקה להתבייתות', 'Search And Rescue Radar Transponder', 'כל התשובות נכונות'], 3))

def s15():
    f = [('מכ״מ X', 'רואה אותו · ✓', 'green'), ('NAVTEX', 'הודעות כתובות · ✗', 'red'), ('ערוץ 70', 'DSC · ✗', 'red'), ('ערוץ 16', 'קשר קולי · ✗', 'red')]
    card('s15_q106', 'מי קולט SART', PROD + side(tiles(f, 190, 42)), 'תשובה ג', 'רק מכ״מ ימי בתחום X רואה את ה-SART. הוא לא משדר בקשר.',
         ('שאלה מהמאגר · 106', 'באילו מכשירים ניתן לקלוט את שידורי ה-SART?', ['NAVTEX', 'VHF על ערוץ 70', 'מכ״ם ימיים בתחום X', 'תחנות החוף על ערוץ 16'], 2))

def screen(col):
    return (f'<img src="{T.asset("u16_sart_radar")}" class="absolute top-0 inset-x-0 w-full">'
            + f'<div class="absolute inset-x-5 bottom-5 top-[700px] grid grid-cols-2 gap-3 content-center">{col}</div>')
def note(s, tone='amber'):
    return glass(f'<div class="p-4 text-white text-[30px] font-bold leading-snug">{s}</div>', f'ring-2 {T.TONES[tone][0]}')

def s16():
    body = screen(note('5-8 מייל · נקודות') + note('1-5 מייל · קשתות', 'sky') + note('פחות ממייל · עיגולים', 'green') + note('SART בנקודה הקרובה למרכז', 'slate'))
    card('s16_sart_screen', 'SART על המכ״מ', body, 'נקודות, קשתות, עיגולים', 'רחוק רואים שורת נקודות, מתקרבים רואים קשתות, וקרוב מאוד עיגולים.')

def s17():
    body = screen(note('SART אחד · מתקרבים אליו') + note('לא 3 רפסודות', 'red'))
    card('s17_q88', 'מה רואים על המסך', body, 'תשובה ג', 'שידורי SART בכ-8 מייל, בכ-5 מייל ובפחות ממייל, בהתאמה.',
         ('שאלה מהמאגר · 88', 'במסך המכ״מ נקלטו נקודות, אחר כך קשתות, ואחר כך עיגולים. מה רואים?',
          ['החזרי מכ״מ חופי של חיל הים', 'משואת מכ״מ לכניסה לנמל', 'SART בכ-8 מייל, כ-5 מייל ופחות ממייל', '3 רפסודות עם SART'], 2))

def s18():
    body = screen(tiles([('כיוון', '✓', 'green'), ('מרחק', '✓', 'green'), ('מהירות', '✗', 'red'), ('קורס', '✗', 'red')], 140, 30))
    card('s18_q126', 'מה מחשבים', body, 'כיוון ומרחק', 'מהסימון על המסך יודעים כיוון ומרחק משוער. ניצול ברפסודה כמעט לא זז.',
         ('שאלה מהמאגר · 126', 'מה ניתן לחשב מגילוי SART על מסך המכ״מ?', ['מרחק וכיוון משוער למטרה', 'מהירות המטרה', 'קורס המטרה', 'שידור מיקום ללוויין'], 0))

SP = [('✓', 'צף · נורה וצפצוף', 'green', 26), ('✓', '96 ש׳ המתנה · 8 ש׳ שידור', 'green', 24), ('✗', 'לא מרותק לסירה', 'red', 26), ('✗', 'אין לחצן שידור', 'red', 26)]
SPQ = ['ציפה, 96 שעות קליטה או 8 שידור, נורה ואות קולי', 'ריתוק קבוע ואנטנה אנכית', 'לחצן שידור שמציג נקודות וקשתות', 'ב ו-ג נכונות']

def s19():
    body = PROD + side('<div class="flex gap-3">' + chip('ON', 'green', 26) + chip('OFF', 'slate', 26) + chip('TEST', 'amber', 26) + '</div>' + rows(*SP))
    card('s19_q87', 'מאפייני SART', body, 'תשובה א', 'צף, עם נורה ואות קולי. 96 שעות בהמתנה או 8 שעות שידור. לפני הפלגה: בדיקה חיצונית, סוללה בתוקף, TEST.',
         ('שאלה מהמאגר · 87', 'מהם מאפייני ה-SART?', SPQ, 0))

def s20():
    card('s20_q177', 'מאפייני SART', PROD + side(chip('אותה שאלה · נוסח אחר', 'amber', 28) + rows(*SP)), 'תשובה א', 'יכולת ציפה, 96 שעות קליטה או 8 שעות שידור, נורה ואות קולי.',
         ('שאלה מהמאגר · 177', 'מה הם מאפייני ה-SART?', SPQ, 0))
def rxtx(extra=''):
    col = lambda head, items, tone: glass(f'<div class="p-5 space-y-2"><div class="{T.TONES[tone][1]} text-[40px] font-extrabold">{head}</div>'
                                          + ''.join(f'<div class="text-white text-[34px] font-semibold ltr text-right">{s}</div>' for s in items) + '</div>', f'ring-2 {T.TONES[tone][0]}')
    return (extra + f'<div class="absolute inset-x-0 top-0 h-[470px] bg-white"></div><img src="{T.asset("u15_navtex_pro")}" class="absolute inset-x-6 top-[20px] h-[430px] w-[calc(100%-48px)] object-contain">' + '<div class="absolute inset-x-6 bottom-6 top-[490px] grid grid-cols-2 gap-5 content-center">'
            + col('קולטים מצוקה', ['NAVTEX · D', 'VHF · DSC'], 'green') + col('רק משדרים', ['EPIRB', 'SART'], 'red') + '</div>')

def s21():
    card('s21_q62', 'מי קולט מצוקה', rxtx(), 'NAVTEX', 'EPIRB ו-SART רק משדרים. מצוקה של אחרים תשמע בקשר וב-NAVTEX.',
         ('שאלה מהמאגר · 62', 'באיזה מכשיר ניתן לדעת על מצוקה של כלי שייט אחרים?', ['NAVTEX', 'SART', 'EPIRB', 'אף תשובה, רק ב-DSC'], 0), )

def s22():
    card('s22_q107', 'מי קולט מצוקה', rxtx(), 'NAVTEX', 'SART ו-EPIRB משדרים בלבד. מצוקה קולטים בקשר וב-NAVTEX.',
         ('שאלה מהמאגר · 107', 'על אילו מכשירים בספינה ניתן לקלוט הודעת מצוקה?', ['NAVTEX', 'S.A.R.T', 'E.P.I.R.B', 'אף תשובה, רק בקשר'], 0), )

def s23():
    ok = tiles([(n, '✓', 'green') for n in ('VHF', 'DSC', 'VHF נייד', 'NAVTEX', 'EPIRB', 'SART')], 150, 38, 24)
    no = tiles([('מכ״מ', 'לא GMDSS · ✗', 'red'), ('D.F.', 'לא דרישה · ✗', 'red')], 150, 38, 24)
    body = at(24, 24, chip('חובה באזור A1', 'green', 34)) + f'<div class="absolute inset-x-6 bottom-6 top-[130px] grid grid-cols-2 gap-3 content-center">{ok}{no}</div>'
    card('s23_q110', 'ציוד חובה ב-A1', body, 'תשובה ב', 'VHF עם DSC, VHF נייד, NAVTEX, EPIRB ו-SART.',
         ('שאלה מהמאגר · 110', 'לפי ה-GMDSS, איזה ציוד חייב להיות בספינה באזור A1?',
          ['SART, EPIRB, DSC, RADAR', 'DSC, SART, EPIRB, VHF נייד, NAVTEX, VHF', 'DSC, SART, EPIRB, VHF נייד', 'VHF, SART, EPIRB, DSC, D.F.'], 1), bg='u13_vhf', shade=0.8)

def tag(x, y, name, info):
    return at(x, y, glass(f'<div class="px-5 py-3"><div class="text-amber-300 font-extrabold text-[30px] ltr">{name}</div>'
                          f'<div class="text-white text-[24px] ltr">{info}</div></div>', 'ring-2 ring-amber-400'))

def s24():
    body = (at(24, 24, chip('AIS · מזהה אוטומטי ב-VHF', 'green', 32))
            + bottom(rows(('ID', 'שם, MMSI, אות קריאה, גודל', 'sky', 28), ('➤', 'מיקום, קורס, מהירות', 'green', 28), ('!', 'מתי תעבור הכי קרוב', 'amber', 28))))
    card('s24_ais', 'מערכת AIS', body, 'AIS', 'כל ספינה משדרת לבד מי היא, איפה, לאן ובאיזו מהירות. רואים אותה על הפלוטר או המכ״מ.',
         bg='u16_vhf_ais', pos='40% 50%', shade=0.05)

def s25():
    f = [('בטיחות', 'נגד התנגשויות · ✓', 'green'), ('DSC', 'לא מחליף · ✗', 'red'), ('NAVTEX', 'לא מחליף · ✗', 'red'), ('מכ״מ', 'לא מגדיל טווח · ✗', 'red')]
    card('s25_q128', 'מטרת ה-AIS', grid(tiles(f, 200, 44), top=600), 'תשובה ג', 'AIS נועד להגביר את בטיחות השייט ולמנוע התנגשויות.',
         ('שאלה מהמאגר · 128', 'מהי מטרתה של מערכת ה-AIS?', ['תחליף ל-DSC', 'מידע בטיחות במקום NAVTEX', 'להגביר בטיחות ולמנוע התנגשויות', 'להגדיל את טווח המכ״מ'], 2),
         bg='u16_vhf_ais', pos='40% 30%', shade=0.1)

def s26():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u16_raft_epirb', focus=(0.45, 0.55))
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['EPIRB · מצוקה + MMSI', 'FLOAT FREE · משתחררת לבד', 'ברפסודה · במים', 'ערוץ 70 · רק A1',
             '406 MHz · כל העולם · דופלר', 'SART · רק מכ״מ X', 'נקודות, קשתות, עיגולים', 'AIS · נגד התנגשויות']
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 5 else C.ORANGE)
        text_r(d, 2380, y + 20, s, F(46, False), TEXT)
    save(im, 's26_summary')
    lst = ''.join(f'<div class="flex items-center gap-4 rounded-2xl bg-slate-800/80 px-5 py-2 text-white text-[34px]"><span class="w-4 h-4 rounded-full {"bg-emerald-400" if i < 5 else "bg-amber-400"} shrink-0"></span>{t}</div>' for i, t in enumerate(items))
    vsave('s26_summary', 'סיכום', T.vphoto('u16_raft_epirb', '45% 55%'), f'<div class="space-y-2">{lst}</div>')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26]
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
