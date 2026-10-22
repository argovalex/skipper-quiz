"""l40 lesson: ערוצים ו-DSC - השלמות למבחן (channels, MMSI, DSC alerts).
Reuses the helpers and the look of equip_cards.py; exam questions are read from data/l40.json."""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import equip_cards as E
from equip_cards import C, S, qcard, info, summary, F, text_c, base, photo, save, TEXT, GREEN, BLUE_L, RC

_answer_card = qcard
def qcard(sid, caption, num, head, good, bads, text, bg, tone='green', shade=0.2, pos='center', extra=None):
    """Two cards per question: <sid>_q (question only, nothing marked) and <sid> (answer + explanation, green)."""
    q, letter = E.bankq(num)
    E.card(sid + '_ask', caption, E.at(24, 24, E.chip('שאלה מהמבחן', 'sky', 34)), 'שאלה מהמבחן', '', (q[0], q[1], q[2], -1), bg=bg, pos=pos, shade=shade)
    import shutil; shutil.copyfile(os.path.join(C.OUT, sid + '_ask.png'), os.path.join(C.OUT, sid + '_a_q.png'))   # same card while the narrator says 'the correct answer is'
    _answer_card(sid, caption, num, head, good, bads, text, bg, tone, shade, pos, extra)

NAME = 'ערוצים ו-DSC - השלמות למבחן'
HERE = os.path.dirname(os.path.abspath(__file__))
C.OUT = os.path.join(HERE, '..', 'cards', NAME); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'קורס GMDSS · ערוצים ו-DSC'

def s01_intro():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u16_ships', focus=(0.5, 0.5))
    text_c(d, RC, 380, 'קורס GMDSS · מבחן משרד התקשורת', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'ערוצים ו-DSC', F(124), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['ערוצי VHF', 'DUPLEX · דיגיטליים', 'MMSI ו-MID', 'תגובה להתרעות DSC']):
        text_c(d, RC, 810 + i * 84, s, F(52, False), TEXT)
    save(im, 's01_intro')

ROWS = [('06', 'Simplex', 'בטיחות בין ספינות (Intership Safety), חיפוש והצלה (SAR).'),
        ('13', 'Simplex', 'בטיחות ניווט (Bridge-to-bridge), בין גשרים של ספינות.'),
        ('16', 'Simplex', 'ערוץ המצוקה, הבטיחות והקריאה (Distress, Safety & Calling). חובת האזנה מתמדת, בלי DUAL WATCH.'),
        ('70', 'Simplex', 'DSC בלבד (Digital Selective Calling): קריאות מצוקה ושיחות דיגיטליות. אסור לדבר.'),
        ('87B, 88B', 'Simplex', 'AIS 1 ו-AIS 2: איתור וזיהוי אוטומטי. אסור לדבר.'),
        ('15, 17, 75, 76', 'Simplex', 'הספק עד 1 וואט. 15 ו-17: קשר על הסיפון.'),
        ('11, 12, 14', 'Simplex', 'פעולות נמל. 11: כלי שייט קטנים. 12 ו-14: רשויות נמל.'),
        ('01–05, 07, 18–28\n60–66, 78–86', 'Duplex', 'שיחה עם תחנת חוף, פעולות נמל ותקשורת ציבורית. כולל 24, 26, 27, ו-79 לכלי שייט קטנים.'),
        ('08, 67, 69, 72, 73, 77', 'Simplex', 'בין ספינות (Intership).')]
R06, R13, R16, R70, R_AIS, R_PORT, R_HARBOR, R_DUPLEX, R_INTERSHIP = range(9)

