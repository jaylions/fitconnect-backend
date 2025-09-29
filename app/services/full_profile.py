from __future__ import annotations

from typing import Iterable

import sqlalchemy as sa
from fastapi import HTTPException, status

from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.certification import Certification
from app.models.document import Document
from app.models.education import Education
from app.models.experience import Experience
from app.models.profile import TalentProfile
from app.schemas.full_profile import FullProfileIn, FullProfileOut


def _validate_date_range(start, end):
    if start is not None and end is not None and end < start:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "DATE_RANGE_INVALID", "message": "end_ym < start_ym"},
        )


def _bulk_delete_insert(session, model, user_id: int, rows: Iterable[dict]):
    session.execute(sa.delete(model).where(model.user_id == user_id))
    if rows:
        session.execute(sa.insert(model), rows)


def save_full_profile(user_id: int, payload: FullProfileIn) -> FullProfileOut:
    with SessionLocal() as session:
        with session.begin():
            # Upsert talent profile
            profile = session.get(TalentProfile, user_id)
            if profile is None:
                profile = TalentProfile(user_id=user_id)
                session.add(profile)

            profile.name = payload.basic.name
            profile.birth_date = payload.basic.birth_date
            profile.phone = payload.basic.phone
            profile.tagline = payload.basic.tagline

            # Submission logic
            should_submit = bool(payload.submit) or bool(payload.basic.is_submitted)
            if should_submit:
                profile.is_submitted = True
                profile.profile_step = 5

            # Educations
            edu_rows: list[dict] = []
            for e in payload.educations:
                _validate_date_range(e.start_ym, e.end_ym)
                edu_rows.append(
                    {
                        "user_id": user_id,
                        "school_name": e.school_name,
                        "major": e.major,
                        "status": e.status,
                        "start_ym": e.start_ym,
                        "end_ym": e.end_ym,
                    }
                )
            _bulk_delete_insert(session, Education, user_id, edu_rows)

            # Experiences
            exp_rows: list[dict] = []
            for x in payload.experiences:
                _validate_date_range(x.start_ym, x.end_ym)
                exp_rows.append(
                    {
                        "user_id": user_id,
                        "company_name": x.company_name,
                        "title": x.title or "",
                        "start_ym": x.start_ym,
                        "end_ym": x.end_ym,
                        "leave_reason": x.leave_reason,
                        "summary": x.summary,
                    }
                )
            _bulk_delete_insert(session, Experience, user_id, exp_rows)

            # Activities
            act_rows: list[dict] = []
            for a in payload.activities:
                act_rows.append(
                    {
                        "user_id": user_id,
                        "name": a.name,
                        "category": a.category,
                        "period_ym": a.period_ym,
                        "description": a.description,
                    }
                )
            _bulk_delete_insert(session, Activity, user_id, act_rows)

            # Certifications
            cert_rows: list[dict] = []
            for c in payload.certifications:
                cert_rows.append(
                    {
                        "user_id": user_id,
                        "name": c.name,
                        "score_or_grade": c.score_or_grade,
                        "acquired_ym": c.acquired_ym,
                    }
                )
            _bulk_delete_insert(session, Certification, user_id, cert_rows)

            # Documents
            doc_rows: list[dict] = []
            for d in payload.documents:
                doc_rows.append(
                    {
                        "user_id": user_id,
                        "doc_type": d.doc_type,
                        "storage_url": str(d.storage_url),
                        "original_name": d.original_name,
                        "mime_type": d.mime_type,
                        "file_size": d.file_size,
                    }
                )
            _bulk_delete_insert(session, Document, user_id, doc_rows)

            # Ensure profile is loaded with latest flags
            session.flush()

            return FullProfileOut(
                user_id=user_id,
                profile_step=profile.profile_step or 0,
                is_submitted=1 if profile.is_submitted else 0,
            )

