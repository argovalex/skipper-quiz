# מפת מערכות SkipperQuiz

נקודת כניסה אחת לכל סשן: לכל מערכת מקור אמת, פקודה, שרת וכתובת. כללי עבודה ב-[CLAUDE.md](../CLAUDE.md), רקע מלא ב-[claude-md-full.md](claude-md-full.md).
עודכן: 2026-10-21.

## תמונה כללית

```
data/lXX.json  ──►  עורך (index.html / vo-editor) ──►  רינדור Railway ──►  Cloudinary videoUrl
     │                                                                          │
     ├─► generate-all-l11.js ─► html/ (נגזר)                                    ├─► quiz-app.html (merge-inject)
     ├─► questions.json (נגזר, השרת מעדכן)                                      ├─► course/ (api + app + site)
     └─► lessons/<lic>/cards/ ─► tools/lesson ─► mp4 ממותג                       └─► הפצה (TikTok / WA / FB / YouTube)
```

## פקודה אחת: `tools/sq.js`

`node tools/sq.js <פקודה>` או `npm run <פקודה> -- <ארגומנטים>`. בלי ארגומנטים מדפיס עזרה.

| פקודה | מה עושה |
|---|---|
| `status` | git status + פער מול origin (פתיחת סשן) |
| `sync` | pull ff-only (בלי autostash) + `gen-vo-lexicon` |
| `preflight <num...> [--license N]` | sync + בדיקה שתמונת `mediaUrl` כבר ב-GitHub |
| `check <num...>` | preflight + `vo-check` (מילים חדשות בלי ניקוד) |
| `render <num...> [--license N]` | preflight + `update-question.js` (כל הדגלים שלו עוברים) |
| `stored <num...>` | l12 מ-`voiceover_text` שמור + propagate |
| `propagate <num...>` | `update-question --no-render` (רונדר כבר בעורך) |
| `render ... --local-voice` | הקול מופק מקומית ב-`voice.js` ונשלח כ-`--audio` (השרת לא מקריא) |
| `voice segments\|say\|question\|master` | הצנרת `tools/voice/voice.js` ישירות |
| `pausemap`, `lexicon`, `html`, `topics`, `brand`, `quota` | עטיפות לסקריפטים הקיימים |

preflight עוצר כשתמונה לא ב-origin. `--push-media` דוחף רק את קבצי המדיה החסרים, ו-`--no-sync` מדלג על pull ועל המילון.

## 1. בנק השאלות (מקור אמת)

| מה | איפה |
|---|---|
| מקור אמת | `data/l11.json`, `data/l12.json`, `data/l30.json` (ו-l40). עורכים in-place בלבד |
| נגזרים, לא לגעת | `questions.json`, `quiz-data-l*.json`, `html/` |
| ויזואל לשאלה | `scenes.js` (getScene), `mediaUrl` דורס |
| עורך ראשי | `index.html` (Skipper Quiz Manager), נטען מ-Pages או file:// |
| אישור בנייד | `approve.html` ב-`https://argovalex.github.io/skipper-quiz/approve.html` |

## 2. ניקוד והגייה (VO)

| מה | איפה |
|---|---|
| מילון קנוני (רק אלכס עורך) | `references/niqqud-lexicon.md` |
| עורך המילון | `vo-editor.html` + `tools/vo-editor-server.js`, פורט 8899, עולה ב-login (Scheduled Task `SkipperQuiz VO Editor`) |
| ייצוא ל-JS | `node tools/quiz-app/gen-vo-lexicon.js` ← `tools/quiz-app/vo-lexicon.js` |
| בניית VO לשאלה | `tools/quiz-app/vo.js` (`buildVoiceover`), בדיקה: `vo-check.js` |
| **מנוע הניקוד (יחיד)** | `applyLexiconText` ב-`tools/quiz-app/vo.js`. Python (`tools/lesson/niqqud.py`, `scratch_niqqud.py`) קורא לו דרך `niqqud-cli.js`. בדיקות: `npm test` |
| קול | ElevenLabs, שיבוט `825LDODpKbomKDZoqVG5`, `eleven_v4` (l11: `eleven_v3`). כלים: `tools/voice/` (`elevenlabs-clone.js`, `el-quota.js`) |
| **צנרת VO (יחידה)** | `tools/voice/voice.js`: מילון ← ElevenLabs ← מסטרינג ← בדיקת אורך. הגדרות (שרשרת מסטרינג, מודלים, השהיות) ב-`tools/voice/voice-config.json`. משתמשים בה: `el_tts.py` (l30/l40), `tools/lesson/tts.py --elevenlabs` (l11), שרת העורך, `master.py`, ו-`sq render --local-voice` |

כללי המנוע: לא דורס ניקוד קיים (חוץ מכפתור "מילון" בעורך, `override`), מעבר אחד הארוך קודם, מילים קצרות רק `או קו אם עד פה אף`, `למנוע`/`צופה` רק בשיעורים (`mode:'lesson'`). רקע: [reports/niqqud-engines-2026-10-21.md](../reports/niqqud-engines-2026-10-21.md).

## 3. הפקת וידאו

