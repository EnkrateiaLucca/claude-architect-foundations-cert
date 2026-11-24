# Claude Certified Architect – Foundations (CCAR-F): Exam Guide Research

Research date: 2026-11-24.

## Context

This file records what Anthropic officially publishes about the Claude Certified Architect – Foundations exam: logistics, audience, blueprint, scenarios, task statements, sample items, scoring, and policies. The lessons, practice questions, flashcards, and cheatsheet in this repo align to the blueprint below. A short, labelled section at the end compares CCAR-F with the Professional exam (CCAR-P).

**Headline:** The official exam guide is public. Two versions exist. v1.0 ("Effective July 2026", 39 pages) and v1.1 ("Effective November 2026", 42 pages). v1.1 changes only the registration, identification, and support sections. The blueprint, scenarios, 30 task statements, 12 sample questions, preparation exercises, and appendix are word-for-word identical. [source: https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542750%2FClaude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf] [source: https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf]

Label conventions: `[source: url]` marks a fetched and read source. `[inferred]` marks my own analysis built on sourced facts. `[unverified]` marks a claim I could not confirm with a fetched page. "Unofficial" marks third-party material.

## Sources

| ID | Source | Type | Fetched |
|----|--------|------|---------|
| G10 | [CCAR-F Exam Guide v1.0 (PDF)](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542750%2FClaude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf) | Official, primary | Yes. curl + `pdftotext -layout`. Still the link in the body of the Foundations exam page |
| G11 | [CCAR-F Exam Guide v1.1 (PDF)](https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf) | Official, primary | Yes. Same method. PDF created 2026-11-17. Linked from the Partner Academy navigation. A Japanese edition sits at `.../1794946295/Claude_Certified_Architect_-_Foundations_Exam_Guide_Japanese.pdf` |
| S3 | [Partner Academy: Earn your Claude certification](https://anthropic-partners.skilljar.com/page/partner-certifications) | Official | Yes |
| S4 | [Partner Academy: Certification FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications) | Official | Yes |
| S5 | [Partner Academy: Certification policies](https://anthropic-partners.skilljar.com/page/policies-certifications) | Official | Yes |
| S6 | [Partner Academy: Who can take an exam](https://anthropic-partners.skilljar.com/page/certification-eligibility) | Official | Yes |
| S7 | [Partner Academy: CCAR-F exam page](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification) | Official | Yes |
| S8 | [Partner Academy: CCAR-F prep courses](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses) | Official | Yes. See `04-official-prep-path.md` |
| S9 | [Partner Academy: all exam prep courses](https://anthropic-partners.skilljar.com/page/claude-certification-exam-prep-courses) | Official | Yes |
| S10 | [anthropic.com: Claude Partner Network (2026-03-12)](https://www.anthropic.com/news/claude-partner-network) | Official | Fetched 2026-10-13, not re-fetched |
| S11 | [claude.com: Four role-based certifications (2026-07-23)](https://claude.com/resources/articles/four-role-based-claude-certifications) | Official | Fetched 2026-10-13, not re-fetched |
| F1 | `https://anthropic-partners.skilljar.com/path/claude-certified-architect-foundations` | Official (guessed URL) | **Failed**: HTTP 404. Foundations has a prep-courses *page*, not a learning *path* like CCAR-P |

## Logistics

Values come from Section 3 "Exam Details at a Glance" of G10 and G11 (identical) unless noted.

| Item | Value | Source |
|------|-------|--------|
| Credential | Claude Certified Architect – Foundations | [source: G10 §3] |
| Exam code | CCAR-F. Community sites also write "CCA-F" | [source: G10 §3] |
| Guide version | v1.1, "Effective November 2026". Document control: 0.1 Initial draft Feb 2026 · 0.2 Draft revision Jun 2026 · 1.0 Formatting and layout updates Jul 2026 · 1.1 Registration, identification, and support updates Nov 2026 | [source: G11 §18] |
| Launch | "Claude Certified Architect, Foundations, available today for partners" (2026-03-12, with the Claude Partner Network) | [source: https://www.anthropic.com/news/claude-partner-network] |
| Number of items | 60 | [source: G10 §3] |
| Item format | "Multiple-choice and multiple-response items; each item states how many responses to select". FAQ: "multiple choice and scenario-based multiple response questions" | [source: G10 §3] [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |
| Exam structure | "4 scenarios drawn from a bank of 6" | [source: G10 §3, §5] |
| Time limit | 120 minutes. FAQ: "Plan for about 135 minutes of total seat time, which includes check-in, instructions, and a brief post-exam survey." | [source: G10 §3] [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |
| Delivery | "Proctored: online proctored and/or test center, per program policy". Pearson VUE: OnVUE online or a Pearson test center | [source: G10 §3] [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |
| Open/closed book | "No. Exams are closed book. Browser translation tools are not permitted under the Pearson proctoring platform." | [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |
| Languages | "The exam and prep content are available in English and Japanese." Non-native speakers can request an ESL time extension through Pearson (3–5 business days) | [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |
| Passing score | "Scaled score of 720 on a scale of 100–1,000". 720 is a scaled score, not 72% raw | [source: G10 §3, §10] [inferred] |
| Fee | $125 USD before any partner-tier discount. Same on the certifications page and the FAQ | [source: G10 §3] [source: https://anthropic-partners.skilljar.com/page/partner-certifications] |
| Validity | 12 months from award. Credentials earned before 2026-06-30 under the old 6-month rule were extended to 12 months | [source: G10 §3, §15] [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |
| Result reporting | "Pass/fail with scaled score (100–1,000), plus percent-correct by domain on the score report." Score appears on screen at the end of the exam | [source: G10 §3] [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |
| Badge | Credly badge by email, usually within minutes for online exams | [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |
| Practice exam | "The practice exam available on the previous platform was retired in the move to Pearson. The exam guide includes sample questions that show the format and style of what's on the exam." | [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |
| Eligibility | People at Claude Partner Network organizations only. Sign in with a company email on a domain in the partner record; personal addresses fail. Age 18+, government-issued ID. Adding a domain takes 7–10 days | [source: https://anthropic-partners.skilljar.com/page/certification-eligibility] [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |
| Partner Network credit | CCAR-F counts toward Claude Partner Network tier eligibility. Associate does not | [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |
| Prerequisite | None. FAQ: "Foundations proves an architect can build with Claude." It does not upgrade to Professional automatically | [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |

The Foundations exam page on Skilljar shows a "Register | FREE" button. That button enrolls you in the Skilljar page that holds the guide and policies. The exam fee is paid at Pearson checkout. [source: https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification] [source: https://anthropic-partners.skilljar.com/page/faq-certifications] [inferred]

## Registration and scheduling (changed in November 2026)

Since 2026-11-12 you sign in to Pearson through Partner Academy single sign-on and pay at Pearson's checkout. [source: https://anthropic-partners.skilljar.com/page/faq-certifications]

1. Sign in to Partner Academy with your company email and open the CCAR-F page.
2. Select **Register**. Confirm your first and last name. They must match your government ID exactly. You can change your name yourself once; confirming the profile locks it for a year.
3. Select **Continue to Pearson**. Choose OnVUE or a test center, accept the policies, pick the exam language, a date and a time.
4. Check out. Any partner discount applies automatically.
5. Keep Pearson's confirmation email. It holds the link that starts an online exam.

[source: https://anthropic-partners.skilljar.com/page/faq-certifications] [source: G11 §11]

**Reschedule and cancel.** OnVUE: up to **1 hour** before the appointment. Test center: up to **48 hours** before. Later changes and no-shows forfeit the fee. Rescheduling keeps the locked price. Cancelling after paying at Pearson starts an automatic refund (7–10 business days). [source: G11 §11] [source: https://anthropic-partners.skilljar.com/page/policies-certifications]

G10 said "You may cancel or reschedule up to 24 hours before your appointment". G11 replaced that text. Use the 1 h / 48 h rule. [source: G10 §11] [source: G11 §11]

## Audience

"The ideal candidate for this certification is a solution architect who designs and implements production applications with Claude." The guide lists hands-on experience with: [source: G10 §2]

- Building agentic applications with the Claude Agent SDK (multi-agent orchestration, subagent delegation, tool integration, lifecycle hooks)
- Configuring Claude Code for team workflows (CLAUDE.md, Agent Skills, MCP servers, plan mode)
- Designing MCP tool and resource interfaces for backend integration
- Engineering prompts for reliable structured output (JSON schemas, few-shot examples, extraction patterns)
- Managing context windows across long documents, multi-turn conversations, and multi-agent handoffs
- Integrating Claude into CI/CD for automated code review, test generation, and PR feedback
- Making escalation and reliability decisions (error handling, human-in-the-loop, self-evaluation)

Recommended experience: "6+ months of practical experience building with Claude APIs, Agent SDK, Claude Code, and MCP". [source: G10 §2]

## Blueprint

[source: G10 §4]

| Domain | Name | Weight | ≈ items of 60 [inferred] | Task statements |
|---|---|---|---|---|
| 1 | Agentic Architecture & Orchestration | 27% | 16 | 7 (1.1–1.7) |
| 2 | Tool Design & MCP Integration | 18% | 11 | 5 (2.1–2.5) |
| 3 | Claude Code Configuration & Workflows | 20% | 12 | 6 (3.1–3.6) |
| 4 | Prompt Engineering & Structured Output | 20% | 12 | 6 (4.1–4.6) |
| 5 | Context Management & Reliability | 15% | 9 | 6 (5.1–5.6) |

Weights "reflect the relative importance of each domain to competent performance as determined through the job task analysis" and give "the approximate proportion of scored items drawn from each domain". [source: G10 §4]

## Scenarios

"During the exam, 4 scenarios are presented and picked at random from the full set of the 6 scenarios below." [source: G10 §5]

| # | Scenario | Setup (condensed) | Primary domains |
|---|---|---|---|
| 1 | Customer Support Resolution Agent | Agent SDK agent with MCP tools `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`. Target 80%+ first-contact resolution | D1, D2, D5 |
| 2 | Code Generation with Claude Code | Team uses Claude Code for generation, refactoring, debugging, docs. Slash commands, CLAUDE.md, plan mode vs direct execution | D3, D5 |
| 3 | Multi-Agent Research System | Coordinator delegates to web search, document analysis, synthesis, and report subagents. Cited reports | D1, D2, D5 |
| 4 | Developer Productivity with Claude | Agent SDK tool for exploring codebases and legacy systems with Read, Write, Bash, Grep, Glob plus MCP servers | D2, D3, D1 |
| 5 | Claude Code for Continuous Integration | Automated reviews, test generation, PR feedback. Actionable feedback, few false positives | D3, D4 |
| 6 | Structured Data Extraction | Extraction from unstructured documents, JSON schema validation, edge cases, downstream integration | D4, D5 |

[source: G10 §5]

Counting primary-domain mentions: D1 3, D2 3, D3 3, D4 2, D5 4. Every scenario touches at least two domains, so prepare all five whichever four you draw. [inferred]

## Task statements (summary)

Each task statement lists "Knowledge of" and "Skills in" bullets. Titles are verbatim. [source: G10 §6]

**Domain 1: Agentic Architecture & Orchestration**
- 1.1 Design and implement agentic loops for autonomous task execution. Loop on `stop_reason` (`"tool_use"` continues, `"end_turn"` stops). Anti-patterns: parsing text for completion, iteration caps as the primary stop, treating text content as "done".
- 1.2 Orchestrate multi-agent systems with coordinator-subagent patterns. Hub-and-spoke, isolated subagent context, dynamic subagent selection, scope partitioning, iterative refinement, risk of overly narrow decomposition.
- 1.3 Configure subagent invocation, context passing, and spawning. `Task` tool, `allowedTools` must include `"Task"`, explicit context in the prompt, `AgentDefinition`, parallel `Task` calls in one response, goal-and-criteria coordinator prompts.
- 1.4 Implement multi-step workflows with enforcement and handoff patterns. Programmatic prerequisites (block `process_refund` until `get_customer` returns a verified ID), multi-concern decomposition, structured human handoff summaries.
- 1.5 Apply Agent SDK hooks for tool call interception and data normalization. `PostToolUse` normalizes formats; call-interception hooks block violations (refund > $500) and redirect to escalation.
- 1.6 Design task decomposition strategies for complex workflows. Prompt chaining for predictable reviews, dynamic decomposition for open-ended investigation, per-file passes plus a cross-file pass.
- 1.7 Manage session state, resumption, and forking. `--resume <session-name>`, `fork_session`, tell a resumed session what changed, start fresh with a summary when tool results are stale.

**Domain 2: Tool Design & MCP Integration**
- 2.1 Design effective tool interfaces with clear descriptions and boundaries. Descriptions drive selection; rename and split overlapping tools; check system prompts for keyword-sensitive wording.
- 2.2 Implement structured error responses for MCP tools. `isError`, error categories (transient, validation, business, permission), `isRetryable`, access failure vs valid empty result, local recovery.
- 2.3 Distribute tools appropriately across agents and configure tool choice. 4–5 tools beats 18, scoped cross-role tools (`verify_fact`), `tool_choice` `"auto"`, `"any"`, forced.
- 2.4 Integrate MCP servers into Claude Code and agent workflows. `.mcp.json` (project) vs `~/.claude.json` (user), `${GITHUB_TOKEN}` expansion, all servers' tools available at once, MCP resources for catalogs, community servers for standard integrations.
- 2.5 Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively. Grep for content, Glob for paths, Edit needs unique anchor text, Read + Write fallback, incremental exploration.

**Domain 3: Claude Code Configuration & Workflows**
- 3.1 Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization. User, project, directory levels; `@import`; `.claude/rules/`; `/memory` to verify loaded files.
- 3.2 Create and configure custom slash commands and skills. `.claude/commands/` vs `~/.claude/commands/`; `.claude/skills/` with `SKILL.md` frontmatter `context: fork`, `allowed-tools`, `argument-hint`; skills vs CLAUDE.md.
- 3.3 Apply path-specific rules for conditional convention loading. `paths:` globs in `.claude/rules/` frontmatter, rules beat subdirectory CLAUDE.md for cross-directory conventions.
- 3.4 Determine when to use plan mode vs direct execution. Plan mode for architectural, multi-file, multi-approach work; direct execution for clear single-file changes; Explore subagent for verbose discovery.
- 3.5 Apply iterative refinement techniques for progressive improvement. 2–3 input/output examples, test-driven iteration, interview pattern, batch interacting fixes vs sequential independent fixes.
- 3.6 Integrate Claude Code into CI/CD pipelines. `-p`/`--print`, `--output-format json`, `--json-schema`, CLAUDE.md for CI context, independent review instance, pass prior findings and existing tests.

**Domain 4: Prompt Engineering & Structured Output**
- 4.1 Design prompts with explicit criteria to improve precision and reduce false positives. Categorical criteria beat "be conservative"; disable noisy categories; severity criteria with code examples.
- 4.2 Apply few-shot prompting to improve output consistency and quality. 2–4 targeted examples with reasoning, format demonstration, varied document structures, fixes for null extraction.
- 4.3 Enforce structured output using tool use and JSON schemas. `tool_use` removes syntax errors, not semantic ones; `tool_choice` options; nullable fields; `"unclear"` and `"other"` + detail.
- 4.4 Implement validation, retry, and feedback loops for extraction quality. Retry with specific errors; retries fail when data is absent; `detected_pattern`; `calculated_total` vs `stated_total`; `conflict_detected`.
- 4.5 Design efficient batch processing strategies. Message Batches API: 50% savings, up to 24 h, no latency SLA, no multi-turn tool calling, `custom_id`, resubmit failures only, refine prompts on a sample first.
- 4.6 Design multi-instance and multi-pass review architectures. Independent reviewer beats self-review; per-file passes plus integration pass; self-reported confidence per finding for routing.

**Domain 5: Context Management & Reliability**
- 5.1 Manage conversation context to preserve critical information across long interactions. Case-facts block, trim tool output, lost-in-the-middle mitigation, structured upstream outputs.
- 5.2 Design effective escalation and ambiguity resolution patterns. Escalate on human request, policy gap, or no progress; sentiment and self-rated confidence are unreliable; ask for identifiers on multiple matches.
- 5.3 Implement error propagation strategies across multi-agent systems. Structured error context, access failure vs empty result, no silent suppression, no whole-workflow termination, coverage annotations.
- 5.4 Manage context effectively in large codebase exploration. Context degradation, scratchpad files, subagent delegation, manifests for crash recovery, `/compact`.
- 5.5 Design human review workflows and confidence calibration. Aggregate accuracy hides segment failures, stratified sampling, field-level confidence calibrated on labeled sets.
- 5.6 Preserve information provenance and handle uncertainty in multi-source synthesis. Claim-source mappings, annotate conflicts, require dates, render content types appropriately.

## Appendix: in scope and out of scope

The guide's Section 17 has three lists. [source: G10 §17]

**Technologies and concepts** that might appear: Claude Agent SDK, MCP, Claude Code, Claude Code CLI (`-p`, `--output-format json`, `--json-schema`), Claude API (`tool_use`, `tool_choice`, `stop_reason`, `max_tokens`, system prompts), Message Batches API, JSON Schema, Pydantic, built-in tools, few-shot prompting, prompt chaining, context window management, session management, confidence scoring.

**Out of scope** (verbatim list condensed): fine-tuning or training custom models · API authentication, billing, account management · detailed language or framework implementation · deploying or hosting MCP servers · Claude's internal architecture, training, weights · Constitutional AI, RLHF, safety training · embedding models and vector databases · computer use · vision · streaming and server-sent events · rate limiting, quotas, pricing calculations · OAuth and key rotation · cloud provider configuration · benchmarking and model comparison · prompt caching "beyond knowing it exists" · tokenization. [source: G10 §17]

## Sample questions

The guide publishes 12 samples "drawn from the practice test", three per scenario for four of the six scenarios. All 12 are single-answer with four options. [source: G10 §9]

| # | Scenario | Tests | Answer and the rule behind it |
|---|---|---|---|
| 1 | Customer Support | 1.4 | A. Programmatic prerequisite blocks `lookup_order`/`process_refund` until `get_customer` verifies the ID |
| 2 | Customer Support | 2.1 | B. Expand tool descriptions (formats, examples, edge cases, boundaries) as the first step |
| 3 | Customer Support | 5.2 | A. Explicit escalation criteria with few-shot examples; self-reported confidence and sentiment lose |
| 4 | Code Generation | 3.2 | A. Team `/review` command goes in `.claude/commands/` |
| 5 | Code Generation | 3.4 | A. Plan mode for a monolith-to-microservices restructure |
| 6 | Code Generation | 3.3 | A. `.claude/rules/` with glob `paths` for test files spread across the tree |
| 7 | Multi-Agent Research | 1.2 | B. The coordinator's decomposition is too narrow |
| 8 | Multi-Agent Research | 5.3 | A. Structured error context (failure type, query, partial results, alternatives) |
| 9 | Multi-Agent Research | 2.3 | A. Scoped `verify_fact` tool for the 85% simple case |
| 10 | Continuous Integration | 3.6 | A. Add `-p` |
| 11 | Continuous Integration | 4.5 | A. Batch the overnight report, keep the pre-merge check synchronous |
| 12 | Continuous Integration | 4.6 | A. Per-file passes plus a cross-file integration pass |

[source: G10 §9]

Ten of the twelve correct answers are A. The live exam randomizes or balances letters, so do not read anything into this. [inferred]

The wrong options repeat a small set of patterns: prompt instructions where a guarantee is needed, new infrastructure before the cheap fix (classifiers, routing layers), bigger models or context windows, unreliable proxies (self-rated confidence, sentiment), invented features (`CLAUDE_HEADLESS`, `--batch`, `.claude/config.json`), and hiding or killing errors. The explanations reward "the proportionate first response" at "the root cause". [source: G10 §9] [inferred]

## Preparation guidance

Section 7 "How to Prepare" lists seven activities: build an Agent SDK agent with a full loop, sessions and subagents; configure Claude Code for a real project; design and test MCP tools; build an extraction pipeline with batches; practice few-shot, criteria, and multi-pass review; study context patterns; review escalation and human review. [source: G10 §7]

Section 8 gives four exercises: (1) multi-tool agent with escalation logic, (2) Claude Code for a team workflow, (3) structured data extraction pipeline, (4) multi-agent research pipeline. [source: G10 §8]

## Scoring

- Criterion-referenced: each candidate is measured against a fixed standard, not against peers. [source: G10 §10]
- The cut score came from "a formal standard-setting study in which trained subject matter experts judged the level of performance expected of a minimally qualified candidate." [source: G10 §10]
- Scaled scoring equates forms of slightly different difficulty. [source: G10 §10]
- Domain percentages on the score report "are not used to determine your pass or fail result". [source: G10 §10]
- The guide does not say whether multiple-response items give partial credit. Treat them as all-or-nothing. [unverified]
- If you pass, you cannot retake to improve your score. [source: https://anthropic-partners.skilljar.com/page/policies-certifications]

## Policies

| Policy | Rule | Source |
|---|---|---|
| Retakes | 14 days after the first fail, 30 after the second, 90 after the third. Max 4 attempts per rolling 12 months, per exam. Each attempt pays the fee; partner discounts apply | [source: G10 §12] [source: https://anthropic-partners.skilljar.com/page/policies-certifications] |
| ID | Valid, unexpired, government-issued photo ID; name must match the exam profile exactly. Mismatch at check-in forfeits the fee | [source: G11 §12] [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |
| Name changes | Update the exam profile yourself before scheduling. OnVUE syncs in near real time; test-center updates sync once a day, so change at least 24 h ahead. One self-service change, then contact certifications-support@anthropic.com | [source: G11 §12] |
| Accommodations | Request through Pearson before scheduling, 10+ days ahead | [source: G10 §12] [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |
| No-show | Fee forfeited; re-register | [source: G10 §12] |
| Conduct | Webcam view, clear desk, no communication, no copying content. Misconduct can lead to invalidation, revocation, bans, and test-center-only requirements | [source: G10 §13] [source: https://anthropic-partners.skilljar.com/page/policies-certifications] |
| NDA | All questions, options, and scenarios are confidential, "including in study groups and online forums" | [source: G10 §14] [source: https://anthropic-partners.skilljar.com/page/policies-certifications] |
| Renewal | Free on-time renewal: review changes and pass a free, non-proctored (policies page: "open-book online") assessment on Partner Academy, retakeable as often as needed. Extends 12 months from the current expiry. A lapse means the full exam at full fee. A substantial exam update can require the full exam | [source: G10 §15] [source: https://anthropic-partners.skilljar.com/page/policies-certifications] |
| Appeals | Within 14 days of a decision, or of the exam date for a result concern, via a Pearson support case. A confirmed faulty question earns a free retake, not a changed score | [source: G10 §16] [source: https://anthropic-partners.skilljar.com/page/policies-certifications] |
| Reporting a bad question | Report to Pearson; reporting never affects your result | [source: https://anthropic-partners.skilljar.com/page/policies-certifications] |
| Support | Sign-in, missing exam, discount, profile: certifications-support@anthropic.com. Scheduling, exam-day, accommodations, results: Pearson support at pearsonvue.com/us/en/anthropic.html. Partner record and domains: partner-support@anthropic.com | [source: G11 §16] [source: https://anthropic-partners.skilljar.com/page/faq-certifications] |

Candidates who attempted CCAR-F before the 2026-06-30 move to Pearson and failed had that attempt cleared, with no waiting period. [source: https://anthropic-partners.skilljar.com/page/faq-certifications]

## Compared with CCAR-P (comparison only)

This section exists to help candidates choose an exam. Nothing in it is CCAR-F content. The CCAR-P figures come from the Professional guide v1.0 (fetched 2026-10-13) and the FAQ. Partner Academy also links a CCAR-P guide "Updated Dec 7", which this file did not review. [source: https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542810%2FClaude+Certified+Architect+%E2%80%93+Professional+Exam+Guide.pdf] [source: https://anthropic-partners.skilljar.com/page/faq-certifications]

| Dimension | Foundations (CCAR-F) | Professional (CCAR-P) |
|---|---|---|
| Items | 60 | 63 |
| Time · pass mark | 120 min · 720 / 100–1,000 | 120 min · 720 / 100–1,000 |
| Structure | 4 scenarios from a bank of 6 | Standalone items, no scenario bank |
| Domains | 5, with 30 numbered task statements ("Knowledge of / Skills in") | 7, with 38 single-line objectives |
| Fee | $125 | $175 |
| Altitude | Implementation detail: `stop_reason`, `tool_choice`, `.mcp.json`, `.claude/rules/`, `-p`, Message Batches | Governance, evaluation, integration architecture, stakeholders; names no API parameters |
| FAQ framing | "Foundations proves an architect can build with Claude." | "Professional proves they can design and govern Claude solutions at enterprise scale." |

Topics CCAR-F lists as out of scope (prompt caching details, embeddings and vector databases, OAuth, cloud provider configuration, benchmarking) appear in CCAR-P objectives. Do not study them for CCAR-F. [inferred]

## Takeaways for the course [inferred]

- Teach the v1.1 guide. Its exam content equals v1.0, so v1.0-based material stays valid, but link v1.1 and use the 1 h / 48 h reschedule rule.
- Weight study time by the blueprint: D1 alone is 27%.
- Write original practice items. The guide's 12 samples are public; the live exam and the retired practice test are confidential.
- Include multiple-response items in practice, because v1.0+ allows them and none of the public samples show one.
- Flag docs drift (see `02-anthropic-docs-and-courses.md`) without changing the exam answer.