def channels_table(sid, hi=()):
    """Whole table on every card; the rows in hi are lit (the rest dim) while the narrator talks about them."""
    im, d = C.base()
    C.text_c(d, 1280, 44, 'טבלת ערוצי קשר ימי נפוצים (VHF)', F(76), TEXT)
    d.rounded_rectangle((1200, 140, 1360, 150), 5, fill=GREEN)
    xr = 2400; cols = [('ערוץ', 560), ('סוג', 360), ('שימוש', 1320)]   # right to left
    y = 176; d.rounded_rectangle((160, y, xr, y + 76), 14, fill=(10, 20, 38))
    x = xr
    for name, w in cols:
        C.text_c(d, x - w / 2, y + 14, name, F(42), BLUE_L); x -= w
    y += 88
    fs_, lh, h = 38, 48, 114
    for i, r in enumerate(ROWS):
        on = i in hi
        d.rounded_rectangle((160, y, xr, y + h), 16, fill=(30, 92, 66) if on else C.PANEL, outline=C.GREEN_L if on else None, width=5)
        col = TEXT if (on or not hi) else (150, 166, 190)
        x = xr
        for (name, w), v in zip(cols, r):
            font = F(fs_, name == 'ערוץ')
            ls = v.split('\n') if '\n' in v else C.wrap(d, v, font, w - 40)[:2]
            for k, ln in enumerate(ls):
                if name == 'שימוש': C.text_r(d, x - 20, y + (h - lh * len(ls)) / 2 + k * lh, ln, font, col)
                else: C.text_c(d, x - w / 2, y + (h - lh * len(ls)) / 2 + k * lh, ln, font, col)
            x -= w
        y += h + 6
    C.save(im, sid)

def s02_channels(): channels_table('s02_channels', (R_DUPLEX,))
def s02_ch70(): channels_table('s02_ch70', (R70, R_AIS))
def s02_dsc(): channels_table('s02_dsc', (R70,))
def s02_ais(): channels_table('s02_ais', (R_AIS,))
def s02_ch17(): channels_table('s02_ch17', (R_PORT,))
def s02_ch11(): channels_table('s02_ch11', (R_HARBOR, R_DUPLEX))
def s02_ch12(): channels_table('s02_ch12', (R_HARBOR,))
def s02_ch16(): channels_table('s02_ch16', (R16,))

def s03_q4019(): qcard('s03_q4019', 'ערוצי DUPLEX', 4019, 'DUPLEX', 'ערוצים 24 ו-27', ['75 ו-76 · מוגבלים, בלי קול', '87B ו-88B · ערוצי AIS', '9 ו-10 · SIMPLEX'],
                       'ערוצי DUPLEX הם ערוצי שיחה עם תחנת חוף.', 'u16_vhf_ais')
def s04_q4205(): qcard('s04_q4205', 'רק DUPLEX', 4205, 'דיבור רק ב-DUPLEX', 'ערוצים 26 ו-27', ['12 ו-14 · נמל, SIMPLEX', '15 ו-17 · קשר פנים, SIMPLEX', 'ד׳ · רק ב׳ נכונה'],
                       'ערוצים 26 ו-27 הם DUPLEX בלבד.', 'u16_vhf_ais')
def s05_q4190(): qcard('s05_q4190', 'קשר עם RCC', 4190, 'ערוצי עבודה', 'ערוצים 25 ו-27', ['10 ו-11 · לא של RCC', '6 ו-8 · לא של RCC', '15 ו-17 · לא של RCC'],
                       'אלה ערוצי עבודה של תחנות חוף ושל ה-RCC.', 'l40_rcc')
def s06_q4015(): qcard('s06_q4015', 'אסור לדבר', 4015, 'ערוצים דיגיטליים', 'ערוצים 70 ו-88B', ['67 ו-73 · מותר לדבר', '11 ו-79 · מותר לדבר', '75 ו-76 · מותר בהספק נמוך'],
                       'ערוצים 70 ו-88B הם דיגיטליים.', 'l40_cockpit')
def s07_q4136(): qcard('s07_q4136', 'אסור לשדר', 4136, 'ערוצי AIS', 'AIS1 ו-AIS2', ['75 ו-76 · הספק נמוך', 'גשר לגשר · ערוץ רגיל', '25 ו-26 · ערוצי שיחה'],
                       'ערוצי AIS אסורים לשידור מכלי שיט.', 'u16_vhf_ais')
def s08_q4131(): qcard('s08_q4131', 'ערוצים דיגיטליים', 4131, 'VHF דיגיטלי', 'ערוצים 70, 87B ו-88B', ['ערוצים דיגיטליים כן קיימים', '16 ו-6 · ערוצי קול', '121.5 · תדר ביות של משואה'],
                       'שלושה ערוצים דיגיטליים במכשיר VHF.', 'u16_vhf_ais')
