from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, HttpUrl, field_validator


def _parse_ym_or_date(v: Optional[str | date]) -> Optional[date]:
    if v is None:
        return None
    if isinstance(v, date):
        return v
    if isinstance(v, str):
        s = v.strip()
        if len(s) == 7 and s[4] == "-":  # YYYY-MM
            s = f"{s}-01"
        try:
            return date.fromisoformat(s)
        except ValueError:
            raise ValueError("Invalid date format; expected YYYY-MM or YYYY-MM-DD")
    return v  # let pydantic handle unexpected types


class BasicProfile(BaseModel):
    name: str
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    tagline: Optional[str] = None
    is_submitted: Optional[bool] = None

    @field_validator("birth_date", mode="before")
    @classmethod
    def _coerce_birth_date(cls, v):
        return _parse_ym_or_date(v)


class EducationIn(BaseModel):
    school_name: str
    major: Optional[str] = None
    status: Literal["재학", "휴학", "졸업 예정", "졸업 유예", "졸업", "중퇴"]
    start_ym: Optional[date] = None
    end_ym: Optional[date] = None

    @field_validator("start_ym", "end_ym", mode="before")
    @classmethod
    def _coerce_dates(cls, v):
        return _parse_ym_or_date(v)


class ExperienceIn(BaseModel):
    company_name: str
    title: Optional[str] = None
    start_ym: Optional[date] = None
    end_ym: Optional[date] = None
    leave_reason: Optional[str] = None
    summary: Optional[str] = None

    @field_validator("start_ym", "end_ym", mode="before")
    @classmethod
    def _coerce_dates(cls, v):
        return _parse_ym_or_date(v)


class ActivityIn(BaseModel):
    name: str
    category: Optional[str] = None
    period_ym: Optional[date] = None
    description: Optional[str] = None

    @field_validator("period_ym", mode="before")
    @classmethod
    def _coerce_period(cls, v):
        return _parse_ym_or_date(v)


class CertificationIn(BaseModel):
    name: str
    score_or_grade: Optional[str] = None
    acquired_ym: Optional[date] = None

    @field_validator("acquired_ym", mode="before")
    @classmethod
    def _coerce_acquired(cls, v):
        return _parse_ym_or_date(v)


class DocumentIn(BaseModel):
    doc_type: Literal["resume", "cover_letter", "portfolio"]
    storage_url: HttpUrl
    original_name: str
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class FullProfileIn(BaseModel):
    basic: BasicProfile
    educations: list[EducationIn] = []
    experiences: list[ExperienceIn] = []
    activities: list[ActivityIn] = []
    certifications: list[CertificationIn] = []
    documents: list[DocumentIn] = []
    submit: Optional[bool] = None


class FullProfileOut(BaseModel):
    user_id: int
    profile_step: int
    is_submitted: int
