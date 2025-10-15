from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.settings import settings
from app.repositories import vector_repo
from app.repositories.vector_repo import FACETS
from app.services import match_service, scoring


router = APIRouter(prefix="/api/match", tags=["match"])


class WeightParams(BaseModel):
    roles: Optional[float] = Field(default=None, alias="weights.roles")
    skills: Optional[float] = Field(default=None, alias="weights.skills")
    growth: Optional[float] = Field(default=None, alias="weights.growth")
    career: Optional[float] = Field(default=None, alias="weights.career")
    vision: Optional[float] = Field(default=None, alias="weights.vision")
    culture: Optional[float] = Field(default=None, alias="weights.culture")

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    def as_weights(self) -> Dict[str, float]:
        weights: Dict[str, float] = {}
        for facet in FACETS:
            value = getattr(self, facet)
            if value is None:
                weights[facet] = 1.0
            else:
                weights[facet] = float(value) if float(value) > 0 else 0.0
        if all(weight == 0.0 for weight in weights.values()):
            weights = {facet: 1.0 for facet in FACETS}
        return weights


def _check_enabled():
    if not settings.MATCHING_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={"code": "MATCHING_DISABLED", "message": "Matching service is disabled"},
        )


def _parse_filters(raw: Optional[str]) -> Dict[str, Any]:
    if raw is None:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "INVALID_FILTERS", "message": "filters must be valid JSON"},
        )
    if not isinstance(parsed, dict):
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "INVALID_FILTERS", "message": "filters must be a JSON object"},
        )
    return parsed


def _round_score(value: float) -> float:
    return round(float(value) + 1e-8, 2)


def _round_result(row: Dict[str, Any], id_key: str) -> Dict[str, Any]:
    payload = {
        id_key: row[id_key],
        "overall": {"score_100": _round_score(row["overall"]["score_100"])},
        "facets": {},
    }
    for facet, data in row.get("facets", {}).items():
        payload["facets"][facet] = {"score_100": _round_score(data["score_100"])}
    return payload


def _round_weight(value: float) -> float:
    return round(float(value) + 1e-8, 2)


def _format_weights(weights: Dict[str, float]) -> Dict[str, float]:
    return {facet: _round_weight(weight) for facet, weight in weights.items()}


def _embedding_not_found(entity: str, entity_id: int) -> HTTPException:
    return HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail={
            "code": "EMBEDDING_NOT_FOUND",
            "message": f"Embedding data not found for {entity} {entity_id}",
        },
    )


def _build_topk_response(
    entity_id: int,
    entity_key: str,
    result_id_key: str,
    rows: List[Dict[str, Any]],
    weights: Dict[str, float],
    start_rank: int = 1,
) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    for idx, row in enumerate(rows, start=start_rank):
        formatted = _round_result(row, result_id_key)
        formatted["rank"] = idx
        results.append(formatted)

    return {
        entity_key: entity_id,
        "weights": _format_weights(weights),
        "results": results,
    }


def _build_all_response(
    entity_id: int,
    entity_key: str,
    result_id_key: str,
    rows: List[Dict[str, Any]],
    weights: Dict[str, float],
    limit: int,
    offset: int,
    total: int,
) -> Dict[str, Any]:
    results: List[Dict[str, Any]] = []
    for idx, row in enumerate(rows, start=offset + 1):
        formatted = _round_result(row, result_id_key)
        formatted["rank"] = idx
        results.append(formatted)

    return {
        entity_key: entity_id,
        "total": total,
        "limit": limit,
        "offset": offset,
        "weights": _format_weights(weights),
        "results": results,
    }


