artifact_id: PLEXIMESH_PHASE_SNAPSHOT_INIT
version: v1
kind: snapshot
domain: governance
authority: Human
status: Authoritative

phase:
  name: canon-bootstrap
  description: Initial Canon and Library MVC establishment
  status: complete

completed:
  - CANON_EXECUTION_PROTOCOL@v1
  - CANON_ARTIFACT_TAXONOMY@v1
  - UI_AGENT_CHARTER@v1
  - PM_AGENT_CHARTER@v1
  - GUARDIAN_CHARTER@v1
  - PROJECT_STATE_SEED@v1

frozen:
  - canon-laws
  - artifact-taxonomy
  - agent-charters
  - project-state-seed

active_next:
  - awacs-ui-execution
  - runtime-execution

out_of_scope:
  - feature-implementation-before-packs
  - agent-execution-without-packs

notes:
  This snapshot establishes the baseline state for all future recovery
  and Pack-based rehydration.
