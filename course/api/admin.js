#!/usr/bin/env node
// Admin CLI — manage brand/price and coupons directly against the DB.
// Run from course/api (reads .env for DATABASE_URL). Examples:
//   node admin.js config get
//   node admin.js config set price_ils 129
//   node admin.js config set brand_name "השם החדש"
//   node admin.js coupon add MADRICH full 100 instructors 50   # code kind value [partner] [maxUses]
//   node admin.js coupon add LAUNCH20 percent 20 partner_ig
//   node admin.js coupon list
//   node admin.js coupon off LAUNCH20  |  coupon on LAUNCH20  |  coupon del LAUNCH20
//   node admin.js instructor add yossi@sail.co.il   # unique free code, 1 device only
//   node admin.js instructor list
//   node admin.js instructor revoke SK-XXXX-XXXX
require('./src/loadenv');
const db = require('./src/db');
const settings = require('./src/settings');
const codes = require('./src/codes');

async function main() {
  if (!db.hasDb()) { console.error('DATABASE_URL not set (check course/api/.env)'); process.exit(1); }
  await db.init();
  await settings.seed();
  const [group, cmd, ...a] = process.argv.slice(2);

  if (group === 'config' && cmd === 'get') {
    console.log(await settings.all());
  } else if (group === 'config' && cmd === 'set') {
    const [key, ...rest] = a;
    await settings.set(key, rest.join(' '));
    console.log('set', key, '=>', (await settings.all())[key]);
  } else if (group === 'coupon' && cmd === 'add') {
    const [code, kind = 'percent', value = '0', partner = null, maxUses = null] = a;
    await db.q(
      `insert into coupons(code, kind, value, partner_ref, max_uses) values ($1,$2,$3,$4,$5)
       on conflict(code) do update set kind=$2, value=$3, partner_ref=$4, max_uses=$5, active=true`,
      [code, kind, Number(value), partner, maxUses != null ? Number(maxUses) : null]
    );
    console.log(`coupon ${code} (${kind} ${value}${partner ? ', partner ' + partner : ''}${maxUses ? ', max ' + maxUses : ''}) ready`);
  } else if (group === 'coupon' && cmd === 'list') {
    const r = await db.q('select code, kind, value, partner_ref, active, uses, max_uses from coupons order by created_at');
    console.table(r.rows);
  } else if (group === 'coupon' && (cmd === 'off' || cmd === 'on')) {
    await db.q('update coupons set active=$2 where lower(code)=lower($1)', [a[0], cmd === 'on']);
    console.log(`coupon ${a[0]} -> active=${cmd === 'on'}`);
  } else if (group === 'coupon' && cmd === 'del') {
    await db.q('delete from coupons where lower(code)=lower($1)', [a[0]]);
    console.log(`coupon ${a[0]} deleted`);
  } else if (group === 'instructor' && cmd === 'add') {
    const email = a[0];
    if (!email) { console.error('usage: instructor add <email>'); process.exit(1); }
    const p = await db.q(
      "insert into purchases(email, amount_ils, partner_ref, status) values ($1, 0, 'instructor', 'comp') returning id",
      [email]
    );
    const code = await codes.issueCode(email, p.rows[0].id, 1); // device_limit = 1
    console.log(`instructor code for ${email}: ${code}  (1 device only)`);
  } else if (group === 'instructor' && cmd === 'list') {
    const r = await db.q(
      `select ac.code, ac.email, ac.device_limit, ac.revoked,
              (select count(*)::int from code_devices d where d.code=ac.code) as devices,
              ac.created_at
       from access_codes ac join purchases p on p.id=ac.purchase_id
       where p.status='comp' and p.partner_ref='instructor'
       order by ac.created_at`
    );
    console.table(r.rows);
  } else if (group === 'instructor' && cmd === 'revoke') {
    await db.q('update access_codes set revoked=true where code=$1', [a[0]]);
    console.log(`instructor code ${a[0]} revoked`);
  } else if (group === 'bank' && cmd === 'import') {
    const fs = require('fs'), path = require('path');
    const file = a[0] || path.join(__dirname, '..', '..', 'data', 'l11.json');
    const rows = JSON.parse(fs.readFileSync(file, 'utf8'));
    let n = 0;
    for (const q of rows) {
      if (q.num == null) continue;
      await db.q('insert into bank(num, data, updated_at) values ($1,$2,now()) on conflict(num) do update set data=$2, updated_at=now()', [q.num, q]);
      n++;
    }
    console.log(`bank: imported ${n} questions from ${file}`);
  } else if (group === 'bank' && cmd === 'count') {
    const r = await db.q('select count(*)::int n from bank');
    console.log('bank rows:', r.rows[0].n);
  } else {
    console.log('usage: config get | config set <key> <value>');
    console.log('       coupon add <code> <kind> <value> [partner] [maxUses] | coupon list | coupon on|off|del <code>');
    console.log('       instructor add <email> | instructor list | instructor revoke <code>');
    console.log('       bank import [file] | bank count');
  }
  process.exit(0);
}
main().catch(e => { console.error(e.message); process.exit(1); });
