from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Literal, Optional

from sqlalchemy.orm import Session

from app.core.settings import settings
from app.models.embeddings import JobEmbedding, TalentEmbedding
from app.services.embedding_validation import (
    DEFAULT_EMBEDDING_DIM,
    DEFAULT_EPSILON,
    FACET_FIELDS,
    EmbeddingValidationError,
    validate_embedding_payload,
)

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "text-embedding-3-small"


@dataclass(slots=True)
class EmbeddingSyncResult:
    status: Literal["disabled", "skipped", "applied", "partial", "error"]
    duration_ms: float = 0.0
    changed_facets: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: Dict[str, str] = field(default_factory=dict)
    message: Optional[str] = None

    def to_meta(self) -> Optional[Dict[str, Any]]:
        if self.status in {"disabled", "skipped", "applied"} and not self.warnings and not self.errors:
            return None
        payload: Dict[str, Any] = {
            "status": self.status,
            "duration_ms": round(self.duration_ms, 2),
        }
        if self.changed_facets:
            payload["changed_facets"] = self.changed_facets
        if self.warnings:
            payload["warnings"] = self.warnings
        if self.errors:
            payload["errors"] = self.errors
        if self.message:
            payload["message"] = self.message
        return {"embedding_sync": payload}


def embed_text(text: str, *, model: str = DEFAULT_MODEL, dim: int = DEFAULT_EMBEDDING_DIM) -> Optional[List[float]]:
    logger.warning(
        "embedding pipeline not configured; skipping text embedding",
        extra={"model": model, "dim": dim},
    )
    return None


def _extract_text_payload(value: Any) -> Optional[str]:
    if isinstance(value, str):
        text = value.strip()
        return text or None
    if isinstance(value, dict):
        for key in ("text", "raw_text", "value"):
            candidate = value.get(key)
            if isinstance(candidate, str):
                text = candidate.strip()
                if text:
                    return text
    return None


def _load_or_create_talent_row(db: Session, user_id: int, *, model: str, dim: int) -> TalentEmbedding:
    row = db.get(TalentEmbedding, user_id)
    if row is None:
        row = TalentEmbedding(talent_id=user_id, model=model, dim=dim)
        db.add(row)
    else:
        row.model = model
        row.dim = dim
    return row


def _load_or_create_job_row(
    db: Session,
    job_id: int,
    *,
    model: str,
    dim: int,
) -> JobEmbedding:
    row = db.get(JobEmbedding, job_id)
    if row is None:
        row = JobEmbedding(job_id=job_id, model=model, dim=dim)
        db.add(row)
    else:
        row.model = model
        row.dim = dim
    return row


def _update_facets(row: Any, updates: Dict[str, Optional[Dict[str, List[float]]]]) -> List[str]:
    changed: List[str] = []
    for facet, payload in updates.items():
        current = getattr(row, facet, None)
        if current == payload:
            continue
        setattr(row, facet, payload)
        changed.append(facet)
    return changed


