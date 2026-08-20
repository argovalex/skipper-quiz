// One-time launch utility: upload the 13 lesson videos + 2 landing videos to
// Cloudinary and print a JSON map of secure URLs to paste back.
//
// The Cloudinary SDK auto-configures from the CLOUDINARY_URL env var, so the
// secret never touches this file or the chat. Run from the repo root:
//
//   npm i cloudinary
//   CLOUDINARY_URL=cloudinary://<key>:<secret>@dzmyg9pel node tools/upload-course-videos.js
//
// (PowerShell:  $env:CLOUDINARY_URL="cloudinary://<key>:<secret>@dzmyg9pel"; node tools/upload-course-videos.js )
//
// Progress goes to stderr; the final JSON goes to stdout — copy that block back.

const cloudinary = require('cloudinary').v2; // reads CLOUDINARY_URL from env

// lessonId -> topic folder name (matches LESSONS[] ids in course/app/index.html)
const LESSONS = [
  ['1',  'אופנוע ים - כללי'],
  ['2',  'אזורי שיט ומהירויות'],
  ['3',  'זכות מעבר'],
  ['4',  'אותות קוליים'],
  ['5',  'סימני יום'],
  ['6',  'דגל צולל'],
  ['7',  'מצוקה'],
  ['8',  'מטאורולוגיה'],
  ['9',  'ניווט וכניסה לנמל'],
  ['10', 'סכנות רכיבה ותמרון'],
  ['11', 'תמרוני ספינה'],
  ['12', 'עזרה ראשונה'],
  ['13', 'בטיחות אש ותדלוק'],
];

const LANDING = [
  ['intro',           'course/site/assets/intro.mp4'],
  ['lesson-daysigns', 'course/site/assets/lesson-daysigns.mp4'],
];

async function up(file, folder, public_id, label) {
  process.stderr.write(`↑ ${label} ... `);
  const r = await cloudinary.uploader.upload(file, {
    resource_type: 'video', type: 'authenticated', folder, public_id, overwrite: true, invalidate: true,
  });
  process.stderr.write('ok\n');
  return r.secure_url;
}

(async () => {
  if (!process.env.CLOUDINARY_URL) {
    console.error('Set CLOUDINARY_URL first (cloudinary://<key>:<secret>@dzmyg9pel).');
    process.exit(1);
  }
  const out = { lessons: {}, landing: {} };
  for (const [id, name] of LESSONS) {
    out.lessons[id] = await up(`lessons/l11/cards/${name}/${name}.mp4`, 'skipper-quiz/lessons', `l${id}`, `lesson ${id} — ${name}`);
  }
  for (const [key, file] of LANDING) {
    out.landing[key] = await up(file, 'skipper-quiz/site', key, `landing ${key}`);
  }
  console.log(JSON.stringify(out, null, 2));
})().catch(e => { console.error('\n' + (e.message || e)); process.exit(1); });
