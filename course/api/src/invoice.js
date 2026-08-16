// Issues a tax invoice for a paid purchase.
// Simulation: logs. Real: wire an Israeli provider (Morning / Green Invoice) when
// INVOICE_API_KEY is set. Alex handles invoicing; this is the seam to automate it.
async function issue(order) {
  if (process.env.INVOICE_API_KEY) {
    // TODO(real): call provider API, return invoice id/url.
  }
  console.error(`🧾 [sim] invoice ₪${order.amount} → ${order.email}`);
  return { issued: true, sim: !process.env.INVOICE_API_KEY };
}
module.exports = { issue };
