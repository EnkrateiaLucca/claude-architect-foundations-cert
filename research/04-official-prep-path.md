# Official Prep Path: Claude Certified Architect – Foundations Prep Courses

Research date: 2026-11-24.

The Anthropic Partner Academy lists seven free courses for CCAR-F at https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses. The page says: "Complete these free courses on to help prepare yourself for the Claude Certified Architect - Foundations certification exam." [source: https://anthropic-partners.skilljar.com/page/claude-certified-architect-foundations-prep-courses]

Foundations has a prep-courses *page*, not a multi-module prep *path* like the Professional exam. `https://anthropic-partners.skilljar.com/path/claude-certified-architect-foundations` returns HTTP 404. The exam prep index describes the Foundations entry only as "Prepare for the Claude Certified Architect Foundations Exam". [source: https://anthropic-partners.skilljar.com/page/claude-certification-exam-prep-courses]

The FAQ calls the exam guide "the authoritative source for exam scope" and says prep coverage "varies by certification". [source: https://anthropic-partners.skilljar.com/page/faq-certifications]

The notes below record only the public structure of each course (title, blurb, curriculum headings). Course content is not reproduced here. Label conventions: `[source: url]` for fetched pages, `[inferred]` for my analysis.

## Mapping to the exam blueprint

The mapping is an inference from curriculum headings. Anthropic does not publish it. [inferred]

| Prep course | Product tag | Exam domains it serves | Priority |
|---|---|---|---|
| Building with the Claude API | Claude Developer Platform | D1 (agent loop, workflows), D2 (tool use), D4 (structured data, prompting, batches) | High |
| Introduction to Model Context Protocol | Claude Code, Claude Developer Platform | D2 (tools, resources, prompts) | High |
| Claude Code in Action | Claude Code | D3 (CLAUDE.md, skills, hooks, plan mode, headless, GitHub Actions), D5 (compaction) | High |
| AI Fluency: Framework & Foundations | AI fluency | Background on delegation and discernment; no task statement maps directly | Low |
| Claude 101 | Claude Enterprise | Background on the Claude apps; no task statement maps directly | Low |
| Claude with Amazon Bedrock | Claude Developer Platform | Same API topics as the Claude API course. Cloud provider configuration is out of scope | Only if you deploy on AWS |
| Claude on Google Cloud | Claude Developer Platform | Same API topics. Cloud provider configuration is out of scope | Only if you deploy on Google Cloud |

## Course structures

### Building with the Claude API
Blurb: "This comprehensive course covers the full spectrum of working with Anthropic models using the Claude API". Prerequisites: Python, basic JSON. [source: https://anthropic-partners.skilljar.com/claude-with-the-anthropic-api]

Curriculum sections: Introduction · Accessing Claude with the API (requests, multi-turn, system prompts, temperature, streaming, structured data) · Prompt evaluation (eval workflow, test datasets, model- and code-based grading) · Prompt engineering techniques (clear and direct, specific, XML tags, examples) · Tool use with Claude (tool functions, schemas, message blocks, tool results, multi-turn with tools, multiple tools, fine-grained tool calling, text edit tool, web search tool) · RAG and Agentic Search · Features of Claude (extended thinking, images, PDFs, citations, prompt caching, code execution and Files API) · Model Context Protocol (clients, tools, inspector, resources, prompts) · Anthropic apps (Claude Code, computer use) · Agents and workflows (parallelization, chaining, routing, agents and tools, environment inspection). [source: https://anthropic-partners.skilljar.com/claude-with-the-anthropic-api]

For CCAR-F, skip RAG, embeddings, image support, prompt caching internals, and computer use: the guide lists them as out of scope. [source: G10 §17] [inferred]

### Introduction to Model Context Protocol
Blurb: "Learn to build Model Context Protocol servers and clients from scratch using Python. Master MCP's three core primitives—tools, resources, and prompts". One learning outcome: "Understand when to use each MCP primitive: tools (model-controlled), resources (app-controlled), and prompts (user-controlled)". [source: https://anthropic-partners.skilljar.com/introduction-to-model-context-protocol]

Curriculum: Introduction (Introducing MCP, MCP clients) · Hands-on with MCP servers (project setup, defining tools, server inspector) · Connecting with MCP clients (implementing a client, defining and accessing resources, defining prompts, prompts in the client) · Assessment and wrap-up. [source: https://anthropic-partners.skilljar.com/introduction-to-model-context-protocol]

Building servers is useful practice, but hosting MCP servers is out of scope for the exam. [source: G10 §17] [inferred]

### Claude Code in Action
Blurb: "Run long, hands-off Claude Code sessions you can trust: steer, configure, automate, and verify". [source: https://anthropic-partners.skilljar.com/claude-code-in-action]

Curriculum: Steer the Work (Steering Long Sessions) · Configure Claude (A CLAUDE.md That Follows, Verification Skills, Permission Modes, Hooks) · Automate Repeat Work (Scheduled tasks and headless, GitHub Actions and Code Review) · Verify and Share (Verifying Unsupervised Runs, Plugins) · Course Quiz. Learning outcomes name plan mode, directed compaction, the rewind menu, a lean CLAUDE.md, skills, permission modes, hooks, headless mode, and the GitHub action. [source: https://anthropic-partners.skilljar.com/claude-code-in-action]

### AI Fluency: Framework & Foundations
Blurb: "Learn to collaborate with AI systems effectively, efficiently, ethically, and safely". Curriculum: the 4D Framework (Delegation, Description, Discernment, Diligence), generative AI fundamentals, capabilities and limitations, effective prompting techniques, the Description-Discernment loop. [source: https://anthropic-partners.skilljar.com/ai-fluency-framework-foundations]

### Claude 101
Blurb: "Learn how to use Claude for everyday work tasks, understand core features, and explore resources for more advanced learning". Curriculum: Meet Claude, projects, artifacts, skills, connecting tools, enterprise search, research, use cases by role. [source: https://anthropic-partners.skilljar.com/claude-101]

### Claude with Amazon Bedrock · Claude on Google Cloud
Both mirror the Claude API course on a cloud platform: requests, multi-turn, system prompts, streaming, structured data, prompt evaluation, prompt engineering, tool use. [source: https://anthropic-partners.skilljar.com/claude-in-amazon-bedrock] [source: https://anthropic-partners.skilljar.com/claude-with-google-vertex]

## Related free courses not on the prep page

The Partner Academy catalog also has three short courses that map closely to CCAR-F task statements. They are not on the official prep page. [inferred]

| Course | Curriculum | Task statements |
|---|---|---|
| [Introduction to subagents](https://anthropic-partners.skilljar.com/introduction-to-subagents) | What are subagents? · Creating a subagent · Designing effective subagents · Using subagents effectively | 1.2, 1.3, 3.4, 5.4 |
| [Introduction to agent skills](https://anthropic-partners.skilljar.com/introduction-to-agent-skills) | What are skills? · Creating your first skill · Configuration and multi-file skills · Skills vs. other Claude Code features · Sharing skills · Troubleshooting skills | 3.2 |
| [Model Context Protocol: Advanced Topics](https://anthropic-partners.skilljar.com/model-context-protocol-advanced-topics) | Sampling · notifications · roots · transports (STDIO, StreamableHTTP) | 2.4 (transport and hosting detail is out of scope) |

[source: https://anthropic-partners.skilljar.com/introduction-to-subagents] [source: https://anthropic-partners.skilljar.com/introduction-to-agent-skills] [source: https://anthropic-partners.skilljar.com/model-context-protocol-advanced-topics]

## What the guide itself prescribes

Section 7 "How to Prepare" and Section 8 "Preparation Exercises" are the guide's own prep path. They are hands-on: build an Agent SDK agent with escalation logic, configure Claude Code for a team, build an extraction pipeline with batches, and debug a multi-agent research pipeline. The courses above give background; the four exercises are the closest match to the exam's scenarios. [source: G10 §7–8] [inferred]

G10 = the official CCAR-F Exam Guide v1.0; v1.1 has identical Sections 7, 8, and 17. See `01-exam-guide.md`.
