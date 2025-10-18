from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_company_role
from app.schemas.company import CompanyFullIn
from app.schemas.job_posting import JobPostingCreateIn
from app.services import company_service
from app.services import job_posting_service


router = APIRouter(prefix="/api/me/company", tags=["company"])
public_router = APIRouter(prefix="/api/companies", tags=["company"])


def _serialize_company(company):
    return {
        "id": company.id,
        "basic": {
            "name": company.name or "",
            "industry": company.industry or "",
            "size": company.size,
            "location_city": company.location_city or "",
            "homepage_url": company.homepage_url,
            "career_page_url": company.career_page_url,
            "one_liner": company.one_liner,
        },
        "about": {
            "vision_mission": company.vision_mission,
            "business_domains": company.business_domains,
            "ideal_talent": company.ideal_talent,
            "culture": company.culture,
            "benefits": company.benefits,
        },
        "profile_step": company.profile_step or 0,
        "is_submitted": company.is_submitted or 0,
        "status": company.status,
        "created_at": company.created_at.isoformat() if company.created_at else None,
        "updated_at": company.updated_at.isoformat() if company.updated_at else None,
    }


@router.get("")
def get_company(user=Depends(require_company_role), db: Session = Depends(get_db)):
    try:
        company = company_service.get_my_company(db, owner_user_id=user["id"])
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            return JSONResponse(status_code=404, content={"ok": False, "error": e.detail})
        raise

    return {"ok": True, "data": _serialize_company(company)}


@router.post("/full")
def upsert_company_full(payload: CompanyFullIn, user=Depends(require_company_role), db: Session = Depends(get_db)):
    try:
        with db.begin():
            company = company_service.upsert_full(db, owner_user_id=user["id"], payload=payload.model_dump())
    except HTTPException as e:
        if e.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            return JSONResponse(status_code=422, content={"ok": False, "error": e.detail})
        raise

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "ok": True,
            "data": {
                "company_id": company.id,
                "profile_step": company.profile_step or 0,
                "is_submitted": company.is_submitted or 0,
            },
        },
    )


@router.post("/submit")
def submit_company(user=Depends(require_company_role), db: Session = Depends(get_db)):
    with db.begin():
        company = company_service.submit_company(db, owner_user_id=user["id"])
    return {
        "ok": True,
        "data": {"is_submitted": company.is_submitted or 0, "profile_step": company.profile_step or 0},
    }


@router.post("/job-postings")
def create_job_posting(payload: JobPostingCreateIn, user=Depends(require_company_role), db: Session = Depends(get_db)):
    try:
        with db.begin():
            posting = job_posting_service.create(db, owner_user_id=user["id"], payload=payload.model_dump())
    except HTTPException as e:
        if e.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_422_UNPROCESSABLE_ENTITY):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "ok": True,
            "data": {
                "id": posting.id,
                "company_id": posting.company_id,
                "title": posting.title,
                "position_group": posting.position_group,
                "position": getattr(posting, "position", None),
                "department": posting.department,
                "employment_type": posting.employment_type,
                "location_city": posting.location_city,
                "career_level": posting.career_level,
                "education_level": posting.education_level,
                "start_date": posting.start_date.isoformat() if posting.start_date else None,
                "term_months": posting.term_months,
                "homepage_url": posting.homepage_url,
                "deadline_date": posting.deadline_date.isoformat() if posting.deadline_date else None,
                "contact_email": posting.contact_email,
                "contact_phone": posting.contact_phone,
                "salary_range": posting.salary_range,
                "responsibilities": posting.responsibilities,
                "requirements_must": posting.requirements_must,
                "requirements_nice": posting.requirements_nice,
                "competencies": posting.competencies,
                "status": posting.status,
                "jd_file_id": posting.jd_file_id,
                "extra_file_id": posting.extra_file_id,
                "published_at": posting.published_at.isoformat() if posting.published_at else None,
                "closed_at": posting.closed_at.isoformat() if posting.closed_at else None,
                "deleted_at": posting.deleted_at.isoformat() if posting.deleted_at else None,
                "created_at": posting.created_at.isoformat() if posting.created_at else None,
                "updated_at": posting.updated_at.isoformat() if posting.updated_at else None,
            },
        },
    )


