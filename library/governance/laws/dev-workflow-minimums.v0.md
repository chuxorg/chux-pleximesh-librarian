# Dev Workflow Minimums (v0) — PlexiMesh Governance Law

## Purpose

This law defines the minimum development workflow required to prevent drift, ensure reproducibility, and keep PlexiMesh safe as multiple agents and humans contribute concurrently. These rules are intentionally lightweight and are enforceable by process immediately, and by automation/events later.

This law is **MVP-critical**.

---

## Scope

Applies to:

- Runtime/Core repositories
- AWACS/UI repositories
- Governance/Library repositories
- Documentation repositories

Applies to work performed by:

- Humans
- Agents (PM, Engineer, Librarian, Documentation, Guardian, etc.)

---

## Branching Rules

1. **No direct commits to `development`**

   - All changes MUST be made on a named branch.

2. Branch naming MUST follow:

   - `feature/<short-description>`
   - `fix/<short-description>`
   - `chore/<short-description>`

3. Branches MUST be rebased or merged with `development` frequently enough to avoid long-running divergence.

---

## Pull Request Rules

1. All changes MUST enter `development` via a Pull Request (PR).
2. A PR MUST include:

   - A clear summary of intent and scope
   - A list of files changed (or link to diff)
   - Test results (see “Test Gate” below)

3. PRs MUST be scoped:

   - Prefer small PRs that map to a single task group or checkpoint.

4. Backup/legacy code MUST NOT silently break builds:

   - If backup sources exist, they MUST be excluded from builds via ignore tags or stored outside build paths.

---

## Test Gate (Required)

1. Runtime changes MUST pass:

   - `go test ./...`

2. If the repo includes integration suites, the PM MAY designate additional required commands per phase gate.
3. A PR MUST NOT be merged if required tests fail.

---

## Approval & Merge Authority

1. **PM is the merge authority** for `development`.
2. Guardian is a governance authority, but does not merge code.
3. If the PM is unavailable, merge authority may be temporarily delegated, but the delegation MUST be recorded as a decision artifact or event.

---

## Workflow Enforcement

These rules MUST be enforced in one of two ways:

### Mode A — Manual Enforcement (Allowed for MVP)

- PM reviews PRs and verifies test gate output before merge.
- PM confirms contract alignment (lifecycle/envelope/gates) for Phase 1 work.

### Mode B — Automated Enforcement (Post-MVP / Recommended)

- CI blocks merge on test failures.
- CI verifies required artifacts exist for the phase (phase gate checks).
- CI validates schema/law references are not broken (link integrity checks).

Manual enforcement is acceptable for MVP, but automation SHOULD be added as soon as practical.

---

## Drift Prevention Requirements (Agents)

1. Agents MUST work from an up-to-date base:

   - Before starting work, agents MUST pull/rebase from `development`.

2. Agents MUST not operate on stale context:

   - If an agent’s plan depends on files likely to have changed, it MUST refresh from repo state before editing.

3. Agents MUST not merge their own work:

   - Agents may open PRs and report status; PM merges.

---

## Release Readiness (MVP Minimal Definition)

A “release candidate” is defined as:

- `development` at a commit where required test gates pass
- Phase checkpoints A–D (for the current phase) are satisfied
- The Phase Gate artifact (if enabled) is approved

Formal versioning and tagging are defined in a separate release law (post-MVP).

---

## Non-Goals

- This law does not define branching strategies beyond minimum safety.
- This law does not define semantic versioning, tags, or packaging.
- This law does not require CI today, but it strongly recommends it post-MVP.
