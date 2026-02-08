artifact_id: CANON_EXECUTION_PROTOCOL
version: v1
class: RULE
authority: Human
status: Authoritative

purpose:
  Define the canonical execution workflow governing how Humans, Agents,
  and the Librarian plan, execute, verify, and recover work without drift.

scope:
  Applies to all projects governed by the Canon.
  Overrides informal or ad-hoc agent behavior.

states:

  DISCOVERY:
    description:
      Open-ended discussion between Human and ChatGPT.
    properties:
      - Non-authoritative
      - No artifacts required
    allowed:
      - Brainstorming
      - Design discussion
      - Risk analysis
      - Architecture exploration
    prohibited:
      - Execution
      - Artifact mutation
      - Agent tasking

  REQUIREMENTS:
    description:
      Phase or feature requirements agreed by the Human.
    properties:
      - Authoritative once accepted
      - Stored as a single Requirements artifact
    allowed:
      - Functional requirements
      - Non-functional constraints
      - Scope boundaries
    prohibited:
      - Task execution
      - Partial acceptance

  PLANNED:
    description:
      Work decomposed into ordered tasks.
    properties:
      - Stable task identifiers
      - Explicit dependencies
    allowed:
      - Task listing (titles only)
      - Dependency ordering
    prohibited:
      - Procedural detail
      - Execution

  EXECUTE:
    description:
      Deterministic task execution by Agents.
    entry_condition:
      Human issues explicit EXECUTE command.
    properties:
      - Prompt-only communication
      - No discussion or explanation
    mandatory_checks:
      - Clean working tree
      - Correct branch
      - No untracked changes
    allowed:
      - Agent-specific prompts
      - Code changes
      - Immediate commits per task
    exit_conditions:
      - Human decision required
      - Contract or rule violation
      - Environmental ambiguity
    exit_behavior:
      Automatic transition to DISCOVERY.

  SNAPSHOT:
    description:
      Immutable capture of project state at phase boundary.
    properties:
      - Mandatory at end of every phase
      - Additive relative to prior snapshots
      - Immutable once stored
    contents:
      - Phase identification
      - Completed scope
      - Newly frozen elements
      - Active next scope
      - Out-of-scope declarations
      - Authoritative artifact references

roles:

  Human:
    responsibilities:
      - Declare state transitions
      - Approve requirements
      - Issue EXECUTE
      - Resolve decision points

  ChatGPT (Guardian):
    responsibilities:
      - Detect violations
      - Halt execution on ambiguity
    limitations:
      - No approvals
      - No silent corrections

  Agent:
    responsibilities:
      - Execute assigned tasks only
      - Verify clean state before execution
      - Commit work immediately
      - Open PR after phase completion
    prohibitions:
      - Scope expansion
      - Helpful reinterpretation
      - Silent fixes

  PM Agent:
    responsibilities:
      - Review PRs
      - Verify scope compliance
      - Approve or reject merges

  Librarian:
    responsibilities:
      - Store authoritative artifacts
      - Maintain versions and checksums
      - Resolve Packs
      - Serve seed injection payloads
    authority:
      MongoDB is the system of record.

invariants:
  - No execution without EXECUTE.
  - No artifact mutation outside EXECUTE.
  - No discussion during EXECUTE.
  - No recovery without Snapshots.
  - Artifact formats are invariant; enforcement is configurable.
