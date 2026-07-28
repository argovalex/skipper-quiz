# quiz-app pipeline (L11 interactive course)

Builds `quiz-data-l11.json` and embeds it into `quiz-app.html` — the public
interactive practice player. The video pauses at the question, waits for the
user's answer, then resumes to the explanation. Pause/resume points are
detected from silence gaps in each rendered video's audio.

## Files
- **build-pausemap.js** — runs ffmpeg `silencedetect` on every `data/l11.json`
  question that has a `videoUrl`, finds the largest silence gap (the `[[PAUSE]]`
  boundary in the VO), and writes `pause-map.json`:
  `{ "1001": { pauseAt, resumeAt, dur }, ... }`.
- **merge-inject.js** — merges `data/l11.json` + `pause-map.json` into
  `../../quiz-data-l11.json` AND re-embeds that JSON inline into
  `../../quiz-app.html` (`<script id="quiz-data">`).
- **pause-map.json** — cached timings (checked in so a full recompute isn't
  needed every time). 161 L11 entries.
- **detect.sh** — original silencedetect helper; superseded by build-pausemap.js.

## One command (recommended): update-question.js
After you want a question's video refreshed, this does the whole cycle —
re-render, sync the new videoUrl into data/l11.json, recompute the pause point,
rebuild quiz-data-l11.json + the quiz-app.html embed, commit and push:
```
node tools/quiz-app/update-question.js 1042            # render + propagate + push
node tools/quiz-app/update-question.js 1042 1057 1080  # several at once
node tools/quiz-app/update-question.js 1042 --no-push  # stop before pushing
node tools/quiz-app/update-question.js 1042 --no-render # you already rendered in the editor; just propagate
```
It renders via the render API (`vo.js` reproduces the editor's exact VO), so the
new video matches what the editor would produce. `questions.json` is left alone —
the render server auto-commits the videoUrl there itself, and the script's
`git pull --rebase` absorbs that commit before pushing.

## Manual run order (what update-question does internally)
```
# 1. (re-)render the affected videos from the editor / render API first
# 2. recompute pause points, then rebuild the public data + app:
node tools/quiz-app/build-pausemap.js
node tools/quiz-app/merge-inject.js
```

## CACHE GOTCHA (read before re-rendering)
`build-pausemap.js` skips any num already present in `pause-map.json`
(`if (done[q.num]) continue`). After re-rendering a video its audio length
changes, so the old pauseAt/resumeAt are wrong. **Delete those nums from
`pause-map.json` before re-running**, e.g.:
```
node -e 'const f="tools/quiz-app/pause-map.json";const p=require("./"+f);for(const n of [1001,1002]) delete p[n];require("fs").writeFileSync(f,JSON.stringify(p,null,0))'
```
Otherwise the stale timing survives and the video pauses in the wrong place.

## Dependency
Local ffmpeg (hardcoded path in build-pausemap.js):
`.../Gyan.FFmpeg.../ffmpeg-8.1.2-full_build/bin/ffmpeg.exe`. Update the `FF`
constant if ffmpeg moves. Paths in these scripts are absolute to this machine.

## Notes
- Videos are hosted on Cloudinary; the app + this data are fully static. The
  render/publisher server is only needed to (re-)render videos, not at runtime.
- Only 69 L11 questions needed a re-render (answer-letter geresh + rejected
  global niqqud); see memory `vo-geresh-drops-answer-letter`.
