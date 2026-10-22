"""l40 lesson: ציוד ובדיקות GMDSS (SART, satellites, EPIRB, AIS, batteries, daily checks).
Same look and helpers as solve_cards.py; the exam questions are read from data/l40.json (wording, options, correct letter)."""
import os, sys, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import supp_cards as S
from supp_cards import C, U12, T, chip, glass, tile, row, at, bottom, grid, rows, flow, centered, photo
from PIL import Image
NAME = 'ציוד ובדיקות GMDSS'
HERE = os.path.dirname(os.path.abspath(__file__))
C.OUT = os.path.join(HERE, '..', 'cards', NAME); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'קורס GMDSS · ציוד ובדיקות'
F, text_c, text_r, dot, base, left_panel, right_block, save, RC = C.F, C.text_c, C.text_r, C.dot, C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, GREEN, GREEN_L, BLUE_L, PANEL = C.TEXT, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL
X0, Y0, X1, Y1, PW, PH = S.X0, S.Y0, S.X1, S.Y1, S.PW, S.PH
BANK = {q['num']: q for q in json.load(open(os.path.join(HERE, '..', '..', '..', 'data', 'l40.json'), encoding='utf-8'))}

def bankq(n):
    q = BANK[n]
    opts = [re.sub(r'^[א-ה]\.\s*', '', o) for o in q['options']]
    return (q['source'].replace('מבחן ', 'מבחן ').replace(' שאלה ', ' · שאלה '), q['q_he'].rstrip(':'), opts, 'אבגדה'.index(q['answer'])), q['answer']

def card(sid, caption, body, title, text, q=None, bg=None, pos='center', shade=0.0):
    im, d = base(); left_panel(d, caption)
    p = Image.open(T.panel('l40e_' + sid, body, PW, PH, bg, pos, shade)).convert('RGBA'); im.paste(p, (X0, Y0), p)
    if bg in S.CR or bg in U12.CREDIT: U12.credit(d, (X0, Y0, X1, Y1), bg)
    right_block(d, title, text, q); save(im, sid)

def ans(head, tone, *rs):
    return at(24, 24, chip(head, tone, 34)) + bottom(rows(*rs))

def qcard(sid, caption, num, head, good, bads, text, bg, tone='green', shade=0.2, pos='center', extra=None):
    q, letter = bankq(num)
    rs = [('✓', good, 'green', 30)] + [('✗', b, 'red', 28) for b in bads]
    if extra: rs = extra
    card(sid, caption, ans(head, tone, *rs), 'תשובה ' + letter, text, q, bg=bg, pos=pos, shade=shade)

def info(sid, caption, chip_text, tone, rs, title, text, bg, shade=0.2, pos='center'):
    body = at(24, 24, chip(chip_text, tone, 34)) + bottom(rows(*rs))
    card(sid, caption, body, title, text, bg=bg, pos=pos, shade=shade)

def summary(sid, photo_name, items, step=98, fs=42):
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), photo_name, focus=(0.5, 0.5))
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    for i, s in enumerate(items):
        y = 360 + i * step
        d.rounded_rectangle((1360, y, 2460, y + 82), 20, fill=PANEL)
        dot(d, (2420, y + 41), 12, GREEN_L if i < 5 else C.ORANGE)
        text_r(d, 2380, y + 16, s, F(fs, False), TEXT)
    save(im, sid)

# ---------- cards ----------
def s01_intro():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u16_ships', focus=(0.5, 0.5))
    text_c(d, RC, 380, 'קורס GMDSS · מבחן משרד התקשורת', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'ציוד ובדיקות', F(124), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['SART · משיב מכ״מ', 'לוויינים ו-LUT', 'EPIRB · AIS', 'מצברים ובדיקות יומיות']):
        text_c(d, RC, 810 + i * 84, s, F(52, False), TEXT)
    save(im, 's01_intro')

def s02_sart():
    info('s02_sart', 'SART', 'משיב מכ״מ', 'green',
         [('9', 'X BAND · 9 GHz', 'green', 30), ('⇢', 'עונה למכ״מ · שורת נקודות', 'sky', 30), ('4d', 'סוללה · 4 ימים בהמתנה', 'amber', 30), ('8h', '8 שעות בשידור', 'amber', 30)],
         'SART', 'משיב מכ״מ בתדר X BAND. לא קולט ולא משדר ב-VHF.', 'u16_sart_radar')

