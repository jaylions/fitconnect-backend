# 📡 FitConnect API 엔드포인트 정리

## 🔐 인증 API

### 회원가입
```http
POST /auth/register
```

### 로그인
```http
POST /auth/login
```

---

## 👤 인재 (Talent) API

### 🔒 인증 필요 (Private)

#### 기본 프로필
```http
GET /api/me/talent/basic
```
- 본인의 기본 프로필 정보 (이름, 이메일, 태그라인, 관심내용 등)

#### 전체 프로필
```http
GET /api/me/talent/full
```
- 본인의 전체 프로필 (기본 정보 + 학력 + 경력 + 활동 + 자격증 + 문서)

#### 프로필 저장
```http
POST /api/me/talent/full
```
- 전체 프로필 정보 저장/업데이트

#### 학력 목록
```http
GET /api/me/talent/educations
```

#### 경력 목록
```http
GET /api/me/talent/experiences
```

#### 활동 목록
```http
GET /api/me/talent/activities
```

#### 자격증 목록
```http
GET /api/me/talent/certifications
```

#### 문서 목록
```http
GET /api/me/talent/documents
```

#### 학력 추가/수정/삭제
```http
POST   /api/me/talent/educations
PUT    /api/me/talent/educations/{education_id}
DELETE /api/me/talent/educations/{education_id}
```

#### 경력 추가/수정/삭제
```http
POST   /api/me/talent/experiences
PUT    /api/me/talent/experiences/{experience_id}
DELETE /api/me/talent/experiences/{experience_id}
```

#### 활동 추가/수정/삭제
```http
POST   /api/me/talent/activities
PUT    /api/me/talent/activities/{activity_id}
DELETE /api/me/talent/activities/{activity_id}
```

#### 자격증 추가/수정/삭제
```http
POST   /api/me/talent/certifications
PUT    /api/me/talent/certifications/{certification_id}
DELETE /api/me/talent/certifications/{certification_id}
```

#### 문서 추가/수정/삭제
```http
POST   /api/me/talent/documents
PUT    /api/me/talent/documents/{document_id}
DELETE /api/me/talent/documents/{document_id}
```

### 🌐 공개 (Public)

#### 인재 프로필 조회
```http
GET /api/talents/{user_id}/profile
```
- 인증 불필요
- 특정 인재의 전체 프로필 정보 조회

---

## 🏢 기업 (Company) API

### 🔒 인증 필요 (Private)

#### 내 기업 정보 조회
```http
GET /api/me/company
```

#### 기업 정보 저장
```http
POST /api/me/company/full
```

#### 채용공고 목록 조회
```http
GET /api/me/company/job-postings?posting_status=active
```
- Query Parameters:
  - `posting_status`: 채용공고 상태 필터 (optional)

#### 채용공고 등록
```http
POST /api/me/company/job-postings
```

#### 채용공고 수정
```http
PUT /api/me/company/job-postings/{job_posting_id}
```

#### 채용공고 삭제
```http
DELETE /api/me/company/job-postings/{job_posting_id}
```

### 🌐 공개 (Public)

#### 기업 프로필 조회
```http
GET /api/companies/{company_id}
```
- 인증 불필요
- 특정 기업의 공개 프로필 정보

#### 채용공고 상세 조회 ⭐ 추천
```http
GET /api/job-postings/{job_posting_id}
```
- 인증 불필요
- **job_posting_id만**으로 조회
- 가장 간편한 방법!

#### 채용공고 상세 조회 (레거시)
```http
GET /api/companies/{company_id}/job-postings/{job_posting_id}
```
- 인증 불필요
- 기존 경로 유지 (deprecated)

---

## 🎯 매칭 (Matching) API

### 🔒 인증 필요 (Private)

#### 인재 → 채용공고 매칭 결과
```http
GET /api/matching-results/talents/{user_id}/job-postings
```
- Query Parameters:
  - `min_score`: 최소 매칭 점수 (default: 0)
  - `limit`: 결과 개수 제한 (default: 100)
- 특정 인재에게 추천되는 채용공고 목록

#### 채용공고 → 인재 매칭 결과
```http
GET /api/matching-results/job-postings/{job_posting_id}/talents
```
- Query Parameters:
  - `min_score`: 최소 매칭 점수 (default: 0)
  - `limit`: 결과 개수 제한 (default: 100)
