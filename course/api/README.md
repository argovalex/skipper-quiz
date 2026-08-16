# course/api — שרת הקורס בתשלום

Node + Express + Postgres. מקור התוכן נשאר `data/l11.json` (השרת מגיש חי, לא snapshot).

## הרצה מקומית
```bash
cd course/api
npm install
cp .env.example .env   # מלא DATABASE_URL אם רוצים את endpoints של ה-DB
npm start
```
בלי `DATABASE_URL` השרת עולה, ו-`/health` + `/api/free` + `/api/content` (עם `DEV_ACCESS_CODE`) עובדים. endpoints של DB מחזירים 503 עד שמחברים Postgres.

## Endpoints
| Method | Path | קוד? | תיאור |
|---|---|---|---|
| GET | `/health` | לא | חי + האם DB מחובר |
| GET | `/api/config` | לא | שם מותג + כותרת מוצר + מחיר (editable) |
| POST | `/api/config` | x-admin | עדכון שם/מחיר בלי redeploy |
| GET | `/api/free` | לא | 10 שאלות חינם (חלון ראווה) |
| GET | `/api/content` | כן | כל הבנק, 13 שיעורים + שם/מחיר |
| GET | `/api/progress` | כן | התקדמות המשתמש (DB) |
| POST | `/api/progress` | כן | שמירת התקדמות `{data:{...}}` (DB) |
| POST | `/api/coupon/validate` | לא | `{coupon}` → הנחה (percent/fixed) + partner_ref |
| POST | `/api/coupon/redeem` | לא | `{coupon,email}` → קוד גישה חינם (coupon מסוג `full`, לקמפיינים) |
| POST | `/api/checkout` | לא | `{email,coupon?,return_url?}` → מתמחר (קופון בשרת), פותח הזמנה, מחזיר `checkout_url` |
| GET | `/api/order/status` | token | `?token=` → `{status, code?}`; האפליקציה עושה poll אחרי חזרה מהתשלום |
| POST | `/api/tranzila/notify` | secret | callback שרת-לשרת → סוגר הזמנה: קוד + מייל + חשבונית |
| GET/POST | `/api/dev/checkout` · `/api/dev/pay` | — | דף תשלום מדומה. מושבת אוטומטית כש-`TRANZILA_TERMINAL` מוגדר |
| POST | `/api/admin/reload` | x-admin | רענון תוכן בלי redeploy |

קוד מועבר ב-header `x-code` או `?code=`. מזהה מכשיר ב-`x-device` (הגבלת מכשירים).

## שם, מחיר, וקופונים — ניהול (admin.js)
שם המותג והמחיר יושבים בטבלת `settings` ב-DB, ניתנים לשינוי **בלי redeploy**. השם ברירת-מחדל גנרי (`לומדה`) כי הפלטפורמה תשרת עוד מבחני תאוריה. הרץ מ-`course/api`:
```
node admin.js config get
node admin.js config set price_ils 129
node admin.js config set brand_name "השם החדש"
node admin.js coupon add LAUNCH20 percent 20 partner_ig   # code kind value [partner] [maxUses]
node admin.js coupon list
node admin.js coupon off LAUNCH20 | coupon on LAUNCH20 | coupon del LAUNCH20
```

### מדריכים — קוד אישי, מכשיר אחד
כל מדריך מקבל **קוד ייחודי משלו**, נעול ל**מכשיר אחד בלבד** (`device_limit=1`). אין קופון משותף.
```
node admin.js instructor add yossi@sail.co.il   # מנפיק קוד ייחודי, מדפיס אותו
node admin.js instructor list                    # כל הקודים: מייל, כמה מכשירים נקשרו, revoked
node admin.js instructor revoke SK-XXXX-XXXX      # ביטול גישה
```
המדריך מזין את הקוד באפליקציה כמו כל משתמש (אותו שער קוד). המכשיר הראשון שנקשר הוא היחיד שיעבוד; ניסיון ממכשיר שני נחסם (403). כל קוד מתועד כ-`comp` ב-`purchases` עם `partner_ref='instructor'`.

### קופונים לקהל
- **קופוני הנחה** (`percent`/`fixed`) עוברים דרך ה-checkout (`/api/coupon/validate`), מתמחרים בשרת + attribution לשותף.
- **קופון `full`** (אם צריך) מנפיק גישה חינם דרך `/api/coupon/redeem` — לקמפיינים כלליים, לא למדריכים.

## פריסה ל-Railway
1. שירות חדש בפרויקט, root = `course/api`, builder = Dockerfile (`railway.toml` מוכן).
2. New → Database → Add PostgreSQL. `DATABASE_URL` נוצר אוטומטית. הסכמה נבנית ב-boot.
3. משתני סביבה: `ALLOWED_ORIGINS` (origin של ה-PWA), `TRANZILA_NOTIFY_SECRET`, `ADMIN_TOKEN`, `PRICE_ILS`, `DATA_URL`. הסר `DEV_ACCESS_CODE` בפרוד.

## חיבור Tranzila אמיתי (כשמגיעים לזה)
כרגע ה-checkout רץ בסימולציה (`/api/dev/checkout`). להחלפה לאמיתי:
1. `TRANZILA_TERMINAL=<שם הטרמינל>` — מפעיל את דף התשלום המתארח של Tranzila ומכבה את הסימולטור.
2. `TRANZILA_NOTIFY_SECRET=<סוד>` — והגדר בטרמינל את ה-notify (transaction notification) שיפנה ל-`POST /api/tranzila/notify`.
3. `PUBLIC_URL=<כתובת ה-api>` בפרוד (לבניית לינקי חזרה).
מיפוי השדות של notify (`Response=000`, `Tempref`, `sum`, `token`) ב-`server.js` — יכוונן מול הטרמינל בפועל. כל השאר (הנפקת קוד, מייל, חשבונית, idempotency) כבר עובד.

**מייל וחשבונית:** `src/email.js` ו-`src/invoice.js` הם seams. ריקים = סימולציה (log). מלא `SMTP_URL` / `INVOICE_API_KEY` כדי לחבר אמיתי (nodemailer / Morning) בלי לגעת בזרימה.

## 🔴 חסם אבטחה לפני גבייה (stage 0)
`DATA_URL` מצביע כרגע על ה-repo הציבורי (`raw.githubusercontent.com/.../data/l11.json`). כלומר כל הבנק זמין חינם ב-URL אחד. **לפני השקה**: להעביר את `data/l11.json` למקור פרטי (repo פרטי / bucket / משתנה סביבה) ולהצביע `DATA_URL` לשם. השרת כבר תומך בכל URL.

## מיפוי topic→שיעור
מוגדר ב-`src/content.js` (`buildLessons`). שאלה חדשה עם `topic` תקין נכנסת אוטומטית לשיעור. שיעור 5 (סימני יום) = תת-קבוצה מ"זכות מעבר" לפי `תמונה 7x/8x/9x`. שיעורים 12/13 מפצלים "בטיחות" לפי מספרי עזרה ראשונה.
