"""l40 lesson: פתרון שאלות המבחן (the 12 exam questions not covered by lessons 1 and 8).
Same look and helpers as supp_cards.py; questions read from lessons/l40/exam-1.json via examq(n)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import supp_cards as S
from supp_cards import C, U12, T, chip, glass, tile, row, at, bottom, grid, rows, flow, centered, examq, photo
from PIL import Image
NAME = 'פתרון שאלות המבחן'
C.OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cards', NAME); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'קורס GMDSS · פתרון שאלות המבחן'
F, text_c, text_r, dot, base, left_panel, right_block, save, RC = C.F, C.text_c, C.text_r, C.dot, C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, GREEN, GREEN_L, BLUE_L, PANEL = C.TEXT, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL
CR = {'u13_handheld': 'Photo: Ulflarsen · CC BY-SA 3.0', 'u18_vhf16': 'Photo: PaterMcFly · CC BY 3.0 · edited',
      'u13_vhf': 'Photo: PaterMcFly · CC BY 3.0'}
U12.CREDIT.update(CR)
X0, Y0, X1, Y1, PW, PH = S.X0, S.Y0, S.X1, S.Y1, S.PW, S.PH

def card(sid, caption, body, title, text, q=None, bg=None, pos='center', shade=0.0):
    im, d = base(); left_panel(d, caption)
    p = Image.open(T.panel('l40p_' + sid, body, PW, PH, bg, pos, shade)).convert('RGBA'); im.paste(p, (X0, Y0), p)
    if bg in CR or bg in S.CR: U12.credit(d, (X0, Y0, X1, Y1), bg)
    right_block(d, title, text, q); save(im, sid)

def ans(head, tone, *rs):
    return at(24, 24, chip(head, tone, 34)) + bottom(rows(*rs))

# ---------- cards ----------
def s01():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u14_coast_station', focus=(0.5, 0.5))
    text_c(d, RC, 380, 'קורס GMDSS · מבחן משרד התקשורת', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'פתרון שאלות המבחן', F(112), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['ערוצים ומכשיר נייד', 'עדיפויות וקודי השתקה', 'AIS · NAVTEX', 'יומן הרדיו · MMSI']):
        text_c(d, RC, 810 + i * 84, s, F(52, False), TEXT)
    text_c(d, RC, 1180, '12 שאלות · ועם השיעורים הקודמים, כל ה-20', F(44, False), GREEN_L)
    save(im, 's01_intro')

def s02():
    body = at(24, 24, chip('ערוצי VHF במבחן', 'sky', 34)) + grid(
        [('16', 'קריאה · מצוקה, דחיפות, בטיחות', 'green'), ('70', 'DSC · ספרתי בלבד', 'sky'),
         ('15', 'על הסיפון · וואט 1', 'amber'), ('17', 'על הסיפון · וואט 1', 'amber')], top=130)
    card('s02_channels', 'הערוצים', body, 'ערוצים', 'ערוץ 16 לקול, ערוץ 70 ל-DSC. ערוצים 15 ו-17 מוגבלים לוואט אחד.',
         bg='u17_vhf_call', shade=0.75)

def s03():
    body = ans('ערוץ 16 · קול', 'green', ('✓', 'מצוקה, דחיפות, בטיחות וקריאה', 'green', 30), ('✗', 'NAVTEX · מקלט נפרד, MF', 'red', 28),
               ('✗', 'קריאה אוטומטית · DSC בערוץ 70', 'red', 28), ('✗', 'מזג אוויר · NAVTEX או ערוץ עבודה', 'red', 28))
    card('s03_g17', 'ערוץ 16', body, 'תשובה ג', 'ערוץ 16 הוא ערוץ הקול של הקריאה ושל המצוקה, הדחיפות והבטיחות.',
         examq(17), bg='u17_vhf_call', shade=0.2)

def s04():
    body = ans('וואט 1 · 15 ו-17', 'amber', ('✓', 'CH15 · CH17 · על הסיפון', 'green', 30), ('✗', '12 · 14 · ערוצי נמל, הספק מלא', 'red', 28),
               ('✗', '70 · DSC · 6 · בין ספינות', 'red', 28), ('✗', '67 · לא מוגבל לוואט 1', 'red', 28))
    card('s04_g3', 'וואט אחד מקסימום', body, 'תשובה ג', 'רק ערוצים 15 ו-17, לקשר על הסיפון, מוגבלים לוואט אחד.',
         examq(3), bg='u17_vhf_call', shade=0.2)

def s05():
    body = (at(24, 24, chip('VHF נייד · סירת הצלה', 'green', 34))
            + bottom(rows(('FM', 'כמו כל VHF ימי', 'green', 30), ('↔', 'SIMPLEX בלבד', 'sky', 30),
                          ('W', 'עד 5 וואט · נמוך 1 וואט', 'amber', 30), ('16', 'ערוץ 16 בסירה', 'green', 30))))
    card('s05_portable', 'המכשיר הנייד', body, 'VHF נייד', 'FM, SIMPLEX, עד חמישה וואט, ובסירת ההצלה ערוץ 16.',
         bg='u13_handheld', pos='50% 40%', shade=0.15)

def s06():
    body = ans('מחפשים את השגויה', 'red', ('✓', 'AM · שגוי, המכשיר ב-FM', 'green', 30), ('✗', 'וואט 1 · נכון, הספק נמוך', 'red', 28),
               ('✗', 'SIMPLEX בלבד · נכון', 'red', 28), ('✗', 'א׳ שגויה · לא ״הכל נכון״', 'red', 28))
    card('s06_g4', 'ההצהרה השגויה', body, 'תשובה א', 'המכשיר הנייד עובד ב-FM, לא ב-AM. זו ההצהרה השגויה.',
         examq(4), bg='u13_handheld', pos='50% 40%', shade=0.2)

def s07():
    body = centered(flow([('MAYDAY · מצוקה · 1', 'red'), ('PAN PAN · דחיפות · 2', 'amber'), ('SECURITE · בטיחות · 3', 'sky')], 36))
    card('s07_priorities', 'העדיפויות בקשר', body, '3 עדיפויות', 'מצוקה היא סכנת חיים מיידית. דחיפות בלי סכנה מיידית. בטיחות היא ניווט ומזג אוויר.',
         bg='u17_tow', shade=0.6)

def s08():
    body = ans('PAN PAN · עדיפות 2', 'amber', ('✓', 'דחיפות · עדיפות שנייה', 'green', 30), ('✗', 'בטיחות · SECURITE, שלישית', 'red', 28),
               ('✗', 'מצוקה · MAYDAY, ראשונה', 'red', 28), ('✗', 'אדם נפל לים · דוגמה, לא הגדרה', 'red', 28))
    card('s08_g9', 'PAN PAN', body, 'תשובה ב', 'PAN PAN הוא כל הודעת דחיפות, בעדיפות שנייה בקשר.',
         examq(9), bg='u17_tow', shade=0.2)

def s09():
    body = ans('SECURITE · בטיחות', 'sky', ('✓', 'בטיחות שייט · אזהרת מזג אוויר', 'green', 30), ('✗', 'אדם בסכנה · דחיפות או מצוקה', 'red', 28),
               ('✗', 'עזרה מיידית · MAYDAY', 'red', 28), ('✗', 'רשימת תעבורה · שגרה', 'red', 28))
    card('s09_g7', 'שלוש פעמים SECURITE', body, 'תשובה א', 'אחרי SECURITE מגיעה הודעה על בטיחות השייט או אזהרת מזג אוויר.',
         examq(7), bg='u14_bridge', shade=0.2)

def s10():
    body = ans('בטיחות = ניווט ומזג אוויר', 'sky', ('✓', 'בטיחות שייט · מטאורולוגיה', 'green', 30), ('✗', 'נפל לים · עדיפות גבוהה יותר', 'red', 28),
               ('✗', 'מצב רפואי · דחיפות, MEDICO', 'red', 28), ('✗', 'א׳ ו-ב׳ שגויות · ג׳ שגויה', 'red', 28))
    card('s10_g14', 'עדיפות בטיחות', body, 'תשובה ד', 'עדיפות בטיחות היא לניווט ולמזג אוויר. אדם במים או מצב רפואי הם עדיפות גבוהה יותר.',
         examq(14), bg='u14_bridge', shade=0.2)

def s11():
    body = ans('כולן PAN PAN', 'amber', ('✓', 'גרירת כלי מוגבל בתנועתו', 'green', 28), ('✓', 'סיוע רפואי לאיש צוות', 'green', 28),
               ('✓', 'בקשה לפינוי רפואי', 'green', 28), ('✓', 'כל התשובות נכונות', 'green', 30))
    card('s11_g18', 'תקשורת דחיפות', body, 'תשובה ד', 'גרירה, סיוע רפואי ופינוי רפואי הם כולם דחיפות.',
         examq(18), bg='u17_tow', shade=0.2)

def s12():
    body = (at(24, 24, chip('קודי השתקה · מצרפתית', 'sky', 34))
            + bottom(rows(('🔇', 'SEELONCE MAYDAY · המפקחת משתיקה', 'red', 28), ('🔇', 'SEELONCE DISTRESS · אחרת משתיקה', 'amber', 28),
                          ('…', 'PRUDONCE · לקראת סיום', 'sky', 28), ('✓', 'SEELONCE FEENEE · הסתיים', 'green', 28))))
    card('s12_silence', 'קודי השתקה', body, 'השתקה', 'SEELONCE FEENEE אומר שהמצוקה הסתיימה, וערוץ 16 חוזר לשגרה.',
         bg='u18_vhf16', shade=0.75)

def s13():
    body = ans('סיום מצוקה', 'green', ('✓', 'SEELONCE FEENEE · הסתיים', 'green', 30), ('✗', 'SEELONCE MAYDAY · משתיק באמצע', 'red', 28),
               ('✗', 'SEELONCE DISTRESS · תחנה אחרת', 'red', 28), ('✗', 'SEELONCE OUT · לא קיים', 'red', 28))
    card('s13_g10', 'סיום מצוקה', body, 'תשובה ב', 'SEELONCE FEENEE מסיים את המצוקה. השאר משתיקים, או לא קיימים.',
         examq(10), bg='u18_vhf16', shade=0.2)

def s14():
    body = (at(24, 24, chip('AIS · משדרת לבד ב-VHF', 'sky', 34))
            + bottom(rows(('ID', 'שם · MMSI', 'sky', 30), ('⌖', 'מיקום · קורס · מהירות', 'green', 30),
                          ('⚠', 'מטרה · למנוע התנגשות', 'amber', 30))))
    card('s14_ais', 'AIS', body, 'זיהוי אוטומטי', 'כל ספינה משדרת מי היא ומה היא עושה, וכולם רואים אותה על הפלוטר או על המכ״מ.',
         bg='u16_ships', shade=0.3)

def s15():
    body = ans('AIS', 'sky', ('✓', 'AUTOMATIC IDENTIFICATION SYSTEM', 'green', 26), ('✗', 'AUTO INSERT SIGNAL · לא קיים', 'red', 26),
               ('✗', 'INFORMATION · לא, היא מזהה', 'red', 26), ('✗', 'יש תשובה נכונה', 'red', 26))
    card('s15_g5', 'מה פירוש AIS', body, 'תשובה ב', 'Automatic Identification System. מערכת זיהוי אוטומטית.',
         examq(5), bg='u16_ships', shade=0.2)

def s16():
    body = centered(flow([('VITAL · משודרת מיד', 'red'), ('IMPORTANT · בחלון הפנוי הראשון', 'amber'), ('ROUTINE · בשידור המתוכנן הבא', 'sky')], 34))
    card('s16_navtex', 'עדיפות ב-NAVTEX', body, '3 רמות', 'כל הודעת NAVTEX מקבלת אחת משלוש רמות, והן קובעות מתי היא משודרת.',
         bg='u15_navtex_pro', shade=0.6)

def s17():
    body = ans('NAVTEX · 3 רמות', 'amber', ('✓', 'VITAL · IMPORTANT · ROUTINE', 'green', 30), ('✗', 'Distress · Urgency · Safety · קול', 'red', 26),
               ('✗', 'עדיפות זהה · לא, VITAL מיד', 'red', 28), ('✗', 'יש תשובה נכונה', 'red', 28))
    card('s17_g13', 'רמות NAVTEX', body, 'תשובה א', 'ב-NAVTEX: VITAL, IMPORTANT ו-ROUTINE. מצוקה, דחיפות ובטיחות הן של הקשר הקולי.',
         examq(13), bg='u15_navtex_pro', shade=0.2)

def s18():
    body = (at(24, 24, chip('יומן הרדיו · של התחנה', 'green', 34))
            + bottom(rows(('✎', 'בדיקות ציוד', 'sky', 30), ('✎', 'מצוקה · דחיפות · בטיחות', 'amber', 30),
                          ('⌂', 'נשמר ליד התחנה', 'green', 30))))
    card('s18_log', 'יומן הרדיו', body, 'יומן', 'היומן שייך לתחנה, ולכן נשמר במקום שבו מפעילים אותה. ביאכטה, ליד המכשיר.',
         bg='u17_logbook', shade=0.15)

def s19():
    body = ans('איפה היומן', 'green', ('✓', 'במקום הפעלת התחנה', 'green', 30), ('✗', 'משרד רב החובל · לא זמין', 'red', 28),
               ('✗', 'חדר המפעיל · לא בהכרח התחנה', 'red', 28), ('✗', 'בכל מקום · לא, ליד התחנה', 'red', 28))
    card('s19_g12', 'היכן נשמר היומן', body, 'תשובה ג', 'היומן נשמר במקום שבו מפעילים את התחנה, כדי שיהיה זמין לרישום.',
         examq(12), bg='u17_logbook', shade=0.2)

MMSI = ('<div class="ltr font-mono text-[44px] leading-snug text-emerald-200 p-6 space-y-3">'
        '<div><span class="text-amber-300 font-bold">428</span>xxxxxx <span class="text-white text-[30px]">· ספינה · ישראל</span></div>'
        '<div><span class="text-amber-300 font-bold">232</span>xxxxxx <span class="text-white text-[30px]">· ספינה · בריטניה</span></div>'
        '<div><span class="text-sky-300 font-bold">0</span>428xxxxx <span class="text-white text-[30px]">· קבוצה</span></div>'
        '<div><span class="text-rose-300 font-bold">00</span>428xxxx <span class="text-white text-[30px]">· תחנת חוף</span></div></div>')

def s20():
    body = at(24, 24, chip('MMSI · 9 ספרות', 'green', 34)) + bottom(glass(MMSI))
    card('s20_mmsi', 'MMSI', body, '9 ספרות', 'שלוש הראשונות הן קוד המדינה, MID. ספינה מתחילה בקוד, בלי אפס.',
         bg='u13_vhf', shade=0.75)

def s21():
    body = ans('ספינה · 9 ספרות, בלי אפס', 'green', ('✓', '232000432 · 9 ספרות, בריטניה', 'green', 30), ('✗', '42800501 · רק 8 ספרות', 'red', 28),
               ('✗', '042811111 · אפס = קבוצה', 'red', 28), ('✗', 'א׳ שגויה · א+ב שגויה', 'red', 28))
    card('s21_g20', 'זיהוי של ספינה', body, 'תשובה ב', 'MMSI של ספינה: תשע ספרות, ומתחיל בקוד מדינה.',
         examq(20), bg='u13_vhf', shade=0.2)

def s22():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u17_vhf_call', focus=(0.5, 0.45))
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['16 · קריאה, מצוקה, דחיפות, בטיחות', '15 ו-17 · וואט אחד', 'נייד · FM ו-SIMPLEX', 'PAN PAN · דחיפות, עדיפות 2',
             'SECURITE · בטיחות ומזג אוויר', 'SEELONCE FEENEE · סיום מצוקה', 'AIS · זיהוי אוטומטי', 'NAVTEX · VITAL, IMPORTANT, ROUTINE',
             'יומן · ליד התחנה', 'MMSI · 9 ספרות, קוד מדינה']
    for i, s in enumerate(items):
        y = 360 + i * 98
        d.rounded_rectangle((1360, y, 2460, y + 82), 20, fill=PANEL)
        dot(d, (2420, y + 41), 12, GREEN_L if i < 5 else C.ORANGE)
        text_r(d, 2380, y + 16, s, F(42, False), TEXT)
    save(im, 's22_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22]

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:                              # OneDrive can lock a freshly written PNG
                    import time; time.sleep(2)
