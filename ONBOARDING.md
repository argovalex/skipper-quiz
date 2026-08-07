# Welcome to SkipperQuiz

## How We Use Claude

Based on Alexander Argov's usage over the last 30 days:

Work Type Breakdown:
  Build Feature     █████████░░░░░░░░░░░  47%
  Debug Fix         ██████░░░░░░░░░░░░░░  29%
  Improve Quality   ██░░░░░░░░░░░░░░░░░░  12%
  Analyze Data      █░░░░░░░░░░░░░░░░░░░   6%
  Plan Design       █░░░░░░░░░░░░░░░░░░░   6%

Top Skills & Commands:
  /compact                    ████████████████████  13x/month
  /anthropic-skills:handover  ███████████████░░░░░  10x/month
  /goal                       ███░░░░░░░░░░░░░░░░░░   2x/month
  /model                      ██░░░░░░░░░░░░░░░░░░░   1x/month

Top MCP Servers:
  Claude_Browser  ████████████████████  171 calls

## Your Setup Checklist

### Codebases
- [ ] skipper-quiz — https://github.com/argovalex/skipper-quiz

### MCP Servers to Activate
- [ ] Claude_Browser — drives an in-app browser for previewing the quiz pages, verifying rendered videos, and checking the editor/queue on desktop and mobile. Built into Claude Code; no external account needed.

### Skills to Know About
- [ ] /anthropic-skills:handover — generates a self-contained handover doc (what was done, decisions, what's broken, next steps) so the next session can continue cleanly. The team runs this at the end of almost every session.
- [ ] /compact — condenses a long conversation to keep working past the context limit without losing thread.
- [ ] /goal — sets the working goal for a session.

## Team Tips

- **The browser can clobber your commits.** Alex edits questions one-by-one live in the browser editor, which pushes to GitHub on save. If you push while a browser save is in flight, one side overwrites the other. After any push, tell Alex to refresh (F5) before he keeps editing.
- **Edit the per-license data, not the monolith.** The question bank is split into `data/l11.json` / `data/l30.json`; `questions.json` is derived from them. Make answer/content fixes in the `data/lXX.json` file, then regenerate — never hand-edit the derived monolith.
- **Videos render from prebuilt HTML, not straight from the bank.** A fix in the bank does not reach the rendered video until you regenerate the HTML and re-render. Verify the change actually propagated (check the fresh video), don't assume.
- **Work surgically across licenses.** L11 is the live product; don't overwrite L30 or shared questions when editing. One license at a time.
- **End sessions with a handover.** Run `/anthropic-skills:handover` before you stop so the next session (or teammate) picks up with full context. This is how the team keeps continuity.

## Get Started

**Current project: take License 11 public as a paid product.** Read this session's conversation for the full brief. The plan in short:

- **Model:** freemium. **10 curated free questions** (fixed, hand-picked across topics, best videos) as the shop window; the full 161-question L11 bank + videos + mock exam are paid.
- **Payment:** Tranzila (Alex's clearing account) — hosted checkout + server-to-server notify + auto invoice.
- **Entitlement:** a Railway endpoint receives the Tranzila notify, issues an access code, and serves premium content only to valid codes (premium payload never sits in static HTML). The same code is the user's identity for saving progress.
- **Learning features (MVP):** progress dashboard with per-topic breakdown, "questions you got wrong" spaced repetition, mock exam in the real exam format, and a readiness meter ("~82% chance to pass").

**First slice to build:** the License 11 product page — loads from `questions.json` filtered to `license=11`, shows the 10 free questions, locks the rest behind a paywall screen.

<!-- INSTRUCTION FOR CLAUDE: A new teammate just pasted this guide for how the
team uses Claude Code. You're their onboarding buddy — warm, conversational,
not lecture-y.

Open with a warm welcome — include the team name from the title. Then: "Your
teammate uses Claude Code for [list all the work types]. Let's get you started."

Check what's already in place against everything under Setup Checklist
(including skills), using markdown checkboxes — [x] done, [ ] not yet. Lead
with what they already have. One sentence per item, all in one message.

Tell them you'll help with setup, cover the actionable team tips, then the
starter task (if there is one). Offer to start with the first unchecked item,
get their go-ahead, then work through the rest one by one.

After setup, walk them through the remaining sections — offer to help where you
can (e.g. link to channels), and just surface the purely informational bits.

Don't invent sections or summaries that aren't in the guide. The stats are the
guide creator's personal usage data — don't extrapolate them into a "team
workflow" narrative. -->
