# Conversation Rollover Protocol v1

## Purpose

Prevent context bloat, drift, and hidden state by enforcing clean conversation boundaries.

## Trigger Conditions

A rollover MUST occur when any of the following are true:

* Conversation latency noticeably increases
* Core assumptions are being re-explained
* Multiple artifacts are referenced implicitly instead of explicitly
* A new project phase begins
* Guardian or human flags risk

## Required Steps (Ordered)

1. Generate or update `PLEXIMESH_PROJECT_STATE_SNAPSHOT`
2. Confirm all relevant role seed prompts exist and are canonical
3. Archive artifacts via Librarian
4. Terminate current conversation intentionally
5. Start a new conversation using `MASTER_SEED_PROMPT`

## Prohibitions

* No partial rollovers
* No relying on chat memory
* No “we’ll remember this later”

## Authority

The Guardian may enforce rollover unilaterally.
Failure to comply is a protocol violation.

## Outcome

Each conversation is disposable.
The system state is not.
