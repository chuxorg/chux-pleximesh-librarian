## AWACS v0 Event Stream UI — File Locations

This artifact is an **operational UI specification**, not governance law, but it *does* govern how AWACS observes the system. That means:

* It **must be persisted in Mongo via the Librarian**
* It **must also have a filesystem seed**

---

## 1. Authoritative Location (Mongo via Librarian)

This is the **source of truth** once ingested.

```
central-librarian://governance/awacs/ui/event-stream-v0.md
```

**Classification:**

* artifact_type: `governance-ui`
* phase: `phase-a`
* status: `observability-core`
* canonical: `true`

All agents and AWACS itself should reference this URI when reasoning about or implementing the Event Stream panel.

---

## 2. Filesystem Seed Location (for ingestion only)

This is where the file should live in the repo so the **Librarian Intake Agent can discover it**.

```
governance/awacs/ui/event-stream-v0.md
```

Once ingested:

* The filesystem copy is **not authoritative**
* Mongo is the only trusted copy

---

## 3. Code Implementation Location (Non-Authoritative)

These are **implementation artifacts**, not canon.

```
awacs/ui/event-stream/
├── EventStream.tsx
├── EventRow.tsx
├── EventFilters.tsx
└── eventStream.types.ts
```

These files:

* Are produced by agents
* Must be ingested by the Librarian
* Are **never** treated as canon
* Can be superseded freely

---

## Locked Rule Going Forward

For anything we define, I will always state:

1. **Canonical Librarian URI** (Mongo authority)
2. **Filesystem seed path** (ingestion source)
3. **Implementation path** (non-authoritative output)

No exceptions.

---

## Next Step (Do Not Pause Phase A)

You can now:

1. Create `governance/awacs/ui/event-stream-v0.md`
2. Let the Intake Agent ingest it
3. Start wiring the Event Stream UI to Mongo `events`

