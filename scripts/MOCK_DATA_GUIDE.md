# 🎭 FitConnect Mock 데이터 가이드

> **완벽하게 연결된 Mock 데이터로 전체 시스템 테스트**

## 📊 데이터 구조 개요

```
인재 10명 (talent01~10)
    ├── TalentProfile (기본 정보 + 관심내용)
    ├── TalentCard (1개 - 카드 데이터)
    └── MatchingVector (6차원 벡터)
         └── MatchingResult (100개 - 모든 채용공고와 매칭)

기업 5개 (company01~05)
    ├── Company (기업 정보)
    └── JobPosting (각 2개 = 총 10개)
         ├── JobPostingCard (1개 - 카드 데이터)
         └── MatchingVector (6차원 벡터)
              └── MatchingResult (100개 - 모든 인재와 매칭)
```

## 🚀 빠른 시작

### 1️⃣ Mock 데이터 생성

```bash
# 기존 데이터 삭제 후 생성
poetry run python scripts/seed_mock_data.py --clean

# 추가 생성 (기존 데이터 유지)
poetry run python scripts/seed_mock_data.py
```

### 2️⃣ 생성 결과 확인

```
✅ 생성 완료!
📊 인재 유저: 10명
📊 기업 유저: 5개
📊 채용 공고: 10개
📊 인재 카드: 10개
📊 공고 카드: 10개
📊 매칭 벡터: 20개
📊 매칭 결과: 100개
```

## 👥 인재 데이터 (10명)

| ID | 이메일 | 이름 | 직무 | 희망연봉 | 희망업종 |
|----|--------|------|------|----------|----------|
| 1 | talent01@fitconnect.test | 김민수 | Frontend Developer | 5,000만원 이상 | IT·인터넷 |
| 2 | talent02@fitconnect.test | 박지현 | Backend Developer | 7,000만원 이상 | IT·인터넷 |
| 3 | talent03@fitconnect.test | 이서연 | 마케터 | 4,500만원 이상 | 광고·마케팅 |
| 4 | talent04@fitconnect.test | 김영준 | 프로덕트 매니저 | 8,000만원 이상 | IT·인터넷 |
| 5 | talent05@fitconnect.test | 박진우 | 영업 | 6,000만원 이상 | 제조·유통 |
| 6 | talent06@fitconnect.test | 정수민 | UI/UX Designer | 4,500만원 이상 | IT·인터넷 |
| 7 | talent07@fitconnect.test | 최동현 | DevOps Engineer | 6,500만원 이상 | IT·인터넷 |
| 8 | talent08@fitconnect.test | 한지원 | Data Scientist | 7,500만원 이상 | IT·인터넷 |
| 9 | talent09@fitconnect.test | 강민지 | 콘텐츠 마케터 | 4,000만원 이상 | 미디어·엔터테인먼트 |
| 10 | talent10@fitconnect.test | 오성훈 | HR Manager | 5,500만원 이상 | 컨설팅 |

### 인재별 상세 정보

#### 1. 김민수 (Frontend Developer)
- **Tagline**: React 전문 Frontend 개발자
- **관심내용**:
  - 희망 직무: Frontend Developer
  - 희망 연봉: 5,000만원 이상
  - 희망 업종: IT·인터넷
  - 희망 기업 규모: 51~200명
  - 거주지: 서울 강남구
  - 희망 근무지: 서울 전체
- **카드 정보**:
  - 헤더: 김민수
  - 배지: Frontend Developer / 5년 / 정규직
  - 주요 역량: React, TypeScript, Redux, Next.js
  - 강점: 문제 해결 능력, 커뮤니케이션, 빠른 학습

#### 2. 박지현 (Backend Developer)
- **Tagline**: Java/Spring 백엔드 아키텍트
- **관심내용**:
  - 희망 직무: Backend Developer
  - 희망 연봉: 7,000만원 이상
  - 희망 업종: IT·인터넷
  - 희망 기업 규모: 201~500명
  - 거주지: 서울 서초구
  - 희망 근무지: 서울·경기 전체
- **주요 역량**: Spring Boot, MSA, Docker, Kubernetes, Redis, Kafka

