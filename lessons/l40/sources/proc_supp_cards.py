"""l40 lesson: נהלים ופונטיקה - השלמות למבחן (phonetics, calling, priorities, distress terms).
Same look as dsc_supp_cards.py. Each exam question = 3 cards: <sid>_ask, <sid>_a_q (copy of _ask), <sid> (answer).
Options and the correct letter come from data/l40.json; only head/text/background are set here."""
import os, sys, re, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import equip_cards as E
from equip_cards import C, S, info, summary, F, text_c, base, photo, save, TEXT, GREEN, BLUE_L, RC

NAME = 'נהלים ופונטיקה - השלמות למבחן'
HERE = os.path.dirname(os.path.abspath(__file__))
C.OUT = os.path.join(HERE, '..', 'cards', NAME); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'קורס GMDSS · נהלים ופונטיקה'

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
    text_c(d, RC, 520, 'נהלים ופונטיקה', F(124), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['אלפבית פונטי', 'קריאה לתחנה', 'עדיפויות בקשר', 'מונחי מצוקה']):
        text_c(d, RC, 810 + i * 84, s, F(52, False), TEXT)
    save(im, 's01_intro')

ALPHA = ['Alfa', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliett', 'Kilo', 'Lima', 'Mike',
         'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra', 'Tango', 'Uniform', 'Victor', 'Whiskey', 'X-ray', 'Yankee', 'Zulu']

def s02_alpha():
    """Whole 26-letter table on one card (display only, not read aloud)."""
    im, d = C.base()
    C.text_c(d, 1280, 36, 'האלפבית הפונטי', F(84), TEXT)
    d.rounded_rectangle((1200, 142, 1360, 152), 5, fill=GREEN)
    cw, gap, y0, rh, rg = 760, 60, 190, 84, 10
    xs = [1280 - gap / 2 - cw, 1280 + gap / 2]
    for i, w in enumerate(ALPHA):
        col, row = divmod(i, 13)
        x = xs[col]; y = y0 + row * (rh + rg)
        d.rounded_rectangle((x, y, x + cw, y + rh), 18, fill=C.PANEL)
        C.text_c(d, x + 90, y + 8, w[0], F(60), GREEN)
        C.text_c(d, x + 90 + (cw - 90) / 2, y + 12, w, F(52, False), TEXT)
    C.save(im, 's02_alpha')

def s02_phonetic():
    info('s02_phonetic', 'אלפבית פונטי', 'ספרות לפי ITU', 'sky',
         [('0', 'אפס · NADAZERO', 'green', 30), ('1', 'אחד · UNAONE', 'green', 30), ('2', 'שניים · BISSOTWO', 'green', 30), ('3', 'שלוש · TERRATHREE', 'green', 30),
          ('4', 'ארבע · KARTEFOUR', 'green', 30), ('5', 'חמש · PANTAFIVE', 'green', 30), ('6', 'שש · SOXISIX', 'green', 30), ('7', 'שבע · SETTESEVEN', 'green', 30),
          ('8', 'שמונה · OKTOEIGHT', 'green', 30), ('9', 'תשע · NOVENINE', 'green', 30)],
         'ספרות ואותיות', 'אותיות בשם הרגיל. ספרות בצורה של ITU.', 'u16_vhf_ais', shade=0.3)

def s03_q4005(): qc('s03_q4005', 'עשר PM', 4005, 'פונטי', 'אחד, אפס ואחר כך האותיות P ו-M.', 'u16_vhf_ais')
def s04_q4137(): qc('s04_q4137', 'ארבע X S Q', 4137, 'פונטי', 'ארבע היא KARTEFOUR.', 'u16_vhf_ais')
def s05_q4177(): qc('s05_q4177', 'M B P שלוש', 4177, 'פונטי', 'אותיות בשם הרגיל, ספרה בצורת ITU.', 'u16_vhf_ais')
def s06_q4202(): qc('s06_q4202', 'J A N 23', 4202, 'פונטי', 'J היא JULIET. שתיים ושלוש: BISSOTWO ו-TERRATHREE.', 'u16_vhf_ais')
def s07_q4108(): qc('s07_q4108', 'AIS CH 87B', 4108, 'פונטי', 'כל אות בשמה, הספרות בצורה הפונטית.', 'u16_vhf_ais')
def s08_q4167(): qc('s08_q4167', 'CH 87B', 4167, 'פונטי', 'CHARLIE HOTEL OKTOEIGHT SETTESEVEN BRAVO.', 'u16_vhf_ais')

def s09_call():
    info('s09_call', 'קריאה לתחנה', 'מלאה ומקוצרת', 'sky',
         [('3×', 'מלאה: שם התחנה ×3 · THIS IS · שם הספינה ×3', 'green', 28), ('1×', 'מקוצרת: שם התחנה ×1 · THIS IS · שם הספינה ×2 · OVER', 'green', 28),
          ('📻', 'תחנת חוף: שם העיר + RADIO', 'green', 28)],
         'איך קוראים', 'תחנת חוף נקראת בשם העיר ואחריו RADIO, כמו HAIFA RADIO.', 'l40_handheld', shade=0.3)

