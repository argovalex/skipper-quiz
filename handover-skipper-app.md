# Handover — SkipperQuiz · אפליקציית הקורס (skipper-app) — 2026-08-16

מסמך העברה לסשן Claude Code הבא. הפרויקט: הפיכת מערכי השיעור ובנק השאלות של רשיון אופנוע ים (L11) לאפליקציית מובייל למכירה.

## מה נבנה בסשן הזה
- נבנתה **אפליקציית מובייל מלאה** (`skipper-app.html`) בעיצוב שאלכס אישר (נייבי‑זהב, Heebo, RTL, מסגרת טלפון). 6 מסכים: Onboarding/Paywall, Home, שיעור בקרוסלת כרטיסים, מבחן, תוצאות, פרופיל + tab bar.
- חובר **בנק השאלות האמיתי**: 13 שיעורים + מבחן מסכם, 192 שאלות מ‑`data/l11.json` ממופות לפי `topic` (מיפוי topic→שיעור), כל שאלה עם `options`/`answer`/`explanation`/`videoUrl`.
- נבנה **מנוע סימולטור**: חזרות מרווחות (SRS, SM‑2 מפושט), גיימיפיקציה (XP, רמות, לבבות, סטריק, צלילי WebAudio, אנימציות), משוב מנומק מיידי על טעות, ותרגול אדפטיבי ("מבחן חיזוק" מהנושאים החלשים).
- **סרטון הסבר לכל שאלה** מוצג עם השאלה (מ‑Cloudinary), מתנגן אוטומטית, **נעצר ב‑`[[PAUSE]]`** וממשיך רק אחרי בחירת תשובה.
- תיקוני UI: הגדלת סרטון השיעור, סרטון השאלה מוצג ביחסו הטבעי (אנכי 9:16), כפתור **"יציאה"** ו‑**"דלג"** במבחן, כפתור **"לשאלות"** לדילוג משיעור.

## החלטות מפתח (לא מובנות מאליהן מהקוד)
- **חיבור שאלות→שיעור = מיפוי topic אחד, בלי תיוג ידני.** כל שאלה כבר נושאת `topic`. המיפוי ב‑JS: `TOPIC→lessonId`. שתי הכרעות: (1) שאלות "סימני יום" יושבות בתוך topic `זכות מעבר` — שיעור 5 מקבל תת‑קבוצה לפי regex על מספרי תמונה 7x/8x/9x. (2) topic `בטיחות` מערבב אש/תדלוק ועזרה ראשונה — פוצל לשיעורים 12/13 לפי טווח `num` (עזרה ראשונה = 1108–1114).
- **עצירת הסרטון ב‑[[PAUSE]] — פתרון זול בלי רינדור מחדש.** מחושב `p` = יחס מיקום ה‑`[[PAUSE]]` בטקסט `voiceover_text` חלקי אורך הטקסט. בזמן ריצה: `pauseAt = p * video.duration`. נשמר כשדה `p` על 59 שאלות שיש בהן `[[PAUSE]]`. **זו הערכה** (מניחה קצב דיבור אחיד, מתעלמת מכרטיס פתיח). השדרוג המדויק: לתפוס את חותמת‑הזמן האמיתית מ‑edge‑tts (WordBoundary offsets) בזמן הרינדור ולשמור `pauseAt` בשניות.
- **גודל סרטון השאלה**: הרילים הם **1080×1920 (אנכי)**. אסור לכפות `aspect-ratio:16/9` — זה ממסגר אותם לפס קטן עם שוליים שחורים. הפתרון: `max-width:100%;max-height:60vh` בלי יחס כפוי → הסרטון מקבל את יחסו הטבעי.
- **התמדה**: `localStorage` עטוף ב‑try/catch (XP, SRS, נושאים חלשים, שיעורים שהושלמו). ב‑Cowork artifact ה‑localStorage עלול להיחסם ואז נופל לזיכרון בלבד. **בפרודקשן ההתמדה עוברת לשרת פר‑משתמש.**

## מצב נוכחי — מה עובד ומה לא
**עובד:** כל 6 המסכים, ניווט, מיפוי 192 שאלות, מנוע SRS/גיימיפיקציה/אדפטיבי, עצירת פאוזה, יציאה/דלג, שמירה מקומית. אומת headless בלי שגיאות JS.
**מודגם בלבד / לא פרודקשן:**
- הסרטונים נטענים מ‑**Cloudinary עם URL ציבורי** (חשוף). לפני גבייה — signed URLs עם תפוגה.
- השאלות **מוטמעות בקובץ** (`LESSON_Q`) לצורך הדגמה. בפרודקשן — `fetch` מ‑Railway מאחורי קוד גישה.
- כפתור "רכוש/התחל" פותח הכל ב‑demo — אין סליקה אמיתית (Tranzila) ואין auth.
- רק **סרטון שיעור אחד** (תמרוני ספינה) הוטמע בגרסת ה‑chat כ‑base64. **בגרסת הריפו הוטמע הווידאו הוסר** (`__VIDEO_DATA__={}`) כדי לא לנפח git — מוצג placeholder עד חיבור Cloudinary.
- `[[PAUSE]]` מבוסס הערכת יחס — עלול לעצור מוקדם/מאוחר בכמה שאלות עד שדרוג ל‑`pauseAt` מדויק.