#### 3. 이서연 (퍼포먼스 마케터)
- **Tagline**: 데이터 기반 퍼포먼스 마케터
- **관심내용**:
  - 희망 직무: 마케터
  - 희망 연봉: 4,500만원 이상
  - 희망 업종: 광고·마케팅
  - 희망 기업 규모: 11~50명
  - 거주지: 서울 마포구
  - 희망 근무지: 서울 서부
- **주요 역량**: Google Ads, Facebook Ads, ROAS, GA4, Amplitude

#### 4. 김영준 (Product Manager)
- **Tagline**: Product Manager with Tech Background
- **관심내용**:
  - 희망 직무: 프로덕트 매니저
  - 희망 연봉: 8,000만원 이상
  - 희망 업종: IT·인터넷
  - 희망 기업 규모: 501~1,000명
  - 거주지: 서울 성동구
  - 희망 근무지: 서울 동부
- **주요 역량**: Product Strategy, PMF, A/B Test, Data Analysis

#### 5. 박진우 (B2B 영업)
- **Tagline**: B2B 영업 전문가
- **관심내용**:
  - 희망 직무: 영업
  - 희망 연봉: 6,000만원 이상
  - 희망 업종: 제조·유통
  - 희망 기업 규모: 1,001명 이상
  - 거주지: 경기 성남시
  - 희망 근무지: 경기 전체
- **주요 역량**: B2B Sales, Enterprise, Partnership, CRM

#### 6. 정수민 (UI/UX Designer)
- **관심내용**: UI/UX Designer / 4,500만원 / IT·인터넷
- **주요 역량**: UX Research, Figma, Design System

#### 7. 최동현 (DevOps Engineer)
- **관심내용**: DevOps Engineer / 6,500만원 / IT·인터넷
- **주요 역량**: CI/CD, Kubernetes, AWS, Terraform

#### 8. 한지원 (Data Scientist)
- **관심내용**: Data Scientist / 7,500만원 / IT·인터넷
- **주요 역량**: Machine Learning, Python, TensorFlow, Spark

#### 9. 강민지 (콘텐츠 마케터)
- **관심내용**: 콘텐츠 마케터 / 4,000만원 / 미디어·엔터테인먼트
- **주요 역량**: Social Media, Instagram, Video, Storytelling

#### 10. 오성훈 (HR Manager)
- **관심내용**: HR Manager / 5,500만원 / 컨설팅
- **주요 역량**: Recruiting, Culture, Survey, Retention

## 🏢 기업 데이터 (5개)

| ID | 이메일 | 기업명 | 업종 | 규모 | 채용공고 수 |
|----|--------|--------|------|------|------------|
| 1 | company01@fitconnect.test | 테크이노베이션 | IT·인터넷 | 51~200명 | 2개 |
| 2 | company02@fitconnect.test | 글로벌금융그룹 | 금융 | 501~1,000명 | 2개 |
| 3 | company03@fitconnect.test | 크리에이티브에이전시 | 마케팅·광고 | 11~50명 | 2개 |
| 4 | company04@fitconnect.test | 이커머스플랫폼 | 이커머스 | 201~500명 | 2개 |
| 5 | company05@fitconnect.test | HR솔루션 | 컨설팅 | 51~200명 | 2개 |

## 📝 채용공고 데이터 (10개)

### 테크이노베이션 (company01)

#### 1. React Frontend 개발자 채용 (ID: 51)
- **포지션**: 프론트엔드 개발자
- **경력**: 경력 3~5년
- **연봉**: 5,000만 ~ 6,500만
- **근무지**: 서울
- **고용 형태**: 정규직

#### 2. UI/UX 디자이너 모집 (ID: 52)
- **포지션**: UI/UX 디자이너
- **경력**: 경력 2~4년
- **연봉**: 4,500만 ~ 6,000만
- **근무지**: 서울
- **고용 형태**: 정규직

### 글로벌금융그룹 (company02)

#### 3. Backend 개발자 (Java/Spring) (ID: 53)
- **포지션**: 백엔드 개발자
- **경력**: 경력 5~7년
- **연봉**: 7,000만 ~ 9,000만
- **근무지**: 서울
- **고용 형태**: 정규직

