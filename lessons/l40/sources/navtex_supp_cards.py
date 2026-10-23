"""l40 lesson: NAVTEX - השלמות למבחן (phonetics, calling, priorities, distress terms).
Same look as dsc_supp_cards.py. Each exam question = 3 cards: <sid>_ask, <sid>_a_q (copy of _ask), <sid> (answer).
Options and the correct letter come from data/l40.json; only head/text/background are set here."""
import os, sys, re, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import equip_cards as E
from equip_cards import C, S, info, summary, F, text_c, base, photo, save, TEXT, GREEN, BLUE_L, RC

NAME = 'NAVTEX - השלמות למבחן'
HERE = os.path.dirname(os.path.abspath(__file__))
C.OUT = os.path.join(HERE, '..', 'cards', NAME); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'קורס GMDSS · NAVTEX'

def short(t, n=46):
    t = re.sub(r'\s+', ' ', t).strip()
    return t if len(t) <= n else t[:n - 1].rstrip() + '…'

def qc(sid, caption, num, head, text, bg, tone='green', good=None, bads=None, extra=None):
    """Question card trio. good/bads default to the bank options (letter stripped, shortened)."""
    q, letter = E.bankq(num)
    E.card(sid + '_ask', caption, E.at(24, 24, E.chip('שאלה מהמבחן', 'sky', 34)), 'שאלה מהמבחן', '', (q[0], q[1], q[2], -1), bg=bg, pos='center', shade=0.2)
    shutil.copyfile(os.path.join(C.OUT, sid + '_ask.png'), os.path.join(C.OUT, sid + '_a_q.png'))
    opts = q[2]; k = q[3]
    g = good or short(opts[k]); bs = bads if bads is not None else [short(o) for i, o in enumerate(opts) if i != k]
    rs = [('✓', g, 'green', 30)] + [('✗', b, 'red', 28) for b in bs]
    if extra: rs = extra
    E.card(sid, caption, E.ans(head, tone, *rs), 'תשובה ' + letter, text, q, bg=bg, pos='center', shade=0.2)

def s01_intro():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u16_ships', focus=(0.5, 0.5))
    text_c(d, RC, 380, 'קורס GMDSS · מבחן משרד התקשורת', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'NAVTEX', F(124), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['תדרים ואזורים', 'קודי הודעה', 'מחזורי שידור', 'MSI ו-NAVAREA']):
        text_c(d, RC, 810 + i * 84, s, F(52, False), TEXT)
    save(im, 's01_intro')

def s02_basics():
    info('s02_basics', 'NAVTEX', 'שירות MSI', 'sky',
         [('1', '518 kHz · אנגלית (בינלאומי)', 'green', 28), ('2', '490 kHz · שפה לאומית', 'green', 28), ('3', '4209.5 kHz · HF', 'green', 28),
          ('4', 'טווח 200 עד 400 מייל ימי', 'green', 28), ('5', 'גל קרקע, MF', 'green', 28), ('6', '21 אזורי NAVAREA', 'green', 28)],
         'NAVTEX', 'MSI: מידע בטיחות ימי. התחנות משדרות והמקלט מדפיס.', 'l40_world_a1a2', shade=0.3)

