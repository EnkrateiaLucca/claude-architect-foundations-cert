# Claude Certified Architect – Foundations (CCAR-F): Exam Prep

Course materials for the O'Reilly live training *Claude Certified Architect – Foundations Exam Prep*. The official [Exam Guide v1.0](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542750%2FClaude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf) is the compass for everything here.

> **Status:** the slide deck covers CCAR-F. The other folders still hold the Professional (CCAR-P) materials this repo was cloned from and will be rewritten for Foundations.

## What's inside

| Path | What it is |
|---|---|
| `study-guide.html` | The whole course on one page: blueprint, domain lessons, all 60 practice questions, exercises, strategy, quick reference, and resources. Open in a browser. |
| `exam-guide.html` | Interactive companion to the official exam guide: blueprint self-assessment, official sample questions, and exam policies |
| `presentation/claude-architect-foundations-exam-prep.html` | Live slide deck (remark.js). Open in a browser; press `P` for presenter notes. |
| `presentation/claude-architect-foundations-exam-prep.pdf` | PDF export of the slide deck |
| `lessons/` | One markdown lesson per exam domain, with verbatim objectives, decision tables, traps, and self-checks |
| `exercises/` | Eight hands-on exercises (design drills with reference answers) plus two runnable scripts in `exercises/scripts/` |
| `questions/practice-questions.md` | 60 original exam-style questions weighted by domain, with answers and distractor analysis |
| `questions/quiz.html` | The same 60 questions as a click-to-check quiz with a score tracker and domain filter |
| `questions/questions.json` | The question database (source of truth) |
| `anki/ccar-p-flashcards.apkg` | 60 Anki flashcards, tagged by domain. Import with **File → Import** |
| `anki/flashcards.csv` | Flashcard source (also importable into other tools) |
| `cheatsheet/ccar-p-cheatsheet.pdf` | Five-page printable cheatsheet of the whole course |
| `research/` | Sourced research notes behind the materials |
| `build.py` | Rebuilds the markdown bank, quiz, and Anki deck: `uv run build.py` |

## Schedule (120 min)

| Segment | Time | Exam domains |
|---|---|---|
| 1. The exam and agentic architecture | 30 min | Blueprint + D1 Agentic Architecture & Orchestration (27%) |
| 2. Tools, MCP, and Claude Code | 35 min | D2 Tool Design & MCP Integration (18%) + D3 Claude Code Configuration & Workflows (20%) |
| 3. Prompting, structured output, and context | 45 min | D4 Prompt Engineering & Structured Output (20%) + D5 Context Management & Reliability (15%) |
| 4. Exam strategy and study plan | 10 min | All |

## Exam at a glance

Exam code CCAR-F · 60 items · 4 scenarios drawn from a bank of 6 · 120 minutes · scaled score 720/1,000 to pass · $125 · Pearson VUE (online or test center) · valid 12 months, free on-time renewal. Registration currently requires a Claude Partner Network company email.

## Exercises

| # | Exercise | Domain |
|---|---|---|
| 00 | Walk the three official samples | All |
| 01 | Ownership, shape, pattern for five business problems | D1 |
| 02 | Break and fix prompt caching (`scripts/prompt_caching.py`) + context strategy | D2 |
| 03 | Integration design review: seven flaws | D3 |
| 04 | Eval plan + mixed-method harness (`scripts/eval_harness.py`) | D4 |
| 05 | Place the safety stack for a loan assistant | D5 |
| 06 | Discovery role-play + one-page ADR | D6 |
| 07 | Put each Claude Code setting at the right layer | D7 |

The scripts use [uv](https://docs.astral.sh/uv/) inline metadata and need `ANTHROPIC_API_KEY`. `uv run exercises/scripts/eval_harness.py --selftest` runs offline.

## Before the session

1. Clone this repo.
2. Read the official [Exam Guide v1.0](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542750%2FClaude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf), especially the 30 task statements (Section 6) and the four preparation exercises (Section 8).
3. Optional: the free [Foundations prep courses](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses) on the Partner Academy (Claude API, MCP, Claude Code in Action, and more).

The deck reproduces the twelve sample questions from the public exam guide. Platform facts were checked against the guide in October 2026 and will change.
