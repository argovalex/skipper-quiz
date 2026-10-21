# SkipperQuiz — הנחיות לסוכנים
פירוט מלא, רקע והיסטוריה של כל חוק: `docs/claude-md-full.md`. כללי קול: `docs/voice-style-v2.md`. וידאו מקומי: `docs/video-pipeline.md`.
**מפת מערכות (בנק, ניקוד, וידאו, אתר, הפצה, דפי ניהול): `docs/SYSTEMS.md`. קרא אותה ראשונה.**

## קול ו-VO
- כל הקראה חדשה (שאלה, שיעור, ריל): ElevenLabs, שיבוט `825LDODpKbomKDZoqVG5`, `eleven_v4` (שאלות l11 שרונדרו נשארות ב-v3). בלי pitch/EQ; מסטרינג רק ב-`tools/voice/master.py`. edge-tts/Hila/Avri/Remy פסולים.
- טקסט מוקרא בסגנון מדובר (משפטים קצרים, שאלות רטוריות, שורה תחתונה → למה → מסיחים). שאלה: שדה `explanation_spoken`, רינדור ב-`update-question.js <num> --license N`.
- **כל VO עובר דרך מילון ההגייה** (`http://localhost:8899/vo-editor.html`). לא מקודדים ניקוד ידנית; מילה שגויה מתקנים במילון. רק אלכס עורך את המילון; אני מסמן ומדווח. כתוב VO בכתיב זהה למפתח המילון. לפני כתיבה: pull + `gen-vo-lexicon.js`.
- ניקוד ידני של אלכס לא נדרס: שומרים ב-`voiceover_text` ומרנדרים ב-POST ישיר (`{voiceover_text, html: genHtml(q), force:true}`), **לא** `update-question.js`. אחר כך sync videoUrl, `build-pausemap`, `merge-inject`, commit+push.
- לכל סרטון מצרפים קובץ VO `.txt` **מנוקד** (`scratch_niqqud.apply_lexicon`), עם קישור לכל קובץ שנמסר.

## פורמט הסבר לשאלה (l11, l12)
`explanation` (למסך, בלי ניקוד): 1) זיהוי הכלי/המצב, 2) הכלל וההחלטה, 3) שלילת **כל** מסיח ("תשובה א שגויה כי..."). `voiceover_text` מנוקד: q1 [[PAUSE]] "התשובה הנכונה היא <אות>: <טקסט>" + ה-explanation. קנוני: שאלה 2127.

## רינדור
- שאלה: `node tools/quiz-app/update-question.js <num>`. אם קוראים ל-API ישירות **חובה** לשלוח `html` (מ-`scenes.js` דרך `tools/quiz-app/scene-html.js`), אחרת הסרטון גנרי.
- `html/` מיוצר ע"י `node src/generate-all-l11.js` אחרי שינוי תוכן. לא tracked, לא נערך ולא נקרא ידנית.
- אל תרנדר שאלה שלא אומתה מול מפתח התשובות הרשמי. רינדור רק אחרי אישור אלכס.

## מקור האמת
- עורכים רק `data/l11.json`, `data/l30.json` (וכן l12). **לא לקרוא ולא לערוך**: `questions.json`, `quiz-data-l11.json`, `html/` (נגזרים וגדולים).
- אל תרג'נרט `data/*.json` בסקריפט חד-פעמי; עריכה in-place ושמירת כל השדות (במיוחד `mediaUrl`). לפני bulk: diff שדות מול HEAD.
- l12: `answer_confirmed:false` עד אימות מול המפתח הרשמי. ויזואל l12 לפי שרשרת ב-`scenes.js` (`mediaUrl` דורס).

## שיעורים
- ארכוב: `lessons/l11/cards/<נושא בעברית>/` עם mp4, כל ה-PNG וה-txt. הארכיון הוא המקור, לא ה-scratchpad.
- מיתוג: `python tools/lesson/brand.py <lesson.mp4> [branded.mp4]` (כרטיס לוגו פתיח/סיום + סימן מים). בלי `intro-meshit11.mp4`. skill: `build-lesson`.

## כללי עבודה
- **הוסף, אל תחליף**: "תוסיף X" = פריט חדש, לא החלפת דף. תוכן גדול בקובץ נפרד עם קישור.
- **אחרי 50 הודעות בסשן (חוק קבוע, חיסכון במכסה): עצור, כתוב handover קצר (skill `handover`) והמלץ לאלכס לפתוח סשן חדש.** כל הודעה שולחת מחדש את כל ההיסטוריה.
- שאלה-שאלה כברירת מחדל. שאל לפני עבודה יקרה (batch, multi-file): תוכנית ב-3 בולטים + הערכת קריאות, וחכה ל"go". בלי over-engineering.
- פתיחת סשן: קרא handover במלואו ואמת מול `git log`/קבצים; הרץ `git status` ו-`git log origin/main..HEAD` לפני עבודה על תוכן; לא להאשים cache לפני git.
- טרמינולוגיה למשתמש: "רשיון אופנוע ים" (לא "רשיון 11"), "מבחן תאוריה". על כל נוסח פונה-משתמש הפעל skill `no-ai-slop`.
- LLM ב-`src/generate.js`/`src/scraper.js`: Haiku (`claude-haiku-4-5-20251001`).

## סביבה (Windows)
- בלי heredocs של bash; כתוב סקריפט לקובץ והרץ. `PYTHONIOENCODING=utf-8`. Python 3.12 דרך `uv`.
- git/commit/push דרך `tools\run-hidden.ps1` (בלי חלונות שחורים). `git push` דורש credential helper מוגדר.
- EOL: `.gitattributes` אוכף (מקור LF, `data/*.json` = -text). אל תוסיף חוק `text` על `data/*.json`. בדוק עם `git diff --ignore-cr-at-eol --stat`.
