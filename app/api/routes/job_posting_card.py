from __future__ import annotations

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.company import Company
from app.models.job_posting import JobPosting
from app.models.job_posting_card import JobPostingCard
from app.schemas.job_posting_card import JobPostingCardCreate, JobPostingCardResponse


router = APIRouter(prefix="/api/job_posting_cards", tags=["JobPostingCard"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_job_posting_card(payload: JobPostingCardCreate, db: Session = Depends(get_db)):
    job_posting = db.get(JobPosting, payload.job_posting_id)
    if job_posting is None:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "ok": False,
                "error": {"code": "JOB_POSTING_NOT_FOUND", "message": "Job posting not found"},
            },
        )

    card = JobPostingCard(**payload.model_dump())
    db.add(card)
    db.flush()  # PK 생성을 위해 flush
    db.refresh(card)  # 관계 로딩

    response = JobPostingCardResponse.model_validate(card)
    return {"ok": True, "data": response.model_dump(mode="json")}


@router.get("/{job_posting_id}")
def get_job_posting_card(job_posting_id: int, db: Session = Depends(get_db)):
    cards = db.scalars(
        select(JobPostingCard).where(JobPostingCard.job_posting_id == job_posting_id)
    ).all()
    if not cards:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"ok": False, "error": {"code": "NOT_FOUND", "message": "Card not found"}},
        )

    response = [JobPostingCardResponse.model_validate(card) for card in cards]
    return {"ok": True, "data": [item.model_dump(mode="json") for item in response]}


@router.patch("/{job_posting_id}")
def update_job_posting_card(
    job_posting_id: int,
    payload: JobPostingCardCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Job Posting Card 전체 덮어쓰기 업데이트
    - JWT 인증 필수
    - 본인 회사의 채용공고 카드만 수정 가능
    - POST와 동일한 Body 구조 사용
    """
    # 1. JWT user_id 추출
    jwt_user_id = int(user["id"])

    # 2. 채용공고가 본인 회사 소유인지 확인
    job_posting = db.get(JobPosting, job_posting_id)
    if job_posting is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "ok": False,
                "error": {
                    "code": "JOB_POSTING_NOT_FOUND",
                    "message": f"Job posting not found for job_posting_id {job_posting_id}",
                },
            },
        )

    # 3. 회사 소유권 확인
    company = db.scalar(
        select(Company).where(
            Company.id == job_posting.company_id,
            Company.owner_user_id == jwt_user_id,
        )
    )
    if company is None:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "ok": False,
                "error": {
                    "code": "FORBIDDEN",
                    "message": "You can only update your company's job posting cards",
                },
            },
        )

    # 4. 카드 존재 확인 (첫 번째 카드만 업데이트, job_posting당 여러 카드 가능)
    card = db.scalar(
        select(JobPostingCard).where(JobPostingCard.job_posting_id == job_posting_id)
    )
    if card is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "ok": False,
                "error": {
                    "code": "CARD_NOT_FOUND",
                    "message": f"Job posting card not found for job_posting_id {job_posting_id}",
                },
            },
        )

    # 5. 전체 덮어쓰기 (payload의 모든 필드로 업데이트)
    update_data = payload.model_dump(exclude={"job_posting_id"})  # job_posting_id는 제외
    for field, value in update_data.items():
        setattr(card, field, value)

    db.flush()
    db.refresh(card)

    response = JobPostingCardResponse.model_validate(card)
    return {"ok": True, "data": response.model_dump(mode="json")}
