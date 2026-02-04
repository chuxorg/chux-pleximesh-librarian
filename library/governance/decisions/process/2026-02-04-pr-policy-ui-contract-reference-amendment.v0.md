---
owner: governance
source_repo: chuxorg/chux-pleximesh-librarian
approval_authority: guardian
authorizing_actor: human
effective_at: 2026-02-04T19:58:59Z
version: v0.1
---

# Policy Amendment: pr-policy UI Contract Reference (v0)

## Artifact

- artifact_id: pr-policy
- version: v0
- kind: policy
- domain: engineering/governance
- status: canonical
- content_type: text/markdown
- path: library/governance/policies/engineer/pr-policy.v0.md
- checksum_sha256: 3c1c333f20a2e1a84f6cb074f445fab4746670507ac87013465bbdced9836cef

## Amendment

- Adds explicit reference to UI-CONTRACT-AWACS.v1 for UI structure and zone immutability.
- Requires prior UI contract revision + authorization artifact for PRs that modify frozen UI structure or zones.
- No other PR rules, scopes, or enforcement mechanisms changed.

## Events Emitted

- event_id: ARTIFACT-AMENDED-2026-02-04-PR-POLICY-UI-CONTRACT-REFERENCE
  type: artifact.amended

## Revision History

- 2026-02-04: UI contract immutability clause added.
