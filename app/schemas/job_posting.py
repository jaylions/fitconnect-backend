from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


EmploymentType = Literal[
    "정규직",
    "계약직",
    "파견직",
    "인턴",
    "임시직",
    "기타",
]

LocationType = Literal[
    "서울",
    "경기",
    "인천",
    "부산",
    "대구",
    "대전",
    "광주",
    "울산",
    "강원",
    "충북",
    "충남",
    "전북",
    "전남",
    "경북",
    "경남",
]

SalaryRange = Literal[
    "연봉 추후 협상",
    "2000만 ~ 3000만",
    "3000만 ~ 4000만",
    "4000만 ~ 5000만",
    "5000만 ~ 6000만",
    "6000만 ~ 7000만",
    "7000만 ~ 8000만",
    "8000만 ~ 9000만",
    "9000만 ~ 1억",
    "1억 ~ 1.2억",
    "1.2억 ~ 1.5억",
    "1.5억 이상",
]

PostingStatus = Literal["DRAFT", "PUBLISHED", "CLOSED", "ARCHIVED"]


class JobPostingCreateIn(BaseModel):
    # Required
    title: str = Field(min_length=1)
    employment_type: EmploymentType
    # Use enum names for location (e.g., "SEOUL", "GYEONGGI")
    location_city: LocationType
    career_level: str = Field(min_length=1)
    education_level: str = Field(min_length=1)

    # Optional basics
    position_group: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    start_date: Optional[date] = None
    term_months: Optional[str] = None
    homepage_url: Optional[str] = None
    # Aliases for convenience (mapped to start_date/term_months in repo)
    join: Optional[date] = None
    period: Optional[str] = None
    deadline_date: Optional[date] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

    # Details
    # Enum-based salary range
    salary_range: Optional[SalaryRange] = None
    responsibilities: Optional[str] = None
    requirements_must: Optional[str] = None
    requirements_nice: Optional[str] = None
    competencies: Optional[str] = None

    # Files
    jd_file_id: Optional[str] = None
    extra_file_id: Optional[str] = None

    # Status (defaults to DRAFT if omitted)
    status: Optional[PostingStatus] = None

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "title": "Backend Engineer",
            "employment_type": "FULL_TIME",
            "location_city": "Seoul",
            "career_level": "Senior",
            "education_level": "Bachelor",
            "position_group": "Engineering",
            "position": "Backend",
            "department": "Platform",
            "start_date": "2025-11-15",
            "term_months": "12개월",
            "homepage_url": "https://company.example.com",
            "deadline_date": "2025-10-31",
            "contact_email": "hr@company.example.com",
            "contact_phone": "010-1234-5678",
            "salary_range": "7000만 ~ 8000만",
            "responsibilities": "- 서비스 API 개발 및 운영\n- 성능 최적화",
            "requirements_must": "- Python, FastAPI 실무 경험\n- RDBMS 설계 경험",
            "requirements_nice": "- AWS, Docker 경험",
            "competencies": "Python, FastAPI, MySQL",
            "jd_file_id": "file_abc123",
            "extra_file_id": "file_xyz789",
            "status": "DRAFT"
        }
    })


class JobPostingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    title: str
    position_group: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    employment_type: str
    location_city: str
    salary_range: Optional[str] = None
    career_level: str
    education_level: str
    start_date: Optional[date] = None
    term_months: Optional[str] = None
    homepage_url: Optional[str] = None
    deadline_date: Optional[date] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    responsibilities: Optional[str] = None
    requirements_must: Optional[str] = None
    requirements_nice: Optional[str] = None
    competencies: Optional[str] = None
    status: str
    jd_file_id: Optional[str] = None
    extra_file_id: Optional[str] = None
    published_at: Optional[str] = None
    closed_at: Optional[str] = None
    deleted_at: Optional[str] = None
    created_at: str
    updated_at: str
