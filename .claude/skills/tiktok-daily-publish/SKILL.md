---
name: tiktok-daily-publish
description: פרסום שאלה יומית מ-SkipperQuiz ל-TikTok דרך חשבון ה-TikTok המחובר (connector), עם ההגדרות הקבועות שאלכס אישר (פרטיות, אינטראקציות, AIGC, תוכן מסחרי). השתמש כשמבקשים "תפרסם ל-TikTok", "TikTok היום", או בהרצה מתוזמנת יומית. קנוני מ-Q#1117 (2026-09-17).
---

# tiktok-daily-publish — פרסום יומי ל-TikTok

**חובה קודם:** בדוק `tiktok_accounts` — status חייב להיות `active`. אם `error`, תעצור ותבקש מאלכס `tiktok_reconnect` (אינו ניתן לביצוע אוטומטי).

**⚠️ מצב עבודה (2026-09-21): מכינים עד הטופס, אלכס לוחץ Publish.** `tiktok_prepare_publish` מחזיר "ask the user to finish the form; do NOT call tiktok_publish yourself" — הפרסום דורש אישור פרטי של אלכס בטופס (widget) של Higgsfield, ולא ניתן להחליף אותו בדגלי הסכמה מהצ'אט. לכן ההרצה (יומית 10:00, ותזכורת ביומן 10:15) מבצעת רק שלבים 0-4 ורושמת `status:"prepared"`. **אסור לקרוא ל-`tiktok_publish`** ואסור להמיר תשובות צ'אט לדגלי הסכמה. סשן הפרסום (`publish_session_id`) פג אחרי כשעתיים.

**חובה להריץ מקומית, לא בענן:** `tools/daily-publish-history.json` ב-.gitignore (קיים רק על המחשב של אלכס), ו-`ffmpeg` והכתיבה ל-`tools/tiktok-publish-history.json` גם הם מקומיים. routine בענן נכשל 4 פעמים (2026-09-18 עד 09-21) בגלל זה, והושבת. ההרצה היא scheduled task מקומי של Claude Desktop (`tiktok-daily-publish`, 10:00 שעון ישראל), שפועל רק כשהאפליקציה פתוחה והמחשב ער. הפרסום עצמו עובר רק דרך כלי ה-MCP של Higgsfield, בניגוד לצינור הפייסבוק (`tools/daily_publish.js`) שרץ headless ב-Windows Task Scheduler.

## שלב 0 — בחירת שאלה (מראה של פוסט פייסבוק שעוד לא שוקף)

TikTok **לא** בוחר שאלה משלו — הוא מפרסם את מה שהאוטומציה של הפייסבוק (`tools/daily_publish.js`) כבר פרסמה ועוד לא שוקף. ככה TikTok תמיד אחרי הפייסבוק, בלי כפילות בחירה. (הפייסבוק רץ לפעמים באיחור או מדלג על יום כשהמחשב כבוי, לכן לא מחפשים "אתמול" דווקא.)

1. תאריך היום, שעון Asia/Jerusalem.
2. קרא את `tools/daily-publish-history.json`. קח את הרשומות שה-`date` שלהן (מומר ל-Asia/Jerusalem) **לפני היום**, מהחדשה לישנה, עד 3 ימים אחורה.
3. קרא את `tools/tiktok-publish-history.json`. רשומת פייסבוק נחשבת משוקפת אם קיימת שם רשומה עם אותו `source_date` (זהה ל-`date` של רשומת הפייסבוק).
4. בחר את הרשומה **החדשה ביותר שלא שוקפה**. אין כזו → אין מה לפרסם היום. דווח וסיים בלי לפרסם (אל תבחר שאלה אחרת במקום).
5. הגנה מכפילות: אם כבר נרשם ב-`tiktok-publish-history.json` פרסום מהיום, סיים.
6. טען את השאלה (`num` מהרשומה) מ-`data/l11.json`; ודא `videoUrl` קיים.

דוגמה: ב-`daily-publish-history.json` יש `{num:1158, date:"2026-09-19T01:38"}` ולא שוקפה → ההרצה הבאה מפרסמת את Q1158, גם אם הפייסבוק רץ באיחור.

## שלב 1 — תיקון FPS (חובה, TikTok דורש 23–60fps)

