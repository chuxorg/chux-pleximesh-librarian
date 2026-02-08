artifact_id: PHASE_COMPLETION_CONTRACT
version: v1
kind: process_contract
status: active
authority: system
scope: global
mutability: locked

# Phase Completion Contract

A development phase is considered COMPLETE only when all of the
following conditions are met.

## Roles & Responsibilities

### CodeX (Implementation Agent)

* Implements changes defined for the phase
* Commits and pushes all changes
* Opens a Pull Request (PR)
* Does NOT declare the phase complete
* Does NOT create snapshots
* Does NOT interact with the Librarian

### UI Agent (State Capture Agent)

* Generates a snapshot of the current system state at phase end
* Snapshot must include:

  * commit SHA
  * repository
  * phase_id
  * authoritative artifacts in force
  * brief structural summary
* Registers the snapshot with the Librarian via REST API
* Reports snapshot artifact_id to the PM

### PM Agent (Phase Authority)

* Reviews the Pull Request
* Verifies:

  * changes match the phase scope
  * no out-of-scope modifications occurred
  * snapshot artifact exists and is registered
* Confirms PR includes the explicit statement:
  "Snapshot created and registered with Librarian"
* Declares the phase complete only after all checks pass

## Mandatory PR Requirements

Every phase-closing PR MUST include:

* Phase name and phase_id
* Summary of changes
* Explicit declaration of what was NOT changed
* Snapshot confirmation statement:
  "Snapshot created and registered: <artifact_id>"

PRs missing this statement must not be merged.

## Snapshot Authority

* Snapshots are authoritative historical records
* Snapshots must be immutable once registered
* A phase without a snapshot is considered INCOMPLETE

## Enforcement

* No subsequent phase may begin until this contract is satisfied
* Any deviation requires an explicit ADR
