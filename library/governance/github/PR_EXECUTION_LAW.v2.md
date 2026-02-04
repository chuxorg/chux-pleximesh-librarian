# PR Execution Law (v2)

## Status

Constitutional Law
Active

---

## Authority

Canonical
Applies to: all_agents_with_repo_access

## Supersedes

PR_EXECUTION_LAW.v1

---

## Law

### 1. Explicit Agent Authority

Any agent authorized to modify a repository is explicitly authorized to:

* Create branches from the canonical development branch
* Commit changes
* Push branches to the remote
* Open, update, and annotate GitHub Pull Requests

This authority applies to (non-exhaustive):

* Engineer Agent
* UI Agent
* Runtime Agent
* Infrastructure Agent

Restrictions on specific agents (e.g., QA Agent) remain governed by their role-specific policies.

### 2. Credential Handling (PATs / Tokens)

Agents may use credentials provided via:

* `.env.local`
* Environment variables

Credentials may be used only at execution time.

Credentials must:

* Never be committed
* Never be logged
* Never be persisted outside runtime memory

Failure to access credentials must halt execution and be reported verbatim.

This clause supersedes implicit or missing credential guidance elsewhere.

### 3. PR Atomicity (Canonical Rule)

Every Pull Request must represent one coherent unit of intent.

No mixed UI/runtime/backend/infra changes.

No task stacking.

Task-specific atomicity rules (e.g., ENG-UI-001) remain valid but subordinate.

If atomicity is violated or unclear, the agent must stop and escalate.

### 4. Branching Canonicalization

For repositories with conflicting branch terminology:

* Canonical development branch: dev
* PRs must target: dev
* Protected branches: main / master (repo-specific), qa (if present)

Where existing laws differ, this Law takes precedence.

### 5. PR Description & Verification

Before opening a PR, agents must verify:

* Only in-scope files changed
* App builds / launches (repo-appropriate command)
* Governing laws and policies are satisfied

Each PR description must state:

* What changed
* What did not change
* Known deviations or tolerances

### 6. Failure Behavior

If PR creation fails, the agent must:

* Stop immediately
* Report the exact error message
* Not attempt workarounds or retries unless instructed

---

## References (Informative, Not Duplicative)

* dev-workflow-enforcement.v0
* dev-workflow-minimums.v0
* gitops-policy.v0
* versioning-and-release-policy.v0
* pull-request-atomicity.v1
* pull-request-requirements.v0

---

## Discovery Keywords

PR, pull request, GitHub, agent execution, PAT
