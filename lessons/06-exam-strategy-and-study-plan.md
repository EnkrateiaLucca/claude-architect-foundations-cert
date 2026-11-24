# Exam Strategy and Study Plan

This lesson covers how to work through the 60 items in 120 minutes, how to read a stem for its trigger, the six distractor patterns, a three-week plan weighted by the blueprint, and the official prep path.

## Pace and method

### Two minutes per item
*Item 20 at 40 minutes, item 40 at 80, item 60 at 120.*

The exam gives 120 minutes for 60 items, which is 2 minutes per item.

| Checkpoint | Target elapsed time |
|---|---|
| Item 20 | 40 min |
| Item 40 | 80 min |
| Item 60 | 120 min |

Flag any item that passes 3 minutes, choose your best answer, and move on. Come back to flagged items at the end. Plan for about 135 minutes of seat time, which includes check-in, instructions, and a short survey.

### Read the stem in the right order
*Last sentence first, predict the answer, then read the options.*

1. Read the last sentence of the stem first. It tells you what is being asked: the root cause, the most effective first step, or where a file goes.
2. Read the scenario and find the trigger phrase (see the table below).
3. Predict the answer before you look at the options.
4. Read all options. Pick the one that matches your prediction and fixes the root cause in proportion to the problem.

Watch for qualifiers. "Most effective first step" favors the cheap, high-leverage fix. "Guaranteed" or "must always" favors code over prompts.

### Multiple-response items
*Treat each option as its own true/false question.*

Multiple-response items state how many responses to select. Judge each option on its own as true or false for the scenario, then select exactly the stated number. Assume all-or-nothing scoring and give no partial credit to yourself in practice.

## Read the trigger, not the options

### Cue → answer table
*Most stems contain a phrase that points straight at the tested concept.*

| Cue in the stem | Points to |
|---|---|
| "financial", "must always", "guaranteed" | Hook or prerequisite gate |
| "minimal descriptions", "similar tools" | Rewrite or split tool descriptions |
| "every developer who clones" | `.claude/commands/`, project CLAUDE.md |
| "regardless of location" | `.claude/rules/` with globs |
| "dozens of files", "service boundaries" | Plan mode |
| "hangs", "waiting for input" | `-p` |
| "overnight", "not blocking" | Message Batches API |
| "inconsistent depth", "contradictory" | Per-file + integration passes |
| "all subagents succeeded, still incomplete" | Coordinator decomposition |
| "absent from the source" | Nullable field, not a retry |

## Six distractor patterns

### The wrong options repeat
*Each pattern comes from wrong options in the twelve official samples.*

| Pattern | Sounds like |
|---|---|
| Prompt as policy | "Make it mandatory in the system prompt." |
| Over-engineering | "Add a routing classifier." "Train a model on old tickets." |
| Bigger model | "Higher-tier model with a larger context window." |
| Unreliable proxy | "Self-reported confidence 1–10." "Sentiment analysis." |
| Invented feature | `CLAUDE_HEADLESS=true` · `--batch` · `.claude/config.json` |
| Hide or kill the error | "Return empty as success." "Terminate the workflow." |

The right answer is the proportionate fix at the root cause. The guide's explanations use the phrases "root cause" and "proportionate first response" again and again. When an option needs new infrastructure before the cheap fix has been tried, it is usually wrong.

## Three-week plan

### Weighted by the blueprint
*Spend time where the points are. Build the four prep exercises yourself.*

| Week | Domains | Do |
|---|---|---|
| 1 | D1 · D2 (45%) | Prep exercises 1 + 4 · API + MCP courses · samples 1–3, 7–9 |
| 2 | D3 · D4 (40%) | Prep exercises 2 + 3 · Claude Code course · samples 4–6, 10–12 |
| 3 | D5 + review (15%) | Re-read all 30 task statements · redo all 12 samples timed |

In week 3, walk each task statement's "Skills in" list and explain how you would perform each skill in one sentence. Any skill you cannot explain is a gap. Then take the 60-question practice bank under timed conditions and review every miss by its distractor pattern.

