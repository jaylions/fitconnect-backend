from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class _OrmBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TalentBasicOut(_OrmBase):
    user_id: int
    name: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    tagline: Optional[str] = None
    profile_step: Optional[int] = None
    is_submitted: bool
    
    # 관심내용 (인재 선호도 설정)
    desired_role: Optional[str] = None  # 희망 직무
    desired_salary: Optional[str] = None  # 희망 연봉
    desired_industry: Optional[str] = None  # 희망 업종
    desired_company_size: Optional[str] = None  # 희망 기업 규모
    residence_location: Optional[str] = None  # 주거 지역
    desired_work_location: Optional[str] = None  # 희망 근무 지역
    
    created_at: datetime
    updated_at: datetime


class EducationOut(_OrmBase):
    id: int
    user_id: int
    school_name: str
    major: Optional[str] = None
    status: str
    start_ym: Optional[date] = None
    end_ym: Optional[date] = None
    created_at: datetime
    updated_at: datetime


class ExperienceOut(_OrmBase):
    id: int
    user_id: int
    company_name: str
    title: Optional[str] = None
    start_ym: Optional[date] = None
    end_ym: Optional[date] = None
    duration_years: Optional[int] = None
    leave_reason: Optional[str] = None
    summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ActivityOut(_OrmBase):
    id: int
    user_id: int
    name: str
    category: Optional[str] = None
    period_ym: Optional[date] = None
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class CertificationOut(_OrmBase):
    id: int
    user_id: int
    name: str
    score_or_grade: Optional[str] = None
    acquired_ym: Optional[date] = None
    created_at: datetime
    updated_at: datetime


class DocumentOut(_OrmBase):
    id: int
    user_id: int
    doc_type: str
    storage_url: str
    original_name: str
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    created_at: datetime
    updated_at: datetime
