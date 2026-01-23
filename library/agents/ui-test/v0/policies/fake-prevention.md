# UI Test Flake Prevention Policy v0

## Do not rely on timing

- No `sleep(1000)` patterns.
- Wait for explicit conditions: visibility, enabled state, content loaded markers.

## Isolate external dependencies

- Prefer mocked Librarian responses or fixture files.
- If integration tests are needed, they must:

  - run against a known local environment
  - have clear setup steps
  - fail fast with helpful diagnostics

## Keep tests small

- Smoke tests should validate the “happy path” only.
- Avoid chaining many UI actions in one test; split into focused tests.

## Debuggability requirements

Each failing test must output:

- which surface failed
- what selector was missing
- last known app state (run id if applicable)
- screenshot on failure (if harness supports it)
