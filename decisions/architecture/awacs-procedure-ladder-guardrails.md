# AWACS Procedure Ladder — Guardrails for Multi-Parameter Operations

## Purpose

Define when sequential prompting (Procedure Ladder) is appropriate and when
simultaneous parameter entry is required.

---

## Rules

1. Sequential Mode (Default)

   - Used when parameters are dependent or order-sensitive
   - Each rung confirms state and provenance before proceeding

2. Simultaneous Mode (Allowed)
   - Used when parameters are independent and time-critical
   - UI must present a single confirmation surface
   - Partial submission is forbidden

---

## Acceptance Criteria

- Operator can see all parameters before execution
- Validation errors are surfaced inline
- Provenance and required state remain visible

---

## Charter Alignment

- UI-first (§3)
- Cockpit mentality (§4.1)
- Future extensibility (§6)
- Truthful observability (§8)
