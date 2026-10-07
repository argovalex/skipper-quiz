# סביבת עיצוב מחדש — alargov.com

הענף `redesign` הוא סביבת הניסוי. `main` נשאר האתר החי ולא משתנה עד שמחליטים למזג.

## שלוש דרכים לראות את האתר

| איפה | מתי | איך |
| --- | --- | --- |
| מקומית במחשב | תוך כדי עבודה | `powershell -File tools/site/preview.ps1` → נפתח http://localhost:8080 |
| Staging ב-Railway | אחרי כל push לענף | https://course-site-staging-production.up.railway.app · שירות "course site staging" בפרויקט Postgres. כל push ל-`redesign` מתפרס לבד |
| האתר החי | אחרי מיזוג ל-`main` | https://www.alargov.com |

## הגדרת Staging ב-Railway (פעם אחת)

1. בפרויקט ב-Railway: New → GitHub Repo → `argovalex/skipper-quiz`.
2. Settings → Source: Branch = `redesign`, Root Directory = `course/site`.
3. Variables: `STAGING=1`.
4. Settings → Networking → Generate Domain.

`STAGING=1` חוסם אינדוקס בגוגל (robots.txt + meta noindex) ומוסיף תווית "STAGING · redesign" בפינת כל עמוד. באתר החי המשתנה לא מוגדר, אז שום דבר מזה לא קורה שם.

## זרימת עבודה

1. עובדים על `redesign` בלבד.
2. כל שינוי גדול = commit נפרד עם הסבר, כדי שאפשר יהיה לבחור מה למזג.
3. עמודים חדשים (מגזין, מדורים) נכנסים לתיקיות חדשות. עמודים קיימים משתנים במקום.
4. עמודי `ofnoa-yam/` נוצרים מ-`topics.json` דרך `node build-topics.js`. לא עורכים אותם ביד.
5. כשמרוצים: Pull Request מ-`redesign` ל-`main`, בדיקה, מיזוג. Railway החי מתפרס מ-`main`.

## מה בודקים לפני מיזוג

- [ ] כל העמודים נפתחים בנייד וברוחב מחשב
- [ ] כפתורי "רכוש עכשיו" ו"התחל חינם" עובדים מול api.alargov.com
- [ ] הסרטונים מ-Cloudinary מתנגנים
- [ ] `sitemap.xml` מעודכן לעמודים חדשים
- [ ] עמודי legal לא נפגעו

## האתר החדש (`/v2/` ב-staging)

בנייה: `node build-site.js` (סקריפט אחד, בונה את כל העמודים החדשים).

- מבנה, תפריט, קורסים ופוטר: `hub.js`. עיצוב: `assets/site.css`. תמונות החלונות: `assets/tiles/`.
- חדשות: `content/posts.json`, ייצוא מה-Back Office. רק `status: "approved"` עולה. שדה `image` אופציונלי.
- סרטונים: `content/reels.json` (מספר שאלה, כותרת, `date` אופציונלי). הקישור נלקח מ-`data/l11.json`.
- חלון "חדש באתר" בדף הבית: אם יש פוסט או סרטון עם תאריך של היום (שעון ישראל), הוא הופך ל"היום באתר" ומציג רק אותם.
