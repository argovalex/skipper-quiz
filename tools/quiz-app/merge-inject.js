// Merge pause-map into the public data file, then embed it into quiz-app.html.
const fs = require("fs");
const ROOT = "C:/Users/argov/OneDrive/Co-Work OS/SkipperQuiz";
const bank = JSON.parse(fs.readFileSync(ROOT + "/data/l11.json", "utf8"));
const pmap = JSON.parse(fs.readFileSync(__dirname + "/pause-map.json", "utf8"));

const pub = bank.map(q => {
  const pm = pmap[q.num] || {};
  return {
    num: q.num,
    topic: q.topic,
    q: q.q_he,
    options: q.options,
    answer: q.answer,
    explanation: q.explanation || "",
    mediaUrl: q.mediaUrl || "",
    videoUrl: q.videoUrl || "",
    pauseAt: pm.pauseAt ?? null,
    resumeAt: pm.resumeAt ?? null
  };
});

const dataStr = JSON.stringify(pub, null, 0);
fs.writeFileSync(ROOT + "/quiz-data-l11.json", dataStr, "utf8");

let html = fs.readFileSync(ROOT + "/quiz-app.html", "utf8");
const safe = dataStr.replace(/<\//g, "<\\/");
const re = /(<script id="quiz-data" type="application\/json">)([\s\S]*?)(<\/script>)/;
if (re.test(html)) html = html.replace(re, "$1" + safe + "$3");
else html = html.replace("__QUIZ_DATA__", safe);
fs.writeFileSync(ROOT + "/quiz-app.html", html, "utf8");

const withPause = pub.filter(q => q.pauseAt != null).length;
console.log(`public data: ${pub.length} questions, ${withPause} with pause point, ${pub.length - withPause} without`);
console.log(`html size: ${(fs.statSync(ROOT + "/quiz-app.html").size / 1024).toFixed(1)} KB`);
