#!/bin/bash

# Mock 데이터 생성 자동화 스크립트
# 사용법: ./create_mock_data.sh

set -e  # 에러 발생시 스크립트 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 설정
API_BASE_URL="http://localhost:8000"
DEFAULT_PASSWORD="password123"

# 로그 함수
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 토큰 저장 배열
declare -A TALENT_TOKENS
declare -A COMPANY_TOKENS

# ========================================
# 1. 인재 로그인
# ========================================
login_talents() {
    log_info "인재 계정 로그인 중..."
    
    for i in {1..10}; do
        email=$(printf "talent%02d@fitconnect.test" $i)
        log_info "  - $email 로그인..."
        
        response=$(curl -s -X POST "$API_BASE_URL/auth/login" \
            -H "Content-Type: application/json" \
            -d "{\"email\":\"$email\",\"password\":\"$DEFAULT_PASSWORD\"}")
        
        token=$(echo $response | jq -r '.access_token // .data.access_token // empty')
        
        if [ -z "$token" ] || [ "$token" == "null" ]; then
            log_error "    로그인 실패: $email"
            log_error "    응답: $response"
            return 1
        fi
        
        TALENT_TOKENS[$i]=$token
        log_success "    로그인 성공"
    done
}

# ========================================
# 2. 기업 로그인
# ========================================
login_companies() {
    log_info "기업 계정 로그인 중..."
    
    for i in {1..5}; do
        email=$(printf "company%02d@fitconnect.test" $i)
        log_info "  - $email 로그인..."
        
        response=$(curl -s -X POST "$API_BASE_URL/auth/login" \
            -H "Content-Type: application/json" \
            -d "{\"email\":\"$email\",\"password\":\"$DEFAULT_PASSWORD\"}")
        
        token=$(echo $response | jq -r '.access_token // .data.access_token // empty')
        
        if [ -z "$token" ] || [ "$token" == "null" ]; then
            log_error "    로그인 실패: $email"
            log_error "    응답: $response"
            return 1
        fi
        
        COMPANY_TOKENS[$i]=$token
        log_success "    로그인 성공"
    done
}

