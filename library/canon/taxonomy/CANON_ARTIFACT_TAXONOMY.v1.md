artifact_id: CANON_ARTIFACT_TAXONOMY
version: v1
class: RULE
authority: Human
status: Authoritative

purpose:
  Define the closed set of canonical artifact classes used by the Canon.
  Eliminate ambiguity in artifact meaning, storage, and enforcement.

scope:
  Applies to all Canon-governed projects and libraries.
  No artifact may exist outside these classifications.

artifact_classes:

  RULE:
    intent:
      Invariants that must never be violated.
    characteristics:
      - Global or scoped authority
      - Rarely change
      - Guardian-enforced

  CHARTER:
    intent:
      Define the role, powers, and limits of an Agent.
    characteristics:
      - Role-scoped
      - Stable across phases
      - Referenced by Packs

  SEED:
    intent:
      Declarative state vector for rehydration.
    characteristics:
      - Zero-prose
      - Declarative only
      - Injected at session start

  PROMPT:
    intent:
      Executable instructions to a specific Agent.
    characteristics:
      - Ephemeral
      - Non-authoritative alone
      - Contextual to EXECUTE

  SNAPSHOT:
    intent:
      Authoritative capture of state at phase boundary.
    characteristics:
      - Immutable
      - Additive
      - Recovery-critical

  PACK:
    intent:
      Bundle references required to initialize a session or Agent.
    characteristics:
      - Reference-only
      - No embedded truth
      - Resolved by Librarian

storage_authority:
  system_of_record: MongoDB
  disk_role:
    - cache
    - export
    - bootstrap only

constraints:
  - Every artifact MUST declare its class.
  - Artifacts MUST NOT span classes.
  - Formats are invariant.
  - Enforcement is policy-driven.
  - Recovery relies on Rules, Seeds, and Snapshots only.
