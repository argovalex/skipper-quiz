"""l40 lesson 1: מבוא ל-GMDSS. Same helpers and look as supp_cards.py (l30 style: Tailwind left panel, PIL right block)."""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('supp', os.path.join(HERE, 'supp_cards.py')); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
C, T = S.C, S.T
from twcard import chip, glass, tile, row
NAME = 'מבוא ל-GMDSS'
C.OUT = os.path.join(HERE, '..', 'cards', NAME); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'קורס GMDSS · מבוא'
S.CR.update({'u13_vhf': 'Photo: PaterMcFly · CC BY 3.0', 'u12_sat': 'Image: NASA · Public domain'}); S.U12.CREDIT.update(S.CR)
card, at, bottom, grid, rows, flow, centered = S.card, S.at, S.bottom, S.grid, S.rows, S.flow, S.centered
F, text_c, text_r, dot, base, save, RC, photo, credit = S.F, S.text_c, S.text_r, S.dot, S.base, S.save, S.RC, S.photo, S.credit
TEXT, GREEN, GREEN_L, BLUE_L, PANEL = S.TEXT, S.GREEN, S.GREEN_L, S.BLUE_L, S.PANEL
EXAM = S.EXAM

def title_card(sid, bg, head, title, items, focus=(0.5, 0.5)):
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), bg, focus=focus)
    if bg in S.CR: credit(d, (0, 0, 1300, 1440), bg)
    text_c(d, RC, 380, head, F(56, False), BLUE_L)
    text_c(d, RC, 520, title, F(124), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(items):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, sid)

def s01():
    title_card('s01_intro', 'l40_cockpit', 'קורס GMDSS · שיעור 1', 'מבוא ל-GMDSS',
               ['למה נולדה המערכת', 'מי צריך אותה', 'איך בנוי המבחן', 'ארבעת אזורי הים'], (0.35, 0.5))

# Night sea, 1912: Titanic (left, bow down, SOS) and the Californian (right), ~10-20 NM apart.
SHIPS = """<svg viewBox="0 0 1130 400" class="w-full h-full">
 <rect width="1130" height="400" fill="#0b1630"/><rect y="270" width="1130" height="130" fill="#0f2a4a"/>
 <g transform="translate(70,150) rotate(9 220 120)">
  <polygon points="0,90 470,90 450,130 25,130" fill="#e5e7eb"/><rect x="0" y="110" width="470" height="20" fill="#111827"/>
  <rect x="60" y="62" width="330" height="28" fill="#f8fafc"/>
  <g fill="#f59e0b"><rect x="95" y="10" width="26" height="52"/><rect x="170" y="10" width="26" height="52"/><rect x="245" y="10" width="26" height="52"/><rect x="320" y="10" width="26" height="52"/></g>
  <g fill="#111827"><rect x="95" y="10" width="26" height="12"/><rect x="170" y="10" width="26" height="12"/><rect x="245" y="10" width="26" height="12"/><rect x="320" y="10" width="26" height="12"/></g>
 </g>
 <text x="300" y="70" fill="#fb7185" font-size="52" font-weight="800" text-anchor="middle" font-family="Heebo">· · · — — — · · ·</text>
 <text x="300" y="370" fill="#fff" font-size="40" font-weight="800" text-anchor="middle" font-family="Heebo">TITANIC</text>
 <g transform="translate(860,205)">
  <polygon points="0,60 210,60 198,88 12,88" fill="#cbd5e1"/><rect x="60" y="38" width="100" height="22" fill="#f1f5f9"/>
  <rect x="100" y="8" width="20" height="30" fill="#334155"/>
 </g>
 <text x="965" y="370" fill="#fff" font-size="40" font-weight="800" text-anchor="middle" font-family="Heebo">CALIFORNIAN</text>
 <text x="965" y="185" fill="#94a3b8" font-size="44" text-anchor="middle">💤</text>
 <line x1="560" y1="300" x2="840" y2="300" stroke="#fbbf24" stroke-width="6" stroke-dasharray="18 12"/>
 <polygon points="560,300 585,288 585,312" fill="#fbbf24"/><polygon points="840,300 815,288 815,312" fill="#fbbf24"/>
 <text x="700" y="275" fill="#fbbf24" font-size="40" font-weight="800" text-anchor="middle" font-family="Heebo">~10-20 מייל</text>
</svg>"""