def s03_q4112(): qcard('s03_q4112', 'תדר ה-SART', 4112, 'X BAND · 9 GHz', 'X BAND · 9 GHz', ['121.5 ו-406 · EPIRB', 'VHF · לא קשור', 'S BAND · מכ״מ אחר'],
                       'ה-SART עונה למכ״מ בתדר X BAND, תשעה ג׳יגה הרץ.', 'u16_sart_radar')
def s04_q4011(): qcard('s04_q4011', 'סוללת SART', 4011, 'המתנה · STAND BY', '4 יממות · STAND BY', ['8 שעות · זמן שידור', 'יומיים · קצר מדי', '3 יממות · קצר מדי'],
                       'ארבע יממות בהמתנה, שמונה שעות בשידור.', 'u16_sart_pro')
def s05_q4133(): qcard('s05_q4133', 'טווח ה-SART', 4133, 'מרחק ההפעלה', 'תלוי בגובה אנטנת המכ״מ', ['5 מייל · לא קבוע', '8 מייל · לא קבוע', '12 מייל · לא קבוע'],
                       'קרינת מכ״מ נעה בקו ישר, ולכן הטווח תלוי בגובה האנטנה.', 'u16_sart_radar')
def s06_q4121(): qcard('s06_q4121', 'מטרת ה-SART', 4121, 'מטרה', 'להתבייט על מכ״מ X BAND', ['לא מתקן קשר', 'לא מתקן התרעה', 'לא משדר זיהוי ספינה'],
                       'ה-SART רק מסמן את המקום על המכ״מ. הוא לא משדר התרעה.', 'u16_sart_pro')

def s07_satellites():
    body = at(24, 24, chip('COSPAS-SARSAT · 406 MHz', 'sky', 32)) + grid(
        [('LEO', '~1,000 ק״מ · LEOLUT', 'green'), ('MEO', '~20,000 ק״מ · MEOLUT', 'sky'), ('GEO', '36,000 ק״מ · GEOLUT', 'amber'), ('LUT', 'תחנת קרקע', 'red')], top=130, h=260, hs=70)
    card('s07_satellites', 'הלוויינים', body, 'LEO · MEO · GEO', 'שלושה סוגי לוויינים, ולכל סוג תחנת קרקע משלו.', bg='u16_cospas', shade=0.7)

def s08_q4016(): qcard('s08_q4016', 'GEO · MEO · LEO', 4016, 'סוגי לוויינים', 'לוויינים בגבהים שונים', ['לא תחנות NAVTEX', 'לא סוגי קרינה', 'לא התפשטות גלי רדיו'],
                       'שלושה מסלולים של לוויינים במערכת GMDSS.', 'u16_cospas')
def s09_q4120(): qcard('s09_q4120', 'המונח MEO', 4120, 'MEO', 'MEDIUM EARTH ORBIT', ['MARITIME EARTH ORBIT · לא קיים', 'MARINE ELECTRONIC OFFICER · לא קיים', 'שאר התשובות · המצאות'],
                       'MEO הוא מסלול בינוני סביב כדור הארץ.', 'u16_cospas')
def s10_q4049(): qcard('s10_q4049', 'גובה LEOSAT', 4049, 'LEOSAT', 'סביב 1,000 ק״מ', ['36,000 ק״מ · GEO', '10,000 ק״מ · אף סוג', 'לא משתנה לפי צורך'],
                       'לוויין LEO נמוך, בערך אלף קילומטר.', 'u16_cospas')
def s11_q4150(): qcard('s11_q4150', 'GALILEO', 4150, 'מי קובע מיקום', 'MEOLUT · לוויין MEO', ['GEOLUT · ללוויין GEO', 'LEOLUT · ללוויין LEO', 'GPSLUT · לא קיימת'],
                       'GALILEO הוא לוויין MEO, ולכן התחנה היא MEOLUT.', 'u16_cospas')
def s12_q4183(): qcard('s12_q4183', 'יחידות LUT', 4183, 'LEOLUT · MEOLUT · GEOLUT', 'קולטות משואות מלוויינים', ['לא מעבירות לתחנות חוף', 'לא שייכות לתקשורת', 'לא מנהלות חיפוש · RCC'],
                       'ה-LUT היא יחידת קרקע שקולטת את אות המשואה.', 'u16_cospas')
