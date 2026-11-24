# D5 · Context Management & Reliability

**15% of the exam · ≈ 9 items · 6 task statements · Scenarios:** Customer Support Resolution Agent, Multi-Agent Research System, Code Generation with Claude Code, Structured Data Extraction

This domain tests how a system keeps the right information in front of the model and how it behaves when something goes wrong. Items cover summaries that lose amounts and dates, long sessions that drift, escalation calls, error propagation between agents, human review routing, and source attribution in research reports.

The decision rule: keep facts, sources, and errors explicit and structured. Persist the facts that matter outside summarized history. Pass errors with enough context to recover. Route uncertain work to humans based on calibrated signals.

## Task statements

1. **5.1** Manage conversation context to preserve critical information across long interactions
2. **5.2** Design effective escalation and ambiguity resolution patterns
3. **5.3** Implement error propagation strategies across multi-agent systems
4. **5.4** Manage context effectively in large codebase exploration
5. **5.5** Design human review workflows and confidence calibration
6. **5.6** Preserve information provenance and handle uncertainty in multi-source synthesis

## Core concepts

### Keep a case facts block outside summarized history
*Summaries blur amounts, dates, and promises. Persist transactional facts separately.*

Progressive summarization condenses long conversations. It tends to turn "$247.83 refund promised by March 14 for order #8812" into "customer discussed a refund." Numbers, percentages, dates, and customer-stated expectations get lost first.

Extract transactional facts into a persistent block and include it in every prompt, outside the summarized history:

```xml
<case_facts>
customer_id: C-20417 (verified)
issue_1: order #8812, damaged item, refund $247.83 approved, ETA 2026-03-14
issue_2: order #8840, late delivery, status: investigating
customer_expectation: refund before March 14; wants email confirmation
</case_facts>
<conversation_summary>...</conversation_summary>
```

For multi-issue sessions, keep each issue's structured data (order ID, amount, status) in its own entry in that layer.

Each API request must carry the complete conversation history the model needs. The API does not remember earlier requests.

Task statements: 5.1

### Trim tool output and order inputs for attention
*40 fields per lookup when 5 matter wastes context. Put key findings first.*

Tool results accumulate in context and consume tokens out of proportion to their relevance. An order lookup that returns 40+ fields fills the context fast when a return decision needs five of them.

| Problem | Fix |
|---|---|
| Verbose tool results pile up | Trim each result to the relevant fields before it enters context (for a return: order ID, items, delivery date, amount, return window) |
| Lost in the middle: models process the start and end of long inputs reliably and may omit the middle | Put a key findings summary at the beginning; organize details under explicit section headers |
| Downstream agent has a small context budget | Change the upstream agent to return structured data (key facts, citations, relevance scores) instead of verbose content and reasoning chains |
| Synthesis lacks context about each finding | Require subagents to include metadata: dates, source locations, methodological context |

Task statements: 5.1

### When to escalate and when to resolve
*Escalate on explicit requests, policy gaps, and lack of progress. Sentiment and self-rated confidence are poor triggers.*

| Situation | Do |
|---|---|
| Customer explicitly asks for a human | Escalate immediately. Do not investigate first |
| Customer is frustrated, issue is straightforward and within the agent's capability | Acknowledge the frustration and offer to resolve. Escalate if the customer repeats the request for a human |
| Policy is ambiguous or silent on the request (competitor price match when policy covers only own-site adjustments) | Escalate |
| The agent cannot make meaningful progress | Escalate |
| A lookup returns several matching customers | Ask for an additional identifier. Do not pick one by heuristic |

Escalation triggers are policy exceptions and gaps. Complexity alone is not a trigger.

Sentiment analysis and self-reported confidence scores are unreliable proxies for case complexity. A calm customer can have a policy exception. An angry customer can have a simple damaged-item replacement.

Put explicit escalation criteria with few-shot examples in the system prompt:

