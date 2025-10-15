from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, Literal, Optional, Tuple, cast

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.embeddings import JobEmbedding, TalentEmbedding
from app.services import embedding_sync_service
from app.services.embedding_sync_service import EmbeddingSyncResult

ALLOWED_ROLES: set[str] = {"talent", "company"}
VECTOR_FIELDS = (
    "vector_roles",
    "vector_skills",
    "vector_growth",
    "vector_career",
    "vector_vision",
    "vector_culture",
)

logger = logging.getLogger(__name__)


def _error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})


def _filter_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    return {field: data[field] for field in VECTOR_FIELDS if field in data}


def _result_meta(result: Optional[EmbeddingSyncResult]) -> Optional[Dict[str, Any]]:
    if result is None:
        return None
    return result.to_meta()


def _fetch_talent_embedding(db: Session, talent_id: int) -> Optional[TalentEmbedding]:
    return db.get(TalentEmbedding, talent_id)


def _fetch_job_embedding(db: Session, job_id: int) -> Optional[JobEmbedding]:
    return db.get(JobEmbedding, job_id)


def _has_any_vector(row: Optional[Any]) -> bool:
    if row is None:
        return False
    for field in VECTOR_FIELDS:
        if getattr(row, field, None):
            return True
    return False


def _sync_upsert(
    db: Session,
    user_id: int,
    role: str,
    payload: Dict[str, Any],
    job_id: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    if not payload:
        return None
    try:
        literal_role = cast(Literal["talent", "company"], role)
        sync_result = embedding_sync_service.upsert_embeddings_for_user(
            db,
            user_id=user_id,
            role=literal_role,
            facets=payload,
            job_id=job_id,
        )
        return _result_meta(sync_result)
    except Exception:  # pragma: no cover - defensive guard
        logger.exception(
            "embedding sync failed during upsert",
            extra={"user_id": user_id, "role": role, "job_id": job_id},
        )
        return {"embedding_sync": {"status": "error", "message": "failed to sync embeddings"}}


def _sync_delete(
    db: Session,
    user_id: int,
    role: str,
    job_id: Optional[int] = None,
) -> Optional[Dict[str, Any]]:
    try:
        literal_role = cast(Literal["talent", "company"], role)
        sync_result = embedding_sync_service.delete_embeddings_for_user(
            db,
            user_id=user_id,
            role=literal_role,
            job_id=job_id,
        )
        return _result_meta(sync_result)
    except Exception:  # pragma: no cover - defensive guard
        logger.exception(
            "embedding sync failed during delete",
            extra={"user_id": user_id, "role": role, "job_id": job_id},
        )
        return {"embedding_sync": {"status": "error", "message": "failed to clear embeddings"}}


def _build_response(
    role: str,
    user_id: int,
    entity_id: int,
    embedding_row: Any,
) -> Dict[str, Any]:
    updated_at = getattr(embedding_row, "updated_at", None)
    if updated_at is None:
        updated_at = datetime.utcnow()

    data = {
        "id": entity_id,
        "user_id": user_id,
        "role": role,
        "updated_at": updated_at,
    }
    if role == "company":
        data["job_id"] = entity_id
    for field in VECTOR_FIELDS:
        data[field] = getattr(embedding_row, field, None)
    return data


def _ensure_role_valid(role: str) -> None:
    if role not in ALLOWED_ROLES:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "INVALID_ROLE", "role must be 'talent' or 'company'")