def s13_q4201(): qcard('s13_q4201', 'MEOSAR', 4201, 'דור שלישי', '', [], 'א ו-ב נכונות. ג׳ שגויה כי המערכת כן צריכה LUT.', 'u16_cospas',
                       extra=[('✓', '70-90 לוויינים · זמינות מיידית', 'green', 30), ('✓', 'חיווי לניצולים כשנקלטה', 'green', 30), ('✗', 'ג׳ · צריך LUT', 'red', 28)])

def s14_epirb():
    info('s14_epirb', 'EPIRB', 'משואה', 'red',
         [('406', 'MHz · לוויינים', 'red', 30), ('↻', 'משתחררת אוטומטית', 'sky', 30), ('GPS', 'GPIRB · מיקום מיידי', 'green', 30), ('Δ', 'בלי GPS · דופלר, איטי', 'amber', 30)],
         'EPIRB', 'GPIRB משדרת מיקום מדויק מיד. משואה בלי GPS מאותרת לפי דופלר.', 'u16_epirb_parts')
def s15_q4020(): qcard('s15_q4020', 'EPIRB באזור A1', 4020, 'היתרון', 'פועלת אוטומטית בטביעה', ['לא גיבוי ל-DSC', 'אמינות · לא ההבדל', 'האות ללוויין · לא היתרון'],
                       'היתרון של המשואה הוא ההפעלה האוטומטית.', 'u16_epirb_bracket')
def s16_q4075(): qcard('s16_q4075', 'דיוק GPS', 4075, 'משדרים מיקום GPS', 'AIS SART · GPIRB · AIS', ['RADAR SART · אין מיקום', 'EPIRB בלי GPS · דופלר', 'NAVTEX · מקלט'],
                       'מי שיש בתוכו מקלט GPS משדר מיקום מדויק.', 'u16_raft_epirb')
def s17_q4189(): qcard('s17_q4189', 'התרעת מצוקה', 4189, 'מתקני התרעה', 'DSC ו-GPIRB', ['SART · איתור, לא התרעה', 'ערוץ 16 · קול, לא ייעודי', 'NAVTEX · מקלט בלבד'],
                       'התרעה משדרים ב-DSC וב-GPIRB. SART הוא מתקן איתור.', 'u16_vhf_ais')
def s18_q4164(): qcard('s18_q4164', 'ניהול אירוע', 4164, 'מי לא מנהל', 'MCC · רק מעביר מידע', ['RCC · מנהל אירועים', 'כלי שיט גדול · מפקח', 'תחנת חוף · עד שה-RCC מפקד'],
                       'ה-MCC מעביר את המידע מהלוויין, אבל לא מנהל את האירוע.', 'l40_rcc')
def s19_q4025(): qcard('s19_q4025', 'OSC', 4025, 'אחראי במקום', 'OSC · מפקד במקום האירוע', ['MCC · לא מפקח', 'DSC · סוג קשר, לא יחידה', 'EGC · הודעות לוויין'],
                       'OSC הוא המפקד במקום האירוע.', 'l40_rcc')
def s20_q4161(): qcard('s20_q4161', 'בדיקת EPIRB', 4161, 'מצב TEST', 'לפני הפלגה, ואחת לחודש בלב ים', ['שבועית · שוחקת סוללה', 'יומית · יותר מדי', 'כל 4 שעות · יותר מדי'],
                       'במצב TEST המשואה לא משדרת התרעה אמיתית.', 'u16_epirb_bracket')
def s21_q4140(): qcard('s21_q4140', 'זיהוי עצמי', 4140, 'לא MMSI של הספינה', 'AIS SART · קוד 970', ['VHF נייד · אין MMSI', 'DSC · MMSI של הספינה', 'EPIRB · קוד משואה'],
                       'ל-AIS SART יש קוד זיהוי משלו שמתחיל ב-970.', 'u16_vhf_ais')
def s22_q4014(): qcard('s22_q4014', 'קוד 970', 4014, '970 441 289', 'קוד AIS SART · מתחיל ב-970', ['MMSI ספינה · מתחיל בקוד מדינה', 'לא קוד NAVTEX', 'לא מטוס חיפוש'],
                       'כל קוד שמתחיל ב-970 הוא AIS SART.', 'u16_vhf_ais')
def s23_q4168(): qcard('s23_q4168', 'מידע ב-AIS', 4168, 'ארבעה סוגי מידע', 'STATIC · DYNAMIC · VOYAGE · SAFETY', ['VITAL · IMPORTANT · ROUTINE · NAVTEX', 'DISTRESS · URGENCY · SAFETY · קשר', 'ג׳ · גם NAVTEX'],
                       'סטטי, דינמי, מסע ובטיחות.', 'u16_vhf_ais')

