"""Render one l40 lesson with the l30 pipeline: el_tts (Alex's voice) -> assemble -> brand -> companion -> burned subtitles.
usage: python render_lesson.py "<lesson folder name>" <work_dir>
Only sections whose text changed are re-voiced (el_tts caches per section)."""
import os, re, sys, subprocess
ROOT = r'C:/Users/argov/OneDrive/Co-Work OS/SkipperQuiz'
L30 = ROOT + '/lessons/l30/sources'; sys.path.insert(0, L30)
import nowin  # child processes without a console window
NUM = {'מבוא ל-GMDSS': 1, 'השלמות למבחן GMDSS': 8}
HEADINGS = {
    'מבוא ל-GMDSS': {'s01_intro': 'פתיחה', 's02_titanic': 'הטיטאניק', 's03_gmdss_born': 'איך נולדה GMDSS', 's04_principle': 'העיקרון: לחיצה אחת',
                     's05_who_needs': 'מי צריך את זה', 's06_exam': 'מבנה המבחן', 's07_areas_intro': 'אזורי הים', 's08_area_a1a2': 'A1 ו-A2',
                     's09_area_a3a4': 'A3 ו-A4', 's10_exam_trap': 'המלכודת: חמישה מייל מהחוף', 's11_q16': 'שאלה 16: ציוד באזור A1',
                     's12_course_map': 'מפת הקורס', 's13_summary': 'סיכום'},
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
run(L30 + '/companion.py', D + '/vo.txt', txt, f'{NAME} · קורס GMDSS · שיעור {NUM[NAME]}')
t = open(txt, encoding='utf-8').read()
t = re.sub(r'^# (s\d\d\w*)$', lambda m: '# ' + HEADINGS[NAME].get(m.group(1), m.group(1)), t, flags=re.M)
open(txt, 'w', encoding='utf-8').write(t)
os.environ['SUBS_WORK'] = os.path.join(W, 'subs'); os.environ['SUBS_PLAIN'] = '1'   # Alex 2026-10-18: burned subtitles without niqqud
run(L30 + '/subs.py', D + '/vo.txt', AUD, os.path.join(D, NAME + '.mp4'), os.path.join(D, NAME + ' - כתוביות.mp4'))
r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(D, NAME + '.mp4')], capture_output=True, text=True)
print(f'DONE {float(r.stdout.strip()):.0f}s', flush=True)