The guide's sample questions come from the scenarios that the four prep exercises cover, so building the exercises is the highest-value preparation.

## The official prep path

### From the exam guide (Section 7)
*Hands-on building is the preparation.*

- Build an agent with the Claude Agent SDK: a complete agentic loop with tool calling, error handling, and session management. Spawn subagents and pass context between them.
- Configure Claude Code for a real project: a CLAUDE.md hierarchy, path-specific rules in `.claude/rules/`, custom skills with `context: fork` and `allowed-tools`, and at least one MCP server.
- Design and test MCP tools: descriptions that separate similar tools, structured error responses with categories and retryable flags, and tool selection tests with ambiguous requests.
- Build a structured data extraction pipeline: `tool_use` with JSON schemas, validation-retry loops, optional and nullable fields, and the Message Batches API.
- Practice prompt engineering: few-shot examples for ambiguous scenarios, explicit review criteria, and multi-pass review for large code reviews.
- Study context management: structured fact extraction from verbose tool output, scratchpad files, and subagent delegation.
- Review escalation and human-in-the-loop patterns: when to escalate and how to route human review by confidence.

### Free prep courses on the Partner Academy
*Prioritize the API, MCP, and Claude Code courses.*

The [Claude Certified Architect – Foundations Prep Courses](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses) page lists seven free courses:

| Course | Priority |
|---|---|
| Building with the Claude API | High (D1, D2, D4) |
| Introduction to Model Context Protocol | High (D2) |
| Claude Code in Action | High (D3) |
| AI Fluency: Framework & Foundations | Background |
| Claude 101 | Background |
| Claude with Amazon Bedrock | Only if you deploy there |
| Claude on Google Cloud | Only if you deploy there |

Cloud provider configuration is out of scope for the exam.

## If you remember seven things

### Seven takeaways
*Every official sample reduces to one of these.*

1. **Loop on `stop_reason`.** `"tool_use"` continues, `"end_turn"` stops. Never parse text.
2. **Subagents know only what you pass them.** Paste findings in. Fan out in one response.
3. **Hard rules go in hooks, not prompts.** Judgment calls go in criteria + examples.
4. **The description is the router.** Fewer, sharper tools. Structured, categorized errors.
5. **Put config at the right layer.** Project vs user. Rules by glob. `-p` in CI.
6. **Schema-valid isn't correct.** Nullable fields, targeted retries, batch what can wait.
7. **Keep facts, sources, and errors explicit.** Case facts, provenance, coverage gaps, human routing.

## Resources

### Official exam resources
*The exam guide is the authoritative reference.*

- [Claude Certified Architect – Foundations Exam Guide v1.1 (PDF)](https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf)
- [Partner Academy: Earn your Claude certification](https://anthropic-partners.skilljar.com/page/partner-certifications)
- [Partner Academy: Foundations prep courses](https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses)
- [Partner Academy: Certification FAQ](https://anthropic-partners.skilljar.com/page/faq-certifications)
- [Partner Academy: Certification policies](https://anthropic-partners.skilljar.com/page/policies-certifications)

### Anthropic documentation
*Read the pages behind the task statements you find weakest.*

| Topic | Domains | Page |
|---|---|---|
| Agent SDK overview, subagents, hooks, sessions | D1, D2 | [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) |
| Tool use and `tool_choice` | D2, D4 | [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) |
| MCP in Claude Code (`.mcp.json`, scopes) | D2, D3 | [Claude Code MCP](https://code.claude.com/docs/en/mcp) |
| CLAUDE.md, `@import`, `.claude/rules/` | D3 | [Claude Code memory](https://code.claude.com/docs/en/memory) |
| Skills and slash commands | D3 | [Claude Code skills](https://code.claude.com/docs/en/skills) |
| Non-interactive mode (`-p`, `--output-format`) | D3 | [Claude Code headless](https://code.claude.com/docs/en/headless) |
| Message Batches API | D4 | [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing) |
| Workflow and agent patterns | D1 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) |

Platform details change faster than the exam guide. When the docs and the guide disagree, answer exam items the way the guide describes.
