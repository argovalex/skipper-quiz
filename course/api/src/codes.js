// Access codes: issue on purchase, validate on access, enforce device limit.
const crypto = require('crypto');
const db = require('./db');

const ALPHA = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // no ambiguous 0/O/1/I
const chunk = () => Array.from({ length: 4 }, () => ALPHA[crypto.randomInt(ALPHA.length)]).join('');

function genCode() { return `SK-${chunk()}-${chunk()}`; }

async function issueCode(email, purchaseId, deviceLimit) {
  const code = genCode();
  await db.q(
    'insert into access_codes(code, email, purchase_id, device_limit) values ($1,$2,$3,$4)',
    [code, email, purchaseId || null, deviceLimit || 1]
  );
  await db.q('insert into progress(code) values ($1) on conflict do nothing', [code]);
  return code;
}

// Returns { ok, email?, reason? }. Dev master code bypasses DB for local testing.
async function validate(code, deviceId) {
  if (!code) return { ok: false, reason: 'missing-code' };
  if (process.env.DEV_ACCESS_CODE && code === process.env.DEV_ACCESS_CODE) return { ok: true, dev: true };
  if (!db.hasDb()) return { ok: false, reason: 'no-db' };

  const r = await db.q('select * from access_codes where code=$1', [code]);
  if (!r.rows.length) return { ok: false, reason: 'not-found' };
  const row = r.rows[0];
  if (row.revoked) return { ok: false, reason: 'revoked' };

  if (deviceId) {
    const ex = await db.q('select 1 from code_devices where code=$1 and device_id=$2', [code, deviceId]);
    if (!ex.rows.length) {
      const c = await db.q('select count(*)::int n from code_devices where code=$1', [code]);
      if (c.rows[0].n >= row.device_limit) return { ok: false, reason: 'device-limit' };
      await db.q('insert into code_devices(code, device_id) values ($1,$2)', [code, deviceId]);
    } else {
      await db.q('update code_devices set last_seen=now() where code=$1 and device_id=$2', [code, deviceId]);
    }
  }
  return { ok: true, email: row.email };
}

module.exports = { genCode, issueCode, validate };