def s03_q4196(): qc('s03_q4196', 'שירות כללי', 4196, 'MSI', 'MSI הוא שירות מידע הבטיחות הימי.', 'l40_world_a1a2')
def s04_q4101(): qc('s04_q4101', 'מקלט MSI', 4101, 'NAVTEX', 'מקלט ה-NAVTEX מספק MSI.', 'l40_world_a1a2')
def s05_q4182(): qc('s05_q4182', 'תפקיד NAVTEX', 4182, 'A1, A2, A4', 'MSI לאזורי A1, A2 ו-A4.', 'l40_world_a1a2')
def s06_q4149(): qc('s06_q4149', 'כיסוי A1 ו-A2', 4149, 'NAVTEX', 'NAVTEX ו-MSI מכסים A1 ו-A2.', 'l40_world_a1a2')
def s07_q4017(): qc('s07_q4017', '170 מייל מהחוף', 4017, 'טווח NAVTEX', 'סביר שנהיה בטווח תחנת NAVTEX.', 'l40_world_a1a2')
def s08_q4188(): qc('s08_q4188', 'כיסוי תחנה', 4188, 'הטווח', '200 עד 400 מייל ימי.', 'l40_world_a1a2')
def s09_q4081(): qc('s09_q4081', 'גל קרקע', 4081, '518 kHz', '518 kHz מתפשט בגל קרקע.', 'l40_world_a1a2')
def s10_q4106(): qc('s10_q4106', 'תדר HF', 4106, '4209.5 kHz', 'זה תדר ה-HF של NAVTEX.', 'l40_world_a1a2')
def s11_q4044(): qc('s11_q4044', 'ההצהרה השגויה', 4044, 'שאלת שלילה', '406 הוא מגה הרץ ושל משואה.', 'l40_world_a1a2')
def s12_q4089(): qc('s12_q4089', 'שפה יוונית', 4089, '490 kHz', 'בתדר 490 משדרים בשפה לאומית.', 'l40_world_a1a2')
def s13_q4071(): qc('s13_q4071', 'אזורי NAVAREA', 4071, '21', 'העולם מחולק ל-21 אזורים.', 'l40_world_a1a2')

def s14_alrs():
    info('s14_alrs', 'פרסום', 'ADMIRALTY', 'sky',
         [('📘', 'ADMIRALTY LIST OF RADIO SIGNALS', 'green', 28), ('5', 'כרך 5 · שירותי GMDSS', 'green', 28), ('📡', 'כולל פרטים על תחנות NAVTEX', 'green', 28)],
         'איפה מחפשים', 'כרך 5 הוא הספר של GMDSS.', 'l40_rcc', shade=0.3)

def s14_q4021(): qc('s14_q4021', 'פרסום', 4021, 'כרך 5', 'ADMIRALTY, כרך 5.', 'l40_rcc')

def s15_q4138(): qc('s15_q4138', 'מחזורי שידור', 4138, '4 תחנות', '4 תחנות × 6 שידורים ביממה = 24.', 'l40_world_a1a2')
def s16_q4126(): qc('s16_q4126', 'מחיקת קוד', 4126, 'קליטה חוזרת', 'כדי לקלוט שוב הודעה שנקלטה שגויה.', 'l40_world_a1a2')

def s17_q4191(): qc('s17_q4191', 'CER 6%', 4191, 'קליטה חוזרת', 'תיקלט שוב בעוד ארבע שעות.', 'l40_world_a1a2')

def s18_q4151(): qc('s18_q4151', 'האות D', 4151, 'חיפוש והצלה', 'D: בקשת סיוע בחיפוש והצלה.', 'l40_rcc')
def s19_q4027(): qc('s19_q4027', 'MAYDAY RELAY', 4027, 'NAVTEX', 'ממסר מצוקה משודר ב-NAVTEX.', 'l40_rcc')
def s20_q4117(): qc('s20_q4117', 'הקוד L D 00', 4117, 'לא ניתן לדחות', 'סוג D, מספר 00: לא ניתן לדחות.', 'l40_world_a1a2')
def s21_q4042(): qc('s21_q4042', 'הודעת בטיחות', 4042, 'א׳ וג׳', 'קוד L, או התקרבות סערה טרופית.', 'l40_cockpit')
def s22_q4093(): qc('s22_q4093', 'אות בטיחות', 4093, 'מטאורולוגיה וניווט', 'אזהרות מטאורולוגיות או אזהרות ניווט.', 'l40_cockpit')

def s23_summary():
    summary('s23_summary', 'u16_vhf_ais', ['NAVTEX · MSI בגל קרקע', '518 · אנגלית  |  490 · לאומית', '4209.5 · HF', 'טווח 200 עד 400 מייל',
             '21 אזורי NAVAREA', '4 תחנות × 6 = 24 מחזורים', 'CER · שגיאות, תיקלט שוב', 'A, B, D, L ו-00 · לא ניתן לדחות'])

