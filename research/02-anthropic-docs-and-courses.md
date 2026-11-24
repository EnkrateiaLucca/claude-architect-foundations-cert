# Anthropic Docs Behind the 30 CCAR-F Task Statements

Research date: 2026-11-24.

## Context

This file maps each CCAR-F task statement to the current Anthropic documentation that supports it, and records the facts verified on those pages. It ends with a drift table: every place where current docs differ from the exam guide. The exam answer always follows the guide. Use the drift notes to avoid confusing learners who also read the docs.

Method: each page was fetched with curl from its markdown endpoint (`<url>.md` on code.claude.com and platform.claude.com, `.md` on modelcontextprotocol.io) on 2026-11-24 and searched for the facts below. The free Partner Academy prep courses are covered in `04-official-prep-path.md`.

Label conventions: `[source: url]` marks a fetched and read page. `[inferred]` marks my own analysis. `[unverified]` marks a claim I could not confirm.

## Pages fetched

| Key | Page | Status |
|---|---|---|
| CC-MEM | https://code.claude.com/docs/en/memory | 200 |
| CC-SKILLS | https://code.claude.com/docs/en/skills (the `slash-commands` URL serves the same page) | 200 |
| CC-SUB | https://code.claude.com/docs/en/sub-agents | 200 |
| CC-MCP | https://code.claude.com/docs/en/mcp | 200 |
| CC-HEADLESS | https://code.claude.com/docs/en/headless | 200 |
| CC-CLI | https://code.claude.com/docs/en/cli-reference | 200 |
| CC-SESS | https://code.claude.com/docs/en/sessions | 200 |
| CC-PERM | https://code.claude.com/docs/en/permission-modes | 200 |
| CC-CTX | https://code.claude.com/docs/en/context-window | 200 |
| CC-TOOLS | https://code.claude.com/docs/en/tools-reference | 200 |
| CC-HOOKS | https://code.claude.com/docs/en/hooks | 200 |
| CC-GHA | https://code.claude.com/docs/en/github-actions | 200 |
| SDK-OV | https://code.claude.com/docs/en/agent-sdk/overview | 200 |
| SDK-LOOP | https://code.claude.com/docs/en/agent-sdk/agent-loop | 200 |
| SDK-SUB | https://code.claude.com/docs/en/agent-sdk/subagents | 200 |
| SDK-HOOKS | https://code.claude.com/docs/en/agent-sdk/hooks | 200 |
| SDK-SESS | https://code.claude.com/docs/en/agent-sdk/sessions | 200 |
| SDK-PERM | https://code.claude.com/docs/en/agent-sdk/permissions | 200 |
| API-TOOLS | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | 200 |
| API-DEFINE | https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools (`implement-tool-use` serves the same page) | 200 |
| API-HANDLE | https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls | 200 |
| API-STOP | https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons | 200 |
| API-SO | https://platform.claude.com/docs/en/build-with-claude/structured-outputs | 200 |
| API-BATCH | https://platform.claude.com/docs/en/build-with-claude/batch-processing | 200 |
| API-PROMPT | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/multishot-prompting (redirects to "Prompting best practices") | 200 |
| API-CTXW | https://platform.claude.com/docs/en/build-with-claude/context-windows | 200 |
| MCP-TOOLS | https://modelcontextprotocol.io/specification/latest/server/tools (spec revision 2026-07-28) | 200 |
| MCP-RES | https://modelcontextprotocol.io/specification/latest/server/resources | 200 |
| MCP-CONCEPTS | https://modelcontextprotocol.io/docs/learn/server-concepts | 200 |

## Domain 1: Agentic Architecture & Orchestration

