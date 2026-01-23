# UI Test Determinism Policy v0

## Rule: Tests must be deterministic

- Prefer fixed fixtures and mocked data sources.
- Avoid network calls unless explicitly testing integration in a stable environment.

## Rule: No time-based flake

- Do not use arbitrary sleeps.
- Use explicit waits for UI conditions (element visible, text present, etc.).

## Rule: Stable ordering

When verifying timelines or lists:

- Assert ordering rules that match product logic (timestamp + stable tiebreak)
- Do not assume incidental ordering from DOM insertion unless product specifies it

## Rule: “No invented state”

If data is missing, expected UI must show “missing/unknown” states.
Tests must reject UIs that fabricate missing facts.
