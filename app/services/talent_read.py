from __future__ import annotations

from collections.abc import Sequence
from typing import Optional, Type, TypeVar

import sqlalchemy as sa
from pydantic import BaseModel

from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.certification import Certification
from app.models.document import Document
from app.models.education import Education
from app.models.experience import Experience
from app.models.profile import TalentProfile
from app.schemas.talent_read import (
    ActivityOut,
    CertificationOut,
    DocumentOut,
    EducationOut,
    ExperienceOut,
    TalentBasicOut,
)

TModel = TypeVar("TModel")
TSchema = TypeVar("TSchema", bound=BaseModel)


def _list_for_user(
    model: Type[TModel],
    schema: Type[TSchema],
    user_id: int,
    order_by: Sequence[sa.ColumnElement] | None = None,
) -> list[TSchema]:
    stmt = sa.select(model).where(model.user_id == user_id)
    deleted_attr = getattr(model, "deleted_at", None)
    if deleted_attr is not None:
        stmt = stmt.where(deleted_attr.is_(None))
    if order_by:
        stmt = stmt.order_by(*order_by)

    with SessionLocal() as session:
        rows = session.execute(stmt).scalars().all()

    return [schema.model_validate(row, from_attributes=True) for row in rows]


def get_basic_profile(user_id: int) -> Optional[TalentBasicOut]:
    with SessionLocal() as session:
        profile = session.get(TalentProfile, user_id)

    if profile is None or getattr(profile, "deleted_at", None) is not None:
        return None

    return TalentBasicOut.model_validate(profile, from_attributes=True)


def list_educations(user_id: int) -> list[EducationOut]:
    return _list_for_user(
        Education,
        EducationOut,
        user_id,
        order_by=(Education.start_ym.asc(), Education.id.asc()),
    )


def list_experiences(user_id: int) -> list[ExperienceOut]:
    return _list_for_user(
        Experience,
        ExperienceOut,
        user_id,
        order_by=(Experience.start_ym.desc(), Experience.id.desc()),
    )


def list_activities(user_id: int) -> list[ActivityOut]:
    return _list_for_user(
        Activity,
        ActivityOut,
        user_id,
        order_by=(Activity.period_ym.desc(), Activity.id.desc()),
    )


def list_certifications(user_id: int) -> list[CertificationOut]:
    return _list_for_user(
        Certification,
        CertificationOut,
        user_id,
        order_by=(Certification.acquired_ym.desc(), Certification.id.desc()),
    )


def list_documents(user_id: int) -> list[DocumentOut]:
    return _list_for_user(
        Document,
        DocumentOut,
        user_id,
        order_by=(Document.created_at.desc(), Document.id.desc()),
    )
