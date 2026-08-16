// Postgres pool. Boots even without DATABASE_URL so file-backed endpoints work.
const fs = require('fs');
const path = require('path');

let pool = null;
if (process.env.DATABASE_URL) {
  const { Pool } = require('pg');
  pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: process.env.PGSSL === 'disable' ? false : { rejectUnauthorized: false },
  });
}

function hasDb() { return !!pool; }

async function q(text, params) {
  if (!pool) throw new Error('DATABASE_URL not set');
  return pool.query(text, params);
}

async function init() {
  if (!pool) {
    console.warn('⚠️  DATABASE_URL not set — codes/progress/coupons/notify disabled (503). File endpoints still work.');
    return;
  }
  const sql = fs.readFileSync(path.join(__dirname, '..', 'db', 'schema.sql'), 'utf8');
  await pool.query(sql);
  console.error('✅ DB schema ready');
}

module.exports = { hasDb, q, init };
