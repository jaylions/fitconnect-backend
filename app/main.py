from fastapi import FastAPI
app = FastAPI(title="FitConnect API")
@app.get("/health")
def health():
    return {"ok": True, "service": "fitconnect", "status": "healthy"}
