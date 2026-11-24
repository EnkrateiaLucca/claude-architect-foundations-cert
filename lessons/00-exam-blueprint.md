# The CCAR-F Exam and Its Blueprint

The Claude Certified Architect – Foundations (CCAR-F) exam tests whether you can make sound tradeoff decisions when you build production solutions with Claude. The official Exam Guide v1.1 (effective November 2026) is the authoritative reference. It defines five weighted domains, 30 task statements, six scenarios, and twelve sample questions. Every lesson, question, and exercise in this course maps back to that guide.

## What the credential validates

### The one-sentence definition
*Informed tradeoff decisions across Claude Code, the Agent SDK, the Claude API, and MCP.*

The guide states: "The Claude Certified Architect – Foundations certification validates that practitioners can make informed decisions about tradeoffs when implementing real-world solutions with Claude."

The exam covers four core technologies:

| Technology | What the exam expects you to know |
|---|---|
| Claude Agent SDK | Agentic loops, `stop_reason`, subagents via the `Task` tool, `allowedTools`, hooks, sessions |
| Claude Code | CLAUDE.md hierarchy, `.claude/rules/`, commands, skills, plan mode, `-p` in CI |
| Claude API | `tool_use` with JSON schemas, `tool_choice`, Message Batches API |
| Model Context Protocol (MCP) | Tools vs resources, `isError`, `.mcp.json` vs `~/.claude.json`, env var expansion |

Questions come from realistic customer use cases. You need practical judgment about architecture, configuration, and tradeoffs. Recall of definitions alone will not pass.

### Who the exam targets
*A solution architect with 6+ months of hands-on Claude experience.*

The ideal candidate designs and implements production applications with Claude and has hands-on experience with:

- Building agentic applications with the Claude Agent SDK: multi-agent orchestration, subagent delegation, tool integration, lifecycle hooks
- Configuring Claude Code for team workflows: CLAUDE.md files, Agent Skills, MCP server integrations, plan mode
- Designing MCP tool and resource interfaces for backend system integration
- Engineering prompts for reliable structured output: JSON schemas, few-shot examples, extraction patterns
- Managing context windows across long documents, multi-turn conversations, and multi-agent handoffs
- Integrating Claude into CI/CD pipelines for code review, test generation, and pull request feedback
- Making escalation and reliability decisions: error handling, human-in-the-loop workflows, self-evaluation

The typical candidate has 6+ months of practical experience with the Claude APIs, Agent SDK, Claude Code, and MCP.

## Exam format

| Item | Detail |
|---|---|
| Exam code | CCAR-F |
| Items | 60, multiple-choice and multiple-response. Each item states how many responses to select |
| Structure | 4 scenarios drawn at random from a bank of 6 |
| Time | 120 minutes, about 2 minutes per item |
| Passing score | Scaled 720 on a 100–1,000 scale. A scaled 720 is not the same as 72% raw |
| Fee | $125 USD per attempt |
| Delivery | Proctored by Pearson VUE, online or at a test center |
| Validity | 12 months. On-time renewal is free |
| Result | Pass/fail with scaled score, plus percent-correct by domain |

Treat multiple-response items as all-or-nothing. Judge each option as its own true/false statement.

## The blueprint

| Domain | Name | Weight | ≈ Items | Task statements |
|---|---|---|---|---|
| D1 | Agentic Architecture & Orchestration | 27% | 16 | 1.1–1.7 |
| D2 | Tool Design & MCP Integration | 18% | 11 | 2.1–2.5 |
| D3 | Claude Code Configuration & Workflows | 20% | 12 | 3.1–3.6 |
| D4 | Prompt Engineering & Structured Output | 20% | 12 | 4.1–4.6 |
| D5 | Context Management & Reliability | 15% | 9 | 5.1–5.6 |

D1 alone carries more than a quarter of the exam. D3 and D4 together carry 40%. Item counts are estimates from the weights; the guide gives percentages only.

### All 30 task statements
*Exam items are written against these objectives.*

**D1 · Agentic Architecture & Orchestration**

