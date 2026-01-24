---
owner: governance
source_repo: chuxorg/chux-pleximesh-librarian
approval_authority: guardian
authorizing_actor: human
effective_at: 2026-01-24T23:02:31Z
version: v0.1
---

# Task Authorization: LIB-004 (v0)

## Authorization Event

- task_id: LIB-004
- version: v0
- status_change: Planned -> Active
- effective_at: 2026-01-24T23:02:31Z
- authorizing_actor: human

## Phase Association

- library/governance/phases/PHASE-LIBRARY-HARDENING.v0.md

## Governing PR Policy

- library/governance/policies/engineer/pr-policy.v0.md

## Implementation Assignment

- Engineer

## Execution Expectations (Non-Scope-Expanding)

- OpenAPI version: 3.1.
- Canonical path: librarian/openapi/librarian.v0.yaml.
- Schemas align exactly with canonical artifact model.
- Examples included for all read endpoints.
- Explicit error models (404, 409, 422, 500).
- Deterministic "latest active version" resolution documented.

## Postman Project (Derived Artifact)

- Maintain/update existing Postman project from OpenAPI spec.
- Treat Postman collection as derived (non-authoritative).
- Requests must cover:
  - GET /artifacts/{artifact_id}
  - GET /artifacts/{artifact_id}?version=vX
  - Typed aliases (tasks/policies/phases)
  - Query listing
  - Health endpoint
- Keep collection in sync with spec changes.

## Non-Goals (Must Be Enforced)

- No authentication or permissions.
- No write APIs beyond documented import path.
- No divergence between spec and implementation.

## Revision History

- 2026-01-24: Authorization recorded.
