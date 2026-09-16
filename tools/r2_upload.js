// r2_upload.js — upload a local file to the Cloudflare R2 bucket (skipperquiz-reels)
// and return its public r2.dev URL. S3-compatible PUT, signed with aws4fetch.
//
//     node tools/r2_upload.js <file> [key]
//
// Reads R2_ACCOUNT_ID / R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY / R2_ENDPOINT /
// R2_BUCKET / R2_PUBLIC_URL_BASE from .env (repo root) or the environment.
const fs = require('fs');
const path = require('path');
const { AwsClient } = require('aws4fetch');

function loadEnvFile() {
  const envPath = path.join(__dirname, '..', '.env');
  if (!fs.existsSync(envPath)) return;
  for (const line of fs.readFileSync(envPath, 'utf8').split('\n')) {
    const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
    if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].trim();
  }
}
loadEnvFile();

const CONTENT_TYPES = { '.mp4': 'video/mp4', '.mp3': 'audio/mpeg', '.srt': 'text/plain', '.png': 'image/png', '.jpg': 'image/jpeg' };

async function uploadToR2(filePath, key) {
  const { R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT, R2_BUCKET, R2_PUBLIC_URL_BASE } = process.env;
  if (!R2_ACCESS_KEY_ID || !R2_SECRET_ACCESS_KEY || !R2_ENDPOINT || !R2_BUCKET || !R2_PUBLIC_URL_BASE) {
    throw new Error('R2 env vars missing — expected R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT, R2_BUCKET, R2_PUBLIC_URL_BASE in .env');
  }
  key = key || path.basename(filePath);
  const body = fs.readFileSync(filePath);
  const contentType = CONTENT_TYPES[path.extname(filePath).toLowerCase()] || 'application/octet-stream';

  const client = new AwsClient({ accessKeyId: R2_ACCESS_KEY_ID, secretAccessKey: R2_SECRET_ACCESS_KEY });
  const putUrl = `${R2_ENDPOINT}/${R2_BUCKET}/${key}`;
  const res = await client.fetch(putUrl, { method: 'PUT', body, headers: { 'Content-Type': contentType } });
  if (!res.ok) throw new Error(`R2 upload failed: ${res.status} ${await res.text()}`);
  return `${R2_PUBLIC_URL_BASE}/${key}`;
}

module.exports = { uploadToR2 };

if (require.main === module) {
  const filePath = process.argv[2];
  if (!filePath) {
    console.error('usage: node tools/r2_upload.js <file> [key]');
    process.exit(1);
  }
  uploadToR2(filePath, process.argv[3])
    .then(url => console.log(url))
    .catch(e => { console.error(e.message); process.exit(1); });
}