# ========================================
# 3. 인재 프로필 생성
# ========================================
create_talent_profiles() {
    log_info "인재 프로필 생성 중..."
    
    # 백엔드 개발자 #1
    log_info "  - Talent #1 (백엔드 개발자) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/talent/full" \
        -H "Authorization: Bearer ${TALENT_TOKENS[1]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "김백엔드",
                "email": "talent01@fitconnect.test",
                "birth_date": "1995-03-15",
                "phone": "010-1001-0001",
                "tagline": "Python/FastAPI 백엔드 개발 5년차",
                "is_submitted": false,
                "desired_role": "백엔드 개발자",
                "desired_salary": "6000만 ~ 8000만",
                "desired_industry": "IT/테크",
                "desired_company_size": "중견기업",
                "residence_location": "서울",
                "desired_work_location": "서울"
            },
            "educations": [{"school_name": "서울대학교", "major": "컴퓨터공학과", "status": "졸업", "start_ym": "2014-03", "end_ym": "2018-02"}],
            "experiences": [{"company_name": "네이버", "title": "백엔드 개발자", "start_ym": "2018-03", "end_ym": "2023-06", "leave_reason": "이직", "summary": "Python/Django 기반 API 개발 및 운영"}],
            "activities": [{"name": "오픈소스 기여", "category": "개발", "period_ym": "2022-01", "description": "FastAPI 공식 문서 한글 번역 기여"}],
            "certifications": [{"name": "정보처리기사", "score_or_grade": "합격", "acquired_ym": "2017-08"}],
            "documents": [],
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
    
    # 백엔드 개발자 #2
    log_info "  - Talent #2 (백엔드 개발자) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/talent/full" \
        -H "Authorization: Bearer ${TALENT_TOKENS[2]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "이서버",
                "email": "talent02@fitconnect.test",
                "birth_date": "1993-07-20",
                "phone": "010-1002-0002",
                "tagline": "Node.js/NestJS 전문 백엔드 개발자",
                "is_submitted": false,
                "desired_role": "백엔드 개발자",
                "desired_salary": "7000만 ~ 9000만",
                "desired_industry": "IT/테크",
                "desired_company_size": "대기업",
                "residence_location": "경기",
                "desired_work_location": "서울"
            },
            "educations": [{"school_name": "연세대학교", "major": "소프트웨어학과", "status": "졸업", "start_ym": "2012-03", "end_ym": "2016-02"}],
            "experiences": [{"company_name": "카카오", "title": "시니어 백엔드 개발자", "start_ym": "2016-03", "end_ym": "2023-12", "leave_reason": "커리어 전환", "summary": "Node.js/TypeScript 기반 MSA 아키텍처 설계 및 개발"}],
            "activities": [],
            "certifications": [{"name": "AWS Certified Solutions Architect", "score_or_grade": "Professional", "acquired_ym": "2020-05"}],
            "documents": [],
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
    
    # 프론트엔드 개발자 #1
    log_info "  - Talent #3 (프론트엔드 개발자) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/talent/full" \
        -H "Authorization: Bearer ${TALENT_TOKENS[3]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "박리액트",
                "email": "talent03@fitconnect.test",
                "birth_date": "1996-11-08",
                "phone": "010-1003-0003",
                "tagline": "React/TypeScript 프론트엔드 개발 4년차",
                "is_submitted": false,
                "desired_role": "프론트엔드 개발자",
                "desired_salary": "5000만 ~ 7000만",
                "desired_industry": "IT/스타트업",
                "desired_company_size": "스타트업",
                "residence_location": "서울",
                "desired_work_location": "서울"
            },
            "educations": [{"school_name": "고려대학교", "major": "정보통신학과", "status": "졸업", "start_ym": "2015-03", "end_ym": "2019-02"}],
            "experiences": [{"company_name": "토스", "title": "프론트엔드 개발자", "start_ym": "2019-07", "end_ym": "2023-08", "leave_reason": "새로운 도전", "summary": "React 기반 금융 서비스 웹/앱 개발"}],
            "activities": [{"name": "프론트엔드 스터디", "category": "개발", "period_ym": "2021-06", "description": "React 고급 패턴 및 성능 최적화 스터디 리딩"}],
            "certifications": [],
            "documents": [],
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
    
    # 프론트엔드 개발자 #2
    log_info "  - Talent #4 (프론트엔드 개발자) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/talent/full" \
        -H "Authorization: Bearer ${TALENT_TOKENS[4]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "최뷰",
                "email": "talent04@fitconnect.test",
                "birth_date": "1997-05-25",
                "phone": "010-1004-0004",
                "tagline": "Vue.js/Nuxt.js 프론트엔드 개발자",
                "is_submitted": false,
                "desired_role": "프론트엔드 개발자",
                "desired_salary": "4500만 ~ 6500만",
                "desired_industry": "IT/게임",
                "desired_company_size": "중소기업",
                "residence_location": "서울",
                "desired_work_location": "서울"
            },
            "educations": [{"school_name": "한양대학교", "major": "컴퓨터소프트웨어학부", "status": "졸업", "start_ym": "2016-03", "end_ym": "2020-02"}],
            "experiences": [{"company_name": "넷마블", "title": "프론트엔드 개발자", "start_ym": "2020-03", "end_ym": "2024-01", "leave_reason": "이직", "summary": "Vue.js 기반 게임 관리 툴 및 커뮤니티 개발"}],
            "activities": [],
            "certifications": [],
            "documents": [],
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
    
    # AI 엔지니어 #1
    log_info "  - Talent #5 (AI 엔지니어) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/talent/full" \
        -H "Authorization: Bearer ${TALENT_TOKENS[5]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "정머신",
                "email": "talent05@fitconnect.test",
                "birth_date": "1994-02-14",
                "phone": "010-1005-0005",
                "tagline": "머신러닝/딥러닝 엔지니어 6년차",
                "is_submitted": false,
                "desired_role": "AI 엔지니어",
                "desired_salary": "8000만 ~ 1억",
                "desired_industry": "AI/빅데이터",
                "desired_company_size": "대기업",
                "residence_location": "서울",
                "desired_work_location": "서울"
            },
            "educations": [
                {"school_name": "KAIST", "major": "전산학부", "status": "졸업", "start_ym": "2013-03", "end_ym": "2017-02"},
                {"school_name": "KAIST", "major": "인공지능학과", "status": "졸업", "start_ym": "2017-03", "end_ym": "2019-02"}
            ],
            "experiences": [{"company_name": "삼성전자", "title": "AI Research Engineer", "start_ym": "2019-03", "end_ym": "2024-02", "leave_reason": "스타트업 도전", "summary": "Computer Vision 및 NLP 모델 연구 개발"}],
            "activities": [{"name": "AI 논문 스터디", "category": "연구", "period_ym": "2022-01", "description": "최신 AI 논문 리뷰 및 재현 스터디"}],
            "certifications": [{"name": "TensorFlow Developer Certificate", "score_or_grade": "합격", "acquired_ym": "2020-03"}],
            "documents": [],
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
    
    # AI 엔지니어 #2
    log_info "  - Talent #6 (AI 엔지니어) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/talent/full" \
        -H "Authorization: Bearer ${TALENT_TOKENS[6]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "강데이터",
                "email": "talent06@fitconnect.test",
                "birth_date": "1995-09-30",
                "phone": "010-1006-0006",
                "tagline": "MLOps 및 데이터 파이프라인 전문가",
                "is_submitted": false,
                "desired_role": "AI 엔지니어",
                "desired_salary": "7000만 ~ 9000만",
                "desired_industry": "AI/데이터",
                "desired_company_size": "중견기업",
                "residence_location": "경기",
                "desired_work_location": "서울"
            },
            "educations": [{"school_name": "서울대학교", "major": "통계학과", "status": "졸업", "start_ym": "2014-03", "end_ym": "2018-02"}],
            "experiences": [{"company_name": "쿠팡", "title": "ML Engineer", "start_ym": "2018-07", "end_ym": "2023-12", "leave_reason": "커리어 전환", "summary": "추천 시스템 및 MLOps 파이프라인 구축"}],
            "activities": [],
            "certifications": [{"name": "Google Cloud Professional ML Engineer", "score_or_grade": "합격", "acquired_ym": "2021-08"}],
            "documents": [],
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
    
    # PM
    log_info "  - Talent #7 (PM) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/talent/full" \
        -H "Authorization: Bearer ${TALENT_TOKENS[7]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "윤프로덕트",
                "email": "talent07@fitconnect.test",
                "birth_date": "1992-06-18",
                "phone": "010-1007-0007",
                "tagline": "프로덕트 매니저 7년차, B2B SaaS 전문",
                "is_submitted": false,
                "desired_role": "프로덕트 매니저",
                "desired_salary": "8000만 ~ 1억",
                "desired_industry": "IT/SaaS",
                "desired_company_size": "중견기업",
                "residence_location": "서울",
                "desired_work_location": "서울"
            },
            "educations": [{"school_name": "성균관대학교", "major": "경영학과", "status": "졸업", "start_ym": "2011-03", "end_ym": "2015-02"}],
            "experiences": [
                {"company_name": "라인", "title": "Product Manager", "start_ym": "2015-03", "end_ym": "2020-06", "leave_reason": "이직", "summary": "메신저 기능 기획 및 프로덕트 로드맵 관리"},
                {"company_name": "배달의민족", "title": "Senior Product Manager", "start_ym": "2020-07", "end_ym": "2024-01", "leave_reason": "새로운 도전", "summary": "B2B 사장님 플랫폼 기획 및 운영"}
            ],
            "activities": [{"name": "PM 커뮤니티 운영", "category": "네트워킹", "period_ym": "2021-03", "description": "프로덕트 매니저 정기 모임 운영"}],
            "certifications": [],
            "documents": [],
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
    
    # 마케팅
    log_info "  - Talent #8 (마케팅) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/talent/full" \
        -H "Authorization: Bearer ${TALENT_TOKENS[8]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "조그로스",
                "email": "talent08@fitconnect.test",
                "birth_date": "1994-12-05",
                "phone": "010-1008-0008",
                "tagline": "퍼포먼스 마케팅 전문가, 그로스 해킹",
                "is_submitted": false,
                "desired_role": "마케팅",
                "desired_salary": "6000만 ~ 8000만",
                "desired_industry": "IT/커머스",
                "desired_company_size": "스타트업",
                "residence_location": "서울",
                "desired_work_location": "서울"
            },
            "educations": [{"school_name": "이화여자대학교", "major": "경영학과", "status": "졸업", "start_ym": "2013-03", "end_ym": "2017-02"}],
            "experiences": [{"company_name": "무신사", "title": "Performance Marketing Manager", "start_ym": "2017-07", "end_ym": "2023-09", "leave_reason": "이직", "summary": "페이스북/구글 광고 운영 및 데이터 분석"}],
            "activities": [{"name": "마케팅 컨퍼런스 발표", "category": "발표", "period_ym": "2022-11", "description": "ROAS 200% 달성한 퍼포먼스 마케팅 전략 공유"}],
            "certifications": [{"name": "Google Ads 인증", "score_or_grade": "합격", "acquired_ym": "2018-05"}],
            "documents": [],
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
    
    # HR
    log_info "  - Talent #9 (HR) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/talent/full" \
        -H "Authorization: Bearer ${TALENT_TOKENS[9]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "신인사",
                "email": "talent09@fitconnect.test",
                "birth_date": "1991-04-22",
                "phone": "010-1009-0009",
                "tagline": "HR 전문가 8년차, 채용 및 조직문화 전문",
                "is_submitted": false,
                "desired_role": "인사",
                "desired_salary": "7000만 ~ 9000만",
                "desired_industry": "IT/스타트업",
                "desired_company_size": "중견기업",
                "residence_location": "서울",
                "desired_work_location": "서울"
            },
            "educations": [{"school_name": "중앙대학교", "major": "심리학과", "status": "졸업", "start_ym": "2010-03", "end_ym": "2014-02"}],
            "experiences": [
                {"company_name": "카카오", "title": "HR Manager", "start_ym": "2014-03", "end_ym": "2019-12", "leave_reason": "이직", "summary": "개발자 채용 및 온보딩 프로세스 설계"},
                {"company_name": "당근마켓", "title": "Senior HR Manager", "start_ym": "2020-01", "end_ym": "2024-02", "leave_reason": "커리어 전환", "summary": "조직문화 개선 및 People Analytics 구축"}
            ],
            "activities": [],
            "certifications": [{"name": "SHRM-CP", "score_or_grade": "합격", "acquired_ym": "2019-06"}],
            "documents": [],
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
    
    # 경영전략
    log_info "  - Talent #10 (경영전략) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/talent/full" \
        -H "Authorization: Bearer ${TALENT_TOKENS[10]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "한전략",
                "email": "talent10@fitconnect.test",
                "birth_date": "1990-08-10",
                "phone": "010-1010-0010",
                "tagline": "경영전략 및 사업기획 전문가 10년차",
                "is_submitted": false,
                "desired_role": "경영전략",
                "desired_salary": "9000만 ~ 1억2000만",
                "desired_industry": "컨설팅/금융",
                "desired_company_size": "대기업",
                "residence_location": "서울",
                "desired_work_location": "서울"
            },
            "educations": [
                {"school_name": "서울대학교", "major": "경영학과", "status": "졸업", "start_ym": "2009-03", "end_ym": "2013-02"},
                {"school_name": "Harvard Business School", "major": "MBA", "status": "졸업", "start_ym": "2015-09", "end_ym": "2017-05"}
            ],
            "experiences": [
                {"company_name": "맥킨지", "title": "Strategy Consultant", "start_ym": "2013-03", "end_ym": "2015-08", "leave_reason": "MBA 진학", "summary": "기업 전략 컨설팅 및 실행 지원"},
                {"company_name": "네이버", "title": "전략기획 팀장", "start_ym": "2017-07", "end_ym": "2024-01", "leave_reason": "새로운 도전", "summary": "신사업 발굴 및 M&A 전략 수립"}
            ],
            "activities": [],
            "certifications": [{"name": "CFA Level 3", "score_or_grade": "합격", "acquired_ym": "2020-12"}],
            "documents": [],
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
}

