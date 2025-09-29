from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router


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
