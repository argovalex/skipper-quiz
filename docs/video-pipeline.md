# Free vertical-video pipeline (`video/`)

Fully-free 9:16 explainer video per quiz question. **No paid cloud**: narration by
`edge-tts`, visuals reused from the CANONICAL `scenes.js` (rendered locally with
puppeteer), assembly by FFmpeg. Output looks identical to the render server because
the visual comes from the same `generateQuizHTML`.

## Run

```bash
# one question (default voice Avri, license 11)
PYTHONIOENCODING=utf-8 python -m video.make_question_video 1056

# Hila voice, a specific question
PYTHONIOENCODING=utf-8 python -m video.make_question_video 1114 --voice hila

# every license-11 question, skipping ones already rendered
PYTHONIOENCODING=utf-8 python -m video.make_question_video --all

# with a looping sea background clip (darkened ~40%) behind the card
PYTHONIOENCODING=utf-8 python -m video.make_question_video 1056 --bg-clip media/sea.mp4
```

Outputs land in `output/videos/`: `q<num>.mp4`, `q<num>.srt`, `q<num>.mp3`.
Use the machine's default `python` (3.14) — it has `edge-tts` (the lesson pipeline
uses the same interpreter). `ffmpeg`/`ffprobe`/`node` must be on PATH.

## Pipeline stages

1. **`video/render_frames.js`** (Node) loads `scenes.js` in a vm sandbox (same as
   `tools/quiz-app/scene-html.js`), builds `generateQuizHTML(q,'he',true)`, and
   screenshots the `#reel` element with puppeteer twice at 390×625 @3x:
   - `q<num>_question.png` — question state (options visible, no reveal).
   - `q<num>_answer.png` — after `window.__startAutoPlay()` fires the reveal
     (correct option green, banner, explanation in the footer).
   It also emits the canonical VO via `buildVoiceover(q)` (`tools/quiz-app/vo.js`).
2. **`video/make_question_video.py`** (Python):
   - Splits the VO on `[[PAUSE]]` into the question part and the answer part.
   - `edge-tts` synthesizes each part to MP3 and collects boundary events for
     synced captions (Hebrew voices emit `SentenceBoundary`, not word-level).
   - Builds four still segments over a background (Ken-Burns gradient, or the
     `--bg-clip`): question → 4 s think-pause with an on-screen countdown → answer
     → short outro hold.
   - Concats them (demuxer copy) and burns an ASS subtitle track.

## Script / VO format

The narration is the bank's canonical `voiceover_text`, rebuilt by `buildVoiceover(q)`:

```
שאלה מספר <num>... <question>. [[PAUSE]] התשובה הנכונה היא <letter>: <answer>. ... <explanation>
```

- `[[PAUSE]]` is the think-gap: 4 s of silence over the question frame with a
  4→1 countdown timer. Anything before it plays over the question frame; anything
  after, over the answer frame.
- The answer **letter** is spoken (`vo.js`, per the bank convention). The outro
  line "אלכס ארגוב · סקיפר דיגיטלי · alargov.com" is added as the final caption.

## Niqqud

The VO is fed to `edge-tts` **with its niqqud intact** — `buildVoiceover` already
bakes the lexicon (`references/niqqud-lexicon.md` → `vo-lexicon.js`) and the flag/
vessel-letter pronunciations. Niqqud improves edge-tts pronunciation (the lesson
pipeline feeds niqqud too), so we do **not** strip it. Captions, by contrast, have
niqqud stripped for readability. The "exception list" is therefore the lexicon
itself, applied upstream in `vo.js`; this module changes none of it.

## Adding a voice

Add an entry to `VOICES` in `make_question_video.py` (`{key: "he-IL-XxxNeural"}`)
and pass `--voice <key>`. Only Microsoft Hebrew neural voices are free via edge-tts.

## Adding / changing the background

Pass `--bg-clip <path>` to any looping video; it is scaled to fill 1080×1920,
cropped, and darkened ~40% behind the card. Without it, a deep-blue gradient with
a subtle Ken-Burns zoom is synthesized. The card itself is pinned near the top so
the bottom ~370 px stays a clean caption band.

## Deviations from the original spec (deliberate)

- **Visuals reuse `scenes.js`, not fresh Pillow cards.** Alex chose to keep the
  canonical visual so the vertical video never drifts from the server render.
  Consequently `python-bidi` / `arabic-reshaper` / Pillow are **not** used: the
  browser renders the card (native RTL) and libass renders captions (fribidi).
- **Niqqud is kept for TTS** (see above), not stripped.
- **Script comes from `voiceover_text`/`buildVoiceover`**, which already has the
  exact `number → question [[PAUSE]] answer → explanation` structure, rather than
  being rebuilt from `explanation`.

## License 12 visuals

`--license 12` works end to end. l12 questions carry no per-question diagram, so
`scenes.js` (guarded on `q.license === 12`, never touching l11) routes visuals as:
`"תמונה N"` question → `mediaUrl` to the official booklet image
`media/signs/tmuna_NNN.png` (served via raw.githubusercontent) → compass-rose /
`generateCompassRoseScene` → right-of-way `getScene` situation → clean
`neutralSceneL12()`. The 126 booklet images were cropped from
`חוברת סימנים.pdf` with PyMuPDF. Full detail: `lessons/l12/L12-INFO.md`.
Note l12 answers are still `answer_confirmed:false` and have no explanations —
verify before rendering for publish.

## Known issues / gotchas (Windows + this FFmpeg build)

- **`drawtext` + fontconfig segfaults** on the installed gyan FFmpeg 8.1. The timer
  uses a **relative `fontfile=f.ttf`** (Arial copied into the work dir, `cwd=work`)
  and fontconfig is avoided entirely. libass gets the font via `fontsdir=.`.
- **Captions must be ASS, not SRT.** An SRT is interpreted in libass's 384×288
  default space, so sizes/positions scale unpredictably; the ASS sets
  `PlayResX/Y=1080/1920` so styling is in true pixels.
- **Drive-colon paths break filtergraphs.** Anything referenced inside
  `-filter_complex`/`-vf` (fonts, subtitles) is passed by a relative name with
  `cwd=work`.
- **Long explanations → long videos** (Q1056 ≈ 99 s). Duration follows the VO; the
  content is not trimmed.
- `--all` is a large batch (161 questions, puppeteer + TTS + encode each). It skips
  existing `q<num>.mp4`. Run in chunks; expect minutes per question.
