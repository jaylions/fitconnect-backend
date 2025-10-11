from __future__ import annotations

from datetime import date, datetime
from typing import Optional, TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, SmallInteger, Text, func
from sqlalchemy.dialects.mysql import JSON as MySQLJSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:  # pragma: no cover
    from app.models.job_posting_card import JobPostingCard


EmploymentTypeEnum = sa.Enum(
    "FULL_TIME",
    "PART_TIME",
    "CONTRACT",
    "INTERN",
    "TEMP",
    "OTHER",
    name="employment_type",
)


JobPostingStatusEnum = sa.Enum(
    "DRAFT",
    "PUBLISHED",
    "CLOSED",
    "ARCHIVED",
    name="job_posting_status",
)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class JobPosting(TimestampMixin, Base):
    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False
    )

    title: Mapped[str] = mapped_column(Text, nullable=False)
    position_group: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    position: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    department: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    employment_type: Mapped[str] = mapped_column(EmploymentTypeEnum, nullable=False)
    location_city: Mapped[str] = mapped_column(Text, nullable=False)
    career_level: Mapped[str] = mapped_column(Text, nullable=False)
    education_level: Mapped[str] = mapped_column(Text, nullable=False)

    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    term_months: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    homepage_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    deadline_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    salary_band: Mapped[Optional[dict]] = mapped_column(MySQLJSON, nullable=True)
    responsibilities: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    requirements_must: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    requirements_nice: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    competencies: Mapped[Optional[list[str]]] = mapped_column(MySQLJSON, nullable=True)

    jd_file_id: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    extra_file_id: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(
        JobPostingStatusEnum, server_default=sa.text("'DRAFT'"), nullable=False
    )
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        sa.Index("ix_job_postings_company_status", "company_id", "status"),
        sa.Index("ix_job_postings_status", "status"),
        sa.Index("ix_job_postings_deadline_date", "deadline_date"),
    )

    card: Mapped[Optional["JobPostingCard"]] = relationship(
        "JobPostingCard",
        back_populates="job_posting",
        uselist=False,
    )

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"JobPosting(id={self.id}, title={self.title!r})"
