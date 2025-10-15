from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Iterable, Sequence

import numpy as np

DEFAULT_EMBEDDING_DIM = 1536
DEFAULT_EPSILON = 1e-5

FACET_FIELDS: tuple[str, ...] = (
    "vector_roles",
    "vector_skills",
    "vector_growth",
    "vector_career",
    "vector_vision",
    "vector_culture",
)


class EmbeddingValidationError(ValueError):
    """Raised when an embedding payload fails runtime validation."""


@dataclass(slots=True)
class EmbeddingValidationResult:
    vector: np.ndarray
    was_normalized: bool

    def as_list(self) -> list[float]:
        return self.vector.astype(np.float32).tolist()


def ensure_f32_unit(
    vec: Sequence[float],
    dim: int = DEFAULT_EMBEDDING_DIM,
    eps: float = DEFAULT_EPSILON,
) -> np.ndarray:
    """
    Validate and normalise a floating point vector.

    Returns the vector cast to float32 and unit-normalised. Raises EmbeddingValidationError
    if the vector cannot be coerced to the expected dimensional, finite representation.
    """
    arr = np.asarray(vec, dtype=np.float32)
    if arr.ndim != 1 or arr.size != dim:
        raise EmbeddingValidationError(f"expected dimension {dim}, received {arr.size}")
    if not np.isfinite(arr).all():
        raise EmbeddingValidationError("embedding contains non-finite values")

    norm = float(np.linalg.norm(arr))
    if norm == 0.0:
        raise EmbeddingValidationError("embedding norm is zero")

    arr = arr / norm
    if not math.isclose(1.0, float(np.linalg.norm(arr)), rel_tol=eps, abs_tol=eps):
        raise EmbeddingValidationError("normalised embedding deviates from unit length")
    return arr


def extract_embedding_vector(value: Any) -> Sequence[float]:
    """
    Pull the raw embedding list from supported payload shapes.
    Supports direct list payloads or dicts containing an `embedding` list.
    """
    if isinstance(value, dict):
        candidate = value.get("embedding")
        if isinstance(candidate, Iterable):
            return list(candidate)
    elif isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return list(value)
    raise EmbeddingValidationError("embedding payload must be list[float] or {'embedding': [...]}")


def validate_embedding_payload(
    value: Any,
    *,
    dim: int = DEFAULT_EMBEDDING_DIM,
    eps: float = DEFAULT_EPSILON,
) -> EmbeddingValidationResult:
    raw_vector = extract_embedding_vector(value)
    raw_array = np.asarray(raw_vector, dtype=np.float32)
    raw_norm = float(np.linalg.norm(raw_array))

    normalised = ensure_f32_unit(raw_vector, dim=dim, eps=eps)
    was_normalised = not math.isclose(raw_norm, 1.0, rel_tol=eps, abs_tol=eps)
    return EmbeddingValidationResult(vector=normalised, was_normalised=was_normalised)


__all__ = [
    "DEFAULT_EMBEDDING_DIM",
    "DEFAULT_EPSILON",
    "FACET_FIELDS",
    "EmbeddingValidationError",
    "EmbeddingValidationResult",
    "ensure_f32_unit",
    "extract_embedding_vector",
    "validate_embedding_payload",
]
