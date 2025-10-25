from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import matching_vector_repo

logger = logging.getLogger(__name__)

ALLOWED_ROLES = {"talent", "company"}
VECTOR_FIELDS = (
    "vector_roles",
    "vector_skills",
    "vector_growth",
    "vector_career",
    "vector_vision",
    "vector_culture",
)


def _error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})


def _require_owned(db_row, user_id: int):
    if db_row is None:
        raise _error(status.HTTP_404_NOT_FOUND, "MATCHING_VECTOR_NOT_FOUND", "Matching vector not found")
    if int(db_row.user_id) != int(user_id):
        raise _error(status.HTTP_403_FORBIDDEN, "FORBIDDEN", "Not your matching vector")
    return db_row


def _filter_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    return {field: data[field] for field in VECTOR_FIELDS if field in data}


def create(db: Session, user_id: int, role: str, payload: Dict[str, Any]):
    if role not in ALLOWED_ROLES:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "INVALID_ROLE", "role must be 'talent' or 'company'")

    job_posting_id = payload.get("job_posting_id")
    
    # Validation: company role must provide job_posting_id
    if role == "company":
        if not job_posting_id:
            raise _error(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "JOB_POSTING_ID_REQUIRED",
                "job_posting_id is required for company role",
            )
        # Check if job_posting exists and belongs to the user
        from app.models.job_posting import JobPosting
        from app.models.company import Company
        job_posting = db.query(JobPosting).filter(JobPosting.id == job_posting_id).first()
        if not job_posting:
            raise _error(status.HTTP_404_NOT_FOUND, "JOB_POSTING_NOT_FOUND", "Job posting not found")
        
        company = db.query(Company).filter(Company.id == job_posting.company_id, Company.owner_user_id == user_id).first()
        if not company:
            raise _error(status.HTTP_403_FORBIDDEN, "FORBIDDEN", "Job posting does not belong to you")
    
    # Validation: talent role must NOT provide job_posting_id
    if role == "talent" and job_posting_id:
        raise _error(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "JOB_POSTING_ID_NOT_ALLOWED",
            "job_posting_id is not allowed for talent role",
        )

    # Check for existing vector
    existing = matching_vector_repo.get_by_user_and_job_posting(
        db, user_id=user_id, job_posting_id=job_posting_id
    )
    if existing is not None:
        if role == "talent":
            raise _error(
                status.HTTP_409_CONFLICT,
                "MATCHING_VECTOR_EXISTS",
                "Matching vector already exists for this talent",
            )
        else:
            raise _error(
                status.HTTP_409_CONFLICT,
                "MATCHING_VECTOR_EXISTS",
                f"Matching vector already exists for job posting {job_posting_id}",
            )

    # Ensure payload uses only allowed fields
    filtered = _filter_payload(payload)
    row = matching_vector_repo.create(
        db, user_id=user_id, role=role, job_posting_id=job_posting_id, payload=filtered
    )
    
    # ✅ 벡터 생성 후 자동 매칭 계산
    try:
        if role == "talent":
            _calculate_all_matches_for_talent(db, row)
        elif role == "company":
            _calculate_all_matches_for_company(db, row)
    except Exception as e:
        logger.error(f"Auto-matching failed for vector {row.id}: {e}")
        # 매칭 실패해도 벡터 생성은 성공으로 처리
    
    return row


def update(db: Session, user_id: int, matching_vector_id: int, payload: Dict[str, Any]):
    row = matching_vector_repo.get_by_id(db, matching_vector_id)
    row = _require_owned(row, user_id)

    filtered = _filter_payload(payload)
    if not filtered:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "NO_FIELDS_TO_UPDATE", "Provide at least one field to update")

    result = matching_vector_repo.update(db, row=row, payload=filtered)
    
    # ✅ 벡터 수정 후 자동 재매칭 계산
    try:
        if result.role == "talent":
            _calculate_all_matches_for_talent(db, result)
        elif result.role == "company":
            _calculate_all_matches_for_company(db, result)
    except Exception as e:
        logger.error(f"Auto-matching failed for vector {result.id}: {e}")
        # 매칭 실패해도 벡터 수정은 성공으로 처리
    
    return result


def delete(db: Session, user_id: int, matching_vector_id: int):
    row = matching_vector_repo.get_by_id(db, matching_vector_id)
    row = _require_owned(row, user_id)
    matching_vector_repo.delete(db, row=row)
    return row


def get_all_by_user(db: Session, user_id: int) -> list:
    """
    현재 사용자의 모든 매칭 벡터 조회 (최신순)
    - talent: 최대 1개
    - company: 여러 개 (job_posting별)
    """
    return matching_vector_repo.get_all_by_user(db, user_id)


