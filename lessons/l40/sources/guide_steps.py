"""User guide for the GMDSS simulator: one source for the VO (simulator/guide/vo.txt, el_tts format) and the on-screen text
(injected into simulator/index.html between /*GUIDE*/ markers).
usage: python guide_steps.py          -> writes vo.txt + updates index.html
       python guide_steps.py --audio  -> also voices it (Alex's voice, tools/voice/voice.js) into simulator/audio/guide/seg_<id>.mp3"""
import os, re, sys, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); SIM = os.path.join(HERE, '..', 'simulator')
# (id, title, target selector, demo, VO text). On-screen text = VO without niqqud and with spelled acronyms joined.
STEPS = [
 ('g01', 'התרחיש', None, None, 'ברוך הבא לסימולטור G M D S S. אתה הסקיפר של היאכטה סונדרה, ארבעה אנשים על הסיפון. פרצה שריפה בחדר המכונות, והיא יוצאת משליטה. המשימה שלך: לשלוח התראת מצוקה, לשדר MAYDAY, לנטוש לרפסודה, ולהביא אליך את ספינת החילוץ. בוא נעבור על זה צעד אחר צעד.'),
 ('g02', 'שורת ההדרכה', '#coach', None, 'בראש המסך יש שורת הדרכה. במצב תרגול היא אומרת לך בכל רגע מה הצעד הבא. במצב מבחן היא נעלמת, ואתה לבד.'),
 ('g03', 'הדלקת ה-VHF', '#kPwr', None, 'הצעד הראשון: מדליקים את מכשיר ה V H F. לחיצה על PWR מדליקה אותו, והוא עולה ישר על ערוץ שש עֶשְׂרֵה. החזקה של שנייה מכבה אותו.'),
 ('g04', 'המסך', '.lcd', None, 'על המסך רואים את הערוץ, ולידו את המיקום מה G P S ואת השעה. את המיקום הזה תקריא ב MAYDAY.'),
 ('g05', 'מכסה DISTRESS', '.dwrap', 'cover', 'עכשיו התראת D S C. כפתור DISTRESS מוגן במכסה אדום, כדי שלא ילחצו עליו בטעות. פותחים את המכסה.'),
 ('g06', 'בחירת מהות', '.bottom', None, 'לחיצה קצרה על DISTRESS פותחת את רשימת מהות האירוע. בוחרים עם החצים FIRE EXPLOSION, שריפה אוֹ פיצוץ, ומאשרים בכפתור העגול.'),
 ('g07', 'שליחת ההתראה', '.dwrap', 'cover', 'ואז מחזיקים את DISTRESS חמש שניות, עד שכל חמשת הריבועים על המסך מתמלאים. ההתראה יוצאת בערוץ שבעים, עם ה MMSI והמיקום, והמכשיר עובר לבד לערוץ שש עֶשְׂרֵה. אחרי כמה שניות תשמע צפצוף: אישור מחיפה רדיו.'),
 ('g08', 'MAYDAY בקול', '#voice', None, 'עכשיו MAYDAY בקול. מתחת למכשיר יש תיבת שידור. לוחצים ומחזיקים את הכפתור הגדול עם המיקרופון, מדברים באנגלית ברור, ומשחררים בסוף. המערכת מזהה את הדיבור. אם אין מיקרופון, מקלידים בשורה שמתחת ולוחצים שדר.'),
 ('g09', 'תבנית MAYDAY', '#tpl', 'tpl', 'שוכח את הסדר? הכפתור תבנית MAYDAY מציג את הנוסח המלא: שלוש פעמים MAYDAY, זיהוי, MMSI, מיקום, מה קרה, איזו עזרה, כמה אנשים, ו Over. במבחן הכפתור הזה לא קיים.'),
 ('g10', 'עוצמה ומשקט רחש', '.knobs', None, 'שים לב לעוצמה ולמשקט הרחש. בעוצמה אפס, אוֹ במשקט גבוה מדי, לא תשמע את תחנת החוף, והשידור ייחשב כפספוס. ובזמן מצוקה נשארים בערוץ שש עֶשְׂרֵה.'),
 ('g11', 'EPIRB', '#epirb', None, 'תחנת החוף תודיע שספינת חילוץ בדרך, והאש תצא משליטה. נוטשים. מפעילים את ה EPIRB: משחררים מהתושבת, מרימים את המגן ולוחצים ON, אוֹ מכניסים למים. אחרי כחמישים שניות יוצאת התראה ללוויין.'),
 ('g12', 'SART', '#sart', None, 'לוקחים את ה SART לרפסודה, מפעילים ON, ומרימים אותו על המוט. SART גבוה נקלט במכ"ם מרחוק יותר. לחיצה על TEST מדגימה במכ"ם, אוטומטית, איך הוא נראה.'),
 ('g13', 'המכ"ם', '#radar', None, 'כאן המכ"ם של ספינת החילוץ. כשה SART פועל, הסימולציה עוברת למהירות פי ארבע. מרחוק תראה שתים עֶשְׂרֵה נקודות בקו. ככל שהספינה מתקרבת הן הופכות לקשתות, ובסוף למעגלים שלמים. אפשר לגרור את הסליידר כדי לקרב ולהרחיק.'),
 ('g14', 'עונים לתחנות', '#log', None, 'תחנות יקראו לך: R C C חיפה, וספינת החילוץ. עונים להן עם שם הכלי, מדווחים שאתם ברפסודה, ומסיימים ב Over. כל השידורים נרשמים ביומן הקשר.'),
 ('g15', 'תרגול ומבחן', '#mPractice', None, 'בסוף מקבלים סיכום עם ציון וכל מה שפוספס. מתחילים בתרגול, וכשאתה מוכן עוברים למבחן. בהצלחה.'),
]
SHOW = [('G M D S S', 'GMDSS'), ('V H F', 'VHF'), ('D S C', 'DSC'), ('G P S', 'GPS'), ('R C C', 'RCC'), ('סונדרה', 'SONDRA'), ('מחיפה רדיו', 'מ-HAIFA RADIO'),
        ('ה EPIRB', 'ה-EPIRB'), ('ה SART', 'ה-SART'), ('ה MMSI', 'ה-MMSI'), ('ה VHF', 'ה-VHF'), ('ה GPS', 'ה-GPS'), ('ב MAYDAY', 'ב-MAYDAY'), ('ב Over', 'ב-Over'), ('ו Over', 'ו-Over'),
        ('FIRE EXPLOSION', 'FIRE/EXPLOSION')]
