# Sprint 2 – Execution Substrate Hardening

## Sprint Overview
- **Repo:** `chux-pleximesh-runtime`
- **Project:** PlexiMesh GitHub Project (existing)
- **Sprint Name:** `Sprint 2 – Execution Substrate Hardening`
- **Sprint Type:** Foundational / Tooling
- **Sprint Goal:** Harden the execution substrate only where Sprint 1 revealed friction, keeping git + filesystem as the sole authority.
- **Reference Sprint:** `Sprint 1 – Engineering: Agent Writes Code` (reference-only baseline)
- **Sprint State:** Armed (execution gates enabled; no tasks assigned)

## Refocus Doctrine
- Follow the principle: **Do not solve problems that have not been empirically observed.**
- Enforce emerging Agentic Programming Laws:
  1. Agents must not assume undeclared capabilities.
  2. Guardian gates must never be bypassed.
  3. No new system becomes authoritative before governing law exists.
  4. UI / observability instruments must reflect behavior, not control it.
- Scope must target execution, observability, and hygiene improvements observed during Sprint 1.

## Mandated Themes
All backlog items must be labeled with exactly one of:
`execution-environment`, `agent-runner`, `canon-sync`, `event-sink`, `observability`.

## Sprint Backlog (Active Only)
Each active issue is mechanical, non-subjective, and tied to Sprint 1 learnings. Assign all to Sprint 2 and label per theme.

### Theme: `execution-environment`

#### Issue: Minimal Agent Runner
**Description:** Define the minimal runner that invokes agents against a repository so executions are repeatable and Guardian-gated. The runner must standardize invocation, capture stdout/logs/events deterministically, and integrate with Guardian approval checkpoints.

**Acceptance Criteria:**
- Runner lifecycle (init, exec, teardown) is documented with concrete inputs/outputs.
- Output capture format for stdout/stderr and structured events is defined.
- Guardian approval hooks and abort semantics are incorporated, matching Sprint 1 gating.

### Theme: `canon-sync`

#### Issue: Read-Only Canon Presence Check
**Description:** Define a read-only verification step that ensures required Canon slices already exist locally (filesystem-only). No new datastore or authority is introduced; the check surfaces discrepancies to Guardian.

**Acceptance Criteria:**
- Process flow enumerates detection of required artifacts and verification of checksums using filesystem/git primitives only.
- Enforcement rules state that missing or tampered artifacts trigger Guardian-visible events without mutating Canon.
- Failure handling describes how execution halts pending Guardian decision.

### Theme: `agent-runner`

#### Issue: Event Sink v0 (Filesystem Append Log)
**Description:** Formalize an append-only event sink stored in the repo (or designated filesystem root) to persist correlation-aware events emitted during agent execution.

**Acceptance Criteria:**
- Schema covers correlation ID, causation ID, timestamps, severity, emitter role, and payload envelope.
- Persistence rules confirm durability and ordering guarantees using filesystem append semantics (no databases).
- Interfaces for writing/reading events are specified without implementation detail beyond filesystem usage.

### Theme: `event-sink`

#### Issue: Voodoo Auto-Hook (Non-Subjective)
**Description:** Define the automatic Voodoo audit hook that runs after each task completion. Hook must fail loudly when evidence is missing and record references to Canon artifacts, without reinterpreting scope.

**Acceptance Criteria:**
- Trigger points (post-task) and required events are enumerated with deterministic checks.
- Failure modes (missing evidence, discrepancies) emit blocking alerts and halt downstream automation.
- Hook output links to Canon references and correlation IDs exactly as observed.

### Theme: `observability`

#### Issue: Read-Only Observability Tap
**Description:** Produce a read-only view (e.g., log summaries) derived from filesystem events so humans can inspect execution without influencing it.

**Acceptance Criteria:**
- View references the filesystem event sink and presents Guardian-approved metadata only.
- No control-surface capabilities exist; outputs are static or append-only.
- Documentation states explicitly that observability tooling cannot modify execution state.

## Deferred Backlog Items (Do Not Execute)

### Execution Environment Capability Manifest
- **Status:** Deferred – speculative; no empirical trigger beyond Sprint 1 needs.
- **Note:** Revisit only after additional executions expose concrete capability gaps.

### MongoDB-backed Artifact Authority / Canon Database
- **Status:** Deferred – speculative storage; violates “filesystem + git as authority”.
- **Note:** Any datastore-backed authority requires Guardian law before reintroduction.

### UI or Control Surfaces Influencing Execution
- **Status:** Deferred – speculative; risks violating agentic law #4.
- **Note:** Observability remains read-only; no UI may alter execution state.

## Sprint Rules
- Do not assign tasks yet.
- Do not instantiate agents yet.
- Work is limited to empirically justified execution substrate hardening; no feature delivery.
- Backlog items must remain mechanical and non-subjective.

## Required Outputs
- Sprint 2 artifact (this document) remains the authoritative reference; it is now frozen under refocused scope.
- Backlog items must remain in the PlexiMesh GitHub Project under Sprint 2 (Armed) until Guardian authorizes task assignment.
- Emit `sprint.scope.refocused` after recording this update.
