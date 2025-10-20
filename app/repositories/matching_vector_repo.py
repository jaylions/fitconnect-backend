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


def get_by_user_and_job_posting(
    db: Session, user_id: int, job_posting_id: Optional[int]
) -> Optional[MatchingVector]:
    """
    user_id와 job_posting_id로 벡터 조회
    - talent: job_posting_id=None, user_id로만 조회
    - company: job_posting_id로 조회
    """
    stmt = select(MatchingVector).where(
        MatchingVector.user_id == user_id,
        MatchingVector.job_posting_id == job_posting_id,
    )
    return db.execute(stmt).scalar_one_or_none()


def get_all_by_user(db: Session, user_id: int) -> list[MatchingVector]:
    """
    user_id로 모든 벡터 조회 (최신순)
    - talent: 최대 1개
    - company: 여러 개 가능
    """
    stmt = (
        select(MatchingVector)
        .where(MatchingVector.user_id == user_id)
        .order_by(MatchingVector.updated_at.desc())
    )
    return list(db.execute(stmt).scalars().all())


def create(
    db: Session,
    user_id: int,
    role: str,
    job_posting_id: Optional[int],
    payload: dict,
) -> MatchingVector:
    row = MatchingVector(
        user_id=user_id,
        role=role,
        job_posting_id=job_posting_id,
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
