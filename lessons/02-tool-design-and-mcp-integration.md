# D2 · Tool Design & MCP Integration

**18% of the exam · ≈ 11 items · 5 task statements · Scenarios:** Customer Support Resolution Agent, Multi-Agent Research System, Developer Productivity with Claude

D2 tests the interface between Claude and everything it can act on. You write tool descriptions that route requests correctly, return errors the agent can recover from, give each agent the right small set of tools, configure MCP servers at the right scope, and pick the right built-in tool for a codebase task.

The core decision rule: the tool description is the router. When Claude picks the wrong tool, fix the description, the name, or the tool boundary before you add infrastructure.

## Task statements

1. **2.1** Design effective tool interfaces with clear descriptions and boundaries
2. **2.2** Implement structured error responses for MCP tools
3. **2.3** Distribute tools appropriately across agents and configure tool choice
4. **2.4** Integrate MCP servers into Claude Code and agent workflows
5. **2.5** Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively

## Core concepts

### The description is the router
*Minimal descriptions cause unreliable selection among similar tools.*

Tool descriptions are the primary mechanism Claude uses to choose a tool. A description like "Retrieves order details" gives the model nothing to tell two similar tools apart. A good description states the purpose, the expected inputs and their formats, the outputs, example queries, edge cases, and when to use a similar tool instead.

```json
{
  "name": "lookup_order",
  "description": "Look up one order by order number. Use when the user mentions an order, shipment, delivery, or return, or gives an ID like '#12345' or 'A-7731'. Returns status, items, amounts, and ship dates. Requires a verified customer_id from get_customer. Do not use for account details such as email or address; use get_customer for those.",
  "input_schema": {
    "type": "object",
    "properties": {
      "order_id": {"type": "string", "description": "Order number with or without '#'"},
      "customer_id": {"type": "string"}
    },
    "required": ["order_id", "customer_id"]
  }
}
```

| Description element | What it prevents |
|---|---|
| Input formats ("IDs like #12345") | The model sending the wrong identifier to the wrong tool |
| Example queries | Misrouting of common phrasings |
| Edge cases | Silent misuse on unusual input |
| Boundary ("use get_customer instead for…") | Overlap with a sibling tool |

Task statements: 2.1

### Rename, rescope, or split overlapping tools
*Near-identical tools misroute. Give each tool one clear job and contract.*

Ambiguous or overlapping descriptions cause misrouting. Two tools named `analyze_content` and `analyze_document` with near-identical descriptions will be confused.

| Problem | Fix | Example |
|---|---|---|
| Two tools with near-identical names and descriptions | Rename and rescope | `analyze_content` becomes `extract_web_results` with a web-specific description |
| One generic tool doing several jobs | Split into purpose-specific tools with defined input/output contracts | `analyze_document` becomes `extract_data_points`, `summarize_content`, `verify_claim_against_source` |
| System prompt says "always analyze the document first" | Review the prompt for keyword-sensitive instructions | The word "analyze" pulls the agent toward `analyze_*` tools |

System prompt wording affects selection. A keyword-sensitive instruction can create an unintended tool association and override a well-written description. When selection is wrong despite good descriptions, read the system prompt.

Task statements: 2.1

### Errors the agent can act on
*Categorize the failure and say whether a retry can help.*

MCP tools report failures with the `isError` flag. A uniform error such as "Operation failed" prevents the agent from choosing a recovery. Return structured metadata instead.

| Category | Example | Agent should | `isRetryable` |
|---|---|---|---|
| Transient | Timeout, service unavailable | Retry, locally first | `true` |
| Validation | Invalid input format | Fix the input and call again | `false` |
| Business | Refund exceeds policy | Explain the rule to the customer | `false` |
| Permission | Caller lacks access | Escalate or route elsewhere | `false` |

```json
{
  "isError": true,
  "content": [{"type": "text", "text": "Refunds over $500 need manager approval."}],
  "errorCategory": "business",
  "isRetryable": false,
  "customerMessage": "I can't approve this refund amount myself. I'll pass it to a specialist."
}
```

