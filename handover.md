# Handover — SkipperQuiz Publisher — 24.6.2026

## What we did this session

- **ארכיטקטורה**: חילקנו את המערכת ל-4 רכיבים — Editor (queue tab), Publisher (tracking), Monitor dashboard, Distributor module
- **הוספנו** טאב "📤 תור פרסום" ל-`index.html` עם stats, תור ממתין, ולוג פרסום
- **עדכנו** `publisher/index.js` — publish log tracking עם 4 רמות עדיפות, `updatePublishLog()`, `loadPublishLog()`
- **יצרנו** `monitor.html` — דשבורד עצמאי שמביא נתונים מ-GitHub/local, `hub.html` — דף מרכזי שמקשר הכל
- **יצרנו** `publisher/distributor.js` — platform-specific caption builder, payload validation, distribution-log
- **Make.com**: שינינו Facebook מ-"Create a Post" ל-"Upload a Video" עם HTTP Download a file לפני. YouTube הוגדר עם `title` field
- **קיצרנו** animation מ-14s ל-12s (שאלה 5s במקום 7s), הקטנו קובץ וידאו (CRF 26)
- **בעיה פתוחה**: `questions.json` לא pushed ל-GitHub — יש `.git/index.lock` שחוסם

## Key decisions

- `monitor.html` ו-`hub.html` קוראים `./questions.json` מקומית (לא GitHub) — דפדפן חוסם file:// CORS, אז צריך `python -m http.server 8080`
- `publisher/index.js` שולח `title` בWebhook payload: `SkipperQuiz — ${q.topic} שאלה #${q.num}`
- `distributor.js` בונה caption פר-פלטפורם עם hashtags ו-maxCaptionLength

## Current state

| מה | סטטוס |
|---|---|
| Make.com scenario | ✅ מוגדר — Facebook Upload Video + HTTP Download |
| YouTube module | ⚠️ title field עודכן ל-`1.title` — טסט אחרון לא הושלם |
| Facebook module | ✅ Upload a Video עם `2.data` |
| Instagram module | ✅ Create a reel post |
| publisher/index.js | ✅ עודכן — לא pushed לגיטהאב |
| distributor.js | ✅ נוצר — לא pushed |
| questions.json | ❌ לא ב-GitHub (lock file) |
| hub.html / monitor.html | ✅ נוצרו — לא pushed |

## Git status

```
modified: hub.html, index.html, monitor.html, publisher (new commits), questions.json
untracked: question-bank.html, skipper-control.html, monitor.html, hub.html
index.lock קיים — חוסם commit
```

## Environment / config

- **Webhook URL**: `https://hook.eu1.make.com/deu5m0qyc6xndo7nhd6noioi9gnwc4yr`
- **Repo main**: `github.com/argovalex/skipper-quiz` (branch: main)
- **Repo publisher**: submodule ב-`publisher/` — repo נפרד
- **Railway**: מריץ `publisher/index.js` כ-cron
- **Make.com**: `eu1.make.com` — org 6571381

## Next steps (בסדר עדיפות)

1. **תקן את index.lock ו-push**:
   ```powershell
   Remove-Item "C:\Users\argov\OneDrive\Co-Work OS\SkipperQuiz\.git\index.lock" -Force
   cd "C:\Users\argov\OneDrive\Co-Work OS\SkipperQuiz"
   git add questions.json hub.html monitor.html index.html
   git commit -m "add questions.json + monitor + hub + queue tab"
   git push origin main
   ```

2. **Push publisher submodule**:
   ```powershell
   cd "C:\Users\argov\OneDrive\Co-Work OS\SkipperQuiz\publisher"
   git add .
   git commit -m "add distributor.js + publish-log + distribution-log"
   git push
   ```

3. **בדוק YouTube title ב-Make** — ודא שהשדה מכיל `{{1.title}}` (לא `1.title` ישן)

4. **הרץ טסט מלא** מ-Railway — Railway → Deploy → Run manually

5. **פתח monitor** דרך `python -m http.server 8080` → `http://localhost:8080/hub.html`

## Copy-paste snippets

```powershell
# Fix lock + push everything
Remove-Item "C:\Users\argov\OneDrive\Co-Work OS\SkipperQuiz\.git\index.lock" -Force
cd "C:\Users\argov\OneDrive\Co-Work OS\SkipperQuiz"
git add questions.json hub.html monitor.html index.html
git commit -m "add questions.json + hub + monitor + queue tab"
git push origin main
cd publisher
git add .
git commit -m "distributor + logs"
git push
```

```powershell
# Run local hub
cd "C:\Users\argov\OneDrive\Co-Work OS\SkipperQuiz"
python -m http.server 8080
# open: http://localhost:8080/hub.html
```

```bash
# Test webhook
curl -X POST "https://hook.eu1.make.com/deu5m0qyc6xndo7nhd6noioi9gnwc4yr" \
  -H "Content-Type: application/json" \
  -d '{"videoUrl":"https://res.cloudinary.com/demo/video/upload/dog.mp4","title":"Skipper Quiz — ניווט שאלה #1","caption":"בדיקה","questionNum":1,"topic":"ניווט"}'
```

## Context for Claude

- ה-publisher הוא **git submodule** — לא ניתן לעשות `git add publisher/` מהroot. חייבים `cd publisher && git add . && git commit && git push` בנפרד
- `questions.json` נמצא ב-root של `skipper-quiz` (לא ב-publisher) — הוא ה-single source of truth
- Make.com router מוגדר: route 1 = YouTube, route 2 = Instagram, route 3 = Facebook (לא ודאי — צריך לבדוק)
- `publisher/index.js` כולל `distributor.js` — חייב להיות ב-Dockerfile. בעבר נשכח ונכשל בdeploy
- Facebook module בעבר נכשל בגלל Make.com test ping (5 bytes ריקים) — יש Skip error handler
- אנימציית הוידאו: 5s שאלה → reveal תשובה (ירוק) → 5.5s הסבר = 12s סה"כ