def s09_q4043(): qcard('s09_q4043', 'כלי שייט קטנים', 4043, 'ערוצים לקטנים', 'ערוצים 11 ו-79', ['75 ו-76 · מוגבלים', '12 ו-14 · נמל', '15 ו-17 · קשר פנים'],
                       'תנועת כלי שייט קטנים בערוצים 11 ו-79.', 'l40_sunset_vhf')
def s10_q4080(): qcard('s10_q4080', 'ערוצי נמל', 4080, '12 · 14 · 20', 'תקשורת עם רשויות נמלים', ['לא כולם PUBLIC CORRESPONDENCE', 'לא כולם DUPLEX', 'ד׳ · ג׳ שגויה'],
                       'ערוצים 12, 14 ו-20 משמשים לרשויות נמל.', 'l40_sunset_vhf')
def s11_q4169(): qcard('s11_q4169', 'בלי DUAL WATCH', 4169, 'ערוץ 16 וערוץ 36', 'ערוצים 16 ו-36', ['16 ו-26 · רגילים', '16 ו-66 · רגילים', '16 ו-86 · רגילים'],
                       'על 16 ו-36 אי אפשר DUAL WATCH. ב-26, 66 ו-86 אפשר.', 'l40_cockpit')
def s12_q4178(): qcard('s12_q4178', 'האזנה בערוץ 16', 4178, 'חובת האזנה', '24 שעות, חוץ מערוצים אחרים', ['6 שעות · לא מספיק', '8 שעות · לא מספיק', 'DSC לא מבטל את ההאזנה'],
                       'חייבים להאזין, כי לא כל ספינה מצוידת ב-DSC.', 'l40_handheld')
def s13_q4054(): qcard('s13_q4054', 'האזנה בערוץ 70', 4054, 'DSC', '24 שעות ביממה', ['4 שעות · לא מספיק', 'רק במצוקה · לא', '8 שעות · לא מספיק'],
                       'ה-DSC חייב להאזין כל הזמן כדי לקלוט התרעות.', 'l40_cockpit')
def s14_q4048(): qcard('s14_q4048', 'אזור A1', 4048, 'הגדרת הטווח', 'ערוץ 70 · DSC', ['ערוץ 16 · קול', '518 kHz · NAVTEX', 'ד׳ · רק ב׳ נכונה'],
                       'טווח A1 מוגדר לפי ערוץ ה-DSC, ערוץ 70.', 'l40_world_a1a2')

ORANGE, BLUE_L2, GREEN_L2, MUTED = C.ORANGE, C.BLUE_L, C.GREEN_L, C.MUTED

def mmsi_card(sid, title, segs, line):
    """segs: [(digits, label, sub, color)] left to right, 9 boxes in all; X = unknown digit."""
    im, d = C.base()
    C.text_c(d, 1280, 60, title, F(96), TEXT)
    d.rounded_rectangle((1200, 190, 1360, 202), 6, fill=GREEN)
    bw, bh, gap, sg = 170, 220, 14, 46
    total = sum(len(g[0]) for g in segs) * bw + sum(len(g[0]) - 1 for g in segs) * gap + (len(segs) - 1) * sg
    x = 1280 + total / 2                       # numbers read left to right: start from the left edge
    x = 1280 - total / 2; y = 380
    for digits, label, sub, col in segs:
        x0 = x
        for ch in digits:
            d.rounded_rectangle((x, y, x + bw, y + bh), 22, fill=C.PANEL, outline=col, width=6)
            C.text_c(d, x + bw / 2, y + 40, ch if ch != 'X' else '?', F(120), TEXT if ch != 'X' else MUTED)
            x += bw + gap
        x -= gap; x1 = x
        d.rounded_rectangle((x0, y + bh + 24, x1, y + bh + 36), 6, fill=col)
        C.text_c(d, (x0 + x1) / 2, y + bh + 60, label, F(52), col)
        if sub: C.text_c(d, (x0 + x1) / 2, y + bh + 130, sub, F(42, False), TEXT)
        x += sg
    C.text_c(d, 1280, 1190, line, F(60, False), TEXT)
    C.save(im, sid)

def s15_mmsi(): mmsi_card('s15_mmsi', 'M M S I · תשע ספרות', [('428', 'MID · קוד המדינה', 'ישראל', BLUE_L2), ('XXXXXX', 'המספר של הספינה', 'שש ספרות', MUTED)],
                          'שלוש הספרות הראשונות הן ה-MID. של ישראל: 428')
