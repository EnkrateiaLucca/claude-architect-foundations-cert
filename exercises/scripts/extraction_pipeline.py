# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic>=0.70", "pydantic>=2.7"]
# ///
"""Exercise 03: a structured extraction pipeline for invoices.

Concepts (CCAR-F task statements):
  4.3  extraction tool with a JSON schema: nullable fields, enum with "other" + detail and "unclear",
       a forced tool_choice so the model must call the extraction tool
  4.4  semantic validation with Pydantic (line items must sum, stated vs calculated total) and
       retry-with-error-feedback: the follow-up carries the document, the failed extraction, and the errors
  4.5  Message Batches request builder keyed by custom_id, and resubmission of failed custom_ids only

Run:
  uv run exercises/scripts/extraction_pipeline.py --selftest              # offline, no API key
  uv run exercises/scripts/extraction_pipeline.py invoice1.txt invoice2.txt
  uv run exercises/scripts/extraction_pipeline.py --batch invoices/*.txt  # submit a batch, print its id
  uv run exercises/scripts/extraction_pipeline.py --results msgbatch_...  # list failed custom_ids
Live modes call the Claude API (needs ANTHROPIC_API_KEY).
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from typing import Literal

from pydantic import BaseModel, ValidationError, model_validator

CATEGORIES = ["software", "hardware", "services", "travel", "other", "unclear"]

EXTRACT_TOOL = {
    "name": "extract_invoice",
    "description": "Record the fields of one invoice. Use null for any field the document does not state.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "additionalProperties": False,
        "required": ["vendor_name", "invoice_number", "invoice_date", "category", "category_detail",
                     "line_items", "stated_total", "calculated_total", "conflict_detected"],
        "properties": {
            "vendor_name": {"type": "string"},
            "invoice_number": {"type": ["string", "null"], "description": "null if the document shows none"},
            "invoice_date": {"type": ["string", "null"], "description": "YYYY-MM-DD, or null if absent"},
            "category": {"type": "string", "enum": CATEGORIES,
                         "description": "'unclear' if the document is ambiguous; 'other' plus category_detail if no value fits"},
            "category_detail": {"type": ["string", "null"], "description": "Required when category is 'other'"},
            "line_items": {"type": "array", "items": {
                "type": "object", "additionalProperties": False, "required": ["description", "amount"],
                "properties": {"description": {"type": "string"}, "amount": {"type": "number"}}}},
            "stated_total": {"type": ["number", "null"], "description": "The total printed on the invoice"},
            "calculated_total": {"type": "number", "description": "Sum of line_items amounts"},
            "conflict_detected": {"type": "boolean", "description": "true if stated_total differs from calculated_total"},
        },
    },
}

PROMPT = """Extract the invoice below with the extract_invoice tool.
Normalization rules: dates as YYYY-MM-DD; amounts as plain numbers without currency symbols or thousands separators.
If a field is not in the document, use null. Never invent a value.

