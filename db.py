import os
from uuid import uuid4
from contextlib import contextmanager

import psycopg


DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://homelab:change-me@localhost:5432/homelab",
)


@contextmanager
def connection():
    with psycopg.connect(DATABASE_URL) as conn:
        yield conn


def init_db():
    with connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS "user" (
                id SERIAL PRIMARY KEY,
                name VARCHAR(120) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title VARCHAR(200) NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                CONSTRAINT posts_user_fk
                    FOREIGN KEY (user_id)
                    REFERENCES "user"(id)
                    ON DELETE CASCADE
            );
            """
        )


def save_user():
    email = f"homelab-{uuid4()}@example.com"
    with connection() as conn:
        row = conn.execute(
            """
            INSERT INTO "user" (name, email)
            VALUES (%s, %s)
            RETURNING id, name, email
            """,
            ("Homelab User", email),
        ).fetchone()
    return {"id": row[0], "name": row[1], "email": row[2]}


def save_posts():
    with connection() as conn:
        query = (
            'SELECT id FROM "user" '
            "ORDER BY id DESC LIMIT 1"
        )
        user = conn.execute(query).fetchone()
        if user is None:
            raise RuntimeError("Execute save_user before saving posts")

        posts = []
        for title, content in (
            ("Primeiro post", "Post criado pelo serviço do homelab."),
            ("Segundo post", "Segundo post criado pelo serviço do homelab."),
        ):
            row = conn.execute(
                """
                INSERT INTO posts (user_id, title, content)
                VALUES (%s, %s, %s)
                RETURNING id, user_id, title, content
                """,
                (user[0], title, content),
            ).fetchone()
            posts.append(
                {
                    "id": row[0],
                    "user_id": row[1],
                    "title": row[2],
                    "content": row[3],
                }
            )
    return posts
