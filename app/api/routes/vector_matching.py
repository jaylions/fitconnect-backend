from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.schemas.vector_matching import VectorMatchRequest, VectorMatchResult
from app.services import vector_matching_service


router = APIRouter(prefix="/api/matching", tags=["vector_matching"])


@router.post("/vectors")
def match_vectors(
    payload: VectorMatchRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = vector_matching_service.match(
        db,
        source_id=payload.source_id,
        target_id=payload.target_id,
    )
    data = VectorMatchResult.model_validate(result).model_dump(mode="json")
    return {"ok": True, "data": data}