def s15_ship(): mmsi_card('s15_ship', 'מספר של ספינה', [('428', 'MID', 'קוד המדינה', BLUE_L2), ('XXXXXX', 'מספר הספינה', 'שש ספרות', GREEN_L2)],
                          'ספינה: MID ואחריו שש ספרות')
def s15_group(): mmsi_card('s15_group', 'מספר של קבוצה', [('0', 'קבוצה', 'אפס אחד', ORANGE), ('428', 'MID', 'קוד המדינה', BLUE_L2), ('XXXXX', 'מספר הקבוצה', 'חמש ספרות', GREEN_L2)],
                           'קבוצה: מתחיל באפס אחד, אחריו MID')
def s15_coast(): mmsi_card('s15_coast', 'מספר של תחנת חוף', [('00', 'תחנת חוף', 'שני אפסים', ORANGE), ('428', 'MID', 'קוד המדינה', BLUE_L2), ('XXXX', 'מספר התחנה', 'ארבע ספרות', GREEN_L2)],
                           'תחנת חוף: מתחיל בשני אפסים, אחריהם MID')
def s15_sar(): mmsi_card('s15_sar', 'מספר של מטוס חיפוש והצלה', [('111', 'מטוס SAR', 'שלוש פעמים אחד', ORANGE), ('428', 'MID', 'קוד המדינה', BLUE_L2), ('XXX', 'מספר המטוס', 'שלוש ספרות', GREEN_L2)],
                         'מטוס: מתחיל בשלוש פעמים אחד, אחריהן MID')

def s15_solve():
    im, d = C.base()
    C.text_c(d, 1280, 60, 'איך מזהים מי קורא', F(96), TEXT)
    d.rounded_rectangle((1200, 190, 1360, 202), 6, fill=GREEN)
    rows_ = [('00', 'תחנת חוף או RCC', '003662345', ORANGE), ('0', 'קבוצה', '036642424', ORANGE),
             ('111', 'מטוס חיפוש והצלה', '111428109', ORANGE), ('MID', 'ספינה', '227428111', BLUE_L2)]
    xr = 2420; cols = [('מתחיל ב', 400), ('מי זה', 800), ('דוגמה מהמבחן', 1000)]
    y = 260; d.rounded_rectangle((140, y, xr, y + 90), 16, fill=(10, 20, 38)); x = xr
    for n, w in cols: C.text_c(d, x - w / 2, y + 14, n, F(48), BLUE_L2); x -= w
    y += 110
    for pre, who, ex, col in rows_:
        d.rounded_rectangle((140, y, xr, y + 190), 22, fill=C.PANEL, outline=col, width=5)
        C.text_c(d, xr - 200, y + 50, pre, F(96), col)
        C.text_c(d, xr - 400 - 400, y + 62, who, F(64), TEXT)
        C.text_c(d, xr - 1200 - 500, y + 55, ex[:len(ex)], F(84, False), TEXT)
        y += 214
    C.text_c(d, 1280, 1290, 'אחרי ההתחלה קוראים את שלוש ספרות ה-MID ומזהים את המדינה', F(54, False), MUTED)
    C.save(im, 's15_solve')

def s16_q4012(): qcard('s16_q4012', 'MMSI ללכטה', 4012, 'MID 227', '227 428 111', ['428 227 111 · MID של ישראל', '972 111 227 · התקן', '970 227 654 · AIS SART'],
                       'ה-MID בא בהתחלה.', 'l40_signal')
def s17_q4186(): qcard('s17_q4186', 'ה-MID', 4186, '234280482', '234', ['428 · סדרה אחרת', '482 · סדרה אחרת', '342 · סדרה אחרת'],
                       'ה-MID הוא שלוש הספרות הראשונות.', 'l40_signal')
def s18_q4185(): qcard('s18_q4185', 'DSC ממטוס SAR', 4185, 'מתחיל ב-111', '111 428 109', ['428 111 109 · MID בהתחלה, ספינה', '970 111 234 · AIS SART', '980 611 109 · קוד אחר'],
                       'שלוש פעמים אחד ואחריהן MID, ככה מזהים מטוס חיפוש.', 'l40_signal')