Business-rule violations should carry `retriable: false` and a customer-friendly explanation so the agent can communicate the outcome. Without the flag, the agent wastes attempts retrying a call that can never succeed.

Task statements: 2.2

### Empty results and local recovery
*"No matches" is a success. "Could not reach the source" is a failure.*

An access failure and a valid empty result are different outcomes. A search that ran and found nothing is a successful query with no matches. A search that timed out says nothing about whether matches exist. Report them differently so the agent decides correctly: retry the failure, accept the empty result.

| Outcome | `isError` | What the agent concludes |
|---|---|---|
| Query ran, 0 rows | `false`, empty list | "There are no matching orders" |
| Query timed out | `true`, `transient`, retryable | "I don't know yet; retry or try another route" |

Subagents should recover locally from transient failures, for example with a retry. They propagate to the coordinator only the errors they cannot resolve, together with the partial results and what they attempted.

Task statements: 2.2

### Fewer, sharper tools per agent
*Too many tools degrade selection. Scope tools to the role.*

Giving one agent 18 tools instead of 4–5 degrades selection reliability because each decision gets harder. Agents also misuse tools outside their specialization; a synthesis agent with web search tools starts searching instead of synthesizing.

| Rule | Example |
|---|---|
| Restrict each subagent to its role | Search agent gets search tools. Synthesis agent gets none of them |
| Constrain generic tools | Replace `fetch_url` with `load_document`, which validates document URLs |
| Add a scoped cross-role tool for a high-frequency need | Give synthesis a `verify_fact` tool for simple fact checks |
| Route complex cases through the coordinator | Deep verification still goes coordinator → search agent |

The scoped cross-role tool applies least privilege. In the guide's sample, 85% of verifications were simple fact checks. A narrow `verify_fact` tool handles those, and the 15% that need real investigation keep the existing coordinator route.

Task statements: 2.3

### tool_choice: auto, any, or a named tool
*Force the first call when order matters. Use "any" to rule out a text reply.*

| Setting | Behavior | Use when |
|---|---|---|
| `{"type": "auto"}` | The model may call a tool or answer in text | Normal agent turns |
| `{"type": "any"}` | The model must call a tool, and picks which | You need a tool call and several tools could fit |
| `{"type": "tool", "name": "extract_metadata"}` | The model must call this tool | One step must run first, for example `extract_metadata` before enrichment tools |

After a forced first call, process the subsequent steps in follow-up turns with `tool_choice` set back to `auto`.

Docs note: current Anthropic docs report that forced tool use (`any` or a named tool) returns an error on the newest models and recommend strict tool use or structured outputs. The exam guide tests the three options above, so answer from the guide.

Task statements: 2.3

### MCP servers in Claude Code: scope and secrets
*Shared tooling goes in .mcp.json. Personal servers go in ~/.claude.json.*

| Need | Where | Shared via git? |
|---|---|---|
| Team-wide server (GitHub, Jira) | Project-scoped `.mcp.json` | Yes |
| Personal or experimental server | User-scoped `~/.claude.json` | No |
| Auth token for a shared server | `${GITHUB_TOKEN}` expansion in `.mcp.json` | The reference is shared; the secret is not |

```json
{
  "mcpServers": {
    "github": {
      "command": "github-mcp-server",
      "env": {"GITHUB_TOKEN": "${GITHUB_TOKEN}"}
    }
  }
}
```

Claude discovers the tools from all configured MCP servers at connection time, and all of them are available at once. A project server and a personal server work side by side.

For standard integrations such as Jira, choose an existing community MCP server. Build a custom server only for team-specific workflows.

Task statements: 2.4

### MCP resources and descriptions that win adoption
*Resources expose catalogs. Detailed descriptions stop the agent preferring Grep.*