- 특정 채용공고에 적합한 인재 목록

#### 기업 → 인재 매칭 결과
```http
GET /api/matching-results/companies/{company_user_id}/talents
```
- Query Parameters:
  - `min_score`: 최소 매칭 점수 (default: 0)
  - `limit`: 결과 개수 제한 (default: 100)
- 특정 기업의 전체 채용공고에 적합한 인재 목록

---

## 📊 매칭 벡터 (Matching Vector) API

### 🔒 인증 필요 (Private)

#### 내 매칭 벡터 조회
```http
GET /api/me/matching-vectors
```
- 본인의 매칭 벡터 정보 (6차원 벡터)

#### 매칭 벡터 생성
```http
POST /api/matching-vectors
```

#### 매칭 벡터 수정
```http
PUT /api/matching-vectors/{vector_id}
```

#### 매칭 벡터 삭제
```http
DELETE /api/matching-vectors/{vector_id}
```

### 🌐 공개 (Public)

#### 매칭 벡터 조회
```http
GET /api/public/matching-vectors/{vector_id}
```
- 인증 불필요
- 특정 벡터 정보 조회

---

## 🎴 카드 (Card) API

### 인재 카드

#### 인재 카드 생성
```http
POST /api/talent_cards
```

#### 인재 카드 조회
```http
GET /api/talent_cards/{user_id}
```

### 채용공고 카드

#### 채용공고 카드 생성
```http
POST /api/job_posting_cards
```

#### 채용공고 카드 조회
```http
GET /api/job_posting_cards/{job_posting_id}
```

---

## 🎨 벡터 매칭 (Vector Matching) API

### 🔒 인증 필요 (Private)

#### 추천 결과 조회
```http
GET /api/matching/recommendations
```
- 본인에게 맞는 추천 결과 (인재는 채용공고, 기업은 인재)

---

## ❤️ 기타 (Health Check)

#### 서버 상태 확인
```http
GET /health
```
- 서버 헬스 체크

---

## 📝 요약

### 인증 불필요 (Public) API
- ✅ `GET /api/talents/{user_id}/profile` - 인재 프로필 조회
- ✅ `GET /api/companies/{company_id}` - 기업 프로필 조회
- ✅ `GET /api/job-postings/{job_posting_id}` - 채용공고 상세 조회 ⭐
- ✅ `GET /api/public/matching-vectors/{vector_id}` - 매칭 벡터 조회
- ✅ `GET /api/talent_cards/{user_id}` - 인재 카드 조회
- ✅ `GET /api/job_posting_cards/{job_posting_id}` - 채용공고 카드 조회
- ✅ `GET /health` - 헬스 체크

### 인증 필요 (Private) API
- 🔒 `/api/me/talent/*` - 인재 전용 API
- 🔒 `/api/me/company/*` - 기업 전용 API
- 🔒 `/api/matching-results/*` - 매칭 결과 조회
- 🔒 `/api/me/matching-vectors` - 내 매칭 벡터
- 🔒 `/api/matching/recommendations` - 추천 결과

### 주요 변경사항
- ✨ **NEW**: `GET /api/job-postings/{job_posting_id}` - job_posting_id만으로 간편 조회!
- ✨ **NEW**: `GET /api/talents/{user_id}/profile` - 인재 프로필 공개 조회
- 📌 **Deprecated**: `GET /api/companies/{company_id}/job-postings/{job_posting_id}` - 레거시 지원용

---

## 🧪 테스트 예시

### 공개 API 테스트
```bash
# 인재 프로필 조회
curl http://localhost:8000/api/talents/103/profile

# 채용공고 조회 (간편!)
curl http://localhost:8000/api/job-postings/1

# 기업 프로필 조회
curl http://localhost:8000/api/companies/1
```

### 인증 API 테스트
```bash
# 로그인
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"minsu.kim@example.com","password":"password123"}' \
  | jq -r '.access_token')

# 내 프로필 조회
curl http://localhost:8000/api/me/talent/full \
  -H "Authorization: Bearer $TOKEN"

# 매칭 결과 조회
curl "http://localhost:8000/api/matching-results/talents/103/job-postings?min_score=70&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```
