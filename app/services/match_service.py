from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

import numpy as np

from app.repositories.vector_repo import FACETS
from app.services.embedding_validation import DEFAULT_EMBEDDING_DIM
from app.services.scoring import fuse_scores_100, to_100

logger = logging.getLogger(__name__)


def _resolve_dim(items: Sequence[Dict[str, Any]], facet: str) -> int:
    for item in items:
        vec = item.get(facet)
        if isinstance(vec, np.ndarray) and vec.ndim == 1 and vec.size > 0:
            return int(vec.size)
    return DEFAULT_EMBEDDING_DIM


def _has_vector(item: Dict[str, Any], facet: str) -> bool:
    vec = item.get(facet)
    if not isinstance(vec, np.ndarray):
        return False
    if vec.ndim != 1:
        return False
    return float(np.linalg.norm(vec)) > 0.0


def stack_matrix(items: Sequence[Dict[str, Any]], facet: str) -> np.ndarray:
    if not items:
        return np.zeros((0, DEFAULT_EMBEDDING_DIM), dtype=np.float32)

    dim = _resolve_dim(items, facet)
    matrix = np.zeros((len(items), dim), dtype=np.float32)

    for idx, item in enumerate(items):
        vec = item.get(facet)
        if not isinstance(vec, np.ndarray):
            continue
        array = np.asarray(vec, dtype=np.float32).reshape(-1)
        if array.size != dim:
            logger.warning(
                "facet dimension mismatch during stack_matrix",
                extra={"facet": facet, "expected": dim, "received": array.size},
            )
            continue
        matrix[idx] = array
    return matrix


def _compute_sims(
    reference: Dict[str, np.ndarray],
    candidates: Sequence[Dict[str, Any]],
) -> Dict[str, np.ma.MaskedArray]:
    sims: Dict[str, np.ma.MaskedArray] = {}
    if not candidates:
        for facet in FACETS:
            sims[facet] = np.ma.masked_array(np.zeros(0, dtype=np.float32), mask=np.zeros(0, dtype=bool))
        return sims

    for facet in FACETS:
        ref_vec = reference.get(facet)
        matrix = stack_matrix(candidates, facet)
        n = matrix.shape[0]

        if ref_vec is None:
            sims[facet] = np.ma.masked_array(np.zeros(n, dtype=np.float32), mask=np.ones(n, dtype=bool))
            continue

        ref_vec = np.asarray(ref_vec, dtype=np.float32).reshape(-1)
        if matrix.shape[1] != ref_vec.size:
            logger.warning(
                "reference/candidate dimension mismatch",
                extra={"facet": facet, "reference": ref_vec.size, "candidate": matrix.shape[1]},
            )
            sims[facet] = np.ma.masked_array(np.zeros(n, dtype=np.float32), mask=np.ones(n, dtype=bool))
            continue

        ref_norm = float(np.linalg.norm(ref_vec))
        if ref_norm == 0.0:
            sims[facet] = np.ma.masked_array(np.zeros(n, dtype=np.float32), mask=np.ones(n, dtype=bool))
            continue

        ref_unit = ref_vec / ref_norm
        cand_norms = np.linalg.norm(matrix, axis=1)
        mask = cand_norms == 0.0
        scores = np.zeros(n, dtype=np.float32)

        valid_idx = np.nonzero(~mask)[0]
        if valid_idx.size > 0:
            normalized = matrix[valid_idx] / cand_norms[valid_idx][:, None]
            scores[valid_idx] = np.clip(normalized @ ref_unit, -1.0, 1.0)

        sims[facet] = np.ma.masked_array(scores, mask=mask)
    return sims


def compute_sims_for_job(
    job_vecs: Dict[str, np.ndarray],
    candidates: Sequence[Dict[str, Any]],
) -> Dict[str, np.ma.MaskedArray]:
    return _compute_sims(job_vecs, candidates)


def compute_sims_for_talent(
    talent_vecs: Dict[str, np.ndarray],
    candidates: Sequence[Dict[str, Any]],
) -> Dict[str, np.ma.MaskedArray]:
    return _compute_sims(talent_vecs, candidates)


def _vectorized_to_100(values: np.ma.MaskedArray) -> np.ma.MaskedArray:
    filled = np.clip(values.filled(0.0), -1.0, 1.0)
    scores = (filled + 1.0) * 50.0
    return np.ma.masked_array(scores, mask=np.ma.getmaskarray(values))


def fuse_batch_100(
    facet_sims: Mapping[str, np.ma.MaskedArray],
    weights: Mapping[str, float],
) -> Tuple[np.ndarray, Dict[str, np.ma.MaskedArray]]:
    if not facet_sims:
        return np.zeros(0, dtype=np.float32), {}

    any_facet = next(iter(facet_sims.values()))
    n = len(any_facet)
    overall = np.zeros(n, dtype=np.float32)
    facet_scores: Dict[str, np.ma.MaskedArray] = {}

    for facet, sims in facet_sims.items():
        facet_scores[facet] = _vectorized_to_100(sims)

    for idx in range(n):
        facet_cos = {}
        for facet, sims in facet_sims.items():
            if np.ma.is_masked(sims[idx]):
                continue
            facet_cos[facet] = float(sims[idx])
        overall[idx] = fuse_scores_100(facet_cos, weights, renorm_missing=True)

    return overall, facet_scores