def s19_q4010(): qcard('s19_q4010', 'התרעת ROUTINE', 4010, 'אסור לשדר', 'ALL STATIONS', ['קבוצה · מותר', 'תחנה בודדת · מותר', 'RCC · מותר'],
                       'שגרה לכל התחנות אסורה.', 'l40_cockpit')
def s20_q4179(): qcard('s20_q4179', 'יוזמת קשר ב-DSC', 4179, 'מתי מותר', 'כלי שייט לכלי שייט · ROUTINE', ['ביטול התרעת שווא · סיום', 'סיום מצוקה · לא לכולם', 'אישור הודעה · תגובה'],
                       'יוזמה היא פנייה בין שתי ספינות בעדיפות שגרה.', 'l40_cockpit')
def s21_q4008(): qcard('s21_q4008', 'מיקום אוטומטי', 4008, 'עדיפויות', 'מצוקה ודחיפות', ['בטיחות · אין מיקום', 'כל ארבע העדיפויות · לא', 'רק מצוקה · לא'],
                       'השאלה חוזרת בשני ניסוחים, והתשובה זהה.', 'l40_cockpit')
def s22_q4036(): qcard('s22_q4036', 'התרעה ל-A1', 4036, 'ציוד שמשדר', 'DSC CONTROLLER', ['NAVTEX · מקלט', 'AIS SART · איתור', 'EPIRB · משדרת ללוויין'],
                       'DSC CONTROLLER משדר התרעות וקריאות לתחנות ייעודיות.', 'l40_cockpit')
def s23_q4146(): qcard('s23_q4146', 'אישור התרעה', 4146, 'איפה מאשרים', 'ערוץ 16', ['ערוץ 6 · גשר לגשר', 'ערוץ 70 · דיגיטלי', 'ערוץ 13 · גשר לגשר'],
                       'מאשרים בדיבור בערוץ 16.', 'l40_handheld')
def s24_q4050(): qcard('s24_q4050', 'דחיפות לכולם', 4050, 'קלטת בערוץ 70', 'עוברים לערוץ 16 ומאזינים', ['לא מאשרים התרעה לכולם', 'אפשר לקלוט דחיפות', 'לא ממתינים בערוץ 70'],
                       'אותו כלל חל על התרעת בטיחות לכל התחנות.', 'l40_handheld')
def s25_q4134(): qcard('s25_q4134', 'תגובה לדחיפות', 4134, 'מה עושים', 'ממתינים בערוץ 16', ['לא שולחים אישור לתחנה', 'לא שולחים אישור ל-RCC', 'לא משדרים PAN PAN'],
                       'ממתינים בהאזנה לפרטי ההודעה.', 'l40_handheld')
def s26_q4176(): qcard('s26_q4176', 'זיהוי ספרתי', 4176, '003662345 קורא ל-036642424', '', [],
                       '00 הוא תחנת חוף או RCC. 0 אחד הוא קבוצה. MID 366 בשניהם.', 'l40_rcc',
                       extra=[('✓', 'RCC 2345 קורא לקבוצה 42424', 'green', 30), ('✗', 'היעד קבוצה, לא ספינה', 'red', 28),
                              ('✗', 'לא כל ספינות MID 366', 'red', 28), ('✗', 'הקורא תחנה, לא ספינה', 'red', 28)])
def s27_q4132(): qcard('s27_q4132', 'SECONDARY ALERT', 4132, 'שאלת שלילה', '', [],
                       'ג׳ שגויה, כי התרעה משנית היא לא כל התרעה ב-DSC. לכן ד׳.', 'l40_cockpit',
                       extra=[('✓', 'ד׳ · ג׳ אינה נכונה', 'green', 30), ('✗', 'ג׳ · כל התרעה דיגיטלית', 'red', 28)])

def s28_summary():
    summary('s28_summary', 'u16_vhf_ais', ['70, 87B ו-88B · דיגיטליים', '11 ו-79 · כלי שייט קטנים', '12 ו-14 · נמלים', '24, 26, 27 · DUPLEX',
             'ערוץ 16 ו-70 · 24 שעות', 'MID · שלוש ספרות', 'מטוס SAR · 111', 'התרעה לכולם · לערוץ 16'])

ALL = [v for k, v in sorted(globals().items()) if re.match(r's\d\d_', k) and callable(v)]

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:
                    import time; time.sleep(2)
