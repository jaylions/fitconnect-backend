from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.routes.talent import router as talent_router
from app.api.routes.company import router as company_router, public_router as company_public_router
from app.api.routes.job_posting_card import router as job_posting_card_router
from app.api.routes.talent_card import router as talent_card_router
from app.api.routes.matching_vector import router as matching_vector_router
from app.api.routes.vector_matching import router as vector_matching_router


app = FastAPI(title="FitConnect API")

origins = [
    "*"  # 개발 중에는 모두 허용, 배포시에는 프론트 도메인만 넣기
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"ok": True, "service": "fitconnect", "status": "healthy"}


app.include_router(auth_router)
app.include_router(talent_router)
app.include_router(matching_vector_router)
app.include_router(vector_matching_router)
app.include_router(company_router)
app.include_router(company_public_router)
app.include_router(job_posting_card_router)
app.include_router(talent_card_router)
