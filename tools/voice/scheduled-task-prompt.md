# פרומפט למשימה המתוזמנת voice-v2-migration

יצירת המשימה נחסמה בסשן 2026-10-01 (דורש אישור של אלכס). להפעלה: אלכס מאשר, והמשימה נוצרת עם:
- taskId: `voice-v2-migration`, cron: `15 6 * * *` (06:15 שעון ישראל = מחוץ לחלון הכשלים 14:00-22:00 UTC).
- prompt: הטקסט למטה.

---

פרויקט: C:\Users\argov\OneDrive\Co-Work OS\SkipperQuiz. קרא את CLAUDE.md של הפרויקט ואת docs/voice-style-v2.md במלואם. עבוד בשקט, בלי שאלות, דווח בסוף בהתראה של עד 5 שורות.

1. `git status` + `git pull --ff-only`. קונפליקט או עץ מלוכלך בקבצים שתיגע בהם → עצור ודווח.
2. קרא tools/voice/migration-state.json ובצע רק את `phase` הנוכחי, בכמות של `batch`. רשום שורה ב-`log`.
3. commit נפרד לכל שלב (`voice-v2: <phase>: <מה>`) ו-push. כשל credentials → דווח, בלי prompt אינטראקטיבי.

שלבים:
- **code**: vo.js מעדיף `explanation_spoken` ופותח ב-"התשובה הנכונה... <אות>'!"; update-question.js מקבל `--audio <dir>` ושולח `audioQuestion`/`audioAnswer` base64 עם `html`; tools/lesson/tts.py מקבל `--from-dir` לשמע מוכן; עדכון docs/video-pipeline.md. בדיקת buildVoiceover עם/בלי השדה. → phase=pilot.
- **pilot**: לשאלות pilot.questions: כתיבת `explanation_spoken` מדובר (ייחוס 110, אותן עובדות), מילון ניקוד, no-ai-slop, עריכה in-place. הפקה ב-Higgsfield generate_audio_batch (text2speech_v2, elevenlabs, element 88948eaa-5208-4ff5-a405-4d1d9eed6ac1, use_unlim false), שתי קריאות לשאלה, הורדה מיידית, `tools/voice/master.py`, `--pause` לקובץ האזנה, `--check`. שיעור pilot.lesson: VO מדובר, seg_<sid>.mp3, assemble+brand, שמירה כ-`<נושא> v2.mp4`/`.txt`. בלי רינדור לשרת ובלי videoUrl. README בתיקיית הפיילוט. → phase=pilot_review, התראה לאלכס להאזין.
- **pilot_review**: רק בדיקת `pilot_approved`. false → תזכורת פעם ב-3 ימים. true → phase=batch.
- **batch**: לפי license_order: עד text_per_run טקסטים, עד audio_per_run הפקות+רינדור hybrid, sync videoUrl, build-pausemap, merge-inject. עצירה אחרי ~12 רינדורים (EAGAIN). שני כשלים ברצף → failed. 5% ל-samples_for_review. → phase=lessons.
- **lessons**: שיעור אחד לריצה מ-lessons/l11/cards/*, מחליף mp4+txt. → phase=done.

ביטחון: נוסח שאלה ותשובות לא משתנה; `explanation` נשמר; skip_manual לא נוגעים; כשל אימות שמע = לא מרנדרים; unlim_choice או חוסר קרדיט → עצור ודווח; לא לרוץ 14:00-22:00 UTC; בלי heredocs; PYTHONIOENCODING=utf-8.
