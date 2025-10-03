from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

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
        department=data.get("department"),
        start_date=data.get("start_date"),
        term_months=data.get("term_months"),
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

