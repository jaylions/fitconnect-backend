# Job Posting Enum 변경사항 (2025-10-17)

## 📋 변경 개요
`job_postings` 테이블의 주요 필드를 Enum 타입으로 변경하여 데이터 일관성과 타입 안정성을 개선했습니다.

## 🔄 변경된 필드

### 1. **location_city** (회사 위치)
- **이전**: `Text` (자유 텍스트)
- **이후**: `ENUM` (15개 지역 코드)
- **가능한 값**:
  ```
  SEOUL, GYEONGGI, INCHEON, BUSAN, DAEGU, 
  DAEJEON, GWANGJU, ULSAN, GANGWON, CHUNGBUK, 
  CHUNGNAM, JEONBUK, JEONNAM, GYEONGBUK, GYEONGNAM
  ```

### 2. **salary_range** (연봉 범위) - 신규 필드
- **타입**: `ENUM` (nullable)
- **가능한 값**:
  ```
  NEGOTIABLE      - 연봉 추후 협상
  RANGE_20_30     - 2000만 ~ 3000만
  RANGE_30_40     - 3000만 ~ 4000만
  RANGE_40_50     - 4000만 ~ 5000만
  RANGE_50_60     - 5000만 ~ 6000만
  RANGE_60_70     - 6000만 ~ 7000만
  RANGE_70_80     - 7000만 ~ 8000만
  RANGE_80_90     - 8000만 ~ 9000만
  RANGE_90_100    - 9000만 ~ 1억
  RANGE_100_120   - 1억 ~ 1.2억
  RANGE_120_150   - 1.2억 ~ 1.5억
  OVER_150        - 1.5억 이상
  ```
- **참고**: 기존 `salary_band` (JSON) 필드는 호환성을 위해 유지됨

### 3. **employment_type** (고용 형태)
- **이전**: ENUM (`FULL_TIME`, `PART_TIME`, `CONTRACT`, `INTERN`, `TEMP`, `OTHER`)
- **이후**: ENUM (`FULL_TIME`, `PART_TIME`, `CONTRACT`, `INTERN`, `OTHER`)
  - `TEMP` 제거
  - Python Enum 클래스로 정의하여 한글 레이블 매핑 가능

### 4. **competencies** (역량/기술)
- **이전**: `JSON` (배열 형태: `["Python", "FastAPI", "MySQL"]`)
- **이후**: `Text` (문자열 형태: `"Python, FastAPI, MySQL"`)

## 📁 파일 변경사항

### 새로 추가된 파일
- `app/models/enums.py` - 3개의 Enum 클래스 정의
  - `LocationEnum`
  - `SalaryRangeEnum`
  - `EmploymentTypeEnum`

### 수정된 파일
- `app/models/job_posting.py`
  - Enum import 추가
  - 컬럼 타입 변경
  - `salary_range` 컬럼 추가
  
- `app/schemas/job_posting.py`
  - Literal 타입 추가 (`LocationType`, `SalaryRange`)
  - 스키마에 `salary_range` 필드 추가
  - `competencies` 타입 변경

- `alembic/versions/20251017000000_update_job_posting_enums.py`
  - 데이터베이스 마이그레이션 스크립트

## 🚀 마이그레이션 적용 방법

### 1. 데이터베이스 백업 (권장)
```bash
# MySQL 덤프 생성
mysqldump -u [user] -p [database_name] > backup_before_migration.sql
```

### 2. 마이그레이션 실행
```bash
# DB 연결 확인
alembic current

# 마이그레이션 적용
alembic upgrade head
```

### 3. 롤백 (필요시)
```bash
# 이전 버전으로 되돌리기
alembic downgrade -1
```

## 📊 데이터 마이그레이션 로직

마이그레이션 스크립트는 기존 데이터를 자동으로 변환합니다:

### location_city 변환 규칙
```sql
'서울' or 'Seoul' → 'SEOUL'
'경기' or 'Gyeonggi' → 'GYEONGGI'
...
(기타 유사한 패턴 매칭)
매칭되지 않는 값 → 'SEOUL' (기본값)
```

### competencies 변환
- JSON 배열이 자동으로 TEXT로 변환됨
- 기존 데이터는 수동 검토 필요할 수 있음

## 🔍 API 변경사항

### Request 예시 (Swagger)

#### Job Posting 생성
```json
{
  "title": "Backend Engineer",
  "employment_type": "FULL_TIME",
  "location_city": "SEOUL",
  "salary_range": "RANGE_70_80",
  "competencies": "Python, FastAPI, MySQL, Docker",
  ...
}
```

### Response 예시
```json
{
  "ok": true,
  "data": {
    "id": 1,
    "employment_type": "FULL_TIME",
    "location_city": "SEOUL",
    "salary_range": "RANGE_70_80",
    "salary_band": {"min": 70000000, "max": 80000000},
    "competencies": "Python, FastAPI, MySQL, Docker",
    ...
  }
}
```

## ⚠️ 주의사항

1. **기존 데이터 검증 필요**
   - 마이그레이션 후 `location_city` 값이 올바르게 변환되었는지 확인
   - 매칭되지 않은 값들은 'SEOUL'로 설정됨

2. **클라이언트 코드 업데이트**
   - 프론트엔드에서 `location_city`에 enum 값 사용
   - `competencies`를 배열이 아닌 문자열로 처리

3. **salary_band vs salary_range**
   - 두 필드 모두 사용 가능 (호환성)
   - 새로운 코드는 `salary_range` 사용 권장

4. **Employment Type 매핑**
   - Python Enum의 `.value`는 한글 (예: "정규직")
   - DB와 API는 `.name` 사용 (예: "FULL_TIME")

## 🧪 테스트 체크리스트

- [ ] 마이그레이션이 에러 없이 완료되는가?
- [ ] 기존 job_posting 데이터가 올바르게 조회되는가?
- [ ] 새로운 job_posting을 생성할 수 있는가?
- [ ] Swagger UI에서 enum 선택이 정상적으로 표시되는가?
- [ ] location_city 값이 올바르게 변환되었는가?
- [ ] salary_range 필드가 정상 작동하는가?

## 📞 문의 및 이슈

문제가 발생하면 다음을 확인하세요:
1. 마이그레이션 로그 확인
2. 변환되지 않은 location_city 값 검색
3. 기존 API 호출이 새 enum 형식을 사용하는지 확인

---

**변경일**: 2025-10-17  
**브랜치**: front-fix  
**커밋**: 6e56eb0
