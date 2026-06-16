from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, build_referral_code
from app.schemas.auth import RegisterRequest, LoginRequest

_users: dict[str, dict] = {}

async def get_user_by_email(email: str) -> dict | None:
    return _users.get(email.lower())

async def create_user(user_in: RegisterRequest) -> dict:
    if await get_user_by_email(user_in.email):
        raise ValueError("Email already registered")

    user_id = uuid4()
    user = {
        "id": user_id,
        "full_name": user_in.full_name,
        "email": user_in.email,
        "hashed_password": get_password_hash(user_in.password),
        "role": user_in.role,
        "target_campus": user_in.target_campus,
        "referral_code": build_referral_code() if user_in.role == "AMBASSADOR" else None,
        "referred_by": None,
        "is_active": True,
        "created_at": datetime.utcnow().isoformat(),
    }
    _users[user_in.email.lower()] = user
    return user

async def authenticate_user(login_in: LoginRequest) -> dict | None:
    user = await get_user_by_email(login_in.email)
    if not user:
        return None
    if not verify_password(login_in.password, user["hashed_password"]):
        return None
    return user

def create_tokens(user: dict) -> dict:
    extra_claims = {
        "full_name": user["full_name"],
        "email": user["email"],
        "role": user["role"],
        "target_campus": user["target_campus"],
        "referral_code": user["referral_code"],
        "referred_by": user["referred_by"],
        "is_active": user["is_active"],
        "created_at": user["created_at"],
    }
    return {
        "access_token": create_access_token(subject=str(user["id"]), extra_claims=extra_claims),
        "refresh_token": create_refresh_token(subject=str(user["id"]), extra_claims=extra_claims),
        "token_type": "bearer",
    }
