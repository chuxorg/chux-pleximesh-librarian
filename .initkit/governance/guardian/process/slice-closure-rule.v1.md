---
artifact_type: governance
rule_name: slice_closure_rule
version: v1
owner: guardian
scope: process
effective_date: 2025-12-21
---

## Rule
A slice may be closed when it has satisfied its acceptance criteria, passed its QA review, and has no unresolved blocking dependencies, even if the broader feature remains open.

## Closure Criteria
- **Acceptance criteria satisfied:** The functional conditions defined for the slice are demonstrably met.
- **QA passed:** The QA gate has completed and recorded its decision for the slice.
- **No blocking dependencies:** Upstream or downstream blockers are resolved or explicitly removed from the slice.

Feature completeness is **not** a prerequisite for slice closure; slices exist to deliver incremental value and evidence.

## Rationale
Closing slices as soon as they are definitionally done keeps throughput visible, enforces small-batch correctness, and prevents team cadence from being coupled to uncertain feature timelines. This rule preserves the Guardian’s focus on evidence-backed progress rather than subjective completeness.
