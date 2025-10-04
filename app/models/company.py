from __future__ import annotations

from datetime import datetime
from typing import Optional

import sqlalchemy as sa

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    SmallInteger,
    Text,
    String,          # ✅ 추가
    JSON,
    text,            # ✅ sa.text 대신 바로 사용
    Enum,
    func            # (size 등을 Enum으로 썼다면 필요)
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


# MySQL-compatible ENUM for company size
CompanySizeEnum = sa.Enum(
    "S_1_10",
    "S_11_50",
    "M_51_200",
    "L_201_500",
    "XL_501_1000",
    "ENT_1000P",
    name="company_size",
)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Company(TimestampMixin, Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    owner_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    name: Mapped[str] = mapped_column(Text, nullable=False)
    industry: Mapped[str] = mapped_column(Text, nullable=False)
    size: Mapped[Optional[str]] = mapped_column(CompanySizeEnum, nullable=True)
    location_city: Mapped[str] = mapped_column(Text, nullable=False)

    homepage_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    career_page_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    one_liner: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    vision_mission: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    business_domains: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ideal_talent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    culture: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    benefits: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    profile_step: Mapped[int] = mapped_column(SmallInteger, server_default=sa.text("0"), nullable=False)
    is_submitted: Mapped[int] = mapped_column(SmallInteger, server_default=sa.text("0"), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, server_default=text("'ACTIVE'"))

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Company(id={self.id}, name={self.name!r})"
