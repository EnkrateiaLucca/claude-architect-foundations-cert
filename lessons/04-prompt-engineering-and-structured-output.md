# D4 · Prompt Engineering & Structured Output

**20% of the exam · ≈ 12 items · 6 task statements · Scenarios:** Claude Code for Continuous Integration, Structured Data Extraction

This domain tests how you get precise, consistent, machine-readable output from Claude. Items cover review prompts that produce too many false positives, extraction pipelines that invent values, retries that never succeed, and workloads that belong in the Message Batches API.

The decision rule: replace vague instructions with explicit criteria and targeted examples, enforce shape with `tool_use` and a JSON schema, and validate meaning in code. A valid schema guarantees syntax. It does not guarantee correct values.

## Task statements

1. **4.1** Design prompts with explicit criteria to improve precision and reduce false positives
2. **4.2** Apply few-shot prompting to improve output consistency and quality
3. **4.3** Enforce structured output using tool use and JSON schemas
4. **4.4** Implement validation, retry, and feedback loops for extraction quality
5. **4.5** Design efficient batch processing strategies
6. **4.6** Design multi-instance and multi-pass review architectures

## Core concepts

### Explicit criteria beat vague caution
*Say which issues to report and which to skip. "Be conservative" does not raise precision.*

General instructions such as "be conservative" or "only report high-confidence findings" do not improve precision much. Specific categorical criteria do.

| Vague (fails) | Explicit (works) |
|---|---|
| "Check that comments are accurate" | "Flag a comment only when its claimed behavior contradicts what the code does" |
| "Be conservative" | "Report bugs and security issues. Skip minor style and patterns local to one file" |
| "Only report high-confidence findings" | Define each severity level with a concrete code example |

A severity definition with examples gives consistent classification:

```text
critical: exploitable now. Example: SQL built by string concatenation from request params.
high:     wrong result in a normal path. Example: off-by-one in pagination drops the last item.
medium:   wrong result in an edge case. Example: no handling of an empty list.
low:      do not report.
```

**False positives erode trust in every category.** When one category produces most of the false positives, developers start ignoring accurate findings too. Disable that category temporarily to restore trust while you improve its prompt.

Task statements: 4.1

### Few-shot examples for the ambiguous cases
*2–4 targeted examples that show why one action beat the alternatives.*

When detailed instructions still produce inconsistent output, few-shot examples are the most effective fix. Target them at the cases where the model is unsure, and show the reasoning.

| Goal | What the examples show |
|---|---|
| Consistent format | The exact output shape: location, issue, severity, suggested fix |
| Fewer false positives | An acceptable pattern next to a genuine issue that looks similar |
| Correct handling of ambiguous requests | Which tool or action was chosen and why the plausible alternative was rejected |
| Less hallucination in extraction | Informal measurements ("about two cups"), varied structures (inline citations vs bibliography, methodology section vs embedded details) |
| Fewer empty or null required fields | Correct extraction from documents in several formats |

```xml
<example>
  <code>items.sort(key=lambda x: x.created_at)</code>
  <verdict>No finding. Sorting in place on a local list is intended here.</verdict>
</example>
<example>
  <code>cache.sort(key=lambda x: x.created_at)</code>
  <verdict>high: cache is shared across requests; in-place sort races with readers.
  Suggested fix: sorted(cache, ...).</verdict>
</example>
```

Good examples let the model generalize the judgment to patterns you did not list. Examples that only enumerate cases teach the model to match those cases.

Task statements: 4.2

### tool_use with a JSON schema guarantees shape
*Define an extraction tool, read the `tool_use` block, and pick the right `tool_choice`.*

The most reliable way to get schema-compliant output is to define a tool whose `input_schema` is the shape you want. Claude's tool call arguments are the structured data. This eliminates JSON syntax errors.

