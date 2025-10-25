#!/usr/bin/env python3
"""
Mock 데이터 생성 스크립트 - Vector 및 Matching 테스트용

사용법:
    poetry run python scripts/seed_mock_data.py
    
    # 또는 기존 데이터 삭제 후 재생성
    poetry run python scripts/seed_mock_data.py --clean
"""
import sys
from pathlib import Path

# 프로젝트 루트를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, date
from math import sqrt
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.profile import TalentProfile
from app.models.company import Company
from app.models.job_posting import JobPosting
from app.models.matching_vector import MatchingVector
from app.models.matching_result import MatchingResult
from app.core.security import hash_password


def clean_existing_data(db: Session):
    """기존 Mock 데이터 삭제"""
    print("🧹 기존 Mock 데이터 삭제 중...")
    
    # Mock 유저 이메일 패턴
    mock_emails = [
        "minsu.kim@example.com",
        "jihyun.park@example.com",
        "seoyeon.lee@example.com",
        "chris.kim@example.com",
        "daniel.park@example.com",
        "tech.startup@example.com",
        "finance.corp@example.com",
        "marketing.agency@example.com",
        "ecommerce.company@example.com",
        "healthtech.startup@example.com",
    ]
    
    user_ids = []
    for email in mock_emails:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user_ids.append(user.id)
    
    if not user_ids:
        print("  삭제할 Mock 데이터 없음")
        return
    
    # 1단계: matching_results 전체 삭제 (관련된 모든 결과)
    deleted_results = db.query(MatchingResult).filter(
        (MatchingResult.talent_user_id.in_(user_ids)) | 
        (MatchingResult.company_user_id.in_(user_ids))
    ).delete(synchronize_session=False)
    print(f"  • 매칭 결과 {deleted_results}개 삭제")
    db.commit()
    
    # 2단계: matching_vectors 삭제
    deleted_vectors = db.query(MatchingVector).filter(
        MatchingVector.user_id.in_(user_ids)
    ).delete(synchronize_session=False)
    print(f"  • 매칭 벡터 {deleted_vectors}개 삭제")
    db.commit()
    
    # 3단계: talent_profiles 삭제 (CASCADE 없음)
    deleted_profiles = db.query(TalentProfile).filter(
        TalentProfile.user_id.in_(user_ids)
    ).delete(synchronize_session=False)
    print(f"  • 인재 프로필 {deleted_profiles}개 삭제")
    db.commit()
    
    # 4단계: 유저 삭제 (CASCADE로 나머지 자동 삭제)
    for email in mock_emails:
        user = db.query(User).filter(User.email == email).first()
        if user:
            db.delete(user)
            print(f"  ✓ 삭제: {email}")
    
    db.commit()
    print("✅ 기존 데이터 삭제 완료\n")


