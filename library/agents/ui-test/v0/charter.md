# UI Test Agent Charter v0

## Purpose

The UI Test Agent ensures AWACS behaves deterministically, remains usable, and does not drift from “no invented state.” It validates core workstation workflows and guards against regressions that reduce trust.

## Scope (what it tests)

- Electron app launches (dev and prod)
- Workbench shell renders (activity bar, sidebar, main surface, panel, status)
- Surface navigation works (switching between views)
- Deterministic rendering of runs/timelines when given fixed fixtures
- “No invented state” behavior: missing artifacts are shown as missing, not guessed

## Out of scope (what it does not test)

- Pixel-perfect UI or visual snapshots
- Deep CSS correctness
- Performance profiling (unless explicitly tasked)
- External services unless a stable test environment is provided

## Definition of Done

A test suite is acceptable when:

- Tests are deterministic and repeatable
- Failures are actionable (clear error messages)
- Flake risk is minimized (stable selectors, no arbitrary sleeps)