# ========================================
# 4. 기업 프로필 생성
# ========================================
create_company_profiles() {
    log_info "기업 프로필 생성 중..."
    
    # Company #1
    log_info "  - Company #1 (테크이노베이션) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/company/full" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[1]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "테크이노베이션",
                "industry": "IT/소프트웨어",
                "size": "100 ~ 200명",
                "location_city": "서울",
                "homepage_url": "https://techinnovation.example.com",
                "career_page_url": "https://techinnovation.example.com/careers",
                "one_liner": "AI 기반 비즈니스 솔루션으로 미래를 설계합니다"
            },
            "about": {
                "vision_mission": "AI 기술로 비즈니스 혁신을 선도하고, 데이터 기반 의사결정 문화를 확산시킵니다.",
                "business_domains": "AI/ML 솔루션, 데이터 분석, 비즈니스 인텔리전스",
                "ideal_talent": "기술에 대한 열정과 문제 해결 능력을 갖춘 인재, 협업과 소통을 중시하는 분",
                "culture": "수평적 조직문화, 자율과 책임, 지속적인 학습과 성장",
                "benefits": "재택근무 가능, 교육비 지원, 점심/저녁 식사 제공, 최신 장비 지급"
            },
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
    
    # Company #2
    log_info "  - Company #2 (스타트업코리아) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/company/full" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[2]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "스타트업코리아",
                "industry": "IT/모바일",
                "size": "10 ~ 50명",
                "location_city": "서울",
                "homepage_url": "https://startupkorea.example.com",
                "career_page_url": "https://startupkorea.example.com/jobs",
                "one_liner": "혁신적인 모바일 경험을 만들어갑니다"
            },
            "about": {
                "vision_mission": "모바일 퍼스트 시대에 최고의 사용자 경험을 제공합니다.",
                "business_domains": "모바일 앱 개발, UI/UX 디자인, 플랫폼 서비스",
                "ideal_talent": "빠른 실행력과 주인의식을 가진 분, 스타트업 문화에 적응 가능한 분",
                "culture": "애자일 개발, 빠른 의사결정, 실패를 두려워하지 않는 도전 정신",
                "benefits": "스톡옵션, 자율 출퇴근, 간식/음료 무제한, 팀 워크샵"
            },
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
    
    # Company #3
    log_info "  - Company #3 (글로벌솔루션즈) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/company/full" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[3]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "글로벌솔루션즈",
                "industry": "제조/IT융합",
                "size": "500 ~ 1000명",
                "location_city": "경기",
                "homepage_url": "https://globalsolutions.example.com",
                "career_page_url": "https://globalsolutions.example.com/careers",
                "one_liner": "IT와 제조의 융합으로 글로벌 시장을 선도합니다"
            },
            "about": {
                "vision_mission": "스마트 팩토리와 디지털 트랜스포메이션을 통해 제조업의 미래를 만듭니다.",
                "business_domains": "스마트 제조 솔루션, IoT, 산업용 AI, MES/ERP 시스템",
                "ideal_talent": "제조와 IT 융합에 관심 있는 분, 글로벌 마인드를 가진 분",
                "culture": "안정적인 대기업 문화, 체계적인 교육 시스템, 워크라이프 밸런스",
                "benefits": "4대 보험, 퇴직연금, 사내 카페테리아, 자녀 학자금 지원, 경조사 지원"
            },
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
    
    # Company #4
    log_info "  - Company #4 (에듀테크플러스) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/company/full" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[4]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "에듀테크플러스",
                "industry": "교육/에듀테크",
                "size": "50 ~ 100명",
                "location_city": "서울",
                "homepage_url": "https://edutechplus.example.com",
                "career_page_url": "https://edutechplus.example.com/recruit",
                "one_liner": "AI로 모두를 위한 맞춤형 교육을 실현합니다"
            },
            "about": {
                "vision_mission": "기술로 교육 격차를 해소하고, 누구나 배울 수 있는 세상을 만듭니다.",
                "business_domains": "온라인 교육 플랫폼, AI 학습 추천, 교육 콘텐츠 제작",
                "ideal_talent": "교육에 대한 열정이 있는 분, 사용자 중심 사고를 가진 분",
                "culture": "임팩트 중심, 실험과 개선의 반복, 서로 배우고 성장하는 문화",
                "benefits": "도서 구매비 지원, 온라인 강의 무료, 유연 근무제, 생일 휴가"
            },
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
    
    # Company #5
    log_info "  - Company #5 (핀테크이노) 생성..."
    curl -s -X POST "$API_BASE_URL/api/me/company/full" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[5]}" \
        -H "Content-Type: application/json" \
        -d '{
            "basic": {
                "name": "핀테크이노",
                "industry": "금융/핀테크",
                "size": "200 ~ 500명",
                "location_city": "서울",
                "homepage_url": "https://fintechino.example.com",
                "career_page_url": "https://fintechino.example.com/careers",
                "one_liner": "금융의 미래를 혁신하는 핀테크 리더"
            },
            "about": {
                "vision_mission": "모든 사람에게 공정하고 편리한 금융 서비스를 제공합니다.",
                "business_domains": "디지털 뱅킹, 결제 시스템, 자산관리, 대출 플랫폼",
                "ideal_talent": "금융과 기술의 융합에 관심 있는 분, 높은 책임감과 보안 의식을 가진 분",
                "culture": "규정 준수와 혁신의 균형, 고객 중심, 데이터 기반 의사결정",
                "benefits": "연봉 상위 10%, 성과급, 건강검진, 헬스장 제휴, 주차 지원"
            },
            "submit": false
        }' > /dev/null
    log_success "    생성 완료"
}