## מבנה הקוד (`skipper-app.html` — קובץ יחיד)
- `LESSONS[]` — מטא‑דאטה של 13 שיעורים + מבחן מסכם (id, title, kicker, overview, theme, facts[], trap; לשיעור 11 יש `cards[]` ידניים). כרטיסי הקרוסלה נבנים ב‑`buildCards()` מ‑facts+trap אם אין `cards`.
- `<script id="lessonq">` — JSON של `LESSON_Q` (מפתח=lessonId, ערך=מערך שאלות `{num,q,opts,c,exp,vid,p}`).
- `TOPIC→lesson`: הסינון נעשה בסקריפט הפייתון שמייצר את `LESSON_Q` (ראה למטה), לא ב‑JS.
- מנוע: `beginQuiz/startQuiz/startReview/startReinforcement`, `selectAns` (XP/hearts/streak/SRS/topicStats/sfx), `srsLapse/srsPromote/dueNums`, `weakLessons/buildReinforcePool`, `persist/loadPersist`, `sfx/floaty/burst`, `hudHtml`.
- מסכים: `vOnboard/vHome/vLesson/vQuiz/vResults/vProfile/vTab` → `render()` מחליף `#scroll`. אירועים ב‑`bindActions()` (data-act / data-open / data-ans).

## Environment / config
- **ריפו:** `C:\Users\argov\OneDrive\Co-Work OS\SkipperQuiz` · branch `main`.
- **מקור אמת לשאלות:** `data/l11.json` (161 שאלות; 13 topics). **אל תערוך** `questions.json` / `quiz-data-l11.json` / `html/` — נגזרים (ראה `CLAUDE.md`).
- **סרטוני שאלות:** Cloudinary (`res.cloudinary.com/dzmyg9pel/...`) — כבר בשדה `videoUrl` של כל שאלה.
- **סרטוני שיעור:** `lessons/l11/cards/<נושא>/<נושא>.mp4` (רוחביים 1280×720). הרילים של השאלות אנכיים 1080×1920.
- **תוכנית מסחור:** `LAUNCH_PLAN.md` (Railway API, Tranzila, Cloudinary signed URLs, קוד גישה צמוד‑מייל).

## git status (בתחילת ההעברה)
```
 M references/niqqud-lexicon.md
?? .claude/settings.local.json
?? media/בופור סולם.jpg
last: d080580 l11: revise "תמרוני ספינה" — capsize scene + Alex niqqud
      b025385 l11: add lesson "תמרוני ספינה" (7 cards + niqqud companion)
      f28c39b l11: add lesson "סכנות רכיבה ותמרון"
```
> `skipper-app.html` ו‑`handover-skipper-app.md` נכתבו לריפו בסשן הזה (untracked עד commit).

## צעדים הבאים (לפי סדר)
1. **חבר את שאר סרטוני השיעור** למסך השיעור: מלא `VIDEO_DATA` (או טען מ‑Cloudinary כ‑`<video src=url>`). היום רק placeholder מלבד תמרוני ספינה.
2. **הוצא את השאלות מהקובץ לשרת**: החלף את הטמעת `LESSON_Q` ב‑`fetch('/l11/questions',{headers:{'x-code':code}})` מ‑Railway. שמור את פונקציית ה‑`bankCard`/`vQuiz` כמו שהן — מבנה השדות זהה.
3. **signed URLs ל‑Cloudinary** (תפוגה) במקום ה‑URL הציבורי.
4. **סליקה + auth**: חבר `buy()` ל‑Tranzila checkout → notify ל‑Railway → קוד גישה צמוד‑מייל → פתיחת פרימיום (לפי `LAUNCH_PLAN.md`).
5. **התמדה בשרת**: העבר `persist()/loadPersist()` (XP, SRS, topicStats, done) ל‑API פר‑משתמש.
6. **`pauseAt` מדויק**: בפייפליין הרינדור (edge‑tts) שמור את חותמת‑הזמן של `[[PAUSE]]` כשדה `pauseAt` בכל שאלה. באפליקציה: אם קיים `pauseAt` השתמש בו במקום `p*duration`.