#### 4. DevOps Engineer 채용 (ID: 54)
- **포지션**: DevOps 엔지니어
- **경력**: 경력 4~6년
- **연봉**: 6,500만 ~ 8,500만
- **근무지**: 서울
- **고용 형태**: 정규직

### 크리에이티브에이전시 (company03)

#### 5. 퍼포먼스 마케터 모집 (ID: 55)
- **포지션**: 퍼포먼스 마케터
- **경력**: 경력 3~5년
- **연봉**: 4,500만 ~ 6,000만
- **근무지**: 서울
- **고용 형태**: 정규직

#### 6. 콘텐츠 마케터 채용 (ID: 56)
- **포지션**: 콘텐츠 마케터
- **경력**: 경력 2~4년
- **연봉**: 4,000만 ~ 5,500만
- **근무지**: 서울
- **고용 형태**: 정규직

### 이커머스플랫폼 (company04)

#### 7. Product Manager 모집 (ID: 57)
- **포지션**: 프로덕트 매니저
- **경력**: 경력 5~7년
- **연봉**: 7,000만 ~ 9,000만
- **근무지**: 서울
- **고용 형태**: 정규직

#### 8. Data Scientist 채용 (ID: 58)
- **포지션**: 데이터 사이언티스트
- **경력**: 경력 4~6년
- **연봉**: 7,500만 ~ 9,500만
- **근무지**: 서울
- **고용 형태**: 정규직

### HR솔루션 (company05)

#### 9. B2B 영업 담당자 모집 (ID: 59)
- **포지션**: B2B 영업
- **경력**: 경력 3~5년
- **연봉**: 5,000만 ~ 7,000만
- **근무지**: 서울
- **고용 형태**: 정규직

#### 10. HR 매니저 채용 (ID: 60)
- **포지션**: HR 매니저
- **경력**: 경력 4~6년
- **연봉**: 5,500만 ~ 7,500만
- **근무지**: 서울
- **고용 형태**: 정규직

## 🔗 매칭 결과 (100개)

- **전체 매칭**: 인재 10명 × 채용공고 10개 = 100개
- **매칭 점수 범위**: 99.4 ~ 100.0점
- **최고 매칭 사례**:
  - 김민수 ↔ React Frontend 개발자 채용: **100.0점**
  - 박지현 ↔ Backend 개발자: **100.0점**
  - 이서연 ↔ 퍼포먼스 마케터 모집: **100.0점**
  - 김영준 ↔ Product Manager 모집: **100.0점**
  - 박진우 ↔ B2B 영업 담당자: **100.0점**
  - 정수민 ↔ UI/UX 디자이너 모집: **100.0점**
  - 최동현 ↔ DevOps Engineer 채용: **100.0점**
  - 한지원 ↔ Data Scientist 채용: **100.0점**
  - 강민지 ↔ 콘텐츠 마케터 채용: **100.0점**
  - 오성훈 ↔ HR 매니저 채용: **100.0점**

## 🧪 API 테스트 시나리오

### 1. 인재 로그인 및 프로필 조회

```bash
# 1-1. 로그인
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "talent01@fitconnect.test",
    "password": "password123"
  }'

# 1-2. 인재 프로필 조회 (공개 API)
curl http://localhost:8000/api/talents/1/profile

# 1-3. 인재 카드 조회
curl http://localhost:8000/api/talents/1/card
```

### 2. 매칭 결과 조회 (인재 → 채용공고)

```bash
# 2-1. 김민수의 매칭 결과 조회 (상위 5개)
curl http://localhost:8000/api/matching-results/talents/1/job-postings?limit=5&sort_by=total_score

# 2-2. 특정 채용공고와의 매칭 상세
curl http://localhost:8000/api/matching-results/talents/1/job-postings/51
```

### 3. 채용공고 조회 및 매칭

```bash
# 3-1. 채용공고 상세 조회 (공개 API)
curl http://localhost:8000/api/job-postings/51

# 3-2. 채용공고 카드 조회
curl http://localhost:8000/api/job-postings/51/card

# 3-3. 채용공고의 매칭된 인재 조회 (상위 5명)
curl http://localhost:8000/api/matching-results/job-postings/51/talents?limit=5&sort_by=total_score
```

