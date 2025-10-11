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
    TalentFullData,
    TalentFullResponse,
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
from app.services import talent_write
from app.schemas.talent_write import (
    EducationCreateIn,
    EducationUpdateIn,
    ExperienceCreateIn,
    ExperienceUpdateIn,
    ActivityCreateIn,
    ActivityUpdateIn,
    CertificationCreateIn,
    CertificationUpdateIn,
    DocumentCreateIn,
    DocumentUpdateIn,
)
from app.schemas.talent_read import (
    EducationOut,
    ExperienceOut,
    ActivityOut,
    CertificationOut,
    DocumentOut,
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


@router.get("/full", response_model=TalentFullResponse)
def read_full_profile(user=Depends(get_current_user)) -> TalentFullResponse:
    user_id = int(user["id"])
    data = TalentFullData(
        basic=get_basic_profile(user_id),
        educations=list_educations(user_id),
        experiences=list_experiences(user_id),
        activities=list_activities(user_id),
        certifications=list_certifications(user_id),
        documents=list_documents(user_id),
    )
    return TalentFullResponse(data=data)


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


# Individual write APIs


@router.post("/educations")
def create_education(body: EducationCreateIn, user=Depends(get_current_user)):
    try:
        row = talent_write.create_education(int(user["id"]), body.model_dump())
    except HTTPException as e:
        if e.status_code in (status.HTTP_422_UNPROCESSABLE_ENTITY,):
            return JSONResponse(status_code=422, content={"ok": False, "error": e.detail})
        raise
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"ok": True, "data": EducationOut.model_validate(row, from_attributes=True).model_dump()})


@router.patch("/educations/{education_id}")
def update_education(education_id: int, body: EducationUpdateIn, user=Depends(get_current_user)):
    try:
        row = talent_write.update_education(int(user["id"]), education_id, body.model_dump(exclude_unset=True))
    except HTTPException as e:
        if e.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN, status.HTTP_422_UNPROCESSABLE_ENTITY):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise
    return {"ok": True, "data": EducationOut.model_validate(row, from_attributes=True).model_dump()}


@router.delete("/educations/{education_id}")
def delete_education(education_id: int, user=Depends(get_current_user)):
    try:
        row = talent_write.delete_education(int(user["id"]), education_id)
    except HTTPException as e:
        if e.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise
    return {"ok": True, "data": {"id": row.id, "deleted_at": row.deleted_at.isoformat() if row.deleted_at else None}}


@router.post("/experiences")
def create_experience(body: ExperienceCreateIn, user=Depends(get_current_user)):
    try:
        row = talent_write.create_experience(int(user["id"]), body.model_dump())
    except HTTPException as e:
        if e.status_code in (status.HTTP_422_UNPROCESSABLE_ENTITY,):
            return JSONResponse(status_code=422, content={"ok": False, "error": e.detail})
        raise
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"ok": True, "data": ExperienceOut.model_validate(row, from_attributes=True).model_dump()})


@router.patch("/experiences/{experience_id}")
def update_experience(experience_id: int, body: ExperienceUpdateIn, user=Depends(get_current_user)):
    try:
        row = talent_write.update_experience(int(user["id"]), experience_id, body.model_dump(exclude_unset=True))
    except HTTPException as e:
        if e.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN, status.HTTP_422_UNPROCESSABLE_ENTITY):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise
    return {"ok": True, "data": ExperienceOut.model_validate(row, from_attributes=True).model_dump()}


@router.delete("/experiences/{experience_id}")
def delete_experience(experience_id: int, user=Depends(get_current_user)):
    try:
        row = talent_write.delete_experience(int(user["id"]), experience_id)
    except HTTPException as e:
        if e.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise
    return {"ok": True, "data": {"id": row.id, "deleted_at": row.deleted_at.isoformat() if row.deleted_at else None}}


@router.post("/activities")
def create_activity(body: ActivityCreateIn, user=Depends(get_current_user)):
    row = talent_write.create_activity(int(user["id"]), body.model_dump())
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"ok": True, "data": ActivityOut.model_validate(row, from_attributes=True).model_dump()})


@router.patch("/activities/{activity_id}")
def update_activity(activity_id: int, body: ActivityUpdateIn, user=Depends(get_current_user)):
    try:
        row = talent_write.update_activity(int(user["id"]), activity_id, body.model_dump(exclude_unset=True))
    except HTTPException as e:
        if e.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise
    return {"ok": True, "data": ActivityOut.model_validate(row, from_attributes=True).model_dump()}


@router.delete("/activities/{activity_id}")
def delete_activity(activity_id: int, user=Depends(get_current_user)):
    try:
        row = talent_write.delete_activity(int(user["id"]), activity_id)
    except HTTPException as e:
        if e.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise
    return {"ok": True, "data": {"id": row.id, "deleted_at": row.deleted_at.isoformat() if row.deleted_at else None}}


@router.post("/certifications")
def create_certification(body: CertificationCreateIn, user=Depends(get_current_user)):
    row = talent_write.create_certification(int(user["id"]), body.model_dump())
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"ok": True, "data": CertificationOut.model_validate(row, from_attributes=True).model_dump()})


@router.patch("/certifications/{certification_id}")
def update_certification(certification_id: int, body: CertificationUpdateIn, user=Depends(get_current_user)):
    try:
        row = talent_write.update_certification(int(user["id"]), certification_id, body.model_dump(exclude_unset=True))
    except HTTPException as e:
        if e.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise
    return {"ok": True, "data": CertificationOut.model_validate(row, from_attributes=True).model_dump()}


@router.delete("/certifications/{certification_id}")
def delete_certification(certification_id: int, user=Depends(get_current_user)):
    try:
        row = talent_write.delete_certification(int(user["id"]), certification_id)
    except HTTPException as e:
        if e.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise
    return {"ok": True, "data": {"id": row.id, "deleted_at": row.deleted_at.isoformat() if row.deleted_at else None}}


@router.post("/documents")
def create_document(body: DocumentCreateIn, user=Depends(get_current_user)):
    row = talent_write.create_document(int(user["id"]), body.model_dump())
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"ok": True, "data": DocumentOut.model_validate(row, from_attributes=True).model_dump()})


@router.patch("/documents/{document_id}")
def update_document(document_id: int, body: DocumentUpdateIn, user=Depends(get_current_user)):
    try:
        row = talent_write.update_document(int(user["id"]), document_id, body.model_dump(exclude_unset=True))
    except HTTPException as e:
        if e.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise
    return {"ok": True, "data": DocumentOut.model_validate(row, from_attributes=True).model_dump()}


@router.delete("/documents/{document_id}")
def delete_document(document_id: int, user=Depends(get_current_user)):
    try:
        row = talent_write.delete_document(int(user["id"]), document_id)
    except HTTPException as e:
        if e.status_code in (status.HTTP_404_NOT_FOUND, status.HTTP_403_FORBIDDEN):
            return JSONResponse(status_code=e.status_code, content={"ok": False, "error": e.detail})
        raise
    return {"ok": True, "data": {"id": row.id, "deleted_at": row.deleted_at.isoformat() if row.deleted_at else None}}
