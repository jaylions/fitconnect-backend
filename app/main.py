from fastapi import FastAPI

from app.api.auth import router as auth_router


app = FastAPI(title="FitConnect API")


@app.get("/health")
def health():
    return {"ok": True, "service": "fitconnect", "status": "healthy"}


app.include_router(auth_router)
