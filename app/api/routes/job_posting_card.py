from __future__ import annotations

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
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
    db.commit()
    db.refresh(card)

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
