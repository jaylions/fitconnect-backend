from __future__ import annotations

import math
from typing import Dict, Mapping

import numpy as np

from app.repositories.vector_repo import FACETS


def cosine(u: np.ndarray, v: np.ndarray) -> float:
    if u.ndim != 1 or v.ndim != 1:
        raise ValueError("cosine expects 1-D arrays")
    if u.size != v.size:
        raise ValueError("vectors must share the same dimension")

    u_norm = np.linalg.norm(u)
    v_norm = np.linalg.norm(v)
    if u_norm == 0.0 or v_norm == 0.0:
        return 0.0
    value = float(np.dot(u, v) / (u_norm * v_norm))
    if math.isnan(value) or math.isinf(value):
        return 0.0
    return float(np.clip(value, -1.0, 1.0))


def to_100(value: float) -> float:
    clamped = max(-1.0, min(1.0, float(value)))
    return (clamped + 1.0) * 50.0


def fuse_scores_100(
    facet_cos: Mapping[str, float],
    weights: Mapping[str, float],
    renorm_missing: bool = True,
) -> float:
    if not facet_cos:
        return 0.0

    total_weight = 0.0
    weighted_sum = 0.0
    for facet, similarity in facet_cos.items():
        weight = float(weights.get(facet, 0.0))
        if weight <= 0:
            continue
        total_weight += weight
        weighted_sum += weight * float(similarity)

    if total_weight == 0.0:
        return 0.0

    if renorm_missing:
        denominator = total_weight
    else:
        denominator = sum(float(weights.get(f, 0.0)) for f in FACETS)
        denominator = denominator or total_weight

    combined = weighted_sum / denominator
    return to_100(combined)


def score_pair_100(
    a: Dict[str, np.ndarray],
    b: Dict[str, np.ndarray],
    weights: Mapping[str, float],
) -> Dict[str, Dict[str, float]]:
    facet_scores: Dict[str, Dict[str, float]] = {}
    facet_cosines: Dict[str, float] = {}

    for facet in FACETS:
        vec_a = a.get(facet)
        vec_b = b.get(facet)
        if vec_a is None or vec_b is None:
            continue

        norm_a = float(np.linalg.norm(vec_a))
        norm_b = float(np.linalg.norm(vec_b))
        if norm_a == 0.0 or norm_b == 0.0:
            facet_scores[facet] = {"score_100": 0.0}
            continue

        score = cosine(vec_a, vec_b)
        facet_cosines[facet] = score
        facet_scores[facet] = {"score_100": to_100(score)}

    overall = fuse_scores_100(facet_cosines, weights, renorm_missing=True)
    return {"overall": {"score_100": overall}, "facets": facet_scores}


__all__ = ["cosine", "to_100", "fuse_scores_100", "score_pair_100"]
