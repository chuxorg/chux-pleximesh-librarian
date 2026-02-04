---
owner: governance
source_repo: chuxorg/chux-pleximesh-librarian
approval_authority: guardian
authorizing_actor: human
effective_at: 2026-02-03T14:11:09Z
version: v0.1
---

# Canonical Law Registration: PR_EXECUTION_LAW (v2)

## Artifact

- artifact_id: PR_EXECUTION_LAW
- version: v2
- kind: law
- domain: governance/github
- status: canonical
- authority: canonical
- applies_to: all_agents_with_repo_access
- content_type: text/markdown
- path: library/governance/github/PR_EXECUTION_LAW.v2.md
- checksum_sha256: 8a5a833f0d66dbc0f9b4c02319408f4e3ed8c0fbe62d924a93ef1f537a299dc7
- supersedes: PR_EXECUTION_LAW.v1

## Keywords

- PR
- pull request
- GitHub
- agent execution
- PAT

## Events Emitted

- event_id: ARTIFACT-CREATED-2026-02-03-PR-EXECUTION-LAW-V2
  type: artifact.created
- event_id: LAW-ACTIVATED-2026-02-03-PR-EXECUTION-LAW-V2
  type: law.activated

## Revision History

- 2026-02-03: Supersedes v1 with explicit agent authority, credential handling, and canonical branch rules.
