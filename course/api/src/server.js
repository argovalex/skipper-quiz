// SkipperQuiz course API — phase A foundation.
// Endpoints: health, free window, code-gated content, progress, coupon validate,
// Tranzila notify (issues access code), admin content reload.
require('./loadenv');
const express = require('express');
const db = require('./db');
const content = require('./content');
const codes = require('./codes');
const settings = require('./settings');
const email = require('./email');
const invoice = require('./invoice');
const crypto = require('crypto');

const app = express();
app.use(express.json({ limit: '256kb' }));
app.use(express.urlencoded({ extended: true })); // Tranzila posts urlencoded

// ── CORS (PWA is a different origin) ────────────────────────────────────────
const ORIGINS = process.env.ALLOWED_ORIGINS || '*';
app.use((req, res, next) => {
  res.set('Access-Control-Allow-Origin', ORIGINS);
  res.set('Access-Control-Allow-Headers', 'Content-Type, x-code, x-device, x-admin');
  res.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  if (req.method === 'OPTIONS') return res.sendStatus(204);
  next();
});

const codeOf = req => req.header('x-code') || req.query.code || (req.body && req.body.code);
const deviceOf = req => req.header('x-device') || req.query.device || (req.body && req.body.device);
const gate = async req => codes.validate(codeOf(req), deviceOf(req));

// ── Health ──────────────────────────────────────────────────────────────────
app.get('/health', (req, res) => res.json({ ok: true, db: db.hasDb(), ts: Date.now() }));

// ── Public config (brand name + price, editable via admin) ────────────────────
app.get('/api/config', async (req, res) => {
  try {
    const [cfg, pr] = await Promise.all([settings.all(), settings.pricing()]);
    // price_ils reflects the current effective price (founders → regular) for display.
    res.json({ ok: true, ...cfg, price_ils: pr.price, pricing: pr });
  } catch (e) { res.status(500).json({ ok: false, error: e.message }); }
});

// Update brand/price without redeploy. Protected by ADMIN_TOKEN.
app.post('/api/config', async (req, res) => {
  if (!process.env.ADMIN_TOKEN || req.header('x-admin') !== process.env.ADMIN_TOKEN) {
    return res.status(403).json({ ok: false });
  }
  if (!db.hasDb()) return res.status(503).json({ ok: false, reason: 'no-db' });
  const allowed = ['brand_name', 'product_title', 'price_ils', 'price_founders', 'price_regular', 'founders_slots'];
  for (const k of allowed) if (req.body[k] != null) await settings.set(k, req.body[k]);
  res.json({ ok: true, ...(await settings.all()) });
});

// ── Free window (no code) ─────────────────────────────────────────────────────
app.get('/api/free', async (req, res) => {
  try {
    const lessons = await content.load();
    res.json({ ok: true, lessons: content.freeSubset(lessons) });
  } catch (e) { res.status(500).json({ ok: false, error: e.message }); }
});

// ── Paid content (code-gated) ─────────────────────────────────────────────────
app.get('/api/content', async (req, res) => {
  const v = await gate(req);
  if (!v.ok) return res.status(403).json({ ok: false, reason: v.reason });
  try {
    const [lessons, cfg, pr] = await Promise.all([content.load(), settings.all(), settings.pricing()]);
    res.json({ ok: true, price_ils: pr.price, brand_name: cfg.brand_name, product_title: cfg.product_title, lessons });
  } catch (e) { res.status(500).json({ ok: false, error: e.message }); }
});

// ── Progress (per code) ────────────────────────────────────────────────────────
app.get('/api/progress', async (req, res) => {
  const v = await gate(req);
  if (!v.ok) return res.status(403).json({ ok: false, reason: v.reason });
  if (!db.hasDb()) return res.status(503).json({ ok: false, reason: 'no-db' });
  const r = await db.q('select data from progress where code=$1', [codeOf(req)]);
  res.json({ ok: true, data: r.rows[0] ? r.rows[0].data : {} });
});

