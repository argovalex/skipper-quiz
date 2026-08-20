// One-time migration: flip every course video on Cloudinary from public `upload`
// delivery to `authenticated`, so a public URL no longer serves and the API's
// signed short-lived URLs (course/api/src/media.js) become the only way in.
//
// The secret never touches this file or the chat — the SDK reads CLOUDINARY_URL.
// Run from the repo root:
//
//   npm i cloudinary   (once)
//   CLOUDINARY_URL=cloudinary://<key>:<secret>@dzmyg9pel node tools/migrate-cloudinary-authenticated.js
//   PowerShell: $env:CLOUDINARY_URL="cloudinary://<key>:<secret>@dzmyg9pel"; node tools/migrate-cloudinary-authenticated.js
//
// Idempotent: an asset already authenticated is reported as "already" and skipped.
// Add --dry to list what would change without touching anything.

const fs = require('fs');
const path = require('path');
const cloudinary = require('cloudinary').v2; // reads CLOUDINARY_URL from env

const DRY = process.argv.includes('--dry');

// public_ids of the per-question reels, parsed out of the canonical bank.
function reelPublicIds() {
  const raw = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'l11.json'), 'utf8'));
  const ids = new Set();
  for (const q of raw) {
    const m = /res\.cloudinary\.com\/[^/]+\/video\/(?:upload|authenticated)\/(?:v\d+\/)?(.+?)\.[a-z0-9]+$/i.exec(q.videoUrl || '');
    if (m) ids.add(m[1]);
  }
  return [...ids];
}

// lesson + landing videos uploaded by tools/upload-course-videos.js
const LESSON_LANDING = [
  ...Array.from({ length: 13 }, (_, i) => `skipper-quiz/lessons/l${i + 1}`),
  'skipper-quiz/site/intro',
  'skipper-quiz/site/lesson-daysigns',
];

async function migrate(publicId) {
  if (DRY) { console.log('would migrate:', publicId); return 'dry'; }
  try {
    await cloudinary.uploader.rename(publicId, publicId, {
      resource_type: 'video', type: 'upload', to_type: 'authenticated', overwrite: true, invalidate: true,
    });
    return 'ok';
  } catch (e) {
    const msg = (e && e.message) || String(e);
    // Not found as `upload` usually means it is already authenticated.
    if (/not found/i.test(msg)) return 'already';
    throw e;
  }
}

(async () => {
  if (!process.env.CLOUDINARY_URL) {
    console.error('Set CLOUDINARY_URL first (cloudinary://<key>:<secret>@dzmyg9pel).');
    process.exit(1);
  }
  const ids = [...reelPublicIds(), ...LESSON_LANDING];
  console.error(`${ids.length} assets to migrate${DRY ? ' (dry run)' : ''}\n`);
  const tally = { ok: 0, already: 0, dry: 0, fail: 0 };
  for (const id of ids) {
    process.stderr.write(`  ${id} ... `);
    try {
      const r = await migrate(id);
      tally[r]++;
      process.stderr.write(r + '\n');
    } catch (e) {
      tally.fail++;
      process.stderr.write('FAIL: ' + ((e && e.message) || e) + '\n');
    }
  }
  console.error(`\ndone — ok:${tally.ok} already:${tally.already} dry:${tally.dry} fail:${tally.fail}`);
  process.exit(tally.fail ? 1 : 0);
})();
