// Delivers the access code to the buyer.
// Real send via nodemailer when SMTP_URL is set (e.g. smtp://user:pass@smtp.host:587);
// otherwise logs (simulation). Failures never throw — the code is already issued and shown in-app,
// so a mail hiccup must not break finalize.
const nodemailer = require('nodemailer');

let tx = null; // false = no SMTP configured; object = transport
function transport() {
  if (tx !== null) return tx;
  if (process.env.SMTP_URL) {
    tx = nodemailer.createTransport(process.env.SMTP_URL);
  } else if (process.env.SMTP_HOST) {
    // Discrete vars avoid URL-encoding the "@" in a Gmail username.
    const port = Number(process.env.SMTP_PORT || 587);
    tx = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port,
      secure: process.env.SMTP_SECURE ? process.env.SMTP_SECURE === 'true' : port === 465,
      auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
    });
  } else {
    tx = false;
  }
  return tx;
}

async function sendCode(email, code) {
  const t = transport();
  if (!t) {
    console.error(`✉️  [sim] access code ${code} → ${email}`);
    return { sent: true, sim: true };
  }
  const from = process.env.MAIL_FROM || 'אלכס ארגוב · תיאוריה בשיט <no-reply@alargov.com>';
  const appUrl = (process.env.APP_URL || 'https://app.alargov.com').replace(/\/$/, '');
  const subject = 'קוד הגישה שלך · קורס תיאוריה לאופנוע ים';
  const text = [
    'תודה על הרכישה!',
    '',
    `קוד הגישה שלך: ${code}`,
    '',
    `כניסה לקורס: ${appUrl}`,
    'הזן את הקוד באפליקציה כדי לפתוח את כל התוכן.',
    '',
    'בהצלחה במבחן,',
    'אלכס ארגוב',
  ].join('\n');
  const html = `<div dir="rtl" style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.7;color:#0a1428">
  <p>תודה על הרכישה!</p>
  <p>קוד הגישה שלך:</p>
  <p style="font-size:26px;font-weight:900;letter-spacing:3px;margin:6px 0 18px">${code}</p>
  <p><a href="${appUrl}" style="background:#f3c24c;color:#20160a;padding:11px 20px;border-radius:11px;text-decoration:none;font-weight:800;display:inline-block">כניסה לקורס</a></p>
  <p style="color:#445">הזן את הקוד באפליקציה כדי לפתוח את כל התוכן.</p>
  <p style="margin-top:20px">בהצלחה במבחן,<br>אלכס ארגוב</p>
</div>`;
  try {
    await t.sendMail({ from, to: email, subject, text, html });
    console.error(`✉️  sent access code → ${email}`);
    return { sent: true, sim: false };
  } catch (e) {
    console.error(`✉️  send FAILED → ${email}: ${e.message}`);
    return { sent: false, sim: false, error: e.message };
  }
}

module.exports = { sendCode };
