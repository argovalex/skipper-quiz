"""l40 lesson 9: כותבים נוהל מצוקה (part A of the exam: EPIRB, DSC ch70, voice MAYDAY ch16, abandon).
No bank questions here: info cards plus a 'written answer' note card, same look as proc_supp_cards.py."""
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import equip_cards as E
from equip_cards import C, info, summary, F, text_c, base, photo, save, TEXT, GREEN, BLUE_L, RC
from PIL import ImageFont

NAME = 'כותבים נוהל מצוקה'
HERE = os.path.dirname(os.path.abspath(__file__))
C.OUT = os.path.join(HERE, '..', 'cards', NAME); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'קורס GMDSS · כותבים נוהל מצוקה'
MONO = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 64)
MONO_S = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 54)

def note(sid, title, lines, chips=(), foot=None):
    """A sheet of paper with the written answer; lines = [(text, color)]; chips = legend rows under it."""
    im, d = C.base()
    C.text_c(d, 1280, 34, title, F(72), TEXT)
    d.rounded_rectangle((230, 140, 2330, 1350), 50, fill=(28, 34, 46), outline=(70, 84, 110), width=6)
    d.rounded_rectangle((290, 200, 2270, 1010 if chips else 1230), 28, fill=(244, 240, 228))
    big = len(lines) <= 8
    for i, (txt, col) in enumerate(lines):
        d.text((350, 222 + i * (88 if big else 74)), txt, font=MONO if big else MONO_S, fill=col)
    y = 1040
    for txt, col in chips:
        d.rounded_rectangle((330, y, 2230, y + 70), 20, fill=(20, 28, 44), outline=col, width=5)
        C.text_r(d, 2190, y + 8, txt, F(44, False), TEXT); y += 80
    if foot: C.text_c(d, 1280, 1290, foot, F(40, False), C.MUTED)
    C.save(im, sid)

INK = (30, 40, 60); RED = (190, 40, 40); BLUE = (30, 90, 170)

def s01_intro():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u16_ships', focus=(0.5, 0.5))
    text_c(d, RC, 380, 'קורס GMDSS · מבחן משרד התקשורת', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'כותבים נוהל מצוקה', F(110), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['EPIRB', 'DSC בערוץ 70', 'MAYDAY בערוץ 16', 'נטישה']):
        text_c(d, RC, 810 + i * 84, s, F(52, False), TEXT)
    save(im, 's01_intro')

def s02_part_a():
    info('s02_part_a', 'החלק הראשון במבחן', 'כתיבה · 15 דקות', 'sky',
         [('1', 'מפעילים EPIRB · 5 נקודות', 'green', 28), ('2', 'DSC בערוץ 70 · 20 נקודות', 'green', 28), ('3', 'MAYDAY בקול בערוץ 16', 'green', 28),
          ('4', 'נטישה · 10 נקודות', 'green', 28)],
         'ארבעה סעיפים', 'ציון מעבר: 80. מקבלים תרחיש וכותבים צעד אחרי צעד.', 'l40_rcc', shade=0.3)

def s03_step1_epirb():
    info('s03_step1_epirb', 'סעיף 1', 'EPIRB · 5 נקודות', 'sky',
         [('✓', 'מפעילים EPIRB בהקדם האפשרי', 'green', 30), ('✓', 'ידנית, בלי לחכות לשחרור אוטומטי', 'green', 28), ('✓', 'משדר ללוויין, בלי קשר לשאר הנוהל', 'green', 28)],
         'הצעד הראשון', 'כותבים אותו ראשון.', 'u16_ships', shade=0.3)

def s04_step2_dsc():
    info('s04_step2_dsc', 'סעיף 2', 'DSC ערוץ 70 · 20 נקודות', 'sky',
         [('1', 'תפריט DISTRESS', 'green', 28), ('2', 'סוג האירוע (למשל FIRE)', 'green', 28), ('3', 'בדיקת מיקום ושעה', 'green', 28),
          ('4', 'לחיצה 5 שניות', 'green', 28), ('✓', 'ה-MMSI נשלח אוטומטית', 'green', 28)],
         'הסעיף הכבד', 'לא מכניסים MMSI ידנית.', 'l40_cockpit', shade=0.3)

