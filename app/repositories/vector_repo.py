from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import sqlalchemy as sa
from sqlalchemy.orm import Session

from app.models.embeddings import JobEmbedding, TalentEmbedding
from app.services.embedding_validation import DEFAULT_EMBEDDING_DIM, extract_embedding_vector

logger = logging.getLogger(__name__)

FACETS: Tuple[str, ...] = ("roles", "skills", "growth", "career", "vision", "culture")
_EMBEDDING_PREFIX = "vector_"


def _zero_vector(dim: int) -> np.ndarray:
    return np.zeros(dim, dtype=np.float32)


def _normalise_payload(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (bytes, bytearray)):
        value = value.decode("utf-8")
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            logger.warning("invalid JSON payload encountered during vector load", extra={"payload": stripped[:64]})
            return None
    return value


def _extract_vector(
    facet: str,
    payload: Any,
    expected_dim: Optional[int],
    source: str,
) -> Optional[np.ndarray]:
    value = _normalise_payload(payload)
    if value is None:
        return None

    try:
        raw_vector = extract_embedding_vector(value)
    except Exception:  # pragma: no cover - defensive guard, extract raises ValueError
        logger.warning("failed to extract embedding payload", extra={"facet": facet, "source": source})
        return None

    array = np.asarray(raw_vector, dtype=np.float32)
    if array.ndim != 1:
        logger.warning("embedding payload is not 1-dimensional", extra={"facet": facet, "source": source})
        return None
    dim = array.size
    if expected_dim is not None and dim != expected_dim:
        logger.warning(
            "embedding dimension mismatch",
            extra={"facet": facet, "source": source, "expected": expected_dim, "received": dim},
        )
        return None

    return array


def _init_result(dim: Optional[int]) -> Dict[str, Optional[np.ndarray]]:
    return {facet: None for facet in FACETS}


def _finalise_vectors(store: Dict[str, Optional[np.ndarray]], dim: Optional[int]) -> Optional[Dict[str, np.ndarray]]:
    first_vector = next((vec for vec in store.values() if vec is not None), None)
    if first_vector is not None and dim is None:
        dim = first_vector.size
    if dim is None:
        dim = DEFAULT_EMBEDDING_DIM

    if first_vector is None:
        return None

    final: Dict[str, np.ndarray] = {}
    for facet, vector in store.items():
        final[facet] = vector if vector is not None else _zero_vector(dim)
    return final


def _load_embedding_rows(
    db: Session,
    model: Any,
    key_field: str,
    ids: Sequence[int],
) -> Dict[int, Any]:
    if not ids:
        return {}
    column = getattr(model, key_field)
    stmt = sa.select(model).where(column.in_(ids))
    rows = db.execute(stmt).scalars().all()
    return {getattr(row, key_field): row for row in rows}


def _parse_embedding_row(row: Any, expected_dim: Optional[int]) -> Tuple[Dict[str, Optional[np.ndarray]], Optional[int]]:
    vectors = _init_result(expected_dim)
    dim = expected_dim

    for facet in FACETS:
        column = f"{_EMBEDDING_PREFIX}{facet}"
        if not hasattr(row, column):
            continue
        payload = getattr(row, column)
        vector = _extract_vector(facet, payload, dim, source="embeddings")
        if vector is not None:
            vectors[facet] = vector
            if dim is None:
                dim = vector.size
    if dim is None:
        dim = getattr(row, "dim", None)
    return vectors, dim


def _assemble_talent_vectors(
    embedding_row: Optional[TalentEmbedding],
) -> Optional[Dict[str, np.ndarray]]:
    if embedding_row is None:
        return None
    vectors, dim = _parse_embedding_row(embedding_row, getattr(embedding_row, "dim", None))
    return _finalise_vectors(vectors, dim)


def load_talent_vectors(db: Session, talent_id: int) -> Optional[Dict[str, np.ndarray]]:
    items = load_talent_vectors_bulk(db, [talent_id])
    return items[0] if items else None


def load_job_vectors(db: Session, job_id: int) -> Optional[Dict[str, np.ndarray]]:
    items = load_job_vectors_bulk(db, [job_id])
    return items[0] if items else None


def load_talent_vectors_bulk(db: Session, talent_ids: Sequence[int]) -> List[Dict[str, Any]]:
    if not talent_ids:
        return []

    embeddings = _load_embedding_rows(db, TalentEmbedding, "talent_id", talent_ids)

    results: List[Dict[str, Any]] = []
    for talent_id in talent_ids:
        embedding_row = embeddings.get(talent_id)
        vectors = _assemble_talent_vectors(embedding_row)
        if vectors is None:
            continue
        item: Dict[str, Any] = {"talent_id": talent_id}
        item.update(vectors)
        results.append(item)
    return results


def _assemble_job_vectors(embedding_row: Optional[JobEmbedding]) -> Optional[Dict[str, np.ndarray]]:
    if embedding_row is None:
        return None
    vectors, dim = _parse_embedding_row(embedding_row, getattr(embedding_row, "dim", None))
    return _finalise_vectors(vectors, dim)


def load_job_vectors_bulk(db: Session, job_ids: Sequence[int]) -> List[Dict[str, Any]]:
    if not job_ids:
        return []

    embeddings = _load_embedding_rows(db, JobEmbedding, "job_id", job_ids)

    results: List[Dict[str, Any]] = []
    for job_id in job_ids:
        embedding_row = embeddings.get(job_id)
        vectors = _assemble_job_vectors(embedding_row)
        if vectors is None:
            continue
        item: Dict[str, Any] = {"job_id": job_id}
        item.update(vectors)
        results.append(item)
    return results


def list_talent_ids(db: Session) -> List[int]:
    ids: set[int] = set()

    stmt_embeddings = sa.select(TalentEmbedding.talent_id).where(
        sa.or_(
            *(getattr(TalentEmbedding, f"{_EMBEDDING_PREFIX}{facet}").isnot(None) for facet in FACETS)
        )
    )
    ids.update(int(row[0]) for row in db.execute(stmt_embeddings))

    return sorted(ids)


def list_job_ids(db: Session) -> List[int]:
    ids: set[int] = set()

    stmt_embeddings = sa.select(JobEmbedding.job_id).where(
        sa.or_(
            *(getattr(JobEmbedding, f"{_EMBEDDING_PREFIX}{facet}").isnot(None) for facet in FACETS)
        )
    )
    ids.update(int(row[0]) for row in db.execute(stmt_embeddings))

    return sorted(ids)


__all__ = [
    "FACETS",
    "load_talent_vectors",
    "load_job_vectors",
    "load_talent_vectors_bulk",
    "load_job_vectors_bulk",
    "list_talent_ids",
    "list_job_ids",
]