1. **1.1** Design and implement agentic loops for autonomous task execution
2. **1.2** Orchestrate multi-agent systems with coordinator-subagent patterns
3. **1.3** Configure subagent invocation, context passing, and spawning
4. **1.4** Implement multi-step workflows with enforcement and handoff patterns
5. **1.5** Apply Agent SDK hooks for tool call interception and data normalization
6. **1.6** Design task decomposition strategies for complex workflows
7. **1.7** Manage session state, resumption, and forking

**D2 · Tool Design & MCP Integration**

1. **2.1** Design effective tool interfaces with clear descriptions and boundaries
2. **2.2** Implement structured error responses for MCP tools
3. **2.3** Distribute tools appropriately across agents and configure tool choice
4. **2.4** Integrate MCP servers into Claude Code and agent workflows
5. **2.5** Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively

**D3 · Claude Code Configuration & Workflows**

1. **3.1** Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization
2. **3.2** Create and configure custom slash commands and skills
3. **3.3** Apply path-specific rules for conditional convention loading
4. **3.4** Determine when to use plan mode vs direct execution
5. **3.5** Apply iterative refinement techniques for progressive improvement
6. **3.6** Integrate Claude Code into CI/CD pipelines

**D4 · Prompt Engineering & Structured Output**

1. **4.1** Design prompts with explicit criteria to improve precision and reduce false positives
2. **4.2** Apply few-shot prompting to improve output consistency and quality
3. **4.3** Enforce structured output using tool use and JSON schemas
4. **4.4** Implement validation, retry, and feedback loops for extraction quality
5. **4.5** Design efficient batch processing strategies
6. **4.6** Design multi-instance and multi-pass review architectures

**D5 · Context Management & Reliability**

1. **5.1** Manage conversation context to preserve critical information across long interactions
2. **5.2** Design effective escalation and ambiguity resolution patterns
3. **5.3** Implement error propagation strategies across multi-agent systems
4. **5.4** Manage context effectively in large codebase exploration
5. **5.5** Design human review workflows and confidence calibration
6. **5.6** Preserve information provenance and handle uncertainty in multi-source synthesis

## The six scenarios

Each scenario frames a set of questions. Your exam shows 4 of the 6, picked at random. Prepare for all six.

| # | Scenario | Setup | Primary domains |
|---|---|---|---|
| 1 | Customer Support Resolution Agent | Agent SDK agent for returns, billing disputes, account issues. MCP tools `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`. Target 80%+ first-contact resolution | D1, D2, D5 |
| 2 | Code Generation with Claude Code | Team uses Claude Code for generation, refactoring, debugging, docs. Custom slash commands, CLAUDE.md, plan mode vs direct execution | D3, D5 |
| 3 | Multi-Agent Research System | Coordinator delegates to web search, document analysis, synthesis, and report subagents. Produces cited reports | D1, D2, D5 |
| 4 | Developer Productivity with Claude | Agent SDK tool that explores codebases and legacy systems with Read, Write, Bash, Grep, Glob plus MCP servers | D2, D3, D1 |
| 5 | Claude Code for Continuous Integration | Automated code review, test generation, PR feedback. Prompts must be actionable and minimize false positives | D3, D4 |
| 6 | Structured Data Extraction | Extract from unstructured documents, validate with JSON schemas, handle edge cases, feed downstream systems | D4, D5 |

### How to use the scenarios
*Learn each scenario's cast of tools and failure modes before exam day.*

The scenario text sets the facts that every question in its set relies on. Read it once and note the tool names, the target metric, and the constraint. In the Customer Support scenario, the 80% first-contact resolution target and the financial tool `process_refund` drive most answers. In the CI scenario, "minimize false positives" drives most answers.

## What is in scope and what is not

