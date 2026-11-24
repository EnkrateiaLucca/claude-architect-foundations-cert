---
name: codebase-map
description: Map an unfamiliar module (entry points, call flow, dependencies) and write the summary to docs/maps/. Use when someone asks how a module works or where to start.
context: fork
allowed-tools: Read, Grep, Glob, Write
argument-hint: <module path, e.g. src/billing>
---

Map the module at $ARGUMENTS.

1. Use Glob to list its files and Grep to find its exported names and entry points.
2. Read only the files on the main call paths. Follow imports from the entry points.
3. Write `docs/maps/<module-name>.md` with: purpose, entry points, call flow, external dependencies, open questions.
4. Return a five-line summary and the path of the file you wrote.