MCP has tools (actions) and resources (content). Expose content catalogs as resources: issue summaries, documentation hierarchies, database schemas. The agent sees what data exists without making exploratory tool calls.

| You want the agent to | Use |
|---|---|
| Know which tables and columns exist | Resource: database schema |
| See the documentation tree before reading pages | Resource: documentation hierarchy |
| Create a ticket | Tool |
| Run a query | Tool |

If the agent keeps using built-in `Grep` instead of your more capable MCP search tool, the MCP tool's description is too thin. Explain its capabilities and outputs in detail, for example "searches the indexed monorepo including generated code and returns symbol definitions with call sites".

Task statements: 2.4

### Pick the right built-in tool
*Grep searches contents. Glob matches paths. Edit needs a unique anchor.*

| Task | Tool |
|---|---|
| Find all callers of `calculateTax` | Grep |
| Locate an error message string | Grep |
| Find every `**/*.test.tsx` file | Glob |
| Load a whole file | Read |
| Create or fully replace a file | Write |
| Change one line in a file | Edit (needs unique matching text) |
| Edit fails because the anchor text appears several times | Read the file, then Write the full new version |
| Run tests or a build | Bash |

Build understanding incrementally. Start with Grep to find entry points, then Read to follow imports and trace flows. Reading every file upfront wastes context.

To trace a function used through wrapper modules, first identify all the names the wrapper exports. Then Grep for each name across the codebase. Searching for the original name alone misses calls made through re-exported aliases.

Task statements: 2.5

## Traps

| Wrong option sounds like | Pattern | Why it loses | Right move |
|---|---|---|---|
| "Add 5–8 few-shot examples for tool routing" | Symptom patch | Token overhead; descriptions stay minimal | Expand the descriptions |
| "Build a keyword routing layer before each turn" | Over-engineering | Bypasses the model's language understanding | Fix descriptions and boundaries |
| "Merge both tools into one lookup_entity" as a first step | Too big a first step | Valid design, but more effort than the problem needs | Clarify descriptions first |
| "Return 'Operation failed'" | Hide the error | No category, no retry signal | `errorCategory`, `isRetryable`, clear message |
| "Return an empty list when the API times out" | Hide the error | The agent concludes "no matches" | `isError: true`, transient, retryable |
| "Give the synthesis agent all search tools" | Over-provisioning | Cross-specialization misuse | Scoped `verify_fact` plus coordinator route |
| "Put the shared server in ~/.claude.json" | Wrong layer | Teammates never get it | Project `.mcp.json` |
| "Commit the token in .mcp.json" | Security failure | Secret in git | `${GITHUB_TOKEN}` expansion |
| "Write a custom Jira MCP server" | Over-engineering | Community server exists | Reuse it; custom only for team workflows |
| "Use Glob to find callers of a function" | Wrong tool | Glob matches paths only | Grep |

## Self-check

### Claude calls get_customer when users ask about orders. Both tools have one-line descriptions. What is the first fix?
Expand both descriptions with input formats, example queries, edge cases, and when to use each tool instead of the other.

### What fields make an MCP error actionable?
The `isError` flag plus an `errorCategory` (transient, validation, business, permission), an `isRetryable` boolean, and a human-readable message.

### A search tool finds no matches. Should it set isError?
No. A query that ran and returned nothing is a valid empty result. Reserve `isError` for access failures such as timeouts.

### Your research synthesis agent has 18 tools and keeps searching the web. What do you change?
Restrict it to the tools its role needs. Add a scoped `verify_fact` tool if it needs frequent simple checks.

### Which tool_choice guarantees a tool call but lets the model pick which tool?
`{"type": "any"}`.

### Where does a team-wide MCP server go, and how do you supply its token?
In the project's `.mcp.json`, with environment variable expansion such as `${GITHUB_TOKEN}`.

### How do you give an agent visibility into a database schema without exploratory tool calls?
Expose the schema as an MCP resource.

### Edit fails because the target line appears three times in the file. What now?
Read the full file, then Write the corrected version.
