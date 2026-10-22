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

def s15_header():
    info('s15_header', 'הודעת NAVTEX', 'מבנה ההודעה', 'sky',
         [('Z', 'ZCZC · תחילת ההודעה', 'green', 28), ('1', 'B1 · אות התחנה', 'green', 28), ('2', 'B2 · אות סוג ההודעה', 'green', 28),
          ('3', 'B3 B4 · מספר סידורי', 'green', 28), ('4h', 'כל תחנה משדרת פעם בארבע שעות', 'green', 28)],
         'מבנה', 'המקלט זוכר קוד הודעה ולא מדפיס אותה שוב.', 'l40_world_a1a2', shade=0.3)

def s15_q4138(): qc('s15_q4138', 'מחזורי שידור', 4138, '4 תחנות', '4 תחנות × 6 שידורים ביממה = 24.', 'l40_world_a1a2')
def s16_q4126(): qc('s16_q4126', 'מחיקת קוד', 4126, 'קליטה חוזרת', 'כדי לקלוט שוב הודעה שנקלטה שגויה.', 'l40_world_a1a2')

def s17_cer():
    info('s17_cer', 'CER', 'שיעור שגיאות', 'sky',
         [('%', 'CER · Character Error Rate', 'green', 28), ('✓', 'אחוז התווים השגויים בהודעה', 'green', 28)],
         'C E R', 'שגיאות בהודעה, ואחוזן.', 'l40_world_a1a2', shade=0.3)

def s17_q4191(): qc('s17_q4191', 'CER 6%', 4191, 'קליטה חוזרת', 'תיקלט שוב בעוד ארבע שעות.', 'l40_world_a1a2')

def s18_codes():
    info('s18_codes', 'אותיות סוג הודעה', 'B2', 'sky',
         [('A', 'אזהרות ניווט', 'green', 28), ('B', 'אזהרות מטאורולוגיות', 'green', 28), ('D', 'חיפוש והצלה', 'green', 28),
          ('L', 'אזהרות ניווט נוספות', 'green', 28), ('00', 'מספר 00 · הודעה דחופה', 'amber', 28)],
         'סוגי הודעות', 'A, B, D ו-L אי אפשר לדחות. גם 00 לא.', 'l40_world_a1a2', shade=0.3)

def s18_q4151(): qc('s18_q4151', 'האות D', 4151, 'חיפוש והצלה', 'D: בקשת סיוע בחיפוש והצלה.', 'l40_rcc')
def s19_q4027(): qc('s19_q4027', 'MAYDAY RELAY', 4027, 'NAVTEX', 'ממסר מצוקה משודר ב-NAVTEX.', 'l40_rcc')
def s20_q4117(): qc('s20_q4117', 'הקוד L D 00', 4117, 'לא ניתן לדחות', 'סוג D, מספר 00: לא ניתן לדחות.', 'l40_world_a1a2')
def s21_q4042(): qc('s21_q4042', 'הודעת בטיחות', 4042, 'א׳ וג׳', 'קוד L, או התקרבות סערה טרופית.', 'l40_cockpit')
def s22_q4093(): qc('s22_q4093', 'אות בטיחות', 4093, 'מטאורולוגיה וניווט', 'אזהרות מטאורולוגיות או אזהרות ניווט.', 'l40_cockpit')

def s23_summary():
    summary('s23_summary', 'u16_vhf_ais', ['NAVTEX · MSI בגל קרקע', '518 · אנגלית  |  490 · לאומית', '4209.5 · HF', 'טווח 200 עד 400 מייל',
             '21 אזורי NAVAREA', '4 תחנות × 6 = 24 מחזורים', 'CER · שגיאות, תיקלט שוב', 'A, B, D, L ו-00 · לא ניתן לדחות'])

ALL = [v for k, v in sorted(globals().items()) if re.match(r's\d\d_', k) and callable(v)]

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:
                    import time; time.sleep(2)
