"""Re-render l30 lessons in Alex's voice (ElevenLabs clone). Old outputs move to <lesson>/_old/ (nothing deleted).
usage: python render_course.py <work_dir> [lesson-number ...]   (default: all)"""
import os, sys, shutil, subprocess
ROOT = r'C:/Users/argov/OneDrive/Co-Work OS/SkipperQuiz'
CARDS = ROOT + '/lessons/l30/cards'
SRC = ROOT + '/lessons/l30/sources'
LESSONS = {1: 'הרשת הגיאוגרפית', 2: 'המפה הימית ומרקטור', 3: 'אזורי זמן', 4: 'אופק כוכבים וכוכב הצפון', 5: 'מצפן מגנטי', 6: "מצפן ג'יירו ושער שטף"}
TITLES = {1: 'הרשת הגיאוגרפית', 2: 'המפה הימית ומרקטור', 3: 'אזורי זמן', 4: 'אופק, כוכבים וכוכב הצפון', 5: 'מצפן מגנטי', 6: "מצפן ג'יירו ושער שטף"}
W = sys.argv[1]
which = [int(a) for a in sys.argv[2:]] or sorted(LESSONS)
py = sys.executable
for n in which:
    name = LESSONS[n]; d = os.path.join(CARDS, name); aud = os.path.join(W, f'l30u{n}el', 'aud')
    print(f'=== lesson {n}: {name}', flush=True)
    subprocess.run([py, SRC + '/el_tts.py', d + '/vo.txt', aud], check=True)
    old = os.path.join(d, '_old'); os.makedirs(old, exist_ok=True)
    for f in os.listdir(d):
        if f.endswith(('.mp4', '.srt')) or (f.endswith('.txt') and f != 'vo.txt'):
            shutil.move(os.path.join(d, f), os.path.join(old, f))
    raw = os.path.join(W, f'l30u{n}el', 'lesson_raw.mp4')
    subprocess.run([py, ROOT + '/tools/lesson/assemble.py', '--vo', d + '/vo.txt', '--audio', aud, '--cards', d, '--out', raw], check=True)
    subprocess.run([py, ROOT + '/tools/lesson/brand.py', raw, os.path.join(d, name + '.mp4')], check=True)
    subprocess.run([py, SRC + '/companion.py', d + '/vo.txt', os.path.join(d, name + '.txt'),
                    f'{TITLES[n]} · קורס ניווט חופי ומכשירים · שיעור {n}'], check=True)
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', os.path.join(d, name + '.mp4')], capture_output=True, text=True)
    print(f'DONE lesson {n}: {float(r.stdout.strip()):.0f}s', flush=True)
