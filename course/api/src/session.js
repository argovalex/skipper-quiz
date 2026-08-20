// Server-issued rotating sessions — the anti-copy layer.
//
// The client never holds a reusable device handle. On start() the server mints a
// device_id and an opaque `sid`, delivered as an httpOnly cookie. resolve() rotates
// the sid every ROTATE_MS and keeps at most ONE active session per device_id.
//
// Effect on a copied cookie jar: the clone and its origin share one device_id
// lineage, so they compete for the single active session. Whenever one rotates,
// the other's sid becomes superseded and it must re-start — the two keep kicking
// each other out. A single honest client (one cookie jar) never self-competes, and
// separate honest devices each claim their own device slot, so they coexist up to
// device_limit. Copying is not prevented (impossible on the web) — concurrent use
// of a copy is made unusable.
const crypto = require('crypto');
const db = require('./db');

const ROTATE_MS = 10 * 60 * 1000; // rotate an active sid once it is older than this
const GRACE_MS = 8 * 1000;        // a just-rotated sid still works briefly (covers in-flight request races)

const newSid = () => crypto.randomBytes(24).toString('base64url');
const newDevice = () => 'srv-' + crypto.randomBytes(12).toString('base64url');

function devBypass(code) {
  return process.env.DEV_ACCESS_CODE && code === process.env.DEV_ACCESS_CODE && process.env.NODE_ENV !== 'production';
}

// Look up the (possibly inactive) session a prior cookie points at, if it belongs
// to `code` — lets a returning client reuse its device slot instead of burning a
// new one when its cookie rotated or expired.
async function priorDevice(priorSid, code) {
  if (!priorSid) return null;
  const r = await db.q('select code, device_id from sessions where sid=$1', [priorSid]);
  const row = r.rows[0];
  return row && row.code === code ? row.device_id : null;
}

// Open a session for a valid code. Claims (or reuses) a device slot atomically and
// deactivates any other session on that device so only one stays live.
async function start(code, priorSid) {
  code = (code || '').trim();
  if (!code) return { ok: false, reason: 'missing-code' };
  if (devBypass(code)) {
    const sid = newSid();
    if (db.hasDb()) await db.q('insert into sessions(sid, code, device_id) values ($1,$2,$3)', [sid, code, 'dev']).catch(() => {});
    return { ok: true, sid, dev: true };
  }
  if (!db.hasDb()) return { ok: false, reason: 'no-db' };

  const reuse = await priorDevice(priorSid, code);
  return db.tx(async (c) => {
    const r = await c.query('select code, revoked, device_limit from access_codes where code=$1 for update', [code]);
    if (!r.rows.length) return { ok: false, reason: 'not-found' };
    const row = r.rows[0];
    if (row.revoked) return { ok: false, reason: 'revoked' };

    let device = reuse;
    if (!device) {
      const cnt = await c.query('select count(distinct device_id)::int n from code_devices where code=$1', [code]);
      if (cnt.rows[0].n >= row.device_limit) return { ok: false, reason: 'device-limit' };
      device = newDevice();
      await c.query('insert into code_devices(code, device_id) values ($1,$2) on conflict do nothing', [code, device]);
    }
    // Only one live session per device.
    await c.query('update sessions set active=false, rotated_at=now() where device_id=$1 and active=true', [device]);
    const sid = newSid();
    await c.query('insert into sessions(sid, code, device_id) values ($1,$2,$3)', [sid, code, device]);
    await c.query('insert into progress(code) values ($1) on conflict do nothing', [code]);
    return { ok: true, sid, email: row.email };
  });
}

// Validate the cookie's sid. Returns { ok, code, sid } where sid may be a freshly
// rotated value the caller must write back as a cookie. Superseded/absent → not ok.
async function resolve(sid) {
  if (!sid) return { ok: false, reason: 'no-session' };
  if (!db.hasDb()) return { ok: false, reason: 'no-db' };
  const r = await db.q('select * from sessions where sid=$1', [sid]);
  if (!r.rows.length) return { ok: false, reason: 'no-session' };
  const s = r.rows[0];

  if (s.device_id !== 'dev') {
    const ac = await db.q('select revoked from access_codes where code=$1', [s.code]);
    if (!ac.rows.length || ac.rows[0].revoked) return { ok: false, reason: 'revoked' };
  }

  if (!s.active) {
    // Superseded token. Within a short grace, hand back the current active sid so a
    // legit in-flight request race doesn't get logged out.
    if (s.rotated_at && Date.now() - new Date(s.rotated_at).getTime() < GRACE_MS) {
      const cur = await db.q(
        'select sid from sessions where device_id=$1 and active=true order by created_at desc limit 1',
        [s.device_id]
      );
      if (cur.rows.length) return { ok: true, code: s.code, sid: cur.rows[0].sid, rotated: true };
    }
    return { ok: false, reason: 'superseded' };
  }

  const age = Date.now() - new Date(s.created_at).getTime();
  if (age > ROTATE_MS) {
    const ns = newSid();
    await db.tx(async (c) => {
      await c.query('update sessions set active=false, rotated_at=now() where device_id=$1 and active=true', [s.device_id]);
      await c.query('insert into sessions(sid, code, device_id) values ($1,$2,$3)', [ns, s.code, s.device_id]);
    });
    return { ok: true, code: s.code, sid: ns, rotated: true };
  }
  await db.q('update sessions set last_seen=now() where sid=$1', [sid]);
  return { ok: true, code: s.code, sid };
}

// End a session (logout). Frees nothing device-wise; the slot stays claimed.
async function end(sid) {
  if (sid && db.hasDb()) await db.q('update sessions set active=false, rotated_at=now() where sid=$1', [sid]).catch(() => {});
}

module.exports = { start, resolve, end, ROTATE_MS };
