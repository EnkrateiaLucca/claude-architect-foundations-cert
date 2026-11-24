# D3 · Claude Code Configuration & Workflows

**20% of the exam · ≈ 12 items · 6 task statements · Scenarios:** Code Generation with Claude Code, Claude Code for Continuous Integration, Developer Productivity with Claude

This domain tests where each piece of Claude Code configuration lives and how you run Claude Code in a team and in CI. Most items describe a symptom, such as a teammate missing instructions, a CI job that hangs, or conventions applied in the wrong files. You answer by naming the right file, flag, or mode.

The decision rule: put each setting at the layer that matches who needs it and when. Shared team behavior goes in version-controlled project files. Personal behavior goes in your home directory. Conventions by file type go in path-scoped rules. Non-interactive runs use `-p`.

## Task statements

1. **3.1** Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization
2. **3.2** Create and configure custom slash commands and skills
3. **3.3** Apply path-specific rules for conditional convention loading
4. **3.4** Determine when to use plan mode vs direct execution
5. **3.5** Apply iterative refinement techniques for progressive improvement
6. **3.6** Integrate Claude Code into CI/CD pipelines

## Core concepts

### The CLAUDE.md hierarchy
*User-level files stay with one person. Project-level files travel with the repo.*

Claude Code reads CLAUDE.md files at three levels. Each level has a different audience.

| Level | Location | Who gets it | Shared through git? |
|---|---|---|---|
| User | `~/.claude/CLAUDE.md` | Only you, in every project | No |
| Project | `CLAUDE.md` at the repo root, or `.claude/CLAUDE.md` | Everyone who clones the repo | Yes |
| Directory | `CLAUDE.md` inside a subdirectory | Anyone working in that part of the tree | Yes |

The classic diagnosis item: a new team member does not get the team's coding standards. The cause is that the standards live in a senior developer's `~/.claude/CLAUDE.md`. That file applies only to its owner. The fix is to move the standards into the project-level CLAUDE.md and commit it.

Use `/memory` to see which memory files Claude Code loaded in the current session. Run it first when behavior differs between sessions or between teammates.

Task statements: 3.1

### Keep CLAUDE.md modular with @import and .claude/rules/
*Import only the standards each package needs. Split a monolith into topic files.*

A single large CLAUDE.md gets hard to maintain and loads text that most tasks do not need. Two tools keep it focused.

**`@import`** pulls an external file into a CLAUDE.md. Each package can import only the standards that apply to it:

```markdown
# packages/billing/CLAUDE.md
Billing service. Money values are integers in cents.

@../../standards/api-conventions.md
@../../standards/pci-handling.md
```

The package maintainer chooses the imports, because that person knows which standards matter for the package.

**`.claude/rules/`** holds topic-specific rule files as an alternative to one monolithic CLAUDE.md:

```
.claude/rules/
  testing.md
  api-conventions.md
  deployment.md
```

Task statements: 3.1

### Path-scoped rules load only for matching files
*YAML `paths:` globs apply conventions by file type, in any directory.*

A rule file in `.claude/rules/` can carry YAML frontmatter with a `paths` field. The rule loads only when Claude edits a file that matches one of the globs. This cuts irrelevant context and token usage.

```markdown
---
paths: ["**/*.test.tsx", "**/*.test.ts"]
---
# Testing conventions
- Use React Testing Library queries by role, not by test ID.
- One behavior per test. Name tests "does X when Y".
- Use the fixtures in tests/fixtures/ instead of inline mock data.
```

```markdown
---
paths: ["terraform/**/*"]
---
# Terraform conventions
- Every resource has owner and cost-center tags.
```

| Convention applies to | Use |
|---|---|
| Files of one type spread across the codebase (tests, migrations, stories) | `.claude/rules/` file with a glob in `paths` |
| Everything inside one directory | Subdirectory CLAUDE.md, or a rule with `paths: ["dir/**/*"]` |
| Every task in the repo | Project CLAUDE.md |

Directory-level CLAUDE.md files are bound to one directory. Test files that sit next to the code they test (`Button.test.tsx` next to `Button.tsx`) live in dozens of directories. A glob rule covers all of them with one file.

Task statements: 3.3

### Slash commands: project vs user scope
*`.claude/commands/` is shared through git. `~/.claude/commands/` is personal.*

A custom slash command is a markdown file. The file name becomes the command name.

