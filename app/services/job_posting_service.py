from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import company_repo
from app.repositories import job_posting_repo

ALLOWED_EMPLOYMENT = {
    "정규직",
    "계약직",
    "파견직",
    "인턴",
    "임시직",
    "기타",
    # 기존 영문 값도 허용 (하위 호환성)
    "FULL_TIME",
    "PART_TIME",
    "CONTRACT",
    "INTERN",
    "TEMP",
    "OTHER",
}

ALLOWED_STATUS = {"DRAFT", "PUBLISHED", "CLOSED", "ARCHIVED"}


def _val_error(msg: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"code": "VALIDATION_ERROR", "message": msg})


def get_by_id(db: Session, job_posting_id: int):
    """채용공고 ID로 조회 (공개 API용)"""
    posting = job_posting_repo.get_by_id(db, job_posting_id)
    if posting is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "JOB_POSTING_NOT_FOUND", "message": "Job posting not found"}
        )
    return posting


def create(db: Session, owner_user_id: int, payload: dict):
    # Ensure company exists for user
    company = company_repo.get_by_owner(db, owner_user_id)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"code": "COMPANY_NOT_FOUND", "message": "Company not found"})

    # Minimal validations
    required = ("title", "employment_type", "location_city", "career_level", "education_level")
    for k in required:
        v = payload.get(k)
        if not isinstance(v, str) or not v.strip():
            raise _val_error(f"{k} is required")

    et = payload.get("employment_type")
    if et not in ALLOWED_EMPLOYMENT:
        raise _val_error("employment_type invalid")

    st = payload.get("status") or "DRAFT"
    if st not in ALLOWED_STATUS:
        raise _val_error("status invalid")
    payload["status"] = st

    posting = job_posting_repo.create(db, company_id=company.id, data=payload)
    return posting


def list_mine(db: Session, owner_user_id: int, status_filter: str | None = None):
    # Ensure company exists
    company = company_repo.get_by_owner(db, owner_user_id)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"code": "COMPANY_NOT_FOUND", "message": "Company not found"})

    if status_filter is not None and status_filter not in ALLOWED_STATUS:
        raise _val_error("status invalid")

    postings = job_posting_repo.list_by_company(db, company_id=company.id, status=status_filter)
    return postings


def update(db: Session, owner_user_id: int, posting_id: int, payload: dict):
    # Ensure company exists for user
    company = company_repo.get_by_owner(db, owner_user_id)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"code": "COMPANY_NOT_FOUND", "message": "Company not found"})

    # Fetch posting
    posting = job_posting_repo.get_by_id_and_company(db, posting_id=posting_id, company_id=company.id)
    if posting is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"code": "JOB_POSTING_NOT_FOUND", "message": "Job posting not found"})

    # Validate enums when present
    et = payload.get("employment_type")
    if et is not None and et not in ALLOWED_EMPLOYMENT:
        raise _val_error("employment_type invalid")

    st = payload.get("status")
    if st is not None and st not in ALLOWED_STATUS:
        raise _val_error("status invalid")

    posting = job_posting_repo.update_partial(db, posting, data=payload)
    return posting


def delete(db: Session, owner_user_id: int, posting_id: int):
    # Ensure company exists for user
    company = company_repo.get_by_owner(db, owner_user_id)
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"code": "COMPANY_NOT_FOUND", "message": "Company not found"})

    # Fetch posting
    posting = job_posting_repo.get_by_id_and_company(db, posting_id=posting_id, company_id=company.id)
    if posting is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"code": "JOB_POSTING_NOT_FOUND", "message": "Job posting not found"})

    posting = job_posting_repo.soft_delete(db, posting)
    return posting