def create_talent_users(db: Session):
    """인재 유저 5명 생성"""
    print("👤 인재 유저 생성 중...")
    
    talents = [
        {
            "email": "minsu.kim@example.com",
            "password": "password123",
            "role": "talent",
            "name": "김민수",
            "tagline": "React 전문 Frontend Developer",
            "desired_role": "Frontend Developer",
            "desired_salary": "4000만원 이상",
            "desired_industry": "IT·인터넷",
            "desired_company_size": "51~200명",
            "residence_location": "서울 강남구",
            "desired_work_location": "서울 전체",
            "vector": {
                "vector_roles": {"dim": 5, "vector": [0.9, 0.8, 0.7, 0.6, 0.5]},
                "vector_skills": {"dim": 5, "vector": [0.95, 0.9, 0.85, 0.8, 0.75]},
                "vector_growth": {"dim": 5, "vector": [0.8, 0.7, 0.75, 0.85, 0.7]},
                "vector_career": {"dim": 5, "vector": [0.7, 0.8, 0.6, 0.75, 0.85]},
                "vector_vision": {"dim": 5, "vector": [0.85, 0.8, 0.75, 0.7, 0.8]},
                "vector_culture": {"dim": 5, "vector": [0.8, 0.85, 0.7, 0.75, 0.9]},
            }
        },
        {
            "email": "jihyun.park@example.com",
            "password": "password123",
            "role": "talent",
            "name": "박지현",
            "tagline": "Java/Spring 전문 Backend Developer",
            "desired_role": "Backend Developer",
            "desired_salary": "5000만원 이상",
            "desired_industry": "IT·인터넷",
            "desired_company_size": "201~500명",
            "residence_location": "서울 서초구",
            "desired_work_location": "서울·경기 전체",
            "vector": {
                "vector_roles": {"dim": 5, "vector": [0.85, 0.9, 0.8, 0.75, 0.7]},
                "vector_skills": {"dim": 5, "vector": [0.9, 0.95, 0.85, 0.9, 0.8]},
                "vector_growth": {"dim": 5, "vector": [0.9, 0.85, 0.8, 0.9, 0.75]},
                "vector_career": {"dim": 5, "vector": [0.8, 0.85, 0.75, 0.8, 0.9]},
                "vector_vision": {"dim": 5, "vector": [0.88, 0.82, 0.78, 0.85, 0.9]},
                "vector_culture": {"dim": 5, "vector": [0.75, 0.8, 0.85, 0.9, 0.7]},
            }
        },
        {
            "email": "seoyeon.lee@example.com",
            "password": "password123",
            "role": "talent",
            "name": "이서연",
            "tagline": "데이터 기반 Performance Marketer",
            "desired_role": "마케터",
            "desired_salary": "3500만원 이상",
            "desired_industry": "광고·마케팅",
            "desired_company_size": "11~50명",
            "residence_location": "서울 마포구",
            "desired_work_location": "서울 서부(마포·서대문·은평)",
            "vector": {
                "vector_roles": {"dim": 5, "vector": [0.8, 0.75, 0.9, 0.7, 0.85]},
                "vector_skills": {"dim": 5, "vector": [0.85, 0.8, 0.95, 0.75, 0.9]},
                "vector_growth": {"dim": 5, "vector": [0.9, 0.8, 0.85, 0.95, 0.8]},
                "vector_career": {"dim": 5, "vector": [0.75, 0.7, 0.85, 0.8, 0.9]},
                "vector_vision": {"dim": 5, "vector": [0.8, 0.85, 0.9, 0.75, 0.85]},
                "vector_culture": {"dim": 5, "vector": [0.9, 0.85, 0.8, 0.9, 0.75]},
            }
        },
        {
            "email": "chris.kim@example.com",
            "password": "password123",
            "role": "talent",
            "name": "김영준",
            "tagline": "Product Manager with Tech Background",
            "desired_role": "프로덕트 매니저",
            "desired_salary": "6000만원 이상",
            "desired_industry": "IT·인터넷",
            "desired_company_size": "501~1,000명",
            "residence_location": "서울 성동구",
            "desired_work_location": "서울 동부(성동·광진·강동)",
            "vector": {
                "vector_roles": {"dim": 5, "vector": [0.75, 0.8, 0.85, 0.9, 0.7]},
                "vector_skills": {"dim": 5, "vector": [0.8, 0.75, 0.85, 0.95, 0.8]},
                "vector_growth": {"dim": 5, "vector": [0.85, 0.9, 0.8, 0.95, 0.85]},
                "vector_career": {"dim": 5, "vector": [0.9, 0.85, 0.8, 0.9, 0.75]},
                "vector_vision": {"dim": 5, "vector": [0.95, 0.9, 0.85, 0.8, 0.9]},
                "vector_culture": {"dim": 5, "vector": [0.85, 0.9, 0.95, 0.8, 0.85]},
            }
        },
        {
            "email": "daniel.park@example.com",
            "password": "password123",
            "role": "talent",
            "name": "박진우",
            "tagline": "B2B Sales Expert",
            "desired_role": "영업",
            "desired_salary": "4500만원 이상",
            "desired_industry": "제조·유통",
            "desired_company_size": "1,001명 이상",
            "residence_location": "경기 성남시",
            "desired_work_location": "경기 전체",
            "vector": {
                "vector_roles": {"dim": 5, "vector": [0.7, 0.75, 0.8, 0.7, 0.95]},
                "vector_skills": {"dim": 5, "vector": [0.75, 0.7, 0.85, 0.8, 0.95]},
                "vector_growth": {"dim": 5, "vector": [0.8, 0.85, 0.75, 0.8, 0.9]},
                "vector_career": {"dim": 5, "vector": [0.85, 0.8, 0.75, 0.7, 0.95]},
                "vector_vision": {"dim": 5, "vector": [0.9, 0.85, 0.8, 0.75, 0.95]},
                "vector_culture": {"dim": 5, "vector": [0.95, 0.9, 0.85, 0.8, 0.9]},
            }
        },
    ]
    
    created_users = []
    
    for talent_data in talents:
        # User 생성
        user = User(
            email=talent_data["email"],
            password_hash=hash_password(talent_data["password"]),
            role=talent_data["role"],
        )
        db.add(user)
        db.flush()  # ID 생성
        
        # TalentProfile 생성 (관심내용 포함)
        profile = TalentProfile(
            user_id=user.id,
            name=talent_data["name"],
            email=talent_data["email"],
            tagline=talent_data["tagline"],
            desired_role=talent_data.get("desired_role"),
            desired_salary=talent_data.get("desired_salary"),
            desired_industry=talent_data.get("desired_industry"),
            desired_company_size=talent_data.get("desired_company_size"),
            residence_location=talent_data.get("residence_location"),
            desired_work_location=talent_data.get("desired_work_location"),
        )
        db.add(profile)
        db.flush()
        
        # MatchingVector 생성
        vector = MatchingVector(
            user_id=user.id,
            role="talent",
            **talent_data["vector"]
        )
        db.add(vector)
        
        created_users.append(user)
        print(f"  ✓ 생성: {talent_data['name']} ({talent_data['email']})")
    
    db.commit()
    print(f"✅ 인재 유저 {len(created_users)}명 생성 완료\n")
    return created_users


