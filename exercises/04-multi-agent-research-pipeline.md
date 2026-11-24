# 04 · Design and debug a multi-agent research pipeline

**Domains:** D1, D2, D5 · **Time:** 30 min · **Format:** Design drill + debugging cases

## Scenario

Multi-Agent Research System. A coordinator built on the Claude Agent SDK delegates to four subagents: web search, document analysis, synthesis, and report writing. A user asks for a cited report on "the effect of remote work on urban office markets, 2020–2026". This drill follows Exercise 4 in Section 8 of the official Exam Guide.

## Your task

Part A: design.

1. What must the coordinator's configuration contain so it can start subagents? What does each subagent definition need?
2. The synthesis subagent starts. What does it know about the search and analysis work? What must you pass it, and in what shape?
3. How does the coordinator run search and analysis at the same time?
4. Write the coordinator's instruction for the search subagent. Choose between step-by-step procedure and goals with quality criteria.
5. Which tools does each subagent get?

Part B: debug. For each case, name the root cause and the fix.

6. Each subagent succeeds, but the report covers only New York and London.
7. The search subagent times out on the 2024 vacancy data.
8. Two credible sources give office vacancy in 2023 as 18.1% and 19.6%. The report shows only 19.6%.
9. A 2021 survey and a 2025 survey disagree on return-to-office rates. The report calls this a contradiction.
10. The final report lost which source supports which claim.

## Reference answer

### Coordinator and subagent configuration
*The coordinator spawns subagents through the Task tool. Each subagent has its own description, prompt, and tools.*

- The coordinator's `allowedTools` must include `"Task"`. Without it the coordinator cannot spawn subagents.
- Each subagent has an `AgentDefinition` with a description (used to choose it), a system prompt, and a restricted tool list.

Docs note: newer Agent SDK releases name this tool `Agent`. The exam guide calls it the Task tool.

Task statements: 1.3

### Subagents start with nothing
*Subagents do not inherit the coordinator's history. Pass complete findings in structured form.*

The synthesis subagent knows only its system prompt and the prompt the coordinator writes for it. Put the complete findings from search and analysis directly into that prompt. Separate content from metadata so attribution survives:

```json
{
  "findings": [
    {
      "claim": "US office vacancy reached 19.6% in Q4 2023",
      "evidence": "national vacancy rate rose to 19.6 percent",
      "source_url": "https://example.com/report-q4-2023",
      "source_name": "Brokerage quarterly report",
      "published": "2024-01-15",
      "page": 4
    }
  ]
}
```

Task statements: 1.3, 5.6

### Parallel subagents
*Emit several Task calls in one coordinator response.*

The coordinator issues one Task call for search and one for analysis in the same response, so both run at once. Calls spread across separate turns run one after another. Measure the latency of both designs in your build.

Task statements: 1.3

### Goals and criteria, not procedures
*Tell subagents what good looks like and let them adapt.*

Weak: "Search Google for 'office vacancy 2023', open the first five results, copy the numbers."

Strong: "Find vacancy, rent, and sublease data for at least eight major metros across North America, Europe, and Asia, 2020–2026. Prefer primary sources (brokerage reports, government statistics). For every figure, return the claim, an excerpt, the source URL, and the publication date. Report gaps you could not fill."

Task statements: 1.3

### Tool distribution
*Each agent gets only the tools for its role, plus narrow cross-role tools for frequent needs.*

| Subagent | Tools |
|---|---|
| Web search | `web_search`, `load_document` (validates document URLs, replaces a generic `fetch_url`) |
| Document analysis | `extract_data_points`, `summarize_content`, `verify_claim_against_source` |
| Synthesis | `verify_fact` for simple fact checks only. Deeper checks go back through the coordinator |
| Report | Write access to the output location |

Giving every agent every tool increases selection errors and leads to misuse, such as synthesis running its own searches.

Task statements: 2.3, 2.1

### Debug case 6: narrow coverage
*All agents succeeded, so the assignment was wrong.*

Root cause: the coordinator decomposed the topic into too few subtopics. Fix: have the coordinator plan coverage across regions before it delegates. Add an iterative refinement loop: the coordinator checks the synthesis for gaps, sends targeted queries to search and analysis, and runs synthesis again until coverage is sufficient.

Task statements: 1.2

### Debug case 7: timeout
*Recover locally if you can. Otherwise return structured context, and the coordinator continues.*

The search subagent retries the transient failure itself. If it still fails, it returns structured error context: failure type (timeout), the attempted query, partial results, and alternatives (another source, a narrower query). The coordinator decides to retry, reroute, or proceed. The report then carries a coverage annotation such as "2024 vacancy data: one source only, primary source unavailable".

Wrong moves: return an empty result marked as success, return a generic "search unavailable", or end the whole workflow.

Task statements: 5.3, 2.2

### Debug cases 8 and 9: conflicts and dates
*Keep both values with their sources. Require dates so time differences do not look like contradictions.*

Case 8: the analysis subagent keeps both values and annotates the conflict with source attribution. The coordinator decides how to reconcile before synthesis. The report shows both figures in a "contested" section with each source's method, such as the market set and vacancy definition.

Case 9: require publication or collection dates in every subagent output. Four years separate the surveys, so the difference is a trend.

Structure the report with separate sections for well-established and contested findings. Render content by type: financial data as tables, news as prose, technical findings as lists.

Task statements: 5.6

### Debug case 10: lost attribution
*Summaries compress away claim-source links unless the format forces them to survive.*

Require structured claim-source mappings from every subagent. Instruct synthesis to preserve and merge them, never to drop them. Place a key-findings summary at the start of long aggregated inputs, with section headers, to reduce the lost-in-the-middle effect.

Task statements: 5.6, 5.1

## Check yourself

- You can say why `"Task"` must appear in the coordinator's `allowedTools`.
- Your synthesis prompt contains the findings themselves, not a reference to "the earlier research".
- Every finding carries claim, evidence, source, and date.
- You return partial results and coverage gaps instead of failing silently or failing the workflow.
- Conflicting credible values both appear in the report with their sources.
