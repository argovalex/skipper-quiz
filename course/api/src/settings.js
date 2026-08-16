// Editable app config (brand name, product title, price). Lives in the DB so it
// changes without a redeploy. Falls back to env defaults when no DB.
const db = require('./db');

const DEFAULTS = {
  brand_name: process.env.BRAND_NAME || 'לומדה',            // גנרי, פלטפורמה לכמה מבחני תאוריה. שנה ב-admin.
  product_title: process.env.PRODUCT_TITLE || 'רשיון אופנוע ים',
  price_ils: String(process.env.PRICE_ILS || '99'),
};

async function seed() {
  if (!db.hasDb()) return;
  for (const [k, v] of Object.entries(DEFAULTS)) {
    await db.q('insert into settings(key, value) values ($1,$2) on conflict(key) do nothing', [k, String(v)]);
  }
}

async function all() {
  const o = { ...DEFAULTS };
  if (db.hasDb()) {
    const r = await db.q('select key, value from settings');
    for (const row of r.rows) o[row.key] = row.value;
  }
  o.price_ils = Number(o.price_ils);
  return o;
}

async function set(key, value) {
  if (!db.hasDb()) throw new Error('no-db');
  await db.q(
    `insert into settings(key, value, updated_at) values ($1,$2,now())
     on conflict(key) do update set value=$2, updated_at=now()`,
    [key, String(value)]
  );
}

module.exports = { seed, all, set, DEFAULTS };
