# Pull Request Atomicity & Merge Strategy Policy v1

## Purpose

This policy defines how Pull Requests represent work, how they are reviewed, and how they are merged.

It exists to ensure:

- **Correctness and auditability**
- **Clear task boundaries**
- **Low process friction for Engineers**
- **Strong governance by PM and Guardian**

This policy intentionally decouples **task atomicity** from **commit count**.

---

## Core Principle

> **A Pull Request must represent exactly one task.
> A Pull Request does NOT need to contain exactly one commit.**

Atomicity is defined by **scope and verification**, not by commit count.

---

## Engineer Rules (Execution Phase)

Engineers:

- MAY create multiple commits while working on a task
- MAY push iterative fixes (lint, tests, normalization, etc.)
- MUST ensure all commits in a PR belong to the same task
- MUST NOT include unrelated changes or scope bleed
- MUST NOT include lockfiles or dependency changes unless explicitly required

Engineers:

- DO NOT decide the final merge shape
- DO NOT squash or rebase unless explicitly instructed

---

## Pull Request Scope Requirements (Hard Rules)

A PR is **not mergeable** if any of the following are true:

- Changes span multiple tasks (scope bleed)
- Verification evidence does not apply to the entire PR
- Required checks (lint/build/tests) do not pass
- Forbidden files are included (e.g. lockfiles without authorization)
- PR intent is ambiguous

These rules are enforced regardless of commit count.

---

## Verification Requirements (Unchanged)

Every PR must include evidence for all applicable steps:

```bash
npm install
npm run lint
npm run build
npm test
npm run dev   # if UI / Electron
```

Evidence must be:

- Reported in the PR description or comments
- Applicable to the entire PR
- Verifiable by the PM

---

## Merge Strategy (PM Authority)

The **PM decides the merge strategy** based on task type and PR contents.

### Allowed strategies

- **Squash merge**

  - Preferred for:

    - tooling changes
    - refactors
    - normalization / linting
    - tasks where commit history adds no audit value

- **Merge commit**

  - Preferred for:

    - feature development
    - multi-step changes where history matters
    - cross-cutting architectural work

Engineers do not choose the strategy.

---

## Guardian Authority

Guardian may:

- Require squash before merge
- Require rebase for clarity
- Block PRs with ambiguous scope
- Grant explicit waivers (rare)

Guardian will **not** block a PR solely because it has multiple commits.

---

## Explicitly Forbidden Practices

- Using commit count as a proxy for correctness
- Requiring cherry-pick gymnastics when scope is correct
- Forcing squash to “fix” scope bleed
- Merging PRs that are “mostly correct”

---

## Definition of Done

A PR is complete when:

- It represents exactly one task
- All verification gates pass
- Scope is clean and unambiguous
- PM has merged using an appropriate strategy

---

## Rationale

Early strictness around single-commit PRs was intentional to surface gaps.
Now that linting, tests, and governance are in place, commit-count rigidity no longer adds safety and actively harms throughput.

This policy reflects a **mature engineering system**.
