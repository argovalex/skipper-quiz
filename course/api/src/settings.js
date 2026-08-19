// Editable app config (brand name, product title, price). Lives in the DB so it
// changes without a redeploy. Falls back to env defaults when no DB.
const db = require('./db');

const DEFAULTS = {
  brand_name: process.env.BRAND_NAME || 'לומדה',            // גנרי, פלטפורמה לכמה מבחני תאוריה. שנה ב-admin.
  product_title: process.env.PRODUCT_TITLE || 'רשיון אופנוע ים',
  price_ils: String(process.env.PRICE_ILS || '199'),        // legacy/base. המחיר האפקטיבי מגיע מ-pricing().
  price_founders: String(process.env.PRICE_FOUNDERS || '199'), // מחיר מייסדים
  price_regular: String(process.env.PRICE_REGULAR || '349'),   // אחרי שהמקומות נגמרו
  founders_slots: String(process.env.FOUNDERS_SLOTS || '10'),  // כמה מקומות מייסדים
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

// Founders pricing: first N paid buyers get the founders price, then it rises to
// the regular price. The effective price is computed from how many paid purchases
// already exist (comp/instructor redemptions don't consume a seat).
async function pricing() {
  const s = await all();
  const num = (v, d) => Number(v != null ? v : d);
  const price_founders = num(s.price_founders, DEFAULTS.price_founders);
  const price_regular = num(s.price_regular, DEFAULTS.price_regular);
  const founders_slots = num(s.founders_slots, DEFAULTS.founders_slots);
  let founders_taken = 0;
  if (db.hasDb()) {
    const r = await db.q("select count(*)::int as n from purchases where status='paid'");
    founders_taken = r.rows[0].n;
  }
  const founders_left = Math.max(0, founders_slots - founders_taken);
  const is_founders = founders_left > 0;
  const price = is_founders ? price_founders : price_regular;
  return { price, is_founders, price_founders, price_regular, founders_slots, founders_taken, founders_left };
}

async function set(key, value) {
  if (!db.hasDb()) throw new Error('no-db');
  await db.q(
    `insert into settings(key, value, updated_at) values ($1,$2,now())
     on conflict(key) do update set value=$2, updated_at=now()`,
    [key, String(value)]
  );
}

module.exports = { seed, all, set, pricing, DEFAULTS };
