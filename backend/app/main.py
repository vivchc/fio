from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.api.endpoints import router as task_router, limiter

# Hide built-in documentations in production
app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs" if settings.DEBUG else None,  
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None, 
)

app.state.limiter = limiter  # registers rate limiter so slowapi can find it for requests
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # what client receives when rate limit is hit

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,  # sets which domains are allowed to call this API
    allow_credentials=True,  # allows cookies and auth headers in cross-origin requests
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # blocks unlisted HTTP methods from the app
    allow_headers=["*"],
)

app.include_router(task_router)  # registers the routes to FastAPI's internal routing table

@app.get("/health")
def health_check():
    """ Returns app status and current environment (development, staging or production). """
    return {"status": "ok", "environment": settings.ENVIRONMENT} 