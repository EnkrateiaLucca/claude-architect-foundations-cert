# Community Resources for CCAR-F (all unofficial)

Research date: 2026-11-24.

## Context

Many unofficial CCAR-F study repos exist on GitHub. This file records what the most-used ones contain, which guide version they follow, where they disagree with the official guide or current docs, and what this course can and cannot reuse. Nothing here is official. The certification policies forbid sharing exam questions "in any form, including in study groups and online forums", so treat any repo that claims real exam items with caution. [source: https://anthropic-partners.skilljar.com/page/policies-certifications]

Label conventions: `[source: url]` marks a fetched and read source. `[inferred]` marks my own analysis. `[unverified]` marks a claim I could not confirm.

### Source key

| Alias | What it is | URL |
|---|---|---|
| `REPO` | paullarionov repo. Paths like `guide_en.md §3.1` refer to it (shallow clone at `11e53a7`, 2026-10-02; still the latest push on 2026-11-24) | https://github.com/paullarionov/claude-certified-architect |
| `OG-F-v0.1` | Official Foundations guide "Version 0.1" (March 2026 launch file) | https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F8lsy243ftffjjy1cx9lm3o2bw%2Fpublic%2F1773274827%2FClaude+Certified+Architect+%E2%80%93+Foundations+Certification+Exam+Guide.pdf |
| `OG-F-v1.0` | Official guide v1.0, effective July 2026 | https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542750%2FClaude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf |
| `OG-F-v1.1` | Official guide v1.1, effective November 2026 (exam content identical to v1.0) | https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf |

Discovery: `gh search repos "claude certified architect"` and `gh search repos "CCAR-F"` on 2026-11-24, then `gh api repos/<repo>` and the README of each repo below.

## The dominant repo: paullarionov/claude-certified-architect

### 1. At a glance
- 5,316 stars, 1,261 forks, created 2026-03-14, last push 2026-10-02. [source: https://api.github.com/repos/paullarionov/claude-certified-architect]
- One study guide in 15 languages (`guide_<lang>.md`, ~3,400 lines in English), PDF and EPUB builds, an HTML practice test in 8 languages, and Anki decks in 8 languages. [source: REPO README.md, file tree]
- The English guide has Part I "Theory Foundations" (13 chapters by technology) and Part II "Exam Domain Notes" (one section per task statement), then 12 example questions, a 76-question practice test, 4 exercises, a technology appendix, and an out-of-scope list. [source: guide_en.md headings]

### 2. Exam and guide version
- Targets CCAR-F only. [source: REPO README.md]
- Mirrors the March 2026 launch guide (`OG-F-v0.1`): "Multiple choice (1 correct out of 4)", "Guessing penalty: None". v1.0 changed the format to "Multiple-choice and multiple-response items; each item states how many responses to select". The repo has not picked this up. [source: guide_en.md "Exam Format"] [source: OG-F-v1.0 §3]
- The 30 task-statement titles are identical in v0.1, v1.0, and v1.1. [source: OG-F-v0.1, OG-F-v1.0, OG-F-v1.1, diff of "Task Statement" lines]
- Its "4 out of 8 possible scenarios" claim is not official. The guides say 4 of 6. Scenario 7 ("Conversational AI Architecture Patterns") and scenario 8 come from candidate reports. Whether they appear on live forms is [unverified]. [source: guide_en.md "Exam Scenarios"] [source: OG-F-v1.0 §5]

### 3. Provenance of its practice items
- README: "The practical test questions come from the real exam materials and are kept as they are." [source: https://github.com/paullarionov/claude-certified-architect]
- The official guide says its samples are "drawn from the practice test". The repo's Q51 and Q57 match official samples 1–2 closely, so its 60-item bank likely mirrors Anthropic's retired practice exam. [source: OG-F-v1.0 §9] [inferred]
- This course does not reproduce or paraphrase those items. It writes its own questions. [inferred]

### 4. Anki and practice-test build
- One `.apkg` per language. English: 60 notes, 15 per scenario across 4 scenarios. Note type "Claude Certified Architect MCQ" with fields `Scenario`, `Situation`, `Question`, `OptionA`–`OptionD`, `Correct`, `Explanation`. [source: REPO anki/practical_test_en.apkg, SQLite inspection]
- Build: `genanki` parses the `QUESTIONS` array in `practical_test_<lang>.html`; a GitHub Action rebuilds decks on change. `extract_question.py`, which the HTML builder calls, is missing from the repo. [source: REPO utils/build_anki_deck.py; utils/build_practical_test_html.py]
- Answer letters in the 60-item bank: A 18, B 15, C 13, D 14. [source: REPO practical_test_en.html, counted]

### 5. Question style
- Scenario-anchored, single answer, A–D. Stems quote production metrics ("12% of cases", "55% vs 80% target") and ask for "the most effective first step" or "most likely root cause". [source: guide_en.md Practice Test]
- README advice: find the deciding phrase, prefer the proportionate root-cause fix with the least new machinery, and choose programmatic enforcement over stronger prompts when a rule must always hold. [source: REPO README.md "How to Read the Practical Test Questions"]
- Recurring distractor types: prompt or few-shot fixes where a guarantee is needed; over-engineering (classifier, routing layer); masking failure (empty result as success, generic error, aggregate metric); bigger model or context; shifting burden to users; invented features (`CLAUDE_HEADLESS`, `--batch`, `.claude/config.json`). [inferred]

### 6. High-yield content it teaches (checked against the guide)
- **Loop:** continue on `stop_reason == "tool_use"`, stop on `"end_turn"`; anti-patterns are text parsing, iteration caps as the main stop, and "assistant produced text". Tool results go back as `tool_result` blocks in a `user` message. [source: guide_en.md §1.2, §3.1] [source: OG-F-v1.0 Task 1.1]
- **Orchestration:** hub-and-spoke; subagents get only what the coordinator passes; parallel `Task` calls in one response; overly narrow decomposition as root cause; partition scope to avoid duplication; scoped `verify_fact`. [source: guide_en.md §3.3–3.4] [source: OG-F-v1.0 Tasks 1.2, 1.3, 2.3]
- **Hooks:** `PostToolUse` normalizes timestamps and status codes; a call-interception hook blocks refunds over $500 and redirects to escalation. The repo uses a pseudo-API (`@hook("PostToolUse")`); the real SDK registers callbacks in `options.hooks` with a `matcher`. [source: guide_en.md §3.5] [source: https://code.claude.com/docs/en/agent-sdk/hooks]
- **Tools:** descriptions drive selection; rename (`analyze_content` → `extract_web_results`); constrain (`fetch_url` → `load_document`); 4–5 tools per agent; keyword-sensitive system prompts misroute. A destructive action with preview is better as two tools (`preview_*` returns a token, `execute_*` requires it). [source: guide_en.md §1.4, §2.2, Q61]
- **MCP:** `.mcp.json` with `${GITHUB_TOKEN}` vs `~/.claude.json`; resources for catalogs; `isError` with categories; access failure vs valid empty result. [source: guide_en.md §4.3–4.4] [source: OG-F-v1.0 Tasks 2.2, 2.4]
- **Claude Code:** CLAUDE.md levels; new hire missing rules that live in user-level files; `.claude/rules/` `paths` globs for cross-directory tests; skills with `context: fork`, `allowed-tools`, `argument-hint`; `.claude/commands/` for team commands; plan mode for 45+ file migrations; `-p` plus `--output-format json --json-schema` in CI; independent review instance. [source: guide_en.md §5.1–5.10] [source: OG-F-v1.0 D3]
- **Prompting and extraction:** categorical criteria beat "be conservative"; disable high false-positive categories; 2–4 few-shot examples with rationale; nullable fields; `"other"` + detail; retry with the specific error; retries fail on absent data; `stated_total` vs `calculated_total`. [source: guide_en.md §2.4, §6.1–6.6] [source: OG-F-v1.0 D4]
- **Batches:** 50% savings, up to 24 h, no SLA, no multi-turn tool calling, `custom_id`, resubmit failures only; a 30 h SLA with 24 h processing implies 4 h submission windows. [source: guide_en.md §7.1–7.5] [source: OG-F-v1.0 Task 4.5]
- **Context and reliability:** case-facts block; key findings first; structured upstream outputs; escalate on explicit request, policy gap, or no progress; ask for more identifiers on multiple matches; structured handoffs; stratified sampling; claim-source mappings with dates. [source: guide_en.md §9–12] [source: OG-F-v1.0 D5]

### 7. Where the repo disagrees with the guide or current docs

| Topic | Repo | Official guide or current docs |
|---|---|---|
| Item format | Single answer, 1 of 4 | Multiple-choice and multiple-response since v1.0 [source: OG-F-v1.0 §3] |
| Scenario bank | 4 of 8 | 4 of 6 [source: OG-F-v1.0 §5] |
| `stop_reason` values | Four | Seven in current docs [source: https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons] |
| `@import` depth | 5 | "maximum depth of four hops" [source: https://code.claude.com/docs/en/memory] |
| `AgentDefinition` fields | `name`, `system_prompt`, `allowed_tools` | `description`, `prompt`, `tools`, `model`, `maxTurns`, ...; the name is the `agents` dict key [source: https://code.claude.com/docs/en/agent-sdk/subagents] |
| Personal skill override (Q36) | Changed on 2026-09-09 to "same name shadows the project skill" | Guide Task 3.2: personal variants "with different names to avoid affecting teammates". Docs precedence: enterprise > personal > project [source: OG-F-v1.0 Task 3.2] [source: https://code.claude.com/docs/en/skills] |
| Assistant prefill (Q72) | "Append a partial assistant message" | Prefill returns 400 on Claude 4.6+ models (fetched 2026-10-13) [source: https://platform.claude.com/docs/en/models/opus-5-5/migration-guide]. Prefill is not a CCAR-F task statement |

The full guide-vs-docs drift list lives in `02-anthropic-docs-and-courses.md`.

## Other community resources

Stars and last-push dates are from `gh search repos` / `gh api` on 2026-11-24. "First-hand" means the author states they sat the exam.

| Repo | Stars · last push | What it is | Notes |
|---|---|---|---|
| [daronyondem/claude-architect-exam-guide](https://github.com/daronyondem/claude-architect-exam-guide) | 1,135 · 2026-11-19 | One long guide in knowledge areas with "What to Know" and "Common Pitfalls" | States "No exam questions are included, paraphrased, or hinted at". More current on API details (structured outputs, MCP protocol vs execution errors) [source: README] |
| [OlivierAlter/Claude-Certified-Architect-Foundations-Certification-Exam](https://github.com/OlivierAlter/Claude-Certified-Architect-Foundations-Certification-Exam) | 246 · 2026-03-15 | 77-question practice exam plus a Claude Code skill to run it | "Reverse-engineered from the official exam guide". Built on the launch guide; not updated since March [source: README] |
| [sarveshtalele/claude-architect-exam-guide](https://github.com/sarveshtalele/claude-architect-exam-guide) | 196 · 2026-11-24 | Curated resources, copies of the official guides, a study skill with `/ccarf-*` commands | Covers Foundations and Professional [source: gh search] |
| [hamzafarooq/claude-certified-architect](https://github.com/hamzafarooq/claude-certified-architect) | 174 · 2026-09-10 | Cheat sheets organized by task statement, practice exam, sample-question analysis | Invites PRs with "a question from the real exam that you're allowed to share", which conflicts with the NDA [source: README] |
| [dnacenta/claude-certified-architect](https://github.com/dnacenta/claude-certified-architect) | 154 · 2026-11-23 | Per-domain deep dive (`domains/d1…d5`) plus overviews of the other certifications | First repo seen that links guide v1.1 and notes "for CCAR-F only the registration, ID, and support text changed" (confirmed by diff) [source: README] |
| [aderegil/claude-certified-architect](https://github.com/aderegil/claude-certified-architect) | 115 · 2026-05-19 | Guided labs: working code for each of the 6 scenarios, all 30 task statements | Good hands-on supplement [source: README] |
| [timothywarner-org/claude-architect](https://github.com/timothywarner-org/claude-architect) | 101 · 2026-09-19 | Live-teaching notebooks and a vendored copy of Anthropic's Claude Cookbooks | Practice questions sourced from paullarionov [source: README] |
| [vkorost/claude-certified-architect-guide](https://github.com/vkorost/claude-certified-architect-guide) | 49 · 2026-11-02 | Book-length guide to Claude Code architecture for CCAR-F | First-hand: "I passed the exam on 22 August 2026", with a Credly link; says the book "will drift" [source: README] |
| [utkarsh1agarwal/claude-architect-exam-guide](https://github.com/utkarsh1agarwal/claude-architect-exam-guide) | 47 · 2026-11-23 | Study guide and 6 mock exams | Not reviewed in depth [source: gh search] |
| [SGridworks/claude-certified-architect-training](https://github.com/SGridworks/claude-certified-architect-training) | 39 · 2026-11-12 | 12-week program, 110 practice questions, a retro RPG game | Not reviewed in depth [source: gh search] |
| [termidy/CCAR-F-practice](https://github.com/termidy/CCAR-F-practice) | 29 · 2026-11-23 | Python practice code ("ShopAssist") on the Claude API, plus Udemy course labs | Companion to a paid course [source: gh search] |
| [hong-chu/claude-certified-architect-foundations-llm-wiki](https://github.com/hong-chu/claude-certified-architect-foundations-llm-wiki) | 31 · 2026-11-16 | Domain-organized study wiki | Not reviewed in depth [source: gh search] |

Commercial and publisher material also exists: Pluralsight demos (`keshawillz/ps-ccarf-agentic-architecture_orchestration`), a Packt bootcamp repo, a Skillsoft bootcamp repo, and Udemy courses. None was evaluated. [source: gh search repos "CCAR-F"] [unverified]

## Takeaways for this course [inferred]

- Most repos still describe the launch format (single answer, 4 options). Practice in this course includes multiple-response items to match v1.0+.
- Several repos claim or invite real exam content. This course cites only the public guide and writes original items.
- The useful community additions are hands-on labs (aderegil, termidy) and docs-drift notes (daronyondem, dnacenta). Point learners there for extra practice.
