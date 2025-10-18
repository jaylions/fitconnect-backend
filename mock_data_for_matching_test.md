# 매칭 성능 평가용 Mock Data

## 📋 개요
- **탤런트**: 5명 (FE 개발자, BE 개발자, 마케터, PM, 영업)
- **기업**: 5개 (각 직무에 맞는 공고 작성)
- **목적**: 벡터 매칭 성능 평가

---

## 👤 탤런트 Mock Data

### 1. Frontend 개발자 - 김민수

#### 프로필 생성 (POST /api/me/talent/full)
```json
{
  "basic": {
    "name": "김민수",
    "email": "minsu.kim@example.com",
    "birth_date": "1995-03-15",
    "phone": "010-1234-5001",
    "tagline": "React 전문 Frontend Developer",
    "is_submitted": false
  },
  "educations": [
    {
      "school_name": "서울대학교",
      "major": "컴퓨터공학",
      "status": "졸업",
      "start_ym": "2014-03",
      "end_ym": "2018-02"
    }
  ],
  "experiences": [
    {
      "company_name": "네이버",
      "title": "Frontend Engineer",
      "start_ym": "2018-03",
      "end_ym": "2023-08",
      "leave_reason": "이직",
      "summary": "React 기반 웹 서비스 개발 및 성능 최적화. 월간 활성 사용자 500만 서비스 개발 및 유지보수"
    }
  ],
  "activities": [
    {
      "name": "React 오픈소스 기여",
      "category": "오픈소스",
      "period_ym": "2020-01",
      "description": "React 관련 오픈소스 프로젝트 기여 및 유지보수, 커뮤니티 활동"
    }
  ],
  "certifications": [
    {
      "name": "정보처리기사",
      "score_or_grade": "합격",
      "acquired_ym": "2017-11"
    }
  ],
  "documents": [],
  "submit": true
}
```

#### 매칭 벡터 생성 (POST /api/me/matching-vectors)
```json
{
  "role": "talent",
  "vector_roles": {"vector": [0.9, 0.8, 0.7, 0.6, 0.5]},
  "vector_skills": {"vector": [0.95, 0.9, 0.85, 0.8, 0.75]},
  "vector_growth": {"vector": [0.8, 0.7, 0.75, 0.85, 0.7]},
  "vector_career": {"vector": [0.7, 0.8, 0.6, 0.75, 0.85]},
  "vector_vision": {"vector": [0.85, 0.8, 0.75, 0.7, 0.8]},
  "vector_culture": {"vector": [0.8, 0.85, 0.7, 0.75, 0.9]}
}
```

---

### 2. Backend 개발자 - 박지현

#### 프로필 생성 (POST /api/me/talent/full)
```json
{
  "basic": {
    "name": "박지현",
    "email": "jihyun.park@example.com",
    "birth_date": "1993-07-22",
    "phone": "010-1234-5002",
    "tagline": "Java/Spring 전문 Backend Developer",
    "is_submitted": false
  },
  "educations": [
    {
      "school_name": "KAIST",
      "major": "전산학부",
      "status": "졸업",
      "start_ym": "2016-03",
      "end_ym": "2018-02"
    }
  ],
  "experiences": [
    {
      "company_name": "카카오",
      "title": "Backend Engineer",
      "start_ym": "2018-03",
      "end_ym": "2024-09",
      "leave_reason": "커리어 성장",
      "summary": "Java/Spring 기반 대규모 트래픽 처리 시스템 설계 및 구축. 일 평균 1억 건 이상 요청 처리"
    }
  ],
  "activities": [
    {
      "name": "Spring One 2023 참석",
      "category": "컨퍼런스",
      "period_ym": "2023-08",
      "description": "Spring Framework 최신 트렌드 학습 및 네트워킹"
    }
  ],
  "certifications": [
    {
      "name": "AWS Solutions Architect - Professional",
      "score_or_grade": "합격",
      "acquired_ym": "2022-06"
    }
  ],
  "documents": [],
  "submit": true
}
```

