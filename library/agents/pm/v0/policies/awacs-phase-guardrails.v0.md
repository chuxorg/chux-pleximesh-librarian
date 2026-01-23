# AWACS Phase Guardrails (PM Policy) v0

## Purpose

This policy governs how AWACS work is executed and merged during the AWACS phase. It exists to prevent irreversible architectural regressions and UI drift.

## Non-negotiable rules

1. **No direct pushes to main/master.**
2. **All work occurs on task branches** created from `development`.
3. **Engineer Agents create PRs**; **PM merges** into `development`.
4. **No “temporary hacks”** that violate guardrails. If a shortcut is required, it must be documented as an explicit waiver artifact with an expiration.

## Phase ordering (must be respected)

AWACS work must proceed in this order unless a PM waiver exists:

1. Electron hardening (preload bridge, isolation)
2. Dev loop (fast iteration)
3. Renderer modularization (Workbench + Surfaces)
4. Librarian read-only integration (Runs + Timeline)
5. UI test harness foundation (enables UI Test Agent)

## Architectural invariants (must not regress)

- **Renderer has no Node integration** once hardening lands.
- **AWACS is read-only** with respect to Librarian/runtime (until a later phase explicitly adds control actions).
- **No invented state**: UI must only render persisted artifacts/events; missing facts must be shown as missing.
- **Surfaces are modular** (no monolithic renderer file).
- **URIs are the identity** of artifacts; timelines are ordered deterministically.

## PR acceptance checklist (PM must verify)

### Security (ENG-001)

- [ ] `contextIsolation: true`
- [ ] `nodeIntegration: false`
- [ ] Preload exposes **minimal** APIs (no broad fs/process access)
- [ ] No unsafe IPC patterns (no “execute arbitrary command”)

### Dev loop (ENG-002)

- [ ] `npm run dev` exists and is documented
- [ ] Dev loop supports rapid renderer iteration (reload/hot reload)
- [ ] Production build still works (`npm run build && npm run electron`)

### Renderer structure (ENG-003)

- [ ] Renderer code is modular (Workbench + Surfaces)
- [ ] No “god file” reintroduced
- [ ] Typecheck passes
- [ ] No behavior regression in baseline observer and mission rail demo modes

### Librarian integration (ENG-004)

- [ ] Librarian access is read-only
- [ ] Runs are grouped by `header.correlation.root_execution_id`
- [ ] Timeline ordering is deterministic (timestamp + stable tiebreak)
- [ ] Missing data is shown as missing (no inference)

### UI test harness (ENG-005)

- [ ] `npm test` runs a UI smoke suite
- [ ] Selectors are stable (data-testid)
- [ ] Tests avoid flake patterns (no arbitrary sleeps)

## Required PR body sections

Every AWACS PR must include:

- Summary
- Changes
- How to test
- Risk/Notes
- Follow-ups (if any)

## Waivers

If a guardrail must be violated:

- Create a waiver artifact in the Library:

  - `library/governance/decisions/waivers/<date>-<slug>.v0.md`

- Must include:

  - rationale
  - blast radius
  - rollback plan
  - expiration condition (what must happen to remove the waiver)
