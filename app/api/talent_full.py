from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.settings import settings
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
bearer = HTTPBearer(auto_error=False)


def get_current_user_id(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> int:
    if credentials is None or not credentials.scheme.lower() == "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        sub = payload.get("sub")
        if sub is None:
            raise ValueError("missing sub")
        return int(sub)
    except (JWTError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.post("/full")
def save_full(
    body: FullProfileIn,
    user_id: int = Depends(get_current_user_id),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        result = save_full_profile(user_id=user_id, payload=body)
    except HTTPException as e:
        if e.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            # Normalize to required error shape
            detail = e.detail if isinstance(e.detail, dict) else {
                "code": "DATE_RANGE_INVALID",
                "message": "end_ym < start_ym",
            }
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
def read_basic_profile(user_id: int = Depends(get_current_user_id)) -> TalentBasicResponse:
    basic = get_basic_profile(user_id)
    return TalentBasicResponse(data=basic)


@router.get("/educations", response_model=TalentEducationListResponse)
def read_educations(user_id: int = Depends(get_current_user_id)) -> TalentEducationListResponse:
    educations = list_educations(user_id)
    return TalentEducationListResponse(data=educations)


@router.get("/experiences", response_model=TalentExperienceListResponse)
def read_experiences(user_id: int = Depends(get_current_user_id)) -> TalentExperienceListResponse:
    experiences = list_experiences(user_id)
    return TalentExperienceListResponse(data=experiences)


@router.get("/activities", response_model=TalentActivityListResponse)
def read_activities(user_id: int = Depends(get_current_user_id)) -> TalentActivityListResponse:
    activities = list_activities(user_id)
    return TalentActivityListResponse(data=activities)


@router.get("/certifications", response_model=TalentCertificationListResponse)
def read_certifications(user_id: int = Depends(get_current_user_id)) -> TalentCertificationListResponse:
    certifications = list_certifications(user_id)
    return TalentCertificationListResponse(data=certifications)


@router.get("/documents", response_model=TalentDocumentListResponse)
def read_documents(user_id: int = Depends(get_current_user_id)) -> TalentDocumentListResponse:
    documents = list_documents(user_id)
    return TalentDocumentListResponse(data=documents)