| מסלול | פקודה | פלט |
|---|---|---|
| שאלה (l11) | `node tools/quiz-app/update-question.js <num>` (render + videoUrl + pausemap + merge-inject + push) | Cloudinary |
| שאלה (l12/l30) | `update-question.js <num> --license N`; VO שמור: `tools/l12/render-stored.js` | Cloudinary |
| שאלה, VO ידני של אלכס | POST ישיר `{voiceover_text, html, force:true}`, ראה CLAUDE.md | Cloudinary |
| שיעור | skill `build-lesson`: `tools/lesson/tts.py` ← `assemble.py` ← `brand.py` | `lessons/<lic>/cards/<נושא>/` |
| אנכי מקומי (legacy, edge-tts) | `python -m video.make_question_video <num>` | `output/videos/` |
| אנימציה | `tools/higgsfield/` | |

שרת רינדור: `https://skipper-quiz-publisher-production.up.railway.app` (`/render/:num`, `/status/:num`, `/tts`). קוד חי ב-`publisher/` (clone מקונן של `argovalex/skipper-quiz-publisher`, `.git` משלו). נתקע אחרי ~18 רינדורים, רנדר במנות.

אפליקציית תרגול: `quiz-app.html`, נבנית ע"י `tools/quiz-app/build-pausemap.js` + `merge-inject.js`. פרטים: [tools/quiz-app/README.md](../tools/quiz-app/README.md), [video-pipeline.md](video-pipeline.md).

## 4. אתר ומוצר בתשלום (`course/`)

| שירות Railway | תיקייה | דומיין |
|---|---|---|
| API (Express + Postgres) | `course/api` | `api.alargov.com` |
| אפליקציה (PWA) | `course/app` | `app.alargov.com` |
| אתר שיווקי | `course/site` | `www.alargov.com` |

דפי נושא SEO: ערוך `course/site/ofnoa-yam/topics.json` ← `node course/site/build-topics.js`. סליקה: Tranzila. ניהול קודי מדריך: `hub.html`. פריסה: [course/DEPLOY.md](../course/DEPLOY.md). push ≠ deploy.

## 5. הפצה

| ערוץ | כלי |
|---|---|
| TikTok יומי | skill `tiktok-daily-publish`, `tools/daily_publish.js`, `tools/run-daily-publish.cmd` |
| WhatsApp קבוצות | `tools/wa-group-publish.js` |
| Facebook | `tools/facebook-groups.json`, `groups-log.json` |
| YouTube | `tools/upload-course-videos.js`, ערוץ תחת alex@alargov.com |
| העלאות | `tools/publish_video.js`, `tools/r2_upload.js` |

## 6. דפי ניהול בשורש

| דף | תפקיד | מצב |
|---|---|---|
| `index.html` | עורך שאלות + רינדור | פעיל, ראשי |
| `vo-editor.html` | מילון הגייה | פעיל (localhost:8899) |
| `approve.html` | אישור סופי בנייד | פעיל |
| `hub.html` | קודי מדריך ושימוש בקורס | פעיל |
| `quiz-app.html` | תרגול ציבורי | פעיל, נגזר |
| `back-office.html`, `monitor.html`, `publish-review.html` | הפצה ופרסום | פעיל, השרת (`publisher/index.js`) מקשר אליהם |
| `admin.html`, `records.html` | ניהול מדריכים ורשומות קורס | פעיל, `course/api` מקשר אליהם |
| `fix-requests.html` | בקשות תיקון | פעיל, `hub.html` מקשר |

**הכלל:** דפים נשארים בשורש כי GitHub Pages מגיש אותם בכתובת `argovalex.github.io/skipper-quiz/<דף>` וקוד השרתים מקשר לשם. העברה לתיקייה תשבור קישורים.

**ארכיון (2026-10-21):** הוצאו מ-git ונשמרו מקומית ב-`_archive/root-2026-10-21/` (מוחרג ב-gitignore): `demo.html`, `question-bank.html`, `review-l11.html`, `skipper-control.html` + `config.json` שלו, `skipper_quiz_studio.html`, `landing.html` ו-`skipper-app.html` (הוחלפו ע"י `course/`), `setup-github.ps1` (ריק), `s3-041_zoom.jpeg`, וקבצים מקומיים לא-עקובים (PDF, תמונות, `questions-Alex.json`, `raspen_5_diverse.json`, `chk.mp3`, `scratch_gen_all.py`). שחזור: העתקה חזרה מהארכיון, או `git checkout e98758d7 -- <קובץ>`.
`LAUNCH_PLAN.md` ← `course/docs/`. `review_license11.xlsx` ← `references/`. `queue.html` כבר לא קיים.
נשארו בשורש בכוונה: `scratch_niqqud.py` (CLAUDE.md מפנה אליו), `scratch_vo_u6b.txt` (ברירת המחדל של `vo-editor.html`), `auth.js` (ריק אבל נטען מ-4 דפים).

## 7. git וסביבה

- git דרך `tools\run-hidden.ps1` (בלי חלונות שחורים).
- `.gitattributes` אוכף EOL; `data/*.json` = `-text`.
- Python 3.12 דרך `uv`, `PYTHONIOENCODING=utf-8`.

## תוכנית ייעול

1. ✅ מפת מערכות (המסמך הזה).
2. ✅ CLI אחד (`tools/sq.js`, `npm run <פקודה>`) שאוכף pull, gen-vo-lexicon ו-push media לבד.
3. ✅ מנוע ניקוד אחד לכל המסלולים.
4. ✅ צנרת VO משותפת (`tools/voice/voice.js`). חריג: `publisher/el-tts.js` (ריפו נפרד בשרת) מחזיק עותק של השרשרת וכלל המודל, לסנכרן ידנית.
5. ✅ ניקוי השורש: דפים מתים לארכיון, דפים חיים נשארו (Pages), קבצים זרים יצאו. ראה סעיף 6.