def s24_batteries():
    info('s24_batteries', 'מצברים', 'מצברי תחנת הקשר', 'amber',
         [('◔', 'בדיקה יומית ושבועית', 'green', 30), ('⚗', 'משקל סגולי · פעם בשבוע', 'sky', 30), ('~', 'אוורור · מימן מתפוצץ', 'red', 30)],
         'מצברים', 'בודקים כל יום וכל שבוע. מקום האחסון חייב אוויר.', 'l40_radio_room')
def s25_q4035(): qcard('s25_q4035', 'בדיקת מצברים', 4035, 'תדירות', 'יומית ושבועית', ['חודשית · לא מספיק', 'לפני הפלגה · לא רק', 'לפי היצרן · לא מספיק'],
                       'התקנה קובעת בדיקה יומית ושבועית.', 'l40_radio_room')
def s26_q4118(): qcard('s26_q4118', 'משקל סגולי', 4118, 'כל תא', 'כל שבוע', ['כל יום · לבדיקת מתח', 'כל חודש · ארוך מדי', 'להפלגה · לא נוהל'],
                       'משקל סגולי של הנוזל בכל תא נבדק פעם בשבוע.', 'l40_cockpit')
def s27_q4141(): qcard('s27_q4141', 'אוורור מצברים', 4141, 'למה מאווררים', 'מזעור סכנת פיצוץ · מימן', ['גיפור הדקים · לא הסיבה', 'חמצן לטעינה · לא', 'ניצוצות · הסכנה, לא התשובה'],
                       'המצבר פולט מימן בטעינה, והוא מתפוצץ.', 'l40_radio_room')

def s28_checks():
    info('s28_checks', 'בדיקות הציוד', 'DSC', 'sky',
         [('D', 'DSC · בדיקה יומית', 'green', 30), ('⚙', 'פנימית של היצרן · בלי שידור', 'sky', 30), ('GPS', 'חיבור חיוני ל-DSC', 'amber', 30)],
         'בדיקות', 'בלב ים בודקים DSC פעם ביממה, בלי לשדר לתחנה.', 'l40_cockpit')
def s29_q4094(): qcard('s29_q4094', 'בדיקת VHF DSC', 4094, 'מינימום', 'יומי', ['שנתי · לא מספיק', 'ביקורת שנתית · לא', 'חודשי · לא מספיק'],
                       'בדיקה יומית היא המינימום.', 'l40_cockpit')
def s30_q4045(): qcard('s30_q4045', 'בדיקת DSC בלב ים', 4045, 'איך בודקים', 'בדיקה פנימית · פעם ביממה', ['קריאה לתחנת חוף · לא', 'שבועית · לא מספיק', 'כן חייבים · גם כשפעיל'],
                       'באמצעים של היצרן, בלי לשלוח קריאה.', 'l40_cockpit')
def s31_q4163(): qcard('s31_q4163', 'חיבור GPS', 4163, 'מתקן עם GPS קבוע', 'DSC · המיקום נכנס להתרעה', ['RADAR SART · אין צורך', 'EPIRB · GPS רק ב-GPIRB', 'NAVTEX · מיקום כללי'],
                       'בלי מיקום אי אפשר לשדר התרעה מלאה.', 'l40_cockpit')
def s32_q4128(): qcard('s32_q4128', 'GPS משובש', 4128, 'נתוני מיקום שגויים', '', [], 'מבטלים את ההשפעה ומזינים מיקום ידנית. לא מנתקים DSC.', 'l40_cockpit',
                       extra=[('✓', 'לבטל את השפעת ה-GPS', 'green', 30), ('✓', 'להזין מיקום ידנית', 'green', 30), ('✗', 'לא מנתקים DSC לגמרי', 'red', 28)])

def s33_summary():
    summary('s33_summary', 'u16_raft_epirb', ['SART · X BAND, 9 GHz', 'סוללת SART · 4 ימים', 'LEO ~1,000 · MEO ~20,000 · GEO 36,000', 'MEOLUT · GALILEO',
             'EPIRB · לפני הפלגה, חודש בים', '970 · AIS SART', 'מצברים · יומית ושבועית', 'DSC · בדיקה יומית, מחובר ל-GPS'])

ALL = [v for k, v in sorted(globals().items()) if re.match(r's\d\d_', k) and callable(v)]

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:                              # OneDrive can lock a freshly written PNG
                    import time; time.sleep(2)
