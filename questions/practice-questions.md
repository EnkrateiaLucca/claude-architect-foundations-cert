# Practice Questions: CCAR-F

Sixty original, scenario-based questions in the style of the Claude Certified Architect – Foundations exam. They are written for this course and are not drawn from the live exam, whose content is confidential. Each question sits in one of the six official exam scenarios and tests one task statement from the Exam Guide.

**How to use this bank**

- **Timed run:** 60 questions in 120 minutes (2 minutes each, the real exam's pace). Open an answer only after you commit.
- **Interactive:** open `quiz.html` (or the Practice tab of `../study-guide.html`) for click-to-check practice with a score tracker and domain filter.
- **Multiple-response items** say "Choose TWO". Score them all-or-nothing.
- **Review every miss.** Write down which distractor pattern caught you (Lesson 06).

| Domain | Weight | Questions |
|---|---|---|
| D1 Agentic Architecture & Orchestration | 27% | 16 (Q1–Q16) |
| D2 Tool Design & MCP Integration | 18% | 11 (Q17–Q27) |
| D3 Claude Code Configuration & Workflows | 20% | 12 (Q28–Q39) |
| D4 Prompt Engineering & Structured Output | 20% | 12 (Q40–Q51) |
| D5 Context Management & Reliability | 15% | 9 (Q52–Q60) |

**Distractor patterns** named in the explanations: *prompt as policy*, *over-engineering*, *bigger model*, *unreliable proxy*, *invented feature*, *hide or kill the error*.

**Readiness bands** (rough guide, not calibrated to the scaled score): 52–60 strong, 45–51 close, 36–44 keep studying your weakest domains, below 36 restart with the lessons.

---

## D1: Agentic Architecture & Orchestration

### Q1

*Scenario: Customer Support Resolution Agent*

Your support agent's loop sends a request, runs any requested tools, and exits as soon as the response contains a text block. Customers report replies such as "Let me check that order for you" followed by nothing: the agent never looks up the order. What change fixes this?

- A. Increase max_tokens so the model can finish its explanation before it decides to call a tool.
- B. Continue the loop while stop_reason is "tool_use" and exit only when stop_reason is "end_turn".
- C. Add a system prompt rule that forbids the agent from writing any explanatory text before it makes a tool call.
- D. Run the loop for a fixed 10 iterations on every request and return the last text produced.

<details><summary>Answer</summary>

**Answer: B**

**Why B wins:** A response can contain text and a tool_use block together. The loop must follow stop_reason: "tool_use" means execute the tool and send the result back, "end_turn" means the agent is done. Checking for text content is a documented anti-pattern.

- **A fails:** Wrong cause. A length cutoff would return stop_reason "max_tokens". This response ended with "tool_use", and the loop ignored it.
- **C fails:** Prompt as policy. Text next to a tool call is normal model behavior. The bug sits in the loop's control flow.
- **D fails:** An iteration cap as the primary stop condition wastes calls on short tasks and cuts off long ones.

*Task statement:* 1.1 Design and implement agentic loops for autonomous task execution

</details>

### Q2

*Scenario: Developer Productivity with Claude*

You review a teammate's agent loop for a codebase-exploration tool. The loop stops when the latest assistant text contains the phrase "TASK COMPLETE". To save tokens, each tool result is sent as a fresh user message, and earlier messages are dropped. The agent repeats searches and sometimes never stops. Which two changes should you make? (Choose TWO.)

- A. Ask the model to output a JSON field {"done": true} in every turn and parse that field to decide when the loop should stop.
- B. End the loop when stop_reason is "end_turn" instead of searching the text for "TASK COMPLETE".
- C. Replace the loop with a fixed sequence of Grep, Read, and Write calls defined in code.
- D. Append the assistant's tool_use turn and the matching tool_result blocks to the messages list before the next request.
- E. Lower the temperature so the model writes "TASK COMPLETE" more consistently.

<details><summary>Answer</summary>

**Answer: B, D**

**Why B, D wins:** stop_reason is the loop's termination signal, so parsing natural language for a stop phrase is unnecessary and fragile. The model can reason about its next action only if the conversation history, including its own tool_use turns and the tool results, goes back with every request. Dropping history causes the repeated searches.

- **A fails:** This still parses model-written text to decide termination. stop_reason already carries that signal.
- **C fails:** A pre-configured tool sequence removes model-driven decisions, and exploration tasks vary too much for one fixed path.
- **E fails:** Wrong lever. A lower temperature does not make a natural-language stop phrase a reliable control signal.

*Task statement:* 1.1 Design and implement agentic loops for autonomous task execution

</details>

### Q3

*Scenario: Multi-Agent Research System*

Your research coordinator sends every query through all four subagents: web search, document analysis, synthesis, and report generation. A simple factual query such as "What year was the agency founded?" takes as long as a full market study. What is the best fix?

- A. Put a separate classifier model in front of the coordinator that predicts query complexity and picks one of three fixed pipelines.
- B. Keep the full pipeline but move every subagent to a smaller, faster model when the query is short.
- C. Instruct the coordinator to analyze each query's requirements and invoke only the subagents that query needs.
- D. Cache each finished report and return the cached report whenever a similar query arrives.

<details><summary>Answer</summary>

**Answer: C**

**Why C wins:** Choosing which subagents to invoke based on query complexity is the coordinator's job. A coordinator prompt that asks it to assess requirements and select subagents dynamically removes the wasted calls without new infrastructure.

- **A fails:** Over-engineering. A new model and fixed pipelines duplicate a decision the coordinator can already make.
- **B fails:** Bigger model, in reverse. A smaller model leaves the root cause in place: four subagents still run for a one-line answer.
- **D fails:** Speculative caching does not fix routing, and similar wording can hide very different research needs.

*Task statement:* 1.2 Orchestrate multi-agent systems with coordinator-subagent patterns

</details>

### Q4

*Scenario: Multi-Agent Research System*

Two of your search subagents both receive the brief "research renewable energy policy". They fetch the same government reports, synthesis receives duplicate findings, and nobody covers industry or academic sources. How should the coordinator change?

- A. Add a deduplication step to the synthesis agent that removes repeated sources before writing.
- B. Give the subagents a shared memory store so each one can see what the others already fetched.
- C. Reduce the system to a single search subagent so duplicated work cannot happen.
- D. Assign each search subagent a distinct subtopic or source type before delegating.

<details><summary>Answer</summary>

**Answer: D**

**Why D wins:** Partitioning scope across subagents prevents duplicate work at the source and closes the coverage gap. Distinct subtopics or source types per subagent are the pattern the guide names.

- **A fails:** Deduplication treats the symptom. The wasted searches still happen and the missing source types stay missing.
- **B fails:** Subagents do not share memory, and a side channel bypasses the coordinator's controlled information flow.
- **C fails:** One subagent removes the parallelism and still leaves the scope undefined.

*Task statement:* 1.2 Orchestrate multi-agent systems with coordinator-subagent patterns

</details>

### Q5

*Scenario: Multi-Agent Research System*

Your coordinator reviews the synthesis draft for a report on battery recycling. Five sections are well supported, but the section on regulatory incentives rests on a single blog post. What should the coordinator do next?

- A. Send targeted queries on regulatory incentives to the search and analysis subagents, then re-run synthesis.
- B. Ask the synthesis agent to expand the thin section using its own background knowledge of regulatory incentives.
- C. Publish the report now and list regulatory incentives as future work.
- D. Restart the whole pipeline from the beginning and give every subagent a larger research budget this time.

<details><summary>Answer</summary>

**Answer: A**

**Why A wins:** The iterative refinement loop has the coordinator evaluate synthesis output for gaps, re-delegate targeted queries, and re-invoke synthesis until coverage is sufficient. Only the weak area is redone.

- **B fails:** Background knowledge has no sources, so the section loses provenance and may be fabricated.
- **C fails:** Coverage annotations are for sources that are unavailable. This gap is fixable with one more targeted search.
- **D fails:** Over-engineering. Re-running everything repeats five sections of finished work to fix one.

*Task statement:* 1.2 Orchestrate multi-agent systems with coordinator-subagent patterns

</details>

### Q6

*Scenario: Multi-Agent Research System*

The synthesis subagent returns a generic report that cites none of the web results gathered earlier. The coordinator's Task call to synthesis contains only: "Synthesize the findings from the earlier research into a report." What is the root cause?

- A. The synthesis subagent's context window is too small to hold the earlier research.
- B. The coordinator never passed the findings, and subagents do not inherit the coordinator's history.
- C. The synthesis subagent lacks read access to the coordinator's session file.
- D. The search subagent did not send its findings directly to the synthesis subagent.

<details><summary>Answer</summary>

**Answer: B**

**Why B wins:** Subagents start with isolated context. Anything they need, here the search results and document analyses, must be written into the Task prompt by the coordinator.

- **A fails:** Bigger model. Context size is not the problem when nothing was passed in.
- **C fails:** Invented feature. Subagents do not load a parent session file. Context must be passed explicitly in the prompt.
- **D fails:** Subagent-to-subagent messaging breaks hub-and-spoke. The coordinator routes all communication.

*Task statement:* 1.3 Configure subagent invocation, context passing, and spawning

</details>

### Q7

*Scenario: Multi-Agent Research System*

Your coordinator delegates four subtopics to search subagents. Logs show it emits one Task call, waits for the result, then emits the next, so a run takes four times as long as one search. How do you fix the latency?

- A. Merge the four subtopics into one Task call so a single subagent covers all of them.
- B. Start four separate coordinator sessions, one per subtopic, and merge their four reports together afterward.
- C. Raise the coordinator's max_tokens so it can plan all four subtopics before delegating.
- D. Have the coordinator emit all four Task tool calls in a single response so the subagents run in parallel.

<details><summary>Answer</summary>

**Answer: D**

**Why D wins:** Parallel subagents come from multiple Task tool calls in one coordinator response. Separate turns force sequential execution.

- **A fails:** One subagent with four topics loses both the parallelism and the scope partitioning.
- **B fails:** Over-engineering. Four coordinators lose central aggregation and error handling.
- **C fails:** Wrong lever. max_tokens limits output length and has no effect on whether tool calls run in parallel.

*Task statement:* 1.3 Configure subagent invocation, context passing, and spawning

</details>

### Q8

*Scenario: Multi-Agent Research System*

You are writing the Task prompt the coordinator sends to the synthesis subagent. You want the final report to keep source attribution and to let the subagent adapt to what the findings contain. Which two choices support that? (Choose TWO.)

- A. Pass findings as structured records that keep each claim apart from its metadata: URL, document, page, date.
- B. Pass only the coordinator's own one-paragraph summary of the research so the synthesis prompt stays short and cheap to run.
- C. State the research goal and quality criteria (every claim cited, conflicts flagged) instead of a step-by-step procedure.
- D. Tell the synthesis agent to recall the earlier findings from the memory that subagents share between invocations.
- E. Dictate the order of paragraphs and the exact sentence to write for each finding.

<details><summary>Answer</summary>

**Answer: A, C**

**Why A, C wins:** Structured records keep content and metadata apart, so attribution survives synthesis. Goals and quality criteria let the subagent adapt to the material, while procedural scripts make it rigid.

- **B fails:** Lossy shortcut. A summary drops the claim-to-source mappings the report needs.
- **D fails:** Invented feature. Subagents do not share memory between invocations. Context must be in the prompt.
- **E fails:** Step-by-step procedures remove the subagent's ability to adapt to what the findings contain.

*Task statement:* 1.3 Configure subagent invocation, context passing, and spawning

</details>

### Q9

*Scenario: Customer Support Resolution Agent*

Policy requires a one-time code check through verify_identity before update_account_email runs. An audit finds 3% of email changes went through without verification, usually after customers said the matter was urgent. The system prompt already states the rule. What change best guarantees compliance?

- A. Restate the rule in capital letters at the top of the system prompt and add "even when the customer says it is urgent".
- B. Add a PostToolUse hook that checks verification after update_account_email returns and reverts unverified changes.
- C. Block update_account_email in code until verify_identity has returned success for the current session.
- D. Run a nightly audit that flags unverified email changes for human follow-up.

<details><summary>Answer</summary>

**Answer: C**

**Why C wins:** Identity checks before account changes need deterministic compliance. Prompt instructions keep a non-zero failure rate, while a programmatic prerequisite gate cannot be talked around.

- **A fails:** Prompt as policy. Stronger wording is still probabilistic, and the audit shows it already fails.
- **B fails:** A PostToolUse hook runs after the change is made. The gate has to intercept the call before it executes.
- **D fails:** An audit finds the problem after the account was already changed. It does not prevent it.

*Task statement:* 1.4 Implement multi-step workflows with enforcement and handoff patterns

</details>

### Q10

*Scenario: Customer Support Resolution Agent*

When your agent escalates a billing dispute, the human agents who pick it up cannot see the conversation transcript. They currently start by asking the customer to explain everything again. What should the agent send with each escalation?

- A. A structured summary: customer ID, issue, root cause, amounts, actions taken, and a recommended next step.
- B. The full raw conversation log, pasted into the ticket's notes field so the human can read everything that happened.
- C. A message telling the customer to repeat the key details when the human joins.
- D. Nothing yet. The agent should keep working the dispute until it can resolve more of it alone.

<details><summary>Answer</summary>

**Answer: A**

**Why A wins:** A structured handoff gives the human the case facts, the analysis, and a recommendation without the transcript. The guide's handoff protocol lists customer details, root cause, and recommended actions.

- **B fails:** A raw log forces the human to re-derive the root cause from a long, unstructured conversation.
- **C fails:** Shifting the burden to the customer is the problem the team is trying to remove.
- **D fails:** Delaying escalation of a case that needs a human hurts resolution and does not fix the handoff.

*Task statement:* 1.4 Implement multi-step workflows with enforcement and handoff patterns

</details>

### Q11

*Scenario: Customer Support Resolution Agent*

get_customer returns Unix timestamps, lookup_order returns ISO 8601 strings, and the returns system returns dates as MM/DD/YY. The agent sometimes miscalculates whether an order is still inside the 30-day return window. What is the most reliable fix?

- A. Add a system prompt section that explains each tool's date format and how to convert between them.
- B. Add a PostToolUse hook that converts every date field to ISO 8601 before the agent processes the result.
- C. Add a convert_date tool and instruct the agent to call it before it compares any two dates from different tools.
- D. Move the agent to a more capable model that handles mixed date formats better.

<details><summary>Answer</summary>

**Answer: B**

**Why B wins:** A PostToolUse hook intercepts tool results and normalizes heterogeneous formats deterministically, before the model ever reasons over them.

- **A fails:** Prompt as policy. The model still has to convert correctly on every call, which is the step that fails.
- **C fails:** An extra tool adds calls and still depends on the model remembering to use it.
- **D fails:** Bigger model. Normalizing the data in code removes the error instead of making it rarer.

*Task statement:* 1.5 Apply Agent SDK hooks for tool call interception and data normalization

</details>

### Q12

*Scenario: Customer Support Resolution Agent*

A new rule says store credits above $250 for accounts younger than 30 days need a supervisor. The rule must hold every time, and blocked cases should reach a human with the details attached. Which design meets the requirement?

- A. A system prompt rule that describes the $250 limit, plus three few-shot examples showing correct escalation.
- B. A PostToolUse hook that reverses any qualifying store credit after issue_store_credit completes.
- C. A hook that intercepts issue_store_credit, blocks qualifying calls, and routes them to escalate_to_human.
- D. A weekly report of qualifying store credits sent to supervisors for review.

<details><summary>Answer</summary>

**Answer: C**

**Why C wins:** Intercepting the outgoing tool call enforces the business rule before the action happens and redirects to the escalation workflow. Hooks give deterministic guarantees where prompts give probabilistic compliance.

- **A fails:** Prompt as policy. Guaranteed compliance cannot rest on the model following instructions.
- **B fails:** Reversing after the fact means the credit was issued. Interception belongs before the call.
- **D fails:** A report detects violations days later and enforces nothing.

*Task statement:* 1.5 Apply Agent SDK hooks for tool call interception and data normalization

</details>

### Q13

*Scenario: Developer Productivity with Claude*

An engineer asks your agent to "add comprehensive tests to the legacy payments service", which has 400 files and no existing tests. Which decomposition strategy fits best?

- A. A fixed chain that generates tests for each file in alphabetical order, then runs the full suite once at the end.
- B. One request that contains the whole codebase so the model can write every test in a single pass.
- C. Let the agent write tests from wherever it starts and stop when line coverage reaches 80%.
- D. Map the structure, find high-impact areas, then follow a prioritized plan that adapts as dependencies appear.

<details><summary>Answer</summary>

**Answer: D**

**Why D wins:** Open-ended work needs dynamic decomposition: understand the structure, find what matters most, and adapt the plan as dependencies appear. The guide uses this exact kind of task as its example.

- **A fails:** A fixed sequence suits predictable work. Alphabetical order ignores risk and dependencies.
- **B fails:** Bigger model thinking. One giant request dilutes attention and leaves no room to adapt.
- **C fails:** A coverage number as the goal produces many low-value tests in whatever code came first.

*Task statement:* 1.6 Design task decomposition strategies for complex workflows

</details>

### Q14

*Scenario: Developer Productivity with Claude*

Every Friday your tool reviews the week's database migration files. Each file is checked for syntax, naming, and reversibility, and then the set is checked for ordering conflicts between migrations. The checks never change. Which approach fits?

- A. A prompt chain: one pass per migration file for the local checks, then a cross-file pass for ordering conflicts.
- B. A dynamic agent that decides at runtime which of the checks to run on which migration files, based on what it finds.
- C. A single prompt that contains every migration file and the full checklist.
- D. A coordinator with one subagent per check type, where each subagent reads all of the migration files at once.

<details><summary>Answer</summary>

**Answer: A**

**Why A wins:** The steps are known in advance, so a fixed prompt chain fits. Per-file passes keep attention focused, and the separate cross-file pass catches ordering conflicts.

- **B fails:** Over-engineering. Dynamic decomposition is for open-ended investigation, not a fixed checklist.
- **C fails:** One prompt over every file invites attention dilution and uneven depth.
- **D fails:** Over-engineering. Several subagents each reading every file adds coordination and still dilutes attention.

*Task statement:* 1.6 Design task decomposition strategies for complex workflows

</details>

### Q15

*Scenario: Developer Productivity with Claude*

Yesterday you analyzed the auth module in a named session, auth-investigation. Overnight a teammate merged changes to token.py and session.py, two of the files you analyzed. The rest of the analysis is still valid. How should you continue today?

- A. Resume the session and keep working. The agent will notice the changes the next time it reads those files.
- B. Start a brand-new session and have the agent re-explore the entire auth module from scratch, including unchanged files.
- C. Run --resume auth-investigation and tell the agent that token.py and session.py changed.
- D. Use fork_session so the old analysis is kept on a separate branch from today's work.

<details><summary>Answer</summary>

**Answer: C**

**Why C wins:** Resumption fits when most prior context is still valid. Telling the agent exactly which files changed enables targeted re-analysis instead of full re-exploration.

- **A fails:** The agent will reason from stale tool results it already holds and may never re-read the files.
- **B fails:** A fresh start throws away analysis that is mostly still correct.
- **D fails:** Forking creates parallel branches for divergent approaches. It does not refresh stale results.

*Task statement:* 1.7 Manage session state, resumption, and forking

</details>

### Q16

*Scenario: Developer Productivity with Claude*

Your agent finished a long analysis of a monolith. You now want to compare two refactoring approaches, extracting a service layer versus introducing an event bus, and each should start from the same analysis. What should you do?

- A. Try both approaches one after the other in the same session.
- B. Use fork_session to create two branches from the analysis session, one for each approach.
- C. Start two new sessions and have each one redo the codebase analysis.
- D. Run --resume twice in parallel with the same session name, one per approach.

<details><summary>Answer</summary>

**Answer: B**

**Why B wins:** fork_session creates independent branches from a shared baseline, which is exactly what comparing two divergent approaches needs.

- **A fails:** The second approach would be biased by the first approach's changes and reasoning.
- **C fails:** Redoing the analysis twice wastes the shared baseline you already have.
- **D fails:** Resuming the same session twice does not create independent branches. Both runs would write to one history.

*Task statement:* 1.7 Manage session state, resumption, and forking

</details>

---

## D2: Tool Design & MCP Integration

### Q17

*Scenario: Multi-Agent Research System*

Your document analysis subagent has two tools, analyze_text (built for short web snippets) and analyze_file (built for full PDFs). Both descriptions read "Analyzes the given content and returns insights." The agent often sends web snippets to analyze_file, which returns poor results. What is the most effective fix?

- A. Add a system prompt line telling the agent to think carefully and always choose the most appropriate analysis tool.
- B. Add ten few-shot examples to the system prompt that show which analysis tool is correct for each kind of input.
- C. Rename analyze_text to extract_web_snippet_facts and rewrite both descriptions to state inputs, outputs, and when to use each.
- D. Remove analyze_text and send all content through analyze_file.

<details><summary>Answer</summary>

**Answer: C**

**Why C wins:** Tool descriptions drive tool selection, and identical descriptions cause misrouting. A clearer name plus descriptions that state inputs, outputs, and boundaries removes the overlap at its source.

- **A fails:** Prompt as policy. A vague instruction gives the model no information to tell the tools apart.
- **B fails:** Few-shot examples add tokens without fixing the overlapping descriptions.
- **D fails:** Removing a tool loses the snippet-specific handling the team built it for.

*Task statement:* 2.1 Design effective tool interfaces with clear descriptions and boundaries

</details>

### Q18

*Scenario: Customer Support Resolution Agent*

Your system prompt says: "When a customer mentions a refund, review their order history." Tool descriptions are detailed, yet the agent calls get_order_history for "What is your refund policy?" instead of calling get_policy. What should you change first?

- A. Rewrite get_policy's description again with more detail, more example queries, and a list of edge cases.
- B. Add a classifier that strips the word "refund" from policy questions before the agent ever sees the message.
- C. Remove get_order_history from the agent's tool set.
- D. Reword the instruction so it applies only when a customer asks about a refund on a specific order.

<details><summary>Answer</summary>

**Answer: D**

**Why D wins:** Keyword-sensitive system prompt wording can override good tool descriptions. The instruction ties the word "refund" to one tool. Conditioning it on intent fixes the misrouting.

- **A fails:** The descriptions are already good. The conflicting instruction is what overrides them.
- **B fails:** Over-engineering. Rewriting user input hides the real cause and can break other requests.
- **C fails:** The agent needs order history for genuine refund requests.

*Task statement:* 2.1 Design effective tool interfaces with clear descriptions and boundaries

</details>

### Q19

*Scenario: Developer Productivity with Claude*

Your agent has a single query_repo tool with a mode parameter: search, blame, dependents, or history. The description lists all four modes, but each mode returns a different output shape, and the agent often picks the wrong mode or misreads the result. What is the best fix?

- A. Split it into purpose-specific tools, such as find_symbol_usages and get_file_history, each with its own contract.
- B. Keep query_repo and add a paragraph to its description that explains each mode's output shape in full detail.
- C. Have query_repo run every mode on each call and return all four results together.
- D. Add a planning step where the agent writes out which mode it intends to use and why before each query_repo call.

<details><summary>Answer</summary>

**Answer: A**

**Why A wins:** A generic tool that hides several jobs behind one parameter is hard to select and hard to read. Purpose-specific tools with defined input and output contracts make each choice explicit.

- **B fails:** A longer description still asks the model to juggle four behaviors behind one name.
- **C fails:** Returning everything floods context with irrelevant results.
- **D fails:** Prompt as policy. A planning step adds a turn and leaves the overloaded interface in place.

*Task statement:* 2.1 Design effective tool interfaces with clear descriptions and boundaries

</details>

### Q20

*Scenario: Customer Support Resolution Agent*

process_refund returns {"isError": true, "content": "Operation failed"} for every failure. When a refund is refused because the order is outside the return window, the agent retries three times and then tells the customer there was a system error. What is the best fix?

- A. Add a system prompt rule telling the agent never to retry process_refund more than once for the same order.
- B. Return structured metadata: a business errorCategory, isRetryable false, and a plain-language explanation.
- C. Return isError false with an empty result when a refund is refused, so the agent moves on without retrying.
- D. Make the MCP server retry internally with exponential backoff and return an error only after every retry fails.

<details><summary>Answer</summary>

**Answer: B**

**Why B wins:** Uniform errors stop the agent from choosing the right recovery. Structured metadata tells it that a policy refusal is not retryable and gives it wording to explain the refusal to the customer.

- **A fails:** Prompt as policy. A blanket retry limit also blocks retries of genuine transient errors.
- **C fails:** Hide or kill the error. Marking a refusal as success misleads both the agent and the customer.
- **D fails:** Backoff helps transient errors. A policy refusal fails the same way on every retry.

*Task statement:* 2.2 Implement structured error responses for MCP tools

</details>

### Q21

*Scenario: Multi-Agent Research System*

You are designing responses for search_archive, an MCP tool used by the research search subagent. Which two responses are designed correctly? (Choose TWO.)

- A. A query with no matching documents returns isError true and the message "No results found for this query".
- B. A permission failure returns the same generic "Operation failed" message that every other failure returns.
- C. A timeout returns isError true, errorCategory "transient", isRetryable true, and the attempted query.
- D. A malformed date filter returns isError false with an empty result list, so the search appears to have worked.
- E. A query with no matching documents returns a successful result with an empty list and the query that was run.

<details><summary>Answer</summary>

**Answer: C, E**

**Why C, E wins:** A timeout is an access failure the agent may retry, so it is flagged as a transient, retryable error with context. An empty result from a valid query is a successful answer, and it must stay distinct from a failure.

- **A fails:** A valid empty result is not an error. Flagging it invites pointless retries.
- **B fails:** Uniform messages hide whether the agent should retry, ask for access, or give up.
- **D fails:** Hide or kill the error. A validation error disguised as "no results" hides a fixable input mistake.

*Task statement:* 2.2 Implement structured error responses for MCP tools

</details>

### Q22

*Scenario: Multi-Agent Research System*

To keep things simple, every agent in your research system received the same 18 tools. The synthesis agent now picks tools unreliably and sometimes runs web searches mid-synthesis, which adds uncited material. What is the best fix?

- A. Keep all 18 tools on every agent and add a system prompt line telling the synthesis agent not to search.
- B. Move the synthesis agent to a larger, more capable model so it can handle the bigger tool set reliably.
- C. Give the synthesis agent only the few tools its role needs and route new research through the coordinator.
- D. Add a priority number to every tool description so that the agent always tries the higher-priority tools first.

<details><summary>Answer</summary>

**Answer: C**

**Why C wins:** Too many tools degrade selection, and tools outside an agent's specialization get misused. Scoping tools to each role fixes both problems, while the coordinator keeps handling research requests.

- **A fails:** Prompt as policy. The tools stay available and the selection load stays high.
- **B fails:** Bigger model. The decision complexity comes from the tool set, not the model.
- **D fails:** Invented mechanism. Priority numbers do not reduce decision complexity or remove off-role tools.

*Task statement:* 2.3 Distribute tools appropriately across agents and configure tool choice

</details>

### Q23

*Scenario: Multi-Agent Research System*

Your document analysis agent must call extract_metadata on each document before any enrichment tool runs. With tool_choice set to "auto", it sometimes skips straight to enrichment. How do you guarantee the order?

- A. Set tool_choice to "any" on every request.
- B. Keep tool_choice "auto" and move extract_metadata to the first position in the tools array of every request.
- C. Put "Always call extract_metadata first" at the top of the system prompt.
- D. Force {"type": "tool", "name": "extract_metadata"} on the first request, then enrich in later turns.

<details><summary>Answer</summary>

**Answer: D**

**Why D wins:** Forced tool selection guarantees that one specific tool is called. Forcing extract_metadata first and processing enrichment in later turns enforces the required order.

- **A fails:** "any" guarantees some tool call but lets the model pick an enrichment tool.
- **B fails:** Array order does not control which tool the model calls.
- **C fails:** Prompt as policy. The instruction lowers the skip rate but does not guarantee the order.

*Task statement:* 2.3 Distribute tools appropriately across agents and configure tool choice

</details>

### Q24

*Scenario: Developer Productivity with Claude*

Your team wants the GitHub MCP server available to every developer who clones the repository. The access token must never be committed. What configuration should you use?

- A. Put it in the project .mcp.json with the token as ${GITHUB_TOKEN}, set by each developer locally.
- B. Add the server to each developer's ~/.claude.json with the token pasted in.
- C. Add the server to the project's .mcp.json with the real token value, then add .mcp.json to .gitignore.
- D. Describe the server in CLAUDE.md so Claude Code connects to it on first use.

<details><summary>Answer</summary>

**Answer: A**

**Why A wins:** Project-scoped .mcp.json shares team tooling through version control. Environment variable expansion keeps credentials out of the repository.

- **B fails:** User scope is for personal or experimental servers. It does not reach teammates who clone the repo.
- **C fails:** Ignoring the file stops it from being shared, which defeats the purpose.
- **D fails:** Invented feature. CLAUDE.md holds instructions. It does not configure MCP servers.

*Task statement:* 2.4 Integrate MCP servers into Claude Code and agent workflows

</details>

### Q25

*Scenario: Developer Productivity with Claude*

Your team's MCP server offers a symbol-aware code search across all company repositories. The agent keeps using the built-in Grep for cross-repository questions. It also makes many exploratory calls just to find out which database schemas exist. Which two changes help most? (Choose TWO.)

- A. Remove Grep from the agent's built-in tools so it has no choice but to use the MCP server for every search.
- B. Expand the MCP tool's description to say what it searches and returns, so the agent prefers it across repos.
- C. Build a second custom MCP server that wraps the built-in Grep tool under a more descriptive name and description.
- D. Expose the schema catalog as an MCP resource so the agent can see available schemas without exploratory calls.
- E. Move the MCP server from the project .mcp.json to ~/.claude.json so its tools load before the built-in tools.

<details><summary>Answer</summary>

**Answer: B, D**

**Why B, D wins:** Detailed MCP tool descriptions stop the agent from defaulting to built-in tools when the MCP tool is more capable. MCP resources expose content catalogs so the agent can see what data exists without exploring.

- **A fails:** Grep is still the right tool for local content search. Removing it over-corrects.
- **C fails:** Over-engineering. A wrapper duplicates Grep and does nothing for the cross-repository search.
- **E fails:** Invented feature. Tools from all servers are discovered together at connection time, and user scope would stop sharing it with the team.

*Task statement:* 2.4 Integrate MCP servers into Claude Code and agent workflows

</details>

### Q26

*Scenario: Developer Productivity with Claude*

The agent needs to change "timeout: 30" to "timeout: 60" in the database section of settings.yaml. Edit fails because "timeout: 30" appears in three sections. What should the agent do?

- A. Retry Edit with the same text until it succeeds.
- B. Use Bash with sed to replace every occurrence of "timeout: 30" in the file.
- C. Use Grep to count the matches, then edit the first one.
- D. Read the full file, then Write it back with only the database section changed.

<details><summary>Answer</summary>

**Answer: D**

**Why D wins:** Edit needs unique anchor text. When the text is not unique, reading the whole file and writing it back with the targeted change is the reliable fallback.

- **A fails:** The match stays non-unique, so Edit fails the same way each time.
- **B fails:** This changes all three sections when only one should change.
- **C fails:** The first match may not be the database section.

*Task statement:* 2.5 Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively

</details>

### Q27

*Scenario: Developer Productivity with Claude*

A new engineer asks your agent: "How does a refund request flow from the API to the ledger?" The legacy repository has 3,000 files. Which exploration strategy should the agent follow?

- A. Read every file under src/ first so it has the full context of the codebase before it answers anything.
- B. Grep for the refund handler to find entry points, then Read those files and follow their imports.
- C. Glob for **/*refund* and read only files whose names contain "refund".
- D. Describe the typical refund architecture for this framework from general knowledge without opening any files.

<details><summary>Answer</summary>

**Answer: B**

**Why B wins:** Understanding builds up step by step: Grep finds the entry points by content, and Read follows imports to trace the actual flow. Nothing unrelated is loaded.

- **A fails:** Reading 3,000 files up front floods context and buries the relevant code.
- **C fails:** Glob matches file names. The ledger code and helpers likely have names without "refund".
- **D fails:** This invents a typical pattern instead of tracing the real code.

*Task statement:* 2.5 Select and apply built-in tools (Read, Write, Edit, Bash, Grep, Glob) effectively

</details>

---

## D3: Claude Code Configuration & Workflows

### Q28

*Scenario: Code Generation with Claude Code*

The tech lead added a rule six months ago: always call the backend through the shared apiClient wrapper. Claude Code follows it in the tech lead's sessions. A new developer cloned the repo last week, and Claude Code ignores the rule in their sessions. You find the rule in the tech lead's ~/.claude/CLAUDE.md. What fixes this?

- A. Ask the new developer to copy the tech lead's ~/.claude/CLAUDE.md into their own home directory.
- B. Have each developer export the rule in a shell profile variable that Claude Code reads at startup.
- C. Move the rule into the project-level CLAUDE.md and commit it so every clone receives it.
- D. Have the new developer restate the rule at the start of each session until the behavior sticks.

<details><summary>Answer</summary>

**Answer: C**

**Why C wins:** User-level instructions in ~/.claude/CLAUDE.md apply only to that user and are not shared through version control. A rule the whole team needs belongs in the project-level CLAUDE.md, which every clone loads.

- **A fails:** Fixes one person by hand. The copy drifts, and the next hire hits the same gap.
- **B fails:** Invented feature. Claude Code has no such variable, and per-shell setup is unversioned and easy to miss.
- **D fails:** Prompt as policy. Session reminders do not persist and depend on someone remembering to type them.

*Task statement:* 3.1 Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization

</details>

### Q29

*Scenario: Code Generation with Claude Code*

In a monorepo, packages/payments/CLAUDE.md uses @import to pull in packages/payments/standards/testing.md. Two developers report that Claude Code follows the payments testing standards in some sessions and ignores them in others. What should you do first?

- A. Run /memory in an affected session to see which memory files are actually loaded.
- B. Copy the payments testing standards into the root CLAUDE.md so they load in every session.
- C. Move both developers to a higher-tier model that follows imported instructions more reliably.
- D. Add "ALWAYS follow the testing standards" in capital letters at the top of the root CLAUDE.md.

<details><summary>Answer</summary>

**Answer: A**

**Why A wins:** The /memory command shows which memory files a session has loaded, so it diagnoses inconsistent behavior across sessions. A likely cause is a session started outside packages/payments, where the directory-level file and its import do not load.

- **B fails:** Acts before diagnosing. It loads payments rules into every package's sessions and may hide the real cause.
- **C fails:** Bigger model. The instructions may never reach the model, so model quality is not the issue.
- **D fails:** Prompt as policy. Emphasis does not help if the file holding the standards is not loaded.

*Task statement:* 3.1 Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization

</details>

### Q30

*Scenario: Developer Productivity with Claude*

Your team's /map-codebase skill reads dozens of files and prints a long dependency analysis. After running it, developers see their main session fill with output, and later answers lose track of the original task. Which change fixes this while keeping the skill?

- A. Add a line to the skill telling Claude to keep its printed analysis under 50 lines.
- B. Move the skill's instructions into CLAUDE.md so the analysis is ready at the start of each session.
- C. Tell developers to run /compact right after every invocation of the skill.
- D. Add context: fork to the SKILL.md frontmatter so the skill runs in an isolated sub-agent context.

<details><summary>Answer</summary>

**Answer: D**

**Why D wins:** context: fork runs the skill in an isolated sub-agent context. The verbose discovery happens there, and only the result returns, so the main conversation stays focused.

- **A fails:** Truncating the printout loses analysis, and the file reads still land in the main context.
- **B fails:** CLAUDE.md is always loaded. It would add cost to every session and still not isolate the output.
- **C fails:** Treats the symptom after the damage. Compaction is lossy and must be repeated on every run.

*Task statement:* 3.2 Create and configure custom slash commands and skills

</details>

### Q31

*Scenario: Developer Productivity with Claude*

You are writing a project skill, /scaffold-endpoint, that generates boilerplate files for a new API endpoint. It must not run shell commands or delete files. Developers often invoke it without naming the endpoint. Which TWO SKILL.md frontmatter settings address these needs? (Choose TWO.)

- A. context: fork, so the skill's sub-agent has no access to the Bash tool.
- B. allowed-tools limited to the file read and write tools the skill needs.
- C. confirm-destructive: true, so Claude Code asks before any Bash call.
- D. A sentence in the skill body that says "Never run shell commands."
- E. argument-hint describing the endpoint name the developer should pass.

<details><summary>Answer</summary>

**Answer: B, E**

**Why B, E wins:** allowed-tools restricts which tools the skill can use while it runs, which blocks shell and destructive operations. argument-hint prompts developers for the required parameter when they invoke the skill without arguments.

- **A fails:** context: fork isolates context. It does not restrict which tools the skill can call.
- **C fails:** Invented feature. SKILL.md has no such field.
- **D fails:** Prompt as policy. A sentence is a request. allowed-tools is the enforced restriction.

*Task statement:* 3.2 Create and configure custom slash commands and skills

</details>

### Q32

*Scenario: Code Generation with Claude Code*

Your root CLAUDE.md holds two kinds of guidance: naming and error-handling standards that apply to every change, and a 400-line release checklist that release engineers use about twice a month. Developers complain that every session starts with a lot of irrelevant context. What is the best arrangement?

- A. Keep both in CLAUDE.md and add clear headers so Claude can find the relevant section faster.
- B. Keep the standards in CLAUDE.md and move the release checklist into a project skill in .claude/skills/.
- C. Move both into project skills so nothing loads until a developer explicitly asks for it.
- D. Move the release checklist into each release engineer's personal ~/.claude/CLAUDE.md so only they load it.

<details><summary>Answer</summary>

**Answer: B**

**Why B wins:** CLAUDE.md is always loaded, so it suits universal standards. Skills load on demand, so they suit task-specific workflows like a release checklist.

- **A fails:** Headers do not reduce what loads. The 400 lines still enter every session.
- **C fails:** Universal standards must apply to every change. Making them opt-in means they get skipped.
- **D fails:** Still always loaded for those engineers, and the checklist leaves version control and drifts.

*Task statement:* 3.2 Create and configure custom slash commands and skills

</details>

### Q33

*Scenario: Code Generation with Claude Code*

Your repo's 120-line Terraform conventions sit in .claude/rules/terraform.md with no frontmatter. Application developers who never touch infrastructure see those conventions in context in every session. What change keeps them for infrastructure work only?

- A. Add YAML frontmatter with paths: ["terraform/**/*"] so the rule loads only for matching files.
- B. Move the conventions to terraform/CLAUDE.md and reference that file from the root CLAUDE.md with @import.
- C. Convert the conventions into a /terraform slash command that engineers run before editing infrastructure.
- D. Add a first line to the file: "Ignore these conventions unless the task involves Terraform."

<details><summary>Answer</summary>

**Answer: A**

**Why A wins:** A paths field with glob patterns in a .claude/rules/ file makes the rule conditional. It loads only when Claude edits matching files, which cuts irrelevant context and tokens for everyone else.

- **B fails:** An @import from the root CLAUDE.md loads the file in every session, which recreates the problem.
- **C fails:** Depends on people remembering to run it. Path rules apply automatically.
- **D fails:** Prompt as policy. The text still loads and costs tokens; the model is only asked to ignore it.

*Task statement:* 3.3 Apply path-specific rules for conditional convention loading

</details>

### Q34

*Scenario: Code Generation with Claude Code*

A production error report includes a stack trace that points to a missing null check in one function of invoice_formatter.py. The fix is a two-line guard, and the module already has a test file. Which approach fits?

- A. Enter plan mode to map how invoice formatting interacts with other modules before you edit.
- B. Spawn the Explore subagent to survey the codebase and return a summary before deciding.
- C. Use direct execution: add the guard and a regression test for the null case.
- D. Ask Claude to interview you about formatting edge cases before it writes any code.

<details><summary>Answer</summary>

**Answer: C**

**Why C wins:** Direct execution suits simple, well-scoped changes such as a single-file fix with a clear stack trace. The scope is known, so planning adds time without reducing risk.

- **A fails:** Over-engineering. Plan mode is for multi-file or architectural changes with several valid approaches.
- **B fails:** Over-engineering. The stack trace already locates the problem; there is nothing to discover.
- **D fails:** The interview pattern helps in unfamiliar domains with open design questions. This fix has none.

*Task statement:* 3.4 Determine when to use plan mode vs direct execution

</details>

### Q35

*Scenario: Developer Productivity with Claude*

You must migrate a logging library used in about 50 files. The first phase is heavy discovery: finding every call site and wrapper. In an earlier attempt, discovery output filled the context and the session lost track of the plan. Which approach fits best?

- A. Use direct execution one file at a time so each change stays small and context stays light.
- B. Plan with the Explore subagent handling discovery, then carry out the approved plan directly.
- C. Paste the list of 50 files into one prompt and ask Claude to migrate them all in one response.
- D. Switch to a model with a larger context window so discovery output fits beside the plan.

<details><summary>Answer</summary>

**Answer: B**

**Why B wins:** A library migration across many files is a plan-mode task. The Explore subagent isolates verbose discovery and returns a summary, so the main context keeps the plan. Implementation then runs as direct execution.

- **A fails:** Skips the design step. Wrappers found late cause rework across files already changed.
- **C fails:** One response over 50 files invites attention dilution and gives no chance to review the approach.
- **D fails:** Bigger model. More room does not stop verbose output from crowding out the plan.

*Task statement:* 3.4 Determine when to use plan mode vs direct execution

</details>

### Q36

*Scenario: Code Generation with Claude Code*

You ask Claude Code to convert legacy address strings into a normalized format. You have rewritten the prose description three times, and each run still handles apartment numbers and PO boxes differently. What is the most effective next step?

- A. Add "be precise and consistent" to the instructions and run the conversion again.
- B. Write a longer prose specification that describes every address format you have seen.
- C. Ask Claude to rate its confidence on each conversion so you can review the low scores.
- D. Provide two or three input/output pairs, including an apartment and a PO box.

<details><summary>Answer</summary>

**Answer: D**

**Why D wins:** Concrete input/output examples communicate a transformation more reliably than prose when prose is read inconsistently. Two or three pairs that cover the problem cases settle the ambiguity.

- **A fails:** A vague instruction adds no information about how to handle the cases that vary.
- **B fails:** More prose repeats the approach that already failed three times.
- **C fails:** Unreliable proxy. Self-rated confidence does not tell you which format is correct.

*Task statement:* 3.5 Apply iterative refinement techniques for progressive improvement

</details>

### Q37

*Scenario: Code Generation with Claude Code*

A migration script from Claude Code has three problems. The batch size exceeds the transaction timeout. The transaction scope leaves partial writes when a batch fails. A log message has a typo. Changing the batch size changes how the transaction scope must work. How should you communicate the fixes?

- A. Describe the batch size and transaction problems together in one message; send the typo on its own.
- B. Report all three problems one at a time, and wait for each fix to land before you describe the next one.
- C. Ask Claude to rewrite the whole script from scratch with the instruction "fix all the bugs."
- D. Fix the typo first so the simplest change clears noise before the harder problems.

<details><summary>Answer</summary>

**Answer: A**

**Why A wins:** Interacting issues belong in a single detailed message so the fixes are designed together. Independent issues, like the typo, can be handled separately.

- **B fails:** Sequential fixes for interacting problems cause churn: the first fix is redone after the second.
- **C fails:** A vague instruction drops the specific diagnosis you already have.
- **D fails:** Ordering by ease ignores the real issue, which is that two of the fixes depend on each other.

*Task statement:* 3.5 Apply iterative refinement techniques for progressive improvement

</details>

### Q38

*Scenario: Claude Code for Continuous Integration*

Your CI job runs a Claude Code review on every push to a pull request. After developers push fixes, each new run reposts comments that were already resolved or already posted. What should you change?

- A. Run the review only once per pull request, on the first push, and skip it on later pushes.
- B. Delete all earlier bot comments before each run so the thread only shows the newest findings.
- C. Pass prior findings into the run and ask for only new or unaddressed issues.
- D. Raise the severity threshold on later runs so only critical issues are posted after the first.

<details><summary>Answer</summary>

**Answer: C**

**Why C wins:** Including prior review findings in context lets Claude compare against what was already raised. It then reports only new or still-unaddressed issues, which removes duplicate comments.

- **A fails:** Misses bugs introduced by later commits.
- **B fails:** Hides history and still reposts unresolved items as new comments on every run.
- **D fails:** Suppresses real non-critical findings in new code without fixing duplication.

*Task statement:* 3.6 Integrate Claude Code into CI/CD pipelines

</details>

### Q39

*Scenario: Claude Code for Continuous Integration*

Your pipeline runs claude -p to review a diff, and a script posts each finding as an inline PR comment. The script often fails because the review comes back as prose in varying layouts. What is the most reliable fix?

- A. Add "respond only in JSON" to the prompt and parse the reply with a fallback regex.
- B. Add --output-format json with a --json-schema that defines file, line, severity, and message.
- C. Add the --format=pr-comments flag so Claude Code emits comments ready for GitHub.
- D. Send the prose through a second Claude call that converts it into JSON before the script posts it.

<details><summary>Answer</summary>

**Answer: B**

**Why B wins:** --output-format json with --json-schema enforces machine-parseable structured findings in CI. The posting script can rely on the fields it needs.

- **A fails:** Prompt as policy. A request for JSON is not enforcement, and regex fallbacks break on new layouts.
- **C fails:** Invented feature. Claude Code has no such flag.
- **D fails:** Over-engineering. It adds a second call and a second failure point when the CLI can enforce the schema.

*Task statement:* 3.6 Integrate Claude Code into CI/CD pipelines

</details>

---

## D4: Prompt Engineering & Structured Output

### Q40

*Scenario: Claude Code for Continuous Integration*

Your automated review flags many code comments as inaccurate, and developers dismiss most of these findings. The prompt says: "Check that comments are accurate. Be conservative and only report high-confidence findings." What change most improves precision?

- A. Add "only report findings you are at least 90% sure about" to the review prompt.
- B. Switch the review job to a higher-tier model that judges comment accuracy better.
- C. Ask Claude to score its confidence on each finding and drop any finding scored below 7 out of 10.
- D. Replace the instruction: flag a comment only when its claimed behavior contradicts the code.

<details><summary>Answer</summary>

**Answer: D**

**Why D wins:** Explicit categorical criteria improve precision. General instructions like "be conservative" or confidence thresholds do not. The criterion defines exactly what counts as an inaccurate comment.

- **A fails:** A confidence instruction is still vague. The guide says these fail to improve precision.
- **B fails:** Bigger model. The problem is an undefined criterion, not model capability.
- **C fails:** Unreliable proxy. Self-reported confidence is poorly calibrated.

*Task statement:* 4.1 Design prompts with explicit criteria to improve precision and reduce false positives

</details>

### Q41

*Scenario: Claude Code for Continuous Integration*

Your CI review posts findings in four categories. Security and correctness findings are usually accepted. Style findings are dismissed 85% of the time, and developers have started ignoring all bot comments. What should you do first?

- A. Turn off the style category while you rewrite its criteria, and keep security and correctness on.
- B. Keep all four categories and add a note that style findings are optional suggestions.
- C. Run the review three times and post only the findings that appear in at least two of the three runs.
- D. Train a classifier on dismissed comments to filter findings before they reach the PR.

<details><summary>Answer</summary>

**Answer: A**

**Why A wins:** High false-positive categories undermine trust in the accurate ones. Disabling the noisy category restores trust while you improve its prompt.

- **B fails:** The noise still reaches developers, so trust keeps falling.
- **C fails:** Consensus voting suppresses real bugs that appear intermittently and triples cost.
- **D fails:** Over-engineering. It needs labeled data and infrastructure before the prompt fix has been tried.

*Task statement:* 4.1 Design prompts with explicit criteria to improve precision and reduce false positives

</details>

### Q42

*Scenario: Claude Code for Continuous Integration*

Your review prompt describes the output format in detail, but findings still vary. Some name the line and some do not, and severity labels drift between runs. What is the most effective way to get consistent output?

- A. Repeat the formatting rules at both the start and the end of the prompt so they are hard to miss.
- B. Raise max_tokens so Claude has enough room to include every field.
- C. Add three examples that each show location, issue, severity, and fix in the exact format.
- D. Ask Claude to check its own findings for format errors before it returns them.

<details><summary>Answer</summary>

**Answer: C**

**Why C wins:** Few-shot examples are the most effective technique for consistent, actionable output when detailed instructions alone produce inconsistent results. Examples show the exact shape of each finding.

- **A fails:** Repeating instructions that already failed adds tokens without new information.
- **B fails:** Output length is not the problem. Findings are short and still inconsistent.
- **D fails:** Self-review in the same pass rarely catches the drift it just produced.

*Task statement:* 4.2 Apply few-shot prompting to improve output consistency and quality

</details>

### Q43

*Scenario: Structured Data Extraction*

Your pipeline extracts the methodology and sample size from research papers. It works when a paper has a Methods section. It returns null when a paper describes its methods inside the introduction or results. The information is present in those papers. What is the most effective fix?

- A. Make the methodology field required so the model must always return a value for it.
- B. Add few-shot examples of correct extraction from papers that embed methods in other sections.
- C. Preprocess each paper to find a section titled Methods and send only that section to the model.
- D. Retry every null extraction up to three times with the same prompt and document.

<details><summary>Answer</summary>

**Answer: B**

**Why B wins:** Few-shot examples that show correct handling of varied document structures fix empty or null extraction when the data is present. The model learns to look beyond the section heading.

- **A fails:** Forcing a value where the model cannot find one invites fabrication.
- **C fails:** Throws away the sections that hold the methods for exactly the failing papers.
- **D fails:** The same prompt produces the same miss. Retries without new guidance waste calls.

*Task statement:* 4.2 Apply few-shot prompting to improve output consistency and quality

</details>

### Q44

*Scenario: Structured Data Extraction*

Your invoice extraction tool defines purchase_order_number as a required string. Many invoices have no PO number. Auditors find plausible-looking PO numbers in the output that appear nowhere in the source documents. What should you change?

- A. Add "never invent values" in bold to the system prompt for the extraction call.
- B. Lower the temperature so the model takes fewer creative liberties with values.
- C. Add a second pass that asks Claude whether each extracted PO number looks like a real one.
- D. Make the field optional and nullable so the model can return null when it is absent.

<details><summary>Answer</summary>

**Answer: D**

**Why D wins:** A required field forces the model to produce a value even when the source has none. Optional, nullable fields let it return null, which prevents fabricated values.

- **A fails:** Prompt as policy. The schema still demands a value, so the conflict remains.
- **B fails:** Temperature does not change the schema's demand for a value.
- **C fails:** A fabricated number can look real. The fix belongs in the schema.

*Task statement:* 4.3 Enforce structured output using tool use and JSON schemas

</details>

### Q45

*Scenario: Structured Data Extraction*

Your system receives mixed documents (invoices, receipts, contracts) with no type label. You defined one extraction tool per document type. Sometimes Claude replies with a text summary and calls no tool. Which configuration guarantees a structured result and still lets Claude choose the right schema?

- A. Set tool_choice to "any" on the extraction request.
- B. Set tool_choice to "auto" and add "always call a tool" to the prompt.
- C. Force the invoice tool with {"type": "tool", "name": "extract_invoice"}.
- D. Merge the three tools into one tool whose schema makes every field optional.

<details><summary>Answer</summary>

**Answer: A**

**Why A wins:** tool_choice "any" requires the model to call a tool but lets it pick which one. That guarantees structured output when the document type is unknown.

- **B fails:** Prompt as policy. With "auto" the model may still return text.
- **C fails:** Forcing one tool guarantees a call but applies the invoice schema to receipts and contracts.
- **D fails:** A schema with every field optional loses the per-type contract and makes validation weak.

*Task statement:* 4.3 Enforce structured output using tool use and JSON schemas

</details>

### Q46

*Scenario: Structured Data Extraction*

Your extraction uses tool use with a strict JSON schema, and syntax errors no longer occur. Finance now reports that some extracted invoices have line items that do not add up to the stated total. How should you catch these cases?

- A. Tighten the JSON schema with stricter numeric types on every amount field.
- B. Rely on the schema, since a valid tool_use response means the values are consistent.
- C. Extract calculated_total with stated_total, compare them in code, and flag conflict_detected.
- D. Tell the model in the prompt to double-check all of its arithmetic before it calls the extraction tool.

<details><summary>Answer</summary>

**Answer: C**

**Why C wins:** Strict schemas eliminate syntax errors but not semantic errors. Extracting both totals and comparing them in code flags discrepancies, and a conflict_detected boolean routes them for review.

- **A fails:** Types already pass. The values are well-typed and still inconsistent.
- **B fails:** Schema compliance says nothing about whether values agree with each other.
- **D fails:** Prompt as policy. A request to check is not a check you can rely on or measure.

*Task statement:* 4.4 Implement validation, retry, and feedback loops for extraction quality

</details>

### Q47

*Scenario: Structured Data Extraction*

Your validation-retry loop sends the document, the failed extraction, and the specific validation error back to Claude. Which TWO failures is such a retry likely to fix? (Choose TWO.)

- A. invoice_date came back as "March 3rd, 2026" and the schema requires YYYY-MM-DD.
- B. contract_value appears only in a master agreement that was not part of the request.
- C. tax_id fails validation because the scanned page that contains it was never sent.
- D. The shipping address was placed in billing_address while shipping_address was left empty.
- E. approver_name is null because the invoice has no signature block at all.

<details><summary>Answer</summary>

**Answer: A, D**

**Why A, D wins:** Retries with error feedback fix format mismatches and structural errors, such as a wrong date format or a value in the wrong field. The information is present, so the model can correct it.

- **B fails:** The information is absent from the source. No retry can extract it.
- **C fails:** The page was never provided. Fix the input, not the prompt.
- **E fails:** Null is the correct answer when the document has no signature block.

*Task statement:* 4.4 Implement validation, retry, and feedback loops for extraction quality

</details>

### Q48

*Scenario: Claude Code for Continuous Integration*

Developers dismiss about 40% of your CI review findings. You want to learn which code constructs trigger the dismissed findings so you can fix the prompt systematically. What should you add?

- A. A free-text notes field where Claude explains its reasoning for each finding.
- B. A detected_pattern field on each finding, then dismissal analysis grouped by that field.
- C. A weekly survey asking developers which findings felt wrong to them.
- D. A self-reported confidence score on each finding, to see which confidence levels get dismissed most.

<details><summary>Answer</summary>

**Answer: B**

**Why B wins:** A detected_pattern field records which construct triggered each finding. Grouping dismissals by it shows which patterns produce false positives, so you can fix those criteria.

- **A fails:** Free text is hard to aggregate. You need a structured field to group by.
- **C fails:** Surveys are slow, sparse, and not tied to specific findings.
- **D fails:** Unreliable proxy. Confidence does not tell you which construct caused the dismissal.

*Task statement:* 4.4 Implement validation, retry, and feedback loops for extraction quality

</details>

### Q49

*Scenario: Structured Data Extraction*

A partner requires every uploaded document to be processed within 30 hours. You use the Message Batches API, which can take up to 24 hours per batch. How often should you submit batches?

- A. Every 8 hours.
- B. Every 12 hours.
- C. Once every 24 hours, timed so each batch closes just before the deadline.
- D. Every 4 hours.

<details><summary>Answer</summary>

**Answer: D**

**Why D wins:** The batch window has no latency guarantee, so plan for the full 24 hours. A document can wait up to one submission interval before it is sent, so the worst case is interval + 24 hours. Every 4 hours gives 28 hours, inside the 30-hour SLA.

- **A fails:** Worst case is 8 + 24 = 32 hours, which breaks the 30-hour SLA.
- **B fails:** Worst case is 12 + 24 = 36 hours, which breaks the 30-hour SLA.
- **C fails:** Worst case is 24 + 24 = 48 hours. Timing the close does not help documents that just missed it.

*Task statement:* 4.5 Design efficient batch processing strategies

</details>

### Q50

*Scenario: Structured Data Extraction*

A nightly batch of 2,000 contracts returns 1,940 successes. Most of the 60 failures exceeded the context limit. What is the best way to handle them?

- A. Resubmit only the failed requests, found by custom_id, after chunking the oversized contracts.
- B. Resubmit the full batch of 2,000 so every result comes from the same processing run.
- C. Send the 60 failures to the synchronous API unchanged, since it has no batch limits.
- D. Drop the failures from tonight's report and retry them unchanged as part of next week's batch run.

<details><summary>Answer</summary>

**Answer: A**

**Why A wins:** custom_id identifies which requests failed, so you resubmit only those. Chunking addresses the cause, since the documents exceeded the context limit.

- **B fails:** Pays again for 1,940 successful requests and repeats the same 60 failures.
- **C fails:** The context limit applies to synchronous calls too. Unchanged documents fail again.
- **D fails:** Delays the work and resubmits documents that will fail for the same reason.

*Task statement:* 4.5 Design efficient batch processing strategies

</details>

### Q51

*Scenario: Claude Code for Continuous Integration*

Claude Code generates a feature in a long session. You then ask the same session to review its own changes. It approves code that a teammate later finds has an off-by-one bug. What change best improves review quality?

- A. Add "review critically, as if someone else wrote this" to the review request in that session.
- B. Turn on extended thinking in the same session before you ask it for the review.
- C. Run the review in a separate Claude instance that lacks the generator's reasoning context.
- D. Ask the generating session to rate its confidence in each change and recheck the lowest.

<details><summary>Answer</summary>

**Answer: C**

**Why C wins:** A model that keeps its generation reasoning is less likely to question its own decisions. An independent instance without that context catches subtle issues more reliably than self-review instructions or extended thinking.

- **A fails:** Prompt as policy. The session still carries the reasoning that produced the bug.
- **B fails:** The guide states independent instances beat extended thinking for catching these issues.
- **D fails:** Unreliable proxy. The generator is already confident in the code it wrote.

*Task statement:* 4.6 Design multi-instance and multi-pass review architectures

</details>

---

## D5: Context Management & Reliability

### Q52

*Scenario: Customer Support Resolution Agent*

In a long support conversation, your agent summarizes older turns to save context. Twenty turns after promising a $65 refund for order #88213, it offers the customer a $40 credit instead. What design change prevents this?

- A. Stop summarizing and keep the full raw history even when it exceeds the context window.
- B. Keep a case facts block (amounts, dates, order numbers) in every prompt, outside the summary.
- C. Tell the summarizer to be much more detailed whenever it condenses the older turns of the conversation.
- D. Move the agent to a model with a larger context window so it never needs to summarize.

<details><summary>Answer</summary>

**Answer: B**

**Why B wins:** Progressive summarization blurs amounts, dates, and promises. A persistent case facts block, kept outside the summarized history and included in every prompt, preserves them exactly.

- **A fails:** History that exceeds the window cannot be sent. Something must be cut.
- **C fails:** A vague instruction. Summaries still compress numbers unpredictably.
- **D fails:** Bigger model. It delays the problem and long inputs still lose details.

*Task statement:* 5.1 Manage conversation context to preserve critical information across long interactions

</details>

### Q53

*Scenario: Multi-Agent Research System*

Your coordinator combines 12 subagent reports into one long input for the synthesis agent. Final reports often omit findings from reports 5 through 9, though those findings are valid. What is the most effective change?

- A. Shuffle the order of the reports on each run so that no single report always sits in the middle.
- B. Ask the synthesis agent to read the full input twice before it writes the report.
- C. Drop reports 5 through 9 from the input, since the final reports rarely use them.
- D. Put a key-findings summary at the start and place each report under a clear section header.

<details><summary>Answer</summary>

**Answer: D**

**Why D wins:** Models process the beginning and end of long inputs reliably and may omit the middle. A key-findings summary up front and explicit section headers mitigate this position effect.

- **A fails:** Moves the loss to different reports at random instead of removing it.
- **B fails:** An instruction does not change how attention spreads across a long input.
- **C fails:** Hide or kill the error. It discards valid findings.

*Task statement:* 5.1 Manage conversation context to preserve critical information across long interactions

</details>

### Q54

*Scenario: Customer Support Resolution Agent*

A customer writes: "I don't want to talk to a bot. Get me a human now." The request is a simple address change that your agent could complete with one tool call. What should the agent do?

- A. Escalate to a human right away and pass along a structured handoff summary.
- B. Make the address change first, then offer a human if the customer is still unhappy.
- C. Explain that the change is quick and ask the customer to let the agent try first.
- D. Check a sentiment score and escalate only if it falls below the configured threshold.

<details><summary>Answer</summary>

**Answer: A**

**Why A wins:** An explicit request for a human is an escalation trigger. The agent honors it immediately, without first attempting the task, and hands off the details so the customer does not repeat them.

- **B fails:** Overrides the customer's explicit request.
- **C fails:** Offering to resolve fits frustration without an explicit request. Here the customer already asked for a human.
- **D fails:** Unreliable proxy. The explicit request is the trigger, whatever the sentiment score says.

*Task statement:* 5.2 Design effective escalation and ambiguity resolution patterns

</details>

### Q55

*Scenario: Customer Support Resolution Agent*

Which TWO situations should cause your support agent to escalate to a human? (Choose TWO.)

- A. The customer wants a competitor price match, and policy covers only price adjustments on your own site.
- B. The customer is annoyed about a late delivery, and the agent can issue the standard delay credit.
- C. The agent has tried three approaches to unlock the account and cannot make further progress.
- D. get_customer returns two accounts that both match the name the customer gave.
- E. The agent rates its own confidence at 4 out of 10 while handling a routine return.

<details><summary>Answer</summary>

**Answer: A, C**

**Why A, C wins:** Policy gaps and inability to make progress are escalation triggers. When policy is silent on the specific request, a human decides the exception.

- **B fails:** Within the agent's capability. Acknowledge the frustration and resolve it.
- **D fails:** Multiple matches call for asking the customer for another identifier, not escalation.
- **E fails:** Unreliable proxy. Self-reported confidence does not track case complexity.

*Task statement:* 5.2 Design effective escalation and ambiguity resolution patterns

</details>

### Q56

*Scenario: Multi-Agent Research System*

The document analysis subagent queries an internal archive. When the archive times out, the subagent returns {"results": []} with status success. When a query has no matches, it returns the same thing. What should change?

- A. Retry every empty result three times before the subagent returns it to the coordinator.
- B. Treat every empty result as a failure so the coordinator always re-delegates the query.
- C. Return isError true with errorCategory "transient", isRetryable true, and the attempted query for timeouts, and keep the empty success only for real no-match queries.
- D. Return status "unknown" for both cases and let the coordinator re-run the query to find out which it was.

<details><summary>Answer</summary>

**Answer: C**

**Why C wins:** Access failures and valid empty results need different handling. A structured error for the timeout gives the coordinator what it needs to recover, and an empty success then means a real no-match.

- **A fails:** Wastes retries on genuine no-match queries and still hides timeouts that persist.
- **B fails:** Re-delegates valid no-match answers forever. The coordinator still cannot tell the cases apart.
- **D fails:** The coordinator still cannot tell a timeout from a real no-match, and every unclear result costs a second query.

*Task statement:* 5.3 Implement error propagation strategies across multi-agent systems

</details>

### Q57

*Scenario: Code Generation with Claude Code*

Two hours into exploring a large legacy codebase, Claude Code starts citing "typical service patterns" instead of the specific classes it found earlier. Some answers contradict earlier ones. What practice best counters this?

- A. Restart the session and have Claude read every file again from the beginning.
- B. Have Claude record key findings in a scratchpad file and consult it for later questions.
- C. Ask Claude to be more specific and to stop referring to generic service patterns.
- D. Load every file in the codebase at the start of the session so everything stays in context throughout.

<details><summary>Answer</summary>

**Answer: B**

**Why B wins:** Generic answers and contradictions are signs of context degradation in long sessions. A scratchpad file persists key findings across context boundaries, and Claude can consult it for later questions.

- **A fails:** Repeats the expensive exploration and will degrade again the same way.
- **C fails:** An instruction cannot restore details that have fallen out of effective context.
- **D fails:** Reading everything upfront exhausts context faster. Build understanding incrementally.

*Task statement:* 5.4 Manage context effectively in large codebase exploration

</details>

### Q58

*Scenario: Multi-Agent Research System*

Your multi-agent research run crashes after four of six subagents finish. Restarting reruns every subagent and costs hours. Which design best supports recovery?

- A. Keep all subagent results in the coordinator's conversation history and resume that session.
- B. Move the coordinator to a larger model so it crashes less often during long runs.
- C. Append the raw output of every subagent to one shared log file that the coordinator rereads on restart.
- D. Have each agent export state to a known location and the coordinator load a manifest on resume.

<details><summary>Answer</summary>

**Answer: D**

**Why D wins:** Structured state exports plus a manifest let the coordinator see which agents finished and inject their state into prompts on resume. Only the unfinished agents rerun.

- **A fails:** A crash can lose the session, and resuming with stale, verbose tool results is unreliable.
- **B fails:** Bigger model. Crashes come from many causes; recovery still needs saved state.
- **C fails:** An unstructured log gives no clear record of which agents finished and floods the context.

*Task statement:* 5.4 Manage context effectively in large codebase exploration

</details>

### Q59

*Scenario: Structured Data Extraction*

Your extraction pipeline reports 97% overall accuracy, and leadership wants to stop human review of high-confidence extractions. Which TWO steps should come first? (Choose TWO.)

- A. Stop review for any extraction the model rates above 0.9, since overall accuracy is high.
- B. Measure accuracy by document type and by field to confirm every segment performs well.
- C. Move to a more capable model until accuracy reaches 99% before changing the review process.
- D. Set up stratified random sampling of high-confidence extractions to track ongoing error rates.
- E. Replace field-level confidence with one document-level score to simplify review routing.

<details><summary>Answer</summary>

**Answer: B, D**

**Why B, D wins:** A 97% aggregate can hide poor accuracy on specific document types or fields. Segment-level analysis checks that first, and stratified sampling keeps measuring error rates and catches novel errors after review is reduced.

- **A fails:** Acts on the aggregate and on uncalibrated confidence, the two things that can mislead you.
- **C fails:** Bigger model. A higher aggregate can still hide a weak segment.
- **E fails:** Loses the field-level signal that routes reviewer attention.

*Task statement:* 5.5 Design human review workflows and confidence calibration

</details>

### Q60

*Scenario: Multi-Agent Research System*

Two credible sources give different market sizes for the same industry: $4.2B in a 2023 report and $5.1B in a 2025 report. Your synthesis agent keeps the higher number and drops the other. What should the system do?

- A. Keep both values with their sources and publication dates, and report them as differing figures.
- B. Average the two values and cite both sources next to the averaged market-size figure.
- C. Keep only the 2025 figure, because newer data always replaces older data in a report.
- D. Ask the web search agent to find a third source and keep whichever of the values the majority supports.

<details><summary>Answer</summary>

**Answer: A**

**Why A wins:** Conflicting statistics from credible sources should be annotated with attribution, not resolved arbitrarily. Publication dates let readers see the gap may reflect time, not a contradiction.

- **B fails:** An average matches neither source and destroys provenance.
- **C fails:** Silently drops a credible source. The reader cannot see that the figures differ.
- **D fails:** Majority voting is still arbitrary selection and loses the conflict annotation.

*Task statement:* 5.6 Preserve information provenance and handle uncertainty in multi-source synthesis

</details>
