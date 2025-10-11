from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

import sqlalchemy as sa
from fastapi import HTTPException, status

from app.db.session import SessionLocal
from app.models.activity import Activity
from app.models.certification import Certification
from app.models.document import Document
from app.models.education import Education
from app.models.experience import Experience


def _validate_date_range(start, end):
    if start is not None and end is not None and end < start:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": "DATE_RANGE_INVALID", "message": "end_ym < start_ym"},
        )


def _require_owned(session, model, item_id: int, user_id: int):
    row = session.get(model, item_id)
    if row is None or getattr(row, "deleted_at", None) is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"code": "NOT_FOUND", "message": "Item not found"})
    if int(row.user_id) != int(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"code": "FORBIDDEN", "message": "Not your item"})
    return row


def _reject_none_for_required(payload: dict, required_fields: list[str]):
    for k in required_fields:
        if k in payload and payload[k] is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"code": "VALIDATION_ERROR", "message": f"{k} cannot be null"},
            )


# Education
def create_education(user_id: int, payload: dict) -> Education:
    _validate_date_range(payload.get("start_ym"), payload.get("end_ym"))
    with SessionLocal() as session:
        with session.begin():
            row = Education(user_id=user_id, **payload)
            session.add(row)
            session.flush()
            session.refresh(row)
            return row


def update_education(user_id: int, edu_id: int, payload: dict) -> Education:
    if "start_ym" in payload or "end_ym" in payload:
        _validate_date_range(payload.get("start_ym"), payload.get("end_ym"))
    _reject_none_for_required(payload, ["school_name", "status"])
    with SessionLocal() as session:
        with session.begin():
            row = _require_owned(session, Education, edu_id, user_id)
            for k, v in payload.items():
                setattr(row, k, v)
            session.flush()
            session.refresh(row)
            return row


def delete_education(user_id: int, edu_id: int) -> Education:
    with SessionLocal() as session:
        with session.begin():
            row = _require_owned(session, Education, edu_id, user_id)
            row.deleted_at = datetime.utcnow()
            session.flush()
            session.refresh(row)
            return row


# Experience
def create_experience(user_id: int, payload: dict) -> Experience:
    _validate_date_range(payload.get("start_ym"), payload.get("end_ym"))
    with SessionLocal() as session:
        with session.begin():
            title = payload.get("title") or ""
            row = Experience(
                user_id=user_id,
                company_name=payload.get("company_name", ""),
                title=title,
                start_ym=payload.get("start_ym"),
                end_ym=payload.get("end_ym"),
                leave_reason=payload.get("leave_reason"),
                summary=payload.get("summary"),
            )
            session.add(row)
            session.flush()
            session.refresh(row)
            return row


def update_experience(user_id: int, exp_id: int, payload: dict) -> Experience:
    if "start_ym" in payload or "end_ym" in payload:
        _validate_date_range(payload.get("start_ym"), payload.get("end_ym"))
    _reject_none_for_required(payload, ["company_name", "title"])
    with SessionLocal() as session:
        with session.begin():
            row = _require_owned(session, Experience, exp_id, user_id)
            for k, v in payload.items():
                setattr(row, k, v)
            session.flush()
            session.refresh(row)
            return row


def delete_experience(user_id: int, exp_id: int) -> Experience:
    with SessionLocal() as session:
        with session.begin():
            row = _require_owned(session, Experience, exp_id, user_id)
            row.deleted_at = datetime.utcnow()
            session.flush()
            session.refresh(row)
            return row


# Activity
def create_activity(user_id: int, payload: dict) -> Activity:
    with SessionLocal() as session:
        with session.begin():
            row = Activity(user_id=user_id, **payload)
            session.add(row)
            session.flush()
            session.refresh(row)
            return row


def update_activity(user_id: int, activity_id: int, payload: dict) -> Activity:
    _reject_none_for_required(payload, ["name"])
    with SessionLocal() as session:
        with session.begin():
            row = _require_owned(session, Activity, activity_id, user_id)
            for k, v in payload.items():
                setattr(row, k, v)
            session.flush()
            session.refresh(row)
            return row


def delete_activity(user_id: int, activity_id: int) -> Activity:
    with SessionLocal() as session:
        with session.begin():
            row = _require_owned(session, Activity, activity_id, user_id)
            row.deleted_at = datetime.utcnow()
            session.flush()
            session.refresh(row)
            return row


# Certification
def create_certification(user_id: int, payload: dict) -> Certification:
    with SessionLocal() as session:
        with session.begin():
            row = Certification(user_id=user_id, **payload)
            session.add(row)
            session.flush()
            session.refresh(row)
            return row


def update_certification(user_id: int, cert_id: int, payload: dict) -> Certification:
    _reject_none_for_required(payload, ["name"])
    with SessionLocal() as session:
        with session.begin():
            row = _require_owned(session, Certification, cert_id, user_id)
            for k, v in payload.items():
                setattr(row, k, v)
            session.flush()
            session.refresh(row)
            return row


def delete_certification(user_id: int, cert_id: int) -> Certification:
    with SessionLocal() as session:
        with session.begin():
            row = _require_owned(session, Certification, cert_id, user_id)
            row.deleted_at = datetime.utcnow()
            session.flush()
            session.refresh(row)
            return row


# Document
def create_document(user_id: int, payload: dict) -> Document:
    with SessionLocal() as session:
        with session.begin():
            data = payload.copy()
            if "storage_url" in data and data["storage_url"] is not None:
                data["storage_url"] = str(data["storage_url"])
            row = Document(user_id=user_id, **data)
            session.add(row)
            session.flush()
            session.refresh(row)
            return row


def update_document(user_id: int, doc_id: int, payload: dict) -> Document:
    _reject_none_for_required(payload, ["doc_type", "storage_url", "original_name"])
    with SessionLocal() as session:
        with session.begin():
            row = _require_owned(session, Document, doc_id, user_id)
            for k, v in payload.items():
                if k == "storage_url" and v is not None:
                    v = str(v)
                setattr(row, k, v)
            session.flush()
            session.refresh(row)
            return row


def delete_document(user_id: int, doc_id: int) -> Document:
    with SessionLocal() as session:
        with session.begin():
            row = _require_owned(session, Document, doc_id, user_id)
            row.deleted_at = datetime.utcnow()
            session.flush()
            session.refresh(row)
            return row
