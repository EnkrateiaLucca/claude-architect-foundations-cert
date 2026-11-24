# 00 · Walk the twelve official samples

**Domains:** All · **Time:** 30 min · **Format:** Read, label, check

## Scenario

The official Exam Guide (Section 9) publishes twelve sample questions, three for each of four scenarios. They show how the exam writes items: a production symptom, four plausible fixes, and one proportionate fix at the root cause. Every wrong option falls into a small set of distractor patterns.

## Your task

For each sample below, before you open the walkthrough:

1. Read the stem and find the **trigger cue**: the phrase that tells you which concept the item tests.
2. Predict the answer before you read the options.
3. Label each wrong option with a distractor pattern: Prompt as policy, Over-engineering, Bigger model, Unreliable proxy, Invented feature, or Hide or kill the error. Some wrong options fit none of the six. Write "Wrong layer" or "Wrong target" for those.
4. Name the task statement the item tests.

Then open each walkthrough and compare. Read the full questions and the official explanations in the [Exam Guide PDF](https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf).

## Customer Support Resolution Agent

### Q1 · The agent skips get_customer in 12% of cases
*Answer A: a programmatic prerequisite blocks order and refund calls until get_customer returns a verified ID.*

**Trigger cue:** "misidentified accounts and incorrect refunds". A required tool order with financial consequences needs a deterministic guarantee.

| Option | Pattern | Why it loses |
|---|---|---|
| B. State in the system prompt that verification is mandatory | Prompt as policy | Prompt compliance is probabilistic. The agent already ignores the order 12% of the time. |
| C. Few-shot examples that always call get_customer first | Prompt as policy | Better prompting lowers the failure rate. It cannot make it zero. |
| D. A routing classifier that enables a subset of tools per request | Over-engineering | It controls which tools exist. The problem is the order of calls. |

**Task statement:** 1.4 (programmatic prerequisites). Also 1.5 (hooks for guaranteed compliance).

### Q2 · The agent calls get_customer for order questions
*Answer B: expand each tool's description with input formats, example queries, edge cases, and boundaries.*

**Trigger cue:** "Both tools have minimal descriptions" and "most effective first step". The description is the router, and a first step should be the cheap root-cause fix.

| Option | Pattern | Why it loses |
|---|---|---|
| A. 5–8 few-shot examples of correct routing | Prompt as policy | It patches routing in the system prompt and adds tokens. The tool descriptions stay ambiguous. |
| C. A keyword routing layer that pre-selects the tool | Over-engineering | It bypasses the model's language understanding and adds a component to maintain. |
| D. Merge both tools into one lookup_entity tool | Over-engineering | A valid design, but too much work for a first step. |

**Task statement:** 2.1 (tool descriptions and boundaries).

### Q3 · 55% first-contact resolution against an 80% target
*Answer A: explicit escalation criteria in the system prompt, with few-shot examples of escalate versus resolve.*

**Trigger cue:** "escalates straightforward cases ... while attempting to autonomously handle complex situations". The decision boundary is unclear. This is a judgment call, so criteria plus examples fit, and a hook does not.

| Option | Pattern | Why it loses |
|---|---|---|
| B. Self-reported confidence 1–10 with a threshold | Unreliable proxy | Self-reported confidence is poorly calibrated. The agent is already confident on the wrong cases. |
| C. A classifier trained on historical tickets | Over-engineering | It needs labeled data and ML infrastructure before the cheap prompt fix has been tried. |
| D. Sentiment analysis with auto-escalation | Unreliable proxy | Sentiment does not track case complexity. |

**Task statement:** 5.2 (escalation criteria). Compare with Q1: hard rules go in code, judgment calls go in criteria and examples.

## Code Generation with Claude Code

### Q4 · A /review command for every developer who clones the repo
*Answer A: put the command file in `.claude/commands/` in the repository.*

**Trigger cue:** "available to every developer when they clone or pull". Shared means project scope, under version control.

