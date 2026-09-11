// Delivers the access code to the buyer over WhatsApp (in addition to email).
// Uses the Meta WhatsApp Cloud API over HTTPS (Railway does not block 443, unlike SMTP ports).
// Business-initiated messages require a pre-approved template, so we send a template message
// with the code as its single body variable ({{1}}).
//
// Config (Railway env on skipper-quiz):
//   WHATSAPP_TOKEN         permanent/system-user access token
//   WHATSAPP_PHONE_ID      the sender's Phone Number ID (NOT the phone number itself)
//   WHATSAPP_TEMPLATE      approved template name (default: access_code)
//   WHATSAPP_TEMPLATE_LANG template language code (default: he)
//   WHATSAPP_API_VERSION   graph API version (default: v21.0)
//
// Failures never throw — the code is already issued, shown in-app, and emailed; a WhatsApp
// hiccup must not break finalize. Missing phone or missing config → silent skip.

const GRAPH = 'https://graph.facebook.com';

// Normalize an Israeli mobile to E.164 digits without '+', as the Cloud API expects (e.g. 972501234567).
// Mirrors the client-side normPhone; returns '' for anything that is not a valid IL mobile.
function toWaNumber(phone) {
  if (!phone) return '';
  let d = String(phone).replace(/[^0-9+]/g, '');
  if (d.startsWith('+')) d = d.slice(1);
  if (d.startsWith('972')) d = d.slice(3);
  else if (d.startsWith('0')) d = d.slice(1);
  if (!/^5\d{8}$/.test(d)) return '';
  return '972' + d;
}

function configured() {
  return !!(process.env.WHATSAPP_TOKEN && process.env.WHATSAPP_PHONE_ID);
}

async function sendCode(phone, code) {
  const to = toWaNumber(phone);
  if (!to) { return { sent: false, skipped: 'no-phone' }; }
  if (!configured()) { console.error(`📱 [sim] wa code ${code} → ${to}`); return { sent: true, sim: true }; }
  const ver = process.env.WHATSAPP_API_VERSION || 'v21.0';
  const tmpl = process.env.WHATSAPP_TEMPLATE || 'access_code';
  const lang = process.env.WHATSAPP_TEMPLATE_LANG || 'he';
  const url = `${GRAPH}/${ver}/${process.env.WHATSAPP_PHONE_ID}/messages`;
  // WhatsApp only approves code-bearing templates under the Authentication category, whose
  // copy-code button accepts alphanumerics only. Strip the hyphens (SK-DXJB-33Y6 → SKDXJB33Y6);
  // the app's session.start canonicalizes it back, so the copied value still validates.
  // Auth templates require the OTP in BOTH the body and the URL/copy-code button component.
  const otp = String(code).replace(/-/g, '');
  const authTemplate = process.env.WHATSAPP_UTILITY !== '1'; // default: authentication-style
  const components = authTemplate
    ? [
        { type: 'body', parameters: [{ type: 'text', text: otp }] },
        { type: 'button', sub_type: 'url', index: '0', parameters: [{ type: 'text', text: otp }] },
      ]
    : [{ type: 'body', parameters: [{ type: 'text', text: String(code) }] }];
  const payload = {
    messaging_product: 'whatsapp',
    to,
    type: 'template',
    template: { name: tmpl, language: { code: lang }, components },
  };
  try {
    const r = await fetch(url, {
      method: 'POST',
      headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!r.ok) throw new Error(`wa ${r.status}: ${(await r.text()).slice(0, 200)}`);
    console.error(`📱 sent access code (whatsapp) → ${to}`);
    return { sent: true, sim: false };
  } catch (e) {
    console.error(`📱 wa send FAILED → ${to}: ${e.message}`);
    return { sent: false, error: e.message };
  }
}

module.exports = { sendCode, toWaNumber };
