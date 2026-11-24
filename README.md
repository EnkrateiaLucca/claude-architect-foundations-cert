# Claude Certified Architect – Foundations (CCAR-F): Exam Prep

Course materials for the O'Reilly live training *Claude Certified Architect – Foundations Exam Prep*. The official [Exam Guide v1.1](https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf) is the compass for everything here. Every lesson, question, flashcard, and exercise maps to its five domains and 30 task statements.

## What's inside

| Path | What it is |
|---|---|
| `study-guide.html` | The whole course on one page: exam overview, five domain lessons, all 60 practice questions, the exercises, and the study plan. Open in a browser. |
| `exam-guide.html` | Interactive companion to the official exam guide: blueprint self-assessment for all 30 task statements, the six scenarios, the 12 official sample questions, and exam policies |
| `presentation/claude-architect-foundations-exam-prep.html` | Live slide deck (remark.js). Open in a browser; press `P` for presenter notes. |
| `presentation/claude-architect-foundations-exam-prep.pdf` | PDF export of the slide deck |
| `lessons/` | One markdown lesson per exam domain (task statements, concepts, traps, self-checks), plus the blueprint (00) and exam strategy (06) |
| `exercises/` | The 12 official samples walked through (00), the four official preparation exercises as design drills with reference answers (01–04), two runnable scripts, and a sample team config |
| `questions/practice-questions.md` | 60 original scenario-based questions weighted by domain, with answers and distractor analysis |
| `questions/quiz.html` | The same 60 questions as a click-to-check quiz with a score tracker and domain filter |
| `questions/questions.json` | The question bank (source of truth) |
| `anki/ccar-f-flashcards.apkg` | 60 Anki flashcards, tagged by domain. Import with **File → Import** |
| `anki/flashcards.csv` | Flashcard source (also importable into other tools) |
| `cheatsheet/ccar-f-cheatsheet.pdf` | Five-page printable cheatsheet of the whole course |
| `research/` | Sourced research notes behind the materials, including where current Anthropic docs differ from the exam guide |
| `build.py` | Rebuilds the question bank pages, quiz, Anki deck, and study guide: `uv run build.py` |

## Schedule (120 min)

| Segment | Time | Exam domains |
|---|---|---|
| 1. The exam and agentic architecture | 30 min | Blueprint + D1 Agentic Architecture & Orchestration (27%) |
| 2. Tools, MCP, and Claude Code | 35 min | D2 Tool Design & MCP Integration (18%) + D3 Claude Code Configuration & Workflows (20%) |
| 3. Prompting, structured output, and context | 45 min | D4 Prompt Engineering & Structured Output (20%) + D5 Context Management & Reliability (15%) |
| 4. Exam strategy and study plan | 10 min | All |

## Exam at a glance

Exam code CCAR-F · 60 items · 4 scenarios drawn from a bank of 6 · 120 minutes · scaled score 720/1,000 to pass · $125 · Pearson VUE (online or test center) · valid 12 months, free on-time renewal. Registration currently requires a Claude Partner Network company email.

| Lesson | Domain | Weight | Practice questions |
|---|---|---|---|
| [00](lessons/00-exam-blueprint.md) | Exam blueprint, scenarios, scope, policies | | |
| [01](lessons/01-agentic-architecture-and-orchestration.md) | D1 Agentic Architecture & Orchestration | 27% | Q1–Q16 |
| [02](lessons/02-tool-design-and-mcp-integration.md) | D2 Tool Design & MCP Integration | 18% | Q17–Q27 |
| [03](lessons/03-claude-code-configuration-and-workflows.md) | D3 Claude Code Configuration & Workflows | 20% | Q28–Q39 |
| [04](lessons/04-prompt-engineering-and-structured-output.md) | D4 Prompt Engineering & Structured Output | 20% | Q40–Q51 |
| [05](lessons/05-context-management-and-reliability.md) | D5 Context Management & Reliability | 15% | Q52–Q60 |
| [06](lessons/06-exam-strategy-and-study-plan.md) | Exam strategy and study plan | | |

## Exercises

| # | Exercise | Domains |
|---|---|---|
| [00](exercises/00-official-samples.md) | Walk the 12 official sample questions | All |
| [01](exercises/01-multi-tool-agent.md) | Build a multi-tool agent with escalation logic (`scripts/support_agent.py`) | D1, D2, D5 |
| [02](exercises/02-team-claude-code-config.md) | Configure Claude Code for a team workflow (`team-config/`) | D3, D2 |
| [03](exercises/03-extraction-pipeline.md) | Build a structured data extraction pipeline (`scripts/extraction_pipeline.py`) | D4, D5 |
| [04](exercises/04-multi-agent-research-pipeline.md) | Design and debug a multi-agent research pipeline | D1, D2, D5 |

Exercises 01–04 follow the four preparation exercises in Section 8 of the exam guide. The scripts use [uv](https://docs.astral.sh/uv/) inline metadata. Run either one with `--selftest` to check it offline. Live mode needs `ANTHROPIC_API_KEY`:

```bash
uv run exercises/scripts/support_agent.py --selftest
uv run exercises/scripts/extraction_pipeline.py --selftest
```

## Exam guide vs current docs

The exam tests the exam guide. Some guide details lag the current Anthropic docs. For example, forced `tool_choice` returns an error on the newest models, and the Agent SDK's `Task` tool is now named `Agent`. The lessons teach the guide's answer and add a short "Docs note" where the docs differ. [`research/02-anthropic-docs-and-courses.md`](research/02-anthropic-docs-and-courses.md) lists every difference.

## Before the session

1. Clone this repo.
2. Read the official [Exam Guide](https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf), especially the 30 task statements (Section 6) and the four preparation exercises (Section 8).
3. Optional: the free [Foundations prep courses](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses) on the Partner Academy (Claude API, MCP, Claude Code in Action, and more).

The deck and `exercises/00-official-samples.md` reproduce the twelve sample questions from the public exam guide. All other questions and flashcards are original. Exam facts follow Exam Guide v1.1 (November 2026). Platform facts were checked against Anthropic's docs in November 2026 and will change.

## Rebuilding

Edit `questions/questions.json`, `anki/flashcards.csv`, `lessons/*.md`, or `exercises/*.md`, then run `uv run build.py`. The build checks the question bank (60 items, domain counts, task statements, answer keys) before it writes anything.