#### 매칭 벡터 생성 (POST /api/me/matching-vectors)
```json
{
  "role": "talent",
  "vector_roles": {"vector": [0.85, 0.9, 0.8, 0.75, 0.7]},
  "vector_skills": {"vector": [0.9, 0.95, 0.85, 0.9, 0.8]},
  "vector_growth": {"vector": [0.9, 0.85, 0.8, 0.9, 0.75]},
  "vector_career": {"vector": [0.8, 0.85, 0.75, 0.8, 0.9]},
  "vector_vision": {"vector": [0.88, 0.82, 0.78, 0.85, 0.9]},
  "vector_culture": {"vector": [0.75, 0.8, 0.85, 0.9, 0.7]}
}
```

---

### 3. 마케터 - 이서연

#### 프로필 생성 (POST /api/me/talent/full)
```json
{
  "basic": {
    "name": "이서연",
    "email": "seoyeon.lee@example.com",
    "birth_date": "1996-11-08",
    "phone": "010-1234-5003",
    "tagline": "데이터 기반 Performance Marketer",
    "is_submitted": false
  },
  "educations": [
    {
      "school_name": "연세대학교",
      "major": "경영학",
      "status": "졸업",
      "start_ym": "2015-03",
      "end_ym": "2019-02"
    }
  ],
  "experiences": [
    {
      "company_name": "쿠팡",
      "title": "Performance Marketer",
      "start_ym": "2019-03",
      "end_ym": "2024-08",
      "leave_reason": "새로운 도전",
      "summary": "디지털 광고 캠페인 기획 및 성과 분석. ROI 200% 달성, 연간 광고비 30억 관리"
    }
  ],
  "activities": [
    {
      "name": "우수 마케터 상 수상",
      "category": "수상",
      "period_ym": "2023-12",
      "description": "한국마케팅협회 주관, 혁신적인 디지털 마케팅 캠페인으로 수상"
    }
  ],
  "certifications": [
    {
      "name": "Google Ads 인증",
      "score_or_grade": "Professional",
      "acquired_ym": "2021-03"
    }
  ],
  "documents": [],
  "submit": true
}
```

#### 매칭 벡터 생성 (POST /api/me/matching-vectors)
```json
{
  "role": "talent",
  "vector_roles": {"vector": [0.75, 0.8, 0.85, 0.7, 0.9]},
  "vector_skills": {"vector": [0.8, 0.75, 0.9, 0.85, 0.7]},
  "vector_growth": {"vector": [0.85, 0.9, 0.8, 0.75, 0.8]},
  "vector_career": {"vector": [0.7, 0.75, 0.8, 0.85, 0.7]},
  "vector_vision": {"vector": [0.9, 0.85, 0.8, 0.75, 0.85]},
  "vector_culture": {"vector": [0.85, 0.9, 0.75, 0.8, 0.85]}
}
```

---

### 4. Product Manager - 최동욱

#### 프로필 생성 (POST /api/me/talent/full)
```json
{
  "basic": {
    "name": "최동욱",
    "email": "dongwook.choi@example.com",
    "birth_date": "1992-05-14",
    "phone": "010-1234-5004",
    "tagline": "0→1 제품 경험 보유 Senior PM",
    "is_submitted": false
  },
  "educations": [
    {
      "school_name": "고려대학교",
      "major": "경영학",
      "status": "졸업",
      "start_ym": "2011-03",
      "end_ym": "2015-02"
    },
    {
      "school_name": "Stanford University",
      "major": "MBA",
      "status": "졸업",
      "start_ym": "2015-09",
      "end_ym": "2017-06"
    }
  ],
  "experiences": [
    {
      "company_name": "토스",
      "title": "Senior Product Manager",
      "start_ym": "2017-07",
      "end_ym": "2024-10",
      "leave_reason": "새로운 도전",
      "summary": "금융 플랫폼 신규 서비스 기획 및 런칭. MAU 500만 달성, 연 거래액 10조 달성"
    }
  ],
  "activities": [
    {
      "name": "핀테크 스타트업 자문",
      "category": "자문",
      "period_ym": "2022-01",
      "description": "5개 핀테크 스타트업 제품 전략 및 그로스 자문 활동"
    }
  ],
  "certifications": [
    {
      "name": "Certified Scrum Product Owner (CSPO)",
      "score_or_grade": "Certified",
      "acquired_ym": "2019-08"
    }
  ],
  "documents": [],
  "submit": true
}
```