def create(
    db: Session,
    user_id: int,
    role: str,
    payload: Dict[str, Any],
) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
    _ensure_role_valid(role)
    job_id = payload.pop("job_id", None)
    filtered = _filter_payload(payload)
    if not filtered:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "NO_VECTOR_FIELDS", "Provide at least one vector field")

    if role == "talent":
        existing = _fetch_talent_embedding(db, user_id)
        if _has_any_vector(existing):
            raise _error(
                status.HTTP_409_CONFLICT,
                "MATCHING_VECTOR_EXISTS",
                "Matching vector already exists for this role",
            )
        sync_meta = _sync_upsert(db, user_id=user_id, role=role, payload=filtered)
        row = _fetch_talent_embedding(db, user_id)
        if row is None:
            raise _error(status.HTTP_500_INTERNAL_SERVER_ERROR, "EMBEDDING_WRITE_FAILED", "Failed to persist embedding")
        return _build_response(role, user_id, user_id, row), sync_meta

    if job_id is None:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "JOB_ID_REQUIRED", "job_id is required for company role")

    existing_job = _fetch_job_embedding(db, job_id)
    if _has_any_vector(existing_job):
        raise _error(
            status.HTTP_409_CONFLICT,
            "MATCHING_VECTOR_EXISTS",
            "Matching vector already exists for this job",
        )
    sync_meta = _sync_upsert(db, user_id=user_id, role=role, payload=filtered, job_id=job_id)
    row = _fetch_job_embedding(db, job_id)
    if row is None:
        raise _error(status.HTTP_500_INTERNAL_SERVER_ERROR, "EMBEDDING_WRITE_FAILED", "Failed to persist embedding")
    return _build_response(role, user_id, job_id, row), sync_meta


def update(
    db: Session,
    user_id: int,
    role: str,
    matching_vector_id: int,
    payload: Dict[str, Any],
) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
    _ensure_role_valid(role)
    filtered = _filter_payload(payload)
    if not filtered:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "NO_FIELDS_TO_UPDATE", "Provide at least one field to update")

    if role == "talent":
        if matching_vector_id != user_id:
            raise _error(status.HTTP_403_FORBIDDEN, "FORBIDDEN", "Can only modify your own matching vector")
        existing = _fetch_talent_embedding(db, user_id)
        if not _has_any_vector(existing):
            raise _error(status.HTTP_404_NOT_FOUND, "MATCHING_VECTOR_NOT_FOUND", "Matching vector not found")
        sync_meta = _sync_upsert(db, user_id=user_id, role=role, payload=filtered)
        row = _fetch_talent_embedding(db, user_id)
        if row is None:
            raise _error(status.HTTP_500_INTERNAL_SERVER_ERROR, "EMBEDDING_WRITE_FAILED", "Failed to persist embedding")
        return _build_response(role, user_id, user_id, row), sync_meta

    job_id = matching_vector_id
    existing = _fetch_job_embedding(db, job_id)
    if not _has_any_vector(existing):
        raise _error(status.HTTP_404_NOT_FOUND, "MATCHING_VECTOR_NOT_FOUND", "Matching vector not found")
    sync_meta = _sync_upsert(db, user_id=user_id, role=role, payload=filtered, job_id=job_id)
    row = _fetch_job_embedding(db, job_id)
    if row is None:
        raise _error(status.HTTP_500_INTERNAL_SERVER_ERROR, "EMBEDDING_WRITE_FAILED", "Failed to persist embedding")
    return _build_response(role, user_id, job_id, row), sync_meta


def delete(
    db: Session,
    user_id: int,
    role: str,
    matching_vector_id: int,
) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
    _ensure_role_valid(role)

    if role == "talent":
        if matching_vector_id != user_id:
            raise _error(status.HTTP_403_FORBIDDEN, "FORBIDDEN", "Can only delete your own matching vector")
        existing = _fetch_talent_embedding(db, user_id)
        if not _has_any_vector(existing):
            raise _error(status.HTTP_404_NOT_FOUND, "MATCHING_VECTOR_NOT_FOUND", "Matching vector not found")
        sync_meta = _sync_delete(db, user_id=user_id, role=role)
        return {"id": user_id, "role": role}, sync_meta

    job_id = matching_vector_id
    existing = _fetch_job_embedding(db, job_id)
    if not _has_any_vector(existing):
        raise _error(status.HTTP_404_NOT_FOUND, "MATCHING_VECTOR_NOT_FOUND", "Matching vector not found")
    sync_meta = _sync_delete(db, user_id=user_id, role=role, job_id=job_id)
    return {"id": job_id, "role": role}, sync_meta
