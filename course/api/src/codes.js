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

module.exports = { genCode, issueCode };
