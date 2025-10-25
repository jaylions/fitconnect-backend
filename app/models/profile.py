from datetime import date, datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, Date, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TalentProfile(Base):
    __tablename__ = "talent_profiles"

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), primary_key=True
    )
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    tagline: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    profile_step: Mapped[Optional[int]] = mapped_column(
        nullable=True
    )
    is_submitted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # 관심내용 (인재 선호도 설정)
    desired_role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="희망 직무")
    desired_salary: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="희망 연봉")
    desired_industry: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="희망 업종")
    desired_company_size: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="희망 기업 규모")
    residence_location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="주거 지역")
    desired_work_location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="희망 근무 지역")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


    
