# Changelog

## v0.1.0 — 2026-10-25

- Package a FastAPI application in a Python 3.12 image running as user 10001.
- Run API and PostgreSQL 16 together through Docker Compose.
- Add liveness and database readiness endpoints, plus startup healthchecks.
- Create and list tasks through PostgreSQL-backed HTTP endpoints.
- Validate and trim task titles; reject invalid request bodies with HTTP 422.
- Keep local database configuration in an ignored `.env` file and provide an example.
- Store PostgreSQL data in a named volume and verify persistence after container recreation.
- Document setup, commands, acceptance results, and release scope.