from PIL import ImageFont, ImageDraw
MONO = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 92)
MONO_S = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 74)
PHOS = (130, 255, 170); PHOS_DIM = (70, 150, 100)

def screen(sid, lines, marks=(), chips=(), title='מקלט NAVTEX', foot=None):
    """NAVTEX receiver mock-up. lines: [(text, color)] in monospace on the green screen.
    marks: [(line, col, n, color)] boxes drawn around n characters; chips: [(text, color)] legend under the screen."""
    im, d = C.base()
    C.text_c(d, 1280, 34, title, F(72), TEXT)
    d.rounded_rectangle((230, 140, 2330, 1350), 50, fill=(28, 34, 46), outline=(70, 84, 110), width=6)
    d.rounded_rectangle((290, 200, 2270, 1010), 28, fill=(6, 22, 14), outline=(30, 80, 52), width=5)
    x0, y0, lh = 350, 236, 112
    cw = d.textlength('M', font=MONO)
    for i, (txt, col) in enumerate(lines):
        d.text((x0, y0 + i * lh), txt, font=MONO, fill=col)
    for ln, c0, n, col in marks:
        d.rounded_rectangle((x0 + c0 * cw + 2, y0 + ln * lh - 6, x0 + (c0 + n) * cw - 2, y0 + ln * lh + 100), 14, outline=col, width=7)
    y = 1030
    for txt, col in chips:
        d.rounded_rectangle((330, y, 2230, y + 70), 20, fill=(20, 28, 44), outline=col, width=5)
        C.text_r(d, 2190, y + 8, txt, F(46, False), TEXT)
        y += 80
    if foot:
        C.text_c(d, 1280, 1290, foot, F(40, False), C.MUTED)
    C.save(im, sid)

def s15_header():
    screen('s15_header', [('ZCZC KA21', PHOS), ('281200 UTC OCT 26', PHOS_DIM), ('NAVAREA III WARNING 123', PHOS_DIM), ('BUOY OFF POSITION. KEEP CLEAR', PHOS_DIM), ('NNNN', PHOS)],
           marks=[(0, 5, 1, C.BLUE_L), (0, 6, 1, C.ORANGE), (0, 7, 2, C.GREEN_L)],
           chips=[('K · B1 · אות התחנה', C.BLUE_L), ('A · B2 · אות סוג ההודעה', C.ORANGE), ('21 · B3 B4 · מספר סידורי', C.GREEN_L)],
           foot='דוגמה להמחשה. ZCZC פותח את ההודעה ו-NNNN סוגר אותה.')

def s17_cer():
    screen('s17_cer', [('ZCZC KA21', PHOS_DIM), ('BUOY OFF POSITION.', PHOS_DIM), ('KEEP CLEAR', PHOS_DIM), ('CER=06%', (255, 190, 80)), ('NNNN', PHOS_DIM)],
           marks=[(3, 0, 7, C.ORANGE)],
           chips=[('C E R · אחוז התווים שנקלטו שגויים', C.ORANGE)],
           foot='בסוף ההודעה. 06% = שישה אחוזים שגיאות.')

def s18_codes():
    screen('s18_codes', [('ZCZC KA21', PHOS), ('ZCZC KB22', PHOS), ('ZCZC KD05', PHOS), ('ZCZC KL07', PHOS), ('ZCZC KD00', (255, 190, 80))],
           marks=[(0, 6, 1, C.GREEN_L), (1, 6, 1, C.GREEN_L), (2, 6, 1, C.GREEN_L), (3, 6, 1, C.GREEN_L), (4, 7, 2, C.ORANGE)],
           chips=[('A אזהרות ניווט · B מטאורולוגיה · D חיפוש והצלה · L ניווט נוספות', C.GREEN_L), ('00 · הודעה דחופה, אי אפשר לדחות', C.ORANGE)],
           title='מקלט NAVTEX · סוגי הודעות', foot='A, B, D ו-L לא נדחות.')


