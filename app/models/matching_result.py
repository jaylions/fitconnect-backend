from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DECIMAL, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:  # pragma: no cover
    from app.models.user import User
    from app.models.job_posting import JobPosting
    from app.models.matching_vector import MatchingVector


class MatchingResult(Base):
    """
    매칭 벡터 계산 결과 저장 테이블
    - 벡터 생성/수정 시 자동으로 반대편 role과 매칭 계산하여 저장
    - UNIQUE (talent_vector_id, company_vector_id)로 중복 방지
    """
    __tablename__ = "matching_results"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    
    # 벡터 ID (핵심)
    talent_vector_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("matching_vectors.id", ondelete="CASCADE"), nullable=False, index=True
    )
    company_vector_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("matching_vectors.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # 편의성 컬럼 (조회 최적화)
    talent_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    company_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_posting_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # 매칭 점수 (DECIMAL(5,2): 0.00 ~ 999.99, 실제 0~100 범위)
    total_score: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    score_roles: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=True)
    score_skills: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=True)
    score_growth: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=True)
    score_career: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=True)
    score_vision: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=True)
    score_culture: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=True)
    
    # 메타 정보
    calculated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    
    # Unique 제약 (동일 벡터 조합 중복 방지)
    __table_args__ = (
        UniqueConstraint("talent_vector_id", "company_vector_id", name="uq_matching_pair"),
    )
    
    # Relationships (optional, for ORM convenience)
    talent_user: Mapped["User"] = relationship("User", foreign_keys=[talent_user_id])
    company_user: Mapped["User"] = relationship("User", foreign_keys=[company_user_id])
    job_posting: Mapped["JobPosting"] = relationship("JobPosting", foreign_keys=[job_posting_id])

    def __repr__(self) -> str:  # pragma: no cover
        return f"MatchingResult(id={self.id}, talent={self.talent_user_id}, job_posting={self.job_posting_id}, score={self.total_score})"