def create_company_users(db: Session):
    """기업 유저 5개 생성"""
    print("🏢 기업 유저 생성 중...")
    
    companies_data = [
        {
            "email": "tech.startup@example.com",
            "password": "password123",
            "role": "company",
            "name": "테크스타트업",
            "industry": "IT/소프트웨어",
            "size": "10명 이하",
            "location_city": "서울",
            "job_postings": [
                {
                    "title": "React Frontend 개발자 모집",
                    "employment_type": "정규직",
                    "location_city": "서울",
                    "career_level": "경력 3년 이상",
                    "education_level": "학력무관",
                    "position_group": "개발",
                    "position": "프론트엔드 개발자",
                    "salary_range": "5000만 ~ 6000만",
                    "status": "PUBLISHED",
                    "vector": {
                        "vector_roles": {"dim": 5, "vector": [0.92, 0.78, 0.68, 0.58, 0.48]},
                        "vector_skills": {"dim": 5, "vector": [0.98, 0.88, 0.83, 0.78, 0.73]},
                        "vector_growth": {"dim": 5, "vector": [0.78, 0.68, 0.73, 0.83, 0.68]},
                        "vector_career": {"dim": 5, "vector": [0.68, 0.78, 0.58, 0.73, 0.83]},
                        "vector_vision": {"dim": 5, "vector": [0.83, 0.78, 0.73, 0.68, 0.78]},
                        "vector_culture": {"dim": 5, "vector": [0.78, 0.83, 0.68, 0.73, 0.88]},
                    }
                }
            ]
        },
        {
            "email": "finance.corp@example.com",
            "password": "password123",
            "role": "company",
            "name": "금융테크",
            "industry": "금융/핀테크",
            "size": "50 ~ 100명",
            "location_city": "서울",
            "job_postings": [
                {
                    "title": "Backend 개발자 (Java/Spring)",
                    "employment_type": "정규직",
                    "location_city": "서울",
                    "career_level": "경력 5년 이상",
                    "education_level": "대졸 이상",
                    "position_group": "개발",
                    "position": "백엔드 개발자",
                    "salary_range": "7000만 ~ 8000만",
                    "status": "PUBLISHED",
                    "vector": {
                        "vector_roles": {"dim": 5, "vector": [0.83, 0.88, 0.78, 0.73, 0.68]},
                        "vector_skills": {"dim": 5, "vector": [0.88, 0.93, 0.83, 0.88, 0.78]},
                        "vector_growth": {"dim": 5, "vector": [0.88, 0.83, 0.78, 0.88, 0.73]},
                        "vector_career": {"dim": 5, "vector": [0.78, 0.83, 0.73, 0.78, 0.88]},
                        "vector_vision": {"dim": 5, "vector": [0.86, 0.8, 0.76, 0.83, 0.88]},
                        "vector_culture": {"dim": 5, "vector": [0.73, 0.78, 0.83, 0.88, 0.68]},
                    }
                }
            ]
        },
        {
            "email": "marketing.agency@example.com",
            "password": "password123",
            "role": "company",
            "name": "마케팅에이전시",
            "industry": "마케팅/광고",
            "size": "30 ~ 50명",
            "location_city": "경기",
            "job_postings": [
                {
                    "title": "Performance Marketer 채용",
                    "employment_type": "정규직",
                    "location_city": "경기",
                    "career_level": "경력 3년 이상",
                    "education_level": "학력무관",
                    "position_group": "마케팅",
                    "position": "퍼포먼스 마케터",
                    "salary_range": "4000만 ~ 5000만",
                    "status": "PUBLISHED",
                    "vector": {
                        "vector_roles": {"dim": 5, "vector": [0.78, 0.73, 0.88, 0.68, 0.83]},
                        "vector_skills": {"dim": 5, "vector": [0.83, 0.78, 0.93, 0.73, 0.88]},
                        "vector_growth": {"dim": 5, "vector": [0.88, 0.78, 0.83, 0.93, 0.78]},
                        "vector_career": {"dim": 5, "vector": [0.73, 0.68, 0.83, 0.78, 0.88]},
                        "vector_vision": {"dim": 5, "vector": [0.78, 0.83, 0.88, 0.73, 0.83]},
                        "vector_culture": {"dim": 5, "vector": [0.88, 0.83, 0.78, 0.88, 0.73]},
                    }
                }
            ]
        },
        {
            "email": "ecommerce.company@example.com",
            "password": "password123",
            "role": "company",
            "name": "이커머스플랫폼",
            "industry": "이커머스",
            "size": "100 ~ 300명",
            "location_city": "서울",
            "job_postings": [
                {
                    "title": "Product Manager 채용",
                    "employment_type": "정규직",
                    "location_city": "서울",
                    "career_level": "경력 5년 이상",
                    "education_level": "대졸 이상",
                    "position_group": "기획",
                    "position": "프로덕트 매니저",
                    "salary_range": "6000만 ~ 7000만",
                    "status": "PUBLISHED",
                    "vector": {
                        "vector_roles": {"dim": 5, "vector": [0.73, 0.78, 0.83, 0.88, 0.68]},
                        "vector_skills": {"dim": 5, "vector": [0.78, 0.73, 0.83, 0.93, 0.78]},
                        "vector_growth": {"dim": 5, "vector": [0.83, 0.88, 0.78, 0.93, 0.83]},
                        "vector_career": {"dim": 5, "vector": [0.88, 0.83, 0.78, 0.88, 0.73]},
                        "vector_vision": {"dim": 5, "vector": [0.93, 0.88, 0.83, 0.78, 0.88]},
                        "vector_culture": {"dim": 5, "vector": [0.83, 0.88, 0.93, 0.78, 0.83]},
                    }
                }
            ]
        },
        {
            "email": "healthtech.startup@example.com",
            "password": "password123",
            "role": "company",
            "name": "헬스케어스타트업",
            "industry": "헬스케어",
            "size": "10 ~ 30명",
            "location_city": "경기",
            "job_postings": [
                {
                    "title": "B2B 영업 담당자 모집",
                    "employment_type": "정규직",
                    "location_city": "경기",
                    "career_level": "경력 3년 이상",
                    "education_level": "학력무관",
                    "position_group": "영업",
                    "position": "B2B 영업",
                    "salary_range": "4000만 ~ 5000만",
                    "status": "PUBLISHED",
                    "vector": {
                        "vector_roles": {"dim": 5, "vector": [0.68, 0.73, 0.78, 0.68, 0.93]},
                        "vector_skills": {"dim": 5, "vector": [0.73, 0.68, 0.83, 0.78, 0.93]},
                        "vector_growth": {"dim": 5, "vector": [0.78, 0.83, 0.73, 0.78, 0.88]},
                        "vector_career": {"dim": 5, "vector": [0.83, 0.78, 0.73, 0.68, 0.93]},
                        "vector_vision": {"dim": 5, "vector": [0.88, 0.83, 0.78, 0.73, 0.93]},
                        "vector_culture": {"dim": 5, "vector": [0.93, 0.88, 0.83, 0.78, 0.88]},
                    }
                }
            ]
        },
    ]
    
    created_companies = []
    
    for company_data in companies_data:
        # User 생성
        user = User(
            email=company_data["email"],
            password_hash=hash_password(company_data["password"]),
            role=company_data["role"],
        )
        db.add(user)
        db.flush()
        
        # Company 생성
        company = Company(
            owner_user_id=user.id,
            name=company_data["name"],
            industry=company_data["industry"],
            size=company_data["size"],
            location_city=company_data["location_city"],
            is_submitted=1,
            status="active",
        )
        db.add(company)
        db.flush()
        
        # JobPosting 및 MatchingVector 생성
        for jp_data in company_data["job_postings"]:
            vector_data = jp_data.pop("vector")
            
            job_posting = JobPosting(
                company_id=company.id,
                **jp_data
            )
            db.add(job_posting)
            db.flush()
            
            # 채용공고별 매칭 벡터
            vector = MatchingVector(
                user_id=user.id,
                role="company",
                job_posting_id=job_posting.id,
                **vector_data
            )
            db.add(vector)
        
        created_companies.append(company)
        print(f"  ✓ 생성: {company_data['name']} ({company_data['email']}) + {len(company_data['job_postings'])}개 공고")
    
    db.commit()
    print(f"✅ 기업 유저 {len(created_companies)}개 생성 완료\n")
    return created_companies