# ========================================
# 4. 채용공고 생성
# ========================================
create_job_postings() {
    log_info "채용공고 생성 중..."
    
    # Company 01 - Job Posting 1: 백엔드 개발자
    log_info "  [1/10] 테크이노베이션 - 백엔드 개발자"
    curl -s -X POST "$API_BASE_URL/api/me/company/job-postings" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[1]}" \
        -H "Content-Type: application/json" \
        -d '{
            "title": "Python/FastAPI 백엔드 개발자",
            "employment_type": "정규직",
            "location_city": "서울",
            "career_level": "경력 3년 이상",
            "education_level": "학력무관",
            "position_group": "개발",
            "position": "백엔드 개발자",
            "department": "플랫폼개발팀",
            "start_date": "2025-11-15",
            "term_months": "정규직 (기간 제한 없음)",
            "salary_range": "6000만 ~ 8000만",
            "homepage_url": "https://techinnovation.example.com",
            "deadline_date": "2025-11-30",
            "contact_email": "recruit@techinnovation.example.com",
            "contact_phone": "02-1234-5678",
            "responsibilities": "- AI 솔루션 백엔드 API 개발 및 운영\n- 데이터베이스 설계 및 최적화\n- 성능 모니터링 및 개선\n- 마이크로서비스 아키텍처 설계",
            "requirements_must": "- Python, FastAPI 실무 경험 3년 이상\n- MySQL/PostgreSQL 등 RDBMS 설계 경험\n- RESTful API 설계 및 개발 경험\n- Git을 활용한 협업 경험",
            "requirements_nice": "- AWS, GCP 등 클라우드 인프라 경험\n- Docker, Kubernetes 사용 경험\n- CI/CD 파이프라인 구축 경험\n- Redis, Celery 등 비동기 처리 경험",
            "competencies": "Python, FastAPI, SQLAlchemy, MySQL, Docker, AWS, Redis",
            "status": "PUBLISHED"
        }' > /dev/null
    log_success "    생성 완료"
    
    # Company 01 - Job Posting 2: AI 엔지니어
    log_info "  [2/10] 테크이노베이션 - AI 엔지니어"
    curl -s -X POST "$API_BASE_URL/api/me/company/job-postings" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[1]}" \
        -H "Content-Type: application/json" \
        -d '{
            "title": "머신러닝/딥러닝 엔지니어",
            "employment_type": "정규직",
            "location_city": "서울",
            "career_level": "경력 5년 이상",
            "education_level": "대졸 이상",
            "position_group": "AI/데이터",
            "position": "AI 엔지니어",
            "department": "AI연구팀",
            "start_date": "2025-12-01",
            "term_months": "정규직 (기간 제한 없음)",
            "salary_range": "8000만 ~ 1억",
            "homepage_url": "https://techinnovation.example.com",
            "deadline_date": "2025-11-30",
            "contact_email": "ai-recruit@techinnovation.example.com",
            "contact_phone": "02-1234-5679",
            "responsibilities": "- Computer Vision 및 NLP 모델 연구 개발\n- AI 솔루션 설계 및 최적화\n- 모델 학습 파이프라인 구축\n- 논문 리서치 및 최신 기술 적용",
            "requirements_must": "- 머신러닝/딥러닝 실무 경험 5년 이상\n- PyTorch, TensorFlow 등 프레임워크 활용 능력\n- Computer Vision 또는 NLP 분야 프로젝트 경험\n- Python 고급 활용 능력",
            "requirements_nice": "- 석사 이상 학위 보유\n- 논문 게재 경험 (CVPR, NeurIPS, ACL 등)\n- MLOps 경험\n- 대규모 데이터 처리 경험",
            "competencies": "Python, PyTorch, TensorFlow, Computer Vision, NLP, MLOps",
            "status": "PUBLISHED"
        }' > /dev/null
    log_success "    생성 완료"
    
    # Company 02 - Job Posting 1: 프론트엔드 개발자 (React)
    log_info "  [3/10] 스타트업코리아 - React 프론트엔드 개발자"
    curl -s -X POST "$API_BASE_URL/api/me/company/job-postings" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[2]}" \
        -H "Content-Type: application/json" \
        -d '{
            "title": "React/TypeScript 프론트엔드 개발자",
            "employment_type": "정규직",
            "location_city": "서울",
            "career_level": "경력 3년 이상",
            "education_level": "학력무관",
            "position_group": "개발",
            "position": "프론트엔드 개발자",
            "department": "프로덕트팀",
            "start_date": "2025-11-20",
            "term_months": "정규직 (기간 제한 없음)",
            "salary_range": "5000만 ~ 7000만",
            "homepage_url": "https://startupkorea.example.com",
            "deadline_date": "2025-11-25",
            "contact_email": "jobs@startupkorea.example.com",
            "contact_phone": "02-2345-6789",
            "responsibilities": "- React 기반 모바일 웹 애플리케이션 개발\n- 컴포넌트 설계 및 재사용 가능한 라이브러리 구축\n- UI/UX 개선 및 성능 최적화\n- 백엔드 개발자와 API 협업",
            "requirements_must": "- React, TypeScript 실무 경험 3년 이상\n- HTML5, CSS3, JavaScript ES6+ 능숙\n- RESTful API 연동 경험\n- Git/GitHub 활용 능력",
            "requirements_nice": "- Next.js, Vite 등 모던 프레임워크 경험\n- 모바일 웹 최적화 경험\n- 디자인 시스템 구축 경험\n- 테스트 코드 작성 경험 (Jest, RTL)",
            "competencies": "React, TypeScript, Next.js, HTML, CSS, JavaScript",
            "status": "PUBLISHED"
        }' > /dev/null
    log_success "    생성 완료"
    
    # Company 02 - Job Posting 2: 프론트엔드 개발자 (Vue)
    log_info "  [4/10] 스타트업코리아 - Vue.js 프론트엔드 개발자"
    curl -s -X POST "$API_BASE_URL/api/me/company/job-postings" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[2]}" \
        -H "Content-Type: application/json" \
        -d '{
            "title": "Vue.js/Nuxt.js 프론트엔드 개발자",
            "employment_type": "정규직",
            "location_city": "서울",
            "career_level": "경력 2년 이상",
            "education_level": "학력무관",
            "position_group": "개발",
            "position": "프론트엔드 개발자",
            "department": "서비스개발팀",
            "start_date": "2025-12-01",
            "term_months": "정규직 (기간 제한 없음)",
            "salary_range": "4500만 ~ 6500만",
            "homepage_url": "https://startupkorea.example.com",
            "deadline_date": "2025-11-30",
            "contact_email": "jobs@startupkorea.example.com",
            "contact_phone": "02-2345-6789",
            "responsibilities": "- Vue.js 기반 웹 애플리케이션 개발\n- Nuxt.js를 활용한 SSR 구현\n- 사용자 인터페이스 개선\n- 코드 리뷰 및 기술 문서 작성",
            "requirements_must": "- Vue.js 실무 경험 2년 이상\n- JavaScript, HTML, CSS 활용 능력\n- RESTful API 통신 경험\n- 반응형 웹 개발 경험",
            "requirements_nice": "- Nuxt.js 프로젝트 경험\n- TypeScript 사용 경험\n- 상태 관리 라이브러리 경험 (Vuex, Pinia)\n- 애니메이션 및 인터랙션 구현 경험",
            "competencies": "Vue.js, Nuxt.js, JavaScript, HTML, CSS, Vuex",
            "status": "PUBLISHED"
        }' > /dev/null
    log_success "    생성 완료"
    
    # Company 03 - Job Posting 1: AI 엔지니어
    log_info "  [5/10] 글로벌솔루션즈 - MLOps 엔지니어"
    curl -s -X POST "$API_BASE_URL/api/me/company/job-postings" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[3]}" \
        -H "Content-Type: application/json" \
        -d '{
            "title": "MLOps 엔지니어 (AI/데이터 파이프라인)",
            "employment_type": "정규직",
            "location_city": "경기",
            "career_level": "경력 4년 이상",
            "education_level": "대졸 이상",
            "position_group": "AI/데이터",
            "position": "AI 엔지니어",
            "department": "스마트팩토리AI팀",
            "start_date": "2025-12-15",
            "term_months": "정규직 (기간 제한 없음)",
            "salary_range": "7000만 ~ 9000만",
            "homepage_url": "https://globalsolutions.example.com",
            "deadline_date": "2025-12-10",
            "contact_email": "hr@globalsolutions.example.com",
            "contact_phone": "031-1234-5678",
            "responsibilities": "- MLOps 파이프라인 설계 및 구축\n- 추천 시스템 및 예측 모델 개발\n- 데이터 수집 및 전처리 자동화\n- 모델 모니터링 및 성능 개선",
            "requirements_must": "- 머신러닝 프로젝트 실무 경험 4년 이상\n- Python, SQL 활용 능력\n- MLOps 도구 경험 (MLflow, Kubeflow 등)\n- 클라우드 환경에서의 ML 시스템 구축 경험",
            "requirements_nice": "- Kubernetes, Docker 활용 능력\n- Airflow, Prefect 등 워크플로우 도구 경험\n- 대규모 데이터 처리 경험 (Spark 등)\n- CI/CD 파이프라인 구축 경험",
            "competencies": "Python, MLOps, Kubernetes, Docker, Airflow, MLflow",
            "status": "PUBLISHED"
        }' > /dev/null
    log_success "    생성 완료"
    
    # Company 03 - Job Posting 2: PM
    log_info "  [6/10] 글로벌솔루션즈 - 프로덕트 매니저"
    curl -s -X POST "$API_BASE_URL/api/me/company/job-postings" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[3]}" \
        -H "Content-Type: application/json" \
        -d '{
            "title": "프로덕트 매니저 (B2B SaaS)",
            "employment_type": "정규직",
            "location_city": "경기",
            "career_level": "경력 5년 이상",
            "education_level": "대졸 이상",
            "position_group": "기획/관리",
            "position": "프로덕트 매니저",
            "department": "프로덕트전략팀",
            "start_date": "2025-11-25",
            "term_months": "정규직 (기간 제한 없음)",
            "salary_range": "8000만 ~ 1억",
            "homepage_url": "https://globalsolutions.example.com",
            "deadline_date": "2025-11-20",
            "contact_email": "pm-recruit@globalsolutions.example.com",
            "contact_phone": "031-1234-5679",
            "responsibilities": "- B2B SaaS 제품 로드맵 수립 및 관리\n- 고객 요구사항 분석 및 우선순위 결정\n- 개발팀과 협업하여 제품 기획 및 출시\n- 제품 성과 분석 및 개선 전략 수립",
            "requirements_must": "- PM 실무 경험 5년 이상\n- B2B SaaS 제품 기획 경험\n- 데이터 기반 의사결정 능력\n- 개발/디자인팀과의 협업 경험",
            "requirements_nice": "- 제조업 도메인 지식\n- SQL 활용 가능\n- Agile/Scrum 방법론 이해\n- UI/UX 기본 지식",
            "competencies": "Product Management, B2B SaaS, Data Analysis, Agile, SQL",
            "status": "PUBLISHED"
        }' > /dev/null
    log_success "    생성 완료"
    
    # Company 04 - Job Posting 1: 백엔드 개발자
    log_info "  [7/10] 에듀테크플러스 - Node.js 백엔드 개발자"
    curl -s -X POST "$API_BASE_URL/api/me/company/job-postings" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[4]}" \
        -H "Content-Type: application/json" \
        -d '{
            "title": "Node.js/NestJS 백엔드 개발자",
            "employment_type": "정규직",
            "location_city": "서울",
            "career_level": "경력 5년 이상",
            "education_level": "학력무관",
            "position_group": "개발",
            "position": "백엔드 개발자",
            "department": "플랫폼개발팀",
            "start_date": "2025-12-01",
            "term_months": "정규직 (기간 제한 없음)",
            "salary_range": "7000만 ~ 9000만",
            "homepage_url": "https://edutechplus.example.com",
            "deadline_date": "2025-11-30",
            "contact_email": "careers@edutechplus.example.com",
            "contact_phone": "02-3456-7890",
            "responsibilities": "- Node.js/TypeScript 기반 MSA 설계 및 개발\n- 교육 플랫폼 백엔드 API 개발\n- 실시간 학습 데이터 처리 시스템 구축\n- 성능 최적화 및 장애 대응",
            "requirements_must": "- Node.js, TypeScript 실무 경험 5년 이상\n- NestJS 또는 Express.js 프레임워크 경험\n- PostgreSQL, MongoDB 등 DB 설계 경험\n- MSA 아키텍처 설계 및 운영 경험",
            "requirements_nice": "- AWS 인프라 구축 경험\n- Redis, RabbitMQ 등 메시징 시스템 경험\n- GraphQL API 설계 경험\n- 교육 도메인 이해도",
            "competencies": "Node.js, NestJS, TypeScript, PostgreSQL, AWS, Redis",
            "status": "PUBLISHED"
        }' > /dev/null
    log_success "    생성 완료"
    
    # Company 04 - Job Posting 2: 마케팅
    log_info "  [8/10] 에듀테크플러스 - 퍼포먼스 마케팅 매니저"
    curl -s -X POST "$API_BASE_URL/api/me/company/job-postings" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[4]}" \
        -H "Content-Type: application/json" \
        -d '{
            "title": "퍼포먼스 마케팅 매니저 (그로스 해킹)",
            "employment_type": "정규직",
            "location_city": "서울",
            "career_level": "경력 4년 이상",
            "education_level": "학력무관",
            "position_group": "마케팅/영업",
            "position": "마케팅",
            "department": "그로스팀",
            "start_date": "2025-11-25",
            "term_months": "정규직 (기간 제한 없음)",
            "salary_range": "6000만 ~ 8000만",
            "homepage_url": "https://edutechplus.example.com",
            "deadline_date": "2025-11-20",
            "contact_email": "marketing@edutechplus.example.com",
            "contact_phone": "02-3456-7891",
            "responsibilities": "- 페이스북, 구글 등 퍼포먼스 광고 운영\n- 데이터 분석을 통한 마케팅 전략 수립\n- ROAS 최적화 및 성과 개선\n- A/B 테스트 설계 및 실행",
            "requirements_must": "- 퍼포먼스 마케팅 실무 경험 4년 이상\n- 페이스북, 구글 광고 운영 경험\n- GA, GTM 등 분석 도구 활용 능력\n- 데이터 기반 의사결정 능력",
            "requirements_nice": "- SQL 활용 가능\n- 교육/이러닝 업계 경험\n- 그로스 해킹 경험\n- CRM 마케팅 경험",
            "competencies": "Performance Marketing, Facebook Ads, Google Ads, GA, Data Analysis",
            "status": "PUBLISHED"
        }' > /dev/null
    log_success "    생성 완료"
    
    # Company 05 - Job Posting 1: HR
    log_info "  [9/10] 핀테크이노 - HR 매니저"
    curl -s -X POST "$API_BASE_URL/api/me/company/job-postings" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[5]}" \
        -H "Content-Type: application/json" \
        -d '{
            "title": "HR 매니저 (채용/조직문화)",
            "employment_type": "정규직",
            "location_city": "서울",
            "career_level": "경력 6년 이상",
            "education_level": "대졸 이상",
            "position_group": "인사/총무",
            "position": "인사",
            "department": "HR팀",
            "start_date": "2025-12-01",
            "term_months": "정규직 (기간 제한 없음)",
            "salary_range": "7000만 ~ 9000만",
            "homepage_url": "https://fintechino.example.com",
            "deadline_date": "2025-11-25",
            "contact_email": "hr@fintechino.example.com",
            "contact_phone": "02-4567-8901",
            "responsibilities": "- 개발자 및 전문 인력 채용 전략 수립 및 실행\n- 온보딩 프로세스 설계 및 운영\n- 조직문화 개선 프로그램 기획\n- People Analytics 구축 및 활용",
            "requirements_must": "- HR 실무 경험 6년 이상\n- IT/핀테크 업계 채용 경험\n- 조직문화 개선 프로젝트 경험\n- 데이터 기반 HR 운영 경험",
            "requirements_nice": "- SHRM-CP 또는 유사 자격증 보유\n- HR 시스템 구축 경험\n- 노무 관리 지식\n- 영어 커뮤니케이션 가능",
            "competencies": "Recruitment, Organizational Culture, People Analytics, HR Operations",
            "status": "PUBLISHED"
        }' > /dev/null
    log_success "    생성 완료"
    
    # Company 05 - Job Posting 2: 경영전략
    log_info "  [10/10] 핀테크이노 - 경영전략 팀장"
    curl -s -X POST "$API_BASE_URL/api/me/company/job-postings" \
        -H "Authorization: Bearer ${COMPANY_TOKENS[5]}" \
        -H "Content-Type: application/json" \
        -d '{
            "title": "경영전략 팀장 (사업기획/M&A)",
            "employment_type": "정규직",
            "location_city": "서울",
            "career_level": "경력 8년 이상",
            "education_level": "대졸 이상 (석사 우대)",
            "position_group": "경영/전략",
            "position": "경영전략",
            "department": "전략기획팀",
            "start_date": "2025-12-15",
            "term_months": "정규직 (기간 제한 없음)",
            "salary_range": "9000만 ~ 1억2000만",
            "homepage_url": "https://fintechino.example.com",
            "deadline_date": "2025-12-10",
            "contact_email": "strategy@fintechino.example.com",
            "contact_phone": "02-4567-8902",
            "responsibilities": "- 중장기 경영 전략 수립 및 실행 관리\n- 신사업 발굴 및 타당성 검토\n- M&A 전략 수립 및 실사\n- 경영진 의사결정 지원",
            "requirements_must": "- 전략 기획/컨설팅 경험 8년 이상\n- 금융/핀테크 도메인 이해도\n- 신사업 기획 및 실행 경험\n- 재무 분석 및 밸류에이션 능력",
            "requirements_nice": "- MBA 학위 보유\n- 컨설팅 펌 (MBB 등) 경력\n- CFA 또는 유사 자격증 보유\n- 영어 비즈니스 레벨",
            "competencies": "Strategy Planning, Business Development, M&A, Financial Analysis, MBA",
            "status": "PUBLISHED"
        }' > /dev/null
    log_success "    생성 완료"
    
    log_success "채용공고 10개 생성 완료"
}

