from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "Server is running smoothly"}