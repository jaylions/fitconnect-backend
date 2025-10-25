from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.repositories import matching_result_repo

router = APIRouter(prefix="/api/matching-results", tags=["matching_results"])


@router.get("/talents/{user_id}/job-postings")
def get_talent_matches(
    user_id: int,
    min_score: float = Query(0.0, ge=0.0, le=100.0, description="최소 점수 필터 (0~100)"),
    limit: int = Query(100, ge=1, le=500, description="최대 반환 개수"),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    특정 인재와 매칭된 공고 목록 조회 (점수 내림차순)
    
    - **user_id**: 인재 user_id
    - **min_score**: 최소 점수 필터 (0~100, 기본값: 0)
    - **limit**: 최대 반환 개수 (기본 100, 최대 500)
    
    Returns:
    - 공고 ID + 매칭 점수 목록 (점수 높은 순)
    """
    matches = matching_result_repo.get_matches_for_talent(
        db, talent_user_id=user_id, min_score=min_score, limit=limit
    )
    
    results = []
    for match in matches:
        results.append({
            "job_posting_id": match.job_posting_id,
            "company_user_id": match.company_user_id,
            "total_score": float(match.total_score),
            "scores": {
                "roles": float(match.score_roles) if match.score_roles else None,
                "skills": float(match.score_skills) if match.score_skills else None,
                "growth": float(match.score_growth) if match.score_growth else None,
                "career": float(match.score_career) if match.score_career else None,
                "vision": float(match.score_vision) if match.score_vision else None,
                "culture": float(match.score_culture) if match.score_culture else None,
            },
            "calculated_at": match.calculated_at.isoformat(),
        })
    
    return {
        "ok": True,
        "data": {
            "talent_user_id": user_id,
            "total_matches": len(results),
            "matches": results,
        }
    }


@router.get("/job-postings/{job_posting_id}/talents")
def get_job_posting_matches(
    job_posting_id: int,
    min_score: float = Query(0.0, ge=0.0, le=100.0, description="최소 점수 필터 (0~100)"),
    limit: int = Query(100, ge=1, le=500, description="최대 반환 개수"),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    특정 공고와 매칭된 인재 목록 조회 (점수 내림차순)
    
    - **job_posting_id**: 공고 ID
    - **min_score**: 최소 점수 필터 (0~100, 기본값: 0)
    - **limit**: 최대 반환 개수 (기본 100, 최대 500)
    
    Returns:
    - 인재 ID + 매칭 점수 목록 (점수 높은 순)
    """
    matches = matching_result_repo.get_matches_for_job_posting(
        db, job_posting_id=job_posting_id, min_score=min_score, limit=limit
    )
    
    results = []
    for match in matches:
        results.append({
            "talent_user_id": match.talent_user_id,
            "total_score": float(match.total_score),
            "scores": {
                "roles": float(match.score_roles) if match.score_roles else None,
                "skills": float(match.score_skills) if match.score_skills else None,
                "growth": float(match.score_growth) if match.score_growth else None,
                "career": float(match.score_career) if match.score_career else None,
                "vision": float(match.score_vision) if match.score_vision else None,
                "culture": float(match.score_culture) if match.score_culture else None,
            },
            "calculated_at": match.calculated_at.isoformat(),
        })
    
    return {
        "ok": True,
        "data": {
            "job_posting_id": job_posting_id,
            "total_matches": len(results),
            "matches": results,
        }
    }


@router.get("/companies/{company_user_id}/talents")
def get_company_matches(
    company_user_id: int,
    min_score: float = Query(0.0, ge=0.0, le=100.0, description="최소 점수 필터 (0~100)"),
    limit: int = Query(100, ge=1, le=500, description="최대 반환 개수"),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    특정 기업의 모든 공고와 매칭된 인재 목록 조회 (점수 내림차순)
    
    - **company_user_id**: 기업 user_id
    - **min_score**: 최소 점수 필터 (0~100, 기본값: 0)
    - **limit**: 최대 반환 개수 (기본 100, 최대 500)
    
    Returns:
    - 인재 ID + 공고 ID + 매칭 점수 목록 (점수 높은 순)
    """
    matches = matching_result_repo.get_matches_for_company(
        db, company_user_id=company_user_id, min_score=min_score, limit=limit
    )
    
    results = []
    for match in matches:
        results.append({
            "talent_user_id": match.talent_user_id,
            "job_posting_id": match.job_posting_id,
            "total_score": float(match.total_score),
            "scores": {
                "roles": float(match.score_roles) if match.score_roles else None,
                "skills": float(match.score_skills) if match.score_skills else None,
                "growth": float(match.score_growth) if match.score_growth else None,
                "career": float(match.score_career) if match.score_career else None,
                "vision": float(match.score_vision) if match.score_vision else None,
                "culture": float(match.score_culture) if match.score_culture else None,
            },
            "calculated_at": match.calculated_at.isoformat(),
        })
    
    return {
        "ok": True,
        "data": {
            "company_user_id": company_user_id,
            "total_matches": len(results),
            "matches": results,
        }
    }