# ========================================
# 메인 실행
# ========================================
main() {
    echo ""
    log_info "=========================================="
    log_info "Mock 데이터 생성 시작"
    log_info "=========================================="
    echo ""
    
    # jq 설치 확인
    if ! command -v jq &> /dev/null; then
        log_error "jq가 설치되어 있지 않습니다. 설치 후 다시 시도해주세요."
        log_info "설치 방법: sudo apt-get install jq (Ubuntu/Debian)"
        log_info "설치 방법: brew install jq (macOS)"
        exit 1
    fi
    
    # 1. 로그인
    login_talents || exit 1
    echo ""
    login_companies || exit 1
    echo ""
    
    # 2. 프로필 생성
    create_talent_profiles || exit 1
    echo ""
    create_company_profiles || exit 1
    echo ""
    
    # 3. 채용공고 생성
    create_job_postings || exit 1
    echo ""
    
    log_success "=========================================="
    log_success "Mock 데이터 생성 완료!"
    log_success "=========================================="
    echo ""
    log_info "생성된 데이터:"
    log_info "  - 인재 프로필: 10개"
    log_info "  - 기업 프로필: 5개"
    log_info "  - 채용공고: 10개 (기업당 2개)"
    echo ""
    log_warning "다음 단계:"
    log_warning "  1. Talent Card 생성 (벡터 생성 후)"
    log_warning "  2. Job Posting Card 생성 (벡터 생성 후)"
    log_warning "  3. 매칭 벡터 및 결과 생성"
    echo ""
}

# 스크립트 실행
main
