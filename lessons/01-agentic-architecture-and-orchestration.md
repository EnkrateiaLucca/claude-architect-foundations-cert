# D1 · Agentic Architecture & Orchestration

**27% of the exam · ≈ 16 items · 7 task statements · Scenarios:** Customer Support Resolution Agent, Multi-Agent Research System, Developer Productivity with Claude

D1 is the heaviest domain. It tests how you build the control flow around Claude: the agentic loop, coordinators and subagents, enforcement of required steps, hooks, task decomposition, and sessions. Most items describe a working system with one reliability problem and ask for the fix.

The core decision rule: code owns control flow and hard rules, and Claude owns judgment. When a step must always happen, enforce it in code. When a step needs reasoning about context, let the model decide and give it what it needs to decide well.

## Task statements

1. **1.1** Design and implement agentic loops for autonomous task execution
2. **1.2** Orchestrate multi-agent systems with coordinator-subagent patterns
3. **1.3** Configure subagent invocation, context passing, and spawning
4. **1.4** Implement multi-step workflows with enforcement and handoff patterns
5. **1.5** Apply Agent SDK hooks for tool call interception and data normalization
6. **1.6** Design task decomposition strategies for complex workflows
7. **1.7** Manage session state, resumption, and forking

## Core concepts

### The agentic loop runs on stop_reason
*Continue on "tool_use". Stop on "end_turn". Never parse the text.*

The loop has four steps. Send the request to Claude. Inspect `stop_reason`. If it is `"tool_use"`, execute the requested tools and append the results to the conversation. Repeat until `stop_reason` is `"end_turn"`.

```python
messages = [{"role": "user", "content": user_request}]
while True:
    resp = client.messages.create(model=MODEL, max_tokens=4096,
                                  system=SYSTEM, tools=TOOLS, messages=messages)
    messages.append({"role": "assistant", "content": resp.content})
    if resp.stop_reason != "tool_use":          # "end_turn": the model is done
        break
    results = [
        {"type": "tool_result", "tool_use_id": b.id, "content": run_tool(b.name, b.input)}
        for b in resp.content if b.type == "tool_use"
    ]
    messages.append({"role": "user", "content": results})
```

Tool results go back into the conversation history. The model reads them on the next iteration and reasons about the next action. That is model-driven decision-making: Claude picks the next tool from context. A pre-configured decision tree fixes the tool sequence in code instead.

| Anti-pattern | Why it fails |
|---|---|
| Parse the reply for "done" or "task complete" | Natural language is not a control signal. Phrasing varies |
| An iteration cap as the primary stop | It cuts off valid work. Keep a cap only as a safety net |
| "The reply has text, so it's finished" | Claude can return text and `tool_use` blocks in the same response |
| Drop tool results between iterations | The model loses the information it asked for and repeats calls |

Task statements: 1.1

### Hub-and-spoke: the coordinator routes everything
*One coordinator decomposes, delegates, aggregates, and handles errors.*

In a hub-and-spoke system, the coordinator manages all communication between subagents. Subagents never talk to each other directly. That routing gives you observability, consistent error handling, and controlled information flow.

| Coordinator job | What good looks like |
|---|---|
| Decompose | Split the topic so every relevant area gets covered |
| Select | Invoke only the subagents the query needs. A simple query skips the full pipeline |
| Partition | Give each subagent a distinct subtopic or source type to minimize duplication |
| Aggregate | Merge results and check them against the goal |
| Refine | Evaluate the synthesis for gaps, re-delegate targeted queries, re-run synthesis until coverage is sufficient |

The classic failure is narrow decomposition. Every subagent succeeds and the report still misses half the topic. If the coordinator split "AI in creative industries" into three visual-arts subtasks, no downstream agent can recover music, writing, or film. Look at the coordinator's assignments first when all subagents report success.

Task statements: 1.2

### Subagents start with only what you pass them
*Spawn with the Task tool. Paste prior findings into the prompt.*

