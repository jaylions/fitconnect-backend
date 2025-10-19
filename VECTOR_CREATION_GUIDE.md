# 매칭 벡터 생성 가이드 (Vector Creation Guide)

> **대상**: 벡터 생성 담당자  
> **최종 업데이트**: 2025-10-19  
> **중요**: 이 문서를 반드시 숙지한 후 벡터를 생성하세요!

---

## 📋 목차
1. [개요](#개요)
2. [벡터 구조 이해하기](#벡터-구조-이해하기)
3. [API 사용 방법](#api-사용-방법)
4. [주의사항 및 제약사항](#주의사항-및-제약사항)
5. [에러 처리](#에러-처리)
6. [예시 코드](#예시-코드)

---

## 개요

### 벡터란?
- 매칭 시스템에서 사용하는 **다차원 숫자 배열**
- 인재(Talent)와 채용공고(Job Posting) 간의 유사도를 계산하는 데 사용
- 6개의 카테고리로 구성: roles, skills, growth, career, vision, culture

### 벡터 생성 규칙
| 구분 | user당 벡터 개수 | job_posting_id 필요 여부 |
|------|------------------|------------------------|
| **Talent (인재)** | **1개** | ❌ 불필요 (NULL) |
| **Company (기업)** | **채용공고당 1개** | ✅ 필수 |

---

## 벡터 구조 이해하기

### 1. 벡터 차원
- **현재 기본 차원**: 5차원
- **유연성**: N차원 지원 (5, 10, 50, 100차원 등 가능)
- **제약**: source와 target 벡터의 차원은 반드시 동일해야 함

### 2. 벡터 카테고리 (6개)

```json
{
  "vector_roles": {"vector": [0.9, 0.8, 0.7, 0.6, 0.5]},      // 직무/역할 관련
  "vector_skills": {"vector": [0.95, 0.9, 0.85, 0.8, 0.75]},  // 기술/스킬 관련
  "vector_growth": {"vector": [0.8, 0.7, 0.75, 0.85, 0.7]},   // 성장 가능성 관련
  "vector_career": {"vector": [0.7, 0.8, 0.6, 0.75, 0.85]},   // 커리어 패스 관련
  "vector_vision": {"vector": [0.85, 0.8, 0.75, 0.7, 0.8]},   // 비전/목표 관련
  "vector_culture": {"vector": [0.8, 0.85, 0.7, 0.75, 0.9]}   // 문화/가치관 관련
}
```

### 3. 벡터 값 범위
- **권장 범위**: 0.0 ~ 1.0 (정규화된 값)
- **실제 제약**: 어떤 숫자든 가능하지만 0~1 사이를 권장
- **Zero Vector 금지**: [0, 0, 0, 0, 0] 같은 영벡터는 매칭 불가 (에러 발생)

---

## API 사용 방법

### 📍 엔드포인트
```
POST /api/me/matching-vectors
Authorization: Bearer <access_token>
```

### 1️⃣ Talent (인재) 벡터 생성

#### Request Body
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

#### ⚠️ 주의사항
- ❌ `job_posting_id` 필드를 **포함하지 마세요**
- ✅ `role`은 반드시 `"talent"`
- ✅ 한 인재당 벡터는 **1개만** 생성 가능
- ✅ 중복 생성 시도 시 409 Conflict 에러

#### Response (성공)
```json
{
  "ok": true,
  "data": {
    "id": 123,
    "user_id": 456,
    "role": "talent",
    "job_posting_id": null,
    "vector_roles": {"vector": [0.9, 0.8, 0.7, 0.6, 0.5]},
    "vector_skills": {"vector": [0.95, 0.9, 0.85, 0.8, 0.75]},
    "vector_growth": {"vector": [0.8, 0.7, 0.75, 0.85, 0.7]},
    "vector_career": {"vector": [0.7, 0.8, 0.6, 0.75, 0.85]},
    "vector_vision": {"vector": [0.85, 0.8, 0.75, 0.7, 0.8]},
    "vector_culture": {"vector": [0.8, 0.85, 0.7, 0.75, 0.9]},
    "updated_at": "2025-10-19T12:34:56"
  }
}
```

---

### 2️⃣ Company (기업) 벡터 생성

#### Request Body
```json
{
  "role": "company",
  "job_posting_id": 789,
  "vector_roles": {"vector": [0.85, 0.9, 0.8, 0.75, 0.7]},
  "vector_skills": {"vector": [0.9, 0.95, 0.85, 0.9, 0.8]},
  "vector_growth": {"vector": [0.9, 0.85, 0.8, 0.9, 0.75]},
  "vector_career": {"vector": [0.8, 0.85, 0.75, 0.8, 0.9]},
  "vector_vision": {"vector": [0.88, 0.82, 0.78, 0.85, 0.9]},
  "vector_culture": {"vector": [0.75, 0.8, 0.85, 0.9, 0.7]}
}
```

#### ⚠️ 주의사항
- ✅ `job_posting_id` 필드는 **필수**
- ✅ `role`은 반드시 `"company"`
- ✅ `job_posting_id`는 반드시 **본인 회사 소유의 채용공고 ID**여야 함
- ✅ 같은 채용공고에 대해 벡터는 **1개만** 생성 가능
- ❌ 다른 회사의 채용공고 ID 사용 시 403 Forbidden 에러
- ✅ 여러 채용공고를 운영하면 **각 공고마다 별도 벡터 생성 가능**

#### Response (성공)
```json
{
  "ok": true,
  "data": {
    "id": 124,
    "user_id": 457,
    "role": "company",
    "job_posting_id": 789,
    "vector_roles": {"vector": [0.85, 0.9, 0.8, 0.75, 0.7]},
    "vector_skills": {"vector": [0.9, 0.95, 0.85, 0.9, 0.8]},
    "vector_growth": {"vector": [0.9, 0.85, 0.8, 0.9, 0.75]},
    "vector_career": {"vector": [0.8, 0.85, 0.75, 0.8, 0.9]},
    "vector_vision": {"vector": [0.88, 0.82, 0.78, 0.85, 0.9]},
    "vector_culture": {"vector": [0.75, 0.8, 0.85, 0.9, 0.7]},
    "updated_at": "2025-10-19T12:35:00"
  }
}
```

---

### 3️⃣ 벡터 조회 (Public API - 인증 불필요)

#### 엔드포인트
```
GET /api/public/matching-vectors/{vector_id}
```

#### Request
```bash
curl http://localhost:8000/api/public/matching-vectors/123
```

#### Response
```json
{
  "ok": true,
  "data": {
    "id": 123,
    "user_id": 456,
    "role": "talent",
    "job_posting_id": null,
    "reference_type": "talent",
    "reference_id": 101,
    "vector_roles": {"vector": [0.9, 0.8, 0.7, 0.6, 0.5]},
    "vector_skills": {"vector": [0.95, 0.9, 0.85, 0.8, 0.75]},
    "vector_growth": {"vector": [0.8, 0.7, 0.75, 0.85, 0.7]},
    "vector_career": {"vector": [0.7, 0.8, 0.6, 0.75, 0.85]},
    "vector_vision": {"vector": [0.85, 0.8, 0.75, 0.7, 0.8]},
    "vector_culture": {"vector": [0.8, 0.85, 0.7, 0.75, 0.9]},
    "updated_at": "2025-10-19T12:34:56"
  }
}
```

---

## 주의사항 및 제약사항

### ⚠️ 필수 체크리스트

#### Talent 벡터 생성 시
- [ ] `role`이 `"talent"`인지 확인
- [ ] `job_posting_id` 필드를 포함하지 않았는지 확인
- [ ] 6개 카테고리 벡터를 모두 제공했는지 확인
- [ ] 각 벡터의 차원이 동일한지 확인 (예: 모두 5차원)
- [ ] 영벡터([0,0,0,0,0])가 없는지 확인
- [ ] 이미 벡터를 생성한 적이 없는지 확인 (1인 1벡터)

#### Company 벡터 생성 시
- [ ] `role`이 `"company"`인지 확인
- [ ] `job_posting_id`를 필수로 제공했는지 확인
- [ ] `job_posting_id`가 본인 회사 소유인지 확인
- [ ] 6개 카테고리 벡터를 모두 제공했는지 확인
- [ ] 각 벡터의 차원이 동일한지 확인 (예: 모두 5차원)
- [ ] 영벡터([0,0,0,0,0])가 없는지 확인
- [ ] 해당 채용공고에 이미 벡터가 없는지 확인

### 🚫 자주 하는 실수

| 실수 | 설명 | 해결 방법 |
|------|------|----------|
| **1. job_posting_id 누락** | Company인데 job_posting_id 안 보냄 | 필수로 포함하세요 |
| **2. 잘못된 job_posting_id** | 다른 회사의 채용공고 ID 사용 | 본인 회사 공고만 사용 |
| **3. Talent에 job_posting_id 포함** | Talent인데 job_posting_id 보냄 | 절대 포함하지 마세요 |
| **4. 차원 불일치** | roles는 5차원, skills는 3차원 | 모든 벡터를 같은 차원으로 |
| **5. 영벡터 사용** | [0, 0, 0, 0, 0] 전송 | 최소 하나는 0이 아닌 값 |
| **6. 중복 생성** | 이미 있는데 또 생성 시도 | PATCH로 업데이트 사용 |

---

## 에러 처리

### 에러 응답 형식
```json
{
  "ok": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "에러 설명"
  }
}
```

### 주요 에러 코드

| HTTP Status | Error Code | 발생 상황 | 해결 방법 |
|-------------|------------|----------|----------|
| **400** | INVALID_VECTOR_DATA | 벡터 형식 오류 | 벡터 형식 확인 (리스트, 숫자만) |
| **403** | FORBIDDEN | 다른 회사의 job_posting 사용 | 본인 회사 공고 ID 사용 |
| **403** | FORBIDDEN_ROLE | role이 user role과 불일치 | user role 확인 |
| **404** | JOB_POSTING_NOT_FOUND | 존재하지 않는 job_posting_id | 유효한 ID 사용 |
| **409** | MATCHING_VECTOR_EXISTS | 이미 벡터가 존재함 | PATCH로 업데이트하거나 기존 사용 |
| **422** | JOB_POSTING_ID_REQUIRED | company인데 job_posting_id 없음 | job_posting_id 추가 |
| **422** | JOB_POSTING_ID_NOT_ALLOWED | talent인데 job_posting_id 있음 | job_posting_id 제거 |
| **422** | VECTOR_DIMENSION_MISMATCH | 벡터 차원이 다름 | 모든 벡터를 같은 차원으로 |
| **422** | ZERO_VECTOR | 영벡터 사용 | 0이 아닌 값 포함 |
| **422** | INCOMPLETE_VECTOR_FIELDS | 6개 중 일부 누락 | 6개 모두 제공 |

### 에러 예시

#### 1. Company인데 job_posting_id 누락
```json
// Request
{
  "role": "company",
  "vector_roles": {"vector": [0.9, 0.8, 0.7, 0.6, 0.5]}
}

// Response (422)
{
  "ok": false,
  "error": {
    "code": "JOB_POSTING_ID_REQUIRED",
    "message": "job_posting_id is required for company role"
  }
}
```

#### 2. 중복 생성 시도
```json
// Response (409)
{
  "ok": false,
  "error": {
    "code": "MATCHING_VECTOR_EXISTS",
    "message": "Matching vector already exists for job posting 789"
  }
}
```

#### 3. 다른 회사의 채용공고 사용
```json
// Response (403)
{
  "ok": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "Job posting does not belong to you"
  }
}
```

---

## 예시 코드

### Python 예시

```python
import requests

BASE_URL = "http://localhost:8000"
ACCESS_TOKEN = "your_access_token_here"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# 1. Talent 벡터 생성
def create_talent_vector():
    payload = {
        "role": "talent",
        "vector_roles": {"vector": [0.9, 0.8, 0.7, 0.6, 0.5]},
        "vector_skills": {"vector": [0.95, 0.9, 0.85, 0.8, 0.75]},
        "vector_growth": {"vector": [0.8, 0.7, 0.75, 0.85, 0.7]},
        "vector_career": {"vector": [0.7, 0.8, 0.6, 0.75, 0.85]},
        "vector_vision": {"vector": [0.85, 0.8, 0.75, 0.7, 0.8]},
        "vector_culture": {"vector": [0.8, 0.85, 0.7, 0.75, 0.9]}
    }
    
    response = requests.post(
        f"{BASE_URL}/api/me/matching-vectors",
        json=payload,
        headers=headers
    )
    
    if response.status_code == 201:
        print("✅ Talent 벡터 생성 성공!")
        print(f"Vector ID: {response.json()['data']['id']}")
    else:
        print(f"❌ 에러: {response.json()['error']}")
    
    return response.json()


# 2. Company 벡터 생성 (채용공고 ID: 789)
def create_company_vector(job_posting_id):
    payload = {
        "role": "company",
        "job_posting_id": job_posting_id,
        "vector_roles": {"vector": [0.85, 0.9, 0.8, 0.75, 0.7]},
        "vector_skills": {"vector": [0.9, 0.95, 0.85, 0.9, 0.8]},
        "vector_growth": {"vector": [0.9, 0.85, 0.8, 0.9, 0.75]},
        "vector_career": {"vector": [0.8, 0.85, 0.75, 0.8, 0.9]},
        "vector_vision": {"vector": [0.88, 0.82, 0.78, 0.85, 0.9]},
        "vector_culture": {"vector": [0.75, 0.8, 0.85, 0.9, 0.7]}
    }
    
    response = requests.post(
        f"{BASE_URL}/api/me/matching-vectors",
        json=payload,
        headers=headers
    )
    
    if response.status_code == 201:
        print(f"✅ Company 벡터 생성 성공! (Job Posting: {job_posting_id})")
        print(f"Vector ID: {response.json()['data']['id']}")
    else:
        print(f"❌ 에러: {response.json()['error']}")
    
    return response.json()


# 3. 벡터 조회 (인증 불필요)
def get_vector_detail(vector_id):
    response = requests.get(
        f"{BASE_URL}/api/public/matching-vectors/{vector_id}"
    )
    
    if response.status_code == 200:
        data = response.json()['data']
        print(f"✅ Vector ID {vector_id} 조회 성공!")
        print(f"Role: {data['role']}")
        print(f"Job Posting ID: {data.get('job_posting_id', 'N/A')}")
        print(f"Vector Roles: {data['vector_roles']}")
    else:
        print(f"❌ 에러: {response.json()['error']}")
    
    return response.json()


# 실행 예시
if __name__ == "__main__":
    # Talent 벡터 생성
    talent_result = create_talent_vector()
    
    # Company 벡터 생성 (채용공고별로)
    company_result_1 = create_company_vector(job_posting_id=789)
    company_result_2 = create_company_vector(job_posting_id=790)
    
    # 벡터 조회
    if talent_result.get('ok'):
        vector_id = talent_result['data']['id']
        get_vector_detail(vector_id)
```

### JavaScript 예시

```javascript
const BASE_URL = "http://localhost:8000";
const ACCESS_TOKEN = "your_access_token_here";

const headers = {
  "Authorization": `Bearer ${ACCESS_TOKEN}`,
  "Content-Type": "application/json"
};

// 1. Talent 벡터 생성
async function createTalentVector() {
  const payload = {
    role: "talent",
    vector_roles: { vector: [0.9, 0.8, 0.7, 0.6, 0.5] },
    vector_skills: { vector: [0.95, 0.9, 0.85, 0.8, 0.75] },
    vector_growth: { vector: [0.8, 0.7, 0.75, 0.85, 0.7] },
    vector_career: { vector: [0.7, 0.8, 0.6, 0.75, 0.85] },
    vector_vision: { vector: [0.85, 0.8, 0.75, 0.7, 0.8] },
    vector_culture: { vector: [0.8, 0.85, 0.7, 0.75, 0.9] }
  };
  
  const response = await fetch(`${BASE_URL}/api/me/matching-vectors`, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(payload)
  });
  
  const result = await response.json();
  
  if (response.status === 201) {
    console.log("✅ Talent 벡터 생성 성공!");
    console.log(`Vector ID: ${result.data.id}`);
  } else {
    console.error("❌ 에러:", result.error);
  }
  
  return result;
}

// 2. Company 벡터 생성
async function createCompanyVector(jobPostingId) {
  const payload = {
    role: "company",
    job_posting_id: jobPostingId,
    vector_roles: { vector: [0.85, 0.9, 0.8, 0.75, 0.7] },
    vector_skills: { vector: [0.9, 0.95, 0.85, 0.9, 0.8] },
    vector_growth: { vector: [0.9, 0.85, 0.8, 0.9, 0.75] },
    vector_career: { vector: [0.8, 0.85, 0.75, 0.8, 0.9] },
    vector_vision: { vector: [0.88, 0.82, 0.78, 0.85, 0.9] },
    vector_culture: { vector: [0.75, 0.8, 0.85, 0.9, 0.7] }
  };
  
  const response = await fetch(`${BASE_URL}/api/me/matching-vectors`, {
    method: "POST",
    headers: headers,
    body: JSON.stringify(payload)
  });
  
  const result = await response.json();
  
  if (response.status === 201) {
    console.log(`✅ Company 벡터 생성 성공! (Job Posting: ${jobPostingId})`);
    console.log(`Vector ID: ${result.data.id}`);
  } else {
    console.error("❌ 에러:", result.error);
  }
  
  return result;
}

// 3. 벡터 조회 (인증 불필요)
async function getVectorDetail(vectorId) {
  const response = await fetch(`${BASE_URL}/api/public/matching-vectors/${vectorId}`);
  const result = await response.json();
  
  if (response.status === 200) {
    console.log(`✅ Vector ID ${vectorId} 조회 성공!`);
    console.log(`Role: ${result.data.role}`);
    console.log(`Job Posting ID: ${result.data.job_posting_id || 'N/A'}`);
    console.log(`Vector Roles:`, result.data.vector_roles);
  } else {
    console.error("❌ 에러:", result.error);
  }
  
  return result;
}

// 실행 예시
(async () => {
  // Talent 벡터 생성
  const talentResult = await createTalentVector();
  
  // Company 벡터 생성 (채용공고별로)
  await createCompanyVector(789);
  await createCompanyVector(790);
  
  // 벡터 조회
  if (talentResult.ok) {
    await getVectorDetail(talentResult.data.id);
  }
})();
```

---

## 📊 비즈니스 시나리오

### 시나리오 1: 한 기업이 여러 채용공고 운영

```
퓨처테크 (Company User ID: 100)
├── Frontend 개발자 채용 (Job Posting ID: 201)
│   └── Vector ID: 301 (FE 특화 벡터)
├── Backend 개발자 채용 (Job Posting ID: 202)
│   └── Vector ID: 302 (BE 특화 벡터)
└── PM 채용 (Job Posting ID: 203)
    └── Vector ID: 303 (PM 특화 벡터)
```

각 채용공고마다 다른 요구사항(벡터)를 설정할 수 있습니다!

### 시나리오 2: 인재 매칭 프로세스

```
김민수 (Talent User ID: 50)
└── Vector ID: 401 (FE 개발자 역량 벡터)

매칭 수행:
- Vector 401 (김민수) ↔ Vector 301 (퓨처테크 FE) → 95% 매칭
- Vector 401 (김민수) ↔ Vector 302 (퓨처테크 BE) → 72% 매칭
- Vector 401 (김민수) ↔ Vector 303 (퓨처테크 PM) → 65% 매칭

→ 김민수는 퓨처테크의 FE 개발자 채용에 가장 적합!
```

---

## 🔗 관련 API

| API | 설명 | 인증 필요 |
|-----|------|----------|
| `POST /api/me/matching-vectors` | 벡터 생성 | ✅ Yes |
| `PATCH /api/me/matching-vectors/{id}` | 벡터 수정 | ✅ Yes |
| `DELETE /api/me/matching-vectors/{id}` | 벡터 삭제 | ✅ Yes |
| `GET /api/public/matching-vectors/{id}` | 벡터 조회 | ❌ No |
| `POST /api/matching/vectors` | 매칭 수행 | ❌ No |

---

## 💡 Best Practices

### 1. 벡터 값 설정 팁
- **0.9 ~ 1.0**: 매우 중요하거나 강점인 영역
- **0.7 ~ 0.8**: 중요하거나 관심 있는 영역
- **0.5 ~ 0.6**: 보통 수준
- **0.3 ~ 0.4**: 중요도가 낮은 영역
- **0.0 ~ 0.2**: 거의 관심 없거나 약점

### 2. 차원 선택 가이드
- **5차원**: 간단한 매칭, 빠른 처리
- **10차원**: 표준적인 정밀도
- **50차원**: 높은 정밀도 필요 시
- **100차원**: 매우 정밀한 매칭 필요 시

### 3. 에러 발생 시 체크리스트
1. [ ] role이 올바른가? (talent/company)
2. [ ] job_posting_id 규칙을 지켰는가?
3. [ ] 6개 벡터를 모두 제공했는가?
4. [ ] 모든 벡터의 차원이 같은가?
5. [ ] 영벡터가 없는가?
6. [ ] 중복 생성이 아닌가?

---

## 📞 문의

벡터 생성 중 문제가 발생하면:
1. 이 문서의 체크리스트를 먼저 확인
2. 에러 코드와 메시지 확인
3. 예시 코드와 비교
4. 그래도 해결 안 되면 백엔드 팀에 문의

---

**작성자**: Backend Team  
**버전**: 1.0.0  
**최종 수정**: 2025-10-19