def upsert_embeddings_for_user(
    db: Session,
    user_id: int,
    role: Literal["talent", "company"],
    facets: Dict[str, Any],
    *,
    job_id: Optional[int] = None,
    model: str = DEFAULT_MODEL,
    dim: int = DEFAULT_EMBEDDING_DIM,
) -> EmbeddingSyncResult:
    if not settings.MATCHING_SYNC_ENABLED:
        return EmbeddingSyncResult(status="disabled", message="sync disabled by flag")

    start = time.perf_counter()
    pending_updates: Dict[str, Optional[Dict[str, List[float]]]] = {}
    warnings: List[str] = []
    errors: Dict[str, str] = {}

    for facet, value in facets.items():
        if facet not in FACET_FIELDS:
            continue
        if value is None:
            pending_updates[facet] = None
            continue

        try:
            validation_result = validate_embedding_payload(value, dim=dim, eps=DEFAULT_EPSILON)
        except EmbeddingValidationError:
            text_payload = _extract_text_payload(value)
            if text_payload is None:
                errors[facet] = "unsupported_payload"
                continue
            vector = embed_text(text_payload, model=model, dim=dim)
            if not isinstance(vector, Iterable) or isinstance(vector, (str, bytes)):
                errors[facet] = "embedding_pipeline_unavailable"
                continue
            try:
                validation_result = validate_embedding_payload(vector, dim=dim, eps=DEFAULT_EPSILON)
            except EmbeddingValidationError as exc:
                errors[facet] = str(exc)
                continue

        if validation_result.was_normalized:
            warnings.append(f"{facet}:normalised")
            logger.warning(
                "normalized non-unit embedding",
                extra={"user_id": user_id, "role": role, "facet": facet},
            )
        payload = {"embedding": validation_result.as_list()}
        pending_updates[facet] = payload

    if not pending_updates and not errors:
        duration_ms = (time.perf_counter() - start) * 1000
        return EmbeddingSyncResult(
            status="skipped",
            duration_ms=duration_ms,
            message="no facets provided",
        )

    if role == "talent":
        row = _load_or_create_talent_row(db, user_id, model=model, dim=dim)
    else:
        if job_id is None:
            duration_ms = (time.perf_counter() - start) * 1000
            message = "job_id required for company embedding sync"
            logger.warning(
                "skipping company embedding sync due to missing job_id",
                extra={"user_id": user_id, "role": role},
            )
            return EmbeddingSyncResult(
                status="error",
                duration_ms=duration_ms,
                errors=errors or {"job": "job_id_missing"},
                message=message,
            )
        row = _load_or_create_job_row(db, job_id, model=model, dim=dim)

    changed_facets = _update_facets(row, pending_updates)
    if changed_facets:
        db.flush()

    duration_ms = (time.perf_counter() - start) * 1000

    if not changed_facets and errors:
        logger.error(
            "embedding sync failed",
            extra={"user_id": user_id, "role": role, "errors": errors},
        )
        return EmbeddingSyncResult(
            status="error",
            duration_ms=duration_ms,
            errors=errors,
            warnings=warnings,
            message="failed to apply embedding updates",
        )

    status: Literal["applied", "partial"]
    if errors or warnings:
        status = "partial"
    else:
        status = "applied"

    log_fn = logger.info if status == "applied" else logger.warning
    log_fn(
        "embedding sync completed",
        extra={
            "user_id": user_id,
            "role": role,
            "changed_facets": changed_facets,
            "warnings": warnings,
            "errors": errors,
            "duration_ms": round(duration_ms, 2),
        },
    )

    return EmbeddingSyncResult(
        status=status,
        duration_ms=duration_ms,
        changed_facets=changed_facets,
        warnings=warnings,
        errors=errors,
        message=None if status == "applied" else "completed with warnings",
    )


def delete_embeddings_for_user(
    db: Session,
    user_id: int,
    role: Literal["talent", "company"],
    *,
    job_id: Optional[int] = None,
) -> EmbeddingSyncResult:
    if not settings.MATCHING_SYNC_ENABLED:
        return EmbeddingSyncResult(status="disabled", message="sync disabled by flag")

    start = time.perf_counter()
    if role == "talent":
        row = db.get(TalentEmbedding, user_id)
    else:
        if job_id is None:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.warning(
                "skipping company embedding delete due to missing job_id",
                extra={"user_id": user_id},
            )
            return EmbeddingSyncResult(
                status="skipped",
                duration_ms=duration_ms,
                message="job_id required for company embedding delete",
            )
        row = db.get(JobEmbedding, job_id)

    if row is None:
        duration_ms = (time.perf_counter() - start) * 1000
        return EmbeddingSyncResult(
            status="skipped",
            duration_ms=duration_ms,
            message="embedding row not found",
        )

    updates = {facet: None for facet in FACET_FIELDS}
    changed_facets = _update_facets(row, updates)
    if not changed_facets:
        duration_ms = (time.perf_counter() - start) * 1000
        return EmbeddingSyncResult(
            status="skipped",
            duration_ms=duration_ms,
            message="no embedding facets to clear",
        )

    db.flush()
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "cleared embeddings for user",
        extra={"user_id": user_id, "role": role, "changed_facets": changed_facets},
    )
    return EmbeddingSyncResult(
        status="applied",
        duration_ms=duration_ms,
        changed_facets=changed_facets,
    )


__all__ = [
    "EmbeddingSyncResult",
    "DEFAULT_MODEL",
    "delete_embeddings_for_user",
    "embed_text",
    "upsert_embeddings_for_user",
]
