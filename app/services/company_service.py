from __future__ import annotations

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import company_repo

ALLOWED_SIZE = {
    "S_1_10",
    "S_11_50",
    "M_51_200",
    "L_201_500",
    "XL_501_1000",
    "ENT_1000P",
}


def _error(code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"code": code, "message": message})


def validate_full_payload(payload: dict) -> None:
    basic = payload.get("basic") or {}
    about = payload.get("about") or {}

    for key in ("name", "industry", "location_city"):
        v = basic.get(key)
        if not isinstance(v, str) or not v.strip():
            raise _error("VALIDATION_ERROR", f"{key} is required")

    size: Optional[str] = basic.get("size")
    if size is not None and size not in ALLOWED_SIZE:
        raise _error("VALIDATION_ERROR", "size must be one of allowed enum or null")

    one_liner = basic.get("one_liner")
    if one_liner is not None and len(one_liner) > 120:
        raise _error("VALIDATION_ERROR", "one_liner must be <= 120 chars")

    # URL validation is handled by Pydantic at schema layer if using HttpUrl.
    # Here we keep minimal additional checks.


def get_my_company(db: Session, owner_user_id: int):
    company = company_repo.get_by_owner(db, owner_user_id)
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "COMPANY_NOT_FOUND", "message": "Company not found for user"},
        )
    return company


def upsert_full(db: Session, owner_user_id: int, payload: dict):
    validate_full_payload(payload)
    basic = payload["basic"]
    about = payload.get("about") or {}
    submit = bool(payload.get("submit"))
    company = company_repo.update_full(db, owner_user_id, basic=basic, about=about, submit=submit)
    return company


def submit_company(db: Session, owner_user_id: int):
    company = company_repo.seed_if_absent(db, owner_user_id)
    company.is_submitted = 1
    company.profile_step = max(company.profile_step or 0, 2)
    db.flush()
    return company

