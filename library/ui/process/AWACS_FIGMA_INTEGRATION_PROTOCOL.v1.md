artifact_id: AWACS_FIGMA_INTEGRATION_PROTOCOL
version: v1
kind: ui-process
domain: ui
scope: awacs
status: canonical
authority: product-architecture
mutability: read-only

# AWACS_FIGMA_INTEGRATION_PROTOCOL

## 1. Purpose

This protocol defines the sanctioned use of Figma in the AWACS UI workflow.

Figma is treated as a **visual intent expression tool**, not a source of UI authority.

---

## 2. Authority Rules

* Figma MUST NOT introduce new UI regions
* Figma MUST NOT introduce new semantics
* Figma MUST NOT introduce interaction
* Figma MUST NOT redefine information architecture
* Figma changes are always considered **proposals**

Canonical authority remains with:

* UI State Report
* UI Information Architecture
* UI Operational Mode
* UI Requirements
* UI Change Review Checklist

---

## 3. Allowed Change Types

Figma MAY be used to propose:

* Positional adjustments (spacing, alignment)
* Visual hierarchy clarification (size, weight, grouping)
* Readability improvements
* Density adjustments
* Consistency corrections

---

## 4. Required Workflow

1. Human edits Figma
2. Atlas Figma plugin pulls updated design into ChatGPT
3. ChatGPT performs:

   * Delta analysis
   * Checklist compliance
   * Constraint validation
4. ChatGPT produces a **UI Agent change prompt**
5. UI Agent applies changes to implementation
6. Human visually verifies result
7. Repeat as needed

---

## 5. Prohibited Uses

* Figma Make auto-generation
* Freeform redesign
* AI-driven styling suggestions inside Figma
* Treating Figma as the "source of truth"

---

## 6. Failure Handling

If a Figma change violates any canonical artifact:

* The change MUST be rejected
* The violation MUST be explained
* A decision artifact MUST be created if the change is intentional

---

End of Protocol
