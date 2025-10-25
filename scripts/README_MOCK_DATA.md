# Mock 데이터 생성 가이드

## 🎯 목적
Vector 매칭 및 추천 API 테스트를 위한 Mock 데이터 생성

## 📦 생성되는 데이터

### 인재 유저 5명
1. **김민수** - React Frontend 개발자
   - 희망 직무: Frontend Developer
   - 희망 연봉: 4000만원 이상
   - 희망 업종: IT·인터넷
   - 희망 기업 규모: 51~200명
   - 주거 지역: 서울 강남구
   - 희망 근무 지역: 서울 전체

2. **박지현** - Java/Spring Backend 개발자
   - 희망 직무: Backend Developer
   - 희망 연봉: 5000만원 이상
   - 희망 업종: IT·인터넷
   - 희망 기업 규모: 201~500명
   - 주거 지역: 서울 서초구
   - 희망 근무 지역: 서울·경기 전체

3. **이서연** - Performance Marketer
   - 희망 직무: 마케터
   - 희망 연봉: 3500만원 이상
   - 희망 업종: 광고·마케팅
   - 희망 기업 규모: 11~50명
   - 주거 지역: 서울 마포구
   - 희망 근무 지역: 서울 서부(마포·서대문·은평)

4. **김영준** - Product Manager
   - 희망 직무: 프로덕트 매니저
   - 희망 연봉: 6000만원 이상
   - 희망 업종: IT·인터넷
   - 희망 기업 규모: 501~1,000명
   - 주거 지역: 서울 성동구
   - 희망 근무 지역: 서울 동부(성동·광진·강동)

5. **박진우** - B2B 영업 전문가
   - 희망 직무: 영업
   - 희망 연봉: 4500만원 이상
   - 희망 업종: 제조·유통
   - 희망 기업 규모: 1,001명 이상
   - 주거 지역: 경기 성남시
   - 희망 근무 지역: 경기 전체

### 기업 유저 5개 + 채용공고 5개
1. **테크스타트업** - React Frontend 개발자 모집
2. **금융테크** - Backend 개발자 (Java/Spring)
3. **마케팅에이전시** - Performance Marketer 채용
4. **이커머스플랫폼** - Product Manager 채용
5. **헬스케어스타트업** - B2B 영업 담당자 모집

### 매칭 벡터 10개
- 인재 벡터: 5개 (각 인재당 1개)
- 기업 벡터: 5개 (각 채용공고당 1개)

## 🚀 사용법

### 1. 기본 실행 (기존 데이터 유지)
```bash
poetry run python scripts/seed_mock_data.py
```

### 2. 기존 Mock 데이터 삭제 후 재생성 (권장)
```bash
poetry run python scripts/seed_mock_data.py --clean
```

## 🔐 로그인 정보

**모든 계정의 비밀번호**: `password123`

### 인재 계정
- `minsu.kim@example.com` - 김민수 (Frontend)
- `jihyun.park@example.com` - 박지현 (Backend)
- `seoyeon.lee@example.com` - 이서연 (Marketing)
- `chris.kim@example.com` - 김영준 (PM)
- `daniel.park@example.com` - 박진우 (Sales)

### 기업 계정
- `tech.startup@example.com` - 테크스타트업
- `finance.corp@example.com` - 금융테크
- `marketing.agency@example.com` - 마케팅에이전시
- `ecommerce.company@example.com` - 이커머스플랫폼
- `healthtech.startup@example.com` - 헬스케어스타트업

## 🧪 테스트 시나리오

### 1. 로그인 테스트
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "minsu.kim@example.com",
    "password": "password123"
  }'
```

### 2. 매칭 벡터 조회
```bash
# 토큰 받아서
TOKEN="your_access_token_here"

# 매칭 벡터 조회
curl -X GET http://localhost:8000/api/me/matching-vectors \
  -H "Authorization: Bearer $TOKEN"
