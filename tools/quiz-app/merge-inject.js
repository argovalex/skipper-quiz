// Merge pause-map into the public data file, then embed it into the player.
// License-aware: `node merge-inject.js [--license N]` (default 11).
const fs = require("fs");
const { paths, parseLicense } = require("./paths");
const P = paths(parseLicense());
const bank = JSON.parse(fs.readFileSync(P.bank, "utf8"));
const pmap = fs.existsSync(P.pauseMap) ? JSON.parse(fs.readFileSync(P.pauseMap, "utf8")) : {};

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
fs.writeFileSync(P.quizData, dataStr, "utf8");

const withPause = pub.filter(q => q.pauseAt != null).length;
console.log(`public data (l${P.license}): ${pub.length} questions, ${withPause} with pause point, ${pub.length - withPause} without`);

// Embed into the player. l11 uses quiz-app.html; other licenses expect quiz-app-l<N>.html.
if (fs.existsSync(P.quizApp)) {
  let html = fs.readFileSync(P.quizApp, "utf8");
  const safe = dataStr.replace(/<\//g, "<\\/");
  const re = /(<script id="quiz-data" type="application\/json">)([\s\S]*?)(<\/script>)/;
  if (re.test(html)) html = html.replace(re, "$1" + safe + "$3");
  else html = html.replace("__QUIZ_DATA__", safe);
  fs.writeFileSync(P.quizApp, html, "utf8");
  console.log(`embedded into ${require("path").basename(P.quizApp)} (${(fs.statSync(P.quizApp).size / 1024).toFixed(1)} KB)`);
} else {
  console.log(`player ${require("path").basename(P.quizApp)} not found — wrote ${require("path").basename(P.quizData)} only (create the player to embed)`);
}
