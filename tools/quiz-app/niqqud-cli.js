#!/usr/bin/env node
// niqqud-cli.js — the vo.js niqqud engine for non-JS callers (tools/lesson/niqqud.py).
// Reads UTF-8 text on stdin, writes it vocalised to stdout.
//   node tools/quiz-app/niqqud-cli.js [--mode quiz|lesson] [--override]
'use strict';
const { applyLexiconText } = require('./vo.js');
const args = process.argv.slice(2);
const mi = args.indexOf('--mode');
const mode = mi !== -1 ? args[mi + 1] : 'lesson';
const override = args.includes('--override');
const chunks = [];
process.stdin.on('data', c => chunks.push(c));
process.stdin.on('end', () => {
  process.stdout.write(applyLexiconText(Buffer.concat(chunks).toString('utf8'), { mode, override }));
});
