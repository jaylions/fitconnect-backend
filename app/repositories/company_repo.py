from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.company import Company


def get_by_owner(db: Session, user_id: int) -> Optional[Company]:
    return db.execute(select(Company).where(Company.owner_user_id == user_id)).scalar_one_or_none()


def seed_if_absent(db: Session, owner_user_id: int) -> Company:
    company = get_by_owner(db, owner_user_id)
    if company is not None:
        return company
    company = Company(
        owner_user_id=owner_user_id,
        name="",
        industry="",
        location_city="",
    )
    db.add(company)
    db.flush()
    return company


def update_full(
    db: Session,
    owner_user_id: int,
    basic: dict,
    about: dict,
    submit: bool,
) -> Company:
    company = seed_if_absent(db, owner_user_id)

    # Update basic fields
    company.name = basic.get("name", company.name)
    company.industry = basic.get("industry", company.industry)
    company.size = basic.get("size")
    company.location_city = basic.get("location_city", company.location_city)
    company.homepage_url = basic.get("homepage_url")
    company.career_page_url = basic.get("career_page_url")
    company.one_liner = basic.get("one_liner")

    # Update about fields
    company.vision_mission = about.get("vision_mission")
    company.business_domains = about.get("business_domains")
    company.ideal_talent = about.get("ideal_talent")
    company.culture = about.get("culture")
    company.benefits = about.get("benefits")

    # Submit handling
    if submit:
        company.is_submitted = 1
        company.profile_step = max(company.profile_step or 0, 2)

    db.flush()
    return company

