from __future__ import annotations

from typing import Optional, Sequence

from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.models.job_posting import JobPosting


def create(db: Session, company_id: int, data: dict) -> JobPosting:
    posting = JobPosting(
        company_id=company_id,
        title=data["title"],
        employment_type=data["employment_type"],
        location_city=data["location_city"],
        career_level=data["career_level"],
        education_level=data["education_level"],
        position_group=data.get("position_group"),
        position=data.get("position"),
        department=data.get("department"),
        start_date=data.get("start_date") or data.get("join"),
        term_months=data.get("term_months") or data.get("period"),
        homepage_url=data.get("homepage_url"),
        deadline_date=data.get("deadline_date"),
        contact_email=data.get("contact_email"),
        contact_phone=data.get("contact_phone"),
        salary_band=data.get("salary_band"),
        responsibilities=data.get("responsibilities"),
        requirements_must=data.get("requirements_must"),
        requirements_nice=data.get("requirements_nice"),
        competencies=data.get("competencies"),
        jd_file_id=data.get("jd_file_id"),
        extra_file_id=data.get("extra_file_id"),
        status=data.get("status") or "DRAFT",
    )
    db.add(posting)
    db.flush()
    return posting


def list_by_company(db: Session, company_id: int, status: Optional[str] = None) -> Sequence[JobPosting]:
    stmt = select(JobPosting).where(JobPosting.company_id == company_id, JobPosting.deleted_at.is_(None))
    if status is not None:
        stmt = stmt.where(JobPosting.status == status)
    stmt = stmt.order_by(desc(JobPosting.created_at))
    return db.execute(stmt).scalars().all()


def get_by_id_and_company(db: Session, posting_id: int, company_id: int) -> Optional[JobPosting]:
    stmt = (
        select(JobPosting)
        .where(JobPosting.id == posting_id, JobPosting.company_id == company_id, JobPosting.deleted_at.is_(None))
        .limit(1)
    )
    return db.execute(stmt).scalar_one_or_none()


def update_partial(db: Session, posting: JobPosting, data: dict) -> JobPosting:
    # Map aliases
    if "join" in data and data.get("join") is not None:
        data["start_date"] = data.pop("join")
    if "period" in data and data.get("period") is not None:
        data["term_months"] = data.pop("period")

    # Allowed fields to patch
    allowed = {
        "title",
        "employment_type",
        "location_city",
        "career_level",
        "education_level",
        "position_group",
        "position",
        "department",
        "start_date",
        "term_months",
        "homepage_url",
        "deadline_date",
        "contact_email",
        "contact_phone",
        "salary_band",
        "responsibilities",
        "requirements_must",
        "requirements_nice",
        "competencies",
        "jd_file_id",
        "extra_file_id",
        "status",
        "published_at",
        "closed_at",
    }
    for k, v in list(data.items()):
        if k in allowed:
            setattr(posting, k, v)
    db.flush()
    return posting


def soft_delete(db: Session, posting: JobPosting) -> JobPosting:
    from datetime import datetime

    posting.deleted_at = datetime.utcnow()
    db.flush()
    return posting