def s05_dsc_why():
    info('s05_dsc_why', 'סוג האירוע', 'מוגדרת או לא', 'sky',
         [('✓', 'מוגדרת: R C C מתארגן מהר יותר', 'green', 28), ('!', 'לא מוגדרת, UNDESIGNATED: כשאין זמן', 'amber', 28), ('✗', 'לא מכבים את המכשיר', 'red', 28)],
         'למה לבחור', 'ההתרעה חוזרת לבד עד לאישור.', 'l40_cockpit', shade=0.3)

def s06_step3_mayday():
    note('s06_step3_mayday', 'MAYDAY בקול · ערוץ 16', [('MAYDAY MAYDAY MAYDAY', RED), ('THIS IS [NAME] x3', INK), ('MAYDAY [NAME]', RED), ('POSITION ...', BLUE),
                                                           ('NATURE OF DISTRESS', INK), ('PERSONS ON BOARD', INK), ('ASSISTANCE REQUIRED', INK), ('OVER', RED)],
         chips=[('הסדר קבוע: מיקום, מהות, אנשים, סיוע', GREEN)])

def s07_position():
    info('s07_position', 'המיקום', 'שתי דרכים', 'sky',
         [('1', 'קואורדינטות ספרה אחר ספרה, רוחב קודם', 'green', 28), ('2', 'כיוון וטווח במייל ימי מנקודת ציון בחוף', 'green', 28),
          ('✗', 'לא מקריאים מספר שלם', 'red', 28)],
         'הטעות הנפוצה', 'הרוחב קודם ואחר כך האורך.', 'l40_world_a1a2', shade=0.3)

def s08_example():
    note('s08_example', 'דוגמה כתובה', [('MAYDAY MAYDAY MAYDAY', RED), ('THIS IS MOTOR YACHT NOA NOA NOA', INK), ('MMSI 4-2-8-6-5-4-3-2-1', INK), ('MAYDAY NOA', RED),
                                         ('POSITION 3-2 DEGREES 5-0 MINUTES NORTH', BLUE), ('0-3-4 DEGREES 4-8 MINUTES EAST', BLUE),
                                         ('FIRE IN THE ENGINE ROOM, NO CONTROL', INK), ('SIX PERSONS ON BOARD', INK), ('REQUIRE IMMEDIATE ASSISTANCE', INK), ('OVER', RED)],
         chips=[('קו הרוחב קודם, אחר כך קו האורך. דוגמה להמחשה', GREEN)])

def s09_ack():
    info('s09_ack', 'אישור קבלה', 'RECEIVED MAYDAY', 'sky',
         [('✓', 'רק תחנת חוף או R C C מאשרת', 'green', 28), ('✓', 'בקול, בערוץ 16', 'green', 28), ('✗', 'כלי שיט אחר לא מאשר את ה-DSC', 'red', 28)],
         'מי עונה', 'כלי שיט אחר יכול לענות בקול.', 'l40_rcc', shade=0.3)

def s10_step4_abandon():
    info('s10_step4_abandon', 'סעיף 4', 'נטישה · 10 נקודות', 'sky',
         [('1', 'EPIRB קשור לאסדה', 'green', 28), ('2', 'SART גבוה ככל האפשר', 'green', 28), ('3', 'VHF נייד בערוץ 16: ווליום מקסימלי, SQUELCH מינימלי', 'green', 26),
          ('4', 'סוללות גיבוי', 'green', 28), ('✓', 'לפני כן: אפודות, בגדים חמים, תיק חירום', 'amber', 26)],
         'ארבעה פרטים', 'עושים אותם לפני שעולים על האסדה.', 'l40_handheld', shade=0.3)