def calculate_cosine_similarity(vec1: List[float], vec2: List[float]) -> Optional[float]:
    """두 벡터 간의 코사인 유사도 계산 (-1~1 범위)"""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return None
    
    # Cosine similarity 계산
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5
    
    if magnitude1 == 0 or magnitude2 == 0:
        return None
    
    similarity = dot_product / (magnitude1 * magnitude2)
    return max(-1.0, min(1.0, similarity))


def normalize_to_score(cosine: float) -> float:
    """코사인 유사도(-1~1)를 점수(0~100)로 변환"""
    clamped = max(min(cosine, 1.0), -1.0)
    return ((clamped + 1.0) / 2.0) * 100.0


def extract_vector_values(vector_data: Dict[str, Any]) -> List[float]:
    """벡터 데이터에서 실제 값 추출"""
    if isinstance(vector_data, dict):
        if "vector" in vector_data:
            return vector_data["vector"]
        elif "values" in vector_data:
            return vector_data["values"]
    return []


def calculate_matching_scores(talent_vector: MatchingVector, company_vector: MatchingVector) -> Dict[str, float]:
    """두 벡터 간 매칭 점수 계산"""
    vector_fields = ["vector_roles", "vector_skills", "vector_growth", "vector_career", "vector_vision", "vector_culture"]
    
    field_scores = {}
    valid_scores = []
    
    for field in vector_fields:
        talent_data = getattr(talent_vector, field)
        company_data = getattr(company_vector, field)
        
        if talent_data is None or company_data is None:
            continue
        
        talent_vec = extract_vector_values(talent_data)
        company_vec = extract_vector_values(company_data)
        
        if not talent_vec or not company_vec:
            continue
        
        # 차원이 다르면 건너뛰기
        if len(talent_vec) != len(company_vec):
            print(f"    ⚠ {field}: 차원 불일치 (talent={len(talent_vec)}, company={len(company_vec)}) - 건너뜀")
            continue
        
        try:
            cosine = calculate_cosine_similarity(talent_vec, company_vec)
            
            if cosine is None:
                continue
            
            score = normalize_to_score(cosine)
            
            field_name = field.replace("vector_", "score_")
            field_scores[field_name] = score
            valid_scores.append(score)
        except Exception as e:
            print(f"    ⚠ {field}: 계산 오류 ({str(e)}) - 건너뜀")
            continue
    
    # 전체 평균 점수 (유효한 점수만 사용)
    if valid_scores:
        total_score = sum(valid_scores) / len(valid_scores)
    else:
        total_score = 0.0
    
    field_scores["total_score"] = total_score
    return field_scores


