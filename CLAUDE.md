# SkipperQuiz — הנחיות לסוכנים

## מקור האמת לשאלות
- **`data/l11.json`** ו-**`data/l30.json`** הם המקור הקנוני (per-license). ערוך אותם בלבד לצורך עבודה על תוכן שאלות.
- **אל תקרא ואל תערוך** את הקבצים הבאים לצורך עבודה על תוכן — הם נגזרים/מיוצרים וגדולים, וקריאתם שורפת טוקני קונטקסט לחינם:
  - `questions.json` — נגזר מ-`data/`. נדרש ב-runtime (ה-publisher קורא אותו). נשאר tracked, אבל לא לעריכה ידנית.
  - `quiz-data-l11.json` — נגזר. נדרש ב-runtime (`quiz-app.html` קורא אותו). נשאר tracked, לא לעריכה ידנית.
  - `html/` — 355 קבצי HTML מיוצרים. **לא tracked ב-git** (ב-.gitignore). לעולם אל תקרא אותם ידנית.

## איך לרנדר תוצרים
- `html/` מיוצר ע"י `node src/generate-all-l11.js` (ו-`src/generate-compass-reel.js` לריל). הרץ אחרי שינוי תוכן; אל תערוך את `html/` ביד.
- **רינדור וידאו של שאלה: השתמש ב-`node tools/quiz-app/update-question.js <num>`.** הוא מרנדר עם ה-VO והויזואל הנכונים ומפיץ לכל המקומות (data/l11.json, quiz-data-l11.json, quiz-app.html).
- **קריטי:** רינדור דרך ה-API של השרת **חייב לשלוח את פרמטר `html`** (הויזואל מ-`scenes.js`, דרך `tools/quiz-app/scene-html.js`). `html/` לא tracked, אז השרת לא יכול למשוך אותו — בלי `html` הסרטון יוצא **גנרי** (עוגן במקום הדיאגרמה). לעולם אל תשלח `/render` רק עם `voiceover_text`.

## API
- קריאות ה-LLM ב-`src/generate.js` ו-`src/scraper.js` משתמשות ב-Haiku (`claude-haiku-4-5-20251001`). השאלות הן JSON פשוט — אין צורך ב-Opus.