app.post('/api/progress', async (req, res) => {
  const v = await gate(req);
  if (!v.ok) return res.status(403).json({ ok: false, reason: v.reason });
  if (!db.hasDb()) return res.status(503).json({ ok: false, reason: 'no-db' });
  const data = (req.body && req.body.data) || {};
  await db.q(
    `insert into progress(code, data, updated_at) values ($1, $2, now())
     on conflict(code) do update set data=$2, updated_at=now()`,
    [codeOf(req), data]
  );
  res.json({ ok: true });
});

// ── Coupon validation (server-side pricing + attribution) ──────────────────────
app.post('/api/coupon/validate', async (req, res) => {
  const code = req.body && req.body.coupon;
  if (!code) return res.status(400).json({ ok: false, reason: 'missing' });
  if (!db.hasDb()) return res.status(503).json({ ok: false, reason: 'no-db' });
  const r = await db.q('select * from coupons where lower(code)=lower($1) and active=true', [code]);
  if (!r.rows.length) return res.json({ ok: false, reason: 'invalid' });
  const c = r.rows[0];
  if (c.max_uses != null && c.uses >= c.max_uses) return res.json({ ok: false, reason: 'exhausted' });
  res.json({ ok: true, kind: c.kind, value: Number(c.value), partner_ref: c.partner_ref });
});

// ── Coupon redeem: full-access (instructors). Issues a code without checkout. ──
app.post('/api/coupon/redeem', async (req, res) => {
  const coupon = req.body && req.body.coupon;
  const email = req.body && req.body.email;
  if (!coupon || !email) return res.status(400).json({ ok: false, reason: 'missing' });
  if (!db.hasDb()) return res.status(503).json({ ok: false, reason: 'no-db' });
  const r = await db.q('select * from coupons where lower(code)=lower($1) and active=true', [coupon]);
  if (!r.rows.length) return res.json({ ok: false, reason: 'invalid' });
  const c = r.rows[0];
  if (c.kind !== 'full') return res.json({ ok: false, reason: 'not-full' }); // discount coupons go through checkout
  if (c.max_uses != null && c.uses >= c.max_uses) return res.json({ ok: false, reason: 'exhausted' });
  try {
    const p = await db.q(
      `insert into purchases(email, amount_ils, coupon_code, partner_ref, status)
       values ($1, 0, $2, $3, 'comp') returning id`,
      [email, c.code, c.partner_ref]
    );
    const code = await codes.issueCode(email, p.rows[0].id);
    await db.q('update coupons set uses=uses+1 where code=$1', [c.code]);
    console.log(`🎓 full-access redeem: ${email} via ${c.code} → ${code}`);
    res.json({ ok: true, code });
  } catch (e) {
    console.error('redeem error', e.message);
    res.status(500).json({ ok: false, error: e.message });
  }
});

// ── Checkout + payment (Tranzila) ──────────────────────────────────────────────
const genToken = () => crypto.randomBytes(18).toString('base64url');
function applyCoupon(base, c) {
  if (!c) return base;
  if (c.kind === 'percent') return Math.max(0, Math.round(base * (1 - Number(c.value) / 100)));
  if (c.kind === 'fixed' || c.kind === 'full') return Math.max(0, base - Number(c.value));
  return base;
}
const selfBase = req => (process.env.PUBLIC_URL || (req.protocol + '://' + req.get('host'))).replace(/\/$/, '');
function buildCheckoutUrl(req, token, amount, buyer, ret) {
  const term = process.env.TRANZILA_TERMINAL;
  const returnTo = ret || selfBase(req);
  const success = returnTo + (returnTo.includes('?') ? '&' : '?') + 'token=' + encodeURIComponent(token);
  if (term) {
    // Real Tranzila hosted page. Field names refined at real-connect; notify is configured on the terminal.
    const p = new URLSearchParams({
      sum: String(amount), currency: '1', email: buyer || '', pdesc: 'course access', token,
      success_url_address: success, fail_url_address: returnTo,
    });
    return `https://direct.tranzila.com/${term}/iframenew.php?${p.toString()}`;
  }
  // Simulated hosted page (until the real terminal is connected).
  const p = new URLSearchParams({ token, amount: String(amount), email: buyer || '', ret: returnTo });
  return selfBase(req) + '/api/dev/checkout?' + p.toString();
}

