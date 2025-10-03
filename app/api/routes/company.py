from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_company_role
from app.schemas.company import CompanyFullIn
from app.services import company_service


router = APIRouter(prefix="/api/me/company", tags=["company"])


@router.get("")
def get_company(user=Depends(require_company_role), db: Session = Depends(get_db)):
    try:
        company = company_service.get_my_company(db, owner_user_id=user["id"])
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            return JSONResponse(status_code=404, content={"ok": False, "error": e.detail})
        raise

    data = {
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
    return {"ok": True, "data": data}


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