def s02():
    body = (f'<div class="absolute inset-x-0 top-0 h-[440px]">{SHIPS}</div>'
            + at(24, 24, chip('1912 · קוד מורס', 'amber', 32))
            + bottom(glass('<div class="p-5 flex items-center gap-4">' + row('💤', 'הקליפורניאן · מפעיל הרדיו ישן', 'slate', 30) + '</div>')))
    card('s02_titanic', 'הטיטאניק', body, '1912', 'הקליפורניאן הייתה 10 עד 20 מייל משם, אבל המפעיל שלה כיבה את המכשיר והלך לישון.',
         bg='l40_radio_room', pos='70% 60%', shade=0.1)

def s03():
    body = centered(flow([('1914 · SOLAS ראשונה · האזנה מסביב לשעון', 'slate'), ('1979 · IMO ו-ITU מתחילים לבנות', 'sky'),
                          ('1988 · נכנסת לאמנת SOLAS', 'amber'), ('1.2.1999 · חובה מלאה', 'green')], 32))
    card('s03_gmdss_born', 'למה לקח כל כך הרבה זמן', body, 'GMDSS', 'אחרי הטיטאניק הקשר נשאר במורס. GMDSS חיכתה ללוויינים ולקשר ספרתי, שהגיעו רק בשנות ה-70 וה-80.',
         bg='l40_signal', shade=0.45)

def s04():
    body = ('<div class="absolute inset-x-6 top-6 grid grid-cols-2 gap-4">'
            + tile('פעם', 'תלוי במזל · מי שומע?', 'red', 'h-[220px]', 64, 28) + tile('היום', 'לחיצה אחת · אוטומטי', 'green', 'h-[220px]', 64, 28) + '</div>'
            + '<div class="absolute inset-x-8 bottom-8 top-[280px] flex flex-col justify-center">'
            + flow([('DISTRESS · לחיצה אחת', 'red'), ('תחנת חוף', 'sky'), ('RCC · מרכז תיאום ההצלה', 'green')], 32) + '</div>')
    card('s04_principle', 'העיקרון', body, 'לחיצה אחת', 'ההתראה מגיעה לתחנת חוף ול-RCC, עם הזהות והמיקום שלך. גם כשאין זמן לדבר.',
         bg='l40_rcc', shade=0.45)

def s05():
    body = (at(24, 24, chip('מי צריך GMDSS', 'green', 34))
            + bottom(rows(('🚢', 'SOLAS · ספינות מסחריות בשיט בינלאומי', 'sky', 28), ('⛵', 'ישראל · מפעיל רדיו טלפון מוגבל', 'green', 28),
                          ('↑', 'בדרך לתעודות המשיט המתקדמות', 'amber', 28), ('✈', 'השכרת יאכטה בחו״ל · למשל קרואטיה', 'amber', 28))))
    card('s05_who_needs', 'מי צריך את זה', body, 'התעודה', 'מפעיל רדיו טלפון מוגבל, בזיקה ל-GMDSS. ההסמכה הבסיסית להפעלת מכשיר הקשר הימי.',
         bg='l40_handheld', pos='20% 40%', shade=0.15)

