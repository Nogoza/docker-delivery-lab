# Docker Delivery Lab

A project for learning how to package a small Python API in Docker and run it
with PostgreSQL through Docker Compose.

## Finish line

Run the API and PostgreSQL with `docker compose up --build`, create and list
tasks through the API, and show that data survives container recreation.

## Milestones

1. **API and image:** build the image and get an HTTP 200 response from `/health`.
2. **Compose and database:** run API and PostgreSQL together; add task creation and listing.
3. **Persistence and handoff:** recreate containers without losing task data, document the demo, and publish the project on GitHub.

Current stage: milestone 1. PostgreSQL and Compose configuration will be added
in milestone 2.

## Requirements

- Docker Engine
- Docker Compose v2 for milestone 2
- `curl` for terminal requests

## Files to read first

- `app/main.py`: the API routes.
- `requirements.txt`: direct Python dependencies, pinned to checked versions.
- `Dockerfile`: the instructions used to build the image.
- `.dockerignore`: files excluded from the Docker build context.

## Build

Run from this project directory:

```bash
docker build -t docker-delivery-lab:dev .
```

The image uses Python 3.12, installs dependencies before copying application
code to reuse the dependency layer, and runs the API as user 10001.

## Run

```bash
docker run --rm -d --name delivery-api -p 127.0.0.1:8000:8000 docker-delivery-lab:dev
```

`--rm` removes this container after it stops. `-d` runs it in the background.
`--name` gives it a readable name. The port mapping publishes container port
8000 on the local machine's loopback port 8000.

## Inspect and call the API

```bash
docker ps --filter name=delivery-api
curl -i http://localhost:8000/health
curl -i http://localhost:8000/
docker logs delivery-api
```

Expected health response: HTTP 200 and `{"status":"ok"}`.
Interactive API documentation is available at `http://localhost:8000/docs`.

## Stop

```bash
docker stop delivery-api
```

The image remains available for the next run. A later exercise will use a
named volume to preserve PostgreSQL data when containers are recreated.

## Scope of this project

The deliverable is a working API, a database, a Compose setup, and a persistence
demo. Kubernetes and cloud deployment belong to later projects.