def s10_q4116(): qc('s10_q4116', 'קריאה מקוצרת', 4116, 'מקוצרת', 'תחנה פעם אחת, THIS IS, ושמך פעמיים.', 'l40_handheld')
def s11_q4088(): qc('s11_q4088', 'קריאה בערוץ 16', 4088, 'מקוצרת', 'קוראים לתחנה פעם אחת ומזדהים פעמיים.', 'l40_handheld')
def s12_q4029(): qc('s12_q4029', 'קריאה לתחנת חוף', 4029, 'שם העיר + RADIO', 'הביטוי הוא תמיד שם העיר ו-RADIO.', 'l40_rcc')
def s13_q4170(): qc('s13_q4170', 'שיחות בתשלום', 4170, 'תחנת חוף', 'VARNA RADIO היא תחנת חוף.', 'l40_rcc')
def s14_q4105(): qc('s14_q4105', 'לא קלטת את הזיהוי', 4105, 'מבקשים לחזור', 'STATION CALLING NUMA, REPEAT YOUR CALL.', 'l40_signal')
def s15_q4109(): qc('s15_q4109', 'מי מפקח', 4109, 'המוען מנהל', 'המוען של הקריאה מנהל את הקשר.', 'l40_signal')
def s16_q4129(): qc('s16_q4129', 'מונחי רדיוטלפון', 4129, 'מונח מקובל', 'STAND-BY.', 'l40_signal')
def s17_q4009(): qc('s17_q4009', 'MY ETA', 4009, 'ETA', 'ETA = ESTIMATED TIME OF ARRIVAL.', 'l40_signal')
def s18_q4102(): qc('s18_q4102', 'TR', 4102, 'שגרה', 'TR הוא דיווח מסע, בעדיפות שגרה.', 'l40_signal')
def s19_q4002(): qc('s19_q4002', 'הודעת בטיחות', 4002, 'ביומן + איש משמרת', 'רושמים ביומן ומוסרים לאיש המשמרת.', 'l40_cockpit')

def s20_priorities():
    info('s20_priorities', 'עדיפויות בקשר', 'שלוש עדיפויות', 'sky',
         [('1', 'מצוקה · MAYDAY', 'red', 32), ('2', 'דחיפות · PAN PAN', 'amber', 32), ('3', 'בטיחות · SECURITE', 'green', 32)],
         'מי קודם', 'כל קריאה נאמרת שלוש פעמים. דחיפות: בקשת גרירה. בטיחות: ניווט ומזג אוויר.', 'l40_cockpit', shade=0.3)

def s21_q4062(): qc('s21_q4062', 'SECURITE', 4062, 'עדיפות שלישית', 'SECURITE היא עדיפות שלישית.', 'l40_cockpit')
def s22_q4069(): qc('s22_q4069', 'PAN PAN', 4069, 'בקשה לגרירה', 'בקשת גרירה היא PAN PAN.', 'l40_cockpit')
def s23_q4074(): qc('s23_q4074', 'SECURITE', 4074, 'בטיחות השייט', 'ניווט ומזג אוויר.', 'l40_cockpit')
def s24_q4092(): qc('s24_q4092', 'עדיפות דחיפות', 4092, 'דחיפות', 'בטיחות של כלי נייד או אדם, בלי סכנה מיידית.', 'l40_cockpit')
def s25_q4113(): qc('s25_q4113', 'MEDICAL ADVICE', 4113, 'ייעוץ רפואי', 'פינוי הוא MEDICAL EVACUATION.', 'l40_handheld')
def s26_q4031(): qc('s26_q4031', 'DISABLED AND ADRIFT', 4031, 'ללא שליטה', 'ללא שליטה, בסכנה, או שזקוק לגרירה דחופה.', 'l40_handheld')

def s27_mayday_terms():
    info('s27_mayday_terms', 'מונחי מצוקה', 'שלושה מונחים', 'sky',
         [('1', 'PRUDONCE · זהירות, המצוקה לקראת סיום', 'green', 28), ('2', 'RECEIVED MAYDAY · תחנה מאשרת שקלטה מצוקה', 'green', 28),
          ('3', 'UNDESIGNATED · בלי סוג מצוקה', 'green', 28)],
         'מונחי מצוקה', 'UNDESIGNATED: המפעיל לחץ מהר על כפתור המצוקה.', 'l40_rcc', shade=0.3)