```xml
<escalation_criteria>
Escalate when: the customer asks for a human; the policy does not cover the request;
you cannot make progress after verifying the account and order.
Resolve when: the request matches a documented policy (damaged item with photo evidence,
return inside 30 days), even if the customer is upset.
</escalation_criteria>
<example>
Customer: "This is the third broken mug, I'm furious." Photo attached, order is 5 days old.
Action: resolve. Apologize, process the replacement under the damaged-item policy.
Why: policy covers it. Frustration alone is not a reason to escalate.
</example>
```

Task statements: 5.2

### Propagate errors the coordinator can act on
*Failure type, attempted query, partial results, alternatives. Never hide the error or kill the workflow.*

A coordinator can recover only if subagents tell it what happened.

```json
{
  "status": "error",
  "failure_type": "timeout",
  "attempted_query": "EU battery recycling regulations 2026",
  "partial_results": [{"claim": "...", "source_url": "https://..."}],
  "alternatives": ["narrow query to Germany and France", "use document_analysis on the cached EU report"]
}
```

| Approach | Verdict |
|---|---|
| Structured error context as above | Right. The coordinator can retry, rephrase, try another source, or proceed with partial results |
| Generic "search unavailable" after retries | Wrong. It hides the context the coordinator needs |
| Catch the timeout and return an empty result marked as success | Wrong. It suppresses the error and produces silently incomplete research |
| Let the exception terminate the whole workflow | Wrong. One failure kills work that could have recovered |

**Access failure vs valid empty result.** A timeout is an access failure that needs a retry decision. A successful query with zero matches is a valid result. Report them differently so the coordinator does not retry a correct empty answer or trust a failed one.

**Local recovery first.** Subagents retry transient failures themselves. They propagate only errors they cannot resolve, along with what they attempted and any partial results.

**Coverage annotations.** The synthesis output states which findings are well supported and which topic areas have gaps because sources were unavailable.

Task statements: 5.3

### Context in long codebase exploration
*Scratchpad files, subagents for discovery, phase summaries, manifests, and /compact.*

In extended sessions the model starts giving inconsistent answers and refers to "typical patterns" instead of the specific classes it found earlier. That is context degradation.

| Technique | How it works |
|---|---|
| Scratchpad file | The agent writes key findings to a file (for example `notes/exploration.md`) and rereads it for later questions |
| Subagent delegation | Spawn subagents for specific questions ("find all test files", "trace refund flow dependencies"). The main agent keeps the high-level picture |
| Phase summaries | Summarize the findings of one exploration phase, then inject that summary into the initial context of the next phase's subagents |
| Crash recovery manifest | Each agent exports its state to a known location. On resume, the coordinator loads the manifest and injects the state into agent prompts |
| `/compact` | Reduces context usage when verbose discovery output fills the window |

```json
{
  "run_id": "refund-audit-0412",
  "agents": {
    "test_mapper":  {"status": "done",    "state_file": "state/test_mapper.json"},
    "flow_tracer":  {"status": "running", "state_file": "state/flow_tracer.json", "last_step": 7}
  }
}
```

Task statements: 5.4

### Human review and confidence calibration
*97% overall can hide a weak segment. Calibrate field-level confidence on labeled data.*

An aggregate accuracy figure can mask poor performance on one document type or one field. A 97% overall score may include handwritten forms at 70%.

| Step | Purpose |
|---|---|
| Measure accuracy by document type and by field | Confirm every segment performs before you reduce human review |
| Have the model output field-level confidence scores | Gives a per-field routing signal |
| Calibrate thresholds on a labeled validation set | Raw model confidence is not calibrated until you check it against ground truth |
| Stratified random sampling of high-confidence extractions | Measures the ongoing error rate and catches novel error patterns |
| Route low-confidence fields and ambiguous or contradictory source documents to humans | Spends limited reviewer capacity where errors are likely |

```json
{"vendor_name": {"value": "Acme GmbH", "confidence": 0.98},
 "tax_id":      {"value": "DE81234567", "confidence": 0.62}}
```