def s06():
    parts = [('א׳', 'נוהל מצוקה בכתב', '15 דק׳ · מעבר 80', 'red'), ('ב׳', '20 שאלות אמריקאיות', '30 דק׳ · מעבר 75', 'sky'),
             ('ג׳', 'בעל פה + סימולטור', 'עובר / לא עובר', 'amber')]
    tl = ''.join(f'<div class="rounded-2xl bg-slate-900/85 ring-2 {T.TONES[t][0]} px-6 py-4 flex items-center gap-6">'
                 f'<div class="{T.TONES[t][1]} font-extrabold text-[84px] leading-none w-[110px] text-center">{n}</div>'
                 f'<div><div class="text-white font-bold text-[42px]">{a}</div><div class="text-white/80 text-[34px]">{b}</div></div></div>' for n, a, b, t in parts)
    body = (f'<div class="absolute inset-x-6 top-6 space-y-4">{tl}</div>'
            + bottom(glass('<div class="p-5 text-white text-[36px] font-bold text-center">נכשלים בעיקר ב-א׳ וב-ג׳</div>')))
    card('s06_exam', 'מבנה המבחן', body, '3 חלקים', 'רק מי שעבר את א׳ ואת ב׳ מגיע ל-ג׳. נכשלת ב-ג׳? חוזרים רק עליו.', bg='u17_logbook', shade=0.8)

AREAS = [('A1', 'VHF · DSC', 'green'), ('A2', 'MF · DSC', 'sky'), ('A3', 'Inmarsat · לוויין', 'amber'), ('A4', 'קוטב · HF', 'red')]

def s07():
    body = at(24, 24, chip('לפי כיסוי · לא לפי מרחק', 'green', 34)) + grid(AREAS, 2, top=130, h=300, hs=96, ss=32)
    card('s07_areas_intro', 'אזורי הים', body, '4 אזורים', 'האזור נקבע לפי איזו תחנה שומעת אותך, ובאיזה מכשיר.', bg='l40_world_a1a2', pos='40% 40%', shade=0.45)

def arc(px, tone, label, sub, top):
    r, t, _ = T.TONES[tone]
    return (f'<div class="absolute rounded-full border-[6px] {r.replace("ring", "border")} bg-slate-900/20" style="width:{px*2}px;height:{px*2}px;right:{-px+60}px;top:{560-px}px"></div>'
            f'<div class="absolute text-right" style="right:{px - 40}px;top:{top}px"><div class="ltr {t} font-extrabold text-[64px] leading-none">{label}</div>'
            f'<div class="text-white text-[32px] font-semibold">{sub}</div></div>')

def s08():
    # map: lessons/l40/sources/map_a1a2.html (Leaflet + OSM), station on Mount Carmel at ~(745, 478); A1 r~90px (25 NM), A2 r~360px (100 NM)
    body = (at(24, 24, chip('טווחים מתחנת חוף · להמחשה', 'sky', 30))
            + at(430, 520, chip('A1 · כ-25 מייל', 'green', 30)) + at(60, 300, chip('A2 · כ-100 מייל', 'sky', 30))
            + at(770, 420, chip('📡 חיפה', 'amber', 26))
            + bottom(rows(('A1', 'מכשיר VHF עם DSC', 'green', 30), ('A2', 'גם מכשיר MF עם DSC', 'sky', 30))))
    card('s08_area_a1a2', 'A1 ו-A2', body, 'תחנת חוף', 'ב-A1 התחנה שומעת אותך ב-VHF, בערך 20 עד 30 מייל. ב-A2 בתדר בינוני, MF, עד כ-100 מייל.', bg='l40_map_a1a2')

def band(text, sub, tone, h):
    r, t, b = T.TONES[tone]
    return (f'<div class="rounded-2xl {b}/50 flex flex-col items-center justify-center" style="height:{h}px">'
            f'<div class="ltr text-white font-extrabold text-[60px] leading-none">{text}</div><div class="text-white text-[32px] font-semibold">{sub}</div></div>')

def s09():
    body = ('<div class="absolute inset-6 flex flex-col gap-3 justify-center">'
            + band('A4', 'קוטב צפוני · HF', 'red', 170) + band('A3', '70°N עד 70°S · לווייני Inmarsat', 'amber', 520) + band('A4', 'קוטב דרומי · HF', 'red', 170) + '</div>')
    card('s09_area_a3a4', 'A3 ו-A4', body, 'לוויין וקוטב', 'A3 מכוסה בלוויינים בין 70 צפון ל-70 דרום. A4 הוא הקטבים, ושם רק HF.', bg='l40_world_a3a4', pos='40% 50%', shade=0.15)

