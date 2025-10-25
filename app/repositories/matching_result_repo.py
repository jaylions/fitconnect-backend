from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.matching_result import MatchingResult


def upsert_result(
    db: Session,
    talent_vector_id: int,
    company_vector_id: int,
    talent_user_id: int,
    company_user_id: int,
    job_posting_id: int,
    total_score: float,
    field_scores: dict,
) -> MatchingResult:
    """
    매칭 결과 저장 (이미 존재하면 UPDATE, 없으면 INSERT)
    
    Args:
        db: DB 세션
        talent_vector_id: 인재 벡터 ID
        company_vector_id: 기업 벡터 ID
        talent_user_id: 인재 user_id
        company_user_id: 기업 user_id
        job_posting_id: 공고 ID
        total_score: 종합 점수
        field_scores: 필드별 점수 dict
    
    Returns:
        MatchingResult 객체
    """
    # 1. 기존 결과 조회
    existing = db.query(MatchingResult).filter(
        MatchingResult.talent_vector_id == talent_vector_id,
        MatchingResult.company_vector_id == company_vector_id,
    ).first()
    
    if existing:
        # UPDATE
        existing.total_score = total_score
        existing.score_roles = field_scores.get("vector_roles")
        existing.score_skills = field_scores.get("vector_skills")
        existing.score_growth = field_scores.get("vector_growth")
        existing.score_career = field_scores.get("vector_career")
        existing.score_vision = field_scores.get("vector_vision")
        existing.score_culture = field_scores.get("vector_culture")
        existing.calculated_at = func.now()
        db.flush()
        db.refresh(existing)
        return existing
    else:
        # INSERT
        new_result = MatchingResult(
            talent_vector_id=talent_vector_id,
            company_vector_id=company_vector_id,
            talent_user_id=talent_user_id,
            company_user_id=company_user_id,
            job_posting_id=job_posting_id,
            total_score=total_score,
            score_roles=field_scores.get("vector_roles"),
            score_skills=field_scores.get("vector_skills"),
            score_growth=field_scores.get("vector_growth"),
            score_career=field_scores.get("vector_career"),
            score_vision=field_scores.get("vector_vision"),
            score_culture=field_scores.get("vector_culture"),
        )
        db.add(new_result)
        db.flush()
        db.refresh(new_result)
        return new_result


def get_matches_for_talent(
    db: Session,
    talent_user_id: int,
    min_score: float = 0.0,
    limit: int = 100,
) -> List[MatchingResult]:
    """
    특정 인재와 매칭된 공고 목록 조회 (점수 내림차순)
    
    Args:
        db: DB 세션
        talent_user_id: 인재 user_id
        min_score: 최소 점수 필터
        limit: 최대 반환 개수
    
    Returns:
        MatchingResult 리스트
    """
    stmt = (
        select(MatchingResult)
        .filter(
            MatchingResult.talent_user_id == talent_user_id,
            MatchingResult.total_score >= min_score,
        )
        .order_by(MatchingResult.total_score.desc())
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().all())


def get_matches_for_job_posting(
    db: Session,
    job_posting_id: int,
    min_score: float = 0.0,
    limit: int = 100,
) -> List[MatchingResult]:
    """
    특정 공고와 매칭된 인재 목록 조회 (점수 내림차순)
    
    Args:
        db: DB 세션
        job_posting_id: 공고 ID
        min_score: 최소 점수 필터
        limit: 최대 반환 개수
    
    Returns:
        MatchingResult 리스트
    """
    stmt = (
        select(MatchingResult)
        .filter(
            MatchingResult.job_posting_id == job_posting_id,
            MatchingResult.total_score >= min_score,
        )
        .order_by(MatchingResult.total_score.desc())
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().all())


def get_matches_for_company(
    db: Session,
    company_user_id: int,
    min_score: float = 0.0,
    limit: int = 100,
) -> List[MatchingResult]:
    """
    특정 기업의 모든 공고와 매칭된 인재 목록 조회 (점수 내림차순)
    
    Args:
        db: DB 세션
        company_user_id: 기업 user_id
        min_score: 최소 점수 필터
        limit: 최대 반환 개수
    
    Returns:
        MatchingResult 리스트
    """
    stmt = (
        select(MatchingResult)
        .filter(
            MatchingResult.company_user_id == company_user_id,
            MatchingResult.total_score >= min_score,
        )
        .order_by(MatchingResult.total_score.desc())
        .limit(limit)
    )
    return list(db.execute(stmt).scalars().all())


def delete_by_vector_id(db: Session, vector_id: int) -> None:
    """
    특정 벡터와 관련된 모든 매칭 결과 삭제
    
    Args:
        db: DB 세션
        vector_id: 벡터 ID
    """
    db.query(MatchingResult).filter(
        (MatchingResult.talent_vector_id == vector_id) |
        (MatchingResult.company_vector_id == vector_id)
    ).delete(synchronize_session=False)
    db.flush()


def count_matches_for_talent(db: Session, talent_user_id: int) -> int:
    """
    특정 인재의 매칭 결과 개수 조회
    
    Args:
        db: DB 세션
        talent_user_id: 인재 user_id
    
    Returns:
        매칭 결과 개수
    """
    return db.query(func.count(MatchingResult.id)).filter(
        MatchingResult.talent_user_id == talent_user_id
    ).scalar() or 0


def count_matches_for_job_posting(db: Session, job_posting_id: int) -> int:
    """
    특정 공고의 매칭 결과 개수 조회
    
    Args:
        db: DB 세션
        job_posting_id: 공고 ID
    
    Returns:
        매칭 결과 개수
    """
    return db.query(func.count(MatchingResult.id)).filter(
        MatchingResult.job_posting_id == job_posting_id
    ).scalar() or 0
