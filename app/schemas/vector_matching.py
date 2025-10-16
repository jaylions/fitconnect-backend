from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, ConfigDict


class VectorMatchRequest(BaseModel):
    source_id: int
    target_id: int

    model_config = ConfigDict(extra="forbid")


class MatchParticipant(BaseModel):
    id: int
    user_id: int
    role: str


class VectorMatchResult(BaseModel):
    source: MatchParticipant
    target: MatchParticipant
    field_scores: Dict[str, float]
    total_similarity: float
    score: float

    model_config = ConfigDict(extra="forbid")