## Copy‑paste — לייצר מחדש את `LESSON_Q` מ‑`data/l11.json`
מיפוי topic→שיעור + חישוב `p` (יחס פאוזה). הרץ ואז הזרק לתוך `<script id="lessonq">`:
```python
import json,re
d=json.load(open('data/l11.json',encoding='utf-8'))
by={}
for q in d: by.setdefault(q.get('topic','—'),[]).append(q)
L2I={'א':0,'ב':1,'ג':2,'ד':3}
clean=lambda o: re.sub(r'^[אבגד][\.\)]\s*','',o).strip()
def pr(q):
    vo=q.get('voiceover_text','') or ''
    if '[[PAUSE]]' not in vo: return None
    i=vo.find('[[PAUSE]]')
    b=re.sub(r'\[\[PAUSE\]\]',' ',vo[:i]).strip(); f=re.sub(r'\[\[PAUSE\]\]',' ',vo).strip()
    return round(len(b)/len(f),3) if f else None
def pack(q):
    o={'num':q['num'],'q':q['q_he'],'opts':[clean(x) for x in q['options']],
       'c':L2I.get(q['answer'],0),'exp':q.get('explanation',''),'vid':q.get('videoUrl','')}
    p=pr(q); 
    if p is not None: o['p']=p
    return o
FA={1108,1109,1110,1111,1113,1114}; LES={}
g=by.get
LES['1']=[pack(x) for x in g('אופנוע ים - כללי',[])+g('חוקים ותקנות',[])]
LES['2']=[pack(x) for x in g('אזורי שיט',[])]
LES['3']=[pack(x) for x in g('זכות מעבר',[])]
LES['4']=[pack(x) for x in g('אותות קוליים',[])]
LES['5']=[pack(x) for x in g('זכות מעבר',[]) if re.search(r'תמונה\s*(7\d|8\d|9\d)',x['q_he'])]
LES['6']=[pack(x) for x in g('דגלים',[])]
LES['7']=[pack(x) for x in g('אותות מצוקה',[])]
LES['8']=[pack(x) for x in g('מזג אוויר',[])]
LES['9']=[pack(x) for x in g('ניווט',[])+g('כניסה לנמל',[])]
LES['10']=[pack(x) for x in g('סכנות רכיבה ותמרון',[])]
LES['11']=[pack(x) for x in g('תמרוני ספינה',[])]
LES['12']=[pack(x) for x in g('בטיחות',[]) if x['num'] in FA]
LES['13']=[pack(x) for x in g('בטיחות',[]) if x['num'] not in FA]
print(json.dumps(LES,ensure_ascii=False))
```
מיפוי topic→שיעור (13 topics → 8 קבוצות‑שיעור, 192 שאלות): כללי+חוקים→1 · אזורי שיט→2 · זכות מעבר→3 · אותות קוליים→4 · סימני יום(תת‑קבוצה מזכות מעבר)→5 · דגלים→6 · אותות מצוקה→7 · מזג אוויר→8 · ניווט+כניסה לנמל→9 · סכנות רכיבה→10 · תמרוני ספינה→11 · בטיחות(עזרה ראשונה)→12 · בטיחות(אש/תדלוק)→13.

## הוספת/עדכון שאלה
ערוך `data/l11.json` ישירות (או `tools/quiz-app/update-question.js <num>`). שדות: `num, topic, q_he, options[4], answer(א/ב/ג/ד), explanation, videoUrl, voiceover_text`. הוספת שאלה עם `topic` תקין נכנסת אוטומטית לשיעור הנכון דרך המיפוי. אחרי עריכה — הרץ את הסקריפט למעלה ורענן את `LESSON_Q`.

## Context for Claude (gotchas)
- **אל תכפה 16:9 על סרטוני השאלות** — הם אנכיים. השתמש ביחס טבעי + `max-height`.
- **`localStorage`** עטוף try/catch — אל תסמוך עליו ב‑artifact; זה למוצר בשרת.
- **`data/*.json`** = בייטים גולמיים (CRLF), אל תוסיף חוק `text` ב‑.gitattributes (ראה `CLAUDE.md`).
- Windows: **בלי heredocs של bash** — כתוב סקריפט לקובץ והרץ (ראה `CLAUDE.md`).
- כל נוסח פונה‑משתמש — הפעל skill `no-ai-slop`; טרמינולוגיה: "רשיון אופנוע ים", "מבחן תאוריה".
- הקובץ `skipper-app.html` שנמסר ל‑chat כולל וידאו base64 מוטמע (~4.5MB). **גרסת הריפו** בלי הווידאו (~155KB) — היא זו שב‑git.
