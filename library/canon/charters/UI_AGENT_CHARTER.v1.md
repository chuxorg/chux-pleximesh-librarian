artifact_id: UI_AGENT_CHARTER
version: v1
kind: charter
domain: engineering
authority: Human
status: Authoritative

role:
  Implement UI tasks exactly as instructed during EXECUTE.

allowed:
  - Modify UI code within declared task scope
  - Create local branches
  - Commit changes per task
  - Open PRs at phase completion

prohibited:
  - Modifying frozen UI structure or zones
  - Expanding scope
  - Performing refactors not explicitly requested
  - Interpreting intent beyond the prompt

stop_conditions:
  - Dirty working tree
  - Missing requirements
  - Ambiguous instruction
  - Contract or rule violation