The `Task` tool spawns subagents. A coordinator can call it only if its `allowedTools` includes `"Task"`. Each subagent type has an `AgentDefinition` with a description, a system prompt, and tool restrictions.

Subagents run with isolated context. They do not inherit the coordinator's conversation history, and they share no memory between invocations. Anything a subagent needs goes into its prompt explicitly.

| Need | Do this |
|---|---|
| Synthesis needs search and analysis results | Include the complete findings in the synthesis subagent's prompt |
| Attribution must survive the handoff | Pass structured data that separates content from metadata (URL, document name, page) |
| Run three searches at once | Emit three `Task` calls in one coordinator response. Separate turns run them serially |
| Subagents must adapt to what they find | Give goals and quality criteria. Avoid step-by-step procedures |

```json
{"findings": [
  {"claim": "Streaming royalties fell 12% in 2025",
   "excerpt": "...royalty payouts declined 12 percent...",
   "source_url": "https://example.org/report", "page": 14, "published": "2026-02-01"}
]}
```

Docs note: newer Agent SDK releases name the subagent tool `Agent`. The exam guide uses `Task`, so answer with `Task`.

Task statements: 1.3

### Enforce required steps in code
*Prompt instructions have a non-zero failure rate. Prerequisite gates do not.*

Workflow ordering can be guided by the prompt or enforced by code. When compliance must be deterministic, for example identity verification before a financial operation, a prompt alone is not enough. The guide states that prompt instructions alone have a non-zero failure rate.

A programmatic prerequisite blocks downstream tool calls until the prerequisite step has completed.

```python
def gate(tool_name: str, state: dict) -> str | None:
    if tool_name in {"lookup_order", "process_refund"} and not state.get("verified_customer_id"):
        return "Blocked: call get_customer and verify the customer first."
    return None
```

| Requirement | Prompt guidance enough? | Mechanism |
|---|---|---|
| Greet the customer by name | Yes | System prompt |
| Prefer the order ID over the email when both exist | Yes | Tool descriptions, few-shot |
| Verify identity before any refund | No | Prerequisite gate |
| Never refund above a limit | No | Tool-call interception hook |

Task statements: 1.4

### Multi-concern requests and human handoffs
*Split the request into items. Hand humans a summary that stands alone.*

A message like "my order arrived broken and I was charged twice" holds two concerns. Decompose it into distinct items. Investigate each, in parallel where possible, using shared context such as the verified customer record. Then synthesize one unified resolution.

When the agent escalates mid-process, the human agent does not see the transcript. The handoff must be a structured summary that stands on its own.

| Field | Example |
|---|---|
| Customer ID | `C-48213` (verified) |
| Issue(s) | Damaged item on order #A-7731; duplicate charge on invoice 9902 |
| Root cause | Carrier damage confirmed by photo; payment gateway retried once |
| Amount | $642.10 refund requested |
| Recommended action | Approve refund above the $500 limit; reverse duplicate charge |

Task statements: 1.4

### Hooks: intercept calls and normalize results
*PreToolUse-style interception blocks violations. PostToolUse transforms results.*

Agent SDK hooks run deterministic code around tool calls.

| Hook pattern | When it runs | Typical use |
|---|---|---|
| Tool call interception | Before the tool executes | Block a refund over $500 and redirect to human escalation |
| `PostToolUse` | After the tool returns, before the model sees the result | Normalize Unix timestamps, ISO 8601 strings, and numeric status codes into one format |

```python
def before_tool(name: str, args: dict):
    if name == "process_refund" and args["amount"] > 500:
        return {"block": True,
                "message": "Refunds over $500 require a human. Call escalate_to_human."}

def post_tool_use(name: str, result: dict) -> dict:
    if "created" in result and isinstance(result["created"], int):
        result["created"] = datetime.fromtimestamp(result["created"], UTC).isoformat()
    return result
```

Choose a hook over a prompt instruction whenever a business rule requires guaranteed compliance. Hooks give deterministic guarantees. Prompts give probabilistic compliance.

