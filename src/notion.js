require('dotenv').config();
const { Client } = require('@notionhq/client');

const notion = new Client({ auth: process.env.NOTION_TOKEN });
const DB_ID = process.env.NOTION_DATABASE_ID;

async function saveDraft(question, formatted, source = 'auto') {
  const page = await notion.pages.create({
    parent: { database_id: DB_ID },
    properties: {
      Name: {
        title: [{ text: { content: question.question_he.substring(0, 80) } }],
      },
      Status: {
        select: { name: 'pending' },
      },
      Source: {
        select: { name: source }, // 'auto' | 'url'
      },
      Topic: {
        rich_text: [{ text: { content: question.topic } }],
      },
      Difficulty: {
        select: { name: question.difficulty },
      },
      PostHebrew: {
        rich_text: [{ text: { content: formatted.hebrew } }],
      },
      PostEnglish: {
        rich_text: [{ text: { content: formatted.english } }],
      },
      AnswerComment: {
        rich_text: [{ text: { content: formatted.answer_comment } }],
      },
      ScheduledDate: {
        date: { start: new Date(Date.now() + 86400000).toISOString().split('T')[0] },
      },
    },
  });
  return page.id;
}

async function getApprovedPosts() {
  const today = new Date().toISOString().split('T')[0];
  const res = await notion.databases.query({
    database_id: DB_ID,
    filter: {
      and: [
        { property: 'Status', select: { equals: 'approved' } },
        { property: 'ScheduledDate', date: { equals: today } },
      ],
    },
  });
  return res.results;
}

async function markPublished(pageId) {
  await notion.pages.update({
    page_id: pageId,
    properties: {
      Status: { select: { name: 'published' } },
    },
  });
}

function extractText(page, field) {
  const prop = page.properties[field];
  if (!prop) return '';
  if (prop.rich_text) return prop.rich_text.map((r) => r.plain_text).join('');
  if (prop.title) return prop.title.map((r) => r.plain_text).join('');
  return '';
}

module.exports = { saveDraft, getApprovedPosts, markPublished, extractText };
