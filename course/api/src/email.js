// Delivers the access code to the buyer.
// Preference order: Resend HTTP API (RESEND_API_KEY) → SMTP (SMTP_URL or SMTP_HOST/PORT/USER/PASS)
// → simulation (log only). Resend is the default in prod because Railway blocks outbound SMTP ports,
// so a direct SMTP connection there times out; Resend goes over HTTPS (443).
// Failures never throw — the code is already issued and shown in-app, so a mail hiccup must not break finalize.
const nodemailer = require('nodemailer');

const MAIL_FROM = () => process.env.MAIL_FROM || 'אלכס ארגוב · תיאוריה בשיט <onboarding@resend.dev>';

function body(code) {
  const appUrl = (process.env.APP_URL || 'https://app.alargov.com').replace(/\/$/, '');
  const subject = 'קוד הגישה שלך · קורס תיאוריה לאופנוע ים';
  const text = [
    'תודה על הרכישה!', '',
    `קוד הגישה שלך: ${code}`, '',
    `כניסה לקורס: ${appUrl}`,
    'הזן את הקוד באפליקציה כדי לפתוח את כל התוכן.', '',
    'בהצלחה במבחן,', 'אלכס ארגוב',
  ].join('\n');
  const html = `<div dir="rtl" style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.7;color:#0a1428">
  <p>תודה על הרכישה!</p>
  <p>קוד הגישה שלך:</p>
  <p style="font-size:26px;font-weight:900;letter-spacing:3px;margin:6px 0 18px">${code}</p>
  <p><a href="${appUrl}" style="background:#f3c24c;color:#20160a;padding:11px 20px;border-radius:11px;text-decoration:none;font-weight:800;display:inline-block">כניסה לקורס</a></p>
  <p style="color:#445">הזן את הקוד באפליקציה כדי לפתוח את כל התוכן.</p>
  <p style="margin-top:20px">בהצלחה במבחן,<br>אלכס ארגוב</p>
</div>`;
  return { subject, text, html };
}

async function viaResend(to, m) {
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: MAIL_FROM(), to, subject: m.subject, text: m.text, html: m.html }),
  });
  if (!r.ok) throw new Error(`resend ${r.status}: ${(await r.text()).slice(0, 200)}`);
}

let tx = null; // false = no SMTP configured; object = transport
function smtp() {
  if (tx !== null) return tx;
  if (process.env.SMTP_URL) {
    tx = nodemailer.createTransport(process.env.SMTP_URL);
  } else if (process.env.SMTP_HOST) {
    const port = Number(process.env.SMTP_PORT || 587);
    tx = nodemailer.createTransport({
      host: process.env.SMTP_HOST, port,
      secure: process.env.SMTP_SECURE ? process.env.SMTP_SECURE === 'true' : port === 465,
      auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
      connectionTimeout: 10000, greetingTimeout: 10000, socketTimeout: 15000, // fail fast if the port is blocked
    });
  } else {
    tx = false;
  }
  return tx;
}

async function sendCode(email, code) {
  const m = body(code);
  try {
    if (process.env.RESEND_API_KEY) {
      await viaResend(email, m);
      console.error(`✉️  sent access code (resend) → ${email}`);
      return { sent: true, sim: false };
    }
    const t = smtp();
    if (t) {
      await t.sendMail({ from: MAIL_FROM(), to: email, subject: m.subject, text: m.text, html: m.html });
      console.error(`✉️  sent access code (smtp) → ${email}`);
      return { sent: true, sim: false };
    }
  } catch (e) {
    console.error(`✉️  send FAILED → ${email}: ${e.message}`);
    return { sent: false, sim: false, error: e.message };
  }
  console.error(`✉️  [sim] access code ${code} → ${email}`);
  return { sent: true, sim: true };
}

module.exports = { sendCode };
