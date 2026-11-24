---
paths:
  - "src/api/**/*"
---

# API handler conventions

- Handlers are `async` and return `Result<T, ApiError>`.
- Validate input with the schemas in `src/api/schemas/` before any database call.
- Map errors to HTTP status codes in one place: `src/api/errors.ts`.
