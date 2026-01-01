# AWACS Theming Model (v0)

## 1. Theming Principles
- **Semantic meaning over decoration:** Every color/style token corresponds to a runtime concept (status, severity, authority, gating, interaction, background).
- **Accessibility-first:** Tokens must meet contrast/readability guidelines in light and dark modes; color is always paired with text/icons for redundancy.
- **Minimal visual noise:** Neutral bases and limited accents keep the UI calm; highlight only actionable changes.
- **Operator clarity under load:** Visuals remain legible and low-stress during prolonged monitoring sessions.

## 2. Core Semantic Tokens
| Category | Tokens & Meaning |
| --- | --- |
| **Status** | `status.idle`, `status.active`, `status.blocked`, `status.completed`, `status.aborted` |
| **Severity** | `severity.info`, `severity.warning`, `severity.error` |
| **Authority** | `authority.human`, `authority.maestro`, `authority.guardian`, `authority.system` |
| **Execution / Gating** | `gating.allowed`, `gating.blocked`, `gating.escalated` |
| **Interaction** | `interaction.focus`, `interaction.selection`, `interaction.hover`, `interaction.disabled` |
| **Background Layers** | `background.app`, `background.panel`, `background.surface`, `background.overlay` |

Each token represents a color + typographic treatment; no specific palette is dictated here.

## 3. Mapping Rules
- **Mandatory usage:** Mission rail badges, run/timeline chips must use `status.*`. Testing Agent findings and alerts must use `severity.*`. Maestro, Guardian, Human panels must use `authority.*`. Gate indicators use `gating.*`. Interaction states across lists/timelines use `interaction.*`. All layout layers use the appropriate `background.*`.
- **Prohibited usage:** Components may not introduce custom/ad-hoc colors; status/severity hues cannot be repurposed for branding or decoration. Interaction tokens must never imply state (only focus/selection/hover). Authority colors must remain unique to their roles.
- **Combining tokens:** When status overlaps severity (e.g., blocked + error), severity drives the accent color; status is communicated via icon/label. Gating tokens may sit beside severity text when a gate fails—colors must remain distinguishable.

## 4. Light / Dark Mode Assumptions
- `background.*` tokens invert between modes while maintaining contrast. Status/severity/authority hues adjust brightness/saturation but retain meaning. Interaction tokens adapt to remain visible on the current background.
- Semantic meaning is invariant: `status.blocked` always signifies a halt, no matter the palette. Contrast targets (WCAG AA+) must hold in both modes.

## 5. Relationship to Runtime Semantics
- **Testing Agent:** `severity.info/warning/error` align exactly with Testing Agent report levels.
- **Authority:** `authority.human/maestro/guardian/system` label panels, icons, and badges tied to those actors (e.g., Maestro guidance threads, Guardian “Why” cards).
- **Gating:** `gating.allowed/blocked/escalated` map directly to `execution.gate.evaluated` and `execution.gate.escalated` events so AWACS displays consistent visuals for gate outcomes.

## 6. Non-Goals (Current Phase)
- No user theme editing or palette customization.
- No branding or marketing color definitions.
- No animation or motion system work.
- No visual polish pass beyond semantic mapping.

This model is UI-framework agnostic, covers all current AWACS surfaces, aligns with the runtime event/severity model, and supports future theming without UI refactors.
