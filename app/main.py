from contextlib import asynccontextmanager
from datetime import datetime

import psycopg
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from app.db import connection, init_schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_schema()
    yield


app = FastAPI(title="Docker Delivery Lab", version="0.1.0", lifespan=lifespan)


class TaskCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=200)


class Task(BaseModel):
    id: int
    title: str
    created_at: datetime


@app.exception_handler(psycopg.OperationalError)
async def database_unavailable(request: Request, exc: psycopg.OperationalError):
    return JSONResponse(status_code=503, content={"detail": "Database unavailable"})


@app.get("/")
def root() -> dict[str, str]:
    return {"project": "Docker Delivery Lab", "message": "API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict[str, str]:
    with connection() as conn:
        conn.execute("SELECT 1")
    return {"status": "ready"}


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> Task:
    with connection() as conn:
        row = conn.execute(
            "INSERT INTO tasks (title) VALUES (%s) RETURNING id, title, created_at",
            (task.title,),
        ).fetchone()
    return Task(**row)


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    with connection() as conn:
        rows = conn.execute(
            "SELECT id, title, created_at FROM tasks ORDER BY id"
        ).fetchall()
    return [Task(**row) for row in rows]
