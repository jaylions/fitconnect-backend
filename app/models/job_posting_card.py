from __future__ import annotations

from datetime import date, datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import JSONType

if TYPE_CHECKING:  # pragma: no cover
    from app.models.job_posting import JobPosting


class JobPostingCard(Base):
    __tablename__ = "job_posting_cards"
    __table_args__ = (UniqueConstraint("job_posting_id", name="uq_job_posting_cards_job_posting_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_posting_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    header_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    badge_role: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    deadline_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    headline: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    posting_info: Mapped[Optional[dict]] = mapped_column(JSONType, nullable=True)
    responsibilities: Mapped[Optional[list[str]]] = mapped_column(JSONType, nullable=True)
    requirements: Mapped[Optional[list[str]]] = mapped_column(JSONType, nullable=True)
    required_competencies: Mapped[Optional[list[str]]] = mapped_column(JSONType, nullable=True)

    company_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    talent_persona: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    challenge_task: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    job_posting: Mapped["JobPosting"] = relationship("JobPosting", back_populates="card")
