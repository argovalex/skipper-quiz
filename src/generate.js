require('dotenv').config();
const Anthropic = require('@anthropic-ai/sdk');

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

const TOPICS = [
  'COLREGs - כללי מניעת התנגשויות בים',
  'ניווט אסטרונומי',
  'מטאורולוגיה ימית',
  'ציוד בטיחות על הסירה',
  'קריאת מפות ימיות',
  'אותות ימיים ודגלים',
  'ניהול סירה בים סוער',
  'קשרים ימיים',
  'מנוע וטכניקת נהיגה',
  'חוק הים הבינלאומי',
];

async function generateQuestion() {
  const topic = TOPICS[Math.floor(Math.random() * TOPICS.length)];

  const response = await client.messages.create({
    model: 'claude-opus-4-6',
    max_tokens: 1000,
    messages: [
      {
        role: 'user',
        content: `צור שאלת מבחן סקיפר בנושא: "${topic}"

פורמט מדויק (JSON בלבד, ללא markdown):
{
  "topic": "${topic}",
  "question_he": "השאלה בעברית",
  "question_en": "The question in English",
  "options_he": ["א. ...", "ב. ...", "ג. ...", "ד. ..."],
  "options_en": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "correct_index": 0,
  "explanation_he": "הסבר קצר מדוע התשובה נכונה",
  "explanation_en": "Short explanation why the answer is correct",
  "difficulty": "easy|medium|hard"
}

דרישות:
- שאלה מקצועית ברמת מבחן סקיפר ישראלי
- 4 תשובות, רק אחת נכונה
- correct_index הוא 0-3
- הסבר מקצועי וקצר`,
      },
    ],
  });

  const text = response.content[0].text.trim();
  const json = text.replace(/```json|```/g, '').trim();
  return JSON.parse(json);
}

function formatFacebookPost(q) {
  const optionsHe = q.options_he.join('\n');
  const optionsEn = q.options_en.join('\n');

  return {
    hebrew: `⚓ מבחן הסקיפר היומי

📚 נושא: ${q.topic}

❓ ${q.question_he}

${optionsHe}

💡 התשובה תפורסם מחר!
#מבחןסקיפר #ימאות #ניווט #sailing`,

    english: `⚓ Daily Skipper Quiz

📚 Topic: ${q.topic}

❓ ${q.question_en}

${optionsEn}

💡 Answer revealed tomorrow!
#SkipperExam #Sailing #Navigation #COLREGs`,

    answer_comment: `✅ תשובה: ${q.options_he[q.correct_index]}

${q.explanation_he}

✅ Answer: ${q.options_en[q.correct_index]}
${q.explanation_en}`,
  };
}

module.exports = { generateQuestion, formatFacebookPost };
