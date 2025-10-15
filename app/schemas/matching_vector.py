from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, ConfigDict


class MatchingVectorBase(BaseModel):
    vector_roles: Optional[Dict[str, Any]] = None
    vector_skills: Optional[Dict[str, Any]] = None
    vector_growth: Optional[Dict[str, Any]] = None
    vector_career: Optional[Dict[str, Any]] = None
    vector_vision: Optional[Dict[str, Any]] = None
    vector_culture: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="forbid")


class MatchingVectorCreateIn(MatchingVectorBase):
    role: Literal["talent", "company"]
    job_id: Optional[int] = None


class MatchingVectorUpdateIn(BaseModel):
    vector_roles: Optional[Dict[str, Any]] = None
    vector_skills: Optional[Dict[str, Any]] = None
    vector_growth: Optional[Dict[str, Any]] = None
    vector_career: Optional[Dict[str, Any]] = None
    vector_vision: Optional[Dict[str, Any]] = None
    vector_culture: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(extra="forbid")


class MatchingVectorOut(MatchingVectorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    role: str
    updated_at: datetime
    job_id: Optional[int] = None