#### 매칭 벡터 생성 (POST /api/me/matching-vectors)
```json
{
  "role": "talent",
  "vector_roles": {"vector": [0.9, 0.85, 0.8, 0.9, 0.75]},
  "vector_skills": {"vector": [0.85, 0.8, 0.9, 0.85, 0.8]},
  "vector_growth": {"vector": [0.9, 0.9, 0.85, 0.8, 0.85]},
  "vector_career": {"vector": [0.85, 0.9, 0.8, 0.85, 0.9]},
  "vector_vision": {"vector": [0.95, 0.9, 0.85, 0.9, 0.85]},
  "vector_culture": {"vector": [0.8, 0.85, 0.9, 0.85, 0.8]}
}
```

---

### 5. 영업 - 정수진

#### 프로필 생성 (POST /api/me/talent/full)
```json
{
  "basic": {
    "name": "정수진",
    "email": "sujin.jung@example.com",
    "birth_date": "1994-09-30",
    "phone": "010-1234-5005",
    "tagline": "글로벌 B2B 영업 전문가",
    "is_submitted": false
  },
  "educations": [
    {
      "school_name": "이화여자대학교",
      "major": "국제사무학",
      "status": "졸업",
      "start_ym": "2013-03",
      "end_ym": "2017-02"
    }
  ],
  "experiences": [
    {
      "company_name": "삼성전자",
      "title": "B2B Sales Manager",
      "start_ym": "2017-03",
      "end_ym": "2024-09",
      "leave_reason": "커리어 도약",
      "summary": "글로벌 기업 대상 솔루션 영업. 연 매출 100억 달성, 주요 고객 30개사 관리"
    }
  ],
  "activities": [
    {
      "name": "올해의 영업사원 수상",
      "category": "수상",
      "period_ym": "2023-01",
      "description": "삼성전자 최고 매출 실적 달성으로 사내 우수 영업사원 선정"
    }
  ],
  "certifications": [
    {
      "name": "Salesforce Certified Administrator",
      "score_or_grade": "Certified",
      "acquired_ym": "2020-11"
    }
  ],
  "documents": [],
  "submit": true
}
```

#### 매칭 벡터 생성 (POST /api/me/matching-vectors)
```json
{
  "role": "talent",
  "vector_roles": {"vector": [0.8, 0.75, 0.9, 0.85, 0.7]},
  "vector_skills": {"vector": [0.75, 0.8, 0.85, 0.9, 0.75]},
  "vector_growth": {"vector": [0.8, 0.85, 0.75, 0.8, 0.9]},
  "vector_career": {"vector": [0.85, 0.8, 0.75, 0.9, 0.8]},
  "vector_vision": {"vector": [0.8, 0.85, 0.9, 0.8, 0.75]},
  "vector_culture": {"vector": [0.9, 0.85, 0.8, 0.75, 0.85]}
}
```

---

## 🏢 기업 Mock Data

### 1. 테크스타트업 - 프론트엔드 개발자 채용

#### 회사 프로필 생성 (POST /api/me/company/full)
```json
{
  "basic": {
    "name": "퓨처테크",
    "industry": "IT/소프트웨어",
    "size": "50 ~ 100명",
    "location_city": "서울시 강남구",
    "homepage_url": "https://futuretech.example.com",
    "career_page_url": "https://futuretech.example.com/careers",
    "one_liner": "AI 기반 차세대 SaaS 플랫폼"
  },
  "about": {
    "vision_mission": "AI 기술로 업무 생산성을 혁신합니다",
    "business_domains": "B2B SaaS, AI 솔루션",
    "ideal_talent": "빠르게 성장하는 스타트업 환경에서 주도적으로 일할 수 있는 분",
    "culture": "수평적 문화, 자율과 책임, 빠른 의사결정",
    "benefits": "스톡옵션, 자유로운 휴가, 최신 장비 지원"
  },
  "submit": true
}
```

