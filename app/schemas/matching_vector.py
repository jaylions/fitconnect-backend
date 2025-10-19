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
    job_posting_id: Optional[int] = None  # company일 때 필수


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
    job_posting_id: Optional[int] = None
    updated_at: datetime


class MatchingVectorDetailOut(BaseModel):
    """Vector ID로 조회할 때 사용하는 상세 응답 스키마"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    role: str
    job_posting_id: Optional[int] = None
    reference_type: Optional[str] = None  # "talent" or "job_posting"
    reference_id: Optional[int] = None    # talent_card_id or job_posting_card_id
    vector_roles: Optional[Dict[str, Any]] = None
    vector_skills: Optional[Dict[str, Any]] = None
    vector_growth: Optional[Dict[str, Any]] = None
    vector_career: Optional[Dict[str, Any]] = None
    vector_vision: Optional[Dict[str, Any]] = None
    vector_culture: Optional[Dict[str, Any]] = None
    updated_at: datetime
