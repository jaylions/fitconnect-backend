from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class JobPostingCreateIn(BaseModel):
    """채용 공고 생성 요청 스키마"""
    
    # === 필수 항목 ===
    title: str = Field(min_length=1, description="공고 제목")
    employment_type: str = Field(description="고용 형태 (예: 정규직, 계약직, 파견직, 인턴, 임시직, 기타)")
    location_city: str = Field(description="근무 지역 (예: 서울, 경기, 인천, 부산, 대구, 대전, 광주, 울산, 강원, 충북, 충남, 전북, 전남, 경북, 경남)")
    career_level: str = Field(min_length=1, description="경력 수준 (예: 신입, 경력 3년, 5년 이상)")
    education_level: str = Field(min_length=1, description="학력 수준 (예: 학력무관, 고졸, 대졸)")

    # === 포지션 정보 ===
    position_group: Optional[str] = Field(None, description="포지션 그룹 (예: 개발)")
    position: Optional[str] = Field(None, description="세부 포지션 (예: 백엔드 개발자)")
    department: Optional[str] = Field(None, description="부서명")

    # === 근무 조건 ===
    start_date: Optional[str] = Field(None, description="입사 희망일 (예: 2025-11-15 또는 협의 후 결정)")
    term_months: Optional[str] = Field(None, description="계약 기간 (예: 12개월, 협의 후 결정)")
    salary_range: Optional[str] = Field(None, description="연봉 범위 (예: 2000만 ~ 3000만, 5000만 ~ 6000만)")

    # === 연락처 및 기한 ===
    homepage_url: Optional[str] = Field(None, description="회사 홈페이지 URL")
    deadline_date: Optional[date] = Field(None, description="지원 마감일")
    contact_email: Optional[str] = Field(None, description="담당자 이메일")
    contact_phone: Optional[str] = Field(None, description="담당자 연락처")

    # === 상세 내용 ===
    responsibilities: Optional[str] = Field(None, description="주요 업무 (줄바꿈 가능)")
    requirements_must: Optional[str] = Field(None, description="필수 요구사항 (줄바꿈 가능)")
    requirements_nice: Optional[str] = Field(None, description="우대 사항 (줄바꿈 가능)")
    competencies: Optional[str] = Field(None, description="필요 역량/기술 스택")

    # === 첨부 파일 ===
    jd_file_id: Optional[str] = Field(None, description="JD 파일 ID")
    extra_file_id: Optional[str] = Field(None, description="추가 파일 ID")

    # === 공고 상태 ===
    status: Optional[str] = Field(None, description="공고 상태 (예: DRAFT, PUBLISHED, CLOSED, ARCHIVED, 기본값: DRAFT)")
    
    # Deprecated aliases (하위 호환성 유지)
    join: Optional[date] = Field(None, deprecated=True, description="입사 희망일 (start_date 사용 권장)")
    period: Optional[str] = Field(None, deprecated=True, description="계약 기간 (term_months 사용 권장)")

    model_config = ConfigDict(json_schema_extra={
        "examples": [
            {
                "title": "백엔드 개발자 (Python/FastAPI)",
                "employment_type": "정규직",
                "location_city": "서울",
                "career_level": "경력 3년 이상",
                "education_level": "학력무관",
                "position_group": "개발",
                "position": "백엔드 개발자",
                "department": "플랫폼팀",
                "start_date": "2025-11-15",
                "term_months": "정규직 (기간 제한 없음)",
                "salary_range": "7000만 ~ 8000만",
                "homepage_url": "https://company.example.com",
                "deadline_date": "2025-10-31",
                "contact_email": "hr@company.example.com",
                "contact_phone": "010-1234-5678",
                "responsibilities": "- 서비스 백엔드 API 개발 및 운영\n- 데이터베이스 설계 및 최적화\n- 성능 모니터링 및 개선",
                "requirements_must": "- Python, FastAPI 실무 경험 3년 이상\n- MySQL/PostgreSQL 등 RDBMS 설계 경험\n- RESTful API 설계 및 개발 경험",
                "requirements_nice": "- AWS, GCP 등 클라우드 인프라 경험\n- Docker, Kubernetes 사용 경험\n- CI/CD 파이프라인 구축 경험",
                "competencies": "Python, FastAPI, SQLAlchemy, MySQL, Docker, AWS",
                "jd_file_id": "file_abc123",
                "extra_file_id": "file_xyz789",
                "status": "DRAFT"
            },
            {
                "title": "프론트엔드 개발 인턴",
                "employment_type": "인턴",
                "location_city": "경기",
                "career_level": "신입/인턴",
                "education_level": "대학 재학 이상",
                "position_group": "개발",
                "position": "프론트엔드 개발자",
                "start_date": "2025-12-01",
                "term_months": "6개월 (정규직 전환 가능)",
                "salary_range": "2000만 ~ 3000만",
                "deadline_date": "2025-11-15",
                "contact_email": "intern@company.example.com",
                "responsibilities": "- React 기반 웹 애플리케이션 개발\n- UI/UX 개선 작업\n- 코드 리뷰 및 학습",
                "requirements_must": "- JavaScript, React 기본 지식\n- HTML/CSS 활용 능력\n- Git 사용 경험",
                "requirements_nice": "- TypeScript 경험\n- 개인/팀 프로젝트 경험",
                "competencies": "JavaScript, React, HTML, CSS",
                "status": "PUBLISHED"
            }
        ]
    })


class JobPostingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    title: str
    position_group: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    employment_type: str  # String 타입
    location_city: str
    salary_range: Optional[str] = None
    career_level: str
    education_level: str
    start_date: Optional[str] = None  # String 타입으로 변경
    term_months: Optional[str] = None
    homepage_url: Optional[str] = None
    deadline_date: Optional[date] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    responsibilities: Optional[str] = None
    requirements_must: Optional[str] = None
    requirements_nice: Optional[str] = None
    competencies: Optional[str] = None
    status: str
    jd_file_id: Optional[str] = None
    extra_file_id: Optional[str] = None
    published_at: Optional[str] = None
    closed_at: Optional[str] = None
    deleted_at: Optional[str] = None
    created_at: str
    updated_at: str
