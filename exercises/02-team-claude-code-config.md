# 02 · Configure Claude Code for a team development workflow

**Domains:** D3, D2 · **Time:** 25 min · **Format:** Sorting drill + sample config (`exercises/team-config/`)

## Scenario

Code Generation with Claude Code. Eight developers share a TypeScript monorepo. API handlers live in `src/api/`. Test files sit next to the code they test (`Button.test.tsx` next to `Button.tsx`) in every directory. The team wants shared standards, a review command, a skill that maps unfamiliar modules without flooding the main session, and GitHub access through MCP. One developer also wants to try an experimental MCP server without affecting anyone else.

This drill follows Exercise 2 in Section 8 of the official Exam Guide.

## Your task

For each requirement, name the file path and the key setting. Then compare with the sample layout in `exercises/team-config/`.

1. Coding standards every developer gets on clone.
2. A personal instruction: "Explain changes in Portuguese."
3. Testing conventions that apply to every `*.test.tsx` file, wherever it lives.
4. API conventions that load only when Claude edits files under `src/api/`.
5. A `/review` command for the whole team.
6. A codebase-mapping skill that runs in isolation, may only read, search, and write its summary file, and prompts for a module path when invoked without one.
7. The GitHub MCP server for everyone, without committing the token.
8. The experimental MCP server for one developer.
9. A new hire says Claude ignores the team's testing standards. Everyone else gets them. How do you diagnose it?
10. For each task, choose plan mode or direct execution: (a) add a null check to one function with a clear stack trace, (b) migrate from one date library to another across 45 files, (c) add real-time notifications where WebSockets and polling are both viable.

## Reference answer

### Where each setting lives
*Shared means project scope in version control. Personal means user scope in your home directory.*

| # | Requirement | Location | Key setting |
|---|---|---|---|
| 1 | Shared standards | `CLAUDE.md` at the repo root (or `.claude/CLAUDE.md`) | `@docs/coding-standards.md` import keeps it modular |
| 2 | Personal instruction | `~/.claude/CLAUDE.md` | Applies to you only. Teammates never see it |
| 3 | Test conventions everywhere | `.claude/rules/testing.md` | `paths: ["**/*.test.tsx", "**/*.test.ts"]` |
| 4 | API conventions | `.claude/rules/api-conventions.md` | `paths: ["src/api/**/*"]` |
| 5 | Team `/review` | `.claude/commands/review.md` | Committed, so every clone has it |
| 6 | Mapping skill | `.claude/skills/codebase-map/SKILL.md` | `context: fork`, `allowed-tools: Read, Grep, Glob, Write`, `argument-hint: <module path>` |
| 7 | Shared GitHub MCP | `.mcp.json` at the repo root | `"Authorization": "Bearer ${GITHUB_TOKEN}"` expands from each developer's environment |
| 8 | Experimental MCP | `~/.claude.json` | User scope. Tools from both servers are available at the same time |

A personal variant of a team skill goes in `~/.claude/skills/` under a different name, so it never shadows the team's version.

Task statements: 3.1, 3.2, 3.3, 2.4

### Rules with globs versus directory CLAUDE.md
*Conventions for a file type that spans directories need a glob. Directory files cover one directory.*

`.claude/rules/testing.md` in the sample:

```markdown
---
paths:
  - "**/*.test.ts"
  - "**/*.test.tsx"
---

# Testing conventions
- One describe block per exported function or component.
- Use the fixtures in test/fixtures/.
```

The rule loads only when Claude works on a matching file, so it costs no context in other sessions. A `CLAUDE.md` in each directory would need a copy in every folder that holds tests. Putting every convention in the root `CLAUDE.md` makes Claude infer which section applies.

Task statements: 3.3

### Skills, commands, and CLAUDE.md
*CLAUDE.md is always loaded. Skills and commands run on demand.*

The sample skill:

```markdown
---
name: codebase-map
description: Map an unfamiliar module and write the summary to docs/maps/.
context: fork
allowed-tools: Read, Grep, Glob, Write
argument-hint: <module path, e.g. src/billing>
---
```

`context: fork` runs the skill in an isolated sub-agent context. The verbose exploration stays out of the main conversation, and only the summary returns. `allowed-tools` blocks destructive tools such as Bash during the skill. `argument-hint` prompts for the module path.

Use `CLAUDE.md` for standards that apply to every task. Use a skill for a task-specific workflow that someone invokes.

Task statements: 3.2

### MCP scopes and credentials
*Project scope for shared servers, user scope for experiments, environment variables for secrets.*

The sample `.mcp.json`:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": { "Authorization": "Bearer ${GITHUB_TOKEN}" }
    }
  }
}
```

Prefer an existing community or vendor MCP server for standard integrations such as GitHub or Jira. Build a custom server only for team-specific workflows. If Claude keeps using Grep where an MCP tool would do better, improve the MCP tool's description so it explains its capabilities and outputs.

Task statements: 2.4

### Diagnose the new hire
*Check which memory files load. The usual cause is user-level placement.*

Ask the new hire to run `/memory` to see which memory files are loaded. The usual cause: the testing standards sit in a teammate's `~/.claude/CLAUDE.md`, so only that person gets them. Move them into the project `CLAUDE.md` or `.claude/rules/` and commit.

Task statements: 3.1

### Plan mode or direct execution
*Plan when the task has architectural choices or touches many files. Execute directly when the scope is clear.*

| Task | Mode | Why |
|---|---|---|
| (a) Null check, clear stack trace | Direct execution | One file, clear scope |
| (b) Date library migration, 45 files | Plan mode, then direct execution | Plan the migration and its order, then execute the plan |
| (c) Notifications, WebSockets or polling | Plan mode | Several valid approaches with different infrastructure needs |

For a long discovery phase, the Explore subagent keeps verbose output out of the main context and returns a summary.

Task statements: 3.4

## Check yourself

- You put nothing personal in a committed file and nothing shared in your home directory.
- You can write a `paths` frontmatter block from memory.
- You can name the three skill frontmatter options the exam tests and what each does.
- You know that `${VAR}` in `.mcp.json` expands from the environment, so the secret never enters git.
- You reach for `/memory` first when instructions apply inconsistently.