| Option | Pattern | Why it loses |
|---|---|---|
| B. `~/.claude/commands/` in each home directory | Wrong layer | User scope is personal. Nothing reaches teammates through git. |
| C. The project CLAUDE.md | Wrong layer | CLAUDE.md holds instructions and context. It does not define commands. |
| D. A `commands` array in `.claude/config.json` | Invented feature | This file and mechanism do not exist in Claude Code. |

**Task statement:** 3.2 (slash commands and skills).

### Q5 · Restructure a monolith into microservices
*Answer A: enter plan mode, explore dependencies, and design the approach before changing code.*

**Trigger cue:** "dozens of files" and "decisions about service boundaries". The stem states the complexity up front.

| Option | Pattern | Why it loses |
|---|---|---|
| B. Direct execution, let the boundaries emerge | Wrong target | Late discovery of dependencies causes costly rework. |
| C. Direct execution with detailed upfront instructions | Wrong target | It assumes you know the right structure before you explore the code. |
| D. Start direct, switch to plan mode if it gets hard | Wrong target | The complexity is already known. Waiting for it to appear wastes work. |

**Task statement:** 3.4 (plan mode vs direct execution).

### Q6 · Conventions for test files spread across the codebase
*Answer A: `.claude/rules/` files with YAML `paths` glob patterns.*

**Trigger cue:** "regardless of location" and "automatically". Files that share a type but not a directory need glob-scoped rules.

| Option | Pattern | Why it loses |
|---|---|---|
| B. One root CLAUDE.md with a section per area | Prompt as policy | It relies on Claude to infer which section applies. Inference is not matching. |
| C. One skill per code type | Wrong layer | Skills load on demand. The requirement is automatic application by file path. |
| D. A CLAUDE.md in each subdirectory | Wrong layer | Directory CLAUDE.md files are bound to one directory. Test files live everywhere. |

**Task statement:** 3.3 (path-specific rules).

## Multi-Agent Research System

### Q7 · Every subagent succeeds, the report covers only visual arts
*Answer B: the coordinator's task decomposition is too narrow.*

**Trigger cue:** "each subagent completes successfully" plus the coordinator log that lists three visual-arts subtasks. When every worker succeeds and the output is still incomplete, look at what the workers were assigned.

| Option | Pattern | Why it loses |
|---|---|---|
| A. The synthesis agent lacks gap-detection instructions | Wrong target | Synthesis worked on what it received. The gap started upstream. |
| C. The web search queries are too narrow | Wrong target | Search ran the subtasks it was given. |
| D. Document analysis filters out non-visual sources | Wrong target | Analysis never received music, writing, or film sources to filter. |

**Task statement:** 1.2 (coordinator decomposition and narrow-decomposition risk).

### Q8 · The web search subagent times out
*Answer A: return structured error context: failure type, attempted query, partial results, alternatives.*

**Trigger cue:** "best enables intelligent recovery". The coordinator can only recover with the facts of the failure.

| Option | Pattern | Why it loses |
|---|---|---|
| B. Retry with backoff, then return a generic "search unavailable" | Hide or kill the error | Local retry is fine. The generic status hides what the coordinator needs to decide. |
| C. Return an empty result marked as success | Hide or kill the error | It turns a failure into a false "no results" and blocks any recovery. |
| D. Propagate to a top-level handler that ends the workflow | Hide or kill the error | One failure kills a workflow that partial results could have saved. |

**Task statement:** 5.3 (error propagation). Also 2.2 (structured error responses).

### Q9 · Synthesis needs fact-checks and each costs 2–3 round trips
*Answer A: give the synthesis agent a scoped verify_fact tool for simple checks. Complex checks still go through the coordinator.*

**Trigger cue:** "85% of these verifications are simple fact-checks". Serve the common case with a narrow tool and keep the existing path for the rest.