def s04b_areas():
    info('s04b_areas', 'אזורי הפלגה', 'A1 עד A4', 'sky',
         [('A1', 'VHF · 20 עד 30 מייל · DSC', 'green', 28), ('A2', 'MF · 100 עד 150 מייל', 'green', 28), ('A3', 'לוויין אינמרסאט', 'amber', 28), ('A4', 'אזורי הקטבים', 'amber', 28)],
         'אזורי הפלגה', 'NAVTEX ב-MF: מכסה A1 ו-A2.', 'l40_world_a1a2', shade=0.3)

def s08b_waves():
    info('s08b_waves', 'התפשטות גל', 'קרקע ושמיים', 'sky',
         [('MF', 'גל קרקע · עוקב אחרי פני הים', 'green', 28), ('HF', 'גל שמיים · מתנתר מהאטמוספירה', 'green', 28), ('406', 'MHz · משואה דרך לוויין', 'amber', 28)],
         'איך הגל מתפשט', 'MF בגל קרקע, HF בגל שמיים.', 'l40_world_a1a2', shade=0.3)

def s10b_other():
    info('s10b_other', 'לא NAVTEX', 'תדרים אחרים', 'sky',
         [('1', '406 MHz · EPIRB', 'amber', 28), ('2', '121.5 MHz · ביות', 'amber', 28), ('3', 'AIS · VHF · STATIC, DYNAMIC, VOYAGE', 'amber', 28), ('4', 'SART · עונה למכ״ם, לא משדר זיהוי', 'amber', 28)],
         'מערכות אחרות', 'אלה לא תדרי NAVTEX.', 'u16_vhf_ais', shade=0.3)

def s12b_navarea():
    info('s12b_navarea', 'NAVAREA', '21 אזורים', 'sky',
         [('21', 'אזורי NAVAREA בעולם', 'green', 30), ('III', 'ישראל · ים תיכון', 'green', 30), ('📡', 'תחנה מתאמת לכל אזור', 'green', 28)],
         'NAVAREA', 'העולם מחולק ל-21 אזורים, לכל אחד מתאם.', 'l40_world_a1a2', shade=0.3)

def s15b_memory():
    info('s15b_memory', 'זיכרון המקלט', 'קוד הודעה', 'sky',
         [('1', 'כל הודעה נקלטת עם קוד', 'green', 28), ('2', 'קוד שנשמר: ההודעה לא נקלטת שוב', 'green', 28), ('3', 'נקלטה עם שגיאות? מוחקים את הקוד', 'amber', 28)],
         'הזיכרון', 'מחיקת הקוד מאפשרת קליטה חוזרת בשידור הבא.', 'l40_world_a1a2', shade=0.3)

def s18b_relay():
    info('s18b_relay', 'MAYDAY RELAY', 'ממסר מצוקה', 'sky',
         [('📡', 'תחנת חוף שמעה מצוקה', 'amber', 28), ('➜', 'משדרת הלאה ב-NAVTEX', 'green', 28), ('🚢', 'כל ספינה בטווח מקבלת', 'green', 28)],
         'ממסר מצוקה', 'המצוקה מועברת הלאה לכלי שיט בסביבה.', 'l40_rcc', shade=0.3)

def s20b_levels():
    info('s20b_levels', 'שלוש רמות', 'מצוקה, דחיפות, בטיחות', 'sky',
         [('1', 'MAYDAY מצוקה · סכנה חמורה ומיידית', 'red', 28), ('2', 'PAN PAN דחיפות · בטיחות ספינה או אדם', 'amber', 28), ('3', 'SECURITE בטיחות · ניווט ומטאורולוגיה', 'green', 28)],
         'עדיפויות', 'מצוקה, דחיפות, בטיחות.', 'l40_cockpit', shade=0.3)

ALL = [v for k, v in sorted(globals().items()) if re.match(r's\d\d\w*?_', k) and callable(v)]

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:
                    import time; time.sleep(2)