def get_vector_detail_by_id(db: Session, vector_id: int) -> Dict[str, Any]:
    """
    Vector ID로 벡터 상세 정보 조회 (인증 불필요)
    - role 반환
    - job_posting_id 반환 (company인 경우)
    - talent_card_id 또는 job_posting_card_id 조회하여 어떤 참조인지 반환
    - 모든 vector 값 반환
    """
    from app.models.talent_card import TalentCard
    from app.models.job_posting_card import JobPostingCard

    row = matching_vector_repo.get_by_id(db, vector_id)
    if row is None:
        raise _error(status.HTTP_404_NOT_FOUND, "MATCHING_VECTOR_NOT_FOUND", "Matching vector not found")

    result = {
        "id": row.id,
        "user_id": row.user_id,
        "role": row.role,
        "job_posting_id": row.job_posting_id,
        "reference_type": None,
        "reference_id": None,
        "vector_roles": row.vector_roles,
        "vector_skills": row.vector_skills,
        "vector_growth": row.vector_growth,
        "vector_career": row.vector_career,
        "vector_vision": row.vector_vision,
        "vector_culture": row.vector_culture,
        "updated_at": row.updated_at,
    }

    # role에 따라 talent_card 또는 job_posting 찾기
    if row.role == "talent":
        talent_card = db.query(TalentCard).filter(TalentCard.user_id == row.user_id).first()
        if talent_card:
            result["reference_type"] = "talent"
            result["reference_id"] = talent_card.id
    elif row.role == "company" and row.job_posting_id:
        result["reference_type"] = "job_posting"
        result["reference_id"] = row.job_posting_id
        # job_posting_card는 별도로 조회할 필요 없음 (job_posting_id가 이미 있음)

    return result


# ============================================================
# 자동 매칭 계산 로직
# ============================================================

def _calculate_all_matches_for_talent(db: Session, talent_vector):
    """
    Talent 벡터가 생성/수정되면 모든 Company 벡터와 매칭 계산
    
    Args:
        db: DB 세션
        talent_vector: MatchingVector 객체 (role='talent')
    """
    from app.models.matching_vector import MatchingVector
    from app.services import vector_matching_service
    from app.repositories import matching_result_repo
    
    # 1. 모든 company 벡터 조회
    company_vectors = db.query(MatchingVector).filter(
        MatchingVector.role == "company"
    ).all()
    
    logger.info(f"[Auto-Matching] Talent vector {talent_vector.id} → {len(company_vectors)} company vectors")
    
    success_count = 0
    error_count = 0
    
    # 2. 각 company 벡터와 매칭 계산
    for company_vector in company_vectors:
        try:
            # 매칭 계산 (기존 vector_matching_service 활용)
            match_result = vector_matching_service.match(
                db, 
                source_id=talent_vector.id, 
                target_id=company_vector.id
            )
            
            # 3. 결과 저장 (UPSERT)
            matching_result_repo.upsert_result(
                db,
                talent_vector_id=talent_vector.id,
                company_vector_id=company_vector.id,
                talent_user_id=talent_vector.user_id,
                company_user_id=company_vector.user_id,
                job_posting_id=company_vector.job_posting_id,
                total_score=match_result["total_similarity"],
                field_scores=match_result["field_scores"],
            )
            success_count += 1
            
        except Exception as e:
            error_count += 1
            logger.warning(f"[Auto-Matching] Failed: Talent {talent_vector.id} × Company {company_vector.id}: {e}")
            continue
    
    db.flush()
    logger.info(f"[Auto-Matching] Talent {talent_vector.id} completed: {success_count} success, {error_count} errors")


def _calculate_all_matches_for_company(db: Session, company_vector):
    """
    Company 벡터가 생성/수정되면 모든 Talent 벡터와 매칭 계산
    
    Args:
        db: DB 세션
        company_vector: MatchingVector 객체 (role='company')
    """
    from app.models.matching_vector import MatchingVector
    from app.services import vector_matching_service
    from app.repositories import matching_result_repo
    
    # 1. 모든 talent 벡터 조회
    talent_vectors = db.query(MatchingVector).filter(
        MatchingVector.role == "talent"
    ).all()
    
    logger.info(f"[Auto-Matching] Company vector {company_vector.id} (JobPosting {company_vector.job_posting_id}) → {len(talent_vectors)} talent vectors")
    
    success_count = 0
    error_count = 0
    
    # 2. 각 talent 벡터와 매칭 계산
    for talent_vector in talent_vectors:
        try:
            # 매칭 계산
            match_result = vector_matching_service.match(
                db,
                source_id=talent_vector.id,
                target_id=company_vector.id
            )
            
            # 3. 결과 저장 (UPSERT)
            matching_result_repo.upsert_result(
                db,
                talent_vector_id=talent_vector.id,
                company_vector_id=company_vector.id,
                talent_user_id=talent_vector.user_id,
                company_user_id=company_vector.user_id,
                job_posting_id=company_vector.job_posting_id,
                total_score=match_result["total_similarity"],
                field_scores=match_result["field_scores"],
            )
            success_count += 1
            
        except Exception as e:
            error_count += 1
            logger.warning(f"[Auto-Matching] Failed: Company {company_vector.id} × Talent {talent_vector.id}: {e}")
            continue
    
    db.flush()
    logger.info(f"[Auto-Matching] Company {company_vector.id} completed: {success_count} success, {error_count} errors")
