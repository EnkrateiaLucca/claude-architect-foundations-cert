---
description: Run the team code review checklist on the current diff
argument-hint: [optional focus area]
---

Review the current git diff against the team checklist. Focus: $ARGUMENTS

Report only these categories:
1. Bugs: logic that produces a wrong result for some input.
2. Security: injection, secrets in code, missing authorization checks.
3. Missing tests for changed behavior.

Skip style comments and patterns that already appear elsewhere in the codebase.
For each finding give: file:line, issue, severity (high/medium/low), suggested fix.