def s11_scenario_fire():
    info('s11_scenario_fire', 'תרחיש 1', 'שריפה בחדר המנוע', 'sky',
         [('1', 'EPIRB', 'green', 28), ('2', 'DSC עם סוג האירוע FIRE', 'green', 28), ('3', 'ערוץ 16, MAYDAY מלא', 'green', 28), ('4', 'אפודות ותיק חירום', 'green', 28),
          ('5', 'נטישה: EPIRB, SART, VHF נייד', 'green', 28), ('6', 'האזנה, שמירה על סוללות', 'green', 28)],
         'הסדר', 'ממתינים ומאזינים לערוץ 16.', 'l40_cockpit', shade=0.3)

def s11_sondra():
    info('s11_sondra', 'מופיע במבחן', 'היאכטה SONDRA', 'sky',
         [('🔥', 'שריפה בחדר המכונות', 'green', 28), ('📍', 'מיקום: קו הרוחב קודם', 'green', 28), ('📋', 'שם, MMSI, מיקום ומספר אנשים: מהתרחיש', 'green', 28)],
         'SONDRA', 'אותו נוהל. הפרטים משתנים.', 'l40_signal', shade=0.3)

def s12_scenario_grounding():
    info('s12_scenario_grounding', 'תרחיש 2', 'עלייה על שרטון', 'sky',
         [('!', 'בלי סכנת חיים: PAN PAN', 'amber', 28), ('✓', 'חדירת מים או סכנה לאנשים: מצוקה', 'red', 28), ('✓', 'DSC עם סוג האירוע GROUNDING', 'green', 28),
          ('✓', 'MAYDAY בערוץ 16, ונטישה אם צריך', 'green', 28)],
         'מצוקה או דחיפות', 'המבחן בודק שאתה מבדיל.', 'l40_cockpit', shade=0.3)

def s12_simulator():
    info('s12_simulator', 'סימולטור', 'שלושה תרחישים', 'sky',
         [('1', 'SONDRA · שריפה', 'green', 28), ('2', 'NOA · שריפה בחדר המנוע', 'green', 28), ('3', 'DANA · עלייה על שרטון', 'green', 28)],
         'מתרגלים', 'כל הנוהל, עם ציון לכל סעיף.', 'l40_cockpit', shade=0.3)

def s13_checklist():
    info('s13_checklist', 'לפני שמגישים', 'רשימת בדיקה', 'sky',
         [('✓', 'EPIRB', 'green', 28), ('✓', 'DSC: הרצף כולו', 'green', 28), ('✓', 'MAYDAY: סדר, ומיקום ספרה ספרה', 'green', 28), ('✓', 'נטישה: ארבעה פרטים', 'green', 28),
          ('!', 'הכי נשכחים: המיקום וה-SQUELCH', 'amber', 28)],
         'בדיקה אחרונה', 'עוברים סעיף סעיף.', 'l40_rcc', shade=0.3)

def s14_summary():
    summary('s14_summary', 'u16_vhf_ais', ['EPIRB · בהקדם · 5', 'DSC ערוץ 70 · 20', 'MAYDAY ערוץ 16 · מיקום ספרה ספרה', 'אישור: תחנת חוף או R C C',
             'נטישה · 10', 'EPIRB קשור, SART גבוה', 'VHF נייד על 16, סוללות', 'ציון מעבר 80'])

def assets():
    """Real simulator footage (sim_record.js): <sid>.mp4 replaces the still, <sid>_sim.png/.mp3 is the radio reply after the narration."""
    import shutil
    A = os.path.join(HERE, 'sim_assets')
    for f in os.listdir(A):
        shutil.copyfile(os.path.join(A, f), os.path.join(C.OUT, f))

ALL = [v for k, v in sorted(globals().items()) if re.match(r's\d\d_', k) and callable(v)]

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:
                    import time; time.sleep(2)
    assets()
