# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic>=0.70"]
# ///
"""Exercise 01: a customer support agent with an agentic loop, structured errors, and hook-style gates.

Concepts (CCAR-F task statements):
  1.1  loop on stop_reason: "tool_use" continues, "end_turn" stops
  1.4  programmatic prerequisite: no order or refund calls before get_customer verifies the customer
  1.5  pre-tool gate blocks refunds above $500 and redirects to escalate_to_human;
       post-tool hook normalizes Unix timestamps to ISO 8601
  2.1  tool descriptions that separate similar tools (get_customer vs lookup_order)
  2.2  structured errors: errorCategory + isRetryable + a readable message
  5.2  multiple customer matches -> ask for another identifier, never guess

Run:
  uv run exercises/scripts/support_agent.py --selftest            # offline, no API key
  uv run exercises/scripts/support_agent.py "I want a refund for order ORD-1001, my email is ana@example.com"
The live mode calls the Claude API (needs ANTHROPIC_API_KEY). Tools run against the in-memory backend below.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from types import SimpleNamespace

REFUND_LIMIT = 500  # dollars; above this a human must approve

SYSTEM = """You are a customer support resolution agent for an online store.
Resolve returns, billing disputes, and account issues on first contact when policy allows.
Always identify the customer with get_customer before any order or refund operation.
If get_customer returns several matches, ask the customer for another identifier. Do not pick one.
Escalate with escalate_to_human when: the customer asks for a human, the policy is silent or ambiguous
on the request, or you cannot make progress. Resolve straightforward cases yourself.
If a tool returns an error with isRetryable true, you may retry once. If isRetryable is false,
explain the situation to the customer in plain words."""

TOOLS = [
    {
        "name": "get_customer",
        "description": (
            "Look up and verify a customer account. Use this FIRST in every conversation, before any order or refund "
            "tool. Input: the customer's email (preferred) or full name. Returns a verified customer_id, or a list of "
            "matches when the name is ambiguous. Does not return order details; use lookup_order for those."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "Customer email, e.g. ana@example.com"},
                "name": {"type": "string", "description": "Full name, only when no email is given"},
            },
        },
    },
    {
        "name": "lookup_order",
        "description": (
            "Fetch one order's status, items, amount, and order date. Use when the customer mentions an order or a "
            "purchase (e.g. 'check my order ORD-1001'). Input: order_id in the form ORD-<digits> and the verified "
            "customer_id from get_customer. Does not look up customers."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"order_id": {"type": "string"}, "customer_id": {"type": "string"}},
            "required": ["order_id", "customer_id"],
        },
    },
    {
        "name": "process_refund",
        "description": (
            "Issue a refund for an order that lookup_order has shown to be eligible. Input: order_id, verified "
            "customer_id, amount in dollars, and a short reason. Refunds above $500 need human approval and are "
            "routed to escalation automatically."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"},
                "customer_id": {"type": "string"},
                "amount": {"type": "number"},
                "reason": {"type": "string"},
            },
            "required": ["order_id", "customer_id", "amount", "reason"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": (
            "Hand the case to a human agent who cannot see this conversation. Use when the customer asks for a human, "
            "policy does not cover the request, or you cannot make progress. Input: a self-contained summary with "
            "customer_id, root cause, amount involved, and the recommended action."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
                "root_cause": {"type": "string"},
                "amount": {"type": "number"},
                "recommended_action": {"type": "string"},
            },
            "required": ["root_cause", "recommended_action"],
        },
    },
]

# ---------- in-memory backend ----------
CUSTOMERS = {
    "C-1": {"customer_id": "C-1", "name": "Ana Silva", "email": "ana@example.com"},
    "C-2": {"customer_id": "C-2", "name": "Sam Lee", "email": "sam.lee@example.com"},
    "C-3": {"customer_id": "C-3", "name": "Sam Lee", "email": "slee@example.org"},
}
ORDERS = {
    "ORD-1001": {"order_id": "ORD-1001", "customer_id": "C-1", "amount": 89.0, "status": "delivered", "created": 1793000000},
    "ORD-1002": {"order_id": "ORD-1002", "customer_id": "C-1", "amount": 1240.0, "status": "delivered", "created": 1793500000},
}
TICKETS: list[dict] = []
REFUNDS: list[dict] = []


def error(category, retryable, message):
    """Structured MCP-style error. category: transient | validation | business | permission."""
    return {"isError": True, "errorCategory": category, "isRetryable": retryable, "message": message}


def get_customer(email=None, name=None):
    if email:
        hits = [c for c in CUSTOMERS.values() if c["email"] == email.lower()]
    elif name:
        hits = [c for c in CUSTOMERS.values() if c["name"].lower() == name.lower()]
    else:
        return error("validation", False, "Provide an email or a full name.")
    if not hits:
        return {"matches": [], "message": "No customer found."}  # valid empty result, not an error
    if len(hits) > 1:
        return {"matches": [{"customer_id": c["customer_id"]} for c in hits],
                "message": "Several customers match. Ask for the email on the account."}
    return {"verified": True, **hits[0]}


def lookup_order(order_id, customer_id):
    if order_id == "ORD-TIMEOUT":
        return error("transient", True, "Order service timed out. Retry once.")
    order = ORDERS.get(order_id)
    if not order:
        return error("validation", False, f"No order {order_id}. Check the ID with the customer.")
    if order["customer_id"] != customer_id:
        return error("permission", False, "This order belongs to a different customer.")
    return dict(order)


def process_refund(order_id, customer_id, amount, reason):
    REFUNDS.append({"order_id": order_id, "customer_id": customer_id, "amount": amount, "reason": reason})
    return {"refunded": True, "order_id": order_id, "amount": amount}


def escalate_to_human(root_cause, recommended_action, customer_id=None, amount=None):
    ticket = {"ticket_id": f"T-{len(TICKETS) + 1}", "customer_id": customer_id, "root_cause": root_cause,
              "amount": amount, "recommended_action": recommended_action}
    TICKETS.append(ticket)
    return {"escalated": True, "ticket_id": ticket["ticket_id"]}


HANDLERS = {"get_customer": get_customer, "lookup_order": lookup_order,
            "process_refund": process_refund, "escalate_to_human": escalate_to_human}


# ---------- hooks: deterministic rules live in code, not in the prompt ----------
def pre_tool_gate(name, args, state):
    """Return a result to use instead of running the tool, or None to let the call through."""
    if name in ("lookup_order", "process_refund"):
        if not state.get("customer_id"):
            return error("permission", False, "Blocked: call get_customer and verify the customer first.")
        if args.get("customer_id") != state["customer_id"]:
            return error("permission", False, "Blocked: customer_id does not match the verified customer.")
    if name == "process_refund" and args.get("amount", 0) > REFUND_LIMIT:
        ticket = escalate_to_human(
            customer_id=state["customer_id"], amount=args["amount"],
            root_cause=f"Refund request of ${args['amount']:.2f} on {args.get('order_id')}: {args.get('reason', '')}",
            recommended_action="Review and approve or deny the refund.")
        return {**error("business", False, f"Refunds above ${REFUND_LIMIT} need human approval. "
                        f"Escalated as {ticket['ticket_id']}. Tell the customer a specialist will follow up."),
                "ticket_id": ticket["ticket_id"]}
    return None


def post_tool_hook(name, result, state):
    """Record verification and normalize timestamps before the model sees the result."""
    if name == "get_customer" and result.get("verified"):
        state["customer_id"] = result["customer_id"]
    if isinstance(result.get("created"), int):
        result["created"] = datetime.fromtimestamp(result["created"], timezone.utc).date().isoformat()
    return result


def run_tool(block, state):
    result = pre_tool_gate(block.name, block.input, state)
    if result is None:
        result = post_tool_hook(block.name, HANDLERS[block.name](**block.input), state)
    return {"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(result),
            "is_error": bool(result.get("isError"))}


# ---------- the agentic loop ----------
def run_agent(client, user_message, model, max_iterations=25):
    messages = [{"role": "user", "content": user_message}]
    state: dict = {}
    # The safety cap guards against runaway loops. stop_reason is the stopping mechanism.
    for _ in range(max_iterations):
        response = client.messages.create(model=model, max_tokens=4096, system=SYSTEM, tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": response.content})
        if response.stop_reason == "tool_use":
            results = [run_tool(b, state) for b in response.content if b.type == "tool_use"]
            messages.append({"role": "user", "content": results})  # all results in ONE user message
            continue
        if response.stop_reason == "end_turn":
            return "".join(b.text for b in response.content if b.type == "text"), messages
        raise RuntimeError(f"Stopped early: stop_reason={response.stop_reason}")
    raise RuntimeError("Hit the safety cap without end_turn")


# ---------- offline self-test ----------
class FakeClient:
    """Replays scripted model turns and records every request."""

    def __init__(self, turns):
        self.turns, self.requests = list(turns), []
        self.messages = self

    def create(self, **kwargs):
        self.requests.append(json.loads(json.dumps(kwargs["messages"], default=vars)))
        return self.turns.pop(0)


def tool_turn(*calls):
    blocks = [SimpleNamespace(type="tool_use", id=f"tu_{i}", name=n, input=a) for i, (n, a) in enumerate(calls)]
    return SimpleNamespace(stop_reason="tool_use", content=blocks)


def results_of(request):
    return [json.loads(r["content"]) for r in request[-1]["content"]]


def selftest():
    fake = FakeClient([
        tool_turn(("lookup_order", {"order_id": "ORD-1002", "customer_id": "C-1"})),   # skips verification
        tool_turn(("get_customer", {"name": "Sam Lee"})),                              # ambiguous name
        tool_turn(("get_customer", {"email": "ana@example.com"})),
        tool_turn(("lookup_order", {"order_id": "ORD-TIMEOUT", "customer_id": "C-1"}),
                  ("lookup_order", {"order_id": "ORD-1002", "customer_id": "C-1"})),   # parallel calls
        tool_turn(("process_refund", {"order_id": "ORD-1002", "customer_id": "C-1", "amount": 1240.0, "reason": "damaged"})),
        SimpleNamespace(stop_reason="end_turn", content=[SimpleNamespace(type="text", text="A specialist will follow up.")]),
    ])
    text, _ = run_agent(fake, "Refund ORD-1002 please", model="test")
    r = fake.requests
    assert len(r) == 6 and text == "A specialist will follow up.", "loop must run until end_turn"
    assert results_of(r[1])[0]["errorCategory"] == "permission", "order lookup before verification is blocked"
    assert len(results_of(r[2])[0]["matches"]) == 2, "ambiguous name returns matches, not a guess"
    assert results_of(r[3])[0]["verified"] is True
    timeout, order = results_of(r[4])
    assert timeout["errorCategory"] == "transient" and timeout["isRetryable"] is True
    assert order["created"] == "2026-11-01", "post-tool hook normalizes Unix time to ISO 8601"
    refund = results_of(r[5])[0]
    assert refund["errorCategory"] == "business" and refund["isRetryable"] is False
    assert not REFUNDS, "refund above the limit never runs"
    assert TICKETS and TICKETS[0]["amount"] == 1240.0 and TICKETS[0]["customer_id"] == "C-1", "gate escalates with a handoff"
    print("selftest passed: loop on stop_reason, verification gate, $500 gate -> escalation, structured errors, "
          "timestamp normalization, ambiguous-match handling")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("message", nargs="?", help="customer message for live mode")
    p.add_argument("--model", default="claude-sonnet-5-5")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        selftest()
    elif a.message:
        import anthropic
        answer, history = run_agent(anthropic.Anthropic(), a.message, a.model)
        print(answer)
        print(f"\n[{len(history)} messages · tickets: {TICKETS} · refunds: {REFUNDS}]")
    else:
        sys.exit(p.format_usage())
