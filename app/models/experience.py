from datetime import date, datetime
from typing import Optional

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Experience(Base):
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)

    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    start_ym: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_ym: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    leave_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    duration_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    @staticmethod
    def calculate_duration_years(start_ym: Optional[date], end_ym: Optional[date]) -> Optional[int]:
        if start_ym is None:
            return None

        effective_end = end_ym or date.today()
        if effective_end < start_ym:
            return 0

        months = (effective_end.year - start_ym.year) * 12 + (effective_end.month - start_ym.month)
        if effective_end.day < start_ym.day:
            months -= 1

        if months < 0:
            months = 0

        return months // 12
