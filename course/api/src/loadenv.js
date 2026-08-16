// Minimal .env loader for local dev. On Railway real env vars are injected and
// this file finds no .env (no-op). Must be required BEFORE ./db (db reads env at load).
const fs = require('fs');
const path = require('path');
try {
  const txt = fs.readFileSync(path.join(__dirname, '..', '.env'), 'utf8');
  for (const line of txt.split(/\r?\n/)) {
    const m = line.match(/^\s*([A-Za-z0-9_]+)\s*=\s*(.*?)\s*$/);
    if (!m || line.trim().startsWith('#')) continue;
    let val = m[2];
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) val = val.slice(1, -1);
    if (!(m[1] in process.env)) process.env[m[1]] = val;
  }
  console.error('📄 .env loaded');
} catch { /* no .env — fine */ }
