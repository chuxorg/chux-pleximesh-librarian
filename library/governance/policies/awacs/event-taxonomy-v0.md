# AWACS Event Taxonomy v0

**Phase A — Observability Core**

## Purpose

This taxonomy defines the **canonical event types** emitted by agents and system components during Phase A.

Its goals are to:

* Make all agent activity observable
* Support correlation and replay
* Avoid inference or hidden state
* Remain stable while process evolves

> If something meaningful happens and no event is emitted, it is a bug.

---

## Universal Event Envelope (REQUIRED)

Every event, regardless of type, MUST conform to this envelope.

```json
{
  "event_id": "uuid",
  "timestamp": "ISO-8601",
  "agent_id": "string",
  "agent_role": "ui | guardian | librarian | intake | system",
  "event_type": "string",
  "correlation_id": "string",
  "severity": "info | warning | error",
  "payload": {}
}
```

### Field Notes

* `correlation_id` ties events to:

  * a task
  * a gate
  * a prompt execution
* `severity` is **descriptive**, not actionable (Phase A is non-blocking)

---

## Event Categories

Phase A defines **five** event categories.

---

## 1. Task Events

Emitted by agents performing work.

### `task.started`

```json
{
  "event_type": "task.started",
  "payload": {
    "task_id": "string",
    "task_name": "string"
  }
}
```

### `task.completed`

```json
{
  "event_type": "task.completed",
  "payload": {
    "task_id": "string",
    "result": "success | partial | failed"
  }
}
```

### `task.abandoned`

```json
{
  "event_type": "task.abandoned",
  "payload": {
    "task_id": "string",
    "reason": "string"
  }
}
```

---

## 2. Artifact Events

Emitted when artifacts are discovered, ingested, or reconciled.

### `artifact.discovered`

```json
{
  "event_type": "artifact.discovered",
  "payload": {
    "path": "filesystem path",
    "source": "agent | filesystem | api"
  }
}
```

### `artifact.ingested`

```json
{
  "event_type": "artifact.ingested",
  "payload": {
    "canonical_uri": "central-librarian://...",
    "content_hash": "sha256",
    "canonical": false
  }
}
```

### `artifact.superseded`

```json
{
  "event_type": "artifact.superseded",
  "payload": {
    "old_uri": "central-librarian://...",
    "new_uri": "central-librarian://..."
  }
}
```

### `artifact.flagged`

```json
{
  "event_type": "artifact.flagged",
  "severity": "warning",
  "payload": {
    "canonical_uri": "central-librarian://...",
    "issue": "missing-metadata | duplicate | conflict | unknown-type"
  }
}
```

---

## 3. Gate Events (Guardian-Centric)

These events **observe** gate behavior in Phase A.
They do **not** block execution.

### `gate.evaluated`

```json
{
  "event_type": "gate.evaluated",
  "payload": {
    "gate_id": "string",
    "inputs_checked": [
      "central-librarian://..."
    ]
  }
}
```

### `gate.observed_pass`

```json
{
  "event_type": "gate.observed_pass",
  "payload": {
    "gate_id": "string",
    "decision_uri": "central-librarian://..."
  }
}
```

### `gate.observed_block`

```json
{
  "event_type": "gate.observed_block",
  "severity": "warning",
  "payload": {
    "gate_id": "string",
    "missing_inputs": [
      "central-librarian://..."
    ]
  }
}
```

---

## 4. Process Anomaly Events

Used to surface **process bugs without blocking**.

### `process.anomaly_detected`

```json
{
  "event_type": "process.anomaly_detected",
  "severity": "warning",
  "payload": {
    "anomaly_type": "missing-artifact | divergent-state | duplicate-authority",
    "details": "string"
  }
}
```

These events are later mined to harden the SDLC.

---

## 5. System Events

Emitted by AWACS / Librarian itself.

### `system.started`

```json
{
  "event_type": "system.started",
  "payload": {
    "component": "awacs | librarian | intake"
  }
}
```

### `system.healthcheck`

```json
{
  "event_type": "system.healthcheck",
  "payload": {
    "component": "string",
    "status": "healthy | degraded"
  }
}
```

---

## Phase A Rules of Engagement

1. **Every artifact ingestion emits an event**
2. **Every Guardian evaluation emits an event**
3. **No silent failure**
4. **No inferred state**
5. **Events are append-only**

If an agent can’t emit an event, that’s a Phase A bug.

---

## Canonical Storage Location

This taxonomy MUST be stored as canon.

### Librarian Canonical URI

```
central-librarian://governance/awacs/event-taxonomy-v0.md
```

### Filesystem Seed (for ingestion only)

```
governance/awacs/event-taxonomy-v0.md
```

---

## What This Unlocks Immediately

* AWACS UI wiring (everything is driven by events)
* Intake Agent emission rules
* Guardian observability without blocking
* Replayable execution timelines
* Process bug harvesting

---
