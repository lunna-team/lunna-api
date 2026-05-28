# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Lunna API** — a prenatal monitoring SaaS white-label backend for private obstetrics clinics. Patients (gestantes), doctors, secretaries, and admins each have distinct roles and permissions.

## Commands

```bash
# Run dev server
uvicorn main:app --reload

# Run with Docker (Redis + API)
docker-compose up -d --build

# Run all tests (requires local PostgreSQL at localhost:5432/appclinica_test)
pytest

# Run a single test
pytest tests/test_auth.py::test_login_success -v

# Background worker (ARQ)
arq app.worker.WorkerSettings

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "describe the change"
alembic downgrade -1
```

## Architecture

### Request Lifecycle
`main.py` → `app/api/v1/router.py` → endpoint module → `app/api/dependencies.py` (auth) → `app/crud/` → async SQLAlchemy session → PostgreSQL

### Core Layers

- **`app/core/config.py`** — Pydantic `Settings` loaded from `.env`. `DATABASE_URL` takes precedence over individual `POSTGRES_*` vars; same pattern for `REDIS_URL` vs `REDIS_HOST/PORT`. The `sqlalchemy_database_uri` property auto-converts `postgresql://` to `postgresql+asyncpg://`.
- **`app/core/database.py`** — Async SQLAlchemy engine with `ssl: "require"` (Supabase). `AsyncSessionLocal` is the session factory.
- **`app/core/security.py`** — JWT (HS256) `create_access_token` / `create_refresh_token`, bcrypt password hashing.
- **`app/api/dependencies.py`** — Three key FastAPI dependencies: `get_db` (yields session), `get_current_user` (decodes JWT, loads User), `require_role(["doctor", "admin"])` (RBAC guard).

### Models

All models inherit from `app/models/base.py::BaseModel` which provides UUID PK, `created_at`, `updated_at`, and `deleted_at` (soft-delete pattern — not enforced in queries automatically).

User has three polymorphic sub-profiles linked by `user_id`:
- `Patient` — gestational data (LMP, EDD, risk level, vitals history)
- `Doctor` — CRM, specialty
- `Secretary` — position

### Roles & RBAC

Defined in `app/models/enums.py::UserRole`: `patient`, `doctor`, `secretary`, `admin`, `superadmin`. Enforce with `Depends(require_role(["doctor"]))` in route definitions.

`superadmin` é o único role sem `clinic_id` — a coluna é nullable exatamente por isso (migration `f1a2b3c4d5e6`). `UserResponse.clinic_id` é `Optional[UUID]`.

### Schemas vs Models

`app/schemas/` holds Pydantic v2 DTOs (request/response). Always use `model_dump(exclude_unset=True)` when applying partial updates so only provided fields are written.

### Background Jobs

`app/worker.py` uses **ARQ** (async Redis queue). Add new tasks by defining `async def my_task(ctx, ...)` and registering in `WorkerSettings.functions`. Enqueue from endpoints via `await redis.enqueue_job("my_task", ...)`.

### Caching

**fastapi-cache2** with Redis backend initialized in `main.py` lifespan. Decorate read endpoints with `@cache(expire=60)`.

## Environment Setup

Copy `.env.example` to `.env`. Minimum required for local dev sem Docker:

```
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/lunna
REDIS_URL=redis://localhost:6379
SECRET_KEY=<any-long-random-string>
```

### Supabase (produção / staging)

Usar o **session pooler** (`aws-1-sa-east-1.pooler.supabase.com:5432`), não a conexão direta (`db.<ref>.supabase.co:5432`).

- A conexão direta resolve para IPv6 em algumas redes, causando timeout silencioso.
- O transaction pooler (porta 6543) é incompatível com asyncpg (prepared statements). Usar porta 5432 do session pooler.
- Senha com `@` deve ser URL-encoded: `@` → `%40` na DATABASE_URL.

```
DATABASE_URL=postgresql+asyncpg://postgres.<ref>:%40SuaSenha@aws-1-sa-east-1.pooler.supabase.com:5432/postgres
```

### Python version

asyncpg não tem wheel para Python 3.14+. Usar **Python 3.12**:

```bash
brew install python@3.12
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Deployment

The API deploys to **Vercel** via `vercel.json` (routes everything through `main.py`). Docker Compose is for local dev — the compose file does not include a PostgreSQL service (database is expected on Supabase).

## Key Gotchas

- `alembic/env.py` uses `connect_args={"ssl": "require"}` — running migrations locally against a non-SSL DB will fail. Override by editing `env.py` temporarily or use `DATABASE_URL` pointing to a local non-SSL instance.
- **`%` na DATABASE_URL com Alembic:** `alembic/env.py` passa a URL via `configparser`, que interpreta `%` como sintaxe de interpolação. A linha que seta a URL deve fazer `.replace("%", "%%")`:
  ```python
  config.set_main_option("sqlalchemy.url", settings.sqlalchemy_database_uri.replace("%", "%%"))
  ```
- **Múltiplos heads no Alembic:** se houver dois branches de migração, `alembic upgrade head` falha. Usar `alembic upgrade heads` (plural) ou criar uma migration de merge com `down_revision` como tupla.
- `tests/conftest.py` imports from `app.core.dependencies` but the actual module is `app.api.dependencies` — tests may need this fixed before running.
- Access token TTL defaults to 1440 minutes (24h); refresh token is hardcoded to 7 days in `security.py`.
- O `seed.py` inclui criação do usuário `superadmin@lunna.app` (role `superadmin`, sem `clinic_id`). Esse usuário deve existir antes de usar o dashboard `/superadmin`.
