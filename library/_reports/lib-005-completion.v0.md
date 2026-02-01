# LIB-005 Completion Report (v0)

Generated: 2026-01-25T12:45:00Z

## Test Execution
Smoke tests executed via `tools/lib005_smoke_tests.py` against `http://localhost:8000`.

Tests:
- GET /artifacts/{artifact_id} (latest active)
- GET /artifacts/{artifact_id}?version=vX (exact version)
- GET /tasks/{task_id}
- GET /policies/{policy_id}
- GET /phases/{phase_id}
- GET /artifacts (filters + ordering)
- Invalid version (400)
- Invalid filter (400)
- Unknown path (404)
- Not found (404)

Results:
- All tests passed. See `library/_reports/lib-005-smoke-tests.v0.yaml`.

## Failures Found
- Version validation rejected valid `v0` values due to a regex escape bug.
- Read validation rejected empty policy content, causing 500 responses for seeded policies.
- Spec/task example mismatch: `/tasks/ENG-UI-001` returns 404 because status is planned.

## Fixes Applied
- Corrected version regex to accept `vN` values.
- Allowed empty string content while preserving checksum validation.
- Updated OpenAPI spec and Postman assets to reflect correct behavior and examples.

## Registered Artifacts
- OpenAPI spec update: `librarian/openapi/librarian.v0.yaml`
- Postman collection update: `postman/librarian-api.postman_collection.json`
- Smoke test results: `library/_reports/lib-005-smoke-tests.v0.yaml`

## References
- Smoke test script: tools/lib005_smoke_tests.py
- OpenAPI spec: librarian/openapi/librarian.v0.yaml
- Postman guide: postman/README.md
