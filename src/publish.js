require('dotenv').config();
const axios = require('axios');

const PAGE_ID = process.env.FB_PAGE_ID;
const TOKEN = process.env.FB_PAGE_ACCESS_TOKEN;
const BASE = `https://graph.facebook.com/v19.0`;

async function publishPost(message) {
  const res = await axios.post(`${BASE}/${PAGE_ID}/feed`, {
    message,
    access_token: TOKEN,
  });
  return res.data.id; // post_id
}

async function publishComment(postId, message) {
  const res = await axios.post(`${BASE}/${postId}/comments`, {
    message,
    access_token: TOKEN,
  });
  return res.data.id;
}

module.exports = { publishPost, publishComment };