// Shared: turn a pending purchase into a paid one — issue code, email, invoice. Idempotent.
async function finalize(p, txn) {
  if (p.status === 'paid') {
    const c = await db.q('select code from access_codes where purchase_id=$1', [p.id]);
    return c.rows[0] && c.rows[0].code;
  }
  const code = await codes.issueCode(p.email, p.id);
  await db.q("update purchases set status='paid', tranzila_txn=$2 where id=$1", [p.id, txn]);
  if (p.coupon_code) await db.q('update coupons set uses=uses+1 where lower(code)=lower($1)', [p.coupon_code]);
  await email.sendCode(p.email, code);
  await invoice.issue({ email: p.email, amount: Number(p.amount_ils), code });
  console.error(`💳 finalized ${p.email} → ${code} (₪${p.amount_ils}${p.coupon_code ? ', ' + p.coupon_code : ''})`);
  return code;
}
async function finalizeById(id, txn) {
  const r = await db.q('select * from purchases where id=$1', [id]);
  return r.rows.length ? finalize(r.rows[0], txn) : null;
}

// Start a checkout: price it (coupon applied server-side), create a pending order, return checkout URL.
app.post('/api/checkout', async (req, res) => {
  if (!db.hasDb()) return res.status(503).json({ ok: false, reason: 'no-db' });
  const { email: buyer, coupon, return_url } = req.body || {};
  if (!buyer || !/.+@.+/.test(buyer)) return res.status(400).json({ ok: false, reason: 'bad-email' });
  const pr = await settings.pricing();
  let amount = pr.price, couponRow = null, partner = null;
  if (coupon) {
    const r = await db.q('select * from coupons where lower(code)=lower($1) and active=true', [coupon]);
    if (r.rows.length) {
      const c = r.rows[0];
      if (!(c.max_uses != null && c.uses >= c.max_uses)) { amount = applyCoupon(amount, c); couponRow = c; partner = c.partner_ref; }
    }
  }
  const token = genToken();
  const p = await db.q(
    `insert into purchases(email, amount_ils, coupon_code, partner_ref, status, token)
     values ($1,$2,$3,$4,'pending',$5) returning id`,
    [buyer, amount, couponRow ? couponRow.code : null, partner, token]
  );
  if (amount <= 0) { // 100% coupon → free, no checkout
    const code = await finalizeById(p.rows[0].id, 'FREE-' + token);
    return res.json({ ok: true, amount: 0, order_token: token, code, checkout_url: null });
  }
  res.json({ ok: true, amount, order_token: token, checkout_url: buildCheckoutUrl(req, token, amount, buyer, return_url) });
});

// App polls this after returning from checkout to get its code once paid.
app.get('/api/order/status', async (req, res) => {
  if (!db.hasDb()) return res.status(503).json({ ok: false, reason: 'no-db' });
  const token = req.query.token;
  if (!token) return res.status(400).json({ ok: false });
  const r = await db.q('select id, status from purchases where token=$1', [token]);
  if (!r.rows.length) return res.json({ ok: false, reason: 'not-found' });
  const row = r.rows[0];
  let code = null;
  if (row.status === 'paid') {
    const c = await db.q('select code from access_codes where purchase_id=$1', [row.id]);
    code = c.rows[0] && c.rows[0].code;
  }
  res.json({ ok: true, status: row.status, code });
});

// Tranzila server-to-server notify → finalize the order.
app.post('/api/tranzila/notify', async (req, res) => {
  if (!db.hasDb()) return res.status(503).send('no-db');
  const b = req.body || {};
  if (process.env.TRANZILA_NOTIFY_SECRET && b.secret !== process.env.TRANZILA_NOTIFY_SECRET) {
    return res.status(403).send('bad-secret');
  }
  const token = b.token || b.uid || null;
  const txn = b.Tempref || b.ConfirmationCode || b.index || ('TZ-' + Date.now());
  const approved = b.Response === '000' || b.approved === '1' || !process.env.TRANZILA_TERMINAL || !!b.Tempref;
  if (!approved) return res.send('OK');
  try {
    let purchase = null;
    if (token) { const r = await db.q('select * from purchases where token=$1', [token]); purchase = r.rows[0]; }
    if (!purchase && b.email) {
      const r = await db.q("insert into purchases(email, amount_ils, status, token) values ($1,$2,'pending',$3) returning *",
        [b.email, Number(b.sum || 0), txn]);
      purchase = r.rows[0];
    }
    if (!purchase) return res.status(400).send('no-order');
    await finalize(purchase, txn);
    res.send('OK');
  } catch (e) { console.error('notify error', e.message); res.status(500).send('error'); }
});

