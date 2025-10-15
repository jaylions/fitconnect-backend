from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.types import JSONType


class TalentEmbedding(Base):
    __tablename__ = "talent_embeddings"

    talent_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("talent_profiles.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    model: Mapped[str] = mapped_column(String(64), nullable=False)
    dim: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    vector_roles: Mapped[Optional[dict[str, list[float]]]] = mapped_column(JSONType, nullable=True)
    vector_skills: Mapped[Optional[dict[str, list[float]]]] = mapped_column(JSONType, nullable=True)
    vector_growth: Mapped[Optional[dict[str, list[float]]]] = mapped_column(JSONType, nullable=True)
    vector_career: Mapped[Optional[dict[str, list[float]]]] = mapped_column(JSONType, nullable=True)
    vector_vision: Mapped[Optional[dict[str, list[float]]]] = mapped_column(JSONType, nullable=True)
    vector_culture: Mapped[Optional[dict[str, list[float]]]] = mapped_column(JSONType, nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

class JobEmbedding(Base):
    __tablename__ = "job_embeddings"

    job_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("job_postings.id", ondelete="CASCADE"),
        primary_key=True,
    )
    model: Mapped[str] = mapped_column(String(64), nullable=False)
    dim: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    vector_roles: Mapped[Optional[dict[str, list[float]]]] = mapped_column(JSONType, nullable=True)
    vector_skills: Mapped[Optional[dict[str, list[float]]]] = mapped_column(JSONType, nullable=True)
    vector_growth: Mapped[Optional[dict[str, list[float]]]] = mapped_column(JSONType, nullable=True)
    vector_career: Mapped[Optional[dict[str, list[float]]]] = mapped_column(JSONType, nullable=True)
    vector_vision: Mapped[Optional[dict[str, list[float]]]] = mapped_column(JSONType, nullable=True)
    vector_culture: Mapped[Optional[dict[str, list[float]]]] = mapped_column(JSONType, nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

__all__ = ["TalentEmbedding", "JobEmbedding"]
