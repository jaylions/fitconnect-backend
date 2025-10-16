from __future__ import annotations

from math import sqrt
from typing import Any, Dict, Iterable, List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import matching_vector_repo
from app.services.matching_vector_service import ALLOWED_ROLES, VECTOR_FIELDS


def _error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})


def _ensure_opposite_roles(source_role: str, target_role: str) -> None:
    if source_role == target_role:
        raise _error(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "ROLE_MISMATCH",
            "Matching vectors must belong to opposite roles",
        )

    roles = {source_role, target_role}
    if not roles.issubset(ALLOWED_ROLES) or roles != {"talent", "company"}:
        raise _error(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "ROLE_MISMATCH",
            "Only talent and company vectors can be matched",
        )


def _ensure_complete(row: Any, label: str) -> None:
    missing = [field for field in VECTOR_FIELDS if getattr(row, field) is None]
    if missing:
        raise _error(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "INCOMPLETE_VECTOR_FIELDS",
            f"{label} vector is missing fields: {', '.join(missing)}",
        )


def _extract_vector(raw: Any, field_name: str, label: str) -> List[float]:
    data = raw
    if isinstance(raw, dict):
        if "vector" in raw:
            data = raw["vector"]
        elif "values" in raw:
            data = raw["values"]
        else:
            raise _error(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "INVALID_VECTOR_DATA",
                f"{label} {field_name} must contain a 'vector' or 'values' list",
            )

    if not isinstance(data, list):
        raise _error(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "INVALID_VECTOR_DATA",
            f"{label} {field_name} must be a list of numbers",
        )

    if not data:
        raise _error(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "INVALID_VECTOR_DATA",
            f"{label} {field_name} cannot be empty",
        )

    try:
        vector = [float(value) for value in data]
    except (TypeError, ValueError):
        raise _error(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "INVALID_VECTOR_DATA",
            f"{label} {field_name} must contain only numeric values",
        ) from None

    return vector


def _cosine_similarity(a: Iterable[float], b: Iterable[float], field_name: str, label: str) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sqrt(sum(x * x for x in a))
    norm_b = sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        raise _error(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "ZERO_VECTOR",
            f"{label} {field_name} contains a zero magnitude vector which cannot be matched",
        )

    return dot / (norm_a * norm_b)


def match(db: Session, source_id: int, target_id: int) -> Dict[str, Any]:
    source = matching_vector_repo.get_by_id(db, source_id)
    if source is None:
        raise _error(status.HTTP_404_NOT_FOUND, "SOURCE_NOT_FOUND", "Source matching vector not found")

    target = matching_vector_repo.get_by_id(db, target_id)
    if target is None:
        raise _error(status.HTTP_404_NOT_FOUND, "TARGET_NOT_FOUND", "Target matching vector not found")

    _ensure_opposite_roles(source.role, target.role)
    _ensure_complete(source, "Source")
    _ensure_complete(target, "Target")

    field_scores: Dict[str, float] = {}
    cosine_scores: List[float] = []

    for field in VECTOR_FIELDS:
        source_vector = _extract_vector(getattr(source, field), field, "Source")
        target_vector = _extract_vector(getattr(target, field), field, "Target")

        if len(source_vector) != len(target_vector):
            raise _error(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "VECTOR_DIMENSION_MISMATCH",
                f"{field} vectors must have the same length",
            )

        cosine = _cosine_similarity(source_vector, target_vector, field, "Either source or target")
        normalized = _normalize_cosine(cosine)

        cosine_scores.append(cosine)

        field_scores[field] = normalized

    aggregate_cosine = sum(cosine_scores) / len(cosine_scores)
    total_score = _normalize_cosine(aggregate_cosine)

    return {
        "source": {"id": source.id, "user_id": source.user_id, "role": source.role},
        "target": {"id": target.id, "user_id": target.user_id, "role": target.role},
        "field_scores": field_scores,
        "total_similarity": total_score,
        "score": total_score,
    }


def _normalize_cosine(value: float) -> float:
    clamped = max(min(value, 1.0), -1.0)
    return ((clamped + 1.0) / 2.0) * 100.0
