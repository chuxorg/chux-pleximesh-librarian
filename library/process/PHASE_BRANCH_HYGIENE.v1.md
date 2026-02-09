artifact_id: PHASE_BRANCH_HYGIENE
version: v1
kind: process_contract_addendum
status: active
authority: system
scope: global
mutability: locked
related_contracts:
  - PHASE_COMPLETION_CONTRACT.v1

# Phase Branch Hygiene Rules

This addendum supplements the Phase Completion Contract and is
mandatory for all agent-driven execution phases.

## Phase Branch Invariant

Each phase MUST operate on exactly one working branch.

* The branch is created or checked out at phase start.
* All work for the phase occurs on this branch.
* No additional branches may be created during the phase.

Recommended naming:

* `phase/<domain>-<phase-id>`
  (example: `phase/ui-phase-2`)

## Working Tree Cleanliness

At the following boundaries, the working tree MUST be clean:

* Phase start
* Between agent prompts
* Before snapshot creation
* Before PR creation

A clean working tree means:

* No uncommitted changes
* No untracked files

If the working tree is not clean at any boundary:

* Execution MUST stop immediately
* The agent MUST report the condition verbatim
* No further work may proceed until resolved

## Commit Discipline

* Agents may commit incrementally during a phase.
* Commits MUST occur on the phase branch only.
* Agents MUST NOT stash changes across prompts.

## Snapshot Integrity

* Snapshots MUST be created from a clean working tree.
* Snapshots taken from a dirty tree are INVALID.
* No rebasing or squashing is permitted after snapshot creation.

## Enforcement

* Violation of these rules invalidates phase completion.
* Any exception requires an explicit Architecture Decision Record (ADR).