| Tested (Appendix, In-Scope Topics) | Not tested (Appendix, Out-of-Scope Topics) |
|---|---|
| Agentic loops, `stop_reason`, loop termination | Fine-tuning or training custom models |
| Coordinator-subagent patterns, parallel subagents, iterative refinement | API authentication, billing, account management |
| Explicit context passing, state persistence, crash-recovery manifests | Deploying or hosting MCP servers |
| Tool descriptions, splitting vs consolidating tools, tool naming | Claude's internal architecture, training, weights |
| MCP tools vs resources, project vs user scope, env var expansion | Constitutional AI, RLHF, safety training |
| Structured errors: transient, validation, business, permission | Embeddings and vector databases |
| Escalation criteria, honoring customer preferences, policy gaps | Computer use, vision/image analysis |
| CLAUDE.md hierarchy, `@import`, `.claude/rules/` globs | Streaming API and server-sent events |
| Commands and skills: `context: fork`, `allowed-tools`, `argument-hint` | Rate limits, quotas, pricing calculations |
| Plan mode vs direct execution, iterative refinement | OAuth, API key rotation |
| `tool_use` structured output, `tool_choice`, nullable fields | Cloud provider configuration (AWS, GCP, Azure) |
| Few-shot prompting, Message Batches API | Benchmarking and model comparison metrics |
| Context trimming, fact extraction, position-aware ordering | Prompt caching details beyond knowing it exists |
| Human review: calibration, stratified sampling, segmentation | Token counting and tokenization |
| Provenance: claim-source mappings, dates, conflicts, coverage gaps | Language/framework details beyond tool and schema config |

Use the right column to prune study time. A practice question that hinges on vector database internals or cache breakpoints is not a CCAR-F question.

## How the exam is scored

### Criterion-referenced, scaled to 720
*You pass against a fixed standard. Other candidates do not affect your result.*

The exam is a criterion-referenced assessment. Subject matter experts set the cut score in a formal standard-setting study, by judging the performance of a minimally qualified candidate. Scores are scaled to 100–1,000 so that exam forms of slightly different difficulty are equivalent. The cut score is 720.

The score report shows the percentage you answered correctly in each domain. Those section percentages help you study. Only the total scaled score decides pass or fail.

## Registration and policies

| Topic | Rule |
|---|---|
| Eligibility | Registration currently requires a Claude Partner Network company email |
| Registration | Click Register on the Partner Academy certification page, confirm your exam profile, then choose a date, delivery mode, and checkout at Pearson |
| Rescheduling | Online (OnVUE) exams: cancel or reschedule up to 1 hour before. Test center exams: up to 48 hours before. Later changes forfeit the fee. Rescheduling keeps your price |
| ID | Valid, unexpired, government-issued photo ID. The name must match the registration exactly. You can fix your name once in your Partner Academy exam profile; for test centers, do it at least 24 hours ahead |
| Accommodations | Request and get approval from Pearson VUE before you schedule |
| Retakes | Wait 14 days after the first fail, 30 after the second, 90 after the third. Up to 4 attempts per rolling 12 months. Each attempt pays the fee |
| No-show | Fee forfeited; you must re-register |
| Exam conduct | Closed book. No notes, phones, smart watches, headphones, or second monitors. Stay in camera view if online |
| Confidentiality | You accept an NDA before the exam. Exam content is confidential |
| Renewal | Free, non-proctored assessment on the Partner Academy before the credential lapses. A lapsed credential requires the full exam at full fee |
| Appeals | Within 14 days, through Pearson VUE support. Item content and the cut score are not appealable |

## Compared with Architect – Professional

### Foundations vs Professional (comparison only)
*CCAR-F names API parameters. CCAR-P tests governance and stakeholder decisions.*

This course prepares you for Foundations. For orientation only: Foundations tests implementation detail such as `stop_reason`, `tool_choice`, `.mcp.json`, and `-p`. The Professional exam (CCAR-P) names no API parameters and focuses on governance, evaluation, and stakeholder decisions. Do not study Professional materials for this exam.

## How this course maps to the guide

| Course material | Guide section it covers |
|---|---|
| Lessons 01–05 | Section 6, one lesson per domain, every task statement |
| Practice questions (60) | Weighted like Section 4; every item sits in a Section 5 scenario |
| Exercise 00 | Section 9, the twelve official sample questions |
| Exercises 01–04 | Section 8, the four official preparation exercises |
| Lesson 06 | Sections 7 and 10, plus exam-day strategy |
| Flashcards and cheatsheet | All of Section 6 and the Appendix |