### 1.1 Agentic loops
- `stop_reason` values today: `end_turn`, `max_tokens`, `stop_sequence`, `tool_use`, `pause_turn`, `refusal`, `model_context_window_exceeded`. For `tool_use`: "Run the tool and return the result." For `end_turn`: "Use the response." [source: https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons]
- Tool results go back in a `user` message as `tool_result` blocks keyed by `tool_use_id`. [source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls]
- In the Agent SDK the loop runs inside the SDK. It ends with a `ResultMessage` whose `subtype` says success or a limit (`error_max_turns`, `error_max_budget_usd`). `max_turns` is optional with "No limit" by default. [source: https://code.claude.com/docs/en/agent-sdk/agent-loop]

### 1.2 Coordinator-subagent orchestration
- Subagent benefits listed: context isolation, parallelization, specialized instructions, tool restrictions. "Only its final message returns to the parent." [source: https://code.claude.com/docs/en/agent-sdk/subagents]
- Claude picks subagents "based on the task and each subagent's `description`". [source: https://code.claude.com/docs/en/agent-sdk/subagents]

### 1.3 Subagent invocation and context passing
- "The only content you pass from parent to subagent is the Agent tool's prompt string, so include any file paths, error messages, or decisions the subagent needs directly in that prompt." [source: https://code.claude.com/docs/en/agent-sdk/subagents]
- A non-fork subagent receives its own system prompt, the Agent tool's prompt, project CLAUDE.md (via `settingSources`), and tool definitions. It does not receive the parent's history, tool results, or system prompt. [source: https://code.claude.com/docs/en/agent-sdk/subagents]
- `AgentDefinition` fields: `description` (required), `prompt` (required), `tools`, `disallowedTools`, `model`, `skills`, `memory`, `mcpServers`, `maxTurns`, and more. [source: https://code.claude.com/docs/en/agent-sdk/subagents]
- The tool is named `Agent` in `tool_use` blocks and `Task` in the `system:init` tool list. "Before Claude Code v2.1.63, `tool_use` blocks also named it `"Task"`." Docs tell you to match both names. [source: https://code.claude.com/docs/en/agent-sdk/subagents]
- Subagents run in the background by default (`status: "async_launched"`); Claude waits when its next step needs the report. [source: https://code.claude.com/docs/en/agent-sdk/subagents]
- A fork copies the conversation instead of starting fresh (`subagent_type: "fork"`). [source: https://code.claude.com/docs/en/agent-sdk/subagents]

### 1.4 Enforcement and handoff
- A `PreToolUse` hook returns `permissionDecision: "deny"` plus `permissionDecisionReason` to block a call and tell the model why. [source: https://code.claude.com/docs/en/agent-sdk/hooks]
- `disallowed_tools=["Bash(rm *)"]` denies matching calls "in every permission mode, including `bypassPermissions`". [source: https://code.claude.com/docs/en/agent-sdk/permissions]
- Handoff summaries for human agents have no dedicated docs page. The guide is the reference. [inferred]

### 1.5 Hooks for interception and normalization
- SDK hook events include `PreToolUse` ("can block or modify"), `PostToolUse`, `PostToolUseFailure`, `Stop`, `SubagentStop`. [source: https://code.claude.com/docs/en/agent-sdk/hooks]
- `PostToolUse` can append `additionalContext` or replace output with `updatedToolOutput` ("works for built-in and MCP tools in both SDKs"). `updatedMCPToolOutput` is the older field. [source: https://code.claude.com/docs/en/agent-sdk/hooks]
- `PreToolUse` can rewrite arguments with `updatedInput`. [source: https://code.claude.com/docs/en/agent-sdk/hooks]

### 1.6 Task decomposition
- The Building with the Claude API course has "Parallelization workflows", "Chaining workflows", "Routing workflows" lessons. [source: https://anthropic-partners.skilljar.com/claude-with-the-anthropic-api]
- Subagents give parallel review (`style-checker`, `security-scanner`, `test-coverage`). [source: https://code.claude.com/docs/en/agent-sdk/subagents]

### 1.7 Sessions, resume, fork
- CLI: `claude --continue`, `claude --resume` (picker), `claude --resume <name>`, `claude --resume <session-id>`. Name a session with `/rename auth-refactor`. [source: https://code.claude.com/docs/en/sessions]
- CLI `--fork-session`: "When resuming, create a new session ID instead of reusing the original". [source: https://code.claude.com/docs/en/cli-reference]
- SDK: `continue_conversation=True`, `resume=<session_id>`, and `fork_session=True` (Python) / `forkSession: true` (TS). The session ID comes from `ResultMessage.session_id`. [source: https://code.claude.com/docs/en/agent-sdk/sessions]
- `claude -p` and SDK sessions do not appear in the picker or in `--continue`; resume them by ID. [source: https://code.claude.com/docs/en/sessions]

## Domain 2: Tool Design & MCP Integration

### 2.1 Tool descriptions
- "Provide extremely detailed descriptions. This is by far the most important factor in tool performance." Aim for "at least 3–4 sentences" per tool, covering what it does, when to use it, parameters, and caveats. [source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools]
- Tools accept `input_examples`; validate each against `input_schema`. [source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools]

### 2.2 Structured MCP errors
- MCP has two error mechanisms. Protocol errors (JSON-RPC) for malformed requests. Tool execution errors "contain actionable feedback that language models can use to self-correct" and are "reported in tool results with `isError: true`". Clients SHOULD pass tool execution errors to the model. [source: https://modelcontextprotocol.io/specification/latest/server/tools]
- The Claude API equivalent is `is_error: true` on a `tool_result` block. [source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls]
- `errorCategory`, `isRetryable`, and `retriable` are not spec fields. They are the guide's convention for the structured content you return inside an error result. [source: https://modelcontextprotocol.io/specification/latest/server/tools] [inferred]

### 2.3 Tool distribution and `tool_choice`
- `tool_choice`: `auto` (default with tools), `any` (must use one of the tools), `tool` (must use the named tool), `none`. [source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools]
- Forced options (`any`, `tool`) "return a 400 error" on Claude Fable 5.2, Mythos 5.2, Opus 5.5, Sonnet 5.5, Fable 5.1, Mythos 5.1, and fail with manual extended thinking. Use `auto` with strict tool use there. [source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools]
- `AgentDefinition.tools` restricts a subagent's tool set; `disallowedTools` removes tools. [source: https://code.claude.com/docs/en/agent-sdk/subagents]

### 2.4 MCP in Claude Code
- Three scopes: local (default, private, stored in `~/.claude.json` under the project), project (`.mcp.json` at the repo root, shared via version control), user (all your projects, `~/.claude.json`). [source: https://code.claude.com/docs/en/mcp]
- `.mcp.json` expands `${VAR}` and `${VAR:-default}` in `command`, `args`, `env`, `url`, `headers`. [source: https://code.claude.com/docs/en/mcp]
- Claude Code asks for approval before using project-scoped servers from `.mcp.json`. [source: https://code.claude.com/docs/en/mcp]
- Tool search is on by default: "Only tool names and server instructions load at session start", and full definitions load on demand. [source: https://code.claude.com/docs/en/mcp]
- Resources are referenced with `@server:protocol://resource/path`. MCP resources are "application-driven"; tools are "model-controlled"; prompts are "user-controlled". [source: https://code.claude.com/docs/en/mcp] [source: https://modelcontextprotocol.io/specification/latest/server/resources] [source: https://modelcontextprotocol.io/docs/learn/server-concepts]

### 2.5 Built-in tools
- Edit "performs exact string replacement"; `old_string` "must appear exactly once", otherwise use more context or `replace_all: true`. [source: https://code.claude.com/docs/en/tools-reference]
- On macOS, Linux, and WSL, Claude Code leaves Glob and Grep out of the default tool set and searches with `find` and `grep` through Bash (embedded `bfs` and `ugrep`). Naming them in `--tools`/`--allowedTools`, removing Bash, or listing them in a subagent's `tools` brings them back. Windows keeps them. [source: https://code.claude.com/docs/en/tools-reference]

## Domain 3: Claude Code Configuration & Workflows

### 3.1 CLAUDE.md hierarchy
- Locations: managed policy (OS-specific path), user `~/.claude/CLAUDE.md`, project `./CLAUDE.md` or `./.claude/CLAUDE.md`, local `./CLAUDE.local.md` (gitignored). Ancestor files load at launch; subdirectory files load when Claude touches files there. All files concatenate; none override. [source: https://code.claude.com/docs/en/memory]
- `@path/to/import` imports, relative to the importing file, "maximum depth of four hops". [source: https://code.claude.com/docs/en/memory]
- Target "under 200 lines per CLAUDE.md file". [source: https://code.claude.com/docs/en/memory]
- `/memory` "lists your CLAUDE.md, CLAUDE.local.md, and other memory file locations". Docs also suggest `/context all` to verify which files loaded. [source: https://code.claude.com/docs/en/memory]

### 3.2 Commands and skills
- "Custom commands have been merged into skills. Your existing `.claude/commands/` files keep working." [source: https://code.claude.com/docs/en/skills]
- Skill locations: enterprise, personal `~/.claude/skills/<name>/SKILL.md`, project `.claude/skills/<name>/SKILL.md`, nested, additional directory. Same name: enterprise > personal > project; a skill beats a command file. [source: https://code.claude.com/docs/en/skills]
- Frontmatter includes `description`, `argument-hint`, `allowed-tools`, `disallowed-tools`, `disable-model-invocation`, `context`, `agent`, `paths`, `model`, `effort`. [source: https://code.claude.com/docs/en/skills]
- `allowed-tools` "grants permission for the listed tools during the turn that invokes the skill ... It does not restrict which tools are available". `disallowed-tools` removes tools. [source: https://code.claude.com/docs/en/skills]
- `context: fork` runs the skill in a new subagent that "doesn't see your conversation history", in the background by default (`background: false` to wait). "Despite the name", it is not a fork of the current conversation. [source: https://code.claude.com/docs/en/skills]

### 3.3 Path-specific rules
- `.claude/rules/*.md` with YAML `paths:` globs. "A path-scoped rule loads when Claude uses the Read, Write, or Edit tool on a matching file." Rules without `paths` load at launch. [source: https://code.claude.com/docs/en/memory]
- Example glob table: `**/*.ts`, `src/**/*`, brace expansion `src/**/*.{ts,tsx}`. [source: https://code.claude.com/docs/en/memory]

### 3.4 Plan mode and Explore
- "Plan mode tells Claude to research and propose changes without making them." `Shift+Tab` cycles modes; `--permission-mode plan` starts in plan mode. [source: https://code.claude.com/docs/en/permission-modes] [source: https://code.claude.com/docs/en/cli-reference]
- Built-in Explore and Plan subagents "start without your CLAUDE.md files and the git status snapshot to keep research fast and inexpensive". [source: https://code.claude.com/docs/en/sub-agents]

### 3.5 Iterative refinement
- No single docs page covers the interview pattern or test-driven iteration. The prompting best-practices page covers examples and clear criteria. [source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/multishot-prompting] [inferred]

### 3.6 CI/CD
- `-p`/`--print` runs non-interactively. `--output-format` accepts `text`, `json`, `stream-json`. `--json-schema` returns "validated JSON output matching a JSON Schema after the agent completes its workflow (print mode only)". [source: https://code.claude.com/docs/en/cli-reference] [source: https://code.claude.com/docs/en/headless]
- `--bare` skips hooks, skills, subagents, MCP servers, auto memory, and CLAUDE.md. Docs call it "the recommended mode for scripted and SDK calls" and say it "will become the default for `-p` in a future release". [source: https://code.claude.com/docs/en/headless]
- Without `--bare`, a `-p` run executes project hooks and connects `.mcp.json` servers even in an untrusted folder. [source: https://code.claude.com/docs/en/headless]
- The GitHub Action and managed Code Review post inline PR comments. [source: https://code.claude.com/docs/en/github-actions]

## Domain 4: Prompt Engineering & Structured Output

### 4.1 Explicit criteria
- Best-practices page: be clear and direct, say what to do, give context for why. [source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/multishot-prompting]

### 4.2 Few-shot
- Examples are "one of the most reliable ways to steer Claude's output format, tone, and structure". Make them relevant, diverse, and wrapped in `<example>` tags. "Include 3–5 examples for best results." [source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/multishot-prompting]

### 4.3 Structured output
- Structured outputs have two features: JSON outputs (`output_config.format`) and strict tool use (`strict: true`), both via constrained decoding. [source: https://platform.claude.com/docs/en/build-with-claude/structured-outputs]
- With `tool_choice` `any` or `tool`, the response starts with the tool call, and forcing a tool skips thinking. [source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools]
- Schema validity does not check meaning (totals, field placement). No docs page contradicts the guide here. [inferred]

### 4.4 Validation and retry
- The Claude API course covers prompt evals and code-based grading; Pydantic is not documented by Anthropic. [source: https://anthropic-partners.skilljar.com/claude-with-the-anthropic-api] [inferred]

### 4.5 Message Batches API
- "reducing costs by 50 percent"; "most batches finishing in less than 1 hour"; batches "expire if processing does not complete within 24 hours". [source: https://platform.claude.com/docs/en/build-with-claude/batch-processing]
- Limits: 100,000 requests or 256 MB per batch; results kept 29 days. `custom_id` is 1–64 alphanumeric, hyphen, or underscore characters. Result types include `succeeded`, `errored`, `expired` (errored and expired are not billed). [source: https://platform.claude.com/docs/en/build-with-claude/batch-processing]
- Batches accept tool definitions, including server tools. Your own (client) tools still cannot run mid-request, so a batch request cannot complete a multi-turn tool loop. [source: https://platform.claude.com/docs/en/build-with-claude/batch-processing] [inferred]

### 4.6 Multi-instance review
- Subagents give an independent context; parallel review agents are a documented use. [source: https://code.claude.com/docs/en/agent-sdk/subagents]

## Domain 5: Context Management & Reliability

### 5.1 Conversation context
- Long-context tips: "Put long-form data at the top", queries at the end "can improve response quality by up to 30 percent". [source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/multishot-prompting]
- The Messages API is stateless; each request sends the conversation so far. [source: https://platform.claude.com/docs/en/build-with-claude/context-windows] [inferred]

### 5.2 Escalation
- No docs page covers customer-support escalation policy. The guide is the reference. [inferred]

### 5.3 Error propagation
- "An API error that ends the subagent early, such as a rate limit, is never delivered as its result." A subagent stopped by `maxTurns` returns output marked partial. [source: https://code.claude.com/docs/en/agent-sdk/subagents]

### 5.4 Large codebase exploration
- `/compact` "replaces the conversation with a structured summary"; `/compact focus on the auth bug fix` steers it. Claude Code also compacts automatically near the limit. [source: https://code.claude.com/docs/en/context-window]
- Subagents keep intermediate tool calls out of the parent context. [source: https://code.claude.com/docs/en/agent-sdk/subagents]

### 5.5 Human review and calibration
- No docs page covers stratified sampling or field-level calibration. The guide is the reference. [inferred]

### 5.6 Provenance
- The Claude API course covers citations; the Citations feature returns cited passages with responses. [source: https://anthropic-partners.skilljar.com/claude-with-the-anthropic-api] [inferred]

## Drift: exam guide vs current docs

Teach the exam answer. Mention the docs note so learners who read the docs are not confused.

| # | Topic | Exam guide says (answer this on the exam) | Current docs say |
|---|---|---|---|
| 1 | Subagent tool name | Spawn subagents with the `Task` tool; `allowedTools` must include `"Task"` (1.3) | The tool is `Agent` in `tool_use` blocks (since Claude Code v2.1.63) and `Task` only in the `system:init` list. Doc examples put `"Agent"` in `allowed_tools`. [source: https://code.claude.com/docs/en/agent-sdk/subagents] |
| 2 | `allowedTools` meaning | Including a tool in `allowedTools` lets the coordinator use it (1.3) | `allowed_tools` auto-approves; unlisted tools still exist. `tools`/`disallowed_tools` control availability. [source: https://code.claude.com/docs/en/agent-sdk/permissions] |
| 3 | Forced `tool_choice` | `"any"` guarantees a tool call; `{"type":"tool","name":...}` forces a specific first step (2.3, 4.3) | `any` and `tool` return 400 on Opus 5.5, Sonnet 5.5, Fable 5.1/5.2, Mythos 5.1/5.2 and with manual extended thinking. Use `auto` + strict tool use. [source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools] |
| 4 | Most reliable structured output | `tool_use` with a JSON schema (4.3) | Native structured outputs (`output_config.format`) and strict tool use (`strict: true`) with constrained decoding. [source: https://platform.claude.com/docs/en/build-with-claude/structured-outputs] |
| 5 | Skill `allowed-tools` | Restricts tool access during the skill (3.2) | Pre-approves listed tools for that turn; "does not restrict which tools are available". `disallowed-tools` removes tools. [source: https://code.claude.com/docs/en/skills] |
| 6 | `context: fork` | Runs the skill in an isolated sub-agent context (3.2) | Same isolation, plus: runs in the background by default, and "Despite the name" it is not a conversation fork. [source: https://code.claude.com/docs/en/skills] |
| 7 | Slash commands | Project commands in `.claude/commands/`, personal in `~/.claude/commands/` (3.2) | Commands merged into skills; `.claude/commands/` still works, and a skill with the same name wins. [source: https://code.claude.com/docs/en/skills] |
| 8 | Personal skill variants | Create personal variants in `~/.claude/skills/` "with different names to avoid affecting teammates" (3.2) | Precedence is enterprise > personal > project, so a same-name personal skill shadows the project skill for you only. [source: https://code.claude.com/docs/en/skills] |
| 9 | MCP scopes | Project `.mcp.json` vs user-level `~/.claude.json` (2.4) | Three scopes: local (default), project, user. Local and user both live in `~/.claude.json`. [source: https://code.claude.com/docs/en/mcp] |
| 10 | MCP tool discovery | Tools from all servers "discovered at connection time and available simultaneously" (2.4) | Tool search is on by default: names load at start, full definitions on demand. All servers' tools are still reachable together. [source: https://code.claude.com/docs/en/mcp] |
| 11 | Structured MCP errors | Return `isError` with `errorCategory` and `isRetryable` (2.2) | The spec defines `isError: true` for tool execution errors. `errorCategory`/`isRetryable` are your own content, not spec fields. [source: https://modelcontextprotocol.io/specification/latest/server/tools] |
| 12 | Built-in Grep and Glob | Grep for content, Glob for paths (2.5) | On macOS, Linux, WSL they are off by default; Claude uses `grep`/`find` via Bash unless you enable them. The selection logic still holds. [source: https://code.claude.com/docs/en/tools-reference] |
| 13 | Sessions | `--resume <session-name>` and `fork_session` (1.7) | Both exist. CLI also has `--continue`, `--fork-session`, and `/rename`. SDK uses `resume=<id>` + `fork_session=True` / `forkSession: true`. [source: https://code.claude.com/docs/en/sessions] [source: https://code.claude.com/docs/en/agent-sdk/sessions] |
| 14 | CI context | CLAUDE.md provides project context to CI-invoked Claude Code (3.6) | Docs recommend `--bare` for scripted runs, and `--bare` skips CLAUDE.md. Without `--bare`, CLAUDE.md loads as the guide says. [source: https://code.claude.com/docs/en/headless] |
| 15 | `--json-schema` | `--output-format json` + `--json-schema` for machine-parseable findings (3.6) | Matches. Output is validated "after the agent completes its workflow (print mode only)". [source: https://code.claude.com/docs/en/cli-reference] |
| 16 | Path rules | `.claude/rules/` with YAML `paths` globs load only for matching files (3.3) | Matches. Loading triggers on Read, Write, Edit (and single-file `cat`/`head`) of a match. [source: https://code.claude.com/docs/en/memory] |
| 17 | `/memory` | Verify which memory files are loaded (3.1) | `/memory` lists and opens the files; docs point to `/context all` to confirm what loaded at launch. [source: https://code.claude.com/docs/en/memory] |
| 18 | CLAUDE.md levels | User, project, directory (3.1) | Adds managed policy CLAUDE.md and `CLAUDE.local.md`; `@path` imports max four hops. [source: https://code.claude.com/docs/en/memory] |
| 19 | Subagent context | Subagents do not inherit parent context (1.2, 1.3) | Still true for history and tool results, but non-fork subagents do load project CLAUDE.md; forks copy the conversation; Explore and Plan skip CLAUDE.md. [source: https://code.claude.com/docs/en/agent-sdk/subagents] [source: https://code.claude.com/docs/en/sub-agents] |
| 20 | Parallel subagents | Emit multiple `Task` calls in one coordinator response (1.3) | Still valid. Subagents now also run in the background by default (`async_launched`). [source: https://code.claude.com/docs/en/agent-sdk/subagents] |
| 21 | `stop_reason` | Two values matter for the loop: `"tool_use"` and `"end_turn"` (1.1) | Seven values exist (`max_tokens`, `stop_sequence`, `pause_turn`, `refusal`, `model_context_window_exceeded` too). A production loop handles them; the exam tests the two. [source: https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons] |
| 22 | Hook output replacement | `PostToolUse` transforms results before the model sees them (1.5) | Field is `updatedToolOutput` (built-in and MCP); `updatedMCPToolOutput` is legacy. [source: https://code.claude.com/docs/en/agent-sdk/hooks] |
| 23 | Few-shot count | 2–4 targeted examples (4.2) | Prompting best practices say 3–5. Use the guide's number on the exam. [source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/multishot-prompting] |
| 24 | Batch latency | Up to 24 h, no SLA (4.5) | Matches; "most batches finishing in less than 1 hour". Still no guarantee, so pre-merge checks stay synchronous. [source: https://platform.claude.com/docs/en/build-with-claude/batch-processing] |

## Open questions

- Will a future guide version adopt the `Agent` tool name or structured outputs? v1.1 (2026-11-17) did not change content. [source: https://cc.sj-cdn.net/instructor/6nizmqk8tpzpfjvt6qmmav7rh/public/1794946250/Claude_Certified_Architect_-_Foundations_Exam_Guide.pdf]
- The guide never names a model. Labs that run forced `tool_choice` need a model that accepts it, or must use `auto` + strict tool use. [inferred]
