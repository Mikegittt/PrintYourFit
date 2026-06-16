import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from app.api.v1.api import api_router
from app.core.database import engine, Base
from app.core.config import settings
import app.models
from app.core.version_debug import get_versions

app = FastAPI(title="Print Your Fit API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def ensure_cors_headers(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as exc:
        traceback.print_exc()
        content = {"detail": "Internal Server Error"}
        # Temporarily expose error details for debugging (remove after fix)
        content["error"] = str(exc)
        response = JSONResponse(status_code=500, content=content)

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    content = {"detail": "Internal Server Error"}
    # Temporarily expose error details for debugging (remove after fix)
    content["error"] = str(exc)
    response = JSONResponse(status_code=500, content=content)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

app.include_router(api_router, prefix="/api/v1")

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    if settings.DEBUG:
        print("Starting Print Your Fit API")
    await create_tables()

@app.get("/")
async def root():
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/admin/orders")

# Temporary debug endpoint to report installed package versions (only enabled in DEBUG mode)
@app.get("/_debug/versions")
async def versions():
    if not settings.DEBUG:
        raise HTTPException(status_code=404, detail="Not Found")
    return get_versions()
