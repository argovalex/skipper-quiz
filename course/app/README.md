# course/app — אפליקציית הקורס (PWA)

קובץ יחיד `index.html`. מושך את כל התוכן, השם והמחיר מהשרת (`course/api`), לא מוטמע.

## הרצה מקומית
1. הפעל את השרת: `cd course/api && npm start` (פורט 8099).
2. הגש את האפליקציה: `npx http-server course/app -p 8055 -c-1` (או preview `course-app`).
3. פתח `http://localhost:8055`.

`API_BASE` ברירת מחדל `http://localhost:8099`. לשנות מול פרודקשן: בקונסול הדפדפן
`localStorage.setItem('sq_api','https://<railway-api-url>')`, או ערוך את ברירת המחדל ב-`index.html`.

## מה מחובר (פאזה B)
- **תוכן מהשרת:** בטעינה — `/api/config` (שם/מחיר), ואז `/api/free` (10 שאלות ראווה). עם קוד גישה שמור — `/api/content` (כל 13 השיעורים).
- **שער קוד:** "יש לי גישה — הזן קוד" → הקוד נשמר ב-localStorage, המכשיר נרשם (`x-device`), והתוכן המלא נטען. קוד לא תקין / מכשיר עודף / גישה מבוטלת → הודעה מתאימה.
- **התקדמות בשרת:** כל `persist()` דוחף XP/SRS/topicStats/done ל-`/api/progress` (debounced). בטעינה עם קוד — מסתנכרן חזרה.
- **מכשיר אחד:** קוד מדריך (`device_limit=1`) ננעל למכשיר הראשון; שני נחסם.
- משתמש עם גישה נוחת ישר ב-home; משתמש חינם רואה onboarding/paywall.

## עדיין לא (פאזה C+)
- כפתור הרכישה עדיין לא מחובר ל-Tranzila (checkout אמיתי → notify → קוד במייל). כרגע מוצג טקסט placeholder; הכניסה עם קוד עובדת.
- `API_BASE` מצביע ל-localhost; להצביע ל-Railway בפרודקשן.
- אין service worker / manifest ל-PWA אמיתי (התקנה למסך הבית) — יתווסף לפני השקה.
