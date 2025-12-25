---
artifact_type: governance
rule_name: execution_evidence_rule
version: v1
owner: guardian
scope: process
effective_date: 2025-12-21
---

## Rule
Every execution must emit a prompt artifact before work begins and a result artifact immediately after completion, with both artifacts ingested by the Librarian intake service.

## Requirements
- **Pre-execution prompt:** The initiating agent records the intent, context, and root execution identifier via the Librarian before acting.
- **Post-execution result:** The executing agent records the observed outcome referencing the originating prompt and execution identifiers.
- **Correlation:** All artifacts cite the same `root_execution_id`, and results reference the issued `prompt_id`.
- **Intake target:** Artifacts are submitted through the Librarian REST endpoint (or its successor transport) so they are stored under the canonical directories.

These requirements do **not** block execution; agents may proceed as soon as the prompt is emitted and must submit the result as soon as practical after completion.

### Exceptions
- **Librarian maintenance:** Changes to the intake service itself may be logged using alternate evidence flows while the service is unavailable.
- **Sandbox / experimental mode:** Explicit Guardian authorization allows temporary suspension when experiments would otherwise flood the ledger.

## Rationale
Prompt/result evidence provides the minimal proof necessary for replay, auditing, and post-hoc analysis without introducing heavy process. Recording through the Librarian ensures institutional memory survives agent turnover and enables future AWACS subscriptions.
