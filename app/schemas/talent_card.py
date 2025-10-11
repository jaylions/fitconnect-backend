from __future__ import annotations

import json
from datetime import datetime
from typing import Any, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CapabilityItem(BaseModel):
    name: str = Field(min_length=1)
    level: Literal["low", "medium", "high"]


class TalentCardBase(BaseModel):
    header_title: Optional[str] = Field(default=None, max_length=100)
    badge_title: Optional[str] = Field(default=None, max_length=120)
    badge_years: Optional[int] = Field(default=None, ge=0)
    badge_employment: Optional[str] = Field(default=None, max_length=120)
    headline: Optional[str] = Field(default=None, max_length=255)

    experiences: Optional[List[str]] = None
    strengths: Optional[List[str]] = None
    general_capabilities: Optional[List[CapabilityItem]] = None
    job_skills: Optional[List[CapabilityItem]] = None

    performance_summary: Optional[str] = None
    collaboration_style: Optional[str] = None
    growth_potential: Optional[str] = None

    @field_validator(
        "experiences",
        "strengths",
        "general_capabilities",
        "job_skills",
        mode="before",
    )
    @classmethod
    def parse_json_array(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                loaded = json.loads(value)
            except json.JSONDecodeError:
                return None
            return loaded
        return value


class TalentCardCreate(TalentCardBase):
    user_id: int = Field(gt=0)


class TalentCardResponse(TalentCardBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