#### 채용공고 생성 (POST /api/me/company/job-postings)
```json
{
  "title": "Frontend Developer (React/TypeScript)",
  "employment_type": "정규직",
  "location_city": "서울",
  "salary_range": "6000만 ~ 7000만",
  "career_level": "주니어~시니어 (3-7년)",
  "education_level": "학사 이상",
  "position_group": "Engineering",
  "position": "Frontend",
  "department": "Product Development",
  "start_date": "2025-12-01",
  "deadline_date": "2025-11-30",
  "contact_email": "recruit@futuretech.example.com",
  "responsibilities": "- React/TypeScript 기반 웹 애플리케이션 개발\n- UI/UX 개선 및 성능 최적화\n- 디자이너, 백엔드 개발자와 협업",
  "requirements_must": "- React 3년 이상 실무 경험\n- TypeScript 능숙\n- Git/Github 사용 경험",
  "requirements_nice": "- Next.js 경험\n- 테스트 코드 작성 경험\n- 오픈소스 기여 경험",
  "competencies": "React, TypeScript, Next.js, Jest, Git",
  "status": "PUBLISHED"
}
```

#### 매칭 벡터 생성 (POST /api/me/matching-vectors)
```json
{
  "role": "company",
  "vector_roles": {"vector": [0.9, 0.8, 0.7, 0.65, 0.55]},
  "vector_skills": {"vector": [0.95, 0.9, 0.85, 0.8, 0.75]},
  "vector_growth": {"vector": [0.85, 0.75, 0.8, 0.9, 0.7]},
  "vector_career": {"vector": [0.7, 0.8, 0.65, 0.75, 0.85]},
  "vector_vision": {"vector": [0.85, 0.8, 0.75, 0.7, 0.8]},
  "vector_culture": {"vector": [0.8, 0.85, 0.7, 0.75, 0.9]}
}
```

---

### 2. 대기업 - 백엔드 개발자 채용

#### 회사 프로필 생성 (POST /api/me/company/full)
```json
{
  "basic": {
    "name": "글로벌테크",
    "industry": "IT 서비스",
    "size": "1000명 이상",
    "location_city": "서울시 서초구",
    "homepage_url": "https://globaltech.example.com",
    "career_page_url": "https://globaltech.example.com/jobs",
    "one_liner": "글로벌 IT 서비스 리더"
  },
  "about": {
    "vision_mission": "기술로 세상을 연결합니다",
    "business_domains": "클라우드 서비스, 엔터프라이즈 솔루션",
    "ideal_talent": "안정적인 환경에서 대규모 시스템 경험을 쌓고 싶은 분",
    "culture": "체계적인 조직 문화, 워라밸 중시, 교육 지원",
    "benefits": "4대보험, 퇴직연금, 건강검진, 자기계발비 지원"
  },
  "submit": true
}
```

#### 채용공고 생성 (POST /api/me/company/job-postings)
```json
{
  "title": "Backend Engineer (Java/Spring)",
  "employment_type": "정규직",
  "location_city": "서울",
  "salary_range": "8000만 ~ 9000만",
  "career_level": "시니어 (5년 이상)",
  "education_level": "학사 이상",
  "position_group": "Engineering",
  "position": "Backend",
  "department": "Platform Team",
  "start_date": "2026-01-01",
  "deadline_date": "2025-12-15",
  "contact_email": "hr@globaltech.example.com",
  "responsibilities": "- Java/Spring 기반 대규모 트래픽 처리 시스템 설계\n- MSA 아키텍처 구축 및 운영\n- 성능 모니터링 및 최적화",
  "requirements_must": "- Java/Spring 5년 이상 실무 경험\n- 대용량 트래픽 처리 경험\n- RDBMS, NoSQL 설계 경험",
  "requirements_nice": "- Kubernetes, Docker 경험\n- AWS/GCP 인프라 경험\n- 오픈소스 컨트리뷰션",
  "competencies": "Java, Spring Boot, Kubernetes, MySQL, Redis",
  "status": "PUBLISHED"
}
```

