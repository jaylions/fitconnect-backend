from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import JSONType

if TYPE_CHECKING:  # pragma: no cover
    from app.models.user import User
    from app.models.job_posting import JobPosting


class MatchingVector(Base):
    __tablename__ = "matching_vectors"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # 벡터 소유자 역할: talent(인재 벡터), company(기업 벡터)
    role: Mapped[str] = mapped_column(
        Enum("talent", "company", name="matching_vector_role"), nullable=False, index=True
    )
    
    # job_posting_id: company role일 때 필수, talent role일 때 NULL
    # 기업은 채용공고별로 다른 벡터를 가질 수 있음
    job_posting_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=True, index=True
    )

    vector_roles: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONType, nullable=True)
    vector_skills: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONType, nullable=True)
    vector_growth: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONType, nullable=True)
    vector_career: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONType, nullable=True)
    vector_vision: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONType, nullable=True)
    vector_culture: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONType, nullable=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Unique constraint: 
    # - talent: user_id당 1개 (job_posting_id는 NULL)
    # - company: job_posting_id당 1개
    __table_args__ = (
        UniqueConstraint("user_id", "job_posting_id", name="uq_matching_vector_user_jobposting"),
    )

    user: Mapped["User"] = relationship("User", back_populates="matching_vectors")
    job_posting: Mapped[Optional["JobPosting"]] = relationship("JobPosting", back_populates="matching_vectors")

