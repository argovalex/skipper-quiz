# השקה — checklist

## 1. שרת (course/api) ל-Railway
1. שירות חדש בפרויקט → root directory = `course/api`, builder = Dockerfile (מוכן).
2. Postgres כבר קיים בפרויקט. קשר את `DATABASE_URL` לשירות (Variables → Reference → Postgres `DATABASE_URL` הפנימי).
3. משתני סביבה לפרודקשן:
   - `DATA_SOURCE=db` — מגיש את הבנק מ-Postgres (לא מה-URL הציבורי).
   - `ALLOWED_ORIGINS=https://<כתובת-האפליקציה>` — לא `*`.
   - `ADMIN_TOKEN=<סוד>` — לעדכון שם/מחיר וניהול.
   - `PRICE_ILS`, `BRAND_NAME`, `PRODUCT_TITLE` — או קבע דרך `admin.js` אחרי העלייה.
   - הסר `DEV_ACCESS_CODE`.
4. אחרי deploy ראשון: ייבא את הבנק ל-DB — `node admin.js bank import` (פעם אחת, מריצים מקומית מול ה-DB, או משלב build).

## 2. אפליקציה (course/app) לאירוח סטטי
- כל host סטטי (GitHub Pages / Railway static / Netlify). זה קובץ יחיד + manifest + sw + icon.
- קבע את כתובת השרת: ערוך ב-`app/index.html` את ברירת המחדל של `API_BASE` לכתובת ה-Railway, או הזרק דרך `localStorage.setItem('sq_api', ...)`.
- ודא ש-`ALLOWED_ORIGINS` בשרת כולל את origin האפליקציה.

## 3. חסם אבטחה — סגירת התוכן הציבורי (חובה לפני גבייה)
כרגע `data/l11.json` זמין להורדה ב-`raw.githubusercontent.com/.../data/l11.json`. `DATA_SOURCE=db` מנתק את **השרת** מה-URL הזה, אבל הקובץ עדיין ציבורי ב-GitHub. לפני גבייה:
- **הפוך את ה-repo לפרטי**, או הסר את `data/` (והנגזרים) מה-repo הציבורי והחזק אותם פרטית.
- ודא שאין נתיב סטטי ציבורי לבנק או לנגזרים.

## 4. מעבר מסימולציה לאמיתי
- **Tranzila:** `TRANZILA_TERMINAL=<טרמינל>` + `TRANZILA_NOTIFY_SECRET=<סוד>`, והגדר בטרמינל notify ל-`POST /api/tranzila/notify`. זה מכבה את `/api/dev/*`. כוונן מיפוי שדות ב-`server.js` מול הטרמינל.
- **מייל:** `SMTP_URL` + חבר nodemailer ב-`src/email.js` (יש seam).
- **חשבונית:** `INVOICE_API_KEY` + חבר Morning/חשבונית ירוקה ב-`src/invoice.js` (יש seam).
- **סרטונים (signed URLs):** כרגע `videoUrl` ציבורי מ-Cloudinary. להקשחה: העלה את הנכסים כ-authenticated וחתום URL עם תפוגה (צריך cloud name + api key + secret). seam לבנייה בשרت אם רוצים.

## 5. לפני כפתור ON
- [ ] מסמכי `legal/` מלאים ואושרו ע״י עו״ד, ומקושרים מהאפליקציה (עדכן כתובות ב-onboarding).
- [ ] שם ומחיר סופיים (`admin.js config set`).
- [ ] קודי מדריכים הונפקו (`admin.js instructor add`).
- [ ] קופונים לשותפים הוזנו (`admin.js coupon add`).
- [ ] עוסק + חשבוניות פעילים.
- [ ] repo פרטי / תוכן סגור.
- [ ] Tranzila + מייל + חשבונית אמיתיים ונבדקו ברכישת בדיקה.
