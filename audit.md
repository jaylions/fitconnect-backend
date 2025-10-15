# FitConnect Backend Compatibility Audit

## Existing API conventions
- FastAPI app bootstraps in `app/main.py` and mounts routers for `/auth`, `/health`, `/api/me/talent`, `/api/me/matching-vectors`, `/api/me/company`, `/api/companies`, `/api/job_posting_cards`, and `/api/talent_cards`.
- API responses under `/api/*` generally follow the envelope `{"ok": true, "data": ...}` and errors shaped as `{"ok": false, "error": {"code": str, "message": str}}`, returned explicitly with `JSONResponse` to preserve status codes.
- Authentication routes in `app/api/auth.py` are legacy: `/auth/register` returns a bare dict (no `ok` flag) and `/auth/login` uses a Pydantic model without the wrapper. Any new endpoints should keep the envelope to match current `/api/*` expectations until auth is modernised.
- `HTTPException` payloads are usually structured dictionaries (e.g., `{"code": "FORBIDDEN", "message": ...}`), but a few older handlers still raise string details (`register`). When raising new errors, prefer the structured form.
- No global exception handlers are registered; per-route handlers decide envelope formatting, so a new `/api/match/*` router should mirror the explicit JSON responses used in `talent.py`, `company.py`, and `matching_vector.py`.

## Database inventory (MySQL 8)
- Docker Compose spins up `mysql:8.0` with UTF-8 defaults: `--character-set-server=utf8mb4`, `--collation-server=utf8mb4_unicode_ci`. Alembic migration `20250929093000` also enforces `utf8mb4_unicode_ci` on existing tables. No custom SQL modes or row formats are defined (falls back to InnoDB defaults).
- Core tables (derived from Alembic migrations and SQLAlchemy models):
  - `users` (`id` PK bigint, `email` unique idx, `password_hash`, `role` enum `talent|company`, timestamps).
  - `talent_profiles` (`user_id` FK→`users.id`, profile step flags, timestamps, soft-delete column).
  - `companies` (`id` PK, `owner_user_id` unique FK→`users.id` with cascade delete, profile fields, Korean `company_size` enum, submission flags, status).
  - `job_postings` (`company_id` FK→`companies.id`, employment/status enums, schedule info, JSON payloads for salary/competencies, soft-delete + published/closed timestamps; indexes on `status`, `deadline_date`, `(company_id,status)`).
  - `matching_vectors` (`user_id` FK→`users.id`, `role` enum `talent|company`, JSON blobs for vectors, `updated_at` timestamp; indexes on `user_id` and `role`).
  - Talent content tables (`educations`, `experiences` with `duration_years`, `activities`, `certifications`, `documents`) each FK to `users.id`, store `created_at`/`updated_at` as `DATETIME` with `CURRENT_TIMESTAMP` defaults and most include `deleted_at` for soft deletes.
  - Card tables (`job_posting_cards`, `talent_cards`) with JSON columns via `app.db.types.JSONType`; `talent_cards.user_id` remains unique.
- No tables for embeddings or vector stores currently exist (`rg` search confirms absence of `embedding`/`vector` tables beyond `matching_vectors`), so new schema additions will be required (e.g., `talent_embeddings`, `job_embeddings`).
- Foreign key coverage already links new matching data back to `users`, `companies`, and `job_postings`; any embedding tables should mirror this pattern (likely FK to `talent_profiles.user_id` or `job_postings.id`).

## App constraints and runtime context
- Tooling: Python `^3.10`, FastAPI `0.117.1`, SQLAlchemy `>=2.0`, Uvicorn `0.37.0`, Alembic `1.16.5`, Pydantic Settings `2.11.0` (from `pyproject.toml`).
- Database session factory in `app/db/session.py` uses synchronous `SessionLocal` with `pool_pre_ping=True`, `autoflush=False`, `expire_on_commit=False`. Routes typically inject a session via `Depends(get_db)` or use on-demand sessions within service modules.
- Transactions: write paths wrap mutations in `with db.begin():` (e.g., `company.py`, `matching_vector.py`) or create scoped sessions (`talent_write.py`) that call `session.begin()`. There is no retry/backoff layer; errors bubble up via `HTTPException`.
- Settings management through `pydantic_settings.BaseSettings`; no feature flags or metrics hooks are present. New toggles (e.g., `MATCHING_ENABLED`) would need to be added to `Settings` and consumed explicitly.
- Logging is limited to default Uvicorn/Alembic output; no structured logging middleware is in place.

## Risks for naming collisions
- Existing router prefixes occupy: `/auth`, `/health`, `/api/me/*` (`talent`, `matching-vectors`, `company`), `/api/companies`, `/api/job_posting_cards`, `/api/talent_cards`. There is no `/api/match/*` namespace yet, so introducing it is safe as long as route names and tags differ from current `matching_vector` endpoints.
- Service/repository modules already use `matching_vector_service.py` and `matching_vector_repo.py`; avoid reusing those names for embedding logic to prevent confusion and accidental imports.
- New SQLAlchemy models should use unique table names (e.g., `talent_embeddings`, `job_embeddings`). Reusing `matching_vectors` or overloading existing enums would break current Alembic history.

## Proposed new module paths
- `app/models/embedding.py` (or split into `talent_embedding.py` / `job_embedding.py`) defining new tables with FK back to users/job postings and JSON/Vector payloads.
- `app/repositories/embedding_repo.py` to encapsulate CRUD/lookups similar to existing repository pattern.
- `app/services/match_service.py` coordinating retrieval, similarity calculations, and graceful fallbacks.
- `app/api/routes/match.py` exposing `/api/match/*` endpoints, returning the standard envelope and structured errors (including `{"code": "EMBEDDING_NOT_FOUND", "message": ...}` for missing vectors).
- Corresponding Pydantic schemas under `app/schemas/match.py` (request/response contracts) to keep API responses typed.

## Error handling & fallback expectations
- When embeddings are unavailable, return `404` with payload `{"ok": False, "error": {"code": "EMBEDDING_NOT_FOUND", "message": "<context>"}}`, mirroring patterns already used in `talent_card.py` and `matching_vector.py`.
- For non-fatal degradations (e.g., fallback to heuristic matches), consider a `200` response with `{"ok": True, "data": {...}, "meta": {"degraded": true}}` if clients need to distinguish—no precedent exists today, so document any deviation in the new schema module.

_Prepared by: Senior backend engineer_
