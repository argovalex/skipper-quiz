"""Lesson 15 (l30): NAVTEX. Left panels in Tailwind (twcard.py) over real Commons photos; right block in PIL."""
import os, sys, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
C = _load('u01', 'u01_cards.py'); U5 = _load('u05', 'u05_cards.py'); U6 = _load('u06', 'u06_cards.py'); U8 = _load('u08', 'u08_cards.py'); U12 = _load('u12', 'u12_cards.py')
import twcard as T
from twcard import chip, glass, tile, row, digits
from PIL import Image
C.OUT = os.path.join(HERE, '..', 'cards', 'NAVTEX'); os.makedirs(C.OUT, exist_ok=True)
C.SUB = 'ניווט חופי ומכשירים · NAVTEX'
F, text_c, text_r, dot, base, left_panel, right_block, save, RC = C.F, C.text_c, C.text_r, C.dot, C.base, C.left_panel, C.right_block, C.save, C.RC
TEXT, GREEN, GREEN_L, BLUE_L, PANEL = C.TEXT, C.GREEN, C.GREEN_L, C.BLUE_L, C.PANEL
photo = U8.photo; credit = U12.credit
CR = {'u15_rx_target': 'Photo: K. Krallis (SV1XV) · CC BY-SA 3.0', 'u15_rx_printer': 'Photo: Clipper · CC BY 2.5',
      'u15_hvar_mast': 'Photo: Coronium · CC BY 4.0'}
U12.CREDIT.update(CR)
X0, Y0, X1, Y1 = [int(v) for v in U5.inner()]; PW, PH = X1 - X0, Y1 - Y0

def card(sid, caption, body, title, text, q=None, bg=None, pos='center', shade=0.0):
    im, d = base(); left_panel(d, caption)
    p = Image.open(T.panel(sid, body, PW, PH, bg, pos, shade)).convert('RGBA'); im.paste(p, (X0, Y0), p)
    if bg in CR: credit(d, (X0, Y0, X1, Y1), bg)
    right_block(d, title, text, q); save(im, sid)

def at(x, y, html, cls=''):
    return f'<div class="absolute {cls}" style="left:{x}px;top:{y}px">{html}</div>'

def bottom(html, cls=''):
    return f'<div class="absolute bottom-6 inset-x-6 {cls}">{html}</div>'

def grid(tiles, cols=2, cls='', top=24):
    return f'<div class="absolute inset-x-6 bottom-6 grid grid-cols-{cols} gap-4 content-center {cls}" style="top:{top}px">{tiles}</div>'

def rows(*rs, gap=3):
    return glass(f'<div class="p-6 space-y-{gap}">' + ''.join(row(*r) for r in rs) + '</div>')

def flow(steps):
    """steps: [(text, tone)] -> vertical chain of boxes with arrows."""
    bg = {'red': 'bg-rose-500/90', 'sky': 'bg-sky-500/90', 'amber': 'bg-amber-500/90', 'green': 'bg-emerald-500/90'}
    out = []
    for i, (s, t) in enumerate(steps):
        if i: out.append('<div class="text-white text-[46px] leading-none text-center">↓</div>')
        out.append(f'<div class="rounded-2xl {bg[t]} px-6 py-4 text-white font-extrabold text-center" style="font-size:{34 * T.S:.0f}px">{s}</div>')
    return '<div class="flex flex-col gap-2">' + ''.join(out) + '</div>'

MSG = ('<div class="ltr font-mono text-[34px] leading-snug text-emerald-200 p-6">'
       '<div class="text-amber-300 font-bold">ZCZC <span class="text-sky-300">HA01</span></div><div>130610 UTC FEB 05</div><div>IRAKLION RADIO</div>'
       '<div>NAVIGATIONAL WARNING</div><div>FLOATING CONTAINER</div><div>OBSERVED AT 3342N 0334E</div><div>DRIFTING WEST 3 KNOTS</div>'
       '<div class="text-amber-300 font-bold">NNNN</div><div class="text-white/60">CER 0.7%</div></div>')

