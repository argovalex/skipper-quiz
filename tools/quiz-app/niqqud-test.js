#!/usr/bin/env node
// niqqud-test.js — rules of the single niqqud engine (vo.js applyLexiconText).
//   node tools/quiz-app/niqqud-test.js
// Cases use lexicon entries; if Alex changes one of those forms, update the case.
'use strict';
const { applyLexiconText: L } = require('./vo.js');
let fail = 0;
function eq(name, got, want) {
  if (got === want) return;
  fail++; console.error(`✗ ${name}\n   got:  ${got}\n   want: ${want}`);
}
const has = (name, got, sub) => { if (!got.includes(sub)) { fail++; console.error(`✗ ${name}: "${sub}" missing in ${got}`); } };

// 1. existing niqqud is never overwritten (default and lesson)
eq('manual כְּלֵי kept', L('כְּלֵי שייט'), 'כְּלֵי שָייט');
eq('manual לָמָה kept', L('לָמָה לא', { mode: 'lesson' }), 'לָמָה לא');
eq('manual עֶשְׂרֵה kept', L('ארבע עֶשְׂרֵה', { mode: 'lesson' }), 'ארבע עֶשְׂרֵה');
// override (editor button only) re-sets the form
has('override re-sets', L('מָצוּף', { override: true }), 'מָצוֹף');
// 2. single pass: phrase entry wins, shorter entry does not re-vocalise inside it
eq('phrase entry', L('שלוש עשרה'), 'שלוש עֶשְׂרֵה');
// 3. shorts: allowlist only
eq('short allowlist', L('אם או עד פה'), 'אִם אוֹ עַד פּה');
eq('letter names untouched', L('די אי בת שם בי', { mode: 'lesson' }), 'די אי בת שם בי');
eq('אל not applied', L('אל תעקוף', { mode: 'lesson' }), 'אל תעקוף');
// 4. quiz-only homographs
eq('quiz skips למנוע', L('כדי למנוע התנגשות'), 'כדי למנוע התנגשות');
has('lesson keeps למנוע', L('מים למנוע', { mode: 'lesson' }), 'לָמָנוע');
// whole-word only
eq('no partial match', L('מצופהו'), 'מצופהו');

if (fail) { console.error(`${fail} failed`); process.exit(1); }
console.log('✓ niqqud engine: all cases pass');
