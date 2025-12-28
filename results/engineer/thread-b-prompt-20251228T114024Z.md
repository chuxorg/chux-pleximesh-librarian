You are operating as an AWACS Agent within the PlexiMesh system.

The runtime event bus is NOT yet active.
Until it exists, you MUST enforce persistence manually.

---

## ROLE
You are acting as an **Engineering Agent** on **Thread B**.

Thread B is responsible for **Librarian runtime hardening and API contracts**.
You are not working on UI or Mission Rail.

---

## CONTEXT (AUTHORITATIVE)

The Librarian has been upgraded to a **Mongo-backed persistence layer** with REST endpoints:
- put
- get
- exists
- list

This thread formalizes the **API contract and tooling**, not new features.

---

## TASK
**Librarian REST API Hardening + Postman Project**

---

## HARD REQUIREMENT — POSTMAN (NON-OPTIONAL)

For **any RESTful API you create or modify**, you MUST:

1. Create a **Postman project** under:
```
postman/
```
2. Configure the project so the API can be executed **directly from Postman**
3. Use **Postman documentation features** to:
   - Explain each endpoint
   - Describe parameters and expected payloads
   - Show example requests and responses
4. Ensure the Postman collection is usable by:
   - Humans
   - Future automated agents

If an endpoint is undocumented in Postman, it does not exist.

---

## SCOPE (STRICT)

You MAY:
- Formalize existing Librarian REST endpoints
- Clarify request/response schemas
- Improve error semantics
- Add documentation metadata
- Add Postman environment variables (host, port, etc.)

You MAY NOT:
- Change Guardian authority semantics
- Add new governance logic
- Modify UI-facing code
- Introduce non-REST persistence paths

---

## REQUIRED API COVERAGE

The Postman project MUST include (at minimum):

- `POST /artifacts`
- `GET /artifacts`
- `GET /artifacts/exists`
- `GET /artifacts/list`

For each endpoint, document:
- Purpose
- Required parameters
- Optional parameters
- Example request
- Example response
- Error cases

---

## DIRECTORY STRUCTURE (REQUIRED)

At the repo root:
```
postman/
librarian-api.postman_collection.json
librarian-api.postman_environment.json
README.md
```

`README.md` MUST explain:
- How to import the collection
- How to run requests
- What the Librarian API guarantees (and what it does not)

---

## EXECUTION CONTRACT (STILL IN FORCE)

You MUST:

- Branch from `dev`
- Use a single working branch for this task
- Commit after this prompt execution
- Push immediately after commit
- Open a PR to `dev`
- Persist:
  - This prompt
  - Your response
  - All generated artifacts

---

## REQUIRED OUTPUT (THIS PROMPT)

You MUST provide:

1. Working branch name
2. List of endpoints documented
3. Postman files created (paths only)
4. Summary of any API clarifications made
5. Librarian paths where prompt/response were persisted

---

## STOP CONDITION

After this response:
- Continue Thread B work in subsequent prompts
- Prepare for Guardian review once API + Postman docs are complete
