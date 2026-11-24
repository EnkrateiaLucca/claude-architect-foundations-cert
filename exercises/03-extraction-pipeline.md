# 03 · Build a structured data extraction pipeline

**Domains:** D4, D5 · **Time:** 30 min · **Format:** Design drill + runnable script (`exercises/scripts/extraction_pipeline.py`)

## Scenario

Structured Data Extraction. Finance receives 4,000 supplier invoices a week as text and PDF. Each needs vendor, invoice number, date, category, line items, and total in JSON for the accounting system. Some invoices have no invoice number. Some print a total that does not match the line items. Categories change as new supplier types appear. The accounting team needs results within 30 hours of receipt. A human review team can check about 200 invoices a week.

This drill follows Exercise 3 in Section 8 of the official Exam Guide.

## Your task

1. Design the extraction schema. Which fields are required, which are nullable, and how do you handle new categories?
2. How do you guarantee the model returns schema-valid JSON instead of prose?
3. List two errors a strict schema cannot catch. How do you catch them?
4. Validation fails. What goes into the retry request? Which failures will a retry not fix?
5. Some invoices cite amounts as "approx. 1.2k" or "EUR 1.240,00". What do you add to the prompt?
6. Choose the API for the weekly volume and say how often you submit to meet the 30-hour SLA. How do you handle failed requests?
7. Accuracy on a labeled sample is 97%. Finance wants to stop human review. What do you check first, and how do you spend the 200 weekly reviews?
8. Run the self-test and find each answer in the code.

```bash
uv run exercises/scripts/extraction_pipeline.py --selftest
uv run exercises/scripts/extraction_pipeline.py invoice.txt          # needs ANTHROPIC_API_KEY
uv run exercises/scripts/extraction_pipeline.py --batch invoices/*.txt
```

## Reference answer

### Schema design
*Nullable for anything the source may lack. Enum with "other" + detail, and "unclear" for ambiguity.*

| Field | Type | Why |
|---|---|---|
| `vendor_name` | string, required | Every invoice has one |
| `invoice_number` | string or null | Some invoices have none. A required non-null field pushes the model to invent one |
| `invoice_date` | string (YYYY-MM-DD) or null | Normalized format, null if absent |
| `category` | enum: software, hardware, services, travel, other, unclear | `unclear` for ambiguous documents |
| `category_detail` | string or null | Filled when `category` is `other`, so new categories stay visible |
| `line_items` | array of {description, amount} | |
| `stated_total` | number or null | The total printed on the invoice |
| `calculated_total` | number | Sum of line items, extracted alongside the stated total |
| `conflict_detected` | boolean | True when the two totals differ |

Task statements: 4.3

### Guaranteed structure with tool use
*Define the schema as a tool's input and make the model call it.*

Define `extract_invoice` with the schema as `input_schema` and read the result from the `tool_use` block. Set `tool_choice` so the model must call the tool:

- `{"type": "tool", "name": "extract_invoice"}` forces this specific tool. Use it when one extraction must run before later steps.
- `{"type": "any"}` forces some tool call. Use it when several extraction schemas exist and the document type is unknown.
- `{"type": "auto"}` lets the model answer in text instead.

Docs note: forced `tool_choice` (`any` or `tool`) returns a 400 on the newest models (Claude Opus 5.5, Sonnet 5.5, Fable 5.1+). The script falls back to `auto` with `strict: true` and an explicit instruction on those models. The exam answer stays the forced `tool_choice`.

Task statements: 4.3, 2.3

### Semantic validation
*A schema-valid result can still be wrong.*

Tool use with a strict schema removes JSON syntax errors. It does not catch:

- Line items that do not sum to `calculated_total`.
- A stated total that differs from the calculated total while `conflict_detected` is false.
- `category: "other"` with no `category_detail`.
- Values in the wrong field, such as a date in `invoice_number`.

The script checks these with a Pydantic `model_validator`. Extracting both totals plus a `conflict_detected` flag makes the model report a mismatch in the source instead of hiding it.

Task statements: 4.3, 4.4

### Retry with error feedback
*Send the document, the failed extraction, and the specific errors. Cap the attempts.*

The retry keeps the original document in the conversation, keeps the failed `tool_use`, and answers it with a `tool_result` that has `is_error: true` and the exact validation errors: "calculated_total is 100.0 but line_items sum to 120.0". The script caps retries at three and routes the rest to human review.

Retries fix format mismatches, arithmetic slips, and misplaced values. Retries do not fix missing information. If the purchase order number exists only in a separate document you did not send, the field stays null and the invoice goes to review.

Task statements: 4.4

### Format normalization and few-shot examples
*Put normalization rules in the prompt next to the strict schema. Show varied formats with examples.*

Add rules: "dates as YYYY-MM-DD; amounts as plain numbers without currency symbols or thousands separators; use null when a field is absent". Add 2–4 few-shot examples that show extraction from different layouts: a table of line items, a narrative invoice, a European number format. Examples reduce empty extractions of required fields and invented values on informal formats.

Task statements: 4.2, 4.3

### Batch strategy
*Overnight-tolerant work goes to the Message Batches API. Resubmit only the failures.*

The work does not block anyone, so use the Message Batches API: 50% cost savings, up to 24 hours of processing, no latency SLA. With a 30-hour SLA and up to 24 hours of processing, an invoice can wait at most 6 hours before submission. Submit a batch every 4 hours to keep a margin.

Give every request a `custom_id` (the script uses the file stem). Results arrive in any order, so join them on `custom_id`. Resubmit only the errored or expired IDs. If a document exceeded the context limit, chunk it before resubmitting. Test the prompt on a sample of 50 invoices first so the large batch succeeds on the first pass.

Batches do not support multi-turn tool calling within one request. A single forced extraction call works. A loop that needs tool results mid-request does not.

Task statements: 4.5

### Human review and calibration
*Check accuracy per segment before cutting review. Spend reviews where errors hide.*

97% overall can hide 70% on handwritten invoices or on the `invoice_date` field. Before you reduce review:

1. Measure accuracy by document type and by field on a labeled validation set.
2. Have the model output a confidence score per field. Calibrate the routing threshold on the labeled set, not on the model's raw numbers.
3. Route low-confidence fields, `conflict_detected: true`, and `category: "unclear"` to review first.
4. Spend part of the 200 reviews on a stratified random sample of high-confidence extractions. It measures the real error rate and catches new error patterns.

Task statements: 5.5

## Check yourself

- Every field the source can lack is nullable.
- You can state the difference between `auto`, `any`, and a forced tool choice.
- Your retry request contains the document, the failed output, and the specific errors.
- You can name one failure that no retry fixes.
- You can compute the submission interval from the SLA and the 24-hour batch window.
- You can explain why 97% overall accuracy does not justify ending review.
