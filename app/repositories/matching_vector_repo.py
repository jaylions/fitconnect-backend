from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.matching_vector import MatchingVector


def get_by_id(db: Session, matching_vector_id: int) -> Optional[MatchingVector]:
    return db.get(MatchingVector, matching_vector_id)


def get_by_user_and_role(db: Session, user_id: int, role: str) -> Optional[MatchingVector]:
    stmt = select(MatchingVector).where(
        MatchingVector.user_id == user_id,
        MatchingVector.role == role,
    )
    return db.execute(stmt).scalar_one_or_none()


def create(
    db: Session,
    user_id: int,
    role: str,
    payload: dict,
) -> MatchingVector:
    row = MatchingVector(
        user_id=user_id,
        role=role,
        **payload,
    )
    db.add(row)
    db.flush()
    db.refresh(row)
    return row


def update(
    db: Session,
    row: MatchingVector,
    payload: dict,
) -> MatchingVector:
    for key, value in payload.items():
        setattr(row, key, value)
    db.flush()
    db.refresh(row)
    return row


def delete(db: Session, row: MatchingVector) -> None:
    db.delete(row)
    db.flush()
