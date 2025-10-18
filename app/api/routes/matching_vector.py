from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.schemas.matching_vector import (
    MatchingVectorCreateIn,
    MatchingVectorOut,
    MatchingVectorUpdateIn,
)
from app.services import matching_vector_service


router = APIRouter(prefix="/api/me/matching-vectors", tags=["matching_vectors"])


def _serialize(row) -> dict:
    return MatchingVectorOut.model_validate(row, from_attributes=True).model_dump(mode="json")


def _error_response(exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"ok": False, "error": exc.detail})


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
