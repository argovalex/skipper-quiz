require('dotenv').config();
const Anthropic = require('@anthropic-ai/sdk');

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

const HAIKU = 'claude-haiku-4-5-20251001';
// Cloudflare Workers AI free tier: 10K Neurons/day shared. Cheapest first.
const CF_MODELS = ['@cf/openai/gpt-oss-120b', '@cf/google/gemma-4-26b-a4b-it'];

async function viaCloudflare(model, prompt, maxTokens) {
  const id = process.env.CF_ACCOUNT_ID || process.env.R2_ACCOUNT_ID;
  const res = await fetch(
    `https://api.cloudflare.com/client/v4/accounts/${id}/ai/run/${model}`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${process.env.CF_API_TOKEN}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: [{ role: 'user', content: prompt }],
        max_tokens: maxTokens * 4, // reasoning models spend part of the budget thinking
      }),
    }
  );
  const data = await res.json();
  if (!res.ok || data.success === false) {
    throw new Error(`Cloudflare ${model} ${res.status}: ${JSON.stringify(data.errors || data).slice(0, 200)}`);
  }
  const r = data.result || {};
  const text = r.response ?? r.choices?.[0]?.message?.content;
  if (!text) throw new Error(`Cloudflare ${model}: empty response`);
  return text;
}

// Haiku first; on any failure (credit exhausted, rate limit, outage) fall back to Cloudflare.
async function complete(prompt, maxTokens = 1000) {
  try {
    const response = await client.messages.create({
      model: HAIKU,
      max_tokens: maxTokens,
      messages: [{ role: 'user', content: prompt }],
    });
    return response.content[0].text;
  } catch (err) {
    if (!process.env.CF_API_TOKEN) throw err;
    console.warn(`[llm] Anthropic failed (${err.status || err.message}), falling back to Cloudflare`);
  }
  let lastErr;
  for (const model of CF_MODELS) {
    try {
      const text = await viaCloudflare(model, prompt, maxTokens);
      console.warn(`[llm] answered by ${model}`);
      return text;
    } catch (err) {
      lastErr = err;
    }
  }
  throw lastErr;
}

module.exports = { complete };