# ---------- cards ----------
def s01():
    im, d = base()
    d.rectangle((0, 0, 1300, 1440), fill='white')                 # product shot on white (supplied by Alex)
    g = Image.open(os.path.join(T.A, 'u15_navtex_pro.jpg')).convert('RGB'); g = g.resize((1240, round(g.height * 1240 / g.width)), Image.LANCZOS)
    im.paste(g, (30, 720 - g.height // 2))
    text_c(d, RC, 380, 'קורס ניווט חופי ומכשירים · שיעור 15', F(56, False), BLUE_L)
    text_c(d, RC, 520, 'NAVTEX', F(130), TEXT)
    d.rounded_rectangle((RC - 80, 740, RC + 80, 754), 7, fill=GREEN)
    for i, s in enumerate(['מה זה NAVTEX', 'תדרים ואזורים', 'סוגי הודעות ועדיפות', 'הכנה לפני הפלגה']):
        text_c(d, RC, 810 + i * 84, s, F(54, False), TEXT)
    save(im, 's01_intro')

def s02():
    body = (at(24, 24, chip('NAVTEX · הודעות כתובות', 'green', 34))
            + bottom(rows(('!', 'אזהרות ניווט', 'amber'), ('☁', 'מזג אוויר', 'sky'), ('SOS', 'חיפוש והצלה', 'red'))
                     + '<div class="flex gap-3 pt-4">' + chip('✓ מקלט בלבד', 'green', 28) + chip('עד 400 מייל', 'sky', 28) + chip('אוטומטי', 'amber', 28) + '</div>'))
    card('s02_navtex', 'מקלט NAVTEX', body, 'NAVTEX', 'תחנות חוף משדרות הודעות כתובות, והמקלט קולט ומדפיס לבד. ביאכטה הוא מקלט בלבד.',
         bg='u15_rx_printer', pos='45% 40%', shade=0.1)

def s03():
    body = (at(24, 24, chip('משדר NAVTEX על החוף', 'green', 32))
            + bottom(rows(('✓', 'מינהלות ומשדרים בפריסה עולמית', 'green', 28), ('✓', 'מקלט מיוחד מדפיס את ההודעה', 'green', 28),
                          ('✗', 'לא ספר חודשי', 'red', 28), ('✗', 'לא לוויינים', 'red', 28), ('✗', 'לא ערוץ 70 · DSC', 'red', 28))))
    card('s03_q166', 'איך ההודעות מועברות', body, 'תשובה ב', 'משדרי חוף בפריסה עולמית, ומקלטי NAVTEX בכלי השייט.',
         ('שאלה מהמאגר · 166', 'כיצד מועברות ההודעות במערכת ה-NAVTEX?',
          ['קובץ חודשי שמורידים מהאינטרנט', 'מינהלות ומשדרים בפריסה עולמית, מקלטים מיוחדים', 'מערך לוויינים שמעביר את המידע', 'אזהרות ב-DSC על ערוץ 70'], 1),
         bg='u15_hvar_mast', pos='70% 50%', shade=0.15)

def s04():
    body = (at(24, 24, chip('מקלט בלבד · אין שידור', 'red', 34))
            + bottom(rows(('✗', 'מצוקה · VITAL', 'red', 30), ('✗', 'בטיחות · IMPORTANT', 'red', 30), ('✗', 'שגרתית · ROUTINE', 'red', 30))))
    card('s04_q144', 'שידור מהספינה?', body, 'אף תשובה', 'NAVTEX בספינה הוא מקלט בלבד. אי אפשר לשדר ממנו שום הודעה.',
         ('שאלה מהמאגר · 144', 'אילו הודעות ניתן לשדר במכשיר NAVTEX מהספינה?',
          ['מצוקה (VITAL)', 'בטיחות, דחופות (IMPORTANT)', 'שגרתיות (ROUTINE)', 'אף תשובה לא נכונה'], 3), bg='u15_rx_target', pos='35% 40%', shade=0.1)

def s05():
    t = tile('518 kHz', 'בינלאומי · אנגלית', 'green', 'h-[230px]', 58, 28) + tile('490 kHz', 'שפה מקומית', 'sky', 'h-[230px]', 58, 28)
    body = (at(24, 24, chip('MF · תדר בינוני', 'amber', 38))
            + bottom(glass(f'<div class="p-6 space-y-5"><div class="grid grid-cols-2 gap-4">{t}</div>'
                           + row('✗', 'לא VHF · לא מכשיר הקשר', 'red', 28) + row('↗', 'מתפשט מעבר לאופק · טווח גדול', 'green', 28) + '</div>')))
    card('s05_freq', 'תדרי NAVTEX', body, '518 ו-490', 'NAVTEX עובד בתדר בינוני, MF. 518 קילו הרץ באנגלית, 490 בשפה המקומית.',
         bg='u15_rx_printer', pos='80% 30%', shade=0.3)

def s06():
    f = [('MF', 'תדר בינוני · NAVTEX', 'green'), ('S.F.', 'אין תחום כזה', 'red'), ('X-BAND', 'מכ״מ', 'red'), ('VHF', 'מכשיר הקשר', 'red')]
    card('s06_q117', 'תחום התדרים', grid(''.join(tile(n, s, t, 'h-[230px]', 56, 28) for n, s, t in f)), 'M.F.', 'NAVTEX קולט בתדר בינוני. VHF הוא מכשיר הקשר, ו-X-BAND הוא מכ״מ.',
         ('שאלה מהמאגר · 117', 'על איזה תחום תדרים קולט מכשיר ה-NAVTEX?', ['M.F.', 'S.F.', 'X-BAND שמכ״ם יקלוט', 'VHF'], 0), bg='u15_rx_printer', shade=0.8)

def slots(active=None):
    cells = ''.join(f'<div class="flex-1 h-[86px] rounded-xl {"bg-emerald-500" if c == active else "bg-slate-700/90"} flex items-center justify-center text-white font-extrabold text-[38px] ltr">{c}</div>'
                    for c in 'ABCDEFGH')
    return f'<div class="flex gap-2" dir="ltr">{cells}</div>'

COORD = [('I', 'בריטניה'), ('II', 'צרפת'), ('III', 'ספרד'), ('IV', 'ארה״ב · מזרח'), ('V', 'ברזיל'), ('VI', 'ארגנטינה'), ('VII', 'דרום אפריקה'),
         ('VIII', 'הודו'), ('IX', 'פקיסטן'), ('X', 'אוסטרליה'), ('XI', 'יפן'), ('XII', 'ארה״ב · מערב'), ('XIII', 'רוסיה'), ('XIV', 'ניו זילנד'),
         ('XV', 'צ׳ילה'), ('XVI', 'פרו'), ('XVII', 'קנדה'), ('XVIII', 'קנדה'), ('XIX', 'נורווגיה'), ('XX', 'רוסיה'), ('XXI', 'רוסיה')]

def s07():
    cell = lambda n, c: (f'<div class="flex items-center gap-2 rounded-lg px-2 py-1 {"bg-emerald-500" if n == "III" else "bg-slate-800/80"}">'
                         f'<span class="ltr font-extrabold text-amber-300 w-[74px] text-[27px]{" text-white" if n == "III" else ""}">{n}</span>'
                         f'<span class="text-white font-semibold text-[27px]">{c}</span></div>')
    body = (f'<img src="{T.asset("u15_navarea")}" class="absolute inset-x-0 top-0 w-full h-[600px] object-cover" style="object-position:50% 45%">'
            + at(20, 20, chip('21 אזורי NAVAREA', 'sky', 30))
            + '<div class="absolute ltr text-white/70 text-[16px]" style="right:10px;top:574px">Map: Chrumps · CC0</div>'
            + '<div class="absolute inset-x-4 bottom-4 top-[612px] rounded-2xl bg-slate-950/90 p-3 flex flex-col gap-2">'
            + '<div class="text-white text-[30px] font-bold">מתאם אזורי · אנחנו ב-III, המתאם ספרד · עד 24 תחנות A-Z</div>'
            + '<div class="grid grid-cols-3 gap-1.5">' + ''.join(cell(n, c) for n, c in COORD) + '</div></div>')
    card('s07_areas', 'אזורים ומתאמים', body, '21 אזורים', 'לכל אזור מתאם. אנחנו באזור III, והמתאם ספרד. התחנות על אותו תדר, עשר דקות כל ארבע שעות.')

def s08():
    body = '<div class="absolute inset-6 flex flex-col justify-center gap-6">' + tile('4 שעות', 'כל תחנה · תור קבוע', 'green', 'h-[330px]', 96, 34) + slots('B') + '</div>'
    card('s08_q66', 'כל כמה זמן', body, 'כל 4 שעות', 'כל תחנה מחכה לתור שלה, והתור חוזר כל ארבע שעות.',
         ('שאלה מהמאגר · 66', 'כל כמה זמן מתקבל שידור NAVTEX מתחנת חוף מסוימת?', ['כל חצי שעה', 'כל 4 שעות', 'כל שעתיים', 'כל 8 שעות'], 1),
         bg='u15_hvar_mast', pos='70% 50%', shade=0.75)

def s09():
    f = [('כל 4 שעות', 'תדירות', 'green'), ('10 דקות', 'לכל היותר', 'green'), ('6×', 'ביממה', 'sky'), ('✗', 'לא 15 דקות · לא דקה', 'red')]
    card('s09_q130', 'כמה ולכמה זמן', grid(''.join(tile(n, s, t, 'h-[230px]', 52, 28) for n, s, t in f)), 'תשובה ב', 'כל ארבע שעות, עשר דקות לכל היותר. החלון מוגבל.',
         ('שאלה מהמאגר · 130', 'כמה פעמים ולכמה זמן תשדר תחנת NAVTEX ביממה אחת?',
          ['כל 6 שעות, עד 15 דקות', 'כל 4 שעות, עד 10 דקות', '4 פעמים, כמה שנחוץ', '6 פעמים, דקה אחת'], 1), bg='u15_hvar_mast', pos='70% 50%', shade=0.8)

def s10():
    circ = lambda x, tone: (f'<div class="absolute rounded-full border-[6px] {tone} flex items-center justify-center" style="left:{x}px;top:150px;width:520px;height:520px">'
                            f'<div class="w-6 h-6 rounded-full bg-white"></div></div>')
    body = (at(24, 24, chip('בלי חפיפה מפריעה · בתאום', 'green', 32))
            + circ(60, 'border-emerald-400 bg-emerald-500/15') + circ(580, 'border-sky-400 bg-sky-500/15')
            + '<div class="absolute ltr text-white font-bold text-[40px]" style="left:200px;top:690px">~400 NM</div>'
            + '<div class="absolute ltr text-amber-300 font-bold text-[40px]" style="left:430px;top:770px">← ~800 NM →</div>'
            + bottom(glass('<div class="p-5 text-white text-[34px] font-semibold text-center">אותו תדר · זמנים שונים</div>')))
    card('s10_q167', 'שרשרת המשדרים', body, 'תשובה ג', 'כ-400 מייל לכל משדר, בלי חפיפה מפריעה עם הסמוך, ובתאום בין המינהלות.',
         ('שאלה מהמאגר · 167', 'כיצד פרושה שרשרת המשדרים של מערך ה-NAVTEX?',
          ['יציאה מטווח אחד לחפיפה של סמוך', 'הצלבה משלושה משדרים בכל שיט', 'כ-400 מייל לכל משדר, בלי חפיפה מפריעה, בתאום', 'אותן שעות, על תדרים שונים'], 2),
         bg='u15_hvar_mast', pos='70% 50%', shade=0.85)

TYPES = [('A', 'אזהרת ניווט', 'red'), ('B', 'אזהרת מזג אוויר', 'red'), ('D', 'חיפוש והצלה', 'red'), ('L', 'אזהרת ניווט נוספת', 'red'),
         ('E', 'תחזית · מומלץ', 'amber'), ('C', 'דיווח קרח', 'slate'), ('Z', 'אין הודעות', 'slate'), ('…', 'ועוד', 'slate')]

def s11():
    body = at(24, 24, chip('🔒 A · B · D · L · אי אפשר לבטל', 'red', 30)) + grid(''.join(tile(n, s, t, 'h-[190px]', 64, 24) for n, s, t in TYPES), 2, top=130)
    card('s11_types', 'סוגי הודעות', body, 'A, B, D, L', 'כל הודעה מסומנת באות. ארבעה סוגים אי אפשר לבטל, וכדאי להוסיף את E, התחזית.',
         bg='u15_rx_printer', shade=0.8)

MAYDAY = flow([('כלי שייט במצוקה', 'red'), ('תחנת חוף · מינהלה אזורית', 'sky'), ('NAVTEX · הודעת D', 'amber'), ('כל הספינות באזור', 'green')])

def s12():
    body = f'<div class="absolute inset-x-10 inset-y-8 flex flex-col justify-center">{MAYDAY}</div>'
    card('s12_q83', 'מצוקה ב-NAVTEX', body, 'תשובה ב', 'תחנות החוף מפיצות את המצוקה ב-NAVTEX, כדי שיותר ספינות יוכלו לעזור.',
         ('שאלה מהמאגר · 83', 'הודעות מצוקה שמופיעות בפלט מקלט NAVTEX:',
          ['מכלי השיט שבמצוקה, לתחנות חוף בלבד', 'מתחנות חוף ומהמינהלה האזורית, להרחיב את מי שיכול לעזור', 'מתחנות חוף וכלי שיט שקלטו ערוץ 16', 'חל איסור להפיץ מצוקה ב-NAVTEX'], 1),
         bg='u15_hvar_mast', pos='70% 50%', shade=0.55)

def s13():
    body = at(24, 24, chip('אותה שאלה · נוסח אחר', 'amber', 32)) + f'<div class="absolute inset-x-10 bottom-8 top-[130px] flex flex-col justify-center">{MAYDAY}</div>'
    card('s13_q168', 'מצוקה ב-NAVTEX', body, 'תשובה ב', 'מקורן בתחנות חוף ובמינהלה האזורית, כדי להרחיב את מספר העוזרים.',
         ('שאלה מהמאגר · 168', 'כיצד מופיעות הודעות מצוקה בפלט מקלט NAVTEX?',
          ['מכלי השיט שבמצוקה, לתחנות חוף בלבד', 'מתחנות חוף ומהמינהלה האזורית, להרחיב את מי שיכול לעזור', 'מתחנות חוף וכלי ים שקלטו ערוץ 16', 'חל איסור להפיץ מצוקה ב-NAVTEX'], 1),
         bg='u15_hvar_mast', pos='70% 50%', shade=0.55)

PRI = [('VITAL', 'חיונית · משודרת מיד', 'red'), ('IMPORTANT', 'חשובה · בחלון הפנוי הראשון', 'amber'), ('ROUTINE', 'שגרתית · בשידור המתוכנן הבא', 'slate')]

def pri_tiles(sub=True):
    return ''.join(tile(n, s if sub else s.split(' · ')[0], t, 'h-[200px]', 56, 28) for n, s, t in PRI)

def s14():
    body = (f'<div class="absolute inset-x-6 top-6 space-y-4">{pri_tiles()}</div>'
            + bottom(glass('<div class="p-5 flex items-center gap-5">' + digits([('00', 'red', 'מספר סידורי')]) + '<div class="text-white text-[36px] font-bold">תמיד נקלטת · אי אפשר לסנן</div></div>')))
    card('s14_priority', 'דרגות עדיפות', body, 'עדיפות', 'VITAL משודרת מיד, IMPORTANT בחלון הפנוי הראשון, ROUTINE בשידור המתוכנן הבא.',
         bg='u15_rx_printer', shade=0.8)

def s15():
    body = f'<div class="absolute inset-6 flex flex-col justify-center gap-4">{pri_tiles(False)}</div>'
    card('s15_q84', 'VITAL · IMPORTANT · ROUTINE', body, 'תשובה א', 'סיווג העדיפות של הודעות NAVTEX עצמו. לא מקביל לדרגות בקשר הקולי.',
         ('שאלה מהמאגר · 84', 'VITAL, IMPORTANT, ROUTINE הם:',
          ['"חיונית", "חשובה", "שגרתית" בהודעות NAVTEX', '"מיוחדת", "מיידית", "דחופה"', 'מקבילים למצוקה, דחיפות ובטיחות בדיבור', 'כל התשובות נכונות'], 0),
         bg='u15_rx_printer', shade=0.8)

def s16():
    body = at(24, 24, chip('אותה שאלה · נוסח אחר', 'amber', 32)) + f'<div class="absolute inset-x-6 bottom-6 top-[130px] flex flex-col justify-center gap-4">{pri_tiles(False)}</div>'
    card('s16_q119', 'VITAL · IMPORTANT · ROUTINE', body, 'תשובה א', 'סיווג עדיפות ותוכן של הודעות NAVTEX. לא VHF ולא EPIRB.',
         ('שאלה מהמאגר · 119', 'למה מתייחסות ההודעות מסוג VITAL, IMPORTANT, ROUTINE?',
          ['"חיונית", "חשובה", "שגרתית" בהודעות NAVTEX', 'ROUTINE ו-IMPORTANT במקלט ה-VHF', 'מקבילים למצוקה, דחיפות ובטיחות ב-EPIRB', 'כל התשובות נכונות'], 0),
         bg='u15_rx_printer', shade=0.8)

def s17():
    body = ('<div class="absolute inset-6 flex flex-col justify-between gap-4">' + glass(MSG)
            + glass('<div class="p-5">' + digits([('H', 'sky', 'תחנה'), ('A', 'amber', 'סוג'), ('01', 'green', 'מספר סידורי')]) + '</div>') + '</div>')
    card('s17_format', 'מבנה הודעה', body, 'ZCZC ... NNNN', 'ZCZC פותח, אחריו תחנה, סוג ומספר. אחר כך תאריך, שעה וטקסט. NNNN סוגר, ו-CER הוא אחוז השגיאה.',
         bg='u15_rx_printer', shade=0.85)

def s18():
    body = ('<div class="absolute inset-6 flex flex-col justify-center gap-6">' + glass('<div class="p-8">' + digits([('M', 'sky', 'תחנה'), ('A', 'amber', 'אזהרת ניווט'), ('33', 'green', 'מספר סידורי')]) + '</div>')
            + rows(('✗', 'לא אות קריאה', 'red', 28), ('✗', 'לא קוד מדינה', 'red', 28), ('✗', 'DSC · 9 ספרות MMSI', 'red', 28)) + '</div>')
    card('s18_q129', 'MA33', body, 'קוד הודעה', 'M היא התחנה, A אזהרת ניווט, 33 המספר הסידורי. קוד זיהוי של הודעת NAVTEX.',
         ('שאלה מהמאגר · 129', 'מה מציין הקוד MA33?',
          ['אות קריאה של אניית רדיו-טלפון', 'קוד זיהוי של הודעת נווטקס', 'תחנת חוף של מדינה "MA"', 'קוד זיהוי של אתר DSC לאזהרת נווט'], 1),
         bg='u15_rx_printer', shade=0.85)

def s19():
    body = (at(24, 24, chip('לפני ההפלגה', 'green', 36))
            + bottom(rows(('1', 'הפעלה 6 שעות לפני', 'green', 30), ('2', 'בדיקת תקינות', 'green', 30), ('3', 'תחנות רלוונטיות לאזור', 'sky', 30), ('4', 'סוגי הודעות', 'sky', 30))
                     + '<div class="flex gap-3 pt-4">' + chip('ספר מפעיל', 'slate', 26) + chip('אדמירליטי כרך 5', 'slate', 26) + '</div>'))
    card('s19_predeparture', 'הכנה לפני הפלגה', body, 'שש שעות מראש', 'כך נקלט סבב שלם מכל התחנות. מגדירים תחנות וסוגי הודעות.',
         bg='u15_rx_target', pos='35% 40%', shade=0.1)

def s20():
    body = (at(24, 24, chip('מה מגדירים', 'green', 36))
            + bottom(rows(('✓', 'התחנות', 'green', 32), ('✓', 'סוגי ההודעות', 'green', 32), ('✗', 'זמני קליטה · המכשיר קולט לבד', 'red', 28), ('✗', 'בטיחות · נקלטת בכל מקרה', 'red', 28))))
    card('s20_q71', 'מה מתקינים', body, 'תשובה ב', 'מגדירים תחנות וסוגי הודעות. אין זמני קליטה לבחור.',
         ('שאלה מהמאגר · 71', 'מה רצוי להתקין במכשיר NAVTEX לפני הפלגה?',
          ['אזור ההפלגה וזמני הקליטה', 'התחנות וסוגי ההודעות המבוקשים', 'סוג הודעות בטיחות ודחיפות', 'השעות לקליטת תחזית'], 1), bg='u15_rx_target', pos='35% 40%', shade=0.1)

def s21():
    im, d = base()
    d = photo(im, (0, 0, 1300, 1440), 'u15_rx_printer', focus=(0.45, 0.5)); credit(d, (0, 0, 1300, 1440), 'u15_rx_printer')
    text_c(d, 1880, 150, 'סיכום', F(120), TEXT)
    d.rounded_rectangle((1810, 310, 1950, 322), 6, fill=GREEN)
    items = ['הודעות כתובות · אוטומטי', 'ביאכטה · מקלט בלבד', 'MF · 518 kHz באנגלית', '10 דקות · כל 4 שעות',
             'טווח · כ-400 מייל', 'A, B, D, L · אי אפשר לבטל', 'מצוקה · מתחנות החוף', 'לפני הפלגה · 6 שעות מראש']
    for i, s in enumerate(items):
        y = 370 + i * 112
        d.rounded_rectangle((1360, y, 2460, y + 92), 20, fill=PANEL)
        dot(d, (2420, y + 46), 12, GREEN_L if i < 5 else C.ORANGE)
        text_r(d, 2380, y + 20, s, F(46, False), TEXT)
    save(im, 's21_summary')

ALL = [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21]
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
