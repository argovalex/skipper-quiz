"""Render one l40 lesson with the l30 pipeline: el_tts (Alex's voice) -> assemble -> brand -> companion -> burned subtitles.
usage: python render_lesson.py "<lesson folder name>" <work_dir>
Only sections whose text changed are re-voiced (el_tts caches per section)."""
import os, re, sys, subprocess
ROOT = r'C:/Users/argov/OneDrive/Co-Work OS/SkipperQuiz'
L30 = ROOT + '/lessons/l30/sources'; sys.path.insert(0, L30)
import nowin  # child processes without a console window
NUM = {'ציוד ובדיקות GMDSS': None, 'מבוא ל-GMDSS': 1, 'השלמות למבחן GMDSS': 8, 'פתרון שאלות המבחן': None, 'ערוצים ו-DSC - השלמות למבחן': None, 'נהלים ופונטיקה - השלמות למבחן': None, 'NAVTEX - השלמות למבחן': None, 'כותבים נוהל מצוקה': 9}
HEADINGS = {
    'ציוד ובדיקות GMDSS': {'s01_intro': 'פתיחה', 's02_sart': 'SART', 's07_satellites': 'הלוויינים', 's14_epirb': 'EPIRB', 's24_batteries': 'מצברים', 's28_checks': 'בדיקות הציוד', 's33_summary': 'סיכום'},
    'מבוא ל-GMDSS': {'s01_intro': 'פתיחה', 's02_titanic': 'הטיטאניק', 's03_gmdss_born': 'איך נולדה GMDSS', 's04_principle': 'העיקרון: לחיצה אחת',
                     's05_who_needs': 'מי צריך את זה', 's06_exam': 'מבנה המבחן', 's07_areas_intro': 'אזורי הים', 's08_area_a1a2': 'A1 ו-A2',
                     's09_area_a3a4': 'A3 ו-A4', 's10_exam_trap': 'המלכודת: חמישה מייל מהחוף', 's11_q16': 'שאלה 16: ציוד באזור A1',
                     's12_course_map': 'מפת הקורס', 's13_summary': 'סיכום'},
    'פתרון שאלות המבחן': {'s01_intro': 'פתיחה', 's02_channels': 'הערוצים', 's03_g17': 'G17: ערוץ 16', 's04_g3': 'G3: וואט אחד מקסימום', 's05_portable': 'המכשיר הנייד',
                          's06_g4': 'G4: ההצהרה השגויה', 's07_priorities': 'העדיפויות בקשר', 's08_g9': 'G9: PAN PAN', 's09_g7': 'G7: שלוש פעמים SECURITE',
                          's10_g14': 'G14: עדיפות בטיחות', 's11_g18': 'G18: תקשורת דחיפות', 's12_silence': 'קודי השתקה', 's13_g10': 'G10: סיום מצוקה',
                          's14_ais': 'AIS', 's15_g5': 'G5: מה פירוש AIS', 's16_navtex': 'עדיפויות ב-NAVTEX', 's17_g13': 'G13: רמות NAVTEX',
                          's18_log': 'יומן הרדיו', 's19_g12': 'G12: היכן נשמר היומן', 's20_mmsi': 'MMSI', 's21_g20': 'G20: זיהוי של ספינה', 's22_summary': 'סיכום'},
    'ערוצים ו-DSC - השלמות למבחן': {'s01_intro': 'פתיחה', 's02_channels': 'הערוצים', 's02_ch70': 'ערוצים דיגיטליים', 's02_ch17': 'קשר על הסיפון', 's02_ch11': 'כלי שייט קטנים ונמלים', 's02_ch16': 'ערוץ 16', 's15_mmsi': 'MMSI', 's28_summary': 'סיכום'},
    'נהלים ופונטיקה - השלמות למבחן': {'s01_intro': 'פתיחה', 's02_alpha': 'האלפבית הפונטי', 's02_phonetic': 'ספרות ואותיות', 's09_call': 'קריאה לתחנה', 's04_callsign': 'הקידומת 4X', 's16_words': 'מונחי רדיוטלפון', 's25_medical_terms': 'מונחים רפואיים', 's33_pubs': 'פרסומים', 's20_priorities': 'העדיפויות',
                                      's27_mayday_terms': 'מונחי מצוקה', 's37_summary': 'סיכום'},
    'כותבים נוהל מצוקה': {'s01_intro': 'פתיחה', 's02_part_a': 'החלק הראשון במבחן', 's03_step1_epirb': 'סעיף 1: EPIRB', 's04_step2_dsc': 'סעיף 2: DSC', 's05_dsc_why': 'סוג האירוע',
                          's06_step3_mayday': 'סעיף 3: MAYDAY בקול', 's07_position': 'המיקום', 's08_example': 'דוגמה', 's09_ack': 'אישור קבלה', 's10_step4_abandon': 'סעיף 4: נטישה',
                          's11_scenario_fire': 'תרחיש: שריפה', 's11_sondra': 'SONDRA', 's12_scenario_grounding': 'תרחיש: שרטון', 's12_simulator': 'הסימולטור',
                          's13_checklist': 'רשימת בדיקה', 's14_summary': 'סיכום'},
    'NAVTEX - השלמות למבחן': {'s01_intro': 'פתיחה', 's02_basics': 'NAVTEX: היסודות', 's14_alrs': 'הפרסום', 's15_header': 'מבנה ההודעה', 's17_cer': 'C E R',
                              's18_codes': 'סוגי הודעות', 's23_summary': 'סיכום'},
    'השלמות למבחן GMDSS': {'s01_intro': 'פתיחה', 's02_functions': 'הדרישות התפקודיות', 's03_q11': 'שאלה 11: דרישה תפקודית', 's04_onscene': 'On-Scene: תקשורת במקום האירוע',
                           's05_q19': 'שאלה 19: On-Scene Communications', 's06_q8': 'שאלה 8: הערוץ במקום האירוע', 's07_cospas': 'מסלול אות המצוקה',
                           's08_q15': 'שאלה 15: מי קובע את המיקום', 's09_false_epirb': 'EPIRB שנדלקה בטעות', 's10_q6': 'שאלה 6: אתרעת שווא',
                           's11_sart': 'הטווח של ה-SART', 's12_q1': 'שאלה 1: להגדיל את הטווח', 's13_traffic': 'Traffic List: רשימת תעבורה',
                           's14_q2': 'שאלה 2: רשימת תעבורה', 's15_summary': 'סיכום'}}
