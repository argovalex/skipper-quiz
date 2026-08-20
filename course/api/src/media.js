// Signs Cloudinary video URLs for time-limited, authenticated delivery.
//
// The bank stores public `.../video/upload/v###/skipper-quiz/<id>.mp4` URLs. Once
// the assets are migrated to delivery type `authenticated` (see
// tools/migrate-cloudinary-authenticated.js), a public URL no longer serves — the
// server must hand out a signed URL that expires. We re-sign per request from the
// stored public_id, so the stored URLs never need rewriting.
//
// Config comes from CLOUDINARY_URL (cloudinary://<key>:<secret>@<cloud>) — the
// secret stays in the server env, never in the client or the bank. With no creds
// the functions pass URLs through unchanged, so nothing breaks before migration.
//
// Expiry needs token-based auth: set CLOUDINARY_AUTH_TOKEN_KEY (Console → Settings →
// Security → the auth-token key). With it, each URL carries `__cld_token__` and dies
// after MEDIA_TTL — a leaked link stops working. Without it we still emit an
// authenticated *signed* URL (blocks unsigned/public access and scraping), but that
// signed link does NOT expire, so set the key to get the "leaked link dies" property.
const TTL = parseInt(process.env.MEDIA_TTL || '14400', 10); // 4h default
const AUTH_TOKEN_KEY = process.env.CLOUDINARY_AUTH_TOKEN_KEY || null;
let warnedNoToken = false;

let cld = null;
try {
  if (process.env.CLOUDINARY_URL || process.env.CLOUDINARY_API_SECRET) {
    cld = require('cloudinary').v2;
    cld.config({ secure: true }); // CLOUDINARY_URL auto-loads; explicit config also honored
    if (process.env.CLOUDINARY_CLOUD_NAME && !process.env.CLOUDINARY_URL) {
      cld.config({
        cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
        api_key: process.env.CLOUDINARY_API_KEY,
        api_secret: process.env.CLOUDINARY_API_SECRET,
        secure: true,
      });
    }
  }
} catch (e) {
  console.warn('media: cloudinary SDK unavailable (' + e.message + ') — serving unsigned URLs');
  cld = null;
}

const enabled = () => !!cld;

// Pull { resource_type, public_id } out of a stored Cloudinary delivery URL.
// e.g. https://res.cloudinary.com/dzmyg9pel/video/upload/v1786890419/skipper-quiz/abc.mp4
//   -> { resource_type: 'video', public_id: 'skipper-quiz/abc' }
function parse(url) {
  const m = /res\.cloudinary\.com\/[^/]+\/([a-z]+)\/(?:authenticated|private|upload)\/(?:s--[^/]+--\/)?(?:v\d+\/)?(.+?)(?:\.[a-z0-9]+)?$/i.exec(url || '');
  if (!m) return null;
  return { resource_type: m[1], public_id: m[2] };
}

// Return a signed authenticated URL with expiry, or the original if signing is off
// or the URL isn't a Cloudinary asset we recognize.
function sign(url) {
  if (!cld || !url) return url;
  const p = parse(url);
  if (!p) return url;
  try {
    const opts = { resource_type: p.resource_type, type: 'authenticated', secure: true, sign_url: true };
    if (AUTH_TOKEN_KEY) {
      opts.auth_token = { key: AUTH_TOKEN_KEY, duration: TTL }; // time-limited: URL expires after TTL
    } else if (!warnedNoToken) {
      console.warn('media: CLOUDINARY_AUTH_TOKEN_KEY not set — signed URLs will not expire');
      warnedNoToken = true;
    }
    return cld.url(p.public_id, opts);
  } catch (e) {
    return url;
  }
}

// Return a copy of the lessons map with every question's `vid` re-signed. Never
// mutates the cached object — signs a fresh copy per request so expiry stays fresh.
function signLessons(lessons) {
  if (!cld || !lessons) return lessons;
  const out = {};
  for (const id of Object.keys(lessons)) {
    const l = lessons[id];
    out[id] = { ...l, questions: (l.questions || []).map(q => (q && q.vid ? { ...q, vid: sign(q.vid) } : q)) };
  }
  return out;
}

module.exports = { sign, signLessons, enabled, TTL };
