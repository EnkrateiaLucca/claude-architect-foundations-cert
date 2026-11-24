# Project instructions

Shared with every developer through version control. Personal preferences go in `~/.claude/CLAUDE.md`, which teammates never see.

## Universal standards

- TypeScript strict mode. No `any` without a comment that says why.
- Run `npm test` before you say a change is done.
- Never edit files under `generated/`.

## Imported standards

@docs/coding-standards.md

Topic rules live in `.claude/rules/`. Rules with a `paths` field load only when Claude works on matching files.
