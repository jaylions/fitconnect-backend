from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CompanyBasicIn(BaseModel):
    name: str = Field(min_length=1)
    industry: str = Field(min_length=1)
    size: Optional[str] = None  # 예: 1 ~ 10명, 10 ~ 50명, 50 ~ 100명, 100 ~ 200명, 200 ~ 500명, 500 ~ 1000명, 1000명 이상
    location_city: str = Field(min_length=1)
    homepage_url: Optional[str] = None
    career_page_url: Optional[str] = None
    one_liner: Optional[str] = Field(default=None, max_length=120)


class CompanyAboutIn(BaseModel):
    vision_mission: Optional[str] = None
    business_domains: Optional[str] = None
    ideal_talent: Optional[str] = None
    culture: Optional[str] = None
    benefits: Optional[str] = None


class CompanyFullIn(BaseModel):
    basic: CompanyBasicIn
    about: CompanyAboutIn
    submit: Optional[bool] = None

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "basic": {
                "name": "FitConnect",
                "industry": "Software",
                "size": "50 ~ 100명",
                "location_city": "Seoul",
                "homepage_url": "https://fitconnect.io",
                "career_page_url": "https://fitconnect.io/careers",
                "one_liner": "We connect talent and companies.",
            },
            "about": {
                "vision_mission": "Empower hiring with data.",
                "business_domains": "Recruiting, HR Tech",
                "ideal_talent": "Ownership, bias to action",
                "culture": "Remote-friendly, async-first",
                "benefits": "Flexible hours, learning budget",
            },
            "submit": True,
        }
    })


class CompanyBasicOut(BaseModel):
    name: str
    industry: str
    size: Optional[str] = None
    location_city: str
    homepage_url: Optional[str] = None
    career_page_url: Optional[str] = None
    one_liner: Optional[str] = None


class CompanyAboutOut(BaseModel):
    vision_mission: Optional[str] = None
    business_domains: Optional[str] = None
    ideal_talent: Optional[str] = None
    culture: Optional[str] = None
    benefits: Optional[str] = None


class CompanyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    company_id: int = Field(alias="id")
    basic: CompanyBasicOut
    about: CompanyAboutOut
    profile_step: int
    is_submitted: int
    status: str
    created_at: str
    updated_at: str