Task statements: 1.5

### Fixed pipelines vs adaptive decomposition
*Predictable work gets prompt chaining. Open-ended work gets a plan that adapts.*

| Workflow shape | Pattern | Example |
|---|---|---|
| Same steps every time, multiple aspects | Prompt chaining (fixed sequential passes) | Review each file, then run a cross-file integration pass |
| Steps depend on what you find | Dynamic adaptive decomposition | Investigate a production bug across services |
| Large code review | Per-file local passes plus one integration pass | Avoids attention dilution and contradictory findings |
| "Add comprehensive tests to a legacy codebase" | Map structure, find high-impact areas, make a prioritized plan, adapt as dependencies appear | Coverage grows where risk is highest |

An adaptive investigation plan generates subtasks from what each step discovers. A fixed pipeline cannot react to a surprise, and that is its point for predictable work.

Task statements: 1.6

### Resume, fork, or start fresh
*Resume when prior context is valid. Start fresh with a summary when it is stale.*

| Situation | Choose |
|---|---|
| Continue yesterday's named investigation | `--resume <session-name>` |
| Compare two refactoring or testing strategies from one analysis | `fork_session` to create independent branches |
| Files changed since the last session | Resume and tell the agent which files changed, for targeted re-analysis |
| Prior tool results are stale or misleading | New session with an injected structured summary |

Resuming with stale tool results leaves old file contents in context, and the agent reasons from them. A fresh session seeded with a structured summary is more reliable in that case. When most context is still valid, resume and name the specific changes. Full re-exploration wastes time.

Task statements: 1.7

## Traps

| Wrong option sounds like | Pattern | Why it loses | Right move |
|---|---|---|---|
| "Make verification mandatory in the system prompt" | Prompt as policy | Probabilistic compliance on a financial step | Prerequisite gate in code |
| "Add few-shot examples showing get_customer first" | Prompt as policy | Still probabilistic | Gate or hook |
| "Stop when the reply contains 'done'" | Invented control signal | Text is not a stop condition | Loop on `stop_reason` |
| "Cap the loop at 5 iterations" | Wrong stopping mechanism | Cuts off valid work | `end_turn` stops; cap is a safety net |
| "Subagents can read the coordinator's history" | Invented feature | Subagent context is isolated | Pass findings in the prompt |
| "Fix the search agent's queries" when the coordinator's plan was narrow | Blame downstream | Subagents did their assigned work | Broaden the coordinator's decomposition |
| "Spawn each subagent in a separate turn" | Slow by design | Serial execution | Multiple `Task` calls in one response |
| "Give the coordinator a step-by-step procedure for each subagent" | Over-specification | Subagents cannot adapt | Goals plus quality criteria |
| "Resume the session" after major code changes | Stale context | Old tool results mislead | Fresh session with a summary, or resume and name the changes |

## Self-check

### What should the loop do when stop_reason is "tool_use"?
Execute each requested tool, append the results as `tool_result` blocks in a user message, and call Claude again. Stop only on `"end_turn"`.

### A coordinator cannot spawn subagents. What configuration is missing?
Its `allowedTools` must include `"Task"`.

### How does a synthesis subagent see the web search results?
The coordinator includes the complete findings in the synthesis subagent's prompt. Subagents inherit nothing automatically.

### How do you run three research subagents in parallel?
Emit three `Task` tool calls in a single coordinator response.

### Refunds above $500 must always go to a human. Where does that rule live?
In a tool-call interception hook that blocks `process_refund` above the threshold and redirects to `escalate_to_human`.

### Two MCP tools return dates as Unix timestamps and ISO 8601 strings. How do you give the agent one format?
A `PostToolUse` hook normalizes the results before the model processes them.

### What must a human handoff summary contain, and why?
Customer ID, root cause, amount, and recommended action. The human agent has no access to the transcript.

### When do you start a new session instead of using --resume?
When the prior tool results are stale. Start fresh and inject a structured summary of what still holds.
