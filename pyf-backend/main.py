import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.v1.api import api_router
from app.core.database import engine
from app.core.config import settings
import app.models

app = FastAPI(title="Print Your Fit API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def ensure_cors_headers(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception:
        traceback.print_exc()
        response = JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    content = {"detail": "Internal Server Error"}
    if settings.DEBUG:
        content["error"] = str(exc)
    response = JSONResponse(status_code=500, content=content)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    if settings.DEBUG:
        print("Starting Print Your Fit API")

@app.get("/")
async def root():
    return {"message": "Print Your Fit API is running"}
