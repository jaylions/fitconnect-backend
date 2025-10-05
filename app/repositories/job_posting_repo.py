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
    stmt = select(JobPosting).where(JobPosting.company_id == company_id)
    if status is not None:
        stmt = stmt.where(JobPosting.status == status)
    stmt = stmt.order_by(desc(JobPosting.created_at))
    return db.execute(stmt).scalars().all()
