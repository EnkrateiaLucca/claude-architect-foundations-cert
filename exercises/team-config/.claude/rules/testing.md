---
paths:
  - "**/*.test.ts"
  - "**/*.test.tsx"
---

# Testing conventions

- One `describe` block per exported function or component.
- Use the fixtures in `test/fixtures/`. Do not build ad hoc mock data inline.
- Test behavior through the public API. Do not assert on private state.
- Every bug fix adds a test that fails before the fix.
