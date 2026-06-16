from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import create_user, authenticate_user, create_session, delete_session, get_user_by_email
from app.schemas.auth import RegisterRequest, LoginRequest, UserResponse
from app.api.v1.deps import get_db
from app.core.config import settings

router = APIRouter()

SESSION_COOKIE_NAME = "sessionid"
SESSION_EXPIRE_DAYS = 30


@router.post("/register", response_model=UserResponse)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = await create_user(db, payload)
    return user


@router.post("/login", response_model=UserResponse)
async def login(payload: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    session = await create_session(db, user, expires_days=SESSION_EXPIRE_DAYS)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session.id,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="none",
        max_age=SESSION_EXPIRE_DAYS * 24 * 60 * 60,
        expires=SESSION_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )
    return user


@router.post("/logout")
async def logout(response: Response, db: AsyncSession = Depends(get_db), session_id: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME)):
    if session_id:
        await delete_session(db, session_id)
    response.delete_cookie(SESSION_COOKIE_NAME, path="/")
    return {"status": "logged_out"}
