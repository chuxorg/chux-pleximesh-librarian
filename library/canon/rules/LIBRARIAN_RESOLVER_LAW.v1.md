artifact_id: LIBRARIAN_RESOLVER_LAW
version: v1
class: RULE
authority: Human
status: Authoritative

purpose:
  Define canonical resolver semantics for Librarian artifact loading.

scope:
  Applies to all Canon-governed packs and resolution operations.

resolver_tokens:

  "@LATEST":
    resolves_to:
      - highest non-deprecated canonical version of the referenced artifact
    guarantees:
      - deterministic at load time
    failure_mode:
      - fatal resolution error if no eligible version exists
    ordering:
      - resolve @LATEST before validation
