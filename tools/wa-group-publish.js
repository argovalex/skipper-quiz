// wa-group-publish.js — sends the daily question (caption + video link) to a WhatsApp
// group via WhatsApp Business, using Baileys (unofficial multi-device "linked device"
// protocol — no browser, no official Cloud API, since Cloud API cannot post to groups).
//
// First run (one-time pairing):
//   node tools/wa-group-publish.js --pair
// Prints a QR in the terminal. Scan it from the phone: WhatsApp Business → הגדרות →
// מכשירים מקושרים → קישור מכשיר. Session is saved to tools/.wa-auth/ (gitignored) and
// reused on every later run — no QR after that, until the session is logged out.
//
// List groups (to find the target group's JID once):
//   node tools/wa-group-publish.js --list-groups
//
// Send (used by daily_publish.js):
//   node tools/wa-group-publish.js --send "<message text>"
// Reads the target group JID from WA_GROUP_JID in .env.
'use strict';
const fs = require('fs');
const path = require('path');
const {
  default: makeWASocket,
  useMultiFileAuthState,
  DisconnectReason,
  fetchLatestBaileysVersion,
} = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');

const ROOT = path.join(__dirname, '..');
const AUTH_DIR = path.join(__dirname, '.wa-auth');

function loadEnvFile() {
  const envPath = path.join(ROOT, '.env');
  if (!fs.existsSync(envPath)) return;
  for (const line of fs.readFileSync(envPath, 'utf8').split('\n')) {
    const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
    if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].trim();
  }
}
loadEnvFile();

async function connect({ interactive }) {
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  const { version } = await fetchLatestBaileysVersion();
  const sock = makeWASocket({
    auth: state,
    version,
    printQRInTerminal: false,
    browser: ['SkipperQuiz', 'Chrome', '1.0'],
  });
  sock.ev.on('creds.update', saveCreds);

  return new Promise((resolve, reject) => {
    sock.ev.on('connection.update', (update) => {
      const { connection, lastDisconnect, qr } = update;
      if (qr && interactive) {
        console.log('\n[wa] סרוק את הקוד עם WhatsApp Business → מכשירים מקושרים:\n');
        qrcode.generate(qr, { small: true });
      }
      if (connection === 'open') resolve(sock);
      if (connection === 'close') {
        const code = lastDisconnect?.error?.output?.statusCode;
        const loggedOut = code === DisconnectReason.loggedOut;
        if (loggedOut) {
          reject(new Error('[wa] session logged out — מחק tools/.wa-auth/ והרץ --pair מחדש'));
        } else {
          reject(new Error(`[wa] connection closed (code ${code || 'unknown'}) — הרץ שוב`));
        }
      }
    });
  });
}

async function listGroups() {
  const sock = await connect({ interactive: true });
  const groups = await sock.groupFetchAllParticipating();
  console.log('\n[wa] קבוצות:');
  for (const g of Object.values(groups)) {
    console.log(`  ${g.subject}  →  ${g.id}`);
  }
  console.log('\nהעתק את ה-JID הרצוי ל-.env כ- WA_GROUP_JID=<jid>');
  await sock.end();
  process.exit(0);
}

async function sendMessage(text) {
  const jid = process.env.WA_GROUP_JID;
  if (!jid) throw new Error('WA_GROUP_JID לא מוגדר ב-.env — הרץ --list-groups כדי למצוא את ה-JID');
  const sock = await connect({ interactive: false });
  await sock.sendMessage(jid, { text });
  console.log(`[wa] נשלח לקבוצה ${jid}`);
  await sock.end();
}

async function main() {
  const args = process.argv.slice(2);
  if (args.includes('--pair')) {
    await connect({ interactive: true });
    console.log('[wa] מחובר. הסשן נשמר ב-tools/.wa-auth/.');
    process.exit(0);
  } else if (args.includes('--list-groups')) {
    await listGroups();
  } else if (args.includes('--send')) {
    const idx = args.indexOf('--send');
    const text = args[idx + 1];
    if (!text) throw new Error('--send דורש טקסט הודעה');
    await sendMessage(text);
    process.exit(0);
  } else {
    console.log('שימוש: --pair | --list-groups | --send "<טקסט>"');
    process.exit(1);
  }
}

module.exports = { sendMessage };

if (require.main === module) {
  main().catch((e) => {
    console.error('[wa] FAILED:', e.message);
    process.exit(1);
  });
}
