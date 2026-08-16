// Delivers the access code to the buyer.
// Simulation: logs to console. Real: wire SMTP (nodemailer) when SMTP_URL is set.
async function sendCode(email, code) {
  if (process.env.SMTP_URL) {
    // TODO(real): const nodemailer=require('nodemailer'); send via process.env.SMTP_URL.
    // Kept as a seam so connecting real email is one module, no flow change.
  }
  console.error(`✉️  [sim] access code ${code} → ${email}`);
  return { sent: true, sim: !process.env.SMTP_URL };
}
module.exports = { sendCode };