def _build_rows(
    ids: Sequence[int],
    overall: np.ndarray,
    facet_scores: Mapping[str, np.ma.MaskedArray],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for idx, entity_id in enumerate(ids):
        facets_payload: Dict[str, Dict[str, float]] = {}
        for facet, values in facet_scores.items():
            if np.ma.is_masked(values[idx]):
                continue
            facets_payload[facet] = {"score_100": float(values[idx])}

        rows.append(
            {
                "id": int(entity_id),
                "overall": {"score_100": float(overall[idx])},
                "facets": facets_payload,
            }
        )
    return rows


def _order_indices(overall: np.ndarray, ids: Sequence[int]) -> np.ndarray:
    if overall.size == 0:
        return np.array([], dtype=int)
    neg_overall = -overall
    ids_array = np.asarray(ids, dtype=np.int64)
    order = np.lexsort((ids_array, neg_overall))
    return order


def _extract_ids(candidates: Sequence[Dict[str, Any]], key: str) -> List[int]:
    ids: List[int] = []
    for item in candidates:
        if key not in item:
            raise KeyError(f"candidate missing expected key '{key}'")
        ids.append(int(item[key]))
    return ids


def topk_for_job(
    job_vecs: Dict[str, np.ndarray],
    candidates: Sequence[Dict[str, Any]],
    weights: Mapping[str, float],
    top_k: int,
) -> List[Dict[str, Any]]:
    if top_k <= 0 or not candidates:
        return []

    sims = compute_sims_for_job(job_vecs, candidates)
    overall, facet_scores = fuse_batch_100(sims, weights)
    ids = _extract_ids(candidates, "talent_id")
    order = _order_indices(overall, ids)

    limited = order[: min(top_k, order.size)]
    rows = _build_rows([ids[idx] for idx in limited], overall[limited], {f: scores[limited] for f, scores in facet_scores.items()})
    for row, _ in zip(rows, limited):
        row["talent_id"] = row.pop("id")
    return rows


def all_for_job(
    job_vecs: Dict[str, np.ndarray],
    candidates: Sequence[Dict[str, Any]],
    weights: Mapping[str, float],
    limit: int,
    offset: int = 0,
) -> Tuple[List[Dict[str, Any]], int]:
    total = len(candidates)
    if total == 0 or limit <= 0:
        return [], total

    sims = compute_sims_for_job(job_vecs, candidates)
    overall, facet_scores = fuse_batch_100(sims, weights)
    ids = _extract_ids(candidates, "talent_id")
    order = _order_indices(overall, ids)

    start = max(offset, 0)
    end = start + limit
    sliced = order[start:end]
    rows = _build_rows([ids[idx] for idx in sliced], overall[sliced], {f: scores[sliced] for f, scores in facet_scores.items()})
    for row, _ in zip(rows, sliced):
        row["talent_id"] = row.pop("id")
    return rows, total


def topk_for_talent(
    talent_vecs: Dict[str, np.ndarray],
    candidates: Sequence[Dict[str, Any]],
    weights: Mapping[str, float],
    top_k: int,
) -> List[Dict[str, Any]]:
    if top_k <= 0 or not candidates:
        return []

    sims = compute_sims_for_talent(talent_vecs, candidates)
    overall, facet_scores = fuse_batch_100(sims, weights)
    ids = _extract_ids(candidates, "job_id")
    order = _order_indices(overall, ids)

    limited = order[: min(top_k, order.size)]
    rows = _build_rows([ids[idx] for idx in limited], overall[limited], {f: scores[limited] for f, scores in facet_scores.items()})
    for row, _ in zip(rows, limited):
        row["job_id"] = row.pop("id")
    return rows


def all_for_talent(
    talent_vecs: Dict[str, np.ndarray],
    candidates: Sequence[Dict[str, Any]],
    weights: Mapping[str, float],
    limit: int,
    offset: int = 0,
) -> Tuple[List[Dict[str, Any]], int]:
    total = len(candidates)
    if total == 0 or limit <= 0:
        return [], total

    sims = compute_sims_for_talent(talent_vecs, candidates)
    overall, facet_scores = fuse_batch_100(sims, weights)
    ids = _extract_ids(candidates, "job_id")
    order = _order_indices(overall, ids)

    start = max(offset, 0)
    end = start + limit
    sliced = order[start:end]
    rows = _build_rows([ids[idx] for idx in sliced], overall[sliced], {f: scores[sliced] for f, scores in facet_scores.items()})
    for row, _ in zip(rows, sliced):
        row["job_id"] = row.pop("id")
    return rows, total


__all__ = [
    "stack_matrix",
    "compute_sims_for_job",
    "compute_sims_for_talent",
    "fuse_batch_100",
    "topk_for_job",
    "all_for_job",
    "topk_for_talent",
    "all_for_talent",
]