def s28_q4013(): qc('s28_q4013', 'מונחי מצוקה', 4013, 'PRUDONCE', 'PAN PAN הוא דחיפות, לא מצוקה.', 'l40_rcc')
def s29_q4145(): qc('s29_q4145', 'RECEIVED MAYDAY', 4145, 'אישור קליטה', 'תחנה מאשרת קבלת התרעת מצוקה.', 'l40_rcc')
def s30_q4143(): qc('s30_q4143', 'UNDESIGNATED', 4143, 'ב׳ וג׳ אפשריות', 'לחיצה מהירה, או התרעת שווא.', 'l40_cockpit')
def s31_q4124(): qc('s31_q4124', 'UNDESIGNATED ב-DSC', 4124, 'א׳ וג׳ נכונות', 'התרעת שווא, או מצוקה אמיתית בלחיצה מהירה.', 'l40_cockpit')
def s32_q4144(): qc('s32_q4144', 'תגובה', 4144, 'ממתינים', 'ממתינים כחמש דקות לרשות חופית, ואז מנסים קשר.', 'l40_cockpit')
def s33_q4154(): qc('s33_q4154', 'חפץ צף', 4154, 'ALL STATIONS', 'הודעת בטיחות לכולם.', 'l40_signal')
def s34_q4104(): qc('s34_q4104', 'פרסום', 4104, 'LIST OF COAST STATIONS', 'פרטים על תחנות חוף.', 'l40_rcc')
def s35_q4153(): qc('s35_q4153', 'סימן זיהוי', 4153, 'שם של כלי שיט', 'שם בלי RADIO הוא כלי שיט.', 'l40_signal')
def s36_q4209(): qc('s36_q4209', 'HAIFA, CYPRUS...', 4209, 'כלי שיט', 'HAIFA לבד: ספינה. HAIFA RADIO: תחנת חוף.', 'l40_signal')

def s37_summary():
    summary('s37_summary', 'u16_vhf_ais', ['ספרות · NADAZERO, UNAONE, KARTEFOUR', 'מקוצרת · תחנה פעם, ושמך פעמיים', 'תחנת חוף · שם העיר + RADIO',
             'MAYDAY · PAN PAN · SECURITE', 'בקשת גרירה · PAN PAN', 'הודעת בטיחות · ביומן + איש משמרת', 'PRUDONCE · RECEIVED MAYDAY', 'UNDESIGNATED · בלי סוג מצוקה'])

def s04_callsign():
    info('s04_callsign', 'אות קריאה', 'הקידומת של ישראל', 'sky',
         [('✓', '4X · אות הקריאה הבינלאומי של ישראל', 'green', 32), ('✓', 'ITU · הקידומת נקבעה על ידי איגוד התקשורת הבינלאומי', 'green', 28),
          ('⚓', 'זיהוי רשמי של כלי שיט ומטוסים אזרחיים הרשומים בישראל', 'green', 28)],
         '4X', 'אות קריאה (Call Sign) הוא סימן זיהוי רשמי.', 'u16_ships', shade=0.3)

def s16_words():
    info('s16_words', 'מונחי רדיוטלפון', 'מונחים מקובלים', 'sky',
         [('1', 'OVER · סיימתי לדבר, ממתין לתשובה', 'green', 28), ('2', 'OUT · הקשר הסתיים, אין צורך בתשובה', 'green', 28),
          ('3', 'ROGER · קיבלתי והבנתי', 'green', 28), ('4', 'STAND-BY · המתן', 'green', 28),
          ('5', 'ETA · זמן הגעה משוער', 'green', 28), ('6', 'TR · דיווח מסע, שגרה', 'green', 28)],
         'מונחים', 'OVER AND OUT הוא ביטוי שגוי: שני הדברים יחד.', 'l40_handheld', shade=0.3)

def s25_medical_terms():
    info('s25_medical_terms', 'מצוקה רפואית ותקלה', 'שלושה מונחים', 'sky',
         [('1', 'MEDICAL ADVICE · ייעוץ רפואי מהחוף', 'green', 28), ('2', 'MEDICAL EVACUATION · פינוי רפואי', 'green', 28),
          ('3', 'DISABLED AND ADRIFT · בלי שליטה, נסחף', 'green', 28)],
         'מונחים', 'ייעוץ הוא לא פינוי.', 'l40_handheld', shade=0.3)

def s33_pubs():
    info('s33_pubs', 'פרסומים', 'ALL STATIONS ופרסומים', 'sky',
         [('✓', 'ALL STATIONS · פנייה לכל התחנות', 'green', 28), ('📘', 'LIST OF COAST STATIONS · תחנות חוף', 'green', 28),
          ('📒', 'GMDSS RADIO LOGBOOK · יומן הרדיו', 'green', 28), ('🚩', 'INTERNATIONAL CODE OF SIGNALS · ספר האותות', 'green', 28)],
         'פרסומים', 'כל פרסום משרת מטרה אחרת.', 'l40_rcc', shade=0.3)

ALL = [v for k, v in sorted(globals().items()) if re.match(r's\d\d_', k) and callable(v)]

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:
                    import time; time.sleep(2)
