"""Maps every question in data/l40.json to the l40 lesson that explains it.
direct = question text appears in a lesson card/voiceover; topic = strong keyword overlap with the lesson text; none = not covered.
Writes lesson/lesson_cover fields into data/l40.json and lessons/l40/question-lesson-map.md."""
import json, re, os, difflib, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS = os.path.join(ROOT, 'lessons', 'l40', 'cards')
LESSONS = [('1', 'מבוא ל-GMDSS'), ('2', 'גלי רדיו ומכשיר VHF'), ('3', 'ערוצים, MMSI ו-DSC'), ('4', 'NAVTEX'), ('5', 'EPIRB, SART ו-AIS'),
           ('6', 'נהלי קשר'), ('7', 'נוהל מצוקה'), ('8', 'השלמות למבחן GMDSS'), ('9', 'פתרון שאלות המבחן')]
def strip(s): return re.sub(r'[֑-ׇ]', '', s)
def stem(t):
    while len(t) > 3 and t[0] in 'הובלמש' and t not in STOP: t = t[1:]
    return t
def toks(s):
    s = strip(s).lower()
    return [stem(t) for t in re.findall(r'[a-z]{2,}|[א-ת]{3,}|\d+', s) if t not in STOP]
STOP = set('את של על עם לא כל או אל מה זה הוא היא הם אין יש כי אם אבל גם רק הבא הבאים הבאות איזה איזו מהם מהבאים בעת כאשר ידי לפי'.split())
def norm(s): return re.sub(r'[^\w]', '', strip(s).lower())
txt = {}
for n, name in LESSONS:
    p = os.path.join(CARDS, name, 'vo.txt')
    txt[n] = strip(open(p, encoding='utf-8').read()) if os.path.exists(p) else ''
tok = {n: set(toks(t)) for n, t in txt.items()}
# sentences/chunks of each lesson for direct-match of the question wording
chunks = {n: [norm(c) for c in re.split(r'[.:?\n]', t) if len(norm(c)) > 12] for n, t in txt.items()}
TOPIC = [  # first lesson whose pattern matches the question + correct answer wins; ordered most specific first
    ('1', r'אזור ים|a[1-4]|solas'),
    ('4', r'navtex|נווטקס|navarea|metarea|518|490|\bmsi\b'),
    ('5', r'epirb|gpirb|\bsart\b|\bais\b|ais-sart|cospas|sarsat|\blut\b|\bmcc\b|\bplb\b|406|121\.5|משואה|משואת|לווייני|\bgeo\b|\bmeo\b|\bleo\b|inmarsat|התבייתות|להתביית'),
    ('7', r'mayday|pan.?pan|securit|seelonce|prudonce|feenee|מצוקה|התרעת שווא|דחיפות|נטישה|relay|medico|medical advice|undesignated|disabled|adrift|\bdistress\b'),
    ('3', r'mmsi|\bdsc\b|ערוץ 70|ch ?70|\bmid\b|\bעדיפות routine\b|התרעה'),
    ('6', r'פונטי|tango|\btr\b|\bimot\b|יומן|traffic|רשימת תעבורה|prowords?|\bover\b|\bout\b|קריאה|רישיון|מצבר|סוללה|בדיק|אות קריאה|זיהוי|\beta\b|stand.?by|radio\b'),
    ('2', r'\bvhf\b|\bmf\b|\bhf\b|\bkhz\b|\bmhz\b|תדר|טווח|סימפלקס|simplex|duplex|דופלקס|אנטנה|הספק|squelch|ערוץ|\bch ?\d|\bdw\b|dual.?watch|bridge to bridge|1w'),
    ('1', r'אזור ים|\ba[1-4]\b|\bsolas\b|gmdss|ציוד חובה|דרישות'),
]
def topic(q, ans):
    t = (q['q_he'] + ' ' + ans).lower()
    for n, pat in TOPIC:
        if re.search(pat, t): return n
    return None
Q = json.load(open(os.path.join(ROOT, 'data', 'l40.json'), encoding='utf-8'))
REVIEW = json.load(open(os.path.join(ROOT, 'lessons', 'l40', 'partial-review.json'), encoding='utf-8'))
rows = []
for q in Q:
    qn = norm(q['q_he']); ans = q['options']['אבגדה'.index(q['answer'])][3:]
    best = (0, None)
    for n, cs in chunks.items():
        for c in cs:
            if abs(len(c) - len(qn)) > max(len(qn), len(c)) * .5: continue
            r = difflib.SequenceMatcher(None, qn, c).ratio()
            if r > best[0]: best = (r, n)
    qt = set(toks(q['q_he'])) | set(toks(ans))
    sc = {n: (len(qt & tok[n]) / len(qt) if qt else 0) for n in tok}
    top = sorted(sc, key=sc.get, reverse=True)[0]
    lesson = topic(q, ans)
    if best[0] >= .8: cover, lesson = 'direct', best[1]
    elif lesson is None: cover = 'none'
    elif sc[lesson] >= .6: cover = 'topic'
    elif sc[lesson] >= .4: cover = 'partial'
    else: cover = 'none'
    if cover == 'partial' and str(q['num']) in REVIEW:      # manual review of partial matches (lessons/l40/partial-review.json)
        v = REVIEW[str(q['num'])]; lesson, cover = (str(v), 'topic') if v else (lesson, 'none')
    q['lesson'] = int(lesson) if lesson else None; q['lesson_cover'] = cover
    rows.append((q, cover, lesson, 0, 0))
json.dump(Q, open(os.path.join(ROOT, 'data', 'l40.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
names = dict(LESSONS); cnt = collections.Counter((c) for _, c, *_ in rows)
out = ['# מיפוי שאלות l40 לשיעורים', '', f'סה"כ {len(rows)} שאלות. ' + ', '.join(f'{k}: {v}' for k, v in cnt.items()), '',
       'direct = נוסח השאלה מופיע בשיעור. topic = הנושא והתשובה מכוסים בהקראה (חפיפת מילים 60%+). partial = חפיפה 40%-60% שלא נבדקה ידנית (אחרי הבדיקה הידנית כולן הפכו ל-topic או none). none = לא מכוסה.', '',
       '| מס\' | מקור | שאלה | תשובה | שיעור | כיסוי |', '|---|---|---|---|---|---|']
for q, c, l, r1, r2 in rows:
    out.append(f"| {q['num']} | {q['source']} | {q['q_he'][:70]} | {q['answer']} | {(l + ' ' + names[l]) if l else 'ללא שיעור ייעודי'} | {c} |")
open(os.path.join(ROOT, 'lessons', 'l40', 'question-lesson-map.md'), 'w', encoding='utf-8').write('\n'.join(out))
print(cnt); print(collections.Counter(q['lesson'] for q, *_ in rows))