def show(t):
    t = re.sub('[\u0591-\u05C7]', '', t)
    for a, b in SHOW: t = t.replace(a, b)
    return t

vo = os.path.join(SIM, 'guide', 'vo.txt'); os.makedirs(os.path.dirname(vo), exist_ok=True)
if os.path.isfile(vo):   # vo.txt is the source of truth for the wording (Alex edits it); STEPS only supply title/target/demo
    sec = dict(re.findall(r'^## (\w+)\n(.*?)\n*(?=^## |\Z)', open(vo, encoding='utf-8').read(), flags=re.S | re.M))
    STEPS = [(i, t, s, d, sec.get(i, v).strip()) for i, t, s, d, v in STEPS]
else:
    open(vo, 'w', encoding='utf-8').write('\n'.join(f'## {i}\n{v}\n' for i, _, _, _, v in STEPS))
js = 'const GUIDE=' + json.dumps([{'id': i, 't': t, 'sel': s, 'demo': d, 'txt': show(v)} for i, t, s, d, v in STEPS], ensure_ascii=False) + ';'
p = os.path.join(SIM, 'index.html'); h = open(p, encoding='utf-8').read()
h = re.sub(r'/\*GUIDE\*/.*?/\*/GUIDE\*/', lambda m: '/*GUIDE*/' + js + '/*/GUIDE*/', h, flags=re.S)
open(p, 'w', encoding='utf-8').write(h)
if '--audio' in sys.argv:
    out = os.path.join(SIM, 'audio', 'guide'); os.makedirs(out, exist_ok=True)
    subprocess.run(['node', os.path.join(HERE, '..', '..', '..', 'tools', 'voice', 'voice.js'), 'segments', vo, out], check=True)  # Alex's ElevenLabs clone, same as all lessons
print('ok')
