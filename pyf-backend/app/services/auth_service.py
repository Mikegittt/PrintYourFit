from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, build_referral_code
from app.schemas.auth import RegisterRequest, LoginRequest
from uuid import UUID

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def get_user(db: AsyncSession, user_id: UUID) -> User | None:
    return await db.get(User, user_id)

async def create_user(db: AsyncSession, user_in: RegisterRequest) -> User:
    referral = build_referral_code() if user_in.role == "AMBASSADOR" else None
    user = User(
        full_name=user_in.full_name,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        target_campus=user_in.target_campus,
        referral_code=referral,
    )
    if user_in.referral_code:
        referrer = await db.execute(select(User).where(User.referral_code == user_in.referral_code))
        referrer = referrer.scalars().first()
        if referrer:
            user.referred_by = referrer.id
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def authenticate_user(db: AsyncSession, login_in: LoginRequest) -> User | None:
    user = await get_user_by_email(db, login_in.email)
    if not user:
        return None
    if not verify_password(login_in.password, user.hashed_password):
        return None
    return user

def create_tokens(user_id: str) -> dict:
    return {
        "access_token": create_access_token(subject=user_id),
        "refresh_token": create_refresh_token(subject=user_id),
        "token_type": "bearer",
    }
