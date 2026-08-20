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

// Run fn inside a transaction with its own client. Used where a read-then-write
// must be atomic (e.g. claiming a device slot against device_limit).
async function tx(fn) {
  if (!pool) throw new Error('DATABASE_URL not set');
  const client = await pool.connect();
  try {
    await client.query('begin');
    const r = await fn(client);
    await client.query('commit');
    return r;
  } catch (e) {
    try { await client.query('rollback'); } catch (_) {}
    throw e;
  } finally {
    client.release();
  }
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

module.exports = { hasDb, q, tx, init };