// ── Simulated Tranzila hosted page (disabled once a real terminal is configured) ─
app.get('/api/dev/checkout', (req, res) => {
  if (process.env.TRANZILA_TERMINAL) return res.status(404).send('disabled');
  const { token, amount, email: buyer, ret } = req.query;
  const j = JSON.stringify;
  res.set('Content-Type', 'text/html; charset=utf-8').send(`<!doctype html><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>תשלום (סימולציה)</title>
<body style="font-family:system-ui,sans-serif;background:#0a1428;color:#fff;display:flex;min-height:100vh;align-items:center;justify-content:center;margin:0" dir=rtl>
<div style="background:#132447;border:1px solid #2a4a8a;border-radius:16px;padding:28px;max-width:320px;text-align:center">
<div style="font-size:12px;color:#7eb8f7;letter-spacing:1px">סימולציית תשלום · Tranzila</div>
<div style="font-size:30px;font-weight:900;margin:10px 0">₪${amount}</div>
<div style="font-size:12px;color:#aac4e8;margin-bottom:18px">${buyer || ''}</div>
<button id=pay style="width:100%;background:#f1c40f;color:#0a1428;border:0;border-radius:12px;padding:14px;font-size:15px;font-weight:900;cursor:pointer">שלם עכשיו</button>
<div id=s style="margin-top:12px;font-size:12px;color:#aac4e8"></div></div>
<script>document.getElementById('pay').onclick=async()=>{document.getElementById('s').textContent='מעבד…';
await fetch('/api/dev/pay?token='+encodeURIComponent(${j(token)}),{method:'POST'});
var r=${j(ret)};location.href=r+(r.indexOf('?')>-1?'&':'?')+'token='+encodeURIComponent(${j(token)});};</script></body>`);
});
app.post('/api/dev/pay', async (req, res) => {
  if (process.env.TRANZILA_TERMINAL) return res.status(404).send('disabled');
  const token = req.query.token;
  const r = await db.q('select id from purchases where token=$1', [token]);
  if (!r.rows.length) return res.status(404).send('no-order');
  await finalizeById(r.rows[0].id, 'SIM-' + Date.now());
  res.send('OK');
});

// ── Admin: reload content without redeploy ─────────────────────────────────────
app.post('/api/admin/reload', async (req, res) => {
  if (!process.env.ADMIN_TOKEN || req.header('x-admin') !== process.env.ADMIN_TOKEN) {
    return res.status(403).json({ ok: false });
  }
  await content.load(true);
  res.json({ ok: true, reloaded: true });
});

// Seed/refresh the Postgres `bank` table from the canonical data/l11.json (repo),
// running inside Railway so the internal DATABASE_URL works — no local DB access needed.
// Body: { nums?: number[] } to upsert only those; omitted = full import. Then reloads cache.
app.post('/api/admin/bank-import', async (req, res) => {
  if (!process.env.ADMIN_TOKEN || req.header('x-admin') !== process.env.ADMIN_TOKEN) {
    return res.status(403).json({ ok: false });
  }
  if (!db.hasDb()) return res.status(503).json({ ok: false, error: 'no DATABASE_URL' });
  try {
    const rows = await content.fetchCanonical();
    const only = Array.isArray(req.body && req.body.nums) ? new Set(req.body.nums.map(String)) : null;
    let n = 0;
    for (const q of rows) {
      if (q.num == null || (only && !only.has(String(q.num)))) continue;
      await db.q('insert into bank(num, data, updated_at) values ($1,$2,now()) on conflict(num) do update set data=$2, updated_at=now()', [q.num, q]);
      n++;
    }
    await content.load(true);
    res.json({ ok: true, imported: n });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

const PORT = process.env.PORT || 8080;
db.init()
  .then(() => settings.seed())
  .catch(e => console.error('DB init failed:', e.message))
  .finally(() => app.listen(PORT, () => console.log(`🚀 course API on :${PORT} (db=${db.hasDb()})`)));
