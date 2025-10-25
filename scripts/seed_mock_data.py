#!/usr/bin/env python3
"""
🎭 FitConnect Mock 데이터 생성 스크립트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ 완벽하게 연결된 Mock 데이터 생성:
   - 인재 10명 (다양한 직무/경력)
   - 기업 5개 (각 2개 채용공고)
   - 카드 데이터 (인재/공고별)
   - 벡터 데이터 (6차원)
   - 매칭 결과 (모든 조합)

📝 사용법:
    poetry run python scripts/seed_mock_data.py
    
🔄 기존 데이터 삭제 후 재생성:
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
from app.models.talent_card import TalentCard
from app.models.job_posting_card import JobPostingCard
from app.core.security import hash_password


def clean_existing_data(db: Session):
    """🧹 기존 Mock 데이터 완전 삭제"""
    print("━" * 60)
    print("🧹 기존 Mock 데이터 삭제 중...")
    print("━" * 60)
    
    # Mock 유저 이메일 리스트 (인재 10명 + 기업 5개)
    mock_emails = [
        # 인재 10명
        "talent01@fitconnect.test",
        "talent02@fitconnect.test",
        "talent03@fitconnect.test",
        "talent04@fitconnect.test",
        "talent05@fitconnect.test",
        "talent06@fitconnect.test",
        "talent07@fitconnect.test",
        "talent08@fitconnect.test",
        "talent09@fitconnect.test",
        "talent10@fitconnect.test",
        # 기업 5개
        "company01@fitconnect.test",
        "company02@fitconnect.test",
        "company03@fitconnect.test",
        "company04@fitconnect.test",
        "company05@fitconnect.test",
    ]
    
    # User ID 수집
    user_ids = []
    for email in mock_emails:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user_ids.append(user.id)
    
    if not user_ids:
        print("✓ 삭제할 Mock 데이터 없음\n")
        return
    
    # 1. MatchingResult 삭제
    deleted_results = db.query(MatchingResult).filter(
        (MatchingResult.talent_user_id.in_(user_ids)) | 
        (MatchingResult.company_user_id.in_(user_ids))
    ).delete(synchronize_session=False)
    print(f"  ✓ 매칭 결과: {deleted_results}개 삭제")
    db.commit()
    
    # 2. MatchingVector 삭제
    deleted_vectors = db.query(MatchingVector).filter(
        MatchingVector.user_id.in_(user_ids)
    ).delete(synchronize_session=False)
    print(f"  ✓ 매칭 벡터: {deleted_vectors}개 삭제")
    db.commit()
    
    # 3. TalentCard 삭제
    deleted_talent_cards = db.query(TalentCard).filter(
        TalentCard.talent_user_id.in_(user_ids)
    ).delete(synchronize_session=False)
    print(f"  ✓ 인재 카드: {deleted_talent_cards}개 삭제")
    db.commit()
    
    # 4. JobPostingCard 삭제 (JobPosting ID로 찾아서)
    job_posting_ids = [jp.id for jp in db.query(JobPosting).join(Company).filter(Company.owner_user_id.in_(user_ids)).all()]
    if job_posting_ids:
        deleted_jp_cards = db.query(JobPostingCard).filter(
            JobPostingCard.job_posting_id.in_(job_posting_ids)
        ).delete(synchronize_session=False)
        print(f"  ✓ 채용공고 카드: {deleted_jp_cards}개 삭제")
        db.commit()
    
    # 5. TalentProfile 삭제
    deleted_profiles = db.query(TalentProfile).filter(
        TalentProfile.user_id.in_(user_ids)
    ).delete(synchronize_session=False)
    print(f"  ✓ 인재 프로필: {deleted_profiles}개 삭제")
    db.commit()
    
    # 6. User 삭제 (CASCADE로 나머지 자동 삭제)
    for email in mock_emails:
        user = db.query(User).filter(User.email == email).first()
        if user:
            db.delete(user)
    
    db.commit()
    print(f"  ✓ 유저: {len(user_ids)}명 삭제")
    print("\n✅ 기존 데이터 삭제 완료!\n")




# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📦 Mock 데이터 정의
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MOCK_TALENTS = [
    {
        "id": 1,
        "email": "talent01@fitconnect.test",
        "name": "김민수",
        "tagline": "React 전문 Frontend 개발자",
        "desired_role": "Frontend Developer",
        "desired_salary": "5,000만원 이상",
        "desired_industry": "IT·인터넷",
        "desired_company_size": "51~200명",
        "residence_location": "서울 강남구",
        "desired_work_location": "서울 전체",
        "vector": {
            "vector_roles": [0.95, 0.85, 0.75, 0.65, 0.55],
            "vector_skills": [0.98, 0.92, 0.88, 0.82, 0.76],
            "vector_growth": [0.85, 0.75, 0.80, 0.90, 0.75],
            "vector_career": [0.75, 0.85, 0.65, 0.78, 0.88],
            "vector_vision": [0.88, 0.82, 0.78, 0.72, 0.82],
            "vector_culture": [0.82, 0.88, 0.72, 0.78, 0.92],
        },
        "cards": [
            {
                "category": "roles",
                "title": "React 전문성",
                "description": "5년 이상의 React 개발 경험으로 복잡한 UI 컴포넌트를 설계하고 구현할 수 있습니다.",
                "keywords": ["React", "TypeScript", "Redux", "Next.js"]
            },
            {
                "category": "skills",
                "title": "성능 최적화 전문가",
                "description": "웹 성능 최적화를 통해 로딩 속도 40% 개선 경험이 있습니다.",
                "keywords": ["Performance", "Optimization", "Lighthouse", "Core Web Vitals"]
            }
        ]
    },
    {
        "id": 2,
        "email": "talent02@fitconnect.test",
        "name": "박지현",
        "tagline": "Java/Spring 백엔드 아키텍트",
        "desired_role": "Backend Developer",
        "desired_salary": "7,000만원 이상",
        "desired_industry": "IT·인터넷",
        "desired_company_size": "201~500명",
        "residence_location": "서울 서초구",
        "desired_work_location": "서울·경기 전체",
        "vector": {
            "vector_roles": [0.88, 0.93, 0.83, 0.78, 0.73],
            "vector_skills": [0.92, 0.97, 0.88, 0.93, 0.83],
            "vector_growth": [0.93, 0.88, 0.83, 0.93, 0.78],
            "vector_career": [0.83, 0.88, 0.78, 0.83, 0.93],
            "vector_vision": [0.90, 0.85, 0.80, 0.88, 0.93],
            "vector_culture": [0.78, 0.83, 0.88, 0.93, 0.73],
        },
        "cards": [
            {
                "category": "roles",
                "title": "MSA 아키텍처 설계",
                "description": "마이크로서비스 아키텍처 전환 프로젝트 리드 경험",
                "keywords": ["Spring Boot", "MSA", "Docker", "Kubernetes"]
            },
            {
                "category": "skills",
                "title": "대용량 트래픽 처리",
                "description": "일 트래픽 1,000만 PV 처리 시스템 설계 및 운영",
                "keywords": ["Redis", "Kafka", "AWS", "Load Balancing"]
            }
        ]
    },
    {
        "id": 3,
        "email": "talent03@fitconnect.test",
        "name": "이서연",
        "tagline": "데이터 기반 퍼포먼스 마케터",
        "desired_role": "마케터",
        "desired_salary": "4,500만원 이상",
        "desired_industry": "광고·마케팅",
        "desired_company_size": "11~50명",
        "residence_location": "서울 마포구",
        "desired_work_location": "서울 서부(마포·서대문·은평)",
        "vector": {
            "vector_roles": [0.83, 0.78, 0.93, 0.73, 0.88],
            "vector_skills": [0.88, 0.83, 0.97, 0.78, 0.93],
            "vector_growth": [0.93, 0.83, 0.88, 0.97, 0.83],
            "vector_career": [0.78, 0.73, 0.88, 0.83, 0.93],
            "vector_vision": [0.83, 0.88, 0.93, 0.78, 0.88],
            "vector_culture": [0.93, 0.88, 0.83, 0.93, 0.78],
        },
        "cards": [
            {
                "category": "roles",
                "title": "퍼포먼스 마케팅 전문가",
                "description": "구글/메타 광고 통해 ROAS 500% 달성",
                "keywords": ["Google Ads", "Facebook Ads", "ROAS", "CPA"]
            },
            {
                "category": "growth",
                "title": "데이터 분석",
                "description": "GA4, Amplitude 활용한 사용자 행동 분석",
                "keywords": ["GA4", "Amplitude", "SQL", "Python"]
            }
        ]
    },
    {
        "id": 4,
        "email": "talent04@fitconnect.test",
        "name": "김영준",
        "tagline": "Product Manager with Tech Background",
        "desired_role": "프로덕트 매니저",
        "desired_salary": "8,000만원 이상",
        "desired_industry": "IT·인터넷",
        "desired_company_size": "501~1,000명",
        "residence_location": "서울 성동구",
        "desired_work_location": "서울 동부(성동·광진·강동)",
        "vector": {
            "vector_roles": [0.78, 0.83, 0.88, 0.93, 0.73],
            "vector_skills": [0.83, 0.78, 0.88, 0.97, 0.83],
            "vector_growth": [0.88, 0.93, 0.83, 0.97, 0.88],
            "vector_career": [0.93, 0.88, 0.83, 0.93, 0.78],
            "vector_vision": [0.97, 0.93, 0.88, 0.83, 0.93],
            "vector_culture": [0.88, 0.93, 0.97, 0.83, 0.88],
        },
        "cards": [
            {
                "category": "roles",
                "title": "프로덕트 전략 수립",
                "description": "0-1 프로덕트 런칭 및 PMF 달성 경험",
                "keywords": ["Product Strategy", "PMF", "0-1 Launch", "OKR"]
            },
            {
                "category": "vision",
                "title": "데이터 기반 의사결정",
                "description": "A/B 테스트 통해 전환율 35% 개선",
                "keywords": ["A/B Test", "Data Analysis", "Metrics", "KPI"]
            }
        ]
    },
    {
        "id": 5,
        "email": "talent05@fitconnect.test",
        "name": "박진우",
        "tagline": "B2B 영업 전문가",
        "desired_role": "영업",
        "desired_salary": "6,000만원 이상",
        "desired_industry": "제조·유통",
        "desired_company_size": "1,001명 이상",
        "residence_location": "경기 성남시",
        "desired_work_location": "경기 전체",
        "vector": {
            "vector_roles": [0.73, 0.78, 0.83, 0.73, 0.97],
            "vector_skills": [0.78, 0.73, 0.88, 0.83, 0.97],
            "vector_growth": [0.83, 0.88, 0.78, 0.83, 0.93],
            "vector_career": [0.88, 0.83, 0.78, 0.73, 0.97],
            "vector_vision": [0.93, 0.88, 0.83, 0.78, 0.97],
            "vector_culture": [0.97, 0.93, 0.88, 0.83, 0.93],
        },
        "cards": [
            {
                "category": "roles",
                "title": "B2B 세일즈 전문",
                "description": "연 매출 30억 달성, 주요 기업 고객 50개사 확보",
                "keywords": ["B2B Sales", "Enterprise", "Contract", "Negotiation"]
            },
            {
                "category": "culture",
                "title": "관계 구축 전문가",
                "description": "장기 파트너십 구축으로 재계약율 95% 달성",
                "keywords": ["Relationship", "Partnership", "Retention", "CRM"]
            }
        ]
    },
    {
        "id": 6,
        "email": "talent06@fitconnect.test",
        "name": "정수민",
        "tagline": "UX/UI 디자이너",
        "desired_role": "UI/UX Designer",
        "desired_salary": "4,500만원 이상",
        "desired_industry": "IT·인터넷",
        "desired_company_size": "51~200명",
        "residence_location": "서울 용산구",
        "desired_work_location": "서울 중부(종로·중구·용산)",
        "vector": {
            "vector_roles": [0.90, 0.80, 0.70, 0.85, 0.60],
            "vector_skills": [0.93, 0.85, 0.78, 0.88, 0.73],
            "vector_growth": [0.80, 0.85, 0.90, 0.75, 0.80],
            "vector_career": [0.70, 0.75, 0.80, 0.85, 0.70],
            "vector_vision": [0.85, 0.90, 0.80, 0.85, 0.75],
            "vector_culture": [0.88, 0.82, 0.85, 0.90, 0.78],
        },
        "cards": [
            {
                "category": "roles",
                "title": "사용자 중심 디자인",
                "description": "사용자 리서치 기반 UX 개선으로 만족도 40% 향상",
                "keywords": ["UX Research", "User Interview", "Persona", "Journey Map"]
            },
            {
                "category": "skills",
                "title": "디자인 시스템 구축",
                "description": "컴포넌트 기반 디자인 시스템 설계 및 운영",
                "keywords": ["Design System", "Figma", "Component", "Token"]
            }
        ]
    },
    {
        "id": 7,
        "email": "talent07@fitconnect.test",
        "name": "최동현",
        "tagline": "DevOps Engineer",
        "desired_role": "DevOps Engineer",
        "desired_salary": "6,500만원 이상",
        "desired_industry": "IT·인터넷",
        "desired_company_size": "201~500명",
        "residence_location": "서울 구로구",
        "desired_work_location": "서울 남서부(관악·동작·구로)",
        "vector": {
            "vector_roles": [0.85, 0.90, 0.75, 0.70, 0.65],
            "vector_skills": [0.90, 0.95, 0.85, 0.80, 0.75],
            "vector_growth": [0.88, 0.82, 0.78, 0.85, 0.80],
            "vector_career": [0.80, 0.88, 0.73, 0.78, 0.85],
            "vector_vision": [0.85, 0.80, 0.88, 0.75, 0.82],
            "vector_culture": [0.75, 0.80, 0.85, 0.88, 0.70],
        },
        "cards": [
            {
                "category": "roles",
                "title": "CI/CD 파이프라인 구축",
                "description": "Jenkins, GitLab CI로 배포 시간 80% 단축",
                "keywords": ["CI/CD", "Jenkins", "GitLab", "Automation"]
            },
            {
                "category": "skills",
                "title": "클라우드 인프라 설계",
                "description": "AWS, GCP 기반 auto-scaling 인프라 구축",
                "keywords": ["AWS", "GCP", "Terraform", "Kubernetes"]
            }
        ]
    },
    {
        "id": 8,
        "email": "talent08@fitconnect.test",
        "name": "한지원",
        "tagline": "데이터 사이언티스트",
        "desired_role": "Data Scientist",
        "desired_salary": "7,500만원 이상",
        "desired_industry": "IT·인터넷",
        "desired_company_size": "201~500명",
        "residence_location": "서울 송파구",
        "desired_work_location": "서울 동남부(송파·강동)",
        "vector": {
            "vector_roles": [0.80, 0.88, 0.93, 0.75, 0.70],
            "vector_skills": [0.85, 0.90, 0.97, 0.88, 0.78],
            "vector_growth": [0.90, 0.85, 0.93, 0.95, 0.82],
            "vector_career": [0.75, 0.80, 0.88, 0.85, 0.90],
            "vector_vision": [0.88, 0.85, 0.92, 0.80, 0.85],
            "vector_culture": [0.82, 0.88, 0.85, 0.90, 0.75],
        },
        "cards": [
            {
                "category": "roles",
                "title": "머신러닝 모델 개발",
                "description": "추천 시스템 개발로 CTR 25% 향상",
                "keywords": ["Machine Learning", "Python", "TensorFlow", "PyTorch"]
            },
            {
                "category": "skills",
                "title": "빅데이터 분석",
                "description": "Spark, Hadoop 활용 대용량 데이터 처리",
                "keywords": ["Spark", "Hadoop", "SQL", "BigQuery"]
            }
        ]
    },
    {
        "id": 9,
        "email": "talent09@fitconnect.test",
        "name": "강민지",
        "tagline": "콘텐츠 마케터",
        "desired_role": "콘텐츠 마케터",
        "desired_salary": "4,000만원 이상",
        "desired_industry": "미디어·엔터테인먼트",
        "desired_company_size": "11~50명",
        "residence_location": "서울 강북구",
        "desired_work_location": "서울 북부(강북·노원·도봉)",
        "vector": {
            "vector_roles": [0.75, 0.70, 0.90, 0.80, 0.85],
            "vector_skills": [0.80, 0.75, 0.93, 0.85, 0.90],
            "vector_growth": [0.88, 0.80, 0.85, 0.92, 0.78],
            "vector_career": [0.70, 0.68, 0.82, 0.78, 0.88],
            "vector_vision": [0.78, 0.82, 0.88, 0.75, 0.82],
            "vector_culture": [0.90, 0.85, 0.80, 0.88, 0.73],
        },
        "cards": [
            {
                "category": "roles",
                "title": "소셜 미디어 운영",
                "description": "인스타그램 팔로워 10만 달성, 월 평균 도달 수 50만",
                "keywords": ["Social Media", "Instagram", "Content", "Community"]
            },
            {
                "category": "growth",
                "title": "바이럴 콘텐츠 기획",
                "description": "조회수 100만 이상 콘텐츠 10개 이상 제작",
                "keywords": ["Viral", "Video", "Storytelling", "Engagement"]
            }
        ]
    },
    {
        "id": 10,
        "email": "talent10@fitconnect.test",
        "name": "오성훈",
        "tagline": "HR 매니저",
        "desired_role": "HR Manager",
        "desired_salary": "5,500만원 이상",
        "desired_industry": "컨설팅",
        "desired_company_size": "101~200명",
        "residence_location": "서울 영등포구",
        "desired_work_location": "서울 서남부(영등포·양천)",
        "vector": {
            "vector_roles": [0.70, 0.75, 0.80, 0.88, 0.92],
            "vector_skills": [0.75, 0.78, 0.83, 0.90, 0.95],
            "vector_growth": [0.82, 0.85, 0.78, 0.88, 0.85],
            "vector_career": [0.88, 0.82, 0.75, 0.85, 0.92],
            "vector_vision": [0.85, 0.88, 0.80, 0.82, 0.90],
            "vector_culture": [0.95, 0.90, 0.88, 0.85, 0.92],
        },
        "cards": [
            {
                "category": "roles",
                "title": "채용 전문가",
                "description": "연간 100명 이상 채용 성공, 이직률 10% 미만 유지",
                "keywords": ["Recruiting", "Hiring", "Talent Acquisition", "ATS"]
            },
            {
                "category": "culture",
                "title": "조직문화 개선",
                "description": "직원 만족도 조사 실시 및 개선 프로그램 운영",
                "keywords": ["Culture", "Engagement", "Survey", "Retention"]
            }
        ]
    },
]

MOCK_COMPANIES = [
    {
        "id": 1,
        "email": "company01@fitconnect.test",
        "name": "테크이노베이션",
        "industry": "IT·인터넷",
        "size": "51~200명",
        "location_city": "서울",
        "job_postings": [
            {
                "id": 1,
                "title": "React Frontend 개발자 채용",
                "employment_type": "정규직",
                "location_city": "서울",
                "career_level": "경력 3~5년",
                "education_level": "학력무관",
                "position_group": "개발",
                "position": "프론트엔드 개발자",
                "salary_range": "5000만 ~ 6500만",
                "term_months": 0,
                "status": "PUBLISHED",
                "vector": {
                    "vector_roles": [0.93, 0.83, 0.73, 0.63, 0.53],
                    "vector_skills": [0.96, 0.90, 0.86, 0.80, 0.74],
                    "vector_growth": [0.83, 0.73, 0.78, 0.88, 0.73],
                    "vector_career": [0.73, 0.83, 0.63, 0.76, 0.86],
                    "vector_vision": [0.86, 0.80, 0.76, 0.70, 0.80],
                    "vector_culture": [0.80, 0.86, 0.70, 0.76, 0.90],
                },
                "cards": [
                    {
                        "category": "roles",
                        "title": "React 프론트엔드 개발",
                        "description": "최신 React 기술 스택으로 사용자 경험을 개선하는 프론트엔드 개발자를 찾습니다.",
                        "keywords": ["React", "TypeScript", "Next.js", "Redux"]
                    },
                    {
                        "category": "growth",
                        "title": "빠른 성장 환경",
                        "description": "스타트업 환경에서 빠르게 성장할 수 있는 기회를 제공합니다.",
                        "keywords": ["Fast Growth", "Startup", "Learning", "Challenge"]
                    }
                ]
            },
            {
                "id": 2,
                "title": "UI/UX 디자이너 모집",
                "employment_type": "정규직",
                "location_city": "서울",
                "career_level": "경력 2~4년",
                "education_level": "학력무관",
                "position_group": "디자인",
                "position": "UI/UX 디자이너",
                "salary_range": "4500만 ~ 6000만",
                "term_months": 0,
                "status": "PUBLISHED",
                "vector": {
                    "vector_roles": [0.88, 0.78, 0.68, 0.83, 0.58],
                    "vector_skills": [0.91, 0.83, 0.76, 0.86, 0.71],
                    "vector_growth": [0.78, 0.83, 0.88, 0.73, 0.78],
                    "vector_career": [0.68, 0.73, 0.78, 0.83, 0.68],
                    "vector_vision": [0.83, 0.88, 0.78, 0.83, 0.73],
                    "vector_culture": [0.86, 0.80, 0.83, 0.88, 0.76],
                },
                "cards": [
                    {
                        "category": "roles",
                        "title": "사용자 중심 디자인",
                        "description": "사용자 경험을 중심으로 한 UI/UX 디자인을 담당합니다.",
                        "keywords": ["UX Design", "Figma", "Prototype", "User Research"]
                    },
                    {
                        "category": "culture",
                        "title": "협업 중심 문화",
                        "description": "개발자, 기획자와 긴밀하게 협업하는 환경입니다.",
                        "keywords": ["Collaboration", "Agile", "Communication", "Team"]
                    }
                ]
            }
        ]
    },
    {
        "id": 2,
        "email": "company02@fitconnect.test",
        "name": "글로벌금융그룹",
        "industry": "금융",
        "size": "501~1,000명",
        "location_city": "서울",
        "job_postings": [
            {
                "id": 3,
                "title": "Backend 개발자 (Java/Spring)",
                "employment_type": "정규직",
                "location_city": "서울",
                "career_level": "경력 5~7년",
                "education_level": "대졸 이상",
                "position_group": "개발",
                "position": "백엔드 개발자",
                "salary_range": "7000만 ~ 9000만",
                "term_months": 0,
                "status": "PUBLISHED",
                "vector": {
                    "vector_roles": [0.86, 0.91, 0.81, 0.76, 0.71],
                    "vector_skills": [0.90, 0.95, 0.86, 0.91, 0.81],
                    "vector_growth": [0.91, 0.86, 0.81, 0.91, 0.76],
                    "vector_career": [0.81, 0.86, 0.76, 0.81, 0.91],
                    "vector_vision": [0.88, 0.83, 0.78, 0.86, 0.91],
                    "vector_culture": [0.76, 0.81, 0.86, 0.91, 0.71],
                },
                "cards": [
                    {
                        "category": "roles",
                        "title": "금융 시스템 개발",
                        "description": "안정적인 금융 시스템 백엔드 개발을 담당합니다.",
                        "keywords": ["Spring Boot", "Java", "MSA", "Database"]
                    },
                    {
                        "category": "career",
                        "title": "커리어 성장 기회",
                        "description": "대기업 환경에서 체계적인 커리어 성장이 가능합니다.",
                        "keywords": ["Career Growth", "Mentoring", "Training", "Promotion"]
                    }
                ]
            },
            {
                "id": 4,
                "title": "DevOps Engineer 채용",
                "employment_type": "정규직",
                "location_city": "서울",
                "career_level": "경력 4~6년",
                "education_level": "학력무관",
                "position_group": "개발",
                "position": "DevOps 엔지니어",
                "salary_range": "6500만 ~ 8500만",
                "term_months": 0,
                "status": "PUBLISHED",
                "vector": {
                    "vector_roles": [0.83, 0.88, 0.73, 0.68, 0.63],
                    "vector_skills": [0.88, 0.93, 0.83, 0.78, 0.73],
                    "vector_growth": [0.86, 0.80, 0.76, 0.83, 0.78],
                    "vector_career": [0.78, 0.86, 0.71, 0.76, 0.83],
                    "vector_vision": [0.83, 0.78, 0.86, 0.73, 0.80],
                    "vector_culture": [0.73, 0.78, 0.83, 0.86, 0.68],
                },
                "cards": [
                    {
                        "category": "roles",
                        "title": "CI/CD 인프라 구축",
                        "description": "최신 DevOps 도구를 활용한 인프라 자동화를 담당합니다.",
                        "keywords": ["Kubernetes", "Docker", "AWS", "Terraform"]
                    },
                    {
                        "category": "skills",
                        "title": "대규모 시스템 운영",
                        "description": "안정적인 대규모 서비스 운영 경험을 쌓을 수 있습니다.",
                        "keywords": ["Monitoring", "Logging", "Scaling", "Reliability"]
                    }
                ]
            }
        ]
    },
    {
        "id": 3,
        "email": "company03@fitconnect.test",
        "name": "크리에이티브에이전시",
        "industry": "마케팅·광고",
        "size": "11~50명",
        "location_city": "서울",
        "job_postings": [
            {
                "id": 5,
                "title": "퍼포먼스 마케터 모집",
                "employment_type": "정규직",
                "location_city": "서울",
                "career_level": "경력 3~5년",
                "education_level": "학력무관",
                "position_group": "마케팅",
                "position": "퍼포먼스 마케터",
                "salary_range": "4500만 ~ 6000만",
                "term_months": 0,
                "status": "PUBLISHED",
                "vector": {
                    "vector_roles": [0.81, 0.76, 0.91, 0.71, 0.86],
                    "vector_skills": [0.86, 0.81, 0.95, 0.76, 0.91],
                    "vector_growth": [0.91, 0.81, 0.86, 0.95, 0.81],
                    "vector_career": [0.76, 0.71, 0.86, 0.81, 0.91],
                    "vector_vision": [0.81, 0.86, 0.91, 0.76, 0.86],
                    "vector_culture": [0.91, 0.86, 0.81, 0.91, 0.76],
                },
                "cards": [
                    {
                        "category": "roles",
                        "title": "데이터 기반 마케팅",
                        "description": "성과 중심의 디지털 마케팅을 담당합니다.",
                        "keywords": ["Google Ads", "Facebook Ads", "ROAS", "Analytics"]
                    },
                    {
                        "category": "growth",
                        "title": "전문성 개발",
                        "description": "마케팅 전문가로 성장할 수 있는 다양한 프로젝트 경험",
                        "keywords": ["Campaign", "Optimization", "Strategy", "Growth"]
                    }
                ]
            },
            {
                "id": 6,
                "title": "콘텐츠 마케터 채용",
                "employment_type": "정규직",
                "location_city": "서울",
                "career_level": "경력 2~4년",
                "education_level": "학력무관",
                "position_group": "마케팅",
                "position": "콘텐츠 마케터",
                "salary_range": "4000만 ~ 5500만",
                "term_months": 0,
                "status": "PUBLISHED",
                "vector": {
                    "vector_roles": [0.73, 0.68, 0.88, 0.78, 0.83],
                    "vector_skills": [0.78, 0.73, 0.91, 0.83, 0.88],
                    "vector_growth": [0.86, 0.78, 0.83, 0.90, 0.76],
                    "vector_career": [0.68, 0.66, 0.80, 0.76, 0.86],
                    "vector_vision": [0.76, 0.80, 0.86, 0.73, 0.80],
                    "vector_culture": [0.88, 0.83, 0.78, 0.86, 0.71],
                },
                "cards": [
                    {
                        "category": "roles",
                        "title": "콘텐츠 기획 및 제작",
                        "description": "소셜 미디어 콘텐츠 기획 및 제작을 담당합니다.",
                        "keywords": ["Content", "Social Media", "Video", "Storytelling"]
                    },
                    {
                        "category": "culture",
                        "title": "창의적인 환경",
                        "description": "자유로운 아이디어 제안이 가능한 수평적 문화",
                        "keywords": ["Creative", "Flexible", "Innovation", "Freedom"]
                    }
                ]
            }
        ]
    },
    {
        "id": 4,
        "email": "company04@fitconnect.test",
        "name": "이커머스플랫폼",
        "industry": "이커머스",
        "size": "201~500명",
        "location_city": "서울",
        "job_postings": [
            {
                "id": 7,
                "title": "Product Manager 모집",
                "employment_type": "정규직",
                "location_city": "서울",
                "career_level": "경력 5~7년",
                "education_level": "대졸 이상",
                "position_group": "기획",
                "position": "프로덕트 매니저",
                "salary_range": "7000만 ~ 9000만",
                "term_months": 0,
                "status": "PUBLISHED",
                "vector": {
                    "vector_roles": [0.76, 0.81, 0.86, 0.91, 0.71],
                    "vector_skills": [0.81, 0.76, 0.86, 0.95, 0.81],
                    "vector_growth": [0.86, 0.91, 0.81, 0.95, 0.86],
                    "vector_career": [0.91, 0.86, 0.81, 0.91, 0.76],
                    "vector_vision": [0.95, 0.91, 0.86, 0.81, 0.91],
                    "vector_culture": [0.86, 0.91, 0.95, 0.81, 0.86],
                },
                "cards": [
                    {
                        "category": "roles",
                        "title": "프로덕트 전략 수립",
                        "description": "이커머스 플랫폼의 핵심 프로덕트를 기획하고 운영합니다.",
                        "keywords": ["Product Strategy", "Roadmap", "Feature", "Analytics"]
                    },
                    {
                        "category": "vision",
                        "title": "비즈니스 임팩트",
                        "description": "수백만 사용자에게 영향을 미치는 의사결정 경험",
                        "keywords": ["Impact", "Scale", "Growth", "Innovation"]
                    }
                ]
            },
            {
                "id": 8,
                "title": "Data Scientist 채용",
                "employment_type": "정규직",
                "location_city": "서울",
                "career_level": "경력 4~6년",
                "education_level": "석사 이상",
                "position_group": "데이터",
                "position": "데이터 사이언티스트",
                "salary_range": "7500만 ~ 9500만",
                "term_months": 0,
                "status": "PUBLISHED",
                "vector": {
                    "vector_roles": [0.78, 0.86, 0.91, 0.73, 0.68],
                    "vector_skills": [0.83, 0.88, 0.95, 0.86, 0.76],
                    "vector_growth": [0.88, 0.83, 0.91, 0.93, 0.80],
                    "vector_career": [0.73, 0.78, 0.86, 0.83, 0.88],
                    "vector_vision": [0.86, 0.83, 0.90, 0.78, 0.83],
                    "vector_culture": [0.80, 0.86, 0.83, 0.88, 0.73],
                },
                "cards": [
                    {
                        "category": "roles",
                        "title": "머신러닝 모델 개발",
                        "description": "추천 시스템, 검색 알고리즘 등 ML 모델을 개발합니다.",
                        "keywords": ["Machine Learning", "Python", "TensorFlow", "Recommendation"]
                    },
                    {
                        "category": "growth",
                        "title": "최신 기술 적용",
                        "description": "최신 AI/ML 기술을 실제 서비스에 적용할 수 있습니다.",
                        "keywords": ["AI", "Deep Learning", "Research", "Innovation"]
                    }
                ]
            }
        ]
    },
    {
        "id": 5,
        "email": "company05@fitconnect.test",
        "name": "HR솔루션",
        "industry": "컨설팅",
        "size": "51~200명",
        "location_city": "서울",
        "job_postings": [
            {
                "id": 9,
                "title": "B2B 영업 담당자 모집",
                "employment_type": "정규직",
                "location_city": "서울",
                "career_level": "경력 3~5년",
                "education_level": "학력무관",
                "position_group": "영업",
                "position": "B2B 영업",
                "salary_range": "5000만 ~ 7000만",
                "term_months": 0,
                "status": "PUBLISHED",
                "vector": {
                    "vector_roles": [0.71, 0.76, 0.81, 0.71, 0.95],
                    "vector_skills": [0.76, 0.71, 0.86, 0.81, 0.95],
                    "vector_growth": [0.81, 0.86, 0.76, 0.81, 0.91],
                    "vector_career": [0.86, 0.81, 0.76, 0.71, 0.95],
                    "vector_vision": [0.91, 0.86, 0.81, 0.76, 0.95],
                    "vector_culture": [0.95, 0.91, 0.86, 0.81, 0.91],
                },
                "cards": [
                    {
                        "category": "roles",
                        "title": "기업 영업 전문",
                        "description": "HR 솔루션 B2B 영업을 담당합니다.",
                        "keywords": ["B2B Sales", "Enterprise", "HR Tech", "SaaS"]
                    },
                    {
                        "category": "culture",
                        "title": "성과 중심 문화",
                        "description": "명확한 성과 보상 체계와 인센티브 제공",
                        "keywords": ["Incentive", "Performance", "Bonus", "Growth"]
                    }
                ]
            },
            {
                "id": 10,
                "title": "HR 매니저 채용",
                "employment_type": "정규직",
                "location_city": "서울",
                "career_level": "경력 4~6년",
                "education_level": "대졸 이상",
                "position_group": "인사",
                "position": "HR 매니저",
                "salary_range": "5500만 ~ 7500만",
                "term_months": 0,
                "status": "PUBLISHED",
                "vector": {
                    "vector_roles": [0.68, 0.73, 0.78, 0.86, 0.90],
                    "vector_skills": [0.73, 0.76, 0.81, 0.88, 0.93],
                    "vector_growth": [0.80, 0.83, 0.76, 0.86, 0.83],
                    "vector_career": [0.86, 0.80, 0.73, 0.83, 0.90],
                    "vector_vision": [0.83, 0.86, 0.78, 0.80, 0.88],
                    "vector_culture": [0.93, 0.88, 0.86, 0.83, 0.90],
                },
                "cards": [
                    {
                        "category": "roles",
                        "title": "인사 전략 수립",
                        "description": "채용, 교육, 평가 등 전반적인 HR 업무를 담당합니다.",
                        "keywords": ["Recruiting", "Training", "Performance", "Culture"]
                    },
                    {
                        "category": "career",
                        "title": "HR 전문가 성장",
                        "description": "HR 전문성을 키울 수 있는 다양한 프로젝트 경험",
                        "keywords": ["HR Strategy", "People", "Organization", "Development"]
                    }
                ]
            }
        ]
    },
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 유틸리티 함수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def calculate_cosine_similarity(vec1: List[float], vec2: List[float]) -> Optional[float]:
    """두 벡터 간의 코사인 유사도 계산 (-1~1 범위)"""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return None
    
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
        
        # 딕셔너리에서 벡터 추출
        if isinstance(talent_data, dict):
            talent_vec = talent_data.get("vector", [])
        else:
            talent_vec = []
            
        if isinstance(company_data, dict):
            company_vec = company_data.get("vector", [])
        else:
            company_vec = []
        
        if not talent_vec or not company_vec or len(talent_vec) != len(company_vec):
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
            continue
    
    # 전체 평균 점수
    field_scores["total_score"] = sum(valid_scores) / len(valid_scores) if valid_scores else 0.0
    return field_scores



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎯 데이터 생성 함수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def create_talent_users(db: Session) -> List[Dict]:
    """👤 인재 유저 10명 생성"""
    print("━" * 60)
    print("👤 인재 유저 생성 중...")
    print("━" * 60)
    
    created_talents = []
    
    for talent_data in MOCK_TALENTS:
        # 1. User 생성
        user = User(
            email=talent_data["email"],
            password_hash=hash_password("password123"),
            role="talent",
        )
        db.add(user)
        db.flush()
        
        # 2. TalentProfile 생성
        profile = TalentProfile(
            user_id=user.id,
            name=talent_data["name"],
            email=talent_data["email"],
            tagline=talent_data["tagline"],
            desired_role=talent_data["desired_role"],
            desired_salary=talent_data["desired_salary"],
            desired_industry=talent_data["desired_industry"],
            desired_company_size=talent_data["desired_company_size"],
            residence_location=talent_data["residence_location"],
            desired_work_location=talent_data["desired_work_location"],
        )
        db.add(profile)
        db.flush()
        
        # 3. MatchingVector 생성
        vector = MatchingVector(
            user_id=user.id,
            role="talent",
            vector_roles={"dim": 5, "vector": talent_data["vector"]["vector_roles"]},
            vector_skills={"dim": 5, "vector": talent_data["vector"]["vector_skills"]},
            vector_growth={"dim": 5, "vector": talent_data["vector"]["vector_growth"]},
            vector_career={"dim": 5, "vector": talent_data["vector"]["vector_career"]},
            vector_vision={"dim": 5, "vector": talent_data["vector"]["vector_vision"]},
            vector_culture={"dim": 5, "vector": talent_data["vector"]["vector_culture"]},
        )
        db.add(vector)
        db.flush()
        
        # 4. TalentCard 생성 (1개 - unique constraint)
        card = TalentCard(
            user_id=user.id,
            header_title=talent_data["name"],
            badge_title=talent_data["desired_role"],
            badge_years=5,  # 경력 5년으로 통일
            badge_employment="정규직",
            headline=talent_data["tagline"],
            experiences=[
                f"{talent_data['desired_role']} 경력",
                f"{talent_data['desired_industry']} 분야 전문",
            ],
            strengths=[
                "문제 해결 능력",
                "커뮤니케이션",
                "빠른 학습",
            ],
            general_capabilities=[
                {"name": "협업", "level": "상"},
                {"name": "리더십", "level": "중"},
            ],
            job_skills=[
                {"name": skill, "proficiency": "고급"} 
                for skill in talent_data["cards"][0]["keywords"][:3]
            ],
            performance_summary=talent_data["cards"][0]["description"],
            collaboration_style="적극적인 커뮤니케이션과 팀워크 중시",
            growth_potential=talent_data.get("cards", [{}])[1].get("description", "지속적인 성장을 추구합니다") if len(talent_data["cards"]) > 1 else "지속적인 성장을 추구합니다",
        )
        db.add(card)
        
        created_talents.append({
            "user_id": user.id,
            "name": talent_data["name"],
            "email": talent_data["email"],
            "vector_id": vector.id,
        })
        
        print(f"  ✓ {talent_data['name']} ({talent_data['email']})")
    
    db.commit()
    print(f"\n✅ 인재 유저 {len(created_talents)}명 생성 완료!\n")
    return created_talents


def create_company_users(db: Session) -> List[Dict]:
    """🏢 기업 유저 5개 생성 (각 2개 채용공고)"""
    print("━" * 60)
    print("🏢 기업 유저 생성 중...")
    print("━" * 60)
    
    created_companies = []
    
    for company_data in MOCK_COMPANIES:
        # 1. User 생성
        user = User(
            email=company_data["email"],
            password_hash=hash_password("password123"),
            role="company",
        )
        db.add(user)
        db.flush()
        
        # 2. Company 생성
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
        
        job_postings_info = []
        
        # 3. JobPosting 및 관련 데이터 생성
        for jp_data in company_data["job_postings"]:
            # 3-1. JobPosting 생성
            job_posting = JobPosting(
                company_id=company.id,
                title=jp_data["title"],
                employment_type=jp_data["employment_type"],
                location_city=jp_data["location_city"],
                career_level=jp_data["career_level"],
                education_level=jp_data["education_level"],
                position_group=jp_data["position_group"],
                position=jp_data["position"],
                salary_range=jp_data["salary_range"],
                term_months=jp_data["term_months"],
                status=jp_data["status"],
            )
            db.add(job_posting)
            db.flush()
            
            # 3-2. MatchingVector 생성
            vector = MatchingVector(
                user_id=user.id,
                role="company",
                job_posting_id=job_posting.id,
                vector_roles={"dim": 5, "vector": jp_data["vector"]["vector_roles"]},
                vector_skills={"dim": 5, "vector": jp_data["vector"]["vector_skills"]},
                vector_growth={"dim": 5, "vector": jp_data["vector"]["vector_growth"]},
                vector_career={"dim": 5, "vector": jp_data["vector"]["vector_career"]},
                vector_vision={"dim": 5, "vector": jp_data["vector"]["vector_vision"]},
                vector_culture={"dim": 5, "vector": jp_data["vector"]["vector_culture"]},
            )
            db.add(vector)
            db.flush()
            
            # 3-3. JobPostingCard 생성 (1개)
            card = JobPostingCard(
                job_posting_id=job_posting.id,
                header_title=company_data["name"],
                badge_role=jp_data["position"],
                deadline_date=None,  # 상시 채용
                headline=jp_data["title"],
                posting_info={
                    "employment_type": jp_data["employment_type"],
                    "location": jp_data["location_city"],
                    "salary": jp_data["salary_range"],
                    "career_level": jp_data["career_level"],
                },
                responsibilities=[
                    f"{jp_data['position']} 업무 수행",
                    "팀과 협업하여 프로젝트 진행",
                ],
                requirements=[
                    f"{jp_data['career_level']} 경력",
                    f"{jp_data['education_level']} 학력",
                ],
                required_competencies=[
                    keyword for keyword in jp_data["cards"][0]["keywords"][:3]
                ],
                company_info=f"{company_data['name']}은(는) {company_data['industry']} 분야의 {company_data['size']} 규모 기업입니다.",
                talent_persona=jp_data["cards"][0]["description"],
                challenge_task=jp_data.get("cards", [{}])[1].get("description", "함께 성장할 인재를 찾습니다") if len(jp_data["cards"]) > 1 else "함께 성장할 인재를 찾습니다",
            )
            db.add(card)
            
            job_postings_info.append({
                "job_posting_id": job_posting.id,
                "title": jp_data["title"],
                "vector_id": vector.id,
            })
        
        created_companies.append({
            "user_id": user.id,
            "company_id": company.id,
            "name": company_data["name"],
            "email": company_data["email"],
            "job_postings": job_postings_info,
        })
        
        print(f"  ✓ {company_data['name']} ({company_data['email']})")
        for jp in job_postings_info:
            print(f"      - {jp['title']} (ID: {jp['job_posting_id']})")
    
    db.commit()
    print(f"\n✅ 기업 {len(created_companies)}개, 채용공고 {sum(len(c['job_postings']) for c in created_companies)}개 생성 완료!\n")
    return created_companies


def generate_matching_results(db: Session, talents: List[Dict], companies: List[Dict]) -> int:
    """🔗 매칭 결과 생성 (모든 인재 x 모든 채용공고)"""
    print("━" * 60)
    print("🔗 매칭 결과 생성 중...")
    print("━" * 60)
    
    created_count = 0
    
    for talent in talents:
        talent_vector = db.query(MatchingVector).filter(
            MatchingVector.user_id == talent["user_id"],
            MatchingVector.role == "talent"
        ).first()
        
        if not talent_vector:
            print(f"  ⚠️  {talent['name']}: 벡터 없음 - 스킵")
            continue
        
        for company in companies:
            for jp_info in company["job_postings"]:
                company_vector = db.query(MatchingVector).filter(
                    MatchingVector.job_posting_id == jp_info["job_posting_id"],
                    MatchingVector.role == "company"
                ).first()
                
                if not company_vector:
                    print(f"  ⚠️  {company['name']} - {jp_info['title']}: 벡터 없음 - 스킵")
                    continue
                
                # 매칭 점수 계산
                scores = calculate_matching_scores(talent_vector, company_vector)
                
                if scores["total_score"] == 0.0:
                    print(f"  ⚠️  {talent['name']} ↔ {jp_info['title']}: 유효한 점수 없음 - 스킵")
                    continue
                
                # MatchingResult 생성
                matching_result = MatchingResult(
                    talent_vector_id=talent_vector.id,
                    company_vector_id=company_vector.id,
                    talent_user_id=talent["user_id"],
                    company_user_id=company["user_id"],
                    job_posting_id=jp_info["job_posting_id"],
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
                
                print(f"  ✓ {talent['name']} ↔ {company['name']}: {jp_info['title']} = {scores['total_score']:.1f}점")
    
    db.commit()
    print(f"\n✅ 매칭 결과 {created_count}개 생성 완료!\n")
    return created_count



# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 메인 실행 함수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="FitConnect Mock 데이터 생성 스크립트")
    parser.add_argument("--clean", action="store_true", help="기존 Mock 데이터 삭제 후 생성")
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("🎭 FitConnect Mock 데이터 생성 스크립트")
    print("=" * 60)
    print()
    
    db = SessionLocal()
    
    try:
        # 1. 기존 데이터 삭제 (--clean 옵션 사용 시)
        if args.clean:
            clean_existing_data(db)
        
        # 2. 인재 유저 생성 (10명)
        talents = create_talent_users(db)
        
        # 3. 기업 유저 생성 (5개, 각 2개 채용공고)
        companies = create_company_users(db)
        
        # 4. 매칭 결과 생성 (모든 조합)
        matching_count = generate_matching_results(db, talents, companies)
        
        # 5. 최종 요약
        print("=" * 60)
        print("✨ Mock 데이터 생성 완료!")
        print("=" * 60)
        print()
        print("📊 생성된 데이터 요약:")
        print(f"  🧑 인재 유저: {len(talents)}명")
        print(f"  🏢 기업 유저: {len(companies)}개")
        print(f"  📝 채용 공고: {sum(len(c['job_postings']) for c in companies)}개")
        print(f"  📇 인재 카드: {len(talents)}개 (인재당 1개)")
        print(f"  📇 공고 카드: {sum(len(c['job_postings']) for c in companies)}개 (공고당 1개)")
        print(f"  📈 매칭 벡터: {len(talents) + sum(len(c['job_postings']) for c in companies)}개")
        print(f"  🔗 매칭 결과: {matching_count}개")
        print()
        print("🔐 로그인 정보:")
        print("  📧 이메일: talent01@fitconnect.test ~ talent10@fitconnect.test")
        print("  📧 이메일: company01@fitconnect.test ~ company05@fitconnect.test")
        print("  🔑 비밀번호: password123 (모든 계정 공통)")
        print()
        print("🧪 테스트 방법:")
        print("  1️⃣  인재 로그인:")
        print("     POST /auth/login")
        print("     Body: {\"email\": \"talent01@fitconnect.test\", \"password\": \"password123\"}")
        print()
        print("  2️⃣  인재 프로필 조회 (공개):")
        print("     GET /api/talents/{user_id}/profile")
        print()
        print("  3️⃣  매칭 결과 확인 (인재):")
        print("     GET /api/matching-results/talents/{user_id}/job-postings")
        print()
        print("  4️⃣  채용공고 조회 (공개):")
        print("     GET /api/job-postings/{job_posting_id}")
        print()
        print("  5️⃣  매칭 결과 확인 (기업):")
        print("     GET /api/matching-results/job-postings/{job_posting_id}/talents")
        print()
        print("=" * 60)
        print("✅ 모든 작업이 완료되었습니다!")
        print("=" * 60)
        print()
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