| Location | Scope | Use for |
|---|---|---|
| `.claude/commands/review.md` in the repo | Every developer who clones or pulls | Team checklists such as `/review` |
| `~/.claude/commands/review.md` | Only you | Personal shortcuts |

```markdown
<!-- .claude/commands/review.md -->
Review the staged diff against our checklist:
1. Input validation at every API boundary.
2. No secrets or tokens in code or logs.
3. New behavior has tests.
Report each finding as file:line, issue, severity, suggested fix.
```

Commands are not defined in CLAUDE.md, and Claude Code has no `.claude/config.json` with a commands array. Options that propose either are invented features.

Task statements: 3.2

### Skills and their frontmatter
*Skills load on demand. `context: fork`, `allowed-tools`, and `argument-hint` shape how they run.*

A skill is a directory under `.claude/skills/` with a `SKILL.md` file. Frontmatter configures how it runs.

```markdown
---
name: analyze-codebase
description: Map modules, entry points, and dependencies of an unfamiliar codebase.
context: fork
allowed-tools: Read, Grep, Glob
argument-hint: "<directory to analyze>"
---
Analyze $ARGUMENTS. Return a summary of at most 40 lines:
modules, entry points, external dependencies, and risky areas.
```

| Frontmatter | Effect | Use when |
|---|---|---|
| `context: fork` | Runs the skill in an isolated sub-agent context. Only the result returns to the main session | The skill produces verbose output (codebase analysis) or exploratory content (brainstorming alternatives) |
| `allowed-tools` | Restricts the tools the skill can use | You want to prevent destructive actions, for example by allowing only read or write operations |
| `argument-hint` | Prompts the developer for a required parameter | The developer may invoke the skill with no arguments |

**Skills vs CLAUDE.md.** CLAUDE.md loads in every session, so it holds universal standards. A skill loads when someone invokes it, so it holds task-specific workflows. Putting a long, occasional workflow in CLAUDE.md wastes context in every session. Putting a universal standard in a skill means it applies only when someone remembers to invoke it.

**Personal variants.** To change a team skill for yourself, create a copy in `~/.claude/skills/` under a different name. Editing the shared skill affects every teammate.

Docs note: current Claude Code docs treat custom commands and skills as one system. Files in `.claude/commands/` still work. The exam keeps the two locations separate.

Task statements: 3.2

### Plan mode vs direct execution
*Plan when the stem names architecture, many files, or several valid approaches. Execute directly when the scope is clear.*

Plan mode lets Claude explore the codebase and design an approach before it changes files. It prevents costly rework on large or ambiguous tasks.

| Signal in the stem | Mode |
|---|---|
| Restructure a monolith into microservices | Plan mode |
| Library migration that touches 45+ files | Plan mode |
| Choose between integration approaches with different infrastructure needs | Plan mode |
| Single-file bug fix with a clear stack trace | Direct execution |
| Add one date validation check to one function | Direct execution |
| Carry out a plan you already approved | Direct execution |

The common combination: plan the migration in plan mode, then execute the approved plan directly.

The trap option says "start in direct execution and switch to plan mode if complexity appears." When the stem already states the complexity, the complexity is known now. Plan first.

**The Explore subagent** isolates verbose discovery. It reads many files, then returns a summary to the main conversation. Use it during long multi-phase tasks so discovery output does not exhaust the main context window.

Task statements: 3.4

### Iterative refinement with evidence
*Show examples, write tests first, let Claude interview you, and batch interacting fixes.*

When Claude's output misses the target, give it better evidence. More adjectives in the prose description rarely help.

| Problem | Technique |
|---|---|
| Prose description of a transformation gets interpreted inconsistently | Give 2–3 concrete input/output examples |
| You need correct behavior across edge cases and performance limits | Write the test suite first, then iterate by sharing test failures |
| You are working in an unfamiliar domain | Interview pattern: ask Claude to question you first (cache invalidation, failure modes) |
| One edge case keeps failing (for example, nulls in a migration script) | Give a specific test case with example input and expected output |
| Several issues where one fix affects another | Describe all of them in one detailed message |
| Several independent issues | Fix them one at a time |

Example of an input/output pair that settles an ambiguous request:

```text
Input:  "  Jane   DOE "     Output: "Jane Doe"
Input:  "o'neil, PAT"       Output: "Pat O'Neil"
Input:  ""                  Output: null
```

Task statements: 3.5

### Claude Code in CI/CD
*`-p` for non-interactive runs, JSON output for machine parsing, an independent instance for review.*

