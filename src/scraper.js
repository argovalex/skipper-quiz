require('dotenv').config();
const axios = require('axios');
const cheerio = require('cheerio');
const Anthropic = require('@anthropic-ai/sdk');

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

async function scrapeUrl(url) {
  const res = await axios.get(url, {
    headers: {
      'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    },
    timeout: 15000,
  });
  const $ = cheerio.load(res.data);

  // Remove noise
  $('script, style, nav, footer, header, .ads, iframe').remove();

  // Extract meaningful text
  const title = $('title').text().trim();
  const h1 = $('h1').first().text().trim();
  const body = $('article, main, .post-content, .entry-content, body')
    .first()
    .text()
    .replace(/\s+/g, ' ')
    .trim()
    .substring(0, 3000);

  return { url, title, h1, body };
}

async function rewriteAsSkipperQuestion(scraped) {
  const response = await client.messages.create({
    model: 'claude-opus-4-6',
    max_tokens: 1000,
    messages: [
      {
        role: 'user',
        content: `תוכן מדף חיצוני:
URL: ${scraped.url}
כותרת: ${scraped.title}
${scraped.h1 ? `H1: ${scraped.h1}` : ''}
תוכן: ${scraped.body}

---
על בסיס התוכן הזה, צור שאלת מבחן סקיפר מקצועית.
אם התוכן אינו קשור לימאות/ניווט/COLREGs — חלץ את הנושא הטכני הרלוונטי ביותר.

פורמט JSON בלבד (ללא markdown):
{
  "topic": "נושא השאלה",
  "question_he": "השאלה בעברית",
  "question_en": "The question in English",
  "options_he": ["א. ...", "ב. ...", "ג. ...", "ד. ..."],
  "options_en": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "correct_index": 0,
  "explanation_he": "הסבר קצר",
  "explanation_en": "Short explanation",
  "difficulty": "easy|medium|hard",
  "source_url": "${scraped.url}"
}`,
      },
    ],
  });

  const text = response.content[0].text.trim();
  const json = text.replace(/```json|```/g, '').trim();
  return JSON.parse(json);
}

module.exports = { scrapeUrl, rewriteAsSkipperQuestion };
