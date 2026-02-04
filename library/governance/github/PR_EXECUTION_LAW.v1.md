# PR Execution Law (v1)

## Status

Constitutional Law
Deprecated

Superseded by PR_EXECUTION_LAW.v2 due to incomplete agent authority and credential handling.

---

## Authority

Canonical
Applies to: all_agents

---

## Law

### 1. Agent Authority

Agents are explicitly authorized to:

* Create git branches
* Commit changes
* Push branches to remote repositories
* Open GitHub Pull Requests
* Update PR descriptions and metadata

This authority applies when acting within assigned scope.

### 2. Credential Handling

Agents may use GitHub credentials provided via:

* `.env.local`
* Environment variables

Agents must not log, persist, or expose credentials.

Failure to access credentials must halt execution and be reported.

### 3. PR Atomicity

Each PR must represent one coherent unit of intent.

UI, runtime, backend, infra changes must not be mixed.

If scope contamination is detected, the agent must stop.

### 4. PR Scope Declaration

Every PR must explicitly state:

* What changed
* What did not change
* Known deviations or tolerances

### 5. Verification Requirement

Before opening a PR, agents must:

* Confirm the app builds / launches
* Confirm no unrelated files changed
* Confirm compliance with governing Laws

### 6. Failure Behavior

If PR creation fails, the agent must:

* Stop immediately
* Report the exact error
* Not attempt workarounds
