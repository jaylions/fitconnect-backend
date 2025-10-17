from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


EmploymentType = Literal[
    "FULL_TIME",
    "PART_TIME",
    "CONTRACT",
    "INTERN",
    "TEMP",
    "OTHER",
]

LocationType = Literal[
    "SEOUL",
    "GYEONGGI",
    "INCHEON",
    "BUSAN",
    "DAEGU",
    "DAEJEON",
    "GWANGJU",
    "ULSAN",
    "GANGWON",
    "CHUNGBUK",
    "CHUNGNAM",
    "JEONBUK",
    "JEONNAM",
    "GYEONGBUK",
    "GYEONGNAM",
]

SalaryRange = Literal[
    "NEGOTIABLE",
    "RANGE_20_30",
    "RANGE_30_40",
    "RANGE_40_50",
    "RANGE_50_60",
    "RANGE_60_70",
    "RANGE_70_80",
    "RANGE_80_90",
    "RANGE_90_100",
    "RANGE_100_120",
    "RANGE_120_150",
    "OVER_150",
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
    term_months: Optional[int] = None
    homepage_url: Optional[str] = None
    # Aliases for convenience (mapped to start_date/term_months in repo)
    join: Optional[date] = None
    period: Optional[int] = None
    deadline_date: Optional[date] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

    # Details
    salary_band: Optional[dict] = None
    # Optional enum-based salary range (use names like "RANGE_70_80" or "NEGOTIABLE")
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
            "term_months": 12,
            "homepage_url": "https://company.example.com",
            "deadline_date": "2025-10-31",
            "contact_email": "hr@company.example.com",
            "contact_phone": "010-1234-5678",
            "salary_band": {"min": 70000000, "max": 90000000, "currency": "KRW"},
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
    term_months: Optional[int] = None
    homepage_url: Optional[str] = None
    deadline_date: Optional[date] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    salary_band: Optional[dict] = None
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