```python
extract_invoice = {
    "name": "extract_invoice",
    "description": "Record the fields of one invoice exactly as the document states them.",
    "input_schema": {
        "type": "object",
        "properties": {
            "invoice_number":   {"type": "string"},
            "stated_total":     {"type": "number"},
            "calculated_total": {"type": "number"},
            "due_date":         {"type": ["string", "null"], "description": "ISO 8601. null if absent."},
            "category":         {"enum": ["services", "goods", "other", "unclear"]},
            "category_detail":  {"type": ["string", "null"]},
            "conflict_detected": {"type": "boolean"}
        },
        "required": ["invoice_number", "stated_total", "calculated_total", "category", "conflict_detected"]
    }
}

resp = client.messages.create(
    model=MODEL, max_tokens=1024, tools=[extract_invoice],
    tool_choice={"type": "tool", "name": "extract_invoice"},
    messages=[{"role": "user", "content": document_text}],
)
data = next(b.input for b in resp.content if b.type == "tool_use")
```

| `tool_choice` | Behavior | Use when |
|---|---|---|
| `{"type": "auto"}` | Model may answer in text instead of calling a tool | Conversational agents |
| `{"type": "any"}` | Model must call a tool but chooses which | Several extraction schemas exist and the document type is unknown |
| `{"type": "tool", "name": "extract_metadata"}` | Model must call that tool | One extraction must run before enrichment steps. Run the later steps in follow-up turns |

Docs note: current Anthropic docs say forced tool use (`any` or a named tool) returns a 400 error on the newest models and recommend strict tool use or structured outputs. The exam tests the three `tool_choice` options as listed above.

Task statements: 4.3

### Schema design that keeps the model honest
*Nullable fields for absent data. "unclear" and "other" + detail for categories.*

| Design choice | Why |
|---|---|
| Make a field nullable (`["string", "null"]`) when the source may not contain it | A required non-null field pushes the model to invent a value |
| Add an `"unclear"` enum value | Ambiguous cases get an honest label instead of a guess |
| Add `"other"` plus a `*_detail` string | New categories stay extensible without schema changes |
| Put format normalization rules in the prompt ("dates as YYYY-MM-DD, amounts as numbers without currency symbols") | The schema checks types. It cannot fix inconsistent source formatting |

A strict schema eliminates syntax errors. It does not prevent semantic errors: line items that do not sum to the total, or a value placed in the wrong field. Catch those with validation in code.

Task statements: 4.3

### Validation, retry, and feedback loops
*Retry with the specific error. Do not retry when the data is missing from the source.*

**Retry with error feedback.** When validation fails (Pydantic or JSON Schema), send a follow-up request that includes three things: the original document, the failed extraction, and the specific validation error.

```python
from pydantic import ValidationError

try:
    Invoice.model_validate(data)
except ValidationError as err:
    retry_prompt = (
        f"<document>{document_text}</document>\n"
        f"<previous_extraction>{json.dumps(data)}</previous_extraction>\n"
        f"<validation_errors>{err}</validation_errors>\n"
        "Correct the extraction. Use null for fields the document does not contain."
    )
```

| Failure | Will a retry help? | Do |
|---|---|---|
| Format mismatch (date as "March 3" instead of ISO) | Yes | Retry with the error |
| Structural output error | Yes | Retry with the error |
| Totals do not add up | Sometimes | Extract `calculated_total` beside `stated_total` and flag the gap |
| Inconsistent source data | No | Set `conflict_detected: true` and route for review |
| Information exists only in a document you did not send | No | Return null or route to a human |

**Feedback loops.** Add a `detected_pattern` field to each structured finding, naming the code construct that triggered it. When developers dismiss findings, you can group dismissals by pattern and see which constructs cause false positives.

Task statements: 4.4

### Batch what can wait
*Message Batches API: 50% cheaper, up to 24 hours, no latency SLA, no multi-turn tool calls.*

| | Synchronous Messages API | Message Batches API |
|---|---|---|
| Cost | Standard | 50% savings |
| Latency | Seconds | Up to 24 hours, no guaranteed SLA |
| Multi-turn tool calling within a request | Yes | No. It cannot execute tools mid-request and return results |
| Correlate results | n/a | `custom_id` on each request |
| Fits | Blocking pre-merge checks | Overnight reports, weekly audits, nightly test generation |

```python
batch = client.messages.batches.create(requests=[
    {"custom_id": f"doc-{d.id}",
     "params": {"model": MODEL, "max_tokens": 2048, "tools": [extract_invoice],
                "tool_choice": {"type": "tool", "name": "extract_invoice"},
                "messages": [{"role": "user", "content": d.text}]}}
    for d in docs
])
```

**SLA arithmetic.** Processing can take up to 24 hours. With a 30-hour SLA, a document can wait at most 6 hours before submission. Submitting every 4 hours keeps every document inside the SLA with margin.

