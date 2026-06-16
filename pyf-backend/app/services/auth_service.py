from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import get_password_hash, verify_password, build_referral_code
from app.models.user import User
from app.models.session import Session
from app.schemas.auth import RegisterRequest, LoginRequest


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


async def create_session(db: AsyncSession, user: User, expires_days: int = 30) -> Session:
    expires_at = datetime.utcnow() + timedelta(days=expires_days)
    session = Session(user_id=user.id, expires_at=expires_at)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


async def delete_session(db: AsyncSession, session_id: str) -> None:
    session = await db.get(Session, session_id)
    if session:
        await db.delete(session)
        await db.commit()