@router.get("/job-postings")
def list_job_postings(posting_status: str | None = None, user=Depends(require_company_role), db: Session = Depends(get_db)):
    try:
        postings = job_posting_service.list_mine(db, owner_user_id=user["id"], status_filter=posting_status)
    except HTTPException as e:
        if e.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_422_UNPROCESSABLE_ENTITY):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise

    items = [
        {
            "id": p.id,
            "company_id": p.company_id,
            "title": p.title,
            "position_group": p.position_group,
            "position": getattr(p, "position", None),
            "department": p.department,
            "employment_type": p.employment_type,
            "location_city": p.location_city,
            "career_level": p.career_level,
            "education_level": p.education_level,
            "start_date": p.start_date.isoformat() if p.start_date else None,
            "term_months": p.term_months,
            "homepage_url": p.homepage_url,
            "deadline_date": p.deadline_date.isoformat() if p.deadline_date else None,
            "contact_email": p.contact_email,
            "contact_phone": p.contact_phone,
            "salary_range": p.salary_range,
            "responsibilities": p.responsibilities,
            "requirements_must": p.requirements_must,
            "requirements_nice": p.requirements_nice,
            "competencies": p.competencies,
            "status": p.status,
            "jd_file_id": p.jd_file_id,
            "extra_file_id": p.extra_file_id,
            "published_at": p.published_at.isoformat() if p.published_at else None,
            "closed_at": p.closed_at.isoformat() if p.closed_at else None,
            "deleted_at": p.deleted_at.isoformat() if p.deleted_at else None,
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "updated_at": p.updated_at.isoformat() if p.updated_at else None,
        }
        for p in postings
    ]

    return {"ok": True, "data": items}


@router.patch("/job-postings/{posting_id}")
def update_job_posting(
    posting_id: int,
    payload: dict,
    user=Depends(require_company_role),
    db: Session = Depends(get_db),
):
    try:
        with db.begin():
            posting = job_posting_service.update(db, owner_user_id=user["id"], posting_id=posting_id, payload=payload)
    except HTTPException as e:
        if e.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise

    return {
        "ok": True,
        "data": {
            "id": posting.id,
            "company_id": posting.company_id,
            "title": posting.title,
            "position_group": posting.position_group,
            "position": getattr(posting, "position", None),
            "department": posting.department,
            "employment_type": posting.employment_type,
            "location_city": posting.location_city,
            "career_level": posting.career_level,
            "education_level": posting.education_level,
            "start_date": posting.start_date.isoformat() if posting.start_date else None,
            "term_months": posting.term_months,
            "homepage_url": posting.homepage_url,
            "deadline_date": posting.deadline_date.isoformat() if posting.deadline_date else None,
            "contact_email": posting.contact_email,
            "contact_phone": posting.contact_phone,
            "salary_range": posting.salary_range,
            "responsibilities": posting.responsibilities,
            "requirements_must": posting.requirements_must,
            "requirements_nice": posting.requirements_nice,
            "competencies": posting.competencies,
            "status": posting.status,
            "jd_file_id": posting.jd_file_id,
            "extra_file_id": posting.extra_file_id,
            "published_at": posting.published_at.isoformat() if posting.published_at else None,
            "closed_at": posting.closed_at.isoformat() if posting.closed_at else None,
            "deleted_at": posting.deleted_at.isoformat() if posting.deleted_at else None,
            "created_at": posting.created_at.isoformat() if posting.created_at else None,
            "updated_at": posting.updated_at.isoformat() if posting.updated_at else None,
        },
    }


@router.delete("/job-postings/{posting_id}")
def delete_job_posting(
    posting_id: int,
    user=Depends(require_company_role),
    db: Session = Depends(get_db),
):
    try:
        with db.begin():
            posting = job_posting_service.delete(db, owner_user_id=user["id"], posting_id=posting_id)
    except HTTPException as e:
        if e.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise

    return {
        "ok": True,
        "data": {"id": posting.id, "deleted_at": posting.deleted_at.isoformat() if posting.deleted_at else None},
    }


@public_router.get("/{company_id}")
def get_company_profile(company_id: int, db: Session = Depends(get_db)):
    try:
        company = company_service.get_public_company(db, company_id=company_id)
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            return JSONResponse(status_code=404, content={"ok": False, "error": e.detail})
        raise

    return {"ok": True, "data": _serialize_company(company)}
