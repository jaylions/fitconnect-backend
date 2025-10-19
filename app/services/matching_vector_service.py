from __future__ import annotations

from typing import Any, Dict

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import matching_vector_repo

ALLOWED_ROLES = {"talent", "company"}
VECTOR_FIELDS = (
    "vector_roles",
    "vector_skills",
    "vector_growth",
    "vector_career",
    "vector_vision",
    "vector_culture",
)


def _error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})


def _require_owned(db_row, user_id: int):
    if db_row is None:
        raise _error(status.HTTP_404_NOT_FOUND, "MATCHING_VECTOR_NOT_FOUND", "Matching vector not found")
    if int(db_row.user_id) != int(user_id):
        raise _error(status.HTTP_403_FORBIDDEN, "FORBIDDEN", "Not your matching vector")
    return db_row


def _filter_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    return {field: data[field] for field in VECTOR_FIELDS if field in data}


def create(db: Session, user_id: int, role: str, payload: Dict[str, Any]):
    if role not in ALLOWED_ROLES:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "INVALID_ROLE", "role must be 'talent' or 'company'")

    existing = matching_vector_repo.get_by_user_and_role(db, user_id=user_id, role=role)
    if existing is not None:
        raise _error(
            status.HTTP_409_CONFLICT,
            "MATCHING_VECTOR_EXISTS",
            "Matching vector already exists for this role",
        )

    # Ensure payload uses only allowed fields
    filtered = _filter_payload(payload)
    row = matching_vector_repo.create(db, user_id=user_id, role=role, payload=filtered)
    return row


def update(db: Session, user_id: int, matching_vector_id: int, payload: Dict[str, Any]):
    row = matching_vector_repo.get_by_id(db, matching_vector_id)
    row = _require_owned(row, user_id)

    filtered = _filter_payload(payload)
    if not filtered:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "NO_FIELDS_TO_UPDATE", "Provide at least one field to update")

    return matching_vector_repo.update(db, row=row, payload=filtered)


def delete(db: Session, user_id: int, matching_vector_id: int):
    row = matching_vector_repo.get_by_id(db, matching_vector_id)
    row = _require_owned(row, user_id)
    matching_vector_repo.delete(db, row=row)
    return row


def get_vector_detail_by_id(db: Session, vector_id: int) -> Dict[str, Any]:
    """
    Vector ID로 벡터 상세 정보 조회 (인증 불필요)
    - role 반환
    - talent_card_id 또는 job_posting_card_id 조회하여 어떤 참조인지 반환
    - 모든 vector 값 반환
    """
    from app.models.talent_card import TalentCard
    from app.models.job_posting_card import JobPostingCard

    row = matching_vector_repo.get_by_id(db, vector_id)
    if row is None:
        raise _error(status.HTTP_404_NOT_FOUND, "MATCHING_VECTOR_NOT_FOUND", "Matching vector not found")

    result = {
        "id": row.id,
        "user_id": row.user_id,
        "role": row.role,
        "reference_type": None,
        "reference_id": None,
        "vector_roles": row.vector_roles,
        "vector_skills": row.vector_skills,
        "vector_growth": row.vector_growth,
        "vector_career": row.vector_career,
        "vector_vision": row.vector_vision,
        "vector_culture": row.vector_culture,
        "updated_at": row.updated_at,
    }

    # role에 따라 talent_card 또는 job_posting_card 찾기
    if row.role == "talent":
        talent_card = db.query(TalentCard).filter(TalentCard.user_id == row.user_id).first()
        if talent_card:
            result["reference_type"] = "talent"
            result["reference_id"] = talent_card.id
    elif row.role == "company":
        job_posting_card = db.query(JobPostingCard).filter(JobPostingCard.user_id == row.user_id).first()
        if job_posting_card:
            result["reference_type"] = "job_posting"
            result["reference_id"] = job_posting_card.id

    return result
