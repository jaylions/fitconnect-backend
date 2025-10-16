# Swagger UI 테스트 데이터

## 1단계: 탤런트 벡터 생성
**Endpoint**: `POST /api/me/matching-vectors`  
**인증**: 탤런트 유저 토큰 필요

```json
{
  "role": "talent",
  "vector_roles": {
    "vector": [0.8, 0.6, 0.7, 0.9, 0.5]
  },
  "vector_skills": {
    "vector": [0.9, 0.8, 0.7, 0.6, 0.8]
  },
  "vector_growth": {
    "vector": [0.7, 0.8, 0.6, 0.9, 0.7]
  },
  "vector_career": {
    "vector": [0.6, 0.7, 0.8, 0.5, 0.9]
  },
  "vector_vision": {
    "vector": [0.8, 0.9, 0.7, 0.6, 0.8]
  },
  "vector_culture": {
    "vector": [0.9, 0.7, 0.8, 0.8, 0.6]
  }
}
```

응답에서 **`id`** 값을 메모하세요! (예: 1)

---

## 2단계: 컴퍼니 벡터 생성
**Endpoint**: `POST /api/me/matching-vectors`  
**인증**: 컴퍼니 유저 토큰 필요

### 옵션 A: 높은 유사도 (95%+ 예상)
```json
{
  "role": "company",
  "vector_roles": {
    "vector": [0.8, 0.6, 0.7, 0.9, 0.5]
  },
  "vector_skills": {
    "vector": [0.9, 0.8, 0.7, 0.6, 0.8]
  },
  "vector_growth": {
    "vector": [0.7, 0.8, 0.6, 0.9, 0.7]
  },
  "vector_career": {
    "vector": [0.6, 0.7, 0.8, 0.5, 0.9]
  },
  "vector_vision": {
    "vector": [0.8, 0.9, 0.7, 0.6, 0.8]
  },
  "vector_culture": {
    "vector": [0.9, 0.7, 0.8, 0.8, 0.6]
  }
}
```

### 옵션 B: 중간 유사도 (70-80% 예상)
```json
{
  "role": "company",
  "vector_roles": {
    "vector": [0.5, 0.8, 0.4, 0.7, 0.6]
  },
  "vector_skills": {
    "vector": [0.6, 0.5, 0.8, 0.7, 0.6]
  },
  "vector_growth": {
    "vector": [0.4, 0.6, 0.7, 0.5, 0.8]
  },
  "vector_career": {
    "vector": [0.7, 0.4, 0.6, 0.8, 0.5]
  },
  "vector_vision": {
    "vector": [0.5, 0.7, 0.4, 0.8, 0.6]
  },
  "vector_culture": {
    "vector": [0.6, 0.5, 0.7, 0.6, 0.8]
  }
}
```

### 옵션 C: 낮은 유사도 (50-60% 예상)
```json
{
  "role": "company",
  "vector_roles": {
    "vector": [0.2, 0.9, 0.3, 0.1, 0.8]
  },
  "vector_skills": {
    "vector": [0.1, 0.2, 0.9, 0.8, 0.3]
  },
  "vector_growth": {
    "vector": [0.3, 0.1, 0.8, 0.2, 0.9]
  },
  "vector_career": {
    "vector": [0.9, 0.3, 0.1, 0.8, 0.2]
  },
  "vector_vision": {
    "vector": [0.2, 0.1, 0.9, 0.8, 0.3]
  },
  "vector_culture": {
    "vector": [0.1, 0.8, 0.2, 0.3, 0.9]
  }
}
```

응답에서 **`id`** 값을 메모하세요! (예: 2)

---

## 3단계: 벡터 매칭 실행
**Endpoint**: `POST /api/matching/vectors`  
**인증**: 아무 유저 토큰 가능

```json
{
  "source_id": 1,
  "target_id": 2
}
```

**주의**: `source_id`와 `target_id`를 1, 2단계에서 받은 실제 ID로 변경하세요!

---

## 📊 예상 결과

```json
{
  "ok": true,
  "data": {
    "source": {
      "id": 1,
      "user_id": 1,
      "role": "talent"
    },
    "target": {
      "id": 2,
      "user_id": 2,
      "role": "company"
    },
    "field_scores": {
      "vector_roles": 95.2,
      "vector_skills": 96.8,
      "vector_growth": 97.1,
      "vector_career": 94.5,
      "vector_vision": 95.9,
      "vector_culture": 96.3
    },
    "total_similarity": 95.97,
    "score": 95.97
  }
}
```

## 💡 팁

1. **Swagger UI 접속**: `http://localhost:8000/docs`
2. 우측 상단 **Authorize** 버튼으로 토큰 입력
3. 각 엔드포인트의 **Try it out** 버튼 클릭
4. 위 JSON을 Request body에 붙여넣기
5. **Execute** 버튼 클릭

## ⚠️ 주의사항

- 탤런트 벡터는 탤런트 유저 토큰으로만 생성 가능
- 컴퍼니 벡터는 컴퍼니 유저 토큰으로만 생성 가능
- 매칭은 탤런트 ↔ 컴퍼니 간에만 가능 (같은 role끼리는 불가)
- 모든 벡터 필드는 필수입니다
