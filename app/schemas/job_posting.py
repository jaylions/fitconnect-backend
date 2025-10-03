from __future__ import annotations

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


EmploymentType = Literal[
    "FULL_TIME",
    "PART_TIME",
    "CONTRACT",
    "INTERN",
    "TEMP",
    "OTHER",
]

PostingStatus = Literal["DRAFT", "PUBLISHED", "CLOSED", "ARCHIVED"]


class JobPostingCreateIn(BaseModel):
    # Required
    title: str = Field(min_length=1)
    employment_type: EmploymentType
    location_city: str = Field(min_length=1)
    career_level: str = Field(min_length=1)
    education_level: str = Field(min_length=1)

    # Optional basics
    position_group: Optional[str] = None
    department: Optional[str] = None
    start_date: Optional[date] = None
    term_months: Optional[int] = None
    homepage_url: Optional[HttpUrl] = None
    deadline_date: Optional[date] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None

    # Details
    salary_band: Optional[dict] = None
    responsibilities: Optional[str] = None
    requirements_must: Optional[str] = None
    requirements_nice: Optional[str] = None
    competencies: Optional[list[str]] = None

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
            "deadline_date": "2025-10-31",
            "salary_band": {"min": 70000000, "max": 90000000, "currency": "KRW"},
            "competencies": ["Python", "FastAPI", "MySQL"],
            "status": "DRAFT",
        }
    })


class JobPostingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    title: str
    employment_type: str
    location_city: str
    career_level: str
    education_level: str
    status: str
    deadline_date: Optional[date] = None
    created_at: str
    updated_at: str

