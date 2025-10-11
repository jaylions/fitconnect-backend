from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import JSONType

if TYPE_CHECKING:  # pragma: no cover
    from app.models.user import User


class TalentCard(Base):
    __tablename__ = "talent_cards"
    __table_args__ = (UniqueConstraint("user_id", name="uq_talent_cards_user_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    header_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    badge_title: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    badge_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    badge_employment: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    headline: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    experiences: Mapped[Optional[list[str]]] = mapped_column(JSONType, nullable=True)
    strengths: Mapped[Optional[list[str]]] = mapped_column(JSONType, nullable=True)
    general_capabilities: Mapped[Optional[list[dict[str, str]]]] = mapped_column(JSONType, nullable=True)
    job_skills: Mapped[Optional[list[dict[str, str]]]] = mapped_column(JSONType, nullable=True)

    performance_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    collaboration_style: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    growth_potential: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="talent_card")
