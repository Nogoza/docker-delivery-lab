import os

import psycopg
from psycopg.rows import dict_row


def connection():
    return psycopg.connect(
        host=os.environ.get("POSTGRES_HOST", "db"),
        port=int(os.environ.get("POSTGRES_PORT", "5432")),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=3,
        row_factory=dict_row,
    )


def init_schema() -> None:
    with connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                title VARCHAR(200) NOT NULL CHECK (length(btrim(title)) > 0),
                created_at TIMESTAMPTZ NOT NULL DEFAULT now()
            )
            """
        )