<document>
{doc}
</document>"""

# Forced tool_choice returns a 400 on these models. Use auto + strict + an explicit instruction there.
NO_FORCED_TOOL_CHOICE = {"claude-opus-5-5", "claude-sonnet-5-5", "claude-fable-5-1", "claude-fable-5-2",
                         "claude-mythos-5-1", "claude-mythos-5-2"}


def tool_choice_for(model):
    if model in NO_FORCED_TOOL_CHOICE:
        return {"type": "auto"}
    return {"type": "tool", "name": EXTRACT_TOOL["name"]}


class LineItem(BaseModel):
    description: str
    amount: float


class Invoice(BaseModel):
    vendor_name: str
    invoice_number: str | None
    invoice_date: date | None
    category: Literal["software", "hardware", "services", "travel", "other", "unclear"]
    category_detail: str | None
    line_items: list[LineItem]
    stated_total: float | None
    calculated_total: float
    conflict_detected: bool

    @model_validator(mode="after")
    def semantic_checks(self):
        total = round(sum(i.amount for i in self.line_items), 2)
        if abs(total - self.calculated_total) > 0.01:
            raise ValueError(f"calculated_total is {self.calculated_total} but line_items sum to {total}")
        if self.stated_total is not None:
            differs = abs(self.stated_total - self.calculated_total) > 0.01
            if differs != self.conflict_detected:
                raise ValueError(f"conflict_detected must be {str(differs).lower()}: stated_total "
                                 f"{self.stated_total} vs calculated_total {self.calculated_total}")
        if self.category == "other" and not self.category_detail:
            raise ValueError("category is 'other' so category_detail must describe the category")
        return self


def request_params(doc, model):
    return {"model": model, "max_tokens": 4096, "tools": [EXTRACT_TOOL], "tool_choice": tool_choice_for(model),
            "messages": [{"role": "user", "content": PROMPT.format(doc=doc)}]}


def tool_input(response):
    return next((b for b in response.content if b.type == "tool_use"), None)


def extract(client, doc, model, max_attempts=3):
    """Extract, validate, and retry with the specific validation errors. Returns a result dict."""
    params = request_params(doc, model)
    messages = params.pop("messages")
    errors = "model did not call extract_invoice"
    for attempt in range(1, max_attempts + 1):
        response = client.messages.create(messages=messages, **params)
        block = tool_input(response)
        messages.append({"role": "assistant", "content": response.content})
        if block is None:
            messages.append({"role": "user", "content": "Call the extract_invoice tool with the fields."})
            continue
        try:
            return {"status": "ok", "attempts": attempt, "data": Invoice(**block.input).model_dump(mode="json")}
        except ValidationError as e:
            errors = "; ".join(err["msg"] for err in e.errors())
        # The document stays in messages[0]; the failed extraction is the tool_use above; add the errors.
        messages.append({"role": "user", "content": [{
            "type": "tool_result", "tool_use_id": block.id, "is_error": True,
            "content": f"Validation failed: {errors}. Re-read the document and call extract_invoice again "
                       "with corrected values. Keep null for fields the document does not contain."}]})
    # Retries fix format and arithmetic errors. They cannot add information the document lacks.
    return {"status": "needs_review", "attempts": max_attempts, "errors": errors}


# ---------- Message Batches ----------
CUSTOM_ID = re.compile(r"^[a-zA-Z0-9_-]{1,64}$")


def build_batch_requests(docs, model):
    """docs: {custom_id: text}. Batch results come back in any order; custom_id is the only join key."""
    bad = [k for k in docs if not CUSTOM_ID.match(k)]
    if bad:
        raise ValueError(f"invalid custom_id(s): {bad}")
    return [{"custom_id": cid, "params": request_params(doc, model)} for cid, doc in docs.items()]


def failed_custom_ids(results):
    """custom_ids to resubmit: errored, expired, or canceled. Resubmit only these, not the whole batch."""
    return sorted(r.custom_id for r in results if r.result.type != "succeeded")


# ---------- offline self-test ----------
class FakeClient:
    def __init__(self, turns):
        self.turns, self.requests = list(turns), []
        self.messages = self

    def create(self, **kwargs):
        self.requests.append(kwargs)
        return self.turns.pop(0)


def extraction_turn(**fields):
    return SimpleNamespace(stop_reason="tool_use",
                           content=[SimpleNamespace(type="tool_use", id="tu_1", name="extract_invoice", input=fields)])


def selftest():
    base = {"vendor_name": "Acme Hosting", "invoice_number": None, "invoice_date": "2026-10-02",
            "category": "other", "category_detail": "cloud hosting", "stated_total": 120.0,
            "line_items": [{"description": "VM", "amount": 90.0}, {"description": "Backup", "amount": 30.0}]}
    wrong = {**base, "calculated_total": 100.0, "conflict_detected": False}   # arithmetic error
    right = {**base, "calculated_total": 120.0, "conflict_detected": False}
    fake = FakeClient([extraction_turn(**wrong), extraction_turn(**right)])
    out = extract(fake, "ACME HOSTING ... Total $120.00", model="claude-sonnet-5-5")
    assert out["status"] == "ok" and out["attempts"] == 2, out
    assert out["data"]["invoice_number"] is None, "absent field stays null"
    retry_msgs = fake.requests[1]["messages"]
    assert "Total $120.00" in retry_msgs[0]["content"], "retry keeps the original document"
    assert retry_msgs[1]["content"][0].input["calculated_total"] == 100.0, "retry keeps the failed extraction"
    feedback = retry_msgs[2]["content"][0]
    assert feedback["is_error"] and "line_items sum to 120" in feedback["content"], "retry carries the specific error"

    conflict = {**base, "stated_total": 150.0, "calculated_total": 120.0, "conflict_detected": True}
    assert Invoice(**conflict).conflict_detected, "a stated/calculated mismatch is recorded, not forced to agree"
    try:
        Invoice(**{**right, "category_detail": None})
        raise AssertionError("'other' without detail must fail")
    except ValidationError:
        pass

    stuck = FakeClient([extraction_turn(**wrong)] * 3)
    assert extract(stuck, "doc", model="claude-sonnet-5")["status"] == "needs_review", "retries are capped"
    assert stuck.requests[0]["tool_choice"] == {"type": "tool", "name": "extract_invoice"}, "forced where supported"
    assert fake.requests[0]["tool_choice"] == {"type": "auto"}, "auto on models that reject forced tool_choice"

    reqs = build_batch_requests({"inv-001": "a", "inv-002": "b"}, "claude-sonnet-5-5")
    assert [r["custom_id"] for r in reqs] == ["inv-001", "inv-002"] and reqs[0]["params"]["tools"][0]["strict"]
    try:
        build_batch_requests({"bad id!": "x"}, "m")
        raise AssertionError("invalid custom_id must be rejected")
    except ValueError:
        pass
    results = [SimpleNamespace(custom_id=c, result=SimpleNamespace(type=t))
               for c, t in [("inv-002", "succeeded"), ("inv-003", "errored"), ("inv-001", "expired")]]
    assert failed_custom_ids(results) == ["inv-001", "inv-003"], "resubmit only failures, matched by custom_id"
    print("selftest passed: nullable fields, semantic validation, retry with error feedback, retry cap, "
          "tool_choice by model, batch requests by custom_id, failed-id resubmission")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("files", nargs="*", type=Path)
    p.add_argument("--model", default="claude-sonnet-5-5")
    p.add_argument("--batch", action="store_true", help="submit the files as one Message Batch")
    p.add_argument("--results", metavar="BATCH_ID", help="print failed custom_ids of an ended batch")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        selftest()
        sys.exit()
    if not (a.files or a.results):
        sys.exit(p.format_usage())
    import anthropic
    client = anthropic.Anthropic()
    if a.results:
        print(json.dumps(failed_custom_ids(client.messages.batches.results(a.results))))
    elif a.batch:
        docs = {f.stem: f.read_text() for f in a.files}
        batch = client.messages.batches.create(requests=build_batch_requests(docs, a.model))
        print(f"batch {batch.id} submitted ({len(docs)} documents). Check later with --results {batch.id}")
    else:
        for f in a.files:
            print(f.name, json.dumps(extract(client, f.read_text(), a.model), indent=2))