| Option | Pattern | Why it loses |
|---|---|---|
| B. Batch all verification needs to the end of the pass | Wrong target | Later synthesis steps depend on facts verified earlier. Batching blocks them. |
| C. Give synthesis all web search tools | Over-engineering | It over-provisions the agent and breaks separation of roles. More tools also hurt selection. |
| D. Have search pre-cache extra context | Over-engineering | Speculative caching cannot predict what synthesis will need. |

**Task statement:** 2.3 (tool distribution and scoped cross-role tools).

## Claude Code for Continuous Integration

### Q10 · The CI job hangs waiting for input
*Answer A: add the `-p` flag: `claude -p "Analyze this pull request for security issues"`.*

**Trigger cue:** "hangs indefinitely" and "waiting for interactive input". Non-interactive mode is `-p` (`--print`).

| Option | Pattern | Why it loses |
|---|---|---|
| B. `CLAUDE_HEADLESS=true` | Invented feature | No such environment variable exists. |
| C. Redirect stdin from `/dev/null` | Wrong target | A Unix workaround. It does not use Claude Code's documented non-interactive mode. |
| D. `--batch` flag | Invented feature | No such flag exists. Message Batches is an API feature, not a CLI flag. |

**Task statement:** 3.6 (Claude Code in CI/CD).

### Q11 · Move a pre-merge check and an overnight report to batches
*Answer A: batch the overnight technical-debt report only. Keep real-time calls for the blocking pre-merge check.*

**Trigger cue:** "blocking pre-merge check" versus "generated overnight". Batches give 50% savings with up to 24 hours of processing and no latency SLA.

| Option | Pattern | Why it loses |
|---|---|---|
| B. Batch both and poll for completion | Wrong target | A blocking workflow cannot depend on batches that are often fast but have no SLA. |
| C. Keep real-time for both because of result ordering | Wrong target | A misconception. `custom_id` correlates requests and results. |
| D. Batch both with a timeout fallback to real time | Over-engineering | It adds machinery when matching each workflow to the right API is enough. |

**Task statement:** 4.5 (batch processing).

### Q12 · A 14-file review gives uneven and contradictory feedback
*Answer A: one focused pass per file for local issues, then a separate integration pass for cross-file data flow.*

**Trigger cue:** "detailed feedback for some files but superficial comments for others" and "contradictory feedback". These are symptoms of attention dilution.

| Option | Pattern | Why it loses |
|---|---|---|
| B. Make developers split PRs into 3–4 files | Wrong target | It shifts the burden to developers and leaves the review design unchanged. |
| C. A higher-tier model with a larger context window | Bigger model | A larger window does not fix attention quality across many files. |
| D. Three full passes, flag only issues found twice | Over-engineering | Consensus filtering suppresses real bugs that one pass catches intermittently. |

**Task statement:** 4.6 (multi-pass review). Also 1.6 (per-file plus integration decomposition).

## Reference answer

The answer letter is A in ten of twelve samples. Do not read anything into letters on the live exam. Read the pattern:

| What the stem shows | Proportionate fix |
|---|---|
| A rule that must always hold (money, identity) | Hook or prerequisite gate in code |
| A judgment call made badly | Explicit criteria plus few-shot examples |
| Similar tools confused | Better descriptions, then split or rename |
| Something every teammate needs | Project scope, in version control |
| Files of one type in many directories | `.claude/rules/` with `paths` globs |
| Stated complexity | Plan mode first |
| All workers succeed, output incomplete | Coordinator decomposition |
| A failure the caller must handle | Structured error context with partial results |
| Hangs in CI | `-p` |
| Work that can wait | Message Batches API |
| Uneven depth across many files | Per-file passes plus an integration pass |

## Check yourself

- You found the trigger cue before you read the options in at least ten of twelve.
- You can say why each "Prompt as policy" option fails in Q1 and why the prompt-based answer wins in Q3.
- You can name the invented features: `.claude/config.json` commands, `CLAUDE_HEADLESS`, `--batch`.
- You can map each sample to one task statement without looking.
