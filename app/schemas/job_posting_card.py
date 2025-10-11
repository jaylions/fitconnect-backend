from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class JobPostingCardBase(BaseModel):
    header_title: Optional[str] = Field(default=None, max_length=100)
    badge_role: Optional[str] = Field(default=None, max_length=100)
    deadline_date: Optional[date] = None
    headline: Optional[str] = Field(default=None, max_length=255)

    posting_info: Optional[Dict[str, Any]] = None
    responsibilities: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
    required_competencies: Optional[List[str]] = None

    company_info: Optional[str] = None
    talent_persona: Optional[str] = None
    challenge_task: Optional[str] = None

    @field_validator(
        "posting_info",
        "responsibilities",
        "requirements",
        "required_competencies",
        mode="before",
    )
    @classmethod
    def parse_json_field(cls, value: Any) -> Any:
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return None
        return value


class JobPostingCardCreate(JobPostingCardBase):
    job_posting_id: int = Field(gt=0)


class JobPostingCardResponse(JobPostingCardBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_posting_id: int
    created_at: datetime
    updated_at: datetime

