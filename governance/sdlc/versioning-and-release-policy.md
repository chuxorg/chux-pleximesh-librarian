## Versioning & Release Policy — AWACS

**Location**

```
governance/sdlc/versioning-and-release-policy.md
```

```md
# AWACS Versioning & Release Policy

## Status

Authoritative SDLC Policy  
Enforced by PM and Guardian  
Applies to: chux-pleximesh-awacs

---

## Purpose

This document defines how AWACS source code is versioned, released, and promoted
across environments. The goal is **tight control, traceability, and zero ambiguity**
between tasks, commits, artifacts, and deployed state.

This policy intentionally starts simple and will evolve.

---

## Branch Model (Authoritative)

AWACS uses three long-lived branches:

- `master` — Production / released state
- `qa` — QA validation and acceptance
- `dev` — Active integration branch

Rules:

- No agent commits directly to `master` or `qa`
- All work originates from `dev`
- Promotion flows only forward:  
  `dev → qa → master`

---

## Working Branches (Mandatory)

Any agent performing work that touches source control MUST:

1. Create a local working branch from `dev`
2. Use the naming convention:
```

<agent>/<task-slug>

```
Examples:
- `ui/mission-rail-scaling`
- `engineer/authority-matrix-hooks`

3. Limit scope strictly to the assigned task

Working branches are temporary and MUST be deleted after merge.

---

## Commit Discipline

After **every prompt execution** that results in code changes:

- Commit locally
- Push to origin
- Reference the task in the commit message

Uncommitted or locally-held changes are prohibited.

---

## Pull Requests

### Creation
- All merges into `dev` require a Pull Request
- UI Agent MUST create PRs for UI-related work
- PR base branch: `dev`

### PR Requirements
Each PR MUST include:
- Linked task reference
- Summary of changes
- Links to Librarian artifacts that justify the change
- Confirmation that Persistence Law was followed

---

## QA Promotion

- Merging `dev → qa` represents **candidate acceptance**
- QA Agent validates:
- Functional correctness
- UI contract
- Governance compliance
- No feature work occurs on `qa`

---

## Production Release

- Merging `qa → master` represents a **release**
- Only PM may authorize release merges
- Guardian must approve any governance-impacting changes

---

## Versioning Scheme (Initial)

Until formal semantic versioning is introduced:

- `master` represents the current released version
- Releases MAY be tagged manually:
```

awacs-v0.x

```
- No agent may invent version numbers independently

A formal versioning scheme (e.g., semantic versioning) will be introduced in a future iteration.

---

## Tags

Tags are:
- Created on `master` only
- Applied at release time
- Authored by PM (or Guardian if governance-related)

Tags represent immutable historical state.

---

## Task ↔ Code Integrity

Rules:
- Every task MUST map to commits
- Every commit MUST map to a task
- Every PR MUST map to one primary task

If task state and repository state diverge:
- Work stops
- PM reconciles
- Guardian escalates if needed

---

## Enforcement

Violations of this policy result in:
- Immediate block of progress
- Task reassignment
- Escalation to Guardian for repeated offenses

---

## Guiding Principle

AWACS is built like a control system, not a startup demo.

Releases must be:
- Traceable
- Auditable
- Intentional

Speed is acceptable. Sloppiness is not.
```