**Failures.** Resubmit only the failed requests, identified by `custom_id`. Change what caused the failure, for example by chunking documents that exceeded the context limit.

**Refine first.** Tune the prompt on a sample set before submitting a large batch. A higher first-pass success rate costs less than repeated resubmissions.

Docs note: Anthropic's docs say most batches finish in under an hour. The exam treats the 24-hour window as the planning limit.

Task statements: 4.5

### Independent instances and multi-pass review
*A fresh instance catches what self-review misses. Split big reviews into per-file and integration passes.*

**Self-review is weak.** The model that generated code keeps its reasoning context and is less likely to question its own decisions. Instructions to "review carefully" or extended thinking in the same session do not fix this. A second, independent Claude instance without the generator's context catches more subtle issues.

**Attention dilution.** One pass over many files gives uneven depth and contradictory findings: a pattern flagged in one file and approved in another.

| Pass | Scope | Catches |
|---|---|---|
| Per-file passes | One file at a time | Local bugs, consistent depth on every file |
| Integration pass | Cross-file data flow | Interface mismatches, broken contracts between modules |
| Verification pass | Each finding with a self-reported confidence | Routes low-confidence findings to a human for calibrated review |

Wrong fixes for attention dilution: a bigger context window (the problem is attention quality, and a larger window leaves it unchanged), forcing developers to split PRs (shifts the burden), and flagging only issues found in 2 of 3 runs (suppresses real bugs that show up intermittently).

Task statements: 4.6

## Traps

| Wrong option sounds like | Pattern | Why it loses | Right move |
|---|---|---|---|
| "Tell it to be conservative and report only high-confidence findings" | Prompt as policy | General caution does not raise precision | Explicit report/skip criteria, severity examples |
| "Keep all categories on while you tune the noisy one" | Wrong lever | False positives in one category erode trust in all | Disable the noisy category temporarily |
| "Make every field required so nothing is missing" | Lossy shortcut | The model fabricates values to fill required fields | Nullable fields for data that may be absent |
| "Strict schema means the totals are right" | Unreliable proxy | Schemas stop syntax errors, not semantic ones | Validate in code; compare `calculated_total` to `stated_total` |
| "Retry until the field is filled" | Over-engineering | The value is absent from the source | Return null or route to a human |
| "Move the pre-merge check to the Batches API to save 50%" | Wrong trigger | Batches have no latency SLA; developers are blocked | Sync for blocking checks, batch for overnight |
| "Resubmit the whole batch after failures" | Over-engineering | Wastes cost on requests that succeeded | Resubmit failed `custom_id`s with fixes |
| "Switch to a model with a larger context window" | Bigger model | Larger windows do not fix attention dilution | Per-file passes plus an integration pass |
| "Ask the generator to double-check its own code" | Unreliable proxy | It keeps its reasoning context | Independent review instance |

## Self-check

### A review prompt says "check that comments are accurate" and flags dozens of harmless comments. What do you change?
Replace it with an explicit criterion: flag a comment only when its claimed behavior contradicts the code's actual behavior.

### Detailed instructions still give inconsistent finding formats. What is the most effective fix?
Add 2–4 few-shot examples that show the exact output format (location, issue, severity, suggested fix).

### Your pipeline has three extraction tools and does not know the document type in advance. Which `tool_choice` guarantees a structured result?
`{"type": "any"}`. The model must call a tool and picks the matching schema.

### The model returns a plausible but invented `due_date` for invoices that have none. What schema change helps?
Make `due_date` nullable and tell the model to return null when the document does not contain it.

### A validation retry keeps failing on `po_number`. The PO number appears only in a purchase order that is not in the request. Retry again?
No. Retries cannot recover information missing from the source. Return null or route to a human.

### A 30-hour SLA, 24-hour batch processing. How often should you submit batches?
At least every 6 hours. Every 4 hours gives margin and guarantees the SLA.

### Why does the same Claude session make a poor reviewer of code it just wrote?
It retains the reasoning that produced the code and is less likely to question those decisions. Use an independent instance.

### Developers dismiss many findings and you want to know why. What field do you add?
`detected_pattern`, naming the code construct that triggered each finding, so you can analyze dismissals by pattern.
