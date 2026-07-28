// Detect the [[PAUSE]] boundary in each L11 video via ffmpeg silencedetect.
// Output: pause-map.json  { "1001": {pauseAt, resumeAt, dur}, ... }  (resume-safe)
const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const FF = "C:/Users/argov/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.2-full_build/bin/ffmpeg.exe";
const BANK = "C:/Users/argov/OneDrive/Co-Work OS/SkipperQuiz/data/l11.json";
const OUT = path.join(__dirname, "pause-map.json");

const data = JSON.parse(fs.readFileSync(BANK, "utf8"));
const vids = data.filter(q => q.videoUrl);
const done = fs.existsSync(OUT) ? JSON.parse(fs.readFileSync(OUT, "utf8")) : {};
console.log(`total ${vids.length} videos, already done ${Object.keys(done).length}`);

function parse(log) {
  const durM = log.match(/Duration:\s*(\d+):(\d+):([\d.]+)/);
  const dur = durM ? (+durM[1]) * 3600 + (+durM[2]) * 60 + (+durM[3]) : null;
  const re = /silence_start:\s*([\d.]+)[\s\S]*?silence_end:\s*([\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)/g;
  let m, best = null;
  while ((m = re.exec(log))) {
    const s = +m[1], e = +m[2], d = +m[3];
    if (s > 1.5 && (dur ? e < dur - 0.5 : true) && d >= 3.0) {
      if (!best || d > best.d) best = { s, e, d };
    }
  }
  return { dur, best };
}

let i = 0;
for (const q of vids) {
  i++;
  if (done[q.num]) continue;
  const r = spawnSync(FF, ["-hide_banner", "-i", q.videoUrl, "-vn",
    "-af", "silencedetect=noise=-30dB:d=0.8", "-f", "null", "-"],
    { encoding: "utf8", maxBuffer: 1 << 26 });
  const log = (r.stderr || "") + (r.stdout || "");
  const { dur, best } = parse(log);
  if (best) {
    done[q.num] = { pauseAt: +best.s.toFixed(2), resumeAt: +best.e.toFixed(2), dur: dur ? +dur.toFixed(2) : null };
    console.log(`[${i}/${vids.length}] Q${q.num}  pause=${done[q.num].pauseAt}  resume=${done[q.num].resumeAt}  dur=${done[q.num].dur}`);
  } else {
    done[q.num] = { pauseAt: null, resumeAt: null, dur: dur ? +dur.toFixed(2) : null };
    console.log(`[${i}/${vids.length}] Q${q.num}  NO CLEAR PAUSE  dur=${dur}  (silenceHits=${(log.match(/silence_start/g)||[]).length})`);
  }
  fs.writeFileSync(OUT, JSON.stringify(done, null, 0));
}
const miss = Object.entries(done).filter(([k, v]) => v.pauseAt == null).map(([k]) => k);
console.log(`\nDONE. ${Object.keys(done).length} processed, ${miss.length} without clear pause: ${miss.join(",")}`);
