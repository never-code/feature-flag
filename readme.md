# feature-flag

A self-hosted feature flag service built with FastAPI, PostgreSQL, and Redis.

## Stack

- **FastAPI** — REST API
- **PostgreSQL** — flag storage and evaluation audit log
- **Redis** — evaluation result caching (1-hour TTL)
- **Alembic** — database migrations

## Features

- Create and manage feature flags per environment (`dev`, `stage`, `prod`)
- Evaluate flags for a user with priority-based rules: user allowlist → group allowlist → scheduling window → percentage rollout → default
- Every evaluation is cached in Redis and logged to the database

## Getting Started

### Prerequisites

- Python 3.13+
- PostgreSQL (database: `featureflags`)
- Redis on `localhost:6379`

### Setup

```bash
cd backend

python -m venv venv
source venv/bin/activate

pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary redis pydantic-settings

alembic upgrade head

uvicorn app.main:app --reload
```

API: `http://localhost:8000`  
Docs: `http://localhost:8000/docs`

## Configuration

| Variable       | Default                                            |
|----------------|----------------------------------------------------|
| `DATABASE_URL` | `postgresql://rsomani@localhost:5432/featureflags` |

## API

| Method | Path                             | Description          |
|--------|----------------------------------|----------------------|
| POST   | `/flags/`                        | Create a flag        |
| GET    | `/flags/`                        | List all flags       |
| GET    | `/flags/{name}?environment=prod` | Get a flag           |
| PUT    | `/flags/{environment}/{name}`    | Update a flag        |
| DELETE | `/flags/{name}`                  | Delete a flag        |
| POST   | `/evaluate`                      | Evaluate a flag for a user |
