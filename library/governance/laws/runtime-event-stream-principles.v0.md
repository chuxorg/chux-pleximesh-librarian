# Runtime Event Stream Principles (v0)

Source: `library/runtime/event-stream/v0/run-event-stream.v0.yaml`

- All events MUST be associated with a run_id
- Events without a valid run_id are invalid
- System events define execution truth
- Event ordering must be deterministic per run