With a threshold of 0.80 calibrated on labeled data, `tax_id` goes to a reviewer and `vendor_name` does not.

Task statements: 5.5

### Preserve provenance through synthesis
*Claim-source mappings, dates on every finding, conflicts annotated, content rendered by type.*

Summarization steps lose attribution when they compress findings without keeping the link between each claim and its source. Require structured claim-source mappings and make the synthesis agent preserve and merge them.

```json
{
  "claim": "Global e-bike sales grew 18% in 2025.",
  "evidence_excerpt": "…sales rose 18 percent year over year…",
  "source_url": "https://example.org/micromobility-2025",
  "document_name": "Micromobility Market Report 2025",
  "publication_date": "2026-02-10"
}
```

| Situation | Do |
|---|---|
| Two credible sources give different statistics | Keep both values with attribution and annotate the conflict. Let the coordinator decide how to reconcile before synthesis |
| Figures differ because they come from different years | Require publication or data collection dates so a temporal difference is not read as a contradiction |
| Some findings are settled, others disputed | Use separate report sections for well-established and contested findings, with original source characterizations and methodological context |
| Mixed content types | Financial data as tables, news as prose, technical findings as structured lists |

Task statements: 5.6

## Traps

| Wrong option sounds like | Pattern | Why it loses | Right move |
|---|---|---|---|
| "Summarize older turns more aggressively to save tokens" | Lossy shortcut | Amounts, dates, and promises vanish | Persistent case facts block |
| "Escalate when sentiment drops below a threshold" | Unreliable proxy | Sentiment does not track case complexity | Explicit criteria with few-shot examples |
| "Escalate when the agent's self-rated confidence is under 7" | Unreliable proxy | Self-reported confidence is poorly calibrated | Policy-gap and request-based triggers |
| "Investigate first, then offer a human if still needed" after an explicit request | Wrong trigger | The customer already asked | Escalate immediately |
| "Pick the customer with the most recent order" | Wrong lever | Heuristic selection risks the wrong account | Ask for another identifier |
| "Return an empty result set marked successful" | Hide or kill the error | The coordinator cannot recover | Structured error with partial results |
| "Terminate the workflow on the first timeout" | Hide or kill the error | Recoverable work is lost | Local retry, then structured propagation |
| "97% accuracy, so remove human review" | Unreliable proxy | Aggregates hide weak segments | Accuracy by document type and field first |
| "Choose the more recent statistic and drop the other" | Lossy shortcut | Loses a credible source and its attribution | Report both, annotate the conflict |

## Self-check

### After 30 turns the support agent forgets the refund amount it promised. What structure fixes this?
A persistent case facts block with amounts, dates, order numbers, and statuses, included in every prompt outside the summarized history.

### A customer writes "I want to talk to a person" in the first message. The issue looks simple. What does the agent do?
Escalate immediately without investigating first.

### The policy covers price adjustments on your own site. A customer asks you to match a competitor's price. Resolve or escalate?
Escalate. The policy is silent on competitor price matching, which is a policy gap.

### `get_customer` returns three customers named "Maria Lopez". What next?
Ask the customer for an additional identifier, such as email or order number.

### What is the difference between an access failure and a valid empty result, and why does it matter?
An access failure (timeout) means the query did not complete and needs a retry decision. A valid empty result means the query succeeded and found nothing. Mixing them causes wasted retries or false confidence.

### Late in a long exploration session, Claude starts describing "typical repository patterns" instead of the classes it found. Name two fixes.
Write key findings to a scratchpad file and reread it. Delegate specific questions to subagents. `/compact` also helps when verbose discovery output fills the context.

### Extraction accuracy is 97% overall. Is it safe to stop human review of high-confidence output?
Not yet. Check accuracy by document type and field, calibrate confidence thresholds on a labeled set, and keep stratified sampling of high-confidence output.

### Two credible reports give different market sizes for the same year. What should the synthesis contain?
Both values with their sources, annotated as a conflict, in a section for contested findings.