@router.get("/job/{job_id}")
def match_job_topk(
    job_id: int,
    top_k: int = Query(default=20, ge=1, le=500),
    weights: WeightParams = Depends(),
    filters: Optional[str] = Query(default=None),
    _debug: bool = Query(default=False),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _check_enabled()
    _parse_filters(filters)

    job_vectors = vector_repo.load_job_vectors(db, job_id)
    if job_vectors is None:
        raise _embedding_not_found("job", job_id)

    weight_map = weights.as_weights()
    talent_ids = vector_repo.list_talent_ids(db)
    if not talent_ids:
        data = _build_topk_response(job_id, "job_id", "talent_id", [], weight_map)
        return {"ok": True, "data": data}

    candidates = vector_repo.load_talent_vectors_bulk(db, talent_ids)
    if not candidates:
        data = _build_topk_response(job_id, "job_id", "talent_id", [], weight_map)
        return {"ok": True, "data": data}

    rows = match_service.topk_for_job(job_vectors, candidates, weight_map, top_k)
    data = _build_topk_response(job_id, "job_id", "talent_id", rows, weight_map)
    return {"ok": True, "data": data}


@router.get("/job/{job_id}/all")
def match_job_all(
    job_id: int,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    weights: WeightParams = Depends(),
    filters: Optional[str] = Query(default=None),
    _debug: bool = Query(default=False),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _check_enabled()
    _parse_filters(filters)

    job_vectors = vector_repo.load_job_vectors(db, job_id)
    if job_vectors is None:
        raise _embedding_not_found("job", job_id)

    weight_map = weights.as_weights()
    talent_ids = vector_repo.list_talent_ids(db)
    if not talent_ids:
        data = _build_all_response(job_id, "job_id", "talent_id", [], weight_map, limit, offset, 0)
        return {"ok": True, "data": data}

    candidates = vector_repo.load_talent_vectors_bulk(db, talent_ids)
    if not candidates:
        data = _build_all_response(job_id, "job_id", "talent_id", [], weight_map, limit, offset, 0)
        return {"ok": True, "data": data}

    rows, total = match_service.all_for_job(job_vectors, candidates, weight_map, limit, offset)
    data = _build_all_response(job_id, "job_id", "talent_id", rows, weight_map, limit, offset, total)
    return {"ok": True, "data": data}


@router.get("/talent/{talent_id}")
def match_talent_topk(
    talent_id: int,
    top_k: int = Query(default=20, ge=1, le=500),
    weights: WeightParams = Depends(),
    filters: Optional[str] = Query(default=None),
    _debug: bool = Query(default=False),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _check_enabled()
    _parse_filters(filters)

    talent_vectors = vector_repo.load_talent_vectors(db, talent_id)
    if talent_vectors is None:
        raise _embedding_not_found("talent", talent_id)

    weight_map = weights.as_weights()
    job_ids = vector_repo.list_job_ids(db)
    if not job_ids:
        data = _build_topk_response(talent_id, "talent_id", "job_id", [], weight_map)
        return {"ok": True, "data": data}

    candidates = vector_repo.load_job_vectors_bulk(db, job_ids)
    if not candidates:
        data = _build_topk_response(talent_id, "talent_id", "job_id", [], weight_map)
        return {"ok": True, "data": data}

    rows = match_service.topk_for_talent(talent_vectors, candidates, weight_map, top_k)
    data = _build_topk_response(talent_id, "talent_id", "job_id", rows, weight_map)
    return {"ok": True, "data": data}


@router.get("/talent/{talent_id}/all")
def match_talent_all(
    talent_id: int,
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    weights: WeightParams = Depends(),
    filters: Optional[str] = Query(default=None),
    _debug: bool = Query(default=False),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _check_enabled()
    _parse_filters(filters)

    talent_vectors = vector_repo.load_talent_vectors(db, talent_id)
    if talent_vectors is None:
        raise _embedding_not_found("talent", talent_id)

    weight_map = weights.as_weights()
    job_ids = vector_repo.list_job_ids(db)
    if not job_ids:
        data = _build_all_response(talent_id, "talent_id", "job_id", [], weight_map, limit, offset, 0)
        return {"ok": True, "data": data}

    candidates = vector_repo.load_job_vectors_bulk(db, job_ids)
    if not candidates:
        data = _build_all_response(talent_id, "talent_id", "job_id", [], weight_map, limit, offset, 0)
        return {"ok": True, "data": data}

    rows, total = match_service.all_for_talent(talent_vectors, candidates, weight_map, limit, offset)
    data = _build_all_response(talent_id, "talent_id", "job_id", rows, weight_map, limit, offset, total)
    return {"ok": True, "data": data}


@router.get("/score")
def score_pair(
    talent_id: int = Query(...),
    job_id: int = Query(...),
    weights: WeightParams = Depends(),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _check_enabled()

    talent_vectors = vector_repo.load_talent_vectors(db, talent_id)
    if talent_vectors is None:
        raise _embedding_not_found("talent", talent_id)

    job_vectors = vector_repo.load_job_vectors(db, job_id)
    if job_vectors is None:
        raise _embedding_not_found("job", job_id)

    weight_map = weights.as_weights()
    result = scoring.score_pair_100(talent_vectors, job_vectors, weight_map)
    overall = _round_score(result["overall"]["score_100"])
    facet_scores = {facet: {"score_100": _round_score(data["score_100"])} for facet, data in result["facets"].items()}

    data = {
        "talent_id": talent_id,
        "job_id": job_id,
        "weights": _format_weights(weight_map),
        "overall": {"score_100": overall},
        "facets": facet_scores,
    }
    return {"ok": True, "data": data}
