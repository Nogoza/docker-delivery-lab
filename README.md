# Docker Delivery Lab

A project for learning how to package a small Python API in Docker and run it
with PostgreSQL through Docker Compose.

**v0.1.0 — completed learning lab.** The API and database start together,
tasks are stored in PostgreSQL, and task data survives container recreation.

## Finish line

Run the API and PostgreSQL with `docker compose up --build`, create and list
tasks through the API, and show that data survives container recreation.

## Milestones

- [x] **API and image:** build the image and get an HTTP 200 response from `/health`.
- [x] **Compose and database:** run API and PostgreSQL together; add task creation and listing.
- [x] **Persistence and handoff:** recreate containers without losing task data, document the demo, and publish the project on GitHub.

The three acceptance criteria are complete. See [project summary](docs/project-summary.md)
for learning outcomes and [changelog](CHANGELOG.md) for release scope.

## Requirements

- Docker Engine
- Docker Compose v2
- `curl` for terminal requests

## Files to read first

- `app/main.py`: the API routes.
- `requirements.txt`: direct Python dependencies, pinned to checked versions.
- `Dockerfile`: the instructions used to build the image.
- `.dockerignore`: files excluded from the Docker build context.
- `compose.yaml`: API and database services, readiness checks, and the database volume.
- `app/db.py`: PostgreSQL connection and table creation.
- `.env.example`: a template for local configuration; the real `.env` is ignored by Git.

## Configure and run

On a fresh clone, create `.env` from the example if it does not exist:

```bash
if [ ! -f .env ]; then cp .env.example .env; fi
```

Set a local password in `.env` before the first database start. Keep existing
settings when reusing an initialized database volume. PostgreSQL initialization
uses these settings when its volume is first created.

```bash
docker compose up --build -d --wait
```

Compose starts PostgreSQL first and waits for its healthcheck before starting
the API. `--wait` waits for both services to become healthy. The API is published
on local loopback port 8000; PostgreSQL is reached as `db:5432` inside the
Compose network. The database does not publish a host port.

The Dockerfile uses Python 3.12, installs dependencies before copying application
code to reuse the dependency layer, and runs the API as user 10001. To build
without starting services, use `docker compose build api` after configuring `.env`.

## Inspect and call the API

```bash
docker compose ps
curl -i http://localhost:8000/health
curl -i http://localhost:8000/ready
docker compose logs api
```

Expected health response: HTTP 200 and `{"status":"ok"}`.
Interactive API documentation is available at `http://localhost:8000/docs`.

`/health` reports that the API is running. `/ready` also checks a live database
connection and returns HTTP 503 when the database cannot be reached.

## Create and list tasks

```bash
curl -i -X POST http://localhost:8000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Learn Docker Compose"}'

curl -i http://localhost:8000/tasks
```

Creation returns HTTP 201 with the task ID, title, and creation time. Listing
returns HTTP 200 and a JSON array of stored tasks. Titles are trimmed and must
contain 1–200 characters; invalid request bodies return HTTP 422.

## How the pieces fit together

- `api` and `db` are service names on a Compose network. The API uses `db` as its database hostname.
- `.env` supplies database settings without putting the local password in Git.
- `depends_on` with `service_healthy` waits for the database readiness check.
- The `postgres_data` named volume stores database files outside the container.
- For this learning lab, the API creates the tasks table on startup. Schema migration tooling is outside this milestone.

## Stop

```bash
docker compose down
```

`down` removes this Compose project's containers and network while retaining
the named database volume. Adding `--volumes` also deletes the stored data.

## Reproduce the persistence demo

Create a task with the POST request above, then run:

```bash
docker compose down
docker compose up -d --wait
curl -i http://localhost:8000/tasks
```

The previously created task should retain its ID, title, and creation timestamp.
This was confirmed in the manual demo on 2026-10-25.

## Scope of this project

The deliverable is a working API, a database, a Compose setup, and a persistence
demo. Kubernetes and cloud deployment belong to later projects.

This is a local learning application. Authentication, schema migration tooling,
and a CI/CD pipeline are outside v0.1.0. Direct Python dependencies are pinned;
transitive dependencies and container base images are not fully locked.

## Verified behavior

Checked in an isolated Compose project with disposable test data:

- API liveness and database readiness returned HTTP 200.
- Creating a task returned HTTP 201; listing included the stored task.
- A blank title returned HTTP 422.
- Both API and database containers were recreated, keeping the named volume.
- The previously created task remained available after recreation.

The manual demo also confirmed both services healthy, successful task creation
and listing, and preservation of the same task after `down` and `up`.
