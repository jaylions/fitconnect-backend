from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse

from app.api.deps import get_current_user
from app.core.settings import settings  # noqa: F401  # kept for parity, not used directly
from app.schemas.full_profile import FullProfileIn
from app.schemas.talent_response import (
    TalentActivityListResponse,
    TalentBasicResponse,
    TalentCertificationListResponse,
    TalentDocumentListResponse,
    TalentEducationListResponse,
    TalentExperienceListResponse,
)
from app.services.full_profile import save_full_profile
from app.services.talent_read import (
    get_basic_profile,
    list_activities,
    list_certifications,
    list_documents,
    list_educations,
    list_experiences,
)


router = APIRouter(prefix="/api/me/talent", tags=["talent"])


@router.post("/full")
def save_full(
    body: FullProfileIn,
    user=Depends(get_current_user),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    user_id = int(user["id"])  # ensure int
    try:
        result = save_full_profile(user_id=user_id, payload=body)
    except HTTPException as e:
        if e.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            detail = (
                e.detail
                if isinstance(e.detail, dict)
                else {"code": "DATE_RANGE_INVALID", "message": "end_ym < start_ym"}
            )
            return JSONResponse(status_code=422, content={"ok": False, "error": detail})
        raise

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "ok": True,
            "data": {
                "user_id": result.user_id,
                "profile_step": result.profile_step,
                "is_submitted": result.is_submitted,
            },
        },
    )


@router.get("/basic", response_model=TalentBasicResponse)
def read_basic_profile(user=Depends(get_current_user)) -> TalentBasicResponse:
    basic = get_basic_profile(int(user["id"]))
    return TalentBasicResponse(data=basic)


@router.get("/educations", response_model=TalentEducationListResponse)
def read_educations(user=Depends(get_current_user)) -> TalentEducationListResponse:
    educations = list_educations(int(user["id"]))
    return TalentEducationListResponse(data=educations)


@router.get("/experiences", response_model=TalentExperienceListResponse)
def read_experiences(user=Depends(get_current_user)) -> TalentExperienceListResponse:
    experiences = list_experiences(int(user["id"]))
    return TalentExperienceListResponse(data=experiences)


@router.get("/activities", response_model=TalentActivityListResponse)
def read_activities(user=Depends(get_current_user)) -> TalentActivityListResponse:
    activities = list_activities(int(user["id"]))
    return TalentActivityListResponse(data=activities)


@router.get("/certifications", response_model=TalentCertificationListResponse)
def read_certifications(user=Depends(get_current_user)) -> TalentCertificationListResponse:
    certifications = list_certifications(int(user["id"]))
    return TalentCertificationListResponse(data=certifications)


@router.get("/documents", response_model=TalentDocumentListResponse)
def read_documents(user=Depends(get_current_user)) -> TalentDocumentListResponse:
    documents = list_documents(int(user["id"]))
    return TalentDocumentListResponse(data=documents)