```

### 3. 추천 결과 조회 (인재 → 기업)
```bash
# 김민수(Frontend) 계정으로 로그인 후
curl -X GET http://localhost:8000/api/matching/recommendations \
  -H "Authorization: Bearer $TOKEN"
```

### 4. 추천 결과 조회 (기업 → 인재)
```bash
# 테크스타트업 계정으로 로그인 후
curl -X GET http://localhost:8000/api/matching/recommendations \
  -H "Authorization: Bearer $TOKEN"
```

## 📊 벡터 데이터 구조

각 매칭 벡터는 6개 차원으로 구성:
```json
{
  "vector_roles": {"dim": 5, "vector": [0.9, 0.8, 0.7, 0.6, 0.5]},
  "vector_skills": {"dim": 5, "vector": [0.95, 0.9, 0.85, 0.8, 0.75]},
  "vector_growth": {"dim": 5, "vector": [0.8, 0.7, 0.75, 0.85, 0.7]},
  "vector_career": {"dim": 5, "vector": [0.7, 0.8, 0.6, 0.75, 0.85]},
  "vector_vision": {"dim": 5, "vector": [0.85, 0.8, 0.75, 0.7, 0.8]},
  "vector_culture": {"dim": 5, "vector": [0.8, 0.85, 0.7, 0.75, 0.9]}
}
```

## 🎨 매칭 예상 결과

### 김민수 (Frontend) ↔ 테크스타트업
- **높은 매칭**: React 전문 Frontend 개발자 ↔ React Frontend 개발자 모집
- 벡터 유사도가 높게 설계됨

### 박지현 (Backend) ↔ 금융테크
- **높은 매칭**: Java/Spring 전문 Backend 개발자 ↔ Backend 개발자 (Java/Spring)
- 경력 및 스킬 벡터가 유사하게 설계됨

### 이서연 (Marketer) ↔ 마케팅에이전시
- **높은 매칭**: Performance Marketer ↔ Performance Marketer 채용
- Growth 및 Culture 벡터 유사도 높음

### 김영준 (PM) ↔ 이커머스플랫폼
- **높은 매칭**: Product Manager ↔ Product Manager 채용
- Vision 및 Career 벡터 유사도 높음

### 박진우 (Sales) ↔ 헬스케어스타트업
- **높은 매칭**: B2B 영업 전문가 ↔ B2B 영업 담당자
- Culture 및 Vision 벡터 유사도 높음

## 🔍 데이터 확인

### DB에서 직접 확인
```bash
# 전체 유저 수
poetry run python -c "from app.db.session import SessionLocal; from app.models.user import User; db = SessionLocal(); print(f'Users: {db.query(User).count()}'); db.close()"

# 매칭 벡터 수
poetry run python -c "from app.db.session import SessionLocal; from app.models.matching_vector import MatchingVector; db = SessionLocal(); print(f'Vectors: {db.query(MatchingVector).count()}'); db.close()"

# 채용 공고 수
poetry run python -c "from app.db.session import SessionLocal; from app.models.job_posting import JobPosting; db = SessionLocal(); print(f'Job Postings: {db.query(JobPosting).count()}'); db.close()"
```

## ⚠️ 주의사항

1. **비밀번호**: 모든 계정이 `password123`로 동일 (테스트용)
2. **데이터 정리**: `--clean` 옵션 사용 시 기존 Mock 계정 삭제
3. **프로덕션 사용 금지**: 테스트 환경에서만 사용

## 🛠️ 문제 해결

### 스크립트 실행 오류
```bash
# 권한 문제
chmod +x scripts/seed_mock_data.py

# 모듈 import 오류
poetry install
```

### 데이터 중복 오류
```bash
# 기존 데이터 삭제 후 재생성
poetry run python scripts/seed_mock_data.py --clean
```

## 📝 커스터마이징

스크립트 내부의 데이터를 수정하여 다른 시나리오 테스트 가능:
- `create_talent_users()`: 인재 데이터 수정
- `create_company_users()`: 기업 및 채용공고 데이터 수정
- 벡터 값 조정으로 매칭 결과 변경 가능