#### 매칭 벡터 생성 (POST /api/me/matching-vectors)
```json
{
  "role": "company",
  "vector_roles": {"vector": [0.85, 0.9, 0.8, 0.75, 0.7]},
  "vector_skills": {"vector": [0.9, 0.95, 0.85, 0.9, 0.8]},
  "vector_growth": {"vector": [0.9, 0.85, 0.8, 0.9, 0.75]},
  "vector_career": {"vector": [0.8, 0.85, 0.75, 0.8, 0.9]},
  "vector_vision": {"vector": [0.88, 0.82, 0.78, 0.85, 0.9]},
  "vector_culture": {"vector": [0.75, 0.8, 0.85, 0.9, 0.7]}
}
```

---

### 3. 이커머스 - 마케터 채용

#### 회사 프로필 생성 (POST /api/me/company/full)
```json
{
  "basic": {
    "name": "마켓플러스",
    "industry": "이커머스/유통",
    "size": "500 ~ 1000명",
    "location_city": "서울시 마포구",
    "homepage_url": "https://marketplus.example.com",
    "career_page_url": "https://marketplus.example.com/careers",
    "one_liner": "국내 1위 온라인 쇼핑몰"
  },
  "about": {
    "vision_mission": "모든 사람이 행복한 쇼핑 경험을 만듭니다",
    "business_domains": "온라인 쇼핑몰, 물류, 핀테크",
    "ideal_talent": "데이터 기반으로 성과를 만들어내는 마케터",
    "culture": "성과 중심, 빠른 실행력, 협업 문화",
    "benefits": "인센티브제, 자율 출퇴근, 도서 구입비"
  },
  "submit": true
}
```

#### 채용공고 생성 (POST /api/me/company/job-postings)
```json
{
  "title": "Performance Marketer",
  "employment_type": "정규직",
  "location_city": "서울",
  "salary_range": "5000만 ~ 6000만",
  "career_level": "주니어~미들 (3-5년)",
  "education_level": "학사 이상",
  "position_group": "Marketing",
  "position": "Performance Marketing",
  "department": "Growth Team",
  "start_date": "2025-11-15",
  "deadline_date": "2025-11-10",
  "contact_email": "jobs@marketplus.example.com",
  "responsibilities": "- 디지털 광고 캠페인 기획 및 집행\n- 데이터 분석을 통한 마케팅 성과 개선\n- 마케팅 예산 관리 및 ROI 최적화",
  "requirements_must": "- 퍼포먼스 마케팅 3년 이상 경험\n- Google Ads, Meta Ads 운영 경험\n- 데이터 분석 능력",
  "requirements_nice": "- SQL 활용 가능\n- A/B 테스트 경험\n- 그로스해킹 경험",
  "competencies": "Google Ads, Facebook Ads, GA4, SQL, Excel",
  "status": "PUBLISHED"
}
```

#### 매칭 벡터 생성 (POST /api/me/matching-vectors)
```json
{
  "role": "company",
  "vector_roles": {"vector": [0.75, 0.8, 0.85, 0.7, 0.9]},
  "vector_skills": {"vector": [0.8, 0.75, 0.9, 0.85, 0.7]},
  "vector_growth": {"vector": [0.85, 0.9, 0.8, 0.75, 0.8]},
  "vector_career": {"vector": [0.7, 0.75, 0.8, 0.85, 0.7]},
  "vector_vision": {"vector": [0.9, 0.85, 0.8, 0.75, 0.85]},
  "vector_culture": {"vector": [0.85, 0.9, 0.75, 0.8, 0.85]}
}
```

---

### 4. 핀테크 - PM 채용