def generate_matching_results(db: Session):
    """모든 인재-기업 조합에 대해 매칭 결과 생성"""
    print("🔗 매칭 결과 생성 중...")
    
    # 기존 모든 matching_results 삭제 (중복 방지)
    existing_count = db.query(MatchingResult).count()
    if existing_count > 0:
        db.query(MatchingResult).delete(synchronize_session=False)
        db.commit()
        print(f"  • 기존 매칭 결과 {existing_count}개 삭제")
    
    # 인재 벡터 가져오기
    talent_vectors = db.query(MatchingVector).filter(MatchingVector.role == "talent").all()
    
    # 기업 벡터 가져오기 (job_posting_id가 있는 것들)
    company_vectors = db.query(MatchingVector).filter(
        MatchingVector.role == "company",
        MatchingVector.job_posting_id.isnot(None)
    ).all()
    
    created_count = 0
    
    for talent_vector in talent_vectors:
        for company_vector in company_vectors:
            # 매칭 점수 계산
            scores = calculate_matching_scores(talent_vector, company_vector)
            
            # total_score가 0이면 스킵 (유효한 벡터 데이터 없음)
            if scores["total_score"] == 0.0:
                talent_user = db.query(User).filter(User.id == talent_vector.user_id).first()
                talent_profile = db.query(TalentProfile).filter(TalentProfile.user_id == talent_vector.user_id).first()
                job_posting = db.query(JobPosting).filter(JobPosting.id == company_vector.job_posting_id).first()
                
                talent_name = talent_profile.name if talent_profile else f"User {talent_user.id}"
                job_title = job_posting.title if job_posting else f"Job {company_vector.job_posting_id}"
                
                print(f"  ⚠️  {talent_name} ↔ {job_title}: 유효한 벡터 없음 - 스킵")
                continue
            
            # MatchingResult 생성
            matching_result = MatchingResult(
                talent_vector_id=talent_vector.id,
                company_vector_id=company_vector.id,
                talent_user_id=talent_vector.user_id,
                company_user_id=company_vector.user_id,
                job_posting_id=company_vector.job_posting_id,
                total_score=scores["total_score"],
                score_roles=scores.get("score_roles"),
                score_skills=scores.get("score_skills"),
                score_growth=scores.get("score_growth"),
                score_career=scores.get("score_career"),
                score_vision=scores.get("score_vision"),
                score_culture=scores.get("score_culture"),
            )
            
            db.add(matching_result)
            created_count += 1
            
            # 인재 이름과 공고 간단 정보 출력
            talent_user = db.query(User).filter(User.id == talent_vector.user_id).first()
            talent_profile = db.query(TalentProfile).filter(TalentProfile.user_id == talent_vector.user_id).first()
            job_posting = db.query(JobPosting).filter(JobPosting.id == company_vector.job_posting_id).first()
            
            talent_name = talent_profile.name if talent_profile else f"User {talent_user.id}"
            job_title = job_posting.title if job_posting else f"Job {company_vector.job_posting_id}"
            
            print(f"  ✓ {talent_name} ↔ {job_title}: {scores['total_score']:.1f}점")
    
    db.commit()
    print(f"✅ 매칭 결과 {created_count}개 생성 완료\n")
    return created_count


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Mock 데이터 생성 스크립트")
    parser.add_argument("--clean", action="store_true", help="기존 Mock 데이터 삭제 후 생성")
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎭 Mock 데이터 생성 스크립트")
    print("=" * 60)
    print()
    
    db = SessionLocal()
    
    try:
        if args.clean:
            clean_existing_data(db)
        
        # 인재 유저 생성
        talent_users = create_talent_users(db)
        
        # 기업 유저 생성
        company_users = create_company_users(db)
        
        # 매칭 결과 생성
        matching_count = generate_matching_results(db)
        
        print("=" * 60)
        print("✨ Mock 데이터 생성 완료!")
        print("=" * 60)
        print()
        print("📊 생성된 데이터:")
        print(f"  - 인재 유저: {len(talent_users)}명")
        print(f"  - 기업 유저: {len(company_users)}개")
        print(f"  - 채용 공고: {len(company_users)}개 (각 기업당 1개)")
        print(f"  - 매칭 벡터: {len(talent_users) + len(company_users)}개")
        print(f"  - 매칭 결과: {matching_count}개 (모든 조합)")
        print()
        print("🔐 로그인 정보:")
        print("  - 모든 계정 비밀번호: password123")
        print()
        print("🧪 테스트 방법:")
        print("  1. 인재 계정으로 로그인: POST /auth/login")
        print("  2. 매칭 결과 확인: GET /api/matching-results/talents/{user_id}/job-postings")
        print("  3. 기업 매칭 확인: GET /api/matching-results/job-postings/{job_posting_id}/talents")
        print()
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
