# auto-ai-service

FastAPI + Uvicorn backend for the services web page. SQLAlchemy 2.0 ORM, Alembic migrations, Pydantic v2 validation, and JWT bearer auth.

## Quick start

```bash
uv sync                          # install deps into .venv
cp .env.example .env             # then set JWT_SECRET_KEY (openssl rand -hex 32)
uv run alembic upgrade head      # create tables
uv run uvicorn app.main:app --reload
```

- API docs: http://localhost:8000/docs
- Health: `GET /health`

## Layout

```
app/
  main.py              FastAPI app, CORS, router mount
  core/config.py       Settings (env / .env via pydantic-settings)
  core/security.py     Password hashing (argon2) + JWT encode/decode
  db/base.py           Declarative Base + timestamp mixin
  db/session.py        Engine, SessionLocal, get_db dependency
  models/              SQLAlchemy models (User, Service)
  schemas/             Pydantic request/response models
  api/deps.py          DbSession / CurrentUser dependencies
  api/routes/          auth.py, services.py
alembic/               Migrations (URL comes from app settings)
tests/                 pytest, in-memory SQLite
```

## API (`/api/v1`)

| Method | Path | Auth | |
|---|---|---|---|
| POST | `/auth/register` | – | JSON `{email, password, full_name?}` |
| POST | `/auth/login` | – | Form `username` (email) + `password` → `{access_token}` |
| GET | `/auth/me` | Bearer | Current user |
| GET | `/services` | – | List active services (`?include_inactive=true&skip=&limit=`) |
| GET | `/services/{id}` | – | |
| POST | `/services` | Bearer | Create |
| PATCH | `/services/{id}` | Bearer | Partial update |
| DELETE | `/services/{id}` | Bearer | |

## Migrations

```bash
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
```

New models must be imported in `app/models/__init__.py` for autogenerate to see them.

## Dev

```bash
uv run pytest
uv run ruff check . && uv run ruff format .
```
