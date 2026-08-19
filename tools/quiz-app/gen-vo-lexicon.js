#!/usr/bin/env node
// Generates tools/quiz-app/vo-lexicon.js from the canonical niqqud lexicon
// (references/niqqud-lexicon.md, "## מילים" table) so the bank editor's "מילון"
// button can apply Alex's own vocalisations client-side (works from GitHub Pages,
// no server round-trip). Single source of truth: edit the .md (via
// tools/add-niqqud.py) and re-run this script; never hand-edit vo-lexicon.js.
//
//   node tools/quiz-app/gen-vo-lexicon.js
//
// Short 1-2 letter plain forms (אי/אם/אף/בי/אן/עד/פה) are SKIPPED: they collide
// with common Hebrew words ("אם"=if) and flag-letter renderings, so a blind
// whole-word replace would create many false positives. Only 3+ Hebrew-letter
// forms are emitted. Mirrors load_lexicon() in tools/lesson/niqqud.py.
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const LEXICON = path.join(ROOT, 'references', 'niqqud-lexicon.md');
const OUT = path.join(ROOT, 'tools', 'quiz-app', 'vo-lexicon.js');
const MARK = /[֑-ׇ]/;                 // niqqud / cantillation
const heLetters = s => (s.match(/[א-ת]/g) || []).length;

const md = fs.readFileSync(LEXICON, 'utf8');
const lines = md.split(/\r?\n/);
let inWords = false;
const seen = new Set();
const pairs = [];
for (const raw of lines) {
  const s = raw.replace(/\s+$/, '');
  if (s.startsWith('## ')) { inWords = s.trim() === '## מילים'; continue; }
  if (!inWords) continue;
  const m = s.match(/^\|(.+?)\|(.+?)\|\s*$/);
  if (!m) continue;
  let src = m[1].trim();
  const dst = m[2].trim();
  if (src === 'רגיל' || /^[-: ]+$/.test(src)) continue;   // header / separator
  src = src.split(' (')[0].trim();                        // drop "(hint)"
  if (!src || !dst) continue;
  if (!MARK.test(dst)) continue;                          // dst must be vocalised
  if (heLetters(src) < 3) continue;                       // skip collision-prone shorts
  if (seen.has(src)) continue;                            // first wins on dupes
  seen.add(src);
  pairs.push([src, dst]);
}
pairs.sort((a, b) => b[0].length - a[0].length);           // longest first

const body = pairs.map(([p, n]) => `  ${JSON.stringify([p, n])},`).join('\n');
const out = `// AUTO-GENERATED from references/niqqud-lexicon.md by
// tools/quiz-app/gen-vo-lexicon.js. Do NOT edit by hand — edit the .md and re-run.
// ${pairs.length} entries (3+ Hebrew-letter forms; short collision-prone words skipped).
const VO_LEXICON = [
${body}
];
if (typeof module !== 'undefined' && module.exports) module.exports = { VO_LEXICON };
`;
fs.writeFileSync(OUT, out, 'utf8');
console.log(`wrote ${OUT} with ${pairs.length} entries`);
