---
owner: governance
source_repo: chuxorg/chux-pleximesh-librarian
approval_authority: guardian
authorizing_actor: human
effective_at: 2026-01-24T22:56:23Z
version: v0.1
---

# Task Authorization: LIB-003 (v0)

## Authorization Event

- task_id: LIB-003
- version: v0
- status_change: Planned -> Active
- effective_at: 2026-01-24T22:56:23Z
- authorizing_actor: human

## Phase Association

- library/governance/phases/PHASE-LIBRARY-HARDENING.v0.md

## Governing PR Policy

- library/governance/policies/engineer/pr-policy.v0.md

## Implementation Assignment

- Engineer

## Execution Expectations (Non-Scope-Expanding)

- Duplicate artifact_id + version: hard fail import; emit clear error; no partial commit.
- Missing or malformed version in filename/metadata: reject artifact; log import error; continue if transactional safety allows.
- Invalid content type or unreadable file: reject artifact; emit import error with file path.
- Checksum mismatch (post-read vs computed): hard fail that artifact; do not store.
- Conflicting "latest" semantics: do not infer; store exactly as versioned.
- Partial import failure: prefer transactional import; otherwise record per-artifact results and ensure no silent success.
- Re-import of identical content: treat as duplicate; do not overwrite; emit idempotency warning/event.

## Non-Goals (Must Be Enforced)

- No preservation of legacy Mongo structure or object IDs.
- No filesystem reads during agent execution beyond seed import.
- No write APIs exposed beyond import path.

## Revision History

- 2026-01-24: Authorization recorded.
