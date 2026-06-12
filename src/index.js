require('dotenv').config();
const cron = require('node-cron');
const { generateQuestion, formatFacebookPost } = require('./generate');
const { saveDraft, getApprovedPosts, markPublished, extractText } = require('./notion');
const { publishPost, publishComment } = require('./publish');

// ─── CRON 1: יצירת שאלה יומית ב-08:00 ─────────────────────────────────────
cron.schedule('0 8 * * *', async () => {
  console.log('[GENERATE] Starting daily question generation...');
  try {
    const question = await generateQuestion();
    const formatted = formatFacebookPost(question);
    const pageId = await saveDraft(question, formatted, 'auto');
    console.log(`[GENERATE] Saved to Notion: ${pageId}`);
  } catch (err) {
    console.error('[GENERATE] Error:', err.message);
  }
});

// ─── CRON 2: פרסום פוסטים מאושרים ב-10:00 ──────────────────────────────────
cron.schedule('0 10 * * *', async () => {
  console.log('[PUBLISH] Checking for approved posts...');
  try {
    const posts = await getApprovedPosts();
    console.log(`[PUBLISH] Found ${posts.length} approved post(s)`);

    for (const post of posts) {
      const hePost = extractText(post, 'PostHebrew');
      const enPost = extractText(post, 'PostEnglish');
      const answer = extractText(post, 'AnswerComment');

      const combinedPost = `${hePost}\n\n━━━━━━━━━━━━━━━\n\n${enPost}`;
      const postId = await publishPost(combinedPost);
      console.log(`[PUBLISH] Published post: ${postId}`);

      // פרסום תשובה של אתמול אם יש
      // (ניתן להרחיב עם lookback logic)

      await markPublished(post.id);
      console.log(`[PUBLISH] Marked as published in Notion`);
    }
  } catch (err) {
    console.error('[PUBLISH] Error:', err.message);
  }
});

console.log('⚓ Skipper Agent running. Cron jobs active: 08:00 generate, 10:00 publish');
