# 01 · Build a multi-tool agent with escalation logic

**Domains:** D1, D2, D5 · **Time:** 30 min · **Format:** Design drill + runnable script (`exercises/scripts/support_agent.py`)

## Scenario

Customer Support Resolution Agent. You build a support agent on the Claude Agent SDK. It handles returns, billing disputes, and account issues through four MCP tools: `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`. The target is 80%+ first-contact resolution. Company policy has two hard rules:

- No order or refund operation before the customer's identity is verified.
- No refund above $500 without human approval.

This drill follows Exercise 1 in Section 8 of the official Exam Guide.

## Your task

Write your answers before you open the reference.

1. Write the description for `get_customer` and `lookup_order`. Both accept identifier-like strings. Make the boundary between them explicit.
2. Write the loop control flow in pseudocode. What ends the loop? What do you append to the conversation after a tool call?
3. Design the error response for `lookup_order` for three cases: the order service times out, the order ID does not exist, and the order belongs to another customer.
4. Decide where each hard rule lives: system prompt, few-shot examples, or code. Say what happens when a refund of $1,240 is requested.
5. A customer writes: "My order ORD-1001 arrived broken, and I was also charged twice for my subscription last month." How should the agent handle it?
6. `get_customer(name="Sam Lee")` returns two accounts. What does the agent do?
7. Run the self-test and read the script. Find where each of your answers lives in the code.

```bash
uv run exercises/scripts/support_agent.py --selftest
uv run exercises/scripts/support_agent.py "I want a refund for ORD-1001, my email is ana@example.com"   # needs ANTHROPIC_API_KEY
```

## Reference answer

### Tool descriptions
*The description is the router. Say what the tool does, its inputs, and when to use the other tool instead.*

- `get_customer`: "Look up and verify a customer account. Use this FIRST, before any order or refund tool. Input: email (preferred) or full name. Returns a verified customer_id, or a list of matches when the name is ambiguous. Does not return order details; use lookup_order for those."
- `lookup_order`: "Fetch one order's status, items, amount, and date. Use when the customer mentions an order (e.g. 'check my order ORD-1001'). Input: order_id in the form ORD-<digits> and the verified customer_id. Does not look up customers."

Each description names the input format, gives an example query, and points to the sibling tool. Minimal descriptions such as "Retrieves customer information" cause misrouting between similar tools.

Task statements: 2.1

### Loop control
*Continue on "tool_use", stop on "end_turn". Never parse the text to decide.*

```python
while True:
    response = client.messages.create(model=model, system=SYSTEM, tools=TOOLS, messages=messages, max_tokens=4096)
    messages.append({"role": "assistant", "content": response.content})
    if response.stop_reason == "tool_use":
        results = [run_tool(block) for block in response.content if block.type == "tool_use"]
        messages.append({"role": "user", "content": results})   # every tool_result in one user message
        continue
    if response.stop_reason == "end_turn":
        break
```

A safety cap on iterations is fine as a guard against runaway loops. It must not be the main stopping mechanism. Checking for assistant text or phrases like "I'm done" is an anti-pattern.

Task statements: 1.1

### Structured errors
*Give the agent enough to decide: category, retryable flag, readable message.*

| Case | errorCategory | isRetryable | Agent behavior |
|---|---|---|---|
| Service timeout | `transient` | `true` | Retry once, then tell the customer and escalate if it persists |
| Order ID not found | `validation` | `false` | Ask the customer to check the ID |
| Order of another customer | `permission` | `false` | Do not reveal details. Explain and stop |
| Refund above policy limit | `business` | `false` | Explain in customer-friendly words that a specialist will follow up |

A search that runs and finds nothing is a valid empty result. Return it as success with zero matches, not as an error. A generic "Operation failed" for every case prevents correct recovery.

Task statements: 2.2, 5.3

### Hard rules go in code
*Both rules have financial consequences. Prompt compliance has a non-zero failure rate.*

Both rules live in a pre-tool-call gate (a hook that intercepts outgoing tool calls):

- `lookup_order` and `process_refund` are blocked until `get_customer` has returned a verified `customer_id`. The gate returns a `permission` error that tells the agent to verify first.
- `process_refund` with `amount > 500` never runs. The gate creates the escalation itself with a structured handoff (customer ID, root cause, amount, recommended action) and returns a `business` error with `isRetryable: false`.

For $1,240 the refund does not execute, a ticket exists with all four handoff fields, and the agent tells the customer a specialist will follow up. The system prompt can mention both rules so the agent explains them well. The prompt is not the guarantee.

A post-tool hook (PostToolUse) normalizes data before the model reads it. The script converts the order's Unix timestamp to an ISO 8601 date.

Task statements: 1.4, 1.5

### Multi-concern requests
*Split the message into separate issues, investigate each, then answer once.*

The message holds two issues: a damaged order (return or replacement) and a duplicate subscription charge (billing dispute). The agent verifies the customer once, then investigates both. It can call `lookup_order` for the order and the billing check in the same turn as parallel tool calls. It answers with one unified resolution that covers both issues. If the duplicate charge falls outside what policy lets it resolve, it resolves the order and escalates the billing part with a handoff summary.

Task statements: 1.4

### Ambiguous matches and escalation triggers
*Ask for another identifier. Escalate on request, on policy gaps, or when stuck.*

With two "Sam Lee" accounts, the agent asks for the email on the account. It does not pick the most recent account or the one with more orders.

Escalation triggers for the system prompt, each with a few-shot example:

- The customer asks for a human: escalate at once, without first investigating.
- Policy is silent or ambiguous on the request (for example, a competitor price match when policy covers only own-site adjustments).
- The agent cannot make progress.

A frustrated customer with a simple issue gets an acknowledgment and an offer to resolve. Escalate if they repeat the request for a human. Sentiment and self-reported confidence are not escalation triggers.

Task statements: 5.2

## Check yourself

- Your loop stops on `stop_reason == "end_turn"` and on nothing else except an error or a safety cap.
- Every tool result in one model turn goes back in a single user message.
- The $500 rule and the verification rule hold even if the system prompt is deleted.
- Your error responses separate transient, validation, business, and permission failures, and empty results are not errors.
- The escalation handoff makes sense to a human who never saw the conversation.
- You can point to `pre_tool_gate`, `post_tool_hook`, and `run_agent` in `support_agent.py` and say which task statement each covers.
