# Event Taxonomy Principles (v0)

Source: `library/runtime/events/v0/event-taxonomy.v0.yaml`

- System events describe ground truth and MUST always be emitted
- Mission events describe responses or side effects to events
- Missions may subscribe to system events but may not suppress them
- AWACS and Guardian must always receive system events
