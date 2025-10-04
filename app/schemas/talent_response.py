from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.talent_read import (
    ActivityOut,
    CertificationOut,
    DocumentOut,
    EducationOut,
    ExperienceOut,
    TalentBasicOut,
)


class _BaseResponse(BaseModel):
    ok: bool = True


class TalentBasicResponse(_BaseResponse):
    data: TalentBasicOut | None = Field(
        default=None,
        json_schema_extra={
            "example": {
                "user_id": 12,
                "name": "홍길동",
                "birth_date": "1998-05-01",
                "phone": "010-1234-5678",
                "tagline": "백엔드 엔지니어",
                "profile_step": 5,
                "is_submitted": True,
                "created_at": "2025-01-12T09:30:00",
                "updated_at": "2025-01-20T14:11:00",
            }
        },
    )


class TalentEducationListResponse(_BaseResponse):
    data: list[EducationOut] = Field(
        default_factory=list,
        json_schema_extra={
            "example": [
                {
                    "id": 1,
                    "user_id": 12,
                    "school_name": "서울대학교",
                    "major": "컴퓨터공학",
                    "status": "졸업",
                    "start_ym": "2017-03-01",
                    "end_ym": "2021-02-01",
                    "created_at": "2025-01-12T09:30:00",
                    "updated_at": "2025-01-12T09:30:00",
                }
            ],
        },
    )


class TalentExperienceListResponse(_BaseResponse):
    data: list[ExperienceOut] = Field(
        default_factory=list,
        json_schema_extra={
            "example": [
                {
                    "id": 4,
                    "user_id": 12,
                    "company_name": "Flex",
                    "title": "Backend Engineer",
                    "start_ym": "2022-01-01",
                    "end_ym": None,
                    "leave_reason": None,
                    "summary": "FitConnect 플랫폼 백엔드 개발",
                    "created_at": "2025-01-18T10:20:00",
                    "updated_at": "2025-01-18T10:20:00",
                }
            ],
        },
    )


class TalentActivityListResponse(_BaseResponse):
    data: list[ActivityOut] = Field(
        default_factory=list,
        json_schema_extra={
            "example": [
                {
                    "id": 2,
                    "user_id": 12,
                    "name": "동아리 해커톤",
                    "category": "대외활동",
                    "period_ym": "2023-09-01",
                    "description": "AI 기반 운동 코칭 서비스 개발",
                    "created_at": "2025-01-18T11:12:00",
                    "updated_at": "2025-01-18T11:12:00",
                }
            ],
        },
    )


class TalentCertificationListResponse(_BaseResponse):
    data: list[CertificationOut] = Field(
        default_factory=list,
        json_schema_extra={
            "example": [
                {
                    "id": 3,
                    "user_id": 12,
                    "name": "정보처리기사",
                    "score_or_grade": "합격",
                    "acquired_ym": "2024-05-01",
                    "created_at": "2025-01-18T11:12:00",
                    "updated_at": "2025-01-18T11:12:00",
                }
            ],
        },
    )


class TalentDocumentListResponse(_BaseResponse):
    data: list[DocumentOut] = Field(
        default_factory=list,
        json_schema_extra={
            "example": [
                {
                    "id": 5,
                    "user_id": 12,
                    "doc_type": "resume",
                    "storage_url": "https://cdn.fitconnect.io/docs/resume_12.pdf",
                    "original_name": "resume.pdf",
                    "mime_type": "application/pdf",
                    "file_size": 204800,
                    "created_at": "2025-01-18T11:12:00",
                    "updated_at": "2025-01-18T11:12:00",
                }
            ],
        },
    )


__all__ = [
    "TalentBasicResponse",
    "TalentEducationListResponse",
    "TalentExperienceListResponse",
    "TalentActivityListResponse",
    "TalentCertificationListResponse",
    "TalentDocumentListResponse",
]