def s10():
    body = (at(24, 24, chip('5 מייל מהחוף · A1?', 'amber', 36))
            + bottom(rows(('✗', 'אין תחנת חוף שקולטת VHF', 'red', 30), ('✗', 'לכן לא A1 · גם אם רואים חוף', 'red', 30),
                          ('✓', 'האזור · לפי הכיסוי בפועל', 'green', 30))))
    card('s10_exam_trap', 'המלכודת', body, 'לא בהכרח', 'בלי תחנת חוף שקולטת VHF, אתה לא ב-A1. גם חמישה מייל מהחוף.', bg='l40_rocky_coast', pos='45% 40%', shade=0.1)

def s11():
    body = (at(24, 24, chip('A1 · הדרישה הבסיסית', 'green', 34))
            + bottom(rows(('✓', 'ציוד ליזום מצוקה מהאנייה לחוף', 'green', 28), ('✗', 'VHF DSC · לא האמצעי היחיד', 'red', 28),
                          ('✗', 'MF / HF · הציוד של A2 ו-A3', 'red', 28), ('✗', 'HF עם MSI · לא מחליף VHF', 'red', 28))))
    card('s11_q16', 'ציוד באזור A1', body, 'תשובה א', 'יכולת לשדר מצוקה מהאנייה לחוף. ב-A1 צריך גם אמצעי נוסף, כמו EPIRB.',
         (EXAM.format(16), 'איזו הצהרה נכונה לגבי ציוד GMDSS לכלי שייט המפליג רק באזור A1?',
          ['חייב ציוד רדיו ליזום אתרעת מצוקה מהאנייה לחוף', 'VHF DSC יכול להיות האמצעי היחידי לאתרעת מצוקה', 'DSC ב-MF או ב-HF יכול לספק את הדרישות', 'SSB ב-HF המשלב MSI יכול לספק את הדרישות'], 0),
         bg='u13_vhf', shade=0.2)

COURSE = [('2', 'גלי רדיו ו-VHF', 'sky'), ('3', 'ערוצים, MMSI ו-DSC', 'sky'), ('4', 'NAVTEX', 'sky'), ('5', 'EPIRB, SART ו-AIS', 'sky'),
          ('6', 'נהלי קשר', 'amber'), ('7', 'נוהל מצוקה', 'amber'), ('8', 'השלמות למבחן', 'green'), ('9', 'חלק א׳ · כתיבת נוהל', 'red'), ('10', 'חלק ג׳ · סימולטור', 'red')]

def s12():
    card('s12_course_map', 'מפת הקורס', grid(COURSE, 3, h=290, hs=72, ss=28), '10 שיעורים', 'מהרדיו והמכשירים, דרך הנהלים, ועד שני השיעורים למבחן עצמו.', bg='u13_vhf', shade=0.85)

def s13():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u14_coast_station', focus=(0.5, 0.5))
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['טיטאניק · מערכת שתלויה באדם אחד', 'GMDSS · חובה מלאה מ-1999', 'לחיצה אחת · תחנת חוף ו-RCC', 'מבחן · א׳ בכתב, ב׳ אמריקאי, ג׳ סימולטור',
             'נכשלים בעיקר ב-א׳ וב-ג׳', 'A1 · VHF   A2 · MF', 'A3 · לוויין   A4 · קוטב', 'האזור · לפי כיסוי, לא מרחק']
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 5 else C.ORANGE)
        text_r(d, 2380, y + 20, s, F(46, False), TEXT)
    save(im, 's13_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13]

if __name__ == '__main__':
    only = sys.argv[1:]
    for fn in ALL:
        if not only or fn.__name__ in only:
            for k in range(5):
                try: fn(); break
                except OSError:
                    import time; time.sleep(2)