```bash
claude -p "Review this PR for security issues. Report only new or unaddressed findings." \
  --output-format json \
  --json-schema review-schema.json
```

| Need | Mechanism |
|---|---|
| The job hangs waiting for input | Add `-p` (or `--print`). Claude processes the prompt, prints to stdout, and exits |
| Findings a script can post as inline PR comments | `--output-format json` with `--json-schema` |
| Testing standards, fixtures, and review criteria in CI | Project CLAUDE.md, which CI-invoked Claude Code reads |
| Re-run after new commits without duplicate comments | Include prior findings in context. Ask for only new or still-unaddressed issues |
| Generated tests repeat existing coverage | Provide the existing test files in context |
| Low-value generated tests | Document valuable test criteria and available fixtures in CLAUDE.md |

A minimal schema for review findings:

```json
{
  "type": "object",
  "properties": {
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "file": {"type": "string"},
          "line": {"type": "integer"},
          "severity": {"enum": ["critical", "high", "medium", "low"]},
          "issue": {"type": "string"},
          "suggested_fix": {"type": "string"}
        },
        "required": ["file", "line", "severity", "issue"]
      }
    }
  },
  "required": ["findings"]
}
```

**Session context isolation.** The session that generated code keeps the reasoning that produced it. It is less likely to question its own decisions. Run the review in a separate, independent Claude instance.

`CLAUDE_HEADLESS=true`, `--batch`, and redirecting stdin from `/dev/null` are distractors. The first two do not exist. The third is a Unix workaround that does not address Claude Code's command syntax.

Task statements: 3.6

## Traps

| Wrong option sounds like | Pattern | Why it loses | Right move |
|---|---|---|---|
| "Put the team standards in `~/.claude/CLAUDE.md`" | Wrong layer | User-level files are not shared through version control | Project CLAUDE.md, committed |
| "Define the command in a `.claude/config.json` commands array" | Invented feature | That mechanism does not exist | `.claude/commands/` in the repo |
| "Consolidate all conventions in root CLAUDE.md and let Claude infer the section" | Prompt as policy | Relies on inference, not explicit path matching | `.claude/rules/` with `paths` globs |
| "A CLAUDE.md in every directory that has tests" | Wrong layer | Directory files are bound to one directory; tests are spread everywhere | One glob rule such as `**/*.test.tsx` |
| "Make a skill for each code type's conventions" | Wrong layer | Skills load on demand, so conventions would not apply automatically | Path-scoped rules |
| "Start direct, switch to plan mode if it gets complex" | Wrong trigger | The stem already states the complexity | Plan mode first |
| "Set `CLAUDE_HEADLESS=true`" or "add `--batch`" | Invented feature | Neither exists | `claude -p` |
| "Ask the same session to review its own code more carefully" | Unreliable proxy | The generator keeps its reasoning context | Independent review instance |
| "Rewrite the instructions with more detail" after inconsistent transformations | Wrong lever | Prose is the thing being misread | 2–3 input/output examples |

## Self-check

### A new hire's Claude Code sessions ignore the team's naming conventions. Everyone else's sessions follow them. What is the likely cause and fix?
The conventions live in someone's user-level `~/.claude/CLAUDE.md`. Move them to the project CLAUDE.md and commit it. Use `/memory` to confirm which files load.

### Storybook stories live next to components in 30 folders. Where do story conventions go?
A file in `.claude/rules/` with frontmatter `paths: ["**/*.stories.tsx"]`. It loads only when Claude edits a matching file, in any folder.

### A codebase-analysis skill floods the main chat with hundreds of lines. What frontmatter fixes it?
`context: fork`. The skill runs in an isolated sub-agent context and returns only its result.

### You want developers prompted for a ticket ID when they run a skill with no arguments. Which frontmatter field does that?
`argument-hint`.

### Which mode fits "add a null check to `parse_date()` given this stack trace"?
Direct execution. The change is small, in one function, and the cause is clear.

### Your CI step runs `claude "Generate tests for changed files"` and never finishes. Why?
Claude Code is waiting for interactive input. Add `-p` so it prints the result and exits.

### After a new commit, the automated review reposts the same five comments. What do you change?
Include the prior findings in the review context and instruct Claude to report only new or still-unaddressed issues.

### Two bugs in a migration script interact: fixing the date parsing changes which rows hit the null handler. One message or two?
One detailed message covering both. Interacting issues need to be fixed together. Independent issues can go one at a time.
