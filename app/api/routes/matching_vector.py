from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.schemas.matching_vector import (
    MatchingVectorCreateIn,
    MatchingVectorDetailOut,
    MatchingVectorOut,
    MatchingVectorUpdateIn,
)
from app.services import matching_vector_service


router = APIRouter(prefix="/api/me/matching-vectors", tags=["matching_vectors"])
public_router = APIRouter(prefix="/api/public/matching-vectors", tags=["matching_vectors_public"])


def _serialize(row) -> dict:
    return MatchingVectorOut.model_validate(row, from_attributes=True).model_dump(mode="json")


def _error_response(exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"ok": False, "error": exc.detail})


@router.get("")
def get_my_matching_vectors(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    현재 로그인한 사용자의 모든 매칭 벡터 조회
    
    - **Talent**: 최대 1개 (user당 1개)
    - **Company**: 여러 개 가능 (job_posting당 1개)
    
    Returns:
    - 벡터 목록 (최신순 정렬)
    - 빈 배열 (벡터가 없을 경우)
    """
    vectors = matching_vector_service.get_all_by_user(db, user_id=int(user["id"]))
    
    serialized_vectors = [_serialize(v) for v in vectors]
    
    return {"ok": True, "data": serialized_vectors}


@router.post("")
def create_matching_vector(
    payload: MatchingVectorCreateIn,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.role != user["role"]:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"ok": False, "error": {"code": "FORBIDDEN_ROLE", "message": "Cannot create matching vector for another role"}},
        )

    payload_dict = payload.model_dump(exclude={"role"}, exclude_unset=True)
    try:
        row = matching_vector_service.create(
            db,
            user_id=int(user["id"]),
            role=payload.role,
            payload=payload_dict,
        )
    except HTTPException as exc:
        if exc.status_code in (
            status.HTTP_409_CONFLICT,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_403_FORBIDDEN,
        ):
            return _error_response(exc)
        raise

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"ok": True, "data": _serialize(row)},
    )


@router.patch("/{matching_vector_id}")
def update_matching_vector(
    matching_vector_id: int,
    payload: MatchingVectorUpdateIn,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    payload_dict = payload.model_dump(exclude_unset=True)
    try:
        row = matching_vector_service.update(
            db,
            user_id=int(user["id"]),
            matching_vector_id=matching_vector_id,
            payload=payload_dict,
        )
    except HTTPException as exc:
        if exc.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_403_FORBIDDEN,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ):
            return _error_response(exc)
        raise

    return {"ok": True, "data": _serialize(row)}


@router.delete("/{matching_vector_id}")
def delete_matching_vector(
    matching_vector_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        row = matching_vector_service.delete(
            db,
            user_id=int(user["id"]),
            matching_vector_id=matching_vector_id,
        )
    except HTTPException as exc:
        if exc.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_403_FORBIDDEN,
        ):
            return _error_response(exc)
        raise

    return {"ok": True, "data": {"id": row.id, "role": row.role}}


# ============================================================
# Public API (인증 불필요)
# ============================================================

@public_router.get("/{vector_id}")
def get_matching_vector_by_id(
    vector_id: int,
    db: Session = Depends(get_db),
):
    """
    Vector ID로 매칭 벡터 상세 정보 조회 (인증 불필요)
    
    - **vector_id**: 조회할 벡터 ID
    
    Returns:
    - id: 벡터 ID
    - user_id: 소유자 유저 ID
    - role: talent 또는 company
    - reference_type: "talent" 또는 "job_posting" (있을 경우)
    - reference_id: talent_card_id 또는 job_posting_card_id (있을 경우)
    - vector_roles, vector_skills, vector_growth, vector_career, vector_vision, vector_culture: 벡터 값들
    - updated_at: 마지막 업데이트 시각
    """
    try:
        data = matching_vector_service.get_vector_detail_by_id(db, vector_id)
        return {"ok": True, "data": data}
    except HTTPException as exc:
        if exc.status_code == status.HTTP_404_NOT_FOUND:
            return _error_response(exc)
        raise