#### 회사 프로필 생성 (POST /api/me/company/full)
```json
{
  "basic": {
    "name": "페이플랫폼",
    "industry": "핀테크",
    "size": "100 ~ 200명",
    "location_city": "서울시 강남구",
    "homepage_url": "https://payplatform.example.com",
    "career_page_url": "https://payplatform.example.com/recruit",
    "one_liner": "혁신적인 금융 플랫폼"
  },
  "about": {
    "vision_mission": "모두가 쉽게 사용하는 금융 서비스를 만듭니다",
    "business_domains": "간편결제, 송금, 자산관리",
    "ideal_talent": "금융과 기술을 이해하고 제품을 만들 수 있는 PM",
    "culture": "데이터 기반 의사결정, 빠른 실험, 고객 중심",
    "benefits": "스톡옵션, 원격근무, 교육비 전액 지원"
  },
  "submit": true
}
```

#### 채용공고 생성 (POST /api/me/company/job-postings)
```json
{
  "title": "Senior Product Manager",
  "employment_type": "정규직",
  "location_city": "서울",
  "salary_range": "9000만 ~ 1억",
  "career_level": "시니어 (5-10년)",
  "education_level": "학사 이상 (MBA 우대)",
  "position_group": "Product",
  "position": "Product Manager",
  "department": "Product Team",
  "start_date": "2026-01-01",
  "deadline_date": "2025-12-20",
  "contact_email": "pm-recruit@payplatform.example.com",
  "responsibilities": "- 금융 서비스 신규 기능 기획 및 출시\n- 데이터 기반 제품 의사결정\n- 개발팀, 디자인팀과 협업하여 로드맵 실행",
  "requirements_must": "- PM 경력 5년 이상\n- 금융/핀테크 도메인 이해\n- SQL, 데이터 분석 능력",
  "requirements_nice": "- MBA 학위\n- 0→1 제품 런칭 경험\n- Agile/Scrum 경험",
  "competencies": "Product Strategy, SQL, Jira, Figma, A/B Testing",
  "status": "PUBLISHED"
}
```

#### 매칭 벡터 생성 (POST /api/me/matching-vectors)
```json
{
  "role": "company",
  "vector_roles": {"vector": [0.9, 0.85, 0.8, 0.9, 0.75]},
  "vector_skills": {"vector": [0.85, 0.8, 0.9, 0.85, 0.8]},
  "vector_growth": {"vector": [0.9, 0.9, 0.85, 0.8, 0.85]},
  "vector_career": {"vector": [0.85, 0.9, 0.8, 0.85, 0.9]},
  "vector_vision": {"vector": [0.95, 0.9, 0.85, 0.9, 0.85]},
  "vector_culture": {"vector": [0.8, 0.85, 0.9, 0.85, 0.8]}
}
```

---

### 5. 제조업 - 영업 채용

#### 회사 프로필 생성 (POST /api/me/company/full)
```json
{
  "basic": {
    "name": "글로벌산업",
    "industry": "제조/화학",
    "size": "1000명 이상",
    "location_city": "서울시 송파구",
    "homepage_url": "https://globalindustry.example.com",
    "career_page_url": "https://globalindustry.example.com/careers",
    "one_liner": "글로벌 산업재 선도기업"
  },
  "about": {
    "vision_mission": "기술과 혁신으로 산업을 선도합니다",
    "business_domains": "산업재, 화학제품, B2B 솔루션",
    "ideal_talent": "글로벌 비즈니스 경험과 협상력을 갖춘 영업 전문가",
    "culture": "성과 중심, 글로벌 마인드, 전문성 존중",
    "benefits": "성과급, 법인차량, 해외연수, 건강검진"
  },
  "submit": true
}
```

#### 채용공고 생성 (POST /api/me/company/job-postings)
```json
{
  "title": "B2B Sales Manager",
  "employment_type": "정규직",
  "location_city": "서울",
  "salary_range": "6000만 ~ 7000만",
  "career_level": "시니어 (5년 이상)",
  "education_level": "학사 이상",
  "position_group": "Sales",
  "position": "B2B Sales",
  "department": "Sales Division",
  "start_date": "2025-12-01",
  "deadline_date": "2025-11-25",
  "contact_email": "sales-recruit@globalindustry.example.com",
  "responsibilities": "- 글로벌 B2B 고객 발굴 및 관계 관리\n- 영업 전략 수립 및 실행\n- 계약 협상 및 성사",
  "requirements_must": "- B2B 영업 5년 이상 경험\n- 영어 능통 (비즈니스 레벨)\n- 글로벌 고객 응대 경험",
  "requirements_nice": "- 제조업 도메인 이해\n- CRM 시스템 활용 경험\n- 해외 출장 가능자",
  "competencies": "B2B Sales, Negotiation, CRM, English, Presentation",
  "status": "PUBLISHED"
}
```

