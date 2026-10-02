#!/usr/bin/env node
// מכסת תווים ב-ElevenLabs (נוצל/מגבלה/איפוס) — לתכנון אצוות קריינות.
//   node tools/voice/el-quota.js
'use strict';
const fs = require('fs');
const path = require('path');
const env = fs.readFileSync(path.resolve(__dirname, '..', '..', '.env'), 'utf8');
const key = (env.match(/^\s*ELEVENLABS_API_KEY\s*=\s*(.+?)\s*$/m) || [])[1];
fetch('https://api.elevenlabs.io/v1/user/subscription', { headers: { 'xi-api-key': key } })
  .then(r => r.json())
  .then(s => console.log(JSON.stringify({
    tier: s.tier, used: s.character_count, limit: s.character_limit,
    left: s.character_limit - s.character_count,
    resets: s.next_character_count_reset_unix && new Date(s.next_character_count_reset_unix * 1000).toISOString(),
    overage: s.can_extend_character_limit, status: s.status,
  })));
