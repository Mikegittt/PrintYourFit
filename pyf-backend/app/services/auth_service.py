from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, build_referral_code
from app.schemas.auth import RegisterRequest, LoginRequest
from app.models.user import User


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email.lower())
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_user(db: AsyncSession, user_in: RegisterRequest) -> User:
    existing = await get_user_by_email(db, user_in.email)
    if existing:
        raise ValueError("Email already registered")

    # Normalize role: AMBASSADOR -> CUSTOMER
    role = "CUSTOMER" if user_in.role in ["AMBASSADOR", "CUSTOMER"] else user_in.role

    user = User(
        full_name=user_in.full_name,
        email=user_in.email.lower(),
        hashed_password=get_password_hash(user_in.password),
        role=role,
        target_campus=user_in.target_campus,
        referral_code=build_referral_code() if role == "CUSTOMER" else None,
        is_active=True,
        kyc_completed=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, login_in: LoginRequest) -> Optional[User]:
    user = await get_user_by_email(db, login_in.email)
    if not user:
        return None
    if not verify_password(login_in.password, user.hashed_password):
        return None
    return user


def create_tokens(user: User) -> dict:
    extra_claims = {
        "full_name": getattr(user, "full_name", None),
        "email": getattr(user, "email", None),
        "role": getattr(user, "role", None),
        "target_campus": getattr(user, "target_campus", None),
        "referral_code": getattr(user, "referral_code", None),
        "referred_by": getattr(user, "referred_by", None),
        "is_active": getattr(user, "is_active", True),
        "kyc_completed": getattr(user, "kyc_completed", False),
        "created_at": getattr(user, "created_at", None),
    }
    return {
        "access_token": create_access_token(subject=str(user.id), extra_claims=extra_claims),
        "refresh_token": create_refresh_token(subject=str(user.id), extra_claims=extra_claims),
        "token_type": "bearer",
        "id": str(user.id),
    }