#### 매칭 벡터 생성 (POST /api/me/matching-vectors)
```json
{
  "role": "company",
  "vector_roles": {"vector": [0.8, 0.75, 0.9, 0.85, 0.7]},
  "vector_skills": {"vector": [0.75, 0.8, 0.85, 0.9, 0.75]},
  "vector_growth": {"vector": [0.8, 0.85, 0.75, 0.8, 0.9]},
  "vector_career": {"vector": [0.85, 0.8, 0.75, 0.9, 0.8]},
  "vector_vision": {"vector": [0.8, 0.85, 0.9, 0.8, 0.75]},
  "vector_culture": {"vector": [0.9, 0.85, 0.8, 0.75, 0.85]}
}
```

---

## 🧪 매칭 테스트 시나리오

### 1. 높은 매칭 예상
- **김민수 (FE)** ↔ **퓨처테크 (FE 개발자 채용)**: ~95% 이상
- **박지현 (BE)** ↔ **글로벌테크 (BE 개발자 채용)**: ~94% 이상
- **이서연 (마케터)** ↔ **마켓플러스 (마케터 채용)**: ~93% 이상
- **최동욱 (PM)** ↔ **페이플랫폼 (PM 채용)**: ~96% 이상
- **정수진 (영업)** ↔ **글로벌산업 (영업 채용)**: ~92% 이상

### 2. 중간 매칭 예상
- **김민수 (FE)** ↔ **글로벌테크 (BE 개발자)**: ~70-75%
- **박지현 (BE)** ↔ **퓨처테크 (FE 개발자)**: ~72-77%

### 3. 낮은 매칭 예상
- **이서연 (마케터)** ↔ **글로벌테크 (BE 개발자)**: ~50-60%
- **정수진 (영업)** ↔ **퓨처테크 (FE 개발자)**: ~48-55%

---

## 📝 사용 방법

### 1. 탤런트 데이터 생성 순서
```bash
# 각 탤런트별로:
1. 회원가입 완료 (이미 완료된 상태로 가정)
2. POST /api/me/talent/full - 프로필 생성
3. POST /api/me/matching-vectors - 매칭 벡터 생성
4. 응답에서 매칭 벡터 ID 기록
```

### 2. 기업 데이터 생성 순서
```bash
# 각 기업별로:
1. 회원가입 완료 (이미 완료된 상태로 가정)
2. POST /api/me/company/full - 회사 프로필 생성
3. POST /api/me/company/job-postings - 채용공고 생성
4. POST /api/me/matching-vectors - 매칭 벡터 생성
5. 응답에서 매칭 벡터 ID 기록
```

### 3. 매칭 테스트 실행
```bash
# 각 조합별로:
POST /api/matching/vectors
{
  "source_id": <talent_vector_id>,
  "target_id": <company_vector_id>
}
```

### 4. 결과 분석
- 매칭 점수 분포 확인
- 필드별 점수 비교
- 예상 매칭률과 실제 결과 비교

---

## 🎯 테스트 체크리스트

- [ ] 5명의 탤런트 프로필 생성 완료
- [ ] 5명의 탤런트 매칭 벡터 생성 완료
- [ ] 5개 기업 프로필 생성 완료
- [ ] 5개 채용공고 생성 완료
- [ ] 5개 기업 매칭 벡터 생성 완료
- [ ] 25개 조합 (5×5) 매칭 테스트 완료
- [ ] 매칭 점수 분포 분석 완료
- [ ] 성능 평가 리포트 작성 완료

---

**생성일**: 2025-10-17  
**목적**: 벡터 매칭 시스템 성능 평가  
**데이터 구성**: 탤런트 5명, 기업 5개, 총 25개 매칭 조합