### 4. 기업 로그인 및 조회

```bash
# 4-1. 기업 로그인
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "company01@fitconnect.test",
    "password": "password123"
  }'

# 4-2. 기업 프로필 조회
curl http://localhost:8000/api/companies/1

# 4-3. 기업의 채용공고 목록
curl http://localhost:8000/api/companies/1/job-postings
```

### 5. 벡터 매칭 테스트

```bash
# 5-1. 인재 벡터 조회
curl http://localhost:8000/api/matching-vectors/talents/1

# 5-2. 채용공고 벡터 조회
curl http://localhost:8000/api/matching-vectors/job-postings/51

# 5-3. 실시간 매칭 점수 계산 (선택적)
curl http://localhost:8000/api/matching/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "talent_user_id": 1,
    "job_posting_id": 51
  }'
```

## 📈 매칭 점수 분포

각 인재는 10개 채용공고와 매칭되며, 평균적으로 다음과 같은 분포를 보입니다:

- **완벽 매칭 (100점)**: 각 인재마다 1개씩 (본인 직무와 정확히 일치)
- **높은 매칭 (99.7~99.9점)**: 3~4개
- **좋은 매칭 (99.4~99.6점)**: 5~6개

### 매칭 점수 계산 방식

```
총점 = (roles + skills + growth + career + vision + culture) / 6

- roles: 역할/직무 적합도
- skills: 기술/역량 적합도  
- growth: 성장 가능성
- career: 경력/커리어 적합도
- vision: 비전/목표 일치도
- culture: 문화/가치관 적합도
```

## 🔐 로그인 정보

### 공통 비밀번호
```
password123
```

### 인재 계정
```
talent01@fitconnect.test ~ talent10@fitconnect.test
```

### 기업 계정
```
company01@fitconnect.test ~ company05@fitconnect.test
```

## 🎯 테스트 체크리스트

### ✅ 인재 관련
- [ ] 인재 프로필 조회 (공개 API)
- [ ] 인재 카드 조회
- [ ] 인재의 매칭 결과 목록
- [ ] 특정 채용공고와의 매칭 상세
- [ ] 관심내용 필드 확인 (6개)

### ✅ 기업 관련
- [ ] 채용공고 조회 (공개 API)
- [ ] 채용공고 카드 조회
- [ ] 채용공고의 매칭된 인재 목록
- [ ] 기업 프로필 조회
- [ ] 기업의 채용공고 목록

### ✅ 매칭 시스템
- [ ] 매칭 벡터 조회 (인재/채용공고)
- [ ] 매칭 결과 정렬 (점수/날짜)
- [ ] 매칭 점수 상세 (6개 차원)
- [ ] 페이지네이션 테스트

### ✅ 데이터 무결성
- [ ] User ID 연결 확인
- [ ] Company ID ↔ JobPosting ID 확인
- [ ] JobPosting ID ↔ Card ID 확인
- [ ] Vector ID ↔ MatchingResult ID 확인

## 🛠️ 트러블슈팅

### 문제: Mock 데이터가 생성되지 않음
```bash
# DB 연결 확인
poetry run python -c "from app.db.session import SessionLocal; db = SessionLocal(); print('DB 연결 성공')"

# 마이그레이션 확인
poetry run alembic current
poetry run alembic upgrade head
```

### 문제: 중복 데이터 오류
```bash
# 기존 데이터 완전 삭제 후 재생성
poetry run python scripts/seed_mock_data.py --clean
```

### 문제: 매칭 점수가 0점
```bash
# 벡터 데이터 확인
poetry run python -c "
from app.db.session import SessionLocal
from app.models.matching_vector import MatchingVector
db = SessionLocal()
vectors = db.query(MatchingVector).all()
for v in vectors:
    print(f'User {v.user_id}: roles={v.vector_roles}')
"
```

## 📚 참고 자료

- [API 엔드포인트 전체 문서](../API_ENDPOINTS.md)
- [README](../README.md)
- [매칭 알고리즘 설명](../README.md#-매칭-알고리즘)

---

**생성일**: 2025-10-25  
**버전**: 1.0.0  
**작성자**: FitConnect Team