NAME, W = sys.argv[1], sys.argv[2]
D = ROOT + '/lessons/l40/cards/' + NAME; AUD = os.path.join(W, 'aud'); RAW = os.path.join(W, 'lesson_raw.mp4')
py = sys.executable
run = lambda *a: subprocess.run([py, *a], check=True)
# Alex 2026-10-15: "לָמָה לא א'/ב'/ג'/ד'" is always לָמָה; the lexicon would give לֶמָה, so vo.txt must carry the niqqud.
if re.search(r"למה(?= לא [אבגד]['׳])", open(D + '/vo.txt', encoding='utf-8').read()):
    sys.exit("vo.txt: write 'לָמָה לא <letter>'' with niqqud")
run(L30 + '/el_tts.py', D + '/vo.txt', AUD)
run(ROOT + '/tools/lesson/assemble.py', '--vo', D + '/vo.txt', '--audio', AUD, '--cards', D, '--out', RAW)
run(ROOT + '/tools/lesson/brand.py', RAW, os.path.join(D, NAME + '.mp4'))
txt = os.path.join(D, NAME + '.txt')
run(L30 + '/companion.py', D + '/vo.txt', txt, f'{NAME} · קורס GMDSS' + (f' · שיעור {NUM[NAME]}' if NUM[NAME] else ''))
t = open(txt, encoding='utf-8').read()
def _head(m):
    sid = m.group(1)
    if sid in HEADINGS[NAME]: return '# ' + HEADINGS[NAME][sid]
    k = re.match(r's\d\d_q(\d+)(_ask|_a_q)?$', sid)
    return '# ' + ('שאלה ' + k.group(1) + {'_ask': ' (השאלה)', '_a_q': ' (התשובה)'}.get(k.group(2), '')) if k else m.group(0)
t = re.sub(r'^# (s\d\d\w*)$', _head, t, flags=re.M)
open(txt, 'w', encoding='utf-8').write(t)
os.environ['SUBS_WORK'] = os.path.join(W, 'subs'); os.environ['SUBS_PLAIN'] = '1'; os.environ['SUBS_SPOKEN'] = '1'   # Alex 2026-10-18: burned subtitles without niqqud
run(L30 + '/subs.py', D + '/vo.txt', AUD, os.path.join(D, NAME + '.mp4'), os.path.join(D, NAME + ' - כתוביות.mp4'))
r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(D, NAME + '.mp4')], capture_output=True, text=True)
print(f'DONE {float(r.stdout.strip()):.0f}s', flush=True)
