// Higgsfield API example (official SDK, server-side only). Run from repo root:
//   node --env-file=.env.local tools/higgsfield/index.mjs
// .env.local (git-ignored) must hold: HF_CREDENTIALS=<key-id>:<key-secret>
// This makes a billable generation request.
import { config, higgsfield } from '@higgsfield/client/v2';

if (!process.env.HF_CREDENTIALS) {
  console.error('HF_CREDENTIALS is not set. Add it to .env.local as key-id:key-secret.');
  process.exit(1);
}
config({ credentials: process.env.HF_CREDENTIALS });

try {
  const result = await higgsfield.subscribe('bytedance/seedance-2.5/text-to-video', {
    input: {
      prompt: 'A cinematic scene at sunset',
      duration: 5,
      resolution: '720p',
      aspect_ratio: '16:9',
    },
    withPolling: true,
  });
  if (result.status === 'completed' && result.video?.url) {
    console.log('video url:', result.video.url);
  } else {
    console.error(`not completed (status: ${result.status})`, result.status === 'nsfw' ? 'blocked by moderation' : '');
    process.exit(2);
  }
} catch (e) {
  console.error('request failed:', e?.message || e);
  process.exit(3);
}