הוידאו המקורי מרונדר ב-17fps ונדחה. **תמיד** בדוק/תקן לפני העלאה:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 <video>
```
אם מתחת ל-23: 
```bash
ffmpeg -y -i <src.mp4> -r 30 -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart <out-30fps.mp4>
```
עבד בתיקיית ה-scratchpad, לא בריפו.

## שלב 2 — העלאה ל-Higgsfield

TikTok דורש `video_url` שמתארח ב-Higgsfield (לא Cloudinary/R2 ישירות):
1. `media_upload` עם filename+content_type → מחזיר `upload_url` (presigned) ו-`url` (cloudfront, זה מה שישמש כ-`video_url`) ו-`media_id`.
2. `curl -X PUT` עם הבייטים המקומיים ל-`upload_url`.
3. `media_confirm` עם ה-`media_id` ו-`type: video`.

## שלב 3 — כותרת ותיאור

- **title** (≤150 תו): הוק קצר + 2–3 האשטגים. דוגמה מ-Q1117: `⚠️ למה האצה פתאומית באופנוע ים מסוכנת? #SkipperQuiz #אופנוע_ים #רישיון_שייט`.
- **description** (≤4000 תו): `buildPublishCaption(q)` מ-`tools/publish_video.js` — אותו caption מלא בו משתמשים לפייסבוק/יוטיוב (CTA + שאלה + תשובה + 💡 הסבר + האשטגים). אין צורך לכתוב caption נפרד ל-TikTok.

## שלב 4 — Prepare

`tiktok_prepare_publish`: `connector_id` מ-`tiktok_accounts` (status active), `mode: DIRECT_POST`, `media_type: VIDEO`, `video_url` (cloudfront מ-Higgsfield), `title`, `description`.

## שלב 5 — ההגדרות הקבועות של אלכס (אושרו 2026-09-17). מעבירים אותן ל-`tiktok_prepare_publish` כ-prefill (`privacy_level`, `allow_*`, `is_aigc`, `commercial_content_disclosure`); אלכס רק מאשר בטופס. לא קוראים ל-`tiktok_publish`.

```
privacy_level: PUBLIC_TO_EVERYONE          privacy_level_selected_by_user: true
allow_comment: true                        allow_duet: true              allow_stitch: false
interaction_settings_selected_by_user: true
is_aigc: true                              (הוידאו מרונדר: קריינות edge-tts + ויזואל סינתטי — תמיד AI)
commercial_content_disclosure: {enabled: true, your_brand: true, branded_content: false}
commercial_content_disclosure_selected_by_user: true
auto_add_music: false                      (משאירים רק את הקריינות המקורית; לא מוזיקת TikTok)
user_confirmed: true    preview_confirmed: true
music_usage_confirmed: true                processing_notice_acknowledged: true
```
אלה החלטות עומדות — אל תציג שוב את ה-AskUserQuestion של פרטיות/אינטראקציות/AIGC/תוכן מסחרי/מוזיקה בכל הרצה יומית. שאל מחדש רק אם אלכס עצמו מבקש לשנות ברירת מחדל, או אם TikTok מחזיר שדה/אפשרות חדשה שלא מופיעה כאן.

## שלב 6 — גיבוי ורישום

1. גיבוי למקרה שהטופס לא נגיש: העתק את הוידאו (אחרי בדיקת ה-FPS) ואת ה-description ל-`output/tiktok-ready/q<num>/` (`q<num>.mp4`, `caption.txt`, שורה ראשונה = title). אז אפשר להעלות ידנית מהאפליקציה.
2. הוסף רשומה ל-`tools/tiktok-publish-history.json`: `{num, topic, date: ISO של היום, status:"prepared", source_date: ה-date המדויק של רשומת הפייסבוק מ-daily-publish-history.json}`. `source_date` הוא מפתח ההתאמה בשלב 0, ורשומה `prepared` נחשבת משוקפת כדי שלא תיבחר שוב מחר.
3. אחרי ש-אלכס מאשר בטופס ומדווח, עדכן את הרשומה ל-`status:"published"` עם `publish_id`, ובדוק `tiktok_publish_status` (`PUBLISH_COMPLETE`).
4. סיים בהודעה אחת: "Q<num> מוכן ב-TikTok, לחץ Publish בטופס. פג בשעה HH:MM."

זה הקובץ ש-`monitor.html` קורא כדי להציג תגית "TikTok" בעמודת הפלטפורמות ליד הרשומה המקורית של הפייסבוק (התאמה לפי `num`). אם משנים את מבנה הקובץ — לעדכן גם את `TIKTOK_LOG_URL`/`renderHistory()` ב-`monitor.html`.

## תקדים

Q#1117 ("סכנות רכיבה ותמרון") — פורסם 2026-09-17, `publish_id: v_pub_url~v2.7686421095972440080`, `PUBLISH_COMPLETE`. שימש לקביעת כל ברירות המחדל בשלב 5. (הרשומה שכבר קיימת ב-`tools/tiktok-publish-history.json` ידנית — פורסמה לפני שהיישור ל-"אתמול" נקבע; אינה מייצגת את הלוגיקה הסופית של שלב 0.)
