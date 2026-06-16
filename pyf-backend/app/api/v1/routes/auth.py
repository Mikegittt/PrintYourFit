from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import create_user, authenticate_user, create_tokens, get_user_by_email
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshTokenRequest, Token
from app.core.security import decode_token
from app.api.v1.deps import get_db

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = await create_user(db, payload)
    return create_tokens(user)


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return create_tokens(user)


@router.post("/refresh", response_model=Token)
async def refresh_token(payload: RefreshTokenRequest):
    try:
        token_data = decode_token(payload.refresh_token)
        if token_data.get("type") != "refresh":
            raise ValueError("Not a refresh token")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    # Rebuild token payload from claims
    return create_tokens(type("U", (), {
        "id": token_data["sub"],
        "full_name": token_data.get("full_name"),
        "email": token_data.get("email"),
        "role": token_data.get("role"),
        "target_campus": token_data.get("target_campus"),
        "referral_code": token_data.get("referral_code"),
        "referred_by": token_data.get("referred_by"),
        "is_active": token_data.get("is_active"),
        "kyc_completed": token_data.get("kyc_completed", False),
        "created_at": token_data.get("created_at"),
    }))


@router.post("/logout")
async def logout():
    return {"status": "logged_out"}
