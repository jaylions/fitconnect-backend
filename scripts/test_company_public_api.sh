#!/bin/bash

# 색상 정의
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}공개 기업 프로필 조회 API 테스트${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 테스트할 user_id (기업 계정의 user_id)
# 실제 테스트 시에는 데이터베이스에 존재하는 user_id를 사용해야 합니다
USER_ID="${USER_ID:-11}"

echo -e "${GREEN}[1] GET /api/companies/user/${USER_ID}${NC}"
echo -e "${BLUE}공개 기업 프로필 조회 (인증 불필요)${NC}"
curl -X GET "${BASE_URL}/api/companies/user/${USER_ID}" \
  -H "Content-Type: application/json" \
  -w "\n\nHTTP Status: %{http_code}\n" | jq '.'

echo ""
echo -e "${GREEN}테스트 완료!${NC}"
echo ""
echo -e "${BLUE}다른 user_id로 테스트하려면:${NC}"
echo -e "USER_ID=12 ./scripts/test_company_public_api.sh"
