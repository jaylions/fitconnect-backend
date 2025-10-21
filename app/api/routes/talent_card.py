from __future__ import annotations

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
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
    db.add(card)
    db.flush()  # PK 생성을 위해 flush
    db.refresh(card)  # 관계 로딩

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


@router.patch("/{user_id}")
def update_talent_card(
    user_id: int,
    payload: TalentCardCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Talent Card 전체 덮어쓰기 업데이트
    - JWT 인증 필수
    - 본인 카드만 수정 가능
    - POST와 동일한 Body 구조 사용
    """
    # 1. JWT user_id와 path user_id 일치 확인
    jwt_user_id = int(user["id"])
    if jwt_user_id != user_id:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "ok": False,
                "error": {
                    "code": "FORBIDDEN",
                    "message": "You can only update your own talent card",
                },
            },
        )

    # 2. 카드 존재 확인
    card = db.scalar(select(TalentCard).where(TalentCard.user_id == user_id))
    if card is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "ok": False,
                "error": {
                    "code": "CARD_NOT_FOUND",
                    "message": f"Talent card not found for user_id {user_id}",
                },
            },
        )

    # 3. 전체 덮어쓰기 (payload의 모든 필드로 업데이트)
    update_data = payload.model_dump(exclude={"user_id"})  # user_id는 제외
    for field, value in update_data.items():
        setattr(card, field, value)

    db.flush()
    db.refresh(card)

    response = TalentCardResponse.model_validate(card)
    return {"ok": True, "data": response.model_dump(mode="json")}
