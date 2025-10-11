from __future__ import annotations

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.talent_card import TalentCard
from app.models.user import User
from app.schemas.talent_card import TalentCardCreate, TalentCardResponse


router = APIRouter(prefix="/api/talent_cards", tags=["TalentCard"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_talent_card(payload: TalentCardCreate, db: Session = Depends(get_db)):
    user = db.get(User, payload.user_id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"ok": False, "error": {"code": "USER_NOT_FOUND", "message": "User not found"}},
        )

    if user.role != "talent":
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "ok": False,
                "error": {"code": "USER_NOT_TALENT", "message": "User is not a talent"},
            },
        )

    existing = db.scalar(select(TalentCard).where(TalentCard.user_id == payload.user_id))
    if existing is not None:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "ok": False,
                "error": {"code": "CARD_EXISTS", "message": "Talent already has a card"},
            },
        )

    card = TalentCard(**payload.model_dump())
    with db.begin():
        db.add(card)

    response = TalentCardResponse.model_validate(card)
    return {"ok": True, "data": response.model_dump(mode="json")}


@router.get("/{user_id}")
def get_talent_card(user_id: int, db: Session = Depends(get_db)):
    card = db.scalar(select(TalentCard).where(TalentCard.user_id == user_id))
    if card is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"ok": False, "error": {"code": "NOT_FOUND", "message": "Card not found"}},
        )

    response = TalentCardResponse.model_validate(card)
    return {"ok": True, "data": response.model_dump(mode="json")}
