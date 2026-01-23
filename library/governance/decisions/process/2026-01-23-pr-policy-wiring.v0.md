---
owner: governance
source_repo: chuxorg/chux-pleximesh-librarian
approval_authority: guardian
effective_date: 2026-01-23
version: v0.1
---

# Policy Wiring Decision: pr-policy (v0)

## Intent

Record the wiring for the Engineer PR policy so it is enforceable, auditable,
and referenced by the appropriate agents during PR creation and review.

## Policy

- name: pr-policy
- version: v0
- path: library/governance/policies/engineer/pr-policy.v0.md
- purpose: Engineer Pull Request scope enforcement and drift prevention.
- mode: strict (default)

## Agents Affected

- Engineer: mandatory prompt inclusion.
- PM: review-time reference.
- Guardian: review-time reference.

## Wiring

- Authoritative registry entry recorded.
- Engineer, PM, and Guardian boot-packs reference the policy.

## Exception Handling

- Scope exceptions require explicit declaration and Guardian authorization.

## Effective Date

2026-01-23

## Linked Artifacts

- library/_reports/canonical-layout.v0.yaml
- library/_reports/inventory.v0.yaml
- library/agents/engineer/v0/boot-pack.v0.yaml
- library/agents/pm/v0/boot-pack.v0.yaml
- library/agents/guardian/v0/boot-pack.v0.yaml

## Revision History

- 2026-01-23: Initial wiring decision.
